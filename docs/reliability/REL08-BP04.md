---
title: REL08-BP04 - Deploy using immutable infrastructure
layout: default
parent: REL08 - How do you implement change?
grand_parent: Reliability
nav_order: 4
---

# REL08-BP04: Deploy using immutable infrastructure

## Overview

Implement immutable infrastructure deployment patterns where infrastructure components are replaced rather than modified in place. This approach eliminates configuration drift, ensures consistency across environments, and provides reliable rollback capabilities by treating infrastructure as disposable and reproducible.

## Implementation Steps

### 1. Design Immutable Infrastructure Architecture
- Implement infrastructure as code with version control
- Design stateless application architectures
- Establish artifact management and image building pipelines
- Configure environment-specific parameter management

### 2. Implement Container-Based Deployments
- Create containerized applications with immutable images
- Configure container orchestration and deployment strategies
- Implement image scanning and security validation
- Establish container registry management and versioning

### 3. Configure Infrastructure Provisioning
- Implement automated infrastructure provisioning
- Design blue-green and canary deployment strategies
- Configure load balancer and traffic routing automation
- Establish resource cleanup and lifecycle management

### 4. Establish Configuration Management
- Implement externalized configuration management
- Configure secrets and credential management
- Design environment-specific configuration injection
- Establish configuration validation and compliance

### 5. Implement Deployment Automation
- Configure automated deployment pipelines
- Implement deployment validation and health checks
- Design rollback automation and recovery procedures
- Establish deployment monitoring and alerting

### 6. Monitor and Optimize Deployment Performance
- Track deployment frequency and success rates
- Monitor infrastructure consistency and drift detection
- Implement cost optimization for immutable deployments
- Establish performance benchmarking and optimization

## Implementation Examples

