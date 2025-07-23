---
title: SEC01-BP05 - Reduce security management scope
layout: default
parent: SEC01 - How do you securely operate your workload?
grand_parent: Security
nav_order: 5
---

<div class="pillar-header">
  <h1>SEC01-BP05: Reduce security management scope</h1>
  <p>Reduce security management scope by minimizing the number of security tooling and processes that you need to maintain. For example, if you have multiple security tools that provide similar capabilities, evaluate if there is a compelling reason to maintain multiple tools.</p>
</div>

## Implementation guidance

Reducing security management scope helps you focus your security efforts, minimize complexity, and improve operational efficiency. By consolidating security tools and processes, you can reduce overhead, improve visibility, and enhance your overall security posture.

### Key steps for implementing this best practice:

1. **Inventory your security tools and processes**:
   - Document all security tools currently in use across your organization
   - Identify overlapping functionality between tools
   - Map tools to security requirements and compliance needs
   - Determine which tools are essential and which are redundant

2. **Consolidate security tooling**:
   - Evaluate AWS-native security services that can replace third-party tools
   - Prioritize tools that integrate well with your AWS environment
   - Consider tools that provide multiple security functions
   - Standardize on a core set of security tools across your organization

3. **Leverage managed services**:
   - Use AWS managed services to reduce operational overhead
   - Implement services like Amazon GuardDuty, AWS Security Hub, and AWS Config
   - Consider AWS managed database services instead of self-managed databases
   - Use container services like Amazon ECS or Amazon EKS instead of managing your own container infrastructure

4. **Implement centralized security management**:
   - Use AWS Organizations for centralized management of multiple accounts
   - Implement AWS Control Tower for account governance
   - Deploy security controls consistently across accounts using Service Control Policies (SCPs)
   - Centralize security monitoring and alerting

5. **Standardize security processes**:
   - Develop standardized security processes and procedures
   - Implement consistent security controls across environments
   - Automate security processes where possible
   - Document and regularly review security processes

## Implementation examples

### Example 1: Consolidating security monitoring with AWS Security Hub

AWS Security Hub provides a comprehensive view of your security state in AWS and helps you check your compliance with security standards and best practices. By using Security Hub, you can consolidate security findings from multiple AWS services and third-party products into a single place.

```yaml
Resources:
  SecurityHub:
    Type: 'AWS::SecurityHub::Hub'
    Properties: {}
  
  SecurityHubStandards:
    Type: 'AWS::SecurityHub::StandardsSubscription'
    Properties:
      StandardsArn: 'arn:aws:securityhub:::ruleset/cis-aws-foundations-benchmark/v/1.2.0'
    DependsOn: SecurityHub
```

### Example 2: Centralizing security management with AWS Organizations

AWS Organizations helps you centrally manage and govern your environment as you scale your AWS resources. You can use Service Control Policies (SCPs) to establish guardrails for all accounts in your organization.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "RequireEncryptionForS3",
      "Effect": "Deny",
      "Action": [
        "s3:PutObject"
      ],
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

### Example 3: Using AWS Control Tower for account governance

AWS Control Tower provides a simplified way to set up and govern a secure, multi-account AWS environment based on best practices. It automates the setup of a landing zone and implements guardrails for security, compliance, and operations.

```
# AWS Control Tower is primarily configured through the AWS Management Console
# The following is a sample of how you might implement additional guardrails using AWS CloudFormation

Resources:
  ConfigRule:
    Type: 'AWS::Config::ConfigRule'
    Properties:
      ConfigRuleName: 'restricted-ssh'
      Description: 'Checks whether security groups allow unrestricted SSH access'
      Source:
        Owner: 'AWS'
        SourceIdentifier: 'INCOMING_SSH_DISABLED'
      Scope:
        ComplianceResourceTypes:
          - 'AWS::EC2::SecurityGroup'
```

## AWS services to consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Security Hub</h4>
    <p>Provides a comprehensive view of your security state in AWS and helps you check your compliance with security standards and best practices. Consolidates security findings from multiple AWS services and third-party products.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Organizations</h4>
    <p>Helps you centrally manage and govern your environment as you scale your AWS resources. Enables you to centrally manage policies across multiple AWS accounts.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Control Tower</h4>
    <p>Provides a simplified way to set up and govern a secure, multi-account AWS environment based on best practices. Automates the setup of a landing zone and implements guardrails for security, compliance, and operations.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Config</h4>
    <p>Enables you to assess, audit, and evaluate the configurations of your AWS resources. Helps you maintain compliance with security standards and best practices through continuous monitoring.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon GuardDuty</h4>
    <p>Provides intelligent threat detection for your AWS accounts and workloads. Continuously monitors for malicious activity and unauthorized behavior to protect your AWS accounts and workloads.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Systems Manager</h4>
    <p>Gives you visibility and control of your infrastructure on AWS. Provides a unified interface for viewing operational data from multiple AWS services and automates operational tasks across your AWS resources.</p>
  </div>
</div>

## Benefits of reducing security management scope

- **Reduced complexity**: Fewer tools and processes to manage
- **Improved visibility**: Consolidated view of security posture
- **Lower costs**: Reduced licensing and operational expenses
- **Enhanced security**: More focused and effective security controls
- **Increased efficiency**: Streamlined security operations
- **Better compliance**: Simplified compliance management

## Related resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/sec_securely_operate_reduce_management_scope.html">AWS Well-Architected Framework - Reduce security management scope</a></li>
    <li><a href="https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/welcome.html">AWS Security Reference Architecture</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-streamline-security-operations-by-integrating-aws-security-hub-with-aws-systems-manager/">How to streamline security operations by integrating AWS Security Hub with AWS Systems Manager</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/simplify-security-assessment-setup-with-aws-security-hub-integration-with-aws-audit-manager/">Simplify security assessment setup with AWS Security Hub integration with AWS Audit Manager</a></li>
    <li><a href="https://aws.amazon.com/organizations/getting-started/">Getting Started with AWS Organizations</a></li>
  </ul>
</div>
