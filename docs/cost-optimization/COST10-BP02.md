---
title: COST10-BP02 - Review and analyze this workload regularly
layout: default
parent: COST10 - How do you evaluate new services?
grand_parent: Cost Optimization
nav_order: 10.2
---

<div class="pillar-header">
  <h1>COST10-BP02: Review and analyze this workload regularly</h1>
  <p>*This page contains guidance for implementing this best practice from the AWS Well-Architected Framework.*</p>
</div>

Implement regular review cycles to analyze workloads against new AWS services, features, and best practices to identify optimization opportunities and ensure continued cost efficiency. Regular workload analysis ensures you stay current with AWS innovations and continuously optimize your architecture for cost and performance.

## Overview

Regular workload analysis is essential for maintaining cost-optimized architectures in the rapidly evolving AWS ecosystem. This involves establishing systematic review schedules, implementing comprehensive analysis frameworks, and creating actionable optimization roadmaps based on new service capabilities and changing business requirements.

Key components of regular workload analysis include:
- **Scheduled Review Cycles**: Establishing regular intervals for workload assessment
- **Comprehensive Analysis Framework**: Systematic evaluation of architecture, costs, and performance
- **New Service Integration**: Evaluating how new AWS services can improve existing workloads
- **Optimization Tracking**: Monitoring and measuring the impact of implemented changes
- **Continuous Improvement**: Using review insights to refine processes and strategies

## Implementation

### Workload Analysis Framework

