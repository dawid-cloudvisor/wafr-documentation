---
title: SEC07 - How do you classify your data?
layout: default
parent: Security
has_children: true
nav_order: 7
---

<div class="pillar-header">
  <h1>SEC07: How do you classify your data?</h1>
  <p>Classification provides a way to categorize data based on levels of sensitivity, and is an important consideration for designing your security controls. Without classification, you cannot apply appropriate protections for your data. You should identify the types of data your organization processes, as well as where it's stored and who has access to it. Data classification should be applied consistently across your organization and automated where possible to reduce the risk of human error.</p>
</div>

## Best Practices

This question includes the following best practices:

<div class="best-practices-list">
  <ul>
    <li><a href="./SEC07-BP01.html">SEC07-BP01: Understand your data classification scheme</a></li>
    <li><a href="./sec07-bp02.html">SEC07-BP02: Apply data protection controls based on data sensitivity</a></li>
    <li><a href="./sec07-bp03.html">SEC07-BP03: Automate identification and classification</a></li>
    <li><a href="./sec07-bp04.html">SEC07-BP04: Define scalable data lifecycle management</a></li>
  </ul>
</div>

## Key Concepts

### Data Classification Fundamentals

**Data Sensitivity Levels**: Establish clear categories that reflect the potential impact of unauthorized disclosure, modification, or destruction of data. Common levels include Public, Internal, Confidential, and Restricted.

**Data Types and Categories**: Identify different types of data your organization handles, such as personal data, financial information, intellectual property, operational data, and system logs.

**Regulatory and Compliance Requirements**: Understand legal and regulatory obligations that affect how different types of data must be handled, stored, and protected (GDPR, HIPAA, PCI DSS, SOX, etc.).

**Data Lifecycle Management**: Implement appropriate controls throughout the entire data lifecycle, from creation and collection through processing, storage, sharing, and eventual disposal.

### Classification Framework Components

**Data Discovery**: Systematically identify and catalog all data assets across your organization, including structured and unstructured data in various storage locations.

**Classification Criteria**: Establish consistent criteria for determining data sensitivity levels based on business impact, regulatory requirements, and organizational policies.

**Labeling and Tagging**: Apply consistent metadata and labels to data assets to enable automated policy enforcement and access controls.

**Policy Enforcement**: Implement technical and procedural controls that automatically apply appropriate protections based on data classification levels.

## AWS Services to Consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon Macie</h4>
    <p>Uses machine learning and pattern matching to discover and protect your sensitive data in AWS. Automatically identifies personally identifiable information (PII) and provides detailed findings and alerts.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Config</h4>
    <p>Enables you to assess, audit, and evaluate the configurations of your AWS resources. Helps track data storage configurations and ensure compliance with classification policies.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS CloudTrail</h4>
    <p>Records API calls for your account and delivers log files to you. Provides audit trails for data access and classification activities across your AWS environment.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon S3</h4>
    <p>Object storage service with built-in tagging capabilities. Supports object-level and bucket-level tags for data classification and automated policy enforcement.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Resource Groups</h4>
    <p>Helps you organize your AWS resources using tags. Enables grouping and management of resources based on data classification and other criteria.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Systems Manager</h4>
    <p>Gives you visibility and control of your infrastructure on AWS. Provides automation capabilities for applying classification-based policies and controls.</p>
  </div>
</div>

## Implementation Approach

### 1. Data Discovery and Inventory
- Conduct comprehensive data discovery across all storage systems
- Identify data sources, repositories, and data flows
- Catalog structured and unstructured data assets
- Map data locations and access patterns
- Document data ownership and stewardship responsibilities

### 2. Classification Framework Development
- Define organizational data classification levels and criteria
- Establish classification policies and procedures
- Create data handling requirements for each classification level
- Develop classification decision trees and guidelines
- Align classification with regulatory and compliance requirements

### 3. Automated Classification Implementation
- Deploy automated data discovery and classification tools
- Implement machine learning-based content analysis
- Configure pattern matching and keyword detection
- Set up automated tagging and labeling systems
- Establish classification validation and quality assurance processes

