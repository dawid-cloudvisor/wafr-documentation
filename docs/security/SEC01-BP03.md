---
title: SEC01-BP03 - Identify and validate control objectives
layout: default
parent: SEC01 - How do you securely operate your workload?
grand_parent: Security
nav_order: 3
---

<div class="pillar-header">
  <h1>SEC01-BP03: Identify and validate control objectives</h1>
  <p>Based on your compliance requirements and risks identified from your threat model, derive and validate the control objectives and controls that you need to apply to your workload. Ongoing validation of control objectives and controls helps you measure the effectiveness of risk mitigation.</p>
</div>

## Implementation guidance

Control objectives are the specific goals and outcomes that your security controls are designed to achieve. By identifying and validating these objectives, you can ensure that your security controls are effective and aligned with your compliance requirements and risk management strategy.

### Key steps for implementing this best practice:

1. **Identify compliance requirements**:
   - Determine which regulatory frameworks apply to your workload (e.g., GDPR, HIPAA, PCI DSS)
   - Identify industry standards relevant to your organization (e.g., ISO 27001, NIST CSF)
   - Document internal security policies and requirements
   - Map compliance requirements to specific control objectives

2. **Conduct threat modeling**:
   - Identify potential threats to your workload
   - Assess the likelihood and impact of each threat
   - Prioritize threats based on risk
   - Determine which controls are needed to mitigate identified threats

3. **Define control objectives**:
   - Create clear, measurable control objectives based on compliance requirements and threat model
   - Ensure control objectives are specific, measurable, achievable, relevant, and time-bound (SMART)
   - Align control objectives with your organization's risk tolerance
   - Document the relationship between control objectives and specific risks

4. **Implement security controls**:
   - Select controls that address your control objectives
   - Implement technical, administrative, and physical controls as needed
   - Document how each control maps to control objectives
   - Ensure controls are properly configured and functioning

5. **Validate controls**:
   - Test controls to ensure they function as expected
   - Conduct regular assessments of control effectiveness
   - Use automated tools to continuously validate controls where possible
   - Perform penetration testing to identify control weaknesses

6. **Monitor and improve**:
   - Continuously monitor control performance
   - Regularly review control objectives and controls
   - Update controls as threats and compliance requirements evolve
   - Implement a continuous improvement process for security controls

## Control frameworks and standards

Several established control frameworks can help you identify and validate control objectives:

### NIST Cybersecurity Framework (CSF)
The NIST CSF provides a policy framework of computer security guidance for organizations to assess and improve their ability to prevent, detect, and respond to cyber attacks. It consists of five core functions:
- Identify
- Protect
- Detect
- Respond
- Recover

### ISO/IEC 27001
ISO/IEC 27001 is an international standard for managing information security. It specifies requirements for establishing, implementing, maintaining, and continually improving an information security management system (ISMS).

### CIS Controls
The Center for Internet Security (CIS) Controls are a set of 18 prioritized safeguards to mitigate the most common cyber attacks. They are organized into three implementation groups based on their complexity and resource requirements.

### AWS Shared Responsibility Model
The AWS Shared Responsibility Model defines the security responsibilities of AWS and its customers. AWS is responsible for "security of the cloud," while customers are responsible for "security in the cloud."

## Implementation examples

### Example 1: Mapping compliance requirements to control objectives

```
Compliance Requirement: PCI DSS Requirement 3.4 - Render PAN unreadable anywhere it is stored
Control Objective: Ensure all cardholder data is encrypted at rest
Controls:
- Implement AWS KMS for encryption key management
- Configure S3 bucket encryption for cardholder data storage
- Enable RDS encryption for database instances storing cardholder data
- Implement AWS Config rules to detect unencrypted storage
- Set up CloudWatch alarms for encryption-related events
```

### Example 2: Control validation using AWS Config

