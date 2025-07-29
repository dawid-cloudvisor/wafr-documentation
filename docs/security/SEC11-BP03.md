---
title: "SEC11-BP03: Perform regular penetration testing"
layout: default
parent: "SEC11 - How do you incorporate and validate the security properties of applications throughout the design, development, and deployment lifecycle?"
grand_parent: Security
nav_order: 3
---

# SEC11-BP03: Perform regular penetration testing

## Overview

Conduct regular penetration testing to validate the effectiveness of security controls and identify vulnerabilities that automated tools might miss. Penetration testing should be performed by qualified security professionals using a combination of automated tools and manual techniques to simulate real-world attack scenarios.

## Implementation Guidance

Penetration testing is a critical component of a comprehensive security testing strategy that goes beyond automated vulnerability scanning. While automated tools can identify known vulnerabilities and misconfigurations, penetration testing provides a human element that can discover complex attack chains, business logic flaws, and novel attack vectors that automated tools might miss.

### Key Principles of Penetration Testing

**Risk-Based Approach**: Focus penetration testing efforts on the most critical assets and highest-risk attack vectors based on threat modeling and risk assessment results.

**Regular Cadence**: Establish a regular penetration testing schedule that aligns with your development cycles, major releases, and compliance requirements.

**Comprehensive Scope**: Include all layers of your application stack, from infrastructure and network components to application logic and user interfaces.

**Realistic Attack Simulation**: Use testing methodologies that simulate real-world attack scenarios and adversary tactics, techniques, and procedures (TTPs).

**Actionable Results**: Ensure penetration testing produces clear, actionable findings with specific remediation guidance and business risk context.

## Implementation Steps

### Step 1: Establish Penetration Testing Program Framework

Create a comprehensive framework for managing penetration testing activities:

