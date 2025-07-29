---
title: SEC11-BP06 - Deploy software programmatically
layout: default
parent: SEC11 - How do you incorporate and validate the security properties of applications?
grand_parent: Security
nav_order: 6
---

<div class="pillar-header">
  <h1>SEC11-BP06: Deploy software programmatically</h1>
  <p>Deploy software programmatically where possible. This approach reduces the likelihood of deployment errors, provides consistency across environments, and enables automated security controls and compliance checks.</p>
</div>

## Implementation guidance

Programmatic software deployment is essential for maintaining security, consistency, and reliability across your application lifecycle. By automating deployments, you eliminate human error, ensure reproducible processes, and enable comprehensive security controls at every stage.

### Key steps for implementing this best practice:

1. **Establish Infrastructure as Code (IaC)**:
   - Use AWS CloudFormation, CDK, or Terraform for infrastructure provisioning
   - Version control all infrastructure definitions
   - Implement infrastructure testing and validation
   - Create reusable infrastructure components and modules
   - Establish infrastructure change management processes

2. **Implement automated CI/CD pipelines**:
   - Set up continuous integration with automated testing
   - Configure continuous deployment with approval gates
   - Implement blue-green or canary deployment strategies
   - Create rollback mechanisms and disaster recovery procedures
   - Integrate security scanning and compliance checks

3. **Configure deployment automation**:
   - Use AWS CodeDeploy, ECS, or Kubernetes for application deployment
   - Implement automated configuration management
   - Set up environment-specific deployment configurations
   - Create deployment monitoring and health checks
   - Establish deployment artifact management

4. **Integrate security controls**:
   - Implement security scanning in deployment pipelines
   - Configure automated compliance validation
   - Set up runtime security monitoring
   - Create security approval workflows
   - Establish security incident response automation

5. **Implement deployment governance**:
   - Create deployment policies and approval processes
   - Set up audit logging and compliance reporting
   - Implement change management and approval workflows
   - Establish deployment metrics and monitoring
   - Create disaster recovery and business continuity procedures

6. **Enable observability and monitoring**:
   - Implement comprehensive logging and monitoring
   - Set up alerting and notification systems
   - Create deployment dashboards and reporting
   - Establish performance and security metrics
   - Configure automated incident response

## Implementation examples

### Example 1: AWS CDK deployment pipeline with security controls

```typescript
import * as cdk from 'aws-cdk-lib';
import * as codepipeline from 'aws-cdk-lib/aws-codepipeline';
import * as codepipeline_actions from 'aws-cdk-lib/aws-codepipeline-actions';
import * as codebuild from 'aws-cdk-lib/aws-codebuild';
import * as codecommit from 'aws-cdk-lib/aws-codecommit';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as sns from 'aws-cdk-lib/aws-sns';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import { Construct } from 'constructs';

export class SecureDeploymentPipelineStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Source repository
    const repository = new codecommit.Repository(this, 'ApplicationRepository', {
      repositoryName: 'secure-application',
      description: 'Application source code with security controls'
    });

    // Artifact bucket for pipeline artifacts
    const artifactBucket = new s3.Bucket(this, 'PipelineArtifacts', {
      bucketName: `pipeline-artifacts-${this.account}-${this.region}`,
      encryption: s3.BucketEncryption.S3_MANAGED,
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
      versioned: true,
      lifecycleRules: [{
        id: 'DeleteOldArtifacts',
        expiration: cdk.Duration.days(30)
      }]
    });

    // SNS topic for deployment notifications
    const deploymentTopic = new sns.Topic(this, 'DeploymentNotifications', {
      displayName: 'Deployment Pipeline Notifications'
    });

    // Security scanning project
    const securityScanProject = new codebuild.Project(this, 'SecurityScanProject', {
      projectName: 'security-scan-project',
      description: 'Security scanning and compliance validation',
      source: codebuild.Source.codeCommit({
        repository: repository
      }),
      environment: {
        buildImage: codebuild.LinuxBuildImage.STANDARD_5_0,
        computeType: codebuild.ComputeType.MEDIUM,
        privileged: true
      },
      buildSpec: codebuild.BuildSpec.fromObject({
        version: '0.2',
        phases: {
          install: {
            'runtime-versions': {
              nodejs: '18',
              python: '3.9'
            },
            commands: [
              'echo Installing security scanning tools...',
              'npm install -g @aws-cdk/cdk-nag',
              'pip install bandit safety checkov',
              'curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sh -s -- -b /usr/local/bin',
              'curl -sSfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin'
            ]
          },
          pre_build: {
            commands: [
              'echo Starting security scans...',
              'echo Logging in to Amazon ECR...',
              'aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com'
            ]
          },
          build: {
            commands: [
              // Static Application Security Testing (SAST)
              'echo "Running SAST scans..."',
              'bandit -r src/ -f json -o bandit-report.json || true',
              'safety check --json --output safety-report.json || true',
              
              // Infrastructure as Code scanning
              'echo "Running IaC security scans..."',
              'checkov -d infrastructure/ --framework cloudformation --output json --output-file checkov-report.json || true',
              
              // CDK Nag scanning
              'echo "Running CDK Nag..."',
              'cd infrastructure && npm install && npm run build',
              'npx cdk-nag --app "npx ts-node app.ts" --output cdk-nag-report.json || true',
              
              // Container image scanning
              'echo "Building and scanning container images..."',
              'docker build -t app:latest .',
              'trivy image --format json --output trivy-report.json app:latest || true',
              'grype app:latest -o json --file grype-report.json || true',
              
              // Dependency scanning
              'echo "Running dependency scans..."',
              'npm audit --json > npm-audit-report.json || true',
              'pip-audit --format=json --output=pip-audit-report.json || true'
            ]
          },
          post_build: {
            commands: [
              'echo "Processing security scan results..."',
              'python scripts/process-security-results.py',
              'echo "Security scanning completed"'
            ]
          }
        },
        artifacts: {
          files: [
            '**/*',
            'security-reports/**/*'
          ]
        }
      }),
      role: new iam.Role(this, 'SecurityScanRole', {
        assumedBy: new iam.ServicePrincipal('codebuild.amazonaws.com'),
        managedPolicies: [
          iam.ManagedPolicy.fromAwsManagedPolicyName('AWSCodeBuildDeveloperAccess'),
          iam.ManagedPolicy.fromAwsManagedPolicyName('AmazonEC2ContainerRegistryPowerUser')
        ],
        inlinePolicies: {
          SecurityScanPolicy: new iam.PolicyDocument({
            statements: [
              new iam.PolicyStatement({
                effect: iam.Effect.ALLOW,
                actions: [
                  'inspector2:*',
                  'securityhub:*',
                  's3:GetObject',
                  's3:PutObject'
                ],
                resources: ['*']
              })
            ]
          })
        }
      })
    });

    // Build project
    const buildProject = new codebuild.Project(this, 'BuildProject', {
      projectName: 'application-build-project',
      description: 'Build and package application',
      source: codebuild.Source.codeCommit({
        repository: repository
      }),
      environment: {
        buildImage: codebuild.LinuxBuildImage.STANDARD_5_0,
        computeType: codebuild.ComputeType.MEDIUM,
        privileged: true
      },
      buildSpec: codebuild.BuildSpec.fromObject({
        version: '0.2',
        phases: {
          install: {
            'runtime-versions': {
              nodejs: '18'
            }
          },
          pre_build: {
            commands: [
              'echo Logging in to Amazon ECR...',
              'aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com',
              'REPOSITORY_URI=$AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/secure-app',
              'COMMIT_HASH=$(echo $CODEBUILD_RESOLVED_SOURCE_VERSION | cut -c 1-7)',
              'IMAGE_TAG=${COMMIT_HASH:=latest}'
            ]
          },
          build: {
            commands: [
              'echo Build started on `date`',
              'echo Building the Docker image...',
              'docker build -t $REPOSITORY_URI:latest .',
              'docker tag $REPOSITORY_URI:latest $REPOSITORY_URI:$IMAGE_TAG'
            ]
          },
          post_build: {
            commands: [
              'echo Build completed on `date`',
              'echo Pushing the Docker images...',
              'docker push $REPOSITORY_URI:latest',
              'docker push $REPOSITORY_URI:$IMAGE_TAG',
              'echo Writing image definitions file...',
              'printf \'[{"name":"secure-app","imageUri":"%s"}]\' $REPOSITORY_URI:$IMAGE_TAG > imagedefinitions.json'
            ]
          }
        },
        artifacts: {
          files: [
            'imagedefinitions.json',
            'infrastructure/**/*'
          ]
        }
      })
    });

    // Deployment approval Lambda
    const deploymentApprovalFunction = new lambda.Function(this, 'DeploymentApprovalFunction', {
      runtime: lambda.Runtime.PYTHON_3_9,
      handler: 'index.lambda_handler',
      code: lambda.Code.fromInline(`
