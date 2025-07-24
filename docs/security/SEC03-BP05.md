---
title: SEC03-BP05 - Define permission guardrails for your organization
layout: default
parent: SEC03 - How do you manage permissions for people and machines?
grand_parent: Security
nav_order: 5
---

<div class="pillar-header">
  <h1>SEC03-BP05: Define permission guardrails for your organization</h1>
  <p>Establish common controls that restrict access to all identities in your organization. For example, you can restrict access to specific AWS Regions, or prevent your team from deleting common resources, such as an IAM role used for your central security team.</p>
</div>

## Implementation guidance

Permission guardrails are organization-wide controls that establish boundaries for what actions can be performed by any identity in your AWS environment. These guardrails help ensure consistent security policies across all accounts and prevent accidental or malicious actions that could compromise your security posture.

### Key steps for implementing this best practice:

1. **Identify organizational security requirements**:
   - Define security policies that apply across all accounts
   - Identify actions that should be restricted organization-wide
   - Determine which AWS services should be allowed or denied
   - Establish data residency and compliance requirements
   - Document emergency access exceptions

2. **Implement Service Control Policies (SCPs)**:
   - Create SCPs to enforce organization-wide restrictions
   - Apply SCPs at the organization, organizational unit (OU), or account level
   - Use deny policies to restrict dangerous actions
   - Implement allow lists for approved services and regions
   - Test SCPs in non-production environments first

3. **Define permission boundaries**:
   - Create permission boundaries for IAM roles and users
   - Establish maximum permissions that can be granted
   - Implement boundaries for different types of workloads
   - Use boundaries to prevent privilege escalation
   - Document boundary policies and their purpose

4. **Implement resource-based policies**:
   - Use resource-based policies for additional access control
   - Implement cross-account access restrictions
   - Define policies for sensitive resources like KMS keys
   - Establish bucket policies for S3 resources
   - Use resource policies to enforce encryption requirements

5. **Monitor and enforce compliance**:
   - Set up monitoring for policy violations
   - Implement automated remediation for non-compliant resources
   - Create alerts for attempts to bypass guardrails
   - Regularly audit guardrail effectiveness
   - Generate compliance reports for management

6. **Maintain and update guardrails**:
   - Regularly review and update guardrail policies
   - Adapt guardrails to new services and features
   - Incorporate lessons learned from security incidents
   - Update guardrails based on changing business requirements
   - Document changes and their rationale

## Implementation examples

### Example 1: Service Control Policy to restrict regions and prevent security role deletion

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "RestrictRegions",
      "Effect": "Deny",
      "Action": "*",
      "Resource": "*",
      "Condition": {
        "StringNotEquals": {
          "aws:RequestedRegion": [
            "us-east-1",
            "us-west-2",
            "eu-west-1"
          ]
        }
      }
    },
    {
      "Sid": "PreventSecurityRoleDeletion",
      "Effect": "Deny",
      "Action": [
        "iam:DeleteRole",
        "iam:DetachRolePolicy",
        "iam:DeleteRolePolicy"
      ],
      "Resource": [
        "arn:aws:iam::*:role/SecurityAuditRole",
        "arn:aws:iam::*:role/SecurityTeamRole",
        "arn:aws:iam::*:role/OrganizationAccountAccessRole"
      ]
    },
    {
      "Sid": "PreventCloudTrailDisabling",
      "Effect": "Deny",
      "Action": [
        "cloudtrail:StopLogging",
        "cloudtrail:DeleteTrail",
        "cloudtrail:PutEventSelectors"
      ],
      "Resource": "*"
    },
    {
      "Sid": "RequireEncryptionForS3",
      "Effect": "Deny",
      "Action": "s3:PutObject",
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

### Example 2: Permission boundary for developer roles

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowedServices",
      "Effect": "Allow",
      "Action": [
        "ec2:*",
        "s3:*",
        "rds:*",
        "lambda:*",
        "cloudwatch:*",
        "logs:*",
        "dynamodb:*"
      ],
      "Resource": "*"
    },
    {
      "Sid": "DenyIAMActions",
      "Effect": "Deny",
      "Action": [
        "iam:*",
        "organizations:*",
        "account:*"
      ],
      "Resource": "*"
    },
    {
      "Sid": "DenyProductionAccess",
      "Effect": "Deny",
      "Action": "*",
      "Resource": "*",
      "Condition": {
        "StringEquals": {
          "aws:ResourceTag/Environment": "Production"
        }
      }
    },
    {
      "Sid": "RequireMFAForSensitiveActions",
      "Effect": "Deny",
      "Action": [
        "ec2:TerminateInstances",
        "rds:DeleteDBInstance",
        "s3:DeleteBucket"
      ],
      "Resource": "*",
      "Condition": {
        "BoolIfExists": {
          "aws:MultiFactorAuthPresent": "false"
        }
      }
    }
  ]
}
```

### Example 3: AWS Config rules for guardrail compliance

```bash
# Create Config rule to ensure S3 buckets are encrypted
aws configservice put-config-rule --config-rule '{
  "ConfigRuleName": "s3-bucket-server-side-encryption-enabled",
  "Description": "Checks that your Amazon S3 bucket either has S3 default encryption enabled or that the S3 bucket policy explicitly denies put-object requests without server side encryption.",
  "Source": {
    "Owner": "AWS",
    "SourceIdentifier": "S3_BUCKET_SERVER_SIDE_ENCRYPTION_ENABLED"
  },
  "Scope": {
    "ComplianceResourceTypes": ["AWS::S3::Bucket"]
  }
}'

