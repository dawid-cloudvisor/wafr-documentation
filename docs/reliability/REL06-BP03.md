---
title: REL06-BP03 - Send notifications (Real-time processing and alarming)
layout: default
parent: REL06 - How do you monitor workload resources?
grand_parent: Reliability
nav_order: 3
---

# REL06-BP03: Send notifications (Real-time processing and alarming)

## Overview

Implement intelligent notification systems that provide real-time alerts for critical events while minimizing alert fatigue through smart filtering, routing, and escalation mechanisms. Effective notifications ensure the right people receive the right information at the right time to enable rapid response to issues.

## Implementation Steps

### 1. Design Alert Prioritization and Classification
- Classify alerts by severity levels (critical, high, medium, low)
- Implement business impact-based alert prioritization
- Design alert categories for different types of issues
- Establish alert ownership and responsibility mapping

### 2. Configure Intelligent Alert Routing
- Implement role-based alert routing and escalation
- Configure time-based routing for different shifts and time zones
- Design context-aware routing based on alert content
- Establish backup notification channels for critical alerts

### 3. Implement Alert Aggregation and Deduplication
- Configure alert grouping to reduce notification volume
- Implement intelligent deduplication to prevent spam
- Design alert correlation to identify related issues
- Establish alert suppression during maintenance windows

### 4. Configure Multi-Channel Notification Delivery
- Implement email, SMS, and push notification channels
- Configure integration with collaboration tools (Slack, Teams)
- Design voice call escalation for critical alerts
- Establish mobile app notifications for on-call personnel

### 5. Establish Alert Lifecycle Management
- Implement alert acknowledgment and assignment workflows
- Configure automatic alert resolution and closure
- Design alert escalation timers and procedures
- Establish alert history and audit trails

### 6. Optimize Alert Quality and Reduce Fatigue
- Monitor alert frequency and response patterns
- Implement alert tuning and threshold optimization
- Design alert feedback loops for continuous improvement
- Establish alert effectiveness metrics and reporting

## Implementation Examples

