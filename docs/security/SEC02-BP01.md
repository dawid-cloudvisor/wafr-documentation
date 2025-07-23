---
title: SEC02-BP01 - Use strong sign-in mechanisms
layout: default
parent: SEC02 - How do you manage identities for people and machines?
grand_parent: Security
nav_order: 1
---

<div class="pillar-header">
  <h1>SEC02-BP01: Use strong sign-in mechanisms</h1>
  <p>Enforce minimum password length, and educate your users to avoid common or reused passwords. Enforce multi-factor authentication (MFA) with software or hardware mechanisms to provide an additional layer of verification.</p>
</div>

## Implementation guidance

Strong sign-in mechanisms are essential for protecting your AWS environment from unauthorized access. By implementing robust authentication methods, you can significantly reduce the risk of credential compromise.

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
     - Virtual MFA (authenticator apps)
     - Hardware MFA devices (YubiKey, etc.)
     - SMS or email-based MFA (less secure, use only when other options aren't available)
   - Monitor and alert on MFA disablement

3. **Implement contextual authentication**:
   - Use conditional access policies based on:
     - User location/IP address
     - Device health and compliance
     - Time of day/unusual access times
     - Unusual access patterns
   - Require step-up authentication for sensitive operations

4. **Educate users on security best practices**:
   - Provide training on creating and managing strong passwords
   - Explain the importance of MFA
   - Teach users to recognize phishing attempts
   - Establish clear procedures for reporting suspected security incidents

5. **Monitor and audit authentication activities**:
   - Track failed login attempts
   - Monitor for unusual authentication patterns
   - Regularly review authentication logs
   - Set up alerts for suspicious activities

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

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/sec_identity_management_strong_sign_in.html">AWS Well-Architected Framework - Use strong sign-in mechanisms</a></li>
    <li><a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_mfa.html">Using multi-factor authentication (MFA) in AWS</a></li>
    <li><a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_passwords_account-policy.html">Setting an account password policy for IAM users</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-create-a-custom-password-policy-for-your-aws-account/">How to create a custom password policy for your AWS account</a></li>
  </ul>
</div>
