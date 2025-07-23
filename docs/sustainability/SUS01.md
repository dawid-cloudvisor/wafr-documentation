---
title: SUS01 - How do you select Regions to support your sustainability goals?
layout: default
parent: Sustainability
nav_order: 1
---

# SUS01: How do you select Regions to support your sustainability goals?

Choose Regions near Amazon's renewable energy projects or where the grid has a published carbon intensity that meets your renewable energy or carbon reduction goals.

## Best Practices

### Choose Regions based on your business requirements and sustainability goals
Evaluate the Regions that meet your business requirements and factor in your sustainability goals when making the final selection. Consider the published sustainability information for each Region, such as Regions with lower carbon intensity.

### Choose Regions close to users to minimize network traffic required
Minimize the network resources required to serve requests by selecting Regions close to your users. This reduces the energy required to deliver your service.

### Choose Regions where renewable energy is a higher percentage of the grid power
Choose Regions where the grid power has a higher percentage of renewable energy. AWS publishes information about the grid mix in each Region.

## Implementation Guidance

1. **Understand your sustainability goals**: Define clear sustainability objectives for your organization.

2. **Evaluate Region options**: Research AWS Regions based on their renewable energy usage and carbon footprint.

3. **Consider proximity to users**: Choose Regions that minimize network distance to your primary user base.

4. **Balance multiple factors**: Make Region selections that balance business requirements, performance needs, and sustainability goals.

5. **Monitor and adjust**: Regularly review your Region choices as AWS expands renewable energy projects and as your business needs evolve.

## AWS Services to Consider

- **AWS Global Infrastructure** - For understanding the AWS Region footprint and characteristics
- **Amazon CloudFront** - For content delivery with reduced latency and network traffic
- **AWS Global Accelerator** - For improving availability and performance using the AWS global network

## Related Resources

- [AWS Well-Architected Framework - Sustainability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/sustainability-pillar/welcome.html)
- [AWS Sustainability](https://sustainability.aboutamazon.com/environment/the-cloud)
- [AWS and Sustainability](https://aws.amazon.com/about-aws/sustainability/)
- [AWS Carbon Footprint Tool](https://aws.amazon.com/aws-cost-management/aws-customer-carbon-footprint-tool/)
