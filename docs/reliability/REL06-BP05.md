---
title: REL06-BP05 - Create dashboards
layout: default
parent: REL06 - How do you monitor workload resources?
grand_parent: Reliability
nav_order: 5
---

# REL06-BP05: Create dashboards

## Overview

Design and implement comprehensive dashboards that provide real-time visibility into workload health, performance, and business metrics. Effective dashboards enable quick identification of issues, support data-driven decision making, and facilitate proactive system management.

## Implementation Steps

### 1. Design Dashboard Architecture
- Define dashboard hierarchy and organization structure
- Establish role-based dashboard access and customization
- Design responsive layouts for different devices and screen sizes
- Implement dashboard templates and standardization

### 2. Implement Real-time Data Visualization
- Configure live data feeds and streaming updates
- Design interactive charts, graphs, and visual indicators
- Implement drill-down capabilities and detailed views
- Establish data refresh rates and caching strategies

### 3. Create Multi-layered Dashboard Views
- Design executive summary dashboards for high-level overview
- Implement operational dashboards for day-to-day monitoring
- Create technical dashboards for detailed system analysis
- Establish incident response dashboards for emergency situations

### 4. Configure Alert Integration and Status Indicators
- Integrate alert status and severity indicators
- Implement visual alert escalation and acknowledgment
- Design status boards and health indicators
- Establish trend analysis and predictive indicators

### 5. Implement Dashboard Customization and Personalization
- Enable user-specific dashboard customization
- Implement saved views and bookmark functionality
- Design collaborative features and shared dashboards
- Establish dashboard versioning and change management

### 6. Monitor Dashboard Usage and Effectiveness
- Track dashboard access patterns and user engagement
- Monitor dashboard performance and load times
- Implement feedback collection and improvement processes
- Establish dashboard governance and maintenance procedures

## Implementation Examples