import json
import boto3
import os

def lambda_handler(event, context):
    codepipeline = boto3.client('codepipeline')
    
    # Extract pipeline information
    job_id = event['CodePipeline.job']['id']
    input_artifacts = event['CodePipeline.job']['data']['inputArtifacts']
    
    try:
        # Process security scan results
        security_results = process_security_results(input_artifacts)
        
        # Determine if deployment should be approved
        approval_decision = evaluate_security_results(security_results)
        
        if approval_decision['approved']:
            codepipeline.put_job_success_result(jobId=job_id)
            send_notification(f"Deployment approved: {approval_decision['reason']}")
        else:
            codepipeline.put_job_failure_result(
                jobId=job_id,
                failureDetails={'message': approval_decision['reason'], 'type': 'JobFailed'}
            )
            send_notification(f"Deployment rejected: {approval_decision['reason']}")
            
    except Exception as e:
        codepipeline.put_job_failure_result(
            jobId=job_id,
            failureDetails={'message': str(e), 'type': 'JobFailed'}
        )
        send_notification(f"Deployment approval failed: {str(e)}")
    
    return {'statusCode': 200}

def process_security_results(input_artifacts):
    # Process security scan results from artifacts
    # Implementation would parse JSON reports from security scanning
    return {
        'critical_vulnerabilities': 0,
        'high_vulnerabilities': 2,
        'medium_vulnerabilities': 5,
        'compliance_score': 85
    }

def evaluate_security_results(results):
    # Define security thresholds
    if results['critical_vulnerabilities'] > 0:
        return {'approved': False, 'reason': 'Critical vulnerabilities detected'}
    
    if results['high_vulnerabilities'] > 5:
        return {'approved': False, 'reason': 'Too many high-severity vulnerabilities'}
    
    if results['compliance_score'] < 80:
        return {'approved': False, 'reason': 'Compliance score below threshold'}
    
    return {'approved': True, 'reason': 'Security validation passed'}

