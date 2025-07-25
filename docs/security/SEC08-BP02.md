---
title: "SEC08-BP02: Enforce encryption at rest"
layout: default
parent: "SEC08 - How do you protect your data at rest?"
grand_parent: Security
nav_order: 2
---

# SEC08-BP02: Enforce encryption at rest

## Overview

Enforcing encryption at rest ensures that all stored data is protected from unauthorized access, even if physical storage media is compromised. This best practice focuses on implementing comprehensive encryption policies across all data storage services, using appropriate encryption methods, and ensuring consistent enforcement through automated controls.

Encryption at rest should be applied to all data stores including databases, file systems, object storage, backups, and logs. The implementation should be transparent to applications while providing strong cryptographic protection for sensitive data.

## Implementation Guidance

### 1. Implement Service-Level Encryption

Enable encryption at rest for all AWS storage services:

- **Amazon S3**: Server-side encryption with KMS, S3-managed keys, or customer-provided keys
- **Amazon RDS**: Database encryption with KMS keys for all database engines
- **Amazon EBS**: Volume encryption for all EC2 instance storage
- **Amazon DynamoDB**: Table encryption with KMS keys
- **Amazon Redshift**: Cluster encryption for data warehouse workloads
- **Amazon EFS**: File system encryption for shared storage

### 2. Use Strong Encryption Standards

Implement industry-standard encryption algorithms:

- **AES-256**: Advanced Encryption Standard with 256-bit keys
- **KMS Integration**: Use AWS KMS for key management and encryption
- **Hardware Security Modules**: Leverage HSM-backed encryption where required
- **Encryption in Transit**: Combine with encryption in transit for comprehensive protection

### 3. Automate Encryption Enforcement

Deploy automated controls to ensure encryption compliance:

- **Service Control Policies**: Prevent creation of unencrypted resources
- **AWS Config Rules**: Monitor and report on encryption compliance
- **CloudFormation Guards**: Validate encryption in infrastructure templates
- **Lambda Functions**: Automated remediation for non-compliant resources

### 4. Implement Granular Encryption Policies

Apply appropriate encryption based on data sensitivity:

- **Data Classification**: Use different encryption keys based on data classification
- **Field-Level Encryption**: Encrypt specific sensitive fields in databases
- **Client-Side Encryption**: Implement application-level encryption for highly sensitive data
- **Envelope Encryption**: Use data keys encrypted with master keys for performance

### 5. Monitor Encryption Compliance

Establish comprehensive monitoring for encryption status:

- **Compliance Dashboards**: Real-time visibility into encryption status
- **Automated Alerts**: Notifications for encryption policy violations
- **Audit Reports**: Regular compliance reporting for security reviews
- **Remediation Workflows**: Automated fixing of encryption gaps

### 6. Plan for Key Rotation and Recovery

Ensure encryption keys are properly managed:

- **Automatic Key Rotation**: Enable regular rotation of encryption keys
- **Backup Encryption**: Encrypt all backup data with appropriate keys
- **Disaster Recovery**: Ensure encrypted data can be recovered across regions
- **Key Archival**: Maintain access to historical encryption keys

## Implementation Examples

### Example 1: Comprehensive Encryption Enforcement System

