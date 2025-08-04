---
title: COST09-BP02 - Implement a buffer or throttle to manage demand
layout: default
parent: COST09 - How do you manage demand, and supply resources?
grand_parent: Cost Optimization
nav_order: 2
---

<div class="pillar-header">
  <h1>COST09-BP02: Implement a buffer or throttle to manage demand</h1>
  <p>Implement buffering, throttling, and queuing mechanisms to manage demand spikes and prevent resource over-provisioning while maintaining acceptable service levels. Effective demand management reduces costs by smoothing demand patterns and preventing unnecessary scaling.</p>
</div>

## Implementation guidance

Demand management through buffering and throttling involves implementing mechanisms that control the flow of requests and workload to prevent sudden spikes from triggering expensive resource scaling. These techniques help maintain cost efficiency while ensuring service quality and availability.

### Demand Management Strategies

**Buffering**: Use queues and buffers to temporarily store requests during demand spikes, allowing resources to process them at a sustainable rate.

**Throttling**: Implement rate limiting and request throttling to control the volume of requests processed per unit time, preventing resource overload.

**Load Shaping**: Distribute demand more evenly over time through techniques like request batching, scheduling, and priority queuing.

**Circuit Breaking**: Implement circuit breakers to prevent cascading failures and resource exhaustion during high-demand periods.

**Graceful Degradation**: Design systems to maintain core functionality while reducing non-essential features during high-demand periods.

### Implementation Patterns

**Queue-Based Buffering**: Use message queues to decouple producers and consumers, allowing for demand smoothing and asynchronous processing.

**API Rate Limiting**: Implement rate limiting at API gateways and application levels to control request flow and prevent overload.

**Priority-Based Processing**: Implement priority queues to ensure critical requests are processed first while managing overall demand.

**Adaptive Throttling**: Dynamically adjust throttling rates based on current system capacity and performance metrics.

## AWS Services to Consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon SQS</h4>
    <p>Implement message queuing for demand buffering and asynchronous processing. Use SQS to decouple components and smooth demand spikes.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon API Gateway</h4>
    <p>Implement API throttling and rate limiting to control request flow. Use API Gateway's built-in throttling capabilities to manage demand.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon Kinesis</h4>
    <p>Stream and buffer real-time data for processing at controlled rates. Use Kinesis for high-throughput data buffering and stream processing.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Application Load Balancer</h4>
    <p>Distribute load and implement connection throttling. Use ALB for intelligent request distribution and connection management.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon ElastiCache</h4>
    <p>Implement caching to reduce backend demand and improve response times. Use ElastiCache to buffer frequently accessed data.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Step Functions</h4>
    <p>Orchestrate workflows with built-in error handling and retry logic. Use Step Functions to manage complex processing workflows with demand control.</p>
  </div>
</div>

## Implementation Steps

### 1. Analyze Demand Patterns
- Identify demand spikes and their characteristics
- Analyze the impact of demand spikes on resource utilization
- Determine appropriate buffering and throttling strategies
- Define acceptable service levels and response times

### 2. Design Buffering Strategy
- Choose appropriate queuing mechanisms for different workload types
- Design queue sizing and retention policies
- Implement dead letter queues for failed message handling
- Plan for queue monitoring and management

### 3. Implement Throttling Mechanisms
- Set up API rate limiting and request throttling
- Implement adaptive throttling based on system capacity
- Create priority-based request handling
- Design graceful degradation strategies

### 4. Deploy Monitoring and Alerting
- Monitor queue depths and processing rates
- Set up alerts for throttling events and capacity issues
- Track service level metrics and user experience impact
- Implement dashboards for demand management visibility

### 5. Test and Validate
- Test buffering and throttling under various load conditions
- Validate that service levels are maintained during demand spikes
- Ensure that cost optimization goals are achieved
- Document performance characteristics and limitations

### 6. Optimize and Tune
- Continuously adjust buffering and throttling parameters
- Optimize based on actual demand patterns and system behavior
- Implement automated tuning where possible
- Regular review and refinement of demand management strategies
## Demand Management Framework

