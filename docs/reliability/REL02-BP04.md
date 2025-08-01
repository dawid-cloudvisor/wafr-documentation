---
title: REL02-BP04 - Prefer hub-and-spoke topologies over many-to-many mesh
layout: default
parent: REL02 - How do you plan your network topology?
grand_parent: Reliability
nav_order: 4
---

# REL02-BP04: Prefer hub-and-spoke topologies over many-to-many mesh

## Overview

Implement hub-and-spoke network topologies to simplify network management, reduce complexity, and improve scalability compared to many-to-many mesh architectures. Hub-and-spoke designs centralize connectivity through a central hub (such as AWS Transit Gateway), making network operations more manageable, cost-effective, and secure while maintaining high availability and performance.

## Implementation Steps

### 1. Design Centralized Hub Architecture
- Deploy AWS Transit Gateway as the central connectivity hub
- Establish hub placement strategy across regions and availability zones
- Design redundant hub architecture for high availability
- Plan hub capacity and performance requirements

### 2. Implement Spoke Network Connections
- Connect VPCs to the central hub using Transit Gateway attachments
- Configure spoke networks with appropriate routing policies
- Implement spoke-to-spoke communication through the hub
- Establish spoke network isolation and segmentation

### 3. Configure Centralized Routing and Security
- Implement centralized routing policies at the hub level
- Deploy security controls and inspection at the hub
- Configure network access control and traffic filtering
- Establish centralized logging and monitoring

### 4. Optimize Network Performance and Cost
- Implement traffic engineering and load balancing
- Configure bandwidth allocation and QoS policies
- Optimize routing paths for performance and cost
- Monitor and tune network performance metrics

### 5. Establish Hub Redundancy and Failover
- Deploy multiple hubs for redundancy and disaster recovery
- Configure automatic failover mechanisms
- Implement cross-region hub connectivity
- Test failover scenarios and recovery procedures

### 6. Implement Centralized Network Management
- Deploy centralized network monitoring and observability
- Establish network configuration management processes
- Implement automated network provisioning and scaling
- Create network documentation and operational procedures

## Implementation Examples

