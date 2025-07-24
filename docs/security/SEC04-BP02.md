---
title: SEC04-BP02 - Capture logs, findings, and metrics in standardized locations
layout: default
parent: SEC04 - How do you detect and investigate security events?
grand_parent: Security
nav_order: 2
---

<div class="pillar-header">
  <h1>SEC04-BP02: Capture logs, findings, and metrics in standardized locations</h1>
  <p>Security operations teams require access to logs, findings, and metrics to investigate security events. Ensure that logs, findings, and metrics are captured in standardized locations and formats. For example, ensure that logs are sent to a centralized logging solution, and that findings from security services are sent to a centralized location such as AWS Security Hub.</p>
</div>

## Implementation guidance

Standardizing the collection and storage of logs, findings, and metrics is crucial for effective security operations. By centralizing these data sources in consistent formats and locations, you enable efficient analysis, correlation, and response to security events across your entire AWS environment.

### Key steps for implementing this best practice:

1. **Establish centralized logging architecture**:
   - Design a centralized logging strategy for your organization
   - Choose appropriate storage solutions for different log types
   - Implement log aggregation from multiple sources
   - Define standard log formats and schemas
   - Establish log routing and distribution mechanisms

2. **Centralize security findings**:
   - Configure AWS Security Hub as your central findings repository
   - Enable integration with all AWS security services
   - Configure third-party security tools to send findings to Security Hub
   - Implement custom findings for application-specific security events
   - Standardize finding formats using AWS Security Finding Format (ASFF)

3. **Implement standardized metrics collection**:
   - Define security metrics and KPIs for your organization
   - Use Amazon CloudWatch for centralized metrics storage
   - Implement custom metrics for application security events
   - Create standardized dashboards for security monitoring
   - Set up automated alerting based on metric thresholds

4. **Configure cross-account log aggregation**:
   - Set up cross-account log delivery for multi-account environments
   - Implement centralized log storage in a dedicated security account
   - Configure appropriate IAM permissions for cross-account access
   - Use AWS Organizations for simplified cross-account setup
   - Implement log replication for high availability

5. **Implement data normalization and enrichment**:
   - Standardize log formats across different sources
   - Implement log parsing and normalization
   - Enrich logs with contextual information
   - Implement correlation identifiers across log sources
   - Use consistent timestamp formats and time zones

6. **Ensure data integrity and retention**:
   - Implement log integrity verification
   - Configure appropriate retention policies
   - Set up automated archival to cost-effective storage
   - Implement backup and disaster recovery for log data
   - Ensure compliance with regulatory retention requirements

## Implementation examples

### Example 1: Centralized logging with Amazon CloudWatch Logs

```bash
# Create a centralized log group for security events
aws logs create-log-group \
  --log-group-name "/security/centralized-logs" \
  --retention-in-days 365

# Create log streams for different sources
aws logs create-log-stream \
  --log-group-name "/security/centralized-logs" \
  --log-stream-name "application-security-events"

aws logs create-log-stream \
  --log-group-name "/security/centralized-logs" \
  --log-stream-name "infrastructure-security-events"

# Set up cross-account log destination
aws logs create-destination \
  --destination-name "SecurityLogDestination" \
  --target-arn "arn:aws:logs:us-west-2:123456789012:log-group:/security/centralized-logs" \
  --role-arn "arn:aws:iam::123456789012:role/LogsDestinationRole"

# Configure destination policy for cross-account access
aws logs put-destination-policy \
  --destination-name "SecurityLogDestination" \
  --access-policy '{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": {
          "AWS": [
            "arn:aws:iam::ACCOUNT-A:root",
            "arn:aws:iam::ACCOUNT-B:root"
          ]
        },
        "Action": "logs:PutLogEvents",
        "Resource": "arn:aws:logs:us-west-2:123456789012:destination:SecurityLogDestination"
      }
    ]
  }'
```

### Example 2: AWS Security Hub configuration for centralized findings

