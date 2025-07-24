---
title: SEC05-BP03 - Implement inspection-based protection
layout: default
parent: SEC05 - How do you protect your network resources?
grand_parent: Security
nav_order: 3
---

<div class="pillar-header">
  <h1>SEC05-BP03: Implement inspection-based protection</h1>
  <p>Inspect and filter your traffic at each layer. For example, a web application firewall can help protect against malicious web requests. You can use inspection to identify attacks, malware, and other threats, and to take action to stop them. You can also use inspection to identify and block unwanted traffic, such as traffic from known bad IP addresses or traffic that doesn't match your expected patterns.</p>
</div>

## Implementation guidance

Inspection-based protection involves analyzing network traffic, application requests, and system behavior to identify and block malicious activities. By implementing comprehensive inspection at multiple layers, you can detect sophisticated attacks that might bypass traditional security controls.

### Key steps for implementing this best practice:

1. **Implement deep packet inspection**:
   - Deploy network firewalls with deep packet inspection capabilities
   - Configure stateful inspection rules for traffic analysis
   - Implement protocol-specific inspection for common services
   - Use signature-based detection for known attack patterns
   - Enable behavioral analysis for anomaly detection

2. **Configure web application firewalls**:
   - Deploy AWS WAF for web application protection
   - Configure managed rule sets for common attack patterns
   - Implement custom rules for application-specific threats
   - Enable rate limiting and geo-blocking capabilities
   - Configure bot detection and mitigation

3. **Implement intrusion detection and prevention**:
   - Deploy network-based intrusion detection systems (NIDS)
   - Configure host-based intrusion detection systems (HIDS)
   - Implement real-time threat detection and alerting
   - Configure automated response to detected threats
   - Integrate with threat intelligence feeds

4. **Enable SSL/TLS inspection**:
   - Implement SSL/TLS decryption for encrypted traffic analysis
   - Configure certificate management for inspection proxies
   - Balance security inspection with privacy requirements
   - Implement selective decryption based on risk assessment
   - Ensure compliance with regulatory requirements

5. **Deploy malware detection**:
   - Implement file scanning and malware detection
   - Configure sandboxing for suspicious file analysis
   - Enable real-time malware signature updates
   - Implement behavioral analysis for zero-day threats
   - Configure quarantine and remediation procedures

6. **Monitor and analyze inspection data**:
   - Centralize inspection logs and alerts
   - Implement correlation and analysis of inspection data
   - Configure dashboards for security visibility
   - Set up automated alerting for critical threats
   - Conduct regular analysis of inspection effectiveness

## Implementation examples

### Example 1: AWS Network Firewall with deep packet inspection

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'AWS Network Firewall with comprehensive inspection rules'

