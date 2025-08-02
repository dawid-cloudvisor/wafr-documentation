---
title: REL07-BP01 - Use auto scaling or on-demand resources
layout: default
parent: REL07 - How do you design your workload to adapt to changes in demand?
grand_parent: Reliability
nav_order: 1
---

# REL07-BP01: Use auto scaling or on-demand resources

## Overview

Implement automatic scaling mechanisms and on-demand resource provisioning to dynamically adjust capacity based on actual demand. This approach ensures optimal performance during peak periods while minimizing costs during low-demand periods through intelligent resource management.

## Implementation Steps

### 1. Design Auto Scaling Architecture
- Analyze workload patterns and scaling requirements
- Choose appropriate scaling strategies (horizontal vs vertical)
- Design scaling policies based on metrics and thresholds
- Implement predictive scaling for known patterns

### 2. Configure Auto Scaling Groups and Policies
- Set up Auto Scaling Groups with appropriate instance types
- Configure scaling policies with proper cooldown periods
- Implement target tracking and step scaling policies
- Establish minimum, maximum, and desired capacity limits

### 3. Implement Application-Level Scaling
- Design applications to support horizontal scaling
- Implement stateless application architecture
- Configure load balancing and service discovery
- Establish database scaling and connection pooling

### 4. Set Up Monitoring and Alerting
- Configure CloudWatch metrics for scaling decisions
- Implement custom metrics for application-specific scaling
- Set up alarms and notifications for scaling events
- Monitor scaling performance and cost optimization

### 5. Optimize Scaling Performance
- Fine-tune scaling policies and thresholds
- Implement warm-up periods and health checks
- Optimize instance launch times and configurations
- Establish cost optimization strategies

### 6. Test and Validate Scaling Behavior
- Conduct load testing to validate scaling performance
- Test scaling under various demand scenarios
- Validate cost optimization and resource utilization
- Implement continuous monitoring and improvement

## Implementation Examples

