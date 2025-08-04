---
title: COST03-BP06 - Allocate costs based on workload metrics
layout: default
parent: COST03 - How do you monitor usage and cost?
grand_parent: Cost Optimization
nav_order: 6
---

<div class="pillar-header">
  <h1>COST03-BP06: Allocate costs based on workload metrics</h1>
  <p>Implement cost allocation methods that use workload-specific metrics to distribute shared costs fairly and accurately. Workload-based allocation provides more precise cost attribution and enables better understanding of the true cost of delivering business value.</p>
</div>

## Implementation guidance

Workload-based cost allocation goes beyond simple tag-based attribution to use actual workload metrics such as resource utilization, transaction volumes, and business outcomes. This approach provides more accurate cost allocation and better insights into the relationship between infrastructure costs and business value delivery.

### Workload Metrics Principles

**Business Relevance**: Use metrics that directly relate to business value delivery, such as transactions processed, users served, or revenue generated.

**Resource Correlation**: Select metrics that correlate strongly with actual resource consumption and infrastructure costs.

**Measurability**: Ensure metrics can be consistently measured and tracked over time with appropriate granularity.

**Fairness**: Design allocation methods that fairly distribute costs based on actual usage and business benefit received.

### Types of Workload Metrics

**Usage Metrics**: Direct measurements of resource utilization such as CPU hours, storage consumed, network bandwidth, and API calls.

**Business Metrics**: Business-relevant measurements such as transactions processed, active users, revenue generated, or orders fulfilled.

**Performance Metrics**: Measurements related to application performance such as response times, throughput, and availability.

**Value Metrics**: Measurements that relate to business value delivery such as customer satisfaction, conversion rates, or business outcomes achieved.

## AWS Services to Consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon CloudWatch</h4>
    <p>Collect and analyze workload metrics for cost allocation. Use CloudWatch metrics to track resource utilization and application performance.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS X-Ray</h4>
    <p>Trace application requests and analyze performance metrics. Use X-Ray data to understand workload behavior and resource consumption patterns.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Cost Explorer</h4>
    <p>Analyze costs alongside workload metrics. Use Cost Explorer APIs to integrate cost data with workload performance data.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon Kinesis</h4>
    <p>Stream workload metrics for real-time cost allocation. Use Kinesis to process high-volume metric streams for dynamic cost attribution.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Lambda</h4>
    <p>Implement custom cost allocation algorithms. Use Lambda to process workload metrics and calculate dynamic cost allocations.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon DynamoDB</h4>
    <p>Store workload metrics and allocation calculations. Use DynamoDB for fast access to metric data and allocation results.</p>
  </div>
</div>

## Implementation Steps

### 1. Identify Workload Metrics
- Analyze workloads to identify relevant metrics for cost allocation
- Map metrics to business value and resource consumption
- Define metric collection methods and frequencies
- Establish baseline measurements and historical data

### 2. Design Allocation Algorithms
- Create algorithms that correlate metrics with costs
- Design fair allocation methods for shared resources
- Implement dynamic allocation based on changing workload patterns
- Create validation and reconciliation procedures

### 3. Implement Metric Collection
- Set up automated collection of workload metrics
- Integrate with existing monitoring and observability tools
- Implement data validation and quality assurance
- Create metric storage and processing infrastructure

### 4. Build Allocation Engine
- Develop cost allocation calculation engine
- Implement allocation algorithms and business rules
- Create allocation result storage and tracking
- Set up allocation validation and audit capabilities

### 5. Create Allocation Reporting
- Build reports showing allocated costs by workload
- Create dashboards for allocation transparency
- Implement allocation reconciliation and adjustment processes
- Set up automated allocation reporting and distribution

### 6. Monitor and Optimize
- Track allocation accuracy and fairness
- Gather feedback from stakeholders on allocation methods
- Refine allocation algorithms based on changing workload patterns
- Continuously improve allocation processes and automation

## Workload Metric Collection

