---
title: COST02-BP03 - Implement an account structure
layout: default
parent: COST02 - How do you govern usage?
grand_parent: Cost Optimization
nav_order: 3
---

<div class="pillar-header">
  <h1>COST02-BP03: Implement an account structure</h1>
  <p>Implement a multi-account structure that supports your organizational requirements and governance needs. A well-designed account structure provides strong isolation boundaries, enables granular cost allocation, simplifies security management, and supports scalable governance across your organization.</p>
</div>

## Implementation guidance

A thoughtfully designed multi-account structure is fundamental to effective cloud governance and cost management. It provides natural boundaries for security, compliance, cost allocation, and operational management while enabling scalable governance across your organization.

### Account Structure Design Principles

**Isolation by Purpose**: Create separate accounts for different purposes such as production, development, testing, security, and shared services. This provides strong isolation and reduces the risk of cross-environment issues.

**Business Alignment**: Align account structure with your organizational structure, business units, and cost centers to enable accurate cost allocation and accountability.

**Scalability**: Design the structure to accommodate future growth in teams, projects, and business units without requiring major restructuring.

**Governance Enablement**: Structure accounts to support your governance requirements, including compliance boundaries, security controls, and operational procedures.

### Common Account Structure Patterns

**Environment-Based Structure**: Separate accounts for production, staging, development, and testing environments. This pattern provides clear isolation between different stages of the development lifecycle.

**Business Unit Structure**: Separate accounts for different business units or divisions. This pattern enables clear cost allocation and allows business units to operate with appropriate autonomy.

**Project-Based Structure**: Individual accounts for major projects or applications. This pattern provides clear project cost visibility and enables project-specific governance.

**Hybrid Structure**: Combination of multiple patterns, such as business unit accounts with environment-specific sub-accounts. This pattern provides flexibility while maintaining clear boundaries.

### Account Categories and Functions

**Core Accounts**: Essential accounts that support the overall organization, including master/management account, security account, logging account, and shared services account.

**Workload Accounts**: Accounts that host specific applications, services, or workloads. These accounts contain the resources that directly support business functions.

**Environment Accounts**: Accounts organized by environment type (production, staging, development) that may span multiple workloads or business units.

**Sandbox Accounts**: Accounts for experimentation, learning, and proof-of-concept activities. These accounts typically have relaxed governance but strict cost controls.

## AWS Services to Consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Organizations</h4>
    <p>Provides centralized management of multiple AWS accounts. Essential for implementing account structure, applying policies consistently, and managing consolidated billing.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Control Tower</h4>
    <p>Provides a pre-configured multi-account environment with built-in governance guardrails. Simplifies the setup and management of a well-architected multi-account structure.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Service Control Policies (SCPs)</h4>
    <p>Enable you to apply governance policies consistently across accounts in your organization. Use SCPs to enforce account-level controls and prevent policy violations.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Single Sign-On (SSO)</h4>
    <p>Provides centralized access management across multiple AWS accounts. Simplifies user management and enables consistent access controls across your account structure.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS CloudFormation StackSets</h4>
    <p>Enables you to deploy CloudFormation stacks across multiple accounts and regions. Use StackSets to ensure consistent resource deployment and configuration across your account structure.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Config</h4>
    <p>Provides configuration monitoring and compliance checking across multiple accounts. Use Config to ensure resources in all accounts comply with organizational standards.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS CloudTrail</h4>
    <p>Provides audit logging across all accounts in your organization. Essential for governance oversight, compliance reporting, and security monitoring.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Cost Explorer</h4>
    <p>Provides cost analysis and reporting across your multi-account structure. Use Cost Explorer to analyze costs by account, organizational unit, and other dimensions.</p>
  </div>
</div>

## Implementation Steps

### 1. Design Account Structure
- Analyze organizational requirements and constraints
- Choose appropriate account structure pattern(s)
- Define account categories and naming conventions
- Plan for future growth and organizational changes
- Document the account structure design and rationale

