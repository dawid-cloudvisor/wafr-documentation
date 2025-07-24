---
title: SEC11 - How do you incorporate and validate the security properties of applications throughout the design, development, and deployment lifecycle?
layout: default
parent: Security
has_children: true
nav_order: 11
---

<div class="pillar-header">
  <h1>SEC11: How do you incorporate and validate the security properties of applications throughout the design, development, and deployment lifecycle?</h1>
  <p>Training people, testing your security properties, and validating that you are meeting your security requirements are key elements to consider when developing any application. Adopting application security testing as a regular part of your software development lifecycle (SDLC) and post-deployment processes help validate that you're implementing security controls properly. Your application security testing should also be performed regularly as part of your security assessment processes.</p>
</div>

## Best Practices

This question includes the following best practices:

<div class="best-practices-list">
  <ul>
    <li><a href="./SEC11-BP01.html">SEC11-BP01: Train for application security</a></li>
    <li><a href="./SEC11-BP02.html">SEC11-BP02: Automate testing throughout the development and release lifecycle</a></li>
    <li><a href="./SEC11-BP03.html">SEC11-BP03: Perform regular penetration testing</a></li>
    <li><a href="./SEC11-BP04.html">SEC11-BP04: Manual code reviews</a></li>
    <li><a href="./SEC11-BP05.html">SEC11-BP05: Centralize services for packages and dependencies</a></li>
    <li><a href="./SEC11-BP06.html">SEC11-BP06: Deploy software programmatically</a></li>
    <li><a href="./SEC11-BP07.html">SEC11-BP07: Regularly assess security properties of the pipelines</a></li>
    <li><a href="./SEC11-BP08.html">SEC11-BP08: Plan security testing for unusual circumstances</a></li>
  </ul>
</div>

## Key Concepts

### Application Security Fundamentals

**Security by Design**: Integrate security considerations from the earliest stages of application design and architecture. Security should be a fundamental requirement, not an afterthought added during or after development.

**Shift-Left Security**: Move security testing and validation activities earlier in the development lifecycle. Early detection and remediation of security issues is more cost-effective and reduces risk.

**DevSecOps Integration**: Seamlessly integrate security practices, tools, and responsibilities into DevOps workflows. Security becomes everyone's responsibility, not just the security team's.

**Continuous Security Validation**: Implement ongoing security testing and validation throughout the application lifecycle, from development through production deployment and maintenance.

### Application Security Lifecycle

**Design Phase**: Incorporate threat modeling, security requirements definition, and secure architecture design. Establish security controls and design patterns that will be implemented throughout development.

**Development Phase**: Implement secure coding practices, conduct code reviews, and perform static application security testing (SAST). Ensure developers have the training and tools needed for secure development.

**Testing Phase**: Execute comprehensive security testing including dynamic application security testing (DAST), interactive application security testing (IAST), and dependency scanning.

**Deployment Phase**: Validate security configurations, perform final security assessments, and ensure secure deployment practices. Implement runtime application self-protection (RASP) where appropriate.

**Operations Phase**: Maintain ongoing security monitoring, conduct regular security assessments, and respond to newly discovered vulnerabilities in production applications.

## AWS Services to Consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon CodeGuru</h4>
    <p>Provides intelligent recommendations for improving code quality and identifying the most expensive lines of code. Includes security-focused code reviews and recommendations.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS CodeBuild</h4>
    <p>Fully managed continuous integration service that compiles source code, runs tests, and produces software packages. Integrates security testing tools into build pipelines.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS CodePipeline</h4>
    <p>Fully managed continuous delivery service that helps you automate your release pipelines. Enables integration of security testing and validation at multiple pipeline stages.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon Inspector</h4>
    <p>Automatically assesses applications for exposure, vulnerabilities, and deviations from best practices. Provides continuous vulnerability assessment for applications and infrastructure.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Security Hub</h4>
    <p>Provides a comprehensive view of your security state in AWS. Centralizes security findings from application security testing tools and provides compliance dashboards.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Systems Manager</h4>
    <p>Gives you visibility and control of your infrastructure on AWS. Provides patch management and configuration management capabilities for application security.</p>
  </div>
</div>

## Implementation Approach

### 1. Security Training and Culture
- Establish comprehensive security training programs for development teams
- Implement security champions programs within development organizations
- Create security coding standards and guidelines
- Provide hands-on security training and workshops
- Foster a culture of security awareness and responsibility

### 2. Secure Development Lifecycle Integration
- Integrate security requirements into project planning and design phases
- Implement threat modeling processes for new applications and features
- Establish secure coding practices and code review procedures
- Deploy automated security testing tools in development environments
- Create security gates and approval processes in release pipelines