Resources:
  # Stateful Rule Group for Malware Detection
  MalwareDetectionRuleGroup:
    Type: AWS::NetworkFirewall::RuleGroup
    Properties:
      RuleGroupName: MalwareDetectionRules
      Type: STATEFUL
      Capacity: 200
      RuleGroup:
        RulesSource:
          RulesSourceList:
            TargetTypes:
              - HTTP_HOST
              - TLS_SNI
            Targets:
              - malware.example.com
              - phishing.example.com
              - botnet.example.com
            GeneratedRulesType: DENYLIST
        RuleVariables:
          IPSets:
            MALWARE_IPS:
              Definition:
                - '192.0.2.0/24'
                - '203.0.113.0/24'
          PortSets:
            SUSPICIOUS_PORTS:
              Definition:
                - '1337'
                - '31337'
                - '54321'
      Tags:
        - Key: Name
          Value: Malware-Detection-Rules

  # Stateful Rule Group for Protocol Inspection
  ProtocolInspectionRuleGroup:
    Type: AWS::NetworkFirewall::RuleGroup
    Properties:
      RuleGroupName: ProtocolInspectionRules
      Type: STATEFUL
      Capacity: 300
      RuleGroup:
        RulesSource:
          StatefulRules:
            - Action: DROP
              Header:
                Direction: FORWARD
                Protocol: TCP
                Source: ANY
                SourcePort: ANY
                Destination: ANY
                DestinationPort: $SUSPICIOUS_PORTS
              RuleOptions:
                - Keyword: sid
                  Settings: ['100']
                - Keyword: msg
                  Settings: ['"Suspicious port access detected"']
            - Action: ALERT
              Header:
                Direction: FORWARD
                Protocol: TCP
                Source: $MALWARE_IPS
                SourcePort: ANY
                Destination: ANY
                DestinationPort: ANY
              RuleOptions:
                - Keyword: sid
                  Settings: ['101']
                - Keyword: msg
                  Settings: ['"Traffic from known malware IP"']
            - Action: DROP
              Header:
                Direction: FORWARD
                Protocol: TCP
                Source: ANY
                SourcePort: ANY
                Destination: ANY
                DestinationPort: ANY
              RuleOptions:
                - Keyword: sid
                  Settings: ['102']
                - Keyword: content
                  Settings: ['"|28 29 2A 2B|"']
                - Keyword: msg
                  Settings: ['"Potential buffer overflow attempt"']
        RuleVariables:
          IPSets:
            MALWARE_IPS:
              Definition:
                - '192.0.2.0/24'
                - '203.0.113.0/24'
          PortSets:
            SUSPICIOUS_PORTS:
              Definition:
                - '1337'
                - '31337'
                - '54321'
      Tags:
        - Key: Name
          Value: Protocol-Inspection-Rules

  # Stateless Rule Group for Initial Filtering
  StatelessFilteringRuleGroup:
    Type: AWS::NetworkFirewall::RuleGroup
    Properties:
      RuleGroupName: StatelessFilteringRules
      Type: STATELESS
      Capacity: 100
      RuleGroup:
        RulesSource:
          StatelessRulesAndCustomActions:
            StatelessRules:
              - RuleDefinition:
                  MatchAttributes:
                    Sources:
                      - AddressDefinition: '0.0.0.0/0'
                    Destinations:
                      - AddressDefinition: '10.0.0.0/8'
                    DestinationPorts:
                      - FromPort: 22
                        ToPort: 22
                    Protocols: [6]
                  Actions:
                    - aws:forward_to_sfe
                Priority: 100
              - RuleDefinition:
                  MatchAttributes:
                    Sources:
                      - AddressDefinition: '192.0.2.0/24'
                    Destinations:
                      - AddressDefinition: '0.0.0.0/0'
                    Protocols: [6, 17]
                  Actions:
                    - aws:drop
                Priority: 200
      Tags:
        - Key: Name
          Value: Stateless-Filtering-Rules

### Example 2: Advanced AWS WAF configuration with inspection rules

