# REL02-BP03: Ensure IP subnet allocation accounts for expansion and availability

## Overview

Design and implement IP subnet allocation strategies that accommodate future growth, multi-AZ deployment requirements, and service expansion while maintaining network isolation and security. This involves careful planning of CIDR blocks, subnet sizing, and address space management to prevent IP exhaustion and enable seamless scaling.

## Implementation Steps

### 1. Design Comprehensive IP Address Strategy
- Plan hierarchical IP addressing scheme for multi-region and multi-account architectures
- Allocate sufficient address space for current and future requirements
- Implement standardized subnet sizing and naming conventions
- Establish IP address management (IPAM) processes and governance

### 2. Implement Multi-AZ Subnet Architecture
- Deploy subnets across multiple Availability Zones for high availability
- Size subnets appropriately for expected workload growth
- Maintain consistent subnet patterns across environments
- Plan for disaster recovery and cross-region expansion

### 3. Establish Network Segmentation Strategy
- Create separate subnets for different tiers (web, application, database)
- Implement security zones with appropriate isolation
- Plan for microservices and container networking requirements
- Design subnets for shared services and infrastructure components

### 4. Configure Dynamic IP Management
- Implement automated subnet creation and management
- Set up IP address monitoring and utilization tracking
- Configure automatic subnet expansion capabilities
- Establish IP address reclamation and optimization processes

### 5. Plan for Service Integration and Expansion
- Reserve address space for AWS managed services
- Plan for VPC peering and Transit Gateway connectivity
- Allocate space for load balancers, NAT gateways, and endpoints
- Design for container orchestration and serverless architectures

### 6. Implement IP Address Governance and Monitoring
- Establish IP address allocation policies and procedures
- Set up monitoring and alerting for subnet utilization
- Implement automated compliance checking and reporting
- Create documentation and change management processes

## Implementation Examples

