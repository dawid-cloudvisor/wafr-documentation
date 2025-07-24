---
title: SEC06-BP01 - Perform vulnerability management
layout: default
parent: SEC06 - How do you protect your compute resources?
grand_parent: Security
nav_order: 1
---

<div class="pillar-header">
  <h1>SEC06-BP01: Perform vulnerability management</h1>
  <p>Frequently scan and patch for vulnerabilities in your code, dependencies, and in your infrastructure to help protect against new threats. Use automation to reduce the time between vulnerability discovery and patching. Regularly assess your applications and infrastructure for vulnerabilities and implement a process to quickly address any issues found.</p>
</div>

## Implementation guidance

Vulnerability management is a continuous process that involves identifying, evaluating, treating, and reporting on security vulnerabilities in systems and software. A comprehensive vulnerability management program helps protect your compute resources from known security weaknesses and reduces the attack surface available to potential threats.

### Key steps for implementing this best practice:

1. **Establish vulnerability scanning processes**:
   - Implement automated vulnerability scanning for all compute resources
   - Configure regular scanning schedules for different resource types
   - Use multiple scanning tools for comprehensive coverage
   - Integrate vulnerability scanning into CI/CD pipelines
   - Establish baseline security configurations and scan for deviations

2. **Implement comprehensive patch management**:
   - Create automated patch deployment processes
   - Establish patch testing procedures in non-production environments
   - Define maintenance windows for critical security patches
   - Implement rollback procedures for problematic patches
   - Track patch compliance across all systems

3. **Manage software dependencies and libraries**:
   - Maintain inventory of all software dependencies
   - Implement automated dependency vulnerability scanning
   - Establish processes for updating vulnerable dependencies
   - Use software composition analysis (SCA) tools
   - Monitor for newly disclosed vulnerabilities in dependencies

4. **Configure infrastructure vulnerability assessment**:
   - Scan infrastructure configurations for security misconfigurations
   - Implement Infrastructure as Code (IaC) security scanning
   - Assess container images for vulnerabilities
   - Monitor cloud service configurations for security issues
   - Perform regular penetration testing and security assessments

5. **Establish vulnerability prioritization and remediation**:
   - Implement risk-based vulnerability prioritization
   - Define Service Level Agreements (SLAs) for vulnerability remediation
   - Create escalation procedures for critical vulnerabilities
   - Track vulnerability metrics and remediation progress
   - Implement compensating controls for vulnerabilities that cannot be immediately patched

6. **Integrate with threat intelligence**:
   - Subscribe to vulnerability intelligence feeds
   - Monitor for exploitation of vulnerabilities in the wild
   - Prioritize vulnerabilities based on active threat campaigns
   - Implement automated threat intelligence correlation
   - Maintain awareness of emerging threats and attack techniques

## Implementation examples

### Example 1: Automated vulnerability scanning with Amazon Inspector

