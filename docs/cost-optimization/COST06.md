---
title: COST06 - How do you meet cost targets when you select resource type, size and number?
layout: default
parent: Cost Optimization
nav_order: 6
has_children: true
---

<div class="pillar-header">
  <h1>COST06: How do you meet cost targets when you select resource type, size and number?</h1>
  <p>Ensure that you choose the appropriate resource type, size, and number of resources for your workload to meet cost targets. Use data-driven approaches, cost modeling, and load testing to make informed decisions about resource selection and sizing.</p>
</div>

## Overview

Meeting cost targets when selecting resources requires a systematic approach that combines cost modeling, data-driven decision making, automated optimization, and performance validation. This involves understanding your workload requirements, modeling different resource configurations, and continuously optimizing based on actual usage patterns and performance metrics.

## Key Principles

**Data-Driven Decisions**: Base resource selection on actual usage data, performance metrics, and cost analysis rather than assumptions or over-provisioning for worst-case scenarios.

**Cost Modeling**: Use comprehensive cost models that account for all cost components including compute, storage, network, and operational overhead to make informed resource selection decisions.

**Automated Optimization**: Implement automated systems that can adjust resource type, size, and number based on real-time metrics and predefined cost targets.

**Performance Validation**: Use load testing and performance monitoring to validate that selected resources meet both cost targets and performance requirements.

## Best Practices

<div class="best-practice">
  <h4><a href="COST06-BP01.html">COST06-BP01: Perform cost modeling</a></h4>
  <p>Create comprehensive cost models that help you understand the cost implications of different resource configurations and make informed decisions about resource selection to meet cost targets.</p>
</div>

<div class="best-practice">
  <h4><a href="COST06-BP02.html">COST06-BP02: Select resource type, size, and number based on data</a></h4>
  <p>Use actual usage data, performance metrics, and workload characteristics to make informed decisions about resource type, size, and number rather than relying on assumptions or over-provisioning.</p>
</div>

<div class="best-practice">
  <h4><a href="COST06-BP03.html">COST06-BP03: Select resource type, size, and number automatically based on metrics</a></h4>
  <p>Implement automated systems that can dynamically adjust resource configurations based on real-time metrics, cost targets, and performance requirements.</p>
</div>

<div class="best-practice">
  <h4><a href="COST06-BP04.html">COST06-BP04: Load test your workload</a></h4>
  <p>Use load testing to validate that your selected resource configurations can meet performance requirements while staying within cost targets under various load conditions.</p>
</div>

## Implementation Strategy

### 1. Establish Cost Modeling Framework
- Create comprehensive cost models for different resource types
- Include all cost components (compute, storage, network, operational)
- Model different usage scenarios and growth patterns
- Validate models against actual costs regularly

### 2. Implement Data Collection
- Set up comprehensive monitoring and metrics collection
- Gather usage patterns, performance data, and cost information
- Create data pipelines for analysis and decision making
- Establish baselines and benchmarks for comparison

### 3. Develop Automated Optimization
- Implement auto-scaling based on cost and performance metrics
- Create policies for automated resource selection and sizing
- Set up alerts and notifications for cost target deviations
- Build feedback loops for continuous optimization

### 4. Establish Testing and Validation
- Create comprehensive load testing frameworks
- Test different resource configurations under various conditions
- Validate cost and performance trade-offs
- Document findings and optimization opportunities

## AWS Services to Consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Pricing Calculator</h4>
    <p>Model costs for different resource configurations and scenarios. Use the calculator to understand cost implications of different resource choices and optimize for cost targets.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Compute Optimizer</h4>
    <p>Get rightsizing recommendations based on actual usage data. Use Compute Optimizer to identify optimal resource types and sizes for your workloads.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon CloudWatch</h4>
    <p>Monitor resource utilization and performance metrics. Use CloudWatch data to make informed decisions about resource sizing and optimization.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Auto Scaling</h4>
    <p>Automatically adjust resource capacity based on demand and cost targets. Use Auto Scaling to optimize resource usage and costs dynamically.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Cost Explorer</h4>
    <p>Analyze cost trends and patterns to inform resource selection decisions. Use Cost Explorer to understand the cost impact of different resource configurations.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Load Testing Solutions</h4>
    <p>Test workload performance under different load conditions. Use load testing to validate resource configurations and optimize for cost-performance balance.</p>
  </div>
</div>

## Common Anti-Patterns

**Over-provisioning for Peak**: Provisioning resources for peak load without considering cost optimization strategies like auto-scaling or spot instances.

**Assumption-Based Sizing**: Making resource selection decisions based on assumptions rather than actual data and performance requirements.

**Ignoring Cost in Performance Testing**: Focusing only on performance metrics during testing without considering cost implications of different resource configurations.

**Static Resource Allocation**: Using fixed resource allocations without implementing dynamic optimization based on changing requirements and usage patterns.

**Incomplete Cost Modeling**: Creating cost models that don't account for all cost components or fail to consider operational and indirect costs.

## Success Metrics

- **Cost Target Achievement**: Percentage of workloads meeting defined cost targets
- **Resource Utilization**: Average utilization rates across different resource types
- **Cost per Transaction**: Cost efficiency metrics for business transactions
- **Rightsizing Accuracy**: Percentage of resources that are appropriately sized
- **Automated Optimization Coverage**: Percentage of resources under automated optimization

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/cost_type_size_number.html">AWS Well-Architected Framework - How do you meet cost targets when you select resource type, size and number?</a></li>
    <li><a href="https://calculator.aws/">AWS Pricing Calculator</a></li>
    <li><a href="https://aws.amazon.com/compute-optimizer/">AWS Compute Optimizer</a></li>
    <li><a href="https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html">Amazon CloudWatch User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/autoscaling/application/userguide/what-is-application-auto-scaling.html">AWS Auto Scaling User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/cost-management/latest/userguide/ce-what-is.html">AWS Cost Explorer User Guide</a></li>
    <li><a href="https://aws.amazon.com/solutions/implementations/distributed-load-testing-on-aws/">Distributed Load Testing on AWS</a></li>
    <li><a href="https://aws.amazon.com/blogs/aws-cost-management/">AWS Cost Management Blog</a></li>
  </ul>
</div>

<style>
.pillar-header {
  background-color: #e8f5e8;
  border-left: 5px solid #2d7d2d;
}

.pillar-header h1 {
  color: #2d7d2d;
}

.best-practice h4 a {
  color: #2d7d2d;
  text-decoration: none;
}

.best-practice h4 a:hover {
  text-decoration: underline;
}

.aws-service-content h4 {
  color: #2d7d2d;
}

.related-resources {
  background-color: #e8f5e8;
}

.related-resources h2 {
  color: #2d7d2d;
}
</style>