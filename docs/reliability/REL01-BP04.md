---
title: REL01-BP04 - Monitor and manage quotas
layout: default
parent: REL01 - How do you manage service quotas and constraints?
grand_parent: Reliability
nav_order: 4
---

# REL01-BP04: Monitor and manage quotas

## Overview

Continuously monitor service quotas and usage patterns to proactively manage capacity and prevent service disruptions. Implement automated monitoring, alerting, and quota management processes to maintain optimal resource availability across your AWS environment.

## Implementation Steps

### 1. Implement Comprehensive Quota Monitoring
- Deploy automated quota monitoring across all AWS services and regions
- Set up real-time usage tracking with configurable alert thresholds
- Create centralized quota dashboards for visibility and management
- Establish baseline usage patterns and growth trend analysis

### 2. Configure Proactive Alerting Systems
- Set up multi-tier alerting at 70%, 80%, and 90% quota utilization
- Implement escalation procedures for critical quota breaches
- Configure automated notifications to relevant teams and stakeholders
- Create runbooks for quota management response procedures

### 3. Automate Quota Increase Requests
- Implement automated quota increase request workflows
- Set up approval processes for quota modifications
- Create trend-based predictive quota management
- Establish emergency quota increase procedures

### 4. Establish Cross-Account and Cross-Region Coordination
- Implement centralized quota management for multi-account environments
- Set up cross-region quota monitoring and coordination
- Create quota sharing and pooling strategies where applicable
- Establish disaster recovery quota pre-warming procedures

### 5. Integrate with Infrastructure Automation
- Embed quota checks in CI/CD pipelines and infrastructure deployment
- Implement quota-aware resource provisioning
- Create automated quota validation for infrastructure changes
- Set up quota impact assessment for new deployments

### 6. Maintain Quota Governance and Optimization
- Establish quota review and optimization processes
- Implement cost-aware quota management strategies
- Create quota utilization reporting and analytics
- Maintain quota documentation and change management

## Implementation Examples

### Example 1: Advanced Quota Monitoring and Management System

