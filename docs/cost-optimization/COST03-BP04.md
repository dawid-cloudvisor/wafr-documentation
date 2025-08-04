---
title: COST03-BP04 - Configure billing and cost management tools
layout: default
parent: COST03 - How do you monitor usage and cost?
grand_parent: Cost Optimization
nav_order: 4
---

<div class="pillar-header">
  <h1>COST03-BP04: Configure billing and cost management tools</h1>
  <p>Configure advanced billing and cost management tools to provide comprehensive cost visibility and enable sophisticated cost analysis. Advanced configuration includes setting up detailed reporting, automated analysis, and integration with business intelligence tools.</p>
</div>

## Implementation guidance

Advanced configuration of billing and cost management tools goes beyond basic setup to provide sophisticated cost analysis capabilities, automated insights, and seamless integration with business processes. This enables organizations to gain deeper insights into their cloud spending patterns and make more informed optimization decisions.

### Advanced Configuration Principles

**Comprehensive Data Collection**: Configure tools to collect the most detailed cost and usage data available, including resource-level information and metadata.

**Automated Analysis**: Set up automated analysis and reporting to reduce manual effort and ensure consistent insights generation.

**Business Integration**: Configure tools to integrate seamlessly with existing business systems and processes for comprehensive cost management.

**Scalable Architecture**: Design configurations that can scale with organizational growth and changing requirements.

### Advanced Tool Capabilities

**Custom Reporting**: Create sophisticated custom reports that combine cost data with business context and operational metrics.

**Predictive Analytics**: Implement forecasting and predictive capabilities to anticipate future costs and identify trends.

**Automated Optimization**: Configure automated identification and implementation of cost optimization opportunities.

**Real-time Monitoring**: Set up near real-time cost monitoring and alerting for immediate visibility into spending changes.

## AWS Services to Consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Cost and Usage Report (CUR)</h4>
    <p>Configure CUR with maximum detail and integrate with analytics platforms. Use CUR data for advanced cost modeling and analysis.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon Athena</h4>
    <p>Query CUR data using SQL for advanced analysis. Create complex cost queries and integrate with business intelligence tools.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon QuickSight</h4>
    <p>Create advanced dashboards and visualizations. Implement machine learning insights and automated anomaly detection.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Glue</h4>
    <p>Process and transform cost data for advanced analytics. Create data pipelines that combine cost data with business data.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon Redshift</h4>
    <p>Store and analyze large volumes of cost data. Create data warehouses that combine cost data with business intelligence.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Lambda</h4>
    <p>Implement custom cost analysis functions and automated responses. Create serverless cost management workflows.</p>
  </div>
</div>

## Implementation Steps

### 1. Design Advanced Architecture
- Plan data flow from cost tools to analytics platforms
- Design integration points with business systems
- Plan for scalability and performance requirements
- Design security and access control for advanced tools

### 2. Configure Advanced Data Collection
- Set up CUR with maximum detail and frequency
- Configure additional data sources and integrations
- Implement data validation and quality assurance
- Set up automated data processing pipelines

### 3. Implement Analytics Platform
- Set up data warehouse or analytics platform
- Configure data transformation and enrichment
- Implement advanced querying and analysis capabilities
- Create machine learning models for cost insights

### 4. Build Advanced Dashboards
- Create role-specific advanced dashboards
- Implement interactive analysis capabilities
- Set up automated report generation and distribution
- Configure advanced alerting and notification systems

### 5. Integrate with Business Systems
- Connect cost tools with ERP and financial systems
- Implement automated data synchronization
- Create APIs for custom integrations
- Set up workflow automation for cost management processes

### 6. Enable Self-Service Analytics
- Create self-service analytics capabilities for users
- Implement data governance and access controls
- Provide training and documentation for advanced features
- Set up support processes for advanced tool usage

## Advanced CUR Configuration

