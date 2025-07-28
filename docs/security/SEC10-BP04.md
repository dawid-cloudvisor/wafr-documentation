---
title: "SEC10-BP04: Develop and test security incident response playbooks"
layout: default
parent: "SEC10 - How do you anticipate, respond to, and recover from incidents?"
grand_parent: Security
nav_order: 4
---

# SEC10-BP04: Develop and test security incident response playbooks

## Overview

A key part of preparing your incident response processes is developing playbooks. Incident response playbooks provide prescriptive guidance and steps to follow when a security event occurs. Having clear structure and steps simplifies the response and reduces the likelihood for human error.

**Level of risk exposed if this best practice is not established:** Medium

## Implementation Guidance

Playbooks should be created for incident scenarios such as:

**Expected incidents:** Playbooks should be created for incidents you anticipate. This includes threats like denial of service (DoS), ransomware, and credential compromise.

**Known security findings or alerts:** Playbooks should be created to address your known security findings and alerts, such as those from Amazon GuardDuty. When you receive a GuardDuty finding, the playbook should provide clear steps to prevent mishandling or ignoring the alert. For more remediation details and guidance, see [Remediating security issues discovered by GuardDuty](https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_remediate.html).

Playbooks should contain technical steps for a security analyst to complete in order to adequately investigate and respond to a potential security incident.

## Implementation Steps

Items to include in a playbook include:

- **Playbook overview:** What risk or incident scenario does this playbook address? What is the goal of the playbook?
- **Prerequisites:** What logs, detection mechanisms, and automated tools are required for this incident scenario? What is the expected notification?
- **Communication and escalation information:** Who is involved and what is their contact information? What are each of the stakeholders' responsibilities?
- **Response steps:** Across phases of incident response, what tactical steps should be taken? What queries should an analyst run? What code should be run to achieve the desired outcome?
  - **Detect:** How will the incident be detected?
  - **Analyze:** How will the scope of impact be determined?
  - **Contain:** How will the incident be isolated to limit scope?
  - **Eradicate:** How will the threat be removed from the environment?
  - **Recover:** How will the affected system or resource be brought back into production?
- **Expected outcomes:** After queries and code are run, what is the expected result of the playbook?
## Implementation Examples

### Example 1: Comprehensive Incident Response Playbook Framework

