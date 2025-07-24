---
title: SEC06-BP04 - Validate software integrity
layout: default
parent: SEC06 - How do you protect your compute resources?
grand_parent: Security
nav_order: 4
---

<div class="pillar-header">
  <h1>SEC06-BP04: Validate software integrity</h1>
  <p>Implement mechanisms to validate software integrity throughout the software lifecycle. For example, use code signing for your applications, and validate the signatures before running the software. Use a checksum to validate the integrity of software packages before installation. These mechanisms help you identify unauthorized modifications and ensure that you are running authentic software.</p>
</div>

## Implementation guidance

Software integrity validation is critical for ensuring that the software running in your environment has not been tampered with or corrupted. By implementing comprehensive integrity validation mechanisms, you can protect against supply chain attacks, unauthorized modifications, and ensure that only authentic, verified software executes in your compute environment.

### Key steps for implementing this best practice:

1. **Implement code signing and verification**:
   - Sign all application code and executables with digital certificates
   - Verify code signatures before execution or deployment
   - Use trusted certificate authorities for code signing certificates
   - Implement certificate lifecycle management and rotation
   - Establish code signing policies and procedures

2. **Validate package and dependency integrity**:
   - Verify checksums and hashes for all software packages
   - Use package managers with built-in integrity verification
   - Implement dependency scanning and validation
   - Maintain approved software catalogs and repositories
   - Monitor for compromised or malicious packages

3. **Establish secure software supply chain**:
   - Implement software bill of materials (SBOM) tracking
   - Verify the integrity of third-party components and libraries
   - Use trusted software repositories and registries
   - Implement provenance tracking for software artifacts
   - Establish vendor security assessment processes

4. **Configure runtime integrity monitoring**:
   - Implement file integrity monitoring (FIM) systems
   - Monitor for unauthorized changes to critical files
   - Use host-based intrusion detection systems
   - Implement application whitelisting and control
   - Configure system call monitoring and filtering

5. **Implement container and image integrity**:
   - Sign container images with digital signatures
   - Verify image signatures before deployment
   - Use content trust and notary services
   - Implement image scanning and vulnerability assessment
   - Establish secure image build and distribution pipelines

6. **Establish integrity validation automation**:
   - Automate integrity checks in CI/CD pipelines
   - Implement continuous integrity monitoring
   - Create automated responses to integrity violations
   - Establish integrity validation reporting and alerting
   - Integrate integrity validation with security orchestration

## Implementation examples

### Example 1: Code signing and verification pipeline

