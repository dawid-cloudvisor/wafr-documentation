---
title: SEC05-BP04 - Automate network protection
layout: default
parent: SEC05 - How do you protect your network resources?
grand_parent: Security
nav_order: 4
---

<div class="pillar-header">
  <h1>SEC05-BP04: Automate network protection</h1>
  <p>Automate your protective controls to provide a self-defending network based on threat intelligence and anomaly detection. For example, intrusion detection and prevention tools can adapt to current threats and reduce their impact. A web application firewall can automatically block or rate limit requests based on patterns in the traffic.</p>
</div>

## Implementation guidance

Automating network protection enables your security infrastructure to respond to threats in real-time without human intervention. By implementing automated protective controls, you can significantly reduce response times and ensure consistent application of security policies across your network infrastructure.

### Key steps for implementing this best practice:

1. **Implement automated threat response**:
   - Configure automatic blocking of malicious IP addresses
   - Set up automated quarantine of compromised resources
   - Implement dynamic security group rule updates
   - Configure automatic traffic redirection during attacks
   - Enable automated incident escalation procedures

2. **Deploy adaptive security controls**:
   - Implement machine learning-based anomaly detection
   - Configure behavioral analysis for network traffic
   - Set up adaptive rate limiting based on traffic patterns
   - Deploy dynamic firewall rules based on threat intelligence
   - Implement context-aware access controls

3. **Configure automated policy enforcement**:
   - Implement Infrastructure as Code for consistent security policies
   - Set up automated compliance checking and remediation
   - Configure automatic security configuration drift detection
   - Deploy policy-based network segmentation
   - Implement automated security baseline enforcement

4. **Enable intelligent traffic management**:
   - Configure automatic load balancing during DDoS attacks
   - Implement geo-blocking based on threat intelligence
   - Set up automated content delivery network (CDN) protection
   - Deploy intelligent traffic routing for threat mitigation
   - Configure automatic capacity scaling for attack resilience

5. **Integrate threat intelligence feeds**:
   - Configure automatic updates from threat intelligence sources
   - Implement real-time indicator of compromise (IoC) blocking
   - Set up automated reputation-based filtering
   - Deploy dynamic blacklist and whitelist management
   - Configure threat hunting automation

6. **Implement automated monitoring and alerting**:
   - Set up real-time security event correlation
   - Configure automated anomaly detection and alerting
   - Implement predictive threat analysis
   - Deploy automated security metrics collection
   - Set up intelligent alert prioritization and routing

## Implementation examples

### Example 1: Automated threat response with Lambda and EventBridge

