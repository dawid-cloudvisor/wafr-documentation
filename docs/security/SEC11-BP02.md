---
title: "SEC11-BP02: Automate testing throughout the development and release lifecycle"
layout: default
parent: "SEC11 - How do you incorporate and validate the security properties of applications throughout the design, development, and deployment lifecycle?"
grand_parent: Security
nav_order: 2
---

# SEC11-BP02: Automate testing throughout the development and release lifecycle

## Overview

Implement automated security testing throughout the software development lifecycle (SDLC) to identify and remediate security vulnerabilities early and continuously. This includes static application security testing (SAST), dynamic application security testing (DAST), interactive application security testing (IAST), dependency scanning, and infrastructure as code (IaC) security testing.

## Implementation Guidance

Automated security testing is essential for maintaining security at the speed of modern software development. Manual security testing alone cannot keep pace with continuous integration and deployment practices. By integrating automated security testing throughout the development lifecycle, organizations can identify vulnerabilities early when they are less expensive to fix, ensure consistent security validation, and maintain security standards across all releases.

### Key Principles of Automated Security Testing

**Shift-Left Security**: Move security testing earlier in the development process to catch issues when they are easier and cheaper to fix. This includes integrating security testing into developer IDEs, pre-commit hooks, and early CI/CD pipeline stages.

**Comprehensive Coverage**: Implement multiple types of automated security testing to cover different aspects of application security, including source code, dependencies, runtime behavior, and infrastructure configuration.

**Continuous Integration**: Integrate security testing into CI/CD pipelines to ensure every code change is automatically tested for security issues before deployment.

**Fast Feedback**: Provide rapid feedback to developers about security issues so they can be addressed quickly without disrupting development velocity.

**Risk-Based Approach**: Prioritize security testing based on risk assessment, focusing more intensive testing on high-risk components and critical security controls.

## Implementation Steps

### Step 1: Implement Static Application Security Testing (SAST)

Deploy SAST tools to analyze source code for security vulnerabilities:

```python
# SAST Integration Framework
import boto3
import json
import subprocess
import os
from datetime import datetime
from typing import Dict, List, Optional

class SASTIntegration:
    def __init__(self):
        self.codebuild = boto3.client('codebuild')
        self.s3 = boto3.client('s3')
        self.sns = boto3.client('sns')
        self.dynamodb = boto3.resource('dynamodb')
        self.results_table = self.dynamodb.Table('sast-scan-results')
        
    def configure_sast_tools(self, project_config: Dict) -> Dict:
        """
        Configure multiple SAST tools for comprehensive coverage
        """
        sast_tools_config = {
            'sonarqube': {
                'enabled': True,
                'server_url': project_config.get('sonarqube_url', 'https://sonar.company.com'),
                'project_key': project_config['project_name'],
                'quality_gate': 'security_focused',
                'coverage_threshold': 80,
                'security_hotspot_threshold': 0,
                'vulnerability_threshold': 0,
                'languages': project_config.get('languages', ['java', 'python', 'javascript']),
                'exclusions': [
                    '**/test/**',
                    '**/tests/**',
                    '**/node_modules/**',
                    '**/vendor/**'
                ]
            },
            'semgrep': {
                'enabled': True,
                'ruleset': 'security',
                'custom_rules_path': 'security/semgrep-rules',
                'severity_threshold': 'WARNING',
                'languages': project_config.get('languages', ['python', 'javascript', 'go']),
                'exclude_patterns': [
                    'test_*.py',
                    '*.test.js',
                    'mock_*.py'
                ]
            },
            'bandit': {
                'enabled': project_config.get('languages', []).count('python') > 0,
                'config_file': '.bandit',
                'severity_level': 'medium',
                'confidence_level': 'medium',
                'exclude_dirs': ['tests', 'test'],
                'skip_tests': ['B101']  # Skip assert_used test
            },
            'eslint_security': {
                'enabled': 'javascript' in project_config.get('languages', []),
                'plugins': ['security', 'security-node'],
                'rules': {
                    'security/detect-object-injection': 'error',
                    'security/detect-non-literal-regexp': 'error',
                    'security/detect-unsafe-regex': 'error',
                    'security/detect-buffer-noassert': 'error',
                    'security/detect-child-process': 'error',
                    'security/detect-disable-mustache-escape': 'error',
                    'security/detect-eval-with-expression': 'error',
                    'security/detect-no-csrf-before-method-override': 'error',
                    'security/detect-non-literal-fs-filename': 'error',
                    'security/detect-non-literal-require': 'error',
                    'security/detect-possible-timing-attacks': 'error',
                    'security/detect-pseudoRandomBytes': 'error'
                }
            },
            'gosec': {
                'enabled': 'go' in project_config.get('languages', []),
                'severity': 'medium',
                'confidence': 'medium',
                'exclude_rules': [],
                'include_rules': ['G101', 'G102', 'G103', 'G104', 'G105']
            }
        }
        
        return sast_tools_config
    
    def create_sast_pipeline_stage(self, tool_config: Dict) -> str:
        """
        Create CodeBuild project for SAST scanning
        """
        buildspec = {
            'version': '0.2',
            'phases': {
                'install': {
                    'runtime-versions': {
                        'python': '3.9',
                        'nodejs': '16'
                    },
                    'commands': [
                        'echo "Installing SAST tools..."',
                        'pip install bandit semgrep',
                        'npm install -g eslint eslint-plugin-security',
                        'wget -O sonar-scanner.zip https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-4.7.0.2747-linux.zip',
                        'unzip sonar-scanner.zip',
                        'export PATH=$PATH:$PWD/sonar-scanner-4.7.0.2747-linux/bin'
                    ]
                },
                'pre_build': {
                    'commands': [
                        'echo "Preparing SAST scan..."',
                        'mkdir -p sast-results'
                    ]
                },
                'build': {
                    'commands': [
                        'echo "Running SAST scans..."',
                        self.generate_sast_commands(tool_config)
                    ]
                },
                'post_build': {
                    'commands': [
                        'echo "Processing SAST results..."',
                        'python scripts/process_sast_results.py',
                        'aws s3 cp sast-results/ s3://$SAST_RESULTS_BUCKET/$(date +%Y%m%d-%H%M%S)/ --recursive'
                    ]
                }
            },
            'artifacts': {
                'files': [
                    'sast-results/**/*'
                ]
            }
        }
        
        project_config = {
            'name': f"sast-scan-{tool_config['project_name']}",
            'source': {
                'type': 'CODEPIPELINE',
                'buildspec': json.dumps(buildspec, indent=2)
            },
            'artifacts': {
                'type': 'CODEPIPELINE'
            },
            'environment': {
                'type': 'LINUX_CONTAINER',
                'image': 'aws/codebuild/amazonlinux2-x86_64-standard:3.0',
                'computeType': 'BUILD_GENERAL1_MEDIUM',
                'environmentVariables': [
                    {
                        'name': 'SAST_RESULTS_BUCKET',
                        'value': tool_config.get('results_bucket', 'security-scan-results')
                    },
                    {
                        'name': 'SONAR_TOKEN',
                        'value': 'sonar-token',
                        'type': 'SECRETS_MANAGER'
                    }
                ]
            },
            'serviceRole': tool_config.get('service_role_arn')
        }
        
        response = self.codebuild.create_project(**project_config)
        return response['project']['arn']
    
    def generate_sast_commands(self, tool_config: Dict) -> str:
        """
        Generate SAST scanning commands based on enabled tools
        """
        commands = []
        
        # SonarQube scan
        if tool_config.get('sonarqube', {}).get('enabled'):
            sonar_config = tool_config['sonarqube']
            commands.extend([
                f'sonar-scanner \\',
                f'  -Dsonar.projectKey={sonar_config["project_key"]} \\',
                f'  -Dsonar.sources=. \\',
                f'  -Dsonar.host.url={sonar_config["server_url"]} \\',
                f'  -Dsonar.login=$SONAR_TOKEN \\',
                f'  -Dsonar.exclusions="{",".join(sonar_config["exclusions"])}" \\',
                f'  -Dsonar.qualitygate.wait=true',
                'sonar_exit_code=$?'
            ])
        
        # Semgrep scan
        if tool_config.get('semgrep', {}).get('enabled'):
            semgrep_config = tool_config['semgrep']
            commands.extend([
                f'semgrep --config=auto \\',
                f'  --severity={semgrep_config["severity_threshold"]} \\',
                f'  --json \\',
                f'  --output=sast-results/semgrep-results.json \\',
                f'  --exclude="{" --exclude=".join(semgrep_config["exclude_patterns"])}" \\',
                f'  .',
                'semgrep_exit_code=$?'
            ])
        
        # Bandit scan for Python
        if tool_config.get('bandit', {}).get('enabled'):
            bandit_config = tool_config['bandit']
            commands.extend([
                f'bandit -r . \\',
                f'  -f json \\',
                f'  -o sast-results/bandit-results.json \\',
                f'  -ll \\',
                f'  -i \\',
                f'  --exclude={",".join(bandit_config["exclude_dirs"])} \\',
                f'  --skip={",".join(bandit_config["skip_tests"])} || true',
                'bandit_exit_code=$?'
            ])
        
        # ESLint security scan for JavaScript
        if tool_config.get('eslint_security', {}).get('enabled'):
            commands.extend([
                'eslint . \\',
                '  --ext .js,.jsx,.ts,.tsx \\',
                '  --format json \\',
                '  --output-file sast-results/eslint-security-results.json \\',
                '  --no-error-on-unmatched-pattern || true',
                'eslint_exit_code=$?'
            ])
        
        # Gosec scan for Go
        if tool_config.get('gosec', {}).get('enabled'):
            gosec_config = tool_config['gosec']
            commands.extend([
                f'gosec -fmt json -out sast-results/gosec-results.json ./...',
                'gosec_exit_code=$?'
            ])
        
        # Combine all commands
        return ' && '.join(commands)
    
    def process_sast_results(self, scan_results_path: str, project_name: str) -> Dict:
        """
        Process and normalize SAST results from multiple tools
        """
        consolidated_results = {
            'scan_id': f"SAST-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            'project_name': project_name,
            'scan_timestamp': datetime.now().isoformat(),
            'tools_used': [],
            'summary': {
                'total_issues': 0,
                'critical_issues': 0,
                'high_issues': 0,
                'medium_issues': 0,
                'low_issues': 0,
                'info_issues': 0
            },
            'issues': [],
            'metrics': {
                'lines_of_code': 0,
                'files_scanned': 0,
                'scan_duration_seconds': 0
            }
        }
        
        # Process SonarQube results
        sonar_results_file = os.path.join(scan_results_path, 'sonar-results.json')
        if os.path.exists(sonar_results_file):
            sonar_issues = self.parse_sonarqube_results(sonar_results_file)
            consolidated_results['tools_used'].append('SonarQube')
            consolidated_results['issues'].extend(sonar_issues)
        
        # Process Semgrep results
        semgrep_results_file = os.path.join(scan_results_path, 'semgrep-results.json')
        if os.path.exists(semgrep_results_file):
            semgrep_issues = self.parse_semgrep_results(semgrep_results_file)
            consolidated_results['tools_used'].append('Semgrep')
            consolidated_results['issues'].extend(semgrep_issues)
        
        # Process Bandit results
        bandit_results_file = os.path.join(scan_results_path, 'bandit-results.json')
        if os.path.exists(bandit_results_file):
            bandit_issues = self.parse_bandit_results(bandit_results_file)
            consolidated_results['tools_used'].append('Bandit')
            consolidated_results['issues'].extend(bandit_issues)
        
        # Process ESLint results
        eslint_results_file = os.path.join(scan_results_path, 'eslint-security-results.json')
        if os.path.exists(eslint_results_file):
            eslint_issues = self.parse_eslint_results(eslint_results_file)
            consolidated_results['tools_used'].append('ESLint Security')
            consolidated_results['issues'].extend(eslint_issues)
        
        # Process Gosec results
        gosec_results_file = os.path.join(scan_results_path, 'gosec-results.json')
        if os.path.exists(gosec_results_file):
            gosec_issues = self.parse_gosec_results(gosec_results_file)
            consolidated_results['tools_used'].append('Gosec')
            consolidated_results['issues'].extend(gosec_issues)
        
        # Calculate summary statistics
        consolidated_results = self.calculate_summary_stats(consolidated_results)
        
        # Store results in DynamoDB
        self.store_scan_results(consolidated_results)
        
        return consolidated_results
    
    def parse_sonarqube_results(self, results_file: str) -> List[Dict]:
        """
        Parse SonarQube results and normalize format
        """
        issues = []
        try:
            with open(results_file, 'r') as f:
                sonar_data = json.load(f)
            
            for issue in sonar_data.get('issues', []):
                normalized_issue = {
                    'tool': 'SonarQube',
                    'rule_id': issue.get('rule'),
                    'severity': self.normalize_severity(issue.get('severity')),
                    'message': issue.get('message'),
                    'file_path': issue.get('component', '').replace(f"{sonar_data.get('projectKey', '')}:", ''),
                    'line_number': issue.get('line', 0),
                    'category': issue.get('type', 'VULNERABILITY'),
                    'cwe_id': self.extract_cwe_from_sonar(issue),
                    'confidence': 'HIGH',
                    'effort_minutes': issue.get('effort', 0)
                }
                issues.append(normalized_issue)
                
        except Exception as e:
            print(f"Error parsing SonarQube results: {e}")
        
        return issues
    
    def parse_semgrep_results(self, results_file: str) -> List[Dict]:
        """
        Parse Semgrep results and normalize format
        """
        issues = []
        try:
            with open(results_file, 'r') as f:
                semgrep_data = json.load(f)
            
            for result in semgrep_data.get('results', []):
                normalized_issue = {
                    'tool': 'Semgrep',
                    'rule_id': result.get('check_id'),
                    'severity': self.normalize_severity(result.get('extra', {}).get('severity')),
                    'message': result.get('extra', {}).get('message'),
                    'file_path': result.get('path'),
                    'line_number': result.get('start', {}).get('line', 0),
                    'category': 'VULNERABILITY',
                    'cwe_id': self.extract_cwe_from_semgrep(result),
                    'confidence': result.get('extra', {}).get('metadata', {}).get('confidence', 'MEDIUM'),
                    'owasp_category': result.get('extra', {}).get('metadata', {}).get('owasp')
                }
                issues.append(normalized_issue)
                
        except Exception as e:
            print(f"Error parsing Semgrep results: {e}")
        
        return issues
    
    def parse_bandit_results(self, results_file: str) -> List[Dict]:
        """
        Parse Bandit results and normalize format
        """
        issues = []
        try:
            with open(results_file, 'r') as f:
                bandit_data = json.load(f)
            
            for result in bandit_data.get('results', []):
                normalized_issue = {
                    'tool': 'Bandit',
                    'rule_id': result.get('test_id'),
                    'severity': self.normalize_severity(result.get('issue_severity')),
                    'message': result.get('issue_text'),
                    'file_path': result.get('filename'),
                    'line_number': result.get('line_number', 0),
                    'category': 'VULNERABILITY',
                    'cwe_id': result.get('issue_cwe', {}).get('id'),
                    'confidence': result.get('issue_confidence'),
                    'more_info': result.get('more_info')
                }
                issues.append(normalized_issue)
                
        except Exception as e:
            print(f"Error parsing Bandit results: {e}")
        
        return issues
    
    def normalize_severity(self, severity: str) -> str:
        """
        Normalize severity levels across different tools
        """
        severity_mapping = {
            # SonarQube
            'BLOCKER': 'CRITICAL',
            'CRITICAL': 'CRITICAL',
            'MAJOR': 'HIGH',
            'MINOR': 'MEDIUM',
            'INFO': 'LOW',
            
            # Semgrep
            'ERROR': 'CRITICAL',
            'WARNING': 'HIGH',
            'INFO': 'LOW',
            
            # Bandit
            'HIGH': 'HIGH',
            'MEDIUM': 'MEDIUM',
            'LOW': 'LOW',
            
            # ESLint
            '2': 'HIGH',
            '1': 'MEDIUM',
            '0': 'LOW'
        }
        
        return severity_mapping.get(str(severity).upper(), 'MEDIUM')
    
    def calculate_summary_stats(self, results: Dict) -> Dict:
        """
        Calculate summary statistics for scan results
        """
        severity_counts = {
            'CRITICAL': 0,
            'HIGH': 0,
            'MEDIUM': 0,
            'LOW': 0,
            'INFO': 0
        }
        
        for issue in results['issues']:
            severity = issue.get('severity', 'MEDIUM')
            if severity in severity_counts:
                severity_counts[severity] += 1
        
        results['summary'] = {
            'total_issues': len(results['issues']),
            'critical_issues': severity_counts['CRITICAL'],
            'high_issues': severity_counts['HIGH'],
            'medium_issues': severity_counts['MEDIUM'],
            'low_issues': severity_counts['LOW'],
            'info_issues': severity_counts['INFO']
        }
        
        return results
    
    def store_scan_results(self, results: Dict):
        """
        Store scan results in DynamoDB for tracking and reporting
        """
        try:
            self.results_table.put_item(Item=results)
        except Exception as e:
            print(f"Error storing scan results: {e}")
    
    def create_security_gates(self, gate_config: Dict) -> Dict:
        """
        Create security gates based on SAST results
        """
        security_gates = {
            'gate_id': f"GATE-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            'project_name': gate_config['project_name'],
            'gate_rules': {
                'critical_issues_threshold': gate_config.get('critical_threshold', 0),
                'high_issues_threshold': gate_config.get('high_threshold', 5),
                'medium_issues_threshold': gate_config.get('medium_threshold', 20),
                'total_issues_threshold': gate_config.get('total_threshold', 50),
                'new_issues_threshold': gate_config.get('new_issues_threshold', 0)
            },
            'actions': {
                'block_deployment': gate_config.get('block_deployment', True),
                'notify_security_team': gate_config.get('notify_security', True),
                'create_jira_tickets': gate_config.get('create_tickets', True),
                'fail_build': gate_config.get('fail_build', True)
            }
        }
        
        return security_gates

# Example usage
sast_integration = SASTIntegration()

# Configure SAST tools for a project
project_config = {
    'project_name': 'secure-web-app',
    'languages': ['python', 'javascript'],
    'sonarqube_url': 'https://sonar.company.com',
    'results_bucket': 'security-scan-results-bucket'
}

sast_config = sast_integration.configure_sast_tools(project_config)
print("SAST Configuration:")
print(json.dumps(sast_config, indent=2))

# Create SAST pipeline stage
pipeline_arn = sast_integration.create_sast_pipeline_stage(sast_config)
print(f"\\nSAST Pipeline ARN: {pipeline_arn}")
```
### Step 2: Implement Dynamic Application Security Testing (DAST)

