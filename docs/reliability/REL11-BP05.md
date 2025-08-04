---
title: REL11-BP05 - Use static stability to prevent bimodal behavior
layout: default
parent: REL11 - How do you design your workload to withstand component failures?
nav_order: 5
---

# REL11-BP05: Use static stability to prevent bimodal behavior

Static stability ensures your system behaves consistently regardless of the state of its dependencies. Avoid architectures that behave differently during normal operations versus failure scenarios. Design systems that can continue operating with cached data, default configurations, or degraded functionality when dependencies are unavailable.

## Implementation Steps

### 1. Identify Dependencies
Map all external dependencies and their impact on system behavior.

### 2. Design Fallback Mechanisms
Implement fallback strategies that maintain consistent behavior during dependency failures.

### 3. Cache Critical Data
Store essential data locally to avoid dependency on external services.

### 4. Use Default Configurations
Define safe default values that allow continued operation.

### 5. Implement Graceful Degradation
Design systems to reduce functionality rather than fail completely.

## Detailed Implementation

{% raw %}
```python
import boto3
import json
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import threading
import sqlite3
import redis
from functools import wraps
import hashlib

class DependencyState(Enum):
    AVAILABLE = "available"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"
    UNKNOWN = "unknown"

class FallbackStrategy(Enum):
    CACHED_DATA = "cached_data"
    DEFAULT_VALUE = "default_value"
    DEGRADED_FUNCTION = "degraded_function"
    SKIP_OPERATION = "skip_operation"
    STATIC_RESPONSE = "static_response"

class OperationMode(Enum):
    NORMAL = "normal"
    DEGRADED = "degraded"
    EMERGENCY = "emergency"

@dataclass
class Dependency:
    name: str
    service_type: str
    endpoint: str
    timeout: int
    retry_count: int
    fallback_strategy: FallbackStrategy
    fallback_data: Any
    health_check_interval: int
    circuit_breaker_threshold: int

@dataclass
class StaticStabilityConfig:
    service_name: str
    dependencies: List[Dependency]
    default_operation_mode: OperationMode
    cache_ttl: int
    health_check_enabled: bool
    graceful_degradation_enabled: bool

class StaticStabilitySystem:
    def __init__(self, config: StaticStabilityConfig):
        self.config = config
        self.service_name = config.service_name
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Dependency state tracking
        self.dependency_states: Dict[str, DependencyState] = {}
        self.circuit_breakers: Dict[str, Dict[str, Any]] = {}
        self.fallback_cache: Dict[str, Any] = {}
        
        # Operation mode
        self.current_mode = config.default_operation_mode
        self.mode_lock = threading.Lock()
        
        # Initialize local cache
        self.local_cache = {}
        self.cache_lock = threading.Lock()
        
        # Initialize Redis for distributed caching (optional)
        try:
            self.redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
            self.redis_available = True
        except:
            self.redis_client = None
            self.redis_available = False
            self.logger.warning("Redis not available, using local cache only")
        
        # Initialize dependencies
        self._initialize_dependencies()
        
        # Start health monitoring
        if config.health_check_enabled:
            self._start_health_monitoring()

    def _initialize_dependencies(self) -> None:
        """Initialize dependency tracking and circuit breakers"""
        try:
            for dependency in self.config.dependencies:
                # Initialize dependency state
                self.dependency_states[dependency.name] = DependencyState.UNKNOWN
                
                # Initialize circuit breaker
                self.circuit_breakers[dependency.name] = {
                    'failure_count': 0,
                    'last_failure_time': None,
                    'state': 'closed',  # closed, open, half-open
                    'threshold': dependency.circuit_breaker_threshold,
                    'timeout': 60  # seconds before trying half-open
                }
                
                # Initialize fallback cache
                if dependency.fallback_strategy == FallbackStrategy.CACHED_DATA:
                    self.fallback_cache[dependency.name] = dependency.fallback_data
            
            self.logger.info(f"Initialized {len(self.config.dependencies)} dependencies")
            
        except Exception as e:
            self.logger.error(f"Dependency initialization failed: {str(e)}")

    def static_stability_decorator(self, dependency_name: str, fallback_strategy: FallbackStrategy = None):
        """Decorator to add static stability to functions"""
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    # Check dependency state
                    dependency_state = self.dependency_states.get(dependency_name, DependencyState.UNKNOWN)
                    
                    # Check circuit breaker
                    if self._is_circuit_breaker_open(dependency_name):
                        return self._execute_fallback(dependency_name, func.__name__, args, kwargs, fallback_strategy)
                    
                    # Execute function with timeout
                    dependency = self._get_dependency(dependency_name)
                    if dependency:
                        result = self._execute_with_timeout(func, dependency.timeout, *args, **kwargs)
                        
                        # Update circuit breaker on success
                        self._record_success(dependency_name)
                        
                        # Cache successful result
                        self._cache_result(dependency_name, func.__name__, result, args, kwargs)
                        
                        return result
                    else:
                        return func(*args, **kwargs)
                        
                except Exception as e:
                    # Record failure
                    self._record_failure(dependency_name)
                    
                    # Execute fallback
                    return self._execute_fallback(dependency_name, func.__name__, args, kwargs, fallback_strategy)
            
            return wrapper
        return decorator

    def get_cached_data(self, cache_key: str, default_value: Any = None) -> Any:
        """Get data from cache with static stability"""
        try:
            # Try Redis first if available
            if self.redis_available:
                try:
                    cached_data = self.redis_client.get(cache_key)
                    if cached_data:
                        return json.loads(cached_data)
                except Exception as e:
                    self.logger.warning(f"Redis cache access failed: {str(e)}")
            
            # Fall back to local cache
            with self.cache_lock:
                cached_data = self.local_cache.get(cache_key)
                if cached_data:
                    # Check if cache is still valid
                    if cached_data.get('expires_at', 0) > time.time():
                        return cached_data['data']
            
            # Return default value if no cache available
            return default_value
            
        except Exception as e:
            self.logger.error(f"Cache access failed: {str(e)}")
            return default_value

    def set_cached_data(self, cache_key: str, data: Any, ttl: int = None) -> bool:
        """Set data in cache with static stability"""
        try:
            ttl = ttl or self.config.cache_ttl
            expires_at = time.time() + ttl
            
            cache_entry = {
                'data': data,
                'expires_at': expires_at,
                'created_at': time.time()
            }
            
            # Try Redis first if available
            if self.redis_available:
                try:
                    self.redis_client.setex(cache_key, ttl, json.dumps(data))
                except Exception as e:
                    self.logger.warning(f"Redis cache write failed: {str(e)}")
            
            # Always update local cache as fallback
            with self.cache_lock:
                self.local_cache[cache_key] = cache_entry
            
            return True
            
        except Exception as e:
            self.logger.error(f"Cache write failed: {str(e)}")
            return False

    def call_external_service(self, service_name: str, operation: str, **kwargs) -> Any:
        """Call external service with static stability"""
        try:
            dependency = self._get_dependency(service_name)
            if not dependency:
                raise ValueError(f"Unknown dependency: {service_name}")
            
            # Check circuit breaker
            if self._is_circuit_breaker_open(service_name):
                return self._execute_service_fallback(dependency, operation, **kwargs)
            
            # Check dependency state
            dependency_state = self.dependency_states.get(service_name, DependencyState.UNKNOWN)
            
            if dependency_state == DependencyState.UNAVAILABLE:
                return self._execute_service_fallback(dependency, operation, **kwargs)
            
            # Attempt service call
            try:
                result = self._make_service_call(dependency, operation, **kwargs)
                
                # Record success
                self._record_success(service_name)
                self.dependency_states[service_name] = DependencyState.AVAILABLE
                
                # Cache result
                cache_key = self._generate_cache_key(service_name, operation, **kwargs)
                self.set_cached_data(cache_key, result)
                
                return result
                
            except Exception as e:
                # Record failure
                self._record_failure(service_name)
                self.dependency_states[service_name] = DependencyState.UNAVAILABLE
                
                # Execute fallback
                return self._execute_service_fallback(dependency, operation, **kwargs)
                
        except Exception as e:
            self.logger.error(f"External service call failed: {str(e)}")
            return self._get_default_response(service_name, operation)

    def get_configuration(self, config_key: str, default_value: Any = None) -> Any:
        """Get configuration with static stability"""
        try:
            # Try to get from external configuration service
            config_dependency = self._get_dependency('configuration_service')
            
            if config_dependency and not self._is_circuit_breaker_open('configuration_service'):
                try:
                    config_value = self._fetch_configuration(config_key)
                    if config_value is not None:
                        # Cache the configuration
                        cache_key = f"config:{config_key}"
                        self.set_cached_data(cache_key, config_value, ttl=3600)
                        return config_value
                except Exception as e:
                    self.logger.warning(f"Configuration fetch failed: {str(e)}")
            
            # Fall back to cached configuration
            cache_key = f"config:{config_key}"
            cached_config = self.get_cached_data(cache_key)
            if cached_config is not None:
                return cached_config
            
            # Fall back to default value
            return default_value
            
        except Exception as e:
            self.logger.error(f"Configuration retrieval failed: {str(e)}")
            return default_value

    def execute_business_logic(self, operation: str, **kwargs) -> Dict[str, Any]:
        """Execute business logic with static stability"""
        try:
            result = {
                'success': False,
                'data': None,
                'mode': self.current_mode.value,
                'degraded_features': []
            }
            
            # Determine operation mode based on dependency states
            operation_mode = self._determine_operation_mode()
            
            if operation_mode == OperationMode.NORMAL:
                # Execute full functionality
                result['data'] = self._execute_normal_operation(operation, **kwargs)
                result['success'] = True
                
            elif operation_mode == OperationMode.DEGRADED:
                # Execute with reduced functionality
                result['data'] = self._execute_degraded_operation(operation, **kwargs)
                result['success'] = True
                result['degraded_features'] = self._get_degraded_features()
                
            elif operation_mode == OperationMode.EMERGENCY:
                # Execute minimal functionality
                result['data'] = self._execute_emergency_operation(operation, **kwargs)
                result['success'] = True
                result['degraded_features'] = ['all_non_essential_features']
            
            return result
            
        except Exception as e:
            self.logger.error(f"Business logic execution failed: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'mode': self.current_mode.value,
                'data': self._get_default_response('business_logic', operation)
            }

    def _execute_fallback(self, dependency_name: str, function_name: str, args: tuple, 
                         kwargs: dict, fallback_strategy: FallbackStrategy = None) -> Any:
        """Execute fallback strategy"""
        try:
            dependency = self._get_dependency(dependency_name)
            if not dependency:
                return None
            
            strategy = fallback_strategy or dependency.fallback_strategy
            
            if strategy == FallbackStrategy.CACHED_DATA:
                cache_key = self._generate_cache_key(dependency_name, function_name, *args, **kwargs)
                return self.get_cached_data(cache_key, dependency.fallback_data)
                
            elif strategy == FallbackStrategy.DEFAULT_VALUE:
                return dependency.fallback_data
                
            elif strategy == FallbackStrategy.DEGRADED_FUNCTION:
                return self._execute_degraded_function(dependency_name, function_name, args, kwargs)
                
            elif strategy == FallbackStrategy.SKIP_OPERATION:
                self.logger.info(f"Skipping operation {function_name} for dependency {dependency_name}")
                return None
                
            elif strategy == FallbackStrategy.STATIC_RESPONSE:
                return dependency.fallback_data
            
            return None
            
        except Exception as e:
            self.logger.error(f"Fallback execution failed: {str(e)}")
            return None

    def _determine_operation_mode(self) -> OperationMode:
        """Determine current operation mode based on dependency states"""
        try:
            available_count = 0
            total_count = len(self.config.dependencies)
            
            for dependency_name, state in self.dependency_states.items():
                if state == DependencyState.AVAILABLE:
                    available_count += 1
            
            if total_count == 0:
                return OperationMode.NORMAL
            
            availability_ratio = available_count / total_count
            
            if availability_ratio >= 0.8:
                return OperationMode.NORMAL
            elif availability_ratio >= 0.5:
                return OperationMode.DEGRADED
            else:
                return OperationMode.EMERGENCY
                
        except Exception as e:
            self.logger.error(f"Operation mode determination failed: {str(e)}")
            return OperationMode.EMERGENCY

    def _execute_normal_operation(self, operation: str, **kwargs) -> Any:
        """Execute operation in normal mode"""
        try:
            # Full functionality available
            if operation == 'user_authentication':
                return self._authenticate_user_full(**kwargs)
            elif operation == 'data_processing':
                return self._process_data_full(**kwargs)
            elif operation == 'recommendation_engine':
                return self._generate_recommendations_full(**kwargs)
            else:
                return {'status': 'completed', 'mode': 'normal'}
                
        except Exception as e:
            self.logger.error(f"Normal operation failed: {str(e)}")
            raise

    def _execute_degraded_operation(self, operation: str, **kwargs) -> Any:
        """Execute operation in degraded mode"""
        try:
            # Reduced functionality
            if operation == 'user_authentication':
                return self._authenticate_user_cached(**kwargs)
            elif operation == 'data_processing':
                return self._process_data_basic(**kwargs)
            elif operation == 'recommendation_engine':
                return self._generate_recommendations_cached(**kwargs)
            else:
                return {'status': 'completed', 'mode': 'degraded'}
                
        except Exception as e:
            self.logger.error(f"Degraded operation failed: {str(e)}")
            raise

    def _execute_emergency_operation(self, operation: str, **kwargs) -> Any:
        """Execute operation in emergency mode"""
        try:
            # Minimal functionality
            if operation == 'user_authentication':
                return self._authenticate_user_basic(**kwargs)
            elif operation == 'data_processing':
                return self._process_data_minimal(**kwargs)
            elif operation == 'recommendation_engine':
                return self._generate_recommendations_default(**kwargs)
            else:
                return {'status': 'completed', 'mode': 'emergency'}
                
        except Exception as e:
            self.logger.error(f"Emergency operation failed: {str(e)}")
            return {'status': 'failed', 'mode': 'emergency'}

    def _authenticate_user_full(self, **kwargs) -> Dict[str, Any]:
        """Full user authentication with all features"""
        user_id = kwargs.get('user_id')
        
        # Call external authentication service
        auth_result = self.call_external_service('auth_service', 'authenticate', user_id=user_id)
        
        # Get user profile
        profile = self.call_external_service('profile_service', 'get_profile', user_id=user_id)
        
        # Get permissions
        permissions = self.call_external_service('permission_service', 'get_permissions', user_id=user_id)
        
        return {
            'authenticated': auth_result.get('valid', False),
            'user_profile': profile,
            'permissions': permissions,
            'features_available': ['all']
        }

    def _authenticate_user_cached(self, **kwargs) -> Dict[str, Any]:
        """Degraded user authentication using cached data"""
        user_id = kwargs.get('user_id')
        
        # Try cached authentication
        cache_key = f"auth:{user_id}"
        cached_auth = self.get_cached_data(cache_key)
        
        if cached_auth:
            return {
                'authenticated': True,
                'user_profile': cached_auth.get('profile', {}),
                'permissions': cached_auth.get('permissions', ['basic']),
                'features_available': ['basic'],
                'note': 'Using cached authentication data'
            }
        
        return {
            'authenticated': False,
            'error': 'Authentication service unavailable and no cached data',
            'features_available': ['guest']
        }

    def _authenticate_user_basic(self, **kwargs) -> Dict[str, Any]:
        """Basic user authentication with minimal features"""
        return {
            'authenticated': True,
            'user_profile': {'id': kwargs.get('user_id'), 'name': 'Guest User'},
            'permissions': ['read'],
            'features_available': ['basic_read_only'],
            'note': 'Emergency mode - basic access only'
        }

    def _is_circuit_breaker_open(self, dependency_name: str) -> bool:
        """Check if circuit breaker is open for dependency"""
        try:
            cb = self.circuit_breakers.get(dependency_name, {})
            
            if cb.get('state') == 'open':
                # Check if timeout has passed for half-open attempt
                if cb.get('last_failure_time'):
                    time_since_failure = time.time() - cb['last_failure_time']
                    if time_since_failure > cb.get('timeout', 60):
                        cb['state'] = 'half-open'
                        return False
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Circuit breaker check failed: {str(e)}")
            return False

    def _record_success(self, dependency_name: str) -> None:
        """Record successful dependency call"""
        try:
            cb = self.circuit_breakers.get(dependency_name, {})
            cb['failure_count'] = 0
            cb['state'] = 'closed'
            cb['last_failure_time'] = None
            
        except Exception as e:
            self.logger.error(f"Success recording failed: {str(e)}")

    def _record_failure(self, dependency_name: str) -> None:
        """Record failed dependency call"""
        try:
            cb = self.circuit_breakers.get(dependency_name, {})
            cb['failure_count'] = cb.get('failure_count', 0) + 1
            cb['last_failure_time'] = time.time()
            
            if cb['failure_count'] >= cb.get('threshold', 5):
                cb['state'] = 'open'
                self.logger.warning(f"Circuit breaker opened for {dependency_name}")
            
        except Exception as e:
            self.logger.error(f"Failure recording failed: {str(e)}")

    def _get_dependency(self, name: str) -> Optional[Dependency]:
        """Get dependency configuration by name"""
        for dependency in self.config.dependencies:
            if dependency.name == name:
                return dependency
        return None

    def _generate_cache_key(self, *args, **kwargs) -> str:
        """Generate cache key from arguments"""
        key_data = f"{args}:{sorted(kwargs.items())}"
        return hashlib.md5(key_data.encode()).hexdigest()

    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status"""
        try:
            status = {
                'service_name': self.service_name,
                'current_mode': self.current_mode.value,
                'dependencies': {},
                'circuit_breakers': {},
                'cache_stats': {
                    'local_cache_size': len(self.local_cache),
                    'redis_available': self.redis_available
                }
            }
            
            # Dependency states
            for name, state in self.dependency_states.items():
                status['dependencies'][name] = state.value
            
            # Circuit breaker states
            for name, cb in self.circuit_breakers.items():
                status['circuit_breakers'][name] = {
                    'state': cb.get('state', 'unknown'),
                    'failure_count': cb.get('failure_count', 0)
                }
            
            return status
            
        except Exception as e:
            self.logger.error(f"Status retrieval failed: {str(e)}")
            return {'error': str(e)}

# Example usage
def main():
    # Define dependencies
    dependencies = [
        Dependency(
            name='auth_service',
            service_type='http',
            endpoint='https://auth.example.com',
            timeout=5,
            retry_count=2,
            fallback_strategy=FallbackStrategy.CACHED_DATA,
            fallback_data={'authenticated': False, 'permissions': ['guest']},
            health_check_interval=30,
            circuit_breaker_threshold=5
        ),
        Dependency(
            name='profile_service',
            service_type='http',
            endpoint='https://profile.example.com',
            timeout=3,
            retry_count=1,
            fallback_strategy=FallbackStrategy.DEFAULT_VALUE,
            fallback_data={'name': 'Guest User', 'preferences': {}},
            health_check_interval=60,
            circuit_breaker_threshold=3
        )
    ]
    
    # Create configuration
    config = StaticStabilityConfig(
        service_name='user_service',
        dependencies=dependencies,
        default_operation_mode=OperationMode.NORMAL,
        cache_ttl=300,
        health_check_enabled=True,
        graceful_degradation_enabled=True
    )
    
    # Initialize static stability system
    stability_system = StaticStabilitySystem(config)
    
    print("Static stability system initialized")
    
    # Example usage with decorator
    @stability_system.static_stability_decorator('auth_service')
    def authenticate_user(user_id: str) -> Dict[str, Any]:
        # This would normally call external auth service
        return {'user_id': user_id, 'authenticated': True}
    
    # Test authentication
    result = authenticate_user('user123')
    print(f"Authentication result: {result}")
    
    # Test business logic execution
    business_result = stability_system.execute_business_logic('user_authentication', user_id='user123')
    print(f"Business logic result: {json.dumps(business_result, indent=2)}")
    
    # Get system status
    status = stability_system.get_system_status()
    print(f"System status: {json.dumps(status, indent=2)}")

if __name__ == "__main__":
    main()
```
{% endraw %}

## AWS Services

### Primary Services
- **Amazon ElastiCache**: Distributed caching for consistent data access
- **Amazon DynamoDB**: NoSQL database with consistent performance
- **AWS Lambda**: Stateless compute with built-in fault tolerance
- **Amazon S3**: Highly available object storage for static content

### Supporting Services
- **Amazon CloudWatch**: Monitoring without dependency on external services
- **AWS Systems Manager Parameter Store**: Configuration management with caching
- **Amazon SQS**: Asynchronous messaging with built-in redundancy
- **AWS App Config**: Feature flag management with local caching

## Benefits

- **Consistent Behavior**: System operates predictably regardless of dependency state
- **Reduced Cascading Failures**: Prevents dependency failures from causing system-wide outages
- **Improved User Experience**: Graceful degradation maintains core functionality
- **Operational Simplicity**: Eliminates bimodal behavior that complicates troubleshooting
- **Higher Availability**: System remains operational even when dependencies fail

## Related Resources

- [AWS Well-Architected Framework - Reliability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/)
- [Amazon ElastiCache User Guide](https://docs.aws.amazon.com/elasticache/)
- [Amazon DynamoDB Developer Guide](https://docs.aws.amazon.com/dynamodb/)
- [AWS Systems Manager Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html)