```python
import boto3
import json
import pandas as pd
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
import logging
import numpy as np

class ReviewFrequency(Enum):
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    ANNUALLY = "annually"

class AnalysisCategory(Enum):
    COST_OPTIMIZATION = "cost_optimization"
    PERFORMANCE_IMPROVEMENT = "performance_improvement"
    SECURITY_ENHANCEMENT = "security_enhancement"
    OPERATIONAL_EFFICIENCY = "operational_efficiency"
    RELIABILITY_IMPROVEMENT = "reliability_improvement"

class OptimizationStatus(Enum):
    IDENTIFIED = "identified"
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    DEFERRED = "deferred"

@dataclass
class WorkloadMetrics:
    workload_id: str
    cost_metrics: Dict[str, float]
    performance_metrics: Dict[str, float]
    utilization_metrics: Dict[str, float]
    availability_metrics: Dict[str, float]
    security_metrics: Dict[str, float]
    collection_date: datetime

@dataclass
class OptimizationOpportunity:
    opportunity_id: str
    workload_id: str
    category: AnalysisCategory
    description: str
    current_state: str
    proposed_solution: str
    estimated_savings: float
    implementation_effort: str
    risk_level: str
    priority: str
    status: OptimizationStatus
    identified_date: datetime
    target_completion_date: Optional[datetime] = None
    actual_completion_date: Optional[datetime] = None
    actual_savings: Optional[float] = None

@dataclass
class WorkloadReviewResult:
    review_id: str
    workload_id: str
    review_date: datetime
    review_type: str
    reviewer: str
    metrics_analyzed: WorkloadMetrics
    opportunities_identified: List[OptimizationOpportunity]
    recommendations: List[Dict]
    next_review_date: datetime
    review_score: float
    improvement_areas: List[str]

class WorkloadAnalysisManager:
    def __init__(self):
        self.cost_explorer = boto3.client('ce')
        self.cloudwatch = boto3.client('cloudwatch')
        self.config = boto3.client('config')
        self.wellarchitected = boto3.client('wellarchitected')
        self.trusted_advisor = boto3.client('support')
        self.systems_manager = boto3.client('ssm')
        
        # Analysis configuration
        self.analysis_config = {
            'cost_thresholds': {
                'high_cost_resource': 1000.0,  # Monthly cost threshold
                'cost_increase_alert': 0.2,    # 20% increase threshold
                'utilization_threshold': 0.8   # 80% utilization threshold
            },
            'review_schedules': {
                'critical_workloads': ReviewFrequency.MONTHLY,
                'important_workloads': ReviewFrequency.QUARTERLY,
                'standard_workloads': ReviewFrequency.ANNUALLY
            },
            'analysis_depth': {
                'comprehensive': ['cost', 'performance', 'security', 'reliability', 'operations'],
                'focused': ['cost', 'performance'],
                'rapid': ['cost']
            }
        }
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def conduct_workload_analysis(self, workload_id: str, analysis_type: str = 'comprehensive') -> WorkloadReviewResult:
        """Conduct comprehensive workload analysis"""
        
        review_id = f"WA_{workload_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Collect workload metrics
        workload_metrics = self.collect_workload_metrics(workload_id)
        
        # Analyze against new services and best practices
        opportunities = self.identify_optimization_opportunities(workload_id, workload_metrics)
        
        # Generate recommendations
        recommendations = self.generate_optimization_recommendations(opportunities, workload_metrics)
        
        # Calculate review score
        review_score = self.calculate_workload_score(workload_metrics, opportunities)
        
        # Identify improvement areas
        improvement_areas = self.identify_improvement_areas(workload_metrics, opportunities)
        
        # Determine next review date
        next_review_date = self.calculate_next_review_date(workload_id, review_score)
        
        review_result = WorkloadReviewResult(
            review_id=review_id,
            workload_id=workload_id,
            review_date=datetime.now(),
            review_type=analysis_type,
            reviewer="automated_analysis",
            metrics_analyzed=workload_metrics,
            opportunities_identified=opportunities,
            recommendations=recommendations,
            next_review_date=next_review_date,
            review_score=review_score,
            improvement_areas=improvement_areas
        )
        
        # Store review results
        self.store_review_results(review_result)
        
        return review_result
    
    def collect_workload_metrics(self, workload_id: str) -> WorkloadMetrics:
        """Collect comprehensive workload metrics"""
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)  # Last 30 days
        
        # Cost metrics
        cost_metrics = self.get_cost_metrics(workload_id, start_date, end_date)
        
        # Performance metrics
        performance_metrics = self.get_performance_metrics(workload_id, start_date, end_date)
        
        # Utilization metrics
        utilization_metrics = self.get_utilization_metrics(workload_id, start_date, end_date)
        
        # Availability metrics
        availability_metrics = self.get_availability_metrics(workload_id, start_date, end_date)
        
        # Security metrics
        security_metrics = self.get_security_metrics(workload_id)
        
        return WorkloadMetrics(
            workload_id=workload_id,
            cost_metrics=cost_metrics,
            performance_metrics=performance_metrics,
            utilization_metrics=utilization_metrics,
            availability_metrics=availability_metrics,
            security_metrics=security_metrics,
            collection_date=datetime.now()
        )
    
    def get_cost_metrics(self, workload_id: str, start_date: datetime, end_date: datetime) -> Dict[str, float]:
        """Get cost metrics for workload"""
        
        try:
            # Get cost and usage data
            response = self.cost_explorer.get_cost_and_usage(
                TimePeriod={
                    'Start': start_date.strftime('%Y-%m-%d'),
                    'End': end_date.strftime('%Y-%m-%d')
                },
                Granularity='DAILY',
                Metrics=['BlendedCost', 'UsageQuantity'],
                GroupBy=[
                    {'Type': 'DIMENSION', 'Key': 'SERVICE'},
                    {'Type': 'TAG', 'Key': f'WorkloadId:{workload_id}'}
                ]
            )
            
            # Process cost data
            total_cost = 0.0
            service_costs = {}
            daily_costs = []
            
            for result in response.get('ResultsByTime', []):
                daily_cost = 0.0
                for group in result.get('Groups', []):
                    cost = float(group['Metrics']['BlendedCost']['Amount'])
                    service = group['Keys'][0]
                    
                    total_cost += cost
                    daily_cost += cost
                    
                    if service not in service_costs:
                        service_costs[service] = 0.0
                    service_costs[service] += cost
                
                daily_costs.append(daily_cost)
            
            # Calculate cost trends
            cost_trend = 0.0
            if len(daily_costs) > 1:
                recent_avg = np.mean(daily_costs[-7:])  # Last 7 days
                previous_avg = np.mean(daily_costs[-14:-7])  # Previous 7 days
                if previous_avg > 0:
                    cost_trend = (recent_avg - previous_avg) / previous_avg
            
            return {
                'total_monthly_cost': total_cost,
                'average_daily_cost': np.mean(daily_costs) if daily_costs else 0.0,
                'cost_trend': cost_trend,
                'highest_cost_service': max(service_costs.items(), key=lambda x: x[1])[0] if service_costs else 'unknown',
                'highest_cost_service_amount': max(service_costs.values()) if service_costs else 0.0,
                'service_count': len(service_costs)
            }
            
        except Exception as e:
            self.logger.error(f"Error collecting cost metrics: {str(e)}")
            return {
                'total_monthly_cost': 0.0,
                'average_daily_cost': 0.0,
                'cost_trend': 0.0,
                'highest_cost_service': 'unknown',
                'highest_cost_service_amount': 0.0,
                'service_count': 0
            }
    
    def get_performance_metrics(self, workload_id: str, start_date: datetime, end_date: datetime) -> Dict[str, float]:
        """Get performance metrics for workload"""
        
        try:
            # Get CloudWatch metrics for common performance indicators
            metrics_to_collect = [
                ('AWS/EC2', 'CPUUtilization'),
                ('AWS/ApplicationELB', 'ResponseTime'),
                ('AWS/RDS', 'DatabaseConnections'),
                ('AWS/Lambda', 'Duration'),
                ('AWS/Lambda', 'Errors')
            ]
            
            performance_data = {}
            
            for namespace, metric_name in metrics_to_collect:
                try:
                    response = self.cloudwatch.get_metric_statistics(
                        Namespace=namespace,
                        MetricName=metric_name,
                        Dimensions=[
                            {'Name': 'WorkloadId', 'Value': workload_id}
                        ],
                        StartTime=start_date,
                        EndTime=end_date,
                        Period=3600,  # 1 hour periods
                        Statistics=['Average', 'Maximum']
                    )
                    
                    if response['Datapoints']:
                        avg_values = [dp['Average'] for dp in response['Datapoints']]
                        max_values = [dp['Maximum'] for dp in response['Datapoints']]
                        
                        performance_data[f'{metric_name.lower()}_avg'] = np.mean(avg_values)
                        performance_data[f'{metric_name.lower()}_max'] = np.max(max_values)
                
                except Exception as metric_error:
                    self.logger.warning(f"Could not collect {metric_name}: {str(metric_error)}")
                    continue
            
            return performance_data
            
        except Exception as e:
            self.logger.error(f"Error collecting performance metrics: {str(e)}")
            return {}
    
    def get_utilization_metrics(self, workload_id: str, start_date: datetime, end_date: datetime) -> Dict[str, float]:
        """Get resource utilization metrics"""
        
        try:
            utilization_metrics = {}
            
            # EC2 utilization
            ec2_response = self.cloudwatch.get_metric_statistics(
                Namespace='AWS/EC2',
                MetricName='CPUUtilization',
                Dimensions=[{'Name': 'WorkloadId', 'Value': workload_id}],
                StartTime=start_date,
                EndTime=end_date,
                Period=3600,
                Statistics=['Average']
            )
            
            if ec2_response['Datapoints']:
                cpu_utilization = [dp['Average'] for dp in ec2_response['Datapoints']]
                utilization_metrics['avg_cpu_utilization'] = np.mean(cpu_utilization)
                utilization_metrics['max_cpu_utilization'] = np.max(cpu_utilization)
                utilization_metrics['min_cpu_utilization'] = np.min(cpu_utilization)
            
            # RDS utilization
            rds_response = self.cloudwatch.get_metric_statistics(
                Namespace='AWS/RDS',
                MetricName='CPUUtilization',
                Dimensions=[{'Name': 'WorkloadId', 'Value': workload_id}],
                StartTime=start_date,
                EndTime=end_date,
                Period=3600,
                Statistics=['Average']
            )
            
            if rds_response['Datapoints']:
                rds_cpu = [dp['Average'] for dp in rds_response['Datapoints']]
                utilization_metrics['avg_rds_cpu_utilization'] = np.mean(rds_cpu)
            
            return utilization_metrics
            
        except Exception as e:
            self.logger.error(f"Error collecting utilization metrics: {str(e)}")
            return {}
    
    def get_availability_metrics(self, workload_id: str, start_date: datetime, end_date: datetime) -> Dict[str, float]:
        """Get availability and reliability metrics"""
        
        try:
            availability_metrics = {}
            
            # Application Load Balancer health
            alb_response = self.cloudwatch.get_metric_statistics(
                Namespace='AWS/ApplicationELB',
                MetricName='HealthyHostCount',
                Dimensions=[{'Name': 'WorkloadId', 'Value': workload_id}],
                StartTime=start_date,
                EndTime=end_date,
                Period=3600,
                Statistics=['Average']
            )
            
            if alb_response['Datapoints']:
                healthy_hosts = [dp['Average'] for dp in alb_response['Datapoints']]
                availability_metrics['avg_healthy_hosts'] = np.mean(healthy_hosts)
                availability_metrics['min_healthy_hosts'] = np.min(healthy_hosts)
            
            # Lambda error rates
            lambda_response = self.cloudwatch.get_metric_statistics(
                Namespace='AWS/Lambda',
                MetricName='Errors',
                Dimensions=[{'Name': 'WorkloadId', 'Value': workload_id}],
                StartTime=start_date,
                EndTime=end_date,
                Period=3600,
                Statistics=['Sum']
            )
            
            if lambda_response['Datapoints']:
                total_errors = sum(dp['Sum'] for dp in lambda_response['Datapoints'])
                availability_metrics['total_lambda_errors'] = total_errors
            
            return availability_metrics
            
        except Exception as e:
            self.logger.error(f"Error collecting availability metrics: {str(e)}")
            return {}
    
    def get_security_metrics(self, workload_id: str) -> Dict[str, float]:
        """Get security-related metrics"""
        
        try:
            security_metrics = {}
            
            # Config compliance
            try:
                config_response = self.config.get_compliance_summary_by_config_rule()
                
                compliant_rules = config_response['ComplianceSummary']['ComplianceByConfigRule']['COMPLIANT']
                non_compliant_rules = config_response['ComplianceSummary']['ComplianceByConfigRule']['NON_COMPLIANT']
                total_rules = compliant_rules + non_compliant_rules
                
                if total_rules > 0:
                    security_metrics['config_compliance_percentage'] = (compliant_rules / total_rules) * 100
                else:
                    security_metrics['config_compliance_percentage'] = 100.0
                    
            except Exception as config_error:
                self.logger.warning(f"Could not collect Config compliance: {str(config_error)}")
                security_metrics['config_compliance_percentage'] = 0.0
            
            # Trusted Advisor security checks (if available)
            try:
                ta_response = self.trusted_advisor.describe_trusted_advisor_checks(language='en')
                security_checks = [
                    check for check in ta_response['checks'] 
                    if 'security' in check['category'].lower()
                ]
                security_metrics['security_checks_available'] = len(security_checks)
                
            except Exception as ta_error:
                self.logger.warning(f"Could not collect Trusted Advisor data: {str(ta_error)}")
                security_metrics['security_checks_available'] = 0
            
            return security_metrics
            
        except Exception as e:
            self.logger.error(f"Error collecting security metrics: {str(e)}")
            return {}
```

