---
title: "SEC08-BP04: Enforce access control"
layout: default
parent: "SEC08 - How do you protect your data at rest?"
grand_parent: Security
nav_order: 4
---

# SEC08-BP04: Enforce access control

## Overview

Enforcing access control for data at rest ensures that only authorized users and systems can access stored data, regardless of the underlying storage mechanism. This best practice focuses on implementing comprehensive access control mechanisms that work in conjunction with encryption to provide defense-in-depth protection for sensitive data.

Access control should be implemented at multiple layers including identity-based controls, resource-based policies, network-level restrictions, and application-level authorization. The controls should be based on the principle of least privilege and support both human and programmatic access patterns.

## Implementation Guidance

### 1. Implement Identity-Based Access Control

Deploy comprehensive identity and access management:

- **AWS IAM Policies**: Fine-grained permissions for users, groups, and roles
- **Attribute-Based Access Control (ABAC)**: Dynamic access control based on attributes
- **Multi-Factor Authentication**: Additional authentication factors for sensitive data access
- **Temporary Credentials**: Time-limited access using AWS STS

### 2. Configure Resource-Based Access Control

Implement resource-specific access policies:

- **S3 Bucket Policies**: Control access to objects and buckets
- **KMS Key Policies**: Control encryption key usage and management
- **RDS Resource Policies**: Database-level access control
- **Cross-Account Access**: Secure sharing across AWS accounts

### 3. Deploy Network-Level Access Control

Establish network-based access restrictions:

- **VPC Endpoints**: Private connectivity to AWS services
- **Security Groups**: Instance-level firewall rules
- **Network ACLs**: Subnet-level network filtering
- **AWS PrivateLink**: Private connectivity for service access

### 4. Implement Application-Level Authorization

Deploy application-specific access controls:

- **Database Permissions**: Row-level and column-level security
- **Application Roles**: Role-based access within applications
- **API Gateway Authorization**: Control access to data APIs
- **Lambda Authorizers**: Custom authorization logic

### 5. Enable Continuous Access Monitoring

Implement comprehensive access monitoring:

- **CloudTrail Logging**: Complete audit trail of access attempts
- **VPC Flow Logs**: Network-level access monitoring
- **Application Logs**: Application-specific access logging
- **Real-Time Alerting**: Immediate notification of unauthorized access

### 6. Establish Access Control Governance

Deploy governance mechanisms for access control:

- **Access Reviews**: Regular review of access permissions
- **Automated Provisioning**: Consistent access provisioning processes
- **Access Certification**: Periodic validation of access requirements
- **Compliance Reporting**: Regular access control compliance reports

## Implementation Examples

### Example 1: Comprehensive Access Control Management System

