---
title: COST06-BP02 - Select resource type, size, and number based on data
layout: default
parent: COST06 - How do you meet cost targets when you select resource type, size and number?
grand_parent: Cost Optimization
nav_order: 2
---

<div class="pillar-header">
  <h1>COST06-BP02: Select resource type, size, and number based on data</h1>
  <p>Use actual usage data, performance metrics, and workload characteristics to make informed decisions about resource type, size, and number rather than relying on assumptions or over-provisioning. Data-driven resource selection ensures optimal cost-performance balance.</p>
</div>

## Implementation guidance

Data-driven resource selection involves collecting and analyzing actual usage patterns, performance metrics, and workload characteristics to make informed decisions about resource configurations. This approach eliminates guesswork and over-provisioning while ensuring performance requirements are met within cost targets.

### Data Collection Strategy

**Usage Metrics**: Collect comprehensive usage data including CPU, memory, storage, and network utilization across different time periods and load conditions.

**Performance Metrics**: Monitor application performance metrics such as response time, throughput, and error rates to understand resource requirements.

**Business Metrics**: Correlate technical metrics with business metrics to understand the relationship between resource usage and business outcomes.

**Cost Metrics**: Track costs at the resource level to understand the cost implications of different resource configurations.

### Analysis Framework

**Baseline Analysis**: Establish baseline resource requirements based on historical data and performance benchmarks.

**Pattern Recognition**: Identify usage patterns, peak loads, and seasonal variations to inform resource sizing decisions.

**Correlation Analysis**: Analyze relationships between different metrics to understand resource dependencies and optimization opportunities.

**Predictive Analysis**: Use historical data to predict future resource requirements and plan for growth.

## AWS Services to Consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Compute Optimizer</h4>
    <p>Get rightsizing recommendations based on actual usage data. Use Compute Optimizer to identify optimal instance types and sizes for your workloads.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon CloudWatch</h4>
    <p>Collect detailed metrics on resource utilization and application performance. Use CloudWatch data to make informed resource selection decisions.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS X-Ray</h4>
    <p>Analyze application performance and identify resource bottlenecks. Use X-Ray data to understand resource requirements for optimal performance.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Cost Explorer</h4>
    <p>Analyze cost patterns and correlate them with resource usage. Use Cost Explorer to understand the cost impact of different resource configurations.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Systems Manager</h4>
    <p>Collect system-level metrics and inventory data. Use Systems Manager to gather comprehensive data about your infrastructure and applications.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon CloudWatch Insights</h4>
    <p>Analyze log data to understand application behavior and resource usage patterns. Use Insights to correlate logs with performance and cost metrics.</p>
  </div>
</div>

## Implementation Steps

### 1. Establish Data Collection
- Set up comprehensive monitoring and metrics collection
- Configure CloudWatch agents and custom metrics
- Implement application performance monitoring
- Create data pipelines for analysis and storage

### 2. Define Analysis Framework
- Establish baseline performance and cost metrics
- Create analysis templates and methodologies
- Define decision criteria and thresholds
- Set up automated analysis and reporting

### 3. Collect Historical Data
- Gather at least 30 days of usage data
- Analyze seasonal patterns and trends
- Identify peak and average usage patterns
- Document workload characteristics and requirements

### 4. Perform Resource Analysis
- Analyze current resource utilization and efficiency
- Identify over-provisioned and under-provisioned resources
- Correlate resource usage with performance metrics
- Calculate cost per unit of work or transaction

### 5. Generate Recommendations
- Use data analysis to generate rightsizing recommendations
- Consider different resource types and configurations
- Evaluate trade-offs between cost and performance
- Prioritize recommendations based on impact and effort

### 6. Implement and Monitor
- Implement resource changes based on data analysis
- Monitor performance and cost impacts
- Validate assumptions and adjust as needed
- Establish ongoing monitoring and optimization processes
## Data-Driven Resource Selection Framework

