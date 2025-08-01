---
title: REL05-BP05 - Set client timeouts
layout: default
parent: REL05 - How do you design interactions in a distributed system to mitigate or withstand failures?
grand_parent: Reliability
nav_order: 5
---

# REL05-BP05: Set client timeouts

## Overview

Configure appropriate client timeouts for all network operations to prevent indefinite blocking and resource exhaustion. Proper timeout configuration ensures that clients can detect failures quickly, free up resources, and implement appropriate fallback strategies when services become unresponsive.

## Implementation Steps

### 1. Configure Connection Timeouts
- Set connection establishment timeouts for all network calls
- Configure different timeouts for different service types and criticality levels
- Implement timeout values based on network latency and service SLAs
- Design timeout escalation for retry scenarios

### 2. Establish Read and Write Timeouts
- Configure read timeouts for data retrieval operations
- Set write timeouts for data submission operations
- Implement different timeouts for streaming vs batch operations
- Design timeout handling for long-running operations

### 3. Implement Request-Level Timeouts
- Set end-to-end request timeouts including all retry attempts
- Configure per-operation timeouts based on expected processing time
- Implement timeout propagation across service boundaries
- Design timeout budgets for complex workflows

### 4. Configure Service-Specific Timeouts
- Set database connection and query timeouts
- Configure cache operation timeouts
- Implement API call timeouts with appropriate values
- Design timeout strategies for third-party service integrations

### 5. Implement Timeout Monitoring and Alerting
- Track timeout occurrences and patterns
- Monitor timeout effectiveness and false positives
- Implement automated timeout tuning based on performance data
- Create dashboards for timeout metrics and analysis

### 6. Design Timeout Error Handling
- Implement graceful timeout error handling
- Design fallback strategies when timeouts occur
- Create informative timeout error messages
- Establish timeout retry policies and backoff strategies

## Implementation Examples