```bash
#!/bin/bash
# Code signing and verification script for CI/CD pipeline

set -e

# Configuration
SIGNING_KEY_ID="12345678-1234-1234-1234-123456789012"
ARTIFACT_BUCKET="my-signed-artifacts"
APPLICATION_NAME="my-application"
VERSION="${GITHUB_SHA:-$(git rev-parse HEAD)}"

# Function to sign application artifacts
sign_artifacts() {
    local artifact_path=$1
    local signed_path="${artifact_path}.signed"
    
    echo "Signing artifact: $artifact_path"
    
    # Sign the artifact using AWS KMS
    aws kms sign \
        --key-id "$SIGNING_KEY_ID" \
        --message-type RAW \
        --signing-algorithm RSASSA_PKCS1_V1_5_SHA_256 \
        --message "fileb://$artifact_path" \
        --output text \
        --query 'Signature' | base64 -d > "${artifact_path}.sig"
    
    # Create signed package with metadata
    cat > "${artifact_path}.metadata" << EOF
{
    "artifact": "$(basename $artifact_path)",
    "version": "$VERSION",
    "build_time": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "signature_algorithm": "RSASSA_PKCS1_V1_5_SHA_256",
    "key_id": "$SIGNING_KEY_ID",
    "checksum_sha256": "$(sha256sum $artifact_path | cut -d' ' -f1)",
    "checksum_sha512": "$(sha512sum $artifact_path | cut -d' ' -f1)"
}
EOF
    
    echo "Artifact signed successfully"
}

# Function to verify artifact signature
verify_signature() {
    local artifact_path=$1
    local signature_path="${artifact_path}.sig"
    local metadata_path="${artifact_path}.metadata"
    
    echo "Verifying signature for: $artifact_path"
    
    # Verify the signature using AWS KMS
    aws kms verify \
        --key-id "$SIGNING_KEY_ID" \
        --message-type RAW \
        --signing-algorithm RSASSA_PKCS1_V1_5_SHA_256 \
        --message "fileb://$artifact_path" \
        --signature "fileb://$signature_path"
    
    if [ $? -eq 0 ]; then
        echo "Signature verification successful"
        
        # Verify checksums
        expected_sha256=$(jq -r '.checksum_sha256' "$metadata_path")
        actual_sha256=$(sha256sum "$artifact_path" | cut -d' ' -f1)
        
        if [ "$expected_sha256" = "$actual_sha256" ]; then
            echo "Checksum verification successful"
            return 0
        else
            echo "ERROR: Checksum verification failed"
            return 1
        fi
    else
        echo "ERROR: Signature verification failed"
        return 1
    fi
}

# Function to upload signed artifacts
upload_signed_artifacts() {
    local artifact_path=$1
    local s3_prefix="$APPLICATION_NAME/$VERSION"
    
    echo "Uploading signed artifacts to S3..."
    
    # Upload artifact and signature files
    aws s3 cp "$artifact_path" "s3://$ARTIFACT_BUCKET/$s3_prefix/"
    aws s3 cp "${artifact_path}.sig" "s3://$ARTIFACT_BUCKET/$s3_prefix/"
    aws s3 cp "${artifact_path}.metadata" "s3://$ARTIFACT_BUCKET/$s3_prefix/"
    
    # Set object metadata for integrity tracking
    aws s3api put-object-tagging \
        --bucket "$ARTIFACT_BUCKET" \
        --key "$s3_prefix/$(basename $artifact_path)" \
        --tagging 'TagSet=[
            {Key=Signed,Value=true},
            {Key=Version,Value='$VERSION'},
            {Key=Application,Value='$APPLICATION_NAME'}
        ]'
    
    echo "Artifacts uploaded successfully"
}

# Function to download and verify artifacts
download_and_verify() {
    local artifact_name=$1
    local version=$2
    local s3_prefix="$APPLICATION_NAME/$version"
    
    echo "Downloading and verifying artifact: $artifact_name"
    
    # Download artifact and signature files
    aws s3 cp "s3://$ARTIFACT_BUCKET/$s3_prefix/$artifact_name" ./
    aws s3 cp "s3://$ARTIFACT_BUCKET/$s3_prefix/${artifact_name}.sig" ./
    aws s3 cp "s3://$ARTIFACT_BUCKET/$s3_prefix/${artifact_name}.metadata" ./
    
    # Verify the downloaded artifact
    if verify_signature "$artifact_name"; then
        echo "Artifact verification successful - safe to deploy"
        return 0
    else
        echo "ERROR: Artifact verification failed - DO NOT DEPLOY"
        return 1
    fi
}

# Main execution logic
case "${1:-}" in
    "sign")
        if [ -z "$2" ]; then
            echo "Usage: $0 sign <artifact_path>"
            exit 1
        fi
        sign_artifacts "$2"
        upload_signed_artifacts "$2"
        ;;
    "verify")
        if [ -z "$2" ] || [ -z "$3" ]; then
            echo "Usage: $0 verify <artifact_name> <version>"
            exit 1
        fi
        download_and_verify "$2" "$3"
        ;;
    "deploy")
        if [ -z "$2" ] || [ -z "$3" ]; then
            echo "Usage: $0 deploy <artifact_name> <version>"
            exit 1
        fi
        if download_and_verify "$2" "$3"; then
            echo "Proceeding with deployment..."
            # Add deployment logic here
        else
            echo "Deployment aborted due to integrity verification failure"
            exit 1
        fi
        ;;
    *)
        echo "Usage: $0 {sign|verify|deploy} [arguments]"
        echo "  sign <artifact_path>        - Sign an artifact"
        echo "  verify <artifact> <version> - Verify an artifact"
        echo "  deploy <artifact> <version> - Verify and deploy an artifact"
        exit 1
        ;;
esac
```

