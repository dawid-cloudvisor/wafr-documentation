---
title: REL06-BP04 - Automate responses (Real-time processing and alarming)
layout: default
parent: REL06 - How do you monitor workload resources?
grand_parent: Reliability
nav_order: 4
---

# REL06-BP04: Automate responses (Real-time processing and alarming)

## Overview

Implement automated response systems that can detect, analyze, and respond to issues without human intervention. Automated responses reduce mean time to recovery (MTTR), ensure consistent incident handling, and free up human resources for more complex problem-solving tasks.

## Implementation Steps

### 1. Design Automated Response Triggers
- Configure metric-based triggers for automated actions
- Implement event-driven response automation
- Design threshold-based and anomaly-based triggers
- Establish multi-condition triggers for complex scenarios

### 2. Implement Self-Healing Mechanisms
- Configure automatic service restarts and health recovery
- Implement auto-scaling responses to load changes
- Design automatic failover and traffic redirection
- Establish resource cleanup and optimization automation

### 3. Configure Incident Response Automation
- Implement automatic incident creation and assignment
- Configure diagnostic data collection automation
- Design automatic escalation and notification workflows
- Establish automated communication and status updates

### 4. Establish Remediation Automation
- Configure automatic infrastructure repairs and replacements
- Implement configuration drift correction automation
- Design security incident response automation
- Establish capacity management and resource optimization

### 5. Implement Response Validation and Rollback
- Configure automated validation of response actions
- Implement rollback mechanisms for failed automated responses
- Design safety checks and approval gates for critical actions
- Establish monitoring and alerting for automation failures

### 6. Monitor and Optimize Automation Effectiveness
- Track automation success rates and response times
- Monitor false positive rates and automation accuracy
- Implement feedback loops for continuous improvement
- Establish metrics for automation ROI and effectiveness

## Implementation Examples