```python
import boto3
import json
from datetime import datetime

def setup_security_hub():
    """Configure AWS Security Hub for centralized findings"""
    
    securityhub = boto3.client('securityhub')
    
    try:
        # Enable Security Hub
        securityhub.enable_security_hub(
            Tags={
                'Environment': 'Production',
                'Purpose': 'CentralizedFindings'
            }
        )
        
        # Enable security standards
        standards = [
            'arn:aws:securityhub:::ruleset/cis-aws-foundations-benchmark/v/1.2.0',
            'arn:aws:securityhub:us-west-2::standard/aws-foundational-security/v/1.0.0',
            'arn:aws:securityhub:us-west-2::standard/pci-dss/v/3.2.1'
        ]
        
        for standard_arn in standards:
            try:
                securityhub.batch_enable_standards(
                    StandardsSubscriptionRequests=[
                        {
                            'StandardsArn': standard_arn
                        }
                    ]
                )
                print(f"Enabled standard: {standard_arn}")
            except Exception as e:
                print(f"Error enabling standard {standard_arn}: {str(e)}")
        
        # Configure custom insights
        create_custom_insights(securityhub)
        
        print("Security Hub configuration completed successfully")
        
    except Exception as e:
        print(f"Error configuring Security Hub: {str(e)}")

def create_custom_insights(securityhub):
    """Create custom insights for security monitoring"""
    
    insights = [
        {
            'Name': 'High Severity Findings by Resource',
            'Filters': {
                'SeverityLabel': [
                    {
                        'Value': 'HIGH',
                        'Comparison': 'EQUALS'
                    },
                    {
                        'Value': 'CRITICAL',
                        'Comparison': 'EQUALS'
                    }
                ],
                'RecordState': [
                    {
                        'Value': 'ACTIVE',
                        'Comparison': 'EQUALS'
                    }
                ]
            },
            'GroupByAttribute': 'ResourceId'
        },
        {
            'Name': 'Failed Login Attempts',
            'Filters': {
                'Title': [
                    {
                        'Value': 'Failed login',
                        'Comparison': 'CONTAINS'
                    }
                ],
                'RecordState': [
                    {
                        'Value': 'ACTIVE',
                        'Comparison': 'EQUALS'
                    }
                ]
            },
            'GroupByAttribute': 'SourceIpAddress'
        }
    ]
    
    for insight in insights:
        try:
            securityhub.create_insight(**insight)
            print(f"Created insight: {insight['Name']}")
        except Exception as e:
            print(f"Error creating insight {insight['Name']}: {str(e)}")

def send_custom_finding(event_data):
    """Send custom security finding to Security Hub"""
    
    securityhub = boto3.client('securityhub')
    
    # Create finding in AWS Security Finding Format (ASFF)
    finding = {
        'SchemaVersion': '2018-10-08',
        'Id': f"custom-finding-{event_data['correlation_id']}",
        'ProductArn': f"arn:aws:securityhub:us-west-2:123456789012:product/123456789012/default",
        'GeneratorId': 'custom-security-monitor',
        'AwsAccountId': '123456789012',
        'Types': ['Sensitive Data Identifications/PII'],
        'FirstObservedAt': datetime.utcnow().isoformat() + 'Z',
        'LastObservedAt': datetime.utcnow().isoformat() + 'Z',
        'CreatedAt': datetime.utcnow().isoformat() + 'Z',
        'UpdatedAt': datetime.utcnow().isoformat() + 'Z',
        'Severity': {
            'Label': event_data.get('severity', 'MEDIUM')
        },
        'Title': event_data.get('title', 'Security Event Detected'),
        'Description': event_data.get('description', 'Custom security event detected'),
        'Resources': [
            {
                'Type': 'Other',
                'Id': event_data.get('resource_id', 'unknown'),
                'Region': 'us-west-2'
            }
        ],
        'SourceUrl': event_data.get('source_url', ''),
        'RecordState': 'ACTIVE',
        'WorkflowState': 'NEW'
    }
    
    try:
        response = securityhub.batch_import_findings(
            Findings=[finding]
        )
        print(f"Successfully imported finding: {finding['Id']}")
        return response
    except Exception as e:
        print(f"Error importing finding: {str(e)}")
        return None

# Example usage
if __name__ == "__main__":
    setup_security_hub()
    
    # Example custom finding
    event_data = {
        'correlation_id': '12345',
        'severity': 'HIGH',
        'title': 'Suspicious Login Activity',
        'description': 'Multiple failed login attempts detected from unusual location',
        'resource_id': 'user-account-johndoe',
        'source_url': 'https://example.com/security-dashboard'
    }
    
    send_custom_finding(event_data)
```

