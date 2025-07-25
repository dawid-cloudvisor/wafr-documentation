---
title: "SEC07-BP04: Define scalable data lifecycle management"
layout: default
parent: "SEC07 - How do you classify your data?"
grand_parent: Security
nav_order: 4
---

# SEC07-BP04: Define scalable data lifecycle management

## Overview

Effective data lifecycle management ensures that data is handled appropriately throughout its entire lifecycle, from creation to deletion, based on its classification level, business value, and regulatory requirements. Scalable lifecycle management automates data transitions, retention policies, and disposal processes while maintaining security and compliance requirements.

This best practice focuses on implementing automated, classification-aware lifecycle policies that can scale with your data growth while ensuring appropriate protection, cost optimization, and regulatory compliance throughout the data's lifecycle.

## Implementation Guidance

### 1. Define Data Lifecycle Stages

Establish clear lifecycle stages for different data classifications:

- **Creation**: Initial data ingestion and classification
- **Active Use**: Data in regular use with full accessibility
- **Infrequent Access**: Data accessed less frequently but still needed
- **Archive**: Long-term storage for compliance or historical purposes
- **Disposal**: Secure deletion when data is no longer needed

### 2. Implement Classification-Based Lifecycle Policies

Create lifecycle policies that align with data classification levels:

- **Public Data**: Basic lifecycle with cost optimization focus
- **Internal Data**: Standard retention with access controls
- **Confidential Data**: Extended retention with enhanced security
- **Restricted Data**: Maximum retention with comprehensive audit trails

### 3. Automate Lifecycle Transitions

Deploy automated systems for lifecycle management:

- **Policy-Driven Automation**: Automatic transitions based on predefined rules
- **Event-Driven Processing**: Lifecycle actions triggered by business events
- **Scheduled Operations**: Regular lifecycle maintenance and cleanup
- **Exception Handling**: Manage special cases and manual overrides

### 4. Ensure Compliance Throughout Lifecycle

Maintain compliance requirements across all lifecycle stages:

- **Retention Requirements**: Meet legal and regulatory retention periods
- **Data Sovereignty**: Ensure data remains in required geographic locations
- **Audit Trails**: Maintain complete records of lifecycle actions
- **Secure Disposal**: Implement certified data destruction methods

### 5. Optimize Costs Across Lifecycle

Balance security requirements with cost optimization:

- **Storage Tiering**: Move data to appropriate storage classes
- **Compression and Deduplication**: Reduce storage costs while maintaining accessibility
- **Resource Optimization**: Right-size compute and storage resources
- **Monitoring and Alerting**: Track lifecycle costs and performance

### 6. Enable Lifecycle Governance and Monitoring

Implement governance controls for lifecycle management:

- **Policy Management**: Centralized lifecycle policy definition and updates
- **Compliance Monitoring**: Continuous monitoring of lifecycle compliance
- **Performance Metrics**: Track lifecycle efficiency and effectiveness
- **Stakeholder Reporting**: Regular reports on lifecycle management status

## Implementation Examples

### Example 1: Classification-Based S3 Lifecycle Management

