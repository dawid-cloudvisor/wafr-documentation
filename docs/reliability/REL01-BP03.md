---
title: REL01-BP03 - Accommodate fixed service quotas and constraints through architecture
layout: default
parent: REL01 - How do you manage service quotas and constraints?
grand_parent: Reliability
nav_order: 3
---

<div class="pillar-header">
  <h1>REL01-BP03: Accommodate fixed service quotas and constraints through architecture</h1>
  <p>Be aware of unchangeable service quotas and physical resources. Design your architecture to prevent these fixed constraints from impacting reliability. Consider quotas for Availability Zones, edge locations, and Regions.</p>
</div>

## Implementation guidance

Fixed service quotas and constraints represent hard limits that cannot be increased through support requests. These constraints require architectural solutions rather than quota increases. Understanding and designing around these limitations is crucial for building reliable, scalable systems that can operate within AWS's fundamental constraints.

### Key steps for implementing this best practice:

1. **Identify fixed quotas and constraints**:
   - Document all hard limits that cannot be increased (Availability Zones per Region, edge locations, etc.)
   - Understand physical resource constraints (instance families, storage types, network bandwidth)
   - Map service-specific hard limits that affect your architecture
   - Identify regional and global service constraints
   - Document constraint interdependencies between services

2. **Design architecture patterns for constraint accommodation**:
   - Implement multi-region architectures to overcome regional limitations
   - Use multiple Availability Zones to distribute load and increase capacity
   - Design horizontal scaling patterns that work within fixed constraints
   - Implement resource pooling and sharing strategies
   - Create abstraction layers that hide constraint complexity

3. **Implement constraint-aware resource distribution**:
   - Distribute workloads across multiple Availability Zones and regions
   - Use multiple AWS accounts to access separate quota pools
   - Implement intelligent load balancing that considers constraints
   - Design data partitioning strategies that respect storage limits
   - Create resource allocation algorithms that optimize within constraints

4. **Build resilience against constraint-related failures**:
   - Design graceful degradation when approaching fixed limits
   - Implement circuit breakers for constraint-related failures
   - Create fallback mechanisms that route around constrained resources
   - Build monitoring and alerting for constraint utilization
   - Implement automated recovery procedures for constraint violations

5. **Optimize resource utilization within constraints**:
   - Implement resource pooling and multiplexing strategies
   - Use caching and buffering to reduce resource consumption
   - Optimize algorithms and data structures for constraint efficiency
   - Implement resource lifecycle management and cleanup
   - Create resource reservation and scheduling systems

6. **Plan for constraint evolution and growth**:
   - Monitor AWS service updates for constraint changes
   - Design flexible architectures that can adapt to new constraints
   - Plan migration strategies for constraint-related limitations
   - Implement feature flags for constraint-dependent functionality
   - Create capacity planning models that account for fixed constraints

## Implementation examples

### Example 1: Multi-AZ architecture with fixed constraint awareness