```python
# encryption_enforcer.py
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
class EncryptionPolicy:
    service: str
    resource_type: str
    encryption_required: bool
    kms_key_required: bool
    compliance_frameworks: List[str]
    remediation_action: str

@dataclass
class EncryptionStatus:
    resource_arn: str
    service: str
    resource_type: str
    encrypted: bool
    encryption_key: Optional[str]
    compliance_status: str
    last_checked: str

class EncryptionEnforcer:
    """
    Comprehensive system for enforcing encryption at rest across AWS services
    """
    
    def __init__(self, region: str = 'us-east-1'):
        self.region = region
        self.s3_client = boto3.client('s3', region_name=region)
        self.rds_client = boto3.client('rds', region_name=region)
        self.ec2_client = boto3.client('ec2', region_name=region)
        self.dynamodb_client = boto3.client('dynamodb', region_name=region)
        self.kms_client = boto3.client('kms', region_name=region)
        self.config_client = boto3.client('config', region_name=region)
        self.lambda_client = boto3.client('lambda', region_name=region)
        self.sns_client = boto3.client('sns', region_name=region)
        self.dynamodb = boto3.resource('dynamodb', region_name=region)
        
        # Encryption compliance tracking
        self.compliance_table = self.dynamodb.Table('encryption-compliance-tracking')
        
        # Encryption policies by service
        self.encryption_policies = self._define_encryption_policies()
    
    def _define_encryption_policies(self) -> Dict[str, EncryptionPolicy]:
        """
        Define encryption policies for different AWS services
        """
        return {
            's3_bucket': EncryptionPolicy(
                service='s3',
                resource_type='bucket',
                encryption_required=True,
                kms_key_required=True,
                compliance_frameworks=['GDPR', 'HIPAA', 'PCI_DSS'],
                remediation_action='enable_s3_encryption'
            ),
            'rds_instance': EncryptionPolicy(
                service='rds',
                resource_type='db_instance',
                encryption_required=True,
                kms_key_required=True,
                compliance_frameworks=['HIPAA', 'PCI_DSS', 'SOX'],
                remediation_action='create_encrypted_snapshot'
            ),
            'ebs_volume': EncryptionPolicy(
                service='ec2',
                resource_type='volume',
                encryption_required=True,
                kms_key_required=False,
                compliance_frameworks=['GDPR', 'HIPAA'],
                remediation_action='create_encrypted_volume'
            ),
            'dynamodb_table': EncryptionPolicy(
                service='dynamodb',
                resource_type='table',
                encryption_required=True,
                kms_key_required=True,
                compliance_frameworks=['GDPR', 'HIPAA', 'PCI_DSS'],
                remediation_action='enable_dynamodb_encryption'
            ),
            'lambda_function': EncryptionPolicy(
                service='lambda',
                resource_type='function',
                encryption_required=True,
                kms_key_required=False,
                compliance_frameworks=['GDPR', 'HIPAA'],
                remediation_action='enable_lambda_encryption'
            )
        }
    
    def scan_encryption_compliance(self) -> Dict[str, Any]:
        """
        Scan all resources for encryption compliance
        """
        compliance_results = {
            'scan_timestamp': datetime.utcnow().isoformat(),
            'total_resources': 0,
            'compliant_resources': 0,
            'non_compliant_resources': 0,
            'services_scanned': [],
            'compliance_by_service': {},
            'non_compliant_details': []
        }
        
        # Scan S3 buckets
        s3_results = self._scan_s3_encryption()
        compliance_results['services_scanned'].append('s3')
        compliance_results['compliance_by_service']['s3'] = s3_results
        compliance_results['total_resources'] += s3_results['total']
        compliance_results['compliant_resources'] += s3_results['compliant']
        compliance_results['non_compliant_resources'] += s3_results['non_compliant']
        compliance_results['non_compliant_details'].extend(s3_results['non_compliant_details'])
        
        # Scan RDS instances
        rds_results = self._scan_rds_encryption()
        compliance_results['services_scanned'].append('rds')
        compliance_results['compliance_by_service']['rds'] = rds_results
        compliance_results['total_resources'] += rds_results['total']
        compliance_results['compliant_resources'] += rds_results['compliant']
        compliance_results['non_compliant_resources'] += rds_results['non_compliant']
        compliance_results['non_compliant_details'].extend(rds_results['non_compliant_details'])
        
        # Scan EBS volumes
        ebs_results = self._scan_ebs_encryption()
        compliance_results['services_scanned'].append('ebs')
        compliance_results['compliance_by_service']['ebs'] = ebs_results
        compliance_results['total_resources'] += ebs_results['total']
        compliance_results['compliant_resources'] += ebs_results['compliant']
        compliance_results['non_compliant_resources'] += ebs_results['non_compliant']
        compliance_results['non_compliant_details'].extend(ebs_results['non_compliant_details'])
        
        # Scan DynamoDB tables
        dynamodb_results = self._scan_dynamodb_encryption()
        compliance_results['services_scanned'].append('dynamodb')
        compliance_results['compliance_by_service']['dynamodb'] = dynamodb_results
        compliance_results['total_resources'] += dynamodb_results['total']
        compliance_results['compliant_resources'] += dynamodb_results['compliant']
        compliance_results['non_compliant_resources'] += dynamodb_results['non_compliant']
        compliance_results['non_compliant_details'].extend(dynamodb_results['non_compliant_details'])
        
        # Calculate compliance percentage
        if compliance_results['total_resources'] > 0:
            compliance_results['compliance_percentage'] = round(
                (compliance_results['compliant_resources'] / compliance_results['total_resources']) * 100, 2
            )
        else:
            compliance_results['compliance_percentage'] = 100.0
        
        # Store compliance results
        self._store_compliance_results(compliance_results)
        
        return compliance_results
    
    def _scan_s3_encryption(self) -> Dict[str, Any]:
        """
        Scan S3 buckets for encryption compliance
        """
        results = {
            'total': 0,
            'compliant': 0,
            'non_compliant': 0,
            'non_compliant_details': []
        }
        
        try:
            # List all S3 buckets
            buckets_response = self.s3_client.list_buckets()
            
            for bucket in buckets_response['Buckets']:
                bucket_name = bucket['Name']
                results['total'] += 1
                
                try:
                    # Check bucket encryption
                    encryption_response = self.s3_client.get_bucket_encryption(Bucket=bucket_name)
                    encryption_config = encryption_response['ServerSideEncryptionConfiguration']
                    
                    # Check if KMS encryption is used
                    has_kms_encryption = False
                    for rule in encryption_config['Rules']:
                        sse_config = rule['ApplyServerSideEncryptionByDefault']
                        if sse_config['SSEAlgorithm'] == 'aws:kms':
                            has_kms_encryption = True
                            break
                    
                    if has_kms_encryption:
                        results['compliant'] += 1
                        self._track_encryption_status(
                            f'arn:aws:s3:::{bucket_name}',
                            's3',
                            'bucket',
                            True,
                            'compliant'
                        )
                    else:
                        results['non_compliant'] += 1
                        results['non_compliant_details'].append({
                            'resource_arn': f'arn:aws:s3:::{bucket_name}',
                            'service': 's3',
                            'issue': 'Bucket not encrypted with KMS',
                            'remediation': 'Enable KMS encryption'
                        })
                        self._track_encryption_status(
                            f'arn:aws:s3:::{bucket_name}',
                            's3',
                            'bucket',
                            False,
                            'non_compliant'
                        )
                
                except self.s3_client.exceptions.NoSuchBucket:
                    continue
                except Exception as e:
                    if 'ServerSideEncryptionConfigurationNotFoundError' in str(e):
                        results['non_compliant'] += 1
                        results['non_compliant_details'].append({
                            'resource_arn': f'arn:aws:s3:::{bucket_name}',
                            'service': 's3',
                            'issue': 'No encryption configured',
                            'remediation': 'Enable S3 encryption'
                        })
                        self._track_encryption_status(
                            f'arn:aws:s3:::{bucket_name}',
                            's3',
                            'bucket',
                            False,
                            'non_compliant'
                        )
                    else:
                        logger.error(f"Error checking S3 bucket {bucket_name}: {str(e)}")
        
        except Exception as e:
            logger.error(f"Error scanning S3 encryption: {str(e)}")
        
        return results
    
    def _scan_rds_encryption(self) -> Dict[str, Any]:
        """
        Scan RDS instances for encryption compliance
        """
        results = {
            'total': 0,
            'compliant': 0,
            'non_compliant': 0,
            'non_compliant_details': []
        }
        
        try:
            # Scan RDS instances
            instances_response = self.rds_client.describe_db_instances()
            
            for instance in instances_response['DBInstances']:
                instance_id = instance['DBInstanceIdentifier']
                instance_arn = instance['DBInstanceArn']
                results['total'] += 1
                
                if instance.get('StorageEncrypted', False):
                    results['compliant'] += 1
                    self._track_encryption_status(
                        instance_arn,
                        'rds',
                        'db_instance',
                        True,
                        'compliant'
                    )
                else:
                    results['non_compliant'] += 1
                    results['non_compliant_details'].append({
                        'resource_arn': instance_arn,
                        'service': 'rds',
                        'issue': 'Database not encrypted',
                        'remediation': 'Create encrypted snapshot and restore'
                    })
                    self._track_encryption_status(
                        instance_arn,
                        'rds',
                        'db_instance',
                        False,
                        'non_compliant'
                    )
            
            # Scan RDS clusters
            clusters_response = self.rds_client.describe_db_clusters()
            
            for cluster in clusters_response['DBClusters']:
                cluster_id = cluster['DBClusterIdentifier']
                cluster_arn = cluster['DBClusterArn']
                results['total'] += 1
                
                if cluster.get('StorageEncrypted', False):
                    results['compliant'] += 1
                    self._track_encryption_status(
                        cluster_arn,
                        'rds',
                        'db_cluster',
                        True,
                        'compliant'
                    )
                else:
                    results['non_compliant'] += 1
                    results['non_compliant_details'].append({
                        'resource_arn': cluster_arn,
                        'service': 'rds',
                        'issue': 'Cluster not encrypted',
                        'remediation': 'Create encrypted cluster snapshot and restore'
                    })
                    self._track_encryption_status(
                        cluster_arn,
                        'rds',
                        'db_cluster',
                        False,
                        'non_compliant'
                    )
        
        except Exception as e:
            logger.error(f"Error scanning RDS encryption: {str(e)}")
        
        return results
    
    def _scan_ebs_encryption(self) -> Dict[str, Any]:
        """
        Scan EBS volumes for encryption compliance
        """
        results = {
            'total': 0,
            'compliant': 0,
            'non_compliant': 0,
            'non_compliant_details': []
        }
        
        try:
            # List all EBS volumes
            volumes_response = self.ec2_client.describe_volumes()
            
            for volume in volumes_response['Volumes']:
                volume_id = volume['VolumeId']
                volume_arn = f"arn:aws:ec2:{self.region}:{self._get_account_id()}:volume/{volume_id}"
                results['total'] += 1
                
                if volume.get('Encrypted', False):
                    results['compliant'] += 1
                    self._track_encryption_status(
                        volume_arn,
                        'ec2',
                        'volume',
                        True,
                        'compliant'
                    )
                else:
                    results['non_compliant'] += 1
                    results['non_compliant_details'].append({
                        'resource_arn': volume_arn,
                        'service': 'ec2',
                        'issue': 'EBS volume not encrypted',
                        'remediation': 'Create encrypted snapshot and new volume'
                    })
                    self._track_encryption_status(
                        volume_arn,
                        'ec2',
                        'volume',
                        False,
                        'non_compliant'
                    )
        
        except Exception as e:
            logger.error(f"Error scanning EBS encryption: {str(e)}")
        
        return results
    
    def _scan_dynamodb_encryption(self) -> Dict[str, Any]:
        """
        Scan DynamoDB tables for encryption compliance
        """
        results = {
            'total': 0,
            'compliant': 0,
            'non_compliant': 0,
            'non_compliant_details': []
        }
        
        try:
            # List all DynamoDB tables
            tables_response = self.dynamodb_client.list_tables()
            
            for table_name in tables_response['TableNames']:
                results['total'] += 1
                
                # Get table description
                table_response = self.dynamodb_client.describe_table(TableName=table_name)
                table_arn = table_response['Table']['TableArn']
                
                # Check encryption status
                sse_description = table_response['Table'].get('SSEDescription', {})
                sse_status = sse_description.get('Status', 'DISABLED')
                
                if sse_status == 'ENABLED':
                    results['compliant'] += 1
                    self._track_encryption_status(
                        table_arn,
                        'dynamodb',
                        'table',
                        True,
                        'compliant'
                    )
                else:
                    results['non_compliant'] += 1
                    results['non_compliant_details'].append({
                        'resource_arn': table_arn,
                        'service': 'dynamodb',
                        'issue': 'Table encryption not enabled',
                        'remediation': 'Enable server-side encryption'
                    })
                    self._track_encryption_status(
                        table_arn,
                        'dynamodb',
                        'table',
                        False,
                        'non_compliant'
                    )
        
        except Exception as e:
            logger.error(f"Error scanning DynamoDB encryption: {str(e)}")
        
        return results
    
    def remediate_encryption_violations(self, resource_arns: List[str]) -> Dict[str, Any]:
        """
        Automatically remediate encryption violations
        """
        remediation_results = {
            'total_resources': len(resource_arns),
            'successful_remediations': 0,
            'failed_remediations': 0,
            'results': []
        }
        
        for resource_arn in resource_arns:
            try:
                # Determine service and resource type from ARN
                service = resource_arn.split(':')[2]
                
                if service == 's3':
                    result = self._remediate_s3_encryption(resource_arn)
                elif service == 'rds':
                    result = self._remediate_rds_encryption(resource_arn)
                elif service == 'ec2':
                    result = self._remediate_ebs_encryption(resource_arn)
                elif service == 'dynamodb':
                    result = self._remediate_dynamodb_encryption(resource_arn)
                else:
                    result = {
                        'resource_arn': resource_arn,
                        'status': 'unsupported',
                        'message': f'Remediation not supported for service: {service}'
                    }
                
                remediation_results['results'].append(result)
                
                if result['status'] == 'success':
                    remediation_results['successful_remediations'] += 1
                else:
                    remediation_results['failed_remediations'] += 1
                    
            except Exception as e:
                remediation_results['results'].append({
                    'resource_arn': resource_arn,
                    'status': 'error',
                    'message': str(e)
                })
                remediation_results['failed_remediations'] += 1
        
        return remediation_results
    
    def _remediate_s3_encryption(self, bucket_arn: str) -> Dict[str, Any]:
        """
        Enable S3 bucket encryption
        """
        try:
            bucket_name = bucket_arn.split(':')[-1]
            
            # Get default KMS key for S3
            default_key_id = f'alias/aws/s3'
            
            # Enable server-side encryption
            self.s3_client.put_bucket_encryption(
                Bucket=bucket_name,
                ServerSideEncryptionConfiguration={
                    'Rules': [
                        {
                            'ApplyServerSideEncryptionByDefault': {
                                'SSEAlgorithm': 'aws:kms',
                                'KMSMasterKeyID': default_key_id
                            },
                            'BucketKeyEnabled': True
                        }
                    ]
                }
            )
            
            logger.info(f"Enabled encryption for S3 bucket: {bucket_name}")
            
            return {
                'resource_arn': bucket_arn,
                'status': 'success',
                'message': 'S3 encryption enabled successfully'
            }
            
        except Exception as e:
            logger.error(f"Error remediating S3 encryption for {bucket_arn}: {str(e)}")
            return {
                'resource_arn': bucket_arn,
                'status': 'error',
                'message': str(e)
            }
    
    def _remediate_dynamodb_encryption(self, table_arn: str) -> Dict[str, Any]:
        """
        Enable DynamoDB table encryption
        """
        try:
            table_name = table_arn.split('/')[-1]
            
            # Enable server-side encryption
            self.dynamodb_client.update_table(
                TableName=table_name,
                SSESpecification={
                    'Enabled': True,
                    'SSEType': 'KMS'
                }
            )
            
            logger.info(f"Enabled encryption for DynamoDB table: {table_name}")
            
            return {
                'resource_arn': table_arn,
                'status': 'success',
                'message': 'DynamoDB encryption enabled successfully'
            }
            
        except Exception as e:
            logger.error(f"Error remediating DynamoDB encryption for {table_arn}: {str(e)}")
            return {
                'resource_arn': table_arn,
                'status': 'error',
                'message': str(e)
            }
    
    def _remediate_rds_encryption(self, instance_arn: str) -> Dict[str, Any]:
        """
        Note: RDS encryption cannot be enabled on existing instances
        This would require creating an encrypted snapshot and restoring
        """
        return {
            'resource_arn': instance_arn,
            'status': 'manual_action_required',
            'message': 'RDS encryption requires manual snapshot and restore process'
        }
    
    def _remediate_ebs_encryption(self, volume_arn: str) -> Dict[str, Any]:
        """
        Note: EBS encryption cannot be enabled on existing volumes
        This would require creating an encrypted snapshot and new volume
        """
        return {
            'resource_arn': volume_arn,
            'status': 'manual_action_required',
            'message': 'EBS encryption requires manual snapshot and new volume creation'
        }
    
    def _track_encryption_status(self, resource_arn: str, service: str, resource_type: str, encrypted: bool, compliance_status: str):
        """
        Track encryption status in DynamoDB
        """
        try:
            self.compliance_table.put_item(
                Item={
                    'resource_arn': resource_arn,
                    'service': service,
                    'resource_type': resource_type,
                    'encrypted': encrypted,
                    'compliance_status': compliance_status,
                    'last_checked': datetime.utcnow().isoformat(),
                    'ttl': int((datetime.utcnow() + timedelta(days=90)).timestamp())
                }
            )
        except Exception as e:
            logger.error(f"Error tracking encryption status: {str(e)}")
    
    def _store_compliance_results(self, results: Dict[str, Any]):
        """
        Store compliance scan results
        """
        try:
            self.compliance_table.put_item(
                Item={
                    'resource_arn': 'COMPLIANCE_SCAN_SUMMARY',
                    'scan_timestamp': results['scan_timestamp'],
                    'compliance_percentage': results['compliance_percentage'],
                    'total_resources': results['total_resources'],
                    'compliant_resources': results['compliant_resources'],
                    'non_compliant_resources': results['non_compliant_resources'],
                    'services_scanned': results['services_scanned'],
                    'ttl': int((datetime.utcnow() + timedelta(days=365)).timestamp())
                }
            )
        except Exception as e:
            logger.error(f"Error storing compliance results: {str(e)}")
    
    def _get_account_id(self) -> str:
        """Get AWS account ID"""
        return boto3.client('sts').get_caller_identity()['Account']

# Example usage
if __name__ == "__main__":
    # Initialize encryption enforcer
    enforcer = EncryptionEnforcer()
    
    # Scan for encryption compliance
    compliance_results = enforcer.scan_encryption_compliance()
    print(f"Compliance scan results: {json.dumps(compliance_results, indent=2)}")
    
    # Remediate non-compliant resources
    if compliance_results['non_compliant_resources'] > 0:
        non_compliant_arns = [
            detail['resource_arn'] 
            for detail in compliance_results['non_compliant_details']
            if detail['service'] in ['s3', 'dynamodb']  # Only auto-remediable services
        ]
        
        if non_compliant_arns:
            remediation_results = enforcer.remediate_encryption_violations(non_compliant_arns)
            print(f"Remediation results: {json.dumps(remediation_results, indent=2)}")
```

