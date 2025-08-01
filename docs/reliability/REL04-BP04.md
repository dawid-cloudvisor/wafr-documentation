---
title: REL04-BP04 - Make mutating operations idempotent
layout: default
parent: REL04 - How do you design interactions in a distributed system to prevent failures?
grand_parent: Reliability
nav_order: 4
---

# REL04-BP04: Make mutating operations idempotent

## Overview

Design all mutating operations to be idempotent, ensuring that performing the same operation multiple times produces the same result as performing it once. Idempotency is crucial for building reliable distributed systems that can handle network failures, timeouts, and retry scenarios without causing data corruption or inconsistent states.

## Implementation Steps

### 1. Design Idempotent API Operations
- Use idempotency keys for all mutating operations
- Implement proper HTTP methods (PUT for updates, POST with idempotency keys)
- Design operations to check current state before making changes
- Return consistent responses for repeated operations

### 2. Implement Idempotency Key Management
- Generate unique idempotency keys for each operation
- Store idempotency keys with operation results
- Implement key expiration and cleanup policies
- Handle key conflicts and validation

### 3. Design State-Aware Operations
- Check current resource state before applying changes
- Use conditional updates based on resource versions
- Implement compare-and-swap operations
- Design operations to be naturally idempotent

### 4. Implement Retry-Safe Patterns
- Design operations that can be safely retried
- Use exponential backoff with jitter for retries
- Implement circuit breakers for failing operations
- Handle partial failures gracefully

### 5. Establish Data Consistency Patterns
- Use optimistic locking for concurrent updates
- Implement event sourcing for audit trails
- Design compensating transactions for rollbacks
- Use distributed locks when necessary

### 6. Monitor and Validate Idempotency
- Track duplicate operations and their handling
- Monitor idempotency key usage patterns
- Validate operation outcomes for consistency
- Implement automated testing for idempotency

## Implementation Examples

