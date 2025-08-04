---
title: COST04-BP01 - Track resources over their lifetime
layout: default
parent: COST04 - How do you decommission resources?
grand_parent: Cost Optimization
nav_order: 1
---

<div class="pillar-header">
  <h1>COST04-BP01: Track resources over their lifetime</h1>
  <p>Implement comprehensive tracking of resources from creation to decommissioning to ensure visibility into resource lifecycle and enable proactive management. Effective tracking prevents resource sprawl and enables timely identification of decommissioning opportunities.</p>
</div>

## Implementation guidance

Resource lifecycle tracking provides the foundation for effective decommissioning by maintaining comprehensive visibility into all resources, their usage patterns, dependencies, and business context throughout their entire lifecycle.

### Tracking Framework Principles

**Comprehensive Coverage**: Track all resources across all accounts, regions, and services to ensure no resources are overlooked during decommissioning activities.

**Lifecycle Visibility**: Maintain visibility into resource status from creation through active use to eventual decommissioning.

**Business Context**: Include business context such as project association, ownership, and purpose to enable informed decommissioning decisions.

**Automated Discovery**: Use automated tools to continuously discover and catalog resources to maintain accurate and up-to-date inventory.

### Resource Tracking Components

**Resource Inventory**: Comprehensive catalog of all resources with metadata including creation date, owner, purpose, and current status.

**Usage Monitoring**: Continuous monitoring of resource utilization patterns to identify underutilized or unused resources.

**Dependency Mapping**: Documentation of resource relationships and dependencies to understand impact of decommissioning decisions.

**Cost Attribution**: Association of costs with resources to enable cost-based decommissioning prioritization.

## AWS Services to Consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Config</h4>
    <p>Automatically discover and track resource configurations and changes. Use Config to maintain comprehensive resource inventory and track configuration drift.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Systems Manager Inventory</h4>
    <p>Collect detailed information about resources and their configurations. Use Systems Manager to gather metadata and track resource attributes.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Resource Groups</h4>
    <p>Organize resources into logical groups for tracking and management. Use resource groups to track related resources and their lifecycle status.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon CloudWatch</h4>
    <p>Monitor resource utilization and performance metrics. Use CloudWatch to track usage patterns and identify decommissioning candidates.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS CloudTrail</h4>
    <p>Track resource creation, modification, and access activities. Use CloudTrail to understand resource usage patterns and ownership.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon DynamoDB</h4>
    <p>Store resource tracking data and metadata. Use DynamoDB for fast access to resource information and lifecycle status.</p>
  </div>
</div>

## Implementation Steps

### 1. Design Tracking Architecture
- Define resource tracking requirements and scope
- Design data model for resource lifecycle information
- Plan integration with existing systems and tools
- Establish data retention and archival policies

### 2. Implement Resource Discovery
- Set up automated resource discovery across all accounts
- Configure resource inventory collection and updates
- Implement resource classification and categorization
- Create resource ownership and accountability frameworks

### 3. Deploy Monitoring Infrastructure
- Set up utilization monitoring for all resource types
- Configure performance and usage metric collection
- Implement dependency discovery and mapping
- Create cost attribution and tracking mechanisms

### 4. Create Tracking Dashboards
- Build comprehensive resource inventory dashboards
- Create lifecycle status and utilization reports
- Implement alerting for tracking anomalies
- Set up automated reporting and notifications

### 5. Establish Governance Processes
- Create resource lifecycle management policies
- Implement ownership and accountability procedures
- Set up regular review and validation processes
- Create audit and compliance reporting capabilities

### 6. Enable Continuous Improvement
- Monitor tracking system effectiveness and accuracy
- Gather feedback from stakeholders and users
- Refine tracking processes based on lessons learned
- Expand tracking coverage to new services and use cases

## Resource Tracking Implementation