### Example 1: Intelligent IP Address Planning and Management System
```python
import boto3
import json
import logging
import ipaddress
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import math

class SubnetType(Enum):
    PUBLIC = "public"
    PRIVATE = "private"
    DATABASE = "database"
    TRANSIT_GATEWAY = "transit_gateway"
    LOAD_BALANCER = "load_balancer"
    CONTAINER = "container"
    LAMBDA = "lambda"
    RESERVED = "reserved"

class EnvironmentType(Enum):
    PRODUCTION = "production"
    STAGING = "staging"
    DEVELOPMENT = "development"
    SHARED_SERVICES = "shared_services"

@dataclass
class SubnetPlan:
    subnet_type: SubnetType
    environment: EnvironmentType
    availability_zone: str
    cidr_block: str
    expected_hosts: int
    growth_factor: float
    utilization_threshold: float = 0.8

@dataclass
class IPAllocationStrategy:
    region: str
    vpc_cidr: str
    environment_allocations: Dict[str, str]
    subnet_size_defaults: Dict[str, int]
    growth_projections: Dict[str, float]
    availability_zones: List[str]

class IntelligentIPAddressManager:
    def __init__(self, config: Dict):
        self.config = config
        self.ec2 = boto3.client('ec2')
        self.cloudwatch = boto3.client('cloudwatch')
        self.dynamodb = boto3.resource('dynamodb')
        self.sns = boto3.client('sns')
        
        # Initialize IPAM table
        self.ipam_table = self.dynamodb.Table(config.get('ipam_table_name', 'ip-address-management'))
        
    def design_comprehensive_ip_strategy(self, strategy_config: Dict) -> Dict:
        """Design comprehensive IP address allocation strategy"""
        strategy_id = f"ip_strategy_{int(datetime.utcnow().timestamp())}"
        
        strategy_result = {
            'strategy_id': strategy_id,
            'timestamp': datetime.utcnow().isoformat(),
            'strategy_config': strategy_config,
            'ip_allocations': {},
            'subnet_plans': {},
            'utilization_projections': {},
            'status': 'initiated'
        }
        
        try:
            # 1. Analyze current IP utilization
            current_utilization = self.analyze_current_ip_utilization(
                strategy_config.get('existing_vpcs', [])
            )
            strategy_result['current_utilization'] = current_utilization
            
            # 2. Calculate future requirements
            future_requirements = self.calculate_future_ip_requirements(
                strategy_config, current_utilization
            )
            strategy_result['future_requirements'] = future_requirements
            
            # 3. Design hierarchical IP allocation
            ip_allocations = self.design_hierarchical_ip_allocation(
                strategy_config, future_requirements
            )
            strategy_result['ip_allocations'] = ip_allocations
            
            # 4. Create detailed subnet plans
            subnet_plans = self.create_detailed_subnet_plans(
                ip_allocations, strategy_config
            )
            strategy_result['subnet_plans'] = subnet_plans
            
            # 5. Generate utilization projections
            utilization_projections = self.generate_utilization_projections(
                subnet_plans, strategy_config
            )
            strategy_result['utilization_projections'] = utilization_projections
            
            # 6. Validate and optimize allocation
            validation_result = self.validate_and_optimize_allocation(
                strategy_result
            )
            strategy_result['validation'] = validation_result
            
            strategy_result['status'] = 'completed'
            
        except Exception as e:
            logging.error(f"Error designing IP strategy: {str(e)}")
            strategy_result['status'] = 'failed'
            strategy_result['error'] = str(e)
        
        return strategy_result
    
    def analyze_current_ip_utilization(self, existing_vpcs: List[str]) -> Dict:
        """Analyze current IP address utilization across existing VPCs"""
        utilization_analysis = {
            'vpcs': {},
            'total_allocated_ips': 0,
            'total_used_ips': 0,
            'overall_utilization': 0.0,
            'subnet_utilization': []
        }
        
        try:
            for vpc_id in existing_vpcs:
                vpc_analysis = self.analyze_vpc_utilization(vpc_id)
                utilization_analysis['vpcs'][vpc_id] = vpc_analysis
                
                utilization_analysis['total_allocated_ips'] += vpc_analysis['allocated_ips']
                utilization_analysis['total_used_ips'] += vpc_analysis['used_ips']
            
            # Calculate overall utilization
            if utilization_analysis['total_allocated_ips'] > 0:
                utilization_analysis['overall_utilization'] = (
                    utilization_analysis['total_used_ips'] / 
                    utilization_analysis['total_allocated_ips']
                )
            
        except Exception as e:
            logging.error(f"Error analyzing current utilization: {str(e)}")
        
        return utilization_analysis
    
    def analyze_vpc_utilization(self, vpc_id: str) -> Dict:
        """Analyze IP utilization for a specific VPC"""
        try:
            # Get VPC information
            vpc_response = self.ec2.describe_vpcs(VpcIds=[vpc_id])
            if not vpc_response['Vpcs']:
                return {'error': 'VPC not found'}
            
            vpc = vpc_response['Vpcs'][0]
            vpc_cidr = vpc['CidrBlock']
            vpc_network = ipaddress.IPv4Network(vpc_cidr)
            
            # Get subnets
            subnets_response = self.ec2.describe_subnets(
                Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}]
            )
            
            subnet_analysis = []
            total_allocated = 0
            total_used = 0
            
            for subnet in subnets_response['Subnets']:
                subnet_network = ipaddress.IPv4Network(subnet['CidrBlock'])
                available_ips = subnet_network.num_addresses - 5  # AWS reserves 5 IPs
                used_ips = available_ips - subnet['AvailableIpAddressCount']
                utilization = (used_ips / available_ips) * 100 if available_ips > 0 else 0
                
                subnet_info = {
                    'subnet_id': subnet['SubnetId'],
                    'cidr_block': subnet['CidrBlock'],
                    'availability_zone': subnet['AvailabilityZone'],
                    'available_ips': available_ips,
                    'used_ips': used_ips,
                    'utilization_percentage': utilization,
                    'tags': subnet.get('Tags', [])
                }
                
                subnet_analysis.append(subnet_info)
                total_allocated += available_ips
                total_used += used_ips
            
            return {
                'vpc_id': vpc_id,
                'vpc_cidr': vpc_cidr,
                'total_vpc_ips': vpc_network.num_addresses,
                'allocated_ips': total_allocated,
                'used_ips': total_used,
                'utilization_percentage': (total_used / total_allocated * 100) if total_allocated > 0 else 0,
                'subnets': subnet_analysis
            }
            
        except Exception as e:
            logging.error(f"Error analyzing VPC {vpc_id}: {str(e)}")
            return {'error': str(e)}
    
    def calculate_future_ip_requirements(self, strategy_config: Dict, 
                                       current_utilization: Dict) -> Dict:
        """Calculate future IP address requirements based on growth projections"""
        requirements = {
            'environments': {},
            'services': {},
            'total_requirements': 0,
            'growth_timeline': {}
        }
        
        try:
            # Get growth projections
            growth_projections = strategy_config.get('growth_projections', {})
            planning_horizon = strategy_config.get('planning_horizon_years', 3)
            
            # Calculate requirements by environment
            for env_name, env_config in strategy_config.get('environments', {}).items():
                env_requirements = self.calculate_environment_requirements(
                    env_config, growth_projections, planning_horizon
                )
                requirements['environments'][env_name] = env_requirements
                requirements['total_requirements'] += env_requirements['total_ips']
            
            # Calculate requirements by service type
            for service_name, service_config in strategy_config.get('services', {}).items():
                service_requirements = self.calculate_service_requirements(
                    service_config, growth_projections, planning_horizon
                )
                requirements['services'][service_name] = service_requirements
            
            # Generate growth timeline
            requirements['growth_timeline'] = self.generate_growth_timeline(
                requirements, planning_horizon
            )
            
        except Exception as e:
            logging.error(f"Error calculating future requirements: {str(e)}")
        
        return requirements
    
    def calculate_environment_requirements(self, env_config: Dict, 
                                         growth_projections: Dict, 
                                         planning_horizon: int) -> Dict:
        """Calculate IP requirements for a specific environment"""
        base_requirements = env_config.get('base_ip_requirements', 1000)
        growth_rate = growth_projections.get(env_config.get('name', 'default'), 0.2)
        
        # Calculate compound growth
        future_requirements = base_requirements * ((1 + growth_rate) ** planning_horizon)
        
        # Add buffer for unexpected growth
        buffer_percentage = env_config.get('buffer_percentage', 0.5)
        total_requirements = future_requirements * (1 + buffer_percentage)
        
        return {
            'base_requirements': base_requirements,
            'growth_rate': growth_rate,
            'future_requirements': future_requirements,
            'buffer_percentage': buffer_percentage,
            'total_ips': int(total_requirements),
            'recommended_cidr_size': self.calculate_recommended_cidr_size(total_requirements)
        }
    
    def calculate_service_requirements(self, service_config: Dict,
                                     growth_projections: Dict,
                                     planning_horizon: int) -> Dict:
        """Calculate IP requirements for a specific service"""
        service_type = service_config.get('type', 'general')
        base_instances = service_config.get('base_instances', 10)
        
        # Service-specific multipliers
        service_multipliers = {
            'web': 2,      # Load balancers, auto-scaling
            'app': 3,      # Application servers, middleware
            'database': 1, # Typically fewer instances
            'container': 5, # Container orchestration overhead
            'lambda': 0.1,  # Serverless, minimal IP requirements
            'analytics': 4  # Big data, processing clusters
        }
        
        multiplier = service_multipliers.get(service_type, 2)
        growth_rate = growth_projections.get(service_type, 0.3)
        
        # Calculate future requirements
        future_instances = base_instances * ((1 + growth_rate) ** planning_horizon)
        total_ips = future_instances * multiplier
        
        return {
            'service_type': service_type,
            'base_instances': base_instances,
            'multiplier': multiplier,
            'growth_rate': growth_rate,
            'future_instances': int(future_instances),
            'total_ips': int(total_ips)
        }
    
    def calculate_recommended_cidr_size(self, required_ips: float) -> int:
        """Calculate recommended CIDR block size for required IPs"""
        # Find the smallest CIDR that can accommodate required IPs
        # Account for AWS reserved IPs and growth buffer
        
        required_ips_with_aws_reserved = required_ips + (required_ips * 0.1)  # 10% for AWS overhead
        
        # Find the power of 2 that accommodates the requirement
        cidr_size = 32 - math.ceil(math.log2(required_ips_with_aws_reserved))
        
        # Ensure minimum and maximum bounds
        cidr_size = max(16, min(28, cidr_size))  # Between /16 and /28
        
        return cidr_size
    
    def design_hierarchical_ip_allocation(self, strategy_config: Dict,
                                        future_requirements: Dict) -> Dict:
        """Design hierarchical IP address allocation"""
        allocation_design = {
            'master_cidr': strategy_config.get('master_cidr', '10.0.0.0/8'),
            'regional_allocations': {},
            'environment_allocations': {},
            'service_allocations': {},
            'reserved_blocks': {}
        }
        
        try:
            master_network = ipaddress.IPv4Network(allocation_design['master_cidr'])
            
            # Allocate by region
            regions = strategy_config.get('regions', ['us-east-1'])
            regional_subnets = list(master_network.subnets(new_prefix=12))  # /12 per region
            
            for i, region in enumerate(regions):
                if i < len(regional_subnets):
                    allocation_design['regional_allocations'][region] = str(regional_subnets[i])
            
            # Allocate by environment within each region
            for region, region_cidr in allocation_design['regional_allocations'].items():
                region_network = ipaddress.IPv4Network(region_cidr)
                env_allocations = {}
                
                environments = strategy_config.get('environments', {})
                env_subnets = list(region_network.subnets(new_prefix=14))  # /14 per environment
                
                for i, (env_name, env_config) in enumerate(environments.items()):
                    if i < len(env_subnets):
                        env_allocations[env_name] = str(env_subnets[i])
                
                allocation_design['environment_allocations'][region] = env_allocations
            
            # Reserve blocks for special purposes
            allocation_design['reserved_blocks'] = {
                'transit_gateway': '10.255.0.0/16',
                'direct_connect': '10.254.0.0/16',
                'vpn_connections': '10.253.0.0/16',
                'future_expansion': '10.252.0.0/16'
            }
            
        except Exception as e:
            logging.error(f"Error designing hierarchical allocation: {str(e)}")
        
        return allocation_design
    
    def create_detailed_subnet_plans(self, ip_allocations: Dict, 
                                   strategy_config: Dict) -> Dict:
        """Create detailed subnet plans for each environment and service"""
        subnet_plans = {}
        
        try:
            for region, env_allocations in ip_allocations.get('environment_allocations', {}).items():
                region_plans = {}
                
                for env_name, env_cidr in env_allocations.items():
                    env_network = ipaddress.IPv4Network(env_cidr)
                    env_config = strategy_config.get('environments', {}).get(env_name, {})
                    
                    # Get availability zones for the region
                    azs = self.get_availability_zones(region)
                    
                    # Create subnet plans for this environment
                    env_subnet_plans = self.create_environment_subnet_plans(
                        env_network, env_config, azs, region
                    )
                    
                    region_plans[env_name] = env_subnet_plans
                
                subnet_plans[region] = region_plans
                
        except Exception as e:
            logging.error(f"Error creating subnet plans: {str(e)}")
        
        return subnet_plans
    
    def create_environment_subnet_plans(self, env_network: ipaddress.IPv4Network,
                                      env_config: Dict, azs: List[str], 
                                      region: str) -> Dict:
        """Create subnet plans for a specific environment"""
        subnet_plans = {
            'public_subnets': [],
            'private_subnets': [],
            'database_subnets': [],
            'container_subnets': [],
            'reserved_subnets': []
        }
        
        try:
            # Define subnet types and their allocation percentages
            subnet_allocations = {
                'public': 0.1,      # 10% for public subnets
                'private': 0.6,     # 60% for private subnets
                'database': 0.1,    # 10% for database subnets
                'container': 0.15,  # 15% for container subnets
                'reserved': 0.05    # 5% for future use
            }
            
            # Calculate subnet sizes
            total_ips = env_network.num_addresses
            current_network = env_network
            
            for subnet_type, percentage in subnet_allocations.items():
                required_ips = int(total_ips * percentage)
                subnet_size = 32 - math.ceil(math.log2(required_ips / len(azs)))
                subnet_size = max(20, min(28, subnet_size))  # Between /20 and /28
                
                # Create subnets across AZs
                type_subnets = []
                subnets_iter = current_network.subnets(new_prefix=subnet_size)
                
                for i, az in enumerate(azs):
                    try:
                        subnet_cidr = next(subnets_iter)
                        
                        subnet_plan = SubnetPlan(
                            subnet_type=SubnetType(subnet_type.lower()),
                            environment=EnvironmentType(env_config.get('type', 'development')),
                            availability_zone=az,
                            cidr_block=str(subnet_cidr),
                            expected_hosts=required_ips // len(azs),
                            growth_factor=env_config.get('growth_factor', 1.5),
                            utilization_threshold=env_config.get('utilization_threshold', 0.8)
                        )
                        
                        type_subnets.append(asdict(subnet_plan))
                        
                    except StopIteration:
                        break
                
                subnet_plans[f"{subnet_type}_subnets"] = type_subnets
                
                # Update current network for next allocation
                try:
                    remaining_subnets = list(subnets_iter)
                    if remaining_subnets:
                        current_network = remaining_subnets[0].supernet()
                except:
                    pass
                    
        except Exception as e:
            logging.error(f"Error creating environment subnet plans: {str(e)}")
        
        return subnet_plans
    
    def get_availability_zones(self, region: str) -> List[str]:
        """Get availability zones for a region"""
        try:
            # Create regional EC2 client
            regional_ec2 = boto3.client('ec2', region_name=region)
            
            azs_response = regional_ec2.describe_availability_zones(
                Filters=[{'Name': 'state', 'Values': ['available']}]
            )
            
            return [az['ZoneName'] for az in azs_response['AvailabilityZones'][:3]]
            
        except Exception as e:
            logging.error(f"Error getting AZs for region {region}: {str(e)}")
            return [f"{region}a", f"{region}b", f"{region}c"]  # Fallback
    
    def generate_utilization_projections(self, subnet_plans: Dict, 
                                       strategy_config: Dict) -> Dict:
        """Generate utilization projections for subnet plans"""
        projections = {
            'timeline': [],
            'utilization_by_region': {},
            'capacity_warnings': [],
            'expansion_recommendations': []
        }
        
        try:
            planning_horizon = strategy_config.get('planning_horizon_years', 3)
            
            # Generate monthly projections
            for month in range(planning_horizon * 12):
                month_projection = {
                    'month': month,
                    'date': (datetime.utcnow() + timedelta(days=month * 30)).strftime('%Y-%m'),
                    'regional_utilization': {}
                }
                
                for region, region_plans in subnet_plans.items():
                    region_utilization = self.calculate_monthly_utilization(
                        region_plans, month, strategy_config
                    )
                    month_projection['regional_utilization'][region] = region_utilization
                
                projections['timeline'].append(month_projection)
            
            # Identify capacity warnings
            projections['capacity_warnings'] = self.identify_capacity_warnings(
                projections['timeline']
            )
            
            # Generate expansion recommendations
            projections['expansion_recommendations'] = self.generate_expansion_recommendations(
                subnet_plans, projections['capacity_warnings']
            )
            
        except Exception as e:
            logging.error(f"Error generating utilization projections: {str(e)}")
        
        return projections
    
    def calculate_monthly_utilization(self, region_plans: Dict, month: int,
                                    strategy_config: Dict) -> Dict:
        """Calculate utilization for a specific month"""
        utilization = {
            'total_capacity': 0,
            'projected_usage': 0,
            'utilization_percentage': 0,
            'environment_breakdown': {}
        }
        
        try:
            growth_rate = strategy_config.get('monthly_growth_rate', 0.02)  # 2% per month
            
            for env_name, env_plans in region_plans.items():
                env_capacity = 0
                env_usage = 0
                
                for subnet_type, subnets in env_plans.items():
                    for subnet in subnets:
                        subnet_network = ipaddress.IPv4Network(subnet['cidr_block'])
                        capacity = subnet_network.num_addresses - 5  # AWS reserved
                        
                        # Calculate projected usage with growth
                        base_usage = subnet['expected_hosts']
                        projected_usage = base_usage * ((1 + growth_rate) ** month)
                        
                        env_capacity += capacity
                        env_usage += min(projected_usage, capacity)  # Cap at capacity
                
                utilization['environment_breakdown'][env_name] = {
                    'capacity': env_capacity,
                    'usage': env_usage,
                    'utilization_percentage': (env_usage / env_capacity * 100) if env_capacity > 0 else 0
                }
                
                utilization['total_capacity'] += env_capacity
                utilization['projected_usage'] += env_usage
            
            # Calculate overall utilization
            if utilization['total_capacity'] > 0:
                utilization['utilization_percentage'] = (
                    utilization['projected_usage'] / utilization['total_capacity'] * 100
                )
                
        except Exception as e:
            logging.error(f"Error calculating monthly utilization: {str(e)}")
        
        return utilization
    
    def identify_capacity_warnings(self, timeline: List[Dict]) -> List[Dict]:
        """Identify potential capacity issues from projections"""
        warnings = []
        
        try:
            for projection in timeline:
                for region, utilization in projection['regional_utilization'].items():
                    if utilization['utilization_percentage'] > 80:
                        warnings.append({
                            'region': region,
                            'month': projection['month'],
                            'date': projection['date'],
                            'utilization_percentage': utilization['utilization_percentage'],
                            'severity': 'critical' if utilization['utilization_percentage'] > 90 else 'warning',
                            'message': f"High utilization projected for {region} in {projection['date']}"
                        })
                        
        except Exception as e:
            logging.error(f"Error identifying capacity warnings: {str(e)}")
        
        return warnings
    
    def validate_and_optimize_allocation(self, strategy_result: Dict) -> Dict:
        """Validate and optimize the IP allocation strategy"""
        validation = {
            'validation_checks': [],
            'optimization_recommendations': [],
            'compliance_status': 'compliant',
            'efficiency_score': 0
        }
        
        try:
            # Check for IP conflicts
            conflict_check = self.check_ip_conflicts(strategy_result['ip_allocations'])
            validation['validation_checks'].append(conflict_check)
            
            # Check subnet sizing efficiency
            sizing_check = self.check_subnet_sizing_efficiency(strategy_result['subnet_plans'])
            validation['validation_checks'].append(sizing_check)
            
            # Check growth accommodation
            growth_check = self.check_growth_accommodation(strategy_result['utilization_projections'])
            validation['validation_checks'].append(growth_check)
            
            # Generate optimization recommendations
            validation['optimization_recommendations'] = self.generate_optimization_recommendations(
                validation['validation_checks']
            )
            
            # Calculate efficiency score
            validation['efficiency_score'] = self.calculate_efficiency_score(
                validation['validation_checks']
            )
            
        except Exception as e:
            logging.error(f"Error validating allocation: {str(e)}")
        
        return validation

# Usage example
def main():
    config = {
        'region': 'us-east-1',
        'ipam_table_name': 'ip-address-management'
    }
    
    ip_manager = IntelligentIPAddressManager(config)
    
    # Define IP strategy configuration
    strategy_config = {
        'master_cidr': '10.0.0.0/8',
        'regions': ['us-east-1', 'us-west-2', 'eu-west-1'],
        'planning_horizon_years': 5,
        'monthly_growth_rate': 0.03,
        'environments': {
            'production': {
                'type': 'production',
                'base_ip_requirements': 5000,
                'buffer_percentage': 1.0,
                'growth_factor': 2.0,
                'utilization_threshold': 0.7
            },
            'staging': {
                'type': 'staging',
                'base_ip_requirements': 1000,
                'buffer_percentage': 0.5,
                'growth_factor': 1.5,
                'utilization_threshold': 0.8
            },
            'development': {
                'type': 'development',
                'base_ip_requirements': 500,
                'buffer_percentage': 0.3,
                'growth_factor': 1.2,
                'utilization_threshold': 0.9
            }
        },
        'services': {
            'web_tier': {
                'type': 'web',
                'base_instances': 20
            },
            'app_tier': {
                'type': 'app',
                'base_instances': 50
            },
            'database_tier': {
                'type': 'database',
                'base_instances': 10
            },
            'container_platform': {
                'type': 'container',
                'base_instances': 100
            }
        },
        'growth_projections': {
            'production': 0.4,
            'staging': 0.2,
            'development': 0.1,
            'web': 0.3,
            'app': 0.4,
            'database': 0.2,
            'container': 0.6
        }
    }
    
    # Design comprehensive IP strategy
    result = ip_manager.design_comprehensive_ip_strategy(strategy_config)
    
    print(f"IP Strategy Status: {result['status']}")
    if result['status'] == 'completed':
        print("IP address strategy designed successfully!")
        print(f"Total IP requirements: {result['future_requirements']['total_requirements']}")
        print(f"Efficiency score: {result['validation']['efficiency_score']}")
        
        # Display warnings
        warnings = result['utilization_projections']['capacity_warnings']
        if warnings:
            print(f"Capacity warnings: {len(warnings)}")
            for warning in warnings[:3]:  # Show first 3 warnings
                print(f"- {warning['message']}")
    else:
        print(f"Strategy design failed: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    main()
```
### Example 2: Automated Subnet Management and Expansion System

