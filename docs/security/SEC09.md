---
title: SEC09 - How do you protect your data in transit?
layout: default
parent: Security
has_children: true
nav_order: 9
---

<div class="pillar-header">
  <h1>SEC09: How do you protect your data in transit?</h1>
  <p>All data in transit should be encrypted using secure protocols to provide confidentiality and integrity of data, as well as authenticity of communicating systems. Providing encryption in transit protects against eavesdropping, tampering, and message forgery. You should encrypt all communication between your services, whether they're in the same network or across networks. Additionally, your users should connect to your services using encrypted connections.</p>
</div>

## Best Practices

This question includes the following best practices:

<div class="best-practices-list">
  <ul>
    <li><a href="./SEC09-BP01.html">SEC09-BP01: Implement secure key and certificate management</a></li>
    <li><a href="./SEC09-BP02.html">SEC09-BP02: Enforce encryption in transit</a></li>
    <li><a href="./SEC09-BP03.html">SEC09-BP03: Automate detection of unintended data access</a></li>
    <li><a href="./SEC09-BP04.html">SEC09-BP04: Authenticate network communications</a></li>
  </ul>
</div>

## Key Concepts

### Data in Transit Protection Fundamentals

**Encryption in Transit**: Protect data as it moves between systems, networks, and services using cryptographic protocols such as TLS/SSL, IPSec, and secure messaging protocols. This ensures confidentiality, integrity, and authenticity of data during transmission.

**End-to-End Encryption**: Implement encryption that protects data from its source to its final destination, ensuring that intermediate systems cannot access plaintext data even if they are compromised.

**Certificate and Key Management**: Properly manage digital certificates and cryptographic keys used for encryption in transit, including certificate lifecycle management, rotation, and validation.

**Network Authentication**: Verify the identity of communicating systems and users before establishing encrypted connections, preventing man-in-the-middle attacks and unauthorized access.

### Communication Security Layers

**Application Layer Security**: Implement encryption at the application level using protocols like HTTPS, secure APIs, and application-specific encryption mechanisms.

**Transport Layer Security**: Use TLS/SSL protocols to provide secure communication channels between clients and servers, ensuring data confidentiality and integrity.

**Network Layer Security**: Implement IPSec and VPN technologies to create secure tunnels for network-to-network communication, particularly for hybrid and multi-cloud scenarios.

**Link Layer Security**: Secure physical and wireless network connections using technologies like WPA3 for wireless networks and encrypted fiber optic connections.

## AWS Services to Consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Certificate Manager (ACM)</h4>
    <p>Provisions, manages, and deploys public and private SSL/TLS certificates for use with AWS services and your internal connected resources. Provides automatic certificate renewal and integration with AWS services.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Private Certificate Authority</h4>
    <p>Managed private certificate authority service that helps you easily and securely manage the lifecycle of your private certificates. Ideal for internal applications and services.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon CloudFront</h4>
    <p>Content delivery network (CDN) that provides HTTPS encryption for content delivery and supports custom SSL certificates. Helps improve performance while maintaining security.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Application Load Balancer (ALB)</h4>
    <p>Provides SSL/TLS termination and end-to-end encryption capabilities. Supports SNI (Server Name Indication) for multiple certificates and advanced routing based on content.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS VPN</h4>
    <p>Provides secure connections between your on-premises networks and AWS VPCs using IPSec VPN tunnels. Includes Site-to-Site VPN and Client VPN options.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Direct Connect</h4>
    <p>Provides dedicated network connections from your premises to AWS. Can be combined with encryption to provide secure, high-bandwidth connections to AWS services.</p>
  </div>
</div>

## Implementation Approach

### 1. Certificate and Key Management Strategy
- Implement centralized certificate management using AWS Certificate Manager
- Establish certificate lifecycle management procedures
- Configure automatic certificate renewal and deployment
- Implement certificate monitoring and alerting
- Plan for certificate revocation and emergency procedures

### 2. Encryption in Transit Implementation
- Enable HTTPS/TLS for all web applications and APIs
- Configure end-to-end encryption for service-to-service communication
- Implement secure protocols for database connections
- Enable encryption for messaging and queuing systems
- Configure secure file transfer protocols

### 3. Network Security and Authentication
- Implement mutual TLS (mTLS) for service authentication
- Configure VPN connections for hybrid connectivity
- Set up network access controls and segmentation
- Implement certificate-based authentication
- Configure secure DNS resolution

