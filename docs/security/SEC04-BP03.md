---
title: SEC04-BP03 - Correlate and enrich security alerts
layout: default
parent: SEC04 - How do you detect and investigate security events?
grand_parent: Security
nav_order: 3
---

<div class="pillar-header">
  <h1>SEC04-BP03: Correlate and enrich security alerts</h1>
  <p>Correlate security alerts and findings to identify patterns and reduce noise. Enrich security alerts with contextual information to help security teams prioritize and respond to incidents more effectively. For example, correlate multiple failed login attempts from the same IP address, or enrich alerts with information about the affected user or resource.</p>
</div>

## Implementation guidance

Security alert correlation and enrichment transforms raw security events into actionable intelligence. By combining related alerts and adding contextual information, security teams can better understand the scope and severity of potential threats, reduce false positives, and respond more effectively to genuine security incidents.

### Key steps for implementing this best practice:

1. **Implement alert correlation mechanisms**:
   - Define correlation rules based on common attack patterns
   - Group related alerts by time, source, destination, or attack type
   - Implement statistical correlation to identify anomalies
   - Use machine learning for advanced pattern recognition
   - Create correlation rules for multi-stage attacks

2. **Enrich alerts with contextual information**:
   - Add asset information (criticality, owner, location)
   - Include user context (role, department, access patterns)
   - Append threat intelligence data
   - Add network topology and segmentation information
   - Include compliance and regulatory context

3. **Implement automated alert prioritization**:
   - Define severity scoring based on multiple factors
   - Consider asset criticality in prioritization
   - Factor in user privilege levels
   - Include threat intelligence reputation scores
   - Implement dynamic scoring based on current threat landscape

4. **Create correlation timelines**:
   - Build chronological views of related events
   - Implement attack chain reconstruction
   - Show progression of security events
   - Include pre and post-incident context
   - Visualize attack patterns and techniques

5. **Implement noise reduction techniques**:
   - Filter out known false positives
   - Implement alert suppression for maintenance windows
   - Use whitelisting for approved activities
   - Implement adaptive thresholds based on baselines
   - Create exception handling for legitimate business activities

6. **Enable collaborative investigation**:
   - Implement case management for correlated alerts
   - Enable annotation and collaboration features
   - Create investigation workflows and playbooks
   - Implement knowledge sharing mechanisms
   - Track investigation progress and outcomes

## Implementation examples

### Example 1: Alert correlation using Amazon EventBridge and Lambda