### Example 2: Service Control Policies for Encryption Enforcement

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyUnencryptedS3Objects",
      "Effect": "Deny",
      "Action": "s3:PutObject",
      "Resource": "*",
      "Condition": {
        "StringNotEquals": {
          "s3:x-amz-server-side-encryption": [
            "aws:kms",
            "AES256"
          ]
        }
      }
    },
    {
      "Sid": "DenyUnencryptedS3Buckets",
      "Effect": "Deny",
      "Action": [
        "s3:CreateBucket"
      ],
      "Resource": "*",
      "Condition": {
        "Bool": {
          "s3:x-amz-bucket-server-side-encryption-enabled": "false"
        }
      }
    },
    {
      "Sid": "DenyUnencryptedRDSInstances",
      "Effect": "Deny",
      "Action": [
        "rds:CreateDBInstance",
        "rds:CreateDBCluster"
      ],
      "Resource": "*",
      "Condition": {
        "Bool": {
          "rds:StorageEncrypted": "false"
        }
      }
    },
    {
      "Sid": "DenyUnencryptedEBSVolumes",
      "Effect": "Deny",
      "Action": [
        "ec2:CreateVolume",
        "ec2:RunInstances"
      ],
      "Resource": [
        "arn:aws:ec2:*:*:volume/*",
        "arn:aws:ec2:*:*:instance/*"
      ],
      "Condition": {
        "Bool": {
          "ec2:Encrypted": "false"
        }
      }
    },
    {
      "Sid": "DenyUnencryptedDynamoDBTables",
      "Effect": "Deny",
      "Action": [
        "dynamodb:CreateTable"
      ],
      "Resource": "*",
      "Condition": {
        "ForAllValues:StringNotEquals": {
          "dynamodb:EncryptionEnabled": "true"
        }
      }
    },
    {
      "Sid": "DenyUnencryptedLambdaFunctions",
      "Effect": "Deny",
      "Action": [
        "lambda:CreateFunction"
      ],
      "Resource": "*",
      "Condition": {
        "Null": {
          "lambda:KMSKeyArn": "true"
        }
      }
    },
    {
      "Sid": "DenyUnencryptedEFSFileSystems",
      "Effect": "Deny",
      "Action": [
        "elasticfilesystem:CreateFileSystem"
      ],
      "Resource": "*",
      "Condition": {
        "Bool": {
          "elasticfilesystem:Encrypted": "false"
        }
      }
    },
    {
      "Sid": "DenyUnencryptedRedshiftClusters",
      "Effect": "Deny",
      "Action": [
        "redshift:CreateCluster"
      ],
      "Resource": "*",
      "Condition": {
        "Bool": {
          "redshift:Encrypted": "false"
        }
      }
    },
    {
      "Sid": "DenyUnencryptedSNSTopics",
      "Effect": "Deny",
      "Action": [
        "sns:CreateTopic"
      ],
      "Resource": "*",
      "Condition": {
        "Null": {
          "sns:KmsMasterKeyId": "true"
        }
      }
    },
    {
      "Sid": "DenyUnencryptedSQSQueues",
      "Effect": "Deny",
      "Action": [
        "sqs:CreateQueue"
      ],
      "Resource": "*",
      "Condition": {
        "Null": {
          "sqs:KmsMasterKeyId": "true"
        }
      }
    }
  ]
}
```

### Example 3: AWS Config Rules for Encryption Monitoring

```python
# config_encryption_rules.py
import boto3
import json
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

