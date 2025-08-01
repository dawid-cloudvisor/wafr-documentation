---
title: REL05-BP03 - Control and limit retry calls
layout: default
parent: REL05 - How do you design interactions in a distributed system to mitigate or withstand failures?
grand_parent: Reliability
nav_order: 3
---

# REL05-BP03: Control and limit retry calls

## Overview

Implement intelligent retry mechanisms with proper controls and limits to handle transient failures without overwhelming downstream services. Effective retry strategies include exponential backoff, jitter, circuit breakers, and retry budgets to prevent retry storms and cascading failures while maintaining system resilience.

## Implementation Steps

### 1. Design Retry Strategies
- Implement exponential backoff with jitter for retry delays
- Configure maximum retry attempts based on operation criticality
- Design different retry strategies for different error types
- Establish retry budgets to prevent retry storms

### 2. Implement Intelligent Error Classification
- Classify errors as retryable vs non-retryable
- Implement different retry policies for different error categories
- Design context-aware retry decisions based on system state
- Handle rate limiting and quota errors appropriately

### 3. Configure Backoff and Jitter Algorithms
- Implement exponential backoff to reduce load on failing services
- Add jitter to prevent thundering herd problems
- Design adaptive backoff based on error patterns
- Configure maximum backoff limits to prevent excessive delays

### 4. Establish Retry Budgets and Limits
- Implement per-client and per-service retry budgets
- Configure retry limits based on SLA requirements
- Design retry budget replenishment strategies
- Monitor retry budget consumption and adjust limits

### 5. Integrate with Circuit Breakers
- Combine retry logic with circuit breaker patterns
- Disable retries when circuit breakers are open
- Implement retry logic for circuit breaker half-open states
- Design coordinated failure handling across retry and circuit breaker systems

### 6. Monitor and Optimize Retry Behavior
- Track retry success rates and patterns
- Monitor retry amplification and system impact
- Implement automated retry policy tuning
- Create dashboards for retry metrics and analysis

## Implementation Examples

