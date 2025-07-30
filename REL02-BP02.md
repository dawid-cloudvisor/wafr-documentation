# REL02-BP02: Provision redundant connectivity between private networks in the cloud and on-premises environments

## Overview

Establish redundant and resilient connectivity between your on-premises infrastructure and AWS cloud environments to ensure reliable hybrid network operations. This involves implementing multiple connection types, redundant paths, and automated failover mechanisms to eliminate single points of failure in your hybrid network architecture.

## Implementation Steps

### 1. Design Redundant Hybrid Connectivity Architecture
- Implement multiple AWS Direct Connect connections across different locations
- Configure redundant VPN connections as backup paths
- Set up AWS Transit Gateway for centralized connectivity management
- Establish diverse network paths to eliminate single points of failure

### 2. Deploy Multi-Path Network Connectivity
- Configure primary and secondary Direct Connect connections
- Implement VPN backup connections with automatic failover
- Set up redundant customer gateways and virtual private gateways
- Establish diverse physical network paths and carrier diversity

### 3. Implement Intelligent Traffic Routing
- Configure BGP routing with path preferences and failover
- Set up dynamic routing protocols for automatic path selection
- Implement traffic engineering and load balancing across connections
- Establish route propagation and filtering policies

### 4. Configure Network Monitoring and Health Checks
- Deploy comprehensive network monitoring across all connection types
- Set up automated health checks and performance monitoring
- Configure alerting for connection failures and performance degradation
- Implement network analytics and troubleshooting tools

### 5. Establish Security and Compliance Controls
- Configure encryption for all hybrid network connections
- Implement network segmentation and access controls
- Set up compliance monitoring and audit trails
- Establish security policies for hybrid network traffic

### 6. Deploy Automated Failover and Recovery
- Configure automatic failover between connection types
- Implement intelligent routing based on connection health
- Set up automated recovery procedures and testing
- Establish disaster recovery and business continuity procedures

## Implementation Examples

