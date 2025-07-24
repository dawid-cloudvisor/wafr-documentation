---
title: SEC03-BP07 - Analyze public and cross-account access
layout: default
parent: SEC03 - How do you manage permissions for people and machines?
grand_parent: Security
nav_order: 7
---

<div class="pillar-header">
  <h1>SEC03-BP07: Analyze public and cross-account access</h1>
  <p>Continually monitor your findings about public and cross-account access. Reduce public access and cross-account access to only the specific resources that require this access. For example, consider if your Amazon S3 buckets or AWS Lambda functions require public access, or if cross-account access is required.</p>
</div>

## Implementation guidance

Public and cross-account access can introduce security risks if not properly managed and monitored. By continuously analyzing and reducing unnecessary external access, you can minimize your attack surface while maintaining the functionality required for legitimate business needs.

### Key steps for implementing this best practice:

1. **Identify public and cross-account access**:
   - Use AWS IAM Access Analyzer to identify resources shared externally
   - Inventory all resources with public access permissions
   - Document legitimate business requirements for external access
   - Identify cross-account access patterns and dependencies
   - Catalog third-party integrations requiring access

2. **Implement continuous monitoring**:
   - Set up AWS IAM Access Analyzer for ongoing analysis
   - Configure alerts for new public or cross-account access
   - Monitor changes to resource-based policies
   - Track access patterns and usage
   - Implement automated scanning for public resources

3. **Establish access validation processes**:
   - Create approval workflows for public access requests
   - Implement regular reviews of external access permissions
   - Validate business justification for cross-account access
   - Document and approve third-party access requirements
   - Establish expiration dates for temporary external access

4. **Implement least privilege for external access**:
   - Restrict public access to only necessary resources
   - Use specific conditions in cross-account policies
   - Implement time-based restrictions where appropriate
   - Use external IDs for cross-account role assumptions
   - Apply IP address restrictions when possible

5. **Secure public resources**:
   - Implement additional security controls for public resources
   - Use encryption for publicly accessible data
   - Implement rate limiting and DDoS protection
   - Monitor public resource usage and access patterns
   - Consider using CloudFront for public web content

6. **Regularly audit and remediate**:
   - Conduct quarterly reviews of public and cross-account access
   - Remove unnecessary external access permissions
   - Update access policies based on changing requirements
   - Implement automated remediation for policy violations
   - Generate compliance reports for management

## Implementation examples

### Example 1: Using AWS IAM Access Analyzer to identify external access

```bash
# Create an Access Analyzer
aws accessanalyzer create-analyzer \
  --analyzer-name "OrganizationAnalyzer" \
  --type ORGANIZATION \
  --tags Key=Environment,Value=Production

# List findings for external access
aws accessanalyzer list-findings \
  --analyzer-arn "arn:aws:access-analyzer:us-west-2:123456789012:analyzer/OrganizationAnalyzer" \
  --filter criteria=resourceType,eq=AWS::S3::Bucket \
  --filter criteria=status,eq=ACTIVE

# Get detailed information about a specific finding
aws accessanalyzer get-finding \
  --analyzer-arn "arn:aws:access-analyzer:us-west-2:123456789012:analyzer/OrganizationAnalyzer" \
  --id "a1b2c3d4-5678-90ab-cdef-EXAMPLE11111"

# Archive a finding after validation
aws accessanalyzer update-findings \
  --analyzer-arn "arn:aws:access-analyzer:us-west-2:123456789012:analyzer/OrganizationAnalyzer" \
  --ids "a1b2c3d4-5678-90ab-cdef-EXAMPLE11111" \
  --status ARCHIVED
```

### Example 2: S3 bucket policy with controlled public access

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadForWebsite",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::my-public-website/*",
      "Condition": {
        "StringEquals": {
          "s3:ExistingObjectTag/PublicAccess": "true"
        },
        "IpAddress": {
          "aws:SourceIp": [
            "203.0.113.0/24",
            "198.51.100.0/24"
          ]
        }
      }
    },
    {
      "Sid": "DenyDirectPublicAccess",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::my-public-website",
        "arn:aws:s3:::my-public-website/*"
      ],
      "Condition": {
        "StringNotEquals": {
          "aws:SourceVpce": "vpce-1234567890abcdef0"
        },
        "Bool": {
          "aws:ViaAWSService": "false"
        }
      }
    }
  ]
}
```

### Example 3: Cross-account IAM role with external ID

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::TRUSTED-ACCOUNT-ID:root"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "sts:ExternalId": "UniqueExternalIdentifier123"
        },
        "IpAddress": {
          "aws:SourceIp": "203.0.113.0/24"
        },
        "DateGreaterThan": {
          "aws:CurrentTime": "2024-01-01T00:00:00Z"
        },
        "DateLessThan": {
          "aws:CurrentTime": "2024-12-31T23:59:59Z"
        }
      }
    }
  ]
}
```

