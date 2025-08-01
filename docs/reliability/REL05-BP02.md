---
title: REL05-BP02 - Throttle requests
layout: default
parent: REL05 - How do you design interactions in a distributed system to mitigate or withstand failures?
grand_parent: Reliability
nav_order: 2
---

# REL05-BP02: Throttle requests

## Overview

Implement request throttling mechanisms to control the rate of incoming requests and prevent system overload. Throttling protects downstream services from being overwhelmed, maintains system stability during traffic spikes, and ensures fair resource allocation across different clients and request types.

## Implementation Steps

### 1. Design Rate Limiting Strategies
- Implement token bucket and leaky bucket algorithms
- Configure rate limits based on client, API endpoint, and resource type
- Design adaptive throttling based on system capacity and health
- Establish different rate limits for different service tiers

### 2. Implement Client-Based Throttling
- Apply rate limits per client ID or API key
- Implement sliding window rate limiting
- Design burst allowances for legitimate traffic spikes
- Create whitelisting mechanisms for critical clients

### 3. Configure Resource-Based Throttling
- Implement throttling based on CPU, memory, and database utilization
- Design backpressure mechanisms for queue-based systems
- Configure adaptive limits based on downstream service capacity
- Implement priority-based throttling for different request types

### 4. Establish Graceful Throttling Responses
- Return appropriate HTTP status codes (429 Too Many Requests)
- Include retry-after headers with backoff recommendations
- Provide informative error messages and guidance
- Implement progressive throttling with warnings before limits

### 5. Monitor and Tune Throttling Parameters
- Track throttling metrics and patterns
- Implement automated tuning based on system performance
- Monitor false positive throttling and adjust limits
- Create dashboards for throttling visibility and analysis

### 6. Test Throttling Under Load
- Conduct load testing to validate throttling effectiveness
- Test throttling behavior during traffic spikes
- Validate client retry behavior and backoff strategies
- Ensure throttling doesn't impact legitimate traffic

## Implementation Examples

