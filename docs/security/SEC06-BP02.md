---
title: SEC06-BP02 - Provision compute from hardened images
layout: default
parent: SEC06 - How do you protect your compute resources?
grand_parent: Security
nav_order: 2
---

<div class="pillar-header">
  <h1>SEC06-BP02: Provision compute from hardened images</h1>
  <p>Build your compute images (such as Amazon Machine Images (AMIs), container images, or VM images) from a hardened operating system, and keep your images up to date with the latest security patches. Remove or disable unnecessary services, and configure your images to meet your security requirements before deploying them to production.</p>
</div>

## Implementation guidance

Hardened images serve as the foundation for secure compute resources by providing a baseline security configuration that reduces the attack surface and ensures consistent security controls across your infrastructure. By starting with hardened images, you can significantly improve your security posture and reduce the time needed to secure new compute resources.

### Key steps for implementing this best practice:

1. **Create hardened base images**:
   - Start with minimal operating system installations
   - Remove unnecessary packages, services, and components
   - Apply security hardening guidelines (CIS benchmarks, STIG)
   - Configure secure default settings and parameters
   - Implement logging and monitoring configurations

2. **Implement automated image building**:
   - Use Infrastructure as Code for consistent image creation
   - Implement automated security scanning during image build
   - Create versioned and immutable image artifacts
   - Establish automated testing for hardened configurations
   - Implement approval workflows for image releases

3. **Maintain image security and updates**:
   - Establish regular image update schedules
   - Implement automated patching and security updates
   - Monitor for new vulnerabilities and security advisories
   - Create processes for emergency security updates
   - Maintain image inventory and lifecycle management

4. **Configure runtime security controls**:
   - Implement host-based intrusion detection systems
   - Configure file integrity monitoring
   - Set up system call monitoring and filtering
   - Implement network security controls at the host level
   - Configure secure boot and trusted platform modules

5. **Establish image governance and compliance**:
   - Create image approval and certification processes
   - Implement compliance scanning and validation
   - Establish image signing and verification
   - Create audit trails for image usage and modifications
   - Implement policy enforcement for image deployment

6. **Monitor and validate hardened configurations**:
   - Implement continuous compliance monitoring
   - Set up configuration drift detection
   - Create automated remediation for configuration violations
   - Establish security metrics and reporting
   - Conduct regular security assessments of deployed images

## Implementation examples

### Example 1: Automated AMI hardening with Packer

```json
{
  "variables": {
    "aws_region": "us-west-2",
    "instance_type": "t3.medium",
    "source_ami": "ami-0c02fb55956c7d316",
    "ami_name": "hardened-amazon-linux-{{timestamp}}"
  },
  "builders": [
    {
      "type": "amazon-ebs",
      "region": "{{user `aws_region`}}",
      "instance_type": "{{user `instance_type`}}",
      "source_ami": "{{user `source_ami`}}",
      "ssh_username": "ec2-user",
      "ami_name": "{{user `ami_name`}}",
      "ami_description": "Hardened Amazon Linux 2 AMI with security configurations",
      "tags": {
        "Name": "{{user `ami_name`}}",
        "Environment": "Production",
        "Hardened": "true",
        "BuildDate": "{{timestamp}}",
        "BaseAMI": "{{user `source_ami`}}"
      },
      "run_tags": {
        "Name": "Packer Builder - {{user `ami_name`}}"
      }
    }
  ],
  "provisioners": [
    {
      "type": "shell",
      "script": "scripts/system-updates.sh"
    },
    {
      "type": "shell",
      "script": "scripts/security-hardening.sh"
    },
    {
      "type": "shell",
      "script": "scripts/cis-benchmark.sh"
    },
    {
      "type": "file",
      "source": "configs/",
      "destination": "/tmp/"
    },
    {
      "type": "shell",
      "script": "scripts/configure-security.sh"
    },
    {
      "type": "shell",
      "script": "scripts/install-security-tools.sh"
    },
    {
      "type": "shell",
      "script": "scripts/cleanup.sh"
    }
  ],
  "post-processors": [
    {
      "type": "manifest",
      "output": "manifest.json",
      "strip_path": true
    }
  ]
}
```