### Example 1: Intelligent Hub-and-Spoke Network Management System
```python
import boto3
import json
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import concurrent.futures
import threading

class NetworkTopologyType(Enum):
    HUB_AND_SPOKE = "hub_and_spoke"
    MESH = "mesh"
    HYBRID = "hybrid"

class HubType(Enum):
    TRANSIT_GATEWAY = "transit_gateway"
    VPC_PEERING = "vpc_peering"
    DIRECT_CONNECT_GATEWAY = "direct_connect_gateway"
    VPN_GATEWAY = "vpn_gateway"

@dataclass
class HubConfiguration:
    hub_id: str
    hub_type: HubType
    region: str
    availability_zones: List[str]
    capacity_gbps: int
    redundancy_enabled: bool
    cross_region_enabled: bool
    security_inspection_enabled: bool

@dataclass
class SpokeConfiguration:
    spoke_id: str
    vpc_id: str
    region: str
    cidr_blocks: List[str]
    hub_attachment_id: str
    routing_policy: str
    security_groups: List[str]
    network_acls: List[str]

class HubAndSpokeNetworkManager:
    def __init__(self, config: Dict):
        self.config = config
        self.ec2 = boto3.client('ec2')
        self.transit_gateway = boto3.client('ec2')
        self.cloudwatch = boto3.client('cloudwatch')
        self.route53 = boto3.client('route53')
        self.sns = boto3.client('sns')
        self.dynamodb = boto3.resource('dynamodb')
        
        # Initialize network topology table
        self.topology_table = self.dynamodb.Table(
            config.get('topology_table_name', 'network-topology-management')
        )
        
    def design_hub_and_spoke_architecture(self, architecture_config: Dict) -> Dict:
        """Design comprehensive hub-and-spoke network architecture"""
        architecture_id = f"hub_spoke_{int(datetime.utcnow().timestamp())}"
        
        architecture_result = {
            'architecture_id': architecture_id,
            'timestamp': datetime.utcnow().isoformat(),
            'architecture_config': architecture_config,
            'hub_configurations': {},
            'spoke_configurations': {},
            'routing_policies': {},
            'performance_metrics': {},
            'status': 'initiated'
        }
        
        try:
            # 1. Analyze current network topology
            current_topology = self.analyze_current_network_topology(
                architecture_config.get('existing_vpcs', [])
            )
            architecture_result['current_topology'] = current_topology
            
            # 2. Design optimal hub placement
            hub_design = self.design_optimal_hub_placement(
                architecture_config, current_topology
            )
            architecture_result['hub_design'] = hub_design
            
            # 3. Configure spoke connections
            spoke_connections = self.configure_spoke_connections(
                hub_design, architecture_config
            )
            architecture_result['spoke_connections'] = spoke_connections
            
            # 4. Implement centralized routing
            routing_configuration = self.implement_centralized_routing(
                hub_design, spoke_connections
            )
            architecture_result['routing_configuration'] = routing_configuration
            
            # 5. Configure security and monitoring
            security_config = self.configure_hub_security_monitoring(
                hub_design, spoke_connections
            )
            architecture_result['security_config'] = security_config
            
            # 6. Validate architecture design
            validation_results = self.validate_architecture_design(architecture_result)
            architecture_result['validation_results'] = validation_results
            
            architecture_result['status'] = 'completed'
            
            # Store architecture configuration
            self.store_architecture_configuration(architecture_result)
            
            # Send notification
            self.send_architecture_notification(architecture_result)
            
            return architecture_result
            
        except Exception as e:
            logging.error(f"Hub-and-spoke architecture design failed: {str(e)}")
            architecture_result['status'] = 'failed'
            architecture_result['error'] = str(e)
            return architecture_result
    def analyze_current_network_topology(self, existing_vpcs: List[str]) -> Dict:
        """Analyze current network topology and identify mesh complexity"""
        topology_analysis = {
            'vpc_count': len(existing_vpcs),
            'peering_connections': [],
            'transit_gateways': [],
            'complexity_score': 0,
            'mesh_connections': 0,
            'hub_candidates': []
        }
        
        try:
            # Analyze VPC peering connections
            peering_response = self.ec2.describe_vpc_peering_connections()
            active_peerings = [
                conn for conn in peering_response['VpcPeeringConnections']
                if conn['Status']['Code'] == 'active'
            ]
            topology_analysis['peering_connections'] = active_peerings
            topology_analysis['mesh_connections'] = len(active_peerings)
            
            # Analyze Transit Gateways
            tgw_response = self.ec2.describe_transit_gateways()
            topology_analysis['transit_gateways'] = tgw_response['TransitGateways']
            
            # Calculate complexity score (mesh = n*(n-1)/2 connections)
            n_vpcs = len(existing_vpcs)
            max_mesh_connections = n_vpcs * (n_vpcs - 1) // 2
            current_connections = len(active_peerings)
            
            if max_mesh_connections > 0:
                complexity_score = (current_connections / max_mesh_connections) * 100
                topology_analysis['complexity_score'] = complexity_score
            
            # Identify hub candidates
            hub_candidates = self.identify_hub_candidates(existing_vpcs, active_peerings)
            topology_analysis['hub_candidates'] = hub_candidates
            
            return topology_analysis
            
        except Exception as e:
            logging.error(f"Network topology analysis failed: {str(e)}")
            return topology_analysis
    
    def design_optimal_hub_placement(self, config: Dict, current_topology: Dict) -> Dict:
        """Design optimal hub placement strategy"""
        hub_design = {
            'primary_hubs': [],
            'secondary_hubs': [],
            'hub_regions': [],
            'redundancy_strategy': {},
            'capacity_planning': {}
        }
        
        try:
            regions = config.get('target_regions', ['us-east-1', 'us-west-2'])
            
            for region in regions:
                # Design primary hub
                primary_hub = {
                    'hub_id': f"tgw-primary-{region}",
                    'region': region,
                    'hub_type': HubType.TRANSIT_GATEWAY.value,
                    'capacity_gbps': config.get('hub_capacity', 50),
                    'availability_zones': self.get_available_azs(region),
                    'redundancy_enabled': True,
                    'cross_region_enabled': True,
                    'security_inspection_enabled': config.get('enable_inspection', True)
                }
                hub_design['primary_hubs'].append(primary_hub)
                
                # Design secondary hub for redundancy
                if config.get('enable_redundancy', True):
                    secondary_hub = {
                        'hub_id': f"tgw-secondary-{region}",
                        'region': region,
                        'hub_type': HubType.TRANSIT_GATEWAY.value,
                        'capacity_gbps': config.get('secondary_hub_capacity', 25),
                        'availability_zones': self.get_available_azs(region),
                        'redundancy_enabled': True,
                        'cross_region_enabled': False,
                        'security_inspection_enabled': False
                    }
                    hub_design['secondary_hubs'].append(secondary_hub)
            
            # Plan cross-region connectivity
            if len(regions) > 1:
                hub_design['cross_region_peering'] = self.plan_cross_region_connectivity(
                    hub_design['primary_hubs']
                )
            
            return hub_design
            
        except Exception as e:
            logging.error(f"Hub placement design failed: {str(e)}")
            return hub_design
    
    def configure_spoke_connections(self, hub_design: Dict, config: Dict) -> Dict:
        """Configure spoke network connections to hubs"""
        spoke_config = {
            'spoke_attachments': [],
            'routing_tables': [],
            'security_policies': [],
            'bandwidth_allocations': {}
        }
        
        try:
            target_vpcs = config.get('target_vpcs', [])
            
            for vpc_config in target_vpcs:
                vpc_id = vpc_config['vpc_id']
                region = vpc_config['region']
                
                # Find appropriate hub for this spoke
                primary_hub = next(
                    (hub for hub in hub_design['primary_hubs'] if hub['region'] == region),
                    None
                )
                
                if primary_hub:
                    spoke_attachment = {
                        'spoke_id': f"spoke-{vpc_id}",
                        'vpc_id': vpc_id,
                        'region': region,
                        'hub_id': primary_hub['hub_id'],
                        'attachment_type': 'vpc',
                        'cidr_blocks': vpc_config.get('cidr_blocks', []),
                        'routing_policy': vpc_config.get('routing_policy', 'isolated'),
                        'bandwidth_limit_mbps': vpc_config.get('bandwidth_limit', 1000),
                        'security_groups': vpc_config.get('security_groups', []),
                        'propagate_routes': vpc_config.get('propagate_routes', True)
                    }
                    spoke_config['spoke_attachments'].append(spoke_attachment)
            
            return spoke_config
            
        except Exception as e:
            logging.error(f"Spoke configuration failed: {str(e)}")
            return spoke_config
```