### Example 1: Comprehensive Dashboard Management System
```python
import boto3
import json
import logging
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from enum import Enum
import time
import uuid

class DashboardType(Enum):
    EXECUTIVE = "executive"
    OPERATIONAL = "operational"
    TECHNICAL = "technical"
    INCIDENT = "incident"
    BUSINESS = "business"

class VisualizationType(Enum):
    LINE_CHART = "line_chart"
    BAR_CHART = "bar_chart"
    PIE_CHART = "pie_chart"
    GAUGE = "gauge"
    TABLE = "table"
    HEATMAP = "heatmap"
    SINGLE_VALUE = "single_value"
    ALERT_STATUS = "alert_status"

class RefreshRate(Enum):
    REAL_TIME = 1  # seconds
    FAST = 30
    NORMAL = 300  # 5 minutes
    SLOW = 1800   # 30 minutes

@dataclass
class Widget:
    widget_id: str
    title: str
    description: str
    visualization_type: VisualizationType
    data_source: Dict[str, Any]
    configuration: Dict[str, Any]
    position: Dict[str, int]  # x, y, width, height
    refresh_rate: RefreshRate
    alert_thresholds: Optional[Dict[str, Any]] = None
    drill_down_config: Optional[Dict[str, Any]] = None

@dataclass
class Dashboard:
    dashboard_id: str
    name: str
    description: str
    dashboard_type: DashboardType
    widgets: List[Widget]
    layout_config: Dict[str, Any]
    access_permissions: List[str]
    tags: List[str]
    created_at: datetime
    updated_at: datetime
    created_by: str
    is_public: bool
    auto_refresh: bool

@dataclass
class DashboardUsage:
    usage_id: str
    dashboard_id: str
    user_id: str
    access_time: datetime
    session_duration: int
    interactions: List[Dict[str, Any]]
    device_info: Dict[str, str]

class DashboardManager:
    """Comprehensive dashboard management system"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
        # AWS clients
        self.cloudwatch = boto3.client('cloudwatch')
        self.quicksight = boto3.client('quicksight')
        self.s3 = boto3.client('s3')
        self.dynamodb = boto3.resource('dynamodb')
        self.lambda_client = boto3.client('lambda')
        
        # Storage
        self.dashboards_table = self.dynamodb.Table(config.get('dashboards_table', 'dashboards'))
        self.usage_table = self.dynamodb.Table(config.get('usage_table', 'dashboard-usage'))
        self.widgets_table = self.dynamodb.Table(config.get('widgets_table', 'dashboard-widgets'))
        
        # Dashboard registry
        self.dashboards = {}
        self.widget_templates = {}
        
        # Load existing dashboards
        self.load_dashboards()
        
    def load_dashboards(self):
        """Load existing dashboards from storage"""
        try:
            response = self.dashboards_table.scan()
            
            for item in response['Items']:
                # Convert datetime strings back to datetime objects
                item['created_at'] = datetime.fromisoformat(item['created_at'])
                item['updated_at'] = datetime.fromisoformat(item['updated_at'])
                
                dashboard = Dashboard(**item)
                self.dashboards[dashboard.dashboard_id] = dashboard
            
            logging.info(f"Loaded {len(self.dashboards)} dashboards")
            
        except Exception as e:
            logging.error(f"Failed to load dashboards: {str(e)}")
    
    async def create_dashboard(self, dashboard_config: Dict[str, Any]) -> str:
        """Create a new dashboard"""
        try:
            dashboard_id = str(uuid.uuid4())
            
            # Create widgets
            widgets = []
            for widget_config in dashboard_config.get('widgets', []):
                widget = Widget(
                    widget_id=str(uuid.uuid4()),
                    title=widget_config['title'],
                    description=widget_config.get('description', ''),
                    visualization_type=VisualizationType(widget_config['visualization_type']),
                    data_source=widget_config['data_source'],
                    configuration=widget_config.get('configuration', {}),
                    position=widget_config['position'],
                    refresh_rate=RefreshRate(widget_config.get('refresh_rate', 300)),
                    alert_thresholds=widget_config.get('alert_thresholds'),
                    drill_down_config=widget_config.get('drill_down_config')
                )
                widgets.append(widget)
            
            # Create dashboard
            dashboard = Dashboard(
                dashboard_id=dashboard_id,
                name=dashboard_config['name'],
                description=dashboard_config.get('description', ''),
                dashboard_type=DashboardType(dashboard_config['dashboard_type']),
                widgets=widgets,
                layout_config=dashboard_config.get('layout_config', {}),
                access_permissions=dashboard_config.get('access_permissions', []),
                tags=dashboard_config.get('tags', []),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                created_by=dashboard_config['created_by'],
                is_public=dashboard_config.get('is_public', False),
                auto_refresh=dashboard_config.get('auto_refresh', True)
            )
            
            # Store dashboard
            await self._store_dashboard(dashboard)
            
            # Store widgets
            for widget in widgets:
                await self._store_widget(widget, dashboard_id)
            
            # Create CloudWatch dashboard if configured
            if dashboard_config.get('create_cloudwatch_dashboard', False):
                await self._create_cloudwatch_dashboard(dashboard)
            
            self.dashboards[dashboard_id] = dashboard
            
            logging.info(f"Created dashboard {dashboard_id}: {dashboard.name}")
            return dashboard_id
            
        except Exception as e:
            logging.error(f"Failed to create dashboard: {str(e)}")
            raise
    
    async def get_dashboard_data(self, dashboard_id: str, user_id: str) -> Dict[str, Any]:
        """Get dashboard data with real-time updates"""
        try:
            dashboard = self.dashboards.get(dashboard_id)
            if not dashboard:
                raise ValueError(f"Dashboard {dashboard_id} not found")
            
            # Check permissions
            if not self._check_dashboard_access(dashboard, user_id):
                raise PermissionError(f"User {user_id} does not have access to dashboard {dashboard_id}")
            
            # Get widget data
            widget_data = {}
            for widget in dashboard.widgets:
                data = await self._get_widget_data(widget)
                widget_data[widget.widget_id] = data
            
            # Record usage
            await self._record_dashboard_usage(dashboard_id, user_id, 'view')
            
            return {
                'dashboard': asdict(dashboard),
                'widget_data': widget_data,
                'last_updated': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logging.error(f"Failed to get dashboard data: {str(e)}")
            raise
    
    async def _get_widget_data(self, widget: Widget) -> Dict[str, Any]:
        """Get data for a specific widget"""
        try:
            data_source = widget.data_source
            source_type = data_source.get('type')
            
            if source_type == 'cloudwatch_metric':
                return await self._get_cloudwatch_metric_data(widget)
            elif source_type == 'custom_api':
                return await self._get_custom_api_data(widget)
            elif source_type == 'database_query':
                return await self._get_database_query_data(widget)
            elif source_type == 'lambda_function':
                return await self._get_lambda_function_data(widget)
            else:
                return {'error': f'Unknown data source type: {source_type}'}
                
        except Exception as e:
            logging.error(f"Failed to get widget data: {str(e)}")
            return {'error': str(e)}
    
    async def _get_cloudwatch_metric_data(self, widget: Widget) -> Dict[str, Any]:
        """Get CloudWatch metric data for widget"""
        try:
            data_source = widget.data_source
            
            # Build metric query
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(hours=data_source.get('time_range_hours', 24))
            
            response = self.cloudwatch.get_metric_statistics(
                Namespace=data_source['namespace'],
                MetricName=data_source['metric_name'],
                Dimensions=data_source.get('dimensions', []),
                StartTime=start_time,
                EndTime=end_time,
                Period=data_source.get('period', 300),
                Statistics=data_source.get('statistics', ['Average'])
            )
            
            # Format data for visualization
            datapoints = sorted(response['Datapoints'], key=lambda x: x['Timestamp'])
            
            formatted_data = {
                'timestamps': [dp['Timestamp'].isoformat() for dp in datapoints],
                'values': [dp.get('Average', dp.get('Sum', dp.get('Maximum', 0))) for dp in datapoints],
                'unit': response.get('Unit', ''),
                'metric_name': data_source['metric_name']
            }
            
            # Add alert status if thresholds are configured
            if widget.alert_thresholds and formatted_data['values']:
                latest_value = formatted_data['values'][-1]
                formatted_data['alert_status'] = self._evaluate_alert_thresholds(
                    latest_value, widget.alert_thresholds
                )
            
            return formatted_data
            
        except Exception as e:
            logging.error(f"Failed to get CloudWatch metric data: {str(e)}")
            return {'error': str(e)}
    
    async def _get_custom_api_data(self, widget: Widget) -> Dict[str, Any]:
        """Get data from custom API endpoint"""
        try:
            import aiohttp
            
            data_source = widget.data_source
            url = data_source['url']
            headers = data_source.get('headers', {})
            params = data_source.get('params', {})
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._format_api_data(data, widget.configuration)
                    else:
                        return {'error': f'API request failed with status {response.status}'}
                        
        except Exception as e:
            logging.error(f"Failed to get custom API data: {str(e)}")
            return {'error': str(e)}
    
    async def _get_lambda_function_data(self, widget: Widget) -> Dict[str, Any]:
        """Get data from Lambda function"""
        try:
            data_source = widget.data_source
            function_name = data_source['function_name']
            payload = data_source.get('payload', {})
            
            response = self.lambda_client.invoke(
                FunctionName=function_name,
                InvocationType='RequestResponse',
                Payload=json.dumps(payload)
            )
            
            result = json.loads(response['Payload'].read())
            
            if response['StatusCode'] == 200:
                return self._format_lambda_data(result, widget.configuration)
            else:
                return {'error': f'Lambda function failed: {result}'}
                
        except Exception as e:
            logging.error(f"Failed to get Lambda function data: {str(e)}")
            return {'error': str(e)}
    
    def _format_api_data(self, raw_data: Any, config: Dict[str, Any]) -> Dict[str, Any]:
        """Format API data for visualization"""
        try:
            # Apply data transformation based on configuration
            if config.get('data_path'):
                # Extract data from nested structure
                data = raw_data
                for key in config['data_path'].split('.'):
                    data = data[key]
            else:
                data = raw_data
            
            # Apply formatting rules
            if config.get('format_as_time_series'):
                return {
                    'timestamps': [item[config['timestamp_field']] for item in data],
                    'values': [item[config['value_field']] for item in data]
                }
            
            return {'data': data}
            
        except Exception as e:
            logging.error(f"Failed to format API data: {str(e)}")
            return {'error': str(e)}
    
    def _evaluate_alert_thresholds(self, value: float, thresholds: Dict[str, Any]) -> str:
        """Evaluate alert thresholds and return status"""
        critical_threshold = thresholds.get('critical')
        warning_threshold = thresholds.get('warning')
        
        if critical_threshold and value >= critical_threshold:
            return 'critical'
        elif warning_threshold and value >= warning_threshold:
            return 'warning'
        else:
            return 'ok'
    
    async def create_executive_dashboard(self, workload_name: str, created_by: str) -> str:
        """Create an executive summary dashboard"""
        dashboard_config = {
            'name': f'{workload_name} - Executive Summary',
            'description': f'High-level overview of {workload_name} health and performance',
            'dashboard_type': 'executive',
            'created_by': created_by,
            'widgets': [
                {
                    'title': 'System Health Score',
                    'visualization_type': 'gauge',
                    'data_source': {
                        'type': 'lambda_function',
                        'function_name': 'calculate-health-score',
                        'payload': {'workload': workload_name}
                    },
                    'position': {'x': 0, 'y': 0, 'width': 6, 'height': 4},
                    'configuration': {
                        'min_value': 0,
                        'max_value': 100,
                        'color_ranges': [
                            {'min': 0, 'max': 60, 'color': 'red'},
                            {'min': 60, 'max': 80, 'color': 'yellow'},
                            {'min': 80, 'max': 100, 'color': 'green'}
                        ]
                    }
                },
                {
                    'title': 'Active Incidents',
                    'visualization_type': 'single_value',
                    'data_source': {
                        'type': 'custom_api',
                        'url': f'/api/incidents/count?workload={workload_name}&status=active'
                    },
                    'position': {'x': 6, 'y': 0, 'width': 3, 'height': 2},
                    'alert_thresholds': {'warning': 1, 'critical': 3}
                },
                {
                    'title': 'Monthly Cost Trend',
                    'visualization_type': 'line_chart',
                    'data_source': {
                        'type': 'cloudwatch_metric',
                        'namespace': 'AWS/Billing',
                        'metric_name': 'EstimatedCharges',
                        'dimensions': [{'Name': 'Currency', 'Value': 'USD'}],
                        'time_range_hours': 720  # 30 days
                    },
                    'position': {'x': 0, 'y': 4, 'width': 12, 'height': 4}
                }
            ],
            'layout_config': {
                'grid_size': 12,
                'row_height': 60
            },
            'access_permissions': ['executives', 'managers'],
            'tags': ['executive', 'summary', workload_name]
        }
        
        return await self.create_dashboard(dashboard_config)
    
    async def create_operational_dashboard(self, workload_name: str, created_by: str) -> str:
        """Create an operational monitoring dashboard"""
        dashboard_config = {
            'name': f'{workload_name} - Operations',
            'description': f'Operational monitoring for {workload_name}',
            'dashboard_type': 'operational',
            'created_by': created_by,
            'widgets': [
                {
                    'title': 'Request Rate',
                    'visualization_type': 'line_chart',
                    'data_source': {
                        'type': 'cloudwatch_metric',
                        'namespace': 'AWS/ApplicationELB',
                        'metric_name': 'RequestCount',
                        'time_range_hours': 24
                    },
                    'position': {'x': 0, 'y': 0, 'width': 6, 'height': 4}
                },
                {
                    'title': 'Error Rate',
                    'visualization_type': 'line_chart',
                    'data_source': {
                        'type': 'cloudwatch_metric',
                        'namespace': 'AWS/ApplicationELB',
                        'metric_name': 'HTTPCode_ELB_5XX_Count',
                        'time_range_hours': 24
                    },
                    'position': {'x': 6, 'y': 0, 'width': 6, 'height': 4},
                    'alert_thresholds': {'warning': 10, 'critical': 50}
                },
                {
                    'title': 'Response Time',
                    'visualization_type': 'line_chart',
                    'data_source': {
                        'type': 'cloudwatch_metric',
                        'namespace': 'AWS/ApplicationELB',
                        'metric_name': 'TargetResponseTime',
                        'time_range_hours': 24
                    },
                    'position': {'x': 0, 'y': 4, 'width': 6, 'height': 4},
                    'alert_thresholds': {'warning': 1.0, 'critical': 2.0}
                },
                {
                    'title': 'Active Connections',
                    'visualization_type': 'single_value',
                    'data_source': {
                        'type': 'cloudwatch_metric',
                        'namespace': 'AWS/ApplicationELB',
                        'metric_name': 'ActiveConnectionCount',
                        'statistics': ['Sum']
                    },
                    'position': {'x': 6, 'y': 4, 'width': 3, 'height': 2}
                }
            ],
            'access_permissions': ['operators', 'engineers'],
            'tags': ['operational', 'monitoring', workload_name]
        }
        
        return await self.create_dashboard(dashboard_config)
    
    def _check_dashboard_access(self, dashboard: Dashboard, user_id: str) -> bool:
        """Check if user has access to dashboard"""
        if dashboard.is_public:
            return True
        
        # In a real implementation, this would check user roles/permissions
        # For now, we'll assume access is granted
        return True
    
    async def _record_dashboard_usage(self, dashboard_id: str, user_id: str, action: str):
        """Record dashboard usage for analytics"""
        try:
            usage = DashboardUsage(
                usage_id=str(uuid.uuid4()),
                dashboard_id=dashboard_id,
                user_id=user_id,
                access_time=datetime.utcnow(),
                session_duration=0,  # Will be updated on session end
                interactions=[{'action': action, 'timestamp': datetime.utcnow().isoformat()}],
                device_info={'user_agent': 'dashboard_manager'}  # Would get from request
            )
            
            usage_dict = asdict(usage)
            usage_dict['access_time'] = usage.access_time.isoformat()
            
            self.usage_table.put_item(Item=usage_dict)
            
        except Exception as e:
            logging.error(f"Failed to record dashboard usage: {str(e)}")
    
    async def _store_dashboard(self, dashboard: Dashboard):
        """Store dashboard in DynamoDB"""
        try:
            dashboard_dict = asdict(dashboard)
            dashboard_dict['created_at'] = dashboard.created_at.isoformat()
            dashboard_dict['updated_at'] = dashboard.updated_at.isoformat()
            
            # Convert widgets to dict format
            dashboard_dict['widgets'] = [asdict(widget) for widget in dashboard.widgets]
            
            self.dashboards_table.put_item(Item=dashboard_dict)
            
        except Exception as e:
            logging.error(f"Failed to store dashboard: {str(e)}")
            raise
    
    async def _store_widget(self, widget: Widget, dashboard_id: str):
        """Store widget configuration"""
        try:
            widget_dict = asdict(widget)
            widget_dict['dashboard_id'] = dashboard_id
            
            self.widgets_table.put_item(Item=widget_dict)
            
        except Exception as e:
            logging.error(f"Failed to store widget: {str(e)}")

# Usage example
async def main():
    config = {
        'dashboards_table': 'dashboards',
        'usage_table': 'dashboard-usage',
        'widgets_table': 'dashboard-widgets'
    }
    
    # Initialize dashboard manager
    dashboard_manager = DashboardManager(config)
    
    # Create executive dashboard
    exec_dashboard_id = await dashboard_manager.create_executive_dashboard(
        workload_name='ecommerce-platform',
        created_by='admin@company.com'
    )
    
    print(f"Created executive dashboard: {exec_dashboard_id}")
    
    # Create operational dashboard
    ops_dashboard_id = await dashboard_manager.create_operational_dashboard(
        workload_name='ecommerce-platform',
        created_by='ops@company.com'
    )
    
    print(f"Created operational dashboard: {ops_dashboard_id}")
    
    # Get dashboard data
    dashboard_data = await dashboard_manager.get_dashboard_data(
        exec_dashboard_id, 
        'user@company.com'
    )
    
    print(f"Dashboard has {len(dashboard_data['widget_data'])} widgets")

if __name__ == "__main__":
    asyncio.run(main())
```