### 4. Monitoring and Detection
- Implement monitoring for unencrypted communications
- Set up alerts for certificate expiration and issues
- Monitor for protocol downgrade attacks
- Implement network traffic analysis and anomaly detection
- Configure compliance monitoring and reporting

## Data in Transit Protection Architecture

### Layered Encryption in Transit
```
User/Client
    ↓ (HTTPS/TLS)
Load Balancer/CDN
    ↓ (TLS Termination/Re-encryption)
Application Services
    ↓ (Service-to-Service TLS)
Database/Storage
    ↓ (Encrypted Connections)
```

### Certificate Management Lifecycle
```
Certificate Request
    ↓ (CSR Generation)
Certificate Authority (ACM/Private CA)
    ↓ (Certificate Issuance)
Certificate Deployment
    ↓ (Automated Distribution)
Certificate Monitoring
    ↓ (Expiration Tracking)
Certificate Renewal/Revocation
```

### End-to-End Encryption Flow
```
Client Application
    ↓ (Client Certificate)
Authentication & Authorization
    ↓ (TLS Handshake)
Encrypted Channel Establishment
    ↓ (Secure Communication)
Service Processing
    ↓ (Encrypted Response)
Client Verification & Processing
```

## Data in Transit Security Controls Framework

### Preventive Controls
- **Protocol Standards**: TLS 1.2/1.3, strong cipher suites, perfect forward secrecy
- **Certificate Management**: Proper certificate validation, chain verification, revocation checking
- **Network Controls**: VPN tunnels, private connectivity, network segmentation
- **Authentication**: Mutual TLS, certificate-based authentication, strong identity verification

### Detective Controls
- **Traffic Monitoring**: Network traffic analysis, protocol inspection, anomaly detection
- **Certificate Monitoring**: Certificate expiration tracking, validation monitoring, compliance checking
- **Access Logging**: Connection logs, authentication events, protocol usage tracking
- **Compliance Auditing**: Regular assessment of encryption standards and implementation

### Responsive Controls
- **Incident Response**: Procedures for certificate compromise and communication breaches
- **Certificate Revocation**: Immediate certificate revocation and replacement capabilities
- **Traffic Blocking**: Automatic blocking of unencrypted or suspicious communications
- **Recovery Procedures**: Rapid restoration of secure communications after incidents

## Common Challenges and Solutions

### Challenge: Certificate Management Complexity
**Solution**: Use AWS Certificate Manager for automated certificate provisioning and renewal, implement centralized certificate monitoring, establish clear certificate governance policies, and automate certificate deployment processes.

### Challenge: Performance Impact of Encryption
**Solution**: Use hardware acceleration for TLS processing, implement efficient cipher suites, optimize certificate chain length, use session resumption and connection pooling, and consider TLS termination at load balancers.

### Challenge: Legacy System Integration
**Solution**: Implement TLS proxies or gateways, use protocol translation services, plan for gradual migration to secure protocols, and implement compensating controls where direct encryption isn't possible.

### Challenge: Service-to-Service Communication Security
**Solution**: Implement service mesh technologies, use mutual TLS for authentication, establish secure service discovery mechanisms, and implement zero-trust networking principles.

### Challenge: Compliance and Regulatory Requirements
**Solution**: Understand specific encryption requirements for your industry, implement approved cryptographic standards, maintain detailed audit trails, and use FIPS-validated encryption where required.

## Data in Transit Protection Maturity Levels

### Level 1: Basic Encryption
- HTTPS enabled for public-facing applications
- Basic SSL/TLS configuration with default settings
- Manual certificate management and renewal
- Limited monitoring of encryption status

### Level 2: Systematic Encryption
- Encryption enforced for all external communications
- Automated certificate management using ACM
- Service-to-service encryption implementation
- Regular monitoring and compliance checking

### Level 3: Advanced Protection
- End-to-end encryption across all communication paths
- Mutual TLS authentication for service communications
- Advanced threat detection and monitoring
- Automated response to encryption violations

### Level 4: Optimized Protection
- AI/ML-powered threat detection and response
- Dynamic encryption optimization based on risk
- Automated security orchestration and remediation
- Continuous compliance and security posture optimization

## Data in Transit Protection Best Practices

### Encryption Implementation:
1. **Encrypt All Communications**: Apply encryption to all data in transit, internal and external
2. **Use Strong Protocols**: Implement TLS 1.2 or higher with strong cipher suites
3. **Enable Perfect Forward Secrecy**: Use ephemeral key exchange mechanisms
4. **Implement End-to-End Encryption**: Protect data from source to destination
5. **Regular Protocol Updates**: Stay current with latest security protocols and standards

