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

AWS accounts provide strong isolation boundaries for your workloads. Using separate accounts for different workloads helps minimize the impact of a security event, simplifies management, and provides a clean separation for security controls, costs, and workload-specific configurations.

### Key steps for implementing this best practice:

1. **Define your multi-account strategy**:
   - Identify your organization's requirements for account separation
   - Consider security, compliance, operational, and business needs
   - Determine the level of isolation required between workloads
   - Plan your account structure based on workload characteristics rather than organizational structure

2. **Implement AWS Organizations**:
   - Create an organization with your existing account as the management account
   - Set up Organizational Units (OUs) to group accounts with similar requirements
   - Consider common OU structures such as:
     - Security OU for security services and tools
     - Infrastructure OU for shared services
     - Sandbox OU for development and testing
     - Workload OUs for production applications
     - Deployment pipeline OUs for CI/CD tools

3. **Apply security controls at the organization level**:
   - Implement Service Control Policies (SCPs) to establish guardrails
   - Start with preventative guardrails that restrict actions across accounts
   - Apply SCPs at the organization, OU, or account level
   - Use AWS Control Tower to implement pre-defined guardrails

4. **Establish account governance**:
   - Define processes for account provisioning and decommissioning
   - Implement standardized account configurations
   - Establish account naming conventions and tagging strategies
   - Define account-level security baselines

5. **Implement centralized identity management**:
   - Use AWS IAM Identity Center for centralized access management
   - Implement federation with your existing identity provider
   - Define permission sets that grant appropriate access levels
   - Assign users and groups to accounts based on their responsibilities

6. **Set up centralized logging and monitoring**:
   - Configure AWS CloudTrail across all accounts
   - Set up centralized log storage in a dedicated logging account
   - Implement cross-account monitoring with Amazon CloudWatch
   - Use AWS Security Hub and Amazon GuardDuty for security monitoring

## Account separation strategies

### Separation by environment
Separate accounts for different stages of your software development lifecycle:
- Development
- Testing/QA
- Staging
- Production

### Separation by workload
Separate accounts for different applications or services:
- Customer-facing website
- Internal applications
- Data processing pipelines
- Analytics platforms

### Separation by team
Separate accounts for different teams or business units:
- Marketing applications
- Finance applications
- Engineering tools
- Research projects

### Separation by regulatory requirement
Separate accounts for workloads with different compliance requirements:
- PCI DSS compliant workloads
- HIPAA compliant workloads
- GDPR relevant workloads
- SOC 2 compliant workloads

## Implementation examples

### Example 1: Basic AWS Organizations structure

```yaml
Organization:
  - Management Account (root)
    - Security OU
      - Security Tooling Account
      - Audit Account
      - Log Archive Account
    - Infrastructure OU
      - Network Account
      - Shared Services Account
    - Workloads OU
      - Production OU
        - Production Account A
        - Production Account B
      - Non-Production OU
        - Development Account
        - Testing Account
```

### Example 2: Service Control Policy to enforce encryption

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "RequireEncryptionForS3",
      "Effect": "Deny",
      "Action": [
        "s3:PutObject"
      ],
      "Resource": "*",
      "Condition": {
        "StringNotEquals": {
          "s3:x-amz-server-side-encryption": [
            "AES256",
            "aws:kms"
          ]
        }
      }
    }
  ]
}
```

### Example 3: AWS Control Tower implementation

AWS Control Tower provides a simplified way to set up and govern a secure, multi-account AWS environment based on best practices. It automates the setup of a landing zone and implements guardrails for security, compliance, and operations.

Key components of an AWS Control Tower implementation:
- Management account
- Log archive account
- Audit account
- Preventive guardrails (implemented as SCPs)
- Detective guardrails (implemented as AWS Config Rules)
- Account Factory for standardized account provisioning

## AWS services to consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Organizations</h4>
    <p>Helps you centrally manage and govern your environment as you scale your AWS resources. Enables you to centrally manage policies across multiple AWS accounts.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Control Tower</h4>
    <p>Provides a simplified way to set up and govern a secure, multi-account AWS environment based on best practices. Automates the setup of a landing zone and implements guardrails for security, compliance, and operations.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS IAM Identity Center</h4>
    <p>Helps you securely create or connect your workforce identities and manage their access centrally across AWS accounts and applications. Provides a single place to assign users and groups access to accounts and applications.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS CloudTrail</h4>
    <p>Records API calls for your account and delivers log files to you. Provides event history of your AWS account activity, including actions taken through the AWS Management Console, AWS SDKs, command line tools, and other AWS services.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Config</h4>
    <p>Enables you to assess, audit, and evaluate the configurations of your AWS resources. Helps you maintain compliance with security standards and best practices through continuous monitoring.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Security Hub</h4>
    <p>Provides a comprehensive view of your security state in AWS and helps you check your compliance with security standards and best practices. Aggregates, organizes, and prioritizes security alerts from multiple AWS services.</p>
  </div>
</div>

## Benefits of separating workloads using accounts

- **Enhanced security**: Isolation between workloads reduces the risk of cross-workload vulnerabilities
- **Simplified access management**: Easier to apply the principle of least privilege
- **Improved cost tracking**: Better visibility into which workloads are generating costs
- **Tailored service quotas**: Each account has its own service quotas
- **Streamlined compliance**: Easier to demonstrate compliance for specific workloads
- **Reduced blast radius**: Security incidents are contained within account boundaries
- **Customized controls**: Apply specific security controls based on workload requirements

## Related resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/sec_securely_operate_multi_accounts.html">AWS Well-Architected Framework - Separate workloads using accounts</a></li>
    <li><a href="https://docs.aws.amazon.com/whitepapers/latest/organizing-your-aws-environment/organizing-your-aws-environment.html">Organizing Your AWS Environment Using Multiple Accounts</a></li>
    <li><a href="https://aws.amazon.com/organizations/getting-started/">Getting Started with AWS Organizations</a></li>
    <li><a href="https://aws.amazon.com/blogs/mt/best-practices-for-organizational-units-with-aws-organizations/">Best Practices for Organizational Units with AWS Organizations</a></li>
    <li><a href="https://docs.aws.amazon.com/controltower/latest/userguide/getting-started-with-control-tower.html">Getting Started with AWS Control Tower</a></li>
    <li><a href="https://aws.amazon.com/blogs/mt/aws-organizations-aws-config-and-terraform-a-multi-account-setup-for-declarative-infrastructure-governance/">AWS Organizations, AWS Config, and Terraform: A Multi-Account Setup for Declarative Infrastructure Governance</a></li>
  </ul>
</div>