```python
import boto3
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass
import asyncio
import aiohttp

@dataclass
class QuotaAlert:
    service_code: str
    quota_code: str
    region: str
    current_usage: float
    quota_value: float
    utilization_percentage: float
    alert_level: str
    timestamp: datetime

class AdvancedQuotaMonitor:
    def __init__(self, config: Dict):
        self.config = config
        self.service_quotas = boto3.client('service-quotas')
        self.cloudwatch = boto3.client('cloudwatch')
        self.sns = boto3.client('sns')
        self.dynamodb = boto3.resource('dynamodb')
        self.quota_table = self.dynamodb.Table(config['quota_table_name'])
        self.alert_thresholds = config.get('alert_thresholds', [70, 80, 90])
        
    async def monitor_all_quotas(self) -> List[QuotaAlert]:
        """Monitor quotas across all services and regions"""
        alerts = []
        
        # Get all AWS regions
        ec2 = boto3.client('ec2')
        regions = [region['RegionName'] for region in ec2.describe_regions()['Regions']]
        
        # Monitor quotas in parallel across regions
        tasks = []
        for region in regions:
            task = self.monitor_region_quotas(region)
            tasks.append(task)
            
        region_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in region_results:
            if isinstance(result, list):
                alerts.extend(result)
                
        return alerts
    
    async def monitor_region_quotas(self, region: str) -> List[QuotaAlert]:
        """Monitor quotas for a specific region"""
        alerts = []
        
        try:
            # Create region-specific clients
            regional_quotas = boto3.client('service-quotas', region_name=region)
            regional_cloudwatch = boto3.client('cloudwatch', region_name=region)
            
            # Get all services with quotas
            services = regional_quotas.list_services()['Services']
            
            for service in services:
                service_code = service['ServiceCode']
                service_alerts = await self.monitor_service_quotas(
                    regional_quotas, regional_cloudwatch, service_code, region
                )
                alerts.extend(service_alerts)
                
        except Exception as e:
            logging.error(f"Error monitoring region {region}: {str(e)}")
            
        return alerts
    
    async def monitor_service_quotas(self, quotas_client, cloudwatch_client, 
                                   service_code: str, region: str) -> List[QuotaAlert]:
        """Monitor quotas for a specific service"""
        alerts = []
        
        try:
            # Get all quotas for the service
            paginator = quotas_client.get_paginator('list_service_quotas')
            
            for page in paginator.paginate(ServiceCode=service_code):
                for quota in page['Quotas']:
                    quota_code = quota['QuotaCode']
                    quota_value = quota['Value']
                    
                    # Get current usage
                    current_usage = await self.get_quota_usage(
                        cloudwatch_client, service_code, quota_code, region
                    )
                    
                    if current_usage is not None:
                        utilization = (current_usage / quota_value) * 100
                        
                        # Check if alert threshold is exceeded
                        for threshold in self.alert_thresholds:
                            if utilization >= threshold:
                                alert = QuotaAlert(
                                    service_code=service_code,
                                    quota_code=quota_code,
                                    region=region,
                                    current_usage=current_usage,
                                    quota_value=quota_value,
                                    utilization_percentage=utilization,
                                    alert_level=self.get_alert_level(utilization),
                                    timestamp=datetime.utcnow()
                                )
                                alerts.append(alert)
                                break
                                
                        # Store quota data for trend analysis
                        await self.store_quota_data(quota, current_usage, region)
                        
        except Exception as e:
            logging.error(f"Error monitoring service {service_code} in {region}: {str(e)}")
            
        return alerts
    
    async def get_quota_usage(self, cloudwatch_client, service_code: str, 
                            quota_code: str, region: str) -> Optional[float]:
        """Get current usage for a quota using CloudWatch metrics"""
        try:
            # Map service codes to CloudWatch metrics
            metric_mapping = self.get_metric_mapping(service_code, quota_code)
            
            if not metric_mapping:
                return None
                
            response = cloudwatch_client.get_metric_statistics(
                Namespace=metric_mapping['namespace'],
                MetricName=metric_mapping['metric_name'],
                Dimensions=metric_mapping.get('dimensions', []),
                StartTime=datetime.utcnow() - timedelta(minutes=5),
                EndTime=datetime.utcnow(),
                Period=300,
                Statistics=['Maximum']
            )
            
            if response['Datapoints']:
                return max(dp['Maximum'] for dp in response['Datapoints'])
                
        except Exception as e:
            logging.error(f"Error getting usage for {service_code}/{quota_code}: {str(e)}")
            
        return None
    
    def get_metric_mapping(self, service_code: str, quota_code: str) -> Optional[Dict]:
        """Map service quotas to CloudWatch metrics"""
        mappings = {
            'ec2': {
                'L-1216C47A': {  # Running On-Demand instances
                    'namespace': 'AWS/EC2',
                    'metric_name': 'RunningInstances',
                    'dimensions': []
                }
            },
            'lambda': {
                'L-B99A9384': {  # Concurrent executions
                    'namespace': 'AWS/Lambda',
                    'metric_name': 'ConcurrentExecutions',
                    'dimensions': []
                }
            },
            'rds': {
                'L-7B6409FD': {  # DB instances
                    'namespace': 'AWS/RDS',
                    'metric_name': 'DatabaseConnections',
                    'dimensions': []
                }
            }
        }
        
        return mappings.get(service_code, {}).get(quota_code)
    
    async def store_quota_data(self, quota: Dict, current_usage: float, region: str):
        """Store quota data for trend analysis"""
        try:
            item = {
                'quota_id': f"{quota['ServiceCode']}#{quota['QuotaCode']}#{region}",
                'timestamp': int(datetime.utcnow().timestamp()),
                'service_code': quota['ServiceCode'],
                'quota_code': quota['QuotaCode'],
                'region': region,
                'quota_name': quota['QuotaName'],
                'quota_value': quota['Value'],
                'current_usage': current_usage,
                'utilization_percentage': (current_usage / quota['Value']) * 100,
                'ttl': int((datetime.utcnow() + timedelta(days=90)).timestamp())
            }
            
            self.quota_table.put_item(Item=item)
            
        except Exception as e:
            logging.error(f"Error storing quota data: {str(e)}")
    
    def get_alert_level(self, utilization: float) -> str:
        """Determine alert level based on utilization"""
        if utilization >= 90:
            return 'CRITICAL'
        elif utilization >= 80:
            return 'WARNING'
        elif utilization >= 70:
            return 'INFO'
        return 'OK'
    
    async def send_alerts(self, alerts: List[QuotaAlert]):
        """Send alerts for quota violations"""
        for alert in alerts:
            await self.send_alert(alert)
    
    async def send_alert(self, alert: QuotaAlert):
        """Send individual alert"""
        try:
            message = {
                'alert_level': alert.alert_level,
                'service': alert.service_code,
                'quota': alert.quota_code,
                'region': alert.region,
                'utilization': alert.utilization_percentage,
                'current_usage': alert.current_usage,
                'quota_value': alert.quota_value,
                'timestamp': alert.timestamp.isoformat()
            }
            
            # Send SNS notification
            self.sns.publish(
                TopicArn=self.config['alert_topic_arn'],
                Message=json.dumps(message),
                Subject=f"Quota Alert: {alert.service_code} {alert.alert_level}"
            )
            
            # Send to CloudWatch as custom metric
            self.cloudwatch.put_metric_data(
                Namespace='QuotaMonitoring',
                MetricData=[
                    {
                        'MetricName': 'QuotaUtilization',
                        'Dimensions': [
                            {'Name': 'Service', 'Value': alert.service_code},
                            {'Name': 'Region', 'Value': alert.region},
                            {'Name': 'AlertLevel', 'Value': alert.alert_level}
                        ],
                        'Value': alert.utilization_percentage,
                        'Unit': 'Percent'
                    }
                ]
            )
            
        except Exception as e:
            logging.error(f"Error sending alert: {str(e)}")

# Usage example
async def main():
    config = {
        'quota_table_name': 'quota-monitoring',
        'alert_topic_arn': 'arn:aws:sns:us-east-1:123456789012:quota-alerts',
        'alert_thresholds': [70, 80, 90]
    }
    
    monitor = AdvancedQuotaMonitor(config)
    alerts = await monitor.monitor_all_quotas()
    await monitor.send_alerts(alerts)
    
    print(f"Processed {len(alerts)} quota alerts")

if __name__ == "__main__":
    asyncio.run(main())
```

### Example 2: Automated Quota Increase Management System