### Comprehensive CUR Setup
```yaml
# CloudFormation template for advanced CUR configuration
Resources:
  CostAndUsageReport:
    Type: AWS::CUR::ReportDefinition
    Properties:
      ReportName: "comprehensive-cost-usage-report"
      TimeUnit: "HOURLY"
      Format: "Parquet"
      Compression: "GZIP"
      AdditionalSchemaElements:
        - "RESOURCES"
        - "SPLIT_COST_ALLOCATION_DATA"
        - "MANUAL_DISCOUNT_COMPATIBILITY"
      AdditionalArtifacts:
        - "REDSHIFT"
        - "QUICKSIGHT"
        - "ATHENA"
      RefreshClosedReports: true
      ReportVersioning: "OVERWRITE_REPORT"
      S3Bucket: !Ref CostDataBucket
      S3Prefix: "cur-reports/"
      S3Region: !Ref AWS::Region
      
  CostDataBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub "${AWS::StackName}-cost-data-${AWS::AccountId}"
      VersioningConfiguration:
        Status: Enabled
      LifecycleConfiguration:
        Rules:
          - Id: CostDataLifecycle
            Status: Enabled
            Transitions:
              - TransitionInDays: 30
                StorageClass: STANDARD_IA
              - TransitionInDays: 90
                StorageClass: GLACIER
              - TransitionInDays: 365
                StorageClass: DEEP_ARCHIVE
                
  CostDataProcessingRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: glue.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole
      Policies:
        - PolicyName: CostDataAccess
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - s3:GetObject
                  - s3:PutObject
                  - s3:DeleteObject
                  - s3:ListBucket
                Resource:
                  - !Sub "${CostDataBucket}/*"
                  - !GetAtt CostDataBucket.Arn
```

