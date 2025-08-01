---
title: REL05-BP07 - Implement emergency levers
layout: default
parent: REL05 - How do you design interactions in a distributed system to mitigate or withstand failures?
grand_parent: Reliability
nav_order: 7
---

# REL05-BP07: Implement emergency levers

## Overview

Implement emergency levers (also known as kill switches or circuit breakers) that allow operators to quickly disable non-essential functionality, redirect traffic, or shut down problematic components during incidents. Emergency levers provide immediate control during crisis situations and help prevent cascading failures while maintaining core system functionality.

## Implementation Steps

### 1. Design Emergency Control Mechanisms
- Implement feature toggles for non-essential functionality
- Create traffic routing controls for emergency redirections
- Design service isolation switches to quarantine problematic components
- Establish load shedding controls for capacity management

### 2. Establish Emergency Response Procedures
- Create runbooks for different emergency scenarios
- Define clear escalation procedures and decision-making authority
- Implement automated emergency responses based on system metrics
- Design communication protocols for emergency situations

### 3. Implement Centralized Emergency Controls
- Create a centralized dashboard for emergency lever management
- Implement role-based access controls for emergency operations
- Design audit trails for all emergency lever activations
- Establish monitoring and alerting for emergency lever usage

### 4. Configure Automated Emergency Responses
- Implement automatic emergency levers based on system health metrics
- Design predictive emergency responses based on trend analysis
- Create automated rollback mechanisms for failed deployments
- Establish automatic traffic redirection during outages

### 5. Test Emergency Procedures Regularly
- Conduct regular emergency response drills and simulations
- Test emergency levers in non-production environments
- Validate emergency procedures through chaos engineering
- Create automated testing for emergency response systems

### 6. Monitor and Optimize Emergency Systems
- Track emergency lever effectiveness and response times
- Monitor false positive activations and tune thresholds
- Implement metrics for emergency response coordination
- Create dashboards for emergency system health and readiness

## Implementation Examples

