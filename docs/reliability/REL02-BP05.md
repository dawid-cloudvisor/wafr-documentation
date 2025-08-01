---
title: REL02-BP05 - Enforce non-overlapping private IP address ranges in all private address spaces where they are connected
layout: default
parent: REL02 - How do you plan your network topology?
grand_parent: Reliability
nav_order: 5
---

# REL02-BP05: Enforce non-overlapping private IP address ranges in all private address spaces where they are connected

## Overview

Implement strict IP address range management to prevent overlapping CIDR blocks across all connected private address spaces, including VPCs, on-premises networks, and partner networks. Non-overlapping IP ranges are essential for proper routing, network connectivity, and avoiding conflicts that can cause communication failures, security issues, and operational complexity.

## Implementation Steps

### 1. Design Comprehensive IP Address Registry
- Create centralized IP address management (IPAM) system
- Document all existing IP address allocations across environments
- Establish IP address allocation policies and governance
- Implement automated conflict detection and prevention

### 2. Implement Hierarchical IP Address Planning
- Design top-level IP address allocation strategy
- Allocate non-overlapping ranges for different environments and regions
- Reserve address space for future expansion and growth
- Establish standardized subnet sizing and allocation patterns

### 3. Configure Automated IP Conflict Detection
- Deploy automated scanning and validation systems
- Implement real-time conflict detection and alerting
- Create pre-deployment validation checks
- Establish continuous monitoring and compliance reporting

### 4. Establish IP Address Governance Framework
- Create IP address allocation request and approval processes
- Implement change management for IP address modifications
- Establish documentation and audit trail requirements
- Define roles and responsibilities for IP address management

### 5. Deploy Network Connectivity Validation
- Implement automated connectivity testing between networks
- Validate routing table configurations and propagation
- Test end-to-end connectivity across all connected networks
- Monitor network performance and troubleshoot routing issues

### 6. Implement IP Address Lifecycle Management
- Establish IP address reclamation and reuse processes
- Monitor IP address utilization and optimize allocations
- Plan for network migrations and consolidations
- Maintain historical records and change tracking
## Implementation Examples

