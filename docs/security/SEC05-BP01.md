---
title: SEC05-BP01 - Create network layers
layout: default
parent: SEC05 - How do you protect your network resources?
grand_parent: Security
nav_order: 1
---

<div class="pillar-header">
  <h1>SEC05-BP01: Create network layers</h1>
  <p>Components that share reachability requirements can be segmented into layers. For example, a database in a VPC should be placed in subnets with no routes to or from the internet. This layered approach mitigates the impact of a single layer misconfiguration, which could allow unintended access. For AWS workloads, you can choose from multiple layering strategies.</p>
</div>

## Implementation guidance

Network layering is a fundamental security principle that involves organizing your network infrastructure into distinct segments or layers, each with specific security controls and access requirements. By implementing proper network layers, you can significantly reduce the attack surface and limit the potential impact of security incidents.

### Key steps for implementing this best practice:

1. **Design multi-tier network architecture**:
   - Create separate layers for different application tiers (web, application, database)
   - Implement network segmentation based on security requirements
   - Design layers with appropriate isolation and access controls
   - Plan for scalability and future growth requirements
   - Document network architecture and layer purposes

2. **Implement subnet-based segmentation**:
   - Create public subnets for internet-facing resources
   - Design private subnets for internal application components
   - Establish isolated subnets for sensitive data and databases
   - Use dedicated subnets for management and administrative access
   - Implement subnet-level access controls and routing

3. **Configure routing and connectivity**:
   - Design routing tables for each network layer
   - Implement controlled connectivity between layers
   - Use NAT gateways for outbound internet access from private subnets
   - Configure VPC endpoints for secure AWS service access
   - Establish secure connectivity for hybrid environments

4. **Apply security controls at each layer**:
   - Implement Network ACLs for subnet-level filtering
   - Configure Security Groups for instance-level protection
   - Deploy network firewalls for advanced threat protection
   - Use load balancers for traffic distribution and security
   - Implement intrusion detection and prevention systems

5. **Monitor and maintain network layers**:
   - Enable VPC Flow Logs for network traffic analysis
   - Implement network monitoring and alerting
   - Regularly review and update network configurations
   - Conduct network security assessments
   - Maintain network documentation and diagrams

6. **Implement defense in depth**:
   - Layer multiple security controls for comprehensive protection
   - Use different security mechanisms at each network layer
   - Implement redundant security measures for critical paths
   - Design fail-safe mechanisms for security control failures
   - Regularly test and validate layered security effectiveness

## Implementation examples

### Example 1: Three-tier network architecture

