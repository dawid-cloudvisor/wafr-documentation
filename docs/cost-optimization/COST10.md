---
title: COST10 - How do you evaluate new services?
layout: default
parent: Cost Optimization
nav_order: 10
has_children: true
---

<div class="pillar-header">
  <h1>COST10: How do you evaluate new services?</h1>
  <p>Establish systematic processes to evaluate new AWS services and features for cost optimization opportunities. Regular evaluation ensures you can take advantage of new services that provide better cost efficiency, performance, or functionality for your workloads.</p>
</div>

## Overview

Evaluating new services involves establishing systematic processes to stay current with AWS service innovations, assess their applicability to your workloads, and implement them when they provide cost or operational benefits. This continuous evaluation ensures your architecture remains optimized as AWS evolves and new services become available.

The evaluation process includes monitoring AWS announcements, conducting thorough workload reviews, performing cost-benefit analysis, and implementing controlled adoption strategies. By developing comprehensive workload review processes, organizations can systematically identify optimization opportunities and make informed decisions about new service adoption.

Key aspects of new service evaluation include:
- **Service Discovery**: Monitoring AWS announcements and identifying relevant new services
- **Workload Assessment**: Analyzing current workloads to identify optimization opportunities  
- **Cost-Benefit Analysis**: Evaluating the financial impact of adopting new services
- **Risk Assessment**: Understanding implementation risks and mitigation strategies
- **Pilot Testing**: Conducting controlled tests before full production adoption
- **Implementation Planning**: Developing systematic rollout strategies

## Key Principles

**Continuous Innovation**: Stay informed about new AWS services, features, and pricing models that could benefit your workloads and reduce costs.

**Systematic Evaluation**: Implement structured processes to evaluate new services against your current architecture, considering cost, performance, and operational impact.

**Risk-Managed Adoption**: Use controlled testing and gradual rollout strategies to safely adopt new services while minimizing risk to production workloads.

**Cost-Benefit Analysis**: Perform comprehensive cost-benefit analysis that includes migration costs, operational changes, and long-term benefits.

**Regular Review Cycles**: Establish regular review processes to continuously evaluate your architecture against new service offerings and optimization opportunities.

## Best Practices

<div class="best-practice">
  <h4><a href="COST10-BP01.html">COST10-BP01: Develop a workload review process</a></h4>
  <p>Establish systematic processes to regularly review workloads for new service adoption opportunities. Create comprehensive frameworks for evaluating new AWS services, conducting workload assessments, and implementing optimization recommendations based on evolving service offerings.</p>
</div>

<div class="best-practice">
  <h4><a href="COST10-BP02.html">COST10-BP02: Review and analyze this workload regularly</a></h4>
  <p>Implement regular review cycles to analyze workloads against new AWS services, features, and best practices. Use automated analysis frameworks to identify optimization opportunities, track performance trends, and ensure continued cost efficiency.</p>
</div>

<div class="best-practice">
  <h4><a href="COST10-BP03.html">COST10-BP03: Implement new service evaluation automation</a></h4>
  <p>Create automated systems to monitor AWS service announcements, evaluate their relevance to your workloads, and generate recommendations for potential adoption opportunities. Use intelligent filtering and machine learning to prioritize the most valuable optimization opportunities.</p>
</div>

## Workload Review Framework

### Review Process Components
- **Discovery Phase**: Monitor AWS service announcements and identify potential optimization opportunities
- **Assessment Phase**: Evaluate new services against workload requirements and current architecture
- **Planning Phase**: Develop implementation roadmaps and cost-benefit analysis
- **Decision Phase**: Make informed go/no-go decisions based on comprehensive analysis

### Review Types and Frequency
- **Comprehensive Reviews**: Annual full architecture assessments (4-6 weeks duration)
- **Focused Reviews**: Quarterly optimization-focused evaluations (2-3 weeks duration)  
- **Rapid Reviews**: Monthly new service assessments (1 week duration)
- **Triggered Reviews**: Event-driven evaluations based on cost spikes or service announcements

### Evaluation Criteria Framework
- **Cost Impact** (30% weight): Direct cost comparison, migration costs, total cost of ownership
- **Technical Fit** (25% weight): Functional alignment, performance characteristics, integration complexity
- **Implementation Effort** (20% weight): Migration complexity, skill requirements, timeline constraints
- **Risk Assessment** (15% weight): Technical risks, business continuity impact, compliance implications
- **Strategic Alignment** (10% weight): Business objectives alignment, competitive advantage potential

