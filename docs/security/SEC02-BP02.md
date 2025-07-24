---
title: SEC02-BP02 - Use temporary credentials
layout: default
parent: SEC02 - How do you manage authentication for people and machines?
grand_parent: Security
nav_order: 2
---

<div class="pillar-header">
  <h1>SEC02-BP02: Use temporary credentials</h1>
  <p>Require identities to dynamically acquire temporary credentials. For workforce identities, use AWS IAM Identity Center, or a federation with IAM roles to access AWS accounts. For machine identities, require the use of IAM roles instead of IAM users with long-term access keys.</p>
</div>

## Implementation guidance

Temporary credentials provide enhanced security compared to long-term credentials because they have a limited lifetime and don't need to be stored or managed by the user. By implementing temporary credentials, you can reduce the risk of unauthorized access due to compromised credentials and simplify credential management.

### Key steps for implementing this best practice:

1. **Implement IAM roles for human access**:
   - Use AWS IAM Identity Center for workforce identities
   - Configure federation with your existing identity provider
   - Set up IAM roles with appropriate permissions
   - Define appropriate session durations
   - Implement role-based access control (RBAC)

2. **Implement IAM roles for machine access**:
   - Use IAM roles for EC2 instances
   - Implement service-linked roles for AWS services
   - Use IAM roles for tasks and containers
   - Configure appropriate trust relationships
   - Apply the principle of least privilege

3. **Implement IAM roles for cross-account access**:
   - Define roles for cross-account access
   - Configure appropriate trust relationships
   - Use external IDs for third-party access
   - Implement appropriate permission boundaries
   - Monitor cross-account role usage

4. **Phase out long-term credentials**:
   - Identify and inventory all long-term credentials
   - Create a migration plan to temporary credentials
   - Implement monitoring for long-term credential usage
   - Establish policies prohibiting new long-term credentials
   - Regularly audit and remove unused long-term credentials

5. **Implement credential monitoring and rotation**:
   - Monitor credential usage with AWS CloudTrail
   - Set up alerts for suspicious credential usage
   - Implement automated credential rotation where long-term credentials are necessary
   - Use AWS Secrets Manager for managing any required secrets
   - Regularly audit credential usage

6. **Educate users and developers**:
   - Train users on how to use temporary credentials
   - Provide developers with examples and tools for implementing temporary credentials
   - Document best practices for different use cases
   - Create clear procedures for exceptional cases
   - Regularly review and update guidance

## Implementation examples

### Example 1: Assuming an IAM role using the AWS CLI

```bash
# Assume a role and get temporary credentials
aws sts assume-role \
  --role-arn arn:aws:iam::123456789012:role/MyRole \
  --role-session-name MySession

# Configure AWS CLI to use temporary credentials
aws configure set aws_access_key_id ASIA1234567890EXAMPLE
aws configure set aws_secret_access_key 9drTJvcXLB89EXAMPLEKEY
aws configure set aws_session_token AQoEXAMPLEH4aoAH0gNCAPy...truncated
```

### Example 2: IAM role for EC2 instance

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::my-bucket",
        "arn:aws:s3:::my-bucket/*"
      ]
    }
  ]
}
```

```bash
# Attach the role to an EC2 instance
aws ec2 associate-iam-instance-profile \
  --instance-id i-1234567890abcdef0 \
  --iam-instance-profile Name=MyInstanceProfile
```

### Example 3: Cross-account role with external ID

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::123456789012:root"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "sts:ExternalId": "UniqueExternalId123"
        }
      }
    }
  ]
}
```

```bash
# Assume a cross-account role with external ID
aws sts assume-role \
  --role-arn arn:aws:iam::987654321098:role/CrossAccountRole \
  --role-session-name CrossAccountSession \
  --external-id UniqueExternalId123
```

## AWS services to consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS IAM Identity Center</h4>
    <p>Helps you securely create or connect your workforce identities and manage their access centrally across AWS accounts and applications. Provides temporary credentials for AWS account access.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Identity and Access Management (IAM)</h4>
    <p>Enables you to manage access to AWS services and resources securely. Supports IAM roles for temporary credentials and federation with external identity providers.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Security Token Service (STS)</h4>
    <p>Enables you to request temporary, limited-privilege credentials for IAM users or for users that you authenticate (federated users). Provides APIs for assuming roles and federating identities.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Secrets Manager</h4>
    <p>Helps you protect secrets needed to access your applications, services, and IT resources. Enables you to rotate, manage, and retrieve database credentials, API keys, and other secrets throughout their lifecycle.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS CloudTrail</h4>
    <p>Records API calls for your account and delivers log files to you. Use CloudTrail to monitor credential usage and detect unauthorized access attempts.</p>
  </div>
</div>

## Benefits of using temporary credentials

- **Enhanced security**: Temporary credentials have a limited lifetime, reducing the risk of credential compromise
- **Simplified management**: No need to store, rotate, or manage long-term credentials
- **Automatic expiration**: Credentials automatically expire after a defined period
- **Dynamic permissions**: Permissions can be dynamically assigned based on context
- **Reduced attack surface**: Eliminates the risk of long-term credential exposure
- **Improved auditability**: Easier to track and audit credential usage
- **Centralized control**: Manage access from a central location

## Related resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/sec_identities_unique.html">AWS Well-Architected Framework - Use temporary credentials</a></li>
    <li><a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use.html">Using IAM roles</a></li>
    <li><a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp.html">Temporary security credentials in IAM</a></li>
    <li><a href="https://docs.aws.amazon.com/singlesignon/latest/userguide/what-is.html">AWS IAM Identity Center User Guide</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-use-aws-iam-role-credentials-for-sql-server-authentication/">How to use AWS IAM role credentials for SQL Server authentication</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-use-external-id-when-granting-access-to-your-aws-resources/">How to use external ID when granting access to your AWS resources</a></li>
  </ul>
</div>