Let me continue with the rest of the implementation:
    
    def identify_optimization_opportunities(self, workload_id: str, metrics: WorkloadMetrics) -> List[OptimizationOpportunity]:
        """Identify optimization opportunities based on workload analysis"""
        
        opportunities = []
        
        # Cost optimization opportunities
        cost_opportunities = self.identify_cost_opportunities(workload_id, metrics)
        opportunities.extend(cost_opportunities)
        
        # Performance optimization opportunities
        performance_opportunities = self.identify_performance_opportunities(workload_id, metrics)
        opportunities.extend(performance_opportunities)
        
        # Utilization optimization opportunities
        utilization_opportunities = self.identify_utilization_opportunities(workload_id, metrics)
        opportunities.extend(utilization_opportunities)
        
        # Security optimization opportunities
        security_opportunities = self.identify_security_opportunities(workload_id, metrics)
        opportunities.extend(security_opportunities)
        
        # New service adoption opportunities
        new_service_opportunities = self.identify_new_service_opportunities(workload_id, metrics)
        opportunities.extend(new_service_opportunities)
        
        return opportunities
    
    def identify_cost_opportunities(self, workload_id: str, metrics: WorkloadMetrics) -> List[OptimizationOpportunity]:
        """Identify cost optimization opportunities"""
        
        opportunities = []
        
        # High cost alert
        if metrics.cost_metrics.get('total_monthly_cost', 0) > self.analysis_config['cost_thresholds']['high_cost_resource']:
            opportunities.append(OptimizationOpportunity(
                opportunity_id=f"COST_{workload_id}_{datetime.now().strftime('%Y%m%d')}_001",
                workload_id=workload_id,
                category=AnalysisCategory.COST_OPTIMIZATION,
                description="High monthly cost detected - review for optimization opportunities",
                current_state=f"Monthly cost: ${metrics.cost_metrics['total_monthly_cost']:,.2f}",
                proposed_solution="Conduct detailed cost analysis and right-sizing review",
                estimated_savings=metrics.cost_metrics['total_monthly_cost'] * 0.15,  # Estimate 15% savings
                implementation_effort="Medium",
                risk_level="Low",
                priority="High",
                status=OptimizationStatus.IDENTIFIED,
                identified_date=datetime.now()
            ))
        
        # Cost trend alert
        cost_trend = metrics.cost_metrics.get('cost_trend', 0)
        if cost_trend > self.analysis_config['cost_thresholds']['cost_increase_alert']:
            opportunities.append(OptimizationOpportunity(
                opportunity_id=f"COST_{workload_id}_{datetime.now().strftime('%Y%m%d')}_002",
                workload_id=workload_id,
                category=AnalysisCategory.COST_OPTIMIZATION,
                description=f"Cost increasing trend detected: {cost_trend:.1%} increase",
                current_state=f"Cost trend: {cost_trend:.1%} increase over last week",
                proposed_solution="Investigate cost drivers and implement cost controls",
                estimated_savings=metrics.cost_metrics['average_daily_cost'] * 30 * abs(cost_trend),
                implementation_effort="Low",
                risk_level="Low",
                priority="Medium",
                status=OptimizationStatus.IDENTIFIED,
                identified_date=datetime.now()
            ))
        
        # Service-specific cost opportunities
        highest_cost_service = metrics.cost_metrics.get('highest_cost_service', '')
        highest_cost_amount = metrics.cost_metrics.get('highest_cost_service_amount', 0)
        
        if highest_cost_amount > 500:  # If highest cost service > $500/month
            opportunities.append(OptimizationOpportunity(
                opportunity_id=f"COST_{workload_id}_{datetime.now().strftime('%Y%m%d')}_003",
                workload_id=workload_id,
                category=AnalysisCategory.COST_OPTIMIZATION,
                description=f"High cost service optimization: {highest_cost_service}",
                current_state=f"{highest_cost_service} costs ${highest_cost_amount:,.2f}/month",
                proposed_solution=f"Review {highest_cost_service} configuration and usage patterns",
                estimated_savings=highest_cost_amount * 0.2,  # Estimate 20% savings
                implementation_effort="Medium",
                risk_level="Medium",
                priority="High",
                status=OptimizationStatus.IDENTIFIED,
                identified_date=datetime.now()
            ))
        
        return opportunities
    
    def identify_performance_opportunities(self, workload_id: str, metrics: WorkloadMetrics) -> List[OptimizationOpportunity]:
        """Identify performance optimization opportunities"""
        
        opportunities = []
        
        # High response time
        response_time = metrics.performance_metrics.get('responsetime_avg', 0)
        if response_time > 2.0:  # > 2 seconds average response time
            opportunities.append(OptimizationOpportunity(
                opportunity_id=f"PERF_{workload_id}_{datetime.now().strftime('%Y%m%d')}_001",
                workload_id=workload_id,
                category=AnalysisCategory.PERFORMANCE_IMPROVEMENT,
                description="High response time detected",
                current_state=f"Average response time: {response_time:.2f} seconds",
                proposed_solution="Implement caching, optimize database queries, or consider CDN",
                estimated_savings=0.0,  # Performance improvement, not direct cost savings
                implementation_effort="Medium",
                risk_level="Medium",
                priority="High",
                status=OptimizationStatus.IDENTIFIED,
                identified_date=datetime.now()
            ))
        
        # High Lambda duration
        lambda_duration = metrics.performance_metrics.get('duration_avg', 0)
        if lambda_duration > 10000:  # > 10 seconds average duration
            opportunities.append(OptimizationOpportunity(
                opportunity_id=f"PERF_{workload_id}_{datetime.now().strftime('%Y%m%d')}_002",
                workload_id=workload_id,
                category=AnalysisCategory.PERFORMANCE_IMPROVEMENT,
                description="High Lambda function duration",
                current_state=f"Average Lambda duration: {lambda_duration:.0f}ms",
                proposed_solution="Optimize Lambda function code and consider provisioned concurrency",
                estimated_savings=100.0,  # Estimated cost savings from optimization
                implementation_effort="Medium",
                risk_level="Low",
                priority="Medium",
                status=OptimizationStatus.IDENTIFIED,
                identified_date=datetime.now()
            ))
        
        return opportunities
    
    def identify_utilization_opportunities(self, workload_id: str, metrics: WorkloadMetrics) -> List[OptimizationOpportunity]:
        """Identify resource utilization optimization opportunities"""
        
        opportunities = []
        
        # Low CPU utilization
        avg_cpu = metrics.utilization_metrics.get('avg_cpu_utilization', 100)
        if avg_cpu < 20:  # < 20% average CPU utilization
            opportunities.append(OptimizationOpportunity(
                opportunity_id=f"UTIL_{workload_id}_{datetime.now().strftime('%Y%m%d')}_001",
                workload_id=workload_id,
                category=AnalysisCategory.COST_OPTIMIZATION,
                description="Low CPU utilization - right-sizing opportunity",
                current_state=f"Average CPU utilization: {avg_cpu:.1f}%",
                proposed_solution="Right-size EC2 instances to smaller instance types",
                estimated_savings=metrics.cost_metrics.get('total_monthly_cost', 0) * 0.3,
                implementation_effort="Low",
                risk_level="Medium",
                priority="High",
                status=OptimizationStatus.IDENTIFIED,
                identified_date=datetime.now()
            ))
        
        # High CPU utilization
        max_cpu = metrics.utilization_metrics.get('max_cpu_utilization', 0)
        if max_cpu > 90:  # > 90% max CPU utilization
            opportunities.append(OptimizationOpportunity(
                opportunity_id=f"UTIL_{workload_id}_{datetime.now().strftime('%Y%m%d')}_002",
                workload_id=workload_id,
                category=AnalysisCategory.PERFORMANCE_IMPROVEMENT,
                description="High CPU utilization - scaling opportunity",
                current_state=f"Maximum CPU utilization: {max_cpu:.1f}%",
                proposed_solution="Implement auto-scaling or upgrade to larger instance types",
                estimated_savings=0.0,  # Performance improvement
                implementation_effort="Medium",
                risk_level="Low",
                priority="High",
                status=OptimizationStatus.IDENTIFIED,
                identified_date=datetime.now()
            ))
        
        return opportunities
    
    def identify_security_opportunities(self, workload_id: str, metrics: WorkloadMetrics) -> List[OptimizationOpportunity]:
        """Identify security optimization opportunities"""
        
        opportunities = []
        
        # Low Config compliance
        compliance_percentage = metrics.security_metrics.get('config_compliance_percentage', 100)
        if compliance_percentage < 90:
            opportunities.append(OptimizationOpportunity(
                opportunity_id=f"SEC_{workload_id}_{datetime.now().strftime('%Y%m%d')}_001",
                workload_id=workload_id,
                category=AnalysisCategory.SECURITY_ENHANCEMENT,
                description="Low Config compliance score",
                current_state=f"Config compliance: {compliance_percentage:.1f}%",
                proposed_solution="Review and remediate Config rule violations",
                estimated_savings=0.0,  # Security improvement
                implementation_effort="Medium",
                risk_level="High",
                priority="High",
                status=OptimizationStatus.IDENTIFIED,
                identified_date=datetime.now()
            ))
        
        return opportunities
    
    def identify_new_service_opportunities(self, workload_id: str, metrics: WorkloadMetrics) -> List[OptimizationOpportunity]:
        """Identify opportunities to adopt new AWS services"""
        
        opportunities = []
        
        # Serverless migration opportunity
        avg_cpu = metrics.utilization_metrics.get('avg_cpu_utilization', 100)
        if avg_cpu < 30 and metrics.cost_metrics.get('total_monthly_cost', 0) > 200:
            opportunities.append(OptimizationOpportunity(
                opportunity_id=f"NEW_{workload_id}_{datetime.now().strftime('%Y%m%d')}_001",
                workload_id=workload_id,
                category=AnalysisCategory.COST_OPTIMIZATION,
                description="Serverless migration opportunity",
                current_state=f"Low utilization ({avg_cpu:.1f}%) with significant costs",
                proposed_solution="Evaluate migration to AWS Lambda or Fargate",
                estimated_savings=metrics.cost_metrics.get('total_monthly_cost', 0) * 0.4,
                implementation_effort="High",
                risk_level="Medium",
                priority="Medium",
                status=OptimizationStatus.IDENTIFIED,
                identified_date=datetime.now()
            ))
        
        # Graviton processor opportunity
        if metrics.cost_metrics.get('highest_cost_service', '') == 'Amazon Elastic Compute Cloud - Compute':
            opportunities.append(OptimizationOpportunity(
                opportunity_id=f"NEW_{workload_id}_{datetime.now().strftime('%Y%m%d')}_002",
                workload_id=workload_id,
                category=AnalysisCategory.COST_OPTIMIZATION,
                description="AWS Graviton processor migration opportunity",
                current_state="Using x86-based EC2 instances",
                proposed_solution="Evaluate migration to Graviton-based instances for cost savings",
                estimated_savings=metrics.cost_metrics.get('highest_cost_service_amount', 0) * 0.2,
                implementation_effort="Medium",
                risk_level="Low",
                priority="Medium",
                status=OptimizationStatus.IDENTIFIED,
                identified_date=datetime.now()
            ))
        
        return opportunities
    
    def generate_optimization_recommendations(self, opportunities: List[OptimizationOpportunity], 
                                            metrics: WorkloadMetrics) -> List[Dict]:
        """Generate actionable optimization recommendations"""
        
        recommendations = []
        
        # Prioritize opportunities by potential savings and effort
        high_value_opportunities = [
            opp for opp in opportunities 
            if opp.estimated_savings > 500 and opp.implementation_effort in ['Low', 'Medium']
        ]
        
        if high_value_opportunities:
            recommendations.append({
                'type': 'high_value_optimization',
                'priority': 'High',
                'title': 'High-Value Optimization Opportunities',
                'description': f"Identified {len(high_value_opportunities)} high-value optimization opportunities",
                'action_items': [
                    f"{opp.description} - Estimated savings: ${opp.estimated_savings:,.2f}"
                    for opp in high_value_opportunities[:5]  # Top 5
                ],
                'estimated_total_savings': sum(opp.estimated_savings for opp in high_value_opportunities)
            })
        
        # Quick wins (low effort, medium savings)
        quick_wins = [
            opp for opp in opportunities 
            if opp.implementation_effort == 'Low' and opp.estimated_savings > 100
        ]
        
        if quick_wins:
            recommendations.append({
                'type': 'quick_wins',
                'priority': 'Medium',
                'title': 'Quick Win Opportunities',
                'description': f"Identified {len(quick_wins)} quick win opportunities",
                'action_items': [
                    f"{opp.description} - Effort: {opp.implementation_effort}"
                    for opp in quick_wins[:3]  # Top 3
                ],
                'estimated_total_savings': sum(opp.estimated_savings for opp in quick_wins)
            })
        
        # Performance improvements
        performance_opportunities = [
            opp for opp in opportunities 
            if opp.category == AnalysisCategory.PERFORMANCE_IMPROVEMENT
        ]
        
        if performance_opportunities:
            recommendations.append({
                'type': 'performance_improvement',
                'priority': 'Medium',
                'title': 'Performance Improvement Opportunities',
                'description': f"Identified {len(performance_opportunities)} performance improvement opportunities",
                'action_items': [
                    opp.description for opp in performance_opportunities[:3]
                ],
                'estimated_total_savings': sum(opp.estimated_savings for opp in performance_opportunities)
            })
        
        # Security enhancements
        security_opportunities = [
            opp for opp in opportunities 
            if opp.category == AnalysisCategory.SECURITY_ENHANCEMENT
        ]
        
        if security_opportunities:
            recommendations.append({
                'type': 'security_enhancement',
                'priority': 'High',
                'title': 'Security Enhancement Opportunities',
                'description': f"Identified {len(security_opportunities)} security improvement opportunities",
                'action_items': [
                    opp.description for opp in security_opportunities
                ],
                'estimated_total_savings': 0.0  # Security improvements don't have direct cost savings
            })
        
        return recommendations
    
    def calculate_workload_score(self, metrics: WorkloadMetrics, 
                               opportunities: List[OptimizationOpportunity]) -> float:
        """Calculate overall workload optimization score (0-100)"""
        
        score = 100.0  # Start with perfect score
        
        # Deduct points for cost issues
        cost_trend = metrics.cost_metrics.get('cost_trend', 0)
        if cost_trend > 0.1:  # > 10% cost increase
            score -= 20
        elif cost_trend > 0.05:  # > 5% cost increase
            score -= 10
        
        # Deduct points for utilization issues
        avg_cpu = metrics.utilization_metrics.get('avg_cpu_utilization', 50)
        if avg_cpu < 20:  # Very low utilization
            score -= 15
        elif avg_cpu > 90:  # Very high utilization
            score -= 10
        
        # Deduct points for performance issues
        response_time = metrics.performance_metrics.get('responsetime_avg', 1.0)
        if response_time > 3.0:  # > 3 seconds
            score -= 20
        elif response_time > 2.0:  # > 2 seconds
            score -= 10
        
        # Deduct points for security issues
        compliance = metrics.security_metrics.get('config_compliance_percentage', 100)
        if compliance < 80:
            score -= 25
        elif compliance < 90:
            score -= 15
        
        # Deduct points for number of high-priority opportunities
        high_priority_opportunities = len([
            opp for opp in opportunities 
            if opp.priority == 'High'
        ])
        score -= min(high_priority_opportunities * 5, 30)  # Max 30 points deduction
        
        return max(0.0, score)  # Ensure score doesn't go below 0
    
    def identify_improvement_areas(self, metrics: WorkloadMetrics, 
                                 opportunities: List[OptimizationOpportunity]) -> List[str]:
        """Identify key areas for improvement"""
        
        improvement_areas = []
        
        # Cost optimization
        cost_opportunities = [opp for opp in opportunities if opp.category == AnalysisCategory.COST_OPTIMIZATION]
        if cost_opportunities:
            improvement_areas.append("Cost Optimization")
        
        # Performance improvement
        performance_opportunities = [opp for opp in opportunities if opp.category == AnalysisCategory.PERFORMANCE_IMPROVEMENT]
        if performance_opportunities:
            improvement_areas.append("Performance Optimization")
        
        # Security enhancement
        security_opportunities = [opp for opp in opportunities if opp.category == AnalysisCategory.SECURITY_ENHANCEMENT]
        if security_opportunities:
            improvement_areas.append("Security Enhancement")
        
        # Utilization optimization
        avg_cpu = metrics.utilization_metrics.get('avg_cpu_utilization', 50)
        if avg_cpu < 30 or avg_cpu > 85:
            improvement_areas.append("Resource Utilization")
        
        # Operational efficiency
        if metrics.cost_metrics.get('service_count', 0) > 10:
            improvement_areas.append("Architecture Simplification")
        
        return improvement_areas
    
    def calculate_next_review_date(self, workload_id: str, review_score: float) -> datetime:
        """Calculate next review date based on workload score and criticality"""
        
        # Get workload criticality (this would come from workload metadata)
        workload_criticality = self.get_workload_criticality(workload_id)
        
        # Determine review frequency based on score and criticality
        if review_score < 60:  # Poor score
            days_until_next_review = 30  # Monthly review
        elif review_score < 80:  # Fair score
            days_until_next_review = 60  # Bi-monthly review
        else:  # Good score
            if workload_criticality == 'critical':
                days_until_next_review = 90  # Quarterly review
            elif workload_criticality == 'important':
                days_until_next_review = 180  # Semi-annual review
            else:
                days_until_next_review = 365  # Annual review
        
        return datetime.now() + timedelta(days=days_until_next_review)
    
    def get_workload_criticality(self, workload_id: str) -> str:
        """Get workload criticality level"""
        # This would typically come from a workload registry or tagging
        # For now, return a default value
        return 'important'
    
    def store_review_results(self, review_result: WorkloadReviewResult):
        """Store review results for tracking and historical analysis"""
        
        try:
            # Store in Systems Manager Parameter Store
            parameter_name = f"/workload-reviews/{review_result.workload_id}/{review_result.review_id}"
            
            review_data = {
                'review_id': review_result.review_id,
                'workload_id': review_result.workload_id,
                'review_date': review_result.review_date.isoformat(),
                'review_score': review_result.review_score,
                'opportunities_count': len(review_result.opportunities_identified),
                'total_estimated_savings': sum(opp.estimated_savings for opp in review_result.opportunities_identified),
                'improvement_areas': review_result.improvement_areas,
                'next_review_date': review_result.next_review_date.isoformat()
            }
            
            self.systems_manager.put_parameter(
                Name=parameter_name,
                Value=json.dumps(review_data),
                Type='String',
                Overwrite=True,
                Description=f'Workload review results for {review_result.workload_id}'
            )
            
            # Also send metrics to CloudWatch
            self.cloudwatch.put_metric_data(
                Namespace='WorkloadAnalysis',
                MetricData=[
                    {
                        'MetricName': 'ReviewScore',
                        'Dimensions': [
                            {'Name': 'WorkloadId', 'Value': review_result.workload_id}
                        ],
                        'Value': review_result.review_score,
                        'Unit': 'None'
                    },
                    {
                        'MetricName': 'OptimizationOpportunities',
                        'Dimensions': [
                            {'Name': 'WorkloadId', 'Value': review_result.workload_id}
                        ],
                        'Value': len(review_result.opportunities_identified),
                        'Unit': 'Count'
                    },
                    {
                        'MetricName': 'EstimatedSavings',
                        'Dimensions': [
                            {'Name': 'WorkloadId', 'Value': review_result.workload_id}
                        ],
                        'Value': sum(opp.estimated_savings for opp in review_result.opportunities_identified),
                        'Unit': 'None'
                    }
                ]
            )
            
            self.logger.info(f"Stored review results for workload {review_result.workload_id}")
            
        except Exception as e:
            self.logger.error(f"Error storing review results: {str(e)}")
    
    def generate_workload_analysis_report(self, review_result: WorkloadReviewResult) -> str:
        """Generate comprehensive workload analysis report"""
        
        report = f"""
# Workload Analysis Report

## Executive Summary
- **Workload ID**: {review_result.workload_id}
- **Review Date**: {review_result.review_date.strftime('%Y-%m-%d %H:%M:%S')}
- **Overall Score**: {review_result.review_score:.1f}/100
- **Optimization Opportunities**: {len(review_result.opportunities_identified)}
- **Total Estimated Savings**: ${sum(opp.estimated_savings for opp in review_result.opportunities_identified):,.2f}

## Current Metrics
### Cost Metrics
- **Monthly Cost**: ${review_result.metrics_analyzed.cost_metrics.get('total_monthly_cost', 0):,.2f}
- **Daily Average**: ${review_result.metrics_analyzed.cost_metrics.get('average_daily_cost', 0):,.2f}
- **Cost Trend**: {review_result.metrics_analyzed.cost_metrics.get('cost_trend', 0):.1%}
- **Highest Cost Service**: {review_result.metrics_analyzed.cost_metrics.get('highest_cost_service', 'N/A')}

### Performance Metrics
- **Average Response Time**: {review_result.metrics_analyzed.performance_metrics.get('responsetime_avg', 0):.2f}s
- **Average CPU Utilization**: {review_result.metrics_analyzed.utilization_metrics.get('avg_cpu_utilization', 0):.1f}%
- **Security Compliance**: {review_result.metrics_analyzed.security_metrics.get('config_compliance_percentage', 0):.1f}%

## Optimization Opportunities
"""
        
        # Group opportunities by category
        opportunities_by_category = {}
        for opp in review_result.opportunities_identified:
            category = opp.category.value
            if category not in opportunities_by_category:
                opportunities_by_category[category] = []
            opportunities_by_category[category].append(opp)
        
        for category, opportunities in opportunities_by_category.items():
            report += f"\n### {category.replace('_', ' ').title()}\n"
            for opp in opportunities[:3]:  # Top 3 per category
                report += f"- **{opp.description}**\n"
                report += f"  - Current State: {opp.current_state}\n"
                report += f"  - Proposed Solution: {opp.proposed_solution}\n"
                report += f"  - Estimated Savings: ${opp.estimated_savings:,.2f}\n"
                report += f"  - Priority: {opp.priority}\n\n"
        
        # Recommendations
        report += "\n## Recommendations\n"
        for i, rec in enumerate(review_result.recommendations, 1):
            report += f"\n### {i}. {rec['title']}\n"
            report += f"- **Priority**: {rec['priority']}\n"
            report += f"- **Description**: {rec['description']}\n"
            if rec.get('estimated_total_savings', 0) > 0:
                report += f"- **Total Estimated Savings**: ${rec['estimated_total_savings']:,.2f}\n"
            
            if rec.get('action_items'):
                report += "- **Action Items**:\n"
                for item in rec['action_items']:
                    report += f"  - {item}\n"
        
        # Next steps
        report += f"\n## Next Steps\n"
        report += f"- **Next Review Date**: {review_result.next_review_date.strftime('%Y-%m-%d')}\n"
        report += f"- **Key Improvement Areas**: {', '.join(review_result.improvement_areas)}\n"
        report += f"- **Recommended Actions**: Prioritize high-value optimization opportunities\n"
        
        return report