```python
import boto3
import json
import logging
import ipaddress
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass
import threading
import time

@dataclass
class SubnetMonitoringConfig:
    subnet_id: str
    utilization_threshold: float
    expansion_trigger: float
    max_expansion_size: int
    notification_topic: str

@dataclass
class SubnetExpansionPlan:
    current_subnet: str
    current_utilization: float
    recommended_action: str
    new_subnet_cidr: Optional[str]
    expansion_timeline: str
    estimated_cost: float

class AutomatedSubnetManager:
    def __init__(self, config: Dict):
        self.config = config
        self.ec2 = boto3.client('ec2')
        self.cloudwatch = boto3.client('cloudwatch')
        self.sns = boto3.client('sns')
        self.dynamodb = boto3.resource('dynamodb')
        
        # Initialize monitoring table
        self.monitoring_table = self.dynamodb.Table(
            config.get('monitoring_table_name', 'subnet-monitoring')
        )
        
        # Monitoring state
        self.monitoring_active = False
        self.monitoring_thread = None
        
    def start_automated_subnet_management(self, management_config: Dict) -> Dict:
        """Start automated subnet monitoring and management"""
        try:
            # Initialize subnet monitoring
            self.initialize_subnet_monitoring(management_config)
            
            # Start monitoring thread
            self.monitoring_active = True
            self.monitoring_thread = threading.Thread(
                target=self.monitoring_loop,
                daemon=True
            )
            self.monitoring_thread.start()
            
            # Set up CloudWatch alarms
            self.setup_subnet_utilization_alarms(management_config)
            
            return {
                'status': 'started',
                'monitored_subnets': len(management_config.get('subnets', [])),
                'monitoring_interval': management_config.get('monitoring_interval', 300),
                'timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logging.error(f"Error starting subnet management: {str(e)}")
            return {'status': 'failed', 'error': str(e)}
    
    def initialize_subnet_monitoring(self, management_config: Dict):
        """Initialize monitoring for configured subnets"""
        for subnet_config in management_config.get('subnets', []):
            try:
                # Store monitoring configuration
                monitoring_item = {
                    'subnet_id': subnet_config['subnet_id'],
                    'vpc_id': subnet_config.get('vpc_id', ''),
                    'utilization_threshold': subnet_config.get('utilization_threshold', 0.8),
                    'expansion_trigger': subnet_config.get('expansion_trigger', 0.9),
                    'max_expansion_size': subnet_config.get('max_expansion_size', 1024),
                    'notification_topic': subnet_config.get('notification_topic', ''),
                    'last_check': int(datetime.utcnow().timestamp()),
                    'status': 'monitoring'
                }
                
                self.monitoring_table.put_item(Item=monitoring_item)
                
            except Exception as e:
                logging.error(f"Error initializing monitoring for subnet {subnet_config['subnet_id']}: {str(e)}")
    
    def monitoring_loop(self):
        """Main monitoring loop for subnet utilization"""
        while self.monitoring_active:
            try:
                # Get all monitored subnets
                monitored_subnets = self.get_monitored_subnets()
                
                # Check each subnet
                for subnet_config in monitored_subnets:
                    self.check_subnet_utilization(subnet_config)
                
                # Sleep until next check
                monitoring_interval = self.config.get('monitoring_interval', 300)
                time.sleep(monitoring_interval)
                
            except Exception as e:
                logging.error(f"Error in monitoring loop: {str(e)}")
                time.sleep(60)  # Wait longer on error
    
    def get_monitored_subnets(self) -> List[Dict]:
        """Get list of monitored subnets from DynamoDB"""
        try:
            response = self.monitoring_table.scan(
                FilterExpression='#status = :status',
                ExpressionAttributeNames={'#status': 'status'},
                ExpressionAttributeValues={':status': 'monitoring'}
            )
            
            return response.get('Items', [])
            
        except Exception as e:
            logging.error(f"Error getting monitored subnets: {str(e)}")
            return []
    
    def check_subnet_utilization(self, subnet_config: Dict):
        """Check utilization for a specific subnet"""
        subnet_id = subnet_config['subnet_id']
        
        try:
            # Get current subnet information
            subnet_info = self.get_subnet_info(subnet_id)
            if not subnet_info:
                return
            
            # Calculate utilization
            utilization = self.calculate_subnet_utilization(subnet_info)
            
            # Update monitoring record
            self.update_monitoring_record(subnet_id, utilization)
            
            # Check if action is needed
            utilization_threshold = float(subnet_config.get('utilization_threshold', 0.8))
            expansion_trigger = float(subnet_config.get('expansion_trigger', 0.9))
            
            if utilization >= expansion_trigger:
                # Trigger subnet expansion
                self.trigger_subnet_expansion(subnet_config, subnet_info, utilization)
            elif utilization >= utilization_threshold:
                # Send warning notification
                self.send_utilization_warning(subnet_config, subnet_info, utilization)
            
            # Send metrics to CloudWatch
            self.send_utilization_metrics(subnet_id, utilization)
            
        except Exception as e:
            logging.error(f"Error checking subnet {subnet_id}: {str(e)}")
    
    def get_subnet_info(self, subnet_id: str) -> Optional[Dict]:
        """Get detailed subnet information"""
        try:
            response = self.ec2.describe_subnets(SubnetIds=[subnet_id])
            
            if response['Subnets']:
                subnet = response['Subnets'][0]
                return {
                    'subnet_id': subnet['SubnetId'],
                    'vpc_id': subnet['VpcId'],
                    'cidr_block': subnet['CidrBlock'],
                    'availability_zone': subnet['AvailabilityZone'],
                    'available_ip_count': subnet['AvailableIpAddressCount'],
                    'tags': subnet.get('Tags', [])
                }
            
            return None
            
        except Exception as e:
            logging.error(f"Error getting subnet info for {subnet_id}: {str(e)}")
            return None
    
    def calculate_subnet_utilization(self, subnet_info: Dict) -> float:
        """Calculate subnet IP utilization percentage"""
        try:
            cidr_block = subnet_info['cidr_block']
            available_ips = subnet_info['available_ip_count']
            
            # Calculate total usable IPs (subtract AWS reserved IPs)
            network = ipaddress.IPv4Network(cidr_block)
            total_ips = network.num_addresses - 5  # AWS reserves 5 IPs
            
            # Calculate used IPs
            used_ips = total_ips - available_ips
            
            # Calculate utilization percentage
            utilization = (used_ips / total_ips) * 100 if total_ips > 0 else 0
            
            return utilization
            
        except Exception as e:
            logging.error(f"Error calculating utilization: {str(e)}")
            return 0.0
    
    def trigger_subnet_expansion(self, subnet_config: Dict, subnet_info: Dict, utilization: float):
        """Trigger automated subnet expansion"""
        subnet_id = subnet_config['subnet_id']
        
        try:
            logging.warning(f"Triggering expansion for subnet {subnet_id} (utilization: {utilization:.1f}%)")
            
            # Create expansion plan
            expansion_plan = self.create_subnet_expansion_plan(subnet_config, subnet_info, utilization)
            
            # Execute expansion if auto-expansion is enabled
            if subnet_config.get('auto_expansion_enabled', False):
                expansion_result = self.execute_subnet_expansion(expansion_plan)
                
                # Send success notification
                self.send_expansion_notification(subnet_config, expansion_plan, expansion_result)
            else:
                # Send expansion recommendation
                self.send_expansion_recommendation(subnet_config, expansion_plan)
            
        except Exception as e:
            logging.error(f"Error triggering expansion for subnet {subnet_id}: {str(e)}")
    
    def create_subnet_expansion_plan(self, subnet_config: Dict, subnet_info: Dict, 
                                   utilization: float) -> SubnetExpansionPlan:
        """Create a plan for subnet expansion"""
        try:
            current_cidr = subnet_info['cidr_block']
            vpc_id = subnet_info['vpc_id']
            
            # Analyze VPC for available address space
            available_space = self.analyze_vpc_address_space(vpc_id)
            
            # Determine expansion strategy
            expansion_strategy = self.determine_expansion_strategy(
                current_cidr, available_space, subnet_config
            )
            
            # Calculate estimated cost
            estimated_cost = self.estimate_expansion_cost(expansion_strategy)
            
            return SubnetExpansionPlan(
                current_subnet=current_cidr,
                current_utilization=utilization,
                recommended_action=expansion_strategy['action'],
                new_subnet_cidr=expansion_strategy.get('new_cidr'),
                expansion_timeline=expansion_strategy.get('timeline', 'immediate'),
                estimated_cost=estimated_cost
            )
            
        except Exception as e:
            logging.error(f"Error creating expansion plan: {str(e)}")
            return SubnetExpansionPlan(
                current_subnet=subnet_info['cidr_block'],
                current_utilization=utilization,
                recommended_action='manual_review_required',
                new_subnet_cidr=None,
                expansion_timeline='unknown',
                estimated_cost=0.0
            )
    
    def analyze_vpc_address_space(self, vpc_id: str) -> Dict:
        """Analyze available address space in VPC"""
        try:
            # Get VPC information
            vpc_response = self.ec2.describe_vpcs(VpcIds=[vpc_id])
            if not vpc_response['Vpcs']:
                return {'error': 'VPC not found'}
            
            vpc_cidr = vpc_response['Vpcs'][0]['CidrBlock']
            vpc_network = ipaddress.IPv4Network(vpc_cidr)
            
            # Get all subnets in VPC
            subnets_response = self.ec2.describe_subnets(
                Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}]
            )
            
            # Calculate used address space
            used_networks = []
            for subnet in subnets_response['Subnets']:
                used_networks.append(ipaddress.IPv4Network(subnet['CidrBlock']))
            
            # Find available address space
            available_space = self.find_available_address_space(vpc_network, used_networks)
            
            return {
                'vpc_cidr': vpc_cidr,
                'total_ips': vpc_network.num_addresses,
                'used_networks': [str(net) for net in used_networks],
                'available_space': available_space
            }
            
        except Exception as e:
            logging.error(f"Error analyzing VPC address space: {str(e)}")
            return {'error': str(e)}
    
    def find_available_address_space(self, vpc_network: ipaddress.IPv4Network,
                                   used_networks: List[ipaddress.IPv4Network]) -> List[str]:
        """Find available address space in VPC"""
        try:
            # Sort used networks by network address
            used_networks.sort(key=lambda x: x.network_address)
            
            available_spaces = []
            current_address = vpc_network.network_address
            
            for used_network in used_networks:
                # Check if there's space before this used network
                if current_address < used_network.network_address:
                    # Calculate available space
                    available_size = int(used_network.network_address) - int(current_address)
                    if available_size >= 256:  # At least /24
                        # Find the largest possible subnet
                        available_prefix = 32 - (available_size - 1).bit_length()
                        available_cidr = f"{current_address}/{available_prefix}"
                        available_spaces.append(available_cidr)
                
                # Move current address past this used network
                current_address = used_network.broadcast_address + 1
            
            # Check for space after the last used network
            if current_address <= vpc_network.broadcast_address:
                remaining_size = int(vpc_network.broadcast_address) - int(current_address) + 1
                if remaining_size >= 256:  # At least /24
                    available_prefix = 32 - (remaining_size - 1).bit_length()
                    available_cidr = f"{current_address}/{available_prefix}"
                    available_spaces.append(available_cidr)
            
            return available_spaces
            
        except Exception as e:
            logging.error(f"Error finding available address space: {str(e)}")
            return []
    
    def determine_expansion_strategy(self, current_cidr: str, available_space: Dict,
                                   subnet_config: Dict) -> Dict:
        """Determine the best expansion strategy"""
        try:
            current_network = ipaddress.IPv4Network(current_cidr)
            max_expansion_size = subnet_config.get('max_expansion_size', 1024)
            
            # Strategy 1: Create additional subnet in same AZ
            if available_space.get('available_space'):
                for available_cidr in available_space['available_space']:
                    available_network = ipaddress.IPv4Network(available_cidr)
                    
                    # Check if this space can accommodate our expansion needs
                    if available_network.num_addresses >= max_expansion_size:
                        # Calculate optimal subnet size
                        optimal_size = min(max_expansion_size, available_network.num_addresses // 2)
                        optimal_prefix = 32 - (optimal_size - 1).bit_length()
                        
                        new_subnet_cidr = f"{available_network.network_address}/{optimal_prefix}"
                        
                        return {
                            'action': 'create_additional_subnet',
                            'new_cidr': new_subnet_cidr,
                            'timeline': 'immediate',
                            'method': 'additional_subnet'
                        }
            
            # Strategy 2: Recommend VPC expansion
            return {
                'action': 'expand_vpc_cidr',
                'timeline': 'manual_intervention_required',
                'method': 'vpc_expansion',
                'reason': 'Insufficient address space in current VPC'
            }
            
        except Exception as e:
            logging.error(f"Error determining expansion strategy: {str(e)}")
            return {
                'action': 'manual_review_required',
                'timeline': 'unknown',
                'method': 'manual',
                'error': str(e)
            }
    
    def execute_subnet_expansion(self, expansion_plan: SubnetExpansionPlan) -> Dict:
        """Execute the subnet expansion plan"""
        try:
            if expansion_plan.recommended_action == 'create_additional_subnet':
                return self.create_additional_subnet(expansion_plan)
            elif expansion_plan.recommended_action == 'expand_vpc_cidr':
                return self.request_vpc_expansion(expansion_plan)
            else:
                return {
                    'status': 'skipped',
                    'reason': 'Manual intervention required',
                    'action': expansion_plan.recommended_action
                }
                
        except Exception as e:
            logging.error(f"Error executing expansion: {str(e)}")
            return {'status': 'failed', 'error': str(e)}
    
    def create_additional_subnet(self, expansion_plan: SubnetExpansionPlan) -> Dict:
        """Create an additional subnet for expansion"""
        try:
            # This would create a new subnet in the same VPC
            # For demonstration, we'll return a success response
            
            logging.info(f"Creating additional subnet: {expansion_plan.new_subnet_cidr}")
            
            # In practice, you would:
            # 1. Create the new subnet
            # 2. Configure route tables
            # 3. Update security groups
            # 4. Configure load balancer targets
            # 5. Update auto-scaling groups
            
            return {
                'status': 'success',
                'action': 'additional_subnet_created',
                'new_subnet_cidr': expansion_plan.new_subnet_cidr,
                'estimated_completion': (datetime.utcnow() + timedelta(minutes=30)).isoformat()
            }
            
        except Exception as e:
            logging.error(f"Error creating additional subnet: {str(e)}")
            return {'status': 'failed', 'error': str(e)}
    
    def send_utilization_warning(self, subnet_config: Dict, subnet_info: Dict, utilization: float):
        """Send warning notification for high utilization"""
        try:
            notification_topic = subnet_config.get('notification_topic')
            if not notification_topic:
                return
            
            message = {
                'alert_type': 'subnet_utilization_warning',
                'subnet_id': subnet_info['subnet_id'],
                'vpc_id': subnet_info['vpc_id'],
                'cidr_block': subnet_info['cidr_block'],
                'availability_zone': subnet_info['availability_zone'],
                'utilization_percentage': utilization,
                'threshold': subnet_config.get('utilization_threshold', 0.8) * 100,
                'available_ips': subnet_info['available_ip_count'],
                'timestamp': datetime.utcnow().isoformat(),
                'message': f'Subnet {subnet_info["subnet_id"]} utilization is {utilization:.1f}%'
            }
            
            self.sns.publish(
                TopicArn=notification_topic,
                Subject=f'Subnet Utilization Warning: {subnet_info["subnet_id"]}',
                Message=json.dumps(message, indent=2)
            )
            
        except Exception as e:
            logging.error(f"Error sending utilization warning: {str(e)}")
    
    def send_expansion_notification(self, subnet_config: Dict, expansion_plan: SubnetExpansionPlan,
                                  expansion_result: Dict):
        """Send notification about subnet expansion"""
        try:
            notification_topic = subnet_config.get('notification_topic')
            if not notification_topic:
                return
            
            message = {
                'alert_type': 'subnet_expansion_executed',
                'expansion_plan': {
                    'current_subnet': expansion_plan.current_subnet,
                    'current_utilization': expansion_plan.current_utilization,
                    'recommended_action': expansion_plan.recommended_action,
                    'new_subnet_cidr': expansion_plan.new_subnet_cidr,
                    'estimated_cost': expansion_plan.estimated_cost
                },
                'execution_result': expansion_result,
                'timestamp': datetime.utcnow().isoformat()
            }
            
            self.sns.publish(
                TopicArn=notification_topic,
                Subject='Subnet Expansion Executed',
                Message=json.dumps(message, indent=2)
            )
            
        except Exception as e:
            logging.error(f"Error sending expansion notification: {str(e)}")
    
    def setup_subnet_utilization_alarms(self, management_config: Dict):
        """Set up CloudWatch alarms for subnet utilization"""
        try:
            for subnet_config in management_config.get('subnets', []):
                subnet_id = subnet_config['subnet_id']
                threshold = subnet_config.get('utilization_threshold', 0.8) * 100
                
                # Create CloudWatch alarm
                self.cloudwatch.put_metric_alarm(
                    AlarmName=f'subnet-utilization-{subnet_id}',
                    ComparisonOperator='GreaterThanThreshold',
                    EvaluationPeriods=2,
                    MetricName='SubnetUtilization',
                    Namespace='Custom/Networking',
                    Period=300,
                    Statistic='Average',
                    Threshold=threshold,
                    ActionsEnabled=True,
                    AlarmActions=[
                        subnet_config.get('notification_topic', '')
                    ] if subnet_config.get('notification_topic') else [],
                    AlarmDescription=f'Subnet utilization alarm for {subnet_id}',
                    Dimensions=[
                        {
                            'Name': 'SubnetId',
                            'Value': subnet_id
                        }
                    ],
                    Unit='Percent'
                )
                
        except Exception as e:
            logging.error(f"Error setting up utilization alarms: {str(e)}")
    
    def send_utilization_metrics(self, subnet_id: str, utilization: float):
        """Send utilization metrics to CloudWatch"""
        try:
            self.cloudwatch.put_metric_data(
                Namespace='Custom/Networking',
                MetricData=[
                    {
                        'MetricName': 'SubnetUtilization',
                        'Dimensions': [
                            {
                                'Name': 'SubnetId',
                                'Value': subnet_id
                            }
                        ],
                        'Value': utilization,
                        'Unit': 'Percent',
                        'Timestamp': datetime.utcnow()
                    }
                ]
            )
            
        except Exception as e:
            logging.error(f"Error sending utilization metrics: {str(e)}")

# Usage example
def main():
    config = {
        'region': 'us-east-1',
        'monitoring_table_name': 'subnet-monitoring',
        'monitoring_interval': 300
    }
    
    subnet_manager = AutomatedSubnetManager(config)
    
    # Define subnet management configuration
    management_config = {
        'monitoring_interval': 300,  # 5 minutes
        'subnets': [
            {
                'subnet_id': 'subnet-1234567890abcdef0',
                'vpc_id': 'vpc-1234567890abcdef0',
                'utilization_threshold': 0.8,
                'expansion_trigger': 0.9,
                'max_expansion_size': 2048,
                'auto_expansion_enabled': True,
                'notification_topic': 'arn:aws:sns:us-east-1:123456789012:subnet-alerts'
            },
            {
                'subnet_id': 'subnet-0987654321fedcba1',
                'vpc_id': 'vpc-1234567890abcdef0',
                'utilization_threshold': 0.75,
                'expansion_trigger': 0.85,
                'max_expansion_size': 1024,
                'auto_expansion_enabled': False,
                'notification_topic': 'arn:aws:sns:us-east-1:123456789012:subnet-alerts'
            }
        ]
    }
    
    # Start automated subnet management
    result = subnet_manager.start_automated_subnet_management(management_config)
    
    print(f"Subnet Management Status: {result['status']}")
    if result['status'] == 'started':
        print("Automated subnet management started successfully!")
        print(f"- Monitored subnets: {result['monitored_subnets']}")
        print(f"- Monitoring interval: {result['monitoring_interval']} seconds")
        
        # Keep monitoring running
        try:
            while True:
                time.sleep(60)
        except KeyboardInterrupt:
            print("Stopping subnet management...")
            subnet_manager.monitoring_active = False
    else:
        print(f"Failed to start management: {result.get('error', 'Unknown error')}")

if __name__ == "__main__":
    main()
```
### Example 3: CloudFormation Template for Scalable Multi-AZ Subnet Architecture

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Scalable multi-AZ subnet architecture with expansion capabilities'

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
  
  PublicSubnetSize:
    Type: Number
    Description: Subnet size for public subnets (CIDR suffix)
    Default: 24
    MinValue: 20
    MaxValue: 28
  
  PrivateSubnetSize:
    Type: Number
    Description: Subnet size for private subnets (CIDR suffix)
    Default: 22
    MinValue: 20
    MaxValue: 28
  
  DatabaseSubnetSize:
    Type: Number
    Description: Subnet size for database subnets (CIDR suffix)
    Default: 24
    MinValue: 20
    MaxValue: 28
  
  ContainerSubnetSize:
    Type: Number
    Description: Subnet size for container subnets (CIDR suffix)
    Default: 20
    MinValue: 18
    MaxValue: 24
  
  EnableExpansionReserve:
    Type: String
    Description: Reserve address space for future expansion
    Default: 'true'
    AllowedValues: ['true', 'false']
  
  ExpansionReservePercentage:
    Type: Number
    Description: Percentage of VPC CIDR to reserve for expansion
    Default: 25
    MinValue: 10
    MaxValue: 50

