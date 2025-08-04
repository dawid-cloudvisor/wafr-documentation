---
title: COST04-BP02 - Implement a decommissioning process
layout: default
parent: COST04 - How do you decommission resources?
grand_parent: Cost Optimization
nav_order: 2
---

<div class="pillar-header">
  <h1>COST04-BP02: Implement a decommissioning process</h1>
  <p>Establish systematic processes and procedures for safely decommissioning resources while ensuring data protection, service continuity, and compliance requirements are met. A well-defined process reduces risks and ensures consistent execution.</p>
</div>

## Implementation guidance

A structured decommissioning process provides the framework for safely and efficiently removing resources while minimizing risks to business operations, data integrity, and compliance requirements.

### Process Design Principles

**Risk Management**: Implement comprehensive risk assessment and mitigation strategies to prevent service disruptions and data loss during decommissioning.

**Stakeholder Involvement**: Ensure appropriate stakeholders are involved in decommissioning decisions and execution to maintain business alignment.

**Documentation**: Maintain detailed documentation of decommissioning procedures, decisions, and outcomes for audit and learning purposes.

**Validation**: Include validation steps to confirm successful decommissioning and verify that objectives have been achieved.

### Process Components

**Assessment Phase**: Systematic evaluation of resources for decommissioning including impact analysis and stakeholder consultation.

**Planning Phase**: Detailed planning of decommissioning activities including timeline, resource allocation, and risk mitigation.

**Execution Phase**: Coordinated execution of decommissioning activities with proper monitoring and validation.

**Validation Phase**: Confirmation of successful decommissioning and achievement of objectives.

## AWS Services to Consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Systems Manager</h4>
    <p>Orchestrate decommissioning workflows and automate process execution. Use Systems Manager for coordinated resource shutdown and validation.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Step Functions</h4>
    <p>Create complex decommissioning workflows with error handling and rollback capabilities. Use Step Functions for multi-step decommissioning processes.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Lambda</h4>
    <p>Implement custom decommissioning logic and automation. Use Lambda for event-driven decommissioning and validation functions.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon SNS</h4>
    <p>Send notifications and alerts during decommissioning processes. Use SNS for stakeholder communication and approval workflows.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS CloudFormation</h4>
    <p>Manage infrastructure as code for coordinated resource decommissioning. Use CloudFormation for stack-based resource lifecycle management.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon DynamoDB</h4>
    <p>Track decommissioning process status and maintain audit trails. Use DynamoDB for process state management and historical records.</p>
  </div>
</div>

## Implementation Steps

### 1. Define Process Framework
- Establish decommissioning process governance and ownership
- Define roles and responsibilities for process execution
- Create process documentation and standard operating procedures
- Establish approval workflows and escalation procedures

### 2. Design Assessment Procedures
- Create resource evaluation criteria and methodologies
- Develop impact assessment frameworks and tools
- Design stakeholder consultation and approval processes
- Establish risk assessment and mitigation procedures

### 3. Create Planning Templates
- Develop decommissioning planning templates and checklists
- Create timeline and resource allocation frameworks
- Design rollback and recovery procedures
- Establish communication and notification protocols

### 4. Implement Execution Workflows
- Create automated decommissioning workflows and procedures
- Implement monitoring and validation mechanisms
- Design error handling and exception management
- Create audit logging and documentation systems

### 5. Establish Validation Procedures
- Define success criteria and validation methods
- Create post-decommissioning verification processes
- Implement cost savings validation and reporting
- Design lessons learned and improvement processes

### 6. Enable Continuous Improvement
- Monitor process effectiveness and efficiency
- Gather feedback from stakeholders and process users
- Refine processes based on lessons learned and best practices
- Update procedures based on changing requirements and technologies

## Decommissioning Process Framework