```python
# access_control_manager.py
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
class AccessPolicy:
    policy_name: str
    resource_type: str
    data_classification: str
    allowed_principals: List[str]
    allowed_actions: List[str]
    conditions: Dict[str, Any]
    policy_document: Dict[str, Any]

@dataclass
class AccessRequest:
    request_id: str
    principal: str
    resource_arn: str
    action: str
    timestamp: str
    source_ip: str
    user_agent: str
    approved: bool
    justification: str

class AccessControlManager:
    """
    Comprehensive access control management system for data at rest
    """
    
    def __init__(self, region: str = 'us-east-1'):
        self.region = region
        self.iam_client = boto3.client('iam', region_name=region)
        self.s3_client = boto3.client('s3', region_name=region)
        self.kms_client = boto3.client('kms', region_name=region)
        self.rds_client = boto3.client('rds', region_name=region)
        self.ec2_client = boto3.client('ec2', region_name=region)
        self.sts_client = boto3.client('sts', region_name=region)
        self.cloudtrail_client = boto3.client('cloudtrail', region_name=region)
        self.dynamodb = boto3.resource('dynamodb', region_name=region)
        
        # Access control tracking tables
        self.access_policies_table = self.dynamodb.Table('access-control-policies')
        self.access_requests_table = self.dynamodb.Table('access-requests')
        self.access_reviews_table = self.dynamodb.Table('access-reviews')
        
        # Classification-based access policies
        self.classification_policies = self._define_classification_access_policies()
    
    def _define_classification_access_policies(self) -> Dict[str, AccessPolicy]:
        """
        Define access policies based on data classification levels
        """
        account_id = self._get_account_id()
        
        return {
            'public': AccessPolicy(
                policy_name='PublicDataAccess',
                resource_type='s3',
                data_classification='public',
                allowed_principals=['*'],
                allowed_actions=['s3:GetObject'],
                conditions={},
                policy_document={
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Principal": "*",
                            "Action": "s3:GetObject",
                            "Resource": "arn:aws:s3:::*/*",
                            "Condition": {
                                "StringEquals": {
                                    "s3:ExistingObjectTag/DataClassification": "public"
                                }
                            }
                        }
                    ]
                }
            ),
            
            'internal': AccessPolicy(
                policy_name='InternalDataAccess',
                resource_type='s3',
                data_classification='internal',
                allowed_principals=[f'arn:aws:iam::{account_id}:root'],
                allowed_actions=['s3:GetObject', 's3:PutObject'],
                conditions={
                    "StringEquals": {
                        "aws:PrincipalOrgID": "o-example123456"
                    }
                },
                policy_document={
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Principal": {"AWS": f"arn:aws:iam::{account_id}:root"},
                            "Action": ["s3:GetObject", "s3:PutObject"],
                            "Resource": "arn:aws:s3:::*/*",
                            "Condition": {
                                "StringEquals": {
                                    "s3:ExistingObjectTag/DataClassification": "internal",
                                    "aws:PrincipalOrgID": "o-example123456"
                                }
                            }
                        }
                    ]
                }
            ),
            
            'confidential': AccessPolicy(
                policy_name='ConfidentialDataAccess',
                resource_type='s3',
                data_classification='confidential',
                allowed_principals=[f'arn:aws:iam::{account_id}:role/ConfidentialDataRole'],
                allowed_actions=['s3:GetObject'],
                conditions={
                    "Bool": {
                        "aws:MultiFactorAuthPresent": "true"
                    },
                    "DateGreaterThan": {
                        "aws:MultiFactorAuthAge": "3600"
                    }
                },
                policy_document={
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Principal": {"AWS": f"arn:aws:iam::{account_id}:role/ConfidentialDataRole"},
                            "Action": "s3:GetObject",
                            "Resource": "arn:aws:s3:::*/*",
                            "Condition": {
                                "StringEquals": {
                                    "s3:ExistingObjectTag/DataClassification": "confidential"
                                },
                                "Bool": {
                                    "aws:MultiFactorAuthPresent": "true"
                                },
                                "NumericLessThan": {
                                    "aws:MultiFactorAuthAge": "3600"
                                }
                            }
                        }
                    ]
                }
            ),
            
            'restricted': AccessPolicy(
                policy_name='RestrictedDataAccess',
                resource_type='s3',
                data_classification='restricted',
                allowed_principals=[f'arn:aws:iam::{account_id}:role/RestrictedDataRole'],
                allowed_actions=['s3:GetObject'],
                conditions={
                    "Bool": {
                        "aws:MultiFactorAuthPresent": "true"
                    },
                    "DateGreaterThan": {
                        "aws:MultiFactorAuthAge": "1800"
                    },
                    "IpAddress": {
                        "aws:SourceIp": ["10.0.0.0/8", "172.16.0.0/12"]
                    }
                },
                policy_document={
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Principal": {"AWS": f"arn:aws:iam::{account_id}:role/RestrictedDataRole"},
                            "Action": "s3:GetObject",
                            "Resource": "arn:aws:s3:::*/*",
                            "Condition": {
                                "StringEquals": {
                                    "s3:ExistingObjectTag/DataClassification": "restricted"
                                },
                                "Bool": {
                                    "aws:MultiFactorAuthPresent": "true"
                                },
                                "NumericLessThan": {
                                    "aws:MultiFactorAuthAge": "1800"
                                },
                                "IpAddress": {
                                    "aws:SourceIp": ["10.0.0.0/8", "172.16.0.0/12"]
                                }
                            }
                        }
                    ]
                }
            )
        }
    
    def apply_access_control_policy(self, resource_arn: str, data_classification: str) -> Dict[str, Any]:
        """
        Apply access control policy based on resource type and data classification
        """
        try:
            # Determine resource type from ARN
            service = resource_arn.split(':')[2]
            
            if service == 's3':
                return self._apply_s3_access_policy(resource_arn, data_classification)
            elif service == 'kms':
                return self._apply_kms_access_policy(resource_arn, data_classification)
            elif service == 'rds':
                return self._apply_rds_access_policy(resource_arn, data_classification)
            else:
                return {
                    'status': 'unsupported',
                    'resource_arn': resource_arn,
                    'message': f'Access control not supported for service: {service}'
                }
                
        except Exception as e:
            logger.error(f"Error applying access control policy: {str(e)}")
            return {
                'status': 'error',
                'resource_arn': resource_arn,
                'message': str(e)
            }
    
    def _apply_s3_access_policy(self, bucket_arn: str, data_classification: str) -> Dict[str, Any]:
        """
        Apply S3 bucket access policy based on data classification
        """
        try:
            bucket_name = bucket_arn.split(':')[-1]
            
            if data_classification not in self.classification_policies:
                return {
                    'status': 'error',
                    'message': f'Unknown data classification: {data_classification}'
                }
            
            policy = self.classification_policies[data_classification]
            
            # Apply bucket policy
            self.s3_client.put_bucket_policy(
                Bucket=bucket_name,
                Policy=json.dumps(policy.policy_document)
            )
            
            # Block public access for non-public data
            if data_classification != 'public':
                self.s3_client.put_public_access_block(
                    Bucket=bucket_name,
                    PublicAccessBlockConfiguration={
                        'BlockPublicAcls': True,
                        'IgnorePublicAcls': True,
                        'BlockPublicPolicy': True,
                        'RestrictPublicBuckets': True
                    }
                )
            
            # Track policy application
            self._track_policy_application(bucket_arn, policy)
            
            logger.info(f"Applied {data_classification} access policy to {bucket_name}")
            
            return {
                'status': 'success',
                'resource_arn': bucket_arn,
                'policy_applied': policy.policy_name,
                'data_classification': data_classification
            }
            
        except Exception as e:
            logger.error(f"Error applying S3 access policy: {str(e)}")
            return {
                'status': 'error',
                'resource_arn': bucket_arn,
                'message': str(e)
            }
    
    def _apply_kms_access_policy(self, key_arn: str, data_classification: str) -> Dict[str, Any]:
        """
        Apply KMS key access policy based on data classification
        """
        try:
            key_id = key_arn.split('/')[-1]
            account_id = self._get_account_id()
            
            # Define KMS policy based on classification
            if data_classification == 'restricted':
                key_policy = {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Sid": "Enable IAM User Permissions",
                            "Effect": "Allow",
                            "Principal": {"AWS": f"arn:aws:iam::{account_id}:root"},
                            "Action": "kms:*",
                            "Resource": "*"
                        },
                        {
                            "Sid": "Allow restricted data access",
                            "Effect": "Allow",
                            "Principal": {"AWS": f"arn:aws:iam::{account_id}:role/RestrictedDataRole"},
                            "Action": [
                                "kms:Encrypt",
                                "kms:Decrypt",
                                "kms:ReEncrypt*",
                                "kms:GenerateDataKey*",
                                "kms:DescribeKey"
                            ],
                            "Resource": "*",
                            "Condition": {
                                "Bool": {
                                    "aws:MultiFactorAuthPresent": "true"
                                },
                                "NumericLessThan": {
                                    "aws:MultiFactorAuthAge": "1800"
                                }
                            }
                        }
                    ]
                }
            else:
                # Standard policy for other classifications
                key_policy = {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Sid": "Enable IAM User Permissions",
                            "Effect": "Allow",
                            "Principal": {"AWS": f"arn:aws:iam::{account_id}:root"},
                            "Action": "kms:*",
                            "Resource": "*"
                        },
                        {
                            "Sid": "Allow data access",
                            "Effect": "Allow",
                            "Principal": {"AWS": f"arn:aws:iam::{account_id}:role/{data_classification.title()}DataRole"},
                            "Action": [
                                "kms:Encrypt",
                                "kms:Decrypt",
                                "kms:ReEncrypt*",
                                "kms:GenerateDataKey*",
                                "kms:DescribeKey"
                            ],
                            "Resource": "*"
                        }
                    ]
                }
            
            # Apply KMS key policy
            self.kms_client.put_key_policy(
                KeyId=key_id,
                PolicyName='default',
                Policy=json.dumps(key_policy)
            )
            
            logger.info(f"Applied {data_classification} KMS policy to {key_id}")
            
            return {
                'status': 'success',
                'resource_arn': key_arn,
                'policy_applied': f'{data_classification}_kms_policy',
                'data_classification': data_classification
            }
            
        except Exception as e:
            logger.error(f"Error applying KMS access policy: {str(e)}")
            return {
                'status': 'error',
                'resource_arn': key_arn,
                'message': str(e)
            }
    
    def create_temporary_access(self, 
                              principal: str, 
                              resource_arn: str, 
                              duration_hours: int = 1,
                              justification: str = "") -> Dict[str, Any]:
        """
        Create temporary access credentials for data access
        """
        try:
            # Create temporary role policy
            temp_policy_name = f"TempAccess-{int(datetime.utcnow().timestamp())}"
            
            # Determine required permissions based on resource type
            service = resource_arn.split(':')[2]
            
            if service == 's3':
                actions = ["s3:GetObject", "s3:ListBucket"]
                resource_patterns = [resource_arn, f"{resource_arn}/*"]
            elif service == 'rds':
                actions = ["rds:DescribeDBInstances", "rds-db:connect"]
                resource_patterns = [resource_arn]
            else:
                return {
                    'status': 'error',
                    'message': f'Temporary access not supported for service: {service}'
                }
            
            # Create temporary policy
            temp_policy_document = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Action": actions,
                        "Resource": resource_patterns,
                        "Condition": {
                            "DateLessThan": {
                                "aws:CurrentTime": (datetime.utcnow() + timedelta(hours=duration_hours)).isoformat()
                            }
                        }
                    }
                ]
            }
            
            # Create IAM policy
            policy_response = self.iam_client.create_policy(
                PolicyName=temp_policy_name,
                PolicyDocument=json.dumps(temp_policy_document),
                Description=f'Temporary access policy for {resource_arn}'
            )
            
            # Attach policy to principal (assuming it's a role)
            if principal.startswith('arn:aws:iam::'):
                role_name = principal.split('/')[-1]
                self.iam_client.attach_role_policy(
                    RoleName=role_name,
                    PolicyArn=policy_response['Policy']['Arn']
                )
            
            # Track access request
            access_request = AccessRequest(
                request_id=temp_policy_name,
                principal=principal,
                resource_arn=resource_arn,
                action='temporary_access',
                timestamp=datetime.utcnow().isoformat(),
                source_ip='unknown',
                user_agent='api',
                approved=True,
                justification=justification
            )
            
            self._track_access_request(access_request)
            
            # Schedule policy cleanup
            self._schedule_policy_cleanup(policy_response['Policy']['Arn'], duration_hours)
            
            logger.info(f"Created temporary access for {principal} to {resource_arn}")
            
            return {
                'status': 'success',
                'policy_arn': policy_response['Policy']['Arn'],
                'expires_at': (datetime.utcnow() + timedelta(hours=duration_hours)).isoformat(),
                'principal': principal,
                'resource_arn': resource_arn
            }
            
        except Exception as e:
            logger.error(f"Error creating temporary access: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def audit_access_patterns(self, resource_arn: str, days: int = 30) -> Dict[str, Any]:
        """
        Audit access patterns for a specific resource
        """
        try:
            # Get CloudTrail events for the resource
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(days=days)
            
            events = self.cloudtrail_client.lookup_events(
                LookupAttributes=[
                    {
                        'AttributeKey': 'ResourceName',
                        'AttributeValue': resource_arn
                    }
                ],
                StartTime=start_time,
                EndTime=end_time
            )
            
            # Analyze access patterns
            access_analysis = {
                'resource_arn': resource_arn,
                'analysis_period_days': days,
                'total_access_events': len(events['Events']),
                'unique_users': set(),
                'access_by_action': {},
                'access_by_hour': {},
                'access_by_source_ip': {},
                'suspicious_activities': [],
                'compliance_issues': []
            }
            
            for event in events['Events']:
                event_name = event['EventName']
                username = event.get('Username', 'Unknown')
                source_ip = event.get('SourceIPAddress', 'Unknown')
                event_time = event['EventTime']
                
                # Track unique users
                access_analysis['unique_users'].add(username)
                
                # Count access by action
                access_analysis['access_by_action'][event_name] = \
                    access_analysis['access_by_action'].get(event_name, 0) + 1
                
                # Count access by hour
                hour_key = event_time.strftime('%H:00')
                access_analysis['access_by_hour'][hour_key] = \
                    access_analysis['access_by_hour'].get(hour_key, 0) + 1
                
                # Count access by source IP
                access_analysis['access_by_source_ip'][source_ip] = \
                    access_analysis['access_by_source_ip'].get(source_ip, 0) + 1
                
                # Check for suspicious activities
                if self._is_suspicious_activity(event):
                    access_analysis['suspicious_activities'].append({
                        'event_name': event_name,
                        'username': username,
                        'source_ip': source_ip,
                        'timestamp': event_time.isoformat(),
                        'reason': 'Unusual access pattern detected'
                    })
            
            # Convert set to list for JSON serialization
            access_analysis['unique_users'] = list(access_analysis['unique_users'])
            
            # Check compliance
            compliance_issues = self._check_access_compliance(resource_arn, access_analysis)
            access_analysis['compliance_issues'] = compliance_issues
            
            return access_analysis
            
        except Exception as e:
            logger.error(f"Error auditing access patterns: {str(e)}")
            return {
                'status': 'error',
                'resource_arn': resource_arn,
                'message': str(e)
            }
    
    def _is_suspicious_activity(self, event: Dict[str, Any]) -> bool:
        """
        Determine if an access event is suspicious
        """
        # Check for access outside business hours
        event_time = event['EventTime']
        if event_time.hour < 6 or event_time.hour > 22:
            return True
        
        # Check for unusual source IPs
        source_ip = event.get('SourceIPAddress', '')
        if not (source_ip.startswith('10.') or source_ip.startswith('172.') or source_ip.startswith('192.168.')):
            return True
        
        # Check for failed access attempts
        if event.get('ErrorCode') or event.get('ErrorMessage'):
            return True
        
        return False
    
    def _check_access_compliance(self, resource_arn: str, access_analysis: Dict[str, Any]) -> List[str]:
        """
        Check access compliance against policies
        """
        issues = []
        
        # Check for excessive access
        if access_analysis['total_access_events'] > 1000:
            issues.append('Excessive access events detected')
        
        # Check for too many unique users
        if len(access_analysis['unique_users']) > 50:
            issues.append('Too many unique users accessing resource')
        
        # Check for suspicious activities
        if len(access_analysis['suspicious_activities']) > 0:
            issues.append(f"{len(access_analysis['suspicious_activities'])} suspicious activities detected")
        
        return issues
    
    def _track_policy_application(self, resource_arn: str, policy: AccessPolicy):
        """
        Track policy application in DynamoDB
        """
        try:
            self.access_policies_table.put_item(
                Item={
                    'resource_arn': resource_arn,
                    'policy_name': policy.policy_name,
                    'data_classification': policy.data_classification,
                    'applied_timestamp': datetime.utcnow().isoformat(),
                    'allowed_principals': policy.allowed_principals,
                    'allowed_actions': policy.allowed_actions,
                    'ttl': int((datetime.utcnow() + timedelta(days=365)).timestamp())
                }
            )
        except Exception as e:
            logger.error(f"Error tracking policy application: {str(e)}")
    
    def _track_access_request(self, request: AccessRequest):
        """
        Track access request in DynamoDB
        """
        try:
            self.access_requests_table.put_item(Item=asdict(request))
        except Exception as e:
            logger.error(f"Error tracking access request: {str(e)}")
    
    def _schedule_policy_cleanup(self, policy_arn: str, hours: int):
        """
        Schedule cleanup of temporary policy (simplified implementation)
        """
        # In a real implementation, this would use EventBridge or Lambda scheduling
        logger.info(f"Scheduled cleanup of policy {policy_arn} in {hours} hours")
    
    def _get_account_id(self) -> str:
        """Get AWS account ID"""
        return self.sts_client.get_caller_identity()['Account']

# Example usage
if __name__ == "__main__":
    # Initialize access control manager
    access_manager = AccessControlManager()
    
    # Apply access control policy to S3 bucket
    s3_result = access_manager.apply_access_control_policy(
        'arn:aws:s3:::confidential-data-bucket',
        'confidential'
    )
    print(f"S3 access control result: {s3_result}")
    
    # Create temporary access
    temp_access_result = access_manager.create_temporary_access(
        'arn:aws:iam::123456789012:role/DataAnalyst',
        'arn:aws:s3:::confidential-data-bucket',
        duration_hours=2,
        justification='Emergency data analysis required'
    )
    print(f"Temporary access result: {temp_access_result}")
    
    # Audit access patterns
    audit_result = access_manager.audit_access_patterns(
        'arn:aws:s3:::confidential-data-bucket',
        days=7
    )
    print(f"Access audit result: {json.dumps(audit_result, indent=2, default=str)}")
```