```python
import boto3
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import math
import uuid

class ConstraintAwareArchitect:
    def __init__(self):
        self.ec2 = boto3.client('ec2')
        self.elbv2 = boto3.client('elbv2')
        self.rds = boto3.client('rds')
        self.dynamodb = boto3.resource('dynamodb')
        self.cloudformation = boto3.client('cloudformation')
        
        # Fixed constraints that cannot be changed
        self.fixed_constraints = {
            'availability_zones': {
                'max_per_region': 6,  # Theoretical maximum, varies by region
                'typical_per_region': 3,  # Most regions have 3 AZs
                'min_recommended': 2  # Minimum for high availability
            },
            'instance_limits': {
                'max_enis_per_instance': {
                    't3.micro': 2,
                    't3.small': 3,
                    't3.medium': 3,
                    't3.large': 3,
                    'm5.large': 3,
                    'm5.xlarge': 4,
                    'm5.2xlarge': 4,
                    'm5.4xlarge': 8,
                    'c5.large': 3,
                    'c5.xlarge': 4
                },
                'max_ebs_volumes_per_instance': 28,  # For most instance types
                'max_security_groups_per_eni': 5
            },
            'networking': {
                'max_subnets_per_vpc': 200,
                'max_route_tables_per_vpc': 200,
                'max_security_groups_per_vpc': 2500,
                'max_rules_per_security_group': 60,
                'max_vpcs_per_region': 5  # Default, can be increased
            },
            'storage': {
                'max_ebs_volume_size_gp3': 16384,  # 16 TiB
                'max_ebs_volume_size_io2': 65536,  # 64 TiB
                'max_iops_per_volume_io2': 64000,
                'max_throughput_per_volume_gp3': 1000  # MB/s
            }
        }
        
        # DynamoDB table for storing architecture decisions
        self.architecture_table = self.dynamodb.Table('ConstraintAwareArchitectures')
    
    def analyze_regional_constraints(self, region: str) -> Dict[str, Any]:
        """Analyze fixed constraints for a specific region"""
        
        constraint_analysis = {
            'region': region,
            'analysis_timestamp': datetime.utcnow().isoformat(),
            'availability_zones': {},
            'instance_types': {},
            'networking_limits': {},
            'storage_constraints': {},
            'recommendations': []
        }
        
        # Analyze Availability Zones
        az_analysis = self.analyze_availability_zones(region)
        constraint_analysis['availability_zones'] = az_analysis
        
        # Analyze instance type availability
        instance_analysis = self.analyze_instance_type_availability(region)
        constraint_analysis['instance_types'] = instance_analysis
        
        # Analyze networking constraints
        networking_analysis = self.analyze_networking_constraints(region)
        constraint_analysis['networking_limits'] = networking_analysis
        
        # Generate recommendations
        constraint_analysis['recommendations'] = self.generate_constraint_recommendations(
            constraint_analysis
        )
        
        return constraint_analysis
    
    def analyze_availability_zones(self, region: str) -> Dict[str, Any]:
        """Analyze Availability Zone constraints for a region"""
        
        try:
            # Get available AZs
            response = self.ec2.describe_availability_zones(
                Filters=[
                    {'Name': 'region-name', 'Values': [region]},
                    {'Name': 'state', 'Values': ['available']}
                ]
            )
            
            available_azs = response['AvailabilityZones']
            
            az_analysis = {
                'total_available': len(available_azs),
                'az_details': [],
                'constraints': {
                    'can_support_multi_az': len(available_azs) >= 2,
                    'can_support_three_az': len(available_azs) >= 3,
                    'recommended_distribution': min(len(available_azs), 3)
                },
                'capacity_considerations': {}
            }
            
            # Analyze each AZ
            for az in available_azs:
                az_detail = {
                    'zone_id': az['ZoneId'],
                    'zone_name': az['ZoneName'],
                    'zone_type': az.get('ZoneType', 'availability-zone'),
                    'parent_zone': az.get('ParentZoneName'),
                    'network_border_group': az.get('NetworkBorderGroup', region)
                }
                
                # Check for capacity constraints (this would require additional API calls)
                az_detail['capacity_status'] = self.check_az_capacity_status(az['ZoneName'])
                
                az_analysis['az_details'].append(az_detail)
            
            # Determine capacity distribution strategy
            az_analysis['capacity_considerations'] = self.calculate_az_distribution_strategy(
                available_azs
            )
            
        except Exception as e:
            az_analysis = {
                'error': f"Failed to analyze AZs: {str(e)}",
                'total_available': 0,
                'constraints': {'can_support_multi_az': False}
            }
        
        return az_analysis
    
    def check_az_capacity_status(self, az_name: str) -> Dict[str, Any]:
        """Check capacity status for an Availability Zone"""
        
        # This is a simplified implementation
        # In practice, you would need to monitor capacity over time
        capacity_status = {
            'status': 'available',  # available, limited, constrained
            'instance_type_availability': {},
            'last_capacity_issue': None,
            'recommendations': []
        }
        
        # Check recent capacity issues (would require historical data)
        # For demonstration, we'll simulate some capacity awareness
        try:
            # Try to describe instance type offerings in this AZ
            response = self.ec2.describe_instance_type_offerings(
                LocationType='availability-zone',
                Filters=[{'Name': 'location', 'Values': [az_name]}]
            )
            
            available_types = [offering['InstanceType'] for offering in response['InstanceTypeOfferings']]
            
            # Check for common instance types
            common_types = ['t3.micro', 't3.small', 'm5.large', 'c5.large']
            for instance_type in common_types:
                capacity_status['instance_type_availability'][instance_type] = {
                    'available': instance_type in available_types,
                    'last_checked': datetime.utcnow().isoformat()
                }
        
        except Exception as e:
            capacity_status['error'] = str(e)
        
        return capacity_status
    
    def calculate_az_distribution_strategy(self, available_azs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate optimal distribution strategy across AZs"""
        
        num_azs = len(available_azs)
        
        distribution_strategy = {
            'recommended_az_count': min(num_azs, 3),
            'distribution_patterns': {},
            'failover_strategy': {},
            'capacity_planning': {}
        }
        
        if num_azs >= 3:
            # Three-AZ deployment for maximum availability
            distribution_strategy['distribution_patterns'] = {
                'primary_pattern': 'three_az_active_active',
                'compute_distribution': '34/33/33',  # Percentage per AZ
                'data_distribution': 'replicated_across_all',
                'load_balancer_targets': 'all_azs'
            }
            
            distribution_strategy['failover_strategy'] = {
                'single_az_failure': 'remaining_azs_handle_66_percent_increase',
                'two_az_failure': 'single_az_handles_full_load',
                'capacity_buffer_required': '50_percent_per_az'
            }
        
        elif num_azs == 2:
            # Two-AZ deployment
            distribution_strategy['distribution_patterns'] = {
                'primary_pattern': 'two_az_active_active',
                'compute_distribution': '50/50',
                'data_distribution': 'replicated_across_both',
                'load_balancer_targets': 'both_azs'
            }
            
            distribution_strategy['failover_strategy'] = {
                'single_az_failure': 'remaining_az_handles_full_load',
                'capacity_buffer_required': '100_percent_per_az'
            }
        
        else:
            # Single AZ - not recommended for production
            distribution_strategy['distribution_patterns'] = {
                'primary_pattern': 'single_az_active',
                'compute_distribution': '100',
                'data_distribution': 'single_az_with_backups',
                'load_balancer_targets': 'single_az'
            }
            
            distribution_strategy['failover_strategy'] = {
                'single_az_failure': 'complete_outage_requires_manual_recovery',
                'recommendation': 'consider_multi_region_deployment'
            }
        
        return distribution_strategy
    
    def design_constraint_aware_architecture(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Design architecture that accommodates fixed constraints"""
        
        architecture_id = str(uuid.uuid4())
        
        architecture_design = {
            'architecture_id': architecture_id,
            'design_timestamp': datetime.utcnow().isoformat(),
            'requirements': requirements,
            'constraint_accommodations': {},
            'architecture_components': {},
            'scaling_strategy': {},
            'resilience_patterns': {},
            'implementation_plan': []
        }
        
        # Analyze requirements against constraints
        constraint_accommodations = self.analyze_requirements_vs_constraints(requirements)
        architecture_design['constraint_accommodations'] = constraint_accommodations
        
        # Design architecture components
        components = self.design_architecture_components(requirements, constraint_accommodations)
        architecture_design['architecture_components'] = components
        
        # Create scaling strategy
        scaling_strategy = self.design_scaling_strategy(requirements, constraint_accommodations)
        architecture_design['scaling_strategy'] = scaling_strategy
        
        # Design resilience patterns
        resilience_patterns = self.design_resilience_patterns(requirements, constraint_accommodations)
        architecture_design['resilience_patterns'] = resilience_patterns
        
        # Create implementation plan
        implementation_plan = self.create_implementation_plan(architecture_design)
        architecture_design['implementation_plan'] = implementation_plan
        
        # Store architecture design
        self.store_architecture_design(architecture_design)
        
        return architecture_design
    
    def analyze_requirements_vs_constraints(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze requirements against fixed constraints"""
        
        accommodations = {
            'constraint_violations': [],
            'accommodation_strategies': {},
            'architectural_adjustments': [],
            'alternative_approaches': []
        }
        
        # Check compute requirements
        if 'compute' in requirements:
            compute_accommodations = self.analyze_compute_constraints(requirements['compute'])
            accommodations['accommodation_strategies']['compute'] = compute_accommodations
        
        # Check storage requirements
        if 'storage' in requirements:
            storage_accommodations = self.analyze_storage_constraints(requirements['storage'])
            accommodations['accommodation_strategies']['storage'] = storage_accommodations
        
        # Check networking requirements
        if 'networking' in requirements:
            network_accommodations = self.analyze_networking_constraints(requirements['networking'])
            accommodations['accommodation_strategies']['networking'] = network_accommodations
        
        # Check availability requirements
        if 'availability' in requirements:
            availability_accommodations = self.analyze_availability_constraints(requirements['availability'])
            accommodations['accommodation_strategies']['availability'] = availability_accommodations
        
        return accommodations
    
    def analyze_compute_constraints(self, compute_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze compute requirements against fixed constraints"""
        
        accommodations = {
            'instance_type_strategy': {},
            'scaling_accommodations': {},
            'network_interface_strategy': {},
            'storage_attachment_strategy': {}
        }
        
        # Analyze instance type requirements
        required_vcpus = compute_requirements.get('vcpus', 2)
        required_memory = compute_requirements.get('memory_gb', 4)
        required_network_performance = compute_requirements.get('network_performance', 'moderate')
        
        # Find suitable instance types
        suitable_instances = self.find_suitable_instance_types(
            required_vcpus, required_memory, required_network_performance
        )
        
        accommodations['instance_type_strategy'] = {
            'primary_instance_types': suitable_instances[:3],
            'fallback_instance_types': suitable_instances[3:6] if len(suitable_instances) > 3 else [],
            'scaling_considerations': self.calculate_scaling_considerations(suitable_instances)
        }
        
        # Analyze ENI requirements
        required_enis = compute_requirements.get('network_interfaces', 1)
        accommodations['network_interface_strategy'] = self.plan_eni_strategy(
            suitable_instances, required_enis
        )
        
        # Analyze EBS volume requirements
        required_volumes = compute_requirements.get('ebs_volumes', 1)
        accommodations['storage_attachment_strategy'] = self.plan_ebs_attachment_strategy(
            suitable_instances, required_volumes
        )
        
        return accommodations
    
    def find_suitable_instance_types(self, vcpus: int, memory_gb: int, 
                                   network_performance: str) -> List[str]:
        """Find instance types that meet requirements within constraints"""
        
        # This would typically query AWS APIs or use a lookup table
        # For demonstration, using a simplified mapping
        instance_specs = {
            't3.micro': {'vcpus': 2, 'memory': 1, 'network': 'low'},
            't3.small': {'vcpus': 2, 'memory': 2, 'network': 'low'},
            't3.medium': {'vcpus': 2, 'memory': 4, 'network': 'low'},
            't3.large': {'vcpus': 2, 'memory': 8, 'network': 'low'},
            'm5.large': {'vcpus': 2, 'memory': 8, 'network': 'moderate'},
            'm5.xlarge': {'vcpus': 4, 'memory': 16, 'network': 'moderate'},
            'm5.2xlarge': {'vcpus': 8, 'memory': 32, 'network': 'high'},
            'c5.large': {'vcpus': 2, 'memory': 4, 'network': 'moderate'},
            'c5.xlarge': {'vcpus': 4, 'memory': 8, 'network': 'moderate'}
        }
        
        suitable_types = []
        
        for instance_type, specs in instance_specs.items():
            if (specs['vcpus'] >= vcpus and 
                specs['memory'] >= memory_gb and
                self.network_performance_meets_requirement(specs['network'], network_performance)):
                suitable_types.append(instance_type)
        
        # Sort by cost-effectiveness (simplified)
        return sorted(suitable_types)
    
    def network_performance_meets_requirement(self, available: str, required: str) -> bool:
        """Check if network performance meets requirements"""
        
        performance_levels = {'low': 1, 'moderate': 2, 'high': 3, 'very_high': 4}
        return performance_levels.get(available, 0) >= performance_levels.get(required, 0)
    
    def plan_eni_strategy(self, instance_types: List[str], required_enis: int) -> Dict[str, Any]:
        """Plan ENI strategy within instance constraints"""
        
        eni_strategy = {
            'feasible_instance_types': [],
            'eni_distribution': {},
            'constraint_accommodations': []
        }
        
        for instance_type in instance_types:
            max_enis = self.fixed_constraints['instance_limits']['max_enis_per_instance'].get(
                instance_type, 2
            )
            
            if max_enis >= required_enis:
                eni_strategy['feasible_instance_types'].append({
                    'instance_type': instance_type,
                    'max_enis': max_enis,
                    'available_enis': max_enis - 1  # One ENI is always used by the instance
                })
            else:
                # Need to accommodate through multiple instances or alternative design
                instances_needed = math.ceil(required_enis / (max_enis - 1))
                eni_strategy['constraint_accommodations'].append({
                    'instance_type': instance_type,
                    'constraint': f'Max {max_enis} ENIs per instance',
                    'accommodation': f'Use {instances_needed} instances to support {required_enis} ENIs',
                    'alternative': 'Consider using fewer ENIs or different networking approach'
                })
        
        return eni_strategy
    
    def design_multi_region_failover_architecture(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Design multi-region architecture to overcome regional constraints"""
        
        failover_architecture = {
            'design_timestamp': datetime.utcnow().isoformat(),
            'primary_region': requirements.get('primary_region', 'us-east-1'),
            'secondary_regions': requirements.get('secondary_regions', ['us-west-2']),
            'failover_strategy': {},
            'data_replication': {},
            'traffic_routing': {},
            'constraint_mitigation': {}
        }
        
        # Design failover strategy
        failover_architecture['failover_strategy'] = {
            'failover_type': requirements.get('failover_type', 'warm_standby'),
            'rto_target': requirements.get('rto_minutes', 15),
            'rpo_target': requirements.get('rpo_minutes', 5),
            'automated_failover': requirements.get('automated_failover', True),
            'failback_strategy': 'manual_validation_required'
        }
        
        # Design data replication
        failover_architecture['data_replication'] = {
            'replication_method': 'cross_region_replication',
            'consistency_model': 'eventual_consistency',
            'replication_lag_target': '< 1 minute',
            'backup_strategy': 'automated_cross_region_backups'
        }
        
        # Design traffic routing
        failover_architecture['traffic_routing'] = {
            'dns_strategy': 'route53_health_checks',
            'load_balancing': 'cross_region_load_balancer',
            'failover_detection': 'automated_health_monitoring',
            'traffic_shifting': 'gradual_traffic_shift'
        }
        
        # Identify constraint mitigations
        failover_architecture['constraint_mitigation'] = {
            'regional_quota_limits': 'distribute_across_multiple_regions',
            'az_capacity_constraints': 'multi_region_capacity_pooling',
            'service_availability': 'region_specific_service_alternatives',
            'network_latency': 'edge_location_optimization'
        }
        
        return failover_architecture
    
    def implement_resource_pooling_strategy(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Implement resource pooling to maximize utilization within constraints"""
        
        pooling_strategy = {
            'strategy_timestamp': datetime.utcnow().isoformat(),
            'pooling_approach': {},
            'resource_allocation': {},
            'sharing_mechanisms': {},
            'optimization_techniques': {}
        }
        
        # Design compute resource pooling
        pooling_strategy['pooling_approach']['compute'] = {
            'strategy': 'shared_compute_pool',
            'pool_size_calculation': 'peak_demand_plus_buffer',
            'allocation_algorithm': 'fair_share_with_priority',
            'oversubscription_ratio': 1.2,  # 20% oversubscription
            'constraint_accommodation': 'horizontal_scaling_across_azs'
        }
        
        # Design storage resource pooling
        pooling_strategy['pooling_approach']['storage'] = {
            'strategy': 'tiered_storage_pool',
            'hot_tier': 'gp3_volumes_with_high_iops',
            'warm_tier': 'gp3_volumes_standard',
            'cold_tier': 's3_intelligent_tiering',
            'constraint_accommodation': 'volume_size_optimization_and_splitting'
        }
        
        # Design network resource pooling
        pooling_strategy['pooling_approach']['networking'] = {
            'strategy': 'shared_network_infrastructure',
            'vpc_sharing': 'cross_account_vpc_sharing',
            'subnet_allocation': 'dynamic_subnet_allocation',
            'security_group_sharing': 'template_based_security_groups',
            'constraint_accommodation': 'multiple_vpcs_for_scale'
        }
        
        return pooling_strategy
    
    def generate_constraint_recommendations(self, constraint_analysis: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on constraint analysis"""
        
        recommendations = []
        
        # AZ-related recommendations
        az_count = constraint_analysis.get('availability_zones', {}).get('total_available', 0)
        
        if az_count >= 3:
            recommendations.append(
                "Deploy across 3 Availability Zones for optimal availability and constraint distribution"
            )
        elif az_count == 2:
            recommendations.append(
                "Deploy across 2 Availability Zones with 100% capacity buffer in each AZ"
            )
            recommendations.append(
                "Consider multi-region deployment for higher availability"
            )
        else:
            recommendations.append(
                "CRITICAL: Single AZ region detected - implement multi-region architecture"
            )
        
        # Instance type recommendations
        instance_analysis = constraint_analysis.get('instance_types', {})
        if instance_analysis:
            recommendations.append(
                "Use multiple instance types to avoid capacity constraints in single instance family"
            )
            recommendations.append(
                "Implement spot instance diversification across instance types and AZs"
            )
        
        # Networking recommendations
        recommendations.append(
            "Design for ENI limits by distributing network interfaces across multiple instances"
        )
        recommendations.append(
            "Plan security group rules within the 60-rule limit per security group"
        )
        
        # Storage recommendations
        recommendations.append(
            "Split large storage requirements across multiple EBS volumes to stay within size limits"
        )
        recommendations.append(
            "Use EBS volume striping for performance requirements exceeding single volume limits"
        )
        
        # General architectural recommendations
        recommendations.append(
            "Implement horizontal scaling patterns that distribute load across constraint boundaries"
        )
        recommendations.append(
            "Use resource pooling and sharing to maximize utilization within fixed constraints"
        )
        recommendations.append(
            "Design graceful degradation for scenarios where constraints are approached"
        )
        
        return recommendations
    
    def store_architecture_design(self, architecture_design: Dict[str, Any]):
        """Store architecture design in DynamoDB"""
        
        try:
            # Prepare item for storage (handle nested objects)
            item = {
                'architecture_id': architecture_design['architecture_id'],
                'design_timestamp': architecture_design['design_timestamp'],
                'architecture_data': json.dumps(architecture_design),
                'ttl': int((datetime.utcnow() + timedelta(days=365)).timestamp())
            }
            
            self.architecture_table.put_item(Item=item)
            
        except Exception as e:
            print(f"Error storing architecture design: {str(e)}")

def lambda_handler(event, context):
    """Lambda function for constraint-aware architecture design"""
    
    architect = ConstraintAwareArchitect()
    
    action = event.get('action', 'analyze_constraints')
    
    if action == 'analyze_constraints':
        region = event.get('region', 'us-east-1')
        result = architect.analyze_regional_constraints(region)
    elif action == 'design_architecture':
        requirements = event.get('requirements', {})
        result = architect.design_constraint_aware_architecture(requirements)
    elif action == 'design_multi_region':
        requirements = event.get('requirements', {})
        result = architect.design_multi_region_failover_architecture(requirements)
    elif action == 'design_resource_pooling':
        requirements = event.get('requirements', {})
        result = architect.implement_resource_pooling_strategy(requirements)
    else:
        result = {'error': 'Invalid action specified'}
    
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
```
### Example 2: Horizontal scaling pattern with constraint distribution

