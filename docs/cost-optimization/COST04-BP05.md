---
title: COST04-BP05 - Enforce data retention policies
layout: default
parent: COST04 - How do you decommission resources?
grand_parent: Cost Optimization
nav_order: 5
---

<div class="pillar-header">
  <h1>COST04-BP05: Enforce data retention policies</h1>
  <p>Implement and enforce comprehensive data retention policies that balance compliance requirements, business needs, and cost optimization. Proper data retention ensures regulatory compliance while preventing unnecessary storage costs from accumulating over time.</p>
</div>

## Implementation guidance

Data retention policies provide the framework for systematically managing data throughout its lifecycle, ensuring compliance with regulatory requirements while optimizing storage costs through appropriate data archival and deletion strategies.

### Data Retention Principles

**Compliance First**: Ensure all data retention policies meet regulatory and legal requirements for your industry and jurisdiction.

**Business Alignment**: Balance compliance requirements with business needs for data accessibility and operational requirements.

**Cost Optimization**: Implement tiered storage and lifecycle management to optimize costs while maintaining data availability.

**Automated Enforcement**: Use automated tools and processes to consistently enforce retention policies across all data stores.

### Retention Policy Components

**Classification Framework**: Systematic classification of data based on sensitivity, business value, and regulatory requirements.

**Retention Schedules**: Defined timelines for data retention, archival, and deletion based on data classification and requirements.

**Lifecycle Management**: Automated processes for transitioning data through different storage tiers and eventual deletion.

**Compliance Monitoring**: Ongoing monitoring and reporting to ensure retention policies are properly enforced.

## AWS Services to Consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon S3</h4>
    <p>Implement lifecycle policies for automated data archival and deletion. Use S3 storage classes for cost-effective long-term retention.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon S3 Glacier</h4>
    <p>Store long-term archival data at low cost. Use Glacier for data that requires long-term retention but infrequent access.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Lambda</h4>
    <p>Implement custom data retention logic and automation. Use Lambda for complex retention rules and cross-service data management.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon DynamoDB</h4>
    <p>Use TTL (Time To Live) for automatic data expiration. Implement point-in-time recovery for compliance requirements.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon RDS</h4>
    <p>Manage database backups and automated snapshots. Use automated backup retention for compliance and recovery.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS CloudTrail</h4>
    <p>Maintain audit logs with appropriate retention periods. Use CloudTrail for compliance and security audit requirements.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon CloudWatch Logs</h4>
    <p>Set retention periods for application and system logs. Use log groups with appropriate retention policies.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Config</h4>
    <p>Monitor compliance with data retention policies. Use Config rules to automatically check retention policy adherence.</p>
  </div>
</div>

## Implementation Steps

### 1. Define Data Classification Framework
- Identify all data types and sources across the organization
- Create data classification categories based on sensitivity and value
- Define regulatory and compliance requirements for each category
- Establish business requirements for data accessibility and retention

### 2. Develop Retention Policies
- Create retention schedules for each data classification category
- Define archival and deletion timelines based on requirements
- Establish exception handling and approval processes
- Document policy rationale and compliance mapping

### 3. Implement Lifecycle Management
- Set up automated lifecycle policies for different storage services
- Configure tiered storage transitions for cost optimization
- Implement automated deletion processes with appropriate safeguards
- Create monitoring and alerting for lifecycle events

### 4. Deploy Compliance Monitoring
- Set up automated compliance checking and reporting
- Create dashboards for retention policy status and metrics
- Implement alerting for policy violations or failures
- Establish audit trails for all retention-related activities

### 5. Create Governance Framework
- Establish roles and responsibilities for data retention management
- Create approval processes for policy changes and exceptions
- Implement regular policy reviews and updates
- Set up training and awareness programs for stakeholders

### 6. Enable Continuous Improvement
- Monitor policy effectiveness and cost impact
- Gather feedback from stakeholders and compliance teams
- Refine policies based on changing requirements and best practices
- Update automation and processes based on lessons learned

