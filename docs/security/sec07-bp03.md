---
title: "SEC07-BP03: Automate identification and classification"
layout: default
parent: "SEC07 - How do you classify your data?"
grand_parent: Security
nav_order: 3
---

# SEC07-BP03: Automate identification and classification

## Overview

Manual data classification is time-consuming, error-prone, and doesn't scale with modern data volumes. Automated identification and classification of data ensures consistent, accurate, and timely classification of your data assets as they are created, modified, or moved within your environment.

This best practice focuses on implementing automated systems that can discover, analyze, and classify data based on content, context, and metadata, enabling real-time application of appropriate protection controls and compliance measures.

## Implementation Guidance

### 1. Implement Content-Based Classification

Deploy automated tools that analyze data content to identify sensitive information:

- **Pattern Recognition**: Use regular expressions and machine learning to identify PII, PHI, financial data
- **Contextual Analysis**: Analyze data relationships and usage patterns
- **Metadata Analysis**: Examine file properties, database schemas, and system metadata
- **Machine Learning Models**: Train models to recognize organization-specific sensitive data patterns

### 2. Establish Real-Time Classification Workflows

Create automated workflows that classify data as it enters your environment:

- **Data Ingestion Points**: Classify data at entry points (APIs, file uploads, database inserts)
- **Event-Driven Classification**: Trigger classification on data creation, modification, or access events
- **Streaming Classification**: Process data streams in real-time for immediate classification
- **Batch Processing**: Schedule regular classification jobs for existing data

### 3. Configure Multi-Service Integration

Integrate classification across your AWS environment:

- **Cross-Service Tagging**: Apply consistent classification tags across all AWS services
- **API Integration**: Use AWS APIs to propagate classification metadata
- **Service-Specific Classification**: Leverage native classification features in AWS services
- **Third-Party Integration**: Connect with external classification tools and systems

### 4. Implement Classification Validation and Quality Control

Ensure accuracy and consistency of automated classification:

- **Confidence Scoring**: Implement confidence levels for classification decisions
- **Human Review Workflows**: Route uncertain classifications for manual review
- **Classification Auditing**: Track and audit classification decisions and changes
- **Feedback Loops**: Improve classification accuracy through continuous learning

### 5. Establish Classification Governance and Monitoring

Monitor and govern your automated classification processes:

- **Classification Metrics**: Track classification coverage, accuracy, and performance
- **Policy Enforcement**: Automatically enforce policies based on classification
- **Exception Handling**: Manage classification exceptions and edge cases
- **Compliance Reporting**: Generate reports for regulatory and audit requirements

### 6. Enable Dynamic Reclassification

Implement systems that can reclassify data as conditions change:

- **Temporal Classification**: Adjust classification based on data age or lifecycle stage
- **Context-Aware Reclassification**: Update classification based on usage patterns or business context
- **Regulatory Changes**: Automatically reclassify data when regulations change
- **Business Rule Updates**: Apply new classification rules to existing data

## Implementation Examples

### Example 1: Amazon Macie Automated Classification System

