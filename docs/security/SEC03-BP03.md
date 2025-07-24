---
title: SEC03-BP03 - Establish emergency access process
layout: default
parent: SEC03 - How do you manage permissions for people and machines?
grand_parent: Security
nav_order: 3
---

<div class="pillar-header">
  <h1>SEC03-BP03: Establish emergency access process</h1>
  <p>Establish a process that allows emergency access to your workload in the unlikely event of an automated process or pipeline issue. This will help you rely on least privilege access, but ensure users can obtain the right level of access when they need it. For example, establish a process for administrators to verify and approve their request.</p>
</div>

## Implementation guidance

Even with well-designed systems and robust automation, emergencies can occur that require immediate access to resolve critical issues. An emergency access process (sometimes called "break-glass" access) provides a controlled mechanism for obtaining elevated privileges in urgent situations while maintaining security and accountability.

### Key steps for implementing this best practice:

1. **Define emergency scenarios**:
   - Identify situations that qualify as emergencies
   - Document criteria for invoking emergency access
   - Establish severity levels for different types of emergencies
   - Define the scope of emergency access for each scenario
   - Create clear guidelines for when emergency access is appropriate

2. **Design emergency access mechanisms**:
   - Create dedicated emergency access roles with appropriate permissions
   - Implement time-limited access for emergency credentials
   - Consider using sealed emergency credentials (physical or digital)
   - Set up just-in-time access provisioning
   - Implement multi-person approval for emergency access

3. **Implement strong controls**:
   - Require multi-factor authentication for emergency access
   - Implement enhanced logging and monitoring for emergency credentials
   - Set up real-time alerts when emergency access is used
   - Enforce automatic expiration of emergency access
   - Consider IP restrictions or other contextual controls

4. **Document emergency procedures**:
   - Create step-by-step instructions for requesting emergency access
   - Document the approval process and required approvers
   - Provide clear procedures for using emergency access
   - Include instructions for revoking access after the emergency
   - Ensure documentation is accessible during emergencies

5. **Establish governance processes**:
   - Require post-incident reviews after emergency access use
   - Implement regular testing of emergency access procedures
   - Conduct periodic audits of emergency access controls
   - Update procedures based on lessons learned
   - Include emergency access in your security training

6. **Secure emergency credentials**:
   - Store emergency credentials securely
   - Implement rotation for emergency credentials
   - Limit knowledge of emergency access mechanisms
   - Consider using sealed envelopes or secure digital vaults
   - Implement monitoring for unauthorized access attempts

## Implementation examples

### Example 1: Emergency access role with approval workflow

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "EmergencyAccessRole",
      "Effect": "Allow",
      "Action": [
        "ec2:*",
        "rds:*",
        "s3:*",
        "cloudwatch:*",
        "logs:*"
      ],
      "Resource": "*",
      "Condition": {
        "Bool": {
          "aws:MultiFactorAuthPresent": "true"
        },
        "NumericLessThan": {
          "aws:MultiFactorAuthAge": "3600"
        }
      }
    }
  ]
}
```

```bash
# Create an emergency access role
aws iam create-role \
  --role-name EmergencyAccessRole \
  --assume-role-policy-document file://trust-policy.json \
  --description "Role for emergency access to critical resources"

# Attach the emergency access policy
aws iam put-role-policy \
  --role-name EmergencyAccessRole \
  --policy-name EmergencyAccessPolicy \
  --policy-document file://emergency-policy.json

# Set up CloudTrail alerting for emergency role usage
aws events put-rule \
  --name "EmergencyRoleUsageAlert" \
  --event-pattern '{
    "source": ["aws.sts"],
    "detail-type": ["AWS API Call via CloudTrail"],
    "detail": {
      "eventSource": ["sts.amazonaws.com"],
      "eventName": ["AssumeRole"],
      "requestParameters": {
        "roleArn": ["arn:aws:iam::123456789012:role/EmergencyAccessRole"]
      }
    }
  }'
```

### Example 2: Break-glass procedure documentation

```
# Emergency Access Procedure

## Criteria for Emergency Access
Emergency access should only be used when:
1. There is a critical production incident affecting business operations
2. Normal access methods are unavailable or insufficient
3. Immediate action is required to resolve the issue
4. The issue cannot be resolved through standard procedures

## Emergency Access Request Process
1. Requestor identifies need for emergency access
2. Requestor contacts the on-call security team via the emergency hotline
3. Requestor provides:
   - Name and employee ID
   - Nature of the emergency
   - Systems requiring access
   - Estimated duration needed
4. Security team validates the request and identity of the requestor
5. If approved, security team provides access to sealed credentials or approves role assumption

## Using Emergency Access
1. Log in using the emergency credentials or assume the emergency role
2. Enable session recording if possible
3. Perform only the necessary actions to resolve the emergency
4. Document all actions taken during the emergency access session
5. Terminate the session as soon as the emergency is resolved