### Example 1: Comprehensive Client Timeout Management
```python
import asyncio
import aiohttp
import time
import logging
from typing import Dict, Optional, Any
from dataclasses import dataclass
from enum import Enum
import boto3
from contextlib import asynccontextmanager

class TimeoutType(Enum):
    CONNECTION = "connection"
    READ = "read"
    WRITE = "write"
    TOTAL = "total"

@dataclass
class TimeoutConfig:
    connection_timeout_ms: int = 5000
    read_timeout_ms: int = 30000
    write_timeout_ms: int = 30000
    total_timeout_ms: int = 60000
    retry_timeout_ms: int = 120000

class TimeoutManager:
    """Centralized timeout configuration management"""
    
    def __init__(self, config: Dict[str, Any]):
        self.default_timeouts = TimeoutConfig(**config.get('default_timeouts', {}))
        self.service_timeouts = {}
        
        # Load service-specific timeouts
        for service, timeout_config in config.get('service_timeouts', {}).items():
            self.service_timeouts[service] = TimeoutConfig(**timeout_config)
    
    def get_timeout_config(self, service_name: str = "default") -> TimeoutConfig:
        """Get timeout configuration for a service"""
        return self.service_timeouts.get(service_name, self.default_timeouts)
    
    def update_timeout_config(self, service_name: str, timeout_config: TimeoutConfig):
        """Update timeout configuration for a service"""
        self.service_timeouts[service_name] = timeout_config
        logging.info(f"Updated timeout config for {service_name}")

class HTTPClientWithTimeouts:
    """HTTP client with comprehensive timeout handling"""
    
    def __init__(self, timeout_manager: TimeoutManager):
        self.timeout_manager = timeout_manager
        self.session = None
        
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def get(self, url: str, service_name: str = "default", **kwargs) -> Dict[str, Any]:
        """HTTP GET with timeout handling"""
        return await self._make_request('GET', url, service_name, **kwargs)
    
    async def post(self, url: str, service_name: str = "default", **kwargs) -> Dict[str, Any]:
        """HTTP POST with timeout handling"""
        return await self._make_request('POST', url, service_name, **kwargs)
    
    async def _make_request(self, method: str, url: str, service_name: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request with comprehensive timeout handling"""
        timeout_config = self.timeout_manager.get_timeout_config(service_name)
        
        # Create aiohttp timeout configuration
        timeout = aiohttp.ClientTimeout(
            total=timeout_config.total_timeout_ms / 1000,
            connect=timeout_config.connection_timeout_ms / 1000,
            sock_read=timeout_config.read_timeout_ms / 1000
        )
        
        start_time = time.time()
        
        try:
            async with self.session.request(method, url, timeout=timeout, **kwargs) as response:
                response_time = (time.time() - start_time) * 1000
                
                # Read response with timeout
                try:
                    data = await response.json()
                except asyncio.TimeoutError:
                    raise TimeoutError(f"Read timeout after {timeout_config.read_timeout_ms}ms")
                
                return {
                    'success': True,
                    'status_code': response.status,
                    'data': data,
                    'response_time_ms': response_time,
                    'service_name': service_name
                }
                
        except asyncio.TimeoutError as e:
            response_time = (time.time() - start_time) * 1000
            timeout_type = self._classify_timeout_error(str(e))
            
            logging.warning(f"Timeout for {service_name} {method} {url}: {timeout_type} after {response_time:.2f}ms")
            
            return {
                'success': False,
                'error': f'{timeout_type} timeout',
                'timeout_type': timeout_type,
                'response_time_ms': response_time,
                'service_name': service_name
            }
        
        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            logging.error(f"Request failed for {service_name}: {str(e)}")
            
            return {
                'success': False,
                'error': str(e),
                'response_time_ms': response_time,
                'service_name': service_name
            }
    
    def _classify_timeout_error(self, error_message: str) -> str:
        """Classify timeout error type"""
        error_lower = error_message.lower()
        
        if 'connect' in error_lower:
            return 'connection'
        elif 'read' in error_lower:
            return 'read'
        elif 'write' in error_lower:
            return 'write'
        else:
            return 'total'

class DatabaseClientWithTimeouts:
    """Database client with timeout configuration"""
    
    def __init__(self, timeout_manager: TimeoutManager):
        self.timeout_manager = timeout_manager
        self.connection_pool = None
    
    async def execute_query(self, query: str, params: Optional[Dict] = None, 
                          service_name: str = "database") -> Dict[str, Any]:
        """Execute database query with timeout"""
        timeout_config = self.timeout_manager.get_timeout_config(service_name)
        
        start_time = time.time()
        
        try:
            # Simulate database query with timeout
            result = await asyncio.wait_for(
                self._execute_query_impl(query, params),
                timeout=timeout_config.total_timeout_ms / 1000
            )
            
            response_time = (time.time() - start_time) * 1000
            
            return {
                'success': True,
                'data': result,
                'response_time_ms': response_time,
                'service_name': service_name
            }
            
        except asyncio.TimeoutError:
            response_time = (time.time() - start_time) * 1000
            logging.warning(f"Database query timeout after {response_time:.2f}ms")
            
            return {
                'success': False,
                'error': 'Query timeout',
                'response_time_ms': response_time,
                'service_name': service_name
            }
        
        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            logging.error(f"Database query failed: {str(e)}")
            
            return {
                'success': False,
                'error': str(e),
                'response_time_ms': response_time,
                'service_name': service_name
            }
    
    async def _execute_query_impl(self, query: str, params: Optional[Dict] = None):
        """Simulate database query execution"""
        # Simulate query processing time
        await asyncio.sleep(0.1)
        return {'rows': [{'id': 1, 'name': 'test'}]}

class AWSClientWithTimeouts:
    """AWS service client with timeout configuration"""
    
    def __init__(self, timeout_manager: TimeoutManager):
        self.timeout_manager = timeout_manager
        self.clients = {}
    
    def get_client(self, service_name: str, aws_service: str):
        """Get AWS client with timeout configuration"""
        timeout_config = self.timeout_manager.get_timeout_config(service_name)
        
        if service_name not in self.clients:
            from botocore.config import Config
            
            # Configure boto3 client with timeouts
            config = Config(
                connect_timeout=timeout_config.connection_timeout_ms / 1000,
                read_timeout=timeout_config.read_timeout_ms / 1000,
                retries={'max_attempts': 0}  # Handle retries separately
            )
            
            self.clients[service_name] = boto3.client(aws_service, config=config)
        
        return self.clients[service_name]
    
    async def call_aws_service(self, service_name: str, aws_service: str, 
                             operation: str, **kwargs) -> Dict[str, Any]:
        """Call AWS service with timeout handling"""
        timeout_config = self.timeout_manager.get_timeout_config(service_name)
        client = self.get_client(service_name, aws_service)
        
        start_time = time.time()
        
        try:
            # Execute AWS operation with total timeout
            operation_func = getattr(client, operation)
            
            result = await asyncio.wait_for(
                asyncio.get_event_loop().run_in_executor(
                    None, lambda: operation_func(**kwargs)
                ),
                timeout=timeout_config.total_timeout_ms / 1000
            )
            
            response_time = (time.time() - start_time) * 1000
            
            return {
                'success': True,
                'data': result,
                'response_time_ms': response_time,
                'service_name': service_name
            }
            
        except asyncio.TimeoutError:
            response_time = (time.time() - start_time) * 1000
            logging.warning(f"AWS {aws_service} {operation} timeout after {response_time:.2f}ms")
            
            return {
                'success': False,
                'error': f'AWS {operation} timeout',
                'response_time_ms': response_time,
                'service_name': service_name
            }
        
        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            logging.error(f"AWS {aws_service} {operation} failed: {str(e)}")
            
            return {
                'success': False,
                'error': str(e),
                'response_time_ms': response_time,
                'service_name': service_name
            }

class TimeoutMetricsCollector:
    """Collect and analyze timeout metrics"""
    
    def __init__(self):
        self.timeout_events = []
        self.service_metrics = {}
    
    def record_timeout_event(self, service_name: str, timeout_type: str, 
                           response_time_ms: float):
        """Record timeout event for analysis"""
        event = {
            'service_name': service_name,
            'timeout_type': timeout_type,
            'response_time_ms': response_time_ms,
            'timestamp': time.time()
        }
        
        self.timeout_events.append(event)
        
        # Update service metrics
        if service_name not in self.service_metrics:
            self.service_metrics[service_name] = {
                'total_timeouts': 0,
                'timeout_types': {},
                'avg_response_time': 0
            }
        
        metrics = self.service_metrics[service_name]
        metrics['total_timeouts'] += 1
        
        if timeout_type not in metrics['timeout_types']:
            metrics['timeout_types'][timeout_type] = 0
        metrics['timeout_types'][timeout_type] += 1
        
        # Update average response time
        metrics['avg_response_time'] = (
            (metrics['avg_response_time'] * (metrics['total_timeouts'] - 1) + response_time_ms) /
            metrics['total_timeouts']
        )
    
    def get_timeout_analysis(self, service_name: Optional[str] = None) -> Dict[str, Any]:
        """Get timeout analysis for a service or all services"""
        if service_name:
            return self.service_metrics.get(service_name, {})
        else:
            return {
                'total_events': len(self.timeout_events),
                'service_metrics': self.service_metrics,
                'recent_events': self.timeout_events[-10:]  # Last 10 events
            }

# Usage example
async def main():
    # Configure timeouts
    timeout_config = {
        'default_timeouts': {
            'connection_timeout_ms': 5000,
            'read_timeout_ms': 30000,
            'total_timeout_ms': 60000
        },
        'service_timeouts': {
            'user_service': {
                'connection_timeout_ms': 2000,
                'read_timeout_ms': 10000,
                'total_timeout_ms': 15000
            },
            'payment_service': {
                'connection_timeout_ms': 3000,
                'read_timeout_ms': 20000,
                'total_timeout_ms': 30000
            }
        }
    }
    
    timeout_manager = TimeoutManager(timeout_config)
    metrics_collector = TimeoutMetricsCollector()
    
    # Test HTTP client with timeouts
    async with HTTPClientWithTimeouts(timeout_manager) as http_client:
        # Make requests to different services
        result1 = await http_client.get('https://httpbin.org/delay/1', 'user_service')
        print(f"User service result: {result1}")
        
        result2 = await http_client.get('https://httpbin.org/delay/5', 'payment_service')
        print(f"Payment service result: {result2}")
        
        # Record timeout events if they occurred
        if not result1['success'] and 'timeout' in result1.get('error', ''):
            metrics_collector.record_timeout_event(
                'user_service', 
                result1.get('timeout_type', 'unknown'),
                result1['response_time_ms']
            )
        
        if not result2['success'] and 'timeout' in result2.get('error', ''):
            metrics_collector.record_timeout_event(
                'payment_service',
                result2.get('timeout_type', 'unknown'), 
                result2['response_time_ms']
            )
    
    # Test database client
    db_client = DatabaseClientWithTimeouts(timeout_manager)
    db_result = await db_client.execute_query("SELECT * FROM users", service_name="database")
    print(f"Database result: {db_result}")
    
    # Get timeout analysis
    analysis = metrics_collector.get_timeout_analysis()
    print(f"Timeout analysis: {analysis}")

if __name__ == "__main__":
    asyncio.run(main())
```