## AWS Services Used

- **Amazon CloudWatch**: Real-time metrics, logs, and custom dashboards
- **Amazon QuickSight**: Business intelligence dashboards and analytics
- **AWS Lambda**: Custom data processing and dashboard logic
- **Amazon DynamoDB**: Dashboard configuration and usage data storage
- **Amazon S3**: Dashboard templates and static asset storage
- **Amazon API Gateway**: Custom dashboard APIs and data endpoints
- **AWS Amplify**: Frontend dashboard hosting and deployment
- **Amazon Cognito**: User authentication and dashboard access control
- **Amazon EventBridge**: Real-time dashboard updates and notifications
- **AWS AppSync**: Real-time GraphQL APIs for dashboard data
- **Amazon ElastiCache**: Dashboard data caching and performance optimization
- **AWS X-Ray**: Application performance monitoring and tracing dashboards
- **Amazon Kinesis**: Real-time data streaming for live dashboards
- **AWS IoT Core**: IoT device monitoring and telemetry dashboards
- **Amazon Timestream**: Time-series data storage for dashboard metrics

## Benefits

- **Real-time Visibility**: Live dashboards provide immediate insight into system status
- **Informed Decision Making**: Data visualization supports better operational decisions
- **Proactive Management**: Early warning indicators enable preventive actions
- **Role-based Views**: Customized dashboards for different user roles and responsibilities
- **Improved Collaboration**: Shared dashboards facilitate team communication
- **Faster Issue Resolution**: Visual indicators help quickly identify and locate problems
- **Performance Tracking**: Historical data enables trend analysis and capacity planning
- **Cost Optimization**: Resource utilization dashboards identify optimization opportunities
- **Compliance Monitoring**: Regulatory and security compliance status visualization
- **Business Alignment**: Business metrics dashboards connect IT operations to business outcomes