### Process Workflow Implementation
```python
import boto3
import json
from datetime import datetime, timedelta
from enum import Enum

class DecommissioningStatus(Enum):
    IDENTIFIED = "identified"
    ASSESSED = "assessed"
    APPROVED = "approved"
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"

class DecommissioningProcess:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.sns = boto3.client('sns')
        self.stepfunctions = boto3.client('stepfunctions')
        self.process_table = self.dynamodb.Table('DecommissioningProcess')
        self.audit_table = self.dynamodb.Table('DecommissioningAudit')
    
    def initiate_decommissioning(self, resource_id, resource_type, initiator, reason):
        """Initiate decommissioning process for a resource"""
        
        process_id = f"DECOMM-{datetime.now().strftime('%Y%m%d%H%M%S')}-{resource_id}"
        
        # Create process record
        process_record = {
            'ProcessId': process_id,
            'ResourceId': resource_id,
            'ResourceType': resource_type,
            'Status': DecommissioningStatus.IDENTIFIED.value,
            'Initiator': initiator,
            'Reason': reason,
            'CreatedAt': datetime.now().isoformat(),
            'LastUpdated': datetime.now().isoformat(),
            'ProcessSteps': [],
            'Stakeholders': [],
            'ApprovalRequired': True,
            'RiskLevel': 'medium'  # Default, will be updated during assessment
        }
        
        # Store process record
        self.process_table.put_item(Item=process_record)
        
        # Log audit event
        self.log_audit_event(process_id, 'PROCESS_INITIATED', {
            'resource_id': resource_id,
            'initiator': initiator,
            'reason': reason
        })
        
        # Start assessment phase
        self.start_assessment_phase(process_id)
        
        return process_id
    
    def start_assessment_phase(self, process_id):
        """Start the assessment phase of decommissioning"""
        
        # Get process record
        process = self.get_process_record(process_id)
        
        # Perform automated assessment
        assessment_results = self.perform_automated_assessment(
            process['ResourceId'], 
            process['ResourceType']
        )
        
        # Update process with assessment results
        self.process_table.update_item(
            Key={'ProcessId': process_id},
            UpdateExpression='SET #status = :status, AssessmentResults = :assessment, LastUpdated = :timestamp',
            ExpressionAttributeNames={'#status': 'Status'},
            ExpressionAttributeValues={
                ':status': DecommissioningStatus.ASSESSED.value,
                ':assessment': assessment_results,
                ':timestamp': datetime.now().isoformat()
            }
        )
        
        # Determine if approval is required
        if assessment_results['risk_level'] in ['high', 'critical']:
            self.request_approval(process_id, assessment_results)
        else:
            self.auto_approve_low_risk(process_id)
        
        # Log audit event
        self.log_audit_event(process_id, 'ASSESSMENT_COMPLETED', assessment_results)
    
    def perform_automated_assessment(self, resource_id, resource_type):
        """Perform automated assessment of decommissioning impact"""
        
        assessment = {
            'resource_id': resource_id,
            'resource_type': resource_type,
            'assessment_timestamp': datetime.now().isoformat(),
            'risk_level': 'low',
            'impact_analysis': {},
            'dependencies': [],
            'recommendations': []
        }
        
        # Get resource dependencies
        dependencies = self.get_resource_dependencies(resource_id)
        assessment['dependencies'] = dependencies
        
        # Assess business impact
        business_impact = self.assess_business_impact(resource_id, resource_type)
        assessment['impact_analysis']['business'] = business_impact
        
        # Assess technical impact
        technical_impact = self.assess_technical_impact(resource_id, resource_type, dependencies)
        assessment['impact_analysis']['technical'] = technical_impact
        
        # Determine overall risk level
        assessment['risk_level'] = self.calculate_risk_level(business_impact, technical_impact, dependencies)
        
        # Generate recommendations
        assessment['recommendations'] = self.generate_recommendations(assessment)
        
        return assessment
    
    def get_resource_dependencies(self, resource_id):
        """Get dependencies for the resource being decommissioned"""
        
        try:
            dependency_table = self.dynamodb.Table('ResourceDependencies')
            response = dependency_table.get_item(
                Key={'ResourceId': resource_id}
            )
            
            if 'Item' in response:
                return {
                    'dependencies': response['Item'].get('Dependencies', []),
                    'dependents': response['Item'].get('Dependents', [])
                }
            else:
                return {'dependencies': [], 'dependents': []}
                
        except Exception as e:
            return {'dependencies': [], 'dependents': [], 'error': str(e)}
    
    def assess_business_impact(self, resource_id, resource_type):
        """Assess business impact of decommissioning"""
        
        # Get resource metadata
        tracking_table = self.dynamodb.Table('ResourceTracking')
        
        try:
            response = tracking_table.get_item(
                Key={
                    'ResourceId': resource_id,
                    'ResourceType': resource_type
                }
            )
            
            if 'Item' in response:
                tracking_data = response['Item']['TrackingData']
                
                # Analyze business context
                environment = tracking_data.get('environment', 'unknown')
                project = tracking_data.get('project', 'unknown')
                owner = tracking_data.get('owner', 'unknown')
                
                # Determine business criticality
                if environment.lower() == 'production':
                    criticality = 'high'
                elif environment.lower() in ['staging', 'pre-prod']:
                    criticality = 'medium'
                else:
                    criticality = 'low'
                
                return {
                    'criticality': criticality,
                    'environment': environment,
                    'project': project,
                    'owner': owner,
                    'business_hours_impact': criticality == 'high'
                }
            
        except Exception as e:
            pass
        
        return {
            'criticality': 'unknown',
            'environment': 'unknown',
            'project': 'unknown',
            'owner': 'unknown',
            'business_hours_impact': True  # Conservative assumption
        }
    
    def assess_technical_impact(self, resource_id, resource_type, dependencies):
        """Assess technical impact of decommissioning"""
        
        impact = {
            'dependency_count': len(dependencies.get('dependents', [])),
            'has_critical_dependencies': False,
            'data_loss_risk': False,
            'service_disruption_risk': False
        }
        
        # Check for critical dependencies
        for dependent in dependencies.get('dependents', []):
            if dependent.get('dependency_type') in ['critical', 'required']:
                impact['has_critical_dependencies'] = True
                impact['service_disruption_risk'] = True
        
        # Assess data loss risk based on resource type
        if resource_type in ['RDSInstance', 'S3Bucket', 'EBSVolume']:
            impact['data_loss_risk'] = True
        
        # Assess service disruption risk
        if resource_type in ['EC2Instance', 'LoadBalancer', 'RDSInstance']:
            if impact['dependency_count'] > 0:
                impact['service_disruption_risk'] = True
        
        return impact
    
    def calculate_risk_level(self, business_impact, technical_impact, dependencies):
        """Calculate overall risk level for decommissioning"""
        
        risk_score = 0
        
        # Business impact scoring
        if business_impact['criticality'] == 'high':
            risk_score += 3
        elif business_impact['criticality'] == 'medium':
            risk_score += 2
        elif business_impact['criticality'] == 'low':
            risk_score += 1
        
        # Technical impact scoring
        if technical_impact['has_critical_dependencies']:
            risk_score += 3
        if technical_impact['data_loss_risk']:
            risk_score += 2
        if technical_impact['service_disruption_risk']:
            risk_score += 2
        
        # Dependency scoring
        dependent_count = len(dependencies.get('dependents', []))
        if dependent_count > 5:
            risk_score += 2
        elif dependent_count > 0:
            risk_score += 1
        
        # Determine risk level
        if risk_score >= 7:
            return 'critical'
        elif risk_score >= 5:
            return 'high'
        elif risk_score >= 3:
            return 'medium'
        else:
            return 'low'
    
    def request_approval(self, process_id, assessment_results):
        """Request approval for high-risk decommissioning"""
        
        # Get process record
        process = self.get_process_record(process_id)
        
        # Determine approvers based on risk level and resource type
        approvers = self.determine_approvers(assessment_results, process)
        
        # Send approval request
        approval_message = {
            'process_id': process_id,
            'resource_id': process['ResourceId'],
            'resource_type': process['ResourceType'],
            'risk_level': assessment_results['risk_level'],
            'assessment_summary': assessment_results,
            'approval_url': f"https://decommissioning-portal.company.com/approve/{process_id}"
        }
        
        for approver in approvers:
            self.sns.publish(
                TopicArn=f"arn:aws:sns:region:account:decommissioning-approvals-{approver}",
                Message=json.dumps(approval_message, indent=2),
                Subject=f"Decommissioning Approval Required: {process['ResourceId']}"
            )
        
        # Update process status
        self.process_table.update_item(
            Key={'ProcessId': process_id},
            UpdateExpression='SET #status = :status, Approvers = :approvers, LastUpdated = :timestamp',
            ExpressionAttributeNames={'#status': 'Status'},
            ExpressionAttributeValues={
                ':status': 'awaiting_approval',
                ':approvers': approvers,
                ':timestamp': datetime.now().isoformat()
            }
        )
        
        # Log audit event
        self.log_audit_event(process_id, 'APPROVAL_REQUESTED', {
            'approvers': approvers,
            'risk_level': assessment_results['risk_level']
        })
    
    def determine_approvers(self, assessment_results, process):
        """Determine required approvers based on risk and resource characteristics"""
        
        approvers = []
        
        # Always require resource owner approval
        if process.get('ResourceOwner'):
            approvers.append(process['ResourceOwner'])
        
        # Risk-based approvals
        risk_level = assessment_results['risk_level']
        
        if risk_level in ['high', 'critical']:
            approvers.extend(['infrastructure-manager', 'security-team'])
        
        if risk_level == 'critical':
            approvers.extend(['cto', 'compliance-officer'])
        
        # Environment-based approvals
        business_impact = assessment_results['impact_analysis']['business']
        if business_impact['environment'].lower() == 'production':
            approvers.append('production-manager')
        
        # Data-related approvals
        technical_impact = assessment_results['impact_analysis']['technical']
        if technical_impact['data_loss_risk']:
            approvers.append('data-protection-officer')
        
        return list(set(approvers))  # Remove duplicates
    
    def log_audit_event(self, process_id, event_type, event_data):
        """Log audit event for decommissioning process"""
        
        audit_record = {
            'ProcessId': process_id,
            'EventId': f"{process_id}-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'EventType': event_type,
            'EventData': event_data,
            'Timestamp': datetime.now().isoformat(),
            'TTL': int((datetime.now() + timedelta(days=2555)).timestamp())  # 7 years retention
        }
        
        try:
            self.audit_table.put_item(Item=audit_record)
        except Exception as e:
            print(f"Error logging audit event: {str(e)}")
    
    def get_process_record(self, process_id):
        """Get decommissioning process record"""
        
        response = self.process_table.get_item(Key={'ProcessId': process_id})
        return response.get('Item', {})
```