### Example 1: Intelligent Alert Management System
```python
import boto3
import json
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import asyncio
import hashlib

class AlertSeverity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

class AlertStatus(Enum):
    OPEN = "open"
    ACKNOWLEDGED = "acknowledged"
    ASSIGNED = "assigned"
    RESOLVED = "resolved"
    CLOSED = "closed"

class NotificationChannel(Enum):
    EMAIL = "email"
    SMS = "sms"
    SLACK = "slack"
    TEAMS = "teams"
    WEBHOOK = "webhook"
    VOICE = "voice"

@dataclass
class Alert:
    alert_id: str
    title: str
    description: str
    severity: AlertSeverity
    status: AlertStatus
    source: str
    metric_name: str
    current_value: float
    threshold_value: float
    dimensions: Dict[str, str]
    created_at: datetime
    updated_at: datetime
    assigned_to: Optional[str] = None
    acknowledged_by: Optional[str] = None
    resolved_by: Optional[str] = None

@dataclass
class NotificationRule:
    rule_id: str
    name: str
    conditions: Dict[str, Any]
    channels: List[NotificationChannel]
    recipients: List[str]
    escalation_delay_minutes: int
    enabled: bool

class IntelligentAlertManager:
    """Intelligent alert management and notification system"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
        # AWS clients
        self.sns = boto3.client('sns')
        self.ses = boto3.client('ses')
        self.dynamodb = boto3.resource('dynamodb')
        self.lambda_client = boto3.client('lambda')
        self.ssm = boto3.client('ssm')
        
        # Storage
        self.alerts_table = self.dynamodb.Table(config.get('alerts_table', 'alerts'))
        self.rules_table = self.dynamodb.Table(config.get('rules_table', 'notification-rules'))
        
        # Notification rules
        self.notification_rules = {}
        self.load_notification_rules()
        
        # Alert deduplication
        self.alert_fingerprints = {}
        self.dedup_window_minutes = config.get('dedup_window_minutes', 5)
        
        # Escalation tracking
        self.escalation_timers = {}
        
    def load_notification_rules(self):
        """Load notification rules from storage"""
        try:
            response = self.rules_table.scan()
            
            for item in response['Items']:
                rule = NotificationRule(**item)
                self.notification_rules[rule.rule_id] = rule
            
            logging.info(f"Loaded {len(self.notification_rules)} notification rules")
            
        except Exception as e:
            logging.error(f"Failed to load notification rules: {str(e)}")
    
    async def process_alert(self, alert_data: Dict[str, Any]) -> str:
        """Process incoming alert and trigger notifications"""
        try:
            # Create alert object
            alert = Alert(
                alert_id=alert_data.get('alert_id', self._generate_alert_id(alert_data)),
                title=alert_data['title'],
                description=alert_data['description'],
                severity=AlertSeverity(alert_data['severity']),
                status=AlertStatus.OPEN,
                source=alert_data['source'],
                metric_name=alert_data.get('metric_name', ''),
                current_value=alert_data.get('current_value', 0.0),
                threshold_value=alert_data.get('threshold_value', 0.0),
                dimensions=alert_data.get('dimensions', {}),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            # Check for duplicate alerts
            if await self._is_duplicate_alert(alert):
                logging.info(f"Duplicate alert detected, skipping: {alert.alert_id}")
                return alert.alert_id
            
            # Store alert
            await self._store_alert(alert)
            
            # Find matching notification rules
            matching_rules = self._find_matching_rules(alert)
            
            # Send notifications
            for rule in matching_rules:
                await self._send_notifications(alert, rule)
            
            # Schedule escalation if needed
            await self._schedule_escalation(alert, matching_rules)
            
            logging.info(f"Processed alert: {alert.alert_id} with {len(matching_rules)} notification rules")
            return alert.alert_id
            
        except Exception as e:
            logging.error(f"Failed to process alert: {str(e)}")
            raise
    
    def _generate_alert_id(self, alert_data: Dict[str, Any]) -> str:
        """Generate unique alert ID"""
        content = f"{alert_data['source']}_{alert_data['title']}_{int(time.time())}"
        return hashlib.md5(content.encode()).hexdigest()[:16]
    
    async def _is_duplicate_alert(self, alert: Alert) -> bool:
        """Check if alert is a duplicate within the deduplication window"""
        # Create fingerprint for deduplication
        fingerprint_content = f"{alert.source}_{alert.metric_name}_{alert.title}"
        fingerprint = hashlib.md5(fingerprint_content.encode()).hexdigest()
        
        current_time = datetime.utcnow()
        
        # Check if we've seen this fingerprint recently
        if fingerprint in self.alert_fingerprints:
            last_seen = self.alert_fingerprints[fingerprint]
            if (current_time - last_seen).total_seconds() < (self.dedup_window_minutes * 60):
                return True
        
        # Update fingerprint timestamp
        self.alert_fingerprints[fingerprint] = current_time
        return False
    
    async def _store_alert(self, alert: Alert):
        """Store alert in DynamoDB"""
        try:
            # Convert datetime objects to ISO strings for DynamoDB
            alert_dict = asdict(alert)
            alert_dict['created_at'] = alert.created_at.isoformat()
            alert_dict['updated_at'] = alert.updated_at.isoformat()
            alert_dict['severity'] = alert.severity.value
            alert_dict['status'] = alert.status.value
            
            self.alerts_table.put_item(Item=alert_dict)
            
        except Exception as e:
            logging.error(f"Failed to store alert: {str(e)}")
            raise
    
    def _find_matching_rules(self, alert: Alert) -> List[NotificationRule]:
        """Find notification rules that match the alert"""
        matching_rules = []
        
        for rule in self.notification_rules.values():
            if not rule.enabled:
                continue
            
            if self._rule_matches_alert(rule, alert):
                matching_rules.append(rule)
        
        return matching_rules
    
    def _rule_matches_alert(self, rule: NotificationRule, alert: Alert) -> bool:
        """Check if a notification rule matches an alert"""
        conditions = rule.conditions
        
        # Check severity condition
        if 'severity' in conditions:
            required_severities = conditions['severity']
            if isinstance(required_severities, str):
                required_severities = [required_severities]
            
            if alert.severity.value not in required_severities:
                return False
        
        # Check source condition
        if 'source' in conditions:
            required_sources = conditions['source']
            if isinstance(required_sources, str):
                required_sources = [required_sources]
            
            if alert.source not in required_sources:
                return False
        
        # Check metric condition
        if 'metric_name' in conditions:
            required_metrics = conditions['metric_name']
            if isinstance(required_metrics, str):
                required_metrics = [required_metrics]
            
            if alert.metric_name not in required_metrics:
                return False
        
        # Check dimension conditions
        if 'dimensions' in conditions:
            required_dimensions = conditions['dimensions']
            for key, value in required_dimensions.items():
                if key not in alert.dimensions or alert.dimensions[key] != value:
                    return False
        
        return True
    
    async def _send_notifications(self, alert: Alert, rule: NotificationRule):
        """Send notifications through configured channels"""
        try:
            notification_tasks = []
            
            for channel in rule.channels:
                for recipient in rule.recipients:
                    task = asyncio.create_task(
                        self._send_notification(alert, channel, recipient)
                    )
                    notification_tasks.append(task)
            
            # Send all notifications concurrently
            await asyncio.gather(*notification_tasks, return_exceptions=True)
            
        except Exception as e:
            logging.error(f"Failed to send notifications: {str(e)}")
    
    async def _send_notification(self, alert: Alert, channel: NotificationChannel, recipient: str):
        """Send notification through specific channel"""
        try:
            if channel == NotificationChannel.EMAIL:
                await self._send_email_notification(alert, recipient)
            elif channel == NotificationChannel.SMS:
                await self._send_sms_notification(alert, recipient)
            elif channel == NotificationChannel.SLACK:
                await self._send_slack_notification(alert, recipient)
            elif channel == NotificationChannel.WEBHOOK:
                await self._send_webhook_notification(alert, recipient)
            
            logging.info(f"Sent {channel.value} notification to {recipient} for alert {alert.alert_id}")
            
        except Exception as e:
            logging.error(f"Failed to send {channel.value} notification: {str(e)}")
    
    async def _send_email_notification(self, alert: Alert, recipient: str):
        """Send email notification"""
        try:
            subject = f"[{alert.severity.value.upper()}] {alert.title}"
            
            body = f"""
Alert Details:
- Alert ID: {alert.alert_id}
- Severity: {alert.severity.value.upper()}
- Source: {alert.source}
- Description: {alert.description}
- Current Value: {alert.current_value}
- Threshold: {alert.threshold_value}
- Created: {alert.created_at.isoformat()}

Dimensions:
{json.dumps(alert.dimensions, indent=2)}

Please investigate and take appropriate action.
            """
            
            self.ses.send_email(
                Source=self.config.get('sender_email', 'alerts@example.com'),
                Destination={'ToAddresses': [recipient]},
                Message={
                    'Subject': {'Data': subject},
                    'Body': {'Text': {'Data': body}}
                }
            )
            
        except Exception as e:
            logging.error(f"Failed to send email notification: {str(e)}")
    
    async def _send_sms_notification(self, alert: Alert, recipient: str):
        """Send SMS notification"""
        try:
            message = f"[{alert.severity.value.upper()}] {alert.title}\n"
            message += f"Source: {alert.source}\n"
            message += f"Value: {alert.current_value} (threshold: {alert.threshold_value})\n"
            message += f"Alert ID: {alert.alert_id}"
            
            self.sns.publish(
                PhoneNumber=recipient,
                Message=message
            )
            
        except Exception as e:
            logging.error(f"Failed to send SMS notification: {str(e)}")
    
    async def _send_slack_notification(self, alert: Alert, webhook_url: str):
        """Send Slack notification"""
        try:
            import aiohttp
            
            # Determine color based on severity
            color_map = {
                AlertSeverity.CRITICAL: "#FF0000",
                AlertSeverity.HIGH: "#FF8C00",
                AlertSeverity.MEDIUM: "#FFD700",
                AlertSeverity.LOW: "#32CD32",
                AlertSeverity.INFO: "#87CEEB"
            }
            
            payload = {
                "attachments": [
                    {
                        "color": color_map.get(alert.severity, "#808080"),
                        "title": f"[{alert.severity.value.upper()}] {alert.title}",
                        "fields": [
                            {"title": "Source", "value": alert.source, "short": True},
                            {"title": "Alert ID", "value": alert.alert_id, "short": True},
                            {"title": "Current Value", "value": str(alert.current_value), "short": True},
                            {"title": "Threshold", "value": str(alert.threshold_value), "short": True},
                            {"title": "Description", "value": alert.description, "short": False}
                        ],
                        "timestamp": int(alert.created_at.timestamp())
                    }
                ]
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(webhook_url, json=payload) as response:
                    if response.status != 200:
                        raise Exception(f"Slack API returned status {response.status}")
            
        except Exception as e:
            logging.error(f"Failed to send Slack notification: {str(e)}")
    
    async def _schedule_escalation(self, alert: Alert, rules: List[NotificationRule]):
        """Schedule alert escalation"""
        try:
            # Find the shortest escalation delay
            min_escalation_delay = min(
                (rule.escalation_delay_minutes for rule in rules if rule.escalation_delay_minutes > 0),
                default=0
            )
            
            if min_escalation_delay > 0:
                escalation_time = datetime.utcnow() + timedelta(minutes=min_escalation_delay)
                self.escalation_timers[alert.alert_id] = escalation_time
                
                # In a real implementation, you would schedule this with a job scheduler
                logging.info(f"Scheduled escalation for alert {alert.alert_id} at {escalation_time}")
            
        except Exception as e:
            logging.error(f"Failed to schedule escalation: {str(e)}")
    
    async def acknowledge_alert(self, alert_id: str, acknowledged_by: str) -> bool:
        """Acknowledge an alert"""
        try:
            # Update alert status
            self.alerts_table.update_item(
                Key={'alert_id': alert_id},
                UpdateExpression='SET #status = :status, acknowledged_by = :ack_by, updated_at = :updated',
                ExpressionAttributeNames={'#status': 'status'},
                ExpressionAttributeValues={
                    ':status': AlertStatus.ACKNOWLEDGED.value,
                    ':ack_by': acknowledged_by,
                    ':updated': datetime.utcnow().isoformat()
                }
            )
            
            # Cancel escalation
            if alert_id in self.escalation_timers:
                del self.escalation_timers[alert_id]
            
            logging.info(f"Alert {alert_id} acknowledged by {acknowledged_by}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to acknowledge alert {alert_id}: {str(e)}")
            return False
    
    async def resolve_alert(self, alert_id: str, resolved_by: str, resolution_notes: str = "") -> bool:
        """Resolve an alert"""
        try:
            # Update alert status
            self.alerts_table.update_item(
                Key={'alert_id': alert_id},
                UpdateExpression='SET #status = :status, resolved_by = :res_by, resolution_notes = :notes, updated_at = :updated',
                ExpressionAttributeNames={'#status': 'status'},
                ExpressionAttributeValues={
                    ':status': AlertStatus.RESOLVED.value,
                    ':res_by': resolved_by,
                    ':notes': resolution_notes,
                    ':updated': datetime.utcnow().isoformat()
                }
            )
            
            # Cancel escalation
            if alert_id in self.escalation_timers:
                del self.escalation_timers[alert_id]
            
            logging.info(f"Alert {alert_id} resolved by {resolved_by}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to resolve alert {alert_id}: {str(e)}")
            return False

# Usage example
async def main():
    config = {
        'alerts_table': 'alerts',
        'rules_table': 'notification-rules',
        'sender_email': 'alerts@example.com',
        'dedup_window_minutes': 5
    }
    
    # Initialize alert manager
    alert_manager = IntelligentAlertManager(config)
    
    # Create notification rule
    critical_rule = NotificationRule(
        rule_id='critical_alerts',
        name='Critical Alerts Rule',
        conditions={
            'severity': ['critical', 'high'],
            'source': ['cloudwatch', 'application']
        },
        channels=[NotificationChannel.EMAIL, NotificationChannel.SMS, NotificationChannel.SLACK],
        recipients=['oncall@example.com', '+1234567890', 'https://hooks.slack.com/webhook'],
        escalation_delay_minutes=15,
        enabled=True
    )
    
    alert_manager.notification_rules['critical_alerts'] = critical_rule
    
    # Process sample alert
    alert_data = {
        'title': 'High CPU Usage Detected',
        'description': 'CPU usage has exceeded 90% for more than 5 minutes',
        'severity': 'critical',
        'source': 'cloudwatch',
        'metric_name': 'CPUUtilization',
        'current_value': 95.5,
        'threshold_value': 90.0,
        'dimensions': {
            'InstanceId': 'i-1234567890abcdef0',
            'Environment': 'production'
        }
    }
    
    alert_id = await alert_manager.process_alert(alert_data)
    print(f"Processed alert: {alert_id}")
    
    # Simulate alert acknowledgment
    await asyncio.sleep(2)
    success = await alert_manager.acknowledge_alert(alert_id, 'operator@example.com')
    print(f"Alert acknowledged: {success}")
    
    # Simulate alert resolution
    await asyncio.sleep(2)
    success = await alert_manager.resolve_alert(alert_id, 'operator@example.com', 'CPU usage returned to normal')
    print(f"Alert resolved: {success}")

if __name__ == "__main__":
    asyncio.run(main())
```