### 2. Set Up AWS Organizations
- Create the master/management account
- Set up organizational units (OUs) to group accounts
- Configure consolidated billing and cost allocation
- Implement initial service control policies
- Set up cross-account access and permissions

### 3. Create Core Accounts
- Set up security account for centralized security services
- Create logging account for centralized log aggregation
- Establish shared services account for common resources
- Configure networking account if using centralized networking
- Set up any other core accounts based on your design

### 4. Implement Account Provisioning Process
- Create standardized account creation procedures
- Implement automation for account setup and configuration
- Establish account naming and tagging standards
- Create account onboarding and offboarding processes
- Set up monitoring and compliance checking for new accounts

### 5. Configure Cross-Account Services
- Set up AWS Single Sign-On for centralized access management
- Configure CloudTrail for organization-wide audit logging
- Implement Config for multi-account compliance monitoring
- Set up centralized monitoring and alerting
- Configure backup and disaster recovery across accounts

### 6. Establish Governance Framework
- Apply service control policies to organizational units
- Implement cost controls and budget alerts
- Set up compliance monitoring and reporting
- Create account management procedures and documentation
- Train teams on multi-account best practices

## Account Structure Examples

### Small Organization Structure
```
Root Organization
├── Security OU
│   └── Security Account
├── Production OU
│   └── Production Account
├── Non-Production OU
│   ├── Development Account
│   └── Testing Account
└── Sandbox OU
    └── Sandbox Account
```

### Medium Organization Structure
```
Root Organization
├── Core OU
│   ├── Master Account
│   ├── Security Account
│   ├── Logging Account
│   └── Shared Services Account
├── Production OU
│   ├── App1 Production Account
│   ├── App2 Production Account
│   └── Infrastructure Account
├── Non-Production OU
│   ├── Development Account
│   ├── Testing Account
│   └── Staging Account
└── Sandbox OU
    ├── Team1 Sandbox Account
    └── Team2 Sandbox Account
```

### Large Enterprise Structure
```
Root Organization
├── Core OU
│   ├── Master Account
│   ├── Security Account
│   ├── Logging Account
│   ├── Networking Account
│   └── Shared Services Account
├── Business Unit A OU
│   ├── BU-A Production OU
│   │   ├── BU-A App1 Prod Account
│   │   └── BU-A App2 Prod Account
│   ├── BU-A Non-Production OU
│   │   ├── BU-A Development Account
│   │   └── BU-A Testing Account
│   └── BU-A Sandbox Account
├── Business Unit B OU
│   ├── BU-B Production OU
│   │   └── BU-B App1 Prod Account
│   ├── BU-B Non-Production OU
│   │   ├── BU-B Development Account
│   │   └── BU-B Testing Account
│   └── BU-B Sandbox Account
└── Suspended OU
    └── Decommissioned Accounts
```

## Account Management Best Practices

### Account Naming and Organization

**Consistent Naming**: Use consistent naming conventions that clearly identify the account purpose, environment, and ownership. For example: "companyname-businessunit-environment-purpose".

**Organizational Units**: Use OUs to group related accounts and apply policies consistently. Structure OUs to match your governance and operational requirements.

**Account Metadata**: Use account tags and descriptions to provide additional context and enable better cost allocation and management.

### Security and Access Management

**Least Privilege Access**: Implement role-based access control with minimum necessary permissions for each account and user role.

**Cross-Account Roles**: Use cross-account IAM roles rather than sharing credentials between accounts. This provides better security and audit trails.

**Centralized Identity Management**: Use AWS SSO or federated identity providers to manage access across all accounts consistently.

### Cost Management and Allocation

**Cost Allocation Tags**: Implement consistent tagging strategies across all accounts to enable detailed cost allocation and reporting.

**Budget Controls**: Set up budgets and alerts for each account to monitor spending and prevent cost overruns.

**Reserved Instance Management**: Coordinate Reserved Instance purchases across accounts to maximize utilization and savings.

### Operational Management

**Standardized Configurations**: Use infrastructure as code to ensure consistent configurations across accounts.

