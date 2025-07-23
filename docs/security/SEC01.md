---
title: SEC01 - How do you securely operate your workload?
layout: default
parent: Security
nav_order: 1
---
<div class="pillar-header">
  <h1>SEC01: How do you securely operate your workload?</h1>
  <p>To securely operate your workload, you must apply overarching best practices to every area of security. Take requirements and processes that you have defined in operational excellence at an organizational and workload level, and apply them to all areas.</p>
</div>

## Best Practices

<div class="best-practice">
  <h4>Separate workloads using accounts</h4>
  <p>Organize workloads in separate accounts and group accounts based on function or common controls, rather than mirroring your reporting structure. Start with security and infrastructure in mind to enable your organization to set common guardrails as your workloads grow.</p>
  
  <p><strong>Implementation guidance:</strong></p>
  <ul>
    <li>Use AWS Organizations to centrally manage and govern your environment as you scale your AWS resources</li>
    <li>Implement AWS Control Tower to set up and govern a secure, compliant multi-account AWS environment</li>
    <li>Consider different account strategies such as:
      <ul>
        <li>Workload-oriented: Separate accounts for each workload</li>
        <li>Environment-oriented: Separate accounts for development, testing, and production</li>
        <li>Team-oriented: Separate accounts for different teams or business units</li>
      </ul>
    </li>
    <li>Use Service Control Policies (SCPs) to establish guardrails for all accounts in your organization</li>
  </ul>
</div>

<div class="best-practice">
  <h4>Secure AWS account</h4>
  <p>Secure access to your accounts, for example by enabling MFA and restrict use of the root user, and configure account contacts.</p>
  
  <p><strong>Implementation guidance:</strong></p>
  <ul>
    <li>Enable Multi-Factor Authentication (MFA) for all users, especially those with elevated privileges</li>
    <li>Restrict and monitor the use of the root user account</li>
    <li>Configure account alternate contacts (security, billing, and operations)</li>
    <li>Implement a strong password policy</li>
    <li>Use AWS IAM Access Analyzer to identify resources that are shared with external entities</li>
    <li>Regularly review and rotate credentials</li>
  </ul>
</div>

<div class="best-practice">
  <h4>Keep up to date with security threats</h4>
  <p>Recognize attack vectors by staying up to date with the latest security threats to help you define and implement appropriate controls.</p>
  
  <p><strong>Implementation guidance:</strong></p>
  <ul>
    <li>Subscribe to the AWS Security Bulletin</li>
    <li>Monitor AWS Trusted Advisor security recommendations</li>
    <li>Review AWS Security Blog regularly</li>
    <li>Participate in security communities and forums</li>
    <li>Implement threat intelligence feeds</li>
    <li>Use AWS Security Hub to view your security state and check compliance with security standards</li>
  </ul>
</div>

<div class="best-practice">
  <h4>Keep up to date with security recommendations</h4>
  <p>Stay up to date with both AWS and industry security recommendations to evolve the security posture of your workload.</p>
  
  <p><strong>Implementation guidance:</strong></p>
  <ul>
    <li>Review AWS Security Best Practices whitepapers and documentation</li>
    <li>Implement AWS Security Hub and review its findings regularly</li>
    <li>Enable AWS Config and use conformance packs for security best practices</li>
    <li>Follow industry standards like CIS, NIST, and PCI DSS</li>
    <li>Attend AWS security webinars and events</li>
    <li>Consider engaging with AWS Professional Services or AWS Partners for security assessments</li>
  </ul>
</div>

<div class="best-practice">
  <h4>Automate testing and validation of security controls</h4>
  <p>Automate testing and validation of all security controls. For example, scan items such as machine images and infrastructure as code templates for security vulnerabilities, irregularities, and drift from an established baseline before they are deployed. Tools and services, such as Amazon Inspector, can be used to automate host and network vulnerability assessments.</p>
  
  <p><strong>Implementation guidance:</strong></p>
  <ul>
    <li>Implement Amazon Inspector for automated security assessments</li>
    <li>Use AWS Config Rules to automatically evaluate the configuration settings of AWS resources</li>
    <li>Integrate security testing into your CI/CD pipeline</li>
    <li>Implement infrastructure as code (IaC) scanning tools</li>
    <li>Use AWS CloudFormation Guard or similar tools to validate IaC templates</li>
    <li>Implement automated compliance validation using AWS Audit Manager</li>
    <li>Use AWS Security Hub to automate security checks against security standards</li>
  </ul>
</div>

<div class="best-practice">
  <h4>Identify and prioritize risks</h4>
  <p>Use a risk model to identify and maintain a list of security risks. Prioritize your risks and adjust your security controls to prevent, detect, and respond. Revisit and reprioritize regularly.</p>
  
  <p><strong>Implementation guidance:</strong></p>
  <ul>
    <li>Develop a risk assessment methodology for your organization</li>
    <li>Maintain a risk register for your workloads</li>
    <li>Prioritize risks based on impact and likelihood</li>
    <li>Align security controls with identified risks</li>
    <li>Implement AWS Security Hub to help identify and prioritize security findings</li>
    <li>Use Amazon GuardDuty for threat detection and continuous security monitoring</li>
    <li>Regularly review and update your risk assessments</li>
  </ul>
</div>

