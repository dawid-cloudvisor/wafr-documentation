---
title: SEC05 - How do you protect your network resources?
layout: default
parent: Security
has_children: true
nav_order: 5
---

<div class="pillar-header">
  <h1>SEC05: How do you protect your network resources?</h1>
  <p>Any workload that has some form of network connectivity, whether it's the internet or a private network, requires multiple layers of defense to help protect from external and internal network-based threats. All network traffic that flows to and from your workload should be controlled at multiple layers with a combination of controls. These controls should include network access controls, such as subnets or security groups, as well as application-level controls, such as web application firewalls.</p>
</div>

## Best Practices

This question includes the following best practices:

<div class="best-practices-list">
  <ul>
    <li><a href="./SEC05-BP01.html">SEC05-BP01: Create network layers</a></li>
    <li><a href="./SEC05-BP02.html">SEC05-BP02: Control traffic at all layers</a></li>
    <li><a href="./SEC05-BP03.html">SEC05-BP03: Implement inspection and protection</a></li>
    <li><a href="./SEC05-BP04.html">SEC05-BP04: Automate network protection</a></li>
    <li><a href="./SEC05-BP05.html">SEC05-BP05: Implement DDoS protection</a></li>
  </ul>
</div>

## Key Concepts

### Network Security Fundamentals

**Defense in Depth**: Implement multiple layers of network security controls to protect against various types of threats. No single control should be relied upon to secure your entire network infrastructure.

**Network Segmentation**: Divide your network into smaller, isolated segments to limit the blast radius of security incidents and control traffic flow between different parts of your workload.

**Zero Trust Networking**: Verify and authenticate all network traffic, regardless of its source or destination. Never trust traffic based solely on network location.

**Least Privilege Network Access**: Grant only the minimum network access required for legitimate business functions, applying the principle of least privilege to network connectivity.

### Network Protection Layers

**Perimeter Security**: Protect the boundary between your network and external networks (internet, partner networks) using firewalls, intrusion detection systems, and DDoS protection.

**Internal Network Security**: Secure traffic flow within your network using micro-segmentation, internal firewalls, and network access controls.

**Application Layer Security**: Protect applications from network-based attacks using web application firewalls, API gateways, and application-specific security controls.

**Infrastructure Security**: Secure the underlying network infrastructure including routers, switches, load balancers, and network management systems.

## AWS Services to Consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon VPC (Virtual Private Cloud)</h4>
    <p>Provides a logically isolated section of the AWS Cloud where you can launch AWS resources in a virtual network. Foundation for implementing network segmentation and access controls.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Security Groups</h4>
    <p>Acts as a virtual firewall for your EC2 instances to control inbound and outbound traffic. Provides stateful packet filtering at the instance level.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Network ACLs</h4>
    <p>Provides an additional layer of security for your VPC that acts as a firewall for controlling traffic in and out of one or more subnets. Offers stateless packet filtering.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS WAF (Web Application Firewall)</h4>
    <p>Helps protect your web applications or APIs against common web exploits and bots. Provides application-layer protection with customizable rules.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Shield</h4>
    <p>Provides managed DDoS protection that safeguards applications running on AWS. Shield Standard is automatically included, while Shield Advanced provides enhanced protections.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Network Firewall</h4>
    <p>A managed service that makes it easy to deploy essential network protections for all of your Amazon VPCs. Provides fine-grained control over network traffic.</p>
  </div>
</div>

## Implementation Approach

### 1. Network Architecture Design
- Design VPC architecture with proper segmentation
- Plan subnet structure for different tiers (public, private, database)
- Implement network isolation between environments
- Design connectivity patterns for hybrid and multi-cloud scenarios
- Plan for scalability and future growth

### 2. Access Control Implementation
- Configure security groups with least privilege rules
- Implement Network ACLs for additional subnet-level protection
- Set up VPC endpoints for secure service access
- Configure NAT gateways for outbound internet access
- Implement private connectivity using AWS PrivateLink

### 3. Traffic Inspection and Protection
- Deploy AWS WAF for application-layer protection
- Implement AWS Network Firewall for advanced inspection
- Configure intrusion detection and prevention systems
- Set up network monitoring and logging
- Implement threat intelligence integration

### 4. DDoS Protection and Resilience
- Enable AWS Shield Standard (automatic)
- Consider AWS Shield Advanced for enhanced protection
- Implement CloudFront for content delivery and protection
- Configure auto-scaling for traffic spikes
- Set up monitoring and alerting for DDoS events

## Network Security Architecture

### Multi-Tier Network Architecture
```
Internet Gateway
    ↓
Public Subnet (Web Tier)
    ↓ (Security Groups + NACLs)
Private Subnet (Application Tier)
    ↓ (Security Groups + NACLs)
Private Subnet (Database Tier)
    ↓
VPC Endpoints / NAT Gateway
```

### Defense in Depth Implementation
```
External Threats
    ↓ AWS Shield (DDoS Protection)
    ↓ AWS WAF (Application Layer)
    ↓ Network Firewall (Network Layer)
    ↓ Security Groups (Instance Level)
    ↓ Network ACLs (Subnet Level)
    ↓ Application Security Controls
```