### Advanced Data Processing Pipeline
```python
import boto3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

class AdvancedCostAnalyzer:
    def __init__(self):
        self.s3 = boto3.client('s3')
        self.athena = boto3.client('athena')
        self.glue = boto3.client('glue')
        self.quicksight = boto3.client('quicksight')
        
    def process_cur_data_advanced(self, bucket, prefix):
        """Advanced processing of CUR data with business context"""
        
        # Query CUR data using Athena
        query = """
        SELECT 
            line_item_usage_account_id,
            product_product_name,
            line_item_resource_id,
            line_item_usage_start_date,
            line_item_usage_end_date,
            line_item_blended_cost,
            line_item_unblended_cost,
            line_item_usage_amount,
            resource_tags_user_environment,
            resource_tags_user_project,
            resource_tags_user_business_unit,
            resource_tags_user_cost_center,
            pricing_term,
            product_instance_type,
            product_region
        FROM cur_table
        WHERE line_item_usage_start_date >= date_add('day', -30, current_date)
        AND line_item_blended_cost > 0
        """
        
        # Execute Athena query
        query_execution = self.athena.start_query_execution(
            QueryString=query,
            QueryExecutionContext={'Database': 'cost_database'},
            ResultConfiguration={
                'OutputLocation': f's3://{bucket}/athena-results/'
            }
        )
        
        # Wait for query completion and get results
        results = self.wait_for_query_completion(query_execution['QueryExecutionId'])
        
        # Process results with advanced analytics
        processed_data = self.apply_advanced_analytics(results)
        
        return processed_data
    
    def apply_advanced_analytics(self, raw_data):
        """Apply advanced analytics to cost data"""
        
        df = pd.DataFrame(raw_data)
        
        # Calculate advanced metrics
        analytics = {
            'cost_trends': self.calculate_cost_trends(df),
            'anomaly_detection': self.detect_cost_anomalies(df),
            'optimization_opportunities': self.identify_optimization_opportunities(df),
            'predictive_forecasting': self.generate_cost_forecasts(df),
            'business_impact_analysis': self.analyze_business_impact(df)
        }
        
        return analytics
    
    def calculate_cost_trends(self, df):
        """Calculate sophisticated cost trends and patterns"""
        
        # Daily cost trends
        daily_costs = df.groupby('line_item_usage_start_date')['line_item_blended_cost'].sum()
        
        # Calculate trend metrics
        trends = {
            'daily_average': daily_costs.mean(),
            'growth_rate': self.calculate_growth_rate(daily_costs),
            'volatility': daily_costs.std(),
            'seasonal_patterns': self.detect_seasonal_patterns(daily_costs),
            'trend_direction': self.determine_trend_direction(daily_costs)
        }
        
        return trends
    
    def detect_cost_anomalies(self, df):
        """Advanced anomaly detection using statistical methods"""
        
        # Group by service and calculate anomalies
        service_costs = df.groupby(['product_product_name', 'line_item_usage_start_date'])['line_item_blended_cost'].sum().reset_index()
        
        anomalies = []
        
        for service in service_costs['product_product_name'].unique():
            service_data = service_costs[service_costs['product_product_name'] == service]
            
            # Calculate statistical thresholds
            mean_cost = service_data['line_item_blended_cost'].mean()
            std_cost = service_data['line_item_blended_cost'].std()
            threshold = mean_cost + (2 * std_cost)  # 2 standard deviations
            
            # Identify anomalies
            service_anomalies = service_data[service_data['line_item_blended_cost'] > threshold]
            
            for _, anomaly in service_anomalies.iterrows():
                anomalies.append({
                    'service': service,
                    'date': anomaly['line_item_usage_start_date'],
                    'cost': anomaly['line_item_blended_cost'],
                    'expected_cost': mean_cost,
                    'deviation': anomaly['line_item_blended_cost'] - mean_cost,
                    'severity': 'high' if anomaly['line_item_blended_cost'] > threshold * 1.5 else 'medium'
                })
        
        return anomalies
    
    def identify_optimization_opportunities(self, df):
        """Identify specific cost optimization opportunities"""
        
        opportunities = []
        
        # Right-sizing opportunities
        rightsizing_opps = self.analyze_rightsizing_opportunities(df)
        opportunities.extend(rightsizing_opps)
        
        # Reserved Instance opportunities
        ri_opps = self.analyze_reserved_instance_opportunities(df)
        opportunities.extend(ri_opps)
        
        # Storage optimization opportunities
        storage_opps = self.analyze_storage_optimization_opportunities(df)
        opportunities.extend(storage_opps)
        
        # Unused resource opportunities
        unused_opps = self.analyze_unused_resources(df)
        opportunities.extend(unused_opps)
        
        return opportunities
    
    def generate_cost_forecasts(self, df):
        """Generate predictive cost forecasts"""
        
        # Prepare time series data
        daily_costs = df.groupby('line_item_usage_start_date')['line_item_blended_cost'].sum().sort_index()
        
        # Simple linear regression forecast (can be enhanced with more sophisticated models)
        from sklearn.linear_model import LinearRegression
        
        # Prepare data for forecasting
        X = np.array(range(len(daily_costs))).reshape(-1, 1)
        y = daily_costs.values
        
        # Train model
        model = LinearRegression()
        model.fit(X, y)
        
        # Generate forecasts for next 30 days
        future_X = np.array(range(len(daily_costs), len(daily_costs) + 30)).reshape(-1, 1)
        forecasts = model.predict(future_X)
        
        return {
            'next_30_days': forecasts.tolist(),
            'trend_slope': model.coef_[0],
            'confidence_interval': self.calculate_confidence_interval(forecasts, daily_costs.std())
        }
    
    def create_advanced_dashboard(self, analytics_data):
        """Create advanced QuickSight dashboard"""
        
        # Create QuickSight data source
        data_source_response = self.quicksight.create_data_source(
            AwsAccountId=boto3.client('sts').get_caller_identity()['Account'],
            DataSourceId='advanced-cost-analytics',
            Name='Advanced Cost Analytics',
            Type='ATHENA',
            DataSourceParameters={
                'AthenaParameters': {
                    'WorkGroup': 'primary'
                }
            }
        )
        
        # Create dataset
        dataset_response = self.quicksight.create_data_set(
            AwsAccountId=boto3.client('sts').get_caller_identity()['Account'],
            DataSetId='cost-analytics-dataset',
            Name='Cost Analytics Dataset',
            PhysicalTableMap={
                'cost-table': {
                    'RelationalTable': {
                        'DataSourceArn': data_source_response['Arn'],
                        'Schema': 'cost_database',
                        'Name': 'cur_table',
                        'InputColumns': [
                            {'Name': 'line_item_usage_account_id', 'Type': 'STRING'},
                            {'Name': 'product_product_name', 'Type': 'STRING'},
                            {'Name': 'line_item_blended_cost', 'Type': 'DECIMAL'},
                            {'Name': 'line_item_usage_start_date', 'Type': 'DATETIME'},
                            {'Name': 'resource_tags_user_environment', 'Type': 'STRING'},
                            {'Name': 'resource_tags_user_business_unit', 'Type': 'STRING'}
                        ]
                    }
                }
            }
        )
        
        # Create analysis with advanced visualizations
        analysis_response = self.quicksight.create_analysis(
            AwsAccountId=boto3.client('sts').get_caller_identity()['Account'],
            AnalysisId='advanced-cost-analysis',
            Name='Advanced Cost Analysis',
            Definition={
                'DataSetIdentifierDeclarations': [
                    {
                        'DataSetArn': dataset_response['Arn'],
                        'Identifier': 'cost-data'
                    }
                ],
                'Sheets': [
                    {
                        'SheetId': 'cost-trends-sheet',
                        'Name': 'Cost Trends',
                        'Visuals': [
                            {
                                'LineChartVisual': {
                                    'VisualId': 'cost-trend-line',
                                    'Title': {'Visibility': 'VISIBLE', 'Label': 'Cost Trends Over Time'},
                                    'FieldWells': {
                                        'LineChartAggregatedFieldWells': {
                                            'Category': [
                                                {
                                                    'DateDimensionField': {
                                                        'FieldId': 'date-field',
                                                        'Column': {
                                                            'DataSetIdentifier': 'cost-data',
                                                            'ColumnName': 'line_item_usage_start_date'
                                                        }
                                                    }
                                                }
                                            ],
                                            'Values': [
                                                {
                                                    'NumericalMeasureField': {
                                                        'FieldId': 'cost-field',
                                                        'Column': {
                                                            'DataSetIdentifier': 'cost-data',
                                                            'ColumnName': 'line_item_blended_cost'
                                                        },
                                                        'AggregationFunction': {'SimpleNumericalAggregation': 'SUM'}
                                                    }
                                                }
                                            ]
                                        }
                                    }
                                }
                            }
                        ]
                    }
                ]
            }
        )
        
        return analysis_response
```

