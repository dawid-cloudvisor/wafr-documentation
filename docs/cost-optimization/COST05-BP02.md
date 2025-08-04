---
title: COST05-BP02 - Analyze all components of this workload
layout: default
parent: COST05 - How do you evaluate cost when you select services?
grand_parent: Cost Optimization
nav_order: 2
---

<div class="pillar-header">
  <h1>COST05-BP02: Analyze all components of this workload</h1>
  <p>Systematically identify and analyze all components that make up your workload to ensure comprehensive cost evaluation. Understanding the complete architecture enables accurate cost modeling and optimization opportunities identification.</p>
</div>

## Implementation guidance

Comprehensive workload analysis involves breaking down the entire system into individual components, understanding their relationships, and evaluating their cost implications both individually and collectively.

### Component Analysis Framework

**Architectural Decomposition**: Break down the workload into logical components including compute, storage, network, database, and application services.

**Dependency Mapping**: Identify relationships and dependencies between components to understand cost interdependencies.

**Usage Pattern Analysis**: Analyze how each component is used, including peak and average utilization patterns.

**Cost Attribution**: Assign costs to individual components to enable granular optimization and decision-making.

### Component Categories

**Compute Components**: EC2 instances, Lambda functions, containers, and other compute resources.

**Storage Components**: S3 buckets, EBS volumes, EFS file systems, and backup storage.

**Network Components**: Load balancers, NAT gateways, VPC endpoints, and data transfer costs.

**Database Components**: RDS instances, DynamoDB tables, ElastiCache clusters, and database storage.

**Application Services**: API Gateway, SQS queues, SNS topics, and other managed services.

**Security Components**: WAF, Shield, GuardDuty, and other security services.

## AWS Services to Consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Application Discovery Service</h4>
    <p>Discover and map application components and dependencies. Use discovery data to understand workload architecture and component relationships.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS X-Ray</h4>
    <p>Trace requests through distributed applications to understand component interactions and performance characteristics.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Cost Explorer</h4>
    <p>Analyze costs by service and resource to understand component-level spending patterns and trends.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Resource Groups</h4>
    <p>Organize and manage related resources as logical groups. Use resource groups to track component costs and utilization.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS CloudFormation</h4>
    <p>Define infrastructure as code to understand component relationships and dependencies. Use stack analysis for cost modeling.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Config</h4>
    <p>Track resource configurations and relationships. Use Config to understand component dependencies and changes over time.</p>
  </div>
</div>

## Implementation Steps

### 1. Inventory All Components
- Create comprehensive inventory of all workload components
- Document component types, configurations, and purposes
- Identify shared and dedicated components
- Map component ownership and responsibilities

### 2. Analyze Component Dependencies
- Map dependencies between components
- Identify critical path components
- Understand data flow and communication patterns
- Document integration points and interfaces

### 3. Evaluate Component Usage
- Analyze utilization patterns for each component
- Identify peak and off-peak usage periods
- Understand seasonal and cyclical patterns
- Document growth trends and projections

### 4. Assess Component Costs
- Calculate current costs for each component
- Project future costs based on usage trends
- Identify cost drivers and optimization opportunities
- Create component-level cost models

### 5. Identify Optimization Opportunities
- Find underutilized or oversized components
- Identify redundant or unnecessary components
- Evaluate alternative service options
- Prioritize optimization efforts based on impact

### 6. Create Component Documentation
- Document all findings and analysis results
- Create component architecture diagrams
- Maintain component cost models and projections
- Establish regular review and update processes

## Workload Component Analysis