```python
import boto3
import json
from datetime import datetime, timedelta

def setup_inspector_vulnerability_scanning():
    """Configure Amazon Inspector for comprehensive vulnerability scanning"""
    
    inspector2 = boto3.client('inspector2')
    
    try:
        # Enable Inspector for EC2, ECR, and Lambda
        inspector2.enable(
            accountIds=[boto3.client('sts').get_caller_identity()['Account']],
            resourceTypes=['EC2', 'ECR', 'LAMBDA']
        )
        
        print("Amazon Inspector enabled for vulnerability scanning")
        
        # Configure scanning settings
        configure_inspector_settings(inspector2)
        
        # Set up automated reporting
        setup_inspector_reporting(inspector2)
        
    except Exception as e:
        print(f"Error enabling Inspector: {str(e)}")

def configure_inspector_settings(inspector2):
    """Configure Inspector scanning settings and filters"""
    
    try:
        # Create filter for high and critical vulnerabilities
        high_severity_filter = {
            'name': 'HighSeverityVulnerabilities',
            'description': 'Filter for high and critical severity vulnerabilities',
            'criteria': {
                'severity': [
                    {
                        'comparison': 'EQUALS',
                        'value': 'HIGH'
                    },
                    {
                        'comparison': 'EQUALS',
                        'value': 'CRITICAL'
                    }
                ]
            },
            'action': 'INCLUDE'
        }
        
        inspector2.create_filter(**high_severity_filter)
        
        # Create filter for production resources
        production_filter = {
            'name': 'ProductionResources',
            'description': 'Filter for production environment resources',
            'criteria': {
                'resourceTags': [
                    {
                        'comparison': 'EQUALS',
                        'key': 'Environment',
                        'value': 'Production'
                    }
                ]
            },
            'action': 'INCLUDE'
        }
        
        inspector2.create_filter(**production_filter)
        
        print("Inspector filters configured successfully")
        
    except Exception as e:
        print(f"Error configuring Inspector settings: {str(e)}")

def setup_inspector_reporting(inspector2):
    """Set up automated Inspector reporting"""
    
    try:
        # Configure finding aggregation
        inspector2.create_findings_report(
            reportFormat='JSON',
            s3Destination={
                'bucketName': 'vulnerability-reports-bucket',
                'keyPrefix': 'inspector-reports/',
                'kmsKeyArn': 'arn:aws:kms:us-west-2:123456789012:key/12345678-1234-1234-1234-123456789012'
            },
            filterCriteria={
                'severity': [
                    {
                        'comparison': 'EQUALS',
                        'value': 'HIGH'
                    },
                    {
                        'comparison': 'EQUALS',
                        'value': 'CRITICAL'
                    }
                ]
            }
        )
        
        print("Inspector reporting configured")
        
    except Exception as e:
        print(f"Error setting up Inspector reporting: {str(e)}")

def process_inspector_findings():
    """Process Inspector findings and create remediation tasks"""
    
    inspector2 = boto3.client('inspector2')
    
    try:
        # Get recent findings
        response = inspector2.list_findings(
            filterCriteria={
                'severity': [
                    {
                        'comparison': 'EQUALS',
                        'value': 'CRITICAL'
                    }
                ],
                'findingStatus': [
                    {
                        'comparison': 'EQUALS',
                        'value': 'ACTIVE'
                    }
                ]
            },
            maxResults=50
        )
        
        findings = response.get('findings', [])
        
        for finding in findings:
            # Process each finding
            process_vulnerability_finding(finding)
        
        print(f"Processed {len(findings)} critical findings")
        
    except Exception as e:
        print(f"Error processing Inspector findings: {str(e)}")

def process_vulnerability_finding(finding):
    """Process individual vulnerability finding and create remediation task"""
    
    finding_id = finding.get('findingArn')
    severity = finding.get('severity')
    title = finding.get('title')
    resource_id = finding.get('resources', [{}])[0].get('id', '')
    
    # Create remediation task based on finding type
    remediation_task = {
        'finding_id': finding_id,
        'severity': severity,
        'title': title,
        'resource_id': resource_id,
        'created_at': datetime.utcnow().isoformat(),
        'status': 'PENDING',
        'remediation_steps': generate_remediation_steps(finding)
    }
    
    # Store remediation task (e.g., in DynamoDB)
    store_remediation_task(remediation_task)
    
    # Send notification for critical findings
    if severity == 'CRITICAL':
        send_critical_vulnerability_alert(remediation_task)

def generate_remediation_steps(finding):
    """Generate specific remediation steps based on vulnerability type"""
    
    vulnerability_type = finding.get('type', '')
    package_name = finding.get('packageVulnerabilityDetails', {}).get('vulnerablePackages', [{}])[0].get('name', '')
    
    if 'PACKAGE_VULNERABILITY' in vulnerability_type:
        return [
            f"Update package {package_name} to the latest secure version",
            "Test the update in a non-production environment",
            "Deploy the update during the next maintenance window",
            "Verify the vulnerability is resolved with a follow-up scan"
        ]
    elif 'NETWORK_REACHABILITY' in vulnerability_type:
        return [
            "Review network security group rules",
            "Implement least privilege network access",
            "Consider using AWS Systems Manager Session Manager for secure access",
            "Update security group rules to restrict unnecessary access"
        ]
    else:
        return [
            "Review the vulnerability details and impact",
            "Consult vendor documentation for remediation guidance",
            "Implement appropriate security controls",
            "Schedule follow-up verification"
        ]

def store_remediation_task(task):
    """Store remediation task in DynamoDB for tracking"""
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('VulnerabilityRemediationTasks')
    
    try:
        table.put_item(Item=task)
        print(f"Stored remediation task: {task['finding_id']}")
    except Exception as e:
        print(f"Error storing remediation task: {str(e)}")

def send_critical_vulnerability_alert(task):
    """Send alert for critical vulnerability findings"""
    
    sns = boto3.client('sns')
    
    message = f"""
Critical Vulnerability Alert

Finding ID: {task['finding_id']}
Severity: {task['severity']}
Title: {task['title']}
Resource: {task['resource_id']}
Created: {task['created_at']}

Remediation Steps:
"""
    
    for step in task['remediation_steps']:
        message += f"- {step}\n"
    
    try:
        sns.publish(
            TopicArn='arn:aws:sns:us-west-2:123456789012:CriticalVulnerabilityAlerts',
            Subject=f'Critical Vulnerability: {task["title"]}',
            Message=message
        )
    except Exception as e:
        print(f"Error sending alert: {str(e)}")

# Example usage
if __name__ == "__main__":
    setup_inspector_vulnerability_scanning()
    process_inspector_findings()
```