```

Now let me add the usage examples and complete the file:
## Usage Examples

### Example 1: Comprehensive Workload Analysis

```python
# Initialize the workload analysis manager
analysis_manager = WorkloadAnalysisManager()

# Conduct comprehensive analysis for a critical workload
workload_id = "ecommerce-platform-prod"
review_result = analysis_manager.conduct_workload_analysis(
    workload_id=workload_id,
    analysis_type="comprehensive"
)

# Print summary results
print(f"Workload Score: {review_result.review_score:.1f}/100")
print(f"Opportunities Identified: {len(review_result.opportunities_identified)}")
print(f"Total Estimated Savings: ${sum(opp.estimated_savings for opp in review_result.opportunities_identified):,.2f}")

# Generate and display report
report = analysis_manager.generate_workload_analysis_report(review_result)
print(report)

# Check high-priority opportunities
high_priority_opportunities = [
    opp for opp in review_result.opportunities_identified 
    if opp.priority == 'High'
]

if high_priority_opportunities:
    print("\n🚨 High Priority Opportunities:")
    for opp in high_priority_opportunities:
        print(f"- {opp.description}")
        print(f"  Estimated Savings: ${opp.estimated_savings:,.2f}")
        print(f"  Implementation Effort: {opp.implementation_effort}")