### Example 2: Attribute-Based Access Control (ABAC) Implementation

```python
# abac_access_control.py
import boto3
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

@dataclass
class AccessAttribute:
    name: str
    value: str
    attribute_type: str  # user, resource, environment, action

@dataclass
class AccessRule:
    rule_id: str
    name: str
    description: str
    subject_attributes: List[AccessAttribute]
    resource_attributes: List[AccessAttribute]
    environment_attributes: List[AccessAttribute]
    action_attributes: List[AccessAttribute]
    effect: str  # Allow or Deny
    priority: int

class ABACAccessController:
    """
    Attribute-Based Access Control implementation for fine-grained data access
    """
    
    def __init__(self, region: str = 'us-east-1'):
        self.region = region
        self.iam_client = boto3.client('iam', region_name=region)
        self.s3_client = boto3.client('s3', region_name=region)
        self.sts_client = boto3.client('sts', region_name=region)
        self.dynamodb = boto3.resource('dynamodb', region_name=region)
        
        # ABAC rules storage
        self.abac_rules_table = self.dynamodb.Table('abac-access-rules')
        self.access_decisions_table = self.dynamodb.Table('abac-access-decisions')
        
        # Define ABAC rules
        self.access_rules = self._define_abac_rules()
    
    def _define_abac_rules(self) -> List[AccessRule]:
        """
        Define ABAC rules for data access control
        """
        return [
            # Rule 1: Department-based access to departmental data
            AccessRule(
                rule_id='dept-data-access',
                name='Department Data Access',
                description='Allow users to access data from their own department',
                subject_attributes=[
                    AccessAttribute('department', '${resource.department}', 'user')
                ],
                resource_attributes=[
                    AccessAttribute('department', '*', 'resource')
                ],
                environment_attributes=[
                    AccessAttribute('time', '09:00-17:00', 'environment'),
                    AccessAttribute('network', 'corporate', 'environment')
                ],
                action_attributes=[
                    AccessAttribute('action', 's3:GetObject', 'action')
                ],
                effect='Allow',
                priority=100
            ),
            
            # Rule 2: Manager access to subordinate data
            AccessRule(
                rule_id='manager-subordinate-access',
                name='Manager Subordinate Access',
                description='Allow managers to access data from their subordinates',
                subject_attributes=[
                    AccessAttribute('role', 'manager', 'user'),
                    AccessAttribute('department', '${resource.department}', 'user')
                ],
                resource_attributes=[
                    AccessAttribute('owner_role', 'employee', 'resource'),
                    AccessAttribute('department', '*', 'resource')
                ],
                environment_attributes=[
                    AccessAttribute('mfa_authenticated', 'true', 'environment')
                ],
                action_attributes=[
                    AccessAttribute('action', 's3:GetObject', 'action')
                ],
                effect='Allow',
                priority=200
            ),
            
            # Rule 3: Restricted data access for authorized personnel only
            AccessRule(
                rule_id='restricted-data-access',
                name='Restricted Data Access',
                description='Allow only authorized personnel to access restricted data',
                subject_attributes=[
                    AccessAttribute('clearance_level', 'restricted', 'user')
                ],
                resource_attributes=[
                    AccessAttribute('classification', 'restricted', 'resource')
                ],
                environment_attributes=[
                    AccessAttribute('mfa_authenticated', 'true', 'environment'),
                    AccessAttribute('network', 'secure', 'environment'),
                    AccessAttribute('time', '08:00-18:00', 'environment')
                ],
                action_attributes=[
                    AccessAttribute('action', 's3:GetObject', 'action')
                ],
                effect='Allow',
                priority=300
            ),
            
            # Rule 4: Deny access outside business hours for sensitive data
            AccessRule(
                rule_id='business-hours-only',
                name='Business Hours Only',
                description='Deny access to sensitive data outside business hours',
                subject_attributes=[],
                resource_attributes=[
                    AccessAttribute('classification', 'confidential|restricted', 'resource')
                ],
                environment_attributes=[
                    AccessAttribute('time', '18:01-07:59', 'environment')
                ],
                action_attributes=[],
                effect='Deny',
                priority=500
            ),
            
            # Rule 5: Emergency access override
            AccessRule(
                rule_id='emergency-access',
                name='Emergency Access Override',
                description='Allow emergency access with proper justification',
                subject_attributes=[
                    AccessAttribute('role', 'emergency_responder', 'user')
                ],
                resource_attributes=[],
                environment_attributes=[
                    AccessAttribute('emergency_declared', 'true', 'environment'),
                    AccessAttribute('justification_provided', 'true', 'environment')
                ],
                action_attributes=[],
                effect='Allow',
                priority=1000
            )
        ]
    
    def evaluate_access_request(self, 
                              subject_attributes: Dict[str, str],
                              resource_attributes: Dict[str, str],
                              environment_attributes: Dict[str, str],
                              action: str) -> Dict[str, Any]:
        """
        Evaluate access request using ABAC rules
        """
        try:
            # Create access context
            access_context = {
                'subject': subject_attributes,
                'resource': resource_attributes,
                'environment': environment_attributes,
                'action': action,
                'timestamp': datetime.utcnow().isoformat()
            }
            
            # Evaluate rules in priority order
            applicable_rules = []
            for rule in sorted(self.access_rules, key=lambda x: x.priority, reverse=True):
                if self._rule_matches(rule, access_context):
                    applicable_rules.append(rule)
            
            # Determine final decision
            decision = self._make_access_decision(applicable_rules)
            
            # Create decision record
            decision_record = {
                'decision_id': f"decision-{int(datetime.utcnow().timestamp())}",
                'access_context': access_context,
                'applicable_rules': [rule.rule_id for rule in applicable_rules],
                'decision': decision['effect'],
                'reason': decision['reason'],
                'timestamp': datetime.utcnow().isoformat()
            }
            
            # Store decision
            self._store_access_decision(decision_record)
            
            logger.info(f"Access decision: {decision['effect']} - {decision['reason']}")
            
            return {
                'decision': decision['effect'],
                'reason': decision['reason'],
                'applicable_rules': [rule.rule_id for rule in applicable_rules],
                'decision_id': decision_record['decision_id']
            }
            
        except Exception as e:
            logger.error(f"Error evaluating access request: {str(e)}")
            return {
                'decision': 'Deny',
                'reason': f'Error in access evaluation: {str(e)}',
                'applicable_rules': [],
                'decision_id': None
            }
    
    def _rule_matches(self, rule: AccessRule, context: Dict[str, Any]) -> bool:
        """
        Check if a rule matches the access context
        """
        try:
            # Check subject attributes
            if not self._attributes_match(rule.subject_attributes, context['subject']):
                return False
            
            # Check resource attributes
            if not self._attributes_match(rule.resource_attributes, context['resource']):
                return False
            
            # Check environment attributes
            if not self._attributes_match(rule.environment_attributes, context['environment']):
                return False
            
            # Check action attributes
            action_attrs = {'action': context['action']}
            if not self._attributes_match(rule.action_attributes, action_attrs):
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error matching rule {rule.rule_id}: {str(e)}")
            return False
    
    def _attributes_match(self, rule_attributes: List[AccessAttribute], context_attributes: Dict[str, str]) -> bool:
        """
        Check if rule attributes match context attributes
        """
        for rule_attr in rule_attributes:
            context_value = context_attributes.get(rule_attr.name, '')
            
            # Handle wildcard matching
            if rule_attr.value == '*':
                continue
            
            # Handle variable substitution (simplified)
            if rule_attr.value.startswith('${'):
                # In a real implementation, this would resolve variables
                continue
            
            # Handle regex patterns
            if '|' in rule_attr.value:
                # Simple OR matching
                allowed_values = rule_attr.value.split('|')
                if context_value not in allowed_values:
                    return False
            elif rule_attr.value != context_value:
                return False
        
        return True
    
    def _make_access_decision(self, applicable_rules: List[AccessRule]) -> Dict[str, str]:
        """
        Make final access decision based on applicable rules
        """
        if not applicable_rules:
            return {
                'effect': 'Deny',
                'reason': 'No applicable rules found'
            }
        
        # Check for explicit deny rules first
        for rule in applicable_rules:
            if rule.effect == 'Deny':
                return {
                    'effect': 'Deny',
                    'reason': f'Denied by rule: {rule.name}'
                }
        
        # Check for allow rules
        for rule in applicable_rules:
            if rule.effect == 'Allow':
                return {
                    'effect': 'Allow',
                    'reason': f'Allowed by rule: {rule.name}'
                }
        
        # Default deny
        return {
            'effect': 'Deny',
            'reason': 'Default deny - no allow rules matched'
        }
    
    def create_dynamic_policy(self, 
                            principal_arn: str,
                            resource_arn: str,
                            subject_attributes: Dict[str, str],
                            resource_attributes: Dict[str, str]) -> Dict[str, Any]:
        """
        Create dynamic IAM policy based on ABAC evaluation
        """
        try:
            # Evaluate access for common actions
            actions_to_test = ['s3:GetObject', 's3:PutObject', 's3:DeleteObject', 's3:ListBucket']
            allowed_actions = []
            
            for action in actions_to_test:
                decision = self.evaluate_access_request(
                    subject_attributes=subject_attributes,
                    resource_attributes=resource_attributes,
                    environment_attributes={
                        'time': datetime.utcnow().strftime('%H:%M'),
                        'network': 'corporate',
                        'mfa_authenticated': 'true'
                    },
                    action=action
                )
                
                if decision['decision'] == 'Allow':
                    allowed_actions.append(action)
            
            if not allowed_actions:
                return {
                    'status': 'no_access',
                    'message': 'No actions allowed based on ABAC evaluation'
                }
            
            # Create dynamic policy
            policy_name = f"ABAC-Policy-{int(datetime.utcnow().timestamp())}"
            
            # Build conditions based on attributes
            conditions = {}
            
            # Add time-based conditions
            current_hour = datetime.utcnow().hour
            if 'time_restriction' in resource_attributes:
                conditions['DateGreaterThan'] = {
                    'aws:CurrentTime': f'{current_hour:02d}:00:00Z'
                }
                conditions['DateLessThan'] = {
                    'aws:CurrentTime': f'{(current_hour + 8) % 24:02d}:00:00Z'
                }
            
            # Add MFA conditions for sensitive data
            if resource_attributes.get('classification') in ['confidential', 'restricted']:
                conditions['Bool'] = {
                    'aws:MultiFactorAuthPresent': 'true'
                }
            
            # Create policy document
            policy_document = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Action": allowed_actions,
                        "Resource": [resource_arn, f"{resource_arn}/*"],
                        "Condition": conditions if conditions else {}
                    }
                ]
            }
            
            # Create IAM policy
            policy_response = self.iam_client.create_policy(
                PolicyName=policy_name,
                PolicyDocument=json.dumps(policy_document),
                Description=f'ABAC-generated policy for {principal_arn}'
            )
            
            logger.info(f"Created dynamic ABAC policy: {policy_name}")
            
            return {
                'status': 'success',
                'policy_arn': policy_response['Policy']['Arn'],
                'policy_name': policy_name,
                'allowed_actions': allowed_actions,
                'conditions_applied': list(conditions.keys())
            }
            
        except Exception as e:
            logger.error(f"Error creating dynamic policy: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _store_access_decision(self, decision_record: Dict[str, Any]):
        """
        Store access decision in DynamoDB
        """
        try:
            self.access_decisions_table.put_item(
                Item={
                    **decision_record,
                    'ttl': int((datetime.utcnow() + timedelta(days=90)).timestamp())
                }
            )
        except Exception as e:
            logger.error(f"Error storing access decision: {str(e)}")
    
    def generate_abac_report(self, days: int = 30) -> Dict[str, Any]:
        """
        Generate ABAC access control report
        """
        try:
            # Query recent access decisions
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(days=days)
            
            response = self.access_decisions_table.scan(
                FilterExpression='#ts BETWEEN :start AND :end',
                ExpressionAttributeNames={'#ts': 'timestamp'},
                ExpressionAttributeValues={
                    ':start': start_time.isoformat(),
                    ':end': end_time.isoformat()
                }
            )
            
            decisions = response['Items']
            
            # Analyze decisions
            report = {
                'report_period_days': days,
                'total_decisions': len(decisions),
                'decisions_by_effect': {'Allow': 0, 'Deny': 0},
                'most_used_rules': {},
                'access_patterns': {},
                'compliance_summary': {
                    'policy_violations': 0,
                    'emergency_access_used': 0,
                    'after_hours_attempts': 0
                }
            }
            
            for decision in decisions:
                # Count by effect
                effect = decision.get('decision', 'Deny')
                report['decisions_by_effect'][effect] += 1
                
                # Count rule usage
                for rule_id in decision.get('applicable_rules', []):
                    report['most_used_rules'][rule_id] = report['most_used_rules'].get(rule_id, 0) + 1
                
                # Analyze access patterns
                context = decision.get('access_context', {})
                subject = context.get('subject', {})
                department = subject.get('department', 'unknown')
                report['access_patterns'][department] = report['access_patterns'].get(department, 0) + 1
                
                # Check for compliance issues
                if 'emergency-access' in decision.get('applicable_rules', []):
                    report['compliance_summary']['emergency_access_used'] += 1
                
                if effect == 'Deny' and 'business-hours-only' in decision.get('applicable_rules', []):
                    report['compliance_summary']['after_hours_attempts'] += 1
            
            return report
            
        except Exception as e:
            logger.error(f"Error generating ABAC report: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }

# Example usage
if __name__ == "__main__":
    # Initialize ABAC controller
    abac_controller = ABACAccessController()
    
    # Example access request evaluation
    decision = abac_controller.evaluate_access_request(
        subject_attributes={
            'department': 'finance',
            'role': 'analyst',
            'clearance_level': 'confidential'
        },
        resource_attributes={
            'classification': 'confidential',
            'department': 'finance',
            'owner_role': 'manager'
        },
        environment_attributes={
            'time': '14:30',
            'network': 'corporate',
            'mfa_authenticated': 'true'
        },
        action='s3:GetObject'
    )
    print(f"ABAC decision: {decision}")
    
    # Create dynamic policy
    policy_result = abac_controller.create_dynamic_policy(
        'arn:aws:iam::123456789012:role/FinanceAnalyst',
        'arn:aws:s3:::finance-data-bucket',
        subject_attributes={
            'department': 'finance',
            'role': 'analyst'
        },
        resource_attributes={
            'classification': 'confidential',
            'department': 'finance'
        }
    )
    print(f"Dynamic policy result: {policy_result}")
    
    # Generate ABAC report
    report = abac_controller.generate_abac_report(days=7)
    print(f"ABAC report: {json.dumps(report, indent=2)}")
```