## Data Retention Framework

### Comprehensive Retention Policy Engine
```python
import boto3
import json
from datetime import datetime, timedelta
from enum import Enum

class DataClassification(Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"

class RetentionAction(Enum):
    RETAIN = "retain"
    ARCHIVE = "archive"
    DELETE = "delete"

class DataRetentionManager:
    def __init__(self):
        self.s3 = boto3.client('s3')
        self.dynamodb = boto3.resource('dynamodb')
        self.cloudwatch_logs = boto3.client('logs')
        self.rds = boto3.client('rds')
        self.lambda_client = boto3.client('lambda')
        
        # Initialize tables
        self.retention_policies_table = self.dynamodb.Table('DataRetentionPolicies')
        self.retention_audit_table = self.dynamodb.Table('RetentionAuditLog')
        self.data_inventory_table = self.dynamodb.Table('DataInventory')
    
    def enforce_retention_policies(self):
        """Main function to enforce all data retention policies"""
        
        enforcement_log = {
            'execution_id': f"RETENTION-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'start_time': datetime.now().isoformat(),
            'policies_processed': 0,
            'actions_taken': 0,
            'errors': [],
            'status': 'running'
        }
        
        try:
            # Get all active retention policies
            policies = self.get_active_retention_policies()
            enforcement_log['policies_processed'] = len(policies)
            
            # Process each policy
            for policy in policies:
                try:
                    result = self.enforce_retention_policy(policy)
                    enforcement_log['actions_taken'] += result['actions_taken']
                    
                except Exception as e:
                    enforcement_log['errors'].append({
                        'policy_id': policy['PolicyId'],
                        'error': str(e)
                    })
            
            enforcement_log['status'] = 'completed'
            
        except Exception as e:
            enforcement_log['status'] = 'failed'
            enforcement_log['error'] = str(e)
        
        enforcement_log['end_time'] = datetime.now().isoformat()
        
        # Store enforcement log
        self.store_enforcement_log(enforcement_log)
        
        return enforcement_log
    
    def get_active_retention_policies(self):
        """Get all active data retention policies"""
        
        response = self.retention_policies_table.scan(
            FilterExpression='PolicyStatus = :status',
            ExpressionAttributeValues={':status': 'active'}
        )
        
        return response['Items']
    
    def enforce_retention_policy(self, policy):
        """Enforce a specific data retention policy"""
        
        result = {
            'policy_id': policy['PolicyId'],
            'actions_taken': 0,
            'items_processed': 0,
            'errors': []
        }
        
        policy_type = policy['PolicyType']
        
        if policy_type == 's3_lifecycle':
            result = self.enforce_s3_retention_policy(policy)
        elif policy_type == 'dynamodb_ttl':
            result = self.enforce_dynamodb_retention_policy(policy)
        elif policy_type == 'cloudwatch_logs':
            result = self.enforce_logs_retention_policy(policy)
        elif policy_type == 'rds_backup':
            result = self.enforce_rds_retention_policy(policy)
        elif policy_type == 'custom':
            result = self.enforce_custom_retention_policy(policy)
        
        # Log policy enforcement
        self.log_policy_enforcement(policy, result)
        
        return result
    
    def enforce_s3_retention_policy(self, policy):
        """Enforce S3 data retention policy"""
        
        result = {
            'policy_id': policy['PolicyId'],
            'actions_taken': 0,
            'items_processed': 0,
            'errors': []
        }
        
        try:
            # Get policy parameters
            bucket_pattern = policy['Parameters']['BucketPattern']
            data_classification = policy['Parameters']['DataClassification']
            retention_rules = policy['Parameters']['RetentionRules']
            
            # Get matching buckets
            buckets = self.get_matching_s3_buckets(bucket_pattern, data_classification)
            
            for bucket in buckets:
                try:
                    # Apply lifecycle policy to bucket
                    lifecycle_result = self.apply_s3_lifecycle_policy(bucket, retention_rules)
                    
                    if lifecycle_result['applied']:
                        result['actions_taken'] += 1
                    
                    result['items_processed'] += 1
                    
                except Exception as e:
                    result['errors'].append({
                        'bucket': bucket,
                        'error': str(e)
                    })
        
        except Exception as e:
            result['errors'].append({'error': str(e)})
        
        return result
    
    def get_matching_s3_buckets(self, bucket_pattern, data_classification):
        """Get S3 buckets matching the retention policy criteria"""
        
        matching_buckets = []
        
        # List all buckets
        buckets = self.s3.list_buckets()
        
        for bucket in buckets['Buckets']:
            bucket_name = bucket['Name']
            
            # Check if bucket matches pattern
            if self.matches_pattern(bucket_name, bucket_pattern):
                # Check data classification
                bucket_classification = self.get_bucket_data_classification(bucket_name)
                
                if bucket_classification == data_classification:
                    matching_buckets.append(bucket_name)
        
        return matching_buckets
    
    def get_bucket_data_classification(self, bucket_name):
        """Get data classification for an S3 bucket"""
        
        try:
            # Get bucket tags
            response = self.s3.get_bucket_tagging(Bucket=bucket_name)
            tags = {tag['Key']: tag['Value'] for tag in response['TagSet']}
            
            return tags.get('DataClassification', 'internal').lower()
            
        except:
            return 'internal'  # Default classification
    
    def apply_s3_lifecycle_policy(self, bucket_name, retention_rules):
        """Apply lifecycle policy to S3 bucket"""
        
        result = {
            'bucket': bucket_name,
            'applied': False,
            'rules_created': 0
        }
        
        try:
            # Create lifecycle configuration
            lifecycle_rules = []
            
            for rule in retention_rules:
                lifecycle_rule = {
                    'ID': f"retention-rule-{rule['Name']}",
                    'Status': 'Enabled',
                    'Filter': {'Prefix': rule.get('Prefix', '')},
                    'Transitions': [],
                    'Expiration': {}
                }
                
                # Add transitions
                if 'Transitions' in rule:
                    for transition in rule['Transitions']:
                        lifecycle_rule['Transitions'].append({
                            'Days': transition['Days'],
                            'StorageClass': transition['StorageClass']
                        })
                
                # Add expiration
                if 'ExpirationDays' in rule:
                    lifecycle_rule['Expiration']['Days'] = rule['ExpirationDays']
                
                lifecycle_rules.append(lifecycle_rule)
                result['rules_created'] += 1
            
            # Apply lifecycle configuration
            self.s3.put_bucket_lifecycle_configuration(
                Bucket=bucket_name,
                LifecycleConfiguration={'Rules': lifecycle_rules}
            )
            
            result['applied'] = True
            
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def enforce_dynamodb_retention_policy(self, policy):
        """Enforce DynamoDB TTL retention policy"""
        
        result = {
            'policy_id': policy['PolicyId'],
            'actions_taken': 0,
            'items_processed': 0,
            'errors': []
        }
        
        try:
            # Get policy parameters
            table_pattern = policy['Parameters']['TablePattern']
            ttl_attribute = policy['Parameters']['TTLAttribute']
            retention_days = policy['Parameters']['RetentionDays']
            
            # Get matching tables
            tables = self.get_matching_dynamodb_tables(table_pattern)
            
            for table_name in tables:
                try:
                    # Enable TTL on table
                    ttl_result = self.enable_dynamodb_ttl(table_name, ttl_attribute)
                    
                    if ttl_result['enabled']:
                        result['actions_taken'] += 1
                    
                    result['items_processed'] += 1
                    
                except Exception as e:
                    result['errors'].append({
                        'table': table_name,
                        'error': str(e)
                    })
        
        except Exception as e:
            result['errors'].append({'error': str(e)})
        
        return result
    
    def enforce_logs_retention_policy(self, policy):
        """Enforce CloudWatch Logs retention policy"""
        
        result = {
            'policy_id': policy['PolicyId'],
            'actions_taken': 0,
            'items_processed': 0,
            'errors': []
        }
        
        try:
            # Get policy parameters
            log_group_pattern = policy['Parameters']['LogGroupPattern']
            retention_days = policy['Parameters']['RetentionDays']
            
            # Get matching log groups
            log_groups = self.get_matching_log_groups(log_group_pattern)
            
            for log_group in log_groups:
                try:
                    # Set retention policy
                    self.cloudwatch_logs.put_retention_policy(
                        logGroupName=log_group,
                        retentionInDays=retention_days
                    )
                    
                    result['actions_taken'] += 1
                    result['items_processed'] += 1
                    
                except Exception as e:
                    result['errors'].append({
                        'log_group': log_group,
                        'error': str(e)
                    })
        
        except Exception as e:
            result['errors'].append({'error': str(e)})
        
        return result
    
    def create_retention_policy(self, policy_definition):
        """Create a new data retention policy"""
        
        policy = {
            'PolicyId': f"POLICY-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'PolicyName': policy_definition['name'],
            'PolicyType': policy_definition['type'],
            'DataClassification': policy_definition['data_classification'],
            'Parameters': policy_definition['parameters'],
            'CreatedBy': policy_definition['created_by'],
            'CreatedAt': datetime.now().isoformat(),
            'PolicyStatus': 'active',
            'ComplianceRequirements': policy_definition.get('compliance_requirements', []),
            'BusinessJustification': policy_definition.get('business_justification', ''),
            'ReviewDate': (datetime.now() + timedelta(days=365)).isoformat()
        }
        
        # Store policy
        self.retention_policies_table.put_item(Item=policy)
        
        # Log policy creation
        self.log_policy_event(policy['PolicyId'], 'POLICY_CREATED', {
            'policy_name': policy['PolicyName'],
            'created_by': policy['CreatedBy']
        })
        
        return policy
    
    def validate_retention_compliance(self):
        """Validate compliance with all retention policies"""
        
        compliance_report = {
            'report_id': f"COMPLIANCE-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'generated_at': datetime.now().isoformat(),
            'policies_checked': 0,
            'compliant_policies': 0,
            'violations': [],
            'recommendations': []
        }
        
        # Get all active policies
        policies = self.get_active_retention_policies()
        compliance_report['policies_checked'] = len(policies)
        
        for policy in policies:
            try:
                # Check policy compliance
                compliance_result = self.check_policy_compliance(policy)
                
                if compliance_result['compliant']:
                    compliance_report['compliant_policies'] += 1
                else:
                    compliance_report['violations'].extend(compliance_result['violations'])
                
                # Add recommendations
                if compliance_result.get('recommendations'):
                    compliance_report['recommendations'].extend(compliance_result['recommendations'])
                
            except Exception as e:
                compliance_report['violations'].append({
                    'policy_id': policy['PolicyId'],
                    'violation_type': 'policy_check_error',
                    'description': str(e)
                })
        
        # Store compliance report
        self.store_compliance_report(compliance_report)
        
        return compliance_report
    
    def log_policy_event(self, policy_id, event_type, event_data):
        """Log retention policy events for audit purposes"""
        
        audit_record = {
            'PolicyId': policy_id,
            'EventId': f"{policy_id}-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'EventType': event_type,
            'EventData': event_data,
            'Timestamp': datetime.now().isoformat(),
            'TTL': int((datetime.now() + timedelta(days=2555)).timestamp())  # 7 years retention
        }
        
        try:
            self.retention_audit_table.put_item(Item=audit_record)
        except Exception as e:
            print(f"Error logging retention policy event: {str(e)}")
```

