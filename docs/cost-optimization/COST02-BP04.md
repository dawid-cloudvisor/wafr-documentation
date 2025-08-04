---
title: COST02-BP04 - Implement groups and roles
layout: default
parent: COST02 - How do you govern usage?
grand_parent: Cost Optimization
nav_order: 4
---

<div class="pillar-header">
  <h1>COST02-BP04: Implement groups and roles</h1>
  <p>Implement groups and roles that align with your organization's structure and governance requirements. Well-designed identity and access management enables appropriate access controls, supports cost accountability, and ensures that users have the permissions they need while preventing unauthorized or inappropriate resource usage.</p>
</div>

## Implementation guidance

Effective identity and access management is crucial for cost governance, as it determines who can provision resources, what resources they can create, and how much they can spend. A well-designed groups and roles structure supports both security and cost management objectives.

### Identity and Access Management Principles

**Principle of Least Privilege**: Grant users and roles only the minimum permissions necessary to perform their job functions. This reduces the risk of unauthorized resource provisioning and associated costs.

**Role-Based Access Control (RBAC)**: Organize permissions around job functions and responsibilities rather than individual users. This simplifies management and ensures consistent access controls.

**Separation of Duties**: Separate sensitive functions such as resource provisioning, cost management, and security administration to prevent conflicts of interest and reduce risk.

**Regular Access Reviews**: Implement regular reviews of user access and permissions to ensure they remain appropriate and current with organizational changes.

### Group and Role Design Strategy

**Functional Alignment**: Design groups and roles that align with organizational functions such as development, operations, security, and finance. This ensures that permissions match job responsibilities.

**Environment-Based Roles**: Create different roles for different environments (production, staging, development) with appropriate permission levels for each environment's risk profile.

**Cost-Aware Permissions**: Include cost-related permissions in role design, ensuring that users who need to monitor or manage costs have appropriate access to cost management tools.

**Scalable Structure**: Design a role structure that can scale with organizational growth without requiring frequent restructuring or permission updates.

### Core Role Categories

**Administrative Roles**: High-privilege roles for system administrators, security teams, and other users who need broad access to manage infrastructure and governance.

**Developer Roles**: Roles for development teams with permissions appropriate for their environment and responsibilities, including resource provisioning within defined limits.

**Operations Roles**: Roles for operational teams responsible for monitoring, maintenance, and incident response, with permissions focused on operational activities.

**Finance and Cost Management Roles**: Specialized roles for users responsible for cost monitoring, budget management, and financial reporting.

## AWS Services to Consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Identity and Access Management (IAM)</h4>
    <p>Provides fine-grained access control for AWS services and resources. Essential for implementing role-based access control and enforcing cost governance policies.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Single Sign-On (SSO)</h4>
    <p>Provides centralized access management across multiple AWS accounts. Simplifies user management and enables consistent role implementation across your organization.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Organizations</h4>
    <p>Enables centralized management of multiple AWS accounts and provides the foundation for implementing consistent access controls across your organization.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS CloudTrail</h4>
    <p>Provides audit logging of all API calls and user activities. Essential for monitoring access patterns, investigating security incidents, and ensuring compliance.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Access Analyzer</h4>
    <p>Helps identify resources that are shared with external entities and validates that access policies meet security and compliance requirements.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Cost Explorer</h4>
    <p>Provides cost analysis capabilities that can be accessed through appropriate IAM permissions. Essential for enabling cost visibility for relevant roles.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Budgets</h4>
    <p>Enables budget creation and monitoring with role-based access controls. Allows different roles to have appropriate levels of budget visibility and management.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Resource Groups</h4>
    <p>Enables logical grouping of resources for management and access control purposes. Supports role-based access to specific resource groups.</p>
  </div>
</div>

## Implementation Steps

### 1. Analyze Organizational Structure
- Map organizational roles and responsibilities
- Identify different user types and their access requirements
- Analyze current access patterns and identify gaps or issues
- Document business requirements for access control and cost governance

### 2. Design Role Architecture
- Create role categories based on job functions and responsibilities
- Define permission sets for each role category
- Design role hierarchy and inheritance patterns
- Plan for role scalability and maintenance

