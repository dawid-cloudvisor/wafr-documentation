---
title: SEC03-BP02 - Grant least privilege access
layout: default
parent: SEC03 - How do you manage permissions for people and machines?
grand_parent: Security
nav_order: 2
---

<div class="pillar-header">
  <h1>SEC03-BP02: Grant least privilege access</h1>
  <p>Grant only the access that identities require by allowing access to specific actions on specific AWS resources under specific conditions. Rely on groups and identity attributes to dynamically set permissions at scale, rather than defining permissions for individual users. For example, you can allow a group of developers access to manage only resources for their project. This way, when a developer is removed from the group, access for the developer is revoked everywhere that the group was used for access control, without requiring updates to the access policies.</p>
</div>

## Implementation guidance

The principle of least privilege is a fundamental security concept that involves granting only the minimum permissions necessary to perform a task. By implementing least privilege access, you can significantly reduce the risk of unauthorized access and limit the potential impact of security incidents.

### Key steps for implementing this best practice:

1. **Start with minimum permissions**:
   - Begin with no permissions and add them as needed
   - Use explicit deny policies to restrict sensitive actions
   - Implement permission boundaries to limit maximum permissions
   - Avoid using wildcard permissions (e.g., `*`) in policies
   - Regularly review and remove unused permissions

2. **Implement attribute-based access control (ABAC)**:
   - Use tags on resources and principals for dynamic access control
   - Define policies based on attributes rather than individual identities
   - Implement consistent tagging strategies across your organization
   - Use conditions in policies to enforce attribute-based restrictions
   - Document your ABAC strategy and implementation

3. **Leverage IAM Access Analyzer**:
   - Use IAM Access Analyzer to identify unused permissions
   - Generate least privilege policies based on access activity
   - Regularly review findings and refine permissions
   - Implement automated remediation for overly permissive policies
   - Monitor for policy changes that increase permissions

4. **Implement time-bound permissions**:
   - Grant temporary access for specific tasks
   - Use IAM roles with session policies for temporary elevated access
   - Implement automated expiration for temporary permissions
   - Require justification for access requests
   - Log and monitor temporary access usage

5. **Use permission guardrails**:
   - Implement Service Control Policies (SCPs) to set organization-wide guardrails
   - Use permission boundaries to limit maximum permissions for roles
   - Create IAM policy conditions to restrict access based on context
   - Implement resource-based policies for additional access control
   - Regularly review and update guardrails

6. **Continuously refine permissions**:
   - Monitor access patterns and usage
   - Identify and remove unused permissions
   - Adjust permissions based on changing requirements
   - Implement regular access reviews
   - Use automated tools to suggest permission refinements

## Implementation examples

### Example 1: Least privilege IAM policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowSpecificEC2Actions",
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeInstances",
        "ec2:StartInstances",
        "ec2:StopInstances"
      ],
      "Resource": "arn:aws:ec2:us-west-2:123456789012:instance/i-*",
      "Condition": {
        "StringEquals": {
          "aws:ResourceTag/Environment": "Development",
          "aws:PrincipalTag/Role": "Developer"
        }
      }
    },
    {
      "Sid": "DenyProductionAccess",
      "Effect": "Deny",
      "Action": "ec2:*",
      "Resource": "*",
      "Condition": {
        "StringEquals": {
          "aws:ResourceTag/Environment": "Production"
        }
      }
    }
  ]
}
```

### Example 2: Attribute-based access control (ABAC)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::${aws:PrincipalTag/Project}/*",
        "arn:aws:s3:::${aws:PrincipalTag/Project}"
      ],
      "Condition": {
        "StringEquals": {
          "s3:ResourceTag/Project": "${aws:PrincipalTag/Project}"
        }
      }
    }
  ]
}
```

### Example 3: Permission boundary

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:*",
        "cloudwatch:*",
        "ec2:*"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Deny",
      "Action": [
        "iam:*",
        "organizations:*",
        "kms:*"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Deny",
      "Action": "*",
      "Resource": "*",
      "Condition": {
        "StringNotEquals": {
          "aws:ResourceTag/Environment": "${aws:PrincipalTag/Environment}"
        }
      }
    }
  ]
}
```

### Example 4: Using IAM Access Analyzer to generate least privilege policies

```bash
# Generate a policy based on access activity
aws accessanalyzer start-policy-generation \
  --policy-generation-details '{
    "principalArn": "arn:aws:iam::123456789012:role/ExampleRole"
  }' \
  --policy-type SERVICE_CONTROL_POLICY

# Retrieve the generated policy
aws accessanalyzer get-generated-policy \
  --job-id a1b2c3d4-5678-90ab-cdef-EXAMPLE11111

# List unused access for a role
aws accessanalyzer start-resource-scan \
  --resource-arn arn:aws:iam::123456789012:role/ExampleRole \
  --resource-owner SELF

# Get the results of the resource scan
aws accessanalyzer get-finding \
  --analyzer-arn arn:aws:access-analyzer:us-west-2:123456789012:analyzer/MyAnalyzer \
  --id a1b2c3d4-5678-90ab-cdef-EXAMPLE22222
```

## AWS services to consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS IAM Access Analyzer</h4>
    <p>Helps you identify resources in your organization and accounts that are shared with an external entity. Also helps identify unused access and generate least privilege policies based on access activity.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Identity and Access Management (IAM)</h4>
    <p>Enables you to manage access to AWS services and resources securely. Use IAM policies, roles, and permission boundaries to implement least privilege access.</p>
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
    <h4>AWS CloudTrail</h4>
    <p>Records API calls for your account and delivers log files to you. Use CloudTrail to monitor access patterns and identify opportunities to refine permissions.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon CloudWatch</h4>
    <p>Monitors your AWS resources and the applications you run on AWS in real time. Set up alerts for suspicious access patterns or policy changes that increase permissions.</p>
  </div>
</div>

## Benefits of granting least privilege access

- **Reduced attack surface**: Minimizes the potential impact of compromised credentials
- **Improved security posture**: Limits the actions that can be performed by any identity
- **Enhanced compliance**: Supports regulatory requirements for access control
- **Better visibility**: Makes it easier to understand who has access to what
- **Simplified auditing**: Clearer access patterns make auditing more straightforward
- **Reduced risk of accidental changes**: Limits the potential for unintended modifications
- **Improved detection of malicious activity**: Unusual access attempts are more visible

## Related resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/sec_permissions_least_privileges.html">AWS Well-Architected Framework - Grant least privilege access</a></li>
    <li><a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html#grant-least-privilege">IAM best practices: Grant least privilege</a></li>
    <li><a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html">Permissions boundaries for IAM entities</a></li>
    <li><a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/tutorial_attribute-based-access-control.html">Tutorial: Define permissions to access AWS resources based on tags</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/techniques-for-writing-least-privilege-iam-policies/">Techniques for writing least privilege IAM policies</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/iam-access-analyzer-makes-it-easier-to-implement-least-privilege-permissions-by-generating-iam-policies-based-on-access-activity/">IAM Access Analyzer makes it easier to implement least privilege permissions</a></li>
  </ul>
</div>