### Demand Buffer and Throttle Manager
```python
import boto3
import json
import time
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from enum import Enum
import threading
from collections import deque
import logging

class ThrottleStrategy(Enum):
    FIXED_RATE = "fixed_rate"
    ADAPTIVE_RATE = "adaptive_rate"
    PRIORITY_BASED = "priority_based"
    CIRCUIT_BREAKER = "circuit_breaker"

class BufferStrategy(Enum):
    FIFO_QUEUE = "fifo_queue"
    PRIORITY_QUEUE = "priority_queue"
    BATCH_PROCESSING = "batch_processing"
    STREAMING_BUFFER = "streaming_buffer"

@dataclass
class DemandRequest:
    request_id: str
    timestamp: datetime
    priority: int  # 1-10, where 10 is highest priority
    payload_size: int
    processing_time_estimate: float
    retry_count: int = 0
    max_retries: int = 3

@dataclass
class ThrottleConfig:
    strategy: ThrottleStrategy
    max_requests_per_second: float
    burst_capacity: int
    adaptive_threshold: float
    circuit_breaker_threshold: int
    recovery_time_seconds: int

class DemandBufferThrottleManager:
    def __init__(self):
        self.sqs = boto3.client('sqs')
        self.apigateway = boto3.client('apigateway')
        self.cloudwatch = boto3.client('cloudwatch')
        self.elasticache = boto3.client('elasticache')
        
        # Internal state management
        self.request_buffer = deque()
        self.processing_queue = deque()
        self.throttle_state = {
            'current_rate': 0.0,
            'burst_tokens': 0,
            'circuit_breaker_failures': 0,
            'circuit_breaker_open': False,
            'last_reset_time': datetime.now()
        }
        
        # Configuration
        self.buffer_config = {
            'max_buffer_size': 10000,
            'batch_size': 100,
            'processing_timeout': 30,
            'priority_levels': 10
        }
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def implement_sqs_buffering(self, queue_config: Dict) -> Dict:
        """Implement SQS-based demand buffering"""
        
        sqs_buffer_config = {
            'queue_name': queue_config.get('queue_name', 'demand-buffer-queue'),
            'queue_attributes': {
                'VisibilityTimeoutSeconds': str(queue_config.get('visibility_timeout', 300)),
                'MessageRetentionPeriod': str(queue_config.get('retention_period', 1209600)),  # 14 days
                'ReceiveMessageWaitTimeSeconds': str(queue_config.get('wait_time', 20)),  # Long polling
                'MaxReceiveCount': str(queue_config.get('max_receive_count', 3))
            },
            'dead_letter_queue': {
                'enabled': queue_config.get('enable_dlq', True),
                'max_receive_count': queue_config.get('dlq_max_receive', 3)
            },
            'scaling_configuration': {
                'target_queue_depth': queue_config.get('target_depth', 100),
                'scale_up_threshold': queue_config.get('scale_up_threshold', 500),
                'scale_down_threshold': queue_config.get('scale_down_threshold', 10),
                'processing_capacity': queue_config.get('processing_capacity', 10)
            }
        }
        
        # Create main queue
        try:
            queue_response = self.sqs.create_queue(
                QueueName=sqs_buffer_config['queue_name'],
                Attributes=sqs_buffer_config['queue_attributes']
            )
            sqs_buffer_config['queue_url'] = queue_response['QueueUrl']
            
            # Create dead letter queue if enabled
            if sqs_buffer_config['dead_letter_queue']['enabled']:
                dlq_response = self.sqs.create_queue(
                    QueueName=f"{sqs_buffer_config['queue_name']}-dlq",
                    Attributes={
                        'MessageRetentionPeriod': str(1209600)  # 14 days
                    }
                )
                sqs_buffer_config['dead_letter_queue']['queue_url'] = dlq_response['QueueUrl']
            
        except Exception as e:
            self.logger.error(f"Error creating SQS buffer: {e}")
        
        return sqs_buffer_config
    
    def implement_api_throttling(self, api_config: Dict) -> Dict:
        """Implement API Gateway throttling configuration"""
        
        throttling_config = {
            'api_id': api_config['api_id'],
            'stage_name': api_config.get('stage_name', 'prod'),
            'throttle_settings': {
                'rate_limit': api_config.get('rate_limit', 1000),  # requests per second
                'burst_limit': api_config.get('burst_limit', 2000),  # burst capacity
            },
            'per_method_throttling': {},
            'usage_plans': []
        }
        
        # Configure per-method throttling
        for method_config in api_config.get('method_throttling', []):
            method_key = f"{method_config['resource_path']}/{method_config['http_method']}"
            throttling_config['per_method_throttling'][method_key] = {
                'rate_limit': method_config.get('rate_limit', 100),
                'burst_limit': method_config.get('burst_limit', 200)
            }
        
        # Create usage plans for different client tiers
        for plan_config in api_config.get('usage_plans', []):
            usage_plan = {
                'name': plan_config['name'],
                'description': plan_config.get('description', ''),
                'throttle': {
                    'rate_limit': plan_config.get('rate_limit', 500),
                    'burst_limit': plan_config.get('burst_limit', 1000)
                },
                'quota': {
                    'limit': plan_config.get('quota_limit', 10000),
                    'period': plan_config.get('quota_period', 'DAY')
                }
            }
            throttling_config['usage_plans'].append(usage_plan)
        
        return throttling_config
    
    def implement_adaptive_throttling(self, system_metrics: Dict) -> Dict:
        """Implement adaptive throttling based on system metrics"""
        
        current_cpu = system_metrics.get('cpu_utilization', 50)
        current_memory = system_metrics.get('memory_utilization', 50)
        current_latency = system_metrics.get('response_latency', 100)
        error_rate = system_metrics.get('error_rate', 0)
        
        # Calculate system health score
        health_score = self.calculate_system_health_score(
            current_cpu, current_memory, current_latency, error_rate
        )
        
        # Adaptive throttling logic
        base_rate = 1000  # Base requests per second
        
        if health_score > 0.8:  # System healthy
            adaptive_rate = base_rate * 1.2  # Allow 20% more traffic
        elif health_score > 0.6:  # System under moderate load
            adaptive_rate = base_rate  # Maintain base rate
        elif health_score > 0.4:  # System under stress
            adaptive_rate = base_rate * 0.7  # Reduce by 30%
        else:  # System overloaded
            adaptive_rate = base_rate * 0.5  # Reduce by 50%
        
        adaptive_config = {
            'current_health_score': health_score,
            'adaptive_rate_limit': adaptive_rate,
            'throttle_adjustment': adaptive_rate / base_rate,
            'system_metrics': system_metrics,
            'throttle_actions': self.generate_throttle_actions(health_score),
            'next_evaluation_time': datetime.now() + timedelta(minutes=5)
        }
        
        return adaptive_config
    
    def calculate_system_health_score(self, cpu: float, memory: float, 
                                    latency: float, error_rate: float) -> float:
        """Calculate overall system health score (0-1)"""
        
        # Normalize metrics to 0-1 scale (higher is better)
        cpu_score = max(0, (100 - cpu) / 100)
        memory_score = max(0, (100 - memory) / 100)
        latency_score = max(0, (1000 - latency) / 1000)  # Assume 1000ms is very poor
        error_score = max(0, (10 - error_rate) / 10)  # Assume 10% error rate is very poor
        
        # Weighted average (can be adjusted based on priorities)
        weights = {'cpu': 0.3, 'memory': 0.2, 'latency': 0.3, 'error': 0.2}
        
        health_score = (
            cpu_score * weights['cpu'] +
            memory_score * weights['memory'] +
            latency_score * weights['latency'] +
            error_score * weights['error']
        )
        
        return min(1.0, max(0.0, health_score))
    
    def implement_priority_queuing(self, requests: List[DemandRequest]) -> Dict:
        """Implement priority-based request queuing"""
        
        # Sort requests by priority (higher number = higher priority)
        sorted_requests = sorted(requests, key=lambda x: (-x.priority, x.timestamp))
        
        # Create priority queues
        priority_queues = {i: [] for i in range(1, 11)}  # Priority levels 1-10
        
        for request in sorted_requests:
            priority_queues[request.priority].append(request)
        
        # Calculate processing order and estimated wait times
        processing_order = []
        current_wait_time = 0
        
        # Process highest priority requests first
        for priority in range(10, 0, -1):
            for request in priority_queues[priority]:
                processing_order.append({
                    'request_id': request.request_id,
                    'priority': request.priority,
                    'estimated_wait_time': current_wait_time,
                    'estimated_processing_time': request.processing_time_estimate
                })
                current_wait_time += request.processing_time_estimate
        
        priority_config = {
            'total_requests': len(requests),
            'priority_distribution': {
                priority: len(queue) for priority, queue in priority_queues.items() if queue
            },
            'processing_order': processing_order,
            'total_estimated_processing_time': current_wait_time,
            'average_wait_time': current_wait_time / len(requests) if requests else 0
        }
        
        return priority_config
    
    def implement_circuit_breaker(self, service_config: Dict) -> Dict:
        """Implement circuit breaker pattern for demand management"""
        
        circuit_breaker_config = {
            'service_name': service_config['service_name'],
            'failure_threshold': service_config.get('failure_threshold', 5),
            'recovery_timeout': service_config.get('recovery_timeout', 60),
            'half_open_max_calls': service_config.get('half_open_max_calls', 3),
            'current_state': 'CLOSED',  # CLOSED, OPEN, HALF_OPEN
            'failure_count': 0,
            'last_failure_time': None,
            'success_count': 0,
            'monitoring': {
                'total_requests': 0,
                'successful_requests': 0,
                'failed_requests': 0,
                'circuit_breaker_trips': 0
            }
        }
        
        return circuit_breaker_config
    
    def process_circuit_breaker_request(self, circuit_config: Dict, request: DemandRequest) -> Dict:
        """Process a request through the circuit breaker"""
        
        current_time = datetime.now()
        result = {
            'request_processed': False,
            'circuit_state': circuit_config['current_state'],
            'action_taken': '',
            'estimated_retry_time': None
        }
        
        # Update total requests
        circuit_config['monitoring']['total_requests'] += 1
        
        if circuit_config['current_state'] == 'CLOSED':
            # Normal operation - process request
            result['request_processed'] = True
            result['action_taken'] = 'processed_normally'
            
        elif circuit_config['current_state'] == 'OPEN':
            # Circuit is open - check if recovery timeout has passed
            if (circuit_config['last_failure_time'] and 
                (current_time - circuit_config['last_failure_time']).seconds >= circuit_config['recovery_timeout']):
                # Move to half-open state
                circuit_config['current_state'] = 'HALF_OPEN'
                circuit_config['success_count'] = 0
                result['circuit_state'] = 'HALF_OPEN'
                result['request_processed'] = True
                result['action_taken'] = 'moved_to_half_open'
            else:
                # Reject request
                result['request_processed'] = False
                result['action_taken'] = 'rejected_circuit_open'
                remaining_timeout = circuit_config['recovery_timeout'] - (current_time - circuit_config['last_failure_time']).seconds
                result['estimated_retry_time'] = current_time + timedelta(seconds=remaining_timeout)
                
        elif circuit_config['current_state'] == 'HALF_OPEN':
            # Half-open state - allow limited requests
            if circuit_config['success_count'] < circuit_config['half_open_max_calls']:
                result['request_processed'] = True
                result['action_taken'] = 'processed_half_open'
            else:
                result['request_processed'] = False
                result['action_taken'] = 'rejected_half_open_limit'
        
        return result
    
    def create_demand_management_dashboard(self) -> Dict:
        """Create comprehensive demand management dashboard"""
        
        dashboard_config = {
            'dashboard_name': 'Demand Management Overview',
            'widgets': [
                {
                    'type': 'metric',
                    'title': 'Request Rate and Throttling',
                    'metrics': [
                        ['AWS/ApiGateway', 'Count', 'ApiName', 'demand-api'],
                        ['AWS/ApiGateway', 'ThrottledCount', 'ApiName', 'demand-api'],
                        ['Custom/DemandManagement', 'AdaptiveThrottleRate']
                    ],
                    'period': 300
                },
                {
                    'type': 'metric',
                    'title': 'Queue Depth and Processing Rate',
                    'metrics': [
                        ['AWS/SQS', 'ApproximateNumberOfMessages', 'QueueName', 'demand-buffer-queue'],
                        ['AWS/SQS', 'NumberOfMessagesSent', 'QueueName', 'demand-buffer-queue'],
                        ['AWS/SQS', 'NumberOfMessagesReceived', 'QueueName', 'demand-buffer-queue']
                    ],
                    'period': 300
                },
                {
                    'type': 'metric',
                    'title': 'System Health Metrics',
                    'metrics': [
                        ['AWS/EC2', 'CPUUtilization'],
                        ['AWS/ApplicationELB', 'TargetResponseTime'],
                        ['Custom/DemandManagement', 'SystemHealthScore']
                    ],
                    'period': 300
                },
                {
                    'type': 'metric',
                    'title': 'Circuit Breaker Status',
                    'metrics': [
                        ['Custom/DemandManagement', 'CircuitBreakerTrips'],
                        ['Custom/DemandManagement', 'CircuitBreakerState'],
                        ['Custom/DemandManagement', 'RejectedRequests']
                    ],
                    'period': 300
                }
            ],
            'alarms': [
                {
                    'alarm_name': 'HighQueueDepth',
                    'metric_name': 'ApproximateNumberOfMessages',
                    'threshold': 1000,
                    'comparison_operator': 'GreaterThanThreshold'
                },
                {
                    'alarm_name': 'HighThrottleRate',
                    'metric_name': 'ThrottledCount',
                    'threshold': 100,
                    'comparison_operator': 'GreaterThanThreshold'
                },
                {
                    'alarm_name': 'CircuitBreakerOpen',
                    'metric_name': 'CircuitBreakerState',
                    'threshold': 1,
                    'comparison_operator': 'GreaterThanOrEqualToThreshold'
                }
            ]
        }
        
        return dashboard_config
```