### 4. Policy Enforcement and Governance
- Implement access controls based on data classification
- Configure automated policy enforcement mechanisms
- Establish data lifecycle management procedures
- Create monitoring and compliance reporting systems
- Develop incident response procedures for classification violations

## Data Classification Architecture

### Data Discovery and Classification Pipeline
```
Data Sources (S3, RDS, DynamoDB, etc.)
    ↓
Amazon Macie (Automated Discovery)
    ↓
Classification Engine (ML + Rules)
    ↓
Tagging and Labeling System
    ↓
Policy Enforcement (Access Controls, Encryption)
```

### Classification-Based Access Control
```
User/Application Request
    ↓
Identity Verification
    ↓
Data Classification Check
    ↓
Policy Evaluation (ABAC)
    ↓
Access Decision (Allow/Deny)
    ↓
Audit Logging
```

### Data Lifecycle Management
```
Data Creation/Collection
    ↓ (Classification Assignment)
Data Processing/Analysis
    ↓ (Classification Validation)
Data Storage/Archival
    ↓ (Retention Policies)
Data Sharing/Distribution
    ↓ (Access Controls)
Data Disposal/Deletion
```

## Data Classification Framework

### Classification Levels

**Public Data**:
- Information intended for public consumption
- No restrictions on access or distribution
- Examples: Marketing materials, public websites, press releases
- Controls: Basic integrity protection, availability assurance

**Internal Data**:
- Information for internal organizational use
- Limited distribution within the organization
- Examples: Internal policies, employee directories, general business information
- Controls: Access controls, basic encryption, audit logging

**Confidential Data**:
- Sensitive information requiring protection from unauthorized disclosure
- Restricted access based on business need
- Examples: Financial data, customer information, strategic plans
- Controls: Strong access controls, encryption, detailed audit trails, data loss prevention

**Restricted Data**:
- Highly sensitive information with severe impact if compromised
- Strictly controlled access and handling procedures
- Examples: Personal health information, payment card data, trade secrets
- Controls: Multi-factor authentication, end-to-end encryption, comprehensive monitoring, strict retention policies

### Data Types and Examples

**Personal Data**:
- Personally identifiable information (PII)
- Protected health information (PHI)
- Financial account information
- Biometric data

**Business Data**:
- Intellectual property and trade secrets
- Financial records and reports
- Strategic plans and competitive information
- Customer and vendor contracts

**Operational Data**:
- System logs and monitoring data
- Configuration information
- Performance metrics
- Backup and recovery data

**Regulatory Data**:
- Data subject to specific compliance requirements
- Audit trails and compliance reports
- Legal hold information
- Regulatory correspondence

## Common Challenges and Solutions

### Challenge: Data Discovery at Scale
**Solution**: Implement automated data discovery tools like Amazon Macie, use APIs to scan multiple data sources, establish regular discovery schedules, and create data catalogs for ongoing inventory management.

### Challenge: Inconsistent Classification
**Solution**: Develop clear classification criteria and decision trees, provide training and guidance to data owners, implement automated classification tools, and establish quality assurance processes.

### Challenge: Dynamic Data Classification
**Solution**: Implement real-time classification engines, use machine learning for adaptive classification, establish re-classification triggers, and automate classification updates based on data changes.

### Challenge: Cross-Border Data Compliance
**Solution**: Understand data residency requirements, implement geo-location controls, establish data transfer agreements, and use encryption and tokenization for cross-border data flows.

### Challenge: Legacy System Integration
**Solution**: Develop APIs for legacy system integration, implement data extraction and classification pipelines, use compensating controls where direct integration isn't possible, and plan for system modernization.

## Data Classification Maturity Levels

### Level 1: Basic Classification
- Manual data identification and classification
- Simple classification schemes (e.g., Public/Private)
- Basic access controls based on classification
- Limited automation and tooling

### Level 2: Structured Classification
- Systematic data discovery and inventory processes
- Well-defined classification levels and criteria
- Automated tagging and labeling systems
- Policy-based access controls and protection

