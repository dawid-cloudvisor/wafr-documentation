---
title: REL01 - How do you manage service quotas and constraints?
layout: default
parent: Reliability
nav_order: 1
---

# REL01: How do you manage service quotas and constraints?

For cloud-based workload architectures, there are service quotas (which are also referred to as service limits). These quotas exist to prevent accidentally provisioning more resources than you need and to limit request rates on API operations so as to protect services from abuse. There are also resource constraints, for example, the rate that you can push bits down a fiber connection, or the amount of storage on a physical disk.

## Best Practices

### Aware of service quotas and constraints
Be aware of your default quotas and quota increase requests for your workload architecture. Be aware of which cloud resources are potentially constrained, such as network bandwidth or compute capacity.

### Manage service quotas across accounts and regions
If you are using multiple accounts or Regions, ensure that you request the appropriate quotas in all environments in which your production workloads run.

### Accommodate fixed service quotas and constraints through architecture
Be aware of unchangeable service quotas and physical resources, and architect to prevent these from impacting reliability.

### Monitor and manage quotas
Evaluate your potential usage and increase your quotas appropriately allowing for planned growth in usage.

### Automate quota management
Implement tools to alert you when thresholds are being approached. By using AWS Service Quotas API, you can automate quota increase requests.

### Ensure that a sufficient gap exists between the current quotas and the maximum usage to accommodate failover
When a resource fails, it may still be counted against quotas until it is successfully terminated. Ensure that your quotas cover the overlap of all failed resources with replacements before the failed resources are terminated. You should consider an Availability Zone failure when calculating this gap.

## Implementation Guidance

1. **Identify service quotas**: Use AWS Service Quotas to view all quotas for AWS services in your account.

2. **Set up monitoring**: Configure CloudWatch alarms to alert when usage approaches quota limits.

3. **Request quota increases**: For services where you anticipate needing higher limits, request increases well in advance of your needs.

4. **Design for constraints**: Architect your applications to work within unchangeable quotas and physical constraints.

5. **Implement automated quota management**: Use the Service Quotas API to programmatically monitor and manage your quotas.

## AWS Services to Consider

- **AWS Service Quotas** - For viewing and managing your quotas for AWS services
- **Amazon CloudWatch** - For monitoring resource utilization and operational performance
- **AWS Trusted Advisor** - For guidance on service limits and identifying when you're approaching them
- **AWS Config** - For assessing, auditing, and evaluating configurations of your AWS resources

## Related Resources

- [AWS Well-Architected Framework - Reliability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html)
- [AWS Service Quotas Documentation](https://docs.aws.amazon.com/servicequotas/latest/userguide/intro.html)
- [Managing AWS Service Quotas](https://aws.amazon.com/blogs/mt/managing-aws-service-quotas/)