### Automated Component Discovery
```python
import boto3
import json
from datetime import datetime, timedelta

class WorkloadComponentAnalyzer:
    def __init__(self):
        self.ec2 = boto3.client('ec2')
        self.rds = boto3.client('rds')
        self.s3 = boto3.client('s3')
        self.elbv2 = boto3.client('elbv2')
        self.lambda_client = boto3.client('lambda')
        self.dynamodb = boto3.client('dynamodb')
        self.cloudwatch = boto3.client('cloudwatch')
        self.ce_client = boto3.client('ce')
        
    def analyze_workload_components(self, workload_id, workload_tags):
        """Comprehensive analysis of all workload components"""
        
        analysis_result = {
            'workload_id': workload_id,
            'analysis_date': datetime.now().isoformat(),
            'components': {},
            'dependencies': {},
            'cost_analysis': {},
            'optimization_opportunities': []
        }
        
        # Discover all components
        components = self.discover_all_components(workload_tags)
        analysis_result['components'] = components
        
        # Analyze dependencies
        dependencies = self.analyze_component_dependencies(components)
        analysis_result['dependencies'] = dependencies
        
        # Perform cost analysis
        cost_analysis = self.analyze_component_costs(components)
        analysis_result['cost_analysis'] = cost_analysis
        
        # Identify optimization opportunities
        opportunities = self.identify_optimization_opportunities(components, cost_analysis)
        analysis_result['optimization_opportunities'] = opportunities
        
        return analysis_result
    
    def discover_all_components(self, workload_tags):
        """Discover all components belonging to the workload"""
        
        components = {
            'compute': self.discover_compute_components(workload_tags),
            'storage': self.discover_storage_components(workload_tags),
            'network': self.discover_network_components(workload_tags),
            'database': self.discover_database_components(workload_tags),
            'serverless': self.discover_serverless_components(workload_tags),
            'managed_services': self.discover_managed_services(workload_tags)
        }
        
        return components
    
    def discover_compute_components(self, workload_tags):
        """Discover compute components (EC2, ECS, etc.)"""
        
        compute_components = []
        
        # EC2 Instances
        instances = self.ec2.describe_instances(
            Filters=[
                {'Name': f'tag:{key}', 'Values': [value]}
                for key, value in workload_tags.items()
            ]
        )
        
        for reservation in instances['Reservations']:
            for instance in reservation['Instances']:
                if instance['State']['Name'] != 'terminated':
                    component = {
                        'component_id': instance['InstanceId'],
                        'component_type': 'EC2Instance',
                        'instance_type': instance['InstanceType'],
                        'state': instance['State']['Name'],
                        'launch_time': instance['LaunchTime'].isoformat(),
                        'vpc_id': instance.get('VpcId'),
                        'subnet_id': instance.get('SubnetId'),
                        'tags': {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])},
                        'usage_metrics': self.get_instance_usage_metrics(instance['InstanceId'])
                    }
                    compute_components.append(component)
        
        return compute_components
    
    def discover_storage_components(self, workload_tags):
        """Discover storage components (S3, EBS, EFS)"""
        
        storage_components = []
        
        # S3 Buckets
        buckets = self.s3.list_buckets()
        for bucket in buckets['Buckets']:
            try:
                tags_response = self.s3.get_bucket_tagging(Bucket=bucket['Name'])
                bucket_tags = {tag['Key']: tag['Value'] for tag in tags_response['TagSet']}
                
                # Check if bucket belongs to workload
                if self.matches_workload_tags(bucket_tags, workload_tags):
                    component = {
                        'component_id': bucket['Name'],
                        'component_type': 'S3Bucket',
                        'creation_date': bucket['CreationDate'].isoformat(),
                        'tags': bucket_tags,
                        'storage_metrics': self.get_s3_storage_metrics(bucket['Name'])
                    }
                    storage_components.append(component)
            except:
                continue
        
        # EBS Volumes
        volumes = self.ec2.describe_volumes(
            Filters=[
                {'Name': f'tag:{key}', 'Values': [value]}
                for key, value in workload_tags.items()
            ]
        )
        
        for volume in volumes['Volumes']:
            component = {
                'component_id': volume['VolumeId'],
                'component_type': 'EBSVolume',
                'size': volume['Size'],
                'volume_type': volume['VolumeType'],
                'state': volume['State'],
                'create_time': volume['CreateTime'].isoformat(),
                'attachments': volume.get('Attachments', []),
                'tags': {tag['Key']: tag['Value'] for tag in volume.get('Tags', [])},
                'usage_metrics': self.get_ebs_usage_metrics(volume['VolumeId'])
            }
            storage_components.append(component)
        
        return storage_components
    
    def discover_database_components(self, workload_tags):
        """Discover database components (RDS, DynamoDB)"""
        
        database_components = []
        
        # RDS Instances
        rds_instances = self.rds.describe_db_instances()
        for instance in rds_instances['DBInstances']:
            try:
                tags_response = self.rds.list_tags_for_resource(
                    ResourceName=instance['DBInstanceArn']
                )
                instance_tags = {tag['Key']: tag['Value'] for tag in tags_response['TagList']}
                
                if self.matches_workload_tags(instance_tags, workload_tags):
                    component = {
                        'component_id': instance['DBInstanceIdentifier'],
                        'component_type': 'RDSInstance',
                        'engine': instance['Engine'],
                        'instance_class': instance['DBInstanceClass'],
                        'allocated_storage': instance['AllocatedStorage'],
                        'status': instance['DBInstanceStatus'],
                        'create_time': instance['InstanceCreateTime'].isoformat(),
                        'tags': instance_tags,
                        'usage_metrics': self.get_rds_usage_metrics(instance['DBInstanceIdentifier'])
                    }
                    database_components.append(component)
            except:
                continue
        
        # DynamoDB Tables
        tables = self.dynamodb.list_tables()
        for table_name in tables['TableNames']:
            try:
                table_description = self.dynamodb.describe_table(TableName=table_name)
                table_arn = table_description['Table']['TableArn']
                
                tags_response = self.dynamodb.list_tags_of_resource(ResourceArn=table_arn)
                table_tags = {tag['Key']: tag['Value'] for tag in tags_response['Tags']}
                
                if self.matches_workload_tags(table_tags, workload_tags):
                    component = {
                        'component_id': table_name,
                        'component_type': 'DynamoDBTable',
                        'table_status': table_description['Table']['TableStatus'],
                        'billing_mode': table_description['Table'].get('BillingModeSummary', {}).get('BillingMode'),
                        'creation_date': table_description['Table']['CreationDateTime'].isoformat(),
                        'tags': table_tags,
                        'usage_metrics': self.get_dynamodb_usage_metrics(table_name)
                    }
                    database_components.append(component)
            except:
                continue
        
        return database_components
    
    def analyze_component_dependencies(self, components):
        """Analyze dependencies between components"""
        
        dependencies = {}
        
        # Analyze compute dependencies
        for compute_component in components['compute']:
            component_id = compute_component['component_id']
            dependencies[component_id] = {
                'depends_on': [],
                'depended_by': []
            }
            
            # Check storage dependencies
            for storage_component in components['storage']:
                if storage_component['component_type'] == 'EBSVolume':
                    for attachment in storage_component.get('attachments', []):
                        if attachment.get('InstanceId') == component_id:
                            dependencies[component_id]['depends_on'].append({
                                'component_id': storage_component['component_id'],
                                'component_type': storage_component['component_type'],
                                'dependency_type': 'storage'
                            })
            
            # Check network dependencies (simplified)
            vpc_id = compute_component.get('vpc_id')
            if vpc_id:
                dependencies[component_id]['depends_on'].append({
                    'component_id': vpc_id,
                    'component_type': 'VPC',
                    'dependency_type': 'network'
                })
        
        return dependencies
    
    def analyze_component_costs(self, components):
        """Analyze costs for each component"""
        
        cost_analysis = {}
        
        # Get cost data for the last 30 days
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        
        for category, category_components in components.items():
            cost_analysis[category] = {
                'total_cost': 0,
                'component_costs': []
            }
            
            for component in category_components:
                component_cost = self.get_component_cost(
                    component['component_id'],
                    component['component_type'],
                    start_date,
                    end_date
                )
                
                cost_analysis[category]['component_costs'].append({
                    'component_id': component['component_id'],
                    'component_type': component['component_type'],
                    'monthly_cost': component_cost,
                    'cost_per_day': component_cost / 30
                })
                
                cost_analysis[category]['total_cost'] += component_cost
        
        return cost_analysis
    
    def get_component_cost(self, component_id, component_type, start_date, end_date):
        """Get cost for a specific component"""
        
        try:
            # This is a simplified cost calculation
            # In practice, you would use more sophisticated cost attribution
            
            if component_type == 'EC2Instance':
                # Get instance cost based on instance type and usage
                return self.estimate_ec2_cost(component_id, start_date, end_date)
            elif component_type == 'S3Bucket':
                return self.estimate_s3_cost(component_id, start_date, end_date)
            elif component_type == 'RDSInstance':
                return self.estimate_rds_cost(component_id, start_date, end_date)
            else:
                return 0
                
        except Exception as e:
            print(f"Error calculating cost for {component_id}: {str(e)}")
            return 0
    
    def identify_optimization_opportunities(self, components, cost_analysis):
        """Identify optimization opportunities for components"""
        
        opportunities = []
        
        # Analyze compute optimization opportunities
        for compute_component in components['compute']:
            usage_metrics = compute_component.get('usage_metrics', {})
            avg_cpu = usage_metrics.get('avg_cpu_utilization', 0)
            
            if avg_cpu < 20:
                opportunities.append({
                    'component_id': compute_component['component_id'],
                    'component_type': compute_component['component_type'],
                    'opportunity_type': 'rightsizing',
                    'description': f'Low CPU utilization ({avg_cpu:.1f}%) - consider downsizing',
                    'potential_savings': self.estimate_rightsizing_savings(compute_component),
                    'priority': 'high' if avg_cpu < 10 else 'medium'
                })
        
        # Analyze storage optimization opportunities
        for storage_component in components['storage']:
            if storage_component['component_type'] == 'EBSVolume':
                if not storage_component.get('attachments'):
                    opportunities.append({
                        'component_id': storage_component['component_id'],
                        'component_type': storage_component['component_type'],
                        'opportunity_type': 'unused_resource',
                        'description': 'Unattached EBS volume - consider deletion',
                        'potential_savings': self.estimate_ebs_savings(storage_component),
                        'priority': 'high'
                    })
        
        return opportunities
    
    def matches_workload_tags(self, resource_tags, workload_tags):
        """Check if resource tags match workload tags"""
        
        for key, value in workload_tags.items():
            if resource_tags.get(key) != value:
                return False
        return True
```

