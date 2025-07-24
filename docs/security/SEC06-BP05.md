---
title: SEC06-BP05 - Automate compute protection
layout: default
parent: SEC06 - How do you protect your compute resources?
grand_parent: Security
nav_order: 5
---

<div class="pillar-header">
  <h1>SEC06-BP05: Automate compute protection</h1>
  <p>Automate your compute protection to improve your security posture, reduce human error, and scale your security operations. Use automation to consistently apply security configurations, respond to security events, and maintain compliance across your compute resources. Implement automated security scanning, patch management, and incident response to ensure comprehensive protection.</p>
</div>

## Implementation guidance

Automating compute protection is essential for maintaining a robust security posture at scale. By implementing automated security controls, monitoring, and response mechanisms, you can ensure consistent protection across all compute resources while reducing the burden on security teams and minimizing the risk of human error.

### Key steps for implementing this best practice:

1. **Implement automated security configuration management**:
   - Use Infrastructure as Code (IaC) for consistent security configurations
   - Automate security baseline deployment and enforcement
   - Implement configuration drift detection and remediation
   - Use policy-as-code for security compliance validation
   - Establish automated security configuration testing

2. **Deploy automated threat detection and response**:
   - Implement endpoint detection and response (EDR) solutions
   - Configure automated malware detection and quarantine
   - Set up behavioral analysis and anomaly detection
   - Implement automated incident response workflows
   - Configure real-time threat intelligence integration

3. **Establish automated vulnerability management**:
   - Implement continuous vulnerability scanning
   - Automate patch deployment and testing
   - Configure automated security updates
   - Set up vulnerability prioritization and remediation workflows
   - Implement automated compliance reporting

4. **Configure automated monitoring and alerting**:
   - Implement comprehensive security event monitoring
   - Set up automated log analysis and correlation
   - Configure intelligent alerting and notification systems
   - Implement automated security metrics collection
   - Establish automated compliance monitoring

5. **Implement automated backup and recovery**:
   - Configure automated backup scheduling and execution
   - Implement automated backup verification and testing
   - Set up automated disaster recovery procedures
   - Configure automated failover and failback processes
   - Implement automated recovery validation

6. **Establish automated security orchestration**:
   - Implement Security Orchestration, Automation, and Response (SOAR)
   - Configure automated playbook execution
   - Set up automated evidence collection and preservation
   - Implement automated communication and notification workflows
   - Configure automated reporting and documentation

## Implementation examples

### Example 1: Automated security configuration with AWS Config

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Automated compute protection with AWS Config and remediation'

