---
title: REL11-BP04 - Rely on the data plane and not the control plane during recovery
layout: default
parent: Reliability
nav_order: 114
---

# REL11-BP04: Rely on the data plane and not the control plane during recovery

During widespread failures, control plane APIs may become unavailable or throttled. Design recovery mechanisms that depend on data plane operations rather than control plane operations. Use pre-provisioned resources, cached configurations, and avoid making API calls during critical recovery paths.

## Implementation Steps

### 1. Pre-Provision Recovery Resources
Deploy standby resources in advance rather than creating them during recovery.

### 2. Cache Configuration Data
Store critical configuration data locally to avoid dependency on external APIs.

### 3. Use Data Plane Operations
Design recovery logic to use data plane operations that remain available during control plane issues.

### 4. Implement Static Routing
Configure static routing and failover paths that don't require API calls.

### 5. Local Decision Making
Enable components to make recovery decisions based on local information.

## Detailed Implementation

{% raw %}
```python
import boto3
import json
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import threading
import sqlite3
import pickle
import os

class PlaneType(Enum):
    CONTROL_PLANE = "control_plane"
    DATA_PLANE = "data_plane"

class RecoveryStrategy(Enum):
    PRE_PROVISIONED = "pre_provisioned"
    CACHED_CONFIG = "cached_config"
    LOCAL_DECISION = "local_decision"
    STATIC_ROUTING = "static_routing"

class ResourceState(Enum):
    ACTIVE = "active"
    STANDBY = "standby"
    FAILED = "failed"
    RECOVERING = "recovering"

@dataclass
class PreProvisionedResource:
    resource_id: str
    resource_type: str
    region: str
    availability_zone: str
    state: ResourceState
    configuration: Dict[str, Any]
    last_health_check: datetime
    activation_trigger: str

@dataclass
class CachedConfiguration:
    config_id: str
    config_type: str
    data: Dict[str, Any]
    last_updated: datetime
    ttl: int
    source: str

class DataPlaneRecoverySystem:
    def __init__(self, region: str = 'us-east-1'):
        self.region = region
        
        # Initialize AWS clients (used only for setup, not recovery)
        self.ec2 = boto3.client('ec2', region_name=region)
        self.elb = boto3.client('elbv2', region_name=region)
        self.route53 = boto3.client('route53')
        self.s3 = boto3.client('s3', region_name=region)
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Local storage for configurations and state
        self.config_cache_file = '/tmp/recovery_config_cache.db'
        self.resource_state_file = '/tmp/resource_state.json'
        self.init_local_storage()
        
        # Pre-provisioned resources tracking
        self.pre_provisioned_resources: Dict[str, PreProvisionedResource] = {}
        self.cached_configurations: Dict[str, CachedConfiguration] = {}
        
        # Recovery state
        self.recovery_lock = threading.Lock()
        self.control_plane_available = True

    def init_local_storage(self) -> None:
        """Initialize local storage for configurations"""
        try:
            # Create SQLite database for configuration cache
            conn = sqlite3.connect(self.config_cache_file)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS config_cache (
                    config_id TEXT PRIMARY KEY,
                    config_type TEXT,
                    data TEXT,
                    last_updated TEXT,
                    ttl INTEGER,
                    source TEXT
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS resource_state (
                    resource_id TEXT PRIMARY KEY,
                    resource_type TEXT,
                    region TEXT,
                    availability_zone TEXT,
                    state TEXT,
                    configuration TEXT,
                    last_health_check TEXT,
                    activation_trigger TEXT
                )
            ''')
            
            conn.commit()
            conn.close()
            
            self.logger.info("Local storage initialized")
            
        except Exception as e:
            self.logger.error(f"Local storage initialization failed: {str(e)}")

    def setup_pre_provisioned_resources(self, resource_configs: List[Dict[str, Any]]) -> List[PreProvisionedResource]:
        """Set up pre-provisioned standby resources"""
        pre_provisioned = []
        
        try:
            for config in resource_configs:
                resource_type = config['resource_type']
                
                if resource_type == 'ec2_instance':
                    resource = self._provision_standby_ec2(config)
                elif resource_type == 'load_balancer':
                    resource = self._provision_standby_lb(config)
                elif resource_type == 'database':
                    resource = self._provision_standby_db(config)
                elif resource_type == 'lambda_function':
                    resource = self._provision_standby_lambda(config)
                else:
                    continue
                
                if resource:
                    pre_provisioned.append(resource)
                    self.pre_provisioned_resources[resource.resource_id] = resource
                    self._store_resource_state(resource)
            
            self.logger.info(f"Pre-provisioned {len(pre_provisioned)} standby resources")
            return pre_provisioned
            
        except Exception as e:
            self.logger.error(f"Pre-provisioning setup failed: {str(e)}")
            return pre_provisioned

    def cache_critical_configurations(self, config_sources: List[Dict[str, Any]]) -> List[CachedConfiguration]:
        """Cache critical configurations locally"""
        cached_configs = []
        
        try:
            for source in config_sources:
                config_type = source['config_type']
                
                if config_type == 'route53_records':
                    configs = self._cache_route53_configs(source)
                elif config_type == 'security_groups':
                    configs = self._cache_security_group_configs(source)
                elif config_type == 'load_balancer_targets':
                    configs = self._cache_lb_target_configs(source)
                elif config_type == 'application_config':
                    configs = self._cache_application_configs(source)
                else:
                    continue
                
                cached_configs.extend(configs)
                
                # Store in local cache
                for config in configs:
                    self.cached_configurations[config.config_id] = config
                    self._store_cached_config(config)
            
            self.logger.info(f"Cached {len(cached_configs)} critical configurations")
            return cached_configs
            
        except Exception as e:
            self.logger.error(f"Configuration caching failed: {str(e)}")
            return cached_configs

    def setup_data_plane_recovery(self, recovery_config: Dict[str, Any]) -> Dict[str, Any]:
        """Set up data plane recovery mechanisms"""
        try:
            recovery_setup = {
                'static_routes': [],
                'health_check_endpoints': [],
                'failover_targets': [],
                'local_decision_rules': []
            }
            
            # Configure static routing
            for route_config in recovery_config.get('static_routes', []):
                static_route = self._setup_static_route(route_config)
                recovery_setup['static_routes'].append(static_route)
            
            # Set up health check endpoints
            for hc_config in recovery_config.get('health_checks', []):
                health_endpoint = self._setup_health_check_endpoint(hc_config)
                recovery_setup['health_check_endpoints'].append(health_endpoint)
            
            # Configure failover targets
            for failover_config in recovery_config.get('failover_targets', []):
                failover_target = self._setup_failover_target(failover_config)
                recovery_setup['failover_targets'].append(failover_target)
            
            # Set up local decision rules
            for rule_config in recovery_config.get('decision_rules', []):
                decision_rule = self._setup_local_decision_rule(rule_config)
                recovery_setup['local_decision_rules'].append(decision_rule)
            
            self.logger.info("Data plane recovery setup completed")
            return recovery_setup
            
        except Exception as e:
            self.logger.error(f"Data plane recovery setup failed: {str(e)}")
            return {}

    def execute_data_plane_recovery(self, failure_scenario: Dict[str, Any]) -> Dict[str, Any]:
        """Execute recovery using only data plane operations"""
        recovery_result = {
            'success': False,
            'actions_taken': [],
            'resources_activated': [],
            'errors': []
        }
        
        try:
            with self.recovery_lock:
                self.logger.info(f"Executing data plane recovery for scenario: {failure_scenario['type']}")
                
                # Check control plane availability
                self.control_plane_available = self._check_control_plane_availability()
                
                if not self.control_plane_available:
                    self.logger.warning("Control plane unavailable, using data plane recovery only")
                
                # Load cached configurations
                cached_configs = self._load_cached_configurations()
                
                # Load pre-provisioned resource states
                pre_provisioned = self._load_resource_states()
                
                # Execute recovery based on failure type
                failure_type = failure_scenario['type']
                
                if failure_type == 'instance_failure':
                    success = self._recover_from_instance_failure(failure_scenario, cached_configs, pre_provisioned)
                elif failure_type == 'availability_zone_failure':
                    success = self._recover_from_az_failure(failure_scenario, cached_configs, pre_provisioned)
                elif failure_type == 'region_failure':
                    success = self._recover_from_region_failure(failure_scenario, cached_configs, pre_provisioned)
                elif failure_type == 'service_failure':
                    success = self._recover_from_service_failure(failure_scenario, cached_configs, pre_provisioned)
                else:
                    success = False
                    recovery_result['errors'].append(f"Unknown failure type: {failure_type}")
                
                recovery_result['success'] = success
                
                self.logger.info(f"Data plane recovery completed: {success}")
                return recovery_result
                
        except Exception as e:
            recovery_result['errors'].append(str(e))
            self.logger.error(f"Data plane recovery failed: {str(e)}")
            return recovery_result

    def _provision_standby_ec2(self, config: Dict[str, Any]) -> Optional[PreProvisionedResource]:
        """Provision standby EC2 instance"""
        try:
            # Launch instance in standby state
            response = self.ec2.run_instances(
                ImageId=config['ami_id'],
                MinCount=1,
                MaxCount=1,
                InstanceType=config['instance_type'],
                KeyName=config.get('key_name'),
                SecurityGroupIds=config['security_groups'],
                SubnetId=config['subnet_id'],
                UserData=config.get('user_data', ''),
                TagSpecifications=[
                    {
                        'ResourceType': 'instance',
                        'Tags': [
                            {'Key': 'Purpose', 'Value': 'StandbyRecovery'},
                            {'Key': 'Environment', 'Value': config.get('environment', 'production')},
                            {'Key': 'AutoActivate', 'Value': 'true'}
                        ]
                    }
                ]
            )
            
            instance_id = response['Instances'][0]['InstanceId']
            
            # Stop instance to save costs (will be started during recovery)
            self.ec2.stop_instances(InstanceIds=[instance_id])
            
            resource = PreProvisionedResource(
                resource_id=instance_id,
                resource_type='ec2_instance',
                region=self.region,
                availability_zone=config['availability_zone'],
                state=ResourceState.STANDBY,
                configuration=config,
                last_health_check=datetime.utcnow(),
                activation_trigger=config.get('activation_trigger', 'instance_failure')
            )
            
            self.logger.info(f"Provisioned standby EC2 instance: {instance_id}")
            return resource
            
        except Exception as e:
            self.logger.error(f"Standby EC2 provisioning failed: {str(e)}")
            return None

    def _cache_route53_configs(self, source: Dict[str, Any]) -> List[CachedConfiguration]:
        """Cache Route 53 DNS configurations"""
        configs = []
        
        try:
            hosted_zone_id = source['hosted_zone_id']
            
            # Get all records in the hosted zone
            response = self.route53.list_resource_record_sets(
                HostedZoneId=hosted_zone_id
            )
            
            for record_set in response['ResourceRecordSets']:
                config = CachedConfiguration(
                    config_id=f"route53-{hosted_zone_id}-{record_set['Name']}-{record_set['Type']}",
                    config_type='route53_record',
                    data={
                        'hosted_zone_id': hosted_zone_id,
                        'name': record_set['Name'],
                        'type': record_set['Type'],
                        'ttl': record_set.get('TTL', 300),
                        'resource_records': record_set.get('ResourceRecords', []),
                        'alias_target': record_set.get('AliasTarget'),
                        'failover': record_set.get('Failover'),
                        'set_identifier': record_set.get('SetIdentifier'),
                        'health_check_id': record_set.get('HealthCheckId')
                    },
                    last_updated=datetime.utcnow(),
                    ttl=source.get('cache_ttl', 3600),
                    source='route53_api'
                )
                configs.append(config)
            
            return configs
            
        except Exception as e:
            self.logger.error(f"Route 53 config caching failed: {str(e)}")
            return configs

    def _recover_from_instance_failure(self, failure_scenario: Dict[str, Any], 
                                     cached_configs: Dict[str, CachedConfiguration],
                                     pre_provisioned: Dict[str, PreProvisionedResource]) -> bool:
        """Recover from instance failure using data plane operations"""
        try:
            failed_instance_id = failure_scenario['resource_id']
            
            # Find suitable standby instance
            standby_instance = None
            for resource in pre_provisioned.values():
                if (resource.resource_type == 'ec2_instance' and 
                    resource.state == ResourceState.STANDBY and
                    resource.activation_trigger in ['instance_failure', 'any']):
                    standby_instance = resource
                    break
            
            if not standby_instance:
                self.logger.error("No suitable standby instance found")
                return False
            
            # Activate standby instance (data plane operation)
            if not self.control_plane_available:
                # Use pre-configured activation script
                activation_success = self._activate_instance_via_userdata(standby_instance)
            else:
                # Use EC2 API if available
                activation_success = self._activate_instance_via_api(standby_instance)
            
            if not activation_success:
                return False
            
            # Update load balancer targets using cached configuration
            lb_update_success = self._update_lb_targets_from_cache(
                failed_instance_id, 
                standby_instance.resource_id, 
                cached_configs
            )
            
            # Update DNS records using cached configuration
            dns_update_success = self._update_dns_from_cache(
                failed_instance_id,
                standby_instance.resource_id,
                cached_configs
            )
            
            # Update resource state
            standby_instance.state = ResourceState.ACTIVE
            self._store_resource_state(standby_instance)
            
            self.logger.info(f"Instance recovery completed: {standby_instance.resource_id}")
            return activation_success and lb_update_success and dns_update_success
            
        except Exception as e:
            self.logger.error(f"Instance failure recovery failed: {str(e)}")
            return False

    def _activate_instance_via_userdata(self, resource: PreProvisionedResource) -> bool:
        """Activate instance using pre-configured user data script"""
        try:
            # This would typically involve sending a signal to the instance
            # via a pre-configured mechanism (e.g., SQS queue, file system trigger)
            
            # For demonstration, we'll simulate the activation
            activation_script = resource.configuration.get('activation_script', '')
            
            if activation_script:
                # In a real implementation, this would trigger the instance
                # to start itself and begin serving traffic
                self.logger.info(f"Triggering instance activation: {resource.resource_id}")
                
                # Simulate activation delay
                time.sleep(5)
                
                # Update resource state
                resource.state = ResourceState.ACTIVE
                resource.last_health_check = datetime.utcnow()
                
                return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Instance activation via userdata failed: {str(e)}")
            return False

    def _update_lb_targets_from_cache(self, failed_instance: str, new_instance: str, 
                                    cached_configs: Dict[str, CachedConfiguration]) -> bool:
        """Update load balancer targets using cached configuration"""
        try:
            # Find load balancer configurations that include the failed instance
            for config_id, config in cached_configs.items():
                if config.config_type == 'load_balancer_targets':
                    targets = config.data.get('targets', [])
                    
                    # Check if failed instance is in targets
                    if any(target.get('id') == failed_instance for target in targets):
                        # Update targets to replace failed instance with new instance
                        updated_targets = []
                        for target in targets:
                            if target.get('id') == failed_instance:
                                target['id'] = new_instance
                            updated_targets.append(target)
                        
                        # Apply the update (this would be a data plane operation)
                        success = self._apply_lb_target_update(config.data['target_group_arn'], updated_targets)
                        
                        if success:
                            # Update cached configuration
                            config.data['targets'] = updated_targets
                            config.last_updated = datetime.utcnow()
                            self._store_cached_config(config)
                            
                            self.logger.info(f"Updated load balancer targets: {failed_instance} -> {new_instance}")
                            return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Load balancer target update failed: {str(e)}")
            return False

    def _check_control_plane_availability(self) -> bool:
        """Check if AWS control plane is available"""
        try:
            # Simple check - try to describe regions
            self.ec2.describe_regions()
            return True
        except Exception:
            return False

    def _load_cached_configurations(self) -> Dict[str, CachedConfiguration]:
        """Load configurations from local cache"""
        configs = {}
        
        try:
            conn = sqlite3.connect(self.config_cache_file)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM config_cache')
            rows = cursor.fetchall()
            
            for row in rows:
                config = CachedConfiguration(
                    config_id=row[0],
                    config_type=row[1],
                    data=json.loads(row[2]),
                    last_updated=datetime.fromisoformat(row[3]),
                    ttl=row[4],
                    source=row[5]
                )
                configs[config.config_id] = config
            
            conn.close()
            return configs
            
        except Exception as e:
            self.logger.error(f"Failed to load cached configurations: {str(e)}")
            return configs

    def _store_cached_config(self, config: CachedConfiguration) -> None:
        """Store configuration in local cache"""
        try:
            conn = sqlite3.connect(self.config_cache_file)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO config_cache 
                (config_id, config_type, data, last_updated, ttl, source)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                config.config_id,
                config.config_type,
                json.dumps(config.data),
                config.last_updated.isoformat(),
                config.ttl,
                config.source
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            self.logger.error(f"Failed to store cached config: {str(e)}")

    def get_recovery_readiness_status(self) -> Dict[str, Any]:
        """Get status of data plane recovery readiness"""
        try:
            status = {
                'pre_provisioned_resources': len(self.pre_provisioned_resources),
                'cached_configurations': len(self.cached_configurations),
                'control_plane_available': self.control_plane_available,
                'last_cache_update': None,
                'standby_resources_by_type': {},
                'cache_freshness': {}
            }
            
            # Analyze standby resources
            for resource in self.pre_provisioned_resources.values():
                resource_type = resource.resource_type
                if resource_type not in status['standby_resources_by_type']:
                    status['standby_resources_by_type'][resource_type] = 0
                status['standby_resources_by_type'][resource_type] += 1
            
            # Analyze cache freshness
            now = datetime.utcnow()
            for config in self.cached_configurations.values():
                config_type = config.config_type
                age = (now - config.last_updated).total_seconds()
                
                if config_type not in status['cache_freshness']:
                    status['cache_freshness'][config_type] = {'oldest': age, 'newest': age, 'average': age}
                else:
                    status['cache_freshness'][config_type]['oldest'] = max(status['cache_freshness'][config_type]['oldest'], age)
                    status['cache_freshness'][config_type]['newest'] = min(status['cache_freshness'][config_type]['newest'], age)
            
            return status
            
        except Exception as e:
            self.logger.error(f"Recovery readiness status check failed: {str(e)}")
            return {}

# Example usage
def main():
    # Initialize data plane recovery system
    recovery_system = DataPlaneRecoverySystem(region='us-east-1')
    
    # Define pre-provisioned resources
    resource_configs = [
        {
            'resource_type': 'ec2_instance',
            'ami_id': 'ami-12345678',
            'instance_type': 't3.medium',
            'security_groups': ['sg-12345678'],
            'subnet_id': 'subnet-12345678',
            'availability_zone': 'us-east-1b',
            'activation_trigger': 'instance_failure',
            'environment': 'production'
        }
    ]
    
    # Define configuration sources to cache
    config_sources = [
        {
            'config_type': 'route53_records',
            'hosted_zone_id': 'Z123456789012345678901',
            'cache_ttl': 3600
        }
    ]
    
    # Set up recovery system
    print("Setting up data plane recovery system...")
    
    pre_provisioned = recovery_system.setup_pre_provisioned_resources(resource_configs)
    cached_configs = recovery_system.cache_critical_configurations(config_sources)
    
    print("Data plane recovery setup complete:")
    print(f"- Pre-provisioned resources: {len(pre_provisioned)}")
    print(f"- Cached configurations: {len(cached_configs)}")
    
    # Get readiness status
    status = recovery_system.get_recovery_readiness_status()
    print(f"Recovery readiness status: {json.dumps(status, indent=2, default=str)}")
    
    # Example recovery execution
    failure_scenario = {
        'type': 'instance_failure',
        'resource_id': 'i-1234567890abcdef0',
        'timestamp': datetime.utcnow().isoformat(),
        'severity': 'high'
    }
    
    recovery_result = recovery_system.execute_data_plane_recovery(failure_scenario)
    print(f"Recovery execution result: {json.dumps(recovery_result, indent=2)}")

if __name__ == "__main__":
    main()
```
{% endraw %}