### Example 2: Automated patch management with Systems Manager

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Automated patch management infrastructure'

Parameters:
  MaintenanceWindowSchedule:
    Type: String
    Default: 'cron(0 2 ? * SUN *)'
    Description: 'Cron expression for maintenance window (default: Sunday 2 AM)'

Resources:
  # Patch baseline for Linux systems
  LinuxPatchBaseline:
    Type: AWS::SSM::PatchBaseline
    Properties:
      Name: 'CustomLinuxPatchBaseline'
      Description: 'Custom patch baseline for Linux systems'
      OperatingSystem: 'AMAZON_LINUX_2'
      PatchGroups:
        - 'Production-Linux'
        - 'Development-Linux'
      ApprovalRules:
        PatchRules:
          - PatchFilterGroup:
              PatchFilters:
                - Key: 'PRODUCT'
                  Values: ['*']
                - Key: 'CLASSIFICATION'
                  Values: ['Security', 'Bugfix', 'Critical']
                - Key: 'SEVERITY'
                  Values: ['Critical', 'Important']
            ApproveAfterDays: 0
            ComplianceLevel: 'CRITICAL'
          - PatchFilterGroup:
              PatchFilters:
                - Key: 'PRODUCT'
                  Values: ['*']
                - Key: 'CLASSIFICATION'
                  Values: ['Security', 'Bugfix']
                - Key: 'SEVERITY'
                  Values: ['Medium', 'Low']
            ApproveAfterDays: 7
            ComplianceLevel: 'HIGH'
      ApprovedPatches: []
      RejectedPatches: []
      Tags:
        - Key: 'Name'
          Value: 'Custom-Linux-Patch-Baseline'

  # Patch baseline for Windows systems
  WindowsPatchBaseline:
    Type: AWS::SSM::PatchBaseline
    Properties:
      Name: 'CustomWindowsPatchBaseline'
      Description: 'Custom patch baseline for Windows systems'
      OperatingSystem: 'WINDOWS'
      PatchGroups:
        - 'Production-Windows'
        - 'Development-Windows'
      ApprovalRules:
        PatchRules:
          - PatchFilterGroup:
              PatchFilters:
                - Key: 'PRODUCT'
                  Values: ['WindowsServer2019', 'WindowsServer2022']
                - Key: 'CLASSIFICATION'
                  Values: ['SecurityUpdates', 'CriticalUpdates']
                - Key: 'MSRC_SEVERITY'
                  Values: ['Critical', 'Important']
            ApproveAfterDays: 0
            ComplianceLevel: 'CRITICAL'
      Tags:
        - Key: 'Name'
          Value: 'Custom-Windows-Patch-Baseline'

  # Maintenance window for patch deployment
  PatchMaintenanceWindow:
    Type: AWS::SSM::MaintenanceWindow
    Properties:
      Name: 'PatchMaintenanceWindow'
      Description: 'Maintenance window for automated patching'
      Schedule: !Ref MaintenanceWindowSchedule
      Duration: 4
      Cutoff: 1
      AllowUnassociatedTargets: false
      Tags:
        - Key: 'Name'
          Value: 'Patch-Maintenance-Window'

  # Maintenance window target for production instances
  ProductionPatchTarget:
    Type: AWS::SSM::MaintenanceWindowTarget
    Properties:
      WindowId: !Ref PatchMaintenanceWindow
      ResourceType: 'INSTANCE'
      Targets:
        - Key: 'tag:Environment'
          Values: ['Production']
        - Key: 'tag:PatchGroup'
          Values: ['Production-Linux', 'Production-Windows']
      Name: 'ProductionInstances'
      Description: 'Production instances for patching'

  # Maintenance window task for patch installation
  PatchInstallationTask:
    Type: AWS::SSM::MaintenanceWindowTask
    Properties:
      WindowId: !Ref PatchMaintenanceWindow
      TaskType: 'RUN_COMMAND'
      TaskArn: 'AWS-RunPatchBaseline'
      Targets:
        - Key: 'WindowTargetIds'
          Values: [!Ref ProductionPatchTarget]
      Priority: 1
      ServiceRoleArn: !GetAtt MaintenanceWindowRole.Arn
      TaskParameters:
        Operation:
          Values: ['Install']
        RebootOption:
          Values: ['RebootIfNeeded']
      MaxConcurrency: '50%'
      MaxErrors: '5'
      Name: 'PatchInstallationTask'
      Description: 'Install approved patches'

  # Maintenance window task for compliance scanning
  ComplianceScanTask:
    Type: AWS::SSM::MaintenanceWindowTask
    Properties:
      WindowId: !Ref PatchMaintenanceWindow
      TaskType: 'RUN_COMMAND'
      TaskArn: 'AWS-RunPatchBaseline'
      Targets:
        - Key: 'WindowTargetIds'
          Values: [!Ref ProductionPatchTarget]
      Priority: 2
      ServiceRoleArn: !GetAtt MaintenanceWindowRole.Arn
      TaskParameters:
        Operation:
          Values: ['Scan']
      MaxConcurrency: '100%'
      MaxErrors: '5'
      Name: 'ComplianceScanTask'
      Description: 'Scan for patch compliance'

  # IAM role for maintenance window execution
  MaintenanceWindowRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: ssm.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/AmazonSSMMaintenanceWindowRole
      Policies:
        - PolicyName: PatchManagementPolicy
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - ssm:SendCommand
                  - ssm:ListCommands
                  - ssm:ListCommandInvocations
                  - ssm:DescribeInstanceInformation
                  - ssm:GetCommandInvocation
                  - ec2:DescribeInstances
                Resource: '*'

  # CloudWatch alarm for patch compliance
  PatchComplianceAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: 'PatchComplianceFailure'
      AlarmDescription: 'Alert when patch compliance falls below threshold'
      MetricName: 'ComplianceByPatchGroup'
      Namespace: 'AWS/SSM-PatchManager'
      Statistic: Average
      Period: 3600
      EvaluationPeriods: 1
      Threshold: 95
      ComparisonOperator: LessThanThreshold
      AlarmActions:
        - !Ref PatchComplianceNotification
      Dimensions:
        - Name: 'PatchGroup'
          Value: 'Production-Linux'

  # SNS topic for patch compliance notifications
  PatchComplianceNotification:
    Type: AWS::SNS::Topic
    Properties:
      TopicName: 'PatchComplianceAlerts'
      DisplayName: 'Patch Compliance Alerts'

