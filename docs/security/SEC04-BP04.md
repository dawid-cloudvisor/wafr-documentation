---
title: SEC04-BP04 - Initiate remediation for non-compliant resources
layout: default
parent: SEC04 - How do you detect and investigate security events?
grand_parent: Security
nav_order: 4
---

<div class="pillar-header">
  <h1>SEC04-BP04: Initiate remediation for non-compliant resources</h1>
  <p>Implement automated remediation for non-compliant resources to reduce the time to resolution and improve your security posture. For example, automatically remediate an S3 bucket that has been configured with public read access by removing the public access configuration.</p>
</div>

## Implementation guidance

Automated remediation of non-compliant resources is essential for maintaining a strong security posture at scale. By implementing automated responses to security violations and misconfigurations, you can reduce the window of exposure, minimize manual intervention, and ensure consistent application of security policies across your environment.

### Key steps for implementing this best practice:

1. **Identify remediable security violations**:
   - Define security policies and compliance requirements
   - Identify common misconfigurations that can be automatically remediated
   - Categorize violations by risk level and remediation complexity
   - Document approved remediation actions for each violation type
   - Establish criteria for automatic vs. manual remediation

2. **Implement detection mechanisms**:
   - Use AWS Config Rules to detect configuration violations
   - Configure AWS Security Hub for centralized finding management
   - Set up Amazon GuardDuty for threat detection
   - Implement custom detection logic for organization-specific requirements
   - Enable real-time monitoring for critical security configurations

3. **Design remediation workflows**:
   - Create automated remediation scripts and functions
   - Implement approval workflows for high-risk remediations
   - Design rollback mechanisms for failed remediations
   - Establish notification and logging for all remediation actions
   - Implement rate limiting to prevent cascading effects

4. **Implement automated remediation**:
   - Use AWS Config Remediation Configurations for standard violations
   - Deploy AWS Lambda functions for custom remediation logic
   - Implement AWS Systems Manager Automation documents
   - Use AWS Security Hub Custom Actions for manual remediation triggers
   - Configure Amazon EventBridge for event-driven remediation

5. **Establish governance and oversight**:
   - Implement approval processes for sensitive remediations
   - Create audit trails for all remediation activities
   - Set up monitoring and alerting for remediation failures
   - Establish escalation procedures for complex violations
   - Implement regular review of remediation effectiveness

6. **Test and validate remediation**:
   - Test remediation scripts in non-production environments
   - Validate that remediation actions don't break functionality
   - Implement monitoring to verify successful remediation
   - Create rollback procedures for problematic remediations
   - Regularly review and update remediation logic

## Implementation examples

### Example 1: AWS Config automatic remediation for S3 public access

```yaml
# CloudFormation template for S3 public access remediation
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Automatic remediation for S3 buckets with public access'

Resources:
  # Config rule to detect public S3 buckets
  S3PublicAccessRule:
    Type: AWS::Config::ConfigRule
    Properties:
      ConfigRuleName: s3-bucket-public-access-prohibited
      Description: Checks that your S3 buckets do not allow public read access
      Source:
        Owner: AWS
        SourceIdentifier: S3_BUCKET_PUBLIC_READ_PROHIBITED
      Scope:
        ComplianceResourceTypes:
          - AWS::S3::Bucket

  # Remediation configuration
  S3PublicAccessRemediation:
    Type: AWS::Config::RemediationConfiguration
    Properties:
      ConfigRuleName: !Ref S3PublicAccessRule
      TargetType: SSM_DOCUMENT
      TargetId: AWSConfigRemediation-RemoveS3BucketPublicAccess
      TargetVersion: "1"
      Parameters:
        AutomationAssumeRole:
          StaticValue: !GetAtt RemediationRole.Arn
        BucketName:
          ResourceValue: RESOURCE_ID
      Automatic: true
      MaximumAutomaticAttempts: 3

  # IAM role for remediation
  RemediationRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service:
                - ssm.amazonaws.com
                - config.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/ConfigRole
      Policies:
        - PolicyName: S3RemediationPolicy
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - s3:GetBucketAcl
                  - s3:GetBucketPolicy
                  - s3:GetBucketPolicyStatus
                  - s3:GetBucketPublicAccessBlock
                  - s3:PutBucketPublicAccessBlock
                  - s3:DeleteBucketPolicy
                Resource: '*'

  # SNS topic for notifications
  RemediationNotifications:
    Type: AWS::SNS::Topic
    Properties:
      TopicName: S3RemediationNotifications
      DisplayName: S3 Remediation Notifications

  # EventBridge rule for remediation events
  RemediationEventRule:
    Type: AWS::Events::Rule
    Properties:
      Name: S3RemediationEvents
      Description: Capture S3 remediation events
      EventPattern:
        source:
          - aws.config
        detail-type:
          - Config Rules Compliance Change
        detail:
          configRuleName:
            - !Ref S3PublicAccessRule
      State: ENABLED
      Targets:
        - Arn: !Ref RemediationNotifications
          Id: SNSTarget
```

