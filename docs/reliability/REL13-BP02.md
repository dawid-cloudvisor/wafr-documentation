---
title: REL13-BP02 - Use defined recovery strategies to meet the recovery objectives
layout: default
parent: REL13 - How do you plan for disaster recovery?
nav_order: 2
---

# REL13-BP02: Use defined recovery strategies to meet the recovery objectives

Implement disaster recovery strategies that align with your defined RTO and RPO objectives. Choose from backup and restore, pilot light, warm standby, or multi-site active/active approaches based on business requirements, cost considerations, and technical constraints.

## Implementation Steps

### 1. Select Appropriate DR Strategy
Choose the disaster recovery strategy that best meets your RTO/RPO requirements within budget constraints.

### 2. Design DR Architecture
Create detailed architecture designs for your chosen disaster recovery approach.

### 3. Implement Cross-Region Infrastructure
Deploy the necessary infrastructure components in your disaster recovery region.

### 4. Configure Data Replication
Set up appropriate data replication mechanisms to meet RPO requirements.

### 5. Establish Recovery Procedures
Document and implement detailed recovery procedures for each DR strategy.

## AWS Services

### Primary Services
- **AWS Site Recovery**: Automated disaster recovery orchestration
- **AWS Elastic Disaster Recovery**: Application-level disaster recovery
- **Amazon Route 53**: DNS failover and traffic routing
- **AWS Global Accelerator**: Global traffic management

### Supporting Services
- **Amazon S3**: Cross-region replication for backup and restore
- **Amazon RDS**: Multi-AZ and cross-region read replicas
- **Amazon DynamoDB**: Global Tables for multi-region replication
- **AWS CloudFormation**: Infrastructure as code for DR environments

## Benefits

- **RTO/RPO Compliance**: Strategies designed to meet specific recovery objectives
- **Cost Optimization**: Choose the most cost-effective strategy for your requirements
- **Scalable Recovery**: Strategies that can scale with business growth
- **Technology Alignment**: Leverage appropriate AWS services for each strategy
- **Business Continuity**: Maintain operations during disasters and outages

## Related Resources

- [AWS Disaster Recovery Strategies](https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/)
- [AWS Site Recovery User Guide](https://docs.aws.amazon.com/drs/)
- [Amazon Route 53 Application Recovery Controller](https://docs.aws.amazon.com/r53recovery/)
- [AWS Architecture Center - Disaster Recovery](https://aws.amazon.com/architecture/disaster-recovery/)