def send_notification(message):
    sns = boto3.client('sns')
    sns.publish(
        TopicArn=os.environ['NOTIFICATION_TOPIC'],
        Subject='Deployment Security Validation',
        Message=message
    )
      `),
      environment: {
        'NOTIFICATION_TOPIC': deploymentTopic.topicArn
      }
    });

    // Grant permissions to the Lambda function
    deploymentTopic.grantPublish(deploymentApprovalFunction);

    // Pipeline artifacts
    const sourceOutput = new codepipeline.Artifact('SourceOutput');
    const securityScanOutput = new codepipeline.Artifact('SecurityScanOutput');
    const buildOutput = new codepipeline.Artifact('BuildOutput');

    // Create the pipeline
    const pipeline = new codepipeline.Pipeline(this, 'SecureDeploymentPipeline', {
      pipelineName: 'secure-deployment-pipeline',
      artifactBucket: artifactBucket,
      stages: [
        {
          stageName: 'Source',
          actions: [
            new codepipeline_actions.CodeCommitSourceAction({
              actionName: 'Source',
              repository: repository,
              branch: 'main',
              output: sourceOutput,
              trigger: codepipeline_actions.CodeCommitTrigger.EVENTS
            })
          ]
        },
        {
          stageName: 'SecurityScan',
          actions: [
            new codepipeline_actions.CodeBuildAction({
              actionName: 'SecurityScan',
              project: securityScanProject,
              input: sourceOutput,
              outputs: [securityScanOutput]
            })
          ]
        },
        {
          stageName: 'SecurityApproval',
          actions: [
            new codepipeline_actions.LambdaInvokeAction({
              actionName: 'SecurityApproval',
              lambda: deploymentApprovalFunction,
              inputs: [securityScanOutput]
            })
          ]
        },
        {
          stageName: 'Build',
          actions: [
            new codepipeline_actions.CodeBuildAction({
              actionName: 'Build',
              project: buildProject,
              input: sourceOutput,
              outputs: [buildOutput]
            })
          ]
        },
        {
          stageName: 'DeployToStaging',
          actions: [
            new codepipeline_actions.EcsDeployAction({
              actionName: 'DeployToStaging',
              service: stagingService, // ECS service reference
              input: buildOutput
            })
          ]
        },
        {
          stageName: 'ProductionApproval',
          actions: [
            new codepipeline_actions.ManualApprovalAction({
              actionName: 'ProductionApproval',
              notificationTopic: deploymentTopic,
              additionalInformation: 'Please review staging deployment and approve for production'
            })
          ]
        },
        {
          stageName: 'DeployToProduction',
          actions: [
            new codepipeline_actions.EcsDeployAction({
              actionName: 'DeployToProduction',
              service: productionService, // ECS service reference
              input: buildOutput
            })
          ]
        }
      ]
    });

    // Output pipeline information
    new cdk.CfnOutput(this, 'PipelineName', {
      value: pipeline.pipelineName,
      description: 'Name of the deployment pipeline'
    });

    new cdk.CfnOutput(this, 'RepositoryCloneUrl', {
      value: repository.repositoryCloneUrlHttp,
      description: 'Repository clone URL'
    });
  }
}
```

### Example 2: Terraform-based infrastructure deployment with security validation

