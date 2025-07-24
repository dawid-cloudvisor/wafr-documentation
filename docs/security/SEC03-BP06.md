---
title: SEC03-BP06 - Manage access based on lifecycle
layout: default
parent: SEC03 - How do you manage permissions for people and machines?
grand_parent: Security
nav_order: 6
---

<div class="pillar-header">
  <h1>SEC03-BP06: Manage access based on lifecycle</h1>
  <p>Integrate access controls with operator and application lifecycle and your centralized federation provider. For example, remove a user's access when they leave the organization or change roles.</p>
</div>

## Implementation guidance

Managing access based on lifecycle ensures that permissions are granted, modified, and revoked in alignment with changes in user roles, employment status, and application requirements. This approach helps maintain security by ensuring that access rights remain appropriate throughout the entire lifecycle of identities and resources.

### Key steps for implementing this best practice:

1. **Define lifecycle stages**:
   - Map out user lifecycle stages (onboarding, role changes, offboarding)
   - Identify application and service lifecycle phases
   - Define access requirements for each lifecycle stage
   - Document approval processes for lifecycle transitions
   - Establish timelines for access provisioning and deprovisioning

2. **Implement automated provisioning**:
   - Integrate with HR systems for user lifecycle events
   - Automate account creation and initial access provisioning
   - Use identity providers for centralized user management
   - Implement just-in-time (JIT) access provisioning
   - Create templates for common access patterns

3. **Establish role-based access management**:
   - Define roles based on job functions and responsibilities
   - Map users to roles based on their current position
   - Implement automatic role assignment based on attributes
   - Create approval workflows for role changes
   - Document role definitions and associated permissions

4. **Implement automated deprovisioning**:
   - Automate access removal when users leave the organization
   - Implement immediate access suspension for terminated employees
   - Create processes for transferring access during role changes
   - Establish retention policies for user accounts and data
   - Implement automated cleanup of unused accounts

5. **Monitor and audit lifecycle events**:
   - Track all access provisioning and deprovisioning events
   - Monitor for orphaned accounts and unused access
   - Implement regular access reviews and certifications
   - Generate reports on lifecycle management effectiveness
   - Set up alerts for unusual lifecycle activities

6. **Handle exceptions and emergency scenarios**:
   - Define processes for emergency access provisioning
   - Establish procedures for handling lifecycle exceptions
   - Create temporary access mechanisms for contractors and vendors
   - Implement break-glass procedures for critical situations
   - Document and audit all exception cases

## Implementation examples

### Example 1: Automated user lifecycle management with AWS IAM Identity Center

```bash
# Create a user in IAM Identity Center
aws identitystore create-user \
  --identity-store-id d-1234567890 \
  --user-name john.doe \
  --display-name "John Doe" \
  --name-given-name John \
  --name-family-name Doe \
  --emails '[{"Value": "john.doe@example.com", "Type": "work", "Primary": true}]'

# Add user to a group based on their role
aws identitystore create-group-membership \
  --identity-store-id d-1234567890 \
  --group-id g-1234567890abcdef \
  --member-id u-1234567890abcdef

# Provision access to AWS accounts based on group membership
aws sso-admin create-account-assignment \
  --instance-arn "arn:aws:sso:::instance/ssoins-1234567890abcdef" \
  --target-id "123456789012" \
  --target-type "AWS_ACCOUNT" \
  --permission-set-arn "arn:aws:sso:::permissionSet/ssoins-1234567890abcdef/ps-1234567890abcdef" \
  --principal-id "g-1234567890abcdef" \
  --principal-type "GROUP"

# Remove user access when they leave (deprovisioning)
aws sso-admin delete-account-assignment \
  --instance-arn "arn:aws:sso:::instance/ssoins-1234567890abcdef" \
  --target-id "123456789012" \
  --target-type "AWS_ACCOUNT" \
  --permission-set-arn "arn:aws:sso:::permissionSet/ssoins-1234567890abcdef/ps-1234567890abcdef" \
  --principal-id "u-1234567890abcdef" \
  --principal-type "USER"

# Delete the user from IAM Identity Center
aws identitystore delete-user \
  --identity-store-id d-1234567890 \
  --user-id u-1234567890abcdef
```

### Example 2: Lambda function for automated lifecycle management

