---
title: SEC06-BP03 - Reduce manual management and interactive access
layout: default
parent: SEC06 - How do you protect your compute resources?
grand_parent: Security
nav_order: 3
---

<div class="pillar-header">
  <h1>SEC06-BP03: Reduce manual management and interactive access</h1>
  <p>Reduce the risk of human error and the potential for configuration drift by replacing manual processes with automated processes where possible. Reduce interactive access to compute resources, for example, by using change management workflows to manage EC2 instances, and by using tools such as Amazon EC2 Systems Manager Session Manager instead of allowing direct access or bastion hosts.</p>
</div>

## Implementation guidance

Reducing manual management and interactive access is crucial for maintaining a secure and consistent compute environment. By minimizing human interaction with production systems, you can significantly reduce the risk of security incidents, configuration errors, and unauthorized access while improving operational efficiency and compliance.

### Key steps for implementing this best practice:

1. **Implement Infrastructure as Code (IaC)**:
   - Use AWS CloudFormation or AWS CDK for infrastructure provisioning
   - Version control all infrastructure definitions
   - Implement automated testing for infrastructure changes
   - Establish code review processes for infrastructure modifications
   - Use immutable infrastructure patterns where possible

2. **Automate configuration management**:
   - Use AWS Systems Manager for configuration management
   - Implement configuration drift detection and remediation
   - Automate software installation and updates
   - Use desired state configuration tools
   - Establish configuration baselines and compliance monitoring

3. **Replace interactive access with secure alternatives**:
   - Use AWS Systems Manager Session Manager for secure shell access
   - Implement break-glass procedures for emergency access
   - Use AWS Systems Manager Run Command for remote execution
   - Eliminate SSH key management where possible
   - Implement just-in-time access for administrative tasks

4. **Implement automated deployment pipelines**:
   - Use CI/CD pipelines for application deployments
   - Implement blue-green or canary deployment strategies
   - Automate rollback procedures for failed deployments
   - Use container orchestration for application management
   - Implement automated testing and validation in pipelines

5. **Establish monitoring and alerting for manual access**:
   - Monitor and log all interactive access attempts
   - Set up alerts for unauthorized or unusual access patterns
   - Implement session recording for audit purposes
   - Track and report on manual interventions
   - Establish metrics for automation coverage

6. **Implement change management workflows**:
   - Use ticketing systems for change requests
   - Implement approval workflows for infrastructure changes
   - Establish emergency change procedures
   - Document all changes and their business justification
   - Implement automated change validation and testing

## Implementation examples

### Example 1: AWS Systems Manager Session Manager configuration

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'AWS Systems Manager Session Manager configuration for secure access'