```python
import boto3
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import math
import threading
import time

class ConstraintAwareScaler:
    def __init__(self):
        self.autoscaling = boto3.client('autoscaling')
        self.ec2 = boto3.client('ec2')
        self.cloudwatch = boto3.client('cloudwatch')
        self.elbv2 = boto3.client('elbv2')
        self.dynamodb = boto3.resource('dynamodb')
        
        # Scaling constraints and limits
        self.scaling_constraints = {
            'max_instances_per_az': 100,  # Practical limit for management
            'max_instances_per_asg': 300,  # Practical ASG limit
            'max_target_groups_per_alb': 100,
            'max_targets_per_target_group': 1000,
            'instance_launch_rate_limit': 10,  # instances per minute
            'cooldown_periods': {
                'scale_out': 300,  # 5 minutes
                'scale_in': 600    # 10 minutes
            }
        }
        
        # Instance type constraints
        self.instance_constraints = {
            'max_network_interfaces': {
                't3.micro': 2, 't3.small': 3, 't3.medium': 3, 't3.large': 3,
                'm5.large': 3, 'm5.xlarge': 4, 'm5.2xlarge': 4, 'm5.4xlarge': 8,
                'c5.large': 3, 'c5.xlarge': 4, 'c5.2xlarge': 4, 'c5.4xlarge': 8
            },
            'max_ebs_volumes': 28,  # Most instance types
            'max_ebs_throughput_mbps': {
                't3.micro': 2085, 't3.small': 2085, 't3.medium': 2085,
                'm5.large': 4750, 'm5.xlarge': 4750, 'm5.2xlarge': 4750,
                'c5.large': 4750, 'c5.xlarge': 4750
            }
        }
        
        # DynamoDB table for scaling decisions
        self.scaling_table = self.dynamodb.Table('ConstraintAwareScaling')
    
    def design_distributed_scaling_architecture(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Design scaling architecture that distributes across constraint boundaries"""
        
        scaling_architecture = {
            'architecture_id': f"scaling-{int(time.time())}",
            'design_timestamp': datetime.utcnow().isoformat(),
            'requirements': requirements,
            'scaling_strategy': {},
            'constraint_accommodations': {},
            'auto_scaling_groups': [],
            'load_balancing_strategy': {},
            'monitoring_and_alerting': {}
        }
        
        # Analyze scaling requirements
        max_capacity = requirements.get('max_capacity', 100)
        target_availability_zones = requirements.get('availability_zones', 3)
        instance_types = requirements.get('instance_types', ['m5.large'])
        
        # Design scaling strategy
        scaling_strategy = self.design_scaling_strategy(
            max_capacity, target_availability_zones, instance_types
        )
        scaling_architecture['scaling_strategy'] = scaling_strategy
        
        # Design constraint accommodations
        constraint_accommodations = self.design_constraint_accommodations(scaling_strategy)
        scaling_architecture['constraint_accommodations'] = constraint_accommodations
        
        # Design Auto Scaling Groups
        asg_design = self.design_auto_scaling_groups(scaling_strategy, constraint_accommodations)
        scaling_architecture['auto_scaling_groups'] = asg_design
        
        # Design load balancing strategy
        lb_strategy = self.design_load_balancing_strategy(asg_design)
        scaling_architecture['load_balancing_strategy'] = lb_strategy
        
        # Design monitoring and alerting
        monitoring_strategy = self.design_monitoring_strategy(scaling_architecture)
        scaling_architecture['monitoring_and_alerting'] = monitoring_strategy
        
        return scaling_architecture
    
    def design_scaling_strategy(self, max_capacity: int, target_azs: int, 
                               instance_types: List[str]) -> Dict[str, Any]:
        """Design scaling strategy within constraints"""
        
        strategy = {
            'total_capacity': max_capacity,
            'availability_zones': target_azs,
            'instance_types': instance_types,
            'distribution_strategy': {},
            'scaling_patterns': {},
            'constraint_considerations': {}
        }
        
        # Calculate distribution across AZs
        instances_per_az = math.ceil(max_capacity / target_azs)
        
        # Check if we exceed per-AZ constraints
        if instances_per_az > self.scaling_constraints['max_instances_per_az']:
            # Need to use multiple ASGs per AZ or reduce capacity
            asgs_per_az = math.ceil(instances_per_az / self.scaling_constraints['max_instances_per_az'])
            instances_per_asg = math.ceil(instances_per_az / asgs_per_az)
            
            strategy['distribution_strategy'] = {
                'pattern': 'multiple_asgs_per_az',
                'asgs_per_az': asgs_per_az,
                'instances_per_asg': instances_per_asg,
                'total_asgs': asgs_per_az * target_azs,
                'constraint_reason': f'Exceeds {self.scaling_constraints["max_instances_per_az"]} instances per AZ limit'
            }
        else:
            strategy['distribution_strategy'] = {
                'pattern': 'single_asg_per_az',
                'asgs_per_az': 1,
                'instances_per_asg': instances_per_az,
                'total_asgs': target_azs,
                'constraint_reason': 'Within per-AZ instance limits'
            }
        
        # Design scaling patterns
        strategy['scaling_patterns'] = {
            'scale_out_pattern': 'distributed_across_azs',
            'scale_in_pattern': 'maintain_az_balance',
            'instance_type_strategy': 'diversified_across_types',
            'launch_rate_limiting': True,
            'cooldown_management': 'per_asg_cooldowns'
        }
        
        # Document constraint considerations
        strategy['constraint_considerations'] = {
            'max_instances_per_az': self.scaling_constraints['max_instances_per_az'],
            'max_instances_per_asg': self.scaling_constraints['max_instances_per_asg'],
            'launch_rate_limit': self.scaling_constraints['instance_launch_rate_limit'],
            'accommodation_strategy': strategy['distribution_strategy']['pattern']
        }
        
        return strategy
    
    def design_constraint_accommodations(self, scaling_strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Design specific accommodations for scaling constraints"""
        
        accommodations = {
            'capacity_distribution': {},
            'launch_rate_management': {},
            'instance_type_diversification': {},
            'network_interface_management': {},
            'storage_constraint_handling': {}
        }
        
        # Capacity distribution accommodations
        total_asgs = scaling_strategy['distribution_strategy']['total_asgs']
        
        accommodations['capacity_distribution'] = {
            'strategy': 'even_distribution_with_overflow_handling',
            'primary_distribution': 'equal_across_asgs',
            'overflow_handling': 'round_robin_additional_capacity',
            'rebalancing_trigger': 'az_imbalance_threshold_20_percent',
            'constraint_mitigation': f'Using {total_asgs} ASGs to stay within per-ASG limits'
        }
        
        # Launch rate management
        accommodations['launch_rate_management'] = {
            'strategy': 'coordinated_launch_throttling',
            'max_concurrent_launches': self.scaling_constraints['instance_launch_rate_limit'],
            'launch_coordination': 'queue_based_with_priority',
            'backoff_strategy': 'exponential_backoff_on_throttling',
            'constraint_mitigation': 'Prevent API throttling and capacity issues'
        }
        
        # Instance type diversification
        instance_types = scaling_strategy['instance_types']
        accommodations['instance_type_diversification'] = {
            'strategy': 'mixed_instance_types_per_asg',
            'primary_instance_types': instance_types[:2],
            'fallback_instance_types': instance_types[2:] if len(instance_types) > 2 else [],
            'allocation_strategy': 'diversified',
            'spot_instance_strategy': 'diversified_across_types_and_azs',
            'constraint_mitigation': 'Avoid capacity constraints in single instance family'
        }
        
        return accommodations
    
    def design_auto_scaling_groups(self, scaling_strategy: Dict[str, Any], 
                                 accommodations: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Design Auto Scaling Groups with constraint awareness"""
        
        asg_designs = []
        
        distribution = scaling_strategy['distribution_strategy']
        total_capacity = scaling_strategy['total_capacity']
        availability_zones = scaling_strategy['availability_zones']
        
        # Calculate capacity per ASG
        capacity_per_asg = math.ceil(total_capacity / distribution['total_asgs'])
        
        asg_counter = 0
        
        for az_index in range(availability_zones):
            az_name = f"az-{az_index + 1}"  # Simplified AZ naming
            
            for asg_index in range(distribution['asgs_per_az']):
                asg_counter += 1
                
                # Calculate this ASG's capacity
                remaining_capacity = total_capacity - (asg_counter - 1) * capacity_per_asg
                this_asg_capacity = min(capacity_per_asg, remaining_capacity)
                
                if this_asg_capacity <= 0:
                    break
                
                asg_design = {
                    'asg_name': f"constraint-aware-asg-{az_name}-{asg_index + 1}",
                    'availability_zone': az_name,
                    'min_size': max(1, this_asg_capacity // 4),  # 25% minimum
                    'max_size': this_asg_capacity,
                    'desired_capacity': max(2, this_asg_capacity // 2),  # 50% desired
                    'instance_types': scaling_strategy['instance_types'],
                    'mixed_instances_policy': self.create_mixed_instances_policy(
                        scaling_strategy['instance_types']
                    ),
                    'scaling_policies': self.create_scaling_policies(this_asg_capacity),
                    'health_check_configuration': {
                        'health_check_type': 'ELB',
                        'health_check_grace_period': 300,
                        'unhealthy_threshold': 2
                    },
                    'constraint_accommodations': {
                        'max_capacity_reason': f'Limited to {this_asg_capacity} to stay within constraints',
                        'launch_rate_limiting': True,
                        'cooldown_periods': self.scaling_constraints['cooldown_periods']
                    }
                }
                
                asg_designs.append(asg_design)
        
        return asg_designs
    
    def create_mixed_instances_policy(self, instance_types: List[str]) -> Dict[str, Any]:
        """Create mixed instances policy for constraint accommodation"""
        
        policy = {
            'instances_distribution': {
                'on_demand_allocation_strategy': 'prioritized',
                'on_demand_base_capacity': 2,
                'on_demand_percentage_above_base_capacity': 25,
                'spot_allocation_strategy': 'diversified',
                'spot_instance_pools': min(len(instance_types), 4),
                'spot_max_price': None  # Use on-demand price
            },
            'launch_template': {
                'overrides': []
            }
        }
        
        # Create overrides for each instance type
        for instance_type in instance_types:
            override = {
                'instance_type': instance_type,
                'weighted_capacity': self.calculate_instance_weight(instance_type)
            }
            policy['launch_template']['overrides'].append(override)
        
        return policy
    
    def calculate_instance_weight(self, instance_type: str) -> int:
        """Calculate instance weight based on capacity"""
        
        # Simplified weight calculation based on vCPUs
        weight_mapping = {
            't3.micro': 1, 't3.small': 1, 't3.medium': 1, 't3.large': 1,
            'm5.large': 2, 'm5.xlarge': 4, 'm5.2xlarge': 8, 'm5.4xlarge': 16,
            'c5.large': 2, 'c5.xlarge': 4, 'c5.2xlarge': 8, 'c5.4xlarge': 16
        }
        
        return weight_mapping.get(instance_type, 1)
    
    def create_scaling_policies(self, max_capacity: int) -> List[Dict[str, Any]]:
        """Create scaling policies with constraint awareness"""
        
        policies = []
        
        # Scale-out policy
        scale_out_policy = {
            'policy_name': 'scale-out-policy',
            'policy_type': 'TargetTrackingScaling',
            'target_tracking_configuration': {
                'target_value': 70.0,
                'predefined_metric_specification': {
                    'predefined_metric_type': 'ASGAverageCPUUtilization'
                },
                'scale_out_cooldown': self.scaling_constraints['cooldown_periods']['scale_out'],
                'scale_in_cooldown': self.scaling_constraints['cooldown_periods']['scale_in']
            },
            'constraint_accommodations': {
                'max_capacity_limit': max_capacity,
                'launch_rate_limiting': True,
                'gradual_scaling': True
            }
        }
        policies.append(scale_out_policy)
        
        # Step scaling policy for rapid scale-out
        step_scaling_policy = {
            'policy_name': 'rapid-scale-out-policy',
            'policy_type': 'StepScaling',
            'adjustment_type': 'ChangeInCapacity',
            'step_adjustments': [
                {
                    'metric_interval_lower_bound': 0,
                    'metric_interval_upper_bound': 50,
                    'scaling_adjustment': min(2, max_capacity // 10)  # 10% or 2 instances
                },
                {
                    'metric_interval_lower_bound': 50,
                    'scaling_adjustment': min(5, max_capacity // 5)   # 20% or 5 instances
                }
            ],
            'cooldown': self.scaling_constraints['cooldown_periods']['scale_out'],
            'constraint_accommodations': {
                'launch_rate_aware': True,
                'capacity_limit_aware': True
            }
        }
        policies.append(step_scaling_policy)
        
        return policies
    
    def design_load_balancing_strategy(self, asg_designs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Design load balancing strategy for distributed ASGs"""
        
        lb_strategy = {
            'load_balancer_type': 'application',
            'target_group_strategy': {},
            'health_check_configuration': {},
            'constraint_accommodations': {}
        }
        
        total_asgs = len(asg_designs)
        max_targets_per_tg = self.scaling_constraints['max_targets_per_target_group']
        
        # Determine target group strategy
        if total_asgs <= 5:
            # Single target group can handle all ASGs
            lb_strategy['target_group_strategy'] = {
                'pattern': 'single_target_group',
                'target_groups': 1,
                'asgs_per_target_group': total_asgs,
                'routing_strategy': 'round_robin'
            }
        else:
            # Multiple target groups needed
            target_groups_needed = math.ceil(total_asgs / 5)  # Max 5 ASGs per TG for management
            
            lb_strategy['target_group_strategy'] = {
                'pattern': 'multiple_target_groups',
                'target_groups': target_groups_needed,
                'asgs_per_target_group': math.ceil(total_asgs / target_groups_needed),
                'routing_strategy': 'weighted_routing'
            }
        
        # Health check configuration
        lb_strategy['health_check_configuration'] = {
            'health_check_path': '/health',
            'health_check_interval_seconds': 30,
            'health_check_timeout_seconds': 5,
            'healthy_threshold_count': 2,
            'unhealthy_threshold_count': 3,
            'matcher': '200'
        }
        
        # Constraint accommodations
        lb_strategy['constraint_accommodations'] = {
            'max_targets_per_tg': max_targets_per_tg,
            'max_tgs_per_alb': self.scaling_constraints['max_target_groups_per_alb'],
            'cross_zone_load_balancing': True,
            'connection_draining': 300  # seconds
        }
        
        return lb_strategy
    
    def implement_constraint_aware_scaling_logic(self, asg_name: str, 
                                               scaling_decision: Dict[str, Any]) -> Dict[str, Any]:
        """Implement scaling logic that respects constraints"""
        
        scaling_result = {
            'asg_name': asg_name,
            'scaling_timestamp': datetime.utcnow().isoformat(),
            'scaling_decision': scaling_decision,
            'constraint_checks': {},
            'scaling_action': {},
            'constraint_violations': []
        }
        
        # Get current ASG state
        current_state = self.get_asg_current_state(asg_name)
        scaling_result['current_state'] = current_state
        
        # Perform constraint checks
        constraint_checks = self.perform_constraint_checks(current_state, scaling_decision)
        scaling_result['constraint_checks'] = constraint_checks
        
        # Determine scaling action
        if constraint_checks['can_scale']:
            scaling_action = self.execute_scaling_action(asg_name, scaling_decision, constraint_checks)
            scaling_result['scaling_action'] = scaling_action
        else:
            scaling_result['constraint_violations'] = constraint_checks['violations']
            scaling_result['scaling_action'] = {
                'action': 'blocked',
                'reason': 'constraint_violations',
                'alternative_actions': constraint_checks.get('alternatives', [])
            }
        
        # Store scaling decision
        self.store_scaling_decision(scaling_result)
        
        return scaling_result
    
    def perform_constraint_checks(self, current_state: Dict[str, Any], 
                                scaling_decision: Dict[str, Any]) -> Dict[str, Any]:
        """Perform comprehensive constraint checks before scaling"""
        
        checks = {
            'can_scale': True,
            'violations': [],
            'warnings': [],
            'alternatives': []
        }
        
        current_capacity = current_state['desired_capacity']
        target_capacity = scaling_decision['target_capacity']
        scaling_direction = 'out' if target_capacity > current_capacity else 'in'
        
        # Check capacity constraints
        if target_capacity > current_state['max_size']:
            checks['can_scale'] = False
            checks['violations'].append({
                'constraint': 'max_capacity',
                'current_max': current_state['max_size'],
                'requested': target_capacity,
                'message': f'Requested capacity {target_capacity} exceeds max size {current_state["max_size"]}'
            })
            
            # Suggest alternative
            checks['alternatives'].append({
                'action': 'increase_max_size',
                'description': f'Increase max size to {target_capacity}',
                'feasible': target_capacity <= self.scaling_constraints['max_instances_per_asg']
            })
        
        # Check launch rate constraints
        if scaling_direction == 'out':
            instances_to_launch = target_capacity - current_capacity
            max_launch_rate = self.scaling_constraints['instance_launch_rate_limit']
            
            if instances_to_launch > max_launch_rate:
                checks['warnings'].append({
                    'constraint': 'launch_rate',
                    'instances_to_launch': instances_to_launch,
                    'max_rate': max_launch_rate,
                    'message': f'Launching {instances_to_launch} instances may hit rate limits'
                })
                
                checks['alternatives'].append({
                    'action': 'gradual_scaling',
                    'description': f'Scale in batches of {max_launch_rate} instances',
                    'estimated_time': math.ceil(instances_to_launch / max_launch_rate)
                })
        
        # Check cooldown constraints
        last_scaling_activity = current_state.get('last_scaling_activity')
        if last_scaling_activity:
            time_since_last = (datetime.utcnow() - datetime.fromisoformat(last_scaling_activity)).seconds
            required_cooldown = self.scaling_constraints['cooldown_periods'][f'scale_{scaling_direction}']
            
            if time_since_last < required_cooldown:
                checks['can_scale'] = False
                checks['violations'].append({
                    'constraint': 'cooldown_period',
                    'time_since_last': time_since_last,
                    'required_cooldown': required_cooldown,
                    'message': f'Must wait {required_cooldown - time_since_last} more seconds'
                })
        
        return checks
    
    def get_asg_current_state(self, asg_name: str) -> Dict[str, Any]:
        """Get current state of Auto Scaling Group"""
        
        try:
            response = self.autoscaling.describe_auto_scaling_groups(
                AutoScalingGroupNames=[asg_name]
            )
            
            if not response['AutoScalingGroups']:
                return {'error': 'ASG not found'}
            
            asg = response['AutoScalingGroups'][0]
            
            return {
                'asg_name': asg['AutoScalingGroupName'],
                'min_size': asg['MinSize'],
                'max_size': asg['MaxSize'],
                'desired_capacity': asg['DesiredCapacity'],
                'current_instances': len(asg['Instances']),
                'availability_zones': asg['AvailabilityZones'],
                'health_check_type': asg['HealthCheckType'],
                'last_scaling_activity': self.get_last_scaling_activity(asg_name)
            }
        
        except Exception as e:
            return {'error': str(e)}
    
    def get_last_scaling_activity(self, asg_name: str) -> Optional[str]:
        """Get timestamp of last scaling activity"""
        
        try:
            response = self.autoscaling.describe_scaling_activities(
                AutoScalingGroupName=asg_name,
                MaxRecords=1
            )
            
            if response['Activities']:
                return response['Activities'][0]['StartTime'].isoformat()
        
        except Exception as e:
            print(f"Error getting scaling activities: {str(e)}")
        
        return None
    
    def execute_scaling_action(self, asg_name: str, scaling_decision: Dict[str, Any], 
                             constraint_checks: Dict[str, Any]) -> Dict[str, Any]:
        """Execute scaling action with constraint awareness"""
        
        action_result = {
            'action': 'scale',
            'asg_name': asg_name,
            'target_capacity': scaling_decision['target_capacity'],
            'execution_timestamp': datetime.utcnow().isoformat(),
            'success': False,
            'constraint_accommodations': []
        }
        
        try:
            # Check if gradual scaling is needed
            if any(alt['action'] == 'gradual_scaling' for alt in constraint_checks.get('alternatives', [])):
                action_result = self.execute_gradual_scaling(asg_name, scaling_decision)
            else:
                # Direct scaling
                self.autoscaling.set_desired_capacity(
                    AutoScalingGroupName=asg_name,
                    DesiredCapacity=scaling_decision['target_capacity'],
                    HonorCooldown=True
                )
                
                action_result['success'] = True
                action_result['method'] = 'direct_scaling'
        
        except Exception as e:
            action_result['error'] = str(e)
            action_result['success'] = False
        
        return action_result
    
    def execute_gradual_scaling(self, asg_name: str, scaling_decision: Dict[str, Any]) -> Dict[str, Any]:
        """Execute gradual scaling to respect launch rate limits"""
        
        current_state = self.get_asg_current_state(asg_name)
        current_capacity = current_state['desired_capacity']
        target_capacity = scaling_decision['target_capacity']
        
        max_launch_rate = self.scaling_constraints['instance_launch_rate_limit']
        
        gradual_result = {
            'action': 'gradual_scaling',
            'asg_name': asg_name,
            'current_capacity': current_capacity,
            'target_capacity': target_capacity,
            'scaling_steps': [],
            'success': True
        }
        
        # Calculate scaling steps
        remaining_capacity = target_capacity - current_capacity
        step_number = 1
        
        while remaining_capacity > 0:
            step_capacity = min(max_launch_rate, remaining_capacity)
            new_capacity = current_capacity + step_capacity
            
            step = {
                'step_number': step_number,
                'target_capacity': new_capacity,
                'instances_to_add': step_capacity,
                'estimated_time': 60  # 1 minute per step
            }
            
            gradual_result['scaling_steps'].append(step)
            
            current_capacity = new_capacity
            remaining_capacity = target_capacity - current_capacity
            step_number += 1
        
        # Execute first step immediately
        if gradual_result['scaling_steps']:
            first_step = gradual_result['scaling_steps'][0]
            
            try:
                self.autoscaling.set_desired_capacity(
                    AutoScalingGroupName=asg_name,
                    DesiredCapacity=first_step['target_capacity'],
                    HonorCooldown=True
                )
                
                first_step['executed'] = True
                first_step['execution_time'] = datetime.utcnow().isoformat()
                
                # Schedule remaining steps (would typically use Step Functions or EventBridge)
                if len(gradual_result['scaling_steps']) > 1:
                    gradual_result['remaining_steps_scheduled'] = True
                    gradual_result['next_step_time'] = (
                        datetime.utcnow() + timedelta(minutes=1)
                    ).isoformat()
            
            except Exception as e:
                gradual_result['success'] = False
                gradual_result['error'] = str(e)
        
        return gradual_result
    
    def store_scaling_decision(self, scaling_result: Dict[str, Any]):
        """Store scaling decision and results"""
        
        try:
            item = {
                'scaling_id': f"{scaling_result['asg_name']}-{int(time.time())}",
                'asg_name': scaling_result['asg_name'],
                'scaling_timestamp': scaling_result['scaling_timestamp'],
                'scaling_data': json.dumps(scaling_result),
                'ttl': int((datetime.utcnow() + timedelta(days=30)).timestamp())
            }
            
            self.scaling_table.put_item(Item=item)
        
        except Exception as e:
            print(f"Error storing scaling decision: {str(e)}")

def lambda_handler(event, context):
    """Lambda function for constraint-aware scaling"""
    
    scaler = ConstraintAwareScaler()
    
    action = event.get('action', 'design_scaling')
    
    if action == 'design_scaling':
        requirements = event.get('requirements', {})
        result = scaler.design_distributed_scaling_architecture(requirements)
    elif action == 'execute_scaling':
        asg_name = event.get('asg_name')
        scaling_decision = event.get('scaling_decision', {})
        result = scaler.implement_constraint_aware_scaling_logic(asg_name, scaling_decision)
    else:
        result = {'error': 'Invalid action specified'}
    
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
```
### Example 3: Storage constraint accommodation patterns

