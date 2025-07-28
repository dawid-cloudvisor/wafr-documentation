---
title: "SEC10-BP02: Develop incident management plans"
layout: default
parent: "SEC10 - How do you anticipate, respond to, and recover from incidents?"
grand_parent: Security
nav_order: 2
---

# SEC10-BP02: Develop incident management plans

## Overview

The first document to develop for incident response is the incident response plan. The incident response plan is designed to be the foundation for your incident response program and strategy.

**Benefits of establishing this best practice:** Developing thorough and clearly defined incident response processes is key to a successful and scalable incident response program. When a security event occurs, clear steps and workflows can help you to respond in a timely manner. You might already have existing incident response processes. Regardless of your current state, it's important to update, iterate, and test your incident response processes regularly.

**Level of risk exposed if this best practice is not established:** High

## Implementation Guidance

An incident management plan is critical to respond, mitigate, and recover from the potential impact of security incidents. An incident management plan is a structured process for identifying, remediating, and responding in a timely matter to security incidents. The cloud has many of the same operational roles and requirements found in an on-premises environment. When you create an incident management plan, it is important to factor response and recovery strategies that best align with your business outcome and compliance requirements.

For example, if you operate workloads in AWS that are FedRAMP compliant in the United States, follow the recommendations in [NIST SP 800-61 Computer Security Handling Guide](https://csrc.nist.gov/publications/detail/sp/800-61/rev-2/final). Similarly, when you operate workloads that store personally identifiable information (PII), consider how to protect and respond to issues related to data residency and use.

When building an incident management plan for your workloads in AWS, start with the [AWS Shared Responsibility Model](https://aws.amazon.com/compliance/shared-responsibility-model/) for building a defense-in-depth approach towards incident response. In this model, AWS manages security of the cloud, and you are responsible for security in the cloud. This means that you retain control and are responsible for the security controls you choose to implement.

The [AWS Security Incident Response Guide](https://docs.aws.amazon.com/whitepapers/latest/aws-security-incident-response-guide/aws-security-incident-response-guide.html) details key concepts and foundational guidance for building a cloud-centric incident management plan. An effective incident management plan must be continually iterated upon, remaining current with your cloud operations goal.

### Implementation Steps

1. **Define roles and responsibilities within your organization for handling security events.** This should involve representatives from various departments, including:
   - Human resources (HR)
   - Executive team
   - Legal department
   - Application owners and developers (subject matter experts, or SMEs)

2. **Clearly outline who is responsible, accountable, consulted, and informed (RACI) during an incident.** Create a RACI chart to facilitate quick and direct communication, and clearly outline the leadership across different stages of an event.

3. **Involve application owners and developers (SMEs) during an incident,** as they can provide valuable information and context to aid in measuring the impact. Build relationships with these SMEs, and practice incident response scenarios with them before an actual incident occurs.

4. **Involve trusted partners or external experts in the investigation or response process,** as they can provide additional expertise and perspective.

5. **Align your incident management plans and roles with any local regulations or compliance requirements** that govern your organization.

6. **Practice and test your incident response plans regularly,** and involve all the defined roles and responsibilities. This helps streamline the process and verify you have a coordinated and efficient response to security incidents.

7. **Review and update the roles, responsibilities, and RACI chart periodically,** or as your organizational structure or requirements change.

### Understand AWS Response Teams and Support

**AWS Support:** Support offers a range of plans that provide access to tools and expertise that support the success and operational health of your AWS solutions. Consider the [Support Center in AWS Management Console](https://console.aws.amazon.com/support/home) as the central point of contact to get support for issues that affect your AWS resources.

**AWS Customer Incident Response Team (CIRT):** The AWS Customer Incident Response Team (CIRT) is a specialized 24/7 global AWS team that provides support to customers during active security events on the customer side of the AWS Shared Responsibility Model. AWS customers can engage the AWS CIRT through a Support case.

**DDoS Response Support:** AWS offers [AWS Shield](https://aws.amazon.com/shield/), which provides a managed distributed denial of service (DDoS) protection service that safeguards web applications running on AWS.

**AWS Managed Services (AMS):** [AWS Managed Services](https://aws.amazon.com/managed-services/) provides ongoing management of your AWS infrastructure so you can focus on your applications. AMS takes responsibility for deploying a suite of security detective controls and provides a 24/7 first line of response to alerts.

### Develop the Incident Response Plan

The incident response plan should be in a formal document. An incident response plan typically includes these sections:

- **An incident response team overview:** Outlines the goals and functions of the incident response team
- **Roles and responsibilities:** Lists the incident response stakeholders and details their roles when an incident occurs
- **A communication plan:** Details contact information and how you communicate during an incident
- **Backup communication methods:** It's a best practice to have out-of-band communication as a backup for incident communication
- **Phases of incident response and actions to take:** Enumerates the phases of incident response (for example, detect, analyze, eradicate, contain, and recover), including high-level actions to take within those phases
- **Incident severity and prioritization definitions:** Details how to classify the severity of an incident, how to prioritize the incident, and then how the severity definitions affect escalation procedures
## Implementation Examples

### Example 1: Comprehensive Incident Management Plan Framework

```python
# incident_management_plan.py
import boto3
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IncidentSeverity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class IncidentPhase(Enum):
    PREPARATION = "preparation"
    DETECTION = "detection"
    ANALYSIS = "analysis"
    CONTAINMENT = "containment"
    ERADICATION = "eradication"
    RECOVERY = "recovery"
    POST_INCIDENT = "post_incident"

@dataclass
class IncidentResponseRole:
    role_name: str
    responsibilities: List[str]
    required_skills: List[str]
    escalation_level: int
    notification_methods: List[str]
    backup_personnel: List[str]
    authority_level: str
    decision_making_scope: List[str]

@dataclass
class IncidentClassification:
    incident_type: str
    severity: IncidentSeverity
    impact_assessment: Dict[str, Any]
    affected_systems: List[str]
    data_classification: str
    regulatory_implications: List[str]
    estimated_recovery_time: str
    business_impact: str

@dataclass
class CommunicationPlan:
    internal_stakeholders: List[Dict[str, str]]
    external_stakeholders: List[Dict[str, str]]
    communication_channels: List[str]
    backup_channels: List[str]
    escalation_triggers: List[str]
    notification_templates: Dict[str, str]
    regulatory_notifications: List[Dict[str, Any]]

class IncidentManagementPlanManager:
    """
    Comprehensive incident management plan framework for AWS environments
    """
    
    def __init__(self, region: str = 'us-east-1'):
        self.region = region
        self.dynamodb = boto3.resource('dynamodb', region_name=region)
        self.sns_client = boto3.client('sns', region_name=region)
        self.ssm_client = boto3.client('ssm', region_name=region)
        self.incident_manager_client = boto3.client('ssm-incidents', region_name=region)
        
        # DynamoDB tables for plan management
        self.plans_table = self.dynamodb.Table('incident-management-plans')
        self.playbooks_table = self.dynamodb.Table('incident-response-playbooks')
        self.procedures_table = self.dynamodb.Table('incident-procedures')
        
        # Initialize incident response framework
        self.incident_phases = self._define_incident_phases()
        self.severity_definitions = self._define_severity_levels()
        self.response_roles = self._define_response_roles()
    
    def _define_incident_phases(self) -> Dict[str, Dict[str, Any]]:
        """
        Define the phases of incident response with specific actions and objectives
        """
        return {
            IncidentPhase.PREPARATION.value: {
                'description': 'Establish and maintain incident response capability',
                'objectives': [
                    'Develop incident response policies and procedures',
                    'Train incident response team members',
                    'Acquire and deploy incident response tools',
                    'Conduct regular incident response exercises'
                ],
                'key_activities': [
                    'Policy development and approval',
                    'Team training and certification',
                    'Tool procurement and configuration',
                    'Tabletop exercises and simulations',
                    'Plan testing and validation'
                ],
                'success_criteria': [
                    'Documented and approved incident response plan',
                    'Trained and certified response team',
                    'Deployed and tested incident response tools',
                    'Regular exercise completion'
                ],
                'aws_services': ['Systems Manager', 'CloudTrail', 'GuardDuty', 'Security Hub']
            },
            IncidentPhase.DETECTION.value: {
                'description': 'Identify potential security incidents through monitoring and analysis',
                'objectives': [
                    'Monitor security events and alerts',
                    'Analyze potential indicators of compromise',
                    'Validate and triage security events',
                    'Initiate incident response procedures'
                ],
                'key_activities': [
                    'Security monitoring and alerting',
                    'Event correlation and analysis',
                    'Initial triage and validation',
                    'Incident declaration and notification'
                ],
                'success_criteria': [
                    'Timely detection of security incidents',
                    'Accurate incident classification',
                    'Proper escalation and notification',
                    'Minimal false positive rates'
                ],
                'aws_services': ['GuardDuty', 'Security Hub', 'CloudWatch', 'Detective']
            },
            IncidentPhase.ANALYSIS.value: {
                'description': 'Investigate and understand the scope and impact of the incident',
                'objectives': [
                    'Determine incident scope and impact',
                    'Identify attack vectors and methods',
                    'Assess data and system compromise',
                    'Document findings and evidence'
                ],
                'key_activities': [
                    'Forensic analysis and investigation',
                    'Log analysis and correlation',
                    'System and data impact assessment',
                    'Evidence collection and preservation',
                    'Timeline reconstruction'
                ],
                'success_criteria': [
                    'Complete understanding of incident scope',
                    'Identified attack vectors and methods',
                    'Documented evidence chain',
                    'Accurate impact assessment'
                ],
                'aws_services': ['Detective', 'CloudTrail', 'VPC Flow Logs', 'Macie']
            },
            IncidentPhase.CONTAINMENT.value: {
                'description': 'Limit the spread and impact of the security incident',
                'objectives': [
                    'Isolate affected systems and networks',
                    'Prevent lateral movement',
                    'Preserve evidence for investigation',
                    'Maintain business continuity'
                ],
                'key_activities': [
                    'System isolation and quarantine',
                    'Network segmentation and blocking',
                    'Account and access revocation',
                    'Evidence preservation',
                    'Backup and recovery preparation'
                ],
                'success_criteria': [
                    'Successful isolation of affected systems',
                    'Prevention of further compromise',
                    'Preserved evidence integrity',
                    'Maintained critical business functions'
                ],
                'aws_services': ['Security Groups', 'NACLs', 'IAM', 'WAF', 'Shield']
            },
            IncidentPhase.ERADICATION.value: {
                'description': 'Remove the threat and vulnerabilities from the environment',
                'objectives': [
                    'Remove malware and unauthorized access',
                    'Patch vulnerabilities and weaknesses',
                    'Update security controls',
                    'Strengthen defensive measures'
                ],
                'key_activities': [
                    'Malware removal and cleanup',
                    'Vulnerability patching and remediation',
                    'Security control updates',
                    'System hardening and configuration',
                    'Credential rotation and reset'
                ],
                'success_criteria': [
                    'Complete removal of threats',
                    'Patched vulnerabilities',
                    'Updated security controls',
                    'Strengthened security posture'
                ],
                'aws_services': ['Systems Manager Patch Manager', 'Inspector', 'Config', 'Secrets Manager']
            },
            IncidentPhase.RECOVERY.value: {
                'description': 'Restore systems and services to normal operations',
                'objectives': [
                    'Restore affected systems and services',
                    'Validate system integrity and security',
                    'Monitor for recurring issues',
                    'Return to normal operations'
                ],
                'key_activities': [
                    'System restoration and validation',
                    'Service recovery and testing',
                    'Enhanced monitoring deployment',
                    'Gradual service restoration',
                    'Stakeholder communication'
                ],
                'success_criteria': [
                    'Restored system functionality',
                    'Validated system integrity',
                    'Enhanced monitoring in place',
                    'Normal operations resumed'
                ],
                'aws_services': ['EC2', 'RDS', 'CloudWatch', 'Systems Manager']
            },
            IncidentPhase.POST_INCIDENT.value: {
                'description': 'Learn from the incident and improve response capabilities',
                'objectives': [
                    'Conduct post-incident review',
                    'Document lessons learned',
                    'Update procedures and controls',
                    'Improve response capabilities'
                ],
                'key_activities': [
                    'Post-incident review meeting',
                    'Lessons learned documentation',
                    'Procedure and plan updates',
                    'Training and awareness updates',
                    'Metrics and reporting'
                ],
                'success_criteria': [
                    'Completed post-incident review',
                    'Documented lessons learned',
                    'Updated procedures and plans',
                    'Improved response capabilities'
                ],
                'aws_services': ['CloudWatch Insights', 'QuickSight', 'S3', 'Athena']
            }
        }
    
    def _define_severity_levels(self) -> Dict[str, Dict[str, Any]]:
        """
        Define incident severity levels with specific criteria and response requirements
        """
        return {
            IncidentSeverity.CRITICAL.value: {
                'description': 'Severe impact on business operations or security',
                'criteria': [
                    'Complete system or service outage',
                    'Confirmed data breach with sensitive data exposure',
                    'Active ongoing attack with system compromise',
                    'Regulatory violation with immediate reporting requirements',
                    'Significant financial or reputational impact'
                ],
                'response_time': '15 minutes',
                'escalation_level': 1,
                'notification_scope': 'Executive leadership, all response teams, external partners',
                'communication_frequency': 'Every 30 minutes',
                'resource_allocation': 'All available resources',
                'external_support': 'AWS CIRT, external security firms, law enforcement if required'
            },
            IncidentSeverity.HIGH.value: {
                'description': 'Significant impact on business operations or security',
                'criteria': [
                    'Partial system or service degradation',
                    'Suspected data breach or unauthorized access',
                    'Malware infection or security control bypass',
                    'Compliance violation requiring investigation',
                    'Moderate business impact'
                ],
                'response_time': '30 minutes',
                'escalation_level': 2,
                'notification_scope': 'Management, response teams, key stakeholders',
                'communication_frequency': 'Every hour',
                'resource_allocation': 'Dedicated response team',
                'external_support': 'AWS Support, specialized consultants as needed'
            },
            IncidentSeverity.MEDIUM.value: {
                'description': 'Moderate impact on business operations or security',
                'criteria': [
                    'Minor service disruption or performance issues',
                    'Security policy violations',
                    'Suspicious activity requiring investigation',
                    'Non-critical system compromise',
                    'Limited business impact'
                ],
                'response_time': '2 hours',
                'escalation_level': 3,
                'notification_scope': 'Response team, affected system owners',
                'communication_frequency': 'Every 4 hours',
                'resource_allocation': 'Standard response team',
                'external_support': 'AWS Support as needed'
            },
            IncidentSeverity.LOW.value: {
                'description': 'Minimal impact on business operations or security',
                'criteria': [
                    'Minor security alerts or anomalies',
                    'Policy violations with no immediate risk',
                    'Informational security events',
                    'Routine security maintenance issues',
                    'Minimal or no business impact'
                ],
                'response_time': '4 hours',
                'escalation_level': 4,
                'notification_scope': 'Response team only',
                'communication_frequency': 'Daily updates',
                'resource_allocation': 'Individual responders',
                'external_support': 'Standard support channels'
            }
        }
    
    def _define_response_roles(self) -> Dict[str, IncidentResponseRole]:
        """
        Define incident response roles with specific responsibilities and requirements
        """
        return {
            'incident_commander': IncidentResponseRole(
                role_name='Incident Commander',
                responsibilities=[
                    'Overall incident response leadership and decision-making',
                    'Coordinate response activities across all teams',
                    'Communicate with executive leadership and stakeholders',
                    'Make critical business and technical decisions',
                    'Declare incident severity and escalation levels',
                    'Authorize resource allocation and external support engagement'
                ],
                required_skills=['Leadership', 'Decision Making', 'Crisis Management', 'Communication'],
                escalation_level=1,
                notification_methods=['Phone', 'SMS', 'Email', 'Slack'],
                backup_personnel=['Deputy Incident Commander', 'Senior Security Manager'],
                authority_level='Executive',
                decision_making_scope=['Business continuity', 'Resource allocation', 'External communications']
            ),
            'incident_manager': IncidentResponseRole(
                role_name='Incident Manager',
                responsibilities=[
                    'Manage incident response process and procedures',
                    'Coordinate between technical teams and business stakeholders',
                    'Track incident timeline and status updates',
                    'Facilitate incident response meetings and communications',
                    'Ensure proper documentation and evidence preservation',
                    'Coordinate post-incident review and lessons learned'
                ],
                required_skills=['Project Management', 'Process Management', 'Communication', 'Documentation'],
                escalation_level=2,
                notification_methods=['Phone', 'SMS', 'Email', 'Slack'],
                backup_personnel=['Senior Incident Manager', 'Operations Manager'],
                authority_level='Management',
                decision_making_scope=['Process execution', 'Resource coordination', 'Timeline management']
            ),
            'technical_lead': IncidentResponseRole(
                role_name='Technical Lead',
                responsibilities=[
                    'Lead technical investigation and analysis activities',
                    'Coordinate technical response and remediation efforts',
                    'Make technical decisions for containment and recovery',
                    'Interface with development and operations teams',
                    'Provide technical status updates and recommendations',
                    'Oversee technical evidence collection and preservation'
                ],
                required_skills=['Technical Leadership', 'System Architecture', 'Troubleshooting', 'Security'],
                escalation_level=2,
                notification_methods=['Phone', 'SMS', 'Email', 'Slack'],
                backup_personnel=['Senior Technical Lead', 'Principal Engineer'],
                authority_level='Technical',
                decision_making_scope=['Technical remediation', 'System changes', 'Tool deployment']
            ),
            'security_analyst': IncidentResponseRole(
                role_name='Security Analyst',
                responsibilities=[
                    'Perform detailed security incident analysis and investigation',
                    'Identify attack vectors, methods, and indicators of compromise',
                    'Conduct digital forensics and evidence analysis',
                    'Coordinate with threat intelligence and external security teams',
                    'Document security findings and recommendations',
                    'Support containment and eradication activities'
                ],
                required_skills=['Security Analysis', 'Digital Forensics', 'Threat Intelligence', 'Investigation'],
                escalation_level=2,
                notification_methods=['Phone', 'SMS', 'Email', 'Slack'],
                backup_personnel=['Senior Security Analyst', 'Security Engineer'],
                authority_level='Technical',
                decision_making_scope=['Security analysis', 'Evidence handling', 'Threat assessment']
            )
        }
    
    def create_incident_management_plan(self, 
                                      organization_name: str,
                                      plan_version: str,
                                      compliance_requirements: List[str]) -> Dict[str, Any]:
        """
        Create comprehensive incident management plan
        """
        try:
            plan_id = f"{organization_name.lower().replace(' ', '_')}_incident_plan_v{plan_version}"
            
            # Create comprehensive incident management plan
            incident_plan = {
                'plan_id': plan_id,
                'organization_name': organization_name,
                'plan_version': plan_version,
                'created_date': datetime.utcnow().isoformat(),
                'last_updated': datetime.utcnow().isoformat(),
                'compliance_requirements': compliance_requirements,
                'plan_sections': {
                    'executive_summary': self._create_executive_summary(organization_name),
                    'incident_response_team': self._create_team_overview(),
                    'roles_and_responsibilities': self.response_roles,
                    'incident_classification': self.severity_definitions,
                    'response_phases': self.incident_phases,
                    'communication_plan': self._create_communication_plan(),
                    'escalation_procedures': self._create_escalation_procedures(),
                    'tools_and_resources': self._create_tools_resources(),
                    'training_requirements': self._create_training_requirements(),
                    'testing_and_exercises': self._create_testing_plan(),
                    'compliance_considerations': self._create_compliance_section(compliance_requirements)
                },
                'approval_status': 'draft',
                'next_review_date': (datetime.utcnow() + timedelta(days=365)).isoformat(),
                'ttl': int((datetime.utcnow() + timedelta(days=1095)).timestamp())  # 3 years
            }
            
            # Store plan in DynamoDB
            self.plans_table.put_item(Item=incident_plan)
            
            # Create associated playbooks
            playbook_results = self._create_incident_playbooks(plan_id)
            
            logger.info(f"Created incident management plan: {plan_id}")
            
            return {
                'status': 'success',
                'plan_id': plan_id,
                'plan_version': plan_version,
                'playbooks_created': len(playbook_results),
                'message': f"Successfully created incident management plan for {organization_name}"
            }
            
        except Exception as e:
            logger.error(f"Error creating incident management plan: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _create_executive_summary(self, organization_name: str) -> Dict[str, Any]:
        """
        Create executive summary section of the incident management plan
        """
        return {
            'purpose': f'This incident management plan establishes the framework for {organization_name} to effectively prepare for, respond to, and recover from security incidents in AWS cloud environments.',
            'scope': 'This plan covers all AWS workloads, applications, and infrastructure managed by the organization.',
            'objectives': [
                'Minimize the impact of security incidents on business operations',
                'Ensure rapid detection, containment, and recovery from security incidents',
                'Maintain compliance with regulatory and legal requirements',
                'Preserve evidence for forensic analysis and legal proceedings',
                'Continuously improve incident response capabilities through lessons learned'
            ],
            'success_metrics': [
                'Mean time to detection (MTTD) < 15 minutes for critical incidents',
                'Mean time to containment (MTTC) < 30 minutes for critical incidents',
                'Mean time to recovery (MTTR) < 4 hours for critical incidents',
                '99% incident response team availability during business hours',
                '100% compliance with regulatory notification requirements'
            ]
        }
    
    def _create_team_overview(self) -> Dict[str, Any]:
        """
        Create incident response team overview
        """
        return {
            'mission': 'To protect organizational assets and maintain business continuity through effective incident response',
            'goals': [
                'Rapid incident detection and response',
                'Minimization of business impact',
                'Preservation of evidence and forensic integrity',
                'Compliance with regulatory requirements',
                'Continuous improvement of security posture'
            ],
            'team_structure': {
                'core_team': ['Incident Commander', 'Incident Manager', 'Technical Lead', 'Security Analyst'],
                'extended_team': ['Communications Lead', 'Legal Counsel', 'HR Representative', 'Subject Matter Experts'],
                'external_partners': ['AWS Support', 'AWS CIRT', 'External Security Consultants', 'Law Enforcement']
            },
            'operating_model': {
                'availability': '24/7 on-call rotation for core team members',
                'escalation': 'Tiered escalation based on incident severity',
                'decision_making': 'Incident Commander has final authority during active incidents',
                'communication': 'Regular status updates and stakeholder briefings'
            }
        }

# Example usage
if __name__ == "__main__":
    # Initialize incident management plan manager
    plan_manager = IncidentManagementPlanManager()
    
    # Create incident management plan
    result = plan_manager.create_incident_management_plan(
        organization_name="Example Corporation",
        plan_version="1.0",
        compliance_requirements=["SOC 2", "PCI DSS", "GDPR", "HIPAA"]
    )
    
    print(f"Plan creation result: {json.dumps(result, indent=2)}")
```
### Example 2: RACI Matrix and Communication Plan Implementation

```python
# raci_communication_manager.py
import boto3
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@dataclass
class RACIAssignment:
    role: str
    responsible: bool
    accountable: bool
    consulted: bool
    informed: bool
    escalation_trigger: Optional[str]
    decision_authority: List[str]

@dataclass
class CommunicationChannel:
    channel_name: str
    channel_type: str  # email, sms, phone, slack, teams
    primary_contact: str
    backup_contact: Optional[str]
    availability: str
    encryption_required: bool
    retention_period: str

class RACICommunicationManager:
    """
    Manages RACI matrix and communication plans for incident response
    """
    
    def __init__(self, region: str = 'us-east-1'):
        self.region = region
        self.dynamodb = boto3.resource('dynamodb', region_name=region)
        self.sns_client = boto3.client('sns', region_name=region)
        
        # DynamoDB tables
        self.raci_table = self.dynamodb.Table('incident-raci-matrix')
        self.communication_table = self.dynamodb.Table('incident-communication-plans')
    
    def create_raci_matrix(self, incident_type: str, activities: List[str]) -> Dict[str, Any]:
        """
        Create RACI matrix for specific incident type and activities
        """
        try:
            # Define RACI assignments for different incident activities
            raci_matrix = {
                'incident_type': incident_type,
                'created_date': datetime.utcnow().isoformat(),
                'activities': {}
            }
            
            # Standard RACI assignments for common incident activities
            standard_assignments = {
                'incident_declaration': {
                    'incident_commander': RACIAssignment('Incident Commander', False, True, False, False, None, ['Declare incident', 'Set severity']),
                    'security_analyst': RACIAssignment('Security Analyst', True, False, False, False, 'Confirmed threat', ['Initial assessment']),
                    'technical_lead': RACIAssignment('Technical Lead', False, False, True, False, None, []),
                    'communications_lead': RACIAssignment('Communications Lead', False, False, False, True, None, []),
                    'executive_team': RACIAssignment('Executive Team', False, False, False, True, 'Critical severity', [])
                },
                'technical_investigation': {
                    'technical_lead': RACIAssignment('Technical Lead', False, True, False, False, None, ['Investigation approach', 'Resource allocation']),
                    'security_analyst': RACIAssignment('Security Analyst', True, False, False, False, None, ['Evidence collection', 'Analysis']),
                    'system_administrators': RACIAssignment('System Administrators', True, False, False, False, None, ['System access', 'Log collection']),
                    'incident_commander': RACIAssignment('Incident Commander', False, False, True, False, None, []),
                    'legal_counsel': RACIAssignment('Legal Counsel', False, False, True, True, 'Evidence preservation', ['Legal guidance'])
                },
                'containment_actions': {
                    'incident_commander': RACIAssignment('Incident Commander', False, True, False, False, None, ['Containment authorization', 'Business impact decisions']),
                    'technical_lead': RACIAssignment('Technical Lead', True, False, False, False, None, ['Technical containment', 'System isolation']),
                    'security_analyst': RACIAssignment('Security Analyst', True, False, False, False, None, ['Security controls', 'Threat mitigation']),
                    'system_administrators': RACIAssignment('System Administrators', True, False, False, False, None, ['System changes', 'Access revocation']),
                    'business_owners': RACIAssignment('Business Owners', False, False, True, True, 'Service impact', [])
                },
                'external_communication': {
                    'communications_lead': RACIAssignment('Communications Lead', False, True, False, False, None, ['External messaging', 'Media relations']),
                    'incident_commander': RACIAssignment('Incident Commander', False, False, True, False, None, []),
                    'legal_counsel': RACIAssignment('Legal Counsel', True, False, False, False, 'Regulatory requirements', ['Legal review', 'Compliance']),
                    'executive_team': RACIAssignment('Executive Team', False, False, True, True, 'Public disclosure', ['Strategic decisions']),
                    'public_relations': RACIAssignment('Public Relations', True, False, False, False, None, ['Media statements', 'Public communications'])
                },
                'recovery_operations': {
                    'technical_lead': RACIAssignment('Technical Lead', False, True, False, False, None, ['Recovery planning', 'System restoration']),
                    'system_administrators': RACIAssignment('System Administrators', True, False, False, False, None, ['System recovery', 'Service restoration']),
                    'security_analyst': RACIAssignment('Security Analyst', False, False, True, False, None, []),
                    'business_owners': RACIAssignment('Business Owners', False, False, True, True, 'Service validation', ['Business validation']),
                    'incident_commander': RACIAssignment('Incident Commander', False, False, True, False, None, [])
                }
            }
            
            # Apply standard assignments to requested activities
            for activity in activities:
                if activity in standard_assignments:
                    raci_matrix['activities'][activity] = {
                        role: asdict(assignment) for role, assignment in standard_assignments[activity].items()
                    }
            
            # Store RACI matrix
            matrix_id = f"{incident_type.lower().replace(' ', '_')}_raci_matrix"
            raci_matrix['matrix_id'] = matrix_id
            
            self.raci_table.put_item(Item=raci_matrix)
            
            return {
                'status': 'success',
                'matrix_id': matrix_id,
                'activities_covered': len(raci_matrix['activities']),
                'message': f"Successfully created RACI matrix for {incident_type}"
            }
            
        except Exception as e:
            logger.error(f"Error creating RACI matrix: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def create_communication_plan(self, 
                                plan_name: str,
                                incident_types: List[str],
                                stakeholder_groups: List[str]) -> Dict[str, Any]:
        """
        Create comprehensive communication plan for incident response
        """
        try:
            # Define communication channels
            communication_channels = [
                CommunicationChannel(
                    channel_name='Primary Email',
                    channel_type='email',
                    primary_contact='incident-response@company.com',
                    backup_contact='security-team@company.com',
                    availability='24/7',
                    encryption_required=True,
                    retention_period='7 years'
                ),
                CommunicationChannel(
                    channel_name='Emergency SMS',
                    channel_type='sms',
                    primary_contact='+1-555-INCIDENT',
                    backup_contact='+1-555-SECURITY',
                    availability='24/7',
                    encryption_required=False,
                    retention_period='1 year'
                ),
                CommunicationChannel(
                    channel_name='Incident Slack Channel',
                    channel_type='slack',
                    primary_contact='#incident-response',
                    backup_contact='#security-alerts',
                    availability='24/7',
                    encryption_required=True,
                    retention_period='2 years'
                ),
                CommunicationChannel(
                    channel_name='Executive Hotline',
                    channel_type='phone',
                    primary_contact='+1-555-EXEC-HOTLINE',
                    backup_contact='+1-555-EXEC-BACKUP',
                    availability='24/7',
                    encryption_required=False,
                    retention_period='1 year'
                ),
                CommunicationChannel(
                    channel_name='Secure Video Conference',
                    channel_type='video',
                    primary_contact='https://company.zoom.us/incident-room',
                    backup_contact='https://company.teams.com/incident-backup',
                    availability='24/7',
                    encryption_required=True,
                    retention_period='90 days'
                )
            ]
            
            # Define stakeholder communication requirements
            stakeholder_communication = {
                'internal_stakeholders': {
                    'executive_team': {
                        'notification_triggers': ['Critical incidents', 'High-impact incidents', 'Regulatory implications'],
                        'communication_frequency': 'Every 30 minutes for critical, hourly for high',
                        'preferred_channels': ['phone', 'email', 'video'],
                        'information_level': 'Executive summary with business impact',
                        'escalation_criteria': 'No response within 15 minutes'
                    },
                    'incident_response_team': {
                        'notification_triggers': ['All incidents'],
                        'communication_frequency': 'Real-time updates',
                        'preferred_channels': ['slack', 'email', 'sms'],
                        'information_level': 'Full technical details',
                        'escalation_criteria': 'No acknowledgment within 5 minutes'
                    },
                    'business_owners': {
                        'notification_triggers': ['Incidents affecting their services'],
                        'communication_frequency': 'Hourly updates during active incidents',
                        'preferred_channels': ['email', 'phone'],
                        'information_level': 'Business impact and recovery timeline',
                        'escalation_criteria': 'Service impact exceeds 2 hours'
                    },
                    'legal_department': {
                        'notification_triggers': ['Data breaches', 'Regulatory violations', 'Law enforcement involvement'],
                        'communication_frequency': 'Immediate notification, then as needed',
                        'preferred_channels': ['phone', 'secure_email'],
                        'information_level': 'Legal implications and compliance requirements',
                        'escalation_criteria': 'Regulatory notification required'
                    }
                },
                'external_stakeholders': {
                    'customers': {
                        'notification_triggers': ['Service outages', 'Data breaches affecting customer data'],
                        'communication_frequency': 'Initial notification within 1 hour, updates every 2 hours',
                        'preferred_channels': ['email', 'website', 'social_media'],
                        'information_level': 'Service impact and expected resolution time',
                        'escalation_criteria': 'Outage exceeds 4 hours'
                    },
                    'regulators': {
                        'notification_triggers': ['Data breaches', 'Compliance violations'],
                        'communication_frequency': 'As required by regulation',
                        'preferred_channels': ['official_portal', 'certified_mail'],
                        'information_level': 'Regulatory compliance details',
                        'escalation_criteria': 'Regulatory deadline approaching'
                    },
                    'aws_support': {
                        'notification_triggers': ['AWS service issues', 'Infrastructure incidents'],
                        'communication_frequency': 'Immediate for critical, within 1 hour for high',
                        'preferred_channels': ['support_case', 'phone'],
                        'information_level': 'Technical details and AWS resource impact',
                        'escalation_criteria': 'No response within SLA'
                    },
                    'media': {
                        'notification_triggers': ['Public incidents', 'Regulatory disclosures'],
                        'communication_frequency': 'As needed based on incident visibility',
                        'preferred_channels': ['press_release', 'media_briefing'],
                        'information_level': 'Public-appropriate incident summary',
                        'escalation_criteria': 'Media inquiry received'
                    }
                }
            }
            
            # Create communication templates
            communication_templates = {
                'initial_notification': {
                    'subject': 'INCIDENT ALERT: {severity} - {incident_type}',
                    'body': '''
INCIDENT NOTIFICATION

Incident ID: {incident_id}
Severity: {severity}
Type: {incident_type}
Detected: {detection_time}
Status: {current_status}

Initial Assessment:
{initial_assessment}

Affected Systems:
{affected_systems}

Next Update: {next_update_time}

Incident Commander: {incident_commander}
Contact: {commander_contact}
                    '''
                },
                'status_update': {
                    'subject': 'INCIDENT UPDATE: {incident_id} - {current_status}',
                    'body': '''
INCIDENT STATUS UPDATE

Incident ID: {incident_id}
Current Status: {current_status}
Last Update: {update_time}

Progress Summary:
{progress_summary}

Actions Completed:
{completed_actions}

Next Steps:
{next_steps}

Estimated Resolution: {estimated_resolution}

Next Update: {next_update_time}
                    '''
                },
                'resolution_notification': {
                    'subject': 'INCIDENT RESOLVED: {incident_id}',
                    'body': '''
INCIDENT RESOLUTION

Incident ID: {incident_id}
Resolution Time: {resolution_time}
Total Duration: {total_duration}

Resolution Summary:
{resolution_summary}

Root Cause:
{root_cause}

Preventive Measures:
{preventive_measures}

Post-Incident Review: {pir_scheduled}
                    '''
                }
            }
            
            # Create comprehensive communication plan
            communication_plan = {
                'plan_id': f"{plan_name.lower().replace(' ', '_')}_comm_plan",
                'plan_name': plan_name,
                'incident_types': incident_types,
                'stakeholder_groups': stakeholder_groups,
                'created_date': datetime.utcnow().isoformat(),
                'communication_channels': [asdict(channel) for channel in communication_channels],
                'stakeholder_communication': stakeholder_communication,
                'communication_templates': communication_templates,
                'escalation_matrix': self._create_escalation_matrix(),
                'backup_procedures': self._create_backup_communication_procedures(),
                'compliance_requirements': self._create_communication_compliance_requirements()
            }
            
            # Store communication plan
            self.communication_table.put_item(Item=communication_plan)
            
            return {
                'status': 'success',
                'plan_id': communication_plan['plan_id'],
                'channels_configured': len(communication_channels),
                'stakeholder_groups': len(stakeholder_groups),
                'message': f"Successfully created communication plan: {plan_name}"
            }
            
        except Exception as e:
            logger.error(f"Error creating communication plan: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _create_escalation_matrix(self) -> Dict[str, Any]:
        """
        Create escalation matrix for communication failures
        """
        return {
            'level_1': {
                'trigger': 'No acknowledgment within 5 minutes',
                'action': 'Escalate to backup contact',
                'notification_methods': ['sms', 'phone']
            },
            'level_2': {
                'trigger': 'No acknowledgment within 15 minutes',
                'action': 'Escalate to manager',
                'notification_methods': ['phone', 'emergency_contact']
            },
            'level_3': {
                'trigger': 'No acknowledgment within 30 minutes',
                'action': 'Escalate to executive team',
                'notification_methods': ['executive_hotline', 'emergency_broadcast']
            },
            'level_4': {
                'trigger': 'No acknowledgment within 60 minutes',
                'action': 'Activate emergency procedures',
                'notification_methods': ['all_available_channels', 'physical_notification']
            }
        }
    
    def _create_backup_communication_procedures(self) -> Dict[str, Any]:
        """
        Create backup communication procedures for system failures
        """
        return {
            'primary_system_failure': {
                'backup_channels': ['personal_phones', 'external_email', 'physical_meeting'],
                'rally_point': 'Emergency operations center',
                'contact_method': 'Phone tree activation'
            },
            'network_outage': {
                'backup_channels': ['cellular_phones', 'satellite_communication', 'radio'],
                'rally_point': 'Alternate facility',
                'contact_method': 'Out-of-band communication'
            },
            'facility_evacuation': {
                'backup_channels': ['mobile_devices', 'remote_access'],
                'rally_point': 'Designated remote location',
                'contact_method': 'Emergency contact system'
            }
        }
    
    def _create_communication_compliance_requirements(self) -> Dict[str, Any]:
        """
        Create communication compliance requirements
        """
        return {
            'data_retention': {
                'incident_communications': '7 years',
                'regulatory_notifications': '10 years',
                'customer_communications': '5 years'
            },
            'encryption_requirements': {
                'internal_communications': 'TLS 1.2 minimum',
                'external_communications': 'End-to-end encryption',
                'regulatory_communications': 'Government-approved encryption'
            },
            'notification_timelines': {
                'gdpr_breach_notification': '72 hours to regulator, 30 days to individuals',
                'hipaa_breach_notification': '60 days to HHS, immediate to individuals',
                'pci_dss_incident': 'Immediate to card brands and acquirer'
            }
        }

# Example usage
if __name__ == "__main__":
    # Initialize RACI and communication manager
    raci_comm_manager = RACICommunicationManager()
    
    # Create RACI matrix
    raci_result = raci_comm_manager.create_raci_matrix(
        incident_type="Security Breach",
        activities=["incident_declaration", "technical_investigation", "containment_actions", "external_communication", "recovery_operations"]
    )
    print(f"RACI matrix result: {json.dumps(raci_result, indent=2)}")
    
    # Create communication plan
    comm_result = raci_comm_manager.create_communication_plan(
        plan_name="Enterprise Security Incident Communication Plan",
        incident_types=["Security Breach", "Data Loss", "System Outage", "Malware Infection"],
        stakeholder_groups=["Executive Team", "IT Operations", "Legal", "Customers", "Regulators"]
    )
    print(f"Communication plan result: {json.dumps(comm_result, indent=2)}")
```
## Resources

### Related Best Practices

- [SEC04 Detection](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/detection.html)
- [SEC10-BP01 Identify key personnel and external resources](./SEC10-BP01.html)

### Related Documents

- [AWS Security Incident Response Guide](https://docs.aws.amazon.com/whitepapers/latest/aws-security-incident-response-guide/aws-security-incident-response-guide.html)
- [NIST: Computer Security Incident Handling Guide](https://csrc.nist.gov/publications/detail/sp/800-61/rev-2/final)
- [AWS Shared Responsibility Model](https://aws.amazon.com/compliance/shared-responsibility-model/)
- [AWS Systems Manager Incident Manager User Guide](https://docs.aws.amazon.com/incident-manager/latest/userguide/what-is-incident-manager.html)

### Related AWS Services

- [AWS Systems Manager Incident Manager](https://docs.aws.amazon.com/incident-manager/latest/userguide/what-is-incident-manager.html)
- [AWS Support](https://aws.amazon.com/support/)
- [AWS Shield](https://aws.amazon.com/shield/)
- [AWS Managed Services](https://aws.amazon.com/managed-services/)
- [AWS Security Hub](https://aws.amazon.com/security-hub/)
- [Amazon GuardDuty](https://aws.amazon.com/guardduty/)

### Related Examples

- [AWS Customer Playbook Framework](https://github.com/aws-samples/aws-customer-playbook-framework)
- [AWS Security Incident Response Runbooks](https://github.com/aws-samples/aws-incident-response-runbooks)
- [Incident Response Playbook Templates](https://docs.aws.amazon.com/incident-manager/latest/userguide/tutorials.html)

### Related Tools

- [AWS CloudTrail](https://aws.amazon.com/cloudtrail/) - For audit logging and forensic analysis
- [Amazon Detective](https://aws.amazon.com/detective/) - For security investigation and analysis
- [AWS Config](https://aws.amazon.com/config/) - For configuration compliance and change tracking
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/) - For monitoring and alerting

### Compliance Frameworks

- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [ISO 27035 - Information Security Incident Management](https://www.iso.org/standard/60803.html)
- [SANS Incident Response Process](https://www.sans.org/white-papers/504/)
- [FedRAMP Incident Response Requirements](https://www.fedramp.gov/assets/resources/documents/CSP_Incident_Communications_Procedures.pdf)
