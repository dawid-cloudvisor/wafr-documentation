---
title: COST07-BP01 - Perform pricing model analysis
layout: default
parent: COST07 - How do you use pricing models to reduce cost?
grand_parent: Cost Optimization
nav_order: 1
---

<div class="pillar-header">
  <h1>COST07-BP01: Perform pricing model analysis</h1>
  <p>Analyze different pricing models available for your workloads and select the most cost-effective options based on usage patterns, commitment levels, and business requirements. Comprehensive pricing analysis enables informed decisions about Reserved Instances, Savings Plans, Spot Instances, and other pricing options.</p>
</div>

## Implementation guidance

Pricing model analysis involves systematically evaluating different AWS pricing options to identify the most cost-effective combinations for your specific workloads. This includes analyzing usage patterns, commitment requirements, and business constraints to optimize your pricing strategy.

### Pricing Model Categories

**On-Demand Pricing**: Pay-as-you-go pricing with no upfront commitments, providing maximum flexibility but typically higher per-unit costs.

**Reserved Instances**: Commit to specific instance types in specific regions for 1 or 3 years in exchange for significant discounts (up to 75% off On-Demand prices).

**Savings Plans**: Flexible pricing model that provides savings (up to 72% off On-Demand) in exchange for a commitment to a consistent amount of usage for 1 or 3 years.

**Spot Instances**: Use spare EC2 capacity at discounts of up to 90% off On-Demand prices, with the trade-off of potential interruption.

**Dedicated Hosts/Instances**: Physical servers dedicated for your use, often required for compliance or licensing requirements.

### Analysis Framework

**Usage Pattern Analysis**: Examine historical usage data to understand consumption patterns, peak usage, and baseline requirements.

**Commitment Analysis**: Evaluate your ability to make long-term commitments based on business stability and growth projections.

**Risk Assessment**: Assess the risk tolerance for different pricing models, especially for Spot Instances and long-term commitments.

**Total Cost of Ownership**: Consider all costs including management overhead, operational complexity, and opportunity costs.

## AWS Services to Consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Cost Explorer</h4>
    <p>Analyze historical costs and usage patterns. Use Cost Explorer's Reserved Instance and Savings Plans recommendations to identify optimization opportunities.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Compute Optimizer</h4>
    <p>Get rightsizing recommendations that complement pricing model optimization. Use insights to ensure you're purchasing the right Reserved Instances.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Pricing Calculator</h4>
    <p>Model different pricing scenarios and compare total costs. Use the calculator to evaluate the financial impact of different pricing model combinations.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Cost and Usage Reports</h4>
    <p>Access detailed cost and usage data for comprehensive analysis. Use CUR data to perform advanced pricing model analysis and optimization.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Budgets</h4>
    <p>Track spending against pricing model commitments and targets. Set up alerts for Reserved Instance and Savings Plans utilization.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Trusted Advisor</h4>
    <p>Get recommendations for cost optimization including Reserved Instance opportunities. Use Trusted Advisor insights to identify pricing model improvements.</p>
  </div>
</div>

## Implementation Steps

### 1. Collect Usage Data
- Gather historical usage data for all AWS services
- Analyze usage patterns and trends over time
- Identify baseline and peak usage requirements
- Document seasonal variations and growth patterns

### 2. Analyze Current Pricing Models
- Audit existing Reserved Instances and Savings Plans
- Calculate current effective rates and utilization
- Identify underutilized commitments and gaps
- Assess current pricing model performance

### 3. Evaluate Pricing Options
- Compare different pricing models for each service
- Calculate potential savings for various commitment levels
- Assess risk and flexibility trade-offs
- Model different scenarios and business conditions

### 4. Develop Pricing Strategy
- Create comprehensive pricing model strategy
- Define commitment levels and terms
- Plan implementation timeline and approach
- Establish monitoring and optimization processes

### 5. Implement Optimized Pricing
- Purchase recommended Reserved Instances and Savings Plans
- Implement Spot Instance usage where appropriate
- Set up monitoring and alerting for utilization
- Document decisions and rationale

