---
title: REL08-BP05 - Deploy changes with automation
layout: default
parent: REL08 - How do you implement change?
grand_parent: Reliability
nav_order: 5
---

# REL08-BP05: Deploy changes with automation

## Overview

Implement comprehensive deployment automation to eliminate manual processes, reduce human error, and ensure consistent, repeatable deployments. Automated deployment pipelines provide faster feedback, improved reliability, and enable continuous delivery practices that support rapid innovation while maintaining system stability.

## Implementation Steps

### 1. Design Automated Deployment Pipeline
- Implement CI/CD pipeline architecture and workflow design
- Configure source control integration and branch strategies
- Design build automation and artifact management
- Establish deployment stage gates and approval processes

### 2. Configure Build and Test Automation
- Implement automated build processes and dependency management
- Configure comprehensive test suite execution
- Design code quality checks and security scanning
- Establish artifact versioning and promotion strategies

### 3. Implement Deployment Orchestration
- Configure multi-environment deployment automation
- Implement deployment strategies and rollout patterns
- Design infrastructure provisioning and configuration management
- Establish service dependency management and coordination

### 4. Configure Monitoring and Validation
- Implement automated deployment health checks
- Configure performance monitoring and validation
- Design automated rollback triggers and procedures
- Establish deployment success criteria and metrics

### 5. Establish Security and Compliance Automation
- Implement automated security scanning and validation
- Configure compliance checks and policy enforcement
- Design secret management and credential automation
- Establish audit logging and change tracking

### 6. Monitor and Optimize Pipeline Performance
- Track deployment frequency and lead times
- Monitor pipeline success rates and failure analysis
- Implement continuous improvement and optimization
- Establish deployment metrics and performance benchmarks

## Implementation Examples

