---
title: Reliability
layout: default
nav_order: 2
has_children: true
permalink: /docs/reliability
---

<div class="pillar-header">
  <h1>Reliability Pillar</h1>
  <p>The reliability pillar focuses on ensuring a workload performs its intended function correctly and consistently when it's expected to. This includes the ability to operate and test the workload through its total lifecycle.</p>
</div>

The Reliability pillar includes the ability to support development and run workloads effectively, gain insight into their operations, and to continuously improve supporting processes and procedures to deliver business value.

## Key Areas

The Reliability pillar includes the following key areas:

- **Foundations** - Managing service quotas and network topology
- **Workload Architecture** - Designing distributed systems that withstand failures
- **Change Management** - Monitoring resources and implementing controlled changes
- **Failure Management** - Backing up data, designing for fault isolation, and planning for disaster recovery

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
    <h4>Amazon CloudWatch</h4>
    <p>Monitors your AWS resources and the applications you run on AWS in real time.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Auto Scaling</h4>
    <p>Monitors your applications and automatically adjusts capacity to maintain steady, predictable performance.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon RDS</h4>
    <p>Makes it easy to set up, operate, and scale a relational database in the cloud with high availability.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Elastic Disaster Recovery</h4>
    <p>Minimizes downtime and data loss with fast, reliable recovery of on-premises and cloud-based applications.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Backup</h4>
    <p>Centrally manages and automates backups across AWS services.</p>
  </div>
</div>

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html">AWS Well-Architected Framework - Reliability Pillar</a></li>
    <li><a href="https://aws.amazon.com/reliability/">Reliability on AWS</a></li>
    <li><a href="https://aws.amazon.com/blogs/architecture/">AWS Architecture Blog</a></li>
  </ul>
</div>