---
title: REL05-BP04 - Fail fast and limit queues
layout: default
parent: REL05 - How do you design interactions in a distributed system to mitigate or withstand failures?
grand_parent: Reliability
nav_order: 4
---

# REL05-BP04: Fail fast and limit queues

## Overview

Implement fail-fast mechanisms and queue limits to prevent resource exhaustion and cascading failures. By quickly rejecting requests that are likely to fail and limiting queue sizes, systems can maintain responsiveness and prevent memory exhaustion during high load or failure scenarios.

## Implementation Steps

### 1. Implement Health Checks and Circuit Breakers
- Deploy comprehensive health checks for all dependencies
- Implement circuit breakers to fail fast when services are unhealthy
- Configure appropriate failure thresholds and recovery timeouts
- Design automatic failover to healthy service instances

### 2. Configure Queue Size Limits
- Set maximum queue sizes based on memory and processing capacity
- Implement queue overflow handling with appropriate error responses
- Design priority queues for critical vs non-critical requests
- Monitor queue depths and implement alerting for capacity issues

### 3. Establish Request Validation and Early Rejection
- Implement input validation to reject malformed requests immediately
- Check resource availability before queuing expensive operations
- Validate authentication and authorization early in the request pipeline
- Implement rate limiting to reject excess requests quickly

### 4. Design Timeout and Deadline Management
- Set appropriate timeouts for all operations and dependencies
- Implement request deadlines to prevent processing stale requests
- Configure cascading timeouts throughout the request chain
- Design timeout handling that fails fast rather than retrying indefinitely

### 5. Implement Load Shedding Mechanisms
- Design load shedding strategies for different request types
- Implement admission control based on system capacity
- Configure automatic load shedding during high CPU or memory usage
- Establish graceful degradation when shedding load

### 6. Monitor and Optimize Failure Detection
- Track failure detection latency and accuracy
- Monitor queue utilization and overflow events
- Implement automated tuning of failure detection parameters
- Create dashboards for fail-fast metrics and queue health

## Implementation Examples