Conditions:
  CreateExpansionReserve: !Equals [!Ref EnableExpansionReserve, 'true']

Resources:
  # VPC
  ScalableVPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: !Ref VpcCidr
      EnableDnsHostnames: true
      EnableDnsSupport: true
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-scalable-vpc'
        - Key: Environment
          Value: !Ref Environment
        - Key: Purpose
          Value: ScalableNetworking

  # Internet Gateway
  InternetGateway:
    Type: AWS::EC2::InternetGateway
    Properties:
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-scalable-igw'
        - Key: Environment
          Value: !Ref Environment

  InternetGatewayAttachment:
    Type: AWS::EC2::VPCGatewayAttachment
    Properties:
      InternetGatewayId: !Ref InternetGateway
      VpcId: !Ref ScalableVPC

  # Public Subnets (Multi-AZ)
  PublicSubnet1:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref ScalableVPC
      AvailabilityZone: !Select [0, !GetAZs '']
      CidrBlock: !Select [0, !Cidr [!Ref VpcCidr, 32, !Ref PublicSubnetSize]]
      MapPublicIpOnLaunch: true
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-public-subnet-1'
        - Key: Environment
          Value: !Ref Environment
        - Key: Type
          Value: Public
        - Key: Tier
          Value: Web

  PublicSubnet2:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref ScalableVPC
      AvailabilityZone: !Select [1, !GetAZs '']
      CidrBlock: !Select [1, !Cidr [!Ref VpcCidr, 32, !Ref PublicSubnetSize]]
      MapPublicIpOnLaunch: true
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-public-subnet-2'
        - Key: Environment
          Value: !Ref Environment
        - Key: Type
          Value: Public
        - Key: Tier
          Value: Web

  PublicSubnet3:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref ScalableVPC
      AvailabilityZone: !Select [2, !GetAZs '']
      CidrBlock: !Select [2, !Cidr [!Ref VpcCidr, 32, !Ref PublicSubnetSize]]
      MapPublicIpOnLaunch: true
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-public-subnet-3'
        - Key: Environment
          Value: !Ref Environment
        - Key: Type
          Value: Public
        - Key: Tier
          Value: Web

  # Private Subnets (Multi-AZ) - Larger for application workloads
  PrivateSubnet1:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref ScalableVPC
      AvailabilityZone: !Select [0, !GetAZs '']
      CidrBlock: !Select [3, !Cidr [!Ref VpcCidr, 32, !Ref PrivateSubnetSize]]
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-private-subnet-1'
        - Key: Environment
          Value: !Ref Environment
        - Key: Type
          Value: Private
        - Key: Tier
          Value: Application

  PrivateSubnet2:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref ScalableVPC
      AvailabilityZone: !Select [1, !GetAZs '']
      CidrBlock: !Select [4, !Cidr [!Ref VpcCidr, 32, !Ref PrivateSubnetSize]]
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-private-subnet-2'
        - Key: Environment
          Value: !Ref Environment
        - Key: Type
          Value: Private
        - Key: Tier
          Value: Application

  PrivateSubnet3:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref ScalableVPC
      AvailabilityZone: !Select [2, !GetAZs '']
      CidrBlock: !Select [5, !Cidr [!Ref VpcCidr, 32, !Ref PrivateSubnetSize]]
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-private-subnet-3'
        - Key: Environment
          Value: !Ref Environment
        - Key: Type
          Value: Private
        - Key: Tier
          Value: Application

  # Database Subnets (Multi-AZ)
  DatabaseSubnet1:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref ScalableVPC
      AvailabilityZone: !Select [0, !GetAZs '']
      CidrBlock: !Select [6, !Cidr [!Ref VpcCidr, 32, !Ref DatabaseSubnetSize]]
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-database-subnet-1'
        - Key: Environment
          Value: !Ref Environment
        - Key: Type
          Value: Database
        - Key: Tier
          Value: Data

  DatabaseSubnet2:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref ScalableVPC
      AvailabilityZone: !Select [1, !GetAZs '']
      CidrBlock: !Select [7, !Cidr [!Ref VpcCidr, 32, !Ref DatabaseSubnetSize]]
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-database-subnet-2'
        - Key: Environment
          Value: !Ref Environment
        - Key: Type
          Value: Database
        - Key: Tier
          Value: Data

  DatabaseSubnet3:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref ScalableVPC
      AvailabilityZone: !Select [2, !GetAZs '']
      CidrBlock: !Select [8, !Cidr [!Ref VpcCidr, 32, !Ref DatabaseSubnetSize]]
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-database-subnet-3'
        - Key: Environment
          Value: !Ref Environment
        - Key: Type
          Value: Database
        - Key: Tier
          Value: Data

  # Container/EKS Subnets (Multi-AZ) - Larger for pod networking
  ContainerSubnet1:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref ScalableVPC
      AvailabilityZone: !Select [0, !GetAZs '']
      CidrBlock: !Select [9, !Cidr [!Ref VpcCidr, 32, !Ref ContainerSubnetSize]]
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-container-subnet-1'
        - Key: Environment
          Value: !Ref Environment
        - Key: Type
          Value: Container
        - Key: Tier
          Value: Container
        - Key: kubernetes.io/role/elb
          Value: '1'

  ContainerSubnet2:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref ScalableVPC
      AvailabilityZone: !Select [1, !GetAZs '']
      CidrBlock: !Select [10, !Cidr [!Ref VpcCidr, 32, !Ref ContainerSubnetSize]]
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-container-subnet-2'
        - Key: Environment
          Value: !Ref Environment
        - Key: Type
          Value: Container
        - Key: Tier
          Value: Container
        - Key: kubernetes.io/role/elb
          Value: '1'

  ContainerSubnet3:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref ScalableVPC
      AvailabilityZone: !Select [2, !GetAZs '']
      CidrBlock: !Select [11, !Cidr [!Ref VpcCidr, 32, !Ref ContainerSubnetSize]]
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-container-subnet-3'
        - Key: Environment
          Value: !Ref Environment
        - Key: Type
          Value: Container
        - Key: Tier
          Value: Container
        - Key: kubernetes.io/role/elb
          Value: '1'

  # Reserved Subnets for Future Expansion
  ReservedSubnet1:
    Type: AWS::EC2::Subnet
    Condition: CreateExpansionReserve
    Properties:
      VpcId: !Ref ScalableVPC
      AvailabilityZone: !Select [0, !GetAZs '']
      CidrBlock: !Select [12, !Cidr [!Ref VpcCidr, 32, 22]]
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-reserved-subnet-1'
        - Key: Environment
          Value: !Ref Environment
        - Key: Type
          Value: Reserved
        - Key: Purpose
          Value: FutureExpansion

  ReservedSubnet2:
    Type: AWS::EC2::Subnet
    Condition: CreateExpansionReserve
    Properties:
      VpcId: !Ref ScalableVPC
      AvailabilityZone: !Select [1, !GetAZs '']
      CidrBlock: !Select [13, !Cidr [!Ref VpcCidr, 32, 22]]
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-reserved-subnet-2'
        - Key: Environment
          Value: !Ref Environment
        - Key: Type
          Value: Reserved
        - Key: Purpose
          Value: FutureExpansion

  ReservedSubnet3:
    Type: AWS::EC2::Subnet
    Condition: CreateExpansionReserve
    Properties:
      VpcId: !Ref ScalableVPC
      AvailabilityZone: !Select [2, !GetAZs '']
      CidrBlock: !Select [14, !Cidr [!Ref VpcCidr, 32, 22]]
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-reserved-subnet-3'
        - Key: Environment
          Value: !Ref Environment
        - Key: Type
          Value: Reserved
        - Key: Purpose
          Value: FutureExpansion

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
      VpcId: !Ref ScalableVPC
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

  # Private Route Tables (one per AZ for high availability)
  PrivateRouteTable1:
    Type: AWS::EC2::RouteTable
    Properties:
      VpcId: !Ref ScalableVPC
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-private-routes-1'
        - Key: Environment
          Value: !Ref Environment

  DefaultPrivateRoute1:
    Type: AWS::EC2::Route
    Properties:
      RouteTableId: !Ref PrivateRouteTable1
      DestinationCidrBlock: 0.0.0.0/0
      NatGatewayId: !Ref NatGateway1

  PrivateRouteTable2:
    Type: AWS::EC2::RouteTable
    Properties:
      VpcId: !Ref ScalableVPC
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-private-routes-2'
        - Key: Environment
          Value: !Ref Environment

  DefaultPrivateRoute2:
    Type: AWS::EC2::Route
    Properties:
      RouteTableId: !Ref PrivateRouteTable2
      DestinationCidrBlock: 0.0.0.0/0
      NatGatewayId: !Ref NatGateway2

  PrivateRouteTable3:
    Type: AWS::EC2::RouteTable
    Properties:
      VpcId: !Ref ScalableVPC
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-private-routes-3'
        - Key: Environment
          Value: !Ref Environment

  DefaultPrivateRoute3:
    Type: AWS::EC2::Route
    Properties:
      RouteTableId: !Ref PrivateRouteTable3
      DestinationCidrBlock: 0.0.0.0/0
      NatGatewayId: !Ref NatGateway3

  # Database Route Tables (isolated)
  DatabaseRouteTable1:
    Type: AWS::EC2::RouteTable
    Properties:
      VpcId: !Ref ScalableVPC
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-database-routes-1'
        - Key: Environment
          Value: !Ref Environment

  DatabaseRouteTable2:
    Type: AWS::EC2::RouteTable
    Properties:
      VpcId: !Ref ScalableVPC
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-database-routes-2'
        - Key: Environment
          Value: !Ref Environment

  DatabaseRouteTable3:
    Type: AWS::EC2::RouteTable
    Properties:
      VpcId: !Ref ScalableVPC
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-database-routes-3'
        - Key: Environment
          Value: !Ref Environment

  # Subnet Route Table Associations
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

  PrivateSubnet1RouteTableAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      RouteTableId: !Ref PrivateRouteTable1
      SubnetId: !Ref PrivateSubnet1

  PrivateSubnet2RouteTableAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      RouteTableId: !Ref PrivateRouteTable2
      SubnetId: !Ref PrivateSubnet2

  PrivateSubnet3RouteTableAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      RouteTableId: !Ref PrivateRouteTable3
      SubnetId: !Ref PrivateSubnet3

  DatabaseSubnet1RouteTableAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      RouteTableId: !Ref DatabaseRouteTable1
      SubnetId: !Ref DatabaseSubnet1

  DatabaseSubnet2RouteTableAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      RouteTableId: !Ref DatabaseRouteTable2
      SubnetId: !Ref DatabaseSubnet2

  DatabaseSubnet3RouteTableAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      RouteTableId: !Ref DatabaseRouteTable3
      SubnetId: !Ref DatabaseSubnet3

  ContainerSubnet1RouteTableAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      RouteTableId: !Ref PrivateRouteTable1
      SubnetId: !Ref ContainerSubnet1

  ContainerSubnet2RouteTableAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      RouteTableId: !Ref PrivateRouteTable2
      SubnetId: !Ref ContainerSubnet2

  ContainerSubnet3RouteTableAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      RouteTableId: !Ref PrivateRouteTable3
      SubnetId: !Ref ContainerSubnet3

  # VPC Endpoints for AWS Services (to reduce NAT Gateway costs)
  S3VPCEndpoint:
    Type: AWS::EC2::VPCEndpoint
    Properties:
      VpcId: !Ref ScalableVPC
      ServiceName: !Sub 'com.amazonaws.${AWS::Region}.s3'
      VpcEndpointType: Gateway
      RouteTableIds:
        - !Ref PrivateRouteTable1
        - !Ref PrivateRouteTable2
        - !Ref PrivateRouteTable3
        - !Ref DatabaseRouteTable1
        - !Ref DatabaseRouteTable2
        - !Ref DatabaseRouteTable3

  DynamoDBVPCEndpoint:
    Type: AWS::EC2::VPCEndpoint
    Properties:
      VpcId: !Ref ScalableVPC
      ServiceName: !Sub 'com.amazonaws.${AWS::Region}.dynamodb'
      VpcEndpointType: Gateway
      RouteTableIds:
        - !Ref PrivateRouteTable1
        - !Ref PrivateRouteTable2
        - !Ref PrivateRouteTable3

  # Security Groups
  WebTierSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupName: !Sub '${Environment}-web-tier-sg'
      GroupDescription: Security group for web tier
      VpcId: !Ref ScalableVPC
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
          Value: !Sub '${Environment}-web-tier-sg'
        - Key: Environment
          Value: !Ref Environment

  AppTierSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupName: !Sub '${Environment}-app-tier-sg'
      GroupDescription: Security group for application tier
      VpcId: !Ref ScalableVPC
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 8080
          ToPort: 8080
          SourceSecurityGroupId: !Ref WebTierSecurityGroup
          Description: Application port from web tier
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-app-tier-sg'
        - Key: Environment
          Value: !Ref Environment

  DatabaseTierSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupName: !Sub '${Environment}-database-tier-sg'
      GroupDescription: Security group for database tier
      VpcId: !Ref ScalableVPC
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 3306
          ToPort: 3306
          SourceSecurityGroupId: !Ref AppTierSecurityGroup
          Description: MySQL from application tier
        - IpProtocol: tcp
          FromPort: 5432
          ToPort: 5432
          SourceSecurityGroupId: !Ref AppTierSecurityGroup
          Description: PostgreSQL from application tier
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-database-tier-sg'
        - Key: Environment
          Value: !Ref Environment

  ContainerSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupName: !Sub '${Environment}-container-sg'
      GroupDescription: Security group for container workloads
      VpcId: !Ref ScalableVPC
      SecurityGroupIngress:
        - IpProtocol: -1
          SourceSecurityGroupId: !Ref ContainerSecurityGroup
          Description: All traffic from same security group
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-container-sg'
        - Key: Environment
          Value: !Ref Environment

  # DB Subnet Group
  DatabaseSubnetGroup:
    Type: AWS::RDS::DBSubnetGroup
    Properties:
      DBSubnetGroupName: !Sub '${Environment}-database-subnet-group'
      DBSubnetGroupDescription: Subnet group for RDS databases
      SubnetIds:
        - !Ref DatabaseSubnet1
        - !Ref DatabaseSubnet2
        - !Ref DatabaseSubnet3
      Tags:
        - Key: Name
          Value: !Sub '${Environment}-database-subnet-group'
        - Key: Environment
          Value: !Ref Environment

