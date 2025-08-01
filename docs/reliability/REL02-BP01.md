---
title: REL02-BP01 - Use highly available network connectivity for your workload public endpoints
layout: default
parent: REL02 - How do you plan your network topology?
grand_parent: Reliability
nav_order: 1
---

# REL02-BP01: Use highly available network connectivity for your workload public endpoints

## Overview

Implement highly available network connectivity for your workload's public endpoints to ensure reliable access for users and external systems. This involves deploying redundant network infrastructure, using multiple Availability Zones, implementing global load balancing, and establishing resilient DNS resolution to eliminate single points of failure in your network architecture.

## Implementation Steps

### 1. Deploy Multi-AZ Load Balancing Infrastructure
- Implement Application Load Balancers (ALB) or Network Load Balancers (NLB) across multiple Availability Zones
- Configure cross-zone load balancing for even traffic distribution
- Set up health checks and automatic failover mechanisms
- Establish load balancer redundancy and backup strategies

### 2. Implement Global Traffic Management
- Deploy Amazon CloudFront for global content delivery and edge caching
- Configure Route 53 with health checks and DNS failover policies
- Implement geolocation and latency-based routing for optimal performance
- Set up multi-region traffic distribution and disaster recovery routing

### 3. Establish Redundant Network Connectivity
- Configure multiple internet gateways and NAT gateways across AZs
- Implement VPC peering and Transit Gateway for inter-VPC connectivity
- Set up redundant Direct Connect connections with backup paths
- Establish multiple network paths and eliminate single points of failure

### 4. Configure Advanced Health Monitoring
- Implement comprehensive health checks at multiple layers
- Set up synthetic monitoring and real user monitoring (RUM)
- Configure automated failover based on health check results
- Establish network performance monitoring and alerting

### 5. Implement Security and DDoS Protection
- Deploy AWS Shield Advanced for DDoS protection
- Configure AWS WAF for application-layer security
- Implement network ACLs and security groups for defense in depth
- Set up VPC Flow Logs for network traffic analysis

### 6. Establish Disaster Recovery and Failover Procedures
- Configure cross-region failover capabilities
- Implement automated disaster recovery workflows
- Set up backup DNS resolution and emergency routing
- Establish network recovery testing and validation procedures

## Implementation Examples