```python
import boto3
import json
from datetime import datetime, timedelta

def lambda_handler(event, context):
    """
    Automated network protection response function
    Responds to GuardDuty findings and WAF events
    """
    
    # Initialize AWS clients
    ec2 = boto3.client('ec2')
    wafv2 = boto3.client('wafv2')
    sns = boto3.client('sns')
    
    try:
        # Parse the incoming event
        event_source = event.get('source')
        detail = event.get('detail', {})
        
        if event_source == 'aws.guardduty':
            return handle_guardduty_finding(ec2, wafv2, sns, detail)
        elif event_source == 'aws.wafv2':
            return handle_waf_event(ec2, wafv2, sns, detail)
        else:
            print(f"Unsupported event source: {event_source}")
            return {'statusCode': 400, 'body': 'Unsupported event source'}
            
    except Exception as e:
        print(f"Error processing event: {str(e)}")
        return {'statusCode': 500, 'body': f'Error: {str(e)}'}

def handle_guardduty_finding(ec2, wafv2, sns, detail):
    """Handle GuardDuty findings with automated response"""
    
    finding_type = detail.get('type', '')
    severity = detail.get('severity', 0)
    
    # Extract threat information
    remote_ip = None
    instance_id = None
    
    if 'service' in detail and 'remoteIpDetails' in detail['service']:
        remote_ip = detail['service']['remoteIpDetails'].get('ipAddressV4')
    
    if 'resource' in detail and 'instanceDetails' in detail['resource']:
        instance_id = detail['resource']['instanceDetails'].get('instanceId')
    
    response_actions = []
    
    # High severity findings require immediate action
    if severity >= 7.0:
        if remote_ip:
            # Block malicious IP in WAF
            block_result = block_ip_in_waf(wafv2, remote_ip)
            response_actions.append(f"Blocked IP {remote_ip} in WAF: {block_result}")
            
            # Add IP to security group deny rule
            sg_result = add_ip_to_deny_rule(ec2, remote_ip)
            response_actions.append(f"Added IP {remote_ip} to deny rule: {sg_result}")
        
        if instance_id and 'Backdoor' in finding_type:
            # Isolate compromised instance
            isolation_result = isolate_instance(ec2, instance_id)
            response_actions.append(f"Isolated instance {instance_id}: {isolation_result}")
    
    # Medium severity findings get monitoring enhancement
    elif severity >= 4.0:
        if remote_ip:
            # Add IP to monitoring watchlist
            watchlist_result = add_ip_to_watchlist(remote_ip)
            response_actions.append(f"Added IP {remote_ip} to watchlist: {watchlist_result}")
    
    # Send notification
    send_notification(sns, finding_type, severity, response_actions)
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'finding_type': finding_type,
            'severity': severity,
            'actions_taken': response_actions
        })
    }

def block_ip_in_waf(wafv2, ip_address):
    """Add IP address to WAF IP set for blocking"""
    
    try:
        # Get existing IP set
        ip_set_response = wafv2.get_ip_set(
            Name='AutoBlockedIPs',
            Scope='REGIONAL',
            Id='12345678-1234-1234-1234-123456789012'
        )
        
        current_addresses = ip_set_response['IPSet']['Addresses']
        
        # Add new IP if not already present
        if f"{ip_address}/32" not in current_addresses:
            current_addresses.append(f"{ip_address}/32")
            
            # Update IP set
            wafv2.update_ip_set(
                Name='AutoBlockedIPs',
                Scope='REGIONAL',
                Id='12345678-1234-1234-1234-123456789012',
                Addresses=current_addresses,
                LockToken=ip_set_response['LockToken']
            )
            
            return "Success"
        else:
            return "Already blocked"
            
    except Exception as e:
        print(f"Error blocking IP in WAF: {str(e)}")
        return f"Error: {str(e)}"

def add_ip_to_deny_rule(ec2, ip_address):
    """Add IP address to security group deny rule"""
    
    try:
        # Create or update security group rule
        ec2.authorize_security_group_ingress(
            GroupId='sg-blocklist123456',
            IpPermissions=[
                {
                    'IpProtocol': '-1',
                    'IpRanges': [
                        {
                            'CidrIp': f'{ip_address}/32',
                            'Description': f'Auto-blocked malicious IP - {datetime.utcnow().isoformat()}'
                        }
                    ]
                }
            ]
        )
        return "Success"
        
    except ec2.exceptions.ClientError as e:
        if 'InvalidPermission.Duplicate' in str(e):
            return "Already blocked"
        else:
            print(f"Error adding IP to deny rule: {str(e)}")
            return f"Error: {str(e)}"

def isolate_instance(ec2, instance_id):
    """Isolate compromised instance by changing security group"""
    
    try:
        # Get current instance details
        response = ec2.describe_instances(InstanceIds=[instance_id])
        
        if response['Reservations']:
            instance = response['Reservations'][0]['Instances'][0]
            
            # Change security group to isolation group
            ec2.modify_instance_attribute(
                InstanceId=instance_id,
                Groups=['sg-isolation123456']
            )
            
            # Add tag to indicate isolation
            ec2.create_tags(
                Resources=[instance_id],
                Tags=[
                    {
                        'Key': 'SecurityStatus',
                        'Value': 'Isolated'
                    },
                    {
                        'Key': 'IsolationTime',
                        'Value': datetime.utcnow().isoformat()
                    }
                ]
            )
            
            return "Success"
        else:
            return "Instance not found"
            
    except Exception as e:
        print(f"Error isolating instance: {str(e)}")
        return f"Error: {str(e)}"

def add_ip_to_watchlist(ip_address):
    """Add IP to monitoring watchlist for enhanced tracking"""
    
    # This would integrate with your monitoring system
    # For example, adding to CloudWatch custom metrics or external SIEM
    
    try:
        cloudwatch = boto3.client('cloudwatch')
        
        # Send custom metric for watchlist IP
        cloudwatch.put_metric_data(
            Namespace='Security/Watchlist',
            MetricData=[
                {
                    'MetricName': 'SuspiciousIP',
                    'Dimensions': [
                        {
                            'Name': 'IPAddress',
                            'Value': ip_address
                        }
                    ],
                    'Value': 1,
                    'Unit': 'Count',
                    'Timestamp': datetime.utcnow()
                }
            ]
        )
        
        return "Success"
        
    except Exception as e:
        print(f"Error adding IP to watchlist: {str(e)}")
        return f"Error: {str(e)}"

def send_notification(sns, finding_type, severity, actions):
    """Send notification about automated response actions"""
    
    message = f"""
Automated Network Protection Response

Finding Type: {finding_type}
Severity: {severity}
Timestamp: {datetime.utcnow().isoformat()}

Actions Taken:
"""
    
    for action in actions:
        message += f"- {action}\n"
    
    try:
        sns.publish(
            TopicArn='arn:aws:sns:us-west-2:123456789012:NetworkProtectionAlerts',
            Subject=f'Automated Response: {finding_type}',
            Message=message
        )
    except Exception as e:
        print(f"Error sending notification: {str(e)}")

def handle_waf_event(ec2, wafv2, sns, detail):
    """Handle WAF events for automated response"""
    
    # Extract WAF event details
    blocked_requests = detail.get('blockedRequests', 0)
    source_ip = detail.get('sourceIP')
    
    # If high volume of blocked requests, enhance protection
    if blocked_requests > 1000:
        if source_ip:
            # Add to more restrictive blocking
            enhanced_block_result = enhance_ip_blocking(wafv2, source_ip)
            
            # Send alert
            send_notification(sns, 'High Volume Attack', 8.0, [enhanced_block_result])
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'blocked_requests': blocked_requests,
            'source_ip': source_ip
        })
    }

def enhance_ip_blocking(wafv2, ip_address):
    """Enhance blocking for high-volume attackers"""
    
    try:
        # Add to high-priority block list with longer duration
        # Implementation would depend on your specific WAF configuration
        return f"Enhanced blocking for {ip_address}"
        
    except Exception as e:
        return f"Error enhancing block: {str(e)}"
```