Outputs:
  VPCId:
    Description: VPC ID
    Value: !Ref ScalableVPC
    Export:
      Name: !Sub '${Environment}-scalable-vpc-id'

  VPCCidr:
    Description: VPC CIDR block
    Value: !Ref VpcCidr
    Export:
      Name: !Sub '${Environment}-vpc-cidr'

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

  DatabaseSubnets:
    Description: Database subnet IDs
    Value: !Join
      - ','
      - - !Ref DatabaseSubnet1
        - !Ref DatabaseSubnet2
        - !Ref DatabaseSubnet3
    Export:
      Name: !Sub '${Environment}-database-subnets'

  ContainerSubnets:
    Description: Container subnet IDs
    Value: !Join
      - ','
      - - !Ref ContainerSubnet1
        - !Ref ContainerSubnet2
        - !Ref ContainerSubnet3
    Export:
      Name: !Sub '${Environment}-container-subnets'

  ReservedSubnets:
    Condition: CreateExpansionReserve
    Description: Reserved subnet IDs for future expansion
    Value: !Join
      - ','
      - - !Ref ReservedSubnet1
        - !Ref ReservedSubnet2
        - !Ref ReservedSubnet3
    Export:
      Name: !Sub '${Environment}-reserved-subnets'

  DatabaseSubnetGroup:
    Description: Database subnet group name
    Value: !Ref DatabaseSubnetGroup
    Export:
      Name: !Sub '${Environment}-database-subnet-group'

  WebTierSecurityGroup:
    Description: Web tier security group ID
    Value: !Ref WebTierSecurityGroup
    Export:
      Name: !Sub '${Environment}-web-tier-sg'

  AppTierSecurityGroup:
    Description: Application tier security group ID
    Value: !Ref AppTierSecurityGroup
    Export:
      Name: !Sub '${Environment}-app-tier-sg'

  DatabaseTierSecurityGroup:
    Description: Database tier security group ID
    Value: !Ref DatabaseTierSecurityGroup
    Export:
      Name: !Sub '${Environment}-database-tier-sg'

  ContainerSecurityGroup:
    Description: Container security group ID
    Value: !Ref ContainerSecurityGroup
    Export:
      Name: !Sub '${Environment}-container-sg'

  AvailabilityZones:
    Description: Availability zones used
    Value: !Join
      - ','
      - - !Select [0, !GetAZs '']
        - !Select [1, !GetAZs '']
        - !Select [2, !GetAZs '']
    Export:
      Name: !Sub '${Environment}-availability-zones'