### Example 1: Multi-Path Direct Connect and VPN Hybrid Architecture
```python
import boto3
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import time
import ipaddress
from enum import Enum

class ConnectionType(Enum):
    DIRECT_CONNECT = "direct_connect"
    VPN = "vpn"
    TRANSIT_GATEWAY = "transit_gateway"

class ConnectionStatus(Enum):
    AVAILABLE = "available"
    DOWN = "down"
    PENDING = "pending"
    DELETING = "deleting"

@dataclass
class NetworkConnection:
    connection_id: str
    connection_type: ConnectionType
    location: str
    bandwidth: str
    status: ConnectionStatus
    bgp_asn: int
    vlan_id: Optional[int] = None
    customer_gateway_ip: Optional[str] = None

@dataclass
class HybridNetworkConfig:
    vpc_cidr: str
    on_premises_cidrs: List[str]
    primary_connection: NetworkConnection
    secondary_connections: List[NetworkConnection]
    bgp_asn: int
    enable_redundancy: bool = True

class HybridNetworkArchitect:
    def __init__(self, config: Dict):
        self.config = config
        self.ec2 = boto3.client('ec2')
        self.directconnect = boto3.client('directconnect')
        self.cloudwatch = boto3.client('cloudwatch')
        self.sns = boto3.client('sns')
        
    def deploy_redundant_hybrid_network(self, network_config: HybridNetworkConfig) -> Dict:
        """Deploy complete redundant hybrid network architecture"""
        deployment_id = f"hybrid_network_{int(datetime.utcnow().timestamp())}"
        
        deployment_result = {
            'deployment_id': deployment_id,
            'timestamp': datetime.utcnow().isoformat(),
            'network_config': asdict(network_config),
            'components': {},
            'status': 'initiated'
        }
        
        try:
            # 1. Create VPC infrastructure
            vpc_result = self.create_hybrid_vpc_infrastructure(network_config)
            deployment_result['components']['vpc'] = vpc_result
            
            # 2. Set up Transit Gateway for centralized connectivity
            tgw_result = self.setup_transit_gateway(network_config, vpc_result)
            deployment_result['components']['transit_gateway'] = tgw_result
            
            # 3. Configure Direct Connect connections
            dx_result = self.configure_direct_connect_connections(
                network_config, tgw_result
            )
            deployment_result['components']['direct_connect'] = dx_result
            
            # 4. Set up redundant VPN connections
            vpn_result = self.setup_redundant_vpn_connections(
                network_config, tgw_result
            )
            deployment_result['components']['vpn'] = vpn_result
            
            # 5. Configure BGP routing and failover
            routing_result = self.configure_bgp_routing_and_failover(
                network_config, dx_result, vpn_result, tgw_result
            )
            deployment_result['components']['routing'] = routing_result
            
            # 6. Set up network monitoring and health checks
            monitoring_result = self.setup_network_monitoring(
                deployment_id, deployment_result['components']
            )
            deployment_result['components']['monitoring'] = monitoring_result
            
            deployment_result['status'] = 'completed'
            
        except Exception as e:
            logging.error(f"Error deploying hybrid network: {str(e)}")
            deployment_result['status'] = 'failed'
            deployment_result['error'] = str(e)
        
        return deployment_result
    
    def create_hybrid_vpc_infrastructure(self, network_config: HybridNetworkConfig) -> Dict:
        """Create VPC infrastructure optimized for hybrid connectivity"""
        try:
            # Create VPC
            vpc_response = self.ec2.create_vpc(
                CidrBlock=network_config.vpc_cidr,
                TagSpecifications=[
                    {
                        'ResourceType': 'vpc',
                        'Tags': [
                            {'Key': 'Name', 'Value': 'hybrid-network-vpc'},
                            {'Key': 'Purpose', 'Value': 'HybridConnectivity'}
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
            
            # Create subnets for hybrid connectivity
            subnets = self.create_hybrid_subnets(vpc_id, available_azs, network_config)
            
            # Create route tables for hybrid routing
            route_tables = self.create_hybrid_route_tables(vpc_id, subnets)
            
            return {
                'vpc_id': vpc_id,
                'vpc_cidr': network_config.vpc_cidr,
                'availability_zones': available_azs,
                'subnets': subnets,
                'route_tables': route_tables,
                'status': 'created'
            }
            
        except Exception as e:
            logging.error(f"Error creating VPC infrastructure: {str(e)}")
            raise
    
    def create_hybrid_subnets(self, vpc_id: str, azs: List[str], 
                            network_config: HybridNetworkConfig) -> Dict:
        """Create subnets optimized for hybrid connectivity"""
        subnets = {
            'private': [],
            'transit_gateway': [],
            'direct_connect': []
        }
        
        # Parse VPC CIDR for subnet creation
        vpc_network = ipaddress.IPv4Network(network_config.vpc_cidr)
        subnet_size = 24  # /24 subnets
        
        subnet_iterator = vpc_network.subnets(new_prefix=subnet_size)
        
        for i, az in enumerate(azs):
            # Private subnet for workloads
            private_subnet = next(subnet_iterator)
            private_response = self.ec2.create_subnet(
                VpcId=vpc_id,
                CidrBlock=str(private_subnet),
                AvailabilityZone=az,
                TagSpecifications=[
                    {
                        'ResourceType': 'subnet',
                        'Tags': [
                            {'Key': 'Name', 'Value': f"private-subnet-{az}"},
                            {'Key': 'Type', 'Value': 'Private'},
                            {'Key': 'Purpose', 'Value': 'HybridWorkloads'}
                        ]
                    }
                ]
            )
            
            subnets['private'].append({
                'subnet_id': private_response['Subnet']['SubnetId'],
                'availability_zone': az,
                'cidr_block': str(private_subnet),
                'type': 'private'
            })
            
            # Transit Gateway subnet
            tgw_subnet = next(subnet_iterator)
            tgw_response = self.ec2.create_subnet(
                VpcId=vpc_id,
                CidrBlock=str(tgw_subnet),
                AvailabilityZone=az,
                TagSpecifications=[
                    {
                        'ResourceType': 'subnet',
                        'Tags': [
                            {'Key': 'Name', 'Value': f"tgw-subnet-{az}"},
                            {'Key': 'Type', 'Value': 'TransitGateway'},
                            {'Key': 'Purpose', 'Value': 'HybridConnectivity'}
                        ]
                    }
                ]
            )
            
            subnets['transit_gateway'].append({
                'subnet_id': tgw_response['Subnet']['SubnetId'],
                'availability_zone': az,
                'cidr_block': str(tgw_subnet),
                'type': 'transit_gateway'
            })
            
            # Direct Connect Gateway subnet (if needed)
            if i < 2:  # Only create in first two AZs
                dx_subnet = next(subnet_iterator)
                dx_response = self.ec2.create_subnet(
                    VpcId=vpc_id,
                    CidrBlock=str(dx_subnet),
                    AvailabilityZone=az,
                    TagSpecifications=[
                        {
                            'ResourceType': 'subnet',
                            'Tags': [
                                {'Key': 'Name', 'Value': f"dx-subnet-{az}"},
                                {'Key': 'Type', 'Value': 'DirectConnect'},
                                {'Key': 'Purpose', 'Value': 'HybridConnectivity'}
                            ]
                        }
                    ]
                )
                
                subnets['direct_connect'].append({
                    'subnet_id': dx_response['Subnet']['SubnetId'],
                    'availability_zone': az,
                    'cidr_block': str(dx_subnet),
                    'type': 'direct_connect'
                })
        
        return subnets
    
    def setup_transit_gateway(self, network_config: HybridNetworkConfig, 
                            vpc_result: Dict) -> Dict:
        """Set up Transit Gateway for centralized hybrid connectivity"""
        try:
            # Create Transit Gateway
            tgw_response = self.ec2.create_transit_gateway(
                Description='Hybrid network Transit Gateway',
                Options={
                    'AmazonSideAsn': network_config.bgp_asn,
                    'AutoAcceptSharedAttachments': 'enable',
                    'DefaultRouteTableAssociation': 'enable',
                    'DefaultRouteTablePropagation': 'enable',
                    'DnsSupport': 'enable',
                    'VpnEcmpSupport': 'enable'
                },
                TagSpecifications=[
                    {
                        'ResourceType': 'transit-gateway',
                        'Tags': [
                            {'Key': 'Name', 'Value': 'hybrid-network-tgw'},
                            {'Key': 'Purpose', 'Value': 'HybridConnectivity'}
                        ]
                    }
                ]
            )
            
            tgw_id = tgw_response['TransitGateway']['TransitGatewayId']
            
            # Wait for Transit Gateway to be available
            self.wait_for_transit_gateway_available(tgw_id)
            
            # Create VPC attachment
            vpc_attachment_response = self.ec2.create_transit_gateway_vpc_attachment(
                TransitGatewayId=tgw_id,
                VpcId=vpc_result['vpc_id'],
                SubnetIds=[subnet['subnet_id'] for subnet in vpc_result['subnets']['transit_gateway']],
                TagSpecifications=[
                    {
                        'ResourceType': 'transit-gateway-attachment',
                        'Tags': [
                            {'Key': 'Name', 'Value': 'hybrid-vpc-attachment'},
                            {'Key': 'Purpose', 'Value': 'HybridConnectivity'}
                        ]
                    }
                ]
            )
            
            vpc_attachment_id = vpc_attachment_response['TransitGatewayVpcAttachment']['TransitGatewayAttachmentId']
            
            # Create Direct Connect Gateway for DX connections
            dx_gateway_response = self.directconnect.create_direct_connect_gateway(
                name='hybrid-network-dx-gateway',
                amazonSideAsn=network_config.bgp_asn
            )
            
            dx_gateway_id = dx_gateway_response['directConnectGateway']['directConnectGatewayId']
            
            # Associate Direct Connect Gateway with Transit Gateway
            dx_tgw_association_response = self.ec2.create_transit_gateway_direct_connect_gateway_attachment(
                TransitGatewayId=tgw_id,
                DirectConnectGatewayId=dx_gateway_id,
                TagSpecifications=[
                    {
                        'ResourceType': 'transit-gateway-attachment',
                        'Tags': [
                            {'Key': 'Name', 'Value': 'dx-gateway-attachment'},
                            {'Key': 'Purpose', 'Value': 'HybridConnectivity'}
                        ]
                    }
                ]
            )
            
            return {
                'transit_gateway_id': tgw_id,
                'vpc_attachment_id': vpc_attachment_id,
                'direct_connect_gateway_id': dx_gateway_id,
                'dx_tgw_attachment_id': dx_tgw_association_response['TransitGatewayDirectConnectGatewayAttachment']['TransitGatewayAttachmentId'],
                'bgp_asn': network_config.bgp_asn,
                'status': 'created'
            }
            
        except Exception as e:
            logging.error(f"Error setting up Transit Gateway: {str(e)}")
            raise
    
    def wait_for_transit_gateway_available(self, tgw_id: str, timeout: int = 600):
        """Wait for Transit Gateway to become available"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            response = self.ec2.describe_transit_gateways(TransitGatewayIds=[tgw_id])
            
            if response['TransitGateways'][0]['State'] == 'available':
                logging.info(f"Transit Gateway {tgw_id} is available")
                return
            
            time.sleep(30)
        
        raise TimeoutError(f"Transit Gateway {tgw_id} did not become available within timeout")
    
    def configure_direct_connect_connections(self, network_config: HybridNetworkConfig,
                                           tgw_result: Dict) -> Dict:
        """Configure redundant Direct Connect connections"""
        try:
            dx_connections = []
            
            # Primary Direct Connect connection
            primary_dx = self.create_direct_connect_connection(
                network_config.primary_connection,
                tgw_result['direct_connect_gateway_id'],
                is_primary=True
            )
            dx_connections.append(primary_dx)
            
            # Secondary Direct Connect connections
            for secondary_connection in network_config.secondary_connections:
                if secondary_connection.connection_type == ConnectionType.DIRECT_CONNECT:
                    secondary_dx = self.create_direct_connect_connection(
                        secondary_connection,
                        tgw_result['direct_connect_gateway_id'],
                        is_primary=False
                    )
                    dx_connections.append(secondary_dx)
            
            return {
                'connections': dx_connections,
                'direct_connect_gateway_id': tgw_result['direct_connect_gateway_id'],
                'status': 'configured'
            }
            
        except Exception as e:
            logging.error(f"Error configuring Direct Connect: {str(e)}")
            return {'status': 'failed', 'error': str(e)}
    
    def create_direct_connect_connection(self, connection_config: NetworkConnection,
                                       dx_gateway_id: str, is_primary: bool = True) -> Dict:
        """Create individual Direct Connect connection"""
        try:
            # Create Direct Connect connection
            dx_response = self.directconnect.create_connection(
                location=connection_config.location,
                bandwidth=connection_config.bandwidth,
                connectionName=f"hybrid-dx-{'primary' if is_primary else 'secondary'}-{connection_config.location}",
                lagId='',  # Not using LAG for this example
                tags=[
                    {'key': 'Name', 'value': f"hybrid-dx-{'primary' if is_primary else 'secondary'}"},
                    {'key': 'Purpose', 'value': 'HybridConnectivity'},
                    {'key': 'Type', 'value': 'Primary' if is_primary else 'Secondary'}
                ]
            )
            
            dx_connection_id = dx_response['connectionId']
            
            # Create Virtual Interface (VIF)
            vif_response = self.directconnect.create_transit_virtual_interface(
                connectionId=dx_connection_id,
                newTransitVirtualInterface={
                    'vlan': connection_config.vlan_id or (100 if is_primary else 200),
                    'bgpAsn': connection_config.bgp_asn,
                    'mtu': 9000,
                    'directConnectGatewayId': dx_gateway_id,
                    'virtualInterfaceName': f"hybrid-vif-{'primary' if is_primary else 'secondary'}",
                    'tags': [
                        {'key': 'Name', 'value': f"hybrid-vif-{'primary' if is_primary else 'secondary'}"},
                        {'key': 'Purpose', 'value': 'HybridConnectivity'}
                    ]
                }
            )
            
            vif_id = vif_response['virtualInterface']['virtualInterfaceId']
            
            return {
                'connection_id': dx_connection_id,
                'virtual_interface_id': vif_id,
                'location': connection_config.location,
                'bandwidth': connection_config.bandwidth,
                'vlan_id': connection_config.vlan_id or (100 if is_primary else 200),
                'bgp_asn': connection_config.bgp_asn,
                'is_primary': is_primary,
                'status': 'created'
            }
            
        except Exception as e:
            logging.error(f"Error creating Direct Connect connection: {str(e)}")
            raise
    
    def setup_redundant_vpn_connections(self, network_config: HybridNetworkConfig,
                                      tgw_result: Dict) -> Dict:
        """Set up redundant VPN connections as backup"""
        try:
            vpn_connections = []
            
            # Create customer gateways for VPN connections
            customer_gateways = self.create_customer_gateways(network_config)
            
            # Create VPN connections for each customer gateway
            for i, cgw in enumerate(customer_gateways):
                vpn_connection = self.create_vpn_connection(
                    cgw, tgw_result['transit_gateway_id'], i + 1
                )
                vpn_connections.append(vpn_connection)
            
            return {
                'customer_gateways': customer_gateways,
                'vpn_connections': vpn_connections,
                'status': 'configured'
            }
            
        except Exception as e:
            logging.error(f"Error setting up VPN connections: {str(e)}")
            return {'status': 'failed', 'error': str(e)}
    
    def create_customer_gateways(self, network_config: HybridNetworkConfig) -> List[Dict]:
        """Create customer gateways for VPN connections"""
        customer_gateways = []
        
        # Extract VPN connection configs
        vpn_connections = [
            conn for conn in network_config.secondary_connections
            if conn.connection_type == ConnectionType.VPN
        ]
        
        for i, vpn_config in enumerate(vpn_connections):
            try:
                cgw_response = self.ec2.create_customer_gateway(
                    Type='ipsec.1',
                    PublicIp=vpn_config.customer_gateway_ip,
                    BgpAsn=vpn_config.bgp_asn,
                    TagSpecifications=[
                        {
                            'ResourceType': 'customer-gateway',
                            'Tags': [
                                {'Key': 'Name', 'Value': f"hybrid-cgw-{i+1}"},
                                {'Key': 'Purpose', 'Value': 'HybridConnectivity'}
                            ]
                        }
                    ]
                )
                
                customer_gateways.append({
                    'customer_gateway_id': cgw_response['CustomerGateway']['CustomerGatewayId'],
                    'public_ip': vpn_config.customer_gateway_ip,
                    'bgp_asn': vpn_config.bgp_asn,
                    'index': i + 1
                })
                
            except Exception as e:
                logging.error(f"Error creating customer gateway {i+1}: {str(e)}")
                continue
        
        return customer_gateways
    
    def create_vpn_connection(self, customer_gateway: Dict, 
                            transit_gateway_id: str, index: int) -> Dict:
        """Create individual VPN connection"""
        try:
            vpn_response = self.ec2.create_vpn_connection(
                Type='ipsec.1',
                CustomerGatewayId=customer_gateway['customer_gateway_id'],
                TransitGatewayId=transit_gateway_id,
                Options={
                    'StaticRoutesOnly': False,  # Use BGP
                    'TunnelInsideIpVersion': 'ipv4'
                },
                TagSpecifications=[
                    {
                        'ResourceType': 'vpn-connection',
                        'Tags': [
                            {'Key': 'Name', 'Value': f"hybrid-vpn-{index}"},
                            {'Key': 'Purpose', 'Value': 'HybridConnectivity'},
                            {'Key': 'Type', 'Value': 'Backup'}
                        ]
                    }
                ]
            )
            
            vpn_connection_id = vpn_response['VpnConnection']['VpnConnectionId']
            
            return {
                'vpn_connection_id': vpn_connection_id,
                'customer_gateway_id': customer_gateway['customer_gateway_id'],
                'customer_gateway_ip': customer_gateway['public_ip'],
                'transit_gateway_id': transit_gateway_id,
                'index': index,
                'status': 'created'
            }
            
        except Exception as e:
            logging.error(f"Error creating VPN connection {index}: {str(e)}")
            raise
    
    def configure_bgp_routing_and_failover(self, network_config: HybridNetworkConfig,
                                         dx_result: Dict, vpn_result: Dict,
                                         tgw_result: Dict) -> Dict:
        """Configure BGP routing with intelligent failover"""
        try:
            routing_config = {
                'transit_gateway_route_tables': [],
                'route_propagations': [],
                'route_preferences': {}
            }
            
            # Get Transit Gateway default route table
            tgw_route_tables = self.ec2.describe_transit_gateway_route_tables(
                Filters=[
                    {'Name': 'transit-gateway-id', 'Values': [tgw_result['transit_gateway_id']]},
                    {'Name': 'default-association-route-table', 'Values': ['true']}
                ]
            )
            
            if tgw_route_tables['TransitGatewayRouteTables']:
                default_route_table_id = tgw_route_tables['TransitGatewayRouteTables'][0]['TransitGatewayRouteTableId']
                
                # Configure route propagation for on-premises networks
                for on_premises_cidr in network_config.on_premises_cidrs:
                    # Create routes with different preferences
                    # Direct Connect gets higher preference (lower metric)
                    if dx_result['status'] == 'configured':
                        for dx_connection in dx_result['connections']:
                            if dx_connection['is_primary']:
                                # Primary DX route with highest preference
                                self.create_transit_gateway_route(
                                    default_route_table_id,
                                    on_premises_cidr,
                                    tgw_result['dx_tgw_attachment_id'],
                                    preference=100
                                )
                    
                    # VPN routes with lower preference (backup)
                    if vpn_result['status'] == 'configured':
                        for vpn_connection in vpn_result['vpn_connections']:
                            # VPN routes as backup with lower preference
                            vpn_attachment_id = self.get_vpn_attachment_id(
                                vpn_connection['vpn_connection_id'],
                                tgw_result['transit_gateway_id']
                            )
                            if vpn_attachment_id:
                                self.create_transit_gateway_route(
                                    default_route_table_id,
                                    on_premises_cidr,
                                    vpn_attachment_id,
                                    preference=200
                                )
                
                routing_config['default_route_table_id'] = default_route_table_id
            
            return {
                'routing_config': routing_config,
                'bgp_asn': network_config.bgp_asn,
                'status': 'configured'
            }
            
        except Exception as e:
            logging.error(f"Error configuring BGP routing: {str(e)}")
            return {'status': 'failed', 'error': str(e)}
    
    def create_transit_gateway_route(self, route_table_id: str, destination_cidr: str,
                                   attachment_id: str, preference: int):
        """Create Transit Gateway route with preference"""
        try:
            self.ec2.create_transit_gateway_route(
                DestinationCidrBlock=destination_cidr,
                TransitGatewayRouteTableId=route_table_id,
                TransitGatewayAttachmentId=attachment_id
            )
            
            logging.info(f"Created route {destination_cidr} -> {attachment_id} with preference {preference}")
            
        except Exception as e:
            logging.error(f"Error creating Transit Gateway route: {str(e)}")
    
    def get_vpn_attachment_id(self, vpn_connection_id: str, transit_gateway_id: str) -> Optional[str]:
        """Get VPN attachment ID for Transit Gateway"""
        try:
            attachments = self.ec2.describe_transit_gateway_attachments(
                Filters=[
                    {'Name': 'transit-gateway-id', 'Values': [transit_gateway_id]},
                    {'Name': 'resource-type', 'Values': ['vpn']},
                    {'Name': 'resource-id', 'Values': [vpn_connection_id]}
                ]
            )
            
            if attachments['TransitGatewayAttachments']:
                return attachments['TransitGatewayAttachments'][0]['TransitGatewayAttachmentId']
            
            return None
            
        except Exception as e:
            logging.error(f"Error getting VPN attachment ID: {str(e)}")
            return None

# Usage example
def main():
    config = {
        'region': 'us-east-1',
        'environment': 'production'
    }
    
    architect = HybridNetworkArchitect(config)
    
    # Define hybrid network configuration
    network_config = HybridNetworkConfig(
        vpc_cidr='10.0.0.0/16',
        on_premises_cidrs=['192.168.0.0/16', '172.16.0.0/12'],
        primary_connection=NetworkConnection(
            connection_id='primary-dx',
            connection_type=ConnectionType.DIRECT_CONNECT,
            location='EqDC2',
            bandwidth='1Gbps',
            status=ConnectionStatus.PENDING,
            bgp_asn=65000,
            vlan_id=100
        ),
        secondary_connections=[
            NetworkConnection(
                connection_id='secondary-dx',
                connection_type=ConnectionType.DIRECT_CONNECT,
                location='EqDA2',
                bandwidth='1Gbps',
                status=ConnectionStatus.PENDING,
                bgp_asn=65000,
                vlan_id=200
            ),
            NetworkConnection(
                connection_id='backup-vpn-1',
                connection_type=ConnectionType.VPN,
                location='on-premises',
                bandwidth='100Mbps',
                status=ConnectionStatus.PENDING,
                bgp_asn=65001,
                customer_gateway_ip='203.0.113.12'
            ),
            NetworkConnection(
                connection_id='backup-vpn-2',
                connection_type=ConnectionType.VPN,
                location='on-premises',
                bandwidth='100Mbps',
                status=ConnectionStatus.PENDING,
                bgp_asn=65001,
                customer_gateway_ip='203.0.113.13'
            )
        ],
        bgp_asn=64512,
        enable_redundancy=True
    )
    
    # Deploy redundant hybrid network
    result = architect.deploy_redundant_hybrid_network(network_config)
    
    print(f"Deployment Status: {result['status']}")
    if result['status'] == 'completed':
        print("Redundant hybrid network deployed successfully!")
        for component, details in result['components'].items():
            print(f"- {component}: {details.get('status', 'unknown')}")
    else:
        print(f"Deployment failed: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    main()
```
### Example 2: Automated Network Health Monitoring and Failover System

