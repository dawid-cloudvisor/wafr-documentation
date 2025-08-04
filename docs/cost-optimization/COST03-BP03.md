---
title: COST03-BP03 - Establish organization metrics
layout: default
parent: COST03 - How do you monitor usage and cost?
grand_parent: Cost Optimization
nav_order: 3
---

<div class="pillar-header">
  <h1>COST03-BP03: Establish organization metrics</h1>
  <p>Define and implement metrics that provide meaningful insights into your organization's cloud cost performance. Well-designed metrics enable data-driven decision-making, support accountability, and help track progress toward cost optimization goals.</p>
</div>

## Implementation guidance

Organization metrics provide the quantitative foundation for cost management and optimization decisions. These metrics should align with business objectives, be easily understood by stakeholders, and enable actionable insights that drive cost optimization activities.

### Metric Design Principles

**Business Relevance**: Metrics should directly relate to business outcomes and objectives, enabling stakeholders to understand the business impact of cost decisions.

**Actionability**: Each metric should enable specific actions or decisions that can improve cost performance or business outcomes.

**Measurability**: Metrics must be quantifiable and consistently measurable over time to enable trend analysis and performance tracking.

**Comparability**: Design metrics that enable meaningful comparisons across time periods, business units, projects, or industry benchmarks.

### Metric Categories

**Financial Metrics**: Direct cost measurements including total spend, cost trends, budget performance, and unit economics.

**Efficiency Metrics**: Measurements of resource utilization, waste, and cost-effectiveness that indicate optimization opportunities.

**Business Metrics**: Metrics that relate cloud costs to business value, such as cost per customer, cost per transaction, or revenue efficiency.

**Operational Metrics**: Measurements of cost management processes, governance effectiveness, and optimization program performance.

## AWS Services to Consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Cost Explorer</h4>
    <p>Create custom metrics and reports using Cost Explorer's analysis capabilities. Use saved reports to track key metrics over time.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon CloudWatch</h4>
    <p>Create custom metrics that combine cost data with operational metrics. Use CloudWatch dashboards to visualize organization metrics.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Cost and Usage Report (CUR)</h4>
    <p>Use detailed cost data to calculate complex organization metrics. Combine CUR data with business data for comprehensive metrics.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon QuickSight</h4>
    <p>Create interactive dashboards and visualizations for organization metrics. Enable self-service analytics for different stakeholder groups.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Lambda</h4>
    <p>Implement automated metric calculation and reporting. Use Lambda to combine data from multiple sources for comprehensive metrics.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon DynamoDB</h4>
    <p>Store historical metric data and business context information. Use DynamoDB for fast access to metric calculations and trends.</p>
  </div>
</div>

## Implementation Steps

### 1. Define Metric Requirements
- Identify stakeholder needs for cost visibility and accountability
- Align metrics with business objectives and decision-making processes
- Define metric calculation methods and data sources
- Establish baseline values and target performance levels

### 2. Design Metric Framework
- Create hierarchical metric structure from executive to operational levels
- Define metric relationships and dependencies
- Establish metric calculation frequencies and reporting schedules
- Design metric validation and quality assurance processes

### 3. Implement Data Collection
- Set up automated data collection from AWS cost management tools
- Integrate business data sources for comprehensive metrics
- Implement data validation and quality checks
- Create data processing pipelines for metric calculations

### 4. Create Reporting and Dashboards
- Build executive dashboards for high-level metrics
- Create operational dashboards for detailed analysis
- Implement automated reporting and distribution
- Set up alerting for metric thresholds and anomalies

### 5. Establish Governance
- Define metric ownership and accountability
- Create processes for metric review and validation
- Implement metric change management procedures
- Establish regular metric review and optimization cycles

### 6. Enable Continuous Improvement
- Monitor metric usage and effectiveness
- Gather feedback from stakeholders on metric value
- Refine metrics based on business changes and lessons learned
- Expand metric coverage to new areas and use cases

## Core Organization Metrics

### Financial Performance Metrics