### Traffic Flow Control
```
User Request
    ↓ CloudFront (CDN + Protection)
    ↓ Application Load Balancer
    ↓ Security Group Rules
    ↓ Application Instances
    ↓ Database Security Groups
    ↓ Database Instances
```

## Network Security Controls Framework

### Preventive Controls
- **Network Segmentation**: VPC design, subnets, security groups
- **Access Controls**: Security group rules, NACLs, VPC endpoints
- **Traffic Filtering**: Firewalls, WAF rules, content filtering
- **Encryption**: TLS/SSL, VPN connections, encrypted protocols

### Detective Controls
- **Traffic Monitoring**: VPC Flow Logs, network monitoring tools
- **Intrusion Detection**: Network-based IDS, anomaly detection
- **Log Analysis**: CloudTrail, DNS logs, firewall logs
- **Threat Intelligence**: IP reputation, domain analysis

### Responsive Controls
- **Automated Blocking**: WAF rules, security group updates
- **Traffic Redirection**: Route table updates, load balancer changes
- **Incident Isolation**: Network segmentation, access revocation
- **DDoS Mitigation**: Shield response, traffic shaping

## Common Challenges and Solutions

### Challenge: Complex Network Architectures
**Solution**: Use infrastructure as code (CloudFormation/CDK) to standardize network deployments, implement consistent naming conventions, and document network designs thoroughly.

### Challenge: Managing Security Group Rules at Scale
**Solution**: Implement centralized security group management, use automation for rule updates, and establish approval processes for security group changes.

### Challenge: East-West Traffic Security
**Solution**: Implement micro-segmentation using security groups, deploy internal firewalls, and use VPC endpoints to reduce internet-bound traffic.

### Challenge: DDoS Attack Mitigation
**Solution**: Enable AWS Shield Advanced, implement CloudFront for content delivery, configure auto-scaling, and establish DDoS response procedures.

### Challenge: Network Performance vs Security
**Solution**: Optimize security controls for performance, use managed services to reduce overhead, and implement intelligent traffic routing.

## Network Security Maturity Levels

### Level 1: Basic Network Security
- Basic VPC setup with public and private subnets
- Security groups with broad rules
- Manual network configuration and management
- Limited network monitoring and logging

### Level 2: Structured Network Security
- Well-designed multi-tier network architecture
- Properly configured security groups and NACLs
- VPC Flow Logs enabled for monitoring
- Basic WAF implementation for web applications

### Level 3: Advanced Network Security
- Comprehensive network segmentation and micro-segmentation
- Advanced threat detection and automated response
- Network Firewall deployment with custom rules
- Integrated DDoS protection and monitoring

### Level 4: Optimized Network Security
- AI/ML-powered threat detection and response
- Automated network security orchestration
- Advanced analytics and threat intelligence integration
- Continuous optimization based on traffic patterns

## Network Protection Best Practices

### Network Design:
1. **Implement Network Segmentation**: Separate different tiers and environments
2. **Use Multiple Availability Zones**: Distribute resources for resilience
3. **Plan IP Address Space**: Use RFC 1918 private address ranges efficiently
4. **Design for Scalability**: Plan for future growth and expansion
5. **Document Network Architecture**: Maintain current network diagrams and documentation

### Access Control:
1. **Apply Least Privilege**: Grant minimum required network access
2. **Use Security Groups Effectively**: Implement specific, purpose-built rules
3. **Layer Network Controls**: Combine security groups, NACLs, and firewalls
4. **Regular Rule Review**: Audit and clean up unnecessary rules
5. **Automate Rule Management**: Use infrastructure as code for consistency

### Traffic Protection:
1. **Enable Comprehensive Logging**: VPC Flow Logs, DNS logs, firewall logs
2. **Implement WAF Protection**: Protect web applications from common attacks
3. **Use Managed Services**: Leverage AWS managed security services
4. **Monitor Traffic Patterns**: Establish baselines and detect anomalies
5. **Integrate Threat Intelligence**: Use external feeds for enhanced protection

## Key Performance Indicators (KPIs)

### Security Metrics:
- Number of blocked attacks and threats
- Security rule coverage and effectiveness
- Mean time to detect network threats (MTTD)
- False positive rate for security alerts

### Performance Metrics:
- Network latency and throughput
- Security control processing overhead
- Availability and uptime metrics
- User experience impact measurements

### Operational Metrics:
- Security group rule compliance rate
- Network configuration drift detection
- Automated response success rate
- Security incident resolution time

## Related resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html">AWS Well-Architected Framework - Security Pillar</a></li>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/sec-05.html">SEC05: How do you protect your network resources?</a></li>
    <li><a href="https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html">Amazon VPC User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html">AWS WAF Developer Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/waf/latest/DDOSAPIReferenceGuide/welcome.html">AWS Shield Advanced Developer Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/network-firewall/latest/developerguide/what-is-aws-network-firewall.html">AWS Network Firewall Developer Guide</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/">AWS Security Blog</a></li>
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