### Automated Resource Discovery
```python
import boto3
import json
from datetime import datetime, timedelta

class ResourceTracker:
    def __init__(self):
        self.config = boto3.client('config')
        self.ec2 = boto3.client('ec2')
        self.rds = boto3.client('rds')
        self.s3 = boto3.client('s3')
        self.dynamodb = boto3.resource('dynamodb')
        self.tracking_table = self.dynamodb.Table('ResourceTracking')
    
    def discover_all_resources(self):
        """Discover and catalog all resources across services"""
        
        resources = {}
        
        # Discover EC2 resources
        resources['ec2'] = self.discover_ec2_resources()
        
        # Discover RDS resources
        resources['rds'] = self.discover_rds_resources()
        
        # Discover S3 resources
        resources['s3'] = self.discover_s3_resources()
        
        # Store tracking information
        self.store_resource_tracking(resources)
        
        return resources
    
    def discover_ec2_resources(self):
        """Discover EC2 instances and related resources"""
        
        ec2_resources = []
        
        # Get all instances
        instances = self.ec2.describe_instances()
        
        for reservation in instances['Reservations']:
            for instance in reservation['Instances']:
                resource_info = {
                    'resource_id': instance['InstanceId'],
                    'resource_type': 'EC2Instance',
                    'state': instance['State']['Name'],
                    'launch_time': instance['LaunchTime'].isoformat(),
                    'instance_type': instance['InstanceType'],
                    'tags': {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])},
                    'vpc_id': instance.get('VpcId'),
                    'subnet_id': instance.get('SubnetId'),
                    'security_groups': [sg['GroupId'] for sg in instance.get('SecurityGroups', [])],
                    'discovered_at': datetime.now().isoformat()
                }
                
                # Add business context from tags
                resource_info['owner'] = resource_info['tags'].get('Owner', 'Unknown')
                resource_info['project'] = resource_info['tags'].get('Project', 'Unknown')
                resource_info['environment'] = resource_info['tags'].get('Environment', 'Unknown')
                resource_info['cost_center'] = resource_info['tags'].get('CostCenter', 'Unknown')
                
                ec2_resources.append(resource_info)
        
        # Get EBS volumes
        volumes = self.ec2.describe_volumes()
        
        for volume in volumes['Volumes']:
            resource_info = {
                'resource_id': volume['VolumeId'],
                'resource_type': 'EBSVolume',
                'state': volume['State'],
                'create_time': volume['CreateTime'].isoformat(),
                'size': volume['Size'],
                'volume_type': volume['VolumeType'],
                'tags': {tag['Key']: tag['Value'] for tag in volume.get('Tags', [])},
                'attachments': volume.get('Attachments', []),
                'discovered_at': datetime.now().isoformat()
            }
            
            # Add business context
            resource_info['owner'] = resource_info['tags'].get('Owner', 'Unknown')
            resource_info['project'] = resource_info['tags'].get('Project', 'Unknown')
            
            ec2_resources.append(resource_info)
        
        return ec2_resources
    
    def discover_rds_resources(self):
        """Discover RDS instances and clusters"""
        
        rds_resources = []
        
        # Get RDS instances
        instances = self.rds.describe_db_instances()
        
        for instance in instances['DBInstances']:
            # Get tags for the instance
            tags_response = self.rds.list_tags_for_resource(
                ResourceName=instance['DBInstanceArn']
            )
            tags = {tag['Key']: tag['Value'] for tag in tags_response['TagList']}
            
            resource_info = {
                'resource_id': instance['DBInstanceIdentifier'],
                'resource_type': 'RDSInstance',
                'state': instance['DBInstanceStatus'],
                'create_time': instance['InstanceCreateTime'].isoformat(),
                'engine': instance['Engine'],
                'instance_class': instance['DBInstanceClass'],
                'allocated_storage': instance['AllocatedStorage'],
                'tags': tags,
                'vpc_id': instance.get('DbSubnetGroup', {}).get('VpcId'),
                'discovered_at': datetime.now().isoformat()
            }
            
            # Add business context
            resource_info['owner'] = tags.get('Owner', 'Unknown')
            resource_info['project'] = tags.get('Project', 'Unknown')
            resource_info['environment'] = tags.get('Environment', 'Unknown')
            
            rds_resources.append(resource_info)
        
        return rds_resources
    
    def discover_s3_resources(self):
        """Discover S3 buckets"""
        
        s3_resources = []
        
        # Get all buckets
        buckets = self.s3.list_buckets()
        
        for bucket in buckets['Buckets']:
            bucket_name = bucket['Name']
            
            try:
                # Get bucket tags
                tags_response = self.s3.get_bucket_tagging(Bucket=bucket_name)
                tags = {tag['Key']: tag['Value'] for tag in tags_response['TagSet']}
            except:
                tags = {}
            
            try:
                # Get bucket location
                location = self.s3.get_bucket_location(Bucket=bucket_name)
                region = location['LocationConstraint'] or 'us-east-1'
            except:
                region = 'Unknown'
            
            resource_info = {
                'resource_id': bucket_name,
                'resource_type': 'S3Bucket',
                'create_time': bucket['CreationDate'].isoformat(),
                'region': region,
                'tags': tags,
                'discovered_at': datetime.now().isoformat()
            }
            
            # Add business context
            resource_info['owner'] = tags.get('Owner', 'Unknown')
            resource_info['project'] = tags.get('Project', 'Unknown')
            resource_info['environment'] = tags.get('Environment', 'Unknown')
            
            s3_resources.append(resource_info)
        
        return s3_resources
    
    def store_resource_tracking(self, resources):
        """Store resource tracking information in DynamoDB"""
        
        for service, service_resources in resources.items():
            for resource in service_resources:
                try:
                    # Calculate resource age
                    if 'create_time' in resource:
                        create_time = datetime.fromisoformat(resource['create_time'].replace('Z', '+00:00'))
                        age_days = (datetime.now() - create_time.replace(tzinfo=None)).days
                        resource['age_days'] = age_days
                    elif 'launch_time' in resource:
                        launch_time = datetime.fromisoformat(resource['launch_time'].replace('Z', '+00:00'))
                        age_days = (datetime.now() - launch_time.replace(tzinfo=None)).days
                        resource['age_days'] = age_days
                    
                    # Store in DynamoDB
                    self.tracking_table.put_item(
                        Item={
                            'ResourceId': resource['resource_id'],
                            'ResourceType': resource['resource_type'],
                            'ServiceCategory': service,
                            'TrackingData': resource,
                            'LastUpdated': datetime.now().isoformat(),
                            'TTL': int((datetime.now() + timedelta(days=365)).timestamp())
                        }
                    )
                    
                except Exception as e:
                    print(f"Error storing resource {resource['resource_id']}: {str(e)}")
```