```python
import json
import boto3
from datetime import datetime, timedelta
from collections import defaultdict

class SecurityAlertCorrelator:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.securityhub = boto3.client('securityhub')
        self.events_table = self.dynamodb.Table('SecurityEvents')
        self.correlations_table = self.dynamodb.Table('AlertCorrelations')
    
    def lambda_handler(self, event, context):
        """Main Lambda handler for alert correlation"""
        
        try:
            # Parse incoming security alert
            alert = self.parse_security_alert(event)
            
            # Store the alert
            self.store_alert(alert)
            
            # Find correlations
            correlations = self.find_correlations(alert)
            
            # Enrich the alert
            enriched_alert = self.enrich_alert(alert)
            
            # Create correlated incident if threshold met
            if len(correlations) >= 3:  # Configurable threshold
                incident = self.create_correlated_incident(alert, correlations)
                self.send_to_security_hub(incident)
            
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'alert_id': alert['id'],
                    'correlations_found': len(correlations),
                    'enrichment_applied': True
                })
            }
            
        except Exception as e:
            print(f"Error processing alert: {str(e)}")
            return {
                'statusCode': 500,
                'body': json.dumps(f'Error: {str(e)}')
            }
    
    def parse_security_alert(self, event):
        """Parse incoming security alert from various sources"""
        
        # Handle different event sources
        if 'source' in event and event['source'] == 'aws.guardduty':
            return self.parse_guardduty_alert(event)
        elif 'source' in event and event['source'] == 'aws.securityhub':
            return self.parse_securityhub_alert(event)
        else:
            return self.parse_generic_alert(event)
    
    def parse_guardduty_alert(self, event):
        """Parse GuardDuty finding"""
        
        detail = event.get('detail', {})
        
        return {
            'id': detail.get('id'),
            'timestamp': event.get('time'),
            'source': 'guardduty',
            'type': detail.get('type'),
            'severity': detail.get('severity'),
            'source_ip': detail.get('service', {}).get('remoteIpDetails', {}).get('ipAddressV4'),
            'target_resource': detail.get('resource', {}).get('instanceDetails', {}).get('instanceId'),
            'user_name': detail.get('resource', {}).get('accessKeyDetails', {}).get('userName'),
            'raw_event': event
        }
    
    def find_correlations(self, alert):
        """Find related alerts for correlation"""
        
        correlations = []
        
        # Time-based correlation (last 1 hour)
        time_threshold = datetime.utcnow() - timedelta(hours=1)
        
        # Query for related events
        correlation_queries = [
            # Same source IP
            {
                'filter_expression': 'source_ip = :ip AND event_time > :time',
                'expression_values': {
                    ':ip': alert.get('source_ip'),
                    ':time': time_threshold.isoformat()
                }
            },
            # Same target resource
            {
                'filter_expression': 'target_resource = :resource AND event_time > :time',
                'expression_values': {
                    ':resource': alert.get('target_resource'),
                    ':time': time_threshold.isoformat()
                }
            },
            # Same user
            {
                'filter_expression': 'user_name = :user AND event_time > :time',
                'expression_values': {
                    ':user': alert.get('user_name'),
                    ':time': time_threshold.isoformat()
                }
            }
        ]
        
        for query in correlation_queries:
            if any(query['expression_values'].values()):  # Only query if we have values
                try:
                    response = self.events_table.scan(
                        FilterExpression=query['filter_expression'],
                        ExpressionAttributeValues=query['expression_values']
                    )
                    correlations.extend(response.get('Items', []))
                except Exception as e:
                    print(f"Error querying correlations: {str(e)}")
        
        return correlations
    
    def enrich_alert(self, alert):
        """Enrich alert with contextual information"""
        
        enriched_alert = alert.copy()
        
        # Enrich with asset information
        if alert.get('target_resource'):
            asset_info = self.get_asset_information(alert['target_resource'])
            enriched_alert['asset_info'] = asset_info
        
        # Enrich with user information
        if alert.get('user_name'):
            user_info = self.get_user_information(alert['user_name'])
            enriched_alert['user_info'] = user_info
        
        # Enrich with threat intelligence
        if alert.get('source_ip'):
            threat_intel = self.get_threat_intelligence(alert['source_ip'])
            enriched_alert['threat_intel'] = threat_intel
        
        # Calculate risk score
        enriched_alert['risk_score'] = self.calculate_risk_score(enriched_alert)
        
        return enriched_alert
    
    def get_asset_information(self, resource_id):
        """Get asset information from CMDB or AWS APIs"""
        
        try:
            # Example: Get EC2 instance information
            if resource_id.startswith('i-'):
                ec2 = boto3.client('ec2')
                response = ec2.describe_instances(InstanceIds=[resource_id])
                
                if response['Reservations']:
                    instance = response['Reservations'][0]['Instances'][0]
                    return {
                        'instance_type': instance.get('InstanceType'),
                        'vpc_id': instance.get('VpcId'),
                        'subnet_id': instance.get('SubnetId'),
                        'security_groups': [sg['GroupId'] for sg in instance.get('SecurityGroups', [])],
                        'tags': {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])},
                        'criticality': self.determine_asset_criticality(instance.get('Tags', []))
                    }
        except Exception as e:
            print(f"Error getting asset information: {str(e)}")
        
        return {}
    
    def get_user_information(self, username):
        """Get user information from IAM or directory service"""
        
        try:
            iam = boto3.client('iam')
            
            # Get user details
            user_response = iam.get_user(UserName=username)
            user = user_response['User']
            
            # Get user groups
            groups_response = iam.get_groups_for_user(UserName=username)
            groups = [group['GroupName'] for group in groups_response['Groups']]
            
            # Get attached policies
            policies_response = iam.list_attached_user_policies(UserName=username)
            policies = [policy['PolicyName'] for policy in policies_response['AttachedPolicies']]
            
            return {
                'user_id': user.get('UserId'),
                'create_date': user.get('CreateDate').isoformat() if user.get('CreateDate') else None,
                'groups': groups,
                'policies': policies,
                'privilege_level': self.determine_privilege_level(groups, policies)
            }
            
        except Exception as e:
            print(f"Error getting user information: {str(e)}")
        
        return {}
    
    def get_threat_intelligence(self, ip_address):
        """Get threat intelligence for IP address"""
        
        # Example implementation - in practice, integrate with threat intel feeds
        known_malicious_ranges = [
            '10.0.0.0/8',    # Example ranges
            '192.168.0.0/16',
            '172.16.0.0/12'
        ]
        
        threat_info = {
            'reputation_score': 0,
            'categories': [],
            'last_seen': None,
            'confidence': 'low'
        }
        
        # Simple reputation scoring (replace with actual threat intel API)
        if any(self.ip_in_range(ip_address, cidr) for cidr in known_malicious_ranges):
            threat_info['reputation_score'] = 8
            threat_info['categories'] = ['malware', 'botnet']
            threat_info['confidence'] = 'high'
        
        return threat_info
    
    def calculate_risk_score(self, alert):
        """Calculate risk score based on multiple factors"""
        
        base_score = alert.get('severity', 5)  # Base severity from original alert
        
        # Asset criticality multiplier
        asset_criticality = alert.get('asset_info', {}).get('criticality', 'medium')
        criticality_multiplier = {'low': 0.5, 'medium': 1.0, 'high': 1.5, 'critical': 2.0}
        
        # User privilege multiplier
        privilege_level = alert.get('user_info', {}).get('privilege_level', 'standard')
        privilege_multiplier = {'standard': 1.0, 'elevated': 1.3, 'admin': 1.8, 'root': 2.5}
        
        # Threat intelligence multiplier
        reputation_score = alert.get('threat_intel', {}).get('reputation_score', 0)
        threat_multiplier = 1.0 + (reputation_score / 10)
        
        # Calculate final risk score
        risk_score = (base_score * 
                     criticality_multiplier.get(asset_criticality, 1.0) * 
                     privilege_multiplier.get(privilege_level, 1.0) * 
                     threat_multiplier)
        
        return min(risk_score, 10.0)  # Cap at 10
    
    def create_correlated_incident(self, primary_alert, correlations):
        """Create a correlated security incident"""
        
        incident = {
            'incident_id': f"incident-{primary_alert['id']}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            'primary_alert': primary_alert,
            'correlated_alerts': correlations,
            'incident_type': self.determine_incident_type(primary_alert, correlations),
            'severity': self.calculate_incident_severity(primary_alert, correlations),
            'timeline': self.build_incident_timeline(primary_alert, correlations),
            'affected_assets': self.get_affected_assets(primary_alert, correlations),
            'created_at': datetime.utcnow().isoformat()
        }
        
        # Store the incident
        self.correlations_table.put_item(Item=incident)
        
        return incident
    
    def determine_incident_type(self, primary_alert, correlations):
        """Determine the type of security incident"""
        
        alert_types = [primary_alert.get('type', '')] + [c.get('type', '') for c in correlations]
        
        # Pattern matching for common attack types
        if any('brute' in t.lower() for t in alert_types):
            return 'Brute Force Attack'
        elif any('malware' in t.lower() for t in alert_types):
            return 'Malware Infection'
        elif any('exfiltration' in t.lower() for t in alert_types):
            return 'Data Exfiltration'
        elif any('privilege' in t.lower() for t in alert_types):
            return 'Privilege Escalation'
        else:
            return 'Security Incident'
    
    def send_to_security_hub(self, incident):
        """Send correlated incident to Security Hub"""
        
        finding = {
            'SchemaVersion': '2018-10-08',
            'Id': incident['incident_id'],
            'ProductArn': f"arn:aws:securityhub:us-west-2:123456789012:product/123456789012/default",
            'GeneratorId': 'security-correlator',
            'AwsAccountId': '123456789012',
            'Types': ['Effects/Data Exfiltration', 'TTPs/Defense Evasion'],
            'FirstObservedAt': incident['created_at'],
            'LastObservedAt': incident['created_at'],
            'CreatedAt': incident['created_at'],
            'UpdatedAt': incident['created_at'],
            'Severity': {
                'Label': incident['severity']
            },
            'Title': f"Correlated Security Incident: {incident['incident_type']}",
            'Description': f"Multiple related security alerts detected. Primary alert: {incident['primary_alert']['type']}. {len(incident['correlated_alerts'])} correlated events found.",
            'Resources': [
                {
                    'Type': 'Other',
                    'Id': asset,
                    'Region': 'us-west-2'
                } for asset in incident['affected_assets']
            ],
            'RecordState': 'ACTIVE',
            'WorkflowState': 'NEW'
        }
        
        try:
            self.securityhub.batch_import_findings(Findings=[finding])
            print(f"Successfully sent correlated incident to Security Hub: {incident['incident_id']}")
        except Exception as e:
            print(f"Error sending to Security Hub: {str(e)}")
    
    # Helper methods
    def store_alert(self, alert):
        """Store alert in DynamoDB for correlation"""
        alert['event_time'] = datetime.utcnow().isoformat()
        self.events_table.put_item(Item=alert)
    
    def determine_asset_criticality(self, tags):
        """Determine asset criticality from tags"""
        for tag in tags:
            if tag.get('Key', '').lower() == 'criticality':
                return tag.get('Value', 'medium').lower()
        return 'medium'
    
    def determine_privilege_level(self, groups, policies):
        """Determine user privilege level"""
        admin_indicators = ['admin', 'root', 'poweruser', 'administrator']
        
        all_items = groups + policies
        for item in all_items:
            if any(indicator in item.lower() for indicator in admin_indicators):
                return 'admin'
        
        return 'standard'
    
    def ip_in_range(self, ip, cidr):
        """Check if IP is in CIDR range"""
        import ipaddress
        try:
            return ipaddress.ip_address(ip) in ipaddress.ip_network(cidr)
        except:
            return False
    
    def build_incident_timeline(self, primary_alert, correlations):
        """Build chronological timeline of events"""
        all_events = [primary_alert] + correlations
        return sorted(all_events, key=lambda x: x.get('timestamp', ''))
    
    def get_affected_assets(self, primary_alert, correlations):
        """Get list of affected assets"""
        assets = set()
        for event in [primary_alert] + correlations:
            if event.get('target_resource'):
                assets.add(event['target_resource'])
        return list(assets)
    
    def calculate_incident_severity(self, primary_alert, correlations):
        """Calculate overall incident severity"""
        severities = [primary_alert.get('severity', 5)] + [c.get('severity', 5) for c in correlations]
        max_severity = max(severities)
        
        if max_severity >= 8:
            return 'CRITICAL'
        elif max_severity >= 6:
            return 'HIGH'
        elif max_severity >= 4:
            return 'MEDIUM'
        else:
            return 'LOW'

# Lambda handler
correlator = SecurityAlertCorrelator()

def lambda_handler(event, context):
    return correlator.lambda_handler(event, context)
```