```python
# Penetration Testing Program Framework
import boto3
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import uuid

class PenetrationTestingProgram:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.s3 = boto3.client('s3')
        self.sns = boto3.client('sns')
        self.ssm = boto3.client('ssm')
        
        # DynamoDB tables for tracking
        self.pentest_table = self.dynamodb.Table('penetration-tests')
        self.findings_table = self.dynamodb.Table('pentest-findings')
        self.remediation_table = self.dynamodb.Table('pentest-remediation')
        
    def create_penetration_testing_framework(self, org_config: Dict) -> Dict:
        """
        Create comprehensive penetration testing framework
        """
        framework = {
            'program_id': f"PENTEST-PROG-{datetime.now().strftime('%Y%m%d')}",
            'organization': org_config['organization_name'],
            'program_scope': {
                'applications': org_config.get('applications', []),
                'infrastructure': org_config.get('infrastructure_scope', []),
                'networks': org_config.get('network_scope', []),
                'cloud_environments': org_config.get('cloud_environments', ['aws']),
                'exclusions': org_config.get('exclusions', [])
            },
            'testing_methodology': {
                'frameworks': ['OWASP', 'NIST', 'PTES', 'OSSTMM'],
                'primary_framework': org_config.get('primary_framework', 'OWASP'),
                'testing_phases': [
                    'reconnaissance',
                    'scanning_enumeration',
                    'vulnerability_assessment',
                    'exploitation',
                    'post_exploitation',
                    'reporting'
                ],
                'attack_vectors': [
                    'web_application',
                    'network_infrastructure',
                    'wireless_networks',
                    'social_engineering',
                    'physical_security',
                    'cloud_configuration'
                ]
            },
            'testing_schedule': {
                'frequency': org_config.get('testing_frequency', 'quarterly'),
                'critical_applications_frequency': 'monthly',
                'infrastructure_frequency': 'semi-annually',
                'ad_hoc_triggers': [
                    'major_application_release',
                    'infrastructure_changes',
                    'security_incident',
                    'compliance_requirement'
                ]
            },
            'resource_requirements': {
                'internal_team_size': org_config.get('internal_team_size', 2),
                'external_vendor_required': org_config.get('use_external_vendor', True),
                'budget_allocation': org_config.get('annual_budget', 100000),
                'tool_requirements': [
                    'vulnerability_scanners',
                    'exploitation_frameworks',
                    'network_analysis_tools',
                    'web_application_testing_tools',
                    'reporting_platforms'
                ]
            },
            'compliance_requirements': {
                'frameworks': org_config.get('compliance_frameworks', []),
                'reporting_requirements': org_config.get('reporting_requirements', []),
                'evidence_retention_period': org_config.get('retention_period', 2555)  # 7 years in days
            },
            'success_metrics': {
                'coverage_percentage': 95,
                'critical_finding_remediation_time': 30,  # days
                'high_finding_remediation_time': 60,
                'medium_finding_remediation_time': 90,
                'retest_pass_rate': 90
            }
        }
        
        return framework
    
    def plan_penetration_test(self, test_config: Dict) -> Dict:
        """
        Plan and schedule a penetration test
        """
        test_plan = {
            'test_id': f"PENTEST-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}",
            'test_name': test_config['test_name'],
            'test_type': test_config.get('test_type', 'comprehensive'),
            'scope': {
                'target_applications': test_config.get('target_applications', []),
                'target_infrastructure': test_config.get('target_infrastructure', []),
                'ip_ranges': test_config.get('ip_ranges', []),
                'domains': test_config.get('domains', []),
                'exclusions': test_config.get('exclusions', []),
                'testing_windows': test_config.get('testing_windows', [])
            },
            'methodology': {
                'testing_approach': test_config.get('approach', 'black_box'),
                'testing_phases': [
                    {
                        'phase': 'reconnaissance',
                        'duration_hours': 8,
                        'techniques': [
                            'passive_information_gathering',
                            'osint_collection',
                            'domain_enumeration',
                            'social_media_reconnaissance'
                        ]
                    },
                    {
                        'phase': 'scanning_enumeration',
                        'duration_hours': 16,
                        'techniques': [
                            'network_port_scanning',
                            'service_enumeration',
                            'vulnerability_scanning',
                            'web_application_discovery'
                        ]
                    },
                    {
                        'phase': 'vulnerability_assessment',
                        'duration_hours': 24,
                        'techniques': [
                            'manual_vulnerability_validation',
                            'configuration_review',
                            'authentication_testing',
                            'authorization_testing'
                        ]
                    },
                    {
                        'phase': 'exploitation',
                        'duration_hours': 32,
                        'techniques': [
                            'manual_exploitation',
                            'automated_exploitation',
                            'privilege_escalation',
                            'lateral_movement'
                        ]
                    },
                    {
                        'phase': 'post_exploitation',
                        'duration_hours': 16,
                        'techniques': [
                            'data_exfiltration_simulation',
                            'persistence_establishment',
                            'impact_assessment',
                            'cleanup_activities'
                        ]
                    },
                    {
                        'phase': 'reporting',
                        'duration_hours': 24,
                        'deliverables': [
                            'executive_summary',
                            'technical_findings',
                            'remediation_recommendations',
                            'risk_assessment'
                        ]
                    }
                ]
            },
            'team_composition': {
                'lead_tester': test_config.get('lead_tester'),
                'team_members': test_config.get('team_members', []),
                'external_vendor': test_config.get('external_vendor'),
                'required_certifications': ['OSCP', 'CEH', 'GPEN', 'CISSP']
            },
            'timeline': {
                'planned_start_date': test_config['start_date'],
                'planned_end_date': test_config['end_date'],
                'estimated_duration_hours': 120,
                'reporting_deadline': test_config.get('reporting_deadline'),
                'remediation_retest_date': test_config.get('retest_date')
            },
            'tools_and_techniques': {
                'automated_tools': [
                    'nmap',
                    'nessus',
                    'burp_suite_professional',
                    'metasploit',
                    'sqlmap',
                    'nikto',
                    'dirb',
                    'gobuster'
                ],
                'manual_techniques': [
                    'manual_code_review',
                    'business_logic_testing',
                    'social_engineering',
                    'physical_security_assessment'
                ],
                'custom_tools': test_config.get('custom_tools', [])
            },
            'risk_management': {
                'risk_assessment': test_config.get('risk_level', 'medium'),
                'backup_procedures': test_config.get('backup_required', True),
                'rollback_plan': test_config.get('rollback_plan'),
                'emergency_contacts': test_config.get('emergency_contacts', []),
                'testing_limitations': test_config.get('limitations', [])
            },
            'legal_compliance': {
                'authorization_obtained': False,
                'rules_of_engagement_signed': False,
                'liability_insurance': test_config.get('insurance_required', True),
                'data_handling_agreement': test_config.get('data_agreement_required', True),
                'regulatory_notifications': test_config.get('regulatory_notifications', [])
            }
        }
        
        # Store test plan
        self.pentest_table.put_item(Item=test_plan)
        
        return test_plan
    
    def create_rules_of_engagement(self, test_id: str, roe_config: Dict) -> Dict:
        """
        Create detailed rules of engagement for penetration test
        """
        rules_of_engagement = {
            'test_id': test_id,
            'document_version': '1.0',
            'created_date': datetime.now().isoformat(),
            'scope_definition': {
                'in_scope_targets': roe_config.get('in_scope', []),
                'out_of_scope_targets': roe_config.get('out_of_scope', []),
                'testing_methods_allowed': roe_config.get('allowed_methods', []),
                'testing_methods_prohibited': roe_config.get('prohibited_methods', []),
                'data_types_accessible': roe_config.get('accessible_data', []),
                'data_types_restricted': roe_config.get('restricted_data', [])
            },
            'testing_constraints': {
                'testing_windows': roe_config.get('testing_windows', []),
                'blackout_periods': roe_config.get('blackout_periods', []),
                'resource_limitations': roe_config.get('resource_limits', {}),
                'network_bandwidth_limits': roe_config.get('bandwidth_limits'),
                'concurrent_user_limits': roe_config.get('user_limits'),
                'dos_testing_restrictions': roe_config.get('dos_restrictions', 'prohibited')
            },
            'communication_protocols': {
                'primary_contacts': roe_config.get('primary_contacts', []),
                'escalation_contacts': roe_config.get('escalation_contacts', []),
                'communication_channels': roe_config.get('communication_channels', []),
                'reporting_frequency': roe_config.get('reporting_frequency', 'daily'),
                'emergency_procedures': roe_config.get('emergency_procedures', [])
            },
            'data_handling': {
                'data_classification_levels': roe_config.get('data_classifications', []),
                'data_retention_policy': roe_config.get('retention_policy'),
                'data_destruction_requirements': roe_config.get('destruction_requirements'),
                'data_sharing_restrictions': roe_config.get('sharing_restrictions', []),
                'evidence_handling_procedures': roe_config.get('evidence_procedures', [])
            },
            'legal_considerations': {
                'authorization_scope': roe_config.get('authorization_scope'),
                'liability_limitations': roe_config.get('liability_limits', []),
                'indemnification_clauses': roe_config.get('indemnification', []),
                'regulatory_compliance_requirements': roe_config.get('compliance_requirements', []),
                'law_enforcement_notification': roe_config.get('law_enforcement_policy')
            },
            'technical_requirements': {
                'vpn_access_required': roe_config.get('vpn_required', False),
                'source_ip_restrictions': roe_config.get('source_ip_restrictions', []),
                'authentication_credentials': roe_config.get('credentials_provided', False),
                'testing_environment_isolation': roe_config.get('isolation_required', True),
                'monitoring_and_logging': roe_config.get('monitoring_requirements', [])
            },
            'success_criteria': {
                'coverage_requirements': roe_config.get('coverage_requirements', {}),
                'finding_validation_requirements': roe_config.get('validation_requirements', []),
                'reporting_standards': roe_config.get('reporting_standards', []),
                'remediation_guidance_requirements': roe_config.get('remediation_requirements', [])
            },
            'post_test_activities': {
                'cleanup_requirements': roe_config.get('cleanup_requirements', []),
                'data_return_requirements': roe_config.get('data_return_requirements', []),
                'follow_up_testing_schedule': roe_config.get('follow_up_schedule'),
                'lessons_learned_session': roe_config.get('lessons_learned_required', True)
            }
        }
        
        # Store rules of engagement
        roe_document = {
            'document_id': f"ROE-{test_id}",
            'test_id': test_id,
            'document_type': 'rules_of_engagement',
            'content': rules_of_engagement,
            'status': 'draft',
            'approvals_required': roe_config.get('approvals_required', []),
            'created_date': datetime.now().isoformat()
        }
        
        # Store in S3 for document management
        s3_key = f"penetration-testing/rules-of-engagement/{test_id}/roe-{test_id}.json"
        self.s3.put_object(
            Bucket=roe_config.get('document_bucket', 'pentest-documents'),
            Key=s3_key,
            Body=json.dumps(roe_document, indent=2),
            ContentType='application/json',
            ServerSideEncryption='AES256'
        )
        
        return {
            'roe_document_id': roe_document['document_id'],
            's3_location': f"s3://{roe_config.get('document_bucket', 'pentest-documents')}/{s3_key}",
            'rules_of_engagement': rules_of_engagement
        }
    
    def execute_penetration_test_phase(self, test_id: str, phase: str, phase_config: Dict) -> Dict:
        """
        Execute specific phase of penetration test
        """
        phase_execution = {
            'execution_id': f"{test_id}-{phase}-{datetime.now().strftime('%Y%m%d%H%M')}",
            'test_id': test_id,
            'phase': phase,
            'start_time': datetime.now().isoformat(),
            'status': 'in_progress',
            'activities': [],
            'findings': [],
            'tools_used': [],
            'techniques_applied': [],
            'evidence_collected': []
        }
        
        # Phase-specific execution logic
        if phase == 'reconnaissance':
            phase_execution = self.execute_reconnaissance_phase(phase_execution, phase_config)
        elif phase == 'scanning_enumeration':
            phase_execution = self.execute_scanning_phase(phase_execution, phase_config)
        elif phase == 'vulnerability_assessment':
            phase_execution = self.execute_vulnerability_assessment_phase(phase_execution, phase_config)
        elif phase == 'exploitation':
            phase_execution = self.execute_exploitation_phase(phase_execution, phase_config)
        elif phase == 'post_exploitation':
            phase_execution = self.execute_post_exploitation_phase(phase_execution, phase_config)
        elif phase == 'reporting':
            phase_execution = self.execute_reporting_phase(phase_execution, phase_config)
        
        phase_execution['end_time'] = datetime.now().isoformat()
        phase_execution['status'] = 'completed'
        
        # Store phase execution results
        self.pentest_table.put_item(Item=phase_execution)
        
        return phase_execution
    
    def execute_reconnaissance_phase(self, phase_execution: Dict, config: Dict) -> Dict:
        """
        Execute reconnaissance phase activities
        """
        reconnaissance_activities = [
            {
                'activity': 'passive_information_gathering',
                'description': 'Collect publicly available information about target',
                'tools': ['google_dorking', 'shodan', 'censys', 'whois'],
                'techniques': [
                    'search_engine_reconnaissance',
                    'social_media_analysis',
                    'public_records_search',
                    'dns_enumeration'
                ],
                'findings': [],
                'evidence': []
            },
            {
                'activity': 'osint_collection',
                'description': 'Open source intelligence gathering',
                'tools': ['maltego', 'recon_ng', 'theharvester', 'spiderfoot'],
                'techniques': [
                    'email_harvesting',
                    'subdomain_enumeration',
                    'employee_information_gathering',
                    'technology_stack_identification'
                ],
                'findings': [],
                'evidence': []
            },
            {
                'activity': 'domain_enumeration',
                'description': 'Enumerate domains and subdomains',
                'tools': ['amass', 'subfinder', 'assetfinder', 'dnsrecon'],
                'techniques': [
                    'dns_zone_transfer',
                    'subdomain_brute_forcing',
                    'certificate_transparency_logs',
                    'reverse_dns_lookups'
                ],
                'findings': [],
                'evidence': []
            }
        ]
        
        phase_execution['activities'] = reconnaissance_activities
        phase_execution['tools_used'] = [
            tool for activity in reconnaissance_activities 
            for tool in activity['tools']
        ]
        phase_execution['techniques_applied'] = [
            technique for activity in reconnaissance_activities 
            for technique in activity['techniques']
        ]
        
        return phase_execution
    
    def execute_scanning_phase(self, phase_execution: Dict, config: Dict) -> Dict:
        """
        Execute scanning and enumeration phase
        """
        scanning_activities = [
            {
                'activity': 'network_port_scanning',
                'description': 'Identify open ports and services',
                'tools': ['nmap', 'masscan', 'zmap'],
                'techniques': [
                    'tcp_syn_scanning',
                    'udp_scanning',
                    'service_version_detection',
                    'os_fingerprinting'
                ],
                'scan_results': {
                    'ports_discovered': [],
                    'services_identified': [],
                    'operating_systems': [],
                    'vulnerabilities_detected': []
                }
            },
            {
                'activity': 'web_application_discovery',
                'description': 'Discover web applications and technologies',
                'tools': ['dirb', 'gobuster', 'wfuzz', 'whatweb'],
                'techniques': [
                    'directory_brute_forcing',
                    'file_extension_enumeration',
                    'technology_fingerprinting',
                    'hidden_parameter_discovery'
                ],
                'scan_results': {
                    'directories_found': [],
                    'files_discovered': [],
                    'technologies_identified': [],
                    'parameters_found': []
                }
            },
            {
                'activity': 'vulnerability_scanning',
                'description': 'Automated vulnerability identification',
                'tools': ['nessus', 'openvas', 'nuclei', 'nikto'],
                'techniques': [
                    'authenticated_scanning',
                    'unauthenticated_scanning',
                    'web_application_scanning',
                    'database_scanning'
                ],
                'scan_results': {
                    'vulnerabilities_found': [],
                    'severity_distribution': {},
                    'false_positives_identified': [],
                    'manual_verification_required': []
                }
            }
        ]
        
        phase_execution['activities'] = scanning_activities
        return phase_execution
    
    def execute_vulnerability_assessment_phase(self, phase_execution: Dict, config: Dict) -> Dict:
        """
        Execute vulnerability assessment phase
        """
        assessment_activities = [
            {
                'activity': 'manual_vulnerability_validation',
                'description': 'Manually validate automated scan results',
                'techniques': [
                    'proof_of_concept_development',
                    'false_positive_elimination',
                    'impact_assessment',
                    'exploitability_analysis'
                ],
                'validation_results': {
                    'confirmed_vulnerabilities': [],
                    'false_positives': [],
                    'risk_ratings': {},
                    'exploitation_difficulty': {}
                }
            },
            {
                'activity': 'authentication_testing',
                'description': 'Test authentication mechanisms',
                'techniques': [
                    'brute_force_attacks',
                    'credential_stuffing',
                    'session_management_testing',
                    'multi_factor_authentication_bypass'
                ],
                'test_results': {
                    'weak_passwords_found': [],
                    'account_lockout_bypass': [],
                    'session_vulnerabilities': [],
                    'mfa_weaknesses': []
                }
            },
            {
                'activity': 'authorization_testing',
                'description': 'Test authorization and access controls',
                'techniques': [
                    'privilege_escalation_testing',
                    'horizontal_access_control_bypass',
                    'vertical_access_control_bypass',
                    'business_logic_flaw_identification'
                ],
                'test_results': {
                    'privilege_escalation_paths': [],
                    'access_control_bypasses': [],
                    'business_logic_flaws': [],
                    'data_exposure_issues': []
                }
            }
        ]
        
        phase_execution['activities'] = assessment_activities
        return phase_execution
    
    def execute_exploitation_phase(self, phase_execution: Dict, config: Dict) -> Dict:
        """
        Execute exploitation phase (with appropriate safeguards)
        """
        exploitation_activities = [
            {
                'activity': 'controlled_exploitation',
                'description': 'Safely exploit validated vulnerabilities',
                'safeguards': [
                    'backup_verification',
                    'rollback_procedures',
                    'impact_limitation',
                    'monitoring_alerts'
                ],
                'techniques': [
                    'manual_exploitation',
                    'automated_exploitation_frameworks',
                    'custom_exploit_development',
                    'social_engineering_simulation'
                ],
                'exploitation_results': {
                    'successful_exploits': [],
                    'failed_exploitation_attempts': [],
                    'access_gained': [],
                    'data_accessed': []
                }
            },
            {
                'activity': 'privilege_escalation',
                'description': 'Attempt to escalate privileges',
                'techniques': [
                    'local_privilege_escalation',
                    'kernel_exploits',
                    'service_misconfigurations',
                    'sudo_misconfigurations'
                ],
                'escalation_results': {
                    'escalation_paths_found': [],
                    'root_access_achieved': False,
                    'administrative_access_gained': [],
                    'service_account_compromise': []
                }
            },
            {
                'activity': 'lateral_movement',
                'description': 'Move laterally through the network',
                'techniques': [
                    'credential_harvesting',
                    'pass_the_hash_attacks',
                    'kerberos_attacks',
                    'network_pivoting'
                ],
                'movement_results': {
                    'systems_compromised': [],
                    'credentials_harvested': [],
                    'network_segments_accessed': [],
                    'critical_systems_reached': []
                }
            }
        ]
        
        phase_execution['activities'] = exploitation_activities
        return phase_execution
    
    def execute_post_exploitation_phase(self, phase_execution: Dict, config: Dict) -> Dict:
        """
        Execute post-exploitation phase
        """
        post_exploitation_activities = [
            {
                'activity': 'impact_assessment',
                'description': 'Assess the potential impact of successful attacks',
                'assessment_areas': [
                    'data_accessibility',
                    'system_control_level',
                    'business_process_impact',
                    'compliance_violations'
                ],
                'impact_results': {
                    'sensitive_data_accessed': [],
                    'business_critical_systems_compromised': [],
                    'regulatory_data_exposed': [],
                    'financial_impact_estimate': 0
                }
            },
            {
                'activity': 'persistence_testing',
                'description': 'Test ability to maintain access (safely)',
                'techniques': [
                    'backdoor_installation_simulation',
                    'scheduled_task_creation',
                    'service_modification',
                    'registry_modification'
                ],
                'persistence_results': {
                    'persistence_mechanisms_tested': [],
                    'detection_evasion_success': [],
                    'cleanup_verification': [],
                    'monitoring_bypass_techniques': []
                }
            },
            {
                'activity': 'data_exfiltration_simulation',
                'description': 'Simulate data exfiltration (without actual data theft)',
                'techniques': [
                    'dns_tunneling',
                    'http_exfiltration',
                    'encrypted_channels',
                    'steganography'
                ],
                'exfiltration_results': {
                    'exfiltration_methods_successful': [],
                    'detection_mechanisms_bypassed': [],
                    'data_loss_prevention_effectiveness': [],
                    'network_monitoring_gaps': []
                }
            }
        ]
        
        phase_execution['activities'] = post_exploitation_activities
        return phase_execution
    
    def execute_reporting_phase(self, phase_execution: Dict, config: Dict) -> Dict:
        """
        Execute reporting phase
        """
        reporting_activities = [
            {
                'activity': 'findings_consolidation',
                'description': 'Consolidate and prioritize all findings',
                'consolidation_process': [
                    'duplicate_removal',
                    'risk_assessment',
                    'business_impact_analysis',
                    'remediation_prioritization'
                ]
            },
            {
                'activity': 'report_generation',
                'description': 'Generate comprehensive penetration test report',
                'report_sections': [
                    'executive_summary',
                    'methodology_overview',
                    'findings_summary',
                    'detailed_technical_findings',
                    'risk_assessment',
                    'remediation_recommendations',
                    'appendices'
                ]
            },
            {
                'activity': 'stakeholder_presentation',
                'description': 'Present findings to stakeholders',
                'presentation_formats': [
                    'executive_briefing',
                    'technical_deep_dive',
                    'remediation_workshop',
                    'lessons_learned_session'
                ]
            }
        ]
        
        phase_execution['activities'] = reporting_activities
        return phase_execution

# Example usage
pentest_program = PenetrationTestingProgram()

# Create penetration testing framework
org_config = {
    'organization_name': 'SecureCompany Inc.',
    'applications': ['web-app-1', 'api-service', 'mobile-app'],
    'infrastructure_scope': ['production-vpc', 'staging-vpc'],
    'network_scope': ['10.0.0.0/16', '172.16.0.0/16'],
    'cloud_environments': ['aws', 'azure'],
    'testing_frequency': 'quarterly',
    'primary_framework': 'OWASP',
    'annual_budget': 150000,
    'compliance_frameworks': ['SOC2', 'PCI-DSS']
}

framework = pentest_program.create_penetration_testing_framework(org_config)
print("Penetration Testing Framework:")
print(json.dumps(framework, indent=2))

# Plan a penetration test
test_config = {
    'test_name': 'Q1 2024 Web Application Penetration Test',
    'test_type': 'web_application',
    'target_applications': ['https://app.securecompany.com'],
    'approach': 'gray_box',
    'start_date': '2024-03-01',
    'end_date': '2024-03-15',
    'lead_tester': 'senior-pentester@company.com',
    'external_vendor': 'PentestCorp LLC'
}

test_plan = pentest_program.plan_penetration_test(test_config)
print(f"\\nPenetration Test Planned: {test_plan['test_id']}")
```
### Step 2: Manage External Penetration Testing Vendors

