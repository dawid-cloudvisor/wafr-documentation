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
    <li><a href="./SEC09-BP03.html">SEC09-BP03: Authenticate network communications</a></li>
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
    <p>Provisions, manages, and deploys public and private SSL/TLS certificates for use with AWS services and your internal connected resources. Provides automatic certificate renewal and integration with AWS services like Application Load Balancer, CloudFront, and API Gateway.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Private Certificate Authority (AWS Private CA)</h4>
    <p>Managed private certificate authority service that helps you easily and securely manage the lifecycle of your private certificates. Essential for implementing mutual TLS (mTLS) authentication between services and issuing certificates for internal applications.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon VPC Lattice</h4>
    <p>Application networking service that provides service-to-service connectivity, security, and monitoring for service-oriented architectures. Supports AWS IAM authentication and authorization policies for secure service communication.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon API Gateway</h4>
    <p>Fully managed service for creating, publishing, maintaining, monitoring, and securing APIs. Supports multiple authentication methods including mutual TLS, JWT authorizers, and AWS IAM authentication for secure API access.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Application Load Balancer (ALB)</h4>
    <p>Provides SSL/TLS termination and end-to-end encryption capabilities. Supports mutual TLS authentication, SNI (Server Name Indication) for multiple certificates, and advanced routing based on content.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS PrivateLink</h4>
    <p>Provides private connectivity between VPCs, AWS services, and on-premises applications, securely on the Amazon network. Eliminates exposure of traffic to the public internet and supports authenticated connections.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS IoT Core</h4>
    <p>Managed cloud service that lets connected devices easily and securely interact with cloud applications and other devices. Provides multiple authentication methods including X.509 certificates and AWS IAM credentials.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS IAM Roles Anywhere</h4>
    <p>Allows workloads outside of AWS to access AWS resources using IAM roles and temporary credentials. Enables secure authentication for external systems that need to communicate with AWS services.</p>
  </div>
</div>

## Implementation Approach

### 1. Secure Key and Certificate Management (SEC09-BP01)
- Implement centralized certificate management using AWS Certificate Manager
- Establish certificate lifecycle management procedures including automated renewal
- Configure certificate monitoring and alerting for expiration and validation issues
- Use AWS Private CA for internal certificates and mutual TLS authentication
- Implement proper certificate validation and chain verification
- Plan for certificate revocation and emergency replacement procedures

### 2. Enforce Encryption in Transit (SEC09-BP02)
- Enable HTTPS/TLS for all web applications and APIs with strong cipher suites
- Configure end-to-end encryption for service-to-service communication
- Implement TLS 1.2 or higher as the minimum protocol version
- Use AWS services that enforce encryption by default (ALB, API Gateway, CloudFront)
- Enable encryption for database connections, messaging systems, and file transfers
- Implement automated detection and remediation of unencrypted communications

### 3. Authenticate Network Communications (SEC09-BP03)
- Implement mutual TLS (mTLS) for service-to-service authentication
- Use AWS Signature Version 4 (SigV4) for API authentication and authorization
- Deploy Amazon VPC Lattice for secure service-to-service communication with built-in authentication
- Configure OAuth 2.0 and OpenID Connect (OIDC) for user and service authentication
- Use AWS IAM Roles Anywhere for external systems requiring AWS service access
- Implement comprehensive monitoring for authentication events and failures

## Data in Transit Protection Architecture

### Comprehensive Data in Transit Protection
```
External Users/Systems
    ↓ (HTTPS/TLS with Client Certificates)
AWS Certificate Manager (ACM)
    ↓ (Certificate Management & Renewal)
Application Load Balancer
    ↓ (TLS Termination & mTLS Authentication)
Amazon VPC Lattice / API Gateway
    ↓ (Service Authentication & Authorization)
Microservices
    ↓ (Service-to-Service mTLS)
AWS Private CA
    ↓ (Internal Certificate Issuance)
Backend Services & Databases
    ↓ (Encrypted Connections)
```

### Certificate Management Lifecycle (SEC09-BP01)
```
Certificate Request
    ↓ (Automated CSR Generation)
AWS Certificate Manager / AWS Private CA
    ↓ (Certificate Issuance & Validation)
Automated Certificate Deployment
    ↓ (Integration with AWS Services)
Certificate Monitoring & Alerting
    ↓ (Expiration & Health Tracking)
Automated Certificate Renewal
    ↓ (Zero-Downtime Updates)
Certificate Revocation (if needed)
```

### Encryption Enforcement Flow (SEC09-BP02)
```
Client Request
    ↓ (TLS 1.2+ Required)
Protocol Validation
    ↓ (Strong Cipher Suite Enforcement)
Certificate Verification
    ↓ (Chain Validation & Revocation Check)
Encrypted Channel Establishment
    ↓ (Perfect Forward Secrecy)
Secure Data Transmission
    ↓ (End-to-End Encryption)
Service Processing & Response
```