Outputs:
  LinuxPatchBaselineId:
    Description: 'ID of the Linux patch baseline'
    Value: !Ref LinuxPatchBaseline
    Export:
      Name: !Sub '${AWS::StackName}-Linux-Patch-Baseline'

  WindowsPatchBaselineId:
    Description: 'ID of the Windows patch baseline'
    Value: !Ref WindowsPatchBaseline
    Export:
      Name: !Sub '${AWS::StackName}-Windows-Patch-Baseline'

  MaintenanceWindowId:
    Description: 'ID of the maintenance window'
    Value: !Ref PatchMaintenanceWindow
    Export:
      Name: !Sub '${AWS::StackName}-Maintenance-Window'

### Example 3: Container image vulnerability scanning

```bash
# Enable ECR image scanning for vulnerability detection
aws ecr put-image-scanning-configuration \
  --repository-name my-application \
  --image-scanning-configuration scanOnPush=true

# Create lifecycle policy to manage vulnerable images
aws ecr put-lifecycle-policy \
  --repository-name my-application \
  --lifecycle-policy-text '{
    "rules": [
      {
        "rulePriority": 1,
        "description": "Delete images with HIGH or CRITICAL vulnerabilities older than 7 days",
        "selection": {
          "tagStatus": "any",
          "countType": "sinceImagePushed",
          "countUnit": "days",
          "countNumber": 7
        },
        "action": {
          "type": "expire"
        }
      }
    ]
  }'

# Scan existing images for vulnerabilities
aws ecr start-image-scan \
  --repository-name my-application \
  --image-id imageTag=latest

# Get scan results
aws ecr describe-image-scan-findings \
  --repository-name my-application \
  --image-id imageTag=latest \
  --query 'imageScanFindings.findings[?severity==`HIGH` || severity==`CRITICAL`]'

# Create script for automated vulnerability reporting
cat > vulnerability-report.sh << 'EOF'
#!/bin/bash

REPOSITORY_NAME=$1
IMAGE_TAG=${2:-latest}

echo "Scanning image: $REPOSITORY_NAME:$IMAGE_TAG"

# Start scan
aws ecr start-image-scan \
  --repository-name $REPOSITORY_NAME \
  --image-id imageTag=$IMAGE_TAG

# Wait for scan completion
while true; do
  SCAN_STATUS=$(aws ecr describe-image-scan-findings \
    --repository-name $REPOSITORY_NAME \
    --image-id imageTag=$IMAGE_TAG \
    --query 'imageScanStatus.status' \
    --output text)
  
  if [ "$SCAN_STATUS" = "COMPLETE" ]; then
    break
  elif [ "$SCAN_STATUS" = "FAILED" ]; then
    echo "Scan failed"
    exit 1
  fi
  
  echo "Scan in progress..."
  sleep 10
done

# Get vulnerability counts
CRITICAL_COUNT=$(aws ecr describe-image-scan-findings \
  --repository-name $REPOSITORY_NAME \
  --image-id imageTag=$IMAGE_TAG \
  --query 'length(imageScanFindings.findings[?severity==`CRITICAL`])' \
  --output text)

HIGH_COUNT=$(aws ecr describe-image-scan-findings \
  --repository-name $REPOSITORY_NAME \
  --image-id imageTag=$IMAGE_TAG \
  --query 'length(imageScanFindings.findings[?severity==`HIGH`])' \
  --output text)

echo "Vulnerability Summary:"
echo "Critical: $CRITICAL_COUNT"
echo "High: $HIGH_COUNT"

# Fail build if critical vulnerabilities found
if [ "$CRITICAL_COUNT" -gt 0 ]; then
  echo "Build failed: Critical vulnerabilities found"
  exit 1
fi

echo "Vulnerability scan passed"
EOF

chmod +x vulnerability-report.sh
```