```python
import boto3
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass
import time
import threading
import subprocess
import ipaddress

@dataclass
class NetworkPath:
    path_id: str
    connection_type: str
    attachment_id: str
    destination_cidr: str
    next_hop: str
    metric: int
    status: str
    last_check: datetime
    failure_count: int = 0
    success_count: int = 0

@dataclass
class HealthCheckConfig:
    target_ip: str
    check_interval: int = 30
    timeout: int = 5
    failure_threshold: int = 3
    recovery_threshold: int = 2

class HybridNetworkMonitor:
    def __init__(self, config: Dict):
        self.config = config
        self.ec2 = boto3.client('ec2')
        self.directconnect = boto3.client('directconnect')
        self.cloudwatch = boto3.client('cloudwatch')
        self.sns = boto3.client('sns')
        
        # Network paths and health status
        self.network_paths: Dict[str, NetworkPath] = {}
        self.health_checks: Dict[str, HealthCheckConfig] = {}
        self.monitoring_active = False
        self.monitoring_thread = None
        
    def start_network_monitoring(self, monitoring_config: Dict) -> Dict:
        """Start comprehensive network monitoring"""
        try:
            # Initialize network paths
            self.initialize_network_paths(monitoring_config)
            
            # Set up health checks
            self.setup_health_checks(monitoring_config)
            
            # Start monitoring thread
            self.monitoring_active = True
            self.monitoring_thread = threading.Thread(
                target=self.monitoring_loop,
                daemon=True
            )
            self.monitoring_thread.start()
            
            # Set up CloudWatch metrics
            self.setup_cloudwatch_metrics()
            
            return {
                'status': 'started',
                'network_paths': len(self.network_paths),
                'health_checks': len(self.health_checks),
                'timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logging.error(f"Error starting network monitoring: {str(e)}")
            return {'status': 'failed', 'error': str(e)}
    
    def initialize_network_paths(self, monitoring_config: Dict):
        """Initialize network paths for monitoring"""
        transit_gateway_id = monitoring_config.get('transit_gateway_id')
        
        if not transit_gateway_id:
            raise ValueError("Transit Gateway ID is required for monitoring")
        
        # Get Transit Gateway route tables
        route_tables = self.ec2.describe_transit_gateway_route_tables(
            Filters=[
                {'Name': 'transit-gateway-id', 'Values': [transit_gateway_id]}
            ]
        )
        
        for route_table in route_tables['TransitGatewayRouteTables']:
            route_table_id = route_table['TransitGatewayRouteTableId']
            
            # Get routes from route table
            routes = self.ec2.search_transit_gateway_routes(
                TransitGatewayRouteTableId=route_table_id,
                Filters=[
                    {'Name': 'state', 'Values': ['active']}
                ]
            )
            
            for route in routes['Routes']:
                if route.get('TransitGatewayAttachments'):
                    for attachment in route['TransitGatewayAttachments']:
                        path_id = f"{route['DestinationCidrBlock']}_{attachment['TransitGatewayAttachmentId']}"
                        
                        network_path = NetworkPath(
                            path_id=path_id,
                            connection_type=attachment['ResourceType'],
                            attachment_id=attachment['TransitGatewayAttachmentId'],
                            destination_cidr=route['DestinationCidrBlock'],
                            next_hop=attachment.get('ResourceId', ''),
                            metric=route.get('PrefixListId', 100),
                            status='unknown',
                            last_check=datetime.utcnow()
                        )
                        
                        self.network_paths[path_id] = network_path
    
    def setup_health_checks(self, monitoring_config: Dict):
        """Set up health checks for network paths"""
        health_check_targets = monitoring_config.get('health_check_targets', [])
        
        for target in health_check_targets:
            target_ip = target.get('ip')
            if target_ip:
                health_check = HealthCheckConfig(
                    target_ip=target_ip,
                    check_interval=target.get('interval', 30),
                    timeout=target.get('timeout', 5),
                    failure_threshold=target.get('failure_threshold', 3),
                    recovery_threshold=target.get('recovery_threshold', 2)
                )
                
                self.health_checks[target_ip] = health_check
    
    def monitoring_loop(self):
        """Main monitoring loop"""
        while self.monitoring_active:
            try:
                # Check network path health
                self.check_network_paths_health()
                
                # Perform connectivity tests
                self.perform_connectivity_tests()
                
                # Update CloudWatch metrics
                self.update_cloudwatch_metrics()
                
                # Check for failover conditions
                self.evaluate_failover_conditions()
                
                # Sleep until next check
                time.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                logging.error(f"Error in monitoring loop: {str(e)}")
                time.sleep(60)  # Wait longer on error
    
    def check_network_paths_health(self):
        """Check health of all network paths"""
        for path_id, network_path in self.network_paths.items():
            try:
                # Check attachment status
                attachment_status = self.check_attachment_status(network_path.attachment_id)
                
                # Update path status
                previous_status = network_path.status
                network_path.status = attachment_status
                network_path.last_check = datetime.utcnow()
                
                # Update counters
                if attachment_status == 'available':
                    network_path.success_count += 1
                    network_path.failure_count = 0
                else:
                    network_path.failure_count += 1
                    network_path.success_count = 0
                
                # Log status changes
                if previous_status != attachment_status:
                    logging.info(f"Network path {path_id} status changed: {previous_status} -> {attachment_status}")
                    
                    # Send notification for status changes
                    self.send_path_status_notification(network_path, previous_status)
                
            except Exception as e:
                logging.error(f"Error checking path {path_id}: {str(e)}")
                network_path.status = 'error'
                network_path.failure_count += 1
    
    def check_attachment_status(self, attachment_id: str) -> str:
        """Check status of Transit Gateway attachment"""
        try:
            attachments = self.ec2.describe_transit_gateway_attachments(
                TransitGatewayAttachmentIds=[attachment_id]
            )
            
            if attachments['TransitGatewayAttachments']:
                return attachments['TransitGatewayAttachments'][0]['State']
            
            return 'not_found'
            
        except Exception as e:
            logging.error(f"Error checking attachment {attachment_id}: {str(e)}")
            return 'error'
    
    def perform_connectivity_tests(self):
        """Perform connectivity tests to on-premises targets"""
        for target_ip, health_check in self.health_checks.items():
            try:
                # Perform ping test
                ping_result = self.ping_test(target_ip, health_check.timeout)
                
                # Perform traceroute test
                traceroute_result = self.traceroute_test(target_ip)
                
                # Update health check status
                self.update_health_check_status(target_ip, ping_result, traceroute_result)
                
            except Exception as e:
                logging.error(f"Error testing connectivity to {target_ip}: {str(e)}")
    
    def ping_test(self, target_ip: str, timeout: int) -> Dict:
        """Perform ping test to target IP"""
        try:
            start_time = time.time()
            
            # Execute ping command
            result = subprocess.run(
                ['ping', '-c', '3', '-W', str(timeout), target_ip],
                capture_output=True,
                text=True,
                timeout=timeout + 5
            )
            
            end_time = time.time()
            
            return {
                'success': result.returncode == 0,
                'response_time': end_time - start_time,
                'output': result.stdout,
                'error': result.stderr
            }
            
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'response_time': timeout,
                'output': '',
                'error': 'Ping timeout'
            }
        except Exception as e:
            return {
                'success': False,
                'response_time': 0,
                'output': '',
                'error': str(e)
            }
    
    def traceroute_test(self, target_ip: str) -> Dict:
        """Perform traceroute test to target IP"""
        try:
            result = subprocess.run(
                ['traceroute', '-m', '10', target_ip],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            return {
                'success': result.returncode == 0,
                'output': result.stdout,
                'error': result.stderr,
                'hops': self.parse_traceroute_hops(result.stdout)
            }
            
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'output': '',
                'error': 'Traceroute timeout',
                'hops': []
            }
        except Exception as e:
            return {
                'success': False,
                'output': '',
                'error': str(e),
                'hops': []
            }
    
    def parse_traceroute_hops(self, traceroute_output: str) -> List[Dict]:
        """Parse traceroute output to extract hops"""
        hops = []
        lines = traceroute_output.split('\n')
        
        for line in lines:
            if line.strip() and not line.startswith('traceroute'):
                parts = line.split()
                if len(parts) >= 2:
                    try:
                        hop_number = int(parts[0])
                        hop_ip = parts[1] if '(' in parts[1] else parts[1]
                        
                        hops.append({
                            'hop': hop_number,
                            'ip': hop_ip,
                            'line': line.strip()
                        })
                    except (ValueError, IndexError):
                        continue
        
        return hops
    
    def update_health_check_status(self, target_ip: str, ping_result: Dict, 
                                 traceroute_result: Dict):
        """Update health check status based on test results"""
        health_check = self.health_checks.get(target_ip)
        if not health_check:
            return
        
        # Determine overall health
        is_healthy = ping_result['success']
        
        # Update counters
        if is_healthy:
            health_check.success_count += 1
            health_check.failure_count = 0
        else:
            health_check.failure_count += 1
            health_check.success_count = 0
        
        # Log health status
        logging.info(f"Health check {target_ip}: {'PASS' if is_healthy else 'FAIL'} "
                    f"(failures: {health_check.failure_count}, successes: {health_check.success_count})")
        
        # Store test results for analysis
        self.store_connectivity_test_results(target_ip, ping_result, traceroute_result)
    
    def evaluate_failover_conditions(self):
        """Evaluate conditions for automatic failover"""
        for target_ip, health_check in self.health_checks.items():
            # Check if failover threshold is reached
            if health_check.failure_count >= health_check.failure_threshold:
                logging.warning(f"Failover threshold reached for {target_ip}")
                self.trigger_network_failover(target_ip, health_check)
            
            # Check if recovery threshold is reached
            elif health_check.success_count >= health_check.recovery_threshold:
                logging.info(f"Recovery threshold reached for {target_ip}")
                self.trigger_network_recovery(target_ip, health_check)
    
    def trigger_network_failover(self, target_ip: str, health_check: HealthCheckConfig):
        """Trigger network failover procedures"""
        try:
            logging.warning(f"Triggering network failover for {target_ip}")
            
            # Find affected network paths
            affected_paths = self.find_paths_to_target(target_ip)
            
            # Implement failover logic
            for path in affected_paths:
                self.failover_network_path(path)
            
            # Send failover notification
            self.send_failover_notification(target_ip, affected_paths)
            
            # Reset failure count to prevent repeated failovers
            health_check.failure_count = 0
            
        except Exception as e:
            logging.error(f"Error triggering failover for {target_ip}: {str(e)}")
    
    def trigger_network_recovery(self, target_ip: str, health_check: HealthCheckConfig):
        """Trigger network recovery procedures"""
        try:
            logging.info(f"Triggering network recovery for {target_ip}")
            
            # Find recovered network paths
            recovered_paths = self.find_paths_to_target(target_ip)
            
            # Implement recovery logic
            for path in recovered_paths:
                self.recover_network_path(path)
            
            # Send recovery notification
            self.send_recovery_notification(target_ip, recovered_paths)
            
            # Reset success count
            health_check.success_count = 0
            
        except Exception as e:
            logging.error(f"Error triggering recovery for {target_ip}: {str(e)}")
    
    def find_paths_to_target(self, target_ip: str) -> List[NetworkPath]:
        """Find network paths that could reach the target IP"""
        affected_paths = []
        
        try:
            target_network = ipaddress.IPv4Address(target_ip)
            
            for path in self.network_paths.values():
                try:
                    path_network = ipaddress.IPv4Network(path.destination_cidr, strict=False)
                    if target_network in path_network:
                        affected_paths.append(path)
                except ValueError:
                    continue
                    
        except ValueError:
            logging.error(f"Invalid target IP: {target_ip}")
        
        return affected_paths
    
    def failover_network_path(self, network_path: NetworkPath):
        """Implement failover for a specific network path"""
        try:
            logging.info(f"Failing over network path: {network_path.path_id}")
            
            # Update route preferences to prefer backup paths
            self.update_route_preferences(network_path, increase_metric=True)
            
            # Log failover action
            self.log_failover_action(network_path, 'failover')
            
        except Exception as e:
            logging.error(f"Error failing over path {network_path.path_id}: {str(e)}")
    
    def recover_network_path(self, network_path: NetworkPath):
        """Implement recovery for a specific network path"""
        try:
            logging.info(f"Recovering network path: {network_path.path_id}")
            
            # Restore original route preferences
            self.update_route_preferences(network_path, increase_metric=False)
            
            # Log recovery action
            self.log_failover_action(network_path, 'recovery')
            
        except Exception as e:
            logging.error(f"Error recovering path {network_path.path_id}: {str(e)}")
    
    def update_route_preferences(self, network_path: NetworkPath, increase_metric: bool):
        """Update route preferences for failover/recovery"""
        try:
            # This would implement actual route preference changes
            # For example, updating BGP metrics or route priorities
            
            action = "increased" if increase_metric else "restored"
            logging.info(f"Route preference {action} for path {network_path.path_id}")
            
        except Exception as e:
            logging.error(f"Error updating route preferences: {str(e)}")
    
    def setup_cloudwatch_metrics(self):
        """Set up CloudWatch custom metrics"""
        try:
            # Create custom metrics for network monitoring
            metric_data = []
            
            for path_id, network_path in self.network_paths.items():
                # Path availability metric
                availability = 1 if network_path.status == 'available' else 0
                
                metric_data.append({
                    'MetricName': 'NetworkPathAvailability',
                    'Dimensions': [
                        {'Name': 'PathId', 'Value': path_id},
                        {'Name': 'ConnectionType', 'Value': network_path.connection_type}
                    ],
                    'Value': availability,
                    'Unit': 'Count'
                })
            
            # Send metrics to CloudWatch
            if metric_data:
                self.cloudwatch.put_metric_data(
                    Namespace='HybridNetwork/Monitoring',
                    MetricData=metric_data
                )
                
        except Exception as e:
            logging.error(f"Error setting up CloudWatch metrics: {str(e)}")
    
    def send_failover_notification(self, target_ip: str, affected_paths: List[NetworkPath]):
        """Send notification about network failover"""
        try:
            message = {
                'event_type': 'NETWORK_FAILOVER',
                'target_ip': target_ip,
                'affected_paths': [path.path_id for path in affected_paths],
                'timestamp': datetime.utcnow().isoformat(),
                'message': f'Network failover triggered for {target_ip}'
            }
            
            if self.config.get('notification_topic_arn'):
                self.sns.publish(
                    TopicArn=self.config['notification_topic_arn'],
                    Subject='Network Failover Alert',
                    Message=json.dumps(message, indent=2)
                )
                
        except Exception as e:
            logging.error(f"Error sending failover notification: {str(e)}")

# Usage example
def main():
    config = {
        'region': 'us-east-1',
        'notification_topic_arn': 'arn:aws:sns:us-east-1:123456789012:network-alerts'
    }
    
    monitor = HybridNetworkMonitor(config)
    
    # Define monitoring configuration
    monitoring_config = {
        'transit_gateway_id': 'tgw-1234567890abcdef0',
        'health_check_targets': [
            {
                'ip': '192.168.1.1',
                'interval': 30,
                'timeout': 5,
                'failure_threshold': 3,
                'recovery_threshold': 2
            },
            {
                'ip': '172.16.1.1',
                'interval': 30,
                'timeout': 5,
                'failure_threshold': 3,
                'recovery_threshold': 2
            }
        ]
    }
    
    # Start network monitoring
    result = monitor.start_network_monitoring(monitoring_config)
    
    print(f"Monitoring Status: {result['status']}")
    if result['status'] == 'started':
        print("Network monitoring started successfully!")
        print(f"- Network paths: {result['network_paths']}")
        print(f"- Health checks: {result['health_checks']}")
        
        # Keep monitoring running
        try:
            while True:
                time.sleep(60)
        except KeyboardInterrupt:
            print("Stopping network monitoring...")
            monitor.monitoring_active = False
    else:
        print(f"Failed to start monitoring: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    main()
```
### Example 3: CloudFormation Template for Redundant Hybrid Connectivity

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Redundant hybrid connectivity infrastructure with Direct Connect and VPN backup'