### Step Functions Workflow
```python
def create_decommissioning_workflow():
    """Create Step Functions workflow for decommissioning process"""
    
    workflow_definition = {
        "Comment": "Resource Decommissioning Workflow",
        "StartAt": "AssessResource",
        "States": {
            "AssessResource": {
                "Type": "Task",
                "Resource": "arn:aws:lambda:REGION:ACCOUNT:function:AssessDecommissioningImpact",
                "Next": "CheckRiskLevel"
            },
            "CheckRiskLevel": {
                "Type": "Choice",
                "Choices": [
                    {
                        "Variable": "$.risk_level",
                        "StringEquals": "low",
                        "Next": "AutoApprove"
                    },
                    {
                        "Variable": "$.risk_level",
                        "StringEquals": "medium",
                        "Next": "RequestApproval"
                    }
                ],
                "Default": "RequestHighRiskApproval"
            },
            "AutoApprove": {
                "Type": "Task",
                "Resource": "arn:aws:lambda:REGION:ACCOUNT:function:AutoApproveDecommissioning",
                "Next": "PlanDecommissioning"
            },
            "RequestApproval": {
                "Type": "Task",
                "Resource": "arn:aws:lambda:REGION:ACCOUNT:function:RequestDecommissioningApproval",
                "Next": "WaitForApproval"
            },
            "RequestHighRiskApproval": {
                "Type": "Task",
                "Resource": "arn:aws:lambda:REGION:ACCOUNT:function:RequestHighRiskApproval",
                "Next": "WaitForApproval"
            },
            "WaitForApproval": {
                "Type": "Wait",
                "Seconds": 3600,
                "Next": "CheckApprovalStatus"
            },
            "CheckApprovalStatus": {
                "Type": "Task",
                "Resource": "arn:aws:lambda:REGION:ACCOUNT:function:CheckApprovalStatus",
                "Next": "ApprovalDecision"
            },
            "ApprovalDecision": {
                "Type": "Choice",
                "Choices": [
                    {
                        "Variable": "$.approval_status",
                        "StringEquals": "approved",
                        "Next": "PlanDecommissioning"
                    },
                    {
                        "Variable": "$.approval_status",
                        "StringEquals": "rejected",
                        "Next": "ProcessRejected"
                    }
                ],
                "Default": "WaitForApproval"
            },
            "PlanDecommissioning": {
                "Type": "Task",
                "Resource": "arn:aws:lambda:REGION:ACCOUNT:function:PlanDecommissioning",
                "Next": "ExecuteDecommissioning"
            },
            "ExecuteDecommissioning": {
                "Type": "Task",
                "Resource": "arn:aws:lambda:REGION:ACCOUNT:function:ExecuteDecommissioning",
                "Retry": [
                    {
                        "ErrorEquals": ["States.TaskFailed"],
                        "IntervalSeconds": 30,
                        "MaxAttempts": 3,
                        "BackoffRate": 2.0
                    }
                ],
                "Catch": [
                    {
                        "ErrorEquals": ["States.ALL"],
                        "Next": "HandleDecommissioningFailure"
                    }
                ],
                "Next": "ValidateDecommissioning"
            },
            "ValidateDecommissioning": {
                "Type": "Task",
                "Resource": "arn:aws:lambda:REGION:ACCOUNT:function:ValidateDecommissioning",
                "Next": "ProcessCompleted"
            },
            "HandleDecommissioningFailure": {
                "Type": "Task",
                "Resource": "arn:aws:lambda:REGION:ACCOUNT:function:HandleDecommissioningFailure",
                "Next": "ProcessFailed"
            },
            "ProcessCompleted": {
                "Type": "Succeed"
            },
            "ProcessFailed": {
                "Type": "Fail",
                "Cause": "Decommissioning process failed"
            },
            "ProcessRejected": {
                "Type": "Succeed"
            }
        }
    }
    
    # Create Step Functions state machine
    stepfunctions = boto3.client('stepfunctions')
    
    try:
        response = stepfunctions.create_state_machine(
            name='ResourceDecommissioningWorkflow',
            definition=json.dumps(workflow_definition),
            roleArn='arn:aws:iam::ACCOUNT:role/StepFunctionsDecommissioningRole'
        )
        
        print(f"Created Step Functions workflow: {response['stateMachineArn']}")
        return response['stateMachineArn']
        
    except Exception as e:
        print(f"Error creating Step Functions workflow: {str(e)}")
        return None
```