## Post-Emergency Process
1. Notify the security team that the emergency is resolved
2. Submit a detailed report within 24 hours including:
   - Actions taken during the emergency session
   - Root cause of the emergency
   - Recommendations to prevent similar emergencies
3. Participate in a post-incident review
4. Security team rotates emergency credentials

## Auditing and Compliance
All emergency access events will be:
1. Logged in CloudTrail and CloudWatch
2. Reviewed by the security team
3. Included in compliance reports
4. Subject to regular audits
```

### Example 3: AWS Systems Manager Automation for emergency access

```yaml
description: 'Automation for emergency access to production environment'
schemaVersion: '0.3'
assumeRole: '{{AutomationAssumeRole}}'
parameters:
  AutomationAssumeRole:
    type: String
    description: Role for automation to assume
  EmergencyAccessRole:
    type: String
    description: Role ARN for emergency access
    default: arn:aws:iam::123456789012:role/EmergencyAccessRole
  RequestorARN:
    type: String
    description: ARN of the identity requesting emergency access
  JustificationText:
    type: String
    description: Justification for emergency access
  DurationSeconds:
    type: String
    description: Duration for emergency access (in seconds)
    default: '3600'
    allowedPattern: '^[0-9]+$'
mainSteps:
  - name: ValidateRequest
    action: 'aws:executeAwsApi'
    inputs:
      Service: iam
      Api: GetUser
      UserName: '{{RequestorARN}}'
    isCritical: true
    nextStep: NotifySecurityTeam
  - name: NotifySecurityTeam
    action: 'aws:executeAwsApi'
    inputs:
      Service: sns
      Api: Publish
      TopicArn: arn:aws:sns:us-west-2:123456789012:EmergencyAccessAlerts
      Subject: 'Emergency Access Request'
      Message: 'Emergency access requested by {{RequestorARN}} with justification: {{JustificationText}}'
    nextStep: GrantAccess
  - name: GrantAccess
    action: 'aws:executeAwsApi'
    inputs:
      Service: sts
      Api: AssumeRole
      RoleArn: '{{EmergencyAccessRole}}'
      RoleSessionName: 'EmergencyAccess-{{RequestorARN}}'
      DurationSeconds: '{{DurationSeconds}}'
    outputs:
      - Name: AccessKeyId
        Selector: $.Credentials.AccessKeyId
      - Name: SecretAccessKey
        Selector: $.Credentials.SecretAccessKey
      - Name: SessionToken
        Selector: $.Credentials.SessionToken
    nextStep: LogAccessGrant
  - name: LogAccessGrant
    action: 'aws:executeAwsApi'
    inputs:
      Service: cloudtrail
      Api: LookupEvents
      LookupAttributes:
        - AttributeKey: EventName
          AttributeValue: AssumeRole
    isEnd: true
```

## AWS services to consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Identity and Access Management (IAM)</h4>
    <p>Enables you to manage access to AWS services and resources securely. Use IAM roles with appropriate permissions for emergency access.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS CloudTrail</h4>
    <p>Records API calls for your account and delivers log files to you. Use CloudTrail to monitor and audit emergency access usage.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon CloudWatch</h4>
    <p>Monitors your AWS resources and the applications you run on AWS in real time. Set up alerts for emergency access usage and create dashboards for visibility.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Secrets Manager</h4>
    <p>Helps you protect secrets needed to access your applications, services, and IT resources. Can be used to securely store emergency access credentials with rotation capabilities.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Systems Manager</h4>
    <p>Gives you visibility and control of your infrastructure on AWS. Use Automation documents to create controlled emergency access workflows.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon SNS</h4>
    <p>A fully managed messaging service for both application-to-application and application-to-person communication. Use SNS to send notifications when emergency access is requested or used.</p>
  </div>
</div>

## Benefits of establishing an emergency access process

- **Reduced operational risk**: Ensures critical issues can be resolved quickly
- **Enhanced security**: Provides controlled access during emergencies while maintaining security principles
- **Improved accountability**: Creates clear audit trails for emergency access usage
- **Better compliance**: Demonstrates due diligence for regulatory requirements
- **Increased confidence**: Teams can implement strict access controls knowing emergency procedures exist
- **Faster incident resolution**: Clear procedures reduce confusion during emergencies
- **Reduced standing privileges**: Allows for tighter day-to-day access controls

## Related resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/sec_permissions_emergency_process.html">AWS Well-Architected Framework - Establish emergency access process</a></li>
    <li><a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user.html">Creating a role to delegate permissions to an IAM user</a></li>
    <li><a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_mfa_configure-api-require.html">Configuring MFA-protected API access</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-create-a-break-glass-admin-role-for-emergency-access-to-your-aws-environment/">How to create a break-glass admin role for emergency access to your AWS environment</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-implement-a-human-review-of-code-deployments-by-using-aws-lambda-and-amazon-sns/">How to implement a human review of code deployments by using AWS Lambda and Amazon SNS</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-record-ssh-sessions-established-through-a-bastion-host/">How to record SSH sessions established through a bastion host</a></li>
  </ul>
</div>
