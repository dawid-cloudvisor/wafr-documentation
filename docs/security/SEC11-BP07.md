---
title: SEC11-BP07 - Regularly assess security properties of the pipelines
layout: default
parent: SEC11 - How do you incorporate and validate the security properties of applications?
grand_parent: Security
nav_order: 7
---

<div class="pillar-header">
  <h1>SEC11-BP07: Regularly assess security properties of the pipelines</h1>
  <p>Apply the same rigor to your deployment pipelines that you apply to your applications. Regularly assess the security properties of your build and deployment pipelines, including the security of the pipeline infrastructure, integrity of the pipeline stages, and access controls.</p>
</div>

## Implementation guidance

Pipeline security assessment is critical for maintaining the integrity of your entire software delivery process. By regularly evaluating your pipeline security properties, you ensure that your deployment infrastructure remains secure, compliant, and resistant to supply chain attacks.

### Key steps for implementing this best practice:

1. **Establish pipeline security assessment framework**:
   - Define security assessment criteria and standards
   - Create pipeline security baselines and benchmarks
   - Implement automated security scanning for pipeline infrastructure
   - Establish regular assessment schedules and procedures
   - Create security metrics and KPIs for pipeline evaluation

2. **Assess pipeline infrastructure security**:
   - Evaluate compute environment security configurations
   - Review network security and access controls
   - Assess storage and artifact security measures
   - Validate encryption and key management practices
   - Review logging and monitoring configurations

3. **Validate pipeline stage integrity**:
   - Assess source code management security
   - Review build environment isolation and security
   - Validate testing and scanning stage effectiveness
   - Evaluate deployment stage security controls
   - Assess approval and governance mechanisms

4. **Review access controls and permissions**:
   - Audit user and service account permissions
   - Validate role-based access control implementation
   - Review authentication and authorization mechanisms
   - Assess secrets management and rotation practices
   - Evaluate audit logging and monitoring coverage

5. **Implement continuous security monitoring**:
   - Set up real-time security monitoring for pipelines
   - Configure alerting for security violations
   - Implement anomaly detection for pipeline activities
   - Create security dashboards and reporting
   - Establish incident response procedures for pipeline security

6. **Conduct regular security reviews and audits**:
   - Perform periodic comprehensive security assessments
   - Conduct penetration testing of pipeline infrastructure
   - Review compliance with security standards and regulations
   - Assess third-party integrations and dependencies
   - Create remediation plans for identified security gaps

## Implementation examples

### Example 1: Automated pipeline security assessment framework