## AWS Services Used

- **Amazon SNS**: Multi-channel notification delivery (email, SMS, mobile push)
- **Amazon SES**: Email notification service with templating and delivery tracking
- **AWS Lambda**: Serverless functions for alert processing and notification logic
- **Amazon DynamoDB**: Storage for alerts, notification rules, and escalation tracking
- **Amazon EventBridge**: Event-driven alert routing and processing
- **AWS Systems Manager**: Parameter store for notification configuration management
- **Amazon CloudWatch**: Alarm generation and metric-based alerting
- **AWS Step Functions**: Complex alert workflow orchestration and escalation
- **Amazon API Gateway**: REST APIs for alert management and acknowledgment
- **AWS Secrets Manager**: Secure storage of notification service credentials
- **Amazon Kinesis**: Real-time alert stream processing and routing
- **AWS Chatbot**: Integration with Slack and Microsoft Teams
- **Amazon Connect**: Voice call notifications for critical alerts
- **AWS X-Ray**: Distributed tracing for notification delivery tracking
- **Amazon CloudFront**: CDN for alert dashboard and management interfaces

## Benefits

- **Rapid Response**: Real-time notifications enable quick incident response
- **Reduced Alert Fatigue**: Intelligent filtering and deduplication prevent notification overload
- **Improved Accountability**: Clear alert ownership and escalation procedures
- **Multi-Channel Delivery**: Flexible notification channels ensure message delivery
- **Context-Aware Routing**: Smart routing based on alert content and recipient roles
- **Escalation Management**: Automated escalation ensures critical issues get attention
- **Audit Trail**: Complete history of alert lifecycle and response actions
- **Cost Optimization**: Efficient notification delivery reduces operational costs
- **Better Collaboration**: Integration with team communication tools improves coordination
- **Continuous Improvement**: Alert metrics and feedback enable optimization