# Create Config rule to ensure CloudTrail is enabled
aws configservice put-config-rule --config-rule '{
  "ConfigRuleName": "cloudtrail-enabled",
  "Description": "Checks whether AWS CloudTrail is enabled in your AWS account.",
  "Source": {
    "Owner": "AWS",
    "SourceIdentifier": "CLOUD_TRAIL_ENABLED"
  }
}'

# Create Config rule to check for root access key usage
aws configservice put-config-rule --config-rule '{
  "ConfigRuleName": "root-access-key-check",
  "Description": "Checks whether the root user access key is available. The rule is compliant if the user access key does not exist.",
  "Source": {
    "Owner": "AWS",
    "SourceIdentifier": "ROOT_ACCESS_KEY_CHECK"
  }
}'

# Set up remediation configuration for non-compliant resources
aws configservice put-remediation-configuration --remediation-configuration '{
  "ConfigRuleName": "s3-bucket-server-side-encryption-enabled",
  "TargetType": "SSM_DOCUMENT",
  "TargetId": "AWSConfigRemediation-EnableS3BucketDefaultEncryption",
  "TargetVersion": "1",
  "Parameters": {
    "AutomationAssumeRole": {
      "StaticValue": {
        "Values": ["arn:aws:iam::123456789012:role/ConfigRemediationRole"]
      }
    },
    "BucketName": {
      "ResourceValue": {
        "Value": "RESOURCE_ID"
      }
    }
  },
  "Automatic": true,
  "MaximumAutomaticAttempts": 3
}'
```

## AWS services to consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Organizations</h4>
    <p>Helps you centrally manage and govern your environment as you scale your AWS resources. Use Service Control Policies (SCPs) to implement organization-wide permission guardrails.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Identity and Access Management (IAM)</h4>
    <p>Enables you to manage access to AWS services and resources securely. Use permission boundaries and policies to implement guardrails at the identity level.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Config</h4>
    <p>Enables you to assess, audit, and evaluate the configurations of your AWS resources. Use Config rules to monitor compliance with your guardrail policies.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Control Tower</h4>
    <p>Provides a simplified way to set up and govern a secure, multi-account AWS environment based on best practices. Includes pre-built guardrails for common security requirements.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS CloudTrail</h4>
    <p>Records API calls for your account and delivers log files to you. Use CloudTrail to monitor attempts to bypass guardrails and detect policy violations.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon EventBridge</h4>
    <p>A serverless event bus that makes it easy to connect applications together using data from your own applications, integrated Software-as-a-Service (SaaS) applications, and AWS services. Use EventBridge to trigger automated responses to guardrail violations.</p>
  </div>
</div>

## Benefits of defining permission guardrails

- **Consistent security posture**: Ensures uniform security policies across all accounts and workloads
- **Reduced risk of security incidents**: Prevents dangerous actions that could compromise security
- **Simplified compliance**: Helps meet regulatory requirements through automated enforcement
- **Operational efficiency**: Reduces the need for manual security reviews and interventions
- **Scalable governance**: Provides a framework that scales with organizational growth
- **Proactive protection**: Prevents security issues before they can occur
- **Clear boundaries**: Establishes clear expectations for what actions are allowed

## Related resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/sec_permissions_define_guardrails.html">AWS Well-Architected Framework - Define permission guardrails for your organization</a></li>
    <li><a href="https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html">Service control policies (SCPs)</a></li>
    <li><a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html">Permissions boundaries for IAM entities</a></li>
    <li><a href="https://docs.aws.amazon.com/controltower/latest/userguide/guardrails.html">Guardrails in AWS Control Tower</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-use-service-control-policies-to-set-permission-guardrails-across-accounts-in-your-aws-organization/">How to use service control policies to set permission guardrails across accounts in your AWS organization</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-use-aws-iam-access-analyzer-to-set-permission-guardrails/">How to use AWS IAM Access Analyzer to set permission guardrails</a></li>
  </ul>
</div>