```python
import boto3
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import pandas as pd
import numpy as np

class RequestStatus(Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    DENIED = "DENIED"
    CASE_OPENED = "CASE_OPENED"
    CASE_RESOLVED = "CASE_RESOLVED"

@dataclass
class QuotaIncreaseRequest:
    service_code: str
    quota_code: str
    region: str
    current_value: float
    requested_value: float
    justification: str
    priority: str
    status: RequestStatus
    case_id: Optional[str] = None
    created_at: Optional[datetime] = None

class AutomatedQuotaManager:
    def __init__(self, config: Dict):
        self.config = config
        self.service_quotas = boto3.client('service-quotas')
        self.support = boto3.client('support')
        self.dynamodb = boto3.resource('dynamodb')
        self.requests_table = self.dynamodb.Table(config['requests_table_name'])
        self.quota_table = self.dynamodb.Table(config['quota_table_name'])
        
    def analyze_quota_trends(self, service_code: str, quota_code: str, 
                           region: str, days: int = 30) -> Dict:
        """Analyze quota usage trends to predict future needs"""
        try:
            # Query historical data
            response = self.quota_table.query(
                KeyConditionExpression='quota_id = :quota_id',
                FilterExpression='#ts >= :start_time',
                ExpressionAttributeNames={'#ts': 'timestamp'},
                ExpressionAttributeValues={
                    ':quota_id': f"{service_code}#{quota_code}#{region}",
                    ':start_time': int((datetime.utcnow() - timedelta(days=days)).timestamp())
                }
            )
            
            if not response['Items']:
                return {'trend': 'insufficient_data', 'prediction': None}
            
            # Convert to DataFrame for analysis
            df = pd.DataFrame(response['Items'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
            df = df.sort_values('timestamp')
            
            # Calculate trend
            usage_values = df['current_usage'].values
            time_values = np.arange(len(usage_values))
            
            # Linear regression for trend
            coefficients = np.polyfit(time_values, usage_values, 1)
            trend_slope = coefficients[0]
            
            # Predict usage in 30 days
            future_usage = usage_values[-1] + (trend_slope * 30)
            current_quota = df['quota_value'].iloc[-1]
            
            # Calculate growth rate
            if len(usage_values) > 1:
                growth_rate = (usage_values[-1] - usage_values[0]) / usage_values[0] * 100
            else:
                growth_rate = 0
            
            return {
                'trend': 'increasing' if trend_slope > 0 else 'stable',
                'growth_rate': growth_rate,
                'predicted_usage_30d': future_usage,
                'current_quota': current_quota,
                'predicted_utilization_30d': (future_usage / current_quota) * 100,
                'recommendation': self.get_quota_recommendation(
                    future_usage, current_quota, growth_rate
                )
            }
            
        except Exception as e:
            logging.error(f"Error analyzing trends: {str(e)}")
            return {'trend': 'error', 'prediction': None}
    
    def get_quota_recommendation(self, predicted_usage: float, 
                               current_quota: float, growth_rate: float) -> Dict:
        """Generate quota increase recommendation"""
        predicted_utilization = (predicted_usage / current_quota) * 100
        
        if predicted_utilization > 80:
            # Calculate recommended new quota with buffer
            buffer_multiplier = 1.5 if growth_rate > 50 else 1.3
            recommended_quota = predicted_usage * buffer_multiplier
            
            return {
                'action': 'increase_recommended',
                'recommended_value': recommended_quota,
                'priority': 'high' if predicted_utilization > 90 else 'medium',
                'justification': f"Predicted utilization: {predicted_utilization:.1f}%, "
                               f"Growth rate: {growth_rate:.1f}%"
            }
        
        return {'action': 'no_action_needed'}
    
    async def process_quota_recommendations(self) -> List[QuotaIncreaseRequest]:
        """Process quota recommendations and create increase requests"""
        requests = []
        
        try:
            # Get all monitored quotas
            response = self.quota_table.scan()
            quota_items = response['Items']
            
            # Group by quota for trend analysis
            quota_groups = {}
            for item in quota_items:
                key = f"{item['service_code']}#{item['quota_code']}#{item['region']}"
                if key not in quota_groups:
                    quota_groups[key] = []
                quota_groups[key].append(item)
            
            # Analyze each quota group
            for quota_key, items in quota_groups.items():
                service_code, quota_code, region = quota_key.split('#')
                
                # Analyze trends
                trend_analysis = self.analyze_quota_trends(
                    service_code, quota_code, region
                )
                
                recommendation = trend_analysis.get('recommendation', {})
                
                if recommendation.get('action') == 'increase_recommended':
                    # Check if request already exists
                    existing_request = self.get_existing_request(
                        service_code, quota_code, region
                    )
                    
                    if not existing_request:
                        request = QuotaIncreaseRequest(
                            service_code=service_code,
                            quota_code=quota_code,
                            region=region,
                            current_value=trend_analysis['current_quota'],
                            requested_value=recommendation['recommended_value'],
                            justification=recommendation['justification'],
                            priority=recommendation['priority'],
                            status=RequestStatus.PENDING,
                            created_at=datetime.utcnow()
                        )
                        requests.append(request)
            
        except Exception as e:
            logging.error(f"Error processing recommendations: {str(e)}")
        
        return requests
    
    def get_existing_request(self, service_code: str, quota_code: str, 
                           region: str) -> Optional[Dict]:
        """Check if quota increase request already exists"""
        try:
            response = self.requests_table.get_item(
                Key={
                    'request_id': f"{service_code}#{quota_code}#{region}",
                    'status': 'PENDING'
                }
            )
            return response.get('Item')
        except:
            return None
    
    async def submit_quota_increase_request(self, request: QuotaIncreaseRequest) -> bool:
        """Submit quota increase request to AWS"""
        try:
            # Try Service Quotas API first
            try:
                response = self.service_quotas.request_service_quota_increase(
                    ServiceCode=request.service_code,
                    QuotaCode=request.quota_code,
                    DesiredValue=request.requested_value
                )
                
                request.status = RequestStatus.APPROVED
                request.case_id = response.get('RequestedQuota', {}).get('Id')
                
            except self.service_quotas.exceptions.InvalidParameterValueException:
                # Fall back to Support API for quotas that require support cases
                case_response = self.support.create_case(
                    subject=f"Service Quota Increase Request: {request.service_code}",
                    serviceCode='service-limit-increase',
                    severityCode='low',
                    categoryCode='service-limit-increase',
                    communicationBody=self.generate_support_case_body(request),
                    ccEmailAddresses=self.config.get('notification_emails', []),
                    language='en'
                )
                
                request.status = RequestStatus.CASE_OPENED
                request.case_id = case_response['caseId']
            
            # Store request in DynamoDB
            await self.store_quota_request(request)
            
            return True
            
        except Exception as e:
            logging.error(f"Error submitting quota request: {str(e)}")
            request.status = RequestStatus.DENIED
            await self.store_quota_request(request)
            return False
    
    def generate_support_case_body(self, request: QuotaIncreaseRequest) -> str:
        """Generate support case body for quota increase request"""
        return f"""
Service Quota Increase Request

Service: {request.service_code}
Quota Code: {request.quota_code}
Region: {request.region}
Current Limit: {request.current_value}
Requested Limit: {request.requested_value}
Priority: {request.priority}

Justification:
{request.justification}

This request was automatically generated based on usage trend analysis.
Please process this quota increase to prevent service disruptions.

Business Impact:
- Prevents service availability issues
- Supports planned capacity growth
- Maintains application performance standards

Technical Details:
- Usage trends indicate approaching quota limits
- Automated monitoring detected the need for increase
- Request includes appropriate buffer for future growth
        """.strip()
    
    async def store_quota_request(self, request: QuotaIncreaseRequest):
        """Store quota request in DynamoDB"""
        try:
            item = {
                'request_id': f"{request.service_code}#{request.quota_code}#{request.region}",
                'timestamp': int(request.created_at.timestamp()),
                'service_code': request.service_code,
                'quota_code': request.quota_code,
                'region': request.region,
                'current_value': request.current_value,
                'requested_value': request.requested_value,
                'justification': request.justification,
                'priority': request.priority,
                'status': request.status.value,
                'case_id': request.case_id,
                'ttl': int((datetime.utcnow() + timedelta(days=365)).timestamp())
            }
            
            self.requests_table.put_item(Item=item)
            
        except Exception as e:
            logging.error(f"Error storing quota request: {str(e)}")
    
    async def check_request_status(self) -> List[Dict]:
        """Check status of pending quota requests"""
        updates = []
        
        try:
            # Get pending requests
            response = self.requests_table.scan(
                FilterExpression='#status IN (:pending, :case_opened)',
                ExpressionAttributeNames={'#status': 'status'},
                ExpressionAttributeValues={
                    ':pending': 'PENDING',
                    ':case_opened': 'CASE_OPENED'
                }
            )
            
            for item in response['Items']:
                if item.get('case_id'):
                    # Check support case status
                    try:
                        case_response = self.support.describe_cases(
                            caseIdList=[item['case_id']],
                            includeResolvedCases=True
                        )
                        
                        if case_response['cases']:
                            case = case_response['cases'][0]
                            if case['status'] == 'resolved':
                                # Update request status
                                self.requests_table.update_item(
                                    Key={
                                        'request_id': item['request_id'],
                                        'timestamp': item['timestamp']
                                    },
                                    UpdateExpression='SET #status = :status',
                                    ExpressionAttributeNames={'#status': 'status'},
                                    ExpressionAttributeValues={':status': 'CASE_RESOLVED'}
                                )
                                updates.append({
                                    'request_id': item['request_id'],
                                    'old_status': item['status'],
                                    'new_status': 'CASE_RESOLVED'
                                })
                                
                    except Exception as e:
                        logging.error(f"Error checking case status: {str(e)}")
        
        except Exception as e:
            logging.error(f"Error checking request status: {str(e)}")
        
        return updates

# Usage example
async def main():
    config = {
        'requests_table_name': 'quota-requests',
        'quota_table_name': 'quota-monitoring',
        'notification_emails': ['admin@company.com']
    }
    
    manager = AutomatedQuotaManager(config)
    
    # Process recommendations and submit requests
    requests = await manager.process_quota_recommendations()
    
    for request in requests:
        success = await manager.submit_quota_increase_request(request)
        print(f"Request for {request.service_code}/{request.quota_code}: {'Success' if success else 'Failed'}")
    
    # Check status of existing requests
    updates = await manager.check_request_status()
    print(f"Status updates: {len(updates)}")

if __name__ == "__main__":
    asyncio.run(main())
```
### Example 3: CloudFormation Template for Quota Management Infrastructure

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Comprehensive quota monitoring and management infrastructure'

