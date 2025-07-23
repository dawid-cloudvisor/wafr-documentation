---
title: OPS01 - How do you determine what your priorities are?
layout: default
parent: Operational Excellence
nav_order: 1
---

# OPS01: How do you determine what your priorities are?

Everyone needs to understand their part in enabling business success. Have shared goals in order to set priorities for resources. This will maximize the benefits of your efforts.

## Best Practices

### Evaluate external customer needs
Involve key stakeholders, including business, development, and operations teams, when determining where to focus efforts on external customer needs. This will ensure that you have a thorough understanding of the support needed for your business outcomes.

### Evaluate internal customer needs
Involve key stakeholders, including business, development, and operations teams, when determining where to focus efforts on internal customer needs. This will ensure that you have a thorough understanding of the support needed for your business outcomes.

### Evaluate governance requirements
Ensure that you are aware of guidelines or obligations defined by your organization that may mandate or emphasize specific focus. Evaluate internal factors, such as organization policy, standards, and requirements. Validate that you have mechanisms to identify changes to governance. If no governance requirements exist, ensure that you have applied due diligence to this determination.

### Evaluate compliance requirements
Evaluate external factors, such as regulatory compliance requirements and industry standards, to ensure that you are aware of guidelines or obligations that may mandate or emphasize specific focus. If no compliance requirements are identified, ensure that you have applied due diligence to this determination.

### Evaluate threat landscape
Evaluate threats to the business (for example, competition, business risk and liabilities, operational risks, and information security threats) and maintain current information in a risk registry. Include the impact of risks when determining where to focus efforts.

### Evaluate tradeoffs
Evaluate the impact of tradeoffs between competing interests or alternative approaches, to help make informed decisions when determining where to focus efforts or choosing a course of action. For example, accelerating speed to market for new features may be emphasized over cost optimization, or you may choose a relational database for non-relational data to simplify the effort to migrate a system, rather than migrating to a database optimized for your data type and updating your application.

### Manage benefits and risks
Manage benefits and risks to make informed decisions when determining where to focus efforts. For example, it may be beneficial to deploy a workload with unresolved issues so that significant new features can be made available to customers. It may be possible to mitigate associated risks, or it may become unacceptable to allow a risk to remain, in which case you will take action to address the risk.

## Implementation Guidance

1. **Identify your stakeholders**: Determine who has an interest in your workload and its outcomes. This includes business owners, development teams, operations teams, and security teams.

2. **Gather requirements**: Collect requirements from all stakeholders, including business goals, technical constraints, security requirements, and compliance obligations.

3. **Prioritize requirements**: Use a prioritization framework (such as MoSCoW - Must have, Should have, Could have, Won't have) to categorize requirements based on their importance.

4. **Document decisions**: Record decisions made about priorities, including the rationale behind them and any tradeoffs considered.

5. **Review regularly**: Establish a cadence for reviewing priorities as business needs and external factors change over time.

## AWS Services to Consider

- **AWS Organizations** - For managing multiple AWS accounts and applying policies across them
- **AWS Config** - For assessing, auditing, and evaluating configurations of AWS resources
- **AWS Control Tower** - For setting up and governing a secure, compliant multi-account environment
- **AWS Service Catalog** - For creating and managing catalogs of approved IT services

## Related Resources

- [AWS Well-Architected Framework - Operational Excellence Pillar](https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/welcome.html)
- [AWS Cloud Adoption Framework](https://aws.amazon.com/professional-services/CAF/)
- [AWS Prescriptive Guidance](https://aws.amazon.com/prescriptive-guidance/)