Resources:
  # Configuration Recorder
  ConfigurationRecorder:
    Type: AWS::Config::ConfigurationRecorder
    Properties:
      Name: 'ComputeProtectionRecorder'
      RoleARN: !GetAtt ConfigRole.Arn
      RecordingGroup:
        AllSupported: true
        IncludeGlobalResourceTypes: true

  # Delivery Channel
  DeliveryChannel:
    Type: AWS::Config::DeliveryChannel
    Properties:
      Name: 'ComputeProtectionDeliveryChannel'
      S3BucketName: !Ref ConfigBucket
      ConfigSnapshotDeliveryProperties:
        DeliveryFrequency: 'TwentyFour_Hours'

  # S3 Bucket for Config
  ConfigBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub 'aws-config-${AWS::AccountId}-${AWS::Region}'
      BucketEncryption:
        ServerSideEncryptionConfiguration:
          - ServerSideEncryptionByDefault:
              SSEAlgorithm: AES256
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true

  # IAM Role for Config
  ConfigRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: config.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/ConfigRole
      Policies:
        - PolicyName: ConfigBucketPolicy
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - s3:GetBucketAcl
                  - s3:ListBucket
                Resource: !Sub '${ConfigBucket}'
              - Effect: Allow
                Action:
                  - s3:GetObject
                  - s3:PutObject
                Resource: !Sub '${ConfigBucket}/*'

  # Config Rule: EC2 instances should not have public IP
  EC2NoPublicIPRule:
    Type: AWS::Config::ConfigRule
    DependsOn: ConfigurationRecorder
    Properties:
      ConfigRuleName: 'ec2-instance-no-public-ip'
      Description: 'Checks whether Amazon EC2 instances have a public IP association'
      Source:
        Owner: AWS
        SourceIdentifier: 'EC2_INSTANCE_NO_PUBLIC_IP'
      Scope:
        ComplianceResourceTypes:
          - 'AWS::EC2::Instance'

  # Config Rule: Security groups should not allow unrestricted access
  SecurityGroupRestrictedRule:
    Type: AWS::Config::ConfigRule
    DependsOn: ConfigurationRecorder
    Properties:
      ConfigRuleName: 'incoming-ssh-disabled'
      Description: 'Checks whether security groups disallow unrestricted incoming SSH traffic'
      Source:
        Owner: AWS
        SourceIdentifier: 'INCOMING_SSH_DISABLED'

  # Config Rule: EBS volumes should be encrypted
  EBSEncryptionRule:
    Type: AWS::Config::ConfigRule
    DependsOn: ConfigurationRecorder
    Properties:
      ConfigRuleName: 'encrypted-volumes'
      Description: 'Checks whether EBS volumes are encrypted'
      Source:
        Owner: AWS
        SourceIdentifier: 'ENCRYPTED_VOLUMES'

  # Remediation Configuration for Security Groups
  SecurityGroupRemediation:
    Type: AWS::Config::RemediationConfiguration
    Properties:
      ConfigRuleName: !Ref SecurityGroupRestrictedRule
      TargetType: 'SSM_DOCUMENT'
      TargetId: 'RemediateUnrestrictedSecurityGroup'
      TargetVersion: '1'
      Parameters:
        AutomationAssumeRole:
          StaticValue: !GetAtt RemediationRole.Arn
        GroupId:
          ResourceValue: 'RESOURCE_ID'
      Automatic: true
      MaximumAutomaticAttempts: 3

  # IAM Role for Remediation
  RemediationRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: ssm.amazonaws.com
            Action: sts:AssumeRole
      Policies:
        - PolicyName: RemediationPolicy
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - ec2:DescribeSecurityGroups
                  - ec2:AuthorizeSecurityGroupIngress
                  - ec2:RevokeSecurityGroupIngress
                  - ec2:CreateTags
                Resource: '*'

  # Systems Manager Document for Security Group Remediation
  SecurityGroupRemediationDocument:
    Type: AWS::SSM::Document
    Properties:
      DocumentType: 'Automation'
      DocumentFormat: 'YAML'
      Name: 'RemediateUnrestrictedSecurityGroup'
      Content:
        schemaVersion: '0.3'
        description: 'Remediate unrestricted security group rules'
        assumeRole: '{{ AutomationAssumeRole }}'
        parameters:
          GroupId:
            type: String
            description: 'Security Group ID to remediate'
          AutomationAssumeRole:
            type: String
            description: 'IAM role for automation'
        mainSteps:
          - name: 'RemoveUnrestrictedRules'
            action: 'aws:executeScript'
            inputs:
              Runtime: 'python3.8'
              Handler: 'remediate_security_group'
              Script: |
                import boto3
                
                def remediate_security_group(events, context):
                    ec2 = boto3.client('ec2')
                    group_id = events['GroupId']
                    
                    try:
                        # Get security group details
                        response = ec2.describe_security_groups(GroupIds=[group_id])
                        sg = response['SecurityGroups'][0]
                        
                        # Check for unrestricted SSH access (0.0.0.0/0 on port 22)
                        for rule in sg['IpPermissions']:
                            if (rule.get('FromPort') == 22 and 
                                rule.get('ToPort') == 22 and
                                rule.get('IpProtocol') == 'tcp'):
                                
                                for ip_range in rule.get('IpRanges', []):
                                    if ip_range.get('CidrIp') == '0.0.0.0/0':
                                        # Remove the unrestricted rule
                                        ec2.revoke_security_group_ingress(
                                            GroupId=group_id,
                                            IpPermissions=[rule]
                                        )
                                        print(f"Removed unrestricted SSH rule from {group_id}")
                        
                        # Tag the security group as remediated
                        ec2.create_tags(
                            Resources=[group_id],
                            Tags=[
                                {
                                    'Key': 'AutoRemediated',
                                    'Value': 'true'
                                },
                                {
                                    'Key': 'RemediationDate',
                                    'Value': str(context.aws_request_id)
                                }
                            ]
                        )
                        
                        return {'status': 'success', 'message': f'Remediated security group {group_id}'}
                        
                    except Exception as e:
                        return {'status': 'error', 'message': str(e)}
              InputPayload:
                GroupId: '{{ GroupId }}'

  # CloudWatch Event Rule for Config Compliance
  ConfigComplianceEventRule:
    Type: AWS::Events::Rule
    Properties:
      Name: 'ConfigComplianceChanges'
      Description: 'Trigger on Config compliance changes'
      EventPattern:
        source:
          - 'aws.config'
        detail-type:
          - 'Config Rules Compliance Change'
        detail:
          newEvaluationResult:
            complianceType:
              - 'NON_COMPLIANT'
      State: 'ENABLED'
      Targets:
        - Arn: !GetAtt ComplianceNotificationTopic.Arn
          Id: 'ConfigComplianceTarget'

  # SNS Topic for Compliance Notifications
  ComplianceNotificationTopic:
    Type: AWS::SNS::Topic
    Properties:
      TopicName: 'ConfigComplianceAlerts'
      DisplayName: 'Config Compliance Alerts'