Deploy DAST tools to test running applications for security vulnerabilities:

```python
# DAST Integration Framework
import boto3
import json
import requests
import time
from datetime import datetime
from typing import Dict, List, Optional

class DASTIntegration:
    def __init__(self):
        self.ecs = boto3.client('ecs')
        self.ec2 = boto3.client('ec2')
        self.ssm = boto3.client('ssm')
        self.s3 = boto3.client('s3')
        self.dynamodb = boto3.resource('dynamodb')
        self.results_table = self.dynamodb.Table('dast-scan-results')
        
    def configure_dast_tools(self, application_config: Dict) -> Dict:
        """
        Configure DAST tools for comprehensive runtime security testing
        """
        dast_tools_config = {
            'owasp_zap': {
                'enabled': True,
                'docker_image': 'owasp/zap2docker-stable',
                'scan_types': ['baseline', 'full', 'api'],
                'authentication': {
                    'enabled': application_config.get('requires_auth', False),
                    'auth_type': application_config.get('auth_type', 'form'),
                    'login_url': application_config.get('login_url'),
                    'username_field': 'username',
                    'password_field': 'password',
                    'credentials_secret': application_config.get('test_credentials_secret')
                },
                'scan_policies': {
                    'baseline': {
                        'passive_scan_only': True,
                        'max_duration_minutes': 30,
                        'alert_threshold': 'MEDIUM'
                    },
                    'full': {
                        'active_scan': True,
                        'max_duration_minutes': 120,
                        'alert_threshold': 'LOW',
                        'attack_strength': 'MEDIUM'
                    },
                    'api': {
                        'api_definition': application_config.get('openapi_spec_url'),
                        'max_duration_minutes': 60,
                        'alert_threshold': 'MEDIUM'
                    }
                },
                'exclusions': [
                    '/logout',
                    '/admin/delete',
                    '/api/v1/users/delete'
                ]
            },
            'nuclei': {
                'enabled': True,
                'docker_image': 'projectdiscovery/nuclei',
                'templates': [
                    'cves',
                    'vulnerabilities',
                    'security-misconfiguration',
                    'exposed-panels',
                    'technologies'
                ],
                'severity_threshold': 'medium',
                'rate_limit': 150,  # requests per second
                'timeout': 10,
                'retries': 1
            },
            'nikto': {
                'enabled': True,
                'docker_image': 'sullo/nikto',
                'scan_options': [
                    '-Tuning', '1,2,3,4,5,6,7,8,9,0',
                    '-Format', 'json',
                    '-maxtime', '3600'
                ],
                'plugins': 'ALL'
            },
            'custom_security_tests': {
                'enabled': True,
                'test_suite_image': 'company/security-test-suite:latest',
                'test_categories': [
                    'authentication_bypass',
                    'authorization_flaws',
                    'input_validation',
                    'session_management',
                    'business_logic'
                ]
            }
        }
        
        return dast_tools_config
    
    def create_dast_environment(self, app_config: Dict) -> Dict:
        """
        Create isolated environment for DAST testing
        """
        # Create VPC for DAST testing
        vpc_response = self.ec2.create_vpc(
            CidrBlock='10.0.0.0/16',
            TagSpecifications=[
                {
                    'ResourceType': 'vpc',
                    'Tags': [
                        {'Key': 'Name', 'Value': f"dast-vpc-{app_config['app_name']}"},
                        {'Key': 'Purpose', 'Value': 'DAST-Testing'},
                        {'Key': 'Environment', 'Value': 'testing'}
                    ]
                }
            ]
        )
        vpc_id = vpc_response['Vpc']['VpcId']
        
        # Create subnet
        subnet_response = self.ec2.create_subnet(
            VpcId=vpc_id,
            CidrBlock='10.0.1.0/24',
            TagSpecifications=[
                {
                    'ResourceType': 'subnet',
                    'Tags': [
                        {'Key': 'Name', 'Value': f"dast-subnet-{app_config['app_name']}"}
                    ]
                }
            ]
        )
        subnet_id = subnet_response['Subnet']['SubnetId']
        
        # Create security group for DAST testing
        sg_response = self.ec2.create_security_group(
            GroupName=f"dast-sg-{app_config['app_name']}",
            Description='Security group for DAST testing environment',
            VpcId=vpc_id,
            TagSpecifications=[
                {
                    'ResourceType': 'security-group',
                    'Tags': [
                        {'Key': 'Name', 'Value': f"dast-sg-{app_config['app_name']}"}
                    ]
                }
            ]
        )
        sg_id = sg_response['GroupId']
        
        # Configure security group rules
        self.ec2.authorize_security_group_ingress(
            GroupId=sg_id,
            IpPermissions=[
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 80,
                    'ToPort': 80,
                    'IpRanges': [{'CidrIp': '10.0.0.0/16'}]
                },
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 443,
                    'ToPort': 443,
                    'IpRanges': [{'CidrIp': '10.0.0.0/16'}]
                },
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 8080,
                    'ToPort': 8090,
                    'IpRanges': [{'CidrIp': '10.0.0.0/16'}]
                }
            ]
        )
        
        # Create ECS cluster for DAST tools
        cluster_response = self.ecs.create_cluster(
            clusterName=f"dast-cluster-{app_config['app_name']}",
            tags=[
                {'key': 'Purpose', 'value': 'DAST-Testing'},
                {'key': 'Application', 'value': app_config['app_name']}
            ]
        )
        
        environment_config = {
            'vpc_id': vpc_id,
            'subnet_id': subnet_id,
            'security_group_id': sg_id,
            'cluster_arn': cluster_response['cluster']['clusterArn'],
            'cluster_name': cluster_response['cluster']['clusterName']
        }
        
        return environment_config
    
    def deploy_application_under_test(self, app_config: Dict, environment: Dict) -> Dict:
        """
        Deploy application in isolated environment for testing
        """
        task_definition = {
            'family': f"dast-app-{app_config['app_name']}",
            'networkMode': 'awsvpc',
            'requiresCompatibilities': ['FARGATE'],
            'cpu': '512',
            'memory': '1024',
            'executionRoleArn': app_config.get('execution_role_arn'),
            'taskRoleArn': app_config.get('task_role_arn'),
            'containerDefinitions': [
                {
                    'name': 'application',
                    'image': app_config['docker_image'],
                    'portMappings': [
                        {
                            'containerPort': app_config.get('port', 8080),
                            'protocol': 'tcp'
                        }
                    ],
                    'environment': [
                        {'name': 'ENV', 'value': 'dast-testing'},
                        {'name': 'DEBUG', 'value': 'false'},
                        {'name': 'LOG_LEVEL', 'value': 'INFO'}
                    ],
                    'secrets': [
                        {
                            'name': 'DB_PASSWORD',
                            'valueFrom': app_config.get('db_secret_arn')
                        }
                    ] if app_config.get('db_secret_arn') else [],
                    'logConfiguration': {
                        'logDriver': 'awslogs',
                        'options': {
                            'awslogs-group': f"/ecs/dast-{app_config['app_name']}",
                            'awslogs-region': 'us-east-1',
                            'awslogs-stream-prefix': 'ecs'
                        }
                    },
                    'healthCheck': {
                        'command': [
                            'CMD-SHELL',
                            f"curl -f http://localhost:{app_config.get('port', 8080)}/health || exit 1"
                        ],
                        'interval': 30,
                        'timeout': 5,
                        'retries': 3,
                        'startPeriod': 60
                    }
                }
            ]
        }
        
        # Register task definition
        task_def_response = self.ecs.register_task_definition(**task_definition)
        
        # Create service
        service_config = {
            'cluster': environment['cluster_name'],
            'serviceName': f"dast-service-{app_config['app_name']}",
            'taskDefinition': task_def_response['taskDefinition']['taskDefinitionArn'],
            'desiredCount': 1,
            'launchType': 'FARGATE',
            'networkConfiguration': {
                'awsvpcConfiguration': {
                    'subnets': [environment['subnet_id']],
                    'securityGroups': [environment['security_group_id']],
                    'assignPublicIp': 'ENABLED'
                }
            },
            'tags': [
                {'key': 'Purpose', 'value': 'DAST-Testing'},
                {'key': 'Application', 'value': app_config['app_name']}
            ]
        }
        
        service_response = self.ecs.create_service(**service_config)
        
        # Wait for service to be stable
        waiter = self.ecs.get_waiter('services_stable')
        waiter.wait(
            cluster=environment['cluster_name'],
            services=[service_config['serviceName']],
            WaiterConfig={'delay': 15, 'maxAttempts': 40}
        )
        
        # Get service endpoint
        service_endpoint = self.get_service_endpoint(
            environment['cluster_name'],
            service_config['serviceName']
        )
        
        deployment_info = {
            'task_definition_arn': task_def_response['taskDefinition']['taskDefinitionArn'],
            'service_arn': service_response['service']['serviceArn'],
            'service_name': service_config['serviceName'],
            'endpoint': service_endpoint,
            'health_check_url': f"http://{service_endpoint}/health"
        }
        
        return deployment_info
    
    def run_owasp_zap_scan(self, target_url: str, scan_config: Dict) -> Dict:
        """
        Run OWASP ZAP security scan
        """
        scan_id = f"ZAP-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        # Create ZAP task definition
        zap_task_definition = {
            'family': f'zap-scanner-{scan_id}',
            'networkMode': 'awsvpc',
            'requiresCompatibilities': ['FARGATE'],
            'cpu': '1024',
            'memory': '2048',
            'executionRoleArn': scan_config.get('execution_role_arn'),
            'containerDefinitions': [
                {
                    'name': 'zap-scanner',
                    'image': scan_config['owasp_zap']['docker_image'],
                    'command': self.build_zap_command(target_url, scan_config),
                    'environment': [
                        {'name': 'ZAP_PORT', 'value': '8080'},
                        {'name': 'TARGET_URL', 'value': target_url}
                    ],
                    'logConfiguration': {
                        'logDriver': 'awslogs',
                        'options': {
                            'awslogs-group': f'/ecs/zap-scanner',
                            'awslogs-region': 'us-east-1',
                            'awslogs-stream-prefix': scan_id
                        }
                    }
                }
            ]
        }
        
        # Register and run ZAP task
        task_def_response = self.ecs.register_task_definition(**zap_task_definition)
        
        run_task_response = self.ecs.run_task(
            cluster=scan_config['cluster_name'],
            taskDefinition=task_def_response['taskDefinition']['taskDefinitionArn'],
            launchType='FARGATE',
            networkConfiguration={
                'awsvpcConfiguration': {
                    'subnets': [scan_config['subnet_id']],
                    'securityGroups': [scan_config['security_group_id']],
                    'assignPublicIp': 'ENABLED'
                }
            },
            tags=[
                {'key': 'ScanType', 'value': 'DAST'},
                {'key': 'Tool', 'value': 'OWASP-ZAP'},
                {'key': 'ScanId', 'value': scan_id}
            ]
        )
        
        task_arn = run_task_response['tasks'][0]['taskArn']
        
        # Wait for task completion
        waiter = self.ecs.get_waiter('tasks_stopped')
        waiter.wait(
            cluster=scan_config['cluster_name'],
            tasks=[task_arn],
            WaiterConfig={'delay': 30, 'maxAttempts': 120}
        )
        
        # Retrieve scan results
        scan_results = self.retrieve_zap_results(task_arn, scan_id)
        
        return {
            'scan_id': scan_id,
            'task_arn': task_arn,
            'target_url': target_url,
            'scan_type': 'OWASP_ZAP',
            'results': scan_results,
            'timestamp': datetime.now().isoformat()
        }
    
    def build_zap_command(self, target_url: str, scan_config: Dict) -> List[str]:
        """
        Build OWASP ZAP command based on scan configuration
        """
        zap_config = scan_config['owasp_zap']
        scan_policy = zap_config['scan_policies']['full']  # Default to full scan
        
        command = [
            'zap-full-scan.py',
            '-t', target_url,
            '-J', f'/zap/wrk/zap-report-{datetime.now().strftime("%Y%m%d-%H%M%S")}.json',
            '-r', f'/zap/wrk/zap-report-{datetime.now().strftime("%Y%m%d-%H%M%S")}.html'
        ]
        
        # Add authentication if configured
        if zap_config['authentication']['enabled']:
            command.extend([
                '-z', f"auth.loginurl={zap_config['authentication']['login_url']}",
                '-z', f"auth.username={zap_config['authentication']['username_field']}",
                '-z', f"auth.password={zap_config['authentication']['password_field']}"
            ])
        
        # Add exclusions
        for exclusion in zap_config['exclusions']:
            command.extend(['-z', f"spider.excludeurl={exclusion}"])
        
        # Add scan duration limit
        command.extend(['-m', str(scan_policy['max_duration_minutes'])])
        
        # Add alert threshold
        command.extend(['-l', scan_policy['alert_threshold']])
        
        return command
    
    def run_nuclei_scan(self, target_url: str, scan_config: Dict) -> Dict:
        """
        Run Nuclei vulnerability scanner
        """
        scan_id = f"NUCLEI-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        nuclei_config = scan_config['nuclei']
        
        # Build Nuclei command
        nuclei_command = [
            'nuclei',
            '-u', target_url,
            '-json',
            '-o', f'/results/nuclei-{scan_id}.json',
            '-severity', nuclei_config['severity_threshold'],
            '-rate-limit', str(nuclei_config['rate_limit']),
            '-timeout', str(nuclei_config['timeout']),
            '-retries', str(nuclei_config['retries'])
        ]
        
        # Add templates
        for template in nuclei_config['templates']:
            nuclei_command.extend(['-t', template])
        
        # Create Nuclei task definition
        nuclei_task_definition = {
            'family': f'nuclei-scanner-{scan_id}',
            'networkMode': 'awsvpc',
            'requiresCompatibilities': ['FARGATE'],
            'cpu': '512',
            'memory': '1024',
            'executionRoleArn': scan_config.get('execution_role_arn'),
            'containerDefinitions': [
                {
                    'name': 'nuclei-scanner',
                    'image': nuclei_config['docker_image'],
                    'command': nuclei_command,
                    'logConfiguration': {
                        'logDriver': 'awslogs',
                        'options': {
                            'awslogs-group': '/ecs/nuclei-scanner',
                            'awslogs-region': 'us-east-1',
                            'awslogs-stream-prefix': scan_id
                        }
                    }
                }
            ]
        }
        
        # Register and run Nuclei task
        task_def_response = self.ecs.register_task_definition(**nuclei_task_definition)
        
        run_task_response = self.ecs.run_task(
            cluster=scan_config['cluster_name'],
            taskDefinition=task_def_response['taskDefinition']['taskDefinitionArn'],
            launchType='FARGATE',
            networkConfiguration={
                'awsvpcConfiguration': {
                    'subnets': [scan_config['subnet_id']],
                    'securityGroups': [scan_config['security_group_id']],
                    'assignPublicIp': 'ENABLED'
                }
            }
        )
        
        task_arn = run_task_response['tasks'][0]['taskArn']
        
        # Wait for completion and retrieve results
        waiter = self.ecs.get_waiter('tasks_stopped')
        waiter.wait(
            cluster=scan_config['cluster_name'],
            tasks=[task_arn],
            WaiterConfig={'delay': 15, 'maxAttempts': 60}
        )
        
        scan_results = self.retrieve_nuclei_results(task_arn, scan_id)
        
        return {
            'scan_id': scan_id,
            'task_arn': task_arn,
            'target_url': target_url,
            'scan_type': 'NUCLEI',
            'results': scan_results,
            'timestamp': datetime.now().isoformat()
        }
    
    def orchestrate_dast_pipeline(self, app_config: Dict, dast_config: Dict) -> Dict:
        """
        Orchestrate complete DAST pipeline
        """
        pipeline_id = f"DAST-PIPELINE-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        pipeline_results = {
            'pipeline_id': pipeline_id,
            'application': app_config['app_name'],
            'start_time': datetime.now().isoformat(),
            'stages': [],
            'overall_status': 'RUNNING',
            'security_gate_status': 'PENDING'
        }
        
        try:
            # Stage 1: Create DAST environment
            print("Creating DAST environment...")
            environment = self.create_dast_environment(app_config)
            pipeline_results['stages'].append({
                'stage': 'environment_setup',
                'status': 'COMPLETED',
                'duration_seconds': 120,
                'details': environment
            })
            
            # Stage 2: Deploy application under test
            print("Deploying application under test...")
            deployment = self.deploy_application_under_test(app_config, environment)
            pipeline_results['stages'].append({
                'stage': 'application_deployment',
                'status': 'COMPLETED',
                'duration_seconds': 300,
                'details': deployment
            })
            
            # Stage 3: Wait for application readiness
            print("Waiting for application readiness...")
            self.wait_for_application_ready(deployment['health_check_url'])
            
            # Stage 4: Run DAST scans
            scan_results = []
            
            # OWASP ZAP scan
            if dast_config['owasp_zap']['enabled']:
                print("Running OWASP ZAP scan...")
                zap_results = self.run_owasp_zap_scan(
                    deployment['endpoint'], 
                    {**dast_config, **environment}
                )
                scan_results.append(zap_results)
            
            # Nuclei scan
            if dast_config['nuclei']['enabled']:
                print("Running Nuclei scan...")
                nuclei_results = self.run_nuclei_scan(
                    deployment['endpoint'],
                    {**dast_config, **environment}
                )
                scan_results.append(nuclei_results)
            
            pipeline_results['stages'].append({
                'stage': 'security_scanning',
                'status': 'COMPLETED',
                'duration_seconds': 1800,
                'scan_results': scan_results
            })
            
            # Stage 5: Process and consolidate results
            consolidated_results = self.consolidate_dast_results(scan_results)
            pipeline_results['consolidated_results'] = consolidated_results
            
            # Stage 6: Apply security gates
            gate_result = self.apply_security_gates(consolidated_results, dast_config)
            pipeline_results['security_gate_status'] = gate_result['status']
            pipeline_results['security_gate_details'] = gate_result
            
            # Stage 7: Cleanup
            print("Cleaning up DAST environment...")
            self.cleanup_dast_environment(environment, deployment)
            
            pipeline_results['overall_status'] = 'COMPLETED'
            pipeline_results['end_time'] = datetime.now().isoformat()
            
        except Exception as e:
            pipeline_results['overall_status'] = 'FAILED'
            pipeline_results['error'] = str(e)
            pipeline_results['end_time'] = datetime.now().isoformat()
        
        # Store pipeline results
        self.store_dast_results(pipeline_results)
        
        return pipeline_results
    
    def consolidate_dast_results(self, scan_results: List[Dict]) -> Dict:
        """
        Consolidate results from multiple DAST tools
        """
        consolidated = {
            'total_vulnerabilities': 0,
            'critical_count': 0,
            'high_count': 0,
            'medium_count': 0,
            'low_count': 0,
            'info_count': 0,
            'vulnerabilities_by_category': {},
            'tools_used': [],
            'scan_coverage': {},
            'detailed_findings': []
        }
        
        for scan_result in scan_results:
            tool_name = scan_result['scan_type']
            consolidated['tools_used'].append(tool_name)
            
            # Process tool-specific results
            if tool_name == 'OWASP_ZAP':
                zap_findings = self.process_zap_findings(scan_result['results'])
                consolidated['detailed_findings'].extend(zap_findings)
            elif tool_name == 'NUCLEI':
                nuclei_findings = self.process_nuclei_findings(scan_result['results'])
                consolidated['detailed_findings'].extend(nuclei_findings)
        
        # Calculate summary statistics
        for finding in consolidated['detailed_findings']:
            severity = finding.get('severity', 'INFO').upper()
            if severity == 'CRITICAL':
                consolidated['critical_count'] += 1
            elif severity == 'HIGH':
                consolidated['high_count'] += 1
            elif severity == 'MEDIUM':
                consolidated['medium_count'] += 1
            elif severity == 'LOW':
                consolidated['low_count'] += 1
            else:
                consolidated['info_count'] += 1
            
            # Count by category
            category = finding.get('category', 'Other')
            consolidated['vulnerabilities_by_category'][category] = \
                consolidated['vulnerabilities_by_category'].get(category, 0) + 1
        
        consolidated['total_vulnerabilities'] = len(consolidated['detailed_findings'])
        
        return consolidated

# Example usage
dast_integration = DASTIntegration()

# Configure application for DAST testing
app_config = {
    'app_name': 'secure-web-app',
    'docker_image': 'company/secure-web-app:latest',
    'port': 8080,
    'requires_auth': True,
    'auth_type': 'form',
    'login_url': '/login',
    'test_credentials_secret': 'arn:aws:secretsmanager:us-east-1:123456789012:secret:dast-test-creds',
    'execution_role_arn': 'arn:aws:iam::123456789012:role/ecsTaskExecutionRole'
}

# Configure DAST tools
dast_config = dast_integration.configure_dast_tools(app_config)
print("DAST Configuration:")
print(json.dumps(dast_config, indent=2))

# Run complete DAST pipeline
pipeline_results = dast_integration.orchestrate_dast_pipeline(app_config, dast_config)
print("\\nDAST Pipeline Results:")
print(json.dumps(pipeline_results, indent=2))
```
### Step 3: Implement Dependency Scanning