### Example 3: CloudFormation Template for Comprehensive Access Control

```yaml
# comprehensive-access-control.yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Comprehensive access control infrastructure for data at rest'

Parameters:
  Environment:
    Type: String
    Default: 'prod'
    AllowedValues: ['dev', 'staging', 'prod']
  
  OrganizationId:
    Type: String
    Description: 'AWS Organization ID for cross-account access control'

Resources:
  # VPC for secure data access
  DataAccessVPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: 10.0.0.0/16
      EnableDnsHostnames: true
      EnableDnsSupport: true
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-data-access-vpc'
        - Key: Environment
          Value: !Ref Environment

  # Private subnets for secure access
  PrivateSubnet1:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref DataAccessVPC
      CidrBlock: 10.0.1.0/24
      AvailabilityZone: !Select [0, !GetAZs '']
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-private-subnet-1'

  PrivateSubnet2:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref DataAccessVPC
      CidrBlock: 10.0.2.0/24
      AvailabilityZone: !Select [1, !GetAZs '']
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-private-subnet-2'

  # Security group for data access
  DataAccessSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupName: !Sub '${Environment}-data-access-sg'
      GroupDescription: 'Security group for secure data access'
      VpcId: !Ref DataAccessVPC
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 443
          ToPort: 443
          CidrIp: 10.0.0.0/16
          Description: 'HTTPS access within VPC'
      SecurityGroupEgress:
        - IpProtocol: tcp
          FromPort: 443
          ToPort: 443
          CidrIp: 0.0.0.0/0
          Description: 'HTTPS outbound access'
      Tags:
        - Key: Environment
          Value: !Ref Environment

  # VPC Endpoints for secure AWS service access
  S3VPCEndpoint:
    Type: AWS::EC2::VPCEndpoint
    Properties:
      VpcId: !Ref DataAccessVPC
      ServiceName: !Sub 'com.amazonaws.${AWS::Region}.s3'
      VpcEndpointType: Gateway
      RouteTableIds:
        - !Ref PrivateRouteTable

  KMSVPCEndpoint:
    Type: AWS::EC2::VPCEndpoint
    Properties:
      VpcId: !Ref DataAccessVPC
      ServiceName: !Sub 'com.amazonaws.${AWS::Region}.kms'
      VpcEndpointType: Interface
      SubnetIds:
        - !Ref PrivateSubnet1
        - !Ref PrivateSubnet2
      SecurityGroupIds:
        - !Ref DataAccessSecurityGroup

  # Route table for private subnets
  PrivateRouteTable:
    Type: AWS::EC2::RouteTable
    Properties:
      VpcId: !Ref DataAccessVPC
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-private-rt'

  PrivateSubnet1RouteTableAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      SubnetId: !Ref PrivateSubnet1
      RouteTableId: !Ref PrivateRouteTable

  PrivateSubnet2RouteTableAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      SubnetId: !Ref PrivateSubnet2
      RouteTableId: !Ref PrivateRouteTable

  # IAM roles for different access levels
  PublicDataAccessRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: !Sub '${Environment}-public-data-access-role'
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              AWS: !Sub 'arn:aws:iam::${AWS::AccountId}:root'
            Action: sts:AssumeRole
            Condition:
              StringEquals:
                'aws:PrincipalOrgID': !Ref OrganizationId
      Policies:
        - PolicyName: PublicDataAccessPolicy
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - 's3:GetObject'
                  - 's3:ListBucket'
                Resource: '*'
                Condition:
                  StringEquals:
                    's3:ExistingObjectTag/DataClassification': 'public'
      Tags:
        - Key: Environment
          Value: !Ref Environment
        - Key: AccessLevel
          Value: public

  InternalDataAccessRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: !Sub '${Environment}-internal-data-access-role'
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              AWS: !Sub 'arn:aws:iam::${AWS::AccountId}:root'
            Action: sts:AssumeRole
            Condition:
              StringEquals:
                'aws:PrincipalOrgID': !Ref OrganizationId
              Bool:
                'aws:SecureTransport': 'true'
      Policies:
        - PolicyName: InternalDataAccessPolicy
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - 's3:GetObject'
                  - 's3:PutObject'
                  - 's3:ListBucket'
                Resource: '*'
                Condition:
                  StringEquals:
                    's3:ExistingObjectTag/DataClassification': 'internal'
                  IpAddress:
                    'aws:SourceIp': 
                      - '10.0.0.0/8'
                      - '172.16.0.0/12'
                      - '192.168.0.0/16'
      Tags:
        - Key: Environment
          Value: !Ref Environment
        - Key: AccessLevel
          Value: internal

  ConfidentialDataAccessRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: !Sub '${Environment}-confidential-data-access-role'
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              AWS: !Sub 'arn:aws:iam::${AWS::AccountId}:root'
            Action: sts:AssumeRole
            Condition:
              StringEquals:
                'aws:PrincipalOrgID': !Ref OrganizationId
              Bool:
                'aws:MultiFactorAuthPresent': 'true'
                'aws:SecureTransport': 'true'
              NumericLessThan:
                'aws:MultiFactorAuthAge': '3600'
      Policies:
        - PolicyName: ConfidentialDataAccessPolicy
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - 's3:GetObject'
                  - 's3:ListBucket'
                Resource: '*'
                Condition:
                  StringEquals:
                    's3:ExistingObjectTag/DataClassification': 'confidential'
                  Bool:
                    'aws:MultiFactorAuthPresent': 'true'
                  NumericLessThan:
                    'aws:MultiFactorAuthAge': '3600'
                  IpAddress:
                    'aws:SourceIp': 
                      - '10.0.0.0/8'
                      - '172.16.0.0/12'
              - Effect: Allow
                Action:
                  - 'kms:Decrypt'
                  - 'kms:DescribeKey'
                Resource: '*'
                Condition:
                  StringEquals:
                    'kms:ViaService': !Sub 's3.${AWS::Region}.amazonaws.com'
      Tags:
        - Key: Environment
          Value: !Ref Environment
        - Key: AccessLevel
          Value: confidential

  RestrictedDataAccessRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: !Sub '${Environment}-restricted-data-access-role'
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              AWS: !Sub 'arn:aws:iam::${AWS::AccountId}:root'
            Action: sts:AssumeRole
            Condition:
              StringEquals:
                'aws:PrincipalOrgID': !Ref OrganizationId
              Bool:
                'aws:MultiFactorAuthPresent': 'true'
                'aws:SecureTransport': 'true'
              NumericLessThan:
                'aws:MultiFactorAuthAge': '1800'
              DateGreaterThan:
                'aws:CurrentTime': '08:00:00Z'
              DateLessThan:
                'aws:CurrentTime': '18:00:00Z'
      Policies:
        - PolicyName: RestrictedDataAccessPolicy
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - 's3:GetObject'
                Resource: '*'
                Condition:
                  StringEquals:
                    's3:ExistingObjectTag/DataClassification': 'restricted'
                  Bool:
                    'aws:MultiFactorAuthPresent': 'true'
                  NumericLessThan:
                    'aws:MultiFactorAuthAge': '1800'
                  IpAddress:
                    'aws:SourceIp': '10.0.0.0/16'
                  DateGreaterThan:
                    'aws:CurrentTime': '08:00:00Z'
                  DateLessThan:
                    'aws:CurrentTime': '18:00:00Z'
              - Effect: Allow
                Action:
                  - 'kms:Decrypt'
                  - 'kms:DescribeKey'
                Resource: '*'
                Condition:
                  StringEquals:
                    'kms:ViaService': !Sub 's3.${AWS::Region}.amazonaws.com'
      Tags:
        - Key: Environment
          Value: !Ref Environment
        - Key: AccessLevel
          Value: restricted

  # Lambda function for access request processing
  AccessRequestProcessor:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: !Sub '${Environment}-access-request-processor'
      Runtime: python3.9
      Handler: index.lambda_handler
      Role: !GetAtt AccessRequestProcessorRole.Arn
      Timeout: 300
      Environment:
        Variables:
          ENVIRONMENT: !Ref Environment
      Code:
        ZipFile: |
          import boto3
          import json
          import os
          from datetime import datetime, timedelta
          
          def lambda_handler(event, context):
              """Process access requests and apply appropriate controls"""
              
              sts = boto3.client('sts')
              iam = boto3.client('iam')
              
              try:
                  # Extract request details
                  principal = event.get('principal', '')
                  resource_arn = event.get('resource_arn', '')
                  data_classification = event.get('data_classification', 'internal')
                  duration_hours = event.get('duration_hours', 1)
                  justification = event.get('justification', '')
                  
                  # Determine appropriate role based on classification
                  role_mapping = {
                      'public': f"arn:aws:iam::{context.invoked_function_arn.split(':')[4]}:role/{os.environ['ENVIRONMENT']}-public-data-access-role",
                      'internal': f"arn:aws:iam::{context.invoked_function_arn.split(':')[4]}:role/{os.environ['ENVIRONMENT']}-internal-data-access-role",
                      'confidential': f"arn:aws:iam::{context.invoked_function_arn.split(':')[4]}:role/{os.environ['ENVIRONMENT']}-confidential-data-access-role",
                      'restricted': f"arn:aws:iam::{context.invoked_function_arn.split(':')[4]}:role/{os.environ['ENVIRONMENT']}-restricted-data-access-role"
                  }
                  
                  target_role = role_mapping.get(data_classification)
                  if not target_role:
                      return {
                          'statusCode': 400,
                          'body': json.dumps({'error': f'Unknown classification: {data_classification}'})
                      }
                  
                  # Generate temporary credentials
                  session_name = f"temp-access-{int(datetime.utcnow().timestamp())}"
                  
                  response = sts.assume_role(
                      RoleArn=target_role,
                      RoleSessionName=session_name,
                      DurationSeconds=duration_hours * 3600
                  )
                  
                  credentials = response['Credentials']
                  
                  return {
                      'statusCode': 200,
                      'body': json.dumps({
                          'access_key_id': credentials['AccessKeyId'],
                          'secret_access_key': credentials['SecretAccessKey'],
                          'session_token': credentials['SessionToken'],
                          'expiration': credentials['Expiration'].isoformat(),
                          'role_arn': target_role,
                          'session_name': session_name
                      }, default=str)
                  }
                  
              except Exception as e:
                  return {
                      'statusCode': 500,
                      'body': json.dumps({'error': str(e)})
                  }

  AccessRequestProcessorRole:
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
        - PolicyName: AccessRequestProcessorPolicy
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - 'sts:AssumeRole'
                Resource:
                  - !GetAtt PublicDataAccessRole.Arn
                  - !GetAtt InternalDataAccessRole.Arn
                  - !GetAtt ConfidentialDataAccessRole.Arn
                  - !GetAtt RestrictedDataAccessRole.Arn

  # CloudWatch Log Group for access monitoring
  AccessControlLogGroup:
    Type: AWS::Logs::LogGroup
    Properties:
      LogGroupName: !Sub '/aws/access-control/${Environment}'
      RetentionInDays: 90

  # CloudWatch Alarms for access monitoring
  UnauthorizedAccessAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: !Sub '${Environment}-unauthorized-access-attempts'
      AlarmDescription: 'Monitor for unauthorized access attempts'
      MetricName: ErrorCount
      Namespace: AWS/ApiGateway
      Statistic: Sum
      Period: 300
      EvaluationPeriods: 2
      Threshold: 5
      ComparisonOperator: GreaterThanThreshold
      AlarmActions:
        - !Ref SecurityNotificationTopic

  # SNS Topic for security notifications
  SecurityNotificationTopic:
    Type: AWS::SNS::Topic
    Properties:
      TopicName: !Sub '${Environment}-access-control-notifications'
      DisplayName: 'Access Control Security Notifications'

Outputs:
  VPCId:
    Description: 'ID of the data access VPC'
    Value: !Ref DataAccessVPC
    Export:
      Name: !Sub '${AWS::StackName}-VPC'
  
  PublicDataRoleArn:
    Description: 'ARN of the public data access role'
    Value: !GetAtt PublicDataAccessRole.Arn
    Export:
      Name: !Sub '${AWS::StackName}-PublicDataRole'
  
  InternalDataRoleArn:
    Description: 'ARN of the internal data access role'
    Value: !GetAtt InternalDataAccessRole.Arn
    Export:
      Name: !Sub '${AWS::StackName}-InternalDataRole'
  
  ConfidentialDataRoleArn:
    Description: 'ARN of the confidential data access role'
    Value: !GetAtt ConfidentialDataAccessRole.Arn
    Export:
      Name: !Sub '${AWS::StackName}-ConfidentialDataRole'
  
  RestrictedDataRoleArn:
    Description: 'ARN of the restricted data access role'
    Value: !GetAtt RestrictedDataAccessRole.Arn
    Export:
      Name: !Sub '${AWS::StackName}-RestrictedDataRole'
  
  AccessRequestProcessorArn:
    Description: 'ARN of the access request processor function'
    Value: !GetAtt AccessRequestProcessor.Arn
    Export:
      Name: !Sub '${AWS::StackName}-AccessRequestProcessor'
```