Outputs:
  ConfigBucketName:
    Description: 'S3 bucket for AWS Config'
    Value: !Ref ConfigBucket
    Export:
      Name: !Sub '${AWS::StackName}-Config-Bucket'

  ComplianceTopicArn:
    Description: 'SNS topic for compliance alerts'
    Value: !Ref ComplianceNotificationTopic
    Export:
      Name: !Sub '${AWS::StackName}-Compliance-Topic'

### Example 2: Automated threat detection and response with GuardDuty

```python
import boto3
import json
from datetime import datetime
import os

class AutomatedThreatResponse:
    """Automated threat detection and response system"""
    
    def __init__(self):
        self.guardduty = boto3.client('guardduty')
        self.ec2 = boto3.client('ec2')
        self.sns = boto3.client('sns')
        self.ssm = boto3.client('ssm')
        self.lambda_client = boto3.client('lambda')
        
    def lambda_handler(self, event, context):
        """Main Lambda handler for GuardDuty findings"""
        
        try:
            # Parse GuardDuty finding
            detail = event.get('detail', {})
            finding_type = detail.get('type', '')
            severity = detail.get('severity', 0)
            
            print(f"Processing GuardDuty finding: {finding_type} (Severity: {severity})")
            
            # Extract relevant information
            finding_info = self.extract_finding_info(detail)
            
            # Determine response actions based on finding type and severity
            response_actions = self.determine_response_actions(finding_type, severity, finding_info)
            
            # Execute response actions
            results = []
            for action in response_actions:
                result = self.execute_response_action(action, finding_info)
                results.append(result)
            
            # Send notification
            self.send_notification(finding_type, severity, finding_info, results)
            
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'finding_type': finding_type,
                    'severity': severity,
                    'actions_executed': len(results),
                    'results': results
                })
            }
            
        except Exception as e:
            print(f"Error processing GuardDuty finding: {str(e)}")
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)})
            }
    
    def extract_finding_info(self, detail):
        """Extract relevant information from GuardDuty finding"""
        
        finding_info = {
            'id': detail.get('id', ''),
            'type': detail.get('type', ''),
            'severity': detail.get('severity', 0),
            'title': detail.get('title', ''),
            'description': detail.get('description', ''),
            'created_at': detail.get('createdAt', ''),
            'updated_at': detail.get('updatedAt', ''),
            'region': detail.get('region', ''),
            'account_id': detail.get('accountId', ''),
            'resource': {},
            'service': {}
        }
        
        # Extract resource information
        if 'resource' in detail:
            resource = detail['resource']
            finding_info['resource'] = {
                'type': resource.get('resourceType', ''),
                'instance_id': resource.get('instanceDetails', {}).get('instanceId', ''),
                'instance_type': resource.get('instanceDetails', {}).get('instanceType', ''),
                'availability_zone': resource.get('instanceDetails', {}).get('availabilityZone', ''),
                'private_ip': resource.get('instanceDetails', {}).get('networkInterfaces', [{}])[0].get('privateIpAddress', ''),
                'public_ip': resource.get('instanceDetails', {}).get('networkInterfaces', [{}])[0].get('publicIp', '')
            }
        
        # Extract service information
        if 'service' in detail:
            service = detail['service']
            finding_info['service'] = {
                'action': service.get('action', {}),
                'remote_ip': service.get('remoteIpDetails', {}).get('ipAddressV4', ''),
                'remote_country': service.get('remoteIpDetails', {}).get('country', {}).get('countryName', ''),
                'remote_org': service.get('remoteIpDetails', {}).get('organization', {}).get('org', '')
            }
        
        return finding_info
    
    def determine_response_actions(self, finding_type, severity, finding_info):
        """Determine appropriate response actions based on finding characteristics"""
        
        actions = []
        
        # High severity findings require immediate action
        if severity >= 7.0:
            actions.extend([
                'isolate_instance',
                'create_forensic_snapshot',
                'block_malicious_ip',
                'send_high_priority_alert'
            ])
        
        # Medium severity findings require monitoring and investigation
        elif severity >= 4.0:
            actions.extend([
                'enhance_monitoring',
                'collect_evidence',
                'send_medium_priority_alert'
            ])
        
        # Specific actions based on finding type
        if 'Backdoor' in finding_type:
            actions.extend(['isolate_instance', 'scan_for_malware'])
        
        if 'CryptoCurrency' in finding_type:
            actions.extend(['block_mining_traffic', 'check_cpu_usage'])
        
        if 'Trojan' in finding_type:
            actions.extend(['quarantine_files', 'full_system_scan'])
        
        if 'Recon' in finding_type:
            actions.extend(['block_source_ip', 'enhance_network_monitoring'])
        
        # Remove duplicates and return
        return list(set(actions))
    
    def execute_response_action(self, action, finding_info):
        """Execute a specific response action"""
        
        try:
            if action == 'isolate_instance':
                return self.isolate_instance(finding_info['resource']['instance_id'])
            
            elif action == 'create_forensic_snapshot':
                return self.create_forensic_snapshot(finding_info['resource']['instance_id'])
            
            elif action == 'block_malicious_ip':
                return self.block_malicious_ip(finding_info['service']['remote_ip'])
            
            elif action == 'enhance_monitoring':
                return self.enhance_monitoring(finding_info['resource']['instance_id'])
            
            elif action == 'collect_evidence':
                return self.collect_evidence(finding_info)
            
            elif action == 'scan_for_malware':
                return self.scan_for_malware(finding_info['resource']['instance_id'])
            
            elif action == 'quarantine_files':
                return self.quarantine_suspicious_files(finding_info['resource']['instance_id'])
            
            else:
                return {'action': action, 'status': 'not_implemented', 'message': 'Action not implemented'}
        
        except Exception as e:
            return {'action': action, 'status': 'error', 'message': str(e)}
    
    def isolate_instance(self, instance_id):
        """Isolate EC2 instance by changing security group"""
        
        if not instance_id:
            return {'action': 'isolate_instance', 'status': 'skipped', 'message': 'No instance ID provided'}
        
        try:
            # Get current instance details
            response = self.ec2.describe_instances(InstanceIds=[instance_id])
            
            if not response['Reservations']:
                return {'action': 'isolate_instance', 'status': 'error', 'message': 'Instance not found'}
            
            instance = response['Reservations'][0]['Instances'][0]
            
            # Create or get isolation security group
            isolation_sg_id = self.get_or_create_isolation_sg()
            
            # Change instance security group
            self.ec2.modify_instance_attribute(
                InstanceId=instance_id,
                Groups=[isolation_sg_id]
            )
            
            # Tag instance as isolated
            self.ec2.create_tags(
                Resources=[instance_id],
                Tags=[
                    {'Key': 'SecurityStatus', 'Value': 'Isolated'},
                    {'Key': 'IsolationTime', 'Value': datetime.utcnow().isoformat()},
                    {'Key': 'IsolationReason', 'Value': 'GuardDuty Finding'}
                ]
            )
            
            return {
                'action': 'isolate_instance',
                'status': 'success',
                'message': f'Instance {instance_id} isolated successfully'
            }
        
        except Exception as e:
            return {'action': 'isolate_instance', 'status': 'error', 'message': str(e)}
    
    def get_or_create_isolation_sg(self):
        """Get or create isolation security group"""
        
        try:
            # Try to find existing isolation security group
            response = self.ec2.describe_security_groups(
                Filters=[
                    {'Name': 'group-name', 'Values': ['isolation-sg']},
                    {'Name': 'description', 'Values': ['Isolation security group for compromised instances']}
                ]
            )
            
            if response['SecurityGroups']:
                return response['SecurityGroups'][0]['GroupId']
            
            # Create new isolation security group
            vpc_response = self.ec2.describe_vpcs(Filters=[{'Name': 'isDefault', 'Values': ['true']}])
            vpc_id = vpc_response['Vpcs'][0]['VpcId']
            
            sg_response = self.ec2.create_security_group(
                GroupName='isolation-sg',
                Description='Isolation security group for compromised instances',
                VpcId=vpc_id
            )
            
            sg_id = sg_response['GroupId']
            
            # Tag the security group
            self.ec2.create_tags(
                Resources=[sg_id],
                Tags=[
                    {'Key': 'Name', 'Value': 'Isolation-SG'},
                    {'Key': 'Purpose', 'Value': 'Instance-Isolation'}
                ]
            )
            
            return sg_id
        
        except Exception as e:
            print(f"Error creating isolation security group: {e}")
            raise
    
    def create_forensic_snapshot(self, instance_id):
        """Create forensic snapshot of instance volumes"""
        
        if not instance_id:
            return {'action': 'create_forensic_snapshot', 'status': 'skipped', 'message': 'No instance ID provided'}
        
        try:
            # Get instance volumes
            response = self.ec2.describe_instances(InstanceIds=[instance_id])
            instance = response['Reservations'][0]['Instances'][0]
            
            snapshots_created = []
            
            for bdm in instance.get('BlockDeviceMappings', []):
                volume_id = bdm['Ebs']['VolumeId']
                
                # Create snapshot
                snapshot_response = self.ec2.create_snapshot(
                    VolumeId=volume_id,
                    Description=f'Forensic snapshot of {volume_id} from instance {instance_id}'
                )
                
                snapshot_id = snapshot_response['SnapshotId']
                snapshots_created.append(snapshot_id)
                
                # Tag snapshot
                self.ec2.create_tags(
                    Resources=[snapshot_id],
                    Tags=[
                        {'Key': 'Purpose', 'Value': 'Forensic'},
                        {'Key': 'SourceInstance', 'Value': instance_id},
                        {'Key': 'SourceVolume', 'Value': volume_id},
                        {'Key': 'CreatedBy', 'Value': 'AutomatedThreatResponse'},
                        {'Key': 'CreationTime', 'Value': datetime.utcnow().isoformat()}
                    ]
                )
            
            return {
                'action': 'create_forensic_snapshot',
                'status': 'success',
                'message': f'Created {len(snapshots_created)} forensic snapshots',
                'snapshots': snapshots_created
            }
        
        except Exception as e:
            return {'action': 'create_forensic_snapshot', 'status': 'error', 'message': str(e)}
    
    def block_malicious_ip(self, ip_address):
        """Block malicious IP address using security groups"""
        
        if not ip_address:
            return {'action': 'block_malicious_ip', 'status': 'skipped', 'message': 'No IP address provided'}
        
        try:
            # Get or create blocking security group
            blocking_sg_id = self.get_or_create_blocking_sg()
            
            # Add rule to block the IP
            self.ec2.authorize_security_group_ingress(
                GroupId=blocking_sg_id,
                IpPermissions=[
                    {
                        'IpProtocol': '-1',
                        'IpRanges': [
                            {
                                'CidrIp': f'{ip_address}/32',
                                'Description': f'Blocked malicious IP - {datetime.utcnow().isoformat()}'
                            }
                        ]
                    }
                ]
            )
            
            return {
                'action': 'block_malicious_ip',
                'status': 'success',
                'message': f'Blocked IP address {ip_address}'
            }
        
        except self.ec2.exceptions.ClientError as e:
            if 'InvalidPermission.Duplicate' in str(e):
                return {
                    'action': 'block_malicious_ip',
                    'status': 'already_blocked',
                    'message': f'IP address {ip_address} already blocked'
                }
            else:
                return {'action': 'block_malicious_ip', 'status': 'error', 'message': str(e)}
    
    def get_or_create_blocking_sg(self):
        """Get or create security group for blocking malicious IPs"""
        
        try:
            # Try to find existing blocking security group
            response = self.ec2.describe_security_groups(
                Filters=[
                    {'Name': 'group-name', 'Values': ['malicious-ip-blocker']},
                    {'Name': 'description', 'Values': ['Security group for blocking malicious IP addresses']}
                ]
            )
            
            if response['SecurityGroups']:
                return response['SecurityGroups'][0]['GroupId']
            
            # Create new blocking security group
            vpc_response = self.ec2.describe_vpcs(Filters=[{'Name': 'isDefault', 'Values': ['true']}])
            vpc_id = vpc_response['Vpcs'][0]['VpcId']
            
            sg_response = self.ec2.create_security_group(
                GroupName='malicious-ip-blocker',
                Description='Security group for blocking malicious IP addresses',
                VpcId=vpc_id
            )
            
            return sg_response['GroupId']
        
        except Exception as e:
            print(f"Error creating blocking security group: {e}")
            raise
    
    def send_notification(self, finding_type, severity, finding_info, results):
        """Send notification about the automated response"""
        
        message = f"""
Automated Threat Response Executed

Finding Details:
- Type: {finding_type}
- Severity: {severity}
- Instance: {finding_info['resource']['instance_id']}
- Remote IP: {finding_info['service']['remote_ip']}
- Country: {finding_info['service']['remote_country']}

Actions Taken:
"""
        
        for result in results:
            status_emoji = "✅" if result['status'] == 'success' else "❌" if result['status'] == 'error' else "⚠️"
            message += f"{status_emoji} {result['action']}: {result['message']}\n"
        
        message += f"\nTimestamp: {datetime.utcnow().isoformat()}Z"
        
        try:
            topic_arn = os.environ.get('SNS_TOPIC_ARN', 'arn:aws:sns:us-west-2:123456789012:ThreatResponseAlerts')
            
            self.sns.publish(
                TopicArn=topic_arn,
                Subject=f'Automated Threat Response: {finding_type}',
                Message=message
            )
        
        except Exception as e:
            print(f"Error sending notification: {e}")

# Lambda deployment package would include this handler
def lambda_handler(event, context):
    """Lambda entry point"""
    threat_response = AutomatedThreatResponse()
    return threat_response.lambda_handler(event, context)

### Example 3: Automated patch management with Systems Manager

```bash
#!/bin/bash
# Automated patch management system with Systems Manager

