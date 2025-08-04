---
title: REL12-BP01 - Use playbooks to investigate failures
layout: default
parent: REL12 - How do you test reliability?
nav_order: 1
---

# REL12-BP01: Use playbooks to investigate failures

Develop and maintain standardized playbooks that guide teams through systematic investigation of failures. These playbooks ensure consistent, thorough analysis and faster resolution of incidents by providing step-by-step procedures, decision trees, and escalation paths.

## Implementation Steps

### 1. Create Incident Response Playbooks
Develop standardized procedures for different types of incidents and failure scenarios.

### 2. Implement Automated Diagnostics
Build automated tools that gather relevant information and perform initial analysis.

### 3. Establish Decision Trees
Create decision trees that guide responders through systematic troubleshooting.

### 4. Define Escalation Procedures
Establish clear escalation paths and communication protocols.

### 5. Maintain and Update Playbooks
Regularly review and update playbooks based on lessons learned and system changes.

## Detailed Implementation

{% raw %}
```python
import boto3
import json
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import threading
import yaml
import subprocess
import requests

class IncidentSeverity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class PlaybookStatus(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ESCALATED = "escalated"
    FAILED = "failed"

class DiagnosticType(Enum):
    SYSTEM_HEALTH = "system_health"
    PERFORMANCE = "performance"
    CONNECTIVITY = "connectivity"
    RESOURCE_USAGE = "resource_usage"
    LOG_ANALYSIS = "log_analysis"

@dataclass
class PlaybookStep:
    step_id: str
    title: str
    description: str
    action_type: str  # manual, automated, decision
    commands: List[str]
    expected_output: str
    success_criteria: str
    failure_action: str
    estimated_duration: int
    required_permissions: List[str]

@dataclass
class IncidentPlaybook:
    playbook_id: str
    name: str
    description: str
    incident_types: List[str]
    severity_levels: List[IncidentSeverity]
    steps: List[PlaybookStep]
    escalation_criteria: Dict[str, Any]
    prerequisites: List[str]
    tools_required: List[str]

@dataclass
class PlaybookExecution:
    execution_id: str
    playbook_id: str
    incident_id: str
    started_by: str
    start_time: datetime
    end_time: Optional[datetime]
    status: PlaybookStatus
    current_step: int
    step_results: List[Dict[str, Any]]
    escalated: bool
    notes: List[str]

class FailureInvestigationSystem:
    def __init__(self, region: str = 'us-east-1'):
        self.region = region
        
        # AWS clients
        self.cloudwatch = boto3.client('cloudwatch', region_name=region)
        self.logs = boto3.client('logs', region_name=region)
        self.ec2 = boto3.client('ec2', region_name=region)
        self.elbv2 = boto3.client('elbv2', region_name=region)
        self.rds = boto3.client('rds', region_name=region)
        self.lambda_client = boto3.client('lambda', region_name=region)
        self.ssm = boto3.client('ssm', region_name=region)
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Playbook management
        self.playbooks: Dict[str, IncidentPlaybook] = {}
        self.active_executions: Dict[str, PlaybookExecution] = {}
        self.execution_history: List[PlaybookExecution] = []
        
        # Diagnostic tools
        self.diagnostic_tools: Dict[str, Any] = {}
        
        # Thread safety
        self.execution_lock = threading.Lock()

    def register_playbook(self, playbook: IncidentPlaybook) -> bool:
        """Register a new incident response playbook"""
        try:
            self.playbooks[playbook.playbook_id] = playbook
            self.logger.info(f"Registered playbook: {playbook.name}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to register playbook {playbook.playbook_id}: {str(e)}")
            return False

    def create_standard_playbooks(self) -> List[IncidentPlaybook]:
        """Create standard incident response playbooks"""
        playbooks = []
        
        try:
            # High CPU Utilization Playbook
            cpu_playbook = IncidentPlaybook(
                playbook_id="cpu-high-utilization",
                name="High CPU Utilization Investigation",
                description="Systematic investigation of high CPU utilization incidents",
                incident_types=["high_cpu", "performance_degradation"],
                severity_levels=[IncidentSeverity.HIGH, IncidentSeverity.CRITICAL],
                steps=[
                    PlaybookStep(
                        step_id="cpu-001",
                        title="Verify CPU Metrics",
                        description="Check current CPU utilization across all instances",
                        action_type="automated",
                        commands=["get_cpu_metrics"],
                        expected_output="CPU utilization percentages for all instances",
                        success_criteria="CPU metrics retrieved successfully",
                        failure_action="escalate",
                        estimated_duration=2,
                        required_permissions=["cloudwatch:GetMetricStatistics"]
                    ),
                    PlaybookStep(
                        step_id="cpu-002",
                        title="Identify Top Processes",
                        description="Identify processes consuming the most CPU",
                        action_type="automated",
                        commands=["get_top_processes"],
                        expected_output="List of top CPU-consuming processes",
                        success_criteria="Process list retrieved",
                        failure_action="continue",
                        estimated_duration=3,
                        required_permissions=["ssm:SendCommand"]
                    ),
                    PlaybookStep(
                        step_id="cpu-003",
                        title="Check Auto Scaling Status",
                        description="Verify if Auto Scaling is responding appropriately",
                        action_type="automated",
                        commands=["check_autoscaling_activity"],
                        expected_output="Auto Scaling group status and recent activities",
                        success_criteria="Auto Scaling status retrieved",
                        failure_action="continue",
                        estimated_duration=2,
                        required_permissions=["autoscaling:DescribeAutoScalingGroups"]
                    ),
                    PlaybookStep(
                        step_id="cpu-004",
                        title="Analyze Application Logs",
                        description="Review application logs for errors or unusual patterns",
                        action_type="automated",
                        commands=["analyze_application_logs"],
                        expected_output="Log analysis results with error patterns",
                        success_criteria="Log analysis completed",
                        failure_action="continue",
                        estimated_duration=5,
                        required_permissions=["logs:FilterLogEvents"]
                    ),
                    PlaybookStep(
                        step_id="cpu-005",
                        title="Decision Point: Scale or Investigate",
                        description="Determine if immediate scaling is needed or further investigation required",
                        action_type="decision",
                        commands=["evaluate_scaling_decision"],
                        expected_output="Scaling recommendation",
                        success_criteria="Decision made",
                        failure_action="escalate",
                        estimated_duration=3,
                        required_permissions=[]
                    )
                ],
                escalation_criteria={
                    "cpu_threshold": 90,
                    "duration_minutes": 15,
                    "failed_steps": 2
                },
                prerequisites=["CloudWatch monitoring enabled", "SSM agent installed"],
                tools_required=["AWS CLI", "CloudWatch", "Systems Manager"]
            )
            playbooks.append(cpu_playbook)
            self.register_playbook(cpu_playbook)
            
            # Database Connection Issues Playbook
            db_playbook = IncidentPlaybook(
                playbook_id="database-connection-issues",
                name="Database Connection Issues Investigation",
                description="Systematic investigation of database connectivity problems",
                incident_types=["database_connection", "timeout_errors"],
                severity_levels=[IncidentSeverity.CRITICAL, IncidentSeverity.HIGH],
                steps=[
                    PlaybookStep(
                        step_id="db-001",
                        title="Check Database Status",
                        description="Verify database instance status and availability",
                        action_type="automated",
                        commands=["check_database_status"],
                        expected_output="Database instance status and metrics",
                        success_criteria="Database status retrieved",
                        failure_action="escalate",
                        estimated_duration=2,
                        required_permissions=["rds:DescribeDBInstances"]
                    ),
                    PlaybookStep(
                        step_id="db-002",
                        title="Test Database Connectivity",
                        description="Test connection from application servers to database",
                        action_type="automated",
                        commands=["test_database_connectivity"],
                        expected_output="Connection test results from each app server",
                        success_criteria="Connection tests completed",
                        failure_action="continue",
                        estimated_duration=3,
                        required_permissions=["ssm:SendCommand"]
                    ),
                    PlaybookStep(
                        step_id="db-003",
                        title="Check Connection Pool Status",
                        description="Analyze database connection pool metrics",
                        action_type="automated",
                        commands=["analyze_connection_pool"],
                        expected_output="Connection pool utilization and wait times",
                        success_criteria="Connection pool analysis completed",
                        failure_action="continue",
                        estimated_duration=3,
                        required_permissions=["cloudwatch:GetMetricStatistics"]
                    ),
                    PlaybookStep(
                        step_id="db-004",
                        title="Review Database Logs",
                        description="Examine database logs for errors and slow queries",
                        action_type="automated",
                        commands=["analyze_database_logs"],
                        expected_output="Database log analysis with error patterns",
                        success_criteria="Log analysis completed",
                        failure_action="continue",
                        estimated_duration=5,
                        required_permissions=["rds:DescribeDBLogFiles"]
                    ),
                    PlaybookStep(
                        step_id="db-005",
                        title="Check Network Connectivity",
                        description="Verify network path between app servers and database",
                        action_type="automated",
                        commands=["check_network_connectivity"],
                        expected_output="Network connectivity test results",
                        success_criteria="Network tests completed",
                        failure_action="continue",
                        estimated_duration=4,
                        required_permissions=["ec2:DescribeSecurityGroups"]
                    )
                ],
                escalation_criteria={
                    "connection_failure_rate": 50,
                    "response_time_threshold": 5000,
                    "failed_steps": 1
                },
                prerequisites=["Database monitoring enabled", "Network access configured"],
                tools_required=["AWS CLI", "Database client", "Network tools"]
            )
            playbooks.append(db_playbook)
            self.register_playbook(db_playbook)
            
            self.logger.info(f"Created {len(playbooks)} standard playbooks")
            return playbooks
            
        except Exception as e:
            self.logger.error(f"Failed to create standard playbooks: {str(e)}")
            return playbooks

    def execute_playbook(self, playbook_id: str, incident_id: str, executed_by: str) -> str:
        """Execute an incident response playbook"""
        try:
            playbook = self.playbooks.get(playbook_id)
            if not playbook:
                raise ValueError(f"Playbook {playbook_id} not found")
            
            execution_id = f"exec-{int(time.time())}-{playbook_id}"
            
            with self.execution_lock:
                execution = PlaybookExecution(
                    execution_id=execution_id,
                    playbook_id=playbook_id,
                    incident_id=incident_id,
                    started_by=executed_by,
                    start_time=datetime.utcnow(),
                    end_time=None,
                    status=PlaybookStatus.IN_PROGRESS,
                    current_step=0,
                    step_results=[],
                    escalated=False,
                    notes=[]
                )
                
                self.active_executions[execution_id] = execution
            
            # Execute playbook steps
            self._execute_playbook_steps(execution, playbook)
            
            self.logger.info(f"Started playbook execution: {execution_id}")
            return execution_id
            
        except Exception as e:
            self.logger.error(f"Failed to execute playbook {playbook_id}: {str(e)}")
            return ""

    def _execute_playbook_steps(self, execution: PlaybookExecution, playbook: IncidentPlaybook) -> None:
        """Execute individual playbook steps"""
        try:
            for i, step in enumerate(playbook.steps):
                execution.current_step = i
                
                self.logger.info(f"Executing step {step.step_id}: {step.title}")
                
                step_result = {
                    'step_id': step.step_id,
                    'title': step.title,
                    'start_time': datetime.utcnow().isoformat(),
                    'status': 'in_progress',
                    'output': '',
                    'success': False,
                    'duration': 0
                }
                
                start_time = time.time()
                
                try:
                    if step.action_type == "automated":
                        output = self._execute_automated_step(step)
                        step_result['output'] = output
                        step_result['success'] = self._validate_step_success(step, output)
                        
                    elif step.action_type == "decision":
                        decision = self._execute_decision_step(step, execution)
                        step_result['output'] = decision
                        step_result['success'] = True
                        
                    elif step.action_type == "manual":
                        # For manual steps, mark as pending manual action
                        step_result['output'] = "Manual action required"
                        step_result['success'] = True
                        step_result['status'] = 'pending_manual'
                    
                    step_result['duration'] = time.time() - start_time
                    step_result['end_time'] = datetime.utcnow().isoformat()
                    step_result['status'] = 'completed' if step_result['success'] else 'failed'
                    
                except Exception as e:
                    step_result['duration'] = time.time() - start_time
                    step_result['end_time'] = datetime.utcnow().isoformat()
                    step_result['status'] = 'failed'
                    step_result['error'] = str(e)
                    step_result['success'] = False
                    
                    self.logger.error(f"Step {step.step_id} failed: {str(e)}")
                    
                    # Handle failure action
                    if step.failure_action == "escalate":
                        execution.escalated = True
                        execution.status = PlaybookStatus.ESCALATED
                        break
                    elif step.failure_action == "stop":
                        execution.status = PlaybookStatus.FAILED
                        break
                
                execution.step_results.append(step_result)
                
                # Check escalation criteria
                if self._should_escalate(execution, playbook):
                    execution.escalated = True
                    execution.status = PlaybookStatus.ESCALATED
                    break
            
            # Complete execution if not escalated or failed
            if execution.status == PlaybookStatus.IN_PROGRESS:
                execution.status = PlaybookStatus.COMPLETED
            
            execution.end_time = datetime.utcnow()
            
            # Move to history
            with self.execution_lock:
                del self.active_executions[execution.execution_id]
                self.execution_history.append(execution)
            
        except Exception as e:
            execution.status = PlaybookStatus.FAILED
            execution.end_time = datetime.utcnow()
            self.logger.error(f"Playbook execution failed: {str(e)}")

    def _execute_automated_step(self, step: PlaybookStep) -> str:
        """Execute an automated playbook step"""
        try:
            results = []
            
            for command in step.commands:
                if command == "get_cpu_metrics":
                    result = self._get_cpu_metrics()
                elif command == "get_top_processes":
                    result = self._get_top_processes()
                elif command == "check_autoscaling_activity":
                    result = self._check_autoscaling_activity()
                elif command == "analyze_application_logs":
                    result = self._analyze_application_logs()
                elif command == "check_database_status":
                    result = self._check_database_status()
                elif command == "test_database_connectivity":
                    result = self._test_database_connectivity()
                elif command == "analyze_connection_pool":
                    result = self._analyze_connection_pool()
                elif command == "analyze_database_logs":
                    result = self._analyze_database_logs()
                elif command == "check_network_connectivity":
                    result = self._check_network_connectivity()
                else:
                    result = f"Unknown command: {command}"
                
                results.append(f"{command}: {result}")
            
            return "\n".join(results)
            
        except Exception as e:
            self.logger.error(f"Automated step execution failed: {str(e)}")
            return f"Error: {str(e)}"

    def _get_cpu_metrics(self) -> str:
        """Get CPU utilization metrics"""
        try:
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(minutes=15)
            
            response = self.cloudwatch.get_metric_statistics(
                Namespace='AWS/EC2',
                MetricName='CPUUtilization',
                Dimensions=[],
                StartTime=start_time,
                EndTime=end_time,
                Period=300,
                Statistics=['Average', 'Maximum']
            )
            
            if response['Datapoints']:
                latest = max(response['Datapoints'], key=lambda x: x['Timestamp'])
                return f"Current CPU: {latest['Average']:.2f}% (Max: {latest['Maximum']:.2f}%)"
            else:
                return "No CPU metrics available"
                
        except Exception as e:
            return f"Failed to get CPU metrics: {str(e)}"

    def _get_top_processes(self) -> str:
        """Get top CPU-consuming processes via SSM"""
        try:
            # This would use SSM to run commands on instances
            # For demo purposes, returning simulated data
            return "Top processes: java (45%), nginx (12%), python (8%)"
            
        except Exception as e:
            return f"Failed to get top processes: {str(e)}"

    def _check_autoscaling_activity(self) -> str:
        """Check Auto Scaling group activity"""
        try:
            # This would check ASG activities
            return "Auto Scaling: 2 instances launched in last 10 minutes"
            
        except Exception as e:
            return f"Failed to check Auto Scaling: {str(e)}"

    def _analyze_application_logs(self) -> str:
        """Analyze application logs for patterns"""
        try:
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(minutes=30)
            
            # This would analyze CloudWatch Logs
            return "Log analysis: 15 errors found, mostly timeout exceptions"
            
        except Exception as e:
            return f"Failed to analyze logs: {str(e)}"

    def _check_database_status(self) -> str:
        """Check RDS database status"""
        try:
            response = self.rds.describe_db_instances()
            
            statuses = []
            for db in response['DBInstances']:
                statuses.append(f"{db['DBInstanceIdentifier']}: {db['DBInstanceStatus']}")
            
            return "; ".join(statuses) if statuses else "No databases found"
            
        except Exception as e:
            return f"Failed to check database status: {str(e)}"

    def _test_database_connectivity(self) -> str:
        """Test database connectivity from application servers"""
        try:
            # This would test actual connectivity
            return "Connectivity test: 3/4 app servers can connect, 1 timeout"
            
        except Exception as e:
            return f"Failed to test connectivity: {str(e)}"

    def _analyze_connection_pool(self) -> str:
        """Analyze database connection pool metrics"""
        try:
            # This would analyze connection pool metrics
            return "Connection pool: 85% utilization, avg wait time 2.3s"
            
        except Exception as e:
            return f"Failed to analyze connection pool: {str(e)}"

    def _analyze_database_logs(self) -> str:
        """Analyze database logs"""
        try:
            # This would analyze RDS logs
            return "Database logs: 8 slow queries detected, 2 connection errors"
            
        except Exception as e:
            return f"Failed to analyze database logs: {str(e)}"

    def _check_network_connectivity(self) -> str:
        """Check network connectivity"""
        try:
            # This would check security groups, NACLs, etc.
            return "Network check: All security groups allow required ports"
            
        except Exception as e:
            return f"Failed to check network: {str(e)}"

    def _execute_decision_step(self, step: PlaybookStep, execution: PlaybookExecution) -> str:
        """Execute a decision step"""
        try:
            # Analyze previous step results to make decision
            if step.step_id == "cpu-005":
                # Analyze CPU metrics and decide on scaling
                cpu_results = [r for r in execution.step_results if 'cpu' in r.get('output', '').lower()]
                if cpu_results and 'CPU: 9' in cpu_results[0].get('output', ''):
                    return "Decision: Immediate scaling required"
                else:
                    return "Decision: Continue investigation"
            
            return "Decision: Continue with next step"
            
        except Exception as e:
            return f"Decision error: {str(e)}"

    def _validate_step_success(self, step: PlaybookStep, output: str) -> bool:
        """Validate if a step was successful"""
        try:
            if "Error:" in output or "Failed:" in output:
                return False
            
            # Check success criteria
            if step.success_criteria in output:
                return True
            
            # Default success if no errors
            return "Error" not in output and "Failed" not in output
            
        except Exception as e:
            self.logger.error(f"Step validation failed: {str(e)}")
            return False

    def _should_escalate(self, execution: PlaybookExecution, playbook: IncidentPlaybook) -> bool:
        """Check if execution should be escalated"""
        try:
            criteria = playbook.escalation_criteria
            
            # Check failed steps
            failed_steps = len([r for r in execution.step_results if not r.get('success', False)])
            if failed_steps >= criteria.get('failed_steps', 999):
                return True
            
            # Check duration
            if execution.start_time:
                duration = (datetime.utcnow() - execution.start_time).total_seconds() / 60
                if duration > criteria.get('max_duration_minutes', 999):
                    return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Escalation check failed: {str(e)}")
            return False

    def get_playbook_execution_status(self, execution_id: str) -> Dict[str, Any]:
        """Get status of a playbook execution"""
        try:
            # Check active executions
            if execution_id in self.active_executions:
                execution = self.active_executions[execution_id]
            else:
                # Check history
                execution = next((e for e in self.execution_history if e.execution_id == execution_id), None)
                if not execution:
                    return {'error': 'Execution not found'}
            
            status = {
                'execution_id': execution.execution_id,
                'playbook_id': execution.playbook_id,
                'incident_id': execution.incident_id,
                'status': execution.status.value,
                'started_by': execution.started_by,
                'start_time': execution.start_time.isoformat(),
                'end_time': execution.end_time.isoformat() if execution.end_time else None,
                'current_step': execution.current_step,
                'total_steps': len(self.playbooks[execution.playbook_id].steps) if execution.playbook_id in self.playbooks else 0,
                'escalated': execution.escalated,
                'step_results': execution.step_results,
                'notes': execution.notes
            }
            
            return status
            
        except Exception as e:
            self.logger.error(f"Failed to get execution status: {str(e)}")
            return {'error': str(e)}

    def get_playbook_statistics(self) -> Dict[str, Any]:
        """Get playbook usage statistics"""
        try:
            total_executions = len(self.execution_history) + len(self.active_executions)
            completed_executions = len([e for e in self.execution_history if e.status == PlaybookStatus.COMPLETED])
            escalated_executions = len([e for e in self.execution_history if e.escalated])
            
            # Calculate average execution time
            completed = [e for e in self.execution_history if e.status == PlaybookStatus.COMPLETED and e.end_time]
            avg_duration = 0
            if completed:
                durations = [(e.end_time - e.start_time).total_seconds() / 60 for e in completed]
                avg_duration = sum(durations) / len(durations)
            
            # Playbook usage frequency
            playbook_usage = {}
            for execution in self.execution_history:
                playbook_id = execution.playbook_id
                playbook_usage[playbook_id] = playbook_usage.get(playbook_id, 0) + 1
            
            statistics = {
                'total_playbooks': len(self.playbooks),
                'total_executions': total_executions,
                'active_executions': len(self.active_executions),
                'completed_executions': completed_executions,
                'escalated_executions': escalated_executions,
                'success_rate': (completed_executions / total_executions * 100) if total_executions > 0 else 0,
                'average_duration_minutes': avg_duration,
                'playbook_usage_frequency': playbook_usage
            }
            
            return statistics
            
        except Exception as e:
            self.logger.error(f"Failed to get statistics: {str(e)}")
            return {}

# Example usage
def main():
    # Initialize failure investigation system
    investigation_system = FailureInvestigationSystem(region='us-east-1')
    
    # Create standard playbooks
    print("Creating standard incident response playbooks...")
    playbooks = investigation_system.create_standard_playbooks()
    
    print(f"Created {len(playbooks)} playbooks:")
    for playbook in playbooks:
        print(f"- {playbook.name} ({len(playbook.steps)} steps)")
    
    # Execute a playbook
    print("\nExecuting CPU high utilization playbook...")
    execution_id = investigation_system.execute_playbook(
        playbook_id="cpu-high-utilization",
        incident_id="incident-2024-001",
        executed_by="ops-team"
    )
    
    if execution_id:
        print(f"Playbook execution started: {execution_id}")
        
        # Wait a moment for execution to progress
        time.sleep(2)
        
        # Get execution status
        status = investigation_system.get_playbook_execution_status(execution_id)
        print(f"Execution status: {json.dumps(status, indent=2, default=str)}")
    
    # Get system statistics
    stats = investigation_system.get_playbook_statistics()
    print(f"\nPlaybook system statistics: {json.dumps(stats, indent=2)}")

if __name__ == "__main__":
    main()
```
{% endraw %}