### Example 2: Security hardening scripts

```bash
#!/bin/bash
# security-hardening.sh - Comprehensive security hardening script

set -e

echo "Starting security hardening process..."

# Update system packages
echo "Updating system packages..."
yum update -y
yum install -y aide rkhunter chkrootkit fail2ban

# Remove unnecessary packages
echo "Removing unnecessary packages..."
yum remove -y telnet rsh-server rsh ypbind ypserv tftp tftp-server talk talk-server xinetd

# Disable unnecessary services
echo "Disabling unnecessary services..."
systemctl disable avahi-daemon
systemctl disable cups
systemctl disable nfs
systemctl disable rpcbind
systemctl disable ypbind

# Configure SSH hardening
echo "Hardening SSH configuration..."
cp /etc/ssh/sshd_config /etc/ssh/sshd_config.backup

cat > /etc/ssh/sshd_config << 'EOF'
# SSH Hardened Configuration
Port 22
Protocol 2
HostKey /etc/ssh/ssh_host_rsa_key
HostKey /etc/ssh/ssh_host_ecdsa_key
HostKey /etc/ssh/ssh_host_ed25519_key

# Authentication
LoginGraceTime 60
PermitRootLogin no
StrictModes yes
MaxAuthTries 3
MaxSessions 4
PubkeyAuthentication yes
PasswordAuthentication no
PermitEmptyPasswords no
ChallengeResponseAuthentication no
UsePAM yes

# Security settings
X11Forwarding no
PrintMotd no
PrintLastLog yes
TCPKeepAlive yes
Compression delayed
ClientAliveInterval 300
ClientAliveCountMax 2
AllowTcpForwarding no
AllowAgentForwarding no
GatewayPorts no
PermitTunnel no

# Logging
SyslogFacility AUTHPRIV
LogLevel VERBOSE

# Banner
Banner /etc/issue.net
EOF

# Create security banner
cat > /etc/issue.net << 'EOF'
***************************************************************************
                            NOTICE TO USERS
***************************************************************************
This computer system is the private property of its owner, whether
individual, corporate or government. It is for authorized use only.
Users (authorized or unauthorized) have no explicit or implicit
expectation of privacy.

Any or all uses of this system and all files on this system may be
intercepted, monitored, recorded, copied, audited, inspected, and
disclosed to your employer, to authorized site, government, and law
enforcement personnel, as well as authorized officials of government
agencies, both domestic and foreign.

By using this system, the user consents to such interception, monitoring,
recording, copying, auditing, inspection, and disclosure at the
discretion of such personnel or officials. Unauthorized or improper use
of this system may result in civil and criminal penalties and
administrative or disciplinary action, as appropriate. By continuing to
use this system you indicate your awareness of and consent to these terms
and conditions of use. LOG OFF IMMEDIATELY if you do not agree to the
conditions stated in this warning.
***************************************************************************
EOF

# Configure kernel parameters for security
echo "Configuring kernel security parameters..."
cat > /etc/sysctl.d/99-security.conf << 'EOF'
# IP Spoofing protection
net.ipv4.conf.default.rp_filter = 1
net.ipv4.conf.all.rp_filter = 1

# Ignore ICMP redirects
net.ipv4.conf.all.accept_redirects = 0
net.ipv6.conf.all.accept_redirects = 0
net.ipv4.conf.default.accept_redirects = 0
net.ipv6.conf.default.accept_redirects = 0

# Ignore send redirects
net.ipv4.conf.all.send_redirects = 0
net.ipv4.conf.default.send_redirects = 0

# Disable source packet routing
net.ipv4.conf.all.accept_source_route = 0
net.ipv6.conf.all.accept_source_route = 0
net.ipv4.conf.default.accept_source_route = 0
net.ipv6.conf.default.accept_source_route = 0

# Log Martians
net.ipv4.conf.all.log_martians = 1
net.ipv4.conf.default.log_martians = 1

# Ignore ICMP ping requests
net.ipv4.icmp_echo_ignore_all = 1

# Ignore Directed pings
net.ipv4.icmp_echo_ignore_broadcasts = 1

# Disable IPv6 if not needed
net.ipv6.conf.all.disable_ipv6 = 1
net.ipv6.conf.default.disable_ipv6 = 1

# TCP SYN flood protection
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_max_syn_backlog = 2048
net.ipv4.tcp_synack_retries = 2
net.ipv4.tcp_syn_retries = 5

# Control buffer overflow attacks
kernel.exec-shield = 1
kernel.randomize_va_space = 2
EOF

# Apply sysctl settings
sysctl -p /etc/sysctl.d/99-security.conf

# Configure file permissions
echo "Setting secure file permissions..."
chmod 700 /root
chmod 600 /etc/ssh/sshd_config
chmod 644 /etc/passwd
chmod 000 /etc/shadow
chmod 000 /etc/gshadow
chmod 644 /etc/group

# Configure password policies
echo "Configuring password policies..."
cat > /etc/security/pwquality.conf << 'EOF'
# Password quality requirements
minlen = 14
minclass = 4
maxrepeat = 2
maxclasrepeat = 2
lcredit = -1
ucredit = -1
dcredit = -1
ocredit = -1
difok = 8
gecoscheck = 1
dictcheck = 1
usercheck = 1
enforcing = 1
EOF

# Configure account lockout
cat > /etc/security/faillock.conf << 'EOF'
# Account lockout configuration
deny = 5
fail_interval = 900
unlock_time = 600
EOF

# Configure audit system
echo "Configuring audit system..."
systemctl enable auditd

cat > /etc/audit/rules.d/audit.rules << 'EOF'
# Delete all existing rules
-D

# Buffer Size
-b 8192

# Failure Mode
-f 1

# Audit the audit logs
-w /var/log/audit/ -p wa -k auditlog

# Audit the configuration files
-w /etc/audit/ -p wa -k auditconfig
-w /etc/libaudit.conf -p wa -k auditconfig
-w /etc/audisp/ -p wa -k audispconfig

# Monitor for changes to system administration scope
-w /etc/sudoers -p wa -k scope
-w /etc/sudoers.d/ -p wa -k scope

# Monitor authentication events
-w /etc/passwd -p wa -k identity
-w /etc/group -p wa -k identity
-w /etc/gshadow -p wa -k identity
-w /etc/shadow -p wa -k identity
-w /etc/security/opasswd -p wa -k identity

# Monitor login configuration
-w /etc/login.defs -p wa -k login
-w /etc/securetty -p wa -k login
-w /var/log/faillog -p wa -k login
-w /var/log/lastlog -p wa -k login
-w /var/log/tallylog -p wa -k login

# Monitor network configuration
-w /etc/hosts -p wa -k network
-w /etc/sysconfig/network -p wa -k network
-w /etc/sysconfig/network-scripts/ -p wa -k network

# Monitor system startup scripts
-w /etc/inittab -p wa -k init
-w /etc/init.d/ -p wa -k init
-w /etc/init/ -p wa -k init

# Monitor library searches
-w /etc/ld.so.conf -p wa -k libpath

# Monitor kernel module loading and unloading
-w /sbin/insmod -p x -k modules
-w /sbin/rmmod -p x -k modules
-w /sbin/modprobe -p x -k modules
-a always,exit -F arch=b64 -S init_module -S delete_module -k modules

# Make the configuration immutable
-e 2
EOF

# Install and configure AIDE (Advanced Intrusion Detection Environment)
echo "Configuring AIDE..."
aide --init
mv /var/lib/aide/aide.db.new.gz /var/lib/aide/aide.db.gz

# Create daily AIDE check
cat > /etc/cron.daily/aide-check << 'EOF'
#!/bin/bash
/usr/sbin/aide --check | /bin/mail -s "AIDE Report - $(hostname)" root
EOF
chmod +x /etc/cron.daily/aide-check

# Configure fail2ban
echo "Configuring fail2ban..."
systemctl enable fail2ban

cat > /etc/fail2ban/jail.local << 'EOF'
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 3
backend = systemd

[sshd]
enabled = true
port = ssh
logpath = %(sshd_log)s
maxretry = 3
bantime = 3600
EOF

# Configure log rotation
echo "Configuring log rotation..."
cat > /etc/logrotate.d/security << 'EOF'
/var/log/secure {
    weekly
    rotate 52
    compress
    delaycompress
    missingok
    notifempty
    create 600 root root
}

/var/log/audit/audit.log {
    weekly
    rotate 52
    compress
    delaycompress
    missingok
    notifempty
    create 600 root root
    postrotate
        /sbin/service auditd restart > /dev/null 2>&1 || true
    endscript
}
EOF

# Remove history files and temporary files
echo "Cleaning up..."
rm -f /root/.bash_history
rm -f /home/*/.bash_history
rm -rf /tmp/*
rm -rf /var/tmp/*

# Clear log files
> /var/log/messages
> /var/log/secure
> /var/log/maillog
> /var/log/cron
> /var/log/boot.log

echo "Security hardening completed successfully!"
```

