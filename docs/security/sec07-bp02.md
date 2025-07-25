---
title: "SEC07-BP02: Apply data protection controls based on data sensitivity"
layout: default
parent: "SEC07 - How do you classify your data?"
grand_parent: Security
nav_order: 2
---

# SEC07-BP02: Apply data protection controls based on data sensitivity

## Overview

Once you understand your data classification scheme (SEC07-BP01), you must implement appropriate protection controls that match the sensitivity level of your data. Different data classifications require different levels of protection, from basic access controls for public data to comprehensive encryption and monitoring for highly sensitive information.

This best practice ensures that your protection mechanisms are proportionate to the value and sensitivity of the data, optimizing both security and operational efficiency while meeting regulatory and compliance requirements.

## Implementation Guidance

### 1. Map Protection Controls to Classification Levels

Define specific protection controls for each data classification level established in your data classification scheme:

- **Public Data**: Basic access logging and integrity protection
- **Internal Data**: Access controls, basic encryption, and audit logging
- **Confidential Data**: Strong encryption, strict access controls, detailed monitoring
- **Restricted Data**: Maximum security controls including encryption at rest and in transit, multi-factor authentication, and comprehensive audit trails

### 2. Implement Encryption Controls

Apply encryption controls based on data sensitivity:

- **Encryption at Rest**: Use AWS KMS with appropriate key management policies
- **Encryption in Transit**: Implement TLS/SSL for data transmission
- **Field-Level Encryption**: Apply granular encryption for highly sensitive fields
- **Client-Side Encryption**: Implement for maximum data protection

### 3. Configure Access Controls

Establish access controls proportionate to data sensitivity:

- **Identity and Access Management**: Implement least privilege access
- **Multi-Factor Authentication**: Require for sensitive data access
- **Attribute-Based Access Control**: Use data classification tags for access decisions
- **Time-Based Access**: Implement temporary access for sensitive operations

### 4. Establish Monitoring and Auditing

Implement monitoring controls based on data classification:

- **Access Logging**: Log all access to classified data
- **Anomaly Detection**: Monitor for unusual access patterns
- **Real-Time Alerting**: Alert on unauthorized access attempts
- **Compliance Reporting**: Generate reports for regulatory requirements

### 5. Implement Data Loss Prevention

Deploy DLP controls appropriate to data sensitivity:

- **Content Inspection**: Scan data for sensitive information
- **Egress Controls**: Prevent unauthorized data exfiltration
- **Endpoint Protection**: Secure data on user devices
- **Network Monitoring**: Monitor data flows across network boundaries

### 6. Configure Backup and Recovery Controls

Establish backup and recovery controls based on data classification:

- **Backup Encryption**: Encrypt backups according to data sensitivity
- **Retention Policies**: Apply appropriate retention periods
- **Recovery Testing**: Test recovery procedures for critical data
- **Geographic Distribution**: Distribute backups based on data requirements

## Implementation Examples

### Example 1: Data Protection Control Matrix

```yaml
# data-protection-matrix.yaml
data_protection_controls:
  classification_levels:
    public:
      encryption:
        at_rest: "optional"
        in_transit: "basic_tls"
        key_management: "aws_managed"
      access_controls:
        authentication: "basic"
        authorization: "role_based"
        mfa_required: false
      monitoring:
        access_logging: "basic"
        anomaly_detection: false
        real_time_alerts: false
      backup:
        encryption_required: false
        retention_period: "30_days"
        geographic_distribution: "single_region"
      
    internal:
      encryption:
        at_rest: "required"
        in_transit: "tls_1_2_minimum"
        key_management: "aws_managed"
      access_controls:
        authentication: "corporate_sso"
        authorization: "attribute_based"
        mfa_required: false
      monitoring:
        access_logging: "detailed"
        anomaly_detection: true
        real_time_alerts: "business_hours"
      backup:
        encryption_required: true
        retention_period: "90_days"
        geographic_distribution: "multi_region"
      
    confidential:
      encryption:
        at_rest: "customer_managed_kms"
        in_transit: "tls_1_3_required"
        key_management: "customer_managed"
        field_level: "sensitive_fields"
      access_controls:
        authentication: "corporate_sso"
        authorization: "attribute_based"
        mfa_required: true
      monitoring:
        access_logging: "comprehensive"
        anomaly_detection: true
        real_time_alerts: "24x7"
        dlp_scanning: true
      backup:
        encryption_required: true
        retention_period: "7_years"
        geographic_distribution: "multi_region"
        cross_account_backup: true
      
    restricted:
      encryption:
        at_rest: "customer_managed_kms"
        in_transit: "mutual_tls"
        key_management: "hsm_backed"
        field_level: "all_fields"
        client_side: "required"
      access_controls:
        authentication: "certificate_based"
        authorization: "attribute_based"
        mfa_required: true
        privileged_access_management: true
      monitoring:
        access_logging: "comprehensive"
        anomaly_detection: true
        real_time_alerts: "immediate"
        dlp_scanning: true
        user_behavior_analytics: true
      backup:
        encryption_required: true
        retention_period: "indefinite"
        geographic_distribution: "multi_region"
        cross_account_backup: true
        immutable_backups: true

  aws_services_mapping:
    encryption:
      kms: "AWS Key Management Service"
      s3_encryption: "S3 Server-Side Encryption"
      ebs_encryption: "EBS Encryption"
      rds_encryption: "RDS Encryption"
    
    access_controls:
      iam: "AWS Identity and Access Management"
      cognito: "Amazon Cognito"
      sso: "AWS Single Sign-On"
      secrets_manager: "AWS Secrets Manager"
    
    monitoring:
      cloudtrail: "AWS CloudTrail"
      guardduty: "Amazon GuardDuty"
      macie: "Amazon Macie"
      config: "AWS Config"
      security_hub: "AWS Security Hub"
    
    backup:
      backup: "AWS Backup"
      s3_glacier: "Amazon S3 Glacier"
      cross_region_replication: "S3 Cross-Region Replication"

compliance_mappings:
  gdpr:
    - "Article 32: Security of processing"
    - "Article 25: Data protection by design and by default"
  hipaa:
    - "164.312(a)(1): Access control"
    - "164.312(e)(1): Transmission security"
  pci_dss:
    - "Requirement 3: Protect stored cardholder data"
    - "Requirement 4: Encrypt transmission of cardholder data"
  sox:
    - "Section 404: Management assessment of internal controls"
```

