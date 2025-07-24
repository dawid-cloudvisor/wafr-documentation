---
title: SEC01 - How do you securely operate your workload?
layout: default
parent: Security
has_children: true
nav_order: 1
---

<div class="pillar-header">
  <h1>SEC01: How do you securely operate your workload?</h1>
  <p>To securely operate your workload, you must apply overarching best practices to every area of security. Take requirements and processes that you have defined in operational excellence at an organizational and workload level, and apply them to all areas.</p>
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

## AWS Services to Consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Organizations</h4>
    <p>Centrally manage and govern your environment as you scale your AWS resources.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Control Tower</h4>
    <p>Set up and govern a secure, compliant multi-account AWS environment based on best practices.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Security Hub</h4>
    <p>Provides a comprehensive view of your security state in AWS and helps you check your compliance with security standards.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon GuardDuty</h4>
    <p>Provides intelligent threat detection for your AWS accounts and workloads.</p>
  </div>
</div>

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html">AWS Well-Architected Framework - Security Pillar</a></li>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/sec-01.html">SEC01: How do you securely operate your workload?</a></li>
    <li><a href="https://aws.amazon.com/architecture/security-identity-compliance/">AWS Security, Identity, and Compliance Architecture</a></li>
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
