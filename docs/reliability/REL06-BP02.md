---
title: REL06-BP02 - Define and calculate metrics (Aggregation)
layout: default
parent: REL06 - How do you monitor workload resources?
grand_parent: Reliability
nav_order: 2
---

# REL06-BP02: Define and calculate metrics (Aggregation)

## Overview

Define meaningful metrics and implement aggregation strategies to transform raw monitoring data into actionable insights. Effective metric aggregation provides the right level of detail for different stakeholders while maintaining the ability to drill down into specific issues when needed.

## Implementation Steps

### 1. Define Key Performance Indicators (KPIs)
- Establish business-level metrics that align with organizational objectives
- Define technical metrics for system health and performance
- Create user experience metrics for customer satisfaction
- Implement operational metrics for team efficiency and incident response

### 2. Implement Metric Aggregation Strategies
- Configure time-based aggregation (hourly, daily, weekly, monthly)
- Implement dimensional aggregation across services, regions, and environments
- Design statistical aggregations (average, percentiles, min/max, sum)
- Create composite metrics from multiple data sources

### 3. Establish Metric Hierarchies and Relationships
- Design metric hierarchies from infrastructure to business level
- Implement metric dependencies and correlations
- Create rollup metrics for executive dashboards
- Establish drill-down capabilities for detailed analysis

### 4. Configure Real-time and Historical Aggregation
- Implement streaming aggregation for real-time monitoring
- Design batch aggregation for historical analysis
- Configure retention policies for different aggregation levels
- Optimize storage and query performance for aggregated data

### 5. Implement Custom Metrics and Calculations
- Create business-specific metrics and calculations
- Implement derived metrics from base measurements
- Design ratio and rate calculations
- Configure trend analysis and forecasting metrics

### 6. Establish Metric Quality and Validation
- Implement data quality checks for metric accuracy
- Configure anomaly detection for metric validation
- Design metric lineage and documentation
- Establish metric governance and change management

## Implementation Examples