### Example 1: Intelligent IP Address Management and Conflict Prevention System
```python
import boto3
import json
import logging
import ipaddress
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import concurrent.futures
import threading
from collections import defaultdict

class NetworkType(Enum):
    VPC = "vpc"
    ON_PREMISES = "on_premises"
    PARTNER = "partner"
    TRANSIT_GATEWAY = "transit_gateway"
    DIRECT_CONNECT = "direct_connect"
    VPN = "vpn"

class ConflictSeverity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

@dataclass
class NetworkRange:
    network_id: str
    network_type: NetworkType
    cidr_block: str
    region: str
    environment: str
    owner: str
    description: str
    created_date: str
    last_modified: str
    tags: Dict[str, str]

@dataclass
class IPConflict:
    conflict_id: str
    severity: ConflictSeverity
    network1: NetworkRange
    network2: NetworkRange
    overlap_cidr: str
    detected_date: str
    resolution_status: str
    resolution_notes: str

class IntelligentIPAddressManager:
    def __init__(self, config: Dict):
        self.config = config
        self.ec2 = boto3.client('ec2')
        self.organizations = boto3.client('organizations')
        self.cloudwatch = boto3.client('cloudwatch')
        self.sns = boto3.client('sns')
        self.dynamodb = boto3.resource('dynamodb')
        
        # Initialize IPAM tables
        self.ipam_table = self.dynamodb.Table(
            config.get('ipam_table_name', 'ip-address-management')
        )
        self.conflicts_table = self.dynamodb.Table(
            config.get('conflicts_table_name', 'ip-conflicts')
        )
        
        # Thread lock for concurrent operations
        self.lock = threading.Lock()
        
    def enforce_non_overlapping_ranges(self, enforcement_config: Dict) -> Dict:
        """Enforce non-overlapping IP address ranges across all networks"""
        enforcement_id = f"ip_enforcement_{int(datetime.utcnow().timestamp())}"
        
        enforcement_result = {
            'enforcement_id': enforcement_id,
            'timestamp': datetime.utcnow().isoformat(),
            'enforcement_config': enforcement_config,
            'discovered_networks': {},
            'detected_conflicts': [],
            'resolution_actions': [],
            'compliance_status': {},
            'status': 'initiated'
        }
        
        try:
            # 1. Discover all network ranges
            discovered_networks = self.discover_all_network_ranges(
                enforcement_config.get('discovery_scope', {})
            )
            enforcement_result['discovered_networks'] = discovered_networks
            
            # 2. Detect IP address conflicts
            detected_conflicts = self.detect_ip_address_conflicts(discovered_networks)
            enforcement_result['detected_conflicts'] = detected_conflicts
            
            # 3. Analyze conflict severity and impact
            conflict_analysis = self.analyze_conflict_severity(detected_conflicts)
            enforcement_result['conflict_analysis'] = conflict_analysis
            
            # 4. Generate resolution recommendations
            resolution_actions = self.generate_resolution_recommendations(
                detected_conflicts, discovered_networks
            )
            enforcement_result['resolution_actions'] = resolution_actions
            
            # 5. Implement automated resolutions
            if enforcement_config.get('auto_resolve', False):
                auto_resolution_results = self.implement_automated_resolutions(
                    resolution_actions, enforcement_config
                )
                enforcement_result['auto_resolution_results'] = auto_resolution_results
            
            # 6. Update compliance status
            compliance_status = self.update_compliance_status(
                discovered_networks, detected_conflicts
            )
            enforcement_result['compliance_status'] = compliance_status
            
            enforcement_result['status'] = 'completed'
            
            # Store enforcement results
            self.store_enforcement_results(enforcement_result)
            
            # Send notifications
            self.send_enforcement_notifications(enforcement_result)
            
            return enforcement_result
            
        except Exception as e:
            logging.error(f"IP address enforcement failed: {str(e)}")
            enforcement_result['status'] = 'failed'
            enforcement_result['error'] = str(e)
            return enforcement_result
    
    def discover_all_network_ranges(self, discovery_scope: Dict) -> Dict:
        """Discover all network ranges across different network types"""
        discovered_networks = {
            'vpcs': [],
            'on_premises': [],
            'partner_networks': [],
            'transit_gateways': [],
            'direct_connect': [],
            'vpn_connections': []
        }
        
        try:
            # Discover VPC networks
            if discovery_scope.get('include_vpcs', True):
                vpc_networks = self.discover_vpc_networks(
                    discovery_scope.get('regions', [])
                )
                discovered_networks['vpcs'] = vpc_networks
            
            # Discover on-premises networks
            if discovery_scope.get('include_on_premises', True):
                on_premises_networks = self.discover_on_premises_networks(
                    discovery_scope.get('on_premises_sources', [])
                )
                discovered_networks['on_premises'] = on_premises_networks
            
            # Discover partner networks
            if discovery_scope.get('include_partners', True):
                partner_networks = self.discover_partner_networks(
                    discovery_scope.get('partner_sources', [])
                )
                discovered_networks['partner_networks'] = partner_networks
            
            # Discover Transit Gateway networks
            if discovery_scope.get('include_transit_gateways', True):
                tgw_networks = self.discover_transit_gateway_networks(
                    discovery_scope.get('regions', [])
                )
                discovered_networks['transit_gateways'] = tgw_networks
            
            # Discover Direct Connect networks
            if discovery_scope.get('include_direct_connect', True):
                dx_networks = self.discover_direct_connect_networks()
                discovered_networks['direct_connect'] = dx_networks
            
            # Discover VPN networks
            if discovery_scope.get('include_vpn', True):
                vpn_networks = self.discover_vpn_networks(
                    discovery_scope.get('regions', [])
                )
                discovered_networks['vpn_connections'] = vpn_networks
            
            return discovered_networks
            
        except Exception as e:
            logging.error(f"Network discovery failed: {str(e)}")
            return discovered_networks
    
    def detect_ip_address_conflicts(self, discovered_networks: Dict) -> List[IPConflict]:
        """Detect IP address conflicts between all discovered networks"""
        conflicts = []
        all_networks = []
        
        try:
            # Flatten all networks into a single list
            for network_type, networks in discovered_networks.items():
                for network in networks:
                    network_range = NetworkRange(
                        network_id=network.get('network_id'),
                        network_type=NetworkType(network.get('network_type')),
                        cidr_block=network.get('cidr_block'),
                        region=network.get('region', 'unknown'),
                        environment=network.get('environment', 'unknown'),
                        owner=network.get('owner', 'unknown'),
                        description=network.get('description', ''),
                        created_date=network.get('created_date', ''),
                        last_modified=network.get('last_modified', ''),
                        tags=network.get('tags', {})
                    )
                    all_networks.append(network_range)
            
            # Check for overlaps between all network pairs
            for i, network1 in enumerate(all_networks):
                for j, network2 in enumerate(all_networks[i+1:], i+1):
                    overlap = self.check_cidr_overlap(
                        network1.cidr_block, 
                        network2.cidr_block
                    )
                    
                    if overlap:
                        conflict = IPConflict(
                            conflict_id=f"conflict_{i}_{j}_{int(time.time())}",
                            severity=self.determine_conflict_severity(network1, network2),
                            network1=network1,
                            network2=network2,
                            overlap_cidr=overlap,
                            detected_date=datetime.utcnow().isoformat(),
                            resolution_status='detected',
                            resolution_notes=''
                        )
                        conflicts.append(conflict)
            
            return conflicts
            
        except Exception as e:
            logging.error(f"Conflict detection failed: {str(e)}")
            return conflicts
    
    def check_cidr_overlap(self, cidr1: str, cidr2: str) -> Optional[str]:
        """Check if two CIDR blocks overlap and return the overlapping range"""
        try:
            network1 = ipaddress.ip_network(cidr1, strict=False)
            network2 = ipaddress.ip_network(cidr2, strict=False)
            
            # Check for overlap
            if network1.overlaps(network2):
                # Calculate the overlapping range
                if network1.subnet_of(network2):
                    return str(network1)
                elif network2.subnet_of(network1):
                    return str(network2)
                else:
                    # Find the intersection
                    start_ip = max(network1.network_address, network2.network_address)
                    end_ip = min(network1.broadcast_address, network2.broadcast_address)
                    
                    # Create a network from the overlapping range
                    overlap_network = ipaddress.summarize_address_range(start_ip, end_ip)
                    return str(list(overlap_network)[0])
            
            return None
            
        except Exception as e:
            logging.error(f"CIDR overlap check failed: {str(e)}")
            return None
    
    def determine_conflict_severity(self, network1: NetworkRange, network2: NetworkRange) -> ConflictSeverity:
        """Determine the severity of an IP address conflict"""
        try:
            # Critical: Production networks overlapping
            if (network1.environment == 'production' and 
                network2.environment == 'production'):
                return ConflictSeverity.CRITICAL
            
            # High: Cross-environment overlaps
            if network1.environment != network2.environment:
                return ConflictSeverity.HIGH
            
            # Medium: Same environment, different regions
            if network1.region != network2.region:
                return ConflictSeverity.MEDIUM
            
            # Low: Same environment and region
            return ConflictSeverity.LOW
            
        except Exception as e:
            logging.error(f"Severity determination failed: {str(e)}")
            return ConflictSeverity.MEDIUM
    
    def generate_resolution_recommendations(self, conflicts: List[IPConflict], 
                                          discovered_networks: Dict) -> List[Dict]:
        """Generate recommendations for resolving IP address conflicts"""
        recommendations = []
        
        try:
            for conflict in conflicts:
                recommendation = {
                    'conflict_id': conflict.conflict_id,
                    'severity': conflict.severity.value,
                    'recommended_actions': [],
                    'estimated_effort': 'medium',
                    'business_impact': 'medium',
                    'timeline': '2-4 weeks'
                }
                
                # Generate specific recommendations based on conflict type
                if conflict.severity == ConflictSeverity.CRITICAL:
                    recommendation['recommended_actions'] = [
                        'Immediate isolation of conflicting networks',
                        'Emergency change to non-overlapping CIDR blocks',
                        'Update routing tables and security groups',
                        'Comprehensive connectivity testing'
                    ]
                    recommendation['estimated_effort'] = 'high'
                    recommendation['business_impact'] = 'high'
                    recommendation['timeline'] = 'immediate'
                
                elif conflict.severity == ConflictSeverity.HIGH:
                    recommendation['recommended_actions'] = [
                        'Plan CIDR block migration for one network',
                        'Coordinate with network owners for change window',
                        'Update DNS and service discovery configurations',
                        'Validate cross-network connectivity'
                    ]
                    recommendation['estimated_effort'] = 'high'
                    recommendation['timeline'] = '1-2 weeks'
                
                elif conflict.severity == ConflictSeverity.MEDIUM:
                    recommendation['recommended_actions'] = [
                        'Schedule CIDR block reallocation',
                        'Update network documentation',
                        'Implement monitoring for future conflicts',
                        'Test network connectivity post-change'
                    ]
                    recommendation['timeline'] = '2-4 weeks'
                
                else:  # LOW severity
                    recommendation['recommended_actions'] = [
                        'Document the conflict for future planning',
                        'Monitor for actual connectivity issues',
                        'Plan resolution during next maintenance window',
                        'Update IP address management policies'
                    ]
                    recommendation['estimated_effort'] = 'low'
                    recommendation['business_impact'] = 'low'
                    recommendation['timeline'] = '1-3 months'
                
                recommendations.append(recommendation)
            
            return recommendations
            
        except Exception as e:
            logging.error(f"Resolution recommendation generation failed: {str(e)}")
            return recommendations
```