### 6. Monitor and Optimize
- Track pricing model performance and utilization
- Regularly review and adjust commitments
- Identify new optimization opportunities
- Refine strategy based on business changes
## Comprehensive Pricing Model Analysis Framework

### Pricing Model Analyzer
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
class PricingOption:
    model_type: str  # on-demand, reserved, savings-plan, spot
    service: str
    instance_type: str
    region: str
    term_length: Optional[str] = None  # 1yr, 3yr
    payment_option: Optional[str] = None  # no-upfront, partial-upfront, all-upfront
    hourly_rate: float = 0.0
    upfront_cost: float = 0.0
    discount_percentage: float = 0.0

@dataclass
class UsagePattern:
    service: str
    instance_type: str
    region: str
    average_hours_per_month: float
    peak_hours_per_month: float
    usage_variability: float
    seasonal_factor: float
    growth_rate: float

@dataclass
class PricingRecommendation:
    current_model: str
    recommended_model: str
    potential_savings: float
    payback_period_months: Optional[float]
    risk_level: str
    confidence_score: float
    rationale: str

class ComprehensivePricingAnalyzer:
    def __init__(self):
        self.ce_client = boto3.client('ce')
        self.pricing_client = boto3.client('pricing', region_name='us-east-1')
        self.ec2 = boto3.client('ec2')
        
        # Pricing data cache
        self.pricing_cache = {}
        
        # Analysis parameters
        self.analysis_period_months = 12
        self.confidence_threshold = 0.8
        
    def perform_comprehensive_pricing_analysis(self, usage_patterns: List[UsagePattern]) -> Dict:
        """Perform comprehensive pricing model analysis"""
        
        analysis_results = {
            'analysis_date': datetime.now().isoformat(),
            'usage_patterns_analyzed': len(usage_patterns),
            'pricing_options': {},
            'recommendations': [],
            'savings_summary': {},
            'risk_assessment': {},
            'implementation_plan': {}
        }
        
        # Analyze each usage pattern
        for pattern in usage_patterns:
            pattern_key = f"{pattern.service}_{pattern.instance_type}_{pattern.region}"
            
            # Get all pricing options for this pattern
            pricing_options = self.get_pricing_options(pattern)
            analysis_results['pricing_options'][pattern_key] = pricing_options
            
            # Analyze and recommend optimal pricing model
            recommendation = self.analyze_pricing_options(pattern, pricing_options)
            if recommendation:
                analysis_results['recommendations'].append(recommendation)
        
        # Generate summary and implementation plan
        analysis_results['savings_summary'] = self.calculate_savings_summary(
            analysis_results['recommendations']
        )
        analysis_results['risk_assessment'] = self.assess_overall_risk(
            analysis_results['recommendations']
        )
        analysis_results['implementation_plan'] = self.create_implementation_plan(
            analysis_results['recommendations']
        )
        
        return analysis_results
    
    def get_pricing_options(self, pattern: UsagePattern) -> List[PricingOption]:
        """Get all available pricing options for a usage pattern"""
        
        options = []
        
        # On-Demand pricing
        on_demand_rate = self.get_on_demand_rate(pattern.service, pattern.instance_type, pattern.region)
        options.append(PricingOption(
            model_type='on-demand',
            service=pattern.service,
            instance_type=pattern.instance_type,
            region=pattern.region,
            hourly_rate=on_demand_rate,
            discount_percentage=0.0
        ))
        
        # Reserved Instance options
        if pattern.service == 'EC2':
            ri_options = self.get_reserved_instance_options(pattern)
            options.extend(ri_options)
        
        # Savings Plans options
        sp_options = self.get_savings_plans_options(pattern)
        options.extend(sp_options)
        
        # Spot Instance pricing (if applicable)
        if self.is_spot_suitable(pattern):
            spot_rate = self.get_spot_rate(pattern.instance_type, pattern.region)
            options.append(PricingOption(
                model_type='spot',
                service=pattern.service,
                instance_type=pattern.instance_type,
                region=pattern.region,
                hourly_rate=spot_rate,
                discount_percentage=((on_demand_rate - spot_rate) / on_demand_rate) * 100
            ))
        
        return options
    
    def get_reserved_instance_options(self, pattern: UsagePattern) -> List[PricingOption]:
        """Get Reserved Instance pricing options"""
        
        options = []
        on_demand_rate = self.get_on_demand_rate(pattern.service, pattern.instance_type, pattern.region)
        
        # Standard Reserved Instances
        ri_configurations = [
            ('1yr', 'no-upfront', 0.6),      # 40% discount
            ('1yr', 'partial-upfront', 0.55), # 45% discount
            ('1yr', 'all-upfront', 0.5),     # 50% discount
            ('3yr', 'no-upfront', 0.4),      # 60% discount
            ('3yr', 'partial-upfront', 0.35), # 65% discount
            ('3yr', 'all-upfront', 0.25),    # 75% discount
        ]
        
        for term, payment, rate_multiplier in ri_configurations:
            hourly_rate = on_demand_rate * rate_multiplier
            upfront_cost = self.calculate_ri_upfront_cost(
                on_demand_rate, term, payment, rate_multiplier
            )
            
            options.append(PricingOption(
                model_type='reserved',
                service=pattern.service,
                instance_type=pattern.instance_type,
                region=pattern.region,
                term_length=term,
                payment_option=payment,
                hourly_rate=hourly_rate,
                upfront_cost=upfront_cost,
                discount_percentage=((on_demand_rate - hourly_rate) / on_demand_rate) * 100
            ))
        
        return options
    
    def get_savings_plans_options(self, pattern: UsagePattern) -> List[PricingOption]:
        """Get Savings Plans pricing options"""
        
        options = []
        on_demand_rate = self.get_on_demand_rate(pattern.service, pattern.instance_type, pattern.region)
        
        # Compute Savings Plans
        sp_configurations = [
            ('1yr', 'no-upfront', 0.66),     # 34% discount
            ('1yr', 'partial-upfront', 0.62), # 38% discount
            ('1yr', 'all-upfront', 0.58),    # 42% discount
            ('3yr', 'no-upfront', 0.46),     # 54% discount
            ('3yr', 'partial-upfront', 0.42), # 58% discount
            ('3yr', 'all-upfront', 0.28),    # 72% discount
        ]
        
        for term, payment, rate_multiplier in sp_configurations:
            hourly_rate = on_demand_rate * rate_multiplier
            
            options.append(PricingOption(
                model_type='savings-plan',
                service=pattern.service,
                instance_type=pattern.instance_type,
                region=pattern.region,
                term_length=term,
                payment_option=payment,
                hourly_rate=hourly_rate,
                discount_percentage=((on_demand_rate - hourly_rate) / on_demand_rate) * 100
            ))
        
        return options
    
    def analyze_pricing_options(self, pattern: UsagePattern, 
                              options: List[PricingOption]) -> Optional[PricingRecommendation]:
        """Analyze pricing options and generate recommendation"""
        
        # Calculate costs for each option
        option_analysis = []
        
        for option in options:
            total_cost = self.calculate_total_cost(pattern, option, self.analysis_period_months)
            
            analysis = {
                'option': option,
                'total_cost': total_cost,
                'monthly_cost': total_cost / self.analysis_period_months,
                'suitability_score': self.calculate_suitability_score(pattern, option),
                'risk_score': self.calculate_risk_score(pattern, option)
            }
            
            option_analysis.append(analysis)
        
        # Find current model (assume on-demand if not specified)
        current_option = next((opt for opt in option_analysis if opt['option'].model_type == 'on-demand'), None)
        if not current_option:
            return None
        
        # Find best option based on cost and suitability
        best_option = min(
            option_analysis,
            key=lambda x: x['total_cost'] * (2 - x['suitability_score'])  # Weight by suitability
        )
        
        # Generate recommendation if there's significant savings
        if best_option != current_option:
            potential_savings = current_option['total_cost'] - best_option['total_cost']
            savings_percentage = (potential_savings / current_option['total_cost']) * 100
            
            if savings_percentage > 10:  # Only recommend if >10% savings
                payback_period = self.calculate_payback_period(
                    current_option['option'], best_option['option'], pattern
                )
                
                return PricingRecommendation(
                    current_model=current_option['option'].model_type,
                    recommended_model=best_option['option'].model_type,
                    potential_savings=potential_savings,
                    payback_period_months=payback_period,
                    risk_level=self.assess_risk_level(best_option['risk_score']),
                    confidence_score=best_option['suitability_score'],
                    rationale=self.generate_recommendation_rationale(
                        pattern, current_option['option'], best_option['option'], savings_percentage
                    )
                )
        
        return None
    
    def calculate_total_cost(self, pattern: UsagePattern, option: PricingOption, months: int) -> float:
        """Calculate total cost for a pricing option over specified months"""
        
        # Base monthly usage cost
        monthly_hours = pattern.average_hours_per_month
        monthly_cost = monthly_hours * option.hourly_rate
        
        # Add upfront cost amortized over the period
        if option.upfront_cost > 0:
            if option.term_length == '1yr':
                amortization_months = min(12, months)
            elif option.term_length == '3yr':
                amortization_months = min(36, months)
            else:
                amortization_months = months
            
            monthly_upfront = option.upfront_cost / amortization_months
            monthly_cost += monthly_upfront
        
        # Apply growth factor
        total_cost = 0
        for month in range(months):
            growth_factor = (1 + pattern.growth_rate / 12) ** month
            month_cost = monthly_cost * growth_factor
            
            # Apply seasonal variation
            seasonal_adjustment = 1 + pattern.seasonal_factor * np.sin(2 * np.pi * month / 12)
            month_cost *= seasonal_adjustment
            
            total_cost += month_cost
        
        return total_cost
    
    def calculate_suitability_score(self, pattern: UsagePattern, option: PricingOption) -> float:
        """Calculate how suitable a pricing option is for a usage pattern"""
        
        score = 0.5  # Base score
        
        # Adjust based on usage variability
        if option.model_type == 'reserved':
            # Reserved instances are better for stable workloads
            if pattern.usage_variability < 0.3:
                score += 0.3
            elif pattern.usage_variability > 0.7:
                score -= 0.2
        
        elif option.model_type == 'spot':
            # Spot instances are suitable for fault-tolerant workloads
            # This would need additional workload characteristics
            score += 0.1  # Assume some suitability
        
        elif option.model_type == 'savings-plan':
            # Savings plans are flexible and generally suitable
            score += 0.2
        
        # Adjust based on commitment length vs business stability
        if option.term_length == '3yr':
            if pattern.growth_rate > 0.5:  # High growth might outgrow commitment
                score -= 0.1
            else:
                score += 0.1  # Stable growth benefits from longer commitment
        
        return max(0.0, min(1.0, score))
    
    def calculate_risk_score(self, pattern: UsagePattern, option: PricingOption) -> float:
        """Calculate risk score for a pricing option (0 = low risk, 1 = high risk)"""
        
        risk = 0.0
        
        # Commitment risk
        if option.model_type in ['reserved', 'savings-plan']:
            if option.term_length == '3yr':
                risk += 0.3
            elif option.term_length == '1yr':
                risk += 0.1
        
        # Upfront payment risk
        if option.payment_option == 'all-upfront':
            risk += 0.2
        elif option.payment_option == 'partial-upfront':
            risk += 0.1
        
        # Usage variability risk
        if option.model_type == 'reserved' and pattern.usage_variability > 0.5:
            risk += 0.2
        
        # Spot interruption risk
        if option.model_type == 'spot':
            risk += 0.4  # Base interruption risk
        
        return min(1.0, risk)
    
    def generate_reserved_instance_recommendations(self, usage_data: Dict) -> List[Dict]:
        """Generate specific Reserved Instance recommendations"""
        
        recommendations = []
        
        # Analyze EC2 usage for RI opportunities
        ec2_usage = usage_data.get('EC2', {})
        
        for instance_type, usage_info in ec2_usage.items():
            if usage_info['average_hours_per_month'] > 500:  # ~70% utilization threshold
                
                # Calculate optimal RI configuration
                optimal_ri = self.calculate_optimal_ri_configuration(
                    instance_type, usage_info
                )
                
                if optimal_ri:
                    recommendations.append({
                        'resource_type': 'EC2',
                        'instance_type': instance_type,
                        'recommended_quantity': optimal_ri['quantity'],
                        'term_length': optimal_ri['term'],
                        'payment_option': optimal_ri['payment'],
                        'estimated_savings': optimal_ri['savings'],
                        'payback_period': optimal_ri['payback_months'],
                        'confidence': optimal_ri['confidence']
                    })
        
        return recommendations
    
    def generate_savings_plans_recommendations(self, usage_data: Dict) -> List[Dict]:
        """Generate Savings Plans recommendations"""
        
        recommendations = []
        
        # Calculate total compute spend
        total_compute_spend = self.calculate_total_compute_spend(usage_data)
        
        if total_compute_spend > 1000:  # Minimum threshold for Savings Plans
            
            # Analyze different commitment levels
            commitment_levels = [0.5, 0.7, 0.8, 0.9]  # 50%, 70%, 80%, 90% of baseline usage
            
            for commitment_level in commitment_levels:
                commitment_amount = total_compute_spend * commitment_level
                
                savings_plan_analysis = self.analyze_savings_plan_commitment(
                    commitment_amount, usage_data
                )
                
                if savings_plan_analysis['savings'] > 0:
                    recommendations.append({
                        'plan_type': 'Compute Savings Plans',
                        'commitment_amount': commitment_amount,
                        'term_length': savings_plan_analysis['optimal_term'],
                        'payment_option': savings_plan_analysis['optimal_payment'],
                        'estimated_savings': savings_plan_analysis['savings'],
                        'coverage_percentage': commitment_level * 100,
                        'risk_level': savings_plan_analysis['risk_level']
                    })
        
        return recommendations
    
    def create_pricing_optimization_dashboard(self, analysis_results: Dict) -> Dict:
        """Create dashboard data for pricing optimization insights"""
        
        dashboard_data = {
            'summary_metrics': {
                'total_potential_savings': sum(
                    r.potential_savings for r in analysis_results['recommendations'] 
                    if r.potential_savings > 0
                ),
                'high_confidence_recommendations': len([
                    r for r in analysis_results['recommendations'] 
                    if r.confidence_score > 0.8
                ]),
                'average_savings_percentage': np.mean([
                    (r.potential_savings / 1000) * 100  # Assuming baseline cost
                    for r in analysis_results['recommendations']
                ]) if analysis_results['recommendations'] else 0
            },
            
            'pricing_model_distribution': self.calculate_pricing_model_distribution(analysis_results),
            'savings_by_model': self.calculate_savings_by_model(analysis_results),
            'risk_assessment': analysis_results.get('risk_assessment', {}),
            'implementation_timeline': self.create_implementation_timeline(analysis_results)
        }
        
        return dashboard_data
    
    def get_on_demand_rate(self, service: str, instance_type: str, region: str) -> float:
        """Get on-demand hourly rate for a service/instance type"""
        
        # This would typically call the AWS Pricing API
        # For demonstration, returning sample rates
        
        base_rates = {
            't3.micro': 0.0104,
            't3.small': 0.0208,
            't3.medium': 0.0416,
            't3.large': 0.0832,
            'm5.large': 0.096,
            'm5.xlarge': 0.192,
            'c5.large': 0.085,
            'c5.xlarge': 0.17
        }
        
        return base_rates.get(instance_type, 0.1)  # Default rate
    
    def is_spot_suitable(self, pattern: UsagePattern) -> bool:
        """Determine if workload is suitable for Spot instances"""
        
        # Simple heuristic - in practice this would be more sophisticated
        return (pattern.usage_variability > 0.3 and 
                pattern.service == 'EC2')
    
    def get_spot_rate(self, instance_type: str, region: str) -> float:
        """Get current spot price for instance type"""
        
        try:
            response = self.ec2.describe_spot_price_history(
                InstanceTypes=[instance_type],
                ProductDescriptions=['Linux/UNIX'],
                MaxResults=1
            )
            
            if response['SpotPriceHistory']:
                return float(response['SpotPriceHistory'][0]['SpotPrice'])
            
        except Exception as e:
            print(f"Error getting spot price: {e}")
        
        # Fallback to estimated spot price (typically 70% discount)
        on_demand_rate = self.get_on_demand_rate('EC2', instance_type, region)
        return on_demand_rate * 0.3