```python
# s3_lifecycle_manager.py
import boto3
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class LifecycleRule:
    rule_id: str
    classification_level: str
    transitions: List[Dict[str, Any]]
    expiration_days: Optional[int]
    noncurrent_version_expiration_days: Optional[int]
    abort_incomplete_multipart_upload_days: int
    filter_tags: Dict[str, str]

@dataclass
class LifecyclePolicy:
    policy_name: str
    description: str
    rules: List[LifecycleRule]
    compliance_frameworks: List[str]

class S3LifecycleManager:
    """
    Manages S3 lifecycle policies based on data classification
    """
    
    def __init__(self, region: str = 'us-east-1'):
        self.region = region
        self.s3_client = boto3.client('s3', region_name=region)
        self.dynamodb = boto3.resource('dynamodb', region_name=region)
        
        # Lifecycle tracking table
        self.lifecycle_table = self.dynamodb.Table('data-lifecycle-tracking')
        
        # Classification-based lifecycle policies
        self.lifecycle_policies = self._define_classification_lifecycle_policies()
    
    def _define_classification_lifecycle_policies(self) -> Dict[str, LifecyclePolicy]:
        """
        Define lifecycle policies for each classification level
        """
        return {
            'public': LifecyclePolicy(
                policy_name='PublicDataLifecycle',
                description='Lifecycle policy for public data with cost optimization focus',
                rules=[
                    LifecycleRule(
                        rule_id='public-data-lifecycle',
                        classification_level='public',
                        transitions=[
                            {'Days': 30, 'StorageClass': 'STANDARD_IA'},
                            {'Days': 90, 'StorageClass': 'GLACIER'},
                            {'Days': 365, 'StorageClass': 'DEEP_ARCHIVE'}
                        ],
                        expiration_days=2555,  # 7 years
                        noncurrent_version_expiration_days=30,
                        abort_incomplete_multipart_upload_days=7,
                        filter_tags={'DataClassification': 'public'}
                    )
                ],
                compliance_frameworks=[]
            ),
            
            'internal': LifecyclePolicy(
                policy_name='InternalDataLifecycle',
                description='Lifecycle policy for internal data with standard retention',
                rules=[
                    LifecycleRule(
                        rule_id='internal-data-lifecycle',
                        classification_level='internal',
                        transitions=[
                            {'Days': 90, 'StorageClass': 'STANDARD_IA'},
                            {'Days': 365, 'StorageClass': 'GLACIER'},
                            {'Days': 1095, 'StorageClass': 'DEEP_ARCHIVE'}  # 3 years
                        ],
                        expiration_days=2555,  # 7 years
                        noncurrent_version_expiration_days=90,
                        abort_incomplete_multipart_upload_days=7,
                        filter_tags={'DataClassification': 'internal'}
                    )
                ],
                compliance_frameworks=['SOX']
            ),
            
            'confidential': LifecyclePolicy(
                policy_name='ConfidentialDataLifecycle',
                description='Lifecycle policy for confidential data with extended retention',
                rules=[
                    LifecycleRule(
                        rule_id='confidential-data-lifecycle',
                        classification_level='confidential',
                        transitions=[
                            {'Days': 180, 'StorageClass': 'STANDARD_IA'},
                            {'Days': 730, 'StorageClass': 'GLACIER'},  # 2 years
                            {'Days': 1825, 'StorageClass': 'DEEP_ARCHIVE'}  # 5 years
                        ],
                        expiration_days=3650,  # 10 years
                        noncurrent_version_expiration_days=365,
                        abort_incomplete_multipart_upload_days=14,
                        filter_tags={'DataClassification': 'confidential'}
                    )
                ],
                compliance_frameworks=['GDPR', 'HIPAA']
            ),
            
            'restricted': LifecyclePolicy(
                policy_name='RestrictedDataLifecycle',
                description='Lifecycle policy for restricted data with maximum retention',
                rules=[
                    LifecycleRule(
                        rule_id='restricted-data-lifecycle',
                        classification_level='restricted',
                        transitions=[
                            {'Days': 365, 'StorageClass': 'STANDARD_IA'},  # 1 year
                            {'Days': 1095, 'StorageClass': 'GLACIER'},  # 3 years
                            {'Days': 2555, 'StorageClass': 'DEEP_ARCHIVE'}  # 7 years
                        ],
                        expiration_days=None,  # No automatic expiration
                        noncurrent_version_expiration_days=730,  # 2 years
                        abort_incomplete_multipart_upload_days=30,
                        filter_tags={'DataClassification': 'restricted'}
                    )
                ],
                compliance_frameworks=['PCI_DSS', 'HIPAA', 'GDPR']
            )
        }
    
    def apply_lifecycle_policy_to_bucket(self, bucket_name: str, classification_level: str) -> Dict[str, Any]:
        """
        Apply classification-based lifecycle policy to S3 bucket
        """
        try:
            if classification_level not in self.lifecycle_policies:
                return {
                    'status': 'error',
                    'message': f'Unknown classification level: {classification_level}'
                }
            
            policy = self.lifecycle_policies[classification_level]
            
            # Convert lifecycle rules to S3 format
            s3_rules = []
            for rule in policy.rules:
                s3_rule = {
                    'ID': rule.rule_id,
                    'Status': 'Enabled',
                    'Filter': {
                        'And': {
                            'Tags': [
                                {'Key': k, 'Value': v} for k, v in rule.filter_tags.items()
                            ]
                        }
                    },
                    'Transitions': rule.transitions,
                    'AbortIncompleteMultipartUpload': {
                        'DaysAfterInitiation': rule.abort_incomplete_multipart_upload_days
                    }
                }
                
                # Add expiration if specified
                if rule.expiration_days:
                    s3_rule['Expiration'] = {'Days': rule.expiration_days}
                
                # Add noncurrent version expiration
                if rule.noncurrent_version_expiration_days:
                    s3_rule['NoncurrentVersionExpiration'] = {
                        'NoncurrentDays': rule.noncurrent_version_expiration_days
                    }
                
                s3_rules.append(s3_rule)
            
            # Apply lifecycle configuration
            self.s3_client.put_bucket_lifecycle_configuration(
                Bucket=bucket_name,
                LifecycleConfiguration={'Rules': s3_rules}
            )
            
            # Track lifecycle policy application
            self._track_lifecycle_policy_application(bucket_name, policy)
            
            logger.info(f"Applied {classification_level} lifecycle policy to bucket {bucket_name}")
            
            return {
                'status': 'success',
                'bucket': bucket_name,
                'classification': classification_level,
                'policy_name': policy.policy_name,
                'rules_applied': len(s3_rules)
            }
            
        except Exception as e:
            logger.error(f"Error applying lifecycle policy to {bucket_name}: {str(e)}")
            return {
                'status': 'error',
                'bucket': bucket_name,
                'message': str(e)
            }
    
    def _track_lifecycle_policy_application(self, bucket_name: str, policy: LifecyclePolicy):
        """
        Track lifecycle policy application in DynamoDB
        """
        try:
            self.lifecycle_table.put_item(
                Item={
                    'resource_arn': f'arn:aws:s3:::{bucket_name}',
                    'policy_application_timestamp': datetime.utcnow().isoformat(),
                    'policy_name': policy.policy_name,
                    'classification_level': policy.rules[0].classification_level,
                    'compliance_frameworks': policy.compliance_frameworks,
                    'rules_count': len(policy.rules),
                    'ttl': int((datetime.utcnow() + timedelta(days=365)).timestamp())
                }
            )
        except Exception as e:
            logger.error(f"Error tracking lifecycle policy application: {str(e)}")
    
    def create_custom_lifecycle_policy(self, 
                                     policy_name: str,
                                     classification_level: str,
                                     custom_rules: List[Dict[str, Any]]) -> LifecyclePolicy:
        """
        Create custom lifecycle policy for specific requirements
        """
        rules = []
        for rule_config in custom_rules:
            rule = LifecycleRule(
                rule_id=rule_config.get('rule_id', f'{policy_name}-rule'),
                classification_level=classification_level,
                transitions=rule_config.get('transitions', []),
                expiration_days=rule_config.get('expiration_days'),
                noncurrent_version_expiration_days=rule_config.get('noncurrent_version_expiration_days'),
                abort_incomplete_multipart_upload_days=rule_config.get('abort_incomplete_multipart_upload_days', 7),
                filter_tags=rule_config.get('filter_tags', {'DataClassification': classification_level})
            )
            rules.append(rule)
        
        custom_policy = LifecyclePolicy(
            policy_name=policy_name,
            description=f'Custom lifecycle policy for {classification_level} data',
            rules=rules,
            compliance_frameworks=[]
        )
        
        return custom_policy
    
    def audit_bucket_lifecycle_compliance(self, bucket_name: str) -> Dict[str, Any]:
        """
        Audit bucket lifecycle configuration for compliance
        """
        try:
            # Get bucket lifecycle configuration
            try:
                lifecycle_response = self.s3_client.get_bucket_lifecycle_configuration(Bucket=bucket_name)
                rules = lifecycle_response.get('Rules', [])
            except self.s3_client.exceptions.NoSuchLifecycleConfiguration:
                return {
                    'bucket': bucket_name,
                    'compliance_status': 'non_compliant',
                    'issues': ['No lifecycle configuration found'],
                    'recommendations': ['Apply appropriate lifecycle policy based on data classification']
                }
            
            # Get bucket classification
            try:
                tags_response = self.s3_client.get_bucket_tagging(Bucket=bucket_name)
                tags = {tag['Key']: tag['Value'] for tag in tags_response['TagSet']}
                classification = tags.get('DataClassification', 'unknown')
            except self.s3_client.exceptions.NoSuchTagSet:
                classification = 'unknown'
            
            # Audit compliance
            audit_results = {
                'bucket': bucket_name,
                'classification': classification,
                'rules_count': len(rules),
                'compliance_status': 'compliant',
                'issues': [],
                'recommendations': []
            }
            
            if classification == 'unknown':
                audit_results['issues'].append('Bucket classification not found')
                audit_results['recommendations'].append('Apply data classification tags')
                audit_results['compliance_status'] = 'non_compliant'
            
            if classification in self.lifecycle_policies:
                expected_policy = self.lifecycle_policies[classification]
                
                # Check if lifecycle rules match expected policy
                compliance_issues = self._validate_lifecycle_rules(rules, expected_policy)
                if compliance_issues:
                    audit_results['issues'].extend(compliance_issues)
                    audit_results['compliance_status'] = 'non_compliant'
                    audit_results['recommendations'].append(f'Update lifecycle policy to match {classification} requirements')
            
            return audit_results
            
        except Exception as e:
            logger.error(f"Error auditing bucket lifecycle compliance: {str(e)}")
            return {
                'bucket': bucket_name,
                'compliance_status': 'error',
                'error': str(e)
            }
    
    def _validate_lifecycle_rules(self, actual_rules: List[Dict[str, Any]], expected_policy: LifecyclePolicy) -> List[str]:
        """
        Validate actual lifecycle rules against expected policy
        """
        issues = []
        
        if len(actual_rules) != len(expected_policy.rules):
            issues.append(f'Expected {len(expected_policy.rules)} rules, found {len(actual_rules)}')
        
        for expected_rule in expected_policy.rules:
            # Find matching actual rule
            matching_rule = None
            for actual_rule in actual_rules:
                if actual_rule.get('ID') == expected_rule.rule_id:
                    matching_rule = actual_rule
                    break
            
            if not matching_rule:
                issues.append(f'Missing lifecycle rule: {expected_rule.rule_id}')
                continue
            
            # Validate transitions
            actual_transitions = matching_rule.get('Transitions', [])
            if len(actual_transitions) != len(expected_rule.transitions):
                issues.append(f'Rule {expected_rule.rule_id}: Expected {len(expected_rule.transitions)} transitions, found {len(actual_transitions)}')
            
            # Validate expiration
            if expected_rule.expiration_days:
                actual_expiration = matching_rule.get('Expiration', {}).get('Days')
                if actual_expiration != expected_rule.expiration_days:
                    issues.append(f'Rule {expected_rule.rule_id}: Expected expiration {expected_rule.expiration_days} days, found {actual_expiration}')
        
        return issues
    
    def generate_lifecycle_report(self, bucket_names: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Generate comprehensive lifecycle management report
        """
        try:
            if bucket_names is None:
                # Get all buckets
                buckets_response = self.s3_client.list_buckets()
                bucket_names = [bucket['Name'] for bucket in buckets_response['Buckets']]
            
            report = {
                'report_timestamp': datetime.utcnow().isoformat(),
                'total_buckets': len(bucket_names),
                'compliance_summary': {
                    'compliant': 0,
                    'non_compliant': 0,
                    'error': 0
                },
                'classification_distribution': {},
                'bucket_details': [],
                'recommendations': []
            }
            
            for bucket_name in bucket_names:
                audit_result = self.audit_bucket_lifecycle_compliance(bucket_name)
                report['bucket_details'].append(audit_result)
                
                # Update compliance summary
                status = audit_result.get('compliance_status', 'error')
                report['compliance_summary'][status] += 1
                
                # Update classification distribution
                classification = audit_result.get('classification', 'unknown')
                report['classification_distribution'][classification] = report['classification_distribution'].get(classification, 0) + 1
            
            # Generate overall recommendations
            if report['compliance_summary']['non_compliant'] > 0:
                report['recommendations'].append('Review and update lifecycle policies for non-compliant buckets')
            
            if report['classification_distribution'].get('unknown', 0) > 0:
                report['recommendations'].append('Apply data classification tags to unclassified buckets')
            
            return report
            
        except Exception as e:
            logger.error(f"Error generating lifecycle report: {str(e)}")
            return {
                'error': str(e),
                'report_timestamp': datetime.utcnow().isoformat()
            }
    
    def optimize_lifecycle_costs(self, bucket_name: str) -> Dict[str, Any]:
        """
        Analyze and optimize lifecycle costs for a bucket
        """
        try:
            # Get bucket size and access patterns (simplified)
            cloudwatch = boto3.client('cloudwatch', region_name=self.region)
            
            # Get bucket size metrics
            size_response = cloudwatch.get_metric_statistics(
                Namespace='AWS/S3',
                MetricName='BucketSizeBytes',
                Dimensions=[
                    {'Name': 'BucketName', 'Value': bucket_name},
                    {'Name': 'StorageType', 'Value': 'StandardStorage'}
                ],
                StartTime=datetime.utcnow() - timedelta(days=30),
                EndTime=datetime.utcnow(),
                Period=86400,  # 1 day
                Statistics=['Average']
            )
            
            # Calculate current storage costs (simplified)
            current_size_gb = 0
            if size_response['Datapoints']:
                current_size_bytes = size_response['Datapoints'][-1]['Average']
                current_size_gb = current_size_bytes / (1024**3)
            
            # Get current lifecycle configuration
            try:
                lifecycle_response = self.s3_client.get_bucket_lifecycle_configuration(Bucket=bucket_name)
                has_lifecycle = True
            except self.s3_client.exceptions.NoSuchLifecycleConfiguration:
                has_lifecycle = False
            
            # Calculate potential savings
            optimization_results = {
                'bucket': bucket_name,
                'current_size_gb': round(current_size_gb, 2),
                'has_lifecycle_policy': has_lifecycle,
                'optimization_recommendations': [],
                'estimated_monthly_savings': 0
            }
            
            if not has_lifecycle:
                # Estimate savings from implementing lifecycle policy
                standard_cost_per_gb = 0.023  # Approximate S3 Standard cost
                ia_cost_per_gb = 0.0125  # Approximate S3 IA cost
                glacier_cost_per_gb = 0.004  # Approximate Glacier cost
                
                # Assume 30% moves to IA after 30 days, 50% to Glacier after 90 days
                potential_savings = (current_size_gb * 0.3 * (standard_cost_per_gb - ia_cost_per_gb)) + \
                                  (current_size_gb * 0.5 * (standard_cost_per_gb - glacier_cost_per_gb))
                
                optimization_results['estimated_monthly_savings'] = round(potential_savings, 2)
                optimization_results['optimization_recommendations'].append(
                    'Implement lifecycle policy to transition data to lower-cost storage classes'
                )
            
            if current_size_gb > 1000:  # Large bucket
                optimization_results['optimization_recommendations'].append(
                    'Consider implementing Intelligent Tiering for automatic cost optimization'
                )
            
            return optimization_results
            
        except Exception as e:
            logger.error(f"Error optimizing lifecycle costs: {str(e)}")
            return {
                'bucket': bucket_name,
                'error': str(e)
            }
    
    def schedule_lifecycle_maintenance(self, schedule_expression: str = 'rate(1 day)') -> Dict[str, Any]:
        """
        Schedule automated lifecycle maintenance using EventBridge and Lambda
        """
        try:
            # This would create EventBridge rule and Lambda function for maintenance
            # Implementation would include:
            # 1. Create Lambda function for lifecycle maintenance
            # 2. Create EventBridge rule with schedule
            # 3. Set up permissions
            
            maintenance_config = {
                'schedule_expression': schedule_expression,
                'lambda_function': 'lifecycle-maintenance-function',
                'eventbridge_rule': 'lifecycle-maintenance-schedule',
                'status': 'configured'
            }
            
            logger.info(f"Scheduled lifecycle maintenance with expression: {schedule_expression}")
            
            return maintenance_config
            
        except Exception as e:
            logger.error(f"Error scheduling lifecycle maintenance: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }

# Example usage
if __name__ == "__main__":
    # Initialize lifecycle manager
    manager = S3LifecycleManager()
    
    # Apply lifecycle policy to a bucket
    result = manager.apply_lifecycle_policy_to_bucket('my-data-bucket', 'confidential')
    print(f"Lifecycle policy application result: {result}")
    
    # Audit bucket compliance
    audit_result = manager.audit_bucket_lifecycle_compliance('my-data-bucket')
    print(f"Audit result: {audit_result}")
    
    # Generate lifecycle report
    report = manager.generate_lifecycle_report(['my-data-bucket', 'another-bucket'])
    print(f"Lifecycle report: {json.dumps(report, indent=2)}")
    
    # Optimize costs
    cost_optimization = manager.optimize_lifecycle_costs('my-data-bucket')
    print(f"Cost optimization: {cost_optimization}")
```