```python
import boto3
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import math
import uuid

class StorageConstraintManager:
    def __init__(self):
        self.ec2 = boto3.client('ec2')
        self.s3 = boto3.client('s3')
        self.dynamodb = boto3.resource('dynamodb')
        self.cloudwatch = boto3.client('cloudwatch')
        
        # EBS volume constraints (fixed limits)
        self.ebs_constraints = {
            'max_volume_sizes': {
                'gp2': 16384,    # 16 TiB
                'gp3': 16384,    # 16 TiB
                'io1': 16384,    # 16 TiB
                'io2': 65536,    # 64 TiB
                'st1': 16384,    # 16 TiB
                'sc1': 16384     # 16 TiB
            },
            'max_iops': {
                'gp2': 16000,    # 3 IOPS per GB, max 16,000
                'gp3': 16000,    # Configurable up to 16,000
                'io1': 64000,    # 50 IOPS per GB, max 64,000
                'io2': 64000     # 500 IOPS per GB, max 64,000
            },
            'max_throughput': {
                'gp3': 1000,     # MB/s
                'st1': 500,      # MB/s
                'sc1': 250       # MB/s
            },
            'max_volumes_per_instance': 28,  # Most instance types
            'max_total_volume_size_per_instance': 65536  # 64 TiB for most instances
        }
        
        # S3 constraints
        self.s3_constraints = {
            'max_object_size': 5497558138880,  # 5 TB
            'max_multipart_parts': 10000,
            'max_part_size': 5368709120,       # 5 GB
            'min_part_size': 5242880,          # 5 MB (except last part)
            'max_keys_per_list_request': 1000,
            'max_delete_objects_per_request': 1000
        }
        
        # DynamoDB table for storage architecture decisions
        self.storage_table = self.dynamodb.Table('StorageConstraintArchitectures')
    
    def design_storage_architecture(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Design storage architecture that accommodates fixed constraints"""
        
        architecture_id = str(uuid.uuid4())
        
        storage_architecture = {
            'architecture_id': architecture_id,
            'design_timestamp': datetime.utcnow().isoformat(),
            'requirements': requirements,
            'storage_strategy': {},
            'constraint_accommodations': {},
            'ebs_design': {},
            's3_design': {},
            'data_lifecycle_management': {},
            'performance_optimization': {}
        }
        
        # Analyze storage requirements
        total_storage_gb = requirements.get('total_storage_gb', 1000)
        performance_requirements = requirements.get('performance', {})
        availability_requirements = requirements.get('availability', {})
        
        # Design EBS storage strategy
        ebs_design = self.design_ebs_storage_strategy(
            total_storage_gb, performance_requirements, availability_requirements
        )
        storage_architecture['ebs_design'] = ebs_design
        
        # Design S3 storage strategy
        s3_design = self.design_s3_storage_strategy(requirements)
        storage_architecture['s3_design'] = s3_design
        
        # Design constraint accommodations
        constraint_accommodations = self.design_storage_constraint_accommodations(
            ebs_design, s3_design, requirements
        )
        storage_architecture['constraint_accommodations'] = constraint_accommodations
        
        # Design data lifecycle management
        lifecycle_management = self.design_data_lifecycle_management(requirements)
        storage_architecture['data_lifecycle_management'] = lifecycle_management
        
        # Design performance optimization
        performance_optimization = self.design_performance_optimization(
            ebs_design, s3_design, performance_requirements
        )
        storage_architecture['performance_optimization'] = performance_optimization
        
        # Store architecture design
        self.store_storage_architecture(storage_architecture)
        
        return storage_architecture
    
    def design_ebs_storage_strategy(self, total_storage_gb: int, 
                                  performance_requirements: Dict[str, Any],
                                  availability_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Design EBS storage strategy within constraints"""
        
        ebs_strategy = {
            'total_storage_gb': total_storage_gb,
            'volume_distribution': {},
            'volume_types': {},
            'performance_configuration': {},
            'availability_configuration': {},
            'constraint_accommodations': []
        }
        
        # Determine optimal volume type
        required_iops = performance_requirements.get('iops', 3000)
        required_throughput = performance_requirements.get('throughput_mbps', 125)
        
        volume_type = self.select_optimal_volume_type(required_iops, required_throughput)
        ebs_strategy['volume_types']['primary'] = volume_type
        
        # Calculate volume distribution
        max_volume_size = self.ebs_constraints['max_volume_sizes'][volume_type]
        
        if total_storage_gb <= max_volume_size:
            # Single volume can accommodate
            ebs_strategy['volume_distribution'] = {
                'strategy': 'single_volume',
                'volume_count': 1,
                'volume_size_gb': total_storage_gb,
                'constraint_accommodation': 'within_single_volume_limit'
            }
        else:
            # Multiple volumes needed
            volumes_needed = math.ceil(total_storage_gb / max_volume_size)
            volume_size_gb = math.ceil(total_storage_gb / volumes_needed)
            
            # Check if we exceed per-instance volume count limit
            max_volumes_per_instance = self.ebs_constraints['max_volumes_per_instance']
            
            if volumes_needed <= max_volumes_per_instance:
                ebs_strategy['volume_distribution'] = {
                    'strategy': 'multiple_volumes_single_instance',
                    'volume_count': volumes_needed,
                    'volume_size_gb': volume_size_gb,
                    'striping_recommended': True,
                    'constraint_accommodation': f'Split across {volumes_needed} volumes'
                }
            else:
                # Need multiple instances
                instances_needed = math.ceil(volumes_needed / max_volumes_per_instance)
                volumes_per_instance = math.ceil(volumes_needed / instances_needed)
                
                ebs_strategy['volume_distribution'] = {
                    'strategy': 'multiple_volumes_multiple_instances',
                    'instances_needed': instances_needed,
                    'volumes_per_instance': volumes_per_instance,
                    'volume_size_gb': volume_size_gb,
                    'total_volumes': volumes_needed,
                    'constraint_accommodation': f'Distribute across {instances_needed} instances'
                }
                
                ebs_strategy['constraint_accommodations'].append({
                    'constraint': 'max_volumes_per_instance',
                    'limit': max_volumes_per_instance,
                    'accommodation': f'Use {instances_needed} instances to support {volumes_needed} volumes'
                })
        
        # Configure performance settings
        ebs_strategy['performance_configuration'] = self.configure_ebs_performance(
            volume_type, volume_size_gb, required_iops, required_throughput
        )
        
        # Configure availability settings
        ebs_strategy['availability_configuration'] = self.configure_ebs_availability(
            availability_requirements, ebs_strategy['volume_distribution']
        )
        
        return ebs_strategy
    
    def select_optimal_volume_type(self, required_iops: int, required_throughput: int) -> str:
        """Select optimal EBS volume type based on requirements"""
        
        # Check if io2 is needed for high IOPS
        if required_iops > 16000:
            return 'io2'
        
        # Check if io1/io2 is needed for consistent IOPS
        if required_iops > 10000:
            return 'io1'
        
        # Check if gp3 can meet requirements
        if required_iops <= 16000 and required_throughput <= 1000:
            return 'gp3'
        
        # Check if throughput-optimized is needed
        if required_throughput > 250:
            return 'st1'
        
        # Default to gp3 for general purpose
        return 'gp3'
    
    def configure_ebs_performance(self, volume_type: str, volume_size_gb: int,
                                required_iops: int, required_throughput: int) -> Dict[str, Any]:
        """Configure EBS performance within constraints"""
        
        performance_config = {
            'volume_type': volume_type,
            'volume_size_gb': volume_size_gb,
            'configured_iops': 0,
            'configured_throughput': 0,
            'performance_optimizations': [],
            'constraint_accommodations': []
        }
        
        max_iops = self.ebs_constraints['max_iops'].get(volume_type, 0)
        max_throughput = self.ebs_constraints['max_throughput'].get(volume_type, 0)
        
        # Configure IOPS
        if volume_type in ['gp3', 'io1', 'io2']:
            if volume_type == 'gp3':
                # gp3 baseline is 3000 IOPS, can provision up to 16000
                baseline_iops = min(3000, volume_size_gb * 3)  # 3 IOPS per GB baseline
                configured_iops = min(required_iops, max_iops)
                
                if configured_iops > baseline_iops:
                    performance_config['configured_iops'] = configured_iops
                    performance_config['performance_optimizations'].append(
                        f'Provisioned IOPS: {configured_iops} (above baseline {baseline_iops})'
                    )
            
            elif volume_type in ['io1', 'io2']:
                # io1/io2 require provisioned IOPS
                max_iops_for_size = volume_size_gb * (500 if volume_type == 'io2' else 50)
                configured_iops = min(required_iops, max_iops, max_iops_for_size)
                performance_config['configured_iops'] = configured_iops
                
                if configured_iops < required_iops:
                    performance_config['constraint_accommodations'].append({
                        'constraint': f'max_iops_for_{volume_type}',
                        'requested': required_iops,
                        'configured': configured_iops,
                        'accommodation': 'Use volume striping or larger volume size'
                    })
        
        # Configure throughput
        if volume_type == 'gp3' and max_throughput > 0:
            baseline_throughput = min(125, volume_size_gb * 0.25)  # 0.25 MB/s per GB baseline
            configured_throughput = min(required_throughput, max_throughput)
            
            if configured_throughput > baseline_throughput:
                performance_config['configured_throughput'] = configured_throughput
                performance_config['performance_optimizations'].append(
                    f'Provisioned throughput: {configured_throughput} MB/s (above baseline {baseline_throughput})'
                )
        
        return performance_config
    
    def configure_ebs_availability(self, availability_requirements: Dict[str, Any],
                                 volume_distribution: Dict[str, Any]) -> Dict[str, Any]:
        """Configure EBS availability within constraints"""
        
        availability_config = {
            'backup_strategy': {},
            'replication_strategy': {},
            'multi_az_strategy': {},
            'disaster_recovery': {}
        }
        
        # Configure backup strategy
        backup_frequency = availability_requirements.get('backup_frequency', 'daily')
        retention_days = availability_requirements.get('backup_retention_days', 30)
        
        availability_config['backup_strategy'] = {
            'snapshot_frequency': backup_frequency,
            'retention_days': retention_days,
            'cross_region_copy': availability_requirements.get('cross_region_backup', False),
            'encryption': True,
            'automation': 'aws_backup_or_dlm'
        }
        
        # Configure replication strategy
        if availability_requirements.get('high_availability', False):
            if volume_distribution['strategy'] == 'single_volume':
                availability_config['replication_strategy'] = {
                    'strategy': 'snapshot_based_replication',
                    'frequency': 'hourly',
                    'cross_az_copies': True,
                    'constraint_accommodation': 'EBS volumes are AZ-specific, use snapshots for cross-AZ'
                }
            else:
                availability_config['replication_strategy'] = {
                    'strategy': 'distributed_volumes_with_raid',
                    'raid_level': 'raid_1_or_raid_10',
                    'cross_az_distribution': True,
                    'constraint_accommodation': 'Distribute volumes across AZs for availability'
                }
        
        return availability_config
    
    def design_s3_storage_strategy(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Design S3 storage strategy within constraints"""
        
        s3_strategy = {
            'bucket_strategy': {},
            'object_size_strategy': {},
            'performance_strategy': {},
            'lifecycle_strategy': {},
            'constraint_accommodations': []
        }
        
        # Analyze object size requirements
        max_object_size_gb = requirements.get('max_object_size_gb', 1)
        total_objects = requirements.get('estimated_object_count', 1000)
        
        max_s3_object_size_gb = self.s3_constraints['max_object_size'] / (1024**3)  # Convert to GB
        
        if max_object_size_gb <= max_s3_object_size_gb:
            s3_strategy['object_size_strategy'] = {
                'strategy': 'standard_objects',
                'max_object_size_gb': max_object_size_gb,
                'constraint_accommodation': 'within_s3_object_size_limit'
            }
        else:
            # Need to split large objects
            parts_needed = math.ceil(max_object_size_gb / max_s3_object_size_gb)
            
            s3_strategy['object_size_strategy'] = {
                'strategy': 'multipart_upload_required',
                'max_object_size_gb': max_object_size_gb,
                'parts_per_object': parts_needed,
                'part_size_gb': max_s3_object_size_gb,
                'constraint_accommodation': f'Split objects into {parts_needed} parts'
            }
            
            s3_strategy['constraint_accommodations'].append({
                'constraint': 'max_s3_object_size',
                'limit_gb': max_s3_object_size_gb,
                'accommodation': f'Use multipart upload with {parts_needed} parts per object'
            })
        
        # Design bucket strategy
        s3_strategy['bucket_strategy'] = self.design_s3_bucket_strategy(
            total_objects, requirements
        )
        
        # Design performance strategy
        s3_strategy['performance_strategy'] = self.design_s3_performance_strategy(
            requirements
        )
        
        return s3_strategy
    
    def design_s3_bucket_strategy(self, total_objects: int, 
                                requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Design S3 bucket strategy for optimal performance"""
        
        bucket_strategy = {
            'bucket_count': 1,
            'naming_strategy': {},
            'partitioning_strategy': {},
            'performance_considerations': {}
        }
        
        # Determine if multiple buckets are needed for performance
        requests_per_second = requirements.get('requests_per_second', 100)
        
        if requests_per_second > 3500:  # S3 request rate scaling threshold
            # Multiple buckets for request rate distribution
            buckets_needed = math.ceil(requests_per_second / 3500)
            
            bucket_strategy.update({
                'bucket_count': buckets_needed,
                'naming_strategy': {
                    'pattern': 'application-name-bucket-{number}',
                    'distribution_method': 'hash_based_routing'
                },
                'performance_considerations': {
                    'reason': 'distribute_request_load',
                    'requests_per_bucket': requests_per_second / buckets_needed
                }
            })
        
        # Design key naming strategy for performance
        bucket_strategy['partitioning_strategy'] = {
            'key_prefix_strategy': 'random_prefix_or_reverse_timestamp',
            'partition_pattern': 'yyyy/mm/dd/hh',
            'hot_spotting_prevention': True,
            'constraint_accommodation': 'Avoid sequential key patterns for better performance'
        }
        
        return bucket_strategy
    
    def design_s3_performance_strategy(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Design S3 performance optimization strategy"""
        
        performance_strategy = {
            'transfer_acceleration': False,
            'multipart_upload_strategy': {},
            'request_optimization': {},
            'caching_strategy': {}
        }
        
        # Configure transfer acceleration
        if requirements.get('global_access', False):
            performance_strategy['transfer_acceleration'] = True
        
        # Configure multipart upload strategy
        large_objects = requirements.get('large_objects', False)
        if large_objects or requirements.get('max_object_size_gb', 0) > 0.1:  # > 100MB
            
            part_size_mb = min(100, max(5, requirements.get('max_object_size_gb', 1) * 1024 / 100))
            
            performance_strategy['multipart_upload_strategy'] = {
                'enabled': True,
                'part_size_mb': part_size_mb,
                'parallel_uploads': min(10, max(1, requirements.get('bandwidth_mbps', 100) // 10)),
                'constraint_accommodation': 'Use multipart for objects > 100MB'
            }
        
        # Configure request optimization
        performance_strategy['request_optimization'] = {
            'request_patterns': 'batch_operations_when_possible',
            'list_operations': 'use_pagination_with_max_keys_1000',
            'delete_operations': 'batch_delete_up_to_1000_objects',
            'constraint_accommodation': 'Respect S3 API rate limits and batch sizes'
        }
        
        return performance_strategy
    
    def design_storage_constraint_accommodations(self, ebs_design: Dict[str, Any],
                                               s3_design: Dict[str, Any],
                                               requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Design comprehensive storage constraint accommodations"""
        
        accommodations = {
            'volume_size_accommodations': [],
            'performance_accommodations': [],
            'availability_accommodations': [],
            'cost_optimization_accommodations': []
        }
        
        # Volume size accommodations
        if ebs_design['volume_distribution']['strategy'] != 'single_volume':
            accommodations['volume_size_accommodations'].append({
                'constraint': 'ebs_max_volume_size',
                'accommodation': ebs_design['volume_distribution']['constraint_accommodation'],
                'implementation': 'volume_striping_or_distribution'
            })
        
        # Performance accommodations
        ebs_perf_config = ebs_design.get('performance_configuration', {})
        for accommodation in ebs_perf_config.get('constraint_accommodations', []):
            accommodations['performance_accommodations'].append({
                'constraint': accommodation['constraint'],
                'accommodation': accommodation['accommodation'],
                'implementation': 'increase_volume_size_or_use_striping'
            })
        
        # S3 constraint accommodations
        for accommodation in s3_design.get('constraint_accommodations', []):
            accommodations['performance_accommodations'].append({
                'constraint': accommodation['constraint'],
                'accommodation': accommodation['accommodation'],
                'implementation': 'multipart_upload_or_object_splitting'
            })
        
        return accommodations
    
    def implement_volume_striping_solution(self, volume_config: Dict[str, Any]) -> Dict[str, Any]:
        """Implement volume striping solution for constraint accommodation"""
        
        striping_solution = {
            'solution_id': str(uuid.uuid4()),
            'implementation_timestamp': datetime.utcnow().isoformat(),
            'volume_configuration': volume_config,
            'striping_strategy': {},
            'performance_expectations': {},
            'implementation_steps': []
        }
        
        volume_count = volume_config['volume_count']
        volume_size_gb = volume_config['volume_size_gb']
        
        # Design striping strategy
        if volume_count <= 8:
            raid_level = 'raid_0'  # Performance focused
            usable_capacity = volume_count * volume_size_gb
            fault_tolerance = 'none'
        elif volume_count <= 16:
            raid_level = 'raid_10'  # Balance of performance and availability
            usable_capacity = (volume_count // 2) * volume_size_gb
            fault_tolerance = 'single_volume_failure'
        else:
            raid_level = 'raid_6'  # High availability
            usable_capacity = (volume_count - 2) * volume_size_gb
            fault_tolerance = 'dual_volume_failure'
        
        striping_solution['striping_strategy'] = {
            'raid_level': raid_level,
            'volume_count': volume_count,
            'volume_size_gb': volume_size_gb,
            'usable_capacity_gb': usable_capacity,
            'fault_tolerance': fault_tolerance,
            'stripe_size': '64KB'  # Optimal for most workloads
        }
        
        # Calculate performance expectations
        base_iops = volume_config.get('configured_iops', 3000)
        base_throughput = volume_config.get('configured_throughput', 125)
        
        if raid_level == 'raid_0':
            expected_iops = base_iops * volume_count
            expected_throughput = base_throughput * volume_count
        elif raid_level == 'raid_10':
            expected_iops = base_iops * (volume_count // 2)
            expected_throughput = base_throughput * (volume_count // 2)
        else:  # raid_6
            expected_iops = base_iops * (volume_count - 2)
            expected_throughput = base_throughput * (volume_count - 2)
        
        striping_solution['performance_expectations'] = {
            'expected_iops': expected_iops,
            'expected_throughput_mbps': expected_throughput,
            'latency_impact': 'minimal_for_sequential_io',
            'cpu_overhead': 'low_to_moderate'
        }
        
        # Generate implementation steps
        striping_solution['implementation_steps'] = [
            {
                'step': 1,
                'action': 'create_ebs_volumes',
                'description': f'Create {volume_count} EBS volumes of {volume_size_gb}GB each',
                'aws_cli_example': f'aws ec2 create-volume --size {volume_size_gb} --volume-type gp3'
            },
            {
                'step': 2,
                'action': 'attach_volumes_to_instance',
                'description': 'Attach all volumes to the target EC2 instance',
                'constraint_check': f'Ensure instance supports {volume_count} volumes'
            },
            {
                'step': 3,
                'action': 'configure_raid',
                'description': f'Configure {raid_level} using mdadm or LVM',
                'linux_example': f'mdadm --create /dev/md0 --level={raid_level.split("_")[1]} --raid-devices={volume_count} /dev/xvd[f-z]'
            },
            {
                'step': 4,
                'action': 'create_filesystem',
                'description': 'Create filesystem on the RAID device',
                'recommendation': 'Use XFS for large filesystems'
            },
            {
                'step': 5,
                'action': 'mount_and_configure',
                'description': 'Mount filesystem and configure for optimal performance',
                'performance_tuning': 'Configure appropriate mount options and I/O scheduler'
            }
        ]
        
        return striping_solution
    
    def store_storage_architecture(self, storage_architecture: Dict[str, Any]):
        """Store storage architecture design"""
        
        try:
            item = {
                'architecture_id': storage_architecture['architecture_id'],
                'design_timestamp': storage_architecture['design_timestamp'],
                'architecture_data': json.dumps(storage_architecture),
                'ttl': int((datetime.utcnow() + timedelta(days=365)).timestamp())
            }
            
            self.storage_table.put_item(Item=item)
        
        except Exception as e:
            print(f"Error storing storage architecture: {str(e)}")

def lambda_handler(event, context):
    """Lambda function for storage constraint management"""
    
    storage_manager = StorageConstraintManager()
    
    action = event.get('action', 'design_storage')
    
    if action == 'design_storage':
        requirements = event.get('requirements', {})
        result = storage_manager.design_storage_architecture(requirements)
    elif action == 'implement_striping':
        volume_config = event.get('volume_config', {})
        result = storage_manager.implement_volume_striping_solution(volume_config)
    else:
        result = {'error': 'Invalid action specified'}
    
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
```
### Example 4: Terraform configuration for constraint-aware infrastructure