### Example 2: Hub-and-Spoke Network Deployment Script
```bash
#!/bin/bash

# Hub-and-Spoke Network Topology Deployment Script
# This script automates the deployment of hub-and-spoke network architecture

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="${SCRIPT_DIR}/hub-spoke-config.json"
LOG_FILE="${SCRIPT_DIR}/hub-spoke-deployment.log"
TEMP_DIR=$(mktemp -d)

# Logging function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Error handling
error_exit() {
    log "ERROR: $1"
    cleanup
    exit 1
}

# Cleanup function
cleanup() {
    rm -rf "$TEMP_DIR"
}

# Trap for cleanup
trap cleanup EXIT

# Load configuration
load_configuration() {
    if [[ ! -f "$CONFIG_FILE" ]]; then
        error_exit "Configuration file not found: $CONFIG_FILE"
    fi
    
    log "Loading hub-and-spoke configuration from $CONFIG_FILE"
    
    # Validate JSON configuration
    if ! jq empty "$CONFIG_FILE" 2>/dev/null; then
        error_exit "Invalid JSON in configuration file"
    fi
    
    # Extract key configuration values
    PRIMARY_REGIONS=$(jq -r '.primary_regions[]' "$CONFIG_FILE")
    HUB_CAPACITY=$(jq -r '.hub_capacity // 50' "$CONFIG_FILE")
    ENABLE_REDUNDANCY=$(jq -r '.enable_redundancy // true' "$CONFIG_FILE")
    ENABLE_INSPECTION=$(jq -r '.enable_inspection // true' "$CONFIG_FILE")
    
    log "Configuration loaded successfully"
}

# Deploy Transit Gateway hubs
deploy_transit_gateway_hubs() {
    log "Deploying Transit Gateway hubs..."
    
    for region in $PRIMARY_REGIONS; do
        log "Deploying primary hub in region: $region"
        
        # Create Transit Gateway
        TGW_ID=$(aws ec2 create-transit-gateway \
            --region "$region" \
            --description "Primary hub for region $region" \
            --options DefaultRouteTableAssociation=enable,DefaultRouteTablePropagation=enable \
            --tag-specifications "ResourceType=transit-gateway,Tags=[{Key=Name,Value=primary-hub-$region},{Key=Environment,Value=production},{Key=Purpose,Value=hub-and-spoke}]" \
            --query 'TransitGateway.TransitGatewayId' \
            --output text)
        
        if [[ -z "$TGW_ID" ]]; then
            error_exit "Failed to create Transit Gateway in region $region"
        fi
        
        log "Created Transit Gateway: $TGW_ID in region $region"
        
        # Wait for Transit Gateway to be available
        log "Waiting for Transit Gateway to become available..."
        aws ec2 wait transit-gateway-available \
            --region "$region" \
            --transit-gateway-ids "$TGW_ID"
        
        # Store hub information
        echo "{\"region\": \"$region\", \"hub_id\": \"$TGW_ID\", \"type\": \"primary\"}" >> "$TEMP_DIR/hubs.json"
        
        # Deploy secondary hub if redundancy is enabled
        if [[ "$ENABLE_REDUNDANCY" == "true" ]]; then
            log "Deploying secondary hub in region: $region"
            
            SECONDARY_TGW_ID=$(aws ec2 create-transit-gateway \
                --region "$region" \
                --description "Secondary hub for region $region" \
                --options DefaultRouteTableAssociation=enable,DefaultRouteTablePropagation=enable \
                --tag-specifications "ResourceType=transit-gateway,Tags=[{Key=Name,Value=secondary-hub-$region},{Key=Environment,Value=production},{Key=Purpose,Value=hub-and-spoke-backup}]" \
                --query 'TransitGateway.TransitGatewayId' \
                --output text)
            
            log "Created secondary Transit Gateway: $SECONDARY_TGW_ID in region $region"
            echo "{\"region\": \"$region\", \"hub_id\": \"$SECONDARY_TGW_ID\", \"type\": \"secondary\"}" >> "$TEMP_DIR/hubs.json"
        fi
    done
    
    log "Transit Gateway hubs deployed successfully"
}

# Attach VPCs to hubs
attach_spokes_to_hubs() {
    log "Attaching spoke VPCs to hubs..."
    
    # Get VPCs to attach from configuration
    jq -c '.spoke_vpcs[]' "$CONFIG_FILE" | while read -r vpc_config; do
        VPC_ID=$(echo "$vpc_config" | jq -r '.vpc_id')
        REGION=$(echo "$vpc_config" | jq -r '.region')
        ROUTING_POLICY=$(echo "$vpc_config" | jq -r '.routing_policy // "isolated"')
        
        log "Attaching VPC $VPC_ID in region $REGION"
        
        # Find primary hub for this region
        HUB_ID=$(jq -r --arg region "$REGION" 'select(.region == $region and .type == "primary") | .hub_id' "$TEMP_DIR/hubs.json")
        
        if [[ -z "$HUB_ID" ]]; then
            log "WARNING: No primary hub found for region $REGION, skipping VPC $VPC_ID"
            continue
        fi
        
        # Create VPC attachment
        ATTACHMENT_ID=$(aws ec2 create-transit-gateway-vpc-attachment \
            --region "$REGION" \
            --transit-gateway-id "$HUB_ID" \
            --vpc-id "$VPC_ID" \
            --subnet-ids $(echo "$vpc_config" | jq -r '.subnet_ids[]' | tr '\n' ' ') \
            --tag-specifications "ResourceType=transit-gateway-attachment,Tags=[{Key=Name,Value=spoke-$VPC_ID},{Key=VpcId,Value=$VPC_ID},{Key=RoutingPolicy,Value=$ROUTING_POLICY}]" \
            --query 'TransitGatewayVpcAttachment.TransitGatewayAttachmentId' \
            --output text)
        
        if [[ -z "$ATTACHMENT_ID" ]]; then
            log "WARNING: Failed to attach VPC $VPC_ID to hub $HUB_ID"
            continue
        fi
        
        log "Created VPC attachment: $ATTACHMENT_ID for VPC $VPC_ID"
        
        # Wait for attachment to be available
        aws ec2 wait transit-gateway-attachment-available \
            --region "$REGION" \
            --transit-gateway-attachment-ids "$ATTACHMENT_ID"
        
        # Store attachment information
        echo "{\"vpc_id\": \"$VPC_ID\", \"region\": \"$REGION\", \"hub_id\": \"$HUB_ID\", \"attachment_id\": \"$ATTACHMENT_ID\", \"routing_policy\": \"$ROUTING_POLICY\"}" >> "$TEMP_DIR/attachments.json"
    done
    
    log "Spoke VPC attachments completed"
}

# Configure routing policies
configure_routing_policies() {
    log "Configuring routing policies..."
    
    # Process each attachment and configure routing based on policy
    if [[ -f "$TEMP_DIR/attachments.json" ]]; then
        while read -r attachment; do
            VPC_ID=$(echo "$attachment" | jq -r '.vpc_id')
            REGION=$(echo "$attachment" | jq -r '.region')
            HUB_ID=$(echo "$attachment" | jq -r '.hub_id')
            ATTACHMENT_ID=$(echo "$attachment" | jq -r '.attachment_id')
            ROUTING_POLICY=$(echo "$attachment" | jq -r '.routing_policy')
            
            log "Configuring routing policy '$ROUTING_POLICY' for VPC $VPC_ID"
            
            case "$ROUTING_POLICY" in
                "isolated")
                    # Create isolated route table
                    ROUTE_TABLE_ID=$(aws ec2 create-transit-gateway-route-table \
                        --region "$REGION" \
                        --transit-gateway-id "$HUB_ID" \
                        --tag-specifications "ResourceType=transit-gateway-route-table,Tags=[{Key=Name,Value=isolated-$VPC_ID},{Key=Policy,Value=isolated}]" \
                        --query 'TransitGatewayRouteTable.TransitGatewayRouteTableId' \
                        --output text)
                    
                    # Associate attachment with isolated route table
                    aws ec2 associate-transit-gateway-route-table \
                        --region "$REGION" \
                        --transit-gateway-attachment-id "$ATTACHMENT_ID" \
                        --transit-gateway-route-table-id "$ROUTE_TABLE_ID"
                    ;;
                "shared")
                    # Use default route table for shared connectivity
                    log "Using default route table for shared connectivity"
                    ;;
                "custom")
                    # Implement custom routing logic
                    log "Implementing custom routing policy for VPC $VPC_ID"
                    ;;
            esac
            
        done < "$TEMP_DIR/attachments.json"
    fi
    
    log "Routing policies configured successfully"
}

# Configure cross-region connectivity
configure_cross_region_connectivity() {
    if [[ $(echo "$PRIMARY_REGIONS" | wc -w) -gt 1 ]]; then
        log "Configuring cross-region connectivity..."
        
        # Create peering connections between regional hubs
        REGIONS_ARRAY=($PRIMARY_REGIONS)
        for ((i=0; i<${#REGIONS_ARRAY[@]}; i++)); do
            for ((j=i+1; j<${#REGIONS_ARRAY[@]}; j++)); do
                REGION1=${REGIONS_ARRAY[i]}
                REGION2=${REGIONS_ARRAY[j]}
                
                HUB1=$(jq -r --arg region "$REGION1" 'select(.region == $region and .type == "primary") | .hub_id' "$TEMP_DIR/hubs.json")
                HUB2=$(jq -r --arg region "$REGION2" 'select(.region == $region and .type == "primary") | .hub_id' "$TEMP_DIR/hubs.json")
                
                log "Creating peering between $HUB1 ($REGION1) and $HUB2 ($REGION2)"
                
                PEERING_ID=$(aws ec2 create-transit-gateway-peering-attachment \
                    --region "$REGION1" \
                    --transit-gateway-id "$HUB1" \
                    --peer-transit-gateway-id "$HUB2" \
                    --peer-region "$REGION2" \
                    --tag-specifications "ResourceType=transit-gateway-attachment,Tags=[{Key=Name,Value=cross-region-$REGION1-$REGION2}]" \
                    --query 'TransitGatewayPeeringAttachment.TransitGatewayAttachmentId' \
                    --output text)
                
                log "Created cross-region peering: $PEERING_ID"
            done
        done
        
        log "Cross-region connectivity configured"
    fi
}

# Deploy monitoring and alerting
deploy_monitoring() {
    log "Deploying monitoring and alerting..."
    
    # Create CloudWatch dashboard for hub-and-spoke monitoring
    DASHBOARD_BODY=$(cat << EOF
{
    "widgets": [
        {
            "type": "metric",
            "properties": {
                "metrics": [
                    ["AWS/TransitGateway", "BytesIn"],
                    [".", "BytesOut"],
                    [".", "PacketDropCount"]
                ],
                "period": 300,
                "stat": "Sum",
                "region": "us-east-1",
                "title": "Transit Gateway Traffic"
            }
        }
    ]
}
EOF
)
    
    aws cloudwatch put-dashboard \
        --dashboard-name "HubAndSpokeNetworkMonitoring" \
        --dashboard-body "$DASHBOARD_BODY"
    
    log "Monitoring dashboard deployed"
}

# Main execution
main() {
    log "Starting hub-and-spoke network deployment"
    
    # Check prerequisites
    if ! command -v aws &> /dev/null; then
        error_exit "AWS CLI not found. Please install AWS CLI."
    fi
    
    if ! command -v jq &> /dev/null; then
        error_exit "jq not found. Please install jq."
    fi
    
    # Load configuration
    load_configuration
    
    # Execute deployment steps
    case "${1:-deploy}" in
        "deploy")
            deploy_transit_gateway_hubs
            attach_spokes_to_hubs
            configure_routing_policies
            configure_cross_region_connectivity
            deploy_monitoring
            log "Hub-and-spoke network deployment completed successfully"
            ;;
        "cleanup")
            log "Cleaning up hub-and-spoke network resources..."
            # Add cleanup logic here
            ;;
        "validate")
            log "Validating hub-and-spoke network configuration..."
            # Add validation logic here
            ;;
        *)
            echo "Usage: $0 {deploy|cleanup|validate}"
            echo "  deploy   - Deploy hub-and-spoke network (default)"
            echo "  cleanup  - Clean up network resources"
            echo "  validate - Validate network configuration"
            exit 1
            ;;
    esac
}

# Execute main function
main "$@"
```