```python
import json
import boto3
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any
import subprocess
import os

class PipelineSecurityAssessor:
    def __init__(self):
        self.codepipeline = boto3.client('codepipeline')
        self.codebuild = boto3.client('codebuild')
        self.iam = boto3.client('iam')
        self.s3 = boto3.client('s3')
        self.cloudtrail = boto3.client('cloudtrail')
        self.config = boto3.client('config')
        self.dynamodb = boto3.resource('dynamodb')
        
        # Assessment results table
        self.assessment_table = self.dynamodb.Table('PipelineSecurityAssessments')
        
        # Security assessment criteria
        self.security_criteria = {
            'infrastructure': {
                'encryption_at_rest': {'weight': 10, 'critical': True},
                'encryption_in_transit': {'weight': 10, 'critical': True},
                'network_isolation': {'weight': 8, 'critical': False},
                'compute_security': {'weight': 9, 'critical': True},
                'logging_enabled': {'weight': 7, 'critical': False}
            },
            'access_control': {
                'least_privilege': {'weight': 10, 'critical': True},
                'mfa_enabled': {'weight': 8, 'critical': False},
                'role_separation': {'weight': 9, 'critical': True},
                'secrets_management': {'weight': 10, 'critical': True},
                'audit_logging': {'weight': 8, 'critical': False}
            },
            'pipeline_integrity': {
                'source_integrity': {'weight': 10, 'critical': True},
                'build_isolation': {'weight': 9, 'critical': True},
                'artifact_signing': {'weight': 8, 'critical': False},
                'approval_gates': {'weight': 7, 'critical': False},
                'rollback_capability': {'weight': 6, 'critical': False}
            },
            'monitoring': {
                'security_monitoring': {'weight': 9, 'critical': True},
                'anomaly_detection': {'weight': 7, 'critical': False},
                'incident_response': {'weight': 8, 'critical': False},
                'compliance_reporting': {'weight': 6, 'critical': False}
            }
        }
    
    def assess_pipeline_security(self, pipeline_name: str) -> Dict[str, Any]:
        """Perform comprehensive security assessment of a pipeline"""
        
        print(f"Starting security assessment for pipeline: {pipeline_name}")
        
        assessment_result = {
            'pipeline_name': pipeline_name,
            'assessment_timestamp': datetime.utcnow().isoformat(),
            'assessment_id': f"{pipeline_name}-{int(datetime.utcnow().timestamp())}",
            'overall_score': 0,
            'security_grade': 'F',
            'critical_issues': [],
            'recommendations': [],
            'category_scores': {},
            'detailed_findings': {}
        }
        
        try:
            # Get pipeline details
            pipeline_details = self.get_pipeline_details(pipeline_name)
            
            # Assess each security category
            assessment_result['category_scores']['infrastructure'] = self.assess_infrastructure_security(pipeline_details)
            assessment_result['category_scores']['access_control'] = self.assess_access_control(pipeline_details)
            assessment_result['category_scores']['pipeline_integrity'] = self.assess_pipeline_integrity(pipeline_details)
            assessment_result['category_scores']['monitoring'] = self.assess_monitoring_security(pipeline_details)
            
            # Calculate overall score
            assessment_result['overall_score'] = self.calculate_overall_score(assessment_result['category_scores'])
            assessment_result['security_grade'] = self.determine_security_grade(assessment_result['overall_score'])
            
            # Generate recommendations
            assessment_result['recommendations'] = self.generate_recommendations(assessment_result)
            
            # Store assessment results
            self.store_assessment_results(assessment_result)
            
            # Send alerts for critical issues
            if assessment_result['critical_issues']:
                self.send_security_alerts(assessment_result)
            
            print(f"Assessment completed. Overall score: {assessment_result['overall_score']}/100")
            return assessment_result
            
        except Exception as e:
            print(f"Error during pipeline security assessment: {str(e)}")
            assessment_result['error'] = str(e)
            return assessment_result
    
    def get_pipeline_details(self, pipeline_name: str) -> Dict[str, Any]:
        """Get comprehensive pipeline configuration details"""
        
        # Get pipeline configuration
        pipeline_response = self.codepipeline.get_pipeline(name=pipeline_name)
        pipeline_config = pipeline_response['pipeline']
        
        # Get pipeline execution history
        executions_response = self.codepipeline.list_pipeline_executions(
            pipelineName=pipeline_name,
            maxResults=10
        )
        
        # Get associated CodeBuild projects
        build_projects = []
        for stage in pipeline_config['stages']:
            for action in stage['actions']:
                if action['actionTypeId']['provider'] == 'CodeBuild':
                    project_name = action['configuration']['ProjectName']
                    project_details = self.codebuild.describe_projects(names=[project_name])
                    build_projects.extend(project_details['projects'])
        
        # Get artifact store details
        artifact_stores = pipeline_config.get('artifactStore', {})
        if isinstance(artifact_stores, dict):
            artifact_stores = [artifact_stores]
        
        return {
            'pipeline_config': pipeline_config,
            'executions': executions_response['pipelineExecutionSummaries'],
            'build_projects': build_projects,
            'artifact_stores': artifact_stores
        }
    
    def assess_infrastructure_security(self, pipeline_details: Dict[str, Any]) -> Dict[str, Any]:
        """Assess pipeline infrastructure security"""
        
        findings = {}
        score = 0
        max_score = 0
        
        # Check artifact store encryption
        for store in pipeline_details['artifact_stores']:
            criterion = 'encryption_at_rest'
            max_score += self.security_criteria['infrastructure'][criterion]['weight']
            
            if store.get('encryptionKey'):
                findings[f'artifact_store_encryption'] = {
                    'status': 'PASS',
                    'message': 'Artifact store is encrypted',
                    'score': self.security_criteria['infrastructure'][criterion]['weight']
                }
                score += self.security_criteria['infrastructure'][criterion]['weight']
            else:
                findings[f'artifact_store_encryption'] = {
                    'status': 'FAIL',
                    'message': 'Artifact store is not encrypted',
                    'score': 0,
                    'critical': self.security_criteria['infrastructure'][criterion]['critical']
                }
        
        # Check CodeBuild project security
        for project in pipeline_details['build_projects']:
            project_name = project['name']
            
            # Check VPC configuration
            criterion = 'network_isolation'
            max_score += self.security_criteria['infrastructure'][criterion]['weight']
            
            if project.get('vpcConfig'):
                findings[f'{project_name}_vpc_config'] = {
                    'status': 'PASS',
                    'message': f'CodeBuild project {project_name} uses VPC',
                    'score': self.security_criteria['infrastructure'][criterion]['weight']
                }
                score += self.security_criteria['infrastructure'][criterion]['weight']
            else:
                findings[f'{project_name}_vpc_config'] = {
                    'status': 'FAIL',
                    'message': f'CodeBuild project {project_name} not in VPC',
                    'score': 0
                }
            
            # Check compute environment security
            criterion = 'compute_security'
            max_score += self.security_criteria['infrastructure'][criterion]['weight']
            
            environment = project.get('environment', {})
            if environment.get('privilegedMode') == False:
                findings[f'{project_name}_privileged_mode'] = {
                    'status': 'PASS',
                    'message': f'CodeBuild project {project_name} runs without privileged mode',
                    'score': self.security_criteria['infrastructure'][criterion]['weight']
                }
                score += self.security_criteria['infrastructure'][criterion]['weight']
            else:
                findings[f'{project_name}_privileged_mode'] = {
                    'status': 'FAIL',
                    'message': f'CodeBuild project {project_name} uses privileged mode',
                    'score': 0,
                    'critical': self.security_criteria['infrastructure'][criterion]['critical']
                }
            
            # Check logging configuration
            criterion = 'logging_enabled'
            max_score += self.security_criteria['infrastructure'][criterion]['weight']
            
            logs_config = project.get('logsConfig', {})
            if logs_config.get('cloudWatchLogs', {}).get('status') == 'ENABLED':
                findings[f'{project_name}_logging'] = {
                    'status': 'PASS',
                    'message': f'CodeBuild project {project_name} has CloudWatch logging enabled',
                    'score': self.security_criteria['infrastructure'][criterion]['weight']
                }
                score += self.security_criteria['infrastructure'][criterion]['weight']
            else:
                findings[f'{project_name}_logging'] = {
                    'status': 'FAIL',
                    'message': f'CodeBuild project {project_name} logging not properly configured',
                    'score': 0
                }
        
        return {
            'score': score,
            'max_score': max_score,
            'percentage': (score / max_score * 100) if max_score > 0 else 0,
            'findings': findings
        }
    
    def assess_access_control(self, pipeline_details: Dict[str, Any]) -> Dict[str, Any]:
        """Assess pipeline access control security"""
        
        findings = {}
        score = 0
        max_score = 0
        
        pipeline_config = pipeline_details['pipeline_config']
        
        # Check service role configuration
        criterion = 'least_privilege'
        max_score += self.security_criteria['access_control'][criterion]['weight']
        
        service_role_arn = pipeline_config.get('roleArn')
        if service_role_arn:
            # Analyze role permissions
            role_name = service_role_arn.split('/')[-1]
            role_analysis = self.analyze_iam_role(role_name)
            
            if role_analysis['follows_least_privilege']:
                findings['service_role_permissions'] = {
                    'status': 'PASS',
                    'message': 'Pipeline service role follows least privilege principle',
                    'score': self.security_criteria['access_control'][criterion]['weight']
                }
                score += self.security_criteria['access_control'][criterion]['weight']
            else:
                findings['service_role_permissions'] = {
                    'status': 'FAIL',
                    'message': 'Pipeline service role has excessive permissions',
                    'score': 0,
                    'critical': self.security_criteria['access_control'][criterion]['critical'],
                    'details': role_analysis['excessive_permissions']
                }
        
        # Check secrets management
        criterion = 'secrets_management'
        max_score += self.security_criteria['access_control'][criterion]['weight']
        
        secrets_properly_managed = True
        for project in pipeline_details['build_projects']:
            environment_vars = project.get('environment', {}).get('environmentVariables', [])
            
            for env_var in environment_vars:
                if env_var.get('type') == 'PLAINTEXT' and self.is_sensitive_variable(env_var.get('name', '')):
                    secrets_properly_managed = False
                    break
        
        if secrets_properly_managed:
            findings['secrets_management'] = {
                'status': 'PASS',
                'message': 'Secrets are properly managed using Parameter Store or Secrets Manager',
                'score': self.security_criteria['access_control'][criterion]['weight']
            }
            score += self.security_criteria['access_control'][criterion]['weight']
        else:
            findings['secrets_management'] = {
                'status': 'FAIL',
                'message': 'Sensitive data found in plaintext environment variables',
                'score': 0,
                'critical': self.security_criteria['access_control'][criterion]['critical']
            }
        
        # Check audit logging
        criterion = 'audit_logging'
        max_score += self.security_criteria['access_control'][criterion]['weight']
        
        # Check if CloudTrail is logging pipeline API calls
        cloudtrail_events = self.check_cloudtrail_logging(pipeline_config['name'])
        
        if cloudtrail_events['logging_enabled']:
            findings['audit_logging'] = {
                'status': 'PASS',
                'message': 'Pipeline activities are logged in CloudTrail',
                'score': self.security_criteria['access_control'][criterion]['weight']
            }
            score += self.security_criteria['access_control'][criterion]['weight']
        else:
            findings['audit_logging'] = {
                'status': 'FAIL',
                'message': 'Pipeline activities not properly logged',
                'score': 0
            }
        
        return {
            'score': score,
            'max_score': max_score,
            'percentage': (score / max_score * 100) if max_score > 0 else 0,
            'findings': findings
        }
    
    def assess_pipeline_integrity(self, pipeline_details: Dict[str, Any]) -> Dict[str, Any]:
        """Assess pipeline integrity and stage security"""
        
        findings = {}
        score = 0
        max_score = 0
        
        pipeline_config = pipeline_details['pipeline_config']
        
        # Check source integrity
        criterion = 'source_integrity'
        max_score += self.security_criteria['pipeline_integrity'][criterion]['weight']
        
        source_stage = None
        for stage in pipeline_config['stages']:
            if stage['name'].lower() in ['source', 'src']:
                source_stage = stage
                break
        
        if source_stage:
            source_secured = True
            for action in source_stage['actions']:
                if action['actionTypeId']['provider'] == 'GitHub':
                    # Check if using OAuth token or webhook
                    if not action.get('configuration', {}).get('OAuthToken'):
                        source_secured = False
                elif action['actionTypeId']['provider'] == 'CodeCommit':
                    # CodeCommit is inherently secure
                    pass
            
            if source_secured:
                findings['source_integrity'] = {
                    'status': 'PASS',
                    'message': 'Source stage uses secure authentication',
                    'score': self.security_criteria['pipeline_integrity'][criterion]['weight']
                }
                score += self.security_criteria['pipeline_integrity'][criterion]['weight']
            else:
                findings['source_integrity'] = {
                    'status': 'FAIL',
                    'message': 'Source stage authentication may be insecure',
                    'score': 0,
                    'critical': self.security_criteria['pipeline_integrity'][criterion]['critical']
                }
        
        # Check build isolation
        criterion = 'build_isolation'
        max_score += self.security_criteria['pipeline_integrity'][criterion]['weight']
        
        build_isolated = True
        for project in pipeline_details['build_projects']:
            # Check if build runs in isolated environment
            if not project.get('vpcConfig') and project.get('environment', {}).get('privilegedMode'):
                build_isolated = False
                break
        
        if build_isolated:
            findings['build_isolation'] = {
                'status': 'PASS',
                'message': 'Build stages run in isolated environments',
                'score': self.security_criteria['pipeline_integrity'][criterion]['weight']
            }
            score += self.security_criteria['pipeline_integrity'][criterion]['weight']
        else:
            findings['build_isolation'] = {
                'status': 'FAIL',
                'message': 'Build stages may not be properly isolated',
                'score': 0,
                'critical': self.security_criteria['pipeline_integrity'][criterion]['critical']
            }
        
        # Check for approval gates
        criterion = 'approval_gates'
        max_score += self.security_criteria['pipeline_integrity'][criterion]['weight']
        
        has_approval_gates = False
        for stage in pipeline_config['stages']:
            for action in stage['actions']:
                if action['actionTypeId']['provider'] == 'Manual':
                    has_approval_gates = True
                    break
        
        if has_approval_gates:
            findings['approval_gates'] = {
                'status': 'PASS',
                'message': 'Pipeline includes manual approval gates',
                'score': self.security_criteria['pipeline_integrity'][criterion]['weight']
            }
            score += self.security_criteria['pipeline_integrity'][criterion]['weight']
        else:
            findings['approval_gates'] = {
                'status': 'FAIL',
                'message': 'Pipeline lacks manual approval gates for critical deployments',
                'score': 0
            }
        
        return {
            'score': score,
            'max_score': max_score,
            'percentage': (score / max_score * 100) if max_score > 0 else 0,
            'findings': findings
        }
    
    def assess_monitoring_security(self, pipeline_details: Dict[str, Any]) -> Dict[str, Any]:
        """Assess pipeline monitoring and alerting security"""
        
        findings = {}
        score = 0
        max_score = 0
        
        # Check security monitoring
        criterion = 'security_monitoring'
        max_score += self.security_criteria['monitoring'][criterion]['weight']
        
        # Check if pipeline has CloudWatch alarms
        pipeline_name = pipeline_details['pipeline_config']['name']
        monitoring_configured = self.check_pipeline_monitoring(pipeline_name)
        
        if monitoring_configured['has_security_alarms']:
            findings['security_monitoring'] = {
                'status': 'PASS',
                'message': 'Pipeline has security monitoring configured',
                'score': self.security_criteria['monitoring'][criterion]['weight']
            }
            score += self.security_criteria['monitoring'][criterion]['weight']
        else:
            findings['security_monitoring'] = {
                'status': 'FAIL',
                'message': 'Pipeline lacks comprehensive security monitoring',
                'score': 0,
                'critical': self.security_criteria['monitoring'][criterion]['critical']
            }
        
        # Check incident response capability
        criterion = 'incident_response'
        max_score += self.security_criteria['monitoring'][criterion]['weight']
        
        if monitoring_configured['has_incident_response']:
            findings['incident_response'] = {
                'status': 'PASS',
                'message': 'Pipeline has incident response procedures configured',
                'score': self.security_criteria['monitoring'][criterion]['weight']
            }
            score += self.security_criteria['monitoring'][criterion]['weight']
        else:
            findings['incident_response'] = {
                'status': 'FAIL',
                'message': 'Pipeline lacks automated incident response',
                'score': 0
            }
        
        return {
            'score': score,
            'max_score': max_score,
            'percentage': (score / max_score * 100) if max_score > 0 else 0,
            'findings': findings
        }
    
    def analyze_iam_role(self, role_name: str) -> Dict[str, Any]:
        """Analyze IAM role for least privilege compliance"""
        
        try:
            # Get role policies
            role_policies = self.iam.list_attached_role_policies(RoleName=role_name)
            inline_policies = self.iam.list_role_policies(RoleName=role_name)
            
            excessive_permissions = []
            
            # Check attached policies
            for policy in role_policies['AttachedPolicies']:
                policy_arn = policy['PolicyArn']
                if 'FullAccess' in policy_arn or 'PowerUser' in policy_arn:
                    excessive_permissions.append(f"Overly broad policy: {policy['PolicyName']}")
            
            # Check inline policies
            for policy_name in inline_policies['PolicyNames']:
                policy_doc = self.iam.get_role_policy(RoleName=role_name, PolicyName=policy_name)
                policy_document = policy_doc['PolicyDocument']
                
                # Check for wildcard permissions
                for statement in policy_document.get('Statement', []):
                    if isinstance(statement.get('Action'), str) and statement['Action'] == '*':
                        excessive_permissions.append(f"Wildcard action in policy: {policy_name}")
                    elif isinstance(statement.get('Resource'), str) and statement['Resource'] == '*':
                        excessive_permissions.append(f"Wildcard resource in policy: {policy_name}")
            
            return {
                'follows_least_privilege': len(excessive_permissions) == 0,
                'excessive_permissions': excessive_permissions
            }
            
        except Exception as e:
            return {
                'follows_least_privilege': False,
                'excessive_permissions': [f"Error analyzing role: {str(e)}"]
            }
    
    def is_sensitive_variable(self, var_name: str) -> bool:
        """Check if environment variable name suggests sensitive data"""
        
        sensitive_patterns = [
            'password', 'secret', 'key', 'token', 'credential',
            'api_key', 'private_key', 'access_key', 'auth'
        ]
        
        var_name_lower = var_name.lower()
        return any(pattern in var_name_lower for pattern in sensitive_patterns)
    
    def check_cloudtrail_logging(self, pipeline_name: str) -> Dict[str, Any]:
        """Check if CloudTrail is logging pipeline activities"""
        
        try:
            # Look for recent CodePipeline events
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(days=7)
            
            events = self.cloudtrail.lookup_events(
                LookupAttributes=[
                    {
                        'AttributeKey': 'EventSource',
                        'AttributeValue': 'codepipeline.amazonaws.com'
                    }
                ],
                StartTime=start_time,
                EndTime=end_time,
                MaxItems=10
            )
            
            return {
                'logging_enabled': len(events['Events']) > 0,
                'recent_events': len(events['Events'])
            }
            
        except Exception as e:
            return {
                'logging_enabled': False,
                'error': str(e)
            }
    
    def check_pipeline_monitoring(self, pipeline_name: str) -> Dict[str, Any]:
        """Check pipeline monitoring configuration"""
        
        try:
            cloudwatch = boto3.client('cloudwatch')
            
            # Check for pipeline-related alarms
            alarms = cloudwatch.describe_alarms(
                AlarmNamePrefix=pipeline_name,
                MaxRecords=50
            )
            
            security_alarms = []
            incident_response_configured = False
            
            for alarm in alarms['MetricAlarms']:
                alarm_name = alarm['AlarmName'].lower()
                if any(keyword in alarm_name for keyword in ['security', 'failed', 'error', 'unauthorized']):
                    security_alarms.append(alarm['AlarmName'])
                
                # Check if alarm has actions (SNS topics, etc.)
                if alarm.get('AlarmActions') or alarm.get('OKActions'):
                    incident_response_configured = True
            
            return {
                'has_security_alarms': len(security_alarms) > 0,
                'security_alarms': security_alarms,
                'has_incident_response': incident_response_configured
            }
            
        except Exception as e:
            return {
                'has_security_alarms': False,
                'has_incident_response': False,
                'error': str(e)
            }
    
    def calculate_overall_score(self, category_scores: Dict[str, Dict[str, Any]]) -> float:
        """Calculate weighted overall security score"""
        
        total_score = 0
        total_weight = 0
        
        category_weights = {
            'infrastructure': 0.25,
            'access_control': 0.30,
            'pipeline_integrity': 0.30,
            'monitoring': 0.15
        }
        
        for category, weight in category_weights.items():
            if category in category_scores:
                category_percentage = category_scores[category]['percentage']
                total_score += category_percentage * weight
                total_weight += weight
        
        return total_score / total_weight if total_weight > 0 else 0
    
    def determine_security_grade(self, score: float) -> str:
        """Determine security grade based on score"""
        
        if score >= 90:
            return 'A'
        elif score >= 80:
            return 'B'
        elif score >= 70:
            return 'C'
        elif score >= 60:
            return 'D'
        else:
            return 'F'
    
    def generate_recommendations(self, assessment_result: Dict[str, Any]) -> List[str]:
        """Generate security improvement recommendations"""
        
        recommendations = []
        
        for category, results in assessment_result['category_scores'].items():
            for finding_name, finding in results['findings'].items():
                if finding['status'] == 'FAIL':
                    if finding.get('critical'):
                        recommendations.append(f"CRITICAL: {finding['message']} - Immediate action required")
                    else:
                        recommendations.append(f"MEDIUM: {finding['message']} - Should be addressed")
        
        # Add general recommendations based on overall score
        overall_score = assessment_result['overall_score']
        if overall_score < 70:
            recommendations.append("Overall security score is below acceptable threshold. Comprehensive security review recommended.")
        
        return recommendations
    
    def store_assessment_results(self, assessment_result: Dict[str, Any]):
        """Store assessment results in DynamoDB"""
        
        try:
            self.assessment_table.put_item(Item=assessment_result)
            print(f"Assessment results stored for pipeline: {assessment_result['pipeline_name']}")
        except Exception as e:
            print(f"Error storing assessment results: {str(e)}")
    
    def send_security_alerts(self, assessment_result: Dict[str, Any]):
        """Send security alerts for critical issues"""
        
        try:
            sns = boto3.client('sns')
            
            critical_issues = [rec for rec in assessment_result['recommendations'] if rec.startswith('CRITICAL')]
            
            if critical_issues:
                message = {
                    'pipeline_name': assessment_result['pipeline_name'],
                    'security_grade': assessment_result['security_grade'],
                    'overall_score': assessment_result['overall_score'],
                    'critical_issues': critical_issues,
                    'assessment_timestamp': assessment_result['assessment_timestamp']
                }
                
                sns.publish(
                    TopicArn='arn:aws:sns:us-west-2:123456789012:PipelineSecurityAlerts',
                    Subject=f"Critical Pipeline Security Issues: {assessment_result['pipeline_name']}",
                    Message=json.dumps(message, indent=2)
                )
                
        except Exception as e:
            print(f"Error sending security alerts: {str(e)}")

def lambda_handler(event, context):
    """Lambda function to perform pipeline security assessment"""
    
    assessor = PipelineSecurityAssessor()
    
    # Get pipeline name from event
    pipeline_name = event.get('pipeline_name')
    
    if not pipeline_name:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Pipeline name is required'})
        }
    
    # Perform security assessment
    assessment_result = assessor.assess_pipeline_security(pipeline_name)
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'assessment_id': assessment_result['assessment_id'],
            'pipeline_name': assessment_result['pipeline_name'],
            'overall_score': assessment_result['overall_score'],
            'security_grade': assessment_result['security_grade'],
            'critical_issues_count': len([r for r in assessment_result['recommendations'] if r.startswith('CRITICAL')])
        })
    }
```
### Example 2: Pipeline security monitoring and alerting system