### Example 2: Automated Protection Control Implementation

```python
# protection_controls_manager.py
import boto3
import json
import yaml
from typing import Dict, List, Any
from dataclasses import dataclass
from enum import Enum

class ClassificationLevel(Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"

@dataclass
class ProtectionControl:
    control_type: str
    service: str
    configuration: Dict[str, Any]
    required: bool
    compliance_frameworks: List[str]

class DataProtectionControlsManager:
    """
    Manages the implementation of data protection controls based on classification levels
    """
    
    def __init__(self, region: str = 'us-east-1'):
        self.region = region
        self.s3_client = boto3.client('s3', region_name=region)
        self.kms_client = boto3.client('kms', region_name=region)
        self.iam_client = boto3.client('iam', region_name=region)
        self.guardduty_client = boto3.client('guardduty', region_name=region)
        self.macie_client = boto3.client('macie2', region_name=region)
        self.config_client = boto3.client('config', region_name=region)
        
        # Load protection control matrix
        self.protection_matrix = self._load_protection_matrix()
    
    def _load_protection_matrix(self) -> Dict[str, Any]:
        """Load the data protection control matrix"""
        try:
            with open('data-protection-matrix.yaml', 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            return self._get_default_protection_matrix()
    
    def _get_default_protection_matrix(self) -> Dict[str, Any]:
        """Return default protection control matrix"""
        return {
            "data_protection_controls": {
                "classification_levels": {
                    "public": {
                        "encryption": {"at_rest": "optional", "in_transit": "basic_tls"},
                        "access_controls": {"mfa_required": False},
                        "monitoring": {"access_logging": "basic"}
                    },
                    "internal": {
                        "encryption": {"at_rest": "required", "in_transit": "tls_1_2_minimum"},
                        "access_controls": {"mfa_required": False},
                        "monitoring": {"access_logging": "detailed", "anomaly_detection": True}
                    },
                    "confidential": {
                        "encryption": {"at_rest": "customer_managed_kms", "in_transit": "tls_1_3_required"},
                        "access_controls": {"mfa_required": True},
                        "monitoring": {"access_logging": "comprehensive", "anomaly_detection": True, "dlp_scanning": True}
                    },
                    "restricted": {
                        "encryption": {"at_rest": "customer_managed_kms", "in_transit": "mutual_tls", "client_side": "required"},
                        "access_controls": {"mfa_required": True, "privileged_access_management": True},
                        "monitoring": {"access_logging": "comprehensive", "anomaly_detection": True, "dlp_scanning": True, "user_behavior_analytics": True}
                    }
                }
            }
        }
    
    def apply_s3_protection_controls(self, bucket_name: str, classification: ClassificationLevel) -> Dict[str, Any]:
        """
        Apply S3 protection controls based on data classification
        """
        results = {
            "bucket": bucket_name,
            "classification": classification.value,
            "controls_applied": [],
            "errors": []
        }
        
        controls = self.protection_matrix["data_protection_controls"]["classification_levels"][classification.value]
        
        try:
            # Apply encryption controls
            encryption_config = controls.get("encryption", {})
            if encryption_config.get("at_rest") in ["required", "customer_managed_kms"]:
                self._apply_s3_encryption(bucket_name, encryption_config)
                results["controls_applied"].append("s3_encryption")
            
            # Apply access controls
            access_config = controls.get("access_controls", {})
            if access_config.get("mfa_required", False):
                self._apply_s3_mfa_policy(bucket_name)
                results["controls_applied"].append("mfa_policy")
            
            # Apply monitoring controls
            monitoring_config = controls.get("monitoring", {})
            if monitoring_config.get("access_logging") in ["detailed", "comprehensive"]:
                self._enable_s3_access_logging(bucket_name)
                results["controls_applied"].append("access_logging")
            
            # Apply backup controls
            backup_config = controls.get("backup", {})
            if backup_config.get("cross_region_replication", False):
                self._enable_s3_cross_region_replication(bucket_name, classification)
                results["controls_applied"].append("cross_region_replication")
            
        except Exception as e:
            results["errors"].append(f"Error applying controls: {str(e)}")
        
        return results
    
    def _apply_s3_encryption(self, bucket_name: str, encryption_config: Dict[str, Any]):
        """Apply S3 encryption based on configuration"""
        if encryption_config.get("at_rest") == "customer_managed_kms":
            # Create or use existing customer-managed KMS key
            kms_key_id = self._get_or_create_kms_key(f"s3-{bucket_name}-key")
            
            encryption_configuration = {
                'Rules': [
                    {
                        'ApplyServerSideEncryptionByDefault': {
                            'SSEAlgorithm': 'aws:kms',
                            'KMSMasterKeyID': kms_key_id
                        },
                        'BucketKeyEnabled': True
                    }
                ]
            }
        else:
            encryption_configuration = {
                'Rules': [
                    {
                        'ApplyServerSideEncryptionByDefault': {
                            'SSEAlgorithm': 'AES256'
                        }
                    }
                ]
            }
        
        self.s3_client.put_bucket_encryption(
            Bucket=bucket_name,
            ServerSideEncryptionConfiguration=encryption_configuration
        )
    
    def _apply_s3_mfa_policy(self, bucket_name: str):
        """Apply MFA requirement policy to S3 bucket"""
        mfa_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "RequireMFAForSensitiveOperations",
                    "Effect": "Deny",
                    "Principal": "*",
                    "Action": [
                        "s3:DeleteObject",
                        "s3:DeleteObjectVersion",
                        "s3:PutObject",
                        "s3:PutObjectAcl"
                    ],
                    "Resource": f"arn:aws:s3:::{bucket_name}/*",
                    "Condition": {
                        "BoolIfExists": {
                            "aws:MultiFactorAuthPresent": "false"
                        }
                    }
                }
            ]
        }
        
        self.s3_client.put_bucket_policy(
            Bucket=bucket_name,
            Policy=json.dumps(mfa_policy)
        )
    
    def _enable_s3_access_logging(self, bucket_name: str):
        """Enable S3 access logging"""
        logging_bucket = f"{bucket_name}-access-logs"
        
        # Create logging bucket if it doesn't exist
        try:
            self.s3_client.head_bucket(Bucket=logging_bucket)
        except:
            self.s3_client.create_bucket(Bucket=logging_bucket)
        
        # Enable access logging
        self.s3_client.put_bucket_logging(
            Bucket=bucket_name,
            BucketLoggingStatus={
                'LoggingEnabled': {
                    'TargetBucket': logging_bucket,
                    'TargetPrefix': f'{bucket_name}/'
                }
            }
        )
    
    def _enable_s3_cross_region_replication(self, bucket_name: str, classification: ClassificationLevel):
        """Enable S3 cross-region replication for backup"""
        # This is a simplified implementation
        # In practice, you would need to set up destination bucket and IAM role
        replication_config = {
            'Role': f'arn:aws:iam::{self._get_account_id()}:role/replication-role',
            'Rules': [
                {
                    'ID': f'{bucket_name}-replication',
                    'Status': 'Enabled',
                    'Prefix': '',
                    'Destination': {
                        'Bucket': f'arn:aws:s3:::{bucket_name}-replica',
                        'StorageClass': 'STANDARD_IA'
                    }
                }
            ]
        }
        
        # Note: This would require proper setup of destination bucket and IAM role
        print(f"Cross-region replication configuration prepared for {bucket_name}")
    
    def _get_or_create_kms_key(self, key_alias: str) -> str:
        """Get existing or create new KMS key"""
        try:
            # Try to get existing key
            response = self.kms_client.describe_key(KeyId=f'alias/{key_alias}')
            return response['KeyMetadata']['KeyId']
        except:
            # Create new key
            response = self.kms_client.create_key(
                Description=f'Customer-managed key for {key_alias}',
                Usage='ENCRYPT_DECRYPT'
            )
            key_id = response['KeyMetadata']['KeyId']
            
            # Create alias
            self.kms_client.create_alias(
                AliasName=f'alias/{key_alias}',
                TargetKeyId=key_id
            )
            
            return key_id
    
    def _get_account_id(self) -> str:
        """Get AWS account ID"""
        return boto3.client('sts').get_caller_identity()['Account']
    
    def apply_rds_protection_controls(self, db_instance_id: str, classification: ClassificationLevel) -> Dict[str, Any]:
        """
        Apply RDS protection controls based on data classification
        """
        results = {
            "db_instance": db_instance_id,
            "classification": classification.value,
            "controls_applied": [],
            "recommendations": []
        }
        
        controls = self.protection_matrix["data_protection_controls"]["classification_levels"][classification.value]
        
        # Generate RDS protection recommendations
        encryption_config = controls.get("encryption", {})
        if encryption_config.get("at_rest") in ["required", "customer_managed_kms"]:
            results["recommendations"].append({
                "control": "rds_encryption",
                "description": "Enable RDS encryption at rest",
                "implementation": "Set StorageEncrypted=true when creating RDS instance"
            })
        
        if encryption_config.get("in_transit") in ["tls_1_2_minimum", "tls_1_3_required"]:
            results["recommendations"].append({
                "control": "rds_ssl",
                "description": "Enforce SSL/TLS connections",
                "implementation": "Use rds.force_ssl parameter and SSL certificates"
            })
        
        monitoring_config = controls.get("monitoring", {})
        if monitoring_config.get("access_logging") in ["detailed", "comprehensive"]:
            results["recommendations"].append({
                "control": "rds_logging",
                "description": "Enable RDS enhanced monitoring and logging",
                "implementation": "Enable Performance Insights and CloudWatch Logs"
            })
        
        return results
    
    def generate_protection_controls_report(self, resources: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate a comprehensive report of protection controls applied to resources
        """
        report = {
            "timestamp": boto3.client('sts').get_caller_identity(),
            "summary": {
                "total_resources": len(resources),
                "by_classification": {},
                "controls_coverage": {}
            },
            "resources": [],
            "recommendations": []
        }
        
        for resource in resources:
            resource_type = resource.get("type")
            classification = ClassificationLevel(resource.get("classification", "internal"))
            
            if resource_type == "s3":
                result = self.apply_s3_protection_controls(
                    resource["name"], 
                    classification
                )
            elif resource_type == "rds":
                result = self.apply_rds_protection_controls(
                    resource["name"], 
                    classification
                )
            else:
                result = {
                    "resource": resource["name"],
                    "type": resource_type,
                    "classification": classification.value,
                    "status": "unsupported_resource_type"
                }
            
            report["resources"].append(result)
            
            # Update summary statistics
            classification_key = classification.value
            if classification_key not in report["summary"]["by_classification"]:
                report["summary"]["by_classification"][classification_key] = 0
            report["summary"]["by_classification"][classification_key] += 1
        
        return report

# Example usage
if __name__ == "__main__":
    # Initialize the protection controls manager
    manager = DataProtectionControlsManager()
    
    # Example resources with classifications
    resources = [
        {"name": "customer-data-bucket", "type": "s3", "classification": "confidential"},
        {"name": "public-website-bucket", "type": "s3", "classification": "public"},
        {"name": "employee-database", "type": "rds", "classification": "restricted"},
        {"name": "analytics-data-bucket", "type": "s3", "classification": "internal"}
    ]
    
    # Generate protection controls report
    report = manager.generate_protection_controls_report(resources)
    
    print("Data Protection Controls Report:")
    print(f"Total Resources: {report['summary']['total_resources']}")
    print(f"Classification Distribution: {report['summary']['by_classification']}")
    
    for resource_result in report["resources"]:
        print(f"\nResource: {resource_result.get('bucket', resource_result.get('db_instance', 'unknown'))}")
        print(f"Classification: {resource_result['classification']}")
        if 'controls_applied' in resource_result:
            print(f"Controls Applied: {', '.join(resource_result['controls_applied'])}")
        if 'recommendations' in resource_result:
            print(f"Recommendations: {len(resource_result['recommendations'])} items")
```

