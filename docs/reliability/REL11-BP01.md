---
title: REL11-BP01 - Monitor all components of the workload to detect failures
layout: default
parent: Reliability
nav_order: 111
---

# REL11-BP01: Monitor all components of the workload to detect failures

Comprehensive monitoring is the foundation of building resilient workloads. By implementing monitoring across all layers of your architecture - from infrastructure to application to business metrics - you can detect failures quickly and trigger appropriate recovery mechanisms before they impact users.

## Implementation Steps

### 1. Infrastructure Monitoring
Set up monitoring for all infrastructure components including compute, storage, network, and database resources.

### 2. Application Performance Monitoring
Implement application-level monitoring to track performance metrics, error rates, and user experience indicators.

### 3. Business Metrics Monitoring
Monitor key business indicators that reflect the health and performance of your workload from a user perspective.

### 4. Synthetic Monitoring
Deploy synthetic transactions and canaries to proactively detect issues before real users are affected.

### 5. Log Aggregation and Analysis
Centralize logs from all components and implement automated analysis to detect patterns and anomalies.

## Detailed Implementation
{% raw %}
```python
import boto3
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

class MonitoringLevel(Enum):
    INFRASTRUCTURE = "infrastructure"
    APPLICATION = "application"
    BUSINESS = "business"
    SYNTHETIC = "synthetic"

class AlertSeverity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

@dataclass
class MonitoringMetric:
    name: str
    namespace: str
    dimensions: Dict[str, str]
    threshold_value: float
    comparison_operator: str
    evaluation_periods: int
    datapoints_to_alarm: int
    statistic: str
    period: int
    severity: AlertSeverity
    description: str

@dataclass
class SyntheticCanary:
    name: str
    endpoint: str
    method: str
    expected_status: int
    timeout: int
    frequency: int
    locations: List[str]
    assertions: List[Dict[str, Any]]

class ComprehensiveMonitoringSystem:
    def __init__(self, region: str = 'us-east-1'):
        self.region = region
        self.cloudwatch = boto3.client('cloudwatch', region_name=region)
        self.synthetics = boto3.client('synthetics', region_name=region)
        self.logs = boto3.client('logs', region_name=region)
        self.sns = boto3.client('sns', region_name=region)
        self.lambda_client = boto3.client('lambda', region_name=region)
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def setup_infrastructure_monitoring(self, resources: Dict[str, List[str]]) -> List[str]:
        """Set up comprehensive infrastructure monitoring"""
        alarm_arns = []
        
        try:
            # EC2 Instance Monitoring
            if 'ec2_instances' in resources:
                for instance_id in resources['ec2_instances']:
                    # CPU Utilization
                    cpu_metric = MonitoringMetric(
                        name="CPUUtilization",
                        namespace="AWS/EC2",
                        dimensions={"InstanceId": instance_id},
                        threshold_value=80.0,
                        comparison_operator="GreaterThanThreshold",
                        evaluation_periods=2,
                        datapoints_to_alarm=2,
                        statistic="Average",
                        period=300,
                        severity=AlertSeverity.HIGH,
                        description=f"High CPU utilization on instance {instance_id}"
                    )
                    alarm_arns.append(self._create_cloudwatch_alarm(cpu_metric, f"EC2-CPU-{instance_id}"))
                    
                    # Status Check Failed
                    status_metric = MonitoringMetric(
                        name="StatusCheckFailed",
                        namespace="AWS/EC2",
                        dimensions={"InstanceId": instance_id},
                        threshold_value=1.0,
                        comparison_operator="GreaterThanOrEqualToThreshold",
                        evaluation_periods=1,
                        datapoints_to_alarm=1,
                        statistic="Maximum",
                        period=60,
                        severity=AlertSeverity.CRITICAL,
                        description=f"Status check failed for instance {instance_id}"
                    )
                    alarm_arns.append(self._create_cloudwatch_alarm(status_metric, f"EC2-Status-{instance_id}"))

            # RDS Database Monitoring
            if 'rds_instances' in resources:
                for db_instance in resources['rds_instances']:
                    # Database Connections
                    conn_metric = MonitoringMetric(
                        name="DatabaseConnections",
                        namespace="AWS/RDS",
                        dimensions={"DBInstanceIdentifier": db_instance},
                        threshold_value=80.0,
                        comparison_operator="GreaterThanThreshold",
                        evaluation_periods=2,
                        datapoints_to_alarm=2,
                        statistic="Average",
                        period=300,
                        severity=AlertSeverity.HIGH,
                        description=f"High database connections on {db_instance}"
                    )
                    alarm_arns.append(self._create_cloudwatch_alarm(conn_metric, f"RDS-Connections-{db_instance}"))
                    
                    # CPU Utilization
                    db_cpu_metric = MonitoringMetric(
                        name="CPUUtilization",
                        namespace="AWS/RDS",
                        dimensions={"DBInstanceIdentifier": db_instance},
                        threshold_value=75.0,
                        comparison_operator="GreaterThanThreshold",
                        evaluation_periods=3,
                        datapoints_to_alarm=2,
                        statistic="Average",
                        period=300,
                        severity=AlertSeverity.MEDIUM,
                        description=f"High CPU utilization on database {db_instance}"
                    )
                    alarm_arns.append(self._create_cloudwatch_alarm(db_cpu_metric, f"RDS-CPU-{db_instance}"))

            # Load Balancer Monitoring
            if 'load_balancers' in resources:
                for lb_name in resources['load_balancers']:
                    # Target Response Time
                    response_metric = MonitoringMetric(
                        name="TargetResponseTime",
                        namespace="AWS/ApplicationELB",
                        dimensions={"LoadBalancer": lb_name},
                        threshold_value=2.0,
                        comparison_operator="GreaterThanThreshold",
                        evaluation_periods=2,
                        datapoints_to_alarm=2,
                        statistic="Average",
                        period=300,
                        severity=AlertSeverity.HIGH,
                        description=f"High response time on load balancer {lb_name}"
                    )
                    alarm_arns.append(self._create_cloudwatch_alarm(response_metric, f"ALB-ResponseTime-{lb_name}"))
                    
                    # HTTP 5XX Errors
                    error_metric = MonitoringMetric(
                        name="HTTPCode_Target_5XX_Count",
                        namespace="AWS/ApplicationELB",
                        dimensions={"LoadBalancer": lb_name},
                        threshold_value=10.0,
                        comparison_operator="GreaterThanThreshold",
                        evaluation_periods=1,
                        datapoints_to_alarm=1,
                        statistic="Sum",
                        period=300,
                        severity=AlertSeverity.CRITICAL,
                        description=f"High 5XX error rate on load balancer {lb_name}"
                    )
                    alarm_arns.append(self._create_cloudwatch_alarm(error_metric, f"ALB-5XX-{lb_name}"))

            self.logger.info(f"Created {len(alarm_arns)} infrastructure monitoring alarms")
            return alarm_arns
            
        except Exception as e:
            self.logger.error(f"Infrastructure monitoring setup failed: {str(e)}")
            return alarm_arns

    def setup_application_monitoring(self, applications: List[Dict[str, Any]]) -> List[str]:
        """Set up application performance monitoring"""
        alarm_arns = []
        
        try:
            for app in applications:
                app_name = app['name']
                namespace = app.get('namespace', f'Application/{app_name}')
                
                # Application Error Rate
                error_metric = MonitoringMetric(
                    name="ErrorRate",
                    namespace=namespace,
                    dimensions={"Application": app_name},
                    threshold_value=5.0,
                    comparison_operator="GreaterThanThreshold",
                    evaluation_periods=2,
                    datapoints_to_alarm=2,
                    statistic="Average",
                    period=300,
                    severity=AlertSeverity.HIGH,
                    description=f"High error rate in application {app_name}"
                )
                alarm_arns.append(self._create_cloudwatch_alarm(error_metric, f"App-ErrorRate-{app_name}"))
                
                # Response Time
                latency_metric = MonitoringMetric(
                    name="ResponseTime",
                    namespace=namespace,
                    dimensions={"Application": app_name},
                    threshold_value=app.get('response_time_threshold', 1000),
                    comparison_operator="GreaterThanThreshold",
                    evaluation_periods=3,
                    datapoints_to_alarm=2,
                    statistic="Average",
                    period=300,
                    severity=AlertSeverity.MEDIUM,
                    description=f"High response time in application {app_name}"
                )
                alarm_arns.append(self._create_cloudwatch_alarm(latency_metric, f"App-Latency-{app_name}"))
                
                # Throughput (Requests per minute)
                throughput_metric = MonitoringMetric(
                    name="RequestCount",
                    namespace=namespace,
                    dimensions={"Application": app_name},
                    threshold_value=app.get('min_throughput', 10),
                    comparison_operator="LessThanThreshold",
                    evaluation_periods=3,
                    datapoints_to_alarm=3,
                    statistic="Sum",
                    period=300,
                    severity=AlertSeverity.MEDIUM,
                    description=f"Low throughput in application {app_name}"
                )
                alarm_arns.append(self._create_cloudwatch_alarm(throughput_metric, f"App-Throughput-{app_name}"))

            self.logger.info(f"Created {len(alarm_arns)} application monitoring alarms")
            return alarm_arns
            
        except Exception as e:
            self.logger.error(f"Application monitoring setup failed: {str(e)}")
            return alarm_arns

    def setup_business_metrics_monitoring(self, business_metrics: List[Dict[str, Any]]) -> List[str]:
        """Set up business metrics monitoring"""
        alarm_arns = []
        
        try:
            for metric_config in business_metrics:
                metric_name = metric_config['name']
                namespace = metric_config.get('namespace', 'Business/Metrics')
                
                business_metric = MonitoringMetric(
                    name=metric_name,
                    namespace=namespace,
                    dimensions=metric_config.get('dimensions', {}),
                    threshold_value=metric_config['threshold'],
                    comparison_operator=metric_config.get('comparison', 'LessThanThreshold'),
                    evaluation_periods=metric_config.get('evaluation_periods', 2),
                    datapoints_to_alarm=metric_config.get('datapoints_to_alarm', 2),
                    statistic=metric_config.get('statistic', 'Average'),
                    period=metric_config.get('period', 300),
                    severity=AlertSeverity(metric_config.get('severity', 'medium')),
                    description=metric_config.get('description', f'Business metric {metric_name} threshold breach')
                )
                
                alarm_arns.append(self._create_cloudwatch_alarm(business_metric, f"Business-{metric_name}"))

            self.logger.info(f"Created {len(alarm_arns)} business metrics monitoring alarms")
            return alarm_arns
            
        except Exception as e:
            self.logger.error(f"Business metrics monitoring setup failed: {str(e)}")
            return alarm_arns

    def setup_synthetic_monitoring(self, canaries: List[SyntheticCanary]) -> List[str]:
        """Set up synthetic monitoring with canaries"""
        canary_arns = []
        
        try:
            for canary in canaries:
                # Create canary script
                canary_script = self._generate_canary_script(canary)
                
                # Create the canary
                response = self.synthetics.create_canary(
                    Name=canary.name,
                    Code={
                        'ZipFile': canary_script
                    },
                    ExecutionRoleArn=self._get_canary_execution_role(),
                    Schedule={
                        'Expression': f'rate({canary.frequency} minutes)'
                    },
                    RunConfig={
                        'TimeoutInSeconds': canary.timeout,
                        'MemoryInMB': 960
                    },
                    SuccessRetentionPeriodInDays=30,
                    FailureRetentionPeriodInDays=30,
                    RuntimeVersion='syn-nodejs-puppeteer-3.8',
                    Tags={
                        'Purpose': 'SyntheticMonitoring',
                        'Environment': 'production'
                    }
                )
                
                canary_arns.append(response['Canary']['Id'])
                
                # Create alarm for canary failures
                canary_alarm = MonitoringMetric(
                    name="SuccessPercent",
                    namespace="CloudWatchSynthetics",
                    dimensions={"CanaryName": canary.name},
                    threshold_value=90.0,
                    comparison_operator="LessThanThreshold",
                    evaluation_periods=2,
                    datapoints_to_alarm=2,
                    statistic="Average",
                    period=300,
                    severity=AlertSeverity.HIGH,
                    description=f"Synthetic canary {canary.name} success rate below threshold"
                )
                
                self._create_cloudwatch_alarm(canary_alarm, f"Canary-{canary.name}")

            self.logger.info(f"Created {len(canary_arns)} synthetic monitoring canaries")
            return canary_arns
            
        except Exception as e:
            self.logger.error(f"Synthetic monitoring setup failed: {str(e)}")
            return canary_arns

    def setup_log_monitoring(self, log_groups: List[Dict[str, Any]]) -> List[str]:
        """Set up log-based monitoring and alerting"""
        alarm_arns = []
        
        try:
            for log_config in log_groups:
                log_group_name = log_config['log_group']
                
                # Create metric filters for error patterns
                for pattern_config in log_config.get('error_patterns', []):
                    filter_name = f"{log_group_name.replace('/', '-')}-{pattern_config['name']}"
                    
                    # Create metric filter
                    self.logs.put_metric_filter(
                        logGroupName=log_group_name,
                        filterName=filter_name,
                        filterPattern=pattern_config['pattern'],
                        metricTransformations=[
                            {
                                'metricName': pattern_config['metric_name'],
                                'metricNamespace': 'Logs/Errors',
                                'metricValue': '1',
                                'defaultValue': 0
                            }
                        ]
                    )
                    
                    # Create alarm for the metric
                    log_metric = MonitoringMetric(
                        name=pattern_config['metric_name'],
                        namespace='Logs/Errors',
                        dimensions={},
                        threshold_value=pattern_config.get('threshold', 1),
                        comparison_operator="GreaterThanOrEqualToThreshold",
                        evaluation_periods=1,
                        datapoints_to_alarm=1,
                        statistic="Sum",
                        period=300,
                        severity=AlertSeverity(pattern_config.get('severity', 'high')),
                        description=f"Error pattern detected in {log_group_name}: {pattern_config['name']}"
                    )
                    
                    alarm_arns.append(self._create_cloudwatch_alarm(log_metric, f"Log-{filter_name}"))

            self.logger.info(f"Created {len(alarm_arns)} log monitoring alarms")
            return alarm_arns
            
        except Exception as e:
            self.logger.error(f"Log monitoring setup failed: {str(e)}")
            return alarm_arns

    def _create_cloudwatch_alarm(self, metric: MonitoringMetric, alarm_name: str) -> str:
        """Create a CloudWatch alarm"""
        try:
            response = self.cloudwatch.put_metric_alarm(
                AlarmName=alarm_name,
                ComparisonOperator=metric.comparison_operator,
                EvaluationPeriods=metric.evaluation_periods,
                MetricName=metric.name,
                Namespace=metric.namespace,
                Period=metric.period,
                Statistic=metric.statistic,
                Threshold=metric.threshold_value,
                ActionsEnabled=True,
                AlarmActions=[
                    self._get_sns_topic_arn(metric.severity)
                ],
                AlarmDescription=metric.description,
                Dimensions=[
                    {
                        'Name': key,
                        'Value': value
                    }
                    for key, value in metric.dimensions.items()
                ],
                Unit='None',
                DatapointsToAlarm=metric.datapoints_to_alarm,
                TreatMissingData='breaching'
            )
            
            return response['ResponseMetadata']['RequestId']
            
        except Exception as e:
            self.logger.error(f"Failed to create alarm {alarm_name}: {str(e)}")
            return ""

    def _generate_canary_script(self, canary: SyntheticCanary) -> bytes:
        """Generate canary script for synthetic monitoring"""
        script_template = f"""
const synthetics = require('Synthetics');
const log = require('SyntheticsLogger');

const checkEndpoint = async function () {{
    const page = await synthetics.getPage();
    
    try {{
        const response = await page.goto('{canary.endpoint}', {{
            waitUntil: 'networkidle0',
            timeout: {canary.timeout * 1000}
        }});
        
        // Check status code
        if (response.status() !== {canary.expected_status}) {{
            throw new Error(`Expected status {canary.expected_status}, got ${{response.status()}}`);
        }}
        
        // Run custom assertions
        {self._generate_assertions(canary.assertions)}
        
        log.info('Canary check passed successfully');
        
    }} catch (error) {{
        log.error('Canary check failed:', error);
        throw error;
    }}
}};

exports.handler = async () => {{
    return await synthetics.executeStep('checkEndpoint', checkEndpoint);
}};
"""
        return script_template.encode('utf-8')

    def _generate_assertions(self, assertions: List[Dict[str, Any]]) -> str:
        """Generate assertion code for canary"""
        assertion_code = ""
        for assertion in assertions:
            if assertion['type'] == 'text_contains':
                assertion_code += f"""
        const content = await page.content();
        if (!content.includes('{assertion['value']}')) {{
            throw new Error('Page does not contain expected text: {assertion['value']}');
        }}
"""
            elif assertion['type'] == 'element_exists':
                assertion_code += f"""
        const element = await page.$('{assertion['selector']}');
        if (!element) {{
            throw new Error('Element not found: {assertion['selector']}');
        }}
"""
        return assertion_code

    def _get_sns_topic_arn(self, severity: AlertSeverity) -> str:
        """Get SNS topic ARN based on alert severity"""
        topic_mapping = {
            AlertSeverity.CRITICAL: f"arn:aws:sns:{self.region}:123456789012:critical-alerts",
            AlertSeverity.HIGH: f"arn:aws:sns:{self.region}:123456789012:high-alerts",
            AlertSeverity.MEDIUM: f"arn:aws:sns:{self.region}:123456789012:medium-alerts",
            AlertSeverity.LOW: f"arn:aws:sns:{self.region}:123456789012:low-alerts",
            AlertSeverity.INFO: f"arn:aws:sns:{self.region}:123456789012:info-alerts"
        }
        return topic_mapping.get(severity, topic_mapping[AlertSeverity.MEDIUM])

    def _get_canary_execution_role(self) -> str:
        """Get or create execution role for canaries"""
        return f"arn:aws:iam::123456789012:role/CloudWatchSyntheticsRole"

    def create_monitoring_dashboard(self, dashboard_name: str, widgets: List[Dict[str, Any]]) -> str:
        """Create CloudWatch dashboard for monitoring overview"""
        try:
            dashboard_body = {
                "widgets": widgets
            }
            
            response = self.cloudwatch.put_dashboard(
                DashboardName=dashboard_name,
                DashboardBody=json.dumps(dashboard_body)
            )
            
            self.logger.info(f"Created monitoring dashboard: {dashboard_name}")
            return response['DashboardArn']
            
        except Exception as e:
            self.logger.error(f"Dashboard creation failed: {str(e)}")
            return ""

# Example usage
def main():
    # Initialize monitoring system
    monitoring = ComprehensiveMonitoringSystem(region='us-east-1')
    
    # Define resources to monitor
    resources = {
        'ec2_instances': ['i-1234567890abcdef0', 'i-0987654321fedcba0'],
        'rds_instances': ['myapp-prod-db', 'myapp-staging-db'],
        'load_balancers': ['app/myapp-alb/1234567890123456']
    }
    
    # Define applications to monitor
    applications = [
        {
            'name': 'web-app',
            'namespace': 'MyApp/WebTier',
            'response_time_threshold': 2000,
            'min_throughput': 50
        },
        {
            'name': 'api-service',
            'namespace': 'MyApp/APITier',
            'response_time_threshold': 1000,
            'min_throughput': 100
        }
    ]
    
    # Define business metrics
    business_metrics = [
        {
            'name': 'OrdersPerMinute',
            'namespace': 'Business/Orders',
            'threshold': 10,
            'comparison': 'LessThanThreshold',
            'severity': 'high',
            'description': 'Order rate below expected threshold'
        },
        {
            'name': 'RevenuePerHour',
            'namespace': 'Business/Revenue',
            'threshold': 1000,
            'comparison': 'LessThanThreshold',
            'severity': 'medium',
            'description': 'Revenue rate below expected threshold'
        }
    ]
    
    # Define synthetic canaries
    canaries = [
        SyntheticCanary(
            name='homepage-check',
            endpoint='https://myapp.example.com',
            method='GET',
            expected_status=200,
            timeout=30,
            frequency=5,
            locations=['us-east-1', 'us-west-2'],
            assertions=[
                {'type': 'text_contains', 'value': 'Welcome'},
                {'type': 'element_exists', 'selector': '#main-content'}
            ]
        ),
        SyntheticCanary(
            name='api-health-check',
            endpoint='https://api.myapp.example.com/health',
            method='GET',
            expected_status=200,
            timeout=15,
            frequency=2,
            locations=['us-east-1'],
            assertions=[
                {'type': 'text_contains', 'value': '"status":"healthy"'}
            ]
        )
    ]
    
    # Define log monitoring
    log_groups = [
        {
            'log_group': '/aws/lambda/myapp-function',
            'error_patterns': [
                {
                    'name': 'errors',
                    'pattern': 'ERROR',
                    'metric_name': 'LambdaErrors',
                    'threshold': 5,
                    'severity': 'high'
                },
                {
                    'name': 'timeouts',
                    'pattern': 'Task timed out',
                    'metric_name': 'LambdaTimeouts',
                    'threshold': 1,
                    'severity': 'critical'
                }
            ]
        }
    ]
    
    # Set up monitoring
    print("Setting up comprehensive monitoring...")
    
    infra_alarms = monitoring.setup_infrastructure_monitoring(resources)
    app_alarms = monitoring.setup_application_monitoring(applications)
    business_alarms = monitoring.setup_business_metrics_monitoring(business_metrics)
    canary_ids = monitoring.setup_synthetic_monitoring(canaries)
    log_alarms = monitoring.setup_log_monitoring(log_groups)
    
    print(f"Monitoring setup complete:")
    print(f"- Infrastructure alarms: {len(infra_alarms)}")
    print(f"- Application alarms: {len(app_alarms)}")
    print(f"- Business metric alarms: {len(business_alarms)}")
    print(f"- Synthetic canaries: {len(canary_ids)}")
    print(f"- Log monitoring alarms: {len(log_alarms)}")

if __name__ == "__main__":
    main()
```
{% endraw %}

## AWS Services

### Primary Services
- **Amazon CloudWatch**: Core monitoring service for metrics, alarms, and dashboards
- **Amazon CloudWatch Synthetics**: Synthetic monitoring with canaries
- **Amazon CloudWatch Logs**: Log aggregation and analysis
- **AWS X-Ray**: Distributed tracing for application insights

### Supporting Services
- **Amazon SNS**: Notification delivery for alerts
- **AWS Lambda**: Custom monitoring logic and automated responses
- **Amazon EventBridge**: Event-driven monitoring workflows
- **AWS Systems Manager**: Operational insights and parameter management

## Benefits

- **Early Detection**: Identify issues before they impact users
- **Comprehensive Coverage**: Monitor all layers from infrastructure to business metrics
- **Automated Response**: Trigger recovery mechanisms automatically
- **Operational Insights**: Gain deep understanding of system behavior
- **Compliance**: Meet monitoring requirements for regulatory standards

## Related Resources

- [Amazon CloudWatch User Guide](https://docs.aws.amazon.com/cloudwatch/)
- [CloudWatch Synthetics User Guide](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries.html)
- [AWS X-Ray Developer Guide](https://docs.aws.amazon.com/xray/)
- [CloudWatch Logs User Guide](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/)
