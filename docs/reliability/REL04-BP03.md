---
title: REL04-BP03 - Do constant work
layout: default
parent: REL04 - How do you design interactions in a distributed system to prevent failures?
grand_parent: Reliability
nav_order: 3
---

# REL04-BP03: Do constant work

## Overview

Implement constant work patterns to maintain consistent resource utilization and avoid the thundering herd problem that occurs when systems experience sudden spikes in demand. By performing work at a steady rate rather than in bursts, you can improve system predictability, reduce resource contention, and prevent cascading failures caused by sudden load changes.

## Implementation Steps

### 1. Implement Steady-State Processing Patterns
- Design systems to process work at consistent rates
- Use background processing for non-urgent tasks
- Implement work smoothing algorithms to distribute load over time
- Avoid batch processing that creates resource spikes

### 2. Design Proactive Resource Management
- Pre-warm resources before they are needed
- Maintain connection pools at steady levels
- Implement predictive scaling based on patterns
- Use health checks and monitoring to maintain readiness

### 3. Implement Rate Limiting and Throttling
- Apply consistent rate limits to prevent sudden spikes
- Use token bucket algorithms for smooth traffic shaping
- Implement backpressure mechanisms to control flow
- Design adaptive throttling based on system capacity

### 4. Establish Predictable Caching Patterns
- Implement cache warming strategies
- Use consistent cache refresh patterns
- Avoid cache stampede scenarios
- Design cache hierarchies for predictable performance

### 5. Design Consistent Database Access Patterns
- Implement read-through and write-through caching
- Use connection pooling with steady connection counts
- Avoid batch operations that create resource spikes
- Implement consistent query patterns and indexing

### 6. Monitor and Optimize Work Distribution
- Track resource utilization patterns and identify spikes
- Implement metrics for work distribution consistency
- Use automated scaling based on steady-state metrics
- Optimize algorithms to maintain consistent performance

## Implementation Examples