Establish processes for selecting, managing, and working with external penetration testing vendors:

```python
# External Penetration Testing Vendor Management
import boto3
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class PentestVendorManagement:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.s3 = boto3.client('s3')
        self.ssm = boto3.client('ssm')
        
        # DynamoDB tables
        self.vendors_table = self.dynamodb.Table('pentest-vendors')
        self.contracts_table = self.dynamodb.Table('pentest-contracts')
        self.evaluations_table = self.dynamodb.Table('vendor-evaluations')
        
    def create_vendor_qualification_framework(self) -> Dict:
        """
        Create framework for qualifying penetration testing vendors
        """
        qualification_framework = {
            'technical_qualifications': {
                'certifications_required': [
                    {
                        'certification': 'OSCP',
                        'minimum_team_members': 2,
                        'priority': 'high'
                    },
                    {
                        'certification': 'GPEN',
                        'minimum_team_members': 1,
                        'priority': 'high'
                    },
                    {
                        'certification': 'CEH',
                        'minimum_team_members': 1,
                        'priority': 'medium'
                    },
                    {
                        'certification': 'CISSP',
                        'minimum_team_members': 1,
                        'priority': 'medium'
                    }
                ],
                'experience_requirements': {
                    'minimum_years_experience': 5,
                    'similar_industry_experience': True,
                    'cloud_security_experience': True,
                    'web_application_testing_experience': True,
                    'network_penetration_testing_experience': True
                },
                'methodology_requirements': {
                    'frameworks_supported': ['OWASP', 'NIST', 'PTES'],
                    'testing_approaches': ['black_box', 'gray_box', 'white_box'],
                    'reporting_standards': ['detailed_technical', 'executive_summary', 'remediation_guidance']
                },
                'tool_proficiency': {
                    'commercial_tools': ['Burp Suite Professional', 'Nessus', 'Metasploit Pro'],
                    'open_source_tools': ['OWASP ZAP', 'Nmap', 'Nikto', 'SQLMap'],
                    'custom_tool_development': True,
                    'automation_capabilities': True
                }
            },
            'business_qualifications': {
                'company_requirements': {
                    'minimum_years_in_business': 3,
                    'minimum_team_size': 5,
                    'financial_stability_verification': True,
                    'client_references_required': 3,
                    'industry_reputation_check': True
                },
                'compliance_requirements': {
                    'iso_27001_certified': True,
                    'soc2_type2_compliant': True,
                    'gdpr_compliant': True,
                    'background_checks_performed': True,
                    'security_clearance_available': False  # Optional
                },
                'insurance_requirements': {
                    'professional_liability_minimum': 2000000,
                    'cyber_liability_minimum': 5000000,
                    'errors_omissions_minimum': 1000000,
                    'certificate_of_insurance_required': True
                },
                'legal_requirements': {
                    'nda_agreement_required': True,
                    'data_processing_agreement_required': True,
                    'liability_limitations_acceptable': True,
                    'indemnification_clauses_required': True,
                    'jurisdiction_requirements': ['US', 'EU']
                }
            },
            'evaluation_process': {
                'initial_screening': {
                    'application_review': True,
                    'reference_checks': True,
                    'certification_verification': True,
                    'financial_background_check': True
                },
                'technical_evaluation': {
                    'sample_report_review': True,
                    'technical_interview': True,
                    'methodology_presentation': True,
                    'tool_demonstration': True
                },
                'pilot_project': {
                    'small_scope_test': True,
                    'performance_evaluation': True,
                    'deliverable_quality_assessment': True,
                    'communication_effectiveness_review': True
                },
                'final_assessment': {
                    'scoring_criteria': {
                        'technical_competency': 40,
                        'reporting_quality': 25,
                        'communication_skills': 15,
                        'cost_effectiveness': 10,
                        'cultural_fit': 10
                    },
                    'minimum_passing_score': 75,
                    'approval_process': ['security_team', 'procurement', 'legal']
                }
            }
        }
        
        return qualification_framework
    
    def evaluate_vendor(self, vendor_id: str, evaluation_data: Dict) -> Dict:
        """
        Evaluate a penetration testing vendor
        """
        evaluation = {
            'evaluation_id': f"EVAL-{vendor_id}-{datetime.now().strftime('%Y%m%d')}",
            'vendor_id': vendor_id,
            'evaluation_date': datetime.now().isoformat(),
            'evaluator': evaluation_data['evaluator'],
            'evaluation_type': evaluation_data.get('evaluation_type', 'initial'),
            
            'technical_assessment': {
                'certifications_score': self.score_certifications(evaluation_data.get('certifications', [])),
                'experience_score': self.score_experience(evaluation_data.get('experience', {})),
                'methodology_score': self.score_methodology(evaluation_data.get('methodology', {})),
                'tool_proficiency_score': self.score_tool_proficiency(evaluation_data.get('tools', {})),
                'technical_interview_score': evaluation_data.get('technical_interview_score', 0)
            },
            
            'business_assessment': {
                'company_stability_score': self.score_company_stability(evaluation_data.get('company_info', {})),
                'compliance_score': self.score_compliance(evaluation_data.get('compliance', {})),
                'insurance_score': self.score_insurance(evaluation_data.get('insurance', {})),
                'legal_score': self.score_legal_requirements(evaluation_data.get('legal', {}))
            },
            
            'quality_assessment': {
                'sample_report_score': evaluation_data.get('sample_report_score', 0),
                'reference_check_score': self.score_reference_checks(evaluation_data.get('references', [])),
                'pilot_project_score': evaluation_data.get('pilot_project_score', 0),
                'communication_score': evaluation_data.get('communication_score', 0)
            },
            
            'cost_assessment': {
                'hourly_rate': evaluation_data.get('hourly_rate', 0),
                'project_rate': evaluation_data.get('project_rate', 0),
                'cost_competitiveness_score': self.score_cost_competitiveness(evaluation_data.get('pricing', {})),
                'value_for_money_score': evaluation_data.get('value_score', 0)
            }
        }
        
        # Calculate overall score
        evaluation['overall_score'] = self.calculate_overall_vendor_score(evaluation)
        evaluation['recommendation'] = self.generate_vendor_recommendation(evaluation)
        evaluation['approval_status'] = 'approved' if evaluation['overall_score'] >= 75 else 'rejected'
        
        # Store evaluation
        self.evaluations_table.put_item(Item=evaluation)
        
        return evaluation
    
    def score_certifications(self, certifications: List[Dict]) -> int:
        """
        Score vendor certifications
        """
        certification_weights = {
            'OSCP': 25,
            'GPEN': 20,
            'CEH': 15,
            'CISSP': 15,
            'GCIH': 10,
            'GSEC': 10,
            'CISM': 5
        }
        
        total_score = 0
        max_possible_score = 100
        
        for cert in certifications:
            cert_name = cert.get('name', '')
            team_members_with_cert = cert.get('team_members', 0)
            
            if cert_name in certification_weights:
                # Score based on certification value and team coverage
                cert_score = certification_weights[cert_name]
                coverage_multiplier = min(team_members_with_cert / 2, 1.0)  # Optimal at 2+ team members
                total_score += cert_score * coverage_multiplier
        
        return min(int(total_score), max_possible_score)
    
    def score_experience(self, experience: Dict) -> int:
        """
        Score vendor experience
        """
        score = 0
        
        # Years of experience (max 30 points)
        years = experience.get('years_in_business', 0)
        score += min(years * 3, 30)
        
        # Industry experience (max 25 points)
        if experience.get('similar_industry_experience', False):
            score += 25
        
        # Cloud security experience (max 25 points)
        if experience.get('cloud_security_experience', False):
            score += 25
        
        # Specialized experience (max 20 points)
        specializations = experience.get('specializations', [])
        score += min(len(specializations) * 5, 20)
        
        return min(score, 100)
    
    def score_methodology(self, methodology: Dict) -> int:
        """
        Score vendor methodology
        """
        score = 0
        
        # Framework support (max 40 points)
        frameworks = methodology.get('frameworks_supported', [])
        required_frameworks = ['OWASP', 'NIST', 'PTES']
        framework_score = sum(10 for fw in required_frameworks if fw in frameworks)
        score += min(framework_score, 40)
        
        # Testing approaches (max 30 points)
        approaches = methodology.get('testing_approaches', [])
        required_approaches = ['black_box', 'gray_box', 'white_box']
        approach_score = sum(10 for app in required_approaches if app in approaches)
        score += min(approach_score, 30)
        
        # Reporting quality (max 30 points)
        if methodology.get('detailed_reporting', False):
            score += 15
        if methodology.get('executive_summaries', False):
            score += 10
        if methodology.get('remediation_guidance', False):
            score += 5
        
        return min(score, 100)
    
    def create_vendor_contract_template(self, contract_config: Dict) -> Dict:
        """
        Create standardized contract template for penetration testing vendors
        """
        contract_template = {
            'contract_id': f"CONTRACT-{datetime.now().strftime('%Y%m%d')}-{contract_config['vendor_id']}",
            'vendor_id': contract_config['vendor_id'],
            'contract_type': contract_config.get('contract_type', 'master_services_agreement'),
            'effective_date': contract_config['effective_date'],
            'expiration_date': contract_config['expiration_date'],
            
            'scope_of_work': {
                'services_included': [
                    'web_application_penetration_testing',
                    'network_penetration_testing',
                    'wireless_security_assessment',
                    'social_engineering_testing',
                    'physical_security_assessment',
                    'cloud_security_assessment'
                ],
                'deliverables': [
                    'detailed_technical_report',
                    'executive_summary',
                    'remediation_recommendations',
                    'retest_validation',
                    'presentation_to_stakeholders'
                ],
                'testing_methodologies': contract_config.get('methodologies', ['OWASP', 'NIST']),
                'compliance_requirements': contract_config.get('compliance_frameworks', [])
            },
            
            'performance_requirements': {
                'response_time_sla': {
                    'initial_response': '4 hours',
                    'status_updates': 'daily',
                    'emergency_response': '1 hour'
                },
                'quality_standards': {
                    'false_positive_rate_max': 10,  # percentage
                    'report_delivery_timeline': '5 business days',
                    'retest_timeline': '30 days',
                    'minimum_coverage_percentage': 95
                },
                'team_requirements': {
                    'lead_tester_certifications': ['OSCP', 'GPEN'],
                    'minimum_team_size': 2,
                    'background_check_required': True,
                    'nda_signed_required': True
                }
            },
            
            'pricing_structure': {
                'pricing_model': contract_config.get('pricing_model', 'time_and_materials'),
                'hourly_rates': {
                    'senior_consultant': contract_config.get('senior_rate', 250),
                    'consultant': contract_config.get('consultant_rate', 200),
                    'junior_consultant': contract_config.get('junior_rate', 150)
                },
                'fixed_price_options': {
                    'web_app_assessment': contract_config.get('webapp_price', 15000),
                    'network_assessment': contract_config.get('network_price', 20000),
                    'comprehensive_assessment': contract_config.get('comprehensive_price', 35000)
                },
                'payment_terms': {
                    'payment_schedule': '30 days net',
                    'milestone_payments': True,
                    'expense_reimbursement': 'pre_approved_only'
                }
            },
            
            'security_requirements': {
                'data_handling': {
                    'data_classification_awareness': True,
                    'data_retention_policy': '90 days post completion',
                    'data_destruction_certificate': True,
                    'data_location_restrictions': ['US', 'EU']
                },
                'access_controls': {
                    'vpn_access_required': True,
                    'multi_factor_authentication': True,
                    'privileged_access_management': True,
                    'access_logging_required': True
                },
                'security_clearance': {
                    'background_checks_required': True,
                    'security_clearance_level': contract_config.get('clearance_level', 'none'),
                    'citizenship_requirements': contract_config.get('citizenship_requirements', [])
                }
            },
            
            'legal_terms': {
                'liability_limitations': {
                    'liability_cap': contract_config.get('liability_cap', 1000000),
                    'consequential_damages_excluded': True,
                    'indemnification_mutual': True
                },
                'intellectual_property': {
                    'work_product_ownership': 'client',
                    'tool_ownership': 'vendor',
                    'methodology_ownership': 'vendor',
                    'report_ownership': 'client'
                },
                'confidentiality': {
                    'nda_duration': '5 years',
                    'confidentiality_scope': 'all_client_information',
                    'permitted_disclosures': ['legal_requirements', 'court_orders']
                },
                'termination_clauses': {
                    'termination_for_convenience': '30 days notice',
                    'termination_for_cause': 'immediate',
                    'data_return_requirements': '30 days',
                    'final_payment_terms': 'pro_rated'
                }
            },
            
            'compliance_requirements': {
                'regulatory_compliance': contract_config.get('regulatory_requirements', []),
                'industry_standards': ['ISO 27001', 'SOC 2 Type II'],
                'audit_rights': {
                    'client_audit_rights': True,
                    'third_party_audit_acceptance': True,
                    'audit_frequency': 'annually'
                },
                'reporting_requirements': {
                    'compliance_reporting': True,
                    'incident_reporting': '24 hours',
                    'breach_notification': 'immediate'
                }
            },
            
            'service_level_agreements': {
                'availability_sla': '99.5%',
                'response_time_sla': {
                    'critical_issues': '1 hour',
                    'high_issues': '4 hours',
                    'medium_issues': '24 hours',
                    'low_issues': '72 hours'
                },
                'performance_metrics': {
                    'customer_satisfaction_target': 4.5,  # out of 5
                    'on_time_delivery_target': 95,  # percentage
                    'quality_score_target': 90  # percentage
                },
                'penalties_and_remedies': {
                    'sla_breach_penalties': True,
                    'service_credits': True,
                    'performance_improvement_plans': True
                }
            }
        }
        
        return contract_template
    
    def manage_vendor_performance(self, vendor_id: str, performance_period: Dict) -> Dict:
        """
        Manage and track vendor performance
        """
        performance_assessment = {
            'assessment_id': f"PERF-{vendor_id}-{datetime.now().strftime('%Y%m%d')}",
            'vendor_id': vendor_id,
            'assessment_period': performance_period,
            'assessment_date': datetime.now().isoformat(),
            
            'quantitative_metrics': {
                'projects_completed': 0,
                'on_time_delivery_rate': 0.0,
                'quality_score_average': 0.0,
                'customer_satisfaction_average': 0.0,
                'sla_compliance_rate': 0.0,
                'false_positive_rate': 0.0,
                'finding_accuracy_rate': 0.0
            },
            
            'qualitative_assessment': {
                'communication_effectiveness': {
                    'score': 0,
                    'comments': '',
                    'improvement_areas': []
                },
                'technical_competency': {
                    'score': 0,
                    'comments': '',
                    'strengths': [],
                    'weaknesses': []
                },
                'report_quality': {
                    'score': 0,
                    'comments': '',
                    'improvement_suggestions': []
                },
                'professionalism': {
                    'score': 0,
                    'comments': '',
                    'notable_incidents': []
                }
            },
            
            'improvement_areas': {
                'identified_gaps': [],
                'training_recommendations': [],
                'process_improvements': [],
                'tool_upgrades': []
            },
            
            'contract_compliance': {
                'sla_violations': [],
                'contract_breaches': [],
                'remediation_actions': [],
                'penalty_assessments': []
            },
            
            'overall_rating': 'satisfactory',  # excellent, satisfactory, needs_improvement, unsatisfactory
            'renewal_recommendation': True,
            'action_items': []
        }
        
        # Calculate performance metrics
        performance_assessment = self.calculate_vendor_performance_metrics(vendor_id, performance_assessment)
        
        # Store performance assessment
        self.evaluations_table.put_item(Item=performance_assessment)
        
        return performance_assessment
    
    def create_vendor_onboarding_process(self, vendor_id: str) -> Dict:
        """
        Create vendor onboarding process
        """
        onboarding_process = {
            'onboarding_id': f"ONBOARD-{vendor_id}-{datetime.now().strftime('%Y%m%d')}",
            'vendor_id': vendor_id,
            'start_date': datetime.now().isoformat(),
            'status': 'initiated',
            
            'onboarding_steps': [
                {
                    'step': 'contract_execution',
                    'description': 'Execute master services agreement',
                    'status': 'pending',
                    'responsible_party': 'legal_team',
                    'due_date': (datetime.now() + timedelta(days=7)).isoformat(),
                    'dependencies': ['vendor_evaluation_approved']
                },
                {
                    'step': 'insurance_verification',
                    'description': 'Verify insurance certificates',
                    'status': 'pending',
                    'responsible_party': 'procurement_team',
                    'due_date': (datetime.now() + timedelta(days=5)).isoformat(),
                    'dependencies': []
                },
                {
                    'step': 'security_clearance',
                    'description': 'Complete security clearance process',
                    'status': 'pending',
                    'responsible_party': 'security_team',
                    'due_date': (datetime.now() + timedelta(days=14)).isoformat(),
                    'dependencies': ['background_checks_completed']
                },
                {
                    'step': 'technical_setup',
                    'description': 'Set up technical access and tools',
                    'status': 'pending',
                    'responsible_party': 'it_team',
                    'due_date': (datetime.now() + timedelta(days=10)).isoformat(),
                    'dependencies': ['security_clearance_approved']
                },
                {
                    'step': 'orientation_training',
                    'description': 'Conduct vendor orientation and training',
                    'status': 'pending',
                    'responsible_party': 'security_team',
                    'due_date': (datetime.now() + timedelta(days=12)).isoformat(),
                    'dependencies': ['technical_setup_completed']
                },
                {
                    'step': 'pilot_project',
                    'description': 'Execute pilot penetration test',
                    'status': 'pending',
                    'responsible_party': 'security_team',
                    'due_date': (datetime.now() + timedelta(days=21)).isoformat(),
                    'dependencies': ['orientation_training_completed']
                },
                {
                    'step': 'performance_review',
                    'description': 'Review pilot project performance',
                    'status': 'pending',
                    'responsible_party': 'security_team',
                    'due_date': (datetime.now() + timedelta(days=28)).isoformat(),
                    'dependencies': ['pilot_project_completed']
                },
                {
                    'step': 'full_activation',
                    'description': 'Activate vendor for full services',
                    'status': 'pending',
                    'responsible_party': 'security_team',
                    'due_date': (datetime.now() + timedelta(days=30)).isoformat(),
                    'dependencies': ['performance_review_passed']
                }
            ],
            
            'required_documents': [
                'executed_contract',
                'insurance_certificates',
                'w9_tax_form',
                'security_questionnaire',
                'data_processing_agreement',
                'nda_agreement',
                'background_check_results',
                'certification_copies'
            ],
            
            'access_requirements': [
                'vpn_access',
                'testing_environment_access',
                'documentation_portal_access',
                'communication_channels',
                'project_management_tools'
            ],
            
            'training_requirements': [
                'company_security_policies',
                'data_handling_procedures',
                'incident_response_procedures',
                'reporting_standards',
                'communication_protocols'
            ]
        }
        
        return onboarding_process

# Example usage
vendor_mgmt = PentestVendorManagement()

# Create vendor qualification framework
qualification_framework = vendor_mgmt.create_vendor_qualification_framework()
print("Vendor Qualification Framework:")
print(json.dumps(qualification_framework, indent=2))

# Evaluate a vendor
evaluation_data = {
    'evaluator': 'security-manager@company.com',
    'certifications': [
        {'name': 'OSCP', 'team_members': 3},
        {'name': 'GPEN', 'team_members': 2},
        {'name': 'CEH', 'team_members': 4}
    ],
    'experience': {
        'years_in_business': 7,
        'similar_industry_experience': True,
        'cloud_security_experience': True,
        'specializations': ['web_apps', 'cloud', 'mobile']
    },
    'technical_interview_score': 85,
    'sample_report_score': 90,
    'communication_score': 88
}

vendor_evaluation = vendor_mgmt.evaluate_vendor('VENDOR-001', evaluation_data)
print(f"\\nVendor Evaluation Score: {vendor_evaluation['overall_score']}")
```
### Step 3: Implement Penetration Testing Results Management