```hcl
# main.tf - Secure infrastructure deployment
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  backend "s3" {
    bucket         = "terraform-state-bucket"
    key            = "secure-app/terraform.tfstate"
    region         = "us-west-2"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}

provider "aws" {
  region = var.aws_region
  
  default_tags {
    tags = {
      Environment   = var.environment
      Project       = var.project_name
      ManagedBy     = "Terraform"
      SecurityScan  = "Required"
    }
  }
}

# Security scanning and validation
resource "null_resource" "security_validation" {
  triggers = {
    always_run = timestamp()
  }
  
  provisioner "local-exec" {
    command = <<-EOT
      echo "Running security validation..."
      
      # Run Checkov for IaC security scanning
      checkov -d . --framework terraform --output json --output-file checkov-results.json
      
      # Run tfsec for Terraform security scanning
      tfsec . --format json --out tfsec-results.json
      
      # Run Terrascan for policy validation
      terrascan scan -t terraform -f . -o json --output terrascan-results.json
      
      # Process results and fail if critical issues found
      python3 scripts/process-terraform-security-results.py
    EOT
  }
}

# VPC with security controls
module "vpc" {
  source = "./modules/secure-vpc"
  
  name_prefix        = "${var.project_name}-${var.environment}"
  cidr_block         = var.vpc_cidr
  availability_zones = var.availability_zones
  
  enable_flow_logs    = true
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  # Security configurations
  enable_network_acls = true
  enable_nat_gateway  = true
  
  tags = local.common_tags
  
  depends_on = [null_resource.security_validation]
}

# ECS cluster with security configurations
resource "aws_ecs_cluster" "main" {
  name = "${var.project_name}-${var.environment}"
  
  configuration {
    execute_command_configuration {
      kms_key_id = aws_kms_key.ecs_key.arn
      logging    = "OVERRIDE"
      
      log_configuration {
        cloud_watch_encryption_enabled = true
        cloud_watch_log_group_name     = aws_cloudwatch_log_group.ecs_exec.name
      }
    }
  }
  
  setting {
    name  = "containerInsights"
    value = "enabled"
  }
  
  tags = local.common_tags
}

# KMS key for encryption
resource "aws_kms_key" "ecs_key" {
  description             = "KMS key for ECS encryption"
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
      }
    ]
  })
  
  tags = local.common_tags
}

resource "aws_kms_alias" "ecs_key" {
  name          = "alias/${var.project_name}-${var.environment}-ecs"
  target_key_id = aws_kms_key.ecs_key.key_id
}

# CloudWatch log group for ECS Exec
resource "aws_cloudwatch_log_group" "ecs_exec" {
  name              = "/aws/ecs/${var.project_name}-${var.environment}/exec"
  retention_in_days = 30
  kms_key_id        = aws_kms_key.ecs_key.arn
  
  tags = local.common_tags
}

# ECS task definition with security configurations
resource "aws_ecs_task_definition" "app" {
  family                   = "${var.project_name}-${var.environment}"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.task_cpu
  memory                   = var.task_memory
  execution_role_arn       = aws_iam_role.ecs_execution_role.arn
  task_role_arn           = aws_iam_role.ecs_task_role.arn
  
  container_definitions = jsonencode([
    {
      name  = "app"
      image = "${var.ecr_repository_url}:${var.image_tag}"
      
      essential = true
      
      portMappings = [
        {
          containerPort = var.container_port
          protocol      = "tcp"
        }
      ]
      
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.app.name
          "awslogs-region"        = var.aws_region
          "awslogs-stream-prefix" = "ecs"
        }
      }
      
      environment = [
        {
          name  = "ENVIRONMENT"
          value = var.environment
        }
      ]
      
      secrets = [
        {
          name      = "DATABASE_PASSWORD"
          valueFrom = aws_ssm_parameter.db_password.arn
        }
      ]
      
      # Security configurations
      readonlyRootFilesystem = true
      user                   = "1000:1000"
      
      linuxParameters = {
        capabilities = {
          drop = ["ALL"]
        }
      }
      
      healthCheck = {
        command     = ["CMD-SHELL", "curl -f http://localhost:${var.container_port}/health || exit 1"]
        interval    = 30
        timeout     = 5
        retries     = 3
        startPeriod = 60
      }
    }
  ])
  
  tags = local.common_tags
}

# ECS service with security configurations
resource "aws_ecs_service" "app" {
  name            = "${var.project_name}-${var.environment}"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.app.arn
  desired_count   = var.desired_count
  launch_type     = "FARGATE"
  
  platform_version = "1.4.0"
  
  network_configuration {
    subnets          = module.vpc.private_subnet_ids
    security_groups  = [aws_security_group.ecs_tasks.id]
    assign_public_ip = false
  }
  
  load_balancer {
    target_group_arn = aws_lb_target_group.app.arn
    container_name   = "app"
    container_port   = var.container_port
  }
  
  deployment_configuration {
    maximum_percent         = 200
    minimum_healthy_percent = 100
    
    deployment_circuit_breaker {
      enable   = true
      rollback = true
    }
  }
  
  enable_execute_command = true
  
  depends_on = [
    aws_lb_listener.app,
    aws_iam_role_policy_attachment.ecs_execution_role_policy
  ]
  
  tags = local.common_tags
}

# Security group for ECS tasks
resource "aws_security_group" "ecs_tasks" {
  name_prefix = "${var.project_name}-${var.environment}-ecs-tasks"
  vpc_id      = module.vpc.vpc_id
  
  ingress {
    protocol        = "tcp"
    from_port       = var.container_port
    to_port         = var.container_port
    security_groups = [aws_security_group.alb.id]
    description     = "Allow inbound from ALB"
  }
  
  egress {
    protocol    = "-1"
    from_port   = 0
    to_port     = 0
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound traffic"
  }
  
  tags = merge(local.common_tags, {
    Name = "${var.project_name}-${var.environment}-ecs-tasks"
  })
}

# Application Load Balancer with security configurations
resource "aws_lb" "app" {
  name               = "${var.project_name}-${var.environment}"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = module.vpc.public_subnet_ids
  
  enable_deletion_protection = var.environment == "production" ? true : false
  
  drop_invalid_header_fields = true
  
  access_logs {
    bucket  = aws_s3_bucket.alb_logs.id
    prefix  = "alb-logs"
    enabled = true
  }
  
  tags = local.common_tags
}

# WAF for application protection
resource "aws_wafv2_web_acl" "app" {
  name  = "${var.project_name}-${var.environment}"
  scope = "REGIONAL"
  
  default_action {
    allow {}
  }
  
  # AWS Managed Rules
  rule {
    name     = "AWSManagedRulesCommonRuleSet"
    priority = 1
    
    override_action {
      none {}
    }
    
    statement {
      managed_rule_group_statement {
        name        = "AWSManagedRulesCommonRuleSet"
        vendor_name = "AWS"
      }
    }
    
    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "CommonRuleSetMetric"
      sampled_requests_enabled   = true
    }
  }
  
  rule {
    name     = "AWSManagedRulesKnownBadInputsRuleSet"
    priority = 2
    
    override_action {
      none {}
    }
    
    statement {
      managed_rule_group_statement {
        name        = "AWSManagedRulesKnownBadInputsRuleSet"
        vendor_name = "AWS"
      }
    }
    
    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "KnownBadInputsRuleSetMetric"
      sampled_requests_enabled   = true
    }
  }
  
  visibility_config {
    cloudwatch_metrics_enabled = true
    metric_name                = "${var.project_name}-${var.environment}-waf"
    sampled_requests_enabled   = true
  }
  
  tags = local.common_tags
}

# Associate WAF with ALB
resource "aws_wafv2_web_acl_association" "app" {
  resource_arn = aws_lb.app.arn
  web_acl_arn  = aws_wafv2_web_acl.app.arn
}

# CloudWatch alarms for monitoring
resource "aws_cloudwatch_metric_alarm" "high_cpu" {
  alarm_name          = "${var.project_name}-${var.environment}-high-cpu"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/ECS"
  period              = "300"
  statistic           = "Average"
  threshold           = "80"
  alarm_description   = "This metric monitors ecs cpu utilization"
  alarm_actions       = [aws_sns_topic.alerts.arn]
  
  dimensions = {
    ServiceName = aws_ecs_service.app.name
    ClusterName = aws_ecs_cluster.main.name
  }
  
  tags = local.common_tags
}

# SNS topic for alerts
resource "aws_sns_topic" "alerts" {
  name              = "${var.project_name}-${var.environment}-alerts"
  kms_master_key_id = aws_kms_key.ecs_key.arn
  
  tags = local.common_tags
}

# Local values
locals {
  common_tags = {
    Environment = var.environment
    Project     = var.project_name
    ManagedBy   = "Terraform"
  }
}

# Data sources
data "aws_caller_identity" "current" {}
data "aws_region" "current" {}
```
```
### Example 3: GitLab CI/CD pipeline with comprehensive security controls

```yaml
# .gitlab-ci.yml
stages:
  - security-scan
  - build
  - security-validation
  - deploy-staging
  - integration-tests
  - deploy-production

variables:
  DOCKER_DRIVER: overlay2
  DOCKER_TLS_CERTDIR: "/certs"
  AWS_DEFAULT_REGION: us-west-2
  ECR_REPOSITORY: $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/secure-app

# Security scanning stage
sast-scan:
  stage: security-scan
  image: python:3.9
  before_script:
    - pip install bandit safety semgrep
  script:
    - echo "Running Static Application Security Testing..."
    - bandit -r src/ -f json -o bandit-report.json || true
    - safety check --json --output safety-report.json || true
    - semgrep --config=auto --json --output=semgrep-report.json src/ || true
    - python scripts/process-sast-results.py
  artifacts:
    reports:
      sast: sast-report.json
    paths:
      - "*-report.json"
    expire_in: 1 week
  only:
    - main
    - develop
    - merge_requests

dependency-scan:
  stage: security-scan
  image: node:18
  script:
    - echo "Running dependency vulnerability scanning..."
    - npm audit --audit-level=moderate --json > npm-audit-report.json || true
    - npx audit-ci --config audit-ci.json
  artifacts:
    paths:
      - npm-audit-report.json
    expire_in: 1 week
  only:
    - main
    - develop
    - merge_requests

