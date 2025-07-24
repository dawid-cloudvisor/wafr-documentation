---
title: SEC03-BP09 - Share resources securely with a third party
layout: default
parent: SEC03 - How do you manage permissions for people and machines?
grand_parent: Security
nav_order: 9
---

<div class="pillar-header">
  <h1>SEC03-BP09: Share resources securely with a third party</h1>
  <p>You might need to share resources with a third party, such as a content delivery network (CDN), a contractor, or a shared service provider. When you share resources with a third party, use mechanisms such as cross-account roles with external IDs, resource-based policies, or third-party access management to maintain control over who can access your resources and under what conditions.</p>
</div>

## Implementation guidance

Sharing resources with third parties introduces additional security considerations beyond internal sharing. It's essential to implement strong controls, monitoring, and governance to ensure that third-party access remains secure and compliant with your organization's security policies.

### Key steps for implementing this best practice:

1. **Establish third-party access governance**:
   - Define policies for third-party access to your resources
   - Implement approval processes for third-party access requests
   - Document third-party relationships and access requirements
   - Establish contractual security requirements for third parties
   - Create procedures for onboarding and offboarding third parties

2. **Implement secure access mechanisms**:
   - Use cross-account IAM roles with external IDs for third-party access
   - Implement time-limited access with automatic expiration
   - Use resource-based policies with specific conditions
   - Apply network-level restrictions where possible
   - Avoid sharing long-term credentials or access keys

3. **Apply additional security controls**:
   - Implement multi-factor authentication requirements
   - Use IP address restrictions for third-party access
   - Apply time-based access controls
   - Implement session monitoring and recording
   - Use encryption for data shared with third parties

4. **Monitor and audit third-party access**:
   - Track all third-party access activities
   - Set up alerts for unusual access patterns
   - Generate regular reports on third-party access
   - Implement automated compliance checks
   - Maintain detailed audit trails

5. **Implement data protection measures**:
   - Classify data before sharing with third parties
   - Apply appropriate encryption for shared data
   - Implement data loss prevention (DLP) controls
   - Use data masking or tokenization where appropriate
   - Establish data retention and deletion policies

6. **Regularly review and validate access**:
   - Conduct periodic reviews of third-party access
   - Validate business justification for continued access
   - Update access permissions based on changing requirements
   - Remove access when no longer needed
   - Test access revocation procedures

## Implementation examples

### Example 1: Cross-account role for third-party access with external ID

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::THIRD-PARTY-ACCOUNT:root"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "sts:ExternalId": "UniqueExternalId-ThirdParty-2024"
        },
        "IpAddress": {
          "aws:SourceIp": [
            "203.0.113.0/24",
            "198.51.100.0/24"
          ]
        },
        "DateGreaterThan": {
          "aws:CurrentTime": "2024-01-01T00:00:00Z"
        },
        "DateLessThan": {
          "aws:CurrentTime": "2024-06-30T23:59:59Z"
        },
        "Bool": {
          "aws:MultiFactorAuthPresent": "true"
        }
      }
    }
  ]
}
```

### Example 2: S3 bucket policy for secure third-party data sharing

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ThirdPartyReadAccess",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::THIRD-PARTY-ACCOUNT:role/DataProcessorRole"
      },
      "Action": [
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::shared-data-bucket/third-party-data/*",
        "arn:aws:s3:::shared-data-bucket"
      ],
      "Condition": {
        "StringEquals": {
          "s3:x-amz-server-side-encryption": "aws:kms",
          "s3:x-amz-server-side-encryption-aws-kms-key-id": "arn:aws:kms:us-west-2:123456789012:key/12345678-1234-1234-1234-123456789012"
        },
        "Bool": {
          "aws:SecureTransport": "true"
        },
        "IpAddress": {
          "aws:SourceIp": "203.0.113.0/24"
        },
        "StringLike": {
          "s3:x-amz-content-sha256": "*"
        }
      }
    },
    {
      "Sid": "DenyUnencryptedObjectUploads",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:PutObject",
      "Resource": "arn:aws:s3:::shared-data-bucket/third-party-data/*",
      "Condition": {
        "StringNotEquals": {
          "s3:x-amz-server-side-encryption": "aws:kms"
        }
      }
    }
  ]
}
```