```python
# macie_auto_classifier.py
import boto3
import json
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ClassificationResult:
    resource_arn: str
    classification_level: str
    sensitive_data_types: List[str]
    confidence_score: float
    classification_timestamp: str
    requires_human_review: bool
    compliance_frameworks: List[str]

@dataclass
class CustomDataIdentifier:
    name: str
    description: str
    regex: str
    keywords: List[str]
    ignore_words: List[str]
    maximum_match_distance: int

class MacieAutoClassifier:
    """
    Automated data classification system using Amazon Macie
    """
    
    def __init__(self, region: str = 'us-east-1'):
        self.region = region
        self.macie_client = boto3.client('macie2', region_name=region)
        self.s3_client = boto3.client('s3', region_name=region)
        self.lambda_client = boto3.client('lambda', region_name=region)
        self.sns_client = boto3.client('sns', region_name=region)
        self.dynamodb = boto3.resource('dynamodb', region_name=region)
        
        # Initialize classification tracking table
        self.classification_table = self.dynamodb.Table('data-classification-results')
        
        # Classification thresholds
        self.confidence_thresholds = {
            'high': 0.9,
            'medium': 0.7,
            'low': 0.5
        }
        
        # Sensitive data type mappings
        self.sensitivity_mappings = {
            'CREDIT_CARD_NUMBER': {'level': 'restricted', 'frameworks': ['PCI_DSS']},
            'SSN': {'level': 'restricted', 'frameworks': ['HIPAA', 'GDPR']},
            'PHONE_NUMBER': {'level': 'confidential', 'frameworks': ['GDPR']},
            'EMAIL_ADDRESS': {'level': 'internal', 'frameworks': ['GDPR']},
            'PERSON_NAME': {'level': 'confidential', 'frameworks': ['GDPR', 'HIPAA']},
            'ADDRESS': {'level': 'confidential', 'frameworks': ['GDPR']},
            'BANK_ACCOUNT_NUMBER': {'level': 'restricted', 'frameworks': ['PCI_DSS']},
            'PASSPORT_NUMBER': {'level': 'restricted', 'frameworks': ['GDPR']},
            'DRIVER_LICENSE': {'level': 'restricted', 'frameworks': ['GDPR']},
            'MEDICAL_RECORD_NUMBER': {'level': 'restricted', 'frameworks': ['HIPAA']}
        }
    
    def setup_macie_environment(self) -> Dict[str, Any]:
        """
        Set up Macie environment for automated classification
        """
        setup_results = {
            'macie_enabled': False,
            'custom_identifiers_created': [],
            'classification_jobs_configured': [],
            'findings_export_configured': False,
            'errors': []
        }
        
        try:
            # Enable Macie if not already enabled
            try:
                self.macie_client.get_macie_session()
                setup_results['macie_enabled'] = True
                logger.info("Macie is already enabled")
            except self.macie_client.exceptions.ResourceNotFoundException:
                self.macie_client.enable_macie()
                setup_results['macie_enabled'] = True
                logger.info("Macie has been enabled")
            
            # Create custom data identifiers
            custom_identifiers = self._get_custom_data_identifiers()
            for identifier in custom_identifiers:
                try:
                    response = self.macie_client.create_custom_data_identifier(
                        name=identifier.name,
                        description=identifier.description,
                        regex=identifier.regex,
                        keywords=identifier.keywords,
                        ignoreWords=identifier.ignore_words,
                        maximumMatchDistance=identifier.maximum_match_distance
                    )
                    setup_results['custom_identifiers_created'].append({
                        'name': identifier.name,
                        'id': response['customDataIdentifierId']
                    })
                    logger.info(f"Created custom data identifier: {identifier.name}")
                except Exception as e:
                    setup_results['errors'].append(f"Failed to create identifier {identifier.name}: {str(e)}")
            
            # Configure findings export
            self._configure_findings_export()
            setup_results['findings_export_configured'] = True
            
        except Exception as e:
            setup_results['errors'].append(f"Setup error: {str(e)}")
            logger.error(f"Macie setup error: {str(e)}")
        
        return setup_results
    
    def _get_custom_data_identifiers(self) -> List[CustomDataIdentifier]:
        """
        Define custom data identifiers for organization-specific data
        """
        return [
            CustomDataIdentifier(
                name="Employee_ID",
                description="Company employee identification numbers",
                regex=r"EMP-\d{6}",
                keywords=["employee", "emp", "staff"],
                ignore_words=["example", "sample", "test"],
                maximum_match_distance=50
            ),
            CustomDataIdentifier(
                name="Customer_ID",
                description="Customer identification numbers",
                regex=r"CUST-[A-Z]{2}\d{8}",
                keywords=["customer", "client", "account"],
                ignore_words=["example", "sample", "demo"],
                maximum_match_distance=50
            ),
            CustomDataIdentifier(
                name="Internal_Project_Code",
                description="Internal project codes",
                regex=r"PROJ-\d{4}-[A-Z]{3}",
                keywords=["project", "initiative", "program"],
                ignore_words=["example", "template"],
                maximum_match_distance=30
            ),
            CustomDataIdentifier(
                name="API_Key",
                description="API keys and tokens",
                regex=r"[A-Za-z0-9]{32,}",
                keywords=["api", "key", "token", "secret"],
                ignore_words=["example", "placeholder"],
                maximum_match_distance=20
            )
        ]
    
    def create_classification_job(self, 
                                bucket_names: List[str], 
                                job_name: str,
                                schedule_expression: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a Macie classification job for specified S3 buckets
        """
        try:
            # Prepare S3 bucket criteria
            s3_bucket_criteria = []
            for bucket_name in bucket_names:
                s3_bucket_criteria.append({
                    'bucketName': bucket_name,
                    'includes': {
                        'and': [
                            {
                                'simpleCriterion': {
                                    'comparator': 'GT',
                                    'key': 'OBJECT_SIZE',
                                    'values': ['0']
                                }
                            }
                        ]
                    }
                })
            
            # Create job parameters
            job_params = {
                'name': job_name,
                'jobType': 'SCHEDULED' if schedule_expression else 'ONE_TIME',
                's3JobDefinition': {
                    'bucketCriteria': {
                        'includes': {
                            'and': s3_bucket_criteria
                        }
                    },
                    'scoping': {
                        'includes': {
                            'and': [
                                {
                                    'simpleCriterion': {
                                        'comparator': 'NE',
                                        'key': 'OBJECT_EXTENSION',
                                        'values': ['zip', 'tar', 'gz', 'exe', 'bin']
                                    }
                                }
                            ]
                        }
                    }
                },
                'samplingPercentage': 100,
                'description': f'Automated classification job for buckets: {", ".join(bucket_names)}'
            }
            
            # Add schedule if provided
            if schedule_expression:
                job_params['scheduleFrequency'] = {
                    'dailySchedule': {}
                }
            
            # Create the job
            response = self.macie_client.create_classification_job(**job_params)
            
            logger.info(f"Created classification job: {job_name} (ID: {response['jobId']})")
            
            return {
                'job_id': response['jobId'],
                'job_name': job_name,
                'buckets': bucket_names,
                'status': 'created',
                'schedule': schedule_expression
            }
            
        except Exception as e:
            logger.error(f"Failed to create classification job: {str(e)}")
            return {
                'error': str(e),
                'job_name': job_name,
                'buckets': bucket_names,
                'status': 'failed'
            }
    
    def process_classification_findings(self, findings: List[Dict[str, Any]]) -> List[ClassificationResult]:
        """
        Process Macie findings and generate classification results
        """
        classification_results = []
        
        for finding in findings:
            try:
                # Extract finding details
                resource_arn = finding.get('resourcesAffected', {}).get('s3Bucket', {}).get('arn', '')
                sensitive_data = finding.get('classificationDetails', {}).get('result', {}).get('sensitiveData', [])
                
                # Determine classification level and confidence
                classification_level, confidence_score, compliance_frameworks = self._determine_classification(sensitive_data)
                
                # Extract sensitive data types
                sensitive_data_types = []
                for data_item in sensitive_data:
                    category = data_item.get('category', '')
                    if category:
                        sensitive_data_types.append(category)
                
                # Determine if human review is required
                requires_review = confidence_score < self.confidence_thresholds['high']
                
                # Create classification result
                result = ClassificationResult(
                    resource_arn=resource_arn,
                    classification_level=classification_level,
                    sensitive_data_types=sensitive_data_types,
                    confidence_score=confidence_score,
                    classification_timestamp=datetime.utcnow().isoformat(),
                    requires_human_review=requires_review,
                    compliance_frameworks=compliance_frameworks
                )
                
                classification_results.append(result)
                
                # Store result in DynamoDB
                self._store_classification_result(result)
                
                # Apply classification tags
                self._apply_classification_tags(result)
                
                # Trigger human review if needed
                if requires_review:
                    self._trigger_human_review(result)
                
            except Exception as e:
                logger.error(f"Error processing finding: {str(e)}")
                continue
        
        return classification_results
    
    def _determine_classification(self, sensitive_data: List[Dict[str, Any]]) -> tuple:
        """
        Determine classification level based on sensitive data found
        """
        max_level = 'public'
        total_confidence = 0.0
        count = 0
        compliance_frameworks = set()
        
        level_hierarchy = {'public': 0, 'internal': 1, 'confidential': 2, 'restricted': 3}
        
        for data_item in sensitive_data:
            category = data_item.get('category', '')
            occurrences = data_item.get('occurrences', 0)
            
            if category in self.sensitivity_mappings:
                mapping = self.sensitivity_mappings[category]
                level = mapping['level']
                frameworks = mapping['frameworks']
                
                # Update max classification level
                if level_hierarchy[level] > level_hierarchy[max_level]:
                    max_level = level
                
                # Add compliance frameworks
                compliance_frameworks.update(frameworks)
                
                # Calculate confidence based on occurrences
                confidence = min(0.9, 0.5 + (occurrences * 0.1))
                total_confidence += confidence
                count += 1
        
        # Calculate average confidence
        avg_confidence = total_confidence / count if count > 0 else 0.0
        
        return max_level, avg_confidence, list(compliance_frameworks)
    
    def _store_classification_result(self, result: ClassificationResult):
        """
        Store classification result in DynamoDB
        """
        try:
            self.classification_table.put_item(
                Item={
                    'resource_arn': result.resource_arn,
                    'classification_timestamp': result.classification_timestamp,
                    'classification_level': result.classification_level,
                    'sensitive_data_types': result.sensitive_data_types,
                    'confidence_score': str(result.confidence_score),
                    'requires_human_review': result.requires_human_review,
                    'compliance_frameworks': result.compliance_frameworks,
                    'ttl': int((datetime.utcnow() + timedelta(days=365)).timestamp())
                }
            )
            logger.info(f"Stored classification result for {result.resource_arn}")
        except Exception as e:
            logger.error(f"Failed to store classification result: {str(e)}")
    
    def _apply_classification_tags(self, result: ClassificationResult):
        """
        Apply classification tags to AWS resources
        """
        try:
            # Extract bucket name from ARN
            bucket_name = result.resource_arn.split(':')[-1]
            
            # Prepare tags
            tags = {
                'DataClassification': result.classification_level,
                'ClassificationTimestamp': result.classification_timestamp,
                'ConfidenceScore': str(result.confidence_score),
                'AutoClassified': 'true'
            }
            
            # Add compliance framework tags
            if result.compliance_frameworks:
                tags['ComplianceFrameworks'] = ','.join(result.compliance_frameworks)
            
            # Apply tags to S3 bucket
            tag_set = [{'Key': k, 'Value': v} for k, v in tags.items()]
            self.s3_client.put_bucket_tagging(
                Bucket=bucket_name,
                Tagging={'TagSet': tag_set}
            )
            
            logger.info(f"Applied classification tags to {bucket_name}")
            
        except Exception as e:
            logger.error(f"Failed to apply classification tags: {str(e)}")
    
    def _trigger_human_review(self, result: ClassificationResult):
        """
        Trigger human review workflow for uncertain classifications
        """
        try:
            # Prepare review message
            message = {
                'resource_arn': result.resource_arn,
                'classification_level': result.classification_level,
                'confidence_score': result.confidence_score,
                'sensitive_data_types': result.sensitive_data_types,
                'review_required': True,
                'timestamp': result.classification_timestamp
            }
            
            # Send to SNS topic for human review
            self.sns_client.publish(
                TopicArn=f'arn:aws:sns:{self.region}:{self._get_account_id()}:data-classification-review',
                Message=json.dumps(message, indent=2),
                Subject=f'Data Classification Review Required: {result.resource_arn}'
            )
            
            logger.info(f"Triggered human review for {result.resource_arn}")
            
        except Exception as e:
            logger.error(f"Failed to trigger human review: {str(e)}")
    
    def _configure_findings_export(self):
        """
        Configure Macie findings export to S3
        """
        try:
            # This would configure findings export to S3 bucket
            # Implementation depends on your specific requirements
            logger.info("Findings export configuration completed")
        except Exception as e:
            logger.error(f"Failed to configure findings export: {str(e)}")
    
    def _get_account_id(self) -> str:
        """Get AWS account ID"""
        return boto3.client('sts').get_caller_identity()['Account']
    
    def get_classification_metrics(self, days: int = 30) -> Dict[str, Any]:
        """
        Get classification metrics for the specified time period
        """
        try:
            # Calculate date range
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=days)
            
            # Query classification results
            response = self.classification_table.scan(
                FilterExpression='classification_timestamp BETWEEN :start AND :end',
                ExpressionAttributeValues={
                    ':start': start_date.isoformat(),
                    ':end': end_date.isoformat()
                }
            )
            
            items = response['Items']
            
            # Calculate metrics
            metrics = {
                'total_classifications': len(items),
                'by_level': {},
                'by_confidence': {'high': 0, 'medium': 0, 'low': 0},
                'requiring_review': 0,
                'compliance_frameworks': {},
                'average_confidence': 0.0
            }
            
            total_confidence = 0.0
            
            for item in items:
                # Classification level distribution
                level = item['classification_level']
                metrics['by_level'][level] = metrics['by_level'].get(level, 0) + 1
                
                # Confidence distribution
                confidence = float(item['confidence_score'])
                total_confidence += confidence
                
                if confidence >= self.confidence_thresholds['high']:
                    metrics['by_confidence']['high'] += 1
                elif confidence >= self.confidence_thresholds['medium']:
                    metrics['by_confidence']['medium'] += 1
                else:
                    metrics['by_confidence']['low'] += 1
                
                # Review requirements
                if item.get('requires_human_review', False):
                    metrics['requiring_review'] += 1
                
                # Compliance frameworks
                frameworks = item.get('compliance_frameworks', [])
                for framework in frameworks:
                    metrics['compliance_frameworks'][framework] = metrics['compliance_frameworks'].get(framework, 0) + 1
            
            # Calculate average confidence
            if len(items) > 0:
                metrics['average_confidence'] = total_confidence / len(items)
            
            return metrics
            
        except Exception as e:
            logger.error(f"Failed to get classification metrics: {str(e)}")
            return {'error': str(e)}
    
    def reclassify_resources(self, resource_arns: List[str]) -> Dict[str, Any]:
        """
        Trigger reclassification of specified resources
        """
        results = {
            'reclassified': [],
            'failed': [],
            'total': len(resource_arns)
        }
        
        for arn in resource_arns:
            try:
                # Extract bucket name from ARN
                bucket_name = arn.split(':')[-1]
                
                # Create new classification job for this bucket
                job_result = self.create_classification_job(
                    bucket_names=[bucket_name],
                    job_name=f'reclassify-{bucket_name}-{int(time.time())}'
                )
                
                if 'error' not in job_result:
                    results['reclassified'].append({
                        'resource_arn': arn,
                        'job_id': job_result['job_id']
                    })
                else:
                    results['failed'].append({
                        'resource_arn': arn,
                        'error': job_result['error']
                    })
                    
            except Exception as e:
                results['failed'].append({
                    'resource_arn': arn,
                    'error': str(e)
                })
        
        return results

# Example usage and testing
if __name__ == "__main__":
    # Initialize the auto classifier
    classifier = MacieAutoClassifier()
    
    # Set up Macie environment
    print("Setting up Macie environment...")
    setup_result = classifier.setup_macie_environment()
    print(f"Setup result: {setup_result}")
    
    # Create classification job for sample buckets
    sample_buckets = ['my-data-bucket', 'customer-files-bucket']
    job_result = classifier.create_classification_job(
        bucket_names=sample_buckets,
        job_name='automated-classification-job',
        schedule_expression='daily'
    )
    print(f"Classification job result: {job_result}")
    
    # Get classification metrics
    metrics = classifier.get_classification_metrics(days=30)
    print(f"Classification metrics: {json.dumps(metrics, indent=2)}")
```

### Example 2: Event-Driven Real-Time Classification System