### Example 1: Advanced Retry Management System
```python
import asyncio
import random
import time
import logging
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass
from enum import Enum
import boto3
from abc import ABC, abstractmethod

class ErrorType(Enum):
    TRANSIENT = "transient"
    RATE_LIMIT = "rate_limit"
    TIMEOUT = "timeout"
    SERVER_ERROR = "server_error"
    CLIENT_ERROR = "client_error"
    NETWORK_ERROR = "network_error"

class RetryStrategy(Enum):
    EXPONENTIAL_BACKOFF = "exponential_backoff"
    LINEAR_BACKOFF = "linear_backoff"
    FIXED_DELAY = "fixed_delay"
    ADAPTIVE = "adaptive"

@dataclass
class RetryConfig:
    max_attempts: int = 3
    base_delay_ms: int = 100
    max_delay_ms: int = 30000
    backoff_multiplier: float = 2.0
    jitter_factor: float = 0.1
    strategy: RetryStrategy = RetryStrategy.EXPONENTIAL_BACKOFF
    retry_budget: int = 100
    enabled: bool = True

@dataclass
class RetryAttempt:
    attempt_number: int
    delay_ms: int
    error_type: ErrorType
    timestamp: float
    success: bool

class RetryBudgetManager:
    """Manages retry budgets to prevent retry storms"""
    
    def __init__(self, config: Dict[str, Any]):
        self.budgets = {}
        self.replenishment_rate = config.get('replenishment_rate_per_minute', 10)
        self.max_budget = config.get('max_budget', 100)
        self.last_replenishment = time.time()
        
    def consume_budget(self, client_id: str, amount: int = 1) -> bool:
        """Consume retry budget for a client"""
        self._replenish_budgets()
        
        current_budget = self.budgets.get(client_id, self.max_budget)
        
        if current_budget >= amount:
            self.budgets[client_id] = current_budget - amount
            return True
        else:
            logging.warning(f"Retry budget exhausted for client {client_id}")
            return False
    
    def _replenish_budgets(self):
        """Replenish retry budgets based on time elapsed"""
        now = time.time()
        elapsed_minutes = (now - self.last_replenishment) / 60
        
        if elapsed_minutes >= 1:
            replenishment_amount = int(elapsed_minutes * self.replenishment_rate)
            
            for client_id in self.budgets:
                self.budgets[client_id] = min(
                    self.max_budget,
                    self.budgets[client_id] + replenishment_amount
                )
            
            self.last_replenishment = now
    
    def get_remaining_budget(self, client_id: str) -> int:
        """Get remaining retry budget for a client"""
        self._replenish_budgets()
        return self.budgets.get(client_id, self.max_budget)

class ErrorClassifier:
    """Classifies errors for retry decision making"""
    
    def __init__(self):
        self.retryable_errors = {
            ErrorType.TRANSIENT: True,
            ErrorType.RATE_LIMIT: True,
            ErrorType.TIMEOUT: True,
            ErrorType.SERVER_ERROR: True,
            ErrorType.CLIENT_ERROR: False,
            ErrorType.NETWORK_ERROR: True
        }
    
    def classify_error(self, exception: Exception) -> ErrorType:
        """Classify exception into error type"""
        error_message = str(exception).lower()
        
        if "timeout" in error_message or "timed out" in error_message:
            return ErrorType.TIMEOUT
        elif "rate limit" in error_message or "throttl" in error_message:
            return ErrorType.RATE_LIMIT
        elif "500" in error_message or "502" in error_message or "503" in error_message:
            return ErrorType.SERVER_ERROR
        elif "400" in error_message or "401" in error_message or "403" in error_message:
            return ErrorType.CLIENT_ERROR
        elif "connection" in error_message or "network" in error_message:
            return ErrorType.NETWORK_ERROR
        else:
            return ErrorType.TRANSIENT
    
    def is_retryable(self, error_type: ErrorType) -> bool:
        """Check if error type is retryable"""
        return self.retryable_errors.get(error_type, False)

class BackoffCalculator:
    """Calculates backoff delays with jitter"""
    
    @staticmethod
    def exponential_backoff_with_jitter(attempt: int, config: RetryConfig) -> int:
        """Calculate exponential backoff delay with jitter"""
        base_delay = config.base_delay_ms
        multiplier = config.backoff_multiplier
        jitter_factor = config.jitter_factor
        max_delay = config.max_delay_ms
        
        # Calculate exponential delay
        delay = base_delay * (multiplier ** (attempt - 1))
        
        # Apply jitter
        jitter = delay * jitter_factor * (2 * random.random() - 1)
        delay_with_jitter = delay + jitter
        
        # Ensure delay is within bounds
        return int(max(base_delay, min(max_delay, delay_with_jitter)))
    
    @staticmethod
    def adaptive_backoff(attempt: int, config: RetryConfig, 
                        recent_success_rate: float) -> int:
        """Calculate adaptive backoff based on recent success rate"""
        base_delay = BackoffCalculator.exponential_backoff_with_jitter(attempt, config)
        
        # Adjust delay based on success rate
        if recent_success_rate > 0.8:
            # High success rate, reduce delay
            adjustment_factor = 0.5
        elif recent_success_rate > 0.5:
            # Medium success rate, normal delay
            adjustment_factor = 1.0
        else:
            # Low success rate, increase delay
            adjustment_factor = 2.0
        
        return int(base_delay * adjustment_factor)

class IntelligentRetryManager:
    """Advanced retry manager with budget control and intelligent backoff"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.budget_manager = RetryBudgetManager(config.get('budget_config', {}))
        self.error_classifier = ErrorClassifier()
        self.retry_history = {}
        self.success_rates = {}
        
        # Default retry configuration
        self.default_retry_config = RetryConfig(**config.get('default_retry_config', {}))
        
        # Service-specific retry configurations
        self.service_configs = {}
        for service, service_config in config.get('service_configs', {}).items():
            self.service_configs[service] = RetryConfig(**service_config)
    
    async def execute_with_retry(self, 
                               operation: Callable,
                               client_id: str,
                               service_name: str = "default",
                               *args, **kwargs) -> Any:
        """Execute operation with intelligent retry logic"""
        retry_config = self.service_configs.get(service_name, self.default_retry_config)
        
        if not retry_config.enabled:
            return await operation(*args, **kwargs)
        
        last_exception = None
        retry_attempts = []
        
        for attempt in range(1, retry_config.max_attempts + 1):
            try:
                # Execute the operation
                result = await operation(*args, **kwargs)
                
                # Record successful attempt
                self._record_attempt_success(client_id, service_name, attempt, retry_attempts)
                
                return result
                
            except Exception as e:
                last_exception = e
                error_type = self.error_classifier.classify_error(e)
                
                # Check if error is retryable
                if not self.error_classifier.is_retryable(error_type):
                    logging.info(f"Non-retryable error for {service_name}: {str(e)}")
                    break
                
                # Check if we have more attempts
                if attempt >= retry_config.max_attempts:
                    logging.warning(f"Max retry attempts reached for {service_name}")
                    break
                
                # Check retry budget
                if not self.budget_manager.consume_budget(client_id):
                    logging.warning(f"Retry budget exhausted for client {client_id}")
                    break
                
                # Calculate backoff delay
                if retry_config.strategy == RetryStrategy.ADAPTIVE:
                    success_rate = self._get_recent_success_rate(client_id, service_name)
                    delay_ms = BackoffCalculator.adaptive_backoff(attempt, retry_config, success_rate)
                else:
                    delay_ms = BackoffCalculator.exponential_backoff_with_jitter(attempt, retry_config)
                
                # Record retry attempt
                retry_attempt = RetryAttempt(
                    attempt_number=attempt,
                    delay_ms=delay_ms,
                    error_type=error_type,
                    timestamp=time.time(),
                    success=False
                )
                retry_attempts.append(retry_attempt)
                
                logging.info(f"Retrying {service_name} attempt {attempt} after {delay_ms}ms delay")
                
                # Wait before retry
                await asyncio.sleep(delay_ms / 1000)
        
        # All retries failed
        self._record_attempt_failure(client_id, service_name, retry_attempts)
        raise last_exception
    
    def _record_attempt_success(self, client_id: str, service_name: str, 
                              final_attempt: int, retry_attempts: List[RetryAttempt]):
        """Record successful operation for metrics"""
        key = f"{client_id}:{service_name}"
        
        if key not in self.retry_history:
            self.retry_history[key] = []
        
        # Record the successful operation
        success_record = {
            'timestamp': time.time(),
            'attempts': final_attempt,
            'success': True,
            'retry_attempts': retry_attempts
        }
        
        self.retry_history[key].append(success_record)
        
        # Keep only recent history (last 100 operations)
        self.retry_history[key] = self.retry_history[key][-100:]
        
        # Update success rate
        self._update_success_rate(client_id, service_name)
    
    def _record_attempt_failure(self, client_id: str, service_name: str, 
                              retry_attempts: List[RetryAttempt]):
        """Record failed operation for metrics"""
        key = f"{client_id}:{service_name}"
        
        if key not in self.retry_history:
            self.retry_history[key] = []
        
        # Record the failed operation
        failure_record = {
            'timestamp': time.time(),
            'attempts': len(retry_attempts) + 1,
            'success': False,
            'retry_attempts': retry_attempts
        }
        
        self.retry_history[key].append(failure_record)
        
        # Keep only recent history
        self.retry_history[key] = self.retry_history[key][-100:]
        
        # Update success rate
        self._update_success_rate(client_id, service_name)
    
    def _update_success_rate(self, client_id: str, service_name: str):
        """Update success rate for adaptive backoff"""
        key = f"{client_id}:{service_name}"
        history = self.retry_history.get(key, [])
        
        if not history:
            self.success_rates[key] = 1.0
            return
        
        # Calculate success rate from recent history (last 20 operations)
        recent_history = history[-20:]
        successful_operations = sum(1 for record in recent_history if record['success'])
        success_rate = successful_operations / len(recent_history)
        
        self.success_rates[key] = success_rate
    
    def _get_recent_success_rate(self, client_id: str, service_name: str) -> float:
        """Get recent success rate for adaptive backoff"""
        key = f"{client_id}:{service_name}"
        return self.success_rates.get(key, 1.0)
    
    def get_retry_metrics(self, client_id: str, service_name: str) -> Dict[str, Any]:
        """Get retry metrics for monitoring"""
        key = f"{client_id}:{service_name}"
        history = self.retry_history.get(key, [])
        
        if not history:
            return {
                'total_operations': 0,
                'success_rate': 1.0,
                'average_attempts': 1.0,
                'retry_budget_remaining': self.budget_manager.get_remaining_budget(client_id)
            }
        
        total_operations = len(history)
        successful_operations = sum(1 for record in history if record['success'])
        total_attempts = sum(record['attempts'] for record in history)
        
        return {
            'total_operations': total_operations,
            'success_rate': successful_operations / total_operations,
            'average_attempts': total_attempts / total_operations,
            'retry_budget_remaining': self.budget_manager.get_remaining_budget(client_id)
        }

# AWS SDK retry configuration
class AWSRetryConfigManager:
    """Manage AWS SDK retry configurations"""
    
    def __init__(self):
        self.session = boto3.Session()
    
    def configure_boto3_retries(self, service_name: str, retry_config: Dict):
        """Configure boto3 client with custom retry settings"""
        from botocore.config import Config
        from botocore.retries import adaptive
        
        # Create retry configuration
        retry_mode = retry_config.get('mode', 'adaptive')  # standard, adaptive, legacy
        max_attempts = retry_config.get('max_attempts', 3)
        
        config = Config(
            retries={
                'mode': retry_mode,
                'max_attempts': max_attempts
            },
            max_pool_connections=retry_config.get('max_pool_connections', 50)
        )
        
        # Create client with retry configuration
        client = self.session.client(service_name, config=config)
        
        return client

# Usage example
async def main():
    config = {
        'budget_config': {
            'replenishment_rate_per_minute': 10,
            'max_budget': 100
        },
        'default_retry_config': {
            'max_attempts': 3,
            'base_delay_ms': 100,
            'max_delay_ms': 30000,
            'backoff_multiplier': 2.0,
            'jitter_factor': 0.1,
            'strategy': 'adaptive'
        },
        'service_configs': {
            'user_service': {
                'max_attempts': 5,
                'base_delay_ms': 200,
                'strategy': 'exponential_backoff'
            }
        }
    }
    
    retry_manager = IntelligentRetryManager(config)
    
    # Example operation that might fail
    async def unreliable_operation():
        if random.random() < 0.7:  # 70% failure rate
            raise Exception("Service temporarily unavailable")
        return {"status": "success", "data": "operation completed"}
    
    try:
        result = await retry_manager.execute_with_retry(
            unreliable_operation,
            client_id="client_123",
            service_name="user_service"
        )
        print(f"Operation succeeded: {result}")
        
        # Get metrics
        metrics = retry_manager.get_retry_metrics("client_123", "user_service")
        print(f"Retry metrics: {metrics}")
        
    except Exception as e:
        print(f"Operation failed after retries: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
```