Deploy dependency scanning tools to identify vulnerabilities in third-party libraries and components:

```python
# Dependency Scanning Framework
import boto3
import json
import subprocess
import os
from datetime import datetime
from typing import Dict, List, Optional

class DependencyScanning:
    def __init__(self):
        self.codebuild = boto3.client('codebuild')
        self.s3 = boto3.client('s3')
        self.dynamodb = boto3.resource('dynamodb')
        self.results_table = self.dynamodb.Table('dependency-scan-results')
        
    def configure_dependency_scanners(self, project_config: Dict) -> Dict:
        """
        Configure dependency scanning tools for different package managers
        """
        scanner_config = {
            'npm_audit': {
                'enabled': 'package.json' in project_config.get('manifest_files', []),
                'audit_level': 'moderate',
                'production_only': True,
                'registry': 'https://registry.npmjs.org/',
                'output_format': 'json'
            },
            'pip_audit': {
                'enabled': any(f in project_config.get('manifest_files', []) 
                             for f in ['requirements.txt', 'Pipfile', 'pyproject.toml']),
                'vulnerability_database': 'pypa',
                'output_format': 'json',
                'ignore_vulns': project_config.get('ignored_vulnerabilities', [])
            },
            'snyk': {
                'enabled': True,
                'severity_threshold': 'medium',
                'monitor': True,
                'test_all_projects': True,
                'fail_on': 'upgradable',
                'package_managers': ['npm', 'pip', 'maven', 'gradle', 'go', 'nuget'],
                'exclude_dev_dependencies': True
            },
            'safety': {
                'enabled': 'python' in project_config.get('languages', []),
                'database': 'safety-db',
                'output_format': 'json',
                'ignore_ids': project_config.get('safety_ignore_ids', [])
            },
            'retire_js': {
                'enabled': 'javascript' in project_config.get('languages', []),
                'severity': ['high', 'medium'],
                'output_format': 'json',
                'ignore_file': '.retireignore'
            },
            'owasp_dependency_check': {
                'enabled': True,
                'formats': ['JSON', 'HTML'],
                'suppression_file': 'dependency-check-suppressions.xml',
                'fail_build_on_cvss': 7.0,
                'enable_experimental': False,
                'enable_retired': True
            }
        }
        
        return scanner_config
    
    def create_dependency_scan_pipeline(self, scanner_config: Dict) -> str:
        """
        Create CodeBuild project for dependency scanning
        """
        buildspec = {
            'version': '0.2',
            'phases': {
                'install': {
                    'runtime-versions': {
                        'python': '3.9',
                        'nodejs': '16',
                        'java': 'corretto11'
                    },
                    'commands': [
                        'echo "Installing dependency scanners..."',
                        'npm install -g npm-audit-resolver retire @snyk/cli',
                        'pip install pip-audit safety',
                        'wget -O dependency-check.zip https://github.com/jeremylong/DependencyCheck/releases/download/v7.4.4/dependency-check-7.4.4-release.zip',
                        'unzip dependency-check.zip',
                        'export PATH=$PATH:$PWD/dependency-check/bin'
                    ]
                },
                'pre_build': {
                    'commands': [
                        'echo "Preparing dependency scan..."',
                        'mkdir -p dependency-scan-results',
                        'echo "Scanning for manifest files..."',
                        'find . -name "package.json" -o -name "requirements.txt" -o -name "pom.xml" -o -name "build.gradle" -o -name "go.mod" -o -name "Cargo.toml" | tee manifest-files.txt'
                    ]
                },
                'build': {
                    'commands': [
                        'echo "Running dependency scans..."',
                        self.generate_dependency_scan_commands(scanner_config)
                    ]
                },
                'post_build': {
                    'commands': [
                        'echo "Processing dependency scan results..."',
                        'python scripts/consolidate_dependency_results.py',
                        'aws s3 cp dependency-scan-results/ s3://$DEPENDENCY_SCAN_BUCKET/$(date +%Y%m%d-%H%M%S)/ --recursive'
                    ]
                }
            },
            'artifacts': {
                'files': [
                    'dependency-scan-results/**/*'
                ]
            }
        }
        
        project_config = {
            'name': f"dependency-scan-{scanner_config['project_name']}",
            'source': {
                'type': 'CODEPIPELINE',
                'buildspec': json.dumps(buildspec, indent=2)
            },
            'artifacts': {
                'type': 'CODEPIPELINE'
            },
            'environment': {
                'type': 'LINUX_CONTAINER',
                'image': 'aws/codebuild/amazonlinux2-x86_64-standard:3.0',
                'computeType': 'BUILD_GENERAL1_MEDIUM',
                'environmentVariables': [
                    {
                        'name': 'DEPENDENCY_SCAN_BUCKET',
                        'value': scanner_config.get('results_bucket', 'dependency-scan-results')
                    },
                    {
                        'name': 'SNYK_TOKEN',
                        'value': 'snyk-api-token',
                        'type': 'SECRETS_MANAGER'
                    }
                ]
            },
            'serviceRole': scanner_config.get('service_role_arn')
        }
        
        response = self.codebuild.create_project(**project_config)
        return response['project']['arn']
    
    def generate_dependency_scan_commands(self, scanner_config: Dict) -> str:
        """
        Generate dependency scanning commands based on enabled tools
        """
        commands = []
        
        # NPM Audit
        if scanner_config.get('npm_audit', {}).get('enabled'):
            npm_config = scanner_config['npm_audit']
            commands.extend([
                'if [ -f "package.json" ]; then',
                f'  npm audit --audit-level={npm_config["audit_level"]} --json > dependency-scan-results/npm-audit.json || true',
                'fi'
            ])
        
        # Pip Audit
        if scanner_config.get('pip_audit', {}).get('enabled'):
            pip_config = scanner_config['pip_audit']
            commands.extend([
                'if [ -f "requirements.txt" ]; then',
                f'  pip-audit --format={pip_config["output_format"]} --output=dependency-scan-results/pip-audit.json || true',
                'fi'
            ])
        
        # Snyk
        if scanner_config.get('snyk', {}).get('enabled'):
            snyk_config = scanner_config['snyk']
            commands.extend([
                f'snyk test --json --severity-threshold={snyk_config["severity_threshold"]} > dependency-scan-results/snyk-test.json || true',
                'snyk monitor || true'
            ])
        
        # Safety (Python)
        if scanner_config.get('safety', {}).get('enabled'):
            safety_config = scanner_config['safety']
            commands.extend([
                'if [ -f "requirements.txt" ]; then',
                f'  safety check --json --output dependency-scan-results/safety.json || true',
                'fi'
            ])
        
        # Retire.js
        if scanner_config.get('retire_js', {}).get('enabled'):
            retire_config = scanner_config['retire_js']
            commands.extend([
                'if [ -f "package.json" ]; then',
                f'  retire --outputformat=json --outputpath=dependency-scan-results/retire-js.json || true',
                'fi'
            ])
        
        # OWASP Dependency Check
        if scanner_config.get('owasp_dependency_check', {}).get('enabled'):
            owasp_config = scanner_config['owasp_dependency_check']
            commands.extend([
                f'dependency-check.sh --project "Security Scan" --scan . --format JSON --format HTML --out dependency-scan-results/ --failOnCVSS {owasp_config["fail_build_on_cvss"]} || true'
            ])
        
        return ' && '.join(commands)
    
    def process_dependency_scan_results(self, results_path: str) -> Dict:
        """
        Process and consolidate dependency scan results
        """
        consolidated_results = {
            'scan_id': f"DEP-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            'scan_timestamp': datetime.now().isoformat(),
            'tools_used': [],
            'summary': {
                'total_vulnerabilities': 0,
                'critical_vulnerabilities': 0,
                'high_vulnerabilities': 0,
                'medium_vulnerabilities': 0,
                'low_vulnerabilities': 0,
                'packages_scanned': 0,
                'vulnerable_packages': 0
            },
            'vulnerabilities': [],
            'package_managers': [],
            'recommendations': []
        }
        
        # Process NPM Audit results
        npm_results_file = os.path.join(results_path, 'npm-audit.json')
        if os.path.exists(npm_results_file):
            npm_vulns = self.parse_npm_audit_results(npm_results_file)
            consolidated_results['tools_used'].append('npm-audit')
            consolidated_results['package_managers'].append('npm')
            consolidated_results['vulnerabilities'].extend(npm_vulns)
        
        # Process Snyk results
        snyk_results_file = os.path.join(results_path, 'snyk-test.json')
        if os.path.exists(snyk_results_file):
            snyk_vulns = self.parse_snyk_results(snyk_results_file)
            consolidated_results['tools_used'].append('snyk')
            consolidated_results['vulnerabilities'].extend(snyk_vulns)
        
        # Process Safety results
        safety_results_file = os.path.join(results_path, 'safety.json')
        if os.path.exists(safety_results_file):
            safety_vulns = self.parse_safety_results(safety_results_file)
            consolidated_results['tools_used'].append('safety')
            consolidated_results['package_managers'].append('pip')
            consolidated_results['vulnerabilities'].extend(safety_vulns)
        
        # Process OWASP Dependency Check results
        owasp_results_file = os.path.join(results_path, 'dependency-check-report.json')
        if os.path.exists(owasp_results_file):
            owasp_vulns = self.parse_owasp_dependency_check_results(owasp_results_file)
            consolidated_results['tools_used'].append('owasp-dependency-check')
            consolidated_results['vulnerabilities'].extend(owasp_vulns)
        
        # Calculate summary statistics
        consolidated_results = self.calculate_dependency_summary(consolidated_results)
        
        # Generate recommendations
        consolidated_results['recommendations'] = self.generate_dependency_recommendations(
            consolidated_results['vulnerabilities']
        )
        
        # Store results
        self.store_dependency_scan_results(consolidated_results)
        
        return consolidated_results
    
    def parse_npm_audit_results(self, results_file: str) -> List[Dict]:
        """
        Parse NPM audit results
        """
        vulnerabilities = []
        try:
            with open(results_file, 'r') as f:
                npm_data = json.load(f)
            
            for vuln_id, vuln_data in npm_data.get('vulnerabilities', {}).items():
                vulnerability = {
                    'tool': 'npm-audit',
                    'vulnerability_id': vuln_id,
                    'package_name': vuln_data.get('name'),
                    'installed_version': vuln_data.get('version'),
                    'severity': self.normalize_severity(vuln_data.get('severity')),
                    'title': vuln_data.get('title'),
                    'description': vuln_data.get('overview'),
                    'cwe_ids': vuln_data.get('cwe', []),
                    'cvss_score': vuln_data.get('cvss', {}).get('score'),
                    'references': vuln_data.get('references', []),
                    'patched_versions': vuln_data.get('patched_versions'),
                    'vulnerable_versions': vuln_data.get('vulnerable_versions'),
                    'recommendation': vuln_data.get('recommendation'),
                    'package_manager': 'npm'
                }
                vulnerabilities.append(vulnerability)
                
        except Exception as e:
            print(f"Error parsing NPM audit results: {e}")
        
        return vulnerabilities
    
    def parse_snyk_results(self, results_file: str) -> List[Dict]:
        """
        Parse Snyk scan results
        """
        vulnerabilities = []
        try:
            with open(results_file, 'r') as f:
                snyk_data = json.load(f)
            
            for vuln in snyk_data.get('vulnerabilities', []):
                vulnerability = {
                    'tool': 'snyk',
                    'vulnerability_id': vuln.get('id'),
                    'package_name': vuln.get('packageName'),
                    'installed_version': vuln.get('version'),
                    'severity': self.normalize_severity(vuln.get('severity')),
                    'title': vuln.get('title'),
                    'description': vuln.get('description'),
                    'cve_ids': [vuln.get('identifiers', {}).get('CVE', [])],
                    'cwe_ids': [vuln.get('identifiers', {}).get('CWE', [])],
                    'cvss_score': vuln.get('cvssScore'),
                    'references': vuln.get('references', []),
                    'upgrade_path': vuln.get('upgradePath', []),
                    'is_patchable': vuln.get('isPatchable', False),
                    'is_upgradable': vuln.get('isUpgradable', False),
                    'package_manager': vuln.get('packageManager', 'unknown')
                }
                vulnerabilities.append(vulnerability)
                
        except Exception as e:
            print(f"Error parsing Snyk results: {e}")
        
        return vulnerabilities
    
    def create_dependency_security_gates(self, gate_config: Dict) -> Dict:
        """
        Create security gates for dependency scanning
        """
        security_gates = {
            'gate_id': f"DEP-GATE-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            'gate_rules': {
                'critical_vulnerabilities_threshold': gate_config.get('critical_threshold', 0),
                'high_vulnerabilities_threshold': gate_config.get('high_threshold', 0),
                'medium_vulnerabilities_threshold': gate_config.get('medium_threshold', 10),
                'total_vulnerabilities_threshold': gate_config.get('total_threshold', 50),
                'cvss_score_threshold': gate_config.get('cvss_threshold', 7.0),
                'age_threshold_days': gate_config.get('age_threshold', 30),
                'allow_dev_dependencies': gate_config.get('allow_dev_deps', True)
            },
            'actions': {
                'block_deployment': gate_config.get('block_deployment', True),
                'create_security_tickets': gate_config.get('create_tickets', True),
                'notify_security_team': gate_config.get('notify_security', True),
                'auto_create_pr_for_updates': gate_config.get('auto_pr', False)
            },
            'exceptions': {
                'allowed_vulnerabilities': gate_config.get('allowed_vulns', []),
                'temporary_exceptions': gate_config.get('temp_exceptions', []),
                'business_justifications': gate_config.get('business_justifications', [])
            }
        }
        
        return security_gates
    
    def generate_dependency_recommendations(self, vulnerabilities: List[Dict]) -> List[Dict]:
        """
        Generate actionable recommendations for dependency vulnerabilities
        """
        recommendations = []
        
        # Group vulnerabilities by package
        packages_with_vulns = {}
        for vuln in vulnerabilities:
            package_name = vuln.get('package_name')
            if package_name not in packages_with_vulns:
                packages_with_vulns[package_name] = []
            packages_with_vulns[package_name].append(vuln)
        
        # Generate recommendations for each package
        for package_name, package_vulns in packages_with_vulns.items():
            highest_severity = max(
                [self.severity_to_numeric(v.get('severity', 'LOW')) for v in package_vulns]
            )
            
            recommendation = {
                'package_name': package_name,
                'vulnerability_count': len(package_vulns),
                'highest_severity': self.numeric_to_severity(highest_severity),
                'recommendation_type': 'UPDATE',
                'priority': 'HIGH' if highest_severity >= 3 else 'MEDIUM',
                'actions': []
            }
            
            # Check if updates are available
            upgradable_vulns = [v for v in package_vulns if v.get('is_upgradable')]
            if upgradable_vulns:
                recommendation['actions'].append({
                    'action': 'UPDATE_PACKAGE',
                    'description': f'Update {package_name} to latest secure version',
                    'automated': True,
                    'effort_estimate': 'LOW'
                })
            
            # Check if patches are available
            patchable_vulns = [v for v in package_vulns if v.get('is_patchable')]
            if patchable_vulns:
                recommendation['actions'].append({
                    'action': 'APPLY_PATCH',
                    'description': f'Apply security patches for {package_name}',
                    'automated': True,
                    'effort_estimate': 'LOW'
                })
            
            # If no automatic fixes available
            if not upgradable_vulns and not patchable_vulns:
                recommendation['actions'].append({
                    'action': 'MANUAL_REVIEW',
                    'description': f'Manual review required for {package_name} vulnerabilities',
                    'automated': False,
                    'effort_estimate': 'HIGH'
                })
            
            recommendations.append(recommendation)
        
        return recommendations

# Example usage
dependency_scanner = DependencyScanning()

# Configure dependency scanners
project_config = {
    'project_name': 'secure-web-app',
    'languages': ['python', 'javascript'],
    'manifest_files': ['package.json', 'requirements.txt'],
    'ignored_vulnerabilities': ['GHSA-example-1234'],
    'safety_ignore_ids': ['12345']
}

scanner_config = dependency_scanner.configure_dependency_scanners(project_config)
print("Dependency Scanner Configuration:")
print(json.dumps(scanner_config, indent=2))

# Create dependency scan pipeline
pipeline_arn = dependency_scanner.create_dependency_scan_pipeline({
    **scanner_config,
    'project_name': project_config['project_name'],
    'results_bucket': 'dependency-scan-results-bucket'
})
print(f"\\nDependency Scan Pipeline ARN: {pipeline_arn}")
```
### Step 4: Implement Infrastructure as Code (IaC) Security Testing

