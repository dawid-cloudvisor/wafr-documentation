---
title: SEC08 - How do you protect your data at rest?
layout: default
parent: Security
has_children: true
nav_order: 8
---

<div class="pillar-header">
  <h1>SEC08: How do you protect your data at rest?</h1>
  <p>Protecting your data at rest reduces the risk of unauthorized access, when encryption keys are securely managed. Encryption should be applied based on the classification of your data. You should encrypt everything by default, and consider additional protections such as access controls and backups. Access to your data should be audited using detective controls, and you should inventory what data you have and where it's stored.</p>
</div>

## Best Practices

This question includes the following best practices:

<div class="best-practices-list">
  <ul>
    <li><a href="./SEC08-BP01.html">SEC08-BP01: Implement secure key management</a></li>
    <li><a href="./SEC08-BP02.html">SEC08-BP02: Enforce encryption at rest</a></li>
    <li><a href="./SEC08-BP03.html">SEC08-BP03: Automate data at rest protection</a></li>
    <li><a href="./SEC08-BP04.html">SEC08-BP04: Enforce access control</a></li>
    <li><a href="./SEC08-BP05.html">SEC08-BP05: Use mechanisms to keep people away from data</a></li>
  </ul>
</div>

## Key Concepts

### Data at Rest Protection Fundamentals

**Encryption by Default**: Apply encryption to all data stored in your systems, regardless of sensitivity level. This provides a baseline level of protection and simplifies security management by eliminating the need to determine which data requires encryption.

**Defense in Depth**: Implement multiple layers of protection for data at rest, including encryption, access controls, network security, and physical security measures. No single control should be relied upon to protect sensitive data.

**Key Management**: Securely generate, store, rotate, and manage encryption keys throughout their lifecycle. Proper key management is critical to maintaining the effectiveness of encryption and ensuring data can be accessed when needed.

**Access Control Integration**: Combine encryption with robust access controls to ensure that even if encryption is compromised, unauthorized users cannot access sensitive data without proper authentication and authorization.

### Data Protection Layers

**Storage-Level Encryption**: Encrypt data at the storage layer using services like Amazon EBS encryption, Amazon S3 server-side encryption, and Amazon RDS encryption. This provides transparent encryption with minimal performance impact.

**Application-Level Encryption**: Implement encryption within applications before data is stored, providing additional control over encryption keys and algorithms. This is particularly important for highly sensitive data.

**Database Encryption**: Use database-native encryption features such as Transparent Data Encryption (TDE) for structured data, combined with encrypted backups and transaction logs.

**Backup and Archive Encryption**: Ensure that all backup copies and archived data are encrypted using the same or stronger encryption standards as the primary data.

## AWS Services to Consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Key Management Service (KMS)</h4>
    <p>Makes it easy for you to create and manage cryptographic keys and control their use across a wide range of AWS services. Provides centralized key management with hardware security module (HSM) protection.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS CloudHSM</h4>
    <p>Provides hardware security modules in the AWS Cloud. Enables you to generate and use your own encryption keys on FIPS 140-2 Level 3 validated hardware.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon S3</h4>
    <p>Object storage service with multiple server-side encryption options including SSE-S3, SSE-KMS, and SSE-C. Supports client-side encryption and bucket-level encryption configuration.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon EBS</h4>
    <p>Block storage service that provides encryption for EBS volumes and snapshots. Encryption is transparent to applications and provides minimal performance impact.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon RDS</h4>
    <p>Managed relational database service that supports encryption at rest for database instances, automated backups, read replicas, and snapshots using AWS KMS.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Secrets Manager</h4>
    <p>Helps you protect secrets needed to access your applications, services, and IT resources. Automatically encrypts secrets and provides secure storage with automatic rotation.</p>
  </div>
</div>

## Implementation Approach

### 1. Key Management Strategy
- Design comprehensive key management architecture
- Implement AWS KMS for centralized key management
- Establish key rotation policies and procedures
- Define key access controls and permissions
- Plan for key backup and disaster recovery

### 2. Encryption Implementation
- Enable encryption by default across all storage services
- Configure appropriate encryption algorithms and key sizes
- Implement client-side encryption for highly sensitive data
- Ensure encryption covers all data copies including backups
- Validate encryption implementation and effectiveness