### Example 3: Standardized metrics collection with CloudWatch

```python
import boto3
import json
from datetime import datetime

class SecurityMetricsCollector:
    def __init__(self):
        self.cloudwatch = boto3.client('cloudwatch')
        self.namespace = 'Security/Metrics'
    
    def send_authentication_metrics(self, success_count, failure_count, source_ip=None):
        """Send authentication metrics to CloudWatch"""
        
        metrics = [
            {
                'MetricName': 'AuthenticationAttempts',
                'Dimensions': [
                    {
                        'Name': 'Result',
                        'Value': 'Success'
                    }
                ],
                'Value': success_count,
                'Unit': 'Count',
                'Timestamp': datetime.utcnow()
            },
            {
                'MetricName': 'AuthenticationAttempts',
                'Dimensions': [
                    {
                        'Name': 'Result',
                        'Value': 'Failure'
                    }
                ],
                'Value': failure_count,
                'Unit': 'Count',
                'Timestamp': datetime.utcnow()
            }
        ]
        
        if source_ip:
            metrics.append({
                'MetricName': 'AuthenticationFailuresByIP',
                'Dimensions': [
                    {
                        'Name': 'SourceIP',
                        'Value': source_ip
                    }
                ],
                'Value': failure_count,
                'Unit': 'Count',
                'Timestamp': datetime.utcnow()
            })
        
        try:
            self.cloudwatch.put_metric_data(
                Namespace=self.namespace,
                MetricData=metrics
            )
            print(f"Successfully sent {len(metrics)} authentication metrics")
        except Exception as e:
            print(f"Error sending metrics: {str(e)}")
    
    def send_data_access_metrics(self, resource_type, access_count, user_id=None):
        """Send data access metrics to CloudWatch"""
        
        dimensions = [
            {
                'Name': 'ResourceType',
                'Value': resource_type
            }
        ]
        
        if user_id:
            dimensions.append({
                'Name': 'UserId',
                'Value': user_id
            })
        
        metric_data = [
            {
                'MetricName': 'DataAccess',
                'Dimensions': dimensions,
                'Value': access_count,
                'Unit': 'Count',
                'Timestamp': datetime.utcnow()
            }
        ]
        
        try:
            self.cloudwatch.put_metric_data(
                Namespace=self.namespace,
                MetricData=metric_data
            )
            print(f"Successfully sent data access metrics for {resource_type}")
        except Exception as e:
            print(f"Error sending data access metrics: {str(e)}")
    
    def create_security_dashboard(self):
        """Create a standardized security dashboard"""
        
        dashboard_body = {
            "widgets": [
                {
                    "type": "metric",
                    "x": 0,
                    "y": 0,
                    "width": 12,
                    "height": 6,
                    "properties": {
                        "metrics": [
                            [self.namespace, "AuthenticationAttempts", "Result", "Success"],
                            [".", ".", ".", "Failure"]
                        ],
                        "period": 300,
                        "stat": "Sum",
                        "region": "us-west-2",
                        "title": "Authentication Attempts"
                    }
                },
                {
                    "type": "metric",
                    "x": 0,
                    "y": 6,
                    "width": 12,
                    "height": 6,
                    "properties": {
                        "metrics": [
                            [self.namespace, "DataAccess", "ResourceType", "S3"],
                            [".", ".", ".", "RDS"],
                            [".", ".", ".", "DynamoDB"]
                        ],
                        "period": 300,
                        "stat": "Sum",
                        "region": "us-west-2",
                        "title": "Data Access by Resource Type"
                    }
                }
            ]
        }
        
        try:
            self.cloudwatch.put_dashboard(
                DashboardName='SecurityMetrics',
                DashboardBody=json.dumps(dashboard_body)
            )
            print("Successfully created security dashboard")
        except Exception as e:
            print(f"Error creating dashboard: {str(e)}")

# Example usage
metrics_collector = SecurityMetricsCollector()
metrics_collector.send_authentication_metrics(100, 5, '192.168.1.100')
metrics_collector.send_data_access_metrics('S3', 50, 'user123')
metrics_collector.create_security_dashboard()
```