```yaml
# CloudFormation template for three-tier network architecture
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Three-tier network architecture with proper layering'

Parameters:
  VpcCidr:
    Type: String
    Default: '10.0.0.0/16'
    Description: CIDR block for the VPC

Resources:
  # VPC
  MainVPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: !Ref VpcCidr
      EnableDnsHostnames: true
      EnableDnsSupport: true
      Tags:
        - Key: Name
          Value: MainVPC
        - Key: Environment
          Value: Production

  # Internet Gateway
  InternetGateway:
    Type: AWS::EC2::InternetGateway
    Properties:
      Tags:
        - Key: Name
          Value: MainVPC-IGW

  AttachGateway:
    Type: AWS::EC2::VPCGatewayAttachment
    Properties:
      VpcId: !Ref MainVPC
      InternetGatewayId: !Ref InternetGateway

  # Public Subnets (Web Tier)
  PublicSubnet1:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref MainVPC
      CidrBlock: '10.0.1.0/24'
      AvailabilityZone: !Select [0, !GetAZs '']
      MapPublicIpOnLaunch: true
      Tags:
        - Key: Name
          Value: Public-Subnet-1
        - Key: Tier
          Value: Web

  PublicSubnet2:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref MainVPC
      CidrBlock: '10.0.2.0/24'
      AvailabilityZone: !Select [1, !GetAZs '']
      MapPublicIpOnLaunch: true
      Tags:
        - Key: Name
          Value: Public-Subnet-2
        - Key: Tier
          Value: Web

  # Private Subnets (Application Tier)
  PrivateSubnet1:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref MainVPC
      CidrBlock: '10.0.11.0/24'
      AvailabilityZone: !Select [0, !GetAZs '']
      Tags:
        - Key: Name
          Value: Private-Subnet-1
        - Key: Tier
          Value: Application

  PrivateSubnet2:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref MainVPC
      CidrBlock: '10.0.12.0/24'
      AvailabilityZone: !Select [1, !GetAZs '']
      Tags:
        - Key: Name
          Value: Private-Subnet-2
        - Key: Tier
          Value: Application

  # Database Subnets (Data Tier)
  DatabaseSubnet1:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref MainVPC
      CidrBlock: '10.0.21.0/24'
      AvailabilityZone: !Select [0, !GetAZs '']
      Tags:
        - Key: Name
          Value: Database-Subnet-1
        - Key: Tier
          Value: Database

  DatabaseSubnet2:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref MainVPC
      CidrBlock: '10.0.22.0/24'
      AvailabilityZone: !Select [1, !GetAZs '']
      Tags:
        - Key: Name
          Value: Database-Subnet-2
        - Key: Tier
          Value: Database

  # NAT Gateways for private subnet internet access
  NATGateway1EIP:
    Type: AWS::EC2::EIP
    DependsOn: AttachGateway
    Properties:
      Domain: vpc

  NATGateway2EIP:
    Type: AWS::EC2::EIP
    DependsOn: AttachGateway
    Properties:
      Domain: vpc

  NATGateway1:
    Type: AWS::EC2::NatGateway
    Properties:
      AllocationId: !GetAtt NATGateway1EIP.AllocationId
      SubnetId: !Ref PublicSubnet1

  NATGateway2:
    Type: AWS::EC2::NatGateway
    Properties:
      AllocationId: !GetAtt NATGateway2EIP.AllocationId
      SubnetId: !Ref PublicSubnet2

  # Route Tables
  PublicRouteTable:
    Type: AWS::EC2::RouteTable
    Properties:
      VpcId: !Ref MainVPC
      Tags:
        - Key: Name
          Value: Public-Route-Table

  DefaultPublicRoute:
    Type: AWS::EC2::Route
    DependsOn: AttachGateway
    Properties:
      RouteTableId: !Ref PublicRouteTable
      DestinationCidrBlock: '0.0.0.0/0'
      GatewayId: !Ref InternetGateway

  PublicSubnet1RouteTableAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      RouteTableId: !Ref PublicRouteTable
      SubnetId: !Ref PublicSubnet1

  PublicSubnet2RouteTableAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      RouteTableId: !Ref PublicRouteTable
      SubnetId: !Ref PublicSubnet2

  PrivateRouteTable1:
    Type: AWS::EC2::RouteTable
    Properties:
      VpcId: !Ref MainVPC
      Tags:
        - Key: Name
          Value: Private-Route-Table-1

  DefaultPrivateRoute1:
    Type: AWS::EC2::Route
    Properties:
      RouteTableId: !Ref PrivateRouteTable1
      DestinationCidrBlock: '0.0.0.0/0'
      NatGatewayId: !Ref NATGateway1

  PrivateSubnet1RouteTableAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      RouteTableId: !Ref PrivateRouteTable1
      SubnetId: !Ref PrivateSubnet1

  PrivateRouteTable2:
    Type: AWS::EC2::RouteTable
    Properties:
      VpcId: !Ref MainVPC
      Tags:
        - Key: Name
          Value: Private-Route-Table-2

  DefaultPrivateRoute2:
    Type: AWS::EC2::Route
    Properties:
      RouteTableId: !Ref PrivateRouteTable2
      DestinationCidrBlock: '0.0.0.0/0'
      NatGatewayId: !Ref NATGateway2

  PrivateSubnet2RouteTableAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      RouteTableId: !Ref PrivateRouteTable2
      SubnetId: !Ref PrivateSubnet2

  DatabaseRouteTable:
    Type: AWS::EC2::RouteTable
    Properties:
      VpcId: !Ref MainVPC
      Tags:
        - Key: Name
          Value: Database-Route-Table

  DatabaseSubnet1RouteTableAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      RouteTableId: !Ref DatabaseRouteTable
      SubnetId: !Ref DatabaseSubnet1

  DatabaseSubnet2RouteTableAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      RouteTableId: !Ref DatabaseRouteTable
      SubnetId: !Ref DatabaseSubnet2

Outputs:
  VPCId:
    Description: VPC ID
    Value: !Ref MainVPC
    Export:
      Name: !Sub '${AWS::StackName}-VPC-ID'

  PublicSubnets:
    Description: Public subnet IDs
    Value: !Join [',', [!Ref PublicSubnet1, !Ref PublicSubnet2]]
    Export:
      Name: !Sub '${AWS::StackName}-Public-Subnets'

  PrivateSubnets:
    Description: Private subnet IDs
    Value: !Join [',', [!Ref PrivateSubnet1, !Ref PrivateSubnet2]]
    Export:
      Name: !Sub '${AWS::StackName}-Private-Subnets'

  DatabaseSubnets:
    Description: Database subnet IDs
    Value: !Join [',', [!Ref DatabaseSubnet1, !Ref DatabaseSubnet2]]
    Export:
      Name: !Sub '${AWS::StackName}-Database-Subnets'
```