### Example 4: Dependency vulnerability scanning in CI/CD

```yaml
# GitHub Actions workflow for dependency vulnerability scanning
name: Vulnerability Scanning

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM

jobs:
  dependency-scan:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Set up Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
        cache: 'npm'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Run npm audit
      run: |
        npm audit --audit-level=high --production
        npm audit fix --dry-run --json > audit-results.json
    
    - name: Run Snyk security scan
      uses: snyk/actions/node@master
      env:
        SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
      with:
        args: --severity-threshold=high --fail-on=all
    
    - name: Run OWASP Dependency Check
      uses: dependency-check/Dependency-Check_Action@main
      with:
        project: 'my-application'
        path: '.'
        format: 'JSON'
        args: >
          --enableRetired
          --enableExperimental
          --failOnCVSS 7
    
    - name: Upload dependency check results
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: dependency-check-report
        path: reports/
    
    - name: Send vulnerability alert
      if: failure()
      uses: 8398a7/action-slack@v3
      with:
        status: failure
        channel: '#security-alerts'
        text: 'Vulnerability scan failed for ${{ github.repository }}'
      env:
        SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}

  infrastructure-scan:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Run Checkov IaC scan
      uses: bridgecrewio/checkov-action@master
      with:
        directory: ./infrastructure
        framework: cloudformation,terraform
        output_format: json
        output_file_path: checkov-report.json
        quiet: true
        soft_fail: false
    
    - name: Run Terrascan
      uses: accurics/terrascan-action@main
      with:
        iac_type: 'terraform'
        iac_version: 'v14'
        policy_type: 'aws'
        only_warn: false
        sarif_upload: true
    
    - name: Upload Terrascan results to GitHub Security
      uses: github/codeql-action/upload-sarif@v2
      if: always()
      with:
        sarif_file: terrascan.sarif

  container-scan:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Build Docker image
      run: |
        docker build -t my-app:${{ github.sha }} .
    
    - name: Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@master
      with:
        image-ref: 'my-app:${{ github.sha }}'
        format: 'sarif'
        output: 'trivy-results.sarif'
        severity: 'CRITICAL,HIGH'
        exit-code: '1'
    
    - name: Upload Trivy scan results to GitHub Security
      uses: github/codeql-action/upload-sarif@v2
      if: always()
      with:
        sarif_file: 'trivy-results.sarif'
    
    - name: Run Grype vulnerability scanner
      uses: anchore/scan-action@v3
      with:
        image: 'my-app:${{ github.sha }}'
        fail-build: true
        severity-cutoff: high
    
    - name: Upload Grype results
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: grype-report
        path: anchore-reports/
```