```python
# event_driven_classifier.py
import boto3
import json
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ClassificationRule:
    name: str
    pattern: str
    classification_level: str
    confidence_weight: float
    compliance_frameworks: List[str]
    description: str

@dataclass
class ClassificationEvent:
    event_source: str
    resource_arn: str
    event_type: str
    timestamp: str
    metadata: Dict[str, Any]

class EventDrivenClassifier:
    """
    Real-time data classification system triggered by AWS events
    """
    
    def __init__(self, region: str = 'us-east-1'):
        self.region = region
        self.s3_client = boto3.client('s3', region_name=region)
        self.lambda_client = boto3.client('lambda', region_name=region)
        self.eventbridge_client = boto3.client('events', region_name=region)
        self.stepfunctions_client = boto3.client('stepfunctions', region_name=region)
        self.comprehend_client = boto3.client('comprehend', region_name=region)
        self.textract_client = boto3.client('textract', region_name=region)
        self.dynamodb = boto3.resource('dynamodb', region_name=region)
        
        # Classification rules
        self.classification_rules = self._load_classification_rules()
        
        # Real-time classification table
        self.realtime_table = self.dynamodb.Table('realtime-classification-events')
    
    def _load_classification_rules(self) -> List[ClassificationRule]:
        """
        Load classification rules for pattern matching
        """
        return [
            ClassificationRule(
                name="credit_card",
                pattern=r'\b(?:\d{4}[-\s]?){3}\d{4}\b',
                classification_level="restricted",
                confidence_weight=0.9,
                compliance_frameworks=["PCI_DSS"],
                description="Credit card number pattern"
            ),
            ClassificationRule(
                name="ssn",
                pattern=r'\b\d{3}-\d{2}-\d{4}\b',
                classification_level="restricted",
                confidence_weight=0.95,
                compliance_frameworks=["HIPAA", "GDPR"],
                description="Social Security Number pattern"
            ),
            ClassificationRule(
                name="email",
                pattern=r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                classification_level="internal",
                confidence_weight=0.8,
                compliance_frameworks=["GDPR"],
                description="Email address pattern"
            ),
            ClassificationRule(
                name="phone",
                pattern=r'\b(?:\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})\b',
                classification_level="confidential",
                confidence_weight=0.7,
                compliance_frameworks=["GDPR"],
                description="Phone number pattern"
            ),
            ClassificationRule(
                name="ip_address",
                pattern=r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',
                classification_level="internal",
                confidence_weight=0.6,
                compliance_frameworks=[],
                description="IP address pattern"
            ),
            ClassificationRule(
                name="api_key",
                pattern=r'\b[A-Za-z0-9]{32,}\b',
                classification_level="restricted",
                confidence_weight=0.85,
                compliance_frameworks=[],
                description="API key pattern"
            )
        ]
    
    def setup_event_driven_classification(self) -> Dict[str, Any]:
        """
        Set up event-driven classification infrastructure
        """
        setup_results = {
            'eventbridge_rules_created': [],
            'lambda_functions_deployed': [],
            'step_functions_created': [],
            'errors': []
        }
        
        try:
            # Create EventBridge rules for S3 events
            s3_rule_result = self._create_s3_event_rule()
            setup_results['eventbridge_rules_created'].append(s3_rule_result)
            
            # Create EventBridge rules for RDS events
            rds_rule_result = self._create_rds_event_rule()
            setup_results['eventbridge_rules_created'].append(rds_rule_result)
            
            # Deploy classification Lambda functions
            lambda_result = self._deploy_classification_lambda()
            setup_results['lambda_functions_deployed'].append(lambda_result)
            
            # Create Step Functions workflow
            stepfunctions_result = self._create_classification_workflow()
            setup_results['step_functions_created'].append(stepfunctions_result)
            
        except Exception as e:
            setup_results['errors'].append(f"Setup error: {str(e)}")
            logger.error(f"Event-driven classification setup error: {str(e)}")
        
        return setup_results
    
    def _create_s3_event_rule(self) -> Dict[str, Any]:
        """
        Create EventBridge rule for S3 object creation events
        """
        try:
            rule_name = 'S3ObjectCreatedClassification'
            
            # Create EventBridge rule
            self.eventbridge_client.put_rule(
                Name=rule_name,
                EventPattern=json.dumps({
                    "source": ["aws.s3"],
                    "detail-type": ["Object Created"],
                    "detail": {
                        "eventSource": ["s3.amazonaws.com"],
                        "eventName": [
                            "PutObject",
                            "PostObject",
                            "CopyObject",
                            "CompleteMultipartUpload"
                        ]
                    }
                }),
                State='ENABLED',
                Description='Trigger classification on S3 object creation'
            )
            
            # Add Lambda target
            self.eventbridge_client.put_targets(
                Rule=rule_name,
                Targets=[
                    {
                        'Id': '1',
                        'Arn': f'arn:aws:lambda:{self.region}:{self._get_account_id()}:function:realtime-classifier',
                        'InputTransformer': {
                            'InputPathsMap': {
                                'bucket': '$.detail.requestParameters.bucketName',
                                'key': '$.detail.requestParameters.key',
                                'eventName': '$.detail.eventName'
                            },
                            'InputTemplate': '{"bucket": "<bucket>", "key": "<key>", "eventName": "<eventName>", "source": "s3"}'
                        }
                    }
                ]
            )
            
            return {
                'rule_name': rule_name,
                'status': 'created',
                'targets': 1
            }
            
        except Exception as e:
            return {
                'rule_name': 'S3ObjectCreatedClassification',
                'status': 'failed',
                'error': str(e)
            }
    
    def _create_rds_event_rule(self) -> Dict[str, Any]:
        """
        Create EventBridge rule for RDS events
        """
        try:
            rule_name = 'RDSDataChangeClassification'
            
            # Create EventBridge rule for RDS events
            self.eventbridge_client.put_rule(
                Name=rule_name,
                EventPattern=json.dumps({
                    "source": ["aws.rds"],
                    "detail-type": ["RDS DB Instance Event", "RDS DB Cluster Event"],
                    "detail": {
                        "EventCategories": ["configuration change", "backup"]
                    }
                }),
                State='ENABLED',
                Description='Trigger classification on RDS data changes'
            )
            
            # Add Lambda target
            self.eventbridge_client.put_targets(
                Rule=rule_name,
                Targets=[
                    {
                        'Id': '1',
                        'Arn': f'arn:aws:lambda:{self.region}:{self._get_account_id()}:function:realtime-classifier',
                        'InputTransformer': {
                            'InputPathsMap': {
                                'sourceId': '$.detail.SourceId',
                                'eventCategories': '$.detail.EventCategories',
                                'message': '$.detail.Message'
                            },
                            'InputTemplate': '{"sourceId": "<sourceId>", "eventCategories": "<eventCategories>", "message": "<message>", "source": "rds"}'
                        }
                    }
                ]
            )
            
            return {
                'rule_name': rule_name,
                'status': 'created',
                'targets': 1
            }
            
        except Exception as e:
            return {
                'rule_name': 'RDSDataChangeClassification',
                'status': 'failed',
                'error': str(e)
            }
    
    def _deploy_classification_lambda(self) -> Dict[str, Any]:
        """
        Deploy Lambda function for real-time classification
        """
        lambda_code = '''
import json
import boto3
import re
from datetime import datetime

def lambda_handler(event, context):
    """
    Real-time classification Lambda function
    """
    
    # Initialize clients
    s3_client = boto3.client('s3')
    comprehend_client = boto3.client('comprehend')
    
    try:
        source = event.get('source')
        
        if source == 's3':
            return classify_s3_object(event, s3_client, comprehend_client)
        elif source == 'rds':
            return classify_rds_event(event)
        else:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Unknown event source'})
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def classify_s3_object(event, s3_client, comprehend_client):
    """
    Classify S3 object content
    """
    bucket = event['bucket']
    key = event['key']
    
    # Get object content (for text files)
    try:
        response = s3_client.get_object(Bucket=bucket, Key=key)
        content = response['Body'].read().decode('utf-8')
        
        # Perform classification
        classification_result = perform_content_classification(content, comprehend_client)
        
        # Apply tags based on classification
        apply_s3_classification_tags(s3_client, bucket, key, classification_result)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'bucket': bucket,
                'key': key,
                'classification': classification_result
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Classification failed: {str(e)}'})
        }

def perform_content_classification(content, comprehend_client):
    """
    Perform content-based classification
    """
    classification_result = {
        'level': 'public',
        'confidence': 0.0,
        'sensitive_data_types': [],
        'compliance_frameworks': []
    }
    
    # Pattern-based classification
    patterns = {
        'credit_card': r'\\b(?:\\d{4}[-\\s]?){3}\\d{4}\\b',
        'ssn': r'\\b\\d{3}-\\d{2}-\\d{4}\\b',
        'email': r'\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b',
        'phone': r'\\b(?:\\+?1[-\\.\\s]?)?\\(?([0-9]{3})\\)?[-\\.\\s]?([0-9]{3})[-\\.\\s]?([0-9]{4})\\b'
    }
    
    max_level = 'public'
    total_confidence = 0.0
    count = 0
    
    for data_type, pattern in patterns.items():
        matches = re.findall(pattern, content)
        if matches:
            classification_result['sensitive_data_types'].append(data_type)
            
            # Determine classification level
            if data_type in ['credit_card', 'ssn']:
                max_level = 'restricted'
                total_confidence += 0.9
            elif data_type in ['phone']:
                if max_level not in ['restricted']:
                    max_level = 'confidential'
                total_confidence += 0.7
            elif data_type in ['email']:
                if max_level not in ['restricted', 'confidential']:
                    max_level = 'internal'
                total_confidence += 0.6
            
            count += 1
    
    classification_result['level'] = max_level
    classification_result['confidence'] = total_confidence / count if count > 0 else 0.0
    
    return classification_result

def apply_s3_classification_tags(s3_client, bucket, key, classification_result):
    """
    Apply classification tags to S3 object
    """
    tags = {
        'DataClassification': classification_result['level'],
        'ClassificationConfidence': str(classification_result['confidence']),
        'ClassificationTimestamp': datetime.utcnow().isoformat(),
        'AutoClassified': 'true'
    }
    
    if classification_result['sensitive_data_types']:
        tags['SensitiveDataTypes'] = ','.join(classification_result['sensitive_data_types'])
    
    # Apply tags to object
    tag_set = [{'Key': k, 'Value': v} for k, v in tags.items()]
    s3_client.put_object_tagging(
        Bucket=bucket,
        Key=key,
        Tagging={'TagSet': tag_set}
    )

def classify_rds_event(event):
    """
    Handle RDS classification events
    """
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'RDS event processed',
            'sourceId': event.get('sourceId'),
            'eventCategories': event.get('eventCategories')
        })
    }
'''
        
        try:
            # Create Lambda function
            response = self.lambda_client.create_function(
                FunctionName='realtime-classifier',
                Runtime='python3.9',
                Role=f'arn:aws:iam::{self._get_account_id()}:role/lambda-classification-role',
                Handler='index.lambda_handler',
                Code={'ZipFile': lambda_code.encode()},
                Description='Real-time data classification function',
                Timeout=300,
                MemorySize=512,
                Environment={
                    'Variables': {
                        'REGION': self.region
                    }
                },
                Tags={
                    'Purpose': 'DataClassification',
                    'Environment': 'Production'
                }
            )
            
            return {
                'function_name': 'realtime-classifier',
                'function_arn': response['FunctionArn'],
                'status': 'created'
            }
            
        except self.lambda_client.exceptions.ResourceConflictException:
            # Function already exists, update it
            self.lambda_client.update_function_code(
                FunctionName='realtime-classifier',
                ZipFile=lambda_code.encode()
            )
            
            return {
                'function_name': 'realtime-classifier',
                'status': 'updated'
            }
        except Exception as e:
            return {
                'function_name': 'realtime-classifier',
                'status': 'failed',
                'error': str(e)
            }
    
    def _create_classification_workflow(self) -> Dict[str, Any]:
        """
        Create Step Functions workflow for complex classification scenarios
        """
        workflow_definition = {
            "Comment": "Data classification workflow",
            "StartAt": "ClassifyContent",
            "States": {
                "ClassifyContent": {
                    "Type": "Task",
                    "Resource": f"arn:aws:lambda:{self.region}:{self._get_account_id()}:function:realtime-classifier",
                    "Next": "EvaluateConfidence"
                },
                "EvaluateConfidence": {
                    "Type": "Choice",
                    "Choices": [
                        {
                            "Variable": "$.classification.confidence",
                            "NumericGreaterThan": 0.8,
                            "Next": "ApplyClassification"
                        },
                        {
                            "Variable": "$.classification.confidence",
                            "NumericLessThan": 0.5,
                            "Next": "RequestHumanReview"
                        }
                    ],
                    "Default": "ApplyClassificationWithMonitoring"
                },
                "ApplyClassification": {
                    "Type": "Task",
                    "Resource": "arn:aws:states:::aws-sdk:s3:putObjectTagging",
                    "End": True
                },
                "ApplyClassificationWithMonitoring": {
                    "Type": "Parallel",
                    "Branches": [
                        {
                            "StartAt": "ApplyTags",
                            "States": {
                                "ApplyTags": {
                                    "Type": "Task",
                                    "Resource": "arn:aws:states:::aws-sdk:s3:putObjectTagging",
                                    "End": True
                                }
                            }
                        },
                        {
                            "StartAt": "SetupMonitoring",
                            "States": {
                                "SetupMonitoring": {
                                    "Type": "Task",
                                    "Resource": "arn:aws:states:::aws-sdk:cloudwatch:putMetricData",
                                    "End": True
                                }
                            }
                        }
                    ],
                    "End": True
                },
                "RequestHumanReview": {
                    "Type": "Task",
                    "Resource": "arn:aws:states:::sns:publish",
                    "Parameters": {
                        "TopicArn": f"arn:aws:sns:{self.region}:{self._get_account_id()}:classification-review",
                        "Message.$": "$"
                    },
                    "End": True
                }
            }
        }
        
        try:
            response = self.stepfunctions_client.create_state_machine(
                name='DataClassificationWorkflow',
                definition=json.dumps(workflow_definition),
                roleArn=f'arn:aws:iam::{self._get_account_id()}:role/stepfunctions-classification-role',
                type='STANDARD',
                tags=[
                    {
                        'key': 'Purpose',
                        'value': 'DataClassification'
                    }
                ]
            )
            
            return {
                'state_machine_name': 'DataClassificationWorkflow',
                'state_machine_arn': response['stateMachineArn'],
                'status': 'created'
            }
            
        except Exception as e:
            return {
                'state_machine_name': 'DataClassificationWorkflow',
                'status': 'failed',
                'error': str(e)
            }
    
    def process_realtime_event(self, event: ClassificationEvent) -> Dict[str, Any]:
        """
        Process real-time classification event
        """
        try:
            # Store event for tracking
            self.realtime_table.put_item(
                Item={
                    'event_id': f"{event.event_source}-{event.resource_arn}-{event.timestamp}",
                    'event_source': event.event_source,
                    'resource_arn': event.resource_arn,
                    'event_type': event.event_type,
                    'timestamp': event.timestamp,
                    'metadata': event.metadata,
                    'processing_status': 'received'
                }
            )
            
            # Determine processing approach based on event source
            if event.event_source == 's3':
                return self._process_s3_event(event)
            elif event.event_source == 'rds':
                return self._process_rds_event(event)
            elif event.event_source == 'dynamodb':
                return self._process_dynamodb_event(event)
            else:
                return {
                    'status': 'unsupported',
                    'message': f'Event source {event.event_source} not supported'
                }
                
        except Exception as e:
            logger.error(f"Error processing real-time event: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _process_s3_event(self, event: ClassificationEvent) -> Dict[str, Any]:
        """
        Process S3 object creation/modification event
        """
        try:
            # Extract bucket and key from resource ARN
            arn_parts = event.resource_arn.split(':')
            bucket_name = arn_parts[-1].split('/')[0]
            object_key = '/'.join(arn_parts[-1].split('/')[1:])
            
            # Get object metadata
            response = self.s3_client.head_object(Bucket=bucket_name, Key=object_key)
            content_type = response.get('ContentType', '')
            content_length = response.get('ContentLength', 0)
            
            # Determine if object should be classified
            if self._should_classify_object(content_type, content_length):
                # Start Step Functions workflow
                workflow_input = {
                    'bucket': bucket_name,
                    'key': object_key,
                    'contentType': content_type,
                    'contentLength': content_length,
                    'eventTimestamp': event.timestamp
                }
                
                self.stepfunctions_client.start_execution(
                    stateMachineArn=f'arn:aws:states:{self.region}:{self._get_account_id()}:stateMachine:DataClassificationWorkflow',
                    name=f'classify-{bucket_name}-{object_key.replace("/", "-")}-{int(datetime.now().timestamp())}',
                    input=json.dumps(workflow_input)
                )
                
                return {
                    'status': 'classification_started',
                    'bucket': bucket_name,
                    'key': object_key,
                    'workflow_started': True
                }
            else:
                return {
                    'status': 'skipped',
                    'reason': 'Object does not require classification',
                    'bucket': bucket_name,
                    'key': object_key
                }
                
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _process_rds_event(self, event: ClassificationEvent) -> Dict[str, Any]:
        """
        Process RDS event for potential data classification
        """
        # RDS events typically don't contain data content directly
        # This would trigger metadata-based classification or schedule full scans
        return {
            'status': 'metadata_classification',
            'message': 'RDS event processed for metadata classification'
        }
    
    def _process_dynamodb_event(self, event: ClassificationEvent) -> Dict[str, Any]:
        """
        Process DynamoDB event for data classification
        """
        # DynamoDB events can contain actual data changes
        # This would analyze the changed data for sensitive content
        return {
            'status': 'content_classification',
            'message': 'DynamoDB event processed for content classification'
        }
    
    def _should_classify_object(self, content_type: str, content_length: int) -> bool:
        """
        Determine if an S3 object should be classified
        """
        # Skip very large files or binary files that can't be easily analyzed
        if content_length > 100 * 1024 * 1024:  # 100MB limit
            return False
        
        # Only classify text-based content types
        text_types = [
            'text/',
            'application/json',
            'application/xml',
            'application/csv',
            'application/pdf'
        ]
        
        return any(content_type.startswith(t) for t in text_types)
    
    def _get_account_id(self) -> str:
        """Get AWS account ID"""
        return boto3.client('sts').get_caller_identity()['Account']
    
    def get_realtime_classification_stats(self, hours: int = 24) -> Dict[str, Any]:
        """
        Get real-time classification statistics
        """
        try:
            # Calculate time range
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(hours=hours)
            
            # Query events from the specified time range
            response = self.realtime_table.scan(
                FilterExpression='#ts BETWEEN :start AND :end',
                ExpressionAttributeNames={'#ts': 'timestamp'},
                ExpressionAttributeValues={
                    ':start': start_time.isoformat(),
                    ':end': end_time.isoformat()
                }
            )
            
            events = response['Items']
            
            # Calculate statistics
            stats = {
                'total_events': len(events),
                'by_source': {},
                'by_type': {},
                'processing_status': {},
                'hourly_distribution': {}
            }
            
            for event in events:
                # Source distribution
                source = event['event_source']
                stats['by_source'][source] = stats['by_source'].get(source, 0) + 1
                
                # Type distribution
                event_type = event['event_type']
                stats['by_type'][event_type] = stats['by_type'].get(event_type, 0) + 1
                
                # Processing status
                status = event.get('processing_status', 'unknown')
                stats['processing_status'][status] = stats['processing_status'].get(status, 0) + 1
                
                # Hourly distribution
                event_hour = datetime.fromisoformat(event['timestamp']).strftime('%Y-%m-%d %H:00')
                stats['hourly_distribution'][event_hour] = stats['hourly_distribution'].get(event_hour, 0) + 1
            
            return stats
            
        except Exception as e:
            logger.error(f"Failed to get real-time classification stats: {str(e)}")
            return {'error': str(e)}

# Example usage
if __name__ == "__main__":
    # Initialize event-driven classifier
    classifier = EventDrivenClassifier()
    
    # Set up event-driven classification
    print("Setting up event-driven classification...")
    setup_result = classifier.setup_event_driven_classification()
    print(f"Setup result: {setup_result}")
    
    # Example event processing
    sample_event = ClassificationEvent(
        event_source='s3',
        resource_arn='arn:aws:s3:::my-bucket/sensitive-data.txt',
        event_type='ObjectCreated',
        timestamp=datetime.utcnow().isoformat(),
        metadata={'contentType': 'text/plain', 'size': 1024}
    )
    
    result = classifier.process_realtime_event(sample_event)
    print(f"Event processing result: {result}")
    
    # Get real-time statistics
    stats = classifier.get_realtime_classification_stats(hours=24)
    print(f"Real-time classification stats: {json.dumps(stats, indent=2)}")
```