container-scan:
  stage: security-scan
  image: docker:latest
  services:
    - docker:dind
  before_script:
    - apk add --no-cache curl
    - curl -sSfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin
  script:
    - echo "Building container image for scanning..."
    - docker build -t temp-scan-image:latest .
    - echo "Running container security scan..."
    - trivy image --format json --output trivy-report.json temp-scan-image:latest
    - trivy image --exit-code 1 --severity HIGH,CRITICAL temp-scan-image:latest
  artifacts:
    paths:
      - trivy-report.json
    expire_in: 1 week
  only:
    - main
    - develop
    - merge_requests

iac-scan:
  stage: security-scan
  image: python:3.9
  before_script:
    - pip install checkov
    - curl -s https://raw.githubusercontent.com/aquasecurity/tfsec/master/scripts/install_linux.sh | bash
  script:
    - echo "Running Infrastructure as Code security scanning..."
    - checkov -d infrastructure/ --framework terraform --output json --output-file checkov-report.json || true
    - tfsec infrastructure/ --format json --out tfsec-report.json || true
    - python scripts/process-iac-results.py
  artifacts:
    paths:
      - "*-report.json"
    expire_in: 1 week
  only:
    - main
    - develop
    - merge_requests

# Build stage
build-application:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  before_script:
    - apk add --no-cache aws-cli
    - aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $ECR_REPOSITORY
  script:
    - echo "Building application container..."
    - export IMAGE_TAG=${CI_COMMIT_SHORT_SHA}
    - docker build -t $ECR_REPOSITORY:$IMAGE_TAG .
    - docker tag $ECR_REPOSITORY:$IMAGE_TAG $ECR_REPOSITORY:latest
    - echo "Pushing container to ECR..."
    - docker push $ECR_REPOSITORY:$IMAGE_TAG
    - docker push $ECR_REPOSITORY:latest
    - echo "IMAGE_TAG=$IMAGE_TAG" > build.env
  artifacts:
    reports:
      dotenv: build.env
  dependencies:
    - sast-scan
    - dependency-scan
    - container-scan
    - iac-scan
  only:
    - main
    - develop

# Security validation stage
security-validation:
  stage: security-validation
  image: python:3.9
  before_script:
    - pip install boto3 requests
  script:
    - echo "Running comprehensive security validation..."
    - python scripts/security-gate-validation.py
    - echo "Security validation completed successfully"
  dependencies:
    - build-application
  only:
    - main
    - develop

# Staging deployment
deploy-staging:
  stage: deploy-staging
  image: 
    name: hashicorp/terraform:1.5
    entrypoint: [""]
  before_script:
    - apk add --no-cache aws-cli
    - terraform --version
    - aws --version
  script:
    - echo "Deploying to staging environment..."
    - cd infrastructure/
    - terraform init
    - terraform workspace select staging || terraform workspace new staging
    - terraform plan -var="environment=staging" -var="image_tag=$IMAGE_TAG" -out=staging.tfplan
    - terraform apply -auto-approve staging.tfplan
    - echo "Staging deployment completed"
  environment:
    name: staging
    url: https://staging.example.com
  dependencies:
    - security-validation
  only:
    - main
    - develop

# Integration tests
integration-tests:
  stage: integration-tests
  image: python:3.9
  before_script:
    - pip install pytest requests
  script:
    - echo "Running integration tests against staging..."
    - python -m pytest tests/integration/ --staging-url=https://staging.example.com
    - echo "Integration tests completed successfully"
  dependencies:
    - deploy-staging
  only:
    - main
    - develop

# Production deployment (manual approval required)
deploy-production:
  stage: deploy-production
  image:
    name: hashicorp/terraform:1.5
    entrypoint: [""]
  before_script:
    - apk add --no-cache aws-cli
  script:
    - echo "Deploying to production environment..."
    - cd infrastructure/
    - terraform init
    - terraform workspace select production || terraform workspace new production
    - terraform plan -var="environment=production" -var="image_tag=$IMAGE_TAG" -out=production.tfplan
    - terraform apply -auto-approve production.tfplan
    - echo "Production deployment completed"
    - python ../scripts/post-deployment-validation.py --environment=production
  environment:
    name: production
    url: https://app.example.com
  when: manual
  dependencies:
    - integration-tests
  only:
    - main
```

```python
# scripts/security-gate-validation.py
import json
import sys
import os
from typing import Dict, List, Any