### Automated Compliance Monitoring
```python
def create_retention_compliance_monitor():
    """Create automated compliance monitoring for retention policies"""
    
    # Lambda function for compliance monitoring
    lambda_code = '''
import boto3
import json
from datetime import datetime, timedelta

def lambda_handler(event, context):
    """Monitor compliance with data retention policies"""
    
    # Initialize clients
    s3 = boto3.client('s3')
    dynamodb = boto3.resource('dynamodb')
    cloudwatch = boto3.client('cloudwatch')
    
    compliance_results = {
        's3_compliance': check_s3_compliance(s3),
        'dynamodb_compliance': check_dynamodb_compliance(dynamodb),
        'logs_compliance': check_logs_compliance(),
        'overall_compliance_score': 0
    }
    
    # Calculate overall compliance score
    total_checks = sum(len(result['checks']) for result in compliance_results.values() if isinstance(result, dict) and 'checks' in result)
    passed_checks = sum(len([c for c in result['checks'] if c['compliant']]) for result in compliance_results.values() if isinstance(result, dict) and 'checks' in result)
    
    if total_checks > 0:
        compliance_results['overall_compliance_score'] = (passed_checks / total_checks) * 100
    
    # Send compliance metrics to CloudWatch
    cloudwatch.put_metric_data(
        Namespace='DataRetention/Compliance',
        MetricData=[
            {
                'MetricName': 'ComplianceScore',
                'Value': compliance_results['overall_compliance_score'],
                'Unit': 'Percent',
                'Timestamp': datetime.now()
            },
            {
                'MetricName': 'TotalChecks',
                'Value': total_checks,
                'Unit': 'Count',
                'Timestamp': datetime.now()
            },
            {
                'MetricName': 'PassedChecks',
                'Value': passed_checks,
                'Unit': 'Count',
                'Timestamp': datetime.now()
            }
        ]
    )
    
    # Send alerts for low compliance
    if compliance_results['overall_compliance_score'] < 90:
        send_compliance_alert(compliance_results)
    
    return {
        'statusCode': 200,
        'body': json.dumps(compliance_results)
    }

def check_s3_compliance(s3):
    """Check S3 bucket compliance with retention policies"""
    
    compliance_result = {
        'service': 's3',
        'checks': [],
        'compliant_buckets': 0,
        'total_buckets': 0
    }
    
    try:
        # Get all buckets
        buckets = s3.list_buckets()
        compliance_result['total_buckets'] = len(buckets['Buckets'])
        
        for bucket in buckets['Buckets']:
            bucket_name = bucket['Name']
            
            # Check if bucket has lifecycle policy
            has_lifecycle = check_bucket_lifecycle_policy(s3, bucket_name)
            
            compliance_result['checks'].append({
                'resource': bucket_name,
                'check_type': 'lifecycle_policy',
                'compliant': has_lifecycle,
                'details': 'Lifecycle policy configured' if has_lifecycle else 'No lifecycle policy found'
            })
            
            if has_lifecycle:
                compliance_result['compliant_buckets'] += 1
    
    except Exception as e:
        compliance_result['error'] = str(e)
    
    return compliance_result

def check_bucket_lifecycle_policy(s3, bucket_name):
    """Check if S3 bucket has lifecycle policy configured"""
    
    try:
        s3.get_bucket_lifecycle_configuration(Bucket=bucket_name)
        return True
    except s3.exceptions.NoSuchLifecycleConfiguration:
        return False
    except Exception:
        return False

def send_compliance_alert(compliance_results):
    """Send alert for low compliance scores"""
    
    sns = boto3.client('sns')
    
    message = {
        'alert_type': 'retention_compliance_low',
        'compliance_score': compliance_results['overall_compliance_score'],
        'timestamp': datetime.now().isoformat(),
        'details': compliance_results
    }
    
    sns.publish(
        TopicArn='arn:aws:sns:region:account:retention-compliance-alerts',
        Message=json.dumps(message, indent=2),
        Subject=f'Low Retention Compliance Score: {compliance_results["overall_compliance_score"]:.1f}%'
    )
'''
    
    # Create Lambda function
    lambda_client = boto3.client('lambda')
    
    try:
        lambda_client.create_function(
            FunctionName='RetentionComplianceMonitor',
            Runtime='python3.9',
            Role='arn:aws:iam::ACCOUNT:role/RetentionComplianceRole',
            Handler='lambda_function.lambda_handler',
            Code={'ZipFile': lambda_code.encode()},
            Description='Monitor compliance with data retention policies',
            Timeout=300
        )
        
        # Set up scheduled execution
        events_client = boto3.client('events')
        
        events_client.put_rule(
            Name='RetentionComplianceSchedule',
            ScheduleExpression='rate(1 day)',  # Daily compliance check
            Description='Trigger daily retention compliance monitoring'
        )
        
        events_client.put_targets(
            Rule='RetentionComplianceSchedule',
            Targets=[
                {
                    'Id': '1',
                    'Arn': f'arn:aws:lambda:REGION:ACCOUNT:function:RetentionComplianceMonitor'
                }
            ]
        )
        
        print("Created retention compliance monitor")
        
    except Exception as e:
        print(f"Error creating compliance monitor: {str(e)}")
```