### Usage Monitoring Integration
```python
def implement_usage_monitoring():
    """Implement comprehensive usage monitoring for tracked resources"""
    
    cloudwatch = boto3.client('cloudwatch')
    
    # Lambda function for usage monitoring
    lambda_code = '''
import boto3
import json
from datetime import datetime, timedelta

def lambda_handler(event, context):
    """Monitor resource usage and update tracking data"""
    
    cloudwatch = boto3.client('cloudwatch')
    dynamodb = boto3.resource('dynamodb')
    tracking_table = dynamodb.Table('ResourceTracking')
    
    # Get all tracked resources
    response = tracking_table.scan()
    resources = response['Items']
    
    for resource in resources:
        resource_id = resource['ResourceId']
        resource_type = resource['ResourceType']
        
        # Get usage metrics based on resource type
        usage_data = get_resource_usage_metrics(resource_id, resource_type, cloudwatch)
        
        # Update tracking data with usage information
        tracking_table.update_item(
            Key={
                'ResourceId': resource_id,
                'ResourceType': resource_type
            },
            UpdateExpression='SET UsageData = :usage, LastMonitored = :timestamp',
            ExpressionAttributeValues={
                ':usage': usage_data,
                ':timestamp': datetime.now().isoformat()
            }
        )
    
    return {'statusCode': 200, 'body': json.dumps(f'Monitored {len(resources)} resources')}

def get_resource_usage_metrics(resource_id, resource_type, cloudwatch):
    """Get usage metrics for specific resource types"""
    
    end_time = datetime.now()
    start_time = end_time - timedelta(days=7)  # Last 7 days
    
    usage_data = {}
    
    try:
        if resource_type == 'EC2Instance':
            # Get CPU utilization
            cpu_response = cloudwatch.get_metric_statistics(
                Namespace='AWS/EC2',
                MetricName='CPUUtilization',
                Dimensions=[{'Name': 'InstanceId', 'Value': resource_id}],
                StartTime=start_time,
                EndTime=end_time,
                Period=3600,
                Statistics=['Average']
            )
            
            if cpu_response['Datapoints']:
                avg_cpu = sum(dp['Average'] for dp in cpu_response['Datapoints']) / len(cpu_response['Datapoints'])
                usage_data['avg_cpu_utilization'] = avg_cpu
                usage_data['max_cpu_utilization'] = max(dp['Average'] for dp in cpu_response['Datapoints'])
                usage_data['cpu_datapoints'] = len(cpu_response['Datapoints'])
            
            # Get network metrics
            network_response = cloudwatch.get_metric_statistics(
                Namespace='AWS/EC2',
                MetricName='NetworkIn',
                Dimensions=[{'Name': 'InstanceId', 'Value': resource_id}],
                StartTime=start_time,
                EndTime=end_time,
                Period=3600,
                Statistics=['Sum']
            )
            
            if network_response['Datapoints']:
                total_network_in = sum(dp['Sum'] for dp in network_response['Datapoints'])
                usage_data['total_network_in'] = total_network_in
        
        elif resource_type == 'RDSInstance':
            # Get database connections
            conn_response = cloudwatch.get_metric_statistics(
                Namespace='AWS/RDS',
                MetricName='DatabaseConnections',
                Dimensions=[{'Name': 'DBInstanceIdentifier', 'Value': resource_id}],
                StartTime=start_time,
                EndTime=end_time,
                Period=3600,
                Statistics=['Average']
            )
            
            if conn_response['Datapoints']:
                avg_connections = sum(dp['Average'] for dp in conn_response['Datapoints']) / len(conn_response['Datapoints'])
                usage_data['avg_connections'] = avg_connections
                usage_data['max_connections'] = max(dp['Average'] for dp in conn_response['Datapoints'])
        
        elif resource_type == 'S3Bucket':
            # Get bucket size
            size_response = cloudwatch.get_metric_statistics(
                Namespace='AWS/S3',
                MetricName='BucketSizeBytes',
                Dimensions=[
                    {'Name': 'BucketName', 'Value': resource_id},
                    {'Name': 'StorageType', 'Value': 'StandardStorage'}
                ],
                StartTime=start_time,
                EndTime=end_time,
                Period=86400,  # Daily
                Statistics=['Average']
            )
            
            if size_response['Datapoints']:
                latest_size = size_response['Datapoints'][-1]['Average']
                usage_data['bucket_size_bytes'] = latest_size
        
        # Add common usage indicators
        usage_data['monitoring_period_days'] = 7
        usage_data['last_monitored'] = datetime.now().isoformat()
        
        # Determine usage status
        usage_data['usage_status'] = determine_usage_status(resource_type, usage_data)
        
    except Exception as e:
        usage_data['error'] = str(e)
        usage_data['usage_status'] = 'monitoring_error'
    
    return usage_data

def determine_usage_status(resource_type, usage_data):
    """Determine usage status based on metrics"""
    
    if resource_type == 'EC2Instance':
        avg_cpu = usage_data.get('avg_cpu_utilization', 0)
        if avg_cpu < 5:
            return 'unused'
        elif avg_cpu < 20:
            return 'underutilized'
        else:
            return 'active'
    
    elif resource_type == 'RDSInstance':
        avg_connections = usage_data.get('avg_connections', 0)
        if avg_connections < 1:
            return 'unused'
        elif avg_connections < 5:
            return 'underutilized'
        else:
            return 'active'
    
    elif resource_type == 'S3Bucket':
        bucket_size = usage_data.get('bucket_size_bytes', 0)
        if bucket_size == 0:
            return 'empty'
        else:
            return 'active'
    
    return 'unknown'
'''
    
    # Create Lambda function
    lambda_client = boto3.client('lambda')
    
    try:
        lambda_client.create_function(
            FunctionName='ResourceUsageMonitoring',
            Runtime='python3.9',
            Role='arn:aws:iam::ACCOUNT:role/ResourceTrackingRole',
            Handler='lambda_function.lambda_handler',
            Code={'ZipFile': lambda_code.encode()},
            Description='Monitor usage for tracked resources',
            Timeout=300
        )
        
        # Set up scheduled execution
        events_client = boto3.client('events')
        
        events_client.put_rule(
            Name='ResourceUsageMonitoringSchedule',
            ScheduleExpression='rate(1 day)',  # Daily monitoring
            Description='Trigger daily resource usage monitoring'
        )
        
        events_client.put_targets(
            Rule='ResourceUsageMonitoringSchedule',
            Targets=[
                {
                    'Id': '1',
                    'Arn': f'arn:aws:lambda:REGION:ACCOUNT:function:ResourceUsageMonitoring'
                }
            ]
        )
        
        print("Set up resource usage monitoring")
        
    except Exception as e:
        print(f"Error setting up usage monitoring: {str(e)}")
```