Deploy IaC security scanning tools to identify misconfigurations and security issues in infrastructure code:

```python
# Infrastructure as Code Security Testing Framework
import boto3
import json
import yaml
import subprocess
import os
from datetime import datetime
from typing import Dict, List, Optional

class IaCSecurityTesting:
    def __init__(self):
        self.codebuild = boto3.client('codebuild')
        self.s3 = boto3.client('s3')
        self.dynamodb = boto3.resource('dynamodb')
        self.results_table = self.dynamodb.Table('iac-scan-results')
        
    def configure_iac_scanners(self, project_config: Dict) -> Dict:
        """
        Configure IaC security scanning tools
        """
        scanner_config = {
            'checkov': {
                'enabled': True,
                'frameworks': ['cloudformation', 'terraform', 'kubernetes', 'dockerfile'],
                'severity_threshold': 'MEDIUM',
                'output_format': 'json',
                'skip_checks': project_config.get('checkov_skip_checks', []),
                'custom_policies_dir': 'security/checkov-policies',
                'enable_secrets_scan': True
            },
            'tfsec': {
                'enabled': 'terraform' in project_config.get('iac_types', []),
                'severity_threshold': 'MEDIUM',
                'output_format': 'json',
                'exclude_checks': project_config.get('tfsec_exclude_checks', []),
                'custom_checks_dir': 'security/tfsec-checks',
                'include_ignored': False
            },
            'cfn_nag': {
                'enabled': 'cloudformation' in project_config.get('iac_types', []),
                'output_format': 'json',
                'rule_directory': 'security/cfn-nag-rules',
                'profile_path': 'security/cfn-nag-profile.json',
                'fail_on_warnings': True
            },
            'kube_score': {
                'enabled': 'kubernetes' in project_config.get('iac_types', []),
                'output_format': 'json',
                'ignore_tests': project_config.get('kube_score_ignore', []),
                'enable_optional_tests': True
            },
            'terrascan': {
                'enabled': True,
                'policy_type': ['aws', 'azure', 'gcp', 'kubernetes'],
                'severity': 'medium',
                'output_format': 'json',
                'config_file': 'security/terrascan-config.toml',
                'skip_rules': project_config.get('terrascan_skip_rules', [])
            },
            'aws_config_rules': {
                'enabled': 'cloudformation' in project_config.get('iac_types', []),
                'rule_sets': ['security-best-practices', 'operational-best-practices'],
                'custom_rules': project_config.get('custom_config_rules', [])
            }
        }
        
        return scanner_config
    
    def create_iac_scan_pipeline(self, scanner_config: Dict) -> str:
        """
        Create CodeBuild project for IaC security scanning
        """
        buildspec = {
            'version': '0.2',
            'phases': {
                'install': {
                    'runtime-versions': {
                        'python': '3.9',
                        'nodejs': '16'
                    },
                    'commands': [
                        'echo "Installing IaC security scanners..."',
                        'pip install checkov',
                        'curl -s https://raw.githubusercontent.com/aquasecurity/tfsec/master/scripts/install_linux.sh | bash',
                        'gem install cfn-nag',
                        'wget -O kube-score.tar.gz https://github.com/zegl/kube-score/releases/download/v1.16.1/kube-score_1.16.1_linux_amd64.tar.gz',
                        'tar -xzf kube-score.tar.gz',
                        'chmod +x kube-score',
                        'mv kube-score /usr/local/bin/',
                        'curl -L "$(curl -s https://api.github.com/repos/tenable/terrascan/releases/latest | grep -o -E "https://.+?_Linux_x86_64.tar.gz")" > terrascan.tar.gz',
                        'tar -xf terrascan.tar.gz terrascan && rm terrascan.tar.gz',
                        'install terrascan /usr/local/bin && rm terrascan'
                    ]
                },
                'pre_build': {
                    'commands': [
                        'echo "Preparing IaC security scan..."',
                        'mkdir -p iac-scan-results',
                        'echo "Discovering IaC files..."',
                        'find . -name "*.tf" -o -name "*.yaml" -o -name "*.yml" -o -name "*.json" -o -name "Dockerfile" | grep -E "\\.(tf|yaml|yml|json|Dockerfile)$" | tee iac-files.txt'
                    ]
                },
                'build': {
                    'commands': [
                        'echo "Running IaC security scans..."',
                        self.generate_iac_scan_commands(scanner_config)
                    ]
                },
                'post_build': {
                    'commands': [
                        'echo "Processing IaC scan results..."',
                        'python scripts/consolidate_iac_results.py',
                        'aws s3 cp iac-scan-results/ s3://$IAC_SCAN_BUCKET/$(date +%Y%m%d-%H%M%S)/ --recursive'
                    ]
                }
            },
            'artifacts': {
                'files': [
                    'iac-scan-results/**/*'
                ]
            }
        }
        
        project_config = {
            'name': f"iac-scan-{scanner_config['project_name']}",
            'source': {
                'type': 'CODEPIPELINE',
                'buildspec': json.dumps(buildspec, indent=2)
            },
            'artifacts': {
                'type': 'CODEPIPELINE'
            },
            'environment': {
                'type': 'LINUX_CONTAINER',
                'image': 'aws/codebuild/amazonlinux2-x86_64-standard:3.0',
                'computeType': 'BUILD_GENERAL1_MEDIUM',
                'environmentVariables': [
                    {
                        'name': 'IAC_SCAN_BUCKET',
                        'value': scanner_config.get('results_bucket', 'iac-scan-results')
                    }
                ]
            },
            'serviceRole': scanner_config.get('service_role_arn')
        }
        
        response = self.codebuild.create_project(**project_config)
        return response['project']['arn']
    
    def generate_iac_scan_commands(self, scanner_config: Dict) -> str:
        """
        Generate IaC scanning commands based on enabled tools
        """
        commands = []
        
        # Checkov scan
        if scanner_config.get('checkov', {}).get('enabled'):
            checkov_config = scanner_config['checkov']
            frameworks = ','.join(checkov_config['frameworks'])
            skip_checks = ','.join(checkov_config.get('skip_checks', []))
            
            checkov_cmd = [
                'checkov',
                '--directory .',
                f'--framework {frameworks}',
                f'--output {checkov_config["output_format"]}',
                '--output-file iac-scan-results/checkov-results.json'
            ]
            
            if skip_checks:
                checkov_cmd.append(f'--skip-check {skip_checks}')
            
            if checkov_config.get('enable_secrets_scan'):
                checkov_cmd.append('--enable-secret-scan-all-files')
            
            commands.append(' '.join(checkov_cmd) + ' || true')
        
        # TFSec scan
        if scanner_config.get('tfsec', {}).get('enabled'):
            tfsec_config = scanner_config['tfsec']
            exclude_checks = ','.join(tfsec_config.get('exclude_checks', []))
            
            tfsec_cmd = [
                'tfsec .',
                f'--format {tfsec_config["output_format"]}',
                '--out iac-scan-results/tfsec-results.json'
            ]
            
            if exclude_checks:
                tfsec_cmd.append(f'--exclude-checks {exclude_checks}')
            
            commands.append(' '.join(tfsec_cmd) + ' || true')
        
        # CFN-Nag scan
        if scanner_config.get('cfn_nag', {}).get('enabled'):
            cfn_nag_config = scanner_config['cfn_nag']
            commands.extend([
                'find . -name "*.yaml" -o -name "*.yml" -o -name "*.json" | grep -E "template|cloudformation" > cf-templates.txt || true',
                'if [ -s cf-templates.txt ]; then',
                f'  cfn_nag_scan --input-path . --output-format {cfn_nag_config["output_format"]} --output-file iac-scan-results/cfn-nag-results.json || true',
                'fi'
            ])
        
        # Kube-score scan
        if scanner_config.get('kube_score', {}).get('enabled'):
            kube_score_config = scanner_config['kube_score']
            commands.extend([
                'find . -name "*.yaml" -o -name "*.yml" | grep -E "k8s|kubernetes|deployment|service" > k8s-files.txt || true',
                'if [ -s k8s-files.txt ]; then',
                f'  kube-score score --output-format {kube_score_config["output_format"]} $(cat k8s-files.txt) > iac-scan-results/kube-score-results.json || true',
                'fi'
            ])
        
        # Terrascan
        if scanner_config.get('terrascan', {}).get('enabled'):
            terrascan_config = scanner_config['terrascan']
            policy_types = ','.join(terrascan_config['policy_type'])
            
            terrascan_cmd = [
                'terrascan scan',
                '--iac-type all',
                f'--policy-type {policy_types}',
                f'--severity {terrascan_config["severity"]}',
                f'--output {terrascan_config["output_format"]}',
                '--output-file iac-scan-results/terrascan-results.json'
            ]
            
            commands.append(' '.join(terrascan_cmd) + ' || true')
        
        return ' && '.join(commands)
    
    def process_iac_scan_results(self, results_path: str) -> Dict:
        """
        Process and consolidate IaC scan results
        """
        consolidated_results = {
            'scan_id': f"IAC-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            'scan_timestamp': datetime.now().isoformat(),
            'tools_used': [],
            'summary': {
                'total_issues': 0,
                'critical_issues': 0,
                'high_issues': 0,
                'medium_issues': 0,
                'low_issues': 0,
                'info_issues': 0,
                'files_scanned': 0,
                'passed_checks': 0,
                'failed_checks': 0
            },
            'issues_by_category': {},
            'issues_by_resource_type': {},
            'detailed_findings': [],
            'compliance_status': {},
            'remediation_suggestions': []
        }
        
        # Process Checkov results
        checkov_results_file = os.path.join(results_path, 'checkov-results.json')
        if os.path.exists(checkov_results_file):
            checkov_issues = self.parse_checkov_results(checkov_results_file)
            consolidated_results['tools_used'].append('checkov')
            consolidated_results['detailed_findings'].extend(checkov_issues)
        
        # Process TFSec results
        tfsec_results_file = os.path.join(results_path, 'tfsec-results.json')
        if os.path.exists(tfsec_results_file):
            tfsec_issues = self.parse_tfsec_results(tfsec_results_file)
            consolidated_results['tools_used'].append('tfsec')
            consolidated_results['detailed_findings'].extend(tfsec_issues)
        
        # Process CFN-Nag results
        cfn_nag_results_file = os.path.join(results_path, 'cfn-nag-results.json')
        if os.path.exists(cfn_nag_results_file):
            cfn_nag_issues = self.parse_cfn_nag_results(cfn_nag_results_file)
            consolidated_results['tools_used'].append('cfn-nag')
            consolidated_results['detailed_findings'].extend(cfn_nag_issues)
        
        # Process Terrascan results
        terrascan_results_file = os.path.join(results_path, 'terrascan-results.json')
        if os.path.exists(terrascan_results_file):
            terrascan_issues = self.parse_terrascan_results(terrascan_results_file)
            consolidated_results['tools_used'].append('terrascan')
            consolidated_results['detailed_findings'].extend(terrascan_issues)
        
        # Calculate summary statistics
        consolidated_results = self.calculate_iac_summary(consolidated_results)
        
        # Generate compliance status
        consolidated_results['compliance_status'] = self.assess_compliance_status(
            consolidated_results['detailed_findings']
        )
        
        # Generate remediation suggestions
        consolidated_results['remediation_suggestions'] = self.generate_iac_remediation_suggestions(
            consolidated_results['detailed_findings']
        )
        
        # Store results
        self.store_iac_scan_results(consolidated_results)
        
        return consolidated_results
    
    def parse_checkov_results(self, results_file: str) -> List[Dict]:
        """
        Parse Checkov scan results
        """
        issues = []
        try:
            with open(results_file, 'r') as f:
                checkov_data = json.load(f)
            
            for result in checkov_data.get('results', {}).get('failed_checks', []):
                issue = {
                    'tool': 'checkov',
                    'check_id': result.get('check_id'),
                    'check_name': result.get('check_name'),
                    'severity': self.normalize_severity(result.get('severity', 'MEDIUM')),
                    'resource_type': result.get('resource'),
                    'resource_name': result.get('resource_name', ''),
                    'file_path': result.get('file_path'),
                    'line_range': result.get('file_line_range', []),
                    'description': result.get('description'),
                    'guideline': result.get('guideline'),
                    'category': self.categorize_iac_issue(result.get('check_id', '')),
                    'remediation': result.get('fixed_definition'),
                    'compliance_frameworks': result.get('bc_check_id', '').split('_')[0] if result.get('bc_check_id') else None
                }
                issues.append(issue)
                
        except Exception as e:
            print(f"Error parsing Checkov results: {e}")
        
        return issues
    
    def parse_tfsec_results(self, results_file: str) -> List[Dict]:
        """
        Parse TFSec scan results
        """
        issues = []
        try:
            with open(results_file, 'r') as f:
                tfsec_data = json.load(f)
            
            for result in tfsec_data.get('results', []):
                issue = {
                    'tool': 'tfsec',
                    'check_id': result.get('rule_id'),
                    'check_name': result.get('rule_description'),
                    'severity': self.normalize_severity(result.get('severity', 'MEDIUM')),
                    'resource_type': result.get('resource_type'),
                    'resource_name': result.get('resource_name', ''),
                    'file_path': result.get('location', {}).get('filename'),
                    'line_range': [result.get('location', {}).get('start_line', 0)],
                    'description': result.get('description'),
                    'impact': result.get('impact'),
                    'resolution': result.get('resolution'),
                    'category': self.categorize_iac_issue(result.get('rule_id', '')),
                    'links': result.get('links', [])
                }
                issues.append(issue)
                
        except Exception as e:
            print(f"Error parsing TFSec results: {e}")
        
        return issues
    
    def categorize_iac_issue(self, check_id: str) -> str:
        """
        Categorize IaC security issues
        """
        category_mapping = {
            'encryption': ['encrypt', 'kms', 'ssl', 'tls'],
            'access_control': ['iam', 'policy', 'permission', 'access'],
            'network_security': ['security_group', 'nacl', 'vpc', 'subnet'],
            'logging_monitoring': ['logging', 'cloudtrail', 'monitoring'],
            'backup_recovery': ['backup', 'snapshot', 'versioning'],
            'compliance': ['compliance', 'cis', 'pci', 'hipaa'],
            'secrets_management': ['secret', 'password', 'key', 'credential'],
            'resource_configuration': ['config', 'setting', 'parameter']
        }
        
        check_id_lower = check_id.lower()
        for category, keywords in category_mapping.items():
            if any(keyword in check_id_lower for keyword in keywords):
                return category
        
        return 'other'
    
    def assess_compliance_status(self, findings: List[Dict]) -> Dict:
        """
        Assess compliance status based on findings
        """
        compliance_frameworks = {
            'CIS': {'total_checks': 0, 'passed_checks': 0, 'failed_checks': 0},
            'PCI-DSS': {'total_checks': 0, 'passed_checks': 0, 'failed_checks': 0},
            'SOC2': {'total_checks': 0, 'passed_checks': 0, 'failed_checks': 0},
            'NIST': {'total_checks': 0, 'passed_checks': 0, 'failed_checks': 0}
        }
        
        for finding in findings:
            # Map findings to compliance frameworks
            frameworks = self.map_finding_to_compliance(finding)
            for framework in frameworks:
                if framework in compliance_frameworks:
                    compliance_frameworks[framework]['total_checks'] += 1
                    compliance_frameworks[framework]['failed_checks'] += 1
        
        # Calculate compliance percentages
        for framework, stats in compliance_frameworks.items():
            if stats['total_checks'] > 0:
                stats['compliance_percentage'] = (
                    stats['passed_checks'] / stats['total_checks']
                ) * 100
            else:
                stats['compliance_percentage'] = 100
        
        return compliance_frameworks
    
    def generate_iac_remediation_suggestions(self, findings: List[Dict]) -> List[Dict]:
        """
        Generate remediation suggestions for IaC issues
        """
        suggestions = []
        
        # Group findings by category
        findings_by_category = {}
        for finding in findings:
            category = finding.get('category', 'other')
            if category not in findings_by_category:
                findings_by_category[category] = []
            findings_by_category[category].append(finding)
        
        # Generate category-specific suggestions
        for category, category_findings in findings_by_category.items():
            suggestion = {
                'category': category,
                'issue_count': len(category_findings),
                'priority': self.calculate_category_priority(category_findings),
                'remediation_steps': self.get_category_remediation_steps(category),
                'automation_potential': self.assess_automation_potential(category),
                'estimated_effort': self.estimate_remediation_effort(category_findings)
            }
            suggestions.append(suggestion)
        
        return suggestions
    
    def create_iac_security_policies(self, policy_config: Dict) -> Dict:
        """
        Create custom security policies for IaC scanning
        """
        policies = {
            'checkov_custom_policies': self.create_checkov_policies(policy_config),
            'tfsec_custom_checks': self.create_tfsec_checks(policy_config),
            'cfn_nag_custom_rules': self.create_cfn_nag_rules(policy_config),
            'terrascan_custom_policies': self.create_terrascan_policies(policy_config)
        }
        
        return policies
    
    def create_checkov_policies(self, policy_config: Dict) -> List[Dict]:
        """
        Create custom Checkov policies
        """
        custom_policies = [
            {
                'policy_name': 'CompanyS3BucketEncryption',
                'policy_description': 'Ensure S3 buckets use company-approved encryption',
                'resource_types': ['aws_s3_bucket'],
                'check_logic': {
                    'condition': 'encryption.server_side_encryption_configuration.rule.apply_server_side_encryption_by_default.sse_algorithm',
                    'operator': 'in',
                    'value': ['AES256', 'aws:kms']
                },
                'severity': 'HIGH',
                'category': 'encryption'
            },
            {
                'policy_name': 'CompanyIAMPasswordPolicy',
                'policy_description': 'Ensure IAM password policy meets company requirements',
                'resource_types': ['aws_iam_account_password_policy'],
                'check_logic': {
                    'conditions': [
                        {'field': 'minimum_password_length', 'operator': '>=', 'value': 12},
                        {'field': 'require_uppercase_characters', 'operator': '==', 'value': True},
                        {'field': 'require_lowercase_characters', 'operator': '==', 'value': True},
                        {'field': 'require_numbers', 'operator': '==', 'value': True},
                        {'field': 'require_symbols', 'operator': '==', 'value': True}
                    ]
                },
                'severity': 'MEDIUM',
                'category': 'access_control'
            }
        ]
        
        return custom_policies

# Example usage
iac_scanner = IaCSecurityTesting()

# Configure IaC scanners
project_config = {
    'project_name': 'secure-infrastructure',
    'iac_types': ['terraform', 'cloudformation', 'kubernetes'],
    'checkov_skip_checks': ['CKV_AWS_20'],
    'tfsec_exclude_checks': ['aws-s3-enable-logging'],
    'terrascan_skip_rules': ['AC_AWS_0001']
}

scanner_config = iac_scanner.configure_iac_scanners(project_config)
print("IaC Scanner Configuration:")
print(json.dumps(scanner_config, indent=2))

# Create IaC scan pipeline
pipeline_arn = iac_scanner.create_iac_scan_pipeline({
    **scanner_config,
    'project_name': project_config['project_name'],
    'results_bucket': 'iac-scan-results-bucket'
})
print(f"\\nIaC Scan Pipeline ARN: {pipeline_arn}")
```
### Step 5: Integrate Security Testing into CI/CD Pipeline