## Relevant AWS Services

### Identity and Access Management
- **AWS Identity and Access Management (IAM)**: Fine-grained access control policies and roles
- **AWS Single Sign-On (SSO)**: Centralized access management across AWS accounts
- **Amazon Cognito**: User authentication and authorization for applications
- **AWS Security Token Service (STS)**: Temporary credential generation

### Network Access Control
- **Amazon VPC**: Network isolation and security groups
- **AWS PrivateLink**: Private connectivity to AWS services
- **VPC Endpoints**: Secure access to AWS services without internet gateway
- **AWS Direct Connect**: Dedicated network connection to AWS

### Resource-Based Access Control
- **Amazon S3**: Bucket policies and access control lists
- **AWS Key Management Service (KMS)**: Key policies for encryption access control
- **Amazon RDS**: Database-level access control and resource policies
- **AWS Lambda**: Function-level access control and resource policies

### Monitoring and Auditing
- **AWS CloudTrail**: Comprehensive audit logging of access attempts
- **Amazon CloudWatch**: Monitoring and alerting for access patterns
- **VPC Flow Logs**: Network-level access monitoring
- **AWS Config**: Configuration compliance monitoring

### Automation and Governance
- **AWS Organizations**: Service Control Policies for organization-wide access control
- **AWS Control Tower**: Automated governance and compliance
- **AWS Systems Manager**: Automated access provisioning and management
- **Amazon EventBridge**: Event-driven access control workflows

