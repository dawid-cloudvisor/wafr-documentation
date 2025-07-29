---
title: REL01-BP01 - Aware of service quotas and constraints
layout: default
parent: REL01 - How do you manage service quotas and constraints?
grand_parent: Reliability
nav_order: 1
---

<div class="pillar-header">
  <h1>REL01-BP01: Aware of service quotas and constraints</h1>
  <p>You are aware of your default quotas and quota increase requests for your workload architecture. You additionally understand how quotas apply to your architecture and which quotas are shared across accounts or regions.</p>
</div>

## Implementation guidance

Understanding AWS service quotas and constraints is fundamental to building reliable workloads. Service quotas define the maximum number of resources you can create or the maximum rate at which you can make API calls for AWS services. Being aware of these limits helps you design resilient architectures, plan for growth, and avoid service disruptions.

### Key steps for implementing this best practice:

1. **Inventory current service usage and quotas**:
   - Document all AWS services used in your workload architecture
   - Identify current usage levels for each service and resource type
   - Review default service quotas for all services in use
   - Understand which quotas are soft limits (adjustable) vs hard limits
   - Map quota dependencies between services and resources

2. **Implement quota monitoring and alerting**:
   - Set up CloudWatch metrics and alarms for quota utilization
   - Create automated alerts when approaching quota limits (typically at 80% utilization)
   - Implement dashboard visualization for quota usage across services
   - Establish regular quota review processes and schedules
   - Monitor quota usage trends and growth patterns

3. **Plan for quota increases and growth**:
   - Forecast future resource needs based on business growth projections
   - Submit quota increase requests proactively before reaching limits
   - Understand AWS quota increase approval processes and timelines
   - Plan for seasonal or event-driven traffic spikes
   - Document quota increase history and rationale

4. **Design architecture with quota awareness**:
   - Distribute workloads across multiple regions to leverage regional quotas
   - Use multiple AWS accounts to increase effective quotas
   - Implement resource pooling and sharing strategies
   - Design for graceful degradation when approaching quota limits
   - Consider alternative services or architectures when quotas are constraining

5. **Establish quota governance and processes**:
   - Create quota management policies and procedures
   - Define roles and responsibilities for quota monitoring and requests
   - Implement approval workflows for quota increase requests
   - Establish communication channels for quota-related issues
   - Document quota-related architectural decisions and trade-offs

6. **Test quota limits and failure scenarios**:
   - Conduct chaos engineering experiments to test quota limit behavior
   - Validate application behavior when quotas are exceeded
   - Test failover and recovery mechanisms related to quota constraints
   - Verify monitoring and alerting effectiveness for quota events
   - Document and practice quota-related incident response procedures

## Implementation examples

### Example 1: Comprehensive quota monitoring and alerting system