### Example 1: Multi-AZ Highly Available Web Application Architecture
```python
import boto3
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import time
import concurrent.futures

@dataclass
class HealthCheckConfig:
    protocol: str
    port: int
    path: str
    interval: int = 30
    timeout: int = 5
    healthy_threshold: int = 3
    unhealthy_threshold: int = 3

@dataclass
class LoadBalancerConfig:
    name: str
    scheme: str  # internet-facing or internal
    load_balancer_type: str  # application, network, or gateway
    subnets: List[str]
    security_groups: List[str]
    health_check: HealthCheckConfig

class HighlyAvailableWebArchitecture:
    def __init__(self, config: Dict):
        self.config = config
        self.ec2 = boto3.client('ec2')
        self.elbv2 = boto3.client('elbv2')
        self.route53 = boto3.client('route53')
        self.cloudfront = boto3.client('cloudfront')
        self.wafv2 = boto3.client('wafv2')
        self.shield = boto3.client('shield')
        self.cloudwatch = boto3.client('cloudwatch')
        
    def deploy_highly_available_architecture(self, architecture_config: Dict) -> Dict:
        """Deploy complete highly available web architecture"""
        deployment_id = f"ha_web_{int(datetime.utcnow().timestamp())}"
        
        deployment_result = {
            'deployment_id': deployment_id,
            'timestamp': datetime.utcnow().isoformat(),
            'architecture_config': architecture_config,
            'components': {},
            'status': 'initiated'
        }
        
        try:
            # 1. Create VPC and networking infrastructure
            vpc_result = self.create_vpc_infrastructure(architecture_config.get('vpc_config', {}))
            deployment_result['components']['vpc'] = vpc_result
            
            # 2. Deploy load balancers across multiple AZs
            lb_result = self.deploy_load_balancers(
                architecture_config.get('load_balancer_configs', []),
                vpc_result['subnets']
            )
            deployment_result['components']['load_balancers'] = lb_result
            
            # 3. Configure Route 53 DNS with health checks
            dns_result = self.configure_dns_with_health_checks(
                architecture_config.get('dns_config', {}),
                lb_result
            )
            deployment_result['components']['dns'] = dns_result
            
            # 4. Deploy CloudFront distribution
            cloudfront_result = self.deploy_cloudfront_distribution(
                architecture_config.get('cloudfront_config', {}),
                lb_result
            )
            deployment_result['components']['cloudfront'] = cloudfront_result
            
            # 5. Configure WAF and Shield protection
            security_result = self.configure_security_protection(
                architecture_config.get('security_config', {}),
                cloudfront_result
            )
            deployment_result['components']['security'] = security_result
            
            # 6. Set up monitoring and alerting
            monitoring_result = self.setup_monitoring_and_alerting(
                deployment_id, deployment_result['components']
            )
            deployment_result['components']['monitoring'] = monitoring_result
            
            deployment_result['status'] = 'completed'
            
        except Exception as e:
            logging.error(f"Error deploying highly available architecture: {str(e)}")
            deployment_result['status'] = 'failed'
            deployment_result['error'] = str(e)
        
        return deployment_result
    
    def create_vpc_infrastructure(self, vpc_config: Dict) -> Dict:
        """Create VPC with multi-AZ subnets and redundant gateways"""
        try:
            # Create VPC
            vpc_response = self.ec2.create_vpc(
                CidrBlock=vpc_config.get('cidr_block', '10.0.0.0/16'),
                TagSpecifications=[
                    {
                        'ResourceType': 'vpc',
                        'Tags': [
                            {'Key': 'Name', 'Value': vpc_config.get('name', 'ha-web-vpc')},
                            {'Key': 'Purpose', 'Value': 'HighlyAvailableWeb'}
                        ]
                    }
                ]
            )
            vpc_id = vpc_response['Vpc']['VpcId']
            
            # Enable DNS hostnames and resolution
            self.ec2.modify_vpc_attribute(VpcId=vpc_id, EnableDnsHostnames={'Value': True})
            self.ec2.modify_vpc_attribute(VpcId=vpc_id, EnableDnsSupport={'Value': True})
            
            # Get available AZs
            azs_response = self.ec2.describe_availability_zones(
                Filters=[{'Name': 'state', 'Values': ['available']}]
            )
            available_azs = [az['ZoneName'] for az in azs_response['AvailabilityZones'][:3]]
            
            # Create subnets across multiple AZs
            subnets = self.create_multi_az_subnets(vpc_id, available_azs, vpc_config)
            
            # Create and attach Internet Gateway
            igw_response = self.ec2.create_internet_gateway(
                TagSpecifications=[
                    {
                        'ResourceType': 'internet-gateway',
                        'Tags': [
                            {'Key': 'Name', 'Value': f"{vpc_config.get('name', 'ha-web')}-igw"},
                            {'Key': 'Purpose', 'Value': 'HighlyAvailableWeb'}
                        ]
                    }
                ]
            )
            igw_id = igw_response['InternetGateway']['InternetGatewayId']
            self.ec2.attach_internet_gateway(InternetGatewayId=igw_id, VpcId=vpc_id)
            
            # Create NAT Gateways in each AZ for high availability
            nat_gateways = self.create_nat_gateways(subnets['public'], available_azs)
            
            # Create route tables
            route_tables = self.create_route_tables(vpc_id, igw_id, nat_gateways, subnets)
            
            return {
                'vpc_id': vpc_id,
                'internet_gateway_id': igw_id,
                'availability_zones': available_azs,
                'subnets': subnets,
                'nat_gateways': nat_gateways,
                'route_tables': route_tables,
                'status': 'created'
            }
            
        except Exception as e:
            logging.error(f"Error creating VPC infrastructure: {str(e)}")
            raise
    
    def create_multi_az_subnets(self, vpc_id: str, azs: List[str], vpc_config: Dict) -> Dict:
        """Create public and private subnets across multiple AZs"""
        subnets = {'public': [], 'private': []}
        
        base_cidr = vpc_config.get('cidr_block', '10.0.0.0/16')
        base_network = base_cidr.split('/')[0].split('.')
        
        for i, az in enumerate(azs):
            # Public subnet
            public_cidr = f"{base_network[0]}.{base_network[1]}.{i * 2}.0/24"
            public_response = self.ec2.create_subnet(
                VpcId=vpc_id,
                CidrBlock=public_cidr,
                AvailabilityZone=az,
                TagSpecifications=[
                    {
                        'ResourceType': 'subnet',
                        'Tags': [
                            {'Key': 'Name', 'Value': f"public-subnet-{az}"},
                            {'Key': 'Type', 'Value': 'Public'},
                            {'Key': 'Purpose', 'Value': 'HighlyAvailableWeb'}
                        ]
                    }
                ]
            )
            
            public_subnet_id = public_response['Subnet']['SubnetId']
            
            # Enable auto-assign public IP for public subnets
            self.ec2.modify_subnet_attribute(
                SubnetId=public_subnet_id,
                MapPublicIpOnLaunch={'Value': True}
            )
            
            subnets['public'].append({
                'subnet_id': public_subnet_id,
                'availability_zone': az,
                'cidr_block': public_cidr
            })
            
            # Private subnet
            private_cidr = f"{base_network[0]}.{base_network[1]}.{i * 2 + 1}.0/24"
            private_response = self.ec2.create_subnet(
                VpcId=vpc_id,
                CidrBlock=private_cidr,
                AvailabilityZone=az,
                TagSpecifications=[
                    {
                        'ResourceType': 'subnet',
                        'Tags': [
                            {'Key': 'Name', 'Value': f"private-subnet-{az}"},
                            {'Key': 'Type', 'Value': 'Private'},
                            {'Key': 'Purpose', 'Value': 'HighlyAvailableWeb'}
                        ]
                    }
                ]
            )
            
            subnets['private'].append({
                'subnet_id': private_response['Subnet']['SubnetId'],
                'availability_zone': az,
                'cidr_block': private_cidr
            })
        
        return subnets
    
    def create_nat_gateways(self, public_subnets: List[Dict], azs: List[str]) -> List[Dict]:
        """Create NAT Gateways in each AZ for high availability"""
        nat_gateways = []
        
        for i, subnet in enumerate(public_subnets):
            # Allocate Elastic IP for NAT Gateway
            eip_response = self.ec2.allocate_address(
                Domain='vpc',
                TagSpecifications=[
                    {
                        'ResourceType': 'elastic-ip',
                        'Tags': [
                            {'Key': 'Name', 'Value': f"nat-gateway-eip-{azs[i]}"},
                            {'Key': 'Purpose', 'Value': 'HighlyAvailableWeb'}
                        ]
                    }
                ]
            )
            
            # Create NAT Gateway
            nat_response = self.ec2.create_nat_gateway(
                SubnetId=subnet['subnet_id'],
                AllocationId=eip_response['AllocationId'],
                TagSpecifications=[
                    {
                        'ResourceType': 'nat-gateway',
                        'Tags': [
                            {'Key': 'Name', 'Value': f"nat-gateway-{azs[i]}"},
                            {'Key': 'Purpose', 'Value': 'HighlyAvailableWeb'}
                        ]
                    }
                ]
            )
            
            nat_gateways.append({
                'nat_gateway_id': nat_response['NatGateway']['NatGatewayId'],
                'availability_zone': azs[i],
                'subnet_id': subnet['subnet_id'],
                'elastic_ip': eip_response['PublicIp']
            })
        
        # Wait for NAT Gateways to be available
        self.wait_for_nat_gateways([ng['nat_gateway_id'] for ng in nat_gateways])
        
        return nat_gateways
    
    def wait_for_nat_gateways(self, nat_gateway_ids: List[str], timeout: int = 300):
        """Wait for NAT Gateways to become available"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            response = self.ec2.describe_nat_gateways(NatGatewayIds=nat_gateway_ids)
            
            all_available = all(
                ng['State'] == 'available' for ng in response['NatGateways']
            )
            
            if all_available:
                logging.info("All NAT Gateways are available")
                return
            
            time.sleep(10)
        
        raise TimeoutError("NAT Gateways did not become available within timeout period")
    
    def deploy_load_balancers(self, lb_configs: List[Dict], subnets: Dict) -> Dict:
        """Deploy Application Load Balancers across multiple AZs"""
        load_balancers = []
        
        # Create security group for load balancers
        sg_response = self.ec2.create_security_group(
            GroupName='ha-web-alb-sg',
            Description='Security group for highly available web ALB',
            VpcId=subnets['public'][0]['subnet_id'].split('-')[0]  # Extract VPC ID
        )
        
        # Get VPC ID properly
        subnet_response = self.ec2.describe_subnets(
            SubnetIds=[subnets['public'][0]['subnet_id']]
        )
        vpc_id = subnet_response['Subnets'][0]['VpcId']
        
        # Create security group properly
        sg_response = self.ec2.create_security_group(
            GroupName=f'ha-web-alb-sg-{int(time.time())}',
            Description='Security group for highly available web ALB',
            VpcId=vpc_id,
            TagSpecifications=[
                {
                    'ResourceType': 'security-group',
                    'Tags': [
                        {'Key': 'Name', 'Value': 'ha-web-alb-sg'},
                        {'Key': 'Purpose', 'Value': 'HighlyAvailableWeb'}
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
                    'IpRanges': [{'CidrIp': '0.0.0.0/0', 'Description': 'HTTP from anywhere'}]
                },
                {
                    'IpProtocol': 'tcp',
                    'FromPort': 443,
                    'ToPort': 443,
                    'IpRanges': [{'CidrIp': '0.0.0.0/0', 'Description': 'HTTPS from anywhere'}]
                }
            ]
        )
        
        for lb_config in lb_configs:
            try:
                # Create Application Load Balancer
                alb_response = self.elbv2.create_load_balancer(
                    Name=lb_config['name'],
                    Subnets=[subnet['subnet_id'] for subnet in subnets['public']],
                    SecurityGroups=[sg_id],
                    Scheme='internet-facing',
                    Type='application',
                    IpAddressType='ipv4',
                    Tags=[
                        {'Key': 'Name', 'Value': lb_config['name']},
                        {'Key': 'Purpose', 'Value': 'HighlyAvailableWeb'}
                    ]
                )
                
                alb_arn = alb_response['LoadBalancers'][0]['LoadBalancerArn']
                alb_dns = alb_response['LoadBalancers'][0]['DNSName']
                
                # Create target group
                tg_response = self.elbv2.create_target_group(
                    Name=f"{lb_config['name']}-tg",
                    Protocol='HTTP',
                    Port=80,
                    VpcId=vpc_id,
                    HealthCheckProtocol='HTTP',
                    HealthCheckPath=lb_config.get('health_check_path', '/health'),
                    HealthCheckIntervalSeconds=30,
                    HealthCheckTimeoutSeconds=5,
                    HealthyThresholdCount=3,
                    UnhealthyThresholdCount=3,
                    Tags=[
                        {'Key': 'Name', 'Value': f"{lb_config['name']}-tg"},
                        {'Key': 'Purpose', 'Value': 'HighlyAvailableWeb'}
                    ]
                )
                
                tg_arn = tg_response['TargetGroups'][0]['TargetGroupArn']
                
                # Create listener
                listener_response = self.elbv2.create_listener(
                    LoadBalancerArn=alb_arn,
                    Protocol='HTTP',
                    Port=80,
                    DefaultActions=[
                        {
                            'Type': 'forward',
                            'TargetGroupArn': tg_arn
                        }
                    ]
                )
                
                # Enable cross-zone load balancing
                self.elbv2.modify_load_balancer_attributes(
                    LoadBalancerArn=alb_arn,
                    Attributes=[
                        {
                            'Key': 'load_balancing.cross_zone.enabled',
                            'Value': 'true'
                        },
                        {
                            'Key': 'deletion_protection.enabled',
                            'Value': 'true'
                        }
                    ]
                )
                
                load_balancers.append({
                    'name': lb_config['name'],
                    'arn': alb_arn,
                    'dns_name': alb_dns,
                    'target_group_arn': tg_arn,
                    'listener_arn': listener_response['Listeners'][0]['ListenerArn'],
                    'security_group_id': sg_id,
                    'status': 'created'
                })
                
            except Exception as e:
                logging.error(f"Error creating load balancer {lb_config['name']}: {str(e)}")
                load_balancers.append({
                    'name': lb_config['name'],
                    'status': 'failed',
                    'error': str(e)
                })
        
        return {
            'load_balancers': load_balancers,
            'security_group_id': sg_id,
            'status': 'completed'
        }
    
    def configure_dns_with_health_checks(self, dns_config: Dict, lb_result: Dict) -> Dict:
        """Configure Route 53 DNS with health checks and failover"""
        try:
            domain_name = dns_config.get('domain_name')
            if not domain_name:
                return {'status': 'skipped', 'reason': 'no_domain_configured'}
            
            # Get hosted zone
            hosted_zones = self.route53.list_hosted_zones_by_name(DNSName=domain_name)
            if not hosted_zones['HostedZones']:
                raise ValueError(f"No hosted zone found for domain {domain_name}")
            
            hosted_zone_id = hosted_zones['HostedZones'][0]['Id']
            
            # Create health checks for each load balancer
            health_checks = []
            for lb in lb_result['load_balancers']:
                if lb['status'] == 'created':
                    hc_response = self.route53.create_health_check(
                        Type='HTTPS_STR_MATCH',
                        ResourcePath=dns_config.get('health_check_path', '/health'),
                        FullyQualifiedDomainName=lb['dns_name'],
                        Port=443,
                        RequestInterval=30,
                        FailureThreshold=3,
                        SearchString=dns_config.get('health_check_string', 'OK'),
                        Tags=[
                            {'Key': 'Name', 'Value': f"health-check-{lb['name']}"},
                            {'Key': 'Purpose', 'Value': 'HighlyAvailableWeb'}
                        ]
                    )
                    
                    health_checks.append({
                        'health_check_id': hc_response['HealthCheck']['Id'],
                        'load_balancer': lb['name'],
                        'dns_name': lb['dns_name']
                    })
            
            # Create DNS records with failover routing
            dns_records = []
            for i, (lb, hc) in enumerate(zip(lb_result['load_balancers'], health_checks)):
                if lb['status'] == 'created':
                    # Primary record
                    record_response = self.route53.change_resource_record_sets(
                        HostedZoneId=hosted_zone_id,
                        ChangeBatch={
                            'Changes': [
                                {
                                    'Action': 'CREATE',
                                    'ResourceRecordSet': {
                                        'Name': domain_name,
                                        'Type': 'A',
                                        'SetIdentifier': f"primary-{i}",
                                        'Failover': 'PRIMARY' if i == 0 else 'SECONDARY',
                                        'TTL': 60,
                                        'ResourceRecords': [
                                            {'Value': lb['dns_name']}
                                        ],
                                        'HealthCheckId': hc['health_check_id']
                                    }
                                }
                            ]
                        }
                    )
                    
                    dns_records.append({
                        'name': domain_name,
                        'type': 'A',
                        'value': lb['dns_name'],
                        'failover': 'PRIMARY' if i == 0 else 'SECONDARY',
                        'health_check_id': hc['health_check_id'],
                        'change_id': record_response['ChangeInfo']['Id']
                    })
            
            return {
                'hosted_zone_id': hosted_zone_id,
                'domain_name': domain_name,
                'health_checks': health_checks,
                'dns_records': dns_records,
                'status': 'configured'
            }
            
        except Exception as e:
            logging.error(f"Error configuring DNS: {str(e)}")
            return {'status': 'failed', 'error': str(e)}

# Usage example
def main():
    config = {
        'region': 'us-east-1',
        'environment': 'production'
    }
    
    architecture = HighlyAvailableWebArchitecture(config)
    
    # Define architecture configuration
    architecture_config = {
        'vpc_config': {
            'name': 'ha-web-vpc',
            'cidr_block': '10.0.0.0/16'
        },
        'load_balancer_configs': [
            {
                'name': 'primary-alb',
                'health_check_path': '/health'
            }
        ],
        'dns_config': {
            'domain_name': 'example.com',
            'health_check_path': '/health',
            'health_check_string': 'OK'
        },
        'cloudfront_config': {
            'price_class': 'PriceClass_All',
            'cache_behaviors': []
        },
        'security_config': {
            'enable_waf': True,
            'enable_shield_advanced': True
        }
    }
    
    # Deploy highly available architecture
    result = architecture.deploy_highly_available_architecture(architecture_config)
    
    print(f"Deployment Status: {result['status']}")
    if result['status'] == 'completed':
        print("Highly available web architecture deployed successfully!")
        for component, details in result['components'].items():
            print(f"- {component}: {details.get('status', 'unknown')}")
    else:
        print(f"Deployment failed: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    main()
```
### Example 2: Global Multi-Region Traffic Management System