### Example 1: Advanced Request Throttling System
```python
import asyncio
import time
import logging
from typing import Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import redis
import boto3
from collections import defaultdict, deque

class ThrottlingAlgorithm(Enum):
    TOKEN_BUCKET = "token_bucket"
    LEAKY_BUCKET = "leaky_bucket"
    SLIDING_WINDOW = "sliding_window"
    FIXED_WINDOW = "fixed_window"

@dataclass
class ThrottlingRule:
    name: str
    algorithm: ThrottlingAlgorithm
    requests_per_second: float
    burst_capacity: int
    window_size_seconds: int = 60
    enabled: bool = True

class TokenBucketThrottler:
    """Token bucket throttling implementation"""
    
    def __init__(self, requests_per_second: float, burst_capacity: int):
        self.rate = requests_per_second
        self.capacity = burst_capacity
        self.tokens = burst_capacity
        self.last_refill = time.time()
        
    def is_allowed(self, tokens_requested: int = 1) -> Tuple[bool, float]:
        """Check if request is allowed and return wait time if not"""
        now = time.time()
        
        # Refill tokens based on elapsed time
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
        self.last_refill = now
        
        if self.tokens >= tokens_requested:
            self.tokens -= tokens_requested
            return True, 0.0
        else:
            # Calculate wait time for next token
            wait_time = (tokens_requested - self.tokens) / self.rate
            return False, wait_time

class SlidingWindowThrottler:
    """Sliding window throttling implementation"""
    
    def __init__(self, requests_per_window: int, window_size_seconds: int):
        self.limit = requests_per_window
        self.window_size = window_size_seconds
        self.requests = deque()
        
    def is_allowed(self) -> Tuple[bool, float]:
        """Check if request is allowed"""
        now = time.time()
        
        # Remove old requests outside the window
        while self.requests and self.requests[0] <= now - self.window_size:
            self.requests.popleft()
        
        if len(self.requests) < self.limit:
            self.requests.append(now)
            return True, 0.0
        else:
            # Calculate wait time until oldest request expires
            wait_time = self.requests[0] + self.window_size - now
            return False, max(0, wait_time)

class AdaptiveThrottler:
    """Adaptive throttling based on system metrics"""
    
    def __init__(self, config: Dict):
        self.base_rate = config.get('base_requests_per_second', 100)
        self.min_rate = config.get('min_requests_per_second', 10)
        self.max_rate = config.get('max_requests_per_second', 1000)
        self.current_rate = self.base_rate
        
        # System metrics thresholds
        self.cpu_threshold = config.get('cpu_threshold', 80)
        self.memory_threshold = config.get('memory_threshold', 85)
        self.error_rate_threshold = config.get('error_rate_threshold', 5)
        
        # Adjustment factors
        self.increase_factor = config.get('increase_factor', 1.1)
        self.decrease_factor = config.get('decrease_factor', 0.8)
        
        self.throttler = TokenBucketThrottler(self.current_rate, int(self.current_rate * 2))
        self.last_adjustment = time.time()
        
    async def is_allowed(self, system_metrics: Dict) -> Tuple[bool, float]:
        """Check if request is allowed with adaptive rate adjustment"""
        # Adjust rate based on system metrics
        await self._adjust_rate(system_metrics)
        
        return self.throttler.is_allowed()
    
    async def _adjust_rate(self, metrics: Dict):
        """Adjust throttling rate based on system metrics"""
        now = time.time()
        
        # Only adjust every 10 seconds
        if now - self.last_adjustment < 10:
            return
        
        cpu_usage = metrics.get('cpu_usage_percent', 0)
        memory_usage = metrics.get('memory_usage_percent', 0)
        error_rate = metrics.get('error_rate_percent', 0)
        
        should_decrease = (
            cpu_usage > self.cpu_threshold or
            memory_usage > self.memory_threshold or
            error_rate > self.error_rate_threshold
        )
        
        should_increase = (
            cpu_usage < self.cpu_threshold * 0.7 and
            memory_usage < self.memory_threshold * 0.7 and
            error_rate < self.error_rate_threshold * 0.5
        )
        
        if should_decrease:
            new_rate = max(self.min_rate, self.current_rate * self.decrease_factor)
            if new_rate != self.current_rate:
                logging.info(f"Decreasing throttling rate from {self.current_rate} to {new_rate}")
                self.current_rate = new_rate
                self.throttler = TokenBucketThrottler(self.current_rate, int(self.current_rate * 2))
        
        elif should_increase:
            new_rate = min(self.max_rate, self.current_rate * self.increase_factor)
            if new_rate != self.current_rate:
                logging.info(f"Increasing throttling rate from {self.current_rate} to {new_rate}")
                self.current_rate = new_rate
                self.throttler = TokenBucketThrottler(self.current_rate, int(self.current_rate * 2))
        
        self.last_adjustment = now

class DistributedThrottlingManager:
    """Distributed throttling using Redis"""
    
    def __init__(self, redis_client, config: Dict):
        self.redis = redis_client
        self.config = config
        self.throttling_rules = {}
        
    def add_throttling_rule(self, client_id: str, rule: ThrottlingRule):
        """Add throttling rule for a client"""
        self.throttling_rules[client_id] = rule
        
    async def is_request_allowed(self, client_id: str, endpoint: str = "default") -> Dict:
        """Check if request is allowed for client and endpoint"""
        rule = self.throttling_rules.get(client_id)
        if not rule or not rule.enabled:
            return {"allowed": True, "wait_time": 0}
        
        key = f"throttle:{client_id}:{endpoint}"
        
        if rule.algorithm == ThrottlingAlgorithm.TOKEN_BUCKET:
            return await self._check_token_bucket_redis(key, rule)
        elif rule.algorithm == ThrottlingAlgorithm.SLIDING_WINDOW:
            return await self._check_sliding_window_redis(key, rule)
        else:
            return {"allowed": True, "wait_time": 0}
    
    async def _check_token_bucket_redis(self, key: str, rule: ThrottlingRule) -> Dict:
        """Distributed token bucket using Redis"""
        lua_script = """
        local key = KEYS[1]
        local rate = tonumber(ARGV[1])
        local capacity = tonumber(ARGV[2])
        local tokens_requested = tonumber(ARGV[3])
        local now = tonumber(ARGV[4])
        
        local bucket = redis.call('HMGET', key, 'tokens', 'last_refill')
        local tokens = tonumber(bucket[1]) or capacity
        local last_refill = tonumber(bucket[2]) or now
        
        -- Refill tokens
        local elapsed = now - last_refill
        tokens = math.min(capacity, tokens + elapsed * rate)
        
        if tokens >= tokens_requested then
            tokens = tokens - tokens_requested
            redis.call('HMSET', key, 'tokens', tokens, 'last_refill', now)
            redis.call('EXPIRE', key, 3600)
            return {1, 0}
        else
            local wait_time = (tokens_requested - tokens) / rate
            redis.call('HMSET', key, 'tokens', tokens, 'last_refill', now)
            redis.call('EXPIRE', key, 3600)
            return {0, wait_time}
        end
        """
        
        try:
            result = await self.redis.eval(
                lua_script, 1, key,
                rule.requests_per_second,
                rule.burst_capacity,
                1,  # tokens requested
                time.time()
            )
            
            return {
                "allowed": bool(result[0]),
                "wait_time": float(result[1])
            }
        except Exception as e:
            logging.error(f"Redis throttling check failed: {str(e)}")
            return {"allowed": True, "wait_time": 0}  # Fail open

# AWS API Gateway integration
class APIGatewayThrottlingManager:
    """Manage API Gateway throttling settings"""
    
    def __init__(self):
        self.apigateway = boto3.client('apigateway')
        self.cloudwatch = boto3.client('cloudwatch')
    
    def configure_api_throttling(self, api_id: str, stage_name: str, 
                               throttling_config: Dict):
        """Configure API Gateway throttling"""
        try:
            # Update stage throttling
            self.apigateway.update_stage(
                restApiId=api_id,
                stageName=stage_name,
                patchOps=[
                    {
                        'op': 'replace',
                        'path': '/throttle/rateLimit',
                        'value': str(throttling_config.get('rate_limit', 1000))
                    },
                    {
                        'op': 'replace',
                        'path': '/throttle/burstLimit',
                        'value': str(throttling_config.get('burst_limit', 2000))
                    }
                ]
            )
            
            logging.info(f"Updated throttling for API {api_id} stage {stage_name}")
            
        except Exception as e:
            logging.error(f"Failed to configure API throttling: {str(e)}")
    
    def create_usage_plan(self, plan_name: str, throttling_config: Dict) -> str:
        """Create usage plan with throttling limits"""
        try:
            response = self.apigateway.create_usage_plan(
                name=plan_name,
                description=f"Usage plan with throttling: {plan_name}",
                throttle={
                    'rateLimit': throttling_config.get('rate_limit', 100),
                    'burstLimit': throttling_config.get('burst_limit', 200)
                },
                quota={
                    'limit': throttling_config.get('quota_limit', 10000),
                    'period': throttling_config.get('quota_period', 'DAY')
                }
            )
            
            usage_plan_id = response['id']
            logging.info(f"Created usage plan: {usage_plan_id}")
            return usage_plan_id
            
        except Exception as e:
            logging.error(f"Failed to create usage plan: {str(e)}")
            return ""

# Usage example
async def main():
    # Initialize Redis client
    redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
    
    # Create distributed throttling manager
    throttling_manager = DistributedThrottlingManager(redis_client, {})
    
    # Add throttling rules
    rule = ThrottlingRule(
        name="api_client_basic",
        algorithm=ThrottlingAlgorithm.TOKEN_BUCKET,
        requests_per_second=10.0,
        burst_capacity=20
    )
    
    throttling_manager.add_throttling_rule("client_123", rule)
    
    # Check if request is allowed
    result = await throttling_manager.is_request_allowed("client_123", "/api/users")
    
    if result["allowed"]:
        print("Request allowed")
    else:
        print(f"Request throttled, wait {result['wait_time']} seconds")

if __name__ == "__main__":
    asyncio.run(main())
```