class ConfigEncryptionRules:
    """
    Deploy and manage AWS Config rules for encryption monitoring
    """
    
    def __init__(self, region: str = 'us-east-1'):
        self.region = region
        self.config_client = boto3.client('config', region_name=region)
        self.lambda_client = boto3.client('lambda', region_name=region)
        
        # Define encryption config rules
        self.encryption_rules = self._define_encryption_rules()
    
    def _define_encryption_rules(self) -> List[Dict[str, Any]]:
        """
        Define AWS Config rules for encryption compliance
        """
        return [
            {
                'ConfigRuleName': 's3-bucket-server-side-encryption-enabled',
                'Description': 'Checks that S3 buckets have server-side encryption enabled',
                'Source': {
                    'Owner': 'AWS',
                    'SourceIdentifier': 'S3_BUCKET_SERVER_SIDE_ENCRYPTION_ENABLED'
                },
                'Scope': {
                    'ComplianceResourceTypes': ['AWS::S3::Bucket']
                }
            },
            {
                'ConfigRuleName': 'rds-storage-encrypted',
                'Description': 'Checks that RDS instances have storage encryption enabled',
                'Source': {
                    'Owner': 'AWS',
                    'SourceIdentifier': 'RDS_STORAGE_ENCRYPTED'
                },
                'Scope': {
                    'ComplianceResourceTypes': ['AWS::RDS::DBInstance']
                }
            },
            {
                'ConfigRuleName': 'encrypted-volumes',
                'Description': 'Checks that EBS volumes are encrypted',
                'Source': {
                    'Owner': 'AWS',
                    'SourceIdentifier': 'ENCRYPTED_VOLUMES'
                },
                'Scope': {
                    'ComplianceResourceTypes': ['AWS::EC2::Volume']
                }
            },
            {
                'ConfigRuleName': 'dynamodb-table-encryption-enabled',
                'Description': 'Checks that DynamoDB tables have encryption enabled',
                'Source': {
                    'Owner': 'AWS',
                    'SourceIdentifier': 'DYNAMODB_TABLE_ENCRYPTION_ENABLED'
                },
                'Scope': {
                    'ComplianceResourceTypes': ['AWS::DynamoDB::Table']
                }
            },
            {
                'ConfigRuleName': 'lambda-function-settings-check',
                'Description': 'Checks Lambda function encryption settings',
                'Source': {
                    'Owner': 'AWS',
                    'SourceIdentifier': 'LAMBDA_FUNCTION_SETTINGS_CHECK'
                },
                'InputParameters': json.dumps({
                    'kmsKeyArn': 'REQUIRED'
                }),
                'Scope': {
                    'ComplianceResourceTypes': ['AWS::Lambda::Function']
                }
            },
            {
                'ConfigRuleName': 'efs-encrypted-check',
                'Description': 'Checks that EFS file systems are encrypted',
                'Source': {
                    'Owner': 'AWS',
                    'SourceIdentifier': 'EFS_ENCRYPTED_CHECK'
                },
                'Scope': {
                    'ComplianceResourceTypes': ['AWS::EFS::FileSystem']
                }
            },
            {
                'ConfigRuleName': 'redshift-cluster-configuration-check',
                'Description': 'Checks Redshift cluster encryption configuration',
                'Source': {
                    'Owner': 'AWS',
                    'SourceIdentifier': 'REDSHIFT_CLUSTER_CONFIGURATION_CHECK'
                },
                'InputParameters': json.dumps({
                    'clusterDbEncrypted': 'true',
                    'loggingEnabled': 'true'
                }),
                'Scope': {
                    'ComplianceResourceTypes': ['AWS::Redshift::Cluster']
                }
            }
        ]
    
    def deploy_encryption_rules(self) -> Dict[str, Any]:
        """
        Deploy all encryption monitoring Config rules
        """
        deployment_results = {
            'total_rules': len(self.encryption_rules),
            'successful_deployments': 0,
            'failed_deployments': 0,
            'results': []
        }
        
        for rule_config in self.encryption_rules:
            try:
                # Check if rule already exists
                try:
                    self.config_client.describe_config_rules(
                        ConfigRuleNames=[rule_config['ConfigRuleName']]
                    )
                    # Rule exists, update it
                    self.config_client.put_config_rule(ConfigRule=rule_config)
                    status = 'updated'
                except self.config_client.exceptions.NoSuchConfigRuleException:
                    # Rule doesn't exist, create it
                    self.config_client.put_config_rule(ConfigRule=rule_config)
                    status = 'created'
                
                deployment_results['successful_deployments'] += 1
                deployment_results['results'].append({
                    'rule_name': rule_config['ConfigRuleName'],
                    'status': status,
                    'message': f'Rule {status} successfully'
                })
                
                logger.info(f"Config rule {rule_config['ConfigRuleName']} {status} successfully")
                
            except Exception as e:
                deployment_results['failed_deployments'] += 1
                deployment_results['results'].append({
                    'rule_name': rule_config['ConfigRuleName'],
                    'status': 'failed',
                    'message': str(e)
                })
                logger.error(f"Failed to deploy Config rule {rule_config['ConfigRuleName']}: {str(e)}")
        
        return deployment_results
    
    def get_compliance_summary(self) -> Dict[str, Any]:
        """
        Get compliance summary for all encryption rules
        """
        compliance_summary = {
            'timestamp': boto3.client('sts').get_caller_identity(),
            'rules_evaluated': 0,
            'compliant_resources': 0,
            'non_compliant_resources': 0,
            'rule_details': []
        }
        
        for rule_config in self.encryption_rules:
            rule_name = rule_config['ConfigRuleName']
            
            try:
                # Get compliance details for this rule
                compliance_response = self.config_client.get_compliance_details_by_config_rule(
                    ConfigRuleName=rule_name
                )
                
                rule_compliance = {
                    'rule_name': rule_name,
                    'compliant_count': 0,
                    'non_compliant_count': 0,
                    'not_applicable_count': 0,
                    'insufficient_data_count': 0
                }
                
                for result in compliance_response['EvaluationResults']:
                    compliance_type = result['ComplianceType']
                    
                    if compliance_type == 'COMPLIANT':
                        rule_compliance['compliant_count'] += 1
                        compliance_summary['compliant_resources'] += 1
                    elif compliance_type == 'NON_COMPLIANT':
                        rule_compliance['non_compliant_count'] += 1
                        compliance_summary['non_compliant_resources'] += 1
                    elif compliance_type == 'NOT_APPLICABLE':
                        rule_compliance['not_applicable_count'] += 1
                    elif compliance_type == 'INSUFFICIENT_DATA':
                        rule_compliance['insufficient_data_count'] += 1
                
                compliance_summary['rule_details'].append(rule_compliance)
                compliance_summary['rules_evaluated'] += 1
                
            except Exception as e:
                logger.error(f"Error getting compliance for rule {rule_name}: {str(e)}")
                compliance_summary['rule_details'].append({
                    'rule_name': rule_name,
                    'error': str(e)
                })
        
        # Calculate overall compliance percentage
        total_evaluated = compliance_summary['compliant_resources'] + compliance_summary['non_compliant_resources']
        if total_evaluated > 0:
            compliance_summary['compliance_percentage'] = round(
                (compliance_summary['compliant_resources'] / total_evaluated) * 100, 2
            )
        else:
            compliance_summary['compliance_percentage'] = 0.0
        
        return compliance_summary
    
    def create_remediation_configuration(self, rule_name: str, remediation_lambda_arn: str) -> Dict[str, Any]:
        """
        Create remediation configuration for a Config rule
        """
        try:
            remediation_config = {
                'ConfigRuleName': rule_name,
                'TargetType': 'SSM_DOCUMENT',
                'TargetId': 'AWSConfigRemediation-RemoveUnrestrictedSourceInSecurityGroup',
                'TargetVersion': '1',
                'Parameters': {
                    'AutomationAssumeRole': {
                        'StaticValue': {
                            'Values': [remediation_lambda_arn]
                        }
                    }
                },
                'Automatic': True,
                'ExecutionControls': {
                    'SsmControls': {
                        'ConcurrentExecutionRatePercentage': 10,
                        'ErrorPercentage': 10
                    }
                }
            }
            
            self.config_client.put_remediation_configurations(
                RemediationConfigurations=[remediation_config]
            )
            
            return {
                'status': 'success',
                'rule_name': rule_name,
                'message': 'Remediation configuration created successfully'
            }
            
        except Exception as e:
            logger.error(f"Error creating remediation configuration for {rule_name}: {str(e)}")
            return {
                'status': 'error',
                'rule_name': rule_name,
                'message': str(e)
            }