set -e

# Configuration
PATCH_GROUP_PROD="Production-Servers"
PATCH_GROUP_DEV="Development-Servers"
MAINTENANCE_WINDOW_PROD="prod-patching-window"
MAINTENANCE_WINDOW_DEV="dev-patching-window"
SNS_TOPIC_ARN="arn:aws:sns:us-west-2:123456789012:PatchingAlerts"

# Function to create patch baseline
create_patch_baseline() {
    local baseline_name=$1
    local operating_system=$2
    local patch_group=$3
    
    echo "Creating patch baseline: $baseline_name"
    
    # Create patch baseline with security-focused rules
    aws ssm create-patch-baseline \
        --name "$baseline_name" \
        --operating-system "$operating_system" \
        --description "Automated security patch baseline for $patch_group" \
        --approval-rules '{
            "PatchRules": [
                {
                    "PatchFilterGroup": {
                        "PatchFilters": [
                            {
                                "Key": "CLASSIFICATION",
                                "Values": ["Security", "CriticalUpdates", "SecurityUpdates"]
                            },
                            {
                                "Key": "SEVERITY",
                                "Values": ["Critical", "Important"]
                            }
                        ]
                    },
                    "ApproveAfterDays": 0,
                    "ComplianceLevel": "CRITICAL",
                    "EnableNonSecurity": false
                },
                {
                    "PatchFilterGroup": {
                        "PatchFilters": [
                            {
                                "Key": "CLASSIFICATION",
                                "Values": ["Security", "Bugfix"]
                            },
                            {
                                "Key": "SEVERITY",
                                "Values": ["Medium", "Low"]
                            }
                        ]
                    },
                    "ApproveAfterDays": 7,
                    "ComplianceLevel": "HIGH",
                    "EnableNonSecurity": false
                }
            ]
        }' \
        --tags Key=Environment,Value="$patch_group" \
               Key=AutomatedPatching,Value=true
    
    # Register patch group
    aws ssm register-patch-baseline-for-patch-group \
        --baseline-id "$baseline_name" \
        --patch-group "$patch_group"
    
    echo "Patch baseline created and registered for $patch_group"
}

