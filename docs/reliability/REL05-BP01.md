---
title: REL05-BP01 - Implement graceful degradation to transform applicable hard dependencies into soft dependencies
layout: default
parent: REL05 - How do you design interactions in a distributed system to mitigate or withstand failures?
grand_parent: Reliability
nav_order: 1
---

# REL05-BP01: Implement graceful degradation to transform applicable hard dependencies into soft dependencies

## Overview

Design systems to gracefully degrade functionality when dependencies become unavailable, transforming hard dependencies that would cause complete system failure into soft dependencies that allow core functionality to continue. This approach maintains essential services while providing reduced functionality, ensuring better user experience and system resilience during partial outages.

## Implementation Steps

### 1. Identify and Classify Dependencies
- Categorize dependencies as critical, important, or optional
- Map dependencies to specific features and functionality
- Identify which features can operate with reduced capability
- Document fallback strategies for each dependency type

### 2. Design Fallback Mechanisms
- Implement cached responses for unavailable services
- Create default behaviors when dependencies fail
- Design simplified workflows that bypass failed components
- Establish static content delivery for dynamic services

### 3. Implement Feature Toggles and Circuit Breakers
- Deploy feature flags to disable non-essential functionality
- Implement circuit breakers to detect and isolate failures
- Create automatic fallback activation based on health checks
- Design manual override capabilities for emergency situations

### 4. Establish Graceful User Experience
- Design user interfaces that adapt to reduced functionality
- Implement informative error messages and status indicators
- Provide alternative workflows when primary paths fail
- Maintain core user journeys even with degraded services

### 5. Implement Data and State Management
- Cache critical data locally for offline operation
- Design eventual consistency patterns for data synchronization
- Implement read-only modes when write operations fail
- Create data replication strategies for high availability

### 6. Monitor and Test Degradation Scenarios
- Implement monitoring for dependency health and fallback activation
- Create automated testing for degradation scenarios
- Establish alerting for when systems operate in degraded mode
- Regularly test fallback mechanisms and recovery procedures

## Implementation Examples

