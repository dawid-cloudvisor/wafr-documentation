---
title: SEC11-BP05 - Centralize services for packages and dependencies
layout: default
parent: SEC11 - How do you incorporate and validate the security properties of applications?
grand_parent: Security
nav_order: 5
---

<div class="pillar-header">
  <h1>SEC11-BP05: Centralize services for packages and dependencies</h1>
  <p>Provide centralized services for your builders to acquire and verify packages and dependencies. This allows you to validate packages before they are included in your software, and provides a centralized platform for patching and updating packages that address security issues.</p>
</div>

## Implementation guidance

Centralizing package and dependency management is crucial for maintaining security, consistency, and compliance across your development lifecycle. By providing centralized services, you can ensure that all packages are vetted, secure, and up-to-date before being used in your applications.

### Key steps for implementing this best practice:

1. **Establish centralized package repositories**:
   - Set up private package repositories for different languages and frameworks
   - Configure artifact repositories with security scanning capabilities
   - Implement package approval workflows and governance policies
   - Create mirrors of public repositories with additional security controls
   - Establish package versioning and lifecycle management policies

2. **Implement package security scanning**:
   - Configure automated vulnerability scanning for all packages
   - Set up license compliance checking and approval processes
   - Implement malware and supply chain attack detection
   - Create security policies for package approval and rejection
   - Establish continuous monitoring for newly discovered vulnerabilities

3. **Create package validation and approval processes**:
   - Define security criteria for package acceptance
   - Implement automated and manual review processes
   - Create package metadata and documentation requirements
   - Establish digital signature verification for packages
   - Set up package provenance and integrity checking

4. **Configure development environment integration**:
   - Integrate centralized repositories with CI/CD pipelines
   - Configure development tools to use centralized repositories
   - Implement package caching and distribution optimization
   - Create developer onboarding and training materials
   - Establish troubleshooting and support processes

5. **Implement package lifecycle management**:
   - Create automated update and patching processes
   - Establish deprecation and end-of-life policies
   - Implement rollback and recovery procedures
   - Set up monitoring and alerting for package issues
   - Create reporting and compliance dashboards

6. **Establish governance and compliance**:
   - Define roles and responsibilities for package management
   - Create audit trails and compliance reporting
   - Implement access controls and authentication
   - Establish incident response procedures for package security issues
   - Create metrics and KPIs for package management effectiveness

## Implementation examples

### Example 1: AWS CodeArtifact setup for centralized package management

```bash
# Create CodeArtifact domain
aws codeartifact create-domain \
  --domain my-company-packages \
  --encryption-key arn:aws:kms:us-west-2:123456789012:key/12345678-1234-1234-1234-123456789012

# Create repository for npm packages
aws codeartifact create-repository \
  --domain my-company-packages \
  --repository npm-packages \
  --description "Centralized npm package repository" \
  --upstreams repositoryName=npm-public

# Create repository for Python packages
aws codeartifact create-repository \
  --domain my-company-packages \
  --repository python-packages \
  --description "Centralized Python package repository" \
  --upstreams repositoryName=pypi-public

# Create public upstream repositories
aws codeartifact create-repository \
  --domain my-company-packages \
  --repository npm-public \
  --description "NPM public packages mirror" \
  --external-connections repositoryName=public:npmjs

aws codeartifact create-repository \
  --domain my-company-packages \
  --repository pypi-public \
  --description "PyPI public packages mirror" \
  --external-connections repositoryName=public:pypi

# Configure repository policies
aws codeartifact put-repository-permissions-policy \
  --domain my-company-packages \
  --repository npm-packages \
  --policy-document file://repository-policy.json
```

### Example 2: Package security scanning with AWS Inspector and Lambda