### Example 1: Comprehensive Emergency Lever System
```python
import boto3
import json
import logging
import time
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, asdict
from enum import Enum
import threading
from datetime import datetime, timedelta

class EmergencyLeverType(Enum):
    FEATURE_TOGGLE = "feature_toggle"
    TRAFFIC_ROUTING = "traffic_routing"
    SERVICE_ISOLATION = "service_isolation"
    LOAD_SHEDDING = "load_shedding"
    CIRCUIT_BREAKER = "circuit_breaker"
    DEPLOYMENT_ROLLBACK = "deployment_rollback"

class EmergencyLeverStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    TRIGGERED = "triggered"
    FAILED = "failed"

@dataclass
class EmergencyLever:
    lever_id: str
    name: str
    lever_type: EmergencyLeverType
    description: str
    status: EmergencyLeverStatus
    auto_trigger_enabled: bool
    trigger_conditions: Dict[str, Any]
    impact_assessment: str
    rollback_procedure: str
    created_at: str
    last_triggered: Optional[str] = None
    triggered_by: Optional[str] = None

@dataclass
class EmergencyEvent:
    event_id: str
    lever_id: str
    triggered_at: str
    triggered_by: str
    trigger_reason: str
    system_state: Dict[str, Any]
    actions_taken: List[str]
    resolution_time: Optional[str] = None

class EmergencyLeverManager:
    """Centralized emergency lever management system"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
        # AWS clients
        self.ssm = boto3.client('ssm')
        self.dynamodb = boto3.resource('dynamodb')
        self.sns = boto3.client('sns')
        self.cloudwatch = boto3.client('cloudwatch')
        self.route53 = boto3.client('route53')
        self.elbv2 = boto3.client('elbv2')
        
        # Storage
        self.levers_table = self.dynamodb.Table(config.get('levers_table', 'emergency-levers'))
        self.events_table = self.dynamodb.Table(config.get('events_table', 'emergency-events'))
        
        # Configuration
        self.notification_topic = config.get('notification_topic_arn')
        self.parameter_prefix = config.get('parameter_prefix', '/emergency/levers/')
        
        # In-memory cache
        self.levers_cache = {}
        self.cache_lock = threading.Lock()
        
        # Load levers from storage
        self._load_levers()
    
    def register_emergency_lever(self, lever: EmergencyLever) -> bool:
        """Register a new emergency lever"""
        try:
            # Store in DynamoDB
            self.levers_table.put_item(Item=asdict(lever))
            
            # Store in Parameter Store for runtime access
            parameter_name = f"{self.parameter_prefix}{lever.lever_id}"
            self.ssm.put_parameter(
                Name=parameter_name,
                Value=json.dumps({
                    'status': lever.status.value,
                    'auto_trigger_enabled': lever.auto_trigger_enabled,
                    'trigger_conditions': lever.trigger_conditions
                }),
                Type='String',
                Overwrite=True,
                Description=f"Emergency lever: {lever.name}"
            )
            
            # Update cache
            with self.cache_lock:
                self.levers_cache[lever.lever_id] = lever
            
            logging.info(f"Registered emergency lever: {lever.lever_id}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to register emergency lever {lever.lever_id}: {str(e)}")
            return False
    
    def trigger_emergency_lever(self, lever_id: str, triggered_by: str, 
                              reason: str, manual: bool = True) -> bool:
        """Trigger an emergency lever"""
        try:
            lever = self.levers_cache.get(lever_id)
            if not lever:
                logging.error(f"Emergency lever {lever_id} not found")
                return False
            
            # Create emergency event
            event = EmergencyEvent(
                event_id=f"event_{int(time.time())}_{lever_id}",
                lever_id=lever_id,
                triggered_at=datetime.utcnow().isoformat(),
                triggered_by=triggered_by,
                trigger_reason=reason,
                system_state=self._capture_system_state(),
                actions_taken=[]
            )
            
            # Execute lever-specific actions
            actions_taken = self._execute_lever_actions(lever, event)
            event.actions_taken = actions_taken
            
            # Update lever status
            lever.status = EmergencyLeverStatus.TRIGGERED
            lever.last_triggered = event.triggered_at
            lever.triggered_by = triggered_by
            
            # Store event
            self.events_table.put_item(Item=asdict(event))
            
            # Update lever in storage
            self.levers_table.put_item(Item=asdict(lever))
            
            # Update Parameter Store
            parameter_name = f"{self.parameter_prefix}{lever_id}"
            self.ssm.put_parameter(
                Name=parameter_name,
                Value=json.dumps({
                    'status': lever.status.value,
                    'last_triggered': lever.last_triggered,
                    'triggered_by': triggered_by
                }),
                Type='String',
                Overwrite=True
            )
            
            # Send notifications
            self._send_emergency_notification(lever, event, manual)
            
            # Publish metrics
            self._publish_emergency_metrics(lever, event)
            
            logging.info(f"Emergency lever {lever_id} triggered by {triggered_by}: {reason}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to trigger emergency lever {lever_id}: {str(e)}")
            return False
    
    def _execute_lever_actions(self, lever: EmergencyLever, event: EmergencyEvent) -> List[str]:
        """Execute actions specific to the lever type"""
        actions_taken = []
        
        try:
            if lever.lever_type == EmergencyLeverType.FEATURE_TOGGLE:
                actions_taken.extend(self._execute_feature_toggle(lever))
            
            elif lever.lever_type == EmergencyLeverType.TRAFFIC_ROUTING:
                actions_taken.extend(self._execute_traffic_routing(lever))
            
            elif lever.lever_type == EmergencyLeverType.SERVICE_ISOLATION:
                actions_taken.extend(self._execute_service_isolation(lever))
            
            elif lever.lever_type == EmergencyLeverType.LOAD_SHEDDING:
                actions_taken.extend(self._execute_load_shedding(lever))
            
            elif lever.lever_type == EmergencyLeverType.CIRCUIT_BREAKER:
                actions_taken.extend(self._execute_circuit_breaker(lever))
            
            elif lever.lever_type == EmergencyLeverType.DEPLOYMENT_ROLLBACK:
                actions_taken.extend(self._execute_deployment_rollback(lever))
            
        except Exception as e:
            logging.error(f"Failed to execute actions for lever {lever.lever_id}: {str(e)}")
            actions_taken.append(f"ERROR: {str(e)}")
        
        return actions_taken
    
    def _execute_feature_toggle(self, lever: EmergencyLever) -> List[str]:
        """Execute feature toggle emergency actions"""
        actions = []
        
        try:
            # Disable features specified in trigger conditions
            features_to_disable = lever.trigger_conditions.get('features', [])
            
            for feature in features_to_disable:
                feature_param = f"/features/{feature}/enabled"
                
                self.ssm.put_parameter(
                    Name=feature_param,
                    Value='false',
                    Type='String',
                    Overwrite=True
                )
                
                actions.append(f"Disabled feature: {feature}")
            
            # Set emergency mode flag
            self.ssm.put_parameter(
                Name='/system/emergency_mode',
                Value='true',
                Type='String',
                Overwrite=True
            )
            
            actions.append("Enabled emergency mode")
            
        except Exception as e:
            actions.append(f"Feature toggle error: {str(e)}")
        
        return actions
    
    def _execute_traffic_routing(self, lever: EmergencyLever) -> List[str]:
        """Execute traffic routing emergency actions"""
        actions = []
        
        try:
            routing_config = lever.trigger_conditions.get('routing', {})
            
            # Route 53 DNS failover
            if 'route53_record' in routing_config:
                record_config = routing_config['route53_record']
                
                self.route53.change_resource_record_sets(
                    HostedZoneId=record_config['hosted_zone_id'],
                    ChangeBatch={
                        'Changes': [{
                            'Action': 'UPSERT',
                            'ResourceRecordSet': {
                                'Name': record_config['name'],
                                'Type': record_config['type'],
                                'TTL': 60,  # Short TTL for quick failover
                                'ResourceRecords': [{'Value': record_config['emergency_value']}]
                            }
                        }]
                    }
                )
                
                actions.append(f"Updated DNS record: {record_config['name']}")
            
            # Load balancer target group changes
            if 'target_group_arn' in routing_config:
                target_group_arn = routing_config['target_group_arn']
                emergency_targets = routing_config.get('emergency_targets', [])
                
                # Deregister current targets
                current_targets = self.elbv2.describe_target_health(
                    TargetGroupArn=target_group_arn
                )
                
                for target in current_targets['TargetHealthDescriptions']:
                    self.elbv2.deregister_targets(
                        TargetGroupArn=target_group_arn,
                        Targets=[{'Id': target['Target']['Id']}]
                    )
                
                # Register emergency targets
                if emergency_targets:
                    self.elbv2.register_targets(
                        TargetGroupArn=target_group_arn,
                        Targets=[{'Id': target_id} for target_id in emergency_targets]
                    )
                
                actions.append(f"Updated load balancer targets")
            
        except Exception as e:
            actions.append(f"Traffic routing error: {str(e)}")
        
        return actions
    
    def _execute_service_isolation(self, lever: EmergencyLever) -> List[str]:
        """Execute service isolation emergency actions"""
        actions = []
        
        try:
            isolation_config = lever.trigger_conditions.get('isolation', {})
            
            # Isolate services by updating security groups
            if 'security_groups' in isolation_config:
                for sg_id in isolation_config['security_groups']:
                    # Remove inbound rules to isolate service
                    ec2 = boto3.client('ec2')
                    
                    # Get current rules
                    response = ec2.describe_security_groups(GroupIds=[sg_id])
                    current_rules = response['SecurityGroups'][0]['IpPermissions']
                    
                    # Revoke all inbound rules
                    if current_rules:
                        ec2.revoke_security_group_ingress(
                            GroupId=sg_id,
                            IpPermissions=current_rules
                        )
                    
                    actions.append(f"Isolated security group: {sg_id}")
            
            # Scale down problematic services
            if 'auto_scaling_groups' in isolation_config:
                autoscaling = boto3.client('autoscaling')
                
                for asg_name in isolation_config['auto_scaling_groups']:
                    autoscaling.update_auto_scaling_group(
                        AutoScalingGroupName=asg_name,
                        DesiredCapacity=0,
                        MinSize=0
                    )
                    
                    actions.append(f"Scaled down ASG: {asg_name}")
            
        except Exception as e:
            actions.append(f"Service isolation error: {str(e)}")
        
        return actions
    
    def _execute_load_shedding(self, lever: EmergencyLever) -> List[str]:
        """Execute load shedding emergency actions"""
        actions = []
        
        try:
            shedding_config = lever.trigger_conditions.get('load_shedding', {})
            
            # Update rate limiting parameters
            if 'rate_limits' in shedding_config:
                for service, limit in shedding_config['rate_limits'].items():
                    param_name = f"/rate_limits/{service}/requests_per_second"
                    
                    self.ssm.put_parameter(
                        Name=param_name,
                        Value=str(limit),
                        Type='String',
                        Overwrite=True
                    )
                    
                    actions.append(f"Updated rate limit for {service}: {limit} req/s")
            
            # Enable load shedding mode
            self.ssm.put_parameter(
                Name='/system/load_shedding_enabled',
                Value='true',
                Type='String',
                Overwrite=True
            )
            
            actions.append("Enabled load shedding mode")
            
        except Exception as e:
            actions.append(f"Load shedding error: {str(e)}")
        
        return actions
    
    def _capture_system_state(self) -> Dict[str, Any]:
        """Capture current system state for emergency event"""
        try:
            # Get CloudWatch metrics
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(minutes=5)
            
            # Example metrics - would be expanded based on system
            metrics_response = self.cloudwatch.get_metric_statistics(
                Namespace='AWS/ApplicationELB',
                MetricName='RequestCount',
                Dimensions=[],
                StartTime=start_time,
                EndTime=end_time,
                Period=300,
                Statistics=['Sum']
            )
            
            return {
                'timestamp': datetime.utcnow().isoformat(),
                'request_count': len(metrics_response.get('Datapoints', [])),
                'system_health': 'degraded'  # Would be calculated from actual metrics
            }
            
        except Exception as e:
            logging.error(f"Failed to capture system state: {str(e)}")
            return {'error': str(e)}
    
    def _send_emergency_notification(self, lever: EmergencyLever, 
                                   event: EmergencyEvent, manual: bool):
        """Send emergency notification"""
        try:
            if not self.notification_topic:
                return
            
            message = {
                'emergency_lever_triggered': {
                    'lever_id': lever.lever_id,
                    'lever_name': lever.name,
                    'lever_type': lever.lever_type.value,
                    'triggered_by': event.triggered_by,
                    'trigger_reason': event.trigger_reason,
                    'triggered_at': event.triggered_at,
                    'manual_trigger': manual,
                    'actions_taken': event.actions_taken,
                    'impact_assessment': lever.impact_assessment
                }
            }
            
            self.sns.publish(
                TopicArn=self.notification_topic,
                Subject=f"EMERGENCY: {lever.name} Activated",
                Message=json.dumps(message, indent=2)
            )
            
        except Exception as e:
            logging.error(f"Failed to send emergency notification: {str(e)}")
    
    def _publish_emergency_metrics(self, lever: EmergencyLever, event: EmergencyEvent):
        """Publish emergency metrics to CloudWatch"""
        try:
            self.cloudwatch.put_metric_data(
                Namespace='Emergency/Levers',
                MetricData=[
                    {
                        'MetricName': 'LeverTriggered',
                        'Dimensions': [
                            {'Name': 'LeverType', 'Value': lever.lever_type.value},
                            {'Name': 'LeverId', 'Value': lever.lever_id}
                        ],
                        'Value': 1,
                        'Unit': 'Count'
                    }
                ]
            )
            
        except Exception as e:
            logging.error(f"Failed to publish emergency metrics: {str(e)}")
    
    def _load_levers(self):
        """Load emergency levers from storage"""
        try:
            response = self.levers_table.scan()
            
            with self.cache_lock:
                for item in response['Items']:
                    lever = EmergencyLever(**item)
                    self.levers_cache[lever.lever_id] = lever
            
            logging.info(f"Loaded {len(self.levers_cache)} emergency levers")
            
        except Exception as e:
            logging.error(f"Failed to load emergency levers: {str(e)}")
    
    def get_lever_status(self, lever_id: str) -> Optional[EmergencyLever]:
        """Get current status of an emergency lever"""
        return self.levers_cache.get(lever_id)
    
    def list_active_levers(self) -> List[EmergencyLever]:
        """List all currently active emergency levers"""
        with self.cache_lock:
            return [
                lever for lever in self.levers_cache.values()
                if lever.status == EmergencyLeverStatus.TRIGGERED
            ]

# Usage example
def main():
    config = {
        'levers_table': 'emergency-levers',
        'events_table': 'emergency-events',
        'notification_topic_arn': 'arn:aws:sns:us-east-1:123456789012:emergency-notifications',
        'parameter_prefix': '/emergency/levers/'
    }
    
    # Initialize emergency lever manager
    emergency_manager = EmergencyLeverManager(config)
    
    # Register emergency levers
    feature_toggle_lever = EmergencyLever(
        lever_id='feature_toggle_non_essential',
        name='Disable Non-Essential Features',
        lever_type=EmergencyLeverType.FEATURE_TOGGLE,
        description='Disable non-essential features during high load',
        status=EmergencyLeverStatus.ACTIVE,
        auto_trigger_enabled=True,
        trigger_conditions={
            'features': ['recommendations', 'analytics', 'social_features'],
            'cpu_threshold': 80,
            'error_rate_threshold': 5
        },
        impact_assessment='Low impact - non-essential features only',
        rollback_procedure='Re-enable features via parameter store',
        created_at=datetime.utcnow().isoformat()
    )
    
    traffic_routing_lever = EmergencyLever(
        lever_id='traffic_routing_maintenance',
        name='Route Traffic to Maintenance Page',
        lever_type=EmergencyLeverType.TRAFFIC_ROUTING,
        description='Route all traffic to maintenance page during emergencies',
        status=EmergencyLeverStatus.ACTIVE,
        auto_trigger_enabled=False,
        trigger_conditions={
            'routing': {
                'route53_record': {
                    'hosted_zone_id': 'Z123456789',
                    'name': 'api.example.com',
                    'type': 'A',
                    'emergency_value': '192.0.2.1'
                }
            }
        },
        impact_assessment='High impact - all traffic affected',
        rollback_procedure='Restore original DNS records',
        created_at=datetime.utcnow().isoformat()
    )
    
    # Register levers
    emergency_manager.register_emergency_lever(feature_toggle_lever)
    emergency_manager.register_emergency_lever(traffic_routing_lever)
    
    # Example: Trigger emergency lever manually
    success = emergency_manager.trigger_emergency_lever(
        lever_id='feature_toggle_non_essential',
        triggered_by='operator@example.com',
        reason='High CPU usage detected - 85%',
        manual=True
    )
    
    if success:
        print("Emergency lever triggered successfully")
    else:
        print("Failed to trigger emergency lever")
    
    # Check active levers
    active_levers = emergency_manager.list_active_levers()
    print(f"Active emergency levers: {len(active_levers)}")
    
    for lever in active_levers:
        print(f"- {lever.name} (triggered by {lever.triggered_by})")

if __name__ == "__main__":
    main()
```

