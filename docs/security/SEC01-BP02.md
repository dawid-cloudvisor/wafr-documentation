---
title: SEC01-BP02 - Secure account root user and properties
layout: default
parent: SEC01 - How do you securely operate your workload?
grand_parent: Security
nav_order: 2
---

<div class="pillar-header">
  <h1>SEC01-BP02: Secure account root user and properties</h1>
  <p>Secure access to your accounts, for example by enabling MFA and restrict use of the root user, and configure account contacts.</p>
</div>

## Implementation guidance

The root user in your AWS account has complete access to all AWS services and resources in the account. Securing this user is critical to the overall security of your AWS environment. Additionally, securing account properties helps ensure that only authorized individuals can make changes to your account settings.

### Key steps for implementing this best practice:

1. **Secure the root user credentials**:
   - Create a strong, complex password for the root user
   - Enable multi-factor authentication (MFA) for the root user
   - Store root user credentials securely using a password manager or physical safe
   - Do not share root user credentials with anyone
   - Do not create access keys for the root user

2. **Restrict use of the root user**:
   - Use the root user only for tasks that specifically require root user access
   - Create administrative IAM users or roles for day-to-day administrative tasks
   - Log out of the root user account immediately after completing required tasks
   - Monitor root user activity using AWS CloudTrail

3. **Configure account contacts**:
   - Set up alternate contacts for billing, operations, and security
   - Use distribution lists rather than individual email addresses
   - Ensure contact information is up-to-date
   - Implement a process to regularly review and update contact information

4. **Secure account recovery options**:
   - Ensure the email address associated with the root user is secure and accessible
   - Verify that the phone number associated with the account is current
   - Document the process for recovering root user access
   - Test the recovery process periodically
   - Ensure multiple team members understand the recovery process

5. **Implement additional account security measures**:
   - Enable AWS CloudTrail in all regions
   - Configure CloudTrail logs to be immutable
   - Set up alerts for root user activity
   - Implement Service Control Policies (SCPs) in AWS Organizations to restrict root user actions
   - Regularly review account security settings

## Tasks that require root user credentials

Only a limited number of tasks require the use of root user credentials:

- Change your account name, email address, or root user password
- Change your AWS support plan
- Close your AWS account
- Register as a seller in the Reserved Instance Marketplace
- Configure an Amazon S3 bucket to enable MFA Delete
- Sign up for AWS GovCloud
- Request removal of the credit card limitation on your account
- Restore IAM user permissions if the only IAM administrator accidentally revokes their own permissions

For all other administrative tasks, create IAM users or roles with appropriate permissions.

## Implementation examples

### Example 1: Securing the root user

```
1. Sign in to the AWS Management Console as the root user
2. Navigate to IAM > Dashboard
3. Under "Security recommendations", look for "Enable MFA on your root account"
4. Click "Manage MFA" and follow the steps to enable MFA
5. Choose between Virtual MFA device, Hardware TOTP token, or Hardware key fob MFA device
6. Complete the MFA setup process
7. Sign out of the root user account
```

### Example 2: Setting up CloudTrail to monitor root user activity

```yaml
Resources:
  CloudTrailBucket:
    Type: 'AWS::S3::Bucket'
    Properties:
      BucketName: !Sub 'cloudtrail-logs-${AWS::AccountId}'
      VersioningConfiguration:
        Status: Enabled
      BucketEncryption:
        ServerSideEncryptionConfiguration:
          - ServerSideEncryptionByDefault:
              SSEAlgorithm: 'AES256'
  
  CloudTrail:
    Type: 'AWS::CloudTrail::Trail'
    Properties:
      IsLogging: true
      IsMultiRegionTrail: true
      EnableLogFileValidation: true
      IncludeGlobalServiceEvents: true
      S3BucketName: !Ref CloudTrailBucket
      CloudWatchLogsLogGroupArn: !GetAtt CloudTrailLogGroup.Arn
      CloudWatchLogsRoleArn: !GetAtt CloudTrailRole.Arn
      EventSelectors:
        - ReadWriteType: All
          IncludeManagementEvents: true
```

### Example 3: Setting up alerts for root user activity

```yaml
Resources:
  RootUserActivityFilter:
    Type: 'AWS::Logs::MetricFilter'
    Properties:
      LogGroupName: !Ref CloudTrailLogGroup
      FilterPattern: '{ $.userIdentity.type = "Root" && $.userIdentity.invokedBy NOT EXISTS }'
      MetricTransformations:
        - MetricName: RootUserActivity
          MetricNamespace: CloudTrailMetrics
          MetricValue: '1'
  
  RootUserActivityAlarm:
    Type: 'AWS::CloudWatch::Alarm'
    Properties:
      AlarmName: RootUserActivityAlarm
      AlarmDescription: 'Alarm when root user activity is detected'
      MetricName: RootUserActivity
      Namespace: CloudTrailMetrics
      Statistic: Sum
      Period: 300
      EvaluationPeriods: 1
      Threshold: 1
      ComparisonOperator: GreaterThanOrEqualToThreshold
      AlarmActions:
        - !Ref AlertSNSTopic
```

## AWS services to consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Identity and Access Management (IAM)</h4>
    <p>Enables you to manage access to AWS services and resources securely. Use IAM to create administrative users instead of using the root user.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS CloudTrail</h4>
    <p>Records API calls for your account and delivers log files to you. Use CloudTrail to monitor root user activity and detect unauthorized access attempts.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon CloudWatch</h4>
    <p>Monitors your AWS resources and the applications you run on AWS in real time. Set up alerts for root user activity and other security-related events.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Organizations</h4>
    <p>Helps you centrally manage and govern your environment as you scale your AWS resources. Use Service Control Policies (SCPs) to restrict root user actions.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Security Hub</h4>
    <p>Provides a comprehensive view of your security state in AWS. Includes checks for root user security best practices.</p>
  </div>
</div>

## Benefits of securing the root user and account properties

- **Reduced risk of unauthorized access**: Protecting the root user prevents attackers from gaining full control of your AWS account
- **Improved security posture**: Following security best practices for the root user strengthens your overall security posture
- **Simplified account recovery**: Properly configured account contacts make it easier to recover access if needed
- **Enhanced accountability**: Using IAM users instead of the root user provides better audit trails and accountability
- **Compliance support**: Many compliance frameworks require securing privileged accounts like the root user

## Related resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/sec_securely_operate_aws_account.html">AWS Well-Architected Framework - Secure AWS account</a></li>
    <li><a href="https://docs.aws.amazon.com/accounts/latest/reference/root-user-tasks.html">Tasks that require root user credentials</a></li>
    <li><a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/id_root-user.html">AWS account root user</a></li>
    <li><a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_mfa.html">Using multi-factor authentication (MFA) in AWS</a></li>
    <li><a href="https://docs.aws.amazon.com/accounts/latest/reference/manage-acct-update-root-user.html">Updating the root user contact information</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/securing-the-root-user/">AWS Security Blog: Securing the Root User</a></li>
  </ul>
</div>
