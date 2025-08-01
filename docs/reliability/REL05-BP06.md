---
title: REL05-BP06 - Make systems stateless where possible
layout: default
parent: REL05 - How do you design interactions in a distributed system to mitigate or withstand failures?
grand_parent: Reliability
nav_order: 6
---

# REL05-BP06: Make systems stateless where possible

## Overview

Design systems to be stateless wherever possible to improve scalability, reliability, and maintainability. Stateless systems can handle failures more gracefully, scale horizontally with ease, and simplify deployment and recovery processes by eliminating the need to maintain and synchronize state across instances.

## Implementation Steps

### 1. Externalize State Storage
- Move session state to external stores like databases or caches
- Use distributed caches for temporary state management
- Implement stateless authentication using tokens
- Store application state in managed services rather than local memory

### 2. Design Stateless Service Interfaces
- Create APIs that don't rely on server-side session state
- Pass all necessary context in requests rather than maintaining it server-side
- Implement idempotent operations that don't depend on previous calls
- Design self-contained request/response patterns

### 3. Implement Stateless Authentication and Authorization
- Use JWT tokens or similar stateless authentication mechanisms
- Implement token-based authorization that doesn't require server-side sessions
- Design API keys and OAuth flows that work without server state
- Create stateless user context passing between services

### 4. Configure Stateless Data Processing
- Design data processing pipelines that don't maintain state between requests
- Implement functional programming patterns for data transformation
- Use event-driven architectures for stateless event processing
- Create batch processing jobs that can restart from any point

### 5. Establish Stateless Deployment Patterns
- Design applications that can start without requiring previous state
- Implement blue-green deployments enabled by stateless architecture
- Create auto-scaling groups that can add/remove instances freely
- Design disaster recovery that doesn't require state synchronization

### 6. Monitor and Optimize Stateless Operations
- Track the effectiveness of stateless design patterns
- Monitor external state store performance and availability
- Implement caching strategies to optimize stateless operations
- Create metrics for stateless service scalability and reliability

## Implementation Examples

