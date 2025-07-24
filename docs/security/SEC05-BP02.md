---
title: SEC05-BP02 - Control traffic flow within your network layers
layout: default
parent: SEC05 - How do you protect your network resources?
grand_parent: Security
nav_order: 2
---

<div class="pillar-header">
  <h1>SEC05-BP02: Control traffic flow within your network layers</h1>
  <p>When designing your network topology, you should apply multiple controls with a defense in depth approach for both inbound and outbound traffic, including the use of security groups, network ACLs, subnets, and firewalls. Within AWS, you can choose from multiple firewall options for controlling traffic flow, including AWS WAF for applications, AWS Network Firewall for VPCs, and AWS Shield for DDoS protection.</p>
</div>

## Implementation guidance

Controlling traffic flow within network layers is essential for implementing a robust security posture. By applying multiple layers of traffic controls, you can ensure that only authorized traffic flows between network segments while blocking malicious or unauthorized communications.

### Key steps for implementing this best practice:

1. **Implement layered traffic controls**:
   - Deploy multiple security controls at different network layers
   - Use security groups for instance-level traffic filtering
   - Configure Network ACLs for subnet-level access control
   - Implement network firewalls for advanced traffic inspection
   - Apply web application firewalls for application-layer protection

2. **Configure inbound traffic controls**:
   - Restrict inbound traffic to only necessary ports and protocols
   - Implement source-based access controls using IP ranges or security groups
   - Configure load balancers with appropriate security settings
   - Use AWS WAF to protect web applications from common attacks
   - Enable DDoS protection with AWS Shield

3. **Manage outbound traffic controls**:
   - Control outbound internet access through NAT gateways or instances
   - Implement egress filtering to prevent data exfiltration
   - Use VPC endpoints to keep AWS service traffic within the AWS network
   - Configure proxy servers for controlled internet access
   - Monitor and log all outbound connections

4. **Implement micro-segmentation**:
   - Create granular security groups for specific application components
   - Use security group references to control inter-service communication
   - Implement network policies for container environments
   - Apply zero-trust networking principles
   - Segment traffic based on application tiers and data sensitivity

5. **Configure advanced traffic inspection**:
   - Deploy AWS Network Firewall for deep packet inspection
   - Implement intrusion detection and prevention systems
   - Use traffic mirroring for security analysis
   - Configure SSL/TLS inspection where appropriate
   - Integrate with threat intelligence feeds

6. **Monitor and analyze traffic flows**:
   - Enable VPC Flow Logs for comprehensive traffic visibility
   - Implement real-time traffic monitoring and alerting
   - Use network analytics tools for traffic pattern analysis
   - Set up automated responses to suspicious traffic patterns
   - Regularly review and optimize traffic control rules

## Implementation examples

### Example 1: Layered security group configuration

