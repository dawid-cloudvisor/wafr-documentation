---
title: COST04-BP04 - Decommission resources automatically
layout: default
parent: COST04 - How do you decommission resources?
grand_parent: Cost Optimization
nav_order: 4
---

<div class="pillar-header">
  <h1>COST04-BP04: Decommission resources automatically</h1>
  <p>Implement automated systems to identify and decommission resources based on predefined criteria and policies. Automation reduces manual effort, ensures consistency, and enables proactive cost management through systematic resource cleanup.</p>
</div>

## Implementation guidance

Automated decommissioning enables organizations to systematically identify and remove unused or underutilized resources without manual intervention, reducing costs and operational overhead while maintaining safety and compliance requirements.

### Automation Principles

**Policy-Driven**: Use clearly defined policies and criteria to determine when resources should be automatically decommissioned.

**Safety First**: Implement comprehensive safety checks and validation to prevent accidental decommissioning of critical resources.

**Gradual Implementation**: Start with low-risk scenarios and gradually expand automation to more complex use cases.

**Monitoring and Alerting**: Maintain visibility into automated decommissioning activities with comprehensive logging and alerting.

### Automation Components

**Resource Discovery**: Automated identification of resources that meet decommissioning criteria.

**Policy Evaluation**: Systematic evaluation of resources against decommissioning policies and rules.

**Safety Validation**: Automated checks to ensure resources can be safely decommissioned.

**Execution Engine**: Automated execution of decommissioning procedures with proper error handling.

## AWS Services to Consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Lambda</h4>
    <p>Implement automated decommissioning logic and workflows. Use Lambda for event-driven and scheduled decommissioning tasks.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon EventBridge</h4>
    <p>Trigger automated decommissioning based on events and schedules. Use EventBridge for coordinating complex automation workflows.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Step Functions</h4>
    <p>Orchestrate complex automated decommissioning workflows. Use Step Functions for multi-step automation with error handling.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon CloudWatch</h4>
    <p>Monitor resource utilization and trigger automated decommissioning. Use CloudWatch metrics and alarms for automation triggers.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Config</h4>
    <p>Evaluate resource compliance with decommissioning policies. Use Config rules for automated policy evaluation and remediation.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Systems Manager</h4>
    <p>Automate resource management and decommissioning tasks. Use Systems Manager for coordinated automation across multiple resources.</p>
  </div>
</div>

## Implementation Steps

### 1. Define Automation Policies
- Establish clear criteria for automated decommissioning
- Define safety checks and validation requirements
- Create exception handling and escalation procedures
- Document automation policies and approval processes

### 2. Implement Resource Discovery
- Create automated resource discovery and classification
- Implement utilization monitoring and analysis
- Set up policy evaluation and scoring systems
- Create candidate identification and prioritization

### 3. Build Safety Validation
- Implement dependency checking and impact analysis
- Create business criticality assessment automation
- Set up stakeholder notification and approval workflows
- Design rollback and recovery mechanisms

### 4. Deploy Automation Engine
- Create automated decommissioning execution workflows
- Implement error handling and exception management
- Set up comprehensive logging and audit trails
- Create monitoring and alerting for automation activities

### 5. Enable Gradual Rollout
- Start with low-risk, non-critical resources
- Implement pilot programs and validation phases
- Gradually expand automation scope and complexity
- Create feedback loops for continuous improvement

### 6. Monitor and Optimize
- Track automation effectiveness and accuracy
- Monitor false positives and safety incidents
- Gather feedback from stakeholders and users
- Continuously refine automation policies and procedures

## Automated Decommissioning Framework

