---
title: COST06-BP01 - Perform cost modeling
layout: default
parent: COST06 - How do you meet cost targets when you select resource type, size and number?
grand_parent: Cost Optimization
nav_order: 1
---

<div class="pillar-header">
  <h1>COST06-BP01: Perform cost modeling</h1>
  <p>Create comprehensive cost models that help you understand the cost implications of different resource configurations and make informed decisions about resource selection to meet cost targets. Cost modeling enables you to predict costs, compare alternatives, and optimize resource allocation.</p>
</div>

## Implementation guidance

Cost modeling involves creating mathematical representations of how different resource configurations impact costs. This includes modeling compute, storage, network, and operational costs across different usage scenarios, time periods, and scaling patterns. Effective cost modeling enables proactive cost management and informed decision-making.

### Cost Modeling Components

**Resource Cost Modeling**: Model the direct costs of compute, storage, network, and other AWS resources under different usage patterns and configurations.

**Operational Cost Modeling**: Include operational costs such as management overhead, monitoring, backup, and disaster recovery in your cost models.

**Scaling Cost Models**: Model how costs change as workloads scale up or down, including the impact of different pricing models and commitment options.

**Time-Based Modeling**: Consider how costs change over time, including the impact of Reserved Instances, Savings Plans, and long-term growth projections.

### Model Types and Applications

**Comparative Cost Models**: Compare costs between different resource types, sizes, and configurations to identify the most cost-effective options.

**Scenario-Based Models**: Model costs under different business scenarios including growth, seasonal variations, and usage pattern changes.

**Total Cost of Ownership (TCO) Models**: Include all direct and indirect costs associated with resource ownership and operation over time.

**Break-Even Analysis Models**: Identify usage thresholds where different resource options become more cost-effective.

## AWS Services to Consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Pricing Calculator</h4>
    <p>Create detailed cost estimates for different resource configurations. Use the calculator to model various scenarios and compare cost implications of different choices.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Cost Explorer</h4>
    <p>Analyze historical cost data to validate and refine cost models. Use Cost Explorer's forecasting capabilities to project future costs based on current trends.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Budgets</h4>
    <p>Set cost targets and track actual costs against modeled projections. Use Budgets to monitor cost model accuracy and trigger alerts when costs deviate from models.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Cost and Usage Reports</h4>
    <p>Get detailed cost and usage data to build accurate cost models. Use CUR data to understand cost drivers and validate model assumptions.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon CloudWatch</h4>
    <p>Collect usage metrics and performance data to inform cost models. Use CloudWatch data to correlate resource utilization with costs.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Trusted Advisor</h4>
    <p>Get cost optimization recommendations to improve cost models. Use Trusted Advisor insights to identify cost modeling opportunities.</p>
  </div>
</div>

## Implementation Steps

### 1. Define Modeling Objectives
- Identify specific cost targets and constraints
- Define the scope and granularity of cost modeling
- Establish success criteria and validation methods
- Set up data collection and analysis infrastructure

### 2. Gather Cost and Usage Data
- Collect historical cost and usage data
- Analyze usage patterns and trends
- Identify cost drivers and key variables
- Document assumptions and constraints

### 3. Build Cost Models
- Create mathematical models for different resource types
- Include all relevant cost components and variables
- Model different scenarios and usage patterns
- Validate models against historical data

### 4. Implement Model Automation
- Automate cost calculations and projections
- Create dashboards and reporting mechanisms
- Set up alerts for cost target deviations
- Implement model updating and refinement processes

### 5. Validate and Refine Models
- Compare model predictions with actual costs
- Identify and correct model inaccuracies
- Refine models based on new data and insights
- Document lessons learned and best practices

### 6. Use Models for Decision Making
- Apply models to resource selection decisions
- Use models for capacity planning and budgeting
- Share models with stakeholders for informed decisions
- Continuously improve models based on outcomes

## Comprehensive Cost Modeling Framework

