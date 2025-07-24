---
title: SEC02 - How do you manage authentication for people and machines?
layout: default
parent: Security
has_children: true
nav_order: 2
---

<div class="pillar-header">
  <h1>SEC02: How do you manage authentication for people and machines?</h1>
  <p>There are two types of identities you need to manage when approaching operating secure AWS workloads. Understanding the type of identity you need to manage and grant access helps you ensure the right identities have access to the right resources under the right conditions. Human identities: Your administrators, developers, operators, and end users require an identity to access your AWS environments and applications. Machine identities: Your service applications, operational tools, and workloads require an identity to make requests to AWS services, for example, to read data. For both types of identities, manage their authentication centrally, and ensure that they're only granted the minimum access required to perform their function.</p>
</div>

## Best Practices

This question includes the following best practices:

<div class="best-practices-list">
  <ul>
    <li><a href="./SEC02-BP01.html">SEC02-BP01: Use strong sign-in mechanisms</a></li>
    <li><a href="./SEC02-BP02.html">SEC02-BP02: Use temporary credentials</a></li>
    <li><a href="./SEC02-BP03.html">SEC02-BP03: Store and use secrets securely</a></li>
    <li><a href="./SEC02-BP04.html">SEC02-BP04: Rely on a centralized identity provider</a></li>
    <li><a href="./SEC02-BP05.html">SEC02-BP05: Audit and rotate credentials periodically</a></li>
    <li><a href="./SEC02-BP06.html">SEC02-BP06: Employ user groups and attributes</a></li>
  </ul>
</div>

## Key Concepts

### Identity Types and Management

**Human Identities**: People who need access to your AWS environment, including:
- Administrators who manage infrastructure and security
- Developers who build and deploy applications
- Operators who monitor and maintain systems
- End users who consume applications and services
- External partners and contractors with limited access needs

**Machine Identities**: Non-human entities that require access to AWS services:
- Applications and microservices
- CI/CD pipelines and automation tools
- Monitoring and logging systems
- Backup and disaster recovery processes
- Third-party integrations and APIs

### Authentication Fundamentals

**Strong Authentication**: Multi-factor authentication (MFA) combining something you know (password), something you have (device), and something you are (biometrics).

**Temporary Credentials**: Short-lived credentials that automatically expire, reducing the risk of credential compromise and eliminating the need for credential rotation.

**Centralized Identity Management**: Single source of truth for identity information, enabling consistent authentication policies and simplified user lifecycle management.

**Zero Trust Authentication**: Verify every authentication request regardless of location or previous authentication status.

## AWS Services to Consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS IAM Identity Center</h4>
    <p>Helps you securely create or connect your workforce identities and manage their access centrally across AWS accounts and applications. Ideal for managing human user authentication at scale.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Identity and Access Management (IAM)</h4>
    <p>Enables you to manage access to AWS services and resources securely. Core service for managing both human and machine identities with fine-grained access control.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon Cognito</h4>
    <p>Provides authentication, authorization, and user management for your web and mobile apps. Ideal for managing end-user authentication in customer-facing applications.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Secrets Manager</h4>
    <p>Helps you protect secrets needed to access your applications, services, and IT resources. Enables automatic rotation and secure storage of credentials.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Directory Service</h4>
    <p>Provides multiple ways to use Microsoft Active Directory (AD) with other AWS services. Enables integration with existing enterprise identity systems.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Security Token Service (STS)</h4>
    <p>Enables you to request temporary, limited-privilege credentials for IAM users or for users that you authenticate (federated users). Essential for implementing temporary credential strategies.</p>
  </div>
</div>

## Implementation Approach

### 1. Identity Strategy and Planning
- Inventory all human and machine identities in your environment
- Define authentication requirements for different identity types
- Choose appropriate identity providers for your organization
- Plan integration with existing identity systems
- Establish identity governance policies and procedures

### 2. Human Identity Management
- Implement centralized identity provider (AWS IAM Identity Center or external IdP)
- Configure multi-factor authentication for all human users
- Set up single sign-on (SSO) for AWS and applications
- Implement role-based access control aligned with job functions
- Establish user lifecycle management processes

### 3. Machine Identity Management
- Replace long-term credentials with IAM roles where possible
- Implement service-to-service authentication using IAM roles
- Secure application secrets using AWS Secrets Manager
- Configure automatic credential rotation for necessary secrets
- Implement least privilege access for all machine identities

### 4. Authentication Security Controls
- Enforce strong password policies and MFA requirements
- Implement conditional access based on risk factors
- Monitor authentication events and detect anomalies
- Establish incident response procedures for identity compromise
- Regular audit and review of authentication configurations

