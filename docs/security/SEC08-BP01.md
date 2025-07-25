---
title: "SEC08-BP01: Implement secure key management"
layout: default
parent: "SEC08 - How do you protect your data at rest?"
grand_parent: Security
nav_order: 1
---

# SEC08-BP01: Implement secure key management

## Overview

Secure key management is fundamental to protecting data at rest. Encryption keys must be properly generated, stored, rotated, and managed throughout their lifecycle to ensure the confidentiality and integrity of encrypted data. Poor key management can render even the strongest encryption ineffective.

This best practice focuses on implementing comprehensive key management strategies using AWS Key Management Service (KMS) and other AWS services to ensure encryption keys are securely managed, properly rotated, and appropriately controlled throughout their lifecycle.

## Implementation Guidance

### 1. Use AWS Key Management Service (KMS)

Leverage AWS KMS for centralized key management:

- **Customer Managed Keys**: Create and manage your own KMS keys for full control
- **AWS Managed Keys**: Use service-specific AWS managed keys for simplified management
- **Key Policies**: Implement fine-grained access controls for key usage
- **Cross-Account Access**: Enable secure key sharing across AWS accounts

### 2. Implement Key Rotation

Establish automated key rotation policies:

- **Automatic Rotation**: Enable automatic annual rotation for customer managed keys
- **Manual Rotation**: Implement manual rotation for specific compliance requirements
- **Rotation Monitoring**: Track rotation status and compliance
- **Backward Compatibility**: Ensure rotated keys maintain access to existing encrypted data

### 3. Establish Key Lifecycle Management

Manage keys throughout their entire lifecycle:

- **Key Creation**: Secure key generation with proper entropy
- **Key Distribution**: Secure key distribution and provisioning
- **Key Usage**: Monitor and audit key usage patterns
- **Key Archival**: Properly archive keys for compliance and recovery
- **Key Destruction**: Securely destroy keys when no longer needed

### 4. Implement Access Controls

Control who can use and manage encryption keys:

- **Principle of Least Privilege**: Grant minimum necessary key permissions
- **Role-Based Access**: Use IAM roles for key access management
- **Multi-Factor Authentication**: Require MFA for sensitive key operations
- **Cross-Service Access**: Control key usage across different AWS services

### 5. Enable Monitoring and Auditing

Implement comprehensive key usage monitoring:

- **CloudTrail Integration**: Log all key management operations
- **CloudWatch Metrics**: Monitor key usage patterns and anomalies
- **AWS Config**: Track key configuration compliance
- **Alerting**: Set up alerts for unauthorized key usage attempts

### 6. Plan for Disaster Recovery

Ensure key availability for disaster recovery scenarios:

- **Multi-Region Keys**: Use multi-region keys for global applications
- **Key Backup**: Implement secure key backup strategies
- **Recovery Procedures**: Establish key recovery procedures
- **Business Continuity**: Ensure key availability doesn't impact business operations

## Implementation Examples

### Example 1: Comprehensive KMS Key Management System