## AWS Services Used

- **AWS Transit Gateway**: Central hub for connecting VPCs, on-premises networks, and other AWS services
- **Amazon VPC**: Virtual private clouds that serve as spokes in the hub-and-spoke topology
- **AWS Direct Connect Gateway**: Hub for connecting multiple Direct Connect connections
- **Amazon Route 53**: DNS resolution and traffic routing for hub-and-spoke networks
- **AWS VPN**: Site-to-site VPN connections through the central hub
- **Amazon CloudWatch**: Network monitoring, metrics, and automated alerting for hub performance
- **AWS Lambda**: Serverless functions for automated network management and scaling
- **Amazon DynamoDB**: Storage for network topology configuration and state management
- **Amazon SNS**: Notification service for network events and alerts
- **AWS Systems Manager**: Configuration management and automation for network policies
- **AWS CloudFormation**: Infrastructure as code for consistent hub-and-spoke deployment
- **VPC Flow Logs**: Network traffic analysis and security monitoring
- **AWS Config**: Configuration compliance monitoring for network resources
- **AWS Security Hub**: Centralized security findings and compliance monitoring
## Benefits

- **Simplified Network Management**: Centralized hub reduces complexity compared to many-to-many mesh topologies
- **Improved Scalability**: Easy addition of new spokes without exponential connection growth
- **Cost Optimization**: Reduced number of connections and centralized traffic inspection lower costs
- **Enhanced Security**: Centralized security controls and traffic inspection at the hub level
- **Better Performance**: Optimized routing paths and traffic engineering through central hub
- **Operational Efficiency**: Centralized monitoring, logging, and management of network traffic
- **High Availability**: Hub redundancy and failover capabilities ensure network resilience
- **Compliance**: Centralized security controls and audit trails support regulatory requirements
- **Bandwidth Efficiency**: Shared bandwidth utilization and traffic optimization at the hub
- **Disaster Recovery**: Simplified backup connectivity and cross-region failover scenarios

## Related Resources

- [AWS Well-Architected Reliability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/)
- [AWS Transit Gateway User Guide](https://docs.aws.amazon.com/vpc/latest/tgw/)
- [Hub-and-Spoke Network Topology](https://docs.aws.amazon.com/wellarchitected/latest/framework/rel_planning_network_topology_prefer_hub_and_spoke.html)
- [AWS VPC Connectivity Options](https://docs.aws.amazon.com/whitepapers/latest/aws-vpc-connectivity-options/)
- [Transit Gateway Network Manager](https://docs.aws.amazon.com/vpc/latest/tgw/network-manager.html)
- [AWS Direct Connect Gateway](https://docs.aws.amazon.com/directconnect/latest/UserGuide/direct-connect-gateways.html)
- [VPC Peering vs Transit Gateway](https://docs.aws.amazon.com/vpc/latest/peering/what-is-vpc-peering.html)
- [AWS Networking Best Practices](https://docs.aws.amazon.com/whitepapers/latest/aws-vpc-connectivity-options/)
- [Transit Gateway Route Tables](https://docs.aws.amazon.com/vpc/latest/tgw/tgw-route-tables.html)
- [Amazon CloudWatch User Guide](https://docs.aws.amazon.com/cloudwatch/latest/monitoring/)