## Component Analysis Templates

### Component Inventory Template
```yaml
Component_Inventory:
  workload_id: "WORKLOAD-001"
  workload_name: "E-commerce Platform"
  analysis_date: "2024-01-15"
  
  compute_components:
    - component_id: "i-1234567890abcdef0"
      component_type: "EC2Instance"
      instance_type: "m5.large"
      purpose: "Web server"
      environment: "production"
      utilization_metrics:
        avg_cpu: 45.2
        max_cpu: 78.5
        avg_memory: 62.1
      monthly_cost: 67.32
      
  storage_components:
    - component_id: "vol-1234567890abcdef0"
      component_type: "EBSVolume"
      size_gb: 100
      volume_type: "gp3"
      purpose: "Application data"
      utilization_metrics:
        avg_iops: 150
        max_iops: 500
      monthly_cost: 8.00
      
  network_components:
    - component_id: "alb-1234567890abcdef0"
      component_type: "ApplicationLoadBalancer"
      purpose: "Traffic distribution"
      monthly_requests: 10000000
      monthly_cost: 22.50
      
  database_components:
    - component_id: "mydb-instance"
      component_type: "RDSInstance"
      engine: "mysql"
      instance_class: "db.t3.medium"
      purpose: "Primary database"
      utilization_metrics:
        avg_cpu: 35.8
        avg_connections: 25
      monthly_cost: 58.40
```