### Example 3: CloudFormation Template for Classification-Based Protection

```yaml
# classification-based-protection.yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Data protection controls based on classification levels'

Parameters:
  DataClassification:
    Type: String
    Default: 'internal'
    AllowedValues: ['public', 'internal', 'confidential', 'restricted']
    Description: 'Data classification level for this stack'
  
  BucketName:
    Type: String
    Description: 'Name of the S3 bucket to protect'
  
  Environment:
    Type: String
    Default: 'dev'
    AllowedValues: ['dev', 'staging', 'prod']
    Description: 'Environment for deployment'

Conditions:
  IsConfidentialOrRestricted: !Or 
    - !Equals [!Ref DataClassification, 'confidential']
    - !Equals [!Ref DataClassification, 'restricted']
  
  IsRestricted: !Equals [!Ref DataClassification, 'restricted']
  
  IsPublic: !Equals [!Ref DataClassification, 'public']
  
  RequiresEncryption: !Not [!Equals [!Ref DataClassification, 'public']]

Resources:
  # KMS Key for customer-managed encryption (confidential/restricted data)
  DataEncryptionKey:
    Type: AWS::KMS::Key
    Condition: IsConfidentialOrRestricted
    Properties:
      Description: !Sub 'Customer-managed key for ${DataClassification} data'
      KeyPolicy:
        Version: '2012-10-17'
        Statement:
          - Sid: Enable IAM User Permissions
            Effect: Allow
            Principal:
              AWS: !Sub 'arn:aws:iam::${AWS::AccountId}:root'
            Action: 'kms:*'
            Resource: '*'
          - Sid: Allow use of the key for encryption/decryption
            Effect: Allow
            Principal:
              AWS: !GetAtt DataAccessRole.Arn
            Action:
              - 'kms:Encrypt'
              - 'kms:Decrypt'
              - 'kms:ReEncrypt*'
              - 'kms:GenerateDataKey*'
              - 'kms:DescribeKey'
            Resource: '*'
      KeyRotationStatus: true
      Tags:
        - Key: DataClassification
          Value: !Ref DataClassification
        - Key: Environment
          Value: !Ref Environment

  DataEncryptionKeyAlias:
    Type: AWS::KMS::Alias
    Condition: IsConfidentialOrRestricted
    Properties:
      AliasName: !Sub 'alias/${BucketName}-${DataClassification}-key'
      TargetKeyId: !Ref DataEncryptionKey

  # S3 Bucket with classification-based protection
  DataBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Ref BucketName
      BucketEncryption:
        ServerSideEncryptionConfiguration:
          - ServerSideEncryptionByDefault:
              SSEAlgorithm: !If 
                - IsConfidentialOrRestricted
                - 'aws:kms'
                - 'AES256'
              KMSMasterKeyID: !If
                - IsConfidentialOrRestricted
                - !Ref DataEncryptionKey
                - !Ref 'AWS::NoValue'
            BucketKeyEnabled: !If [IsConfidentialOrRestricted, true, false]
      
      PublicAccessBlockConfiguration:
        BlockPublicAcls: !If [IsPublic, false, true]
        BlockPublicPolicy: !If [IsPublic, false, true]
        IgnorePublicAcls: !If [IsPublic, false, true]
        RestrictPublicBuckets: !If [IsPublic, false, true]
      
      LoggingConfiguration: !If
        - RequiresEncryption
        - DestinationBucketName: !Ref AccessLogsBucket
          LogFilePrefix: !Sub '${BucketName}/'
        - !Ref 'AWS::NoValue'
      
      NotificationConfiguration: !If
        - IsConfidentialOrRestricted
        - CloudWatchConfigurations:
            - Event: 's3:ObjectCreated:*'
              CloudWatchConfiguration:
                LogGroupName: !Ref DataAccessLogGroup
        - !Ref 'AWS::NoValue'
      
      VersioningConfiguration:
        Status: !If [IsConfidentialOrRestricted, 'Enabled', 'Suspended']
      
      Tags:
        - Key: DataClassification
          Value: !Ref DataClassification
        - Key: Environment
          Value: !Ref Environment
        - Key: BackupRequired
          Value: !If [IsConfidentialOrRestricted, 'true', 'false']

  # Access logs bucket (for non-public data)
  AccessLogsBucket:
    Type: AWS::S3::Bucket
    Condition: RequiresEncryption
    Properties:
      BucketName: !Sub '${BucketName}-access-logs'
      BucketEncryption:
        ServerSideEncryptionConfiguration:
          - ServerSideEncryptionByDefault:
              SSEAlgorithm: 'AES256'
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true
      LifecycleConfiguration:
        Rules:
          - Id: DeleteOldLogs
            Status: Enabled
            ExpirationInDays: !If [IsRestricted, 2555, 90]  # 7 years for restricted, 90 days for others

  # IAM Role for data access
  DataAccessRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: !Sub '${BucketName}-${DataClassification}-access-role'
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: ec2.amazonaws.com
            Action: 'sts:AssumeRole'
            Condition: !If
              - IsRestricted
              - Bool:
                  'aws:MultiFactorAuthPresent': 'true'
              - !Ref 'AWS::NoValue'
      
      Policies:
        - PolicyName: DataAccessPolicy
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - 's3:GetObject'
                  - 's3:PutObject'
                  - !If [IsConfidentialOrRestricted, 's3:DeleteObject', !Ref 'AWS::NoValue']
                Resource: !Sub '${DataBucket}/*'
                Condition: !If
                  - IsRestricted
                  - Bool:
                      'aws:MultiFactorAuthPresent': 'true'
                  - !Ref 'AWS::NoValue'
              
              - Effect: Allow
                Action:
                  - 's3:ListBucket'
                Resource: !GetAtt DataBucket.Arn
              
              - !If
                - IsConfidentialOrRestricted
                - Effect: Allow
                  Action:
                    - 'kms:Encrypt'
                    - 'kms:Decrypt'
                    - 'kms:ReEncrypt*'
                    - 'kms:GenerateDataKey*'
                    - 'kms:DescribeKey'
                  Resource: !GetAtt DataEncryptionKey.Arn
                - !Ref 'AWS::NoValue'
      
      Tags:
        - Key: DataClassification
          Value: !Ref DataClassification
        - Key: Environment
          Value: !Ref Environment

  # CloudWatch Log Group for access monitoring (confidential/restricted)
  DataAccessLogGroup:
    Type: AWS::Logs::LogGroup
    Condition: IsConfidentialOrRestricted
    Properties:
      LogGroupName: !Sub '/aws/s3/${BucketName}/access'
      RetentionInDays: !If [IsRestricted, 2555, 365]  # 7 years for restricted, 1 year for confidential
      KmsKeyId: !If [IsRestricted, !GetAtt DataEncryptionKey.Arn, !Ref 'AWS::NoValue']

  # CloudWatch Alarm for unusual access patterns (confidential/restricted)
  UnusualAccessAlarm:
    Type: AWS::CloudWatch::Alarm
    Condition: IsConfidentialOrRestricted
    Properties:
      AlarmName: !Sub '${BucketName}-unusual-access'
      AlarmDescription: 'Alarm for unusual access patterns to classified data'
      MetricName: NumberOfObjects
      Namespace: AWS/S3
      Statistic: Sum
      Period: 300
      EvaluationPeriods: 2
      Threshold: !If [IsRestricted, 10, 50]  # Lower threshold for restricted data
      ComparisonOperator: GreaterThanThreshold
      Dimensions:
        - Name: BucketName
          Value: !Ref DataBucket
      AlarmActions:
        - !Ref SecurityNotificationTopic

  # SNS Topic for security notifications (confidential/restricted)
  SecurityNotificationTopic:
    Type: AWS::SNS::Topic
    Condition: IsConfidentialOrRestricted
    Properties:
      TopicName: !Sub '${BucketName}-security-notifications'
      KmsMasterKeyId: !If [IsRestricted, !Ref DataEncryptionKey, 'alias/aws/sns']
      Tags:
        - Key: DataClassification
          Value: !Ref DataClassification
        - Key: Environment
          Value: !Ref Environment

  # Config Rule to monitor compliance (confidential/restricted)
  S3EncryptionComplianceRule:
    Type: AWS::Config::ConfigRule
    Condition: IsConfidentialOrRestricted
    Properties:
      ConfigRuleName: !Sub '${BucketName}-encryption-compliance'
      Description: 'Checks that S3 buckets have encryption enabled'
      Source:
        Owner: AWS
        SourceIdentifier: S3_BUCKET_SERVER_SIDE_ENCRYPTION_ENABLED
      Scope:
        ComplianceResourceTypes:
          - AWS::S3::Bucket
        ComplianceResourceId: !Ref DataBucket

  # Backup Vault for classified data (confidential/restricted)
  DataBackupVault:
    Type: AWS::Backup::BackupVault
    Condition: IsConfidentialOrRestricted
    Properties:
      BackupVaultName: !Sub '${BucketName}-backup-vault'
      EncryptionKeyArn: !GetAtt DataEncryptionKey.Arn
      Notifications:
        BackupVaultEvents:
          - BACKUP_JOB_COMPLETED
          - BACKUP_JOB_FAILED
        SNSTopicArn: !Ref SecurityNotificationTopic
      AccessPolicy:
        Version: '2012-10-17'
        Statement:
          - Effect: Deny
            Principal: '*'
            Action: '*'
            Resource: '*'
            Condition:
              Bool:
                'aws:MultiFactorAuthPresent': 'false'

  # Backup Plan for classified data
  DataBackupPlan:
    Type: AWS::Backup::BackupPlan
    Condition: IsConfidentialOrRestricted
    Properties:
      BackupPlan:
        BackupPlanName: !Sub '${BucketName}-backup-plan'
        BackupPlanRule:
          - RuleName: DailyBackups
            TargetBackupVault: !Ref DataBackupVault
            ScheduleExpression: 'cron(0 2 ? * * *)'  # Daily at 2 AM
            StartWindowMinutes: 60
            CompletionWindowMinutes: 120
            Lifecycle:
              DeleteAfterDays: !If [IsRestricted, 2555, 365]  # 7 years for restricted
              MoveToColdStorageAfterDays: 30
            RecoveryPointTags:
              DataClassification: !Ref DataClassification
              Environment: !Ref Environment

Outputs:
  BucketName:
    Description: 'Name of the created S3 bucket'
    Value: !Ref DataBucket
    Export:
      Name: !Sub '${AWS::StackName}-BucketName'
  
  BucketArn:
    Description: 'ARN of the created S3 bucket'
    Value: !GetAtt DataBucket.Arn
    Export:
      Name: !Sub '${AWS::StackName}-BucketArn'
  
  EncryptionKeyId:
    Condition: IsConfidentialOrRestricted
    Description: 'ID of the KMS encryption key'
    Value: !Ref DataEncryptionKey
    Export:
      Name: !Sub '${AWS::StackName}-EncryptionKeyId'
  
  DataAccessRoleArn:
    Description: 'ARN of the data access role'
    Value: !GetAtt DataAccessRole.Arn
    Export:
      Name: !Sub '${AWS::StackName}-DataAccessRoleArn'
  
  SecurityNotificationTopicArn:
    Condition: IsConfidentialOrRestricted
    Description: 'ARN of the security notification topic'
    Value: !Ref SecurityNotificationTopic
    Export:
      Name: !Sub '${AWS::StackName}-SecurityNotificationTopicArn'
```