```
### Example 4: IP Address Management and Utilization Analysis Tool

```bash
#!/bin/bash

# IP Address Management and Utilization Analysis Tool
# Comprehensive analysis and management of IP address allocation and utilization

set -euo pipefail

# Configuration
CONFIG_FILE="${CONFIG_FILE:-./ipam-config.json}"
LOG_FILE="${LOG_FILE:-./ipam-analysis.log}"
RESULTS_DIR="${RESULTS_DIR:-./ipam-results}"
TEMP_DIR="${TEMP_DIR:-/tmp/ipam-analysis}"

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
REGIONS=($(jq -r '.regions[]' "$CONFIG_FILE"))
ENVIRONMENTS=($(jq -r '.environments[]' "$CONFIG_FILE"))
UTILIZATION_THRESHOLD=$(jq -r '.utilization_threshold // 80' "$CONFIG_FILE")
EXPANSION_THRESHOLD=$(jq -r '.expansion_threshold // 90' "$CONFIG_FILE")

log "Starting IP address management analysis"
log "Regions: ${#REGIONS[@]}"
log "Environments: ${#ENVIRONMENTS[@]}"
log "Utilization threshold: ${UTILIZATION_THRESHOLD}%"

# Function to analyze VPC IP utilization
analyze_vpc_utilization() {
    local region="$1"
    local analysis_id="vpc_analysis_$(date +%s)"
    local results_file="$RESULTS_DIR/vpc_utilization_${region}_${analysis_id}.json"
    
    log "Analyzing VPC utilization in region: $region"
    
    # Initialize results
    cat > "$results_file" << EOF
{
    "analysis_id": "$analysis_id",
    "region": "$region",
    "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "vpcs": [],
    "summary": {
        "total_vpcs": 0,
        "total_allocated_ips": 0,
        "total_used_ips": 0,
        "overall_utilization": 0,
        "high_utilization_vpcs": 0
    }
}
EOF
    
    # Get all VPCs in the region
    local vpcs=$(aws ec2 describe-vpcs \
        --region "$region" \
        --query 'Vpcs[*].{VpcId:VpcId,CidrBlock:CidrBlock,Tags:Tags}' \
        --output json 2>/dev/null || echo '[]')
    
    local total_allocated=0
    local total_used=0
    local high_util_count=0
    
    # Analyze each VPC
    echo "$vpcs" | jq -c '.[]' | while read -r vpc; do
        local vpc_id=$(echo "$vpc" | jq -r '.VpcId')
        local vpc_cidr=$(echo "$vpc" | jq -r '.CidrBlock')
        
        log "Analyzing VPC: $vpc_id ($vpc_cidr)"
        
        # Analyze VPC subnets
        local vpc_analysis=$(analyze_vpc_subnets "$region" "$vpc_id" "$vpc_cidr")
        
        # Add VPC analysis to results
        jq --argjson vpc_analysis "$vpc_analysis" \
            '.vpcs += [$vpc_analysis]' "$results_file" > "$results_file.tmp"
        mv "$results_file.tmp" "$results_file"
        
        # Update totals
        local vpc_allocated=$(echo "$vpc_analysis" | jq -r '.total_allocated_ips')
        local vpc_used=$(echo "$vpc_analysis" | jq -r '.total_used_ips')
        local vpc_utilization=$(echo "$vpc_analysis" | jq -r '.utilization_percentage')
        
        total_allocated=$((total_allocated + vpc_allocated))
        total_used=$((total_used + vpc_used))
        
        if (( $(echo "$vpc_utilization >= $UTILIZATION_THRESHOLD" | bc -l) )); then
            high_util_count=$((high_util_count + 1))
        fi
    done
    
    # Calculate overall utilization
    local overall_utilization=0
    if [[ $total_allocated -gt 0 ]]; then
        overall_utilization=$(echo "scale=2; $total_used * 100 / $total_allocated" | bc -l)
    fi
    
    # Update summary
    local vpc_count=$(echo "$vpcs" | jq 'length')
    jq --argjson total_vpcs "$vpc_count" \
       --argjson total_allocated "$total_allocated" \
       --argjson total_used "$total_used" \
       --argjson overall_util "$overall_utilization" \
       --argjson high_util_count "$high_util_count" \
       '.summary.total_vpcs = $total_vpcs |
        .summary.total_allocated_ips = $total_allocated |
        .summary.total_used_ips = $total_used |
        .summary.overall_utilization = $overall_util |
        .summary.high_utilization_vpcs = $high_util_count' \
        "$results_file" > "$results_file.tmp"
    mv "$results_file.tmp" "$results_file"
    
    log "VPC utilization analysis completed for $region"
    echo "$results_file"
}