### Application Performance Metrics
```python
import boto3
import json
from datetime import datetime, timedelta

class WorkloadMetricsCollector:
    def __init__(self):
        self.cloudwatch = boto3.client('cloudwatch')
        self.xray = boto3.client('xray')
        self.dynamodb = boto3.resource('dynamodb')
        self.metrics_table = self.dynamodb.Table('WorkloadMetrics')
    
    def collect_application_metrics(self, application_name, start_time, end_time):
        """Collect comprehensive application metrics for cost allocation"""
        
        metrics = {}
        
        # Collect CloudWatch metrics
        cw_metrics = self.collect_cloudwatch_metrics(application_name, start_time, end_time)
        metrics.update(cw_metrics)
        
        # Collect X-Ray metrics
        xray_metrics = self.collect_xray_metrics(application_name, start_time, end_time)
        metrics.update(xray_metrics)
        
        # Collect custom business metrics
        business_metrics = self.collect_business_metrics(application_name, start_time, end_time)
        metrics.update(business_metrics)
        
        # Store metrics for allocation processing
        self.store_workload_metrics(application_name, metrics, start_time, end_time)
        
        return metrics
    
    def collect_cloudwatch_metrics(self, application_name, start_time, end_time):
        """Collect CloudWatch metrics for workload analysis"""
        
        metrics = {}
        
        # Define metrics to collect
        metric_queries = [
            {
                'name': 'cpu_utilization',
                'namespace': 'AWS/EC2',
                'metric_name': 'CPUUtilization',
                'dimensions': [{'Name': 'Application', 'Value': application_name}]
            },
            {
                'name': 'request_count',
                'namespace': 'AWS/ApplicationELB',
                'metric_name': 'RequestCount',
                'dimensions': [{'Name': 'LoadBalancer', 'Value': f'{application_name}-alb'}]
            },
            {
                'name': 'response_time',
                'namespace': 'AWS/ApplicationELB',
                'metric_name': 'TargetResponseTime',
                'dimensions': [{'Name': 'LoadBalancer', 'Value': f'{application_name}-alb'}]
            },
            {
                'name': 'database_connections',
                'namespace': 'AWS/RDS',
                'metric_name': 'DatabaseConnections',
                'dimensions': [{'Name': 'DBInstanceIdentifier', 'Value': f'{application_name}-db'}]
            }
        ]
        
        # Collect each metric
        for query in metric_queries:
            try:
                response = self.cloudwatch.get_metric_statistics(
                    Namespace=query['namespace'],
                    MetricName=query['metric_name'],
                    Dimensions=query['dimensions'],
                    StartTime=start_time,
                    EndTime=end_time,
                    Period=3600,  # 1 hour periods
                    Statistics=['Average', 'Sum', 'Maximum']
                )
                
                if response['Datapoints']:
                    metrics[query['name']] = {
                        'average': sum(dp['Average'] for dp in response['Datapoints']) / len(response['Datapoints']),
                        'total': sum(dp['Sum'] for dp in response['Datapoints']),
                        'peak': max(dp['Maximum'] for dp in response['Datapoints']),
                        'datapoints': len(response['Datapoints'])
                    }
                
            except Exception as e:
                print(f"Error collecting metric {query['name']}: {str(e)}")
        
        return metrics
    
    def collect_xray_metrics(self, application_name, start_time, end_time):
        """Collect X-Ray tracing metrics for detailed workload analysis"""
        
        metrics = {}
        
        try:
            # Get service statistics
            response = self.xray.get_service_graph(
                TimeRangeType='TimeRangeByStartTime',
                StartTime=start_time,
                EndTime=end_time
            )
            
            # Process service statistics
            for service in response['Services']:
                if application_name in service['Name']:
                    service_stats = service.get('SummaryStatistics', {})
                    
                    metrics['xray_request_count'] = service_stats.get('TotalCount', 0)
                    metrics['xray_error_rate'] = service_stats.get('ErrorStatistics', {}).get('ErrorRate', 0)
                    metrics['xray_response_time'] = service_stats.get('ResponseTimeHistogram', {}).get('TotalTime', 0)
                    metrics['xray_fault_rate'] = service_stats.get('FaultStatistics', {}).get('FaultRate', 0)
            
            # Get trace summaries for detailed analysis
            trace_response = self.xray.get_trace_summaries(
                TimeRangeType='TimeRangeByStartTime',
                StartTime=start_time,
                EndTime=end_time,
                FilterExpression=f'service("{application_name}")'
            )
            
            if trace_response['TraceSummaries']:
                response_times = [trace['ResponseTime'] for trace in trace_response['TraceSummaries']]
                metrics['xray_avg_response_time'] = sum(response_times) / len(response_times)
                metrics['xray_trace_count'] = len(trace_response['TraceSummaries'])
        
        except Exception as e:
            print(f"Error collecting X-Ray metrics: {str(e)}")
        
        return metrics
    
    def collect_business_metrics(self, application_name, start_time, end_time):
        """Collect business-specific metrics for value-based allocation"""
        
        # This would integrate with your business systems
        # Example implementation for common business metrics
        
        metrics = {}
        
        try:
            # Example: Get transaction count from application logs
            logs_client = boto3.client('logs')
            
            query = f"""
            fields @timestamp, @message
            | filter @message like /transaction_completed/
            | filter application = "{application_name}"
            | stats count() as transaction_count
            """
            
            response = logs_client.start_query(
                logGroupName=f'/aws/lambda/{application_name}',
                startTime=int(start_time.timestamp()),
                endTime=int(end_time.timestamp()),
                queryString=query
            )
            
            # Wait for query completion and get results
            query_id = response['queryId']
            results = self.wait_for_query_completion(logs_client, query_id)
            
            if results:
                metrics['transaction_count'] = int(results[0][0]['value'])
            
            # Example: Get user count from application database
            # This would connect to your application database
            metrics['active_users'] = self.get_active_user_count(application_name, start_time, end_time)
            
            # Example: Get revenue attribution
            metrics['revenue_attributed'] = self.get_revenue_attribution(application_name, start_time, end_time)
            
        except Exception as e:
            print(f"Error collecting business metrics: {str(e)}")
        
        return metrics
    
    def store_workload_metrics(self, application_name, metrics, start_time, end_time):
        """Store collected metrics for allocation processing"""
        
        try:
            self.metrics_table.put_item(
                Item={
                    'ApplicationName': application_name,
                    'TimeRange': f"{start_time.isoformat()}_{end_time.isoformat()}",
                    'Metrics': metrics,
                    'CollectionTimestamp': datetime.now().isoformat(),
                    'TTL': int((datetime.now() + timedelta(days=90)).timestamp())
                }
            )
            
        except Exception as e:
            print(f"Error storing workload metrics: {str(e)}")
```