### Example 4: Terraform Configuration for Multi-Service Protection Controls

```hcl
# main.tf - Classification-based protection controls
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

variable "data_classification" {
  description = "Data classification level"
  type        = string
  default     = "internal"
  validation {
    condition = contains(["public", "internal", "confidential", "restricted"], var.data_classification)
    error_message = "Data classification must be one of: public, internal, confidential, restricted."
  }
}

variable "resource_name" {
  description = "Base name for resources"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}

locals {
  # Define protection controls based on classification
  protection_controls = {
    public = {
      encryption_required = false
      kms_customer_managed = false
      mfa_required = false
      access_logging = "basic"
      backup_retention_days = 30
      cross_region_backup = false
      monitoring_level = "basic"
    }
    internal = {
      encryption_required = true
      kms_customer_managed = false
      mfa_required = false
      access_logging = "detailed"
      backup_retention_days = 90
      cross_region_backup = false
      monitoring_level = "standard"
    }
    confidential = {
      encryption_required = true
      kms_customer_managed = true
      mfa_required = true
      access_logging = "comprehensive"
      backup_retention_days = 365
      cross_region_backup = true
      monitoring_level = "enhanced"
    }
    restricted = {
      encryption_required = true
      kms_customer_managed = true
      mfa_required = true
      access_logging = "comprehensive"
      backup_retention_days = 2555  # 7 years
      cross_region_backup = true
      monitoring_level = "maximum"
    }
  }
  
  current_controls = local.protection_controls[var.data_classification]
  
  common_tags = {
    DataClassification = var.data_classification
    Environment = var.environment
    ManagedBy = "terraform"
  }
}

# KMS Key for customer-managed encryption
resource "aws_kms_key" "data_encryption" {
  count = local.current_controls.kms_customer_managed ? 1 : 0
  
  description             = "Customer-managed key for ${var.data_classification} data"
  deletion_window_in_days = var.data_classification == "restricted" ? 30 : 10
  enable_key_rotation     = true
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "Enable IAM User Permissions"
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"
        }
        Action   = "kms:*"
        Resource = "*"
      },
      {
        Sid    = "Allow use of the key"
        Effect = "Allow"
        Principal = {
          AWS = aws_iam_role.data_access.arn
        }
        Action = [
          "kms:Encrypt",
          "kms:Decrypt",
          "kms:ReEncrypt*",
          "kms:GenerateDataKey*",
          "kms:DescribeKey"
        ]
        Resource = "*"
      }
    ]
  })
  
  tags = merge(local.common_tags, {
    Name = "${var.resource_name}-${var.data_classification}-key"
  })
}

resource "aws_kms_alias" "data_encryption" {
  count = local.current_controls.kms_customer_managed ? 1 : 0
  
  name          = "alias/${var.resource_name}-${var.data_classification}-key"
  target_key_id = aws_kms_key.data_encryption[0].key_id
}

# S3 Bucket with classification-based protection
resource "aws_s3_bucket" "data" {
  bucket = "${var.resource_name}-${var.data_classification}-data"
  
  tags = merge(local.common_tags, {
    Name = "${var.resource_name}-${var.data_classification}-data"
  })
}

resource "aws_s3_bucket_encryption" "data" {
  bucket = aws_s3_bucket.data.id
  
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = local.current_controls.kms_customer_managed ? "aws:kms" : "AES256"
        kms_master_key_id = local.current_controls.kms_customer_managed ? aws_kms_key.data_encryption[0].arn : null
      }
      bucket_key_enabled = local.current_controls.kms_customer_managed
    }
  }
}

resource "aws_s3_bucket_public_access_block" "data" {
  bucket = aws_s3_bucket.data.id
  
  block_public_acls       = var.data_classification != "public"
  block_public_policy     = var.data_classification != "public"
  ignore_public_acls      = var.data_classification != "public"
  restrict_public_buckets = var.data_classification != "public"
}

resource "aws_s3_bucket_versioning" "data" {
  bucket = aws_s3_bucket.data.id
  
  versioning_configuration {
    status = contains(["confidential", "restricted"], var.data_classification) ? "Enabled" : "Suspended"
  }
}

# Access logging bucket
resource "aws_s3_bucket" "access_logs" {
  count = local.current_controls.encryption_required ? 1 : 0
  
  bucket = "${var.resource_name}-${var.data_classification}-access-logs"
  
  tags = merge(local.common_tags, {
    Name = "${var.resource_name}-${var.data_classification}-access-logs"
  })
}

resource "aws_s3_bucket_encryption" "access_logs" {
  count = local.current_controls.encryption_required ? 1 : 0
  
  bucket = aws_s3_bucket.access_logs[0].id
  
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}

resource "aws_s3_bucket_logging" "data" {
  count = local.current_controls.encryption_required ? 1 : 0
  
  bucket = aws_s3_bucket.data.id
  
  target_bucket = aws_s3_bucket.access_logs[0].id
  target_prefix = "${aws_s3_bucket.data.id}/"
}

# IAM Role for data access
resource "aws_iam_role" "data_access" {
  name = "${var.resource_name}-${var.data_classification}-access-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
        Condition = local.current_controls.mfa_required ? {
          Bool = {
            "aws:MultiFactorAuthPresent" = "true"
          }
        } : {}
      }
    ]
  })
  
  tags = local.common_tags
}

resource "aws_iam_role_policy" "data_access" {
  name = "DataAccessPolicy"
  role = aws_iam_role.data_access.id
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = concat([
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject"
        ]
        Resource = "${aws_s3_bucket.data.arn}/*"
        Condition = local.current_controls.mfa_required ? {
          Bool = {
            "aws:MultiFactorAuthPresent" = "true"
          }
        } : {}
      },
      {
        Effect = "Allow"
        Action = [
          "s3:ListBucket"
        ]
        Resource = aws_s3_bucket.data.arn
      }
    ], local.current_controls.kms_customer_managed ? [
      {
        Effect = "Allow"
        Action = [
          "kms:Encrypt",
          "kms:Decrypt",
          "kms:ReEncrypt*",
          "kms:GenerateDataKey*",
          "kms:DescribeKey"
        ]
        Resource = aws_kms_key.data_encryption[0].arn
      }
    ] : [])
  })
}

# CloudWatch Log Group for monitoring
resource "aws_cloudwatch_log_group" "data_access" {
  count = contains(["confidential", "restricted"], var.data_classification) ? 1 : 0
  
  name              = "/aws/s3/${aws_s3_bucket.data.id}/access"
  retention_in_days = local.current_controls.backup_retention_days
  kms_key_id        = var.data_classification == "restricted" ? aws_kms_key.data_encryption[0].arn : null
  
  tags = local.common_tags
}

# CloudWatch Alarm for unusual access
resource "aws_cloudwatch_metric_alarm" "unusual_access" {
  count = contains(["confidential", "restricted"], var.data_classification) ? 1 : 0
  
  alarm_name          = "${var.resource_name}-unusual-access"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "NumberOfObjects"
  namespace           = "AWS/S3"
  period              = "300"
  statistic           = "Sum"
  threshold           = var.data_classification == "restricted" ? "10" : "50"
  alarm_description   = "This metric monitors unusual access patterns"
  
  dimensions = {
    BucketName = aws_s3_bucket.data.id
  }
  
  alarm_actions = [aws_sns_topic.security_notifications[0].arn]
  
  tags = local.common_tags
}

# SNS Topic for security notifications
resource "aws_sns_topic" "security_notifications" {
  count = contains(["confidential", "restricted"], var.data_classification) ? 1 : 0
  
  name              = "${var.resource_name}-security-notifications"
  kms_master_key_id = var.data_classification == "restricted" ? aws_kms_key.data_encryption[0].id : "alias/aws/sns"
  
  tags = local.common_tags
}

# AWS Backup Vault for classified data
resource "aws_backup_vault" "data" {
  count = contains(["confidential", "restricted"], var.data_classification) ? 1 : 0
  
  name        = "${var.resource_name}-backup-vault"
  kms_key_arn = aws_kms_key.data_encryption[0].arn
  
  tags = local.common_tags
}

# AWS Backup Plan
resource "aws_backup_plan" "data" {
  count = contains(["confidential", "restricted"], var.data_classification) ? 1 : 0
  
  name = "${var.resource_name}-backup-plan"
  
  rule {
    rule_name         = "daily_backups"
    target_vault_name = aws_backup_vault.data[0].name
    schedule          = "cron(0 2 ? * * *)"  # Daily at 2 AM
    
    start_window      = 60
    completion_window = 120
    
    lifecycle {
      delete_after = local.current_controls.backup_retention_days
      cold_storage_after = 30
    }
    
    recovery_point_tags = local.common_tags
  }
  
  tags = local.common_tags
}

# Data sources
data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

# Outputs
output "bucket_name" {
  description = "Name of the created S3 bucket"
  value       = aws_s3_bucket.data.id
}

output "bucket_arn" {
  description = "ARN of the created S3 bucket"
  value       = aws_s3_bucket.data.arn
}

output "encryption_key_id" {
  description = "ID of the KMS encryption key"
  value       = local.current_controls.kms_customer_managed ? aws_kms_key.data_encryption[0].key_id : null
}

output "data_access_role_arn" {
  description = "ARN of the data access role"
  value       = aws_iam_role.data_access.arn
}

output "protection_controls_applied" {
  description = "Summary of protection controls applied"
  value = {
    classification = var.data_classification
    encryption_required = local.current_controls.encryption_required
    kms_customer_managed = local.current_controls.kms_customer_managed
    mfa_required = local.current_controls.mfa_required
    access_logging = local.current_controls.access_logging
    backup_retention_days = local.current_controls.backup_retention_days
    cross_region_backup = local.current_controls.cross_region_backup
    monitoring_level = local.current_controls.monitoring_level
  }
}
```

