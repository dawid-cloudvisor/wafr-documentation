---
title: SEC03-BP08 - Share resources securely within your organization
layout: default
parent: SEC03 - How do you manage permissions for people and machines?
grand_parent: Security
nav_order: 8
---

<div class="pillar-header">
  <h1>SEC03-BP08: Share resources securely within your organization</h1>
  <p>As the number of workloads grows, you might need to share access to resources in those workloads, or you might own resources that other workloads need to access. When you share resources with other teams, maintain least privilege access and avoid sharing credentials. Define clear ownership for resources to avoid confusion during an incident response. Monitor shared resource access.</p>
</div>

## Implementation guidance

Secure resource sharing within your organization enables collaboration while maintaining security boundaries. By implementing proper sharing mechanisms, you can provide necessary access without compromising security or creating management overhead.

### Key steps for implementing this best practice:

1. **Establish resource sharing governance**:
   - Define policies for resource sharing within the organization
   - Establish approval processes for sharing requests
   - Document resource ownership and responsibilities
   - Create guidelines for different types of shared resources
   - Implement regular reviews of shared resource access

2. **Use AWS Resource Access Manager (RAM)**:
   - Share resources across AWS accounts within your organization
   - Implement centralized sharing for common resources
   - Use resource shares to group related resources
   - Apply appropriate permissions to shared resources
   - Monitor resource share usage and access patterns

3. **Implement cross-account access with IAM roles**:
   - Create dedicated roles for cross-account access
   - Use external IDs for additional security
   - Implement time-limited access where appropriate
   - Apply conditions to restrict access based on context
   - Avoid sharing long-term credentials

4. **Secure shared storage resources**:
   - Use S3 bucket policies for controlled sharing
   - Implement encryption for shared data
   - Use S3 Access Points for fine-grained access control
   - Monitor access to shared storage resources
   - Implement data classification and handling requirements

5. **Monitor and audit shared resource access**:
   - Track all access to shared resources
   - Set up alerts for unusual access patterns
   - Generate regular reports on resource sharing
   - Implement automated compliance checks
   - Maintain audit trails for shared resource usage

6. **Implement secure sharing patterns**:
   - Use service-to-service authentication where possible
   - Implement network-level controls for shared resources
   - Use encryption in transit and at rest
   - Apply least privilege principles to shared access
   - Regularly validate sharing configurations

## Implementation examples

### Example 1: Sharing resources using AWS Resource Access Manager

```bash
# Create a resource share for VPC subnets
aws ram create-resource-share \
  --name "SharedNetworkResources" \
  --resource-arns "arn:aws:ec2:us-west-2:123456789012:subnet/subnet-12345678" \
  --principals "123456789013,123456789014" \
  --tags Key=Environment,Value=Production

# Associate additional resources with the share
aws ram associate-resource-share \
  --resource-share-arn "arn:aws:ram:us-west-2:123456789012:resource-share/12345678-1234-1234-1234-123456789012" \
  --resource-arns "arn:aws:ec2:us-west-2:123456789012:subnet/subnet-87654321"

# Accept a resource share invitation
aws ram accept-resource-share-invitation \
  --resource-share-invitation-arn "arn:aws:ram:us-west-2:123456789013:invitation/12345678-1234-1234-1234-123456789012"

# List shared resources
aws ram get-resource-shares \
  --resource-owner SELF \
  --resource-share-status ACTIVE
```