### Example 2: Automated security group management

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Automated security group management with Lambda'

Resources:
  # Lambda function for automated security group updates
  SecurityGroupAutomationFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: SecurityGroupAutomation
      Runtime: python3.9
      Handler: index.lambda_handler
      Role: !GetAtt SecurityGroupAutomationRole.Arn
      Timeout: 300
      Code:
        ZipFile: |
          import boto3
          import json
          from datetime import datetime, timedelta
          
          def lambda_handler(event, context):
              ec2 = boto3.client('ec2')
              
              # Automated security group rule cleanup
              cleanup_expired_rules(ec2)
              
              # Update security groups based on threat intelligence
              update_threat_intelligence_rules(ec2)
              
              return {'statusCode': 200, 'body': 'Security groups updated'}
          
          def cleanup_expired_rules(ec2):
              # Remove temporary rules that have expired
              try:
                  # Get security groups with temporary rules
                  response = ec2.describe_security_groups(
                      Filters=[
                          {
                              'Name': 'tag:AutoManaged',
                              'Values': ['true']
                          }
                      ]
                  )
                  
                  for sg in response['SecurityGroups']:
                      for rule in sg.get('IpPermissions', []):
                          for ip_range in rule.get('IpRanges', []):
                              description = ip_range.get('Description', '')
                              if 'Expires:' in description:
                                  # Parse expiration date and remove if expired
                                  # Implementation details would go here
                                  pass
                                  
              except Exception as e:
                  print(f"Error cleaning up rules: {str(e)}")
          
          def update_threat_intelligence_rules(ec2):
              # Update rules based on latest threat intelligence
              try:
                  # This would integrate with threat intelligence feeds
                  # Implementation details would go here
                  pass
              except Exception as e:
                  print(f"Error updating threat intelligence: {str(e)}")

  # IAM role for Lambda function
  SecurityGroupAutomationRole:
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
        - PolicyName: SecurityGroupManagement
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - ec2:DescribeSecurityGroups
                  - ec2:AuthorizeSecurityGroupIngress
                  - ec2:RevokeSecurityGroupIngress
                  - ec2:AuthorizeSecurityGroupEgress
                  - ec2:RevokeSecurityGroupEgress
                  - ec2:CreateTags
                  - ec2:DescribeTags
                Resource: '*'

  # EventBridge rule for scheduled execution
  SecurityGroupAutomationSchedule:
    Type: AWS::Events::Rule
    Properties:
      Name: SecurityGroupAutomationSchedule
      Description: 'Trigger security group automation every hour'
      ScheduleExpression: 'rate(1 hour)'
      State: ENABLED
      Targets:
        - Arn: !GetAtt SecurityGroupAutomationFunction.Arn
          Id: SecurityGroupAutomationTarget

  # Permission for EventBridge to invoke Lambda
  SecurityGroupAutomationPermission:
    Type: AWS::Lambda::Permission
    Properties:
      FunctionName: !Ref SecurityGroupAutomationFunction
      Action: lambda:InvokeFunction
      Principal: events.amazonaws.com
      SourceArn: !GetAtt SecurityGroupAutomationSchedule.Arn

  # Auto-managed security group for dynamic rules
  AutoManagedSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: 'Auto-managed security group for dynamic threat response'
      VpcId: !Ref VPC
      Tags:
        - Key: Name
          Value: Auto-Managed-SG
        - Key: AutoManaged
          Value: 'true'
        - Key: Purpose
          Value: 'Dynamic-Threat-Response'

  # Security group for isolated instances
  IsolationSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: 'Security group for isolated instances'
      VpcId: !Ref VPC
      SecurityGroupEgress: []  # No outbound rules - complete isolation
      Tags:
        - Key: Name
          Value: Isolation-SG
        - Key: Purpose
          Value: 'Instance-Isolation'