### Example 1: Comprehensive Automated Deployment System
{% raw %}
```python
import boto3
import json
import logging
import asyncio
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import yaml
import subprocess

class PipelineStage(Enum):
    SOURCE = "source"
    BUILD = "build"
    TEST = "test"
    SECURITY_SCAN = "security_scan"
    DEPLOY_STAGING = "deploy_staging"
    INTEGRATION_TEST = "integration_test"
    DEPLOY_PRODUCTION = "deploy_production"
    POST_DEPLOY_VALIDATION = "post_deploy_validation"

class PipelineStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class PipelineExecution:
    execution_id: str
    pipeline_name: str
    source_version: str
    triggered_by: str
    started_at: datetime
    completed_at: Optional[datetime]
    status: PipelineStatus
    current_stage: Optional[PipelineStage]
    stage_results: Dict[str, Any]
    artifacts: Dict[str, str]
    error_message: Optional[str]

@dataclass
class DeploymentStage:
    stage_name: str
    stage_type: PipelineStage
    actions: List[Dict[str, Any]]
    input_artifacts: List[str]
    output_artifacts: List[str]
    timeout_minutes: int
    retry_count: int
    rollback_on_failure: bool

class AutomatedDeploymentPipeline:
    """Comprehensive automated deployment pipeline system"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
        # AWS clients
        self.codepipeline = boto3.client('codepipeline')
        self.codebuild = boto3.client('codebuild')
        self.codecommit = boto3.client('codecommit')
        self.codedeploy = boto3.client('codedeploy')
        self.s3 = boto3.client('s3')
        self.lambda_client = boto3.client('lambda')
        self.cloudformation = boto3.client('cloudformation')
        self.dynamodb = boto3.resource('dynamodb')
        self.sns = boto3.client('sns')
        self.cloudwatch = boto3.client('cloudwatch')
        
        # Storage
        self.executions_table = self.dynamodb.Table(config.get('executions_table', 'pipeline-executions'))
        self.pipelines_table = self.dynamodb.Table(config.get('pipelines_table', 'deployment-pipelines'))
        
        # Configuration
        self.artifact_bucket = config.get('artifact_bucket', 'deployment-artifacts')
        self.notification_topic = config.get('notification_topic_arn')
        
        # Active executions
        self.active_executions = {}
        
    async def create_deployment_pipeline(self, pipeline_config: Dict[str, Any]) -> str:
        """Create automated deployment pipeline"""
        try:
            pipeline_name = pipeline_config['pipeline_name']
            
            # Create CodePipeline
            pipeline_definition = self._build_pipeline_definition(pipeline_config)
            
            self.codepipeline.create_pipeline(pipeline=pipeline_definition)
            
            # Create supporting resources
            await self._create_build_projects(pipeline_config)
            await self._create_deployment_applications(pipeline_config)
            
            # Store pipeline configuration
            await self._store_pipeline_config(pipeline_config)
            
            logging.info(f"Created deployment pipeline: {pipeline_name}")
            return pipeline_name
            
        except Exception as e:
            logging.error(f"Failed to create deployment pipeline: {str(e)}")
            raise
    
    def _build_pipeline_definition(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Build CodePipeline definition"""
        pipeline_name = config['pipeline_name']
        
        return {
            'name': pipeline_name,
            'roleArn': config['service_role_arn'],
            'artifactStore': {
                'type': 'S3',
                'location': self.artifact_bucket
            },
            'stages': [
                {
                    'name': 'Source',
                    'actions': [
                        {
                            'name': 'SourceAction',
                            'actionTypeId': {
                                'category': 'Source',
                                'owner': 'AWS',
                                'provider': 'CodeCommit',
                                'version': '1'
                            },
                            'configuration': {
                                'RepositoryName': config['repository_name'],
                                'BranchName': config.get('branch_name', 'main')
                            },
                            'outputArtifacts': [{'name': 'SourceOutput'}]
                        }
                    ]
                },
                {
                    'name': 'Build',
                    'actions': [
                        {
                            'name': 'BuildAction',
                            'actionTypeId': {
                                'category': 'Build',
                                'owner': 'AWS',
                                'provider': 'CodeBuild',
                                'version': '1'
                            },
                            'configuration': {
                                'ProjectName': f"{pipeline_name}-build"
                            },
                            'inputArtifacts': [{'name': 'SourceOutput'}],
                            'outputArtifacts': [{'name': 'BuildOutput'}]
                        }
                    ]
                },
                {
                    'name': 'Test',
                    'actions': [
                        {
                            'name': 'TestAction',
                            'actionTypeId': {
                                'category': 'Build',
                                'owner': 'AWS',
                                'provider': 'CodeBuild',
                                'version': '1'
                            },
                            'configuration': {
                                'ProjectName': f"{pipeline_name}-test"
                            },
                            'inputArtifacts': [{'name': 'BuildOutput'}],
                            'outputArtifacts': [{'name': 'TestOutput'}]
                        }
                    ]
                },
                {
                    'name': 'DeployStaging',
                    'actions': [
                        {
                            'name': 'DeployToStaging',
                            'actionTypeId': {
                                'category': 'Deploy',
                                'owner': 'AWS',
                                'provider': 'CodeDeploy',
                                'version': '1'
                            },
                            'configuration': {
                                'ApplicationName': f"{pipeline_name}-app",
                                'DeploymentGroupName': 'staging'
                            },
                            'inputArtifacts': [{'name': 'BuildOutput'}]
                        }
                    ]
                },
                {
                    'name': 'IntegrationTest',
                    'actions': [
                        {
                            'name': 'IntegrationTestAction',
                            'actionTypeId': {
                                'category': 'Invoke',
                                'owner': 'AWS',
                                'provider': 'Lambda',
                                'version': '1'
                            },
                            'configuration': {
                                'FunctionName': f"{pipeline_name}-integration-tests"
                            }
                        }
                    ]
                },
                {
                    'name': 'ProductionApproval',
                    'actions': [
                        {
                            'name': 'ManualApproval',
                            'actionTypeId': {
                                'category': 'Approval',
                                'owner': 'AWS',
                                'provider': 'Manual',
                                'version': '1'
                            },
                            'configuration': {
                                'NotificationArn': self.notification_topic,
                                'CustomData': 'Please review staging deployment and approve production deployment'
                            }
                        }
                    ]
                },
                {
                    'name': 'DeployProduction',
                    'actions': [
                        {
                            'name': 'DeployToProduction',
                            'actionTypeId': {
                                'category': 'Deploy',
                                'owner': 'AWS',
                                'provider': 'CodeDeploy',
                                'version': '1'
                            },
                            'configuration': {
                                'ApplicationName': f"{pipeline_name}-app",
                                'DeploymentGroupName': 'production'
                            },
                            'inputArtifacts': [{'name': 'BuildOutput'}]
                        }
                    ]
                }
            ]
        }
    
    async def _create_build_projects(self, config: Dict[str, Any]):
        """Create CodeBuild projects for pipeline"""
        try:
            pipeline_name = config['pipeline_name']
            
            # Build project
            build_project = {
                'name': f"{pipeline_name}-build",
                'description': f'Build project for {pipeline_name}',
                'source': {
                    'type': 'CODEPIPELINE',
                    'buildspec': self._generate_build_spec(config)
                },
                'artifacts': {
                    'type': 'CODEPIPELINE'
                },
                'environment': {
                    'type': 'LINUX_CONTAINER',
                    'image': 'aws/codebuild/standard:5.0',
                    'computeType': 'BUILD_GENERAL1_MEDIUM',
                    'privilegedMode': True
                },
                'serviceRole': config['build_service_role_arn']
            }
            
            self.codebuild.create_project(**build_project)
            
            # Test project
            test_project = {
                'name': f"{pipeline_name}-test",
                'description': f'Test project for {pipeline_name}',
                'source': {
                    'type': 'CODEPIPELINE',
                    'buildspec': self._generate_test_spec(config)
                },
                'artifacts': {
                    'type': 'CODEPIPELINE'
                },
                'environment': {
                    'type': 'LINUX_CONTAINER',
                    'image': 'aws/codebuild/standard:5.0',
                    'computeType': 'BUILD_GENERAL1_MEDIUM'
                },
                'serviceRole': config['build_service_role_arn']
            }
            
            self.codebuild.create_project(**test_project)
            
            logging.info(f"Created build projects for pipeline: {pipeline_name}")
            
        except Exception as e:
            logging.error(f"Failed to create build projects: {str(e)}")
            raise
    
    def _generate_build_spec(self, config: Dict[str, Any]) -> str:
        """Generate buildspec for build phase"""
        buildspec = {
            'version': '0.2',
            'phases': {
                'pre_build': {
                    'commands': [
                        'echo Logging in to Amazon ECR...',
                        'aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com'
                    ]
                },
                'build': {
                    'commands': [
                        'echo Build started on `date`',
                        'echo Building the Docker image...',
                        f'docker build -t {config["application_name"]} .',
                        f'docker tag {config["application_name"]}:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/{config["application_name"]}:$CODEBUILD_RESOLVED_SOURCE_VERSION'
                    ]
                },
                'post_build': {
                    'commands': [
                        'echo Build completed on `date`',
                        'echo Pushing the Docker image...',
                        f'docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/{config["application_name"]}:$CODEBUILD_RESOLVED_SOURCE_VERSION',
                        'echo Writing image definitions file...',
                        f'printf \'[{{"name":"{config["application_name"]}","imageUri":"%s"}}]\' $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/{config["application_name"]}:$CODEBUILD_RESOLVED_SOURCE_VERSION > imagedefinitions.json'
                    ]
                }
            },
            'artifacts': {
                'files': [
                    'imagedefinitions.json',
                    'appspec.yml',
                    'scripts/**/*'
                ]
            }
        }
        
        return yaml.dump(buildspec)
    
    def _generate_test_spec(self, config: Dict[str, Any]) -> str:
        """Generate buildspec for test phase"""
        buildspec = {
            'version': '0.2',
            'phases': {
                'install': {
                    'runtime-versions': {
                        'python': '3.8'
                    },
                    'commands': [
                        'pip install -r requirements-test.txt'
                    ]
                },
                'pre_build': {
                    'commands': [
                        'echo Starting unit tests...'
                    ]
                },
                'build': {
                    'commands': [
                        'python -m pytest tests/unit/ --junitxml=unit-test-results.xml',
                        'python -m pytest tests/integration/ --junitxml=integration-test-results.xml',
                        'echo Running security scan...',
                        'bandit -r . -f json -o security-scan-results.json || true',
                        'echo Running code quality checks...',
                        'pylint src/ --output-format=json > code-quality-results.json || true'
                    ]
                },
                'post_build': {
                    'commands': [
                        'echo Test phase completed on `date`'
                    ]
                }
            },
            'reports': {
                'unit-tests': {
                    'files': ['unit-test-results.xml'],
                    'file-format': 'JUNITXML'
                },
                'integration-tests': {
                    'files': ['integration-test-results.xml'],
                    'file-format': 'JUNITXML'
                }
            },
            'artifacts': {
                'files': [
                    'security-scan-results.json',
                    'code-quality-results.json'
                ]
            }
        }
        
        return yaml.dump(buildspec)
    
    async def execute_pipeline(self, pipeline_name: str, triggered_by: str = 'manual') -> str:
        """Execute deployment pipeline"""
        try:
            # Start pipeline execution
            response = self.codepipeline.start_pipeline_execution(name=pipeline_name)
            execution_id = response['pipelineExecutionId']
            
            # Create execution record
            execution = PipelineExecution(
                execution_id=execution_id,
                pipeline_name=pipeline_name,
                source_version='',  # Will be updated when source stage completes
                triggered_by=triggered_by,
                started_at=datetime.utcnow(),
                completed_at=None,
                status=PipelineStatus.RUNNING,
                current_stage=PipelineStage.SOURCE,
                stage_results={},
                artifacts={},
                error_message=None
            )
            
            # Store execution
            await self._store_execution(execution)
            
            # Start monitoring
            self.active_executions[execution_id] = execution
            asyncio.create_task(self._monitor_pipeline_execution(execution))
            
            logging.info(f"Started pipeline execution: {execution_id}")
            return execution_id
            
        except Exception as e:
            logging.error(f"Failed to execute pipeline: {str(e)}")
            raise
    
    async def _monitor_pipeline_execution(self, execution: PipelineExecution):
        """Monitor pipeline execution progress"""
        try:
            while execution.status == PipelineStatus.RUNNING:
                # Get pipeline execution status
                response = self.codepipeline.get_pipeline_execution(
                    pipelineName=execution.pipeline_name,
                    pipelineExecutionId=execution.execution_id
                )
                
                pipeline_execution = response['pipelineExecution']
                execution.status = PipelineStatus(pipeline_execution['status'].lower())
                
                # Get stage executions
                stage_response = self.codepipeline.list_stage_executions(
                    pipelineName=execution.pipeline_name,
                    pipelineExecutionId=execution.execution_id
                )
                
                # Update stage results
                for stage_execution in stage_response['stageExecutions']:
                    stage_name = stage_execution['stageName']
                    stage_status = stage_execution['status']
                    
                    execution.stage_results[stage_name] = {
                        'status': stage_status,
                        'start_time': stage_execution.get('startTime', '').isoformat() if stage_execution.get('startTime') else None,
                        'end_time': stage_execution.get('endTime', '').isoformat() if stage_execution.get('endTime') else None
                    }
                    
                    # Update current stage
                    if stage_status == 'InProgress':
                        execution.current_stage = self._map_stage_name_to_enum(stage_name)
                
                # Store updated execution
                await self._store_execution(execution)
                
                # Check if execution is complete
                if execution.status in [PipelineStatus.SUCCEEDED, PipelineStatus.FAILED, PipelineStatus.CANCELLED]:
                    execution.completed_at = datetime.utcnow()
                    
                    # Send notification
                    await self._send_pipeline_notification(execution)
                    
                    # Perform post-execution actions
                    if execution.status == PipelineStatus.SUCCEEDED:
                        await self._handle_successful_deployment(execution)
                    elif execution.status == PipelineStatus.FAILED:
                        await self._handle_failed_deployment(execution)
                    
                    break
                
                # Wait before next check
                await asyncio.sleep(30)
            
        except Exception as e:
            logging.error(f"Pipeline monitoring failed: {str(e)}")
            execution.status = PipelineStatus.FAILED
            execution.error_message = str(e)
            execution.completed_at = datetime.utcnow()
        
        finally:
            # Store final execution state
            await self._store_execution(execution)
            
            # Remove from active executions
            if execution.execution_id in self.active_executions:
                del self.active_executions[execution.execution_id]
    
    def _map_stage_name_to_enum(self, stage_name: str) -> Optional[PipelineStage]:
        """Map stage name to enum"""
        stage_mapping = {
            'Source': PipelineStage.SOURCE,
            'Build': PipelineStage.BUILD,
            'Test': PipelineStage.TEST,
            'DeployStaging': PipelineStage.DEPLOY_STAGING,
            'IntegrationTest': PipelineStage.INTEGRATION_TEST,
            'DeployProduction': PipelineStage.DEPLOY_PRODUCTION
        }
        
        return stage_mapping.get(stage_name)
    
    async def _handle_successful_deployment(self, execution: PipelineExecution):
        """Handle successful deployment"""
        try:
            # Send success metrics
            self.cloudwatch.put_metric_data(
                Namespace='DeploymentPipeline',
                MetricData=[
                    {
                        'MetricName': 'DeploymentSuccess',
                        'Value': 1,
                        'Unit': 'Count',
                        'Dimensions': [
                            {
                                'Name': 'PipelineName',
                                'Value': execution.pipeline_name
                            }
                        ]
                    }
                ]
            )
            
            # Calculate deployment duration
            if execution.completed_at and execution.started_at:
                duration = (execution.completed_at - execution.started_at).total_seconds()
                
                self.cloudwatch.put_metric_data(
                    Namespace='DeploymentPipeline',
                    MetricData=[
                        {
                            'MetricName': 'DeploymentDuration',
                            'Value': duration,
                            'Unit': 'Seconds',
                            'Dimensions': [
                                {
                                    'Name': 'PipelineName',
                                    'Value': execution.pipeline_name
                                }
                            ]
                        }
                    ]
                )
            
            logging.info(f"Deployment successful: {execution.execution_id}")
            
        except Exception as e:
            logging.error(f"Failed to handle successful deployment: {str(e)}")
    
    async def _handle_failed_deployment(self, execution: PipelineExecution):
        """Handle failed deployment"""
        try:
            # Send failure metrics
            self.cloudwatch.put_metric_data(
                Namespace='DeploymentPipeline',
                MetricData=[
                    {
                        'MetricName': 'DeploymentFailure',
                        'Value': 1,
                        'Unit': 'Count',
                        'Dimensions': [
                            {
                                'Name': 'PipelineName',
                                'Value': execution.pipeline_name
                            }
                        ]
                    }
                ]
            )
            
            # Trigger automated rollback if configured
            pipeline_config = await self._get_pipeline_config(execution.pipeline_name)
            if pipeline_config and pipeline_config.get('auto_rollback_enabled', False):
                await self._trigger_automated_rollback(execution)
            
            logging.error(f"Deployment failed: {execution.execution_id}")
            
        except Exception as e:
            logging.error(f"Failed to handle deployment failure: {str(e)}")
    
    async def _send_pipeline_notification(self, execution: PipelineExecution):
        """Send pipeline execution notification"""
        try:
            if not self.notification_topic:
                return
            
            message = {
                'pipeline_name': execution.pipeline_name,
                'execution_id': execution.execution_id,
                'status': execution.status.value,
                'triggered_by': execution.triggered_by,
                'duration': str(execution.completed_at - execution.started_at) if execution.completed_at else None,
                'current_stage': execution.current_stage.value if execution.current_stage else None,
                'error_message': execution.error_message
            }
            
            subject = f"Pipeline {execution.status.value.title()}: {execution.pipeline_name}"
            
            self.sns.publish(
                TopicArn=self.notification_topic,
                Message=json.dumps(message, indent=2),
                Subject=subject
            )
            
        except Exception as e:
            logging.error(f"Failed to send pipeline notification: {str(e)}")
    
    async def _store_execution(self, execution: PipelineExecution):
        """Store pipeline execution"""
        try:
            execution_dict = asdict(execution)
            execution_dict['started_at'] = execution.started_at.isoformat()
            if execution.completed_at:
                execution_dict['completed_at'] = execution.completed_at.isoformat()
            
            self.executions_table.put_item(Item=execution_dict)
            
        except Exception as e:
            logging.error(f"Failed to store execution: {str(e)}")

# Usage example
async def main():
    config = {
        'executions_table': 'pipeline-executions',
        'pipelines_table': 'deployment-pipelines',
        'artifact_bucket': 'my-deployment-artifacts',
        'notification_topic_arn': 'arn:aws:sns:us-east-1:123456789012:pipeline-notifications'
    }
    
    # Initialize deployment pipeline
    pipeline = AutomatedDeploymentPipeline(config)
    
    # Create pipeline
    pipeline_config = {
        'pipeline_name': 'web-app-pipeline',
        'repository_name': 'web-app-repo',
        'branch_name': 'main',
        'application_name': 'web-app',
        'service_role_arn': 'arn:aws:iam::123456789012:role/CodePipelineServiceRole',
        'build_service_role_arn': 'arn:aws:iam::123456789012:role/CodeBuildServiceRole'
    }
    
    pipeline_name = await pipeline.create_deployment_pipeline(pipeline_config)
    print(f"Created pipeline: {pipeline_name}")
    
    # Execute pipeline
    execution_id = await pipeline.execute_pipeline(pipeline_name, 'developer@company.com')
    print(f"Started execution: {execution_id}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```
{% endraw %}

