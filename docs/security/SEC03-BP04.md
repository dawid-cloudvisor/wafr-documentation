---
title: SEC03-BP04 - Reduce permissions continuously
layout: default
parent: SEC03 - How do you manage permissions for people and machines?
grand_parent: Security
nav_order: 4
---

<div class="pillar-header">
  <h1>SEC03-BP04: Reduce permissions continuously</h1>
  <p>As teams and workloads determine what access they need, remove permissions they no longer use and establish review processes to achieve least privilege permissions. Continuously monitor and reduce unused identities and permissions.</p>
</div>

## Implementation guidance

Implementing least privilege is not a one-time effort but an ongoing process. As your workloads evolve, the permissions required by your identities will change. Continuously reducing permissions ensures that identities have only the access they need, minimizing security risks and maintaining a strong security posture.

### Key steps for implementing this best practice:

1. **Analyze access patterns**:
   - Use AWS IAM Access Analyzer to identify unused permissions
   - Review CloudTrail logs to understand actual access patterns
   - Identify permissions that haven't been used in the last 90 days
   - Monitor for overly permissive policies
   - Track permission usage trends over time

2. **Implement automated permission refinement**:
   - Use IAM Access Analyzer to generate least privilege policies
   - Implement automated policy refinement based on usage data
   - Set up regular jobs to identify and remove unused permissions
   - Create workflows for permission reduction approvals
   - Implement automated alerts for unused permissions

3. **Establish regular review processes**:
   - Schedule quarterly permission reviews
   - Implement role-based access reviews
   - Create dashboards for permission usage and trends
   - Document review procedures and responsibilities
   - Track metrics on permission reduction progress

4. **Implement permission guardrails**:
   - Use Service Control Policies (SCPs) to enforce permission boundaries
   - Implement permission boundaries for IAM roles
   - Create approval workflows for permission increases
   - Set up automated validation of policy changes
   - Implement policy validation in CI/CD pipelines

5. **Educate and engage teams**:
   - Train teams on least privilege principles
   - Provide tools for self-service permission analysis
   - Create incentives for permission reduction
   - Share success metrics and improvements
   - Establish a permission reduction champion in each team

6. **Measure and improve**:
   - Track permission reduction metrics over time
   - Set goals for permission reduction
   - Compare permissions across similar workloads
   - Identify patterns in permission usage
   - Continuously refine your approach based on results

## Implementation examples

### Example 1: Using IAM Access Analyzer to identify and remove unused permissions

```bash
# Generate a policy based on CloudTrail access activity
aws accessanalyzer start-policy-generation \
  --policy-generation-details '{
    "principalArn": "arn:aws:iam::123456789012:role/DeveloperRole"
  }' \
  --policy-type SERVICE_CONTROL_POLICY

# Retrieve the generated policy
aws accessanalyzer get-generated-policy \
  --job-id a1b2c3d4-5678-90ab-cdef-EXAMPLE11111

# Update the role with the refined policy
aws iam update-assume-role-policy \
  --role-name DeveloperRole \
  --policy-document file://refined-policy.json
```

### Example 2: Automated permission review workflow

```yaml
# AWS Step Functions state machine for permission review
{
  "Comment": "Permission Review Workflow",
  "StartAt": "IdentifyUnusedPermissions",
  "States": {
    "IdentifyUnusedPermissions": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-west-2:123456789012:function:IdentifyUnusedPermissions",
      "Next": "AnyUnusedPermissions"
    },
    "AnyUnusedPermissions": {
      "Type": "Choice",
      "Choices": [
        {
          "Variable": "$.unusedPermissionsFound",
          "BooleanEquals": true,
          "Next": "NotifyReviewers"
        }
      ],
      "Default": "NoActionNeeded"
    },
    "NotifyReviewers": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-west-2:123456789012:function:NotifyReviewers",
      "Next": "WaitForApproval"
    },
    "WaitForApproval": {
      "Type": "Task",
      "Resource": "arn:aws:states:::lambda:invoke.waitForTaskToken",
      "Parameters": {
        "FunctionName": "arn:aws:lambda:us-west-2:123456789012:function:WaitForApproval",
        "Payload": {
          "taskToken.$": "$$.Task.Token",
          "unusedPermissions.$": "$.unusedPermissions"
        }
      },
      "Next": "ProcessApproval"
    },
    "ProcessApproval": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-west-2:123456789012:function:ProcessApproval",
      "Next": "UpdatePermissions"
    },
    "UpdatePermissions": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-west-2:123456789012:function:UpdatePermissions",
      "End": true
    },
    "NoActionNeeded": {
      "Type": "Pass",
      "End": true
    }
  }
}
```

