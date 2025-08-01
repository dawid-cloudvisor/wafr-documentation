---
title: REL04-BP02 - Implement loosely coupled dependencies
layout: default
parent: REL04 - How do you design interactions in a distributed system to prevent failures?
grand_parent: Reliability
nav_order: 2
---

# REL04-BP02: Implement loosely coupled dependencies

## Overview

Design and implement loosely coupled dependencies between distributed system components to minimize the impact of failures and enable independent evolution of services. Loose coupling reduces cascading failures, improves system resilience, and allows services to operate independently even when dependencies are unavailable or degraded.

## Implementation Steps

### 1. Design Asynchronous Communication Patterns
- Implement message queues and event-driven architectures
- Use publish-subscribe patterns for service communication
- Design fire-and-forget messaging for non-critical operations
- Implement event sourcing and CQRS patterns where appropriate

### 2. Implement Service Interface Abstraction
- Create abstraction layers between services and their dependencies
- Use dependency injection and interface-based programming
- Implement adapter patterns for external service integration
- Design service contracts that hide implementation details

### 3. Establish Temporal Decoupling
- Implement asynchronous processing for time-consuming operations
- Use message queues to buffer requests during peak loads
- Design batch processing for non-real-time operations
- Implement eventual consistency patterns where appropriate

### 4. Implement Spatial Decoupling
- Use service discovery mechanisms instead of hard-coded endpoints
- Implement load balancers and service meshes for routing
- Design location-transparent service communication
- Use content-based routing and message transformation

### 5. Design Failure Isolation Mechanisms
- Implement bulkhead patterns to isolate failures
- Use circuit breakers to prevent cascading failures
- Design graceful degradation and fallback mechanisms
- Implement timeout and retry strategies with exponential backoff

### 6. Establish Data Decoupling Strategies
- Avoid shared databases between services
- Implement data replication and synchronization patterns
- Use event-driven data consistency mechanisms
- Design service-specific data models and storage
## Implementation Examples

