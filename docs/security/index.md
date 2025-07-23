---
title: Security
layout: default
nav_order: 2
has_children: true
permalink: /docs/security
---

<div class="pillar-header">
  <h1>Security Pillar</h1>
  <p>The security pillar focuses on protecting information and systems. Key topics include confidentiality and integrity of data, identifying and managing who can do what with privilege management, protecting systems, and establishing controls to detect security events.</p>
</div>

The Security pillar includes the ability to support development and run workloads effectively, gain insight into their operations, and to continuously improve supporting processes and procedures to deliver business value.

## Key Areas

The Security pillar includes the following key areas:

- **Security Foundations** - Implementing a strong identity foundation
- **Identity and Access Management** - Ensuring only authorized and authenticated users can access your resources
- **Detection** - Implementing monitoring, alerting, and audit actions
- **Infrastructure Protection** - Protecting systems and services within your workload
- **Data Protection** - Classifying data and implementing controls to protect it
- **Incident Response** - Responding to and mitigating the potential impact of security incidents

## Questions

The AWS Well-Architected Framework provides a set of questions that allows you to review an existing or proposed architecture. It also provides a set of AWS best practices for each pillar.

<div class="question-cards">
  {% for child in site.pages %}
    {% if child.parent == page.title %}
      <div class="question-card">
        <h3>{{ child.title }}</h3>
        <a href="{{ child.url | absolute_url }}">View details →</a>
      </div>
    {% endif %}
  {% endfor %}
</div>

## AWS Services for {title}

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Identity and Access Management (IAM)</h4>
    <p>Enables you to manage access to AWS services and resources securely.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon GuardDuty</h4>
    <p>Provides intelligent threat detection for your AWS accounts and workloads.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Security Hub</h4>
    <p>Gives you a comprehensive view of your security alerts and security posture across your AWS accounts.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Key Management Service (KMS)</h4>
    <p>Makes it easy for you to create and manage cryptographic keys and control their use.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Shield</h4>
    <p>Provides protection against DDoS attacks for applications running on AWS.</p>
  </div>
</div>

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html">AWS Well-Architected Framework - Security Pillar</a></li>
    <li><a href="https://docs.aws.amazon.com/security/">AWS Security Documentation</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/">AWS Security Blog</a></li>
  </ul>
</div>