### Example 1: Comprehensive Immutable Infrastructure System
```python
import boto3
import json
import logging
import asyncio
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import yaml
import hashlib

class DeploymentStrategy(Enum):
    BLUE_GREEN = "blue_green"
    CANARY = "canary"
    ROLLING = "rolling"
    RECREATE = "recreate"

class DeploymentStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"

@dataclass
class ImmutableDeployment:
    deployment_id: str
    application_name: str
    version: str
    strategy: DeploymentStrategy
    infrastructure_template: str
    container_image: str
    configuration: Dict[str, Any]
    target_environment: str
    created_at: datetime
    created_by: str

@dataclass
class DeploymentExecution:
    execution_id: str
    deployment_id: str
    status: DeploymentStatus
    started_at: datetime
    completed_at: Optional[datetime]
    current_phase: str
    blue_environment: Optional[str]
    green_environment: Optional[str]
    traffic_percentage: int
    health_checks_passed: bool
    rollback_triggered: bool
    error_message: Optional[str]

class ImmutableInfrastructureManager:
    """Comprehensive immutable infrastructure deployment system"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
        # AWS clients
        self.cloudformation = boto3.client('cloudformation')
        self.ecs = boto3.client('ecs')
        self.ecr = boto3.client('ecr')
        self.elbv2 = boto3.client('elbv2')
        self.route53 = boto3.client('route53')
        self.lambda_client = boto3.client('lambda')
        self.codedeploy = boto3.client('codedeploy')
        self.dynamodb = boto3.resource('dynamodb')
        self.s3 = boto3.client('s3')
        
        # Storage
        self.deployments_table = self.dynamodb.Table(config.get('deployments_table', 'immutable-deployments'))
        self.executions_table = self.dynamodb.Table(config.get('executions_table', 'deployment-executions'))
        
        # Configuration
        self.template_bucket = config.get('template_bucket', 'infrastructure-templates')
        self.artifact_bucket = config.get('artifact_bucket', 'deployment-artifacts')
        
        # Active deployments
        self.active_deployments = {}
        
    async def create_immutable_deployment(self, deployment_config: Dict[str, Any]) -> str:
        """Create a new immutable deployment"""
        try:
            deployment_id = f"deploy_{int(datetime.utcnow().timestamp())}_{deployment_config['application_name']}"
            
            # Build container image
            image_uri = await self._build_container_image(deployment_config)
            
            # Generate infrastructure template
            template_content = await self._generate_infrastructure_template(deployment_config)
            
            # Create deployment record
            deployment = ImmutableDeployment(
                deployment_id=deployment_id,
                application_name=deployment_config['application_name'],
                version=deployment_config['version'],
                strategy=DeploymentStrategy(deployment_config.get('strategy', 'blue_green')),
                infrastructure_template=template_content,
                container_image=image_uri,
                configuration=deployment_config.get('configuration', {}),
                target_environment=deployment_config['target_environment'],
                created_at=datetime.utcnow(),
                created_by=deployment_config['created_by']
            )
            
            # Store deployment
            await self._store_deployment(deployment)
            
            logging.info(f"Created immutable deployment: {deployment_id}")
            return deployment_id
            
        except Exception as e:
            logging.error(f"Failed to create immutable deployment: {str(e)}")
            raise
    
    async def execute_deployment(self, deployment_id: str) -> str:
        """Execute immutable deployment"""
        try:
            # Get deployment
            deployment = await self._get_deployment(deployment_id)
            if not deployment:
                raise ValueError(f"Deployment {deployment_id} not found")
            
            # Create execution record
            execution_id = f"exec_{int(datetime.utcnow().timestamp())}_{deployment_id}"
            
            execution = DeploymentExecution(
                execution_id=execution_id,
                deployment_id=deployment_id,
                status=DeploymentStatus.PENDING,
                started_at=datetime.utcnow(),
                completed_at=None,
                current_phase="initialization",
                blue_environment=None,
                green_environment=None,
                traffic_percentage=0,
                health_checks_passed=False,
                rollback_triggered=False,
                error_message=None
            )
            
            # Store execution
            await self._store_execution(execution)
            
            # Start deployment execution
            self.active_deployments[execution_id] = execution
            asyncio.create_task(self._execute_deployment_strategy(deployment, execution))
            
            logging.info(f"Started deployment execution: {execution_id}")
            return execution_id
            
        except Exception as e:
            logging.error(f"Failed to execute deployment: {str(e)}")
            raise
    
    async def _execute_deployment_strategy(self, deployment: ImmutableDeployment, 
                                         execution: DeploymentExecution):
        """Execute deployment based on strategy"""
        try:
            execution.status = DeploymentStatus.IN_PROGRESS
            await self._store_execution(execution)
            
            if deployment.strategy == DeploymentStrategy.BLUE_GREEN:
                await self._execute_blue_green_deployment(deployment, execution)
            elif deployment.strategy == DeploymentStrategy.CANARY:
                await self._execute_canary_deployment(deployment, execution)
            elif deployment.strategy == DeploymentStrategy.ROLLING:
                await self._execute_rolling_deployment(deployment, execution)
            else:
                raise ValueError(f"Unsupported deployment strategy: {deployment.strategy}")
            
            execution.status = DeploymentStatus.COMPLETED
            execution.completed_at = datetime.utcnow()
            
        except Exception as e:
            logging.error(f"Deployment execution failed: {str(e)}")
            execution.status = DeploymentStatus.FAILED
            execution.error_message = str(e)
            execution.completed_at = datetime.utcnow()
            
            # Trigger rollback
            await self._trigger_rollback(deployment, execution)
        
        finally:
            await self._store_execution(execution)
            if execution.execution_id in self.active_deployments:
                del self.active_deployments[execution.execution_id]
    
    async def _execute_blue_green_deployment(self, deployment: ImmutableDeployment, 
                                           execution: DeploymentExecution):
        """Execute blue-green deployment"""
        try:
            # Phase 1: Create green environment
            execution.current_phase = "creating_green_environment"
            green_stack_name = f"{deployment.application_name}-green-{int(time.time())}"
            
            await self._create_infrastructure_stack(
                green_stack_name, 
                deployment.infrastructure_template,
                deployment.configuration
            )
            
            execution.green_environment = green_stack_name
            await self._store_execution(execution)
            
            # Phase 2: Deploy application to green environment
            execution.current_phase = "deploying_to_green"
            await self._deploy_application_to_environment(
                deployment, green_stack_name
            )
            
            # Phase 3: Health checks on green environment
            execution.current_phase = "health_checks"
            health_passed = await self._perform_health_checks(green_stack_name)
            execution.health_checks_passed = health_passed
            
            if not health_passed:
                raise Exception("Health checks failed on green environment")
            
            # Phase 4: Switch traffic to green environment
            execution.current_phase = "switching_traffic"
            await self._switch_traffic_to_green(deployment, green_stack_name)
            execution.traffic_percentage = 100
            
            # Phase 5: Cleanup old blue environment
            execution.current_phase = "cleanup"
            await self._cleanup_old_environment(deployment.application_name, green_stack_name)
            
            logging.info(f"Blue-green deployment completed: {green_stack_name}")
            
        except Exception as e:
            logging.error(f"Blue-green deployment failed: {str(e)}")
            raise
    
    async def _execute_canary_deployment(self, deployment: ImmutableDeployment, 
                                       execution: DeploymentExecution):
        """Execute canary deployment"""
        try:
            # Phase 1: Create canary environment
            execution.current_phase = "creating_canary_environment"
            canary_stack_name = f"{deployment.application_name}-canary-{int(time.time())}"
            
            await self._create_infrastructure_stack(
                canary_stack_name,
                deployment.infrastructure_template,
                deployment.configuration
            )
            
            execution.green_environment = canary_stack_name
            
            # Phase 2: Deploy to canary
            execution.current_phase = "deploying_to_canary"
            await self._deploy_application_to_environment(deployment, canary_stack_name)
            
            # Phase 3: Gradual traffic shift
            traffic_percentages = [10, 25, 50, 100]
            
            for percentage in traffic_percentages:
                execution.current_phase = f"traffic_shift_{percentage}%"
                execution.traffic_percentage = percentage
                
                # Shift traffic
                await self._shift_traffic_percentage(deployment, canary_stack_name, percentage)
                
                # Monitor for issues
                await asyncio.sleep(300)  # Wait 5 minutes
                
                # Check metrics
                metrics_healthy = await self._check_canary_metrics(canary_stack_name)
                if not metrics_healthy:
                    raise Exception(f"Canary metrics unhealthy at {percentage}% traffic")
                
                await self._store_execution(execution)
            
            # Phase 4: Complete deployment
            execution.current_phase = "completing_deployment"
            await self._complete_canary_deployment(deployment, canary_stack_name)
            
            logging.info(f"Canary deployment completed: {canary_stack_name}")
            
        except Exception as e:
            logging.error(f"Canary deployment failed: {str(e)}")
            raise
    
    async def _build_container_image(self, deployment_config: Dict[str, Any]) -> str:
        """Build and push container image"""
        try:
            app_name = deployment_config['application_name']
            version = deployment_config['version']
            
            # Get ECR repository
            repository_name = f"{app_name}-repo"
            
            try:
                repo_response = self.ecr.describe_repositories(repositoryNames=[repository_name])
                repository_uri = repo_response['repositories'][0]['repositoryUri']
            except self.ecr.exceptions.RepositoryNotFoundException:
                # Create repository if it doesn't exist
                create_response = self.ecr.create_repository(repositoryName=repository_name)
                repository_uri = create_response['repository']['repositoryUri']
            
            # Build image URI
            image_uri = f"{repository_uri}:{version}"
            
            # In a real implementation, this would trigger a build process
            # For now, we'll assume the image is already built and pushed
            logging.info(f"Using container image: {image_uri}")
            
            return image_uri
            
        except Exception as e:
            logging.error(f"Failed to build container image: {str(e)}")
            raise
    
    async def _generate_infrastructure_template(self, deployment_config: Dict[str, Any]) -> str:
        """Generate CloudFormation template for immutable infrastructure"""
        try:
            app_name = deployment_config['application_name']
            
            template = {
                "AWSTemplateFormatVersion": "2010-09-09",
                "Description": f"Immutable infrastructure for {app_name}",
                "Parameters": {
                    "ImageUri": {
                        "Type": "String",
                        "Description": "Container image URI"
                    },
                    "Environment": {
                        "Type": "String",
                        "Description": "Deployment environment"
                    }
                },
                "Resources": {
                    "ECSCluster": {
                        "Type": "AWS::ECS::Cluster",
                        "Properties": {
                            "ClusterName": f"{app_name}-cluster"
                        }
                    },
                    "TaskDefinition": {
                        "Type": "AWS::ECS::TaskDefinition",
                        "Properties": {
                            "Family": f"{app_name}-task",
                            "NetworkMode": "awsvpc",
                            "RequiresCompatibilities": ["FARGATE"],
                            "Cpu": "256",
                            "Memory": "512",
                            "ContainerDefinitions": [
                                {
                                    "Name": app_name,
                                    "Image": {"Ref": "ImageUri"},
                                    "PortMappings": [
                                        {
                                            "ContainerPort": 8080,
                                            "Protocol": "tcp"
                                        }
                                    ],
                                    "LogConfiguration": {
                                        "LogDriver": "awslogs",
                                        "Options": {
                                            "awslogs-group": f"/ecs/{app_name}",
                                            "awslogs-region": {"Ref": "AWS::Region"},
                                            "awslogs-stream-prefix": "ecs"
                                        }
                                    }
                                }
                            ]
                        }
                    },
                    "ECSService": {
                        "Type": "AWS::ECS::Service",
                        "Properties": {
                            "ServiceName": f"{app_name}-service",
                            "Cluster": {"Ref": "ECSCluster"},
                            "TaskDefinition": {"Ref": "TaskDefinition"},
                            "DesiredCount": 2,
                            "LaunchType": "FARGATE",
                            "NetworkConfiguration": {
                                "AwsvpcConfiguration": {
                                    "SecurityGroups": [{"Ref": "SecurityGroup"}],
                                    "Subnets": deployment_config.get('subnet_ids', [])
                                }
                            }
                        }
                    },
                    "SecurityGroup": {
                        "Type": "AWS::EC2::SecurityGroup",
                        "Properties": {
                            "GroupDescription": f"Security group for {app_name}",
                            "VpcId": deployment_config.get('vpc_id'),
                            "SecurityGroupIngress": [
                                {
                                    "IpProtocol": "tcp",
                                    "FromPort": 8080,
                                    "ToPort": 8080,
                                    "CidrIp": "0.0.0.0/0"
                                }
                            ]
                        }
                    }
                },
                "Outputs": {
                    "ServiceArn": {
                        "Description": "ECS Service ARN",
                        "Value": {"Ref": "ECSService"}
                    },
                    "ClusterArn": {
                        "Description": "ECS Cluster ARN",
                        "Value": {"Ref": "ECSCluster"}
                    }
                }
            }
            
            return json.dumps(template, indent=2)
            
        except Exception as e:
            logging.error(f"Failed to generate infrastructure template: {str(e)}")
            raise
    
    async def _create_infrastructure_stack(self, stack_name: str, template: str, 
                                         parameters: Dict[str, Any]):
        """Create CloudFormation stack"""
        try:
            # Convert parameters to CloudFormation format
            cf_parameters = []
            for key, value in parameters.items():
                cf_parameters.append({
                    'ParameterKey': key,
                    'ParameterValue': str(value)
                })
            
            # Create stack
            self.cloudformation.create_stack(
                StackName=stack_name,
                TemplateBody=template,
                Parameters=cf_parameters,
                Capabilities=['CAPABILITY_IAM']
            )
            
            # Wait for stack creation to complete
            waiter = self.cloudformation.get_waiter('stack_create_complete')
            waiter.wait(StackName=stack_name, WaiterConfig={'Delay': 30, 'MaxAttempts': 60})
            
            logging.info(f"Created infrastructure stack: {stack_name}")
            
        except Exception as e:
            logging.error(f"Failed to create infrastructure stack: {str(e)}")
            raise
    
    async def _deploy_application_to_environment(self, deployment: ImmutableDeployment, 
                                               environment_name: str):
        """Deploy application to environment"""
        try:
            # Update ECS service with new task definition
            # This is simplified - in practice, you'd update the service with the new image
            
            logging.info(f"Deployed application to environment: {environment_name}")
            
        except Exception as e:
            logging.error(f"Failed to deploy application: {str(e)}")
            raise
    
    async def _perform_health_checks(self, environment_name: str) -> bool:
        """Perform health checks on environment"""
        try:
            # Get stack outputs to find service endpoint
            stack_response = self.cloudformation.describe_stacks(StackName=environment_name)
            
            # Perform health checks
            # This is simplified - in practice, you'd check service health endpoints
            
            # Wait for services to be healthy
            await asyncio.sleep(60)  # Wait 1 minute for services to start
            
            # Check ECS service status
            # This would involve checking service health and target group health
            
            logging.info(f"Health checks passed for environment: {environment_name}")
            return True
            
        except Exception as e:
            logging.error(f"Health checks failed: {str(e)}")
            return False
    
    async def _switch_traffic_to_green(self, deployment: ImmutableDeployment, 
                                     green_environment: str):
        """Switch traffic to green environment"""
        try:
            # Update load balancer target groups or Route 53 records
            # This is simplified - in practice, you'd update ALB target groups
            
            logging.info(f"Switched traffic to green environment: {green_environment}")
            
        except Exception as e:
            logging.error(f"Failed to switch traffic: {str(e)}")
            raise
    
    async def _trigger_rollback(self, deployment: ImmutableDeployment, 
                              execution: DeploymentExecution):
        """Trigger deployment rollback"""
        try:
            execution.rollback_triggered = True
            execution.current_phase = "rollback"
            
            # Clean up failed green environment
            if execution.green_environment:
                await self._cleanup_environment(execution.green_environment)
            
            # Restore traffic to blue environment if needed
            if execution.traffic_percentage > 0:
                await self._restore_traffic_to_blue(deployment)
            
            logging.info(f"Rollback completed for deployment: {deployment.deployment_id}")
            
        except Exception as e:
            logging.error(f"Rollback failed: {str(e)}")
    
    async def _cleanup_environment(self, environment_name: str):
        """Clean up environment resources"""
        try:
            # Delete CloudFormation stack
            self.cloudformation.delete_stack(StackName=environment_name)
            
            # Wait for deletion to complete
            waiter = self.cloudformation.get_waiter('stack_delete_complete')
            waiter.wait(StackName=environment_name, WaiterConfig={'Delay': 30, 'MaxAttempts': 60})
            
            logging.info(f"Cleaned up environment: {environment_name}")
            
        except Exception as e:
            logging.error(f"Failed to cleanup environment: {str(e)}")
    
    async def _store_deployment(self, deployment: ImmutableDeployment):
        """Store deployment record"""
        try:
            deployment_dict = asdict(deployment)
            deployment_dict['created_at'] = deployment.created_at.isoformat()
            
            self.deployments_table.put_item(Item=deployment_dict)
            
        except Exception as e:
            logging.error(f"Failed to store deployment: {str(e)}")
    
    async def _store_execution(self, execution: DeploymentExecution):
        """Store execution record"""
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
        'deployments_table': 'immutable-deployments',
        'executions_table': 'deployment-executions',
        'template_bucket': 'infrastructure-templates',
        'artifact_bucket': 'deployment-artifacts'
    }
    
    # Initialize immutable infrastructure manager
    infra_manager = ImmutableInfrastructureManager(config)
    
    # Create deployment
    deployment_config = {
        'application_name': 'web-app',
        'version': '2.1.0',
        'strategy': 'blue_green',
        'target_environment': 'production',
        'created_by': 'devops@company.com',
        'configuration': {
            'ImageUri': 'my-app:2.1.0',
            'Environment': 'production'
        },
        'vpc_id': 'vpc-12345678',
        'subnet_ids': ['subnet-12345678', 'subnet-87654321']
    }
    
    # Create deployment
    deployment_id = await infra_manager.create_immutable_deployment(deployment_config)
    print(f"Created deployment: {deployment_id}")
    
    # Execute deployment
    execution_id = await infra_manager.execute_deployment(deployment_id)
    print(f"Started execution: {execution_id}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## AWS Services Used

- **AWS CloudFormation**: Infrastructure as code and immutable stack management
- **Amazon ECS/Fargate**: Container orchestration and immutable container deployments
- **Amazon ECR**: Container image registry and version management
- **Elastic Load Balancing**: Traffic routing and blue-green deployment support
- **Amazon Route 53**: DNS-based traffic switching and weighted routing
- **AWS CodeDeploy**: Automated deployment orchestration and rollback
- **AWS Lambda**: Custom deployment logic and automation functions
- **Amazon S3**: Template storage and deployment artifact management
- **Amazon DynamoDB**: Deployment state and execution history storage
- **AWS Systems Manager**: Configuration management and parameter storage
- **Amazon CloudWatch**: Deployment monitoring and health checks
- **AWS Auto Scaling**: Immutable scaling group replacements
- **Amazon API Gateway**: API versioning and traffic management
- **AWS Step Functions**: Complex deployment workflow orchestration
- **AWS Secrets Manager**: Secure configuration and credential management

## Benefits

- **Consistency**: Identical infrastructure across all environments eliminates configuration drift
- **Reliability**: Immutable deployments reduce deployment-related failures and inconsistencies
- **Rollback Speed**: Quick rollback to previous known-good state without complex recovery procedures
- **Auditability**: Complete deployment history and infrastructure versioning for compliance
- **Scalability**: Automated provisioning supports rapid scaling and environment creation
- **Security**: Fresh infrastructure reduces security vulnerabilities from long-running systems
- **Testing**: Identical environments enable reliable testing and validation
- **Disaster Recovery**: Rapid environment recreation from code and artifacts
- **Cost Optimization**: Efficient resource utilization through automated lifecycle management
- **Team Confidence**: Predictable deployments increase team confidence and deployment frequency

## Related Resources

- [AWS Well-Architected Reliability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/)
- [Deploy Using Immutable Infrastructure](https://docs.aws.amazon.com/wellarchitected/latest/framework/rel_implement_change_immutable_infrastructure.html)
- [AWS CloudFormation User Guide](https://docs.aws.amazon.com/cloudformation/latest/userguide/)
- [Amazon ECS Developer Guide](https://docs.aws.amazon.com/ecs/latest/developerguide/)
- [Amazon ECR User Guide](https://docs.aws.amazon.com/ecr/latest/userguide/)
- [AWS CodeDeploy User Guide](https://docs.aws.amazon.com/codedeploy/latest/userguide/)
- [Elastic Load Balancing User Guide](https://docs.aws.amazon.com/elasticloadbalancing/latest/userguide/)
- [Amazon Route 53 Developer Guide](https://docs.aws.amazon.com/route53/latest/developerguide/)
- [Infrastructure as Code Best Practices](https://docs.aws.amazon.com/whitepapers/latest/introduction-devops-aws/infrastructure-as-code.html)
- [AWS Builders' Library - Automating Safe Deployments](https://aws.amazon.com/builders-library/automating-safe-hands-off-deployments/)
- [Blue-Green Deployments](https://docs.aws.amazon.com/whitepapers/latest/blue-green-deployments/welcome.html)
- [Container Best Practices](https://aws.amazon.com/architecture/containers/)