Parameters:
  AlertEmail:
    Type: String
    Description: Email address for quota alerts
    Default: admin@company.com
  
  MonitoringSchedule:
    Type: String
    Description: CloudWatch Events schedule for quota monitoring
    Default: 'rate(5 minutes)'
  
  Environment:
    Type: String
    Description: Environment name
    Default: production
    AllowedValues: [development, staging, production]

Resources:
  # DynamoDB Tables
  QuotaMonitoringTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: !Sub '${Environment}-quota-monitoring'
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: quota_id
          AttributeType: S
        - AttributeName: timestamp
          AttributeType: N
      KeySchema:
        - AttributeName: quota_id
          KeyType: HASH
        - AttributeName: timestamp
          KeyType: RANGE
      TimeToLiveSpecification:
        AttributeName: ttl
        Enabled: true
      StreamSpecification:
        StreamViewType: NEW_AND_OLD_IMAGES
      PointInTimeRecoverySpecification:
        PointInTimeRecoveryEnabled: true

  QuotaRequestsTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: !Sub '${Environment}-quota-requests'
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: request_id
          AttributeType: S
        - AttributeName: timestamp
          AttributeType: N
        - AttributeName: status
          AttributeType: S
      KeySchema:
        - AttributeName: request_id
          KeyType: HASH
        - AttributeName: timestamp
          KeyType: RANGE
      GlobalSecondaryIndexes:
        - IndexName: status-index
          KeySchema:
            - AttributeName: status
              KeyType: HASH
            - AttributeName: timestamp
              KeyType: RANGE
          Projection:
            ProjectionType: ALL
      TimeToLiveSpecification:
        AttributeName: ttl
        Enabled: true

  # SNS Topics
  QuotaAlertTopic:
    Type: AWS::SNS::Topic
    Properties:
      TopicName: !Sub '${Environment}-quota-alerts'
      DisplayName: 'AWS Quota Monitoring Alerts'

  QuotaAlertSubscription:
    Type: AWS::SNS::Subscription
    Properties:
      Protocol: email
      TopicArn: !Ref QuotaAlertTopic
      Endpoint: !Ref AlertEmail

  # IAM Roles
  QuotaMonitoringRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: !Sub '${Environment}-quota-monitoring-role'
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
      Policies:
        - PolicyName: QuotaMonitoringPolicy
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - service-quotas:*
                  - cloudwatch:*
                  - dynamodb:*
                  - sns:Publish
                  - support:*
                  - ec2:DescribeRegions
                  - organizations:ListAccounts
                  - sts:AssumeRole
                Resource: '*'

  # Lambda Functions
  QuotaMonitoringFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: !Sub '${Environment}-quota-monitoring'
      Runtime: python3.9
      Handler: index.lambda_handler
      Role: !GetAtt QuotaMonitoringRole.Arn
      Timeout: 900
      MemorySize: 1024
      Environment:
        Variables:
          QUOTA_TABLE_NAME: !Ref QuotaMonitoringTable
          ALERT_TOPIC_ARN: !Ref QuotaAlertTopic
          ENVIRONMENT: !Ref Environment
      Code:
        ZipFile: |
          import json
          import boto3
          import os
          import asyncio
          from datetime import datetime, timedelta
          
          def lambda_handler(event, context):
              # Import the monitoring class (would be in a layer in practice)
              # This is a simplified version for the template
              
              config = {
                  'quota_table_name': os.environ['QUOTA_TABLE_NAME'],
                  'alert_topic_arn': os.environ['ALERT_TOPIC_ARN'],
                  'alert_thresholds': [70, 80, 90]
              }
              
              # Initialize monitoring
              service_quotas = boto3.client('service-quotas')
              cloudwatch = boto3.client('cloudwatch')
              dynamodb = boto3.resource('dynamodb')
              sns = boto3.client('sns')
              
              # Basic quota monitoring logic
              try:
                  # Get current region quotas
                  services = service_quotas.list_services()['Services']
                  alerts_sent = 0
                  
                  for service in services[:5]:  # Limit for demo
                      service_code = service['ServiceCode']
                      
                      try:
                          quotas = service_quotas.list_service_quotas(
                              ServiceCode=service_code
                          )['Quotas']
                          
                          for quota in quotas[:3]:  # Limit for demo
                              # Store quota data
                              table = dynamodb.Table(config['quota_table_name'])
                              table.put_item(
                                  Item={
                                      'quota_id': f"{service_code}#{quota['QuotaCode']}#{context.invoked_function_arn.split(':')[3]}",
                                      'timestamp': int(datetime.utcnow().timestamp()),
                                      'service_code': service_code,
                                      'quota_code': quota['QuotaCode'],
                                      'quota_name': quota['QuotaName'],
                                      'quota_value': quota['Value'],
                                      'current_usage': 0,  # Would get from CloudWatch
                                      'utilization_percentage': 0,
                                      'ttl': int((datetime.utcnow() + timedelta(days=90)).timestamp())
                                  }
                              )
                              
                      except Exception as e:
                          print(f"Error processing service {service_code}: {str(e)}")
                          continue
                  
                  return {
                      'statusCode': 200,
                      'body': json.dumps({
                          'message': f'Quota monitoring completed',
                          'alerts_sent': alerts_sent
                      })
                  }
                  
              except Exception as e:
                  print(f"Error in quota monitoring: {str(e)}")
                  return {
                      'statusCode': 500,
                      'body': json.dumps({'error': str(e)})
                  }

  QuotaManagerFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: !Sub '${Environment}-quota-manager'
      Runtime: python3.9
      Handler: index.lambda_handler
      Role: !GetAtt QuotaMonitoringRole.Arn
      Timeout: 900
      MemorySize: 1024
      Environment:
        Variables:
          QUOTA_TABLE_NAME: !Ref QuotaMonitoringTable
          REQUESTS_TABLE_NAME: !Ref QuotaRequestsTable
          ALERT_TOPIC_ARN: !Ref QuotaAlertTopic
          ENVIRONMENT: !Ref Environment
      Code:
        ZipFile: |
          import json
          import boto3
          import os
          from datetime import datetime, timedelta
          
          def lambda_handler(event, context):
              # Quota management logic
              config = {
                  'quota_table_name': os.environ['QUOTA_TABLE_NAME'],
                  'requests_table_name': os.environ['REQUESTS_TABLE_NAME'],
                  'alert_topic_arn': os.environ['ALERT_TOPIC_ARN']
              }
              
              service_quotas = boto3.client('service-quotas')
              support = boto3.client('support')
              dynamodb = boto3.resource('dynamodb')
              
              try:
                  # Check for quota increase opportunities
                  quota_table = dynamodb.Table(config['quota_table_name'])
                  requests_table = dynamodb.Table(config['requests_table_name'])
                  
                  # Scan for high utilization quotas
                  response = quota_table.scan(
                      FilterExpression='utilization_percentage > :threshold',
                      ExpressionAttributeValues={':threshold': 80}
                  )
                  
                  requests_created = 0
                  
                  for item in response['Items']:
                      # Check if request already exists
                      request_id = f"{item['service_code']}#{item['quota_code']}#{item.get('region', 'us-east-1')}"
                      
                      try:
                          existing = requests_table.get_item(
                              Key={'request_id': request_id, 'timestamp': int(datetime.utcnow().timestamp())}
                          )
                          
                          if 'Item' not in existing:
                              # Create new request
                              requests_table.put_item(
                                  Item={
                                      'request_id': request_id,
                                      'timestamp': int(datetime.utcnow().timestamp()),
                                      'service_code': item['service_code'],
                                      'quota_code': item['quota_code'],
                                      'current_value': item['quota_value'],
                                      'requested_value': item['quota_value'] * 2,
                                      'justification': f"High utilization: {item['utilization_percentage']}%",
                                      'priority': 'high' if item['utilization_percentage'] > 90 else 'medium',
                                      'status': 'PENDING',
                                      'ttl': int((datetime.utcnow() + timedelta(days=365)).timestamp())
                                  }
                              )
                              requests_created += 1
                              
                      except Exception as e:
                          print(f"Error processing quota request: {str(e)}")
                          continue
                  
                  return {
                      'statusCode': 200,
                      'body': json.dumps({
                          'message': 'Quota management completed',
                          'requests_created': requests_created
                      })
                  }
                  
              except Exception as e:
                  print(f"Error in quota management: {str(e)}")
                  return {
                      'statusCode': 500,
                      'body': json.dumps({'error': str(e)})
                  }

  # EventBridge Rules
  QuotaMonitoringSchedule:
    Type: AWS::Events::Rule
    Properties:
      Name: !Sub '${Environment}-quota-monitoring-schedule'
      Description: 'Schedule for quota monitoring'
      ScheduleExpression: !Ref MonitoringSchedule
      State: ENABLED
      Targets:
        - Arn: !GetAtt QuotaMonitoringFunction.Arn
          Id: QuotaMonitoringTarget

  QuotaManagerSchedule:
    Type: AWS::Events::Rule
    Properties:
      Name: !Sub '${Environment}-quota-manager-schedule'
      Description: 'Schedule for quota management'
      ScheduleExpression: 'rate(1 hour)'
      State: ENABLED
      Targets:
        - Arn: !GetAtt QuotaManagerFunction.Arn
          Id: QuotaManagerTarget

  # Lambda Permissions
  QuotaMonitoringPermission:
    Type: AWS::Lambda::Permission
    Properties:
      FunctionName: !Ref QuotaMonitoringFunction
      Action: lambda:InvokeFunction
      Principal: events.amazonaws.com
      SourceArn: !GetAtt QuotaMonitoringSchedule.Arn

  QuotaManagerPermission:
    Type: AWS::Lambda::Permission
    Properties:
      FunctionName: !Ref QuotaManagerFunction
      Action: lambda:InvokeFunction
      Principal: events.amazonaws.com
      SourceArn: !GetAtt QuotaManagerSchedule.Arn

  # CloudWatch Dashboard
  QuotaDashboard:
    Type: AWS::CloudWatch::Dashboard
    Properties:
      DashboardName: !Sub '${Environment}-quota-monitoring'
      DashboardBody: !Sub |
        {
          "widgets": [
            {
              "type": "metric",
              "x": 0,
              "y": 0,
              "width": 12,
              "height": 6,
              "properties": {
                "metrics": [
                  [ "QuotaMonitoring", "QuotaUtilization", "AlertLevel", "CRITICAL" ],
                  [ ".", ".", ".", "WARNING" ],
                  [ ".", ".", ".", "INFO" ]
                ],
                "view": "timeSeries",
                "stacked": false,
                "region": "${AWS::Region}",
                "title": "Quota Utilization by Alert Level",
                "period": 300
              }
            },
            {
              "type": "metric",
              "x": 12,
              "y": 0,
              "width": 12,
              "height": 6,
              "properties": {
                "metrics": [
                  [ "AWS/Lambda", "Duration", "FunctionName", "${QuotaMonitoringFunction}" ],
                  [ ".", "Errors", ".", "." ],
                  [ ".", "Invocations", ".", "." ]
                ],
                "view": "timeSeries",
                "stacked": false,
                "region": "${AWS::Region}",
                "title": "Quota Monitoring Function Metrics",
                "period": 300
              }
            }
          ]
        }

  # CloudWatch Alarms
  HighQuotaUtilizationAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: !Sub '${Environment}-high-quota-utilization'
      AlarmDescription: 'Alert when quota utilization is high'
      MetricName: QuotaUtilization
      Namespace: QuotaMonitoring
      Statistic: Maximum
      Period: 300
      EvaluationPeriods: 2
      Threshold: 90
      ComparisonOperator: GreaterThanThreshold
      AlarmActions:
        - !Ref QuotaAlertTopic
      Dimensions:
        - Name: AlertLevel
          Value: CRITICAL