```python
import boto3
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any
import uuid

class QuotaMonitoringSystem:
    def __init__(self):
        self.service_quotas = boto3.client('service-quotas')
        self.cloudwatch = boto3.client('cloudwatch')
        self.sns = boto3.client('sns')
        self.dynamodb = boto3.resource('dynamodb')
        
        # DynamoDB table for storing quota information
        self.quota_table = self.dynamodb.Table('ServiceQuotas')
        
        # Services to monitor (can be expanded)
        self.monitored_services = {
            'ec2': {
                'service_code': 'ec2',
                'quotas': [
                    'L-1216C47A',  # Running On-Demand EC2 instances
                    'L-34B43A08',  # All Standard (A, C, D, H, I, M, R, T, Z) Spot Instance Requests
                    'L-0263D0A3',  # EC2-VPC Elastic IPs
                    'L-FE5A380F',  # VPCs per Region
                    'L-F678F1CE',  # Internet gateways per Region
                ]
            },
            'lambda': {
                'service_code': 'lambda',
                'quotas': [
                    'L-B99A9384',  # Concurrent executions
                    'L-2DC4B5D8',  # Function and layer storage
                    'L-9FEE3D26',  # Elastic network interfaces per VPC
                ]
            },
            'rds': {
                'service_code': 'rds',
                'quotas': [
                    'L-7B6409FD',  # DB instances
                    'L-952B80B8',  # DB clusters
                    'L-AADA54BB',  # Manual DB cluster snapshots
                ]
            },
            's3': {
                'service_code': 's3',
                'quotas': [
                    'L-DC2B2D3D',  # Buckets
                    'L-89F76E4F',  # Access points per bucket
                ]
            },
            'dynamodb': {
                'service_code': 'dynamodb',
                'quotas': [
                    'L-F98FE922',  # Table count per Region
                    'L-8A0B4B6B',  # Account-level read capacity units
                    'L-B1A4B0E1',  # Account-level write capacity units
                ]
            }
        }
    
    def get_service_quotas(self, service_code: str) -> List[Dict[str, Any]]:
        """Retrieve service quotas for a specific service"""
        
        quotas = []
        
        try:
            paginator = self.service_quotas.get_paginator('list_service_quotas')
            
            for page in paginator.paginate(ServiceCode=service_code):
                for quota in page['Quotas']:
                    quota_info = {
                        'service_code': service_code,
                        'quota_code': quota['QuotaCode'],
                        'quota_name': quota['QuotaName'],
                        'quota_value': quota['Value'],
                        'unit': quota.get('Unit', 'Count'),
                        'adjustable': quota['Adjustable'],
                        'global_quota': quota.get('GlobalQuota', False),
                        'usage_metric': quota.get('UsageMetric', {}),
                        'period': quota.get('Period', {}),
                        'error_reason': quota.get('ErrorReason'),
                        'retrieved_at': datetime.utcnow().isoformat()
                    }
                    quotas.append(quota_info)
            
        except Exception as e:
            print(f"Error retrieving quotas for {service_code}: {str(e)}")
        
        return quotas
    
    def get_quota_usage(self, service_code: str, quota_code: str, quota_info: Dict[str, Any]) -> Dict[str, Any]:
        """Get current usage for a specific quota"""
        
        usage_info = {
            'service_code': service_code,
            'quota_code': quota_code,
            'current_usage': 0,
            'quota_value': quota_info['quota_value'],
            'utilization_percentage': 0,
            'usage_retrieved_at': datetime.utcnow().isoformat(),
            'usage_method': 'unknown'
        }
        
        # Try to get usage from Service Quotas API first
        try:
            response = self.service_quotas.get_service_quota_usage_metric(
                ServiceCode=service_code,
                QuotaCode=quota_code
            )
            
            if 'UsageMetric' in response:
                usage_metric = response['UsageMetric']
                
                # Get CloudWatch metric data
                if 'MetricDimensions' in usage_metric:
                    usage_info['current_usage'] = self.get_cloudwatch_metric_value(usage_metric)
                    usage_info['usage_method'] = 'service_quotas_api'
        
        except Exception as e:
            print(f"Error getting usage from Service Quotas API for {quota_code}: {str(e)}")
            
            # Fallback to service-specific usage retrieval
            usage_info['current_usage'] = self.get_service_specific_usage(service_code, quota_code)
            usage_info['usage_method'] = 'service_specific_api'
        
        # Calculate utilization percentage
        if usage_info['quota_value'] > 0:
            usage_info['utilization_percentage'] = (
                usage_info['current_usage'] / usage_info['quota_value'] * 100
            )
        
        return usage_info
    
    def get_cloudwatch_metric_value(self, usage_metric: Dict[str, Any]) -> float:
        """Retrieve metric value from CloudWatch"""
        
        try:
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(hours=1)
            
            response = self.cloudwatch.get_metric_statistics(
                Namespace=usage_metric['MetricNamespace'],
                MetricName=usage_metric['MetricName'],
                Dimensions=usage_metric.get('MetricDimensions', {}),
                StartTime=start_time,
                EndTime=end_time,
                Period=3600,  # 1 hour
                Statistics=['Maximum']
            )
            
            if response['Datapoints']:
                return max(dp['Maximum'] for dp in response['Datapoints'])
        
        except Exception as e:
            print(f"Error retrieving CloudWatch metric: {str(e)}")
        
        return 0
    
    def get_service_specific_usage(self, service_code: str, quota_code: str) -> float:
        """Get usage using service-specific APIs"""
        
        usage_methods = {
            'ec2': self.get_ec2_usage,
            'lambda': self.get_lambda_usage,
            'rds': self.get_rds_usage,
            's3': self.get_s3_usage,
            'dynamodb': self.get_dynamodb_usage
        }
        
        if service_code in usage_methods:
            try:
                return usage_methods[service_code](quota_code)
            except Exception as e:
                print(f"Error getting {service_code} usage for {quota_code}: {str(e)}")
        
        return 0
    
    def get_ec2_usage(self, quota_code: str) -> float:
        """Get EC2-specific usage metrics"""
        
        ec2 = boto3.client('ec2')
        
        usage_mapping = {
            'L-1216C47A': lambda: len(ec2.describe_instances(
                Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
            )['Reservations']),
            'L-0263D0A3': lambda: len(ec2.describe_addresses()['Addresses']),
            'L-FE5A380F': lambda: len(ec2.describe_vpcs()['Vpcs']),
            'L-F678F1CE': lambda: len(ec2.describe_internet_gateways()['InternetGateways'])
        }
        
        if quota_code in usage_mapping:
            return float(usage_mapping[quota_code]())
        
        return 0
    
    def get_lambda_usage(self, quota_code: str) -> float:
        """Get Lambda-specific usage metrics"""
        
        lambda_client = boto3.client('lambda')
        
        if quota_code == 'L-B99A9384':  # Concurrent executions
            try:
                response = lambda_client.get_account_settings()
                return float(response.get('AccountUsage', {}).get('FunctionCount', 0))
            except:
                return 0
        
        return 0
    
    def get_rds_usage(self, quota_code: str) -> float:
        """Get RDS-specific usage metrics"""
        
        rds = boto3.client('rds')
        
        usage_mapping = {
            'L-7B6409FD': lambda: len(rds.describe_db_instances()['DBInstances']),
            'L-952B80B8': lambda: len(rds.describe_db_clusters()['DBClusters'])
        }
        
        if quota_code in usage_mapping:
            return float(usage_mapping[quota_code]())
        
        return 0
    
    def get_s3_usage(self, quota_code: str) -> float:
        """Get S3-specific usage metrics"""
        
        s3 = boto3.client('s3')
        
        if quota_code == 'L-DC2B2D3D':  # Buckets
            try:
                return float(len(s3.list_buckets()['Buckets']))
            except:
                return 0
        
        return 0
    
    def get_dynamodb_usage(self, quota_code: str) -> float:
        """Get DynamoDB-specific usage metrics"""
        
        dynamodb = boto3.client('dynamodb')
        
        if quota_code == 'L-F98FE922':  # Table count
            try:
                tables = []
                paginator = dynamodb.get_paginator('list_tables')
                for page in paginator.paginate():
                    tables.extend(page['TableNames'])
                return float(len(tables))
            except:
                return 0
        
        return 0
    
    def monitor_all_quotas(self) -> Dict[str, Any]:
        """Monitor quotas for all configured services"""
        
        monitoring_result = {
            'monitoring_timestamp': datetime.utcnow().isoformat(),
            'services_monitored': [],
            'alerts_generated': [],
            'total_quotas_checked': 0,
            'quotas_approaching_limit': [],
            'quotas_at_limit': []
        }
        
        for service_name, service_config in self.monitored_services.items():
            service_code = service_config['service_code']
            
            print(f"Monitoring quotas for {service_name}...")
            
            service_result = {
                'service_name': service_name,
                'service_code': service_code,
                'quotas_checked': 0,
                'quotas_with_alerts': 0,
                'quota_details': []
            }
            
            # Get all quotas for the service
            all_quotas = self.get_service_quotas(service_code)
            
            # Filter to monitored quotas if specified
            if 'quotas' in service_config:
                monitored_quota_codes = service_config['quotas']
                quotas_to_check = [q for q in all_quotas if q['quota_code'] in monitored_quota_codes]
            else:
                quotas_to_check = all_quotas
            
            for quota in quotas_to_check:
                quota_code = quota['quota_code']
                
                # Get current usage
                usage_info = self.get_quota_usage(service_code, quota_code, quota)
                
                # Combine quota and usage information
                quota_detail = {
                    **quota,
                    **usage_info,
                    'alert_threshold_80': usage_info['utilization_percentage'] >= 80,
                    'alert_threshold_90': usage_info['utilization_percentage'] >= 90,
                    'at_limit': usage_info['utilization_percentage'] >= 100
                }
                
                service_result['quota_details'].append(quota_detail)
                service_result['quotas_checked'] += 1
                
                # Generate alerts if needed
                if quota_detail['alert_threshold_80']:
                    alert = self.generate_quota_alert(quota_detail)
                    monitoring_result['alerts_generated'].append(alert)
                    service_result['quotas_with_alerts'] += 1
                    
                    if quota_detail['alert_threshold_90']:
                        monitoring_result['quotas_approaching_limit'].append(quota_detail)
                    
                    if quota_detail['at_limit']:
                        monitoring_result['quotas_at_limit'].append(quota_detail)
                
                # Store quota information in DynamoDB
                self.store_quota_information(quota_detail)
            
            monitoring_result['services_monitored'].append(service_result)
            monitoring_result['total_quotas_checked'] += service_result['quotas_checked']
        
        # Send consolidated alert if there are critical issues
        if monitoring_result['quotas_at_limit'] or len(monitoring_result['quotas_approaching_limit']) > 5:
            self.send_consolidated_alert(monitoring_result)
        
        return monitoring_result
    
    def generate_quota_alert(self, quota_detail: Dict[str, Any]) -> Dict[str, Any]:
        """Generate alert for quota approaching limit"""
        
        alert_id = str(uuid.uuid4())
        
        # Determine alert severity
        if quota_detail['at_limit']:
            severity = 'CRITICAL'
            message = f"CRITICAL: Quota limit reached for {quota_detail['quota_name']}"
        elif quota_detail['alert_threshold_90']:
            severity = 'HIGH'
            message = f"HIGH: Quota utilization above 90% for {quota_detail['quota_name']}"
        else:
            severity = 'MEDIUM'
            message = f"MEDIUM: Quota utilization above 80% for {quota_detail['quota_name']}"
        
        alert = {
            'alert_id': alert_id,
            'alert_timestamp': datetime.utcnow().isoformat(),
            'severity': severity,
            'service_code': quota_detail['service_code'],
            'quota_code': quota_detail['quota_code'],
            'quota_name': quota_detail['quota_name'],
            'current_usage': quota_detail['current_usage'],
            'quota_value': quota_detail['quota_value'],
            'utilization_percentage': quota_detail['utilization_percentage'],
            'message': message,
            'recommended_actions': self.get_recommended_actions(quota_detail),
            'adjustable': quota_detail['adjustable']
        }
        
        # Send individual alert
        self.send_quota_alert(alert)
        
        return alert
    
    def get_recommended_actions(self, quota_detail: Dict[str, Any]) -> List[str]:
        """Get recommended actions for quota alerts"""
        
        actions = []
        
        if quota_detail['adjustable']:
            actions.append("Submit a quota increase request through AWS Service Quotas console")
            actions.append("Review current usage patterns and optimize resource utilization")
        else:
            actions.append("This is a hard limit - consider architectural changes to work within constraints")
            actions.append("Evaluate alternative services or multi-region deployment strategies")
        
        if quota_detail['utilization_percentage'] >= 90:
            actions.append("URGENT: Implement immediate mitigation measures to prevent service disruption")
            actions.append("Consider temporary resource cleanup or scaling down non-critical workloads")
        
        actions.append("Review and update capacity planning and forecasting models")
        actions.append("Implement automated monitoring and alerting for this quota")
        
        return actions
    
    def store_quota_information(self, quota_detail: Dict[str, Any]):
        """Store quota information in DynamoDB"""
        
        try:
            item = {
                'quota_id': f"{quota_detail['service_code']}#{quota_detail['quota_code']}",
                'service_code': quota_detail['service_code'],
                'quota_code': quota_detail['quota_code'],
                'quota_name': quota_detail['quota_name'],
                'quota_value': quota_detail['quota_value'],
                'current_usage': quota_detail['current_usage'],
                'utilization_percentage': quota_detail['utilization_percentage'],
                'adjustable': quota_detail['adjustable'],
                'last_updated': quota_detail['usage_retrieved_at'],
                'ttl': int((datetime.utcnow() + timedelta(days=30)).timestamp())  # 30-day TTL
            }
            
            self.quota_table.put_item(Item=item)
            
        except Exception as e:
            print(f"Error storing quota information: {str(e)}")
    
    def send_quota_alert(self, alert: Dict[str, Any]):
        """Send individual quota alert via SNS"""
        
        try:
            message = {
                'alert_id': alert['alert_id'],
                'severity': alert['severity'],
                'service': alert['service_code'],
                'quota': alert['quota_name'],
                'utilization': f"{alert['utilization_percentage']:.1f}%",
                'current_usage': alert['current_usage'],
                'quota_limit': alert['quota_value'],
                'adjustable': alert['adjustable'],
                'recommended_actions': alert['recommended_actions']
            }
            
            self.sns.publish(
                TopicArn='arn:aws:sns:us-west-2:123456789012:QuotaAlerts',
                Subject=f"AWS Quota Alert: {alert['severity']} - {alert['quota_name']}",
                Message=json.dumps(message, indent=2)
            )
            
        except Exception as e:
            print(f"Error sending quota alert: {str(e)}")
    
    def send_consolidated_alert(self, monitoring_result: Dict[str, Any]):
        """Send consolidated alert for multiple quota issues"""
        
        try:
            message = {
                'alert_type': 'CONSOLIDATED_QUOTA_ALERT',
                'timestamp': monitoring_result['monitoring_timestamp'],
                'total_quotas_checked': monitoring_result['total_quotas_checked'],
                'quotas_at_limit': len(monitoring_result['quotas_at_limit']),
                'quotas_approaching_limit': len(monitoring_result['quotas_approaching_limit']),
                'critical_quotas': [
                    {
                        'service': q['service_code'],
                        'quota': q['quota_name'],
                        'utilization': f"{q['utilization_percentage']:.1f}%"
                    }
                    for q in monitoring_result['quotas_at_limit']
                ],
                'warning_quotas': [
                    {
                        'service': q['service_code'],
                        'quota': q['quota_name'],
                        'utilization': f"{q['utilization_percentage']:.1f}%"
                    }
                    for q in monitoring_result['quotas_approaching_limit']
                ]
            }
            
            self.sns.publish(
                TopicArn='arn:aws:sns:us-west-2:123456789012:CriticalQuotaAlerts',
                Subject="URGENT: Multiple AWS Quota Limits Approaching",
                Message=json.dumps(message, indent=2)
            )
            
        except Exception as e:
            print(f"Error sending consolidated alert: {str(e)}")

def lambda_handler(event, context):
    """Lambda function to monitor service quotas"""
    
    quota_monitor = QuotaMonitoringSystem()
    
    # Monitor all configured quotas
    monitoring_result = quota_monitor.monitor_all_quotas()
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'monitoring_timestamp': monitoring_result['monitoring_timestamp'],
            'total_quotas_checked': monitoring_result['total_quotas_checked'],
            'alerts_generated': len(monitoring_result['alerts_generated']),
            'quotas_at_limit': len(monitoring_result['quotas_at_limit']),
            'quotas_approaching_limit': len(monitoring_result['quotas_approaching_limit'])
        })
    }
```
### Example 2: Automated quota increase request system