### Cost Allocation Engine
```python
class WorkloadCostAllocator:
    def __init__(self):
        self.ce_client = boto3.client('ce')
        self.dynamodb = boto3.resource('dynamodb')
        self.metrics_table = self.dynamodb.Table('WorkloadMetrics')
        self.allocation_table = self.dynamodb.Table('CostAllocations')
    
    def allocate_costs_by_workload_metrics(self, start_date, end_date):
        """Allocate costs based on workload metrics"""
        
        # Get cost data
        cost_data = self.get_cost_data(start_date, end_date)
        
        # Get workload metrics
        workload_metrics = self.get_workload_metrics(start_date, end_date)
        
        # Calculate allocations
        allocations = self.calculate_metric_based_allocations(cost_data, workload_metrics)
        
        # Store allocation results
        self.store_allocation_results(allocations, start_date, end_date)
        
        return allocations
    
    def calculate_metric_based_allocations(self, cost_data, workload_metrics):
        """Calculate cost allocations based on workload metrics"""
        
        allocations = {}
        
        # Define allocation methods for different cost types
        allocation_methods = {
            'compute_costs': self.allocate_by_cpu_utilization,
            'storage_costs': self.allocate_by_storage_usage,
            'network_costs': self.allocate_by_request_count,
            'database_costs': self.allocate_by_transaction_count,
            'shared_costs': self.allocate_by_business_value
        }
        
        # Process each cost category
        for cost_category, costs in cost_data.items():
            if cost_category in allocation_methods:
                allocation_method = allocation_methods[cost_category]
                category_allocations = allocation_method(costs, workload_metrics)
                allocations[cost_category] = category_allocations
            else:
                # Default allocation method
                allocations[cost_category] = self.allocate_proportionally(costs, workload_metrics)
        
        return allocations
    
    def allocate_by_cpu_utilization(self, costs, workload_metrics):
        """Allocate compute costs based on CPU utilization"""
        
        allocations = {}
        total_cpu_hours = 0
        
        # Calculate total CPU hours across all workloads
        for app_name, metrics in workload_metrics.items():
            cpu_utilization = metrics.get('cpu_utilization', {}).get('average', 0)
            cpu_hours = cpu_utilization * metrics.get('instance_hours', 0)
            total_cpu_hours += cpu_hours
        
        # Allocate costs proportionally
        for app_name, metrics in workload_metrics.items():
            if total_cpu_hours > 0:
                cpu_utilization = metrics.get('cpu_utilization', {}).get('average', 0)
                cpu_hours = cpu_utilization * metrics.get('instance_hours', 0)
                allocation_percentage = cpu_hours / total_cpu_hours
                
                allocations[app_name] = {
                    'allocated_cost': costs['total'] * allocation_percentage,
                    'allocation_basis': 'cpu_utilization',
                    'cpu_hours': cpu_hours,
                    'allocation_percentage': allocation_percentage * 100
                }
        
        return allocations
    
    def allocate_by_request_count(self, costs, workload_metrics):
        """Allocate network costs based on request count"""
        
        allocations = {}
        total_requests = 0
        
        # Calculate total requests across all workloads
        for app_name, metrics in workload_metrics.items():
            requests = metrics.get('request_count', {}).get('total', 0)
            total_requests += requests
        
        # Allocate costs proportionally
        for app_name, metrics in workload_metrics.items():
            if total_requests > 0:
                requests = metrics.get('request_count', {}).get('total', 0)
                allocation_percentage = requests / total_requests
                
                allocations[app_name] = {
                    'allocated_cost': costs['total'] * allocation_percentage,
                    'allocation_basis': 'request_count',
                    'request_count': requests,
                    'allocation_percentage': allocation_percentage * 100
                }
        
        return allocations
    
    def allocate_by_transaction_count(self, costs, workload_metrics):
        """Allocate database costs based on transaction count"""
        
        allocations = {}
        total_transactions = 0
        
        # Calculate total transactions across all workloads
        for app_name, metrics in workload_metrics.items():
            transactions = metrics.get('transaction_count', 0)
            total_transactions += transactions
        
        # Allocate costs proportionally
        for app_name, metrics in workload_metrics.items():
            if total_transactions > 0:
                transactions = metrics.get('transaction_count', 0)
                allocation_percentage = transactions / total_transactions
                
                allocations[app_name] = {
                    'allocated_cost': costs['total'] * allocation_percentage,
                    'allocation_basis': 'transaction_count',
                    'transaction_count': transactions,
                    'allocation_percentage': allocation_percentage * 100
                }
        
        return allocations
    
    def allocate_by_business_value(self, costs, workload_metrics):
        """Allocate shared costs based on business value metrics"""
        
        allocations = {}
        total_business_value = 0
        
        # Calculate total business value across all workloads
        for app_name, metrics in workload_metrics.items():
            # Composite business value score
            revenue = metrics.get('revenue_attributed', 0)
            users = metrics.get('active_users', 0)
            transactions = metrics.get('transaction_count', 0)
            
            # Weighted business value calculation
            business_value = (revenue * 0.5) + (users * 0.3) + (transactions * 0.2)
            total_business_value += business_value
        
        # Allocate costs based on business value
        for app_name, metrics in workload_metrics.items():
            if total_business_value > 0:
                revenue = metrics.get('revenue_attributed', 0)
                users = metrics.get('active_users', 0)
                transactions = metrics.get('transaction_count', 0)
                
                business_value = (revenue * 0.5) + (users * 0.3) + (transactions * 0.2)
                allocation_percentage = business_value / total_business_value
                
                allocations[app_name] = {
                    'allocated_cost': costs['total'] * allocation_percentage,
                    'allocation_basis': 'business_value',
                    'business_value_score': business_value,
                    'allocation_percentage': allocation_percentage * 100,
                    'value_components': {
                        'revenue': revenue,
                        'users': users,
                        'transactions': transactions
                    }
                }
        
        return allocations
    
    def calculate_dynamic_allocation_weights(self, workload_metrics):
        """Calculate dynamic allocation weights based on workload patterns"""
        
        weights = {}
        
        for app_name, metrics in workload_metrics.items():
            # Calculate efficiency metrics
            cpu_efficiency = self.calculate_cpu_efficiency(metrics)
            cost_efficiency = self.calculate_cost_efficiency(metrics)
            business_impact = self.calculate_business_impact(metrics)
            
            # Composite weight calculation
            weight = (cpu_efficiency * 0.3) + (cost_efficiency * 0.4) + (business_impact * 0.3)
            
            weights[app_name] = {
                'composite_weight': weight,
                'cpu_efficiency': cpu_efficiency,
                'cost_efficiency': cost_efficiency,
                'business_impact': business_impact
            }
        
        return weights
    
    def calculate_cpu_efficiency(self, metrics):
        """Calculate CPU efficiency score"""
        
        cpu_utilization = metrics.get('cpu_utilization', {}).get('average', 0)
        
        # Efficiency score based on utilization (optimal range 70-85%)
        if 70 <= cpu_utilization <= 85:
            return 1.0
        elif cpu_utilization < 70:
            return cpu_utilization / 70
        else:
            return max(0.5, 1.0 - ((cpu_utilization - 85) / 15))
    
    def calculate_cost_efficiency(self, metrics):
        """Calculate cost efficiency score"""
        
        cost_per_transaction = metrics.get('cost_per_transaction', 0)
        revenue_per_transaction = metrics.get('revenue_per_transaction', 0)
        
        if revenue_per_transaction > 0 and cost_per_transaction > 0:
            return min(1.0, revenue_per_transaction / cost_per_transaction / 10)
        else:
            return 0.5  # Default score for missing data
    
    def calculate_business_impact(self, metrics):
        """Calculate business impact score"""
        
        active_users = metrics.get('active_users', 0)
        transaction_count = metrics.get('transaction_count', 0)
        revenue_attributed = metrics.get('revenue_attributed', 0)
        
        # Normalize and combine business metrics
        user_score = min(1.0, active_users / 10000)  # Normalize to 10k users
        transaction_score = min(1.0, transaction_count / 100000)  # Normalize to 100k transactions
        revenue_score = min(1.0, revenue_attributed / 1000000)  # Normalize to $1M revenue
        
        return (user_score + transaction_score + revenue_score) / 3
```

