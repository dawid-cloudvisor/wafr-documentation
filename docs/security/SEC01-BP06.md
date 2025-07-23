---
title: SEC01-BP06 - Automate deployment of standard security controls
layout: default
parent: SEC01 - How do you securely operate your workload?
grand_parent: Security
nav_order: 6
---

<div class="pillar-header">
  <h1>SEC01-BP06: Automate deployment of standard security controls</h1>
  <p>Automate testing and validation of all security controls. For example, scan items such as machine images and infrastructure as code templates for security vulnerabilities, irregularities, and drift from an established baseline before they are deployed. Tools and services, such as Amazon Inspector, can be used to automate host and network vulnerability assessments.</p>
</div>

## Implementation guidance

Automating the deployment of security controls helps ensure consistent application of security standards across your AWS environment. This reduces human error, increases efficiency, and provides a reliable security baseline for all your workloads.

### Key steps for implementing this best practice:

1. **Define standard security controls**:
   - Identify the security controls required for your workloads
   - Document security control specifications and configurations
   - Establish security baselines for different types of resources
   - Define compliance requirements and security standards

2. **Implement infrastructure as code (IaC)**:
   - Use AWS CloudFormation or AWS CDK to define infrastructure
   - Include security controls in your IaC templates
   - Version control your IaC templates
   - Implement security guardrails in your templates

3. **Automate security testing and validation**:
   - Implement pre-deployment security scanning for IaC templates
   - Use tools like cfn-nag or AWS CloudFormation Guard to validate templates
   - Scan machine images for vulnerabilities before deployment
   - Implement automated compliance validation

4. **Implement continuous compliance monitoring**:
   - Use AWS Config to monitor resource configurations
   - Create AWS Config Rules to automatically evaluate compliance
   - Set up AWS Security Hub to aggregate security findings
   - Implement automated remediation for non-compliant resources

5. **Integrate security into CI/CD pipelines**:
   - Add security testing stages to your CI/CD pipelines
   - Implement automated security gates that prevent deployment of non-compliant resources
   - Include vulnerability scanning in your build process
   - Automate security testing of application code

## Implementation examples

### Example 1: Automating security controls with AWS CloudFormation

```yaml
Resources:
  S3Bucket:
    Type: 'AWS::S3::Bucket'
    Properties:
      BucketName: !Sub '${AWS::StackName}-secure-bucket'
      BucketEncryption:
        ServerSideEncryptionConfiguration:
          - ServerSideEncryptionByDefault:
              SSEAlgorithm: 'AES256'
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true
      VersioningConfiguration:
        Status: Enabled
      LoggingConfiguration:
        DestinationBucketName: !Ref LoggingBucket
        LogFilePrefix: 's3-access-logs/'
```

### Example 2: Automating security validation with AWS Config Rules

```yaml
Resources:
  S3BucketPublicReadProhibited:
    Type: AWS::Config::ConfigRule
    Properties:
      ConfigRuleName: s3-bucket-public-read-prohibited
      Description: Checks that your S3 buckets do not allow public read access
      Source:
        Owner: AWS
        SourceIdentifier: S3_BUCKET_PUBLIC_READ_PROHIBITED
      Scope:
        ComplianceResourceTypes:
          - AWS::S3::Bucket

  S3BucketServerSideEncryptionEnabled:
    Type: AWS::Config::ConfigRule
    Properties:
      ConfigRuleName: s3-bucket-server-side-encryption-enabled
      Description: Checks that your S3 buckets have server-side encryption enabled
      Source:
        Owner: AWS
        SourceIdentifier: S3_BUCKET_SERVER_SIDE_ENCRYPTION_ENABLED
      Scope:
        ComplianceResourceTypes:
          - AWS::S3::Bucket
```

### Example 3: Automating security scanning in CI/CD pipeline

```yaml
version: 0.2

phases:
  install:
    runtime-versions:
      python: 3.9
    commands:
      - pip install cfn-lint cfn-nag
  
  pre_build:
    commands:
      - echo "Running CloudFormation template validation"
      - cfn-lint templates/*.yaml
      - echo "Running security scan on CloudFormation templates"
      - cfn_nag_scan --input-path templates/
  
  build:
    commands:
      - echo "Deploying CloudFormation stack"
      - aws cloudformation deploy --template-file templates/main.yaml --stack-name secure-stack --capabilities CAPABILITY_IAM
```

## AWS services to consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS CloudFormation</h4>
    <p>Provides a common language to model and provision AWS and third-party resources in your cloud environment. Enables you to define security controls as code and deploy them consistently.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Config</h4>
    <p>Enables you to assess, audit, and evaluate the configurations of your AWS resources. Helps you maintain compliance with security standards and best practices through continuous monitoring and automated remediation.</p>
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
    <h4>AWS Security Hub</h4>
    <p>Provides a comprehensive view of your security state in AWS and helps you check your compliance with security standards and best practices. Aggregates, organizes, and prioritizes security alerts from multiple AWS services.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS CodePipeline</h4>
    <p>A fully managed continuous delivery service that helps you automate your release pipelines. Enables you to integrate security testing and validation into your deployment process.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Systems Manager</h4>
    <p>Gives you visibility and control of your infrastructure on AWS. Helps you automate operational tasks, including the deployment and maintenance of security controls.</p>
  </div>
</div>

## Benefits of automation

- **Consistency**: Security controls are applied consistently across all resources
- **Reduced human error**: Minimizes the risk of misconfiguration due to manual processes
- **Scalability**: Security controls scale with your infrastructure
- **Auditability**: Provides a clear record of security control implementation
- **Efficiency**: Reduces the time and effort required to implement security controls
- **Rapid remediation**: Enables quick response to security issues

## Related resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/sec_securely_operate_automate_security_controls.html">AWS Well-Architected Framework - Automate deployment of standard security controls</a></li>
    <li><a href="https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/welcome.html">AWS Security Reference Architecture</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-use-ci-cd-to-deploy-and-configure-aws-security-services-with-terraform/">How to use CI/CD to deploy and configure AWS security services</a></li>
    <li><a href="https://aws.amazon.com/blogs/devops/implementing-devsecops-using-aws-codepipeline/">Implementing DevSecOps using AWS CodePipeline</a></li>
    <li><a href="https://aws.amazon.com/solutions/implementations/aws-security-hub-automated-response-and-remediation/">AWS Security Hub Automated Response and Remediation</a></li>
  </ul>
</div>