# Example usage
if __name__ == "__main__":
    # Initialize Config rules manager
    config_rules = ConfigEncryptionRules()
    
    # Deploy encryption monitoring rules
    deployment_results = config_rules.deploy_encryption_rules()
    print(f"Config rules deployment: {json.dumps(deployment_results, indent=2)}")
    
    # Get compliance summary
    compliance_summary = config_rules.get_compliance_summary()
    print(f"Compliance summary: {json.dumps(compliance_summary, indent=2)}")
```

### Example 4: CloudFormation Template for Encryption-by-Default

```yaml
# encryption-by-default.yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Enforce encryption at rest across AWS services'

Parameters:
  Environment:
    Type: String
    Default: 'prod'
    AllowedValues: ['dev', 'staging', 'prod']
  
  KMSKeyArn:
    Type: String
    Description: 'ARN of the KMS key to use for encryption'

Resources:
  # S3 Bucket with enforced encryption
  EncryptedS3Bucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub 'encrypted-data-${Environment}-${AWS::AccountId}'
      BucketEncryption:
        ServerSideEncryptionConfiguration:
          - ServerSideEncryptionByDefault:
              SSEAlgorithm: aws:kms
              KMSMasterKeyID: !Ref KMSKeyArn
            BucketKeyEnabled: true
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true
      NotificationConfiguration:
        CloudWatchConfigurations:
          - Event: 's3:ObjectCreated:*'
            CloudWatchConfiguration:
              LogGroupName: !Ref S3AccessLogGroup
      Tags:
        - Key: Environment
          Value: !Ref Environment
        - Key: EncryptionEnforced
          Value: 'true'

  # S3 Bucket Policy to enforce encryption
  S3BucketPolicy:
    Type: AWS::S3::BucketPolicy
    Properties:
      Bucket: !Ref EncryptedS3Bucket
      PolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Sid: DenyUnencryptedObjectUploads
            Effect: Deny
            Principal: '*'
            Action: 's3:PutObject'
            Resource: !Sub '${EncryptedS3Bucket}/*'
            Condition:
              StringNotEquals:
                's3:x-amz-server-side-encryption': 'aws:kms'
          - Sid: DenyInsecureConnections
            Effect: Deny
            Principal: '*'
            Action: 's3:*'
            Resource:
              - !GetAtt EncryptedS3Bucket.Arn
              - !Sub '${EncryptedS3Bucket}/*'
            Condition:
              Bool:
                'aws:SecureTransport': 'false'

  # RDS Instance with encryption
  EncryptedRDSInstance:
    Type: AWS::RDS::DBInstance
    Properties:
      DBInstanceIdentifier: !Sub 'encrypted-db-${Environment}'
      DBInstanceClass: db.t3.micro
      Engine: mysql
      EngineVersion: '8.0'
      MasterUsername: admin
      MasterUserPassword: !Ref DBPassword
      AllocatedStorage: 20
      StorageType: gp2
      StorageEncrypted: true
      KmsKeyId: !Ref KMSKeyArn
      BackupRetentionPeriod: 7
      DeletionProtection: true
      EnablePerformanceInsights: true
      PerformanceInsightsKMSKeyId: !Ref KMSKeyArn
      Tags:
        - Key: Environment
          Value: !Ref Environment
        - Key: EncryptionEnforced
          Value: 'true'

  DBPassword:
    Type: AWS::SecretsManager::Secret
    Properties:
      Name: !Sub 'rds-password-${Environment}'
      Description: 'RDS instance password'
      GenerateSecretString:
        SecretStringTemplate: '{"username": "admin"}'
        GenerateStringKey: 'password'
        PasswordLength: 32
        ExcludeCharacters: '"@/\'
      KmsKeyId: !Ref KMSKeyArn

  # DynamoDB Table with encryption
  EncryptedDynamoDBTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: !Sub 'encrypted-table-${Environment}'
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: id
          AttributeType: S
      KeySchema:
        - AttributeName: id
          KeyType: HASH
      SSESpecification:
        SSEEnabled: true
        KMSMasterKeyId: !Ref KMSKeyArn
      PointInTimeRecoverySpecification:
        PointInTimeRecoveryEnabled: true
      Tags:
        - Key: Environment
          Value: !Ref Environment
        - Key: EncryptionEnforced
          Value: 'true'

  # EFS File System with encryption
  EncryptedEFSFileSystem:
    Type: AWS::EFS::FileSystem
    Properties:
      Encrypted: true
      KmsKeyId: !Ref KMSKeyArn
      PerformanceMode: generalPurpose
      ThroughputMode: bursting
      FileSystemTags:
        - Key: Name
          Value: !Sub 'encrypted-efs-${Environment}'
        - Key: Environment
          Value: !Ref Environment
        - Key: EncryptionEnforced
          Value: 'true'

  # Lambda Function with encryption
  EncryptedLambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: !Sub 'encrypted-function-${Environment}'
      Runtime: python3.9
      Handler: index.lambda_handler
      Role: !GetAtt LambdaExecutionRole.Arn
      KmsKeyArn: !Ref KMSKeyArn
      Environment:
        Variables:
          ENVIRONMENT: !Ref Environment
      Code:
        ZipFile: |
          import json
          def lambda_handler(event, context):
              return {
                  'statusCode': 200,
                  'body': json.dumps('Hello from encrypted Lambda!')
              }
      Tags:
        - Key: Environment
          Value: !Ref Environment
        - Key: EncryptionEnforced
          Value: 'true'

  LambdaExecutionRole:
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

  # SNS Topic with encryption
  EncryptedSNSTopic:
    Type: AWS::SNS::Topic
    Properties:
      TopicName: !Sub 'encrypted-topic-${Environment}'
      KmsMasterKeyId: !Ref KMSKeyArn
      Tags:
        - Key: Environment
          Value: !Ref Environment
        - Key: EncryptionEnforced
          Value: 'true'

  # SQS Queue with encryption
  EncryptedSQSQueue:
    Type: AWS::SQS::Queue
    Properties:
      QueueName: !Sub 'encrypted-queue-${Environment}'
      KmsMasterKeyId: !Ref KMSKeyArn
      KmsDataKeyReusePeriodSeconds: 300
      Tags:
        - Key: Environment
          Value: !Ref Environment
        - Key: EncryptionEnforced
          Value: 'true'

  # CloudWatch Log Group with encryption
  S3AccessLogGroup:
    Type: AWS::Logs::LogGroup
    Properties:
      LogGroupName: !Sub '/aws/s3/${EncryptedS3Bucket}/access'
      RetentionInDays: 90
      KmsKeyId: !Ref KMSKeyArn

  # Config Rules for encryption compliance
  S3EncryptionConfigRule:
    Type: AWS::Config::ConfigRule
    Properties:
      ConfigRuleName: !Sub 's3-encryption-${Environment}'
      Description: 'Checks that S3 buckets have encryption enabled'
      Source:
        Owner: AWS
        SourceIdentifier: S3_BUCKET_SERVER_SIDE_ENCRYPTION_ENABLED
      Scope:
        ComplianceResourceTypes:
          - AWS::S3::Bucket

  RDSEncryptionConfigRule:
    Type: AWS::Config::ConfigRule
    Properties:
      ConfigRuleName: !Sub 'rds-encryption-${Environment}'
      Description: 'Checks that RDS instances have encryption enabled'
      Source:
        Owner: AWS
        SourceIdentifier: RDS_STORAGE_ENCRYPTED
      Scope:
        ComplianceResourceTypes:
          - AWS::RDS::DBInstance

  DynamoDBEncryptionConfigRule:
    Type: AWS::Config::ConfigRule
    Properties:
      ConfigRuleName: !Sub 'dynamodb-encryption-${Environment}'
      Description: 'Checks that DynamoDB tables have encryption enabled'
      Source:
        Owner: AWS
        SourceIdentifier: DYNAMODB_TABLE_ENCRYPTION_ENABLED
      Scope:
        ComplianceResourceTypes:
          - AWS::DynamoDB::Table

  # CloudWatch Alarms for encryption compliance
  EncryptionComplianceAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: !Sub 'encryption-compliance-${Environment}'
      AlarmDescription: 'Monitor encryption compliance across services'
      MetricName: ComplianceByConfigRule
      Namespace: AWS/Config
      Statistic: Average
      Period: 300
      EvaluationPeriods: 1
      Threshold: 1
      ComparisonOperator: LessThanThreshold
      Dimensions:
        - Name: RuleName
          Value: !Ref S3EncryptionConfigRule
      AlarmActions:
        - !Ref EncryptedSNSTopic