Resources:
  # IAM role for EC2 instances to use Session Manager
  SessionManagerInstanceRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: ec2.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore
      Policies:
        - PolicyName: SessionManagerLogging
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - logs:CreateLogGroup
                  - logs:CreateLogStream
                  - logs:PutLogEvents
                  - logs:DescribeLogStreams
                Resource: '*'
              - Effect: Allow
                Action:
                  - s3:PutObject
                  - s3:GetEncryptionConfiguration
                Resource: 
                  - !Sub '${SessionManagerLogsBucket}/*'

  # Instance profile for EC2 instances
  SessionManagerInstanceProfile:
    Type: AWS::IAM::InstanceProfile
    Properties:
      Roles:
        - !Ref SessionManagerInstanceRole

  # S3 bucket for session logs
  SessionManagerLogsBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub 'session-manager-logs-${AWS::AccountId}-${AWS::Region}'
      BucketEncryption:
        ServerSideEncryptionConfiguration:
          - ServerSideEncryptionByDefault:
              SSEAlgorithm: AES256
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true
      LifecycleConfiguration:
        Rules:
          - Id: SessionLogsRetention
            Status: Enabled
            ExpirationInDays: 90

  # CloudWatch Log Group for session logs
  SessionManagerLogGroup:
    Type: AWS::Logs::LogGroup
    Properties:
      LogGroupName: '/aws/sessionmanager/sessions'
      RetentionInDays: 90

  # Session Manager preferences document
  SessionManagerPreferences:
    Type: AWS::SSM::Document
    Properties:
      DocumentType: Session
      DocumentFormat: JSON
      Content:
        schemaVersion: '1.0'
        description: 'Session Manager preferences for secure access'
        sessionType: Standard_Stream
        inputs:
          s3BucketName: !Ref SessionManagerLogsBucket
          s3KeyPrefix: 'session-logs/'
          s3EncryptionEnabled: true
          cloudWatchLogGroupName: !Ref SessionManagerLogGroup
          cloudWatchEncryptionEnabled: true
          idleSessionTimeout: '20'
          maxSessionDuration: '60'
          runAsEnabled: false
          runAsDefaultUser: 'ssm-user'
          shellProfile:
            windows: 'powershell'
            linux: |
              # Configure secure shell environment
              export HISTSIZE=1000
              export HISTFILESIZE=1000
              export HISTCONTROL=ignoredups:erasedups
              
              # Set secure umask
              umask 027
              
              # Display security banner
              echo "==============================================="
              echo "  AUTHORIZED ACCESS ONLY"
              echo "  All activities are logged and monitored"
              echo "==============================================="
              
              # Set PS1 to show session info
              export PS1="[SSM-Session] \u@\h:\w$ "

  # IAM policy for users to access Session Manager
  SessionManagerUserPolicy:
    Type: AWS::IAM::ManagedPolicy
    Properties:
      ManagedPolicyName: SessionManagerUserAccess
      Description: 'Policy for users to access Session Manager'
      PolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Action:
              - ssm:StartSession
            Resource:
              - 'arn:aws:ec2:*:*:instance/*'
            Condition:
              StringEquals:
                'ssm:resourceTag/Environment': ['Development', 'Staging']
          - Effect: Allow
            Action:
              - ssm:StartSession
            Resource:
              - !Sub 'arn:aws:ssm:*:*:document/${SessionManagerPreferences}'
          - Effect: Allow
            Action:
              - ssm:DescribeSessions
              - ssm:GetConnectionStatus
              - ssm:DescribeInstanceInformation
              - ssm:DescribeInstanceProperties
              - ec2:DescribeInstances
            Resource: '*'

  # CloudWatch alarm for unusual session activity
  UnusualSessionActivityAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: 'UnusualSessionManagerActivity'
      AlarmDescription: 'Alert on unusual Session Manager activity'
      MetricName: 'SessionCount'
      Namespace: 'AWS/SSM-SessionManager'
      Statistic: Sum
      Period: 300
      EvaluationPeriods: 2
      Threshold: 10
      ComparisonOperator: GreaterThanThreshold
      AlarmActions:
        - !Ref SecurityAlertsTopic

  # SNS topic for security alerts
  SecurityAlertsTopic:
    Type: AWS::SNS::Topic
    Properties:
      TopicName: 'SessionManagerSecurityAlerts'
      DisplayName: 'Session Manager Security Alerts'

Outputs:
  SessionManagerInstanceRoleArn:
    Description: 'ARN of the Session Manager instance role'
    Value: !GetAtt SessionManagerInstanceRole.Arn
    Export:
      Name: !Sub '${AWS::StackName}-SessionManager-Role'

  SessionManagerLogsBucket:
    Description: 'S3 bucket for Session Manager logs'
    Value: !Ref SessionManagerLogsBucket
    Export:
      Name: !Sub '${AWS::StackName}-SessionManager-Logs-Bucket'
```

### Example 2: Automated configuration management with Systems Manager

```python
import boto3
import json
from datetime import datetime

