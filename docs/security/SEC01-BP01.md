---
title: SEC01-BP01 - Separate workloads using accounts
layout: default
parent: SEC01 - How do you securely operate your workload?
grand_parent: Security
nav_order: 1
---

<div class="pillar-header">
  <h1>SEC01-BP01: Separate workloads using accounts</h1>
  <p>Organize workloads in separate accounts and group accounts based on function or common controls, rather than mirroring your reporting structure. Start with security and infrastructure in mind to enable your organization to set common guardrails as your workloads grow.</p>
</div>

## Implementation guidance

Separating workloads across multiple AWS accounts is a fundamental security best practice that provides several benefits:

- **Isolation boundary**: AWS accounts provide a strong isolation boundary for security, billing, and access control.
- **Minimize blast radius**: If a security event occurs in one account, it's less likely to affect resources in other accounts.
- **Simplified auditing**: Separate accounts make it easier to audit and report on specific workloads.
- **Specialized security controls**: Different workloads may require different security controls.

### Key steps for implementing this best practice:

1. **Define an account strategy** based on your organization's needs:
   - Workload-oriented: Separate accounts for each workload
   - Environment-oriented: Separate accounts for development, testing, and production
   - Team-oriented: Separate accounts for different teams or business units

2. **Implement AWS Organizations** to centrally manage and govern your environment:
   - Create an organization with your existing account as the management account
   - Create member accounts for your workloads
   - Group accounts into organizational units (OUs) based on common requirements

3. **Apply guardrails using Service Control Policies (SCPs)**:
   - Define preventative guardrails that restrict actions across accounts
   - Apply SCPs at the organization, OU, or account level
   - Start with least privilege and add permissions as needed

4. **Consider using AWS Control Tower**:
   - Automate the setup of a landing zone with best-practice blueprints
   - Implement guardrails for security, compliance, and operations
   - Provision new accounts that conform to your organization's standards

## AWS services to consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Organizations</h4>
    <p>Centrally manage and govern your environment as you scale your AWS resources. Use Service Control Policies (SCPs) to establish guardrails for all accounts in your organization.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Control Tower</h4>
    <p>Set up and govern a secure, compliant multi-account AWS environment based on best practices. Provides ongoing account management and governance as well as implementation of security controls.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS IAM Identity Center</h4>
    <p>Centrally manage access to multiple AWS accounts and business applications. Provides a single place to assign users and groups access to accounts and applications.</p>
  </div>
</div>

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/sec_securely_operate_workload_separate_workloads.html">AWS Well-Architected Framework - Separate workloads using accounts</a></li>
    <li><a href="https://docs.aws.amazon.com/whitepapers/latest/organizing-your-aws-environment/organizing-your-aws-environment.html">Organizing Your AWS Environment Using Multiple Accounts</a></li>
    <li><a href="https://aws.amazon.com/organizations/getting-started/">Getting Started with AWS Organizations</a></li>
  </ul>
</div>