### Example 1: Graceful Degradation Framework
```python
import boto3
import json
import logging
import time
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable, Union
from dataclasses import dataclass, asdict
from enum import Enum
from abc import ABC, abstractmethod
import threading
from contextlib import asynccontextmanager

class DependencyType(Enum):
    CRITICAL = "critical"
    IMPORTANT = "important"
    OPTIONAL = "optional"

class DegradationLevel(Enum):
    FULL_FUNCTIONALITY = "full_functionality"
    REDUCED_FUNCTIONALITY = "reduced_functionality"
    MINIMAL_FUNCTIONALITY = "minimal_functionality"
    EMERGENCY_MODE = "emergency_mode"

@dataclass
class DependencyStatus:
    name: str
    dependency_type: DependencyType
    is_healthy: bool
    last_check: datetime
    failure_count: int
    response_time_ms: float
    error_message: Optional[str] = None

@dataclass
class FallbackStrategy:
    dependency_name: str
    fallback_type: str
    fallback_data: Dict[str, Any]
    cache_ttl_seconds: int
    enabled: bool = True

class DependencyHealthChecker:
    """Health checker for system dependencies"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.dependencies = {}
        self.health_status = {}
        self.check_interval = config.get('check_interval_seconds', 30)
        self.failure_threshold = config.get('failure_threshold', 3)
        
    def register_dependency(self, name: str, dependency_type: DependencyType, 
                          health_check_func: Callable) -> None:
        """Register a dependency for health monitoring"""
        self.dependencies[name] = {
            'type': dependency_type,
            'health_check': health_check_func,
            'status': DependencyStatus(
                name=name,
                dependency_type=dependency_type,
                is_healthy=True,
                last_check=datetime.utcnow(),
                failure_count=0,
                response_time_ms=0.0
            )
        }
        logging.info(f"Registered dependency: {name} ({dependency_type.value})")
    
    async def start_health_monitoring(self):
        """Start continuous health monitoring"""
        while True:
            try:
                await self._check_all_dependencies()
                await asyncio.sleep(self.check_interval)
            except Exception as e:
                logging.error(f"Health monitoring error: {str(e)}")
                await asyncio.sleep(self.check_interval)
    
    async def _check_all_dependencies(self):
        """Check health of all registered dependencies"""
        tasks = []
        for name, dependency in self.dependencies.items():
            task = asyncio.create_task(self._check_dependency_health(name, dependency))
            tasks.append(task)
        
        await asyncio.gather(*tasks, return_exceptions=True)
    
    async def _check_dependency_health(self, name: str, dependency: Dict[str, Any]):
        """Check health of individual dependency"""
        try:
            start_time = time.time()
            health_check_func = dependency['health_check']
            
            # Execute health check
            is_healthy = await health_check_func()
            response_time = (time.time() - start_time) * 1000
            
            # Update status
            status = dependency['status']
            status.is_healthy = is_healthy
            status.last_check = datetime.utcnow()
            status.response_time_ms = response_time
            
            if is_healthy:
                status.failure_count = 0
                status.error_message = None
            else:
                status.failure_count += 1
                status.error_message = "Health check failed"
            
            self.health_status[name] = status
            
            # Log status changes
            if not is_healthy and status.failure_count >= self.failure_threshold:
                logging.warning(f"Dependency {name} is unhealthy (failures: {status.failure_count})")
            elif is_healthy and status.failure_count == 0:
                logging.info(f"Dependency {name} is healthy (response time: {response_time:.2f}ms)")
                
        except Exception as e:
            logging.error(f"Health check failed for {name}: {str(e)}")
            status = dependency['status']
            status.is_healthy = False
            status.failure_count += 1
            status.error_message = str(e)
            status.last_check = datetime.utcnow()
            self.health_status[name] = status
    
    def get_dependency_status(self, name: str) -> Optional[DependencyStatus]:
        """Get current status of a dependency"""
        return self.health_status.get(name)
    
    def get_system_degradation_level(self) -> DegradationLevel:
        """Determine current system degradation level"""
        critical_failures = 0
        important_failures = 0
        
        for status in self.health_status.values():
            if not status.is_healthy and status.failure_count >= self.failure_threshold:
                if status.dependency_type == DependencyType.CRITICAL:
                    critical_failures += 1
                elif status.dependency_type == DependencyType.IMPORTANT:
                    important_failures += 1
        
        if critical_failures > 0:
            return DegradationLevel.EMERGENCY_MODE
        elif important_failures >= 2:
            return DegradationLevel.MINIMAL_FUNCTIONALITY
        elif important_failures >= 1:
            return DegradationLevel.REDUCED_FUNCTIONALITY
        else:
            return DegradationLevel.FULL_FUNCTIONALITY

class GracefulDegradationManager:
    """Manager for graceful degradation strategies"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.health_checker = DependencyHealthChecker(config.get('health_checker', {}))
        self.fallback_strategies = {}
        self.cache = {}
        self.feature_flags = {}
        
        # AWS clients
        self.dynamodb = boto3.resource('dynamodb')
        self.s3 = boto3.client('s3')
        self.ssm = boto3.client('ssm')
        
        # Cache configuration
        self.cache_table_name = config.get('cache_table_name', 'degradation-cache')
        self.cache_table = self.dynamodb.Table(self.cache_table_name)
    
    def register_fallback_strategy(self, strategy: FallbackStrategy):
        """Register a fallback strategy for a dependency"""
        self.fallback_strategies[strategy.dependency_name] = strategy
        logging.info(f"Registered fallback strategy for {strategy.dependency_name}")
    
    async def execute_with_fallback(self, dependency_name: str, 
                                  primary_func: Callable, 
                                  *args, **kwargs) -> Dict[str, Any]:
        """Execute function with fallback on dependency failure"""
        try:
            # Check dependency health
            status = self.health_checker.get_dependency_status(dependency_name)
            
            if status and status.is_healthy:
                # Dependency is healthy, execute primary function
                result = await primary_func(*args, **kwargs)
                
                # Cache successful result for future fallback
                await self._cache_result(dependency_name, result)
                
                return {
                    'success': True,
                    'data': result,
                    'source': 'primary',
                    'degradation_level': 'none'
                }
            else:
                # Dependency is unhealthy, use fallback
                return await self._execute_fallback(dependency_name, *args, **kwargs)
                
        except Exception as e:
            logging.error(f"Primary function failed for {dependency_name}: {str(e)}")
            return await self._execute_fallback(dependency_name, *args, **kwargs)
    
    async def _execute_fallback(self, dependency_name: str, *args, **kwargs) -> Dict[str, Any]:
        """Execute fallback strategy for failed dependency"""
        try:
            strategy = self.fallback_strategies.get(dependency_name)
            
            if not strategy or not strategy.enabled:
                return {
                    'success': False,
                    'error': f'No fallback strategy available for {dependency_name}',
                    'source': 'none',
                    'degradation_level': 'critical'
                }
            
            if strategy.fallback_type == 'cached_response':
                return await self._get_cached_fallback(dependency_name)
            elif strategy.fallback_type == 'static_response':
                return await self._get_static_fallback(strategy)
            elif strategy.fallback_type == 'alternative_service':
                return await self._get_alternative_service_fallback(strategy, *args, **kwargs)
            elif strategy.fallback_type == 'degraded_functionality':
                return await self._get_degraded_functionality_fallback(strategy, *args, **kwargs)
            else:
                return {
                    'success': False,
                    'error': f'Unknown fallback type: {strategy.fallback_type}',
                    'source': 'fallback',
                    'degradation_level': 'critical'
                }
                
        except Exception as e:
            logging.error(f"Fallback execution failed for {dependency_name}: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'source': 'fallback',
                'degradation_level': 'critical'
            }
    
    async def _get_cached_fallback(self, dependency_name: str) -> Dict[str, Any]:
        """Get cached response as fallback"""
        try:
            response = self.cache_table.get_item(
                Key={'dependency_name': dependency_name}
            )
            
            if 'Item' in response:
                cached_data = response['Item']
                cache_age = time.time() - float(cached_data.get('timestamp', 0))
                
                return {
                    'success': True,
                    'data': json.loads(cached_data.get('data', '{}')),
                    'source': 'cache',
                    'degradation_level': 'reduced',
                    'cache_age_seconds': cache_age
                }
            else:
                return {
                    'success': False,
                    'error': 'No cached data available',
                    'source': 'cache',
                    'degradation_level': 'critical'
                }
                
        except Exception as e:
            logging.error(f"Cache fallback failed: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'source': 'cache',
                'degradation_level': 'critical'
            }
    
    async def _get_static_fallback(self, strategy: FallbackStrategy) -> Dict[str, Any]:
        """Get static response as fallback"""
        return {
            'success': True,
            'data': strategy.fallback_data,
            'source': 'static',
            'degradation_level': 'minimal'
        }
    
    async def _cache_result(self, dependency_name: str, result: Any):
        """Cache successful result for future fallback use"""
        try:
            self.cache_table.put_item(
                Item={
                    'dependency_name': dependency_name,
                    'data': json.dumps(result, default=str),
                    'timestamp': str(time.time()),
                    'ttl': int(time.time() + 3600)  # 1 hour TTL
                }
            )
        except Exception as e:
            logging.error(f"Failed to cache result for {dependency_name}: {str(e)}")

class FeatureToggleManager:
    """Manager for feature toggles during degradation"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.ssm = boto3.client('ssm')
        self.feature_flags = {}
        self.parameter_prefix = config.get('parameter_prefix', '/app/features/')
    
    async def load_feature_flags(self):
        """Load feature flags from AWS Systems Manager Parameter Store"""
        try:
            response = self.ssm.get_parameters_by_path(
                Path=self.parameter_prefix,
                Recursive=True
            )
            
            for parameter in response['Parameters']:
                feature_name = parameter['Name'].replace(self.parameter_prefix, '')
                self.feature_flags[feature_name] = parameter['Value'].lower() == 'true'
            
            logging.info(f"Loaded {len(self.feature_flags)} feature flags")
            
        except Exception as e:
            logging.error(f"Failed to load feature flags: {str(e)}")
    
    def is_feature_enabled(self, feature_name: str) -> bool:
        """Check if a feature is enabled"""
        return self.feature_flags.get(feature_name, True)  # Default to enabled
    
    async def disable_feature(self, feature_name: str):
        """Disable a feature during degradation"""
        try:
            parameter_name = f"{self.parameter_prefix}{feature_name}"
            
            self.ssm.put_parameter(
                Name=parameter_name,
                Value='false',
                Type='String',
                Overwrite=True
            )
            
            self.feature_flags[feature_name] = False
            logging.info(f"Disabled feature: {feature_name}")
            
        except Exception as e:
            logging.error(f"Failed to disable feature {feature_name}: {str(e)}")

# Usage example
async def main():
    config = {
        'health_checker': {
            'check_interval_seconds': 30,
            'failure_threshold': 3
        },
        'cache_table_name': 'degradation-cache'
    }
    
    # Initialize graceful degradation manager
    degradation_manager = GracefulDegradationManager(config)
    
    # Register dependencies
    async def check_user_service_health():
        # Implement actual health check
        return True
    
    degradation_manager.health_checker.register_dependency(
        'user_service',
        DependencyType.IMPORTANT,
        check_user_service_health
    )
    
    # Register fallback strategy
    fallback_strategy = FallbackStrategy(
        dependency_name='user_service',
        fallback_type='cached_response',
        fallback_data={},
        cache_ttl_seconds=3600
    )
    degradation_manager.register_fallback_strategy(fallback_strategy)
    
    # Start health monitoring
    await degradation_manager.health_checker.start_health_monitoring()

if __name__ == "__main__":
    asyncio.run(main())
```