### Example 3: Permission reduction metrics dashboard

```
# Permission Reduction Metrics Dashboard

## Overall Metrics
- Total number of IAM roles: 120
- Roles with unused permissions: 78 (65%)
- Total unused permissions identified: 342
- Permissions removed this quarter: 156
- Permission reduction rate: 45%

## Top 5 Roles with Most Unused Permissions
1. AdminRole: 45 unused permissions
2. DeveloperRole: 38 unused permissions
3. DataAnalystRole: 27 unused permissions
4. NetworkAdminRole: 24 unused permissions
5. SecurityAuditorRole: 18 unused permissions

## Unused Permission Types
- EC2 Actions: 89 (26%)
- S3 Actions: 76 (22%)
- IAM Actions: 54 (16%)
- RDS Actions: 43 (13%)
- Other Services: 80 (23%)

## Quarterly Trend
Q1: 423 unused permissions identified, 98 removed (23%)
Q2: 387 unused permissions identified, 124 removed (32%)
Q3: 342 unused permissions identified, 156 removed (45%)

## Teams Performance
- Team A: 87% of recommended reductions implemented
- Team B: 62% of recommended reductions implemented
- Team C: 41% of recommended reductions implemented
- Team D: 73% of recommended reductions implemented
```

## AWS services to consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS IAM Access Analyzer</h4>
    <p>Helps you identify unused permissions and generate least privilege policies based on access activity. Use it to continuously analyze and refine permissions.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS CloudTrail</h4>
    <p>Records API calls for your account and delivers log files to you. Use CloudTrail data to understand actual permission usage patterns.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon CloudWatch</h4>
    <p>Monitors your AWS resources and the applications you run on AWS in real time. Create dashboards and alerts for permission usage and changes.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Organizations</h4>
    <p>Helps you centrally manage and govern your environment as you scale your AWS resources. Use Service Control Policies (SCPs) to enforce permission guardrails.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Step Functions</h4>
    <p>Coordinates multiple AWS services into serverless workflows. Use Step Functions to create automated permission review and reduction workflows.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon QuickSight</h4>
    <p>A business intelligence service that makes it easy to deliver insights to everyone in your organization. Create dashboards to visualize permission usage and reduction metrics.</p>
  </div>
</div>

## Benefits of reducing permissions continuously

- **Enhanced security posture**: Minimizes the risk of unauthorized access and potential damage
- **Reduced attack surface**: Limits the actions that can be performed by compromised credentials
- **Improved compliance**: Supports regulatory requirements for least privilege access
- **Better visibility**: Provides clearer understanding of actual permission requirements
- **Operational efficiency**: Simplifies permission management and reduces complexity
- **Proactive risk management**: Identifies and addresses permission issues before they can be exploited
- **Cultural improvement**: Fosters a security-conscious culture across teams

## Related resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/sec_permissions_continuous_reduction.html">AWS Well-Architected Framework - Reduce permissions continuously</a></li>
    <li><a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_access-advisor.html">Refining permissions using last accessed information</a></li>
    <li><a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-policy-generation.html">IAM Access Analyzer policy generation</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/automate-analyzing-permissions-using-iam-access-analyzer/">Automate analyzing permissions using IAM Access Analyzer</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-automatically-update-your-security-groups-for-amazon-cloudfront-and-aws-waf-by-using-aws-lambda/">How to automatically update your security groups for Amazon CloudFront and AWS WAF by using AWS Lambda</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-use-aws-iam-access-analyzer-to-set-permission-guardrails/">How to use AWS IAM Access Analyzer to set permission guardrails</a></li>
  </ul>
</div>