```

### Example 2: Automated Regular Review Process

```python
# Set up automated review process for multiple workloads
workloads_to_review = [
    {"id": "web-app-prod", "criticality": "critical"},
    {"id": "data-pipeline", "criticality": "important"},
    {"id": "reporting-system", "criticality": "standard"}
]

def automated_workload_review_process():
    """Automated process for regular workload reviews"""
    
    analysis_manager = WorkloadAnalysisManager()
    review_results = []
    
    for workload in workloads_to_review:
        workload_id = workload["id"]
        criticality = workload["criticality"]
        
        print(f"\n📊 Analyzing workload: {workload_id} ({criticality})")
        
        # Conduct analysis
        review_result = analysis_manager.conduct_workload_analysis(
            workload_id=workload_id,
            analysis_type="comprehensive" if criticality == "critical" else "focused"
        )
        
        review_results.append(review_result)
        
        # Alert on poor scores
        if review_result.review_score < 70:
            print(f"⚠️  LOW SCORE ALERT: {workload_id} scored {review_result.review_score:.1f}/100")
            
            # Send notification (implementation would depend on your notification system)
            send_low_score_alert(workload_id, review_result.review_score)
        
        # Alert on high-value opportunities
        high_value_opportunities = [
            opp for opp in review_result.opportunities_identified
            if opp.estimated_savings > 1000
        ]
        
        if high_value_opportunities:
            total_savings = sum(opp.estimated_savings for opp in high_value_opportunities)
            print(f"💰 HIGH VALUE OPPORTUNITIES: ${total_savings:,.2f} potential savings")
    
    # Generate summary report
    generate_portfolio_summary_report(review_results)
    
    return review_results

