---
title: REL11-BP07 - Architect your product to meet availability targets and uptime service level agreements (SLAs)
layout: default
parent: REL11 - How do you design your workload to withstand component failures?
nav_order: 7
---

# REL11-BP07: Architect your product to meet availability targets and uptime service level agreements (SLAs)

Design your architecture with specific availability targets and SLA requirements in mind. This includes calculating expected availability, implementing appropriate redundancy, establishing recovery time objectives (RTO) and recovery point objectives (RPO), and continuously measuring and optimizing to meet commitments.

## Implementation Steps

### 1. Define Availability Requirements
Establish clear availability targets, SLAs, and service level objectives (SLOs).

### 2. Calculate System Availability
Model your architecture to predict overall system availability based on component reliability.

### 3. Implement Redundancy Strategy
Design redundancy at appropriate levels to meet availability targets.

### 4. Establish RTO and RPO
Define recovery time and data loss objectives for different failure scenarios.

### 5. Monitor and Measure SLA Compliance
Implement continuous monitoring to track SLA performance and identify improvement areas.

## Detailed Implementation

{% raw %}
```python
import boto3
import json
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import threading
import math
import statistics
from concurrent.futures import ThreadPoolExecutor

class AvailabilityTier(Enum):
    BASIC = "basic"          # 99.0% - 87.6 hours downtime/year
    STANDARD = "standard"    # 99.9% - 8.76 hours downtime/year
    HIGH = "high"           # 99.95% - 4.38 hours downtime/year
    CRITICAL = "critical"   # 99.99% - 52.56 minutes downtime/year
    MISSION_CRITICAL = "mission_critical"  # 99.999% - 5.26 minutes downtime/year

class ComponentType(Enum):
    COMPUTE = "compute"
    DATABASE = "database"
    STORAGE = "storage"
    NETWORK = "network"
    LOAD_BALANCER = "load_balancer"
    CDN = "cdn"
    DNS = "dns"

class RedundancyPattern(Enum):
    SINGLE_INSTANCE = "single_instance"
    ACTIVE_PASSIVE = "active_passive"
    ACTIVE_ACTIVE = "active_active"
    MULTI_AZ = "multi_az"
    MULTI_REGION = "multi_region"

@dataclass
class SLARequirement:
    service_name: str
    availability_target: float  # e.g., 99.9 for 99.9%
    rto_minutes: int           # Recovery Time Objective
    rpo_minutes: int           # Recovery Point Objective
    measurement_period: str    # monthly, quarterly, yearly
    penalties: Dict[str, float]  # SLA penalties for breaches
    exclusions: List[str]      # Planned maintenance exclusions

@dataclass
class ComponentReliability:
    component_id: str
    component_type: ComponentType
    base_availability: float
    redundancy_pattern: RedundancyPattern
    mtbf_hours: float         # Mean Time Between Failures
    mttr_minutes: float       # Mean Time To Repair
    dependencies: List[str]
    aws_service: str

@dataclass
class AvailabilityMeasurement:
    timestamp: datetime
    service_name: str
    availability_percentage: float
    downtime_minutes: float
    incident_count: int
    sla_breach: bool
    measurement_period: str

class SLAArchitectureSystem:
    def __init__(self, region: str = 'us-east-1'):
        self.region = region
        
        # AWS clients
        self.cloudwatch = boto3.client('cloudwatch', region_name=region)
        self.route53 = boto3.client('route53')
        self.ec2 = boto3.client('ec2', region_name=region)
        self.rds = boto3.client('rds', region_name=region)
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # SLA tracking
        self.sla_requirements: Dict[str, SLARequirement] = {}
        self.component_reliability: Dict[str, ComponentReliability] = {}
        self.availability_measurements: List[AvailabilityMeasurement] = []
        
        # Architecture modeling
        self.system_architecture: Dict[str, Any] = {}
        self.availability_calculations: Dict[str, float] = {}
        
        # Thread safety
        self.sla_lock = threading.Lock()

    def define_sla_requirement(self, requirement: SLARequirement) -> bool:
        """Define SLA requirement for a service"""
        try:
            self.sla_requirements[requirement.service_name] = requirement
            self.logger.info(f"Defined SLA requirement for {requirement.service_name}: {requirement.availability_target}%")
            return True
        except Exception as e:
            self.logger.error(f"Failed to define SLA requirement: {str(e)}")
            return False

    def register_component_reliability(self, component: ComponentReliability) -> bool:
        """Register component reliability characteristics"""
        try:
            self.component_reliability[component.component_id] = component
            self.logger.info(f"Registered component reliability: {component.component_id}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to register component reliability: {str(e)}")
            return False

    def calculate_system_availability(self, architecture_config: Dict[str, Any]) -> Dict[str, float]:
        """Calculate expected system availability based on architecture"""
        try:
            availability_results = {}
            
            for service_name, service_config in architecture_config.items():
                # Calculate availability for each service
                service_availability = self._calculate_service_availability(service_config)
                availability_results[service_name] = service_availability
                
                # Store calculation
                self.availability_calculations[service_name] = service_availability
                
                self.logger.info(f"Calculated availability for {service_name}: {service_availability:.4f}%")
            
            return availability_results
            
        except Exception as e:
            self.logger.error(f"System availability calculation failed: {str(e)}")
            return {}

    def design_redundancy_strategy(self, service_name: str, target_availability: float) -> Dict[str, Any]:
        """Design redundancy strategy to meet availability target"""
        try:
            sla_requirement = self.sla_requirements.get(service_name)
            if not sla_requirement:
                raise ValueError(f"No SLA requirement defined for {service_name}")
            
            redundancy_strategy = {
                'service_name': service_name,
                'target_availability': target_availability,
                'recommended_patterns': [],
                'architecture_recommendations': [],
                'estimated_cost_impact': 0.0
            }
            
            # Determine required availability tier
            availability_tier = self._determine_availability_tier(target_availability)
            
            # Generate redundancy recommendations based on tier
            if availability_tier == AvailabilityTier.BASIC:
                redundancy_strategy['recommended_patterns'] = [
                    RedundancyPattern.SINGLE_INSTANCE,
                    RedundancyPattern.ACTIVE_PASSIVE
                ]
                redundancy_strategy['architecture_recommendations'] = [
                    "Single AZ deployment with backup instances",
                    "Regular automated backups",
                    "Basic monitoring and alerting"
                ]
                redundancy_strategy['estimated_cost_impact'] = 1.2
                
            elif availability_tier == AvailabilityTier.STANDARD:
                redundancy_strategy['recommended_patterns'] = [
                    RedundancyPattern.ACTIVE_PASSIVE,
                    RedundancyPattern.MULTI_AZ
                ]
                redundancy_strategy['architecture_recommendations'] = [
                    "Multi-AZ deployment with automatic failover",
                    "Load balancer with health checks",
                    "Database with read replicas",
                    "Comprehensive monitoring and alerting"
                ]
                redundancy_strategy['estimated_cost_impact'] = 1.8
                
            elif availability_tier == AvailabilityTier.HIGH:
                redundancy_strategy['recommended_patterns'] = [
                    RedundancyPattern.ACTIVE_ACTIVE,
                    RedundancyPattern.MULTI_AZ
                ]
                redundancy_strategy['architecture_recommendations'] = [
                    "Active-active multi-AZ deployment",
                    "Auto Scaling with multiple AZs",
                    "Database clustering with automatic failover",
                    "CDN for static content",
                    "Advanced monitoring with predictive alerting"
                ]
                redundancy_strategy['estimated_cost_impact'] = 2.5
                
            elif availability_tier in [AvailabilityTier.CRITICAL, AvailabilityTier.MISSION_CRITICAL]:
                redundancy_strategy['recommended_patterns'] = [
                    RedundancyPattern.ACTIVE_ACTIVE,
                    RedundancyPattern.MULTI_REGION
                ]
                redundancy_strategy['architecture_recommendations'] = [
                    "Multi-region active-active deployment",
                    "Global load balancing with Route 53",
                    "Cross-region database replication",
                    "Disaster recovery automation",
                    "Chaos engineering and fault injection testing",
                    "24/7 monitoring and on-call support"
                ]
                redundancy_strategy['estimated_cost_impact'] = 4.0
            
            self.logger.info(f"Generated redundancy strategy for {service_name}")
            return redundancy_strategy
            
        except Exception as e:
            self.logger.error(f"Redundancy strategy design failed: {str(e)}")
            return {}

    def implement_sla_monitoring(self, service_name: str) -> Dict[str, Any]:
        """Implement SLA monitoring and measurement"""
        try:
            sla_requirement = self.sla_requirements.get(service_name)
            if not sla_requirement:
                raise ValueError(f"No SLA requirement defined for {service_name}")
            
            monitoring_config = {
                'service_name': service_name,
                'cloudwatch_alarms': [],
                'synthetic_monitors': [],
                'dashboards': [],
                'reports': []
            }
            
            # Create availability monitoring alarms
            availability_alarm = self._create_availability_alarm(service_name, sla_requirement)
            monitoring_config['cloudwatch_alarms'].append(availability_alarm)
            
            # Create RTO monitoring
            rto_alarm = self._create_rto_alarm(service_name, sla_requirement)
            monitoring_config['cloudwatch_alarms'].append(rto_alarm)
            
            # Create synthetic monitoring
            synthetic_monitors = self._create_synthetic_monitors(service_name, sla_requirement)
            monitoring_config['synthetic_monitors'].extend(synthetic_monitors)
            
            # Create SLA dashboard
            dashboard = self._create_sla_dashboard(service_name, sla_requirement)
            monitoring_config['dashboards'].append(dashboard)
            
            # Set up automated reporting
            report_config = self._setup_sla_reporting(service_name, sla_requirement)
            monitoring_config['reports'].append(report_config)
            
            self.logger.info(f"Implemented SLA monitoring for {service_name}")
            return monitoring_config
            
        except Exception as e:
            self.logger.error(f"SLA monitoring implementation failed: {str(e)}")
            return {}

    def measure_sla_compliance(self, service_name: str, measurement_period: str) -> Dict[str, Any]:
        """Measure SLA compliance for a service"""
        try:
            sla_requirement = self.sla_requirements.get(service_name)
            if not sla_requirement:
                raise ValueError(f"No SLA requirement defined for {service_name}")
            
            # Get measurement period dates
            start_date, end_date = self._get_measurement_period_dates(measurement_period)
            
            # Collect availability data
            availability_data = self._collect_availability_data(service_name, start_date, end_date)
            
            # Calculate metrics
            total_minutes = (end_date - start_date).total_seconds() / 60
            downtime_minutes = sum(data['downtime_minutes'] for data in availability_data)
            uptime_minutes = total_minutes - downtime_minutes
            availability_percentage = (uptime_minutes / total_minutes) * 100
            
            # Check SLA compliance
            sla_breach = availability_percentage < sla_requirement.availability_target
            
            # Calculate SLA credits/penalties
            penalty_amount = 0.0
            if sla_breach:
                penalty_amount = self._calculate_sla_penalty(
                    sla_requirement, 
                    availability_percentage
                )
            
            compliance_result = {
                'service_name': service_name,
                'measurement_period': measurement_period,
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat(),
                'target_availability': sla_requirement.availability_target,
                'actual_availability': availability_percentage,
                'total_minutes': total_minutes,
                'uptime_minutes': uptime_minutes,
                'downtime_minutes': downtime_minutes,
                'sla_breach': sla_breach,
                'penalty_amount': penalty_amount,
                'incident_count': len(availability_data),
                'mttr_minutes': statistics.mean([data['mttr_minutes'] for data in availability_data]) if availability_data else 0,
                'rto_compliance': all(data['rto_met'] for data in availability_data),
                'rpo_compliance': all(data['rpo_met'] for data in availability_data)
            }
            
            # Store measurement
            measurement = AvailabilityMeasurement(
                timestamp=datetime.utcnow(),
                service_name=service_name,
                availability_percentage=availability_percentage,
                downtime_minutes=downtime_minutes,
                incident_count=len(availability_data),
                sla_breach=sla_breach,
                measurement_period=measurement_period
            )
            
            with self.sla_lock:
                self.availability_measurements.append(measurement)
            
            self.logger.info(f"Measured SLA compliance for {service_name}: {availability_percentage:.4f}%")
            return compliance_result
            
        except Exception as e:
            self.logger.error(f"SLA compliance measurement failed: {str(e)}")
            return {}

    def optimize_for_sla_compliance(self, service_name: str) -> Dict[str, Any]:
        """Analyze and recommend optimizations for SLA compliance"""
        try:
            # Get recent measurements
            recent_measurements = [
                m for m in self.availability_measurements 
                if m.service_name == service_name and 
                m.timestamp > datetime.utcnow() - timedelta(days=90)
            ]
            
            if not recent_measurements:
                return {'error': 'No recent measurements available'}
            
            # Analyze trends
            availability_trend = [m.availability_percentage for m in recent_measurements]
            downtime_trend = [m.downtime_minutes for m in recent_measurements]
            
            # Calculate statistics
            avg_availability = statistics.mean(availability_trend)
            availability_variance = statistics.variance(availability_trend) if len(availability_trend) > 1 else 0
            total_incidents = sum(m.incident_count for m in recent_measurements)
            
            # Generate recommendations
            recommendations = []
            
            sla_requirement = self.sla_requirements.get(service_name)
            if sla_requirement:
                availability_gap = sla_requirement.availability_target - avg_availability
                
                if availability_gap > 0:
                    if availability_gap > 1.0:  # More than 1% gap
                        recommendations.append({
                            'priority': 'high',
                            'category': 'architecture',
                            'recommendation': 'Consider multi-region deployment for higher availability',
                            'estimated_improvement': '0.5-1.0% availability increase',
                            'implementation_effort': 'high'
                        })
                    
                    if availability_variance > 0.1:  # High variance
                        recommendations.append({
                            'priority': 'medium',
                            'category': 'monitoring',
                            'recommendation': 'Implement predictive alerting to reduce MTTR',
                            'estimated_improvement': '10-20% MTTR reduction',
                            'implementation_effort': 'medium'
                        })
                    
                    if total_incidents > 10:  # High incident count
                        recommendations.append({
                            'priority': 'high',
                            'category': 'reliability',
                            'recommendation': 'Implement chaos engineering to identify weak points',
                            'estimated_improvement': '20-30% incident reduction',
                            'implementation_effort': 'medium'
                        })
            
            optimization_result = {
                'service_name': service_name,
                'analysis_period': '90 days',
                'current_performance': {
                    'average_availability': avg_availability,
                    'availability_variance': availability_variance,
                    'total_incidents': total_incidents,
                    'average_downtime_per_incident': statistics.mean(downtime_trend) if downtime_trend else 0
                },
                'sla_gap': availability_gap if sla_requirement else None,
                'recommendations': recommendations,
                'next_review_date': (datetime.utcnow() + timedelta(days=30)).isoformat()
            }
            
            self.logger.info(f"Generated SLA optimization recommendations for {service_name}")
            return optimization_result
            
        except Exception as e:
            self.logger.error(f"SLA optimization analysis failed: {str(e)}")
            return {}

    def _calculate_service_availability(self, service_config: Dict[str, Any]) -> float:
        """Calculate availability for a service configuration"""
        try:
            components = service_config.get('components', [])
            topology = service_config.get('topology', 'series')
            
            if topology == 'series':
                # Series configuration - multiply availabilities
                total_availability = 1.0
                for component_id in components:
                    component = self.component_reliability.get(component_id)
                    if component:
                        component_availability = self._calculate_component_availability(component)
                        total_availability *= (component_availability / 100.0)
                return total_availability * 100.0
                
            elif topology == 'parallel':
                # Parallel configuration - calculate combined availability
                total_unavailability = 1.0
                for component_id in components:
                    component = self.component_reliability.get(component_id)
                    if component:
                        component_availability = self._calculate_component_availability(component)
                        component_unavailability = 1.0 - (component_availability / 100.0)
                        total_unavailability *= component_unavailability
                return (1.0 - total_unavailability) * 100.0
                
            elif topology == 'mixed':
                # Mixed topology - calculate based on configuration
                return self._calculate_mixed_topology_availability(service_config)
            
            return 99.0  # Default fallback
            
        except Exception as e:
            self.logger.error(f"Service availability calculation failed: {str(e)}")
            return 99.0

    def _calculate_component_availability(self, component: ComponentReliability) -> float:
        """Calculate availability for a single component"""
        try:
            base_availability = component.base_availability
            
            # Apply redundancy pattern multiplier
            if component.redundancy_pattern == RedundancyPattern.SINGLE_INSTANCE:
                return base_availability
            elif component.redundancy_pattern == RedundancyPattern.ACTIVE_PASSIVE:
                # Assume 99.9% failover success rate
                return base_availability + (100.0 - base_availability) * 0.999
            elif component.redundancy_pattern == RedundancyPattern.ACTIVE_ACTIVE:
                # Calculate parallel availability
                unavailability = (100.0 - base_availability) / 100.0
                combined_unavailability = unavailability * unavailability
                return (1.0 - combined_unavailability) * 100.0
            elif component.redundancy_pattern == RedundancyPattern.MULTI_AZ:
                # Multi-AZ typically provides 99.99% availability
                return min(99.99, base_availability * 1.1)
            elif component.redundancy_pattern == RedundancyPattern.MULTI_REGION:
                # Multi-region provides highest availability
                return min(99.999, base_availability * 1.2)
            
            return base_availability
            
        except Exception as e:
            self.logger.error(f"Component availability calculation failed: {str(e)}")
            return component.base_availability

    def _determine_availability_tier(self, target_availability: float) -> AvailabilityTier:
        """Determine availability tier based on target"""
        if target_availability >= 99.999:
            return AvailabilityTier.MISSION_CRITICAL
        elif target_availability >= 99.99:
            return AvailabilityTier.CRITICAL
        elif target_availability >= 99.95:
            return AvailabilityTier.HIGH
        elif target_availability >= 99.9:
            return AvailabilityTier.STANDARD
        else:
            return AvailabilityTier.BASIC

    def _create_availability_alarm(self, service_name: str, sla_requirement: SLARequirement) -> str:
        """Create CloudWatch alarm for availability monitoring"""
        try:
            alarm_name = f"{service_name}-availability-sla"
            
            response = self.cloudwatch.put_metric_alarm(
                AlarmName=alarm_name,
                ComparisonOperator='LessThanThreshold',
                EvaluationPeriods=1,
                MetricName='Availability',
                Namespace=f'SLA/{service_name}',
                Period=3600,  # 1 hour
                Statistic='Average',
                Threshold=sla_requirement.availability_target,
                ActionsEnabled=True,
                AlarmActions=[
                    f'arn:aws:sns:{self.region}:123456789012:sla-breach-alerts'
                ],
                AlarmDescription=f'SLA availability breach for {service_name}',
                Unit='Percent'
            )
            
            return alarm_name
            
        except Exception as e:
            self.logger.error(f"Availability alarm creation failed: {str(e)}")
            return ""

    def _calculate_sla_penalty(self, sla_requirement: SLARequirement, actual_availability: float) -> float:
        """Calculate SLA penalty based on availability breach"""
        try:
            availability_gap = sla_requirement.availability_target - actual_availability
            
            # Apply penalty tiers from SLA requirement
            penalty = 0.0
            for threshold, penalty_rate in sla_requirement.penalties.items():
                threshold_value = float(threshold)
                if availability_gap >= threshold_value:
                    penalty = penalty_rate
            
            return penalty
            
        except Exception as e:
            self.logger.error(f"SLA penalty calculation failed: {str(e)}")
            return 0.0

    def get_sla_dashboard_data(self, service_name: str) -> Dict[str, Any]:
        """Get dashboard data for SLA monitoring"""
        try:
            sla_requirement = self.sla_requirements.get(service_name)
            if not sla_requirement:
                return {}
            
            # Get recent measurements
            recent_measurements = [
                m for m in self.availability_measurements 
                if m.service_name == service_name and 
                m.timestamp > datetime.utcnow() - timedelta(days=30)
            ]
            
            dashboard_data = {
                'service_name': service_name,
                'sla_target': sla_requirement.availability_target,
                'current_availability': recent_measurements[-1].availability_percentage if recent_measurements else 0,
                'availability_trend': [
                    {
                        'timestamp': m.timestamp.isoformat(),
                        'availability': m.availability_percentage
                    }
                    for m in recent_measurements
                ],
                'incident_count_30d': sum(m.incident_count for m in recent_measurements),
                'total_downtime_30d': sum(m.downtime_minutes for m in recent_measurements),
                'sla_breach_count': len([m for m in recent_measurements if m.sla_breach]),
                'rto_target': sla_requirement.rto_minutes,
                'rpo_target': sla_requirement.rpo_minutes
            }
            
            return dashboard_data
            
        except Exception as e:
            self.logger.error(f"Dashboard data retrieval failed: {str(e)}")
            return {}

# Example usage
def main():
    # Initialize SLA architecture system
    sla_system = SLAArchitectureSystem(region='us-east-1')
    
    # Define SLA requirements
    web_app_sla = SLARequirement(
        service_name='web_application',
        availability_target=99.9,
        rto_minutes=15,
        rpo_minutes=60,
        measurement_period='monthly',
        penalties={
            '0.1': 0.05,  # 5% penalty for 0.1% breach
            '0.5': 0.10,  # 10% penalty for 0.5% breach
            '1.0': 0.25   # 25% penalty for 1.0% breach
        },
        exclusions=['planned_maintenance']
    )
    
    sla_system.define_sla_requirement(web_app_sla)
    
    # Register component reliability
    web_server = ComponentReliability(
        component_id='web_server',
        component_type=ComponentType.COMPUTE,
        base_availability=99.5,
        redundancy_pattern=RedundancyPattern.MULTI_AZ,
        mtbf_hours=720,
        mttr_minutes=10,
        dependencies=['load_balancer', 'database'],
        aws_service='EC2'
    )
    
    sla_system.register_component_reliability(web_server)
    
    # Design redundancy strategy
    redundancy_strategy = sla_system.design_redundancy_strategy('web_application', 99.9)
    print(f"Redundancy strategy: {json.dumps(redundancy_strategy, indent=2)}")
    
    # Calculate system availability
    architecture_config = {
        'web_application': {
            'components': ['web_server', 'load_balancer', 'database'],
            'topology': 'series'
        }
    }
    
    availability_results = sla_system.calculate_system_availability(architecture_config)
    print(f"System availability: {json.dumps(availability_results, indent=2)}")
    
    # Implement SLA monitoring
    monitoring_config = sla_system.implement_sla_monitoring('web_application')
    print(f"Monitoring configuration: {json.dumps(monitoring_config, indent=2, default=str)}")

if __name__ == "__main__":
    main()
```
{% endraw %}

## AWS Services

### Primary Services
- **Amazon CloudWatch**: SLA monitoring, metrics, and alerting
- **AWS Well-Architected Tool**: Architecture review and recommendations
- **Amazon Route 53**: DNS with health checks and failover
- **Elastic Load Balancing**: High availability load balancing

### Supporting Services
- **AWS Config**: Configuration compliance monitoring
- **AWS Systems Manager**: Operational insights and automation
- **Amazon CloudWatch Synthetics**: Synthetic monitoring for SLA validation
- **AWS Cost Explorer**: Cost analysis for redundancy strategies

## Benefits

- **SLA Compliance**: Meet contractual availability commitments
- **Predictable Performance**: Architecture designed for specific availability targets
- **Cost Optimization**: Right-size redundancy based on requirements
- **Risk Management**: Quantify and mitigate availability risks
- **Continuous Improvement**: Data-driven optimization of availability

## Related Resources

- [AWS Well-Architected Framework - Reliability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/)
- [Amazon CloudWatch User Guide](https://docs.aws.amazon.com/cloudwatch/)
- [AWS Architecture Center](https://aws.amazon.com/architecture/)
- [AWS Service Level Agreements](https://aws.amazon.com/legal/service-level-agreements/)
