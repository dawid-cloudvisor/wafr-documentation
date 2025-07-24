---
title: SEC04-BP01 - Configure service and application logging
layout: default
parent: SEC04 - How do you detect and investigate security events?
grand_parent: Security
nav_order: 1
---

<div class="pillar-header">
  <h1>SEC04-BP01: Configure service and application logging</h1>
  <p>Configure logging throughout your workload, including application logs, resource logs, and AWS service logs. For example, ensure that AWS CloudTrail, VPC Flow Logs, and DNS logs are enabled and centralized.</p>
</div>

## Implementation guidance

Comprehensive logging is essential for detecting security events, investigating incidents, and maintaining compliance. By configuring logging across all layers of your workload, you create a detailed audit trail that enables effective security monitoring and incident response.

### Key steps for implementing this best practice:

1. **Enable AWS service logging**:
   - Configure AWS CloudTrail for API activity logging
   - Enable VPC Flow Logs for network traffic monitoring
   - Set up DNS query logging with Route 53 Resolver
   - Enable AWS Config for resource configuration tracking
   - Configure load balancer access logs
   - Enable database audit logs (RDS, DynamoDB)

2. **Configure application logging**:
   - Implement structured logging in your applications
   - Log security-relevant events (authentication, authorization, data access)
   - Include contextual information (user ID, session ID, IP address)
   - Use consistent log formats across applications
   - Implement log correlation identifiers

3. **Centralize log collection**:
   - Use Amazon CloudWatch Logs for centralized log storage
   - Configure log agents on EC2 instances and containers
   - Set up log streaming from Lambda functions
   - Implement log forwarding from on-premises systems
   - Use AWS Systems Manager for hybrid log collection

4. **Implement log retention and lifecycle management**:
   - Define retention policies based on compliance requirements
   - Configure automatic log archival to cost-effective storage
   - Implement log compression and optimization
   - Set up automated log deletion for expired data
   - Consider long-term archival requirements

5. **Secure log data**:
   - Encrypt logs in transit and at rest
   - Implement access controls for log data
   - Use separate accounts or roles for log management
   - Protect log integrity with checksums or digital signatures
   - Monitor for unauthorized log access or modification

6. **Optimize logging for analysis**:
   - Use structured logging formats (JSON, XML)
   - Implement consistent timestamp formats
   - Include relevant metadata and context
   - Configure log parsing and normalization
   - Set up log indexing for efficient searching

## Implementation examples

### Example 1: Comprehensive CloudTrail configuration

```json
{
  "Trail": {
    "Name": "OrganizationCloudTrail",
    "S3BucketName": "organization-cloudtrail-logs",
    "S3KeyPrefix": "cloudtrail-logs/",
    "IncludeGlobalServiceEvents": true,
    "IsMultiRegionTrail": true,
    "EnableLogFileValidation": true,
    "EventSelectors": [
      {
        "ReadWriteType": "All",
        "IncludeManagementEvents": true,
        "DataResources": [
          {
            "Type": "AWS::S3::Object",
            "Values": ["arn:aws:s3:::sensitive-data-bucket/*"]
          },
          {
            "Type": "AWS::Lambda::Function",
            "Values": ["*"]
          }
        ]
      }
    ],
    "InsightSelectors": [
      {
        "InsightType": "ApiCallRateInsight"
      }
    ]
  }
}
```

```bash
# Create CloudTrail with comprehensive logging
aws cloudtrail create-trail \
  --name OrganizationCloudTrail \
  --s3-bucket-name organization-cloudtrail-logs \
  --s3-key-prefix cloudtrail-logs/ \
  --include-global-service-events \
  --is-multi-region-trail \
  --enable-log-file-validation \
  --cloud-watch-logs-log-group-arn arn:aws:logs:us-west-2:123456789012:log-group:CloudTrail/OrganizationCloudTrail:* \
  --cloud-watch-logs-role-arn arn:aws:iam::123456789012:role/CloudTrailLogsRole

# Configure event selectors for data events
aws cloudtrail put-event-selectors \
  --trail-name OrganizationCloudTrail \
  --event-selectors file://event-selectors.json

# Enable CloudTrail insights
aws cloudtrail put-insight-selectors \
  --trail-name OrganizationCloudTrail \
  --insight-selectors InsightType=ApiCallRateInsight
```

### Example 2: VPC Flow Logs configuration

