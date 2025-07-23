---
title: SEC02-BP04 - Rely on a centralized identity provider
layout: default
parent: SEC02 - How do you manage identities for people and machines?
grand_parent: Security
nav_order: 4
---

<div class="pillar-header">
  <h1>SEC02-BP04: Rely on a centralized identity provider</h1>
  <p>For workforce identities (your employees, contractors, and partners), rely on an identity provider that enables you to manage identities in a centralized place. This makes it easier to manage access across multiple applications and services because you are creating, managing, and revoking access from a single location.</p>
</div>

## Implementation guidance

Centralizing identity management provides numerous benefits, including simplified user management, consistent security policies, and improved user experience. By using a centralized identity provider, you can manage access across multiple AWS accounts and applications from a single location.

### Key steps for implementing this best practice:

1. **Choose a centralized identity provider**:
   - Use AWS IAM Identity Center as your primary identity provider
   - Or integrate with your existing identity provider:
     - Microsoft Active Directory (on-premises or AWS Managed Microsoft AD)
     - Azure Active Directory (Microsoft Entra ID)
     - Okta, Ping Identity, or other SAML 2.0 compatible providers
   - Consider your organization's existing investments and requirements
   - Evaluate features like MFA support, user lifecycle management, and reporting capabilities

2. **Configure federation between AWS and your identity provider**:
   - Set up SAML 2.0 federation
   - Configure attribute mapping to pass user attributes to AWS
   - Establish trust relationships between your identity provider and AWS
   - Test the federation setup with sample users
   - Document the federation configuration

3. **Implement single sign-on (SSO)**:
   - Enable SSO for AWS Management Console access
   - Configure SSO for AWS CLI and SDK access
   - Extend SSO to other business applications
   - Implement consistent authentication policies
   - Provide user training on SSO usage

4. **Manage user lifecycle centrally**:
   - Implement automated user provisioning and deprovisioning
   - Synchronize user attributes and group memberships
   - Establish processes for handling user role changes
   - Implement regular access reviews
   - Create procedures for emergency access management

5. **Apply consistent security policies**:
   - Enforce MFA through your identity provider
   - Implement consistent password policies
   - Apply conditional access policies based on user, device, and network context
   - Standardize session duration and timeout settings
   - Implement risk-based authentication where appropriate

6. **Monitor and audit identity activities**:
   - Set up centralized logging for authentication events
   - Monitor for suspicious login attempts
   - Create alerts for unusual access patterns
   - Implement regular access reviews
   - Generate compliance reports for identity management

## Implementation examples

### Example 1: Setting up AWS IAM Identity Center with AWS Organizations

```bash
# Enable AWS IAM Identity Center
aws organizations enable-aws-service-access --service-principal sso.amazonaws.com

# Create an IAM Identity Center instance
aws sso-admin create-instance --name "MyCompanyIdentityCenter" --tags Key=Environment,Value=Production

# Create a permission set
aws sso-admin create-permission-set \
  --instance-arn "arn:aws:sso:::instance/ssoins-1234567890abcdef" \
  --name "DeveloperAccess" \
  --description "Developer access to AWS resources" \
  --session-duration "PT8H"

# Attach an AWS managed policy to the permission set
aws sso-admin attach-managed-policy-to-permission-set \
  --instance-arn "arn:aws:sso:::instance/ssoins-1234567890abcdef" \
  --permission-set-arn "arn:aws:sso:::permissionSet/ssoins-1234567890abcdef/ps-1234567890abcdef" \
  --managed-policy-arn "arn:aws:iam::aws:policy/PowerUserAccess"
```

### Example 2: Configuring SAML federation with an external identity provider

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::123456789012:saml-provider/ExternalIdP"
      },
      "Action": "sts:AssumeRoleWithSAML",
      "Condition": {
        "StringEquals": {
          "SAML:aud": "https://signin.aws.amazon.com/saml"
        }
      }
    }
  ]
}
```

```bash
# Create a SAML provider
aws iam create-saml-provider \
  --saml-metadata-document file://metadata.xml \
  --name ExternalIdP

# Create a role for federated users
aws iam create-role \
  --role-name SAMLFederationRole \
  --assume-role-policy-document file://trust-policy.json

# Attach a policy to the role
aws iam attach-role-policy \
  --role-name SAMLFederationRole \
  --policy-arn arn:aws:iam::aws:policy/ReadOnlyAccess
```

### Example 3: Setting up AWS Managed Microsoft AD and AWS IAM Identity Center

```bash
# Create an AWS Managed Microsoft AD directory
aws ds create-microsoft-ad \
  --name corp.example.com \
  --password "SecureP@ssw0rd" \
  --description "Corporate Directory" \
  --vpc-settings "VpcId=vpc-12345678,SubnetIds=subnet-1234567a,subnet-1234567b" \
  --edition Standard

# Configure AWS IAM Identity Center to use the directory
aws sso-admin create-instance --name "CorporateIdentityCenter" --tags Key=Environment,Value=Production

# Configure directory as identity source
aws identitystore connect-directory \
  --identity-store-id d-1234567890 \
  --directory-id d-abcdef1234
```

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
    <h4>AWS Organizations</h4>
    <p>Helps you centrally manage and govern your environment as you scale your AWS resources. Works with IAM Identity Center to provide centralized access management across multiple AWS accounts.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS CloudTrail</h4>
    <p>Records API calls for your account and delivers log files to you. Use CloudTrail to monitor identity-related activities and detect unauthorized access attempts.</p>
  </div>
</div>

## Benefits of relying on a centralized identity provider

- **Simplified user management**: Manage users in a single location instead of across multiple systems
- **Consistent security policies**: Apply security policies uniformly across all applications and services
- **Improved user experience**: Users have a single set of credentials for accessing multiple systems
- **Streamlined onboarding and offboarding**: Quickly provision and deprovision access across multiple systems
- **Enhanced security**: Enforce strong authentication and access policies from a central location
- **Reduced administrative overhead**: Eliminate the need to manage users in multiple systems
- **Improved compliance**: Centralized visibility and control over user access
- **Scalable access management**: Easily manage access as your organization and AWS footprint grows

## Related resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/sec_identities_identity_provider.html">AWS Well-Architected Framework - Rely on a centralized identity provider</a></li>
    <li><a href="https://docs.aws.amazon.com/singlesignon/latest/userguide/what-is.html">AWS IAM Identity Center User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers.html">Identity providers and federation in IAM</a></li>
    <li><a href="https://docs.aws.amazon.com/directoryservice/latest/admin-guide/what_is.html">AWS Directory Service Administration Guide</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/the-next-evolution-in-aws-single-sign-on/">The next evolution in AWS Single Sign-On</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-connect-saml-2-0-identity-providers-to-aws-iam-identity-center/">How to connect SAML 2.0 identity providers to AWS IAM Identity Center</a></li>
  </ul>
</div>