### Allocation Reporting and Validation
```python
def create_allocation_reports(allocations):
    """Create comprehensive allocation reports"""
    
    reports = {
        'allocation_summary': create_allocation_summary(allocations),
        'workload_cost_breakdown': create_workload_breakdown(allocations),
        'allocation_fairness_analysis': analyze_allocation_fairness(allocations),
        'metric_correlation_analysis': analyze_metric_correlations(allocations)
    }
    
    return reports

def create_allocation_summary(allocations):
    """Create high-level allocation summary"""
    
    summary = {
        'total_allocated_cost': 0,
        'allocation_methods': {},
        'workload_summary': {}
    }
    
    # Aggregate across all cost categories
    for category, category_allocations in allocations.items():
        category_total = 0
        
        for workload, allocation in category_allocations.items():
            allocated_cost = allocation['allocated_cost']
            category_total += allocated_cost
            summary['total_allocated_cost'] += allocated_cost
            
            # Track allocation methods
            method = allocation['allocation_basis']
            if method not in summary['allocation_methods']:
                summary['allocation_methods'][method] = 0
            summary['allocation_methods'][method] += allocated_cost
            
            # Aggregate by workload
            if workload not in summary['workload_summary']:
                summary['workload_summary'][workload] = {
                    'total_cost': 0,
                    'cost_categories': {}
                }
            
            summary['workload_summary'][workload]['total_cost'] += allocated_cost
            summary['workload_summary'][workload]['cost_categories'][category] = allocated_cost
    
    return summary

def analyze_allocation_fairness(allocations):
    """Analyze fairness of cost allocations"""
    
    fairness_analysis = {
        'allocation_distribution': {},
        'concentration_metrics': {},
        'fairness_score': 0
    }
    
    # Calculate allocation distribution
    total_cost = 0
    workload_costs = {}
    
    for category, category_allocations in allocations.items():
        for workload, allocation in category_allocations.items():
            cost = allocation['allocated_cost']
            total_cost += cost
            
            if workload not in workload_costs:
                workload_costs[workload] = 0
            workload_costs[workload] += cost
    
    # Calculate distribution metrics
    if total_cost > 0:
        cost_percentages = {
            workload: (cost / total_cost) * 100 
            for workload, cost in workload_costs.items()
        }
        
        fairness_analysis['allocation_distribution'] = cost_percentages
        
        # Calculate concentration metrics
        sorted_percentages = sorted(cost_percentages.values(), reverse=True)
        
        # Gini coefficient for inequality measurement
        gini = calculate_gini_coefficient(sorted_percentages)
        fairness_analysis['concentration_metrics']['gini_coefficient'] = gini
        
        # Top workload concentration
        top_3_concentration = sum(sorted_percentages[:3])
        fairness_analysis['concentration_metrics']['top_3_concentration'] = top_3_concentration
        
        # Fairness score (inverse of Gini coefficient)
        fairness_analysis['fairness_score'] = 1 - gini
    
    return fairness_analysis

def validate_allocation_accuracy(allocations, actual_costs):
    """Validate allocation accuracy against actual costs"""
    
    validation_results = {
        'total_allocated': 0,
        'total_actual': 0,
        'allocation_accuracy': 0,
        'category_variances': {},
        'validation_errors': []
    }
    
    # Calculate totals
    for category, category_allocations in allocations.items():
        allocated_total = sum(
            allocation['allocated_cost'] 
            for allocation in category_allocations.values()
        )
        validation_results['total_allocated'] += allocated_total
        
        # Compare with actual costs
        if category in actual_costs:
            actual_total = actual_costs[category]
            variance = abs(allocated_total - actual_total)
            variance_percentage = (variance / actual_total) * 100 if actual_total > 0 else 0
            
            validation_results['category_variances'][category] = {
                'allocated': allocated_total,
                'actual': actual_total,
                'variance': variance,
                'variance_percentage': variance_percentage
            }
            
            if variance_percentage > 5:  # 5% threshold
                validation_results['validation_errors'].append({
                    'category': category,
                    'error_type': 'high_variance',
                    'variance_percentage': variance_percentage
                })
    
    # Calculate overall accuracy
    validation_results['total_actual'] = sum(actual_costs.values())
    if validation_results['total_actual'] > 0:
        total_variance = abs(validation_results['total_allocated'] - validation_results['total_actual'])
        validation_results['allocation_accuracy'] = (
            1 - (total_variance / validation_results['total_actual'])
        ) * 100
    
    return validation_results
```

