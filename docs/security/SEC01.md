---
title: SEC01 - How do you securely operate your workload?
layout: default
parent: Security
has_children: true
nav_order: 1
---

<div class="pillar-header">
  <h1>SEC01: How do you securely operate your workload?</h1>
  <p>To operate your workload securely, you must apply overarching best practices to every area of security. Take requirements and processes that you have defined in operational excellence at an organizational and workload level, and apply them to all areas. Staying up to date with AWS and industry security threats and recommendations helps you evolve your threat model and control objectives. Automating security processes, testing, and validation allow you to scale your security operations.</p>
</div>

## Best Practices

This question includes the following best practices:

<div class="best-practices-list">
  <ul>
    <li><a href="./SEC01-BP01.html">SEC01-BP01: Separate workloads using accounts</a></li>
    <li><a href="./SEC01-BP02.html">SEC01-BP02: Secure account root user and properties</a></li>
    <li><a href="./SEC01-BP03.html">SEC01-BP03: Identify and validate control objectives</a></li>
    <li><a href="./SEC01-BP04.html">SEC01-BP04: Stay up to date with security threats and recommendations</a></li>
    <li><a href="./SEC01-BP05.html">SEC01-BP05: Reduce security management scope</a></li>
    <li><a href="./SEC01-BP06.html">SEC01-BP06: Automate deployment of standard security controls</a></li>
    <li><a href="./SEC01-BP07.html">SEC01-BP07: Identify threats and prioritize mitigations using a threat model</a></li>
    <li><a href="./SEC01-BP08.html">SEC01-BP08: Evaluate and implement new security services and features regularly</a></li>
  </ul>
</div>

## Key Concepts

### Security Operations Principles

**Defense in Depth**: Implement multiple layers of security controls throughout your workload. No single security control should be relied upon to protect your entire workload.

**Shared Responsibility Model**: Understand the division of security responsibilities between AWS and you as the customer. AWS secures the infrastructure, while you secure your workloads and data.

**Continuous Security**: Security is not a one-time implementation but an ongoing process that requires continuous monitoring, assessment, and improvement.

### Foundational Security Elements

**Account Separation**: Use separate AWS accounts to isolate workloads and limit the blast radius of security incidents. This provides strong isolation boundaries and simplifies security management.

**Root User Security**: Protect the AWS account root user with the highest level of security controls, including MFA and restricted access.

**Threat Modeling**: Systematically identify potential threats to your workload and implement appropriate mitigations based on risk assessment.

**Automation**: Automate security processes wherever possible to reduce human error, ensure consistency, and scale security operations.

## AWS Services to Consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Organizations</h4>
    <p>Helps you centrally manage and govern your environment as you scale your AWS resources. Essential for implementing account separation and organizational security policies.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Control Tower</h4>
    <p>Provides a simplified way to set up and govern a secure, multi-account AWS environment based on best practices. Automates the setup of baseline security controls.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Security Hub</h4>
    <p>Provides a comprehensive view of your security state in AWS and helps you check your compliance with security standards and best practices.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Config</h4>
    <p>Enables you to assess, audit, and evaluate the configurations of your AWS resources. Helps maintain compliance with security standards.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS CloudFormation</h4>
    <p>Gives you an easy way to model a collection of related AWS and third-party resources. Enables infrastructure as code and consistent security control deployment.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Systems Manager</h4>
    <p>Gives you visibility and control of your infrastructure on AWS. Helps automate security operations and maintain compliance at scale.</p>
  </div>
</div>

## Implementation Approach

### 1. Foundation and Governance
- Establish multi-account architecture using AWS Organizations
- Secure root user accounts across all AWS accounts
- Implement baseline security controls and guardrails
- Define security policies and procedures
- Establish incident response procedures

### 2. Threat Assessment and Planning
- Conduct threat modeling exercises for your workloads
- Identify and document security control objectives
- Assess current security posture and identify gaps
- Prioritize security improvements based on risk
- Create security roadmap and implementation plan