```python
import boto3
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import time
import concurrent.futures

@dataclass
class RegionEndpoint:
    region: str
    load_balancer_dns: str
    health_check_id: str
    priority: int
    weight: int
    status: str

@dataclass
class TrafficPolicy:
    policy_type: str  # failover, weighted, latency, geolocation
    primary_region: str
    secondary_regions: List[str]
    health_check_interval: int = 30
    failure_threshold: int = 3

class GlobalTrafficManager:
    def __init__(self, config: Dict):
        self.config = config
        self.route53 = boto3.client('route53')
        self.cloudfront = boto3.client('cloudfront')
        self.cloudwatch = boto3.client('cloudwatch')
        self.sns = boto3.client('sns')
        
        # Regional clients for multi-region operations
        self.regional_clients = {}
        
    def deploy_global_traffic_management(self, traffic_config: Dict) -> Dict:
        """Deploy global traffic management across multiple regions"""
        deployment_id = f"global_traffic_{int(datetime.utcnow().timestamp())}"
        
        deployment_result = {
            'deployment_id': deployment_id,
            'timestamp': datetime.utcnow().isoformat(),
            'traffic_config': traffic_config,
            'regional_endpoints': {},
            'global_components': {},
            'status': 'initiated'
        }
        
        try:
            # 1. Set up regional endpoints
            regional_result = self.setup_regional_endpoints(
                traffic_config.get('regions', [])
            )
            deployment_result['regional_endpoints'] = regional_result
            
            # 2. Configure global DNS with traffic policies
            dns_result = self.configure_global_dns_policies(
                traffic_config.get('dns_config', {}),
                regional_result
            )
            deployment_result['global_components']['dns'] = dns_result
            
            # 3. Deploy CloudFront with multiple origins
            cloudfront_result = self.deploy_global_cloudfront(
                traffic_config.get('cloudfront_config', {}),
                regional_result
            )
            deployment_result['global_components']['cloudfront'] = cloudfront_result
            
            # 4. Set up global health monitoring
            monitoring_result = self.setup_global_health_monitoring(
                deployment_id, regional_result
            )
            deployment_result['global_components']['monitoring'] = monitoring_result
            
            # 5. Configure automated failover
            failover_result = self.configure_automated_failover(
                traffic_config.get('failover_config', {}),
                regional_result, dns_result
            )
            deployment_result['global_components']['failover'] = failover_result
            
            deployment_result['status'] = 'completed'
            
        except Exception as e:
            logging.error(f"Error deploying global traffic management: {str(e)}")
            deployment_result['status'] = 'failed'
            deployment_result['error'] = str(e)
        
        return deployment_result
    
    def setup_regional_endpoints(self, regions_config: List[Dict]) -> Dict:
        """Set up load balancers and endpoints in multiple regions"""
        regional_endpoints = {}
        
        # Use ThreadPoolExecutor for parallel regional setup
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_to_region = {
                executor.submit(self.setup_region_endpoint, region_config): region_config['region']
                for region_config in regions_config
            }
            
            for future in concurrent.futures.as_completed(future_to_region):
                region = future_to_region[future]
                try:
                    endpoint_result = future.result()
                    regional_endpoints[region] = endpoint_result
                except Exception as e:
                    logging.error(f"Error setting up region {region}: {str(e)}")
                    regional_endpoints[region] = {
                        'status': 'failed',
                        'error': str(e)
                    }
        
        return regional_endpoints
    
    def setup_region_endpoint(self, region_config: Dict) -> Dict:
        """Set up endpoint infrastructure in a specific region"""
        region = region_config['region']
        
        try:
            # Get regional clients
            elbv2 = self.get_regional_client('elbv2', region)
            route53 = self.route53  # Route53 is global
            
            # Create or get existing load balancer
            lb_result = self.create_regional_load_balancer(
                elbv2, region_config
            )
            
            # Create health check for this region
            health_check_result = self.create_regional_health_check(
                route53, lb_result['dns_name'], region_config
            )
            
            # Set up regional monitoring
            monitoring_result = self.setup_regional_monitoring(
                region, lb_result, health_check_result
            )
            
            return {
                'region': region,
                'load_balancer': lb_result,
                'health_check': health_check_result,
                'monitoring': monitoring_result,
                'status': 'active'
            }
            
        except Exception as e:
            logging.error(f"Error setting up region endpoint {region}: {str(e)}")
            raise
    
    def create_regional_load_balancer(self, elbv2_client, region_config: Dict) -> Dict:
        """Create load balancer in a specific region"""
        region = region_config['region']
        
        try:
            # Get VPC and subnets for the region
            ec2 = self.get_regional_client('ec2', region)
            
            # Get default VPC (in production, use specific VPC)
            vpcs = ec2.describe_vpcs(Filters=[{'Name': 'is-default', 'Values': ['true']}])
            if not vpcs['Vpcs']:
                raise ValueError(f"No default VPC found in region {region}")
            
            vpc_id = vpcs['Vpcs'][0]['VpcId']
            
            # Get subnets across multiple AZs
            subnets = ec2.describe_subnets(
                Filters=[
                    {'Name': 'vpc-id', 'Values': [vpc_id]},
                    {'Name': 'default-for-az', 'Values': ['true']}
                ]
            )
            
            if len(subnets['Subnets']) < 2:
                raise ValueError(f"Need at least 2 subnets in different AZs in region {region}")
            
            subnet_ids = [subnet['SubnetId'] for subnet in subnets['Subnets'][:3]]
            
            # Create security group
            sg_response = ec2.create_security_group(
                GroupName=f'global-alb-sg-{region}-{int(time.time())}',
                Description=f'Security group for global ALB in {region}',
                VpcId=vpc_id
            )
            sg_id = sg_response['GroupId']
            
            # Configure security group rules
            ec2.authorize_security_group_ingress(
                GroupId=sg_id,
                IpPermissions=[
                    {
                        'IpProtocol': 'tcp',
                        'FromPort': 80,
                        'ToPort': 80,
                        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                    },
                    {
                        'IpProtocol': 'tcp',
                        'FromPort': 443,
                        'ToPort': 443,
                        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                    }
                ]
            )
            
            # Create Application Load Balancer
            alb_response = elbv2_client.create_load_balancer(
                Name=f"global-alb-{region}",
                Subnets=subnet_ids,
                SecurityGroups=[sg_id],
                Scheme='internet-facing',
                Type='application',
                IpAddressType='ipv4'
            )
            
            alb_arn = alb_response['LoadBalancers'][0]['LoadBalancerArn']
            alb_dns = alb_response['LoadBalancers'][0]['DNSName']
            
            # Create target group
            tg_response = elbv2_client.create_target_group(
                Name=f"global-tg-{region}",
                Protocol='HTTP',
                Port=80,
                VpcId=vpc_id,
                HealthCheckPath='/health',
                HealthCheckIntervalSeconds=30,
                HealthCheckTimeoutSeconds=5,
                HealthyThresholdCount=2,
                UnhealthyThresholdCount=3
            )
            
            tg_arn = tg_response['TargetGroups'][0]['TargetGroupArn']
            
            # Create listener
            elbv2_client.create_listener(
                LoadBalancerArn=alb_arn,
                Protocol='HTTP',
                Port=80,
                DefaultActions=[
                    {
                        'Type': 'forward',
                        'TargetGroupArn': tg_arn
                    }
                ]
            )
            
            return {
                'arn': alb_arn,
                'dns_name': alb_dns,
                'target_group_arn': tg_arn,
                'security_group_id': sg_id,
                'region': region,
                'status': 'created'
            }
            
        except Exception as e:
            logging.error(f"Error creating load balancer in {region}: {str(e)}")
            raise
    
    def create_regional_health_check(self, route53_client, dns_name: str, 
                                   region_config: Dict) -> Dict:
        """Create Route 53 health check for regional endpoint"""
        try:
            health_check_response = route53_client.create_health_check(
                Type='HTTP',
                ResourcePath=region_config.get('health_check_path', '/health'),
                FullyQualifiedDomainName=dns_name,
                Port=80,
                RequestInterval=30,
                FailureThreshold=3,
                Tags=[
                    {
                        'Key': 'Name',
                        'Value': f"health-check-{region_config['region']}"
                    },
                    {
                        'Key': 'Region',
                        'Value': region_config['region']
                    }
                ]
            )
            
            health_check_id = health_check_response['HealthCheck']['Id']
            
            return {
                'health_check_id': health_check_id,
                'dns_name': dns_name,
                'path': region_config.get('health_check_path', '/health'),
                'status': 'created'
            }
            
        except Exception as e:
            logging.error(f"Error creating health check for {dns_name}: {str(e)}")
            raise
    
    def configure_global_dns_policies(self, dns_config: Dict, 
                                    regional_endpoints: Dict) -> Dict:
        """Configure global DNS with traffic policies"""
        try:
            domain_name = dns_config.get('domain_name')
            if not domain_name:
                return {'status': 'skipped', 'reason': 'no_domain_configured'}
            
            # Get hosted zone
            hosted_zones = self.route53.list_hosted_zones_by_name(DNSName=domain_name)
            if not hosted_zones['HostedZones']:
                raise ValueError(f"No hosted zone found for domain {domain_name}")
            
            hosted_zone_id = hosted_zones['HostedZones'][0]['Id']
            
            # Create traffic policy
            traffic_policy = self.create_traffic_policy(
                dns_config, regional_endpoints
            )
            
            # Create DNS records based on policy type
            dns_records = []
            policy_type = dns_config.get('policy_type', 'failover')
            
            if policy_type == 'failover':
                dns_records = self.create_failover_dns_records(
                    hosted_zone_id, domain_name, regional_endpoints
                )
            elif policy_type == 'weighted':
                dns_records = self.create_weighted_dns_records(
                    hosted_zone_id, domain_name, regional_endpoints, dns_config
                )
            elif policy_type == 'latency':
                dns_records = self.create_latency_dns_records(
                    hosted_zone_id, domain_name, regional_endpoints
                )
            elif policy_type == 'geolocation':
                dns_records = self.create_geolocation_dns_records(
                    hosted_zone_id, domain_name, regional_endpoints, dns_config
                )
            
            return {
                'hosted_zone_id': hosted_zone_id,
                'domain_name': domain_name,
                'traffic_policy': traffic_policy,
                'dns_records': dns_records,
                'policy_type': policy_type,
                'status': 'configured'
            }
            
        except Exception as e:
            logging.error(f"Error configuring global DNS: {str(e)}")
            return {'status': 'failed', 'error': str(e)}
    
    def create_failover_dns_records(self, hosted_zone_id: str, domain_name: str,
                                  regional_endpoints: Dict) -> List[Dict]:
        """Create failover DNS records"""
        dns_records = []
        
        # Sort regions by priority (primary first)
        sorted_regions = sorted(
            regional_endpoints.items(),
            key=lambda x: x[1].get('priority', 100)
        )
        
        for i, (region, endpoint) in enumerate(sorted_regions):
            if endpoint['status'] != 'active':
                continue
            
            failover_type = 'PRIMARY' if i == 0 else 'SECONDARY'
            
            change_response = self.route53.change_resource_record_sets(
                HostedZoneId=hosted_zone_id,
                ChangeBatch={
                    'Changes': [
                        {
                            'Action': 'CREATE',
                            'ResourceRecordSet': {
                                'Name': domain_name,
                                'Type': 'CNAME',
                                'SetIdentifier': f"failover-{region}",
                                'Failover': failover_type,
                                'TTL': 60,
                                'ResourceRecords': [
                                    {'Value': endpoint['load_balancer']['dns_name']}
                                ],
                                'HealthCheckId': endpoint['health_check']['health_check_id']
                            }
                        }
                    ]
                }
            )
            
            dns_records.append({
                'region': region,
                'type': 'CNAME',
                'failover': failover_type,
                'dns_name': endpoint['load_balancer']['dns_name'],
                'health_check_id': endpoint['health_check']['health_check_id'],
                'change_id': change_response['ChangeInfo']['Id']
            })
        
        return dns_records
    
    def create_weighted_dns_records(self, hosted_zone_id: str, domain_name: str,
                                  regional_endpoints: Dict, dns_config: Dict) -> List[Dict]:
        """Create weighted DNS records for traffic distribution"""
        dns_records = []
        weights = dns_config.get('weights', {})
        
        for region, endpoint in regional_endpoints.items():
            if endpoint['status'] != 'active':
                continue
            
            weight = weights.get(region, 100)  # Default weight
            
            change_response = self.route53.change_resource_record_sets(
                HostedZoneId=hosted_zone_id,
                ChangeBatch={
                    'Changes': [
                        {
                            'Action': 'CREATE',
                            'ResourceRecordSet': {
                                'Name': domain_name,
                                'Type': 'CNAME',
                                'SetIdentifier': f"weighted-{region}",
                                'Weight': weight,
                                'TTL': 60,
                                'ResourceRecords': [
                                    {'Value': endpoint['load_balancer']['dns_name']}
                                ],
                                'HealthCheckId': endpoint['health_check']['health_check_id']
                            }
                        }
                    ]
                }
            )
            
            dns_records.append({
                'region': region,
                'type': 'CNAME',
                'weight': weight,
                'dns_name': endpoint['load_balancer']['dns_name'],
                'health_check_id': endpoint['health_check']['health_check_id'],
                'change_id': change_response['ChangeInfo']['Id']
            })
        
        return dns_records
    
    def create_latency_dns_records(self, hosted_zone_id: str, domain_name: str,
                                 regional_endpoints: Dict) -> List[Dict]:
        """Create latency-based DNS records"""
        dns_records = []
        
        for region, endpoint in regional_endpoints.items():
            if endpoint['status'] != 'active':
                continue
            
            change_response = self.route53.change_resource_record_sets(
                HostedZoneId=hosted_zone_id,
                ChangeBatch={
                    'Changes': [
                        {
                            'Action': 'CREATE',
                            'ResourceRecordSet': {
                                'Name': domain_name,
                                'Type': 'CNAME',
                                'SetIdentifier': f"latency-{region}",
                                'Region': region,
                                'TTL': 60,
                                'ResourceRecords': [
                                    {'Value': endpoint['load_balancer']['dns_name']}
                                ],
                                'HealthCheckId': endpoint['health_check']['health_check_id']
                            }
                        }
                    ]
                }
            )
            
            dns_records.append({
                'region': region,
                'type': 'CNAME',
                'routing_policy': 'latency',
                'dns_name': endpoint['load_balancer']['dns_name'],
                'health_check_id': endpoint['health_check']['health_check_id'],
                'change_id': change_response['ChangeInfo']['Id']
            })
        
        return dns_records
    
    def deploy_global_cloudfront(self, cloudfront_config: Dict, 
                               regional_endpoints: Dict) -> Dict:
        """Deploy CloudFront distribution with multiple regional origins"""
        try:
            # Prepare origins from regional endpoints
            origins = []
            origin_groups = []
            
            for i, (region, endpoint) in enumerate(regional_endpoints.items()):
                if endpoint['status'] != 'active':
                    continue
                
                origin_id = f"origin-{region}"
                origins.append({
                    'Id': origin_id,
                    'DomainName': endpoint['load_balancer']['dns_name'],
                    'CustomOriginConfig': {
                        'HTTPPort': 80,
                        'HTTPSPort': 443,
                        'OriginProtocolPolicy': 'http-only',
                        'OriginSslProtocols': {
                            'Quantity': 1,
                            'Items': ['TLSv1.2']
                        }
                    }
                })
            
            if not origins:
                return {'status': 'skipped', 'reason': 'no_active_origins'}
            
            # Create origin group for failover
            if len(origins) > 1:
                origin_groups.append({
                    'Id': 'primary-origin-group',
                    'FailoverCriteria': {
                        'StatusCodes': {
                            'Quantity': 3,
                            'Items': [403, 404, 500]
                        }
                    },
                    'Members': {
                        'Quantity': len(origins),
                        'Items': [
                            {'OriginId': origin['Id'], 'Priority': i}
                            for i, origin in enumerate(origins)
                        ]
                    }
                })
            
            # Create CloudFront distribution
            distribution_config = {
                'CallerReference': f"global-cf-{int(time.time())}",
                'Comment': 'Global highly available distribution',
                'DefaultRootObject': 'index.html',
                'Origins': {
                    'Quantity': len(origins),
                    'Items': origins
                },
                'DefaultCacheBehavior': {
                    'TargetOriginId': origin_groups[0]['Id'] if origin_groups else origins[0]['Id'],
                    'ViewerProtocolPolicy': 'redirect-to-https',
                    'TrustedSigners': {
                        'Enabled': False,
                        'Quantity': 0
                    },
                    'ForwardedValues': {
                        'QueryString': False,
                        'Cookies': {'Forward': 'none'}
                    },
                    'MinTTL': 0,
                    'DefaultTTL': 86400,
                    'MaxTTL': 31536000
                },
                'Enabled': True,
                'PriceClass': cloudfront_config.get('price_class', 'PriceClass_All')
            }
            
            if origin_groups:
                distribution_config['OriginGroups'] = {
                    'Quantity': len(origin_groups),
                    'Items': origin_groups
                }
            
            cf_response = self.cloudfront.create_distribution(
                DistributionConfig=distribution_config
            )
            
            distribution_id = cf_response['Distribution']['Id']
            domain_name = cf_response['Distribution']['DomainName']
            
            return {
                'distribution_id': distribution_id,
                'domain_name': domain_name,
                'origins': origins,
                'origin_groups': origin_groups,
                'status': 'created'
            }
            
        except Exception as e:
            logging.error(f"Error deploying CloudFront: {str(e)}")
            return {'status': 'failed', 'error': str(e)}
    
    def get_regional_client(self, service: str, region: str):
        """Get or create a regional AWS client"""
        client_key = f"{service}#{region}"
        
        if client_key not in self.regional_clients:
            self.regional_clients[client_key] = boto3.client(service, region_name=region)
        
        return self.regional_clients[client_key]

# Usage example
def main():
    config = {
        'primary_region': 'us-east-1'
    }
    
    traffic_manager = GlobalTrafficManager(config)
    
    # Define global traffic configuration
    traffic_config = {
        'regions': [
            {
                'region': 'us-east-1',
                'priority': 1,
                'health_check_path': '/health'
            },
            {
                'region': 'us-west-2',
                'priority': 2,
                'health_check_path': '/health'
            },
            {
                'region': 'eu-west-1',
                'priority': 3,
                'health_check_path': '/health'
            }
        ],
        'dns_config': {
            'domain_name': 'example.com',
            'policy_type': 'failover'
        },
        'cloudfront_config': {
            'price_class': 'PriceClass_All'
        },
        'failover_config': {
            'enable_automated_failover': True,
            'failover_threshold': 3
        }
    }
    
    # Deploy global traffic management
    result = traffic_manager.deploy_global_traffic_management(traffic_config)
    
    print(f"Deployment Status: {result['status']}")
    if result['status'] == 'completed':
        print("Global traffic management deployed successfully!")
        print(f"Regional endpoints: {len(result['regional_endpoints'])}")
        for component, details in result['global_components'].items():
            print(f"- {component}: {details.get('status', 'unknown')}")
    else:
        print(f"Deployment failed: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    main()
```
### Example 3: CloudFormation Template for Highly Available Network Infrastructure

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Highly available network connectivity infrastructure for public endpoints'