```python
import boto3
import json

def create_advanced_waf_configuration():
    """Create advanced AWS WAF configuration with comprehensive inspection"""
    
    wafv2 = boto3.client('wafv2')
    
    # Create regex pattern set for SQL injection detection
    sql_injection_patterns = wafv2.create_regex_pattern_set(
        Name='SQLInjectionPatterns',
        Scope='REGIONAL',
        Description='Regex patterns for SQL injection detection',
        RegularExpressionList=[
            {'RegexString': r'(\%27)|(\')|(\-\-)|(\%23)|(#)'},
            {'RegexString': r'((\%3D)|(=))[^\n]*((\%27)|(\')|(\-\-)|(\%3B)|(;))'},
            {'RegexString': r'\w*((\%27)|(\'))((\%6F)|o|(\%4F))((\%72)|r|(\%52))'},
            {'RegexString': r'((\%27)|(\'))union'},
            {'RegexString': r'exec(\s|\+)+(s|x)p\w+'}
        ],
        Tags=[
            {
                'Key': 'Name',
                'Value': 'SQL-Injection-Patterns'
            }
        ]
    )
    
    # Create IP set for known malicious IPs
    malicious_ip_set = wafv2.create_ip_set(
        Name='MaliciousIPSet',
        Scope='REGIONAL',
        IPAddressVersion='IPV4',
        Addresses=[
            '192.0.2.0/24',
            '203.0.113.0/24',
            '198.51.100.44/32'
        ],
        Description='Known malicious IP addresses',
        Tags=[
            {
                'Key': 'Name',
                'Value': 'Malicious-IP-Set'
            }
        ]
    )
    
    # Create comprehensive Web ACL with inspection rules
    web_acl_rules = [
        {
            'Name': 'BlockMaliciousIPs',
            'Priority': 1,
            'Action': {'Block': {}},
            'Statement': {
                'IPSetReferenceStatement': {
                    'ARN': malicious_ip_set['Summary']['ARN']
                }
            },
            'VisibilityConfig': {
                'SampledRequestsEnabled': True,
                'CloudWatchMetricsEnabled': True,
                'MetricName': 'BlockMaliciousIPs'
            }
        },
        {
            'Name': 'SQLInjectionProtection',
            'Priority': 2,
            'Action': {'Block': {}},
            'Statement': {
                'OrStatement': {
                    'Statements': [
                        {
                            'RegexPatternSetReferenceStatement': {
                                'ARN': sql_injection_patterns['Summary']['ARN'],
                                'FieldToMatch': {
                                    'Body': {}
                                },
                                'TextTransformations': [
                                    {
                                        'Priority': 1,
                                        'Type': 'URL_DECODE'
                                    },
                                    {
                                        'Priority': 2,
                                        'Type': 'HTML_ENTITY_DECODE'
                                    }
                                ]
                            }
                        },
                        {
                            'RegexPatternSetReferenceStatement': {
                                'ARN': sql_injection_patterns['Summary']['ARN'],
                                'FieldToMatch': {
                                    'UriPath': {}
                                },
                                'TextTransformations': [
                                    {
                                        'Priority': 1,
                                        'Type': 'URL_DECODE'
                                    }
                                ]
                            }
                        }
                    ]
                }
            },
            'VisibilityConfig': {
                'SampledRequestsEnabled': True,
                'CloudWatchMetricsEnabled': True,
                'MetricName': 'SQLInjectionProtection'
            }
        },
        {
            'Name': 'AWSManagedRulesCommonRuleSet',
            'Priority': 3,
            'OverrideAction': {'None': {}},
            'Statement': {
                'ManagedRuleGroupStatement': {
                    'VendorName': 'AWS',
                    'Name': 'AWSManagedRulesCommonRuleSet',
                    'ExcludedRules': []
                }
            },
            'VisibilityConfig': {
                'SampledRequestsEnabled': True,
                'CloudWatchMetricsEnabled': True,
                'MetricName': 'CommonRuleSet'
            }
        },
        {
            'Name': 'AWSManagedRulesKnownBadInputsRuleSet',
            'Priority': 4,
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
                'MetricName': 'KnownBadInputs'
            }
        },
        {
            'Name': 'RateLimitingRule',
            'Priority': 5,
            'Action': {'Block': {}},
            'Statement': {
                'RateBasedStatement': {
                    'Limit': 2000,
                    'AggregateKeyType': 'IP',
                    'ScopeDownStatement': {
                        'NotStatement': {
                            'Statement': {
                                'ByteMatchStatement': {
                                    'SearchString': 'healthcheck',
                                    'FieldToMatch': {
                                        'UriPath': {}
                                    },
                                    'TextTransformations': [
                                        {
                                            'Priority': 1,
                                            'Type': 'LOWERCASE'
                                        }
                                    ],
                                    'PositionalConstraint': 'CONTAINS'
                                }
                            }
                        }
                    }
                }
            },
            'VisibilityConfig': {
                'SampledRequestsEnabled': True,
                'CloudWatchMetricsEnabled': True,
                'MetricName': 'RateLimiting'
            }
        }
    ]
    
    try:
        web_acl_response = wafv2.create_web_acl(
            Name='AdvancedInspectionWebACL',
            Scope='REGIONAL',
            DefaultAction={'Allow': {}},
            Rules=web_acl_rules,
            Description='Advanced WAF with comprehensive inspection capabilities',
            Tags=[
                {
                    'Key': 'Name',
                    'Value': 'Advanced-Inspection-WebACL'
                }
            ],
            VisibilityConfig={
                'SampledRequestsEnabled': True,
                'CloudWatchMetricsEnabled': True,
                'MetricName': 'AdvancedInspectionWebACL'
            }
        )
        
        return web_acl_response['Summary']['ARN']
        
    except Exception as e:
        print(f"Error creating advanced WAF configuration: {str(e)}")
        return None

### Example 3: VPC Traffic Mirroring for inspection

```bash
# Create traffic mirror target (Network Load Balancer for inspection appliances)
aws ec2 create-traffic-mirror-target \
  --network-load-balancer-arn arn:aws:elasticloadbalancing:us-west-2:123456789012:loadbalancer/net/inspection-nlb/1234567890123456 \
  --description "Traffic mirror target for security inspection" \
  --tag-specifications 'ResourceType=traffic-mirror-target,Tags=[{Key=Name,Value=Inspection-Mirror-Target}]'

# Create traffic mirror filter for specific traffic types
aws ec2 create-traffic-mirror-filter \
  --description "Filter for mirroring suspicious traffic" \
  --tag-specifications 'ResourceType=traffic-mirror-filter,Tags=[{Key=Name,Value=Suspicious-Traffic-Filter}]'

