---
title: Cost Optimization
layout: default
nav_order: 2
has_children: true
permalink: /docs/cost-optimization
---

<div class="pillar-header">
  <h1>Cost Optimization Pillar</h1>
  <p>The cost optimization pillar focuses on avoiding unnecessary costs. Key topics include understanding and controlling where money is being spent, selecting the most appropriate and right number of resource types, analyzing spend over time, and scaling to meet business needs without overspending.</p>
</div>

The Cost Optimization pillar includes the ability to support development and run workloads effectively, gain insight into their operations, and to continuously improve supporting processes and procedures to deliver business value.

## Key Areas

The Cost Optimization pillar includes the following key areas:

- **Practice Cloud Financial Management** - Implementing organizational processes for cost management
- **Expenditure and Usage Awareness** - Increasing visibility and accountability
- **Cost-Effective Resources** - Using the appropriate services and resources for your workload
- **Manage Demand and Supply Resources** - Scaling resources to match business requirements
- **Optimize Over Time** - Continuously reviewing and refining your cost optimization approach

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
    <h4>AWS Cost Explorer</h4>
    <p>Visualize, understand, and manage your AWS costs and usage over time.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Budgets</h4>
    <p>Set custom cost and usage budgets that alert you when your budget thresholds are exceeded.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Cost and Usage Report</h4>
    <p>Access comprehensive cost and usage data for your AWS account.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Trusted Advisor</h4>
    <p>Provides recommendations that help you follow AWS best practices for cost optimization.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Compute Optimizer</h4>
    <p>Recommends optimal AWS resources for your workloads to reduce costs.</p>
  </div>
</div>

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/welcome.html">AWS Well-Architected Framework - Cost Optimization Pillar</a></li>
    <li><a href="https://aws.amazon.com/aws-cost-management/">AWS Cost Management</a></li>
    <li><a href="https://aws.amazon.com/aws-cost-management/cost-optimization-hub/">AWS Cost Optimization Hub</a></li>
  </ul>
</div>