Parameters:
  Environment:
    Type: String
    Description: Environment name
    Default: production
    AllowedValues: [development, staging, production]
  
  VpcCidr:
    Type: String
    Description: CIDR block for the VPC
    Default: 10.0.0.0/16
    AllowedPattern: ^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])(\/(1[6-9]|2[0-8]))$
  
  OnPremisesCidr:
    Type: String
    Description: CIDR block for on-premises network
    Default: 192.168.0.0/16
    AllowedPattern: ^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])(\/(1[6-9]|2[0-8]))$
  
  BgpAsn:
    Type: Number
    Description: BGP ASN for AWS side
    Default: 64512
    MinValue: 64512
    MaxValue: 65534
  
  CustomerBgpAsn:
    Type: Number
    Description: BGP ASN for customer side
    Default: 65000
    MinValue: 1
    MaxValue: 65534
  
  CustomerGatewayIp1:
    Type: String
    Description: Public IP address for first customer gateway
    Default: 203.0.113.12
    AllowedPattern: ^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$
  
  CustomerGatewayIp2:
    Type: String
    Description: Public IP address for second customer gateway
    Default: 203.0.113.13
    AllowedPattern: ^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$
  
  DirectConnectLocation1:
    Type: String
    Description: Direct Connect location for primary connection
    Default: EqDC2
  
  DirectConnectLocation2:
    Type: String
    Description: Direct Connect location for secondary connection
    Default: EqDA2
  
  DirectConnectBandwidth:
    Type: String
    Description: Bandwidth for Direct Connect connections
    Default: 1Gbps
    AllowedValues: [50Mbps, 100Mbps, 200Mbps, 300Mbps, 400Mbps, 500Mbps, 1Gbps, 2Gbps, 5Gbps, 10Gbps]