## Implementation Strategy

### 1. Establish Review Framework
- Create systematic processes for evaluating new services
- Define evaluation criteria and decision frameworks
- Establish regular review schedules and responsibilities
- Set up information gathering and monitoring systems

### 2. Implement Evaluation Processes
- Monitor AWS service announcements and updates
- Assess new services against current workload requirements
- Perform cost-benefit analysis for potential adoptions
- Create pilot programs for testing new services

### 3. Enable Continuous Optimization
- Implement regular workload review cycles
- Track optimization opportunities and implementation progress
- Measure and report on optimization outcomes
- Share learnings and best practices across teams

### 4. Manage Change and Risk
- Use controlled testing and gradual rollout strategies
- Implement rollback capabilities for new service adoptions
- Monitor performance and cost impacts of changes
- Document decisions and lessons learned

## Service Evaluation Categories

**Cost Optimization Services**: New services that can directly reduce costs through better pricing models, improved efficiency, or reduced operational overhead.

**Performance Enhancement Services**: Services that improve performance while maintaining or reducing costs, providing better value for money.

**Operational Simplification Services**: Managed services that reduce operational complexity and associated costs while maintaining functionality.

**Emerging Technologies**: New technologies and services that may provide future cost optimization opportunities or competitive advantages.

**Regional Expansions**: New service availability in different regions that may provide cost or performance benefits.

## AWS Services to Consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS What's New</h4>
    <p>Stay updated on new AWS services and features. Subscribe to AWS What's New to receive notifications about service launches and updates that may benefit your workloads.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Pricing Calculator</h4>
    <p>Model costs for new services and compare them with existing solutions. Use the calculator to evaluate the financial impact of adopting new services.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Cost Explorer</h4>
    <p>Analyze current costs to identify areas where new services might provide optimization opportunities. Use Cost Explorer to understand baseline costs for comparison.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Well-Architected Tool</h4>
    <p>Evaluate workloads against Well-Architected principles and identify opportunities for new service adoption. Use the tool to track optimization progress.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Trusted Advisor</h4>
    <p>Get recommendations for cost optimization and new service adoption opportunities. Use Trusted Advisor insights to identify potential improvements.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Config</h4>
    <p>Track configuration changes and compliance with best practices. Use Config to monitor the impact of new service adoptions on your architecture.</p>
  </div>
</div>

## Common Anti-Patterns

**Ad-Hoc Evaluation**: Evaluating new services only when problems arise, missing proactive optimization opportunities.

**Lack of Systematic Process**: Not having structured processes for service evaluation, leading to inconsistent or incomplete assessments.

**Ignoring Migration Costs**: Focusing only on operational cost savings without considering migration and implementation costs.

**Fear of Change**: Avoiding new services due to risk aversion, missing significant optimization opportunities.

**Incomplete Testing**: Not thoroughly testing new services before production adoption, leading to unexpected issues or costs.

## Success Metrics

- **Service Adoption Rate**: Number of new services evaluated and adopted per quarter
- **Cost Optimization Impact**: Cost savings achieved through new service adoption
- **Review Cycle Compliance**: Percentage of workloads reviewed according to schedule
- **Time to Value**: Time from service evaluation to production implementation
- **Optimization Opportunity Identification**: Number of optimization opportunities identified through reviews

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/cost_evaluate_new_services.html">AWS Well-Architected Framework - How do you evaluate new services?</a></li>
    <li><a href="https://aws.amazon.com/new/">AWS What's New</a></li>
    <li><a href="https://calculator.aws/">AWS Pricing Calculator</a></li>
    <li><a href="https://docs.aws.amazon.com/cost-management/latest/userguide/ce-what-is.html">AWS Cost Explorer User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/userguide/intro.html">AWS Well-Architected Tool User Guide</a></li>
    <li><a href="https://aws.amazon.com/premiumsupport/technology/trusted-advisor/">AWS Trusted Advisor</a></li>
    <li><a href="https://docs.aws.amazon.com/config/latest/developerguide/WhatIsConfig.html">AWS Config Developer Guide</a></li>
    <li><a href="https://aws.amazon.com/blogs/">AWS Blogs</a></li>
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