```bash
# Enable VPC Flow Logs for all network interfaces
aws ec2 create-flow-logs \
  --resource-type VPC \
  --resource-ids vpc-12345678 \
  --traffic-type ALL \
  --log-destination-type cloud-watch-logs \
  --log-group-name VPCFlowLogs \
  --deliver-logs-permission-arn arn:aws:iam::123456789012:role/flowlogsRole

# Enable Flow Logs with custom format
aws ec2 create-flow-logs \
  --resource-type NetworkInterface \
  --resource-ids eni-1234567890abcdef0 \
  --traffic-type ALL \
  --log-destination-type s3 \
  --log-destination arn:aws:s3:::vpc-flow-logs-bucket/flow-logs/ \
  --log-format '${srcaddr} ${dstaddr} ${srcport} ${dstport} ${protocol} ${packets} ${bytes} ${windowstart} ${windowend} ${action}'

# Create Flow Logs for subnet
aws ec2 create-flow-logs \
  --resource-type Subnet \
  --resource-ids subnet-12345678 \
  --traffic-type REJECT \
  --log-destination-type cloud-watch-logs \
  --log-group-name VPCFlowLogs-Rejected
```

### Example 3: Application logging with structured format

```python
import json
import logging
import uuid
from datetime import datetime
from flask import Flask, request, g

app = Flask(__name__)

# Configure structured logging
class StructuredLogger:
    def __init__(self, logger_name):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.INFO)
        
        # Create handler
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        
        # Create formatter for structured logs
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        
        self.logger.addHandler(handler)
    
    def log_event(self, event_type, message, **kwargs):
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'event_type': event_type,
            'message': message,
            'correlation_id': getattr(g, 'correlation_id', None),
            'user_id': getattr(g, 'user_id', None),
            'session_id': getattr(g, 'session_id', None),
            'source_ip': request.remote_addr if request else None,
            'user_agent': request.headers.get('User-Agent') if request else None,
            **kwargs
        }
        
        self.logger.info(json.dumps(log_entry))

# Initialize logger
security_logger = StructuredLogger('security')
app_logger = StructuredLogger('application')

@app.before_request
def before_request():
    g.correlation_id = str(uuid.uuid4())
    g.start_time = datetime.utcnow()

@app.after_request
def after_request(response):
    duration = (datetime.utcnow() - g.start_time).total_seconds()
    
    app_logger.log_event(
        'http_request',
        f'{request.method} {request.path}',
        status_code=response.status_code,
        duration_seconds=duration,
        request_size=request.content_length,
        response_size=response.content_length
    )
    
    return response

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    
    # Log authentication attempt
    security_logger.log_event(
        'authentication_attempt',
        'User login attempt',
        username=username,
        success=False  # Will be updated based on result
    )
    
    # Authentication logic here
    if authenticate_user(username, request.json.get('password')):
        g.user_id = username
        g.session_id = str(uuid.uuid4())
        
        security_logger.log_event(
            'authentication_success',
            'User successfully authenticated',
            username=username
        )
        
        return {'status': 'success', 'session_id': g.session_id}
    else:
        security_logger.log_event(
            'authentication_failure',
            'User authentication failed',
            username=username,
            failure_reason='invalid_credentials'
        )
        
        return {'status': 'error', 'message': 'Invalid credentials'}, 401

@app.route('/sensitive-data')
def get_sensitive_data():
    if not g.get('user_id'):
        security_logger.log_event(
            'unauthorized_access_attempt',
            'Attempt to access sensitive data without authentication',
            endpoint='/sensitive-data'
        )
        return {'error': 'Unauthorized'}, 401
    
    security_logger.log_event(
        'data_access',
        'User accessed sensitive data',
        data_type='sensitive',
        endpoint='/sensitive-data'
    )
    
    return {'data': 'sensitive information'}

def authenticate_user(username, password):
    # Authentication logic implementation
    return True  # Simplified for example
```

### Example 4: CloudWatch Logs configuration with Lambda