```hcl
# terraform/constraint-aware-infrastructure.tf
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# Variables
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-west-2"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "production"
}

variable "total_storage_gb" {
  description = "Total storage requirement in GB"
  type        = number
  default     = 10000
}

variable "required_iops" {
  description = "Required IOPS"
  type        = number
  default     = 5000
}

variable "max_instances" {
  description = "Maximum number of instances"
  type        = number
  default     = 100
}

# Data sources
data "aws_availability_zones" "available" {
  state = "available"
}

data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]
  
  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}

# Local calculations for constraint accommodation
locals {
  # EBS constraints
  max_volume_size_gb = 16384  # 16 TiB for gp3
  max_volumes_per_instance = 28
  max_iops_per_volume = 16000
  
  # Calculate volume distribution
  volumes_needed = ceil(var.total_storage_gb / local.max_volume_size_gb)
  volume_size_gb = ceil(var.total_storage_gb / local.volumes_needed)
  
  # Calculate instance distribution if volumes exceed per-instance limit
  instances_needed = max(1, ceil(local.volumes_needed / local.max_volumes_per_instance))
  volumes_per_instance = ceil(local.volumes_needed / local.instances_needed)
  
  # AZ distribution
  available_azs = length(data.aws_availability_zones.available.names)
  azs_to_use = min(local.available_azs, 3)  # Use up to 3 AZs
  instances_per_az = ceil(local.instances_needed / local.azs_to_use)
  
  # Auto Scaling Group distribution
  max_instances_per_asg = 100  # Practical limit
  asgs_needed = ceil(var.max_instances / local.max_instances_per_asg)
  asgs_per_az = ceil(local.asgs_needed / local.azs_to_use)
  
  # Tags
  common_tags = {
    Environment = var.environment
    Project     = "constraint-aware-infrastructure"
    ManagedBy   = "Terraform"
  }
}

# VPC and networking
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = merge(local.common_tags, {
    Name = "${var.environment}-constraint-aware-vpc"
  })
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  
  tags = merge(local.common_tags, {
    Name = "${var.environment}-igw"
  })
}

# Subnets across multiple AZs
resource "aws_subnet" "public" {
  count = local.azs_to_use
  
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.${count.index + 1}.0/24"
  availability_zone       = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true
  
  tags = merge(local.common_tags, {
    Name = "${var.environment}-public-subnet-${count.index + 1}"
    Type = "Public"
    AZ   = data.aws_availability_zones.available.names[count.index]
  })
}

resource "aws_subnet" "private" {
  count = local.azs_to_use
  
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${count.index + 10}.0/24"
  availability_zone = data.aws_availability_zones.available.names[count.index]
  
  tags = merge(local.common_tags, {
    Name = "${var.environment}-private-subnet-${count.index + 1}"
    Type = "Private"
    AZ   = data.aws_availability_zones.available.names[count.index]
  })
}

# Route tables
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }
  
  tags = merge(local.common_tags, {
    Name = "${var.environment}-public-rt"
  })
}

resource "aws_route_table_association" "public" {
  count = local.azs_to_use
  
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

# NAT Gateways for private subnets
resource "aws_eip" "nat" {
  count = local.azs_to_use
  
  domain = "vpc"
  
  tags = merge(local.common_tags, {
    Name = "${var.environment}-nat-eip-${count.index + 1}"
  })
  
  depends_on = [aws_internet_gateway.main]
}

resource "aws_nat_gateway" "main" {
  count = local.azs_to_use
  
  allocation_id = aws_eip.nat[count.index].id
  subnet_id     = aws_subnet.public[count.index].id
  
  tags = merge(local.common_tags, {
    Name = "${var.environment}-nat-gateway-${count.index + 1}"
  })
}

resource "aws_route_table" "private" {
  count = local.azs_to_use
  
  vpc_id = aws_vpc.main.id
  
  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.main[count.index].id
  }
  
  tags = merge(local.common_tags, {
    Name = "${var.environment}-private-rt-${count.index + 1}"
  })
}

resource "aws_route_table_association" "private" {
  count = local.azs_to_use
  
  subnet_id      = aws_subnet.private[count.index].id
  route_table_id = aws_route_table.private[count.index].id
}

# Security groups
resource "aws_security_group" "web" {
  name_prefix = "${var.environment}-web-"
  vpc_id      = aws_vpc.main.id
  description = "Security group for web servers"
  
  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
    description = "HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = merge(local.common_tags, {
    Name = "${var.environment}-web-sg"
  })
  
  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_security_group" "app" {
  name_prefix = "${var.environment}-app-"
  vpc_id      = aws_vpc.main.id
  description = "Security group for application servers"
  
  ingress {
    description     = "App traffic from web tier"
    from_port       = 8080
    to_port         = 8080
    protocol        = "tcp"
    security_groups = [aws_security_group.web.id]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = merge(local.common_tags, {
    Name = "${var.environment}-app-sg"
  })
  
  lifecycle {
    create_before_destroy = true
  }
}

# Launch template with constraint-aware configuration
resource "aws_launch_template" "app" {
  name_prefix   = "${var.environment}-app-"
  image_id      = data.aws_ami.amazon_linux.id
  instance_type = "m5.large"  # Supports up to 3 ENIs, 28 EBS volumes
  
  vpc_security_group_ids = [aws_security_group.app.id]
  
  # EBS optimization for storage performance
  ebs_optimized = true
  
  # Block device mappings with constraint accommodation
  dynamic "block_device_mappings" {
    for_each = range(min(local.volumes_per_instance, local.max_volumes_per_instance))
    
    content {
      device_name = "/dev/sd${substr("fghijklmnopqrstuvwxyz", block_device_mappings.value, 1)}"
      
      ebs {
        volume_type           = "gp3"
        volume_size           = local.volume_size_gb
        iops                  = min(var.required_iops / local.volumes_per_instance, local.max_iops_per_volume)
        throughput            = min(250, local.volume_size_gb / 4)  # 0.25 MB/s per GB baseline
        delete_on_termination = true
        encrypted             = true
      }
    }
  }
  
  # User data for volume configuration
  user_data = base64encode(templatefile("${path.module}/user_data.sh", {
    volumes_count = min(local.volumes_per_instance, local.max_volumes_per_instance)
    raid_level    = local.volumes_per_instance > 1 ? "0" : "none"
  }))
  
  tag_specifications {
    resource_type = "instance"
    tags = merge(local.common_tags, {
      Name = "${var.environment}-app-instance"
    })
  }
  
  tag_specifications {
    resource_type = "volume"
    tags = merge(local.common_tags, {
      Name = "${var.environment}-app-volume"
    })
  }
  
  tags = merge(local.common_tags, {
    Name = "${var.environment}-app-launch-template"
  })
  
  lifecycle {
    create_before_destroy = true
  }
}

# Auto Scaling Groups distributed across AZs
resource "aws_autoscaling_group" "app" {
  count = local.asgs_needed
  
  name                = "${var.environment}-app-asg-${count.index + 1}"
  vpc_zone_identifier = [aws_subnet.private[count.index % local.azs_to_use].id]
  
  min_size         = 1
  max_size         = min(local.max_instances_per_asg, ceil(var.max_instances / local.asgs_needed))
  desired_capacity = max(2, ceil(var.max_instances / local.asgs_needed / 2))
  
  health_check_type         = "ELB"
  health_check_grace_period = 300
  
  launch_template {
    id      = aws_launch_template.app.id
    version = "$Latest"
  }
  
  # Instance refresh for rolling updates
  instance_refresh {
    strategy = "Rolling"
    preferences {
      min_healthy_percentage = 50
      instance_warmup        = 300
    }
  }
  
  # Constraint-aware scaling policies
  tag {
    key                 = "Name"
    value               = "${var.environment}-app-asg-${count.index + 1}"
    propagate_at_launch = true
  }
  
  tag {
    key                 = "Environment"
    value               = var.environment
    propagate_at_launch = true
  }
  
  tag {
    key                 = "ConstraintGroup"
    value               = "asg-${count.index + 1}"
    propagate_at_launch = true
  }
  
  lifecycle {
    create_before_destroy = true
  }
}

# Target tracking scaling policies
resource "aws_autoscaling_policy" "scale_out" {
  count = local.asgs_needed
  
  name                   = "${var.environment}-scale-out-${count.index + 1}"
  scaling_adjustment     = 2
  adjustment_type        = "ChangeInCapacity"
  cooldown              = 300
  autoscaling_group_name = aws_autoscaling_group.app[count.index].name
  policy_type           = "SimpleScaling"
}

resource "aws_autoscaling_policy" "scale_in" {
  count = local.asgs_needed
  
  name                   = "${var.environment}-scale-in-${count.index + 1}"
  scaling_adjustment     = -1
  adjustment_type        = "ChangeInCapacity"
  cooldown              = 600
  autoscaling_group_name = aws_autoscaling_group.app[count.index].name
  policy_type           = "SimpleScaling"
}

# CloudWatch alarms for scaling
resource "aws_cloudwatch_metric_alarm" "high_cpu" {
  count = local.asgs_needed
  
  alarm_name          = "${var.environment}-high-cpu-${count.index + 1}"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = "300"
  statistic           = "Average"
  threshold           = "80"
  alarm_description   = "This metric monitors ec2 cpu utilization"
  alarm_actions       = [aws_autoscaling_policy.scale_out[count.index].arn]
  
  dimensions = {
    AutoScalingGroupName = aws_autoscaling_group.app[count.index].name
  }
  
  tags = local.common_tags
}

resource "aws_cloudwatch_metric_alarm" "low_cpu" {
  count = local.asgs_needed
  
  alarm_name          = "${var.environment}-low-cpu-${count.index + 1}"
  comparison_operator = "LessThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = "300"
  statistic           = "Average"
  threshold           = "20"
  alarm_description   = "This metric monitors ec2 cpu utilization"
  alarm_actions       = [aws_autoscaling_policy.scale_in[count.index].arn]
  
  dimensions = {
    AutoScalingGroupName = aws_autoscaling_group.app[count.index].name
  }
  
  tags = local.common_tags
}

# Application Load Balancer
resource "aws_lb" "app" {
  name               = "${var.environment}-app-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.web.id]
  subnets            = aws_subnet.public[*].id
  
  enable_deletion_protection = false
  
  tags = merge(local.common_tags, {
    Name = "${var.environment}-app-alb"
  })
}

# Target groups for each ASG (constraint accommodation)
resource "aws_lb_target_group" "app" {
  count = local.asgs_needed
  
  name     = "${var.environment}-app-tg-${count.index + 1}"
  port     = 8080
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id
  
  health_check {
    enabled             = true
    healthy_threshold   = 2
    unhealthy_threshold = 3
    timeout             = 5
    interval            = 30
    path                = "/health"
    matcher             = "200"
    port                = "traffic-port"
    protocol            = "HTTP"
  }
  
  tags = merge(local.common_tags, {
    Name = "${var.environment}-app-tg-${count.index + 1}"
  })
}

# Attach ASGs to target groups
resource "aws_autoscaling_attachment" "app" {
  count = local.asgs_needed
  
  autoscaling_group_name = aws_autoscaling_group.app[count.index].id
  lb_target_group_arn    = aws_lb_target_group.app[count.index].arn
}

# ALB listener with weighted routing across target groups
resource "aws_lb_listener" "app" {
  load_balancer_arn = aws_lb.app.arn
  port              = "80"
  protocol          = "HTTP"
  
  default_action {
    type = "forward"
    
    forward {
      dynamic "target_group" {
        for_each = aws_lb_target_group.app
        
        content {
          arn    = target_group.value.arn
          weight = 100 / local.asgs_needed  # Equal weight distribution
        }
      }
    }
  }
  
  tags = local.common_tags
}

# S3 bucket with constraint-aware configuration
resource "aws_s3_bucket" "app_data" {
  bucket = "${var.environment}-app-data-${random_id.bucket_suffix.hex}"
  
  tags = merge(local.common_tags, {
    Name = "${var.environment}-app-data"
  })
}

resource "random_id" "bucket_suffix" {
  byte_length = 4
}

resource "aws_s3_bucket_versioning" "app_data" {
  bucket = aws_s3_bucket.app_data.id
  
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "app_data" {
  bucket = aws_s3_bucket.app_data.id
  
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# S3 bucket policy for constraint accommodation
resource "aws_s3_bucket_policy" "app_data" {
  bucket = aws_s3_bucket.app_data.id
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "DenyInsecureConnections"
        Effect = "Deny"
        Principal = "*"
        Action = "s3:*"
        Resource = [
          aws_s3_bucket.app_data.arn,
          "${aws_s3_bucket.app_data.arn}/*"
        ]
        Condition = {
          Bool = {
            "aws:SecureTransport" = "false"
          }
        }
      }
    ]
  })
}

# Outputs
output "constraint_analysis" {
  description = "Analysis of constraints and accommodations"
  value = {
    storage_constraints = {
      total_storage_gb         = var.total_storage_gb
      max_volume_size_gb      = local.max_volume_size_gb
      volumes_needed          = local.volumes_needed
      volume_size_gb          = local.volume_size_gb
      instances_needed        = local.instances_needed
      volumes_per_instance    = local.volumes_per_instance
    }
    
    scaling_constraints = {
      max_instances           = var.max_instances
      max_instances_per_asg   = local.max_instances_per_asg
      asgs_needed            = local.asgs_needed
      asgs_per_az            = local.asgs_per_az
    }
    
    availability_constraints = {
      available_azs          = local.available_azs
      azs_to_use            = local.azs_to_use
      instances_per_az      = local.instances_per_az
    }
  }
}

output "infrastructure_endpoints" {
  description = "Infrastructure endpoints"
  value = {
    load_balancer_dns = aws_lb.app.dns_name
    s3_bucket_name   = aws_s3_bucket.app_data.id
    vpc_id           = aws_vpc.main.id
  }
}

output "constraint_accommodations" {
  description = "How constraints were accommodated"
  value = {
    storage_accommodation = local.volumes_needed > 1 ? "Multiple volumes with RAID configuration" : "Single volume sufficient"
    scaling_accommodation = local.asgs_needed > 1 ? "Multiple ASGs to distribute load" : "Single ASG sufficient"
    availability_accommodation = "Distributed across ${local.azs_to_use} Availability Zones"
  }
}
```