## AWS services to consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon Inspector</h4>
    <p>Automatically assesses applications for exposure, vulnerabilities, and deviations from best practices. Provides continuous vulnerability assessment for EC2 instances, container images, and Lambda functions.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Systems Manager Patch Manager</h4>
    <p>Automates the process of patching managed instances with both security related and other types of updates. Provides centralized patch management across your infrastructure.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon ECR Image Scanning</h4>
    <p>Provides vulnerability scanning for container images stored in Amazon Elastic Container Registry. Identifies software vulnerabilities in container images.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Security Hub</h4>
    <p>Provides a comprehensive view of your security state in AWS. Centralizes vulnerability findings from multiple security services for unified management.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Config</h4>
    <p>Enables you to assess, audit, and evaluate the configurations of your AWS resources. Helps identify configuration vulnerabilities and compliance issues.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon CodeGuru</h4>
    <p>Provides intelligent recommendations for improving code quality and identifying the most expensive lines of code. Includes security-focused code reviews and vulnerability detection.</p>
  </div>
</div>

## Benefits of performing vulnerability management

- **Reduced attack surface**: Systematic identification and remediation of vulnerabilities reduces potential entry points for attackers
- **Improved security posture**: Regular vulnerability assessments help maintain a strong security baseline
- **Compliance support**: Helps meet regulatory requirements for vulnerability management and security controls
- **Risk reduction**: Proactive vulnerability management reduces the likelihood and impact of security incidents
- **Cost efficiency**: Early detection and remediation of vulnerabilities is more cost-effective than incident response
- **Enhanced visibility**: Comprehensive vulnerability scanning provides better understanding of security risks
- **Automated protection**: Automated scanning and patching reduce manual effort and human error

## Related resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/sec_protect_compute_vulnerability_management.html">AWS Well-Architected Framework - Perform vulnerability management</a></li>
    <li><a href="https://docs.aws.amazon.com/inspector/latest/userguide/inspector_introduction.html">Amazon Inspector User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-patch.html">AWS Systems Manager Patch Manager</a></li>
    <li><a href="https://docs.aws.amazon.com/AmazonECR/latest/userguide/image-scanning.html">Amazon ECR Image Scanning</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-set-up-continuous-compliance-with-aws-config-and-aws-systems-manager/">How to set up continuous compliance with AWS Config and AWS Systems Manager</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-remediate-amazon-inspector-security-findings-automatically/">How to remediate Amazon Inspector security findings automatically</a></li>
  </ul>