### 3. Access Control Integration
- Implement identity-based access controls for encrypted data
- Configure resource-based policies for data access
- Use attribute-based access control (ABAC) where appropriate
- Establish audit trails for all data access activities
- Implement least privilege access principles

### 4. Automation and Monitoring
- Automate encryption configuration and compliance checking
- Implement continuous monitoring of encryption status
- Set up alerts for encryption policy violations
- Automate key rotation and lifecycle management
- Establish metrics and reporting for data protection effectiveness

## Data at Rest Protection Architecture

### Layered Encryption Architecture
```
Application Layer
    ↓ (Client-Side Encryption)
Service Layer (S3, RDS, EBS)
    ↓ (Server-Side Encryption)
Storage Layer
    ↓ (Volume/Disk Encryption)
Hardware Layer (HSM/KMS)
```

### Key Management Hierarchy
```
Customer Master Keys (CMK)
    ↓ (AWS KMS)
Data Encryption Keys (DEK)
    ↓ (Service Integration)
Encrypted Data Storage
    ↓ (Access Controls)
Authorized Applications/Users
```

### Comprehensive Data Protection Flow
```
Data Creation/Ingestion
    ↓ (Classification & Tagging)
Encryption Key Selection
    ↓ (Based on Data Classification)
Encryption Application
    ↓ (Transparent/Application-Level)
Secure Storage
    ↓ (Access Controls & Monitoring)
Audit & Compliance Reporting
```

## Data Protection Controls Framework

### Preventive Controls
- **Encryption Standards**: AES-256, RSA-2048, approved algorithms and key sizes
- **Key Management**: Secure generation, storage, rotation, and destruction
- **Access Controls**: Identity-based, resource-based, and attribute-based controls
- **Network Security**: VPC isolation, private endpoints, secure data transfer

### Detective Controls
- **Encryption Monitoring**: Continuous validation of encryption status and compliance
- **Access Auditing**: Comprehensive logging of all data access activities
- **Key Usage Tracking**: Monitoring of encryption key usage and access patterns
- **Compliance Reporting**: Regular assessment against security standards and regulations

### Responsive Controls
- **Incident Response**: Procedures for encryption key compromise and data breaches
- **Key Revocation**: Immediate key disabling and data re-encryption capabilities
- **Access Revocation**: Rapid removal of access permissions for compromised accounts
- **Recovery Procedures**: Data restoration from encrypted backups and archives

## Common Challenges and Solutions

### Challenge: Performance Impact of Encryption
**Solution**: Use hardware-accelerated encryption, choose appropriate encryption algorithms, implement encryption at the storage layer for transparency, and optimize key caching strategies.

### Challenge: Key Management Complexity
**Solution**: Use AWS KMS for centralized key management, implement automated key rotation, establish clear key governance policies, and use envelope encryption for large datasets.

### Challenge: Compliance and Regulatory Requirements
**Solution**: Understand specific encryption requirements for your industry, implement appropriate key management controls, maintain detailed audit trails, and use FIPS 140-2 validated encryption where required.

### Challenge: Cross-Region Data Protection
**Solution**: Implement multi-region key management strategies, use cross-region replication with encryption, establish data residency controls, and plan for disaster recovery scenarios.

### Challenge: Legacy System Integration
**Solution**: Implement encryption proxies or gateways, use database-level encryption features, plan for gradual migration to encrypted storage, and implement compensating controls where direct encryption isn't possible.

## Data at Rest Protection Maturity Levels

### Level 1: Basic Encryption
- Manual encryption configuration for critical data
- Basic key management using service defaults
- Limited encryption coverage across data stores
- Reactive approach to encryption requirements

### Level 2: Systematic Encryption
- Encryption by default policies implemented
- Centralized key management using AWS KMS
- Comprehensive encryption across most data stores
- Regular encryption compliance assessments

### Level 3: Advanced Protection
- Automated encryption deployment and management
- Advanced key management with rotation and lifecycle policies
- Client-side encryption for highly sensitive data
- Integrated access controls and audit capabilities

### Level 4: Optimized Protection
- AI/ML-powered encryption optimization and monitoring
- Dynamic encryption based on data classification and risk
- Automated threat response and key management
- Continuous compliance and security posture optimization

## Data at Rest Protection Best Practices