**Total Cloud Spend**: Overall cloud costs across all services and accounts
```python
def calculate_total_cloud_spend(start_date, end_date):
    ce_client = boto3.client('ce')
    
    response = ce_client.get_cost_and_usage(
        TimePeriod={'Start': start_date, 'End': end_date},
        Granularity='MONTHLY',
        Metrics=['BlendedCost']
    )
    
    total_spend = sum(
        float(result['Total']['BlendedCost']['Amount'])
        for result in response['ResultsByTime']
    )
    
    return total_spend
```

**Cost Growth Rate**: Month-over-month and year-over-year cost change percentages
```python
def calculate_cost_growth_rate(current_period, previous_period):
    current_cost = calculate_total_cloud_spend(
        current_period['start'], current_period['end']
    )
    previous_cost = calculate_total_cloud_spend(
        previous_period['start'], previous_period['end']
    )
    
    if previous_cost > 0:
        growth_rate = ((current_cost - previous_cost) / previous_cost) * 100
    else:
        growth_rate = 0
    
    return {
        'current_cost': current_cost,
        'previous_cost': previous_cost,
        'growth_rate': growth_rate
    }
```

**Budget Variance**: Difference between actual and budgeted costs
```python
def calculate_budget_variance():
    budgets_client = boto3.client('budgets')
    account_id = boto3.client('sts').get_caller_identity()['Account']
    
    budgets = budgets_client.describe_budgets(AccountId=account_id)
    
    variances = []
    for budget in budgets['Budgets']:
        budget_name = budget['BudgetName']
        budget_limit = float(budget['BudgetLimit']['Amount'])
        
        # Get actual spend
        actual_spend = budgets_client.describe_budget_performance_history(
            AccountId=account_id,
            BudgetName=budget_name
        )
        
        if actual_spend['BudgetPerformanceHistory']:
            latest_actual = float(
                actual_spend['BudgetPerformanceHistory'][-1]['CostFilters']['ActualCost']
            )
            variance = ((latest_actual - budget_limit) / budget_limit) * 100
            
            variances.append({
                'budget_name': budget_name,
                'budget_limit': budget_limit,
                'actual_spend': latest_actual,
                'variance_percentage': variance
            })
    
    return variances
```

### Efficiency Metrics

**Cost per Business Unit**: Allocated costs for different organizational units
```python
def calculate_cost_per_business_unit(start_date, end_date):
    ce_client = boto3.client('ce')
    
    response = ce_client.get_cost_and_usage(
        TimePeriod={'Start': start_date, 'End': end_date},
        Granularity='MONTHLY',
        Metrics=['BlendedCost'],
        GroupBy=[{'Type': 'TAG', 'Key': 'BusinessUnit'}]
    )
    
    bu_costs = {}
    for result in response['ResultsByTime']:
        for group in result['Groups']:
            bu_name = group['Keys'][0] if group['Keys'][0] else 'Unallocated'
            cost = float(group['Metrics']['BlendedCost']['Amount'])
            
            if bu_name not in bu_costs:
                bu_costs[bu_name] = 0
            bu_costs[bu_name] += cost
    
    return bu_costs
```

**Resource Utilization Rate**: Percentage of provisioned resources actually used
```python
def calculate_resource_utilization():
    cloudwatch = boto3.client('cloudwatch')
    ec2 = boto3.client('ec2')
    
    # Get all running instances
    instances = ec2.describe_instances(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
    )
    
    utilization_data = []
    
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            
            # Get CPU utilization
            cpu_metrics = cloudwatch.get_metric_statistics(
                Namespace='AWS/EC2',
                MetricName='CPUUtilization',
                Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
                StartTime=datetime.now() - timedelta(days=7),
                EndTime=datetime.now(),
                Period=3600,
                Statistics=['Average']
            )
            
            if cpu_metrics['Datapoints']:
                avg_cpu = sum(dp['Average'] for dp in cpu_metrics['Datapoints']) / len(cpu_metrics['Datapoints'])
                
                utilization_data.append({
                    'instance_id': instance_id,
                    'instance_type': instance['InstanceType'],
                    'avg_cpu_utilization': avg_cpu
                })
    
    # Calculate overall utilization rate
    if utilization_data:
        overall_utilization = sum(item['avg_cpu_utilization'] for item in utilization_data) / len(utilization_data)
    else:
        overall_utilization = 0
    
    return {
        'overall_utilization': overall_utilization,
        'instance_details': utilization_data,
        'underutilized_instances': [
            item for item in utilization_data 
            if item['avg_cpu_utilization'] < 20
        ]
    }
```