### 3. Automated Security Testing
- Implement static application security testing (SAST) in development workflows
- Deploy dynamic application security testing (DAST) in staging environments
- Configure dependency and vulnerability scanning for third-party components
- Set up container image security scanning for containerized applications
- Implement infrastructure as code security scanning

### 4. Continuous Security Validation
- Establish regular penetration testing and security assessments
- Implement continuous monitoring and runtime security protection
- Create feedback loops from production security events to development teams
- Maintain security metrics and reporting dashboards
- Conduct regular security architecture reviews and updates

## Application Security Architecture

### Secure Development Lifecycle Integration
```
Requirements & Design
    ↓ (Threat Modeling, Security Requirements)
Development
    ↓ (Secure Coding, SAST, Code Reviews)
Testing
    ↓ (DAST, IAST, Penetration Testing)
Deployment
    ↓ (Security Configuration, Final Assessment)
Operations
    ↓ (Runtime Monitoring, Continuous Assessment)
```

### DevSecOps Pipeline Integration
```
Source Code Repository
    ↓ (Pre-commit Hooks, SAST)
Build Pipeline (CodeBuild)
    ↓ (Dependency Scanning, Container Scanning)
Test Environment
    ↓ (DAST, Integration Testing)
Security Gate
    ↓ (Security Approval, Risk Assessment)
Production Deployment
    ↓ (Runtime Protection, Monitoring)
```

### Security Testing Pyramid
```
Manual Security Testing
    ↓ (Penetration Testing, Security Reviews)
Integration Security Testing
    ↓ (DAST, IAST, API Testing)
Unit Security Testing
    ↓ (SAST, Dependency Scanning, Code Analysis)
```

## Application Security Controls Framework

### Preventive Controls
- **Secure Coding Standards**: Established coding guidelines and security patterns
- **Input Validation**: Comprehensive input sanitization and validation
- **Authentication & Authorization**: Strong identity and access controls
- **Encryption**: Data protection in transit and at rest
- **Security Headers**: HTTP security headers and content security policies

### Detective Controls
- **Security Testing**: SAST, DAST, IAST, and penetration testing
- **Vulnerability Scanning**: Regular assessment of application and dependencies
- **Runtime Monitoring**: Application performance and security monitoring
- **Log Analysis**: Security event correlation and analysis
- **Compliance Monitoring**: Adherence to security standards and policies

### Responsive Controls
- **Incident Response**: Application security incident procedures
- **Vulnerability Management**: Rapid patching and remediation processes
- **Security Updates**: Automated security patch deployment
- **Rollback Procedures**: Rapid rollback capabilities for security issues
- **Emergency Response**: Crisis management for critical security vulnerabilities

## Common Challenges and Solutions

### Challenge: Developer Security Skills Gap
**Solution**: Implement comprehensive security training programs, establish security champions within development teams, provide hands-on workshops and labs, and create easily accessible security resources and documentation.

### Challenge: Integration of Security Tools in CI/CD
**Solution**: Use API-driven security tools, implement security as code practices, create reusable security pipeline templates, and establish clear security gates with automated decision-making where possible.

### Challenge: Managing False Positives from Security Tools
**Solution**: Tune security tools for your environment, implement risk-based prioritization, create exception management processes, and use multiple complementary testing approaches.

### Challenge: Balancing Security and Development Velocity
**Solution**: Automate security testing and validation, implement risk-based security gates, provide fast feedback loops to developers, and focus on high-impact security issues.

### Challenge: Third-Party Component Security
**Solution**: Implement software composition analysis (SCA), maintain approved component libraries, establish component update policies, and monitor for newly discovered vulnerabilities.

## Application Security Maturity Levels

### Level 1: Basic Application Security
- Manual security testing and code reviews
- Basic security training for developers
- Ad-hoc security assessments
- Limited integration with development processes

### Level 2: Systematic Application Security
- Automated security testing in CI/CD pipelines
- Regular security training and awareness programs
- Established secure coding standards and guidelines
- Systematic vulnerability management processes

### Level 3: Advanced Application Security
- Comprehensive DevSecOps integration
- Advanced security testing techniques and tools
- Proactive threat modeling and security architecture
- Continuous security monitoring and feedback

### Level 4: Optimized Application Security
- AI/ML-powered security testing and analysis
- Predictive security risk assessment
- Automated security remediation and response
- Continuous security optimization and improvement

## Application Security Best Practices