### Example 3: Lambda function for third-party access monitoring

```python
import json
import boto3
from datetime import datetime, timedelta

def lambda_handler(event, context):
    """
    Monitor third-party access and generate security alerts
    """
    
    # Initialize AWS clients
    cloudtrail = boto3.client('cloudtrail')
    sns = boto3.client('sns')
    dynamodb = boto3.resource('dynamodb')
    
    # Third-party account IDs to monitor
    third_party_accounts = [
        'THIRD-PARTY-ACCOUNT-1',
        'THIRD-PARTY-ACCOUNT-2'
    ]
    
    try:
        # Look for third-party access events in the last hour
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=1)
        
        response = cloudtrail.lookup_events(
            StartTime=start_time,
            EndTime=end_time
        )
        
        third_party_events = []
        
        for event in response.get('Events', []):
            event_detail = json.loads(event.get('CloudTrailEvent', '{}'))
            
            # Check if this is third-party access
            if is_third_party_access(event_detail, third_party_accounts):
                third_party_events.append(event_detail)
        
        # Analyze access patterns
        analysis_result = analyze_third_party_access(third_party_events)
        
        # Store access data for trend analysis
        store_access_data(dynamodb, analysis_result)
        
        # Send alerts if suspicious activity detected
        if analysis_result.get('alerts'):
            send_security_alerts(sns, analysis_result)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'events_processed': len(third_party_events),
                'alerts_generated': len(analysis_result.get('alerts', []))
            })
        }
        
    except Exception as e:
        print(f"Error monitoring third-party access: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }

def is_third_party_access(event_detail, third_party_accounts):
    """Check if the event represents third-party access"""
    
    user_identity = event_detail.get('userIdentity', {})
    account_id = user_identity.get('accountId')
    
    return account_id in third_party_accounts

def analyze_third_party_access(events):
    """Analyze third-party access patterns for security issues"""
    
    analysis = {
        'total_events': len(events),
        'unique_accounts': set(),
        'unique_users': set(),
        'alerts': []
    }
    
    for event in events:
        user_identity = event.get('userIdentity', {})
        source_ip = event.get('sourceIPAddress')
        event_name = event.get('eventName')
        
        analysis['unique_accounts'].add(user_identity.get('accountId'))
        analysis['unique_users'].add(user_identity.get('arn'))
        
        # Check for suspicious patterns
        if is_suspicious_third_party_access(event):
            analysis['alerts'].append({
                'type': 'suspicious_access',
                'event_name': event_name,
                'source_ip': source_ip,
                'user_arn': user_identity.get('arn'),
                'timestamp': event.get('eventTime')
            })
        
        # Check for access outside allowed hours
        if is_outside_allowed_hours(event):
            analysis['alerts'].append({
                'type': 'outside_hours_access',
                'event_name': event_name,
                'user_arn': user_identity.get('arn'),
                'timestamp': event.get('eventTime')
            })
    
    analysis['unique_accounts'] = len(analysis['unique_accounts'])
    analysis['unique_users'] = len(analysis['unique_users'])
    
    return analysis

def is_suspicious_third_party_access(event):
    """Identify potentially suspicious third-party access"""
    
    source_ip = event.get('sourceIPAddress')
    event_name = event.get('eventName')
    
    # Check for access from unexpected IP addresses
    allowed_ips = ['203.0.113.0/24', '198.51.100.0/24']  # Define allowed IP ranges
    if not any(ip_in_range(source_ip, allowed_ip) for allowed_ip in allowed_ips):
        return True
    
    # Check for high-risk actions
    high_risk_actions = [
        'DeleteBucket',
        'PutBucketPolicy',
        'CreateUser',
        'AttachUserPolicy'
    ]
    
    if event_name in high_risk_actions:
        return True
    
    return False

def is_outside_allowed_hours(event):
    """Check if access is outside allowed business hours"""
    
    event_time = datetime.fromisoformat(event.get('eventTime').replace('Z', '+00:00'))
    
    # Define allowed hours (9 AM to 6 PM UTC)
    allowed_start = 9
    allowed_end = 18
    
    if event_time.hour < allowed_start or event_time.hour >= allowed_end:
        return True
    
    # Check if it's weekend
    if event_time.weekday() >= 5:  # Saturday = 5, Sunday = 6
        return True
    
    return False

def ip_in_range(ip, cidr):
    """Check if IP address is in CIDR range"""
    import ipaddress
    try:
        return ipaddress.ip_address(ip) in ipaddress.ip_network(cidr)
    except:
        return False

def store_access_data(dynamodb, analysis):
    """Store access data for trend analysis"""
    
    table = dynamodb.Table('ThirdPartyAccessLog')
    
    table.put_item(
        Item={
            'timestamp': datetime.utcnow().isoformat(),
            'total_events': analysis['total_events'],
            'unique_accounts': analysis['unique_accounts'],
            'unique_users': analysis['unique_users'],
            'alert_count': len(analysis['alerts'])
        }
    )

def send_security_alerts(sns, analysis):
    """Send security alerts for suspicious third-party access"""
    
    if not analysis['alerts']:
        return
    
    message = f"Third-party security alerts detected!\n\n"
    message += f"Total events: {analysis['total_events']}\n"
    message += f"Number of alerts: {len(analysis['alerts'])}\n\n"
    
    for alert in analysis['alerts'][:5]:  # Limit to first 5 alerts
        message += f"Alert Type: {alert['type']}\n"
        message += f"Event: {alert['event_name']}\n"
        message += f"User: {alert.get('user_arn', 'Unknown')}\n"
        message += f"Source IP: {alert.get('source_ip', 'Unknown')}\n"
        message += f"Time: {alert['timestamp']}\n\n"
    
    sns.publish(
        TopicArn='arn:aws:sns:us-west-2:123456789012:ThirdPartySecurityAlerts',
        Subject='Third-Party Access Security Alert',
        Message=message
    )
```