## Advanced Monitoring and Alerting

### Real-time Cost Monitoring
```python
def setup_realtime_cost_monitoring():
    """Set up real-time cost monitoring with advanced alerting"""
    
    # Create CloudWatch custom metrics for real-time cost tracking
    cloudwatch = boto3.client('cloudwatch')
    
    # Lambda function for real-time cost calculation
    lambda_code = '''
import boto3
import json
from datetime import datetime, timedelta

def lambda_handler(event, context):
    """Calculate and publish real-time cost metrics"""
    
    # Get current hour cost data
    ce_client = boto3.client('ce')
    cloudwatch = boto3.client('cloudwatch')
    
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=1)
    
    # Get hourly cost data
    response = ce_client.get_cost_and_usage(
        TimePeriod={
            'Start': start_time.strftime('%Y-%m-%d'),
            'End': end_time.strftime('%Y-%m-%d')
        },
        Granularity='HOURLY',
        Metrics=['BlendedCost'],
        GroupBy=[
            {'Type': 'DIMENSION', 'Key': 'SERVICE'},
            {'Type': 'TAG', 'Key': 'Environment'}
        ]
    )
    
    # Process and publish metrics
    for result in response['ResultsByTime']:
        for group in result['Groups']:
            service = group['Keys'][0]
            environment = group['Keys'][1] if len(group['Keys']) > 1 else 'Unknown'
            cost = float(group['Metrics']['BlendedCost']['Amount'])
            
            # Publish custom metric
            cloudwatch.put_metric_data(
                Namespace='AWS/CostManagement/RealTime',
                MetricData=[
                    {
                        'MetricName': 'HourlyCost',
                        'Dimensions': [
                            {'Name': 'Service', 'Value': service},
                            {'Name': 'Environment', 'Value': environment}
                        ],
                        'Value': cost,
                        'Unit': 'None',
                        'Timestamp': datetime.now()
                    }
                ]
            )
    
    return {'statusCode': 200}
'''
    
    # Create Lambda function
    lambda_client = boto3.client('lambda')
    
    try:
        lambda_client.create_function(
            FunctionName='RealTimeCostMonitoring',
            Runtime='python3.9',
            Role='arn:aws:iam::ACCOUNT:role/CostMonitoringRole',
            Handler='lambda_function.lambda_handler',
            Code={'ZipFile': lambda_code.encode()},
            Description='Real-time cost monitoring and alerting'
        )
        
        # Set up hourly execution
        events_client = boto3.client('events')
        
        events_client.put_rule(
            Name='HourlyCostMonitoring',
            ScheduleExpression='rate(1 hour)',
            Description='Trigger hourly cost monitoring'
        )
        
        events_client.put_targets(
            Rule='HourlyCostMonitoring',
            Targets=[
                {
                    'Id': '1',
                    'Arn': f'arn:aws:lambda:REGION:ACCOUNT:function:RealTimeCostMonitoring'
                }
            ]
        )
        
        print("Set up real-time cost monitoring")
        
    except Exception as e:
        print(f"Error setting up real-time monitoring: {str(e)}")

def create_advanced_cost_alarms():
    """Create sophisticated cost alarms with multiple conditions"""
    
    cloudwatch = boto3.client('cloudwatch')
    
    # Composite alarm for multiple cost conditions
    cloudwatch.put_composite_alarm(
        AlarmName='ComprehensiveCostAlert',
        AlarmRule=(
            "ALARM('HighHourlyCost') OR "
            "ALARM('AnomalousSpendPattern') OR "
            "ALARM('BudgetThresholdExceeded')"
        ),
        ActionsEnabled=True,
        AlarmActions=[
            'arn:aws:sns:REGION:ACCOUNT:critical-cost-alerts'
        ],
        AlarmDescription='Comprehensive cost monitoring with multiple conditions'
    )
    
    # Individual component alarms
    alarms = [
        {
            'AlarmName': 'HighHourlyCost',
            'MetricName': 'HourlyCost',
            'Threshold': 1000.0,
            'ComparisonOperator': 'GreaterThanThreshold'
        },
        {
            'AlarmName': 'AnomalousSpendPattern',
            'MetricName': 'CostAnomaly',
            'Threshold': 2.0,  # 2 standard deviations
            'ComparisonOperator': 'GreaterThanThreshold'
        },
        {
            'AlarmName': 'BudgetThresholdExceeded',
            'MetricName': 'BudgetUtilization',
            'Threshold': 90.0,  # 90% of budget
            'ComparisonOperator': 'GreaterThanThreshold'
        }
    ]
    
    for alarm in alarms:
        cloudwatch.put_metric_alarm(
            AlarmName=alarm['AlarmName'],
            ComparisonOperator=alarm['ComparisonOperator'],
            EvaluationPeriods=1,
            MetricName=alarm['MetricName'],
            Namespace='AWS/CostManagement/Advanced',
            Period=3600,  # 1 hour
            Statistic='Sum',
            Threshold=alarm['Threshold'],
            ActionsEnabled=True,
            AlarmActions=[
                'arn:aws:sns:REGION:ACCOUNT:cost-alerts'
            ]
        )
```