### Secure Development:
1. **Security Training**: Provide comprehensive security training for all developers
2. **Threat Modeling**: Conduct threat modeling for all applications and major features
3. **Secure Coding**: Implement and enforce secure coding standards and practices
4. **Code Reviews**: Perform security-focused code reviews for all changes
5. **Security Champions**: Establish security champions within development teams

### Security Testing:
1. **Automated Testing**: Integrate automated security testing throughout the pipeline
2. **Multiple Testing Types**: Use SAST, DAST, IAST, and SCA for comprehensive coverage
3. **Regular Assessments**: Conduct regular penetration testing and security assessments
4. **Dependency Management**: Monitor and manage third-party component vulnerabilities
5. **Runtime Protection**: Implement runtime application security monitoring

### Pipeline Security:
1. **Security Gates**: Implement security approval gates in deployment pipelines
2. **Infrastructure Security**: Scan infrastructure as code for security misconfigurations
3. **Container Security**: Implement container image scanning and runtime protection
4. **Deployment Security**: Validate security configurations during deployment
5. **Rollback Capabilities**: Maintain rapid rollback capabilities for security issues

## Key Performance Indicators (KPIs)

### Security Testing Metrics:
- Security test coverage across applications
- Mean time to detect (MTTD) security vulnerabilities
- Mean time to remediate (MTTR) security issues
- False positive rate for security testing tools

### Development Integration Metrics:
- Percentage of code commits with security testing
- Security gate pass/fail rates in CI/CD pipelines
- Developer security training completion rates
- Security issue resolution time in development

### Vulnerability Management Metrics:
- Number of security vulnerabilities by severity
- Vulnerability remediation rates and timelines
- Third-party component vulnerability exposure
- Security debt accumulation and reduction

## Security Testing Types and Tools

### Static Application Security Testing (SAST):
- **Purpose**: Analyze source code for security vulnerabilities
- **Integration**: IDE plugins, pre-commit hooks, CI/CD pipelines
- **Benefits**: Early detection, comprehensive coverage, low false positives
- **Limitations**: Cannot detect runtime issues, requires source code access

### Dynamic Application Security Testing (DAST):
- **Purpose**: Test running applications for security vulnerabilities
- **Integration**: Staging environments, automated testing pipelines
- **Benefits**: Detects runtime issues, no source code required
- **Limitations**: Limited coverage, requires running application

### Interactive Application Security Testing (IAST):
- **Purpose**: Combines SAST and DAST approaches for comprehensive testing
- **Integration**: Application runtime environments, testing frameworks
- **Benefits**: High accuracy, real-time feedback, comprehensive coverage
- **Limitations**: Performance impact, complex implementation

### Software Composition Analysis (SCA):
- **Purpose**: Identify vulnerabilities in third-party components and dependencies
- **Integration**: Build systems, package managers, CI/CD pipelines
- **Benefits**: Comprehensive dependency visibility, license compliance
- **Limitations**: Requires accurate dependency mapping, false positives

## Compliance and Regulatory Considerations

### Industry Standards:
- **OWASP Top 10**: Address the most critical web application security risks
- **SANS Top 25**: Focus on the most dangerous software errors
- **ISO 27001**: Implement information security management systems
- **NIST Cybersecurity Framework**: Align with cybersecurity best practices

### Regulatory Requirements:
- **PCI DSS**: Payment card industry security requirements for applications
- **HIPAA**: Healthcare application security and privacy requirements
- **GDPR**: Data protection requirements for applications processing personal data
- **SOX**: Financial reporting application security and controls

### Compliance Integration:
- **Automated Compliance Checking**: Integrate compliance validation into pipelines
- **Documentation**: Maintain security testing and validation documentation
- **Audit Trails**: Preserve evidence of security testing and remediation activities
- **Reporting**: Generate compliance reports and security metrics dashboards

## Related resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html">AWS Well-Architected Framework - Security Pillar</a></li>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/sec-11.html">SEC11: How do you incorporate and validate the security properties of applications?</a></li>
    <li><a href="https://docs.aws.amazon.com/codeguru/latest/reviewer-ug/welcome.html">Amazon CodeGuru Reviewer User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/codebuild/latest/userguide/welcome.html">AWS CodeBuild User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/codepipeline/latest/userguide/welcome.html">AWS CodePipeline User Guide</a></li>
    <li><a href="https://owasp.org/www-project-top-ten/">OWASP Top 10 Web Application Security Risks</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-build-a-ci-cd-pipeline-for-container-vulnerability-scanning-with-trivy-and-aws-security-hub/">How to build a CI/CD pipeline for container vulnerability scanning</a></li>
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