# Function to create maintenance window
create_maintenance_window() {
    local window_name=$1
    local schedule=$2
    local duration=$3
    local patch_group=$4
    
    echo "Creating maintenance window: $window_name"
    
    # Create maintenance window
    WINDOW_ID=$(aws ssm create-maintenance-window \
        --name "$window_name" \
        --description "Automated patching maintenance window for $patch_group" \
        --schedule "$schedule" \
        --duration "$duration" \
        --cutoff 1 \
        --allow-unassociated-targets \
        --tags Key=PatchGroup,Value="$patch_group" \
               Key=AutomatedPatching,Value=true \
        --query 'WindowId' \
        --output text)
    
    echo "Created maintenance window: $WINDOW_ID"
    
    # Create maintenance window target
    TARGET_ID=$(aws ssm register-target-with-maintenance-window \
        --window-id "$WINDOW_ID" \
        --resource-type "INSTANCE" \
        --targets Key=tag:PatchGroup,Values="$patch_group" \
        --name "${patch_group}-Targets" \
        --description "Instances in $patch_group for automated patching" \
        --query 'WindowTargetId' \
        --output text)
    
    echo "Created maintenance window target: $TARGET_ID"
    
    # Create patch installation task
    INSTALL_TASK_ID=$(aws ssm register-task-with-maintenance-window \
        --window-id "$WINDOW_ID" \
        --task-type "RUN_COMMAND" \
        --task-arn "AWS-RunPatchBaseline" \
        --targets Key=WindowTargetIds,Values="$TARGET_ID" \
        --service-role-arn "arn:aws:iam::$(aws sts get-caller-identity --query Account --output text):role/MaintenanceWindowRole" \
        --priority 1 \
        --max-concurrency "50%" \
        --max-errors "10%" \
        --name "PatchInstallation-$patch_group" \
        --description "Install approved patches for $patch_group" \
        --task-parameters '{
            "Operation": {
                "Values": ["Install"]
            },
            "RebootOption": {
                "Values": ["RebootIfNeeded"]
            }
        }' \
        --query 'WindowTaskId' \
        --output text)
    
    echo "Created patch installation task: $INSTALL_TASK_ID"
    
    # Create compliance scan task
    SCAN_TASK_ID=$(aws ssm register-task-with-maintenance-window \
        --window-id "$WINDOW_ID" \
        --task-type "RUN_COMMAND" \
        --task-arn "AWS-RunPatchBaseline" \
        --targets Key=WindowTargetIds,Values="$TARGET_ID" \
        --service-role-arn "arn:aws:iam::$(aws sts get-caller-identity --query Account --output text):role/MaintenanceWindowRole" \
        --priority 2 \
        --max-concurrency "100%" \
        --max-errors "5%" \
        --name "ComplianceScan-$patch_group" \
        --description "Scan patch compliance for $patch_group" \
        --task-parameters '{
            "Operation": {
                "Values": ["Scan"]
            }
        }' \
        --query 'WindowTaskId' \
        --output text)
    
    echo "Created compliance scan task: $SCAN_TASK_ID"
    
    return 0
}