## AWS Services Used

- **AWS CodePipeline**: Continuous integration and deployment pipeline orchestration
- **AWS CodeBuild**: Automated build, test, and packaging services
- **AWS CodeDeploy**: Automated application deployment and rollback
- **AWS CodeCommit**: Source control integration and version management
- **Amazon S3**: Artifact storage and deployment package management
- **AWS Lambda**: Custom deployment logic and validation functions
- **AWS CloudFormation**: Infrastructure deployment and stack management
- **Amazon DynamoDB**: Pipeline state and execution history storage
- **Amazon SNS**: Pipeline notifications and alerting
- **Amazon CloudWatch**: Pipeline monitoring, metrics, and logging
- **AWS Systems Manager**: Configuration management and parameter storage
- **Amazon ECR**: Container image registry and management
- **AWS Secrets Manager**: Secure credential and configuration management
- **AWS Step Functions**: Complex deployment workflow orchestration
- **Amazon EventBridge**: Event-driven pipeline triggers and automation

## Benefits

- **Consistency**: Automated processes eliminate human error and ensure repeatable deployments
- **Speed**: Automated pipelines significantly reduce deployment time and enable rapid iteration
- **Reliability**: Comprehensive testing and validation improve deployment success rates
- **Traceability**: Complete audit trail of all changes and deployment activities
- **Scalability**: Automated systems scale with team growth and deployment frequency
- **Quality**: Integrated testing and quality gates maintain high code standards
- **Security**: Automated security scanning and compliance checks reduce vulnerabilities
- **Efficiency**: Reduced manual effort allows teams to focus on development and innovation
- **Feedback**: Rapid feedback loops enable quick identification and resolution of issues
- **Compliance**: Automated processes support regulatory and governance requirements