# Function to analyze subnets within a VPC
analyze_vpc_subnets() {
    local region="$1"
    local vpc_id="$2"
    local vpc_cidr="$3"
    
    # Get all subnets in the VPC
    local subnets=$(aws ec2 describe-subnets \
        --region "$region" \
        --filters "Name=vpc-id,Values=$vpc_id" \
        --query 'Subnets[*].{SubnetId:SubnetId,CidrBlock:CidrBlock,AvailabilityZone:AvailabilityZone,AvailableIpAddressCount:AvailableIpAddressCount,Tags:Tags}' \
        --output json 2>/dev/null || echo '[]')
    
    local subnet_analysis=()
    local total_allocated=0
    local total_used=0
    
    # Analyze each subnet
    echo "$subnets" | jq -c '.[]' | while read -r subnet; do
        local subnet_id=$(echo "$subnet" | jq -r '.SubnetId')
        local subnet_cidr=$(echo "$subnet" | jq -r '.CidrBlock')
        local az=$(echo "$subnet" | jq -r '.AvailabilityZone')
        local available_ips=$(echo "$subnet" | jq -r '.AvailableIpAddressCount')
        
        # Calculate subnet utilization
        local subnet_network_size=$(calculate_network_size "$subnet_cidr")
        local usable_ips=$((subnet_network_size - 5))  # AWS reserves 5 IPs
        local used_ips=$((usable_ips - available_ips))
        local utilization=0
        
        if [[ $usable_ips -gt 0 ]]; then
            utilization=$(echo "scale=2; $used_ips * 100 / $usable_ips" | bc -l)
        fi
        
        # Get subnet tags for categorization
        local subnet_tags=$(echo "$subnet" | jq -r '.Tags // []')
        local subnet_type=$(echo "$subnet_tags" | jq -r '.[] | select(.Key == "Type") | .Value // "unknown"')
        local subnet_tier=$(echo "$subnet_tags" | jq -r '.[] | select(.Key == "Tier") | .Value // "unknown"')
        
        subnet_analysis+=("{
            \"subnet_id\": \"$subnet_id\",
            \"cidr_block\": \"$subnet_cidr\",
            \"availability_zone\": \"$az\",
            \"subnet_type\": \"$subnet_type\",
            \"subnet_tier\": \"$subnet_tier\",
            \"total_ips\": $subnet_network_size,
            \"usable_ips\": $usable_ips,
            \"used_ips\": $used_ips,
            \"available_ips\": $available_ips,
            \"utilization_percentage\": $utilization,
            \"status\": \"$(get_utilization_status "$utilization")\"
        }")
        
        total_allocated=$((total_allocated + usable_ips))
        total_used=$((total_used + used_ips))
    done
    
    # Calculate VPC utilization
    local vpc_utilization=0
    if [[ $total_allocated -gt 0 ]]; then
        vpc_utilization=$(echo "scale=2; $total_used * 100 / $total_allocated" | bc -l)
    fi
    
    # Get VPC tags
    local vpc_tags=$(aws ec2 describe-vpcs \
        --region "$region" \
        --vpc-ids "$vpc_id" \
        --query 'Vpcs[0].Tags // []' \
        --output json 2>/dev/null || echo '[]')
    
    local vpc_name=$(echo "$vpc_tags" | jq -r '.[] | select(.Key == "Name") | .Value // "unnamed"')
    local vpc_environment=$(echo "$vpc_tags" | jq -r '.[] | select(.Key == "Environment") | .Value // "unknown"')
    
    # Create subnet analysis JSON
    local subnet_analysis_json=$(printf '%s\n' "${subnet_analysis[@]}" | jq -s .)
    
    cat << EOF
{
    "vpc_id": "$vpc_id",
    "vpc_name": "$vpc_name",
    "vpc_environment": "$vpc_environment",
    "vpc_cidr": "$vpc_cidr",
    "region": "$region",
    "total_allocated_ips": $total_allocated,
    "total_used_ips": $total_used,
    "utilization_percentage": $vpc_utilization,
    "status": "$(get_utilization_status "$vpc_utilization")",
    "subnet_count": $(echo "$subnets" | jq 'length'),
    "subnets": $subnet_analysis_json
}
EOF
}

# Function to calculate network size from CIDR
calculate_network_size() {
    local cidr="$1"
    local prefix=$(echo "$cidr" | cut -d'/' -f2)
    local network_size=$((2 ** (32 - prefix)))
    echo "$network_size"
}

# Function to get utilization status
get_utilization_status() {
    local utilization="$1"
    
    if (( $(echo "$utilization >= $EXPANSION_THRESHOLD" | bc -l) )); then
        echo "critical"
    elif (( $(echo "$utilization >= $UTILIZATION_THRESHOLD" | bc -l) )); then
        echo "warning"
    elif (( $(echo "$utilization >= 50" | bc -l) )); then
        echo "normal"
    else
        echo "low"
    fi
}

# Function to generate expansion recommendations
generate_expansion_recommendations() {
    local analysis_files=("$@")
    local recommendations_file="$RESULTS_DIR/expansion_recommendations_$(date +%Y%m%d_%H%M%S).json"
    
    log "Generating expansion recommendations"
    
    # Initialize recommendations
    cat > "$recommendations_file" << EOF
{
    "generated_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "analysis_files": $(printf '%s\n' "${analysis_files[@]}" | jq -R . | jq -s .),
    "recommendations": [],
    "summary": {
        "total_recommendations": 0,
        "critical_recommendations": 0,
        "warning_recommendations": 0
    }
}
EOF
    
    local recommendations=()
    local critical_count=0
    local warning_count=0
    
    # Analyze each file for recommendations
    for analysis_file in "${analysis_files[@]}"; do
        if [[ -f "$analysis_file" ]]; then
            # Extract high utilization VPCs and subnets
            local high_util_vpcs=$(jq -r '.vpcs[] | select(.utilization_percentage >= '$UTILIZATION_THRESHOLD')' "$analysis_file" 2>/dev/null || echo '{}')
            
            if [[ "$high_util_vpcs" != "{}" ]]; then
                echo "$high_util_vpcs" | jq -c '.' | while read -r vpc; do
                    local vpc_id=$(echo "$vpc" | jq -r '.vpc_id')
                    local vpc_utilization=$(echo "$vpc" | jq -r '.utilization_percentage')
                    local region=$(echo "$vpc" | jq -r '.region')
                    
                    # Generate VPC-level recommendation
                    local priority="warning"
                    if (( $(echo "$vpc_utilization >= $EXPANSION_THRESHOLD" | bc -l) )); then
                        priority="critical"
                        critical_count=$((critical_count + 1))
                    else
                        warning_count=$((warning_count + 1))
                    fi
                    
                    local recommendation=$(generate_vpc_recommendation "$vpc" "$priority")
                    recommendations+=("$recommendation")
                    
                    # Generate subnet-level recommendations
                    echo "$vpc" | jq -c '.subnets[] | select(.utilization_percentage >= '$UTILIZATION_THRESHOLD')' | while read -r subnet; do
                        local subnet_recommendation=$(generate_subnet_recommendation "$subnet" "$vpc_id" "$region")
                        recommendations+=("$subnet_recommendation")
                    done
                done
            fi
        fi
    done
    
    # Add recommendations to file
    local recommendations_json=$(printf '%s\n' "${recommendations[@]}" | jq -s .)
    local total_recommendations=$(echo "$recommendations_json" | jq 'length')
    
    jq --argjson recs "$recommendations_json" \
       --argjson total "$total_recommendations" \
       --argjson critical "$critical_count" \
       --argjson warning "$warning_count" \
       '.recommendations = $recs |
        .summary.total_recommendations = $total |
        .summary.critical_recommendations = $critical |
        .summary.warning_recommendations = $warning' \
        "$recommendations_file" > "$recommendations_file.tmp"
    mv "$recommendations_file.tmp" "$recommendations_file"
    
    log "Expansion recommendations generated: $recommendations_file"
    echo "$recommendations_file"
}