## AWS Services Used

- **AWS Systems Manager Parameter Store**: Dynamic configuration management for emergency levers
- **Amazon DynamoDB**: Storage for emergency lever configurations and event history
- **Amazon SNS**: Notifications for emergency lever activations and status changes
- **Amazon CloudWatch**: Metrics monitoring and automated emergency lever triggers
- **Amazon Route 53**: DNS-based traffic routing for emergency redirections
- **Elastic Load Balancing**: Load balancer configuration changes for traffic management
- **AWS Auto Scaling**: Automatic scaling adjustments during emergency situations
- **Amazon EC2**: Security group modifications for service isolation
- **AWS Lambda**: Serverless functions for automated emergency response logic
- **Amazon API Gateway**: API throttling and request routing during emergencies
- **AWS Step Functions**: Workflow orchestration for complex emergency procedures
- **AWS CloudFormation**: Infrastructure rollback and emergency stack management
- **Amazon S3**: Static content serving for maintenance pages and emergency responses
- **AWS X-Ray**: Distributed tracing for emergency response analysis
- **AWS Config**: Configuration compliance monitoring for emergency procedures

## Benefits

- **Rapid Incident Response**: Immediate control during crisis situations to prevent escalation
- **Damage Limitation**: Quick isolation of problematic components to prevent cascading failures
- **Service Continuity**: Maintain core functionality while disabling non-essential features
- **Operational Control**: Clear procedures and tools for emergency decision-making
- **Automated Response**: Proactive emergency actions based on system health metrics
- **Audit Trail**: Complete logging and tracking of emergency actions for post-incident analysis
- **Risk Mitigation**: Reduced blast radius through controlled emergency responses
- **Recovery Acceleration**: Faster system recovery through organized emergency procedures
- **Team Coordination**: Centralized emergency management improves team response coordination
- **Business Protection**: Minimize business impact through controlled degradation strategies