### Example 1: Advanced Metrics Aggregation System
```python
import boto3
import json
import logging
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import asyncio
import statistics
from collections import defaultdict

class AggregationType(Enum):
    SUM = "sum"
    AVERAGE = "average"
    MIN = "min"
    MAX = "max"
    COUNT = "count"
    PERCENTILE = "percentile"
    RATE = "rate"
    RATIO = "ratio"

class TimeWindow(Enum):
    MINUTE = "1m"
    FIVE_MINUTES = "5m"
    HOUR = "1h"
    DAY = "1d"
    WEEK = "1w"
    MONTH = "1M"

@dataclass
class MetricDefinition:
    metric_name: str
    source_metrics: List[str]
    aggregation_type: AggregationType
    time_windows: List[TimeWindow]
    dimensions: List[str]
    filters: Dict[str, Any]
    calculation_formula: Optional[str] = None
    percentile_value: Optional[float] = None

@dataclass
class AggregatedMetric:
    metric_name: str
    value: float
    timestamp: datetime
    time_window: TimeWindow
    dimensions: Dict[str, str]
    sample_count: int
    aggregation_type: AggregationType

class MetricsAggregationEngine:
    """Advanced metrics aggregation and calculation engine"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
        # AWS clients
        self.cloudwatch = boto3.client('cloudwatch')
        self.timestream = boto3.client('timestream-write')
        self.s3 = boto3.client('s3')
        
        # Metric definitions registry
        self.metric_definitions = {}
        self.aggregation_rules = {}
        
        # Data storage
        self.raw_metrics_buffer = []
        self.aggregated_metrics_buffer = []
        
        # Configuration
        self.timestream_database = config.get('timestream_database', 'MetricsDB')
        self.timestream_table = config.get('timestream_table', 'AggregatedMetrics')
        
    def register_metric_definition(self, definition: MetricDefinition):
        """Register a metric definition for aggregation"""
        self.metric_definitions[definition.metric_name] = definition
        logging.info(f"Registered metric definition: {definition.metric_name}")
    
    async def process_raw_metrics(self, raw_metrics: List[Dict[str, Any]]) -> List[AggregatedMetric]:
        """Process raw metrics and generate aggregations"""
        aggregated_metrics = []
        
        try:
            # Group metrics by definition
            metrics_by_definition = self._group_metrics_by_definition(raw_metrics)
            
            # Process each metric definition
            for metric_name, definition in self.metric_definitions.items():
                if metric_name in metrics_by_definition:
                    metrics_data = metrics_by_definition[metric_name]
                    
                    # Generate aggregations for each time window
                    for time_window in definition.time_windows:
                        aggregated = await self._aggregate_metrics(
                            metrics_data, definition, time_window
                        )
                        aggregated_metrics.extend(aggregated)
            
            return aggregated_metrics
            
        except Exception as e:
            logging.error(f"Failed to process raw metrics: {str(e)}")
            return []
    
    def _group_metrics_by_definition(self, raw_metrics: List[Dict[str, Any]]) -> Dict[str, List[Dict]]:
        """Group raw metrics by their definitions"""
        grouped_metrics = defaultdict(list)
        
        for metric in raw_metrics:
            metric_name = metric.get('MetricName')
            if metric_name in self.metric_definitions:
                grouped_metrics[metric_name].append(metric)
        
        return grouped_metrics
    
    async def _aggregate_metrics(self, metrics_data: List[Dict], 
                               definition: MetricDefinition, 
                               time_window: TimeWindow) -> List[AggregatedMetric]:
        """Aggregate metrics for a specific time window"""
        aggregated_metrics = []
        
        try:
            # Convert to DataFrame for easier processing
            df = pd.DataFrame(metrics_data)
            if df.empty:
                return aggregated_metrics
            
            # Parse timestamps
            df['Timestamp'] = pd.to_datetime(df['Timestamp'])
            
            # Group by time window and dimensions
            time_freq = self._get_pandas_frequency(time_window)
            grouping_columns = ['Timestamp_Window'] + definition.dimensions
            
            # Create time windows
            df['Timestamp_Window'] = df['Timestamp'].dt.floor(time_freq)
            
            # Apply filters if specified
            if definition.filters:
                df = self._apply_filters(df, definition.filters)
            
            # Group by time window and dimensions
            if definition.dimensions:
                # Ensure dimension columns exist
                for dim in definition.dimensions:
                    if dim not in df.columns:
                        df[dim] = 'unknown'
                
                grouped = df.groupby(grouping_columns)
            else:
                grouped = df.groupby(['Timestamp_Window'])
            
            # Calculate aggregations
            for group_key, group_data in grouped:
                if isinstance(group_key, tuple):
                    timestamp_window = group_key[0]
                    dimension_values = dict(zip(definition.dimensions, group_key[1:]))
                else:
                    timestamp_window = group_key
                    dimension_values = {}
                
                # Calculate aggregated value
                aggregated_value = self._calculate_aggregation(
                    group_data['Value'].tolist(), definition.aggregation_type, definition.percentile_value
                )
                
                # Create aggregated metric
                aggregated_metric = AggregatedMetric(
                    metric_name=definition.metric_name,
                    value=aggregated_value,
                    timestamp=timestamp_window,
                    time_window=time_window,
                    dimensions=dimension_values,
                    sample_count=len(group_data),
                    aggregation_type=definition.aggregation_type
                )
                
                aggregated_metrics.append(aggregated_metric)
            
        except Exception as e:
            logging.error(f"Failed to aggregate metrics for {definition.metric_name}: {str(e)}")
        
        return aggregated_metrics
    
    def _calculate_aggregation(self, values: List[float], 
                             aggregation_type: AggregationType, 
                             percentile_value: Optional[float] = None) -> float:
        """Calculate aggregated value based on aggregation type"""
        if not values:
            return 0.0
        
        try:
            if aggregation_type == AggregationType.SUM:
                return sum(values)
            elif aggregation_type == AggregationType.AVERAGE:
                return statistics.mean(values)
            elif aggregation_type == AggregationType.MIN:
                return min(values)
            elif aggregation_type == AggregationType.MAX:
                return max(values)
            elif aggregation_type == AggregationType.COUNT:
                return len(values)
            elif aggregation_type == AggregationType.PERCENTILE:
                if percentile_value is not None:
                    return np.percentile(values, percentile_value)
                else:
                    return np.percentile(values, 95)  # Default to P95
            elif aggregation_type == AggregationType.RATE:
                # Calculate rate (change over time)
                if len(values) >= 2:
                    return (values[-1] - values[0]) / len(values)
                return 0.0
            else:
                return statistics.mean(values)  # Default to average
                
        except Exception as e:
            logging.error(f"Failed to calculate aggregation: {str(e)}")
            return 0.0
    
    def _get_pandas_frequency(self, time_window: TimeWindow) -> str:
        """Convert TimeWindow enum to pandas frequency string"""
        frequency_map = {
            TimeWindow.MINUTE: '1T',
            TimeWindow.FIVE_MINUTES: '5T',
            TimeWindow.HOUR: '1H',
            TimeWindow.DAY: '1D',
            TimeWindow.WEEK: '1W',
            TimeWindow.MONTH: '1M'
        }
        return frequency_map.get(time_window, '1H')
    
    def _apply_filters(self, df: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
        """Apply filters to the DataFrame"""
        filtered_df = df.copy()
        
        for column, filter_value in filters.items():
            if column in filtered_df.columns:
                if isinstance(filter_value, list):
                    filtered_df = filtered_df[filtered_df[column].isin(filter_value)]
                else:
                    filtered_df = filtered_df[filtered_df[column] == filter_value]
        
        return filtered_df
    
    async def create_composite_metrics(self, aggregated_metrics: List[AggregatedMetric]) -> List[AggregatedMetric]:
        """Create composite metrics from aggregated metrics"""
        composite_metrics = []
        
        try:
            # Group metrics by timestamp and dimensions for composite calculations
            metrics_by_time = defaultdict(list)
            
            for metric in aggregated_metrics:
                key = (metric.timestamp, tuple(sorted(metric.dimensions.items())))
                metrics_by_time[key].append(metric)
            
            # Calculate composite metrics
            for (timestamp, dimensions_tuple), metrics_group in metrics_by_time.items():
                dimensions = dict(dimensions_tuple)
                
                # Example: Calculate error rate (errors / total requests)
                error_count = next((m.value for m in metrics_group if m.metric_name == 'ErrorCount'), 0)
                request_count = next((m.value for m in metrics_group if m.metric_name == 'RequestCount'), 1)
                
                if request_count > 0:
                    error_rate = (error_count / request_count) * 100
                    
                    composite_metric = AggregatedMetric(
                        metric_name='ErrorRate',
                        value=error_rate,
                        timestamp=timestamp,
                        time_window=TimeWindow.HOUR,  # Default time window
                        dimensions=dimensions,
                        sample_count=1,
                        aggregation_type=AggregationType.RATIO
                    )
                    
                    composite_metrics.append(composite_metric)
                
                # Example: Calculate availability (successful requests / total requests)
                success_count = next((m.value for m in metrics_group if m.metric_name == 'SuccessCount'), 0)
                
                if request_count > 0:
                    availability = (success_count / request_count) * 100
                    
                    composite_metric = AggregatedMetric(
                        metric_name='Availability',
                        value=availability,
                        timestamp=timestamp,
                        time_window=TimeWindow.HOUR,
                        dimensions=dimensions,
                        sample_count=1,
                        aggregation_type=AggregationType.RATIO
                    )
                    
                    composite_metrics.append(composite_metric)
            
        except Exception as e:
            logging.error(f"Failed to create composite metrics: {str(e)}")
        
        return composite_metrics
    
    async def store_aggregated_metrics(self, metrics: List[AggregatedMetric]):
        """Store aggregated metrics in TimeStream"""
        try:
            # Prepare records for TimeStream
            records = []
            
            for metric in metrics:
                # Convert dimensions to TimeStream format
                dimensions = [
                    {'Name': key, 'Value': value}
                    for key, value in metric.dimensions.items()
                ]
                
                # Add metric-specific dimensions
                dimensions.extend([
                    {'Name': 'MetricName', 'Value': metric.metric_name},
                    {'Name': 'TimeWindow', 'Value': metric.time_window.value},
                    {'Name': 'AggregationType', 'Value': metric.aggregation_type.value}
                ])
                
                record = {
                    'Time': str(int(metric.timestamp.timestamp() * 1000)),
                    'TimeUnit': 'MILLISECONDS',
                    'Dimensions': dimensions,
                    'MeasureName': 'value',
                    'MeasureValue': str(metric.value),
                    'MeasureValueType': 'DOUBLE'
                }
                
                records.append(record)
            
            # Write to TimeStream in batches
            batch_size = 100
            for i in range(0, len(records), batch_size):
                batch = records[i:i + batch_size]
                
                self.timestream.write_records(
                    DatabaseName=self.timestream_database,
                    TableName=self.timestream_table,
                    Records=batch
                )
            
            logging.info(f"Stored {len(metrics)} aggregated metrics in TimeStream")
            
        except Exception as e:
            logging.error(f"Failed to store aggregated metrics: {str(e)}")
    
    async def generate_metric_summary(self, time_range: Tuple[datetime, datetime]) -> Dict[str, Any]:
        """Generate summary statistics for metrics"""
        try:
            start_time, end_time = time_range
            
            # Query aggregated metrics from TimeStream
            query = f"""
            SELECT 
                MetricName,
                AVG(value) as avg_value,
                MIN(value) as min_value,
                MAX(value) as max_value,
                COUNT(*) as sample_count
            FROM "{self.timestream_database}"."{self.timestream_table}"
            WHERE time BETWEEN '{start_time.isoformat()}' AND '{end_time.isoformat()}'
            GROUP BY MetricName
            ORDER BY MetricName
            """
            
            # Execute query (simplified - would use actual TimeStream query)
            summary = {
                'time_range': {
                    'start': start_time.isoformat(),
                    'end': end_time.isoformat()
                },
                'metrics_summary': {
                    'total_metrics': len(self.metric_definitions),
                    'active_metrics': len([d for d in self.metric_definitions.values()]),
                    'aggregation_types': list(set(d.aggregation_type.value for d in self.metric_definitions.values()))
                }
            }
            
            return summary
            
        except Exception as e:
            logging.error(f"Failed to generate metric summary: {str(e)}")
            return {}

# Usage example
async def main():
    config = {
        'timestream_database': 'MetricsDB',
        'timestream_table': 'AggregatedMetrics'
    }
    
    # Initialize aggregation engine
    aggregation_engine = MetricsAggregationEngine(config)
    
    # Define metrics for aggregation
    request_count_definition = MetricDefinition(
        metric_name='RequestCount',
        source_metrics=['HTTPRequests'],
        aggregation_type=AggregationType.SUM,
        time_windows=[TimeWindow.MINUTE, TimeWindow.HOUR, TimeWindow.DAY],
        dimensions=['Service', 'Environment', 'Region'],
        filters={'StatusCode': [200, 201, 202]}
    )
    
    response_time_definition = MetricDefinition(
        metric_name='ResponseTimeP95',
        source_metrics=['ResponseTime'],
        aggregation_type=AggregationType.PERCENTILE,
        time_windows=[TimeWindow.FIVE_MINUTES, TimeWindow.HOUR],
        dimensions=['Service', 'Environment'],
        filters={},
        percentile_value=95.0
    )
    
    error_count_definition = MetricDefinition(
        metric_name='ErrorCount',
        source_metrics=['HTTPRequests'],
        aggregation_type=AggregationType.COUNT,
        time_windows=[TimeWindow.MINUTE, TimeWindow.HOUR],
        dimensions=['Service', 'Environment'],
        filters={'StatusCode': [400, 401, 403, 404, 500, 502, 503, 504]}
    )
    
    # Register metric definitions
    aggregation_engine.register_metric_definition(request_count_definition)
    aggregation_engine.register_metric_definition(response_time_definition)
    aggregation_engine.register_metric_definition(error_count_definition)
    
    # Simulate raw metrics data
    raw_metrics = [
        {
            'MetricName': 'RequestCount',
            'Value': 100,
            'Timestamp': datetime.utcnow(),
            'Service': 'web-api',
            'Environment': 'production',
            'Region': 'us-east-1',
            'StatusCode': 200
        },
        {
            'MetricName': 'ResponseTime',
            'Value': 250.5,
            'Timestamp': datetime.utcnow(),
            'Service': 'web-api',
            'Environment': 'production'
        }
    ]
    
    # Process metrics
    aggregated_metrics = await aggregation_engine.process_raw_metrics(raw_metrics)
    print(f"Generated {len(aggregated_metrics)} aggregated metrics")
    
    # Create composite metrics
    composite_metrics = await aggregation_engine.create_composite_metrics(aggregated_metrics)
    print(f"Generated {len(composite_metrics)} composite metrics")
    
    # Store aggregated metrics
    all_metrics = aggregated_metrics + composite_metrics
    await aggregation_engine.store_aggregated_metrics(all_metrics)
    
    # Generate summary
    time_range = (datetime.utcnow() - timedelta(hours=1), datetime.utcnow())
    summary = await aggregation_engine.generate_metric_summary(time_range)
    print(f"Metrics summary: {json.dumps(summary, indent=2)}")

if __name__ == "__main__":
    asyncio.run(main())
```