class SecurityGateValidator:
    def __init__(self):
        self.security_thresholds = {
            'critical_vulnerabilities': 0,
            'high_vulnerabilities': 5,
            'medium_vulnerabilities': 20,
            'sast_critical_issues': 0,
            'sast_high_issues': 3,
            'dependency_critical': 0,
            'dependency_high': 5,
            'iac_critical_issues': 0,
            'iac_high_issues': 2
        }
        
        self.validation_results = {
            'passed': True,
            'violations': [],
            'summary': {}
        }
    
    def validate_security_reports(self):
        """Validate all security scan reports against thresholds"""
        
        print("Starting security gate validation...")
        
        # Validate SAST results
        self.validate_sast_results()
        
        # Validate dependency scan results
        self.validate_dependency_results()
        
        # Validate container scan results
        self.validate_container_results()
        
        # Validate IaC scan results
        self.validate_iac_results()
        
        # Generate final report
        self.generate_validation_report()
        
        # Exit with appropriate code
        if not self.validation_results['passed']:
            print("❌ Security gate validation FAILED")
            sys.exit(1)
        else:
            print("✅ Security gate validation PASSED")
            sys.exit(0)
    
    def validate_sast_results(self):
        """Validate Static Application Security Testing results"""
        
        print("Validating SAST results...")
        
        # Process Bandit results
        if os.path.exists('bandit-report.json'):
            with open('bandit-report.json', 'r') as f:
                bandit_data = json.load(f)
                
            high_issues = len([r for r in bandit_data.get('results', []) 
                             if r.get('issue_severity') == 'HIGH'])
            critical_issues = len([r for r in bandit_data.get('results', []) 
                                 if r.get('issue_severity') == 'CRITICAL'])
            
            if critical_issues > self.security_thresholds['sast_critical_issues']:
                self.validation_results['violations'].append({
                    'type': 'SAST_CRITICAL_ISSUES',
                    'count': critical_issues,
                    'threshold': self.security_thresholds['sast_critical_issues'],
                    'tool': 'Bandit'
                })
                self.validation_results['passed'] = False
            
            if high_issues > self.security_thresholds['sast_high_issues']:
                self.validation_results['violations'].append({
                    'type': 'SAST_HIGH_ISSUES',
                    'count': high_issues,
                    'threshold': self.security_thresholds['sast_high_issues'],
                    'tool': 'Bandit'
                })
                self.validation_results['passed'] = False
        
        # Process Semgrep results
        if os.path.exists('semgrep-report.json'):
            with open('semgrep-report.json', 'r') as f:
                semgrep_data = json.load(f)
            
            critical_findings = len([r for r in semgrep_data.get('results', []) 
                                   if r.get('extra', {}).get('severity') == 'ERROR'])
            
            if critical_findings > self.security_thresholds['sast_critical_issues']:
                self.validation_results['violations'].append({
                    'type': 'SAST_CRITICAL_ISSUES',
                    'count': critical_findings,
                    'threshold': self.security_thresholds['sast_critical_issues'],
                    'tool': 'Semgrep'
                })
                self.validation_results['passed'] = False
    
    def validate_dependency_results(self):
        """Validate dependency vulnerability scan results"""
        
        print("Validating dependency scan results...")
        
        if os.path.exists('npm-audit-report.json'):
            with open('npm-audit-report.json', 'r') as f:
                audit_data = json.load(f)
            
            vulnerabilities = audit_data.get('vulnerabilities', {})
            
            critical_count = 0
            high_count = 0
            
            for vuln_name, vuln_data in vulnerabilities.items():
                severity = vuln_data.get('severity', '').lower()
                if severity == 'critical':
                    critical_count += 1
                elif severity == 'high':
                    high_count += 1
            
            if critical_count > self.security_thresholds['dependency_critical']:
                self.validation_results['violations'].append({
                    'type': 'DEPENDENCY_CRITICAL_VULNERABILITIES',
                    'count': critical_count,
                    'threshold': self.security_thresholds['dependency_critical'],
                    'tool': 'npm audit'
                })
                self.validation_results['passed'] = False
            
            if high_count > self.security_thresholds['dependency_high']:
                self.validation_results['violations'].append({
                    'type': 'DEPENDENCY_HIGH_VULNERABILITIES',
                    'count': high_count,
                    'threshold': self.security_thresholds['dependency_high'],
                    'tool': 'npm audit'
                })
                self.validation_results['passed'] = False
    
    def validate_container_results(self):
        """Validate container security scan results"""
        
        print("Validating container scan results...")
        
        if os.path.exists('trivy-report.json'):
            with open('trivy-report.json', 'r') as f:
                trivy_data = json.load(f)
            
            critical_count = 0
            high_count = 0
            
            for result in trivy_data.get('Results', []):
                for vuln in result.get('Vulnerabilities', []):
                    severity = vuln.get('Severity', '').upper()
                    if severity == 'CRITICAL':
                        critical_count += 1
                    elif severity == 'HIGH':
                        high_count += 1
            
            if critical_count > self.security_thresholds['critical_vulnerabilities']:
                self.validation_results['violations'].append({
                    'type': 'CONTAINER_CRITICAL_VULNERABILITIES',
                    'count': critical_count,
                    'threshold': self.security_thresholds['critical_vulnerabilities'],
                    'tool': 'Trivy'
                })
                self.validation_results['passed'] = False
            
            if high_count > self.security_thresholds['high_vulnerabilities']:
                self.validation_results['violations'].append({
                    'type': 'CONTAINER_HIGH_VULNERABILITIES',
                    'count': high_count,
                    'threshold': self.security_thresholds['high_vulnerabilities'],
                    'tool': 'Trivy'
                })
                self.validation_results['passed'] = False
    
    def validate_iac_results(self):
        """Validate Infrastructure as Code scan results"""
        
        print("Validating IaC scan results...")
        
        # Process Checkov results
        if os.path.exists('checkov-report.json'):
            with open('checkov-report.json', 'r') as f:
                checkov_data = json.load(f)
            
            failed_checks = checkov_data.get('results', {}).get('failed_checks', [])
            
            critical_issues = len([c for c in failed_checks 
                                 if c.get('severity') == 'CRITICAL'])
            high_issues = len([c for c in failed_checks 
                             if c.get('severity') == 'HIGH'])
            
            if critical_issues > self.security_thresholds['iac_critical_issues']:
                self.validation_results['violations'].append({
                    'type': 'IAC_CRITICAL_ISSUES',
                    'count': critical_issues,
                    'threshold': self.security_thresholds['iac_critical_issues'],
                    'tool': 'Checkov'
                })
                self.validation_results['passed'] = False
            
            if high_issues > self.security_thresholds['iac_high_issues']:
                self.validation_results['violations'].append({
                    'type': 'IAC_HIGH_ISSUES',
                    'count': high_issues,
                    'threshold': self.security_thresholds['iac_high_issues'],
                    'tool': 'Checkov'
                })
                self.validation_results['passed'] = False
        
        # Process tfsec results
        if os.path.exists('tfsec-report.json'):
            with open('tfsec-report.json', 'r') as f:
                tfsec_data = json.load(f)
            
            critical_issues = len([r for r in tfsec_data.get('results', []) 
                                 if r.get('severity') == 'CRITICAL'])
            high_issues = len([r for r in tfsec_data.get('results', []) 
                             if r.get('severity') == 'HIGH'])
            
            if critical_issues > self.security_thresholds['iac_critical_issues']:
                self.validation_results['violations'].append({
                    'type': 'IAC_CRITICAL_ISSUES',
                    'count': critical_issues,
                    'threshold': self.security_thresholds['iac_critical_issues'],
                    'tool': 'tfsec'
                })
                self.validation_results['passed'] = False
    
    def generate_validation_report(self):
        """Generate comprehensive validation report"""
        
        print("\n" + "="*60)
        print("SECURITY GATE VALIDATION REPORT")
        print("="*60)
        
        if self.validation_results['passed']:
            print("✅ Overall Status: PASSED")
        else:
            print("❌ Overall Status: FAILED")
        
        print(f"\nViolations Found: {len(self.validation_results['violations'])}")
        
        if self.validation_results['violations']:
            print("\nViolation Details:")
            for violation in self.validation_results['violations']:
                print(f"  - {violation['type']}: {violation['count']} "
                      f"(threshold: {violation['threshold']}) - {violation['tool']}")
        
        print("\nSecurity Thresholds:")
        for threshold, value in self.security_thresholds.items():
            print(f"  - {threshold}: {value}")
        
        print("="*60)
        
        # Save detailed report
        with open('security-gate-report.json', 'w') as f:
            json.dump(self.validation_results, f, indent=2)