### Example 1: Loosely Coupled Architecture Implementation Framework
```python
import boto3
import json
import logging
import asyncio
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from enum import Enum
from abc import ABC, abstractmethod
import concurrent.futures
import threading
from contextlib import asynccontextmanager

class CouplingType(Enum):
    TEMPORAL = "temporal"
    SPATIAL = "spatial"
    PLATFORM = "platform"
    DATA = "data"

class CommunicationPattern(Enum):
    SYNCHRONOUS = "synchronous"
    ASYNCHRONOUS = "asynchronous"
    EVENT_DRIVEN = "event_driven"
    STREAMING = "streaming"

@dataclass
class ServiceDependency:
    service_name: str
    dependency_name: str
    coupling_type: CouplingType
    communication_pattern: CommunicationPattern
    criticality: str
    timeout_ms: int
    retry_config: Dict[str, Any]
    fallback_strategy: str

class ServiceInterface(ABC):
    """Abstract interface for service dependencies"""
    
    @abstractmethod
    async def call(self, request: Dict[str, Any]) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    async def health_check(self) -> bool:
        pass

class CircuitBreaker:
    """Circuit breaker implementation for fault tolerance"""
    
    def __init__(self, failure_threshold: int = 5, timeout_seconds: int = 60, 
                 half_open_max_calls: int = 3):
        self.failure_threshold = failure_threshold
        self.timeout_seconds = timeout_seconds
        self.half_open_max_calls = half_open_max_calls
        
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
        self.half_open_calls = 0
        self.lock = threading.Lock()
    
    async def call(self, func: Callable, *args, **kwargs):
        """Execute function with circuit breaker protection"""
        with self.lock:
            if self.state == "OPEN":
                if self._should_attempt_reset():
                    self.state = "HALF_OPEN"
                    self.half_open_calls = 0
                else:
                    raise Exception("Circuit breaker is OPEN")
            
            if self.state == "HALF_OPEN":
                if self.half_open_calls >= self.half_open_max_calls:
                    raise Exception("Circuit breaker HALF_OPEN limit exceeded")
                self.half_open_calls += 1
        
        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e
    
    def _should_attempt_reset(self) -> bool:
        """Check if circuit breaker should attempt reset"""
        if self.last_failure_time is None:
            return True
        return time.time() - self.last_failure_time >= self.timeout_seconds
    
    def _on_success(self):
        """Handle successful call"""
        with self.lock:
            self.failure_count = 0
            if self.state == "HALF_OPEN":
                self.state = "CLOSED"
    
    def _on_failure(self):
        """Handle failed call"""
        with self.lock:
            self.failure_count += 1
            self.last_failure_time = time.time()
            
            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"

class AsyncServiceClient(ServiceInterface):
    """Asynchronous service client with loose coupling patterns"""
    
    def __init__(self, service_config: Dict[str, Any]):
        self.service_name = service_config['name']
        self.endpoint_url = service_config.get('endpoint_url')
        self.timeout_ms = service_config.get('timeout_ms', 5000)
        self.retry_config = service_config.get('retry_config', {
            'max_retries': 3,
            'backoff_factor': 2,
            'base_delay_ms': 100
        })
        
        # Initialize circuit breaker
        self.circuit_breaker = CircuitBreaker(
            failure_threshold=service_config.get('circuit_breaker', {}).get('failure_threshold', 5),
            timeout_seconds=service_config.get('circuit_breaker', {}).get('timeout_seconds', 60)
        )
        
        # Initialize AWS clients
        self.sqs = boto3.client('sqs')
        self.sns = boto3.client('sns')
        self.eventbridge = boto3.client('events')
        
        # Message queue for async communication
        self.request_queue_url = service_config.get('request_queue_url')
        self.response_topic_arn = service_config.get('response_topic_arn')
    
    async def call(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Make service call with circuit breaker protection"""
        return await self.circuit_breaker.call(self._make_request, request)
    
    async def _make_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Make actual service request with retry logic"""
        last_exception = None
        
        for attempt in range(self.retry_config['max_retries'] + 1):
            try:
                if self.request_queue_url:
                    # Asynchronous communication via SQS
                    return await self._send_async_request(request)
                else:
                    # Synchronous HTTP request (with timeout)
                    return await self._send_sync_request(request)
                    
            except Exception as e:
                last_exception = e
                if attempt < self.retry_config['max_retries']:
                    delay = self._calculate_backoff_delay(attempt)
                    await asyncio.sleep(delay / 1000)  # Convert to seconds
                    logging.warning(f"Request failed, retrying in {delay}ms: {str(e)}")
        
        raise last_exception
    
    async def _send_async_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Send asynchronous request via message queue"""
        try:
            # Add correlation ID for response tracking
            correlation_id = f"{self.service_name}_{int(time.time() * 1000)}"
            request['correlation_id'] = correlation_id
            request['response_topic'] = self.response_topic_arn
            request['timestamp'] = datetime.utcnow().isoformat()
            
            # Send message to SQS queue
            response = self.sqs.send_message(
                QueueUrl=self.request_queue_url,
                MessageBody=json.dumps(request),
                MessageAttributes={
                    'CorrelationId': {
                        'StringValue': correlation_id,
                        'DataType': 'String'
                    },
                    'ServiceName': {
                        'StringValue': self.service_name,
                        'DataType': 'String'
                    }
                }
            )
            
            # For async calls, return immediately with correlation ID
            return {
                'status': 'accepted',
                'correlation_id': correlation_id,
                'message_id': response['MessageId']
            }
            
        except Exception as e:
            logging.error(f"Async request failed: {str(e)}")
            raise
    
    async def _send_sync_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Send synchronous HTTP request"""
        import aiohttp
        
        try:
            timeout = aiohttp.ClientTimeout(total=self.timeout_ms / 1000)
            
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(self.endpoint_url, json=request) as response:
                    if response.status >= 400:
                        raise Exception(f"HTTP {response.status}: {await response.text()}")
                    
                    return await response.json()
                    
        except asyncio.TimeoutError:
            raise Exception(f"Request timeout after {self.timeout_ms}ms")
        except Exception as e:
            logging.error(f"Sync request failed: {str(e)}")
            raise
    
    def _calculate_backoff_delay(self, attempt: int) -> int:
        """Calculate exponential backoff delay"""
        base_delay = self.retry_config['base_delay_ms']
        backoff_factor = self.retry_config['backoff_factor']
        return int(base_delay * (backoff_factor ** attempt))
    
    async def health_check(self) -> bool:
        """Perform health check on the service"""
        try:
            if self.endpoint_url:
                # HTTP health check
                import aiohttp
                timeout = aiohttp.ClientTimeout(total=5)
                
                async with aiohttp.ClientSession(timeout=timeout) as session:
                    health_url = f"{self.endpoint_url}/health"
                    async with session.get(health_url) as response:
                        return response.status == 200
            else:
                # Queue-based health check
                return await self._check_queue_health()
                
        except Exception as e:
            logging.warning(f"Health check failed for {self.service_name}: {str(e)}")
            return False
    
    async def _check_queue_health(self) -> bool:
        """Check health of message queue"""
        try:
            if self.request_queue_url:
                # Check queue attributes
                response = self.sqs.get_queue_attributes(
                    QueueUrl=self.request_queue_url,
                    AttributeNames=['ApproximateNumberOfMessages']
                )
                return True  # If we can get attributes, queue is healthy
            return False
            
        except Exception:
            return False

class EventDrivenService:
    """Service implementation using event-driven patterns"""
    
    def __init__(self, service_config: Dict[str, Any]):
        self.service_name = service_config['name']
        self.event_bus_name = service_config.get('event_bus_name', 'default')
        
        # Initialize AWS clients
        self.eventbridge = boto3.client('events')
        self.sqs = boto3.client('sqs')
        self.sns = boto3.client('sns')
        
        # Event handlers registry
        self.event_handlers: Dict[str, Callable] = {}
        
        # Dead letter queue for failed events
        self.dlq_url = service_config.get('dead_letter_queue_url')
    
    def register_event_handler(self, event_type: str, handler: Callable):
        """Register handler for specific event type"""
        self.event_handlers[event_type] = handler
        logging.info(f"Registered handler for event type: {event_type}")
    
    async def publish_event(self, event_type: str, event_data: Dict[str, Any]):
        """Publish event to EventBridge"""
        try:
            event_entry = {
                'Source': self.service_name,
                'DetailType': event_type,
                'Detail': json.dumps({
                    **event_data,
                    'timestamp': datetime.utcnow().isoformat(),
                    'service_name': self.service_name
                }),
                'EventBusName': self.event_bus_name
            }
            
            response = self.eventbridge.put_events(Entries=[event_entry])
            
            if response['FailedEntryCount'] > 0:
                raise Exception(f"Failed to publish event: {response['Entries'][0].get('ErrorMessage')}")
            
            logging.info(f"Published event {event_type} to {self.event_bus_name}")
            
        except Exception as e:
            logging.error(f"Failed to publish event {event_type}: {str(e)}")
            raise
    
    async def process_event(self, event: Dict[str, Any]):
        """Process incoming event"""
        try:
            event_type = event.get('DetailType')
            event_data = json.loads(event.get('Detail', '{}'))
            
            if event_type in self.event_handlers:
                handler = self.event_handlers[event_type]
                await handler(event_data)
                logging.info(f"Successfully processed event {event_type}")
            else:
                logging.warning(f"No handler registered for event type: {event_type}")
                
        except Exception as e:
            logging.error(f"Failed to process event: {str(e)}")
            
            # Send to dead letter queue if configured
            if self.dlq_url:
                await self._send_to_dlq(event, str(e))
            
            raise
    
    async def _send_to_dlq(self, event: Dict[str, Any], error_message: str):
        """Send failed event to dead letter queue"""
        try:
            dlq_message = {
                'original_event': event,
                'error_message': error_message,
                'failed_at': datetime.utcnow().isoformat(),
                'service_name': self.service_name
            }
            
            self.sqs.send_message(
                QueueUrl=self.dlq_url,
                MessageBody=json.dumps(dlq_message)
            )
            
            logging.info("Sent failed event to dead letter queue")
            
        except Exception as e:
            logging.error(f"Failed to send event to DLQ: {str(e)}")

class LooseCouplingOrchestrator:
    """Orchestrator for managing loosely coupled services"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.services: Dict[str, AsyncServiceClient] = {}
        self.event_service = EventDrivenService(config.get('event_service', {}))
        
        # Initialize services
        for service_config in config.get('services', []):
            service_name = service_config['name']
            self.services[service_name] = AsyncServiceClient(service_config)
    
    async def execute_workflow(self, workflow_config: Dict[str, Any]) -> Dict[str, Any]:
        """Execute workflow with loose coupling patterns"""
        workflow_id = f"workflow_{int(time.time() * 1000)}"
        workflow_result = {
            'workflow_id': workflow_id,
            'status': 'started',
            'steps': [],
            'started_at': datetime.utcnow().isoformat()
        }
        
        try:
            steps = workflow_config.get('steps', [])
            
            for step_config in steps:
                step_result = await self._execute_step(step_config)
                workflow_result['steps'].append(step_result)
                
                # Check if step failed and handle accordingly
                if not step_result.get('success', False):
                    if step_config.get('required', True):
                        workflow_result['status'] = 'failed'
                        break
                    else:
                        # Continue with optional step failure
                        logging.warning(f"Optional step failed: {step_config.get('name')}")
            
            if workflow_result['status'] != 'failed':
                workflow_result['status'] = 'completed'
            
            workflow_result['completed_at'] = datetime.utcnow().isoformat()
            
            # Publish workflow completion event
            await self.event_service.publish_event(
                'WorkflowCompleted',
                {
                    'workflow_id': workflow_id,
                    'status': workflow_result['status'],
                    'duration_ms': self._calculate_duration(workflow_result)
                }
            )
            
            return workflow_result
            
        except Exception as e:
            workflow_result['status'] = 'error'
            workflow_result['error'] = str(e)
            workflow_result['completed_at'] = datetime.utcnow().isoformat()
            
            # Publish workflow error event
            await self.event_service.publish_event(
                'WorkflowFailed',
                {
                    'workflow_id': workflow_id,
                    'error': str(e)
                }
            )
            
            return workflow_result
    
    async def _execute_step(self, step_config: Dict[str, Any]) -> Dict[str, Any]:
        """Execute individual workflow step"""
        step_name = step_config.get('name', 'unknown')
        service_name = step_config.get('service')
        
        step_result = {
            'step_name': step_name,
            'service_name': service_name,
            'started_at': datetime.utcnow().isoformat(),
            'success': False
        }
        
        try:
            if service_name in self.services:
                service_client = self.services[service_name]
                
                # Execute service call
                request_data = step_config.get('request', {})
                response = await service_client.call(request_data)
                
                step_result['response'] = response
                step_result['success'] = True
                
            else:
                raise Exception(f"Service {service_name} not found")
            
            step_result['completed_at'] = datetime.utcnow().isoformat()
            return step_result
            
        except Exception as e:
            step_result['error'] = str(e)
            step_result['completed_at'] = datetime.utcnow().isoformat()
            logging.error(f"Step {step_name} failed: {str(e)}")
            return step_result
    
    def _calculate_duration(self, workflow_result: Dict[str, Any]) -> int:
        """Calculate workflow duration in milliseconds"""
        try:
            start_time = datetime.fromisoformat(workflow_result['started_at'].replace('Z', '+00:00'))
            end_time = datetime.fromisoformat(workflow_result['completed_at'].replace('Z', '+00:00'))
            return int((end_time - start_time).total_seconds() * 1000)
        except:
            return 0
```