### Resource Analytics Engine
```python
import boto3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import json
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns

@dataclass
class ResourceMetrics:
    resource_id: str
    resource_type: str
    instance_type: str
    cpu_utilization: List[float]
    memory_utilization: List[float]
    network_utilization: List[float]
    storage_utilization: List[float]
    cost_per_hour: float
    performance_metrics: Dict
    timestamps: List[datetime]

@dataclass
class ResourceRecommendation:
    current_config: str
    recommended_config: str
    confidence_score: float
    potential_savings: float
    performance_impact: str
    implementation_effort: str
    rationale: str

class DataDrivenResourceSelector:
    def __init__(self):
        self.cloudwatch = boto3.client('cloudwatch')
        self.compute_optimizer = boto3.client('compute-optimizer')
        self.ce_client = boto3.client('ce')
        self.ec2 = boto3.client('ec2')
        
        # Analysis parameters
        self.analysis_period_days = 30
        self.confidence_threshold = 0.8
        self.utilization_thresholds = {
            'under_utilized': 30,
            'optimal': 70,
            'over_utilized': 85
        }
    
    def collect_resource_metrics(self, resource_ids: List[str], 
                               resource_type: str = 'EC2') -> List[ResourceMetrics]:
        """Collect comprehensive metrics for resources"""
        
        metrics_list = []
        end_time = datetime.now()
        start_time = end_time - timedelta(days=self.analysis_period_days)
        
        for resource_id in resource_ids:
            try:
                metrics = ResourceMetrics(
                    resource_id=resource_id,
                    resource_type=resource_type,
                    instance_type=self.get_instance_type(resource_id),
                    cpu_utilization=[],
                    memory_utilization=[],
                    network_utilization=[],
                    storage_utilization=[],
                    cost_per_hour=0.0,
                    performance_metrics={},
                    timestamps=[]
                )
                
                # Collect CPU utilization
                cpu_data = self.get_cloudwatch_metrics(
                    resource_id, 'AWS/EC2', 'CPUUtilization', start_time, end_time
                )
                metrics.cpu_utilization = [dp['Average'] for dp in cpu_data]
                metrics.timestamps = [dp['Timestamp'] for dp in cpu_data]
                
                # Collect memory utilization (if available)
                memory_data = self.get_cloudwatch_metrics(
                    resource_id, 'CWAgent', 'mem_used_percent', start_time, end_time
                )
                metrics.memory_utilization = [dp['Average'] for dp in memory_data] if memory_data else []
                
                # Collect network utilization
                network_data = self.get_cloudwatch_metrics(
                    resource_id, 'AWS/EC2', 'NetworkIn', start_time, end_time
                )
                if network_data:
                    # Convert bytes to percentage of network capacity
                    network_capacity = self.get_network_capacity(metrics.instance_type)
                    metrics.network_utilization = [
                        (dp['Average'] * 8) / (network_capacity * 1000000) * 100  # Convert to Mbps and percentage
                        for dp in network_data
                    ]
                
                # Collect storage utilization
                storage_data = self.get_cloudwatch_metrics(
                    resource_id, 'CWAgent', 'disk_used_percent', start_time, end_time
                )
                metrics.storage_utilization = [dp['Average'] for dp in storage_data] if storage_data else []
                
                # Get cost information
                metrics.cost_per_hour = self.get_resource_cost_per_hour(resource_id, metrics.instance_type)
                
                # Collect performance metrics
                metrics.performance_metrics = self.collect_performance_metrics(resource_id, start_time, end_time)
                
                metrics_list.append(metrics)
                
            except Exception as e:
                print(f"Error collecting metrics for {resource_id}: {e}")
                continue
        
        return metrics_list
    
    def get_cloudwatch_metrics(self, resource_id: str, namespace: str, 
                             metric_name: str, start_time: datetime, end_time: datetime) -> List[Dict]:
        """Get CloudWatch metrics for a resource"""
        
        try:
            response = self.cloudwatch.get_metric_statistics(
                Namespace=namespace,
                MetricName=metric_name,
                Dimensions=[
                    {'Name': 'InstanceId', 'Value': resource_id}
                ],
                StartTime=start_time,
                EndTime=end_time,
                Period=3600,  # 1 hour periods
                Statistics=['Average', 'Maximum', 'Minimum']
            )
            
            return response.get('Datapoints', [])
            
        except Exception as e:
            print(f"Error getting CloudWatch metrics: {e}")
            return []
    
    def analyze_resource_utilization(self, metrics: ResourceMetrics) -> Dict:
        """Analyze resource utilization patterns"""
        
        analysis = {
            'resource_id': metrics.resource_id,
            'instance_type': metrics.instance_type,
            'analysis_period_days': self.analysis_period_days,
            'utilization_summary': {},
            'usage_patterns': {},
            'efficiency_score': 0,
            'optimization_opportunities': []
        }
        
        # Analyze CPU utilization
        if metrics.cpu_utilization:
            cpu_stats = {
                'average': np.mean(metrics.cpu_utilization),
                'maximum': np.max(metrics.cpu_utilization),
                'minimum': np.min(metrics.cpu_utilization),
                'p95': np.percentile(metrics.cpu_utilization, 95),
                'p99': np.percentile(metrics.cpu_utilization, 99),
                'standard_deviation': np.std(metrics.cpu_utilization)
            }
            analysis['utilization_summary']['cpu'] = cpu_stats
            
            # Identify CPU usage patterns
            analysis['usage_patterns']['cpu'] = self.identify_usage_patterns(metrics.cpu_utilization)
        
        # Analyze memory utilization
        if metrics.memory_utilization:
            memory_stats = {
                'average': np.mean(metrics.memory_utilization),
                'maximum': np.max(metrics.memory_utilization),
                'p95': np.percentile(metrics.memory_utilization, 95)
            }
            analysis['utilization_summary']['memory'] = memory_stats
            analysis['usage_patterns']['memory'] = self.identify_usage_patterns(metrics.memory_utilization)
        
        # Calculate efficiency score
        analysis['efficiency_score'] = self.calculate_efficiency_score(metrics)
        
        # Identify optimization opportunities
        analysis['optimization_opportunities'] = self.identify_optimization_opportunities(metrics, analysis)
        
        return analysis
    
    def identify_usage_patterns(self, utilization_data: List[float]) -> Dict:
        """Identify usage patterns in utilization data"""
        
        if not utilization_data:
            return {}
        
        patterns = {
            'pattern_type': 'unknown',
            'variability': 'unknown',
            'trend': 'stable',
            'seasonality': False,
            'burst_frequency': 0
        }
        
        # Calculate variability
        std_dev = np.std(utilization_data)
        mean_util = np.mean(utilization_data)
        
        if std_dev / mean_util < 0.2:
            patterns['variability'] = 'low'
            patterns['pattern_type'] = 'steady'
        elif std_dev / mean_util < 0.5:
            patterns['variability'] = 'medium'
            patterns['pattern_type'] = 'variable'
        else:
            patterns['variability'] = 'high'
            patterns['pattern_type'] = 'bursty'
        
        # Identify bursts (utilization > 80%)
        bursts = [u for u in utilization_data if u > 80]
        patterns['burst_frequency'] = len(bursts) / len(utilization_data)
        
        # Simple trend analysis
        if len(utilization_data) > 10:
            first_half = np.mean(utilization_data[:len(utilization_data)//2])
            second_half = np.mean(utilization_data[len(utilization_data)//2:])
            
            if second_half > first_half * 1.1:
                patterns['trend'] = 'increasing'
            elif second_half < first_half * 0.9:
                patterns['trend'] = 'decreasing'
        
        return patterns
    
    def calculate_efficiency_score(self, metrics: ResourceMetrics) -> float:
        """Calculate overall efficiency score for a resource"""
        
        scores = []
        weights = []
        
        # CPU efficiency
        if metrics.cpu_utilization:
            avg_cpu = np.mean(metrics.cpu_utilization)
            cpu_score = self.calculate_utilization_score(avg_cpu)
            scores.append(cpu_score)
            weights.append(0.4)
        
        # Memory efficiency
        if metrics.memory_utilization:
            avg_memory = np.mean(metrics.memory_utilization)
            memory_score = self.calculate_utilization_score(avg_memory)
            scores.append(memory_score)
            weights.append(0.3)
        
        # Network efficiency
        if metrics.network_utilization:
            avg_network = np.mean(metrics.network_utilization)
            network_score = self.calculate_utilization_score(avg_network)
            scores.append(network_score)
            weights.append(0.2)
        
        # Storage efficiency
        if metrics.storage_utilization:
            avg_storage = np.mean(metrics.storage_utilization)
            storage_score = self.calculate_utilization_score(avg_storage)
            scores.append(storage_score)
            weights.append(0.1)
        
        if scores:
            # Normalize weights
            total_weight = sum(weights)
            normalized_weights = [w / total_weight for w in weights]
            
            # Calculate weighted average
            efficiency_score = sum(s * w for s, w in zip(scores, normalized_weights))
            return efficiency_score
        
        return 0.5  # Default neutral score
    
    def calculate_utilization_score(self, utilization: float) -> float:
        """Calculate utilization score (0-1, where 1 is optimal)"""
        
        if utilization < self.utilization_thresholds['under_utilized']:
            # Under-utilized: score decreases as utilization decreases
            return utilization / self.utilization_thresholds['under_utilized'] * 0.7
        
        elif utilization <= self.utilization_thresholds['optimal']:
            # Optimal range: high score
            return 0.9 + (utilization - self.utilization_thresholds['under_utilized']) / \
                   (self.utilization_thresholds['optimal'] - self.utilization_thresholds['under_utilized']) * 0.1
        
        elif utilization <= self.utilization_thresholds['over_utilized']:
            # Approaching over-utilization: score decreases
            return 1.0 - (utilization - self.utilization_thresholds['optimal']) / \
                   (self.utilization_thresholds['over_utilized'] - self.utilization_thresholds['optimal']) * 0.3
        
        else:
            # Over-utilized: low score
            return 0.3 - min(0.2, (utilization - self.utilization_thresholds['over_utilized']) / 100)
    
    def generate_rightsizing_recommendations(self, metrics_list: List[ResourceMetrics]) -> List[ResourceRecommendation]:
        """Generate rightsizing recommendations based on data analysis"""
        
        recommendations = []
        
        for metrics in metrics_list:
            analysis = self.analyze_resource_utilization(metrics)
            
            # Generate recommendation based on analysis
            recommendation = self.create_recommendation(metrics, analysis)
            
            if recommendation:
                recommendations.append(recommendation)
        
        # Sort recommendations by potential savings
        recommendations.sort(key=lambda x: x.potential_savings, reverse=True)
        
        return recommendations
    
    def create_recommendation(self, metrics: ResourceMetrics, analysis: Dict) -> Optional[ResourceRecommendation]:
        """Create a specific recommendation for a resource"""
        
        cpu_stats = analysis['utilization_summary'].get('cpu', {})
        avg_cpu = cpu_stats.get('average', 50)
        max_cpu = cpu_stats.get('maximum', 50)
        p95_cpu = cpu_stats.get('p95', 50)
        
        current_config = f"{metrics.instance_type}"
        
        # Rightsizing logic
        if avg_cpu < self.utilization_thresholds['under_utilized'] and p95_cpu < 60:
            # Recommend smaller instance
            recommended_type = self.get_smaller_instance_type(metrics.instance_type)
            if recommended_type != metrics.instance_type:
                potential_savings = self.calculate_potential_savings(
                    metrics.instance_type, recommended_type, metrics.cost_per_hour
                )
                
                confidence = self.calculate_confidence_score(analysis)
                
                return ResourceRecommendation(
                    current_config=current_config,
                    recommended_config=recommended_type,
                    confidence_score=confidence,
                    potential_savings=potential_savings,
                    performance_impact="Low risk - CPU utilization well below capacity",
                    implementation_effort="Low - Simple instance type change",
                    rationale=f"Average CPU utilization is {avg_cpu:.1f}%, indicating over-provisioning"
                )
        
        elif p95_cpu > self.utilization_thresholds['over_utilized']:
            # Recommend larger instance
            recommended_type = self.get_larger_instance_type(metrics.instance_type)
            if recommended_type != metrics.instance_type:
                cost_increase = self.calculate_cost_increase(
                    metrics.instance_type, recommended_type, metrics.cost_per_hour
                )
                
                confidence = self.calculate_confidence_score(analysis)
                
                return ResourceRecommendation(
                    current_config=current_config,
                    recommended_config=recommended_type,
                    confidence_score=confidence,
                    potential_savings=-cost_increase,  # Negative savings = cost increase
                    performance_impact="Positive - Improved performance and reduced risk",
                    implementation_effort="Low - Simple instance type change",
                    rationale=f"P95 CPU utilization is {p95_cpu:.1f}%, indicating potential performance issues"
                )
        
        # Check for alternative instance families
        alternative_type = self.suggest_alternative_instance_family(metrics, analysis)
        if alternative_type and alternative_type != metrics.instance_type:
            potential_savings = self.calculate_potential_savings(
                metrics.instance_type, alternative_type, metrics.cost_per_hour
            )
            
            if potential_savings > 0:
                confidence = self.calculate_confidence_score(analysis) * 0.8  # Lower confidence for family changes
                
                return ResourceRecommendation(
                    current_config=current_config,
                    recommended_config=alternative_type,
                    confidence_score=confidence,
                    potential_savings=potential_savings,
                    performance_impact="Medium risk - Different instance family",
                    implementation_effort="Medium - Requires testing and validation",
                    rationale=f"Alternative instance family may provide better price-performance ratio"
                )
        
        return None
    
    def calculate_confidence_score(self, analysis: Dict) -> float:
        """Calculate confidence score for recommendation"""
        
        base_confidence = 0.7
        
        # Increase confidence based on data quality
        cpu_stats = analysis['utilization_summary'].get('cpu', {})
        if cpu_stats:
            std_dev = cpu_stats.get('standard_deviation', 0)
            avg_cpu = cpu_stats.get('average', 50)
            
            # Lower variability increases confidence
            if avg_cpu > 0:
                coefficient_of_variation = std_dev / avg_cpu
                if coefficient_of_variation < 0.3:
                    base_confidence += 0.2
                elif coefficient_of_variation > 0.7:
                    base_confidence -= 0.1
        
        # Increase confidence based on analysis period
        if self.analysis_period_days >= 30:
            base_confidence += 0.1
        
        return min(1.0, max(0.0, base_confidence))
    
    def perform_workload_clustering(self, metrics_list: List[ResourceMetrics]) -> Dict:
        """Cluster workloads based on usage patterns"""
        
        if len(metrics_list) < 3:
            return {'clusters': [], 'recommendations': []}
        
        # Prepare data for clustering
        features = []
        resource_ids = []
        
        for metrics in metrics_list:
            if metrics.cpu_utilization:
                feature_vector = [
                    np.mean(metrics.cpu_utilization),
                    np.std(metrics.cpu_utilization),
                    np.max(metrics.cpu_utilization),
                    np.percentile(metrics.cpu_utilization, 95)
                ]
                
                # Add memory features if available
                if metrics.memory_utilization:
                    feature_vector.extend([
                        np.mean(metrics.memory_utilization),
                        np.max(metrics.memory_utilization)
                    ])
                else:
                    feature_vector.extend([0, 0])
                
                features.append(feature_vector)
                resource_ids.append(metrics.resource_id)
        
        if len(features) < 3:
            return {'clusters': [], 'recommendations': []}
        
        # Perform clustering
        scaler = StandardScaler()
        scaled_features = scaler.fit_transform(features)
        
        # Determine optimal number of clusters (max 5)
        n_clusters = min(5, max(2, len(features) // 3))
        
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        cluster_labels = kmeans.fit_predict(scaled_features)
        
        # Analyze clusters
        clusters = {}
        for i in range(n_clusters):
            cluster_indices = [j for j, label in enumerate(cluster_labels) if label == i]
            cluster_resources = [resource_ids[j] for j in cluster_indices]
            cluster_features = [features[j] for j in cluster_indices]
            
            # Calculate cluster characteristics
            avg_features = np.mean(cluster_features, axis=0)
            
            clusters[f'cluster_{i}'] = {
                'resources': cluster_resources,
                'characteristics': {
                    'avg_cpu_utilization': avg_features[0],
                    'cpu_variability': avg_features[1],
                    'max_cpu_utilization': avg_features[2],
                    'p95_cpu_utilization': avg_features[3],
                    'avg_memory_utilization': avg_features[4] if len(avg_features) > 4 else 0,
                    'max_memory_utilization': avg_features[5] if len(avg_features) > 5 else 0
                },
                'recommended_instance_type': self.recommend_instance_for_cluster(avg_features),
                'optimization_strategy': self.recommend_optimization_strategy(avg_features)
            }
        
        return {
            'clusters': clusters,
            'cluster_labels': cluster_labels,
            'recommendations': self.generate_cluster_recommendations(clusters)
        }
    
    def recommend_instance_for_cluster(self, avg_features: List[float]) -> str:
        """Recommend optimal instance type for a cluster"""
        
        avg_cpu = avg_features[0]
        cpu_variability = avg_features[1]
        max_cpu = avg_features[2]
        
        # Simple heuristic for instance type recommendation
        if avg_cpu < 20 and max_cpu < 50:
            return "t3.medium"  # Burstable for low utilization
        elif avg_cpu < 40 and max_cpu < 70:
            return "m5.large"   # General purpose
        elif avg_cpu < 60 and max_cpu < 85:
            return "m5.xlarge"  # General purpose, larger
        else:
            return "c5.xlarge"  # Compute optimized
    
    def create_resource_selection_dashboard(self, metrics_list: List[ResourceMetrics], 
                                          recommendations: List[ResourceRecommendation]) -> Dict:
        """Create dashboard data for resource selection insights"""
        
        dashboard_data = {
            'summary_metrics': {
                'total_resources': len(metrics_list),
                'total_recommendations': len(recommendations),
                'potential_monthly_savings': sum(r.potential_savings for r in recommendations if r.potential_savings > 0),
                'high_confidence_recommendations': len([r for r in recommendations if r.confidence_score > 0.8])
            },
            'utilization_distribution': self.calculate_utilization_distribution(metrics_list),
            'efficiency_scores': [self.calculate_efficiency_score(m) for m in metrics_list],
            'cost_optimization_opportunities': self.identify_cost_optimization_opportunities(metrics_list, recommendations),
            'instance_type_analysis': self.analyze_instance_type_distribution(metrics_list)
        }
        
        return dashboard_data
    
    def calculate_utilization_distribution(self, metrics_list: List[ResourceMetrics]) -> Dict:
        """Calculate distribution of resource utilization"""
        
        cpu_utilizations = []
        for metrics in metrics_list:
            if metrics.cpu_utilization:
                cpu_utilizations.append(np.mean(metrics.cpu_utilization))
        
        if not cpu_utilizations:
            return {}
        
        return {
            'under_utilized': len([u for u in cpu_utilizations if u < 30]) / len(cpu_utilizations) * 100,
            'optimal': len([u for u in cpu_utilizations if 30 <= u <= 70]) / len(cpu_utilizations) * 100,
            'over_utilized': len([u for u in cpu_utilizations if u > 70]) / len(cpu_utilizations) * 100,
            'average_utilization': np.mean(cpu_utilizations),
            'utilization_variance': np.var(cpu_utilizations)
        }
```