### 3. Implement Core Roles
- Create administrative roles with appropriate high-level permissions
- Implement developer roles with environment-appropriate permissions
- Set up operations roles focused on monitoring and maintenance
- Create specialized roles for cost management and financial oversight

### 4. Configure Access Management
- Set up AWS SSO or federated identity management
- Implement role-based access control across all accounts
- Configure cross-account access using roles rather than shared credentials
- Set up automated user provisioning and deprovisioning

### 5. Implement Cost-Aware Permissions
- Include cost management permissions in relevant roles
- Set up budget and cost alert access for appropriate users
- Implement spending limits and approval workflows
- Configure cost allocation and reporting access

### 6. Establish Governance Processes
- Create role request and approval processes
- Implement regular access reviews and audits
- Set up monitoring and alerting for access anomalies
- Create documentation and training for role management

## Role Design Examples

### Development Team Roles

**Junior Developer Role**:
- Read access to development environment resources
- Limited resource creation permissions (small instances only)
- No production environment access
- Basic cost visibility for their projects

**Senior Developer Role**:
- Full access to development and staging environments
- Limited production read access for troubleshooting
- Ability to create and modify resources within budget limits
- Cost monitoring access for their applications

**Lead Developer Role**:
- Full development and staging access
- Production deployment permissions with approval workflows
- Budget management for their team's projects
- Access to cost optimization tools and recommendations

### Operations Team Roles

**Operations Engineer Role**:
- Read access to all environments for monitoring
- Incident response permissions for production
- Ability to scale resources during incidents
- Full access to monitoring and logging tools

**Site Reliability Engineer Role**:
- Full operational access across all environments
- Ability to implement performance and cost optimizations
- Access to capacity planning and forecasting tools
- Permissions to implement automated scaling and optimization

**Operations Manager Role**:
- Oversight access to all operational activities
- Budget management for operational costs
- Access to operational metrics and cost reporting
- Ability to approve operational changes and expenditures

### Finance and Cost Management Roles

**Cost Analyst Role**:
- Read access to all cost and usage data
- Ability to create and manage budgets and alerts
- Access to cost optimization recommendations
- Permissions to generate cost reports and analysis

**Finance Manager Role**:
- Full access to cost management tools and data
- Ability to set spending limits and approval thresholds
- Access to financial forecasting and planning tools
- Permissions to manage Reserved Instances and Savings Plans

**FinOps Engineer Role**:
- Technical access to implement cost optimization recommendations
- Ability to configure automated cost controls
- Access to detailed usage and performance data
- Permissions to implement cost allocation and tagging strategies

### Administrative Roles

**Security Administrator Role**:
- Full access to security-related services and configurations
- Ability to implement and manage access controls
- Access to audit logs and security monitoring tools
- Permissions to investigate and respond to security incidents

**Cloud Administrator Role**:
- Full administrative access to cloud infrastructure
- Ability to manage accounts, organizations, and policies
- Access to all monitoring and management tools
- Permissions to implement governance controls and automation

**Compliance Officer Role**:
- Read access to compliance-related data and reports
- Ability to configure compliance monitoring and alerting
- Access to audit trails and governance reports
- Permissions to generate compliance documentation

## Permission Boundary Strategies

### Cost-Based Permission Boundaries

**Spending Limits**: Implement permission boundaries that prevent users from creating resources that exceed specified cost thresholds.

**Resource Type Restrictions**: Limit users to specific resource types or sizes based on their role and cost implications.

**Time-Based Limits**: Implement temporary permissions that automatically expire, reducing the risk of long-term cost accumulation.

**Approval-Based Boundaries**: Require approval for actions that exceed certain cost thresholds or risk levels.

### Environment-Based Boundaries

**Production Restrictions**: Implement stricter permission boundaries for production environments, requiring additional approvals or limiting resource types.

**Development Flexibility**: Provide more flexible permissions in development environments while maintaining cost controls.

**Sandbox Limitations**: Implement strict cost and time limits for sandbox environments to prevent runaway costs.

### Project-Based Boundaries