### Example 2: Container image signing with Docker Content Trust

```bash
#!/bin/bash
# Container image signing and verification with Docker Content Trust

set -e

# Configuration
REGISTRY="123456789012.dkr.ecr.us-west-2.amazonaws.com"
REPOSITORY="my-application"
TAG="${GITHUB_SHA:-latest}"
NOTARY_SERVER="https://notary.docker.io"

# Enable Docker Content Trust
export DOCKER_CONTENT_TRUST=1
export DOCKER_CONTENT_TRUST_SERVER="$NOTARY_SERVER"

# Function to set up signing keys
setup_signing_keys() {
    echo "Setting up Docker Content Trust keys..."
    
    # Generate root key (do this once and store securely)
    if [ ! -f ~/.docker/trust/private/root_keys ]; then
        docker trust key generate root
    fi
    
    # Generate repository key
    docker trust key generate "$REPOSITORY"
    
    # Initialize repository with signing key
    docker trust signer add --key "$REPOSITORY.pub" "$REPOSITORY" "$REGISTRY/$REPOSITORY"
    
    echo "Signing keys configured successfully"
}

# Function to build and sign container image
build_and_sign_image() {
    local dockerfile_path=${1:-Dockerfile}
    local context_path=${2:-.}
    
    echo "Building container image..."
    
    # Build the image
    docker build -t "$REGISTRY/$REPOSITORY:$TAG" -f "$dockerfile_path" "$context_path"
    
    # Scan image for vulnerabilities before signing
    echo "Scanning image for vulnerabilities..."
    trivy image --exit-code 1 --severity HIGH,CRITICAL "$REGISTRY/$REPOSITORY:$TAG"
    
    if [ $? -ne 0 ]; then
        echo "ERROR: Image contains high or critical vulnerabilities"
        exit 1
    fi
    
    # Sign and push the image
    echo "Signing and pushing image..."
    docker push "$REGISTRY/$REPOSITORY:$TAG"
    
    # Verify the signature was created
    docker trust inspect "$REGISTRY/$REPOSITORY:$TAG"
    
    echo "Image built, signed, and pushed successfully"
}

# Function to verify image signature before deployment
verify_and_deploy_image() {
    local tag=${1:-$TAG}
    local deployment_name=${2:-my-application}
    
    echo "Verifying image signature..."
    
    # Pull and verify the signed image
    docker pull "$REGISTRY/$REPOSITORY:$tag"
    
    # Check trust data
    docker trust inspect "$REGISTRY/$REPOSITORY:$tag" --pretty
    
    if [ $? -eq 0 ]; then
        echo "Image signature verification successful"
        
        # Deploy the verified image
        echo "Deploying verified image..."
        kubectl set image deployment/"$deployment_name" \
            "$deployment_name"="$REGISTRY/$REPOSITORY:$tag"
        
        # Wait for rollout to complete
        kubectl rollout status deployment/"$deployment_name" --timeout=300s
        
        echo "Deployment completed successfully"
    else
        echo "ERROR: Image signature verification failed"
        exit 1
    fi
}

# Function to create image attestation
create_image_attestation() {
    local tag=${1:-$TAG}
    
    echo "Creating image attestation..."
    
    # Get image digest
    IMAGE_DIGEST=$(docker inspect --format='{{index .RepoDigests 0}}' "$REGISTRY/$REPOSITORY:$tag")
    
    # Create attestation document
    cat > image-attestation.json << EOF
{
    "attestation_version": "1.0",
    "image": "$REGISTRY/$REPOSITORY:$tag",
    "digest": "$IMAGE_DIGEST",
    "build_time": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "build_system": "GitHub Actions",
    "build_id": "${GITHUB_RUN_ID:-unknown}",
    "source_repository": "${GITHUB_REPOSITORY:-unknown}",
    "source_commit": "${GITHUB_SHA:-unknown}",
    "vulnerability_scan": {
        "scanner": "trivy",
        "scan_time": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
        "status": "passed"
    },
    "compliance_checks": {
        "dockerfile_best_practices": "passed",
        "security_policies": "passed"
    }
}
EOF
    
    # Sign the attestation
    gpg --armor --detach-sign image-attestation.json
    
    # Store attestation in secure location
    aws s3 cp image-attestation.json "s3://my-attestations-bucket/images/$REPOSITORY/$tag/"
    aws s3 cp image-attestation.json.asc "s3://my-attestations-bucket/images/$REPOSITORY/$tag/"
    
    echo "Image attestation created and stored"
}

# Function to verify image attestation
verify_image_attestation() {
    local tag=${1:-$TAG}
    
    echo "Verifying image attestation..."
    
    # Download attestation
    aws s3 cp "s3://my-attestations-bucket/images/$REPOSITORY/$tag/image-attestation.json" ./
    aws s3 cp "s3://my-attestations-bucket/images/$REPOSITORY/$tag/image-attestation.json.asc" ./
    
    # Verify attestation signature
    gpg --verify image-attestation.json.asc image-attestation.json
    
    if [ $? -eq 0 ]; then
        echo "Attestation signature verification successful"
        
        # Validate attestation content
        ATTESTED_DIGEST=$(jq -r '.digest' image-attestation.json)
        CURRENT_DIGEST=$(docker inspect --format='{{index .RepoDigests 0}}' "$REGISTRY/$REPOSITORY:$tag")
        
        if [ "$ATTESTED_DIGEST" = "$CURRENT_DIGEST" ]; then
            echo "Attestation content verification successful"
            return 0
        else
            echo "ERROR: Attestation content verification failed"
            return 1
        fi
    else
        echo "ERROR: Attestation signature verification failed"
        return 1
    fi
}

# Main execution logic
case "${1:-}" in
    "setup")
        setup_signing_keys
        ;;
    "build")
        build_and_sign_image "$2" "$3"
        create_image_attestation
        ;;
    "verify")
        verify_image_attestation "$2"
        ;;
    "deploy")
        if verify_image_attestation "$2"; then
            verify_and_deploy_image "$2" "$3"
        else
            echo "Deployment aborted due to attestation verification failure"
            exit 1
        fi
        ;;
    *)
        echo "Usage: $0 {setup|build|verify|deploy} [arguments]"
        echo "  setup                           - Set up signing keys"
        echo "  build [dockerfile] [context]    - Build and sign image"
        echo "  verify [tag]                    - Verify image attestation"
        echo "  deploy [tag] [deployment]       - Verify and deploy image"
        exit 1
        ;;
esac
```

