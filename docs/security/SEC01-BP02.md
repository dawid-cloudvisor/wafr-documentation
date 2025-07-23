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

The root user in your AWS account has complete access to all AWS services and resources in the account. Securing this user is critical to the overall security of your AWS environment.

### Key steps for implementing this best practice:

1. **Secure the root user**:
   - Enable multi-factor authentication (MFA) for the root user
   - Do not create access keys for the root user
   - Store root user credentials securely (password and MFA device)
   - Use a complex password for the root user

2. **Limit use of the root user**:
   - Use the root user only for tasks that specifically require root user access
   - Create administrative IAM users for day-to-day administrative tasks
   - Monitor root user activity using AWS CloudTrail

3. **Configure account contacts**:
   - Set up alternate contacts for billing, operations, and security
   - Ensure contact information is up-to-date
   - Consider using distribution lists rather than individual email addresses

4. **Secure account properties**:
   - Configure account security challenge questions
   - Verify that the account's email address is secure and accessible
   - Ensure the account's phone number is current

5. **Implement account recovery procedures**:
   - Document the process for recovering root user access
   - Ensure multiple team members understand the recovery process
   - Test the recovery process periodically

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
    <p>Records API calls for your account and delivers log files to you. Use CloudTrail to monitor root user activity.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Organizations</h4>
    <p>Centrally manage and govern your environment as you scale your AWS resources. Helps you manage multiple accounts and implement security controls across them.</p>
  </div>
</div>

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/sec_securely_operate_workload_secure_account.html">AWS Well-Architected Framework - Secure AWS account</a></li>
    <li><a href="https://docs.aws.amazon.com/accounts/latest/reference/root-user-tasks.html">Tasks that require root user credentials</a></li>
    <li><a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/id_root-user.html">AWS account root user</a></li>
    <li><a href="https://docs.aws.amazon.com/accounts/latest/reference/manage-acct-update-root-user.html">Updating the root user contact information</a></li>
  </ul>
</div>