### Example 2: Custom Lambda function for security group remediation

```python
import json
import boto3
from datetime import datetime

def lambda_handler(event, context):
    """
    Lambda function to remediate overly permissive security groups
    """
    
    ec2 = boto3.client('ec2')
    sns = boto3.client('sns')
    
    try:
        # Parse the Config rule evaluation result
        config_item = event['configurationItem']
        resource_id = config_item['resourceId']
        
        # Get security group details
        response = ec2.describe_security_groups(GroupIds=[resource_id])
        security_group = response['SecurityGroups'][0]
        
        # Check for overly permissive rules
        remediation_actions = []
        
        for rule in security_group.get('IpPermissions', []):
            if has_unrestricted_access(rule):
                remediation_actions.append({
                    'action': 'revoke_ingress',
                    'rule': rule,
                    'reason': 'Unrestricted access detected'
                })
        
        # Perform remediation
        if remediation_actions:
            remediation_result = perform_security_group_remediation(
                ec2, resource_id, remediation_actions
            )
            
            # Send notification
            send_remediation_notification(
                sns, resource_id, remediation_actions, remediation_result
            )
            
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'resource_id': resource_id,
                    'actions_taken': len(remediation_actions),
                    'success': remediation_result['success']
                })
            }
        else:
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'resource_id': resource_id,
                    'message': 'No remediation required'
                })
            }
            
    except Exception as e:
        print(f"Error remediating security group: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }

def has_unrestricted_access(rule):
    """Check if a security group rule has unrestricted access"""
    
    # Check for 0.0.0.0/0 in IPv4 ranges
    for ip_range in rule.get('IpRanges', []):
        if ip_range.get('CidrIp') == '0.0.0.0/0':
            # Allow HTTP/HTTPS from anywhere for web servers
            if rule.get('FromPort') in [80, 443]:
                continue
            return True
    
    # Check for ::/0 in IPv6 ranges
    for ipv6_range in rule.get('Ipv6Ranges', []):
        if ipv6_range.get('CidrIpv6') == '::/0':
            if rule.get('FromPort') in [80, 443]:
                continue
            return True
    
    return False

def perform_security_group_remediation(ec2, group_id, actions):
    """Perform the actual remediation actions"""
    
    remediation_result = {
        'success': True,
        'actions_completed': [],
        'actions_failed': []
    }
    
    for action in actions:
        try:
            if action['action'] == 'revoke_ingress':
                # Create a backup rule first
                backup_rule(ec2, group_id, action['rule'])
                
                # Revoke the overly permissive rule
                ec2.revoke_security_group_ingress(
                    GroupId=group_id,
                    IpPermissions=[action['rule']]
                )
                
                remediation_result['actions_completed'].append(action)
                print(f"Successfully revoked rule from {group_id}")
                
        except Exception as e:
            print(f"Failed to remediate rule: {str(e)}")
            remediation_result['actions_failed'].append({
                'action': action,
                'error': str(e)
            })
            remediation_result['success'] = False
    
    return remediation_result

def backup_rule(ec2, group_id, rule):
    """Create a backup of the security group rule"""
    
    # Store rule details in DynamoDB for potential rollback
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('SecurityGroupBackups')
    
    backup_item = {
        'group_id': group_id,
        'timestamp': datetime.utcnow().isoformat(),
        'rule': json.dumps(rule, default=str),
        'action': 'revoked_by_remediation'
    }
    
    table.put_item(Item=backup_item)
    print(f"Backed up rule for {group_id}")

def send_remediation_notification(sns, resource_id, actions, result):
    """Send notification about remediation actions"""
    
    message = f"""
Security Group Remediation Report

Resource ID: {resource_id}
Timestamp: {datetime.utcnow().isoformat()}

Actions Taken:
"""
    
    for action in actions:
        message += f"- {action['action']}: {action['reason']}\n"
    
    message += f"\nRemediation Success: {result['success']}\n"
    message += f"Actions Completed: {len(result['actions_completed'])}\n"
    message += f"Actions Failed: {len(result['actions_failed'])}\n"
    
    if result['actions_failed']:
        message += "\nFailed Actions:\n"
        for failed_action in result['actions_failed']:
            message += f"- {failed_action['error']}\n"
    
    try:
        sns.publish(
            TopicArn='arn:aws:sns:us-west-2:123456789012:SecurityRemediationAlerts',
            Subject=f'Security Group Remediation: {resource_id}',
            Message=message
        )
    except Exception as e:
        print(f"Failed to send notification: {str(e)}")
```