```python
import boto3
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any
import uuid

class QuotaIncreaseManager:
    def __init__(self):
        self.service_quotas = boto3.client('service-quotas')
        self.support = boto3.client('support')
        self.dynamodb = boto3.resource('dynamodb')
        self.sns = boto3.client('sns')
        
        # DynamoDB tables
        self.quota_requests_table = self.dynamodb.Table('QuotaIncreaseRequests')
        self.quota_history_table = self.dynamodb.Table('QuotaHistory')
        
        # Quota increase thresholds and policies
        self.increase_policies = {
            'default': {
                'trigger_threshold': 80,  # Trigger increase request at 80% utilization
                'increase_multiplier': 2.0,  # Double the current quota
                'min_increase': 10,  # Minimum increase amount
                'max_increase': 10000,  # Maximum increase amount
                'auto_approve_threshold': 1000  # Auto-approve increases up to this amount
            },
            'ec2': {
                'L-1216C47A': {  # Running On-Demand EC2 instances
                    'trigger_threshold': 85,
                    'increase_multiplier': 1.5,
                    'min_increase': 50,
                    'max_increase': 5000
                }
            },
            'lambda': {
                'L-B99A9384': {  # Concurrent executions
                    'trigger_threshold': 75,
                    'increase_multiplier': 2.0,
                    'min_increase': 1000,
                    'max_increase': 100000
                }
            }
        }
    
    def evaluate_quota_increase_need(self, quota_detail: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate if a quota needs to be increased"""
        
        evaluation = {
            'quota_id': f"{quota_detail['service_code']}#{quota_detail['quota_code']}",
            'service_code': quota_detail['service_code'],
            'quota_code': quota_detail['quota_code'],
            'quota_name': quota_detail['quota_name'],
            'current_quota': quota_detail['quota_value'],
            'current_usage': quota_detail['current_usage'],
            'utilization_percentage': quota_detail['utilization_percentage'],
            'increase_needed': False,
            'increase_recommended': False,
            'recommended_new_quota': quota_detail['quota_value'],
            'increase_justification': '',
            'evaluation_timestamp': datetime.utcnow().isoformat()
        }
        
        # Get policy for this specific quota or use default
        policy = self.get_quota_policy(quota_detail['service_code'], quota_detail['quota_code'])
        
        # Check if increase is needed based on utilization threshold
        if evaluation['utilization_percentage'] >= policy['trigger_threshold']:
            evaluation['increase_needed'] = True
            evaluation['increase_recommended'] = True
            
            # Calculate recommended new quota
            current_quota = evaluation['current_quota']
            increase_amount = max(
                policy['min_increase'],
                min(
                    policy['max_increase'],
                    int(current_quota * (policy['increase_multiplier'] - 1))
                )
            )
            
            evaluation['recommended_new_quota'] = current_quota + increase_amount
            evaluation['increase_justification'] = (
                f"Current utilization ({evaluation['utilization_percentage']:.1f}%) "
                f"exceeds threshold ({policy['trigger_threshold']}%). "
                f"Recommending increase from {current_quota} to {evaluation['recommended_new_quota']} "
                f"to provide adequate headroom for growth."
            )
        
        # Check historical trends for proactive increases
        historical_trend = self.analyze_quota_usage_trend(
            quota_detail['service_code'], 
            quota_detail['quota_code']
        )
        
        if historical_trend['growth_rate'] > 0.1:  # 10% growth rate
            projected_usage = evaluation['current_usage'] * (1 + historical_trend['growth_rate'])
            projected_utilization = (projected_usage / evaluation['current_quota']) * 100
            
            if projected_utilization >= policy['trigger_threshold']:
                evaluation['increase_recommended'] = True
                if not evaluation['increase_needed']:
                    evaluation['increase_justification'] = (
                        f"Proactive increase recommended based on usage trend. "
                        f"Current growth rate: {historical_trend['growth_rate']:.1%}. "
                        f"Projected utilization in 30 days: {projected_utilization:.1f}%"
                    )
        
        return evaluation
    
    def get_quota_policy(self, service_code: str, quota_code: str) -> Dict[str, Any]:
        """Get quota increase policy for specific service and quota"""
        
        # Check for service-specific quota policy
        if service_code in self.increase_policies:
            service_policies = self.increase_policies[service_code]
            if quota_code in service_policies:
                return {**self.increase_policies['default'], **service_policies[quota_code]}
        
        # Return default policy
        return self.increase_policies['default']
    
    def analyze_quota_usage_trend(self, service_code: str, quota_code: str) -> Dict[str, Any]:
        """Analyze historical quota usage trends"""
        
        trend_analysis = {
            'service_code': service_code,
            'quota_code': quota_code,
            'data_points': 0,
            'growth_rate': 0.0,
            'trend_direction': 'stable',
            'confidence': 'low'
        }
        
        try:
            # Query historical data from DynamoDB
            quota_id = f"{service_code}#{quota_code}"
            
            response = self.quota_history_table.query(
                KeyConditionExpression='quota_id = :quota_id',
                ExpressionAttributeValues={':quota_id': quota_id},
                ScanIndexForward=False,  # Most recent first
                Limit=30  # Last 30 data points
            )
            
            historical_data = response.get('Items', [])
            
            if len(historical_data) >= 7:  # Need at least a week of data
                trend_analysis['data_points'] = len(historical_data)
                
                # Calculate growth rate using linear regression
                usage_values = [float(item['current_usage']) for item in historical_data]
                timestamps = [datetime.fromisoformat(item['timestamp']) for item in historical_data]
                
                # Simple linear regression for growth rate
                n = len(usage_values)
                x_values = list(range(n))
                
                sum_x = sum(x_values)
                sum_y = sum(usage_values)
                sum_xy = sum(x * y for x, y in zip(x_values, usage_values))
                sum_x2 = sum(x * x for x in x_values)
                
                if n * sum_x2 - sum_x * sum_x != 0:
                    slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
                    
                    # Convert slope to growth rate percentage
                    if sum_y > 0:
                        trend_analysis['growth_rate'] = slope / (sum_y / n)
                        
                        if trend_analysis['growth_rate'] > 0.05:
                            trend_analysis['trend_direction'] = 'increasing'
                        elif trend_analysis['growth_rate'] < -0.05:
                            trend_analysis['trend_direction'] = 'decreasing'
                        
                        trend_analysis['confidence'] = 'high' if n >= 14 else 'medium'
        
        except Exception as e:
            print(f"Error analyzing quota usage trend: {str(e)}")
        
        return trend_analysis
    
    def submit_quota_increase_request(self, evaluation: Dict[str, Any]) -> Dict[str, Any]:
        """Submit quota increase request to AWS"""
        
        request_id = str(uuid.uuid4())
        
        request_info = {
            'request_id': request_id,
            'service_code': evaluation['service_code'],
            'quota_code': evaluation['quota_code'],
            'quota_name': evaluation['quota_name'],
            'current_quota': evaluation['current_quota'],
            'requested_quota': evaluation['recommended_new_quota'],
            'increase_amount': evaluation['recommended_new_quota'] - evaluation['current_quota'],
            'justification': evaluation['increase_justification'],
            'request_timestamp': datetime.utcnow().isoformat(),
            'request_status': 'submitted',
            'aws_request_id': None,
            'approval_status': 'pending',
            'estimated_approval_time': None
        }
        
        try:
            # Check if quota is adjustable
            quota_info = self.service_quotas.get_service_quota(
                ServiceCode=evaluation['service_code'],
                QuotaCode=evaluation['quota_code']
            )
            
            if not quota_info['Quota']['Adjustable']:
                request_info['request_status'] = 'failed'
                request_info['failure_reason'] = 'Quota is not adjustable'
                return request_info
            
            # Submit quota increase request
            response = self.service_quotas.request_service_quota_increase(
                ServiceCode=evaluation['service_code'],
                QuotaCode=evaluation['quota_code'],
                DesiredValue=evaluation['recommended_new_quota']
            )
            
            request_info['aws_request_id'] = response['RequestedQuota']['Id']
            request_info['request_status'] = 'submitted'
            request_info['approval_status'] = response['RequestedQuota']['Status']
            
            # Store request information
            self.store_quota_request(request_info)
            
            # Send notification
            self.send_quota_request_notification(request_info)
            
        except Exception as e:
            request_info['request_status'] = 'failed'
            request_info['failure_reason'] = str(e)
            print(f"Error submitting quota increase request: {str(e)}")
        
        return request_info
    
    def check_quota_request_status(self, request_id: str) -> Dict[str, Any]:
        """Check the status of a quota increase request"""
        
        try:
            # Get request information from DynamoDB
            response = self.quota_requests_table.get_item(
                Key={'request_id': request_id}
            )
            
            if 'Item' not in response:
                return {'error': 'Request not found'}
            
            request_info = response['Item']
            
            if request_info.get('aws_request_id'):
                # Check status with AWS
                aws_response = self.service_quotas.get_requested_service_quota_change(
                    RequestId=request_info['aws_request_id']
                )
                
                # Update status
                request_info['approval_status'] = aws_response['RequestedQuota']['Status']
                request_info['last_updated'] = datetime.utcnow().isoformat()
                
                # If approved, update the quota value
                if request_info['approval_status'] == 'APPROVED':
                    request_info['approved_quota'] = aws_response['RequestedQuota']['DesiredValue']
                    request_info['approval_timestamp'] = datetime.utcnow().isoformat()
                
                # Update DynamoDB record
                self.quota_requests_table.put_item(Item=request_info)
                
                # Send status update notification
                if request_info['approval_status'] in ['APPROVED', 'DENIED']:
                    self.send_quota_status_notification(request_info)
            
            return request_info
            
        except Exception as e:
            return {'error': str(e)}
    
    def process_quota_evaluations(self, quota_details: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Process quota evaluations and submit increase requests as needed"""
        
        processing_result = {
            'processing_timestamp': datetime.utcnow().isoformat(),
            'quotas_evaluated': len(quota_details),
            'increases_needed': 0,
            'increases_recommended': 0,
            'requests_submitted': 0,
            'requests_failed': 0,
            'evaluation_details': [],
            'submitted_requests': []
        }
        
        for quota_detail in quota_details:
            # Evaluate quota increase need
            evaluation = self.evaluate_quota_increase_need(quota_detail)
            processing_result['evaluation_details'].append(evaluation)
            
            if evaluation['increase_needed']:
                processing_result['increases_needed'] += 1
            
            if evaluation['increase_recommended']:
                processing_result['increases_recommended'] += 1
                
                # Check if we should auto-submit the request
                if self.should_auto_submit_request(evaluation):
                    request_result = self.submit_quota_increase_request(evaluation)
                    processing_result['submitted_requests'].append(request_result)
                    
                    if request_result['request_status'] == 'submitted':
                        processing_result['requests_submitted'] += 1
                    else:
                        processing_result['requests_failed'] += 1
        
        return processing_result
    
    def should_auto_submit_request(self, evaluation: Dict[str, Any]) -> bool:
        """Determine if quota increase request should be auto-submitted"""
        
        # Check if there's already a pending request for this quota
        existing_request = self.check_existing_request(
            evaluation['service_code'], 
            evaluation['quota_code']
        )
        
        if existing_request:
            return False
        
        # Check auto-approval policies
        policy = self.get_quota_policy(evaluation['service_code'], evaluation['quota_code'])
        increase_amount = evaluation['recommended_new_quota'] - evaluation['current_quota']
        
        # Auto-submit if increase is within auto-approval threshold
        if increase_amount <= policy.get('auto_approve_threshold', 1000):
            return True
        
        # Auto-submit for critical utilization levels
        if evaluation['utilization_percentage'] >= 95:
            return True
        
        return False
    
    def check_existing_request(self, service_code: str, quota_code: str) -> Dict[str, Any]:
        """Check if there's an existing pending request for a quota"""
        
        try:
            # Query for pending requests
            response = self.quota_requests_table.scan(
                FilterExpression='service_code = :service_code AND quota_code = :quota_code AND approval_status = :status',
                ExpressionAttributeValues={
                    ':service_code': service_code,
                    ':quota_code': quota_code,
                    ':status': 'PENDING'
                }
            )
            
            if response['Items']:
                return response['Items'][0]
        
        except Exception as e:
            print(f"Error checking existing requests: {str(e)}")
        
        return None
    
    def store_quota_request(self, request_info: Dict[str, Any]):
        """Store quota request information in DynamoDB"""
        
        try:
            self.quota_requests_table.put_item(Item=request_info)
        except Exception as e:
            print(f"Error storing quota request: {str(e)}")
    
    def send_quota_request_notification(self, request_info: Dict[str, Any]):
        """Send notification about quota increase request"""
        
        try:
            message = {
                'request_id': request_info['request_id'],
                'service': request_info['service_code'],
                'quota': request_info['quota_name'],
                'current_quota': request_info['current_quota'],
                'requested_quota': request_info['requested_quota'],
                'increase_amount': request_info['increase_amount'],
                'justification': request_info['justification'],
                'aws_request_id': request_info.get('aws_request_id'),
                'status': request_info['request_status']
            }
            
            self.sns.publish(
                TopicArn='arn:aws:sns:us-west-2:123456789012:QuotaIncreaseRequests',
                Subject=f"Quota Increase Request Submitted: {request_info['quota_name']}",
                Message=json.dumps(message, indent=2)
            )
            
        except Exception as e:
            print(f"Error sending quota request notification: {str(e)}")
    
    def send_quota_status_notification(self, request_info: Dict[str, Any]):
        """Send notification about quota request status update"""
        
        try:
            message = {
                'request_id': request_info['request_id'],
                'service': request_info['service_code'],
                'quota': request_info['quota_name'],
                'requested_quota': request_info['requested_quota'],
                'status': request_info['approval_status'],
                'approved_quota': request_info.get('approved_quota'),
                'approval_timestamp': request_info.get('approval_timestamp')
            }
            
            subject = f"Quota Request {request_info['approval_status']}: {request_info['quota_name']}"
            
            self.sns.publish(
                TopicArn='arn:aws:sns:us-west-2:123456789012:QuotaRequestUpdates',
                Subject=subject,
                Message=json.dumps(message, indent=2)
            )
            
        except Exception as e:
            print(f"Error sending quota status notification: {str(e)}")

def lambda_handler(event, context):
    """Lambda function to manage quota increase requests"""
    
    quota_manager = QuotaIncreaseManager()
    
    action = event.get('action', 'process_evaluations')
    
    if action == 'process_evaluations':
        quota_details = event.get('quota_details', [])
        result = quota_manager.process_quota_evaluations(quota_details)
    elif action == 'check_request_status':
        request_id = event.get('request_id')
        result = quota_manager.check_quota_request_status(request_id)
    else:
        result = {'error': 'Invalid action specified'}
    
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
```