## Common Challenges and Solutions

### Challenge: Discovering All Workload Components

**Solution**: Use automated discovery tools and maintain comprehensive tagging strategies. Implement regular audits and validation processes. Use multiple discovery methods to ensure complete coverage.

### Challenge: Understanding Component Dependencies

**Solution**: Use application tracing and monitoring tools. Implement dependency mapping automation. Create and maintain architecture documentation and diagrams.

### Challenge: Accurate Cost Attribution

**Solution**: Implement comprehensive tagging and cost allocation strategies. Use detailed billing data and cost analysis tools. Create component-specific cost models and validation processes.

### Challenge: Analyzing Complex Distributed Systems

**Solution**: Use distributed tracing and observability tools. Break down analysis into manageable segments. Focus on critical path components and high-cost areas first.

### Challenge: Keeping Analysis Current

**Solution**: Implement automated discovery and analysis processes. Set up regular review cycles and updates. Use monitoring and alerting to detect changes in component usage patterns.

## Related Resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/cost_select_service_analyze_components.html">AWS Well-Architected Framework - Analyze all components of this workload</a></li>
    <li><a href="https://docs.aws.amazon.com/application-discovery/latest/userguide/what-is-appdiscovery.html">AWS Application Discovery Service</a></li>
    <li><a href="https://docs.aws.amazon.com/xray/latest/devguide/aws-xray.html">AWS X-Ray Developer Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/cost-management/latest/userguide/ce-what-is.html">AWS Cost Explorer User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/ARG/latest/userguide/welcome.html">AWS Resource Groups User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html">AWS CloudFormation User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/config/latest/developerguide/WhatIsConfig.html">AWS Config User Guide</a></li>
    <li><a href="https://aws.amazon.com/blogs/aws-cost-management/">AWS Cost Management Blog</a></li>
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