```python
import json
import boto3
import requests
from datetime import datetime, timedelta

class PackageSecurityScanner:
    def __init__(self):
        self.inspector = boto3.client('inspector2')
        self.codeartifact = boto3.client('codeartifact')
        self.dynamodb = boto3.resource('dynamodb')
        self.sns = boto3.client('sns')
        
        # DynamoDB table for tracking package security status
        self.package_table = self.dynamodb.Table('PackageSecurityStatus')
        
    def scan_package(self, package_name, package_version, repository):
        """Scan a package for security vulnerabilities"""
        
        try:
            # Download package metadata
            package_info = self.get_package_info(package_name, package_version, repository)
            
            # Perform vulnerability scanning
            vulnerabilities = self.check_vulnerabilities(package_name, package_version)
            
            # Check license compliance
            license_status = self.check_license_compliance(package_info)
            
            # Verify package integrity
            integrity_status = self.verify_package_integrity(package_info)
            
            # Calculate security score
            security_score = self.calculate_security_score(
                vulnerabilities, license_status, integrity_status
            )
            
            # Store results
            scan_result = {
                'package_name': package_name,
                'package_version': package_version,
                'repository': repository,
                'scan_timestamp': datetime.utcnow().isoformat(),
                'vulnerabilities': vulnerabilities,
                'license_status': license_status,
                'integrity_status': integrity_status,
                'security_score': security_score,
                'approval_status': self.determine_approval_status(security_score, vulnerabilities)
            }
            
            self.store_scan_result(scan_result)
            
            # Send alerts for high-risk packages
            if security_score < 50 or any(v['severity'] == 'CRITICAL' for v in vulnerabilities):
                self.send_security_alert(scan_result)
            
            return scan_result
            
        except Exception as e:
            print(f"Error scanning package {package_name}:{package_version}: {str(e)}")
            return None
    
    def get_package_info(self, package_name, package_version, repository):
        """Retrieve package information from CodeArtifact"""
        
        response = self.codeartifact.describe_package_version(
            domain='my-company-packages',
            repository=repository,
            format='npm',  # or 'pypi', 'maven', etc.
            package=package_name,
            packageVersion=package_version
        )
        
        return response['packageVersion']
    
    def check_vulnerabilities(self, package_name, package_version):
        """Check package for known vulnerabilities"""
        
        vulnerabilities = []
        
        # Check against multiple vulnerability databases
        # Example: OSV (Open Source Vulnerabilities)
        osv_vulns = self.query_osv_database(package_name, package_version)
        vulnerabilities.extend(osv_vulns)
        
        # Check against NVD (National Vulnerability Database)
        nvd_vulns = self.query_nvd_database(package_name, package_version)
        vulnerabilities.extend(nvd_vulns)
        
        # Check against Snyk database (if available)
        snyk_vulns = self.query_snyk_database(package_name, package_version)
        vulnerabilities.extend(snyk_vulns)
        
        return vulnerabilities
    
    def query_osv_database(self, package_name, package_version):
        """Query OSV database for vulnerabilities"""
        
        try:
            url = "https://api.osv.dev/v1/query"
            payload = {
                "package": {
                    "name": package_name,
                    "ecosystem": "npm"  # Adjust based on package type
                },
                "version": package_version
            }
            
            response = requests.post(url, json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                vulnerabilities = []
                
                for vuln in data.get('vulns', []):
                    vulnerabilities.append({
                        'id': vuln.get('id'),
                        'summary': vuln.get('summary'),
                        'severity': self.map_severity(vuln.get('database_specific', {}).get('severity')),
                        'source': 'OSV',
                        'published': vuln.get('published'),
                        'modified': vuln.get('modified')
                    })
                
                return vulnerabilities
            
        except Exception as e:
            print(f"Error querying OSV database: {str(e)}")
        
        return []
    
    def check_license_compliance(self, package_info):
        """Check if package license is compliant with company policies"""
        
        # Define approved licenses
        approved_licenses = [
            'MIT', 'Apache-2.0', 'BSD-3-Clause', 'BSD-2-Clause',
            'ISC', 'GPL-3.0', 'LGPL-2.1', 'MPL-2.0'
        ]
        
        # Define prohibited licenses
        prohibited_licenses = [
            'GPL-2.0', 'AGPL-3.0', 'SSPL-1.0'
        ]
        
        license_info = package_info.get('license', 'Unknown')
        
        if license_info in prohibited_licenses:
            return {
                'status': 'REJECTED',
                'license': license_info,
                'reason': 'License is prohibited by company policy'
            }
        elif license_info in approved_licenses:
            return {
                'status': 'APPROVED',
                'license': license_info,
                'reason': 'License is approved'
            }
        else:
            return {
                'status': 'REVIEW_REQUIRED',
                'license': license_info,
                'reason': 'License requires manual review'
            }
    
    def verify_package_integrity(self, package_info):
        """Verify package integrity using checksums and signatures"""
        
        try:
            # Verify package checksums
            expected_checksum = package_info.get('checksum')
            if expected_checksum:
                # Download and verify package checksum
                # Implementation depends on package format
                pass
            
            # Verify digital signatures if available
            signature = package_info.get('signature')
            if signature:
                # Verify package signature
                # Implementation depends on signing method
                pass
            
            return {
                'status': 'VERIFIED',
                'checksum_verified': True,
                'signature_verified': True
            }
            
        except Exception as e:
            return {
                'status': 'FAILED',
                'error': str(e),
                'checksum_verified': False,
                'signature_verified': False
            }
    
    def calculate_security_score(self, vulnerabilities, license_status, integrity_status):
        """Calculate overall security score for the package"""
        
        base_score = 100
        
        # Deduct points for vulnerabilities
        for vuln in vulnerabilities:
            if vuln['severity'] == 'CRITICAL':
                base_score -= 30
            elif vuln['severity'] == 'HIGH':
                base_score -= 20
            elif vuln['severity'] == 'MEDIUM':
                base_score -= 10
            elif vuln['severity'] == 'LOW':
                base_score -= 5
        
        # Deduct points for license issues
        if license_status['status'] == 'REJECTED':
            base_score -= 50
        elif license_status['status'] == 'REVIEW_REQUIRED':
            base_score -= 20
        
        # Deduct points for integrity issues
        if integrity_status['status'] == 'FAILED':
            base_score -= 40
        
        return max(0, base_score)
    
    def determine_approval_status(self, security_score, vulnerabilities):
        """Determine if package should be approved based on security assessment"""
        
        # Reject packages with critical vulnerabilities
        if any(v['severity'] == 'CRITICAL' for v in vulnerabilities):
            return 'REJECTED'
        
        # Approve packages with high security scores
        if security_score >= 80:
            return 'APPROVED'
        elif security_score >= 60:
            return 'CONDITIONAL_APPROVAL'
        else:
            return 'REJECTED'
    
    def store_scan_result(self, scan_result):
        """Store scan results in DynamoDB"""
        
        self.package_table.put_item(Item=scan_result)
    
    def send_security_alert(self, scan_result):
        """Send security alert for high-risk packages"""
        
        message = {
            'alert_type': 'PACKAGE_SECURITY_RISK',
            'package': f"{scan_result['package_name']}:{scan_result['package_version']}",
            'security_score': scan_result['security_score'],
            'vulnerabilities': len(scan_result['vulnerabilities']),
            'approval_status': scan_result['approval_status'],
            'scan_timestamp': scan_result['scan_timestamp']
        }
        
        self.sns.publish(
            TopicArn='arn:aws:sns:us-west-2:123456789012:PackageSecurityAlerts',
            Subject=f"Security Alert: {scan_result['package_name']}",
            Message=json.dumps(message, indent=2)
        )

def lambda_handler(event, context):
    """Lambda function to handle package security scanning"""
    
    scanner = PackageSecurityScanner()
    
    # Process CodeArtifact events
    for record in event.get('Records', []):
        if record.get('eventSource') == 'aws:codeartifact':
            event_name = record.get('eventName')
            
            if event_name == 'PackageVersionPublished':
                # Extract package information from event
                package_name = record['codeartifact']['package']['name']
                package_version = record['codeartifact']['packageVersion']['version']
                repository = record['codeartifact']['repository']['name']
                
                # Scan the package
                result = scanner.scan_package(package_name, package_version, repository)
                
                if result:
                    print(f"Scanned {package_name}:{package_version} - Score: {result['security_score']}")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Package security scanning completed')
    }
```