### Example 1: Comprehensive Automated Response System
```python
import boto3
import json
import logging
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import time

class ResponseType(Enum):
    RESTART_SERVICE = "restart_service"
    SCALE_OUT = "scale_out"
    SCALE_IN = "scale_in"
    FAILOVER = "failover"
    ISOLATE_INSTANCE = "isolate_instance"
    PATCH_SYSTEM = "patch_system"
    CLEANUP_RESOURCES = "cleanup_resources"
    NOTIFY_TEAM = "notify_team"

class TriggerCondition(Enum):
    THRESHOLD_EXCEEDED = "threshold_exceeded"
    ANOMALY_DETECTED = "anomaly_detected"
    SERVICE_UNHEALTHY = "service_unhealthy"
    ERROR_RATE_HIGH = "error_rate_high"
    RESOURCE_EXHAUSTED = "resource_exhausted"

@dataclass
class AutomatedResponse:
    response_id: str
    name: str
    description: str
    response_type: ResponseType
    trigger_conditions: List[Dict[str, Any]]
    actions: List[Dict[str, Any]]
    validation_checks: List[Dict[str, Any]]
    rollback_actions: List[Dict[str, Any]]
    enabled: bool
    max_executions_per_hour: int
    requires_approval: bool

@dataclass
class ResponseExecution:
    execution_id: str
    response_id: str
    triggered_by: str
    trigger_data: Dict[str, Any]
    started_at: datetime
    completed_at: Optional[datetime]
    status: str
    actions_taken: List[str]
    validation_results: List[Dict[str, Any]]
    rollback_performed: bool
    error_message: Optional[str]

class AutomatedResponseEngine:
    """Automated response system for real-time incident handling"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
        # AWS clients
        self.cloudwatch = boto3.client('cloudwatch')
        self.ec2 = boto3.client('ec2')
        self.autoscaling = boto3.client('autoscaling')
        self.elbv2 = boto3.client('elbv2')
        self.lambda_client = boto3.client('lambda')
        self.sns = boto3.client('sns')
        self.ssm = boto3.client('ssm')
        self.dynamodb = boto3.resource('dynamodb')
        
        # Storage
        self.responses_table = self.dynamodb.Table(config.get('responses_table', 'automated-responses'))
        self.executions_table = self.dynamodb.Table(config.get('executions_table', 'response-executions'))
        
        # Response registry
        self.automated_responses = {}
        self.execution_counters = {}
        
        # Load responses
        self.load_automated_responses()
        
    def load_automated_responses(self):
        """Load automated response configurations"""
        try:
            response = self.responses_table.scan()
            
            for item in response['Items']:
                automated_response = AutomatedResponse(**item)
                self.automated_responses[automated_response.response_id] = automated_response
            
            logging.info(f"Loaded {len(self.automated_responses)} automated responses")
            
        except Exception as e:
            logging.error(f"Failed to load automated responses: {str(e)}")
    
    async def process_trigger_event(self, event_data: Dict[str, Any]) -> List[str]:
        """Process trigger event and execute matching automated responses"""
        executed_responses = []
        
        try:
            # Find matching automated responses
            matching_responses = self._find_matching_responses(event_data)
            
            # Execute responses
            for response in matching_responses:
                if await self._should_execute_response(response, event_data):
                    execution_id = await self._execute_automated_response(response, event_data)
                    if execution_id:
                        executed_responses.append(execution_id)
            
            return executed_responses
            
        except Exception as e:
            logging.error(f"Failed to process trigger event: {str(e)}")
            return []
    
    def _find_matching_responses(self, event_data: Dict[str, Any]) -> List[AutomatedResponse]:
        """Find automated responses that match the trigger event"""
        matching_responses = []
        
        for response in self.automated_responses.values():
            if not response.enabled:
                continue
            
            if self._response_matches_event(response, event_data):
                matching_responses.append(response)
        
        return matching_responses
    
    def _response_matches_event(self, response: AutomatedResponse, event_data: Dict[str, Any]) -> bool:
        """Check if response matches the trigger event"""
        for condition in response.trigger_conditions:
            if self._condition_matches_event(condition, event_data):
                return True
        return False
    
    def _condition_matches_event(self, condition: Dict[str, Any], event_data: Dict[str, Any]) -> bool:
        """Check if a specific condition matches the event"""
        condition_type = condition.get('type')
        
        if condition_type == 'metric_threshold':
            metric_name = condition.get('metric_name')
            threshold = condition.get('threshold')
            operator = condition.get('operator', '>')
            
            event_metric = event_data.get('metric_name')
            event_value = event_data.get('value', 0)
            
            if event_metric == metric_name:
                if operator == '>' and event_value > threshold:
                    return True
                elif operator == '<' and event_value < threshold:
                    return True
                elif operator == '==' and event_value == threshold:
                    return True
        
        elif condition_type == 'service_health':
            service_name = condition.get('service_name')
            expected_status = condition.get('expected_status', 'healthy')
            
            event_service = event_data.get('service_name')
            event_status = event_data.get('status')
            
            if event_service == service_name and event_status != expected_status:
                return True
        
        return False
    
    async def _should_execute_response(self, response: AutomatedResponse, event_data: Dict[str, Any]) -> bool:
        """Check if response should be executed based on rate limits and approval"""
        # Check execution rate limit
        current_hour = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
        counter_key = f"{response.response_id}_{current_hour.isoformat()}"
        
        current_count = self.execution_counters.get(counter_key, 0)
        if current_count >= response.max_executions_per_hour:
            logging.warning(f"Rate limit exceeded for response {response.response_id}")
            return False
        
        # Check if approval is required
        if response.requires_approval:
            # In a real implementation, this would check for pending approvals
            logging.info(f"Response {response.response_id} requires approval, skipping automatic execution")
            return False
        
        return True
    
    async def _execute_automated_response(self, response: AutomatedResponse, event_data: Dict[str, Any]) -> Optional[str]:
        """Execute an automated response"""
        execution_id = f"exec_{int(time.time())}_{response.response_id}"
        
        execution = ResponseExecution(
            execution_id=execution_id,
            response_id=response.response_id,
            triggered_by=event_data.get('source', 'unknown'),
            trigger_data=event_data,
            started_at=datetime.utcnow(),
            completed_at=None,
            status='running',
            actions_taken=[],
            validation_results=[],
            rollback_performed=False,
            error_message=None
        )
        
        try:
            # Store execution record
            await self._store_execution(execution)
            
            # Execute actions
            for action in response.actions:
                action_result = await self._execute_action(action, event_data)
                execution.actions_taken.append(f"{action['type']}: {action_result}")
            
            # Validate response
            validation_passed = await self._validate_response(response, execution)
            
            if not validation_passed:
                # Perform rollback
                await self._perform_rollback(response, execution)
                execution.rollback_performed = True
                execution.status = 'rolled_back'
            else:
                execution.status = 'completed'
            
            execution.completed_at = datetime.utcnow()
            
            # Update execution record
            await self._store_execution(execution)
            
            # Update execution counter
            current_hour = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
            counter_key = f"{response.response_id}_{current_hour.isoformat()}"
            self.execution_counters[counter_key] = self.execution_counters.get(counter_key, 0) + 1
            
            logging.info(f"Executed automated response {response.response_id}: {execution.status}")
            return execution_id
            
        except Exception as e:
            execution.status = 'failed'
            execution.error_message = str(e)
            execution.completed_at = datetime.utcnow()
            
            await self._store_execution(execution)
            
            logging.error(f"Failed to execute automated response {response.response_id}: {str(e)}")
            return None
    
    async def _execute_action(self, action: Dict[str, Any], event_data: Dict[str, Any]) -> str:
        """Execute a specific action"""
        action_type = action.get('type')
        
        try:
            if action_type == 'restart_service':
                return await self._restart_service_action(action, event_data)
            elif action_type == 'scale_out':
                return await self._scale_out_action(action, event_data)
            elif action_type == 'scale_in':
                return await self._scale_in_action(action, event_data)
            elif action_type == 'isolate_instance':
                return await self._isolate_instance_action(action, event_data)
            elif action_type == 'send_notification':
                return await self._send_notification_action(action, event_data)
            else:
                return f"Unknown action type: {action_type}"
                
        except Exception as e:
            logging.error(f"Action execution failed: {str(e)}")
            return f"Failed: {str(e)}"
    
    async def _restart_service_action(self, action: Dict[str, Any], event_data: Dict[str, Any]) -> str:
        """Restart service action"""
        service_name = action.get('service_name')
        restart_method = action.get('method', 'lambda')
        
        if restart_method == 'lambda':
            function_name = action.get('function_name')
            
            # Invoke Lambda function to restart service
            self.lambda_client.invoke(
                FunctionName=function_name,
                InvocationType='Event',
                Payload=json.dumps({
                    'action': 'restart',
                    'service_name': service_name,
                    'trigger_data': event_data
                })
            )
            
            return f"Initiated service restart for {service_name} via Lambda {function_name}"
        
        elif restart_method == 'ssm':
            # Use Systems Manager to restart service
            document_name = action.get('document_name', 'AWS-RestartService')
            instance_ids = action.get('instance_ids', [])
            
            response = self.ssm.send_command(
                InstanceIds=instance_ids,
                DocumentName=document_name,
                Parameters={
                    'ServiceName': [service_name]
                }
            )
            
            command_id = response['Command']['CommandId']
            return f"Initiated service restart via SSM command {command_id}"
        
        return f"Restarted service {service_name}"
    
    async def _scale_out_action(self, action: Dict[str, Any], event_data: Dict[str, Any]) -> str:
        """Scale out action"""
        asg_name = action.get('auto_scaling_group_name')
        scale_amount = action.get('scale_amount', 1)
        
        # Get current capacity
        response = self.autoscaling.describe_auto_scaling_groups(
            AutoScalingGroupNames=[asg_name]
        )
        
        if response['AutoScalingGroups']:
            asg = response['AutoScalingGroups'][0]
            current_capacity = asg['DesiredCapacity']
            new_capacity = current_capacity + scale_amount
            
            # Update desired capacity
            self.autoscaling.set_desired_capacity(
                AutoScalingGroupName=asg_name,
                DesiredCapacity=new_capacity,
                HonorCooldown=False
            )
            
            return f"Scaled out {asg_name} from {current_capacity} to {new_capacity} instances"
        
        return f"Auto Scaling Group {asg_name} not found"
    
    async def _isolate_instance_action(self, action: Dict[str, Any], event_data: Dict[str, Any]) -> str:
        """Isolate instance action"""
        instance_id = action.get('instance_id') or event_data.get('instance_id')
        
        if not instance_id:
            return "No instance ID provided for isolation"
        
        # Get instance security groups
        response = self.ec2.describe_instances(InstanceIds=[instance_id])
        
        if response['Reservations']:
            instance = response['Reservations'][0]['Instances'][0]
            security_groups = [sg['GroupId'] for sg in instance['SecurityGroups']]
            
            # Create isolation security group
            isolation_sg_response = self.ec2.create_security_group(
                GroupName=f'isolation-{instance_id}',
                Description=f'Isolation security group for {instance_id}'
            )
            
            isolation_sg_id = isolation_sg_response['GroupId']
            
            # Modify instance security groups
            self.ec2.modify_instance_attribute(
                InstanceId=instance_id,
                Groups=[isolation_sg_id]
            )
            
            return f"Isolated instance {instance_id} with security group {isolation_sg_id}"
        
        return f"Instance {instance_id} not found"
    
    async def _send_notification_action(self, action: Dict[str, Any], event_data: Dict[str, Any]) -> str:
        """Send notification action"""
        topic_arn = action.get('topic_arn')
        message = action.get('message', f"Automated response triggered: {event_data}")
        
        self.sns.publish(
            TopicArn=topic_arn,
            Message=json.dumps(message, indent=2),
            Subject=f"Automated Response: {action.get('subject', 'System Alert')}"
        )
        
        return f"Sent notification to {topic_arn}"
    
    async def _validate_response(self, response: AutomatedResponse, execution: ResponseExecution) -> bool:
        """Validate that the automated response was successful"""
        try:
            for validation in response.validation_checks:
                validation_result = await self._perform_validation_check(validation, execution)
                execution.validation_results.append(validation_result)
                
                if not validation_result['passed']:
                    return False
            
            return True
            
        except Exception as e:
            logging.error(f"Validation failed: {str(e)}")
            return False
    
    async def _perform_validation_check(self, validation: Dict[str, Any], execution: ResponseExecution) -> Dict[str, Any]:
        """Perform a specific validation check"""
        check_type = validation.get('type')
        
        if check_type == 'metric_check':
            metric_name = validation.get('metric_name')
            expected_condition = validation.get('condition')
            
            # Get current metric value
            # This is simplified - in reality you'd query CloudWatch
            current_value = 50.0  # Simulated value
            
            passed = self._evaluate_condition(current_value, expected_condition)
            
            return {
                'type': check_type,
                'metric_name': metric_name,
                'current_value': current_value,
                'condition': expected_condition,
                'passed': passed
            }
        
        elif check_type == 'service_health_check':
            service_name = validation.get('service_name')
            
            # Perform health check
            # This is simplified - in reality you'd check actual service health
            is_healthy = True  # Simulated result
            
            return {
                'type': check_type,
                'service_name': service_name,
                'is_healthy': is_healthy,
                'passed': is_healthy
            }
        
        return {'type': check_type, 'passed': True}
    
    def _evaluate_condition(self, value: float, condition: Dict[str, Any]) -> bool:
        """Evaluate a condition against a value"""
        operator = condition.get('operator', '>')
        threshold = condition.get('threshold', 0)
        
        if operator == '>':
            return value > threshold
        elif operator == '<':
            return value < threshold
        elif operator == '==':
            return value == threshold
        elif operator == '>=':
            return value >= threshold
        elif operator == '<=':
            return value <= threshold
        
        return False
    
    async def _perform_rollback(self, response: AutomatedResponse, execution: ResponseExecution):
        """Perform rollback actions"""
        try:
            for rollback_action in response.rollback_actions:
                rollback_result = await self._execute_action(rollback_action, execution.trigger_data)
                execution.actions_taken.append(f"ROLLBACK {rollback_action['type']}: {rollback_result}")
            
            logging.info(f"Performed rollback for execution {execution.execution_id}")
            
        except Exception as e:
            logging.error(f"Rollback failed for execution {execution.execution_id}: {str(e)}")
    
    async def _store_execution(self, execution: ResponseExecution):
        """Store execution record in DynamoDB"""
        try:
            execution_dict = asdict(execution)
            execution_dict['started_at'] = execution.started_at.isoformat()
            if execution.completed_at:
                execution_dict['completed_at'] = execution.completed_at.isoformat()
            
            self.executions_table.put_item(Item=execution_dict)
            
        except Exception as e:
            logging.error(f"Failed to store execution record: {str(e)}")

# Usage example
async def main():
    config = {
        'responses_table': 'automated-responses',
        'executions_table': 'response-executions'
    }
    
    # Initialize response engine
    response_engine = AutomatedResponseEngine(config)
    
    # Create automated response
    high_cpu_response = AutomatedResponse(
        response_id='high_cpu_scale_out',
        name='High CPU Scale Out Response',
        description='Automatically scale out when CPU usage is high',
        response_type=ResponseType.SCALE_OUT,
        trigger_conditions=[
            {
                'type': 'metric_threshold',
                'metric_name': 'CPUUtilization',
                'threshold': 80.0,
                'operator': '>'
            }
        ],
        actions=[
            {
                'type': 'scale_out',
                'auto_scaling_group_name': 'web-servers-asg',
                'scale_amount': 2
            },
            {
                'type': 'send_notification',
                'topic_arn': 'arn:aws:sns:us-east-1:123456789012:alerts',
                'message': 'Automatically scaled out due to high CPU usage',
                'subject': 'Auto Scaling Event'
            }
        ],
        validation_checks=[
            {
                'type': 'metric_check',
                'metric_name': 'CPUUtilization',
                'condition': {'operator': '<', 'threshold': 70.0}
            }
        ],
        rollback_actions=[
            {
                'type': 'scale_in',
                'auto_scaling_group_name': 'web-servers-asg',
                'scale_amount': 2
            }
        ],
        enabled=True,
        max_executions_per_hour=3,
        requires_approval=False
    )
    
    response_engine.automated_responses['high_cpu_scale_out'] = high_cpu_response
    
    # Simulate trigger event
    trigger_event = {
        'source': 'cloudwatch',
        'metric_name': 'CPUUtilization',
        'value': 85.0,
        'instance_id': 'i-1234567890abcdef0',
        'timestamp': datetime.utcnow().isoformat()
    }
    
    # Process trigger event
    executed_responses = await response_engine.process_trigger_event(trigger_event)
    print(f"Executed {len(executed_responses)} automated responses: {executed_responses}")

if __name__ == "__main__":
    asyncio.run(main())
```