if __name__ == "__main__":
    validator = SecurityGateValidator()
    validator.validate_security_reports()
```
### Example 4: Kubernetes deployment with GitOps and security controls

```yaml
# k8s-deployment/base/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: secure-app
  labels:
    app: secure-app
    version: v1
spec:
  replicas: 3
  selector:
    matchLabels:
      app: secure-app
  template:
    metadata:
      labels:
        app: secure-app
        version: v1
      annotations:
        # Security annotations
        container.apparmor.security.beta.kubernetes.io/app: runtime/default
        seccomp.security.alpha.kubernetes.io/pod: runtime/default
    spec:
      serviceAccountName: secure-app-sa
      automountServiceAccountToken: false
      
      # Security context for the pod
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        runAsGroup: 1000
        fsGroup: 1000
        seccompProfile:
          type: RuntimeDefault
      
      containers:
      - name: app
        image: 123456789012.dkr.ecr.us-west-2.amazonaws.com/secure-app:latest
        imagePullPolicy: Always
        
        ports:
        - containerPort: 8080
          name: http
          protocol: TCP
        
        # Security context for the container
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          runAsNonRoot: true
          runAsUser: 1000
          runAsGroup: 1000
          capabilities:
            drop:
            - ALL
            add:
            - NET_BIND_SERVICE
        
        # Resource limits
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        
        # Health checks
        livenessProbe:
          httpGet:
            path: /health
            port: http
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        
        readinessProbe:
          httpGet:
            path: /ready
            port: http
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
        
        # Environment variables
        env:
        - name: PORT
          value: "8080"
        - name: ENVIRONMENT
          value: "production"
        
        # Secrets from AWS Secrets Manager
        envFrom:
        - secretRef:
            name: app-secrets
        
        # Volume mounts for writable directories
        volumeMounts:
        - name: tmp-volume
          mountPath: /tmp
        - name: cache-volume
          mountPath: /app/cache
      
      volumes:
      - name: tmp-volume
        emptyDir: {}
      - name: cache-volume
        emptyDir: {}
      
      # Node selection and affinity
      nodeSelector:
        kubernetes.io/os: linux
      
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchExpressions:
                - key: app
                  operator: In
                  values:
                  - secure-app
              topologyKey: kubernetes.io/hostname

---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: secure-app-sa
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::123456789012:role/SecureAppRole
automountServiceAccountToken: false

---
apiVersion: v1
kind: Service
metadata:
  name: secure-app-service
  labels:
    app: secure-app
spec:
  type: ClusterIP
  ports:
  - port: 80
    targetPort: http
    protocol: TCP
    name: http
  selector:
    app: secure-app

---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: secure-app-network-policy
spec:
  podSelector:
    matchLabels:
      app: secure-app
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to: []
    ports:
    - protocol: TCP
      port: 443  # HTTPS
    - protocol: TCP
      port: 53   # DNS
    - protocol: UDP
      port: 53   # DNS

---
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: secure-app-pdb
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: secure-app
```

```yaml
# .github/workflows/gitops-deployment.yml
name: GitOps Deployment with Security

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