Outputs:
  QuotaMonitoringTableName:
    Description: 'Name of the quota monitoring DynamoDB table'
    Value: !Ref QuotaMonitoringTable
    Export:
      Name: !Sub '${Environment}-quota-monitoring-table'

  QuotaRequestsTableName:
    Description: 'Name of the quota requests DynamoDB table'
    Value: !Ref QuotaRequestsTable
    Export:
      Name: !Sub '${Environment}-quota-requests-table'

  AlertTopicArn:
    Description: 'ARN of the quota alert SNS topic'
    Value: !Ref QuotaAlertTopic
    Export:
      Name: !Sub '${Environment}-quota-alert-topic'

  DashboardURL:
    Description: 'URL of the quota monitoring dashboard'
    Value: !Sub 'https://${AWS::Region}.console.aws.amazon.com/cloudwatch/home?region=${AWS::Region}#dashboards:name=${Environment}-quota-monitoring'
```
### Example 4: Multi-Account Quota Coordination System

```bash
#!/bin/bash

# Multi-Account Quota Coordination Script
# Coordinates quota monitoring and management across AWS Organizations

set -euo pipefail

# Configuration
CONFIG_FILE="${CONFIG_FILE:-./quota-config.json}"
LOG_FILE="${LOG_FILE:-./quota-coordination.log}"
TEMP_DIR="${TEMP_DIR:-/tmp/quota-coordination}"