Parameters:
  Environment:
    Type: String
    Description: Environment name
    Default: production
    AllowedValues: [development, staging, production]
  
  DomainName:
    Type: String
    Description: Domain name for the application
    Default: example.com
  
  CertificateArn:
    Type: String
    Description: ACM certificate ARN for HTTPS
    Default: ''
  
  EnableCloudFront:
    Type: String
    Description: Enable CloudFront distribution
    Default: 'true'
    AllowedValues: ['true', 'false']
  
  EnableWAF:
    Type: String
    Description: Enable AWS WAF protection
    Default: 'true'
    AllowedValues: ['true', 'false']
  
  HealthCheckPath:
    Type: String
    Description: Health check path for load balancers
    Default: '/health'

Conditions:
  CreateCloudFront: !Equals [!Ref EnableCloudFront, 'true']
  CreateWAF: !Equals [!Ref EnableWAF, 'true']
  HasCertificate: !Not [!Equals [!Ref CertificateArn, '']]

Resources:
  # VPC and Networking Infrastructure
  VPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: 10.0.0.0/16
      EnableDnsHostnames: true
      EnableDnsSupport: true
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-ha-vpc'
        - Key: Environment
          Value: !Ref Environment
        - Key: Purpose
          Value: HighlyAvailableNetwork

  # Internet Gateway
  InternetGateway:
    Type: AWS::EC2::InternetGateway
    Properties:
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-ha-igw'
        - Key: Environment
          Value: !Ref Environment

  InternetGatewayAttachment:
    Type: AWS::EC2::VPCGatewayAttachment
    Properties:
      InternetGatewayId: !Ref InternetGateway
      VpcId: !Ref VPC

  # Public Subnets across multiple AZs
  PublicSubnet1:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      AvailabilityZone: !Select [0, !GetAZs '']
      CidrBlock: 10.0.1.0/24
      MapPublicIpOnLaunch: true
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-public-subnet-1'
        - Key: Environment
          Value: !Ref Environment
        - Key: Type
          Value: Public

  PublicSubnet2:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      AvailabilityZone: !Select [1, !GetAZs '']
      CidrBlock: 10.0.2.0/24
      MapPublicIpOnLaunch: true
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-public-subnet-2'
        - Key: Environment
          Value: !Ref Environment
        - Key: Type
          Value: Public

  PublicSubnet3:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      AvailabilityZone: !Select [2, !GetAZs '']
      CidrBlock: 10.0.3.0/24
      MapPublicIpOnLaunch: true
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-public-subnet-3'
        - Key: Environment
          Value: !Ref Environment
        - Key: Type
          Value: Public

  # Private Subnets
  PrivateSubnet1:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      AvailabilityZone: !Select [0, !GetAZs '']
      CidrBlock: 10.0.11.0/24
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-private-subnet-1'
        - Key: Environment
          Value: !Ref Environment
        - Key: Type
          Value: Private

  PrivateSubnet2:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      AvailabilityZone: !Select [1, !GetAZs '']
      CidrBlock: 10.0.12.0/24
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-private-subnet-2'
        - Key: Environment
          Value: !Ref Environment
        - Key: Type
          Value: Private

  PrivateSubnet3:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      AvailabilityZone: !Select [2, !GetAZs '']
      CidrBlock: 10.0.13.0/24
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-private-subnet-3'
        - Key: Environment
          Value: !Ref Environment
        - Key: Type
          Value: Private

  # NAT Gateways for high availability
  NatGateway1EIP:
    Type: AWS::EC2::EIP
    DependsOn: InternetGatewayAttachment
    Properties:
      Domain: vpc
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-nat-eip-1'

  NatGateway2EIP:
    Type: AWS::EC2::EIP
    DependsOn: InternetGatewayAttachment
    Properties:
      Domain: vpc
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-nat-eip-2'

  NatGateway3EIP:
    Type: AWS::EC2::EIP
    DependsOn: InternetGatewayAttachment
    Properties:
      Domain: vpc
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-nat-eip-3'

  NatGateway1:
    Type: AWS::EC2::NatGateway
    Properties:
      AllocationId: !GetAtt NatGateway1EIP.AllocationId
      SubnetId: !Ref PublicSubnet1
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-nat-gateway-1'

  NatGateway2:
    Type: AWS::EC2::NatGateway
    Properties:
      AllocationId: !GetAtt NatGateway2EIP.AllocationId
      SubnetId: !Ref PublicSubnet2
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-nat-gateway-2'

  NatGateway3:
    Type: AWS::EC2::NatGateway
    Properties:
      AllocationId: !GetAtt NatGateway3EIP.AllocationId
      SubnetId: !Ref PublicSubnet3
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-nat-gateway-3'

  # Route Tables
  PublicRouteTable:
    Type: AWS::EC2::RouteTable
    Properties:
      VpcId: !Ref VPC
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-public-routes'
        - Key: Environment
          Value: !Ref Environment

  DefaultPublicRoute:
    Type: AWS::EC2::Route
    DependsOn: InternetGatewayAttachment
    Properties:
      RouteTableId: !Ref PublicRouteTable
      DestinationCidrBlock: 0.0.0.0/0
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

  PublicSubnet3RouteTableAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      RouteTableId: !Ref PublicRouteTable
      SubnetId: !Ref PublicSubnet3

  # Private Route Tables (one per AZ for high availability)
  PrivateRouteTable1:
    Type: AWS::EC2::RouteTable
    Properties:
      VpcId: !Ref VPC
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-private-routes-1'

  DefaultPrivateRoute1:
    Type: AWS::EC2::Route
    Properties:
      RouteTableId: !Ref PrivateRouteTable1
      DestinationCidrBlock: 0.0.0.0/0
      NatGatewayId: !Ref NatGateway1

  PrivateSubnet1RouteTableAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      RouteTableId: !Ref PrivateRouteTable1
      SubnetId: !Ref PrivateSubnet1

  PrivateRouteTable2:
    Type: AWS::EC2::RouteTable
    Properties:
      VpcId: !Ref VPC
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-private-routes-2'

  DefaultPrivateRoute2:
    Type: AWS::EC2::Route
    Properties:
      RouteTableId: !Ref PrivateRouteTable2
      DestinationCidrBlock: 0.0.0.0/0
      NatGatewayId: !Ref NatGateway2

  PrivateSubnet2RouteTableAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      RouteTableId: !Ref PrivateRouteTable2
      SubnetId: !Ref PrivateSubnet2

  PrivateRouteTable3:
    Type: AWS::EC2::RouteTable
    Properties:
      VpcId: !Ref VPC
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-private-routes-3'

  DefaultPrivateRoute3:
    Type: AWS::EC2::Route
    Properties:
      RouteTableId: !Ref PrivateRouteTable3
      DestinationCidrBlock: 0.0.0.0/0
      NatGatewayId: !Ref NatGateway3

  PrivateSubnet3RouteTableAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      RouteTableId: !Ref PrivateRouteTable3
      SubnetId: !Ref PrivateSubnet3

  # Security Groups
  ALBSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupName: !Sub '${Environment}-alb-sg'
      GroupDescription: Security group for Application Load Balancer
      VpcId: !Ref VPC
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: 0.0.0.0/0
          Description: HTTP from anywhere
        - IpProtocol: tcp
          FromPort: 443
          ToPort: 443
          CidrIp: 0.0.0.0/0
          Description: HTTPS from anywhere
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-alb-sg'
        - Key: Environment
          Value: !Ref Environment

  WebServerSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupName: !Sub '${Environment}-web-sg'
      GroupDescription: Security group for web servers
      VpcId: !Ref VPC
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          SourceSecurityGroupId: !Ref ALBSecurityGroup
          Description: HTTP from ALB
        - IpProtocol: tcp
          FromPort: 443
          ToPort: 443
          SourceSecurityGroupId: !Ref ALBSecurityGroup
          Description: HTTPS from ALB
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-web-sg'
        - Key: Environment
          Value: !Ref Environment

  # Application Load Balancer
  ApplicationLoadBalancer:
    Type: AWS::ElasticLoadBalancingV2::LoadBalancer
    Properties:
      Name: !Sub '${Environment}-ha-alb'
      Scheme: internet-facing
      Type: application
      IpAddressType: ipv4
      Subnets:
        - !Ref PublicSubnet1
        - !Ref PublicSubnet2
        - !Ref PublicSubnet3
      SecurityGroups:
        - !Ref ALBSecurityGroup
      LoadBalancerAttributes:
        - Key: idle_timeout.timeout_seconds
          Value: '60'
        - Key: routing.http2.enabled
          Value: 'true'
        - Key: access_logs.s3.enabled
          Value: 'false'
        - Key: deletion_protection.enabled
          Value: 'true'
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-ha-alb'
        - Key: Environment
          Value: !Ref Environment

  # Target Group
  ALBTargetGroup:
    Type: AWS::ElasticLoadBalancingV2::TargetGroup
    Properties:
      Name: !Sub '${Environment}-ha-tg'
      Port: 80
      Protocol: HTTP
      VpcId: !Ref VPC
      HealthCheckEnabled: true
      HealthCheckIntervalSeconds: 30
      HealthCheckPath: !Ref HealthCheckPath
      HealthCheckProtocol: HTTP
      HealthCheckTimeoutSeconds: 5
      HealthyThresholdCount: 2
      UnhealthyThresholdCount: 3
      TargetType: instance
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-ha-tg'
        - Key: Environment
          Value: !Ref Environment

  # HTTP Listener
  ALBListenerHTTP:
    Type: AWS::ElasticLoadBalancingV2::Listener
    Properties:
      DefaultActions:
        - Type: redirect
          RedirectConfig:
            Protocol: HTTPS
            Port: 443
            StatusCode: HTTP_301
      LoadBalancerArn: !Ref ApplicationLoadBalancer
      Port: 80
      Protocol: HTTP

  # HTTPS Listener (conditional)
  ALBListenerHTTPS:
    Type: AWS::ElasticLoadBalancingV2::Listener
    Condition: HasCertificate
    Properties:
      DefaultActions:
        - Type: forward
          TargetGroupArn: !Ref ALBTargetGroup
      LoadBalancerArn: !Ref ApplicationLoadBalancer
      Port: 443
      Protocol: HTTPS
      Certificates:
        - CertificateArn: !Ref CertificateArn
      SslPolicy: ELBSecurityPolicy-TLS-1-2-2017-01

  # Route 53 Health Check
  Route53HealthCheck:
    Type: AWS::Route53::HealthCheck
    Properties:
      Type: HTTPS
      ResourcePath: !Ref HealthCheckPath
      FullyQualifiedDomainName: !GetAtt ApplicationLoadBalancer.DNSName
      Port: 443
      RequestInterval: 30
      FailureThreshold: 3
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-alb-health-check'
        - Key: Environment
          Value: !Ref Environment

  # WAF Web ACL (conditional)
  WebACL:
    Type: AWS::WAFv2::WebACL
    Condition: CreateWAF
    Properties:
      Name: !Sub '${Environment}-web-acl'
      Scope: REGIONAL
      DefaultAction:
        Allow: {}
      Rules:
        - Name: AWSManagedRulesCommonRuleSet
          Priority: 1
          OverrideAction:
            None: {}
          Statement:
            ManagedRuleGroupStatement:
              VendorName: AWS
              Name: AWSManagedRulesCommonRuleSet
          VisibilityConfig:
            SampledRequestsEnabled: true
            CloudWatchMetricsEnabled: true
            MetricName: CommonRuleSetMetric
        - Name: AWSManagedRulesKnownBadInputsRuleSet
          Priority: 2
          OverrideAction:
            None: {}
          Statement:
            ManagedRuleGroupStatement:
              VendorName: AWS
              Name: AWSManagedRulesKnownBadInputsRuleSet
          VisibilityConfig:
            SampledRequestsEnabled: true
            CloudWatchMetricsEnabled: true
            MetricName: KnownBadInputsRuleSetMetric
      VisibilityConfig:
        SampledRequestsEnabled: true
        CloudWatchMetricsEnabled: true
        MetricName: !Sub '${Environment}WebACL'
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-web-acl'
        - Key: Environment
          Value: !Ref Environment

  # Associate WAF with ALB
  WebACLAssociation:
    Type: AWS::WAFv2::WebACLAssociation
    Condition: CreateWAF
    Properties:
      ResourceArn: !Ref ApplicationLoadBalancer
      WebACLArn: !GetAtt WebACL.Arn

  # CloudFront Distribution (conditional)
  CloudFrontDistribution:
    Type: AWS::CloudFront::Distribution
    Condition: CreateCloudFront
    Properties:
      DistributionConfig:
        Comment: !Sub 'CloudFront distribution for ${Environment}'
        DefaultCacheBehavior:
          TargetOriginId: ALBOrigin
          ViewerProtocolPolicy: redirect-to-https
          AllowedMethods:
            - GET
            - HEAD
            - OPTIONS
            - PUT
            - POST
            - PATCH
            - DELETE
          CachedMethods:
            - GET
            - HEAD
          Compress: true
          ForwardedValues:
            QueryString: true
            Headers:
              - Host
              - CloudFront-Forwarded-Proto
            Cookies:
              Forward: none
          TrustedSigners:
            - self
        Enabled: true
        HttpVersion: http2
        Origins:
          - Id: ALBOrigin
            DomainName: !GetAtt ApplicationLoadBalancer.DNSName
            CustomOriginConfig:
              HTTPPort: 80
              HTTPSPort: 443
              OriginProtocolPolicy: https-only
              OriginSSLProtocols:
                - TLSv1.2
        PriceClass: PriceClass_All
        ViewerCertificate:
          CloudFrontDefaultCertificate: true
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-cloudfront'
        - Key: Environment
          Value: !Ref Environment

  # CloudWatch Alarms
  ALBTargetResponseTimeAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: !Sub '${Environment}-alb-high-response-time'
      AlarmDescription: ALB target response time is too high
      MetricName: TargetResponseTime
      Namespace: AWS/ApplicationELB
      Statistic: Average
      Period: 300
      EvaluationPeriods: 2
      Threshold: 1
      ComparisonOperator: GreaterThanThreshold
      Dimensions:
        - Name: LoadBalancer
          Value: !GetAtt ApplicationLoadBalancer.LoadBalancerFullName
      TreatMissingData: notBreaching

  ALBUnhealthyHostCountAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: !Sub '${Environment}-alb-unhealthy-hosts'
      AlarmDescription: ALB has unhealthy targets
      MetricName: UnHealthyHostCount
      Namespace: AWS/ApplicationELB
      Statistic: Average
      Period: 300
      EvaluationPeriods: 2
      Threshold: 0
      ComparisonOperator: GreaterThanThreshold
      Dimensions:
        - Name: TargetGroup
          Value: !GetAtt ALBTargetGroup.TargetGroupFullName
      TreatMissingData: notBreaching

  ALB5XXErrorAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: !Sub '${Environment}-alb-5xx-errors'
      AlarmDescription: ALB is generating 5XX errors
      MetricName: HTTPCode_ELB_5XX_Count
      Namespace: AWS/ApplicationELB
      Statistic: Sum
      Period: 300
      EvaluationPeriods: 2
      Threshold: 10
      ComparisonOperator: GreaterThanThreshold
      Dimensions:
        - Name: LoadBalancer
          Value: !GetAtt ApplicationLoadBalancer.LoadBalancerFullName
      TreatMissingData: notBreaching

  # VPC Flow Logs
  VPCFlowLogRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: vpc-flow-logs.amazonaws.com
            Action: sts:AssumeRole
      Policies:
        - PolicyName: flowlogsDeliveryRolePolicy
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - logs:CreateLogGroup
                  - logs:CreateLogStream
                  - logs:PutLogEvents
                  - logs:DescribeLogGroups
                  - logs:DescribeLogStreams
                Resource: '*'

  VPCFlowLogGroup:
    Type: AWS::Logs::LogGroup
    Properties:
      LogGroupName: !Sub '/aws/vpc/flowlogs/${Environment}'
      RetentionInDays: 14

  VPCFlowLog:
    Type: AWS::EC2::FlowLog
    Properties:
      ResourceType: VPC
      ResourceId: !Ref VPC
      TrafficType: ALL
      LogDestinationType: cloud-watch-logs
      LogGroupName: !Ref VPCFlowLogGroup
      DeliverLogsPermissionArn: !GetAtt VPCFlowLogRole.Arn
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-vpc-flow-logs'
        - Key: Environment
          Value: !Ref Environment