env:
  AWS_REGION: us-west-2
  EKS_CLUSTER_NAME: secure-cluster
  ECR_REPOSITORY: secure-app

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Run Kubernetes security scan
      uses: azure/k8s-lint@v1
      with:
        manifests: |
          k8s-deployment/base/deployment.yaml
    
    - name: Run Polaris security scan
      run: |
        curl -L https://github.com/FairwindsOps/polaris/releases/latest/download/polaris_linux_amd64.tar.gz | tar xz
        ./polaris audit --audit-path k8s-deployment/ --format json > polaris-report.json
    
    - name: Run Falco rules validation
      run: |
        docker run --rm -v $(pwd):/workspace falcosecurity/falco:latest \
          falco --validate /workspace/security/falco-rules.yaml
    
    - name: Upload security reports
      uses: actions/upload-artifact@v3
      with:
        name: k8s-security-reports
        path: "*-report.json"

  build-and-push:
    needs: security-scan
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v2
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: ${{ env.AWS_REGION }}
    
    - name: Login to Amazon ECR
      id: login-ecr
      uses: aws-actions/amazon-ecr-login@v1
    
    - name: Build, tag, and push image to Amazon ECR
      env:
        ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
        IMAGE_TAG: ${{ github.sha }}
      run: |
        docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
        docker tag $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG $ECR_REGISTRY/$ECR_REPOSITORY:latest
        docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
        docker push $ECR_REGISTRY/$ECR_REPOSITORY:latest
        echo "IMAGE_URI=$ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG" >> $GITHUB_OUTPUT
    
    outputs:
      image-uri: ${{ steps.build-and-push.outputs.IMAGE_URI }}

  update-manifests:
    needs: build-and-push
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout GitOps repository
      uses: actions/checkout@v3
      with:
        repository: company/gitops-manifests
        token: ${{ secrets.GITOPS_TOKEN }}
        path: gitops-repo
    
    - name: Update Kubernetes manifests
      env:
        IMAGE_URI: ${{ needs.build-and-push.outputs.image-uri }}
      run: |
        cd gitops-repo
        
        # Update image in Kustomization
        sed -i "s|newTag:.*|newTag: ${GITHUB_SHA}|g" overlays/production/kustomization.yaml
        
        # Commit and push changes
        git config user.name "GitHub Actions"
        git config user.email "actions@github.com"
        git add .
        git commit -m "Update secure-app image to ${GITHUB_SHA}"
        git push

  deploy-staging:
    needs: [security-scan, build-and-push]
    runs-on: ubuntu-latest
    environment: staging
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v2
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: ${{ env.AWS_REGION }}
    
    - name: Update kubeconfig
      run: |
        aws eks update-kubeconfig --region ${{ env.AWS_REGION }} --name ${{ env.EKS_CLUSTER_NAME }}-staging
    
    - name: Deploy to staging
      env:
        IMAGE_URI: ${{ needs.build-and-push.outputs.image-uri }}
      run: |
        # Update image in deployment
        sed -i "s|image:.*|image: ${IMAGE_URI}|g" k8s-deployment/overlays/staging/deployment.yaml
        
        # Apply manifests
        kubectl apply -k k8s-deployment/overlays/staging/
        
        # Wait for rollout to complete
        kubectl rollout status deployment/secure-app -n staging --timeout=300s
        
        # Run post-deployment security checks
        kubectl run security-check --rm -i --restart=Never --image=aquasec/kube-bench:latest -- --version 1.20
    
    - name: Run integration tests
      run: |
        # Get service endpoint
        STAGING_URL=$(kubectl get service secure-app-service -n staging -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
        
        # Run integration tests
        python tests/integration_tests.py --url http://${STAGING_URL}

  security-validation:
    needs: deploy-staging
    runs-on: ubuntu-latest
    
    steps:
    - name: Run runtime security validation
      run: |
        # Run Falco for runtime security monitoring
        kubectl apply -f https://raw.githubusercontent.com/falcosecurity/falco/master/examples/k8s_audit_config/falco-k8s-audit-rules.yaml
        
        # Check for security policy violations
        kubectl get events --field-selector type=Warning -n staging
        
        # Validate network policies
        kubectl describe networkpolicy secure-app-network-policy -n staging

  deploy-production:
    needs: [deploy-staging, security-validation]
    runs-on: ubuntu-latest
    environment: production
    if: github.ref == 'refs/heads/main'
    
    steps:
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v2
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: ${{ env.AWS_REGION }}
    
    - name: Update kubeconfig
      run: |
        aws eks update-kubeconfig --region ${{ env.AWS_REGION }} --name ${{ env.EKS_CLUSTER_NAME }}-production
    
    - name: Deploy to production with canary
      env:
        IMAGE_URI: ${{ needs.build-and-push.outputs.image-uri }}
      run: |
        # Deploy canary version (10% traffic)
        kubectl patch deployment secure-app -p '{"spec":{"template":{"spec":{"containers":[{"name":"app","image":"'${IMAGE_URI}'"}]}}}}'
        kubectl patch deployment secure-app -p '{"spec":{"replicas":1}}'
        
        # Wait for canary deployment
        kubectl rollout status deployment/secure-app --timeout=300s
        
        # Monitor canary metrics for 5 minutes
        sleep 300
        
        # Check error rates and performance metrics
        python scripts/validate-canary-metrics.py
        
        # If validation passes, complete the rollout
        kubectl patch deployment secure-app -p '{"spec":{"replicas":3}}'
        kubectl rollout status deployment/secure-app --timeout=300s
    
    - name: Post-deployment validation
      run: |
        # Validate deployment health
        kubectl get pods -l app=secure-app -n production
        
        # Check security compliance
        kubectl run compliance-check --rm -i --restart=Never --image=aquasec/kube-bench:latest
        
        # Validate network policies are active
        kubectl describe networkpolicy secure-app-network-policy -n production
        
        # Send deployment notification
        curl -X POST ${{ secrets.SLACK_WEBHOOK_URL }} \
          -H 'Content-type: application/json' \
          --data '{"text":"✅ Production deployment completed successfully for commit '${{ github.sha }}'"}'
```

## AWS services to consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS CodePipeline</h4>
    <p>Fully managed continuous delivery service that helps you automate your release pipelines for fast and reliable application and infrastructure updates.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS CodeBuild</h4>
    <p>Fully managed continuous integration service that compiles source code, runs tests, and produces software packages that are ready to deploy.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS CodeDeploy</h4>
    <p>Deployment service that automates application deployments to Amazon EC2 instances, on-premises instances, serverless Lambda functions, or Amazon ECS services.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS CloudFormation</h4>
    <p>Infrastructure as code service that helps you model and set up your Amazon Web Services resources using templates.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS CDK</h4>
    <p>Open-source software development framework to define cloud infrastructure in code and provision it through AWS CloudFormation.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon ECS</h4>
    <p>Fully managed container orchestration service that makes it easy to deploy, manage, and scale containerized applications.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon EKS</h4>
    <p>Managed Kubernetes service that makes it easy to run Kubernetes on AWS without needing to install and operate your own Kubernetes clusters.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Systems Manager</h4>
    <p>Management service that helps you automatically collect software inventory, apply OS patches, create system images, and configure Windows and Linux operating systems.</p>
  </div>
</div>

## Benefits of deploying software programmatically

- **Consistency and reliability**: Eliminates human error and ensures reproducible deployments
- **Enhanced security**: Enables automated security controls and compliance validation
- **Faster time to market**: Accelerates deployment cycles through automation
- **Improved auditability**: Provides complete audit trails and deployment history
- **Risk reduction**: Enables automated rollback and disaster recovery procedures
- **Scalability**: Supports deployment across multiple environments and regions
- **Cost optimization**: Reduces manual effort and operational overhead
- **Compliance support**: Ensures consistent application of security and governance policies

## Related resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/sec_appsec_deploy_software_programmatically.html">AWS Well-Architected Framework - Deploy software programmatically</a></li>
    <li><a href="https://docs.aws.amazon.com/codepipeline/latest/userguide/welcome.html">AWS CodePipeline User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/codebuild/latest/userguide/welcome.html">AWS CodeBuild User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/codedeploy/latest/userguide/welcome.html">AWS CodeDeploy User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/cdk/v2/guide/home.html">AWS CDK Developer Guide</a></li>
    <li><a href="https://aws.amazon.com/blogs/devops/implementing-gitops-with-aws-codepipeline/">Implementing GitOps with AWS CodePipeline</a></li>
    <li><a href="https://aws.amazon.com/blogs/containers/securing-amazon-eks-with-aws-app-mesh-and-aws-x-ray/">Securing Amazon EKS with AWS App Mesh and AWS X-Ray</a></li>
  </ul>
</div>