### Example 1: Comprehensive Auto Scaling System
```python
import boto3
import json
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

class ScalingType(Enum):
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"
    PREDICTIVE = "predictive"
    REACTIVE = "reactive"

class ScalingDirection(Enum):
    SCALE_OUT = "scale_out"
    SCALE_IN = "scale_in"
    SCALE_UP = "scale_up"
    SCALE_DOWN = "scale_down"

@dataclass
class ScalingPolicy:
    policy_name: str
    scaling_type: ScalingType
    metric_name: str
    threshold: float
    comparison_operator: str
    scaling_adjustment: int
    cooldown_period: int
    enabled: bool

@dataclass
class AutoScalingGroup:
    asg_name: str
    min_size: int
    max_size: int
    desired_capacity: int
    instance_type: str
    availability_zones: List[str]
    scaling_policies: List[ScalingPolicy]
    health_check_type: str
    health_check_grace_period: int

class AutoScalingManager:
    """Comprehensive auto scaling management system"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
        # AWS clients
        self.autoscaling = boto3.client('autoscaling')
        self.ec2 = boto3.client('ec2')
        self.cloudwatch = boto3.client('cloudwatch')
        self.elbv2 = boto3.client('elbv2')
        self.lambda_client = boto3.client('lambda')
        
        # Scaling configuration
        self.scaling_groups = {}
        self.scaling_metrics = {}
        
    async def create_auto_scaling_group(self, asg_config: AutoScalingGroup) -> bool:
        """Create and configure Auto Scaling Group"""
        try:
            # Create launch template
            launch_template_id = await self._create_launch_template(asg_config)
            
            # Create Auto Scaling Group
            self.autoscaling.create_auto_scaling_group(
                AutoScalingGroupName=asg_config.asg_name,
                LaunchTemplate={
                    'LaunchTemplateId': launch_template_id,
                    'Version': '$Latest'
                },
                MinSize=asg_config.min_size,
                MaxSize=asg_config.max_size,
                DesiredCapacity=asg_config.desired_capacity,
                AvailabilityZones=asg_config.availability_zones,
                HealthCheckType=asg_config.health_check_type,
                HealthCheckGracePeriod=asg_config.health_check_grace_period,
                Tags=[
                    {
                        'Key': 'Name',
                        'Value': asg_config.asg_name,
                        'PropagateAtLaunch': True,
                        'ResourceId': asg_config.asg_name,
                        'ResourceType': 'auto-scaling-group'
                    }
                ]
            )
            
            # Create scaling policies
            for policy in asg_config.scaling_policies:
                await self._create_scaling_policy(asg_config.asg_name, policy)
            
            self.scaling_groups[asg_config.asg_name] = asg_config
            
            logging.info(f"Created Auto Scaling Group: {asg_config.asg_name}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to create Auto Scaling Group: {str(e)}")
            return False
    
    async def _create_launch_template(self, asg_config: AutoScalingGroup) -> str:
        """Create launch template for Auto Scaling Group"""
        try:
            template_name = f"{asg_config.asg_name}-template"
            
            # Get latest AMI
            ami_response = self.ec2.describe_images(
                Owners=['amazon'],
                Filters=[
                    {'Name': 'name', 'Values': ['amzn2-ami-hvm-*']},
                    {'Name': 'architecture', 'Values': ['x86_64']},
                    {'Name': 'state', 'Values': ['available']}
                ]
            )
            
            latest_ami = sorted(ami_response['Images'], 
                              key=lambda x: x['CreationDate'], reverse=True)[0]
            
            # Create launch template
            response = self.ec2.create_launch_template(
                LaunchTemplateName=template_name,
                LaunchTemplateData={
                    'ImageId': latest_ami['ImageId'],
                    'InstanceType': asg_config.instance_type,
                    'SecurityGroupIds': self.config.get('security_group_ids', []),
                    'IamInstanceProfile': {
                        'Name': self.config.get('instance_profile', 'EC2-SSM-Role')
                    },
                    'UserData': self._get_user_data_script(),
                    'Monitoring': {'Enabled': True},
                    'TagSpecifications': [
                        {
                            'ResourceType': 'instance',
                            'Tags': [
                                {'Key': 'Name', 'Value': f"{asg_config.asg_name}-instance"},
                                {'Key': 'AutoScalingGroup', 'Value': asg_config.asg_name}
                            ]
                        }
                    ]
                }
            )
            
            return response['LaunchTemplate']['LaunchTemplateId']
            
        except Exception as e:
            logging.error(f"Failed to create launch template: {str(e)}")
            raise
    
    def _get_user_data_script(self) -> str:
        """Get user data script for instance initialization"""
        return """#!/bin/bash
yum update -y
yum install -y amazon-cloudwatch-agent
yum install -y aws-cli

# Install application dependencies
yum install -y python3 python3-pip
pip3 install flask gunicorn boto3

# Configure CloudWatch agent
cat > /opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json << 'EOF'
{
    "metrics": {
        "namespace": "CustomApp/Metrics",
        "metrics_collected": {
            "cpu": {
                "measurement": ["cpu_usage_idle", "cpu_usage_iowait", "cpu_usage_user", "cpu_usage_system"],
                "metrics_collection_interval": 60
            },
            "disk": {
                "measurement": ["used_percent"],
                "metrics_collection_interval": 60,
                "resources": ["*"]
            },
            "mem": {
                "measurement": ["mem_used_percent"],
                "metrics_collection_interval": 60
            }
        }
    }
}
EOF

# Start CloudWatch agent
/opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
    -a fetch-config -m ec2 -c file:/opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json -s

# Start application
systemctl enable amazon-cloudwatch-agent
systemctl start amazon-cloudwatch-agent
"""
    
    async def _create_scaling_policy(self, asg_name: str, policy: ScalingPolicy) -> str:
        """Create scaling policy for Auto Scaling Group"""
        try:
            # Create scaling policy
            policy_response = self.autoscaling.put_scaling_policy(
                AutoScalingGroupName=asg_name,
                PolicyName=policy.policy_name,
                PolicyType='TargetTrackingScaling' if policy.scaling_type == ScalingType.REACTIVE else 'StepScaling',
                AdjustmentType='ChangeInCapacity',
                ScalingAdjustment=policy.scaling_adjustment,
                Cooldown=policy.cooldown_period,
                Enabled=policy.enabled
            )
            
            policy_arn = policy_response['PolicyARN']
            
            # Create CloudWatch alarm
            alarm_name = f"{asg_name}-{policy.policy_name}-alarm"
            
            self.cloudwatch.put_metric_alarm(
                AlarmName=alarm_name,
                ComparisonOperator=policy.comparison_operator,
                EvaluationPeriods=2,
                MetricName=policy.metric_name,
                Namespace='AWS/EC2',
                Period=300,
                Statistic='Average',
                Threshold=policy.threshold,
                ActionsEnabled=True,
                AlarmActions=[policy_arn],
                AlarmDescription=f'Scaling alarm for {asg_name}',
                Dimensions=[
                    {
                        'Name': 'AutoScalingGroupName',
                        'Value': asg_name
                    }
                ]
            )
            
            logging.info(f"Created scaling policy: {policy.policy_name}")
            return policy_arn
            
        except Exception as e:
            logging.error(f"Failed to create scaling policy: {str(e)}")
            raise
    
    async def implement_predictive_scaling(self, asg_name: str, historical_data: List[Dict[str, Any]]) -> bool:
        """Implement predictive scaling based on historical patterns"""
        try:
            # Analyze historical patterns
            patterns = self._analyze_demand_patterns(historical_data)
            
            # Create scheduled scaling actions
            for pattern in patterns:
                await self._create_scheduled_action(asg_name, pattern)
            
            logging.info(f"Implemented predictive scaling for {asg_name}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to implement predictive scaling: {str(e)}")
            return False
    
    def _analyze_demand_patterns(self, historical_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze historical data to identify demand patterns"""
        patterns = []
        
        try:
            # Group data by hour of day and day of week
            hourly_patterns = {}
            daily_patterns = {}
            
            for data_point in historical_data:
                timestamp = datetime.fromisoformat(data_point['timestamp'])
                hour = timestamp.hour
                day_of_week = timestamp.weekday()
                demand = data_point['demand']
                
                if hour not in hourly_patterns:
                    hourly_patterns[hour] = []
                hourly_patterns[hour].append(demand)
                
                if day_of_week not in daily_patterns:
                    daily_patterns[day_of_week] = []
                daily_patterns[day_of_week].append(demand)
            
            # Calculate average demand for each hour
            for hour, demands in hourly_patterns.items():
                avg_demand = sum(demands) / len(demands)
                if avg_demand > self.config.get('scale_out_threshold', 70):
                    patterns.append({
                        'type': 'hourly',
                        'hour': hour,
                        'expected_demand': avg_demand,
                        'action': 'scale_out',
                        'capacity_adjustment': int(avg_demand / 50)  # Simple calculation
                    })
            
            return patterns
            
        except Exception as e:
            logging.error(f"Failed to analyze demand patterns: {str(e)}")
            return []
    
    async def _create_scheduled_action(self, asg_name: str, pattern: Dict[str, Any]) -> bool:
        """Create scheduled scaling action"""
        try:
            action_name = f"{asg_name}-scheduled-{pattern['type']}-{pattern.get('hour', 'daily')}"
            
            # Calculate recurrence pattern
            if pattern['type'] == 'hourly':
                recurrence = f"0 {pattern['hour']} * * *"  # Daily at specific hour
            else:
                recurrence = "0 8 * * 1-5"  # Default: weekdays at 8 AM
            
            self.autoscaling.put_scheduled_update_group_action(
                AutoScalingGroupName=asg_name,
                ScheduledActionName=action_name,
                Recurrence=recurrence,
                DesiredCapacity=pattern.get('capacity_adjustment', 2)
            )
            
            logging.info(f"Created scheduled action: {action_name}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to create scheduled action: {str(e)}")
            return False
    
    async def monitor_scaling_performance(self, asg_name: str) -> Dict[str, Any]:
        """Monitor Auto Scaling Group performance"""
        try:
            # Get Auto Scaling Group details
            asg_response = self.autoscaling.describe_auto_scaling_groups(
                AutoScalingGroupNames=[asg_name]
            )
            
            if not asg_response['AutoScalingGroups']:
                return {'error': f'Auto Scaling Group {asg_name} not found'}
            
            asg = asg_response['AutoScalingGroups'][0]
            
            # Get scaling activities
            activities_response = self.autoscaling.describe_scaling_activities(
                AutoScalingGroupName=asg_name,
                MaxRecords=10
            )
            
            # Get CloudWatch metrics
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(hours=24)
            
            metrics_response = self.cloudwatch.get_metric_statistics(
                Namespace='AWS/AutoScaling',
                MetricName='GroupDesiredCapacity',
                Dimensions=[
                    {
                        'Name': 'AutoScalingGroupName',
                        'Value': asg_name
                    }
                ],
                StartTime=start_time,
                EndTime=end_time,
                Period=3600,
                Statistics=['Average', 'Maximum', 'Minimum']
            )
            
            # Calculate performance metrics
            performance_data = {
                'asg_name': asg_name,
                'current_capacity': asg['DesiredCapacity'],
                'min_size': asg['MinSize'],
                'max_size': asg['MaxSize'],
                'instance_count': len(asg['Instances']),
                'healthy_instances': len([i for i in asg['Instances'] if i['HealthStatus'] == 'Healthy']),
                'recent_activities': [
                    {
                        'activity_id': activity['ActivityId'],
                        'description': activity['Description'],
                        'status': activity['StatusCode'],
                        'start_time': activity['StartTime'].isoformat(),
                        'end_time': activity.get('EndTime', datetime.utcnow()).isoformat()
                    }
                    for activity in activities_response['Activities']
                ],
                'capacity_metrics': [
                    {
                        'timestamp': dp['Timestamp'].isoformat(),
                        'average': dp['Average'],
                        'maximum': dp['Maximum'],
                        'minimum': dp['Minimum']
                    }
                    for dp in metrics_response['Datapoints']
                ]
            }
            
            return performance_data
            
        except Exception as e:
            logging.error(f"Failed to monitor scaling performance: {str(e)}")
            return {'error': str(e)}
    
    async def optimize_scaling_costs(self, asg_name: str) -> Dict[str, Any]:
        """Optimize Auto Scaling Group for cost efficiency"""
        try:
            recommendations = []
            
            # Get current configuration
            asg_response = self.autoscaling.describe_auto_scaling_groups(
                AutoScalingGroupNames=[asg_name]
            )
            
            if not asg_response['AutoScalingGroups']:
                return {'error': f'Auto Scaling Group {asg_name} not found'}
            
            asg = asg_response['AutoScalingGroups'][0]
            
            # Analyze utilization patterns
            utilization_data = await self._get_utilization_metrics(asg_name)
            
            # Generate cost optimization recommendations
            if utilization_data['average_cpu'] < 30:
                recommendations.append({
                    'type': 'instance_type',
                    'description': 'Consider using smaller instance types due to low CPU utilization',
                    'current_utilization': utilization_data['average_cpu'],
                    'potential_savings': '20-40%'
                })
            
            if utilization_data['peak_hours'] < 8:
                recommendations.append({
                    'type': 'scheduling',
                    'description': 'Implement scheduled scaling to reduce capacity during off-peak hours',
                    'peak_hours': utilization_data['peak_hours'],
                    'potential_savings': '15-30%'
                })
            
            # Check for Spot Instance opportunities
            if not self._uses_spot_instances(asg):
                recommendations.append({
                    'type': 'spot_instances',
                    'description': 'Consider using Spot Instances for cost savings',
                    'potential_savings': '50-90%'
                })
            
            return {
                'asg_name': asg_name,
                'current_cost_estimate': await self._estimate_monthly_cost(asg),
                'recommendations': recommendations,
                'utilization_data': utilization_data
            }
            
        except Exception as e:
            logging.error(f"Failed to optimize scaling costs: {str(e)}")
            return {'error': str(e)}
    
    async def _get_utilization_metrics(self, asg_name: str) -> Dict[str, Any]:
        """Get utilization metrics for cost optimization"""
        try:
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(days=7)
            
            # Get CPU utilization
            cpu_response = self.cloudwatch.get_metric_statistics(
                Namespace='AWS/EC2',
                MetricName='CPUUtilization',
                Dimensions=[
                    {
                        'Name': 'AutoScalingGroupName',
                        'Value': asg_name
                    }
                ],
                StartTime=start_time,
                EndTime=end_time,
                Period=3600,
                Statistics=['Average']
            )
            
            cpu_values = [dp['Average'] for dp in cpu_response['Datapoints']]
            average_cpu = sum(cpu_values) / len(cpu_values) if cpu_values else 0
            
            # Calculate peak hours (CPU > 50%)
            peak_hours = len([cpu for cpu in cpu_values if cpu > 50])
            
            return {
                'average_cpu': average_cpu,
                'peak_hours': peak_hours,
                'total_hours': len(cpu_values)
            }
            
        except Exception as e:
            logging.error(f"Failed to get utilization metrics: {str(e)}")
            return {'average_cpu': 0, 'peak_hours': 0, 'total_hours': 0}
    
    def _uses_spot_instances(self, asg: Dict[str, Any]) -> bool:
        """Check if Auto Scaling Group uses Spot Instances"""
        # This is a simplified check - in reality, you'd check the launch template
        return False
    
    async def _estimate_monthly_cost(self, asg: Dict[str, Any]) -> float:
        """Estimate monthly cost for Auto Scaling Group"""
        # Simplified cost calculation
        instance_count = asg['DesiredCapacity']
        # Assuming t3.medium at $0.0416/hour
        hourly_cost = instance_count * 0.0416
        monthly_cost = hourly_cost * 24 * 30
        return round(monthly_cost, 2)

# Usage example
async def main():
    config = {
        'security_group_ids': ['sg-12345678'],
        'instance_profile': 'EC2-SSM-Role',
        'scale_out_threshold': 70
    }
    
    # Initialize auto scaling manager
    scaling_manager = AutoScalingManager(config)
    
    # Create Auto Scaling Group configuration
    asg_config = AutoScalingGroup(
        asg_name='web-app-asg',
        min_size=2,
        max_size=10,
        desired_capacity=3,
        instance_type='t3.medium',
        availability_zones=['us-east-1a', 'us-east-1b', 'us-east-1c'],
        scaling_policies=[
            ScalingPolicy(
                policy_name='scale-out-cpu',
                scaling_type=ScalingType.REACTIVE,
                metric_name='CPUUtilization',
                threshold=70.0,
                comparison_operator='GreaterThanThreshold',
                scaling_adjustment=2,
                cooldown_period=300,
                enabled=True
            ),
            ScalingPolicy(
                policy_name='scale-in-cpu',
                scaling_type=ScalingType.REACTIVE,
                metric_name='CPUUtilization',
                threshold=30.0,
                comparison_operator='LessThanThreshold',
                scaling_adjustment=-1,
                cooldown_period=300,
                enabled=True
            )
        ],
        health_check_type='ELB',
        health_check_grace_period=300
    )
    
    # Create Auto Scaling Group
    success = await scaling_manager.create_auto_scaling_group(asg_config)
    if success:
        print(f"Successfully created Auto Scaling Group: {asg_config.asg_name}")
        
        # Monitor performance
        performance = await scaling_manager.monitor_scaling_performance(asg_config.asg_name)
        print(f"Current capacity: {performance.get('current_capacity', 'N/A')}")
        
        # Get cost optimization recommendations
        cost_optimization = await scaling_manager.optimize_scaling_costs(asg_config.asg_name)
        print(f"Estimated monthly cost: ${cost_optimization.get('current_cost_estimate', 'N/A')}")
        print(f"Optimization recommendations: {len(cost_optimization.get('recommendations', []))}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## AWS Services Used

- **Amazon EC2 Auto Scaling**: Automatic scaling of EC2 instances based on demand and policies
- **AWS Auto Scaling**: Unified scaling across multiple AWS services and resources
- **AWS Lambda**: Serverless compute that automatically scales with demand
- **Amazon ECS Service Auto Scaling**: Container-based application scaling with task management
- **Amazon EKS Cluster Autoscaler**: Kubernetes node scaling and pod scheduling
- **AWS Fargate**: Serverless containers with automatic capacity management
- **Elastic Load Balancing**: Traffic distribution and health-based scaling triggers
- **Amazon CloudWatch**: Metrics collection, alarms, and scaling decision triggers
- **Amazon DynamoDB**: On-demand scaling for NoSQL database workloads
- **Amazon API Gateway**: Managed API service with automatic scaling capabilities
- **AWS Application Auto Scaling**: Scaling for various AWS services beyond EC2
- **Amazon CloudFront**: Global content delivery with edge location scaling
- **AWS Batch**: Dynamic compute environment scaling for batch workloads
- **Amazon EMR**: Managed cluster scaling for big data processing
- **Amazon RDS**: Database scaling with read replicas and storage auto scaling

## Benefits

- **Cost Optimization**: Pay only for resources actually needed, reducing over-provisioning costs
- **Performance Consistency**: Maintain optimal performance during varying demand periods
- **Operational Efficiency**: Reduce manual intervention through automated scaling decisions
- **High Availability**: Distribute load across multiple instances and availability zones
- **Rapid Response**: Quickly adapt to sudden changes in demand or traffic spikes
- **Resource Utilization**: Optimize resource usage through intelligent scaling algorithms
- **Predictable Scaling**: Use historical data to anticipate and prepare for demand changes
- **Fault Tolerance**: Replace unhealthy instances automatically to maintain capacity
- **Global Reach**: Scale across multiple regions and availability zones as needed
- **Application Agnostic**: Support various application types and architectures

## Related Resources

- [AWS Well-Architected Reliability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/)
- [Use Auto Scaling or On-Demand Resources](https://docs.aws.amazon.com/wellarchitected/latest/framework/rel_adapt_to_changes_in_demand_autoscaling_ondemand.html)
- [Amazon EC2 Auto Scaling User Guide](https://docs.aws.amazon.com/autoscaling/ec2/userguide/)
- [AWS Auto Scaling User Guide](https://docs.aws.amazon.com/autoscaling/application/userguide/)
- [AWS Lambda Developer Guide](https://docs.aws.amazon.com/lambda/latest/dg/)
- [Amazon ECS Service Auto Scaling](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service-auto-scaling.html)
- [Amazon EKS Cluster Autoscaler](https://docs.aws.amazon.com/eks/latest/userguide/cluster-autoscaler.html)
- [AWS Fargate User Guide](https://docs.aws.amazon.com/AmazonECS/latest/userguide/what-is-fargate.html)
- [Elastic Load Balancing User Guide](https://docs.aws.amazon.com/elasticloadbalancing/latest/userguide/)
- [Amazon CloudWatch User Guide](https://docs.aws.amazon.com/cloudwatch/latest/monitoring/)
- [Auto Scaling Best Practices](https://docs.aws.amazon.com/autoscaling/ec2/userguide/auto-scaling-benefits.html)
- [AWS Builders' Library - Load Balancing](https://aws.amazon.com/builders-library/using-load-balancing-to-avoid-overload/)