### Core Automation Engine
```python
import boto3
import json
from datetime import datetime, timedelta
from enum import Enum

class AutomationRiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AutomatedDecommissioner:
    def __init__(self):
        self.ec2 = boto3.client('ec2')
        self.rds = boto3.client('rds')
        self.cloudwatch = boto3.client('cloudwatch')
        self.dynamodb = boto3.resource('dynamodb')
        self.sns = boto3.client('sns')
        self.lambda_client = boto3.client('lambda')
        
        # Initialize tables
        self.automation_table = self.dynamodb.Table('AutomatedDecommissioning')
        self.policy_table = self.dynamodb.Table('DecommissioningPolicies')
        self.whitelist_table = self.dynamodb.Table('DecommissioningWhitelist')
    
    def run_automated_decommissioning(self):
        """Main function to run automated decommissioning process"""
        
        execution_log = {
            'execution_id': f"AUTO-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'start_time': datetime.now().isoformat(),
            'candidates_identified': 0,
            'resources_decommissioned': 0,
            'errors': [],
            'status': 'running'
        }
        
        try:
            # Step 1: Discover decommissioning candidates
            candidates = self.discover_decommissioning_candidates()
            execution_log['candidates_identified'] = len(candidates)
            execution_log['candidates'] = candidates
            
            # Step 2: Process each candidate
            for candidate in candidates:
                try:
                    result = self.process_decommissioning_candidate(candidate)
                    if result['action_taken']:
                        execution_log['resources_decommissioned'] += 1
                        
                except Exception as e:
                    execution_log['errors'].append({
                        'resource_id': candidate['resource_id'],
                        'error': str(e)
                    })
            
            execution_log['status'] = 'completed'
            
        except Exception as e:
            execution_log['status'] = 'failed'
            execution_log['error'] = str(e)
        
        execution_log['end_time'] = datetime.now().isoformat()
        
        # Store execution log
        self.store_execution_log(execution_log)
        
        # Send summary notification
        self.send_execution_summary(execution_log)
        
        return execution_log
    
    def discover_decommissioning_candidates(self):
        """Discover resources that are candidates for automated decommissioning"""
        
        candidates = []
        
        # Discover EC2 candidates
        ec2_candidates = self.discover_ec2_candidates()
        candidates.extend(ec2_candidates)
        
        # Discover RDS candidates
        rds_candidates = self.discover_rds_candidates()
        candidates.extend(rds_candidates)
        
        # Discover EBS volume candidates
        ebs_candidates = self.discover_ebs_candidates()
        candidates.extend(ebs_candidates)
        
        # Discover S3 bucket candidates
        s3_candidates = self.discover_s3_candidates()
        candidates.extend(s3_candidates)
        
        return candidates
    
    def discover_ec2_candidates(self):
        """Discover EC2 instances that are candidates for decommissioning"""
        
        candidates = []
        
        # Get all instances
        instances = self.ec2.describe_instances()
        
        for reservation in instances['Reservations']:
            for instance in reservation['Instances']:
                if instance['State']['Name'] in ['running', 'stopped']:
                    candidate = self.evaluate_ec2_instance(instance)
                    if candidate['eligible']:
                        candidates.append(candidate)
        
        return candidates
    
    def evaluate_ec2_instance(self, instance):
        """Evaluate EC2 instance for automated decommissioning"""
        
        instance_id = instance['InstanceId']
        
        candidate = {
            'resource_id': instance_id,
            'resource_type': 'EC2Instance',
            'eligible': False,
            'risk_level': AutomationRiskLevel.HIGH.value,
            'reasons': [],
            'safety_checks': {},
            'automation_policy': None
        }
        
        # Check if instance is whitelisted
        if self.is_resource_whitelisted(instance_id):
            candidate['reasons'].append('Resource is whitelisted')
            return candidate
        
        # Get instance metadata
        tags = {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])}
        launch_time = instance['LaunchTime']
        instance_age = (datetime.now(launch_time.tzinfo) - launch_time).days
        
        # Check age-based policies
        age_policy = self.check_age_based_policy(instance_age, tags)
        if age_policy['eligible']:
            candidate['eligible'] = True
            candidate['automation_policy'] = age_policy
            candidate['reasons'].append(f"Instance age ({instance_age} days) exceeds policy threshold")
        
        # Check utilization-based policies
        utilization_policy = self.check_utilization_policy(instance_id, tags)
        if utilization_policy['eligible']:
            candidate['eligible'] = True
            candidate['automation_policy'] = utilization_policy
            candidate['reasons'].append("Low utilization detected")
        
        # Perform safety checks
        candidate['safety_checks'] = self.perform_safety_checks(instance_id, 'EC2Instance', tags)
        
        # Determine risk level
        candidate['risk_level'] = self.calculate_automation_risk_level(candidate)
        
        return candidate
    
    def check_age_based_policy(self, resource_age, tags):
        """Check if resource meets age-based decommissioning policy"""
        
        policy = {
            'eligible': False,
            'policy_type': 'age_based',
            'threshold_days': 0,
            'environment_factor': 1.0
        }
        
        # Get environment-specific thresholds
        environment = tags.get('Environment', 'unknown').lower()
        
        age_thresholds = {
            'sandbox': 7,      # 1 week
            'development': 30, # 1 month
            'testing': 60,     # 2 months
            'staging': 90,     # 3 months
            'production': 365  # 1 year (very conservative)
        }
        
        threshold = age_thresholds.get(environment, 180)  # Default 6 months
        policy['threshold_days'] = threshold
        
        if resource_age > threshold:
            policy['eligible'] = True
        
        return policy
    
    def check_utilization_policy(self, resource_id, tags):
        """Check if resource meets utilization-based decommissioning policy"""
        
        policy = {
            'eligible': False,
            'policy_type': 'utilization_based',
            'avg_cpu_utilization': 0,
            'monitoring_period_days': 14,
            'threshold_percentage': 5
        }
        
        try:
            # Get CPU utilization for the last 14 days
            end_time = datetime.now()
            start_time = end_time - timedelta(days=14)
            
            response = self.cloudwatch.get_metric_statistics(
                Namespace='AWS/EC2',
                MetricName='CPUUtilization',
                Dimensions=[{'Name': 'InstanceId', 'Value': resource_id}],
                StartTime=start_time,
                EndTime=end_time,
                Period=3600,  # 1 hour periods
                Statistics=['Average']
            )
            
            if response['Datapoints']:
                avg_cpu = sum(dp['Average'] for dp in response['Datapoints']) / len(response['Datapoints'])
                policy['avg_cpu_utilization'] = avg_cpu
                
                # Check if utilization is below threshold
                environment = tags.get('Environment', 'unknown').lower()
                
                # Environment-specific thresholds
                utilization_thresholds = {
                    'sandbox': 1,      # Very low threshold for sandbox
                    'development': 3,  # Low threshold for dev
                    'testing': 5,      # Standard threshold
                    'staging': 10,     # Higher threshold for staging
                    'production': 20   # Much higher threshold for production
                }
                
                threshold = utilization_thresholds.get(environment, 5)
                policy['threshold_percentage'] = threshold
                
                if avg_cpu < threshold:
                    policy['eligible'] = True
            
        except Exception as e:
            policy['error'] = str(e)
        
        return policy
    
    def perform_safety_checks(self, resource_id, resource_type, tags):
        """Perform comprehensive safety checks before automated decommissioning"""
        
        safety_checks = {
            'whitelist_check': self.is_resource_whitelisted(resource_id),
            'dependency_check': self.check_resource_dependencies(resource_id),
            'business_hours_check': self.is_business_hours(),
            'environment_check': self.check_environment_safety(tags),
            'backup_check': self.check_backup_requirements(resource_id, resource_type),
            'approval_check': self.check_approval_requirements(resource_id, tags)
        }
        
        # Overall safety assessment
        safety_checks['safe_to_automate'] = all([
            not safety_checks['whitelist_check'],  # Not whitelisted
            not safety_checks['dependency_check']['has_critical_dependencies'],
            not safety_checks['business_hours_check'],  # Outside business hours
            safety_checks['environment_check']['safe_environment'],
            safety_checks['backup_check']['backup_not_required'] or safety_checks['backup_check']['backup_exists'],
            not safety_checks['approval_check']['approval_required']
        ])
        
        return safety_checks
    
    def check_resource_dependencies(self, resource_id):
        """Check for resource dependencies that would prevent safe decommissioning"""
        
        dependency_check = {
            'has_dependencies': False,
            'has_critical_dependencies': False,
            'dependency_count': 0,
            'dependencies': []
        }
        
        try:
            # Get dependency information from tracking system
            dependency_table = self.dynamodb.Table('ResourceDependencies')
            response = dependency_table.get_item(Key={'ResourceId': resource_id})
            
            if 'Item' in response:
                dependencies = response['Item'].get('Dependents', [])
                dependency_check['dependency_count'] = len(dependencies)
                dependency_check['dependencies'] = dependencies
                
                if dependencies:
                    dependency_check['has_dependencies'] = True
                    
                    # Check for critical dependencies
                    for dep in dependencies:
                        if dep.get('dependency_type') in ['critical', 'required']:
                            dependency_check['has_critical_dependencies'] = True
                            break
            
        except Exception as e:
            dependency_check['error'] = str(e)
        
        return dependency_check
    
    def check_environment_safety(self, tags):
        """Check if the resource environment is safe for automated decommissioning"""
        
        environment = tags.get('Environment', 'unknown').lower()
        
        # Define safe environments for automation
        safe_environments = ['sandbox', 'development', 'testing', 'dev', 'test']
        
        return {
            'environment': environment,
            'safe_environment': environment in safe_environments,
            'requires_approval': environment in ['staging', 'production', 'prod']
        }
    
    def calculate_automation_risk_level(self, candidate):
        """Calculate risk level for automated decommissioning"""
        
        risk_score = 0
        
        # Safety check scoring
        safety_checks = candidate['safety_checks']
        
        if safety_checks.get('dependency_check', {}).get('has_critical_dependencies'):
            risk_score += 3
        
        if safety_checks.get('environment_check', {}).get('requires_approval'):
            risk_score += 2
        
        if safety_checks.get('backup_check', {}).get('backup_required') and not safety_checks.get('backup_check', {}).get('backup_exists'):
            risk_score += 2
        
        if safety_checks.get('business_hours_check'):
            risk_score += 1
        
        # Policy type scoring
        if candidate.get('automation_policy', {}).get('policy_type') == 'utilization_based':
            risk_score += 1  # Utilization-based is slightly riskier
        
        # Determine risk level
        if risk_score >= 6:
            return AutomationRiskLevel.CRITICAL.value
        elif risk_score >= 4:
            return AutomationRiskLevel.HIGH.value
        elif risk_score >= 2:
            return AutomationRiskLevel.MEDIUM.value
        else:
            return AutomationRiskLevel.LOW.value
    
    def process_decommissioning_candidate(self, candidate):
        """Process a decommissioning candidate based on risk level and policies"""
        
        result = {
            'resource_id': candidate['resource_id'],
            'action_taken': False,
            'action_type': 'none',
            'reason': '',
            'timestamp': datetime.now().isoformat()
        }
        
        # Only proceed if safety checks pass
        if not candidate['safety_checks']['safe_to_automate']:
            result['reason'] = 'Safety checks failed'
            return result
        
        # Process based on risk level
        risk_level = candidate['risk_level']
        
        if risk_level == AutomationRiskLevel.LOW.value:
            # Automatically decommission low-risk resources
            result = self.execute_automated_decommissioning(candidate)
            
        elif risk_level == AutomationRiskLevel.MEDIUM.value:
            # Send notification and wait for approval or auto-approve after delay
            result = self.handle_medium_risk_decommissioning(candidate)
            
        else:
            # High and critical risk resources require manual approval
            result = self.request_manual_approval(candidate)
        
        return result
    
    def execute_automated_decommissioning(self, candidate):
        """Execute automated decommissioning for low-risk resources"""
        
        result = {
            'resource_id': candidate['resource_id'],
            'action_taken': False,
            'action_type': 'automated_decommission',
            'reason': '',
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            resource_type = candidate['resource_type']
            resource_id = candidate['resource_id']
            
            if resource_type == 'EC2Instance':
                # Stop instance first, then schedule termination
                self.ec2.stop_instances(InstanceIds=[resource_id])
                
                # Schedule termination after a grace period
                self.schedule_delayed_termination(resource_id, hours=24)
                
                result['action_taken'] = True
                result['reason'] = 'Instance stopped, termination scheduled in 24 hours'
                
            elif resource_type == 'EBSVolume':
                # Create snapshot before deletion
                snapshot = self.ec2.create_snapshot(
                    VolumeId=resource_id,
                    Description=f'Automated backup before decommissioning {resource_id}'
                )
                
                # Schedule volume deletion after snapshot completion
                self.schedule_volume_deletion(resource_id, snapshot['SnapshotId'])
                
                result['action_taken'] = True
                result['reason'] = 'Snapshot created, volume deletion scheduled'
            
            # Log the action
            self.log_automation_action(candidate, result)
            
        except Exception as e:
            result['reason'] = f'Error during automated decommissioning: {str(e)}'
        
        return result
    
    def schedule_delayed_termination(self, instance_id, hours=24):
        """Schedule delayed termination of an instance"""
        
        # Use EventBridge to schedule delayed termination
        eventbridge = boto3.client('events')
        
        # Schedule rule for delayed execution
        rule_name = f'delayed-termination-{instance_id}'
        
        eventbridge.put_rule(
            Name=rule_name,
            ScheduleExpression=f'rate({hours} hours)',
            Description=f'Delayed termination for instance {instance_id}',
            State='ENABLED'
        )
        
        # Add target to execute termination
        eventbridge.put_targets(
            Rule=rule_name,
            Targets=[
                {
                    'Id': '1',
                    'Arn': 'arn:aws:lambda:REGION:ACCOUNT:function:ExecuteDelayedTermination',
                    'Input': json.dumps({
                        'instance_id': instance_id,
                        'action': 'terminate',
                        'scheduled_time': (datetime.now() + timedelta(hours=hours)).isoformat()
                    })
                }
            ]
        )
```

