---
title: SEC01-BP08 - Evaluate and implement new security services and features regularly
layout: default
parent: SEC01 - How do you securely operate your workload?
grand_parent: Security
nav_order: 8
---

<div class="pillar-header">
  <h1>SEC01-BP08: Evaluate and implement new security services and features regularly</h1>
  <p>Evaluate and implement security services and features from AWS and AWS Partners that allow you to evolve the security posture of your workload.</p>
</div>

## Implementation guidance

AWS regularly releases new security services and features to help you improve your security posture. By staying informed about these releases and evaluating them for your workloads, you can continuously enhance your security capabilities and address evolving threats.

### Key steps for implementing this best practice:

1. **Stay informed about new security services and features**:
   - Subscribe to the AWS What's New announcements
   - Follow the AWS Security Blog
   - Attend AWS events like re:Invent, re:Inforce, and AWS Summits
   - Join AWS security webinars and virtual workshops
   - Follow AWS security experts on social media
   - Participate in AWS security communities and forums

2. **Establish a process for evaluating new security services**:
   - Create a security roadmap aligned with your business objectives
   - Define criteria for evaluating new security services
   - Assign responsibility for monitoring and evaluating new services
   - Establish a regular cadence for security service reviews
   - Document evaluation results and decisions

3. **Test new security services in non-production environments**:
   - Set up dedicated test accounts for security evaluations
   - Create proof-of-concept implementations
   - Test integration with existing security tools and processes
   - Evaluate the impact on performance, cost, and operations
   - Document findings and lessons learned

4. **Implement new security services strategically**:
   - Prioritize services that address your highest security risks
   - Develop an implementation plan with clear milestones
   - Start with low-risk workloads before expanding to critical ones
   - Monitor and measure the effectiveness of new security services
   - Adjust your implementation based on results

5. **Continuously improve your security posture**:
   - Regularly review the effectiveness of implemented security services
   - Stay informed about updates to existing security services
   - Retire outdated or redundant security controls
   - Adjust your security strategy based on evolving threats
   - Share knowledge and best practices across your organization

## Implementation examples

### Example 1: Security service evaluation framework

```
Security Service Evaluation Criteria:
1. Alignment with security requirements and compliance needs
2. Integration with existing security tools and processes
3. Implementation effort and resource requirements
4. Cost implications (implementation and ongoing)
5. Impact on performance and user experience
6. Maturity and reliability of the service
7. Support and documentation availability

Evaluation Process:
1. Initial assessment against criteria
2. Proof-of-concept in test environment
3. Limited pilot in non-critical production environment
4. Full implementation plan with success metrics
5. Post-implementation review
```

### Example 2: Security services implementation roadmap

```
Q1 2025:
- Evaluate and implement AWS Security Hub
- Enable Amazon GuardDuty in all accounts
- Implement AWS Config with security-focused rules

Q2 2025:
- Evaluate and implement Amazon Detective
- Implement AWS IAM Access Analyzer
- Enhance CloudTrail logging with additional event types

Q3 2025:
- Evaluate and implement AWS Network Firewall
- Implement AWS WAF with managed rules
- Enhance S3 security with Macie

Q4 2025:
- Evaluate and implement AWS CloudHSM
- Implement AWS Secrets Manager
- Review and optimize all implemented security services
```

### Example 3: Automated security service deployment

```yaml
# CloudFormation template to deploy security services across accounts
Resources:
  SecurityHubEnablement:
    Type: 'AWS::SecurityHub::Hub'
    Properties: {}
  
  GuardDutyDetector:
    Type: 'AWS::GuardDuty::Detector'
    Properties:
      Enable: true
      FindingPublishingFrequency: 'FIFTEEN_MINUTES'
  
  MacieConfiguration:
    Type: 'AWS::Macie::Session'
    Properties:
      Status: 'ENABLED'
      FindingPublishingFrequency: 'FIFTEEN_MINUTES'
  
  ConfigRecorder:
    Type: 'AWS::Config::ConfigurationRecorder'
    Properties:
      RecordingGroup:
        AllSupported: true
        IncludeGlobalResourceTypes: true
      RoleARN: !GetAtt ConfigRole.Arn
  
  ConfigDeliveryChannel:
    Type: 'AWS::Config::DeliveryChannel'
    Properties:
      ConfigSnapshotDeliveryProperties:
        DeliveryFrequency: 'One_Hour'
      S3BucketName: !Ref ConfigBucket
      S3KeyPrefix: 'config'
```

## AWS services to consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Security Hub</h4>
    <p>Provides a comprehensive view of your security state in AWS and helps you check your compliance with security standards and best practices. Aggregates, organizes, and prioritizes security alerts from multiple AWS services.</p>
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
    <h4>Amazon Inspector</h4>
    <p>Automated security assessment service that helps improve the security and compliance of applications deployed on AWS. Automatically assesses applications for exposure, vulnerabilities, and deviations from best practices.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS IAM Access Analyzer</h4>
    <p>Helps you identify resources in your organization and accounts that are shared with an external entity. Identifies unintended access to your resources and data, which is a security risk.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon Macie</h4>
    <p>A fully managed data security and data privacy service that uses machine learning and pattern matching to discover and protect your sensitive data in AWS. Provides visibility into data security risks.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Firewall Manager</h4>
    <p>A security management service that allows you to centrally configure and manage firewall rules across your accounts and applications in AWS Organizations. Simplifies your AWS WAF, AWS Shield Advanced, and VPC security groups administration.</p>
  </div>
</div>

## Benefits of regularly evaluating and implementing new security services

- **Enhanced security posture**: Access to the latest security capabilities
- **Proactive threat mitigation**: Stay ahead of evolving security threats
- **Operational efficiency**: Leverage new automation and integration capabilities
- **Cost optimization**: Take advantage of more efficient security solutions
- **Compliance support**: Address new compliance requirements with purpose-built services
- **Reduced security debt**: Avoid accumulating outdated security practices
- **Competitive advantage**: Implement security innovations faster than competitors

## Related resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/sec_securely_operate_implement_services_features.html">AWS Well-Architected Framework - Evaluate and implement new security services and features regularly</a></li>
    <li><a href="https://aws.amazon.com/security/security-learning/">AWS Security Learning</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/">AWS Security Blog</a></li>
    <li><a href="https://aws.amazon.com/new/?whats-new-content-all.sort-by=item.additionalFields.postDateTime&whats-new-content-all.sort-order=desc&whats-new-content-all.q=security&whats-new-content-all.q_operator=AND&awsf.whats-new-products=*all">AWS What's New - Security Announcements</a></li>
    <li><a href="https://aws.amazon.com/security/security-bulletins/">AWS Security Bulletins</a></li>
    <li><a href="https://aws.amazon.com/architecture/security-identity-compliance/">AWS Security, Identity, and Compliance Architecture</a></li>
  </ul>
</div>