# Logging function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

# Create temporary directory
mkdir -p "$TEMP_DIR"

# Load configuration
if [[ ! -f "$CONFIG_FILE" ]]; then
    log "ERROR: Configuration file $CONFIG_FILE not found"
    exit 1
fi

# Parse configuration
MASTER_ACCOUNT=$(jq -r '.master_account' "$CONFIG_FILE")
REGIONS=($(jq -r '.regions[]' "$CONFIG_FILE"))
SERVICES=($(jq -r '.services[]' "$CONFIG_FILE"))
ALERT_THRESHOLD=$(jq -r '.alert_threshold' "$CONFIG_FILE")

log "Starting multi-account quota coordination"
log "Master Account: $MASTER_ACCOUNT"
log "Regions: ${REGIONS[*]}"
log "Services: ${SERVICES[*]}"

# Function to assume role in target account
assume_role() {
    local account_id="$1"
    local role_name="$2"
    local session_name="quota-coordination-$(date +%s)"
    
    aws sts assume-role \
        --role-arn "arn:aws:iam::${account_id}:role/${role_name}" \
        --role-session-name "$session_name" \
        --output json > "$TEMP_DIR/credentials-${account_id}.json"
    
    if [[ $? -eq 0 ]]; then
        log "Successfully assumed role in account $account_id"
        return 0
    else
        log "ERROR: Failed to assume role in account $account_id"
        return 1
    fi
}