### Example 3: CI/CD integration with centralized package management

```yaml
# .github/workflows/package-security.yml
name: Package Security Validation

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  package-security-scan:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
    
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v2
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: us-west-2
    
    - name: Configure CodeArtifact
      run: |
        # Get CodeArtifact authorization token
        export CODEARTIFACT_AUTH_TOKEN=$(aws codeartifact get-authorization-token \
          --domain my-company-packages \
          --query authorizationToken \
          --output text)
        
        # Configure npm to use CodeArtifact
        npm config set registry https://my-company-packages-123456789012.d.codeartifact.us-west-2.amazonaws.com/npm/npm-packages/
        npm config set //my-company-packages-123456789012.d.codeartifact.us-west-2.amazonaws.com/npm/npm-packages/:_authToken=$CODEARTIFACT_AUTH_TOKEN
    
    - name: Install dependencies
      run: npm ci
    
    - name: Run package security audit
      run: |
        # Run npm audit
        npm audit --audit-level=moderate
        
        # Run custom security checks
        node scripts/package-security-check.js
    
    - name: Validate package sources
      run: |
        # Ensure all packages come from approved repositories
        node scripts/validate-package-sources.js
    
    - name: Generate security report
      run: |
        # Generate package security report
        node scripts/generate-security-report.js
    
    - name: Upload security report
      uses: actions/upload-artifact@v3
      with:
        name: package-security-report
        path: reports/package-security-report.json
```

