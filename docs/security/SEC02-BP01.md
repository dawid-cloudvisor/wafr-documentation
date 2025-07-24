---
title: SEC02-BP01 - Use strong sign-in mechanisms
layout: default
parent: SEC02 - How do you manage authentication for people and machines?
grand_parent: Security
nav_order: 1
---

<div class="pillar-header">
  <h1>SEC02-BP01: Use strong sign-in mechanisms</h1>
  <p>Enforce minimum password length, and educate your users to avoid common or reused passwords. Enforce multi-factor authentication (MFA) with software or hardware mechanisms to provide an additional layer of verification.</p>
</div>

## Implementation guidance

Strong sign-in mechanisms are essential for protecting your AWS environment from unauthorized access. By implementing robust authentication methods, you can significantly reduce the risk of credential compromise and unauthorized access to your AWS resources.

### Key steps for implementing this best practice:

1. **Implement strong password policies**:
   - Enforce minimum password length (at least 12 characters)
   - Require a mix of character types (uppercase, lowercase, numbers, special characters)
   - Prevent the use of common or previously breached passwords
   - Set appropriate password expiration policies
   - Implement account lockout after multiple failed attempts

2. **Enforce Multi-Factor Authentication (MFA)**:
   - Require MFA for all users, especially those with elevated privileges
   - Support multiple MFA options:
     - Virtual MFA (authenticator apps like AWS Virtual MFA, Google Authenticator)
     - Hardware MFA devices (YubiKey, Gemalto token)
     - FIDO security keys (U2F, WebAuthn)
   - Monitor and alert on MFA disablement
   - Consider implementing MFA for programmatic access

3. **Implement contextual authentication**:
   - Use conditional access policies based on:
     - User location/IP address
     - Device health and compliance
     - Time of day/unusual access times
     - Unusual access patterns
   - Require step-up authentication for sensitive operations

4. **Secure root user accounts**:
   - Enable MFA for all root user accounts
   - Store root user credentials securely
   - Limit the use of root user accounts to only necessary tasks
   - Monitor root user activity

5. **Implement single sign-on (SSO) where appropriate**:
   - Use AWS IAM Identity Center for workforce identities
   - Integrate with your existing identity provider
   - Implement just-in-time access provisioning
   - Enforce consistent authentication policies across all applications

6. **Educate users on security best practices**:
   - Provide training on creating and managing strong passwords
   - Explain the importance of MFA
   - Teach users to recognize phishing attempts
   - Establish clear procedures for reporting suspected security incidents

## Implementation examples

### Example 1: Setting up a strong IAM password policy

```json
{
  "MinimumPasswordLength": 14,
  "RequireSymbols": true,
  "RequireNumbers": true,
  "RequireUppercaseCharacters": true,
  "RequireLowercaseCharacters": true,
  "AllowUsersToChangePassword": true,
  "MaxPasswordAge": 90,
  "PasswordReusePrevention": 24,
  "HardExpiry": false
}
```

AWS CLI command:
```bash
aws iam update-account-password-policy \
  --minimum-password-length 14 \
  --require-symbols \
  --require-numbers \
  --require-uppercase-characters \
  --require-lowercase-characters \
  --allow-users-to-change-password \
  --max-password-age 90 \
  --password-reuse-prevention 24
```

### Example 2: Enforcing MFA using Service Control Policies (SCPs)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyAllExceptListedIfNoMFA",
      "Effect": "Deny",
      "NotAction": [
        "iam:CreateVirtualMFADevice",
        "iam:EnableMFADevice",
        "iam:GetUser",
        "iam:ListMFADevices",
        "iam:ListVirtualMFADevices",
        "iam:ResyncMFADevice",
        "sts:GetSessionToken"
      ],
      "Resource": "*",
      "Condition": {
        "BoolIfExists": {
          "aws:MultiFactorAuthPresent": "false"
        }
      }
    }
  ]
}
```

### Example 3: Setting up MFA for a user in AWS IAM

```bash
# Create a virtual MFA device
aws iam create-virtual-mfa-device \
  --virtual-mfa-device-name MyUser-MFA \
  --outfile QRCode.png \
  --bootstrap-method QRCodePNG

# Enable MFA for a user
aws iam enable-mfa-device \
  --user-name MyUser \
  --serial-number arn:aws:iam::123456789012:mfa/MyUser-MFA \
  --authentication-code-1 123456 \
  --authentication-code-2 789012
```

## AWS services to consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Identity and Access Management (IAM)</h4>
    <p>Enables you to manage access to AWS services and resources securely. IAM supports MFA and allows you to set password policies for IAM users.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS IAM Identity Center</h4>
    <p>Helps you securely create or connect your workforce identities and manage their access centrally across AWS accounts and applications. Supports MFA and integrates with your existing identity provider.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Organizations</h4>
    <p>Helps you centrally manage and govern your environment as you scale your AWS resources. Use Service Control Policies (SCPs) to enforce MFA across your organization.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon Cognito</h4>
    <p>Provides authentication, authorization, and user management for your web and mobile apps. Supports MFA and allows you to implement adaptive authentication.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS CloudTrail</h4>
    <p>Records API calls for your account and delivers log files to you. Use CloudTrail to monitor sign-in activities and detect unauthorized access attempts.</p>
  </div>
</div>

## Benefits of using strong sign-in mechanisms

- **Reduced risk of unauthorized access**: Strong authentication mechanisms make it significantly harder for attackers to gain access to your AWS environment
- **Defense in depth**: Multiple authentication factors provide layered security
- **Compliance support**: Many compliance frameworks require strong authentication mechanisms
- **Improved security posture**: Strengthens your overall security posture by protecting the entry point to your AWS resources
- **Reduced risk of credential theft**: MFA protects against attacks even if passwords are compromised
- **Increased user awareness**: Implementing strong authentication raises security awareness among users

## Related resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/sec_identities_enforce_mechanisms.html">AWS Well-Architected Framework - Use strong sign-in mechanisms</a></li>
    <li><a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_mfa.html">Using multi-factor authentication (MFA) in AWS</a></li>
    <li><a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_passwords_account-policy.html">Setting an account password policy for IAM users</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-create-a-custom-password-policy-for-your-aws-account/">How to create a custom password policy for your AWS account</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-protect-the-integrity-of-your-encrypted-data-by-using-aws-key-management-service-and-encryptioncontext/">How to protect the integrity of your encrypted data by using AWS Key Management Service and EncryptionContext</a></li>
    <li><a href="https://docs.aws.amazon.com/singlesignon/latest/userguide/mfa-how-to.html">Enable MFA for AWS IAM Identity Center</a></li>
  </ul>
</div>