Outputs:
  VPCId:
    Description: VPC ID
    Value: !Ref VPC
    Export:
      Name: !Sub '${Environment}-vpc-id'

  PublicSubnets:
    Description: Public subnet IDs
    Value: !Join
      - ','
      - - !Ref PublicSubnet1
        - !Ref PublicSubnet2
        - !Ref PublicSubnet3
    Export:
      Name: !Sub '${Environment}-public-subnets'

  PrivateSubnets:
    Description: Private subnet IDs
    Value: !Join
      - ','
      - - !Ref PrivateSubnet1
        - !Ref PrivateSubnet2
        - !Ref PrivateSubnet3
    Export:
      Name: !Sub '${Environment}-private-subnets'

  ApplicationLoadBalancerArn:
    Description: Application Load Balancer ARN
    Value: !Ref ApplicationLoadBalancer
    Export:
      Name: !Sub '${Environment}-alb-arn'

  ApplicationLoadBalancerDNS:
    Description: Application Load Balancer DNS name
    Value: !GetAtt ApplicationLoadBalancer.DNSName
    Export:
      Name: !Sub '${Environment}-alb-dns'

  TargetGroupArn:
    Description: Target Group ARN
    Value: !Ref ALBTargetGroup
    Export:
      Name: !Sub '${Environment}-target-group-arn'

  WebServerSecurityGroupId:
    Description: Web server security group ID
    Value: !Ref WebServerSecurityGroup
    Export:
      Name: !Sub '${Environment}-web-sg-id'

  Route53HealthCheckId:
    Description: Route 53 health check ID
    Value: !Ref Route53HealthCheck
    Export:
      Name: !Sub '${Environment}-health-check-id'

  CloudFrontDistributionId:
    Condition: CreateCloudFront
    Description: CloudFront distribution ID
    Value: !Ref CloudFrontDistribution
    Export:
      Name: !Sub '${Environment}-cloudfront-id'

  CloudFrontDomainName:
    Condition: CreateCloudFront
    Description: CloudFront distribution domain name
    Value: !GetAtt CloudFrontDistribution.DomainName
    Export:
      Name: !Sub '${Environment}-cloudfront-domain'

  WebACLArn:
    Condition: CreateWAF
    Description: WAF Web ACL ARN
    Value: !GetAtt WebACL.Arn
    Export:
      Name: !Sub '${Environment}-web-acl-arn'