```python
import json
import boto3
from datetime import datetime, timedelta
import re
from typing import Dict, List, Any

class PipelineSecurityMonitor:
    def __init__(self):
        self.cloudwatch = boto3.client('cloudwatch')
        self.logs = boto3.client('logs')
        self.sns = boto3.client('sns')
        self.codepipeline = boto3.client('codepipeline')
        self.dynamodb = boto3.resource('dynamodb')
        
        # Security monitoring table
        self.monitoring_table = self.dynamodb.Table('PipelineSecurityMonitoring')
        
        # Security patterns to monitor
        self.security_patterns = {
            'unauthorized_access': [
                r'AccessDenied',
                r'UnauthorizedOperation',
                r'InvalidUserID\.NotFound',
                r'TokenRefreshRequired'
            ],
            'suspicious_activity': [
                r'unusual.*login.*pattern',
                r'multiple.*failed.*attempts',
                r'privilege.*escalation',
                r'suspicious.*api.*calls'
            ],
            'security_violations': [
                r'security.*scan.*failed',
                r'vulnerability.*detected',
                r'compliance.*violation',
                r'policy.*violation'
            ],
            'configuration_changes': [
                r'iam.*role.*modified',
                r'security.*group.*changed',
                r'encryption.*disabled',
                r'logging.*disabled'
            ]
        }
    
    def monitor_pipeline_security(self, pipeline_name: str, time_range_hours: int = 24) -> Dict[str, Any]:
        """Monitor pipeline security events and anomalies"""
        
        print(f"Starting security monitoring for pipeline: {pipeline_name}")
        
        monitoring_result = {
            'pipeline_name': pipeline_name,
            'monitoring_timestamp': datetime.utcnow().isoformat(),
            'time_range_hours': time_range_hours,
            'security_events': [],
            'anomalies_detected': [],
            'risk_score': 0,
            'recommendations': []
        }
        
        try:
            # Monitor CloudWatch Logs for security events
            log_events = self.analyze_pipeline_logs(pipeline_name, time_range_hours)
            monitoring_result['security_events'].extend(log_events)
            
            # Monitor CloudTrail for API activities
            api_events = self.analyze_api_activities(pipeline_name, time_range_hours)
            monitoring_result['security_events'].extend(api_events)
            
            # Detect anomalies in pipeline behavior
            anomalies = self.detect_pipeline_anomalies(pipeline_name, time_range_hours)
            monitoring_result['anomalies_detected'].extend(anomalies)
            
            # Calculate risk score
            monitoring_result['risk_score'] = self.calculate_risk_score(monitoring_result)
            
            # Generate recommendations
            monitoring_result['recommendations'] = self.generate_security_recommendations(monitoring_result)
            
            # Store monitoring results
            self.store_monitoring_results(monitoring_result)
            
            # Send alerts if high risk detected
            if monitoring_result['risk_score'] > 70:
                self.send_security_alerts(monitoring_result)
            
            return monitoring_result
            
        except Exception as e:
            print(f"Error during pipeline security monitoring: {str(e)}")
            monitoring_result['error'] = str(e)
            return monitoring_result
    
    def analyze_pipeline_logs(self, pipeline_name: str, time_range_hours: int) -> List[Dict[str, Any]]:
        """Analyze CloudWatch Logs for security events"""
        
        security_events = []
        
        try:
            # Get log groups related to the pipeline
            log_groups = self.get_pipeline_log_groups(pipeline_name)
            
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(hours=time_range_hours)
            
            for log_group in log_groups:
                try:
                    # Search for security-related log entries
                    for pattern_category, patterns in self.security_patterns.items():
                        for pattern in patterns:
                            events = self.logs.filter_log_events(
                                logGroupName=log_group,
                                startTime=int(start_time.timestamp() * 1000),
                                endTime=int(end_time.timestamp() * 1000),
                                filterPattern=pattern,
                                limit=100
                            )
                            
                            for event in events.get('events', []):
                                security_events.append({
                                    'event_type': 'log_security_event',
                                    'category': pattern_category,
                                    'pattern': pattern,
                                    'log_group': log_group,
                                    'timestamp': datetime.fromtimestamp(event['timestamp'] / 1000).isoformat(),
                                    'message': event['message'][:500],  # Truncate long messages
                                    'severity': self.determine_event_severity(pattern_category)
                                })
                
                except Exception as e:
                    print(f"Error analyzing log group {log_group}: {str(e)}")
                    continue
        
        except Exception as e:
            print(f"Error analyzing pipeline logs: {str(e)}")
        
        return security_events
    
    def analyze_api_activities(self, pipeline_name: str, time_range_hours: int) -> List[Dict[str, Any]]:
        """Analyze CloudTrail API activities for security events"""
        
        security_events = []
        
        try:
            cloudtrail = boto3.client('cloudtrail')
            
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(hours=time_range_hours)
            
            # Look for CodePipeline API events
            events = cloudtrail.lookup_events(
                LookupAttributes=[
                    {
                        'AttributeKey': 'EventSource',
                        'AttributeValue': 'codepipeline.amazonaws.com'
                    }
                ],
                StartTime=start_time,
                EndTime=end_time,
                MaxItems=100
            )
            
            for event in events.get('Events', []):
                event_name = event.get('EventName', '')
                username = event.get('Username', 'Unknown')
                source_ip = event.get('SourceIPAddress', 'Unknown')
                
                # Check for suspicious API activities
                if self.is_suspicious_api_activity(event_name, username, source_ip):
                    security_events.append({
                        'event_type': 'api_security_event',
                        'category': 'suspicious_api_activity',
                        'event_name': event_name,
                        'username': username,
                        'source_ip': source_ip,
                        'timestamp': event['EventTime'].isoformat(),
                        'severity': 'HIGH' if 'Delete' in event_name or 'Stop' in event_name else 'MEDIUM'
                    })
                
                # Check for failed API calls
                if event.get('ErrorCode') or event.get('ErrorMessage'):
                    security_events.append({
                        'event_type': 'api_error_event',
                        'category': 'api_failures',
                        'event_name': event_name,
                        'username': username,
                        'error_code': event.get('ErrorCode', 'Unknown'),
                        'error_message': event.get('ErrorMessage', 'Unknown'),
                        'timestamp': event['EventTime'].isoformat(),
                        'severity': 'MEDIUM'
                    })
        
        except Exception as e:
            print(f"Error analyzing API activities: {str(e)}")
        
        return security_events
    
    def detect_pipeline_anomalies(self, pipeline_name: str, time_range_hours: int) -> List[Dict[str, Any]]:
        """Detect anomalies in pipeline behavior"""
        
        anomalies = []
        
        try:
            # Get pipeline execution history
            executions = self.codepipeline.list_pipeline_executions(
                pipelineName=pipeline_name,
                maxResults=50
            )
            
            recent_executions = []
            cutoff_time = datetime.utcnow() - timedelta(hours=time_range_hours)
            
            for execution in executions.get('pipelineExecutionSummaries', []):
                start_time = execution.get('startTime')
                if start_time and start_time > cutoff_time:
                    recent_executions.append(execution)
            
            # Analyze execution patterns
            if len(recent_executions) > 0:
                # Check for unusual execution frequency
                execution_frequency = len(recent_executions) / time_range_hours
                historical_frequency = self.get_historical_execution_frequency(pipeline_name)
                
                if execution_frequency > historical_frequency * 2:
                    anomalies.append({
                        'anomaly_type': 'unusual_execution_frequency',
                        'description': f'Pipeline execution frequency ({execution_frequency:.2f}/hour) is unusually high',
                        'severity': 'MEDIUM',
                        'current_frequency': execution_frequency,
                        'historical_frequency': historical_frequency
                    })
                
                # Check for unusual failure patterns
                failed_executions = [e for e in recent_executions if e.get('status') == 'Failed']
                failure_rate = len(failed_executions) / len(recent_executions)
                
                if failure_rate > 0.3:  # More than 30% failure rate
                    anomalies.append({
                        'anomaly_type': 'high_failure_rate',
                        'description': f'Pipeline failure rate ({failure_rate:.1%}) is unusually high',
                        'severity': 'HIGH',
                        'failure_rate': failure_rate,
                        'failed_executions': len(failed_executions),
                        'total_executions': len(recent_executions)
                    })
                
                # Check for executions outside normal hours
                off_hours_executions = self.detect_off_hours_executions(recent_executions)
                if off_hours_executions:
                    anomalies.append({
                        'anomaly_type': 'off_hours_execution',
                        'description': f'{len(off_hours_executions)} pipeline executions occurred outside normal business hours',
                        'severity': 'MEDIUM',
                        'off_hours_count': len(off_hours_executions),
                        'executions': off_hours_executions
                    })
        
        except Exception as e:
            print(f"Error detecting pipeline anomalies: {str(e)}")
        
        return anomalies
    
    def get_pipeline_log_groups(self, pipeline_name: str) -> List[str]:
        """Get CloudWatch log groups associated with the pipeline"""
        
        log_groups = []
        
        try:
            # Get pipeline configuration
            pipeline = self.codepipeline.get_pipeline(name=pipeline_name)
            
            # Find CodeBuild projects in the pipeline
            for stage in pipeline['pipeline']['stages']:
                for action in stage['actions']:
                    if action['actionTypeId']['provider'] == 'CodeBuild':
                        project_name = action['configuration']['ProjectName']
                        log_groups.append(f'/aws/codebuild/{project_name}')
            
            # Add pipeline-specific log groups
            log_groups.append(f'/aws/codepipeline/{pipeline_name}')
            
            # Filter to only existing log groups
            existing_log_groups = []
            for log_group in log_groups:
                try:
                    self.logs.describe_log_groups(logGroupNamePrefix=log_group, limit=1)
                    existing_log_groups.append(log_group)
                except:
                    continue
            
            return existing_log_groups
        
        except Exception as e:
            print(f"Error getting pipeline log groups: {str(e)}")
            return []
    
    def is_suspicious_api_activity(self, event_name: str, username: str, source_ip: str) -> bool:
        """Determine if API activity is suspicious"""
        
        # Check for suspicious event names
        suspicious_events = [
            'DeletePipeline', 'StopPipelineExecution', 'DisableStageTransition',
            'PutJobFailureResult', 'RetryStageExecution'
        ]
        
        if event_name in suspicious_events:
            return True
        
        # Check for unusual source IPs (basic check)
        if source_ip and not source_ip.startswith(('10.', '172.', '192.168.')):
            # External IP - could be suspicious depending on context
            return True
        
        # Check for service account activities outside normal hours
        if username and username.startswith('codebuild-') or username.startswith('codepipeline-'):
            current_hour = datetime.utcnow().hour
            if current_hour < 6 or current_hour > 22:  # Outside 6 AM - 10 PM UTC
                return True
        
        return False
    
    def get_historical_execution_frequency(self, pipeline_name: str) -> float:
        """Get historical execution frequency for comparison"""
        
        try:
            # Get executions from the past 30 days
            executions = self.codepipeline.list_pipeline_executions(
                pipelineName=pipeline_name,
                maxResults=100
            )
            
            cutoff_time = datetime.utcnow() - timedelta(days=30)
            historical_executions = []
            
            for execution in executions.get('pipelineExecutionSummaries', []):
                start_time = execution.get('startTime')
                if start_time and start_time > cutoff_time:
                    historical_executions.append(execution)
            
            # Calculate average executions per hour over 30 days
            if len(historical_executions) > 0:
                return len(historical_executions) / (30 * 24)  # executions per hour
            else:
                return 0.1  # Default low frequency
        
        except Exception as e:
            print(f"Error getting historical execution frequency: {str(e)}")
            return 0.1
    
    def detect_off_hours_executions(self, executions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detect executions that occurred outside normal business hours"""
        
        off_hours_executions = []
        
        for execution in executions:
            start_time = execution.get('startTime')
            if start_time:
                # Check if execution started outside 6 AM - 10 PM UTC
                hour = start_time.hour
                if hour < 6 or hour > 22:
                    off_hours_executions.append({
                        'execution_id': execution.get('pipelineExecutionId'),
                        'start_time': start_time.isoformat(),
                        'status': execution.get('status'),
                        'trigger': execution.get('trigger', {}).get('triggerType', 'Unknown')
                    })
        
        return off_hours_executions
    
    def determine_event_severity(self, pattern_category: str) -> str:
        """Determine severity based on pattern category"""
        
        severity_map = {
            'unauthorized_access': 'HIGH',
            'suspicious_activity': 'HIGH',
            'security_violations': 'CRITICAL',
            'configuration_changes': 'MEDIUM'
        }
        
        return severity_map.get(pattern_category, 'LOW')
    
    def calculate_risk_score(self, monitoring_result: Dict[str, Any]) -> int:
        """Calculate overall risk score based on security events and anomalies"""
        
        risk_score = 0
        
        # Score based on security events
        for event in monitoring_result['security_events']:
            severity = event.get('severity', 'LOW')
            if severity == 'CRITICAL':
                risk_score += 25
            elif severity == 'HIGH':
                risk_score += 15
            elif severity == 'MEDIUM':
                risk_score += 10
            else:
                risk_score += 5
        
        # Score based on anomalies
        for anomaly in monitoring_result['anomalies_detected']:
            severity = anomaly.get('severity', 'LOW')
            if severity == 'CRITICAL':
                risk_score += 20
            elif severity == 'HIGH':
                risk_score += 15
            elif severity == 'MEDIUM':
                risk_score += 10
            else:
                risk_score += 5
        
        # Cap the risk score at 100
        return min(risk_score, 100)
    
    def generate_security_recommendations(self, monitoring_result: Dict[str, Any]) -> List[str]:
        """Generate security recommendations based on monitoring results"""
        
        recommendations = []
        
        # Recommendations based on security events
        event_categories = set()
        for event in monitoring_result['security_events']:
            event_categories.add(event.get('category', 'unknown'))
        
        if 'unauthorized_access' in event_categories:
            recommendations.append("Review and strengthen access controls for pipeline resources")
            recommendations.append("Enable MFA for all pipeline administrators")
        
        if 'suspicious_activity' in event_categories:
            recommendations.append("Investigate suspicious activities and consider implementing additional monitoring")
            recommendations.append("Review user access patterns and implement anomaly detection")
        
        if 'security_violations' in event_categories:
            recommendations.append("URGENT: Address security violations immediately")
            recommendations.append("Review and update security policies and compliance checks")
        
        # Recommendations based on anomalies
        anomaly_types = set()
        for anomaly in monitoring_result['anomalies_detected']:
            anomaly_types.add(anomaly.get('anomaly_type', 'unknown'))
        
        if 'unusual_execution_frequency' in anomaly_types:
            recommendations.append("Investigate cause of unusual pipeline execution frequency")
            recommendations.append("Consider implementing execution rate limiting")
        
        if 'high_failure_rate' in anomaly_types:
            recommendations.append("Investigate and address causes of pipeline failures")
            recommendations.append("Review pipeline configuration and dependencies")
        
        if 'off_hours_execution' in anomaly_types:
            recommendations.append("Review off-hours pipeline executions for legitimacy")
            recommendations.append("Consider implementing time-based access controls")
        
        # General recommendations based on risk score
        risk_score = monitoring_result['risk_score']
        if risk_score > 70:
            recommendations.append("HIGH RISK: Immediate security review and remediation required")
        elif risk_score > 40:
            recommendations.append("MEDIUM RISK: Schedule security review within 24 hours")
        
        return recommendations
    
    def store_monitoring_results(self, monitoring_result: Dict[str, Any]):
        """Store monitoring results in DynamoDB"""
        
        try:
            # Prepare item for DynamoDB (handle datetime serialization)
            item = monitoring_result.copy()
            
            # Convert datetime objects to ISO strings
            for event in item.get('security_events', []):
                if 'timestamp' in event and isinstance(event['timestamp'], datetime):
                    event['timestamp'] = event['timestamp'].isoformat()
            
            self.monitoring_table.put_item(Item=item)
            print(f"Monitoring results stored for pipeline: {monitoring_result['pipeline_name']}")
        
        except Exception as e:
            print(f"Error storing monitoring results: {str(e)}")
    
    def send_security_alerts(self, monitoring_result: Dict[str, Any]):
        """Send security alerts for high-risk situations"""
        
        try:
            message = {
                'alert_type': 'PIPELINE_SECURITY_RISK',
                'pipeline_name': monitoring_result['pipeline_name'],
                'risk_score': monitoring_result['risk_score'],
                'security_events_count': len(monitoring_result['security_events']),
                'anomalies_count': len(monitoring_result['anomalies_detected']),
                'recommendations': monitoring_result['recommendations'][:5],  # Top 5 recommendations
                'monitoring_timestamp': monitoring_result['monitoring_timestamp']
            }
            
            self.sns.publish(
                TopicArn='arn:aws:sns:us-west-2:123456789012:PipelineSecurityAlerts',
                Subject=f"High Risk Security Alert: {monitoring_result['pipeline_name']}",
                Message=json.dumps(message, indent=2)
            )
            
            print(f"Security alert sent for pipeline: {monitoring_result['pipeline_name']}")
        
        except Exception as e:
            print(f"Error sending security alerts: {str(e)}")

def lambda_handler(event, context):
    """Lambda function for pipeline security monitoring"""
    
    monitor = PipelineSecurityMonitor()
    
    # Get parameters from event
    pipeline_name = event.get('pipeline_name')
    time_range_hours = event.get('time_range_hours', 24)
    
    if not pipeline_name:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Pipeline name is required'})
        }
    
    # Perform security monitoring
    monitoring_result = monitor.monitor_pipeline_security(pipeline_name, time_range_hours)
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'pipeline_name': monitoring_result['pipeline_name'],
            'risk_score': monitoring_result['risk_score'],
            'security_events_count': len(monitoring_result['security_events']),
            'anomalies_count': len(monitoring_result['anomalies_detected']),
            'monitoring_timestamp': monitoring_result['monitoring_timestamp']
        })
    }
```
### Example 3: Terraform configuration for pipeline security assessment infrastructure