### Example 3: Systems Manager Automation for EC2 instance remediation

```yaml
# SSM Automation document for EC2 instance remediation
schemaVersion: '0.3'
description: 'Remediate non-compliant EC2 instances'
assumeRole: '{{AutomationAssumeRole}}'
parameters:
  InstanceId:
    type: String
    description: 'EC2 Instance ID to remediate'
  AutomationAssumeRole:
    type: String
    description: 'IAM role for automation'
  ViolationType:
    type: String
    description: 'Type of security violation'
    allowedValues:
      - 'missing-security-patches'
      - 'non-compliant-security-group'
      - 'missing-encryption'
      - 'unauthorized-software'

mainSteps:
  - name: DetermineRemediationAction
    action: 'aws:branch'
    inputs:
      Choices:
        - Variable: '{{ViolationType}}'
          StringEquals: 'missing-security-patches'
          NextStep: InstallSecurityPatches
        - Variable: '{{ViolationType}}'
          StringEquals: 'non-compliant-security-group'
          NextStep: UpdateSecurityGroup
        - Variable: '{{ViolationType}}'
          StringEquals: 'missing-encryption'
          NextStep: EnableEncryption
        - Variable: '{{ViolationType}}'
          StringEquals: 'unauthorized-software'
          NextStep: RemoveUnauthorizedSoftware
      Default: NotifyManualReview

  - name: InstallSecurityPatches
    action: 'aws:runCommand'
    inputs:
      DocumentName: 'AWS-RunPatchBaseline'
      InstanceIds:
        - '{{InstanceId}}'
      Parameters:
        Operation: 'Install'
    nextStep: VerifyRemediation

  - name: UpdateSecurityGroup
    action: 'aws:executeAwsApi'
    inputs:
      Service: ec2
      Api: ModifyInstanceAttribute
      InstanceId: '{{InstanceId}}'
      Groups:
        - 'sg-compliant-security-group'
    nextStep: VerifyRemediation

  - name: EnableEncryption
    action: 'aws:executeScript'
    inputs:
      Runtime: python3.8
      Handler: enable_encryption
      Script: |
        def enable_encryption(events, context):
            import boto3
            
            ec2 = boto3.client('ec2')
            instance_id = events['InstanceId']
            
            # Stop instance
            ec2.stop_instances(InstanceIds=[instance_id])
            
            # Wait for instance to stop
            waiter = ec2.get_waiter('instance_stopped')
            waiter.wait(InstanceIds=[instance_id])
            
            # Create encrypted snapshot and replace root volume
            # Implementation details would go here
            
            return {'status': 'success'}
      InputPayload:
        InstanceId: '{{InstanceId}}'
    nextStep: VerifyRemediation

  - name: RemoveUnauthorizedSoftware
    action: 'aws:runCommand'
    inputs:
      DocumentName: 'AWS-RunShellScript'
      InstanceIds:
        - '{{InstanceId}}'
      Parameters:
        commands:
          - 'sudo apt-get remove -y unauthorized-package || sudo yum remove -y unauthorized-package'
          - 'sudo systemctl stop unauthorized-service || sudo service unauthorized-service stop'
    nextStep: VerifyRemediation

  - name: VerifyRemediation
    action: 'aws:executeScript'
    inputs:
      Runtime: python3.8
      Handler: verify_remediation
      Script: |
        def verify_remediation(events, context):
            # Implement verification logic
            return {'verification_status': 'passed'}
      InputPayload:
        InstanceId: '{{InstanceId}}'
        ViolationType: '{{ViolationType}}'
    nextStep: SendNotification

  - name: SendNotification
    action: 'aws:executeAwsApi'
    inputs:
      Service: sns
      Api: Publish
      TopicArn: 'arn:aws:sns:us-west-2:123456789012:RemediationNotifications'
      Subject: 'EC2 Instance Remediation Completed'
      Message: 'Instance {{InstanceId}} has been successfully remediated for {{ViolationType}}'
    isEnd: true

  - name: NotifyManualReview
    action: 'aws:executeAwsApi'
    inputs:
      Service: sns
      Api: Publish
      TopicArn: 'arn:aws:sns:us-west-2:123456789012:ManualReviewRequired'
      Subject: 'Manual Review Required'
      Message: 'Instance {{InstanceId}} requires manual review for {{ViolationType}}'
    isEnd: true

outputs:
  - RemediationStatus
  - VerificationResult
```