### Example 3: Container image hardening with multi-stage builds

```dockerfile
# Multi-stage Dockerfile for hardened container images
# Stage 1: Build stage
FROM node:18-alpine AS builder

# Create app directory
WORKDIR /usr/src/app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production && npm cache clean --force

# Copy source code
COPY . .

# Build application
RUN npm run build

# Stage 2: Security scanning stage
FROM builder AS security-scan

# Install security scanning tools
RUN apk add --no-cache \
    curl \
    wget

# Run security scans (this would typically be done in CI/CD)
# RUN npm audit --audit-level=high
# RUN trivy fs --exit-code 1 --severity HIGH,CRITICAL .

# Stage 3: Production stage with hardened base
FROM alpine:3.18 AS production

# Install only necessary packages
RUN apk add --no-cache \
    nodejs \
    npm \
    dumb-init \
    && rm -rf /var/cache/apk/*

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001 -G nodejs

# Set up application directory
WORKDIR /usr/src/app

# Copy built application from builder stage
COPY --from=builder --chown=nodejs:nodejs /usr/src/app/dist ./dist
COPY --from=builder --chown=nodejs:nodejs /usr/src/app/node_modules ./node_modules
COPY --from=builder --chown=nodejs:nodejs /usr/src/app/package*.json ./

# Security hardening
RUN chmod -R 755 /usr/src/app && \
    chown -R nodejs:nodejs /usr/src/app

# Remove unnecessary files and packages
RUN rm -rf /tmp/* /var/tmp/* /var/cache/apk/*

# Set security-focused environment variables
ENV NODE_ENV=production
ENV NPM_CONFIG_LOGLEVEL=warn
ENV NPM_CONFIG_AUDIT_LEVEL=high

# Use non-root user
USER nodejs

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD node healthcheck.js

# Use dumb-init to handle signals properly
ENTRYPOINT ["dumb-init", "--"]

# Start application
CMD ["node", "dist/index.js"]

# Security labels
LABEL security.scan.date="$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
      security.hardened="true" \
      security.non-root="true" \
      security.minimal="true"
```