# Function to set credentials from assumed role
set_credentials() {
    local account_id="$1"
    local creds_file="$TEMP_DIR/credentials-${account_id}.json"
    
    if [[ -f "$creds_file" ]]; then
        export AWS_ACCESS_KEY_ID=$(jq -r '.Credentials.AccessKeyId' "$creds_file")
        export AWS_SECRET_ACCESS_KEY=$(jq -r '.Credentials.SecretAccessKey' "$creds_file")
        export AWS_SESSION_TOKEN=$(jq -r '.Credentials.SessionToken' "$creds_file")
        log "Set credentials for account $account_id"
    else
        log "ERROR: Credentials file not found for account $account_id"
        return 1
    fi
}

# Function to clear credentials
clear_credentials() {
    unset AWS_ACCESS_KEY_ID
    unset AWS_SECRET_ACCESS_KEY
    unset AWS_SESSION_TOKEN
}

# Function to get quota utilization for an account
get_account_quotas() {
    local account_id="$1"
    local region="$2"
    local output_file="$TEMP_DIR/quotas-${account_id}-${region}.json"
    
    log "Getting quotas for account $account_id in region $region"
    
    # Initialize output file
    echo '{"account_id": "'$account_id'", "region": "'$region'", "quotas": []}' > "$output_file"
    
    for service in "${SERVICES[@]}"; do
        log "Processing service $service in account $account_id, region $region"
        
        # Get service quotas
        aws service-quotas list-service-quotas \
            --service-code "$service" \
            --region "$region" \
            --output json > "$TEMP_DIR/service-quotas-${service}.json" 2>/dev/null || {
            log "WARNING: Could not get quotas for service $service in region $region"
            continue
        }
        
        # Process each quota
        jq -r '.Quotas[] | @base64' "$TEMP_DIR/service-quotas-${service}.json" | while read -r quota_data; do
            quota=$(echo "$quota_data" | base64 -d)
            quota_code=$(echo "$quota" | jq -r '.QuotaCode')
            quota_name=$(echo "$quota" | jq -r '.QuotaName')
            quota_value=$(echo "$quota" | jq -r '.Value')
            
            # Get current usage (simplified - would use CloudWatch in practice)
            current_usage=0
            utilization=0
            
            # Create quota record
            quota_record=$(jq -n \
                --arg service "$service" \
                --arg quota_code "$quota_code" \
                --arg quota_name "$quota_name" \
                --argjson quota_value "$quota_value" \
                --argjson current_usage "$current_usage" \
                --argjson utilization "$utilization" \
                '{
                    service_code: $service,
                    quota_code: $quota_code,
                    quota_name: $quota_name,
                    quota_value: $quota_value,
                    current_usage: $current_usage,
                    utilization_percentage: $utilization
                }')
            
            # Add to output file
            jq --argjson quota "$quota_record" '.quotas += [$quota]' "$output_file" > "$output_file.tmp"
            mv "$output_file.tmp" "$output_file"
        done
    done
    
    log "Completed quota collection for account $account_id in region $region"
}

# Function to analyze cross-account quota utilization
analyze_cross_account_quotas() {
    local analysis_file="$TEMP_DIR/quota-analysis.json"
    
    log "Analyzing cross-account quota utilization"
    
    # Initialize analysis file
    echo '{"timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'", "analysis": {}}' > "$analysis_file"
    
    # Combine all quota files
    for quota_file in "$TEMP_DIR"/quotas-*.json; do
        if [[ -f "$quota_file" ]]; then
            account_id=$(jq -r '.account_id' "$quota_file")
            region=$(jq -r '.region' "$quota_file")
            
            log "Processing quota data for account $account_id, region $region"
            
            # Process each quota in the file
            jq -r '.quotas[] | @base64' "$quota_file" | while read -r quota_data; do
                quota=$(echo "$quota_data" | base64 -d)
                service_code=$(echo "$quota" | jq -r '.service_code')
                quota_code=$(echo "$quota" | jq -r '.quota_code')
                utilization=$(echo "$quota" | jq -r '.utilization_percentage')
                
                # Check if utilization exceeds threshold
                if (( $(echo "$utilization >= $ALERT_THRESHOLD" | bc -l) )); then
                    log "ALERT: High utilization in account $account_id, region $region, service $service_code, quota $quota_code: ${utilization}%"
                    
                    # Add to analysis
                    alert_record=$(jq -n \
                        --arg account_id "$account_id" \
                        --arg region "$region" \
                        --arg service_code "$service_code" \
                        --arg quota_code "$quota_code" \
                        --argjson utilization "$utilization" \
                        '{
                            account_id: $account_id,
                            region: $region,
                            service_code: $service_code,
                            quota_code: $quota_code,
                            utilization_percentage: $utilization,
                            alert_level: (if $utilization >= 90 then "CRITICAL" elif $utilization >= 80 then "WARNING" else "INFO" end)
                        }')
                    
                    # Add alert to analysis file
                    key="${service_code}_${quota_code}"
                    jq --arg key "$key" --argjson alert "$alert_record" \
                        '.analysis[$key] += [$alert]' "$analysis_file" > "$analysis_file.tmp"
                    mv "$analysis_file.tmp" "$analysis_file"
                fi
            done
        fi
    done
    
    log "Cross-account quota analysis completed"
}