### Cost Modeling Engine
```python
import boto3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import json
from scipy import optimize
import matplotlib.pyplot as plt

@dataclass
class ResourceConfig:
    resource_type: str
    instance_type: str
    quantity: int
    region: str
    pricing_model: str  # on-demand, reserved, spot
    commitment_term: Optional[str] = None
    utilization_percent: float = 100.0

@dataclass
class CostComponent:
    name: str
    cost_type: str  # fixed, variable, step
    base_cost: float
    variable_rate: float
    scaling_factor: float
    minimum_cost: float = 0.0
    maximum_cost: Optional[float] = None

class ComprehensiveCostModeler:
    def __init__(self):
        self.pricing_client = boto3.client('pricing', region_name='us-east-1')
        self.ce_client = boto3.client('ce')
        self.cloudwatch = boto3.client('cloudwatch')
        
        # Cost model database
        self.cost_models = {}
        self.pricing_cache = {}
        
    def create_resource_cost_model(self, resource_config: ResourceConfig, 
                                 usage_scenarios: List[Dict]) -> Dict:
        """Create comprehensive cost model for a resource configuration"""
        
        model = {
            'resource_config': resource_config,
            'cost_components': self.identify_cost_components(resource_config),
            'pricing_data': self.get_pricing_data(resource_config),
            'usage_scenarios': {},
            'optimization_recommendations': [],
            'model_metadata': {
                'created_date': datetime.now().isoformat(),
                'model_version': '1.0',
                'validation_status': 'pending'
            }
        }
        
        # Model costs for different usage scenarios
        for scenario in usage_scenarios:
            scenario_costs = self.model_scenario_costs(resource_config, scenario)
            model['usage_scenarios'][scenario['name']] = scenario_costs
        
        # Generate optimization recommendations
        model['optimization_recommendations'] = self.generate_optimization_recommendations(
            resource_config, model['usage_scenarios']
        )
        
        return model
    
    def identify_cost_components(self, resource_config: ResourceConfig) -> List[CostComponent]:
        """Identify all cost components for a resource configuration"""
        
        components = []
        
        # Compute costs
        if resource_config.resource_type in ['EC2', 'ECS', 'EKS']:
            components.append(CostComponent(
                name='compute_hours',
                cost_type='variable',
                base_cost=0,
                variable_rate=self.get_compute_hourly_rate(resource_config),
                scaling_factor=1.0
            ))
        
        # Storage costs
        if resource_config.resource_type in ['EC2', 'RDS']:
            components.append(CostComponent(
                name='ebs_storage',
                cost_type='variable',
                base_cost=0,
                variable_rate=0.10,  # $0.10 per GB-month for gp3
                scaling_factor=1.0
            ))
        
        # Network costs
        components.append(CostComponent(
            name='data_transfer',
            cost_type='variable',
            base_cost=0,
            variable_rate=0.09,  # $0.09 per GB for internet egress
            scaling_factor=1.0
        ))
        
        # Operational costs
        components.append(CostComponent(
            name='operational_overhead',
            cost_type='fixed',
            base_cost=50,  # $50/month operational overhead
            variable_rate=0,
            scaling_factor=0.1  # 10% of compute costs
        ))
        
        return components
    
    def get_compute_hourly_rate(self, resource_config: ResourceConfig) -> float:
        """Get hourly compute rate for resource configuration"""
        
        # Check cache first
        cache_key = f"{resource_config.resource_type}_{resource_config.instance_type}_{resource_config.region}_{resource_config.pricing_model}"
        
        if cache_key in self.pricing_cache:
            return self.pricing_cache[cache_key]
        
        try:
            # Get pricing from AWS Pricing API
            if resource_config.resource_type == 'EC2':
                rate = self.get_ec2_pricing(resource_config)
            elif resource_config.resource_type == 'RDS':
                rate = self.get_rds_pricing(resource_config)
            else:
                rate = 0.10  # Default rate
            
            self.pricing_cache[cache_key] = rate
            return rate
            
        except Exception as e:
            print(f"Error getting pricing data: {e}")
            return 0.10  # Default fallback rate
    
    def get_ec2_pricing(self, resource_config: ResourceConfig) -> float:
        """Get EC2 pricing from AWS Pricing API"""
        
        try:
            response = self.pricing_client.get_products(
                ServiceCode='AmazonEC2',
                Filters=[
                    {'Type': 'TERM_MATCH', 'Field': 'instanceType', 'Value': resource_config.instance_type},
                    {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': self.get_location_name(resource_config.region)},
                    {'Type': 'TERM_MATCH', 'Field': 'tenancy', 'Value': 'Shared'},
                    {'Type': 'TERM_MATCH', 'Field': 'operating-system', 'Value': 'Linux'}
                ]
            )
            
            if response['PriceList']:
                price_data = json.loads(response['PriceList'][0])
                
                if resource_config.pricing_model == 'on-demand':
                    on_demand = price_data['terms']['OnDemand']
                    price_dimensions = list(on_demand.values())[0]['priceDimensions']
                    hourly_rate = float(list(price_dimensions.values())[0]['pricePerUnit']['USD'])
                    return hourly_rate
                
                elif resource_config.pricing_model == 'reserved':
                    # Simplified reserved instance pricing calculation
                    on_demand = price_data['terms']['OnDemand']
                    price_dimensions = list(on_demand.values())[0]['priceDimensions']
                    hourly_rate = float(list(price_dimensions.values())[0]['pricePerUnit']['USD'])
                    
                    # Apply typical reserved instance discount (30-60%)
                    discount = 0.4 if resource_config.commitment_term == '1yr' else 0.6
                    return hourly_rate * (1 - discount)
            
            return 0.10  # Default if no pricing found
            
        except Exception as e:
            print(f"Error getting EC2 pricing: {e}")
            return 0.10
    
    def model_scenario_costs(self, resource_config: ResourceConfig, scenario: Dict) -> Dict:
        """Model costs for a specific usage scenario"""
        
        scenario_results = {
            'scenario_name': scenario['name'],
            'monthly_costs': {},
            'annual_costs': {},
            'cost_breakdown': {},
            'utilization_metrics': {},
            'optimization_opportunities': []
        }
        
        # Calculate monthly costs for each component
        total_monthly_cost = 0
        
        for component in self.identify_cost_components(resource_config):
            monthly_cost = self.calculate_component_cost(
                component, resource_config, scenario
            )
            scenario_results['monthly_costs'][component.name] = monthly_cost
            total_monthly_cost += monthly_cost
        
        scenario_results['monthly_costs']['total'] = total_monthly_cost
        scenario_results['annual_costs']['total'] = total_monthly_cost * 12
        
        # Calculate utilization metrics
        scenario_results['utilization_metrics'] = self.calculate_utilization_metrics(
            resource_config, scenario
        )
        
        # Identify optimization opportunities
        scenario_results['optimization_opportunities'] = self.identify_optimization_opportunities(
            resource_config, scenario, scenario_results
        )
        
        return scenario_results
    
    def calculate_component_cost(self, component: CostComponent, 
                               resource_config: ResourceConfig, scenario: Dict) -> float:
        """Calculate cost for a specific component"""
        
        if component.cost_type == 'fixed':
            return component.base_cost
        
        elif component.cost_type == 'variable':
            usage_amount = scenario.get(component.name, 0)
            
            if component.name == 'compute_hours':
                # Calculate based on hours per month and quantity
                hours_per_month = 24 * 30 * (scenario.get('utilization_percent', 100) / 100)
                usage_amount = hours_per_month * resource_config.quantity
            
            elif component.name == 'ebs_storage':
                # Calculate based on storage size in GB
                usage_amount = scenario.get('storage_gb', 100) * resource_config.quantity
            
            elif component.name == 'data_transfer':
                # Calculate based on data transfer in GB
                usage_amount = scenario.get('data_transfer_gb', 10)
            
            return usage_amount * component.variable_rate
        
        elif component.cost_type == 'step':
            # Step function pricing (e.g., Lambda requests)
            usage_amount = scenario.get(component.name, 0)
            return self.calculate_step_pricing(usage_amount, component)
        
        return 0
    
    def calculate_utilization_metrics(self, resource_config: ResourceConfig, scenario: Dict) -> Dict:
        """Calculate utilization metrics for the scenario"""
        
        metrics = {
            'cpu_utilization': scenario.get('avg_cpu_percent', 50),
            'memory_utilization': scenario.get('avg_memory_percent', 60),
            'storage_utilization': scenario.get('storage_utilization_percent', 70),
            'network_utilization': scenario.get('network_utilization_percent', 30),
            'overall_efficiency': 0
        }
        
        # Calculate overall efficiency score
        efficiency_weights = {
            'cpu_utilization': 0.4,
            'memory_utilization': 0.3,
            'storage_utilization': 0.2,
            'network_utilization': 0.1
        }
        
        weighted_efficiency = sum(
            metrics[metric] * weight 
            for metric, weight in efficiency_weights.items()
        )
        
        metrics['overall_efficiency'] = weighted_efficiency
        
        return metrics
    
    def generate_optimization_recommendations(self, resource_config: ResourceConfig, 
                                            usage_scenarios: Dict) -> List[Dict]:
        """Generate optimization recommendations based on cost modeling"""
        
        recommendations = []
        
        # Analyze utilization across scenarios
        avg_cpu = np.mean([
            scenario['utilization_metrics']['cpu_utilization'] 
            for scenario in usage_scenarios.values()
        ])
        
        avg_efficiency = np.mean([
            scenario['utilization_metrics']['overall_efficiency'] 
            for scenario in usage_scenarios.values()
        ])
        
        # Rightsizing recommendations
        if avg_cpu < 30:
            recommendations.append({
                'type': 'rightsizing',
                'priority': 'high',
                'description': f'CPU utilization is low ({avg_cpu:.1f}%) - consider smaller instance type',
                'potential_savings_percent': 30,
                'implementation_effort': 'medium',
                'suggested_action': f'Test {self.get_smaller_instance_type(resource_config.instance_type)}'
            })
        
        elif avg_cpu > 80:
            recommendations.append({
                'type': 'rightsizing',
                'priority': 'high',
                'description': f'CPU utilization is high ({avg_cpu:.1f}%) - consider larger instance type',
                'potential_cost_increase_percent': 50,
                'implementation_effort': 'medium',
                'suggested_action': f'Test {self.get_larger_instance_type(resource_config.instance_type)}'
            })
        
        # Pricing model recommendations
        if resource_config.pricing_model == 'on-demand':
            recommendations.append({
                'type': 'pricing_model',
                'priority': 'medium',
                'description': 'Consider Reserved Instances for predictable workloads',
                'potential_savings_percent': 40,
                'implementation_effort': 'low',
                'suggested_action': 'Evaluate Reserved Instance options'
            })
        
        # Auto-scaling recommendations
        cpu_variance = np.std([
            scenario['utilization_metrics']['cpu_utilization'] 
            for scenario in usage_scenarios.values()
        ])
        
        if cpu_variance > 20:
            recommendations.append({
                'type': 'auto_scaling',
                'priority': 'medium',
                'description': f'High CPU variance ({cpu_variance:.1f}%) suggests auto-scaling opportunity',
                'potential_savings_percent': 25,
                'implementation_effort': 'high',
                'suggested_action': 'Implement auto-scaling policies'
            })
        
        return recommendations
    
    def create_comparative_cost_model(self, resource_options: List[ResourceConfig], 
                                    usage_scenarios: List[Dict]) -> Dict:
        """Create comparative cost model for multiple resource options"""
        
        comparison = {
            'comparison_date': datetime.now().isoformat(),
            'resource_options': {},
            'scenario_comparisons': {},
            'recommendations': [],
            'break_even_analysis': {}
        }
        
        # Model costs for each resource option
        for resource_config in resource_options:
            option_key = f"{resource_config.resource_type}_{resource_config.instance_type}"
            comparison['resource_options'][option_key] = self.create_resource_cost_model(
                resource_config, usage_scenarios
            )
        
        # Compare costs across scenarios
        for scenario in usage_scenarios:
            scenario_name = scenario['name']
            scenario_comparison = {}
            
            for option_key, option_model in comparison['resource_options'].items():
                scenario_costs = option_model['usage_scenarios'][scenario_name]
                scenario_comparison[option_key] = {
                    'monthly_cost': scenario_costs['monthly_costs']['total'],
                    'annual_cost': scenario_costs['annual_costs']['total'],
                    'efficiency_score': scenario_costs['utilization_metrics']['overall_efficiency']
                }
            
            # Find best option for this scenario
            best_option = min(
                scenario_comparison.keys(),
                key=lambda x: scenario_comparison[x]['monthly_cost']
            )
            
            scenario_comparison['best_option'] = best_option
            scenario_comparison['cost_range'] = {
                'min': min(opt['monthly_cost'] for opt in scenario_comparison.values() if isinstance(opt, dict)),
                'max': max(opt['monthly_cost'] for opt in scenario_comparison.values() if isinstance(opt, dict))
            }
            
            comparison['scenario_comparisons'][scenario_name] = scenario_comparison
        
        # Generate overall recommendations
        comparison['recommendations'] = self.generate_comparative_recommendations(comparison)
        
        return comparison
    
    def validate_cost_model(self, model: Dict, actual_costs: List[Dict]) -> Dict:
        """Validate cost model against actual cost data"""
        
        validation_results = {
            'validation_date': datetime.now().isoformat(),
            'accuracy_metrics': {},
            'model_adjustments': [],
            'validation_status': 'pending'
        }
        
        # Calculate accuracy metrics
        predicted_costs = []
        actual_cost_values = []
        
        for actual_cost in actual_costs:
            scenario_name = actual_cost['scenario']
            if scenario_name in model['usage_scenarios']:
                predicted = model['usage_scenarios'][scenario_name]['monthly_costs']['total']
                actual = actual_cost['monthly_cost']
                
                predicted_costs.append(predicted)
                actual_cost_values.append(actual)
        
        if predicted_costs and actual_cost_values:
            # Calculate accuracy metrics
            errors = [abs(p - a) / a for p, a in zip(predicted_costs, actual_cost_values)]
            
            validation_results['accuracy_metrics'] = {
                'mean_absolute_percentage_error': np.mean(errors) * 100,
                'max_error_percent': max(errors) * 100,
                'predictions_within_10_percent': sum(1 for e in errors if e <= 0.1) / len(errors) * 100,
                'correlation_coefficient': np.corrcoef(predicted_costs, actual_cost_values)[0, 1]
            }
            
            # Determine validation status
            mape = validation_results['accuracy_metrics']['mean_absolute_percentage_error']
            if mape <= 10:
                validation_results['validation_status'] = 'excellent'
            elif mape <= 20:
                validation_results['validation_status'] = 'good'
            elif mape <= 30:
                validation_results['validation_status'] = 'acceptable'
            else:
                validation_results['validation_status'] = 'needs_improvement'
        
        return validation_results
    
    def get_location_name(self, region: str) -> str:
        """Convert AWS region to location name for pricing API"""
        
        region_mapping = {
            'us-east-1': 'US East (N. Virginia)',
            'us-west-2': 'US West (Oregon)',
            'eu-west-1': 'Europe (Ireland)',
            'ap-southeast-1': 'Asia Pacific (Singapore)'
        }
        
        return region_mapping.get(region, 'US East (N. Virginia)')
    
    def get_smaller_instance_type(self, current_type: str) -> str:
        """Get smaller instance type recommendation"""
        
        size_mapping = {
            'large': 'medium',
            'xlarge': 'large',
            '2xlarge': 'xlarge',
            '4xlarge': '2xlarge'
        }
        
        for size, smaller in size_mapping.items():
            if size in current_type:
                return current_type.replace(size, smaller)
        
        return current_type
    
    def get_larger_instance_type(self, current_type: str) -> str:
        """Get larger instance type recommendation"""
        
        size_mapping = {
            'medium': 'large',
            'large': 'xlarge',
            'xlarge': '2xlarge',
            '2xlarge': '4xlarge'
        }
        
        for size, larger in size_mapping.items():
            if size in current_type:
                return current_type.replace(size, larger)
        
        return current_type
```