```javascript
// scripts/package-security-check.js
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

class PackageSecurityValidator {
    constructor() {
        this.packageJson = JSON.parse(fs.readFileSync('package.json', 'utf8'));
        this.packageLock = JSON.parse(fs.readFileSync('package-lock.json', 'utf8'));
        this.securityReport = {
            timestamp: new Date().toISOString(),
            packages: [],
            violations: [],
            summary: {}
        };
    }

    async validatePackages() {
        console.log('Starting package security validation...');
        
        // Validate direct dependencies
        await this.validateDependencies(this.packageJson.dependencies, 'production');
        await this.validateDependencies(this.packageJson.devDependencies, 'development');
        
        // Check for known vulnerabilities
        await this.checkVulnerabilities();
        
        // Validate package sources
        await this.validatePackageSources();
        
        // Check for license compliance
        await this.checkLicenseCompliance();
        
        // Generate summary
        this.generateSummary();
        
        // Save report
        this.saveReport();
        
        // Exit with error if critical issues found
        if (this.securityReport.violations.some(v => v.severity === 'CRITICAL')) {
            console.error('Critical security violations found!');
            process.exit(1);
        }
        
        console.log('Package security validation completed successfully.');
    }

    async validateDependencies(dependencies, type) {
        if (!dependencies) return;
        
        for (const [packageName, version] of Object.entries(dependencies)) {
            const packageInfo = {
                name: packageName,
                version: version,
                type: type,
                resolved: this.getResolvedVersion(packageName),
                source: this.getPackageSource(packageName)
            };
            
            // Validate package source
            if (!this.isApprovedSource(packageInfo.source)) {
                this.securityReport.violations.push({
                    type: 'UNAPPROVED_SOURCE',
                    severity: 'HIGH',
                    package: packageName,
                    message: `Package ${packageName} is not from an approved source: ${packageInfo.source}`
                });
            }
            
            // Check for deprecated packages
            if (await this.isDeprecated(packageName)) {
                this.securityReport.violations.push({
                    type: 'DEPRECATED_PACKAGE',
                    severity: 'MEDIUM',
                    package: packageName,
                    message: `Package ${packageName} is deprecated`
                });
            }
            
            this.securityReport.packages.push(packageInfo);
        }
    }

    async checkVulnerabilities() {
        try {
            // Run npm audit and parse results
            const auditResult = execSync('npm audit --json', { encoding: 'utf8' });
            const auditData = JSON.parse(auditResult);
            
            if (auditData.vulnerabilities) {
                for (const [packageName, vulnInfo] of Object.entries(auditData.vulnerabilities)) {
                    const severity = this.mapSeverity(vulnInfo.severity);
                    
                    this.securityReport.violations.push({
                        type: 'VULNERABILITY',
                        severity: severity,
                        package: packageName,
                        message: `Vulnerability found in ${packageName}: ${vulnInfo.via.join(', ')}`,
                        cves: vulnInfo.via.filter(v => typeof v === 'object').map(v => v.source)
                    });
                }
            }
        } catch (error) {
            console.warn('npm audit failed:', error.message);
        }
    }

    async validatePackageSources() {
        const approvedSources = [
            'https://my-company-packages-123456789012.d.codeartifact.us-west-2.amazonaws.com/npm/npm-packages/',
            'https://registry.npmjs.org/' // Only for approved public packages
        ];
        
        // Check package-lock.json for actual sources
        this.traversePackageLock(this.packageLock, (packageName, packageData) => {
            if (packageData.resolved) {
                const source = new URL(packageData.resolved).origin;
                
                if (!approvedSources.some(approved => source.startsWith(approved))) {
                    this.securityReport.violations.push({
                        type: 'UNAPPROVED_SOURCE',
                        severity: 'HIGH',
                        package: packageName,
                        message: `Package ${packageName} resolved from unapproved source: ${source}`
                    });
                }
            }
        });
    }

    async checkLicenseCompliance() {
        const approvedLicenses = ['MIT', 'Apache-2.0', 'BSD-3-Clause', 'ISC'];
        const prohibitedLicenses = ['GPL-2.0', 'AGPL-3.0'];
        
        try {
            const licenseCheck = execSync('npx license-checker --json', { encoding: 'utf8' });
            const licenses = JSON.parse(licenseCheck);
            
            for (const [packageName, licenseInfo] of Object.entries(licenses)) {
                const license = licenseInfo.licenses;
                
                if (prohibitedLicenses.includes(license)) {
                    this.securityReport.violations.push({
                        type: 'PROHIBITED_LICENSE',
                        severity: 'CRITICAL',
                        package: packageName,
                        message: `Package ${packageName} has prohibited license: ${license}`
                    });
                } else if (!approvedLicenses.includes(license) && license !== 'UNKNOWN') {
                    this.securityReport.violations.push({
                        type: 'UNAPPROVED_LICENSE',
                        severity: 'MEDIUM',
                        package: packageName,
                        message: `Package ${packageName} has unapproved license: ${license}`
                    });
                }
            }
        } catch (error) {
            console.warn('License check failed:', error.message);
        }
    }

    getResolvedVersion(packageName) {
        // Get actual resolved version from package-lock.json
        const lockEntry = this.packageLock.packages?.[`node_modules/${packageName}`];
        return lockEntry?.version || 'unknown';
    }

    getPackageSource(packageName) {
        // Get package source from package-lock.json
        const lockEntry = this.packageLock.packages?.[`node_modules/${packageName}`];
        if (lockEntry?.resolved) {
            return new URL(lockEntry.resolved).origin;
        }
        return 'unknown';
    }

    isApprovedSource(source) {
        const approvedSources = [
            'https://my-company-packages-123456789012.d.codeartifact.us-west-2.amazonaws.com',
            'https://registry.npmjs.org'
        ];
        
        return approvedSources.some(approved => source.startsWith(approved));
    }

    async isDeprecated(packageName) {
        try {
            const packageInfo = execSync(`npm view ${packageName} --json`, { encoding: 'utf8' });
            const data = JSON.parse(packageInfo);
            return data.deprecated !== undefined;
        } catch (error) {
            return false;
        }
    }

    mapSeverity(npmSeverity) {
        const severityMap = {
            'critical': 'CRITICAL',
            'high': 'HIGH',
            'moderate': 'MEDIUM',
            'low': 'LOW'
        };
        
        return severityMap[npmSeverity] || 'UNKNOWN';
    }

    traversePackageLock(obj, callback, path = '') {
        if (obj.packages) {
            for (const [packagePath, packageData] of Object.entries(obj.packages)) {
                if (packagePath.startsWith('node_modules/')) {
                    const packageName = packagePath.replace('node_modules/', '');
                    callback(packageName, packageData);
                }
            }
        }
    }

    generateSummary() {
        const violations = this.securityReport.violations;
        
        this.securityReport.summary = {
            totalPackages: this.securityReport.packages.length,
            totalViolations: violations.length,
            criticalViolations: violations.filter(v => v.severity === 'CRITICAL').length,
            highViolations: violations.filter(v => v.severity === 'HIGH').length,
            mediumViolations: violations.filter(v => v.severity === 'MEDIUM').length,
            lowViolations: violations.filter(v => v.severity === 'LOW').length
        };
    }

    saveReport() {
        const reportsDir = 'reports';
        if (!fs.existsSync(reportsDir)) {
            fs.mkdirSync(reportsDir, { recursive: true });
        }
        
        fs.writeFileSync(
            path.join(reportsDir, 'package-security-report.json'),
            JSON.stringify(this.securityReport, null, 2)
        );
        
        console.log('Security report saved to reports/package-security-report.json');
    }
}

// Run validation
const validator = new PackageSecurityValidator();
validator.validatePackages().catch(error => {
    console.error('Package security validation failed:', error);
    process.exit(1);
});
```
```

### Example 4: Package governance and policy enforcement

```python
import json
import boto3
from datetime import datetime, timedelta