## AWS Services Used

- **Amazon API Gateway**: Built-in request throttling with rate limiting and burst capacity
- **AWS Lambda**: Serverless functions with reserved concurrency for throttling control
- **Amazon ElastiCache (Redis)**: Distributed throttling state management and rate limiting
- **Amazon CloudWatch**: Monitoring throttling metrics and automated scaling triggers
- **AWS Application Load Balancer**: Request rate limiting and connection throttling
- **Amazon DynamoDB**: Throttling configuration storage and request tracking
- **AWS WAF**: Web application firewall with rate-based rules and IP throttling
- **Amazon Kinesis**: Stream throttling and backpressure management
- **AWS Step Functions**: Workflow throttling and execution rate control
- **Amazon SQS**: Message throttling and visibility timeout management
- **AWS Systems Manager**: Parameter store for dynamic throttling configuration
- **Amazon CloudFront**: CDN-level rate limiting and geographic throttling
- **AWS X-Ray**: Distributed tracing for throttling pattern analysis
- **Amazon Route 53**: DNS-based load balancing with health-based throttling
- **AWS Auto Scaling**: Automatic scaling based on throttling metrics

## Benefits

- **System Protection**: Prevents system overload and maintains stability during traffic spikes
- **Fair Resource Allocation**: Ensures equitable access to resources across different clients
- **Improved Performance**: Maintains consistent response times by controlling request rates
- **Cost Control**: Prevents excessive resource consumption and associated costs
- **Better User Experience**: Provides predictable service availability and response times
- **DDoS Protection**: Helps mitigate distributed denial-of-service attacks
- **Capacity Planning**: Provides insights into system capacity and usage patterns
- **Service Level Management**: Enables different service tiers with appropriate rate limits
- **Graceful Degradation**: Allows systems to degrade gracefully under high load
- **Operational Stability**: Reduces the risk of cascading failures due to overload

## Related Resources

- [AWS Well-Architected Reliability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/)
- [Throttle Requests](https://docs.aws.amazon.com/wellarchitected/latest/framework/rel_mitigate_interaction_failure_throttle_requests.html)
- [Amazon API Gateway Throttling](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html)
- [AWS Lambda Concurrency](https://docs.aws.amazon.com/lambda/latest/dg/concurrent-executions.html)
- [Amazon ElastiCache for Redis](https://docs.aws.amazon.com/elasticache/latest/red-ug/)
- [AWS WAF Rate-Based Rules](https://docs.aws.amazon.com/waf/latest/developerguide/waf-rule-statement-type-rate-based.html)
- [Application Load Balancer Request Routing](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/)
- [Rate Limiting Patterns](https://aws.amazon.com/builders-library/using-load-shedding-to-avoid-overload/)
- [Amazon CloudWatch Metrics](https://docs.aws.amazon.com/cloudwatch/latest/monitoring/)
- [AWS Auto Scaling User Guide](https://docs.aws.amazon.com/autoscaling/latest/userguide/)
- [Token Bucket Algorithm](https://en.wikipedia.org/wiki/Token_bucket)
- [Building Resilient Systems](https://aws.amazon.com/builders-library/)
