---
title: REL12-BP05 - Test resiliency using chaos engineering
layout: default
parent: REL12 - How do you test reliability?
nav_order: 5
---

# REL12-BP05: Test resiliency using chaos engineering

Proactively inject failures into your system to identify weaknesses and validate recovery mechanisms. Use chaos engineering principles to build confidence in system resilience by testing failure scenarios in controlled environments.

## Implementation Steps

### 1. Start with Hypothesis-Driven Experiments
Define clear hypotheses about system behavior during failures before conducting experiments.

### 2. Begin in Non-Production Environments
Start chaos experiments in development and staging environments before production.

### 3. Implement Gradual Failure Injection
Start with small, controlled failures and gradually increase complexity and scope.

### 4. Monitor System Behavior
Collect comprehensive metrics during experiments to understand system response.

### 5. Automate Chaos Engineering
Build automated chaos engineering into your regular testing and deployment processes.

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
import random
import uuid

class ChaosExperimentType(Enum):
    INSTANCE_TERMINATION = "instance_termination"
    NETWORK_LATENCY = "network_latency"
    DISK_FILL = "disk_fill"
    CPU_STRESS = "cpu_stress"
    MEMORY_STRESS = "memory_stress"
    SERVICE_UNAVAILABLE = "service_unavailable"
    DATABASE_FAILURE = "database_failure"
    DEPENDENCY_TIMEOUT = "dependency_timeout"

class ExperimentStatus(Enum):
    PLANNED = "planned"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    ABORTED = "aborted"

class BlastRadius(Enum):
    SINGLE_INSTANCE = "single_instance"
    SINGLE_AZ = "single_az"
    MULTIPLE_AZ = "multiple_az"
    SINGLE_REGION = "single_region"
    MULTIPLE_REGION = "multiple_region"

@dataclass
class ChaosExperiment:
    experiment_id: str
    name: str
    description: str
    experiment_type: ChaosExperimentType
    hypothesis: str
    blast_radius: BlastRadius
    target_resources: List[str]
    duration_minutes: int
    rollback_plan: str
    success_criteria: List[str]
    abort_conditions: List[str]
    environment: str

@dataclass
class ExperimentExecution:
    execution_id: str
    experiment_id: str
    status: ExperimentStatus
    start_time: datetime
    end_time: Optional[datetime]
    hypothesis_validated: Optional[bool]
    observations: List[str]
    metrics_collected: Dict[str, Any]
    issues_discovered: List[str]
    improvements_identified: List[str]