### Example 3: CloudFormation template for quota monitoring infrastructure

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'AWS Service Quota Monitoring and Management Infrastructure'

Parameters:
  NotificationEmail:
    Type: String
    Description: Email address for quota alerts
    Default: admin@company.com
  
  MonitoringSchedule:
    Type: String
    Description: CloudWatch Events schedule for quota monitoring
    Default: 'rate(1 hour)'
  
  AlertThreshold:
    Type: Number
    Description: Utilization percentage threshold for alerts
    Default: 80
    MinValue: 50
    MaxValue: 95

Resources:
  # DynamoDB Tables
  ServiceQuotasTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: ServiceQuotas
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: quota_id
          AttributeType: S
      KeySchema:
        - AttributeName: quota_id
          KeyType: HASH
      TimeToLiveSpecification:
        AttributeName: ttl
        Enabled: true
      PointInTimeRecoverySpecification:
        PointInTimeRecoveryEnabled: true
      Tags:
        - Key: Purpose
          Value: QuotaMonitoring
        - Key: Component
          Value: Storage

  QuotaIncreaseRequestsTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: QuotaIncreaseRequests
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: request_id
          AttributeType: S
        - AttributeName: service_code
          AttributeType: S
        - AttributeName: request_timestamp
          AttributeType: S
      KeySchema:
        - AttributeName: request_id
          KeyType: HASH
      GlobalSecondaryIndexes:
        - IndexName: ServiceCodeIndex
          KeySchema:
            - AttributeName: service_code
              KeyType: HASH
            - AttributeName: request_timestamp
              KeyType: RANGE
          Projection:
            ProjectionType: ALL
      Tags:
        - Key: Purpose
          Value: QuotaManagement
        - Key: Component
          Value: Storage

  QuotaHistoryTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: QuotaHistory
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: quota_id
          AttributeType: S
        - AttributeName: timestamp
          AttributeType: S
      KeySchema:
        - AttributeName: quota_id
          KeyType: HASH
        - AttributeName: timestamp
          KeyType: RANGE
      TimeToLiveSpecification:
        AttributeName: ttl
        Enabled: true
      Tags:
        - Key: Purpose
          Value: QuotaHistory
        - Key: Component
          Value: Storage

  # SNS Topics
  QuotaAlertsTopicPolicy:
    Type: AWS::SNS::TopicPolicy
    Properties:
      Topics:
        - !Ref QuotaAlertsTopic
      PolicyDocument:
        Statement:
          - Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action: sns:Publish
            Resource: !Ref QuotaAlertsTopic

  QuotaAlertsTopic:
    Type: AWS::SNS::Topic
    Properties:
      TopicName: QuotaAlerts
      DisplayName: AWS Service Quota Alerts
      KmsMasterKeyId: alias/aws/sns

  QuotaAlertsSubscription:
    Type: AWS::SNS::Subscription
    Properties:
      Protocol: email
      TopicArn: !Ref QuotaAlertsTopic
      Endpoint: !Ref NotificationEmail

  CriticalQuotaAlertsTopic:
    Type: AWS::SNS::Topic
    Properties:
      TopicName: CriticalQuotaAlerts
      DisplayName: Critical AWS Service Quota Alerts
      KmsMasterKeyId: alias/aws/sns

  CriticalQuotaAlertsSubscription:
    Type: AWS::SNS::Subscription
    Properties:
      Protocol: email
      TopicArn: !Ref CriticalQuotaAlertsTopic
      Endpoint: !Ref NotificationEmail

  QuotaIncreaseRequestsTopic:
    Type: AWS::SNS::Topic
    Properties:
      TopicName: QuotaIncreaseRequests
      DisplayName: AWS Quota Increase Requests
      KmsMasterKeyId: alias/aws/sns

  QuotaIncreaseRequestsSubscription:
    Type: AWS::SNS::Subscription
    Properties:
      Protocol: email
      TopicArn: !Ref QuotaIncreaseRequestsTopic
      Endpoint: !Ref NotificationEmail

  # IAM Roles
  QuotaMonitoringRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: QuotaMonitoringRole
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
                  - service-quotas:GetServiceQuota
                  - service-quotas:ListServiceQuotas
                  - service-quotas:GetServiceQuotaUsageMetric
                  - service-quotas:RequestServiceQuotaIncrease
                  - service-quotas:GetRequestedServiceQuotaChange
                  - service-quotas:ListRequestedServiceQuotaChangeHistory
                Resource: '*'
              - Effect: Allow
                Action:
                  - cloudwatch:GetMetricStatistics
                  - cloudwatch:ListMetrics
                Resource: '*'
              - Effect: Allow
                Action:
                  - ec2:Describe*
                  - lambda:GetAccountSettings
                  - lambda:ListFunctions
                  - rds:Describe*
                  - s3:ListAllMyBuckets
                  - dynamodb:ListTables
                Resource: '*'
              - Effect: Allow
                Action:
                  - dynamodb:GetItem
                  - dynamodb:PutItem
                  - dynamodb:Query
                  - dynamodb:Scan
                Resource:
                  - !GetAtt ServiceQuotasTable.Arn
                  - !GetAtt QuotaIncreaseRequestsTable.Arn
                  - !GetAtt QuotaHistoryTable.Arn
                  - !Sub '${QuotaIncreaseRequestsTable.Arn}/index/*'
              - Effect: Allow
                Action:
                  - sns:Publish
                Resource:
                  - !Ref QuotaAlertsTopic
                  - !Ref CriticalQuotaAlertsTopic
                  - !Ref QuotaIncreaseRequestsTopic

  # Lambda Functions
  QuotaMonitoringFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: quota-monitoring-function
      Runtime: python3.9
      Handler: lambda_function.lambda_handler
      Role: !GetAtt QuotaMonitoringRole.Arn
      Timeout: 300
      MemorySize: 512
      Environment:
        Variables:
          QUOTA_TABLE_NAME: !Ref ServiceQuotasTable
          REQUESTS_TABLE_NAME: !Ref QuotaIncreaseRequestsTable
          HISTORY_TABLE_NAME: !Ref QuotaHistoryTable
          ALERT_TOPIC_ARN: !Ref QuotaAlertsTopic
          CRITICAL_ALERT_TOPIC_ARN: !Ref CriticalQuotaAlertsTopic
          ALERT_THRESHOLD: !Ref AlertThreshold
      Code:
        ZipFile: |
          import json
          import boto3
          import os
          from datetime import datetime
          
          def lambda_handler(event, context):
              # Placeholder - replace with actual monitoring code
              print("Quota monitoring function executed")
              
              return {
                  'statusCode': 200,
                  'body': json.dumps('Quota monitoring completed')
              }

  QuotaIncreaseManagerFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: quota-increase-manager-function
      Runtime: python3.9
      Handler: lambda_function.lambda_handler
      Role: !GetAtt QuotaMonitoringRole.Arn
      Timeout: 300
      MemorySize: 512
      Environment:
        Variables:
          REQUESTS_TABLE_NAME: !Ref QuotaIncreaseRequestsTable
          HISTORY_TABLE_NAME: !Ref QuotaHistoryTable
          REQUEST_TOPIC_ARN: !Ref QuotaIncreaseRequestsTopic
      Code:
        ZipFile: |
          import json
          import boto3
          import os
          from datetime import datetime
          
          def lambda_handler(event, context):
              # Placeholder - replace with actual quota increase management code
              print("Quota increase manager function executed")
              
              return {
                  'statusCode': 200,
                  'body': json.dumps('Quota increase management completed')
              }

  # CloudWatch Events
  QuotaMonitoringSchedule:
    Type: AWS::Events::Rule
    Properties:
      Name: QuotaMonitoringSchedule
      Description: Schedule for quota monitoring
      ScheduleExpression: !Ref MonitoringSchedule
      State: ENABLED
      Targets:
        - Arn: !GetAtt QuotaMonitoringFunction.Arn
          Id: QuotaMonitoringTarget

  QuotaMonitoringPermission:
    Type: AWS::Lambda::Permission
    Properties:
      FunctionName: !Ref QuotaMonitoringFunction
      Action: lambda:InvokeFunction
      Principal: events.amazonaws.com
      SourceArn: !GetAtt QuotaMonitoringSchedule.Arn

  # CloudWatch Dashboard
  QuotaMonitoringDashboard:
    Type: AWS::CloudWatch::Dashboard
    Properties:
      DashboardName: ServiceQuotaMonitoring
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
                  ["AWS/Lambda", "Duration", "FunctionName", "${QuotaMonitoringFunction}"],
                  [".", "Errors", ".", "."],
                  [".", "Invocations", ".", "."]
                ],
                "view": "timeSeries",
                "stacked": false,
                "region": "${AWS::Region}",
                "title": "Quota Monitoring Function Metrics",
                "period": 300
              }
            },
            {
              "type": "log",
              "x": 0,
              "y": 6,
              "width": 24,
              "height": 6,
              "properties": {
                "query": "SOURCE '/aws/lambda/${QuotaMonitoringFunction}' | fields @timestamp, @message\n| filter @message like /ALERT/\n| sort @timestamp desc\n| limit 20",
                "region": "${AWS::Region}",
                "title": "Recent Quota Alerts",
                "view": "table"
              }
            }
          ]
        }