## AWS Services Used

- **AWS SDK**: Built-in retry mechanisms with exponential backoff and adaptive retry modes
- **Amazon API Gateway**: Request retry handling and timeout configuration
- **AWS Lambda**: Automatic retry for asynchronous invocations and error handling
- **Amazon SQS**: Message retry with dead letter queues and visibility timeout
- **AWS Step Functions**: Built-in retry and error handling for workflow steps
- **Amazon Kinesis**: Stream retry mechanisms and error record handling
- **Amazon DynamoDB**: Conditional write retries and throttling handling
- **Amazon S3**: Multipart upload retries and error recovery
- **AWS Batch**: Job retry configuration and failure handling
- **Amazon CloudWatch**: Retry metrics monitoring and alerting
- **AWS X-Ray**: Distributed tracing for retry pattern analysis
- **Amazon ElastiCache**: Connection retry and failover handling
- **AWS Systems Manager**: Parameter store for retry configuration management
- **Amazon EventBridge**: Event retry and dead letter queue configuration
- **AWS Secrets Manager**: Retry configuration for secret retrieval operations

## Benefits

- **Improved Resilience**: Automatic recovery from transient failures without manual intervention
- **Reduced Error Rates**: Intelligent retry strategies significantly reduce overall failure rates
- **Better Resource Utilization**: Controlled retries prevent overwhelming downstream services
- **Enhanced User Experience**: Transparent error recovery improves application reliability
- **Cost Optimization**: Efficient retry strategies reduce unnecessary resource consumption
- **Operational Stability**: Prevents retry storms and cascading failures
- **Better Monitoring**: Detailed retry metrics provide insights into system health
- **Adaptive Behavior**: Dynamic retry strategies adapt to changing system conditions
- **SLA Compliance**: Proper retry handling helps maintain service level agreements
- **Simplified Error Handling**: Centralized retry logic reduces code complexity

## Related Resources

- [AWS Well-Architected Reliability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/)
- [Control and Limit Retry Calls](https://docs.aws.amazon.com/wellarchitected/latest/framework/rel_mitigate_interaction_failure_limit_retries.html)
- [AWS SDK Retry Behavior](https://docs.aws.amazon.com/general/latest/gr/api-retries.html)
- [Boto3 Retry Configuration](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/retries.html)
- [Amazon API Gateway Error Handling](https://docs.aws.amazon.com/apigateway/latest/developerguide/handle-errors-in-lambda-integration.html)
- [AWS Lambda Error Handling](https://docs.aws.amazon.com/lambda/latest/dg/invocation-retries.html)
- [Amazon SQS Message Retry](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html)
- [AWS Step Functions Error Handling](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-error-handling.html)
- [Exponential Backoff and Jitter](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)
- [Circuit Breaker Pattern](https://aws.amazon.com/builders-library/implementing-health-checks/)
- [Amazon CloudWatch Metrics](https://docs.aws.amazon.com/cloudwatch/latest/monitoring/)
- [Building Resilient Systems](https://aws.amazon.com/builders-library/)
