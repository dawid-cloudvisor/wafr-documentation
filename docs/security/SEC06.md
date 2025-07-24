---
title: SEC06 - How do you protect your compute resources?
layout: default
parent: Security
has_children: true
nav_order: 6
---

<div class="pillar-header">
  <h1>SEC06: How do you protect your compute resources?</h1>
  <p>Compute resources in your workload require multiple layers of defense to help protect from external and internal threats. Compute resources include EC2 instances, containers, AWS Lambda functions, database services, IoT devices, and more. Recommendations in this section focus on three main areas: defending against threats, reducing the attack surface, and implementing a uniform baseline. Defending against threats includes implementing a vulnerability management program, reducing the attack surface, and implementing automated patching.</p>
</div>

## Best Practices

This question includes the following best practices:

<div class="best-practices-list">
  <ul>
    <li><a href="./SEC06-BP01.html">SEC06-BP01: Perform vulnerability management</a></li>
    <li><a href="./SEC06-BP02.html">SEC06-BP02: Provision compute from hardened images</a></li>
    <li><a href="./SEC06-BP03.html">SEC06-BP03: Reduce manual management and interactive access</a></li>
    <li><a href="./SEC06-BP04.html">SEC06-BP04: Validate software integrity</a></li>
    <li><a href="./SEC06-BP05.html">SEC06-BP05: Automate compute protection</a></li>
  </ul>
</div>

## Key Concepts

### Compute Security Fundamentals

**Defense in Depth**: Implement multiple layers of security controls across your compute infrastructure. This includes host-based security, application security, container security, and serverless security measures.

**Attack Surface Reduction**: Minimize the potential entry points for attackers by removing unnecessary software, closing unused ports, disabling unneeded services, and implementing least privilege access.

**Vulnerability Management**: Establish systematic processes to identify, assess, prioritize, and remediate security vulnerabilities across all compute resources throughout their lifecycle.

**Automated Protection**: Implement automated security controls and responses to reduce human error, ensure consistency, and enable rapid response to threats at scale.

### Compute Resource Types and Security Considerations

**Virtual Machines (EC2)**: Traditional compute instances requiring OS-level security, patch management, host-based intrusion detection, and configuration hardening.

**Containers**: Lightweight, portable compute units requiring container image security, runtime protection, orchestration security, and supply chain security.

**Serverless Functions (Lambda)**: Event-driven compute requiring function-level security, dependency management, execution environment protection, and secure coding practices.

**Database Services**: Managed and self-managed databases requiring access controls, encryption, audit logging, and vulnerability management.

**IoT and Edge Devices**: Distributed compute resources requiring device authentication, secure communication, firmware management, and physical security.

## AWS Services to Consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon Inspector</h4>
    <p>Automatically assesses applications for exposure, vulnerabilities, and deviations from best practices. Provides detailed findings and remediation guidance for EC2 instances and container images.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Systems Manager</h4>
    <p>Gives you visibility and control of your infrastructure on AWS. Provides patch management, configuration management, and automation capabilities for compute resources.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon GuardDuty</h4>
    <p>Provides intelligent threat detection for your AWS accounts and workloads. Includes runtime protection for EC2 instances, containers, and serverless functions.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Security Hub</h4>
    <p>Provides a comprehensive view of your security state in AWS. Centralizes security findings from compute security tools and provides compliance dashboards.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon ECR (Elastic Container Registry)</h4>
    <p>Fully managed Docker container registry that makes it easy to store, manage, and deploy Docker container images. Includes vulnerability scanning for container images.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Lambda</h4>
    <p>Lets you run code without provisioning or managing servers. Provides built-in security features and integrates with other AWS security services for comprehensive protection.</p>
  </div>
</div>

## Implementation Approach

### 1. Vulnerability Management Program
- Implement continuous vulnerability scanning across all compute resources
- Establish vulnerability assessment and prioritization processes
- Create automated patching workflows for operating systems and applications
- Set up vulnerability tracking and remediation reporting
- Integrate vulnerability management with CI/CD pipelines