```hcl
# terraform/pipeline-security-assessment.tf
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# Variables
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-west-2"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "production"
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "pipeline-security"
}

# DynamoDB table for storing assessment results
resource "aws_dynamodb_table" "pipeline_security_assessments" {
  name           = "PipelineSecurityAssessments"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "assessment_id"
  range_key      = "pipeline_name"
  
  attribute {
    name = "assessment_id"
    type = "S"
  }
  
  attribute {
    name = "pipeline_name"
    type = "S"
  }
  
  attribute {
    name = "assessment_timestamp"
    type = "S"
  }
  
  global_secondary_index {
    name     = "PipelineNameIndex"
    hash_key = "pipeline_name"
    range_key = "assessment_timestamp"
  }
  
  point_in_time_recovery {
    enabled = true
  }
  
  server_side_encryption {
    enabled = true
  }
  
  tags = {
    Environment = var.environment
    Project     = var.project_name
    Purpose     = "Pipeline Security Assessment Storage"
  }
}

# DynamoDB table for monitoring results
resource "aws_dynamodb_table" "pipeline_security_monitoring" {
  name           = "PipelineSecurityMonitoring"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "pipeline_name"
  range_key      = "monitoring_timestamp"
  
  attribute {
    name = "pipeline_name"
    type = "S"
  }
  
  attribute {
    name = "monitoring_timestamp"
    type = "S"
  }
  
  ttl {
    attribute_name = "ttl"
    enabled        = true
  }
  
  point_in_time_recovery {
    enabled = true
  }
  
  server_side_encryption {
    enabled = true
  }
  
  tags = {
    Environment = var.environment
    Project     = var.project_name
    Purpose     = "Pipeline Security Monitoring Storage"
  }
}

# SNS topic for security alerts
resource "aws_sns_topic" "pipeline_security_alerts" {
  name              = "PipelineSecurityAlerts"
  kms_master_key_id = aws_kms_key.pipeline_security.arn
  
  tags = {
    Environment = var.environment
    Project     = var.project_name
    Purpose     = "Pipeline Security Alerts"
  }
}

# KMS key for encryption
resource "aws_kms_key" "pipeline_security" {
  description             = "KMS key for pipeline security assessment encryption"
  deletion_window_in_days = 7
  enable_key_rotation     = true
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "Enable IAM User Permissions"
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"
        }
        Action   = "kms:*"
        Resource = "*"
      },
      {
        Sid    = "Allow Lambda Functions"
        Effect = "Allow"
        Principal = {
          AWS = [
            aws_iam_role.pipeline_assessor_role.arn,
            aws_iam_role.pipeline_monitor_role.arn
          ]
        }
        Action = [
          "kms:Decrypt",
          "kms:DescribeKey",
          "kms:Encrypt",
          "kms:GenerateDataKey*",
          "kms:ReEncrypt*"
        ]
        Resource = "*"
      }
    ]
  })
  
  tags = {
    Environment = var.environment
    Project     = var.project_name
    Purpose     = "Pipeline Security Encryption"
  }
}

resource "aws_kms_alias" "pipeline_security" {
  name          = "alias/${var.project_name}-${var.environment}"
  target_key_id = aws_kms_key.pipeline_security.key_id
}

# IAM role for pipeline security assessor Lambda
resource "aws_iam_role" "pipeline_assessor_role" {
  name = "PipelineSecurityAssessorRole"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
  
  tags = {
    Environment = var.environment
    Project     = var.project_name
  }
}

# IAM policy for pipeline security assessor
resource "aws_iam_role_policy" "pipeline_assessor_policy" {
  name = "PipelineSecurityAssessorPolicy"
  role = aws_iam_role.pipeline_assessor_role.id
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "codepipeline:GetPipeline",
          "codepipeline:ListPipelines",
          "codepipeline:ListPipelineExecutions",
          "codepipeline:GetPipelineExecution",
          "codepipeline:GetPipelineState"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "codebuild:DescribeProjects",
          "codebuild:ListProjects",
          "codebuild:BatchGetProjects"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "iam:GetRole",
          "iam:GetRolePolicy",
          "iam:ListAttachedRolePolicies",
          "iam:ListRolePolicies",
          "iam:GetPolicy",
          "iam:GetPolicyVersion"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "s3:GetBucketEncryption",
          "s3:GetBucketPolicy",
          "s3:GetBucketVersioning",
          "s3:GetBucketLogging"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "cloudtrail:LookupEvents",
          "cloudtrail:DescribeTrails"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "cloudwatch:DescribeAlarms",
          "cloudwatch:GetMetricStatistics"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "dynamodb:PutItem",
          "dynamodb:GetItem",
          "dynamodb:Query",
          "dynamodb:Scan"
        ]
        Resource = [
          aws_dynamodb_table.pipeline_security_assessments.arn,
          "${aws_dynamodb_table.pipeline_security_assessments.arn}/index/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "sns:Publish"
        ]
        Resource = aws_sns_topic.pipeline_security_alerts.arn
      },
      {
        Effect = "Allow"
        Action = [
          "kms:Decrypt",
          "kms:DescribeKey",
          "kms:Encrypt",
          "kms:GenerateDataKey*"
        ]
        Resource = aws_kms_key.pipeline_security.arn
      }
    ]
  })
}

# Attach basic Lambda execution role
resource "aws_iam_role_policy_attachment" "pipeline_assessor_basic" {
  role       = aws_iam_role.pipeline_assessor_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# IAM role for pipeline security monitor Lambda
resource "aws_iam_role" "pipeline_monitor_role" {
  name = "PipelineSecurityMonitorRole"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
  
  tags = {
    Environment = var.environment
    Project     = var.project_name
  }
}

# IAM policy for pipeline security monitor
resource "aws_iam_role_policy" "pipeline_monitor_policy" {
  name = "PipelineSecurityMonitorPolicy"
  role = aws_iam_role.pipeline_monitor_role.id
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "logs:DescribeLogGroups",
          "logs:DescribeLogStreams",
          "logs:FilterLogEvents",
          "logs:GetLogEvents"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "codepipeline:GetPipeline",
          "codepipeline:ListPipelineExecutions",
          "codepipeline:GetPipelineExecution"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "cloudtrail:LookupEvents"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "cloudwatch:DescribeAlarms",
          "cloudwatch:GetMetricStatistics"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "dynamodb:PutItem",
          "dynamodb:GetItem",
          "dynamodb:Query"
        ]
        Resource = aws_dynamodb_table.pipeline_security_monitoring.arn
      },
      {
        Effect = "Allow"
        Action = [
          "sns:Publish"
        ]
        Resource = aws_sns_topic.pipeline_security_alerts.arn
      },
      {
        Effect = "Allow"
        Action = [
          "kms:Decrypt",
          "kms:DescribeKey",
          "kms:Encrypt",
          "kms:GenerateDataKey*"
        ]
        Resource = aws_kms_key.pipeline_security.arn
      }
    ]
  })
}

# Attach basic Lambda execution role
resource "aws_iam_role_policy_attachment" "pipeline_monitor_basic" {
  role       = aws_iam_role.pipeline_monitor_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Lambda function for pipeline security assessment
resource "aws_lambda_function" "pipeline_security_assessor" {
  filename         = "pipeline_security_assessor.zip"
  function_name    = "pipeline-security-assessor"
  role            = aws_iam_role.pipeline_assessor_role.arn
  handler         = "lambda_function.lambda_handler"
  runtime         = "python3.9"
  timeout         = 300
  memory_size     = 512
  
  environment {
    variables = {
      ASSESSMENT_TABLE_NAME = aws_dynamodb_table.pipeline_security_assessments.name
      ALERT_TOPIC_ARN      = aws_sns_topic.pipeline_security_alerts.arn
      KMS_KEY_ID           = aws_kms_key.pipeline_security.arn
    }
  }
  
  tags = {
    Environment = var.environment
    Project     = var.project_name
    Purpose     = "Pipeline Security Assessment"
  }
}

# Lambda function for pipeline security monitoring
resource "aws_lambda_function" "pipeline_security_monitor" {
  filename         = "pipeline_security_monitor.zip"
  function_name    = "pipeline-security-monitor"
  role            = aws_iam_role.pipeline_monitor_role.arn
  handler         = "lambda_function.lambda_handler"
  runtime         = "python3.9"
  timeout         = 300
  memory_size     = 512
  
  environment {
    variables = {
      MONITORING_TABLE_NAME = aws_dynamodb_table.pipeline_security_monitoring.name
      ALERT_TOPIC_ARN      = aws_sns_topic.pipeline_security_alerts.arn
      KMS_KEY_ID           = aws_kms_key.pipeline_security.arn
    }
  }
  
  tags = {
    Environment = var.environment
    Project     = var.project_name
    Purpose     = "Pipeline Security Monitoring"
  }
}

# EventBridge rule for scheduled assessments
resource "aws_cloudwatch_event_rule" "pipeline_assessment_schedule" {
  name                = "pipeline-security-assessment-schedule"
  description         = "Trigger pipeline security assessments"
  schedule_expression = "rate(24 hours)"  # Daily assessments
  
  tags = {
    Environment = var.environment
    Project     = var.project_name
  }
}

# EventBridge target for assessment Lambda
resource "aws_cloudwatch_event_target" "pipeline_assessment_target" {
  rule      = aws_cloudwatch_event_rule.pipeline_assessment_schedule.name
  target_id = "PipelineAssessmentTarget"
  arn       = aws_lambda_function.pipeline_security_assessor.arn
  
  input = jsonencode({
    pipeline_name = "all"  # Assess all pipelines
  })
}

# Permission for EventBridge to invoke assessment Lambda
resource "aws_lambda_permission" "allow_eventbridge_assessment" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.pipeline_security_assessor.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.pipeline_assessment_schedule.arn
}

# EventBridge rule for continuous monitoring
resource "aws_cloudwatch_event_rule" "pipeline_monitoring_schedule" {
  name                = "pipeline-security-monitoring-schedule"
  description         = "Trigger pipeline security monitoring"
  schedule_expression = "rate(1 hour)"  # Hourly monitoring
  
  tags = {
    Environment = var.environment
    Project     = var.project_name
  }
}

# EventBridge target for monitoring Lambda
resource "aws_cloudwatch_event_target" "pipeline_monitoring_target" {
  rule      = aws_cloudwatch_event_rule.pipeline_monitoring_schedule.name
  target_id = "PipelineMonitoringTarget"
  arn       = aws_lambda_function.pipeline_security_monitor.arn
  
  input = jsonencode({
    pipeline_name = "all"  # Monitor all pipelines
    time_range_hours = 1
  })
}

# Permission for EventBridge to invoke monitoring Lambda
resource "aws_lambda_permission" "allow_eventbridge_monitoring" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.pipeline_security_monitor.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.pipeline_monitoring_schedule.arn
}

# CloudWatch dashboard for pipeline security metrics
resource "aws_cloudwatch_dashboard" "pipeline_security_dashboard" {
  dashboard_name = "PipelineSecurityDashboard"
  
  dashboard_body = jsonencode({
    widgets = [
      {
        type   = "metric"
        x      = 0
        y      = 0
        width  = 12
        height = 6
        
        properties = {
          metrics = [
            ["AWS/Lambda", "Duration", "FunctionName", aws_lambda_function.pipeline_security_assessor.function_name],
            [".", "Errors", ".", "."],
            [".", "Invocations", ".", "."]
          ]
          view    = "timeSeries"
          stacked = false
          region  = var.aws_region
          title   = "Pipeline Security Assessor Metrics"
          period  = 300
        }
      },
      {
        type   = "metric"
        x      = 0
        y      = 6
        width  = 12
        height = 6
        
        properties = {
          metrics = [
            ["AWS/Lambda", "Duration", "FunctionName", aws_lambda_function.pipeline_security_monitor.function_name],
            [".", "Errors", ".", "."],
            [".", "Invocations", ".", "."]
          ]
          view    = "timeSeries"
          stacked = false
          region  = var.aws_region
          title   = "Pipeline Security Monitor Metrics"
          period  = 300
        }
      },
      {
        type   = "log"
        x      = 0
        y      = 12
        width  = 24
        height = 6
        
        properties = {
          query   = "SOURCE '/aws/lambda/${aws_lambda_function.pipeline_security_assessor.function_name}' | fields @timestamp, @message | filter @message like /CRITICAL/ | sort @timestamp desc | limit 20"
          region  = var.aws_region
          title   = "Critical Security Issues"
          view    = "table"
        }
      }
    ]
  })
}

# Data sources
data "aws_caller_identity" "current" {}

# Outputs
output "assessment_table_name" {
  description = "Name of the DynamoDB table for assessment results"
  value       = aws_dynamodb_table.pipeline_security_assessments.name
}

output "monitoring_table_name" {
  description = "Name of the DynamoDB table for monitoring results"
  value       = aws_dynamodb_table.pipeline_security_monitoring.name
}

output "alert_topic_arn" {
  description = "ARN of the SNS topic for security alerts"
  value       = aws_sns_topic.pipeline_security_alerts.arn
}

output "assessor_function_name" {
  description = "Name of the pipeline security assessor Lambda function"
  value       = aws_lambda_function.pipeline_security_assessor.function_name
}

output "monitor_function_name" {
  description = "Name of the pipeline security monitor Lambda function"
  value       = aws_lambda_function.pipeline_security_monitor.function_name
}

output "dashboard_url" {
  description = "URL of the CloudWatch dashboard"
  value       = "https://${var.aws_region}.console.aws.amazon.com/cloudwatch/home?region=${var.aws_region}#dashboards:name=${aws_cloudwatch_dashboard.pipeline_security_dashboard.dashboard_name}"
}
```
### Example 4: Pipeline security compliance checker script