### Example 2: EventBridge rules for alert correlation

```json
{
  "Rules": [
    {
      "Name": "GuardDutyAlertCorrelation",
      "EventPattern": {
        "source": ["aws.guardduty"],
        "detail-type": ["GuardDuty Finding"],
        "detail": {
          "severity": [
            {"numeric": [">=", 4]}
          ]
        }
      },
      "State": "ENABLED",
      "Targets": [
        {
          "Id": "1",
          "Arn": "arn:aws:lambda:us-west-2:123456789012:function:SecurityAlertCorrelator"
        }
      ]
    },
    {
      "Name": "SecurityHubAlertCorrelation",
      "EventPattern": {
        "source": ["aws.securityhub"],
        "detail-type": ["Security Hub Findings - Imported"],
        "detail": {
          "findings": {
            "Severity": {
              "Label": ["HIGH", "CRITICAL"]
            }
          }
        }
      },
      "State": "ENABLED",
      "Targets": [
        {
          "Id": "1",
          "Arn": "arn:aws:lambda:us-west-2:123456789012:function:SecurityAlertCorrelator"
        }
      ]
    }
  ]
}
```

### Example 3: CloudWatch dashboard for correlated alerts

```python
import boto3
import json

def create_correlation_dashboard():
    """Create CloudWatch dashboard for alert correlation metrics"""
    
    cloudwatch = boto3.client('cloudwatch')
    
    dashboard_body = {
        "widgets": [
            {
                "type": "metric",
                "x": 0,
                "y": 0,
                "width": 12,
                "height": 6,
                "properties": {
                    "metrics": [
                        ["Security/Correlation", "AlertsProcessed"],
                        [".", "CorrelationsFound"],
                        [".", "IncidentsCreated"]
                    ],
                    "period": 300,
                    "stat": "Sum",
                    "region": "us-west-2",
                    "title": "Alert Correlation Metrics"
                }
            },
            {
                "type": "metric",
                "x": 0,
                "y": 6,
                "width": 12,
                "height": 6,
                "properties": {
                    "metrics": [
                        ["Security/Correlation", "HighSeverityIncidents"],
                        [".", "MediumSeverityIncidents"],
                        [".", "LowSeverityIncidents"]
                    ],
                    "period": 300,
                    "stat": "Sum",
                    "region": "us-west-2",
                    "title": "Incident Severity Distribution"
                }
            },
            {
                "type": "log",
                "x": 0,
                "y": 12,
                "width": 24,
                "height": 6,
                "properties": {
                    "query": "SOURCE '/aws/lambda/SecurityAlertCorrelator'\n| fields @timestamp, @message\n| filter @message like /correlated incident/\n| sort @timestamp desc\n| limit 20",
                    "region": "us-west-2",
                    "title": "Recent Correlated Incidents",
                    "view": "table"
                }
            }
        ]
    }
    
    try:
        cloudwatch.put_dashboard(
            DashboardName='SecurityAlertCorrelation',
            DashboardBody=json.dumps(dashboard_body)
        )
        print("Successfully created correlation dashboard")
    except Exception as e:
        print(f"Error creating dashboard: {str(e)}")

# Create the dashboard
create_correlation_dashboard()
```

