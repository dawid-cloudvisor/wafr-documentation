---
title: REL08-BP03 - Integrate resiliency testing as part of your deployment
layout: default
parent: REL08 - How do you implement change?
grand_parent: Reliability
nav_order: 3
---

# REL08-BP03: Integrate resiliency testing as part of your deployment

## Overview

Implement comprehensive resiliency testing as an integral part of your deployment pipeline to validate that your system can withstand failures and maintain availability under adverse conditions. Resiliency testing, including chaos engineering, ensures that your applications gracefully handle failures and recover quickly from disruptions.

## Implementation Steps

### 1. Design Resiliency Testing Strategy
- Define failure scenarios and testing objectives
- Establish testing environments and safety boundaries
- Design test automation and execution frameworks
- Implement monitoring and observability during tests

### 2. Implement Chaos Engineering Practices
- Create controlled failure injection mechanisms
- Design infrastructure and application-level chaos experiments
- Implement gradual rollout of chaos testing
- Establish experiment hypothesis and validation criteria

### 3. Configure Fault Injection Testing
- Implement network latency and partition testing
- Configure resource exhaustion and capacity testing
- Design dependency failure and timeout testing
- Establish security and compliance failure scenarios

### 4. Establish Recovery Testing
- Implement disaster recovery and backup testing
- Configure auto-scaling and self-healing validation
- Design rollback and failover testing
- Establish data consistency and integrity validation

### 5. Integrate with CI/CD Pipelines
- Configure automated resiliency testing in deployment pipelines
- Implement test result analysis and failure criteria
- Design progressive testing with canary deployments
- Establish automated rollback based on resiliency test results

### 6. Monitor and Optimize Resiliency
- Track system behavior during failure scenarios
- Monitor recovery times and success rates
- Implement continuous improvement based on test insights
- Establish resiliency metrics and SLA validation

## Implementation Examples