# Function to generate VPC recommendation
generate_vpc_recommendation() {
    local vpc="$1"
    local priority="$2"
    
    local vpc_id=$(echo "$vpc" | jq -r '.vpc_id')
    local vpc_cidr=$(echo "$vpc" | jq -r '.vpc_cidr')
    local utilization=$(echo "$vpc" | jq -r '.utilization_percentage')
    local region=$(echo "$vpc" | jq -r '.region')
    
    cat << EOF
{
    "type": "vpc_expansion",
    "priority": "$priority",
    "vpc_id": "$vpc_id",
    "region": "$region",
    "current_cidr": "$vpc_cidr",
    "current_utilization": $utilization,
    "recommendation": "Consider adding secondary CIDR block to VPC",
    "suggested_actions": [
        "Add secondary CIDR block to VPC",
        "Create additional subnets in new CIDR range",
        "Update route tables and security groups",
        "Plan migration strategy for high-utilization subnets"
    ],
    "estimated_timeline": "2-4 weeks",
    "business_impact": "$(get_business_impact "$priority")"
}
EOF
}

# Function to generate subnet recommendation
generate_subnet_recommendation() {
    local subnet="$1"
    local vpc_id="$2"
    local region="$3"
    
    local subnet_id=$(echo "$subnet" | jq -r '.subnet_id')
    local subnet_cidr=$(echo "$subnet" | jq -r '.cidr_block')
    local utilization=$(echo "$subnet" | jq -r '.utilization_percentage')
    local subnet_type=$(echo "$subnet" | jq -r '.subnet_type')
    local az=$(echo "$subnet" | jq -r '.availability_zone')
    
    local priority="warning"
    if (( $(echo "$utilization >= $EXPANSION_THRESHOLD" | bc -l) )); then
        priority="critical"
    fi
    
    cat << EOF
{
    "type": "subnet_expansion",
    "priority": "$priority",
    "subnet_id": "$subnet_id",
    "vpc_id": "$vpc_id",
    "region": "$region",
    "availability_zone": "$az",
    "subnet_type": "$subnet_type",
    "current_cidr": "$subnet_cidr",
    "current_utilization": $utilization,
    "recommendation": "Create additional subnet or migrate workloads",
    "suggested_actions": [
        "Create additional subnet in same AZ",
        "Migrate some workloads to new subnet",
        "Update load balancer target groups",
        "Review auto-scaling group configurations"
    ],
    "estimated_timeline": "1-2 weeks",
    "business_impact": "$(get_business_impact "$priority")"
}
EOF
}

# Function to get business impact
get_business_impact() {
    local priority="$1"
    
    case "$priority" in
        "critical")
            echo "High - Risk of service disruption due to IP exhaustion"
            ;;
        "warning")
            echo "Medium - Potential capacity constraints for scaling"
            ;;
        *)
            echo "Low - Proactive capacity planning recommended"
            ;;
    esac
}

# Function to generate comprehensive IPAM report
generate_ipam_report() {
    local analysis_files=("$@")
    local report_file="$RESULTS_DIR/ipam_comprehensive_report_$(date +%Y%m%d_%H%M%S).json"
    
    log "Generating comprehensive IPAM report"
    
    # Collect all analysis data
    local all_analysis=()
    for analysis_file in "${analysis_files[@]}"; do
        if [[ -f "$analysis_file" ]]; then
            all_analysis+=("$(cat "$analysis_file")")
        fi
    done
    
    # Create comprehensive report
    local all_analysis_json=$(printf '%s\n' "${all_analysis[@]}" | jq -s .)
    
    # Calculate global statistics
    local global_stats=$(echo "$all_analysis_json" | jq '
        {
            "total_regions": length,
            "total_vpcs": [.[].summary.total_vpcs] | add,
            "total_allocated_ips": [.[].summary.total_allocated_ips] | add,
            "total_used_ips": [.[].summary.total_used_ips] | add,
            "total_high_utilization_vpcs": [.[].summary.high_utilization_vpcs] | add,
            "global_utilization": (([.[].summary.total_used_ips] | add) / ([.[].summary.total_allocated_ips] | add) * 100)
        }
    ')
    
    cat > "$report_file" << EOF
{
    "report_id": "ipam_report_$(date +%s)",
    "generated_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "configuration": $(cat "$CONFIG_FILE"),
    "global_statistics": $global_stats,
    "regional_analysis": $all_analysis_json,
    "utilization_thresholds": {
        "warning_threshold": $UTILIZATION_THRESHOLD,
        "critical_threshold": $EXPANSION_THRESHOLD
    }
}
EOF
    
    log "Comprehensive IPAM report generated: $report_file"
    echo "$report_file"
}

# Main execution
main() {
    log "Starting comprehensive IPAM analysis"
    
    local analysis_files=()
    
    # Analyze each region
    for region in "${REGIONS[@]}"; do
        log "Analyzing region: $region"
        analysis_file=$(analyze_vpc_utilization "$region")
        analysis_files+=("$analysis_file")
    done
    
    # Generate expansion recommendations
    recommendations_file=$(generate_expansion_recommendations "${analysis_files[@]}")
    
    # Generate comprehensive report
    report_file=$(generate_ipam_report "${analysis_files[@]}")
    
    # Display summary
    log "IPAM analysis completed"
    log "Analysis files: ${#analysis_files[@]}"
    log "Recommendations file: $recommendations_file"
    log "Comprehensive report: $report_file"
    
    # Show summary statistics
    if [[ -f "$report_file" ]]; then
        local summary=$(jq -r '.global_statistics | "Total VPCs: \(.total_vpcs), Global Utilization: \(.global_utilization | round)%, High Utilization VPCs: \(.total_high_utilization_vpcs)"' "$report_file")
        log "Global Summary: $summary"
    fi
    
    # Show critical recommendations
    if [[ -f "$recommendations_file" ]]; then
        local critical_recs=$(jq -r '.summary.critical_recommendations' "$recommendations_file")
        if [[ "$critical_recs" -gt 0 ]]; then
            log "WARNING: $critical_recs critical recommendations require immediate attention"
        fi
    fi
}

# Configuration file template
create_config_template() {
    cat > ipam-config.json << 'EOF'
{
    "regions": [
        "us-east-1",
        "us-west-2",
        "eu-west-1"
    ],
    "environments": [
        "production",
        "staging",
        "development"
    ],
    "utilization_threshold": 80,
    "expansion_threshold": 90,
    "analysis_settings": {
        "include_reserved_subnets": true,
        "calculate_growth_projections": true,
        "generate_cost_estimates": false
    },
    "notification_settings": {
        "sns_topic_arn": "arn:aws:sns:us-east-1:123456789012:ipam-alerts",
        "email_recipients": ["admin@company.com"]
    }
}
EOF
    log "Created configuration template: ipam-config.json"
}

# Command line argument handling
case "${1:-}" in
    "config")
        create_config_template
        ;;
    "analyze"|"")
        main
        ;;
    *)
        echo "Usage: $0 [config|analyze]"
        echo "  config  - Create configuration template"
        echo "  analyze - Run IPAM analysis (default)"
        exit 1
        ;;
esac

# Cleanup
rm -rf "$TEMP_DIR"
log "IPAM analysis process completed"
```

## AWS Services Used

- **Amazon VPC**: Virtual private cloud with flexible IP address allocation and CIDR management
- **Amazon EC2**: Subnet creation and management across multiple Availability Zones
- **AWS Transit Gateway**: Centralized connectivity hub with IP address coordination
- **Amazon Route 53**: DNS resolution and private hosted zones for internal networking
- **AWS Direct Connect**: Dedicated network connections with IP address coordination
- **Amazon CloudWatch**: Network monitoring, metrics, and automated alerting for IP utilization
- **AWS Lambda**: Serverless functions for automated IP management and monitoring
- **Amazon DynamoDB**: Storage for IP address management data and utilization tracking
- **Amazon SNS**: Notification service for IP utilization alerts and expansion recommendations
- **AWS Systems Manager**: Configuration management and automation for IP address policies
- **AWS CloudFormation**: Infrastructure as code for consistent subnet deployment
- **VPC Flow Logs**: Network traffic analysis and IP address usage monitoring

## Benefits

- **Scalable Architecture**: Accommodates future growth through intelligent IP address planning
- **High Availability**: Multi-AZ subnet deployment ensures resilience and fault tolerance
- **Automated Management**: Reduces manual overhead through automated monitoring and expansion
- **Cost Optimization**: Efficient IP address utilization and right-sized subnet allocation
- **Security Segmentation**: Proper network isolation through tiered subnet architecture
- **Compliance**: Standardized IP address allocation following best practices
- **Operational Efficiency**: Centralized IP address management and monitoring
- **Disaster Recovery**: Cross-region IP address coordination for business continuity
- **Container Ready**: Optimized subnet sizing for container orchestration platforms
- **Future-Proof**: Reserved address space and expansion capabilities for growth

## Related Resources

- [AWS Well-Architected Reliability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/)
- [Amazon VPC User Guide](https://docs.aws.amazon.com/vpc/latest/userguide/)
- [AWS VPC CIDR Planning](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html)
- [AWS Transit Gateway User Guide](https://docs.aws.amazon.com/vpc/latest/tgw/)
- [Amazon EKS Networking](https://docs.aws.amazon.com/eks/latest/userguide/network_reqs.html)
- [AWS IP Address Manager (IPAM)](https://docs.aws.amazon.com/vpc/latest/ipam/)
- [VPC Sharing](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-sharing.html)
- [AWS Networking Best Practices](https://docs.aws.amazon.com/whitepapers/latest/aws-vpc-connectivity-options/)
- [Amazon CloudWatch User Guide](https://docs.aws.amazon.com/cloudwatch/latest/monitoring/)