**Waste Metrics**: Costs associated with unused or underutilized resources
```python
def calculate_waste_metrics():
    waste_categories = {
        'idle_instances': calculate_idle_instance_costs(),
        'unused_storage': calculate_unused_storage_costs(),
        'unattached_volumes': calculate_unattached_volume_costs(),
        'unused_load_balancers': calculate_unused_lb_costs()
    }
    
    total_waste = sum(waste_categories.values())
    
    return {
        'total_waste': total_waste,
        'waste_breakdown': waste_categories,
        'waste_percentage': (total_waste / calculate_total_cloud_spend()) * 100
    }

def calculate_idle_instance_costs():
    # Implementation to identify and cost idle instances
    utilization_data = calculate_resource_utilization()
    idle_instances = [
        instance for instance in utilization_data['instance_details']
        if instance['avg_cpu_utilization'] < 5
    ]
    
    # Calculate costs for idle instances
    idle_cost = 0
    for instance in idle_instances:
        # Get instance pricing (simplified)
        instance_cost = get_instance_hourly_cost(instance['instance_type'])
        idle_cost += instance_cost * 24 * 30  # Monthly cost
    
    return idle_cost
```

### Business Value Metrics

**Cost per Customer**: Allocated cloud costs per customer or user
```python
def calculate_cost_per_customer(start_date, end_date):
    # Get total cloud costs
    total_cost = calculate_total_cloud_spend(start_date, end_date)
    
    # Get customer count from business system
    customer_count = get_active_customer_count(start_date, end_date)
    
    if customer_count > 0:
        cost_per_customer = total_cost / customer_count
    else:
        cost_per_customer = 0
    
    return {
        'total_cost': total_cost,
        'customer_count': customer_count,
        'cost_per_customer': cost_per_customer
    }

def get_active_customer_count(start_date, end_date):
    # This would integrate with your business systems
    # Placeholder implementation
    return 10000  # Example customer count
```

**Revenue Efficiency**: Cloud costs as percentage of revenue
```python
def calculate_revenue_efficiency(start_date, end_date):
    total_cost = calculate_total_cloud_spend(start_date, end_date)
    total_revenue = get_revenue_for_period(start_date, end_date)
    
    if total_revenue > 0:
        cost_percentage = (total_cost / total_revenue) * 100
    else:
        cost_percentage = 0
    
    return {
        'total_cost': total_cost,
        'total_revenue': total_revenue,
        'cost_as_percentage_of_revenue': cost_percentage
    }
```

**Cost per Transaction**: Unit cost for business transactions
```python
def calculate_cost_per_transaction(start_date, end_date):
    total_cost = calculate_total_cloud_spend(start_date, end_date)
    transaction_count = get_transaction_count(start_date, end_date)
    
    if transaction_count > 0:
        cost_per_transaction = total_cost / transaction_count
    else:
        cost_per_transaction = 0
    
    return {
        'total_cost': total_cost,
        'transaction_count': transaction_count,
        'cost_per_transaction': cost_per_transaction
    }
```

## Metric Dashboard Implementation