```

## Pricing Analysis Templates

### Pricing Model Analysis Report Template
```yaml
Pricing_Model_Analysis_Report:
  analysis_id: "PRICING-ANALYSIS-2024-001"
  analysis_date: "2024-01-15"
  analysis_period_months: 12
  
  current_state:
    total_monthly_spend: 15000.00
    pricing_model_breakdown:
      on_demand: 85
      reserved_instances: 10
      savings_plans: 3
      spot_instances: 2
      
  usage_patterns_analyzed:
    - service: "EC2"
      instance_types: ["m5.large", "c5.xlarge", "t3.medium"]
      regions: ["us-east-1", "us-west-2"]
      average_utilization: 65
      usage_variability: 0.4
      
  pricing_recommendations:
    reserved_instances:
      - instance_type: "m5.large"
        quantity: 10
        term: "1yr"
        payment: "partial-upfront"
        estimated_savings: 3600.00
        payback_months: 8
        confidence: 0.92
        
    savings_plans:
      - plan_type: "Compute Savings Plans"
        commitment_amount: 5000.00
        term: "1yr"
        payment: "no-upfront"
        estimated_savings: 1800.00
        coverage: 70
        risk_level: "low"
        
    spot_instances:
      - workload: "batch-processing"
        instance_types: ["c5.large", "m5.large"]
        estimated_savings: 2400.00
        interruption_tolerance: "high"
        
  savings_summary:
    total_potential_savings: 7800.00
    savings_percentage: 43.3
    payback_period_months: 6
    implementation_complexity: "medium"
    
  risk_assessment:
    overall_risk: "low-medium"
    commitment_risk: "low"
    operational_risk: "medium"
    financial_risk: "low"
    
  implementation_plan:
    phase_1:
      duration: "Month 1"
      actions:
        - "Purchase high-confidence Reserved Instances"
        - "Implement Compute Savings Plans"
      expected_savings: 5400.00
      
    phase_2:
      duration: "Month 2-3"
      actions:
        - "Implement Spot Instance usage for batch workloads"
        - "Optimize remaining on-demand usage"
      expected_savings: 2400.00