### Example 2: Multi-Service Data Lifecycle Orchestration

```python
# multi_service_lifecycle.py
import boto3
import json
from typing import Dict, List, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

@dataclass
class DataAsset:
    resource_arn: str
    service_type: str
    classification: str
    creation_date: datetime
    last_accessed: datetime
    size_bytes: int
    compliance_requirements: List[str]

class MultiServiceLifecycleManager:
    """
    Manages data lifecycle across multiple AWS services
    """
    
    def __init__(self, region: str = 'us-east-1'):
        self.region = region
        self.s3_client = boto3.client('s3', region_name=region)
        self.rds_client = boto3.client('rds', region_name=region)
        self.dynamodb_client = boto3.client('dynamodb', region_name=region)
        self.backup_client = boto3.client('backup', region_name=region)
        self.stepfunctions_client = boto3.client('stepfunctions', region_name=region)
        
        # Service-specific lifecycle policies
        self.service_policies = {
            's3': self._get_s3_lifecycle_policies(),
            'rds': self._get_rds_lifecycle_policies(),
            'dynamodb': self._get_dynamodb_lifecycle_policies()
        }
    
    def _get_s3_lifecycle_policies(self) -> Dict[str, Dict[str, Any]]:
        """S3 lifecycle policies by classification"""
        return {
            'public': {
                'transitions': [
                    {'days': 30, 'storage_class': 'STANDARD_IA'},
                    {'days': 90, 'storage_class': 'GLACIER'},
                    {'days': 365, 'storage_class': 'DEEP_ARCHIVE'}
                ],
                'expiration_days': 2555
            },
            'confidential': {
                'transitions': [
                    {'days': 180, 'storage_class': 'STANDARD_IA'},
                    {'days': 730, 'storage_class': 'GLACIER'},
                    {'days': 1825, 'storage_class': 'DEEP_ARCHIVE'}
                ],
                'expiration_days': 3650
            },
            'restricted': {
                'transitions': [
                    {'days': 365, 'storage_class': 'STANDARD_IA'},
                    {'days': 1095, 'storage_class': 'GLACIER'}
                ],
                'expiration_days': None  # No automatic expiration
            }
        }
    
    def _get_rds_lifecycle_policies(self) -> Dict[str, Dict[str, Any]]:
        """RDS lifecycle policies by classification"""
        return {
            'public': {
                'backup_retention_days': 7,
                'snapshot_retention_days': 30,
                'archive_after_days': 365
            },
            'confidential': {
                'backup_retention_days': 35,
                'snapshot_retention_days': 365,
                'archive_after_days': 1095
            },
            'restricted': {
                'backup_retention_days': 35,
                'snapshot_retention_days': 2555,
                'archive_after_days': None
            }
        }
    
    def _get_dynamodb_lifecycle_policies(self) -> Dict[str, Dict[str, Any]]:
        """DynamoDB lifecycle policies by classification"""
        return {
            'public': {
                'point_in_time_recovery': False,
                'backup_retention_days': 30
            },
            'confidential': {
                'point_in_time_recovery': True,
                'backup_retention_days': 365
            },
            'restricted': {
                'point_in_time_recovery': True,
                'backup_retention_days': 2555
            }
        }
    
    def discover_data_assets(self) -> List[DataAsset]:
        """Discover data assets across AWS services"""
        assets = []
        
        # Discover S3 buckets
        try:
            buckets = self.s3_client.list_buckets()['Buckets']
            for bucket in buckets:
                classification = self._get_resource_classification(f"arn:aws:s3:::{bucket['Name']}")
                size = self._get_s3_bucket_size(bucket['Name'])
                
                asset = DataAsset(
                    resource_arn=f"arn:aws:s3:::{bucket['Name']}",
                    service_type='s3',
                    classification=classification,
                    creation_date=bucket['CreationDate'],
                    last_accessed=datetime.utcnow(),  # Simplified
                    size_bytes=size,
                    compliance_requirements=self._get_compliance_requirements(classification)
                )
                assets.append(asset)
        except Exception as e:
            logger.error(f"Error discovering S3 assets: {str(e)}")
        
        # Discover RDS instances
        try:
            db_instances = self.rds_client.describe_db_instances()['DBInstances']
            for db in db_instances:
                classification = self._get_resource_classification(db['DBInstanceArn'])
                
                asset = DataAsset(
                    resource_arn=db['DBInstanceArn'],
                    service_type='rds',
                    classification=classification,
                    creation_date=db['InstanceCreateTime'],
                    last_accessed=datetime.utcnow(),  # Simplified
                    size_bytes=db.get('AllocatedStorage', 0) * 1024**3,  # Convert GB to bytes
                    compliance_requirements=self._get_compliance_requirements(classification)
                )
                assets.append(asset)
        except Exception as e:
            logger.error(f"Error discovering RDS assets: {str(e)}")
        
        return assets
    
    def apply_lifecycle_policies(self, assets: List[DataAsset]) -> Dict[str, Any]:
        """Apply lifecycle policies to discovered assets"""
        results = {
            'total_assets': len(assets),
            'policies_applied': 0,
            'errors': [],
            'service_breakdown': {}
        }
        
        for asset in assets:
            try:
                if asset.service_type == 's3':
                    self._apply_s3_lifecycle_policy(asset)
                elif asset.service_type == 'rds':
                    self._apply_rds_lifecycle_policy(asset)
                elif asset.service_type == 'dynamodb':
                    self._apply_dynamodb_lifecycle_policy(asset)
                
                results['policies_applied'] += 1
                
                # Update service breakdown
                service = asset.service_type
                if service not in results['service_breakdown']:
                    results['service_breakdown'][service] = 0
                results['service_breakdown'][service] += 1
                
            except Exception as e:
                results['errors'].append({
                    'resource_arn': asset.resource_arn,
                    'error': str(e)
                })
        
        return results
    
    def _apply_s3_lifecycle_policy(self, asset: DataAsset):
        """Apply S3 lifecycle policy"""
        bucket_name = asset.resource_arn.split(':')[-1]
        policy = self.service_policies['s3'].get(asset.classification, self.service_policies['s3']['public'])
        
        rules = [{
            'ID': f'{asset.classification}-lifecycle',
            'Status': 'Enabled',
            'Filter': {'Tag': {'Key': 'DataClassification', 'Value': asset.classification}},
            'Transitions': [
                {'Days': t['days'], 'StorageClass': t['storage_class']} 
                for t in policy['transitions']
            ]
        }]
        
        if policy['expiration_days']:
            rules[0]['Expiration'] = {'Days': policy['expiration_days']}
        
        self.s3_client.put_bucket_lifecycle_configuration(
            Bucket=bucket_name,
            LifecycleConfiguration={'Rules': rules}
        )
    
    def _apply_rds_lifecycle_policy(self, asset: DataAsset):
        """Apply RDS lifecycle policy"""
        db_identifier = asset.resource_arn.split(':')[-1]
        policy = self.service_policies['rds'].get(asset.classification, self.service_policies['rds']['public'])
        
        # Update backup retention
        self.rds_client.modify_db_instance(
            DBInstanceIdentifier=db_identifier,
            BackupRetentionPeriod=policy['backup_retention_days'],
            ApplyImmediately=False
        )
    
    def _apply_dynamodb_lifecycle_policy(self, asset: DataAsset):
        """Apply DynamoDB lifecycle policy"""
        table_name = asset.resource_arn.split('/')[-1]
        policy = self.service_policies['dynamodb'].get(asset.classification, self.service_policies['dynamodb']['public'])
        
        # Update point-in-time recovery
        if policy['point_in_time_recovery']:
            self.dynamodb_client.update_continuous_backups(
                TableName=table_name,
                PointInTimeRecoverySpecification={'PointInTimeRecoveryEnabled': True}
            )
    
    def _get_resource_classification(self, resource_arn: str) -> str:
        """Get resource classification from tags"""
        try:
            if 's3' in resource_arn:
                bucket_name = resource_arn.split(':')[-1]
                tags = self.s3_client.get_bucket_tagging(Bucket=bucket_name)['TagSet']
                for tag in tags:
                    if tag['Key'] == 'DataClassification':
                        return tag['Value']
        except:
            pass
        return 'internal'  # Default classification
    
    def _get_s3_bucket_size(self, bucket_name: str) -> int:
        """Get S3 bucket size in bytes"""
        try:
            cloudwatch = boto3.client('cloudwatch', region_name=self.region)
            response = cloudwatch.get_metric_statistics(
                Namespace='AWS/S3',
                MetricName='BucketSizeBytes',
                Dimensions=[
                    {'Name': 'BucketName', 'Value': bucket_name},
                    {'Name': 'StorageType', 'Value': 'StandardStorage'}
                ],
                StartTime=datetime.utcnow() - timedelta(days=2),
                EndTime=datetime.utcnow(),
                Period=86400,
                Statistics=['Average']
            )
            if response['Datapoints']:
                return int(response['Datapoints'][-1]['Average'])
        except:
            pass
        return 0
    
    def _get_compliance_requirements(self, classification: str) -> List[str]:
        """Get compliance requirements for classification"""
        compliance_map = {
            'public': [],
            'internal': ['SOX'],
            'confidential': ['GDPR', 'HIPAA'],
            'restricted': ['PCI_DSS', 'HIPAA', 'GDPR']
        }
        return compliance_map.get(classification, [])
    
    def create_lifecycle_workflow(self) -> Dict[str, Any]:
        """Create Step Functions workflow for lifecycle management"""
        workflow_definition = {
            "Comment": "Multi-service data lifecycle management workflow",
            "StartAt": "DiscoverAssets",
            "States": {
                "DiscoverAssets": {
                    "Type": "Task",
                    "Resource": f"arn:aws:lambda:{self.region}:{self._get_account_id()}:function:discover-data-assets",
                    "Next": "ApplyPolicies"
                },
                "ApplyPolicies": {
                    "Type": "Map",
                    "ItemsPath": "$.assets",
                    "Iterator": {
                        "StartAt": "ApplyLifecyclePolicy",
                        "States": {
                            "ApplyLifecyclePolicy": {
                                "Type": "Task",
                                "Resource": f"arn:aws:lambda:{self.region}:{self._get_account_id()}:function:apply-lifecycle-policy",
                                "End": True
                            }
                        }
                    },
                    "Next": "GenerateReport"
                },
                "GenerateReport": {
                    "Type": "Task",
                    "Resource": f"arn:aws:lambda:{self.region}:{self._get_account_id()}:function:generate-lifecycle-report",
                    "End": True
                }
            }
        }
        
        try:
            response = self.stepfunctions_client.create_state_machine(
                name='DataLifecycleManagement',
                definition=json.dumps(workflow_definition),
                roleArn=f'arn:aws:iam::{self._get_account_id()}:role/StepFunctionsLifecycleRole'
            )
            
            return {
                'state_machine_arn': response['stateMachineArn'],
                'status': 'created'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _get_account_id(self) -> str:
        """Get AWS account ID"""
        return boto3.client('sts').get_caller_identity()['Account']

# Example usage
if __name__ == "__main__":
    manager = MultiServiceLifecycleManager()
    
    # Discover assets
    assets = manager.discover_data_assets()
    print(f"Discovered {len(assets)} data assets")
    
    # Apply lifecycle policies
    results = manager.apply_lifecycle_policies(assets)
    print(f"Applied policies to {results['policies_applied']} assets")
    
    # Create workflow
    workflow_result = manager.create_lifecycle_workflow()
    print(f"Workflow creation: {workflow_result}")
```