### Example 3: File integrity monitoring with AIDE

```bash
#!/bin/bash
# Advanced Intrusion Detection Environment (AIDE) setup and monitoring

set -e

# Configuration
AIDE_CONFIG="/etc/aide.conf"
AIDE_DB="/var/lib/aide/aide.db.gz"
AIDE_DB_NEW="/var/lib/aide/aide.db.new.gz"
LOG_FILE="/var/log/aide.log"
ALERT_EMAIL="security@company.com"

# Function to install and configure AIDE
setup_aide() {
    echo "Installing and configuring AIDE..."
    
    # Install AIDE
    if command -v yum &> /dev/null; then
        yum install -y aide
    elif command -v apt-get &> /dev/null; then
        apt-get update && apt-get install -y aide
    else
        echo "ERROR: Unsupported package manager"
        exit 1
    fi
    
    # Create comprehensive AIDE configuration
    cat > "$AIDE_CONFIG" << 'EOF'
# AIDE Configuration for File Integrity Monitoring

# Database and log file locations
database=file:/var/lib/aide/aide.db.gz
database_out=file:/var/lib/aide/aide.db.new.gz
gzip_dbout=yes
verbose=5
report_url=file:/var/log/aide.log
report_url=stdout

# Define what to check
# p = permissions, i = inode, n = number of links, u = user, g = group
# s = size, b = block count, m = mtime, a = atime, c = ctime
# S = check for growing size, md5 = md5 checksum, sha1 = sha1 checksum
# sha256 = sha256 checksum, sha512 = sha512 checksum
# R = p+i+n+u+g+s+m+c+md5
# L = p+i+n+u+g
# E = Empty group
# > = Growing logfile p+u+g+i+n+S

# Custom rule definitions
FIPSR = p+i+n+u+g+s+m+c+md5+sha256+sha512
NORMAL = FIPSR
DIR = p+i+n+u+g
DATAONLY = p+n+u+g+s+md5+sha256+sha512
LSPP = FIPSR
LOG = p+u+g+n+S

# System directories
/boot NORMAL
/bin NORMAL
/sbin NORMAL
/lib NORMAL
/lib64 NORMAL
/opt NORMAL
/usr NORMAL
/root NORMAL

# Configuration files
/etc NORMAL

# Variable directories (logs, temporary files)
/var/log LOG
/var/run DIR
/var/lock DIR

# Exclude temporary and cache directories
!/tmp
!/var/tmp
!/var/cache
!/var/spool
!/proc
!/sys
!/dev
!/run
!/media
!/mnt

# Application-specific directories
/home NORMAL
/srv NORMAL

# Docker and container directories (if applicable)
!/var/lib/docker
!/var/lib/containerd

# Exclude backup files
!.*~
!.*\.bak$
!.*\.tmp$
EOF
    
    echo "AIDE configuration created"
}

# Function to initialize AIDE database
initialize_aide_db() {
    echo "Initializing AIDE database..."
    
    # Initialize the database
    aide --init
    
    # Move the new database to the active location
    if [ -f "$AIDE_DB_NEW" ]; then
        mv "$AIDE_DB_NEW" "$AIDE_DB"
        echo "AIDE database initialized successfully"
    else
        echo "ERROR: Failed to initialize AIDE database"
        exit 1
    fi
}

# Function to run AIDE check
run_aide_check() {
    local send_email=${1:-false}
    
    echo "Running AIDE integrity check..."
    
    # Run AIDE check and capture output
    if aide --check > "$LOG_FILE" 2>&1; then
        echo "AIDE check completed - no changes detected"
        return 0
    else
        echo "AIDE check completed - changes detected"
        
        # Display summary of changes
        echo "=== AIDE Check Summary ==="
        grep -E "(added|removed|changed)" "$LOG_FILE" | head -20
        
        # Send email alert if requested
        if [ "$send_email" = "true" ]; then
            send_aide_alert
        fi
        
        return 1
    fi
}

# Function to send AIDE alert
send_aide_alert() {
    local hostname=$(hostname)
    local timestamp=$(date)
    
    echo "Sending AIDE alert email..."
    
    # Create email content
    cat > /tmp/aide_alert.txt << EOF
Subject: AIDE File Integrity Alert - $hostname

AIDE has detected file system changes on $hostname at $timestamp.

Please review the attached log file for details.

This is an automated security alert. Please investigate immediately.

=== Recent Changes Summary ===
$(grep -E "(added|removed|changed)" "$LOG_FILE" | head -10)

Full log available at: $LOG_FILE
EOF
    
    # Send email (requires mail command to be configured)
    if command -v mail &> /dev/null; then
        mail -s "AIDE Alert - $hostname" "$ALERT_EMAIL" < /tmp/aide_alert.txt
        echo "Alert email sent to $ALERT_EMAIL"
    else
        echo "WARNING: mail command not available - cannot send email alert"
    fi
    
    # Send to syslog
    logger -p security.warning "AIDE: File integrity changes detected on $hostname"
    
    # Clean up
    rm -f /tmp/aide_alert.txt
}

# Function to update AIDE database
update_aide_db() {
    echo "Updating AIDE database..."
    
    # Create new database
    aide --init
    
    # Backup current database
    if [ -f "$AIDE_DB" ]; then
        cp "$AIDE_DB" "${AIDE_DB}.backup.$(date +%Y%m%d_%H%M%S)"
    fi
    
    # Replace current database with new one
    mv "$AIDE_DB_NEW" "$AIDE_DB"
    
    echo "AIDE database updated successfully"
}

# Function to setup automated AIDE monitoring
setup_aide_cron() {
    echo "Setting up automated AIDE monitoring..."
    
    # Create AIDE monitoring script
    cat > /usr/local/bin/aide-monitor.sh << 'EOF'
#!/bin/bash
# Automated AIDE monitoring script

LOG_FILE="/var/log/aide-monitor.log"
AIDE_SCRIPT="/usr/local/bin/aide-integrity.sh"

{
    echo "=== AIDE Monitor - $(date) ==="
    
    # Run AIDE check
    if "$AIDE_SCRIPT" check true; then
        echo "AIDE check passed - no integrity violations"
    else
        echo "AIDE check failed - integrity violations detected"
        
        # Additional security actions
        echo "Triggering additional security measures..."
        
        # Lock down system (example - customize as needed)
        # systemctl stop unnecessary-service
        
        # Send to security monitoring system
        curl -X POST -H "Content-Type: application/json" \
             -d '{"alert":"AIDE integrity violation","hostname":"'$(hostname)'","timestamp":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"}' \
             https://security-monitoring.company.com/alerts || true
    fi
    
    echo "=== AIDE Monitor Complete ==="
    echo ""
} >> "$LOG_FILE" 2>&1
EOF
    
    chmod +x /usr/local/bin/aide-monitor.sh
    
    # Add to crontab (run daily at 2 AM)
    (crontab -l 2>/dev/null; echo "0 2 * * * /usr/local/bin/aide-monitor.sh") | crontab -
    
    echo "AIDE automated monitoring configured"
}

# Function to generate AIDE report
generate_aide_report() {
    local output_file=${1:-/tmp/aide-report.html}
    
    echo "Generating AIDE report..."
    
    # Create HTML report
    cat > "$output_file" << EOF
<!DOCTYPE html>
<html>
<head>
    <title>AIDE File Integrity Report - $(hostname)</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { background-color: #f0f0f0; padding: 10px; border-radius: 5px; }
        .section { margin: 20px 0; }
        .alert { background-color: #ffebee; padding: 10px; border-left: 4px solid #f44336; }
        .success { background-color: #e8f5e8; padding: 10px; border-left: 4px solid #4caf50; }
        pre { background-color: #f5f5f5; padding: 10px; overflow-x: auto; }
    </style>
</head>
<body>
    <div class="header">
        <h1>AIDE File Integrity Report</h1>
        <p><strong>Hostname:</strong> $(hostname)</p>
        <p><strong>Report Generated:</strong> $(date)</p>
    </div>
    
    <div class="section">
        <h2>Database Information</h2>
        <pre>$(aide --version 2>/dev/null || echo "AIDE version information not available")</pre>
        <p><strong>Database Location:</strong> $AIDE_DB</p>
        <p><strong>Database Size:</strong> $(ls -lh "$AIDE_DB" 2>/dev/null | awk '{print $5}' || echo "N/A")</p>
        <p><strong>Last Modified:</strong> $(ls -l "$AIDE_DB" 2>/dev/null | awk '{print $6, $7, $8}' || echo "N/A")</p>
    </div>
    
    <div class="section">
        <h2>Recent Check Results</h2>
EOF
    
    # Add check results
    if [ -f "$LOG_FILE" ]; then
        if grep -q "no changes detected" "$LOG_FILE"; then
            echo '<div class="success"><strong>Status:</strong> No integrity violations detected</div>' >> "$output_file"
        else
            echo '<div class="alert"><strong>Status:</strong> Integrity violations detected</div>' >> "$output_file"
            echo '<h3>Recent Changes:</h3>' >> "$output_file"
            echo '<pre>' >> "$output_file"
            tail -50 "$LOG_FILE" >> "$output_file"
            echo '</pre>' >> "$output_file"
        fi
    else
        echo '<p>No recent check results available</p>' >> "$output_file"
    fi
    
    # Close HTML
    cat >> "$output_file" << EOF
    </div>
</body>
</html>
EOF
    
    echo "AIDE report generated: $output_file"
}

# Main execution logic
case "${1:-}" in
    "setup")
        setup_aide
        initialize_aide_db
        setup_aide_cron
        ;;
    "init")
        initialize_aide_db
        ;;
    "check")
        run_aide_check "$2"
        ;;
    "update")
        update_aide_db
        ;;
    "report")
        generate_aide_report "$2"
        ;;
    "monitor")
        setup_aide_cron
        ;;
    *)
        echo "Usage: $0 {setup|init|check|update|report|monitor} [arguments]"
        echo "  setup                    - Install and configure AIDE"
        echo "  init                     - Initialize AIDE database"
        echo "  check [send_email]       - Run integrity check"
        echo "  update                   - Update AIDE database"
        echo "  report [output_file]     - Generate HTML report"
        echo "  monitor                  - Setup automated monitoring"
        exit 1
        ;;
esac
```