```json
{
  "WebTierSecurityGroup": {
    "Type": "AWS::EC2::SecurityGroup",
    "Properties": {
      "GroupDescription": "Security group for web tier with strict traffic controls",
      "VpcId": {"Ref": "MainVPC"},
      "SecurityGroupIngress": [
        {
          "IpProtocol": "tcp",
          "FromPort": 443,
          "ToPort": 443,
          "SourceSecurityGroupId": {"Ref": "LoadBalancerSecurityGroup"},
          "Description": "HTTPS from load balancer only"
        },
        {
          "IpProtocol": "tcp",
          "FromPort": 22,
          "ToPort": 22,
          "SourceSecurityGroupId": {"Ref": "BastionSecurityGroup"},
          "Description": "SSH from bastion host only"
        }
      ],
      "SecurityGroupEgress": [
        {
          "IpProtocol": "tcp",
          "FromPort": 8080,
          "ToPort": 8080,
          "DestinationSecurityGroupId": {"Ref": "AppTierSecurityGroup"},
          "Description": "Application tier access"
        },
        {
          "IpProtocol": "tcp",
          "FromPort": 443,
          "ToPort": 443,
          "CidrIp": "0.0.0.0/0",
          "Description": "HTTPS outbound for updates"
        },
        {
          "IpProtocol": "tcp",
          "FromPort": 53,
          "ToPort": 53,
          "CidrIp": "0.0.0.0/0",
          "Description": "DNS resolution"
        },
        {
          "IpProtocol": "udp",
          "FromPort": 53,
          "ToPort": 53,
          "CidrIp": "0.0.0.0/0",
          "Description": "DNS resolution"
        }
      ],
      "Tags": [
        {"Key": "Name", "Value": "Web-Tier-SG"},
        {"Key": "Layer", "Value": "Web"}
      ]
    }
  },
  "AppTierSecurityGroup": {
    "Type": "AWS::EC2::SecurityGroup",
    "Properties": {
      "GroupDescription": "Security group for application tier",
      "VpcId": {"Ref": "MainVPC"},
      "SecurityGroupIngress": [
        {
          "IpProtocol": "tcp",
          "FromPort": 8080,
          "ToPort": 8080,
          "SourceSecurityGroupId": {"Ref": "WebTierSecurityGroup"},
          "Description": "Application port from web tier"
        },
        {
          "IpProtocol": "tcp",
          "FromPort": 22,
          "ToPort": 22,
          "SourceSecurityGroupId": {"Ref": "BastionSecurityGroup"},
          "Description": "SSH from bastion host only"
        }
      ],
      "SecurityGroupEgress": [
        {
          "IpProtocol": "tcp",
          "FromPort": 3306,
          "ToPort": 3306,
          "DestinationSecurityGroupId": {"Ref": "DatabaseSecurityGroup"},
          "Description": "MySQL database access"
        },
        {
          "IpProtocol": "tcp",
          "FromPort": 6379,
          "ToPort": 6379,
          "DestinationSecurityGroupId": {"Ref": "CacheSecurityGroup"},
          "Description": "Redis cache access"
        },
        {
          "IpProtocol": "tcp",
          "FromPort": 443,
          "ToPort": 443,
          "CidrIp": "0.0.0.0/0",
          "Description": "HTTPS for external API calls"
        }
      ],
      "Tags": [
        {"Key": "Name", "Value": "App-Tier-SG"},
        {"Key": "Layer", "Value": "Application"}
      ]
    }
  },
  "DatabaseSecurityGroup": {
    "Type": "AWS::EC2::SecurityGroup",
    "Properties": {
      "GroupDescription": "Security group for database tier",
      "VpcId": {"Ref": "MainVPC"},
      "SecurityGroupIngress": [
        {
          "IpProtocol": "tcp",
          "FromPort": 3306,
          "ToPort": 3306,
          "SourceSecurityGroupId": {"Ref": "AppTierSecurityGroup"},
          "Description": "MySQL from application tier"
        },
        {
          "IpProtocol": "tcp",
          "FromPort": 22,
          "ToPort": 22,
          "SourceSecurityGroupId": {"Ref": "BastionSecurityGroup"},
          "Description": "SSH from bastion host only"
        }
      ],
      "Tags": [
        {"Key": "Name", "Value": "Database-Tier-SG"},
        {"Key": "Layer", "Value": "Database"}
      ]
    }
  }
}
```

### Example 2: AWS Network Firewall configuration

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'AWS Network Firewall for advanced traffic control'