### Executive Dashboard
```python
def create_executive_dashboard():
    """Create high-level metrics dashboard for executives"""
    
    # Calculate key metrics
    current_month = datetime.now().replace(day=1)
    previous_month = (current_month - timedelta(days=1)).replace(day=1)
    
    metrics = {
        'total_spend': calculate_total_cloud_spend(
            current_month.strftime('%Y-%m-%d'),
            datetime.now().strftime('%Y-%m-%d')
        ),
        'growth_rate': calculate_cost_growth_rate(
            {'start': current_month.strftime('%Y-%m-%d'), 'end': datetime.now().strftime('%Y-%m-%d')},
            {'start': previous_month.strftime('%Y-%m-%d'), 'end': current_month.strftime('%Y-%m-%d')}
        ),
        'budget_variance': calculate_budget_variance(),
        'cost_per_customer': calculate_cost_per_customer(
            current_month.strftime('%Y-%m-%d'),
            datetime.now().strftime('%Y-%m-%d')
        ),
        'revenue_efficiency': calculate_revenue_efficiency(
            current_month.strftime('%Y-%m-%d'),
            datetime.now().strftime('%Y-%m-%d')
        )
    }
    
    # Create dashboard data structure
    dashboard = {
        'title': 'Executive Cost Dashboard',
        'generated_at': datetime.now().isoformat(),
        'metrics': metrics,
        'alerts': generate_executive_alerts(metrics),
        'trends': calculate_metric_trends(metrics)
    }
    
    return dashboard

def generate_executive_alerts(metrics):
    """Generate alerts for executive attention"""
    alerts = []
    
    # Growth rate alert
    if metrics['growth_rate']['growth_rate'] > 20:
        alerts.append({
            'type': 'warning',
            'message': f"Cost growth rate of {metrics['growth_rate']['growth_rate']:.1f}% exceeds threshold",
            'action': 'Review cost drivers and optimization opportunities'
        })
    
    # Budget variance alert
    for variance in metrics['budget_variance']:
        if variance['variance_percentage'] > 10:
            alerts.append({
                'type': 'critical',
                'message': f"Budget {variance['budget_name']} is {variance['variance_percentage']:.1f}% over budget",
                'action': 'Immediate cost control measures required'
            })
    
    return alerts
```

### Operational Dashboard
```python
def create_operational_dashboard():
    """Create detailed metrics dashboard for operations teams"""
    
    metrics = {
        'utilization': calculate_resource_utilization(),
        'waste': calculate_waste_metrics(),
        'cost_by_service': calculate_cost_by_service(),
        'cost_by_environment': calculate_cost_by_environment(),
        'optimization_opportunities': identify_optimization_opportunities()
    }
    
    dashboard = {
        'title': 'Operational Cost Dashboard',
        'generated_at': datetime.now().isoformat(),
        'metrics': metrics,
        'recommendations': generate_optimization_recommendations(metrics)
    }
    
    return dashboard

def identify_optimization_opportunities():
    """Identify specific cost optimization opportunities"""
    opportunities = []
    
    # Right-sizing opportunities
    utilization = calculate_resource_utilization()
    for instance in utilization['underutilized_instances']:
        opportunities.append({
            'type': 'rightsizing',
            'resource': instance['instance_id'],
            'current_type': instance['instance_type'],
            'recommended_action': 'Downsize instance',
            'estimated_savings': calculate_rightsizing_savings(instance)
        })
    
    # Reserved Instance opportunities
    ri_opportunities = calculate_ri_opportunities()
    opportunities.extend(ri_opportunities)
    
    return opportunities
```

## Metric Automation and Alerting

### Automated Metric Collection
```python
def setup_automated_metrics():
    """Set up automated metric collection and processing"""
    
    # Lambda function for daily metric calculation
    lambda_code = '''
import boto3
import json
from datetime import datetime, timedelta

def lambda_handler(event, context):
    """Calculate and store daily metrics"""
    
    # Calculate key metrics
    metrics = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'total_spend': calculate_daily_spend(),
        'utilization': calculate_daily_utilization(),
        'waste': calculate_daily_waste()
    }
    
    # Store metrics in DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('OrganizationMetrics')
    
    table.put_item(Item=metrics)
    
    # Check for alerts
    alerts = check_metric_thresholds(metrics)
    if alerts:
        send_metric_alerts(alerts)
    
    return {'statusCode': 200, 'body': json.dumps(metrics)}
'''
    
    # Create Lambda function
    lambda_client = boto3.client('lambda')
    
    try:
        lambda_client.create_function(
            FunctionName='DailyMetricsCalculation',
            Runtime='python3.9',
            Role='arn:aws:iam::ACCOUNT:role/MetricsCalculationRole',
            Handler='lambda_function.lambda_handler',
            Code={'ZipFile': lambda_code.encode()},
            Description='Calculate daily organization metrics'
        )
        
        # Set up CloudWatch Events rule for daily execution
        events_client = boto3.client('events')
        
        events_client.put_rule(
            Name='DailyMetricsSchedule',
            ScheduleExpression='cron(0 8 * * ? *)',  # Daily at 8 AM UTC
            Description='Trigger daily metrics calculation'
        )
        
        events_client.put_targets(
            Rule='DailyMetricsSchedule',
            Targets=[
                {
                    'Id': '1',
                    'Arn': f'arn:aws:lambda:REGION:ACCOUNT:function:DailyMetricsCalculation'
                }
            ]
        )
        
        print("Set up automated metrics collection")
        
    except Exception as e:
        print(f"Error setting up automation: {str(e)}")
```