```yaml
Resources:
  # AWS Config rule to check if EBS volumes are encrypted
  ConfigRuleEncryptedVolumes:
    Type: 'AWS::Config::ConfigRule'
    Properties:
      ConfigRuleName: encrypted-volumes
      Description: 'Checks whether EBS volumes are encrypted'
      Source:
        Owner: AWS
        SourceIdentifier: ENCRYPTED_VOLUMES
      Scope:
        ComplianceResourceTypes:
          - 'AWS::EC2::Volume'
  
  # AWS Config rule to check if S3 buckets have encryption enabled
  ConfigRuleS3BucketEncryption:
    Type: 'AWS::Config::ConfigRule'
    Properties:
      ConfigRuleName: s3-bucket-server-side-encryption-enabled
      Description: 'Checks if S3 buckets have encryption enabled'
      Source:
        Owner: AWS
        SourceIdentifier: S3_BUCKET_SERVER_SIDE_ENCRYPTION_ENABLED
      Scope:
        ComplianceResourceTypes:
          - 'AWS::S3::Bucket'
```

### Example 3: Control validation using AWS Security Hub

```yaml
Resources:
  # Enable AWS Security Hub
  SecurityHub:
    Type: 'AWS::SecurityHub::Hub'
    Properties: {}
  
  # Enable CIS AWS Foundations Benchmark standard
  CISBenchmarkStandard:
    Type: 'AWS::SecurityHub::StandardsSubscription'
    Properties:
      StandardsArn: 'arn:aws:securityhub:::ruleset/cis-aws-foundations-benchmark/v/1.2.0'
    DependsOn: SecurityHub
  
  # Enable PCI DSS standard
  PCIDSSStandard:
    Type: 'AWS::SecurityHub::StandardsSubscription'
    Properties:
      StandardsArn: 'arn:aws:securityhub:us-east-1::standards/pci-dss/v/3.2.1'
    DependsOn: SecurityHub
```

## AWS services to consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Audit Manager</h4>
    <p>Helps you continuously audit your AWS usage to simplify how you assess risk and compliance with regulations and industry standards. Provides pre-built frameworks for common compliance standards.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Security Hub</h4>
    <p>Provides a comprehensive view of your security state in AWS and helps you check your compliance with security standards and best practices. Includes automated compliance checks for various security standards.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Config</h4>
    <p>Enables you to assess, audit, and evaluate the configurations of your AWS resources. Helps you maintain compliance with internal policies and regulatory standards through continuous monitoring.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon Inspector</h4>
    <p>Automated security assessment service that helps improve the security and compliance of applications deployed on AWS. Automatically assesses applications for exposure, vulnerabilities, and deviations from best practices.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS CloudTrail</h4>
    <p>Records API calls for your account and delivers log files to you. Provides event history of your AWS account activity for security analysis, resource change tracking, and compliance auditing.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon CloudWatch</h4>
    <p>Monitors your AWS resources and the applications you run on AWS in real time. Helps you collect and track metrics, collect and monitor log files, and set alarms for security-related events.</p>
  </div>
</div>

## Benefits of identifying and validating control objectives

- **Aligned security controls**: Ensures security controls are directly tied to specific risks and compliance requirements
- **Measurable security posture**: Provides clear metrics for evaluating security effectiveness
- **Efficient resource allocation**: Focuses security investments on the most important control objectives
- **Simplified compliance**: Makes it easier to demonstrate compliance with regulatory requirements
- **Improved risk management**: Provides a structured approach to managing security risks
- **Enhanced security governance**: Establishes clear accountability for security controls

## Related resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/sec_securely_operate_control_objectives.html">AWS Well-Architected Framework - Identify and validate control objectives</a></li>
    <li><a href="https://docs.aws.amazon.com/audit-manager/latest/userguide/what-is.html">AWS Audit Manager User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/securityhub/latest/userguide/what-is-securityhub.html">AWS Security Hub User Guide</a></li>
    <li><a href="https://aws.amazon.com/compliance/programs/">AWS Compliance Programs</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-use-aws-security-hub-and-aws-config-to-monitor-compliance-after-aws-account-creation/">How to use AWS Security Hub and AWS Config to monitor compliance after AWS account creation</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-automate-aws-security-hub-control-disablement-at-scale-with-aws-organizations/">How to automate AWS Security Hub control disablement at scale with AWS Organizations</a></li>
  </ul>
</div>