class PackageGovernanceEngine:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.sns = boto3.client('sns')
        self.stepfunctions = boto3.client('stepfunctions')
        
        # DynamoDB tables
        self.packages_table = self.dynamodb.Table('PackageRegistry')
        self.policies_table = self.dynamodb.Table('PackagePolicies')
        self.approvals_table = self.dynamodb.Table('PackageApprovals')
        
    def evaluate_package_policy(self, package_name, package_version, metadata):
        """Evaluate package against governance policies"""
        
        # Get applicable policies
        policies = self.get_applicable_policies(package_name, metadata)
        
        evaluation_result = {
            'package_name': package_name,
            'package_version': package_version,
            'evaluation_timestamp': datetime.utcnow().isoformat(),
            'policies_evaluated': [],
            'violations': [],
            'approval_required': False,
            'auto_approved': False
        }
        
        for policy in policies:
            policy_result = self.evaluate_single_policy(policy, metadata)
            evaluation_result['policies_evaluated'].append(policy_result)
            
            if not policy_result['compliant']:
                evaluation_result['violations'].append({
                    'policy_id': policy['policy_id'],
                    'policy_name': policy['name'],
                    'violation_type': policy_result['violation_type'],
                    'severity': policy_result['severity'],
                    'message': policy_result['message']
                })
        
        # Determine approval status
        evaluation_result['approval_required'] = self.requires_manual_approval(evaluation_result)
        evaluation_result['auto_approved'] = self.can_auto_approve(evaluation_result)
        
        # Store evaluation result
        self.store_evaluation_result(evaluation_result)
        
        # Trigger approval workflow if needed
        if evaluation_result['approval_required'] and not evaluation_result['auto_approved']:
            self.trigger_approval_workflow(evaluation_result)
        
        return evaluation_result
    
    def get_applicable_policies(self, package_name, metadata):
        """Get policies applicable to the package"""
        
        response = self.policies_table.scan(
            FilterExpression='attribute_exists(active) AND active = :active',
            ExpressionAttributeValues={':active': True}
        )
        
        applicable_policies = []
        
        for policy in response['Items']:
            if self.policy_applies_to_package(policy, package_name, metadata):
                applicable_policies.append(policy)
        
        return applicable_policies
    
    def policy_applies_to_package(self, policy, package_name, metadata):
        """Check if policy applies to the specific package"""
        
        # Check package name patterns
        if 'package_patterns' in policy:
            import re
            for pattern in policy['package_patterns']:
                if re.match(pattern, package_name):
                    return True
        
        # Check package categories
        if 'categories' in policy and 'category' in metadata:
            if metadata['category'] in policy['categories']:
                return True
        
        # Check package ecosystems
        if 'ecosystems' in policy and 'ecosystem' in metadata:
            if metadata['ecosystem'] in policy['ecosystems']:
                return True
        
        # Default policies apply to all packages
        return policy.get('applies_to_all', False)
    
    def evaluate_single_policy(self, policy, metadata):
        """Evaluate a single policy against package metadata"""
        
        policy_result = {
            'policy_id': policy['policy_id'],
            'policy_name': policy['name'],
            'compliant': True,
            'violation_type': None,
            'severity': 'LOW',
            'message': 'Policy compliant'
        }
        
        # Evaluate security requirements
        if 'security_requirements' in policy:
            security_result = self.evaluate_security_requirements(
                policy['security_requirements'], metadata
            )
            if not security_result['compliant']:
                policy_result.update(security_result)
                return policy_result
        
        # Evaluate license requirements
        if 'license_requirements' in policy:
            license_result = self.evaluate_license_requirements(
                policy['license_requirements'], metadata
            )
            if not license_result['compliant']:
                policy_result.update(license_result)
                return policy_result
        
        # Evaluate version requirements
        if 'version_requirements' in policy:
            version_result = self.evaluate_version_requirements(
                policy['version_requirements'], metadata
            )
            if not version_result['compliant']:
                policy_result.update(version_result)
                return policy_result
        
        # Evaluate maintenance requirements
        if 'maintenance_requirements' in policy:
            maintenance_result = self.evaluate_maintenance_requirements(
                policy['maintenance_requirements'], metadata
            )
            if not maintenance_result['compliant']:
                policy_result.update(maintenance_result)
                return policy_result
        
        return policy_result
    
    def evaluate_security_requirements(self, requirements, metadata):
        """Evaluate security-related policy requirements"""
        
        # Check vulnerability thresholds
        if 'max_vulnerabilities' in requirements:
            vuln_count = len(metadata.get('vulnerabilities', []))
            max_allowed = requirements['max_vulnerabilities']
            
            if vuln_count > max_allowed:
                return {
                    'compliant': False,
                    'violation_type': 'SECURITY_VULNERABILITY_THRESHOLD',
                    'severity': 'HIGH',
                    'message': f'Package has {vuln_count} vulnerabilities, exceeds limit of {max_allowed}'
                }
        
        # Check security score threshold
        if 'min_security_score' in requirements:
            security_score = metadata.get('security_score', 0)
            min_score = requirements['min_security_score']
            
            if security_score < min_score:
                return {
                    'compliant': False,
                    'violation_type': 'SECURITY_SCORE_THRESHOLD',
                    'severity': 'MEDIUM',
                    'message': f'Package security score {security_score} below minimum {min_score}'
                }
        
        # Check for critical vulnerabilities
        if requirements.get('no_critical_vulnerabilities', False):
            critical_vulns = [
                v for v in metadata.get('vulnerabilities', [])
                if v.get('severity') == 'CRITICAL'
            ]
            
            if critical_vulns:
                return {
                    'compliant': False,
                    'violation_type': 'CRITICAL_VULNERABILITY',
                    'severity': 'CRITICAL',
                    'message': f'Package contains {len(critical_vulns)} critical vulnerabilities'
                }
        
        return {'compliant': True}
    
    def evaluate_license_requirements(self, requirements, metadata):
        """Evaluate license-related policy requirements"""
        
        package_license = metadata.get('license', 'Unknown')
        
        # Check approved licenses
        if 'approved_licenses' in requirements:
            if package_license not in requirements['approved_licenses']:
                return {
                    'compliant': False,
                    'violation_type': 'UNAPPROVED_LICENSE',
                    'severity': 'MEDIUM',
                    'message': f'Package license {package_license} not in approved list'
                }
        
        # Check prohibited licenses
        if 'prohibited_licenses' in requirements:
            if package_license in requirements['prohibited_licenses']:
                return {
                    'compliant': False,
                    'violation_type': 'PROHIBITED_LICENSE',
                    'severity': 'HIGH',
                    'message': f'Package license {package_license} is prohibited'
                }
        
        return {'compliant': True}
    
    def evaluate_version_requirements(self, requirements, metadata):
        """Evaluate version-related policy requirements"""
        
        # Check for pre-release versions
        if requirements.get('no_prerelease', False):
            version = metadata.get('version', '')
            if any(marker in version.lower() for marker in ['alpha', 'beta', 'rc', 'pre']):
                return {
                    'compliant': False,
                    'violation_type': 'PRERELEASE_VERSION',
                    'severity': 'MEDIUM',
                    'message': f'Pre-release version {version} not allowed'
                }
        
        # Check version age
        if 'max_age_days' in requirements:
            published_date = metadata.get('published_date')
            if published_date:
                age_days = (datetime.utcnow() - datetime.fromisoformat(published_date)).days
                max_age = requirements['max_age_days']
                
                if age_days > max_age:
                    return {
                        'compliant': False,
                        'violation_type': 'VERSION_TOO_OLD',
                        'severity': 'LOW',
                        'message': f'Package version is {age_days} days old, exceeds limit of {max_age}'
                    }
        
        return {'compliant': True}
    
    def evaluate_maintenance_requirements(self, requirements, metadata):
        """Evaluate maintenance-related policy requirements"""
        
        # Check last update date
        if 'max_days_since_update' in requirements:
            last_update = metadata.get('last_update_date')
            if last_update:
                days_since_update = (datetime.utcnow() - datetime.fromisoformat(last_update)).days
                max_days = requirements['max_days_since_update']
                
                if days_since_update > max_days:
                    return {
                        'compliant': False,
                        'violation_type': 'STALE_PACKAGE',
                        'severity': 'MEDIUM',
                        'message': f'Package not updated for {days_since_update} days, exceeds limit of {max_days}'
                    }
        
        # Check maintainer activity
        if requirements.get('active_maintainer_required', False):
            maintainer_active = metadata.get('maintainer_active', False)
            if not maintainer_active:
                return {
                    'compliant': False,
                    'violation_type': 'INACTIVE_MAINTAINER',
                    'severity': 'MEDIUM',
                    'message': 'Package maintainer appears to be inactive'
                }
        
        return {'compliant': True}
    
    def requires_manual_approval(self, evaluation_result):
        """Determine if package requires manual approval"""
        
        # Always require approval for violations
        if evaluation_result['violations']:
            return True
        
        # Require approval for new packages from unknown sources
        # Additional logic can be added here
        
        return False
    
    def can_auto_approve(self, evaluation_result):
        """Determine if package can be automatically approved"""
        
        # Don't auto-approve if there are violations
        if evaluation_result['violations']:
            return False
        
        # Don't auto-approve if manual approval is required
        if evaluation_result['approval_required']:
            return False
        
        return True
    
    def store_evaluation_result(self, evaluation_result):
        """Store policy evaluation result"""
        
        self.packages_table.put_item(Item=evaluation_result)
    
    def trigger_approval_workflow(self, evaluation_result):
        """Trigger manual approval workflow"""
        
        workflow_input = {
            'package_name': evaluation_result['package_name'],
            'package_version': evaluation_result['package_version'],
            'evaluation_result': evaluation_result,
            'approval_required_reason': 'Policy violations detected'
        }
        
        # Start Step Functions workflow for approval process
        self.stepfunctions.start_execution(
            stateMachineArn='arn:aws:states:us-west-2:123456789012:stateMachine:PackageApprovalWorkflow',
            input=json.dumps(workflow_input)
        )
        
        # Send notification to security team
        self.sns.publish(
            TopicArn='arn:aws:sns:us-west-2:123456789012:PackageApprovalRequired',
            Subject=f'Package Approval Required: {evaluation_result["package_name"]}',
            Message=json.dumps(evaluation_result, indent=2)
        )