### Certificate Management:
1. **Centralized Management**: Use AWS Certificate Manager for consistent certificate handling
2. **Automated Renewal**: Implement automatic certificate renewal and deployment
3. **Certificate Monitoring**: Monitor certificate health, expiration, and compliance
4. **Proper Validation**: Implement certificate chain validation and revocation checking
5. **Emergency Procedures**: Establish rapid certificate revocation and replacement processes

### Network Security:
1. **Mutual Authentication**: Implement mTLS for service-to-service communication
2. **Network Segmentation**: Use VPCs and security groups to control traffic flow
3. **VPN Connectivity**: Secure hybrid connections with IPSec VPN or Direct Connect
4. **DNS Security**: Implement secure DNS resolution and DNS over HTTPS
5. **Traffic Analysis**: Monitor network traffic for encryption compliance and anomalies

## Key Performance Indicators (KPIs)

### Encryption Coverage Metrics:
- Percentage of communications encrypted in transit
- TLS/SSL adoption rate across services
- Certificate deployment success rate
- Encryption protocol compliance rate

### Certificate Management Metrics:
- Certificate renewal success rate
- Certificate expiration incidents
- Mean time to certificate deployment
- Certificate validation failure rate

### Security and Performance Metrics:
- Encryption-related security incidents
- TLS handshake performance metrics
- Protocol downgrade detection rate
- Compliance assessment scores

## Protocol and Cipher Suite Recommendations

### Recommended TLS Versions:
- **Minimum**: TLS 1.2 for all new implementations
- **Preferred**: TLS 1.3 for optimal security and performance
- **Deprecated**: SSL 3.0, TLS 1.0, TLS 1.1 (should not be used)

### Recommended Cipher Suites (TLS 1.2):
- ECDHE-RSA-AES256-GCM-SHA384
- ECDHE-RSA-AES128-GCM-SHA256
- ECDHE-RSA-AES256-SHA384
- ECDHE-RSA-AES128-SHA256

### Recommended Cipher Suites (TLS 1.3):
- TLS_AES_256_GCM_SHA384
- TLS_CHACHA20_POLY1305_SHA256
- TLS_AES_128_GCM_SHA256

### Certificate Requirements:
- **Key Size**: Minimum RSA 2048-bit or ECC P-256
- **Hash Algorithm**: SHA-256 or stronger
- **Certificate Chain**: Complete and valid certificate chain
- **Validity Period**: Maximum 1 year for public certificates

## Service-Specific Implementation Guidance

### Web Applications and APIs:
- Enable HTTPS with HTTP Strict Transport Security (HSTS)
- Implement proper certificate validation in clients
- Use secure cookie attributes (Secure, HttpOnly, SameSite)
- Configure Content Security Policy (CSP) headers

### Database Connections:
- Enable SSL/TLS for all database connections
- Use certificate-based authentication where supported
- Implement connection encryption for replication
- Configure secure backup and restore procedures

### Messaging and Queuing:
- Enable TLS for message broker connections
- Implement message-level encryption for sensitive data
- Use secure authentication mechanisms
- Configure encrypted message persistence

### File Transfer and Storage:
- Use SFTP, FTPS, or HTTPS for file transfers
- Implement client-side encryption for cloud storage
- Enable encryption for backup and synchronization
- Use secure protocols for content delivery

### Microservices and Containers:
- Implement service mesh with automatic mTLS
- Use secure service discovery mechanisms
- Configure encrypted container-to-container communication
- Implement secure secrets management for certificates

## Related resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html">AWS Well-Architected Framework - Security Pillar</a></li>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/sec-09.html">SEC09: How do you protect your data in transit?</a></li>
    <li><a href="https://docs.aws.amazon.com/acm/latest/userguide/acm-overview.html">AWS Certificate Manager User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/acm-pca/latest/userguide/PcaWelcome.html">AWS Private Certificate Authority User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/elasticloadbalancing/latest/application/create-https-listener.html">Create an HTTPS listener for your Application Load Balancer</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-prepare-for-aws-move-to-its-own-certificate-authority/">How to prepare for AWS move to its own certificate authority</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/tls-1-2-required-for-aws-fips-endpoints/">TLS 1.2 required for AWS FIPS endpoints</a></li>
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