## Related Resources

- [AWS Well-Architected Reliability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/)
- [Send Notifications](https://docs.aws.amazon.com/wellarchitected/latest/framework/rel_monitor_aws_resources_notification_monitor.html)
- [Amazon SNS User Guide](https://docs.aws.amazon.com/sns/latest/dg/)
- [Amazon SES Developer Guide](https://docs.aws.amazon.com/ses/latest/dg/)
- [Amazon CloudWatch Alarms](https://docs.aws.amazon.com/cloudwatch/latest/monitoring/AlarmThatSendsEmail.html)
- [AWS Chatbot User Guide](https://docs.aws.amazon.com/chatbot/latest/adminguide/)
- [AWS Lambda Best Practices](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
- [Alert Management Best Practices](https://aws.amazon.com/blogs/mt/best-practices-for-monitoring-and-alerting-with-amazon-cloudwatch/)
- [Amazon EventBridge User Guide](https://docs.aws.amazon.com/eventbridge/latest/userguide/)
- [AWS Step Functions User Guide](https://docs.aws.amazon.com/step-functions/latest/dg/)
- [Incident Response Automation](https://aws.amazon.com/blogs/mt/automated-incident-response-and-forensics-framework/)
- [Building Resilient Systems](https://aws.amazon.com/builders-library/)