### Example 2: Cross-account IAM role for secure resource access

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": [
          "arn:aws:iam::ACCOUNT-A:role/DataProcessingRole",
          "arn:aws:iam::ACCOUNT-B:role/AnalyticsRole"
        ]
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "sts:ExternalId": "SharedResourceAccess2024"
        },
        "IpAddress": {
          "aws:SourceIp": [
            "10.0.0.0/8",
            "172.16.0.0/12"
          ]
        },
        "DateGreaterThan": {
          "aws:CurrentTime": "2024-01-01T00:00:00Z"
        },
        "DateLessThan": {
          "aws:CurrentTime": "2024-12-31T23:59:59Z"
        }
      }
    }
  ]
}
```

### Example 3: S3 bucket policy for secure cross-account sharing

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowCrossAccountRead",
      "Effect": "Allow",
      "Principal": {
        "AWS": [
          "arn:aws:iam::ACCOUNT-A:role/DataConsumerRole",
          "arn:aws:iam::ACCOUNT-B:role/ReportingRole"
        ]
      },
      "Action": [
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::shared-data-bucket",
        "arn:aws:s3:::shared-data-bucket/shared/*"
      ],
      "Condition": {
        "StringEquals": {
          "s3:x-amz-server-side-encryption": "aws:kms"
        },
        "Bool": {
          "aws:SecureTransport": "true"
        }
      }
    },
    {
      "Sid": "DenyDirectPublicAccess",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::shared-data-bucket",
        "arn:aws:s3:::shared-data-bucket/*"
      ],
      "Condition": {
        "StringNotEquals": {
          "aws:PrincipalOrgID": "o-1234567890"
        }
      }
    }
  ]
}
```

### Example 4: Monitoring shared resource access with CloudWatch and Lambda

```python
import json
import boto3
from datetime import datetime, timedelta

def lambda_handler(event, context):
    """
    Monitor shared resource access and generate alerts
    """
    
    # Initialize AWS clients
    cloudtrail = boto3.client('cloudtrail')
    cloudwatch = boto3.client('cloudwatch')
    sns = boto3.client('sns')
    
    try:
        # Look for cross-account access events in the last hour
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=1)
        
        response = cloudtrail.lookup_events(
            LookupAttributes=[
                {
                    'AttributeKey': 'EventName',
                    'AttributeValue': 'AssumeRole'
                }
            ],
            StartTime=start_time,
            EndTime=end_time
        )
        
        cross_account_events = []
        
        for event in response.get('Events', []):
            event_detail = json.loads(event.get('CloudTrailEvent', '{}'))
            
            # Check if this is cross-account access
            if is_cross_account_access(event_detail):
                cross_account_events.append(event_detail)
        
        # Analyze access patterns
        analysis_result = analyze_access_patterns(cross_account_events)
        
        # Send metrics to CloudWatch
        send_metrics_to_cloudwatch(cloudwatch, analysis_result)
        
        # Send alerts if suspicious activity detected
        if analysis_result.get('suspicious_activity'):
            send_security_alert(sns, analysis_result)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'events_processed': len(cross_account_events),
                'suspicious_activity': analysis_result.get('suspicious_activity', False)
            })
        }
        
    except Exception as e:
        print(f"Error monitoring shared resource access: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }

def is_cross_account_access(event_detail):
    """Check if the event represents cross-account access"""
    
    source_account = event_detail.get('recipientAccountId')
    assumed_role_arn = event_detail.get('responseElements', {}).get('assumedRoleUser', {}).get('arn', '')
    
    if assumed_role_arn:
        # Extract account ID from the assumed role ARN
        role_account = assumed_role_arn.split(':')[4]
        return source_account != role_account
    
    return False

def analyze_access_patterns(events):
    """Analyze access patterns for suspicious activity"""
    
    analysis = {
        'total_events': len(events),
        'unique_accounts': set(),
        'unique_roles': set(),
        'suspicious_activity': False
    }
    
    for event in events:
        source_ip = event.get('sourceIPAddress')
        user_identity = event.get('userIdentity', {})
        
        analysis['unique_accounts'].add(user_identity.get('accountId'))
        analysis['unique_roles'].add(user_identity.get('arn'))
        
        # Check for suspicious patterns
        if is_suspicious_access(event):
            analysis['suspicious_activity'] = True
    
    analysis['unique_accounts'] = len(analysis['unique_accounts'])
    analysis['unique_roles'] = len(analysis['unique_roles'])
    
    return analysis

def is_suspicious_access(event):
    """Identify potentially suspicious access patterns"""
    
    source_ip = event.get('sourceIPAddress')
    user_agent = event.get('userAgent', '')
    
    # Check for access from unexpected locations
    suspicious_ips = ['0.0.0.0']  # Add known suspicious IPs
    if source_ip in suspicious_ips:
        return True
    
    # Check for unusual user agents
    if 'aws-cli' not in user_agent.lower() and 'aws-sdk' not in user_agent.lower():
        return True
    
    return False

def send_metrics_to_cloudwatch(cloudwatch, analysis):
    """Send metrics to CloudWatch"""
    
    cloudwatch.put_metric_data(
        Namespace='SharedResources/Access',
        MetricData=[
            {
                'MetricName': 'CrossAccountEvents',
                'Value': analysis['total_events'],
                'Unit': 'Count'
            },
            {
                'MetricName': 'UniqueAccounts',
                'Value': analysis['unique_accounts'],
                'Unit': 'Count'
            }
        ]
    )

def send_security_alert(sns, analysis):
    """Send security alert for suspicious activity"""
    
    message = f"Suspicious shared resource access detected!\n\n"
    message += f"Total cross-account events: {analysis['total_events']}\n"
    message += f"Unique accounts involved: {analysis['unique_accounts']}\n"
    message += f"Unique roles involved: {analysis['unique_roles']}\n"
    
    sns.publish(
        TopicArn='arn:aws:sns:us-west-2:123456789012:SecurityAlerts',
        Subject='Suspicious Shared Resource Access',
        Message=message
    )
```