</div>

### Example 3: Container image vulnerability scanning

```bash
# Enable ECR image scanning for vulnerability detection
aws ecr put-image-scanning-configuration \
  --repository-name my-application \
  --image-scanning-configuration scanOnPush=true

# Create lifecycle policy to manage vulnerable images
aws ecr put-lifecycle-policy \
  --repository-name my-application \
  --lifecycle-policy-text '{
    "rules": [
      {
        "rulePriority": 1,
        "description": "Delete images with HIGH or CRITICAL vulnerabilities older than 7 days",
        "selection": {
          "tagStatus": "any",
          "countType": "sinceImagePushed",
          "countUnit": "days",
          "countNumber": 7
        },
        "action": {
          "type": "expire"
        }
      }
    ]
  }'

# Scan existing images for vulnerabilities
aws ecr start-image-scan \
  --repository-name my-application \
  --image-id imageTag=latest

# Get scan results
aws ecr describe-image-scan-findings \
  --repository-name my-application \
  --image-id imageTag=latest \
  --query 'imageScanFindings.findings[?severity==`HIGH` || severity==`CRITICAL`]'

# Create script for automated vulnerability reporting
cat > vulnerability-report.sh << 'EOF'
#!/bin/bash

REPOSITORY_NAME=$1
IMAGE_TAG=${2:-latest}

echo "Scanning image: $REPOSITORY_NAME:$IMAGE_TAG"

# Start scan
aws ecr start-image-scan \
  --repository-name $REPOSITORY_NAME \
  --image-id imageTag=$IMAGE_TAG

# Wait for scan completion
while true; do
  SCAN_STATUS=$(aws ecr describe-image-scan-findings \
    --repository-name $REPOSITORY_NAME \
    --image-id imageTag=$IMAGE_TAG \
    --query 'imageScanStatus.status' \
    --output text)
  
  if [ "$SCAN_STATUS" = "COMPLETE" ]; then
    break
  elif [ "$SCAN_STATUS" = "FAILED" ]; then
    echo "Scan failed"
    exit 1
  fi
  
  echo "Scan in progress..."
  sleep 10
done

# Get vulnerability counts
CRITICAL_COUNT=$(aws ecr describe-image-scan-findings \
  --repository-name $REPOSITORY_NAME \
  --image-id imageTag=$IMAGE_TAG \
  --query 'length(imageScanFindings.findings[?severity==`CRITICAL`])' \
  --output text)

HIGH_COUNT=$(aws ecr describe-image-scan-findings \
  --repository-name $REPOSITORY_NAME \
  --image-id imageTag=$IMAGE_TAG \
  --query 'length(imageScanFindings.findings[?severity==`HIGH`])' \
  --output text)

echo "Vulnerability Summary:"
echo "Critical: $CRITICAL_COUNT"
echo "High: $HIGH_COUNT"

# Fail build if critical vulnerabilities found
if [ "$CRITICAL_COUNT" -gt 0 ]; then
  echo "Build failed: Critical vulnerabilities found"
  exit 1
fi

echo "Vulnerability scan passed"
EOF

chmod +x vulnerability-report.sh
```

### Example 4: Dependency vulnerability scanning in CI/CD