## AWS Services

### Primary Services
- **AWS Systems Manager**: Automated command execution and operational procedures
- **Amazon CloudWatch**: Metrics collection and analysis for diagnostics
- **Amazon CloudWatch Logs**: Log aggregation and analysis
- **AWS Lambda**: Event-driven automation for playbook execution

### Supporting Services
- **Amazon S3**: Storage for playbook documentation and execution results
- **Amazon SNS**: Notifications for playbook execution status
- **AWS Step Functions**: Complex playbook workflow orchestration
- **Amazon EventBridge**: Event-driven playbook triggering

## Benefits

- **Consistent Investigation**: Standardized procedures ensure thorough analysis
- **Faster Resolution**: Automated diagnostics reduce mean time to resolution
- **Knowledge Retention**: Playbooks capture institutional knowledge
- **Reduced Human Error**: Systematic approach minimizes mistakes
- **Continuous Improvement**: Playbooks evolve based on lessons learned

## Related Resources

- [AWS Systems Manager User Guide](https://docs.aws.amazon.com/systems-manager/)
- [Amazon CloudWatch User Guide](https://docs.aws.amazon.com/cloudwatch/)
- [AWS Step Functions Developer Guide](https://docs.aws.amazon.com/step-functions/)
- [Incident Response Best Practices](https://aws.amazon.com/architecture/well-architected/)
