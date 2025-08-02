---
title: REL07-BP02 - Obtain resources upon detection of impairment to a workload
layout: default
parent: REL07 - How do you design your workload to adapt to changes in demand?
grand_parent: Reliability
nav_order: 2
---

# REL07-BP02: Obtain resources upon detection of impairment to a workload

## Overview

Implement automated systems to detect workload impairments and rapidly provision additional resources to maintain service availability and performance. This proactive approach ensures that degraded components are quickly replaced or supplemented, minimizing impact on users and maintaining system reliability.

## Implementation Steps

### 1. Design Impairment Detection Systems
- Implement comprehensive health monitoring across all workload components
- Configure multi-layered health checks and synthetic monitoring
- Establish baseline performance metrics and deviation thresholds
- Design real-time anomaly detection and alerting systems

### 2. Create Automated Resource Provisioning
- Implement automatic resource replacement for failed components
- Configure rapid provisioning of backup resources and standby capacity
- Design intelligent resource allocation based on impairment type and severity
- Establish resource pools and pre-warmed capacity for quick deployment

### 3. Implement Self-Healing Mechanisms
- Configure automatic instance replacement and service recovery
- Implement circuit breakers and failover mechanisms
- Design graceful degradation strategies for partial impairments
- Establish automated rollback and recovery procedures

### 4. Set Up Cross-Region and Multi-AZ Recovery
- Implement automatic failover to healthy regions and availability zones
- Configure cross-region resource provisioning and data replication
- Design traffic routing and load balancing for impaired resources
- Establish disaster recovery automation and orchestration

### 5. Configure Intelligent Resource Scaling
- Implement predictive scaling based on impairment patterns
- Configure burst capacity and emergency resource allocation
- Design cost-optimized resource provisioning strategies
- Establish resource lifecycle management and cleanup

### 6. Monitor and Optimize Recovery Performance
- Track mean time to detection (MTTD) and mean time to recovery (MTTR)
- Monitor resource provisioning speed and success rates
- Implement continuous improvement based on recovery analytics
- Establish recovery testing and validation procedures

## Implementation Examples