Outputs:
  EncryptedS3BucketName:
    Description: 'Name of the encrypted S3 bucket'
    Value: !Ref EncryptedS3Bucket
    Export:
      Name: !Sub '${AWS::StackName}-S3Bucket'
  
  EncryptedRDSEndpoint:
    Description: 'Endpoint of the encrypted RDS instance'
    Value: !GetAtt EncryptedRDSInstance.Endpoint.Address
    Export:
      Name: !Sub '${AWS::StackName}-RDSEndpoint'
  
  EncryptedDynamoDBTableName:
    Description: 'Name of the encrypted DynamoDB table'
    Value: !Ref EncryptedDynamoDBTable
    Export:
      Name: !Sub '${AWS::StackName}-DynamoDBTable'
  
  EncryptedEFSFileSystemId:
    Description: 'ID of the encrypted EFS file system'
    Value: !Ref EncryptedEFSFileSystem
    Export:
      Name: !Sub '${AWS::StackName}-EFSFileSystem'
```

## Relevant AWS Services

### Core Encryption Services
- **Amazon S3**: Server-side encryption with KMS, S3-managed keys, or customer-provided keys
- **Amazon RDS**: Database encryption for all supported database engines
- **Amazon EBS**: Volume encryption for EC2 instances
- **Amazon DynamoDB**: Table encryption with KMS keys
- **Amazon EFS**: File system encryption for shared storage
- **Amazon Redshift**: Data warehouse encryption

### Key Management Integration
- **AWS Key Management Service (KMS)**: Centralized key management for encryption
- **AWS CloudHSM**: Hardware security modules for high-security requirements
- **AWS Certificate Manager**: SSL/TLS certificate management

### Compliance and Monitoring
- **AWS Config**: Configuration compliance monitoring and rules
- **AWS CloudTrail**: Audit logging for encryption-related activities
- **Amazon CloudWatch**: Monitoring and alerting for encryption compliance
- **AWS Security Hub**: Centralized security findings management

### Automation and Enforcement
- **AWS Organizations**: Service Control Policies for encryption enforcement
- **AWS Lambda**: Automated remediation functions
- **Amazon EventBridge**: Event-driven encryption compliance workflows
- **AWS Systems Manager**: Automated configuration management

## Benefits of Enforcing Encryption at Rest

### Security Benefits
- **Data Protection**: Comprehensive protection against unauthorized access
- **Compliance Assurance**: Meet regulatory requirements for data protection
- **Defense in Depth**: Additional security layer beyond access controls
- **Key Management**: Centralized control over encryption keys

### Operational Benefits
- **Automated Enforcement**: Prevent creation of unencrypted resources
- **Consistent Implementation**: Uniform encryption across all services
- **Transparent Operation**: No impact on application functionality
- **Scalable Management**: Centralized encryption policy management

### Compliance Benefits
- **Regulatory Adherence**: Meet GDPR, HIPAA, PCI DSS requirements
- **Audit Readiness**: Complete audit trails for encryption activities
- **Risk Mitigation**: Reduce risk of data breaches and compliance violations
- **Documentation**: Comprehensive encryption compliance reporting

## Related Resources

- [AWS Well-Architected Framework - Data at Rest Protection](https://docs.aws.amazon.com/wellarchitected/latest/framework/sec-08.html)
- [AWS Encryption at Rest](https://docs.aws.amazon.com/whitepapers/latest/logical-separation/encrypting-data-at-rest-and-in-transit.html)
- [Amazon S3 Encryption](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucket-encryption.html)
- [Amazon RDS Encryption](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Overview.Encryption.html)
- [AWS Config Rules for Encryption](https://docs.aws.amazon.com/config/latest/developerguide/managed-rules-by-aws-config.html)
- [AWS Security Blog - Encryption](https://aws.amazon.com/blogs/security/tag/encryption/)
```
```