```bash
#!/bin/bash
# user_data.sh - User data script for volume configuration

set -euo pipefail

# Variables from Terraform
VOLUMES_COUNT=${volumes_count}
RAID_LEVEL=${raid_level}

# Log function
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a /var/log/volume-setup.log
}

log "Starting volume configuration with $VOLUMES_COUNT volumes, RAID level: $RAID_LEVEL"

# Update system
yum update -y
yum install -y mdadm xfsprogs

# Wait for volumes to be available
sleep 30

# Discover attached volumes (excluding root volume)
VOLUMES=($(lsblk -dn -o NAME | grep -v nvme0n1 | grep -v xvda | head -n $VOLUMES_COUNT))

log "Discovered volumes: ${VOLUMES[*]}"

if [ ${#VOLUMES[@]} -eq 0 ]; then
    log "ERROR: No additional volumes found"
    exit 1
fi

# Configure storage based on volume count and RAID level
if [ "$RAID_LEVEL" = "none" ] || [ ${#VOLUMES[@]} -eq 1 ]; then
    # Single volume configuration
    DEVICE="/dev/${VOLUMES[0]}"
    log "Configuring single volume: $DEVICE"
    
    # Create filesystem
    mkfs.xfs -f $DEVICE
    
    # Create mount point
    mkdir -p /data
    
    # Mount volume
    mount $DEVICE /data
    
    # Add to fstab
    echo "$DEVICE /data xfs defaults,noatime 0 2" >> /etc/fstab
    
else
    # RAID configuration
    log "Configuring RAID $RAID_LEVEL with ${#VOLUMES[@]} volumes"
    
    # Prepare device list for mdadm
    DEVICE_LIST=""
    for vol in "${VOLUMES[@]}"; do
        DEVICE_LIST="$DEVICE_LIST /dev/$vol"
    done
    
    log "Creating RAID array with devices: $DEVICE_LIST"
    
    # Create RAID array
    mdadm --create /dev/md0 \
        --level=$RAID_LEVEL \
        --raid-devices=${#VOLUMES[@]} \
        $DEVICE_LIST \
        --assume-clean
    
    # Wait for array to be ready
    sleep 10
    
    # Create filesystem on RAID device
    mkfs.xfs -f /dev/md0
    
    # Create mount point
    mkdir -p /data
    
    # Mount RAID device
    mount /dev/md0 /data
    
    # Add to fstab
    echo "/dev/md0 /data xfs defaults,noatime 0 2" >> /etc/fstab
    
    # Save RAID configuration
    mdadm --detail --scan >> /etc/mdadm.conf
fi

# Set permissions
chown -R ec2-user:ec2-user /data
chmod 755 /data

# Configure I/O scheduler for optimal performance
for vol in "${VOLUMES[@]}"; do
    echo mq-deadline > /sys/block/$vol/queue/scheduler
done

log "Volume configuration completed successfully"

# Install and start application (placeholder)
log "Installing application dependencies"
yum install -y docker
systemctl start docker
systemctl enable docker

# Add ec2-user to docker group
usermod -a -G docker ec2-user

log "System configuration completed"
```