## AWS Services Used

- **AWS Systems Manager Parameter Store**: Feature flag management and configuration storage
- **Amazon DynamoDB**: Caching layer for fallback responses and dependency status
- **Amazon S3**: Static content delivery for degraded functionality
- **Amazon CloudFront**: CDN for serving cached and static content during degradation
- **AWS Lambda**: Serverless functions for health checks and fallback processing
- **Amazon API Gateway**: API management with built-in throttling and fallback responses
- **Amazon ElastiCache**: High-performance caching for frequently accessed fallback data
- **Amazon CloudWatch**: Monitoring and alerting for degradation events and recovery
- **AWS Step Functions**: Workflow orchestration with fallback and retry logic
- **Amazon SQS**: Message queuing for asynchronous fallback processing
- **Amazon SNS**: Notifications for degradation events and system status changes
- **AWS X-Ray**: Distributed tracing for monitoring degradation patterns and performance
- **Amazon Route 53**: DNS-based failover and health checking for service endpoints
- **Elastic Load Balancing**: Load balancing with health checks and automatic failover
- **AWS Config**: Configuration compliance monitoring for degradation policies
- **AWS Secrets Manager**: Secure storage of fallback service credentials and API keys

## Benefits

- **Improved System Resilience**: Core functionality continues even when dependencies fail
- **Better User Experience**: Users can still access essential features during outages
- **Reduced Blast Radius**: Dependency failures don't cause complete system outages
- **Faster Recovery**: Systems can operate in degraded mode while issues are resolved
- **Cost Optimization**: Reduced infrastructure requirements during degraded operation
- **Enhanced Availability**: Higher overall system availability through graceful degradation
- **Simplified Incident Response**: Clear degradation levels help prioritize recovery efforts
- **Business Continuity**: Critical business processes can continue with reduced functionality
- **Improved Testing**: Degradation scenarios can be tested and validated regularly
- **Better Monitoring**: Clear visibility into system health and degradation levels

## Related Resources

- [AWS Well-Architected Reliability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/)
- [Implement Graceful Degradation](https://docs.aws.amazon.com/wellarchitected/latest/framework/rel_mitigate_interaction_failure_graceful_degradation.html)
- [AWS Systems Manager Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html)
- [Amazon DynamoDB Best Practices](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html)
- [Circuit Breaker Pattern](https://aws.amazon.com/builders-library/implementing-health-checks/)
- [Feature Flags and Toggles](https://aws.amazon.com/builders-library/automating-safe-hands-off-deployments/)
- [Amazon CloudFront User Guide](https://docs.aws.amazon.com/cloudfront/latest/developerguide/)
- [Graceful Degradation Patterns](https://aws.amazon.com/builders-library/avoiding-fallback-in-distributed-systems/)
- [Amazon Route 53 Health Checks](https://docs.aws.amazon.com/route53/latest/developerguide/health-checks-creating.html)
- [AWS Lambda Best Practices](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
- [Amazon ElastiCache User Guide](https://docs.aws.amazon.com/elasticache/latest/userguide/)
- [Building Resilient Systems](https://aws.amazon.com/builders-library/)