## AWS Services Used

- **AWS SDK (Boto3)**: Built-in timeout configuration for all AWS service calls
- **Amazon API Gateway**: Request timeout configuration and client timeout handling
- **AWS Lambda**: Function timeout settings and client invocation timeouts
- **Amazon RDS**: Database connection and query timeout configuration
- **Amazon DynamoDB**: Request timeout and connection timeout settings
- **Amazon ElastiCache**: Connection timeout and operation timeout configuration
- **Amazon S3**: Upload/download timeout configuration for large objects
- **Amazon SQS**: Message receive timeout and visibility timeout settings
- **AWS Step Functions**: State timeout and heartbeat timeout configuration
- **Amazon Kinesis**: Stream read/write timeout configuration
- **AWS Systems Manager**: Parameter store timeout configuration
- **Amazon CloudWatch**: Timeout metrics monitoring and alerting
- **AWS X-Ray**: Timeout pattern analysis and distributed tracing
- **Amazon Route 53**: Health check timeout configuration
- **Elastic Load Balancing**: Backend timeout and connection timeout settings

## Benefits

- **Improved System Responsiveness**: Prevents indefinite blocking and resource exhaustion
- **Better Error Detection**: Quick identification of unresponsive services and network issues
- **Resource Management**: Prevents connection pool exhaustion and memory leaks
- **Enhanced User Experience**: Faster error feedback and fallback activation
- **System Stability**: Prevents cascading failures due to hanging connections
- **Better Monitoring**: Clear visibility into service response times and timeout patterns
- **Cost Optimization**: Reduced resource consumption through proper timeout handling
- **Improved Debugging**: Easier identification of performance bottlenecks
- **SLA Compliance**: Predictable response times through proper timeout configuration
- **Operational Efficiency**: Automated timeout handling reduces manual intervention

## Related Resources

- [AWS Well-Architected Reliability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/)
- [Set Client Timeouts](https://docs.aws.amazon.com/wellarchitected/latest/framework/rel_mitigate_interaction_failure_client_timeouts.html)
- [AWS SDK Timeout Configuration](https://docs.aws.amazon.com/general/latest/gr/api-retries.html)
- [Boto3 Configuration](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html)
- [Amazon API Gateway Timeout](https://docs.aws.amazon.com/apigateway/latest/developerguide/limits.html)
- [AWS Lambda Timeout](https://docs.aws.amazon.com/lambda/latest/dg/configuration-function-common.html)
- [Amazon RDS Connection Timeout](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ConnectToInstance.html)
- [Amazon DynamoDB Timeout](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Programming.Errors.html)
- [Timeout Patterns](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)
- [Amazon CloudWatch Metrics](https://docs.aws.amazon.com/cloudwatch/latest/monitoring/)
- [Network Timeout Best Practices](https://aws.amazon.com/builders-library/)
- [Building Resilient Systems](https://aws.amazon.com/builders-library/)