### Example 4: Automated monitoring and alerting for public access

```python
import json
import boto3
from datetime import datetime

def lambda_handler(event, context):
    """
    Lambda function to monitor and alert on public access changes
    """
    
    # Initialize AWS clients
    access_analyzer = boto3.client('accessanalyzer')
    sns = boto3.client('sns')
    
    try:
        # Get active findings from Access Analyzer
        response = access_analyzer.list_findings(
            analyzerArn='arn:aws:access-analyzer:us-west-2:123456789012:analyzer/OrganizationAnalyzer',
            filter={
                'status': {
                    'eq': ['ACTIVE']
                }
            }
        )
        
        findings = response.get('findings', [])
        high_risk_findings = []
        
        # Analyze findings for high-risk public access
        for finding in findings:
            if is_high_risk_finding(finding):
                high_risk_findings.append(finding)
        
        # Send alerts for high-risk findings
        if high_risk_findings:
            send_alert(sns, high_risk_findings)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'Processed {len(findings)} findings, {len(high_risk_findings)} high-risk',
                'high_risk_findings': len(high_risk_findings)
            })
        }
        
    except Exception as e:
        print(f"Error processing findings: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }

def is_high_risk_finding(finding):
    """Determine if a finding represents high risk"""
    
    # Check for unrestricted public access
    if finding.get('condition', {}) == {}:
        return True
    
    # Check for overly broad cross-account access
    principal = finding.get('principal', {})
    if principal.get('AWS') == '*':
        return True
    
    # Check for sensitive resource types
    sensitive_resources = [
        'AWS::S3::Bucket',
        'AWS::KMS::Key',
        'AWS::SecretsManager::Secret'
    ]
    
    if finding.get('resourceType') in sensitive_resources:
        return True
    
    return False

def send_alert(sns, findings):
    """Send SNS alert for high-risk findings"""
    
    message = f"High-risk public access detected!\n\n"
    message += f"Number of high-risk findings: {len(findings)}\n\n"
    
    for finding in findings[:5]:  # Limit to first 5 findings
        message += f"Resource: {finding.get('resource')}\n"
        message += f"Type: {finding.get('resourceType')}\n"
        message += f"Principal: {finding.get('principal')}\n"
        message += f"Action: {finding.get('action')}\n\n"
    
    sns.publish(
        TopicArn='arn:aws:sns:us-west-2:123456789012:SecurityAlerts',
        Subject='High-Risk Public Access Detected',
        Message=message
    )
```

## AWS services to consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS IAM Access Analyzer</h4>
    <p>Helps you identify resources in your organization and accounts that are shared with an external entity. Provides continuous monitoring and analysis of public and cross-account access.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Config</h4>
    <p>Enables you to assess, audit, and evaluate the configurations of your AWS resources. Use Config rules to monitor for public access and policy changes.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS CloudTrail</h4>
    <p>Records API calls for your account and delivers log files to you. Use CloudTrail to monitor changes to resource policies and access permissions.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon CloudWatch</h4>
    <p>Monitors your AWS resources and the applications you run on AWS in real time. Set up alerts for public access changes and unusual access patterns.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Security Hub</h4>
    <p>Provides a comprehensive view of your security state in AWS. Aggregates findings from Access Analyzer and other security services for centralized monitoring.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon GuardDuty</h4>
    <p>Provides intelligent threat detection for your AWS accounts and workloads. Can detect suspicious access patterns to public resources.</p>
  </div>
</div>

## Benefits of analyzing public and cross-account access

- **Reduced attack surface**: Minimizes exposure by eliminating unnecessary public access
- **Enhanced security posture**: Provides visibility into external access patterns
- **Improved compliance**: Supports regulatory requirements for access control and monitoring
- **Proactive risk management**: Identifies potential security issues before they can be exploited
- **Better governance**: Ensures external access aligns with business requirements
- **Operational efficiency**: Automates monitoring and reduces manual review overhead
- **Incident prevention**: Helps prevent data breaches and unauthorized access

## Related resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/sec_permissions_analyze_cross_account.html">AWS Well-Architected Framework - Analyze public and cross-account access</a></li>
    <li><a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/what-is-access-analyzer.html">AWS IAM Access Analyzer User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html">AWS global condition context keys</a></li>
    <li><a href="https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_common-scenarios_third-party.html">Providing access to an AWS account owned by a third party</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/identify-unintended-resource-access-with-aws-iam-access-analyzer/">Identify unintended resource access with AWS IAM Access Analyzer</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-use-external-id-when-granting-access-to-your-aws-resources/">How to use external ID when granting access to your AWS resources</a></li>
  </ul>
</div>