### Example 4: Infrastructure as Code for hardened EC2 instances

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Hardened EC2 instances with security configurations'

Parameters:
  HardenedAMIId:
    Type: AWS::EC2::Image::Id
    Description: 'ID of the hardened AMI to use'
  
  InstanceType:
    Type: String
    Default: 't3.medium'
    Description: 'EC2 instance type'
  
  KeyPairName:
    Type: AWS::EC2::KeyPair::KeyName
    Description: 'EC2 Key Pair for SSH access'

Resources:
  # Security group for hardened instances
  HardenedInstanceSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: 'Security group for hardened EC2 instances'
      VpcId: !Ref VPC
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 22
          ToPort: 22
          SourceSecurityGroupId: !Ref BastionSecurityGroup
          Description: 'SSH access from bastion host only'
      SecurityGroupEgress:
        - IpProtocol: tcp
          FromPort: 443
          ToPort: 443
          CidrIp: '0.0.0.0/0'
          Description: 'HTTPS outbound for updates'
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: '0.0.0.0/0'
          Description: 'HTTP outbound for package updates'
        - IpProtocol: udp
          FromPort: 53
          ToPort: 53
          CidrIp: '0.0.0.0/0'
          Description: 'DNS resolution'
      Tags:
        - Key: Name
          Value: 'Hardened-Instance-SG'

  # IAM role for hardened instances
  HardenedInstanceRole:
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
        - arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy
      Policies:
        - PolicyName: SecurityLogging
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
                  - s3:GetObject
                Resource: 
                  - !Sub '${SecurityLogsBucket}/*'

  # Instance profile
  HardenedInstanceProfile:
    Type: AWS::IAM::InstanceProfile
    Properties:
      Roles:
        - !Ref HardenedInstanceRole

  # Launch template for hardened instances
  HardenedInstanceLaunchTemplate:
    Type: AWS::EC2::LaunchTemplate
    Properties:
      LaunchTemplateName: 'HardenedInstanceTemplate'
      LaunchTemplateData:
        ImageId: !Ref HardenedAMIId
        InstanceType: !Ref InstanceType
        KeyName: !Ref KeyPairName
        IamInstanceProfile:
          Arn: !GetAtt HardenedInstanceProfile.Arn
        SecurityGroupIds:
          - !Ref HardenedInstanceSecurityGroup
        BlockDeviceMappings:
          - DeviceName: '/dev/xvda'
            Ebs:
              VolumeSize: 20
              VolumeType: 'gp3'
              Encrypted: true
              DeleteOnTermination: true
        MetadataOptions:
          HttpTokens: required
          HttpPutResponseHopLimit: 1
          HttpEndpoint: enabled
        Monitoring:
          Enabled: true
        UserData:
          Fn::Base64: !Sub |
            #!/bin/bash
            yum update -y
            
            # Install CloudWatch agent
            wget https://s3.amazonaws.com/amazoncloudwatch-agent/amazon_linux/amd64/latest/amazon-cloudwatch-agent.rpm
            rpm -U ./amazon-cloudwatch-agent.rpm
            
            # Configure CloudWatch agent
            cat > /opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json << 'EOF'
            {
              "agent": {
                "metrics_collection_interval": 60,
                "run_as_user": "cwagent"
              },
              "logs": {
                "logs_collected": {
                  "files": {
                    "collect_list": [
                      {
                        "file_path": "/var/log/secure",
                        "log_group_name": "/aws/ec2/security",
                        "log_stream_name": "{instance_id}/secure"
                      },
                      {
                        "file_path": "/var/log/audit/audit.log",
                        "log_group_name": "/aws/ec2/audit",
                        "log_stream_name": "{instance_id}/audit"
                      }
                    ]
                  }
                }
              },
              "metrics": {
                "namespace": "CWAgent",
                "metrics_collected": {
                  "cpu": {
                    "measurement": [
                      "cpu_usage_idle",
                      "cpu_usage_iowait",
                      "cpu_usage_user",
                      "cpu_usage_system"
                    ],
                    "metrics_collection_interval": 60
                  },
                  "disk": {
                    "measurement": [
                      "used_percent"
                    ],
                    "metrics_collection_interval": 60,
                    "resources": [
                      "*"
                    ]
                  },
                  "mem": {
                    "measurement": [
                      "mem_used_percent"
                    ],
                    "metrics_collection_interval": 60
                  }
                }
              }
            }
            EOF
            
            # Start CloudWatch agent
            /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
              -a fetch-config -m ec2 -s \
              -c file:/opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json
            
            # Configure additional security settings
            echo "Configuring additional security settings..."
            
            # Enable automatic security updates
            echo "0 2 * * * root yum update -y --security" >> /etc/crontab
            
            # Configure log forwarding to S3
            cat > /etc/cron.daily/log-backup << 'EOF'
            #!/bin/bash
            DATE=$(date +%Y-%m-%d)
            tar -czf /tmp/logs-$DATE.tar.gz /var/log/secure /var/log/audit/audit.log
            aws s3 cp /tmp/logs-$DATE.tar.gz s3://${SecurityLogsBucket}/$(curl -s http://169.254.169.254/latest/meta-data/instance-id)/
            rm -f /tmp/logs-$DATE.tar.gz
            EOF
            chmod +x /etc/cron.daily/log-backup
            
            # Signal completion
            /opt/aws/bin/cfn-signal -e $? --stack ${AWS::StackName} --resource HardenedAutoScalingGroup --region ${AWS::Region}

  # Auto Scaling Group for hardened instances
  HardenedAutoScalingGroup:
    Type: AWS::AutoScaling::AutoScalingGroup
    Properties:
      AutoScalingGroupName: 'HardenedInstancesASG'
      LaunchTemplate:
        LaunchTemplateId: !Ref HardenedInstanceLaunchTemplate
        Version: !GetAtt HardenedInstanceLaunchTemplate.LatestVersionNumber
      MinSize: 1
      MaxSize: 3
      DesiredCapacity: 2
      VPCZoneIdentifier:
        - !Ref PrivateSubnet1
        - !Ref PrivateSubnet2
      HealthCheckType: EC2
      HealthCheckGracePeriod: 300
      Tags:
        - Key: Name
          Value: 'Hardened-Instance'
          PropagateAtLaunch: true
        - Key: Environment
          Value: 'Production'
          PropagateAtLaunch: true
        - Key: Hardened
          Value: 'true'
          PropagateAtLaunch: true
    CreationPolicy:
      ResourceSignal:
        Count: 2
        Timeout: PT15M

  # S3 bucket for security logs
  SecurityLogsBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub 'security-logs-${AWS::AccountId}-${AWS::Region}'
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
          - Id: SecurityLogsRetention
            Status: Enabled
            Transitions:
              - TransitionInDays: 30
                StorageClass: STANDARD_IA
              - TransitionInDays: 90
                StorageClass: GLACIER
            ExpirationInDays: 2555  # 7 years