Outputs:
  ServiceQuotasTableName:
    Description: Name of the Service Quotas DynamoDB table
    Value: !Ref ServiceQuotasTable
    Export:
      Name: !Sub '${AWS::StackName}-ServiceQuotasTable'

  QuotaAlertsTopicArn:
    Description: ARN of the Quota Alerts SNS topic
    Value: !Ref QuotaAlertsTopic
    Export:
      Name: !Sub '${AWS::StackName}-QuotaAlertsTopic'

  QuotaMonitoringFunctionArn:
    Description: ARN of the Quota Monitoring Lambda function
    Value: !GetAtt QuotaMonitoringFunction.Arn
    Export:
      Name: !Sub '${AWS::StackName}-QuotaMonitoringFunction'

  DashboardURL:
    Description: URL of the CloudWatch Dashboard
    Value: !Sub 'https://${AWS::Region}.console.aws.amazon.com/cloudwatch/home?region=${AWS::Region}#dashboards:name=${QuotaMonitoringDashboard}'
```
### Example 4: Quota awareness integration with Terraform

```hcl
# terraform/quota-monitoring.tf
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# Variables
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-west-2"
}

variable "notification_email" {
  description = "Email for quota notifications"
  type        = string
}

variable "alert_threshold" {
  description = "Quota utilization threshold for alerts"
  type        = number
  default     = 80
}