Resources:
  # Network Firewall Rule Group for Web Traffic
  WebTrafficRuleGroup:
    Type: AWS::NetworkFirewall::RuleGroup
    Properties:
      RuleGroupName: WebTrafficRules
      Type: STATEFUL
      Capacity: 100
      RuleGroup:
        RulesSource:
          StatefulRules:
            - Action: PASS
              Header:
                Direction: FORWARD
                Protocol: TCP
                Source: ANY
                SourcePort: ANY
                Destination: 10.0.1.0/24
                DestinationPort: 443
              RuleOptions:
                - Keyword: sid
                  Settings: ['1']
            - Action: PASS
              Header:
                Direction: FORWARD
                Protocol: TCP
                Source: ANY
                SourcePort: ANY
                Destination: 10.0.1.0/24
                DestinationPort: 80
              RuleOptions:
                - Keyword: sid
                  Settings: ['2']
            - Action: DROP
              Header:
                Direction: FORWARD
                Protocol: TCP
                Source: ANY
                SourcePort: ANY
                Destination: 10.0.1.0/24
                DestinationPort: ANY
              RuleOptions:
                - Keyword: sid
                  Settings: ['3']
      Tags:
        - Key: Name
          Value: Web-Traffic-Rules

  # Network Firewall Rule Group for Application Traffic
  AppTrafficRuleGroup:
    Type: AWS::NetworkFirewall::RuleGroup
    Properties:
      RuleGroupName: AppTrafficRules
      Type: STATEFUL
      Capacity: 100
      RuleGroup:
        RulesSource:
          StatefulRules:
            - Action: PASS
              Header:
                Direction: FORWARD
                Protocol: TCP
                Source: 10.0.1.0/24
                SourcePort: ANY
                Destination: 10.0.11.0/24
                DestinationPort: 8080
              RuleOptions:
                - Keyword: sid
                  Settings: ['10']
            - Action: DROP
              Header:
                Direction: FORWARD
                Protocol: TCP
                Source: ANY
                SourcePort: ANY
                Destination: 10.0.11.0/24
                DestinationPort: ANY
              RuleOptions:
                - Keyword: sid
                  Settings: ['11']
      Tags:
        - Key: Name
          Value: App-Traffic-Rules

  # Network Firewall Policy
  NetworkFirewallPolicy:
    Type: AWS::NetworkFirewall::FirewallPolicy
    Properties:
      FirewallPolicyName: MainFirewallPolicy
      FirewallPolicy:
        StatelessDefaultActions:
          - aws:forward_to_sfe
        StatelessFragmentDefaultActions:
          - aws:forward_to_sfe
        StatefulRuleGroupReferences:
          - ResourceArn: !Ref WebTrafficRuleGroup
            Priority: 100
          - ResourceArn: !Ref AppTrafficRuleGroup
            Priority: 200
        StatefulDefaultActions:
          - aws:drop_strict
      Tags:
        - Key: Name
          Value: Main-Firewall-Policy

  # Network Firewall
  NetworkFirewall:
    Type: AWS::NetworkFirewall::Firewall
    Properties:
      FirewallName: MainNetworkFirewall
      FirewallPolicyArn: !Ref NetworkFirewallPolicy
      VpcId: !Ref MainVPC
      SubnetMappings:
        - SubnetId: !Ref FirewallSubnet1
        - SubnetId: !Ref FirewallSubnet2
      Tags:
        - Key: Name
          Value: Main-Network-Firewall

  # Firewall Logging Configuration
  FirewallLogging:
    Type: AWS::NetworkFirewall::LoggingConfiguration
    Properties:
      FirewallArn: !Ref NetworkFirewall
      LoggingConfiguration:
        LogDestinationConfigs:
          - LogType: FLOW
            LogDestination:
              logGroup: !Ref FirewallLogGroup
            LogDestinationType: CloudWatchLogs
          - LogType: ALERT
            LogDestination:
              logGroup: !Ref FirewallLogGroup
            LogDestinationType: CloudWatchLogs

  # CloudWatch Log Group for Firewall Logs
  FirewallLogGroup:
    Type: AWS::Logs::LogGroup
    Properties:
      LogGroupName: /aws/networkfirewall/logs
      RetentionInDays: 90

Outputs:
  NetworkFirewallArn:
    Description: ARN of the Network Firewall
    Value: !Ref NetworkFirewall
    Export:
      Name: !Sub '${AWS::StackName}-NetworkFirewall-ARN'
```

### Example 3: AWS WAF configuration for application layer protection

```python
import boto3
import json

