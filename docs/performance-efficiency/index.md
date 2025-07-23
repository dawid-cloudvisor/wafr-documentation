---
title: Performance Efficiency
layout: default
nav_order: 2
has_children: true
permalink: /docs/performance-efficiency
---

<div class="pillar-header">
  <h1>Performance Efficiency Pillar</h1>
  <p>The performance efficiency pillar focuses on using IT and computing resources efficiently. Key topics include selecting the right resource types and sizes based on workload requirements, monitoring performance, and making informed decisions to maintain efficiency as business needs evolve.</p>
</div>

The Performance Efficiency pillar includes the ability to support development and run workloads effectively, gain insight into their operations, and to continuously improve supporting processes and procedures to deliver business value.

## Key Areas

The Performance Efficiency pillar includes the following key areas:

- **Selection** - Choosing the right compute, storage, database, and networking solutions
- **Review** - Continuously evaluating new services and technologies
- **Monitoring** - Ensuring resources are performing as expected
- **Tradeoffs** - Using caching, partitioning, and other techniques to improve performance

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
    <h4>Amazon EC2</h4>
    <p>Provides resizable compute capacity in the cloud with a wide selection of instance types.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon S3</h4>
    <p>Object storage built to store and retrieve any amount of data from anywhere.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon RDS</h4>
    <p>Makes it easy to set up, operate, and scale a relational database in the cloud.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon DynamoDB</h4>
    <p>Fast and flexible NoSQL database service for any scale.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon CloudFront</h4>
    <p>Fast content delivery network (CDN) service that securely delivers data, videos, applications, and APIs.</p>
  </div>
</div>

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/performance-efficiency-pillar/welcome.html">AWS Well-Architected Framework - Performance Efficiency Pillar</a></li>
    <li><a href="https://aws.amazon.com/architecture/well-architected/performance-efficiency/">AWS Performance Efficiency</a></li>
    <li><a href="https://aws.amazon.com/blogs/compute/">AWS Compute Blog</a></li>
  </ul>
</div>