### Example 2: IP Address Conflict Detection and Prevention Script
```bash
#!/bin/bash

# IP Address Conflict Detection and Prevention Script
# This script discovers and validates non-overlapping IP ranges across all connected networks

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="${SCRIPT_DIR}/ip-conflict-config.json"
LOG_FILE="${SCRIPT_DIR}/ip-conflict-detection.log"
TEMP_DIR=$(mktemp -d)
RESULTS_DIR="${SCRIPT_DIR}/results"

# Create results directory
mkdir -p "$RESULTS_DIR"

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
    
    log "Loading IP conflict detection configuration from $CONFIG_FILE"
    
    # Validate JSON configuration
    if ! jq empty "$CONFIG_FILE" 2>/dev/null; then
        error_exit "Invalid JSON in configuration file"
    fi
    
    # Extract configuration values
    DISCOVERY_REGIONS=$(jq -r '.discovery_regions[]?' "$CONFIG_FILE" | tr '\n' ' ')
    INCLUDE_ON_PREMISES=$(jq -r '.include_on_premises // true' "$CONFIG_FILE")
    INCLUDE_PARTNERS=$(jq -r '.include_partners // false' "$CONFIG_FILE")
    AUTO_RESOLVE=$(jq -r '.auto_resolve // false' "$CONFIG_FILE")
    NOTIFICATION_TOPIC=$(jq -r '.notification_topic // ""' "$CONFIG_FILE")
    
    log "Configuration loaded successfully"
}

# Discover VPC networks
discover_vpc_networks() {
    log "Discovering VPC networks across regions..."
    
    echo "[]" > "$TEMP_DIR/vpc_networks.json"
    
    for region in $DISCOVERY_REGIONS; do
        log "Discovering VPCs in region: $region"
        
        # Get all VPCs in the region
        aws ec2 describe-vpcs \
            --region "$region" \
            --query 'Vpcs[*].{VpcId:VpcId,CidrBlock:CidrBlock,State:State,Tags:Tags}' \
            --output json > "$TEMP_DIR/vpcs_${region}.json"
        
        # Process each VPC
        jq -c '.[]' "$TEMP_DIR/vpcs_${region}.json" | while read -r vpc; do
            VPC_ID=$(echo "$vpc" | jq -r '.VpcId')
            CIDR_BLOCK=$(echo "$vpc" | jq -r '.CidrBlock')
            STATE=$(echo "$vpc" | jq -r '.State')
            
            if [[ "$STATE" == "available" ]]; then
                # Get VPC name from tags
                VPC_NAME=$(echo "$vpc" | jq -r '.Tags[]? | select(.Key=="Name") | .Value // "unnamed"')
                ENVIRONMENT=$(echo "$vpc" | jq -r '.Tags[]? | select(.Key=="Environment") | .Value // "unknown"')
                
                # Create network entry
                NETWORK_ENTRY=$(cat << EOF
{
    "network_id": "$VPC_ID",
    "network_type": "vpc",
    "cidr_block": "$CIDR_BLOCK",
    "region": "$region",
    "environment": "$ENVIRONMENT",
    "name": "$VPC_NAME",
    "owner": "aws",
    "description": "VPC in $region",
    "discovered_date": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF
)
                
                # Add to networks list
                jq --argjson entry "$NETWORK_ENTRY" '. += [$entry]' "$TEMP_DIR/vpc_networks.json" > "$TEMP_DIR/vpc_networks_tmp.json"
                mv "$TEMP_DIR/vpc_networks_tmp.json" "$TEMP_DIR/vpc_networks.json"
                
                log "Discovered VPC: $VPC_ID ($CIDR_BLOCK) in $region"
            fi
        done
    done
    
    VPC_COUNT=$(jq length "$TEMP_DIR/vpc_networks.json")
    log "Discovered $VPC_COUNT VPC networks"
}

# Discover on-premises networks
discover_on_premises_networks() {
    if [[ "$INCLUDE_ON_PREMISES" == "true" ]]; then
        log "Discovering on-premises networks..."
        
        echo "[]" > "$TEMP_DIR/on_premises_networks.json"
        
        # Get on-premises networks from configuration
        if jq -e '.on_premises_networks' "$CONFIG_FILE" > /dev/null; then
            jq '.on_premises_networks[]' "$CONFIG_FILE" | while read -r network; do
                NETWORK_ENTRY=$(echo "$network" | jq --arg discovered_date "$(date -u +%Y-%m-%dT%H:%M:%SZ)" '. + {discovered_date: $discovered_date}')
                
                jq --argjson entry "$NETWORK_ENTRY" '. += [$entry]' "$TEMP_DIR/on_premises_networks.json" > "$TEMP_DIR/on_premises_networks_tmp.json"
                mv "$TEMP_DIR/on_premises_networks_tmp.json" "$TEMP_DIR/on_premises_networks.json"
            done
        fi
        
        # Discover Direct Connect virtual interfaces
        for region in $DISCOVERY_REGIONS; do
            aws directconnect describe-virtual-interfaces \
                --region "$region" \
                --query 'virtualInterfaces[?virtualInterfaceState==`available`].{VirtualInterfaceId:virtualInterfaceId,CustomerAddress:customerAddress,AmazonAddress:amazonAddress,Vlan:vlan}' \
                --output json > "$TEMP_DIR/dx_vifs_${region}.json"
            
            jq -c '.[]' "$TEMP_DIR/dx_vifs_${region}.json" | while read -r vif; do
                VIF_ID=$(echo "$vif" | jq -r '.VirtualInterfaceId')
                CUSTOMER_ADDRESS=$(echo "$vif" | jq -r '.CustomerAddress // ""')
                
                if [[ -n "$CUSTOMER_ADDRESS" && "$CUSTOMER_ADDRESS" != "null" ]]; then
                    # Extract network from customer address (assuming /30 or /31)
                    CUSTOMER_NETWORK=$(echo "$CUSTOMER_ADDRESS" | sed 's/\.[0-9]*\//.0\//' | sed 's/\/3[01]$/\/24/')
                    
                    NETWORK_ENTRY=$(cat << EOF
{
    "network_id": "$VIF_ID",
    "network_type": "on_premises",
    "cidr_block": "$CUSTOMER_NETWORK",
    "region": "$region",
    "environment": "production",
    "name": "Direct Connect VIF $VIF_ID",
    "owner": "customer",
    "description": "On-premises network via Direct Connect",
    "discovered_date": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF
)
                    
                    jq --argjson entry "$NETWORK_ENTRY" '. += [$entry]' "$TEMP_DIR/on_premises_networks.json" > "$TEMP_DIR/on_premises_networks_tmp.json"
                    mv "$TEMP_DIR/on_premises_networks_tmp.json" "$TEMP_DIR/on_premises_networks.json"
                fi
            done
        done
        
        ON_PREMISES_COUNT=$(jq length "$TEMP_DIR/on_premises_networks.json")
        log "Discovered $ON_PREMISES_COUNT on-premises networks"
    else
        echo "[]" > "$TEMP_DIR/on_premises_networks.json"
        log "Skipping on-premises network discovery"
    fi
}

# Discover Transit Gateway networks
discover_transit_gateway_networks() {
    log "Discovering Transit Gateway networks..."
    
    echo "[]" > "$TEMP_DIR/tgw_networks.json"
    
    for region in $DISCOVERY_REGIONS; do
        # Get Transit Gateway route tables
        aws ec2 describe-transit-gateway-route-tables \
            --region "$region" \
            --query 'TransitGatewayRouteTables[?State==`available`].{RouteTableId:TransitGatewayRouteTableId,TransitGatewayId:TransitGatewayId,Tags:Tags}' \
            --output json > "$TEMP_DIR/tgw_route_tables_${region}.json"
        
        jq -c '.[]' "$TEMP_DIR/tgw_route_tables_${region}.json" | while read -r route_table; do
            ROUTE_TABLE_ID=$(echo "$route_table" | jq -r '.RouteTableId')
            TGW_ID=$(echo "$route_table" | jq -r '.TransitGatewayId')
            
            # Get routes from the route table
            aws ec2 search-transit-gateway-routes \
                --region "$region" \
                --transit-gateway-route-table-id "$ROUTE_TABLE_ID" \
                --filters "Name=state,Values=active" \
                --query 'Routes[].DestinationCidrBlock' \
                --output json > "$TEMP_DIR/tgw_routes_${ROUTE_TABLE_ID}.json"
            
            # Process each route
            jq -r '.[]' "$TEMP_DIR/tgw_routes_${ROUTE_TABLE_ID}.json" | while read -r cidr; do
                if [[ "$cidr" != "0.0.0.0/0" && "$cidr" != "::/0" ]]; then
                    NETWORK_ENTRY=$(cat << EOF
{
    "network_id": "${TGW_ID}_${cidr//\//_}",
    "network_type": "transit_gateway",
    "cidr_block": "$cidr",
    "region": "$region",
    "environment": "shared",
    "name": "Transit Gateway Route $cidr",
    "owner": "aws",
    "description": "Transit Gateway routed network",
    "discovered_date": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF
)
                    
                    jq --argjson entry "$NETWORK_ENTRY" '. += [$entry]' "$TEMP_DIR/tgw_networks.json" > "$TEMP_DIR/tgw_networks_tmp.json"
                    mv "$TEMP_DIR/tgw_networks_tmp.json" "$TEMP_DIR/tgw_networks.json"
                fi
            done
        done
    done
    
    TGW_COUNT=$(jq length "$TEMP_DIR/tgw_networks.json")
    log "Discovered $TGW_COUNT Transit Gateway networks"
}

# Detect IP address conflicts
detect_ip_conflicts() {
    log "Detecting IP address conflicts..."
    
    # Combine all discovered networks
    jq -s 'add' "$TEMP_DIR"/*_networks.json > "$TEMP_DIR/all_networks.json"
    
    TOTAL_NETWORKS=$(jq length "$TEMP_DIR/all_networks.json")
    log "Analyzing $TOTAL_NETWORKS total networks for conflicts"
    
    echo "[]" > "$TEMP_DIR/conflicts.json"
    
    # Python script for conflict detection
    python3 << 'EOF'
import json
import ipaddress
import sys
from datetime import datetime

def check_cidr_overlap(cidr1, cidr2):
    try:
        network1 = ipaddress.ip_network(cidr1, strict=False)
        network2 = ipaddress.ip_network(cidr2, strict=False)
        return network1.overlaps(network2)
    except:
        return False

def determine_severity(net1, net2):
    if net1.get('environment') == 'production' and net2.get('environment') == 'production':
        return 'critical'
    elif net1.get('environment') != net2.get('environment'):
        return 'high'
    elif net1.get('region') != net2.get('region'):
        return 'medium'
    else:
        return 'low'

# Load networks
with open('/tmp/tmp.*/all_networks.json', 'r') as f:
    networks = json.load(f)

conflicts = []
conflict_id = 1

for i, net1 in enumerate(networks):
    for j, net2 in enumerate(networks[i+1:], i+1):
        if check_cidr_overlap(net1['cidr_block'], net2['cidr_block']):
            conflict = {
                'conflict_id': f'conflict_{conflict_id:04d}',
                'severity': determine_severity(net1, net2),
                'network1': net1,
                'network2': net2,
                'detected_date': datetime.utcnow().isoformat() + 'Z',
                'status': 'detected'
            }
            conflicts.append(conflict)
            conflict_id += 1

# Save conflicts
with open('/tmp/tmp.*/conflicts.json', 'w') as f:
    json.dump(conflicts, f, indent=2)

print(f"Detected {len(conflicts)} IP address conflicts")
EOF
    
    CONFLICT_COUNT=$(jq length "$TEMP_DIR/conflicts.json")
    log "Detected $CONFLICT_COUNT IP address conflicts"
    
    # Copy results to results directory
    cp "$TEMP_DIR/conflicts.json" "$RESULTS_DIR/conflicts_$(date +%Y%m%d_%H%M%S).json"
    cp "$TEMP_DIR/all_networks.json" "$RESULTS_DIR/networks_$(date +%Y%m%d_%H%M%S).json"
}

# Generate conflict report
generate_conflict_report() {
    log "Generating conflict report..."
    
    REPORT_FILE="$RESULTS_DIR/ip_conflict_report_$(date +%Y%m%d_%H%M%S).html"
    
    cat << 'EOF' > "$REPORT_FILE"
<!DOCTYPE html>
<html>
<head>
    <title>IP Address Conflict Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { background-color: #f0f0f0; padding: 20px; border-radius: 5px; }
        .conflict { margin: 20px 0; padding: 15px; border-left: 4px solid #ff6b6b; background-color: #fff5f5; }
        .conflict.critical { border-left-color: #ff0000; }
        .conflict.high { border-left-color: #ff6b00; }
        .conflict.medium { border-left-color: #ffaa00; }
        .conflict.low { border-left-color: #00aa00; }
        .network-details { background-color: #f9f9f9; padding: 10px; margin: 10px 0; border-radius: 3px; }
        .summary { background-color: #e3f2fd; padding: 15px; border-radius: 5px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="header">
        <h1>IP Address Conflict Detection Report</h1>
        <p>Generated on: $(date)</p>
        <p>Total Networks Analyzed: $(jq length "$TEMP_DIR/all_networks.json")</p>
        <p>Total Conflicts Detected: $(jq length "$TEMP_DIR/conflicts.json")</p>
    </div>
EOF
    
    # Add summary statistics
    cat << EOF >> "$REPORT_FILE"
    <div class="summary">
        <h2>Conflict Summary</h2>
        <ul>
            <li>Critical Conflicts: $(jq '[.[] | select(.severity == "critical")] | length' "$TEMP_DIR/conflicts.json")</li>
            <li>High Severity Conflicts: $(jq '[.[] | select(.severity == "high")] | length' "$TEMP_DIR/conflicts.json")</li>
            <li>Medium Severity Conflicts: $(jq '[.[] | select(.severity == "medium")] | length' "$TEMP_DIR/conflicts.json")</li>
            <li>Low Severity Conflicts: $(jq '[.[] | select(.severity == "low")] | length' "$TEMP_DIR/conflicts.json")</li>
        </ul>
    </div>
EOF
    
    # Add detailed conflicts
    echo "<h2>Detailed Conflicts</h2>" >> "$REPORT_FILE"
    
    jq -c '.[]' "$TEMP_DIR/conflicts.json" | while read -r conflict; do
        CONFLICT_ID=$(echo "$conflict" | jq -r '.conflict_id')
        SEVERITY=$(echo "$conflict" | jq -r '.severity')
        NET1_ID=$(echo "$conflict" | jq -r '.network1.network_id')
        NET1_CIDR=$(echo "$conflict" | jq -r '.network1.cidr_block')
        NET1_TYPE=$(echo "$conflict" | jq -r '.network1.network_type')
        NET2_ID=$(echo "$conflict" | jq -r '.network2.network_id')
        NET2_CIDR=$(echo "$conflict" | jq -r '.network2.cidr_block')
        NET2_TYPE=$(echo "$conflict" | jq -r '.network2.network_type')
        
        cat << EOF >> "$REPORT_FILE"
    <div class="conflict $SEVERITY">
        <h3>Conflict ID: $CONFLICT_ID (Severity: $SEVERITY)</h3>
        <div class="network-details">
            <strong>Network 1:</strong> $NET1_ID ($NET1_TYPE)<br>
            <strong>CIDR Block:</strong> $NET1_CIDR
        </div>
        <div class="network-details">
            <strong>Network 2:</strong> $NET2_ID ($NET2_TYPE)<br>
            <strong>CIDR Block:</strong> $NET2_CIDR
        </div>
    </div>
EOF
    done
    
    echo "</body></html>" >> "$REPORT_FILE"
    
    log "Conflict report generated: $REPORT_FILE"
}

# Send notifications
send_notifications() {
    if [[ -n "$NOTIFICATION_TOPIC" ]]; then
        log "Sending notifications..."
        
        CONFLICT_COUNT=$(jq length "$TEMP_DIR/conflicts.json")
        CRITICAL_COUNT=$(jq '[.[] | select(.severity == "critical")] | length' "$TEMP_DIR/conflicts.json")
        
        MESSAGE="IP Address Conflict Detection Results:
- Total Conflicts: $CONFLICT_COUNT
- Critical Conflicts: $CRITICAL_COUNT
- Report generated at: $(date)
- Check detailed report for resolution recommendations"
        
        aws sns publish \
            --topic-arn "$NOTIFICATION_TOPIC" \
            --subject "IP Address Conflict Detection Report" \
            --message "$MESSAGE"
        
        log "Notifications sent to $NOTIFICATION_TOPIC"
    fi
}

# Main execution
main() {
    log "Starting IP address conflict detection"
    
    # Check prerequisites
    if ! command -v aws &> /dev/null; then
        error_exit "AWS CLI not found. Please install AWS CLI."
    fi
    
    if ! command -v jq &> /dev/null; then
        error_exit "jq not found. Please install jq."
    fi
    
    if ! command -v python3 &> /dev/null; then
        error_exit "Python 3 not found. Please install Python 3."
    fi
    
    # Load configuration
    load_configuration
    
    # Execute detection steps
    case "${1:-detect}" in
        "detect")
            discover_vpc_networks
            discover_on_premises_networks
            discover_transit_gateway_networks
            detect_ip_conflicts
            generate_conflict_report
            send_notifications
            log "IP address conflict detection completed successfully"
            ;;
        "report")
            if [[ -f "$TEMP_DIR/conflicts.json" ]]; then
                generate_conflict_report
            else
                error_exit "No conflict data found. Run detection first."
            fi
            ;;
        "validate")
            log "Validating IP address ranges..."
            # Add validation logic here
            ;;
        *)
            echo "Usage: $0 {detect|report|validate}"
            echo "  detect   - Run full conflict detection (default)"
            echo "  report   - Generate report from existing data"
            echo "  validate - Validate IP address configurations"
            exit 1
            ;;
    esac
}

# Execute main function
main "$@"
```
## AWS Services Used