def create_configuration_automation():
    """Create Systems Manager automation for configuration management"""
    
    ssm = boto3.client('ssm')
    
    # Create automation document for server hardening
    automation_document = {
        "schemaVersion": "0.3",
        "description": "Automated server hardening configuration",
        "assumeRole": "{{ AutomationAssumeRole }}",
        "parameters": {
            "InstanceId": {
                "type": "String",
                "description": "EC2 Instance ID to configure"
            },
            "AutomationAssumeRole": {
                "type": "String",
                "description": "IAM role for automation execution"
            }
        },
        "mainSteps": [
            {
                "name": "UpdateSystem",
                "action": "aws:runCommand",
                "inputs": {
                    "DocumentName": "AWS-RunShellScript",
                    "InstanceIds": ["{{ InstanceId }}"],
                    "Parameters": {
                        "commands": [
                            "#!/bin/bash",
                            "yum update -y",
                            "echo 'System updated successfully'"
                        ]
                    }
                }
            },
            {
                "name": "ConfigureFirewall",
                "action": "aws:runCommand",
                "inputs": {
                    "DocumentName": "AWS-RunShellScript",
                    "InstanceIds": ["{{ InstanceId }}"],
                    "Parameters": {
                        "commands": [
                            "#!/bin/bash",
                            "systemctl enable firewalld",
                            "systemctl start firewalld",
                            "firewall-cmd --permanent --remove-service=ssh",
                            "firewall-cmd --permanent --add-port=22/tcp --source=10.0.0.0/8",
                            "firewall-cmd --reload",
                            "echo 'Firewall configured successfully'"
                        ]
                    }
                }
            },
            {
                "name": "ConfigureAuditLogging",
                "action": "aws:runCommand",
                "inputs": {
                    "DocumentName": "AWS-RunShellScript",
                    "InstanceIds": ["{{ InstanceId }}"],
                    "Parameters": {
                        "commands": [
                            "#!/bin/bash",
                            "systemctl enable auditd",
                            "systemctl start auditd",
                            "echo 'Audit logging configured successfully'"
                        ]
                    }
                }
            },
            {
                "name": "ValidateConfiguration",
                "action": "aws:runCommand",
                "inputs": {
                    "DocumentName": "AWS-RunShellScript",
                    "InstanceIds": ["{{ InstanceId }}"],
                    "Parameters": {
                        "commands": [
                            "#!/bin/bash",
                            "echo 'Validating configuration...'",
                            "systemctl is-active firewalld",
                            "systemctl is-active auditd",
                            "echo 'Configuration validation completed'"
                        ]
                    }
                }
            }
        ]
    }
    
    try:
        response = ssm.create_document(
            Content=json.dumps(automation_document),
            Name='ServerHardeningAutomation',
            DocumentType='Automation',
            DocumentFormat='JSON',
            Tags=[
                {
                    'Key': 'Purpose',
                    'Value': 'ServerHardening'
                },
                {
                    'Key': 'Automation',
                    'Value': 'true'
                }
            ]
        )
        
        print(f"Created automation document: {response['DocumentDescription']['Name']}")
        return response['DocumentDescription']['Name']
        
    except Exception as e:
        print(f"Error creating automation document: {str(e)}")
        return None

def create_maintenance_window():
    """Create maintenance window for automated configuration management"""
    
    ssm = boto3.client('ssm')
    
    try:
        # Create maintenance window
        mw_response = ssm.create_maintenance_window(
            Name='ConfigurationManagementWindow',
            Description='Automated configuration management maintenance window',
            Schedule='cron(0 2 ? * SUN *)',  # Every Sunday at 2 AM
            Duration=4,
            Cutoff=1,
            AllowUnassociatedTargets=False,
            Tags=[
                {
                    'Key': 'Purpose',
                    'Value': 'ConfigurationManagement'
                }
            ]
        )
        
        window_id = mw_response['WindowId']
        
        # Create maintenance window target
        target_response = ssm.register_target_with_maintenance_window(
            WindowId=window_id,
            ResourceType='INSTANCE',
            Targets=[
                {
                    'Key': 'tag:AutomatedManagement',
                    'Values': ['true']
                }
            ],
            Name='AutomatedManagedInstances',
            Description='Instances managed through automation'
        )
        
        target_id = target_response['WindowTargetId']
        
        # Create maintenance window task
        task_response = ssm.register_task_with_maintenance_window(
            WindowId=window_id,
            TaskType='AUTOMATION',
            TaskArn='ServerHardeningAutomation',
            Targets=[
                {
                    'Key': 'WindowTargetIds',
                    'Values': [target_id]
                }
            ],
            ServiceRoleArn='arn:aws:iam::123456789012:role/MaintenanceWindowRole',
            Priority=1,
            MaxConcurrency='50%',
            MaxErrors='5',
            Name='ConfigurationHardeningTask',
            Description='Automated configuration hardening task'
        )
        
        print(f"Created maintenance window: {window_id}")
        print(f"Created maintenance window task: {task_response['WindowTaskId']}")
        
        return window_id
        
    except Exception as e:
        print(f"Error creating maintenance window: {str(e)}")
        return None