### Example 4: Software supply chain security with SBOM

```python
import json
import hashlib
import requests
import subprocess
from datetime import datetime
from pathlib import Path
import yaml

class SoftwareBillOfMaterials:
    """Software Bill of Materials (SBOM) generator and validator"""
    
    def __init__(self, project_name, version):
        self.project_name = project_name
        self.version = version
        self.sbom_data = {
            "bomFormat": "CycloneDX",
            "specVersion": "1.4",
            "serialNumber": f"urn:uuid:{self._generate_uuid()}",
            "version": 1,
            "metadata": {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "tools": [
                    {
                        "vendor": "Company",
                        "name": "SBOM Generator",
                        "version": "1.0.0"
                    }
                ],
                "component": {
                    "type": "application",
                    "name": project_name,
                    "version": version
                }
            },
            "components": []
        }
    
    def _generate_uuid(self):
        """Generate a UUID for the SBOM"""
        import uuid
        return str(uuid.uuid4())
    
    def _calculate_file_hash(self, file_path, algorithm='sha256'):
        """Calculate hash of a file"""
        hash_obj = hashlib.new(algorithm)
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_obj.update(chunk)
        return hash_obj.hexdigest()
    
    def scan_python_dependencies(self, requirements_file='requirements.txt'):
        """Scan Python dependencies and add to SBOM"""
        print(f"Scanning Python dependencies from {requirements_file}")
        
        try:
            # Get installed packages with versions
            result = subprocess.run(['pip', 'freeze'], capture_output=True, text=True)
            if result.returncode != 0:
                raise Exception("Failed to get pip freeze output")
            
            for line in result.stdout.strip().split('\n'):
                if '==' in line:
                    name, version = line.split('==')
                    self._add_python_component(name.strip(), version.strip())
        
        except Exception as e:
            print(f"Error scanning Python dependencies: {e}")
    
    def _add_python_component(self, name, version):
        """Add a Python component to the SBOM"""
        # Get package information from PyPI
        try:
            response = requests.get(f"https://pypi.org/pypi/{name}/{version}/json", timeout=10)
            if response.status_code == 200:
                package_info = response.json()
                
                component = {
                    "type": "library",
                    "name": name,
                    "version": version,
                    "purl": f"pkg:pypi/{name}@{version}",
                    "description": package_info.get('info', {}).get('summary', ''),
                    "licenses": self._extract_licenses(package_info),
                    "externalReferences": [
                        {
                            "type": "website",
                            "url": package_info.get('info', {}).get('home_page', '')
                        }
                    ]
                }
                
                # Add vulnerability information if available
                vulnerabilities = self._check_vulnerabilities(name, version)
                if vulnerabilities:
                    component['vulnerabilities'] = vulnerabilities
                
                self.sbom_data['components'].append(component)
        
        except Exception as e:
            print(f"Warning: Could not get information for {name}=={version}: {e}")
            # Add basic component information
            component = {
                "type": "library",
                "name": name,
                "version": version,
                "purl": f"pkg:pypi/{name}@{version}"
            }
            self.sbom_data['components'].append(component)
    
    def generate_sbom(self, output_file='sbom.json'):
        """Generate and save SBOM to file"""
        print(f"Generating SBOM: {output_file}")
        
        # Add generation timestamp
        self.sbom_data['metadata']['timestamp'] = datetime.utcnow().isoformat() + "Z"
        
        # Sort components by name for consistency
        self.sbom_data['components'].sort(key=lambda x: x['name'])
        
        # Write SBOM to file
        with open(output_file, 'w') as f:
            json.dump(self.sbom_data, f, indent=2)
        
        # Generate hash of SBOM for integrity verification
        sbom_hash = self._calculate_file_hash(output_file)
        
        # Create integrity file
        integrity_file = f"{output_file}.integrity"
        with open(integrity_file, 'w') as f:
            json.dump({
                "file": output_file,
                "sha256": sbom_hash,
                "generated_at": datetime.utcnow().isoformat() + "Z",
                "generator": "SBOM Generator v1.0.0"
            }, f, indent=2)
        
        print(f"SBOM generated successfully: {output_file}")
        print(f"Integrity file created: {integrity_file}")
        print(f"SBOM SHA256: {sbom_hash}")
        
        return output_file
```