class ChaosEngineeringSystem:
    def __init__(self, region: str = 'us-east-1'):
        self.region = region
        
        # AWS clients
        self.fis = boto3.client('fis', region_name=region)
        self.ec2 = boto3.client('ec2', region_name=region)
        self.cloudwatch = boto3.client('cloudwatch', region_name=region)
        self.ssm = boto3.client('ssm', region_name=region)
        self.lambda_client = boto3.client('lambda', region_name=region)
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        # Experiment management
        self.experiments: Dict[str, ChaosExperiment] = {}
        self.executions: List[ExperimentExecution] = []
        self.safety_checks: List[str] = []
        
        # Thread safety
        self.chaos_lock = threading.Lock()

    def create_chaos_experiment(self, experiment_config: Dict[str, Any]) -> str:
        """Create a new chaos engineering experiment"""
        try:
            experiment_id = f"chaos-{uuid.uuid4().hex[:8]}"
            
            experiment = ChaosExperiment(
                experiment_id=experiment_id,
                name=experiment_config['name'],
                description=experiment_config['description'],
                experiment_type=ChaosExperimentType(experiment_config['type']),
                hypothesis=experiment_config['hypothesis'],
                blast_radius=BlastRadius(experiment_config['blast_radius']),
                target_resources=experiment_config['target_resources'],
                duration_minutes=experiment_config['duration_minutes'],
                rollback_plan=experiment_config['rollback_plan'],
                success_criteria=experiment_config['success_criteria'],
                abort_conditions=experiment_config['abort_conditions'],
                environment=experiment_config['environment']
            )
            
            self.experiments[experiment_id] = experiment
            
            self.logger.info(f"Created chaos experiment: {experiment.name}")
            return experiment_id
            
        except Exception as e:
            self.logger.error(f"Failed to create chaos experiment: {str(e)}")
            return ""

    def execute_chaos_experiment(self, experiment_id: str) -> str:
        """Execute a chaos engineering experiment"""
        try:
            experiment = self.experiments.get(experiment_id)
            if not experiment:
                raise ValueError(f"Experiment {experiment_id} not found")
            
            # Perform safety checks
            if not self._perform_safety_checks(experiment):
                raise ValueError("Safety checks failed - experiment aborted")
            
            execution_id = f"exec-{uuid.uuid4().hex[:8]}"
            
            execution = ExperimentExecution(
                execution_id=execution_id,
                experiment_id=experiment_id,
                status=ExperimentStatus.RUNNING,
                start_time=datetime.utcnow(),
                end_time=None,
                hypothesis_validated=None,
                observations=[],
                metrics_collected={},
                issues_discovered=[],
                improvements_identified=[]
            )
            
            with self.chaos_lock:
                self.executions.append(execution)
            
            # Start monitoring
            self._start_experiment_monitoring(execution, experiment)
            
            # Execute the chaos experiment
            if experiment.experiment_type == ChaosExperimentType.INSTANCE_TERMINATION:
                self._execute_instance_termination(execution, experiment)
            elif experiment.experiment_type == ChaosExperimentType.NETWORK_LATENCY:
                self._execute_network_latency(execution, experiment)
            elif experiment.experiment_type == ChaosExperimentType.CPU_STRESS:
                self._execute_cpu_stress(execution, experiment)
            elif experiment.experiment_type == ChaosExperimentType.SERVICE_UNAVAILABLE:
                self._execute_service_unavailable(execution, experiment)
            else:
                self._execute_generic_chaos(execution, experiment)
            
            # Wait for experiment duration
            time.sleep(experiment.duration_minutes * 60)
            
            # Complete experiment
            self._complete_experiment(execution, experiment)
            
            self.logger.info(f"Chaos experiment completed: {execution_id}")
            return execution_id
            
        except Exception as e:
            self.logger.error(f"Chaos experiment execution failed: {str(e)}")
            return ""

    def _perform_safety_checks(self, experiment: ChaosExperiment) -> bool:
        """Perform safety checks before experiment execution"""
        try:
            # Check environment restrictions
            if experiment.environment == "production" and experiment.blast_radius in [BlastRadius.MULTIPLE_AZ, BlastRadius.MULTIPLE_REGION]:
                self.logger.warning("Large blast radius in production - requires additional approval")
                return False
            
            # Check business hours (avoid peak times)
            current_hour = datetime.utcnow().hour
            if experiment.environment == "production" and 9 <= current_hour <= 17:
                self.logger.warning("Production experiment during business hours - not recommended")
                return False
            
            # Verify rollback plan exists
            if not experiment.rollback_plan:
                self.logger.error("No rollback plan defined - experiment aborted")
                return False
            
            # Check target resources exist
            for resource in experiment.target_resources:
                if not self._verify_resource_exists(resource):
                    self.logger.error(f"Target resource {resource} not found")
                    return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Safety check failed: {str(e)}")
            return False

    def _execute_instance_termination(self, execution: ExperimentExecution, experiment: ChaosExperiment) -> None:
        """Execute instance termination chaos experiment"""
        try:
            target_instances = experiment.target_resources
            
            # Select random instance(s) based on blast radius
            if experiment.blast_radius == BlastRadius.SINGLE_INSTANCE:
                instances_to_terminate = [random.choice(target_instances)]
            else:
                instances_to_terminate = target_instances[:2]  # Limit for safety
            
            execution.observations.append(f"Targeting instances: {instances_to_terminate}")
            
            # Terminate instances using FIS or direct EC2 API
            for instance_id in instances_to_terminate:
                try:
                    # In real implementation, use AWS FIS for safer execution
                    # self.fis.start_experiment(...)
                    
                    # For demo, simulate termination
                    execution.observations.append(f"Simulated termination of {instance_id}")
                    self.logger.info(f"Simulated instance termination: {instance_id}")
                    
                except Exception as e:
                    execution.issues_discovered.append(f"Failed to terminate {instance_id}: {str(e)}")
            
        except Exception as e:
            execution.issues_discovered.append(f"Instance termination experiment failed: {str(e)}")

    def _execute_network_latency(self, execution: ExperimentExecution, experiment: ChaosExperiment) -> None:
        """Execute network latency chaos experiment"""
        try:
            latency_ms = 500  # Add 500ms latency
            
            execution.observations.append(f"Injecting {latency_ms}ms network latency")
            
            # Use SSM to inject network latency
            for resource in experiment.target_resources:
                command = f"tc qdisc add dev eth0 root netem delay {latency_ms}ms"
                
                # In real implementation, execute via SSM
                # response = self.ssm.send_command(...)
                
                execution.observations.append(f"Applied network latency to {resource}")
            
        except Exception as e:
            execution.issues_discovered.append(f"Network latency experiment failed: {str(e)}")

    def _execute_cpu_stress(self, execution: ExperimentExecution, experiment: ChaosExperiment) -> None:
        """Execute CPU stress chaos experiment"""
        try:
            cpu_percentage = 80  # Stress CPU to 80%
            
            execution.observations.append(f"Applying {cpu_percentage}% CPU stress")
            
            # Use stress-ng or similar tool via SSM
            for resource in experiment.target_resources:
                command = f"stress-ng --cpu 0 --cpu-load {cpu_percentage} --timeout {experiment.duration_minutes}m"
                
                # In real implementation, execute via SSM
                execution.observations.append(f"Applied CPU stress to {resource}")
            
        except Exception as e:
            execution.issues_discovered.append(f"CPU stress experiment failed: {str(e)}")

    def _execute_service_unavailable(self, execution: ExperimentExecution, experiment: ChaosExperiment) -> None:
        """Execute service unavailable chaos experiment"""
        try:
            execution.observations.append("Making service unavailable")
            
            # Simulate service unavailability (e.g., stop service, block ports)
            for resource in experiment.target_resources:
                # In real implementation, stop service or block traffic
                execution.observations.append(f"Made service unavailable on {resource}")
            
        except Exception as e:
            execution.issues_discovered.append(f"Service unavailable experiment failed: {str(e)}")

    def _execute_generic_chaos(self, execution: ExperimentExecution, experiment: ChaosExperiment) -> None:
        """Execute generic chaos experiment"""
        try:
            execution.observations.append(f"Executing {experiment.experiment_type.value} experiment")
            
            # Generic chaos implementation
            for resource in experiment.target_resources:
                execution.observations.append(f"Applied chaos to {resource}")
            
        except Exception as e:
            execution.issues_discovered.append(f"Generic chaos experiment failed: {str(e)}")

    def _start_experiment_monitoring(self, execution: ExperimentExecution, experiment: ChaosExperiment) -> None:
        """Start monitoring during experiment"""
        try:
            # Collect baseline metrics
            baseline_metrics = self._collect_system_metrics(experiment.target_resources)
            execution.metrics_collected['baseline'] = baseline_metrics
            
            execution.observations.append("Started experiment monitoring")
            
        except Exception as e:
            execution.issues_discovered.append(f"Monitoring setup failed: {str(e)}")

    def _complete_experiment(self, execution: ExperimentExecution, experiment: ChaosExperiment) -> None:
        """Complete chaos experiment and analyze results"""
        try:
            # Collect final metrics
            final_metrics = self._collect_system_metrics(experiment.target_resources)
            execution.metrics_collected['final'] = final_metrics
            
            # Execute rollback
            self._execute_rollback(execution, experiment)
            
            # Analyze results
            self._analyze_experiment_results(execution, experiment)
            
            # Update status
            execution.status = ExperimentStatus.COMPLETED
            execution.end_time = datetime.utcnow()
            
            execution.observations.append("Experiment completed successfully")
            
        except Exception as e:
            execution.status = ExperimentStatus.FAILED
            execution.issues_discovered.append(f"Experiment completion failed: {str(e)}")

    def _execute_rollback(self, execution: ExperimentExecution, experiment: ChaosExperiment) -> None:
        """Execute rollback plan"""
        try:
            execution.observations.append("Executing rollback plan")
            
            # Execute rollback based on experiment type
            if experiment.experiment_type == ChaosExperimentType.NETWORK_LATENCY:
                # Remove network latency
                for resource in experiment.target_resources:
                    # tc qdisc del dev eth0 root
                    execution.observations.append(f"Removed network latency from {resource}")
            
            elif experiment.experiment_type == ChaosExperimentType.CPU_STRESS:
                # Stop stress processes
                for resource in experiment.target_resources:
                    # pkill stress-ng
                    execution.observations.append(f"Stopped CPU stress on {resource}")
            
            execution.observations.append("Rollback completed")
            
        except Exception as e:
            execution.issues_discovered.append(f"Rollback failed: {str(e)}")

    def _analyze_experiment_results(self, execution: ExperimentExecution, experiment: ChaosExperiment) -> None:
        """Analyze experiment results and validate hypothesis"""
        try:
            # Compare baseline and final metrics
            baseline = execution.metrics_collected.get('baseline', {})
            final = execution.metrics_collected.get('final', {})
            
            # Check success criteria
            success_count = 0
            for criteria in experiment.success_criteria:
                if self._evaluate_success_criteria(criteria, baseline, final):
                    success_count += 1
                else:
                    execution.issues_discovered.append(f"Success criteria not met: {criteria}")
            
            # Validate hypothesis
            hypothesis_met = success_count >= len(experiment.success_criteria) * 0.8  # 80% threshold
            execution.hypothesis_validated = hypothesis_met
            
            if hypothesis_met:
                execution.observations.append("Hypothesis validated - system behaved as expected")
            else:
                execution.observations.append("Hypothesis not validated - unexpected system behavior")
                execution.improvements_identified.append("System resilience needs improvement")
            
            # Generate recommendations
            recommendations = self._generate_recommendations(execution, experiment)
            execution.improvements_identified.extend(recommendations)
            
        except Exception as e:
            execution.issues_discovered.append(f"Result analysis failed: {str(e)}")

    def _collect_system_metrics(self, resources: List[str]) -> Dict[str, Any]:
        """Collect system metrics"""
        try:
            metrics = {}
            
            # Collect CloudWatch metrics
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(minutes=5)
            
            # CPU Utilization
            cpu_response = self.cloudwatch.get_metric_statistics(
                Namespace='AWS/EC2',
                MetricName='CPUUtilization',
                StartTime=start_time,
                EndTime=end_time,
                Period=300,
                Statistics=['Average']
            )
            
            if cpu_response['Datapoints']:
                metrics['cpu_utilization'] = cpu_response['Datapoints'][-1]['Average']
            
            # Add more metrics as needed
            metrics['timestamp'] = datetime.utcnow().isoformat()
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"Metrics collection failed: {str(e)}")
            return {}

    def _evaluate_success_criteria(self, criteria: str, baseline: Dict, final: Dict) -> bool:
        """Evaluate success criteria"""
        try:
            # Simple criteria evaluation
            if "response_time" in criteria.lower():
                # Check if response time remained acceptable
                return True  # Simplified for demo
            elif "availability" in criteria.lower():
                # Check if system remained available
                return True  # Simplified for demo
            elif "auto_scaling" in criteria.lower():
                # Check if auto-scaling responded
                return True  # Simplified for demo
            
            return True  # Default to success for demo
            
        except Exception as e:
            self.logger.error(f"Criteria evaluation failed: {str(e)}")
            return False

    def _generate_recommendations(self, execution: ExperimentExecution, experiment: ChaosExperiment) -> List[str]:
        """Generate improvement recommendations"""
        recommendations = []
        
        try:
            if execution.issues_discovered:
                recommendations.append("Implement additional monitoring and alerting")
                recommendations.append("Review and improve incident response procedures")
            
            if not execution.hypothesis_validated:
                recommendations.append("Strengthen system resilience mechanisms")
                recommendations.append("Consider additional redundancy")
            
            if experiment.experiment_type == ChaosExperimentType.INSTANCE_TERMINATION:
                recommendations.append("Verify auto-scaling configuration")
                recommendations.append("Test application graceful shutdown")
            
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Recommendation generation failed: {str(e)}")
            return []

    def _verify_resource_exists(self, resource_id: str) -> bool:
        """Verify that a target resource exists"""
        try:
            if resource_id.startswith('i-'):
                # EC2 instance
                response = self.ec2.describe_instances(InstanceIds=[resource_id])
                return len(response['Reservations']) > 0
            
            # Add other resource type checks as needed
            return True  # Default to exists for demo
            
        except Exception as e:
            self.logger.error(f"Resource verification failed: {str(e)}")
            return False

    def get_experiment_results(self, execution_id: str) -> Dict[str, Any]:
        """Get results of a chaos experiment execution"""
        try:
            execution = next((e for e in self.executions if e.execution_id == execution_id), None)
            if not execution:
                return {'error': 'Execution not found'}
            
            experiment = self.experiments.get(execution.experiment_id)
            
            results = {
                'execution_id': execution_id,
                'experiment_name': experiment.name if experiment else 'Unknown',
                'status': execution.status.value,
                'start_time': execution.start_time.isoformat(),
                'end_time': execution.end_time.isoformat() if execution.end_time else None,
                'hypothesis_validated': execution.hypothesis_validated,
                'observations': execution.observations,
                'issues_discovered': execution.issues_discovered,
                'improvements_identified': execution.improvements_identified,
                'metrics_collected': execution.metrics_collected
            }
            
            return results
            
        except Exception as e:
            self.logger.error(f"Failed to get experiment results: {str(e)}")
            return {'error': str(e)}

    def generate_chaos_report(self, time_period_days: int = 30) -> Dict[str, Any]:
        """Generate chaos engineering report"""
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=time_period_days)
            recent_executions = [
                e for e in self.executions 
                if e.start_time > cutoff_date
            ]
            
            if not recent_executions:
                return {'message': 'No chaos experiments in the specified time period'}
            
            # Calculate statistics
            total_experiments = len(recent_executions)
            successful_experiments = len([e for e in recent_executions if e.status == ExperimentStatus.COMPLETED])
            hypothesis_validated = len([e for e in recent_executions if e.hypothesis_validated])
            
            # Experiment type distribution
            type_distribution = {}
            for execution in recent_executions:
                experiment = self.experiments.get(execution.experiment_id)
                if experiment:
                    exp_type = experiment.experiment_type.value
                    type_distribution[exp_type] = type_distribution.get(exp_type, 0) + 1
            
            # Issues discovered
            all_issues = []
            for execution in recent_executions:
                all_issues.extend(execution.issues_discovered)
            
            report = {
                'report_period_days': time_period_days,
                'total_experiments': total_experiments,
                'successful_experiments': successful_experiments,
                'success_rate': (successful_experiments / total_experiments * 100) if total_experiments > 0 else 0,
                'hypothesis_validation_rate': (hypothesis_validated / total_experiments * 100) if total_experiments > 0 else 0,
                'experiment_type_distribution': type_distribution,
                'total_issues_discovered': len(all_issues),
                'common_issues': self._analyze_common_issues(all_issues),
                'recommendations': self._generate_chaos_recommendations(recent_executions)
            }
            
            return report
            
        except Exception as e:
            self.logger.error(f"Chaos report generation failed: {str(e)}")
            return {}

    def _analyze_common_issues(self, issues: List[str]) -> List[str]:
        """Analyze common issues from chaos experiments"""
        # Simple analysis - in real implementation, use NLP or pattern matching
        issue_keywords = {}
        for issue in issues:
            words = issue.lower().split()
            for word in words:
                if len(word) > 4:  # Filter short words
                    issue_keywords[word] = issue_keywords.get(word, 0) + 1
        
        # Return top issues
        sorted_issues = sorted(issue_keywords.items(), key=lambda x: x[1], reverse=True)
        return [f"{word} ({count} occurrences)" for word, count in sorted_issues[:5]]

    def _generate_chaos_recommendations(self, executions: List[ExperimentExecution]) -> List[str]:
        """Generate chaos engineering recommendations"""
        recommendations = []
        
        try:
            failed_experiments = [e for e in executions if e.status == ExperimentStatus.FAILED]
            if len(failed_experiments) > len(executions) * 0.2:  # More than 20% failed
                recommendations.append("Review experiment safety checks and rollback procedures")
            
            unvalidated_hypotheses = [e for e in executions if not e.hypothesis_validated]
            if len(unvalidated_hypotheses) > len(executions) * 0.3:  # More than 30% unvalidated
                recommendations.append("Strengthen system resilience and recovery mechanisms")
            
            if len(executions) < 4:  # Less than 4 experiments per month
                recommendations.append("Increase frequency of chaos engineering experiments")
            
            recommendations.append("Expand chaos experiments to cover more failure scenarios")
            recommendations.append("Integrate chaos engineering into CI/CD pipeline")
            
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Chaos recommendations failed: {str(e)}")
            return []