## Relevant AWS Services

### Encryption Services
- **AWS Key Management Service (KMS)**: Customer-managed keys for sensitive data encryption
- **AWS CloudHSM**: Hardware security modules for highest security requirements
- **AWS Certificate Manager**: SSL/TLS certificates for encryption in transit

### Access Control Services
- **AWS Identity and Access Management (IAM)**: Fine-grained access control policies
- **AWS Single Sign-On (SSO)**: Centralized access management
- **Amazon Cognito**: User authentication and authorization
- **AWS Secrets Manager**: Secure storage and rotation of secrets

### Monitoring and Auditing Services
- **AWS CloudTrail**: API call logging and audit trails
- **Amazon GuardDuty**: Threat detection and security monitoring
- **Amazon Macie**: Data classification and sensitive data discovery
- **AWS Config**: Configuration compliance monitoring
- **AWS Security Hub**: Centralized security findings management

### Data Loss Prevention Services
- **Amazon Macie**: Content inspection and DLP capabilities
- **AWS Network Firewall**: Network-level content filtering
- **Amazon VPC**: Network segmentation and traffic control

### Backup and Recovery Services
- **AWS Backup**: Centralized backup across AWS services
- **Amazon S3 Cross-Region Replication**: Geographic data distribution
- **AWS Storage Gateway**: Hybrid cloud backup solutions