### Example 4: Cross-account log aggregation with AWS Organizations

```yaml
# CloudFormation template for cross-account log aggregation
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Cross-account log aggregation setup'

Parameters:
  OrganizationId:
    Type: String
    Description: AWS Organizations ID
  SecurityAccountId:
    Type: String
    Description: Account ID for centralized security logging

Resources:
  # S3 bucket for centralized log storage
  CentralizedLogsBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub 'centralized-security-logs-${AWS::AccountId}'
      BucketEncryption:
        ServerSideEncryptionConfiguration:
          - ServerSideEncryptionByDefault:
              SSEAlgorithm: AES256
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true
      LifecycleConfiguration:
        Rules:
          - Id: LogRetentionRule
            Status: Enabled
            Transitions:
              - TransitionInDays: 30
                StorageClass: STANDARD_IA
              - TransitionInDays: 90
                StorageClass: GLACIER
              - TransitionInDays: 365
                StorageClass: DEEP_ARCHIVE
      NotificationConfiguration:
        CloudWatchConfigurations:
          - Event: 's3:ObjectCreated:*'
            CloudWatchConfiguration:
              LogGroupName: !Ref LogProcessingLogGroup

  # Bucket policy for cross-account access
  CentralizedLogsBucketPolicy:
    Type: AWS::S3::BucketPolicy
    Properties:
      Bucket: !Ref CentralizedLogsBucket
      PolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Sid: AllowOrganizationAccounts
            Effect: Allow
            Principal: '*'
            Action:
              - 's3:PutObject'
              - 's3:PutObjectAcl'
            Resource: !Sub '${CentralizedLogsBucket}/*'
            Condition:
              StringEquals:
                'aws:PrincipalOrgID': !Ref OrganizationId
          - Sid: AllowCloudTrailDelivery
            Effect: Allow
            Principal:
              Service: cloudtrail.amazonaws.com
            Action: 's3:PutObject'
            Resource: !Sub '${CentralizedLogsBucket}/cloudtrail-logs/*'
            Condition:
              StringEquals:
                's3:x-amz-acl': 'bucket-owner-full-control'

  # CloudWatch Log Group for processing
  LogProcessingLogGroup:
    Type: AWS::Logs::LogGroup
    Properties:
      LogGroupName: '/security/log-processing'
      RetentionInDays: 90

  # Lambda function for log processing
  LogProcessingFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: SecurityLogProcessor
      Runtime: python3.9
      Handler: index.lambda_handler
      Role: !GetAtt LogProcessingRole.Arn
      Code:
        ZipFile: |
          import json
          import boto3
          import gzip
          from urllib.parse import unquote_plus
          
          def lambda_handler(event, context):
              s3 = boto3.client('s3')
              
              for record in event['Records']:
                  bucket = record['s3']['bucket']['name']
                  key = unquote_plus(record['s3']['object']['key'])
                  
                  # Process the log file
                  try:
                      response = s3.get_object(Bucket=bucket, Key=key)
                      
                      if key.endswith('.gz'):
                          content = gzip.decompress(response['Body'].read())
                      else:
                          content = response['Body'].read()
                      
                      # Process and normalize log content
                      process_log_content(content.decode('utf-8'))
                      
                  except Exception as e:
                      print(f"Error processing {key}: {str(e)}")
              
              return {'statusCode': 200}
          
          def process_log_content(content):
              # Implement log processing logic
              print(f"Processing log content: {len(content)} bytes")

  # IAM role for Lambda function
  LogProcessingRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action: 'sts:AssumeRole'
      ManagedPolicyArns:
        - 'arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'
      Policies:
        - PolicyName: S3AccessPolicy
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - 's3:GetObject'
                  - 's3:PutObject'
                Resource: !Sub '${CentralizedLogsBucket}/*'

  # S3 bucket notification
  BucketNotification:
    Type: AWS::S3::Bucket
    Properties:
      NotificationConfiguration:
        LambdaConfigurations:
          - Event: 's3:ObjectCreated:*'
            Function: !GetAtt LogProcessingFunction.Arn

Outputs:
  CentralizedLogsBucketName:
    Description: 'Name of the centralized logs bucket'
    Value: !Ref CentralizedLogsBucket
    Export:
      Name: !Sub '${AWS::StackName}-CentralizedLogsBucket'
  
  LogProcessingFunctionArn:
    Description: 'ARN of the log processing function'
    Value: !GetAtt LogProcessingFunction.Arn
    Export:
      Name: !Sub '${AWS::StackName}-LogProcessingFunction'
```