```bash
#!/bin/bash
# pipeline-security-compliance-checker.sh
# Comprehensive pipeline security compliance validation script

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="${SCRIPT_DIR}/pipeline-security-check.log"
REPORT_FILE="${SCRIPT_DIR}/pipeline-security-report.json"
AWS_REGION="${AWS_REGION:-us-west-2}"
COMPLIANCE_THRESHOLD=80

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

# Error handling
error_exit() {
    echo -e "${RED}ERROR: $1${NC}" >&2
    exit 1
}

# Success message
success() {
    echo -e "${GREEN}✓ $1${NC}"
}

# Warning message
warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Info message
info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Initialize report structure
init_report() {
    cat > "$REPORT_FILE" << EOF
{
  "assessment_timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "aws_region": "$AWS_REGION",
  "pipelines_assessed": [],
  "overall_compliance_score": 0,
  "compliance_threshold": $COMPLIANCE_THRESHOLD,
  "passed": false,
  "summary": {
    "total_pipelines": 0,
    "compliant_pipelines": 0,
    "non_compliant_pipelines": 0,
    "critical_issues": 0,
    "high_issues": 0,
    "medium_issues": 0,
    "low_issues": 0
  },
  "recommendations": []
}
EOF
}

# Get list of all CodePipeline pipelines
get_pipelines() {
    log "Retrieving list of CodePipeline pipelines..."
    
    aws codepipeline list-pipelines \
        --region "$AWS_REGION" \
        --query 'pipelines[].name' \
        --output text || error_exit "Failed to retrieve pipeline list"
}

# Check pipeline encryption settings
check_pipeline_encryption() {
    local pipeline_name=$1
    local issues=()
    
    log "Checking encryption settings for pipeline: $pipeline_name"
    
    # Get pipeline configuration
    local pipeline_config
    pipeline_config=$(aws codepipeline get-pipeline \
        --name "$pipeline_name" \
        --region "$AWS_REGION" \
        --output json) || return 1
    
    # Check artifact store encryption
    local artifact_stores
    artifact_stores=$(echo "$pipeline_config" | jq -r '.pipeline.artifactStore // .pipeline.artifactStores // empty')
    
    if [[ -z "$artifact_stores" ]]; then
        issues+=("No artifact store configuration found")
    else
        # Handle both single artifact store and multiple artifact stores
        local encryption_keys
        encryption_keys=$(echo "$artifact_stores" | jq -r '
            if type == "object" then
                if .encryptionKey then "encrypted" else "not_encrypted" end
            elif type == "array" then
                map(if .encryptionKey then "encrypted" else "not_encrypted" end) | join(",")
            else
                "unknown"
            end
        ')
        
        if [[ "$encryption_keys" == *"not_encrypted"* ]]; then
            issues+=("Artifact store is not encrypted")
        fi
    fi
    
    # Return issues as JSON array
    printf '%s\n' "${issues[@]}" | jq -R . | jq -s .
}

# Check pipeline IAM permissions
check_pipeline_iam() {
    local pipeline_name=$1
    local issues=()
    
    log "Checking IAM permissions for pipeline: $pipeline_name"
    
    # Get pipeline service role
    local service_role_arn
    service_role_arn=$(aws codepipeline get-pipeline \
        --name "$pipeline_name" \
        --region "$AWS_REGION" \
        --query 'pipeline.roleArn' \
        --output text) || return 1
    
    if [[ "$service_role_arn" == "None" || -z "$service_role_arn" ]]; then
        issues+=("No service role configured for pipeline")
        printf '%s\n' "${issues[@]}" | jq -R . | jq -s .
        return 0
    fi
    
    # Extract role name from ARN
    local role_name
    role_name=$(echo "$service_role_arn" | awk -F'/' '{print $NF}')
    
    # Check for overly broad policies
    local attached_policies
    attached_policies=$(aws iam list-attached-role-policies \
        --role-name "$role_name" \
        --query 'AttachedPolicies[].PolicyArn' \
        --output text) || return 1
    
    for policy_arn in $attached_policies; do
        if [[ "$policy_arn" == *"FullAccess"* ]] || [[ "$policy_arn" == *"PowerUser"* ]]; then
            issues+=("Role has overly broad policy: $(basename "$policy_arn")")
        fi
    done
    
    # Check inline policies for wildcard permissions
    local inline_policies
    inline_policies=$(aws iam list-role-policies \
        --role-name "$role_name" \
        --query 'PolicyNames' \
        --output text) || return 1
    
    for policy_name in $inline_policies; do
        local policy_document
        policy_document=$(aws iam get-role-policy \
            --role-name "$role_name" \
            --policy-name "$policy_name" \
            --query 'PolicyDocument' \
            --output json) || continue
        
        # Check for wildcard actions or resources
        local wildcard_actions
        wildcard_actions=$(echo "$policy_document" | jq -r '
            .Statement[]? | 
            select(.Action == "*" or (.Action | type == "array" and contains(["*"]))) |
            "Wildcard action in policy: " + (.Sid // "unnamed")
        ')
        
        local wildcard_resources
        wildcard_resources=$(echo "$policy_document" | jq -r '
            .Statement[]? | 
            select(.Resource == "*" or (.Resource | type == "array" and contains(["*"]))) |
            "Wildcard resource in policy: " + (.Sid // "unnamed")
        ')
        
        if [[ -n "$wildcard_actions" ]]; then
            issues+=("$wildcard_actions")
        fi
        
        if [[ -n "$wildcard_resources" ]]; then
            issues+=("$wildcard_resources")
        fi
    done
    
    printf '%s\n' "${issues[@]}" | jq -R . | jq -s .
}

# Check pipeline logging configuration
check_pipeline_logging() {
    local pipeline_name=$1
    local issues=()
    
    log "Checking logging configuration for pipeline: $pipeline_name"
    
    # Get pipeline configuration
    local pipeline_config
    pipeline_config=$(aws codepipeline get-pipeline \
        --name "$pipeline_name" \
        --region "$AWS_REGION" \
        --output json) || return 1
    
    # Check for CodeBuild projects and their logging
    local build_projects
    build_projects=$(echo "$pipeline_config" | jq -r '
        .pipeline.stages[]?.actions[]? |
        select(.actionTypeId.provider == "CodeBuild") |
        .configuration.ProjectName
    ')
    
    for project_name in $build_projects; do
        if [[ -n "$project_name" ]]; then
            local project_config
            project_config=$(aws codebuild describe-projects \
                --names "$project_name" \
                --region "$AWS_REGION" \
                --output json) || continue
            
            local cloudwatch_logs_status
            cloudwatch_logs_status=$(echo "$project_config" | jq -r '
                .projects[0].logsConfig.cloudWatchLogs.status // "DISABLED"
            ')
            
            if [[ "$cloudwatch_logs_status" != "ENABLED" ]]; then
                issues+=("CodeBuild project $project_name does not have CloudWatch logging enabled")
            fi
        fi
    done
    
    # Check if CloudTrail is logging CodePipeline events
    local cloudtrail_events
    cloudtrail_events=$(aws cloudtrail lookup-events \
        --lookup-attributes AttributeKey=EventSource,AttributeValue=codepipeline.amazonaws.com \
        --start-time "$(date -d '7 days ago' -u +%Y-%m-%dT%H:%M:%SZ)" \
        --end-time "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
        --region "$AWS_REGION" \
        --max-items 1 \
        --query 'Events | length(@)' \
        --output text) || cloudtrail_events=0
    
    if [[ "$cloudtrail_events" -eq 0 ]]; then
        issues+=("No CloudTrail events found for CodePipeline activities")
    fi
    
    printf '%s\n' "${issues[@]}" | jq -R . | jq -s .
}

# Check pipeline monitoring and alerting
check_pipeline_monitoring() {
    local pipeline_name=$1
    local issues=()
    
    log "Checking monitoring and alerting for pipeline: $pipeline_name"
    
    # Check for CloudWatch alarms related to the pipeline
    local alarms
    alarms=$(aws cloudwatch describe-alarms \
        --alarm-name-prefix "$pipeline_name" \
        --region "$AWS_REGION" \
        --query 'MetricAlarms | length(@)' \
        --output text) || alarms=0
    
    if [[ "$alarms" -eq 0 ]]; then
        issues+=("No CloudWatch alarms configured for pipeline monitoring")
    fi
    
    # Check for SNS topics for notifications
    local pipeline_config
    pipeline_config=$(aws codepipeline get-pipeline \
        --name "$pipeline_name" \
        --region "$AWS_REGION" \
        --output json) || return 1
    
    local manual_approval_actions
    manual_approval_actions=$(echo "$pipeline_config" | jq -r '
        .pipeline.stages[]?.actions[]? |
        select(.actionTypeId.provider == "Manual") |
        .configuration.NotificationArn // empty
    ')
    
    local has_notifications=false
    for notification_arn in $manual_approval_actions; do
        if [[ -n "$notification_arn" ]]; then
            has_notifications=true
            break
        fi
    done
    
    if [[ "$has_notifications" == false ]]; then
        issues+=("No SNS notifications configured for manual approval actions")
    fi
    
    printf '%s\n' "${issues[@]}" | jq -R . | jq -s .
}

# Check pipeline security controls
check_pipeline_security_controls() {
    local pipeline_name=$1
    local issues=()
    
    log "Checking security controls for pipeline: $pipeline_name"
    
    # Get pipeline configuration
    local pipeline_config
    pipeline_config=$(aws codepipeline get-pipeline \
        --name "$pipeline_name" \
        --region "$AWS_REGION" \
        --output json) || return 1
    
    # Check for manual approval gates
    local manual_approvals
    manual_approvals=$(echo "$pipeline_config" | jq -r '
        .pipeline.stages[]?.actions[]? |
        select(.actionTypeId.provider == "Manual") |
        .name
    ')
    
    if [[ -z "$manual_approvals" ]]; then
        issues+=("No manual approval gates found in pipeline")
    fi
    
    # Check for security testing stages
    local security_testing=false
    local stage_names
    stage_names=$(echo "$pipeline_config" | jq -r '.pipeline.stages[].name')
    
    for stage_name in $stage_names; do
        if [[ "$stage_name" == *"Security"* ]] || [[ "$stage_name" == *"Test"* ]] || [[ "$stage_name" == *"Scan"* ]]; then
            security_testing=true
            break
        fi
    done
    
    if [[ "$security_testing" == false ]]; then
        issues+=("No apparent security testing stages in pipeline")
    fi
    
    # Check CodeBuild projects for security configurations
    local build_projects
    build_projects=$(echo "$pipeline_config" | jq -r '
        .pipeline.stages[]?.actions[]? |
        select(.actionTypeId.provider == "CodeBuild") |
        .configuration.ProjectName
    ')
    
    for project_name in $build_projects; do
        if [[ -n "$project_name" ]]; then
            local project_config
            project_config=$(aws codebuild describe-projects \
                --names "$project_name" \
                --region "$AWS_REGION" \
                --output json) || continue
            
            # Check if privileged mode is enabled
            local privileged_mode
            privileged_mode=$(echo "$project_config" | jq -r '
                .projects[0].environment.privilegedMode // false
            ')
            
            if [[ "$privileged_mode" == "true" ]]; then
                issues+=("CodeBuild project $project_name runs in privileged mode")
            fi
            
            # Check if VPC configuration is present
            local vpc_config
            vpc_config=$(echo "$project_config" | jq -r '
                .projects[0].vpcConfig // empty
            ')
            
            if [[ -z "$vpc_config" ]]; then
                issues+=("CodeBuild project $project_name is not configured to run in VPC")
            fi
        fi
    done
    
    printf '%s\n' "${issues[@]}" | jq -R . | jq -s .
}

# Assess single pipeline
assess_pipeline() {
    local pipeline_name=$1
    
    info "Assessing pipeline: $pipeline_name"
    
    local encryption_issues
    local iam_issues
    local logging_issues
    local monitoring_issues
    local security_issues
    
    encryption_issues=$(check_pipeline_encryption "$pipeline_name")
    iam_issues=$(check_pipeline_iam "$pipeline_name")
    logging_issues=$(check_pipeline_logging "$pipeline_name")
    monitoring_issues=$(check_pipeline_monitoring "$pipeline_name")
    security_issues=$(check_pipeline_security_controls "$pipeline_name")
    
    # Calculate compliance score
    local total_checks=5
    local passed_checks=0
    
    [[ $(echo "$encryption_issues" | jq 'length') -eq 0 ]] && ((passed_checks++))
    [[ $(echo "$iam_issues" | jq 'length') -eq 0 ]] && ((passed_checks++))
    [[ $(echo "$logging_issues" | jq 'length') -eq 0 ]] && ((passed_checks++))
    [[ $(echo "$monitoring_issues" | jq 'length') -eq 0 ]] && ((passed_checks++))
    [[ $(echo "$security_issues" | jq 'length') -eq 0 ]] && ((passed_checks++))
    
    local compliance_score=$((passed_checks * 100 / total_checks))
    
    # Determine compliance status
    local compliant=false
    [[ $compliance_score -ge $COMPLIANCE_THRESHOLD ]] && compliant=true
    
    # Count issue severities
    local critical_count=0
    local high_count=0
    local medium_count=0
    local low_count=0
    
    # Categorize issues by severity
    for issues in "$encryption_issues" "$iam_issues" "$security_issues"; do
        local count
        count=$(echo "$issues" | jq 'length')
        critical_count=$((critical_count + count))
    done
    
    for issues in "$logging_issues" "$monitoring_issues"; do
        local count
        count=$(echo "$issues" | jq 'length')
        medium_count=$((medium_count + count))
    done
    
    # Create pipeline assessment result
    local pipeline_result
    pipeline_result=$(jq -n \
        --arg name "$pipeline_name" \
        --argjson score "$compliance_score" \
        --argjson compliant "$compliant" \
        --argjson encryption_issues "$encryption_issues" \
        --argjson iam_issues "$iam_issues" \
        --argjson logging_issues "$logging_issues" \
        --argjson monitoring_issues "$monitoring_issues" \
        --argjson security_issues "$security_issues" \
        --argjson critical "$critical_count" \
        --argjson high "$high_count" \
        --argjson medium "$medium_count" \
        --argjson low "$low_count" \
        '{
            pipeline_name: $name,
            compliance_score: $score,
            compliant: $compliant,
            issues: {
                encryption: $encryption_issues,
                iam: $iam_issues,
                logging: $logging_issues,
                monitoring: $monitoring_issues,
                security_controls: $security_issues
            },
            issue_counts: {
                critical: $critical,
                high: $high,
                medium: $medium,
                low: $low
            }
        }')
    
    # Update report with pipeline results
    local temp_report
    temp_report=$(mktemp)
    jq --argjson pipeline "$pipeline_result" '
        .pipelines_assessed += [$pipeline] |
        .summary.total_pipelines += 1 |
        if $pipeline.compliant then
            .summary.compliant_pipelines += 1
        else
            .summary.non_compliant_pipelines += 1
        end |
        .summary.critical_issues += $pipeline.issue_counts.critical |
        .summary.high_issues += $pipeline.issue_counts.high |
        .summary.medium_issues += $pipeline.issue_counts.medium |
        .summary.low_issues += $pipeline.issue_counts.low
    ' "$REPORT_FILE" > "$temp_report" && mv "$temp_report" "$REPORT_FILE"
    
    if [[ "$compliant" == "true" ]]; then
        success "Pipeline $pipeline_name is compliant (Score: $compliance_score%)"
    else
        warning "Pipeline $pipeline_name is non-compliant (Score: $compliance_score%)"
    fi
}

# Generate final report and recommendations
finalize_report() {
    log "Finalizing security assessment report..."
    
    # Calculate overall compliance score
    local total_pipelines
    local compliant_pipelines
    total_pipelines=$(jq -r '.summary.total_pipelines' "$REPORT_FILE")
    compliant_pipelines=$(jq -r '.summary.compliant_pipelines' "$REPORT_FILE")
    
    local overall_score=0
    if [[ $total_pipelines -gt 0 ]]; then
        overall_score=$((compliant_pipelines * 100 / total_pipelines))
    fi
    
    # Determine overall pass/fail
    local overall_passed=false
    [[ $overall_score -ge $COMPLIANCE_THRESHOLD ]] && overall_passed=true
    
    # Generate recommendations
    local recommendations=()
    
    local critical_issues
    local high_issues
    critical_issues=$(jq -r '.summary.critical_issues' "$REPORT_FILE")
    high_issues=$(jq -r '.summary.high_issues' "$REPORT_FILE")
    
    if [[ $critical_issues -gt 0 ]]; then
        recommendations+=("URGENT: Address $critical_issues critical security issues immediately")
    fi
    
    if [[ $high_issues -gt 0 ]]; then
        recommendations+=("Address $high_issues high-priority security issues within 24 hours")
    fi
    
    if [[ $overall_score -lt $COMPLIANCE_THRESHOLD ]]; then
        recommendations+=("Overall compliance score ($overall_score%) is below threshold ($COMPLIANCE_THRESHOLD%)")
        recommendations+=("Implement comprehensive security controls across all pipelines")
    fi
    
    # Update final report
    local temp_report
    temp_report=$(mktemp)
    jq --argjson score "$overall_score" \
       --argjson passed "$overall_passed" \
       --argjson recs "$(printf '%s\n' "${recommendations[@]}" | jq -R . | jq -s .)" \
       '.overall_compliance_score = $score |
        .passed = $passed |
        .recommendations = $recs' \
       "$REPORT_FILE" > "$temp_report" && mv "$temp_report" "$REPORT_FILE"
}

# Print summary
print_summary() {
    echo
    echo "=========================================="
    echo "PIPELINE SECURITY ASSESSMENT SUMMARY"
    echo "=========================================="
    
    local total_pipelines
    local compliant_pipelines
    local overall_score
    local passed
    
    total_pipelines=$(jq -r '.summary.total_pipelines' "$REPORT_FILE")
    compliant_pipelines=$(jq -r '.summary.compliant_pipelines' "$REPORT_FILE")
    overall_score=$(jq -r '.overall_compliance_score' "$REPORT_FILE")
    passed=$(jq -r '.passed' "$REPORT_FILE")
    
    echo "Total Pipelines Assessed: $total_pipelines"
    echo "Compliant Pipelines: $compliant_pipelines"
    echo "Non-Compliant Pipelines: $((total_pipelines - compliant_pipelines))"
    echo "Overall Compliance Score: $overall_score%"
    echo "Compliance Threshold: $COMPLIANCE_THRESHOLD%"
    
    if [[ "$passed" == "true" ]]; then
        success "OVERALL ASSESSMENT: PASSED"
    else
        warning "OVERALL ASSESSMENT: FAILED"
    fi
    
    echo
    echo "Issue Summary:"
    jq -r '
        "  Critical Issues: " + (.summary.critical_issues | tostring) + "\n" +
        "  High Issues: " + (.summary.high_issues | tostring) + "\n" +
        "  Medium Issues: " + (.summary.medium_issues | tostring) + "\n" +
        "  Low Issues: " + (.summary.low_issues | tostring)
    ' "$REPORT_FILE"
    
    echo
    echo "Recommendations:"
    jq -r '.recommendations[] | "  • " + .' "$REPORT_FILE"
    
    echo
    echo "Detailed report saved to: $REPORT_FILE"
    echo "Log file saved to: $LOG_FILE"
}

# Main execution
main() {
    echo "Starting Pipeline Security Compliance Assessment..."
    echo "Region: $AWS_REGION"
    echo "Compliance Threshold: $COMPLIANCE_THRESHOLD%"
    echo
    
    # Initialize
    init_report
    
    # Get list of pipelines
    local pipelines
    pipelines=$(get_pipelines)
    
    if [[ -z "$pipelines" ]]; then
        warning "No CodePipeline pipelines found in region $AWS_REGION"
        exit 0
    fi
    
    # Assess each pipeline
    for pipeline in $pipelines; do
        assess_pipeline "$pipeline"
    done
    
    # Finalize report
    finalize_report
    
    # Print summary
    print_summary
    
    # Exit with appropriate code
    local passed
    passed=$(jq -r '.passed' "$REPORT_FILE")
    
    if [[ "$passed" == "true" ]]; then
        exit 0
    else
        exit 1
    fi
}

# Check dependencies
check_dependencies() {
    local deps=("aws" "jq")
    
    for dep in "${deps[@]}"; do
        if ! command -v "$dep" &> /dev/null; then
            error_exit "$dep is required but not installed"
        fi
    done
    
    # Check AWS CLI configuration
    if ! aws sts get-caller-identity &> /dev/null; then
        error_exit "AWS CLI is not configured or credentials are invalid"
    fi
}

# Script entry point
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    check_dependencies
    main "$@"
fi
```