<div class="best-practice">
  <h4>Evaluate and implement new security services and features regularly</h4>
  <p>Evaluate and implement security services and features from AWS and AWS Partners that allow you to evolve the security posture of your workload.</p>
  
  <p><strong>Implementation guidance:</strong></p>
  <ul>
    <li>Subscribe to AWS What's New announcements for security services</li>
    <li>Review AWS re:Invent and other AWS event announcements for new security features</li>
    <li>Establish a process to evaluate and test new security services</li>
    <li>Explore the AWS Security Competency Partners for additional security solutions</li>
    <li>Implement a security roadmap that includes adoption of new security services</li>
    <li>Regularly review AWS Trusted Advisor recommendations</li>
  </ul>
</div>

## Implementation Guidance

<div class="implementation-step">
  <h4>1. Establish a Security Baseline</h4>
  <p>Start by establishing a security baseline for your AWS environment. This includes setting up AWS Organizations, implementing account-level controls, and defining security policies.</p>
  <ul>
    <li>Set up AWS Organizations and organize accounts based on workload or function</li>
    <li>Implement AWS Control Tower for account governance</li>
    <li>Configure Service Control Policies (SCPs) to enforce security guardrails</li>
    <li>Enable AWS Security Hub and configure security standards</li>
    <li>Implement AWS Config for resource configuration monitoring</li>
  </ul>
</div>

<div class="implementation-step">
  <h4>2. Implement Continuous Monitoring</h4>
  <p>Implement continuous monitoring to detect security threats and compliance violations in your environment.</p>
  <ul>
    <li>Enable Amazon GuardDuty for threat detection</li>
    <li>Configure AWS Security Hub to aggregate and prioritize findings</li>
    <li>Set up Amazon CloudWatch alarms for security-related events</li>
    <li>Implement AWS CloudTrail for API activity monitoring</li>
    <li>Use Amazon EventBridge to automate responses to security events</li>
    <li>Configure AWS Config Rules for continuous compliance monitoring</li>
  </ul>
</div>

<div class="implementation-step">
  <h4>3. Automate Security Processes</h4>
  <p>Automate security processes to ensure consistent application of security controls and rapid response to security events.</p>
  <ul>
    <li>Implement infrastructure as code (IaC) using AWS CloudFormation or AWS CDK</li>
    <li>Integrate security testing into your CI/CD pipeline</li>
    <li>Automate security patching using AWS Systems Manager Patch Manager</li>
    <li>Set up automated remediation for common security issues using AWS Config Rules</li>
    <li>Implement automated incident response using AWS Security Hub and Amazon EventBridge</li>
  </ul>
</div>

<div class="implementation-step">
  <h4>4. Develop a Security Incident Response Plan</h4>
  <p>Develop and test a security incident response plan to ensure you can effectively respond to security events.</p>
  <ul>
    <li>Define roles and responsibilities for incident response</li>
    <li>Establish communication protocols for security incidents</li>
    <li>Create playbooks for common security scenarios</li>
    <li>Implement AWS Security Incident Response Guide recommendations</li>
    <li>Regularly test your incident response plan through simulations</li>
    <li>Use AWS Security Hub for incident management</li>
  </ul>
</div>

<div class="implementation-step">
  <h4>5. Continuously Improve Security Posture</h4>
  <p>Continuously evaluate and improve your security posture based on new threats, recommendations, and services.</p>
  <ul>
    <li>Regularly review AWS Trusted Advisor recommendations</li>
    <li>Conduct periodic security assessments and penetration tests</li>
    <li>Stay updated with AWS security best practices and new services</li>
    <li>Implement a security roadmap with regular milestones</li>
    <li>Measure and track security metrics over time</li>
  </ul>
</div>

## AWS Services to Consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Organizations</h4>
    <p>Centrally manage and govern your environment as you scale your AWS resources. Use Service Control Policies (SCPs) to establish guardrails for all accounts in your organization.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Control Tower</h4>
    <p>Set up and govern a secure, compliant multi-account AWS environment based on best practices. Provides ongoing account management and governance as well as implementation of security controls.</p>
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
    <h4>Amazon GuardDuty</h4>
    <p>Provides intelligent threat detection for your AWS accounts and workloads. Continuously monitors for malicious activity and unauthorized behavior to protect your AWS accounts and workloads.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Config</h4>
    <p>Enables you to assess, audit, and evaluate the configurations of your AWS resources. Continuously monitors and records your AWS resource configurations and allows you to automate the evaluation of recorded configurations against desired configurations.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS CloudTrail</h4>
    <p>Enables governance, compliance, operational auditing, and risk auditing of your AWS account. Continuously monitors and records account activity across your AWS infrastructure, giving you control over storage, analysis, and remediation actions.</p>
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

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html">AWS Well-Architected Framework - Security Pillar</a></li>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/sec-01.html">SEC01: How do you securely operate your workload?</a></li>
    <li><a href="https://aws.amazon.com/architecture/security-identity-compliance/">AWS Security, Identity, and Compliance Architecture</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/">AWS Security Blog</a></li>
    <li><a href="https://docs.aws.amazon.com/security/">AWS Security Documentation</a></li>
    <li><a href="https://aws.amazon.com/security/security-learning/">AWS Security Learning</a></li>
    <li><a href="https://aws.amazon.com/organizations/getting-started/">Getting Started with AWS Organizations</a></li>
  </ul>
</div>