```python
import json
import boto3
import gzip
import base64
from datetime import datetime

def lambda_handler(event, context):
    """
    Process CloudWatch Logs and forward security events
    """
    
    # Decode and decompress log data
    compressed_payload = base64.b64decode(event['awslogs']['data'])
    uncompressed_payload = gzip.decompress(compressed_payload)
    log_data = json.loads(uncompressed_payload)
    
    security_events = []
    
    # Process each log event
    for log_event in log_data['logEvents']:
        try:
            # Parse structured log message
            message = json.loads(log_event['message'])
            
            # Identify security-relevant events
            if is_security_event(message):
                security_event = {
                    'timestamp': datetime.fromtimestamp(log_event['timestamp'] / 1000).isoformat(),
                    'log_group': log_data['logGroup'],
                    'log_stream': log_data['logStream'],
                    'event_type': message.get('event_type'),
                    'message': message.get('message'),
                    'user_id': message.get('user_id'),
                    'source_ip': message.get('source_ip'),
                    'correlation_id': message.get('correlation_id'),
                    'severity': determine_severity(message)
                }
                
                security_events.append(security_event)
        
        except json.JSONDecodeError:
            # Handle non-JSON log messages
            continue
    
    # Forward security events to SIEM or security team
    if security_events:
        forward_security_events(security_events)
    
    return {
        'statusCode': 200,
        'body': json.dumps(f'Processed {len(security_events)} security events')
    }

def is_security_event(message):
    """Determine if a log message represents a security event"""
    
    security_event_types = [
        'authentication_attempt',
        'authentication_failure',
        'authorization_failure',
        'data_access',
        'configuration_change',
        'suspicious_activity'
    ]
    
    return message.get('event_type') in security_event_types

def determine_severity(message):
    """Determine the severity of a security event"""
    
    event_type = message.get('event_type')
    
    high_severity_events = [
        'authentication_failure',
        'unauthorized_access_attempt',
        'privilege_escalation'
    ]
    
    medium_severity_events = [
        'authentication_attempt',
        'configuration_change'
    ]
    
    if event_type in high_severity_events:
        return 'HIGH'
    elif event_type in medium_severity_events:
        return 'MEDIUM'
    else:
        return 'LOW'

def forward_security_events(events):
    """Forward security events to external systems"""
    
    # Example: Send to SNS topic
    sns = boto3.client('sns')
    
    for event in events:
        if event['severity'] in ['HIGH', 'CRITICAL']:
            sns.publish(
                TopicArn='arn:aws:sns:us-west-2:123456789012:SecurityAlerts',
                Subject=f"Security Event: {event['event_type']}",
                Message=json.dumps(event, indent=2)
            )
    
    # Example: Send to external SIEM
    # siem_client.send_events(events)
```

## AWS services to consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS CloudTrail</h4>
    <p>Records API calls for your account and delivers log files to you. Essential for auditing AWS service usage and detecting unauthorized activities.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon CloudWatch Logs</h4>
    <p>Monitors, stores, and provides access to your log files from Amazon EC2 instances, AWS CloudTrail, and other sources. Centralized logging solution for AWS workloads.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon VPC Flow Logs</h4>
    <p>Captures information about the IP traffic going to and from network interfaces in your VPC. Essential for network security monitoring and troubleshooting.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Config</h4>
    <p>Enables you to assess, audit, and evaluate the configurations of your AWS resources. Provides configuration history and change notifications.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon Route 53 Resolver</h4>
    <p>Provides DNS resolution for your VPC and on-premises networks. DNS query logging helps detect malicious domain lookups and data exfiltration attempts.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Systems Manager</h4>
    <p>Gives you visibility and control of your infrastructure on AWS. Use Systems Manager Agent to collect logs from EC2 instances and hybrid environments.</p>
  </div>
</div>

## Benefits of configuring service and application logging

- **Enhanced security visibility**: Provides comprehensive view of activities across your workload
- **Improved incident response**: Enables faster detection and investigation of security events
- **Compliance support**: Meets regulatory requirements for audit trails and logging
- **Operational insights**: Helps identify performance issues and optimization opportunities
- **Forensic capabilities**: Provides detailed evidence for security investigations
- **Proactive monitoring**: Enables early detection of security threats and anomalies
- **Accountability**: Creates audit trails for user and system activities

## Related resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/sec_detect_investigate_events_app_service_logging.html">AWS Well-Architected Framework - Configure service and application logging</a></li>
    <li><a href="https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html">AWS CloudTrail User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html">VPC Flow Logs User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/WhatIsCloudWatchLogs.html">Amazon CloudWatch Logs User Guide</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-monitor-and-visualize-failed-ssh-access-attempts-to-amazon-ec2-linux-instances/">How to monitor and visualize failed SSH access attempts to Amazon EC2 Linux instances</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-centralize-findings-from-aws-security-services-using-aws-security-hub-custom-insights/">How to centralize findings from AWS security services using AWS Security Hub custom insights</a></li>
  </ul>
</div>