## Common Challenges and Solutions

### Challenge: Metric Data Quality and Availability

**Solution**: Implement comprehensive data validation and quality checks. Use multiple data sources for cross-validation. Create default allocation methods for missing metrics. Establish data governance processes for metric collection.

### Challenge: Complex Allocation Algorithm Design

**Solution**: Start with simple allocation methods and gradually add complexity. Use industry best practices and benchmarks. Involve stakeholders in algorithm design and validation. Implement multiple allocation methods for comparison.

### Challenge: Stakeholder Acceptance of Allocations

**Solution**: Involve stakeholders in allocation method design. Provide transparency in allocation calculations. Create clear documentation and examples. Implement feedback mechanisms and regular reviews.

### Challenge: Dynamic Workload Patterns

**Solution**: Use time-weighted allocation methods. Implement dynamic allocation based on changing patterns. Create allocation methods that adapt to workload seasonality. Use predictive analytics for allocation forecasting.

### Challenge: Performance Impact of Complex Allocations

**Solution**: Optimize allocation algorithms for performance. Use appropriate caching and storage strategies. Implement parallel processing where possible. Consider using managed analytics services for complex calculations.

## Related Resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/cost_monitor_usage_workload_metrics.html">AWS Well-Architected Framework - Allocate costs based on workload metrics</a></li>
    <li><a href="https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html">Amazon CloudWatch User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/xray/latest/devguide/aws-xray.html">AWS X-Ray Developer Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/cost-management/latest/userguide/ce-what-is.html">AWS Cost Explorer User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/kinesis/latest/dev/introduction.html">Amazon Kinesis Developer Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/lambda/latest/dg/welcome.html">AWS Lambda Developer Guide</a></li>
    <li><a href="https://aws.amazon.com/blogs/aws-cost-management/">AWS Cost Management Blog</a></li>
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