- **AWS VPC IPAM (IP Address Manager)**: Centralized IP address planning, tracking, and monitoring across AWS accounts
- **Amazon VPC**: Virtual private clouds with CIDR block management and validation
- **AWS Transit Gateway**: Centralized connectivity hub with route table management and conflict detection
- **AWS Direct Connect**: Dedicated network connections with IP address coordination and validation
- **AWS Site-to-Site VPN**: VPN connections with IP address range management and routing
- **Amazon Route 53**: DNS resolution and private hosted zones for network connectivity validation
- **AWS Organizations**: Multi-account IP address coordination and governance
- **Amazon CloudWatch**: Network monitoring, metrics, and automated alerting for IP conflicts
- **AWS Lambda**: Serverless functions for automated IP address validation and conflict detection
- **Amazon DynamoDB**: Storage for IP address registry, conflict tracking, and audit trails
- **Amazon SNS**: Notification service for IP conflict alerts and resolution updates
- **AWS Systems Manager**: Configuration management and automation for IP address policies
- **AWS CloudFormation**: Infrastructure as code for consistent IP address allocation
- **AWS Config**: Configuration compliance monitoring for IP address ranges and network resources
- **VPC Flow Logs**: Network traffic analysis and IP address usage monitoring

## Benefits

- **Prevents Network Conflicts**: Eliminates IP address overlaps that cause routing and connectivity issues
- **Improves Network Reliability**: Ensures proper routing and communication between all connected networks
- **Reduces Operational Complexity**: Centralized IP address management simplifies network operations
- **Enhances Security**: Prevents unintended network access due to IP address conflicts
- **Supports Scalability**: Enables predictable network growth without addressing conflicts
- **Ensures Compliance**: Maintains audit trails and documentation for IP address allocations
- **Facilitates Troubleshooting**: Clear IP address boundaries simplify network problem diagnosis
- **Enables Automation**: Automated conflict detection and prevention reduces manual errors
- **Supports Multi-Cloud**: Consistent IP address management across hybrid and multi-cloud environments
- **Improves Performance**: Optimal routing paths without conflicts enhance network performance

## Related Resources

- [AWS Well-Architected Reliability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/)
- [Non-overlapping IP Address Ranges](https://docs.aws.amazon.com/wellarchitected/latest/framework/rel_planning_network_topology_non_overlap_ip.html)
- [AWS VPC IPAM User Guide](https://docs.aws.amazon.com/vpc/latest/ipam/)
- [Amazon VPC User Guide](https://docs.aws.amazon.com/vpc/latest/userguide/)
- [AWS VPC CIDR Planning](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html)
- [AWS Transit Gateway User Guide](https://docs.aws.amazon.com/vpc/latest/tgw/)
- [AWS Direct Connect User Guide](https://docs.aws.amazon.com/directconnect/latest/UserGuide/)
- [VPC Peering Connection Guide](https://docs.aws.amazon.com/vpc/latest/peering/)
- [AWS Networking Best Practices](https://docs.aws.amazon.com/whitepapers/latest/aws-vpc-connectivity-options/)
- [IP Address Planning for AWS](https://aws.amazon.com/blogs/networking-and-content-delivery/ip-address-planning-for-your-aws-deployment/)
- [Amazon CloudWatch User Guide](https://docs.aws.amazon.com/cloudwatch/latest/monitoring/)