# Add ingress rule to mirror HTTP/HTTPS traffic
aws ec2 create-traffic-mirror-filter-rule \
  --traffic-mirror-filter-id tmf-12345678 \
  --traffic-direction ingress \
  --rule-number 100 \
  --rule-action accept \
  --protocol 6 \
  --destination-port-range FromPort=80,ToPort=80 \
  --source-cidr-block 0.0.0.0/0 \
  --destination-cidr-block 10.0.0.0/8 \
  --description "Mirror HTTP traffic"

aws ec2 create-traffic-mirror-filter-rule \
  --traffic-mirror-filter-id tmf-12345678 \
  --traffic-direction ingress \
  --rule-number 110 \
  --rule-action accept \
  --protocol 6 \
  --destination-port-range FromPort=443,ToPort=443 \
  --source-cidr-block 0.0.0.0/0 \
  --destination-cidr-block 10.0.0.0/8 \
  --description "Mirror HTTPS traffic"

# Add egress rule to mirror outbound traffic to suspicious destinations
aws ec2 create-traffic-mirror-filter-rule \
  --traffic-mirror-filter-id tmf-12345678 \
  --traffic-direction egress \
  --rule-number 200 \
  --rule-action accept \
  --protocol 6 \
  --source-cidr-block 10.0.0.0/8 \
  --destination-cidr-block 192.0.2.0/24 \
  --description "Mirror traffic to suspicious IPs"

# Create traffic mirror session for specific instances
aws ec2 create-traffic-mirror-session \
  --network-interface-id eni-12345678 \
  --traffic-mirror-target-id tmt-12345678 \
  --traffic-mirror-filter-id tmf-12345678 \
  --session-number 1 \
  --description "Mirror session for web server inspection" \
  --tag-specifications 'ResourceType=traffic-mirror-session,Tags=[{Key=Name,Value=WebServer-Mirror-Session}]'
```

### Example 4: GuardDuty malware detection integration

```python
import boto3
import json
from datetime import datetime

def setup_guardduty_malware_protection():
    """Configure GuardDuty with malware protection for comprehensive inspection"""
    
    guardduty = boto3.client('guardduty')
    s3 = boto3.client('s3')
    
    # Get GuardDuty detector ID
    detectors = guardduty.list_detectors()
    if not detectors['DetectorIds']:
        # Create GuardDuty detector if none exists
        detector_response = guardduty.create_detector(
            Enable=True,
            FindingPublishingFrequency='FIFTEEN_MINUTES',
            DataSources={
                'S3Logs': {
                    'Enable': True
                },
                'Kubernetes': {
                    'AuditLogs': {
                        'Enable': True
                    }
                },
                'MalwareProtection': {
                    'ScanEc2InstanceWithFindings': {
                        'EbsVolumes': True
                    }
                }
            },
            Tags={
                'Name': 'Main-GuardDuty-Detector',
                'Purpose': 'Malware-Detection'
            }
        )
        detector_id = detector_response['DetectorId']
    else:
        detector_id = detectors['DetectorIds'][0]
    
    # Configure malware protection
    try:
        guardduty.update_malware_protection_plan(
            DetectorId=detector_id,
            Role='arn:aws:iam::123456789012:role/GuardDutyMalwareProtectionRole',
            Actions={
                'Tagging': {
                    'Status': 'ENABLED'
                }
            }
        )
        print(f"Configured malware protection for detector: {detector_id}")
    except Exception as e:
        print(f"Error configuring malware protection: {str(e)}")
    
    # Create custom threat intelligence set
    threat_intel_bucket = 'my-threat-intelligence-bucket'
    threat_intel_key = 'malware-indicators.txt'
    
    # Create threat intelligence file content
    threat_indicators = [
        '192.0.2.100',  # Known malware C&C server
        '203.0.113.50', # Phishing server
        'malware.example.com',  # Malicious domain
        'botnet.example.org'    # Botnet domain
    ]
    
    try:
        # Upload threat intelligence to S3
        s3.put_object(
            Bucket=threat_intel_bucket,
            Key=threat_intel_key,
            Body='\n'.join(threat_indicators),
            ContentType='text/plain'
        )
        
        # Create threat intelligence set in GuardDuty
        threat_intel_response = guardduty.create_threat_intel_set(
            DetectorId=detector_id,
            Name='CustomMalwareIndicators',
            Format='TXT',
            Location=f'https://s3.amazonaws.com/{threat_intel_bucket}/{threat_intel_key}',
            Activate=True,
            Tags={
                'Name': 'Custom-Malware-Indicators',
                'Type': 'ThreatIntelligence'
            }
        )
        
        print(f"Created threat intelligence set: {threat_intel_response['ThreatIntelSetId']}")
        
    except Exception as e:
        print(f"Error creating threat intelligence set: {str(e)}")
    
    return detector_id

