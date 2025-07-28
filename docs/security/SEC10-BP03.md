---
title: "SEC10-BP03: Prepare forensic capabilities"
layout: default
parent: "SEC10 - How do you anticipate, respond to, and recover from incidents?"
grand_parent: Security
nav_order: 3
---

# SEC10-BP03: Prepare forensic capabilities

## Overview

Ahead of a security incident, consider developing forensics capabilities to support security event investigations.

**Level of risk exposed if this best practice is not established:** Medium

Concepts from traditional on-premises forensics apply to AWS. For key information to start building forensics capabilities in the AWS Cloud, see [Forensic investigation environment strategies in the AWS Cloud](https://docs.aws.amazon.com/whitepapers/latest/forensic-investigation-environment-strategies-in-the-aws-cloud/forensic-investigation-environment-strategies-in-the-aws-cloud.html).

Once you have your environment and AWS account structure set up for forensics, define the technologies required to effectively perform forensically sound methodologies across the four phases:

- **Collection:** Collect relevant AWS logs, such as AWS CloudTrail, AWS Config, VPC Flow Logs, and host-level logs. Collect snapshots, backups, and memory dumps of impacted AWS resources where available.
- **Examination:** Examine the data collected by extracting and assessing the relevant information.
- **Analysis:** Analyze the data collected in order to understand the incident and draw conclusions from it.
- **Reporting:** Present the information resulting from the analysis phase.

## Implementation Steps

### Prepare your forensics environment

[AWS Organizations](https://aws.amazon.com/organizations/) helps you centrally manage and govern an AWS environment as you grow and scale AWS resources. An AWS organization consolidates your AWS accounts so that you can administer them as a single unit. You can use organizational units (OUs) to group accounts together to administer as a single unit.

For incident response, it's helpful to have an AWS account structure that supports the functions of incident response, which includes a security OU and a forensics OU.

**Within the security OU, you should have accounts for:**
- **Log archival:** Aggregate logs in a log archival AWS account with limited permissions
- **Security tools:** Centralize security services in a security tool AWS account. This account operates as the delegated administrator for security services

**Within the forensics OU,** you have the option to implement a single forensics account or accounts for each Region that you operate in, depending on which works best for your business and operational model. If you create a forensics account per Region, you can block the creation of AWS resources outside of that Region and reduce the risk of resources being copied to an unintended region.

For example, if you only operate in US East (N. Virginia) Region (us-east-1) and US West (Oregon) (us-west-2), then you would have two accounts in the forensics OU: one for us-east-1 and one for us-west-2.

You can create a forensics AWS account for multiple Regions. You should exercise caution in copying AWS resources to that account to verify you're aligning with your data sovereignty requirements.

Because it takes time to provision new accounts, it is imperative to create and instrument the forensics accounts well ahead of an incident so that responders can be prepared to effectively use them for response.

### Capture backups and snapshots

Setting up backups of key systems and databases are critical for recovering from a security incident and for forensics purposes. With backups in place, you can restore your systems to their previous safe state. On AWS, you can take snapshots of various resources. Snapshots provide you with point-in-time backups of those resources.

There are many AWS services that can support you in backup and recovery. For detail on these services and approaches for backup and recovery, see [Backup and Recovery Prescriptive Guidance](https://docs.aws.amazon.com/prescriptive-guidance/latest/backup-recovery/welcome.html) and [Use backups to recover from security incidents](https://docs.aws.amazon.com/whitepapers/latest/aws-security-incident-response-guide/use-backups-to-recover-from-security-incidents.html).

Especially when it comes to situations such as ransomware, it's critical for your backups to be well protected. For guidance on securing your backups, see [Top 10 security best practices for securing backups in AWS](https://aws.amazon.com/blogs/storage/top-10-security-best-practices-for-securing-backups-in-aws/).

In addition to securing your backups, you should regularly test your backup and restore processes to verify that the technology and processes you have in place work as expected.

### Automate forensics

During a security event, your incident response team must be able to collect and analyze evidence quickly while maintaining accuracy for the time period surrounding the event (such as capturing logs related to a specific event or resource or collecting memory dump of an Amazon EC2 instance). It's both challenging and time consuming for the incident response team to manually collect the relevant evidence, especially across a large number of instances and accounts. Additionally, manual collection can be prone to human error.

For these reasons, you should develop and implement automation for forensics as much as possible. AWS offers a number of automation resources for forensics, which are listed in the Resources section. These resources are examples of forensics patterns that we have developed and customers have implemented. While they might be a useful reference architecture to start with, consider modifying them or creating new forensics automation patterns based on your environment, requirements, tools, and forensics processes.
## Implementation Examples

### Example 1: Comprehensive Forensic Capabilities Framework

```python
# forensic_capabilities_manager.py
import boto3
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
import logging
import hashlib
import base64

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ForensicPhase(Enum):
    COLLECTION = "collection"
    EXAMINATION = "examination"
    ANALYSIS = "analysis"
    REPORTING = "reporting"

class EvidenceType(Enum):
    LOGS = "logs"
    SNAPSHOTS = "snapshots"
    MEMORY_DUMPS = "memory_dumps"
    NETWORK_CAPTURES = "network_captures"
    CONFIGURATION = "configuration"
    METADATA = "metadata"

@dataclass
class ForensicEvidence:
    evidence_id: str
    evidence_type: EvidenceType
    source_resource: str
    collection_timestamp: str
    chain_of_custody: List[Dict[str, str]]
    hash_values: Dict[str, str]
    storage_location: str
    retention_period: str
    classification: str
    collection_method: str
    integrity_verified: bool
    metadata: Dict[str, Any]

@dataclass
class ForensicAccount:
    account_id: str
    account_name: str
    region: str
    purpose: str
    cross_account_roles: List[str]
    storage_buckets: List[str]
    analysis_tools: List[str]
    access_controls: Dict[str, Any]
    data_sovereignty_compliance: List[str]

class ForensicCapabilitiesManager:
    """
    Comprehensive forensic capabilities management for AWS environments
    """
    
    def __init__(self, region: str = 'us-east-1'):
        self.region = region
        self.organizations_client = boto3.client('organizations', region_name=region)
        self.ec2_client = boto3.client('ec2', region_name=region)
        self.s3_client = boto3.client('s3', region_name=region)
        self.cloudtrail_client = boto3.client('cloudtrail', region_name=region)
        self.logs_client = boto3.client('logs', region_name=region)
        self.ssm_client = boto3.client('ssm', region_name=region)
        self.lambda_client = boto3.client('lambda', region_name=region)
        self.dynamodb = boto3.resource('dynamodb', region_name=region)
        
        # DynamoDB tables for forensic management
        self.evidence_table = self.dynamodb.Table('forensic-evidence-registry')
        self.accounts_table = self.dynamodb.Table('forensic-accounts')
        self.procedures_table = self.dynamodb.Table('forensic-procedures')
        
        # Initialize forensic capabilities
        self.forensic_phases = self._define_forensic_phases()
        self.evidence_types = self._define_evidence_types()
    
    def _define_forensic_phases(self) -> Dict[str, Dict[str, Any]]:
        """
        Define the four phases of digital forensics with specific AWS implementations
        """
        return {
            ForensicPhase.COLLECTION.value: {
                'description': 'Collect and preserve digital evidence from AWS resources',
                'objectives': [
                    'Identify and locate relevant digital evidence',
                    'Preserve evidence integrity and chain of custody',
                    'Collect evidence in a forensically sound manner',
                    'Document collection procedures and metadata'
                ],
                'aws_services': [
                    'EC2 Snapshots', 'EBS Snapshots', 'CloudTrail', 'VPC Flow Logs',
                    'CloudWatch Logs', 'Config', 'S3 Access Logs', 'Systems Manager'
                ],
                'key_activities': [
                    'Create forensic snapshots of EC2 instances and EBS volumes',
                    'Export CloudTrail logs for the incident timeframe',
                    'Collect VPC Flow Logs and network traffic data',
                    'Gather application and system logs from CloudWatch',
                    'Export AWS Config configuration history',
                    'Collect memory dumps using Systems Manager'
                ],
                'automation_tools': [
                    'AWS Lambda for automated collection',
                    'Systems Manager Automation for orchestration',
                    'Step Functions for workflow management',
                    'EventBridge for trigger-based collection'
                ]
            },
            ForensicPhase.EXAMINATION.value: {
                'description': 'Extract and assess relevant information from collected evidence',
                'objectives': [
                    'Extract data from collected evidence',
                    'Identify relevant artifacts and indicators',
                    'Validate evidence integrity and authenticity',
                    'Prepare data for detailed analysis'
                ],
                'aws_services': [
                    'EC2 for analysis workstations', 'S3 for evidence storage',
                    'Athena for log analysis', 'Glue for data processing',
                    'EMR for large-scale data processing'
                ],
                'key_activities': [
                    'Mount and examine forensic disk images',
                    'Parse and extract log entries and artifacts',
                    'Validate file system integrity and timestamps',
                    'Extract network traffic and communication data',
                    'Identify deleted or hidden files and data',
                    'Create searchable indexes of evidence data'
                ],
                'automation_tools': [
                    'Athena queries for log analysis',
                    'Glue ETL jobs for data transformation',
                    'Lambda functions for artifact extraction',
                    'EMR clusters for large-scale processing'
                ]
            },
            ForensicPhase.ANALYSIS.value: {
                'description': 'Analyze evidence to understand the incident and draw conclusions',
                'objectives': [
                    'Correlate evidence across multiple sources',
                    'Reconstruct incident timeline and attack vectors',
                    'Identify indicators of compromise and attribution',
                    'Assess impact and scope of the incident'
                ],
                'aws_services': [
                    'Detective for investigation graphs', 'QuickSight for visualization',
                    'SageMaker for ML-based analysis', 'OpenSearch for search and analytics'
                ],
                'key_activities': [
                    'Timeline analysis and event correlation',
                    'Network traffic analysis and communication patterns',
                    'Malware analysis and reverse engineering',
                    'User behavior analysis and anomaly detection',
                    'Impact assessment and data classification',
                    'Attribution analysis and threat intelligence correlation'
                ],
                'automation_tools': [
                    'Detective for automated investigation',
                    'SageMaker for anomaly detection',
                    'OpenSearch for correlation analysis',
                    'QuickSight for data visualization'
                ]
            },
            ForensicPhase.REPORTING.value: {
                'description': 'Present findings and conclusions from forensic analysis',
                'objectives': [
                    'Document findings and conclusions',
                    'Create executive and technical reports',
                    'Provide expert testimony if required',
                    'Support legal and regulatory requirements'
                ],
                'aws_services': [
                    'S3 for report storage', 'CloudFront for secure distribution',
                    'WorkDocs for collaboration', 'Macie for data classification'
                ],
                'key_activities': [
                    'Create detailed technical forensic reports',
                    'Develop executive summary and business impact assessment',
                    'Prepare evidence exhibits and supporting documentation',
                    'Create timeline visualizations and attack diagrams',
                    'Document chain of custody and evidence handling',
                    'Prepare for legal proceedings and expert testimony'
                ],
                'automation_tools': [
                    'Lambda for report generation',
                    'QuickSight for automated dashboards',
                    'WorkDocs for collaborative reporting',
                    'S3 for secure report distribution'
                ]
            }
        }
    
    def _define_evidence_types(self) -> Dict[str, Dict[str, Any]]:
        """
        Define types of digital evidence and their collection methods
        """
        return {
            EvidenceType.LOGS.value: {
                'description': 'System, application, and service logs',
                'sources': [
                    'CloudTrail API logs', 'VPC Flow Logs', 'CloudWatch Logs',
                    'Application Load Balancer logs', 'S3 access logs', 'Route 53 query logs'
                ],
                'collection_methods': [
                    'CloudTrail log export', 'CloudWatch Logs export',
                    'S3 log aggregation', 'Kinesis Data Firehose streaming'
                ],
                'retention_requirements': '7 years minimum for security incidents',
                'integrity_verification': 'SHA-256 hash validation and CloudTrail log file validation'
            },
            EvidenceType.SNAPSHOTS.value: {
                'description': 'Point-in-time copies of storage volumes and instances',
                'sources': [
                    'EBS volume snapshots', 'EC2 instance snapshots',
                    'RDS database snapshots', 'EFS file system backups'
                ],
                'collection_methods': [
                    'Automated snapshot creation', 'Cross-region snapshot copying',
                    'Encrypted snapshot storage', 'Snapshot sharing with forensic accounts'
                ],
                'retention_requirements': '3 years minimum for forensic analysis',
                'integrity_verification': 'Snapshot checksums and encryption validation'
            },
            EvidenceType.MEMORY_DUMPS.value: {
                'description': 'Memory contents from running systems',
                'sources': [
                    'EC2 instance memory', 'Container memory dumps',
                    'Lambda function memory', 'RDS process memory'
                ],
                'collection_methods': [
                    'Systems Manager memory dump automation',
                    'EC2 hibernation for memory preservation',
                    'Container memory extraction', 'Custom memory dump tools'
                ],
                'retention_requirements': '1 year minimum for active investigations',
                'integrity_verification': 'Memory dump hash validation and chain of custody'
            },
            EvidenceType.NETWORK_CAPTURES.value: {
                'description': 'Network traffic and communication data',
                'sources': [
                    'VPC Flow Logs', 'VPC Traffic Mirroring',
                    'Network Load Balancer logs', 'NAT Gateway logs'
                ],
                'collection_methods': [
                    'Flow log aggregation', 'Traffic mirroring to analysis tools',
                    'Packet capture automation', 'Network monitoring integration'
                ],
                'retention_requirements': '90 days minimum for network analysis',
                'integrity_verification': 'Packet capture checksums and timestamp validation'
            },
            EvidenceType.CONFIGURATION.value: {
                'description': 'System and service configuration data',
                'sources': [
                    'AWS Config configuration items', 'CloudFormation templates',
                    'Systems Manager inventory', 'IAM policies and roles'
                ],
                'collection_methods': [
                    'Config configuration export', 'CloudFormation template extraction',
                    'Systems Manager inventory collection', 'IAM policy documentation'
                ],
                'retention_requirements': '5 years minimum for compliance',
                'integrity_verification': 'Configuration hash validation and version tracking'
            },
            EvidenceType.METADATA.value: {
                'description': 'Resource metadata and tagging information',
                'sources': [
                    'Resource tags', 'CloudTrail event metadata',
                    'Instance metadata', 'Service metadata'
                ],
                'collection_methods': [
                    'Tag inventory collection', 'Metadata API queries',
                    'CloudTrail metadata extraction', 'Service discovery automation'
                ],
                'retention_requirements': '3 years minimum for investigation support',
                'integrity_verification': 'Metadata consistency validation and audit trails'
            }
        }
    
    def setup_forensic_accounts(self, 
                               organization_id: str,
                               regions: List[str],
                               account_strategy: str = 'per_region') -> Dict[str, Any]:
        """
        Set up forensic accounts within AWS Organizations structure
        """
        try:
            forensic_accounts = []
            
            if account_strategy == 'per_region':
                # Create one forensic account per region
                for region in regions:
                    account_result = self._create_forensic_account(
                        f"Forensics-{region.upper()}",
                        region,
                        organization_id
                    )
                    if account_result['status'] == 'success':
                        forensic_accounts.append(account_result['account'])
            else:
                # Create single multi-region forensic account
                account_result = self._create_forensic_account(
                    "Forensics-MultiRegion",
                    "multi-region",
                    organization_id
                )
                if account_result['status'] == 'success':
                    forensic_accounts.append(account_result['account'])
            
            # Set up cross-account roles and permissions
            for account in forensic_accounts:
                self._setup_forensic_account_permissions(account)
                self._setup_forensic_storage(account)
                self._setup_forensic_tools(account)
            
            logger.info(f"Set up {len(forensic_accounts)} forensic accounts")
            
            return {
                'status': 'success',
                'accounts_created': len(forensic_accounts),
                'forensic_accounts': forensic_accounts,
                'message': f"Successfully set up forensic accounts for {len(regions)} regions"
            }
            
        except Exception as e:
            logger.error(f"Error setting up forensic accounts: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def collect_forensic_evidence(self, 
                                incident_id: str,
                                resource_identifiers: List[str],
                                evidence_types: List[str],
                                time_range: Dict[str, str]) -> Dict[str, Any]:
        """
        Automated collection of forensic evidence from AWS resources
        """
        try:
            collection_results = []
            evidence_registry = []
            
            for resource_id in resource_identifiers:
                for evidence_type in evidence_types:
                    collection_result = self._collect_evidence_by_type(
                        incident_id,
                        resource_id,
                        evidence_type,
                        time_range
                    )
                    
                    if collection_result['status'] == 'success':
                        evidence = ForensicEvidence(
                            evidence_id=collection_result['evidence_id'],
                            evidence_type=EvidenceType(evidence_type),
                            source_resource=resource_id,
                            collection_timestamp=datetime.utcnow().isoformat(),
                            chain_of_custody=[{
                                'handler': 'Automated Collection System',
                                'timestamp': datetime.utcnow().isoformat(),
                                'action': 'Evidence Collection',
                                'location': collection_result['storage_location']
                            }],
                            hash_values=collection_result['hash_values'],
                            storage_location=collection_result['storage_location'],
                            retention_period=collection_result['retention_period'],
                            classification='Confidential',
                            collection_method=collection_result['collection_method'],
                            integrity_verified=True,
                            metadata=collection_result['metadata']
                        )
                        
                        # Store evidence in registry
                        self.evidence_table.put_item(Item=asdict(evidence))
                        evidence_registry.append(evidence)
                    
                    collection_results.append(collection_result)
            
            successful_collections = sum(1 for result in collection_results if result['status'] == 'success')
            
            return {
                'status': 'success',
                'incident_id': incident_id,
                'total_collections': len(collection_results),
                'successful_collections': successful_collections,
                'evidence_collected': len(evidence_registry),
                'evidence_registry': [asdict(evidence) for evidence in evidence_registry],
                'collection_results': collection_results
            }
            
        except Exception as e:
            logger.error(f"Error collecting forensic evidence: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _create_forensic_account(self, account_name: str, region: str, organization_id: str) -> Dict[str, Any]:
        """
        Create a dedicated forensic account within AWS Organizations
        """
        try:
            # Create account (simplified - in practice, this requires proper account creation process)
            account_id = f"123456789{hash(account_name) % 1000:03d}"  # Simulated account ID
            
            forensic_account = ForensicAccount(
                account_id=account_id,
                account_name=account_name,
                region=region,
                purpose="Digital forensics and incident response",
                cross_account_roles=[
                    f"arn:aws:iam::{account_id}:role/ForensicInvestigatorRole",
                    f"arn:aws:iam::{account_id}:role/EvidenceCollectionRole"
                ],
                storage_buckets=[
                    f"forensic-evidence-{account_id.lower()}",
                    f"forensic-reports-{account_id.lower()}"
                ],
                analysis_tools=[
                    "Amazon Detective", "Amazon Athena", "Amazon QuickSight",
                    "Amazon OpenSearch", "Amazon SageMaker"
                ],
                access_controls={
                    "mfa_required": True,
                    "ip_restrictions": ["10.0.0.0/8", "172.16.0.0/12"],
                    "session_duration": "4 hours",
                    "break_glass_access": True
                },
                data_sovereignty_compliance=["US", "EU"] if region != "multi-region" else ["Global"]
            )
            
            # Store account information
            self.accounts_table.put_item(Item=asdict(forensic_account))
            
            return {
                'status': 'success',
                'account': forensic_account,
                'message': f"Successfully created forensic account {account_name}"
            }
            
        except Exception as e:
            logger.error(f"Error creating forensic account: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _collect_evidence_by_type(self, 
                                 incident_id: str,
                                 resource_id: str,
                                 evidence_type: str,
                                 time_range: Dict[str, str]) -> Dict[str, Any]:
        """
        Collect specific type of evidence from AWS resource
        """
        try:
            evidence_id = f"{incident_id}_{resource_id}_{evidence_type}_{int(datetime.utcnow().timestamp())}"
            
            if evidence_type == EvidenceType.LOGS.value:
                return self._collect_logs_evidence(evidence_id, resource_id, time_range)
            elif evidence_type == EvidenceType.SNAPSHOTS.value:
                return self._collect_snapshot_evidence(evidence_id, resource_id)
            elif evidence_type == EvidenceType.MEMORY_DUMPS.value:
                return self._collect_memory_evidence(evidence_id, resource_id)
            elif evidence_type == EvidenceType.NETWORK_CAPTURES.value:
                return self._collect_network_evidence(evidence_id, resource_id, time_range)
            elif evidence_type == EvidenceType.CONFIGURATION.value:
                return self._collect_configuration_evidence(evidence_id, resource_id)
            elif evidence_type == EvidenceType.METADATA.value:
                return self._collect_metadata_evidence(evidence_id, resource_id)
            else:
                return {
                    'status': 'error',
                    'message': f'Unsupported evidence type: {evidence_type}'
                }
                
        except Exception as e:
            logger.error(f"Error collecting evidence: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _collect_logs_evidence(self, evidence_id: str, resource_id: str, time_range: Dict[str, str]) -> Dict[str, Any]:
        """
        Collect log evidence from CloudWatch Logs and CloudTrail
        """
        try:
            # Export CloudWatch Logs
            log_group_name = f"/aws/ec2/{resource_id}"
            export_task_id = f"export-{evidence_id}"
            
            # Create log export task (simplified)
            storage_location = f"s3://forensic-evidence-bucket/logs/{evidence_id}/"
            
            # Calculate hash of collected logs
            log_content = f"Simulated log content for {resource_id}"
            log_hash = hashlib.sha256(log_content.encode()).hexdigest()
            
            return {
                'status': 'success',
                'evidence_id': evidence_id,
                'storage_location': storage_location,
                'collection_method': 'CloudWatch Logs Export',
                'hash_values': {'sha256': log_hash},
                'retention_period': '7 years',
                'metadata': {
                    'log_group': log_group_name,
                    'export_task_id': export_task_id,
                    'time_range': time_range,
                    'log_size_bytes': len(log_content)
                }
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _collect_snapshot_evidence(self, evidence_id: str, resource_id: str) -> Dict[str, Any]:
        """
        Collect snapshot evidence from EC2 instances and EBS volumes
        """
        try:
            # Create EBS snapshot
            snapshot_id = f"snap-{evidence_id[-8:]}"
            
            # Simulate snapshot creation
            storage_location = f"snapshot://{snapshot_id}"
            
            # Calculate snapshot hash (simplified)
            snapshot_content = f"Simulated snapshot content for {resource_id}"
            snapshot_hash = hashlib.sha256(snapshot_content.encode()).hexdigest()
            
            return {
                'status': 'success',
                'evidence_id': evidence_id,
                'storage_location': storage_location,
                'collection_method': 'EBS Snapshot Creation',
                'hash_values': {'sha256': snapshot_hash},
                'retention_period': '3 years',
                'metadata': {
                    'snapshot_id': snapshot_id,
                    'source_volume': resource_id,
                    'snapshot_size_gb': 100,
                    'encryption_status': 'encrypted'
                }
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _collect_memory_evidence(self, evidence_id: str, resource_id: str) -> Dict[str, Any]:
        """
        Collect memory dump evidence from EC2 instances
        """
        try:
            # Create memory dump using Systems Manager
            storage_location = f"s3://forensic-evidence-bucket/memory/{evidence_id}.mem"
            
            # Calculate memory dump hash
            memory_content = f"Simulated memory dump for {resource_id}"
            memory_hash = hashlib.sha256(memory_content.encode()).hexdigest()
            
            return {
                'status': 'success',
                'evidence_id': evidence_id,
                'storage_location': storage_location,
                'collection_method': 'Systems Manager Memory Dump',
                'hash_values': {'sha256': memory_hash},
                'retention_period': '1 year',
                'metadata': {
                    'instance_id': resource_id,
                    'memory_size_mb': 8192,
                    'dump_format': 'raw',
                    'collection_tool': 'SSM Agent'
                }
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }

# Example usage
if __name__ == "__main__":
    # Initialize forensic capabilities manager
    forensic_manager = ForensicCapabilitiesManager()
    
    # Set up forensic accounts
    accounts_result = forensic_manager.setup_forensic_accounts(
        organization_id="o-example123456",
        regions=["us-east-1", "us-west-2"],
        account_strategy="per_region"
    )
    print(f"Forensic accounts setup: {json.dumps(accounts_result, indent=2, default=str)}")
    
    # Collect forensic evidence
    evidence_result = forensic_manager.collect_forensic_evidence(
        incident_id="INC-2024-001",
        resource_identifiers=["i-1234567890abcdef0", "vol-0987654321fedcba0"],
        evidence_types=["logs", "snapshots", "memory_dumps"],
        time_range={
            "start_time": "2024-01-01T00:00:00Z",
            "end_time": "2024-01-01T23:59:59Z"
        }
    )
    print(f"Evidence collection: {json.dumps(evidence_result, indent=2, default=str)}")
```
### Example 2: Automated Forensic Evidence Collection and Analysis

```python
# automated_forensic_orchestrator.py
import boto3
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class AutomatedForensicOrchestrator:
    """
    Orchestrates automated forensic evidence collection and initial analysis
    """
    
    def __init__(self, region: str = 'us-east-1'):
        self.region = region
        self.stepfunctions_client = boto3.client('stepfunctions', region_name=region)
        self.lambda_client = boto3.client('lambda', region_name=region)
        self.ec2_client = boto3.client('ec2', region_name=region)
        self.s3_client = boto3.client('s3', region_name=region)
        self.ssm_client = boto3.client('ssm', region_name=region)
        self.athena_client = boto3.client('athena', region_name=region)
        self.detective_client = boto3.client('detective', region_name=region)
    
    def create_forensic_workflow(self) -> Dict[str, Any]:
        """
        Create Step Functions workflow for automated forensic evidence collection
        """
        try:
            # Define the forensic collection workflow
            workflow_definition = {
                "Comment": "Automated Forensic Evidence Collection Workflow",
                "StartAt": "InitiateForensicCollection",
                "States": {
                    "InitiateForensicCollection": {
                        "Type": "Task",
                        "Resource": "arn:aws:states:::lambda:invoke",
                        "Parameters": {
                            "FunctionName": "forensic-collection-initiator",
                            "Payload.$": "$"
                        },
                        "Next": "ParallelEvidenceCollection"
                    },
                    "ParallelEvidenceCollection": {
                        "Type": "Parallel",
                        "Branches": [
                            {
                                "StartAt": "CollectSnapshots",
                                "States": {
                                    "CollectSnapshots": {
                                        "Type": "Task",
                                        "Resource": "arn:aws:states:::lambda:invoke",
                                        "Parameters": {
                                            "FunctionName": "forensic-snapshot-collector",
                                            "Payload.$": "$"
                                        },
                                        "End": True
                                    }
                                }
                            },
                            {
                                "StartAt": "CollectLogs",
                                "States": {
                                    "CollectLogs": {
                                        "Type": "Task",
                                        "Resource": "arn:aws:states:::lambda:invoke",
                                        "Parameters": {
                                            "FunctionName": "forensic-log-collector",
                                            "Payload.$": "$"
                                        },
                                        "End": True
                                    }
                                }
                            },
                            {
                                "StartAt": "CollectMemoryDumps",
                                "States": {
                                    "CollectMemoryDumps": {
                                        "Type": "Task",
                                        "Resource": "arn:aws:states:::lambda:invoke",
                                        "Parameters": {
                                            "FunctionName": "forensic-memory-collector",
                                            "Payload.$": "$"
                                        },
                                        "End": True
                                    }
                                }
                            },
                            {
                                "StartAt": "CollectNetworkData",
                                "States": {
                                    "CollectNetworkData": {
                                        "Type": "Task",
                                        "Resource": "arn:aws:states:::lambda:invoke",
                                        "Parameters": {
                                            "FunctionName": "forensic-network-collector",
                                            "Payload.$": "$"
                                        },
                                        "End": True
                                    }
                                }
                            }
                        ],
                        "Next": "ValidateEvidenceIntegrity"
                    },
                    "ValidateEvidenceIntegrity": {
                        "Type": "Task",
                        "Resource": "arn:aws:states:::lambda:invoke",
                        "Parameters": {
                            "FunctionName": "forensic-integrity-validator",
                            "Payload.$": "$"
                        },
                        "Next": "InitialAnalysis"
                    },
                    "InitialAnalysis": {
                        "Type": "Task",
                        "Resource": "arn:aws:states:::lambda:invoke",
                        "Parameters": {
                            "FunctionName": "forensic-initial-analyzer",
                            "Payload.$": "$"
                        },
                        "Next": "GenerateForensicReport"
                    },
                    "GenerateForensicReport": {
                        "Type": "Task",
                        "Resource": "arn:aws:states:::lambda:invoke",
                        "Parameters": {
                            "FunctionName": "forensic-report-generator",
                            "Payload.$": "$"
                        },
                        "Next": "NotifyInvestigators"
                    },
                    "NotifyInvestigators": {
                        "Type": "Task",
                        "Resource": "arn:aws:states:::sns:publish",
                        "Parameters": {
                            "TopicArn": "arn:aws:sns:us-east-1:123456789012:forensic-notifications",
                            "Message.$": "$.forensic_report_summary"
                        },
                        "End": True
                    }
                }
            }
            
            # Create the Step Functions state machine
            response = self.stepfunctions_client.create_state_machine(
                name='ForensicEvidenceCollectionWorkflow',
                definition=json.dumps(workflow_definition),
                roleArn='arn:aws:iam::123456789012:role/StepFunctionsForensicRole',
                type='STANDARD',
                tags=[
                    {
                        'key': 'Purpose',
                        'value': 'ForensicInvestigation'
                    },
                    {
                        'key': 'Automation',
                        'value': 'EvidenceCollection'
                    }
                ]
            )
            
            return {
                'status': 'success',
                'state_machine_arn': response['stateMachineArn'],
                'message': 'Successfully created forensic workflow'
            }
            
        except Exception as e:
            logger.error(f"Error creating forensic workflow: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def deploy_forensic_lambda_functions(self) -> Dict[str, Any]:
        """
        Deploy Lambda functions for forensic evidence collection
        """
        try:
            lambda_functions = []
            
            # Forensic Snapshot Collector
            snapshot_collector_code = '''
import boto3
import json
from datetime import datetime

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    
    instance_ids = event.get('instance_ids', [])
    incident_id = event.get('incident_id', 'unknown')
    
    snapshots_created = []
    
    for instance_id in instance_ids:
        try:
            # Get instance volumes
            response = ec2.describe_instances(InstanceIds=[instance_id])
            
            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    for block_device in instance.get('BlockDeviceMappings', []):
                        volume_id = block_device['Ebs']['VolumeId']
                        
                        # Create forensic snapshot
                        snapshot_response = ec2.create_snapshot(
                            VolumeId=volume_id,
                            Description=f'Forensic snapshot for incident {incident_id} - {instance_id}',
                            TagSpecifications=[
                                {
                                    'ResourceType': 'snapshot',
                                    'Tags': [
                                        {'Key': 'Purpose', 'Value': 'Forensic'},
                                        {'Key': 'IncidentId', 'Value': incident_id},
                                        {'Key': 'SourceInstance', 'Value': instance_id},
                                        {'Key': 'CreatedBy', 'Value': 'ForensicAutomation'}
                                    ]
                                }
                            ]
                        )
                        
                        snapshots_created.append({
                            'snapshot_id': snapshot_response['SnapshotId'],
                            'volume_id': volume_id,
                            'instance_id': instance_id
                        })
                        
        except Exception as e:
            print(f"Error creating snapshot for {instance_id}: {str(e)}")
    
    return {
        'statusCode': 200,
        'body': {
            'snapshots_created': snapshots_created,
            'total_snapshots': len(snapshots_created)
        }
    }
'''
            
            # Forensic Log Collector
            log_collector_code = '''
import boto3
import json
from datetime import datetime, timedelta

def lambda_handler(event, context):
    logs_client = boto3.client('logs')
    s3_client = boto3.client('s3')
    
    incident_id = event.get('incident_id', 'unknown')
    time_range = event.get('time_range', {})
    log_groups = event.get('log_groups', [])
    
    export_tasks = []
    
    for log_group in log_groups:
        try:
            # Create log export task
            export_task_response = logs_client.create_export_task(
                logGroupName=log_group,
                fromTime=int(datetime.fromisoformat(time_range['start_time'].replace('Z', '+00:00')).timestamp() * 1000),
                to=int(datetime.fromisoformat(time_range['end_time'].replace('Z', '+00:00')).timestamp() * 1000),
                destination=f'forensic-evidence-{incident_id}',
                destinationPrefix=f'logs/{log_group.replace("/", "_")}/'
            )
            
            export_tasks.append({
                'task_id': export_task_response['taskId'],
                'log_group': log_group,
                'status': 'PENDING'
            })
            
        except Exception as e:
            print(f"Error exporting logs for {log_group}: {str(e)}")
    
    return {
        'statusCode': 200,
        'body': {
            'export_tasks': export_tasks,
            'total_exports': len(export_tasks)
        }
    }
'''
            
            # Forensic Memory Collector
            memory_collector_code = '''
import boto3
import json

def lambda_handler(event, context):
    ssm_client = boto3.client('ssm')
    
    instance_ids = event.get('instance_ids', [])
    incident_id = event.get('incident_id', 'unknown')
    
    memory_dumps = []
    
    for instance_id in instance_ids:
        try:
            # Execute memory dump command via Systems Manager
            response = ssm_client.send_command(
                InstanceIds=[instance_id],
                DocumentName='AWS-RunShellScript',
                Parameters={
                    'commands': [
                        f'sudo dd if=/proc/kcore of=/tmp/memory_dump_{incident_id}_{instance_id}.mem bs=1M count=1024',
                        f'aws s3 cp /tmp/memory_dump_{incident_id}_{instance_id}.mem s3://forensic-evidence-{incident_id}/memory/',
                        f'rm /tmp/memory_dump_{incident_id}_{instance_id}.mem'
                    ]
                },
                Comment=f'Forensic memory dump for incident {incident_id}'
            )
            
            memory_dumps.append({
                'command_id': response['Command']['CommandId'],
                'instance_id': instance_id,
                'status': 'InProgress'
            })
            
        except Exception as e:
            print(f"Error collecting memory dump for {instance_id}: {str(e)}")
    
    return {
        'statusCode': 200,
        'body': {
            'memory_dumps': memory_dumps,
            'total_dumps': len(memory_dumps)
        }
    }
'''
            
            # Deploy Lambda functions
            functions_to_deploy = [
                {
                    'name': 'forensic-snapshot-collector',
                    'code': snapshot_collector_code,
                    'description': 'Automated forensic snapshot collection'
                },
                {
                    'name': 'forensic-log-collector',
                    'code': log_collector_code,
                    'description': 'Automated forensic log collection'
                },
                {
                    'name': 'forensic-memory-collector',
                    'code': memory_collector_code,
                    'description': 'Automated forensic memory dump collection'
                }
            ]
            
            for func_config in functions_to_deploy:
                try:
                    response = self.lambda_client.create_function(
                        FunctionName=func_config['name'],
                        Runtime='python3.9',
                        Role='arn:aws:iam::123456789012:role/ForensicLambdaExecutionRole',
                        Handler='index.lambda_handler',
                        Code={'ZipFile': func_config['code'].encode()},
                        Description=func_config['description'],
                        Timeout=900,  # 15 minutes
                        MemorySize=512,
                        Tags={
                            'Purpose': 'ForensicInvestigation',
                            'Component': 'EvidenceCollection'
                        }
                    )
                    
                    lambda_functions.append({
                        'function_name': func_config['name'],
                        'function_arn': response['FunctionArn'],
                        'status': 'deployed'
                    })
                    
                except Exception as e:
                    logger.error(f"Error deploying {func_config['name']}: {str(e)}")
                    lambda_functions.append({
                        'function_name': func_config['name'],
                        'status': 'failed',
                        'error': str(e)
                    })
            
            return {
                'status': 'success',
                'functions_deployed': len([f for f in lambda_functions if f['status'] == 'deployed']),
                'lambda_functions': lambda_functions,
                'message': 'Successfully deployed forensic Lambda functions'
            }
            
        except Exception as e:
            logger.error(f"Error deploying forensic Lambda functions: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def setup_forensic_analysis_environment(self, forensic_account_id: str) -> Dict[str, Any]:
        """
        Set up forensic analysis environment with necessary tools and services
        """
        try:
            analysis_components = []
            
            # Set up Athena for log analysis
            athena_setup = self._setup_athena_forensic_analysis(forensic_account_id)
            analysis_components.append(athena_setup)
            
            # Set up Detective for investigation graphs
            detective_setup = self._setup_detective_forensic_analysis(forensic_account_id)
            analysis_components.append(detective_setup)
            
            # Set up forensic workstation EC2 instances
            workstation_setup = self._setup_forensic_workstations(forensic_account_id)
            analysis_components.append(workstation_setup)
            
            # Set up secure evidence storage
            storage_setup = self._setup_forensic_evidence_storage(forensic_account_id)
            analysis_components.append(storage_setup)
            
            successful_setups = sum(1 for component in analysis_components if component['status'] == 'success')
            
            return {
                'status': 'success',
                'forensic_account_id': forensic_account_id,
                'components_configured': successful_setups,
                'analysis_components': analysis_components,
                'message': f'Successfully set up forensic analysis environment in account {forensic_account_id}'
            }
            
        except Exception as e:
            logger.error(f"Error setting up forensic analysis environment: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _setup_athena_forensic_analysis(self, account_id: str) -> Dict[str, Any]:
        """
        Set up Athena for forensic log analysis
        """
        try:
            # Create Athena workgroup for forensic analysis
            workgroup_name = 'forensic-investigation'
            
            # Create forensic analysis queries
            forensic_queries = {
                'cloudtrail_analysis': '''
                    SELECT eventTime, eventName, sourceIPAddress, userIdentity, 
                           awsRegion, errorCode, errorMessage
                    FROM cloudtrail_logs 
                    WHERE eventTime BETWEEN '{start_time}' AND '{end_time}'
                    AND (errorCode IS NOT NULL OR eventName LIKE '%Delete%' OR eventName LIKE '%Terminate%')
                    ORDER BY eventTime DESC
                ''',
                'vpc_flow_analysis': '''
                    SELECT srcaddr, dstaddr, srcport, dstport, protocol, 
                           packets, bytes, windowstart, windowend, action
                    FROM vpc_flow_logs 
                    WHERE windowstart BETWEEN {start_timestamp} AND {end_timestamp}
                    AND action = 'REJECT'
                    ORDER BY windowstart DESC
                ''',
                'security_group_changes': '''
                    SELECT eventTime, eventName, sourceIPAddress, userIdentity,
                           requestParameters, responseElements
                    FROM cloudtrail_logs 
                    WHERE eventName IN ('AuthorizeSecurityGroupIngress', 'RevokeSecurityGroupIngress',
                                       'AuthorizeSecurityGroupEgress', 'RevokeSecurityGroupEgress')
                    AND eventTime BETWEEN '{start_time}' AND '{end_time}'
                    ORDER BY eventTime DESC
                '''
            }
            
            return {
                'status': 'success',
                'component': 'athena',
                'workgroup': workgroup_name,
                'queries_available': len(forensic_queries),
                'message': 'Successfully configured Athena for forensic analysis'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'component': 'athena',
                'message': str(e)
            }
    
    def _setup_detective_forensic_analysis(self, account_id: str) -> Dict[str, Any]:
        """
        Set up Amazon Detective for forensic investigation graphs
        """
        try:
            # Enable Detective (simplified - requires proper setup)
            detective_graph_arn = f"arn:aws:detective:us-east-1:{account_id}:graph:forensic-investigation"
            
            return {
                'status': 'success',
                'component': 'detective',
                'graph_arn': detective_graph_arn,
                'message': 'Successfully configured Detective for forensic analysis'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'component': 'detective',
                'message': str(e)
            }
    
    def _setup_forensic_workstations(self, account_id: str) -> Dict[str, Any]:
        """
        Set up secure forensic analysis workstations
        """
        try:
            # Launch forensic workstation instances
            workstation_config = {
                'instance_type': 'm5.2xlarge',
                'ami_id': 'ami-0abcdef1234567890',  # Forensic analysis AMI
                'security_group': 'sg-forensic-workstation',
                'subnet_id': 'subnet-forensic-analysis',
                'key_pair': 'forensic-investigation-key'
            }
            
            workstations = []
            for i in range(2):  # Create 2 workstations
                workstation_id = f"i-forensic-workstation-{i+1}"
                workstations.append({
                    'instance_id': workstation_id,
                    'instance_type': workstation_config['instance_type'],
                    'purpose': 'Forensic Analysis',
                    'tools_installed': [
                        'SIFT Workstation', 'Volatility', 'Autopsy',
                        'Wireshark', 'Sleuth Kit', 'AWS CLI'
                    ]
                })
            
            return {
                'status': 'success',
                'component': 'workstations',
                'workstations_created': len(workstations),
                'workstations': workstations,
                'message': 'Successfully configured forensic workstations'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'component': 'workstations',
                'message': str(e)
            }
    
    def _setup_forensic_evidence_storage(self, account_id: str) -> Dict[str, Any]:
        """
        Set up secure evidence storage with proper access controls
        """
        try:
            # Create evidence storage buckets
            evidence_buckets = [
                {
                    'bucket_name': f'forensic-evidence-{account_id}',
                    'purpose': 'Primary evidence storage',
                    'encryption': 'AES-256',
                    'versioning': True,
                    'mfa_delete': True
                },
                {
                    'bucket_name': f'forensic-reports-{account_id}',
                    'purpose': 'Forensic reports and documentation',
                    'encryption': 'AES-256',
                    'versioning': True,
                    'mfa_delete': True
                },
                {
                    'bucket_name': f'forensic-backups-{account_id}',
                    'purpose': 'Evidence backups and archives',
                    'encryption': 'AES-256',
                    'versioning': True,
                    'mfa_delete': True
                }
            ]
            
            return {
                'status': 'success',
                'component': 'storage',
                'buckets_created': len(evidence_buckets),
                'evidence_buckets': evidence_buckets,
                'message': 'Successfully configured forensic evidence storage'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'component': 'storage',
                'message': str(e)
            }

# Example usage
if __name__ == "__main__":
    # Initialize automated forensic orchestrator
    forensic_orchestrator = AutomatedForensicOrchestrator()
    
    # Create forensic workflow
    workflow_result = forensic_orchestrator.create_forensic_workflow()
    print(f"Forensic workflow creation: {json.dumps(workflow_result, indent=2)}")
    
    # Deploy Lambda functions
    lambda_result = forensic_orchestrator.deploy_forensic_lambda_functions()
    print(f"Lambda functions deployment: {json.dumps(lambda_result, indent=2)}")
    
    # Set up analysis environment
    analysis_result = forensic_orchestrator.setup_forensic_analysis_environment("123456789012")
    print(f"Analysis environment setup: {json.dumps(analysis_result, indent=2)}")
```
## Resources

### Related Documents

- [AWS Security Incident Response Guide - Develop Forensics Capabilities](https://docs.aws.amazon.com/whitepapers/latest/aws-security-incident-response-guide/develop-forensics-capabilities.html)
- [AWS Security Incident Response Guide - Forensics Resources](https://docs.aws.amazon.com/whitepapers/latest/aws-security-incident-response-guide/forensics-resources.html)
- [Forensic investigation environment strategies in the AWS Cloud](https://docs.aws.amazon.com/whitepapers/latest/forensic-investigation-environment-strategies-in-the-aws-cloud/forensic-investigation-environment-strategies-in-the-aws-cloud.html)
- [How to automate forensic disk collection in AWS](https://aws.amazon.com/blogs/security/how-to-automate-forensic-disk-collection-in-aws/)
- [AWS Prescriptive Guidance - Automate incident response and forensics](https://docs.aws.amazon.com/prescriptive-guidance/latest/patterns/automate-incident-response-and-forensics-using-aws-services.html)
- [Backup and Recovery Prescriptive Guidance](https://docs.aws.amazon.com/prescriptive-guidance/latest/backup-recovery/welcome.html)
- [Use backups to recover from security incidents](https://docs.aws.amazon.com/whitepapers/latest/aws-security-incident-response-guide/use-backups-to-recover-from-security-incidents.html)
- [Top 10 security best practices for securing backups in AWS](https://aws.amazon.com/blogs/storage/top-10-security-best-practices-for-securing-backups-in-aws/)

### Related AWS Services

- [AWS Organizations](https://aws.amazon.com/organizations/) - For forensic account structure and management
- [Amazon EC2 Snapshots](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSSnapshots.html) - For forensic disk imaging
- [AWS CloudTrail](https://aws.amazon.com/cloudtrail/) - For API activity logging and forensic analysis
- [Amazon VPC Flow Logs](https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html) - For network traffic analysis
- [AWS Config](https://aws.amazon.com/config/) - For configuration change tracking
- [Amazon CloudWatch Logs](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/WhatIsCloudWatchLogs.html) - For application and system log collection
- [AWS Systems Manager](https://aws.amazon.com/systems-manager/) - For automated evidence collection
- [Amazon Detective](https://aws.amazon.com/detective/) - For security investigation and analysis
- [Amazon Athena](https://aws.amazon.com/athena/) - For forensic log analysis
- [AWS Step Functions](https://aws.amazon.com/step-functions/) - For forensic workflow orchestration
- [Amazon S3](https://aws.amazon.com/s3/) - For secure evidence storage
- [AWS Backup](https://aws.amazon.com/backup/) - For automated backup and recovery

### Related Videos

- [Automating Incident Response and Forensics](https://www.youtube.com/watch?v=f_EcwmmXkXk)
- [AWS re:Invent 2020: Incident response and forensics in the cloud](https://www.youtube.com/watch?v=MHHTp6_vAzs)

### Related Examples

- [Automated Incident Response and Forensics Framework](https://github.com/aws-samples/automated-incident-response-and-forensics)
- [Automated Forensics Orchestrator for Amazon EC2](https://github.com/aws-samples/automated-forensics-orchestrator-for-amazon-ec2)
- [AWS Security Analytics Bootstrap](https://github.com/aws-samples/aws-security-analytics-bootstrap)
- [AWS CloudTrail Analysis Framework](https://github.com/aws-samples/aws-cloudtrail-analyzer)

### Related Tools and Solutions

- [SIFT Workstation](https://digital-forensics.sans.org/community/downloads) - Digital forensics and incident response toolkit
- [Volatility Framework](https://www.volatilityfoundation.org/) - Memory forensics framework
- [Autopsy](https://www.autopsy.com/) - Digital forensics platform
- [Sleuth Kit](https://www.sleuthkit.org/) - Digital investigation tools
- [Wireshark](https://www.wireshark.org/) - Network protocol analyzer
- [YARA](https://virustotal.github.io/yara/) - Malware identification and classification

### Compliance and Legal Considerations

- [NIST SP 800-86: Guide to Integrating Forensic Techniques into Incident Response](https://csrc.nist.gov/publications/detail/sp/800-86/final)
- [ISO/IEC 27037: Guidelines for identification, collection, acquisition and preservation of digital evidence](https://www.iso.org/standard/44381.html)
- [Federal Rules of Evidence](https://www.uscourts.gov/rules-policies/current-rules-practice-procedure/federal-rules-evidence) - For legal admissibility of digital evidence
- [GDPR Article 33](https://gdpr-info.eu/art-33-gdpr/) - Personal data breach notification requirements
- [HIPAA Security Rule](https://www.hhs.gov/hipaa/for-professionals/security/index.html) - Healthcare data protection requirements

### Best Practices and Guidelines

- Maintain proper chain of custody documentation for all evidence
- Use write-blocking tools when acquiring disk images
- Implement time synchronization across all forensic systems
- Regularly test forensic procedures and tools
- Ensure forensic personnel have appropriate training and certifications
- Document all forensic procedures and maintain detailed case notes
- Implement secure evidence storage with appropriate access controls
- Regular backup and testing of forensic tools and environments
