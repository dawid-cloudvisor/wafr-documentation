---
title: REL08-BP01 - Use runbooks for standard activities such as deployment
layout: default
parent: REL08 - How do you implement change?
grand_parent: Reliability
nav_order: 1
---

# REL08-BP01: Use runbooks for standard activities such as deployment

## Overview

Implement comprehensive runbooks that provide step-by-step procedures for standard operational activities, particularly deployments. Runbooks ensure consistency, reduce human error, enable knowledge sharing, and provide clear guidance for both routine operations and incident response scenarios.

## Implementation Steps

### 1. Design Runbook Framework and Standards
- Establish runbook templates and formatting standards
- Define runbook categories and classification systems
- Implement version control and change management for runbooks
- Design runbook discovery and search mechanisms

### 2. Create Deployment Runbooks
- Document step-by-step deployment procedures
- Include pre-deployment validation and preparation steps
- Define rollback procedures and emergency protocols
- Establish post-deployment verification and monitoring

### 3. Implement Automated Runbook Execution
- Create executable runbooks with automation integration
- Implement parameter validation and input sanitization
- Design approval workflows and authorization controls
- Establish execution logging and audit trails

### 4. Configure Runbook Management System
- Implement centralized runbook repository and management
- Configure access controls and permission management
- Design runbook scheduling and execution orchestration
- Establish runbook performance monitoring and optimization

### 5. Establish Runbook Maintenance and Updates
- Implement regular runbook review and validation processes
- Configure automated testing of runbook procedures
- Design feedback collection and improvement mechanisms
- Establish runbook retirement and archival procedures

### 6. Monitor Runbook Usage and Effectiveness
- Track runbook execution success rates and performance
- Monitor user adoption and feedback
- Implement continuous improvement based on usage analytics
- Establish runbook quality metrics and KPIs

## Implementation Examples