### Example 1: Comprehensive Resiliency Testing Framework
```python
import boto3
import json
import logging
import asyncio
import random
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import subprocess
import psutil

class FailureType(Enum):
    INSTANCE_TERMINATION = "instance_termination"
    NETWORK_LATENCY = "network_latency"
    NETWORK_PARTITION = "network_partition"
    CPU_STRESS = "cpu_stress"
    MEMORY_STRESS = "memory_stress"
    DISK_STRESS = "disk_stress"
    SERVICE_UNAVAILABLE = "service_unavailable"
    DATABASE_FAILURE = "database_failure"
    DEPENDENCY_TIMEOUT = "dependency_timeout"

class TestPhase(Enum):
    PREPARATION = "preparation"
    INJECTION = "injection"
    OBSERVATION = "observation"
    RECOVERY = "recovery"
    VALIDATION = "validation"

class ExperimentStatus(Enum):
    PLANNED = "planned"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    ABORTED = "aborted"

@dataclass
class ChaosExperiment:
    experiment_id: str
    name: str
    description: str
    failure_type: FailureType
    target_resources: List[str]
    failure_parameters: Dict[str, Any]
    duration_minutes: int
    hypothesis: str
    success_criteria: List[Dict[str, Any]]
    rollback_plan: List[str]
    safety_checks: List[Dict[str, Any]]

@dataclass
class ExperimentExecution:
    execution_id: str
    experiment_id: str
    status: ExperimentStatus
    started_at: datetime
    completed_at: Optional[datetime]
    current_phase: TestPhase
    phase_results: Dict[str, Any]
    metrics_collected: List[Dict[str, Any]]
    hypothesis_validated: Optional[bool]
    error_message: Optional[str]
    rollback_performed: bool

class ResiliencyTestingFramework:
    """Comprehensive resiliency testing and chaos engineering framework"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
        # AWS clients
        self.ec2 = boto3.client('ec2')
        self.autoscaling = boto3.client('autoscaling')
        self.elbv2 = boto3.client('elbv2')
        self.rds = boto3.client('rds')
        self.lambda_client = boto3.client('lambda')
        self.cloudwatch = boto3.client('cloudwatch')
        self.dynamodb = boto3.resource('dynamodb')
        self.ssm = boto3.client('ssm')
        
        # Storage
        self.experiments_table = self.dynamodb.Table(config.get('experiments_table', 'chaos-experiments'))
        self.executions_table = self.dynamodb.Table(config.get('executions_table', 'experiment-executions'))
        
        # Configuration
        self.safety_enabled = config.get('safety_enabled', True)
        self.max_blast_radius = config.get('max_blast_radius', 0.1)  # 10% of resources
        self.monitoring_interval = config.get('monitoring_interval', 30)  # seconds
        
        # Active experiments
        self.active_experiments = {}
        
    async def execute_chaos_experiment(self, experiment_id: str, 
                                     environment: str = 'staging') -> str:
        """Execute a chaos engineering experiment"""
        try:
            # Get experiment definition
            experiment = await self._get_experiment(experiment_id)
            if not experiment:
                raise ValueError(f"Experiment {experiment_id} not found")
            
            # Validate safety constraints
            if not await self._validate_safety_constraints(experiment, environment):
                raise ValueError("Safety constraints not met")
            
            # Create execution record
            execution_id = f"exec_{int(datetime.utcnow().timestamp())}_{experiment_id}"
            
            execution = ExperimentExecution(
                execution_id=execution_id,
                experiment_id=experiment_id,
                status=ExperimentStatus.RUNNING,
                started_at=datetime.utcnow(),
                completed_at=None,
                current_phase=TestPhase.PREPARATION,
                phase_results={},
                metrics_collected=[],
                hypothesis_validated=None,
                error_message=None,
                rollback_performed=False
            )
            
            # Store execution record
            await self._store_execution(execution)
            
            # Start experiment execution
            self.active_experiments[execution_id] = execution
            asyncio.create_task(self._execute_experiment_phases(experiment, execution))
            
            logging.info(f"Started chaos experiment: {execution_id}")
            return execution_id
            
        except Exception as e:
            logging.error(f"Failed to execute chaos experiment: {str(e)}")
            raise
    
    async def _execute_experiment_phases(self, experiment: ChaosExperiment, 
                                       execution: ExperimentExecution):
        """Execute all phases of the chaos experiment"""
        try:
            # Phase 1: Preparation
            execution.current_phase = TestPhase.PREPARATION
            await self._execute_preparation_phase(experiment, execution)
            
            # Phase 2: Failure Injection
            execution.current_phase = TestPhase.INJECTION
            await self._execute_injection_phase(experiment, execution)
            
            # Phase 3: Observation
            execution.current_phase = TestPhase.OBSERVATION
            await self._execute_observation_phase(experiment, execution)
            
            # Phase 4: Recovery
            execution.current_phase = TestPhase.RECOVERY
            await self._execute_recovery_phase(experiment, execution)
            
            # Phase 5: Validation
            execution.current_phase = TestPhase.VALIDATION
            await self._execute_validation_phase(experiment, execution)
            
            # Complete experiment
            execution.status = ExperimentStatus.COMPLETED
            execution.completed_at = datetime.utcnow()
            
            # Generate experiment report
            await self._generate_experiment_report(experiment, execution)
            
        except Exception as e:
            logging.error(f"Experiment execution failed: {str(e)}")
            execution.status = ExperimentStatus.FAILED
            execution.error_message = str(e)
            execution.completed_at = datetime.utcnow()
            
            # Perform emergency rollback
            await self._perform_emergency_rollback(experiment, execution)
        
        finally:
            # Store final execution state
            await self._store_execution(execution)
            
            # Remove from active experiments
            if execution.execution_id in self.active_experiments:
                del self.active_experiments[execution.execution_id]
    
    async def _execute_preparation_phase(self, experiment: ChaosExperiment, 
                                       execution: ExperimentExecution):
        """Execute preparation phase"""
        try:
            logging.info(f"Starting preparation phase for {experiment.name}")
            
            # Collect baseline metrics
            baseline_metrics = await self._collect_baseline_metrics(experiment.target_resources)
            execution.phase_results['preparation'] = {
                'baseline_metrics': baseline_metrics,
                'target_resources_validated': True,
                'safety_checks_passed': True
            }
            
            # Verify target resources are healthy
            healthy_resources = await self._verify_resource_health(experiment.target_resources)
            if not healthy_resources:
                raise Exception("Target resources are not healthy")
            
            # Set up monitoring
            await self._setup_experiment_monitoring(experiment, execution)
            
            logging.info("Preparation phase completed successfully")
            
        except Exception as e:
            logging.error(f"Preparation phase failed: {str(e)}")
            raise
    
    async def _execute_injection_phase(self, experiment: ChaosExperiment, 
                                     execution: ExperimentExecution):
        """Execute failure injection phase"""
        try:
            logging.info(f"Starting injection phase for {experiment.name}")
            
            # Inject failure based on type
            if experiment.failure_type == FailureType.INSTANCE_TERMINATION:
                await self._inject_instance_termination(experiment, execution)
            elif experiment.failure_type == FailureType.NETWORK_LATENCY:
                await self._inject_network_latency(experiment, execution)
            elif experiment.failure_type == FailureType.CPU_STRESS:
                await self._inject_cpu_stress(experiment, execution)
            elif experiment.failure_type == FailureType.MEMORY_STRESS:
                await self._inject_memory_stress(experiment, execution)
            elif experiment.failure_type == FailureType.SERVICE_UNAVAILABLE:
                await self._inject_service_unavailable(experiment, execution)
            else:
                raise ValueError(f"Unsupported failure type: {experiment.failure_type}")
            
            execution.phase_results['injection'] = {
                'failure_injected': True,
                'injection_time': datetime.utcnow().isoformat(),
                'affected_resources': experiment.target_resources
            }
            
            logging.info("Injection phase completed successfully")
            
        except Exception as e:
            logging.error(f"Injection phase failed: {str(e)}")
            raise
    
    async def _execute_observation_phase(self, experiment: ChaosExperiment, 
                                       execution: ExperimentExecution):
        """Execute observation phase"""
        try:
            logging.info(f"Starting observation phase for {experiment.name}")
            
            # Monitor system behavior during failure
            observation_duration = experiment.duration_minutes * 60  # Convert to seconds
            start_time = time.time()
            
            metrics_collected = []
            
            while time.time() - start_time < observation_duration:
                # Collect current metrics
                current_metrics = await self._collect_current_metrics(experiment.target_resources)
                metrics_collected.append({
                    'timestamp': datetime.utcnow().isoformat(),
                    'metrics': current_metrics
                })
                
                # Check safety conditions
                if self.safety_enabled:
                    safety_violation = await self._check_safety_conditions(experiment, current_metrics)
                    if safety_violation:
                        logging.warning("Safety violation detected, aborting experiment")
                        execution.status = ExperimentStatus.ABORTED
                        await self._perform_emergency_rollback(experiment, execution)
                        return
                
                # Wait before next collection
                await asyncio.sleep(self.monitoring_interval)
            
            execution.metrics_collected = metrics_collected
            execution.phase_results['observation'] = {
                'duration_seconds': observation_duration,
                'metrics_points_collected': len(metrics_collected),
                'safety_violations': 0
            }
            
            logging.info("Observation phase completed successfully")
            
        except Exception as e:
            logging.error(f"Observation phase failed: {str(e)}")
            raise
    
    async def _execute_recovery_phase(self, experiment: ChaosExperiment, 
                                    execution: ExperimentExecution):
        """Execute recovery phase"""
        try:
            logging.info(f"Starting recovery phase for {experiment.name}")
            
            # Remove failure injection
            await self._remove_failure_injection(experiment, execution)
            
            # Wait for system recovery
            recovery_timeout = 300  # 5 minutes
            start_time = time.time()
            
            while time.time() - start_time < recovery_timeout:
                # Check if system has recovered
                recovery_status = await self._check_system_recovery(experiment.target_resources)
                
                if recovery_status['recovered']:
                    execution.phase_results['recovery'] = {
                        'recovery_time_seconds': time.time() - start_time,
                        'recovery_successful': True,
                        'final_health_status': recovery_status
                    }
                    logging.info("System recovery completed successfully")
                    return
                
                await asyncio.sleep(30)  # Check every 30 seconds
            
            # Recovery timeout
            execution.phase_results['recovery'] = {
                'recovery_time_seconds': recovery_timeout,
                'recovery_successful': False,
                'timeout_reached': True
            }
            
            logging.warning("System recovery timed out")
            
        except Exception as e:
            logging.error(f"Recovery phase failed: {str(e)}")
            raise
    
    async def _execute_validation_phase(self, experiment: ChaosExperiment, 
                                      execution: ExperimentExecution):
        """Execute validation phase"""
        try:
            logging.info(f"Starting validation phase for {experiment.name}")
            
            # Validate hypothesis
            hypothesis_validated = await self._validate_hypothesis(experiment, execution)
            execution.hypothesis_validated = hypothesis_validated
            
            # Check success criteria
            success_criteria_met = await self._check_success_criteria(experiment, execution)
            
            execution.phase_results['validation'] = {
                'hypothesis_validated': hypothesis_validated,
                'success_criteria_met': success_criteria_met,
                'validation_time': datetime.utcnow().isoformat()
            }
            
            logging.info(f"Validation phase completed: hypothesis={hypothesis_validated}, criteria={success_criteria_met}")
            
        except Exception as e:
            logging.error(f"Validation phase failed: {str(e)}")
            raise
    
    async def _inject_instance_termination(self, experiment: ChaosExperiment, 
                                         execution: ExperimentExecution):
        """Inject instance termination failure"""
        try:
            target_instances = experiment.target_resources
            termination_count = experiment.failure_parameters.get('count', 1)
            
            # Select random instances to terminate
            instances_to_terminate = random.sample(target_instances, 
                                                 min(termination_count, len(target_instances)))
            
            # Terminate instances
            self.ec2.terminate_instances(InstanceIds=instances_to_terminate)
            
            logging.info(f"Terminated instances: {instances_to_terminate}")
            
        except Exception as e:
            logging.error(f"Instance termination injection failed: {str(e)}")
            raise
    
    async def _inject_network_latency(self, experiment: ChaosExperiment, 
                                    execution: ExperimentExecution):
        """Inject network latency failure"""
        try:
            target_instances = experiment.target_resources
            latency_ms = experiment.failure_parameters.get('latency_ms', 1000)
            
            # Use SSM to inject network latency
            for instance_id in target_instances:
                command = f"tc qdisc add dev eth0 root netem delay {latency_ms}ms"
                
                self.ssm.send_command(
                    InstanceIds=[instance_id],
                    DocumentName='AWS-RunShellScript',
                    Parameters={'commands': [command]}
                )
            
            logging.info(f"Injected {latency_ms}ms network latency on instances: {target_instances}")
            
        except Exception as e:
            logging.error(f"Network latency injection failed: {str(e)}")
            raise
    
    async def _inject_cpu_stress(self, experiment: ChaosExperiment, 
                               execution: ExperimentExecution):
        """Inject CPU stress failure"""
        try:
            target_instances = experiment.target_resources
            cpu_percentage = experiment.failure_parameters.get('cpu_percentage', 80)
            duration_minutes = experiment.duration_minutes
            
            # Use SSM to inject CPU stress
            for instance_id in target_instances:
                command = f"stress-ng --cpu 0 --cpu-load {cpu_percentage} --timeout {duration_minutes}m &"
                
                self.ssm.send_command(
                    InstanceIds=[instance_id],
                    DocumentName='AWS-RunShellScript',
                    Parameters={'commands': [command]}
                )
            
            logging.info(f"Injected {cpu_percentage}% CPU stress on instances: {target_instances}")
            
        except Exception as e:
            logging.error(f"CPU stress injection failed: {str(e)}")
            raise
    
    async def _collect_baseline_metrics(self, target_resources: List[str]) -> Dict[str, Any]:
        """Collect baseline metrics before experiment"""
        try:
            metrics = {}
            
            # Collect CPU utilization
            cpu_response = self.cloudwatch.get_metric_statistics(
                Namespace='AWS/EC2',
                MetricName='CPUUtilization',
                Dimensions=[{'Name': 'InstanceId', 'Value': target_resources[0]}],
                StartTime=datetime.utcnow() - timedelta(minutes=10),
                EndTime=datetime.utcnow(),
                Period=300,
                Statistics=['Average']
            )
            
            if cpu_response['Datapoints']:
                metrics['baseline_cpu'] = cpu_response['Datapoints'][-1]['Average']
            
            # Collect response time metrics
            response_time_response = self.cloudwatch.get_metric_statistics(
                Namespace='AWS/ApplicationELB',
                MetricName='TargetResponseTime',
                StartTime=datetime.utcnow() - timedelta(minutes=10),
                EndTime=datetime.utcnow(),
                Period=300,
                Statistics=['Average']
            )
            
            if response_time_response['Datapoints']:
                metrics['baseline_response_time'] = response_time_response['Datapoints'][-1]['Average']
            
            return metrics
            
        except Exception as e:
            logging.error(f"Failed to collect baseline metrics: {str(e)}")
            return {}
    
    async def _validate_hypothesis(self, experiment: ChaosExperiment, 
                                 execution: ExperimentExecution) -> bool:
        """Validate experiment hypothesis"""
        try:
            # This is a simplified validation - in practice, this would be more sophisticated
            recovery_successful = execution.phase_results.get('recovery', {}).get('recovery_successful', False)
            
            # Check if system maintained availability during failure
            if 'system maintains availability' in experiment.hypothesis.lower():
                return recovery_successful
            
            # Check if auto-scaling worked
            if 'auto-scaling' in experiment.hypothesis.lower():
                # Check if new instances were launched
                return await self._check_auto_scaling_response(experiment.target_resources)
            
            return True  # Default to true for unknown hypotheses
            
        except Exception as e:
            logging.error(f"Hypothesis validation failed: {str(e)}")
            return False
    
    async def _check_success_criteria(self, experiment: ChaosExperiment, 
                                    execution: ExperimentExecution) -> bool:
        """Check if success criteria are met"""
        try:
            for criteria in experiment.success_criteria:
                criteria_type = criteria.get('type')
                
                if criteria_type == 'recovery_time':
                    max_recovery_time = criteria.get('max_seconds', 300)
                    actual_recovery_time = execution.phase_results.get('recovery', {}).get('recovery_time_seconds', float('inf'))
                    
                    if actual_recovery_time > max_recovery_time:
                        return False
                
                elif criteria_type == 'availability':
                    min_availability = criteria.get('min_percentage', 99.0)
                    # Calculate availability from metrics
                    # This would be implemented based on your specific metrics
                    pass
            
            return True
            
        except Exception as e:
            logging.error(f"Success criteria check failed: {str(e)}")
            return False
    
    async def _remove_failure_injection(self, experiment: ChaosExperiment, 
                                      execution: ExperimentExecution):
        """Remove failure injection"""
        try:
            if experiment.failure_type == FailureType.NETWORK_LATENCY:
                # Remove network latency
                for instance_id in experiment.target_resources:
                    command = "tc qdisc del dev eth0 root"
                    
                    self.ssm.send_command(
                        InstanceIds=[instance_id],
                        DocumentName='AWS-RunShellScript',
                        Parameters={'commands': [command]}
                    )
            
            elif experiment.failure_type == FailureType.CPU_STRESS:
                # Kill stress processes
                for instance_id in experiment.target_resources:
                    command = "pkill -f stress-ng"
                    
                    self.ssm.send_command(
                        InstanceIds=[instance_id],
                        DocumentName='AWS-RunShellScript',
                        Parameters={'commands': [command]}
                    )
            
            logging.info("Failure injection removed successfully")
            
        except Exception as e:
            logging.error(f"Failed to remove failure injection: {str(e)}")
    
    async def _store_execution(self, execution: ExperimentExecution):
        """Store experiment execution"""
        try:
            execution_dict = asdict(execution)
            execution_dict['started_at'] = execution.started_at.isoformat()
            if execution.completed_at:
                execution_dict['completed_at'] = execution.completed_at.isoformat()
            
            self.executions_table.put_item(Item=execution_dict)
            
        except Exception as e:
            logging.error(f"Failed to store execution: {str(e)}")
    
    async def _generate_experiment_report(self, experiment: ChaosExperiment, 
                                        execution: ExperimentExecution):
        """Generate comprehensive experiment report"""
        try:
            report = {
                'experiment': {
                    'id': experiment.experiment_id,
                    'name': experiment.name,
                    'hypothesis': experiment.hypothesis,
                    'failure_type': experiment.failure_type.value
                },
                'execution': {
                    'id': execution.execution_id,
                    'status': execution.status.value,
                    'duration': str(execution.completed_at - execution.started_at) if execution.completed_at else None,
                    'hypothesis_validated': execution.hypothesis_validated
                },
                'results': execution.phase_results,
                'insights': await self._generate_insights(experiment, execution)
            }
            
            logging.info(f"Generated experiment report: {json.dumps(report, indent=2)}")
            
        except Exception as e:
            logging.error(f"Failed to generate experiment report: {str(e)}")

# Usage example
async def main():
    config = {
        'experiments_table': 'chaos-experiments',
        'executions_table': 'experiment-executions',
        'safety_enabled': True,
        'max_blast_radius': 0.1
    }
    
    # Initialize resiliency testing framework
    resiliency_framework = ResiliencyTestingFramework(config)
    
    # Create chaos experiment
    experiment = ChaosExperiment(
        experiment_id='instance_termination_test',
        name='Instance Termination Resilience Test',
        description='Test system resilience to instance termination',
        failure_type=FailureType.INSTANCE_TERMINATION,
        target_resources=['i-1234567890abcdef0'],
        failure_parameters={'count': 1},
        duration_minutes=10,
        hypothesis='System maintains availability when one instance is terminated due to auto-scaling',
        success_criteria=[
            {'type': 'recovery_time', 'max_seconds': 300},
            {'type': 'availability', 'min_percentage': 99.0}
        ],
        rollback_plan=['Launch replacement instance if auto-scaling fails'],
        safety_checks=[
            {'type': 'min_healthy_instances', 'threshold': 2}
        ]
    )
    
    # Execute experiment
    execution_id = await resiliency_framework.execute_chaos_experiment(
        experiment.experiment_id,
        'staging'
    )
    
    print(f"Chaos experiment started: {execution_id}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## AWS Services Used

- **AWS Systems Manager**: Failure injection and system command execution
- **Amazon EC2**: Instance management and termination testing
- **AWS Auto Scaling**: Scaling behavior validation during failures
- **Elastic Load Balancing**: Load balancer behavior and health check testing
- **Amazon CloudWatch**: Metrics collection and monitoring during experiments
- **AWS Lambda**: Custom chaos functions and automated responses
- **Amazon DynamoDB**: Experiment configuration and execution history storage
- **Amazon RDS**: Database failure testing and recovery validation
- **AWS Step Functions**: Complex experiment workflow orchestration
- **Amazon SNS**: Experiment notifications and alerting
- **AWS Config**: Configuration compliance during failure scenarios
- **Amazon VPC**: Network partition and connectivity testing
- **AWS X-Ray**: Application tracing during failure injection
- **Amazon ECS/EKS**: Container-based chaos testing and orchestration
- **AWS Fault Injection Simulator**: Managed chaos engineering service

## Benefits

- **Improved Resilience**: Proactive identification and resolution of system weaknesses
- **Confidence Building**: Validation that systems can handle real-world failures
- **Faster Recovery**: Optimized recovery procedures through testing and validation
- **Risk Reduction**: Early detection of failure modes before they impact production
- **Team Learning**: Improved understanding of system behavior under stress
- **Automated Validation**: Continuous validation of resilience improvements
- **Compliance**: Meeting reliability and availability requirements
- **Cost Optimization**: Preventing costly outages through proactive testing
- **Innovation**: Safe experimentation with new failure scenarios
- **Documentation**: Living documentation of system failure and recovery patterns

## Related Resources

- [AWS Well-Architected Reliability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/)
- [Integrate Resiliency Testing](https://docs.aws.amazon.com/wellarchitected/latest/framework/rel_implement_change_resiliency_testing.html)
- [AWS Fault Injection Simulator](https://docs.aws.amazon.com/fis/latest/userguide/)
- [AWS Systems Manager User Guide](https://docs.aws.amazon.com/systems-manager/latest/userguide/)
- [Amazon EC2 User Guide](https://docs.aws.amazon.com/ec2/latest/userguide/)
- [AWS Auto Scaling User Guide](https://docs.aws.amazon.com/autoscaling/application/userguide/)
- [Amazon CloudWatch User Guide](https://docs.aws.amazon.com/cloudwatch/latest/monitoring/)
- [AWS Step Functions Developer Guide](https://docs.aws.amazon.com/step-functions/latest/dg/)
- [Chaos Engineering Best Practices](https://aws.amazon.com/builders-library/)
- [AWS Builders' Library - Implementing Health Checks](https://aws.amazon.com/builders-library/implementing-health-checks/)
- [Resilience Testing Strategies](https://aws.amazon.com/architecture/well-architected/)
- [Disaster Recovery Best Practices](https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-options-in-the-cloud.html)