### Example 4: EventBridge-driven remediation orchestration

```python
import json
import boto3
from datetime import datetime

def lambda_handler(event, context):
    """
    Orchestrate remediation based on EventBridge events
    """
    
    # Initialize AWS clients
    config_client = boto3.client('config')
    ssm_client = boto3.client('ssm')
    sns_client = boto3.client('sns')
    
    try:
        # Parse the incoming event
        event_source = event.get('source')
        detail_type = event.get('detail-type')
        detail = event.get('detail', {})
        
        # Determine remediation strategy
        remediation_plan = determine_remediation_strategy(event_source, detail_type, detail)
        
        if not remediation_plan:
            return {
                'statusCode': 200,
                'body': json.dumps('No remediation required')
            }
        
        # Execute remediation
        remediation_result = execute_remediation(
            config_client, ssm_client, remediation_plan
        )
        
        # Send notification
        send_remediation_summary(sns_client, remediation_plan, remediation_result)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'remediation_plan': remediation_plan['type'],
                'success': remediation_result['success'],
                'resources_remediated': len(remediation_result.get('completed', []))
            })
        }
        
    except Exception as e:
        print(f"Error in remediation orchestration: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }

def determine_remediation_strategy(source, detail_type, detail):
    """Determine the appropriate remediation strategy"""
    
    remediation_strategies = {
        'aws.config': {
            'Config Rules Compliance Change': handle_config_compliance_change,
        },
        'aws.securityhub': {
            'Security Hub Findings - Imported': handle_security_hub_finding,
        },
        'aws.guardduty': {
            'GuardDuty Finding': handle_guardduty_finding,
        }
    }
    
    handler = remediation_strategies.get(source, {}).get(detail_type)
    
    if handler:
        return handler(detail)
    
    return None

def handle_config_compliance_change(detail):
    """Handle AWS Config compliance changes"""
    
    if detail.get('newEvaluationResult', {}).get('complianceType') == 'NON_COMPLIANT':
        resource_type = detail.get('resourceType')
        resource_id = detail.get('resourceId')
        config_rule_name = detail.get('configRuleName')
        
        # Map Config rules to remediation actions
        remediation_mapping = {
            's3-bucket-public-access-prohibited': {
                'type': 'config_remediation',
                'action': 'remove_s3_public_access',
                'resource_type': resource_type,
                'resource_id': resource_id,
                'automation_document': 'AWSConfigRemediation-RemoveS3BucketPublicAccess'
            },
            'ec2-security-group-attached-to-eni': {
                'type': 'custom_remediation',
                'action': 'update_security_group',
                'resource_type': resource_type,
                'resource_id': resource_id,
                'lambda_function': 'SecurityGroupRemediationFunction'
            },
            'encrypted-volumes': {
                'type': 'ssm_automation',
                'action': 'enable_ebs_encryption',
                'resource_type': resource_type,
                'resource_id': resource_id,
                'automation_document': 'CustomEBSEncryptionRemediation'
            }
        }
        
        return remediation_mapping.get(config_rule_name)
    
    return None

def handle_security_hub_finding(detail):
    """Handle Security Hub findings"""
    
    findings = detail.get('findings', [])
    
    for finding in findings:
        severity = finding.get('Severity', {}).get('Label')
        finding_type = finding.get('Types', [])
        
        if severity in ['HIGH', 'CRITICAL']:
            # Determine remediation based on finding type
            if 'Sensitive Data Identifications' in str(finding_type):
                return {
                    'type': 'data_protection',
                    'action': 'encrypt_sensitive_data',
                    'finding_id': finding.get('Id'),
                    'resources': finding.get('Resources', [])
                }
            elif 'Network Reachability' in str(finding_type):
                return {
                    'type': 'network_security',
                    'action': 'restrict_network_access',
                    'finding_id': finding.get('Id'),
                    'resources': finding.get('Resources', [])
                }
    
    return None

def handle_guardduty_finding(detail):
    """Handle GuardDuty findings"""
    
    finding_type = detail.get('type', '')
    severity = detail.get('severity', 0)
    
    if severity >= 7.0:  # High severity findings
        if 'Backdoor' in finding_type or 'Trojan' in finding_type:
            return {
                'type': 'incident_response',
                'action': 'isolate_compromised_instance',
                'finding_id': detail.get('id'),
                'instance_id': detail.get('resource', {}).get('instanceDetails', {}).get('instanceId')
            }
        elif 'CryptoCurrency' in finding_type:
            return {
                'type': 'malware_response',
                'action': 'block_cryptocurrency_mining',
                'finding_id': detail.get('id'),
                'instance_id': detail.get('resource', {}).get('instanceDetails', {}).get('instanceId')
            }
    
    return None

def execute_remediation(config_client, ssm_client, plan):
    """Execute the remediation plan"""
    
    result = {
        'success': False,
        'completed': [],
        'failed': [],
        'details': {}
    }
    
    try:
        if plan['type'] == 'config_remediation':
            # Use AWS Config remediation
            response = config_client.start_remediation_execution(
                ConfigRuleName=plan.get('config_rule_name', ''),
                ResourceKeys=[
                    {
                        'resourceType': plan['resource_type'],
                        'resourceId': plan['resource_id']
                    }
                ]
            )
            result['success'] = True
            result['completed'].append(plan['resource_id'])
            result['details']['remediation_execution_id'] = response.get('FailureMessage', 'Success')
            
        elif plan['type'] == 'ssm_automation':
            # Use Systems Manager automation
            response = ssm_client.start_automation_execution(
                DocumentName=plan['automation_document'],
                Parameters={
                    'InstanceId': [plan['resource_id']],
                    'AutomationAssumeRole': ['arn:aws:iam::123456789012:role/AutomationRole']
                }
            )
            result['success'] = True
            result['completed'].append(plan['resource_id'])
            result['details']['automation_execution_id'] = response['AutomationExecutionId']
            
        elif plan['type'] == 'custom_remediation':
            # Invoke custom Lambda function
            lambda_client = boto3.client('lambda')
            response = lambda_client.invoke(
                FunctionName=plan['lambda_function'],
                Payload=json.dumps({
                    'resource_id': plan['resource_id'],
                    'action': plan['action']
                })
            )
            result['success'] = True
            result['completed'].append(plan['resource_id'])
            result['details']['lambda_response'] = json.loads(response['Payload'].read())
            
    except Exception as e:
        result['failed'].append({
            'resource_id': plan.get('resource_id'),
            'error': str(e)
        })
        print(f"Remediation failed: {str(e)}")
    
    return result

def send_remediation_summary(sns_client, plan, result):
    """Send summary of remediation actions"""
    
    message = f"""
Automated Remediation Summary

Remediation Type: {plan['type']}
Action: {plan['action']}
Timestamp: {datetime.utcnow().isoformat()}

Results:
- Success: {result['success']}
- Resources Completed: {len(result['completed'])}
- Resources Failed: {len(result['failed'])}

"""
    
    if result['completed']:
        message += f"Successfully remediated: {', '.join(result['completed'])}\n"
    
    if result['failed']:
        message += "Failed remediations:\n"
        for failure in result['failed']:
            message += f"- {failure['resource_id']}: {failure['error']}\n"
    
    try:
        sns_client.publish(
            TopicArn='arn:aws:sns:us-west-2:123456789012:RemediationSummary',
            Subject=f"Remediation Summary: {plan['type']}",
            Message=message
        )
    except Exception as e:
        print(f"Failed to send notification: {str(e)}")
```

