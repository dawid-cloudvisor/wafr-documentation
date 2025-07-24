---
title: SEC03-BP01 - Define access requirements
layout: default
parent: SEC03 - How do you manage permissions for people and machines?
grand_parent: Security
nav_order: 1
---

<div class="pillar-header">
  <h1>SEC03-BP01: Define access requirements</h1>
  <p>Each component or resource of your workload needs to be accessed by administrators, end users, or other components. Have a clear definition of who or what should have access to each component, choose the appropriate identity type and method of authentication and authorization.</p>
</div>

## Implementation guidance

Defining clear access requirements is the foundation for implementing effective permissions management. By understanding who needs access to what resources and under what conditions, you can implement the principle of least privilege and reduce the risk of unauthorized access.

### Key steps for implementing this best practice:

1. **Identify resources and components**:
   - Document all resources and components in your workload
   - Classify resources based on sensitivity and criticality
   - Group related resources that typically share access patterns
   - Identify dependencies between resources
   - Document resource ownership

2. **Identify access personas**:
   - Define administrator personas (e.g., system administrators, security administrators)
   - Define end-user personas (e.g., developers, analysts, business users)
   - Identify service and application identities
   - Document third-party access requirements
   - Consider emergency access scenarios

3. **Define access patterns**:
   - Determine what actions each persona needs to perform
   - Identify when access is needed (e.g., business hours, on-call periods)
   - Define where access should be allowed from (e.g., corporate network, specific locations)
   - Document access conditions (e.g., MFA requirements, device compliance)
   - Consider break-glass procedures for emergency access

4. **Choose appropriate identity types**:
   - Select human identity types (e.g., IAM users, federated identities)
   - Select machine identity types (e.g., IAM roles, service accounts)
   - Determine authentication methods for each identity type
   - Define session duration and refresh requirements
   - Document identity lifecycle management processes

5. **Define authorization model**:
   - Choose between role-based, attribute-based, or resource-based access control
   - Define roles or permission sets aligned with job functions
   - Establish permission boundaries for different personas
   - Document approval workflows for access requests
   - Define access review and recertification processes

6. **Document access requirements**:
   - Create a formal access requirements document
   - Include resource-to-persona mappings
   - Document required permissions for each persona
   - Define access review frequency
   - Establish processes for updating access requirements

## Implementation examples

### Example 1: Access requirements matrix

```
Resource: Production RDS Database
| Persona             | Actions                                   | Conditions                                | Identity Type      |
|---------------------|-------------------------------------------|-------------------------------------------|-------------------|
| Database Admin      | Full admin access                         | MFA required, Business hours only         | Federated Identity |
| Application         | Read/write to specific tables             | From application servers only             | IAM Role          |
| Data Analyst        | Read-only access to specific tables       | MFA required, Corporate network only      | Federated Identity |
| DevOps Engineer     | Monitoring, performance tuning            | MFA required, Approved change request     | Federated Identity |
| Backup System       | Create and export snapshots               | Scheduled windows only                    | IAM Role          |
| Emergency Access    | Full admin access                         | Break-glass procedure, time-limited       | IAM Role          |
```

### Example 2: IAM policy based on access requirements

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DataAnalystReadAccess",
      "Effect": "Allow",
      "Action": [
        "rds:DescribeDBInstances",
        "rds:DescribeDBClusters",
        "rds:DescribeDBSnapshots"
      ],
      "Resource": "arn:aws:rds:us-west-2:123456789012:db:production-db",
      "Condition": {
        "Bool": {
          "aws:MultiFactorAuthPresent": "true"
        },
        "IpAddress": {
          "aws:SourceIp": ["192.0.2.0/24", "198.51.100.0/24"]
        },
        "DateDayOfWeek": {
          "aws:CurrentTime": ["Mon-Fri"]
        },
        "DateGreaterThan": {
          "aws:CurrentTime": "2023-01-01T09:00:00Z"
        },
        "DateLessThan": {
          "aws:CurrentTime": "2023-01-01T17:00:00Z"
        }
      }
    }
  ]
}
```

### Example 3: Access requirements documentation template

```
# Access Requirements Document

## Resource Information
- Resource Name: [Resource Name]
- Resource Type: [Resource Type]
- Resource Owner: [Owner Name/Team]
- Data Classification: [Public/Internal/Confidential/Restricted]

## Access Personas

### Persona 1: [Persona Name]
- Description: [Brief description of the persona]
- Identity Type: [IAM User/IAM Role/Federated Identity]
- Required Actions:
  - [Action 1]
  - [Action 2]
- Access Conditions:
  - Authentication: [Password/MFA/Certificate]
  - Network Restrictions: [Any/Corporate Network/VPN]
  - Time Restrictions: [Any/Business Hours/Specific Schedule]
  - Approval Process: [None/Manager Approval/Change Request]
- Access Review Frequency: [Quarterly/Bi-annually/Annually]

### Persona 2: [Persona Name]
...

## Emergency Access Procedure
- Activation Process: [Process description]
- Required Approvals: [Approver names/roles]
- Access Duration: [Time limit]
- Logging Requirements: [Specific logging requirements]
- Post-Access Review Process: [Process description]
```

## AWS services to consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Identity and Access Management (IAM)</h4>
    <p>Enables you to manage access to AWS services and resources securely. Use IAM to create policies based on your defined access requirements.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS IAM Identity Center</h4>
    <p>Helps you securely create or connect your workforce identities and manage their access centrally across AWS accounts and applications. Use permission sets to implement your access requirements.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon Cognito</h4>
    <p>Provides authentication, authorization, and user management for your web and mobile apps. Use Cognito to implement access requirements for your application users.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Resource Access Manager (RAM)</h4>
    <p>Helps you securely share your resources across AWS accounts. Use RAM to implement cross-account access based on your requirements.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Organizations</h4>
    <p>Helps you centrally manage and govern your environment as you scale your AWS resources. Use Service Control Policies (SCPs) to implement organization-wide access guardrails.</p>
  </div>
</div>

## Benefits of defining access requirements

- **Improved security posture**: Clear access requirements help implement the principle of least privilege
- **Simplified permissions management**: Well-defined requirements make it easier to create and maintain appropriate permissions
- **Reduced risk of unauthorized access**: Explicit access conditions help prevent inappropriate access
- **Enhanced compliance**: Documented access requirements support compliance with regulatory requirements
- **Streamlined access reviews**: Clear requirements make it easier to review and validate access
- **Better operational efficiency**: Well-defined access patterns reduce friction for legitimate access needs
- **Improved auditability**: Documented requirements provide a baseline for access audits

## Related resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/sec_permissions_define.html">AWS Well-Architected Framework - Define access requirements</a></li>
    <li><a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html">Policies and permissions in IAM</a></li>
    <li><a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_identity-vs-resource.html">Identity-based policies and resource-based policies</a></li>
    <li><a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html">Policy evaluation logic</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/techniques-for-writing-least-privilege-iam-policies/">Techniques for writing least privilege IAM policies</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-use-aws-iam-access-analyzer-to-set-permission-guardrails/">How to use AWS IAM Access Analyzer to set permission guardrails</a></li>
  </ul>
</div>