### Example 1: Comprehensive Runbook Management System
```python
import boto3
import json
import logging
import asyncio
import yaml
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import subprocess
import tempfile
import os

class RunbookType(Enum):
    DEPLOYMENT = "deployment"
    MAINTENANCE = "maintenance"
    INCIDENT_RESPONSE = "incident_response"
    BACKUP_RESTORE = "backup_restore"
    SCALING = "scaling"
    MONITORING = "monitoring"

class RunbookStatus(Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"

class ExecutionStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class RunbookStep:
    step_id: str
    name: str
    description: str
    command: Optional[str]
    parameters: Dict[str, Any]
    validation: Optional[Dict[str, Any]]
    rollback_command: Optional[str]
    timeout_seconds: int
    retry_count: int
    required: bool

@dataclass
class Runbook:
    runbook_id: str
    name: str
    description: str
    runbook_type: RunbookType
    version: str
    status: RunbookStatus
    steps: List[RunbookStep]
    prerequisites: List[str]
    parameters: Dict[str, Any]
    tags: List[str]
    created_by: str
    created_at: datetime
    updated_at: datetime

@dataclass
class RunbookExecution:
    execution_id: str
    runbook_id: str
    runbook_version: str
    status: ExecutionStatus
    started_by: str
    started_at: datetime
    completed_at: Optional[datetime]
    parameters: Dict[str, Any]
    step_results: List[Dict[str, Any]]
    error_message: Optional[str]
    rollback_performed: bool

class RunbookManager:
    """Comprehensive runbook management system"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
        # AWS clients
        self.s3 = boto3.client('s3')
        self.ssm = boto3.client('ssm')
        self.lambda_client = boto3.client('lambda')
        self.dynamodb = boto3.resource('dynamodb')
        self.sns = boto3.client('sns')
        
        # Storage
        self.runbooks_table = self.dynamodb.Table(config.get('runbooks_table', 'runbooks'))
        self.executions_table = self.dynamodb.Table(config.get('executions_table', 'runbook-executions'))
        
        # Configuration
        self.runbook_bucket = config.get('runbook_bucket', 'runbook-storage')
        self.execution_timeout = config.get('execution_timeout', 3600)  # 1 hour
        
        # Active executions
        self.active_executions = {}
        
    async def create_runbook(self, runbook_data: Dict[str, Any]) -> str:
        """Create a new runbook"""
        try:
            runbook_id = f"rb_{int(datetime.utcnow().timestamp())}_{runbook_data['name'].replace(' ', '_').lower()}"
            
            # Create runbook steps
            steps = []
            for step_data in runbook_data.get('steps', []):
                step = RunbookStep(
                    step_id=step_data['step_id'],
                    name=step_data['name'],
                    description=step_data['description'],
                    command=step_data.get('command'),
                    parameters=step_data.get('parameters', {}),
                    validation=step_data.get('validation'),
                    rollback_command=step_data.get('rollback_command'),
                    timeout_seconds=step_data.get('timeout_seconds', 300),
                    retry_count=step_data.get('retry_count', 0),
                    required=step_data.get('required', True)
                )
                steps.append(step)
            
            # Create runbook
            runbook = Runbook(
                runbook_id=runbook_id,
                name=runbook_data['name'],
                description=runbook_data['description'],
                runbook_type=RunbookType(runbook_data['runbook_type']),
                version=runbook_data.get('version', '1.0.0'),
                status=RunbookStatus.DRAFT,
                steps=steps,
                prerequisites=runbook_data.get('prerequisites', []),
                parameters=runbook_data.get('parameters', {}),
                tags=runbook_data.get('tags', []),
                created_by=runbook_data['created_by'],
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            # Store runbook
            await self._store_runbook(runbook)
            
            # Store runbook content in S3
            await self._store_runbook_content(runbook)
            
            logging.info(f"Created runbook: {runbook_id}")
            return runbook_id
            
        except Exception as e:
            logging.error(f"Failed to create runbook: {str(e)}")
            raise
    
    async def execute_runbook(self, runbook_id: str, parameters: Dict[str, Any], 
                            executed_by: str) -> str:
        """Execute a runbook"""
        try:
            # Get runbook
            runbook = await self._get_runbook(runbook_id)
            if not runbook:
                raise ValueError(f"Runbook {runbook_id} not found")
            
            if runbook.status != RunbookStatus.ACTIVE:
                raise ValueError(f"Runbook {runbook_id} is not active")
            
            # Create execution record
            execution_id = f"exec_{int(datetime.utcnow().timestamp())}_{runbook_id}"
            
            execution = RunbookExecution(
                execution_id=execution_id,
                runbook_id=runbook_id,
                runbook_version=runbook.version,
                status=ExecutionStatus.PENDING,
                started_by=executed_by,
                started_at=datetime.utcnow(),
                completed_at=None,
                parameters=parameters,
                step_results=[],
                error_message=None,
                rollback_performed=False
            )
            
            # Store execution record
            await self._store_execution(execution)
            
            # Start execution
            self.active_executions[execution_id] = execution
            asyncio.create_task(self._execute_runbook_steps(runbook, execution))
            
            logging.info(f"Started runbook execution: {execution_id}")
            return execution_id
            
        except Exception as e:
            logging.error(f"Failed to execute runbook: {str(e)}")
            raise
    
    async def _execute_runbook_steps(self, runbook: Runbook, execution: RunbookExecution):
        """Execute runbook steps"""
        try:
            execution.status = ExecutionStatus.RUNNING
            await self._store_execution(execution)
            
            for step in runbook.steps:
                try:
                    logging.info(f"Executing step: {step.name}")
                    
                    # Execute step
                    step_result = await self._execute_step(step, execution.parameters)
                    
                    # Record step result
                    execution.step_results.append({
                        'step_id': step.step_id,
                        'name': step.name,
                        'status': 'success',
                        'output': step_result.get('output', ''),
                        'duration': step_result.get('duration', 0),
                        'timestamp': datetime.utcnow().isoformat()
                    })
                    
                    # Validate step result if validation is defined
                    if step.validation:
                        validation_result = await self._validate_step_result(step, step_result)
                        if not validation_result:
                            raise Exception(f"Step validation failed: {step.name}")
                    
                except Exception as step_error:
                    logging.error(f"Step {step.name} failed: {str(step_error)}")
                    
                    # Record step failure
                    execution.step_results.append({
                        'step_id': step.step_id,
                        'name': step.name,
                        'status': 'failed',
                        'error': str(step_error),
                        'timestamp': datetime.utcnow().isoformat()
                    })
                    
                    # Check if step is required
                    if step.required:
                        # Perform rollback
                        await self._perform_rollback(runbook, execution)
                        execution.status = ExecutionStatus.FAILED
                        execution.error_message = str(step_error)
                        execution.rollback_performed = True
                        break
            
            # Complete execution if no failures
            if execution.status == ExecutionStatus.RUNNING:
                execution.status = ExecutionStatus.SUCCESS
            
            execution.completed_at = datetime.utcnow()
            await self._store_execution(execution)
            
            # Remove from active executions
            if execution.execution_id in self.active_executions:
                del self.active_executions[execution.execution_id]
            
            # Send notification
            await self._send_execution_notification(execution)
            
        except Exception as e:
            logging.error(f"Runbook execution failed: {str(e)}")
            execution.status = ExecutionStatus.FAILED
            execution.error_message = str(e)
            execution.completed_at = datetime.utcnow()
            await self._store_execution(execution)
    
    async def _execute_step(self, step: RunbookStep, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single runbook step"""
        try:
            start_time = datetime.utcnow()
            
            if step.command:
                # Execute command
                result = await self._execute_command(step.command, step.parameters, parameters)
            else:
                # Manual step or custom logic
                result = await self._execute_custom_step(step, parameters)
            
            end_time = datetime.utcnow()
            duration = (end_time - start_time).total_seconds()
            
            return {
                'output': result,
                'duration': duration,
                'success': True
            }
            
        except Exception as e:
            logging.error(f"Step execution failed: {str(e)}")
            raise
    
    async def _execute_command(self, command: str, step_params: Dict[str, Any], 
                             execution_params: Dict[str, Any]) -> str:
        """Execute a command with parameter substitution"""
        try:
            # Merge parameters
            all_params = {**step_params, **execution_params}
            
            # Substitute parameters in command
            formatted_command = command.format(**all_params)
            
            # Execute command
            if command.startswith('aws:ssm:'):
                # Execute SSM document
                document_name = formatted_command.replace('aws:ssm:', '')
                return await self._execute_ssm_document(document_name, all_params)
            elif command.startswith('aws:lambda:'):
                # Execute Lambda function
                function_name = formatted_command.replace('aws:lambda:', '')
                return await self._execute_lambda_function(function_name, all_params)
            else:
                # Execute shell command
                return await self._execute_shell_command(formatted_command)
                
        except Exception as e:
            logging.error(f"Command execution failed: {str(e)}")
            raise
    
    async def _execute_ssm_document(self, document_name: str, parameters: Dict[str, Any]) -> str:
        """Execute SSM document"""
        try:
            response = self.ssm.send_command(
                DocumentName=document_name,
                Parameters=parameters,
                MaxConcurrency='1',
                MaxErrors='0'
            )
            
            command_id = response['Command']['CommandId']
            
            # Wait for command completion
            while True:
                status_response = self.ssm.get_command_invocation(
                    CommandId=command_id,
                    InstanceId=parameters.get('InstanceId', 'localhost')
                )
                
                status = status_response['Status']
                if status in ['Success', 'Failed', 'Cancelled', 'TimedOut']:
                    break
                
                await asyncio.sleep(5)
            
            if status == 'Success':
                return status_response.get('StandardOutputContent', '')
            else:
                raise Exception(f"SSM command failed: {status_response.get('StandardErrorContent', '')}")
                
        except Exception as e:
            logging.error(f"SSM document execution failed: {str(e)}")
            raise
    
    async def _execute_lambda_function(self, function_name: str, parameters: Dict[str, Any]) -> str:
        """Execute Lambda function"""
        try:
            response = self.lambda_client.invoke(
                FunctionName=function_name,
                InvocationType='RequestResponse',
                Payload=json.dumps(parameters)
            )
            
            if response['StatusCode'] == 200:
                result = json.loads(response['Payload'].read())
                return json.dumps(result)
            else:
                raise Exception(f"Lambda function failed with status: {response['StatusCode']}")
                
        except Exception as e:
            logging.error(f"Lambda function execution failed: {str(e)}")
            raise
    
    async def _execute_shell_command(self, command: str) -> str:
        """Execute shell command"""
        try:
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                return stdout.decode()
            else:
                raise Exception(f"Command failed: {stderr.decode()}")
                
        except Exception as e:
            logging.error(f"Shell command execution failed: {str(e)}")
            raise
    
    async def _validate_step_result(self, step: RunbookStep, result: Dict[str, Any]) -> bool:
        """Validate step execution result"""
        try:
            validation = step.validation
            if not validation:
                return True
            
            validation_type = validation.get('type')
            
            if validation_type == 'output_contains':
                expected_text = validation.get('expected_text')
                return expected_text in result.get('output', '')
            elif validation_type == 'exit_code':
                expected_code = validation.get('expected_code', 0)
                return result.get('exit_code', 0) == expected_code
            elif validation_type == 'custom':
                # Execute custom validation function
                validation_function = validation.get('function')
                return await self._execute_custom_validation(validation_function, result)
            
            return True
            
        except Exception as e:
            logging.error(f"Step validation failed: {str(e)}")
            return False
    
    async def _perform_rollback(self, runbook: Runbook, execution: RunbookExecution):
        """Perform rollback of executed steps"""
        try:
            logging.info(f"Performing rollback for execution: {execution.execution_id}")
            
            # Execute rollback commands in reverse order
            successful_steps = [r for r in execution.step_results if r['status'] == 'success']
            
            for step_result in reversed(successful_steps):
                step_id = step_result['step_id']
                step = next((s for s in runbook.steps if s.step_id == step_id), None)
                
                if step and step.rollback_command:
                    try:
                        logging.info(f"Rolling back step: {step.name}")
                        await self._execute_command(
                            step.rollback_command, 
                            step.parameters, 
                            execution.parameters
                        )
                    except Exception as rollback_error:
                        logging.error(f"Rollback failed for step {step.name}: {str(rollback_error)}")
            
        except Exception as e:
            logging.error(f"Rollback failed: {str(e)}")
    
    async def _store_runbook(self, runbook: Runbook):
        """Store runbook in DynamoDB"""
        try:
            runbook_dict = asdict(runbook)
            runbook_dict['created_at'] = runbook.created_at.isoformat()
            runbook_dict['updated_at'] = runbook.updated_at.isoformat()
            
            # Convert steps to dict format
            runbook_dict['steps'] = [asdict(step) for step in runbook.steps]
            
            self.runbooks_table.put_item(Item=runbook_dict)
            
        except Exception as e:
            logging.error(f"Failed to store runbook: {str(e)}")
            raise
    
    async def _store_runbook_content(self, runbook: Runbook):
        """Store runbook content in S3"""
        try:
            # Create YAML representation
            runbook_content = {
                'metadata': {
                    'name': runbook.name,
                    'description': runbook.description,
                    'version': runbook.version,
                    'type': runbook.runbook_type.value
                },
                'parameters': runbook.parameters,
                'prerequisites': runbook.prerequisites,
                'steps': [asdict(step) for step in runbook.steps]
            }
            
            yaml_content = yaml.dump(runbook_content, default_flow_style=False)
            
            # Store in S3
            self.s3.put_object(
                Bucket=self.runbook_bucket,
                Key=f"runbooks/{runbook.runbook_id}/{runbook.version}/runbook.yaml",
                Body=yaml_content,
                ContentType='application/x-yaml'
            )
            
        except Exception as e:
            logging.error(f"Failed to store runbook content: {str(e)}")
    
    async def _get_runbook(self, runbook_id: str) -> Optional[Runbook]:
        """Get runbook from storage"""
        try:
            response = self.runbooks_table.get_item(Key={'runbook_id': runbook_id})
            
            if 'Item' in response:
                item = response['Item']
                
                # Convert datetime strings back to datetime objects
                item['created_at'] = datetime.fromisoformat(item['created_at'])
                item['updated_at'] = datetime.fromisoformat(item['updated_at'])
                
                # Convert steps back to RunbookStep objects
                steps = []
                for step_data in item['steps']:
                    step = RunbookStep(**step_data)
                    steps.append(step)
                item['steps'] = steps
                
                return Runbook(**item)
            
            return None
            
        except Exception as e:
            logging.error(f"Failed to get runbook: {str(e)}")
            return None
    
    async def _store_execution(self, execution: RunbookExecution):
        """Store execution record in DynamoDB"""
        try:
            execution_dict = asdict(execution)
            execution_dict['started_at'] = execution.started_at.isoformat()
            if execution.completed_at:
                execution_dict['completed_at'] = execution.completed_at.isoformat()
            
            self.executions_table.put_item(Item=execution_dict)
            
        except Exception as e:
            logging.error(f"Failed to store execution: {str(e)}")
    
    async def _send_execution_notification(self, execution: RunbookExecution):
        """Send execution completion notification"""
        try:
            topic_arn = self.config.get('notification_topic_arn')
            if not topic_arn:
                return
            
            message = {
                'execution_id': execution.execution_id,
                'runbook_id': execution.runbook_id,
                'status': execution.status.value,
                'started_by': execution.started_by,
                'duration': str(execution.completed_at - execution.started_at) if execution.completed_at else None,
                'error_message': execution.error_message
            }
            
            self.sns.publish(
                TopicArn=topic_arn,
                Message=json.dumps(message, indent=2),
                Subject=f"Runbook Execution {execution.status.value.title()}: {execution.runbook_id}"
            )
            
        except Exception as e:
            logging.error(f"Failed to send notification: {str(e)}")

# Usage example
async def main():
    config = {
        'runbooks_table': 'runbooks',
        'executions_table': 'runbook-executions',
        'runbook_bucket': 'my-runbook-storage',
        'notification_topic_arn': 'arn:aws:sns:us-east-1:123456789012:runbook-notifications'
    }
    
    # Initialize runbook manager
    runbook_manager = RunbookManager(config)
    
    # Create deployment runbook
    deployment_runbook = {
        'name': 'Web Application Deployment',
        'description': 'Standard deployment procedure for web application',
        'runbook_type': 'deployment',
        'version': '1.0.0',
        'created_by': 'devops@company.com',
        'prerequisites': [
            'Application build completed successfully',
            'All tests passed',
            'Deployment approval obtained'
        ],
        'parameters': {
            'application_name': {'type': 'string', 'required': True},
            'version': {'type': 'string', 'required': True},
            'environment': {'type': 'string', 'required': True, 'allowed_values': ['staging', 'production']}
        },
        'steps': [
            {
                'step_id': 'pre_deployment_check',
                'name': 'Pre-deployment Health Check',
                'description': 'Verify system health before deployment',
                'command': 'aws:lambda:health-check-function',
                'parameters': {'environment': '{environment}'},
                'timeout_seconds': 300,
                'retry_count': 2,
                'required': True
            },
            {
                'step_id': 'backup_current_version',
                'name': 'Backup Current Version',
                'description': 'Create backup of current application version',
                'command': 'aws:ssm:backup-application',
                'parameters': {'app_name': '{application_name}', 'env': '{environment}'},
                'rollback_command': 'aws:ssm:restore-application',
                'timeout_seconds': 600,
                'required': True
            },
            {
                'step_id': 'deploy_application',
                'name': 'Deploy Application',
                'description': 'Deploy new application version',
                'command': 'aws codedeploy create-deployment --application-name {application_name} --deployment-group-name {environment}',
                'parameters': {'version': '{version}'},
                'validation': {
                    'type': 'output_contains',
                    'expected_text': 'deployment created successfully'
                },
                'timeout_seconds': 1800,
                'required': True
            },
            {
                'step_id': 'post_deployment_verification',
                'name': 'Post-deployment Verification',
                'description': 'Verify deployment success and application health',
                'command': 'aws:lambda:post-deployment-check',
                'parameters': {'app_name': '{application_name}', 'version': '{version}'},
                'timeout_seconds': 300,
                'required': True
            }
        ],
        'tags': ['deployment', 'web-application', 'production']
    }
    
    # Create runbook
    runbook_id = await runbook_manager.create_runbook(deployment_runbook)
    print(f"Created runbook: {runbook_id}")
    
    # Execute runbook
    execution_params = {
        'application_name': 'my-web-app',
        'version': '2.1.0',
        'environment': 'staging'
    }
    
    execution_id = await runbook_manager.execute_runbook(
        runbook_id, 
        execution_params, 
        'devops@company.com'
    )
    
    print(f"Started execution: {execution_id}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## AWS Services Used

- **AWS Systems Manager**: Document execution, parameter management, and automation
- **AWS Lambda**: Custom step execution and validation functions
- **Amazon S3**: Runbook content storage and version management
- **Amazon DynamoDB**: Runbook metadata and execution history storage
- **Amazon SNS**: Execution notifications and alerting
- **AWS CodeDeploy**: Application deployment automation
- **AWS CodePipeline**: Integration with CI/CD pipelines
- **AWS CloudFormation**: Infrastructure deployment runbooks
- **Amazon EventBridge**: Event-driven runbook execution
- **AWS Step Functions**: Complex workflow orchestration
- **AWS Config**: Configuration compliance and change tracking
- **Amazon CloudWatch**: Execution monitoring and logging
- **AWS Secrets Manager**: Secure parameter and credential management
- **AWS IAM**: Access control and permission management
- **Amazon EC2**: Instance management and deployment targets

## Benefits

- **Consistency**: Standardized procedures ensure consistent execution across teams
- **Error Reduction**: Step-by-step guidance reduces human errors and omissions
- **Knowledge Sharing**: Documented procedures enable knowledge transfer and training
- **Automation Integration**: Executable runbooks enable automated operations
- **Audit Trail**: Complete execution history for compliance and troubleshooting
- **Rollback Capability**: Automated rollback procedures for quick recovery
- **Scalability**: Centralized management supports large-scale operations
- **Continuous Improvement**: Feedback and analytics drive procedure optimization
- **Compliance**: Documented procedures support regulatory requirements
- **Incident Response**: Rapid response through pre-defined procedures

## Related Resources

- [AWS Well-Architected Reliability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/)
- [Use Runbooks for Standard Activities](https://docs.aws.amazon.com/wellarchitected/latest/framework/rel_implement_change_runbook_standard_activities.html)
- [AWS Systems Manager User Guide](https://docs.aws.amazon.com/systems-manager/latest/userguide/)
- [AWS Lambda Developer Guide](https://docs.aws.amazon.com/lambda/latest/dg/)
- [Amazon S3 User Guide](https://docs.aws.amazon.com/s3/latest/userguide/)
- [Amazon DynamoDB Developer Guide](https://docs.aws.amazon.com/dynamodb/latest/developerguide/)
- [AWS CodeDeploy User Guide](https://docs.aws.amazon.com/codedeploy/latest/userguide/)
- [AWS Step Functions Developer Guide](https://docs.aws.amazon.com/step-functions/latest/dg/)
- [AWS Builders' Library - Runbooks](https://aws.amazon.com/builders-library/)
- [DevOps Best Practices](https://aws.amazon.com/devops/)
- [Operational Excellence Pillar](https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/)
- [Infrastructure as Code Best Practices](https://docs.aws.amazon.com/whitepapers/latest/introduction-devops-aws/infrastructure-as-code.html)