### Example 3: Multi-Service Classification Orchestration

```yaml
# classification-orchestration.yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Multi-service automated data classification orchestration'

Parameters:
  Environment:
    Type: String
    Default: 'prod'
    AllowedValues: ['dev', 'staging', 'prod']
    Description: 'Environment for deployment'
  
  ClassificationSchedule:
    Type: String
    Default: 'rate(1 hour)'
    Description: 'Schedule expression for automated classification jobs'

Resources:
  # DynamoDB table for classification results
  ClassificationResultsTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: !Sub '${Environment}-classification-results'
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: resource_arn
          AttributeType: S
        - AttributeName: classification_timestamp
          AttributeType: S
        - AttributeName: classification_level
          AttributeType: S
      KeySchema:
        - AttributeName: resource_arn
          KeyType: HASH
        - AttributeName: classification_timestamp
          KeyType: RANGE
      GlobalSecondaryIndexes:
        - IndexName: ClassificationLevelIndex
          KeySchema:
            - AttributeName: classification_level
              KeyType: HASH
            - AttributeName: classification_timestamp
              KeyType: RANGE
          Projection:
            ProjectionType: ALL
      StreamSpecification:
        StreamViewType: NEW_AND_OLD_IMAGES
      TimeToLiveSpecification:
        AttributeName: ttl
        Enabled: true
      Tags:
        - Key: Environment
          Value: !Ref Environment
        - Key: Purpose
          Value: DataClassification

  # Lambda function for classification orchestration
  ClassificationOrchestratorFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: !Sub '${Environment}-classification-orchestrator'
      Runtime: python3.9
      Handler: index.lambda_handler
      Role: !GetAtt ClassificationOrchestratorRole.Arn
      Timeout: 900
      MemorySize: 1024
      Environment:
        Variables:
          ENVIRONMENT: !Ref Environment
          CLASSIFICATION_TABLE: !Ref ClassificationResultsTable
          MACIE_REGION: !Ref AWS::Region
      Code:
        ZipFile: |
          import boto3
          import json
          import os
          from datetime import datetime, timedelta
          import logging
          
          logger = logging.getLogger()
          logger.setLevel(logging.INFO)
          
          def lambda_handler(event, context):
              """
              Orchestrate multi-service data classification
              """
              
              # Initialize clients
              macie_client = boto3.client('macie2')
              s3_client = boto3.client('s3')
              rds_client = boto3.client('rds')
              comprehend_client = boto3.client('comprehend')
              dynamodb = boto3.resource('dynamodb')
              
              table = dynamodb.Table(os.environ['CLASSIFICATION_TABLE'])
              
              try:
                  # Get list of resources to classify
                  resources_to_classify = discover_resources_for_classification()
                  
                  results = {
                      'total_resources': len(resources_to_classify),
                      'classification_jobs_started': [],
                      'errors': []
                  }
                  
                  for resource in resources_to_classify:
                      try:
                          if resource['type'] == 's3':
                              job_result = start_s3_classification(macie_client, resource)
                              results['classification_jobs_started'].append(job_result)
                          elif resource['type'] == 'rds':
                              job_result = start_rds_classification(rds_client, comprehend_client, resource)
                              results['classification_jobs_started'].append(job_result)
                          
                      except Exception as e:
                          results['errors'].append({
                              'resource': resource,
                              'error': str(e)
                          })
                  
                  return {
                      'statusCode': 200,
                      'body': json.dumps(results)
                  }
                  
              except Exception as e:
                  logger.error(f"Orchestration error: {str(e)}")
                  return {
                      'statusCode': 500,
                      'body': json.dumps({'error': str(e)})
                  }
          
          def discover_resources_for_classification():
              """
              Discover AWS resources that need classification
              """
              s3_client = boto3.client('s3')
              rds_client = boto3.client('rds')
              
              resources = []
              
              # Discover S3 buckets
              try:
                  buckets_response = s3_client.list_buckets()
                  for bucket in buckets_response['Buckets']:
                      # Check if bucket needs classification
                      if should_classify_bucket(s3_client, bucket['Name']):
                          resources.append({
                              'type': 's3',
                              'name': bucket['Name'],
                              'arn': f"arn:aws:s3:::{bucket['Name']}",
                              'last_modified': bucket['CreationDate'].isoformat()
                          })
              except Exception as e:
                  logger.error(f"Error discovering S3 buckets: {str(e)}")
              
              # Discover RDS instances
              try:
                  rds_response = rds_client.describe_db_instances()
                  for db_instance in rds_response['DBInstances']:
                      if should_classify_rds_instance(db_instance):
                          resources.append({
                              'type': 'rds',
                              'name': db_instance['DBInstanceIdentifier'],
                              'arn': db_instance['DBInstanceArn'],
                              'engine': db_instance['Engine']
                          })
              except Exception as e:
                  logger.error(f"Error discovering RDS instances: {str(e)}")
              
              return resources
          
          def should_classify_bucket(s3_client, bucket_name):
              """
              Determine if S3 bucket should be classified
              """
              try:
                  # Check if bucket has classification tags
                  tags_response = s3_client.get_bucket_tagging(Bucket=bucket_name)
                  tags = {tag['Key']: tag['Value'] for tag in tags_response['TagSet']}
                  
                  # Skip if already classified recently
                  if 'DataClassification' in tags and 'ClassificationTimestamp' in tags:
                      classification_time = datetime.fromisoformat(tags['ClassificationTimestamp'])
                      if datetime.utcnow() - classification_time < timedelta(days=7):
                          return False
                  
                  return True
                  
              except s3_client.exceptions.NoSuchTagSet:
                  return True
              except Exception as e:
                  logger.error(f"Error checking bucket {bucket_name}: {str(e)}")
                  return False
          
          def should_classify_rds_instance(db_instance):
              """
              Determine if RDS instance should be classified
              """
              # Check tags for recent classification
              tags = {tag['Key']: tag['Value'] for tag in db_instance.get('TagList', [])}
              
              if 'DataClassification' in tags and 'ClassificationTimestamp' in tags:
                  classification_time = datetime.fromisoformat(tags['ClassificationTimestamp'])
                  if datetime.utcnow() - classification_time < timedelta(days=30):
                      return False
              
              return True
          
          def start_s3_classification(macie_client, resource):
              """
              Start Macie classification job for S3 bucket
              """
              job_name = f"auto-classify-{resource['name']}-{int(datetime.utcnow().timestamp())}"
              
              response = macie_client.create_classification_job(
                  name=job_name,
                  jobType='ONE_TIME',
                  s3JobDefinition={
                      'bucketCriteria': {
                          'includes': {
                              'and': [
                                  {
                                      'simpleCriterion': {
                                          'comparator': 'EQ',
                                          'key': 'BUCKET_NAME',
                                          'values': [resource['name']]
                                      }
                                  }
                              ]
                          }
                      }
                  },
                  samplingPercentage=100
              )
              
              return {
                  'resource_type': 's3',
                  'resource_name': resource['name'],
                  'job_id': response['jobId'],
                  'job_name': job_name
              }
          
          def start_rds_classification(rds_client, comprehend_client, resource):
              """
              Start RDS classification process
              """
              # For RDS, we would typically:
              # 1. Create a snapshot
              # 2. Export data to S3
              # 3. Run classification on exported data
              # This is a simplified placeholder
              
              return {
                  'resource_type': 'rds',
                  'resource_name': resource['name'],
                  'status': 'metadata_classification_started'
              }
      Tags:
        - Key: Environment
          Value: !Ref Environment
        - Key: Purpose
          Value: DataClassification

  # IAM role for classification orchestrator
  ClassificationOrchestratorRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: !Sub '${Environment}-classification-orchestrator-role'
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
        - PolicyName: ClassificationOrchestratorPolicy
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - macie2:*
                  - s3:ListAllMyBuckets
                  - s3:GetBucketTagging
                  - s3:PutBucketTagging
                  - s3:GetObject
                  - s3:ListBucket
                  - rds:DescribeDBInstances
                  - rds:DescribeDBClusters
                  - rds:ListTagsForResource
                  - rds:AddTagsToResource
                  - comprehend:*
                  - dynamodb:PutItem
                  - dynamodb:GetItem
                  - dynamodb:Query
                  - dynamodb:Scan
                  - dynamodb:UpdateItem
                Resource: '*'
      Tags:
        - Key: Environment
          Value: !Ref Environment

  # EventBridge rule for scheduled classification
  ClassificationScheduleRule:
    Type: AWS::Events::Rule
    Properties:
      Name: !Sub '${Environment}-classification-schedule'
      Description: 'Scheduled automated data classification'
      ScheduleExpression: !Ref ClassificationSchedule
      State: ENABLED
      Targets:
        - Arn: !GetAtt ClassificationOrchestratorFunction.Arn
          Id: ClassificationOrchestratorTarget
          Input: !Sub |
            {
              "source": "scheduled",
              "environment": "${Environment}",
              "timestamp": "{{aws.events.event.ingestion-time}}"
            }

  # Permission for EventBridge to invoke Lambda
  ClassificationSchedulePermission:
    Type: AWS::Lambda::Permission
    Properties:
      FunctionName: !Ref ClassificationOrchestratorFunction
      Action: lambda:InvokeFunction
      Principal: events.amazonaws.com
      SourceArn: !GetAtt ClassificationScheduleRule.Arn

  # SNS topic for classification notifications
  ClassificationNotificationTopic:
    Type: AWS::SNS::Topic
    Properties:
      TopicName: !Sub '${Environment}-classification-notifications'
      DisplayName: 'Data Classification Notifications'
      Tags:
        - Key: Environment
          Value: !Ref Environment
        - Key: Purpose
          Value: DataClassification

  # Lambda function for processing classification results
  ClassificationResultsProcessor:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: !Sub '${Environment}-classification-results-processor'
      Runtime: python3.9
      Handler: index.lambda_handler
      Role: !GetAtt ClassificationResultsProcessorRole.Arn
      Timeout: 300
      Environment:
        Variables:
          ENVIRONMENT: !Ref Environment
          NOTIFICATION_TOPIC: !Ref ClassificationNotificationTopic
      Code:
        ZipFile: |
          import boto3
          import json
          import os
          from datetime import datetime
          import logging
          
          logger = logging.getLogger()
          logger.setLevel(logging.INFO)
          
          def lambda_handler(event, context):
              """
              Process classification results from DynamoDB stream
              """
              
              sns_client = boto3.client('sns')
              s3_client = boto3.client('s3')
              
              try:
                  for record in event['Records']:
                      if record['eventName'] in ['INSERT', 'MODIFY']:
                          # Process new or updated classification result
                          classification_result = record['dynamodb']['NewImage']
                          
                          # Extract classification details
                          resource_arn = classification_result['resource_arn']['S']
                          classification_level = classification_result['classification_level']['S']
                          confidence_score = float(classification_result.get('confidence_score', {}).get('N', '0'))
                          
                          # Apply protection controls based on classification
                          apply_protection_controls(s3_client, resource_arn, classification_level)
                          
                          # Send notification for high-risk classifications
                          if classification_level in ['confidential', 'restricted'] or confidence_score < 0.7:
                              send_classification_notification(
                                  sns_client, 
                                  resource_arn, 
                                  classification_level, 
                                  confidence_score
                              )
                  
                  return {
                      'statusCode': 200,
                      'body': json.dumps({'message': 'Classification results processed successfully'})
                  }
                  
              except Exception as e:
                  logger.error(f"Error processing classification results: {str(e)}")
                  return {
                      'statusCode': 500,
                      'body': json.dumps({'error': str(e)})
                  }
          
          def apply_protection_controls(s3_client, resource_arn, classification_level):
              """
              Apply protection controls based on classification level
              """
              try:
                  # Extract bucket name from ARN
                  bucket_name = resource_arn.split(':')[-1]
                  
                  # Define protection controls based on classification
                  protection_controls = {
                      'public': {'encryption': False, 'public_access': True},
                      'internal': {'encryption': True, 'public_access': False},
                      'confidential': {'encryption': True, 'public_access': False, 'versioning': True},
                      'restricted': {'encryption': True, 'public_access': False, 'versioning': True, 'mfa_delete': True}
                  }
                  
                  controls = protection_controls.get(classification_level, protection_controls['internal'])
                  
                  # Apply encryption if required
                  if controls.get('encryption', False):
                      s3_client.put_bucket_encryption(
                          Bucket=bucket_name,
                          ServerSideEncryptionConfiguration={
                              'Rules': [
                                  {
                                      'ApplyServerSideEncryptionByDefault': {
                                          'SSEAlgorithm': 'aws:kms' if classification_level == 'restricted' else 'AES256'
                                      }
                                  }
                              ]
                          }
                      )
                  
                  # Block public access if required
                  if not controls.get('public_access', False):
                      s3_client.put_public_access_block(
                          Bucket=bucket_name,
                          PublicAccessBlockConfiguration={
                              'BlockPublicAcls': True,
                              'IgnorePublicAcls': True,
                              'BlockPublicPolicy': True,
                              'RestrictPublicBuckets': True
                          }
                      )
                  
                  # Enable versioning if required
                  if controls.get('versioning', False):
                      s3_client.put_bucket_versioning(
                          Bucket=bucket_name,
                          VersioningConfiguration={'Status': 'Enabled'}
                      )
                  
                  logger.info(f"Applied protection controls to {bucket_name} for classification {classification_level}")
                  
              except Exception as e:
                  logger.error(f"Error applying protection controls: {str(e)}")
          
          def send_classification_notification(sns_client, resource_arn, classification_level, confidence_score):
              """
              Send notification for classification results requiring attention
              """
              try:
                  message = {
                      'resource_arn': resource_arn,
                      'classification_level': classification_level,
                      'confidence_score': confidence_score,
                      'timestamp': datetime.utcnow().isoformat(),
                      'action_required': confidence_score < 0.7
                  }
                  
                  sns_client.publish(
                      TopicArn=os.environ['NOTIFICATION_TOPIC'],
                      Message=json.dumps(message, indent=2),
                      Subject=f'Data Classification Alert: {classification_level} - {resource_arn}'
                  )
                  
                  logger.info(f"Sent classification notification for {resource_arn}")
                  
              except Exception as e:
                  logger.error(f"Error sending notification: {str(e)}")
      Tags:
        - Key: Environment
          Value: !Ref Environment
        - Key: Purpose
          Value: DataClassification

  # IAM role for classification results processor
  ClassificationResultsProcessorRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: !Sub '${Environment}-classification-results-processor-role'
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
        - PolicyName: ClassificationResultsProcessorPolicy
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - dynamodb:DescribeStream
                  - dynamodb:GetRecords
                  - dynamodb:GetShardIterator
                  - dynamodb:ListStreams
                  - s3:PutBucketEncryption
                  - s3:PutPublicAccessBlock
                  - s3:PutBucketVersioning
                  - s3:PutBucketTagging
                  - sns:Publish
                Resource: '*'
      Tags:
        - Key: Environment
          Value: !Ref Environment

  # Event source mapping for DynamoDB stream
  ClassificationResultsStreamMapping:
    Type: AWS::Lambda::EventSourceMapping
    Properties:
      EventSourceArn: !GetAtt ClassificationResultsTable.StreamArn
      FunctionName: !Ref ClassificationResultsProcessor
      StartingPosition: LATEST
      BatchSize: 10
      MaximumBatchingWindowInSeconds: 5

  # CloudWatch dashboard for classification monitoring
  ClassificationDashboard:
    Type: AWS::CloudWatch::Dashboard
    Properties:
      DashboardName: !Sub '${Environment}-data-classification-dashboard'
      DashboardBody: !Sub |
        {
          "widgets": [
            {
              "type": "metric",
              "x": 0,
              "y": 0,
              "width": 12,
              "height": 6,
              "properties": {
                "metrics": [
                  [ "AWS/Lambda", "Invocations", "FunctionName", "${ClassificationOrchestratorFunction}" ],
                  [ ".", "Errors", ".", "." ],
                  [ ".", "Duration", ".", "." ]
                ],
                "period": 300,
                "stat": "Sum",
                "region": "${AWS::Region}",
                "title": "Classification Orchestrator Metrics"
              }
            },
            {
              "type": "metric",
              "x": 12,
              "y": 0,
              "width": 12,
              "height": 6,
              "properties": {
                "metrics": [
                  [ "AWS/Lambda", "Invocations", "FunctionName", "${ClassificationResultsProcessor}" ],
                  [ ".", "Errors", ".", "." ]
                ],
                "period": 300,
                "stat": "Sum",
                "region": "${AWS::Region}",
                "title": "Results Processor Metrics"
              }
            }
          ]
        }

Outputs:
  ClassificationTableName:
    Description: 'Name of the classification results table'
    Value: !Ref ClassificationResultsTable
    Export:
      Name: !Sub '${AWS::StackName}-ClassificationTable'
  
  OrchestratorFunctionArn:
    Description: 'ARN of the classification orchestrator function'
    Value: !GetAtt ClassificationOrchestratorFunction.Arn
    Export:
      Name: !Sub '${AWS::StackName}-OrchestratorFunction'
  
  NotificationTopicArn:
    Description: 'ARN of the classification notification topic'
    Value: !Ref ClassificationNotificationTopic
    Export:
      Name: !Sub '${AWS::StackName}-NotificationTopic'
  
  DashboardURL:
    Description: 'URL of the classification monitoring dashboard'
    Value: !Sub 'https://${AWS::Region}.console.aws.amazon.com/cloudwatch/home?region=${AWS::Region}#dashboards:name=${Environment}-data-classification-dashboard'
```