```python
# kms_key_manager.py
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
class KeyPolicy:
    key_id: str
    policy_document: Dict[str, Any]
    description: str
    compliance_frameworks: List[str]

@dataclass
class KeyMetadata:
    key_id: str
    key_arn: str
    description: str
    key_usage: str
    key_state: str
    creation_date: datetime
    deletion_date: Optional[datetime]
    rotation_enabled: bool
    multi_region: bool
    tags: Dict[str, str]

class KMSKeyManager:
    """
    Comprehensive AWS KMS key management system
    """
    
    def __init__(self, region: str = 'us-east-1'):
        self.region = region
        self.kms_client = boto3.client('kms', region_name=region)
        self.iam_client = boto3.client('iam', region_name=region)
        self.cloudtrail_client = boto3.client('cloudtrail', region_name=region)
        self.cloudwatch = boto3.client('cloudwatch', region_name=region)
        self.dynamodb = boto3.resource('dynamodb', region_name=region)
        
        # Key management tracking table
        self.key_tracking_table = self.dynamodb.Table('kms-key-management-tracking')
        
        # Standard key policies
        self.standard_policies = self._define_standard_key_policies()
    
    def _define_standard_key_policies(self) -> Dict[str, KeyPolicy]:
        """
        Define standard key policies for different use cases
        """
        account_id = self._get_account_id()
        
        return {
            'application_key': KeyPolicy(
                key_id='',
                policy_document={
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
                            "Sid": "Allow use of the key for application",
                            "Effect": "Allow",
                            "Principal": {"AWS": f"arn:aws:iam::{account_id}:role/ApplicationRole"},
                            "Action": [
                                "kms:Encrypt",
                                "kms:Decrypt",
                                "kms:ReEncrypt*",
                                "kms:GenerateDataKey*",
                                "kms:DescribeKey"
                            ],
                            "Resource": "*"
                        },
                        {
                            "Sid": "Allow attachment of persistent resources",
                            "Effect": "Allow",
                            "Principal": {"AWS": f"arn:aws:iam::{account_id}:role/ApplicationRole"},
                            "Action": [
                                "kms:CreateGrant",
                                "kms:ListGrants",
                                "kms:RevokeGrant"
                            ],
                            "Resource": "*",
                            "Condition": {
                                "Bool": {"kms:GrantIsForAWSResource": "true"}
                            }
                        }
                    ]
                },
                description='Standard policy for application encryption keys',
                compliance_frameworks=['SOX', 'PCI_DSS']
            ),
            
            'database_key': KeyPolicy(
                key_id='',
                policy_document={
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
                            "Sid": "Allow RDS service to use the key",
                            "Effect": "Allow",
                            "Principal": {"Service": "rds.amazonaws.com"},
                            "Action": [
                                "kms:Encrypt",
                                "kms:Decrypt",
                                "kms:ReEncrypt*",
                                "kms:GenerateDataKey*",
                                "kms:DescribeKey",
                                "kms:CreateGrant"
                            ],
                            "Resource": "*"
                        },
                        {
                            "Sid": "Allow database administrators",
                            "Effect": "Allow",
                            "Principal": {"AWS": f"arn:aws:iam::{account_id}:role/DatabaseAdminRole"},
                            "Action": [
                                "kms:Decrypt",
                                "kms:DescribeKey"
                            ],
                            "Resource": "*",
                            "Condition": {
                                "StringEquals": {
                                    "kms:ViaService": f"rds.{self.region}.amazonaws.com"
                                }
                            }
                        }
                    ]
                },
                description='Policy for database encryption keys',
                compliance_frameworks=['HIPAA', 'GDPR']
            ),
            
            'backup_key': KeyPolicy(
                key_id='',
                policy_document={
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
                            "Sid": "Allow AWS Backup service",
                            "Effect": "Allow",
                            "Principal": {"Service": "backup.amazonaws.com"},
                            "Action": [
                                "kms:Encrypt",
                                "kms:Decrypt",
                                "kms:ReEncrypt*",
                                "kms:GenerateDataKey*",
                                "kms:DescribeKey",
                                "kms:CreateGrant"
                            ],
                            "Resource": "*"
                        },
                        {
                            "Sid": "Allow backup administrators",
                            "Effect": "Allow",
                            "Principal": {"AWS": f"arn:aws:iam::{account_id}:role/BackupAdminRole"},
                            "Action": [
                                "kms:Decrypt",
                                "kms:DescribeKey",
                                "kms:ListGrants"
                            ],
                            "Resource": "*"
                        }
                    ]
                },
                description='Policy for backup encryption keys',
                compliance_frameworks=['SOX', 'HIPAA']
            )
        }
    
    def create_customer_managed_key(self, 
                                  key_description: str,
                                  key_usage: str = 'ENCRYPT_DECRYPT',
                                  policy_type: str = 'application_key',
                                  enable_rotation: bool = True,
                                  multi_region: bool = False,
                                  tags: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Create a customer managed KMS key with specified configuration
        """
        try:
            # Prepare key creation parameters
            create_params = {
                'Description': key_description,
                'KeyUsage': key_usage,
                'KeySpec': 'SYMMETRIC_DEFAULT',
                'Origin': 'AWS_KMS',
                'MultiRegion': multi_region
            }
            
            # Add tags if provided
            if tags:
                tag_list = [{'TagKey': k, 'TagValue': v} for k, v in tags.items()]
                create_params['Tags'] = tag_list
            
            # Create the key
            response = self.kms_client.create_key(**create_params)
            key_id = response['KeyMetadata']['KeyId']
            key_arn = response['KeyMetadata']['Arn']
            
            # Apply key policy
            if policy_type in self.standard_policies:
                policy = self.standard_policies[policy_type]
                policy.key_id = key_id
                
                self.kms_client.put_key_policy(
                    KeyId=key_id,
                    PolicyName='default',
                    Policy=json.dumps(policy.policy_document)
                )
            
            # Enable key rotation if requested
            if enable_rotation:
                self.kms_client.enable_key_rotation(KeyId=key_id)
            
            # Create key alias
            alias_name = f"alias/{key_description.lower().replace(' ', '-')}"
            try:
                self.kms_client.create_alias(
                    AliasName=alias_name,
                    TargetKeyId=key_id
                )
            except self.kms_client.exceptions.AlreadyExistsException:
                # Alias already exists, update it
                self.kms_client.update_alias(
                    AliasName=alias_name,
                    TargetKeyId=key_id
                )
            
            # Track key creation
            self._track_key_operation(key_id, 'CREATE', {
                'description': key_description,
                'policy_type': policy_type,
                'rotation_enabled': enable_rotation,
                'multi_region': multi_region
            })
            
            logger.info(f"Created KMS key: {key_id} with alias: {alias_name}")
            
            return {
                'status': 'success',
                'key_id': key_id,
                'key_arn': key_arn,
                'alias_name': alias_name,
                'rotation_enabled': enable_rotation,
                'multi_region': multi_region
            }
            
        except Exception as e:
            logger.error(f"Error creating KMS key: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def rotate_key(self, key_id: str, force_rotation: bool = False) -> Dict[str, Any]:
        """
        Rotate a customer managed key
        """
        try:
            # Check if key supports rotation
            key_metadata = self.kms_client.describe_key(KeyId=key_id)['KeyMetadata']
            
            if key_metadata['KeyManager'] != 'CUSTOMER':
                return {
                    'status': 'error',
                    'message': 'Only customer managed keys can be manually rotated'
                }
            
            # Check current rotation status
            rotation_status = self.kms_client.get_key_rotation_status(KeyId=key_id)
            
            if not rotation_status['KeyRotationEnabled'] and not force_rotation:
                return {
                    'status': 'error',
                    'message': 'Key rotation is not enabled. Use force_rotation=True to override.'
                }
            
            # Enable rotation if not already enabled
            if not rotation_status['KeyRotationEnabled']:
                self.kms_client.enable_key_rotation(KeyId=key_id)
            
            # For immediate rotation, we need to create a new key version
            # This is done automatically by AWS KMS during the rotation process
            
            # Track rotation operation
            self._track_key_operation(key_id, 'ROTATE', {
                'forced': force_rotation,
                'previous_rotation_enabled': rotation_status['KeyRotationEnabled']
            })
            
            logger.info(f"Key rotation initiated for key: {key_id}")
            
            return {
                'status': 'success',
                'key_id': key_id,
                'rotation_enabled': True,
                'message': 'Key rotation initiated successfully'
            }
            
        except Exception as e:
            logger.error(f"Error rotating key {key_id}: {str(e)}")
            return {
                'status': 'error',
                'key_id': key_id,
                'message': str(e)
            }
    
    def audit_key_usage(self, key_id: str, days: int = 30) -> Dict[str, Any]:
        """
        Audit key usage patterns and compliance
        """
        try:
            # Get key metadata
            key_metadata = self.kms_client.describe_key(KeyId=key_id)['KeyMetadata']
            
            # Get CloudTrail events for key usage
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(days=days)
            
            events = self.cloudtrail_client.lookup_events(
                LookupAttributes=[
                    {
                        'AttributeKey': 'ResourceName',
                        'AttributeValue': key_id
                    }
                ],
                StartTime=start_time,
                EndTime=end_time
            )
            
            # Analyze usage patterns
            usage_analysis = {
                'key_id': key_id,
                'key_arn': key_metadata['Arn'],
                'analysis_period_days': days,
                'total_operations': len(events['Events']),
                'operations_by_type': {},
                'operations_by_user': {},
                'operations_by_service': {},
                'compliance_status': 'compliant',
                'recommendations': []
            }
            
            for event in events['Events']:
                event_name = event['EventName']
                username = event.get('Username', 'Unknown')
                source_ip = event.get('SourceIPAddress', 'Unknown')
                
                # Count operations by type
                usage_analysis['operations_by_type'][event_name] = \
                    usage_analysis['operations_by_type'].get(event_name, 0) + 1
                
                # Count operations by user
                usage_analysis['operations_by_user'][username] = \
                    usage_analysis['operations_by_user'].get(username, 0) + 1
                
                # Identify service usage
                if '.amazonaws.com' in source_ip:
                    service = source_ip.split('.')[0]
                    usage_analysis['operations_by_service'][service] = \
                        usage_analysis['operations_by_service'].get(service, 0) + 1
            
            # Check compliance
            compliance_issues = self._check_key_compliance(key_id, key_metadata, usage_analysis)
            if compliance_issues:
                usage_analysis['compliance_status'] = 'non_compliant'
                usage_analysis['recommendations'].extend(compliance_issues)
            
            return usage_analysis
            
        except Exception as e:
            logger.error(f"Error auditing key usage for {key_id}: {str(e)}")
            return {
                'status': 'error',
                'key_id': key_id,
                'message': str(e)
            }
    
    def _check_key_compliance(self, key_id: str, key_metadata: Dict[str, Any], usage_analysis: Dict[str, Any]) -> List[str]:
        """
        Check key compliance against best practices
        """
        issues = []
        
        # Check if rotation is enabled
        try:
            rotation_status = self.kms_client.get_key_rotation_status(KeyId=key_id)
            if not rotation_status['KeyRotationEnabled'] and key_metadata['KeyManager'] == 'CUSTOMER':
                issues.append('Key rotation is not enabled for customer managed key')
        except:
            pass
        
        # Check key age
        key_age = datetime.utcnow() - key_metadata['CreationDate'].replace(tzinfo=None)
        if key_age.days > 365:
            issues.append(f'Key is {key_age.days} days old - consider rotation')
        
        # Check for excessive permissions
        if usage_analysis['total_operations'] == 0:
            issues.append('Key has not been used in the analysis period - consider deletion')
        
        # Check for unusual access patterns
        decrypt_ops = usage_analysis['operations_by_type'].get('Decrypt', 0)
        encrypt_ops = usage_analysis['operations_by_type'].get('Encrypt', 0)
        
        if decrypt_ops > encrypt_ops * 10:  # More than 10:1 ratio
            issues.append('Unusual access pattern detected - high decrypt to encrypt ratio')
        
        return issues
    
    def _track_key_operation(self, key_id: str, operation: str, metadata: Dict[str, Any]):
        """
        Track key operations in DynamoDB
        """
        try:
            self.key_tracking_table.put_item(
                Item={
                    'key_id': key_id,
                    'timestamp': datetime.utcnow().isoformat(),
                    'operation': operation,
                    'metadata': metadata,
                    'ttl': int((datetime.utcnow() + timedelta(days=365)).timestamp())
                }
            )
        except Exception as e:
            logger.error(f"Error tracking key operation: {str(e)}")
    
    def _get_account_id(self) -> str:
        """Get AWS account ID"""
        return boto3.client('sts').get_caller_identity()['Account']

# Example usage
if __name__ == "__main__":
    # Initialize key manager
    key_manager = KMSKeyManager()
    
    # Create application encryption key
    app_key_result = key_manager.create_customer_managed_key(
        key_description='Application Data Encryption Key',
        policy_type='application_key',
        enable_rotation=True,
        tags={
            'Environment': 'Production',
            'Application': 'WebApp',
            'DataClassification': 'Confidential'
        }
    )
    print(f"Application key creation: {app_key_result}")
    
    # Create database encryption key
    db_key_result = key_manager.create_customer_managed_key(
        key_description='Database Encryption Key',
        policy_type='database_key',
        enable_rotation=True,
        tags={
            'Environment': 'Production',
            'Service': 'RDS',
            'DataClassification': 'Restricted'
        }
    )
    print(f"Database key creation: {db_key_result}")
    
    # Audit key usage
    if app_key_result['status'] == 'success':
        audit_result = key_manager.audit_key_usage(app_key_result['key_id'])
        print(f"Key audit result: {audit_result}")
```