## Benefits of Classification-Based Protection Controls

### Security Benefits
- **Proportionate Protection**: Apply security controls appropriate to data sensitivity
- **Risk Reduction**: Reduce risk of data breaches through layered security
- **Compliance Support**: Meet regulatory requirements for data protection
- **Threat Detection**: Enhanced monitoring for sensitive data access

### Operational Benefits
- **Cost Optimization**: Avoid over-protecting low-sensitivity data
- **Automation**: Automated application of protection controls
- **Consistency**: Standardized protection across all data assets
- **Scalability**: Easily extend protection to new data assets

### Compliance Benefits
- **Regulatory Alignment**: Meet GDPR, HIPAA, PCI DSS requirements
- **Audit Readiness**: Comprehensive audit trails and documentation
- **Policy Enforcement**: Automated enforcement of data protection policies
- **Risk Management**: Clear documentation of protection measures

## Related Resources

- [AWS Well-Architected Framework - Data Classification](https://docs.aws.amazon.com/wellarchitected/latest/framework/sec_data_classification.html)
- [Amazon S3 Security Best Practices](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html)
- [AWS KMS Best Practices](https://docs.aws.amazon.com/kms/latest/developerguide/best-practices.html)
- [Amazon Macie User Guide](https://docs.aws.amazon.com/macie/latest/user/what-is-macie.html)
- [AWS Security Blog - Data Classification](https://aws.amazon.com/blogs/security/tag/data-classification/)
- [NIST Privacy Framework](https://www.nist.gov/privacy-framework)
```