## Retention Policy Templates

### Standard Retention Policies
```yaml
Standard_Retention_Policies:
  Financial_Records:
    retention_period: 7_years
    storage_tiers:
      - tier: standard
        duration: 1_year
      - tier: glacier
        duration: 6_years
    compliance_requirements:
      - SOX
      - IRS_regulations
      
  Application_Logs:
    retention_period: 90_days
    storage_tiers:
      - tier: standard
        duration: 30_days
      - tier: glacier
        duration: 60_days
    compliance_requirements:
      - security_audit
      
  Customer_Data:
    retention_period: varies_by_jurisdiction
    storage_tiers:
      - tier: standard
        duration: 2_years
      - tier: glacier
        duration: 5_years
    compliance_requirements:
      - GDPR
      - CCPA
      - data_protection_laws
      
  Backup_Data:
    retention_period: 1_year
    storage_tiers:
      - tier: standard
        duration: 30_days
      - tier: glacier
        duration: 11_months
    compliance_requirements:
      - business_continuity
      - disaster_recovery
```

## Common Challenges and Solutions

### Challenge: Balancing Compliance and Cost

**Solution**: Implement tiered storage strategies that meet compliance requirements while optimizing costs. Use automated lifecycle policies to transition data to lower-cost storage tiers over time.