Create a comprehensive CI/CD pipeline that integrates all security testing tools:

```python
# Comprehensive Security Testing CI/CD Pipeline
import boto3
import json
from datetime import datetime
from typing import Dict, List, Optional

class SecurityTestingPipeline:
    def __init__(self):
        self.codepipeline = boto3.client('codepipeline')
        self.codebuild = boto3.client('codebuild')
        self.s3 = boto3.client('s3')
        self.sns = boto3.client('sns')
        self.dynamodb = boto3.resource('dynamodb')
        
    def create_comprehensive_security_pipeline(self, pipeline_config: Dict) -> Dict:
        """
        Create comprehensive security testing pipeline
        """
        pipeline_definition = {
            'name': f"security-pipeline-{pipeline_config['application_name']}",
            'roleArn': pipeline_config['pipeline_role_arn'],
            'artifactStore': {
                'type': 'S3',
                'location': pipeline_config['artifact_bucket']
            },
            'stages': [
                # Stage 1: Source
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
                                'RepositoryName': pipeline_config['repository_name'],
                                'BranchName': pipeline_config.get('branch_name', 'main')
                            },
                            'outputArtifacts': [{'name': 'SourceOutput'}]
                        }
                    ]
                },
                
                # Stage 2: Pre-commit Security Checks
                {
                    'name': 'PreCommitSecurity',
                    'actions': [
                        {
                            'name': 'SecretsScanning',
                            'actionTypeId': {
                                'category': 'Build',
                                'owner': 'AWS',
                                'provider': 'CodeBuild',
                                'version': '1'
                            },
                            'configuration': {
                                'ProjectName': f"secrets-scan-{pipeline_config['application_name']}"
                            },
                            'inputArtifacts': [{'name': 'SourceOutput'}],
                            'outputArtifacts': [{'name': 'SecretsOutput'}],
                            'runOrder': 1
                        },
                        {
                            'name': 'LicenseCompliance',
                            'actionTypeId': {
                                'category': 'Build',
                                'owner': 'AWS',
                                'provider': 'CodeBuild',
                                'version': '1'
                            },
                            'configuration': {
                                'ProjectName': f"license-check-{pipeline_config['application_name']}"
                            },
                            'inputArtifacts': [{'name': 'SourceOutput'}],
                            'outputArtifacts': [{'name': 'LicenseOutput'}],
                            'runOrder': 1
                        }
                    ]
                },
                
                # Stage 3: Static Analysis Security Testing (SAST)
                {
                    'name': 'StaticAnalysis',
                    'actions': [
                        {
                            'name': 'SASTScan',
                            'actionTypeId': {
                                'category': 'Build',
                                'owner': 'AWS',
                                'provider': 'CodeBuild',
                                'version': '1'
                            },
                            'configuration': {
                                'ProjectName': f"sast-scan-{pipeline_config['application_name']}"
                            },
                            'inputArtifacts': [{'name': 'SourceOutput'}],
                            'outputArtifacts': [{'name': 'SASTOutput'}],
                            'runOrder': 1
                        },
                        {
                            'name': 'IaCScan',
                            'actionTypeId': {
                                'category': 'Build',
                                'owner': 'AWS',
                                'provider': 'CodeBuild',
                                'version': '1'
                            },
                            'configuration': {
                                'ProjectName': f"iac-scan-{pipeline_config['application_name']}"
                            },
                            'inputArtifacts': [{'name': 'SourceOutput'}],
                            'outputArtifacts': [{'name': 'IaCOutput'}],
                            'runOrder': 1
                        }
                    ]
                },
                
                # Stage 4: Dependency Security Testing
                {
                    'name': 'DependencyAnalysis',
                    'actions': [
                        {
                            'name': 'DependencyScan',
                            'actionTypeId': {
                                'category': 'Build',
                                'owner': 'AWS',
                                'provider': 'CodeBuild',
                                'version': '1'
                            },
                            'configuration': {
                                'ProjectName': f"dependency-scan-{pipeline_config['application_name']}"
                            },
                            'inputArtifacts': [{'name': 'SourceOutput'}],
                            'outputArtifacts': [{'name': 'DependencyOutput'}],
                            'runOrder': 1
                        }
                    ]
                },
                
                # Stage 5: Build and Package
                {
                    'name': 'Build',
                    'actions': [
                        {
                            'name': 'BuildApplication',
                            'actionTypeId': {
                                'category': 'Build',
                                'owner': 'AWS',
                                'provider': 'CodeBuild',
                                'version': '1'
                            },
                            'configuration': {
                                'ProjectName': f"build-{pipeline_config['application_name']}"
                            },
                            'inputArtifacts': [{'name': 'SourceOutput'}],
                            'outputArtifacts': [{'name': 'BuildOutput'}],
                            'runOrder': 1
                        }
                    ]
                },
                
                # Stage 6: Container Security Scanning
                {
                    'name': 'ContainerSecurity',
                    'actions': [
                        {
                            'name': 'ContainerScan',
                            'actionTypeId': {
                                'category': 'Build',
                                'owner': 'AWS',
                                'provider': 'CodeBuild',
                                'version': '1'
                            },
                            'configuration': {
                                'ProjectName': f"container-scan-{pipeline_config['application_name']}"
                            },
                            'inputArtifacts': [{'name': 'BuildOutput'}],
                            'outputArtifacts': [{'name': 'ContainerOutput'}],
                            'runOrder': 1
                        }
                    ]
                },
                
                # Stage 7: Deploy to Test Environment
                {
                    'name': 'DeployTest',
                    'actions': [
                        {
                            'name': 'DeployToTest',
                            'actionTypeId': {
                                'category': 'Deploy',
                                'owner': 'AWS',
                                'provider': 'ECS',
                                'version': '1'
                            },
                            'configuration': {
                                'ClusterName': pipeline_config['test_cluster'],
                                'ServiceName': f"test-{pipeline_config['application_name']}",
                                'FileName': 'imagedefinitions.json'
                            },
                            'inputArtifacts': [{'name': 'BuildOutput'}],
                            'runOrder': 1
                        }
                    ]
                },
                
                # Stage 8: Dynamic Application Security Testing (DAST)
                {
                    'name': 'DynamicTesting',
                    'actions': [
                        {
                            'name': 'DASTScan',
                            'actionTypeId': {
                                'category': 'Build',
                                'owner': 'AWS',
                                'provider': 'CodeBuild',
                                'version': '1'
                            },
                            'configuration': {
                                'ProjectName': f"dast-scan-{pipeline_config['application_name']}"
                            },
                            'inputArtifacts': [{'name': 'BuildOutput'}],
                            'outputArtifacts': [{'name': 'DASTOutput'}],
                            'runOrder': 1
                        },
                        {
                            'name': 'APISecurityTest',
                            'actionTypeId': {
                                'category': 'Build',
                                'owner': 'AWS',
                                'provider': 'CodeBuild',
                                'version': '1'
                            },
                            'configuration': {
                                'ProjectName': f"api-security-test-{pipeline_config['application_name']}"
                            },
                            'inputArtifacts': [{'name': 'BuildOutput'}],
                            'outputArtifacts': [{'name': 'APITestOutput'}],
                            'runOrder': 2
                        }
                    ]
                },
                
                # Stage 9: Security Gate and Approval
                {
                    'name': 'SecurityGate',
                    'actions': [
                        {
                            'name': 'SecurityResultsConsolidation',
                            'actionTypeId': {
                                'category': 'Build',
                                'owner': 'AWS',
                                'provider': 'CodeBuild',
                                'version': '1'
                            },
                            'configuration': {
                                'ProjectName': f"security-gate-{pipeline_config['application_name']}"
                            },
                            'inputArtifacts': [
                                {'name': 'SASTOutput'},
                                {'name': 'DependencyOutput'},
                                {'name': 'IaCOutput'},
                                {'name': 'DASTOutput'},
                                {'name': 'ContainerOutput'}
                            ],
                            'outputArtifacts': [{'name': 'SecurityGateOutput'}],
                            'runOrder': 1
                        },
                        {
                            'name': 'SecurityApproval',
                            'actionTypeId': {
                                'category': 'Approval',
                                'owner': 'AWS',
                                'provider': 'Manual',
                                'version': '1'
                            },
                            'configuration': {
                                'NotificationArn': pipeline_config['approval_topic_arn'],
                                'CustomData': 'Please review security scan results before approving deployment to production.'
                            },
                            'runOrder': 2
                        }
                    ]
                },
                
                # Stage 10: Production Deployment
                {
                    'name': 'DeployProduction',
                    'actions': [
                        {
                            'name': 'DeployToProduction',
                            'actionTypeId': {
                                'category': 'Deploy',
                                'owner': 'AWS',
                                'provider': 'ECS',
                                'version': '1'
                            },
                            'configuration': {
                                'ClusterName': pipeline_config['prod_cluster'],
                                'ServiceName': f"prod-{pipeline_config['application_name']}",
                                'FileName': 'imagedefinitions.json'
                            },
                            'inputArtifacts': [{'name': 'BuildOutput'}],
                            'runOrder': 1
                        }
                    ]
                }
            ]
        }
        
        # Create the pipeline
        response = self.codepipeline.create_pipeline(pipeline=pipeline_definition)
        
        return {
            'pipeline_name': pipeline_definition['name'],
            'pipeline_arn': response['pipeline']['name'],
            'stages_count': len(pipeline_definition['stages']),
            'security_stages': [
                'PreCommitSecurity',
                'StaticAnalysis', 
                'DependencyAnalysis',
                'ContainerSecurity',
                'DynamicTesting',
                'SecurityGate'
            ]
        }
    
    def create_security_gate_logic(self, gate_config: Dict) -> Dict:
        """
        Create security gate logic for pipeline
        """
        security_gate_buildspec = {
            'version': '0.2',
            'phases': {
                'install': {
                    'runtime-versions': {
                        'python': '3.9'
                    },
                    'commands': [
                        'pip install boto3 jq'
                    ]
                },
                'build': {
                    'commands': [
                        'echo "Consolidating security scan results..."',
                        'python scripts/security_gate_processor.py',
                        'echo "Applying security gates..."',
                        'python scripts/apply_security_gates.py'
                    ]
                }
            },
            'artifacts': {
                'files': [
                    'security-gate-report.json',
                    'security-gate-decision.json'
                ]
            }
        }
        
        gate_logic = {
            'buildspec': security_gate_buildspec,
            'gate_rules': {
                'critical_vulnerabilities_threshold': gate_config.get('critical_threshold', 0),
                'high_vulnerabilities_threshold': gate_config.get('high_threshold', 5),
                'medium_vulnerabilities_threshold': gate_config.get('medium_threshold', 20),
                'dependency_vulnerabilities_threshold': gate_config.get('dependency_threshold', 10),
                'iac_violations_threshold': gate_config.get('iac_threshold', 15),
                'container_vulnerabilities_threshold': gate_config.get('container_threshold', 8),
                'dast_findings_threshold': gate_config.get('dast_threshold', 12)
            },
            'gate_actions': {
                'block_deployment_on_critical': True,
                'require_approval_on_high': True,
                'auto_create_security_tickets': True,
                'notify_security_team': True,
                'generate_security_report': True
            }
        }
        
        return gate_logic
    
    def create_security_dashboard(self, dashboard_config: Dict) -> Dict:
        """
        Create security testing dashboard
        """
        dashboard_definition = {
            'dashboard_name': f"SecurityTesting-{dashboard_config['application_name']}",
            'widgets': [
                {
                    'type': 'metric',
                    'properties': {
                        'metrics': [
                            ['AWS/CodePipeline', 'PipelineExecutionSuccess', 'PipelineName', dashboard_config['pipeline_name']],
                            ['AWS/CodePipeline', 'PipelineExecutionFailure', 'PipelineName', dashboard_config['pipeline_name']]
                        ],
                        'period': 300,
                        'stat': 'Sum',
                        'region': 'us-east-1',
                        'title': 'Pipeline Execution Status'
                    }
                },
                {
                    'type': 'log',
                    'properties': {
                        'query': f'''
                        SOURCE '/aws/codebuild/sast-scan-{dashboard_config["application_name"]}'
                        | fields @timestamp, @message
                        | filter @message like /CRITICAL|HIGH/
                        | sort @timestamp desc
                        | limit 100
                        ''',
                        'region': 'us-east-1',
                        'title': 'Critical Security Findings',
                        'view': 'table'
                    }
                },
                {
                    'type': 'metric',
                    'properties': {
                        'metrics': [
                            ['Custom/Security', 'VulnerabilitiesFound', 'Application', dashboard_config['application_name'], 'Severity', 'Critical'],
                            ['Custom/Security', 'VulnerabilitiesFound', 'Application', dashboard_config['application_name'], 'Severity', 'High'],
                            ['Custom/Security', 'VulnerabilitiesFound', 'Application', dashboard_config['application_name'], 'Severity', 'Medium']
                        ],
                        'period': 3600,
                        'stat': 'Average',
                        'region': 'us-east-1',
                        'title': 'Vulnerability Trends'
                    }
                }
            ]
        }
        
        return dashboard_definition
    
    def implement_security_feedback_loop(self, feedback_config: Dict) -> Dict:
        """
        Implement security feedback loop for continuous improvement
        """
        feedback_system = {
            'automated_feedback': {
                'vulnerability_trending': {
                    'enabled': True,
                    'analysis_period_days': 30,
                    'trend_threshold_percentage': 20,
                    'notification_channels': ['slack', 'email', 'jira']
                },
                'false_positive_learning': {
                    'enabled': True,
                    'ml_model_training': True,
                    'feedback_collection_method': 'developer_annotation',
                    'model_update_frequency': 'weekly'
                },
                'security_metrics_tracking': {
                    'enabled': True,
                    'metrics': [
                        'mean_time_to_detection',
                        'mean_time_to_remediation',
                        'vulnerability_density',
                        'security_debt_ratio',
                        'compliance_score'
                    ],
                    'reporting_frequency': 'daily'
                }
            },
            'manual_feedback': {
                'security_champion_reviews': {
                    'enabled': True,
                    'review_frequency': 'weekly',
                    'review_scope': ['high_severity_findings', 'new_vulnerability_types'],
                    'feedback_integration': 'tool_configuration_updates'
                },
                'developer_feedback_collection': {
                    'enabled': True,
                    'feedback_methods': ['survey', 'interview', 'tool_usage_analytics'],
                    'feedback_frequency': 'monthly',
                    'improvement_tracking': True
                }
            },
            'continuous_improvement': {
                'tool_effectiveness_analysis': {
                    'enabled': True,
                    'analysis_metrics': [
                        'true_positive_rate',
                        'false_positive_rate',
                        'coverage_percentage',
                        'performance_impact'
                    ],
                    'improvement_actions': [
                        'tool_configuration_tuning',
                        'custom_rule_development',
                        'tool_replacement_evaluation'
                    ]
                },
                'process_optimization': {
                    'enabled': True,
                    'optimization_areas': [
                        'scan_execution_time',
                        'result_processing_efficiency',
                        'developer_workflow_integration',
                        'security_gate_accuracy'
                    ]
                }
            }
        }
        
        return feedback_system

# Example usage
security_pipeline = SecurityTestingPipeline()

# Configure comprehensive security pipeline
pipeline_config = {
    'application_name': 'secure-web-app',
    'repository_name': 'secure-web-app-repo',
    'branch_name': 'main',
    'pipeline_role_arn': 'arn:aws:iam::123456789012:role/CodePipelineServiceRole',
    'artifact_bucket': 'security-pipeline-artifacts',
    'test_cluster': 'test-cluster',
    'prod_cluster': 'prod-cluster',
    'approval_topic_arn': 'arn:aws:sns:us-east-1:123456789012:security-approval'
}

# Create comprehensive security pipeline
pipeline_result = security_pipeline.create_comprehensive_security_pipeline(pipeline_config)
print("Security Pipeline Created:")
print(json.dumps(pipeline_result, indent=2))

# Create security gate logic
gate_config = {
    'critical_threshold': 0,
    'high_threshold': 3,
    'medium_threshold': 15,
    'dependency_threshold': 8,
    'iac_threshold': 10,
    'container_threshold': 5,
    'dast_threshold': 8
}

gate_logic = security_pipeline.create_security_gate_logic(gate_config)
print("\\nSecurity Gate Logic:")
print(json.dumps(gate_logic, indent=2))
```