### Example 1: Constant Work Processing System
```python
import asyncio
import time
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import boto3
from concurrent.futures import ThreadPoolExecutor

class WorkPattern(Enum):
    CONSTANT_RATE = "constant_rate"
    ADAPTIVE_RATE = "adaptive_rate"
    PREDICTIVE_RATE = "predictive_rate"

@dataclass
class WorkItem:
    item_id: str
    priority: int
    created_at: float
    data: Dict[str, Any]

class ConstantWorkProcessor:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.target_rate = config.get('target_rate_per_second', 10)
        self.work_pattern = WorkPattern(config.get('work_pattern', 'constant_rate'))
        self.buffer_size = config.get('buffer_size', 1000)
        
        # AWS clients
        self.sqs = boto3.client('sqs')
        self.cloudwatch = boto3.client('cloudwatch')
        
        # Work management
        self.work_buffer: List[WorkItem] = []
        self.processing_rate = self.target_rate
        self.last_adjustment = time.time()
        
        # Metrics
        self.processed_count = 0
        self.error_count = 0
        self.start_time = time.time()
        
    async def start_processing(self):
        """Start constant work processing"""
        logging.info(f"Starting constant work processor at {self.target_rate} items/second")
        
        # Start background tasks
        tasks = [
            asyncio.create_task(self._work_producer()),
            asyncio.create_task(self._work_processor()),
            asyncio.create_task(self._metrics_reporter()),
            asyncio.create_task(self._rate_adjuster())
        ]
        
        try:
            await asyncio.gather(*tasks)
        except Exception as e:
            logging.error(f"Processing error: {str(e)}")
            for task in tasks:
                task.cancel()
    
    async def _work_producer(self):
        """Continuously produce work items at steady rate"""
        while True:
            try:
                # Fetch work from queue
                if len(self.work_buffer) < self.buffer_size:
                    new_items = await self._fetch_work_items()
                    self.work_buffer.extend(new_items)
                
                # Maintain steady production rate
                await asyncio.sleep(0.1)  # Check every 100ms
                
            except Exception as e:
                logging.error(f"Work producer error: {str(e)}")
                await asyncio.sleep(1)
    
    async def _work_processor(self):
        """Process work items at constant rate"""
        interval = 1.0 / self.processing_rate
        
        while True:
            try:
                if self.work_buffer:
                    # Get next work item
                    work_item = self.work_buffer.pop(0)
                    
                    # Process item
                    await self._process_work_item(work_item)
                    self.processed_count += 1
                    
                    # Maintain constant rate
                    await asyncio.sleep(interval)
                else:
                    # No work available, maintain rhythm
                    await asyncio.sleep(interval)
                    
            except Exception as e:
                logging.error(f"Work processor error: {str(e)}")
                self.error_count += 1
                await asyncio.sleep(interval)
    
    async def _rate_adjuster(self):
        """Adjust processing rate based on system conditions"""
        while True:
            try:
                if self.work_pattern == WorkPattern.ADAPTIVE_RATE:
                    await self._adjust_adaptive_rate()
                elif self.work_pattern == WorkPattern.PREDICTIVE_RATE:
                    await self._adjust_predictive_rate()
                
                await asyncio.sleep(30)  # Adjust every 30 seconds
                
            except Exception as e:
                logging.error(f"Rate adjuster error: {str(e)}")
                await asyncio.sleep(30)
    
    async def _adjust_adaptive_rate(self):
        """Adjust rate based on current system conditions"""
        try:
            # Get system metrics
            cpu_utilization = await self._get_cpu_utilization()
            memory_utilization = await self._get_memory_utilization()
            queue_depth = len(self.work_buffer)
            
            # Calculate adjustment factor
            adjustment_factor = 1.0
            
            if cpu_utilization > 80:
                adjustment_factor *= 0.9  # Reduce rate
            elif cpu_utilization < 50:
                adjustment_factor *= 1.1  # Increase rate
            
            if queue_depth > self.buffer_size * 0.8:
                adjustment_factor *= 1.2  # Increase rate to clear backlog
            elif queue_depth < self.buffer_size * 0.2:
                adjustment_factor *= 0.95  # Slightly reduce rate
            
            # Apply adjustment with limits
            new_rate = self.processing_rate * adjustment_factor
            new_rate = max(1, min(new_rate, self.target_rate * 2))
            
            if abs(new_rate - self.processing_rate) > 0.5:
                logging.info(f"Adjusting processing rate from {self.processing_rate:.2f} to {new_rate:.2f}")
                self.processing_rate = new_rate
                self.last_adjustment = time.time()
            
        except Exception as e:
            logging.error(f"Adaptive rate adjustment failed: {str(e)}")
    
    async def _fetch_work_items(self) -> List[WorkItem]:
        """Fetch work items from queue"""
        try:
            queue_url = self.config.get('work_queue_url')
            if not queue_url:
                return []
            
            response = self.sqs.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=10,
                WaitTimeSeconds=1
            )
            
            work_items = []
            for message in response.get('Messages', []):
                work_item = WorkItem(
                    item_id=message['MessageId'],
                    priority=1,
                    created_at=time.time(),
                    data=json.loads(message['Body'])
                )
                work_items.append(work_item)
                
                # Delete message from queue
                self.sqs.delete_message(
                    QueueUrl=queue_url,
                    ReceiptHandle=message['ReceiptHandle']
                )
            
            return work_items
            
        except Exception as e:
            logging.error(f"Failed to fetch work items: {str(e)}")
            return []
    
    async def _process_work_item(self, work_item: WorkItem):
        """Process individual work item"""
        try:
            # Simulate work processing
            processing_time = work_item.data.get('processing_time', 0.1)
            await asyncio.sleep(processing_time)
            
            # Log processing
            logging.debug(f"Processed work item {work_item.item_id}")
            
        except Exception as e:
            logging.error(f"Failed to process work item {work_item.item_id}: {str(e)}")
            raise

class TokenBucketRateLimiter:
    """Token bucket rate limiter for constant work patterns"""
    
    def __init__(self, rate: float, capacity: int):
        self.rate = rate  # tokens per second
        self.capacity = capacity  # maximum tokens
        self.tokens = capacity
        self.last_update = time.time()
        self.lock = asyncio.Lock()
    
    async def acquire(self, tokens: int = 1) -> bool:
        """Acquire tokens from bucket"""
        async with self.lock:
            now = time.time()
            
            # Add tokens based on elapsed time
            elapsed = now - self.last_update
            self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
            self.last_update = now
            
            # Check if enough tokens available
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            else:
                return False
    
    async def wait_for_tokens(self, tokens: int = 1):
        """Wait until tokens are available"""
        while not await self.acquire(tokens):
            await asyncio.sleep(0.01)  # Wait 10ms before retry

# Usage example
async def main():
    config = {
        'target_rate_per_second': 10,
        'work_pattern': 'adaptive_rate',
        'buffer_size': 100,
        'work_queue_url': 'https://sqs.us-east-1.amazonaws.com/123456789012/work-queue'
    }
    
    processor = ConstantWorkProcessor(config)
    await processor.start_processing()

if __name__ == "__main__":
    asyncio.run(main())
```

