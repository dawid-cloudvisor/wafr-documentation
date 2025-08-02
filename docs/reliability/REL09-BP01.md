---
title: REL09-BP01 - Identify and back up all data that needs to be backed up, or reproduce the data from sources
layout: default
parent: REL09 - How do you back up data?
grand_parent: Reliability
nav_order: 1
---

# REL09-BP01: Identify and back up all data that needs to be backed up, or reproduce the data from sources

## Overview

Implement comprehensive data discovery and classification processes to identify all critical data assets that require backup protection. Establish clear data categorization based on business criticality, regulatory requirements, and recovery objectives to ensure complete data protection coverage.

## Implementation Steps

### 1. Conduct Data Discovery and Inventory
- Implement automated data discovery across all systems and services
- Create comprehensive data asset inventory and classification
- Identify data sources, dependencies, and relationships
- Establish data lineage and flow mapping

### 2. Classify Data by Criticality and Requirements
- Define data classification categories based on business impact
- Establish Recovery Time Objectives (RTO) and Recovery Point Objectives (RPO)
- Identify regulatory and compliance requirements for different data types
- Create data retention and lifecycle policies

### 3. Design Backup Strategies by Data Type
- Implement differentiated backup strategies based on data classification
- Design backup frequency and retention policies for each data category
- Establish cross-region and multi-tier backup approaches
- Configure backup validation and integrity checking

### 4. Implement Automated Data Discovery
- Configure continuous data discovery and classification updates
- Implement automated backup policy assignment based on data classification
- Design data change detection and backup triggering
- Establish data governance and policy enforcement

### 5. Create Data Reproducibility Framework
- Identify data that can be reproduced from authoritative sources
- Implement automated data regeneration and reconstruction processes
- Design source system integration and data pipeline automation
- Establish data quality validation and consistency checking

### 6. Monitor and Maintain Data Coverage
- Track backup coverage across all identified data assets
- Monitor data classification accuracy and completeness
- Implement continuous improvement based on data discovery insights
- Establish data protection gap analysis and remediation

## Implementation Examples