## Process Documentation and Templates

### Decommissioning Checklist Template
```yaml
Decommissioning_Checklist:
  Pre_Decommissioning:
    - Verify resource identification and ownership
    - Confirm business justification for decommissioning
    - Complete impact assessment and risk analysis
    - Obtain required approvals and sign-offs
    - Schedule decommissioning window
    - Notify affected stakeholders
    
  Data_Protection:
    - Identify data retention requirements
    - Create necessary data backups
    - Verify backup integrity and accessibility
    - Document data archival locations
    - Confirm compliance with retention policies
    
  Dependency_Management:
    - Map all resource dependencies
    - Identify dependent services and applications
    - Plan for dependency migration or updates
    - Test dependency changes in non-production
    - Prepare rollback procedures
    
  Execution:
    - Follow planned decommissioning sequence
    - Monitor for errors or unexpected issues
    - Validate each step before proceeding
    - Document any deviations from plan
    - Maintain communication with stakeholders
    
  Post_Decommissioning:
    - Verify successful resource removal
    - Confirm cost savings achievement
    - Update documentation and inventory
    - Conduct lessons learned review
    - Archive process documentation
```

### Risk Assessment Matrix
```yaml
Risk_Assessment_Matrix:
  Business_Impact:
    Critical:
      - Production services with customer impact
      - Revenue-generating applications
      - Compliance-critical systems
    High:
      - Internal production systems
      - Customer-facing non-critical services
      - Business-critical development environments
    Medium:
      - Internal tools and utilities
      - Staging and testing environments
      - Non-critical support systems
    Low:
      - Development and sandbox environments
      - Unused or obsolete resources
      - Temporary or experimental systems
      
  Technical_Impact:
    Critical:
      - Resources with many critical dependencies
      - Single points of failure
      - Data stores with no backups
    High:
      - Resources with some dependencies
      - Shared infrastructure components
      - Data stores with recent backups
    Medium:
      - Resources with minimal dependencies
      - Redundant infrastructure components
      - Well-backed-up data stores
    Low:
      - Isolated resources
      - Fully redundant components
      - Temporary or disposable resources
```