### Example 1: Fail-Fast Queue Management System
```python
import asyncio
import time
import logging
from typing import Dict, Optional, Callable, Any
from dataclasses import dataclass
from enum import Enum
from collections import deque
import threading
import psutil

class QueueType(Enum):
    FIFO = "fifo"
    PRIORITY = "priority"
    LIFO = "lifo"

class RequestPriority(Enum):
    CRITICAL = 1
    HIGH = 2
    NORMAL = 3
    LOW = 4

@dataclass
class QueuedRequest:
    request_id: str
    priority: RequestPriority
    payload: Dict[str, Any]
    queued_at: float
    deadline: float
    retry_count: int = 0

class FailFastQueue:
    """Queue with fail-fast mechanisms and size limits"""
    
    def __init__(self, config: Dict[str, Any]):
        self.max_size = config.get('max_size', 1000)
        self.queue_type = QueueType(config.get('queue_type', 'fifo'))
        self.default_timeout_ms = config.get('default_timeout_ms', 30000)
        
        # Queue storage
        if self.queue_type == QueueType.PRIORITY:
            import heapq
            self.queue = []
        else:
            self.queue = deque()
        
        self.lock = threading.Lock()
        self.current_size = 0
        
        # Metrics
        self.enqueued_count = 0
        self.dequeued_count = 0
        self.rejected_count = 0
        self.expired_count = 0
        
    def enqueue(self, request: QueuedRequest) -> bool:
        """Enqueue request with fail-fast checks"""
        with self.lock:
            # Check queue capacity
            if self.current_size >= self.max_size:
                logging.warning(f"Queue full, rejecting request {request.request_id}")
                self.rejected_count += 1
                return False
            
            # Check if request has already expired
            if time.time() * 1000 > request.deadline:
                logging.warning(f"Request {request.request_id} expired before queuing")
                self.expired_count += 1
                return False
            
            # Add to queue based on type
            if self.queue_type == QueueType.PRIORITY:
                import heapq
                heapq.heappush(self.queue, (request.priority.value, request.queued_at, request))
            elif self.queue_type == QueueType.LIFO:
                self.queue.append(request)
            else:  # FIFO
                self.queue.append(request)
            
            self.current_size += 1
            self.enqueued_count += 1
            
            logging.debug(f"Enqueued request {request.request_id}, queue size: {self.current_size}")
            return True
    
    def dequeue(self) -> Optional[QueuedRequest]:
        """Dequeue request with expiration check"""
        with self.lock:
            if self.current_size == 0:
                return None
            
            # Get next request based on queue type
            if self.queue_type == QueueType.PRIORITY:
                import heapq
                _, _, request = heapq.heappop(self.queue)
            elif self.queue_type == QueueType.LIFO:
                request = self.queue.pop()
            else:  # FIFO
                request = self.queue.popleft()
            
            self.current_size -= 1
            
            # Check if request has expired
            if time.time() * 1000 > request.deadline:
                logging.warning(f"Request {request.request_id} expired in queue")
                self.expired_count += 1
                return self.dequeue()  # Try next request
            
            self.dequeued_count += 1
            logging.debug(f"Dequeued request {request.request_id}, queue size: {self.current_size}")
            return request
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get queue metrics"""
        with self.lock:
            return {
                'current_size': self.current_size,
                'max_size': self.max_size,
                'utilization_percent': (self.current_size / self.max_size) * 100,
                'enqueued_count': self.enqueued_count,
                'dequeued_count': self.dequeued_count,
                'rejected_count': self.rejected_count,
                'expired_count': self.expired_count
            }

class CircuitBreaker:
    """Circuit breaker for fail-fast behavior"""
    
    def __init__(self, config: Dict[str, Any]):
        self.failure_threshold = config.get('failure_threshold', 5)
        self.timeout_seconds = config.get('timeout_seconds', 60)
        self.half_open_max_calls = config.get('half_open_max_calls', 3)
        
        self.failure_count = 0
        self.last_failure_time = 0
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
        self.half_open_calls = 0
        self.lock = threading.Lock()
    
    def call_allowed(self) -> bool:
        """Check if call is allowed through circuit breaker"""
        with self.lock:
            if self.state == "CLOSED":
                return True
            elif self.state == "OPEN":
                if time.time() - self.last_failure_time >= self.timeout_seconds:
                    self.state = "HALF_OPEN"
                    self.half_open_calls = 0
                    return True
                return False
            elif self.state == "HALF_OPEN":
                if self.half_open_calls < self.half_open_max_calls:
                    self.half_open_calls += 1
                    return True
                return False
        
        return False
    
    def record_success(self):
        """Record successful call"""
        with self.lock:
            self.failure_count = 0
            if self.state == "HALF_OPEN":
                self.state = "CLOSED"
    
    def record_failure(self):
        """Record failed call"""
        with self.lock:
            self.failure_count += 1
            self.last_failure_time = time.time()
            
            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"

class LoadShedder:
    """Load shedding based on system resources"""
    
    def __init__(self, config: Dict[str, Any]):
        self.cpu_threshold = config.get('cpu_threshold_percent', 80)
        self.memory_threshold = config.get('memory_threshold_percent', 85)
        self.queue_threshold = config.get('queue_threshold_percent', 90)
        self.shed_probability = config.get('shed_probability', 0.5)
        
    def should_shed_load(self, queue_metrics: Dict[str, Any]) -> bool:
        """Determine if load should be shed"""
        # Check system resources
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory_percent = psutil.virtual_memory().percent
        queue_utilization = queue_metrics.get('utilization_percent', 0)
        
        # Shed load if any threshold is exceeded
        if cpu_percent > self.cpu_threshold:
            logging.warning(f"CPU usage {cpu_percent}% exceeds threshold, shedding load")
            return True
        
        if memory_percent > self.memory_threshold:
            logging.warning(f"Memory usage {memory_percent}% exceeds threshold, shedding load")
            return True
        
        if queue_utilization > self.queue_threshold:
            logging.warning(f"Queue utilization {queue_utilization}% exceeds threshold, shedding load")
            return True
        
        return False

class FailFastRequestProcessor:
    """Request processor with fail-fast mechanisms"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.queue = FailFastQueue(config.get('queue_config', {}))
        self.circuit_breaker = CircuitBreaker(config.get('circuit_breaker_config', {}))
        self.load_shedder = LoadShedder(config.get('load_shedder_config', {}))
        
        self.processing = False
        self.processed_count = 0
        self.failed_count = 0
        
    async def submit_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Submit request with fail-fast validation"""
        try:
            # Early validation
            if not self._validate_request(request_data):
                return {
                    'success': False,
                    'error': 'Invalid request format',
                    'failed_fast': True
                }
            
            # Check circuit breaker
            if not self.circuit_breaker.call_allowed():
                return {
                    'success': False,
                    'error': 'Service unavailable (circuit breaker open)',
                    'failed_fast': True
                }
            
            # Check load shedding
            queue_metrics = self.queue.get_metrics()
            if self.load_shedder.should_shed_load(queue_metrics):
                return {
                    'success': False,
                    'error': 'Service overloaded, request rejected',
                    'failed_fast': True
                }
            
            # Create queued request
            request = QueuedRequest(
                request_id=request_data.get('request_id', str(time.time())),
                priority=RequestPriority(request_data.get('priority', 3)),
                payload=request_data,
                queued_at=time.time() * 1000,
                deadline=time.time() * 1000 + request_data.get('timeout_ms', 30000)
            )
            
            # Try to enqueue
            if not self.queue.enqueue(request):
                return {
                    'success': False,
                    'error': 'Queue full or request expired',
                    'failed_fast': True
                }
            
            return {
                'success': True,
                'request_id': request.request_id,
                'queued_at': request.queued_at
            }
            
        except Exception as e:
            logging.error(f"Request submission failed: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'failed_fast': True
            }
    
    def _validate_request(self, request_data: Dict[str, Any]) -> bool:
        """Validate request format and required fields"""
        required_fields = ['action', 'data']
        
        for field in required_fields:
            if field not in request_data:
                logging.warning(f"Missing required field: {field}")
                return False
        
        # Additional validation logic here
        return True
    
    async def start_processing(self):
        """Start processing queued requests"""
        self.processing = True
        logging.info("Started fail-fast request processor")
        
        while self.processing:
            try:
                request = self.queue.dequeue()
                
                if request is None:
                    await asyncio.sleep(0.1)  # No requests, wait briefly
                    continue
                
                # Process request
                success = await self._process_request(request)
                
                if success:
                    self.circuit_breaker.record_success()
                    self.processed_count += 1
                else:
                    self.circuit_breaker.record_failure()
                    self.failed_count += 1
                    
            except Exception as e:
                logging.error(f"Request processing error: {str(e)}")
                self.circuit_breaker.record_failure()
                self.failed_count += 1
                await asyncio.sleep(1)  # Brief pause on error
    
    async def _process_request(self, request: QueuedRequest) -> bool:
        """Process individual request"""
        try:
            # Check if request has expired
            if time.time() * 1000 > request.deadline:
                logging.warning(f"Request {request.request_id} expired during processing")
                return False
            
            # Simulate processing
            processing_time = request.payload.get('processing_time_ms', 100)
            await asyncio.sleep(processing_time / 1000)
            
            logging.debug(f"Processed request {request.request_id}")
            return True
            
        except Exception as e:
            logging.error(f"Request processing failed: {str(e)}")
            return False
    
    def stop_processing(self):
        """Stop processing requests"""
        self.processing = False
        logging.info("Stopped fail-fast request processor")
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get processor metrics"""
        queue_metrics = self.queue.get_metrics()
        
        return {
            'queue_metrics': queue_metrics,
            'processed_count': self.processed_count,
            'failed_count': self.failed_count,
            'circuit_breaker_state': self.circuit_breaker.state,
            'processing': self.processing
        }

# Usage example
async def main():
    config = {
        'queue_config': {
            'max_size': 100,
            'queue_type': 'priority',
            'default_timeout_ms': 30000
        },
        'circuit_breaker_config': {
            'failure_threshold': 5,
            'timeout_seconds': 60
        },
        'load_shedder_config': {
            'cpu_threshold_percent': 80,
            'memory_threshold_percent': 85,
            'queue_threshold_percent': 90
        }
    }
    
    processor = FailFastRequestProcessor(config)
    
    # Start processing in background
    processing_task = asyncio.create_task(processor.start_processing())
    
    # Submit test requests
    for i in range(10):
        request_data = {
            'request_id': f'req_{i}',
            'action': 'process_data',
            'data': {'value': i},
            'priority': 2,
            'timeout_ms': 5000,
            'processing_time_ms': 200
        }
        
        result = await processor.submit_request(request_data)
        print(f"Request {i}: {result}")
        
        await asyncio.sleep(0.1)
    
    # Wait a bit for processing
    await asyncio.sleep(3)
    
    # Get metrics
    metrics = processor.get_metrics()
    print(f"Processor metrics: {metrics}")
    
    # Stop processing
    processor.stop_processing()
    processing_task.cancel()

if __name__ == "__main__":
    asyncio.run(main())
```