## AWS services to consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Security Hub</h4>
    <p>Provides a comprehensive view of your security state in AWS and helps you check your compliance with security standards and best practices. Central repository for security findings from multiple sources.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon CloudWatch Logs</h4>
    <p>Monitors, stores, and provides access to your log files from Amazon EC2 instances, AWS CloudTrail, and other sources. Centralized logging solution with cross-account capabilities.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon CloudWatch</h4>
    <p>Monitors your AWS resources and the applications you run on AWS in real time. Centralized metrics collection and dashboard creation for security monitoring.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon S3</h4>
    <p>Object storage service that offers industry-leading scalability, data availability, security, and performance. Cost-effective long-term storage for logs and findings.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Organizations</h4>
    <p>Helps you centrally manage and govern your environment as you scale your AWS resources. Simplifies cross-account log aggregation and centralized security management.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon Kinesis Data Firehose</h4>
    <p>A fully managed service for delivering real-time streaming data to destinations such as Amazon S3, Amazon Redshift, Amazon Elasticsearch Service, and Splunk. Useful for real-time log streaming and processing.</p>
  </div>
</div>

## Benefits of capturing logs, findings, and metrics in standardized locations

- **Improved security visibility**: Centralized view of security events across your entire environment
- **Enhanced incident response**: Faster correlation and analysis of security events
- **Simplified compliance**: Centralized audit trails and standardized reporting
- **Operational efficiency**: Reduced complexity in security monitoring and analysis
- **Better threat detection**: Improved ability to identify patterns and anomalies
- **Cost optimization**: Efficient storage and processing of security data
- **Scalable architecture**: Supports growth in data volume and organizational complexity

## Related resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/sec_detect_investigate_events_logs.html">AWS Well-Architected Framework - Capture logs, findings, and metrics in standardized locations</a></li>
    <li><a href="https://docs.aws.amazon.com/securityhub/latest/userguide/what-is-securityhub.html">AWS Security Hub User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/WhatIsCloudWatchLogs.html">Amazon CloudWatch Logs User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-findings-format.html">AWS Security Finding Format (ASFF)</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-centralize-findings-from-aws-security-services-using-aws-security-hub-custom-insights/">How to centralize findings from AWS security services using AWS Security Hub custom insights</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-set-up-a-two-tier-permissions-model-for-cross-account-access-to-aws-security-hub/">How to set up a two-tier permissions model for cross-account access to AWS Security Hub</a></li>
  </ul>
</div>