### Example 2: Loose Coupling Implementation Script
```bash
#!/bin/bash

# Loose Coupling Implementation Script
# This script implements loosely coupled architecture patterns

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="${SCRIPT_DIR}/loose-coupling-config.json"
LOG_FILE="${SCRIPT_DIR}/loose-coupling-implementation.log"
TEMP_DIR=$(mktemp -d)
RESULTS_DIR="${SCRIPT_DIR}/results"

# Create results directory
mkdir -p "$RESULTS_DIR"

# Logging function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Error handling
error_exit() {
    log "ERROR: $1"
    cleanup
    exit 1
}

# Cleanup function
cleanup() {
    rm -rf "$TEMP_DIR"
}

# Trap for cleanup
trap cleanup EXIT

# Load configuration
load_configuration() {
    if [[ ! -f "$CONFIG_FILE" ]]; then
        error_exit "Configuration file not found: $CONFIG_FILE"
    fi
    
    log "Loading loose coupling configuration from $CONFIG_FILE"
    
    # Validate JSON configuration
    if ! jq empty "$CONFIG_FILE" 2>/dev/null; then
        error_exit "Invalid JSON in configuration file"
    fi
    
    # Extract configuration values
    PROJECT_NAME=$(jq -r '.project_name // "loose-coupling-demo"' "$CONFIG_FILE")
    AWS_REGION=$(jq -r '.aws_region // "us-east-1"' "$CONFIG_FILE")
    DEPLOYMENT_STAGE=$(jq -r '.deployment_stage // "dev"' "$CONFIG_FILE")
    
    log "Configuration loaded successfully for project: $PROJECT_NAME"
}

# Create SQS queues for async communication
create_message_queues() {
    log "Creating SQS queues for asynchronous communication..."
    
    # Read queue configurations
    jq -c '.message_queues[]?' "$CONFIG_FILE" | while read -r queue_config; do
        QUEUE_NAME=$(echo "$queue_config" | jq -r '.name')
        VISIBILITY_TIMEOUT=$(echo "$queue_config" | jq -r '.visibility_timeout_seconds // 30')
        MESSAGE_RETENTION=$(echo "$queue_config" | jq -r '.message_retention_seconds // 1209600')
        
        log "Creating SQS queue: $QUEUE_NAME"
        
        # Create main queue
        QUEUE_URL=$(aws sqs create-queue \
            --region "$AWS_REGION" \
            --queue-name "$PROJECT_NAME-$QUEUE_NAME-$DEPLOYMENT_STAGE" \
            --attributes "{
                \"VisibilityTimeoutSeconds\": \"$VISIBILITY_TIMEOUT\",
                \"MessageRetentionPeriod\": \"$MESSAGE_RETENTION\",
                \"ReceiveMessageWaitTimeSeconds\": \"20\"
            }" \
            --query 'QueueUrl' \
            --output text)
        
        # Create dead letter queue
        DLQ_URL=$(aws sqs create-queue \
            --region "$AWS_REGION" \
            --queue-name "$PROJECT_NAME-$QUEUE_NAME-dlq-$DEPLOYMENT_STAGE" \
            --query 'QueueUrl' \
            --output text)
        
        # Get DLQ ARN
        DLQ_ARN=$(aws sqs get-queue-attributes \
            --region "$AWS_REGION" \
            --queue-url "$DLQ_URL" \
            --attribute-names QueueArn \
            --query 'Attributes.QueueArn' \
            --output text)
        
        # Configure redrive policy
        aws sqs set-queue-attributes \
            --region "$AWS_REGION" \
            --queue-url "$QUEUE_URL" \
            --attributes "{
                \"RedrivePolicy\": \"{\\\"deadLetterTargetArn\\\":\\\"$DLQ_ARN\\\",\\\"maxReceiveCount\\\":3}\"
            }"
        
        # Store queue information
        echo "{\"name\": \"$QUEUE_NAME\", \"url\": \"$QUEUE_URL\", \"dlq_url\": \"$DLQ_URL\"}" >> "$TEMP_DIR/created_queues.json"
        
        log "Created SQS queue: $QUEUE_NAME with DLQ"
    done
    
    # Combine all queue information
    if [[ -f "$TEMP_DIR/created_queues.json" ]]; then
        jq -s '.' "$TEMP_DIR/created_queues.json" > "$RESULTS_DIR/message_queues.json"
        QUEUE_COUNT=$(jq length "$RESULTS_DIR/message_queues.json")
        log "Created $QUEUE_COUNT message queues"
    fi
}

# Create SNS topics for pub/sub messaging
create_pub_sub_topics() {
    log "Creating SNS topics for publish-subscribe messaging..."
    
    echo "[]" > "$TEMP_DIR/created_topics.json"
    
    # Read topic configurations
    jq -c '.pub_sub_topics[]?' "$CONFIG_FILE" | while read -r topic_config; do
        TOPIC_NAME=$(echo "$topic_config" | jq -r '.name')
        
        log "Creating SNS topic: $TOPIC_NAME"
        
        # Create SNS topic
        TOPIC_ARN=$(aws sns create-topic \
            --region "$AWS_REGION" \
            --name "$PROJECT_NAME-$TOPIC_NAME-$DEPLOYMENT_STAGE" \
            --query 'TopicArn' \
            --output text)
        
        # Configure topic attributes
        aws sns set-topic-attributes \
            --region "$AWS_REGION" \
            --topic-arn "$TOPIC_ARN" \
            --attribute-name DisplayName \
            --attribute-value "$TOPIC_NAME Topic"
        
        # Store topic information
        TOPIC_INFO=$(cat << EOF
{
    "name": "$TOPIC_NAME",
    "arn": "$TOPIC_ARN"
}
EOF
)
        
        jq --argjson topic "$TOPIC_INFO" '. += [$topic]' "$TEMP_DIR/created_topics.json" > "$TEMP_DIR/created_topics_tmp.json"
        mv "$TEMP_DIR/created_topics_tmp.json" "$TEMP_DIR/created_topics.json"
        
        log "Created SNS topic: $TOPIC_NAME"
    done
    
    # Copy results
    cp "$TEMP_DIR/created_topics.json" "$RESULTS_DIR/pub_sub_topics.json"
    TOPIC_COUNT=$(jq length "$RESULTS_DIR/pub_sub_topics.json")
    log "Created $TOPIC_COUNT pub/sub topics"
}

# Create EventBridge custom bus
create_event_bus() {
    log "Creating EventBridge custom bus for event-driven communication..."
    
    EVENT_BUS_NAME="$PROJECT_NAME-events-$DEPLOYMENT_STAGE"
    
    # Create custom event bus
    aws events create-event-bus \
        --region "$AWS_REGION" \
        --name "$EVENT_BUS_NAME" \
        --tags Key=Project,Value="$PROJECT_NAME" Key=Stage,Value="$DEPLOYMENT_STAGE"
    
    # Create event rules for different event types
    jq -c '.event_rules[]?' "$CONFIG_FILE" | while read -r rule_config; do
        RULE_NAME=$(echo "$rule_config" | jq -r '.name')
        EVENT_PATTERN=$(echo "$rule_config" | jq -r '.event_pattern')
        
        log "Creating EventBridge rule: $RULE_NAME"
        
        # Create event rule
        aws events put-rule \
            --region "$AWS_REGION" \
            --name "$PROJECT_NAME-$RULE_NAME-$DEPLOYMENT_STAGE" \
            --event-pattern "$EVENT_PATTERN" \
            --event-bus-name "$EVENT_BUS_NAME" \
            --description "Event rule for $RULE_NAME"
        
        log "Created EventBridge rule: $RULE_NAME"
    done
    
    # Store event bus information
    EVENT_BUS_INFO=$(cat << EOF
{
    "name": "$EVENT_BUS_NAME",
    "arn": "arn:aws:events:$AWS_REGION:$(aws sts get-caller-identity --query Account --output text):event-bus/$EVENT_BUS_NAME"
}
EOF
)
    
    echo "$EVENT_BUS_INFO" > "$RESULTS_DIR/event_bus.json"
    
    log "Created EventBridge custom bus: $EVENT_BUS_NAME"
}

# Deploy circuit breaker Lambda function
deploy_circuit_breaker_function() {
    log "Deploying circuit breaker Lambda function..."
    
    FUNCTION_DIR="$TEMP_DIR/circuit_breaker_function"
    mkdir -p "$FUNCTION_DIR"
    
    # Create circuit breaker implementation
    cat << 'EOF' > "$FUNCTION_DIR/lambda_function.py"
import json
import boto3
import time
import logging
from typing import Dict, Any
from dataclasses import dataclass, asdict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class CircuitBreakerState:
    state: str  # CLOSED, OPEN, HALF_OPEN
    failure_count: int
    last_failure_time: float
    failure_threshold: int
    timeout_seconds: int
    half_open_max_calls: int
    half_open_calls: int

class CircuitBreakerManager:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.table_name = os.environ.get('CIRCUIT_BREAKER_TABLE', 'circuit-breaker-state')
        self.table = self.dynamodb.Table(self.table_name)
    
    def get_circuit_state(self, service_name: str) -> CircuitBreakerState:
        """Get current circuit breaker state"""
        try:
            response = self.table.get_item(Key={'service_name': service_name})
            
            if 'Item' in response:
                item = response['Item']
                return CircuitBreakerState(
                    state=item.get('state', 'CLOSED'),
                    failure_count=int(item.get('failure_count', 0)),
                    last_failure_time=float(item.get('last_failure_time', 0)),
                    failure_threshold=int(item.get('failure_threshold', 5)),
                    timeout_seconds=int(item.get('timeout_seconds', 60)),
                    half_open_max_calls=int(item.get('half_open_max_calls', 3)),
                    half_open_calls=int(item.get('half_open_calls', 0))
                )
            else:
                # Return default state for new service
                return CircuitBreakerState(
                    state='CLOSED',
                    failure_count=0,
                    last_failure_time=0,
                    failure_threshold=5,
                    timeout_seconds=60,
                    half_open_max_calls=3,
                    half_open_calls=0
                )
                
        except Exception as e:
            logger.error(f"Failed to get circuit state: {str(e)}")
            raise
    
    def update_circuit_state(self, service_name: str, state: CircuitBreakerState):
        """Update circuit breaker state"""
        try:
            self.table.put_item(
                Item={
                    'service_name': service_name,
                    **asdict(state),
                    'updated_at': time.time()
                }
            )
        except Exception as e:
            logger.error(f"Failed to update circuit state: {str(e)}")
            raise
    
    def should_allow_request(self, service_name: str) -> Dict[str, Any]:
        """Check if request should be allowed through circuit breaker"""
        state = self.get_circuit_state(service_name)
        current_time = time.time()
        
        if state.state == 'CLOSED':
            return {'allowed': True, 'reason': 'Circuit is closed'}
        
        elif state.state == 'OPEN':
            if current_time - state.last_failure_time >= state.timeout_seconds:
                # Transition to half-open
                state.state = 'HALF_OPEN'
                state.half_open_calls = 0
                self.update_circuit_state(service_name, state)
                return {'allowed': True, 'reason': 'Circuit transitioning to half-open'}
            else:
                return {'allowed': False, 'reason': 'Circuit is open'}
        
        elif state.state == 'HALF_OPEN':
            if state.half_open_calls < state.half_open_max_calls:
                state.half_open_calls += 1
                self.update_circuit_state(service_name, state)
                return {'allowed': True, 'reason': 'Circuit is half-open, allowing test call'}
            else:
                return {'allowed': False, 'reason': 'Circuit half-open limit exceeded'}
        
        return {'allowed': False, 'reason': 'Unknown circuit state'}
    
    def record_success(self, service_name: str):
        """Record successful call"""
        state = self.get_circuit_state(service_name)
        
        if state.state == 'HALF_OPEN':
            # Transition back to closed
            state.state = 'CLOSED'
            state.failure_count = 0
            state.half_open_calls = 0
        elif state.state == 'CLOSED':
            # Reset failure count on success
            state.failure_count = 0
        
        self.update_circuit_state(service_name, state)
    
    def record_failure(self, service_name: str):
        """Record failed call"""
        state = self.get_circuit_state(service_name)
        state.failure_count += 1
        state.last_failure_time = time.time()
        
        if state.failure_count >= state.failure_threshold:
            state.state = 'OPEN'
        
        self.update_circuit_state(service_name, state)

# Lambda handler
circuit_breaker_manager = CircuitBreakerManager()

def lambda_handler(event, context):
    """Lambda handler for circuit breaker operations"""
    try:
        action = event.get('action')
        service_name = event.get('service_name')
        
        if not service_name:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'service_name is required'})
            }
        
        if action == 'check':
            result = circuit_breaker_manager.should_allow_request(service_name)
            return {
                'statusCode': 200,
                'body': json.dumps(result)
            }
        
        elif action == 'success':
            circuit_breaker_manager.record_success(service_name)
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'Success recorded'})
            }
        
        elif action == 'failure':
            circuit_breaker_manager.record_failure(service_name)
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'Failure recorded'})
            }
        
        else:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Invalid action'})
            }
    
    except Exception as e:
        logger.error(f"Circuit breaker handler error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error'})
        }
EOF

    # Create deployment package
    cd "$FUNCTION_DIR"
    zip -r circuit_breaker_function.zip lambda_function.py
    
    # Deploy Lambda function
    FUNCTION_NAME="$PROJECT_NAME-circuit-breaker-$DEPLOYMENT_STAGE"
    
    aws lambda create-function \
        --region "$AWS_REGION" \
        --function-name "$FUNCTION_NAME" \
        --runtime python3.9 \
        --role "arn:aws:iam::$(aws sts get-caller-identity --query Account --output text):role/lambda-execution-role" \
        --handler lambda_function.lambda_handler \
        --zip-file fileb://circuit_breaker_function.zip \
        --timeout 30 \
        --environment Variables="{CIRCUIT_BREAKER_TABLE=$PROJECT_NAME-circuit-breaker-$DEPLOYMENT_STAGE}" \
        --tags Project="$PROJECT_NAME",Stage="$DEPLOYMENT_STAGE"
    
    # Store function information
    FUNCTION_INFO=$(cat << EOF
{
    "name": "$FUNCTION_NAME",
    "arn": "arn:aws:lambda:$AWS_REGION:$(aws sts get-caller-identity --query Account --output text):function:$FUNCTION_NAME"
}
EOF
)
    
    echo "$FUNCTION_INFO" > "$RESULTS_DIR/circuit_breaker_function.json"
    
    log "Deployed circuit breaker Lambda function: $FUNCTION_NAME"
}

# Create DynamoDB table for circuit breaker state
create_circuit_breaker_table() {
    log "Creating DynamoDB table for circuit breaker state..."
    
    TABLE_NAME="$PROJECT_NAME-circuit-breaker-$DEPLOYMENT_STAGE"
    
    # Create DynamoDB table
    aws dynamodb create-table \
        --region "$AWS_REGION" \
        --table-name "$TABLE_NAME" \
        --attribute-definitions AttributeName=service_name,AttributeType=S \
        --key-schema AttributeName=service_name,KeyType=HASH \
        --billing-mode PAY_PER_REQUEST \
        --tags Key=Project,Value="$PROJECT_NAME" Key=Stage,Value="$DEPLOYMENT_STAGE"
    
    # Wait for table to be active
    aws dynamodb wait table-exists --region "$AWS_REGION" --table-name "$TABLE_NAME"
    
    log "Created DynamoDB table for circuit breaker: $TABLE_NAME"
}

# Generate loose coupling documentation
generate_loose_coupling_documentation() {
    log "Generating loose coupling implementation documentation..."
    
    DOC_FILE="$RESULTS_DIR/loose_coupling_documentation.md"
    
    cat << EOF > "$DOC_FILE"
# Loose Coupling Implementation Documentation

Generated on: $(date)
Project: $PROJECT_NAME
Stage: $DEPLOYMENT_STAGE

## Overview

This document describes the loosely coupled architecture components implemented for the $PROJECT_NAME project.

## Message Queues

The following SQS queues have been created for asynchronous communication:

EOF
    
    # Add queue information
    if [[ -f "$RESULTS_DIR/message_queues.json" ]]; then
        jq -r '.[] | "- **\(.name)**: \(.url)"' "$RESULTS_DIR/message_queues.json" >> "$DOC_FILE"
    fi
    
    cat << EOF >> "$DOC_FILE"

## Pub/Sub Topics

The following SNS topics have been created for publish-subscribe messaging:

EOF
    
    # Add topic information
    if [[ -f "$RESULTS_DIR/pub_sub_topics.json" ]]; then
        jq -r '.[] | "- **\(.name)**: \(.arn)"' "$RESULTS_DIR/pub_sub_topics.json" >> "$DOC_FILE"
    fi
    
    cat << EOF >> "$DOC_FILE"

## Event-Driven Architecture

- **Event Bus**: $(jq -r '.name' "$RESULTS_DIR/event_bus.json" 2>/dev/null || echo "Not created")
- **Event Bus ARN**: $(jq -r '.arn' "$RESULTS_DIR/event_bus.json" 2>/dev/null || echo "Not available")

## Circuit Breaker

- **Function**: $(jq -r '.name' "$RESULTS_DIR/circuit_breaker_function.json" 2>/dev/null || echo "Not deployed")
- **Function ARN**: $(jq -r '.arn' "$RESULTS_DIR/circuit_breaker_function.json" 2>/dev/null || echo "Not available")

## Usage Examples

### Asynchronous Message Processing

\`\`\`python
import boto3

sqs = boto3.client('sqs')

# Send message to queue
sqs.send_message(
    QueueUrl='your-queue-url',
    MessageBody=json.dumps({
        'action': 'process_order',
        'order_id': '12345',
        'timestamp': datetime.utcnow().isoformat()
    })
)
\`\`\`

### Event Publishing

\`\`\`python
import boto3

eventbridge = boto3.client('events')

# Publish event
eventbridge.put_events(
    Entries=[
        {
            'Source': 'order-service',
            'DetailType': 'Order Created',
            'Detail': json.dumps({
                'order_id': '12345',
                'customer_id': '67890'
            }),
            'EventBusName': '$(jq -r '.name' "$RESULTS_DIR/event_bus.json" 2>/dev/null)'
        }
    ]
)
\`\`\`

### Circuit Breaker Usage

\`\`\`python
import boto3

lambda_client = boto3.client('lambda')

# Check if request should be allowed
response = lambda_client.invoke(
    FunctionName='$(jq -r '.name' "$RESULTS_DIR/circuit_breaker_function.json" 2>/dev/null)',
    Payload=json.dumps({
        'action': 'check',
        'service_name': 'external-api'
    })
)

result = json.loads(response['Payload'].read())
if result['allowed']:
    # Make service call
    pass
else:
    # Handle circuit breaker open
    pass
\`\`\`

## Best Practices

1. **Asynchronous Processing**: Use message queues for non-critical operations
2. **Event-Driven Design**: Publish events for state changes and business events
3. **Circuit Breakers**: Implement circuit breakers for external service calls
4. **Timeout Configuration**: Set appropriate timeouts for all service calls
5. **Retry Logic**: Implement exponential backoff for transient failures
6. **Dead Letter Queues**: Use DLQs for failed message processing
7. **Monitoring**: Monitor queue depths, event processing, and circuit breaker states

EOF
    
    log "Documentation generated: $DOC_FILE"
}

# Main execution
main() {
    log "Starting loose coupling implementation"
    
    # Check prerequisites
    if ! command -v aws &> /dev/null; then
        error_exit "AWS CLI not found. Please install AWS CLI."
    fi
    
    if ! command -v jq &> /dev/null; then
        error_exit "jq not found. Please install jq."
    fi
    
    if ! command -v zip &> /dev/null; then
        error_exit "zip not found. Please install zip."
    fi
    
    # Load configuration
    load_configuration
    
    # Execute implementation steps
    case "${1:-implement}" in
        "implement")
            create_message_queues
            create_pub_sub_topics
            create_event_bus
            create_circuit_breaker_table
            deploy_circuit_breaker_function
            generate_loose_coupling_documentation
            log "Loose coupling implementation completed successfully"
            ;;
        "queues")
            create_message_queues
            log "Message queues created successfully"
            ;;
        "events")
            create_event_bus
            log "Event bus created successfully"
            ;;
        "circuit-breaker")
            create_circuit_breaker_table
            deploy_circuit_breaker_function
            log "Circuit breaker deployed successfully"
            ;;
        *)
            echo "Usage: $0 {implement|queues|events|circuit-breaker}"
            echo "  implement      - Implement all loose coupling components (default)"
            echo "  queues         - Create message queues only"
            echo "  events         - Create event bus only"
            echo "  circuit-breaker - Deploy circuit breaker only"
            exit 1
            ;;
    esac
}

# Execute main function
main "$@"
```