## Authentication Architecture Patterns

### Workforce Identity Federation
```
Corporate Identity Provider (Active Directory/Okta/Azure AD)
    ↓ SAML/OIDC Federation
AWS IAM Identity Center
    ↓ Temporary Credentials
AWS Services and Applications
```

### Application Authentication Flow
```
Application
    ↓ Assume Role
AWS IAM Role (with policies)
    ↓ Temporary Credentials
AWS Services (S3, RDS, etc.)
```

### Customer Identity Management
```
Customer Application
    ↓ Authentication
Amazon Cognito User Pool
    ↓ JWT Tokens
Application Backend
    ↓ IAM Role
AWS Services
```

## Security Controls Framework

### Preventive Controls
- **Strong Authentication**: MFA, strong passwords, biometric authentication
- **Access Policies**: Least privilege, time-based access, conditional access
- **Credential Management**: Temporary credentials, automatic rotation, secure storage
- **Network Controls**: IP restrictions, VPN requirements, device compliance

### Detective Controls
- **Authentication Monitoring**: Login attempts, unusual access patterns, failed authentications
- **Credential Usage Tracking**: API calls, resource access, privilege escalation attempts
- **Compliance Monitoring**: Policy violations, configuration drift, unauthorized changes
- **Threat Detection**: Compromised credentials, insider threats, external attacks

### Responsive Controls
- **Incident Response**: Credential compromise procedures, account lockout, emergency access
- **Automated Remediation**: Suspicious activity response, policy enforcement, access revocation
- **Recovery Procedures**: Account restoration, credential reset, access re-establishment
- **Communication**: User notifications, security team alerts, management reporting

## Common Challenges and Solutions

### Challenge: Password Fatigue and Weak Passwords
**Solution**: Implement single sign-on (SSO) to reduce password burden, enforce strong password policies, and require multi-factor authentication for all accounts.

### Challenge: Long-term Credential Management
**Solution**: Replace long-term credentials with temporary credentials using IAM roles, implement automatic credential rotation, and use managed services for credential storage.

### Challenge: Identity Sprawl Across Multiple Systems
**Solution**: Implement centralized identity management with federation, standardize on common identity providers, and establish consistent authentication policies.

### Challenge: Machine Identity Security
**Solution**: Use IAM roles for service-to-service authentication, implement least privilege access, and regularly audit machine identity permissions.

### Challenge: Third-party Integration Security
**Solution**: Use external IDs for cross-account access, implement time-limited access, and apply additional monitoring for third-party activities.

## Authentication Maturity Levels

### Level 1: Basic Authentication
- Username and password authentication
- Manual user provisioning and deprovisioning
- Basic logging of authentication events
- Individual account management

### Level 2: Enhanced Authentication
- Multi-factor authentication implemented
- Centralized identity provider in use
- Automated user lifecycle management
- Role-based access control

### Level 3: Advanced Authentication
- Single sign-on across all systems
- Risk-based authentication and conditional access
- Automated credential rotation and management
- Comprehensive authentication monitoring

### Level 4: Intelligent Authentication
- AI/ML-powered risk assessment
- Behavioral authentication patterns
- Predictive threat detection
- Automated response to authentication anomalies

## Best Practices Summary

### For Human Identities:
1. **Centralize Identity Management**: Use AWS IAM Identity Center or integrate with existing identity providers
2. **Enforce Strong Authentication**: Require MFA for all human users
3. **Implement SSO**: Reduce password fatigue and improve user experience
4. **Use Temporary Credentials**: Avoid long-term access keys for human users
5. **Regular Access Reviews**: Periodically review and validate user access

### For Machine Identities:
1. **Use IAM Roles**: Replace long-term credentials with IAM roles wherever possible
2. **Secure Secret Storage**: Use AWS Secrets Manager for necessary secrets
3. **Implement Rotation**: Automatically rotate credentials that cannot be replaced with roles
4. **Least Privilege**: Grant only the minimum permissions required
5. **Monitor Usage**: Track and audit machine identity access patterns

## Related resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html">AWS Well-Architected Framework - Security Pillar</a></li>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/sec-02.html">SEC02: How do you manage authentication for people and machines?</a></li>
    <li><a href="https://docs.aws.amazon.com/singlesignon/latest/userguide/what-is.html">AWS IAM Identity Center User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html">Security best practices in IAM</a></li>
    <li><a href="https://aws.amazon.com/identity/">AWS Identity Solutions</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/">AWS Security Blog</a></li>
    <li><a href="https://docs.aws.amazon.com/cognito/latest/developerguide/what-is-amazon-cognito.html">Amazon Cognito Developer Guide</a></li>
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