### Example 3: Compliance-Driven Lifecycle Automation

```yaml
# compliance-lifecycle-automation.yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Compliance-driven data lifecycle automation'

Parameters:
  Environment:
    Type: String
    Default: 'prod'
    AllowedValues: ['dev', 'staging', 'prod']
  
  ComplianceFramework:
    Type: String
    Default: 'GDPR'
    AllowedValues: ['GDPR', 'HIPAA', 'PCI_DSS', 'SOX']

Resources:
  # DynamoDB table for lifecycle tracking
  LifecycleTrackingTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: !Sub '${Environment}-lifecycle-tracking'
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: resource_arn
          AttributeType: S
        - AttributeName: lifecycle_stage
          AttributeType: S
        - AttributeName: compliance_deadline
          AttributeType: S
      KeySchema:
        - AttributeName: resource_arn
          KeyType: HASH
        - AttributeName: lifecycle_stage
          KeyType: RANGE
      GlobalSecondaryIndexes:
        - IndexName: ComplianceDeadlineIndex
          KeySchema:
            - AttributeName: compliance_deadline
              KeyType: HASH
          Projection:
            ProjectionType: ALL
      TimeToLiveSpecification:
        AttributeName: ttl
        Enabled: true

  # Lambda function for lifecycle enforcement
  LifecycleEnforcementFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: !Sub '${Environment}-lifecycle-enforcement'
      Runtime: python3.9
      Handler: index.lambda_handler
      Role: !GetAtt LifecycleEnforcementRole.Arn
      Timeout: 900
      Environment:
        Variables:
          TRACKING_TABLE: !Ref LifecycleTrackingTable
          COMPLIANCE_FRAMEWORK: !Ref ComplianceFramework
      Code:
        ZipFile: |
          import boto3
          import json
          import os
          from datetime import datetime, timedelta
          
          def lambda_handler(event, context):
              """Enforce lifecycle policies based on compliance requirements"""
              
              s3_client = boto3.client('s3')
              dynamodb = boto3.resource('dynamodb')
              table = dynamodb.Table(os.environ['TRACKING_TABLE'])
              
              compliance_framework = os.environ['COMPLIANCE_FRAMEWORK']
              
              # Define compliance-based retention periods
              retention_policies = {
                  'GDPR': {
                      'personal_data': 2555,  # 7 years max
                      'consent_records': 1095,  # 3 years
                      'processing_logs': 365  # 1 year
                  },
                  'HIPAA': {
                      'phi_data': 2190,  # 6 years
                      'audit_logs': 2190,  # 6 years
                      'access_logs': 2190  # 6 years
                  },
                  'PCI_DSS': {
                      'cardholder_data': 365,  # 1 year
                      'audit_trails': 365,  # 1 year
                      'vulnerability_scans': 365  # 1 year
                  }
              }
              
              try:
                  # Get resources approaching compliance deadlines
                  deadline_threshold = (datetime.utcnow() + timedelta(days=30)).isoformat()
                  
                  response = table.query(
                      IndexName='ComplianceDeadlineIndex',
                      KeyConditionExpression='compliance_deadline < :threshold',
                      ExpressionAttributeValues={':threshold': deadline_threshold}
                  )
                  
                  results = {
                      'resources_processed': 0,
                      'actions_taken': [],
                      'errors': []
                  }
                  
                  for item in response['Items']:
                      try:
                          resource_arn = item['resource_arn']
                          data_type = item.get('data_type', 'general')
                          
                          # Apply compliance-specific actions
                          if 's3' in resource_arn:
                              action_result = apply_s3_compliance_action(
                                  s3_client, resource_arn, data_type, compliance_framework
                              )
                              results['actions_taken'].append(action_result)
                          
                          results['resources_processed'] += 1
                          
                      except Exception as e:
                          results['errors'].append({
                              'resource': item.get('resource_arn', 'unknown'),
                              'error': str(e)
                          })
                  
                  return {
                      'statusCode': 200,
                      'body': json.dumps(results)
                  }
                  
              except Exception as e:
                  return {
                      'statusCode': 500,
                      'body': json.dumps({'error': str(e)})
                  }
          
          def apply_s3_compliance_action(s3_client, resource_arn, data_type, framework):
              """Apply compliance-specific action to S3 resource"""
              bucket_name = resource_arn.split(':')[-1]
              
              if framework == 'GDPR' and data_type == 'personal_data':
                  # Apply GDPR-specific lifecycle policy
                  lifecycle_config = {
                      'Rules': [{
                          'ID': 'GDPR-PersonalData-Lifecycle',
                          'Status': 'Enabled',
                          'Filter': {'Tag': {'Key': 'DataType', 'Value': 'personal_data'}},
                          'Expiration': {'Days': 2555}  # 7 years max retention
                      }]
                  }
                  
                  s3_client.put_bucket_lifecycle_configuration(
                      Bucket=bucket_name,
                      LifecycleConfiguration=lifecycle_config
                  )
                  
                  return {
                      'resource': resource_arn,
                      'action': 'GDPR lifecycle policy applied',
                      'retention_days': 2555
                  }
              
              return {
                  'resource': resource_arn,
                  'action': 'no action required',
                  'framework': framework
              }

  # IAM role for lifecycle enforcement
  LifecycleEnforcementRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
      Policies:
        - PolicyName: LifecycleEnforcementPolicy
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - dynamodb:Query
                  - dynamodb:GetItem
                  - dynamodb:PutItem
                  - dynamodb:UpdateItem
                  - s3:PutLifecycleConfiguration
                  - s3:GetLifecycleConfiguration
                  - s3:PutBucketTagging
                  - s3:GetBucketTagging
                  - rds:ModifyDBInstance
                  - rds:DescribeDBInstances
                Resource: '*'

  # EventBridge rule for scheduled enforcement
  LifecycleEnforcementSchedule:
    Type: AWS::Events::Rule
    Properties:
      Name: !Sub '${Environment}-lifecycle-enforcement-schedule'
      ScheduleExpression: 'rate(1 day)'
      State: ENABLED
      Targets:
        - Arn: !GetAtt LifecycleEnforcementFunction.Arn
          Id: LifecycleEnforcementTarget

  # Permission for EventBridge to invoke Lambda
  LifecycleEnforcementPermission:
    Type: AWS::Lambda::Permission
    Properties:
      FunctionName: !Ref LifecycleEnforcementFunction
      Action: lambda:InvokeFunction
      Principal: events.amazonaws.com
      SourceArn: !GetAtt LifecycleEnforcementSchedule.Arn

Outputs:
  TrackingTableName:
    Description: 'Name of the lifecycle tracking table'
    Value: !Ref LifecycleTrackingTable
    Export:
      Name: !Sub '${AWS::StackName}-TrackingTable'
  
  EnforcementFunctionArn:
    Description: 'ARN of the lifecycle enforcement function'
    Value: !GetAtt LifecycleEnforcementFunction.Arn
    Export:
      Name: !Sub '${AWS::StackName}-EnforcementFunction'
```