## Related Resources

- [AWS Well-Architected Reliability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/)
- [Deploy Changes with Automation](https://docs.aws.amazon.com/wellarchitected/latest/framework/rel_implement_change_automation.html)
- [AWS CodePipeline User Guide](https://docs.aws.amazon.com/codepipeline/latest/userguide/)
- [AWS CodeBuild User Guide](https://docs.aws.amazon.com/codebuild/latest/userguide/)
- [AWS CodeDeploy User Guide](https://docs.aws.amazon.com/codedeploy/latest/userguide/)
- [AWS CodeCommit User Guide](https://docs.aws.amazon.com/codecommit/latest/userguide/)
- [Amazon S3 User Guide](https://docs.aws.amazon.com/s3/latest/userguide/)
- [AWS Lambda Developer Guide](https://docs.aws.amazon.com/lambda/latest/dg/)
- [CI/CD Best Practices](https://docs.aws.amazon.com/whitepapers/latest/practicing-continuous-integration-continuous-delivery/welcome.html)
- [AWS Builders' Library - Automating Safe Deployments](https://aws.amazon.com/builders-library/automating-safe-hands-off-deployments/)
- [DevOps Best Practices](https://aws.amazon.com/devops/)
- [Deployment Automation Strategies](https://aws.amazon.com/architecture/well-architected/)