### Example 1: Automated Impairment Detection and Recovery System
```python
import boto3
import json
import logging
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import time
import uuid

class ImpairmentType(Enum):
    INSTANCE_FAILURE = "instance_failure"
    SERVICE_DEGRADATION = "service_degradation"
    NETWORK_ISSUE = "network_issue"
    RESOURCE_EXHAUSTION = "resource_exhaustion"
    APPLICATION_ERROR = "application_error"
    DATABASE_ISSUE = "database_issue"

class ImpairmentSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class RecoveryAction(Enum):
    REPLACE_INSTANCE = "replace_instance"
    SCALE_OUT = "scale_out"
    FAILOVER = "failover"
    RESTART_SERVICE = "restart_service"
    PROVISION_BACKUP = "provision_backup"
    REDIRECT_TRAFFIC = "redirect_traffic"

@dataclass
class ImpairmentEvent:
    event_id: str
    impairment_type: ImpairmentType
    severity: ImpairmentSeverity
    affected_resources: List[str]
    detection_time: datetime
    description: str
    metrics: Dict[str, Any]
    recovery_actions: List[RecoveryAction]
    resolved: bool
    resolution_time: Optional[datetime] = None

@dataclass
class RecoveryPlan:
    plan_id: str
    impairment_type: ImpairmentType
    severity_threshold: ImpairmentSeverity
    recovery_actions: List[Dict[str, Any]]
    max_execution_time: int
    rollback_actions: List[Dict[str, Any]]
    enabled: bool

class ImpairmentRecoverySystem:
    """Automated impairment detection and recovery system"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
        # AWS clients
        self.ec2 = boto3.client('ec2')
        self.autoscaling = boto3.client('autoscaling')
        self.elbv2 = boto3.client('elbv2')
        self.route53 = boto3.client('route53')
        self.cloudwatch = boto3.client('cloudwatch')
        self.lambda_client = boto3.client('lambda')
        self.sns = boto3.client('sns')
        self.dynamodb = boto3.resource('dynamodb')
        
        # Storage
        self.events_table = self.dynamodb.Table(config.get('events_table', 'impairment-events'))
        self.recovery_plans_table = self.dynamodb.Table(config.get('recovery_plans_table', 'recovery-plans'))
        
        # Recovery configuration
        self.recovery_plans = {}
        self.active_recoveries = {}
        
        # Load recovery plans
        self.load_recovery_plans()
        
    def load_recovery_plans(self):
        """Load recovery plans from storage"""
        try:
            response = self.recovery_plans_table.scan()
            
            for item in response['Items']:
                plan = RecoveryPlan(**item)
                self.recovery_plans[plan.plan_id] = plan
            
            logging.info(f"Loaded {len(self.recovery_plans)} recovery plans")
            
        except Exception as e:
            logging.error(f"Failed to load recovery plans: {str(e)}")
    
    async def detect_impairments(self) -> List[ImpairmentEvent]:
        """Continuously monitor for workload impairments"""
        detected_impairments = []
        
        try:
            # Check instance health
            instance_impairments = await self._check_instance_health()
            detected_impairments.extend(instance_impairments)
            
            # Check service health
            service_impairments = await self._check_service_health()
            detected_impairments.extend(service_impairments)
            
            # Check network connectivity
            network_impairments = await self._check_network_health()
            detected_impairments.extend(network_impairments)
            
            # Check resource utilization
            resource_impairments = await self._check_resource_utilization()
            detected_impairments.extend(resource_impairments)
            
            # Check application metrics
            application_impairments = await self._check_application_health()
            detected_impairments.extend(application_impairments)
            
            # Process detected impairments
            for impairment in detected_impairments:
                await self._process_impairment(impairment)
            
            return detected_impairments
            
        except Exception as e:
            logging.error(f"Failed to detect impairments: {str(e)}")
            return []
    
    async def _check_instance_health(self) -> List[ImpairmentEvent]:
        """Check EC2 instance health status"""
        impairments = []
        
        try:
            # Get all instances in Auto Scaling Groups
            asg_response = self.autoscaling.describe_auto_scaling_groups()
            
            for asg in asg_response['AutoScalingGroups']:
                for instance in asg['Instances']:
                    if instance['HealthStatus'] != 'Healthy':
                        impairment = ImpairmentEvent(
                            event_id=f"instance_{instance['InstanceId']}_{int(time.time())}",
                            impairment_type=ImpairmentType.INSTANCE_FAILURE,
                            severity=ImpairmentSeverity.HIGH,
                            affected_resources=[instance['InstanceId']],
                            detection_time=datetime.utcnow(),
                            description=f"Instance {instance['InstanceId']} is unhealthy",
                            metrics={'health_status': instance['HealthStatus']},
                            recovery_actions=[RecoveryAction.REPLACE_INSTANCE],
                            resolved=False
                        )
                        impairments.append(impairment)
            
            # Check instance status checks
            instance_status_response = self.ec2.describe_instance_status()
            
            for status in instance_status_response['InstanceStatuses']:
                if (status['InstanceStatus']['Status'] != 'ok' or 
                    status['SystemStatus']['Status'] != 'ok'):
                    
                    impairment = ImpairmentEvent(
                        event_id=f"status_{status['InstanceId']}_{int(time.time())}",
                        impairment_type=ImpairmentType.INSTANCE_FAILURE,
                        severity=ImpairmentSeverity.MEDIUM,
                        affected_resources=[status['InstanceId']],
                        detection_time=datetime.utcnow(),
                        description=f"Instance {status['InstanceId']} failed status checks",
                        metrics={
                            'instance_status': status['InstanceStatus']['Status'],
                            'system_status': status['SystemStatus']['Status']
                        },
                        recovery_actions=[RecoveryAction.REPLACE_INSTANCE],
                        resolved=False
                    )
                    impairments.append(impairment)
            
            return impairments
            
        except Exception as e:
            logging.error(f"Failed to check instance health: {str(e)}")
            return []
    
    async def _check_service_health(self) -> List[ImpairmentEvent]:
        """Check service health through load balancer health checks"""
        impairments = []
        
        try:
            # Get all load balancers
            lb_response = self.elbv2.describe_load_balancers()
            
            for lb in lb_response['LoadBalancers']:
                # Get target groups
                tg_response = self.elbv2.describe_target_groups(
                    LoadBalancerArn=lb['LoadBalancerArn']
                )
                
                for tg in tg_response['TargetGroups']:
                    # Get target health
                    health_response = self.elbv2.describe_target_health(
                        TargetGroupArn=tg['TargetGroupArn']
                    )
                    
                    unhealthy_targets = [
                        target for target in health_response['TargetHealthDescriptions']
                        if target['TargetHealth']['State'] != 'healthy'
                    ]
                    
                    if unhealthy_targets:
                        severity = (ImpairmentSeverity.CRITICAL 
                                  if len(unhealthy_targets) > len(health_response['TargetHealthDescriptions']) / 2
                                  else ImpairmentSeverity.HIGH)
                        
                        impairment = ImpairmentEvent(
                            event_id=f"service_{tg['TargetGroupName']}_{int(time.time())}",
                            impairment_type=ImpairmentType.SERVICE_DEGRADATION,
                            severity=severity,
                            affected_resources=[target['Target']['Id'] for target in unhealthy_targets],
                            detection_time=datetime.utcnow(),
                            description=f"Service degradation in target group {tg['TargetGroupName']}",
                            metrics={
                                'unhealthy_targets': len(unhealthy_targets),
                                'total_targets': len(health_response['TargetHealthDescriptions']),
                                'target_group': tg['TargetGroupName']
                            },
                            recovery_actions=[RecoveryAction.SCALE_OUT, RecoveryAction.REPLACE_INSTANCE],
                            resolved=False
                        )
                        impairments.append(impairment)
            
            return impairments
            
        except Exception as e:
            logging.error(f"Failed to check service health: {str(e)}")
            return []
    
    async def _check_resource_utilization(self) -> List[ImpairmentEvent]:
        """Check for resource exhaustion issues"""
        impairments = []
        
        try:
            # Check CPU utilization
            cpu_impairments = await self._check_cpu_utilization()
            impairments.extend(cpu_impairments)
            
            # Check memory utilization
            memory_impairments = await self._check_memory_utilization()
            impairments.extend(memory_impairments)
            
            # Check disk utilization
            disk_impairments = await self._check_disk_utilization()
            impairments.extend(disk_impairments)
            
            return impairments
            
        except Exception as e:
            logging.error(f"Failed to check resource utilization: {str(e)}")
            return []
    
    async def _check_cpu_utilization(self) -> List[ImpairmentEvent]:
        """Check CPU utilization across instances"""
        impairments = []
        
        try:
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(minutes=10)
            
            # Get CPU metrics for all instances
            response = self.cloudwatch.get_metric_statistics(
                Namespace='AWS/EC2',
                MetricName='CPUUtilization',
                StartTime=start_time,
                EndTime=end_time,
                Period=300,
                Statistics=['Average']
            )
            
            # Check for high CPU utilization
            for datapoint in response['Datapoints']:
                if datapoint['Average'] > 90:  # 90% CPU threshold
                    impairment = ImpairmentEvent(
                        event_id=f"cpu_exhaustion_{int(time.time())}",
                        impairment_type=ImpairmentType.RESOURCE_EXHAUSTION,
                        severity=ImpairmentSeverity.HIGH,
                        affected_resources=['cpu'],
                        detection_time=datetime.utcnow(),
                        description=f"High CPU utilization detected: {datapoint['Average']:.1f}%",
                        metrics={'cpu_utilization': datapoint['Average']},
                        recovery_actions=[RecoveryAction.SCALE_OUT],
                        resolved=False
                    )
                    impairments.append(impairment)
            
            return impairments
            
        except Exception as e:
            logging.error(f"Failed to check CPU utilization: {str(e)}")
            return []
    
    async def _process_impairment(self, impairment: ImpairmentEvent):
        """Process detected impairment and initiate recovery"""
        try:
            # Store impairment event
            await self._store_impairment_event(impairment)
            
            # Find matching recovery plan
            recovery_plan = self._find_recovery_plan(impairment)
            
            if recovery_plan:
                # Execute recovery actions
                recovery_id = await self._execute_recovery_plan(impairment, recovery_plan)
                
                if recovery_id:
                    self.active_recoveries[recovery_id] = {
                        'impairment': impairment,
                        'recovery_plan': recovery_plan,
                        'start_time': datetime.utcnow()
                    }
                    
                    logging.info(f"Initiated recovery {recovery_id} for impairment {impairment.event_id}")
            else:
                logging.warning(f"No recovery plan found for impairment {impairment.event_id}")
                
                # Send alert for manual intervention
                await self._send_manual_intervention_alert(impairment)
            
        except Exception as e:
            logging.error(f"Failed to process impairment {impairment.event_id}: {str(e)}")
    
    def _find_recovery_plan(self, impairment: ImpairmentEvent) -> Optional[RecoveryPlan]:
        """Find appropriate recovery plan for impairment"""
        for plan in self.recovery_plans.values():
            if (plan.impairment_type == impairment.impairment_type and
                plan.severity_threshold.value <= impairment.severity.value and
                plan.enabled):
                return plan
        return None
    
    async def _execute_recovery_plan(self, impairment: ImpairmentEvent, plan: RecoveryPlan) -> Optional[str]:
        """Execute recovery plan actions"""
        try:
            recovery_id = f"recovery_{int(time.time())}_{impairment.event_id}"
            
            for action in plan.recovery_actions:
                action_result = await self._execute_recovery_action(action, impairment)
                
                if not action_result:
                    logging.error(f"Recovery action failed: {action}")
                    # Execute rollback if needed
                    await self._execute_rollback_actions(plan.rollback_actions, impairment)
                    return None
            
            return recovery_id
            
        except Exception as e:
            logging.error(f"Failed to execute recovery plan: {str(e)}")
            return None
    
    async def _execute_recovery_action(self, action: Dict[str, Any], impairment: ImpairmentEvent) -> bool:
        """Execute a specific recovery action"""
        try:
            action_type = RecoveryAction(action['type'])
            
            if action_type == RecoveryAction.REPLACE_INSTANCE:
                return await self._replace_instance_action(action, impairment)
            elif action_type == RecoveryAction.SCALE_OUT:
                return await self._scale_out_action(action, impairment)
            elif action_type == RecoveryAction.FAILOVER:
                return await self._failover_action(action, impairment)
            elif action_type == RecoveryAction.RESTART_SERVICE:
                return await self._restart_service_action(action, impairment)
            elif action_type == RecoveryAction.PROVISION_BACKUP:
                return await self._provision_backup_action(action, impairment)
            elif action_type == RecoveryAction.REDIRECT_TRAFFIC:
                return await self._redirect_traffic_action(action, impairment)
            else:
                logging.warning(f"Unknown recovery action type: {action_type}")
                return False
                
        except Exception as e:
            logging.error(f"Failed to execute recovery action: {str(e)}")
            return False
    
    async def _replace_instance_action(self, action: Dict[str, Any], impairment: ImpairmentEvent) -> bool:
        """Replace failed instances"""
        try:
            for resource_id in impairment.affected_resources:
                if resource_id.startswith('i-'):  # EC2 instance
                    # Terminate unhealthy instance (Auto Scaling will replace it)
                    self.ec2.terminate_instances(InstanceIds=[resource_id])
                    
                    logging.info(f"Terminated unhealthy instance: {resource_id}")
            
            return True
            
        except Exception as e:
            logging.error(f"Failed to replace instance: {str(e)}")
            return False
    
    async def _scale_out_action(self, action: Dict[str, Any], impairment: ImpairmentEvent) -> bool:
        """Scale out to handle impairment"""
        try:
            asg_name = action.get('auto_scaling_group_name')
            scale_amount = action.get('scale_amount', 2)
            
            if not asg_name:
                logging.error("No Auto Scaling Group specified for scale out action")
                return False
            
            # Get current capacity
            response = self.autoscaling.describe_auto_scaling_groups(
                AutoScalingGroupNames=[asg_name]
            )
            
            if response['AutoScalingGroups']:
                asg = response['AutoScalingGroups'][0]
                current_capacity = asg['DesiredCapacity']
                new_capacity = min(current_capacity + scale_amount, asg['MaxSize'])
                
                # Update desired capacity
                self.autoscaling.set_desired_capacity(
                    AutoScalingGroupName=asg_name,
                    DesiredCapacity=new_capacity,
                    HonorCooldown=False
                )
                
                logging.info(f"Scaled out {asg_name} from {current_capacity} to {new_capacity}")
                return True
            
            return False
            
        except Exception as e:
            logging.error(f"Failed to scale out: {str(e)}")
            return False
    
    async def _failover_action(self, action: Dict[str, Any], impairment: ImpairmentEvent) -> bool:
        """Perform failover to backup resources"""
        try:
            failover_type = action.get('failover_type', 'region')
            
            if failover_type == 'region':
                return await self._perform_region_failover(action, impairment)
            elif failover_type == 'availability_zone':
                return await self._perform_az_failover(action, impairment)
            else:
                logging.error(f"Unknown failover type: {failover_type}")
                return False
                
        except Exception as e:
            logging.error(f"Failed to perform failover: {str(e)}")
            return False
    
    async def _perform_region_failover(self, action: Dict[str, Any], impairment: ImpairmentEvent) -> bool:
        """Perform cross-region failover"""
        try:
            backup_region = action.get('backup_region')
            hosted_zone_id = action.get('hosted_zone_id')
            record_name = action.get('record_name')
            
            if not all([backup_region, hosted_zone_id, record_name]):
                logging.error("Missing required parameters for region failover")
                return False
            
            # Update Route 53 record to point to backup region
            self.route53.change_resource_record_sets(
                HostedZoneId=hosted_zone_id,
                ChangeBatch={
                    'Changes': [
                        {
                            'Action': 'UPSERT',
                            'ResourceRecordSet': {
                                'Name': record_name,
                                'Type': 'A',
                                'SetIdentifier': 'failover-backup',
                                'Failover': 'SECONDARY',
                                'AliasTarget': {
                                    'DNSName': action.get('backup_dns_name'),
                                    'EvaluateTargetHealth': True,
                                    'HostedZoneId': action.get('backup_zone_id')
                                }
                            }
                        }
                    ]
                }
            )
            
            logging.info(f"Performed region failover to {backup_region}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to perform region failover: {str(e)}")
            return False
    
    async def _store_impairment_event(self, impairment: ImpairmentEvent):
        """Store impairment event in DynamoDB"""
        try:
            event_dict = asdict(impairment)
            event_dict['detection_time'] = impairment.detection_time.isoformat()
            if impairment.resolution_time:
                event_dict['resolution_time'] = impairment.resolution_time.isoformat()
            
            self.events_table.put_item(Item=event_dict)
            
        except Exception as e:
            logging.error(f"Failed to store impairment event: {str(e)}")
    
    async def _send_manual_intervention_alert(self, impairment: ImpairmentEvent):
        """Send alert for manual intervention"""
        try:
            topic_arn = self.config.get('manual_intervention_topic_arn')
            if not topic_arn:
                return
            
            message = {
                'event_id': impairment.event_id,
                'impairment_type': impairment.impairment_type.value,
                'severity': impairment.severity.value,
                'description': impairment.description,
                'affected_resources': impairment.affected_resources,
                'detection_time': impairment.detection_time.isoformat(),
                'action_required': 'Manual intervention required - no automated recovery plan available'
            }
            
            self.sns.publish(
                TopicArn=topic_arn,
                Message=json.dumps(message, indent=2),
                Subject=f"Manual Intervention Required: {impairment.impairment_type.value}"
            )
            
        except Exception as e:
            logging.error(f"Failed to send manual intervention alert: {str(e)}")

# Usage example
async def main():
    config = {
        'events_table': 'impairment-events',
        'recovery_plans_table': 'recovery-plans',
        'manual_intervention_topic_arn': 'arn:aws:sns:us-east-1:123456789012:manual-intervention'
    }
    
    # Initialize recovery system
    recovery_system = ImpairmentRecoverySystem(config)
    
    # Create sample recovery plan
    recovery_plan = RecoveryPlan(
        plan_id='instance-failure-plan',
        impairment_type=ImpairmentType.INSTANCE_FAILURE,
        severity_threshold=ImpairmentSeverity.MEDIUM,
        recovery_actions=[
            {
                'type': 'replace_instance',
                'description': 'Replace failed instances'
            },
            {
                'type': 'scale_out',
                'auto_scaling_group_name': 'web-app-asg',
                'scale_amount': 1,
                'description': 'Scale out to maintain capacity'
            }
        ],
        max_execution_time=600,  # 10 minutes
        rollback_actions=[],
        enabled=True
    )
    
    recovery_system.recovery_plans[recovery_plan.plan_id] = recovery_plan
    
    # Detect and process impairments
    impairments = await recovery_system.detect_impairments()
    print(f"Detected {len(impairments)} impairments")
    
    for impairment in impairments:
        print(f"- {impairment.impairment_type.value}: {impairment.description}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## AWS Services Used

- **Amazon EC2**: Instance health monitoring, status checks, and automated replacement
- **AWS Auto Scaling**: Automatic capacity adjustment and unhealthy instance replacement
- **Elastic Load Balancing**: Health checks, target group monitoring, and traffic distribution
- **Amazon Route 53**: DNS-based failover and health check routing
- **Amazon CloudWatch**: Metrics monitoring, alarms, and automated response triggers
- **AWS Lambda**: Serverless functions for custom health checks and recovery logic
- **Amazon SNS**: Alert notifications and manual intervention requests
- **Amazon DynamoDB**: Storage for impairment events and recovery plan configurations
- **AWS Systems Manager**: Automated patching, configuration management, and remediation
- **Amazon RDS**: Multi-AZ deployments and automated failover for databases
- **Amazon S3**: Cross-region replication and backup storage for disaster recovery
- **AWS CloudFormation**: Infrastructure as code for rapid resource provisioning
- **Amazon ECS/EKS**: Container health monitoring and automatic task replacement
- **AWS Step Functions**: Complex recovery workflow orchestration and state management
- **Amazon EventBridge**: Event-driven recovery automation and cross-service integration

## Benefits

- **Rapid Recovery**: Automated detection and response minimize downtime and service impact
- **Proactive Healing**: Self-healing mechanisms prevent small issues from becoming major outages
- **Cost Efficiency**: Intelligent resource provisioning optimizes costs during recovery operations
- **Reduced Manual Intervention**: Automation reduces the need for human intervention during incidents
- **Consistent Response**: Standardized recovery procedures ensure reliable and predictable outcomes
- **Multi-Layer Protection**: Comprehensive monitoring across all infrastructure and application layers
- **Cross-Region Resilience**: Automatic failover capabilities provide geographic redundancy
- **Faster MTTR**: Automated recovery significantly reduces mean time to recovery
- **Scalable Operations**: Recovery systems scale with workload growth and complexity
- **Audit Trail**: Complete logging and tracking of all recovery actions for compliance and analysis

## Related Resources

- [AWS Well-Architected Reliability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/)
- [Obtain Resources Upon Detection of Impairment](https://docs.aws.amazon.com/wellarchitected/latest/framework/rel_adapt_to_changes_in_demand_reactive_auto_scaling.html)
- [Amazon EC2 Auto Scaling User Guide](https://docs.aws.amazon.com/autoscaling/ec2/userguide/)
- [Elastic Load Balancing User Guide](https://docs.aws.amazon.com/elasticloadbalancing/latest/userguide/)
- [Amazon Route 53 Developer Guide](https://docs.aws.amazon.com/route53/latest/developerguide/)
- [Amazon CloudWatch User Guide](https://docs.aws.amazon.com/cloudwatch/latest/monitoring/)
- [AWS Lambda Developer Guide](https://docs.aws.amazon.com/lambda/latest/dg/)
- [AWS Systems Manager User Guide](https://docs.aws.amazon.com/systems-manager/latest/userguide/)
- [Amazon RDS User Guide](https://docs.aws.amazon.com/rds/latest/userguide/)
- [AWS Step Functions Developer Guide](https://docs.aws.amazon.com/step-functions/latest/dg/)
- [AWS Builders' Library - Implementing Health Checks](https://aws.amazon.com/builders-library/implementing-health-checks/)
- [Disaster Recovery Strategies](https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-options-in-the-cloud.html)