### Example 1: Idempotent Operations Framework
```python
import boto3
import json
import hashlib
import time
import logging
from typing import Dict, Any, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime, timedelta
import uuid

class OperationType(Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    PROCESS = "process"

@dataclass
class IdempotencyRecord:
    idempotency_key: str
    operation_type: OperationType
    resource_id: str
    request_hash: str
    response_data: Dict[str, Any]
    status: str
    created_at: str
    expires_at: str

class IdempotentOperationManager:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.dynamodb = boto3.resource('dynamodb')
        self.table_name = config.get('idempotency_table', 'idempotency-records')
        self.table = self.dynamodb.Table(self.table_name)
        self.ttl_hours = config.get('ttl_hours', 24)
        
    def generate_idempotency_key(self, operation_data: Dict[str, Any]) -> str:
        """Generate idempotency key from operation data"""
        # Create deterministic key from operation data
        key_data = {
            'operation_type': operation_data.get('operation_type'),
            'resource_id': operation_data.get('resource_id'),
            'user_id': operation_data.get('user_id'),
            'timestamp': operation_data.get('timestamp', '').split('T')[0]  # Date only
        }
        
        key_string = json.dumps(key_data, sort_keys=True)
        return hashlib.sha256(key_string.encode()).hexdigest()[:32]
    
    async def execute_idempotent_operation(self, 
                                         idempotency_key: str,
                                         operation_func: Callable,
                                         operation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute operation with idempotency protection"""
        try:
            # Check if operation already exists
            existing_record = await self._get_idempotency_record(idempotency_key)
            
            if existing_record:
                if existing_record['status'] == 'completed':
                    logging.info(f"Returning cached result for idempotency key: {idempotency_key}")
                    return existing_record['response_data']
                elif existing_record['status'] == 'in_progress':
                    # Operation is still in progress, wait and retry
                    await self._wait_for_completion(idempotency_key)
                    return await self.execute_idempotent_operation(idempotency_key, operation_func, operation_data)
            
            # Create new idempotency record
            request_hash = self._calculate_request_hash(operation_data)
            await self._create_idempotency_record(idempotency_key, operation_data, request_hash)
            
            try:
                # Execute the operation
                result = await operation_func(operation_data)
                
                # Update record with success
                await self._update_idempotency_record(idempotency_key, result, 'completed')
                
                return result
                
            except Exception as e:
                # Update record with failure
                await self._update_idempotency_record(
                    idempotency_key, 
                    {'error': str(e)}, 
                    'failed'
                )
                raise
                
        except Exception as e:
            logging.error(f"Idempotent operation failed: {str(e)}")
            raise
    
    async def _get_idempotency_record(self, idempotency_key: str) -> Optional[Dict[str, Any]]:
        """Get existing idempotency record"""
        try:
            response = self.table.get_item(Key={'idempotency_key': idempotency_key})
            return response.get('Item')
        except Exception as e:
            logging.error(f"Failed to get idempotency record: {str(e)}")
            return None
    
    async def _create_idempotency_record(self, idempotency_key: str, 
                                       operation_data: Dict[str, Any], 
                                       request_hash: str):
        """Create new idempotency record"""
        try:
            expires_at = int((datetime.utcnow() + timedelta(hours=self.ttl_hours)).timestamp())
            
            record = IdempotencyRecord(
                idempotency_key=idempotency_key,
                operation_type=OperationType(operation_data.get('operation_type', 'process')),
                resource_id=operation_data.get('resource_id', ''),
                request_hash=request_hash,
                response_data={},
                status='in_progress',
                created_at=datetime.utcnow().isoformat(),
                expires_at=str(expires_at)
            )
            
            self.table.put_item(
                Item=asdict(record),
                ConditionExpression='attribute_not_exists(idempotency_key)'
            )
            
        except Exception as e:
            if 'ConditionalCheckFailedException' in str(e):
                # Record already exists, this is expected in concurrent scenarios
                pass
            else:
                logging.error(f"Failed to create idempotency record: {str(e)}")
                raise
    
    def _calculate_request_hash(self, operation_data: Dict[str, Any]) -> str:
        """Calculate hash of request data for validation"""
        # Remove timestamp and other non-deterministic fields
        hashable_data = {k: v for k, v in operation_data.items() 
                        if k not in ['timestamp', 'request_id']}
        
        data_string = json.dumps(hashable_data, sort_keys=True)
        return hashlib.sha256(data_string.encode()).hexdigest()

class IdempotentResourceManager:
    """Manager for idempotent resource operations"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.dynamodb = boto3.resource('dynamodb')
        self.idempotency_manager = IdempotentOperationManager(config)
        
        # Resource table
        self.resource_table_name = config.get('resource_table', 'resources')
        self.resource_table = self.dynamodb.Table(self.resource_table_name)
    
    async def create_resource(self, resource_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create resource idempotently"""
        idempotency_key = self.idempotency_manager.generate_idempotency_key({
            'operation_type': 'create',
            'resource_type': resource_data.get('resource_type'),
            'user_id': resource_data.get('user_id'),
            'unique_identifier': resource_data.get('name') or resource_data.get('email')
        })
        
        return await self.idempotency_manager.execute_idempotent_operation(
            idempotency_key,
            self._create_resource_impl,
            resource_data
        )
    
    async def _create_resource_impl(self, resource_data: Dict[str, Any]) -> Dict[str, Any]:
        """Implementation of resource creation"""
        try:
            # Check if resource already exists
            existing_resource = await self._find_existing_resource(resource_data)
            if existing_resource:
                logging.info("Resource already exists, returning existing resource")
                return existing_resource
            
            # Create new resource
            resource_id = str(uuid.uuid4())
            resource = {
                'resource_id': resource_id,
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat(),
                'version': 1,
                **resource_data
            }
            
            # Store resource
            self.resource_table.put_item(Item=resource)
            
            logging.info(f"Created new resource: {resource_id}")
            return resource
            
        except Exception as e:
            logging.error(f"Resource creation failed: {str(e)}")
            raise
    
    async def update_resource(self, resource_id: str, 
                            updates: Dict[str, Any], 
                            expected_version: Optional[int] = None) -> Dict[str, Any]:
        """Update resource idempotently with optimistic locking"""
        idempotency_key = self.idempotency_manager.generate_idempotency_key({
            'operation_type': 'update',
            'resource_id': resource_id,
            'updates_hash': hashlib.sha256(json.dumps(updates, sort_keys=True).encode()).hexdigest()[:16],
            'user_id': updates.get('updated_by')
        })
        
        operation_data = {
            'operation_type': 'update',
            'resource_id': resource_id,
            'updates': updates,
            'expected_version': expected_version
        }
        
        return await self.idempotency_manager.execute_idempotent_operation(
            idempotency_key,
            self._update_resource_impl,
            operation_data
        )
    
    async def _update_resource_impl(self, operation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Implementation of resource update with optimistic locking"""
        try:
            resource_id = operation_data['resource_id']
            updates = operation_data['updates']
            expected_version = operation_data.get('expected_version')
            
            # Get current resource
            response = self.resource_table.get_item(Key={'resource_id': resource_id})
            if 'Item' not in response:
                raise ValueError(f"Resource {resource_id} not found")
            
            current_resource = response['Item']
            current_version = int(current_resource.get('version', 1))
            
            # Check version if provided
            if expected_version is not None and current_version != expected_version:
                raise ValueError(f"Version mismatch: expected {expected_version}, got {current_version}")
            
            # Prepare update
            new_version = current_version + 1
            updated_resource = {
                **current_resource,
                **updates,
                'updated_at': datetime.utcnow().isoformat(),
                'version': new_version
            }
            
            # Conditional update
            try:
                self.resource_table.put_item(
                    Item=updated_resource,
                    ConditionExpression='version = :expected_version',
                    ExpressionAttributeValues={':expected_version': current_version}
                )
            except Exception as e:
                if 'ConditionalCheckFailedException' in str(e):
                    raise ValueError("Resource was modified by another operation")
                raise
            
            logging.info(f"Updated resource {resource_id} to version {new_version}")
            return updated_resource
            
        except Exception as e:
            logging.error(f"Resource update failed: {str(e)}")
            raise
    
    async def delete_resource(self, resource_id: str) -> Dict[str, Any]:
        """Delete resource idempotently"""
        idempotency_key = self.idempotency_manager.generate_idempotency_key({
            'operation_type': 'delete',
            'resource_id': resource_id
        })
        
        return await self.idempotency_manager.execute_idempotent_operation(
            idempotency_key,
            self._delete_resource_impl,
            {'resource_id': resource_id}
        )
    
    async def _delete_resource_impl(self, operation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Implementation of resource deletion"""
        try:
            resource_id = operation_data['resource_id']
            
            # Check if resource exists
            response = self.resource_table.get_item(Key={'resource_id': resource_id})
            if 'Item' not in response:
                # Resource doesn't exist, deletion is idempotent
                logging.info(f"Resource {resource_id} already deleted or never existed")
                return {'resource_id': resource_id, 'status': 'deleted'}
            
            # Delete resource
            self.resource_table.delete_item(Key={'resource_id': resource_id})
            
            logging.info(f"Deleted resource: {resource_id}")
            return {'resource_id': resource_id, 'status': 'deleted'}
            
        except Exception as e:
            logging.error(f"Resource deletion failed: {str(e)}")
            raise

# Usage example
async def main():
    config = {
        'idempotency_table': 'idempotency-records',
        'resource_table': 'resources',
        'ttl_hours': 24
    }
    
    resource_manager = IdempotentResourceManager(config)
    
    # Create resource idempotently
    resource_data = {
        'resource_type': 'user',
        'name': 'John Doe',
        'email': 'john@example.com',
        'user_id': 'user123'
    }
    
    result = await resource_manager.create_resource(resource_data)
    print(f"Created resource: {result['resource_id']}")
    
    # Update resource idempotently
    updates = {
        'name': 'John Smith',
        'updated_by': 'admin'
    }
    
    updated_result = await resource_manager.update_resource(
        result['resource_id'], 
        updates, 
        expected_version=1
    )
    print(f"Updated resource to version: {updated_result['version']}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## AWS Services Used

- **Amazon DynamoDB**: NoSQL database with conditional writes for idempotency record storage
- **AWS Lambda**: Serverless functions with built-in retry mechanisms and idempotent processing
- **Amazon API Gateway**: API management with idempotency key support and request deduplication
- **Amazon SQS**: Message queuing with message deduplication for idempotent message processing
- **AWS Step Functions**: Workflow orchestration with idempotent state transitions
- **Amazon EventBridge**: Event processing with idempotent event handling
- **Amazon S3**: Object storage with conditional puts and versioning for idempotent uploads
- **Amazon RDS**: Relational database with transaction support for idempotent operations
- **AWS Systems Manager**: Parameter store for idempotency configuration management
- **Amazon CloudWatch**: Monitoring and logging for tracking idempotent operation patterns
- **AWS X-Ray**: Distributed tracing for monitoring idempotent operation flows
- **Amazon Kinesis**: Stream processing with idempotent record processing
- **AWS Batch**: Batch processing with job deduplication and idempotent execution
- **Amazon ElastiCache**: Caching layer for storing idempotency keys and operation results
- **AWS Secrets Manager**: Secure storage of idempotency keys and operation tokens

## Benefits

- **Reliable Retries**: Operations can be safely retried without causing duplicate effects
- **Consistent State**: System state remains consistent even with network failures and timeouts
- **Simplified Error Handling**: Retry logic becomes simpler when operations are idempotent
- **Better User Experience**: Users can safely retry failed operations without fear of duplication
- **Reduced Data Corruption**: Idempotent operations prevent data inconsistencies
- **Improved System Reliability**: Systems become more resilient to transient failures
- **Easier Testing**: Idempotent operations are easier to test and validate
- **Better Concurrency Handling**: Multiple concurrent operations produce predictable results
- **Simplified Integration**: External systems can safely retry operations
- **Enhanced Monitoring**: Easier to track and audit operation outcomes

## Related Resources

- [AWS Well-Architected Reliability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/)
- [Make Mutating Operations Idempotent](https://docs.aws.amazon.com/wellarchitected/latest/framework/rel_prevent_interaction_failure_idempotent.html)
- [Amazon DynamoDB Conditional Writes](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/WorkingWithItems.html#WorkingWithItems.ConditionalUpdate)
- [API Gateway Idempotency](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-idempotency.html)
- [AWS Lambda Idempotency](https://docs.aws.amazon.com/lambda/latest/dg/invocation-retries.html)
- [Amazon SQS Message Deduplication](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/FIFO-queues-exactly-once-processing.html)
- [Idempotency Patterns](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)
- [Optimistic Locking](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBMapper.OptimisticLocking.html)
- [AWS Step Functions Idempotency](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-read-consistency.html)
- [Event Sourcing Patterns](https://aws.amazon.com/blogs/compute/building-event-sourcing-applications-with-amazon-msk-and-amazon-kinesis-data-streams/)
- [Amazon S3 Conditional Operations](https://docs.aws.amazon.com/AmazonS3/latest/userguide/conditional-requests.html)
- [Building Resilient Systems](https://aws.amazon.com/builders-library/)