## Business Intelligence Integration

### ERP System Integration
```python
def integrate_with_erp_system():
    """Integrate cost data with ERP system for comprehensive financial reporting"""
    
    # Example integration with SAP or similar ERP system
    class ERPIntegration:
        def __init__(self, erp_endpoint, credentials):
            self.erp_endpoint = erp_endpoint
            self.credentials = credentials
            
        def sync_cost_data(self, cost_data):
            """Sync AWS cost data with ERP system"""
            
            # Transform cost data to ERP format
            erp_data = self.transform_to_erp_format(cost_data)
            
            # Send data to ERP system
            response = self.send_to_erp(erp_data)
            
            return response
        
        def transform_to_erp_format(self, cost_data):
            """Transform AWS cost data to ERP-compatible format"""
            
            erp_records = []
            
            for record in cost_data:
                erp_record = {
                    'cost_center': record.get('cost_center', 'IT-CLOUD'),
                    'account_code': self.map_service_to_account_code(record['service']),
                    'amount': record['cost'],
                    'currency': 'USD',
                    'transaction_date': record['date'],
                    'description': f"AWS {record['service']} - {record.get('environment', 'Unknown')}",
                    'project_code': record.get('project', ''),
                    'department': record.get('business_unit', 'IT')
                }
                erp_records.append(erp_record)
            
            return erp_records
        
        def map_service_to_account_code(self, service):
            """Map AWS services to ERP account codes"""
            
            service_mapping = {
                'Amazon Elastic Compute Cloud - Compute': '6100-COMPUTE',
                'Amazon Simple Storage Service': '6200-STORAGE',
                'Amazon Relational Database Service': '6300-DATABASE',
                'Amazon CloudFront': '6400-CDN',
                'AWS Lambda': '6500-SERVERLESS'
            }
            
            return service_mapping.get(service, '6000-CLOUD-OTHER')
    
    # Initialize ERP integration
    erp = ERPIntegration('https://erp.company.com/api', {'api_key': 'your-api-key'})
    
    # Get cost data and sync with ERP
    cost_data = get_monthly_cost_data()
    erp.sync_cost_data(cost_data)
```