## Benefits of Enforcing Access Control

### Security Benefits
- **Defense in Depth**: Multiple layers of access control protection
- **Principle of Least Privilege**: Minimal necessary access permissions
- **Dynamic Access Control**: Context-aware access decisions
- **Comprehensive Auditing**: Complete visibility into access patterns

### Operational Benefits
- **Automated Provisioning**: Consistent access control implementation
- **Centralized Management**: Single point of control for access policies
- **Scalable Architecture**: Access control that grows with infrastructure
- **Reduced Administrative Overhead**: Automated access management

### Compliance Benefits
- **Regulatory Adherence**: Meet compliance requirements for data access
- **Audit Readiness**: Complete audit trails for access control
- **Policy Enforcement**: Consistent enforcement of access policies
- **Risk Management**: Controlled access to sensitive data

### Business Benefits
- **Data Protection**: Safeguard valuable business data assets
- **Operational Continuity**: Secure access without business disruption
- **Cost Optimization**: Efficient access control resource utilization
- **Competitive Advantage**: Secure data handling as business differentiator

## Related Resources

- [AWS Well-Architected Framework - Data at Rest Protection](https://docs.aws.amazon.com/wellarchitected/latest/framework/sec-08.html)
- [AWS IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [Amazon S3 Access Control](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-overview.html)
- [AWS Security Blog - Access Control](https://aws.amazon.com/blogs/security/tag/access-control/)
- [NIST Access Control Guidelines](https://csrc.nist.gov/publications/detail/sp/800-162/final)
- [AWS Security Reference Architecture](https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/welcome.html)
```
```