## AWS services to consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Resource Access Manager (RAM)</h4>
    <p>Helps you securely share your resources across AWS accounts within your organization or organizational units (OUs) and with IAM roles and users for supported resource types.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Identity and Access Management (IAM)</h4>
    <p>Enables you to manage access to AWS services and resources securely. Use IAM roles for secure cross-account access without sharing credentials.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Organizations</h4>
    <p>Helps you centrally manage and govern your environment as you scale your AWS resources. Use Organizations to define trusted relationships for resource sharing.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon S3</h4>
    <p>Object storage service that offers industry-leading scalability, data availability, security, and performance. Use S3 bucket policies and Access Points for secure data sharing.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS CloudTrail</h4>
    <p>Records API calls for your account and delivers log files to you. Use CloudTrail to monitor and audit shared resource access across accounts.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon CloudWatch</h4>
    <p>Monitors your AWS resources and the applications you run on AWS in real time. Set up metrics and alarms for shared resource usage and access patterns.</p>
  </div>
</div>

## Benefits of sharing resources securely within your organization

- **Enhanced collaboration**: Enables teams to work together while maintaining security boundaries
- **Reduced duplication**: Eliminates the need to duplicate resources across accounts
- **Centralized management**: Provides centralized control over shared resource access
- **Improved security**: Maintains least privilege access while enabling necessary sharing
- **Cost optimization**: Reduces costs by sharing common resources instead of duplicating them
- **Operational efficiency**: Streamlines resource management across multiple teams and accounts
- **Better governance**: Provides clear ownership and accountability for shared resources

## Related resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/sec_permissions_share_securely.html">AWS Well-Architected Framework - Share resources securely within your organization</a></li>
    <li><a href="https://docs.aws.amazon.com/ram/latest/userguide/what-is.html">AWS Resource Access Manager User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/tutorial_cross-account-with-roles.html">Tutorial: Delegate access across AWS accounts using IAM roles</a></li>
    <li><a href="https://docs.aws.amazon.com/s3/latest/userguide/access-points.html">Managing data access with Amazon S3 access points</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-use-aws-resource-access-manager-to-share-your-vpc-subnets-with-your-organization/">How to use AWS Resource Access Manager to share your VPC subnets with your organization</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-monitor-and-visualize-failed-ssh-access-attempts-to-amazon-ec2-linux-instances/">How to monitor and visualize failed SSH access attempts to Amazon EC2 Linux instances</a></li>
  </ul>
</div>