def send_low_score_alert(workload_id: str, score: float):
    """Send alert for workloads with low optimization scores"""
    # Implementation would integrate with your alerting system
    print(f"🚨 ALERT: Workload {workload_id} requires immediate attention (Score: {score:.1f})")

def generate_portfolio_summary_report(review_results: List[WorkloadReviewResult]):
    """Generate summary report across all workloads"""
    
    total_workloads = len(review_results)
    average_score = sum(result.review_score for result in review_results) / total_workloads
    total_opportunities = sum(len(result.opportunities_identified) for result in review_results)
    total_potential_savings = sum(
        sum(opp.estimated_savings for opp in result.opportunities_identified)
        for result in review_results
    )
    
    print(f"""
📈 PORTFOLIO OPTIMIZATION SUMMARY
================================
Total Workloads Analyzed: {total_workloads}
Average Optimization Score: {average_score:.1f}/100
Total Opportunities Identified: {total_opportunities}
Total Potential Savings: ${total_potential_savings:,.2f}

Top Recommendations:
- Focus on workloads with scores below 70
- Prioritize high-value optimization opportunities
- Implement quick wins for immediate impact
""")

# Run the automated review process
review_results = automated_workload_review_process()
```

### Example 3: Trend Analysis and Historical Comparison

```python
def analyze_workload_trends(workload_id: str, months_back: int = 6):
    """Analyze workload optimization trends over time"""
    
    analysis_manager = WorkloadAnalysisManager()
    
    # Get historical review data
    historical_reviews = get_historical_reviews(workload_id, months_back)
    
    if len(historical_reviews) < 2:
        print("Insufficient historical data for trend analysis")
        return
    
    # Analyze trends
    scores = [review['review_score'] for review in historical_reviews]
    costs = [review['monthly_cost'] for review in historical_reviews]
    opportunities = [review['opportunities_count'] for review in historical_reviews]
    
    # Calculate trends
    score_trend = (scores[-1] - scores[0]) / scores[0] if scores[0] > 0 else 0
    cost_trend = (costs[-1] - costs[0]) / costs[0] if costs[0] > 0 else 0
    
    print(f"""
📊 WORKLOAD TREND ANALYSIS: {workload_id}
==========================================
Review Period: {months_back} months
Number of Reviews: {len(historical_reviews)}

Score Trend: {score_trend:+.1%} ({'Improving' if score_trend > 0 else 'Declining'})
Cost Trend: {cost_trend:+.1%} ({'Increasing' if cost_trend > 0 else 'Decreasing'})

Current Status:
- Latest Score: {scores[-1]:.1f}/100
- Latest Monthly Cost: ${costs[-1]:,.2f}
- Active Opportunities: {opportunities[-1]}

Recommendations:
""")
    
    if score_trend < -0.1:  # Score declining by more than 10%
        print("- 🚨 Optimization score is declining - immediate review recommended")
    
    if cost_trend > 0.2:  # Cost increasing by more than 20%
        print("- 💸 Cost is increasing significantly - cost optimization review needed")
    
    if opportunities[-1] > 5:
        print("- 🎯 Multiple optimization opportunities available - prioritize implementation")