```python
# incident_response_playbooks.py
import boto3
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
import logging
import yaml

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IncidentType(Enum):
    CREDENTIAL_COMPROMISE = "credential_compromise"
    RANSOMWARE = "ransomware"
    DATA_EXFILTRATION = "data_exfiltration"
    DOS_ATTACK = "dos_attack"
    MALWARE_INFECTION = "malware_infection"
    UNAUTHORIZED_ACCESS = "unauthorized_access"
    GUARDDUTY_FINDING = "guardduty_finding"
    CONFIG_VIOLATION = "config_violation"

class PlaybookPhase(Enum):
    DETECT = "detect"
    ANALYZE = "analyze"
    CONTAIN = "contain"
    ERADICATE = "eradicate"
    RECOVER = "recover"
    POST_INCIDENT = "post_incident"

@dataclass
class PlaybookStep:
    step_id: str
    phase: PlaybookPhase
    title: str
    description: str
    prerequisites: List[str]
    actions: List[Dict[str, Any]]
    expected_outcome: str
    automation_available: bool
    estimated_duration: str
    required_permissions: List[str]
    tools_required: List[str]

@dataclass
class IncidentPlaybook:
    playbook_id: str
    incident_type: IncidentType
    title: str
    description: str
    severity_levels: List[str]
    prerequisites: List[str]
    stakeholders: List[Dict[str, str]]
    communication_plan: Dict[str, Any]
    response_steps: List[PlaybookStep]
    automation_runbooks: List[str]
    testing_procedures: List[str]
    last_updated: str
    version: str

class IncidentResponsePlaybookManager:
    """
    Comprehensive incident response playbook management system
    """
    
    def __init__(self, region: str = 'us-east-1'):
        self.region = region
        self.dynamodb = boto3.resource('dynamodb', region_name=region)
        self.ssm_client = boto3.client('ssm', region_name=region)
        self.lambda_client = boto3.client('lambda', region_name=region)
        self.s3_client = boto3.client('s3', region_name=region)
        
        # DynamoDB tables for playbook management
        self.playbooks_table = self.dynamodb.Table('incident-response-playbooks')
        self.executions_table = self.dynamodb.Table('playbook-executions')
        self.testing_table = self.dynamodb.Table('playbook-testing-results')
        
        # Initialize playbook templates
        self.playbook_templates = self._create_playbook_templates()
    
    def _create_playbook_templates(self) -> Dict[str, IncidentPlaybook]:
        """
        Create comprehensive incident response playbook templates
        """
        playbooks = {}
        
        # Credential Compromise Playbook
        credential_compromise_steps = [
            PlaybookStep(
                step_id="detect_001",
                phase=PlaybookPhase.DETECT,
                title="Identify Compromised Credentials",
                description="Detect signs of credential compromise through monitoring and alerts",
                prerequisites=["CloudTrail enabled", "GuardDuty active", "Unusual API activity alerts"],
                actions=[
                    {
                        "type": "query",
                        "service": "cloudtrail",
                        "query": "SELECT * FROM cloudtrail_logs WHERE errorCode = 'SigninFailure' AND sourceIPAddress NOT IN (known_ip_ranges) ORDER BY eventTime DESC LIMIT 100"
                    },
                    {
                        "type": "api_call",
                        "service": "guardduty",
                        "action": "list_findings",
                        "parameters": {"FindingCriteria": {"Criterion": {"type": {"Eq": ["UnauthorizedAPICall"]}}}}
                    }
                ],
                expected_outcome="List of suspicious authentication events and potential credential compromise indicators",
                automation_available=True,
                estimated_duration="15 minutes",
                required_permissions=["cloudtrail:LookupEvents", "guardduty:ListFindings"],
                tools_required=["AWS CLI", "CloudTrail Insights", "GuardDuty Console"]
            ),
            PlaybookStep(
                step_id="analyze_001",
                phase=PlaybookPhase.ANALYZE,
                title="Assess Scope of Compromise",
                description="Determine which credentials are compromised and what actions were taken",
                prerequisites=["Suspicious activity identified", "CloudTrail logs available"],
                actions=[
                    {
                        "type": "investigation",
                        "description": "Analyze user activity patterns for compromised account",
                        "query": "SELECT eventName, sourceIPAddress, userAgent, eventTime FROM cloudtrail_logs WHERE userIdentity.userName = '{compromised_user}' AND eventTime > '{incident_start_time}' ORDER BY eventTime"
                    },
                    {
                        "type": "api_call",
                        "service": "iam",
                        "action": "get_account_authorization_details",
                        "description": "Review current permissions and recent changes"
                    }
                ],
                expected_outcome="Complete timeline of compromised account activity and impact assessment",
                automation_available=True,
                estimated_duration="30 minutes",
                required_permissions=["iam:GetAccountAuthorizationDetails", "cloudtrail:LookupEvents"],
                tools_required=["AWS CLI", "CloudTrail Console", "Detective"]
            ),
            PlaybookStep(
                step_id="contain_001",
                phase=PlaybookPhase.CONTAIN,
                title="Disable Compromised Credentials",
                description="Immediately disable compromised user accounts and access keys",
                prerequisites=["Compromised credentials identified", "IAM admin permissions"],
                actions=[
                    {
                        "type": "api_call",
                        "service": "iam",
                        "action": "update_login_profile",
                        "parameters": {"UserName": "{compromised_user}", "PasswordResetRequired": True}
                    },
                    {
                        "type": "api_call",
                        "service": "iam",
                        "action": "update_access_key",
                        "parameters": {"UserName": "{compromised_user}", "AccessKeyId": "{access_key_id}", "Status": "Inactive"}
                    },
                    {
                        "type": "api_call",
                        "service": "iam",
                        "action": "attach_user_policy",
                        "parameters": {"UserName": "{compromised_user}", "PolicyArn": "arn:aws:iam::aws:policy/AWSDenyAll"}
                    }
                ],
                expected_outcome="Compromised credentials disabled and account access blocked",
                automation_available=True,
                estimated_duration="10 minutes",
                required_permissions=["iam:UpdateLoginProfile", "iam:UpdateAccessKey", "iam:AttachUserPolicy"],
                tools_required=["AWS CLI", "IAM Console"]
            ),
            PlaybookStep(
                step_id="eradicate_001",
                phase=PlaybookPhase.ERADICATE,
                title="Remove Unauthorized Changes",
                description="Revert any unauthorized changes made by compromised credentials",
                prerequisites=["Unauthorized changes identified", "Admin permissions"],
                actions=[
                    {
                        "type": "review_and_revert",
                        "description": "Review and revert unauthorized IAM policy changes",
                        "query": "SELECT * FROM cloudtrail_logs WHERE eventName LIKE '%Policy%' AND userIdentity.userName = '{compromised_user}'"
                    },
                    {
                        "type": "api_call",
                        "service": "ec2",
                        "action": "describe_security_groups",
                        "description": "Review security group changes and revert unauthorized modifications"
                    }
                ],
                expected_outcome="All unauthorized changes reverted and systems restored to secure state",
                automation_available=False,
                estimated_duration="45 minutes",
                required_permissions=["iam:*", "ec2:*", "s3:*"],
                tools_required=["AWS CLI", "AWS Console", "CloudTrail"]
            ),
            PlaybookStep(
                step_id="recover_001",
                phase=PlaybookPhase.RECOVER,
                title="Restore Legitimate Access",
                description="Restore legitimate user access with new credentials",
                prerequisites=["Threat eradicated", "User identity verified"],
                actions=[
                    {
                        "type": "api_call",
                        "service": "iam",
                        "action": "create_access_key",
                        "parameters": {"UserName": "{compromised_user}"}
                    },
                    {
                        "type": "api_call",
                        "service": "iam",
                        "action": "detach_user_policy",
                        "parameters": {"UserName": "{compromised_user}", "PolicyArn": "arn:aws:iam::aws:policy/AWSDenyAll"}
                    },
                    {
                        "type": "notification",
                        "description": "Notify user of credential reset and provide new access instructions"
                    }
                ],
                expected_outcome="User access restored with new credentials and enhanced monitoring",
                automation_available=True,
                estimated_duration="20 minutes",
                required_permissions=["iam:CreateAccessKey", "iam:DetachUserPolicy"],
                tools_required=["AWS CLI", "IAM Console", "Communication tools"]
            )
        ]
        
        playbooks[IncidentType.CREDENTIAL_COMPROMISE.value] = IncidentPlaybook(
            playbook_id="pb_credential_compromise_v1",
            incident_type=IncidentType.CREDENTIAL_COMPROMISE,
            title="AWS Credential Compromise Response",
            description="Comprehensive playbook for responding to compromised AWS credentials",
            severity_levels=["High", "Critical"],
            prerequisites=[
                "CloudTrail logging enabled",
                "GuardDuty active",
                "IAM administrative access",
                "Incident response team activated"
            ],
            stakeholders=[
                {"role": "Incident Commander", "contact": "commander@company.com"},
                {"role": "Security Analyst", "contact": "security@company.com"},
                {"role": "IAM Administrator", "contact": "iam-admin@company.com"}
            ],
            communication_plan={
                "initial_notification": "Immediate notification to security team and affected user",
                "escalation_criteria": "If compromise affects privileged accounts or multiple users",
                "update_frequency": "Every 30 minutes during active response"
            },
            response_steps=credential_compromise_steps,
            automation_runbooks=["credential-compromise-containment", "unauthorized-change-detection"],
            testing_procedures=["Quarterly tabletop exercise", "Annual red team simulation"],
            last_updated=datetime.utcnow().isoformat(),
            version="1.0"
        )
        
        # GuardDuty Finding Playbook
        guardduty_steps = [
            PlaybookStep(
                step_id="detect_gd_001",
                phase=PlaybookPhase.DETECT,
                title="Process GuardDuty Finding",
                description="Receive and categorize GuardDuty security finding",
                prerequisites=["GuardDuty enabled", "Finding notification received"],
                actions=[
                    {
                        "type": "api_call",
                        "service": "guardduty",
                        "action": "get_findings",
                        "parameters": {"DetectorId": "{detector_id}", "FindingIds": ["{finding_id}"]}
                    },
                    {
                        "type": "categorization",
                        "description": "Categorize finding by type and severity",
                        "categories": ["Reconnaissance", "Instance Compromise", "Cryptocurrency Mining", "Malware", "Data Exfiltration"]
                    }
                ],
                expected_outcome="GuardDuty finding details retrieved and categorized",
                automation_available=True,
                estimated_duration="5 minutes",
                required_permissions=["guardduty:GetFindings"],
                tools_required=["GuardDuty Console", "AWS CLI"]
            ),
            PlaybookStep(
                step_id="analyze_gd_001",
                phase=PlaybookPhase.ANALYZE,
                title="Investigate GuardDuty Finding",
                description="Analyze the finding to determine legitimacy and impact",
                prerequisites=["Finding details available", "CloudTrail access"],
                actions=[
                    {
                        "type": "investigation",
                        "description": "Correlate finding with CloudTrail events",
                        "query": "SELECT * FROM cloudtrail_logs WHERE sourceIPAddress = '{finding_source_ip}' AND eventTime BETWEEN '{finding_start_time}' AND '{finding_end_time}'"
                    },
                    {
                        "type": "threat_intelligence",
                        "description": "Check IP reputation and threat intelligence feeds",
                        "sources": ["VirusTotal", "AbuseIPDB", "AWS Threat Intelligence"]
                    }
                ],
                expected_outcome="Finding validated as true/false positive with impact assessment",
                automation_available=True,
                estimated_duration="20 minutes",
                required_permissions=["cloudtrail:LookupEvents", "guardduty:GetThreatIntelSet"],
                tools_required=["CloudTrail", "Detective", "Threat Intelligence Tools"]
            ),
            PlaybookStep(
                step_id="contain_gd_001",
                phase=PlaybookPhase.CONTAIN,
                title="Contain Threat Based on Finding Type",
                description="Apply appropriate containment measures based on GuardDuty finding type",
                prerequisites=["Finding validated as true positive", "Admin permissions"],
                actions=[
                    {
                        "type": "conditional_action",
                        "conditions": {
                            "UnauthorizedAPICall": [
                                {"action": "disable_access_key", "target": "{compromised_access_key}"},
                                {"action": "isolate_instance", "target": "{affected_instance}"}
                            ],
                            "CryptoCurrency": [
                                {"action": "stop_instance", "target": "{mining_instance}"},
                                {"action": "block_network_access", "target": "{mining_instance}"}
                            ],
                            "Malware": [
                                {"action": "isolate_instance", "target": "{infected_instance}"},
                                {"action": "create_forensic_snapshot", "target": "{infected_instance}"}
                            ]
                        }
                    }
                ],
                expected_outcome="Threat contained based on finding type with minimal business impact",
                automation_available=True,
                estimated_duration="15 minutes",
                required_permissions=["ec2:*", "iam:*", "vpc:*"],
                tools_required=["AWS CLI", "EC2 Console", "VPC Console"]
            )
        ]
        
        playbooks[IncidentType.GUARDDUTY_FINDING.value] = IncidentPlaybook(
            playbook_id="pb_guardduty_finding_v1",
            incident_type=IncidentType.GUARDDUTY_FINDING,
            title="GuardDuty Finding Response",
            description="Standardized response procedures for GuardDuty security findings",
            severity_levels=["Low", "Medium", "High"],
            prerequisites=[
                "GuardDuty enabled and configured",
                "CloudTrail logging active",
                "Automated finding notifications configured"
            ],
            stakeholders=[
                {"role": "Security Analyst", "contact": "security@company.com"},
                {"role": "SOC Manager", "contact": "soc-manager@company.com"},
                {"role": "Cloud Operations", "contact": "cloudops@company.com"}
            ],
            communication_plan={
                "initial_notification": "Automated notification to SOC team",
                "escalation_criteria": "High severity findings or confirmed true positives",
                "update_frequency": "Every hour for active investigations"
            },
            response_steps=guardduty_steps,
            automation_runbooks=["guardduty-finding-processor", "threat-containment-automation"],
            testing_procedures=["Monthly finding simulation", "Quarterly response drill"],
            last_updated=datetime.utcnow().isoformat(),
            version="1.0"
        )
        
        return playbooks
    
    def create_playbook(self, playbook: IncidentPlaybook) -> Dict[str, Any]:
        """
        Create and store incident response playbook
        """
        try:
            # Store playbook in DynamoDB
            playbook_item = asdict(playbook)
            playbook_item['created_at'] = datetime.utcnow().isoformat()
            playbook_item['ttl'] = int((datetime.utcnow() + timedelta(days=1095)).timestamp())  # 3 years
            
            self.playbooks_table.put_item(Item=playbook_item)
            
            # Create automation runbooks if specified
            automation_results = []
            for runbook_name in playbook.automation_runbooks:
                automation_result = self._create_automation_runbook(runbook_name, playbook)
                automation_results.append(automation_result)
            
            logger.info(f"Created playbook: {playbook.playbook_id}")
            
            return {
                'status': 'success',
                'playbook_id': playbook.playbook_id,
                'automation_runbooks': len(automation_results),
                'message': f"Successfully created playbook for {playbook.incident_type.value}"
            }
            
        except Exception as e:
            logger.error(f"Error creating playbook: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def execute_playbook(self, 
                        playbook_id: str,
                        incident_id: str,
                        incident_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute incident response playbook with given context
        """
        try:
            # Retrieve playbook
            response = self.playbooks_table.get_item(Key={'playbook_id': playbook_id})
            if 'Item' not in response:
                return {
                    'status': 'error',
                    'message': f'Playbook {playbook_id} not found'
                }
            
            playbook_data = response['Item']
            execution_id = f"{incident_id}_{playbook_id}_{int(datetime.utcnow().timestamp())}"
            
            # Execute playbook steps
            execution_results = []
            for step_data in playbook_data['response_steps']:
                step_result = self._execute_playbook_step(step_data, incident_context)
                execution_results.append(step_result)
                
                # Stop execution if critical step fails
                if step_result['status'] == 'failed' and step_data.get('critical', False):
                    break
            
            # Record execution
            execution_record = {
                'execution_id': execution_id,
                'playbook_id': playbook_id,
                'incident_id': incident_id,
                'executed_at': datetime.utcnow().isoformat(),
                'incident_context': incident_context,
                'execution_results': execution_results,
                'status': 'completed' if all(r['status'] == 'success' for r in execution_results) else 'partial',
                'ttl': int((datetime.utcnow() + timedelta(days=365)).timestamp())
            }
            
            self.executions_table.put_item(Item=execution_record)
            
            successful_steps = sum(1 for result in execution_results if result['status'] == 'success')
            
            return {
                'status': 'success',
                'execution_id': execution_id,
                'playbook_id': playbook_id,
                'total_steps': len(execution_results),
                'successful_steps': successful_steps,
                'execution_results': execution_results
            }
            
        except Exception as e:
            logger.error(f"Error executing playbook: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def test_playbook(self, 
                     playbook_id: str,
                     test_scenario: Dict[str, Any]) -> Dict[str, Any]:
        """
        Test incident response playbook with simulated scenario
        """
        try:
            test_id = f"test_{playbook_id}_{int(datetime.utcnow().timestamp())}"
            
            # Execute playbook in test mode
            test_execution = self.execute_playbook(
                playbook_id=playbook_id,
                incident_id=f"TEST_{test_id}",
                incident_context=test_scenario
            )
            
            # Analyze test results
            test_analysis = self._analyze_test_results(test_execution, test_scenario)
            
            # Record test results
            test_record = {
                'test_id': test_id,
                'playbook_id': playbook_id,
                'test_scenario': test_scenario,
                'test_execution': test_execution,
                'test_analysis': test_analysis,
                'tested_at': datetime.utcnow().isoformat(),
                'ttl': int((datetime.utcnow() + timedelta(days=365)).timestamp())
            }
            
            self.testing_table.put_item(Item=test_record)
            
            return {
                'status': 'success',
                'test_id': test_id,
                'playbook_id': playbook_id,
                'test_results': test_analysis,
                'recommendations': test_analysis.get('recommendations', [])
            }
            
        except Exception as e:
            logger.error(f"Error testing playbook: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _execute_playbook_step(self, step_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute individual playbook step
        """
        try:
            step_id = step_data['step_id']
            
            # Check prerequisites
            prerequisites_met = self._check_prerequisites(step_data.get('prerequisites', []), context)
            if not prerequisites_met['all_met']:
                return {
                    'step_id': step_id,
                    'status': 'failed',
                    'message': f"Prerequisites not met: {prerequisites_met['missing']}"
                }
            
            # Execute actions
            action_results = []
            for action in step_data.get('actions', []):
                action_result = self._execute_action(action, context)
                action_results.append(action_result)
            
            # Determine step success
            step_success = all(result.get('success', False) for result in action_results)
            
            return {
                'step_id': step_id,
                'status': 'success' if step_success else 'failed',
                'action_results': action_results,
                'execution_time': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            return {
                'step_id': step_data.get('step_id', 'unknown'),
                'status': 'error',
                'message': str(e)
            }
    
    def _execute_action(self, action: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute individual action within a playbook step
        """
        try:
            action_type = action.get('type', 'unknown')
            
            if action_type == 'api_call':
                return self._execute_api_call(action, context)
            elif action_type == 'query':
                return self._execute_query(action, context)
            elif action_type == 'notification':
                return self._send_notification(action, context)
            elif action_type == 'investigation':
                return self._perform_investigation(action, context)
            else:
                return {
                    'action_type': action_type,
                    'success': False,
                    'message': f'Unsupported action type: {action_type}'
                }
                
        except Exception as e:
            return {
                'action_type': action.get('type', 'unknown'),
                'success': False,
                'message': str(e)
            }
    
    def _create_automation_runbook(self, runbook_name: str, playbook: IncidentPlaybook) -> Dict[str, Any]:
        """
        Create Systems Manager automation runbook for playbook
        """
        try:
            # Create automation document
            automation_content = {
                "schemaVersion": "0.3",
                "description": f"Automated runbook for {playbook.title}",
                "assumeRole": "{{ AutomationAssumeRole }}",
                "parameters": {
                    "IncidentId": {
                        "type": "String",
                        "description": "Incident ID for tracking"
                    },
                    "AutomationAssumeRole": {
                        "type": "String",
                        "description": "IAM role for automation execution"
                    }
                },
                "mainSteps": []
            }
            
            # Add automated steps from playbook
            for step in playbook.response_steps:
                if step.automation_available:
                    automation_step = {
                        "name": f"Step_{step.step_id}",
                        "action": "aws:executeAwsApi",
                        "description": step.description,
                        "inputs": {
                            "Service": "lambda",
                            "Api": "Invoke",
                            "FunctionName": f"playbook-automation-{step.step_id}",
                            "Payload": json.dumps({
                                "incident_id": "{{ IncidentId }}",
                                "step_data": asdict(step)
                            })
                        }
                    }
                    automation_content["mainSteps"].append(automation_step)
            
            # Create the automation document
            response = self.ssm_client.create_document(
                Content=json.dumps(automation_content),
                Name=runbook_name,
                DocumentType='Automation',
                DocumentFormat='JSON',
                Tags=[
                    {'Key': 'Purpose', 'Value': 'IncidentResponse'},
                    {'Key': 'PlaybookId', 'Value': playbook.playbook_id}
                ]
            )
            
            return {
                'status': 'success',
                'runbook_name': runbook_name,
                'document_name': response['DocumentDescription']['Name']
            }
            
        except Exception as e:
            logger.error(f"Error creating automation runbook: {str(e)}")
            return {
                'status': 'error',
                'runbook_name': runbook_name,
                'message': str(e)
            }

# Example usage
if __name__ == "__main__":
    # Initialize playbook manager
    playbook_manager = IncidentResponsePlaybookManager()
    
    # Create credential compromise playbook
    credential_playbook = playbook_manager.playbook_templates[IncidentType.CREDENTIAL_COMPROMISE.value]
    result = playbook_manager.create_playbook(credential_playbook)
    print(f"Playbook creation result: {json.dumps(result, indent=2)}")
    
    # Test playbook with simulated scenario
    test_scenario = {
        "compromised_user": "test-user",
        "incident_start_time": "2024-01-01T10:00:00Z",
        "source_ip": "192.168.1.100",
        "suspicious_activities": ["CreateUser", "AttachUserPolicy", "CreateAccessKey"]
    }
    
    test_result = playbook_manager.test_playbook(
        playbook_id="pb_credential_compromise_v1",
        test_scenario=test_scenario
    )
    print(f"Playbook test result: {json.dumps(test_result, indent=2, default=str)}")
```
### Example 2: Ransomware Response Playbook with Jupyter Integration