def create_waf_configuration():
    """Create AWS WAF configuration for application layer traffic control"""
    
    wafv2 = boto3.client('wafv2')
    
    # Create IP set for allowed countries
    ip_set_response = wafv2.create_ip_set(
        Name='AllowedCountriesIPSet',
        Scope='REGIONAL',
        IPAddressVersion='IPV4',
        Addresses=[
            # Add specific IP ranges for allowed countries
            '203.0.113.0/24',  # Example IP range
            '198.51.100.0/24'  # Example IP range
        ],
        Description='IP addresses from allowed countries',
        Tags=[
            {
                'Key': 'Name',
                'Value': 'Allowed-Countries-IP-Set'
            }
        ]
    )
    
    ip_set_arn = ip_set_response['Summary']['ARN']
    
    # Create WAF Web ACL with multiple rules
    web_acl_rules = [
        {
            'Name': 'AWSManagedRulesCommonRuleSet',
            'Priority': 1,
            'OverrideAction': {'None': {}},
            'Statement': {
                'ManagedRuleGroupStatement': {
                    'VendorName': 'AWS',
                    'Name': 'AWSManagedRulesCommonRuleSet'
                }
            },
            'VisibilityConfig': {
                'SampledRequestsEnabled': True,
                'CloudWatchMetricsEnabled': True,
                'MetricName': 'CommonRuleSetMetric'
            }
        },
        {
            'Name': 'AWSManagedRulesKnownBadInputsRuleSet',
            'Priority': 2,
            'OverrideAction': {'None': {}},
            'Statement': {
                'ManagedRuleGroupStatement': {
                    'VendorName': 'AWS',
                    'Name': 'AWSManagedRulesKnownBadInputsRuleSet'
                }
            },
            'VisibilityConfig': {
                'SampledRequestsEnabled': True,
                'CloudWatchMetricsEnabled': True,
                'MetricName': 'KnownBadInputsMetric'
            }
        },
        {
            'Name': 'RateLimitRule',
            'Priority': 3,
            'Action': {'Block': {}},
            'Statement': {
                'RateBasedStatement': {
                    'Limit': 2000,
                    'AggregateKeyType': 'IP'
                }
            },
            'VisibilityConfig': {
                'SampledRequestsEnabled': True,
                'CloudWatchMetricsEnabled': True,
                'MetricName': 'RateLimitMetric'
            }
        },
        {
            'Name': 'GeoBlockRule',
            'Priority': 4,
            'Action': {'Block': {}},
            'Statement': {
                'NotStatement': {
                    'Statement': {
                        'IPSetReferenceStatement': {
                            'ARN': ip_set_arn
                        }
                    }
                }
            },
            'VisibilityConfig': {
                'SampledRequestsEnabled': True,
                'CloudWatchMetricsEnabled': True,
                'MetricName': 'GeoBlockMetric'
            }
        }
    ]
    
    try:
        web_acl_response = wafv2.create_web_acl(
            Name='ApplicationProtectionWebACL',
            Scope='REGIONAL',
            DefaultAction={'Allow': {}},
            Rules=web_acl_rules,
            Description='Web ACL for application layer traffic control',
            Tags=[
                {
                    'Key': 'Name',
                    'Value': 'Application-Protection-WebACL'
                }
            ],
            VisibilityConfig={
                'SampledRequestsEnabled': True,
                'CloudWatchMetricsEnabled': True,
                'MetricName': 'ApplicationProtectionWebACL'
            }
        )
        
        web_acl_arn = web_acl_response['Summary']['ARN']
        print(f"Created Web ACL: {web_acl_arn}")
        
        return web_acl_arn
        
    except Exception as e:
        print(f"Error creating Web ACL: {str(e)}")
        return None

def associate_waf_with_alb(web_acl_arn, alb_arn):
    """Associate WAF Web ACL with Application Load Balancer"""
    
    wafv2 = boto3.client('wafv2')
    
    try:
        wafv2.associate_web_acl(
            WebACLArn=web_acl_arn,
            ResourceArn=alb_arn
        )
        print(f"Associated Web ACL with ALB: {alb_arn}")
        
    except Exception as e:
        print(f"Error associating Web ACL with ALB: {str(e)}")

def setup_waf_logging(web_acl_arn):
    """Configure WAF logging for traffic analysis"""
    
    wafv2 = boto3.client('wafv2')
    logs = boto3.client('logs')
    
    # Create CloudWatch Log Group for WAF logs
    log_group_name = '/aws/wafv2/logs'
    
    try:
        logs.create_log_group(
            logGroupName=log_group_name,
            retentionInDays=90
        )
        print(f"Created log group: {log_group_name}")
    except logs.exceptions.ResourceAlreadyExistsException:
        print(f"Log group already exists: {log_group_name}")
    
    # Configure WAF logging
    try:
        wafv2.put_logging_configuration(
            LoggingConfiguration={
                'ResourceArn': web_acl_arn,
                'LogDestinationConfigs': [
                    f'arn:aws:logs:us-west-2:123456789012:log-group:{log_group_name}'
                ],
                'RedactedFields': [
                    {
                        'SingleHeader': {
                            'Name': 'authorization'
                        }
                    },
                    {
                        'SingleHeader': {
                            'Name': 'cookie'
                        }
                    }
                ]
            }
        )
        print("Configured WAF logging")
        
    except Exception as e:
        print(f"Error configuring WAF logging: {str(e)}")

# Example usage
if __name__ == "__main__":
    web_acl_arn = create_waf_configuration()
    if web_acl_arn:
        # Replace with your ALB ARN
        alb_arn = "arn:aws:elasticloadbalancing:us-west-2:123456789012:loadbalancer/app/my-alb/1234567890123456"
        associate_waf_with_alb(web_acl_arn, alb_arn)
        setup_waf_logging(web_acl_arn)
```

### Example 4: VPC endpoints for controlled AWS service access

```bash
# Create VPC endpoint for S3 (Gateway endpoint)
aws ec2 create-vpc-endpoint \
  --vpc-id vpc-12345678 \
  --service-name com.amazonaws.us-west-2.s3 \
  --vpc-endpoint-type Gateway \
  --route-table-ids rtb-12345678 rtb-87654321 \
  --policy-document '{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": "*",
        "Action": [
          "s3:GetObject",
          "s3:PutObject"
        ],
        "Resource": [
          "arn:aws:s3:::my-secure-bucket/*"
        ]
      }
    ]
  }' \
  --tag-specifications 'ResourceType=vpc-endpoint,Tags=[{Key=Name,Value=S3-VPC-Endpoint}]'