### Example 2: Multi-Region Key Management with Disaster Recovery

```python
# multi_region_key_manager.py
import boto3
import json
from typing import Dict, List, Any
from dataclasses import dataclass
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@dataclass
class MultiRegionKeyConfig:
    primary_region: str
    replica_regions: List[str]
    key_description: str
    policy_document: Dict[str, Any]
    tags: Dict[str, str]

class MultiRegionKeyManager:
    """
    Manages KMS keys across multiple AWS regions for disaster recovery
    """
    
    def __init__(self, primary_region: str = 'us-east-1'):
        self.primary_region = primary_region
        self.kms_clients = {}
        self.regions = ['us-east-1', 'us-west-2', 'eu-west-1']
        
        # Initialize KMS clients for all regions
        for region in self.regions:
            self.kms_clients[region] = boto3.client('kms', region_name=region)
    
    def create_multi_region_key(self, config: MultiRegionKeyConfig) -> Dict[str, Any]:
        """
        Create a multi-region KMS key with replicas
        """
        try:
            primary_client = self.kms_clients[config.primary_region]
            
            # Create primary multi-region key
            primary_response = primary_client.create_key(
                Description=config.key_description,
                KeyUsage='ENCRYPT_DECRYPT',
                KeySpec='SYMMETRIC_DEFAULT',
                Origin='AWS_KMS',
                MultiRegion=True,
                Tags=[{'TagKey': k, 'TagValue': v} for k, v in config.tags.items()]
            )
            
            primary_key_id = primary_response['KeyMetadata']['KeyId']
            primary_key_arn = primary_response['KeyMetadata']['Arn']
            
            # Apply key policy to primary key
            primary_client.put_key_policy(
                KeyId=primary_key_id,
                PolicyName='default',
                Policy=json.dumps(config.policy_document)
            )
            
            # Enable rotation on primary key
            primary_client.enable_key_rotation(KeyId=primary_key_id)
            
            # Create replica keys in other regions
            replica_keys = {}
            for region in config.replica_regions:
                if region != config.primary_region and region in self.kms_clients:
                    replica_client = self.kms_clients[region]
                    
                    replica_response = replica_client.replicate_key(
                        KeyId=primary_key_id,
                        ReplicaRegion=region,
                        Description=f"{config.key_description} - {region} replica",
                        Tags=[{'TagKey': k, 'TagValue': v} for k, v in config.tags.items()]
                    )
                    
                    replica_key_id = replica_response['ReplicaKeyMetadata']['KeyId']
                    replica_keys[region] = {
                        'key_id': replica_key_id,
                        'key_arn': replica_response['ReplicaKeyMetadata']['Arn']
                    }
                    
                    # Apply same policy to replica
                    replica_client.put_key_policy(
                        KeyId=replica_key_id,
                        PolicyName='default',
                        Policy=json.dumps(config.policy_document)
                    )
            
            result = {
                'status': 'success',
                'primary_key': {
                    'region': config.primary_region,
                    'key_id': primary_key_id,
                    'key_arn': primary_key_arn
                },
                'replica_keys': replica_keys,
                'total_regions': len(replica_keys) + 1
            }
            
            logger.info(f"Created multi-region key with {len(replica_keys)} replicas")
            return result
            
        except Exception as e:
            logger.error(f"Error creating multi-region key: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def test_cross_region_encryption(self, primary_key_id: str, test_data: str = "Test encryption data") -> Dict[str, Any]:
        """
        Test encryption/decryption across regions
        """
        results = {
            'test_data': test_data,
            'encryption_tests': {},
            'cross_region_tests': {},
            'overall_status': 'success'
        }
        
        try:
            # Test encryption in each region
            encrypted_data = {}
            
            for region, client in self.kms_clients.items():
                try:
                    # Encrypt data in this region
                    encrypt_response = client.encrypt(
                        KeyId=primary_key_id,
                        Plaintext=test_data.encode()
                    )
                    
                    encrypted_data[region] = encrypt_response['CiphertextBlob']
                    results['encryption_tests'][region] = 'success'
                    
                except Exception as e:
                    results['encryption_tests'][region] = f'failed: {str(e)}'
                    results['overall_status'] = 'partial_failure'
            
            # Test cross-region decryption
            for encrypt_region, ciphertext in encrypted_data.items():
                for decrypt_region, client in self.kms_clients.items():
                    test_key = f"{encrypt_region}_to_{decrypt_region}"
                    
                    try:
                        decrypt_response = client.decrypt(CiphertextBlob=ciphertext)
                        decrypted_text = decrypt_response['Plaintext'].decode()
                        
                        if decrypted_text == test_data:
                            results['cross_region_tests'][test_key] = 'success'
                        else:
                            results['cross_region_tests'][test_key] = 'data_mismatch'
                            results['overall_status'] = 'partial_failure'
                            
                    except Exception as e:
                        results['cross_region_tests'][test_key] = f'failed: {str(e)}'
                        results['overall_status'] = 'partial_failure'
            
            return results
            
        except Exception as e:
            logger.error(f"Error testing cross-region encryption: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def monitor_key_health(self, key_id: str) -> Dict[str, Any]:
        """
        Monitor key health across all regions
        """
        health_status = {
            'key_id': key_id,
            'timestamp': datetime.utcnow().isoformat(),
            'region_status': {},
            'overall_health': 'healthy',
            'issues': []
        }
        
        for region, client in self.kms_clients.items():
            try:
                # Check key status
                key_response = client.describe_key(KeyId=key_id)
                key_metadata = key_response['KeyMetadata']
                
                region_health = {
                    'key_state': key_metadata['KeyState'],
                    'enabled': key_metadata['Enabled'],
                    'key_usage': key_metadata['KeyUsage'],
                    'rotation_enabled': False
                }
                
                # Check rotation status
                try:
                    rotation_response = client.get_key_rotation_status(KeyId=key_id)
                    region_health['rotation_enabled'] = rotation_response['KeyRotationEnabled']
                except:
                    pass
                
                # Determine health status
                if key_metadata['KeyState'] != 'Enabled' or not key_metadata['Enabled']:
                    region_health['status'] = 'unhealthy'
                    health_status['overall_health'] = 'degraded'
                    health_status['issues'].append(f"Key disabled or in invalid state in {region}")
                else:
                    region_health['status'] = 'healthy'
                
                health_status['region_status'][region] = region_health
                
            except Exception as e:
                health_status['region_status'][region] = {
                    'status': 'error',
                    'error': str(e)
                }
                health_status['overall_health'] = 'degraded'
                health_status['issues'].append(f"Cannot access key in {region}: {str(e)}")
        
        return health_status

# Example usage
if __name__ == "__main__":
    # Initialize multi-region key manager
    mr_manager = MultiRegionKeyManager()
    
    # Configure multi-region key
    config = MultiRegionKeyConfig(
        primary_region='us-east-1',
        replica_regions=['us-west-2', 'eu-west-1'],
        key_description='Multi-Region Application Key',
        policy_document={
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "Enable IAM User Permissions",
                    "Effect": "Allow",
                    "Principal": {"AWS": "arn:aws:iam::123456789012:root"},
                    "Action": "kms:*",
                    "Resource": "*"
                }
            ]
        },
        tags={
            'Environment': 'Production',
            'Application': 'GlobalApp',
            'DisasterRecovery': 'Enabled'
        }
    )
    
    # Create multi-region key
    result = mr_manager.create_multi_region_key(config)
    print(f"Multi-region key creation: {result}")
    
    # Test cross-region functionality
    if result['status'] == 'success':
        test_result = mr_manager.test_cross_region_encryption(
            result['primary_key']['key_id']
        )
        print(f"Cross-region test: {test_result}")
        
        # Monitor key health
        health_result = mr_manager.monitor_key_health(
            result['primary_key']['key_id']
        )
        print(f"Key health: {health_result}")
```