### Example 4: Machine Learning-Based Classification Pipeline

```python
# ml_classification_pipeline.py
import boto3
import json
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging
import pickle
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class TrainingData:
    content: str
    classification_level: str
    sensitive_data_types: List[str]
    confidence_score: float
    source: str

@dataclass
class ClassificationPrediction:
    classification_level: str
    confidence_score: float
    feature_importance: Dict[str, float]
    sensitive_patterns_detected: List[str]
    recommendation: str

class MLClassificationPipeline:
    """
    Machine Learning-based data classification pipeline
    """
    
    def __init__(self, region: str = 'us-east-1'):
        self.region = region
        self.s3_client = boto3.client('s3', region_name=region)
        self.sagemaker_client = boto3.client('sagemaker', region_name=region)
        self.comprehend_client = boto3.client('comprehend', region_name=region)
        self.dynamodb = boto3.resource('dynamodb', region_name=region)
        
        # ML model components
        self.vectorizer = None
        self.classifier = None
        self.model_version = None
        self.feature_names = None
        
        # Training data table
        self.training_table = self.dynamodb.Table('ml-classification-training-data')
        
        # Sensitive data patterns
        self.sensitive_patterns = {
            'credit_card': r'\b(?:\d{4}[-\s]?){3}\d{4}\b',
            'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'\b(?:\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})\b',
            'ip_address': r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',
            'api_key': r'\b[A-Za-z0-9]{32,}\b',
            'aws_access_key': r'\bAKIA[0-9A-Z]{16}\b',
            'private_key': r'-----BEGIN [A-Z ]+PRIVATE KEY-----',
            'passport': r'\b[A-Z]{1,2}[0-9]{6,9}\b',
            'bank_account': r'\b[0-9]{8,17}\b'
        }
    
    def collect_training_data(self, days: int = 30) -> List[TrainingData]:
        """
        Collect training data from various sources
        """
        training_data = []
        
        try:
            # Collect data from Macie findings
            macie_data = self._collect_macie_training_data(days)
            training_data.extend(macie_data)
            
            # Collect data from manual classifications
            manual_data = self._collect_manual_training_data(days)
            training_data.extend(manual_data)
            
            # Collect data from existing classifications
            existing_data = self._collect_existing_classification_data(days)
            training_data.extend(existing_data)
            
            logger.info(f"Collected {len(training_data)} training samples")
            
        except Exception as e:
            logger.error(f"Error collecting training data: {str(e)}")
        
        return training_data
    
    def _collect_macie_training_data(self, days: int) -> List[TrainingData]:
        """
        Collect training data from Macie findings
        """
        training_data = []
        
        try:
            macie_client = boto3.client('macie2', region_name=self.region)
            
            # Get Macie findings from the last N days
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=days)
            
            findings_response = macie_client.get_findings(
                findingCriteria={
                    'criterion': {
                        'createdAt': {
                            'gte': start_date.isoformat(),
                            'lte': end_date.isoformat()
                        }
                    }
                }
            )
            
            for finding in findings_response['findings']:
                # Extract content sample and classification details
                sensitive_data = finding.get('classificationDetails', {}).get('result', {}).get('sensitiveData', [])
                
                if sensitive_data:
                    # Determine classification level based on sensitive data types
                    classification_level = self._determine_classification_from_sensitive_data(sensitive_data)
                    sensitive_types = [item.get('category', '') for item in sensitive_data]
                    
                    # Create training sample
                    training_sample = TrainingData(
                        content=self._extract_content_sample(finding),
                        classification_level=classification_level,
                        sensitive_data_types=sensitive_types,
                        confidence_score=0.9,  # High confidence for Macie findings
                        source='macie'
                    )
                    
                    training_data.append(training_sample)
            
        except Exception as e:
            logger.error(f"Error collecting Macie training data: {str(e)}")
        
        return training_data
    
    def _collect_manual_training_data(self, days: int) -> List[TrainingData]:
        """
        Collect training data from manual classifications
        """
        training_data = []
        
        try:
            # Query manual classification records from DynamoDB
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=days)
            
            response = self.training_table.scan(
                FilterExpression='#source = :source AND #timestamp BETWEEN :start AND :end',
                ExpressionAttributeNames={
                    '#source': 'source',
                    '#timestamp': 'timestamp'
                },
                ExpressionAttributeValues={
                    ':source': 'manual',
                    ':start': start_date.isoformat(),
                    ':end': end_date.isoformat()
                }
            )
            
            for item in response['Items']:
                training_sample = TrainingData(
                    content=item['content'],
                    classification_level=item['classification_level'],
                    sensitive_data_types=item.get('sensitive_data_types', []),
                    confidence_score=float(item.get('confidence_score', 1.0)),
                    source='manual'
                )
                training_data.append(training_sample)
            
        except Exception as e:
            logger.error(f"Error collecting manual training data: {str(e)}")
        
        return training_data
    
    def _collect_existing_classification_data(self, days: int) -> List[TrainingData]:
        """
        Collect training data from existing automated classifications
        """
        training_data = []
        
        try:
            # Query existing classification results
            classification_table = self.dynamodb.Table('data-classification-results')
            
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=days)
            
            response = classification_table.scan(
                FilterExpression='classification_timestamp BETWEEN :start AND :end AND confidence_score > :min_confidence',
                ExpressionAttributeValues={
                    ':start': start_date.isoformat(),
                    ':end': end_date.isoformat(),
                    ':min_confidence': '0.8'  # Only use high-confidence classifications
                }
            )
            
            for item in response['Items']:
                # Get content sample for this resource
                content_sample = self._get_content_sample_for_resource(item['resource_arn'])
                
                if content_sample:
                    training_sample = TrainingData(
                        content=content_sample,
                        classification_level=item['classification_level'],
                        sensitive_data_types=item.get('sensitive_data_types', []),
                        confidence_score=float(item['confidence_score']),
                        source='automated'
                    )
                    training_data.append(training_sample)
            
        except Exception as e:
            logger.error(f"Error collecting existing classification data: {str(e)}")
        
        return training_data
    
    def train_classification_model(self, training_data: List[TrainingData]) -> Dict[str, Any]:
        """
        Train machine learning model for data classification
        """
        try:
            # Prepare training data
            X, y = self._prepare_training_features(training_data)
            
            if len(X) < 10:
                return {
                    'status': 'insufficient_data',
                    'message': f'Need at least 10 training samples, got {len(X)}'
                }
            
            # Split data for training and validation
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y
            )
            
            # Train TF-IDF vectorizer
            self.vectorizer = TfidfVectorizer(
                max_features=10000,
                ngram_range=(1, 3),
                stop_words='english',
                lowercase=True
            )
            
            X_train_vectorized = self.vectorizer.fit_transform(X_train)
            X_test_vectorized = self.vectorizer.transform(X_test)
            
            # Train Random Forest classifier
            self.classifier = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                class_weight='balanced'
            )
            
            self.classifier.fit(X_train_vectorized, y_train)
            
            # Evaluate model
            y_pred = self.classifier.predict(X_test_vectorized)
            
            # Generate evaluation metrics
            evaluation_results = {
                'classification_report': classification_report(y_test, y_pred, output_dict=True),
                'confusion_matrix': confusion_matrix(y_test, y_pred).tolist(),
                'feature_importance': self._get_feature_importance(),
                'training_samples': len(training_data),
                'model_version': datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            }
            
            # Save model
            self._save_model()
            
            logger.info(f"Model trained successfully with {len(training_data)} samples")
            
            return {
                'status': 'success',
                'evaluation': evaluation_results
            }
            
        except Exception as e:
            logger.error(f"Error training classification model: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _prepare_training_features(self, training_data: List[TrainingData]) -> Tuple[List[str], List[str]]:
        """
        Prepare features and labels for training
        """
        X = []  # Features (text content)
        y = []  # Labels (classification levels)
        
        for sample in training_data:
            # Extract features from content
            features = self._extract_text_features(sample.content)
            X.append(features)
            y.append(sample.classification_level)
        
        return X, y
    
    def _extract_text_features(self, content: str) -> str:
        """
        Extract text features for classification
        """
        # Combine original content with pattern-based features
        features = content
        
        # Add pattern detection results as features
        for pattern_name, pattern in self.sensitive_patterns.items():
            matches = len(re.findall(pattern, content, re.IGNORECASE))
            if matches > 0:
                features += f" {pattern_name}_detected_{matches}"
        
        # Add content-based features
        features += f" content_length_{len(content)}"
        features += f" word_count_{len(content.split())}"
        features += f" numeric_ratio_{sum(c.isdigit() for c in content) / len(content) if content else 0:.2f}"
        
        return features
    
    def _get_feature_importance(self) -> Dict[str, float]:
        """
        Get feature importance from trained model
        """
        if not self.classifier or not self.vectorizer:
            return {}
        
        feature_names = self.vectorizer.get_feature_names_out()
        importance_scores = self.classifier.feature_importances_
        
        # Get top 20 most important features
        feature_importance = dict(zip(feature_names, importance_scores))
        sorted_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
        
        return dict(sorted_features[:20])
    
    def _save_model(self):
        """
        Save trained model to S3
        """
        try:
            model_data = {
                'vectorizer': self.vectorizer,
                'classifier': self.classifier,
                'model_version': datetime.utcnow().strftime('%Y%m%d_%H%M%S'),
                'sensitive_patterns': self.sensitive_patterns
            }
            
            # Serialize model
            model_bytes = pickle.dumps(model_data)
            
            # Upload to S3
            bucket_name = f'ml-classification-models-{self._get_account_id()}'
            key = f'models/classification_model_{model_data["model_version"]}.pkl'
            
            self.s3_client.put_object(
                Bucket=bucket_name,
                Key=key,
                Body=model_bytes,
                ServerSideEncryption='AES256'
            )
            
            # Update current model pointer
            self.s3_client.put_object(
                Bucket=bucket_name,
                Key='models/current_model.txt',
                Body=key.encode(),
                ServerSideEncryption='AES256'
            )
            
            self.model_version = model_data["model_version"]
            logger.info(f"Model saved to S3: {key}")
            
        except Exception as e:
            logger.error(f"Error saving model: {str(e)}")
    
    def load_model(self, model_version: Optional[str] = None) -> bool:
        """
        Load trained model from S3
        """
        try:
            bucket_name = f'ml-classification-models-{self._get_account_id()}'
            
            if model_version:
                key = f'models/classification_model_{model_version}.pkl'
            else:
                # Load current model
                current_model_response = self.s3_client.get_object(
                    Bucket=bucket_name,
                    Key='models/current_model.txt'
                )
                key = current_model_response['Body'].read().decode()
            
            # Download and deserialize model
            model_response = self.s3_client.get_object(Bucket=bucket_name, Key=key)
            model_data = pickle.loads(model_response['Body'].read())
            
            self.vectorizer = model_data['vectorizer']
            self.classifier = model_data['classifier']
            self.model_version = model_data['model_version']
            self.sensitive_patterns = model_data['sensitive_patterns']
            
            logger.info(f"Model loaded successfully: {self.model_version}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            return False
    
    def classify_content(self, content: str) -> ClassificationPrediction:
        """
        Classify content using trained ML model
        """
        if not self.classifier or not self.vectorizer:
            raise ValueError("Model not loaded. Call load_model() first.")
        
        try:
            # Extract features
            features = self._extract_text_features(content)
            
            # Vectorize features
            features_vectorized = self.vectorizer.transform([features])
            
            # Make prediction
            prediction = self.classifier.predict(features_vectorized)[0]
            prediction_proba = self.classifier.predict_proba(features_vectorized)[0]
            
            # Get confidence score
            confidence_score = max(prediction_proba)
            
            # Detect sensitive patterns
            sensitive_patterns_detected = []
            for pattern_name, pattern in self.sensitive_patterns.items():
                if re.search(pattern, content, re.IGNORECASE):
                    sensitive_patterns_detected.append(pattern_name)
            
            # Get feature importance for this prediction
            feature_importance = self._get_prediction_feature_importance(features_vectorized)
            
            # Generate recommendation
            recommendation = self._generate_classification_recommendation(
                prediction, confidence_score, sensitive_patterns_detected
            )
            
            return ClassificationPrediction(
                classification_level=prediction,
                confidence_score=confidence_score,
                feature_importance=feature_importance,
                sensitive_patterns_detected=sensitive_patterns_detected,
                recommendation=recommendation
            )
            
        except Exception as e:
            logger.error(f"Error classifying content: {str(e)}")
            raise
    
    def _get_prediction_feature_importance(self, features_vectorized) -> Dict[str, float]:
        """
        Get feature importance for a specific prediction
        """
        try:
            # Get feature names and their values for this prediction
            feature_names = self.vectorizer.get_feature_names_out()
            feature_values = features_vectorized.toarray()[0]
            
            # Get model feature importance
            model_importance = self.classifier.feature_importances_
            
            # Calculate weighted importance for this prediction
            weighted_importance = {}
            for i, (name, value, importance) in enumerate(zip(feature_names, feature_values, model_importance)):
                if value > 0:  # Only include features present in this document
                    weighted_importance[name] = value * importance
            
            # Return top 10 features
            sorted_features = sorted(weighted_importance.items(), key=lambda x: x[1], reverse=True)
            return dict(sorted_features[:10])
            
        except Exception as e:
            logger.error(f"Error getting prediction feature importance: {str(e)}")
            return {}
    
    def _generate_classification_recommendation(self, 
                                             classification: str, 
                                             confidence: float, 
                                             sensitive_patterns: List[str]) -> str:
        """
        Generate recommendation based on classification results
        """
        recommendations = []
        
        if confidence < 0.7:
            recommendations.append("Low confidence classification - consider human review")
        
        if classification in ['confidential', 'restricted'] and confidence > 0.8:
            recommendations.append("High-risk classification detected - apply strict access controls")
        
        if sensitive_patterns:
            recommendations.append(f"Sensitive data patterns detected: {', '.join(sensitive_patterns)}")
        
        if classification == 'restricted':
            recommendations.append("Restricted data requires encryption, MFA, and audit logging")
        elif classification == 'confidential':
            recommendations.append("Confidential data requires access controls and monitoring")
        elif classification == 'internal':
            recommendations.append("Internal data requires basic access controls")
        
        return '; '.join(recommendations) if recommendations else "Standard data handling procedures apply"
    
    def retrain_model_with_feedback(self, feedback_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Retrain model with user feedback
        """
        try:
            # Convert feedback to training data
            feedback_training_data = []
            for feedback in feedback_data:
                training_sample = TrainingData(
                    content=feedback['content'],
                    classification_level=feedback['correct_classification'],
                    sensitive_data_types=feedback.get('sensitive_data_types', []),
                    confidence_score=1.0,  # High confidence for human feedback
                    source='feedback'
                )
                feedback_training_data.append(training_sample)
            
            # Collect existing training data
            existing_data = self.collect_training_data(days=90)
            
            # Combine with feedback data
            all_training_data = existing_data + feedback_training_data
            
            # Retrain model
            return self.train_classification_model(all_training_data)
            
        except Exception as e:
            logger.error(f"Error retraining model with feedback: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _determine_classification_from_sensitive_data(self, sensitive_data: List[Dict[str, Any]]) -> str:
        """
        Determine classification level from Macie sensitive data findings
        """
        max_level = 'public'
        level_hierarchy = {'public': 0, 'internal': 1, 'confidential': 2, 'restricted': 3}
        
        for data_item in sensitive_data:
            category = data_item.get('category', '')
            
            if category in ['CREDIT_CARD_NUMBER', 'SSN', 'BANK_ACCOUNT_NUMBER', 'PASSPORT_NUMBER']:
                max_level = 'restricted'
            elif category in ['PERSON_NAME', 'ADDRESS', 'PHONE_NUMBER'] and level_hierarchy[max_level] < 2:
                max_level = 'confidential'
            elif category in ['EMAIL_ADDRESS'] and level_hierarchy[max_level] < 1:
                max_level = 'internal'
        
        return max_level
    
    def _extract_content_sample(self, finding: Dict[str, Any]) -> str:
        """
        Extract content sample from Macie finding
        """
        # This would extract actual content samples from the finding
        # For security reasons, we'll return a placeholder
        return f"Content sample from {finding.get('type', 'unknown')} finding"
    
    def _get_content_sample_for_resource(self, resource_arn: str) -> Optional[str]:
        """
        Get content sample for a resource ARN
        """
        try:
            # Extract bucket and key from S3 ARN
            if 's3' in resource_arn:
                parts = resource_arn.split(':')
                bucket_name = parts[-1].split('/')[0]
                
                # Get a sample object from the bucket
                objects_response = self.s3_client.list_objects_v2(
                    Bucket=bucket_name,
                    MaxKeys=1
                )
                
                if 'Contents' in objects_response:
                    key = objects_response['Contents'][0]['Key']
                    
                    # Get object content (first 1KB)
                    response = self.s3_client.get_object(
                        Bucket=bucket_name,
                        Key=key,
                        Range='bytes=0-1023'
                    )
                    
                    return response['Body'].read().decode('utf-8', errors='ignore')
            
        except Exception as e:
            logger.error(f"Error getting content sample for {resource_arn}: {str(e)}")
        
        return None
    
    def _get_account_id(self) -> str:
        """Get AWS account ID"""
        return boto3.client('sts').get_caller_identity()['Account']

# Example usage
if __name__ == "__main__":
    # Initialize ML classification pipeline
    pipeline = MLClassificationPipeline()
    
    # Collect training data
    print("Collecting training data...")
    training_data = pipeline.collect_training_data(days=30)
    print(f"Collected {len(training_data)} training samples")
    
    # Train model
    if len(training_data) >= 10:
        print("Training classification model...")
        training_result = pipeline.train_classification_model(training_data)
        print(f"Training result: {training_result}")
        
        # Test classification
        if training_result['status'] == 'success':
            test_content = "John Doe's credit card number is 4532-1234-5678-9012 and his SSN is 123-45-6789"
            prediction = pipeline.classify_content(test_content)
            
            print(f"Classification: {prediction.classification_level}")
            print(f"Confidence: {prediction.confidence_score:.2f}")
            print(f"Sensitive patterns: {prediction.sensitive_patterns_detected}")
            print(f"Recommendation: {prediction.recommendation}")
    else:
        print("Insufficient training data for model training")
```

