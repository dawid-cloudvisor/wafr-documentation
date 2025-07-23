---
title: Operational Excellence
layout: default
nav_order: 2
has_children: true
permalink: /docs/operational-excellence
---

<div class="pillar-header">
  <h1>Operational Excellence Pillar</h1>
  <p>The operational excellence pillar focuses on running and monitoring systems to deliver business value, and continually improving processes and procedures.</p>
</div>

The Operational Excellence pillar includes the ability to support development and run workloads effectively, gain insight into their operations, and to continuously improve supporting processes and procedures to deliver business value.

## Key Areas

The Operational Excellence pillar includes the following key areas:

- **Organization** - How teams are structured and how they collaborate
- **Prepare** - Design for operations and understand workload health
- **Operate** - Understand workload health and achieve operational success
- **Evolve** - Learn, share, and continuously improve

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
    <h4>AWS CloudFormation</h4>
    <p>Provides a common language to model and provision AWS and third-party resources in your cloud environment.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Config</h4>
    <p>Enables you to assess, audit, and evaluate the configurations of your AWS resources.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS CloudTrail</h4>
    <p>Enables governance, compliance, operational auditing, and risk auditing of your AWS account.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon CloudWatch</h4>
    <p>Monitors your AWS resources and the applications you run on AWS in real time.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Systems Manager</h4>
    <p>Gives you visibility and control of your infrastructure on AWS.</p>
  </div>
</div>

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/welcome.html">AWS Well-Architected Framework - Operational Excellence Pillar</a></li>
    <li><a href="https://aws.amazon.com/architecture/well-architected/">AWS Well-Architected</a></li>
    <li><a href="https://aws.amazon.com/devops/">DevOps on AWS</a></li>
  </ul>
</div>