Create comprehensive systems for managing penetration testing results and remediation:

```python
# Penetration Testing Results Management System
import boto3
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import hashlib

class PentestResultsManagement:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.s3 = boto3.client('s3')
        self.sns = boto3.client('sns')
        self.lambda_client = boto3.client('lambda')
        
        # DynamoDB tables
        self.findings_table = self.dynamodb.Table('pentest-findings')
        self.remediation_table = self.dynamodb.Table('pentest-remediation')
        self.metrics_table = self.dynamodb.Table('pentest-metrics')
        
    def process_penetration_test_results(self, test_id: str, results_data: Dict) -> Dict:
        """
        Process and normalize penetration test results
        """
        processed_results = {
            'processing_id': f"PROC-{test_id}-{datetime.now().strftime('%Y%m%d%H%M')}",
            'test_id': test_id,
            'processing_date': datetime.now().isoformat(),
            'raw_results': results_data,
            'normalized_findings': [],
            'risk_assessment': {},
            'remediation_plan': {},
            'compliance_impact': {},
            'executive_summary': {}
        }
        
        # Normalize findings from different sources
        if 'manual_findings' in results_data:
            manual_findings = self.normalize_manual_findings(results_data['manual_findings'])
            processed_results['normalized_findings'].extend(manual_findings)
        
        if 'automated_findings' in results_data:
            automated_findings = self.normalize_automated_findings(results_data['automated_findings'])
            processed_results['normalized_findings'].extend(automated_findings)
        
        # Deduplicate findings
        processed_results['normalized_findings'] = self.deduplicate_findings(
            processed_results['normalized_findings']
        )
        
        # Perform risk assessment
        processed_results['risk_assessment'] = self.assess_findings_risk(
            processed_results['normalized_findings']
        )
        
        # Create remediation plan
        processed_results['remediation_plan'] = self.create_remediation_plan(
            processed_results['normalized_findings']
        )
        
        # Assess compliance impact
        processed_results['compliance_impact'] = self.assess_compliance_impact(
            processed_results['normalized_findings']
        )
        
        # Generate executive summary
        processed_results['executive_summary'] = self.generate_executive_summary(
            processed_results
        )
        
        # Store processed results
        self.store_processed_results(processed_results)
        
        return processed_results
    
    def normalize_manual_findings(self, manual_findings: List[Dict]) -> List[Dict]:
        """
        Normalize manual penetration testing findings
        """
        normalized_findings = []
        
        for finding in manual_findings:
            normalized_finding = {
                'finding_id': self.generate_finding_id(finding),
                'source': 'manual_testing',
                'test_id': finding.get('test_id'),
                'category': finding.get('category', 'other'),
                'subcategory': finding.get('subcategory', ''),
                'title': finding.get('title', ''),
                'description': finding.get('description', ''),
                'severity': self.normalize_severity(finding.get('severity', 'medium')),
                'cvss_score': finding.get('cvss_score', 0.0),
                'cvss_vector': finding.get('cvss_vector', ''),
                'cwe_id': finding.get('cwe_id', ''),
                'owasp_category': finding.get('owasp_category', ''),
                'affected_assets': finding.get('affected_assets', []),
                'attack_vector': finding.get('attack_vector', ''),
                'attack_complexity': finding.get('attack_complexity', 'unknown'),
                'privileges_required': finding.get('privileges_required', 'unknown'),
                'user_interaction': finding.get('user_interaction', 'unknown'),
                'scope': finding.get('scope', 'unchanged'),
                'confidentiality_impact': finding.get('confidentiality_impact', 'none'),
                'integrity_impact': finding.get('integrity_impact', 'none'),
                'availability_impact': finding.get('availability_impact', 'none'),
                'exploitability': finding.get('exploitability', 'unknown'),
                'proof_of_concept': finding.get('proof_of_concept', ''),
                'evidence': finding.get('evidence', []),
                'business_impact': finding.get('business_impact', ''),
                'remediation_effort': finding.get('remediation_effort', 'unknown'),
                'remediation_priority': self.calculate_remediation_priority(finding),
                'false_positive_likelihood': finding.get('false_positive_likelihood', 'low'),
                'retest_required': finding.get('retest_required', True),
                'compliance_violations': finding.get('compliance_violations', []),
                'references': finding.get('references', []),
                'discovered_date': finding.get('discovered_date', datetime.now().isoformat()),
                'tester': finding.get('tester', ''),
                'testing_phase': finding.get('testing_phase', ''),
                'status': 'open'
            }
            
            normalized_findings.append(normalized_finding)
        
        return normalized_findings
    
    def normalize_automated_findings(self, automated_findings: List[Dict]) -> List[Dict]:
        """
        Normalize automated tool findings
        """
        normalized_findings = []
        
        for finding in automated_findings:
            # Map automated tool output to standardized format
            normalized_finding = {
                'finding_id': self.generate_finding_id(finding),
                'source': f"automated_{finding.get('tool', 'unknown')}",
                'tool_name': finding.get('tool', ''),
                'tool_version': finding.get('tool_version', ''),
                'scan_id': finding.get('scan_id', ''),
                'category': self.map_tool_category(finding.get('category', '')),
                'title': finding.get('name', finding.get('title', '')),
                'description': finding.get('description', ''),
                'severity': self.normalize_severity(finding.get('severity', 'medium')),
                'confidence': finding.get('confidence', 'medium'),
                'cvss_score': finding.get('cvss_score', 0.0),
                'affected_assets': [finding.get('host', finding.get('url', ''))],
                'port': finding.get('port', ''),
                'protocol': finding.get('protocol', ''),
                'service': finding.get('service', ''),
                'plugin_id': finding.get('plugin_id', ''),
                'vulnerability_id': finding.get('vulnerability_id', ''),
                'cve_ids': finding.get('cve_ids', []),
                'cwe_id': finding.get('cwe_id', ''),
                'solution': finding.get('solution', ''),
                'references': finding.get('references', []),
                'first_seen': finding.get('first_seen', datetime.now().isoformat()),
                'last_seen': finding.get('last_seen', datetime.now().isoformat()),
                'false_positive_likelihood': self.assess_false_positive_likelihood(finding),
                'manual_verification_required': True,
                'status': 'pending_verification'
            }
            
            normalized_findings.append(normalized_finding)
        
        return normalized_findings
    
    def deduplicate_findings(self, findings: List[Dict]) -> List[Dict]:
        """
        Remove duplicate findings based on similarity analysis
        """
        deduplicated_findings = []
        finding_signatures = set()
        
        for finding in findings:
            # Create signature for deduplication
            signature_data = {
                'category': finding.get('category', ''),
                'title': finding.get('title', ''),
                'affected_asset': finding.get('affected_assets', [None])[0],
                'severity': finding.get('severity', ''),
                'cwe_id': finding.get('cwe_id', '')
            }
            
            signature = hashlib.md5(
                json.dumps(signature_data, sort_keys=True).encode()
            ).hexdigest()
            
            if signature not in finding_signatures:
                finding_signatures.add(signature)
                finding['deduplication_signature'] = signature
                deduplicated_findings.append(finding)
            else:
                # Mark as duplicate and reference original
                finding['status'] = 'duplicate'
                finding['duplicate_of'] = signature
        
        return deduplicated_findings
    
    def assess_findings_risk(self, findings: List[Dict]) -> Dict:
        """
        Assess overall risk from penetration test findings
        """
        risk_assessment = {
            'overall_risk_score': 0.0,
            'risk_level': 'low',
            'critical_findings_count': 0,
            'high_findings_count': 0,
            'medium_findings_count': 0,
            'low_findings_count': 0,
            'risk_by_category': {},
            'risk_by_asset': {},
            'business_risk_factors': [],
            'technical_risk_factors': [],
            'compliance_risk_factors': []
        }
        
        # Count findings by severity
        for finding in findings:
            severity = finding.get('severity', 'low').lower()
            if severity == 'critical':
                risk_assessment['critical_findings_count'] += 1
            elif severity == 'high':
                risk_assessment['high_findings_count'] += 1
            elif severity == 'medium':
                risk_assessment['medium_findings_count'] += 1
            else:
                risk_assessment['low_findings_count'] += 1
        
        # Calculate overall risk score
        risk_score = (
            risk_assessment['critical_findings_count'] * 10 +
            risk_assessment['high_findings_count'] * 7 +
            risk_assessment['medium_findings_count'] * 4 +
            risk_assessment['low_findings_count'] * 1
        )
        
        risk_assessment['overall_risk_score'] = risk_score
        
        # Determine risk level
        if risk_score >= 50:
            risk_assessment['risk_level'] = 'critical'
        elif risk_score >= 30:
            risk_assessment['risk_level'] = 'high'
        elif risk_score >= 15:
            risk_assessment['risk_level'] = 'medium'
        else:
            risk_assessment['risk_level'] = 'low'
        
        # Analyze risk by category
        category_risks = {}
        for finding in findings:
            category = finding.get('category', 'other')
            if category not in category_risks:
                category_risks[category] = {'count': 0, 'max_severity': 'low'}
            
            category_risks[category]['count'] += 1
            current_severity = category_risks[category]['max_severity']
            finding_severity = finding.get('severity', 'low')
            
            if self.severity_to_numeric(finding_severity) > self.severity_to_numeric(current_severity):
                category_risks[category]['max_severity'] = finding_severity
        
        risk_assessment['risk_by_category'] = category_risks
        
        # Identify key risk factors
        risk_assessment['business_risk_factors'] = self.identify_business_risk_factors(findings)
        risk_assessment['technical_risk_factors'] = self.identify_technical_risk_factors(findings)
        risk_assessment['compliance_risk_factors'] = self.identify_compliance_risk_factors(findings)
        
        return risk_assessment
    
    def create_remediation_plan(self, findings: List[Dict]) -> Dict:
        """
        Create comprehensive remediation plan
        """
        remediation_plan = {
            'plan_id': f"REMED-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            'created_date': datetime.now().isoformat(),
            'total_findings': len(findings),
            'remediation_phases': [],
            'resource_requirements': {},
            'timeline_estimate': {},
            'success_criteria': {},
            'risk_mitigation_priorities': []
        }
        
        # Sort findings by remediation priority
        prioritized_findings = sorted(
            findings,
            key=lambda x: (
                self.severity_to_numeric(x.get('severity', 'low')),
                x.get('exploitability', 'unknown') == 'high',
                len(x.get('affected_assets', []))
            ),
            reverse=True
        )
        
        # Create remediation phases
        phases = {
            'immediate': {'findings': [], 'timeline': '1-7 days', 'description': 'Critical security issues requiring immediate attention'},
            'short_term': {'findings': [], 'timeline': '1-4 weeks', 'description': 'High-priority issues with significant risk'},
            'medium_term': {'findings': [], 'timeline': '1-3 months', 'description': 'Medium-priority issues for planned remediation'},
            'long_term': {'findings': [], 'timeline': '3-6 months', 'description': 'Lower-priority issues for future remediation'}
        }
        
        # Assign findings to phases
        for finding in prioritized_findings:
            severity = finding.get('severity', 'low').lower()
            exploitability = finding.get('exploitability', 'unknown').lower()
            
            if severity == 'critical' or (severity == 'high' and exploitability == 'high'):
                phases['immediate']['findings'].append(finding)
            elif severity == 'high' or (severity == 'medium' and exploitability == 'high'):
                phases['short_term']['findings'].append(finding)
            elif severity == 'medium':
                phases['medium_term']['findings'].append(finding)
            else:
                phases['long_term']['findings'].append(finding)
        
        # Create detailed phase plans
        for phase_name, phase_data in phases.items():
            if phase_data['findings']:
                phase_plan = {
                    'phase': phase_name,
                    'timeline': phase_data['timeline'],
                    'description': phase_data['description'],
                    'findings_count': len(phase_data['findings']),
                    'findings': phase_data['findings'],
                    'remediation_actions': self.generate_remediation_actions(phase_data['findings']),
                    'resource_requirements': self.estimate_phase_resources(phase_data['findings']),
                    'success_metrics': self.define_phase_success_metrics(phase_data['findings'])
                }
                remediation_plan['remediation_phases'].append(phase_plan)
        
        # Calculate overall resource requirements
        remediation_plan['resource_requirements'] = self.calculate_total_resources(
            remediation_plan['remediation_phases']
        )
        
        # Create timeline estimate
        remediation_plan['timeline_estimate'] = self.create_timeline_estimate(
            remediation_plan['remediation_phases']
        )
        
        return remediation_plan
    
    def generate_remediation_actions(self, findings: List[Dict]) -> List[Dict]:
        """
        Generate specific remediation actions for findings
        """
        actions = []
        
        # Group findings by category for efficient remediation
        findings_by_category = {}
        for finding in findings:
            category = finding.get('category', 'other')
            if category not in findings_by_category:
                findings_by_category[category] = []
            findings_by_category[category].append(finding)
        
        # Generate category-specific actions
        for category, category_findings in findings_by_category.items():
            category_actions = self.get_category_remediation_actions(category, category_findings)
            actions.extend(category_actions)
        
        return actions
    
    def get_category_remediation_actions(self, category: str, findings: List[Dict]) -> List[Dict]:
        """
        Get remediation actions for specific vulnerability category
        """
        action_templates = {
            'injection': [
                {
                    'action': 'implement_input_validation',
                    'description': 'Implement comprehensive input validation and sanitization',
                    'effort_estimate': 'medium',
                    'technical_complexity': 'medium',
                    'business_impact': 'low'
                },
                {
                    'action': 'use_parameterized_queries',
                    'description': 'Replace dynamic SQL with parameterized queries',
                    'effort_estimate': 'high',
                    'technical_complexity': 'medium',
                    'business_impact': 'low'
                }
            ],
            'authentication': [
                {
                    'action': 'implement_mfa',
                    'description': 'Implement multi-factor authentication',
                    'effort_estimate': 'medium',
                    'technical_complexity': 'low',
                    'business_impact': 'medium'
                },
                {
                    'action': 'strengthen_password_policy',
                    'description': 'Implement stronger password policies',
                    'effort_estimate': 'low',
                    'technical_complexity': 'low',
                    'business_impact': 'low'
                }
            ],
            'authorization': [
                {
                    'action': 'implement_rbac',
                    'description': 'Implement role-based access control',
                    'effort_estimate': 'high',
                    'technical_complexity': 'high',
                    'business_impact': 'medium'
                },
                {
                    'action': 'review_access_controls',
                    'description': 'Review and update access control mechanisms',
                    'effort_estimate': 'medium',
                    'technical_complexity': 'medium',
                    'business_impact': 'low'
                }
            ],
            'encryption': [
                {
                    'action': 'implement_data_encryption',
                    'description': 'Implement encryption for sensitive data',
                    'effort_estimate': 'medium',
                    'technical_complexity': 'medium',
                    'business_impact': 'low'
                },
                {
                    'action': 'enforce_tls',
                    'description': 'Enforce TLS for all communications',
                    'effort_estimate': 'low',
                    'technical_complexity': 'low',
                    'business_impact': 'low'
                }
            ]
        }
        
        actions = []
        category_templates = action_templates.get(category, [])
        
        for template in category_templates:
            action = {
                **template,
                'category': category,
                'affected_findings': [f['finding_id'] for f in findings],
                'priority': self.calculate_action_priority(template, findings),
                'estimated_completion_date': self.estimate_completion_date(template),
                'assigned_team': self.determine_responsible_team(category),
                'dependencies': self.identify_action_dependencies(template, category),
                'success_criteria': self.define_action_success_criteria(template, findings)
            }
            actions.append(action)
        
        return actions
    
    def track_remediation_progress(self, remediation_plan_id: str) -> Dict:
        """
        Track progress of remediation activities
        """
        progress_tracking = {
            'tracking_id': f"TRACK-{remediation_plan_id}-{datetime.now().strftime('%Y%m%d')}",
            'remediation_plan_id': remediation_plan_id,
            'tracking_date': datetime.now().isoformat(),
            'overall_progress': 0.0,
            'phase_progress': {},
            'completed_actions': [],
            'in_progress_actions': [],
            'blocked_actions': [],
            'overdue_actions': [],
            'risk_reduction_achieved': 0.0,
            'next_milestones': [],
            'escalation_required': False
        }
        
        # Get remediation plan details
        remediation_plan = self.get_remediation_plan(remediation_plan_id)
        
        # Track progress for each phase
        total_actions = 0
        completed_actions = 0
        
        for phase in remediation_plan.get('remediation_phases', []):
            phase_name = phase['phase']
            phase_actions = phase.get('remediation_actions', [])
            phase_completed = 0
            
            for action in phase_actions:
                total_actions += 1
                action_status = self.get_action_status(action['action'])
                
                if action_status == 'completed':
                    completed_actions += 1
                    phase_completed += 1
                    progress_tracking['completed_actions'].append(action)
                elif action_status == 'in_progress':
                    progress_tracking['in_progress_actions'].append(action)
                elif action_status == 'blocked':
                    progress_tracking['blocked_actions'].append(action)
                elif self.is_action_overdue(action):
                    progress_tracking['overdue_actions'].append(action)
            
            phase_progress = (phase_completed / len(phase_actions)) * 100 if phase_actions else 0
            progress_tracking['phase_progress'][phase_name] = phase_progress
        
        # Calculate overall progress
        progress_tracking['overall_progress'] = (completed_actions / total_actions) * 100 if total_actions > 0 else 0
        
        # Calculate risk reduction
        progress_tracking['risk_reduction_achieved'] = self.calculate_risk_reduction(
            remediation_plan_id,
            progress_tracking['completed_actions']
        )
        
        # Identify next milestones
        progress_tracking['next_milestones'] = self.identify_next_milestones(
            progress_tracking['in_progress_actions']
        )
        
        # Determine if escalation is required
        progress_tracking['escalation_required'] = (
            len(progress_tracking['overdue_actions']) > 0 or
            len(progress_tracking['blocked_actions']) > 0 or
            progress_tracking['overall_progress'] < 50  # Behind schedule
        )
        
        # Store progress tracking
        self.remediation_table.put_item(Item=progress_tracking)
        
        return progress_tracking
    
    def generate_finding_id(self, finding: Dict) -> str:
        """
        Generate unique finding ID
        """
        finding_data = {
            'title': finding.get('title', ''),
            'category': finding.get('category', ''),
            'asset': finding.get('affected_assets', [None])[0],
            'timestamp': datetime.now().strftime('%Y%m%d')
        }
        
        hash_input = json.dumps(finding_data, sort_keys=True)
        finding_hash = hashlib.md5(hash_input.encode()).hexdigest()[:8]
        
        return f"FIND-{finding_hash.upper()}"
    
    def normalize_severity(self, severity: str) -> str:
        """
        Normalize severity levels across different sources
        """
        severity_mapping = {
            'critical': 'critical',
            'high': 'high',
            'medium': 'medium',
            'low': 'low',
            'info': 'info',
            'informational': 'info',
            '4': 'critical',
            '3': 'high',
            '2': 'medium',
            '1': 'low',
            '0': 'info'
        }
        
        return severity_mapping.get(str(severity).lower(), 'medium')
    
    def severity_to_numeric(self, severity: str) -> int:
        """
        Convert severity to numeric value for comparison
        """
        severity_values = {
            'critical': 4,
            'high': 3,
            'medium': 2,
            'low': 1,
            'info': 0
        }
        
        return severity_values.get(severity.lower(), 2)

# Example usage
results_mgmt = PentestResultsManagement()

# Process penetration test results
test_results = {
    'manual_findings': [
        {
            'title': 'SQL Injection in Login Form',
            'category': 'injection',
            'severity': 'high',
            'description': 'SQL injection vulnerability found in login form',
            'affected_assets': ['https://app.company.com/login'],
            'cvss_score': 8.1,
            'proof_of_concept': 'admin\' OR \'1\'=\'1\' --',
            'business_impact': 'Potential unauthorized access to user accounts'
        }
    ],
    'automated_findings': [
        {
            'tool': 'nessus',
            'name': 'SSL Certificate Expired',
            'severity': 'medium',
            'host': 'api.company.com',
            'port': '443',
            'description': 'SSL certificate has expired'
        }
    ]
}

processed_results = results_mgmt.process_penetration_test_results('PENTEST-001', test_results)
print("Processed Results:")
print(json.dumps(processed_results['risk_assessment'], indent=2))
```
### Step 4: Integrate with AWS Security Services

