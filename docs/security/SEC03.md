---
title: SEC03 - How do you manage permissions for people and machines?
layout: default
parent: Security
has_children: true
nav_order: 3
---

<div class="pillar-header">
  <h1>SEC03: How do you manage permissions for people and machines?</h1>
  <p>Manage permissions to control access to people and machine identities that require access to AWS and your workload. Permissions control who can access what, and under what conditions.</p>
</div>

## Best Practices

This question includes the following best practices:

<div class="best-practices-list">
  <ul>
    <li><a href="SEC03-BP01.html">SEC03-BP01: Define access requirements</a></li>
    <li><a href="SEC03-BP02.html">SEC03-BP02: Grant least privilege access</a></li>
    <li><a href="SEC03-BP03.html">SEC03-BP03: Establish emergency access process</a></li>
    <li><a href="SEC03-BP04.html">SEC03-BP04: Reduce permissions continuously</a></li>
    <li><a href="SEC03-BP05.html">SEC03-BP05: Define permission guardrails for your organization</a></li>
    <li><a href="SEC03-BP06.html">SEC03-BP06: Manage access based on lifecycle</a></li>
    <li><a href="SEC03-BP07.html">SEC03-BP07: Analyze public and cross-account access</a></li>
    <li><a href="SEC03-BP08.html">SEC03-BP08: Share resources securely within your organization</a></li>
    <li><a href="SEC03-BP09.html">SEC03-BP09: Share resources securely with a third party</a></li>
  </ul>
</div>

## Key Concepts

### Permission Management Principles

**Least Privilege**: Grant only the minimum permissions necessary to perform required tasks. This fundamental principle reduces the potential impact of compromised credentials and limits the scope of potential security incidents.

**Defense in Depth**: Implement multiple layers of access controls, including identity-based policies, resource-based policies, permission boundaries, and organizational controls.

**Zero Trust**: Verify every access request regardless of location or previous authentication. Continuously validate access decisions based on current context and risk factors.

### Access Control Models

**Role-Based Access Control (RBAC)**: Assign permissions to roles based on job functions, then assign users to appropriate roles. This simplifies permission management and ensures consistent access patterns.

**Attribute-Based Access Control (ABAC)**: Make access decisions based on attributes of the user, resource, environment, and action. This provides fine-grained, dynamic access control.

**Resource-Based Access Control**: Use resource-based policies to control access to specific resources, enabling cross-account access and service-to-service authentication.

## AWS Services to Consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Identity and Access Management (IAM)</h4>
    <p>Enables you to manage access to AWS services and resources securely. Core service for implementing identity-based policies, roles, and permission boundaries.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS IAM Identity Center</h4>
    <p>Helps you securely create or connect your workforce identities and manage their access centrally across AWS accounts and applications. Ideal for managing human user access at scale.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Organizations</h4>
    <p>Helps you centrally manage and govern your environment as you scale your AWS resources. Use Service Control Policies (SCPs) to implement organization-wide permission guardrails.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS IAM Access Analyzer</h4>
    <p>Helps you identify resources in your organization and accounts that are shared with an external entity. Also helps identify unused permissions and generate least privilege policies.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Resource Access Manager (RAM)</h4>
    <p>Helps you securely share your resources across AWS accounts within your organization. Enables controlled resource sharing without compromising security.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS CloudTrail</h4>
    <p>Records API calls for your account and delivers log files to you. Essential for monitoring permission usage and detecting unauthorized access attempts.</p>
  </div>
</div>

## Implementation Approach

### 1. Assessment and Planning
- Inventory all identities (human and machine) that need access
- Document current access patterns and requirements
- Identify compliance and regulatory requirements
- Define your organization's risk tolerance

### 2. Design and Architecture
- Choose appropriate access control models for different use cases
- Design role hierarchies and permission structures
- Plan for cross-account and third-party access scenarios
- Design emergency access procedures

### 3. Implementation
- Implement identity providers and federation
- Create roles and policies following least privilege principles
- Set up permission boundaries and guardrails
- Implement monitoring and auditing mechanisms

### 4. Operations and Maintenance
- Regularly review and update permissions
- Monitor for unused and excessive permissions
- Conduct periodic access reviews
- Respond to security events and policy violations

## Common Challenges and Solutions

### Challenge: Permission Sprawl
**Solution**: Implement regular permission reviews, use IAM Access Analyzer to identify unused permissions, and establish processes for permission lifecycle management.

### Challenge: Emergency Access
**Solution**: Design and test break-glass procedures, implement time-limited emergency roles, and ensure proper monitoring and auditing of emergency access usage.

### Challenge: Cross-Account Access
**Solution**: Use IAM roles with external IDs for secure cross-account access, implement proper trust relationships, and monitor cross-account activities.

### Challenge: Third-Party Access
**Solution**: Implement additional security controls for third-party access, use time-limited credentials, and apply enhanced monitoring and restrictions.

## Related resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html">AWS Well-Architected Framework - Security Pillar</a></li>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/sec-03.html">SEC03: How do you manage permissions for people and machines?</a></li>
    <li><a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html">Security best practices in IAM</a></li>
    <li><a href="https://aws.amazon.com/identity/">AWS Identity Solutions</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/techniques-for-writing-least-privilege-iam-policies/">Techniques for writing least privilege IAM policies</a></li>
  </ul>
</div>

<style>
.best-practices-list ul {
  list-style-type: none;
  padding-left: 0;
}

.best-practices-list li {
  background-color: #ffead7;
  margin-bottom: 0.5rem;
  border-radius: 5px;
  border: 1px solid #ffcca5;
}

.best-practices-list li a {
  display: block;
  padding: 0.75rem 1rem;
  color: #ff6a00;
  text-decoration: none;
  font-weight: 500;
}

.best-practices-list li a:hover {
  background-color: #ffcca5;
  border-radius: 4px;
}
</style>