## AWS services to consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon EventBridge</h4>
    <p>A serverless event bus that makes it easy to connect applications together using data from your own applications, integrated Software-as-a-Service (SaaS) applications, and AWS services. Essential for routing and correlating security events.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Lambda</h4>
    <p>Lets you run code without provisioning or managing servers. Use Lambda functions to implement correlation logic and alert enrichment processing.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon DynamoDB</h4>
    <p>A key-value and document database that delivers single-digit millisecond performance at any scale. Ideal for storing security events and correlation data for fast lookups.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Security Hub</h4>
    <p>Provides a comprehensive view of your security state in AWS and helps you check your compliance with security standards and best practices. Central repository for correlated security findings.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon CloudWatch</h4>
    <p>Monitors your AWS resources and the applications you run on AWS in real time. Use CloudWatch for correlation metrics, dashboards, and alerting on correlation patterns.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon Elasticsearch Service</h4>
    <p>A fully managed service that makes it easy to deploy, secure, and run Elasticsearch cost effectively at scale. Useful for advanced correlation analysis and search capabilities.</p>
  </div>
</div>

## Benefits of correlating and enriching security alerts

- **Reduced alert fatigue**: Fewer, more meaningful alerts through correlation and noise reduction
- **Improved threat detection**: Better identification of complex, multi-stage attacks
- **Faster incident response**: Enriched context enables quicker understanding and response
- **Enhanced prioritization**: Risk-based scoring helps focus on the most critical threats
- **Better investigation efficiency**: Correlated timelines and context speed up investigations
- **Reduced false positives**: Contextual information helps distinguish real threats from benign activities
- **Improved security posture**: Better understanding of attack patterns and organizational vulnerabilities

## Related resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/sec_detect_investigate_events_security_alerts.html">AWS Well-Architected Framework - Correlate and enrich security alerts</a></li>
    <li><a href="https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-what-is.html">Amazon EventBridge User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-findings-format.html">AWS Security Finding Format (ASFF)</a></li>
    <li><a href="https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_findings.html">Amazon GuardDuty findings</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-build-a-multi-region-threat-detection-strategy-with-amazon-guardduty/">How to build a multi-Region threat detection strategy with Amazon GuardDuty</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-centralize-findings-from-aws-security-services-using-aws-security-hub-custom-insights/">How to centralize findings from AWS security services using AWS Security Hub custom insights</a></li>
  </ul>
</div>