### 3. Automation and Standardization
- Implement infrastructure as code for security controls
- Automate security assessments and compliance checks
- Standardize security configurations across environments
- Create reusable security templates and patterns
- Implement automated remediation where appropriate

### 4. Continuous Improvement
- Stay current with security threats and AWS security features
- Regularly review and update threat models
- Conduct security assessments and penetration testing
- Implement lessons learned from security incidents
- Continuously refine security processes and controls

## Security Operations Framework

### Preventive Controls
- **Account Isolation**: Separate workloads using AWS accounts
- **Access Controls**: Implement least privilege access principles
- **Network Security**: Control traffic flow and network access
- **Data Protection**: Encrypt data at rest and in transit
- **Configuration Management**: Maintain secure configurations

### Detective Controls
- **Logging and Monitoring**: Comprehensive logging across all services
- **Threat Detection**: Real-time threat detection and alerting
- **Compliance Monitoring**: Continuous compliance assessment
- **Vulnerability Management**: Regular vulnerability scanning
- **Security Metrics**: Track security posture and trends

### Responsive Controls
- **Incident Response**: Structured incident response procedures
- **Automated Remediation**: Automatic response to security events
- **Forensic Capabilities**: Tools and processes for investigation
- **Recovery Procedures**: Restore operations after incidents
- **Communication Plans**: Stakeholder communication during incidents

## Common Challenges and Solutions

### Challenge: Account Sprawl
**Solution**: Implement proper account governance with AWS Organizations, establish naming conventions, and use automation for account provisioning and management.

### Challenge: Root User Management
**Solution**: Implement strong authentication for root users, limit root user usage to essential tasks only, and establish procedures for root user access.

### Challenge: Security Control Consistency
**Solution**: Use infrastructure as code, implement automated deployment of security controls, and establish security baselines for all environments.

### Challenge: Threat Model Maintenance
**Solution**: Establish regular threat modeling reviews, integrate threat modeling into development processes, and maintain threat intelligence feeds.

### Challenge: Security Operations Scale
**Solution**: Implement automation for routine security tasks, use managed security services, and establish clear escalation procedures.

## Security Maturity Levels

### Level 1: Basic Security
- AWS account separation implemented
- Root user secured with MFA
- Basic logging enabled
- Manual security processes

### Level 2: Managed Security
- Automated security control deployment
- Centralized security monitoring
- Regular security assessments
- Documented incident response procedures

### Level 3: Optimized Security
- Continuous security monitoring and alerting
- Automated threat response
- Regular threat modeling updates
- Security metrics and continuous improvement

### Level 4: Innovative Security
- Predictive security analytics
- AI/ML-powered threat detection
- Automated security orchestration
- Proactive threat hunting

## Related resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html">AWS Well-Architected Framework - Security Pillar</a></li>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/sec-01.html">SEC01: How do you securely operate your workload?</a></li>
    <li><a href="https://aws.amazon.com/organizations/getting-started/best-practices/">AWS Organizations Best Practices</a></li>
    <li><a href="https://docs.aws.amazon.com/accounts/latest/reference/root-user-tasks.html">Tasks that require root user credentials</a></li>
    <li><a href="https://aws.amazon.com/security/security-resources/">AWS Security Resources</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/">AWS Security Blog</a></li>
  </ul>
</div>

<style>
.best-practices-list ul {
  list-style-type: none;
  padding-left: 0;
}

.best-practices-list li {
  background-color: #ffead7;
  margin-bottom: 0.5rem;
  border-radius: 5px;
  border: 1px solid #ffcca5;
}

.best-practices-list li a {
  display: block;
  padding: 0.75rem 1rem;
  color: #ff6a00;
  text-decoration: none;
  font-weight: 500;
}

.best-practices-list li a:hover {
  background-color: #ffcca5;
  border-radius: 4px;
}
</style>