## AWS Services Used

- **AWS Lambda**: Serverless functions for automated response logic and execution
- **Amazon CloudWatch**: Metric-based triggers and automated alarm responses
- **AWS Auto Scaling**: Automatic capacity adjustments based on demand and health
- **AWS Systems Manager**: Automated patch management and configuration remediation
- **Amazon EventBridge**: Event-driven automation and response orchestration
- **AWS Step Functions**: Complex workflow automation and response coordination
- **Amazon SNS**: Automated notifications and alert escalation
- **Amazon DynamoDB**: Storage for response configurations and execution history
- **AWS Config**: Automated compliance remediation and configuration drift correction
- **Amazon EC2**: Instance management, isolation, and automated recovery
- **Elastic Load Balancing**: Automated traffic routing and health-based failover
- **AWS Security Hub**: Automated security finding remediation and response
- **Amazon GuardDuty**: Automated threat response and security incident handling
- **AWS Backup**: Automated backup and recovery operations
- **Amazon Route 53**: Automated DNS failover and health check responses

## Benefits

- **Faster Recovery**: Automated responses reduce mean time to recovery (MTTR)
- **Consistent Handling**: Standardized responses ensure consistent incident management
- **24/7 Coverage**: Automated systems provide round-the-clock monitoring and response
- **Reduced Human Error**: Automation eliminates manual mistakes during incident response
- **Cost Optimization**: Automatic resource scaling and optimization reduce costs
- **Improved Reliability**: Self-healing systems improve overall system availability
- **Resource Efficiency**: Frees up human resources for strategic and complex tasks
- **Scalable Operations**: Automated responses scale with system growth
- **Audit Trail**: Complete logging of automated actions for compliance and analysis
- **Continuous Improvement**: Response effectiveness metrics enable optimization

## Related Resources

- [AWS Well-Architected Reliability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/)
- [Automate Responses](https://docs.aws.amazon.com/wellarchitected/latest/framework/rel_monitor_aws_resources_automate_response_monitor.html)
- [AWS Lambda User Guide](https://docs.aws.amazon.com/lambda/latest/dg/)
- [Amazon CloudWatch Alarms](https://docs.aws.amazon.com/cloudwatch/latest/monitoring/AlarmThatSendsEmail.html)
- [AWS Auto Scaling User Guide](https://docs.aws.amazon.com/autoscaling/latest/userguide/)
- [AWS Systems Manager Automation](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-automation.html)
- [AWS Step Functions User Guide](https://docs.aws.amazon.com/step-functions/latest/dg/)
- [Amazon EventBridge User Guide](https://docs.aws.amazon.com/eventbridge/latest/userguide/)
- [Automated Incident Response](https://aws.amazon.com/blogs/mt/automated-incident-response-and-forensics-framework/)
- [Self-Healing Systems](https://aws.amazon.com/builders-library/implementing-health-checks/)
- [AWS Config Remediation](https://docs.aws.amazon.com/config/latest/developerguide/remediation.html)
- [Building Resilient Systems](https://aws.amazon.com/builders-library/)