### Example 2: Network ACLs for layer-specific access control

```bash
# Create Network ACLs for different tiers
aws ec2 create-network-acl \
  --vpc-id vpc-12345678 \
  --tag-specifications 'ResourceType=network-acl,Tags=[{Key=Name,Value=Web-Tier-NACL},{Key=Tier,Value=Web}]'

aws ec2 create-network-acl \
  --vpc-id vpc-12345678 \
  --tag-specifications 'ResourceType=network-acl,Tags=[{Key=Name,Value=App-Tier-NACL},{Key=Tier,Value=Application}]'

aws ec2 create-network-acl \
  --vpc-id vpc-12345678 \
  --tag-specifications 'ResourceType=network-acl,Tags=[{Key=Name,Value=DB-Tier-NACL},{Key=Tier,Value=Database}]'

# Configure Web Tier NACL (allow HTTP/HTTPS inbound, ephemeral ports outbound)
aws ec2 create-network-acl-entry \
  --network-acl-id acl-web123456 \
  --rule-number 100 \
  --protocol tcp \
  --rule-action allow \
  --port-range From=80,To=80 \
  --cidr-block 0.0.0.0/0

aws ec2 create-network-acl-entry \
  --network-acl-id acl-web123456 \
  --rule-number 110 \
  --protocol tcp \
  --rule-action allow \
  --port-range From=443,To=443 \
  --cidr-block 0.0.0.0/0

aws ec2 create-network-acl-entry \
  --network-acl-id acl-web123456 \
  --rule-number 100 \
  --protocol tcp \
  --rule-action allow \
  --port-range From=1024,To=65535 \
  --cidr-block 0.0.0.0/0 \
  --egress

# Configure Application Tier NACL (allow from web tier only)
aws ec2 create-network-acl-entry \
  --network-acl-id acl-app123456 \
  --rule-number 100 \
  --protocol tcp \
  --rule-action allow \
  --port-range From=8080,To=8080 \
  --cidr-block 10.0.1.0/24

aws ec2 create-network-acl-entry \
  --network-acl-id acl-app123456 \
  --rule-number 110 \
  --protocol tcp \
  --rule-action allow \
  --port-range From=8080,To=8080 \
  --cidr-block 10.0.2.0/24

# Configure Database Tier NACL (allow from application tier only)
aws ec2 create-network-acl-entry \
  --network-acl-id acl-db123456 \
  --rule-number 100 \
  --protocol tcp \
  --rule-action allow \
  --port-range From=3306,To=3306 \
  --cidr-block 10.0.11.0/24

aws ec2 create-network-acl-entry \
  --network-acl-id acl-db123456 \
  --rule-number 110 \
  --protocol tcp \
  --rule-action allow \
  --port-range From=3306,To=3306 \
  --cidr-block 10.0.12.0/24
```

### Example 3: Security Groups for layered protection