### Challenge: Complex Regulatory Requirements

**Solution**: Create comprehensive mapping of regulatory requirements to retention policies. Use automated compliance monitoring and reporting. Engage legal and compliance teams in policy development.

### Challenge: Data Discovery and Classification

**Solution**: Implement automated data discovery and classification tools. Use machine learning to identify and classify data types. Create comprehensive data inventory and mapping.

### Challenge: Cross-Service Data Management

**Solution**: Create unified data retention policies that span multiple AWS services. Use centralized orchestration and monitoring. Implement consistent tagging and metadata strategies.

### Challenge: Audit and Reporting Requirements

**Solution**: Implement comprehensive audit logging for all retention activities. Create automated compliance reporting and dashboards. Maintain detailed documentation and evidence of policy enforcement.

## Related Resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/cost_decommission_resources_data_retention.html">AWS Well-Architected Framework - Enforce data retention policies</a></li>
    <li><a href="https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html">Amazon S3 Lifecycle Management</a></li>
    <li><a href="https://docs.aws.amazon.com/amazons3/latest/userguide/storage-class-intro.html">Amazon S3 Storage Classes</a></li>
    <li><a href="https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html">DynamoDB Time To Live (TTL)</a></li>
    <li><a href="https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/Working-with-log-groups-and-streams.html">CloudWatch Logs Retention</a></li>
    <li><a href="https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.html">RDS Automated Backups</a></li>
    <li><a href="https://aws.amazon.com/blogs/aws-cost-management/">AWS Cost Management Blog</a></li>
    <li><a href="https://docs.aws.amazon.com/config/latest/developerguide/WhatIsConfig.html">AWS Config User Guide</a></li>
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