Outputs:
  LaunchTemplateId:
    Description: 'ID of the hardened instance launch template'
    Value: !Ref HardenedInstanceLaunchTemplate
    Export:
      Name: !Sub '${AWS::StackName}-LaunchTemplate'

  AutoScalingGroupName:
    Description: 'Name of the hardened instances Auto Scaling Group'
    Value: !Ref HardenedAutoScalingGroup
    Export:
      Name: !Sub '${AWS::StackName}-ASG'

## AWS services to consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon EC2 Image Builder</h4>
    <p>Simplifies the building, testing, and deployment of Virtual Machine and container images for use on AWS or on-premises. Provides automated image hardening and security scanning capabilities.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Systems Manager</h4>
    <p>Gives you visibility and control of your infrastructure on AWS. Provides patch management, configuration compliance, and automation capabilities for maintaining hardened images.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon Inspector</h4>
    <p>Automatically assesses applications for exposure, vulnerabilities, and deviations from best practices. Provides vulnerability scanning for AMIs and container images.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon ECR (Elastic Container Registry)</h4>
    <p>Fully managed Docker container registry that makes it easy to store, manage, and deploy Docker container images. Includes vulnerability scanning for container images.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Config</h4>
    <p>Enables you to assess, audit, and evaluate the configurations of your AWS resources. Helps monitor compliance with hardening standards and detect configuration drift.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS CloudFormation</h4>
    <p>Gives you an easy way to model a collection of related AWS and third-party resources. Enables Infrastructure as Code for consistent deployment of hardened compute resources.</p>
  </div>