## Demand Management Implementation Templates

### SQS Buffer Configuration Template
```yaml
SQS_Buffer_Configuration:
  implementation_id: "SQS-BUFFER-2024-001"
  objective: "Implement demand buffering to smooth traffic spikes"
  
  queue_configuration:
    main_queue:
      name: "demand-buffer-queue"
      visibility_timeout: 300  # 5 minutes
      message_retention_period: 1209600  # 14 days
      receive_message_wait_time: 20  # Long polling
      max_receive_count: 3
      
    dead_letter_queue:
      name: "demand-buffer-dlq"
      enabled: true
      max_receive_count: 3
      retention_period: 1209600  # 14 days
      
  processing_configuration:
    batch_size: 10
    processing_timeout: 30
    concurrent_processors: 5
    auto_scaling:
      enabled: true
      target_queue_depth: 100
      scale_up_threshold: 500
      scale_down_threshold: 10
      
  monitoring:
    cloudwatch_metrics:
      - "ApproximateNumberOfMessages"
      - "NumberOfMessagesSent"
      - "NumberOfMessagesReceived"
      - "NumberOfMessagesDeleted"
      
    alarms:
      - name: "HighQueueDepth"
        threshold: 1000
        action: "scale_up_processors"
        
      - name: "LowQueueDepth"
        threshold: 5
        action: "scale_down_processors"
        
  cost_optimization:
    estimated_monthly_cost: 150.00
    cost_per_million_requests: 0.40
    savings_from_reduced_scaling: 800.00
    net_monthly_savings: 650.00
```