## Data Analysis Templates

### Resource Analysis Report Template
```yaml
Resource_Analysis_Report:
  analysis_id: "RESOURCE-ANALYSIS-2024-001"
  analysis_date: "2024-01-15"
  analysis_period_days: 30
  
  resource_summary:
    total_resources_analyzed: 25
    resource_types:
      EC2: 20
      RDS: 3
      ELB: 2
      
  utilization_analysis:
    cpu_utilization:
      average: 35.2
      median: 28.5
      p95: 67.8
      under_utilized_count: 15
      optimal_count: 8
      over_utilized_count: 2
      
    memory_utilization:
      average: 42.1
      median: 38.7
      p95: 78.2
      
  efficiency_metrics:
    overall_efficiency_score: 0.68
    cost_per_transaction: 0.025
    resource_waste_percentage: 32
    
  recommendations:
    total_recommendations: 18
    high_confidence: 12
    medium_confidence: 4
    low_confidence: 2
    
    potential_savings:
      monthly: 1250.00
      annual: 15000.00
      percentage: 28
      
  top_recommendations:
    - resource_id: "i-1234567890abcdef0"
      current_type: "m5.xlarge"
      recommended_type: "m5.large"
      confidence: 0.92
      monthly_savings: 67.32
      rationale: "Average CPU 18%, P95 CPU 34%"
      
    - resource_id: "i-0987654321fedcba0"
      current_type: "c5.large"
      recommended_type: "t3.large"
      confidence: 0.85
      monthly_savings: 45.20
      rationale: "Variable workload suitable for burstable"
```