Leverage AWS services to enhance penetration testing capabilities and results management:

```python
# AWS Security Services Integration for Penetration Testing
import boto3
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class AWSPentestIntegration:
    def __init__(self):
        self.security_hub = boto3.client('securityhub')
        self.inspector = boto3.client('inspector2')
        self.guardduty = boto3.client('guardduty')
        self.config = boto3.client('config')
        self.cloudtrail = boto3.client('cloudtrail')
        self.systems_manager = boto3.client('ssm')
        
    def integrate_with_security_hub(self, pentest_findings: List[Dict]) -> Dict:
        """
        Import penetration test findings into AWS Security Hub
        """
        security_hub_findings = []
        
        for finding in pentest_findings:
            # Convert pentest finding to Security Hub format
            security_hub_finding = {
                'SchemaVersion': '2018-10-08',
                'Id': f"pentest/{finding['finding_id']}",
                'ProductArn': f"arn:aws:securityhub:{boto3.Session().region_name}:{boto3.client('sts').get_caller_identity()['Account']}:product/custom/penetration-testing",
                'GeneratorId': 'penetration-testing-program',
                'AwsAccountId': boto3.client('sts').get_caller_identity()['Account'],
                'CreatedAt': finding.get('discovered_date', datetime.now().isoformat()),
                'UpdatedAt': datetime.now().isoformat(),
                'Severity': {
                    'Label': finding.get('severity', 'MEDIUM').upper()
                },
                'Title': finding.get('title', 'Penetration Test Finding'),
                'Description': finding.get('description', ''),
                'Types': [
                    'Sensitive Data Identifications',
                    'Security Findings'
                ],
                'SourceUrl': f"https://pentest-portal.company.com/findings/{finding['finding_id']}",
                'Remediation': {
                    'Recommendation': {
                        'Text': finding.get('remediation_recommendation', 'See detailed report for remediation guidance'),
                        'Url': f"https://pentest-portal.company.com/remediation/{finding['finding_id']}"
                    }
                },
                'Resources': self.map_finding_resources(finding),
                'Compliance': {
                    'Status': 'FAILED' if finding.get('severity') in ['critical', 'high'] else 'WARNING'
                },
                'Workflow': {
                    'Status': 'NEW'
                },
                'RecordState': 'ACTIVE',
                'Note': {
                    'Text': f"Finding from penetration test {finding.get('test_id', 'unknown')}",
                    'UpdatedBy': 'penetration-testing-program',
                    'UpdatedAt': datetime.now().isoformat()
                }
            }
            
            # Add CVSS information if available
            if finding.get('cvss_score'):
                security_hub_finding['Severity']['Normalized'] = int(finding['cvss_score'] * 10)
                
            # Add CWE information if available
            if finding.get('cwe_id'):
                security_hub_finding['Types'].append(f"CWE-{finding['cwe_id']}")
            
            security_hub_findings.append(security_hub_finding)
        
        # Batch import findings to Security Hub
        if security_hub_findings:
            response = self.security_hub.batch_import_findings(
                Findings=security_hub_findings
            )
            
            return {
                'imported_findings': len(security_hub_findings),
                'successful_imports': response.get('SuccessCount', 0),
                'failed_imports': response.get('FailedCount', 0),
                'failed_findings': response.get('FailedFindings', [])
            }
        
        return {'imported_findings': 0}
    
    def map_finding_resources(self, finding: Dict) -> List[Dict]:
        """
        Map penetration test finding to AWS resources
        """
        resources = []
        
        for asset in finding.get('affected_assets', []):
            if asset.startswith('arn:aws:'):
                # Direct AWS resource ARN
                resources.append({
                    'Type': 'AwsResource',
                    'Id': asset,
                    'Region': boto3.Session().region_name
                })
            elif '.' in asset and ('http' in asset or 'https' in asset):
                # Web application or API endpoint
                resources.append({
                    'Type': 'Other',
                    'Id': asset,
                    'Details': {
                        'Other': {
                            'ResourceType': 'WebApplication',
                            'Url': asset
                        }
                    }
                })
            else:
                # Generic resource
                resources.append({
                    'Type': 'Other',
                    'Id': asset,
                    'Details': {
                        'Other': {
                            'ResourceType': 'NetworkResource'
                        }
                    }
                })
        
        return resources
    
    def create_pentest_environment(self, environment_config: Dict) -> Dict:
        """
        Create isolated AWS environment for penetration testing
        """
        environment_setup = {
            'environment_id': f"pentest-env-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            'created_date': datetime.now().isoformat(),
            'configuration': environment_config,
            'resources_created': [],
            'access_configuration': {},
            'monitoring_setup': {},
            'cleanup_schedule': {}
        }
        
        # Create VPC for isolated testing
        vpc_config = self.create_pentest_vpc(environment_config)
        environment_setup['resources_created'].append(vpc_config)
        
        # Set up monitoring and logging
        monitoring_config = self.setup_pentest_monitoring(environment_config)
        environment_setup['monitoring_setup'] = monitoring_config
        
        # Configure access controls
        access_config = self.configure_pentest_access(environment_config)
        environment_setup['access_configuration'] = access_config
        
        # Schedule cleanup
        cleanup_config = self.schedule_environment_cleanup(environment_config)
        environment_setup['cleanup_schedule'] = cleanup_config
        
        return environment_setup
    
    def create_pentest_vpc(self, config: Dict) -> Dict:
        """
        Create VPC for penetration testing
        """
        ec2 = boto3.client('ec2')
        
        # Create VPC
        vpc_response = ec2.create_vpc(
            CidrBlock=config.get('vpc_cidr', '10.100.0.0/16'),
            TagSpecifications=[
                {
                    'ResourceType': 'vpc',
                    'Tags': [
                        {'Key': 'Name', 'Value': f"pentest-vpc-{config.get('test_id', 'unknown')}"},
                        {'Key': 'Purpose', 'Value': 'PenetrationTesting'},
                        {'Key': 'Environment', 'Value': 'testing'},
                        {'Key': 'AutoCleanup', 'Value': 'true'},
                        {'Key': 'CleanupDate', 'Value': (datetime.now() + timedelta(days=7)).isoformat()}
                    ]
                }
            ]
        )
        
        vpc_id = vpc_response['Vpc']['VpcId']
        
        # Create subnets
        public_subnet = ec2.create_subnet(
            VpcId=vpc_id,
            CidrBlock=config.get('public_subnet_cidr', '10.100.1.0/24'),
            TagSpecifications=[
                {
                    'ResourceType': 'subnet',
                    'Tags': [
                        {'Key': 'Name', 'Value': f"pentest-public-subnet-{config.get('test_id', 'unknown')}"},
                        {'Key': 'Type', 'Value': 'Public'}
                    ]
                }
            ]
        )
        
        private_subnet = ec2.create_subnet(
            VpcId=vpc_id,
            CidrBlock=config.get('private_subnet_cidr', '10.100.2.0/24'),
            TagSpecifications=[
                {
                    'ResourceType': 'subnet',
                    'Tags': [
                        {'Key': 'Name', 'Value': f"pentest-private-subnet-{config.get('test_id', 'unknown')}"},
                        {'Key': 'Type', 'Value': 'Private'}
                    ]
                }
            ]
        )
        
        # Create Internet Gateway
        igw_response = ec2.create_internet_gateway(
            TagSpecifications=[
                {
                    'ResourceType': 'internet-gateway',
                    'Tags': [
                        {'Key': 'Name', 'Value': f"pentest-igw-{config.get('test_id', 'unknown')}"}
                    ]
                }
            ]
        )
        
        igw_id = igw_response['InternetGateway']['InternetGatewayId']
        
        # Attach Internet Gateway to VPC
        ec2.attach_internet_gateway(
            InternetGatewayId=igw_id,
            VpcId=vpc_id
        )
        
        # Create security groups
        pentest_sg = ec2.create_security_group(
            GroupName=f"pentest-sg-{config.get('test_id', 'unknown')}",
            Description='Security group for penetration testing',
            VpcId=vpc_id,
            TagSpecifications=[
                {
                    'ResourceType': 'security-group',
                    'Tags': [
                        {'Key': 'Name', 'Value': f"pentest-sg-{config.get('test_id', 'unknown')}"}
                    ]
                }
            ]
        )
        
        sg_id = pentest_sg['GroupId']
        
        # Configure security group rules for testing
        ec2.authorize_security_group_ingress(
            GroupId=sg_id,
            IpPermissions=[
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 22,
                    'ToPort': 22,
                    'IpRanges': [{'CidrIp': config.get('tester_ip_range', '0.0.0.0/0')}]
                },
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 80,
                    'ToPort': 80,
                    'IpRanges': [{'CidrIp': '10.100.0.0/16'}]
                },
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 443,
                    'ToPort': 443,
                    'IpRanges': [{'CidrIp': '10.100.0.0/16'}]
                }
            ]
        )
        
        return {
            'vpc_id': vpc_id,
            'public_subnet_id': public_subnet['Subnet']['SubnetId'],
            'private_subnet_id': private_subnet['Subnet']['SubnetId'],
            'internet_gateway_id': igw_id,
            'security_group_id': sg_id
        }
    
    def setup_pentest_monitoring(self, config: Dict) -> Dict:
        """
        Set up monitoring and logging for penetration testing
        """
        cloudwatch = boto3.client('cloudwatch')
        logs = boto3.client('logs')
        
        # Create CloudWatch log group for pentest activities
        log_group_name = f"/aws/pentest/{config.get('test_id', 'unknown')}"
        
        try:
            logs.create_log_group(
                logGroupName=log_group_name,
                tags={
                    'Purpose': 'PenetrationTesting',
                    'TestId': config.get('test_id', 'unknown'),
                    'RetentionDays': '30'
                }
            )
            
            # Set retention policy
            logs.put_retention_policy(
                logGroupName=log_group_name,
                retentionInDays=30
            )
            
        except logs.exceptions.ResourceAlreadyExistsException:
            pass  # Log group already exists
        
        # Create custom metrics for pentest activities
        custom_metrics = [
            {
                'MetricName': 'PentestFindingsCount',
                'Namespace': 'PenetrationTesting',
                'Dimensions': [
                    {'Name': 'TestId', 'Value': config.get('test_id', 'unknown')},
                    {'Name': 'Severity', 'Value': 'Critical'}
                ]
            },
            {
                'MetricName': 'PentestProgress',
                'Namespace': 'PenetrationTesting',
                'Dimensions': [
                    {'Name': 'TestId', 'Value': config.get('test_id', 'unknown')},
                    {'Name': 'Phase', 'Value': 'Overall'}
                ]
            }
        ]
        
        # Create CloudWatch alarms for critical findings
        alarm_config = {
            'AlarmName': f"pentest-critical-findings-{config.get('test_id', 'unknown')}",
            'ComparisonOperator': 'GreaterThanThreshold',
            'EvaluationPeriods': 1,
            'MetricName': 'PentestFindingsCount',
            'Namespace': 'PenetrationTesting',
            'Period': 300,
            'Statistic': 'Sum',
            'Threshold': 0.0,
            'ActionsEnabled': True,
            'AlarmActions': [
                config.get('notification_topic_arn', '')
            ],
            'AlarmDescription': 'Alert when critical penetration test findings are discovered',
            'Dimensions': [
                {'Name': 'TestId', 'Value': config.get('test_id', 'unknown')},
                {'Name': 'Severity', 'Value': 'Critical'}
            ]
        }
        
        if config.get('notification_topic_arn'):
            cloudwatch.put_metric_alarm(**alarm_config)
        
        return {
            'log_group_name': log_group_name,
            'custom_metrics': custom_metrics,
            'alarms_created': [alarm_config['AlarmName']] if config.get('notification_topic_arn') else []
        }
    
    def generate_compliance_report(self, pentest_results: Dict, compliance_frameworks: List[str]) -> Dict:
        """
        Generate compliance report based on penetration test results
        """
        compliance_report = {
            'report_id': f"COMPLIANCE-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            'generated_date': datetime.now().isoformat(),
            'test_id': pentest_results.get('test_id'),
            'frameworks_assessed': compliance_frameworks,
            'compliance_status': {},
            'findings_by_framework': {},
            'remediation_requirements': {},
            'certification_impact': {}
        }
        
        findings = pentest_results.get('normalized_findings', [])
        
        for framework in compliance_frameworks:
            framework_assessment = self.assess_framework_compliance(framework, findings)
            compliance_report['compliance_status'][framework] = framework_assessment
            
            framework_findings = self.map_findings_to_framework(framework, findings)
            compliance_report['findings_by_framework'][framework] = framework_findings
            
            remediation_reqs = self.get_framework_remediation_requirements(framework, framework_findings)
            compliance_report['remediation_requirements'][framework] = remediation_reqs
            
            cert_impact = self.assess_certification_impact(framework, framework_findings)
            compliance_report['certification_impact'][framework] = cert_impact
        
        return compliance_report
    
    def assess_framework_compliance(self, framework: str, findings: List[Dict]) -> Dict:
        """
        Assess compliance status for specific framework
        """
        framework_mappings = {
            'PCI-DSS': {
                'critical_controls': ['encryption', 'access_control', 'network_security'],
                'acceptable_risk_level': 'medium',
                'critical_finding_threshold': 0
            },
            'SOC2': {
                'critical_controls': ['access_control', 'monitoring', 'encryption'],
                'acceptable_risk_level': 'medium',
                'critical_finding_threshold': 0
            },
            'HIPAA': {
                'critical_controls': ['encryption', 'access_control', 'audit_logging'],
                'acceptable_risk_level': 'low',
                'critical_finding_threshold': 0
            },
            'ISO27001': {
                'critical_controls': ['access_control', 'encryption', 'incident_management'],
                'acceptable_risk_level': 'medium',
                'critical_finding_threshold': 1
            }
        }
        
        framework_config = framework_mappings.get(framework, {})
        critical_controls = framework_config.get('critical_controls', [])
        
        # Count findings affecting critical controls
        critical_findings = 0
        high_findings = 0
        affected_controls = set()
        
        for finding in findings:
            if finding.get('severity') == 'critical':
                critical_findings += 1
            elif finding.get('severity') == 'high':
                high_findings += 1
            
            finding_category = finding.get('category', '')
            if finding_category in critical_controls:
                affected_controls.add(finding_category)
        
        # Determine compliance status
        compliance_status = 'compliant'
        if critical_findings > framework_config.get('critical_finding_threshold', 0):
            compliance_status = 'non_compliant'
        elif high_findings > 5 or len(affected_controls) > len(critical_controls) / 2:
            compliance_status = 'at_risk'
        
        return {
            'status': compliance_status,
            'critical_findings_count': critical_findings,
            'high_findings_count': high_findings,
            'affected_controls': list(affected_controls),
            'compliance_score': max(0, 100 - (critical_findings * 25) - (high_findings * 10)),
            'remediation_required': compliance_status != 'compliant'
        }

# Example usage
aws_integration = AWSPentestIntegration()

# Integrate pentest findings with Security Hub
pentest_findings = [
    {
        'finding_id': 'FIND-12345678',
        'test_id': 'PENTEST-001',
        'title': 'SQL Injection Vulnerability',
        'description': 'SQL injection found in login form',
        'severity': 'high',
        'cvss_score': 8.1,
        'affected_assets': ['https://app.company.com/login'],
        'discovered_date': datetime.now().isoformat()
    }
]

security_hub_result = aws_integration.integrate_with_security_hub(pentest_findings)
print("Security Hub Integration:")
print(json.dumps(security_hub_result, indent=2))

# Generate compliance report
compliance_report = aws_integration.generate_compliance_report(
    {'test_id': 'PENTEST-001', 'normalized_findings': pentest_findings},
    ['PCI-DSS', 'SOC2']
)
print("\\nCompliance Report:")
print(json.dumps(compliance_report['compliance_status'], indent=2))
```