## AWS Services Used

- **Amazon SQS**: Message queuing with dead letter queues and visibility timeout for fail-fast behavior
- **AWS Lambda**: Serverless functions with reserved concurrency and timeout configuration
- **Amazon API Gateway**: Request throttling and timeout handling with fail-fast responses
- **Amazon ECS/EKS**: Container orchestration with health checks and resource limits
- **AWS Application Load Balancer**: Health checks and automatic failover for fail-fast routing
- **Amazon CloudWatch**: Monitoring queue depths, failure rates, and system health metrics
- **AWS Auto Scaling**: Automatic scaling based on queue metrics and system load
- **Amazon ElastiCache**: In-memory caching with connection limits and timeout handling
- **Amazon DynamoDB**: Conditional writes and capacity management for fail-fast operations
- **AWS Step Functions**: Workflow timeout and error handling with fail-fast patterns
- **Amazon Kinesis**: Stream processing with shard limits and backpressure handling
- **AWS Batch**: Job queue management with size limits and timeout configuration
- **Amazon EventBridge**: Event processing with retry limits and dead letter queues
- **AWS Systems Manager**: Parameter store for dynamic configuration of fail-fast parameters
- **Amazon Route 53**: Health checks and DNS failover for fail-fast service discovery

## Benefits

- **Improved System Responsiveness**: Quick rejection of failing requests maintains system performance
- **Resource Protection**: Queue limits prevent memory exhaustion and system overload
- **Better Error Handling**: Fast failure detection enables quicker error recovery
- **Enhanced User Experience**: Users receive quick feedback rather than waiting for timeouts
- **Reduced Resource Waste**: Prevents processing of requests that are likely to fail
- **Better Scalability**: Systems can handle higher loads by rejecting excess requests quickly
- **Improved Monitoring**: Clear failure patterns help identify and resolve issues faster
- **Cost Optimization**: Reduced resource consumption through efficient request handling
- **System Stability**: Prevents cascading failures through early failure detection
- **Better SLA Compliance**: Predictable response times through fail-fast mechanisms

## Related Resources

- [AWS Well-Architected Reliability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/)
- [Fail Fast and Limit Queues](https://docs.aws.amazon.com/wellarchitected/latest/framework/rel_mitigate_interaction_failure_fail_fast.html)
- [Amazon SQS Best Practices](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-best-practices.html)
- [AWS Lambda Concurrency](https://docs.aws.amazon.com/lambda/latest/dg/concurrent-executions.html)
- [Amazon API Gateway Throttling](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html)
- [Circuit Breaker Pattern](https://aws.amazon.com/builders-library/implementing-health-checks/)
- [Load Shedding](https://aws.amazon.com/builders-library/using-load-shedding-to-avoid-overload/)
- [Amazon CloudWatch Metrics](https://docs.aws.amazon.com/cloudwatch/latest/monitoring/)
- [AWS Auto Scaling](https://docs.aws.amazon.com/autoscaling/latest/userguide/)
- [Health Checks and Monitoring](https://aws.amazon.com/builders-library/implementing-health-checks/)
- [Queue Management Patterns](https://aws.amazon.com/builders-library/)
- [Building Resilient Systems](https://aws.amazon.com/builders-library/)