```yaml
# GitHub Actions workflow for dependency vulnerability scanning
name: Vulnerability Scanning

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM

jobs:
  dependency-scan:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Set up Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
        cache: 'npm'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Run npm audit
      run: |
        npm audit --audit-level=high --production
        npm audit fix --dry-run --json > audit-results.json
    
    - name: Run Snyk security scan
      uses: snyk/actions/node@master
      env:
        SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
      with:
        args: --severity-threshold=high --fail-on=all
    
    - name: Run OWASP Dependency Check
      uses: dependency-check/Dependency-Check_Action@main
      with:
        project: 'my-application'
        path: '.'
        format: 'JSON'
        args: >
          --enableRetired
          --enableExperimental
          --failOnCVSS 7
    
    - name: Upload dependency check results
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: dependency-check-report
        path: reports/
    
    - name: Send vulnerability alert
      if: failure()
      uses: 8398a7/action-slack@v3
      with:
        status: failure
        channel: '#security-alerts'
        text: 'Vulnerability scan failed for ${{ github.repository }}'
      env:
        SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}

  infrastructure-scan:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Run Checkov IaC scan
      uses: bridgecrewio/checkov-action@master
      with:
        directory: ./infrastructure
        framework: cloudformation,terraform
        output_format: json
        output_file_path: checkov-report.json
        quiet: true
        soft_fail: false
    
    - name: Run Terrascan
      uses: accurics/terrascan-action@main
      with:
        iac_type: 'terraform'
        iac_version: 'v14'
        policy_type: 'aws'
        only_warn: false
        sarif_upload: true
    
    - name: Upload Terrascan results to GitHub Security
      uses: github/codeql-action/upload-sarif@v2
      if: always()
      with:
        sarif_file: terrascan.sarif

  container-scan:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Build Docker image
      run: |
        docker build -t my-app:${{ github.sha }} .
    
    - name: Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@master
      with:
        image-ref: 'my-app:${{ github.sha }}'
        format: 'sarif'
        output: 'trivy-results.sarif'
        severity: 'CRITICAL,HIGH'
        exit-code: '1'
    
    - name: Upload Trivy scan results to GitHub Security
      uses: github/codeql-action/upload-sarif@v2
      if: always()
      with:
        sarif_file: 'trivy-results.sarif'
    
    - name: Run Grype vulnerability scanner
      uses: anchore/scan-action@v3
      with:
        image: 'my-app:${{ github.sha }}'
        fail-build: true
        severity-cutoff: high
    
    - name: Upload Grype results
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: grype-report
        path: anchore-reports/
```

## AWS services to consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon Inspector</h4>
    <p>Automatically assesses applications for exposure, vulnerabilities, and deviations from best practices. Provides continuous vulnerability assessment for EC2 instances, container images, and Lambda functions.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Systems Manager Patch Manager</h4>
    <p>Automates the process of patching managed instances with both security related and other types of updates. Provides centralized patch management across your infrastructure.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon ECR Image Scanning</h4>
    <p>Provides vulnerability scanning for container images stored in Amazon Elastic Container Registry. Identifies software vulnerabilities in container images.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Security Hub</h4>
    <p>Provides a comprehensive view of your security state in AWS. Centralizes vulnerability findings from multiple security services for unified management.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Config</h4>
    <p>Enables you to assess, audit, and evaluate the configurations of your AWS resources. Helps identify configuration vulnerabilities and compliance issues.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon CodeGuru</h4>
    <p>Provides intelligent recommendations for improving code quality and identifying the most expensive lines of code. Includes security-focused code reviews and vulnerability detection.</p>
  </div>
</div>

## Benefits of performing vulnerability management

- **Reduced attack surface**: Systematic identification and remediation of vulnerabilities reduces potential entry points for attackers
- **Improved security posture**: Regular vulnerability assessments help maintain a strong security baseline
- **Compliance support**: Helps meet regulatory requirements for vulnerability management and security controls
- **Risk reduction**: Proactive vulnerability management reduces the likelihood and impact of security incidents
- **Cost efficiency**: Early detection and remediation of vulnerabilities is more cost-effective than incident response
- **Enhanced visibility**: Comprehensive vulnerability scanning provides better understanding of security risks
- **Automated protection**: Automated scanning and patching reduce manual effort and human error

## Related resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/sec_protect_compute_vulnerability_management.html">AWS Well-Architected Framework - Perform vulnerability management</a></li>
    <li><a href="https://docs.aws.amazon.com/inspector/latest/userguide/inspector_introduction.html">Amazon Inspector User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-patch.html">AWS Systems Manager Patch Manager</a></li>
    <li><a href="https://docs.aws.amazon.com/AmazonECR/latest/userguide/image-scanning.html">Amazon ECR Image Scanning</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-set-up-continuous-compliance-with-aws-config-and-aws-systems-manager/">How to set up continuous compliance with AWS Config and AWS Systems Manager</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-remediate-amazon-inspector-security-findings-automatically/">How to remediate Amazon Inspector security findings automatically</a></li>
  </ul>
</div>
```