## Common Challenges and Solutions

### Challenge: Stakeholder Resistance to Decommissioning

**Solution**: Involve stakeholders in the process design and decision-making. Provide clear communication about benefits and risks. Implement gradual decommissioning approaches and provide adequate notice periods.

### Challenge: Complex Approval Workflows

**Solution**: Design streamlined approval processes based on risk levels. Use automated approval for low-risk scenarios. Implement clear escalation procedures and time-bound approvals.

### Challenge: Incomplete Impact Assessment

**Solution**: Use automated tools for dependency discovery and impact analysis. Implement comprehensive assessment frameworks. Create feedback loops to improve assessment accuracy over time.

### Challenge: Process Compliance and Audit Requirements

**Solution**: Implement comprehensive audit logging and documentation. Create standardized process templates and checklists. Use automated compliance checking and reporting.

### Challenge: Rollback and Recovery Complexity

**Solution**: Design comprehensive rollback procedures and test them regularly. Implement automated rollback capabilities where possible. Maintain detailed recovery documentation and procedures.

## Related Resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/cost_decommission_resources_process.html">AWS Well-Architected Framework - Implement a decommissioning process</a></li>
    <li><a href="https://docs.aws.amazon.com/systems-manager/latest/userguide/what-is-systems-manager.html">AWS Systems Manager User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html">AWS Step Functions Developer Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/lambda/latest/dg/welcome.html">AWS Lambda Developer Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/sns/latest/dg/welcome.html">Amazon SNS Developer Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html">AWS CloudFormation User Guide</a></li>
    <li><a href="https://aws.amazon.com/blogs/aws-cost-management/">AWS Cost Management Blog</a></li>
    <li><a href="https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html">Amazon DynamoDB Developer Guide</a></li>
  </ul>
</div>

<style>
.pillar-header {
  background-color: #e8f5e8;
  border-left: 5px solid #2d7d2d;
}

.pillar-header h1 {
  color: #2d7d2d;
}

.aws-service-content h4 {
  color: #2d7d2d;
}

.related-resources {
  background-color: #e8f5e8;
}

.related-resources h2 {
  color: #2d7d2d;
}
</style>