# Data sources for current quotas
data "aws_servicequotas_service_quota" "ec2_instances" {
  service_code = "ec2"
  quota_code   = "L-1216C47A"  # Running On-Demand EC2 instances
}

data "aws_servicequotas_service_quota" "lambda_concurrent" {
  service_code = "lambda"
  quota_code   = "L-B99A9384"  # Concurrent executions
}

data "aws_servicequotas_service_quota" "rds_instances" {
  service_code = "rds"
  quota_code   = "L-7B6409FD"  # DB instances
}

# Local values for quota calculations
locals {
  quota_info = {
    ec2_instances = {
      service_code    = "ec2"
      quota_code      = "L-1216C47A"
      quota_name      = "Running On-Demand EC2 instances"
      current_quota   = data.aws_servicequotas_service_quota.ec2_instances.value
      desired_quota   = max(data.aws_servicequotas_service_quota.ec2_instances.value * 1.5, 100)
      increase_needed = data.aws_servicequotas_service_quota.ec2_instances.value < 100
    }
    lambda_concurrent = {
      service_code    = "lambda"
      quota_code      = "L-B99A9384"
      quota_name      = "Lambda Concurrent executions"
      current_quota   = data.aws_servicequotas_service_quota.lambda_concurrent.value
      desired_quota   = max(data.aws_servicequotas_service_quota.lambda_concurrent.value * 2, 10000)
      increase_needed = data.aws_servicequotas_service_quota.lambda_concurrent.value < 10000
    }
    rds_instances = {
      service_code    = "rds"
      quota_code      = "L-7B6409FD"
      quota_name      = "RDS DB instances"
      current_quota   = data.aws_servicequotas_service_quota.rds_instances.value
      desired_quota   = max(data.aws_servicequotas_service_quota.rds_instances.value * 1.5, 50)
      increase_needed = data.aws_servicequotas_service_quota.rds_instances.value < 50
    }
  }
}

