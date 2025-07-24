---
title: SEC02-BP05 - Audit and rotate credentials periodically
layout: default
parent: SEC02 - How do you manage authentication for people and machines?
grand_parent: Security
nav_order: 5
---

<div class="pillar-header">
  <h1>SEC02-BP05: Audit and rotate credentials periodically</h1>
  <p>When you cannot rely on temporary credentials and need to use long-term credentials, audit the credentials to ensure that the defined controls (such as MFA) are enforced, rotated regularly, and have the appropriate level of access.</p>
</div>

## Implementation guidance

While temporary credentials are preferred, there are cases where long-term credentials are necessary. In these situations, it's essential to implement robust processes for auditing and rotating these credentials to minimize security risks. Regular credential rotation reduces the impact of compromised credentials and helps maintain a strong security posture.

### Key steps for implementing this best practice:

1. **Inventory all long-term credentials**:
   - Identify all IAM users with long-term credentials
   - Document service accounts and their credentials
   - Identify application credentials stored in configuration files
   - Track API keys used by applications and services
   - Catalog database credentials and other secrets

2. **Implement credential auditing**:
   - Use AWS IAM Access Analyzer to identify unused credentials
   - Enable AWS Config to monitor credential compliance
   - Configure AWS CloudTrail to log credential usage
   - Set up Amazon CloudWatch alarms for suspicious credential activities
   - Implement regular credential access reviews

3. **Establish credential rotation policies**:
   - Define rotation schedules based on credential type and sensitivity
   - Document procedures for credential rotation
   - Implement automated rotation where possible
   - Create emergency rotation procedures for compromised credentials
   - Align rotation policies with compliance requirements

4. **Automate credential rotation**:
   - Use AWS Secrets Manager for automatic rotation of secrets
   - Implement Lambda functions for custom rotation logic
   - Configure database credential rotation
   - Set up API key rotation processes
   - Implement certificate rotation procedures

5. **Monitor credential compliance**:
   - Track credential age and rotation status
   - Set up alerts for credentials approaching rotation deadlines
   - Generate compliance reports for credential management
   - Monitor for unauthorized credential creation
   - Audit privileged credential usage

6. **Implement credential security controls**:
   - Enforce MFA for all human users with long-term credentials
   - Implement the principle of least privilege for all credentials
   - Use credential vaulting for sensitive credentials
   - Apply appropriate access controls to credential stores
   - Implement just-in-time access for privileged credentials

## Implementation examples

### Example 1: Auditing IAM users for credential compliance

```bash
# List IAM users with access keys older than 90 days
aws iam list-users --query 'Users[*].[UserName]' --output text | while read username; do
  aws iam list-access-keys --user-name $username --query 'AccessKeyMetadata[?CreateDate<=`'$(date -d '90 days ago' '+%Y-%m-%dT%H:%M:%SZ')'`].[UserName,AccessKeyId,Status,CreateDate]' --output text
done

# List IAM users without MFA enabled
aws iam list-users --query 'Users[?!MFADevices].UserName' --output text

# Create an AWS Config rule to check for MFA
aws configservice put-config-rule --config-rule '{
  "ConfigRuleName": "mfa-enabled-for-iam-console-access",
  "Description": "Checks whether AWS Multi-Factor Authentication (MFA) is enabled for all IAM users that use a console password.",
  "Source": {
    "Owner": "AWS",
    "SourceIdentifier": "MFA_ENABLED_FOR_IAM_CONSOLE_ACCESS"
  },
  "Scope": {
    "ComplianceResourceTypes": ["AWS::IAM::User"]
  }
}'
```

### Example 2: Setting up automatic rotation with AWS Secrets Manager