## AWS services to consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Config</h4>
    <p>Enables you to assess, audit, and evaluate the configurations of your AWS resources. Provides built-in remediation configurations for common security violations.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Systems Manager</h4>
    <p>Gives you visibility and control of your infrastructure on AWS. Use Automation documents to implement complex remediation workflows across multiple resources.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Lambda</h4>
    <p>Lets you run code without provisioning or managing servers. Ideal for implementing custom remediation logic and orchestrating remediation workflows.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon EventBridge</h4>
    <p>A serverless event bus that makes it easy to connect applications together. Essential for triggering remediation actions based on security events.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Security Hub</h4>
    <p>Provides a comprehensive view of your security state in AWS. Supports custom actions for manual remediation triggers and centralized finding management.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon GuardDuty</h4>
    <p>Provides intelligent threat detection for your AWS accounts and workloads. Findings can trigger automated remediation workflows for threat response.</p>
  </div>
</div>

## Benefits of initiating remediation for non-compliant resources

- **Reduced exposure time**: Automated remediation minimizes the window of vulnerability
- **Consistent security posture**: Ensures uniform application of security policies across all resources
- **Operational efficiency**: Reduces manual intervention and speeds up incident response
- **Scalable security management**: Handles large-scale environments without proportional increase in staff
- **Improved compliance**: Maintains continuous compliance with security standards and regulations
- **Cost reduction**: Reduces the cost of manual security operations and potential breach impacts
- **Enhanced audit readiness**: Provides detailed logs of all remediation actions for compliance reporting

## Related resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/sec_detect_investigate_events_noncompliant_resources.html">AWS Well-Architected Framework - Initiate remediation for non-compliant resources</a></li>
    <li><a href="https://docs.aws.amazon.com/config/latest/developerguide/remediation.html">AWS Config Remediation</a></li>
    <li><a href="https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-automation.html">AWS Systems Manager Automation</a></li>
    <li><a href="https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-custom-actions.html">AWS Security Hub Custom Actions</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-set-up-continuous-compliance-with-aws-config-and-aws-systems-manager/">How to set up continuous compliance with AWS Config and AWS Systems Manager</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-remediate-amazon-inspector-security-findings-automatically/">How to remediate Amazon Inspector security findings automatically</a></li>
  </ul>
</div>
