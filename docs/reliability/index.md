---
title: Reliability
layout: default
nav_order: 3
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
  <div class="question-card">
    <h3>REL01 - How do you manage service quotas and constraints?</h3>
    <a href="REL01.html">View details →</a>
  </div>
  <div class="question-card">
    <h3>REL02 - How do you plan your network topology?</h3>
    <a href="REL02.html">View details →</a>
  </div>
  <div class="question-card">
    <h3>REL03 - How do you design your workload service architecture?</h3>
    <a href="REL03.html">View details →</a>
  </div>
  <div class="question-card">
    <h3>REL04 - How do you design interactions in a distributed system to prevent failures?</h3>
    <a href="REL04.html">View details →</a>
  </div>
  <div class="question-card">
    <h3>REL05 - How do you design interactions in a distributed system to mitigate or withstand failures?</h3>
    <a href="REL05.html">View details →</a>
  </div>
  <div class="question-card">
    <h3>REL06 - How do you monitor workload resources?</h3>
    <a href="REL06.html">View details →</a>
  </div>
  <div class="question-card">
    <h3>REL07 - How do you design your workload to adapt to changes in demand?</h3>
    <a href="REL07.html">View details →</a>
  </div>
  <div class="question-card">
    <h3>REL08 - How do you implement change?</h3>
    <a href="REL08.html">View details →</a>
  </div>
  <div class="question-card">
    <h3>REL09 - How do you back up data?</h3>
    <a href="REL09.html">View details →</a>
  </div>
  <div class="question-card">
    <h3>REL10 - How do you use fault isolation to protect your workload?</h3>
    <a href="REL10.html">View details →</a>
  </div>
  <div class="question-card">
    <h3>REL11 - How do you design your workload to withstand component failures?</h3>
    <a href="REL11.html">View details →</a>
  </div>
  <div class="question-card">
    <h3>REL12 - How do you test reliability?</h3>
    <a href="REL12.html">View details →</a>
  </div>
  <div class="question-card">
    <h3>REL13 - How do you plan for disaster recovery?</h3>
    <a href="REL13.html">View details →</a>
  </div>
</div>

## AWS Services for Reliability

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