```python
import json
import boto3
from datetime import datetime, timedelta

def lambda_handler(event, context):
    """
    Lambda function to handle user lifecycle events
    """
    
    # Initialize AWS clients
    identitystore = boto3.client('identitystore')
    sso_admin = boto3.client('sso-admin')
    
    # Parse the lifecycle event
    event_type = event.get('eventType')
    user_data = event.get('userData')
    
    if event_type == 'USER_ONBOARDING':
        return handle_user_onboarding(identitystore, sso_admin, user_data)
    elif event_type == 'USER_ROLE_CHANGE':
        return handle_role_change(identitystore, sso_admin, user_data)
    elif event_type == 'USER_OFFBOARDING':
        return handle_user_offboarding(identitystore, sso_admin, user_data)
    else:
        return {
            'statusCode': 400,
            'body': json.dumps('Unknown event type')
        }

def handle_user_onboarding(identitystore, sso_admin, user_data):
    """Handle new user onboarding"""
    try:
        # Create user in Identity Center
        response = identitystore.create_user(
            IdentityStoreId=user_data['identityStoreId'],
            UserName=user_data['userName'],
            DisplayName=user_data['displayName'],
            Name={
                'GivenName': user_data['firstName'],
                'FamilyName': user_data['lastName']
            },
            Emails=[{
                'Value': user_data['email'],
                'Type': 'work',
                'Primary': True
            }]
        )
        
        user_id = response['UserId']
        
        # Add user to appropriate groups based on role
        for group_id in user_data.get('groups', []):
            identitystore.create_group_membership(
                IdentityStoreId=user_data['identityStoreId'],
                GroupId=group_id,
                MemberId={'UserId': user_id}
            )
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'User onboarded successfully',
                'userId': user_id
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error onboarding user: {str(e)}')
        }

def handle_user_offboarding(identitystore, sso_admin, user_data):
    """Handle user offboarding"""
    try:
        user_id = user_data['userId']
        
        # Remove user from all groups
        memberships = identitystore.list_group_memberships_for_member(
            IdentityStoreId=user_data['identityStoreId'],
            MemberId={'UserId': user_id}
        )
        
        for membership in memberships['GroupMemberships']:
            identitystore.delete_group_membership(
                IdentityStoreId=user_data['identityStoreId'],
                MembershipId=membership['MembershipId']
            )
        
        # Disable user account (or delete based on policy)
        identitystore.update_user(
            IdentityStoreId=user_data['identityStoreId'],
            UserId=user_id,
            Operations=[{
                'AttributePath': 'active',
                'AttributeValue': False
            }]
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps('User offboarded successfully')
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error offboarding user: {str(e)}')
        }
```

### Example 3: Lifecycle management workflow with AWS Step Functions

```json
{
  "Comment": "User Lifecycle Management Workflow",
  "StartAt": "DetermineLifecycleEvent",
  "States": {
    "DetermineLifecycleEvent": {
      "Type": "Choice",
      "Choices": [
        {
          "Variable": "$.eventType",
          "StringEquals": "ONBOARDING",
          "Next": "OnboardUser"
        },
        {
          "Variable": "$.eventType",
          "StringEquals": "ROLE_CHANGE",
          "Next": "UpdateUserRole"
        },
        {
          "Variable": "$.eventType",
          "StringEquals": "OFFBOARDING",
          "Next": "OffboardUser"
        }
      ],
      "Default": "InvalidEvent"
    },
    "OnboardUser": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-west-2:123456789012:function:OnboardUser",
      "Next": "NotifyManager"
    },
    "UpdateUserRole": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-west-2:123456789012:function:UpdateUserRole",
      "Next": "NotifyManager"
    },
    "OffboardUser": {
      "Type": "Parallel",
      "Branches": [
        {
          "StartAt": "DisableAccess",
          "States": {
            "DisableAccess": {
              "Type": "Task",
              "Resource": "arn:aws:lambda:us-west-2:123456789012:function:DisableUserAccess",
              "End": true
            }
          }
        },
        {
          "StartAt": "BackupUserData",
          "States": {
            "BackupUserData": {
              "Type": "Task",
              "Resource": "arn:aws:lambda:us-west-2:123456789012:function:BackupUserData",
              "End": true
            }
          }
        }
      ],
      "Next": "NotifyManager"
    },
    "NotifyManager": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-west-2:123456789012:function:NotifyManager",
      "End": true
    },
    "InvalidEvent": {
      "Type": "Fail",
      "Error": "InvalidEventType",
      "Cause": "The provided event type is not supported"
    }
  }
}
```

## AWS services to consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS IAM Identity Center</h4>
    <p>Helps you securely create or connect your workforce identities and manage their access centrally across AWS accounts and applications. Provides APIs for automated lifecycle management.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Identity and Access Management (IAM)</h4>
    <p>Enables you to manage access to AWS services and resources securely. Use IAM for managing service accounts and application identities throughout their lifecycle.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Lambda</h4>
    <p>Lets you run code without provisioning or managing servers. Use Lambda functions to automate lifecycle management processes and integrate with external systems.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Step Functions</h4>
    <p>Coordinates multiple AWS services into serverless workflows. Use Step Functions to orchestrate complex lifecycle management processes.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon EventBridge</h4>
    <p>A serverless event bus that makes it easy to connect applications together. Use EventBridge to trigger lifecycle management workflows based on events from HR systems or other sources.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS CloudTrail</h4>
    <p>Records API calls for your account and delivers log files to you. Use CloudTrail to audit and monitor lifecycle management activities.</p>
  </div>
</div>

## Benefits of managing access based on lifecycle

- **Enhanced security**: Ensures access is appropriate for current roles and employment status
- **Reduced risk**: Minimizes the risk of unauthorized access from former employees or changed roles
- **Improved compliance**: Supports regulatory requirements for access management and auditing
- **Operational efficiency**: Automates routine access management tasks
- **Better visibility**: Provides clear audit trails for access changes
- **Consistent processes**: Ensures standardized handling of lifecycle events
- **Reduced administrative overhead**: Minimizes manual intervention in access management

## Related resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/sec_permissions_lifecycle.html">AWS Well-Architected Framework - Manage access based on lifecycle</a></li>
    <li><a href="https://docs.aws.amazon.com/singlesignon/latest/userguide/what-is.html">AWS IAM Identity Center User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/singlesignon/latest/userguide/provision-automatically.html">Automatic provisioning in AWS IAM Identity Center</a></li>
    <li><a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_manage.html">Managing IAM users</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-automate-user-lifecycle-management-in-aws-iam-identity-center/">How to automate user lifecycle management in AWS IAM Identity Center</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-create-a-break-glass-admin-role-for-emergency-access-to-your-aws-environment/">How to create a break-glass admin role for emergency access to your AWS environment</a></li>
  </ul>
</div>
