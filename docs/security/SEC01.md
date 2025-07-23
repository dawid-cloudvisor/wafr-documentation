---
title: SEC01 - How do you securely operate your workload?
layout: default
parent: Security
nav_order: 1
---

# SEC01: How do you securely operate your workload?

To securely operate your workload, you must apply overarching best practices to every area of security. Take requirements and processes that you have defined in operational excellence at an organizational and workload level, and apply them to all areas.

## Best Practices

### Separate workloads using accounts
Organize workloads in separate accounts and group accounts based on function or common controls, rather than mirroring your reporting structure. Start with security and infrastructure in mind to enable your organization to set common guardrails as your workloads grow.

### Secure AWS account
Secure access to your accounts, for example by enabling MFA and restrict use of the root user, and configure account contacts.

### Keep up to date with security threats
Recognize attack vectors by staying up to date with the latest security threats to help you define and implement appropriate controls.

### Keep up to date with security recommendations
Stay up to date with both AWS and industry security recommendations to evolve the security posture of your workload.

### Automate testing and validation of security controls
Automate testing and validation of all security controls. For example, scan items such as machine images and infrastructure as code templates for security vulnerabilities, irregularities, and drift from an established baseline before they are deployed. Tools and services, such as Amazon Inspector, can be used to automate host and network vulnerability assessments.

### Identify and prioritize risks
Use a risk model to identify and maintain a list of security risks. Prioritize your risks and adjust your security controls to prevent, detect, and respond. Revisit and reprioritize regularly.

### Evaluate and implement new security services and features regularly
Evaluate and implement security services and features from AWS and AWS Partners that allow you to evolve the security posture of your workload.

## Implementation Guidance

1. **Implement AWS Organizations**: Use AWS Organizations to manage and govern your environment as you scale your AWS resources.

2. **Enable Multi-Factor Authentication (MFA)**: Require MFA for all users, especially those with elevated privileges.

3. **Implement least privilege access**: Grant only the permissions needed to perform specific tasks.

4. **Configure AWS Config**: Use AWS Config to assess, audit, and evaluate the configurations of your AWS resources.

5. **Enable AWS CloudTrail**: Monitor and record account activity across your AWS infrastructure.

6. **Implement automated security testing**: Use tools like Amazon Inspector and AWS Security Hub to automate security assessments.

7. **Establish a security incident response plan**: Define processes for responding to security incidents.

## AWS Services to Consider

- **AWS Organizations** - For managing multiple AWS accounts
- **AWS Identity and Access Management (IAM)** - For securely controlling access to AWS services
- **AWS Config** - For assessing, auditing, and evaluating configurations of AWS resources
- **AWS CloudTrail** - For governance, compliance, operational auditing, and risk auditing of your AWS account
- **Amazon GuardDuty** - For threat detection and continuous security monitoring
- **AWS Security Hub** - For comprehensive view of security alerts and security posture across AWS accounts
- **Amazon Inspector** - For automated security assessment service

## Related Resources

- [AWS Well-Architected Framework - Security Pillar](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html)
- [AWS Security Best Practices](https://aws.amazon.com/architecture/security-identity-compliance/)
- [AWS Security Documentation](https://docs.aws.amazon.com/security/)