```json
{
  "WebTierSecurityGroup": {
    "Type": "AWS::EC2::SecurityGroup",
    "Properties": {
      "GroupDescription": "Security group for web tier instances",
      "VpcId": {"Ref": "MainVPC"},
      "SecurityGroupIngress": [
        {
          "IpProtocol": "tcp",
          "FromPort": 80,
          "ToPort": 80,
          "CidrIp": "0.0.0.0/0",
          "Description": "Allow HTTP from internet"
        },
        {
          "IpProtocol": "tcp",
          "FromPort": 443,
          "ToPort": 443,
          "CidrIp": "0.0.0.0/0",
          "Description": "Allow HTTPS from internet"
        }
      ],
      "SecurityGroupEgress": [
        {
          "IpProtocol": "tcp",
          "FromPort": 8080,
          "ToPort": 8080,
          "DestinationSecurityGroupId": {"Ref": "AppTierSecurityGroup"},
          "Description": "Allow outbound to application tier"
        }
      ],
      "Tags": [
        {"Key": "Name", "Value": "Web-Tier-SG"},
        {"Key": "Tier", "Value": "Web"}
      ]
    }
  },
  "AppTierSecurityGroup": {
    "Type": "AWS::EC2::SecurityGroup",
    "Properties": {
      "GroupDescription": "Security group for application tier instances",
      "VpcId": {"Ref": "MainVPC"},
      "SecurityGroupIngress": [
        {
          "IpProtocol": "tcp",
          "FromPort": 8080,
          "ToPort": 8080,
          "SourceSecurityGroupId": {"Ref": "WebTierSecurityGroup"},
          "Description": "Allow inbound from web tier"
        }
      ],
      "SecurityGroupEgress": [
        {
          "IpProtocol": "tcp",
          "FromPort": 3306,
          "ToPort": 3306,
          "DestinationSecurityGroupId": {"Ref": "DatabaseTierSecurityGroup"},
          "Description": "Allow outbound to database tier"
        }
      ],
      "Tags": [
        {"Key": "Name", "Value": "App-Tier-SG"},
        {"Key": "Tier", "Value": "Application"}
      ]
    }
  },
  "DatabaseTierSecurityGroup": {
    "Type": "AWS::EC2::SecurityGroup",
    "Properties": {
      "GroupDescription": "Security group for database tier instances",
      "VpcId": {"Ref": "MainVPC"},
      "SecurityGroupIngress": [
        {
          "IpProtocol": "tcp",
          "FromPort": 3306,
          "ToPort": 3306,
          "SourceSecurityGroupId": {"Ref": "AppTierSecurityGroup"},
          "Description": "Allow inbound from application tier"
        }
      ],
      "Tags": [
        {"Key": "Name", "Value": "Database-Tier-SG"},
        {"Key": "Tier", "Value": "Database"}
      ]
    }
  }
}
```

### Example 4: VPC Flow Logs for network monitoring

```python
import boto3
import json
from datetime import datetime

def setup_vpc_flow_logs():
    """Configure VPC Flow Logs for network layer monitoring"""
    
    ec2 = boto3.client('ec2')
    logs = boto3.client('logs')
    
    # Create CloudWatch Log Group for VPC Flow Logs
    log_group_name = '/aws/vpc/flowlogs'
    
    try:
        logs.create_log_group(
            logGroupName=log_group_name,
            retentionInDays=90
        )
        print(f"Created log group: {log_group_name}")
    except logs.exceptions.ResourceAlreadyExistsException:
        print(f"Log group already exists: {log_group_name}")
    
    # Create IAM role for VPC Flow Logs
    iam = boto3.client('iam')
    
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "vpc-flow-logs.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }
    
    flow_logs_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "logs:CreateLogGroup",
                    "logs:CreateLogStream",
                    "logs:PutLogEvents",
                    "logs:DescribeLogGroups",
                    "logs:DescribeLogStreams"
                ],
                "Resource": "*"
            }
        ]
    }
    
    try:
        # Create IAM role
        role_response = iam.create_role(
            RoleName='VPCFlowLogsRole',
            AssumeRolePolicyDocument=json.dumps(trust_policy),
            Description='Role for VPC Flow Logs to write to CloudWatch'
        )
        
        # Attach policy to role
        iam.put_role_policy(
            RoleName='VPCFlowLogsRole',
            PolicyName='VPCFlowLogsPolicy',
            PolicyDocument=json.dumps(flow_logs_policy)
        )
        
        role_arn = role_response['Role']['Arn']
        print(f"Created IAM role: {role_arn}")
        
    except iam.exceptions.EntityAlreadyExistsException:
        # Get existing role ARN
        role_response = iam.get_role(RoleName='VPCFlowLogsRole')
        role_arn = role_response['Role']['Arn']
        print(f"Using existing IAM role: {role_arn}")
    
    # Enable VPC Flow Logs for different network layers
    vpc_id = 'vpc-12345678'  # Replace with your VPC ID
    
    # Custom log format to capture layer-specific information
    log_format = '${srcaddr} ${dstaddr} ${srcport} ${dstport} ${protocol} ${packets} ${bytes} ${windowstart} ${windowend} ${action} ${flowlogstatus} ${subnet-id} ${instance-id}'
    
    try:
        response = ec2.create_flow_logs(
            ResourceType='VPC',
            ResourceIds=[vpc_id],
            TrafficType='ALL',
            LogDestinationType='cloud-watch-logs',
            LogGroupName=log_group_name,
            DeliverLogsPermissionArn=role_arn,
            LogFormat=log_format,
            TagSpecifications=[
                {
                    'ResourceType': 'vpc-flow-log',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': 'VPC-Flow-Logs'
                        },
                        {
                            'Key': 'Purpose',
                            'Value': 'Network-Layer-Monitoring'
                        }
                    ]
                }
            ]
        )
        
        print(f"Created VPC Flow Logs: {response['FlowLogIds']}")
        
    except Exception as e:
        print(f"Error creating VPC Flow Logs: {str(e)}")

def analyze_network_layer_traffic():
    """Analyze VPC Flow Logs for network layer insights"""
    
    logs = boto3.client('logs')
    
    # Query for traffic patterns between network layers
    query = """
    fields @timestamp, srcaddr, dstaddr, srcport, dstport, protocol, action, subnet_id
    | filter action = "ACCEPT"
    | stats count() by srcaddr, dstaddr, dstport
    | sort count desc
    | limit 20
    """
    
    try:
        response = logs.start_query(
            logGroupName='/aws/vpc/flowlogs',
            startTime=int((datetime.now().timestamp() - 3600) * 1000),  # Last hour
            endTime=int(datetime.now().timestamp() * 1000),
            queryString=query
        )
        
        query_id = response['queryId']
        print(f"Started CloudWatch Insights query: {query_id}")
        
        # In a real implementation, you would poll for results
        # and analyze traffic patterns between network layers
        
    except Exception as e:
        print(f"Error starting query: {str(e)}")

# Example usage
if __name__ == "__main__":
    setup_vpc_flow_logs()
    analyze_network_layer_traffic()
```