**Project-Specific Permissions**: Limit users to resources within their assigned projects or cost centers.

**Budget-Aligned Boundaries**: Align permission boundaries with project budgets and spending allocations.

**Resource Tagging Requirements**: Require appropriate resource tagging for cost allocation and governance.

## Access Review and Governance

### Regular Access Reviews

**Quarterly Reviews**: Conduct comprehensive reviews of all user access and role assignments every quarter.

**Role-Based Reviews**: Review permissions for each role category to ensure they remain appropriate and current.

**Exception Reviews**: Regularly review any exceptions or temporary access grants to ensure they are still needed.

**Automated Reviews**: Implement automated tools to identify unused permissions, excessive access, or policy violations.

### Access Monitoring and Alerting

**Unusual Access Patterns**: Monitor for access patterns that deviate from normal behavior or indicate potential security issues.

**Cost-Related Access**: Monitor access to cost management tools and high-cost resource creation activities.

**Cross-Account Access**: Monitor and alert on cross-account access activities to ensure they are authorized and appropriate.

**Privileged Access**: Implement enhanced monitoring and alerting for high-privilege administrative access.

### Compliance and Audit Support

**Audit Trail Maintenance**: Maintain comprehensive audit trails of all access-related activities for compliance and investigation purposes.

**Compliance Reporting**: Generate regular reports on access controls, role assignments, and compliance with governance policies.

**Policy Validation**: Regularly validate that access policies meet organizational and regulatory requirements.

**Documentation Maintenance**: Keep role definitions, procedures, and documentation current and accessible for audits.

## Common Challenges and Solutions

### Challenge: Role Proliferation and Complexity

**Solution**: Design a hierarchical role structure with inheritance to reduce duplication. Use role templates and automation for consistent role creation. Regularly review and consolidate similar roles.

### Challenge: Balancing Security and Usability

**Solution**: Implement graduated permissions based on risk levels. Use temporary elevated access for high-risk activities. Provide self-service capabilities for routine tasks while maintaining controls for sensitive operations.

### Challenge: Managing Access Across Multiple Accounts

**Solution**: Use AWS SSO for centralized access management. Implement consistent role naming and structure across accounts. Use cross-account roles rather than duplicating users in multiple accounts.

### Challenge: Keeping Permissions Current with Changing Roles

**Solution**: Implement regular access reviews and automated permission analysis. Use role-based rather than user-based permissions. Create processes for updating permissions when job roles change.

### Challenge: Cost Control Without Hindering Innovation

**Solution**: Implement graduated spending limits based on user experience and role. Provide sandbox environments with strict limits for experimentation. Use approval workflows for high-cost activities rather than blanket restrictions.

## Integration with Cost Governance

### Budget Integration
- Align role permissions with budget allocations and spending limits
- Implement role-based budget visibility and management
- Create approval workflows that consider both permissions and budget availability
- Use role assignments to drive cost allocation and chargeback processes

### Cost Monitoring Integration
- Provide appropriate cost visibility based on role responsibilities
- Implement role-based cost alerting and notification
- Enable cost optimization activities through appropriate role permissions
- Create cost reporting that aligns with organizational roles and responsibilities

### Policy Enforcement Integration
- Use IAM policies to enforce cost governance requirements
- Implement service control policies that align with role-based access
- Create automated policy enforcement that considers both security and cost implications
- Use role-based access to implement approval workflows for cost-sensitive activities

## Related Resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/cost_govern_usage_groups_roles.html">AWS Well-Architected Framework - Implement groups and roles</a></li>
    <li><a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html">AWS IAM User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/singlesignon/latest/userguide/what-is.html">AWS Single Sign-On User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html">IAM Best Practices</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-use-permission-boundaries-to-delegate-responsibly-in-aws/">Using Permission Boundaries to Delegate Responsibly</a></li>
    <li><a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html">Permissions Boundaries for IAM Entities</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/techniques-for-writing-least-privilege-iam-policies/">Techniques for Writing Least Privilege IAM Policies</a></li>
    <li><a href="https://docs.aws.amazon.com/organizations/latest/userguide/orgs_introduction.html">AWS Organizations User Guide</a></li>
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