## Related Resources

- [AWS Well-Architected Reliability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/)
- [Implement Emergency Levers](https://docs.aws.amazon.com/wellarchitected/latest/framework/rel_mitigate_interaction_failure_emergency_levers.html)
- [AWS Systems Manager Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html)
- [Amazon CloudWatch Alarms](https://docs.aws.amazon.com/cloudwatch/latest/monitoring/AlarmThatSendsEmail.html)
- [Amazon Route 53 Health Checks](https://docs.aws.amazon.com/route53/latest/developerguide/health-checks-creating.html)
- [AWS Auto Scaling](https://docs.aws.amazon.com/autoscaling/latest/userguide/)
- [Circuit Breaker Pattern](https://aws.amazon.com/builders-library/implementing-health-checks/)
- [Feature Flags and Toggles](https://aws.amazon.com/builders-library/automating-safe-hands-off-deployments/)
- [Incident Response](https://aws.amazon.com/blogs/architecture/disaster-recovery-dr-architecture-on-aws-part-i-strategies-for-recovery-in-the-cloud/)
- [Chaos Engineering](https://aws.amazon.com/blogs/architecture/verify-the-resilience-of-your-workloads-using-chaos-engineering/)
- [Amazon SNS User Guide](https://docs.aws.amazon.com/sns/latest/dg/)
- [Building Resilient Systems](https://aws.amazon.com/builders-library/)