</div>

## Benefits of provisioning compute from hardened images

- **Reduced attack surface**: Hardened images remove unnecessary components and services that could be exploited by attackers
- **Consistent security baseline**: All compute resources start with the same security configuration, ensuring uniform protection
- **Faster deployment**: Pre-hardened images reduce the time needed to secure new compute resources
- **Compliance assurance**: Hardened images can be configured to meet specific compliance requirements and security standards
- **Reduced configuration drift**: Starting with hardened images minimizes the risk of security misconfigurations
- **Improved incident response**: Standardized hardened images make it easier to investigate and respond to security incidents
- **Cost efficiency**: Automated hardening reduces manual security configuration effort and associated costs

## Related resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/sec_protect_compute_hardened_images.html">AWS Well-Architected Framework - Provision compute from hardened images</a></li>
    <li><a href="https://docs.aws.amazon.com/imagebuilder/latest/userguide/what-is-image-builder.html">EC2 Image Builder User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/systems-manager/latest/userguide/what-is-systems-manager.html">AWS Systems Manager User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/inspector/latest/userguide/inspector_introduction.html">Amazon Inspector User Guide</a></li>
    <li><a href="https://www.cisecurity.org/cis-benchmarks/">CIS Benchmarks</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-create-hardened-amis-for-amazon-ec2/">How to create hardened AMIs for Amazon EC2</a></li>
  </ul>