def setup_configuration_compliance():
    """Set up configuration compliance monitoring"""
    
    ssm = boto3.client('ssm')
    
    # Create compliance association for security baseline
    compliance_document = {
        "schemaVersion": "2.2",
        "description": "Security baseline compliance check",
        "parameters": {},
        "mainSteps": [
            {
                "action": "aws:runShellScript",
                "name": "SecurityBaselineCheck",
                "inputs": {
                    "runCommand": [
                        "#!/bin/bash",
                        "echo 'Running security baseline compliance check...'",
                        "",
                        "# Check if firewall is running",
                        "if systemctl is-active --quiet firewalld; then",
                        "    echo 'PASS: Firewall is active'",
                        "else",
                        "    echo 'FAIL: Firewall is not active'",
                        "    exit 1",
                        "fi",
                        "",
                        "# Check if audit logging is enabled",
                        "if systemctl is-active --quiet auditd; then",
                        "    echo 'PASS: Audit logging is active'",
                        "else",
                        "    echo 'FAIL: Audit logging is not active'",
                        "    exit 1",
                        "fi",
                        "",
                        "# Check SSH configuration",
                        "if grep -q 'PermitRootLogin no' /etc/ssh/sshd_config; then",
                        "    echo 'PASS: Root login is disabled'",
                        "else",
                        "    echo 'FAIL: Root login is not properly configured'",
                        "    exit 1",
                        "fi",
                        "",
                        "echo 'Security baseline compliance check completed successfully'"
                    ]
                }
            }
        ]
    }
    
    try:
        # Create compliance document
        doc_response = ssm.create_document(
            Content=json.dumps(compliance_document),
            Name='SecurityBaselineCompliance',
            DocumentType='Command',
            DocumentFormat='JSON'
        )
        
        # Create association for compliance checking
        association_response = ssm.create_association(
            Name='SecurityBaselineCompliance',
            Targets=[
                {
                    'Key': 'tag:AutomatedManagement',
                    'Values': ['true']
                }
            ],
            ScheduleExpression='rate(1 day)',
            ComplianceSeverity='HIGH',
            AssociationName='SecurityBaselineComplianceCheck'
        )
        
        print(f"Created compliance document: {doc_response['DocumentDescription']['Name']}")
        print(f"Created compliance association: {association_response['AssociationDescription']['AssociationId']}")
        
    except Exception as e:
        print(f"Error setting up compliance monitoring: {str(e)}")

def monitor_manual_access():
    """Set up monitoring for manual access attempts"""
    
    cloudwatch = boto3.client('cloudwatch')
    logs = boto3.client('logs')
    
    try:
        # Create CloudWatch Log Group for access monitoring
        logs.create_log_group(
            logGroupName='/aws/systems-manager/access-monitoring',
            retentionInDays=90
        )
        
        # Create metric filter for SSH access attempts
        logs.put_metric_filter(
            logGroupName='/var/log/secure',
            filterName='SSHAccessAttempts',
            filterPattern='[timestamp, hostname, process="sshd*", message="Failed password*"]',
            metricTransformations=[
                {
                    'metricName': 'SSHFailedLogins',
                    'metricNamespace': 'Security/Access',
                    'metricValue': '1',
                    'defaultValue': 0
                }
            ]
        )
        
        # Create alarm for failed SSH attempts
        cloudwatch.put_metric_alarm(
            AlarmName='HighSSHFailedLogins',
            ComparisonOperator='GreaterThanThreshold',
            EvaluationPeriods=1,
            MetricName='SSHFailedLogins',
            Namespace='Security/Access',
            Period=300,
            Statistic='Sum',
            Threshold=5.0,
            ActionsEnabled=True,
            AlarmActions=[
                'arn:aws:sns:us-west-2:123456789012:SecurityAlerts'
            ],
            AlarmDescription='Alert on high number of SSH failed login attempts'
        )
        
        print("Set up manual access monitoring successfully")
        
    except Exception as e:
        print(f"Error setting up access monitoring: {str(e)}")

# Example usage
if __name__ == "__main__":
    # Create automation infrastructure
    automation_doc = create_configuration_automation()
    if automation_doc:
        maintenance_window = create_maintenance_window()
    
    # Set up compliance monitoring
    setup_configuration_compliance()
    
    # Set up access monitoring
    monitor_manual_access()
```

### Example 3: CI/CD pipeline for infrastructure automation

```yaml
# GitHub Actions workflow for infrastructure automation
name: Infrastructure Automation