### Encryption Implementation:
1. **Encrypt Everything by Default**: Apply encryption to all data regardless of sensitivity
2. **Use Strong Encryption Standards**: Implement AES-256 or equivalent approved algorithms
3. **Layer Encryption Controls**: Combine storage-level and application-level encryption
4. **Encrypt All Data Copies**: Include backups, snapshots, and replicas in encryption scope
5. **Validate Encryption Effectiveness**: Regularly test and verify encryption implementation

### Key Management:
1. **Centralized Key Management**: Use AWS KMS for consistent key management across services
2. **Implement Key Rotation**: Establish regular key rotation schedules and procedures
3. **Secure Key Storage**: Use hardware security modules (HSMs) for key protection
4. **Control Key Access**: Implement strict access controls and audit key usage
5. **Plan for Key Recovery**: Establish key backup and disaster recovery procedures

### Access Control Integration:
1. **Combine with Identity Controls**: Integrate encryption with IAM and access management
2. **Implement Least Privilege**: Grant minimum required access to encrypted data
3. **Use Attribute-Based Controls**: Leverage data classification for access decisions
4. **Monitor Data Access**: Implement comprehensive audit logging and monitoring
5. **Regular Access Reviews**: Periodically review and validate data access permissions

## Key Performance Indicators (KPIs)

### Encryption Coverage Metrics:
- Percentage of data encrypted at rest
- Encryption compliance rate across services
- Time to encrypt new data stores
- Coverage of backup and archive encryption

### Key Management Metrics:
- Key rotation compliance rate
- Key access audit findings
- Mean time to key provisioning
- Key management operational costs

### Security and Compliance Metrics:
- Data protection policy violations
- Encryption-related security incidents
- Compliance assessment scores
- Audit finding resolution time

## Encryption Standards and Algorithms

### Approved Encryption Algorithms:
- **Symmetric Encryption**: AES-128, AES-192, AES-256
- **Asymmetric Encryption**: RSA-2048, RSA-3072, RSA-4096, ECC P-256, ECC P-384
- **Hash Functions**: SHA-256, SHA-384, SHA-512
- **Key Derivation**: PBKDF2, scrypt, Argon2

### Key Size Recommendations:
- **Minimum Key Sizes**: AES-128, RSA-2048, ECC P-256
- **Recommended Key Sizes**: AES-256, RSA-3072, ECC P-384
- **High Security Key Sizes**: AES-256, RSA-4096, ECC P-521

### Compliance Considerations:
- **FIPS 140-2**: Use FIPS-validated encryption modules where required
- **Common Criteria**: Implement CC-evaluated encryption solutions for high-security environments
- **Industry Standards**: Follow sector-specific encryption requirements (PCI DSS, HIPAA, etc.)

## Service-Specific Implementation Guidance

### Amazon S3 Encryption:
- Enable default bucket encryption with SSE-S3 or SSE-KMS
- Use bucket policies to enforce encryption requirements
- Implement client-side encryption for highly sensitive data
- Configure Cross-Region Replication with encryption

### Amazon EBS Encryption:
- Enable encryption by default for new volumes
- Encrypt existing volumes using snapshot and restore process
- Use customer-managed KMS keys for additional control
- Ensure encrypted snapshots for backup and recovery

### Amazon RDS Encryption:
- Enable encryption at database creation time
- Use encrypted automated backups and snapshots
- Implement encryption for read replicas
- Consider Transparent Data Encryption (TDE) for additional protection

### AWS Lambda and Serverless:
- Encrypt environment variables using KMS
- Use encrypted storage for temporary files
- Implement client-side encryption in function code
- Secure secrets using AWS Secrets Manager

## Related resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html">AWS Well-Architected Framework - Security Pillar</a></li>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/sec-08.html">SEC08: How do you protect your data at rest?</a></li>
    <li><a href="https://docs.aws.amazon.com/kms/latest/developerguide/overview.html">AWS Key Management Service Developer Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/cloudhsm/latest/userguide/introduction.html">AWS CloudHSM User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/AmazonS3/latest/userguide/serv-side-encryption.html">Amazon S3 Server-Side Encryption</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-encrypt-and-decrypt-your-data-with-the-aws-encryption-sdk/">How to encrypt and decrypt your data with the AWS Encryption SDK</a></li>
    <li><a href="https://aws.amazon.com/compliance/fips/">AWS FIPS 140-2 Overview</a></li>
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