## AWS Services Used

- **Amazon SQS**: Message queuing for asynchronous communication and temporal decoupling
- **Amazon SNS**: Publish-subscribe messaging for event-driven architectures
- **Amazon EventBridge**: Event routing and processing for loosely coupled event-driven systems
- **AWS Lambda**: Serverless functions for event processing and circuit breaker implementation
- **Amazon API Gateway**: API management with built-in throttling and circuit breaker patterns
- **AWS Step Functions**: Workflow orchestration with error handling and retry logic
- **Amazon DynamoDB**: NoSQL database for storing circuit breaker state and configuration
- **Amazon ElastiCache**: Caching layer for reducing direct dependencies on databases
- **AWS App Mesh**: Service mesh for managing service-to-service communication
- **Amazon CloudWatch**: Monitoring and alerting for loose coupling patterns and health
- **AWS X-Ray**: Distributed tracing for understanding service interactions and dependencies
- **Amazon Kinesis**: Real-time data streaming for event-driven architectures
- **AWS Systems Manager**: Parameter store for configuration management and service discovery
- **Amazon Route 53**: DNS-based service discovery and health checking
- **Elastic Load Balancing**: Load balancing with health checks and automatic failover
- **AWS Secrets Manager**: Secure credential management for service authentication

## Benefits