## AWS services to consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon VPC (Virtual Private Cloud)</h4>
    <p>Provides the foundation for creating network layers with subnets, route tables, and security controls. Essential for implementing network segmentation and isolation.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Security Groups</h4>
    <p>Acts as a virtual firewall for your EC2 instances to control inbound and outbound traffic. Provides stateful packet filtering at the instance level for each network layer.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Network ACLs</h4>
    <p>Provides an additional layer of security for your VPC that acts as a firewall for controlling traffic in and out of subnets. Offers stateless packet filtering at the subnet level.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS NAT Gateway</h4>
    <p>Enables instances in private subnets to connect to the internet or other AWS services while preventing the internet from initiating connections with those instances.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>VPC Endpoints</h4>
    <p>Enables you to privately connect your VPC to supported AWS services without requiring an internet gateway, NAT device, VPN connection, or AWS Direct Connect connection.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Network Firewall</h4>
    <p>A managed service that makes it easy to deploy essential network protections for all of your Amazon VPCs. Provides fine-grained control over network traffic at the VPC level.</p>
  </div>
</div>

## Benefits of creating network layers

- **Reduced attack surface**: Limits the exposure of sensitive resources by isolating them in appropriate network layers
- **Improved security posture**: Enables implementation of defense-in-depth strategies with multiple security controls
- **Better compliance**: Supports regulatory requirements for network segmentation and data protection
- **Enhanced monitoring**: Provides clear boundaries for network traffic analysis and security monitoring
- **Simplified management**: Organizes network resources logically, making configuration and maintenance easier
- **Scalable architecture**: Supports growth and changes in application requirements without compromising security
- **Incident containment**: Limits the spread of security incidents by containing them within specific network layers

## Related resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/sec_network_protection_create_layers.html">AWS Well-Architected Framework - Create network layers</a></li>
    <li><a href="https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html">Amazon VPC User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html">VPCs and subnets</a></li>
    <li><a href="https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-groups.html">Security groups for your VPC</a></li>
    <li><a href="https://docs.aws.amazon.com/vpc/latest/userguide/vpc-network-acls.html">Network ACLs</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-create-a-more-secure-environment-by-using-security-groups-as-a-firewall/">How to create a more secure environment by using security groups as a firewall</a></li>
  </ul>
</div>