## Dependency Mapping and Analysis

### Resource Dependency Discovery
```python
def implement_dependency_mapping():
    """Implement comprehensive dependency mapping for resources"""
    
    class DependencyMapper:
        def __init__(self):
            self.ec2 = boto3.client('ec2')
            self.elbv2 = boto3.client('elbv2')
            self.rds = boto3.client('rds')
            self.dynamodb = boto3.resource('dynamodb')
            self.dependency_table = self.dynamodb.Table('ResourceDependencies')
        
        def map_all_dependencies(self):
            """Map dependencies for all tracked resources"""
            
            dependencies = {}
            
            # Map EC2 dependencies
            dependencies.update(self.map_ec2_dependencies())
            
            # Map Load Balancer dependencies
            dependencies.update(self.map_load_balancer_dependencies())
            
            # Map RDS dependencies
            dependencies.update(self.map_rds_dependencies())
            
            # Store dependency information
            self.store_dependencies(dependencies)
            
            return dependencies
        
        def map_ec2_dependencies(self):
            """Map EC2 instance dependencies"""
            
            dependencies = {}
            
            # Get all instances
            instances = self.ec2.describe_instances()
            
            for reservation in instances['Reservations']:
                for instance in reservation['Instances']:
                    instance_id = instance['InstanceId']
                    
                    instance_dependencies = {
                        'resource_id': instance_id,
                        'resource_type': 'EC2Instance',
                        'dependencies': [],
                        'dependents': []
                    }
                    
                    # VPC dependency
                    if 'VpcId' in instance:
                        instance_dependencies['dependencies'].append({
                            'resource_id': instance['VpcId'],
                            'resource_type': 'VPC',
                            'dependency_type': 'network'
                        })
                    
                    # Subnet dependency
                    if 'SubnetId' in instance:
                        instance_dependencies['dependencies'].append({
                            'resource_id': instance['SubnetId'],
                            'resource_type': 'Subnet',
                            'dependency_type': 'network'
                        })
                    
                    # Security Group dependencies
                    for sg in instance.get('SecurityGroups', []):
                        instance_dependencies['dependencies'].append({
                            'resource_id': sg['GroupId'],
                            'resource_type': 'SecurityGroup',
                            'dependency_type': 'security'
                        })
                    
                    # EBS Volume dependencies
                    for bdm in instance.get('BlockDeviceMappings', []):
                        if 'Ebs' in bdm:
                            instance_dependencies['dependencies'].append({
                                'resource_id': bdm['Ebs']['VolumeId'],
                                'resource_type': 'EBSVolume',
                                'dependency_type': 'storage'
                            })
                    
                    dependencies[instance_id] = instance_dependencies
            
            return dependencies
        
        def map_load_balancer_dependencies(self):
            """Map load balancer dependencies"""
            
            dependencies = {}
            
            # Get all load balancers
            load_balancers = self.elbv2.describe_load_balancers()
            
            for lb in load_balancers['LoadBalancers']:
                lb_arn = lb['LoadBalancerArn']
                lb_name = lb['LoadBalancerName']
                
                lb_dependencies = {
                    'resource_id': lb_name,
                    'resource_type': 'LoadBalancer',
                    'dependencies': [],
                    'dependents': []
                }
                
                # Subnet dependencies
                for subnet_id in lb.get('AvailabilityZones', []):
                    if 'SubnetId' in subnet_id:
                        lb_dependencies['dependencies'].append({
                            'resource_id': subnet_id['SubnetId'],
                            'resource_type': 'Subnet',
                            'dependency_type': 'network'
                        })
                
                # Security Group dependencies
                for sg_id in lb.get('SecurityGroups', []):
                    lb_dependencies['dependencies'].append({
                        'resource_id': sg_id,
                        'resource_type': 'SecurityGroup',
                        'dependency_type': 'security'
                    })
                
                # Target Group dependencies
                target_groups = self.elbv2.describe_target_groups(
                    LoadBalancerArn=lb_arn
                )
                
                for tg in target_groups['TargetGroups']:
                    lb_dependencies['dependents'].append({
                        'resource_id': tg['TargetGroupName'],
                        'resource_type': 'TargetGroup',
                        'dependency_type': 'routing'
                    })
                
                dependencies[lb_name] = lb_dependencies
            
            return dependencies
        
        def store_dependencies(self, dependencies):
            """Store dependency information in DynamoDB"""
            
            for resource_id, dependency_info in dependencies.items():
                try:
                    self.dependency_table.put_item(
                        Item={
                            'ResourceId': resource_id,
                            'ResourceType': dependency_info['resource_type'],
                            'Dependencies': dependency_info['dependencies'],
                            'Dependents': dependency_info['dependents'],
                            'LastUpdated': datetime.now().isoformat(),
                            'TTL': int((datetime.now() + timedelta(days=90)).timestamp())
                        }
                    )
                    
                except Exception as e:
                    print(f"Error storing dependencies for {resource_id}: {str(e)}")
    
    # Initialize and run dependency mapping
    mapper = DependencyMapper()
    dependencies = mapper.map_all_dependencies()
    
    return dependencies
```