## AWS Services

### Primary Services
- **Amazon S3**: Store configuration backups and recovery scripts
- **Amazon Route 53**: DNS failover with health checks (data plane operations)
- **Elastic Load Balancing**: Traffic routing without API dependencies
- **Amazon EC2**: Pre-provisioned standby instances

### Supporting Services
- **AWS Systems Manager**: Parameter Store for configuration caching
- **Amazon CloudWatch**: Metrics and alarms (data plane operations)
- **Amazon SQS**: Asynchronous communication for recovery triggers
- **AWS Lambda**: Event-driven recovery logic

## Benefits

- **Control Plane Independence**: Recovery works even when APIs are unavailable
- **Faster Recovery**: Pre-provisioned resources eliminate provisioning delays
- **Reduced API Throttling**: Avoid control plane rate limits during incidents
- **Higher Reliability**: Less dependency on external services during recovery
- **Cost Optimization**: Use stopped instances and cached data to reduce costs

## Related Resources

- [AWS Well-Architected Framework - Reliability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/)
- [Amazon Route 53 Health Checks](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/health-checks-how-they-work.html)
- [Elastic Load Balancing User Guide](https://docs.aws.amazon.com/elasticloadbalancing/)
- [Amazon S3 Developer Guide](https://docs.aws.amazon.com/s3/)