### API Throttling Strategy
```python
def create_api_throttling_strategy():
    """Create comprehensive API throttling strategy"""
    
    strategy = {
        'throttling_tiers': {
            'public_api': {
                'rate_limit': 100,  # requests per second
                'burst_limit': 200,
                'quota_limit': 10000,  # requests per day
                'throttle_strategy': 'fixed_rate'
            },
            'premium_api': {
                'rate_limit': 500,
                'burst_limit': 1000,
                'quota_limit': 100000,
                'throttle_strategy': 'adaptive_rate'
            },
            'internal_api': {
                'rate_limit': 1000,
                'burst_limit': 2000,
                'quota_limit': 1000000,
                'throttle_strategy': 'priority_based'
            }
        },
        
        'adaptive_throttling': {
            'health_check_interval': 60,  # seconds
            'adjustment_factors': {
                'healthy': 1.2,      # Allow 20% more traffic
                'moderate': 1.0,     # Maintain current rate
                'stressed': 0.7,     # Reduce by 30%
                'overloaded': 0.5    # Reduce by 50%
            },
            'health_thresholds': {
                'cpu_threshold': 80,
                'memory_threshold': 85,
                'latency_threshold': 1000,  # milliseconds
                'error_rate_threshold': 5   # percentage
            }
        },
        
        'circuit_breaker': {
            'failure_threshold': 5,
            'recovery_timeout': 60,  # seconds
            'half_open_max_calls': 3,
            'monitoring_window': 300  # seconds
        },
        
        'priority_handling': {
            'priority_levels': {
                'critical': {'weight': 10, 'guaranteed_capacity': 0.3},
                'high': {'weight': 7, 'guaranteed_capacity': 0.2},
                'medium': {'weight': 5, 'guaranteed_capacity': 0.3},
                'low': {'weight': 3, 'guaranteed_capacity': 0.2}
            },
            'queue_management': {
                'max_queue_size': 10000,
                'queue_timeout': 30,  # seconds
                'drop_policy': 'drop_lowest_priority'
            }
        },
        
        'cost_optimization': {
            'estimated_infrastructure_savings': '25-40%',
            'reduced_over_provisioning': '30-50%',
            'improved_resource_utilization': '20-35%',
            'operational_cost_reduction': '15-25%'
        }
    }
    
    return strategy
```