## Cost Modeling Templates and Examples

### Resource Cost Model Template
```yaml
Resource_Cost_Model:
  model_id: "COST-MODEL-EC2-001"
  created_date: "2024-01-15"
  resource_configuration:
    resource_type: "EC2"
    instance_type: "m5.large"
    quantity: 3
    region: "us-east-1"
    pricing_model: "on-demand"
    
  cost_components:
    compute_hours:
      type: "variable"
      hourly_rate: 0.096
      monthly_hours: 720
      monthly_cost: 207.36
      
    ebs_storage:
      type: "variable"
      storage_gb: 100
      cost_per_gb: 0.10
      monthly_cost: 30.00
      
    data_transfer:
      type: "variable"
      transfer_gb: 50
      cost_per_gb: 0.09
      monthly_cost: 4.50
      
    operational_overhead:
      type: "fixed"
      monthly_cost: 50.00
      
  usage_scenarios:
    production:
      utilization_percent: 75
      monthly_cost: 291.86
      efficiency_score: 75
      
    development:
      utilization_percent: 25
      monthly_cost: 291.86
      efficiency_score: 25
      
    testing:
      utilization_percent: 40
      monthly_cost: 291.86
      efficiency_score: 40
      
  optimization_recommendations:
    - type: "rightsizing"
      priority: "high"
      description: "Low utilization in dev/test - consider smaller instances"
      potential_savings: 30
      
    - type: "pricing_model"
      priority: "medium"
      description: "Consider Reserved Instances for production workload"
      potential_savings: 40
      
  validation_results:
    accuracy_mape: 8.5
    status: "excellent"
    last_validated: "2024-01-10"
```