### Example 1: Stateless Web Application Framework
```python
import jwt
import redis
import json
import time
import logging
from typing import Dict, Optional, Any
from dataclasses import dataclass, asdict
from flask import Flask, request, jsonify
import boto3
from functools import wraps

@dataclass
class UserContext:
    user_id: str
    username: str
    roles: list
    permissions: list
    session_id: str
    expires_at: float

class StatelessAuthManager:
    """Stateless authentication using JWT tokens"""
    
    def __init__(self, config: Dict[str, Any]):
        self.secret_key = config.get('jwt_secret_key', 'your-secret-key')
        self.token_expiry_hours = config.get('token_expiry_hours', 24)
        self.algorithm = config.get('jwt_algorithm', 'HS256')
        
        # External state storage
        self.redis_client = redis.Redis(
            host=config.get('redis_host', 'localhost'),
            port=config.get('redis_port', 6379),
            decode_responses=True
        )
        
        # AWS clients for external services
        self.dynamodb = boto3.resource('dynamodb')
        self.user_table = self.dynamodb.Table(config.get('user_table', 'users'))
    
    def create_token(self, user_context: UserContext) -> str:
        """Create stateless JWT token"""
        payload = {
            'user_id': user_context.user_id,
            'username': user_context.username,
            'roles': user_context.roles,
            'permissions': user_context.permissions,
            'session_id': user_context.session_id,
            'iat': time.time(),
            'exp': time.time() + (self.token_expiry_hours * 3600)
        }
        
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        
        # Store minimal session info in external cache for revocation
        self.redis_client.setex(
            f"session:{user_context.session_id}",
            self.token_expiry_hours * 3600,
            json.dumps({'user_id': user_context.user_id, 'active': True})
        )
        
        return token
    
    def validate_token(self, token: str) -> Optional[UserContext]:
        """Validate stateless JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            
            # Check if session is still active (for revocation support)
            session_data = self.redis_client.get(f"session:{payload['session_id']}")
            if not session_data:
                logging.warning(f"Session {payload['session_id']} not found or expired")
                return None
            
            session_info = json.loads(session_data)
            if not session_info.get('active', False):
                logging.warning(f"Session {payload['session_id']} is inactive")
                return None
            
            return UserContext(
                user_id=payload['user_id'],
                username=payload['username'],
                roles=payload['roles'],
                permissions=payload['permissions'],
                session_id=payload['session_id'],
                expires_at=payload['exp']
            )
            
        except jwt.ExpiredSignatureError:
            logging.warning("Token has expired")
            return None
        except jwt.InvalidTokenError as e:
            logging.warning(f"Invalid token: {str(e)}")
            return None
    
    def revoke_session(self, session_id: str):
        """Revoke session (mark as inactive)"""
        session_data = self.redis_client.get(f"session:{session_id}")
        if session_data:
            session_info = json.loads(session_data)
            session_info['active'] = False
            
            # Update with remaining TTL
            ttl = self.redis_client.ttl(f"session:{session_id}")
            if ttl > 0:
                self.redis_client.setex(
                    f"session:{session_id}",
                    ttl,
                    json.dumps(session_info)
                )

class StatelessDataProcessor:
    """Stateless data processing service"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
        # External storage for processing state
        self.s3 = boto3.client('s3')
        self.dynamodb = boto3.resource('dynamodb')
        
        self.processing_bucket = config.get('processing_bucket', 'data-processing')
        self.results_table = self.dynamodb.Table(config.get('results_table', 'processing-results'))
    
    async def process_data(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process data in a stateless manner"""
        processing_id = request_data.get('processing_id')
        data_source = request_data.get('data_source')
        processing_config = request_data.get('config', {})
        
        try:
            # Load data from external source (stateless)
            input_data = await self._load_data(data_source)
            
            # Process data (pure function, no state)
            processed_data = await self._transform_data(input_data, processing_config)
            
            # Store results externally
            result_location = await self._store_results(processing_id, processed_data)
            
            # Record processing metadata
            await self._record_processing_metadata(processing_id, {
                'status': 'completed',
                'result_location': result_location,
                'processed_at': time.time(),
                'input_size': len(input_data) if isinstance(input_data, list) else 0,
                'output_size': len(processed_data) if isinstance(processed_data, list) else 0
            })
            
            return {
                'success': True,
                'processing_id': processing_id,
                'result_location': result_location,
                'metadata': {
                    'processed_records': len(processed_data) if isinstance(processed_data, list) else 0,
                    'processing_time_ms': 0  # Would be calculated in real implementation
                }
            }
            
        except Exception as e:
            logging.error(f"Data processing failed for {processing_id}: {str(e)}")
            
            # Record failure metadata
            await self._record_processing_metadata(processing_id, {
                'status': 'failed',
                'error': str(e),
                'failed_at': time.time()
            })
            
            return {
                'success': False,
                'processing_id': processing_id,
                'error': str(e)
            }
    
    async def _load_data(self, data_source: str) -> Any:
        """Load data from external source"""
        if data_source.startswith('s3://'):
            # Load from S3
            bucket, key = data_source.replace('s3://', '').split('/', 1)
            response = self.s3.get_object(Bucket=bucket, Key=key)
            return json.loads(response['Body'].read())
        else:
            # Simulate loading from other sources
            return [{'id': i, 'value': f'data_{i}'} for i in range(100)]
    
    async def _transform_data(self, input_data: Any, config: Dict[str, Any]) -> Any:
        """Transform data (pure function, stateless)"""
        # Example transformation - filter and map
        if isinstance(input_data, list):
            # Apply filters
            filtered_data = input_data
            if 'filter_condition' in config:
                # Apply filter logic here
                pass
            
            # Apply transformations
            transformed_data = []
            for item in filtered_data:
                transformed_item = {
                    **item,
                    'processed': True,
                    'processed_at': time.time()
                }
                
                # Apply custom transformations from config
                for transform in config.get('transformations', []):
                    # Apply transformation logic here
                    pass
                
                transformed_data.append(transformed_item)
            
            return transformed_data
        
        return input_data
    
    async def _store_results(self, processing_id: str, processed_data: Any) -> str:
        """Store processing results externally"""
        result_key = f"results/{processing_id}/output.json"
        
        self.s3.put_object(
            Bucket=self.processing_bucket,
            Key=result_key,
            Body=json.dumps(processed_data, default=str),
            ContentType='application/json'
        )
        
        return f"s3://{self.processing_bucket}/{result_key}"
    
    async def _record_processing_metadata(self, processing_id: str, metadata: Dict[str, Any]):
        """Record processing metadata in external store"""
        self.results_table.put_item(
            Item={
                'processing_id': processing_id,
                'timestamp': int(time.time()),
                **metadata
            }
        )

class StatelessWebApplication:
    """Stateless web application using Flask"""
    
    def __init__(self, config: Dict[str, Any]):
        self.app = Flask(__name__)
        self.auth_manager = StatelessAuthManager(config.get('auth_config', {}))
        self.data_processor = StatelessDataProcessor(config.get('processor_config', {}))
        
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup stateless API routes"""
        
        @self.app.route('/api/login', methods=['POST'])
        def login():
            """Stateless login endpoint"""
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
            
            # Validate credentials (would use external service)
            if self._validate_credentials(username, password):
                # Create user context
                user_context = UserContext(
                    user_id=f"user_{username}",
                    username=username,
                    roles=['user'],
                    permissions=['read', 'write'],
                    session_id=f"session_{int(time.time())}_{username}",
                    expires_at=time.time() + 24 * 3600
                )
                
                # Create stateless token
                token = self.auth_manager.create_token(user_context)
                
                return jsonify({
                    'success': True,
                    'token': token,
                    'expires_at': user_context.expires_at
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'Invalid credentials'
                }), 401
        
        @self.app.route('/api/process', methods=['POST'])
        @self._require_auth
        def process_data():
            """Stateless data processing endpoint"""
            data = request.get_json()
            
            # All context is passed in the request
            processing_request = {
                'processing_id': data.get('processing_id', f"proc_{int(time.time())}"),
                'data_source': data.get('data_source'),
                'config': data.get('config', {}),
                'user_context': request.user_context  # Added by auth decorator
            }
            
            # Process data statelessly
            import asyncio
            result = asyncio.run(self.data_processor.process_data(processing_request))
            
            return jsonify(result)
        
        @self.app.route('/api/status/<processing_id>', methods=['GET'])
        @self._require_auth
        def get_processing_status(processing_id):
            """Get processing status (stateless)"""
            try:
                # Query external store for status
                response = self.data_processor.results_table.get_item(
                    Key={'processing_id': processing_id}
                )
                
                if 'Item' in response:
                    return jsonify({
                        'success': True,
                        'processing_id': processing_id,
                        'status': response['Item']
                    })
                else:
                    return jsonify({
                        'success': False,
                        'error': 'Processing ID not found'
                    }), 404
                    
            except Exception as e:
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
    
    def _require_auth(self, f):
        """Decorator for stateless authentication"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            
            if not auth_header or not auth_header.startswith('Bearer '):
                return jsonify({'error': 'Missing or invalid authorization header'}), 401
            
            token = auth_header.split(' ')[1]
            user_context = self.auth_manager.validate_token(token)
            
            if not user_context:
                return jsonify({'error': 'Invalid or expired token'}), 401
            
            # Add user context to request (but don't store it server-side)
            request.user_context = user_context
            
            return f(*args, **kwargs)
        
        return decorated_function
    
    def _validate_credentials(self, username: str, password: str) -> bool:
        """Validate user credentials (would use external service)"""
        # In real implementation, this would query external user store
        return username == 'testuser' and password == 'testpass'
    
    def run(self, host='0.0.0.0', port=5000, debug=False):
        """Run the stateless web application"""
        self.app.run(host=host, port=port, debug=debug)

# Usage example
def main():
    config = {
        'auth_config': {
            'jwt_secret_key': 'your-secret-key-here',
            'token_expiry_hours': 24,
            'redis_host': 'localhost',
            'redis_port': 6379,
            'user_table': 'users'
        },
        'processor_config': {
            'processing_bucket': 'my-processing-bucket',
            'results_table': 'processing-results'
        }
    }
    
    # Create and run stateless web application
    app = StatelessWebApplication(config)
    
    print("Starting stateless web application...")
    print("Example requests:")
    print("POST /api/login - {'username': 'testuser', 'password': 'testpass'}")
    print("POST /api/process - {'data_source': 'test', 'config': {}} (requires auth)")
    print("GET /api/status/<processing_id> (requires auth)")
    
    app.run(debug=True)

if __name__ == "__main__":
    main()
```

