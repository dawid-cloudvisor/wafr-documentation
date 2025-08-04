---
title: REL11-BP02 - Fail over to healthy resources
layout: default
parent: REL11 - How do you design your workload to withstand component failures?
nav_order: 2
---

# REL11-BP02: Fail over to healthy resources

Automatic failover mechanisms ensure that when failures are detected, traffic and workloads are seamlessly redirected to healthy resources. This includes both planned failover for maintenance and unplanned failover for unexpected failures, maintaining service availability while failed components are recovered.

## Implementation Steps

### 1. Health Check Configuration
Implement comprehensive health checks that accurately determine resource health status.

### 2. Automatic Failover Logic
Design failover mechanisms that can make decisions without human intervention.

### 3. Traffic Routing
Configure intelligent traffic routing to direct requests to healthy resources.

### 4. State Management
Ensure application state is properly managed during failover scenarios.

### 5. Failback Procedures
Implement automated failback when failed resources are restored to healthy state.

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
from concurrent.futures import ThreadPoolExecutor, as_completed

class FailoverType(Enum):
    PLANNED = "planned"
    UNPLANNED = "unplanned"
    AUTOMATIC = "automatic"
    MANUAL = "manual"

class ResourceHealth(Enum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    DEGRADED = "degraded"
    UNKNOWN = "unknown"

class FailoverStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"

@dataclass
class HealthCheck:
    name: str
    endpoint: str
    method: str
    expected_status: int
    timeout: int
    interval: int
    healthy_threshold: int
    unhealthy_threshold: int
    path: str = "/"
    port: int = 80

@dataclass
class FailoverTarget:
    resource_id: str
    resource_type: str
    region: str
    availability_zone: str
    capacity: int
    priority: int
    health_status: ResourceHealth
    last_health_check: datetime

@dataclass
class FailoverEvent:
    event_id: str
    source_resource: str
    target_resource: str
    failover_type: FailoverType
    status: FailoverStatus
    start_time: datetime
    end_time: Optional[datetime]
    reason: str
    rollback_plan: Dict[str, Any]

class AutomaticFailoverSystem:
    def __init__(self, region: str = 'us-east-1'):
        self.region = region
        self.ec2 = boto3.client('ec2', region_name=region)
        self.elb = boto3.client('elbv2', region_name=region)
        self.route53 = boto3.client('route53')
        self.rds = boto3.client('rds', region_name=region)
        self.asg = boto3.client('autoscaling', region_name=region)
        self.cloudwatch = boto3.client('cloudwatch', region_name=region)
        self.sns = boto3.client('sns', region_name=region)
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Failover state tracking
        self.active_failovers: Dict[str, FailoverEvent] = {}
        self.health_check_results: Dict[str, ResourceHealth] = {}
        self.failover_lock = threading.Lock()

    def setup_load_balancer_failover(self, lb_config: Dict[str, Any]) -> Dict[str, Any]:
        """Set up automatic failover for load balancers"""
        try:
            lb_arn = lb_config['load_balancer_arn']
            target_groups = lb_config['target_groups']
            
            failover_config = {
                'load_balancer_arn': lb_arn,
                'primary_targets': [],
                'secondary_targets': [],
                'health_checks': []
            }
            
            for tg_config in target_groups:
                tg_arn = tg_config['target_group_arn']
                
                # Configure health check
                health_check = HealthCheck(
                    name=f"tg-{tg_arn.split('/')[-1]}",
                    endpoint=tg_config.get('health_check_path', '/health'),
                    method='GET',
                    expected_status=200,
                    timeout=tg_config.get('health_check_timeout', 5),
                    interval=tg_config.get('health_check_interval', 30),
                    healthy_threshold=tg_config.get('healthy_threshold', 2),
                    unhealthy_threshold=tg_config.get('unhealthy_threshold', 2),
                    port=tg_config.get('health_check_port', 80)
                )
                
                # Update target group health check settings
                self.elb.modify_target_group(
                    TargetGroupArn=tg_arn,
                    HealthCheckProtocol='HTTP',
                    HealthCheckPath=health_check.path,
                    HealthCheckIntervalSeconds=health_check.interval,
                    HealthCheckTimeoutSeconds=health_check.timeout,
                    HealthyThresholdCount=health_check.healthy_threshold,
                    UnhealthyThresholdCount=health_check.unhealthy_threshold,
                    HealthCheckPort=str(health_check.port)
                )
                
                failover_config['health_checks'].append(asdict(health_check))
                
                # Categorize targets by priority
                if tg_config.get('priority', 1) == 1:
                    failover_config['primary_targets'].append(tg_arn)
                else:
                    failover_config['secondary_targets'].append(tg_arn)
            
            # Set up CloudWatch alarms for automatic failover
            self._setup_failover_alarms(lb_arn, failover_config)
            
            self.logger.info(f"Load balancer failover configured for {lb_arn}")
            return failover_config
            
        except Exception as e:
            self.logger.error(f"Load balancer failover setup failed: {str(e)}")
            return {}

    def setup_dns_failover(self, dns_config: Dict[str, Any]) -> Dict[str, Any]:
        """Set up DNS-based failover with Route 53"""
        try:
            hosted_zone_id = dns_config['hosted_zone_id']
            record_name = dns_config['record_name']
            primary_endpoint = dns_config['primary_endpoint']
            secondary_endpoint = dns_config['secondary_endpoint']
            
            # Create health checks
            primary_health_check = self.route53.create_health_check(
                Type='HTTPS',
                ResourcePath=dns_config.get('health_check_path', '/health'),
                FullyQualifiedDomainName=primary_endpoint,
                Port=dns_config.get('port', 443),
                RequestInterval=30,
                FailureThreshold=3
            )
            
            secondary_health_check = self.route53.create_health_check(
                Type='HTTPS',
                ResourcePath=dns_config.get('health_check_path', '/health'),
                FullyQualifiedDomainName=secondary_endpoint,
                Port=dns_config.get('port', 443),
                RequestInterval=30,
                FailureThreshold=3
            )
            
            # Create primary record with failover routing
            primary_record = self.route53.change_resource_record_sets(
                HostedZoneId=hosted_zone_id,
                ChangeBatch={
                    'Changes': [{
                        'Action': 'UPSERT',
                        'ResourceRecordSet': {
                            'Name': record_name,
                            'Type': 'A',
                            'SetIdentifier': 'primary',
                            'Failover': 'PRIMARY',
                            'TTL': 60,
                            'ResourceRecords': [{'Value': primary_endpoint}],
                            'HealthCheckId': primary_health_check['HealthCheck']['Id']
                        }
                    }]
                }
            )
            
            # Create secondary record with failover routing
            secondary_record = self.route53.change_resource_record_sets(
                HostedZoneId=hosted_zone_id,
                ChangeBatch={
                    'Changes': [{
                        'Action': 'UPSERT',
                        'ResourceRecordSet': {
                            'Name': record_name,
                            'Type': 'A',
                            'SetIdentifier': 'secondary',
                            'Failover': 'SECONDARY',
                            'TTL': 60,
                            'ResourceRecords': [{'Value': secondary_endpoint}]
                        }
                    }]
                }
            )
            
            failover_config = {
                'hosted_zone_id': hosted_zone_id,
                'record_name': record_name,
                'primary_endpoint': primary_endpoint,
                'secondary_endpoint': secondary_endpoint,
                'primary_health_check_id': primary_health_check['HealthCheck']['Id'],
                'secondary_health_check_id': secondary_health_check['HealthCheck']['Id']
            }
            
            self.logger.info(f"DNS failover configured for {record_name}")
            return failover_config
            
        except Exception as e:
            self.logger.error(f"DNS failover setup failed: {str(e)}")
            return {}

    def setup_database_failover(self, db_config: Dict[str, Any]) -> Dict[str, Any]:
        """Set up database failover with RDS Multi-AZ"""
        try:
            db_instance_id = db_config['db_instance_identifier']
            
            # Enable Multi-AZ deployment
            self.rds.modify_db_instance(
                DBInstanceIdentifier=db_instance_id,
                MultiAZ=True,
                ApplyImmediately=db_config.get('apply_immediately', False)
            )
            
            # Create read replicas for additional failover options
            read_replicas = []
            for replica_config in db_config.get('read_replicas', []):
                replica_response = self.rds.create_db_instance_read_replica(
                    DBInstanceIdentifier=replica_config['identifier'],
                    SourceDBInstanceIdentifier=db_instance_id,
                    DBInstanceClass=replica_config.get('instance_class', 'db.t3.micro'),
                    AvailabilityZone=replica_config.get('availability_zone'),
                    MultiAZ=replica_config.get('multi_az', False),
                    PubliclyAccessible=False,
                    AutoMinorVersionUpgrade=True,
                    Tags=[
                        {'Key': 'Purpose', 'Value': 'ReadReplica'},
                        {'Key': 'SourceDB', 'Value': db_instance_id}
                    ]
                )
                read_replicas.append(replica_response['DBInstance']['DBInstanceIdentifier'])
            
            # Set up CloudWatch alarms for database health
            self._setup_database_failover_alarms(db_instance_id)
            
            failover_config = {
                'primary_db': db_instance_id,
                'multi_az_enabled': True,
                'read_replicas': read_replicas,
                'failover_type': 'automatic'
            }
            
            self.logger.info(f"Database failover configured for {db_instance_id}")
            return failover_config
            
        except Exception as e:
            self.logger.error(f"Database failover setup failed: {str(e)}")
            return {}

    def setup_auto_scaling_failover(self, asg_config: Dict[str, Any]) -> Dict[str, Any]:
        """Set up Auto Scaling Group failover across AZs"""
        try:
            asg_name = asg_config['auto_scaling_group_name']
            
            # Update ASG to span multiple AZs
            self.asg.update_auto_scaling_group(
                AutoScalingGroupName=asg_name,
                AvailabilityZones=asg_config['availability_zones'],
                HealthCheckType='ELB',
                HealthCheckGracePeriod=asg_config.get('health_check_grace_period', 300),
                DefaultCooldown=asg_config.get('cooldown', 300)
            )
            
            # Create scaling policies for failover scenarios
            scale_up_policy = self.asg.put_scaling_policy(
                AutoScalingGroupName=asg_name,
                PolicyName=f"{asg_name}-failover-scale-up",
                PolicyType='StepScaling',
                AdjustmentType='ChangeInCapacity',
                StepAdjustments=[
                    {
                        'MetricIntervalLowerBound': 0,
                        'ScalingAdjustment': asg_config.get('failover_scale_amount', 2)
                    }
                ],
                Cooldown=60
            )
            
            # Set up CloudWatch alarms for ASG health
            self._setup_asg_failover_alarms(asg_name, scale_up_policy['PolicyARN'])
            
            failover_config = {
                'auto_scaling_group': asg_name,
                'availability_zones': asg_config['availability_zones'],
                'health_check_type': 'ELB',
                'scale_up_policy_arn': scale_up_policy['PolicyARN']
            }
            
            self.logger.info(f"Auto Scaling failover configured for {asg_name}")
            return failover_config
            
        except Exception as e:
            self.logger.error(f"Auto Scaling failover setup failed: {str(e)}")
            return {}

    def execute_manual_failover(self, failover_request: Dict[str, Any]) -> FailoverEvent:
        """Execute manual failover operation"""
        event_id = f"failover-{int(time.time())}"
        
        try:
            with self.failover_lock:
                failover_event = FailoverEvent(
                    event_id=event_id,
                    source_resource=failover_request['source_resource'],
                    target_resource=failover_request['target_resource'],
                    failover_type=FailoverType.MANUAL,
                    status=FailoverStatus.PENDING,
                    start_time=datetime.utcnow(),
                    end_time=None,
                    reason=failover_request.get('reason', 'Manual failover requested'),
                    rollback_plan=failover_request.get('rollback_plan', {})
                )
                
                self.active_failovers[event_id] = failover_event
            
            # Update status to in progress
            failover_event.status = FailoverStatus.IN_PROGRESS
            
            # Execute failover based on resource type
            resource_type = failover_request['resource_type']
            
            if resource_type == 'load_balancer':
                success = self._execute_lb_failover(failover_request)
            elif resource_type == 'database':
                success = self._execute_db_failover(failover_request)
            elif resource_type == 'dns':
                success = self._execute_dns_failover(failover_request)
            elif resource_type == 'auto_scaling':
                success = self._execute_asg_failover(failover_request)
            else:
                raise ValueError(f"Unsupported resource type: {resource_type}")
            
            # Update final status
            failover_event.status = FailoverStatus.COMPLETED if success else FailoverStatus.FAILED
            failover_event.end_time = datetime.utcnow()
            
            # Send notification
            self._send_failover_notification(failover_event)
            
            self.logger.info(f"Manual failover {event_id} completed with status: {failover_event.status}")
            return failover_event
            
        except Exception as e:
            failover_event.status = FailoverStatus.FAILED
            failover_event.end_time = datetime.utcnow()
            self.logger.error(f"Manual failover {event_id} failed: {str(e)}")
            return failover_event

    def monitor_health_and_failover(self, monitoring_config: Dict[str, Any]) -> None:
        """Continuously monitor health and trigger automatic failover"""
        try:
            while True:
                with ThreadPoolExecutor(max_workers=10) as executor:
                    # Submit health check tasks
                    health_check_futures = []
                    
                    for resource_config in monitoring_config['resources']:
                        future = executor.submit(
                            self._perform_health_check,
                            resource_config
                        )
                        health_check_futures.append((future, resource_config))
                    
                    # Process health check results
                    for future, resource_config in health_check_futures:
                        try:
                            health_status = future.result(timeout=30)
                            resource_id = resource_config['resource_id']
                            
                            # Update health status
                            previous_status = self.health_check_results.get(resource_id, ResourceHealth.UNKNOWN)
                            self.health_check_results[resource_id] = health_status
                            
                            # Trigger failover if health degraded
                            if (previous_status == ResourceHealth.HEALTHY and 
                                health_status in [ResourceHealth.UNHEALTHY, ResourceHealth.DEGRADED]):
                                
                                self._trigger_automatic_failover(resource_config, health_status)
                                
                        except Exception as e:
                            self.logger.error(f"Health check failed for {resource_config['resource_id']}: {str(e)}")
                
                # Wait before next health check cycle
                time.sleep(monitoring_config.get('check_interval', 60))
                
        except KeyboardInterrupt:
            self.logger.info("Health monitoring stopped")
        except Exception as e:
            self.logger.error(f"Health monitoring error: {str(e)}")

    def _perform_health_check(self, resource_config: Dict[str, Any]) -> ResourceHealth:
        """Perform health check on a resource"""
        try:
            resource_type = resource_config['resource_type']
            
            if resource_type == 'ec2':
                return self._check_ec2_health(resource_config)
            elif resource_type == 'rds':
                return self._check_rds_health(resource_config)
            elif resource_type == 'load_balancer':
                return self._check_lb_health(resource_config)
            elif resource_type == 'endpoint':
                return self._check_endpoint_health(resource_config)
            else:
                return ResourceHealth.UNKNOWN
                
        except Exception as e:
            self.logger.error(f"Health check error: {str(e)}")
            return ResourceHealth.UNKNOWN

    def _check_ec2_health(self, resource_config: Dict[str, Any]) -> ResourceHealth:
        """Check EC2 instance health"""
        try:
            instance_id = resource_config['resource_id']
            
            response = self.ec2.describe_instance_status(
                InstanceIds=[instance_id],
                IncludeAllInstances=True
            )
            
            if not response['InstanceStatuses']:
                return ResourceHealth.UNKNOWN
            
            status = response['InstanceStatuses'][0]
            instance_status = status['InstanceStatus']['Status']
            system_status = status['SystemStatus']['Status']
            
            if instance_status == 'ok' and system_status == 'ok':
                return ResourceHealth.HEALTHY
            elif instance_status == 'impaired' or system_status == 'impaired':
                return ResourceHealth.DEGRADED
            else:
                return ResourceHealth.UNHEALTHY
                
        except Exception as e:
            self.logger.error(f"EC2 health check failed: {str(e)}")
            return ResourceHealth.UNKNOWN

    def _check_rds_health(self, resource_config: Dict[str, Any]) -> ResourceHealth:
        """Check RDS instance health"""
        try:
            db_instance_id = resource_config['resource_id']
            
            response = self.rds.describe_db_instances(
                DBInstanceIdentifier=db_instance_id
            )
            
            db_instance = response['DBInstances'][0]
            status = db_instance['DBInstanceStatus']
            
            if status == 'available':
                return ResourceHealth.HEALTHY
            elif status in ['backing-up', 'modifying', 'upgrading']:
                return ResourceHealth.DEGRADED
            else:
                return ResourceHealth.UNHEALTHY
                
        except Exception as e:
            self.logger.error(f"RDS health check failed: {str(e)}")
            return ResourceHealth.UNKNOWN

    def _trigger_automatic_failover(self, resource_config: Dict[str, Any], health_status: ResourceHealth) -> None:
        """Trigger automatic failover based on health status"""
        try:
            if not resource_config.get('auto_failover_enabled', False):
                return
            
            failover_request = {
                'source_resource': resource_config['resource_id'],
                'target_resource': resource_config.get('failover_target'),
                'resource_type': resource_config['resource_type'],
                'reason': f'Automatic failover triggered due to {health_status.value} status',
                'rollback_plan': resource_config.get('rollback_plan', {})
            }
            
            self.execute_manual_failover(failover_request)
            
        except Exception as e:
            self.logger.error(f"Automatic failover trigger failed: {str(e)}")

    def _setup_failover_alarms(self, lb_arn: str, config: Dict[str, Any]) -> None:
        """Set up CloudWatch alarms for load balancer failover"""
        try:
            # Unhealthy host count alarm
            self.cloudwatch.put_metric_alarm(
                AlarmName=f"LB-UnhealthyHosts-{lb_arn.split('/')[-1]}",
                ComparisonOperator='GreaterThanThreshold',
                EvaluationPeriods=2,
                MetricName='UnHealthyHostCount',
                Namespace='AWS/ApplicationELB',
                Period=300,
                Statistic='Average',
                Threshold=0.0,
                ActionsEnabled=True,
                AlarmActions=[
                    self._get_failover_sns_topic()
                ],
                AlarmDescription='Load balancer has unhealthy targets',
                Dimensions=[
                    {
                        'Name': 'LoadBalancer',
                        'Value': lb_arn.split('/')[-3] + '/' + lb_arn.split('/')[-2] + '/' + lb_arn.split('/')[-1]
                    }
                ]
            )
            
        except Exception as e:
            self.logger.error(f"Failover alarm setup failed: {str(e)}")

    def _get_failover_sns_topic(self) -> str:
        """Get SNS topic ARN for failover notifications"""
        return f"arn:aws:sns:{self.region}:123456789012:failover-notifications"

    def _send_failover_notification(self, failover_event: FailoverEvent) -> None:
        """Send notification about failover event"""
        try:
            message = {
                'event_id': failover_event.event_id,
                'source_resource': failover_event.source_resource,
                'target_resource': failover_event.target_resource,
                'status': failover_event.status.value,
                'reason': failover_event.reason,
                'start_time': failover_event.start_time.isoformat(),
                'end_time': failover_event.end_time.isoformat() if failover_event.end_time else None
            }
            
            self.sns.publish(
                TopicArn=self._get_failover_sns_topic(),
                Message=json.dumps(message, indent=2),
                Subject=f"Failover Event: {failover_event.status.value.title()}"
            )
            
        except Exception as e:
            self.logger.error(f"Failover notification failed: {str(e)}")

# Example usage
def main():
    # Initialize failover system
    failover_system = AutomaticFailoverSystem(region='us-east-1')
    
    # Configure load balancer failover
    lb_config = {
        'load_balancer_arn': 'arn:aws:elasticloadbalancing:us-east-1:123456789012:loadbalancer/app/myapp-alb/1234567890123456',
        'target_groups': [
            {
                'target_group_arn': 'arn:aws:elasticloadbalancing:us-east-1:123456789012:targetgroup/myapp-tg-primary/1234567890123456',
                'priority': 1,
                'health_check_path': '/health',
                'health_check_interval': 30,
                'healthy_threshold': 2,
                'unhealthy_threshold': 2
            },
            {
                'target_group_arn': 'arn:aws:elasticloadbalancing:us-east-1:123456789012:targetgroup/myapp-tg-secondary/1234567890123456',
                'priority': 2,
                'health_check_path': '/health',
                'health_check_interval': 30,
                'healthy_threshold': 2,
                'unhealthy_threshold': 2
            }
        ]
    }
    
    # Configure DNS failover
    dns_config = {
        'hosted_zone_id': 'Z123456789012345678901',
        'record_name': 'api.myapp.com',
        'primary_endpoint': '1.2.3.4',
        'secondary_endpoint': '5.6.7.8',
        'health_check_path': '/health',
        'port': 443
    }
    
    # Configure database failover
    db_config = {
        'db_instance_identifier': 'myapp-prod-db',
        'apply_immediately': False,
        'read_replicas': [
            {
                'identifier': 'myapp-prod-db-replica-1',
                'instance_class': 'db.t3.medium',
                'availability_zone': 'us-east-1b'
            }
        ]
    }
    
    # Set up failover configurations
    print("Setting up failover mechanisms...")
    
    lb_failover = failover_system.setup_load_balancer_failover(lb_config)
    dns_failover = failover_system.setup_dns_failover(dns_config)
    db_failover = failover_system.setup_database_failover(db_config)
    
    print("Failover setup complete:")
    print(f"- Load balancer failover: {len(lb_failover.get('primary_targets', []))} primary targets")
    print(f"- DNS failover: {dns_failover.get('record_name', 'N/A')}")
    print(f"- Database failover: {db_failover.get('primary_db', 'N/A')}")
    
    # Example manual failover
    manual_failover_request = {
        'source_resource': 'i-1234567890abcdef0',
        'target_resource': 'i-0987654321fedcba0',
        'resource_type': 'ec2',
        'reason': 'Planned maintenance',
        'rollback_plan': {
            'auto_rollback': True,
            'rollback_delay': 3600
        }
    }
    
    failover_event = failover_system.execute_manual_failover(manual_failover_request)
    print(f"Manual failover executed: {failover_event.event_id} - Status: {failover_event.status.value}")

if __name__ == "__main__":
    main()
```
{% endraw %}

## AWS Services

### Primary Services
- **Elastic Load Balancing**: Automatic traffic distribution and health checking
- **Amazon Route 53**: DNS-based failover with health checks
- **Amazon RDS Multi-AZ**: Automatic database failover
- **Amazon EC2 Auto Scaling**: Instance-level failover and replacement

### Supporting Services
- **AWS Global Accelerator**: Global traffic management and failover
- **Amazon CloudWatch**: Health monitoring and alarm-based failover triggers
- **Amazon SNS**: Failover event notifications
- **AWS Lambda**: Custom failover logic and automation

## Benefits

- **Automatic Recovery**: Seamless failover without manual intervention
- **Reduced Downtime**: Faster recovery through pre-configured failover paths
- **Multi-Layer Protection**: Failover at DNS, load balancer, and application levels
- **Geographic Distribution**: Cross-region failover capabilities
- **State Preservation**: Maintain application state during failover events

## Related Resources

- [Elastic Load Balancing User Guide](https://docs.aws.amazon.com/elasticloadbalancing/)
- [Amazon Route 53 Developer Guide](https://docs.aws.amazon.com/route53/)
- [Amazon RDS User Guide - Multi-AZ Deployments](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.MultiAZ.html)
- [Amazon EC2 Auto Scaling User Guide](https://docs.aws.amazon.com/autoscaling/ec2/)