## Common Challenges and Solutions

### Challenge: Incomplete Cost Data

**Solution**: Implement comprehensive cost tracking and tagging. Use AWS Cost and Usage Reports for detailed cost breakdowns. Establish data collection processes for all cost components.

### Challenge: Dynamic Pricing Changes

**Solution**: Regularly update pricing data and models. Implement automated pricing updates. Use APIs to fetch current pricing information. Build buffers into cost models for pricing volatility.

### Challenge: Complex Multi-Service Dependencies

**Solution**: Model service dependencies and their cost interactions. Use holistic cost modeling approaches. Consider indirect costs and operational overhead. Implement dependency mapping and impact analysis.

### Challenge: Validating Model Accuracy

**Solution**: Regularly compare model predictions with actual costs. Implement automated validation processes. Use statistical methods to measure model accuracy. Continuously refine models based on validation results.

### Challenge: Scaling Cost Models

**Solution**: Use automated tools and frameworks for cost modeling. Implement template-based modeling approaches. Create reusable cost model components. Use cloud-native tools for scalable cost analysis.

## Related Resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/cost_type_size_number_modeling.html">AWS Well-Architected Framework - Perform cost modeling</a></li>
    <li><a href="https://calculator.aws/">AWS Pricing Calculator</a></li>
    <li><a href="https://docs.aws.amazon.com/cost-management/latest/userguide/ce-what-is.html">AWS Cost Explorer User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/budgets-managing-costs.html">AWS Budgets User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/cur/latest/userguide/what-is-cur.html">AWS Cost and Usage Reports User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html">Amazon CloudWatch User Guide</a></li>
    <li><a href="https://aws.amazon.com/premiumsupport/technology/trusted-advisor/">AWS Trusted Advisor</a></li>
    <li><a href="https://aws.amazon.com/blogs/aws-cost-management/">AWS Cost Management Blog</a></li>
  </ul>
</div>

<style>
.pillar-header {
  background-color: #e8f5e8;
  border-left: 5px solid #2d7d2d;
}

.pillar-header h1 {
  color: #2d7d2d;
}

.aws-service-content h4 {
  color: #2d7d2d;
}

.related-resources {
  background-color: #e8f5e8;
}

.related-resources h2 {
  color: #2d7d2d;
}
</style>