### Example 1: Comprehensive Data Discovery and Backup Management System
```python
import boto3
import json
import logging
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import re

class DataClassification(Enum):
    CRITICAL = "critical"
    IMPORTANT = "important"
    STANDARD = "standard"
    ARCHIVAL = "archival"

class DataType(Enum):
    DATABASE = "database"
    FILE_SYSTEM = "file_system"
    OBJECT_STORAGE = "object_storage"
    APPLICATION_DATA = "application_data"
    CONFIGURATION = "configuration"
    LOGS = "logs"

@dataclass
class DataAsset:
    asset_id: str
    name: str
    data_type: DataType
    classification: DataClassification
    location: str
    size_gb: float
    owner: str
    rto_hours: int
    rpo_hours: int
    backup_required: bool
    reproducible: bool
    source_systems: List[str]
    compliance_requirements: List[str]
    last_discovered: datetime

@dataclass
class BackupPolicy:
    policy_id: str
    name: str
    data_classification: DataClassification
    backup_frequency_hours: int
    retention_days: int
    cross_region_replication: bool
    encryption_required: bool
    validation_required: bool

class DataDiscoveryManager:
    """Comprehensive data discovery and backup management system"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
        # AWS clients
        self.s3 = boto3.client('s3')
        self.rds = boto3.client('rds')
        self.dynamodb_client = boto3.client('dynamodb')
        self.dynamodb = boto3.resource('dynamodb')
        self.efs = boto3.client('efs')
        self.ec2 = boto3.client('ec2')
        self.backup = boto3.client('backup')
        self.organizations = boto3.client('organizations')
        
        # Storage
        self.assets_table = self.dynamodb.Table(config.get('assets_table', 'data-assets'))
        self.policies_table = self.dynamodb.Table(config.get('policies_table', 'backup-policies'))
        
        # Configuration
        self.discovery_rules = config.get('discovery_rules', {})
        self.classification_rules = config.get('classification_rules', {})
        
        # Discovered assets
        self.discovered_assets = {}
        
    async def discover_all_data_assets(self) -> List[DataAsset]:
        """Discover all data assets across AWS services"""
        try:
            all_assets = []
            
            # Discover S3 data
            s3_assets = await self._discover_s3_assets()
            all_assets.extend(s3_assets)
            
            # Discover RDS databases
            rds_assets = await self._discover_rds_assets()
            all_assets.extend(rds_assets)
            
            # Discover DynamoDB tables
            dynamodb_assets = await self._discover_dynamodb_assets()
            all_assets.extend(dynamodb_assets)
            
            # Discover EFS file systems
            efs_assets = await self._discover_efs_assets()
            all_assets.extend(efs_assets)
            
            # Discover EBS volumes
            ebs_assets = await self._discover_ebs_assets()
            all_assets.extend(ebs_assets)
            
            # Store discovered assets
            for asset in all_assets:
                await self._store_data_asset(asset)
                self.discovered_assets[asset.asset_id] = asset
            
            logging.info(f"Discovered {len(all_assets)} data assets")
            return all_assets
            
        except Exception as e:
            logging.error(f"Failed to discover data assets: {str(e)}")
            return []
    
    async def _discover_s3_assets(self) -> List[DataAsset]:
        """Discover S3 bucket assets"""
        try:
            assets = []
            
            # List all S3 buckets
            response = self.s3.list_buckets()
            
            for bucket in response['Buckets']:
                bucket_name = bucket['Name']
                
                try:
                    # Get bucket size and object count
                    size_info = await self._get_s3_bucket_size(bucket_name)
                    
                    # Get bucket tags for classification
                    tags = await self._get_s3_bucket_tags(bucket_name)
                    
                    # Classify bucket based on tags and naming patterns
                    classification = self._classify_s3_bucket(bucket_name, tags)
                    
                    # Determine if backup is required
                    backup_required = self._should_backup_s3_bucket(bucket_name, tags, classification)
                    
                    # Check if data is reproducible
                    reproducible = self._is_s3_data_reproducible(bucket_name, tags)
                    
                    # Get compliance requirements
                    compliance_reqs = self._get_compliance_requirements(tags, classification)
                    
                    # Create data asset
                    asset = DataAsset(
                        asset_id=f"s3_{bucket_name}",
                        name=bucket_name,
                        data_type=DataType.OBJECT_STORAGE,
                        classification=classification,
                        location=f"s3://{bucket_name}",
                        size_gb=size_info['size_gb'],
                        owner=tags.get('Owner', 'unknown'),
                        rto_hours=self._get_rto_for_classification(classification),
                        rpo_hours=self._get_rpo_for_classification(classification),
                        backup_required=backup_required,
                        reproducible=reproducible,
                        source_systems=self._identify_source_systems(tags),
                        compliance_requirements=compliance_reqs,
                        last_discovered=datetime.utcnow()
                    )
                    
                    assets.append(asset)
                    
                except Exception as bucket_error:
                    logging.warning(f"Failed to analyze S3 bucket {bucket_name}: {str(bucket_error)}")
                    continue
            
            return assets
            
        except Exception as e:
            logging.error(f"Failed to discover S3 assets: {str(e)}")
            return []
    
    async def _discover_rds_assets(self) -> List[DataAsset]:
        """Discover RDS database assets"""
        try:
            assets = []
            
            # List all RDS instances
            response = self.rds.describe_db_instances()
            
            for db_instance in response['DBInstances']:
                db_identifier = db_instance['DBInstanceIdentifier']
                
                try:
                    # Get database size
                    size_gb = db_instance.get('AllocatedStorage', 0)
                    
                    # Get database tags
                    tags_response = self.rds.list_tags_for_resource(
                        ResourceName=db_instance['DBInstanceArn']
                    )
                    tags = {tag['Key']: tag['Value'] for tag in tags_response['TagList']}
                    
                    # Classify database
                    classification = self._classify_rds_database(db_identifier, tags, db_instance)
                    
                    # Determine backup requirements
                    backup_required = True  # RDS databases typically require backup
                    reproducible = self._is_rds_data_reproducible(db_identifier, tags)
                    
                    # Create data asset
                    asset = DataAsset(
                        asset_id=f"rds_{db_identifier}",
                        name=db_identifier,
                        data_type=DataType.DATABASE,
                        classification=classification,
                        location=f"rds://{db_identifier}",
                        size_gb=float(size_gb),
                        owner=tags.get('Owner', 'unknown'),
                        rto_hours=self._get_rto_for_classification(classification),
                        rpo_hours=self._get_rpo_for_classification(classification),
                        backup_required=backup_required,
                        reproducible=reproducible,
                        source_systems=self._identify_source_systems(tags),
                        compliance_requirements=self._get_compliance_requirements(tags, classification),
                        last_discovered=datetime.utcnow()
                    )
                    
                    assets.append(asset)
                    
                except Exception as db_error:
                    logging.warning(f"Failed to analyze RDS instance {db_identifier}: {str(db_error)}")
                    continue
            
            return assets
            
        except Exception as e:
            logging.error(f"Failed to discover RDS assets: {str(e)}")
            return []
    
    async def _discover_dynamodb_assets(self) -> List[DataAsset]:
        """Discover DynamoDB table assets"""
        try:
            assets = []
            
            # List all DynamoDB tables
            response = self.dynamodb_client.list_tables()
            
            for table_name in response['TableNames']:
                try:
                    # Get table details
                    table_response = self.dynamodb_client.describe_table(TableName=table_name)
                    table = table_response['Table']
                    
                    # Get table size
                    size_gb = table.get('TableSizeBytes', 0) / (1024**3)
                    
                    # Get table tags
                    tags_response = self.dynamodb_client.list_tags_of_resource(
                        ResourceArn=table['TableArn']
                    )
                    tags = {tag['Key']: tag['Value'] for tag in tags_response['Tags']}
                    
                    # Classify table
                    classification = self._classify_dynamodb_table(table_name, tags, table)
                    
                    # Determine backup requirements
                    backup_required = True  # DynamoDB tables typically require backup
                    reproducible = self._is_dynamodb_data_reproducible(table_name, tags)
                    
                    # Create data asset
                    asset = DataAsset(
                        asset_id=f"dynamodb_{table_name}",
                        name=table_name,
                        data_type=DataType.DATABASE,
                        classification=classification,
                        location=f"dynamodb://{table_name}",
                        size_gb=size_gb,
                        owner=tags.get('Owner', 'unknown'),
                        rto_hours=self._get_rto_for_classification(classification),
                        rpo_hours=self._get_rpo_for_classification(classification),
                        backup_required=backup_required,
                        reproducible=reproducible,
                        source_systems=self._identify_source_systems(tags),
                        compliance_requirements=self._get_compliance_requirements(tags, classification),
                        last_discovered=datetime.utcnow()
                    )
                    
                    assets.append(asset)
                    
                except Exception as table_error:
                    logging.warning(f"Failed to analyze DynamoDB table {table_name}: {str(table_error)}")
                    continue
            
            return assets
            
        except Exception as e:
            logging.error(f"Failed to discover DynamoDB assets: {str(e)}")
            return []
    
    async def _get_s3_bucket_size(self, bucket_name: str) -> Dict[str, Any]:
        """Get S3 bucket size information"""
        try:
            # Use CloudWatch metrics to get bucket size
            from datetime import datetime, timedelta
            
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(days=2)
            
            # This is simplified - in practice, you'd use CloudWatch metrics
            # For now, we'll return a placeholder
            return {'size_gb': 10.0, 'object_count': 1000}
            
        except Exception as e:
            logging.warning(f"Failed to get S3 bucket size for {bucket_name}: {str(e)}")
            return {'size_gb': 0.0, 'object_count': 0}
    
    async def _get_s3_bucket_tags(self, bucket_name: str) -> Dict[str, str]:
        """Get S3 bucket tags"""
        try:
            response = self.s3.get_bucket_tagging(Bucket=bucket_name)
            return {tag['Key']: tag['Value'] for tag in response['TagSet']}
        except Exception:
            return {}
    
    def _classify_s3_bucket(self, bucket_name: str, tags: Dict[str, str]) -> DataClassification:
        """Classify S3 bucket based on naming patterns and tags"""
        try:
            # Check explicit classification tag
            if 'DataClassification' in tags:
                return DataClassification(tags['DataClassification'].lower())
            
            # Check naming patterns
            if any(pattern in bucket_name.lower() for pattern in ['prod', 'production', 'critical']):
                return DataClassification.CRITICAL
            elif any(pattern in bucket_name.lower() for pattern in ['backup', 'archive']):
                return DataClassification.ARCHIVAL
            elif any(pattern in bucket_name.lower() for pattern in ['log', 'temp', 'cache']):
                return DataClassification.STANDARD
            else:
                return DataClassification.IMPORTANT
                
        except Exception as e:
            logging.warning(f"Failed to classify S3 bucket {bucket_name}: {str(e)}")
            return DataClassification.STANDARD
    
    def _classify_rds_database(self, db_identifier: str, tags: Dict[str, str], 
                             db_instance: Dict[str, Any]) -> DataClassification:
        """Classify RDS database"""
        try:
            # Check explicit classification tag
            if 'DataClassification' in tags:
                return DataClassification(tags['DataClassification'].lower())
            
            # Check environment tags
            environment = tags.get('Environment', '').lower()
            if environment in ['prod', 'production']:
                return DataClassification.CRITICAL
            elif environment in ['staging', 'test']:
                return DataClassification.IMPORTANT
            else:
                return DataClassification.STANDARD
                
        except Exception as e:
            logging.warning(f"Failed to classify RDS database {db_identifier}: {str(e)}")
            return DataClassification.IMPORTANT
    
    def _classify_dynamodb_table(self, table_name: str, tags: Dict[str, str], 
                                table: Dict[str, Any]) -> DataClassification:
        """Classify DynamoDB table"""
        try:
            # Check explicit classification tag
            if 'DataClassification' in tags:
                return DataClassification(tags['DataClassification'].lower())
            
            # Check table name patterns
            if any(pattern in table_name.lower() for pattern in ['prod', 'production']):
                return DataClassification.CRITICAL
            elif any(pattern in table_name.lower() for pattern in ['user', 'customer', 'order']):
                return DataClassification.IMPORTANT
            else:
                return DataClassification.STANDARD
                
        except Exception as e:
            logging.warning(f"Failed to classify DynamoDB table {table_name}: {str(e)}")
            return DataClassification.STANDARD
    
    def _should_backup_s3_bucket(self, bucket_name: str, tags: Dict[str, str], 
                               classification: DataClassification) -> bool:
        """Determine if S3 bucket should be backed up"""
        try:
            # Check explicit backup tag
            if 'BackupRequired' in tags:
                return tags['BackupRequired'].lower() == 'true'
            
            # Check if it's a backup bucket itself
            if any(pattern in bucket_name.lower() for pattern in ['backup', 'archive', 'snapshot']):
                return False
            
            # Check if it's temporary data
            if any(pattern in bucket_name.lower() for pattern in ['temp', 'cache', 'log']):
                return False
            
            # Backup based on classification
            return classification in [DataClassification.CRITICAL, DataClassification.IMPORTANT]
            
        except Exception as e:
            logging.warning(f"Failed to determine backup requirement for {bucket_name}: {str(e)}")
            return True
    
    def _is_s3_data_reproducible(self, bucket_name: str, tags: Dict[str, str]) -> bool:
        """Check if S3 data can be reproduced from sources"""
        try:
            # Check explicit reproducible tag
            if 'Reproducible' in tags:
                return tags['Reproducible'].lower() == 'true'
            
            # Check if it's derived data
            if any(pattern in bucket_name.lower() for pattern in ['processed', 'derived', 'report', 'analytics']):
                return True
            
            # Check if it's log data
            if 'log' in bucket_name.lower():
                return True
            
            return False
            
        except Exception as e:
            logging.warning(f"Failed to determine reproducibility for {bucket_name}: {str(e)}")
            return False
    
    def _is_rds_data_reproducible(self, db_identifier: str, tags: Dict[str, str]) -> bool:
        """Check if RDS data can be reproduced"""
        try:
            # Check explicit reproducible tag
            if 'Reproducible' in tags:
                return tags['Reproducible'].lower() == 'true'
            
            # Most database data is not easily reproducible
            return False
            
        except Exception as e:
            logging.warning(f"Failed to determine reproducibility for {db_identifier}: {str(e)}")
            return False
    
    def _is_dynamodb_data_reproducible(self, table_name: str, tags: Dict[str, str]) -> bool:
        """Check if DynamoDB data can be reproduced"""
        try:
            # Check explicit reproducible tag
            if 'Reproducible' in tags:
                return tags['Reproducible'].lower() == 'true'
            
            # Check if it's cache or session data
            if any(pattern in table_name.lower() for pattern in ['cache', 'session', 'temp']):
                return True
            
            return False
            
        except Exception as e:
            logging.warning(f"Failed to determine reproducibility for {table_name}: {str(e)}")
            return False
    
    def _get_rto_for_classification(self, classification: DataClassification) -> int:
        """Get RTO hours based on data classification"""
        rto_mapping = {
            DataClassification.CRITICAL: 1,    # 1 hour
            DataClassification.IMPORTANT: 4,   # 4 hours
            DataClassification.STANDARD: 24,   # 24 hours
            DataClassification.ARCHIVAL: 72    # 72 hours
        }
        return rto_mapping.get(classification, 24)
    
    def _get_rpo_for_classification(self, classification: DataClassification) -> int:
        """Get RPO hours based on data classification"""
        rpo_mapping = {
            DataClassification.CRITICAL: 1,    # 1 hour
            DataClassification.IMPORTANT: 4,   # 4 hours
            DataClassification.STANDARD: 24,   # 24 hours
            DataClassification.ARCHIVAL: 168   # 1 week
        }
        return rpo_mapping.get(classification, 24)
    
    def _identify_source_systems(self, tags: Dict[str, str]) -> List[str]:
        """Identify source systems from tags"""
        source_systems = []
        
        if 'SourceSystem' in tags:
            source_systems.append(tags['SourceSystem'])
        
        if 'Application' in tags:
            source_systems.append(tags['Application'])
        
        return source_systems
    
    def _get_compliance_requirements(self, tags: Dict[str, str], 
                                   classification: DataClassification) -> List[str]:
        """Get compliance requirements based on tags and classification"""
        requirements = []
        
        if 'ComplianceRequirement' in tags:
            requirements.extend(tags['ComplianceRequirement'].split(','))
        
        # Add default requirements based on classification
        if classification == DataClassification.CRITICAL:
            requirements.extend(['SOX', 'PCI-DSS'])
        
        return list(set(requirements))  # Remove duplicates
    
    async def create_backup_policies(self) -> List[BackupPolicy]:
        """Create backup policies based on data classifications"""
        try:
            policies = []
            
            # Critical data policy
            critical_policy = BackupPolicy(
                policy_id='critical_data_policy',
                name='Critical Data Backup Policy',
                data_classification=DataClassification.CRITICAL,
                backup_frequency_hours=4,  # Every 4 hours
                retention_days=2555,       # 7 years
                cross_region_replication=True,
                encryption_required=True,
                validation_required=True
            )
            policies.append(critical_policy)
            
            # Important data policy
            important_policy = BackupPolicy(
                policy_id='important_data_policy',
                name='Important Data Backup Policy',
                data_classification=DataClassification.IMPORTANT,
                backup_frequency_hours=12,  # Every 12 hours
                retention_days=1095,        # 3 years
                cross_region_replication=True,
                encryption_required=True,
                validation_required=True
            )
            policies.append(important_policy)
            
            # Standard data policy
            standard_policy = BackupPolicy(
                policy_id='standard_data_policy',
                name='Standard Data Backup Policy',
                data_classification=DataClassification.STANDARD,
                backup_frequency_hours=24,  # Daily
                retention_days=365,         # 1 year
                cross_region_replication=False,
                encryption_required=True,
                validation_required=False
            )
            policies.append(standard_policy)
            
            # Archival data policy
            archival_policy = BackupPolicy(
                policy_id='archival_data_policy',
                name='Archival Data Backup Policy',
                data_classification=DataClassification.ARCHIVAL,
                backup_frequency_hours=168,  # Weekly
                retention_days=3650,         # 10 years
                cross_region_replication=False,
                encryption_required=True,
                validation_required=False
            )
            policies.append(archival_policy)
            
            # Store policies
            for policy in policies:
                await self._store_backup_policy(policy)
            
            logging.info(f"Created {len(policies)} backup policies")
            return policies
            
        except Exception as e:
            logging.error(f"Failed to create backup policies: {str(e)}")
            return []
    
    async def assign_backup_policies(self, assets: List[DataAsset]) -> Dict[str, str]:
        """Assign backup policies to data assets"""
        try:
            assignments = {}
            
            for asset in assets:
                if not asset.backup_required:
                    continue
                
                # Assign policy based on classification
                policy_id = f"{asset.classification.value}_data_policy"
                assignments[asset.asset_id] = policy_id
                
                # Update asset with policy assignment
                asset_dict = asdict(asset)
                asset_dict['backup_policy_id'] = policy_id
                asset_dict['last_discovered'] = asset.last_discovered.isoformat()
                
                self.assets_table.put_item(Item=asset_dict)
            
            logging.info(f"Assigned backup policies to {len(assignments)} assets")
            return assignments
            
        except Exception as e:
            logging.error(f"Failed to assign backup policies: {str(e)}")
            return {}
    
    async def _store_data_asset(self, asset: DataAsset):
        """Store data asset in DynamoDB"""
        try:
            asset_dict = asdict(asset)
            asset_dict['last_discovered'] = asset.last_discovered.isoformat()
            
            self.assets_table.put_item(Item=asset_dict)
            
        except Exception as e:
            logging.error(f"Failed to store data asset: {str(e)}")
    
    async def _store_backup_policy(self, policy: BackupPolicy):
        """Store backup policy in DynamoDB"""
        try:
            policy_dict = asdict(policy)
            self.policies_table.put_item(Item=policy_dict)
            
        except Exception as e:
            logging.error(f"Failed to store backup policy: {str(e)}")

# Usage example
async def main():
    config = {
        'assets_table': 'data-assets',
        'policies_table': 'backup-policies',
        'discovery_rules': {},
        'classification_rules': {}
    }
    
    # Initialize data discovery manager
    discovery_manager = DataDiscoveryManager(config)
    
    # Discover all data assets
    assets = await discovery_manager.discover_all_data_assets()
    print(f"Discovered {len(assets)} data assets")
    
    # Create backup policies
    policies = await discovery_manager.create_backup_policies()
    print(f"Created {len(policies)} backup policies")
    
    # Assign policies to assets
    assignments = await discovery_manager.assign_backup_policies(assets)
    print(f"Assigned policies to {len(assignments)} assets")
    
    # Print summary by classification
    classification_summary = {}
    for asset in assets:
        classification = asset.classification.value
        if classification not in classification_summary:
            classification_summary[classification] = {'count': 0, 'total_size_gb': 0}
        classification_summary[classification]['count'] += 1
        classification_summary[classification]['total_size_gb'] += asset.size_gb
    
    print("\nData Asset Summary by Classification:")
    for classification, summary in classification_summary.items():
        print(f"- {classification}: {summary['count']} assets, {summary['total_size_gb']:.2f} GB")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## AWS Services Used

- **AWS Backup**: Centralized backup service for cross-service data protection
- **Amazon S3**: Object storage with lifecycle policies and cross-region replication
- **Amazon RDS**: Database backup with automated snapshots and point-in-time recovery
- **Amazon DynamoDB**: NoSQL database with point-in-time recovery and on-demand backup
- **Amazon EFS**: File system backup with automatic and manual snapshots
- **Amazon EBS**: Block storage snapshots with lifecycle management
- **AWS Organizations**: Multi-account data discovery and governance
- **AWS Config**: Resource inventory and configuration tracking
- **Amazon CloudWatch**: Metrics collection for storage utilization and backup monitoring
- **AWS CloudTrail**: Audit logging for data access and backup operations
- **AWS Systems Manager**: Parameter management for backup configurations
- **AWS Lambda**: Custom data discovery and classification automation
- **Amazon EventBridge**: Event-driven backup policy enforcement
- **AWS Step Functions**: Complex data discovery workflow orchestration
- **AWS Glue**: Data catalog and metadata management for discovery

## Benefits

- **Complete Coverage**: Comprehensive discovery ensures no critical data is missed
- **Risk-Based Protection**: Data classification enables appropriate protection levels
- **Cost Optimization**: Differentiated backup strategies optimize storage costs
- **Compliance Assurance**: Automated classification supports regulatory requirements
- **Operational Efficiency**: Automated discovery reduces manual inventory management
- **Data Governance**: Centralized data asset management and policy enforcement
- **Recovery Planning**: Clear RTO/RPO objectives enable effective disaster recovery
- **Source Integration**: Reproducible data strategies reduce backup storage requirements
- **Continuous Monitoring**: Ongoing discovery maintains accurate data inventory
- **Policy Automation**: Automated policy assignment ensures consistent protection

## Related Resources

- [AWS Well-Architected Reliability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/)
- [Identify and Back Up Data](https://docs.aws.amazon.com/wellarchitected/latest/framework/rel_back_up_data_identify_all_data.html)
- [AWS Backup User Guide](https://docs.aws.amazon.com/aws-backup/latest/devguide/)
- [Amazon S3 User Guide](https://docs.aws.amazon.com/s3/latest/userguide/)
- [Amazon RDS User Guide](https://docs.aws.amazon.com/rds/latest/userguide/)
- [Amazon DynamoDB Developer Guide](https://docs.aws.amazon.com/dynamodb/latest/developerguide/)
- [Amazon EFS User Guide](https://docs.aws.amazon.com/efs/latest/ug/)
- [Amazon EBS User Guide](https://docs.aws.amazon.com/ebs/latest/userguide/)
- [AWS Config Developer Guide](https://docs.aws.amazon.com/config/latest/developerguide/)
- [Data Classification Best Practices](https://aws.amazon.com/architecture/well-architected/)
- [Backup Strategy Planning](https://aws.amazon.com/backup-recovery/)
- [Data Governance on AWS](https://aws.amazon.com/big-data/datalakes-and-analytics/)