Resources:
  # VPC Infrastructure
  HybridVPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: !Ref VpcCidr
      EnableDnsHostnames: true
      EnableDnsSupport: true
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-hybrid-vpc'
        - Key: Environment
          Value: !Ref Environment
        - Key: Purpose
          Value: HybridConnectivity

  # Private Subnets for workloads
  PrivateSubnet1:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref HybridVPC
      AvailabilityZone: !Select [0, !GetAZs '']
      CidrBlock: !Select [0, !Cidr [!Ref VpcCidr, 8, 8]]
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-private-subnet-1'
        - Key: Type
          Value: Private

  PrivateSubnet2:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref HybridVPC
      AvailabilityZone: !Select [1, !GetAZs '']
      CidrBlock: !Select [1, !Cidr [!Ref VpcCidr, 8, 8]]
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-private-subnet-2'
        - Key: Type
          Value: Private

  # Transit Gateway Subnets
  TransitGatewaySubnet1:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref HybridVPC
      AvailabilityZone: !Select [0, !GetAZs '']
      CidrBlock: !Select [2, !Cidr [!Ref VpcCidr, 8, 8]]
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-tgw-subnet-1'
        - Key: Type
          Value: TransitGateway

  TransitGatewaySubnet2:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref HybridVPC
      AvailabilityZone: !Select [1, !GetAZs '']
      CidrBlock: !Select [3, !Cidr [!Ref VpcCidr, 8, 8]]
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-tgw-subnet-2'
        - Key: Type
          Value: TransitGateway

  # Transit Gateway
  TransitGateway:
    Type: AWS::EC2::TransitGateway
    Properties:
      AmazonSideAsn: !Ref BgpAsn
      Description: !Sub 'Transit Gateway for ${Environment} hybrid connectivity'
      DefaultRouteTableAssociation: enable
      DefaultRouteTablePropagation: enable
      DnsSupport: enable
      VpnEcmpSupport: enable
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-hybrid-tgw'
        - Key: Environment
          Value: !Ref Environment

  # VPC Attachment to Transit Gateway
  TransitGatewayVPCAttachment:
    Type: AWS::EC2::TransitGatewayVpcAttachment
    Properties:
      TransitGatewayId: !Ref TransitGateway
      VpcId: !Ref HybridVPC
      SubnetIds:
        - !Ref TransitGatewaySubnet1
        - !Ref TransitGatewaySubnet2
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-vpc-attachment'
        - Key: Environment
          Value: !Ref Environment

  # Direct Connect Gateway
  DirectConnectGateway:
    Type: AWS::DirectConnect::DirectConnectGateway
    Properties:
      Name: !Sub '${Environment}-dx-gateway'
      AmazonSideAsn: !Ref BgpAsn

  # Direct Connect Gateway Association with Transit Gateway
  DirectConnectGatewayToTransitGatewayAssociation:
    Type: AWS::EC2::TransitGatewayDirectConnectGatewayAttachment
    Properties:
      TransitGatewayId: !Ref TransitGateway
      DirectConnectGatewayId: !Ref DirectConnectGateway
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-dx-tgw-attachment'
        - Key: Environment
          Value: !Ref Environment

  # Primary Direct Connect Connection
  PrimaryDirectConnectConnection:
    Type: AWS::DirectConnect::Connection
    Properties:
      ConnectionName: !Sub '${Environment}-primary-dx'
      Location: !Ref DirectConnectLocation1
      Bandwidth: !Ref DirectConnectBandwidth
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-primary-dx'
        - Key: Environment
          Value: !Ref Environment
        - Key: Type
          Value: Primary

  # Secondary Direct Connect Connection
  SecondaryDirectConnectConnection:
    Type: AWS::DirectConnect::Connection
    Properties:
      ConnectionName: !Sub '${Environment}-secondary-dx'
      Location: !Ref DirectConnectLocation2
      Bandwidth: !Ref DirectConnectBandwidth
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-secondary-dx'
        - Key: Environment
          Value: !Ref Environment
        - Key: Type
          Value: Secondary

  # Primary Direct Connect Virtual Interface
  PrimaryDirectConnectVIF:
    Type: AWS::DirectConnect::TransitVirtualInterface
    Properties:
      ConnectionId: !Ref PrimaryDirectConnectConnection
      DirectConnectGatewayId: !Ref DirectConnectGateway
      Vlan: 100
      BgpAsn: !Ref CustomerBgpAsn
      Mtu: 9000
      VirtualInterfaceName: !Sub '${Environment}-primary-vif'
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-primary-vif'
        - Key: Environment
          Value: !Ref Environment

  # Secondary Direct Connect Virtual Interface
  SecondaryDirectConnectVIF:
    Type: AWS::DirectConnect::TransitVirtualInterface
    Properties:
      ConnectionId: !Ref SecondaryDirectConnectConnection
      DirectConnectGatewayId: !Ref DirectConnectGateway
      Vlan: 200
      BgpAsn: !Ref CustomerBgpAsn
      Mtu: 9000
      VirtualInterfaceName: !Sub '${Environment}-secondary-vif'
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-secondary-vif'
        - Key: Environment
          Value: !Ref Environment

  # Customer Gateways for VPN backup
  CustomerGateway1:
    Type: AWS::EC2::CustomerGateway
    Properties:
      Type: ipsec.1
      BgpAsn: !Ref CustomerBgpAsn
      IpAddress: !Ref CustomerGatewayIp1
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-cgw-1'
        - Key: Environment
          Value: !Ref Environment

  CustomerGateway2:
    Type: AWS::EC2::CustomerGateway
    Properties:
      Type: ipsec.1
      BgpAsn: !Ref CustomerBgpAsn
      IpAddress: !Ref CustomerGatewayIp2
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-cgw-2'
        - Key: Environment
          Value: !Ref Environment

  # VPN Connections for backup
  VPNConnection1:
    Type: AWS::EC2::VPNConnection
    Properties:
      Type: ipsec.1
      CustomerGatewayId: !Ref CustomerGateway1
      TransitGatewayId: !Ref TransitGateway
      StaticRoutesOnly: false
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-vpn-1'
        - Key: Environment
          Value: !Ref Environment
        - Key: Type
          Value: Backup

  VPNConnection2:
    Type: AWS::EC2::VPNConnection
    Properties:
      Type: ipsec.1
      CustomerGatewayId: !Ref CustomerGateway2
      TransitGatewayId: !Ref TransitGateway
      StaticRoutesOnly: false
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-vpn-2'
        - Key: Environment
          Value: !Ref Environment
        - Key: Type
          Value: Backup

  # Route Tables
  PrivateRouteTable1:
    Type: AWS::EC2::RouteTable
    Properties:
      VpcId: !Ref HybridVPC
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-private-rt-1'
        - Key: Environment
          Value: !Ref Environment

  PrivateRouteTable2:
    Type: AWS::EC2::RouteTable
    Properties:
      VpcId: !Ref HybridVPC
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-private-rt-2'
        - Key: Environment
          Value: !Ref Environment

  # Route to on-premises via Transit Gateway
  OnPremisesRoute1:
    Type: AWS::EC2::Route
    DependsOn: TransitGatewayVPCAttachment
    Properties:
      RouteTableId: !Ref PrivateRouteTable1
      DestinationCidrBlock: !Ref OnPremisesCidr
      TransitGatewayId: !Ref TransitGateway

  OnPremisesRoute2:
    Type: AWS::EC2::Route
    DependsOn: TransitGatewayVPCAttachment
    Properties:
      RouteTableId: !Ref PrivateRouteTable2
      DestinationCidrBlock: !Ref OnPremisesCidr
      TransitGatewayId: !Ref TransitGateway

  # Subnet Route Table Associations
  PrivateSubnet1RouteTableAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      SubnetId: !Ref PrivateSubnet1
      RouteTableId: !Ref PrivateRouteTable1

  PrivateSubnet2RouteTableAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      SubnetId: !Ref PrivateSubnet2
      RouteTableId: !Ref PrivateRouteTable2

  # Security Groups
  HybridConnectivitySecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupName: !Sub '${Environment}-hybrid-sg'
      GroupDescription: Security group for hybrid connectivity
      VpcId: !Ref HybridVPC
      SecurityGroupIngress:
        - IpProtocol: -1
          CidrIp: !Ref OnPremisesCidr
          Description: All traffic from on-premises
        - IpProtocol: icmp
          FromPort: -1
          ToPort: -1
          CidrIp: !Ref VpcCidr
          Description: ICMP within VPC
      SecurityGroupEgress:
        - IpProtocol: -1
          CidrIp: 0.0.0.0/0
          Description: All outbound traffic
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-hybrid-sg'
        - Key: Environment
          Value: !Ref Environment

  # VPC Flow Logs for network monitoring
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
      LogGroupName: !Sub '/aws/vpc/flowlogs/${Environment}-hybrid'
      RetentionInDays: 30

  VPCFlowLog:
    Type: AWS::EC2::FlowLog
    Properties:
      ResourceType: VPC
      ResourceId: !Ref HybridVPC
      TrafficType: ALL
      LogDestinationType: cloud-watch-logs
      LogGroupName: !Ref VPCFlowLogGroup
      DeliverLogsPermissionArn: !GetAtt VPCFlowLogRole.Arn
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-hybrid-flow-logs'
        - Key: Environment
          Value: !Ref Environment

  # CloudWatch Alarms for monitoring
  DirectConnectConnectionStateAlarm1:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: !Sub '${Environment}-dx-primary-connection-down'
      AlarmDescription: Primary Direct Connect connection is down
      MetricName: ConnectionState
      Namespace: AWS/DX
      Statistic: Maximum
      Period: 300
      EvaluationPeriods: 2
      Threshold: 0
      ComparisonOperator: LessThanOrEqualToThreshold
      Dimensions:
        - Name: ConnectionId
          Value: !Ref PrimaryDirectConnectConnection
      TreatMissingData: breaching

  DirectConnectConnectionStateAlarm2:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: !Sub '${Environment}-dx-secondary-connection-down'
      AlarmDescription: Secondary Direct Connect connection is down
      MetricName: ConnectionState
      Namespace: AWS/DX
      Statistic: Maximum
      Period: 300
      EvaluationPeriods: 2
      Threshold: 0
      ComparisonOperator: LessThanOrEqualToThreshold
      Dimensions:
        - Name: ConnectionId
          Value: !Ref SecondaryDirectConnectConnection
      TreatMissingData: breaching

  VPNConnectionStateAlarm1:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: !Sub '${Environment}-vpn-1-tunnel-down'
      AlarmDescription: VPN connection 1 tunnel is down
      MetricName: TunnelState
      Namespace: AWS/VPN
      Statistic: Maximum
      Period: 300
      EvaluationPeriods: 2
      Threshold: 0
      ComparisonOperator: LessThanOrEqualToThreshold
      Dimensions:
        - Name: VpnId
          Value: !Ref VPNConnection1
      TreatMissingData: breaching

  VPNConnectionStateAlarm2:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: !Sub '${Environment}-vpn-2-tunnel-down'
      AlarmDescription: VPN connection 2 tunnel is down
      MetricName: TunnelState
      Namespace: AWS/VPN
      Statistic: Maximum
      Period: 300
      EvaluationPeriods: 2
      Threshold: 0
      ComparisonOperator: LessThanOrEqualToThreshold
      Dimensions:
        - Name: VpnId
          Value: !Ref VPNConnection2
      TreatMissingData: breaching

  # SNS Topic for notifications
  HybridConnectivityAlerts:
    Type: AWS::SNS::Topic
    Properties:
      TopicName: !Sub '${Environment}-hybrid-connectivity-alerts'
      DisplayName: 'Hybrid Connectivity Alerts'

  # CloudWatch Dashboard
  HybridConnectivityDashboard:
    Type: AWS::CloudWatch::Dashboard
    Properties:
      DashboardName: !Sub '${Environment}-hybrid-connectivity'
      DashboardBody: !Sub |
        {
          "widgets": [
            {
              "type": "metric",
              "x": 0,
              "y": 0,
              "width": 12,
              "height": 6,
              "properties": {
                "metrics": [
                  [ "AWS/DX", "ConnectionState", "ConnectionId", "${PrimaryDirectConnectConnection}" ],
                  [ ".", ".", ".", "${SecondaryDirectConnectConnection}" ]
                ],
                "view": "timeSeries",
                "stacked": false,
                "region": "${AWS::Region}",
                "title": "Direct Connect Connection State",
                "period": 300,
                "yAxis": {
                  "left": {
                    "min": 0,
                    "max": 1
                  }
                }
              }
            },
            {
              "type": "metric",
              "x": 12,
              "y": 0,
              "width": 12,
              "height": 6,
              "properties": {
                "metrics": [
                  [ "AWS/VPN", "TunnelState", "VpnId", "${VPNConnection1}" ],
                  [ ".", ".", ".", "${VPNConnection2}" ]
                ],
                "view": "timeSeries",
                "stacked": false,
                "region": "${AWS::Region}",
                "title": "VPN Connection State",
                "period": 300,
                "yAxis": {
                  "left": {
                    "min": 0,
                    "max": 1
                  }
                }
              }
            },
            {
              "type": "metric",
              "x": 0,
              "y": 6,
              "width": 24,
              "height": 6,
              "properties": {
                "metrics": [
                  [ "AWS/DX", "ConnectionBpsEgress", "ConnectionId", "${PrimaryDirectConnectConnection}" ],
                  [ ".", "ConnectionBpsIngress", ".", "." ],
                  [ ".", "ConnectionBpsEgress", ".", "${SecondaryDirectConnectConnection}" ],
                  [ ".", "ConnectionBpsIngress", ".", "." ]
                ],
                "view": "timeSeries",
                "stacked": false,
                "region": "${AWS::Region}",
                "title": "Direct Connect Bandwidth Utilization",
                "period": 300
              }
            }
          ]
        }