# Create VPC endpoint for EC2 (Interface endpoint)
aws ec2 create-vpc-endpoint \
  --vpc-id vpc-12345678 \
  --service-name com.amazonaws.us-west-2.ec2 \
  --vpc-endpoint-type Interface \
  --subnet-ids subnet-12345678 subnet-87654321 \
  --security-group-ids sg-12345678 \
  --private-dns-enabled \
  --policy-document '{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": "*",
        "Action": [
          "ec2:DescribeInstances",
          "ec2:DescribeImages",
          "ec2:DescribeSnapshots"
        ],
        "Resource": "*"
      }
    ]
  }' \
  --tag-specifications 'ResourceType=vpc-endpoint,Tags=[{Key=Name,Value=EC2-VPC-Endpoint}]'

# Create VPC endpoint for Systems Manager
aws ec2 create-vpc-endpoint \
  --vpc-id vpc-12345678 \
  --service-name com.amazonaws.us-west-2.ssm \
  --vpc-endpoint-type Interface \
  --subnet-ids subnet-12345678 subnet-87654321 \
  --security-group-ids sg-12345678 \
  --private-dns-enabled \
  --tag-specifications 'ResourceType=vpc-endpoint,Tags=[{Key=Name,Value=SSM-VPC-Endpoint}]'

# Create security group for VPC endpoints
aws ec2 create-security-group \
  --group-name VPCEndpoint-SG \
  --description "Security group for VPC endpoints" \
  --vpc-id vpc-12345678 \
  --tag-specifications 'ResourceType=security-group,Tags=[{Key=Name,Value=VPCEndpoint-SG}]'

# Allow HTTPS traffic to VPC endpoints
aws ec2 authorize-security-group-ingress \
  --group-id sg-12345678 \
  --protocol tcp \
  --port 443 \
  --source-group sg-87654321 \
  --group-owner-id 123456789012
```

## AWS services to consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Security Groups</h4>
    <p>Acts as a virtual firewall for your EC2 instances to control inbound and outbound traffic. Provides stateful packet filtering and supports security group references for micro-segmentation.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Network ACLs</h4>
    <p>Provides an additional layer of security for your VPC that acts as a firewall for controlling traffic in and out of subnets. Offers stateless packet filtering with explicit allow and deny rules.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Network Firewall</h4>
    <p>A managed service that makes it easy to deploy essential network protections for all of your Amazon VPCs. Provides fine-grained control over network traffic with stateful inspection.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS WAF (Web Application Firewall)</h4>
    <p>Helps protect your web applications or APIs against common web exploits and bots. Provides application-layer protection with customizable rules and managed rule sets.</p>
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
    <h4>VPC Endpoints</h4>
    <p>Enables you to privately connect your VPC to supported AWS services without requiring an internet gateway. Helps control and secure traffic to AWS services.</p>
  </div>
</div>

## Benefits of controlling traffic flow within network layers

- **Enhanced security posture**: Multiple layers of controls provide comprehensive protection against various attack vectors
- **Reduced attack surface**: Granular traffic controls limit potential entry points for attackers
- **Improved compliance**: Supports regulatory requirements for network security and data protection
- **Better incident containment**: Traffic controls help limit the spread of security incidents
- **Enhanced visibility**: Detailed traffic controls provide better monitoring and analysis capabilities
- **Flexible security policies**: Layered approach allows for different security policies at different network levels
- **Scalable protection**: Controls can be applied consistently across large and complex network architectures

## Related resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/sec_network_protection_layered.html">AWS Well-Architected Framework - Control traffic flow within your network layers</a></li>
    <li><a href="https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-groups.html">Security groups for your VPC</a></li>
    <li><a href="https://docs.aws.amazon.com/vpc/latest/userguide/vpc-network-acls.html">Network ACLs</a></li>
    <li><a href="https://docs.aws.amazon.com/network-firewall/latest/developerguide/what-is-aws-network-firewall.html">AWS Network Firewall Developer Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html">AWS WAF Developer Guide</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-create-a-more-secure-environment-by-using-security-groups-as-a-firewall/">How to create a more secure environment by using security groups as a firewall</a></li>
  </ul>
</div>
