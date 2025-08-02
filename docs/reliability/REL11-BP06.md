---
title: REL11-BP06 - Send notifications when events impact availability
layout: default
parent: Reliability
nav_order: 116
---

# REL11-BP06: Send notifications when events impact availability

Implement comprehensive notification systems that alert appropriate stakeholders when events impact or could impact system availability. This includes both technical teams for immediate response and business stakeholders for impact assessment and communication planning.

## Implementation Steps

### 1. Define Notification Categories
Classify events by severity and impact to determine appropriate notification channels.

### 2. Configure Multi-Channel Delivery
Set up multiple notification channels to ensure message delivery during outages.

### 3. Implement Escalation Procedures
Design escalation workflows that increase notification scope based on event duration and impact.

### 4. Create Status Pages
Provide public and internal status pages for transparent communication.

### 5. Automate Incident Communication
Implement automated systems for consistent and timely incident communication.

## Detailed Implementation

{% raw %}
```python
import boto3
import json
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, asdict
from enum import Enum
import threading
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import slack_sdk
from twilio.rest import Client as TwilioClient

class NotificationSeverity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

class NotificationChannel(Enum):
    EMAIL = "email"
    SMS = "sms"
    SLACK = "slack"
    PAGERDUTY = "pagerduty"
    WEBHOOK = "webhook"
    STATUS_PAGE = "status_page"
    SNS = "sns"

class IncidentStatus(Enum):
    INVESTIGATING = "investigating"
    IDENTIFIED = "identified"
    MONITORING = "monitoring"
    RESOLVED = "resolved"

class AudienceType(Enum):
    TECHNICAL = "technical"
    BUSINESS = "business"
    CUSTOMER = "customer"
    EXECUTIVE = "executive"

@dataclass
class NotificationRule:
    name: str
    severity: NotificationSeverity
    channels: List[NotificationChannel]
    audiences: List[AudienceType]
    conditions: Dict[str, Any]
    escalation_delay: int
    max_escalations: int
    enabled: bool

@dataclass
class NotificationRecipient:
    name: str
    audience_type: AudienceType
    email: Optional[str]
    phone: Optional[str]
    slack_user_id: Optional[str]
    escalation_level: int

@dataclass
class AvailabilityEvent:
    event_id: str
    title: str
    description: str
    severity: NotificationSeverity
    affected_services: List[str]
    start_time: datetime
    end_time: Optional[datetime]
    status: IncidentStatus
    impact_description: str
    root_cause: Optional[str]
    resolution_steps: List[str]

class AvailabilityNotificationSystem:
    def __init__(self, region: str = 'us-east-1'):
        self.region = region
        
        # AWS clients
        self.sns = boto3.client('sns', region_name=region)
        self.ses = boto3.client('ses', region_name=region)
        self.cloudwatch = boto3.client('cloudwatch', region_name=region)
        self.lambda_client = boto3.client('lambda', region_name=region)
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Notification state
        self.notification_rules: Dict[str, NotificationRule] = {}
        self.recipients: Dict[str, NotificationRecipient] = {}
        self.active_incidents: Dict[str, AvailabilityEvent] = {}
        self.notification_history: List[Dict[str, Any]] = []
        
        # External service clients
        self.slack_client = None
        self.twilio_client = None
        self.pagerduty_api_key = None
        
        # Status page configuration
        self.status_page_config = {}
        
        # Thread safety
        self.notification_lock = threading.Lock()

    def configure_external_services(self, config: Dict[str, Any]) -> None:
        """Configure external notification services"""
        try:
            # Slack configuration
            if 'slack_token' in config:
                self.slack_client = slack_sdk.WebClient(token=config['slack_token'])
                self.logger.info("Slack client configured")
            
            # Twilio configuration
            if 'twilio_account_sid' in config and 'twilio_auth_token' in config:
                self.twilio_client = TwilioClient(
                    config['twilio_account_sid'],
                    config['twilio_auth_token']
                )
                self.logger.info("Twilio client configured")
            
            # PagerDuty configuration
            if 'pagerduty_api_key' in config:
                self.pagerduty_api_key = config['pagerduty_api_key']
                self.logger.info("PagerDuty API key configured")
            
            # Status page configuration
            if 'status_page' in config:
                self.status_page_config = config['status_page']
                self.logger.info("Status page configured")
                
        except Exception as e:
            self.logger.error(f"External service configuration failed: {str(e)}")

    def register_notification_rule(self, rule: NotificationRule) -> bool:
        """Register a notification rule"""
        try:
            self.notification_rules[rule.name] = rule
            self.logger.info(f"Registered notification rule: {rule.name}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to register notification rule {rule.name}: {str(e)}")
            return False

    def register_recipient(self, recipient: NotificationRecipient) -> bool:
        """Register a notification recipient"""
        try:
            self.recipients[recipient.name] = recipient
            self.logger.info(f"Registered notification recipient: {recipient.name}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to register recipient {recipient.name}: {str(e)}")
            return False

    def create_availability_event(self, event: AvailabilityEvent) -> str:
        """Create and process an availability event"""
        try:
            with self.notification_lock:
                self.active_incidents[event.event_id] = event
            
            # Determine applicable notification rules
            applicable_rules = self._get_applicable_rules(event)
            
            # Send initial notifications
            for rule in applicable_rules:
                self._send_notifications(event, rule, escalation_level=0)
            
            # Update status page
            self._update_status_page(event)
            
            # Schedule escalations if needed
            self._schedule_escalations(event, applicable_rules)
            
            self.logger.info(f"Created availability event: {event.event_id}")
            return event.event_id
            
        except Exception as e:
            self.logger.error(f"Failed to create availability event: {str(e)}")
            return ""

    def update_availability_event(self, event_id: str, updates: Dict[str, Any]) -> bool:
        """Update an existing availability event"""
        try:
            with self.notification_lock:
                if event_id not in self.active_incidents:
                    raise ValueError(f"Event {event_id} not found")
                
                event = self.active_incidents[event_id]
                
                # Update event fields
                for field, value in updates.items():
                    if hasattr(event, field):
                        setattr(event, field, value)
                
                # Send update notifications
                if updates.get('send_notification', True):
                    applicable_rules = self._get_applicable_rules(event)
                    for rule in applicable_rules:
                        self._send_update_notifications(event, rule, updates)
                
                # Update status page
                self._update_status_page(event)
                
                # Move to history if resolved
                if event.status == IncidentStatus.RESOLVED:
                    del self.active_incidents[event_id]
                    self._archive_incident(event)
            
            self.logger.info(f"Updated availability event: {event_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update availability event {event_id}: {str(e)}")
            return False

    def _send_notifications(self, event: AvailabilityEvent, rule: NotificationRule, escalation_level: int = 0) -> None:
        """Send notifications for an event"""
        try:
            # Get recipients for this rule and escalation level
            recipients = self._get_recipients_for_rule(rule, escalation_level)
            
            # Send notifications through each configured channel
            for channel in rule.channels:
                if channel == NotificationChannel.EMAIL:
                    self._send_email_notifications(event, recipients)
                elif channel == NotificationChannel.SMS:
                    self._send_sms_notifications(event, recipients)
                elif channel == NotificationChannel.SLACK:
                    self._send_slack_notifications(event, recipients)
                elif channel == NotificationChannel.PAGERDUTY:
                    self._send_pagerduty_notifications(event, recipients)
                elif channel == NotificationChannel.SNS:
                    self._send_sns_notifications(event, recipients)
                elif channel == NotificationChannel.WEBHOOK:
                    self._send_webhook_notifications(event, recipients)
            
            # Record notification in history
            self._record_notification(event, rule, recipients, escalation_level)
            
        except Exception as e:
            self.logger.error(f"Failed to send notifications: {str(e)}")

    def _send_email_notifications(self, event: AvailabilityEvent, recipients: List[NotificationRecipient]) -> None:
        """Send email notifications"""
        try:
            email_recipients = [r for r in recipients if r.email]
            if not email_recipients:
                return
            
            # Create email content
            subject = f"[{event.severity.value.upper()}] {event.title}"
            
            html_body = self._generate_email_template(event)
            text_body = self._generate_text_template(event)
            
            # Send via SES
            for recipient in email_recipients:
                try:
                    response = self.ses.send_email(
                        Source='noreply@example.com',
                        Destination={'ToAddresses': [recipient.email]},
                        Message={
                            'Subject': {'Data': subject},
                            'Body': {
                                'Html': {'Data': html_body},
                                'Text': {'Data': text_body}
                            }
                        }
                    )
                    self.logger.info(f"Email sent to {recipient.email}: {response['MessageId']}")
                except Exception as e:
                    self.logger.error(f"Failed to send email to {recipient.email}: {str(e)}")
                    
        except Exception as e:
            self.logger.error(f"Email notification failed: {str(e)}")

    def _send_sms_notifications(self, event: AvailabilityEvent, recipients: List[NotificationRecipient]) -> None:
        """Send SMS notifications"""
        try:
            if not self.twilio_client:
                self.logger.warning("Twilio client not configured, skipping SMS notifications")
                return
            
            sms_recipients = [r for r in recipients if r.phone]
            if not sms_recipients:
                return
            
            # Create SMS content
            message = f"[{event.severity.value.upper()}] {event.title}\n\n{event.description}\n\nAffected: {', '.join(event.affected_services)}\n\nStatus: {event.status.value}"
            
            # Truncate if too long
            if len(message) > 1600:
                message = message[:1597] + "..."
            
            # Send SMS
            for recipient in sms_recipients:
                try:
                    message_obj = self.twilio_client.messages.create(
                        body=message,
                        from_='+1234567890',  # Your Twilio number
                        to=recipient.phone
                    )
                    self.logger.info(f"SMS sent to {recipient.phone}: {message_obj.sid}")
                except Exception as e:
                    self.logger.error(f"Failed to send SMS to {recipient.phone}: {str(e)}")
                    
        except Exception as e:
            self.logger.error(f"SMS notification failed: {str(e)}")

    def _send_slack_notifications(self, event: AvailabilityEvent, recipients: List[NotificationRecipient]) -> None:
        """Send Slack notifications"""
        try:
            if not self.slack_client:
                self.logger.warning("Slack client not configured, skipping Slack notifications")
                return
            
            # Create Slack message
            blocks = self._generate_slack_blocks(event)
            
            # Send to channels and direct messages
            slack_recipients = [r for r in recipients if r.slack_user_id]
            
            # Send to incident channel
            try:
                response = self.slack_client.chat_postMessage(
                    channel='#incidents',
                    blocks=blocks,
                    text=f"[{event.severity.value.upper()}] {event.title}"
                )
                self.logger.info(f"Slack message sent to #incidents: {response['ts']}")
            except Exception as e:
                self.logger.error(f"Failed to send Slack message to #incidents: {str(e)}")
            
            # Send direct messages to recipients
            for recipient in slack_recipients:
                try:
                    response = self.slack_client.chat_postMessage(
                        channel=recipient.slack_user_id,
                        blocks=blocks,
                        text=f"[{event.severity.value.upper()}] {event.title}"
                    )
                    self.logger.info(f"Slack DM sent to {recipient.name}: {response['ts']}")
                except Exception as e:
                    self.logger.error(f"Failed to send Slack DM to {recipient.name}: {str(e)}")
                    
        except Exception as e:
            self.logger.error(f"Slack notification failed: {str(e)}")

    def _send_pagerduty_notifications(self, event: AvailabilityEvent, recipients: List[NotificationRecipient]) -> None:
        """Send PagerDuty notifications"""
        try:
            if not self.pagerduty_api_key:
                self.logger.warning("PagerDuty API key not configured, skipping PagerDuty notifications")
                return
            
            # Create PagerDuty event
            payload = {
                "routing_key": "your-integration-key",
                "event_action": "trigger",
                "dedup_key": event.event_id,
                "payload": {
                    "summary": event.title,
                    "source": "availability-monitoring",
                    "severity": event.severity.value,
                    "component": "system",
                    "group": "infrastructure",
                    "class": "availability",
                    "custom_details": {
                        "description": event.description,
                        "affected_services": event.affected_services,
                        "impact": event.impact_description
                    }
                }
            }
            
            # Send to PagerDuty
            response = requests.post(
                'https://events.pagerduty.com/v2/enqueue',
                json=payload,
                headers={
                    'Authorization': f'Token token={self.pagerduty_api_key}',
                    'Content-Type': 'application/json'
                }
            )
            
            if response.status_code == 202:
                self.logger.info(f"PagerDuty alert created for event {event.event_id}")
            else:
                self.logger.error(f"PagerDuty alert failed: {response.status_code} - {response.text}")
                
        except Exception as e:
            self.logger.error(f"PagerDuty notification failed: {str(e)}")

    def _send_sns_notifications(self, event: AvailabilityEvent, recipients: List[NotificationRecipient]) -> None:
        """Send SNS notifications"""
        try:
            # Create SNS message
            message = {
                'default': f"[{event.severity.value.upper()}] {event.title}",
                'email': self._generate_text_template(event),
                'sms': f"[{event.severity.value.upper()}] {event.title}\n{event.description}"
            }
            
            # Publish to SNS topic
            response = self.sns.publish(
                TopicArn=f'arn:aws:sns:{self.region}:123456789012:availability-alerts',
                Message=json.dumps(message),
                MessageStructure='json',
                Subject=f"[{event.severity.value.upper()}] {event.title}"
            )
            
            self.logger.info(f"SNS notification sent: {response['MessageId']}")
            
        except Exception as e:
            self.logger.error(f"SNS notification failed: {str(e)}")

    def _update_status_page(self, event: AvailabilityEvent) -> None:
        """Update status page with incident information"""
        try:
            if not self.status_page_config:
                return
            
            # Create status page update
            status_update = {
                'incident_id': event.event_id,
                'title': event.title,
                'description': event.description,
                'status': event.status.value,
                'affected_services': event.affected_services,
                'created_at': event.start_time.isoformat(),
                'updated_at': datetime.utcnow().isoformat(),
                'severity': event.severity.value
            }
            
            # Update status page via API
            if self.status_page_config.get('api_endpoint'):
                response = requests.post(
                    f"{self.status_page_config['api_endpoint']}/incidents",
                    json=status_update,
                    headers={
                        'Authorization': f"Bearer {self.status_page_config.get('api_key')}",
                        'Content-Type': 'application/json'
                    }
                )
                
                if response.status_code in [200, 201]:
                    self.logger.info(f"Status page updated for incident {event.event_id}")
                else:
                    self.logger.error(f"Status page update failed: {response.status_code}")
            
        except Exception as e:
            self.logger.error(f"Status page update failed: {str(e)}")

    def _generate_email_template(self, event: AvailabilityEvent) -> str:
        """Generate HTML email template"""
        severity_colors = {
            NotificationSeverity.CRITICAL: '#dc3545',
            NotificationSeverity.HIGH: '#fd7e14',
            NotificationSeverity.MEDIUM: '#ffc107',
            NotificationSeverity.LOW: '#28a745',
            NotificationSeverity.INFO: '#17a2b8'
        }
        
        color = severity_colors.get(event.severity, '#6c757d')
        
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; margin: 0; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto;">
                <div style="background-color: {color}; color: white; padding: 20px; border-radius: 5px 5px 0 0;">
                    <h1 style="margin: 0; font-size: 24px;">[{event.severity.value.upper()}] {event.title}</h1>
                </div>
                <div style="background-color: #f8f9fa; padding: 20px; border: 1px solid #dee2e6; border-top: none; border-radius: 0 0 5px 5px;">
                    <p><strong>Status:</strong> {event.status.value.title()}</p>
                    <p><strong>Started:</strong> {event.start_time.strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
                    <p><strong>Affected Services:</strong> {', '.join(event.affected_services)}</p>
                    
                    <h3>Description</h3>
                    <p>{event.description}</p>
                    
                    <h3>Impact</h3>
                    <p>{event.impact_description}</p>
                    
                    {f'<h3>Root Cause</h3><p>{event.root_cause}</p>' if event.root_cause else ''}
                    
                    {f'<h3>Resolution Steps</h3><ul>{"".join([f"<li>{step}</li>" for step in event.resolution_steps])}</ul>' if event.resolution_steps else ''}
                </div>
            </div>
        </body>
        </html>
        """
        
        return html

    def _generate_slack_blocks(self, event: AvailabilityEvent) -> List[Dict[str, Any]]:
        """Generate Slack message blocks"""
        severity_colors = {
            NotificationSeverity.CRITICAL: 'danger',
            NotificationSeverity.HIGH: 'warning',
            NotificationSeverity.MEDIUM: 'warning',
            NotificationSeverity.LOW: 'good',
            NotificationSeverity.INFO: '#17a2b8'
        }
        
        color = severity_colors.get(event.severity, 'good')
        
        blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*[{event.severity.value.upper()}] {event.title}*"
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"*Status:*\n{event.status.value.title()}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Started:*\n{event.start_time.strftime('%Y-%m-%d %H:%M:%S UTC')}"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*Affected Services:*\n{', '.join(event.affected_services)}"
                    }
                ]
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Description:*\n{event.description}"
                }
            }
        ]
        
        if event.impact_description:
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Impact:*\n{event.impact_description}"
                }
            })
        
        return blocks

    def get_notification_statistics(self) -> Dict[str, Any]:
        """Get notification system statistics"""
        try:
            stats = {
                'active_incidents': len(self.active_incidents),
                'notification_rules': len(self.notification_rules),
                'registered_recipients': len(self.recipients),
                'notifications_sent_24h': 0,
                'incidents_by_severity': {},
                'notifications_by_channel': {}
            }
            
            # Count incidents by severity
            for incident in self.active_incidents.values():
                severity = incident.severity.value
                stats['incidents_by_severity'][severity] = stats['incidents_by_severity'].get(severity, 0) + 1
            
            # Count recent notifications
            cutoff_time = datetime.utcnow() - timedelta(hours=24)
            recent_notifications = [
                n for n in self.notification_history 
                if datetime.fromisoformat(n['timestamp']) > cutoff_time
            ]
            stats['notifications_sent_24h'] = len(recent_notifications)
            
            # Count by channel
            for notification in recent_notifications:
                for channel in notification.get('channels', []):
                    stats['notifications_by_channel'][channel] = stats['notifications_by_channel'].get(channel, 0) + 1
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Statistics calculation failed: {str(e)}")
            return {}

# Example usage
def main():
    # Initialize notification system
    notification_system = AvailabilityNotificationSystem(region='us-east-1')
    
    # Configure external services
    external_config = {
        'slack_token': 'xoxb-your-slack-token',
        'twilio_account_sid': 'your-twilio-sid',
        'twilio_auth_token': 'your-twilio-token',
        'pagerduty_api_key': 'your-pagerduty-key',
        'status_page': {
            'api_endpoint': 'https://api.statuspage.io/v1/pages/your-page-id',
            'api_key': 'your-statuspage-key'
        }
    }
    
    notification_system.configure_external_services(external_config)
    
    # Register notification rules
    critical_rule = NotificationRule(
        name='critical_incidents',
        severity=NotificationSeverity.CRITICAL,
        channels=[NotificationChannel.EMAIL, NotificationChannel.SMS, NotificationChannel.SLACK, NotificationChannel.PAGERDUTY],
        audiences=[AudienceType.TECHNICAL, AudienceType.BUSINESS],
        conditions={'immediate': True},
        escalation_delay=300,  # 5 minutes
        max_escalations=3,
        enabled=True
    )
    
    notification_system.register_notification_rule(critical_rule)
    
    # Register recipients
    tech_lead = NotificationRecipient(
        name='tech_lead',
        audience_type=AudienceType.TECHNICAL,
        email='tech.lead@example.com',
        phone='+1234567890',
        slack_user_id='U1234567890',
        escalation_level=0
    )
    
    notification_system.register_recipient(tech_lead)
    
    # Create availability event
    event = AvailabilityEvent(
        event_id='incident-2024-001',
        title='Database Connection Failures',
        description='Primary database is experiencing connection timeouts affecting user authentication',
        severity=NotificationSeverity.CRITICAL,
        affected_services=['user-service', 'auth-service'],
        start_time=datetime.utcnow(),
        end_time=None,
        status=IncidentStatus.INVESTIGATING,
        impact_description='Users unable to log in, existing sessions may be affected',
        root_cause=None,
        resolution_steps=['Investigating database connection pool', 'Checking network connectivity']
    )
    
    # Process the event
    event_id = notification_system.create_availability_event(event)
    print(f"Created availability event: {event_id}")
    
    # Get statistics
    stats = notification_system.get_notification_statistics()
    print(f"Notification statistics: {json.dumps(stats, indent=2)}")

if __name__ == "__main__":
    main()
```
{% endraw %}

## AWS Services

### Primary Services
- **Amazon SNS**: Multi-channel notification delivery
- **Amazon SES**: Email notification service
- **AWS Lambda**: Event-driven notification processing
- **Amazon CloudWatch**: Monitoring and alerting integration

### Supporting Services
- **Amazon EventBridge**: Event routing for notifications
- **AWS Systems Manager**: Parameter management for notification configuration
- **Amazon S3**: Storage for notification templates and history
- **AWS Step Functions**: Orchestration of complex notification workflows

## Benefits

- **Rapid Response**: Immediate notification enables faster incident response
- **Stakeholder Awareness**: Keep all relevant parties informed of availability impacts
- **Escalation Management**: Automatic escalation ensures critical issues get attention
- **Communication Transparency**: Status pages provide public visibility
- **Audit Trail**: Complete history of notifications for compliance and analysis

## Related Resources

- [Amazon SNS Developer Guide](https://docs.aws.amazon.com/sns/)
- [Amazon SES Developer Guide](https://docs.aws.amazon.com/ses/)
- [AWS Lambda Developer Guide](https://docs.aws.amazon.com/lambda/)
- [Amazon CloudWatch User Guide](https://docs.aws.amazon.com/cloudwatch/)