### Example 4: Cost-Optimized Lifecycle Management

```python
# cost_optimized_lifecycle.py
import boto3
from typing import Dict, List, Any
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class CostOptimizedLifecycleManager:
    """
    Cost-optimized data lifecycle management with intelligent tiering
    """
    
    def __init__(self, region: str = 'us-east-1'):
        self.region = region
        self.s3_client = boto3.client('s3', region_name=region)
        self.cloudwatch = boto3.client('cloudwatch', region_name=region)
        self.cost_explorer = boto3.client('ce', region_name='us-east-1')  # Cost Explorer is only in us-east-1
        
        # Storage class pricing (approximate, per GB per month)
        self.storage_pricing = {
            'STANDARD': 0.023,
            'STANDARD_IA': 0.0125,
            'ONEZONE_IA': 0.01,
            'GLACIER': 0.004,
            'DEEP_ARCHIVE': 0.00099,
            'INTELLIGENT_TIERING': 0.0125  # Base price, auto-optimizes
        }
    
    def analyze_access_patterns(self, bucket_name: str, days: int = 30) -> Dict[str, Any]:
        """Analyze S3 bucket access patterns for lifecycle optimization"""
        try:
            # Get access metrics from CloudWatch
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(days=days)
            
            # Get number of requests
            requests_response = self.cloudwatch.get_metric_statistics(
                Namespace='AWS/S3',
                MetricName='NumberOfObjects',
                Dimensions=[{'Name': 'BucketName', 'Value': bucket_name}],
                StartTime=start_time,
                EndTime=end_time,
                Period=86400,  # Daily
                Statistics=['Average']
            )
            
            # Get bucket size
            size_response = self.cloudwatch.get_metric_statistics(
                Namespace='AWS/S3',
                MetricName='BucketSizeBytes',
                Dimensions=[
                    {'Name': 'BucketName', 'Value': bucket_name},
                    {'Name': 'StorageType', 'Value': 'StandardStorage'}
                ],
                StartTime=start_time,
                EndTime=end_time,
                Period=86400,
                Statistics=['Average']
            )
            
            # Calculate access frequency
            total_requests = sum(dp['Average'] for dp in requests_response['Datapoints'])
            avg_daily_requests = total_requests / days if days > 0 else 0
            
            # Get current size
            current_size_bytes = 0
            if size_response['Datapoints']:
                current_size_bytes = size_response['Datapoints'][-1]['Average']
            
            current_size_gb = current_size_bytes / (1024**3)
            
            # Determine access pattern
            if avg_daily_requests > 100:
                access_pattern = 'frequent'
            elif avg_daily_requests > 10:
                access_pattern = 'moderate'
            elif avg_daily_requests > 1:
                access_pattern = 'infrequent'
            else:
                access_pattern = 'rare'
            
            return {
                'bucket': bucket_name,
                'size_gb': round(current_size_gb, 2),
                'avg_daily_requests': round(avg_daily_requests, 2),
                'access_pattern': access_pattern,
                'analysis_period_days': days
            }
            
        except Exception as e:
            logger.error(f"Error analyzing access patterns for {bucket_name}: {str(e)}")
            return {
                'bucket': bucket_name,
                'error': str(e)
            }
    
    def recommend_optimal_lifecycle_policy(self, bucket_name: str, classification: str) -> Dict[str, Any]:
        """Recommend optimal lifecycle policy based on access patterns and classification"""
        try:
            # Analyze access patterns
            access_analysis = self.analyze_access_patterns(bucket_name)
            
            if 'error' in access_analysis:
                return access_analysis
            
            access_pattern = access_analysis['access_pattern']
            size_gb = access_analysis['size_gb']
            
            # Base recommendations on access pattern and classification
            recommendations = {
                'bucket': bucket_name,
                'classification': classification,
                'access_pattern': access_pattern,
                'size_gb': size_gb,
                'recommended_policy': {},
                'cost_analysis': {},
                'rationale': []
            }
            
            # Define lifecycle policy based on access pattern and classification
            if access_pattern == 'frequent':
                if size_gb > 1000:  # Large bucket
                    policy = {
                        'intelligent_tiering': True,
                        'transitions': [
                            {'days': 90, 'storage_class': 'GLACIER'},
                            {'days': 365, 'storage_class': 'DEEP_ARCHIVE'}
                        ]
                    }
                    recommendations['rationale'].append('Large frequently accessed bucket - use Intelligent Tiering')
                else:
                    policy = {
                        'transitions': [
                            {'days': 30, 'storage_class': 'STANDARD_IA'},
                            {'days': 180, 'storage_class': 'GLACIER'}
                        ]
                    }
                    recommendations['rationale'].append('Frequently accessed bucket - delayed transitions')
            
            elif access_pattern == 'moderate':
                policy = {
                    'transitions': [
                        {'days': 30, 'storage_class': 'STANDARD_IA'},
                        {'days': 90, 'storage_class': 'GLACIER'},
                        {'days': 365, 'storage_class': 'DEEP_ARCHIVE'}
                    ]
                }
                recommendations['rationale'].append('Moderately accessed bucket - standard transitions')
            
            elif access_pattern == 'infrequent':
                policy = {
                    'transitions': [
                        {'days': 7, 'storage_class': 'STANDARD_IA'},
                        {'days': 30, 'storage_class': 'GLACIER'},
                        {'days': 90, 'storage_class': 'DEEP_ARCHIVE'}
                    ]
                }
                recommendations['rationale'].append('Infrequently accessed bucket - aggressive transitions')
            
            else:  # rare access
                policy = {
                    'transitions': [
                        {'days': 1, 'storage_class': 'GLACIER'},
                        {'days': 30, 'storage_class': 'DEEP_ARCHIVE'}
                    ]
                }
                recommendations['rationale'].append('Rarely accessed bucket - immediate archival')
            
            # Adjust for classification requirements
            if classification == 'restricted':
                # Restricted data may need longer retention in accessible tiers
                policy['transitions'] = [t for t in policy['transitions'] if t['days'] >= 30]
                recommendations['rationale'].append('Restricted classification - extended accessible retention')
            
            # Calculate cost savings
            cost_analysis = self._calculate_cost_savings(size_gb, policy)
            
            recommendations['recommended_policy'] = policy
            recommendations['cost_analysis'] = cost_analysis
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error recommending lifecycle policy for {bucket_name}: {str(e)}")
            return {
                'bucket': bucket_name,
                'error': str(e)
            }
    
    def _calculate_cost_savings(self, size_gb: float, policy: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate potential cost savings from lifecycle policy"""
        try:
            # Current cost (all in STANDARD)
            current_monthly_cost = size_gb * self.storage_pricing['STANDARD']
            
            # Projected cost with lifecycle policy
            projected_cost = 0
            remaining_data = size_gb
            
            if policy.get('intelligent_tiering'):
                # Assume 70% stays in Standard, 30% moves to IA automatically
                projected_cost += (remaining_data * 0.7 * self.storage_pricing['STANDARD'])
                projected_cost += (remaining_data * 0.3 * self.storage_pricing['STANDARD_IA'])
            else:
                # Calculate based on transitions
                current_tier_cost = self.storage_pricing['STANDARD']
                
                for transition in policy.get('transitions', []):
                    # Assume 50% of data transitions at each stage
                    transitioning_data = remaining_data * 0.5
                    staying_data = remaining_data * 0.5
                    
                    projected_cost += staying_data * current_tier_cost
                    remaining_data = transitioning_data
                    current_tier_cost = self.storage_pricing[transition['storage_class']]
                
                # Add cost for final tier
                projected_cost += remaining_data * current_tier_cost
            
            monthly_savings = current_monthly_cost - projected_cost
            annual_savings = monthly_savings * 12
            savings_percentage = (monthly_savings / current_monthly_cost * 100) if current_monthly_cost > 0 else 0
            
            return {
                'current_monthly_cost': round(current_monthly_cost, 2),
                'projected_monthly_cost': round(projected_cost, 2),
                'monthly_savings': round(monthly_savings, 2),
                'annual_savings': round(annual_savings, 2),
                'savings_percentage': round(savings_percentage, 1)
            }
            
        except Exception as e:
            logger.error(f"Error calculating cost savings: {str(e)}")
            return {'error': str(e)}
    
    def implement_cost_optimized_policy(self, bucket_name: str, policy: Dict[str, Any]) -> Dict[str, Any]:
        """Implement cost-optimized lifecycle policy"""
        try:
            rules = []
            
            if policy.get('intelligent_tiering'):
                # Enable Intelligent Tiering
                rules.append({
                    'ID': 'IntelligentTieringRule',
                    'Status': 'Enabled',
                    'Filter': {'Prefix': ''},
                    'Transitions': [
                        {'Days': 0, 'StorageClass': 'INTELLIGENT_TIERING'}
                    ] + policy.get('transitions', [])
                })
            else:
                # Standard lifecycle transitions
                rules.append({
                    'ID': 'CostOptimizedLifecycle',
                    'Status': 'Enabled',
                    'Filter': {'Prefix': ''},
                    'Transitions': policy.get('transitions', []),
                    'AbortIncompleteMultipartUpload': {'DaysAfterInitiation': 7}
                })
            
            # Apply lifecycle configuration
            self.s3_client.put_bucket_lifecycle_configuration(
                Bucket=bucket_name,
                LifecycleConfiguration={'Rules': rules}
            )
            
            return {
                'status': 'success',
                'bucket': bucket_name,
                'rules_applied': len(rules),
                'policy_type': 'intelligent_tiering' if policy.get('intelligent_tiering') else 'standard'
            }
            
        except Exception as e:
            logger.error(f"Error implementing lifecycle policy for {bucket_name}: {str(e)}")
            return {
                'status': 'error',
                'bucket': bucket_name,
                'error': str(e)
            }

# Example usage
if __name__ == "__main__":
    manager = CostOptimizedLifecycleManager()
    
    # Analyze access patterns
    analysis = manager.analyze_access_patterns('my-data-bucket')
    print(f"Access analysis: {analysis}")
    
    # Get recommendations
    recommendations = manager.recommend_optimal_lifecycle_policy('my-data-bucket', 'confidential')
    print(f"Recommendations: {recommendations}")
    
    # Implement policy
    if 'recommended_policy' in recommendations:
        implementation = manager.implement_cost_optimized_policy(
            'my-data-bucket', 
            recommendations['recommended_policy']
        )
        print(f"Implementation result: {implementation}")
```

