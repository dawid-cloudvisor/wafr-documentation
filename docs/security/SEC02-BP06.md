---
title: SEC02-BP06 - Employ user groups and attributes
layout: default
parent: SEC02 - How do you manage authentication for people and machines?
grand_parent: Security
nav_order: 6
---

<div class="pillar-header">
  <h1>SEC02-BP06: Employ user groups and attributes</h1>
  <p>As the number of users you manage grows, you need to reduce the overhead of managing access. Place users with common security requirements in groups defined by your identity provider, and put mechanisms in place to ensure that user attributes that may be used for access control (such as department or location) are correct and updated.</p>
</div>

## Implementation guidance

Managing access for individual users becomes increasingly complex as your organization grows. By using groups and attributes, you can implement scalable access management that reduces administrative overhead and ensures consistent access control across your AWS environment.

### Key steps for implementing this best practice:

1. **Design your group structure**:
   - Identify common access patterns in your organization
   - Create groups based on job functions or roles
   - Consider organizational structure when designing groups
   - Plan for nested groups if supported by your identity provider
   - Document your group naming conventions and structure

2. **Implement attribute-based access control (ABAC)**:
   - Identify user attributes relevant for access control (department, job role, location, etc.)
   - Ensure attributes are correctly maintained in your identity provider
   - Map attributes from your identity provider to AWS
   - Design IAM policies that use attributes for access decisions
   - Test attribute-based policies with sample users

3. **Configure group-based access control (GBAC)**:
   - Create IAM roles that correspond to your groups
   - Define permission sets in AWS IAM Identity Center
   - Map groups to roles or permission sets
   - Implement least privilege access for each group
   - Regularly review group memberships and permissions

4. **Maintain group and attribute integrity**:
   - Implement processes for managing group membership
   - Automate group assignments based on user attributes where possible
   - Establish approval workflows for group membership changes
   - Regularly audit group memberships and user attributes
   - Implement controls to prevent unauthorized attribute changes

5. **Implement access governance**:
   - Conduct regular access reviews for groups
   - Document group purpose and access levels
   - Implement attestation processes for group memberships
   - Monitor for unusual group membership changes
   - Generate reports on group usage and membership

6. **Scale your approach**:
   - Design for growth in user numbers and complexity
   - Implement automation for group management
   - Use templates for common access patterns
   - Document processes for creating new groups
   - Regularly review and optimize your group structure

## Implementation examples

### Example 1: Attribute-based access control with IAM

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": [
        "arn:aws:s3:::${aws:PrincipalTag/Department}/*"
      ],
      "Condition": {
        "StringEquals": {
          "aws:PrincipalTag/JobFunction": "Developer"
        }
      }
    }
  ]
}
```

```bash
# Tag an IAM user with attributes
aws iam tag-user \
  --user-name johndoe \
  --tags '[{"Key": "Department", "Value": "Engineering"}, {"Key": "JobFunction", "Value": "Developer"}]'

# Create a role with a trust policy that allows users with specific tags
aws iam create-role \
  --role-name DeveloperRole \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": {"AWS": "arn:aws:iam::123456789012:root"},
        "Action": "sts:AssumeRole",
        "Condition": {
          "StringEquals": {
            "aws:PrincipalTag/JobFunction": "Developer"
          }
        }
      }
    ]
  }'
```

### Example 2: Group-based access with AWS IAM Identity Center

```bash
# Create a group in IAM Identity Center
aws identitystore create-group \
  --identity-store-id d-1234567890 \
  --display-name "Developers" \
  --description "Software development team"

# Create a permission set
aws sso-admin create-permission-set \
  --instance-arn "arn:aws:sso:::instance/ssoins-1234567890abcdef" \
  --name "DeveloperAccess" \
  --description "Access for software developers" \
  --session-duration "PT8H"