```python
# ransomware_response_playbook.py
import boto3
import json
from typing import Dict, List, Any
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class RansomwareResponsePlaybook:
    """
    Specialized playbook for ransomware incident response
    """
    
    def __init__(self, region: str = 'us-east-1'):
        self.region = region
        self.ec2_client = boto3.client('ec2', region_name=region)
        self.s3_client = boto3.client('s3', region_name=region)
        self.backup_client = boto3.client('backup', region_name=region)
        self.guardduty_client = boto3.client('guardduty', region_name=region)
        self.sns_client = boto3.client('sns', region_name=region)
        self.lambda_client = boto3.client('lambda', region_name=region)
    
    def execute_ransomware_response(self, incident_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute comprehensive ransomware response playbook
        """
        try:
            playbook_execution = {
                'incident_id': incident_context.get('incident_id', f"RANSOMWARE_{int(datetime.utcnow().timestamp())}"),
                'started_at': datetime.utcnow().isoformat(),
                'phases': {}
            }
            
            # Phase 1: Immediate Detection and Assessment
            detection_result = self._phase_1_detect_and_assess(incident_context)
            playbook_execution['phases']['detection'] = detection_result
            
            # Phase 2: Rapid Containment
            containment_result = self._phase_2_contain_threat(incident_context, detection_result)
            playbook_execution['phases']['containment'] = containment_result
            
            # Phase 3: Impact Analysis
            analysis_result = self._phase_3_analyze_impact(incident_context, containment_result)
            playbook_execution['phases']['analysis'] = analysis_result
            
            # Phase 4: Eradication and Recovery
            recovery_result = self._phase_4_eradicate_and_recover(incident_context, analysis_result)
            playbook_execution['phases']['recovery'] = recovery_result
            
            # Phase 5: Post-Incident Activities
            post_incident_result = self._phase_5_post_incident(incident_context, playbook_execution)
            playbook_execution['phases']['post_incident'] = post_incident_result
            
            playbook_execution['completed_at'] = datetime.utcnow().isoformat()
            playbook_execution['status'] = 'completed'
            
            return playbook_execution
            
        except Exception as e:
            logger.error(f"Error executing ransomware response playbook: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _phase_1_detect_and_assess(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Phase 1: Immediate Detection and Assessment
        """
        try:
            phase_result = {
                'phase': 'detection_and_assessment',
                'started_at': datetime.utcnow().isoformat(),
                'actions': []
            }
            
            # Action 1.1: Identify Ransomware Indicators
            indicators_action = {
                'action': 'identify_ransomware_indicators',
                'description': 'Scan for common ransomware indicators and file extensions',
                'steps': [
                    'Check for suspicious file extensions (.encrypted, .locked, .crypto)',
                    'Look for ransom notes (README.txt, DECRYPT_INSTRUCTIONS.html)',
                    'Identify unusual file modification patterns',
                    'Check for suspicious process names and network connections'
                ],
                'automated_checks': [
                    self._check_file_extensions(context),
                    self._check_ransom_notes(context),
                    self._check_process_anomalies(context)
                ],
                'status': 'completed'
            }
            phase_result['actions'].append(indicators_action)
            
            # Action 1.2: Assess Scope of Infection
            scope_action = {
                'action': 'assess_infection_scope',
                'description': 'Determine which systems and data are affected',
                'steps': [
                    'Inventory affected EC2 instances',
                    'Check S3 bucket integrity',
                    'Assess database encryption status',
                    'Identify network propagation paths'
                ],
                'affected_resources': self._identify_affected_resources(context),
                'status': 'completed'
            }
            phase_result['actions'].append(scope_action)
            
            # Action 1.3: Determine Ransomware Variant
            variant_action = {
                'action': 'determine_ransomware_variant',
                'description': 'Identify specific ransomware family and characteristics',
                'steps': [
                    'Analyze file encryption patterns',
                    'Examine ransom note content and format',
                    'Check against known ransomware signatures',
                    'Consult threat intelligence feeds'
                ],
                'variant_analysis': self._analyze_ransomware_variant(context),
                'status': 'completed'
            }
            phase_result['actions'].append(variant_action)
            
            phase_result['completed_at'] = datetime.utcnow().isoformat()
            phase_result['status'] = 'completed'
            
            return phase_result
            
        except Exception as e:
            return {
                'phase': 'detection_and_assessment',
                'status': 'error',
                'message': str(e)
            }
    
    def _phase_2_contain_threat(self, context: Dict[str, Any], detection_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Phase 2: Rapid Containment
        """
        try:
            phase_result = {
                'phase': 'containment',
                'started_at': datetime.utcnow().isoformat(),
                'actions': []
            }
            
            # Action 2.1: Isolate Infected Systems
            isolation_action = {
                'action': 'isolate_infected_systems',
                'description': 'Immediately isolate infected instances to prevent spread',
                'steps': [
                    'Create isolation security group with no inbound/outbound rules',
                    'Apply isolation security group to infected instances',
                    'Document original security group configurations',
                    'Notify stakeholders of isolation actions'
                ],
                'isolated_instances': self._isolate_infected_instances(context, detection_result),
                'status': 'completed'
            }
            phase_result['actions'].append(isolation_action)
            
            # Action 2.2: Preserve Evidence
            evidence_action = {
                'action': 'preserve_forensic_evidence',
                'description': 'Create forensic snapshots before any remediation',
                'steps': [
                    'Create EBS snapshots of infected volumes',
                    'Capture memory dumps from running instances',
                    'Export relevant CloudTrail logs',
                    'Document system state and configurations'
                ],
                'evidence_collected': self._preserve_forensic_evidence(context, detection_result),
                'status': 'completed'
            }
            phase_result['actions'].append(evidence_action)
            
            # Action 2.3: Protect Backups
            backup_action = {
                'action': 'protect_backup_systems',
                'description': 'Secure backup systems from ransomware spread',
                'steps': [
                    'Verify backup system integrity',
                    'Isolate backup networks if necessary',
                    'Check for backup encryption and tampering',
                    'Implement additional backup protection measures'
                ],
                'backup_status': self._protect_backup_systems(context),
                'status': 'completed'
            }
            phase_result['actions'].append(backup_action)
            
            phase_result['completed_at'] = datetime.utcnow().isoformat()
            phase_result['status'] = 'completed'
            
            return phase_result
            
        except Exception as e:
            return {
                'phase': 'containment',
                'status': 'error',
                'message': str(e)
            }
    
    def _phase_3_analyze_impact(self, context: Dict[str, Any], containment_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Phase 3: Impact Analysis
        """
        try:
            phase_result = {
                'phase': 'impact_analysis',
                'started_at': datetime.utcnow().isoformat(),
                'actions': []
            }
            
            # Action 3.1: Data Impact Assessment
            data_impact_action = {
                'action': 'assess_data_impact',
                'description': 'Determine extent of data encryption and corruption',
                'steps': [
                    'Catalog encrypted files and databases',
                    'Assess data recovery possibilities',
                    'Identify critical business data affected',
                    'Estimate data recovery time and costs'
                ],
                'data_assessment': self._assess_data_impact(context, containment_result),
                'status': 'completed'
            }
            phase_result['actions'].append(data_impact_action)
            
            # Action 3.2: Business Impact Analysis
            business_impact_action = {
                'action': 'analyze_business_impact',
                'description': 'Evaluate business operations and financial impact',
                'steps': [
                    'Identify affected business processes',
                    'Estimate downtime and revenue impact',
                    'Assess customer and partner impact',
                    'Evaluate regulatory and compliance implications'
                ],
                'business_impact': self._analyze_business_impact(context, containment_result),
                'status': 'completed'
            }
            phase_result['actions'].append(business_impact_action)
            
            # Action 3.3: Recovery Options Evaluation
            recovery_options_action = {
                'action': 'evaluate_recovery_options',
                'description': 'Assess available recovery methods and timelines',
                'steps': [
                    'Evaluate backup restoration options',
                    'Assess decryption tool availability',
                    'Consider ransom payment implications',
                    'Develop recovery timeline and priorities'
                ],
                'recovery_options': self._evaluate_recovery_options(context, containment_result),
                'status': 'completed'
            }
            phase_result['actions'].append(recovery_options_action)
            
            phase_result['completed_at'] = datetime.utcnow().isoformat()
            phase_result['status'] = 'completed'
            
            return phase_result
            
        except Exception as e:
            return {
                'phase': 'impact_analysis',
                'status': 'error',
                'message': str(e)
            }
    
    def _phase_4_eradicate_and_recover(self, context: Dict[str, Any], analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Phase 4: Eradication and Recovery
        """
        try:
            phase_result = {
                'phase': 'eradication_and_recovery',
                'started_at': datetime.utcnow().isoformat(),
                'actions': []
            }
            
            # Action 4.1: Remove Ransomware
            eradication_action = {
                'action': 'remove_ransomware',
                'description': 'Eliminate ransomware from infected systems',
                'steps': [
                    'Terminate infected instances if necessary',
                    'Launch clean instances from AMIs',
                    'Apply security patches and updates',
                    'Install and run anti-malware tools'
                ],
                'eradication_results': self._remove_ransomware(context, analysis_result),
                'status': 'completed'
            }
            phase_result['actions'].append(eradication_action)
            
            # Action 4.2: Restore from Backups
            restoration_action = {
                'action': 'restore_from_backups',
                'description': 'Restore systems and data from clean backups',
                'steps': [
                    'Verify backup integrity and cleanliness',
                    'Restore systems in isolated environment',
                    'Validate restored data integrity',
                    'Test system functionality before production'
                ],
                'restoration_results': self._restore_from_backups(context, analysis_result),
                'status': 'completed'
            }
            phase_result['actions'].append(restoration_action)
            
            # Action 4.3: Strengthen Security Controls
            hardening_action = {
                'action': 'strengthen_security_controls',
                'description': 'Implement additional security measures to prevent reinfection',
                'steps': [
                    'Update security group configurations',
                    'Implement additional monitoring and alerting',
                    'Deploy endpoint detection and response tools',
                    'Enhance backup and recovery procedures'
                ],
                'security_enhancements': self._strengthen_security_controls(context),
                'status': 'completed'
            }
            phase_result['actions'].append(hardening_action)
            
            phase_result['completed_at'] = datetime.utcnow().isoformat()
            phase_result['status'] = 'completed'
            
            return phase_result
            
        except Exception as e:
            return {
                'phase': 'eradication_and_recovery',
                'status': 'error',
                'message': str(e)
            }
    
    def _phase_5_post_incident(self, context: Dict[str, Any], execution_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Phase 5: Post-Incident Activities
        """
        try:
            phase_result = {
                'phase': 'post_incident',
                'started_at': datetime.utcnow().isoformat(),
                'actions': []
            }
            
            # Action 5.1: Lessons Learned Analysis
            lessons_learned_action = {
                'action': 'conduct_lessons_learned',
                'description': 'Analyze incident response and identify improvements',
                'steps': [
                    'Document incident timeline and response actions',
                    'Identify what worked well and what needs improvement',
                    'Update incident response procedures',
                    'Provide recommendations for prevention'
                ],
                'lessons_learned': self._conduct_lessons_learned(context, execution_result),
                'status': 'completed'
            }
            phase_result['actions'].append(lessons_learned_action)
            
            # Action 5.2: Update Security Measures
            security_updates_action = {
                'action': 'update_security_measures',
                'description': 'Implement long-term security improvements',
                'steps': [
                    'Update security policies and procedures',
                    'Enhance monitoring and detection capabilities',
                    'Improve backup and recovery processes',
                    'Conduct security awareness training'
                ],
                'security_updates': self._update_security_measures(context, execution_result),
                'status': 'completed'
            }
            phase_result['actions'].append(security_updates_action)
            
            # Action 5.3: Generate Final Report
            reporting_action = {
                'action': 'generate_final_report',
                'description': 'Create comprehensive incident report',
                'steps': [
                    'Compile incident details and timeline',
                    'Document response actions and outcomes',
                    'Include lessons learned and recommendations',
                    'Distribute report to stakeholders'
                ],
                'final_report': self._generate_final_report(context, execution_result),
                'status': 'completed'
            }
            phase_result['actions'].append(reporting_action)
            
            phase_result['completed_at'] = datetime.utcnow().isoformat()
            phase_result['status'] = 'completed'
            
            return phase_result
            
        except Exception as e:
            return {
                'phase': 'post_incident',
                'status': 'error',
                'message': str(e)
            }
    
    # Helper methods for each action (simplified implementations)
    def _check_file_extensions(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Check for suspicious file extensions indicating ransomware"""
        suspicious_extensions = ['.encrypted', '.locked', '.crypto', '.crypt', '.enc']
        # Simplified implementation
        return {
            'suspicious_extensions_found': suspicious_extensions[:2],  # Simulated findings
            'affected_file_count': 1250,
            'scan_completed': True
        }
    
    def _isolate_infected_instances(self, context: Dict[str, Any], detection_result: Dict[str, Any]) -> List[str]:
        """Isolate infected EC2 instances"""
        # Simplified implementation
        infected_instances = context.get('infected_instances', ['i-1234567890abcdef0'])
        
        for instance_id in infected_instances:
            try:
                # Create isolation security group
                isolation_sg = self.ec2_client.create_security_group(
                    GroupName=f'isolation-{instance_id}',
                    Description='Isolation security group for ransomware containment'
                )
                
                # Apply isolation security group
                self.ec2_client.modify_instance_attribute(
                    InstanceId=instance_id,
                    Groups=[isolation_sg['GroupId']]
                )
                
            except Exception as e:
                logger.error(f"Error isolating instance {instance_id}: {str(e)}")
        
        return infected_instances
    
    def _preserve_forensic_evidence(self, context: Dict[str, Any], detection_result: Dict[str, Any]) -> Dict[str, Any]:
        """Preserve forensic evidence"""
        # Simplified implementation
        return {
            'snapshots_created': ['snap-1234567890abcdef0', 'snap-0987654321fedcba0'],
            'memory_dumps_collected': 2,
            'logs_exported': ['cloudtrail', 'vpc_flow_logs', 'guardduty'],
            'evidence_location': 's3://forensic-evidence-bucket/ransomware-incident/'
        }

# Create Jupyter notebook template for interactive playbook execution
def create_jupyter_playbook_template():
    """
    Create Jupyter notebook template for interactive ransomware response
    """
    notebook_content = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# Ransomware Incident Response Playbook\n",
                    "\n",
                    "This interactive playbook guides you through the ransomware incident response process.\n",
                    "\n",
                    "**Incident ID:** [TO BE FILLED]\n",
                    "**Date:** [TO BE FILLED]\n",
                    "**Incident Commander:** [TO BE FILLED]\n"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "source": [
                    "# Initialize the ransomware response playbook\n",
                    "import boto3\n",
                    "from ransomware_response_playbook import RansomwareResponsePlaybook\n",
                    "\n",
                    "# Initialize playbook\n",
                    "playbook = RansomwareResponsePlaybook()\n",
                    "\n",
                    "# Define incident context\n",
                    "incident_context = {\n",
                    "    'incident_id': 'RANSOMWARE_2024_001',\n",
                    "    'detected_at': '2024-01-01T10:00:00Z',\n",
                    "    'infected_instances': ['i-1234567890abcdef0'],\n",
                    "    'affected_regions': ['us-east-1'],\n",
                    "    'initial_indicators': ['suspicious file extensions', 'ransom note found']\n",
                    "}\n",
                    "\n",
                    "print(f\"Incident Context: {incident_context}\")"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## Phase 1: Detection and Assessment\n",
                    "\n",
                    "Execute the detection and assessment phase to identify the scope and nature of the ransomware attack."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "source": [
                    "# Execute Phase 1: Detection and Assessment\n",
                    "detection_result = playbook._phase_1_detect_and_assess(incident_context)\n",
                    "print(\"Phase 1 Results:\")\n",
                    "print(json.dumps(detection_result, indent=2, default=str))"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## Phase 2: Containment\n",
                    "\n",
                    "Immediately contain the ransomware to prevent further spread."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "source": [
                    "# Execute Phase 2: Containment\n",
                    "containment_result = playbook._phase_2_contain_threat(incident_context, detection_result)\n",
                    "print(\"Phase 2 Results:\")\n",
                    "print(json.dumps(containment_result, indent=2, default=str))"
                ]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.8.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    
    return notebook_content

# Example usage
if __name__ == "__main__":
    # Initialize ransomware response playbook
    ransomware_playbook = RansomwareResponsePlaybook()
    
    # Execute ransomware response
    incident_context = {
        'incident_id': 'RANSOMWARE_2024_001',
        'detected_at': '2024-01-01T10:00:00Z',
        'infected_instances': ['i-1234567890abcdef0', 'i-0987654321fedcba0'],
        'affected_regions': ['us-east-1'],
        'initial_indicators': ['suspicious file extensions', 'ransom note found', 'unusual network activity']
    }
    
    execution_result = ransomware_playbook.execute_ransomware_response(incident_context)
    print(f"Ransomware response execution: {json.dumps(execution_result, indent=2, default=str)}")
    
    # Create Jupyter notebook template
    notebook_template = create_jupyter_playbook_template()
    with open('ransomware_response_playbook.ipynb', 'w') as f:
        json.dump(notebook_template, f, indent=2)
    
    print("Jupyter notebook template created: ransomware_response_playbook.ipynb")
```
## Resources