## Best Practices for Penetration Testing

### 1. Establish Clear Scope and Objectives

**Define Testing Scope**: Clearly define what systems, applications, and networks are in scope for testing, as well as any exclusions or limitations.

**Set Clear Objectives**: Establish specific goals for each penetration test, such as validating specific controls, testing incident response, or meeting compliance requirements.

**Document Rules of Engagement**: Create detailed rules of engagement that specify testing methods, timing, communication protocols, and emergency procedures.

### 2. Use Risk-Based Testing Approach

**Prioritize High-Risk Assets**: Focus testing efforts on the most critical and high-risk systems and applications.

**Threat-Informed Testing**: Base testing scenarios on relevant threat intelligence and known attack patterns for your industry.

**Business Context**: Consider business impact and criticality when planning tests and interpreting results.

### 3. Combine Multiple Testing Approaches

**Black Box, Gray Box, and White Box**: Use different testing approaches to get comprehensive coverage and validate security from multiple perspectives.

**Internal and External Testing**: Conduct both external (internet-facing) and internal (insider threat) penetration tests.

**Automated and Manual Testing**: Combine automated tools with manual testing techniques to achieve thorough coverage.

### 4. Ensure Quality and Accuracy

**Qualified Testers**: Use experienced, certified penetration testers with relevant expertise for your environment.