## Relevant AWS Services

### Core Lifecycle Services
- **Amazon S3**: Object lifecycle management with storage class transitions
- **AWS Backup**: Centralized backup across AWS services with lifecycle policies
- **Amazon EBS**: Snapshot lifecycle management
- **Amazon RDS**: Automated backups and snapshot retention

### Automation Services
- **AWS Lambda**: Serverless functions for lifecycle automation
- **Amazon EventBridge**: Event-driven lifecycle triggers
- **AWS Step Functions**: Complex lifecycle workflow orchestration
- **AWS Systems Manager**: Automated lifecycle maintenance

### Monitoring and Analytics
- **Amazon CloudWatch**: Metrics and monitoring for lifecycle decisions
- **AWS Cost Explorer**: Cost analysis and optimization
- **AWS CloudTrail**: Audit trails for lifecycle actions
- **Amazon QuickSight**: Lifecycle reporting and dashboards

### Compliance Services
- **AWS Config**: Configuration compliance monitoring
- **AWS Security Hub**: Centralized compliance findings
- **Amazon Macie**: Data classification for lifecycle decisions
- **AWS Artifact**: Compliance documentation and reports

## Benefits of Scalable Data Lifecycle Management

### Cost Benefits
- **Storage Optimization**: Automatic transitions to lower-cost storage classes
- **Resource Efficiency**: Right-sizing based on actual usage patterns
- **Predictable Costs**: Automated cost management and optimization
- **Waste Reduction**: Elimination of unnecessary data retention