```

## Common Challenges and Solutions

### Challenge: Complex Pricing Model Combinations

**Solution**: Use systematic analysis frameworks and tools. Start with high-impact, low-risk optimizations. Implement gradual changes with monitoring and validation.

### Challenge: Changing Usage Patterns

**Solution**: Regularly review and adjust pricing models. Use flexible options like Savings Plans when usage patterns are uncertain. Implement monitoring to detect pattern changes.

### Challenge: Commitment Risk Management

**Solution**: Start with shorter-term commitments. Use a portfolio approach mixing different commitment levels. Regularly assess business stability and growth projections.

### Challenge: Spot Instance Complexity

**Solution**: Start with fault-tolerant workloads. Implement proper interruption handling. Use Spot Fleet for diversification across instance types and availability zones.

### Challenge: ROI Calculation Complexity

**Solution**: Use comprehensive TCO models that include all costs. Consider opportunity costs and operational overhead. Implement tracking and measurement systems.

## Related Resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/cost_pricing_model_analysis.html">AWS Well-Architected Framework - Perform pricing model analysis</a></li>
    <li><a href="https://docs.aws.amazon.com/cost-management/latest/userguide/ce-what-is.html">AWS Cost Explorer User Guide</a></li>
    <li><a href="https://aws.amazon.com/compute-optimizer/">AWS Compute Optimizer</a></li>
    <li><a href="https://calculator.aws/">AWS Pricing Calculator</a></li>
    <li><a href="https://docs.aws.amazon.com/cur/latest/userguide/what-is-cur.html">AWS Cost and Usage Reports User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/budgets-managing-costs.html">AWS Budgets User Guide</a></li>
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