**Methodology Standards**: Follow established methodologies like OWASP, NIST, or PTES to ensure comprehensive and consistent testing.

**Quality Assurance**: Implement quality assurance processes to validate findings and reduce false positives.

## Common Challenges and Solutions

### Challenge 1: Balancing Testing Frequency with Resource Constraints

**Problem**: Limited budget and resources for conducting regular penetration tests.

**Solutions**:
- Implement risk-based testing schedules
- Use automated tools to supplement manual testing
- Focus on critical assets and high-risk areas
- Consider managed security service providers
- Integrate continuous security testing approaches

### Challenge 2: Managing Business Disruption

**Problem**: Penetration testing potentially disrupting business operations.

**Solutions**:
- Conduct testing during maintenance windows
- Use isolated testing environments when possible
- Implement careful change control and rollback procedures
- Coordinate closely with operations teams
- Consider read-only or passive testing approaches

### Challenge 3: Keeping Up with Evolving Threats

**Problem**: Ensuring penetration tests reflect current threat landscape.

**Solutions**:
- Regularly update testing methodologies
- Incorporate threat intelligence into test planning
- Use red team exercises to simulate advanced threats
- Participate in industry threat sharing groups
- Continuously train testing teams on new techniques

### Challenge 4: Translating Technical Findings to Business Risk

