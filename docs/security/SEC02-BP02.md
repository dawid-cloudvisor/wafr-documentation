---
title: SEC02-BP02 - Rely on a centralized identity provider
layout: default
parent: SEC02 - How do you manage identities for people and machines?
grand_parent: Security
nav_order: 2
---

<div class="pillar-header">
  <h1>SEC02-BP02: Rely on a centralized identity provider</h1>
  <p>For workforce identities (your employees, contractors, and partners), rely on an identity provider that enables you to manage identities in a centralized place. This makes it easier to manage access across multiple applications and services because you are creating, managing, and revoking access from a single location.</p>
</div>

## Implementation guidance

Centralizing identity management provides numerous benefits, including simplified user management, consistent security policies, and improved user experience. By using a centralized identity provider, you can manage access across multiple AWS accounts and applications from a single location.

### Key steps for implementing this best practice:

1. **Choose a centralized identity provider**:
   - Use AWS IAM Identity Center as your primary identity provider
   - Or integrate with your existing identity provider:
     - Microsoft Active Directory (on-premises or AWS Managed Microsoft AD)
     - Azure Active Directory
     - Okta, Ping Identity, or other SAML 2.0 compatible providers
   - Consider your organization's existing investments and requirements

2. **Configure federation between AWS and your identity provider**:
   - Set up SAML 2.0 federation
   - Configure attribute mapping to pass user attributes to AWS
   - Establish trust relationships between your identity provider and AWS

3. **Implement single sign-on (SSO)**:
   - Enable SSO for AWS Management Console access
   - Configure SSO for AWS CLI and SDK access
   - Extend SSO to other business applications

4. **Manage user lifecycle centrally**:
   - Implement automated user provisioning and deprovisioning
   - Synchronize user attributes and group memberships
   - Establish processes for handling user role changes

5. **Apply consistent security policies**:
   - Enforce MFA through your identity provider
   - Implement consistent password policies
   - Apply conditional access policies based on user, device, and network context

## AWS services to consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS IAM Identity Center</h4>
    <p>Helps you securely create or connect your workforce identities and manage their access centrally across AWS accounts and applications. Provides built-in identity store or integrates with your existing identity provider.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Directory Service</h4>
    <p>Provides multiple ways to use Microsoft Active Directory (AD) with other AWS services. Includes AWS Managed Microsoft AD, Simple AD, and AD Connector.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Identity and Access Management (IAM)</h4>
    <p>Enables you to manage access to AWS services and resources securely. Supports identity federation with external identity providers.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon Cognito</h4>
    <p>Provides authentication, authorization, and user management for your web and mobile apps. Can be used as an identity provider for customer-facing applications.</p>
  </div>
</div>

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/sec_identity_management_centralized_identity.html">AWS Well-Architected Framework - Rely on a centralized identity provider</a></li>
    <li><a href="https://docs.aws.amazon.com/singlesignon/latest/userguide/what-is.html">AWS IAM Identity Center User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers.html">Identity providers and federation in IAM</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/the-next-evolution-in-aws-single-sign-on/">The next evolution in AWS Single Sign-On</a></li>
  </ul>
</div>
