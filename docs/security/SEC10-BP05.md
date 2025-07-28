---
title: "SEC10-BP05: Pre-provision access"
layout: default
parent: "SEC10 - How do you anticipate, respond to, and recover from incidents?"
grand_parent: Security
nav_order: 5
---

# SEC10-BP05: Pre-provision access

## Overview

Verify that incident responders have the correct access pre-provisioned in AWS to reduce the time needed for investigation through to recovery.

**Common anti-patterns:**
- Using the root account for incident response
- Altering existing accounts
- Manipulating IAM permissions directly when providing just-in-time privilege elevation

**Level of risk exposed if this best practice is not established:** Medium

## Implementation Guidance

AWS recommends reducing or eliminating reliance on long-lived credentials wherever possible, in favor of temporary credentials and just-in-time privilege escalation mechanisms. Long-lived credentials are prone to security risk and increase operational overhead.

For most management tasks, as well as incident response tasks, we recommend you implement [identity federation alongside temporary escalation for administrative access](https://docs.aws.amazon.com/whitepapers/latest/organizing-your-aws-environment/organizing-your-aws-environment.html). In this model, a user requests elevation to a higher level of privilege (such as an incident response role) and, provided the user is eligible for elevation, a request is sent to an approver. If the request is approved, the user receives a set of temporary AWS credentials which can be used to complete their tasks. After these credentials expire, the user must submit a new elevation request.

We recommend the use of temporary privilege escalation in the majority of incident response scenarios. The correct way to do this is to use the AWS Security Token Service and session policies to scope access.

### Emergency Break Glass Access

There are scenarios where federated identities are unavailable, such as:
- Outage related to a compromised identity provider (IdP)
- Misconfiguration or human error causing broken federated access management system
- Malicious activity such as a distributed denial of service (DDoS) event or rendering unavailability of the system

In the preceding cases, there should be emergency break glass access configured to allow investigation and timely remediation of incidents.

### Pre-provisioned Dedicated Accounts

We recommend that you use a user, group, or role with appropriate permissions to perform tasks and access AWS resources. [Use the root user only for tasks that require root user credentials](https://docs.aws.amazon.com/accounts/latest/reference/root-user-tasks.html).

To verify that incident responders have the correct level of access to AWS and other relevant systems, we recommend the pre-provisioning of dedicated accounts. The accounts require privileged access, and must be tightly controlled and monitored. The accounts must be built with the fewest privileges required to perform the necessary tasks, and the level of access should be based on the playbooks created as part of the incident management plan.

### Key Implementation Principles

- **Purpose-built and dedicated users and roles**: Use dedicated accounts rather than modifying existing ones
- **Minimize dependencies**: Remove as many dependencies as possible to ensure access under failure scenarios
- **Individual accountability**: Each responder must have their own named account
- **Strong authentication**: Enforce strong password policy and multi-factor authentication (MFA)
- **Principle of least privilege**: Grant only the minimum permissions required
- **Comprehensive monitoring**: Log and alert on all incident response role usage

### Access Management Best Practices

- Create incident response users in a dedicated security account
- Do not manage through existing Federation or SSO solutions for break glass scenarios
- Configure users with no privileges other than the ability to assume incident response roles
- Use [IAM Access Analyzer](https://docs.aws.amazon.com/IAM/latest/UserGuide/what-is-access-analyzer.html) to generate policies based on CloudTrail logs
- Implement separate IAM policies for each playbook scenario
- Use [Systems Manager Session Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager.html) for EC2 access
- Store credentials in [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/) for database and third-party access
## Implementation Examples

### Example 1: Comprehensive Break Glass Access Management System

```python
# break_glass_access_manager.py
import boto3
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import logging
import secrets
import string

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class BreakGlassUser:
    username: str
    user_arn: str
    user_id: str
    created_date: str
    mfa_enabled: bool
    access_keys_disabled: bool
    last_used: Optional[str]
    assigned_responder: str
    emergency_contact: str
    account_status: str

@dataclass
class IncidentResponseRole:
    role_name: str
    role_arn: str
    account_id: str
    playbook_type: str
    permissions_boundary: str
    trust_policy: Dict[str, Any]
    managed_policies: List[str]
    inline_policies: Dict[str, Any]
    session_duration: int
    mfa_required: bool
    created_date: str

@dataclass
class AccessRequest:
    request_id: str
    requester: str
    role_requested: str
    justification: str
    incident_id: str
    requested_at: str
    approved_by: Optional[str]
    approved_at: Optional[str]
    expires_at: str
    status: str
    session_credentials: Optional[Dict[str, str]]

class BreakGlassAccessManager:
    """
    Comprehensive break glass access management for incident response
    """
    
    def __init__(self, security_account_id: str, region: str = 'us-east-1'):
        self.security_account_id = security_account_id
        self.region = region
        self.iam_client = boto3.client('iam', region_name=region)
        self.sts_client = boto3.client('sts', region_name=region)
        self.organizations_client = boto3.client('organizations', region_name=region)
        self.sns_client = boto3.client('sns', region_name=region)
        self.dynamodb = boto3.resource('dynamodb', region_name=region)
        self.secrets_client = boto3.client('secretsmanager', region_name=region)
        
        # DynamoDB tables for access management
        self.users_table = self.dynamodb.Table('break-glass-users')
        self.roles_table = self.dynamodb.Table('incident-response-roles')
        self.requests_table = self.dynamodb.Table('access-requests')
        self.sessions_table = self.dynamodb.Table('active-sessions')
        
        # Initialize role templates
        self.role_templates = self._define_role_templates()
    
    def _define_role_templates(self) -> Dict[str, Dict[str, Any]]:
        """
        Define incident response role templates for different scenarios
        """
        return {
            'security_investigator': {
                'description': 'Security investigation and analysis role',
                'max_session_duration': 14400,  # 4 hours
                'managed_policies': [
                    'arn:aws:iam::aws:policy/SecurityAudit',
                    'arn:aws:iam::aws:policy/ReadOnlyAccess'
                ],
                'inline_policies': {
                    'SecurityInvestigationPolicy': {
                        'Version': '2012-10-17',
                        'Statement': [
                            {
                                'Effect': 'Allow',
                                'Action': [
                                    'guardduty:*',
                                    'detective:*',
                                    'securityhub:*',
                                    'cloudtrail:LookupEvents',
                                    'logs:FilterLogEvents',
                                    'logs:GetLogEvents'
                                ],
                                'Resource': '*'
                            }
                        ]
                    }
                },
                'permissions_boundary': 'arn:aws:iam::aws:policy/PowerUserAccess'
            },
            'incident_responder': {
                'description': 'Full incident response and remediation role',
                'max_session_duration': 28800,  # 8 hours
                'managed_policies': [
                    'arn:aws:iam::aws:policy/PowerUserAccess'
                ],
                'inline_policies': {
                    'IncidentResponsePolicy': {
                        'Version': '2012-10-17',
                        'Statement': [
                            {
                                'Effect': 'Allow',
                                'Action': [
                                    'ec2:*',
                                    'iam:ListUsers',
                                    'iam:ListRoles',
                                    'iam:GetUser',
                                    'iam:GetRole',
                                    'iam:UpdateAccessKey',
                                    'iam:DeleteAccessKey',
                                    'iam:AttachUserPolicy',
                                    'iam:DetachUserPolicy',
                                    'organizations:*'
                                ],
                                'Resource': '*'
                            },
                            {
                                'Effect': 'Deny',
                                'Action': [
                                    'iam:CreateUser',
                                    'iam:DeleteUser',
                                    'iam:CreateRole',
                                    'iam:DeleteRole'
                                ],
                                'Resource': '*'
                            }
                        ]
                    }
                },
                'permissions_boundary': 'arn:aws:iam::aws:policy/PowerUserAccess'
            },
            'forensics_analyst': {
                'description': 'Digital forensics and evidence collection role',
                'max_session_duration': 14400,  # 4 hours
                'managed_policies': [
                    'arn:aws:iam::aws:policy/ReadOnlyAccess'
                ],
                'inline_policies': {
                    'ForensicsPolicy': {
                        'Version': '2012-10-17',
                        'Statement': [
                            {
                                'Effect': 'Allow',
                                'Action': [
                                    'ec2:CreateSnapshot',
                                    'ec2:CopySnapshot',
                                    'ec2:DescribeSnapshots',
                                    'ec2:CreateImage',
                                    'ec2:CopyImage',
                                    's3:GetObject',
                                    's3:PutObject',
                                    's3:ListBucket',
                                    'ssm:SendCommand',
                                    'ssm:GetCommandInvocation'
                                ],
                                'Resource': '*'
                            }
                        ]
                    }
                },
                'permissions_boundary': 'arn:aws:iam::aws:policy/ReadOnlyAccess'
            },
            'break_glass_admin': {
                'description': 'Emergency administrative access for critical incidents',
                'max_session_duration': 3600,  # 1 hour
                'managed_policies': [
                    'arn:aws:iam::aws:policy/AdministratorAccess'
                ],
                'inline_policies': {},
                'permissions_boundary': None
            }
        }
    
    def create_break_glass_user(self, 
                               responder_name: str,
                               responder_email: str,
                               emergency_contact: str) -> Dict[str, Any]:
        """
        Create dedicated break glass user for incident responder
        """
        try:
            username = f"{responder_name.lower().replace(' ', '.')}-BREAK-GLASS"
            
            # Generate secure temporary password
            temp_password = self._generate_secure_password()
            
            # Create IAM user
            user_response = self.iam_client.create_user(
                UserName=username,
                Path='/incident-response/',
                Tags=[
                    {'Key': 'Purpose', 'Value': 'IncidentResponse'},
                    {'Key': 'ResponderName', 'Value': responder_name},
                    {'Key': 'ResponderEmail', 'Value': responder_email},
                    {'Key': 'CreatedBy', 'Value': 'BreakGlassAccessManager'}
                ]
            )
            
            # Create login profile with temporary password
            self.iam_client.create_login_profile(
                UserName=username,
                Password=temp_password,
                PasswordResetRequired=True
            )
            
            # Attach policy to prevent access key creation
            no_access_keys_policy = {
                'Version': '2012-10-17',
                'Statement': [
                    {
                        'Effect': 'Deny',
                        'Action': [
                            'iam:CreateAccessKey',
                            'iam:UpdateAccessKey'
                        ],
                        'Resource': f'arn:aws:iam::{self.security_account_id}:user/incident-response/{username}'
                    }
                ]
            }
            
            self.iam_client.put_user_policy(
                UserName=username,
                PolicyName='DenyAccessKeyCreation',
                PolicyDocument=json.dumps(no_access_keys_policy)
            )
            
            # Store user information
            break_glass_user = BreakGlassUser(
                username=username,
                user_arn=user_response['User']['Arn'],
                user_id=user_response['User']['UserId'],
                created_date=datetime.utcnow().isoformat(),
                mfa_enabled=False,  # Will be enabled during setup
                access_keys_disabled=True,
                last_used=None,
                assigned_responder=responder_name,
                emergency_contact=emergency_contact,
                account_status='active'
            )
            
            self.users_table.put_item(Item=asdict(break_glass_user))
            
            # Store temporary password in Secrets Manager
            self.secrets_client.create_secret(
                Name=f'break-glass-password/{username}',
                Description=f'Temporary password for break glass user {username}',
                SecretString=json.dumps({
                    'username': username,
                    'temporary_password': temp_password,
                    'responder_email': responder_email
                }),
                Tags=[
                    {'Key': 'Purpose', 'Value': 'BreakGlassAccess'},
                    {'Key': 'Username', 'Value': username}
                ]
            )
            
            logger.info(f"Created break glass user: {username}")
            
            return {
                'status': 'success',
                'username': username,
                'user_arn': user_response['User']['Arn'],
                'temporary_password_secret': f'break-glass-password/{username}',
                'next_steps': [
                    'User must log in and change password',
                    'User must enable MFA',
                    'Verify user can assume incident response roles'
                ]
            }
            
        except Exception as e:
            logger.error(f"Error creating break glass user: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def create_incident_response_role(self, 
                                    target_account_id: str,
                                    role_type: str,
                                    playbook_name: str) -> Dict[str, Any]:
        """
        Create incident response role in target account
        """
        try:
            if role_type not in self.role_templates:
                return {
                    'status': 'error',
                    'message': f'Unknown role type: {role_type}'
                }
            
            role_template = self.role_templates[role_type]
            role_name = f'BREAK-GLASS-{role_type.upper()}-{playbook_name.upper()}'
            
            # Create trust policy requiring MFA
            trust_policy = {
                'Version': '2012-10-17',
                'Statement': [
                    {
                        'Effect': 'Allow',
                        'Principal': {
                            'AWS': f'arn:aws:iam::{self.security_account_id}:root'
                        },
                        'Action': 'sts:AssumeRole',
                        'Condition': {
                            'Bool': {
                                'aws:MultiFactorAuthPresent': 'true'
                            },
                            'NumericLessThan': {
                                'aws:MultiFactorAuthAge': '3600'  # MFA within last hour
                            },
                            'StringLike': {
                                'aws:userid': f'*:*-BREAK-GLASS'
                            }
                        }
                    }
                ]
            }
            
            # Assume role in target account to create the role
            target_credentials = self._assume_role_in_target_account(target_account_id)
            target_iam_client = boto3.client(
                'iam',
                aws_access_key_id=target_credentials['AccessKeyId'],
                aws_secret_access_key=target_credentials['SecretAccessKey'],
                aws_session_token=target_credentials['SessionToken']
            )
            
            # Create the role
            role_response = target_iam_client.create_role(
                RoleName=role_name,
                AssumeRolePolicyDocument=json.dumps(trust_policy),
                Description=role_template['description'],
                MaxSessionDuration=role_template['max_session_duration'],
                PermissionsBoundary=role_template.get('permissions_boundary'),
                Tags=[
                    {'Key': 'Purpose', 'Value': 'IncidentResponse'},
                    {'Key': 'RoleType', 'Value': role_type},
                    {'Key': 'PlaybookName', 'Value': playbook_name},
                    {'Key': 'CreatedBy', 'Value': 'BreakGlassAccessManager'}
                ]
            )
            
            # Attach managed policies
            for policy_arn in role_template['managed_policies']:
                target_iam_client.attach_role_policy(
                    RoleName=role_name,
                    PolicyArn=policy_arn
                )
            
            # Create and attach inline policies
            for policy_name, policy_document in role_template['inline_policies'].items():
                target_iam_client.put_role_policy(
                    RoleName=role_name,
                    PolicyName=policy_name,
                    PolicyDocument=json.dumps(policy_document)
                )
            
            # Store role information
            incident_role = IncidentResponseRole(
                role_name=role_name,
                role_arn=role_response['Role']['Arn'],
                account_id=target_account_id,
                playbook_type=playbook_name,
                permissions_boundary=role_template.get('permissions_boundary', ''),
                trust_policy=trust_policy,
                managed_policies=role_template['managed_policies'],
                inline_policies=role_template['inline_policies'],
                session_duration=role_template['max_session_duration'],
                mfa_required=True,
                created_date=datetime.utcnow().isoformat()
            )
            
            self.roles_table.put_item(Item=asdict(incident_role))
            
            logger.info(f"Created incident response role: {role_name} in account {target_account_id}")
            
            return {
                'status': 'success',
                'role_name': role_name,
                'role_arn': role_response['Role']['Arn'],
                'account_id': target_account_id,
                'role_type': role_type
            }
            
        except Exception as e:
            logger.error(f"Error creating incident response role: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def request_emergency_access(self, 
                               requester_username: str,
                               role_arn: str,
                               incident_id: str,
                               justification: str,
                               duration_hours: int = 4) -> Dict[str, Any]:
        """
        Request emergency access to incident response role
        """
        try:
            request_id = f"ACCESS_{incident_id}_{int(datetime.utcnow().timestamp())}"
            
            # Validate requester is a break glass user
            try:
                user_response = self.users_table.get_item(Key={'username': requester_username})
                if 'Item' not in user_response:
                    return {
                        'status': 'error',
                        'message': f'User {requester_username} is not a registered break glass user'
                    }
            except Exception:
                return {
                    'status': 'error',
                    'message': f'Unable to validate user {requester_username}'
                }
            
            # Create access request
            access_request = AccessRequest(
                request_id=request_id,
                requester=requester_username,
                role_requested=role_arn,
                justification=justification,
                incident_id=incident_id,
                requested_at=datetime.utcnow().isoformat(),
                approved_by=None,
                approved_at=None,
                expires_at=(datetime.utcnow() + timedelta(hours=duration_hours)).isoformat(),
                status='pending_approval',
                session_credentials=None
            )
            
            self.requests_table.put_item(Item=asdict(access_request))
            
            # Send notification for approval
            self._send_approval_notification(access_request)
            
            logger.info(f"Created access request: {request_id}")
            
            return {
                'status': 'success',
                'request_id': request_id,
                'status': 'pending_approval',
                'message': 'Access request submitted for approval'
            }
            
        except Exception as e:
            logger.error(f"Error requesting emergency access: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def approve_access_request(self, 
                             request_id: str,
                             approver: str,
                             approval_decision: str) -> Dict[str, Any]:
        """
        Approve or deny access request
        """
        try:
            # Retrieve access request
            request_response = self.requests_table.get_item(Key={'request_id': request_id})
            if 'Item' not in request_response:
                return {
                    'status': 'error',
                    'message': f'Access request {request_id} not found'
                }
            
            request_item = request_response['Item']
            
            if approval_decision.lower() == 'approved':
                # Generate temporary credentials
                credentials = self._generate_temporary_credentials(
                    request_item['role_requested'],
                    request_item['requester']
                )
                
                # Update request with approval and credentials
                self.requests_table.update_item(
                    Key={'request_id': request_id},
                    UpdateExpression='SET approved_by = :approver, approved_at = :approved_at, #status = :status, session_credentials = :credentials',
                    ExpressionAttributeNames={'#status': 'status'},
                    ExpressionAttributeValues={
                        ':approver': approver,
                        ':approved_at': datetime.utcnow().isoformat(),
                        ':status': 'approved',
                        ':credentials': credentials
                    }
                )
                
                # Log the approval
                self._log_access_approval(request_id, approver, 'approved')
                
                return {
                    'status': 'success',
                    'request_id': request_id,
                    'decision': 'approved',
                    'credentials': credentials
                }
            else:
                # Update request with denial
                self.requests_table.update_item(
                    Key={'request_id': request_id},
                    UpdateExpression='SET approved_by = :approver, approved_at = :approved_at, #status = :status',
                    ExpressionAttributeNames={'#status': 'status'},
                    ExpressionAttributeValues={
                        ':approver': approver,
                        ':approved_at': datetime.utcnow().isoformat(),
                        ':status': 'denied'
                    }
                )
                
                # Log the denial
                self._log_access_approval(request_id, approver, 'denied')
                
                return {
                    'status': 'success',
                    'request_id': request_id,
                    'decision': 'denied'
                }
                
        except Exception as e:
            logger.error(f"Error approving access request: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def setup_cloudtrail_monitoring(self) -> Dict[str, Any]:
        """
        Set up CloudTrail monitoring for break glass access usage
        """
        try:
            # Create CloudWatch metric filter for AssumeRole events
            metric_filter_name = 'BreakGlassRoleUsage'
            log_group_name = 'CloudTrail/BreakGlassAccess'
            
            # Metric filter pattern for break glass role assumptions
            filter_pattern = '''
            {
                $.eventName = "AssumeRole" &&
                $.requestParameters.roleArn = "*BREAK-GLASS*" &&
                $.userIdentity.invokedBy NOT EXISTS &&
                $.eventType != "AwsServiceEvent"
            }
            '''
            
            # Create CloudWatch alarm for break glass usage
            alarm_name = 'BreakGlassAccessUsed'
            
            monitoring_setup = {
                'metric_filter': {
                    'name': metric_filter_name,
                    'log_group': log_group_name,
                    'pattern': filter_pattern.strip()
                },
                'alarm': {
                    'name': alarm_name,
                    'description': 'Alert when break glass access is used',
                    'threshold': 1,
                    'comparison': 'GreaterThanOrEqualToThreshold'
                }
            }
            
            return {
                'status': 'success',
                'monitoring_setup': monitoring_setup,
                'message': 'CloudTrail monitoring configured for break glass access'
            }
            
        except Exception as e:
            logger.error(f"Error setting up CloudTrail monitoring: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _generate_secure_password(self, length: int = 16) -> str:
        """Generate secure temporary password"""
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        return password
    
    def _assume_role_in_target_account(self, target_account_id: str) -> Dict[str, str]:
        """Assume role in target account for role creation"""
        # Simplified implementation - in practice, you would assume a cross-account role
        # that has permissions to create IAM roles in the target account
        return {
            'AccessKeyId': 'SIMULATED_ACCESS_KEY',
            'SecretAccessKey': 'SIMULATED_SECRET_KEY',
            'SessionToken': 'SIMULATED_SESSION_TOKEN'
        }
    
    def _generate_temporary_credentials(self, role_arn: str, requester: str) -> Dict[str, str]:
        """Generate temporary credentials for approved access"""
        # Simplified implementation - in practice, you would use STS AssumeRole
        return {
            'AccessKeyId': f'ASIA{secrets.token_hex(8).upper()}',
            'SecretAccessKey': secrets.token_hex(20),
            'SessionToken': secrets.token_hex(100),
            'Expiration': (datetime.utcnow() + timedelta(hours=4)).isoformat()
        }
    
    def _send_approval_notification(self, access_request: AccessRequest):
        """Send notification for access request approval"""
        try:
            message = f"""
            Emergency Access Request Requires Approval
            
            Request ID: {access_request.request_id}
            Requester: {access_request.requester}
            Role Requested: {access_request.role_requested}
            Incident ID: {access_request.incident_id}
            Justification: {access_request.justification}
            Requested At: {access_request.requested_at}
            
            Please review and approve/deny this request immediately.
            """
            
            # Send SNS notification (simplified)
            logger.info(f"Approval notification sent for request {access_request.request_id}")
            
        except Exception as e:
            logger.error(f"Error sending approval notification: {str(e)}")
    
    def _log_access_approval(self, request_id: str, approver: str, decision: str):
        """Log access approval decision"""
        try:
            log_entry = {
                'timestamp': datetime.utcnow().isoformat(),
                'request_id': request_id,
                'approver': approver,
                'decision': decision,
                'event_type': 'access_approval'
            }
            
            logger.info(f"Access approval logged: {json.dumps(log_entry)}")
            
        except Exception as e:
            logger.error(f"Error logging access approval: {str(e)}")

# Example usage
if __name__ == "__main__":
    # Initialize break glass access manager
    access_manager = BreakGlassAccessManager(security_account_id="123456789012")
    
    # Create break glass user
    user_result = access_manager.create_break_glass_user(
        responder_name="John Doe",
        responder_email="john.doe@company.com",
        emergency_contact="jane.smith@company.com"
    )
    print(f"Break glass user creation: {json.dumps(user_result, indent=2)}")
    
    # Create incident response role
    role_result = access_manager.create_incident_response_role(
        target_account_id="987654321098",
        role_type="security_investigator",
        playbook_name="credential_compromise"
    )
    print(f"Incident response role creation: {json.dumps(role_result, indent=2)}")
    
    # Request emergency access
    access_result = access_manager.request_emergency_access(
        requester_username="john.doe-BREAK-GLASS",
        role_arn="arn:aws:iam::987654321098:role/BREAK-GLASS-SECURITY_INVESTIGATOR-CREDENTIAL_COMPROMISE",
        incident_id="INC-2024-001",
        justification="Investigating suspected credential compromise in production account",
        duration_hours=4
    )
    print(f"Emergency access request: {json.dumps(access_result, indent=2)}")
```
### Example 2: Just-in-Time Access with Session Policies

```python
# jit_access_manager.py
import boto3
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class JustInTimeAccessManager:
    """
    Just-in-time access management with session policies for incident response
    """
    
    def __init__(self, region: str = 'us-east-1'):
        self.region = region
        self.sts_client = boto3.client('sts', region_name=region)
        self.iam_client = boto3.client('iam', region_name=region)
        self.dynamodb = boto3.resource('dynamodb', region_name=region)
        
        # DynamoDB table for session tracking
        self.sessions_table = self.dynamodb.Table('jit-access-sessions')
        
        # Session policy templates
        self.session_policies = self._define_session_policies()
    
    def _define_session_policies(self) -> Dict[str, Dict[str, Any]]:
        """
        Define session policies for different incident response scenarios
        """
        return {
            'read_only_investigation': {
                'description': 'Read-only access for initial incident investigation',
                'max_duration': 14400,  # 4 hours
                'policy': {
                    'Version': '2012-10-17',
                    'Statement': [
                        {
                            'Effect': 'Allow',
                            'Action': [
                                'cloudtrail:LookupEvents',
                                'logs:FilterLogEvents',
                                'logs:GetLogEvents',
                                'guardduty:GetFindings',
                                'guardduty:ListFindings',
                                'detective:*',
                                'securityhub:GetFindings',
                                'config:GetComplianceDetailsByConfigRule',
                                'config:GetResourceConfigHistory'
                            ],
                            'Resource': '*'
                        },
                        {
                            'Effect': 'Allow',
                            'Action': [
                                'ec2:Describe*',
                                'iam:Get*',
                                'iam:List*',
                                's3:GetBucketLocation',
                                's3:GetBucketLogging',
                                's3:GetBucketPolicy',
                                's3:ListBucket'
                            ],
                            'Resource': '*'
                        }
                    ]
                }
            },
            'containment_actions': {
                'description': 'Limited write access for incident containment',
                'max_duration': 7200,  # 2 hours
                'policy': {
                    'Version': '2012-10-17',
                    'Statement': [
                        {
                            'Effect': 'Allow',
                            'Action': [
                                'ec2:StopInstances',
                                'ec2:TerminateInstances',
                                'ec2:ModifyInstanceAttribute',
                                'ec2:AuthorizeSecurityGroupIngress',
                                'ec2:RevokeSecurityGroupIngress',
                                'ec2:AuthorizeSecurityGroupEgress',
                                'ec2:RevokeSecurityGroupEgress',
                                'iam:UpdateAccessKey',
                                'iam:DeleteAccessKey',
                                'iam:AttachUserPolicy',
                                'iam:DetachUserPolicy'
                            ],
                            'Resource': '*',
                            'Condition': {
                                'StringEquals': {
                                    'aws:RequestedRegion': ['us-east-1', 'us-west-2']
                                }
                            }
                        },
                        {
                            'Effect': 'Deny',
                            'Action': [
                                'iam:CreateUser',
                                'iam:DeleteUser',
                                'iam:CreateRole',
                                'iam:DeleteRole',
                                'organizations:*'
                            ],
                            'Resource': '*'
                        }
                    ]
                }
            },
            'forensics_collection': {
                'description': 'Access for forensic evidence collection',
                'max_duration': 10800,  # 3 hours
                'policy': {
                    'Version': '2012-10-17',
                    'Statement': [
                        {
                            'Effect': 'Allow',
                            'Action': [
                                'ec2:CreateSnapshot',
                                'ec2:CopySnapshot',
                                'ec2:DescribeSnapshots',
                                'ec2:CreateImage',
                                'ec2:CopyImage',
                                'ec2:DescribeImages',
                                'ssm:SendCommand',
                                'ssm:GetCommandInvocation',
                                'ssm:DescribeInstanceInformation'
                            ],
                            'Resource': '*'
                        },
                        {
                            'Effect': 'Allow',
                            'Action': [
                                's3:GetObject',
                                's3:PutObject',
                                's3:ListBucket'
                            ],
                            'Resource': [
                                'arn:aws:s3:::forensic-evidence-*',
                                'arn:aws:s3:::forensic-evidence-*/*'
                            ]
                        }
                    ]
                }
            },
            'emergency_admin': {
                'description': 'Emergency administrative access for critical incidents',
                'max_duration': 3600,  # 1 hour
                'policy': {
                    'Version': '2012-10-17',
                    'Statement': [
                        {
                            'Effect': 'Allow',
                            'Action': '*',
                            'Resource': '*'
                        },
                        {
                            'Effect': 'Deny',
                            'Action': [
                                'organizations:CloseAccount',
                                'account:CloseAccount',
                                'iam:DeleteRole',
                                'iam:DeleteUser'
                            ],
                            'Resource': '*'
                        }
                    ]
                }
            }
        }
    
    def request_jit_access(self, 
                          base_role_arn: str,
                          session_policy_type: str,
                          incident_id: str,
                          justification: str,
                          requester_identity: str) -> Dict[str, Any]:
        """
        Request just-in-time access with session policy
        """
        try:
            if session_policy_type not in self.session_policies:
                return {
                    'status': 'error',
                    'message': f'Unknown session policy type: {session_policy_type}'
                }
            
            session_policy = self.session_policies[session_policy_type]
            session_name = f"IncidentResponse-{incident_id}-{int(datetime.utcnow().timestamp())}"
            
            # Assume role with session policy
            assume_role_response = self.sts_client.assume_role(
                RoleArn=base_role_arn,
                RoleSessionName=session_name,
                Policy=json.dumps(session_policy['policy']),
                DurationSeconds=session_policy['max_duration'],
                Tags=[
                    {'Key': 'IncidentId', 'Value': incident_id},
                    {'Key': 'SessionPolicyType', 'Value': session_policy_type},
                    {'Key': 'Requester', 'Value': requester_identity}
                ]
            )
            
            credentials = assume_role_response['Credentials']
            
            # Record session
            session_record = {
                'session_id': session_name,
                'base_role_arn': base_role_arn,
                'session_policy_type': session_policy_type,
                'incident_id': incident_id,
                'justification': justification,
                'requester_identity': requester_identity,
                'assumed_at': datetime.utcnow().isoformat(),
                'expires_at': credentials['Expiration'].isoformat(),
                'access_key_id': credentials['AccessKeyId'],
                'session_token_hash': self._hash_session_token(credentials['SessionToken']),
                'status': 'active'
            }
            
            self.sessions_table.put_item(Item=session_record)
            
            logger.info(f"JIT access granted: {session_name}")
            
            return {
                'status': 'success',
                'session_id': session_name,
                'credentials': {
                    'AccessKeyId': credentials['AccessKeyId'],
                    'SecretAccessKey': credentials['SecretAccessKey'],
                    'SessionToken': credentials['SessionToken'],
                    'Expiration': credentials['Expiration'].isoformat()
                },
                'session_policy_type': session_policy_type,
                'expires_at': credentials['Expiration'].isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error requesting JIT access: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def create_scoped_session_policy(self, 
                                   base_permissions: List[str],
                                   resource_constraints: Dict[str, List[str]],
                                   condition_constraints: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create custom scoped session policy for specific incident requirements
        """
        try:
            # Build session policy with constraints
            session_policy = {
                'Version': '2012-10-17',
                'Statement': [
                    {
                        'Effect': 'Allow',
                        'Action': base_permissions,
                        'Resource': resource_constraints.get('allowed_resources', ['*'])
                    }
                ]
            }
            
            # Add conditions if specified
            if condition_constraints:
                session_policy['Statement'][0]['Condition'] = condition_constraints
            
            # Add explicit denies for high-risk actions
            session_policy['Statement'].append({
                'Effect': 'Deny',
                'Action': [
                    'iam:CreateUser',
                    'iam:DeleteUser',
                    'iam:CreateRole',
                    'iam:DeleteRole',
                    'organizations:CloseAccount',
                    'account:CloseAccount'
                ],
                'Resource': '*'
            })
            
            return {
                'status': 'success',
                'session_policy': session_policy,
                'policy_size': len(json.dumps(session_policy))
            }
            
        except Exception as e:
            logger.error(f"Error creating scoped session policy: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def revoke_jit_session(self, session_id: str, revoked_by: str) -> Dict[str, Any]:
        """
        Revoke active JIT session (mark as revoked for tracking)
        """
        try:
            # Update session record
            self.sessions_table.update_item(
                Key={'session_id': session_id},
                UpdateExpression='SET #status = :status, revoked_by = :revoked_by, revoked_at = :revoked_at',
                ExpressionAttributeNames={'#status': 'status'},
                ExpressionAttributeValues={
                    ':status': 'revoked',
                    ':revoked_by': revoked_by,
                    ':revoked_at': datetime.utcnow().isoformat()
                }
            )
            
            logger.info(f"JIT session revoked: {session_id} by {revoked_by}")
            
            return {
                'status': 'success',
                'session_id': session_id,
                'revoked_by': revoked_by,
                'message': 'Session marked as revoked'
            }
            
        except Exception as e:
            logger.error(f"Error revoking JIT session: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def audit_jit_sessions(self, 
                          start_date: str,
                          end_date: str,
                          incident_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Audit JIT access sessions for compliance and security review
        """
        try:
            # Query sessions within date range
            scan_kwargs = {
                'FilterExpression': 'assumed_at BETWEEN :start_date AND :end_date',
                'ExpressionAttributeValues': {
                    ':start_date': start_date,
                    ':end_date': end_date
                }
            }
            
            if incident_id:
                scan_kwargs['FilterExpression'] += ' AND incident_id = :incident_id'
                scan_kwargs['ExpressionAttributeValues'][':incident_id'] = incident_id
            
            response = self.sessions_table.scan(**scan_kwargs)
            sessions = response['Items']
            
            # Analyze session patterns
            audit_summary = {
                'total_sessions': len(sessions),
                'active_sessions': len([s for s in sessions if s['status'] == 'active']),
                'revoked_sessions': len([s for s in sessions if s['status'] == 'revoked']),
                'expired_sessions': len([s for s in sessions if datetime.fromisoformat(s['expires_at']) < datetime.utcnow()]),
                'session_types': {},
                'requesters': {},
                'incidents': {}
            }
            
            for session in sessions:
                # Count by session type
                session_type = session['session_policy_type']
                audit_summary['session_types'][session_type] = audit_summary['session_types'].get(session_type, 0) + 1
                
                # Count by requester
                requester = session['requester_identity']
                audit_summary['requesters'][requester] = audit_summary['requesters'].get(requester, 0) + 1
                
                # Count by incident
                incident = session['incident_id']
                audit_summary['incidents'][incident] = audit_summary['incidents'].get(incident, 0) + 1
            
            return {
                'status': 'success',
                'audit_period': {'start': start_date, 'end': end_date},
                'audit_summary': audit_summary,
                'detailed_sessions': sessions
            }
            
        except Exception as e:
            logger.error(f"Error auditing JIT sessions: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _hash_session_token(self, session_token: str) -> str:
        """Create hash of session token for tracking without storing sensitive data"""
        import hashlib
        return hashlib.sha256(session_token.encode()).hexdigest()[:16]

# Example usage and testing
def demonstrate_jit_access():
    """
    Demonstrate just-in-time access patterns for incident response
    """
    jit_manager = JustInTimeAccessManager()
    
    # Example 1: Request read-only investigation access
    investigation_access = jit_manager.request_jit_access(
        base_role_arn='arn:aws:iam::123456789012:role/IncidentResponseBaseRole',
        session_policy_type='read_only_investigation',
        incident_id='INC-2024-001',
        justification='Initial investigation of suspicious CloudTrail events',
        requester_identity='security.analyst@company.com'
    )
    print(f"Investigation access: {json.dumps(investigation_access, indent=2, default=str)}")
    
    # Example 2: Request containment actions access
    containment_access = jit_manager.request_jit_access(
        base_role_arn='arn:aws:iam::123456789012:role/IncidentResponseBaseRole',
        session_policy_type='containment_actions',
        incident_id='INC-2024-001',
        justification='Need to isolate compromised EC2 instances',
        requester_identity='incident.responder@company.com'
    )
    print(f"Containment access: {json.dumps(containment_access, indent=2, default=str)}")
    
    # Example 3: Create custom scoped policy
    custom_policy = jit_manager.create_scoped_session_policy(
        base_permissions=[
            'ec2:DescribeInstances',
            'ec2:StopInstances',
            'logs:FilterLogEvents'
        ],
        resource_constraints={
            'allowed_resources': [
                'arn:aws:ec2:us-east-1:123456789012:instance/i-1234567890abcdef0',
                'arn:aws:logs:us-east-1:123456789012:log-group:/aws/ec2/*'
            ]
        },
        condition_constraints={
            'StringEquals': {
                'aws:RequestedRegion': 'us-east-1'
            },
            'DateLessThan': {
                'aws:CurrentTime': (datetime.utcnow() + timedelta(hours=2)).strftime('%Y-%m-%dT%H:%M:%SZ')
            }
        }
    )
    print(f"Custom policy: {json.dumps(custom_policy, indent=2, default=str)}")
    
    # Example 4: Audit sessions
    audit_results = jit_manager.audit_jit_sessions(
        start_date='2024-01-01T00:00:00Z',
        end_date='2024-12-31T23:59:59Z',
        incident_id='INC-2024-001'
    )
    print(f"Audit results: {json.dumps(audit_results, indent=2, default=str)}")

if __name__ == "__main__":
    demonstrate_jit_access()
```
## Resources

### Related Documents

- [Managing temporary elevated access to your AWS environment](https://docs.aws.amazon.com/whitepapers/latest/organizing-your-aws-environment/managing-temporary-elevated-access-to-your-aws-environment.html)
- [AWS Security Incident Response Guide](https://docs.aws.amazon.com/whitepapers/latest/aws-security-incident-response-guide/aws-security-incident-response-guide.html)
- [AWS Elastic Disaster Recovery](https://aws.amazon.com/disaster-recovery/)
- [AWS Systems Manager Incident Manager](https://docs.aws.amazon.com/incident-manager/latest/userguide/what-is-incident-manager.html)
- [Setting an account password policy for IAM users](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_passwords_account-policy.html)
- [Using multi-factor authentication (MFA) in AWS](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_mfa.html)
- [Configuring Cross-Account Access with MFA](https://aws.amazon.com/blogs/security/how-to-use-trust-policies-with-iam-roles/)
- [Using IAM Access Analyzer to generate IAM policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-policy-generation.html)
- [Best Practices for AWS Organizations Service Control Policies in a Multi-Account Environment](https://aws.amazon.com/blogs/security/best-practices-for-aws-organizations-service-control-policies-in-a-multi-account-environment/)
- [How to Receive Notifications When Your AWS Account's Root Access Keys Are Used](https://aws.amazon.com/blogs/security/how-to-receive-notifications-when-your-aws-accounts-root-access-keys-are-used/)
- [Create fine-grained session permissions using IAM managed policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html)
- [Break glass access](https://docs.aws.amazon.com/whitepapers/latest/organizing-your-aws-environment/break-glass-access.html)

### Related Videos

- [Automating Incident Response and Forensics in AWS](https://www.youtube.com/watch?v=f_EcwmmXkXk)
- [DIY guide to runbooks, incident reports, and incident response](https://www.youtube.com/watch?v=E1NaYN_fJUw)
- [Prepare for and respond to security incidents in your AWS environment](https://www.youtube.com/watch?v=8uiO0Z5meCs)

### AWS Services for Access Management

- [AWS Identity and Access Management (IAM)](https://aws.amazon.com/iam/) - For user and role management
- [AWS Security Token Service (STS)](https://docs.aws.amazon.com/STS/latest/APIReference/welcome.html) - For temporary credentials
- [AWS Systems Manager Session Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager.html) - For secure instance access
- [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/) - For credential storage
- [AWS CloudTrail](https://aws.amazon.com/cloudtrail/) - For access logging and monitoring
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/) - For alerting and monitoring
- [AWS Organizations](https://aws.amazon.com/organizations/) - For multi-account management
- [AWS IAM Access Analyzer](https://docs.aws.amazon.com/IAM/latest/UserGuide/what-is-access-analyzer.html) - For policy analysis and generation

### Implementation Best Practices

**Break Glass Account Setup:**
- Create dedicated security account for break glass users
- Use descriptive naming convention (e.g., `username-BREAK-GLASS`)
- Enforce strong password policies and MFA requirements
- Disable access key creation for console-only users
- Implement regular account review and cleanup processes

**Role Design Principles:**
- Use least privilege principle for all roles
- Implement permissions boundaries to limit maximum permissions
- Require MFA for all role assumptions
- Set appropriate session duration limits
- Use separate roles for different incident types

**Session Policy Implementation:**
- Scope permissions to specific resources when possible
- Include time-based conditions for session validity
- Implement explicit deny statements for high-risk actions
- Use condition keys to restrict access by region or IP
- Regular review and update of session policies

**Monitoring and Auditing:**
- Enable CloudTrail logging for all accounts
- Set up real-time alerts for break glass access usage
- Implement automated session tracking and reporting
- Regular audit of access patterns and usage
- Maintain detailed logs for compliance requirements

### Common Access Patterns

**Investigation Phase:**
- Read-only access to logs and security services
- CloudTrail event lookup and analysis
- GuardDuty and Security Hub finding review
- Resource configuration and status checking

**Containment Phase:**
- Instance stop/terminate permissions
- Security group modification rights
- Access key disable/delete capabilities
- Network isolation and blocking actions

**Recovery Phase:**
- Resource restoration and configuration
- Service restart and validation
- Backup and snapshot operations
- System hardening and patching

**Forensics Phase:**
- Snapshot and image creation
- Memory dump collection
- Log export and preservation
- Evidence chain of custody maintenance

### Compliance Considerations

- **SOC 2**: Implement proper access controls and monitoring
- **PCI DSS**: Ensure cardholder data environment protection
- **HIPAA**: Maintain audit trails for healthcare data access
- **GDPR**: Document data access for privacy compliance
- **SOX**: Implement segregation of duties for financial systems

### Emergency Scenarios

**Identity Provider Outage:**
- Pre-positioned break glass accounts in security account
- Direct IAM user access with MFA requirements
- Emergency contact procedures and approval workflows
- Documented recovery procedures and role assumptions

**Account Lockout:**
- Root user access procedures and safeguards
- Cross-account emergency access roles
- Out-of-band communication channels
- Escalation procedures for critical incidents

**Compromised Federation:**
- Immediate break glass activation procedures
- Isolation of compromised identity systems
- Alternative authentication mechanisms
- Incident response team activation protocols

### Testing and Validation

- **Regular Access Testing**: Quarterly validation of break glass procedures
- **Tabletop Exercises**: Scenario-based access requirement testing
- **Automated Validation**: Continuous testing of role assumptions
- **Documentation Updates**: Regular review and update of procedures
- **Training Programs**: Regular training for incident responders