### Workload Clustering Analysis
```python
def create_workload_clustering_report(clustering_results):
    """Create comprehensive workload clustering report"""
    
    report = {
        'clustering_summary': {
            'total_clusters': len(clustering_results['clusters']),
            'clustering_date': datetime.now().isoformat(),
            'clustering_algorithm': 'K-Means'
        },
        'cluster_details': {},
        'optimization_strategies': {},
        'implementation_roadmap': []
    }
    
    for cluster_id, cluster_data in clustering_results['clusters'].items():
        cluster_summary = {
            'resource_count': len(cluster_data['resources']),
            'characteristics': cluster_data['characteristics'],
            'recommended_instance_type': cluster_data['recommended_instance_type'],
            'optimization_strategy': cluster_data['optimization_strategy'],
            'estimated_savings': calculate_cluster_savings(cluster_data),
            'implementation_priority': determine_implementation_priority(cluster_data)
        }
        
        report['cluster_details'][cluster_id] = cluster_summary
    
    return report
```

## Common Challenges and Solutions

### Challenge: Insufficient Historical Data

**Solution**: Start with available data and gradually extend the analysis period. Use synthetic data generation for testing. Implement comprehensive monitoring from the beginning of new deployments.

### Challenge: Seasonal Usage Patterns

**Solution**: Collect data over multiple seasonal cycles. Use time-series analysis to identify seasonal patterns. Create separate models for different seasons or usage patterns.

### Challenge: Complex Multi-Tier Applications

**Solution**: Analyze application tiers separately and together. Use distributed tracing to understand dependencies. Consider the impact of changes on the entire application stack.

### Challenge: Performance vs. Cost Trade-offs

**Solution**: Define clear performance requirements and SLAs. Use multi-objective optimization techniques. Create cost-performance efficiency metrics to guide decisions.

### Challenge: Data Quality and Completeness

**Solution**: Implement data validation and quality checks. Use multiple data sources for validation. Establish data collection standards and monitoring for data quality.

## Related Resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/cost_type_size_number_data.html">AWS Well-Architected Framework - Select resource type, size, and number based on data</a></li>
    <li><a href="https://aws.amazon.com/compute-optimizer/">AWS Compute Optimizer</a></li>
    <li><a href="https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html">Amazon CloudWatch User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/xray/latest/devguide/aws-xray.html">AWS X-Ray Developer Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/cost-management/latest/userguide/ce-what-is.html">AWS Cost Explorer User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/systems-manager/latest/userguide/what-is-systems-manager.html">AWS Systems Manager User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/AnalyzingLogData.html">Amazon CloudWatch Logs Insights</a></li>
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