## AWS Services Used

- **AWS Lambda**: Inherently stateless serverless compute platform
- **Amazon API Gateway**: Stateless API management and routing
- **Amazon DynamoDB**: External state storage for stateless applications
- **Amazon ElastiCache (Redis)**: Session and temporary state storage
- **Amazon S3**: Object storage for application state and data
- **AWS Systems Manager Parameter Store**: Configuration management for stateless apps
- **Amazon CloudFront**: Stateless content delivery and caching
- **Elastic Load Balancing**: Load balancing across stateless instances
- **AWS Auto Scaling**: Automatic scaling of stateless application instances
- **Amazon ECS/EKS**: Container orchestration for stateless services
- **AWS Fargate**: Serverless container platform for stateless workloads
- **Amazon SQS**: Message queuing for stateless event processing
- **Amazon EventBridge**: Event-driven architecture for stateless services
- **AWS Step Functions**: Stateless workflow orchestration
- **Amazon CloudWatch**: Monitoring stateless application metrics

## Benefits

- **Improved Scalability**: Easy horizontal scaling without state synchronization concerns
- **Enhanced Reliability**: Failure of individual instances doesn't affect overall system state
- **Simplified Deployment**: Blue-green deployments and rolling updates without state migration
- **Better Disaster Recovery**: Quick recovery without complex state restoration procedures
- **Reduced Complexity**: Eliminates need for state synchronization and session management
- **Cost Optimization**: Efficient resource utilization through auto-scaling
- **Improved Performance**: No state-related bottlenecks or memory leaks
- **Enhanced Security**: Reduced attack surface through elimination of server-side sessions
- **Better Testing**: Easier unit and integration testing without state dependencies
- **Operational Simplicity**: Simplified monitoring, debugging, and maintenance

## Related Resources

- [AWS Well-Architected Reliability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/)
- [Make Systems Stateless](https://docs.aws.amazon.com/wellarchitected/latest/framework/rel_mitigate_interaction_failure_stateless.html)
- [AWS Lambda Best Practices](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
- [Amazon API Gateway Best Practices](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-basic-concept.html)
- [Stateless Authentication with JWT](https://jwt.io/introduction/)
- [Amazon DynamoDB Best Practices](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html)
- [Amazon ElastiCache for Redis](https://docs.aws.amazon.com/elasticache/latest/red-ug/)
- [AWS Auto Scaling](https://docs.aws.amazon.com/autoscaling/latest/userguide/)
- [Twelve-Factor App Methodology](https://12factor.net/)
- [Microservices Patterns](https://microservices.io/patterns/data/database-per-service.html)
- [Amazon ECS Best Practices](https://docs.aws.amazon.com/AmazonECS/latest/bestpracticesguide/)
- [Building Resilient Systems](https://aws.amazon.com/builders-library/)