## Common Challenges and Solutions

### Challenge: Balancing Throughput with Latency

**Solution**: Implement adaptive buffering that adjusts based on current system load. Use priority queues to ensure critical requests are processed quickly. Monitor end-to-end latency and adjust buffer sizes accordingly.

### Challenge: Determining Optimal Throttling Rates

**Solution**: Use historical demand analysis to set baseline rates. Implement adaptive throttling that adjusts based on real-time system health. Continuously monitor and tune throttling parameters based on performance data.

### Challenge: Managing Queue Overflow

**Solution**: Implement multiple queue tiers with different retention policies. Use dead letter queues for failed messages. Implement queue depth monitoring with automatic scaling of processing capacity.

### Challenge: Maintaining Service Quality During Throttling

**Solution**: Implement graceful degradation strategies. Use priority-based throttling to protect critical functionality. Provide clear feedback to clients about throttling status and retry recommendations.

### Challenge: Complex Multi-Service Throttling

**Solution**: Implement centralized throttling policies with service-specific configurations. Use distributed rate limiting with shared state. Coordinate throttling across service boundaries to prevent cascading effects.

## Related Resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/cost_demand_supply_buffer.html">AWS Well-Architected Framework - Implement a buffer or throttle to manage demand</a></li>
    <li><a href="https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html">Amazon SQS Developer Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html">API Gateway Request Throttling</a></li>
    <li><a href="https://docs.aws.amazon.com/kinesis/latest/dev/introduction.html">Amazon Kinesis Developer Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/elasticloadbalancing/latest/application/introduction.html">Application Load Balancer User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/WhatIs.html">Amazon ElastiCache for Redis User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html">AWS Step Functions Developer Guide</a></li>
    <li><a href="https://aws.amazon.com/blogs/architecture/">AWS Architecture Blog</a></li>
  </ul>
</div>

<style>
.pillar-header {
  background-color: #e8f5e8;
  border-left: 5px solid #2d7d2d;
}

.pillar-header h1 {
  color: #2d7d2d;
}

.aws-service-content h4 {
  color: #2d7d2d;
}

.related-resources {
  background-color: #e8f5e8;
}

.related-resources h2 {
  color: #2d7d2d;
}
</style>