### Related Well-Architected Best Practices

- [SEC10-BP02 - Develop incident management plans](./SEC10-BP02.html)
- [SEC10-BP01 - Identify key personnel and external resources](./SEC10-BP01.html)
- [SEC10-BP03 - Prepare forensic capabilities](./SEC10-BP03.html)

### Related Documents

- [Framework for Incident Response Playbooks](https://docs.aws.amazon.com/whitepapers/latest/aws-security-incident-response-guide/framework-for-incident-response-playbooks.html)
- [Develop your own Incident Response Playbooks](https://aws.amazon.com/blogs/security/develop-your-own-incident-response-playbooks/)
- [Incident Response Playbook Samples](https://github.com/aws-samples/aws-incident-response-playbooks)
- [Building an AWS incident response runbook using Jupyter playbooks and CloudTrail Lake](https://aws.amazon.com/blogs/security/building-an-aws-incident-response-runbook-using-jupyter-playbooks-and-cloudtrail-lake/)
- [AWS Security Incident Response Guide](https://docs.aws.amazon.com/whitepapers/latest/aws-security-incident-response-guide/aws-security-incident-response-guide.html)
- [Remediating security issues discovered by GuardDuty](https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_remediate.html)

### AWS Services for Playbook Implementation

- [AWS Systems Manager Automation](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-automation.html) - For automated playbook execution
- [AWS Step Functions](https://aws.amazon.com/step-functions/) - For orchestrating complex playbook workflows
- [AWS Lambda](https://aws.amazon.com/lambda/) - For custom playbook actions and integrations
- [Amazon GuardDuty](https://aws.amazon.com/guardduty/) - For threat detection and finding-based playbooks
- [AWS Security Hub](https://aws.amazon.com/security-hub/) - For centralized security finding management
- [Amazon Detective](https://aws.amazon.com/detective/) - For security investigation and analysis
- [AWS CloudTrail](https://aws.amazon.com/cloudtrail/) - For audit logging and forensic analysis
- [Amazon CloudWatch](https://aws.amazon.com/cloudwatch/) - For monitoring and alerting

### Playbook Templates and Examples

- [AWS Incident Response Playbooks Repository](https://github.com/aws-samples/aws-incident-response-playbooks)
- [NIST Cybersecurity Framework Playbooks](https://www.nist.gov/cyberframework/online-learning/components-framework)
- [SANS Incident Response Playbooks](https://www.sans.org/white-papers/incident-response-playbooks/)
- [Ransomware Response Playbook Template](https://www.cisa.gov/sites/default/files/publications/CISA_MS-ISAC_Ransomware%20Guide_S508C.pdf)

### Interactive Playbook Tools

- [Jupyter Notebooks](https://jupyter.org/) - For interactive playbook execution
- [AWS CloudShell](https://aws.amazon.com/cloudshell/) - For browser-based AWS CLI access
- [AWS Systems Manager Session Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager.html) - For secure instance access
- [Phantom/Splunk SOAR](https://www.splunk.com/en_us/software/splunk-security-orchestration-and-automation-response.html) - For security orchestration

### Common Incident Types and Playbooks

**Credential Compromise:**
- Unauthorized API calls
- Privilege escalation
- Account takeover
- Access key exposure

**Ransomware:**
- File encryption detection
- System isolation
- Backup restoration
- Payment decision framework

**Data Exfiltration:**
- Unusual data access patterns
- Large data transfers
- Unauthorized S3 access
- Database compromise

**DDoS Attacks:**
- Traffic pattern analysis
- AWS Shield activation
- CloudFront configuration
- Rate limiting implementation

**Malware Infection:**
- Instance compromise
- Lateral movement detection
- System remediation
- Network isolation

### Testing and Validation

- **Tabletop Exercises**: Regular scenario-based discussions
- **Red Team Exercises**: Simulated attack scenarios
- **Purple Team Activities**: Collaborative defense testing
- **Automated Testing**: Continuous playbook validation
- **Metrics and KPIs**: Response time and effectiveness measurement

### Compliance and Regulatory Considerations

- **GDPR**: Data breach notification requirements (72 hours)
- **HIPAA**: Healthcare data incident response procedures
- **PCI DSS**: Payment card data security incident handling
- **SOX**: Financial reporting system incident procedures
- **NIST**: Cybersecurity Framework incident response guidelines

### Best Practices for Playbook Development

1. **Keep playbooks current**: Regular updates based on threat landscape changes
2. **Make them actionable**: Include specific commands, queries, and procedures
3. **Test regularly**: Conduct regular drills and simulations
4. **Document everything**: Maintain detailed logs and evidence chains
5. **Automate where possible**: Reduce manual effort and human error
6. **Train your team**: Ensure all responders are familiar with playbooks
7. **Measure effectiveness**: Track metrics and continuously improve

### Training and Certification Resources

- [AWS Security Specialty Certification](https://aws.amazon.com/certification/certified-security-specialty/)
- [SANS Incident Response Training](https://www.sans.org/cyber-security-courses/incident-response/)
- [NIST Cybersecurity Framework Training](https://www.nist.gov/cyberframework/online-learning)
- [AWS Security Learning Path](https://aws.amazon.com/training/learning-paths/security/)
- [Certified Computer Security Incident Handler (CSIH)](https://www.eccouncil.org/programs/computer-security-incident-handler-csih/)