### Network Authentication Flow (SEC09-BP03)
```
Service/Client Identity
    ↓ (Certificate or AWS IAM Credentials)
Authentication Method Selection
    ├── mTLS (X.509 Certificates)
    ├── AWS SigV4 (IAM-based)
    └── JWT/OAuth 2.0 (Token-based)
Identity Verification
    ↓ (Certificate/Token Validation)
Authorization Policy Check
    ↓ (VPC Lattice Auth Policies / IAM Policies)
Secure Communication Established
    ↓ (Authenticated & Encrypted Channel)
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

### SEC09-BP01: Secure Key and Certificate Management
1. **Centralized Certificate Management**: Use AWS Certificate Manager for consistent certificate handling across all services
2. **Automated Certificate Lifecycle**: Implement automatic certificate provisioning, renewal, and deployment
3. **Certificate Monitoring**: Continuously monitor certificate health, expiration dates, and validation status
4. **Private Certificate Authority**: Use AWS Private CA for internal certificates and mutual TLS authentication
5. **Certificate Validation**: Implement proper certificate chain validation and revocation checking
6. **Emergency Procedures**: Establish rapid certificate revocation and replacement processes for security incidents

### SEC09-BP02: Enforce Encryption in Transit
1. **Universal Encryption**: Apply encryption to all data in transit, both external and internal communications
2. **Strong Protocol Standards**: Use TLS 1.2 or higher with strong cipher suites and perfect forward secrecy
3. **Service Integration**: Leverage AWS services that enforce encryption by default (ALB, API Gateway, CloudFront)
4. **End-to-End Encryption**: Protect data from source to destination without intermediate plaintext exposure
5. **Automated Enforcement**: Implement policies and controls that prevent unencrypted communications
6. **Performance Optimization**: Balance security with performance using efficient encryption implementations

### SEC09-BP03: Authenticate Network Communications
1. **Mutual Authentication**: Implement mTLS for service-to-service communication to verify both parties
2. **AWS IAM Integration**: Use AWS Signature Version 4 (SigV4) for API authentication and authorization
3. **Service Mesh Security**: Deploy Amazon VPC Lattice for secure, authenticated service-to-service communication
4. **Standard Protocols**: Implement OAuth 2.0 and OpenID Connect (OIDC) for user and service authentication
5. **External System Integration**: Use AWS IAM Roles Anywhere for secure authentication of external systems
6. **Comprehensive Monitoring**: Monitor all authentication events, failures, and anomalous access patterns

## Key Performance Indicators (KPIs)

### Certificate Management Metrics (SEC09-BP01):
- Certificate renewal success rate and automation coverage
- Certificate expiration incidents and near-miss events
- Mean time to certificate deployment and propagation
- Certificate validation failure rate and resolution time
- Private CA certificate issuance and revocation metrics

### Encryption Enforcement Metrics (SEC09-BP02):
- Percentage of communications encrypted in transit (target: 100%)
- TLS/SSL protocol version compliance rate (TLS 1.2+ adoption)
- Strong cipher suite usage percentage
- Unencrypted communication detection and remediation time
- Encryption performance impact and optimization metrics

### Authentication Metrics (SEC09-BP03):
- Mutual TLS authentication success rate for service-to-service communication
- AWS SigV4 authentication adoption rate across APIs
- Authentication failure rate and incident response time
- OAuth/OIDC token validation success rate
- Network authentication coverage across all communication paths

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
  
  <h3>AWS Well-Architected Framework</h3>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html">AWS Well-Architected Framework - Security Pillar</a></li>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/sec-09.html">SEC09: How do you protect your data in transit?</a></li>
  </ul>

  <h3>Certificate Management (SEC09-BP01)</h3>
  <ul>
    <li><a href="https://docs.aws.amazon.com/acm/latest/userguide/acm-overview.html">AWS Certificate Manager User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/acm-pca/latest/userguide/PcaWelcome.html">AWS Private Certificate Authority User Guide</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-prepare-for-aws-move-to-its-own-certificate-authority/">How to prepare for AWS move to its own certificate authority</a></li>
  </ul>

  <h3>Encryption in Transit (SEC09-BP02)</h3>
  <ul>
    <li><a href="https://docs.aws.amazon.com/elasticloadbalancing/latest/application/create-https-listener.html">Create an HTTPS listener for your Application Load Balancer</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/tls-1-2-required-for-aws-fips-endpoints/">TLS 1.2 required for AWS FIPS endpoints</a></li>
    <li><a href="https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html">Working with AWS Lambda proxy integrations for HTTP APIs</a></li>
  </ul>

  <h3>Network Authentication (SEC09-BP03)</h3>
  <ul>
    <li><a href="https://docs.aws.amazon.com/vpc-lattice/latest/ug/what-is-vpc-lattice.html">What is Amazon VPC Lattice?</a></li>
    <li><a href="https://docs.aws.amazon.com/apigateway/latest/developerguide/rest-api-mutual-tls.html">Configuring mutual TLS authentication for a REST API</a></li>
    <li><a href="https://docs.aws.amazon.com/elasticloadbalancing/latest/application/mutual-authentication.html">Mutual TLS authentication for Application Load Balancer</a></li>
    <li><a href="https://docs.aws.amazon.com/rolesanywhere/latest/userguide/introduction.html">AWS IAM Roles Anywhere User Guide</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-secure-api-gateway-http-endpoints-with-jwt-authorizer/">How to secure API Gateway HTTP endpoints with JWT authorizer</a></li>
  </ul>

  <h3>Implementation Examples and Workshops</h3>
  <ul>
    <li><a href="https://catalog.us-east-1.prod.workshops.aws/workshops/9e543f60-e409-43d4-b37f-78ff3e1a07f5/en-US">Amazon VPC Lattice Workshop</a></li>
    <li><a href="https://catalog.us-east-1.prod.workshops.aws/workshops/dc413216-deab-4371-9e4a-879a4f14233d/en-US">Zero-Trust Episode 1 – The Phantom Service Perimeter workshop</a></li>
    <li><a href="https://aws.amazon.com/blogs/compute/evaluating-access-control-methods-to-secure-amazon-api-gateway-apis/">Evaluating access control methods to secure Amazon API Gateway APIs</a></li>
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