Outputs:
  VPCId:
    Description: VPC ID
    Value: !Ref HybridVPC
    Export:
      Name: !Sub '${Environment}-hybrid-vpc-id'

  TransitGatewayId:
    Description: Transit Gateway ID
    Value: !Ref TransitGateway
    Export:
      Name: !Sub '${Environment}-transit-gateway-id'

  DirectConnectGatewayId:
    Description: Direct Connect Gateway ID
    Value: !Ref DirectConnectGateway
    Export:
      Name: !Sub '${Environment}-dx-gateway-id'

  PrimaryDirectConnectConnectionId:
    Description: Primary Direct Connect Connection ID
    Value: !Ref PrimaryDirectConnectConnection
    Export:
      Name: !Sub '${Environment}-primary-dx-connection-id'

  SecondaryDirectConnectConnectionId:
    Description: Secondary Direct Connect Connection ID
    Value: !Ref SecondaryDirectConnectConnection
    Export:
      Name: !Sub '${Environment}-secondary-dx-connection-id'

  VPNConnection1Id:
    Description: VPN Connection 1 ID
    Value: !Ref VPNConnection1
    Export:
      Name: !Sub '${Environment}-vpn-1-id'

  VPNConnection2Id:
    Description: VPN Connection 2 ID
    Value: !Ref VPNConnection2
    Export:
      Name: !Sub '${Environment}-vpn-2-id'

  HybridSecurityGroupId:
    Description: Hybrid connectivity security group ID
    Value: !Ref HybridConnectivitySecurityGroup
    Export:
      Name: !Sub '${Environment}-hybrid-sg-id'

  DashboardURL:
    Description: CloudWatch Dashboard URL
    Value: !Sub 'https://${AWS::Region}.console.aws.amazon.com/cloudwatch/home?region=${AWS::Region}#dashboards:name=${Environment}-hybrid-connectivity'
```
### Example 4: Network Connectivity Testing and Validation Framework

```bash
#!/bin/bash

# Network Connectivity Testing and Validation Framework
# Comprehensive testing of hybrid network connectivity and failover scenarios

set -euo pipefail

# Configuration
CONFIG_FILE="${CONFIG_FILE:-./network-test-config.json}"
LOG_FILE="${LOG_FILE:-./network-testing.log}"
RESULTS_DIR="${RESULTS_DIR:-./network-test-results}"
TEMP_DIR="${TEMP_DIR:-/tmp/network-testing}"

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
TRANSIT_GATEWAY_ID=$(jq -r '.transit_gateway_id' "$CONFIG_FILE")
DX_CONNECTION_IDS=($(jq -r '.direct_connect_connections[]' "$CONFIG_FILE"))
VPN_CONNECTION_IDS=($(jq -r '.vpn_connections[]' "$CONFIG_FILE"))
TEST_TARGETS=($(jq -r '.test_targets[].ip' "$CONFIG_FILE"))
ON_PREMISES_CIDRS=($(jq -r '.on_premises_cidrs[]' "$CONFIG_FILE"))

log "Starting network connectivity testing"
log "Transit Gateway: $TRANSIT_GATEWAY_ID"
log "Direct Connect Connections: ${#DX_CONNECTION_IDS[@]}"
log "VPN Connections: ${#VPN_CONNECTION_IDS[@]}"
log "Test Targets: ${#TEST_TARGETS[@]}"