# Quota increase requests (conditional)
resource "aws_servicequotas_service_quota" "ec2_instances_increase" {
  count = local.quota_info.ec2_instances.increase_needed ? 1 : 0
  
  service_code = local.quota_info.ec2_instances.service_code
  quota_code   = local.quota_info.ec2_instances.quota_code
  value        = local.quota_info.ec2_instances.desired_quota
  
  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_servicequotas_service_quota" "lambda_concurrent_increase" {
  count = local.quota_info.lambda_concurrent.increase_needed ? 1 : 0
  
  service_code = local.quota_info.lambda_concurrent.service_code
  quota_code   = local.quota_info.lambda_concurrent.quota_code
  value        = local.quota_info.lambda_concurrent.desired_quota
  
  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_servicequotas_service_quota" "rds_instances_increase" {
  count = local.quota_info.rds_instances.increase_needed ? 1 : 0
  
  service_code = local.quota_info.rds_instances.service_code
  quota_code   = local.quota_info.rds_instances.quota_code
  value        = local.quota_info.rds_instances.desired_quota
  
  lifecycle {
    create_before_destroy = true
  }
}

# CloudWatch alarms for quota monitoring
resource "aws_cloudwatch_metric_alarm" "ec2_instance_quota_utilization" {
  alarm_name          = "ec2-instance-quota-utilization"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "ResourceCount"
  namespace           = "AWS/Usage"
  period              = "300"
  statistic           = "Maximum"
  threshold           = local.quota_info.ec2_instances.current_quota * (var.alert_threshold / 100)
  alarm_description   = "This metric monitors EC2 instance quota utilization"
  alarm_actions       = [aws_sns_topic.quota_alerts.arn]
  
  dimensions = {
    Type     = "Resource"
    Resource = "vCPU"
    Service  = "EC2-Instance"
    Class    = "Standard/OnDemand"
  }
  
  tags = {
    Name        = "EC2 Instance Quota Utilization"
    Environment = "production"
    Purpose     = "quota-monitoring"
  }
}

resource "aws_cloudwatch_metric_alarm" "lambda_concurrent_quota_utilization" {
  alarm_name          = "lambda-concurrent-quota-utilization"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "ConcurrentExecutions"
  namespace           = "AWS/Lambda"
  period              = "300"
  statistic           = "Maximum"
  threshold           = local.quota_info.lambda_concurrent.current_quota * (var.alert_threshold / 100)
  alarm_description   = "This metric monitors Lambda concurrent execution quota utilization"
  alarm_actions       = [aws_sns_topic.quota_alerts.arn]
  
  tags = {
    Name        = "Lambda Concurrent Execution Quota Utilization"
    Environment = "production"
    Purpose     = "quota-monitoring"
  }
}

# SNS topic for quota alerts
resource "aws_sns_topic" "quota_alerts" {
  name              = "quota-alerts"
  kms_master_key_id = "alias/aws/sns"
  
  tags = {
    Name        = "Quota Alerts"
    Environment = "production"
    Purpose     = "quota-monitoring"
  }
}

resource "aws_sns_topic_subscription" "quota_alerts_email" {
  topic_arn = aws_sns_topic.quota_alerts.arn
  protocol  = "email"
  endpoint  = var.notification_email
}

# Lambda function for quota monitoring
resource "aws_lambda_function" "quota_monitor" {
  filename         = "quota_monitor.zip"
  function_name    = "quota-monitor"
  role            = aws_iam_role.quota_monitor_role.arn
  handler         = "lambda_function.lambda_handler"
  runtime         = "python3.9"
  timeout         = 300
  memory_size     = 512
  
  environment {
    variables = {
      SNS_TOPIC_ARN    = aws_sns_topic.quota_alerts.arn
      ALERT_THRESHOLD  = var.alert_threshold
      AWS_REGION       = var.aws_region
    }
  }
  
  tags = {
    Name        = "Quota Monitor"
    Environment = "production"
    Purpose     = "quota-monitoring"
  }
}

# IAM role for Lambda function
resource "aws_iam_role" "quota_monitor_role" {
  name = "quota-monitor-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
  
  tags = {
    Name        = "Quota Monitor Role"
    Environment = "production"
    Purpose     = "quota-monitoring"
  }
}