**Centralized Monitoring**: Implement centralized logging, monitoring, and alerting across all accounts.

**Automated Compliance**: Use AWS Config and other services to automatically monitor and enforce compliance across accounts.

## Account Lifecycle Management

### Account Creation Process
- Define standard account creation procedures and automation
- Implement approval workflows for new account requests
- Set up baseline configurations and security controls automatically
- Establish account onboarding procedures and documentation

### Account Maintenance
- Regular review of account usage and relevance
- Update account configurations based on changing requirements
- Monitor account compliance and security posture
- Implement account health checks and reporting

### Account Decommissioning
- Establish procedures for safely decommissioning unused accounts
- Ensure data backup and retention requirements are met
- Clean up cross-account dependencies and access
- Move decommissioned accounts to suspended OU for audit trail

## Common Challenges and Solutions

### Challenge: Account Sprawl and Management Overhead

**Solution**: Implement clear account creation policies and approval processes. Use automation for account setup and management. Regularly review and consolidate accounts where appropriate. Establish clear account lifecycle management procedures.

### Challenge: Cross-Account Networking Complexity

**Solution**: Use AWS Transit Gateway or similar services for centralized networking. Implement standardized networking patterns and automation. Consider using a dedicated networking account for shared network resources.

### Challenge: Cost Allocation and Chargeback Complexity

**Solution**: Implement comprehensive tagging strategies and cost allocation methods. Use AWS Cost Explorer and billing tools to automate cost reporting. Establish clear cost allocation policies and procedures.

### Challenge: Maintaining Consistency Across Accounts

**Solution**: Use AWS Organizations service control policies and AWS Config for governance. Implement infrastructure as code for consistent deployments. Use AWS Control Tower for standardized account setup and management.

### Challenge: Security and Compliance Management

**Solution**: Implement centralized security monitoring and logging. Use AWS Security Hub for centralized security findings. Establish clear security policies and automated compliance checking across all accounts.

## Integration with Governance Framework

### Policy Application
- Use organizational units to apply policies consistently across related accounts
- Implement service control policies that enforce organizational requirements
- Create account-specific policies for unique requirements
- Regular review and update of policies based on changing needs

### Compliance Monitoring
- Implement centralized compliance monitoring across all accounts
- Use AWS Config rules to check compliance with organizational standards
- Create compliance dashboards and reporting for stakeholders
- Establish procedures for addressing compliance violations

### Cost Governance
- Implement budget controls and spending limits for each account
- Use cost allocation tags to enable detailed cost reporting
- Create cost optimization processes that work across the account structure
- Establish cost review and approval processes for account-level spending

## Related Resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/cost_govern_usage_account_structure.html">AWS Well-Architected Framework - Implement an account structure</a></li>
    <li><a href="https://docs.aws.amazon.com/organizations/latest/userguide/orgs_introduction.html">AWS Organizations User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/controltower/latest/userguide/what-is-control-tower.html">AWS Control Tower User Guide</a></li>
    <li><a href="https://aws.amazon.com/blogs/mt/best-practices-for-organizational-units-with-aws-organizations/">Best Practices for Organizational Units with AWS Organizations</a></li>
    <li><a href="https://docs.aws.amazon.com/singlesignon/latest/userguide/what-is.html">AWS Single Sign-On User Guide</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-use-service-control-policies-to-set-permission-guardrails-across-accounts-in-your-aws-organization/">Using Service Control Policies for Permission Guardrails</a></li>
    <li><a href="https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/what-is-cfnstacksets.html">AWS CloudFormation StackSets</a></li>
    <li><a href="https://aws.amazon.com/architecture/well-architected/">AWS Well-Architected Framework</a></li>
  </ul>
</div>

<style>
.pillar-header {
  background-color: #e8f5e8;
  border-left: 5px solid #2d7d2d;
}

.pillar-header h1 {
  color: #2d7d2d;
}

.aws-service-content h4 {
  color: #2d7d2d;
}

.related-resources {
  background-color: #e8f5e8;
}

.related-resources h2 {
  color: #2d7d2d;
}
</style>