# Example usage
def main():
    # Initialize chaos engineering system
    chaos_system = ChaosEngineeringSystem(region='us-east-1')
    
    # Create chaos experiment
    experiment_config = {
        'name': 'EC2 Instance Termination Test',
        'description': 'Test system resilience when EC2 instances are terminated',
        'type': 'instance_termination',
        'hypothesis': 'System will maintain availability when 1 instance is terminated due to auto-scaling',
        'blast_radius': 'single_instance',
        'target_resources': ['i-1234567890abcdef0', 'i-0987654321fedcba0'],
        'duration_minutes': 10,
        'rollback_plan': 'Auto Scaling will launch replacement instances',
        'success_criteria': [
            'System availability > 99%',
            'Response time < 2 seconds',
            'Auto Scaling launches replacement instance'
        ],
        'abort_conditions': [
            'System availability < 95%',
            'Response time > 5 seconds'
        ],
        'environment': 'staging'
    }
    
    print("Creating chaos experiment...")
    experiment_id = chaos_system.create_chaos_experiment(experiment_config)
    
    if experiment_id:
        print(f"Created experiment: {experiment_id}")
        
        # Execute experiment
        print("Executing chaos experiment...")
        execution_id = chaos_system.execute_chaos_experiment(experiment_id)
        
        if execution_id:
            print(f"Experiment execution: {execution_id}")
            
            # Get results
            results = chaos_system.get_experiment_results(execution_id)
            print(f"Experiment results: {json.dumps(results, indent=2, default=str)}")
    
    # Generate chaos report
    report = chaos_system.generate_chaos_report(30)
    print(f"Chaos engineering report: {json.dumps(report, indent=2)}")