## AWS Services Used

- **Amazon CloudWatch**: Metrics aggregation, statistical functions, and custom metrics
- **Amazon Timestream**: Time-series database for storing aggregated metrics
- **AWS Lambda**: Serverless functions for real-time metric processing and aggregation
- **Amazon Kinesis Data Analytics**: Stream processing for real-time metric aggregation
- **Amazon Kinesis Data Streams**: Data ingestion for high-volume metric streams
- **Amazon S3**: Long-term storage for historical aggregated metrics
- **Amazon Athena**: SQL queries on historical metric data stored in S3
- **AWS Glue**: ETL jobs for batch metric processing and aggregation
- **Amazon QuickSight**: Business intelligence dashboards for aggregated metrics
- **Amazon OpenSearch**: Search and analytics for metric data exploration
- **AWS Step Functions**: Orchestration of complex metric aggregation workflows
- **Amazon EventBridge**: Event-driven metric processing and aggregation triggers
- **Amazon DynamoDB**: Storage for metric definitions and aggregation rules
- **AWS Systems Manager**: Parameter store for metric configuration management
- **Amazon SNS**: Notifications for metric aggregation status and alerts

## Benefits

- **Actionable Insights**: Transform raw data into meaningful business and technical metrics
- **Improved Performance**: Optimized queries through pre-aggregated data
- **Cost Optimization**: Reduced storage and compute costs through intelligent aggregation
- **Better Decision Making**: Clear KPIs and metrics for informed business decisions
- **Scalable Analytics**: Handle large volumes of metric data efficiently
- **Real-time Monitoring**: Stream processing for immediate metric availability
- **Historical Analysis**: Long-term trend analysis through time-based aggregations
- **Customizable Views**: Flexible aggregation strategies for different stakeholders
- **Data Quality**: Validation and quality checks ensure metric accuracy
- **Operational Efficiency**: Automated aggregation reduces manual data processing