### Level 3: Advanced Classification
- Automated data discovery and classification
- Machine learning-enhanced classification accuracy
- Dynamic classification based on content and context
- Integrated data lifecycle management

### Level 4: Intelligent Classification
- AI-powered classification with continuous learning
- Predictive classification for new data types
- Automated policy adaptation and optimization
- Real-time classification and protection enforcement

## Data Classification Best Practices

### Discovery and Inventory:
1. **Comprehensive Data Mapping**: Identify all data sources and repositories
2. **Regular Discovery Scans**: Implement scheduled and triggered discovery processes
3. **Data Flow Analysis**: Understand how data moves through your systems
4. **Shadow IT Detection**: Identify unauthorized data storage and processing
5. **Data Lineage Tracking**: Maintain visibility into data origins and transformations

### Classification Implementation:
1. **Clear Classification Criteria**: Establish unambiguous classification rules
2. **Automated Classification**: Use ML and pattern matching for consistent results
3. **Human Review Processes**: Implement validation and exception handling
4. **Classification Metadata**: Maintain rich metadata about classification decisions
5. **Regular Re-classification**: Update classifications as data and context change

### Policy Enforcement:
1. **Attribute-Based Access Control**: Use classification as a key access control attribute
2. **Automated Policy Application**: Enforce policies based on classification tags
3. **Data Loss Prevention**: Implement DLP controls based on classification levels
4. **Encryption Requirements**: Apply encryption based on data sensitivity
5. **Monitoring and Alerting**: Track classification compliance and violations

## Key Performance Indicators (KPIs)

### Discovery and Classification Metrics:
- Percentage of data assets discovered and classified
- Classification accuracy and consistency rates
- Time to classify new data assets
- Coverage of automated vs. manual classification

### Compliance and Governance Metrics:
- Policy compliance rates by classification level
- Data handling violations and incidents
- Audit finding resolution time
- Regulatory compliance assessment scores

### Operational Metrics:
- Classification system performance and availability
- User adoption and training completion rates
- Cost of classification program operations
- Return on investment from classification initiatives

## Regulatory and Compliance Considerations

### GDPR (General Data Protection Regulation):
- Identify and classify personal data
- Implement data subject rights procedures
- Establish lawful basis for processing
- Maintain data processing records

### HIPAA (Health Insurance Portability and Accountability Act):
- Classify protected health information (PHI)
- Implement administrative, physical, and technical safeguards
- Establish business associate agreements
- Maintain audit trails and breach notification procedures

### PCI DSS (Payment Card Industry Data Security Standard):
- Identify and classify cardholder data
- Implement data protection and access control requirements
- Establish secure network and system configurations
- Maintain vulnerability management and monitoring programs

### SOX (Sarbanes-Oxley Act):
- Classify financial and accounting data
- Implement internal controls and audit procedures
- Establish data retention and disposal policies
- Maintain documentation and evidence of compliance

## Related resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html">AWS Well-Architected Framework - Security Pillar</a></li>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/sec-07.html">SEC07: How do you classify your data?</a></li>
    <li><a href="https://docs.aws.amazon.com/macie/latest/user/what-is-macie.html">Amazon Macie User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/config/latest/developerguide/WhatIsConfig.html">AWS Config Developer Guide</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-use-amazon-macie-to-preview-sensitive-data-in-s3-buckets/">How to use Amazon Macie to preview sensitive data in S3 buckets</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-implement-data-classification-and-protection-using-aws-services/">How to implement data classification and protection using AWS services</a></li>
    <li><a href="https://aws.amazon.com/compliance/data-privacy/">AWS Data Privacy</a></li>
  </ul>
</div>

<style>
.best-practices-list ul {
  list-style-type: none;
  padding-left: 0;
}

.best-practices-list li {
  background-color: #ffead7;
  margin-bottom: 0.5rem;
  border-radius: 5px;
  border: 1px solid #ffcca5;
}

.best-practices-list li a {
  display: block;
  padding: 0.75rem 1rem;
  color: #ff6a00;
  text-decoration: none;
  font-weight: 500;
}

.best-practices-list li a:hover {
  background-color: #ffcca5;
  border-radius: 4px;
}
</style>
