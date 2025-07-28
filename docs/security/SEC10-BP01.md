---
title: "SEC10-BP01: Identify key personnel and external resources"
layout: default
parent: "SEC10 - How do you anticipate, respond to, and recover from incidents?"
grand_parent: Security
nav_order: 1
---

# SEC10-BP01: Identify key personnel and external resources

## Overview

Identify internal and external personnel, resources, and legal obligations to help your organization respond to an incident.

**Desired outcome:** You have a list of key personnel, their contact information, and the roles they play when responding to a security event. You review this information regularly and update it to reflect personnel changes from an internal and external tools perspective. You consider all third-party service providers and vendors while documenting this information, including security partners, cloud providers, and software-as-a-service (SaaS) applications. During a security event, personnel are available with the appropriate level of responsibility, context, and access to be able to respond and recover.

**Common anti-patterns:**
- Not maintaining an updated list of key personnel with contact information, their roles, and their responsibilities when responding to security events
- Assuming that everyone understands the people, dependencies, infrastructure, and solutions when responding to and recovering from an event
- Not having a document or knowledge repository that represents key infrastructure or application design
- Not having proper onboarding processes for new employees to effectively contribute to a security event response, such as conducting event simulations
- Not having an escalation path in place when key personnel are temporarily unavailable or fail to respond during security events

**Benefits of establishing this best practice:**
- This practice reduces the triage and response time spent on identifying the right personnel and their roles during an event
- Minimize wasted time during an event by maintaining an updated list of key personnel and their roles so you can bring the right individuals to triage and recover from an event

**Level of risk exposed if this best practice is not established:** High

## Implementation Guidance

### Identify key personnel in your organization

Maintain a contact list of personnel within your organization that you need to involve. Regularly review and update this information in the event of personnel movement, like organizational changes, promotions, and team changes. This is especially important for key roles like incident managers, incident responders, and communications lead.

**Key Roles:**

- **Incident manager:** Incident managers have overall authority during the event response
- **Incident responders:** Incident responders are responsible for investigation and remediation activities. These people can differ based on the type of event, but are typically developers and operation teams responsible for the impacted application
- **Communications lead:** The communications lead is responsible for internal and external communications, especially with public agencies, regulators, and customers
- **Subject matter experts (SMEs):** In the case of distributed and autonomous teams, we recommend you identify an SME for mission critical workloads. They offer insights into the operation and data classification of critical workloads involved in the event

**Onboarding process:** Regularly train and onboard new employees to equip them with the necessary skills and knowledge to contribute effectively to incident response efforts. Incorporate simulations and hands-on exercises as part of the onboarding process to facilitate their preparedness.

### Example Contact Table Format

| Role | Name | Contact Information | Responsibilities |
|------|------|-------------------|------------------|
| Incident Manager | Jane Doe | jane.doe@example.com | Overall authority during response |
| Incident Responder | John Smith | john.smith@example.com | Investigation and remediation |
| Communications Lead | Emily Johnson | emily.johnson@example.com | Internal and external communications |
| SME | Michael Brown | michael.brown@example.com | Insights on critical workloads |