# Function to setup automated patch reporting
setup_patch_reporting() {
    echo "Setting up automated patch reporting..."
    
    # Create CloudWatch dashboard for patch compliance
    aws cloudwatch put-dashboard \
        --dashboard-name "PatchCompliance" \
        --dashboard-body '{
            "widgets": [
                {
                    "type": "metric",
                    "x": 0,
                    "y": 0,
                    "width": 12,
                    "height": 6,
                    "properties": {
                        "metrics": [
                            ["AWS/SSM-PatchManager", "ComplianceByPatchGroup", "PatchGroup", "'$PATCH_GROUP_PROD'"],
                            [".", ".", ".", "'$PATCH_GROUP_DEV'"]
                        ],
                        "period": 3600,
                        "stat": "Average",
                        "region": "us-west-2",
                        "title": "Patch Compliance by Group"
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
                            ["AWS/SSM-PatchManager", "NonCompliantInstanceCount", "PatchGroup", "'$PATCH_GROUP_PROD'"],
                            [".", ".", ".", "'$PATCH_GROUP_DEV'"]
                        ],
                        "period": 3600,
                        "stat": "Average",
                        "region": "us-west-2",
                        "title": "Non-Compliant Instances"
                    }
                }
            ]
        }'
    
    # Create CloudWatch alarms for patch compliance
    aws cloudwatch put-metric-alarm \
        --alarm-name "PatchComplianceFailure-Production" \
        --alarm-description "Alert when production patch compliance falls below threshold" \
        --metric-name "ComplianceByPatchGroup" \
        --namespace "AWS/SSM-PatchManager" \
        --statistic "Average" \
        --period 3600 \
        --evaluation-periods 1 \
        --threshold 95 \
        --comparison-operator "LessThanThreshold" \
        --dimensions Name=PatchGroup,Value="$PATCH_GROUP_PROD" \
        --alarm-actions "$SNS_TOPIC_ARN"
    
    aws cloudwatch put-metric-alarm \
        --alarm-name "NonCompliantInstances-Production" \
        --alarm-description "Alert when non-compliant instances exceed threshold" \
        --metric-name "NonCompliantInstanceCount" \
        --namespace "AWS/SSM-PatchManager" \
        --statistic "Average" \
        --period 3600 \
        --evaluation-periods 1 \
        --threshold 5 \
        --comparison-operator "GreaterThanThreshold" \
        --dimensions Name=PatchGroup,Value="$PATCH_GROUP_PROD" \
        --alarm-actions "$SNS_TOPIC_ARN"
    
    echo "Patch reporting and alerting configured"
}