## Common Challenges and Solutions

### Challenge: Data Volume and Performance

**Solution**: Use appropriate data storage and processing technologies. Implement data partitioning and indexing. Use caching for frequently accessed data. Consider using managed analytics services.

### Challenge: Complex Integration Requirements

**Solution**: Design modular integration architecture. Use standard APIs and data formats. Implement robust error handling and retry logic. Create comprehensive testing and validation procedures.

### Challenge: Real-time Processing Requirements

**Solution**: Use streaming data processing technologies. Implement efficient data pipelines. Use appropriate caching and storage strategies. Consider using managed streaming services.

### Challenge: Advanced Analytics Complexity

**Solution**: Start with simple analytics and gradually add complexity. Use managed machine learning services. Implement proper data validation and quality checks. Provide training and documentation for advanced features.

### Challenge: Cost of Advanced Tools

**Solution**: Optimize tool usage and configuration. Use appropriate pricing models and reserved capacity. Monitor tool costs and optimize regularly. Consider open-source alternatives where appropriate.

## Related Resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/cost_monitor_usage_configure_tools.html">AWS Well-Architected Framework - Configure billing and cost management tools</a></li>
    <li><a href="https://docs.aws.amazon.com/cur/latest/userguide/what-is-cur.html">AWS Cost and Usage Report User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/athena/latest/ug/what-is.html">Amazon Athena User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/quicksight/latest/user/welcome.html">Amazon QuickSight User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/glue/latest/dg/what-is-glue.html">AWS Glue Developer Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/redshift/latest/mgmt/welcome.html">Amazon Redshift Management Guide</a></li>
    <li><a href="https://aws.amazon.com/blogs/aws-cost-management/">AWS Cost Management Blog</a></li>
    <li><a href="https://docs.aws.amazon.com/lambda/latest/dg/welcome.html">AWS Lambda Developer Guide</a></li>
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