on:
  push:
    branches: [ main ]
    paths: [ 'infrastructure/**' ]
  pull_request:
    branches: [ main ]
    paths: [ 'infrastructure/**' ]

env:
  AWS_REGION: us-west-2

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v2
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: ${{ env.AWS_REGION }}
    
    - name: Validate CloudFormation templates
      run: |
        for template in infrastructure/*.yaml; do
          echo "Validating $template"
          aws cloudformation validate-template --template-body file://$template
        done
    
    - name: Run security scanning
      uses: bridgecrewio/checkov-action@master
      with:
        directory: ./infrastructure
        framework: cloudformation
        output_format: json
        quiet: true
        soft_fail: false
    
    - name: Run cost estimation
      uses: infracost/actions/setup@v2
      with:
        api-key: ${{ secrets.INFRACOST_API_KEY }}
    
    - name: Generate cost estimate
      run: |
        infracost breakdown --path=infrastructure/ \
          --format=json \
          --out-file=infracost.json
        
        infracost comment github \
          --path=infracost.json \
          --repo=$GITHUB_REPOSITORY \
          --github-token=${{ secrets.GITHUB_TOKEN }} \
          --pull-request=${{ github.event.pull_request.number }}

  deploy-staging:
    needs: validate
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
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
    
    - name: Deploy to staging
      run: |
        aws cloudformation deploy \
          --template-file infrastructure/main.yaml \
          --stack-name infrastructure-staging \
          --parameter-overrides Environment=staging \
          --capabilities CAPABILITY_IAM \
          --no-fail-on-empty-changeset
    
    - name: Run integration tests
      run: |
        # Run automated tests against staging environment
        python tests/integration_tests.py --environment=staging
    
    - name: Run security validation
      run: |
        # Validate security configurations in staging
        python tests/security_validation.py --environment=staging

  deploy-production:
    needs: deploy-staging
    runs-on: ubuntu-latest
    environment: production
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v2
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: ${{ env.AWS_REGION }}
    
    - name: Create change set
      run: |
        aws cloudformation create-change-set \
          --template-body file://infrastructure/main.yaml \
          --stack-name infrastructure-production \
          --change-set-name automated-deployment-$(date +%Y%m%d%H%M%S) \
          --parameter-overrides Environment=production \
          --capabilities CAPABILITY_IAM
    
    - name: Review change set
      run: |
        # Wait for change set creation
        aws cloudformation wait change-set-create-complete \
          --stack-name infrastructure-production \
          --change-set-name automated-deployment-$(date +%Y%m%d%H%M%S)
        
        # Describe changes
        aws cloudformation describe-change-set \
          --stack-name infrastructure-production \
          --change-set-name automated-deployment-$(date +%Y%m%d%H%M%S) \
          --query 'Changes[*].[Action,ResourceChange.LogicalResourceId,ResourceChange.ResourceType]' \
          --output table
    
    - name: Execute change set
      run: |
        aws cloudformation execute-change-set \
          --stack-name infrastructure-production \
          --change-set-name automated-deployment-$(date +%Y%m%d%H%M%S)
        
        # Wait for deployment completion
        aws cloudformation wait stack-update-complete \
          --stack-name infrastructure-production
    
    - name: Validate deployment
      run: |
        # Run post-deployment validation
        python tests/deployment_validation.py --environment=production
    
    - name: Send notification
      if: always()
      uses: 8398a7/action-slack@v3
      with:
        status: ${{ job.status }}
        channel: '#infrastructure'
        text: 'Production infrastructure deployment completed'
      env:
        SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}

  rollback:
    runs-on: ubuntu-latest
    if: failure()
    environment: production
    
    steps:
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v2
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: ${{ env.AWS_REGION }}
    
    - name: Rollback deployment
      run: |
        # Cancel any in-progress updates
        aws cloudformation cancel-update-stack \
          --stack-name infrastructure-production || true
        
        # Continue rollback if needed
        aws cloudformation continue-update-rollback \
          --stack-name infrastructure-production || true
        
        # Wait for rollback completion
        aws cloudformation wait stack-rollback-complete \
          --stack-name infrastructure-production
    
    - name: Send rollback notification
      uses: 8398a7/action-slack@v3
      with:
        status: failure
        channel: '#infrastructure'
        text: 'Production infrastructure deployment failed and was rolled back'
      env:
        SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

### Example 4: Immutable infrastructure with container orchestration

```yaml
# Kubernetes deployment with immutable infrastructure principles
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-application
  namespace: production
  labels:
    app: web-application
    version: v1.2.3
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
      maxSurge: 1
  selector:
    matchLabels:
      app: web-application
  template:
    metadata:
      labels:
        app: web-application
        version: v1.2.3
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8080"
        prometheus.io/path: "/metrics"
    spec:
      serviceAccountName: web-application-sa
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 2000
      containers:
      - name: web-application
        image: 123456789012.dkr.ecr.us-west-2.amazonaws.com/web-application:v1.2.3
        imagePullPolicy: Always
        ports:
        - containerPort: 8080
          name: http
        env:
        - name: ENVIRONMENT
          value: "production"
        - name: LOG_LEVEL
          value: "info"
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          capabilities:
            drop:
            - ALL
        volumeMounts:
        - name: tmp-volume
          mountPath: /tmp
        - name: config-volume
          mountPath: /app/config
          readOnly: true
      volumes:
      - name: tmp-volume
        emptyDir: {}
      - name: config-volume
        configMap:
          name: web-application-config
      nodeSelector:
        node-type: application
      tolerations:
      - key: "application-workload"
        operator: "Equal"
        value: "true"
        effect: "NoSchedule"

---
apiVersion: v1
kind: Service
metadata:
  name: web-application-service
  namespace: production
spec:
  selector:
    app: web-application
  ports:
  - port: 80
    targetPort: 8080
    protocol: TCP
  type: ClusterIP

---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: web-application-network-policy
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: web-application
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
  - to:
    - namespaceSelector:
        matchLabels:
          name: database
    ports:
    - protocol: TCP
      port: 5432
  - to: []
    ports:
    - protocol: TCP
      port: 443
    - protocol: UDP
      port: 53
```

## AWS services to consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Systems Manager Session Manager</h4>
    <p>Provides secure and auditable instance management without the need to open inbound ports, maintain bastion hosts, or manage SSH keys. Enables secure shell access with comprehensive logging.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Systems Manager Automation</h4>
    <p>Simplifies common maintenance and deployment tasks of Amazon EC2 instances and other AWS resources. Enables automated configuration management and reduces manual intervention.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS CodePipeline</h4>
    <p>Fully managed continuous delivery service that helps you automate your release pipelines for fast and reliable application and infrastructure updates.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS CloudFormation</h4>
    <p>Gives you an easy way to model a collection of related AWS and third-party resources. Enables Infrastructure as Code and reduces manual infrastructure management.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon ECS/EKS</h4>
    <p>Container orchestration services that eliminate the need for manual container management. Provide automated deployment, scaling, and management of containerized applications.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Config</h4>
    <p>Enables you to assess, audit, and evaluate the configurations of your AWS resources. Helps detect configuration drift and automate remediation of non-compliant resources.</p>
  </div>
</div>

## Benefits of reducing manual management and interactive access

- **Reduced human error**: Automation eliminates mistakes that can occur during manual operations and configuration changes
- **Improved security posture**: Limiting interactive access reduces the attack surface and potential for unauthorized access
- **Enhanced auditability**: Automated processes provide better audit trails and compliance evidence than manual operations
- **Increased consistency**: Automated processes ensure consistent application of configurations and security policies
- **Better scalability**: Automated management scales more effectively than manual processes as infrastructure grows
- **Faster incident response**: Automated remediation can respond to issues faster than manual intervention
- **Cost efficiency**: Reduced manual effort translates to lower operational costs and improved resource utilization

## Related resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/sec_protect_compute_reduce_manual_management.html">AWS Well-Architected Framework - Reduce manual management and interactive access</a></li>
    <li><a href="https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager.html">AWS Systems Manager Session Manager</a></li>
    <li><a href="https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-automation.html">AWS Systems Manager Automation</a></li>
    <li><a href="https://docs.aws.amazon.com/codepipeline/latest/userguide/welcome.html">AWS CodePipeline User Guide</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-record-ssh-sessions-established-through-a-bastion-host/">How to record SSH sessions established through a bastion host</a></li>
    <li><a href="https://aws.amazon.com/blogs/mt/replacing-a-bastion-host-with-amazon-ec2-systems-manager/">Replacing a bastion host with Amazon EC2 Systems Manager</a></li>
  </ul>
</div>