### 2. Attack Surface Reduction
- Harden operating system configurations and remove unnecessary components
- Implement least privilege access for compute resources
- Disable unused services and close unnecessary network ports
- Use minimal base images for containers and serverless functions
- Implement network segmentation and micro-segmentation

### 3. Automated Security Controls
- Deploy endpoint detection and response (EDR) solutions
- Implement automated patch management and configuration drift detection
- Set up runtime security monitoring and threat detection
- Configure automated incident response and remediation
- Establish security baseline enforcement and compliance monitoring

### 4. Secure Development and Deployment
- Implement secure coding practices and code review processes
- Integrate security testing into CI/CD pipelines
- Use infrastructure as code for consistent security configurations
- Implement container image scanning and signing
- Establish secure software supply chain practices

## Compute Security Architecture

### Multi-Layer Compute Protection
```
Application Layer Security
    ↓ (Code Analysis, WAF, API Security)
Runtime Protection
    ↓ (EDR, Behavioral Analysis, Threat Detection)
Host/Container Security
    ↓ (OS Hardening, Patch Management, Configuration)
Infrastructure Security
    ↓ (Network Controls, Access Management, Monitoring)
```

### Vulnerability Management Lifecycle
```
Asset Discovery
    ↓
Vulnerability Scanning
    ↓
Risk Assessment & Prioritization
    ↓
Remediation Planning
    ↓
Patch Deployment
    ↓
Verification & Reporting
```

### Secure Development Integration
```
Code Development
    ↓ Static Analysis (SAST)
Build Process
    ↓ Dependency Scanning
Container/Package Creation
    ↓ Image Scanning
Deployment
    ↓ Dynamic Analysis (DAST)
Runtime
    ↓ Runtime Protection (RASP)
```

## Compute Security Controls Framework

### Preventive Controls
- **Hardening**: OS configuration, service minimization, secure baselines
- **Access Controls**: Least privilege, role-based access, multi-factor authentication
- **Patch Management**: Automated patching, vulnerability remediation, update policies
- **Code Security**: Secure coding practices, dependency management, supply chain security

### Detective Controls
- **Vulnerability Scanning**: Continuous assessment, compliance monitoring, risk evaluation
- **Runtime Monitoring**: Behavioral analysis, anomaly detection, threat hunting
- **Log Analysis**: Security event correlation, audit trail analysis, compliance reporting
- **Integrity Monitoring**: File integrity, configuration drift, unauthorized changes

### Responsive Controls
- **Incident Response**: Automated containment, forensic analysis, recovery procedures
- **Threat Mitigation**: Real-time blocking, quarantine, traffic redirection
- **Patch Deployment**: Emergency patching, rollback procedures, testing protocols
- **Recovery Operations**: Backup restoration, system rebuilding, service continuity

## Common Challenges and Solutions

### Challenge: Patch Management at Scale
**Solution**: Implement AWS Systems Manager Patch Manager for automated patching, establish maintenance windows, use immutable infrastructure patterns, and implement canary deployments for updates.

### Challenge: Container Security Complexity
**Solution**: Use Amazon ECR for image scanning, implement runtime security monitoring, establish secure base images, and integrate security into container orchestration platforms.

### Challenge: Serverless Security Visibility
**Solution**: Implement function-level monitoring, use AWS X-Ray for tracing, establish secure coding practices for Lambda, and monitor function dependencies and permissions.

### Challenge: Legacy System Protection
**Solution**: Implement compensating controls, use network segmentation, deploy host-based security solutions, and plan for system modernization and migration.

### Challenge: DevSecOps Integration
**Solution**: Shift security left in development processes, automate security testing in CI/CD pipelines, provide security training for developers, and establish security champions programs.

## Compute Security Maturity Levels