### Metric Alerting System
```python
def setup_metric_alerting():
    """Set up alerting for metric thresholds"""
    
    # CloudWatch alarms for key metrics
    cloudwatch = boto3.client('cloudwatch')
    
    # Total spend alarm
    cloudwatch.put_metric_alarm(
        AlarmName='HighCloudSpend',
        ComparisonOperator='GreaterThanThreshold',
        EvaluationPeriods=1,
        MetricName='TotalCloudSpend',
        Namespace='Organization/Metrics',
        Period=86400,  # Daily
        Statistic='Sum',
        Threshold=100000.0,  # $100k threshold
        ActionsEnabled=True,
        AlarmActions=[
            'arn:aws:sns:REGION:ACCOUNT:cost-alerts'
        ],
        AlarmDescription='Alert when daily cloud spend exceeds threshold'
    )
    
    # Cost growth rate alarm
    cloudwatch.put_metric_alarm(
        AlarmName='HighCostGrowthRate',
        ComparisonOperator='GreaterThanThreshold',
        EvaluationPeriods=1,
        MetricName='CostGrowthRate',
        Namespace='Organization/Metrics',
        Period=2592000,  # Monthly
        Statistic='Average',
        Threshold=20.0,  # 20% growth threshold
        ActionsEnabled=True,
        AlarmActions=[
            'arn:aws:sns:REGION:ACCOUNT:cost-alerts'
        ],
        AlarmDescription='Alert when cost growth rate exceeds 20%'
    )
```

## Common Challenges and Solutions

### Challenge: Metric Overload

**Solution**: Focus on a core set of actionable metrics. Create role-based metric views. Use exception-based reporting. Implement metric hierarchies from summary to detail.

### Challenge: Data Quality Issues

**Solution**: Implement comprehensive data validation. Use multiple data sources for verification. Create data quality monitoring and alerting. Establish data governance processes.

### Challenge: Lack of Business Context

**Solution**: Integrate business data with cost metrics. Create metrics that relate to business outcomes. Involve business stakeholders in metric design. Provide business context in metric reporting.

### Challenge: Metric Relevance Over Time

**Solution**: Regular review and refinement of metrics. Create feedback loops from metric users. Monitor metric usage and effectiveness. Evolve metrics based on business changes.

### Challenge: Complex Metric Calculations

**Solution**: Use automated calculation and validation. Document metric definitions and calculations clearly. Implement version control for metric definitions. Provide training on metric interpretation.

## Related Resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/cost_monitor_usage_metrics.html">AWS Well-Architected Framework - Establish organization metrics</a></li>
    <li><a href="https://docs.aws.amazon.com/cost-management/latest/userguide/ce-what-is.html">AWS Cost Explorer User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html">Amazon CloudWatch User Guide</a></li>
    <li><a href="https://aws.amazon.com/quicksight/">Amazon QuickSight</a></li>
    <li><a href="https://aws.amazon.com/blogs/aws-cost-management/">AWS Cost Management Blog</a></li>
    <li><a href="https://docs.aws.amazon.com/cur/latest/userguide/what-is-cur.html">AWS Cost and Usage Report User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/lambda/latest/dg/welcome.html">AWS Lambda Developer Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html">Amazon DynamoDB Developer Guide</a></li>
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
