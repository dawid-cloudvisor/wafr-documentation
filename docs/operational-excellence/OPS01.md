---
title: OPS01 - How do you determine what your priorities are?
layout: default
parent: Operational Excellence
nav_order: 1
---

<div class="pillar-header">
  <h1>OPS01: How do you determine what your priorities are?</h1>
  <p>Everyone needs to understand their part in enabling business success. Have shared goals in order to set priorities for resources. This will maximize the benefits of your efforts.</p>
</div>

## Best Practices

<div class="best-practice">
  <h4>Evaluate external customer needs</h4>
  <p>Involve key stakeholders, including business, development, and operations teams, when determining where to focus efforts on external customer needs. This will ensure that you have a thorough understanding of the support needed for your business outcomes.</p>
</div>

<div class="best-practice">
  <h4>Evaluate internal customer needs</h4>
  <p>Involve key stakeholders, including business, development, and operations teams, when determining where to focus efforts on internal customer needs. This will ensure that you have a thorough understanding of the support needed for your business outcomes.</p>
</div>

<div class="best-practice">
  <h4>Evaluate governance requirements</h4>
  <p>Ensure that you are aware of guidelines or obligations defined by your organization that may mandate or emphasize specific focus. Evaluate internal factors, such as organization policy, standards, and requirements. Validate that you have mechanisms to identify changes to governance. If no governance requirements exist, ensure that you have applied due diligence to this determination.</p>
</div>

<div class="best-practice">
  <h4>Evaluate compliance requirements</h4>
  <p>Evaluate external factors, such as regulatory compliance requirements and industry standards, to ensure that you are aware of guidelines or obligations that may mandate or emphasize specific focus. If no compliance requirements are identified, ensure that you have applied due diligence to this determination.</p>
</div>

<div class="best-practice">
  <h4>Evaluate threat landscape</h4>
  <p>Evaluate threats to the business (for example, competition, business risk and liabilities, operational risks, and information security threats) and maintain current information in a risk registry. Include the impact of risks when determining where to focus efforts.</p>
</div>

<div class="best-practice">
  <h4>Evaluate tradeoffs</h4>
  <p>Evaluate the impact of tradeoffs between competing interests or alternative approaches, to help make informed decisions when determining where to focus efforts or choosing a course of action. For example, accelerating speed to market for new features may be emphasized over cost optimization, or you may choose a relational database for non-relational data to simplify the effort to migrate a system, rather than migrating to a database optimized for your data type and updating your application.</p>
</div>

<div class="best-practice">
  <h4>Manage benefits and risks</h4>
  <p>Manage benefits and risks to make informed decisions when determining where to focus efforts. For example, it may be beneficial to deploy a workload with unresolved issues so that significant new features can be made available to customers. It may be possible to mitigate associated risks, or it may become unacceptable to allow a risk to remain, in which case you will take action to address the risk.</p>
</div>

## Implementation Guidance

<div class="implementation-step">
  <h4>1. Identify your stakeholders</h4>
  <p>Determine who has an interest in your workload and its outcomes. This includes business owners, development teams, operations teams, and security teams.</p>
</div>

<div class="implementation-step">
  <h4>2. Gather requirements</h4>
  <p>Collect requirements from all stakeholders, including business goals, technical constraints, security requirements, and compliance obligations.</p>
</div>

<div class="implementation-step">
  <h4>3. Prioritize requirements</h4>
  <p>Use a prioritization framework (such as MoSCoW - Must have, Should have, Could have, Won't have) to categorize requirements based on their importance.</p>
</div>

<div class="implementation-step">
  <h4>4. Document decisions</h4>
  <p>Record decisions made about priorities, including the rationale behind them and any tradeoffs considered.</p>
</div>

<div class="implementation-step">
  <h4>5. Review regularly</h4>
  <p>Establish a cadence for reviewing priorities as business needs and external factors change over time.</p>
</div>

## AWS Services to Consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Organizations</h4>
    <p>For managing multiple AWS accounts and applying policies across them</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Config</h4>
    <p>For assessing, auditing, and evaluating configurations of AWS resources</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Control Tower</h4>
    <p>For setting up and governing a secure, compliant multi-account environment</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Service Catalog</h4>
    <p>For creating and managing catalogs of approved IT services</p>
  </div>
</div>

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/welcome.html">AWS Well-Architected Framework - Operational Excellence Pillar</a></li>
    <li><a href="https://aws.amazon.com/professional-services/CAF/">AWS Cloud Adoption Framework</a></li>
    <li><a href="https://aws.amazon.com/prescriptive-guidance/">AWS Prescriptive Guidance</a></li>
  </ul>
</div>