## Best Practices for Automated Security Testing

### 1. Implement Shift-Left Security

**Early Integration**: Integrate security testing as early as possible in the development process, including pre-commit hooks, IDE plugins, and early CI/CD stages.

**Developer-Friendly Tools**: Choose tools that provide clear, actionable feedback and integrate well with developer workflows.

**Fast Feedback Loops**: Ensure security tests run quickly to avoid disrupting development velocity.

### 2. Use Multiple Testing Approaches

**Layered Security Testing**: Implement multiple types of security testing (SAST, DAST, IAST, dependency scanning) to achieve comprehensive coverage.

**Tool Diversity**: Use multiple tools for each testing type to reduce false negatives and increase detection coverage.

**Complementary Techniques**: Combine automated testing with manual security reviews and penetration testing.

### 3. Optimize for Accuracy and Performance

**Reduce False Positives**: Tune tools and create custom rules to minimize false positives that can lead to alert fatigue.

**Prioritize Findings**: Implement risk-based prioritization to focus on the most critical security issues first.

**Performance Optimization**: Optimize scan execution time and resource usage to maintain development velocity.

### 4. Establish Effective Security Gates

**Risk-Based Thresholds**: Set security gate thresholds based on risk assessment and business requirements.

**Graduated Response**: Implement different actions based on severity levels (block, require approval, notify).