### Example 3: Automated DDoS protection with CloudFront and Shield

```python
import boto3
import json
from datetime import datetime

def setup_automated_ddos_protection():
    """Configure automated DDoS protection with CloudFront and Shield Advanced"""
    
    cloudfront = boto3.client('cloudfront')
    shield = boto3.client('shield')
    route53 = boto3.client('route53')
    
    # Enable Shield Advanced for enhanced DDoS protection
    try:
        shield.create_subscription()
        print("Shield Advanced subscription created")
    except shield.exceptions.ResourceAlreadyExistsException:
        print("Shield Advanced already enabled")
    
    # Create CloudFront distribution with DDoS protection
    distribution_config = {
        'CallerReference': f'ddos-protection-{datetime.utcnow().strftime("%Y%m%d%H%M%S")}',
        'Comment': 'Automated DDoS protection distribution',
        'DefaultCacheBehavior': {
            'TargetOriginId': 'primary-origin',
            'ViewerProtocolPolicy': 'redirect-to-https',
            'TrustedSigners': {
                'Enabled': False,
                'Quantity': 0
            },
            'ForwardedValues': {
                'QueryString': False,
                'Cookies': {'Forward': 'none'}
            },
            'MinTTL': 0,
            'Compress': True
        },
        'Origins': {
            'Quantity': 1,
            'Items': [
                {
                    'Id': 'primary-origin',
                    'DomainName': 'example.com',
                    'CustomOriginConfig': {
                        'HTTPPort': 80,
                        'HTTPSPort': 443,
                        'OriginProtocolPolicy': 'https-only',
                        'OriginSslProtocols': {
                            'Quantity': 1,
                            'Items': ['TLSv1.2']
                        }
                    }
                }
            ]
        },
        'Enabled': True,
        'WebACLId': 'arn:aws:wafv2:us-east-1:123456789012:global/webacl/DDoSProtection/12345678-1234-1234-1234-123456789012'
    }
    
    try:
        distribution_response = cloudfront.create_distribution(
            DistributionConfig=distribution_config
        )
        
        distribution_id = distribution_response['Distribution']['Id']
        distribution_domain = distribution_response['Distribution']['DomainName']
        
        print(f"Created CloudFront distribution: {distribution_id}")
        
        # Configure Route 53 health checks for failover
        setup_health_checks_and_failover(route53, distribution_domain)
        
        return distribution_id
        
    except Exception as e:
        print(f"Error creating CloudFront distribution: {str(e)}")
        return None

def setup_health_checks_and_failover(route53, distribution_domain):
    """Set up Route 53 health checks and automated failover"""
    
    try:
        # Create health check for primary endpoint
        health_check_response = route53.create_health_check(
            Type='HTTPS',
            ResourcePath='/health',
            FullyQualifiedDomainName=distribution_domain,
            Port=443,
            RequestInterval=30,
            FailureThreshold=3,
            Tags=[
                {
                    'Key': 'Name',
                    'Value': 'Primary-Endpoint-Health-Check'
                }
            ]
        )
        
        health_check_id = health_check_response['HealthCheck']['Id']
        
        # Create CloudWatch alarm for health check
        cloudwatch = boto3.client('cloudwatch')
        
        cloudwatch.put_metric_alarm(
            AlarmName='PrimaryEndpointHealthCheck',
            ComparisonOperator='LessThanThreshold',
            EvaluationPeriods=2,
            MetricName='HealthCheckStatus',
            Namespace='AWS/Route53',
            Period=60,
            Statistic='Minimum',
            Threshold=1.0,
            ActionsEnabled=True,
            AlarmActions=[
                'arn:aws:sns:us-west-2:123456789012:DDoSProtectionAlerts'
            ],
            AlarmDescription='Primary endpoint health check failure',
            Dimensions=[
                {
                    'Name': 'HealthCheckId',
                    'Value': health_check_id
                }
            ]
        )
        
        print(f"Created health check and alarm: {health_check_id}")
        
    except Exception as e:
        print(f"Error setting up health checks: {str(e)}")

def create_automated_waf_rules():
    """Create WAF rules with automated DDoS protection"""
    
    wafv2 = boto3.client('wafv2')
    
    # Create rate-based rule with automatic scaling
    rate_based_rule = {
        'Name': 'AutomatedRateLimiting',
        'Priority': 1,
        'Action': {'Block': {}},
        'Statement': {
            'RateBasedStatement': {
                'Limit': 2000,
                'AggregateKeyType': 'IP',
                'ScopeDownStatement': {
                    'NotStatement': {
                        'Statement': {
                            'GeoMatchStatement': {
                                'CountryCodes': ['US', 'CA', 'GB']  # Allow from trusted countries
                            }
                        }
                    }
                }
            }
        },
        'VisibilityConfig': {
            'SampledRequestsEnabled': True,
            'CloudWatchMetricsEnabled': True,
            'MetricName': 'AutomatedRateLimiting'
        }
    }
    
    # Create adaptive rule based on request patterns
    adaptive_rule = {
        'Name': 'AdaptiveProtection',
        'Priority': 2,
        'Action': {'Block': {}},
        'Statement': {
            'AndStatement': {
                'Statements': [
                    {
                        'ByteMatchStatement': {
                            'SearchString': 'bot',
                            'FieldToMatch': {'SingleHeader': {'Name': 'user-agent'}},
                            'TextTransformations': [
                                {'Priority': 1, 'Type': 'LOWERCASE'}
                            ],
                            'PositionalConstraint': 'CONTAINS'
                        }
                    },
                    {
                        'RateBasedStatement': {
                            'Limit': 100,
                            'AggregateKeyType': 'IP'
                        }
                    }
                ]
            }
        },
        'VisibilityConfig': {
            'SampledRequestsEnabled': True,
            'CloudWatchMetricsEnabled': True,
            'MetricName': 'AdaptiveProtection'
        }
    }
    
    try:
        web_acl_response = wafv2.create_web_acl(
            Name='AutomatedDDoSProtection',
            Scope='CLOUDFRONT',
            DefaultAction={'Allow': {}},
            Rules=[rate_based_rule, adaptive_rule],
            Description='Automated DDoS protection with adaptive rules',
            Tags=[
                {
                    'Key': 'Name',
                    'Value': 'Automated-DDoS-Protection'
                }
            ],
            VisibilityConfig={
                'SampledRequestsEnabled': True,
                'CloudWatchMetricsEnabled': True,
                'MetricName': 'AutomatedDDoSProtection'
            }
        )
        
        return web_acl_response['Summary']['ARN']
        
    except Exception as e:
        print(f"Error creating automated WAF rules: {str(e)}")
        return None

### Example 4: Infrastructure as Code for automated network security

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Automated network security infrastructure'

Parameters:
  VpcCidr:
    Type: String
    Default: '10.0.0.0/16'
  ThreatIntelligenceBucket:
    Type: String
    Description: 'S3 bucket containing threat intelligence feeds'

Resources:
  # Custom resource for automated threat intelligence updates
  ThreatIntelligenceUpdater:
    Type: AWS::CloudFormation::CustomResource
    Properties:
      ServiceToken: !GetAtt ThreatIntelligenceFunction.Arn
      ThreatIntelligenceBucket: !Ref ThreatIntelligenceBucket

  # Lambda function for threat intelligence processing
  ThreatIntelligenceFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: ThreatIntelligenceProcessor
      Runtime: python3.9
      Handler: index.lambda_handler
      Role: !GetAtt ThreatIntelligenceRole.Arn
      Timeout: 300
      Code:
        ZipFile: |
          import boto3
          import json
          import cfnresponse
          
          def lambda_handler(event, context):
              try:
                  if event['RequestType'] == 'Create' or event['RequestType'] == 'Update':
                      # Process threat intelligence feeds
                      process_threat_intelligence(event['ResourceProperties'])
                      cfnresponse.send(event, context, cfnresponse.SUCCESS, {})
                  else:
                      cfnresponse.send(event, context, cfnresponse.SUCCESS, {})
              except Exception as e:
                  print(f"Error: {str(e)}")
                  cfnresponse.send(event, context, cfnresponse.FAILED, {})
          
          def process_threat_intelligence(properties):
              # Download and process threat intelligence feeds
              # Update WAF IP sets and security groups
              pass

  # IAM role for threat intelligence function
  ThreatIntelligenceRole:
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
        - PolicyName: ThreatIntelligencePolicy
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - s3:GetObject
                  - s3:ListBucket
                  - wafv2:UpdateIPSet
                  - wafv2:GetIPSet
                  - ec2:AuthorizeSecurityGroupIngress
                  - ec2:RevokeSecurityGroupIngress
                Resource: '*'

  # EventBridge rule for automated threat intelligence updates
  ThreatIntelligenceSchedule:
    Type: AWS::Events::Rule
    Properties:
      Name: ThreatIntelligenceUpdate
      Description: 'Update threat intelligence feeds every 4 hours'
      ScheduleExpression: 'rate(4 hours)'
      State: ENABLED
      Targets:
        - Arn: !GetAtt ThreatIntelligenceFunction.Arn
          Id: ThreatIntelligenceTarget

  # Permission for EventBridge to invoke Lambda
  ThreatIntelligencePermission:
    Type: AWS::Lambda::Permission
    Properties:
      FunctionName: !Ref ThreatIntelligenceFunction
      Action: lambda:InvokeFunction
      Principal: events.amazonaws.com
      SourceArn: !GetAtt ThreatIntelligenceSchedule.Arn

  # Auto-scaling group for network security appliances
  NetworkSecurityASG:
    Type: AWS::AutoScaling::AutoScalingGroup
    Properties:
      AutoScalingGroupName: NetworkSecurityAppliances
      VPCZoneIdentifier:
        - !Ref PrivateSubnet1
        - !Ref PrivateSubnet2
      LaunchTemplate:
        LaunchTemplateId: !Ref SecurityApplianceLaunchTemplate
        Version: !GetAtt SecurityApplianceLaunchTemplate.LatestVersionNumber
      MinSize: 2
      MaxSize: 10
      DesiredCapacity: 2
      TargetGroupARNs:
        - !Ref SecurityApplianceTargetGroup
      Tags:
        - Key: Name
          Value: Network-Security-Appliance
          PropagateAtLaunch: true

  # Launch template for security appliances
  SecurityApplianceLaunchTemplate:
    Type: AWS::EC2::LaunchTemplate
    Properties:
      LaunchTemplateName: SecurityApplianceLaunchTemplate
      LaunchTemplateData:
        ImageId: ami-12345678  # Security appliance AMI
        InstanceType: c5.large
        SecurityGroupIds:
          - !Ref SecurityApplianceSecurityGroup
        IamInstanceProfile:
          Arn: !GetAtt SecurityApplianceInstanceProfile.Arn
        UserData:
          Fn::Base64: !Sub |
            #!/bin/bash
            # Configure security appliance with automated threat feeds
            /opt/security-appliance/configure-automation.sh

Outputs:
  ThreatIntelligenceFunctionArn:
    Description: 'ARN of the threat intelligence processing function'
    Value: !GetAtt ThreatIntelligenceFunction.Arn
    Export:
      Name: !Sub '${AWS::StackName}-ThreatIntelligence-Function'
```