### Example 3: CloudFormation Template for Secure Key Infrastructure

```yaml
# secure-key-infrastructure.yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Secure KMS key infrastructure with comprehensive management'

Parameters:
  Environment:
    Type: String
    Default: 'prod'
    AllowedValues: ['dev', 'staging', 'prod']
  
  ApplicationName:
    Type: String
    Description: 'Name of the application using these keys'
  
  EnableMultiRegion:
    Type: String
    Default: 'false'
    AllowedValues: ['true', 'false']
    Description: 'Enable multi-region keys'

Conditions:
  IsProduction: !Equals [!Ref Environment, 'prod']
  EnableMR: !Equals [!Ref EnableMultiRegion, 'true']

Resources:
  # Application encryption key
  ApplicationEncryptionKey:
    Type: AWS::KMS::Key
    Properties:
      Description: !Sub '${ApplicationName} application encryption key'
      KeyUsage: ENCRYPT_DECRYPT
      KeySpec: SYMMETRIC_DEFAULT
      MultiRegion: !If [EnableMR, true, false]
      EnableKeyRotation: true
      KeyPolicy:
        Version: '2012-10-17'
        Statement:
          - Sid: Enable IAM User Permissions
            Effect: Allow
            Principal:
              AWS: !Sub 'arn:aws:iam::${AWS::AccountId}:root'
            Action: 'kms:*'
            Resource: '*'
          - Sid: Allow application role to use key
            Effect: Allow
            Principal:
              AWS: !GetAtt ApplicationRole.Arn
            Action:
              - 'kms:Encrypt'
              - 'kms:Decrypt'
              - 'kms:ReEncrypt*'
              - 'kms:GenerateDataKey*'
              - 'kms:DescribeKey'
            Resource: '*'
          - Sid: Allow application role to create grants
            Effect: Allow
            Principal:
              AWS: !GetAtt ApplicationRole.Arn
            Action:
              - 'kms:CreateGrant'
              - 'kms:ListGrants'
              - 'kms:RevokeGrant'
            Resource: '*'
            Condition:
              Bool:
                'kms:GrantIsForAWSResource': 'true'
      Tags:
        - Key: Environment
          Value: !Ref Environment
        - Key: Application
          Value: !Ref ApplicationName
        - Key: KeyType
          Value: Application
        - Key: RotationEnabled
          Value: 'true'

  ApplicationEncryptionKeyAlias:
    Type: AWS::KMS::Alias
    Properties:
      AliasName: !Sub 'alias/${ApplicationName}-${Environment}-app-key'
      TargetKeyId: !Ref ApplicationEncryptionKey

  # Database encryption key
  DatabaseEncryptionKey:
    Type: AWS::KMS::Key
    Properties:
      Description: !Sub '${ApplicationName} database encryption key'
      KeyUsage: ENCRYPT_DECRYPT
      KeySpec: SYMMETRIC_DEFAULT
      MultiRegion: !If [EnableMR, true, false]
      EnableKeyRotation: true
      KeyPolicy:
        Version: '2012-10-17'
        Statement:
          - Sid: Enable IAM User Permissions
            Effect: Allow
            Principal:
              AWS: !Sub 'arn:aws:iam::${AWS::AccountId}:root'
            Action: 'kms:*'
            Resource: '*'
          - Sid: Allow RDS service
            Effect: Allow
            Principal:
              Service: rds.amazonaws.com
            Action:
              - 'kms:Encrypt'
              - 'kms:Decrypt'
              - 'kms:ReEncrypt*'
              - 'kms:GenerateDataKey*'
              - 'kms:DescribeKey'
              - 'kms:CreateGrant'
            Resource: '*'
          - Sid: Allow database administrators
            Effect: Allow
            Principal:
              AWS: !GetAtt DatabaseAdminRole.Arn
            Action:
              - 'kms:Decrypt'
              - 'kms:DescribeKey'
            Resource: '*'
            Condition:
              StringEquals:
                'kms:ViaService': !Sub 'rds.${AWS::Region}.amazonaws.com'
      Tags:
        - Key: Environment
          Value: !Ref Environment
        - Key: Application
          Value: !Ref ApplicationName
        - Key: KeyType
          Value: Database
        - Key: RotationEnabled
          Value: 'true'

  DatabaseEncryptionKeyAlias:
    Type: AWS::KMS::Alias
    Properties:
      AliasName: !Sub 'alias/${ApplicationName}-${Environment}-db-key'
      TargetKeyId: !Ref DatabaseEncryptionKey

  # Backup encryption key
  BackupEncryptionKey:
    Type: AWS::KMS::Key
    Properties:
      Description: !Sub '${ApplicationName} backup encryption key'
      KeyUsage: ENCRYPT_DECRYPT
      KeySpec: SYMMETRIC_DEFAULT
      MultiRegion: !If [EnableMR, true, false]
      EnableKeyRotation: true
      KeyPolicy:
        Version: '2012-10-17'
        Statement:
          - Sid: Enable IAM User Permissions
            Effect: Allow
            Principal:
              AWS: !Sub 'arn:aws:iam::${AWS::AccountId}:root'
            Action: 'kms:*'
            Resource: '*'
          - Sid: Allow AWS Backup service
            Effect: Allow
            Principal:
              Service: backup.amazonaws.com
            Action:
              - 'kms:Encrypt'
              - 'kms:Decrypt'
              - 'kms:ReEncrypt*'
              - 'kms:GenerateDataKey*'
              - 'kms:DescribeKey'
              - 'kms:CreateGrant'
            Resource: '*'
          - Sid: Allow backup administrators
            Effect: Allow
            Principal:
              AWS: !GetAtt BackupAdminRole.Arn
            Action:
              - 'kms:Decrypt'
              - 'kms:DescribeKey'
              - 'kms:ListGrants'
            Resource: '*'
      Tags:
        - Key: Environment
          Value: !Ref Environment
        - Key: Application
          Value: !Ref ApplicationName
        - Key: KeyType
          Value: Backup
        - Key: RotationEnabled
          Value: 'true'

  BackupEncryptionKeyAlias:
    Type: AWS::KMS::Alias
    Properties:
      AliasName: !Sub 'alias/${ApplicationName}-${Environment}-backup-key'
      TargetKeyId: !Ref BackupEncryptionKey

  # IAM Roles
  ApplicationRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: !Sub '${ApplicationName}-${Environment}-application-role'
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: ec2.amazonaws.com
            Action: sts:AssumeRole
          - Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
      Tags:
        - Key: Environment
          Value: !Ref Environment
        - Key: Application
          Value: !Ref ApplicationName

  DatabaseAdminRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: !Sub '${ApplicationName}-${Environment}-db-admin-role'
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              AWS: !Sub 'arn:aws:iam::${AWS::AccountId}:root'
            Action: sts:AssumeRole
            Condition:
              Bool:
                'aws:MultiFactorAuthPresent': 'true'
      Policies:
        - PolicyName: DatabaseAdminPolicy
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - 'rds:*'
                Resource: '*'
      Tags:
        - Key: Environment
          Value: !Ref Environment
        - Key: Application
          Value: !Ref ApplicationName

  BackupAdminRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: !Sub '${ApplicationName}-${Environment}-backup-admin-role'
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              AWS: !Sub 'arn:aws:iam::${AWS::AccountId}:root'
            Action: sts:AssumeRole
            Condition:
              Bool:
                'aws:MultiFactorAuthPresent': 'true'
      Policies:
        - PolicyName: BackupAdminPolicy
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - 'backup:*'
                  - 's3:GetObject'
                  - 's3:ListBucket'
                Resource: '*'
      Tags:
        - Key: Environment
          Value: !Ref Environment
        - Key: Application
          Value: !Ref ApplicationName

  # CloudWatch Alarms for key monitoring
  KeyUsageAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: !Sub '${ApplicationName}-${Environment}-key-usage-alarm'
      AlarmDescription: 'Monitor unusual KMS key usage patterns'
      MetricName: NumberOfRequestsSucceeded
      Namespace: AWS/KMS
      Statistic: Sum
      Period: 300
      EvaluationPeriods: 2
      Threshold: 1000
      ComparisonOperator: GreaterThanThreshold
      Dimensions:
        - Name: KeyId
          Value: !Ref ApplicationEncryptionKey
      AlarmActions:
        - !Ref SecurityNotificationTopic

  # SNS Topic for security notifications
  SecurityNotificationTopic:
    Type: AWS::SNS::Topic
    Properties:
      TopicName: !Sub '${ApplicationName}-${Environment}-security-notifications'
      KmsMasterKeyId: !Ref ApplicationEncryptionKey
      Tags:
        - Key: Environment
          Value: !Ref Environment
        - Key: Application
          Value: !Ref ApplicationName

  # Lambda function for key rotation monitoring
  KeyRotationMonitor:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: !Sub '${ApplicationName}-${Environment}-key-rotation-monitor'
      Runtime: python3.9
      Handler: index.lambda_handler
      Role: !GetAtt KeyRotationMonitorRole.Arn
      Environment:
        Variables:
          APPLICATION_KEY_ID: !Ref ApplicationEncryptionKey
          DATABASE_KEY_ID: !Ref DatabaseEncryptionKey
          BACKUP_KEY_ID: !Ref BackupEncryptionKey
          SNS_TOPIC_ARN: !Ref SecurityNotificationTopic
      Code:
        ZipFile: |
          import boto3
          import json
          import os
          from datetime import datetime, timedelta
          
          def lambda_handler(event, context):
              kms = boto3.client('kms')
              sns = boto3.client('sns')
              
              key_ids = [
                  os.environ['APPLICATION_KEY_ID'],
                  os.environ['DATABASE_KEY_ID'],
                  os.environ['BACKUP_KEY_ID']
              ]
              
              alerts = []
              
              for key_id in key_ids:
                  try:
                      # Check rotation status
                      rotation_response = kms.get_key_rotation_status(KeyId=key_id)
                      
                      if not rotation_response['KeyRotationEnabled']:
                          alerts.append(f"Key rotation disabled for {key_id}")
                      
                      # Check key metadata
                      key_response = kms.describe_key(KeyId=key_id)
                      key_metadata = key_response['KeyMetadata']
                      
                      # Check key age
                      key_age = datetime.utcnow() - key_metadata['CreationDate'].replace(tzinfo=None)
                      if key_age.days > 365:
                          alerts.append(f"Key {key_id} is {key_age.days} days old")
                      
                  except Exception as e:
                      alerts.append(f"Error checking key {key_id}: {str(e)}")
              
              if alerts:
                  message = "KMS Key Rotation Alerts:\n" + "\n".join(alerts)
                  sns.publish(
                      TopicArn=os.environ['SNS_TOPIC_ARN'],
                      Message=message,
                      Subject="KMS Key Rotation Alert"
                  )
              
              return {
                  'statusCode': 200,
                  'body': json.dumps({
                      'alerts_count': len(alerts),
                      'alerts': alerts
                  })
              }
      Tags:
        - Key: Environment
          Value: !Ref Environment
        - Key: Application
          Value: !Ref ApplicationName

  KeyRotationMonitorRole:
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
        - PolicyName: KeyMonitoringPolicy
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - 'kms:DescribeKey'
                  - 'kms:GetKeyRotationStatus'
                  - 'sns:Publish'
                Resource: '*'

  # EventBridge rule for scheduled key monitoring
  KeyMonitoringSchedule:
    Type: AWS::Events::Rule
    Properties:
      Name: !Sub '${ApplicationName}-${Environment}-key-monitoring'
      ScheduleExpression: 'rate(1 day)'
      State: ENABLED
      Targets:
        - Arn: !GetAtt KeyRotationMonitor.Arn
          Id: KeyRotationMonitorTarget

  KeyMonitoringPermission:
    Type: AWS::Lambda::Permission
    Properties:
      FunctionName: !Ref KeyRotationMonitor
      Action: lambda:InvokeFunction
      Principal: events.amazonaws.com
      SourceArn: !GetAtt KeyMonitoringSchedule.Arn

Outputs:
  ApplicationKeyId:
    Description: 'Application encryption key ID'
    Value: !Ref ApplicationEncryptionKey
    Export:
      Name: !Sub '${AWS::StackName}-ApplicationKeyId'
  
  ApplicationKeyArn:
    Description: 'Application encryption key ARN'
    Value: !GetAtt ApplicationEncryptionKey.Arn
    Export:
      Name: !Sub '${AWS::StackName}-ApplicationKeyArn'
  
  DatabaseKeyId:
    Description: 'Database encryption key ID'
    Value: !Ref DatabaseEncryptionKey
    Export:
      Name: !Sub '${AWS::StackName}-DatabaseKeyId'
  
  BackupKeyId:
    Description: 'Backup encryption key ID'
    Value: !Ref BackupEncryptionKey
    Export:
      Name: !Sub '${AWS::StackName}-BackupKeyId'
  
  ApplicationRoleArn:
    Description: 'Application role ARN'
    Value: !GetAtt ApplicationRole.Arn
    Export:
      Name: !Sub '${AWS::StackName}-ApplicationRoleArn'
```