def get_historical_reviews(workload_id: str, months_back: int) -> List[Dict]:
    """Get historical review data for trend analysis"""
    # This would query your review data storage
    # For demonstration, returning sample data
    
    sample_data = []
    for i in range(months_back):
        date = datetime.now() - timedelta(days=30 * i)
        sample_data.append({
            'review_date': date,
            'review_score': 75 + (i * 2),  # Improving trend
            'monthly_cost': 5000 - (i * 100),  # Decreasing cost
            'opportunities_count': max(1, 8 - i)  # Decreasing opportunities
        })
    
    return list(reversed(sample_data))  # Chronological order

# Analyze trends for a specific workload
analyze_workload_trends("ecommerce-platform-prod", months_back=6)
```

## Review Schedule Templates

### Workload Review Schedule Configuration
```yaml
Workload_Review_Schedules:
  critical_workloads:
    frequency: "monthly"
    analysis_type: "comprehensive"
    stakeholders: ["technical_lead", "business_owner", "cost_optimization_team"]
    duration: "2 weeks"
    deliverables:
      - "Detailed analysis report"
      - "Optimization roadmap"
      - "Cost-benefit analysis"
      - "Implementation timeline"
    
  important_workloads:
    frequency: "quarterly"
    analysis_type: "focused"
    stakeholders: ["technical_lead", "cost_optimization_team"]
    duration: "1 week"
    deliverables:
      - "Analysis summary"
      - "Priority optimization opportunities"
      - "Quick wins identification"
    
  standard_workloads:
    frequency: "annually"
    analysis_type: "rapid"
    stakeholders: ["technical_lead"]
    duration: "3 days"
    deliverables:
      - "Basic analysis report"
      - "High-level recommendations"

