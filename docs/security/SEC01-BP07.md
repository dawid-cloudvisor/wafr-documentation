---
title: SEC01-BP07 - Identify threats and prioritize mitigations using a threat model
layout: default
parent: SEC01 - How do you securely operate your workload?
grand_parent: Security
nav_order: 7
---

<div class="pillar-header">
  <h1>SEC01-BP07: Identify threats and prioritize mitigations using a threat model</h1>
  <p>Use a threat model to identify and maintain a list of security threats. Prioritize your threats and adjust your security controls to prevent, detect, and respond. Revisit and reprioritize regularly.</p>
</div>

## Implementation guidance

Threat modeling is a structured approach to identifying, quantifying, and addressing security threats to your workload. By creating a threat model, you can systematically identify potential threats, assess their impact, and prioritize mitigation efforts based on risk.

### Key steps for implementing this best practice:

1. **Establish a threat modeling process**:
   - Select a threat modeling methodology (e.g., STRIDE, PASTA, OCTAVE)
   - Define the scope of your threat modeling activities
   - Identify key stakeholders and their responsibilities
   - Establish a regular cadence for threat modeling activities

2. **Identify potential threats**:
   - Document your system architecture and data flows
   - Identify trust boundaries within your system
   - Brainstorm potential threats using your chosen methodology
   - Consider both internal and external threat actors
   - Review industry-specific threat intelligence

3. **Assess and prioritize threats**:
   - Evaluate the likelihood of each threat
   - Assess the potential impact of each threat
   - Calculate risk scores based on likelihood and impact
   - Prioritize threats based on risk scores
   - Consider business context when prioritizing

4. **Develop mitigation strategies**:
   - Identify security controls to address each threat
   - Categorize controls as preventive, detective, or responsive
   - Evaluate the effectiveness of existing controls
   - Identify gaps in your security controls
   - Develop a plan to implement additional controls

5. **Implement and validate controls**:
   - Deploy security controls according to your prioritization
   - Test the effectiveness of implemented controls
   - Conduct regular security assessments and penetration tests
   - Update your threat model based on testing results

6. **Continuously review and update**:
   - Regularly revisit your threat model
   - Update the model as your system evolves
   - Incorporate new threat intelligence
   - Adjust priorities based on changing business needs
   - Refine your security controls based on new information

## Threat modeling methodologies

### STRIDE
STRIDE is a threat modeling methodology developed by Microsoft that categorizes threats into six types:
- **S**poofing: Impersonating something or someone else
- **T**ampering: Modifying data or code
- **R**epudiation: Claiming to not have performed an action
- **I**nformation disclosure: Exposing information to unauthorized individuals
- **D**enial of service: Denying or degrading service to users
- **E**levation of privilege: Gaining capabilities without proper authorization

### PASTA (Process for Attack Simulation and Threat Analysis)
PASTA is a risk-centric threat modeling methodology with seven stages:
1. Define objectives
2. Define technical scope
3. Application decomposition
4. Threat analysis
5. Vulnerability analysis
6. Attack analysis
7. Risk and impact analysis

### OCTAVE (Operationally Critical Threat, Asset, and Vulnerability Evaluation)
OCTAVE is a risk-based strategic assessment and planning technique for security that focuses on:
- Identifying critical assets
- Identifying threats to those assets
- Identifying vulnerabilities
- Developing security strategies

## Implementation examples

### Example 1: Threat modeling for an API-based web application

```
1. System Description:
   - Web application with public API endpoints
   - User authentication via IAM Identity Center
   - Data stored in Amazon RDS and Amazon S3
   - Processing performed by AWS Lambda functions

2. Identified Threats:
   - Unauthorized API access (Spoofing)
   - SQL injection attacks (Tampering)
   - Sensitive data exposure (Information disclosure)
   - API rate limiting bypass (Denial of service)
   - Privilege escalation through misconfigured IAM roles

3. Risk Assessment:
   - Unauthorized API access: High likelihood, High impact
   - SQL injection: Medium likelihood, High impact
   - Sensitive data exposure: Medium likelihood, High impact
   - API rate limiting bypass: High likelihood, Medium impact
   - Privilege escalation: Low likelihood, High impact

4. Mitigation Strategies:
   - Implement API Gateway with AWS WAF for API protection
   - Use parameterized queries and input validation for SQL injection prevention
   - Encrypt sensitive data at rest and in transit
   - Implement strict API throttling and monitoring
   - Apply least privilege principle to all IAM roles
```

### Example 2: AWS-specific threat model documentation

```yaml
Threat: Unauthorized S3 bucket access
Risk: High (Likelihood: Medium, Impact: High)
Mitigations:
  - Implement S3 bucket policies to restrict access
  - Enable S3 Block Public Access settings
  - Use AWS CloudTrail to monitor S3 access
  - Configure Amazon GuardDuty to detect suspicious access patterns
  - Implement S3 object encryption

Threat: Compromised IAM credentials
Risk: High (Likelihood: Medium, Impact: High)
Mitigations:
  - Enforce MFA for all IAM users
  - Implement IAM Access Analyzer to identify unintended access
  - Use temporary credentials with appropriate timeouts
  - Monitor and alert on unusual IAM activity using CloudTrail
  - Implement just-in-time access for privileged operations
```

## AWS services to consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon GuardDuty</h4>
    <p>Provides intelligent threat detection for your AWS accounts and workloads. Continuously monitors for malicious activity and unauthorized behavior to protect your AWS accounts and workloads.</p>
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
    <h4>AWS Config</h4>
    <p>Enables you to assess, audit, and evaluate the configurations of your AWS resources. Helps you maintain compliance with security standards and best practices through continuous monitoring.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon Detective</h4>
    <p>Makes it easy to analyze, investigate, and quickly identify the root cause of security findings or suspicious activities. Automatically collects log data from your AWS resources and uses machine learning to create a unified view.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS CloudTrail</h4>
    <p>Records API calls for your account and delivers log files to you. Provides event history of your AWS account activity, including actions taken through the AWS Management Console, AWS SDKs, command line tools, and other AWS services.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS WAF</h4>
    <p>Helps protect your web applications or APIs against common web exploits and bots that may affect availability, compromise security, or consume excessive resources. Gives you control over how traffic reaches your applications.</p>
  </div>
</div>

## Benefits of threat modeling

- **Proactive security**: Identifies and addresses threats before they can be exploited
- **Risk-based approach**: Focuses security efforts on the most significant risks
- **Efficient resource allocation**: Prioritizes security investments based on risk
- **Improved security awareness**: Builds security knowledge across the organization
- **Better architectural decisions**: Influences system design to address security concerns early
- **Regulatory compliance**: Helps meet compliance requirements for risk assessment

## Related resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/sec_securely_operate_threat_model.html">AWS Well-Architected Framework - Identify threats and prioritize mitigations using a threat model</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-approach-threat-modeling/">How to approach threat modeling</a></li>
    <li><a href="https://owasp.org/www-community/Threat_Modeling">OWASP Threat Modeling</a></li>
    <li><a href="https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/welcome.html">AWS Security Reference Architecture</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-build-a-multi-region-threat-detection-strategy-with-amazon-guardduty/">How to build a multi-Region threat detection strategy with Amazon GuardDuty</a></li>
  </ul>
</div>