def setup_guardduty_event_processing():
    """Set up EventBridge rules for GuardDuty findings processing"""
    
    events = boto3.client('events')
    
    # Create EventBridge rule for high severity GuardDuty findings
    rule_response = events.put_rule(
        Name='GuardDutyHighSeverityFindings',
        EventPattern=json.dumps({
            "source": ["aws.guardduty"],
            "detail-type": ["GuardDuty Finding"],
            "detail": {
                "severity": [
                    {"numeric": [">=", 7.0]}
                ],
                "type": [
                    {"prefix": "Trojan"},
                    {"prefix": "Backdoor"},
                    {"prefix": "Cryptocurrency"}
                ]
            }
        }),
        State='ENABLED',
        Description='Capture high severity GuardDuty malware findings'
    )
    
    # Add Lambda target for automated response
    events.put_targets(
        Rule='GuardDutyHighSeverityFindings',
        Targets=[
            {
                'Id': '1',
                'Arn': 'arn:aws:lambda:us-west-2:123456789012:function:GuardDutyResponseFunction',
                'InputTransformer': {
                    'InputPathsMap': {
                        'severity': '$.detail.severity',
                        'type': '$.detail.type',
                        'instanceId': '$.detail.resource.instanceDetails.instanceId',
                        'findingId': '$.detail.id'
                    },
                    'InputTemplate': '{"severity": "<severity>", "type": "<type>", "instanceId": "<instanceId>", "findingId": "<findingId>"}'
                }
            }
        ]
    )
    
    print("Configured GuardDuty event processing")

# Example usage
if __name__ == "__main__":
    detector_id = setup_guardduty_malware_protection()
    setup_guardduty_event_processing()
```

## AWS services to consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Network Firewall</h4>
    <p>A managed service that makes it easy to deploy essential network protections for all of your Amazon VPCs. Provides deep packet inspection with stateful and stateless rule processing.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS WAF (Web Application Firewall)</h4>
    <p>Helps protect your web applications or APIs against common web exploits and bots. Provides application-layer inspection with customizable rules and managed rule sets.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon GuardDuty</h4>
    <p>Provides intelligent threat detection for your AWS accounts and workloads. Uses machine learning and threat intelligence to identify malicious activity and malware.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon Inspector</h4>
    <p>Automatically assesses applications for exposure, vulnerabilities, and deviations from best practices. Provides continuous vulnerability assessment and malware detection.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>VPC Traffic Mirroring</h4>
    <p>Enables you to copy network traffic from an elastic network interface and send it to security and monitoring appliances for deep packet inspection.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Security Hub</h4>
    <p>Provides a comprehensive view of your security state in AWS. Centralizes findings from inspection-based security services for unified analysis and response.</p>
  </div>
</div>

## Benefits of implementing inspection-based protection

- **Advanced threat detection**: Identifies sophisticated attacks that bypass traditional security controls
- **Real-time protection**: Provides immediate response to detected threats and malicious activities
- **Comprehensive coverage**: Inspects traffic at multiple layers for complete protection
- **Behavioral analysis**: Detects zero-day threats and unknown attack patterns
- **Compliance support**: Helps meet regulatory requirements for traffic inspection and monitoring
- **Reduced false positives**: Advanced inspection techniques provide more accurate threat detection
- **Automated response**: Enables immediate action against detected threats without manual intervention

## Related resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/sec_network_protection_inspection.html">AWS Well-Architected Framework - Implement inspection-based protection</a></li>
    <li><a href="https://docs.aws.amazon.com/network-firewall/latest/developerguide/what-is-aws-network-firewall.html">AWS Network Firewall Developer Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html">AWS WAF Developer Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/guardduty/latest/ug/what-is-guardduty.html">Amazon GuardDuty User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/vpc/latest/mirroring/what-is-traffic-mirroring.html">VPC Traffic Mirroring Guide</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-deploy-aws-network-firewall-by-using-aws-firewall-manager/">How to deploy AWS Network Firewall by using AWS Firewall Manager</a></li>
  </ul>
</div>