</div>

## AWS services to consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon EC2 Image Builder</h4>
    <p>Simplifies the building, testing, and deployment of Virtual Machine and container images for use on AWS or on-premises. Provides automated image hardening and security scanning capabilities.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Systems Manager</h4>
    <p>Gives you visibility and control of your infrastructure on AWS. Provides patch management, configuration compliance, and automation capabilities for maintaining hardened images.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon Inspector</h4>
    <p>Automatically assesses applications for exposure, vulnerabilities, and deviations from best practices. Provides vulnerability scanning for AMIs and container images.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon ECR (Elastic Container Registry)</h4>
    <p>Fully managed Docker container registry that makes it easy to store, manage, and deploy Docker container images. Includes vulnerability scanning for container images.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Config</h4>
    <p>Enables you to assess, audit, and evaluate the configurations of your AWS resources. Helps monitor compliance with hardening standards and detect configuration drift.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS CloudFormation</h4>
    <p>Gives you an easy way to model a collection of related AWS and third-party resources. Enables Infrastructure as Code for consistent deployment of hardened compute resources.</p>
  </div>
</div>

## Benefits of provisioning compute from hardened images

- **Reduced attack surface**: Hardened images remove unnecessary components and services that could be exploited by attackers
- **Consistent security baseline**: All compute resources start with the same security configuration, ensuring uniform protection
- **Faster deployment**: Pre-hardened images reduce the time needed to secure new compute resources
- **Compliance assurance**: Hardened images can be configured to meet specific compliance requirements and security standards
- **Reduced configuration drift**: Starting with hardened images minimizes the risk of security misconfigurations
- **Improved incident response**: Standardized hardened images make it easier to investigate and respond to security incidents
- **Cost efficiency**: Automated hardening reduces manual security configuration effort and associated costs

## Related resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/sec_protect_compute_hardened_images.html">AWS Well-Architected Framework - Provision compute from hardened images</a></li>
    <li><a href="https://docs.aws.amazon.com/imagebuilder/latest/userguide/what-is-image-builder.html">EC2 Image Builder User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/systems-manager/latest/userguide/what-is-systems-manager.html">AWS Systems Manager User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/inspector/latest/userguide/inspector_introduction.html">Amazon Inspector User Guide</a></li>
    <li><a href="https://www.cisecurity.org/cis-benchmarks/">CIS Benchmarks</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-create-hardened-amis-for-amazon-ec2/">How to create hardened AMIs for Amazon EC2</a></li>
  </ul>
</div>
```
