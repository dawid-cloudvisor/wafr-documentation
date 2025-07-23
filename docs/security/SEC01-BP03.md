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

Control objectives are the specific goals and outcomes that your security controls are designed to achieve. Identifying and validating these objectives ensures that your security controls are effective and aligned with your compliance requirements and risk management strategy.

### Key steps for implementing this best practice:

1. **Identify compliance requirements**:
   - Determine which regulatory frameworks apply to your workload (e.g., GDPR, HIPAA, PCI DSS)
   - Identify industry standards relevant to your organization (e.g., ISO 27001, NIST)
   - Document internal security policies and requirements

2. **Conduct threat modeling**:
   - Identify potential threats to your workload
   - Assess the likelihood and impact of each threat
   - Prioritize threats based on risk

3. **Define control objectives**:
   - Map compliance requirements to specific control objectives
   - Align control objectives with identified threats
   - Ensure control objectives are specific, measurable, and achievable

4. **Implement security controls**:
   - Select controls that address your control objectives
   - Implement technical, administrative, and physical controls as needed
   - Document how each control maps to control objectives

5. **Validate controls**:
   - Test controls to ensure they function as expected
   - Conduct regular assessments of control effectiveness
   - Use automated tools to continuously validate controls where possible

6. **Monitor and improve**:
   - Regularly review control objectives and controls
   - Update controls as threats and compliance requirements evolve
   - Implement a continuous improvement process

## AWS services to consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Audit Manager</h4>
    <p>Helps you continuously audit your AWS usage to simplify how you assess risk and compliance with regulations and industry standards.</p>
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
    <p>Enables you to assess, audit, and evaluate the configurations of your AWS resources. Helps you maintain compliance with internal policies and regulatory standards.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon Inspector</h4>
    <p>Automated security assessment service that helps improve the security and compliance of applications deployed on AWS.</p>
  </div>
</div>

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/sec_securely_operate_workload_control_objectives.html">AWS Well-Architected Framework - Identify and validate control objectives</a></li>
    <li><a href="https://aws.amazon.com/compliance/programs/">AWS Compliance Programs</a></li>
    <li><a href="https://docs.aws.amazon.com/audit-manager/latest/userguide/what-is.html">AWS Audit Manager User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/securityhub/latest/userguide/what-is-securityhub.html">AWS Security Hub User Guide</a></li>
  </ul>
</div>