- **Improved Resilience**: Failures in one service don't cascade to dependent services
- **Independent Scalability**: Services can scale independently based on their specific load patterns
- **Faster Development**: Teams can develop and deploy services independently
- **Better Fault Isolation**: Issues are contained within service boundaries
- **Enhanced Maintainability**: Loose coupling makes systems easier to understand and modify
- **Technology Diversity**: Different services can use optimal technologies for their requirements
- **Improved Testing**: Services can be tested in isolation with mock dependencies
- **Better Performance**: Asynchronous patterns reduce blocking and improve throughput
- **Cost Optimization**: Resources can be allocated based on individual service needs
- **Operational Flexibility**: Services can be updated, replaced, or retired independently

## Related Resources

- [AWS Well-Architected Reliability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/)
- [Implement Loosely Coupled Dependencies](https://docs.aws.amazon.com/wellarchitected/latest/framework/rel_prevent_interaction_failure_loosely_coupled_system.html)
- [Amazon SQS User Guide](https://docs.aws.amazon.com/sqs/latest/dg/)
- [Amazon SNS User Guide](https://docs.aws.amazon.com/sns/latest/dg/)
- [Amazon EventBridge User Guide](https://docs.aws.amazon.com/eventbridge/latest/userguide/)
- [AWS Lambda Best Practices](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
- [Circuit Breaker Pattern](https://aws.amazon.com/builders-library/implementing-health-checks/)
- [Event-Driven Architecture](https://aws.amazon.com/event-driven-architecture/)
- [Asynchronous Messaging Patterns](https://aws.amazon.com/builders-library/avoiding-fallback-in-distributed-systems/)
- [AWS Step Functions User Guide](https://docs.aws.amazon.com/step-functions/latest/dg/)
- [AWS App Mesh User Guide](https://docs.aws.amazon.com/app-mesh/latest/userguide/)
- [Microservices Communication Patterns](https://aws.amazon.com/blogs/architecture/)