# IAM policy for quota monitoring
resource "aws_iam_role_policy" "quota_monitor_policy" {
  name = "quota-monitor-policy"
  role = aws_iam_role.quota_monitor_role.id
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "service-quotas:GetServiceQuota",
          "service-quotas:ListServiceQuotas",
          "service-quotas:GetServiceQuotaUsageMetric",
          "service-quotas:RequestServiceQuotaIncrease",
          "service-quotas:GetRequestedServiceQuotaChange"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "cloudwatch:GetMetricStatistics",
          "cloudwatch:ListMetrics"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "ec2:Describe*",
          "lambda:GetAccountSettings",
          "rds:Describe*",
          "s3:ListAllMyBuckets",
          "dynamodb:ListTables"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "sns:Publish"
        ]
        Resource = aws_sns_topic.quota_alerts.arn
      },
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:*"
      }
    ]
  })
}

# EventBridge rule for scheduled quota monitoring
resource "aws_cloudwatch_event_rule" "quota_monitor_schedule" {
  name                = "quota-monitor-schedule"
  description         = "Trigger quota monitoring Lambda function"
  schedule_expression = "rate(1 hour)"
  
  tags = {
    Name        = "Quota Monitor Schedule"
    Environment = "production"
    Purpose     = "quota-monitoring"
  }
}

resource "aws_cloudwatch_event_target" "quota_monitor_target" {
  rule      = aws_cloudwatch_event_rule.quota_monitor_schedule.name
  target_id = "QuotaMonitorTarget"
  arn       = aws_lambda_function.quota_monitor.arn
}

resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.quota_monitor.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.quota_monitor_schedule.arn
}

# CloudWatch dashboard for quota monitoring
resource "aws_cloudwatch_dashboard" "quota_monitoring" {
  dashboard_name = "ServiceQuotaMonitoring"
  
  dashboard_body = jsonencode({
    widgets = [
      {
        type   = "metric"
        x      = 0
        y      = 0
        width  = 12
        height = 6
        
        properties = {
          metrics = [
            ["AWS/Usage", "ResourceCount", "Type", "Resource", "Resource", "vCPU", "Service", "EC2-Instance", "Class", "Standard/OnDemand"],
            ["AWS/Lambda", "ConcurrentExecutions"],
            ["AWS/RDS", "DatabaseConnections"]
          ]
          view    = "timeSeries"
          stacked = false
          region  = var.aws_region
          title   = "Service Usage Metrics"
          period  = 300
          annotations = {
            horizontal = [
              {
                label = "EC2 Instance Quota (${local.quota_info.ec2_instances.current_quota})"
                value = local.quota_info.ec2_instances.current_quota
              },
              {
                label = "Lambda Concurrent Quota (${local.quota_info.lambda_concurrent.current_quota})"
                value = local.quota_info.lambda_concurrent.current_quota
              }
            ]
          }
        }
      },
      {
        type   = "metric"
        x      = 12
        y      = 0
        width  = 12
        height = 6
        
        properties = {
          metrics = [
            ["AWS/Lambda", "Duration", "FunctionName", aws_lambda_function.quota_monitor.function_name],
            [".", "Errors", ".", "."],
            [".", "Invocations", ".", "."]
          ]
          view    = "timeSeries"
          stacked = false
          region  = var.aws_region
          title   = "Quota Monitor Function Metrics"
          period  = 300
        }
      }
    ]
  })
  
  depends_on = [aws_lambda_function.quota_monitor]
}

# Outputs
output "quota_info" {
  description = "Current quota information"
  value = {
    for key, quota in local.quota_info : key => {
      service_code    = quota.service_code
      quota_name      = quota.quota_name
      current_quota   = quota.current_quota
      desired_quota   = quota.desired_quota
      increase_needed = quota.increase_needed
    }
  }
}

output "monitoring_resources" {
  description = "Quota monitoring resources"
  value = {
    lambda_function_arn = aws_lambda_function.quota_monitor.arn
    sns_topic_arn      = aws_sns_topic.quota_alerts.arn
    dashboard_url      = "https://${var.aws_region}.console.aws.amazon.com/cloudwatch/home?region=${var.aws_region}#dashboards:name=${aws_cloudwatch_dashboard.quota_monitoring.dashboard_name}"
  }
}

output "quota_increase_requests" {
  description = "Quota increase requests submitted"
  value = {
    ec2_instances_increase = local.quota_info.ec2_instances.increase_needed ? "Requested increase to ${local.quota_info.ec2_instances.desired_quota}" : "No increase needed"
    lambda_concurrent_increase = local.quota_info.lambda_concurrent.increase_needed ? "Requested increase to ${local.quota_info.lambda_concurrent.desired_quota}" : "No increase needed"
    rds_instances_increase = local.quota_info.rds_instances.increase_needed ? "Requested increase to ${local.quota_info.rds_instances.desired_quota}" : "No increase needed"
  }
}
```

## AWS services to consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Service Quotas</h4>
    <p>Centralized service for viewing and managing your quotas for AWS services. Provides APIs to retrieve current quotas, usage metrics, and submit increase requests.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon CloudWatch</h4>
    <p>Monitoring service that provides metrics for quota utilization and enables creation of alarms when approaching quota limits.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Lambda</h4>
    <p>Serverless compute service for running automated quota monitoring and management functions without managing infrastructure.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon DynamoDB</h4>
    <p>NoSQL database service for storing quota information, usage history, and increase request tracking data.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon SNS</h4>
    <p>Messaging service for sending quota alerts and notifications when limits are approached or exceeded.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Support API</h4>
    <p>Programmatic access to AWS Support for creating and managing support cases related to quota increases.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon EventBridge</h4>
    <p>Event bus service for scheduling regular quota monitoring and triggering automated responses to quota events.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Config</h4>
    <p>Configuration management service for tracking quota changes and maintaining compliance with quota policies.</p>
  </div>
</div>

## Benefits of being aware of service quotas and constraints

- **Proactive capacity planning**: Enables planning for growth and avoiding service disruptions
- **Improved reliability**: Prevents application failures due to quota limits being reached
- **Cost optimization**: Helps optimize resource usage and avoid unnecessary quota increases
- **Better architecture decisions**: Informs architectural choices based on service constraints
- **Faster incident resolution**: Reduces time to identify and resolve quota-related issues
- **Enhanced monitoring**: Provides visibility into resource utilization and growth trends
- **Automated management**: Enables automated quota monitoring and increase request processes
- **Compliance assurance**: Ensures adherence to organizational resource usage policies

## Related resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/rel_manage_service_quotas_aware_quotas_constraints.html">AWS Well-Architected Framework - Aware of service quotas and constraints</a></li>
    <li><a href="https://docs.aws.amazon.com/servicequotas/latest/userguide/intro.html">AWS Service Quotas User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/general/latest/gr/aws_service_limits.html">AWS Service Quotas Reference</a></li>
    <li><a href="https://aws.amazon.com/blogs/aws/service-quotas-view-and-manage-quotas-for-aws-services-from-one-location/">Service Quotas – View and Manage Quotas for AWS Services from One Location</a></li>
    <li><a href="https://docs.aws.amazon.com/servicequotas/latest/APIReference/Welcome.html">AWS Service Quotas API Reference</a></li>
    <li><a href="https://aws.amazon.com/premiumsupport/knowledge-center/manage-service-limits/">How do I manage AWS service quotas?</a></li>
  </ul>
</div>