Consider using the [AWS Systems Manager Incident Manager](https://docs.aws.amazon.com/incident-manager/latest/userguide/what-is-incident-manager.html) feature to capture key contacts, define a response plan, automate on-call schedules, and create escalation plans. Automate and rotate all staff through an on-call schedule, so that responsibility for the workload is shared across its owners. This promotes good practices, such as emitting relevant metrics and logs as well as defining alarm thresholds that matter for the workload.

### Identify external partners

Enterprises use tools built by independent software vendors (ISVs), partners, and subcontractors to build differentiating solutions for their customers. Engage key personnel from these parties who can help respond to and recover from an incident. We recommend you sign up for the appropriate level of [AWS Support](https://aws.amazon.com/support/) in order to get prompt access to AWS subject matter experts through a support case. Consider similar arrangements with all critical solutions providers for the workloads.

Some security events require publicly listed businesses to notify relevant public agencies and regulators of the event and impacts. Maintain and update contact information for the relevant departments and responsible individuals.
### Implementation Steps

1. **Set up an incident management solution:** Consider deploying [Incident Manager](https://docs.aws.amazon.com/incident-manager/latest/userguide/what-is-incident-manager.html) in your Security Tooling account

2. **Define contacts in your incident management solution:** Define at least two types of contact channels for each contact (such as SMS, phone, or email), to ensure reachability during an incident

3. **Define a response plan:** Identify the most appropriate contacts to engage during an incident

4. **Define escalation plans:** Align escalation plans to the roles of personnel to be engaged, rather than individual contacts. Consider including contacts that may be responsible for informing external entities, even if they are not directly engaged to resolve the incident
## Implementation Examples

### Example 1: Incident Response Team Management System

```python
# incident_response_team_manager.py
import boto3
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ContactInfo:
    name: str
    role: str
    primary_email: str
    secondary_email: Optional[str]
    primary_phone: str
    secondary_phone: Optional[str]
    sms_number: str
    department: str
    manager: str
    backup_contact: Optional[str]
    availability_hours: str
    time_zone: str
    escalation_level: int
    skills: List[str]
    certifications: List[str]
    last_updated: str

@dataclass
class ExternalResource:
    organization: str
    contact_name: str
    role: str
    service_type: str
    contract_number: Optional[str]
    support_level: str
    contact_email: str
    contact_phone: str
    escalation_email: str
    escalation_phone: str
    availability: str
    response_sla: str
    expertise_areas: List[str]
    last_updated: str

class IncidentResponseTeamManager:
    """
    Comprehensive system for managing incident response team personnel and external resources
    """
    
    def __init__(self, region: str = 'us-east-1'):
        self.region = region
        self.incident_manager_client = boto3.client('ssm-incidents', region_name=region)
        self.sns_client = boto3.client('sns', region_name=region)
        self.dynamodb = boto3.resource('dynamodb', region_name=region)
        self.ssm_client = boto3.client('ssm', region_name=region)
        
        # DynamoDB tables for storing contact information
        self.contacts_table = self.dynamodb.Table('incident-response-contacts')
        self.external_resources_table = self.dynamodb.Table('external-incident-resources')
        self.escalation_plans_table = self.dynamodb.Table('incident-escalation-plans')
        
        # Initialize incident response roles
        self.incident_roles = self._define_incident_roles()
    
    def _define_incident_roles(self) -> Dict[str, Dict[str, Any]]:
        """
        Define standard incident response roles and their responsibilities
        """
        return {
            'incident_commander': {
                'title': 'Incident Commander',
                'responsibilities': [
                    'Overall authority and decision-making during incident response',
                    'Coordinate response activities across teams',
                    'Communicate with executive leadership',
                    'Make critical business decisions during incidents',
                    'Declare incident severity and escalation levels'
                ],
                'required_skills': ['Leadership', 'Decision Making', 'Communication'],
                'escalation_level': 1,
                'notification_priority': 'immediate'
            },
            'incident_manager': {
                'title': 'Incident Manager',
                'responsibilities': [
                    'Manage incident response process and timeline',
                    'Coordinate between technical teams and stakeholders',
                    'Track incident progress and status updates',
                    'Facilitate incident response meetings',
                    'Ensure proper documentation and post-incident review'
                ],
                'required_skills': ['Project Management', 'Communication', 'Process Management'],
                'escalation_level': 2,
                'notification_priority': 'immediate'
            },
            'technical_lead': {
                'title': 'Technical Lead',
                'responsibilities': [
                    'Lead technical investigation and analysis',
                    'Coordinate technical response activities',
                    'Make technical decisions for remediation',
                    'Interface with development and operations teams',
                    'Provide technical status updates'
                ],
                'required_skills': ['Technical Leadership', 'System Architecture', 'Troubleshooting'],
                'escalation_level': 2,
                'notification_priority': 'immediate'
            },
            'security_analyst': {
                'title': 'Security Analyst',
                'responsibilities': [
                    'Perform security incident analysis and investigation',
                    'Identify attack vectors and impact assessment',
                    'Coordinate with threat intelligence teams',
                    'Implement security containment measures',
                    'Document security findings and evidence'
                ],
                'required_skills': ['Security Analysis', 'Forensics', 'Threat Intelligence'],
                'escalation_level': 2,
                'notification_priority': 'immediate'
            },
            'communications_lead': {
                'title': 'Communications Lead',
                'responsibilities': [
                    'Manage internal and external communications',
                    'Coordinate with public relations and legal teams',
                    'Prepare customer and stakeholder notifications',
                    'Handle media inquiries and public statements',
                    'Ensure compliance with notification requirements'
                ],
                'required_skills': ['Communications', 'Public Relations', 'Legal Compliance'],
                'escalation_level': 3,
                'notification_priority': 'high'
            },
            'subject_matter_expert': {
                'title': 'Subject Matter Expert',
                'responsibilities': [
                    'Provide specialized technical expertise',
                    'Assist with system-specific troubleshooting',
                    'Support technical decision-making',
                    'Provide context on system behavior and dependencies',
                    'Assist with technical remediation activities'
                ],
                'required_skills': ['Domain Expertise', 'System Knowledge', 'Technical Analysis'],
                'escalation_level': 3,
                'notification_priority': 'high'
            },
            'legal_counsel': {
                'title': 'Legal Counsel',
                'responsibilities': [
                    'Provide legal guidance during incident response',
                    'Assess regulatory and compliance implications',
                    'Coordinate with law enforcement if required',
                    'Review external communications for legal compliance',
                    'Manage legal documentation and evidence preservation'
                ],
                'required_skills': ['Legal Expertise', 'Regulatory Compliance', 'Risk Assessment'],
                'escalation_level': 4,
                'notification_priority': 'medium'
            }
        }
    
    def add_internal_contact(self, contact: ContactInfo) -> Dict[str, Any]:
        """
        Add or update internal incident response contact
        """
        try:
            # Validate contact information
            validation_result = self._validate_contact_info(contact)
            if not validation_result['valid']:
                return {
                    'status': 'error',
                    'message': f"Contact validation failed: {validation_result['errors']}"
                }
            
            # Store contact in DynamoDB
            contact_item = asdict(contact)
            contact_item['contact_id'] = f"{contact.role}_{contact.name.replace(' ', '_').lower()}"
            contact_item['created_at'] = datetime.utcnow().isoformat()
            contact_item['ttl'] = int((datetime.utcnow() + timedelta(days=365)).timestamp())
            
            self.contacts_table.put_item(Item=contact_item)
            
            # Create or update Incident Manager contact
            self._create_incident_manager_contact(contact)
            
            logger.info(f"Added internal contact: {contact.name} ({contact.role})")
            
            return {
                'status': 'success',
                'contact_id': contact_item['contact_id'],
                'message': f"Successfully added contact {contact.name}"
            }
            
        except Exception as e:
            logger.error(f"Error adding internal contact: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def add_external_resource(self, resource: ExternalResource) -> Dict[str, Any]:
        """
        Add or update external incident response resource
        """
        try:
            # Store external resource in DynamoDB
            resource_item = asdict(resource)
            resource_item['resource_id'] = f"{resource.organization}_{resource.service_type}".replace(' ', '_').lower()
            resource_item['created_at'] = datetime.utcnow().isoformat()
            resource_item['ttl'] = int((datetime.utcnow() + timedelta(days=365)).timestamp())
            
            self.external_resources_table.put_item(Item=resource_item)
            
            logger.info(f"Added external resource: {resource.organization} ({resource.service_type})")
            
            return {
                'status': 'success',
                'resource_id': resource_item['resource_id'],
                'message': f"Successfully added external resource {resource.organization}"
            }
            
        except Exception as e:
            logger.error(f"Error adding external resource: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def create_escalation_plan(self, 
                              plan_name: str,
                              incident_types: List[str],
                              escalation_levels: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create incident escalation plan
        """
        try:
            escalation_plan = {
                'plan_id': plan_name.replace(' ', '_').lower(),
                'plan_name': plan_name,
                'incident_types': incident_types,
                'escalation_levels': escalation_levels,
                'created_at': datetime.utcnow().isoformat(),
                'last_updated': datetime.utcnow().isoformat(),
                'ttl': int((datetime.utcnow() + timedelta(days=365)).timestamp())
            }
            
            # Store escalation plan
            self.escalation_plans_table.put_item(Item=escalation_plan)
            
            # Create Incident Manager response plan
            response_plan_arn = self._create_incident_manager_response_plan(plan_name, escalation_levels)
            
            logger.info(f"Created escalation plan: {plan_name}")
            
            return {
                'status': 'success',
                'plan_id': escalation_plan['plan_id'],
                'response_plan_arn': response_plan_arn,
                'message': f"Successfully created escalation plan {plan_name}"
            }
            
        except Exception as e:
            logger.error(f"Error creating escalation plan: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def get_incident_response_team(self, incident_type: str, severity: str) -> Dict[str, Any]:
        """
        Get appropriate incident response team based on incident type and severity
        """
        try:
            # Query contacts based on incident type and severity
            team_members = []
            
            # Get all contacts
            response = self.contacts_table.scan()
            contacts = response['Items']
            
            # Filter contacts based on incident requirements
            for contact in contacts:
                role_info = self.incident_roles.get(contact['role'], {})
                
                # Include based on escalation level and incident severity
                if self._should_include_in_team(contact, incident_type, severity, role_info):
                    team_members.append({
                        'name': contact['name'],
                        'role': contact['role'],
                        'contact_info': {
                            'primary_email': contact['primary_email'],
                            'primary_phone': contact['primary_phone'],
                            'sms_number': contact['sms_number']
                        },
                        'responsibilities': role_info.get('responsibilities', []),
                        'escalation_level': contact['escalation_level']
                    })
            
            # Sort by escalation level
            team_members.sort(key=lambda x: x['escalation_level'])
            
            return {
                'status': 'success',
                'incident_type': incident_type,
                'severity': severity,
                'team_members': team_members,
                'team_size': len(team_members)
            }
            
        except Exception as e:
            logger.error(f"Error getting incident response team: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def notify_incident_team(self, 
                           incident_id: str,
                           incident_type: str,
                           severity: str,
                           description: str) -> Dict[str, Any]:
        """
        Notify incident response team members
        """
        try:
            # Get incident response team
            team_result = self.get_incident_response_team(incident_type, severity)
            
            if team_result['status'] != 'success':
                return team_result
            
            team_members = team_result['team_members']
            notification_results = []
            
            # Send notifications to team members
            for member in team_members:
                notification_result = self._send_incident_notification(
                    member, incident_id, incident_type, severity, description
                )
                notification_results.append(notification_result)
            
            # Create Incident Manager incident
            incident_arn = self._create_incident_manager_incident(
                incident_id, incident_type, severity, description
            )
            
            successful_notifications = sum(1 for result in notification_results if result['status'] == 'success')
            
            return {
                'status': 'success',
                'incident_id': incident_id,
                'incident_arn': incident_arn,
                'team_size': len(team_members),
                'successful_notifications': successful_notifications,
                'notification_results': notification_results
            }
            
        except Exception as e:
            logger.error(f"Error notifying incident team: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _validate_contact_info(self, contact: ContactInfo) -> Dict[str, Any]:
        """
        Validate contact information
        """
        errors = []
        
        if not contact.name or len(contact.name.strip()) == 0:
            errors.append("Name is required")
        
        if not contact.primary_email or '@' not in contact.primary_email:
            errors.append("Valid primary email is required")
        
        if not contact.primary_phone or len(contact.primary_phone) < 10:
            errors.append("Valid primary phone number is required")
        
        if contact.role not in self.incident_roles:
            errors.append(f"Role must be one of: {list(self.incident_roles.keys())}")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }
    
    def _create_incident_manager_contact(self, contact: ContactInfo):
        """
        Create contact in AWS Systems Manager Incident Manager
        """
        try:
            contact_channels = [
                {
                    'ChannelAddress': contact.primary_email,
                    'ChannelType': 'EMAIL',
                    'DeferActivation': False
                },
                {
                    'ChannelAddress': contact.primary_phone,
                    'ChannelType': 'VOICE',
                    'DeferActivation': False
                },
                {
                    'ChannelAddress': contact.sms_number,
                    'ChannelType': 'SMS',
                    'DeferActivation': False
                }
            ]
            
            # Add secondary channels if available
            if contact.secondary_email:
                contact_channels.append({
                    'ChannelAddress': contact.secondary_email,
                    'ChannelType': 'EMAIL',
                    'DeferActivation': False
                })
            
            if contact.secondary_phone:
                contact_channels.append({
                    'ChannelAddress': contact.secondary_phone,
                    'ChannelType': 'VOICE',
                    'DeferActivation': False
                })
            
            # Create contact in Incident Manager
            response = self.incident_manager_client.create_contact(
                Alias=f"{contact.role}_{contact.name.replace(' ', '_').lower()}",
                DisplayName=f"{contact.name} ({contact.role})",
                Type='PERSONAL',
                Plan={
                    'Stages': [
                        {
                            'DurationInMinutes': 1,
                            'Targets': [
                                {
                                    'ChannelTargetInfo': {
                                        'ContactChannelId': channel['ChannelAddress']
                                    }
                                } for channel in contact_channels[:2]  # Use first 2 channels
                            ]
                        }
                    ]
                }
            )
            
            return response['ContactArn']
            
        except Exception as e:
            logger.error(f"Error creating Incident Manager contact: {str(e)}")
            return None
    
    def _should_include_in_team(self, contact: Dict[str, Any], incident_type: str, severity: str, role_info: Dict[str, Any]) -> bool:
        """
        Determine if contact should be included in incident response team
        """
        # Always include level 1 and 2 escalation contacts
        if contact['escalation_level'] <= 2:
            return True
        
        # Include level 3 for high severity incidents
        if severity in ['high', 'critical'] and contact['escalation_level'] <= 3:
            return True
        
        # Include level 4 for critical incidents
        if severity == 'critical' and contact['escalation_level'] <= 4:
            return True
        
        return False

# Example usage
if __name__ == "__main__":
    # Initialize incident response team manager
    team_manager = IncidentResponseTeamManager()
    
    # Add internal contacts
    incident_commander = ContactInfo(
        name="Jane Smith",
        role="incident_commander",
        primary_email="jane.smith@company.com",
        secondary_email="jane.smith.backup@company.com",
        primary_phone="+1-555-0101",
        secondary_phone="+1-555-0102",
        sms_number="+1-555-0101",
        department="Security Operations",
        manager="John Doe",
        backup_contact="Mike Johnson",
        availability_hours="24/7",
        time_zone="UTC-5",
        escalation_level=1,
        skills=["Incident Management", "Leadership", "Crisis Communication"],
        certifications=["CISSP", "CISM"],
        last_updated=datetime.utcnow().isoformat()
    )
    
    result = team_manager.add_internal_contact(incident_commander)
    print(f"Add contact result: {json.dumps(result, indent=2)}")
    
    # Add external resource
    aws_support = ExternalResource(
        organization="AWS Support",
        contact_name="AWS Technical Support",
        role="Cloud Infrastructure Support",
        service_type="Cloud Support",
        contract_number="ENT-12345",
        support_level="Enterprise",
        contact_email="support@aws.amazon.com",
        contact_phone="+1-800-AWS-SUPPORT",
        escalation_email="enterprise-support@aws.amazon.com",
        escalation_phone="+1-800-AWS-SUPPORT",
        availability="24/7",
        response_sla="15 minutes",
        expertise_areas=["AWS Infrastructure", "Security", "Networking"],
        last_updated=datetime.utcnow().isoformat()
    )
    
    result = team_manager.add_external_resource(aws_support)
    print(f"Add external resource result: {json.dumps(result, indent=2)}")
```
### Example 2: AWS Systems Manager Incident Manager Integration

```python
# incident_manager_integration.py
import boto3
import json
from typing import Dict, List, Any
from datetime import datetime

class IncidentManagerIntegration:
    """
    Integration with AWS Systems Manager Incident Manager for automated incident response
    """
    
    def __init__(self, region: str = 'us-east-1'):
        self.region = region
        self.incident_manager_client = boto3.client('ssm-incidents', region_name=region)
        self.ssm_client = boto3.client('ssm', region_name=region)
    
    def setup_incident_manager_contacts(self) -> Dict[str, Any]:
        """
        Set up contacts in AWS Systems Manager Incident Manager
        """
        try:
            contacts_created = []
            
            # Define incident response contacts
            contacts = [
                {
                    'alias': 'incident-commander-primary',
                    'display_name': 'Primary Incident Commander',
                    'type': 'PERSONAL',
                    'channels': [
                        {'address': 'commander@company.com', 'type': 'EMAIL'},
                        {'address': '+1-555-0101', 'type': 'SMS'},
                        {'address': '+1-555-0101', 'type': 'VOICE'}
                    ]
                },
                {
                    'alias': 'security-team-lead',
                    'display_name': 'Security Team Lead',
                    'type': 'PERSONAL',
                    'channels': [
                        {'address': 'security-lead@company.com', 'type': 'EMAIL'},
                        {'address': '+1-555-0201', 'type': 'SMS'},
                        {'address': '+1-555-0201', 'type': 'VOICE'}
                    ]
                },
                {
                    'alias': 'communications-lead',
                    'display_name': 'Communications Lead',
                    'type': 'PERSONAL',
                    'channels': [
                        {'address': 'comms@company.com', 'type': 'EMAIL'},
                        {'address': '+1-555-0301', 'type': 'SMS'}
                    ]
                }
            ]
            
            # Create contacts
            for contact_config in contacts:
                contact_arn = self._create_contact_with_channels(contact_config)
                contacts_created.append({
                    'alias': contact_config['alias'],
                    'arn': contact_arn
                })
            
            return {
                'status': 'success',
                'contacts_created': contacts_created,
                'message': f"Successfully created {len(contacts_created)} contacts"
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def create_response_plan(self, 
                           plan_name: str,
                           incident_template: Dict[str, Any],
                           escalation_plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create incident response plan in Incident Manager
        """
        try:
            response = self.incident_manager_client.create_response_plan(
                Name=plan_name,
                DisplayName=plan_name.replace('-', ' ').title(),
                IncidentTemplate={
                    'Title': incident_template.get('title', 'Security Incident'),
                    'Impact': incident_template.get('impact', 3),
                    'Summary': incident_template.get('summary', 'Security incident requiring immediate attention'),
                    'DedupeString': incident_template.get('dedupe_string', 'security-incident-{timestamp}'),
                    'NotificationTargets': incident_template.get('notification_targets', []),
                    'IncidentTags': incident_template.get('tags', {})
                },
                Engagements=escalation_plan.get('engagements', []),
                Actions=escalation_plan.get('actions', []),
                ChatChannel={
                    'ChatbotSns': escalation_plan.get('chat_channel', [])
                } if escalation_plan.get('chat_channel') else {},
                Tags=escalation_plan.get('plan_tags', {})
            )
            
            return {
                'status': 'success',
                'response_plan_arn': response['Arn'],
                'message': f"Successfully created response plan {plan_name}"
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _create_contact_with_channels(self, contact_config: Dict[str, Any]) -> str:
        """
        Create contact with multiple communication channels
        """
        # First create the contact
        contact_response = self.incident_manager_client.create_contact(
            Alias=contact_config['alias'],
            DisplayName=contact_config['display_name'],
            Type=contact_config['type'],
            Plan={
                'Stages': [
                    {
                        'DurationInMinutes': 1,
                        'Targets': []  # Will be populated after creating channels
                    }
                ]
            }
        )
        
        contact_arn = contact_response['ContactArn']
        channel_targets = []
        
        # Create communication channels
        for channel in contact_config['channels']:
            try:
                channel_response = self.incident_manager_client.create_contact_channel(
                    ContactId=contact_arn,
                    Name=f"{contact_config['alias']}-{channel['type'].lower()}",
                    Type=channel['type'],
                    DeliveryAddress={
                        'SimpleAddress': channel['address']
                    }
                )
                
                channel_targets.append({
                    'ChannelTargetInfo': {
                        'ContactChannelId': channel_response['ContactChannelArn']
                    }
                })
                
            except Exception as e:
                print(f"Warning: Could not create channel {channel['type']} for {contact_config['alias']}: {str(e)}")
        
        # Update contact plan with channel targets
        if channel_targets:
            self.incident_manager_client.update_contact(
                ContactId=contact_arn,
                Plan={
                    'Stages': [
                        {
                            'DurationInMinutes': 1,
                            'Targets': channel_targets[:3]  # Limit to 3 targets per stage
                        }
                    ]
                }
            )
        
        return contact_arn

# Example usage
if __name__ == "__main__":
    # Initialize Incident Manager integration
    incident_integration = IncidentManagerIntegration()
    
    # Set up contacts
    contacts_result = incident_integration.setup_incident_manager_contacts()
    print(f"Contacts setup result: {json.dumps(contacts_result, indent=2)}")
    
    # Create response plan
    incident_template = {
        'title': 'Security Incident Response',
        'impact': 2,
        'summary': 'Security incident requiring immediate investigation and response',
        'tags': {
            'Department': 'Security',
            'Priority': 'High',
            'Type': 'Security'
        }
    }
    
    escalation_plan = {
        'engagements': [
            'arn:aws:ssm-contacts:us-east-1:123456789012:contact/incident-commander-primary',
            'arn:aws:ssm-contacts:us-east-1:123456789012:contact/security-team-lead'
        ],
        'actions': [
            {
                'SsmAutomation': {
                    'DocumentName': 'AWSIncidents-CriticalIncidentRunbookTemplate',
                    'RoleArn': 'arn:aws:iam::123456789012:role/IncidentResponseRole',
                    'Parameters': {
                        'IncidentType': ['Security'],
                        'Severity': ['High']
                    }
                }
            }
        ]
    }
    
    plan_result = incident_integration.create_response_plan(
        'security-incident-response-plan',
        incident_template,
        escalation_plan
    )
    print(f"Response plan result: {json.dumps(plan_result, indent=2)}")
```
## Resources

### Related Best Practices

- [OPS02-BP03 Operations activities have identified owners responsible for their performance](https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/ops_ops_model_def_ops_activities.html)

### Related Documents

- [AWS Security Incident Response Guide](https://docs.aws.amazon.com/whitepapers/latest/aws-security-incident-response-guide/aws-security-incident-response-guide.html)
- [AWS Systems Manager Incident Manager User Guide](https://docs.aws.amazon.com/incident-manager/latest/userguide/what-is-incident-manager.html)
- [AWS Support Plans](https://aws.amazon.com/support/plans/)

### Related Examples

- [AWS customer playbook framework](https://github.com/aws-samples/aws-customer-playbook-framework)
- [Prepare for and respond to security incidents in your AWS environment](https://aws.amazon.com/blogs/security/prepare-for-and-respond-to-security-incidents-in-your-aws-environment/)

### Related Tools

- [AWS Systems Manager Incident Manager](https://docs.aws.amazon.com/incident-manager/latest/userguide/what-is-incident-manager.html)
- [AWS Support Center](https://console.aws.amazon.com/support/home)
- [AWS Personal Health Dashboard](https://aws.amazon.com/premiumsupport/technology/personal-health-dashboard/)

### Related Videos

- [Amazon's approach to security during development](https://www.youtube.com/watch?v=KJiCfPXOW-U)