# Function to generate patch compliance report
generate_compliance_report() {
    local output_file=${1:-patch-compliance-report.json}
    
    echo "Generating patch compliance report..."
    
    # Get patch compliance summary
    aws ssm describe-patch-group-state \
        --patch-group "$PATCH_GROUP_PROD" > "${output_file}.prod"
    
    aws ssm describe-patch-group-state \
        --patch-group "$PATCH_GROUP_DEV" > "${output_file}.dev"
    
    # Get detailed compliance information
    aws ssm list-compliance-items \
        --resource-types "ManagedInstance" \
        --filters Key=ComplianceType,Values=Patch,Type=EQUAL \
        --max-items 100 > "${output_file}.details"
    
    # Create summary report
    cat > "$output_file" << EOF
{
    "report_generated": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "production_compliance": $(cat "${output_file}.prod"),
    "development_compliance": $(cat "${output_file}.dev"),
    "detailed_compliance": $(cat "${output_file}.details")
}
EOF
    
    # Clean up temporary files
    rm -f "${output_file}.prod" "${output_file}.dev" "${output_file}.details"
    
    echo "Compliance report generated: $output_file"
}

# Function to setup emergency patching
setup_emergency_patching() {
    echo "Setting up emergency patching capability..."
    
    # Create emergency patch document
    aws ssm create-document \
        --name "EmergencyPatchDeployment" \
        --document-type "Command" \
        --document-format "YAML" \
        --content '
schemaVersion: "2.2"
description: "Emergency patch deployment for critical security vulnerabilities"
parameters:
  PatchGroup:
    type: String
    description: "Patch group to target for emergency patching"
  RebootOption:
    type: String
    description: "Reboot option after patching"
    default: "RebootIfNeeded"
    allowedValues:
      - "RebootIfNeeded"
      - "NoReboot"
mainSteps:
  - action: "aws:runShellScript"
    name: "EmergencyPatch"
    inputs:
      runCommand:
        - "#!/bin/bash"
        - "echo \"Starting emergency patch deployment...\""
        - "yum update -y --security || apt-get update && apt-get upgrade -y"
        - "echo \"Emergency patching completed\""
        - "if [ \"{{ RebootOption }}\" = \"RebootIfNeeded\" ]; then"
        - "  if [ -f /var/run/reboot-required ]; then"
        - "    echo \"Reboot required - scheduling reboot\""
        - "    shutdown -r +1"
        - "  fi"
        - "fi"
' \
        --tags Key=Purpose,Value=EmergencyPatching \
               Key=AutomatedPatching,Value=true
    
    echo "Emergency patching document created"
}