## AWS Services Used

- **Amazon SQS**: Message queuing with consistent polling patterns for steady work distribution
- **AWS Lambda**: Serverless functions with reserved concurrency for predictable execution
- **Amazon CloudWatch**: Monitoring and metrics for tracking work distribution patterns
- **Amazon Kinesis**: Stream processing with consistent shard allocation and processing
- **AWS Step Functions**: Workflow orchestration with consistent execution patterns
- **Amazon DynamoDB**: Database with consistent read/write patterns and auto-scaling
- **Amazon ElastiCache**: Caching with consistent connection pools and refresh patterns
- **AWS Auto Scaling**: Predictive scaling based on historical patterns
- **Amazon EventBridge**: Event processing with consistent rate limiting
- **AWS Batch**: Batch processing with steady job submission patterns
- **Amazon ECS/EKS**: Container orchestration with consistent resource allocation
- **AWS Systems Manager**: Parameter store for configuration management
- **Amazon CloudFront**: CDN with consistent cache warming patterns
- **Elastic Load Balancing**: Load balancing with consistent health checking
- **AWS X-Ray**: Distributed tracing for monitoring consistent performance patterns

## Benefits

- **Predictable Performance**: Consistent resource utilization leads to predictable system behavior
- **Reduced Resource Contention**: Steady work patterns prevent resource spikes and contention
- **Improved Scalability**: Consistent load patterns enable better auto-scaling decisions
- **Better Cost Management**: Predictable resource usage enables better cost optimization
- **Enhanced Reliability**: Avoiding sudden spikes reduces the risk of cascading failures
- **Simplified Monitoring**: Consistent patterns make it easier to detect anomalies
- **Better User Experience**: Steady performance provides consistent response times
- **Reduced Thundering Herd**: Constant work patterns prevent sudden demand spikes
- **Improved Resource Planning**: Predictable patterns enable better capacity planning
- **Enhanced System Stability**: Consistent work distribution improves overall system stability

## Related Resources

- [AWS Well-Architected Reliability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/)
- [Do Constant Work](https://docs.aws.amazon.com/wellarchitected/latest/framework/rel_prevent_interaction_failure_constant_work.html)
- [Amazon SQS Best Practices](https://docs.aws.amazon.com/sqs/latest/dg/sqs-best-practices.html)
- [AWS Lambda Concurrency](https://docs.aws.amazon.com/lambda/latest/dg/concurrent-executions.html)
- [Amazon CloudWatch User Guide](https://docs.aws.amazon.com/cloudwatch/latest/monitoring/)
- [AWS Auto Scaling User Guide](https://docs.aws.amazon.com/autoscaling/latest/userguide/)
- [Rate Limiting Patterns](https://aws.amazon.com/builders-library/using-load-shedding-to-avoid-overload/)
- [Thundering Herd Problem](https://aws.amazon.com/builders-library/avoiding-fallback-in-distributed-systems/)
- [Amazon Kinesis Best Practices](https://docs.aws.amazon.com/kinesis/latest/dev/kinesis-record-processor-scaling.html)
- [AWS Batch User Guide](https://docs.aws.amazon.com/batch/latest/userguide/)
- [Predictive Scaling](https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-predictive-scaling.html)
- [Building Resilient Systems](https://aws.amazon.com/builders-library/)