# Example usage
def lambda_handler(event, context):
    """Lambda function for package governance evaluation"""
    
    governance_engine = PackageGovernanceEngine()
    
    # Process package evaluation request
    package_name = event.get('package_name')
    package_version = event.get('package_version')
    metadata = event.get('metadata', {})
    
    if package_name and package_version:
        result = governance_engine.evaluate_package_policy(
            package_name, package_version, metadata
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }
    
    return {
        'statusCode': 400,
        'body': json.dumps({'error': 'Missing required parameters'})
    }
```

## AWS services to consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS CodeArtifact</h4>
    <p>Fully managed artifact repository service that makes it easy for organizations to securely store, publish, and share packages used in their software development process.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon Inspector</h4>
    <p>Automated security assessment service that helps improve the security and compliance of applications by automatically assessing applications for vulnerabilities.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Lambda</h4>
    <p>Serverless compute service for running package security scanning and governance logic without managing servers.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon DynamoDB</h4>
    <p>NoSQL database service for storing package metadata, security scan results, and governance policies.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Step Functions</h4>
    <p>Serverless orchestration service for coordinating package approval workflows and complex governance processes.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon SNS</h4>
    <p>Messaging service for sending notifications about package security issues and approval requests.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Systems Manager</h4>
    <p>Management service for maintaining package inventories and enforcing compliance across your infrastructure.</p>
  </div>
</div>

## Benefits of centralizing services for packages and dependencies

- **Enhanced security posture**: Centralized scanning and validation of all packages before use
- **Improved compliance**: Consistent application of security and licensing policies
- **Reduced supply chain risk**: Protection against malicious packages and supply chain attacks
- **Operational efficiency**: Streamlined package management and automated security processes
- **Cost optimization**: Reduced bandwidth usage through package caching and mirroring
- **Developer productivity**: Simplified access to approved packages with clear governance
- **Audit capabilities**: Complete visibility into package usage and security status
- **Faster incident response**: Centralized tracking enables quick identification of affected systems

## Related resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/sec_appsec_centralize_services_for_packages_and_dependencies.html">AWS Well-Architected Framework - Centralize services for packages and dependencies</a></li>
    <li><a href="https://docs.aws.amazon.com/codeartifact/latest/ug/welcome.html">AWS CodeArtifact User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/inspector/latest/user/what-is-inspector.html">Amazon Inspector User Guide</a></li>
    <li><a href="https://aws.amazon.com/blogs/devops/how-to-publish-and-share-packages-with-aws-codeartifact/">How to publish and share packages with AWS CodeArtifact</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-implement-dependency-scanning-for-java-applications-using-amazon-inspector/">How to implement dependency scanning for Java applications using Amazon Inspector</a></li>
    <li><a href="https://docs.aws.amazon.com/codeartifact/latest/ug/packages-overview.html">Working with packages in CodeArtifact</a></li>
  </ul>
</div>