### Level 1: Basic Compute Security
- Manual vulnerability scanning and patching
- Basic antivirus and host-based protection
- Standard OS configurations with minimal hardening
- Reactive security incident response

### Level 2: Managed Compute Security
- Automated vulnerability scanning and reporting
- Centralized patch management and deployment
- Standardized security baselines and configurations
- Proactive threat detection and monitoring

### Level 3: Advanced Compute Security
- Continuous vulnerability assessment and remediation
- Runtime protection and behavioral analysis
- Automated security orchestration and response
- Integrated security in development lifecycle

### Level 4: Optimized Compute Security
- AI/ML-powered threat detection and response
- Predictive vulnerability management
- Autonomous security operations and remediation
- Continuous security optimization and improvement

## Compute Protection Best Practices

### Vulnerability Management:
1. **Implement Continuous Scanning**: Regular assessment of all compute resources
2. **Prioritize Based on Risk**: Focus on critical vulnerabilities and high-value assets
3. **Automate Patch Deployment**: Reduce time between vulnerability discovery and remediation
4. **Test Before Deployment**: Validate patches in non-production environments
5. **Track and Report**: Maintain visibility into vulnerability status and trends

### Attack Surface Reduction:
1. **Minimize Installed Software**: Remove unnecessary applications and services
2. **Harden Configurations**: Apply security baselines and best practices
3. **Implement Least Privilege**: Restrict access to minimum required permissions
4. **Use Immutable Infrastructure**: Replace rather than patch infrastructure components
5. **Regular Security Assessments**: Continuously evaluate and reduce attack surface

### Automation and Orchestration:
1. **Automate Security Controls**: Reduce manual processes and human error
2. **Integrate with CI/CD**: Build security into development and deployment pipelines
3. **Implement SOAR**: Security orchestration, automation, and response capabilities
4. **Use Infrastructure as Code**: Ensure consistent security configurations
5. **Continuous Monitoring**: Real-time visibility into security posture and threats

## Key Performance Indicators (KPIs)

### Vulnerability Management Metrics:
- Mean time to detect vulnerabilities (MTTD)
- Mean time to remediate vulnerabilities (MTTR)
- Vulnerability remediation rate and backlog
- Critical vulnerability exposure time

### Security Posture Metrics:
- Security baseline compliance rate
- Patch deployment success rate
- Security incident frequency and impact
- Attack surface reduction measurements

### Operational Metrics:
- Automated security control coverage
- Security tool integration effectiveness
- Security team productivity and efficiency
- Cost of security operations and tools

## Technology-Specific Considerations

### EC2 Instance Security:
- Use AWS Systems Manager for patch management
- Implement Amazon Inspector for vulnerability assessment
- Deploy GuardDuty for runtime threat detection
- Use AWS Config for configuration compliance

### Container Security:
- Scan images with Amazon ECR vulnerability scanning
- Implement runtime protection with GuardDuty for EKS
- Use AWS Fargate for serverless container security
- Establish secure container image pipelines

### Serverless Security:
- Implement function-level permissions and policies
- Use AWS X-Ray for application tracing and monitoring
- Secure function dependencies and third-party libraries
- Monitor function execution and resource usage

### Database Security:
- Enable encryption at rest and in transit
- Implement database activity monitoring
- Use AWS Secrets Manager for credential management
- Regular security assessments and compliance checks

## Related resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html">AWS Well-Architected Framework - Security Pillar</a></li>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/sec-06.html">SEC06: How do you protect your compute resources?</a></li>
    <li><a href="https://docs.aws.amazon.com/inspector/latest/userguide/inspector_introduction.html">Amazon Inspector User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/systems-manager/latest/userguide/what-is-systems-manager.html">AWS Systems Manager User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/guardduty/latest/ug/what-is-guardduty.html">Amazon GuardDuty User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/AmazonECR/latest/userguide/what-is-ecr.html">Amazon ECR User Guide</a></li>
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