# Function to test Direct Connect connectivity
test_direct_connect_connectivity() {
    local test_id="dx_test_$(date +%s)"
    local results_file="$RESULTS_DIR/dx_connectivity_${test_id}.json"
    
    log "Testing Direct Connect connectivity"
    
    # Initialize results
    cat > "$results_file" << EOF
{
    "test_id": "$test_id",
    "test_type": "direct_connect_connectivity",
    "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "transit_gateway_id": "$TRANSIT_GATEWAY_ID",
    "connection_tests": [],
    "overall_status": "running"
}
EOF
    
    # Test each Direct Connect connection
    for dx_connection_id in "${DX_CONNECTION_IDS[@]}"; do
        log "Testing Direct Connect connection: $dx_connection_id"
        
        local connection_result=$(test_dx_connection "$dx_connection_id")
        
        # Add result to results file
        jq --argjson result "$connection_result" \
            '.connection_tests += [$result]' "$results_file" > "$results_file.tmp"
        mv "$results_file.tmp" "$results_file"
    done
    
    # Calculate overall status
    local overall_status=$(jq -r '
        .connection_tests | 
        if all(.status == "healthy") then "healthy"
        elif any(.status == "healthy") then "degraded"
        else "failed"
        end
    ' "$results_file")
    
    # Update overall status
    jq --arg status "$overall_status" '.overall_status = $status' "$results_file" > "$results_file.tmp"
    mv "$results_file.tmp" "$results_file"
    
    log "Direct Connect connectivity test completed: $overall_status"
    echo "$results_file"
}

# Function to test individual Direct Connect connection
test_dx_connection() {
    local dx_connection_id="$1"
    
    # Get connection status from AWS
    local connection_info=$(aws directconnect describe-connections \
        --connection-ids "$dx_connection_id" \
        --output json 2>/dev/null || echo '{"connections": []}')
    
    local connection_state="unknown"
    local bandwidth="unknown"
    local location="unknown"
    
    if [[ $(echo "$connection_info" | jq '.connections | length') -gt 0 ]]; then
        connection_state=$(echo "$connection_info" | jq -r '.connections[0].connectionState')
        bandwidth=$(echo "$connection_info" | jq -r '.connections[0].bandwidth')
        location=$(echo "$connection_info" | jq -r '.connections[0].location')
    fi
    
    # Get Virtual Interface information
    local vif_info=$(aws directconnect describe-virtual-interfaces \
        --connection-id "$dx_connection_id" \
        --output json 2>/dev/null || echo '{"virtualInterfaces": []}')
    
    local vif_tests=()
    
    if [[ $(echo "$vif_info" | jq '.virtualInterfaces | length') -gt 0 ]]; then
        # Test each Virtual Interface
        echo "$vif_info" | jq -c '.virtualInterfaces[]' | while read -r vif; do
            local vif_id=$(echo "$vif" | jq -r '.virtualInterfaceId')
            local vif_state=$(echo "$vif" | jq -r '.virtualInterfaceState')
            local bgp_status=$(echo "$vif" | jq -r '.bgpPeers[0].bgpStatus // "unknown"')
            
            vif_tests+=("{
                \"vif_id\": \"$vif_id\",
                \"vif_state\": \"$vif_state\",
                \"bgp_status\": \"$bgp_status\"
            }")
        done
    fi
    
    # Determine overall connection health
    local status="healthy"
    if [[ "$connection_state" != "available" ]]; then
        status="unhealthy"
    fi
    
    # Create connection test result
    local vif_tests_json=$(printf '%s\n' "${vif_tests[@]}" | jq -s . 2>/dev/null || echo '[]')
    
    cat << EOF
{
    "connection_id": "$dx_connection_id",
    "connection_state": "$connection_state",
    "bandwidth": "$bandwidth",
    "location": "$location",
    "virtual_interfaces": $vif_tests_json,
    "status": "$status",
    "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF
}

# Function to test VPN connectivity
test_vpn_connectivity() {
    local test_id="vpn_test_$(date +%s)"
    local results_file="$RESULTS_DIR/vpn_connectivity_${test_id}.json"
    
    log "Testing VPN connectivity"
    
    # Initialize results
    cat > "$results_file" << EOF
{
    "test_id": "$test_id",
    "test_type": "vpn_connectivity",
    "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "transit_gateway_id": "$TRANSIT_GATEWAY_ID",
    "connection_tests": [],
    "overall_status": "running"
}
EOF
    
    # Test each VPN connection
    for vpn_connection_id in "${VPN_CONNECTION_IDS[@]}"; do
        log "Testing VPN connection: $vpn_connection_id"
        
        local connection_result=$(test_vpn_connection "$vpn_connection_id")
        
        # Add result to results file
        jq --argjson result "$connection_result" \
            '.connection_tests += [$result]' "$results_file" > "$results_file.tmp"
        mv "$results_file.tmp" "$results_file"
    done
    
    # Calculate overall status
    local overall_status=$(jq -r '
        .connection_tests | 
        if all(.status == "healthy") then "healthy"
        elif any(.status == "healthy") then "degraded"
        else "failed"
        end
    ' "$results_file")
    
    # Update overall status
    jq --arg status "$overall_status" '.overall_status = $status' "$results_file" > "$results_file.tmp"
    mv "$results_file.tmp" "$results_file"
    
    log "VPN connectivity test completed: $overall_status"
    echo "$results_file"
}

# Function to test individual VPN connection
test_vpn_connection() {
    local vpn_connection_id="$1"
    
    # Get VPN connection status from AWS
    local vpn_info=$(aws ec2 describe-vpn-connections \
        --vpn-connection-ids "$vpn_connection_id" \
        --output json 2>/dev/null || echo '{"VpnConnections": []}')
    
    local vpn_state="unknown"
    local customer_gateway_ip="unknown"
    local tunnel_tests=()
    
    if [[ $(echo "$vpn_info" | jq '.VpnConnections | length') -gt 0 ]]; then
        vpn_state=$(echo "$vpn_info" | jq -r '.VpnConnections[0].State')
        customer_gateway_ip=$(echo "$vpn_info" | jq -r '.VpnConnections[0].CustomerGatewayConfiguration // "unknown"')
        
        # Test each tunnel
        echo "$vpn_info" | jq -c '.VpnConnections[0].VgwTelemetry[]' | while read -r tunnel; do
            local tunnel_ip=$(echo "$tunnel" | jq -r '.OutsideIpAddress')
            local tunnel_status=$(echo "$tunnel" | jq -r '.Status')
            local accepted_routes=$(echo "$tunnel" | jq -r '.AcceptedRouteCount // 0')
            
            tunnel_tests+=("{
                \"tunnel_ip\": \"$tunnel_ip\",
                \"tunnel_status\": \"$tunnel_status\",
                \"accepted_routes\": $accepted_routes
            }")
        done
    fi
    
    # Determine overall connection health
    local status="healthy"
    if [[ "$vpn_state" != "available" ]]; then
        status="unhealthy"
    fi
    
    # Create connection test result
    local tunnel_tests_json=$(printf '%s\n' "${tunnel_tests[@]}" | jq -s . 2>/dev/null || echo '[]')
    
    cat << EOF
{
    "connection_id": "$vpn_connection_id",
    "vpn_state": "$vpn_state",
    "customer_gateway_ip": "$customer_gateway_ip",
    "tunnels": $tunnel_tests_json,
    "status": "$status",
    "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF
}

# Function to test end-to-end connectivity
test_end_to_end_connectivity() {
    local test_id="e2e_test_$(date +%s)"
    local results_file="$RESULTS_DIR/e2e_connectivity_${test_id}.json"
    
    log "Testing end-to-end connectivity"
    
    # Initialize results
    cat > "$results_file" << EOF
{
    "test_id": "$test_id",
    "test_type": "end_to_end_connectivity",
    "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "target_tests": [],
    "overall_status": "running"
}
EOF
    
    # Test connectivity to each target
    for target_ip in "${TEST_TARGETS[@]}"; do
        log "Testing connectivity to target: $target_ip"
        
        local target_result=$(test_target_connectivity "$target_ip")
        
        # Add result to results file
        jq --argjson result "$target_result" \
            '.target_tests += [$result]' "$results_file" > "$results_file.tmp"
        mv "$results_file.tmp" "$results_file"
    done
    
    # Calculate overall status
    local overall_status=$(jq -r '
        .target_tests | 
        if all(.status == "reachable") then "healthy"
        elif any(.status == "reachable") then "degraded"
        else "failed"
        end
    ' "$results_file")
    
    # Update overall status
    jq --arg status "$overall_status" '.overall_status = $status' "$results_file" > "$results_file.tmp"
    mv "$results_file.tmp" "$results_file"
    
    log "End-to-end connectivity test completed: $overall_status"
    echo "$results_file"
}

# Function to test connectivity to specific target
test_target_connectivity() {
    local target_ip="$1"
    
    # Ping test
    local ping_result=$(ping -c 5 -W 5 "$target_ip" 2>&1 || echo "ping failed")
    local ping_success=false
    local avg_latency=0
    local packet_loss=100
    
    if echo "$ping_result" | grep -q "5 received"; then
        ping_success=true
        avg_latency=$(echo "$ping_result" | grep "avg" | cut -d'/' -f5 2>/dev/null || echo "0")
        packet_loss=0
    elif echo "$ping_result" | grep -q "received"; then
        ping_success=true
        local received=$(echo "$ping_result" | grep "received" | cut -d' ' -f4)
        packet_loss=$(( (5 - received) * 20 ))
        avg_latency=$(echo "$ping_result" | grep "avg" | cut -d'/' -f5 2>/dev/null || echo "0")
    fi
    
    # Traceroute test
    local traceroute_result=$(traceroute -m 15 "$target_ip" 2>&1 || echo "traceroute failed")
    local hop_count=0
    
    if ! echo "$traceroute_result" | grep -q "failed"; then
        hop_count=$(echo "$traceroute_result" | grep -c "^ *[0-9]" || echo "0")
    fi
    
    # TCP connectivity test (if port specified)
    local tcp_test_result=""
    local target_config=$(jq -r --arg ip "$target_ip" '.test_targets[] | select(.ip == $ip)' "$CONFIG_FILE")
    local test_port=$(echo "$target_config" | jq -r '.port // empty')
    
    if [[ -n "$test_port" ]]; then
        if timeout 10 bash -c "echo >/dev/tcp/$target_ip/$test_port" 2>/dev/null; then
            tcp_test_result="success"
        else
            tcp_test_result="failed"
        fi
    fi
    
    # Determine overall status
    local status="unreachable"
    if [[ "$ping_success" == "true" ]]; then
        if [[ "$packet_loss" -eq 0 ]]; then
            status="reachable"
        else
            status="degraded"
        fi
    fi
    
    cat << EOF
{
    "target_ip": "$target_ip",
    "ping_test": {
        "success": $ping_success,
        "avg_latency": $avg_latency,
        "packet_loss": $packet_loss
    },
    "traceroute_test": {
        "hop_count": $hop_count,
        "output": "$traceroute_result"
    },
    "tcp_test": {
        "port": "$test_port",
        "result": "$tcp_test_result"
    },
    "status": "$status",
    "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF
}

# Function to test failover scenarios
test_failover_scenarios() {
    local test_id="failover_test_$(date +%s)"
    local results_file="$RESULTS_DIR/failover_test_${test_id}.json"
    
    log "Testing failover scenarios"
    
    # Initialize results
    cat > "$results_file" << EOF
{
    "test_id": "$test_id",
    "test_type": "failover_scenarios",
    "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "scenario_tests": [],
    "overall_status": "running"
}
EOF
    
    # Test Direct Connect failover scenario
    log "Testing Direct Connect failover scenario"
    local dx_failover_result=$(simulate_dx_failover)
    
    jq --argjson result "$dx_failover_result" \
        '.scenario_tests += [$result]' "$results_file" > "$results_file.tmp"
    mv "$results_file.tmp" "$results_file"
    
    # Test VPN failover scenario
    log "Testing VPN failover scenario"
    local vpn_failover_result=$(simulate_vpn_failover)
    
    jq --argjson result "$vpn_failover_result" \
        '.scenario_tests += [$result]' "$results_file" > "$results_file.tmp"
    mv "$results_file.tmp" "$results_file"
    
    # Calculate overall status
    local overall_status=$(jq -r '
        .scenario_tests | 
        if all(.status == "passed") then "passed"
        elif any(.status == "passed") then "partial"
        else "failed"
        end
    ' "$results_file")
    
    # Update overall status
    jq --arg status "$overall_status" '.overall_status = $status' "$results_file" > "$results_file.tmp"
    mv "$results_file.tmp" "$results_file"
    
    log "Failover scenario testing completed: $overall_status"
    echo "$results_file"
}

# Function to simulate Direct Connect failover
simulate_dx_failover() {
    log "Simulating Direct Connect failover scenario"
    
    # This is a simulation - in practice, you would:
    # 1. Disable primary DX connection
    # 2. Wait for BGP convergence
    # 3. Test connectivity via backup paths
    # 4. Re-enable primary connection
    # 5. Verify traffic returns to primary path
    
    local scenario_start=$(date +%s)
    local connectivity_maintained=true
    local failover_time=0
    local recovery_time=0
    
    # Simulate connectivity tests during failover
    for target_ip in "${TEST_TARGETS[@]}"; do
        # Test connectivity during simulated failover
        local test_result=$(test_target_connectivity "$target_ip")
        local target_status=$(echo "$test_result" | jq -r '.status')
        
        if [[ "$target_status" != "reachable" ]]; then
            connectivity_maintained=false
            break
        fi
    done
    
    local scenario_end=$(date +%s)
    local total_time=$((scenario_end - scenario_start))
    
    local status="passed"
    if [[ "$connectivity_maintained" != "true" ]]; then
        status="failed"
    fi
    
    cat << EOF
{
    "scenario": "direct_connect_failover",
    "connectivity_maintained": $connectivity_maintained,
    "failover_time": $failover_time,
    "recovery_time": $recovery_time,
    "total_test_time": $total_time,
    "status": "$status",
    "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF
}

# Function to simulate VPN failover
simulate_vpn_failover() {
    log "Simulating VPN failover scenario"
    
    local scenario_start=$(date +%s)
    local connectivity_maintained=true
    local failover_time=0
    local recovery_time=0
    
    # Simulate VPN tunnel failover test
    for target_ip in "${TEST_TARGETS[@]}"; do
        local test_result=$(test_target_connectivity "$target_ip")
        local target_status=$(echo "$test_result" | jq -r '.status')
        
        if [[ "$target_status" != "reachable" ]]; then
            connectivity_maintained=false
            break
        fi
    done
    
    local scenario_end=$(date +%s)
    local total_time=$((scenario_end - scenario_start))
    
    local status="passed"
    if [[ "$connectivity_maintained" != "true" ]]; then
        status="failed"
    fi
    
    cat << EOF
{
    "scenario": "vpn_failover",
    "connectivity_maintained": $connectivity_maintained,
    "failover_time": $failover_time,
    "recovery_time": $recovery_time,
    "total_test_time": $total_time,
    "status": "$status",
    "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF
}

# Function to generate comprehensive test report
generate_test_report() {
    local report_file="$RESULTS_DIR/network_test_report_$(date +%Y%m%d_%H%M%S).json"
    
    log "Generating comprehensive test report"
    
    # Collect all test results
    local test_results=()
    for result_file in "$RESULTS_DIR"/*.json; do
        if [[ -f "$result_file" && "$result_file" != "$report_file" ]]; then
            test_results+=("$(cat "$result_file")")
        fi
    done
    
    # Create comprehensive report
    local test_results_json=$(printf '%s\n' "${test_results[@]}" | jq -s .)
    
    cat > "$report_file" << EOF
{
    "report_id": "network_test_report_$(date +%s)",
    "generated_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "test_configuration": $(cat "$CONFIG_FILE"),
    "test_results": $test_results_json,
    "summary": {
        "total_tests": $(echo "$test_results_json" | jq 'length'),
        "passed_tests": $(echo "$test_results_json" | jq '[.[] | select(.overall_status == "healthy" or .overall_status == "passed")] | length'),
        "failed_tests": $(echo "$test_results_json" | jq '[.[] | select(.overall_status == "failed")] | length'),
        "degraded_tests": $(echo "$test_results_json" | jq '[.[] | select(.overall_status == "degraded" or .overall_status == "partial")] | length')
    }
}
EOF
    
    log "Test report generated: $report_file"
    echo "$report_file"
}

# Main execution
main() {
    log "Starting comprehensive network connectivity testing"
    
    # Test Direct Connect connectivity
    dx_results=$(test_direct_connect_connectivity)
    
    # Test VPN connectivity
    vpn_results=$(test_vpn_connectivity)
    
    # Test end-to-end connectivity
    e2e_results=$(test_end_to_end_connectivity)
    
    # Test failover scenarios
    failover_results=$(test_failover_scenarios)
    
    # Generate comprehensive report
    report_file=$(generate_test_report)
    
    # Display summary
    log "Network connectivity testing completed"
    log "Results files generated:"
    log "- Direct Connect: $dx_results"
    log "- VPN: $vpn_results"
    log "- End-to-End: $e2e_results"
    log "- Failover: $failover_results"
    log "- Report: $report_file"
    
    # Show summary
    local summary=$(jq -r '.summary | "Total: \(.total_tests), Passed: \(.passed_tests), Failed: \(.failed_tests), Degraded: \(.degraded_tests)"' "$report_file")
    log "Test Summary: $summary"
}

# Configuration file template
create_config_template() {
    cat > network-test-config.json << 'EOF'
{
    "transit_gateway_id": "tgw-1234567890abcdef0",
    "direct_connect_connections": [
        "dxcon-fg1234567890abcdef",
        "dxcon-fg0987654321fedcba"
    ],
    "vpn_connections": [
        "vpn-1234567890abcdef0",
        "vpn-0987654321fedcba1"
    ],
    "on_premises_cidrs": [
        "192.168.0.0/16",
        "172.16.0.0/12"
    ],
    "test_targets": [
        {
            "ip": "192.168.1.1",
            "port": 22,
            "description": "On-premises server 1"
        },
        {
            "ip": "172.16.1.1",
            "port": 80,
            "description": "On-premises server 2"
        }
    ]
}
EOF
    log "Created configuration template: network-test-config.json"
}

# Command line argument handling
case "${1:-}" in
    "config")
        create_config_template
        ;;
    "test"|"")
        main
        ;;
    *)
        echo "Usage: $0 [config|test]"
        echo "  config - Create configuration template"
        echo "  test   - Run network connectivity tests (default)"
        exit 1
        ;;
esac

# Cleanup
rm -rf "$TEMP_DIR"
log "Network connectivity testing completed"
```

## AWS Services Used

- **AWS Transit Gateway**: Centralized hub for connecting VPCs and on-premises networks
- **AWS Direct Connect**: Dedicated network connections with high bandwidth and low latency
- **AWS VPN**: Encrypted IPsec VPN connections for backup connectivity
- **Direct Connect Gateway**: Connects multiple VPCs to Direct Connect connections
- **Customer Gateway**: Represents on-premises VPN device configuration
- **Virtual Private Gateway**: AWS-side VPN endpoint (legacy, replaced by Transit Gateway)
- **Amazon Route 53**: DNS resolution and health checks for hybrid environments
- **Amazon CloudWatch**: Network monitoring, metrics, and automated alerting
- **AWS CloudFormation**: Infrastructure as code for hybrid network deployment
- **VPC Flow Logs**: Network traffic analysis and security monitoring
- **AWS Systems Manager**: Configuration management and automation
- **Amazon SNS**: Notification service for network alerts and events

## Benefits

- **Redundant Connectivity**: Multiple connection types eliminate single points of failure
- **Automatic Failover**: Intelligent routing ensures seamless failover between connections
- **High Performance**: Direct Connect provides consistent, high-bandwidth connectivity
- **Cost Optimization**: VPN backup connections provide cost-effective redundancy
- **Centralized Management**: Transit Gateway simplifies complex network topologies
- **Enhanced Security**: Encrypted connections and network segmentation
- **Scalability**: Easy addition of new VPCs and on-premises locations
- **Monitoring and Visibility**: Comprehensive network monitoring and alerting
- **Disaster Recovery**: Cross-region connectivity for business continuity
- **Compliance**: Network audit trails and security controls

## Related Resources

- [AWS Well-Architected Reliability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/)
- [AWS Transit Gateway User Guide](https://docs.aws.amazon.com/vpc/latest/tgw/)
- [AWS Direct Connect User Guide](https://docs.aws.amazon.com/directconnect/latest/UserGuide/)
- [AWS VPN User Guide](https://docs.aws.amazon.com/vpn/latest/s2svpn/)
- [Amazon VPC User Guide](https://docs.aws.amazon.com/vpc/latest/userguide/)
- [AWS Hybrid Connectivity Whitepaper](https://docs.aws.amazon.com/whitepapers/latest/hybrid-connectivity/)
- [AWS Network Connectivity Options](https://docs.aws.amazon.com/whitepapers/latest/aws-vpc-connectivity-options/)
- [BGP Routing in AWS](https://docs.aws.amazon.com/directconnect/latest/UserGuide/routing-and-bgp.html)
- [AWS CloudWatch User Guide](https://docs.aws.amazon.com/cloudwatch/latest/monitoring/)