## Relevant AWS Services

### Core Classification Services
- **Amazon Macie**: Automated sensitive data discovery and classification
- **Amazon Comprehend**: Natural language processing for content analysis
- **Amazon Textract**: Extract text from documents and images for classification
- **Amazon Rekognition**: Image and video content analysis

### Event-Driven Services
- **Amazon EventBridge**: Event routing for real-time classification triggers
- **AWS Lambda**: Serverless functions for classification processing
- **AWS Step Functions**: Workflow orchestration for complex classification scenarios
- **Amazon Kinesis**: Real-time data streaming for classification

### Machine Learning Services
- **Amazon SageMaker**: Custom ML model training and deployment
- **AWS Batch**: Large-scale batch processing for classification jobs
- **Amazon Bedrock**: Foundation models for advanced content analysis

### Storage and Database Services
- **Amazon S3**: Object storage with event notifications
- **Amazon DynamoDB**: NoSQL database with streams for real-time processing
- **Amazon RDS**: Relational database with event notifications
- **Amazon DocumentDB**: Document database for unstructured data

### Integration Services
- **Amazon SNS**: Notifications for classification events
- **Amazon SQS**: Message queuing for classification workflows
- **AWS Systems Manager**: Parameter store for classification rules and configurations

## Benefits of Automated Classification