### Example 4: CloudFormation template for third-party access setup

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Third-party access setup with monitoring'

Parameters:
  ThirdPartyAccountId:
    Type: String
    Description: AWS Account ID of the third party
  ExternalId:
    Type: String
    Description: External ID for additional security
    NoEcho: true
  AllowedIPRange:
    Type: String
    Description: IP range allowed for third-party access
    Default: '203.0.113.0/24'

Resources:
  ThirdPartyAccessRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: ThirdPartyAccessRole
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              AWS: !Sub 'arn:aws:iam::${ThirdPartyAccountId}:root'
            Action: 'sts:AssumeRole'
            Condition:
              StringEquals:
                'sts:ExternalId': !Ref ExternalId
              IpAddress:
                'aws:SourceIp': !Ref AllowedIPRange
              Bool:
                'aws:MultiFactorAuthPresent': 'true'
      ManagedPolicyArns:
        - 'arn:aws:iam::aws:policy/ReadOnlyAccess'
      Tags:
        - Key: Purpose
          Value: ThirdPartyAccess
        - Key: Environment
          Value: Production

  ThirdPartyAccessPolicy:
    Type: AWS::IAM::Policy
    Properties:
      PolicyName: ThirdPartyAccessPolicy
      PolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Action:
              - 's3:GetObject'
              - 's3:ListBucket'
            Resource:
              - !Sub '${SharedDataBucket}'
              - !Sub '${SharedDataBucket}/*'
            Condition:
              Bool:
                'aws:SecureTransport': 'true'
      Roles:
        - !Ref ThirdPartyAccessRole

  SharedDataBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub 'third-party-shared-data-${AWS::AccountId}'
      BucketEncryption:
        ServerSideEncryptionConfiguration:
          - ServerSideEncryptionByDefault:
              SSEAlgorithm: aws:kms
              KMSMasterKeyID: !Ref SharedDataKMSKey
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true
      NotificationConfiguration:
        CloudWatchConfigurations:
          - Event: 's3:ObjectCreated:*'
            CloudWatchConfiguration:
              LogGroupName: !Ref AccessLogGroup

  SharedDataKMSKey:
    Type: AWS::KMS::Key
    Properties:
      Description: 'KMS key for third-party shared data encryption'
      KeyPolicy:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              AWS: !Sub 'arn:aws:iam::${AWS::AccountId}:root'
            Action: 'kms:*'
            Resource: '*'
          - Effect: Allow
            Principal:
              AWS: !GetAtt ThirdPartyAccessRole.Arn
            Action:
              - 'kms:Decrypt'
              - 'kms:GenerateDataKey'
            Resource: '*'

  AccessLogGroup:
    Type: AWS::Logs::LogGroup
    Properties:
      LogGroupName: '/aws/third-party-access'
      RetentionInDays: 90