**Exception Handling**: Provide mechanisms for handling legitimate exceptions while maintaining security standards.

## Common Challenges and Solutions

### Challenge 1: Tool Integration Complexity

**Problem**: Difficulty integrating multiple security tools into existing CI/CD pipelines.

**Solutions**:
- Use standardized APIs and output formats
- Implement orchestration platforms (SOAR)
- Create wrapper scripts for tool integration
- Use containerized tools for consistency
- Implement gradual rollout strategies

### Challenge 2: False Positive Management

**Problem**: High false positive rates leading to alert fatigue and reduced effectiveness.

**Solutions**:
- Implement machine learning for false positive reduction
- Create custom rules and suppressions
- Use multiple tools for validation
- Implement developer feedback loops
- Regular tool tuning and optimization

### Challenge 3: Performance Impact

**Problem**: Security testing slowing down development and deployment processes.

**Solutions**:
- Implement parallel scanning
- Use incremental and differential scanning
- Optimize tool configurations
- Cache scan results where appropriate
- Implement smart scheduling

### Challenge 4: Results Management and Tracking

**Problem**: Difficulty managing and tracking security findings across multiple tools and projects.

**Solutions**:
- Implement centralized vulnerability management
- Use standardized vulnerability formats (SARIF)
- Create unified dashboards and reporting
- Implement automated ticket creation and tracking
- Establish clear remediation workflows