### Operational Benefits
- **Scalability**: Handle large volumes of data automatically
- **Consistency**: Apply classification rules uniformly across all data
- **Speed**: Real-time classification as data is created or modified
- **Cost Efficiency**: Reduce manual effort and human error

### Security Benefits
- **Immediate Protection**: Apply security controls as soon as data is classified
- **Comprehensive Coverage**: Classify all data assets, not just samples
- **Continuous Monitoring**: Ongoing classification as data changes
- **Risk Reduction**: Minimize exposure of unclassified sensitive data

### Compliance Benefits
- **Audit Trail**: Complete record of classification decisions and changes
- **Regulatory Compliance**: Meet requirements for data identification and protection
- **Policy Enforcement**: Automatically enforce data handling policies
- **Reporting**: Generate compliance reports and metrics

## Related Resources

- [AWS Well-Architected Framework - Data Classification](https://docs.aws.amazon.com/wellarchitected/latest/framework/sec_data_classification.html)
- [Amazon Macie User Guide](https://docs.aws.amazon.com/macie/latest/user/what-is-macie.html)
- [Amazon Comprehend Developer Guide](https://docs.aws.amazon.com/comprehend/latest/dg/what-is.html)
- [AWS Lambda Developer Guide](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)
- [Amazon EventBridge User Guide](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-what-is.html)
- [AWS Step Functions Developer Guide](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html)
- [Amazon SageMaker Developer Guide](https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html)
```
```
