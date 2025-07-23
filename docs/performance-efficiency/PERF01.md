---
title: PERF01 - How do you select the best performing architecture?
layout: default
parent: Performance Efficiency
nav_order: 1
---

# PERF01: How do you select the best performing architecture?

Often, multiple approaches are required for optimal performance across a workload. Well-architected systems use multiple solutions and features to improve performance.

## Best Practices

### Understand the available services and resources
Learn about and understand the wide range of services and resources available in the cloud. Identify the relevant services and configuration options for your workload, and understand how to achieve optimal performance.

### Define a process for architectural choices
Use internal experience and knowledge of the cloud, or external resources such as published use cases, relevant documentation, or whitepapers to define a process to choose resources and services. You should define a process that encourages experimentation and benchmarking with the services that could be used in your workload.

### Factor cost requirements into decisions
Workload owners are often required to balance cost with performance and other aspects of the architecture. Using a data-driven approach to select the instance type or service, you can achieve the most cost effective performance for your workload.

### Use policies or reference architectures
Maximize performance and efficiency by evaluating internal policies and existing reference architectures and using your analysis to select services and configurations for your workload.

### Use guidance from cloud provider or an appropriate partner
Use cloud company resources, such as solutions architects, professional services, or an appropriate partner to guide your decisions. These resources can help review and improve your architecture for optimal performance.

### Benchmark existing workloads
Benchmark the performance of an existing workload to understand how it performs on the cloud. Use the data collected from benchmarks to drive architectural decisions.

### Load test your workload
Deploy your latest workload architecture on the cloud using different resource types and sizes. Monitor the deployment to capture performance metrics that identify bottlenecks or excess capacity. Use this performance information to design or improve your architecture and resource selection.

## Implementation Guidance

1. **Understand your workload requirements**: Define performance requirements, including latency, throughput, and scalability needs.

2. **Evaluate compute options**: Consider different EC2 instance types, container services, or serverless options based on your workload characteristics.

3. **Evaluate storage options**: Choose appropriate storage services (S3, EBS, EFS, etc.) based on access patterns, throughput requirements, and data characteristics.

4. **Evaluate database options**: Select the right database service (RDS, DynamoDB, etc.) based on data model, query patterns, and scaling requirements.

5. **Evaluate networking options**: Consider VPC design, placement groups, enhanced networking, and global content delivery options.

6. **Benchmark and load test**: Use tools like Amazon CloudWatch and AWS X-Ray to monitor performance and identify bottlenecks.

## AWS Services to Consider

- **Amazon EC2** - For compute capacity with various instance types optimized for different workloads
- **AWS Lambda** - For serverless compute without managing servers
- **Amazon S3** - For object storage with different storage classes
- **Amazon RDS** - For managed relational databases
- **Amazon DynamoDB** - For managed NoSQL databases
- **Amazon CloudFront** - For content delivery with low latency
- **AWS Auto Scaling** - For automatically adjusting capacity to maintain performance
- **Amazon CloudWatch** - For monitoring performance metrics

## Related Resources

- [AWS Well-Architected Framework - Performance Efficiency Pillar](https://docs.aws.amazon.com/wellarchitected/latest/performance-efficiency-pillar/welcome.html)
- [AWS Architecture Center](https://aws.amazon.com/architecture/)
- [AWS Performance Efficiency Documentation](https://docs.aws.amazon.com/wellarchitected/latest/performance-efficiency-pillar/welcome.html)