## AWS services to consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Key Management Service (KMS)</h4>
    <p>Makes it easy for you to create and manage cryptographic keys and control their use across a wide range of AWS services. Essential for code signing and integrity validation.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Certificate Manager (ACM)</h4>
    <p>Provisions, manages, and deploys public and private SSL/TLS certificates. Can be used for code signing certificates and integrity validation.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon ECR (Elastic Container Registry)</h4>
    <p>Fully managed Docker container registry with image scanning and signing capabilities. Supports Docker Content Trust for image integrity validation.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS CodeArtifact</h4>
    <p>Fully managed artifact repository service that makes it easy to securely store, publish, and share software packages. Provides package integrity validation.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon Inspector</h4>
    <p>Automatically assesses applications for exposure, vulnerabilities, and deviations from best practices. Helps validate software integrity through vulnerability scanning.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS CloudTrail</h4>
    <p>Records API calls for your account and delivers log files to you. Provides audit trails for software deployment and integrity validation activities.</p>
  </div>
</div>

## Benefits of validating software integrity

- **Supply chain security**: Protects against compromised or malicious software components in the supply chain
- **Tamper detection**: Identifies unauthorized modifications to software and configuration files
- **Compliance assurance**: Helps meet regulatory requirements for software integrity and authenticity
- **Incident response**: Provides forensic capabilities to investigate security incidents and determine impact
- **Trust establishment**: Builds confidence in software authenticity through cryptographic verification
- **Risk reduction**: Minimizes the risk of running compromised or malicious software in production environments
- **Automated validation**: Enables continuous integrity monitoring without manual intervention

## Related resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/sec_protect_compute_validate_software_integrity.html">AWS Well-Architected Framework - Validate software integrity</a></li>
    <li><a href="https://docs.aws.amazon.com/kms/latest/developerguide/overview.html">AWS Key Management Service Developer Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/acm/latest/userguide/acm-overview.html">AWS Certificate Manager User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/AmazonECR/latest/userguide/image-signing.html">Amazon ECR Image Signing</a></li>
    <li><a href="https://docs.docker.com/engine/security/trust/">Docker Content Trust</a></li>
    <li><a href="https://slsa.dev/">Supply-chain Levels for Software Artifacts (SLSA)</a></li>
  </ul>
</div>
