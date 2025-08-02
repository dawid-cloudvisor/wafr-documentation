---
title: REL11-BP03 - Automate healing on all layers
layout: default
parent: Reliability
nav_order: 113
---

# REL11-BP03: Automate healing on all layers

Automated healing mechanisms operate at every layer of your architecture to detect and recover from failures without human intervention. This includes infrastructure-level healing (instance replacement), platform-level healing (service restart), and application-level healing (circuit breakers, retry logic).

## Implementation Steps

### 1. Infrastructure Layer Healing
Implement automated instance replacement, scaling, and resource provisioning.

### 2. Platform Layer Healing
Configure service-level healing including container restarts and service recovery.

### 3. Application Layer Healing
Build application-level resilience with circuit breakers, retries, and graceful degradation.

### 4. Data Layer Healing
Implement automated backup restoration and data consistency checks.

### 5. Network Layer Healing
Configure automatic network path recovery and traffic rerouting.

## Detailed Implementation

{% raw %}
```python
import boto3
import json
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import threading
from concurrent.futures import ThreadPoolExecutor
import requests
import subprocess

class HealingLayer(Enum):
    INFRASTRUCTURE = "infrastructure"
    PLATFORM = "platform"
    APPLICATION = "application"
    DATA = "data"
    NETWORK = "network"

class HealingAction(Enum):
    RESTART = "restart"
    REPLACE = "replace"
    SCALE = "scale"
    ROLLBACK = "rollback"
    REPAIR = "repair"
    FAILOVER = "failover"

class HealingStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"

@dataclass
class HealingRule:
    name: str
    layer: HealingLayer
    trigger_condition: str
    action: HealingAction
    parameters: Dict[str, Any]
    cooldown_period: int
    max_attempts: int
    enabled: bool

@dataclass
class HealingEvent:
    event_id: str
    rule_name: str
    layer: HealingLayer
    action: HealingAction
    resource_id: str
    status: HealingStatus
    start_time: datetime
    end_time: Optional[datetime]
    attempt_count: int
    error_message: Optional[str]

class AutomatedHealingSystem:
    def __init__(self, region: str = 'us-east-1'):
        self.region = region
        self.ec2 = boto3.client('ec2', region_name=region)
        self.asg = boto3.client('autoscaling', region_name=region)
        self.ecs = boto3.client('ecs', region_name=region)
        self.lambda_client = boto3.client('lambda', region_name=region)
        self.rds = boto3.client('rds', region_name=region)
        self.cloudwatch = boto3.client('cloudwatch', region_name=region)
        self.sns = boto3.client('sns', region_name=region)
        self.ssm = boto3.client('ssm', region_name=region)
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Healing state management
        self.healing_rules: Dict[str, HealingRule] = {}
        self.active_healing_events: Dict[str, HealingEvent] = {}
        self.healing_history: List[HealingEvent] = []
        self.healing_lock = threading.Lock()

    def register_healing_rule(self, rule: HealingRule) -> bool:
        """Register a new healing rule"""
        try:
            self.healing_rules[rule.name] = rule
            self.logger.info(f"Registered healing rule: {rule.name}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to register healing rule {rule.name}: {str(e)}")
            return False

    def setup_infrastructure_healing(self) -> List[HealingRule]:
        """Set up infrastructure layer healing rules"""
        rules = []
        
        try:
            # EC2 Instance Healing
            ec2_healing_rule = HealingRule(
                name="ec2-instance-healing",
                layer=HealingLayer.INFRASTRUCTURE,
                trigger_condition="instance_status_check_failed",
                action=HealingAction.REPLACE,
                parameters={
                    'health_check_grace_period': 300,
                    'replacement_strategy': 'immediate',
                    'preserve_eip': True
                },
                cooldown_period=600,
                max_attempts=3,
                enabled=True
            )
            rules.append(ec2_healing_rule)
            self.register_healing_rule(ec2_healing_rule)
            
            # Auto Scaling Group Healing
            asg_healing_rule = HealingRule(
                name="asg-capacity-healing",
                layer=HealingLayer.INFRASTRUCTURE,
                trigger_condition="unhealthy_instance_threshold",
                action=HealingAction.SCALE,
                parameters={
                    'scale_out_amount': 2,
                    'health_check_type': 'ELB',
                    'terminate_unhealthy': True
                },
                cooldown_period=300,
                max_attempts=5,
                enabled=True
            )
            rules.append(asg_healing_rule)
            self.register_healing_rule(asg_healing_rule)
            
            # EBS Volume Healing
            ebs_healing_rule = HealingRule(
                name="ebs-volume-healing",
                layer=HealingLayer.INFRASTRUCTURE,
                trigger_condition="volume_io_performance_degraded",
                action=HealingAction.REPAIR,
                parameters={
                    'create_snapshot': True,
                    'force_detach': False,
                    'replacement_volume_type': 'gp3'
                },
                cooldown_period=1800,
                max_attempts=2,
                enabled=True
            )
            rules.append(ebs_healing_rule)
            self.register_healing_rule(ebs_healing_rule)
            
            self.logger.info(f"Set up {len(rules)} infrastructure healing rules")
            return rules
            
        except Exception as e:
            self.logger.error(f"Infrastructure healing setup failed: {str(e)}")
            return rules

    def setup_platform_healing(self) -> List[HealingRule]:
        """Set up platform layer healing rules"""
        rules = []
        
        try:
            # ECS Service Healing
            ecs_service_rule = HealingRule(
                name="ecs-service-healing",
                layer=HealingLayer.PLATFORM,
                trigger_condition="service_unhealthy_tasks",
                action=HealingAction.RESTART,
                parameters={
                    'force_new_deployment': True,
                    'desired_count_adjustment': 1,
                    'stop_unhealthy_tasks': True
                },
                cooldown_period=300,
                max_attempts=3,
                enabled=True
            )
            rules.append(ecs_service_rule)
            self.register_healing_rule(ecs_service_rule)
            
            # Lambda Function Healing
            lambda_healing_rule = HealingRule(
                name="lambda-function-healing",
                layer=HealingLayer.PLATFORM,
                trigger_condition="high_error_rate",
                action=HealingAction.ROLLBACK,
                parameters={
                    'rollback_to_previous_version': True,
                    'update_alias': True,
                    'notification_required': True
                },
                cooldown_period=600,
                max_attempts=2,
                enabled=True
            )
            rules.append(lambda_healing_rule)
            self.register_healing_rule(lambda_healing_rule)
            
            # RDS Instance Healing
            rds_healing_rule = HealingRule(
                name="rds-instance-healing",
                layer=HealingLayer.PLATFORM,
                trigger_condition="database_connection_failures",
                action=HealingAction.RESTART,
                parameters={
                    'force_failover': False,
                    'apply_pending_maintenance': False,
                    'backup_before_restart': True
                },
                cooldown_period=1800,
                max_attempts=2,
                enabled=True
            )
            rules.append(rds_healing_rule)
            self.register_healing_rule(rds_healing_rule)
            
            self.logger.info(f"Set up {len(rules)} platform healing rules")
            return rules
            
        except Exception as e:
            self.logger.error(f"Platform healing setup failed: {str(e)}")
            return rules

    def setup_application_healing(self) -> List[HealingRule]:
        """Set up application layer healing rules"""
        rules = []
        
        try:
            # Circuit Breaker Healing
            circuit_breaker_rule = HealingRule(
                name="circuit-breaker-healing",
                layer=HealingLayer.APPLICATION,
                trigger_condition="circuit_breaker_open",
                action=HealingAction.REPAIR,
                parameters={
                    'reset_circuit_breaker': True,
                    'gradual_recovery': True,
                    'test_requests_percentage': 10
                },
                cooldown_period=300,
                max_attempts=5,
                enabled=True
            )
            rules.append(circuit_breaker_rule)
            self.register_healing_rule(circuit_breaker_rule)
            
            # Memory Leak Healing
            memory_healing_rule = HealingRule(
                name="memory-leak-healing",
                layer=HealingLayer.APPLICATION,
                trigger_condition="high_memory_usage",
                action=HealingAction.RESTART,
                parameters={
                    'memory_threshold': 85,
                    'graceful_shutdown': True,
                    'heap_dump_before_restart': True
                },
                cooldown_period=600,
                max_attempts=3,
                enabled=True
            )
            rules.append(memory_healing_rule)
            self.register_healing_rule(memory_healing_rule)
            
            # Connection Pool Healing
            connection_pool_rule = HealingRule(
                name="connection-pool-healing",
                layer=HealingLayer.APPLICATION,
                trigger_condition="connection_pool_exhausted",
                action=HealingAction.REPAIR,
                parameters={
                    'reset_connections': True,
                    'increase_pool_size': True,
                    'connection_timeout_adjustment': 30
                },
                cooldown_period=180,
                max_attempts=4,
                enabled=True
            )
            rules.append(connection_pool_rule)
            self.register_healing_rule(connection_pool_rule)
            
            self.logger.info(f"Set up {len(rules)} application healing rules")
            return rules
            
        except Exception as e:
            self.logger.error(f"Application healing setup failed: {str(e)}")
            return rules

    def setup_data_healing(self) -> List[HealingRule]:
        """Set up data layer healing rules"""
        rules = []
        
        try:
            # Database Corruption Healing
            db_corruption_rule = HealingRule(
                name="database-corruption-healing",
                layer=HealingLayer.DATA,
                trigger_condition="data_corruption_detected",
                action=HealingAction.ROLLBACK,
                parameters={
                    'restore_from_backup': True,
                    'point_in_time_recovery': True,
                    'verify_data_integrity': True
                },
                cooldown_period=3600,
                max_attempts=2,
                enabled=True
            )
            rules.append(db_corruption_rule)
            self.register_healing_rule(db_corruption_rule)
            
            # Cache Invalidation Healing
            cache_healing_rule = HealingRule(
                name="cache-invalidation-healing",
                layer=HealingLayer.DATA,
                trigger_condition="cache_hit_rate_low",
                action=HealingAction.REPAIR,
                parameters={
                    'warm_cache': True,
                    'invalidate_stale_entries': True,
                    'adjust_ttl': True
                },
                cooldown_period=300,
                max_attempts=3,
                enabled=True
            )
            rules.append(cache_healing_rule)
            self.register_healing_rule(cache_healing_rule)
            
            # Backup Verification Healing
            backup_healing_rule = HealingRule(
                name="backup-verification-healing",
                layer=HealingLayer.DATA,
                trigger_condition="backup_verification_failed",
                action=HealingAction.REPAIR,
                parameters={
                    'create_new_backup': True,
                    'test_restore_process': True,
                    'update_backup_schedule': True
                },
                cooldown_period=7200,
                max_attempts=2,
                enabled=True
            )
            rules.append(backup_healing_rule)
            self.register_healing_rule(backup_healing_rule)
            
            self.logger.info(f"Set up {len(rules)} data healing rules")
            return rules
            
        except Exception as e:
            self.logger.error(f"Data healing setup failed: {str(e)}")
            return rules

    def execute_healing_action(self, rule_name: str, resource_id: str, trigger_data: Dict[str, Any]) -> HealingEvent:
        """Execute a healing action based on a rule"""
        event_id = f"healing-{int(time.time())}-{rule_name}"
        
        try:
            rule = self.healing_rules.get(rule_name)
            if not rule or not rule.enabled:
                raise ValueError(f"Healing rule {rule_name} not found or disabled")
            
            # Check cooldown period
            if self._is_in_cooldown(rule_name, resource_id):
                self.logger.info(f"Healing action {rule_name} for {resource_id} skipped due to cooldown")
                return self._create_skipped_event(event_id, rule, resource_id)
            
            # Create healing event
            with self.healing_lock:
                healing_event = HealingEvent(
                    event_id=event_id,
                    rule_name=rule_name,
                    layer=rule.layer,
                    action=rule.action,
                    resource_id=resource_id,
                    status=HealingStatus.PENDING,
                    start_time=datetime.utcnow(),
                    end_time=None,
                    attempt_count=1,
                    error_message=None
                )
                
                self.active_healing_events[event_id] = healing_event
            
            # Update status to in progress
            healing_event.status = HealingStatus.IN_PROGRESS
            
            # Execute healing action based on layer and action
            success = self._execute_layer_healing(rule, resource_id, trigger_data)
            
            # Update final status
            healing_event.status = HealingStatus.COMPLETED if success else HealingStatus.FAILED
            healing_event.end_time = datetime.utcnow()
            
            # Move to history
            with self.healing_lock:
                del self.active_healing_events[event_id]
                self.healing_history.append(healing_event)
            
            # Send notification
            self._send_healing_notification(healing_event)
            
            self.logger.info(f"Healing action {event_id} completed with status: {healing_event.status}")
            return healing_event
            
        except Exception as e:
            healing_event.status = HealingStatus.FAILED
            healing_event.error_message = str(e)
            healing_event.end_time = datetime.utcnow()
            self.logger.error(f"Healing action {event_id} failed: {str(e)}")
            return healing_event

    def _execute_layer_healing(self, rule: HealingRule, resource_id: str, trigger_data: Dict[str, Any]) -> bool:
        """Execute healing action based on layer"""
        try:
            if rule.layer == HealingLayer.INFRASTRUCTURE:
                return self._execute_infrastructure_healing(rule, resource_id, trigger_data)
            elif rule.layer == HealingLayer.PLATFORM:
                return self._execute_platform_healing(rule, resource_id, trigger_data)
            elif rule.layer == HealingLayer.APPLICATION:
                return self._execute_application_healing(rule, resource_id, trigger_data)
            elif rule.layer == HealingLayer.DATA:
                return self._execute_data_healing(rule, resource_id, trigger_data)
            elif rule.layer == HealingLayer.NETWORK:
                return self._execute_network_healing(rule, resource_id, trigger_data)
            else:
                return False
                
        except Exception as e:
            self.logger.error(f"Layer healing execution failed: {str(e)}")
            return False

    def _execute_infrastructure_healing(self, rule: HealingRule, resource_id: str, trigger_data: Dict[str, Any]) -> bool:
        """Execute infrastructure layer healing"""
        try:
            if rule.action == HealingAction.REPLACE and resource_id.startswith('i-'):
                # Replace EC2 instance
                return self._replace_ec2_instance(resource_id, rule.parameters)
            elif rule.action == HealingAction.SCALE and resource_id.startswith('asg-'):
                # Scale Auto Scaling Group
                return self._scale_auto_scaling_group(resource_id, rule.parameters)
            elif rule.action == HealingAction.REPAIR and resource_id.startswith('vol-'):
                # Repair EBS volume
                return self._repair_ebs_volume(resource_id, rule.parameters)
            else:
                return False
                
        except Exception as e:
            self.logger.error(f"Infrastructure healing failed: {str(e)}")
            return False

    def _execute_platform_healing(self, rule: HealingRule, resource_id: str, trigger_data: Dict[str, Any]) -> bool:
        """Execute platform layer healing"""
        try:
            if rule.action == HealingAction.RESTART and 'ecs' in resource_id:
                # Restart ECS service
                return self._restart_ecs_service(resource_id, rule.parameters)
            elif rule.action == HealingAction.ROLLBACK and resource_id.startswith('lambda'):
                # Rollback Lambda function
                return self._rollback_lambda_function(resource_id, rule.parameters)
            elif rule.action == HealingAction.RESTART and resource_id.startswith('db-'):
                # Restart RDS instance
                return self._restart_rds_instance(resource_id, rule.parameters)
            else:
                return False
                
        except Exception as e:
            self.logger.error(f"Platform healing failed: {str(e)}")
            return False

    def _execute_application_healing(self, rule: HealingRule, resource_id: str, trigger_data: Dict[str, Any]) -> bool:
        """Execute application layer healing"""
        try:
            if rule.action == HealingAction.REPAIR and 'circuit-breaker' in rule.name:
                # Reset circuit breaker
                return self._reset_circuit_breaker(resource_id, rule.parameters)
            elif rule.action == HealingAction.RESTART and 'memory' in rule.name:
                # Restart application due to memory issues
                return self._restart_application_for_memory(resource_id, rule.parameters)
            elif rule.action == HealingAction.REPAIR and 'connection-pool' in rule.name:
                # Repair connection pool
                return self._repair_connection_pool(resource_id, rule.parameters)
            else:
                return False
                
        except Exception as e:
            self.logger.error(f"Application healing failed: {str(e)}")
            return False

    def _replace_ec2_instance(self, instance_id: str, parameters: Dict[str, Any]) -> bool:
        """Replace unhealthy EC2 instance"""
        try:
            # Get instance details
            response = self.ec2.describe_instances(InstanceIds=[instance_id])
            instance = response['Reservations'][0]['Instances'][0]
            
            # Terminate the unhealthy instance
            self.ec2.terminate_instances(InstanceIds=[instance_id])
            
            # If part of ASG, let ASG handle replacement
            # Otherwise, launch new instance with same configuration
            if not self._is_instance_in_asg(instance_id):
                launch_template = {
                    'ImageId': instance['ImageId'],
                    'InstanceType': instance['InstanceType'],
                    'KeyName': instance.get('KeyName'),
                    'SecurityGroupIds': [sg['GroupId'] for sg in instance['SecurityGroups']],
                    'SubnetId': instance['SubnetId']
                }
                
                new_instance = self.ec2.run_instances(
                    MinCount=1,
                    MaxCount=1,
                    **launch_template
                )
                
                self.logger.info(f"Launched replacement instance: {new_instance['Instances'][0]['InstanceId']}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"EC2 instance replacement failed: {str(e)}")
            return False

    def _restart_ecs_service(self, service_arn: str, parameters: Dict[str, Any]) -> bool:
        """Restart ECS service"""
        try:
            cluster_name = service_arn.split('/')[1]
            service_name = service_arn.split('/')[-1]
            
            # Force new deployment
            self.ecs.update_service(
                cluster=cluster_name,
                service=service_name,
                forceNewDeployment=parameters.get('force_new_deployment', True)
            )
            
            # Stop unhealthy tasks if requested
            if parameters.get('stop_unhealthy_tasks', False):
                tasks = self.ecs.list_tasks(
                    cluster=cluster_name,
                    serviceName=service_name
                )
                
                for task_arn in tasks['taskArns']:
                    self.ecs.stop_task(
                        cluster=cluster_name,
                        task=task_arn,
                        reason='Automated healing - unhealthy task'
                    )
            
            return True
            
        except Exception as e:
            self.logger.error(f"ECS service restart failed: {str(e)}")
            return False

    def _is_in_cooldown(self, rule_name: str, resource_id: str) -> bool:
        """Check if healing action is in cooldown period"""
        try:
            rule = self.healing_rules.get(rule_name)
            if not rule:
                return False
            
            # Check recent healing events for this rule and resource
            cutoff_time = datetime.utcnow() - timedelta(seconds=rule.cooldown_period)
            
            for event in self.healing_history:
                if (event.rule_name == rule_name and 
                    event.resource_id == resource_id and 
                    event.start_time > cutoff_time):
                    return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Cooldown check failed: {str(e)}")
            return False

    def _send_healing_notification(self, healing_event: HealingEvent) -> None:
        """Send notification about healing event"""
        try:
            message = {
                'event_id': healing_event.event_id,
                'rule_name': healing_event.rule_name,
                'layer': healing_event.layer.value,
                'action': healing_event.action.value,
                'resource_id': healing_event.resource_id,
                'status': healing_event.status.value,
                'start_time': healing_event.start_time.isoformat(),
                'end_time': healing_event.end_time.isoformat() if healing_event.end_time else None,
                'attempt_count': healing_event.attempt_count,
                'error_message': healing_event.error_message
            }
            
            self.sns.publish(
                TopicArn=f"arn:aws:sns:{self.region}:123456789012:healing-notifications",
                Message=json.dumps(message, indent=2),
                Subject=f"Healing Event: {healing_event.status.value.title()}"
            )
            
        except Exception as e:
            self.logger.error(f"Healing notification failed: {str(e)}")

    def start_healing_monitor(self, monitoring_config: Dict[str, Any]) -> None:
        """Start continuous healing monitoring"""
        try:
            self.logger.info("Starting automated healing monitor...")
            
            while True:
                # Check for healing triggers
                for rule_name, rule in self.healing_rules.items():
                    if not rule.enabled:
                        continue
                    
                    # Check trigger conditions
                    triggered_resources = self._check_healing_triggers(rule, monitoring_config)
                    
                    for resource_id, trigger_data in triggered_resources.items():
                        # Execute healing action
                        self.execute_healing_action(rule_name, resource_id, trigger_data)
                
                # Wait before next check
                time.sleep(monitoring_config.get('check_interval', 60))
                
        except KeyboardInterrupt:
            self.logger.info("Healing monitor stopped")
        except Exception as e:
            self.logger.error(f"Healing monitor error: {str(e)}")

    def get_healing_statistics(self) -> Dict[str, Any]:
        """Get healing system statistics"""
        try:
            total_events = len(self.healing_history)
            successful_events = len([e for e in self.healing_history if e.status == HealingStatus.COMPLETED])
            failed_events = len([e for e in self.healing_history if e.status == HealingStatus.FAILED])
            
            layer_stats = {}
            for layer in HealingLayer:
                layer_events = [e for e in self.healing_history if e.layer == layer]
                layer_stats[layer.value] = {
                    'total': len(layer_events),
                    'successful': len([e for e in layer_events if e.status == HealingStatus.COMPLETED]),
                    'failed': len([e for e in layer_events if e.status == HealingStatus.FAILED])
                }
            
            return {
                'total_healing_events': total_events,
                'successful_healing_events': successful_events,
                'failed_healing_events': failed_events,
                'success_rate': (successful_events / total_events * 100) if total_events > 0 else 0,
                'active_healing_events': len(self.active_healing_events),
                'registered_rules': len(self.healing_rules),
                'enabled_rules': len([r for r in self.healing_rules.values() if r.enabled]),
                'layer_statistics': layer_stats
            }
            
        except Exception as e:
            self.logger.error(f"Statistics calculation failed: {str(e)}")
            return {}

# Example usage
def main():
    # Initialize healing system
    healing_system = AutomatedHealingSystem(region='us-east-1')
    
    # Set up healing rules for all layers
    print("Setting up automated healing system...")
    
    infra_rules = healing_system.setup_infrastructure_healing()
    platform_rules = healing_system.setup_platform_healing()
    app_rules = healing_system.setup_application_healing()
    data_rules = healing_system.setup_data_healing()
    
    print("Healing system setup complete:")
    print(f"- Infrastructure rules: {len(infra_rules)}")
    print(f"- Platform rules: {len(platform_rules)}")
    print(f"- Application rules: {len(app_rules)}")
    print(f"- Data rules: {len(data_rules)}")
    
    # Example healing action execution
    healing_event = healing_system.execute_healing_action(
        rule_name="ec2-instance-healing",
        resource_id="i-1234567890abcdef0",
        trigger_data={'status_check': 'failed', 'timestamp': datetime.utcnow().isoformat()}
    )
    
    print(f"Healing action executed: {healing_event.event_id} - Status: {healing_event.status.value}")
    
    # Get system statistics
    stats = healing_system.get_healing_statistics()
    print(f"Healing system statistics: {json.dumps(stats, indent=2)}")

if __name__ == "__main__":
    main()
```
{% endraw %}

## AWS Services

### Primary Services
- **Amazon EC2 Auto Scaling**: Automatic instance replacement and scaling
- **Amazon ECS**: Container-level healing and service management
- **AWS Lambda**: Serverless function healing and rollback
- **Amazon RDS**: Database healing and automated backups

### Supporting Services
- **AWS Systems Manager**: Automated patching and maintenance
- **Amazon CloudWatch**: Monitoring and alarm-based healing triggers
- **AWS Auto Scaling**: Unified scaling across multiple services
- **Amazon SNS**: Healing event notifications

## Benefits

- **Self-Healing Infrastructure**: Automatic recovery without human intervention
- **Multi-Layer Protection**: Healing at every architectural layer
- **Reduced MTTR**: Faster recovery through automated actions
- **Proactive Maintenance**: Prevention of issues before they impact users
- **Operational Efficiency**: Reduced manual intervention and operational overhead

## Related Resources

- [Amazon EC2 Auto Scaling User Guide](https://docs.aws.amazon.com/autoscaling/ec2/)
- [Amazon ECS Developer Guide](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/)
- [AWS Lambda Developer Guide](https://docs.aws.amazon.com/lambda/)
- [AWS Systems Manager User Guide](https://docs.aws.amazon.com/systems-manager/)