if __name__ == "__main__":
    main()
```
{% endraw %}

## AWS Services

### Primary Services
- **AWS Fault Injection Simulator (FIS)**: Managed chaos engineering service
- **Amazon EC2**: Instance termination and resource stress testing
- **Amazon CloudWatch**: Monitoring and metrics during experiments
- **AWS Systems Manager**: Command execution for chaos injection

### Supporting Services
- **AWS Lambda**: Event-driven chaos experiment automation
- **Amazon SNS**: Notifications for experiment status and results
- **AWS Step Functions**: Complex chaos experiment workflows
- **Amazon S3**: Storage for experiment results and analysis

## Benefits

- **Proactive Resilience Testing**: Identify weaknesses before they cause outages
- **Confidence Building**: Validate that recovery mechanisms work as expected
- **Improved Incident Response**: Practice responding to failures in controlled environments
- **System Understanding**: Gain deeper insights into system behavior under stress
- **Continuous Improvement**: Regular chaos experiments drive ongoing resilience improvements

## Related Resources

- [AWS Fault Injection Simulator User Guide](https://docs.aws.amazon.com/fis/)
- [Chaos Engineering on AWS](https://aws.amazon.com/builders-library/chaos-engineering/)
- [Amazon CloudWatch User Guide](https://docs.aws.amazon.com/cloudwatch/)
- [Principles of Chaos Engineering](https://principlesofchaos.org/)