## Relevant AWS Services

### Core Key Management Services
- **AWS Key Management Service (KMS)**: Centralized key management with hardware security modules
- **AWS CloudHSM**: Dedicated hardware security modules for high-security requirements
- **AWS Certificate Manager**: SSL/TLS certificate management and automatic renewal
- **AWS Secrets Manager**: Secure storage and automatic rotation of secrets

### Integration Services
- **AWS IAM**: Identity and access management for key permissions
- **AWS CloudTrail**: Audit logging for all key management operations
- **AWS Config**: Configuration compliance monitoring for key policies
- **Amazon CloudWatch**: Monitoring and alerting for key usage patterns

### Application Integration
- **Amazon S3**: Server-side encryption with KMS keys
- **Amazon RDS**: Database encryption with customer managed keys
- **Amazon EBS**: Volume encryption with KMS integration
- **AWS Lambda**: Serverless functions with environment variable encryption

## Benefits of Secure Key Management

### Security Benefits
- **Centralized Control**: Single point of control for all encryption keys
- **Hardware Protection**: Keys protected by FIPS 140-2 Level 2 validated HSMs
- **Access Control**: Fine-grained permissions for key usage and management
- **Audit Trail**: Complete logging of all key operations

### Operational Benefits
- **Automated Rotation**: Automatic key rotation without application changes
- **Service Integration**: Native integration with AWS services
- **Multi-Region Support**: Global key availability for distributed applications
- **Disaster Recovery**: Built-in redundancy and backup capabilities

### Compliance Benefits
- **Regulatory Compliance**: Meet requirements for key management standards
- **Data Sovereignty**: Control over key location and access
- **Audit Readiness**: Comprehensive audit trails for compliance reporting
- **Policy Enforcement**: Automated enforcement of key usage policies

## Related Resources

- [AWS Well-Architected Framework - Data at Rest Protection](https://docs.aws.amazon.com/wellarchitected/latest/framework/sec-08.html)
- [AWS Key Management Service Developer Guide](https://docs.aws.amazon.com/kms/latest/developerguide/overview.html)
- [AWS KMS Best Practices](https://docs.aws.amazon.com/kms/latest/developerguide/best-practices.html)
- [AWS CloudHSM User Guide](https://docs.aws.amazon.com/cloudhsm/latest/userguide/introduction.html)
- [AWS Security Blog - Key Management](https://aws.amazon.com/blogs/security/tag/key-management/)
- [NIST Cryptographic Standards](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines)
```
```