## AWS services to consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Lambda</h4>
    <p>Lets you run code without provisioning or managing servers. Essential for implementing automated response functions and security orchestration workflows.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon EventBridge</h4>
    <p>A serverless event bus that makes it easy to connect applications together. Enables automated response to security events from multiple AWS services.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Systems Manager</h4>
    <p>Gives you visibility and control of your infrastructure on AWS. Provides automation capabilities for security configuration management and incident response.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon CloudWatch</h4>
    <p>Monitors your AWS resources and applications in real time. Provides metrics, alarms, and automated actions for network security monitoring.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS CloudFormation</h4>
    <p>Gives you an easy way to model a collection of related AWS and third-party resources. Enables Infrastructure as Code for consistent security deployments.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon GuardDuty</h4>
    <p>Provides intelligent threat detection for your AWS accounts and workloads. Integrates with automated response systems for immediate threat mitigation.</p>
  </div>
</div>

## Benefits of automating network protection

- **Rapid threat response**: Automated systems can respond to threats in seconds rather than minutes or hours
- **Consistent policy enforcement**: Automation ensures security policies are applied uniformly across all network resources
- **Reduced human error**: Automated processes eliminate mistakes that can occur during manual security operations
- **24/7 protection**: Automated systems provide continuous protection without requiring human oversight
- **Scalable security**: Automation scales with your infrastructure growth without proportional increases in security staff
- **Improved threat intelligence**: Automated systems can process and act on threat intelligence feeds in real-time
- **Cost efficiency**: Reduces operational costs by minimizing manual security operations and faster incident resolution

## Related resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/sec_network_auto_protect.html">AWS Well-Architected Framework - Automate network protection</a></li>
    <li><a href="https://docs.aws.amazon.com/lambda/latest/dg/welcome.html">AWS Lambda Developer Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-what-is.html">Amazon EventBridge User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/systems-manager/latest/userguide/what-is-systems-manager.html">AWS Systems Manager User Guide</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-automate-incident-response-in-aws-cloud-for-ec2-instances/">How to automate incident response in AWS Cloud for EC2 instances</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-build-a-multi-region-incident-response-plan/">How to build a multi-Region incident response plan</a></li>
  </ul>
</div>
```