```bash
# Create a secret with rotation enabled
aws secretsmanager create-secret \
  --name "prod/db/credentials" \
  --description "Production database credentials" \
  --secret-string '{"username":"admin","password":"initial-password"}' \
  --tags Key=Environment,Value=Production

# Configure automatic rotation
aws secretsmanager rotate-secret \
  --secret-id "prod/db/credentials" \
  --rotation-lambda-arn "arn:aws:lambda:region:account-id:function:RotationFunction" \
  --rotation-rules '{"AutomaticallyAfterDays": 30}'

# Create a CloudWatch Events rule to monitor rotation failures
aws events put-rule \
  --name "SecretsManagerRotationFailure" \
  --event-pattern '{
    "source": ["aws.secretsmanager"],
    "detail-type": ["AWS API Call via CloudTrail"],
    "detail": {
      "eventSource": ["secretsmanager.amazonaws.com"],
      "eventName": ["RotateSecret"],
      "errorCode": [{"exists": true}]
    }
  }'

# Add a target to the rule (SNS topic)
aws events put-targets \
  --rule "SecretsManagerRotationFailure" \
  --targets "Id"="1","Arn"="arn:aws:sns:region:account-id:SecretRotationFailures"
```

### Example 3: Implementing a credential audit and rotation policy

```
# Sample Credential Audit and Rotation Policy

1. Credential Inventory:
   - Maintain a central inventory of all long-term credentials
   - Document credential type, owner, purpose, and systems accessed
   - Update inventory when new credentials are created or retired

2. Rotation Schedules:
   - IAM user access keys: 90 days
   - Database credentials: 60 days
   - API keys for external services: 180 days
   - SSL/TLS certificates: 1 year or before expiration
   - Service account passwords: 90 days

3. Audit Procedures:
   - Weekly automated scan for non-compliant credentials
   - Monthly review of credential inventory
   - Quarterly access review for all privileged credentials
   - Immediate audit after security incidents

4. Compliance Reporting:
   - Generate monthly credential compliance reports
   - Track rotation metrics and trends
   - Report exceptions with justification
   - Include credential status in security posture reporting
```

## AWS services to consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS IAM Access Analyzer</h4>
    <p>Helps you identify resources in your organization and accounts that are shared with an external entity. Also identifies unused access to help you remove unnecessary permissions.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Secrets Manager</h4>
    <p>Helps you protect secrets needed to access your applications, services, and IT resources. Enables you to rotate, manage, and retrieve database credentials, API keys, and other secrets throughout their lifecycle.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Config</h4>
    <p>Enables you to assess, audit, and evaluate the configurations of your AWS resources. Helps you maintain compliance with credential policies through continuous monitoring and automated remediation.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS CloudTrail</h4>
    <p>Records API calls for your account and delivers log files to you. Use CloudTrail to monitor credential usage and detect unauthorized access attempts.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon CloudWatch</h4>
    <p>Monitors your AWS resources and the applications you run on AWS in real time. Set up alarms for credential-related events and automate responses to security issues.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Lambda</h4>
    <p>Lets you run code without provisioning or managing servers. Used for implementing custom credential rotation logic and automated compliance checks.</p>
  </div>
</div>

## Benefits of auditing and rotating credentials periodically

- **Reduced risk exposure**: Limiting the lifetime of credentials reduces the impact of credential compromise
- **Improved security posture**: Regular rotation helps maintain a strong security posture
- **Compliance support**: Meets requirements for many compliance frameworks
- **Early detection of issues**: Regular audits help identify security issues before they can be exploited
- **Enforced security practices**: Ensures security controls like MFA are consistently applied
- **Reduced credential sprawl**: Regular audits help identify and remove unnecessary credentials
- **Automated security**: Automation reduces the burden of manual credential management

## Related resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/sec_identities_audit.html">AWS Well-Architected Framework - Audit and rotate credentials periodically</a></li>
    <li><a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html">Managing access keys for IAM users</a></li>
    <li><a href="https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets.html">Rotating your AWS Secrets Manager secrets</a></li>
    <li><a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html">Security best practices in IAM</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-rotate-access-keys-for-iam-users/">How to rotate access keys for IAM users</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-use-aws-config-to-monitor-for-and-respond-to-amazon-rds-instances-not-using-iam-authentication/">How to use AWS Config to monitor for and respond to Amazon RDS instances not using IAM authentication</a></li>
  </ul>
</div>
