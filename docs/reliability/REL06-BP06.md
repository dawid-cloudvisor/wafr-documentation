---
title: REL06-BP06 - Review metrics at regular intervals
layout: default
parent: REL06 - How do you monitor workload resources?
grand_parent: Reliability
nav_order: 6
---

# REL06-BP06: Review metrics at regular intervals

## Overview

Establish systematic processes for regularly reviewing metrics, analyzing trends, and identifying opportunities for improvement. Regular metric reviews ensure monitoring systems remain effective, thresholds stay relevant, and insights drive continuous optimization of workload reliability.

## Implementation Steps

### 1. Establish Review Schedules and Cadences
- Define daily, weekly, monthly, and quarterly review cycles
- Assign ownership and responsibilities for different review types
- Create standardized review agendas and documentation templates
- Implement automated review reminders and scheduling

### 2. Implement Trend Analysis and Pattern Recognition
- Configure automated trend detection and anomaly identification
- Establish baseline metrics and performance benchmarks
- Implement seasonal and cyclical pattern analysis
- Create predictive analytics for capacity and performance planning

### 3. Create Review Processes and Workflows
- Design structured review meetings and documentation processes
- Implement action item tracking and follow-up procedures
- Establish escalation paths for critical findings
- Create feedback loops for continuous improvement

### 4. Configure Automated Review Assistance
- Implement automated metric summarization and reporting
- Configure intelligent alerting for review-worthy events
- Create automated recommendations and insights generation
- Establish machine learning-based pattern detection

### 5. Establish Metric Governance and Optimization
- Regularly review and update alert thresholds and conditions
- Implement metric lifecycle management and deprecation
- Optimize monitoring costs and resource utilization
- Establish metric quality and accuracy validation

### 6. Track Review Effectiveness and Outcomes
- Monitor review completion rates and timeliness
- Track action item resolution and implementation success
- Measure improvement in system reliability and performance
- Establish ROI metrics for monitoring and review processes

## Implementation Examples