Review_Triggers:
  cost_spike:
    threshold: "20% increase over 7 days"
    action: "immediate_review"
    analysis_type: "focused"
    
  performance_degradation:
    threshold: "response_time > 3 seconds"
    action: "performance_review"
    analysis_type: "focused"
    
  security_compliance_drop:
    threshold: "compliance < 90%"
    action: "security_review"
    analysis_type: "comprehensive"
    
  new_service_announcement:
    trigger: "relevant_aws_service_launch"
    action: "service_evaluation_review"
    analysis_type: "rapid"

Analysis_Metrics:
  cost_optimization:
    - "monthly_cost_trend"
    - "service_cost_distribution"
    - "utilization_efficiency"
    - "reserved_instance_coverage"
    
  performance_optimization:
    - "response_time_percentiles"
    - "throughput_metrics"
    - "error_rates"
    - "availability_metrics"
    
  security_optimization:
    - "config_compliance_score"
    - "security_group_analysis"
    - "encryption_coverage"
    - "access_pattern_analysis"
    
  operational_optimization:
    - "automation_coverage"
    - "monitoring_completeness"
    - "backup_compliance"
    - "disaster_recovery_readiness"
```

## Common Challenges and Solutions

### Challenge: Data Collection Complexity

**Solution**: Implement automated data collection pipelines using AWS APIs and CloudWatch metrics. Create standardized data collection templates and use AWS Config for configuration tracking.

### Challenge: Analysis Consistency

**Solution**: Develop standardized analysis frameworks and scoring methodologies. Use automated analysis tools and maintain consistent evaluation criteria across all workloads.

### Challenge: Review Fatigue

**Solution**: Implement risk-based review scheduling where high-performing workloads are reviewed less frequently. Use automation to reduce manual effort and focus human attention on high-value activities.

### Challenge: Tracking Implementation Progress

**Solution**: Create optimization opportunity tracking systems with status updates and progress monitoring. Implement automated reporting and dashboard visualization for stakeholder communication.

### Challenge: Measuring Review Effectiveness

**Solution**: Track key metrics such as optimization implementation rates, actual vs. estimated savings, and workload score improvements over time. Use this data to continuously improve the review process.

## Related Resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/cost_evaluate_new_services_review_analyze.html">AWS Well-Architected Framework - Review and analyze this workload regularly</a></li>
    <li><a href="https://docs.aws.amazon.com/cost-management/latest/userguide/ce-what-is.html">AWS Cost Explorer User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html">Amazon CloudWatch User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/config/latest/developerguide/WhatIsConfig.html">AWS Config Developer Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/userguide/intro.html">AWS Well-Architected Tool User Guide</a></li>
    <li><a href="https://aws.amazon.com/premiumsupport/technology/trusted-advisor/">AWS Trusted Advisor</a></li>
    <li><a href="https://docs.aws.amazon.com/systems-manager/latest/userguide/what-is-systems-manager.html">AWS Systems Manager User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/quicksight/latest/user/welcome.html">Amazon QuickSight User Guide</a></li>
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