# Main execution
case "${1:-}" in
    "setup")
        echo "Setting up automated patch management..."
        
        # Create patch baselines
        create_patch_baseline "ProductionPatchBaseline" "AMAZON_LINUX_2" "$PATCH_GROUP_PROD"
        create_patch_baseline "DevelopmentPatchBaseline" "AMAZON_LINUX_2" "$PATCH_GROUP_DEV"
        
        # Create maintenance windows
        create_maintenance_window "$MAINTENANCE_WINDOW_PROD" "cron(0 2 ? * SUN *)" 4 "$PATCH_GROUP_PROD"
        create_maintenance_window "$MAINTENANCE_WINDOW_DEV" "cron(0 2 ? * SAT *)" 4 "$PATCH_GROUP_DEV"
        
        # Setup reporting and emergency patching
        setup_patch_reporting
        setup_emergency_patching
        
        echo "Automated patch management setup completed"
        ;;
    "report")
        generate_compliance_report "$2"
        ;;
    "emergency")
        if [ -z "$2" ]; then
            echo "Usage: $0 emergency <patch_group>"
            exit 1
        fi
        
        echo "Executing emergency patching for $2..."
        aws ssm send-command \
            --document-name "EmergencyPatchDeployment" \
            --parameters "PatchGroup=$2,RebootOption=RebootIfNeeded" \
            --targets Key=tag:PatchGroup,Values="$2" \
            --max-concurrency "25%" \
            --max-errors "10%"
        ;;
    *)
        echo "Usage: $0 {setup|report|emergency} [arguments]"
        echo "  setup                    - Set up automated patch management"
        echo "  report [output_file]     - Generate compliance report"
        echo "  emergency <patch_group>  - Execute emergency patching"
        exit 1
        ;;
esac
```

## AWS services to consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Config</h4>
    <p>Enables you to assess, audit, and evaluate the configurations of your AWS resources. Provides automated remediation capabilities for configuration compliance.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon GuardDuty</h4>
    <p>Provides intelligent threat detection for your AWS accounts and workloads. Integrates with automated response systems for immediate threat mitigation.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Systems Manager</h4>
    <p>Gives you visibility and control of your infrastructure on AWS. Provides automation capabilities for patch management, configuration management, and incident response.</p>
  </div>
</div>

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
    <h4>Amazon CloudWatch</h4>
    <p>Monitors your AWS resources and applications in real time. Provides metrics, alarms, and automated actions for security monitoring and response.</p>
  </div>
</div>

## Benefits of automating compute protection

- **Consistent security posture**: Automated controls ensure uniform security configurations across all compute resources
- **Rapid threat response**: Automated systems can respond to threats in seconds rather than minutes or hours
- **Reduced human error**: Automation eliminates mistakes that can occur during manual security operations
- **Scalable protection**: Automated security scales with your infrastructure growth without proportional increases in security staff
- **24/7 monitoring**: Automated systems provide continuous protection without requiring human oversight
- **Improved compliance**: Automated compliance monitoring and remediation helps maintain regulatory adherence
- **Cost efficiency**: Reduces operational costs through automated security operations and faster incident resolution

## Related resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/sec_protect_compute_auto_protection.html">AWS Well-Architected Framework - Automate compute protection</a></li>
    <li><a href="https://docs.aws.amazon.com/config/latest/developerguide/WhatIsConfig.html">AWS Config Developer Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/guardduty/latest/ug/what-is-guardduty.html">Amazon GuardDuty User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/systems-manager/latest/userguide/what-is-systems-manager.html">AWS Systems Manager User Guide</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-automate-incident-response-in-aws-cloud-for-ec2-instances/">How to automate incident response in AWS Cloud for EC2 instances</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-set-up-continuous-compliance-with-aws-config-and-aws-systems-manager/">How to set up continuous compliance with AWS Config and AWS Systems Manager</a></li>
  </ul>
</div>
```
```