```
### Example 4: Network Health Monitoring and Automated Failover System

```bash
#!/bin/bash

# Network Health Monitoring and Automated Failover System
# Monitors network connectivity and automatically triggers failover procedures

set -euo pipefail

# Configuration
CONFIG_FILE="${CONFIG_FILE:-./network-monitoring-config.json}"
LOG_FILE="${LOG_FILE:-./network-monitoring.log}"
RESULTS_DIR="${RESULTS_DIR:-./network-monitoring-results}"
TEMP_DIR="${TEMP_DIR:-/tmp/network-monitoring}"

# Create directories
mkdir -p "$RESULTS_DIR" "$TEMP_DIR"

# Logging function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

# Load configuration
if [[ ! -f "$CONFIG_FILE" ]]; then
    log "ERROR: Configuration file $CONFIG_FILE not found"
    exit 1
fi

# Parse configuration
ENDPOINTS=($(jq -r '.endpoints[].url' "$CONFIG_FILE"))
HEALTH_CHECK_INTERVAL=$(jq -r '.health_check_interval // 30' "$CONFIG_FILE")
FAILURE_THRESHOLD=$(jq -r '.failure_threshold // 3' "$CONFIG_FILE")
RECOVERY_THRESHOLD=$(jq -r '.recovery_threshold // 2' "$CONFIG_FILE")
NOTIFICATION_TOPIC=$(jq -r '.notification_topic // ""' "$CONFIG_FILE")

log "Starting network health monitoring"
log "Endpoints: ${#ENDPOINTS[@]}"
log "Health check interval: ${HEALTH_CHECK_INTERVAL}s"
log "Failure threshold: $FAILURE_THRESHOLD"

# Function to check endpoint health
check_endpoint_health() {
    local endpoint="$1"
    local timeout="${2:-10}"
    local expected_status="${3:-200}"
    
    local start_time=$(date +%s.%N)
    local response_code
    local response_time
    local health_status="healthy"
    local error_message=""
    
    # Perform HTTP health check
    if response_code=$(curl -s -o /dev/null -w "%{http_code}" \
        --max-time "$timeout" \
        --connect-timeout 5 \
        --retry 0 \
        "$endpoint" 2>/dev/null); then
        
        local end_time=$(date +%s.%N)
        response_time=$(echo "$end_time - $start_time" | bc -l)
        
        if [[ "$response_code" != "$expected_status" ]]; then
            health_status="unhealthy"
            error_message="HTTP $response_code (expected $expected_status)"
        fi
    else
        local end_time=$(date +%s.%N)
        response_time=$(echo "$end_time - $start_time" | bc -l)
        health_status="unhealthy"
        error_message="Connection failed or timeout"
        response_code="000"
    fi
    
    # Create health check result
    cat << EOF
{
    "endpoint": "$endpoint",
    "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "health_status": "$health_status",
    "response_code": "$response_code",
    "response_time": $response_time,
    "error_message": "$error_message"
}
EOF
}