### Automated Policy Engine
```python
def create_automated_policy_engine():
    """Create comprehensive automated policy engine"""
    
    # Lambda function for policy evaluation
    lambda_code = '''
import boto3
import json
from datetime import datetime, timedelta

def lambda_handler(event, context):
    """Evaluate resources against automated decommissioning policies"""
    
    # Initialize clients
    dynamodb = boto3.resource('dynamodb')
    policy_table = dynamodb.Table('DecommissioningPolicies')
    
    # Get active policies
    policies = get_active_policies(policy_table)
    
    # Evaluate each resource type
    results = {}
    
    for policy in policies:
        policy_results = evaluate_policy(policy)
        results[policy['PolicyId']] = policy_results
    
    return {
        'statusCode': 200,
        'body': json.dumps(results)
    }

def get_active_policies(policy_table):
    """Get all active decommissioning policies"""
    
    response = policy_table.scan(
        FilterExpression='PolicyStatus = :status',
        ExpressionAttributeValues={':status': 'active'}
    )
    
    return response['Items']

def evaluate_policy(policy):
    """Evaluate a specific decommissioning policy"""
    
    policy_type = policy['PolicyType']
    
    if policy_type == 'age_based':
        return evaluate_age_based_policy(policy)
    elif policy_type == 'utilization_based':
        return evaluate_utilization_based_policy(policy)
    elif policy_type == 'cost_based':
        return evaluate_cost_based_policy(policy)
    else:
        return {'error': f'Unknown policy type: {policy_type}'}

def evaluate_age_based_policy(policy):
    """Evaluate age-based decommissioning policy"""
    
    # Implementation for age-based policy evaluation
    candidates = []
    
    # Get resources older than threshold
    threshold_days = policy['Parameters']['ThresholdDays']
    cutoff_date = datetime.now() - timedelta(days=threshold_days)
    
    # Query resources based on age
    # Implementation would depend on resource tracking system
    
    return {
        'policy_id': policy['PolicyId'],
        'candidates_found': len(candidates),
        'candidates': candidates
    }
'''
    
    # Create Lambda function
    lambda_client = boto3.client('lambda')
    
    try:
        lambda_client.create_function(
            FunctionName='AutomatedPolicyEngine',
            Runtime='python3.9',
            Role='arn:aws:iam::ACCOUNT:role/AutomatedDecommissioningRole',
            Handler='lambda_function.lambda_handler',
            Code={'ZipFile': lambda_code.encode()},
            Description='Automated policy engine for resource decommissioning',
            Timeout=300
        )
        
        print("Created automated policy engine")
        
    except Exception as e:
        print(f"Error creating policy engine: {str(e)}")
```