## AWS services to consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon EC2</h4>
    <p>Compute service with fixed constraints on instance types, network interfaces, and EBS volume attachments that require architectural accommodation.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon EBS</h4>
    <p>Block storage service with fixed volume size limits, IOPS limits, and throughput constraints that require volume striping or distribution strategies.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon S3</h4>
    <p>Object storage service with fixed object size limits and request rate constraints that require multipart uploads and request distribution.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Auto Scaling</h4>
    <p>Scaling service that must work within fixed constraints like launch rates, cooldown periods, and capacity limits per Auto Scaling Group.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Elastic Load Balancing</h4>
    <p>Load balancing service with constraints on targets per target group and target groups per load balancer requiring distribution strategies.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon VPC</h4>
    <p>Networking service with fixed constraints on subnets, route tables, and security groups per VPC requiring multi-VPC architectures for scale.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Lambda</h4>
    <p>Serverless compute service for implementing constraint-aware logic and automation without managing infrastructure constraints.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon DynamoDB</h4>
    <p>NoSQL database service for storing architecture decisions and constraint accommodation strategies.</p>
  </div>
</div>

## Benefits of accommodating fixed service quotas through architecture

- **Unlimited scalability**: Enables scaling beyond individual service limits through architectural patterns
- **Improved reliability**: Reduces single points of failure by distributing across constraint boundaries
- **Enhanced performance**: Optimizes resource utilization within fixed constraints
- **Cost efficiency**: Maximizes value from available resources without over-provisioning
- **Future-proofing**: Creates flexible architectures that can adapt to changing constraints
- **Operational simplicity**: Automates constraint accommodation reducing manual intervention
- **Better resource utilization**: Efficiently uses available capacity across multiple constraint boundaries
- **Reduced risk**: Prevents service disruptions due to hitting fixed limits

## Related resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/rel_manage_service_limits_aware_fixed_limits.html">AWS Well-Architected Framework - Accommodate fixed service quotas and constraints through architecture</a></li>
    <li><a href="https://docs.aws.amazon.com/general/latest/gr/aws-service-information.html">AWS Service Information and Quotas</a></li>
    <li><a href="https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-volume-types.html">Amazon EBS Volume Types</a></li>
    <li><a href="https://docs.aws.amazon.com/AmazonS3/latest/userguide/qfacts.html">Amazon S3 Performance Guidelines</a></li>
    <li><a href="https://aws.amazon.com/blogs/storage/optimizing-amazon-ebs-performance/">Optimizing Amazon EBS Performance</a></li>
    <li><a href="https://docs.aws.amazon.com/autoscaling/ec2/userguide/auto-scaling-benefits.html">Benefits of Auto Scaling</a></li>
  </ul>
</div>