# Function to perform comprehensive endpoint monitoring
monitor_endpoint() {
    local endpoint="$1"
    local endpoint_config=$(jq -r --arg url "$endpoint" '.endpoints[] | select(.url == $url)' "$CONFIG_FILE")
    
    local timeout=$(echo "$endpoint_config" | jq -r '.timeout // 10')
    local expected_status=$(echo "$endpoint_config" | jq -r '.expected_status // 200')
    local health_check_path=$(echo "$endpoint_config" | jq -r '.health_check_path // ""')
    
    # Construct full health check URL
    local health_check_url="$endpoint"
    if [[ -n "$health_check_path" ]]; then
        health_check_url="${endpoint}${health_check_path}"
    fi
    
    log "Monitoring endpoint: $health_check_url"
    
    # Perform basic health check
    local basic_result=$(check_endpoint_health "$health_check_url" "$timeout" "$expected_status")
    
    # Perform additional checks
    local dns_result=$(check_dns_resolution "$endpoint")
    local ssl_result=$(check_ssl_certificate "$endpoint")
    local connectivity_result=$(check_network_connectivity "$endpoint")
    
    # Combine results
    local comprehensive_result=$(jq -n \
        --argjson basic "$basic_result" \
        --argjson dns "$dns_result" \
        --argjson ssl "$ssl_result" \
        --argjson connectivity "$connectivity_result" \
        '{
            endpoint: $basic.endpoint,
            timestamp: $basic.timestamp,
            health_checks: {
                basic: $basic,
                dns: $dns,
                ssl: $ssl,
                connectivity: $connectivity
            },
            overall_status: (
                if ($basic.health_status == "healthy" and 
                    $dns.status == "healthy" and 
                    $ssl.status == "healthy" and 
                    $connectivity.status == "healthy")
                then "healthy"
                else "unhealthy"
                end
            )
        }')
    
    echo "$comprehensive_result"
}