### Example 1: Automated Metric Review System
```python
import boto3
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import statistics
import numpy as np

class ReviewType(Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"

class TrendDirection(Enum):
    INCREASING = "increasing"
    DECREASING = "decreasing"
    STABLE = "stable"
    VOLATILE = "volatile"

@dataclass
class MetricReview:
    review_id: str
    metric_name: str
    review_type: ReviewType
    review_date: datetime
    current_value: float
    previous_value: float
    trend_direction: TrendDirection
    anomalies_detected: List[Dict[str, Any]]
    recommendations: List[str]
    action_items: List[Dict[str, Any]]
    reviewer: str

@dataclass
class ReviewInsight:
    insight_id: str
    metric_name: str
    insight_type: str
    description: str
    severity: str
    confidence_score: float
    supporting_data: Dict[str, Any]
    recommended_actions: List[str]

class MetricReviewEngine:
    """Automated metric review and analysis system"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
        # AWS clients
        self.cloudwatch = boto3.client('cloudwatch')
        self.dynamodb = boto3.resource('dynamodb')
        self.sns = boto3.client('sns')
        
        # Storage
        self.reviews_table = self.dynamodb.Table(config.get('reviews_table', 'metric-reviews'))
        self.insights_table = self.dynamodb.Table(config.get('insights_table', 'review-insights'))
        
        # Review configuration
        self.review_schedules = config.get('review_schedules', {})
        self.metric_configs = config.get('metric_configs', {})
        
    async def perform_scheduled_review(self, review_type: ReviewType) -> List[str]:
        """Perform scheduled metric review"""
        try:
            review_ids = []
            
            # Get metrics to review
            metrics_to_review = self._get_metrics_for_review(review_type)
            
            for metric_config in metrics_to_review:
                review_id = await self._review_metric(metric_config, review_type)
                if review_id:
                    review_ids.append(review_id)
            
            # Generate summary report
            await self._generate_review_summary(review_ids, review_type)
            
            logging.info(f"Completed {review_type.value} review for {len(review_ids)} metrics")
            return review_ids
            
        except Exception as e:
            logging.error(f"Failed to perform scheduled review: {str(e)}")
            return []
    
    def _get_metrics_for_review(self, review_type: ReviewType) -> List[Dict[str, Any]]:
        """Get list of metrics to review based on schedule"""
        metrics = []
        
        for metric_name, config in self.metric_configs.items():
            review_schedule = config.get('review_schedule', [])
            
            if review_type.value in review_schedule:
                metrics.append({
                    'metric_name': metric_name,
                    'namespace': config['namespace'],
                    'dimensions': config.get('dimensions', []),
                    'statistic': config.get('statistic', 'Average'),
                    'thresholds': config.get('thresholds', {}),
                    'review_config': config.get('review_config', {})
                })
        
        return metrics
    
    async def _review_metric(self, metric_config: Dict[str, Any], review_type: ReviewType) -> Optional[str]:
        """Review a specific metric"""
        try:
            metric_name = metric_config['metric_name']
            
            # Get metric data
            current_data = await self._get_metric_data(metric_config, review_type)
            previous_data = await self._get_previous_period_data(metric_config, review_type)
            
            if not current_data or not previous_data:
                logging.warning(f"Insufficient data for metric {metric_name}")
                return None
            
            # Analyze trends
            trend_analysis = self._analyze_trend(current_data, previous_data)
            
            # Detect anomalies
            anomalies = self._detect_anomalies(current_data, metric_config)
            
            # Generate insights
            insights = await self._generate_insights(metric_config, current_data, trend_analysis, anomalies)
            
            # Create recommendations
            recommendations = self._generate_recommendations(metric_config, trend_analysis, anomalies, insights)
            
            # Create action items
            action_items = self._create_action_items(recommendations, metric_config)
            
            # Create review record
            review = MetricReview(
                review_id=f"review_{int(datetime.utcnow().timestamp())}_{metric_name}",
                metric_name=metric_name,
                review_type=review_type,
                review_date=datetime.utcnow(),
                current_value=statistics.mean(current_data) if current_data else 0,
                previous_value=statistics.mean(previous_data) if previous_data else 0,
                trend_direction=trend_analysis['direction'],
                anomalies_detected=anomalies,
                recommendations=recommendations,
                action_items=action_items,
                reviewer='automated_system'
            )
            
            # Store review
            await self._store_review(review)
            
            # Store insights
            for insight in insights:
                await self._store_insight(insight)
            
            return review.review_id
            
        except Exception as e:
            logging.error(f"Failed to review metric {metric_config['metric_name']}: {str(e)}")
            return None
    
    async def _get_metric_data(self, metric_config: Dict[str, Any], review_type: ReviewType) -> List[float]:
        """Get metric data for the review period"""
        try:
            # Determine time range based on review type
            time_ranges = {
                ReviewType.DAILY: timedelta(days=1),
                ReviewType.WEEKLY: timedelta(days=7),
                ReviewType.MONTHLY: timedelta(days=30),
                ReviewType.QUARTERLY: timedelta(days=90)
            }
            
            end_time = datetime.utcnow()
            start_time = end_time - time_ranges[review_type]
            
            response = self.cloudwatch.get_metric_statistics(
                Namespace=metric_config['namespace'],
                MetricName=metric_config['metric_name'],
                Dimensions=metric_config.get('dimensions', []),
                StartTime=start_time,
                EndTime=end_time,
                Period=3600,  # 1 hour periods
                Statistics=[metric_config.get('statistic', 'Average')]
            )
            
            statistic = metric_config.get('statistic', 'Average')
            return [dp[statistic] for dp in response['Datapoints']]
            
        except Exception as e:
            logging.error(f"Failed to get metric data: {str(e)}")
            return []
    
    async def _get_previous_period_data(self, metric_config: Dict[str, Any], review_type: ReviewType) -> List[float]:
        """Get metric data for the previous period for comparison"""
        try:
            time_ranges = {
                ReviewType.DAILY: timedelta(days=1),
                ReviewType.WEEKLY: timedelta(days=7),
                ReviewType.MONTHLY: timedelta(days=30),
                ReviewType.QUARTERLY: timedelta(days=90)
            }
            
            current_range = time_ranges[review_type]
            end_time = datetime.utcnow() - current_range
            start_time = end_time - current_range
            
            response = self.cloudwatch.get_metric_statistics(
                Namespace=metric_config['namespace'],
                MetricName=metric_config['metric_name'],
                Dimensions=metric_config.get('dimensions', []),
                StartTime=start_time,
                EndTime=end_time,
                Period=3600,
                Statistics=[metric_config.get('statistic', 'Average')]
            )
            
            statistic = metric_config.get('statistic', 'Average')
            return [dp[statistic] for dp in response['Datapoints']]
            
        except Exception as e:
            logging.error(f"Failed to get previous period data: {str(e)}")
            return []
    
    def _analyze_trend(self, current_data: List[float], previous_data: List[float]) -> Dict[str, Any]:
        """Analyze trend between current and previous periods"""
        try:
            if not current_data or not previous_data:
                return {'direction': TrendDirection.STABLE, 'change_percent': 0}
            
            current_avg = statistics.mean(current_data)
            previous_avg = statistics.mean(previous_data)
            
            if previous_avg == 0:
                change_percent = 0
            else:
                change_percent = ((current_avg - previous_avg) / previous_avg) * 100
            
            # Determine trend direction
            if abs(change_percent) < 5:  # Less than 5% change
                direction = TrendDirection.STABLE
            elif change_percent > 0:
                direction = TrendDirection.INCREASING
            else:
                direction = TrendDirection.DECREASING
            
            # Check for volatility
            current_std = statistics.stdev(current_data) if len(current_data) > 1 else 0
            previous_std = statistics.stdev(previous_data) if len(previous_data) > 1 else 0
            
            volatility_increase = current_std > previous_std * 1.5
            if volatility_increase:
                direction = TrendDirection.VOLATILE
            
            return {
                'direction': direction,
                'change_percent': change_percent,
                'current_average': current_avg,
                'previous_average': previous_avg,
                'volatility_increase': volatility_increase
            }
            
        except Exception as e:
            logging.error(f"Failed to analyze trend: {str(e)}")
            return {'direction': TrendDirection.STABLE, 'change_percent': 0}
    
    def _detect_anomalies(self, data: List[float], metric_config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detect anomalies in metric data"""
        anomalies = []
        
        try:
            if len(data) < 3:
                return anomalies
            
            # Statistical anomaly detection
            mean_val = statistics.mean(data)
            std_val = statistics.stdev(data)
            
            # Z-score based anomaly detection
            for i, value in enumerate(data):
                z_score = abs((value - mean_val) / std_val) if std_val > 0 else 0
                
                if z_score > 2:  # More than 2 standard deviations
                    anomalies.append({
                        'type': 'statistical_outlier',
                        'value': value,
                        'z_score': z_score,
                        'position': i,
                        'severity': 'high' if z_score > 3 else 'medium'
                    })
            
            # Threshold-based anomaly detection
            thresholds = metric_config.get('thresholds', {})
            if thresholds:
                for value in data:
                    if 'critical' in thresholds and value > thresholds['critical']:
                        anomalies.append({
                            'type': 'threshold_exceeded',
                            'value': value,
                            'threshold': thresholds['critical'],
                            'threshold_type': 'critical',
                            'severity': 'critical'
                        })
                    elif 'warning' in thresholds and value > thresholds['warning']:
                        anomalies.append({
                            'type': 'threshold_exceeded',
                            'value': value,
                            'threshold': thresholds['warning'],
                            'threshold_type': 'warning',
                            'severity': 'warning'
                        })
            
            return anomalies
            
        except Exception as e:
            logging.error(f"Failed to detect anomalies: {str(e)}")
            return []
    
    async def _generate_insights(self, metric_config: Dict[str, Any], data: List[float], 
                               trend_analysis: Dict[str, Any], anomalies: List[Dict[str, Any]]) -> List[ReviewInsight]:
        """Generate insights from metric analysis"""
        insights = []
        
        try:
            metric_name = metric_config['metric_name']
            
            # Trend insights
            if trend_analysis['direction'] == TrendDirection.INCREASING:
                if trend_analysis['change_percent'] > 20:
                    insights.append(ReviewInsight(
                        insight_id=f"trend_{metric_name}_{int(datetime.utcnow().timestamp())}",
                        metric_name=metric_name,
                        insight_type='trend_analysis',
                        description=f"Significant upward trend detected: {trend_analysis['change_percent']:.1f}% increase",
                        severity='medium' if trend_analysis['change_percent'] < 50 else 'high',
                        confidence_score=0.8,
                        supporting_data=trend_analysis,
                        recommended_actions=['Investigate cause of increase', 'Check capacity planning', 'Review scaling policies']
                    ))
            
            # Anomaly insights
            if anomalies:
                critical_anomalies = [a for a in anomalies if a.get('severity') == 'critical']
                if critical_anomalies:
                    insights.append(ReviewInsight(
                        insight_id=f"anomaly_{metric_name}_{int(datetime.utcnow().timestamp())}",
                        metric_name=metric_name,
                        insight_type='anomaly_detection',
                        description=f"Critical anomalies detected: {len(critical_anomalies)} instances",
                        severity='critical',
                        confidence_score=0.9,
                        supporting_data={'anomalies': critical_anomalies},
                        recommended_actions=['Immediate investigation required', 'Check system health', 'Review recent changes']
                    ))
            
            # Performance insights
            if data:
                avg_value = statistics.mean(data)
                thresholds = metric_config.get('thresholds', {})
                
                if 'optimal' in thresholds and avg_value > thresholds['optimal']:
                    insights.append(ReviewInsight(
                        insight_id=f"performance_{metric_name}_{int(datetime.utcnow().timestamp())}",
                        metric_name=metric_name,
                        insight_type='performance_analysis',
                        description=f"Performance below optimal: average {avg_value:.2f} exceeds optimal threshold {thresholds['optimal']}",
                        severity='medium',
                        confidence_score=0.7,
                        supporting_data={'average_value': avg_value, 'optimal_threshold': thresholds['optimal']},
                        recommended_actions=['Performance optimization needed', 'Review resource allocation', 'Consider scaling']
                    ))
            
            return insights
            
        except Exception as e:
            logging.error(f"Failed to generate insights: {str(e)}")
            return []
    
    def _generate_recommendations(self, metric_config: Dict[str, Any], trend_analysis: Dict[str, Any], 
                                anomalies: List[Dict[str, Any]], insights: List[ReviewInsight]) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        try:
            # Trend-based recommendations
            if trend_analysis['direction'] == TrendDirection.INCREASING and trend_analysis['change_percent'] > 30:
                recommendations.append("Consider implementing auto-scaling to handle increased load")
                recommendations.append("Review capacity planning and resource allocation")
            
            elif trend_analysis['direction'] == TrendDirection.VOLATILE:
                recommendations.append("Investigate source of volatility and implement smoothing mechanisms")
                recommendations.append("Consider adjusting monitoring thresholds to reduce noise")
            
            # Anomaly-based recommendations
            if anomalies:
                high_severity_anomalies = [a for a in anomalies if a.get('severity') in ['high', 'critical']]
                if high_severity_anomalies:
                    recommendations.append("Immediate investigation of anomalies required")
                    recommendations.append("Review recent deployments and configuration changes")
            
            # Insight-based recommendations
            for insight in insights:
                recommendations.extend(insight.recommended_actions)
            
            # General recommendations
            recommendations.append("Update alert thresholds based on current performance patterns")
            recommendations.append("Schedule follow-up review to track improvement")
            
            return list(set(recommendations))  # Remove duplicates
            
        except Exception as e:
            logging.error(f"Failed to generate recommendations: {str(e)}")
            return []
    
    def _create_action_items(self, recommendations: List[str], metric_config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create actionable items from recommendations"""
        action_items = []
        
        try:
            for i, recommendation in enumerate(recommendations):
                action_items.append({
                    'id': f"action_{int(datetime.utcnow().timestamp())}_{i}",
                    'description': recommendation,
                    'priority': self._determine_priority(recommendation),
                    'assigned_to': metric_config.get('owner', 'unassigned'),
                    'due_date': (datetime.utcnow() + timedelta(days=7)).isoformat(),
                    'status': 'open',
                    'created_date': datetime.utcnow().isoformat()
                })
            
            return action_items
            
        except Exception as e:
            logging.error(f"Failed to create action items: {str(e)}")
            return []
    
    def _determine_priority(self, recommendation: str) -> str:
        """Determine priority level for action item"""
        high_priority_keywords = ['immediate', 'critical', 'urgent', 'investigate']
        medium_priority_keywords = ['review', 'consider', 'update']
        
        recommendation_lower = recommendation.lower()
        
        if any(keyword in recommendation_lower for keyword in high_priority_keywords):
            return 'high'
        elif any(keyword in recommendation_lower for keyword in medium_priority_keywords):
            return 'medium'
        else:
            return 'low'
    
    async def _store_review(self, review: MetricReview):
        """Store review in DynamoDB"""
        try:
            review_dict = asdict(review)
            review_dict['review_date'] = review.review_date.isoformat()
            
            self.reviews_table.put_item(Item=review_dict)
            
        except Exception as e:
            logging.error(f"Failed to store review: {str(e)}")
    
    async def _store_insight(self, insight: ReviewInsight):
        """Store insight in DynamoDB"""
        try:
            insight_dict = asdict(insight)
            self.insights_table.put_item(Item=insight_dict)
            
        except Exception as e:
            logging.error(f"Failed to store insight: {str(e)}")
    
    async def _generate_review_summary(self, review_ids: List[str], review_type: ReviewType):
        """Generate and send review summary"""
        try:
            summary = {
                'review_type': review_type.value,
                'review_date': datetime.utcnow().isoformat(),
                'total_metrics_reviewed': len(review_ids),
                'review_ids': review_ids
            }
            
            # Send summary notification
            topic_arn = self.config.get('summary_topic_arn')
            if topic_arn:
                self.sns.publish(
                    TopicArn=topic_arn,
                    Message=json.dumps(summary, indent=2),
                    Subject=f"{review_type.value.title()} Metric Review Summary"
                )
            
            logging.info(f"Generated {review_type.value} review summary for {len(review_ids)} metrics")
            
        except Exception as e:
            logging.error(f"Failed to generate review summary: {str(e)}")

# Usage example
async def main():
    config = {
        'reviews_table': 'metric-reviews',
        'insights_table': 'review-insights',
        'summary_topic_arn': 'arn:aws:sns:us-east-1:123456789012:metric-reviews',
        'metric_configs': {
            'CPUUtilization': {
                'namespace': 'AWS/EC2',
                'dimensions': [{'Name': 'InstanceId', 'Value': 'i-1234567890abcdef0'}],
                'statistic': 'Average',
                'thresholds': {'warning': 70, 'critical': 90, 'optimal': 60},
                'review_schedule': ['daily', 'weekly'],
                'owner': 'ops-team@company.com'
            },
            'ResponseTime': {
                'namespace': 'AWS/ApplicationELB',
                'statistic': 'Average',
                'thresholds': {'warning': 1.0, 'critical': 2.0, 'optimal': 0.5},
                'review_schedule': ['daily', 'monthly'],
                'owner': 'app-team@company.com'
            }
        }
    }
    
    # Initialize review engine
    review_engine = MetricReviewEngine(config)
    
    # Perform daily review
    daily_reviews = await review_engine.perform_scheduled_review(ReviewType.DAILY)
    print(f"Completed daily review: {len(daily_reviews)} metrics reviewed")
    
    # Perform weekly review
    weekly_reviews = await review_engine.perform_scheduled_review(ReviewType.WEEKLY)
    print(f"Completed weekly review: {len(weekly_reviews)} metrics reviewed")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## AWS Services Used

- **Amazon CloudWatch**: Historical metric data retrieval and trend analysis
- **AWS Lambda**: Automated review execution and scheduling
- **Amazon DynamoDB**: Storage for review results, insights, and action items
- **Amazon SNS**: Review summary notifications and alert distribution
- **Amazon EventBridge**: Scheduled review triggers and workflow automation
- **AWS Systems Manager**: Parameter storage for review configurations
- **Amazon S3**: Long-term storage of review reports and historical data
- **Amazon QuickSight**: Review dashboard creation and trend visualization
- **AWS Step Functions**: Complex review workflow orchestration
- **Amazon Kinesis**: Real-time metric streaming for continuous analysis
- **AWS Config**: Configuration change tracking for review context
- **Amazon Athena**: Ad-hoc analysis of historical review data
- **AWS Glue**: Data preparation and transformation for review analytics
- **Amazon Timestream**: Time-series data storage for metric history
- **AWS X-Ray**: Performance analysis and review insights

## Benefits

- **Continuous Improvement**: Regular reviews drive ongoing optimization and enhancement
- **Proactive Issue Detection**: Systematic analysis identifies problems before they impact users
- **Data-Driven Decisions**: Trend analysis and insights support informed decision making
- **Threshold Optimization**: Regular review ensures alert thresholds remain relevant and effective
- **Cost Optimization**: Identifies opportunities to optimize monitoring costs and resource usage
- **Knowledge Sharing**: Structured reviews facilitate team learning and knowledge transfer
- **Compliance Assurance**: Regular reviews ensure monitoring meets regulatory requirements
- **Performance Tracking**: Historical analysis enables performance trend identification
- **Capacity Planning**: Trend analysis supports accurate capacity and scaling decisions
- **Risk Mitigation**: Early identification of concerning trends reduces operational risk

## Related Resources

- [AWS Well-Architected Reliability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/)
- [Review Metrics at Regular Intervals](https://docs.aws.amazon.com/wellarchitected/latest/framework/rel_monitor_aws_resources_review_monitoring_monitor.html)
- [Amazon CloudWatch User Guide](https://docs.aws.amazon.com/cloudwatch/latest/monitoring/)
- [AWS Lambda User Guide](https://docs.aws.amazon.com/lambda/latest/dg/)
- [Amazon DynamoDB Developer Guide](https://docs.aws.amazon.com/dynamodb/latest/developerguide/)
- [Amazon EventBridge User Guide](https://docs.aws.amazon.com/eventbridge/latest/userguide/)
- [AWS Step Functions User Guide](https://docs.aws.amazon.com/step-functions/latest/dg/)
- [Amazon QuickSight User Guide](https://docs.aws.amazon.com/quicksight/latest/user/)
- [Monitoring Best Practices](https://aws.amazon.com/builders-library/implementing-health-checks/)
- [Operational Excellence](https://aws.amazon.com/architecture/well-architected/)
- [Metric Analysis Techniques](https://docs.aws.amazon.com/cloudwatch/latest/monitoring/cloudwatch_concepts.html)
- [Performance Monitoring](https://aws.amazon.com/builders-library/)