## Related Resources

- [AWS Well-Architected Reliability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/)
- [Define and Calculate Metrics](https://docs.aws.amazon.com/wellarchitected/latest/framework/rel_monitor_aws_resources_notification_aggregation.html)
- [Amazon CloudWatch Metrics](https://docs.aws.amazon.com/cloudwatch/latest/monitoring/working_with_metrics.html)
- [Amazon Timestream User Guide](https://docs.aws.amazon.com/timestream/latest/developerguide/)
- [Amazon Kinesis Data Analytics](https://docs.aws.amazon.com/kinesisanalytics/latest/dev/)
- [AWS Lambda for Data Processing](https://docs.aws.amazon.com/lambda/latest/dg/lambda-services.html)
- [Amazon QuickSight User Guide](https://docs.aws.amazon.com/quicksight/latest/user/)
- [Metrics Aggregation Patterns](https://aws.amazon.com/blogs/mt/create-a-metric-filter-and-alarm-on-amazon-cloudwatch-logs/)
- [Time Series Analytics](https://aws.amazon.com/blogs/big-data/analyzing-time-series-data-with-apache-spark-and-amazon-emr/)
- [AWS Glue ETL Jobs](https://docs.aws.amazon.com/glue/latest/dg/author-job.html)
- [Amazon Athena User Guide](https://docs.aws.amazon.com/athena/latest/ug/)
- [Building Analytics Solutions](https://aws.amazon.com/big-data/datalakes-and-analytics/)