## Common Challenges and Solutions

### Challenge: Resource Discovery Across Multiple Accounts

**Solution**: Use AWS Organizations and cross-account roles for centralized discovery. Implement automated discovery tools that can access multiple accounts. Create standardized tagging and naming conventions across accounts.

### Challenge: Tracking Dynamic Resources

**Solution**: Implement real-time discovery and tracking updates. Use event-driven tracking with CloudWatch Events. Create automated processes for tracking short-lived resources.

### Challenge: Maintaining Data Quality

**Solution**: Implement comprehensive data validation and quality checks. Use automated reconciliation processes. Create feedback loops for data accuracy improvement.

### Challenge: Scalability of Tracking Systems

**Solution**: Use scalable storage and processing solutions. Implement efficient data structures and indexing. Use managed services for large-scale data processing.

### Challenge: Integration with Existing Systems

**Solution**: Design flexible integration architectures. Use standard APIs and data formats. Implement gradual migration strategies for existing systems.

## Related Resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/cost_decommission_resources_track.html">AWS Well-Architected Framework - Track resources over their lifetime</a></li>
    <li><a href="https://docs.aws.amazon.com/config/latest/developerguide/WhatIsConfig.html">AWS Config User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-inventory.html">AWS Systems Manager Inventory</a></li>
    <li><a href="https://docs.aws.amazon.com/ARG/latest/userguide/welcome.html">AWS Resource Groups User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html">Amazon CloudWatch User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html">AWS CloudTrail User Guide</a></li>
    <li><a href="https://aws.amazon.com/blogs/aws-cost-management/">AWS Cost Management Blog</a></li>
    <li><a href="https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html">Amazon DynamoDB Developer Guide</a></li>
  </ul>
</div>

<style>
.pillar-header {
  background-color: #e8f5e8;
  border-left: 5px solid #2d7d2d;
}

.pillar-header h1 {
  color: #2d7d2d;
}

.aws-service-content h4 {
  color: #2d7d2d;
}

.related-resources {
  background-color: #e8f5e8;
}

.related-resources h2 {
  color: #2d7d2d;
}
</style>