Outputs:
  ThirdPartyRoleArn:
    Description: 'ARN of the third-party access role'
    Value: !GetAtt ThirdPartyAccessRole.Arn
  SharedBucketName:
    Description: 'Name of the shared data bucket'
    Value: !Ref SharedDataBucket
```

## AWS services to consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Identity and Access Management (IAM)</h4>
    <p>Enables you to manage access to AWS services and resources securely. Use IAM roles with external IDs for secure third-party access without sharing credentials.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS CloudTrail</h4>
    <p>Records API calls for your account and delivers log files to you. Essential for monitoring and auditing third-party access activities.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon CloudWatch</h4>
    <p>Monitors your AWS resources and the applications you run on AWS in real time. Set up alerts and dashboards for third-party access monitoring.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Key Management Service (KMS)</h4>
    <p>Makes it easy for you to create and manage cryptographic keys and control their use. Use KMS to encrypt data shared with third parties.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon S3</h4>
    <p>Object storage service that offers industry-leading scalability, data availability, security, and performance. Use S3 bucket policies and encryption for secure data sharing with third parties.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Config</h4>
    <p>Enables you to assess, audit, and evaluate the configurations of your AWS resources. Use Config rules to monitor compliance with third-party access policies.</p>
  </div>
</div>

## Benefits of sharing resources securely with third parties

- **Enhanced security**: Maintains control over third-party access while enabling necessary collaboration
- **Improved compliance**: Supports regulatory requirements for third-party data sharing and access control
- **Better risk management**: Reduces risks associated with third-party access through proper controls
- **Operational efficiency**: Enables secure collaboration without compromising security posture
- **Audit readiness**: Provides comprehensive audit trails for third-party access activities
- **Scalable governance**: Establishes repeatable processes for managing third-party relationships
- **Incident response**: Enables quick identification and response to third-party security incidents

## Related resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/sec_permissions_share_securely_third_party.html">AWS Well-Architected Framework - Share resources securely with a third party</a></li>
    <li><a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_common-scenarios_third-party.html">Providing access to an AWS account owned by a third party</a></li>
    <li><a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html">AWS global condition context keys</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-use-external-id-when-granting-access-to-your-aws-resources/">How to use external ID when granting access to your AWS resources</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-monitor-and-visualize-failed-ssh-access-attempts-to-amazon-ec2-linux-instances/">How to monitor and visualize failed SSH access attempts to Amazon EC2 Linux instances</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-create-a-secure-account-structure-using-aws-organizations-and-aws-sso/">How to create a secure account structure using AWS Organizations and AWS SSO</a></li>
  </ul>
</div>