## AWS services to consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS CodePipeline</h4>
    <p>Continuous delivery service that provides the pipeline infrastructure to assess. Understanding pipeline configuration is essential for security evaluation.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS CodeBuild</h4>
    <p>Build service that executes within pipelines. Security assessment must evaluate build environment configurations, permissions, and isolation.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS CloudTrail</h4>
    <p>Audit logging service that tracks API calls and user activities. Essential for monitoring pipeline access and detecting suspicious activities.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon CloudWatch</h4>
    <p>Monitoring and observability service for tracking pipeline metrics, logs, and setting up alerts for security events.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Lambda</h4>
    <p>Serverless compute service for running automated security assessments and monitoring functions without managing infrastructure.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon DynamoDB</h4>
    <p>NoSQL database service for storing assessment results, monitoring data, and maintaining historical security metrics.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon SNS</h4>
    <p>Messaging service for sending security alerts and notifications when pipeline security issues are detected.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Config</h4>
    <p>Configuration management service for tracking changes to pipeline resources and ensuring compliance with security policies.</p>
  </div>
</div>

## Benefits of regularly assessing security properties of pipelines

- **Proactive threat detection**: Identifies security vulnerabilities before they can be exploited
- **Compliance assurance**: Ensures pipelines meet security standards and regulatory requirements
- **Risk mitigation**: Reduces the likelihood of supply chain attacks and security breaches
- **Continuous improvement**: Enables ongoing enhancement of pipeline security posture
- **Audit readiness**: Provides comprehensive documentation for security audits and reviews
- **Incident prevention**: Prevents security incidents through early detection and remediation
- **Cost optimization**: Reduces potential costs associated with security breaches and downtime
- **Stakeholder confidence**: Demonstrates commitment to security best practices to customers and partners

## Related resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/sec_appsec_regularly_assess_security_properties_of_pipelines.html">AWS Well-Architected Framework - Regularly assess security properties of the pipelines</a></li>
    <li><a href="https://docs.aws.amazon.com/codepipeline/latest/userguide/security.html">AWS CodePipeline Security</a></li>
    <li><a href="https://docs.aws.amazon.com/codebuild/latest/userguide/security.html">AWS CodeBuild Security</a></li>
    <li><a href="https://aws.amazon.com/blogs/devops/validating-aws-codepipeline-pipeline-configuration-using-aws-config-rules/">Validating AWS CodePipeline pipeline configuration using AWS Config Rules</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-monitor-and-visualize-failed-ssh-access-attempts-to-amazon-ec2-linux-instances/">How to monitor and visualize failed SSH access attempts to Amazon EC2 Linux instances</a></li>
    <li><a href="https://docs.aws.amazon.com/config/latest/developerguide/evaluate-config.html">Evaluating Resources with AWS Config Rules</a></li>
  </ul>
</div>