**Problem**: Difficulty communicating technical findings to business stakeholders.

**Solutions**:
- Provide clear business impact assessments
- Use risk-based scoring and prioritization
- Create executive summaries with business context
- Quantify potential financial impact where possible
- Provide clear remediation roadmaps

## Resources and Further Reading

### AWS Documentation and Services
- [AWS Penetration Testing](https://aws.amazon.com/security/penetration-testing/)
- [AWS Security Hub User Guide](https://docs.aws.amazon.com/securityhub/latest/userguide/)
- [AWS Inspector User Guide](https://docs.aws.amazon.com/inspector/latest/userguide/)
- [AWS Well-Architected Security Pillar](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/)

### Industry Standards and Frameworks
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [NIST SP 800-115 - Technical Guide to Information Security Testing](https://csrc.nist.gov/publications/detail/sp/800-115/final)
- [PTES - Penetration Testing Execution Standard](http://www.pentest-standard.org/)
- [OSSTMM - Open Source Security Testing Methodology Manual](https://www.isecom.org/OSSTMM.3.pdf)

### Professional Organizations and Certifications
- [SANS GIAC Penetration Tester (GPEN)](https://www.giac.org/certification/penetration-tester-gpen)
- [Offensive Security Certified Professional (OSCP)](https://www.offensive-security.com/pwk-oscp/)
- [Certified Ethical Hacker (CEH)](https://www.eccouncil.org/programs/certified-ethical-hacker-ceh/)
- [CREST Penetration Testing Certifications](https://www.crest-approved.org/)

### Tools and Resources
- [Metasploit Framework](https://www.metasploit.com/) - Penetration testing framework
- [Burp Suite](https://portswigger.net/burp) - Web application security testing
- [Nmap](https://nmap.org/) - Network discovery and security auditing
- [OWASP ZAP](https://owasp.org/www-project-zap/) - Web application security scanner

---

*This documentation provides comprehensive guidance for implementing regular penetration testing programs. Regular updates ensure the content remains current with evolving threats and testing methodologies.*