# Function to generate quota coordination recommendations
generate_recommendations() {
    local analysis_file="$TEMP_DIR/quota-analysis.json"
    local recommendations_file="$TEMP_DIR/recommendations.json"
    
    log "Generating quota coordination recommendations"
    
    # Initialize recommendations file
    echo '{"timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'", "recommendations": []}' > "$recommendations_file"
    
    # Process analysis results
    if [[ -f "$analysis_file" ]]; then
        jq -r '.analysis | keys[]' "$analysis_file" | while read -r quota_key; do
            alerts=$(jq -r ".analysis[\"$quota_key\"]" "$analysis_file")
            alert_count=$(echo "$alerts" | jq 'length')
            
            if [[ "$alert_count" -gt 1 ]]; then
                # Multiple accounts affected - recommend coordination
                recommendation=$(jq -n \
                    --arg quota_key "$quota_key" \
                    --argjson alert_count "$alert_count" \
                    --argjson alerts "$alerts" \
                    '{
                        type: "cross_account_coordination",
                        quota_key: $quota_key,
                        affected_accounts: $alert_count,
                        recommendation: "Consider workload redistribution or coordinated quota increases",
                        priority: "high",
                        affected_resources: $alerts
                    }')
                
                jq --argjson rec "$recommendation" '.recommendations += [$rec]' "$recommendations_file" > "$recommendations_file.tmp"
                mv "$recommendations_file.tmp" "$recommendations_file"
                
                log "RECOMMENDATION: Cross-account coordination needed for $quota_key ($alert_count accounts affected)"
            fi
        done
    fi
    
    log "Recommendations generated"
}

# Function to send notifications
send_notifications() {
    local analysis_file="$TEMP_DIR/quota-analysis.json"
    local recommendations_file="$TEMP_DIR/recommendations.json"
    
    log "Sending notifications"
    
    # Check if SNS topic is configured
    SNS_TOPIC=$(jq -r '.sns_topic_arn // empty' "$CONFIG_FILE")
    
    if [[ -n "$SNS_TOPIC" ]]; then
        # Send analysis results
        if [[ -f "$analysis_file" ]]; then
            aws sns publish \
                --topic-arn "$SNS_TOPIC" \
                --subject "Multi-Account Quota Analysis Results" \
                --message file://"$analysis_file" \
                --region us-east-1
            
            log "Sent analysis results to SNS topic"
        fi
        
        # Send recommendations
        if [[ -f "$recommendations_file" ]]; then
            aws sns publish \
                --topic-arn "$SNS_TOPIC" \
                --subject "Multi-Account Quota Recommendations" \
                --message file://"$recommendations_file" \
                --region us-east-1
            
            log "Sent recommendations to SNS topic"
        fi
    else
        log "No SNS topic configured, skipping notifications"
    fi
}

# Main execution
main() {
    log "Starting multi-account quota coordination process"
    
    # Get list of accounts from AWS Organizations
    ACCOUNTS=($(aws organizations list-accounts --query 'Accounts[?Status==`ACTIVE`].Id' --output text))
    
    log "Found ${#ACCOUNTS[@]} active accounts"
    
    # Process each account
    for account_id in "${ACCOUNTS[@]}"; do
        log "Processing account $account_id"
        
        # Skip master account for role assumption
        if [[ "$account_id" == "$MASTER_ACCOUNT" ]]; then
            log "Skipping role assumption for master account"
        else
            # Assume role in target account
            if ! assume_role "$account_id" "QuotaMonitoringRole"; then
                log "Skipping account $account_id due to role assumption failure"
                continue
            fi
            
            set_credentials "$account_id"
        fi
        
        # Process each region
        for region in "${REGIONS[@]}"; do
            get_account_quotas "$account_id" "$region"
        done
        
        # Clear credentials if not master account
        if [[ "$account_id" != "$MASTER_ACCOUNT" ]]; then
            clear_credentials
        fi
    done
    
    # Analyze results
    analyze_cross_account_quotas
    generate_recommendations
    send_notifications
    
    log "Multi-account quota coordination completed"
}

# Configuration file template
create_config_template() {
    cat > quota-config.json << 'EOF'
{
    "master_account": "123456789012",
    "regions": ["us-east-1", "us-west-2", "eu-west-1"],
    "services": ["ec2", "lambda", "rds", "s3"],
    "alert_threshold": 80,
    "sns_topic_arn": "arn:aws:sns:us-east-1:123456789012:quota-alerts"
}
EOF
    log "Created configuration template: quota-config.json"
}

# Command line argument handling
case "${1:-}" in
    "config")
        create_config_template
        ;;
    "run"|"")
        main
        ;;
    *)
        echo "Usage: $0 [config|run]"
        echo "  config - Create configuration template"
        echo "  run    - Run quota coordination (default)"
        exit 1
        ;;
esac

# Cleanup
rm -rf "$TEMP_DIR"
log "Cleanup completed"
```

## AWS Services Used

- **AWS Service Quotas**: Core service for quota monitoring and management
- **Amazon CloudWatch**: Metrics collection and alerting for quota utilization
- **Amazon DynamoDB**: Storage for quota data, trends, and request tracking
- **Amazon SNS**: Notification system for quota alerts and updates
- **AWS Lambda**: Serverless execution of monitoring and management functions
- **Amazon EventBridge**: Scheduling and event-driven quota management
- **AWS Support API**: Automated support case creation for quota increases
- **AWS Organizations**: Multi-account quota coordination and governance
- **AWS Step Functions**: Orchestration of complex quota management workflows
- **Amazon CloudFormation**: Infrastructure as code for quota management systems

## Benefits

- **Proactive Management**: Prevents service disruptions through early quota monitoring
- **Automated Operations**: Reduces manual overhead with automated monitoring and requests
- **Cross-Account Visibility**: Provides centralized view of quota utilization across accounts
- **Trend Analysis**: Enables predictive quota management based on usage patterns
- **Cost Optimization**: Prevents over-provisioning while ensuring adequate capacity
- **Compliance Support**: Maintains audit trails and governance for quota changes
- **Scalable Architecture**: Handles monitoring across multiple accounts and regions
- **Integration Ready**: Works with existing CI/CD and infrastructure automation

## Related Resources

- [AWS Service Quotas User Guide](https://docs.aws.amazon.com/servicequotas/latest/userguide/)
- [AWS Well-Architected Reliability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/)
- [AWS Organizations Best Practices](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_best-practices.html)
- [Amazon CloudWatch User Guide](https://docs.aws.amazon.com/cloudwatch/latest/monitoring/)
- [AWS Support API Reference](https://docs.aws.amazon.com/support/latest/APIReference/)