## Resources and Further Reading

### AWS Documentation and Services
- [AWS CodeBuild User Guide](https://docs.aws.amazon.com/codebuild/latest/userguide/)
- [AWS CodePipeline User Guide](https://docs.aws.amazon.com/codepipeline/latest/userguide/)
- [Amazon CodeGuru Reviewer](https://docs.aws.amazon.com/codeguru/latest/reviewer-ug/)
- [AWS Security Hub](https://docs.aws.amazon.com/securityhub/latest/userguide/)

### Security Testing Tools
- [OWASP ZAP](https://owasp.org/www-project-zap/) - Dynamic application security testing
- [SonarQube](https://www.sonarqube.org/) - Static code analysis
- [Snyk](https://snyk.io/) - Dependency vulnerability scanning
- [Checkov](https://www.checkov.io/) - Infrastructure as code security scanning
- [Semgrep](https://semgrep.dev/) - Static analysis for security

### Industry Standards and Frameworks
- [OWASP Application Security Verification Standard (ASVS)](https://owasp.org/www-project-application-security-verification-standard/)
- [NIST Secure Software Development Framework (SSDF)](https://csrc.nist.gov/Projects/ssdf)
- [SANS Secure Coding Practices](https://www.sans.org/white-papers/2172/)
- [ISO/IEC 27034 - Application Security](https://www.iso.org/standard/44378.html)

### Best Practices and Guides
- [OWASP DevSecOps Guideline](https://owasp.org/www-project-devsecops-guideline/)
- [NIST SP 800-218 - Secure Software Development Framework](https://csrc.nist.gov/publications/detail/sp/800-218/final)
- [Microsoft Security Development Lifecycle (SDL)](https://www.microsoft.com/en-us/securityengineering/sdl/)

---

*This documentation provides comprehensive guidance for implementing automated security testing throughout the development and release lifecycle. Regular updates ensure the content remains current with evolving security testing tools and practices.*