### Operational Benefits
- **Automation**: Reduced manual effort for lifecycle management
- **Scalability**: Handles growing data volumes automatically
- **Consistency**: Uniform lifecycle policies across all data assets
- **Efficiency**: Streamlined data management processes

### Compliance Benefits
- **Regulatory Adherence**: Automated compliance with retention requirements
- **Audit Readiness**: Complete lifecycle audit trails
- **Risk Management**: Controlled data disposal and retention
- **Policy Enforcement**: Consistent application of lifecycle policies

### Security Benefits
- **Data Protection**: Appropriate security controls throughout lifecycle
- **Access Control**: Lifecycle-aware access management
- **Secure Disposal**: Certified data destruction methods
- **Compliance Monitoring**: Continuous lifecycle compliance validation

## Related Resources

- [AWS Well-Architected Framework - Data Lifecycle Management](https://docs.aws.amazon.com/wellarchitected/latest/framework/sec_data_classification_lifecycle_management.html)
- [Amazon S3 Lifecycle Management](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html)
- [AWS Backup User Guide](https://docs.aws.amazon.com/aws-backup/latest/devguide/whatisbackup.html)
- [AWS Cost Optimization Best Practices](https://docs.aws.amazon.com/whitepapers/latest/cost-optimization-pillar/welcome.html)
- [AWS Compliance Center](https://aws.amazon.com/compliance/)
- [AWS Security Blog - Data Lifecycle Management](https://aws.amazon.com/blogs/security/tag/data-lifecycle-management/)
```
```