## Common Challenges and Solutions

### Challenge: False Positives in Automated Detection

**Solution**: Implement comprehensive safety checks and validation. Use machine learning to improve detection accuracy over time. Create feedback loops to learn from false positives.

### Challenge: Stakeholder Trust in Automation

**Solution**: Start with low-risk scenarios and gradually build trust. Provide comprehensive visibility and control. Implement easy override and rollback mechanisms.

### Challenge: Complex Dependency Management

**Solution**: Implement sophisticated dependency mapping and analysis. Use gradual automation rollout. Create comprehensive testing and validation procedures.

### Challenge: Compliance and Audit Requirements

**Solution**: Implement comprehensive audit logging for all automated activities. Create detailed documentation and approval trails. Use automated compliance checking and reporting.

### Challenge: Balancing Automation and Safety

**Solution**: Use risk-based automation approaches. Implement multiple safety checks and validation layers. Create clear escalation and override procedures.

## Related Resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/cost_decommission_resources_automatically.html">AWS Well-Architected Framework - Decommission resources automatically</a></li>
    <li><a href="https://docs.aws.amazon.com/lambda/latest/dg/welcome.html">AWS Lambda Developer Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-what-is.html">Amazon EventBridge User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html">AWS Step Functions Developer Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html">Amazon CloudWatch User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/config/latest/developerguide/WhatIsConfig.html">AWS Config User Guide</a></li>
    <li><a href="https://aws.amazon.com/blogs/aws-cost-management/">AWS Cost Management Blog</a></li>
    <li><a href="https://docs.aws.amazon.com/systems-manager/latest/userguide/what-is-systems-manager.html">AWS Systems Manager User Guide</a></li>
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