# Attach an AWS managed policy to the permission set
aws sso-admin attach-managed-policy-to-permission-set \
  --instance-arn "arn:aws:sso:::instance/ssoins-1234567890abcdef" \
  --permission-set-arn "arn:aws:sso:::permissionSet/ssoins-1234567890abcdef/ps-1234567890abcdef" \
  --managed-policy-arn "arn:aws:iam::aws:policy/PowerUserAccess"

# Provision the permission set to an account for the group
aws sso-admin create-account-assignment \
  --instance-arn "arn:aws:sso:::instance/ssoins-1234567890abcdef" \
  --target-id "123456789012" \
  --target-type "AWS_ACCOUNT" \
  --permission-set-arn "arn:aws:sso:::permissionSet/ssoins-1234567890abcdef/ps-1234567890abcdef" \
  --principal-id "g-1234567890abcdef" \
  --principal-type "GROUP"
```

### Example 3: SAML attribute mapping for AWS access

```json
{
  "Rules": [
    {
      "Name": "RoleSessionName",
      "Rule": "user.email"
    },
    {
      "Name": "Department",
      "Rule": "user.department"
    },
    {
      "Name": "JobFunction",
      "Rule": "user.jobTitle"
    },
    {
      "Name": "CostCenter",
      "Rule": "user.costCenter"
    }
  ],
  "Version": "2012-10-17"
}
```

```bash
# Create a SAML provider with attribute mapping
aws iam create-saml-provider \
  --saml-metadata-document file://metadata.xml \
  --name ExternalIdP \
  --tags Key=Environment,Value=Production

# Update an existing SAML provider with attribute mapping
aws iam update-saml-provider \
  --saml-metadata-document file://metadata.xml \
  --saml-provider-arn arn:aws:iam::123456789012:saml-provider/ExternalIdP
```

## AWS services to consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS IAM Identity Center</h4>
    <p>Helps you securely create or connect your workforce identities and manage their access centrally across AWS accounts and applications. Supports group-based access management and attribute-based access control.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Identity and Access Management (IAM)</h4>
    <p>Enables you to manage access to AWS services and resources securely. Supports attribute-based access control through principal tags and resource tags.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Directory Service</h4>
    <p>Provides multiple ways to use Microsoft Active Directory (AD) with other AWS services. Supports group management and attribute synchronization from your directory.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Organizations</h4>
    <p>Helps you centrally manage and govern your environment as you scale your AWS resources. Works with IAM Identity Center to provide group-based access across multiple AWS accounts.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS CloudTrail</h4>
    <p>Records API calls for your account and delivers log files to you. Use CloudTrail to monitor group membership changes and attribute modifications.</p>
  </div>
</div>

## Benefits of employing user groups and attributes

- **Simplified access management**: Manage access for groups of users rather than individuals
- **Consistent access control**: Apply the same permissions to all users with similar roles
- **Reduced administrative overhead**: Update permissions for multiple users at once
- **Scalable access management**: Easily manage access as your organization grows
- **Dynamic access control**: Use attributes to make access decisions based on user characteristics
- **Improved security governance**: Easier to audit and review access when organized by groups
- **Streamlined onboarding**: Quickly grant appropriate access to new users by adding them to groups

## Related resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/sec_identities_groups_attributes.html">AWS Well-Architected Framework - Employ user groups and attributes</a></li>
    <li><a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html">Tagging IAM resources</a></li>
    <li><a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/access_iam-tags.html">Controlling access to AWS resources using tags</a></li>
    <li><a href="https://docs.aws.amazon.com/singlesignon/latest/userguide/attributemappingsconcept.html">Attribute mappings in AWS IAM Identity Center</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/attribute-based-access-control-with-aws-iam-identity-center/">Attribute-based access control with AWS IAM Identity Center</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-implement-saml-session-tags-for-abac-in-aws-iam-identity-center/">How to implement SAML session tags for ABAC in AWS IAM Identity Center</a></li>
  </ul>
</div>