## Related Resources

- [AWS Well-Architected Reliability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/)
- [Create Dashboards](https://docs.aws.amazon.com/wellarchitected/latest/framework/rel_monitor_aws_resources_create_dashboards_monitor.html)
- [Amazon CloudWatch Dashboards](https://docs.aws.amazon.com/cloudwatch/latest/monitoring/CloudWatch_Dashboards.html)
- [Amazon QuickSight User Guide](https://docs.aws.amazon.com/quicksight/latest/user/)
- [AWS Lambda User Guide](https://docs.aws.amazon.com/lambda/latest/dg/)
- [Amazon DynamoDB Developer Guide](https://docs.aws.amazon.com/dynamodb/latest/developerguide/)
- [AWS Amplify User Guide](https://docs.aws.amazon.com/amplify/latest/userguide/)
- [Amazon API Gateway Developer Guide](https://docs.aws.amazon.com/apigateway/latest/developerguide/)
- [Dashboard Design Best Practices](https://aws.amazon.com/builders-library/building-dashboards-for-operational-visibility/)
- [Observability Best Practices](https://aws.amazon.com/builders-library/implementing-health-checks/)
- [Real-time Analytics](https://aws.amazon.com/real-time-analytics/)
- [Data Visualization Guidelines](https://docs.aws.amazon.com/quicksight/latest/user/working-with-visual-types.html)