# Function to check DNS resolution
check_dns_resolution() {
    local endpoint="$1"
    local hostname=$(echo "$endpoint" | sed 's|https\?://||' | cut -d'/' -f1 | cut -d':' -f1)
    
    local start_time=$(date +%s.%N)
    local status="healthy"
    local error_message=""
    local resolved_ips=()
    
    if resolved_ips=($(dig +short "$hostname" A 2>/dev/null)); then
        if [[ ${#resolved_ips[@]} -eq 0 ]]; then
            status="unhealthy"
            error_message="No A records found"
        fi
    else
        status="unhealthy"
        error_message="DNS resolution failed"
    fi
    
    local end_time=$(date +%s.%N)
    local resolution_time=$(echo "$end_time - $start_time" | bc -l)
    
    cat << EOF
{
    "hostname": "$hostname",
    "status": "$status",
    "resolved_ips": $(printf '%s\n' "${resolved_ips[@]}" | jq -R . | jq -s .),
    "resolution_time": $resolution_time,
    "error_message": "$error_message"
}
EOF
}

# Function to check SSL certificate
check_ssl_certificate() {
    local endpoint="$1"
    
    # Skip if not HTTPS
    if [[ ! "$endpoint" =~ ^https:// ]]; then
        cat << EOF
{
    "status": "skipped",
    "reason": "not_https"
}
EOF
        return
    fi
    
    local hostname=$(echo "$endpoint" | sed 's|https://||' | cut -d'/' -f1 | cut -d':' -f1)
    local port=$(echo "$endpoint" | sed 's|https://||' | cut -d'/' -f1 | cut -d':' -f2)
    
    # Default to 443 if no port specified
    if [[ "$port" == "$hostname" ]]; then
        port=443
    fi
    
    local status="healthy"
    local error_message=""
    local cert_info=""
    
    # Check SSL certificate
    if cert_info=$(echo | timeout 10 openssl s_client -connect "$hostname:$port" -servername "$hostname" 2>/dev/null | openssl x509 -noout -dates 2>/dev/null); then
        # Parse certificate dates
        local not_after=$(echo "$cert_info" | grep "notAfter" | cut -d'=' -f2)
        local expiry_timestamp=$(date -d "$not_after" +%s 2>/dev/null || echo "0")
        local current_timestamp=$(date +%s)
        local days_until_expiry=$(( (expiry_timestamp - current_timestamp) / 86400 ))
        
        if [[ $days_until_expiry -lt 30 ]]; then
            status="warning"
            error_message="Certificate expires in $days_until_expiry days"
        elif [[ $days_until_expiry -lt 0 ]]; then
            status="unhealthy"
            error_message="Certificate has expired"
        fi
    else
        status="unhealthy"
        error_message="SSL certificate check failed"
    fi
    
    cat << EOF
{
    "hostname": "$hostname",
    "port": $port,
    "status": "$status",
    "error_message": "$error_message",
    "certificate_info": "$cert_info"
}
EOF
}

# Function to check network connectivity
check_network_connectivity() {
    local endpoint="$1"
    local hostname=$(echo "$endpoint" | sed 's|https\?://||' | cut -d'/' -f1 | cut -d':' -f1)
    
    local status="healthy"
    local error_message=""
    local ping_result=""
    local traceroute_result=""
    
    # Ping test
    if ping_result=$(ping -c 3 -W 5 "$hostname" 2>&1); then
        local avg_time=$(echo "$ping_result" | grep "avg" | cut -d'/' -f5 2>/dev/null || echo "0")
        if (( $(echo "$avg_time > 1000" | bc -l 2>/dev/null || echo 0) )); then
            status="warning"
            error_message="High latency: ${avg_time}ms"
        fi
    else
        status="unhealthy"
        error_message="Ping failed"
    fi
    
    # Traceroute test (simplified)
    if command -v traceroute >/dev/null 2>&1; then
        traceroute_result=$(timeout 30 traceroute -m 10 "$hostname" 2>/dev/null | tail -5 || echo "Traceroute failed")
    fi
    
    cat << EOF
{
    "hostname": "$hostname",
    "status": "$status",
    "error_message": "$error_message",
    "ping_result": "$ping_result",
    "traceroute_result": "$traceroute_result"
}
EOF
}

# Function to update endpoint status
update_endpoint_status() {
    local endpoint="$1"
    local current_status="$2"
    local status_file="$TEMP_DIR/$(echo "$endpoint" | sed 's|[^a-zA-Z0-9]|_|g').status"
    
    # Initialize status file if it doesn't exist
    if [[ ! -f "$status_file" ]]; then
        cat > "$status_file" << EOF
{
    "endpoint": "$endpoint",
    "current_status": "healthy",
    "consecutive_failures": 0,
    "consecutive_successes": 0,
    "last_failure": null,
    "last_success": null,
    "failover_active": false
}
EOF
    fi
    
    # Read current status
    local status_data=$(cat "$status_file")
    local previous_status=$(echo "$status_data" | jq -r '.current_status')
    local consecutive_failures=$(echo "$status_data" | jq -r '.consecutive_failures')
    local consecutive_successes=$(echo "$status_data" | jq -r '.consecutive_successes')
    local failover_active=$(echo "$status_data" | jq -r '.failover_active')
    
    # Update counters
    if [[ "$current_status" == "healthy" ]]; then
        consecutive_successes=$((consecutive_successes + 1))
        consecutive_failures=0
        last_success=$(date -u +%Y-%m-%dT%H:%M:%SZ)
        last_failure=$(echo "$status_data" | jq -r '.last_failure')
    else
        consecutive_failures=$((consecutive_failures + 1))
        consecutive_successes=0
        last_failure=$(date -u +%Y-%m-%dT%H:%M:%SZ)
        last_success=$(echo "$status_data" | jq -r '.last_success')
    fi
    
    # Determine if failover should be triggered or recovered
    local trigger_failover=false
    local trigger_recovery=false
    
    if [[ "$consecutive_failures" -ge "$FAILURE_THRESHOLD" && "$failover_active" == "false" ]]; then
        trigger_failover=true
        failover_active=true
    elif [[ "$consecutive_successes" -ge "$RECOVERY_THRESHOLD" && "$failover_active" == "true" ]]; then
        trigger_recovery=true
        failover_active=false
    fi
    
    # Update status file
    jq -n \
        --arg endpoint "$endpoint" \
        --arg current_status "$current_status" \
        --argjson consecutive_failures "$consecutive_failures" \
        --argjson consecutive_successes "$consecutive_successes" \
        --arg last_failure "$last_failure" \
        --arg last_success "$last_success" \
        --argjson failover_active "$failover_active" \
        '{
            endpoint: $endpoint,
            current_status: $current_status,
            consecutive_failures: $consecutive_failures,
            consecutive_successes: $consecutive_successes,
            last_failure: $last_failure,
            last_success: $last_success,
            failover_active: $failover_active
        }' > "$status_file"
    
    # Trigger actions if needed
    if [[ "$trigger_failover" == "true" ]]; then
        log "ALERT: Triggering failover for endpoint $endpoint"
        trigger_endpoint_failover "$endpoint"
        send_notification "FAILOVER_TRIGGERED" "$endpoint" "Endpoint failed $consecutive_failures times"
    elif [[ "$trigger_recovery" == "true" ]]; then
        log "INFO: Triggering recovery for endpoint $endpoint"
        trigger_endpoint_recovery "$endpoint"
        send_notification "RECOVERY_TRIGGERED" "$endpoint" "Endpoint recovered after $consecutive_successes successful checks"
    fi
    
    echo "$status_file"
}

# Function to trigger endpoint failover
trigger_endpoint_failover() {
    local endpoint="$1"
    local endpoint_config=$(jq -r --arg url "$endpoint" '.endpoints[] | select(.url == $url)' "$CONFIG_FILE")
    
    log "Executing failover procedures for $endpoint"
    
    # Get failover configuration
    local failover_dns=$(echo "$endpoint_config" | jq -r '.failover.dns_record // ""')
    local failover_target=$(echo "$endpoint_config" | jq -r '.failover.target_endpoint // ""')
    local route53_hosted_zone=$(echo "$endpoint_config" | jq -r '.failover.route53_hosted_zone // ""')
    
    # Update Route 53 DNS record if configured
    if [[ -n "$failover_dns" && -n "$failover_target" && -n "$route53_hosted_zone" ]]; then
        log "Updating Route 53 DNS record: $failover_dns -> $failover_target"
        
        # Create Route 53 change batch
        local change_batch=$(cat << EOF
{
    "Changes": [
        {
            "Action": "UPSERT",
            "ResourceRecordSet": {
                "Name": "$failover_dns",
                "Type": "CNAME",
                "TTL": 60,
                "ResourceRecords": [
                    {
                        "Value": "$failover_target"
                    }
                ]
            }
        }
    ]
}
EOF
        )
        
        # Execute DNS change
        if aws route53 change-resource-record-sets \
            --hosted-zone-id "$route53_hosted_zone" \
            --change-batch "$change_batch" \
            --output json > "$TEMP_DIR/dns_change_result.json" 2>&1; then
            
            local change_id=$(jq -r '.ChangeInfo.Id' "$TEMP_DIR/dns_change_result.json")
            log "DNS change submitted successfully: $change_id"
        else
            log "ERROR: Failed to update DNS record"
            cat "$TEMP_DIR/dns_change_result.json" >> "$LOG_FILE"
        fi
    fi
    
    # Execute custom failover script if configured
    local failover_script=$(echo "$endpoint_config" | jq -r '.failover.script // ""')
    if [[ -n "$failover_script" && -x "$failover_script" ]]; then
        log "Executing custom failover script: $failover_script"
        if "$failover_script" "$endpoint" "failover" >> "$LOG_FILE" 2>&1; then
            log "Custom failover script executed successfully"
        else
            log "ERROR: Custom failover script failed"
        fi
    fi
}

# Function to trigger endpoint recovery
trigger_endpoint_recovery() {
    local endpoint="$1"
    local endpoint_config=$(jq -r --arg url "$endpoint" '.endpoints[] | select(.url == $url)' "$CONFIG_FILE")
    
    log "Executing recovery procedures for $endpoint"
    
    # Get recovery configuration
    local primary_dns=$(echo "$endpoint_config" | jq -r '.primary.dns_record // ""')
    local primary_target=$(echo "$endpoint_config" | jq -r '.primary.target_endpoint // ""')
    local route53_hosted_zone=$(echo "$endpoint_config" | jq -r '.primary.route53_hosted_zone // ""')
    
    # Restore Route 53 DNS record if configured
    if [[ -n "$primary_dns" && -n "$primary_target" && -n "$route53_hosted_zone" ]]; then
        log "Restoring Route 53 DNS record: $primary_dns -> $primary_target"
        
        # Create Route 53 change batch
        local change_batch=$(cat << EOF
{
    "Changes": [
        {
            "Action": "UPSERT",
            "ResourceRecordSet": {
                "Name": "$primary_dns",
                "Type": "CNAME",
                "TTL": 300,
                "ResourceRecords": [
                    {
                        "Value": "$primary_target"
                    }
                ]
            }
        }
    ]
}
EOF
        )
        
        # Execute DNS change
        if aws route53 change-resource-record-sets \
            --hosted-zone-id "$route53_hosted_zone" \
            --change-batch "$change_batch" \
            --output json > "$TEMP_DIR/dns_recovery_result.json" 2>&1; then
            
            local change_id=$(jq -r '.ChangeInfo.Id' "$TEMP_DIR/dns_recovery_result.json")
            log "DNS recovery submitted successfully: $change_id"
        else
            log "ERROR: Failed to restore DNS record"
            cat "$TEMP_DIR/dns_recovery_result.json" >> "$LOG_FILE"
        fi
    fi
    
    # Execute custom recovery script if configured
    local recovery_script=$(echo "$endpoint_config" | jq -r '.recovery.script // ""')
    if [[ -n "$recovery_script" && -x "$recovery_script" ]]; then
        log "Executing custom recovery script: $recovery_script"
        if "$recovery_script" "$endpoint" "recovery" >> "$LOG_FILE" 2>&1; then
            log "Custom recovery script executed successfully"
        else
            log "ERROR: Custom recovery script failed"
        fi
    fi
}

# Function to send notifications
send_notification() {
    local event_type="$1"
    local endpoint="$2"
    local message="$3"
    
    if [[ -n "$NOTIFICATION_TOPIC" ]]; then
        local notification_message=$(cat << EOF
{
    "event_type": "$event_type",
    "endpoint": "$endpoint",
    "message": "$message",
    "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF
        )
        
        if aws sns publish \
            --topic-arn "$NOTIFICATION_TOPIC" \
            --subject "Network Health Alert: $event_type" \
            --message "$notification_message" \
            --output json > /dev/null 2>&1; then
            
            log "Notification sent successfully"
        else
            log "ERROR: Failed to send notification"
        fi
    fi
}

# Function to generate monitoring report
generate_monitoring_report() {
    local report_file="$RESULTS_DIR/network_monitoring_report_$(date +%Y%m%d_%H%M%S).json"
    
    log "Generating monitoring report"
    
    # Collect all status files
    local endpoint_statuses=()
    for status_file in "$TEMP_DIR"/*.status; do
        if [[ -f "$status_file" ]]; then
            endpoint_statuses+=("$(cat "$status_file")")
        fi
    done
    
    # Create comprehensive report
    local endpoint_statuses_json=$(printf '%s\n' "${endpoint_statuses[@]}" | jq -s .)
    
    cat > "$report_file" << EOF
{
    "report_id": "network_monitoring_$(date +%s)",
    "generated_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "monitoring_config": $(cat "$CONFIG_FILE"),
    "endpoint_statuses": $endpoint_statuses_json,
    "summary": {
        "total_endpoints": $(echo "$endpoint_statuses_json" | jq 'length'),
        "healthy_endpoints": $(echo "$endpoint_statuses_json" | jq '[.[] | select(.current_status == "healthy")] | length'),
        "unhealthy_endpoints": $(echo "$endpoint_statuses_json" | jq '[.[] | select(.current_status == "unhealthy")] | length'),
        "failovers_active": $(echo "$endpoint_statuses_json" | jq '[.[] | select(.failover_active == true)] | length')
    }
}
EOF
    
    log "Monitoring report generated: $report_file"
    echo "$report_file"
}

# Main monitoring loop
main_monitoring_loop() {
    log "Starting main monitoring loop"
    
    while true; do
        local cycle_start=$(date +%s)
        
        # Monitor all endpoints
        for endpoint in "${ENDPOINTS[@]}"; do
            log "Checking endpoint: $endpoint"
            
            # Perform comprehensive monitoring
            local monitoring_result=$(monitor_endpoint "$endpoint")
            local overall_status=$(echo "$monitoring_result" | jq -r '.overall_status')
            
            # Update endpoint status and trigger actions if needed
            local status_file=$(update_endpoint_status "$endpoint" "$overall_status")
            
            # Store monitoring result
            local result_file="$RESULTS_DIR/$(echo "$endpoint" | sed 's|[^a-zA-Z0-9]|_|g')_$(date +%Y%m%d_%H%M%S).json"
            echo "$monitoring_result" > "$result_file"
            
            log "Endpoint $endpoint status: $overall_status"
        done
        
        # Generate periodic report
        if (( $(date +%s) % 3600 == 0 )); then  # Every hour
            generate_monitoring_report
        fi
        
        # Calculate sleep time
        local cycle_end=$(date +%s)
        local cycle_duration=$((cycle_end - cycle_start))
        local sleep_time=$((HEALTH_CHECK_INTERVAL - cycle_duration))
        
        if [[ $sleep_time -gt 0 ]]; then
            log "Sleeping for ${sleep_time}s until next check"
            sleep "$sleep_time"
        else
            log "WARNING: Monitoring cycle took ${cycle_duration}s (longer than interval)"
        fi
    done
}

# Configuration file template
create_config_template() {
    cat > network-monitoring-config.json << 'EOF'
{
    "health_check_interval": 30,
    "failure_threshold": 3,
    "recovery_threshold": 2,
    "notification_topic": "arn:aws:sns:us-east-1:123456789012:network-alerts",
    "endpoints": [
        {
            "url": "https://api.example.com",
            "timeout": 10,
            "expected_status": 200,
            "health_check_path": "/health",
            "primary": {
                "dns_record": "api.example.com",
                "target_endpoint": "primary-alb-123456789.us-east-1.elb.amazonaws.com",
                "route53_hosted_zone": "Z1234567890ABC"
            },
            "failover": {
                "dns_record": "api.example.com",
                "target_endpoint": "failover-alb-987654321.us-west-2.elb.amazonaws.com",
                "route53_hosted_zone": "Z1234567890ABC",
                "script": "./scripts/failover.sh"
            },
            "recovery": {
                "script": "./scripts/recovery.sh"
            }
        }
    ]
}
EOF
    log "Created configuration template: network-monitoring-config.json"
}

# Command line argument handling
case "${1:-}" in
    "config")
        create_config_template
        ;;
    "monitor"|"")
        main_monitoring_loop
        ;;
    "report")
        generate_monitoring_report
        ;;
    *)
        echo "Usage: $0 [config|monitor|report]"
        echo "  config  - Create configuration template"
        echo "  monitor - Start monitoring loop (default)"
        echo "  report  - Generate monitoring report"
        exit 1
        ;;
esac
```

## AWS Services Used

- **Amazon Route 53**: DNS management with health checks and failover routing policies
- **Elastic Load Balancing (ALB/NLB)**: Multi-AZ load balancing with health checks and cross-zone load balancing
- **Amazon CloudFront**: Global content delivery network with multiple origin failover
- **AWS WAF**: Web application firewall for application-layer protection
- **AWS Shield**: DDoS protection for network and application layers
- **Amazon VPC**: Virtual private cloud with multi-AZ subnets and redundant gateways
- **AWS Direct Connect**: Dedicated network connections with redundant paths
- **Amazon CloudWatch**: Network monitoring, metrics, and automated alerting
- **AWS Lambda**: Serverless functions for automated network management tasks
- **Amazon SNS**: Notification service for network health alerts
- **VPC Flow Logs**: Network traffic analysis and monitoring
- **AWS Certificate Manager**: SSL/TLS certificate management for HTTPS endpoints

## Benefits

- **High Availability**: Eliminates single points of failure in network connectivity
- **Global Reach**: Provides optimal performance for users worldwide through CloudFront
- **Automatic Failover**: Intelligent routing based on health checks and performance metrics
- **DDoS Protection**: Built-in protection against network and application-layer attacks
- **Performance Optimization**: Edge caching and intelligent routing for reduced latency
- **Comprehensive Monitoring**: Real-time visibility into network health and performance
- **Cost Optimization**: Efficient traffic routing and bandwidth utilization
- **Scalability**: Automatic scaling to handle traffic spikes and growth
- **Security**: Multiple layers of network and application security
- **Disaster Recovery**: Cross-region failover capabilities for business continuity

## Related Resources

- [AWS Well-Architected Reliability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/)
- [Amazon Route 53 Developer Guide](https://docs.aws.amazon.com/route53/latest/developerguide/)
- [Elastic Load Balancing User Guide](https://docs.aws.amazon.com/elasticloadbalancing/latest/userguide/)
- [Amazon CloudFront Developer Guide](https://docs.aws.amazon.com/cloudfront/latest/developerguide/)
- [AWS WAF Developer Guide](https://docs.aws.amazon.com/waf/latest/developerguide/)
- [AWS Shield Advanced Guide](https://docs.aws.amazon.com/waf/latest/developerguide/shield-chapter.html)
- [Amazon VPC User Guide](https://docs.aws.amazon.com/vpc/latest/userguide/)
- [AWS Direct Connect User Guide](https://docs.aws.amazon.com/directconnect/latest/UserGuide/)
- [Amazon CloudWatch User Guide](https://docs.aws.amazon.com/cloudwatch/latest/monitoring/)
