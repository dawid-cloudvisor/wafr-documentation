---
title: REL07-BP04 - Load test your workload
layout: default
parent: REL07 - How do you design your workload to adapt to changes in demand?
grand_parent: Reliability
nav_order: 4
---

# REL07-BP04: Load test your workload

## Overview

Implement comprehensive load testing strategies to validate workload performance, scaling behavior, and reliability under various demand scenarios. Load testing ensures that scaling mechanisms work correctly and helps identify performance bottlenecks before they impact production users.

## Implementation Steps

### 1. Design Load Testing Strategy
- Define load testing objectives and success criteria
- Identify critical user journeys and business transactions
- Design realistic load patterns and traffic scenarios
- Establish baseline performance metrics and targets

### 2. Create Load Testing Environments
- Set up dedicated load testing infrastructure
- Configure production-like test environments
- Implement data seeding and test data management
- Establish network and security configurations

### 3. Implement Load Testing Scenarios
- Design gradual load increase and spike testing
- Create sustained load and endurance testing
- Implement stress testing and breaking point analysis
- Design volume testing and capacity validation

### 4. Configure Automated Load Testing
- Implement continuous load testing in CI/CD pipelines
- Configure scheduled load testing for regular validation
- Design chaos engineering and failure injection testing
- Establish performance regression testing

### 5. Monitor and Analyze Results
- Implement comprehensive performance monitoring during tests
- Configure real-time dashboards and alerting
- Design automated result analysis and reporting
- Establish performance trend analysis and benchmarking

### 6. Optimize Based on Results
- Identify and resolve performance bottlenecks
- Tune scaling policies and thresholds
- Optimize resource configurations and capacity planning
- Implement continuous improvement processes

## Implementation Examples

### Example 1: Comprehensive Load Testing Framework
```python
import boto3
import json
import logging
import asyncio
import aiohttp
import time
import statistics
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import concurrent.futures
import numpy as np

class LoadTestType(Enum):
    BASELINE = "baseline"
    SPIKE = "spike"
    STRESS = "stress"
    VOLUME = "volume"
    ENDURANCE = "endurance"
    SCALABILITY = "scalability"

class TestPhase(Enum):
    RAMP_UP = "ramp_up"
    STEADY_STATE = "steady_state"
    RAMP_DOWN = "ramp_down"
    SPIKE_PHASE = "spike_phase"

@dataclass
class LoadTestConfig:
    test_id: str
    test_name: str
    test_type: LoadTestType
    target_url: str
    max_users: int
    duration_minutes: int
    ramp_up_minutes: int
    ramp_down_minutes: int
    request_patterns: List[Dict[str, Any]]
    success_criteria: Dict[str, float]
    monitoring_config: Dict[str, Any]

@dataclass
class LoadTestResult:
    test_id: str
    start_time: datetime
    end_time: datetime
    total_requests: int
    successful_requests: int
    failed_requests: int
    average_response_time: float
    p95_response_time: float
    p99_response_time: float
    max_response_time: float
    requests_per_second: float
    error_rate: float
    throughput_mbps: float
    success_criteria_met: bool

@dataclass
class PerformanceMetrics:
    timestamp: datetime
    active_users: int
    response_time: float
    requests_per_second: float
    error_rate: float
    cpu_utilization: float
    memory_utilization: float
    network_io: float

class LoadTestingFramework:
    """Comprehensive load testing framework"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
        # AWS clients
        self.cloudwatch = boto3.client('cloudwatch')
        self.autoscaling = boto3.client('autoscaling')
        self.elbv2 = boto3.client('elbv2')
        self.lambda_client = boto3.client('lambda')
        self.dynamodb = boto3.resource('dynamodb')
        
        # Storage
        self.results_table = self.dynamodb.Table(config.get('results_table', 'load-test-results'))
        self.metrics_table = self.dynamodb.Table(config.get('metrics_table', 'load-test-metrics'))
        
        # Test configuration
        self.active_tests = {}
        self.performance_data = []
        
    async def execute_load_test(self, test_config: LoadTestConfig) -> LoadTestResult:
        """Execute comprehensive load test"""
        try:
            logging.info(f"Starting load test: {test_config.test_name}")
            
            # Initialize test
            test_result = LoadTestResult(
                test_id=test_config.test_id,
                start_time=datetime.utcnow(),
                end_time=datetime.utcnow(),
                total_requests=0,
                successful_requests=0,
                failed_requests=0,
                average_response_time=0.0,
                p95_response_time=0.0,
                p99_response_time=0.0,
                max_response_time=0.0,
                requests_per_second=0.0,
                error_rate=0.0,
                throughput_mbps=0.0,
                success_criteria_met=False
            )
            
            # Start monitoring
            monitoring_task = asyncio.create_task(
                self._monitor_system_metrics(test_config)
            )
            
            # Execute test based on type
            if test_config.test_type == LoadTestType.BASELINE:
                await self._execute_baseline_test(test_config, test_result)
            elif test_config.test_type == LoadTestType.SPIKE:
                await self._execute_spike_test(test_config, test_result)
            elif test_config.test_type == LoadTestType.STRESS:
                await self._execute_stress_test(test_config, test_result)
            elif test_config.test_type == LoadTestType.VOLUME:
                await self._execute_volume_test(test_config, test_result)
            elif test_config.test_type == LoadTestType.ENDURANCE:
                await self._execute_endurance_test(test_config, test_result)
            elif test_config.test_type == LoadTestType.SCALABILITY:
                await self._execute_scalability_test(test_config, test_result)
            
            # Stop monitoring
            monitoring_task.cancel()
            
            # Finalize results
            test_result.end_time = datetime.utcnow()
            test_result.success_criteria_met = self._evaluate_success_criteria(
                test_result, test_config.success_criteria
            )
            
            # Store results
            await self._store_test_results(test_result)
            
            # Generate report
            await self._generate_test_report(test_config, test_result)
            
            logging.info(f"Completed load test: {test_config.test_name}")
            return test_result
            
        except Exception as e:
            logging.error(f"Failed to execute load test: {str(e)}")
            raise
    
    async def _execute_baseline_test(self, config: LoadTestConfig, result: LoadTestResult):
        """Execute baseline performance test"""
        try:
            # Gradual ramp-up to target load
            await self._ramp_up_load(config, result)
            
            # Maintain steady state
            await self._maintain_steady_load(config, result)
            
            # Gradual ramp-down
            await self._ramp_down_load(config, result)
            
        except Exception as e:
            logging.error(f"Failed to execute baseline test: {str(e)}")
            raise
    
    async def _execute_spike_test(self, config: LoadTestConfig, result: LoadTestResult):
        """Execute spike load test"""
        try:
            # Start with baseline load
            baseline_users = config.max_users // 4
            await self._generate_load(baseline_users, config, result, duration_minutes=2)
            
            # Sudden spike to maximum load
            await self._generate_load(config.max_users, config, result, duration_minutes=5)
            
            # Return to baseline
            await self._generate_load(baseline_users, config, result, duration_minutes=2)
            
        except Exception as e:
            logging.error(f"Failed to execute spike test: {str(e)}")
            raise
    
    async def _execute_stress_test(self, config: LoadTestConfig, result: LoadTestResult):
        """Execute stress test to find breaking point"""
        try:
            current_users = config.max_users
            increment = config.max_users // 4
            
            while current_users <= config.max_users * 3:  # Test up to 3x normal load
                logging.info(f"Testing with {current_users} users")
                
                # Test current load level
                phase_result = await self._generate_load(
                    current_users, config, result, duration_minutes=3
                )
                
                # Check if system is still stable
                if phase_result['error_rate'] > 5.0:  # 5% error threshold
                    logging.info(f"Breaking point reached at {current_users} users")
                    break
                
                current_users += increment
            
        except Exception as e:
            logging.error(f"Failed to execute stress test: {str(e)}")
            raise
    
    async def _execute_scalability_test(self, config: LoadTestConfig, result: LoadTestResult):
        """Execute scalability test to validate auto scaling"""
        try:
            # Record initial capacity
            initial_capacity = await self._get_current_capacity()
            
            # Gradually increase load and monitor scaling
            for load_level in [25, 50, 75, 100]:
                users = int(config.max_users * (load_level / 100))
                logging.info(f"Testing scalability at {load_level}% load ({users} users)")
                
                # Generate load
                await self._generate_load(users, config, result, duration_minutes=10)
                
                # Monitor scaling behavior
                current_capacity = await self._get_current_capacity()
                scaling_occurred = current_capacity > initial_capacity
                
                logging.info(f"Capacity changed from {initial_capacity} to {current_capacity}")
                
                # Wait for scaling to complete
                await asyncio.sleep(300)  # 5 minutes
            
        except Exception as e:
            logging.error(f"Failed to execute scalability test: {str(e)}")
            raise
    
    async def _generate_load(self, users: int, config: LoadTestConfig, 
                           result: LoadTestResult, duration_minutes: int) -> Dict[str, Any]:
        """Generate load with specified number of users"""
        try:
            start_time = time.time()
            end_time = start_time + (duration_minutes * 60)
            
            # Create user sessions
            tasks = []
            for user_id in range(users):
                task = asyncio.create_task(
                    self._simulate_user_session(user_id, config, end_time)
                )
                tasks.append(task)
            
            # Wait for all sessions to complete
            session_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Aggregate results
            phase_result = self._aggregate_session_results(session_results)
            
            # Update overall test result
            result.total_requests += phase_result['total_requests']
            result.successful_requests += phase_result['successful_requests']
            result.failed_requests += phase_result['failed_requests']
            
            return phase_result
            
        except Exception as e:
            logging.error(f"Failed to generate load: {str(e)}")
            return {'error_rate': 100.0}
    
    async def _simulate_user_session(self, user_id: int, config: LoadTestConfig, 
                                   end_time: float) -> Dict[str, Any]:
        """Simulate individual user session"""
        session_result = {
            'user_id': user_id,
            'requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'response_times': [],
            'errors': []
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                while time.time() < end_time:
                    # Select request pattern
                    pattern = self._select_request_pattern(config.request_patterns)
                    
                    # Execute request
                    request_result = await self._execute_request(session, pattern, config)
                    
                    # Record results
                    session_result['requests'] += 1
                    if request_result['success']:
                        session_result['successful_requests'] += 1
                        session_result['response_times'].append(request_result['response_time'])
                    else:
                        session_result['failed_requests'] += 1
                        session_result['errors'].append(request_result['error'])
                    
                    # Think time between requests
                    think_time = pattern.get('think_time', 1.0)
                    await asyncio.sleep(think_time)
            
            return session_result
            
        except Exception as e:
            logging.error(f"User session {user_id} failed: {str(e)}")
            session_result['errors'].append(str(e))
            return session_result
    
    def _select_request_pattern(self, patterns: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Select request pattern based on weights"""
        import random
        
        total_weight = sum(pattern.get('weight', 1) for pattern in patterns)
        random_value = random.uniform(0, total_weight)
        
        current_weight = 0
        for pattern in patterns:
            current_weight += pattern.get('weight', 1)
            if random_value <= current_weight:
                return pattern
        
        return patterns[0]  # Fallback
    
    async def _execute_request(self, session: aiohttp.ClientSession, 
                             pattern: Dict[str, Any], config: LoadTestConfig) -> Dict[str, Any]:
        """Execute HTTP request"""
        try:
            start_time = time.time()
            
            method = pattern.get('method', 'GET')
            path = pattern.get('path', '/')
            headers = pattern.get('headers', {})
            data = pattern.get('data')
            
            url = f"{config.target_url.rstrip('/')}{path}"
            
            async with session.request(
                method=method,
                url=url,
                headers=headers,
                json=data if data else None,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                response_time = time.time() - start_time
                
                # Read response body
                await response.read()
                
                return {
                    'success': response.status < 400,
                    'status_code': response.status,
                    'response_time': response_time,
                    'error': None if response.status < 400 else f"HTTP {response.status}"
                }
                
        except Exception as e:
            response_time = time.time() - start_time
            return {
                'success': False,
                'status_code': 0,
                'response_time': response_time,
                'error': str(e)
            }
    
    def _aggregate_session_results(self, session_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Aggregate results from all user sessions"""
        try:
            total_requests = 0
            successful_requests = 0
            failed_requests = 0
            all_response_times = []
            
            for result in session_results:
                if isinstance(result, dict):  # Skip exceptions
                    total_requests += result.get('requests', 0)
                    successful_requests += result.get('successful_requests', 0)
                    failed_requests += result.get('failed_requests', 0)
                    all_response_times.extend(result.get('response_times', []))
            
            # Calculate statistics
            error_rate = (failed_requests / total_requests * 100) if total_requests > 0 else 0
            avg_response_time = statistics.mean(all_response_times) if all_response_times else 0
            
            # Calculate percentiles
            if all_response_times:
                sorted_times = sorted(all_response_times)
                p95_response_time = np.percentile(sorted_times, 95)
                p99_response_time = np.percentile(sorted_times, 99)
                max_response_time = max(sorted_times)
            else:
                p95_response_time = p99_response_time = max_response_time = 0
            
            return {
                'total_requests': total_requests,
                'successful_requests': successful_requests,
                'failed_requests': failed_requests,
                'error_rate': error_rate,
                'average_response_time': avg_response_time,
                'p95_response_time': p95_response_time,
                'p99_response_time': p99_response_time,
                'max_response_time': max_response_time
            }
            
        except Exception as e:
            logging.error(f"Failed to aggregate session results: {str(e)}")
            return {'error_rate': 100.0}
    
    async def _monitor_system_metrics(self, config: LoadTestConfig):
        """Monitor system metrics during load test"""
        try:
            while True:
                # Collect system metrics
                metrics = await self._collect_system_metrics()
                
                # Store metrics
                performance_metric = PerformanceMetrics(
                    timestamp=datetime.utcnow(),
                    active_users=0,  # Would be tracked separately
                    response_time=metrics.get('response_time', 0),
                    requests_per_second=metrics.get('requests_per_second', 0),
                    error_rate=metrics.get('error_rate', 0),
                    cpu_utilization=metrics.get('cpu_utilization', 0),
                    memory_utilization=metrics.get('memory_utilization', 0),
                    network_io=metrics.get('network_io', 0)
                )
                
                self.performance_data.append(performance_metric)
                
                # Store in database
                await self._store_performance_metrics(performance_metric)
                
                # Wait before next collection
                await asyncio.sleep(30)  # Collect every 30 seconds
                
        except asyncio.CancelledError:
            logging.info("Monitoring stopped")
        except Exception as e:
            logging.error(f"Failed to monitor system metrics: {str(e)}")
    
    async def _collect_system_metrics(self) -> Dict[str, float]:
        """Collect current system metrics"""
        try:
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(minutes=5)
            
            metrics = {}
            
            # CPU utilization
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
            
            # Response time from load balancer
            response_time_response = self.cloudwatch.get_metric_statistics(
                Namespace='AWS/ApplicationELB',
                MetricName='TargetResponseTime',
                StartTime=start_time,
                EndTime=end_time,
                Period=300,
                Statistics=['Average']
            )
            
            if response_time_response['Datapoints']:
                metrics['response_time'] = response_time_response['Datapoints'][-1]['Average']
            
            # Request count
            request_response = self.cloudwatch.get_metric_statistics(
                Namespace='AWS/ApplicationELB',
                MetricName='RequestCount',
                StartTime=start_time,
                EndTime=end_time,
                Period=300,
                Statistics=['Sum']
            )
            
            if request_response['Datapoints']:
                metrics['requests_per_second'] = request_response['Datapoints'][-1]['Sum'] / 300
            
            return metrics
            
        except Exception as e:
            logging.error(f"Failed to collect system metrics: {str(e)}")
            return {}
    
    async def _get_current_capacity(self) -> int:
        """Get current system capacity"""
        try:
            response = self.autoscaling.describe_auto_scaling_groups()
            
            total_capacity = 0
            for asg in response['AutoScalingGroups']:
                total_capacity += asg['DesiredCapacity']
            
            return total_capacity
            
        except Exception as e:
            logging.error(f"Failed to get current capacity: {str(e)}")
            return 0
    
    def _evaluate_success_criteria(self, result: LoadTestResult, 
                                 criteria: Dict[str, float]) -> bool:
        """Evaluate if test met success criteria"""
        try:
            for metric, threshold in criteria.items():
                if metric == 'max_response_time' and result.p95_response_time > threshold:
                    return False
                elif metric == 'error_rate' and result.error_rate > threshold:
                    return False
                elif metric == 'min_throughput' and result.requests_per_second < threshold:
                    return False
            
            return True
            
        except Exception as e:
            logging.error(f"Failed to evaluate success criteria: {str(e)}")
            return False
    
    async def _store_test_results(self, result: LoadTestResult):
        """Store test results in DynamoDB"""
        try:
            result_dict = asdict(result)
            result_dict['start_time'] = result.start_time.isoformat()
            result_dict['end_time'] = result.end_time.isoformat()
            
            self.results_table.put_item(Item=result_dict)
            
        except Exception as e:
            logging.error(f"Failed to store test results: {str(e)}")
    
    async def _store_performance_metrics(self, metrics: PerformanceMetrics):
        """Store performance metrics in DynamoDB"""
        try:
            metrics_dict = asdict(metrics)
            metrics_dict['timestamp'] = metrics.timestamp.isoformat()
            
            self.metrics_table.put_item(Item=metrics_dict)
            
        except Exception as e:
            logging.error(f"Failed to store performance metrics: {str(e)}")
    
    async def _generate_test_report(self, config: LoadTestConfig, result: LoadTestResult):
        """Generate comprehensive test report"""
        try:
            report = {
                'test_summary': {
                    'test_name': config.test_name,
                    'test_type': config.test_type.value,
                    'duration': str(result.end_time - result.start_time),
                    'success_criteria_met': result.success_criteria_met
                },
                'performance_metrics': {
                    'total_requests': result.total_requests,
                    'successful_requests': result.successful_requests,
                    'failed_requests': result.failed_requests,
                    'error_rate': f"{result.error_rate:.2f}%",
                    'average_response_time': f"{result.average_response_time:.3f}s",
                    'p95_response_time': f"{result.p95_response_time:.3f}s",
                    'p99_response_time': f"{result.p99_response_time:.3f}s",
                    'requests_per_second': f"{result.requests_per_second:.2f}"
                },
                'system_behavior': {
                    'scaling_observed': len(self.performance_data) > 0,
                    'peak_cpu_utilization': max([m.cpu_utilization for m in self.performance_data]) if self.performance_data else 0,
                    'peak_memory_utilization': max([m.memory_utilization for m in self.performance_data]) if self.performance_data else 0
                }
            }
            
            logging.info(f"Test Report: {json.dumps(report, indent=2)}")
            
        except Exception as e:
            logging.error(f"Failed to generate test report: {str(e)}")

# Usage example
async def main():
    config = {
        'results_table': 'load-test-results',
        'metrics_table': 'load-test-metrics'
    }
    
    # Initialize load testing framework
    load_tester = LoadTestingFramework(config)
    
    # Create load test configuration
    test_config = LoadTestConfig(
        test_id='baseline_test_001',
        test_name='Baseline Performance Test',
        test_type=LoadTestType.BASELINE,
        target_url='https://api.example.com',
        max_users=100,
        duration_minutes=30,
        ramp_up_minutes=5,
        ramp_down_minutes=5,
        request_patterns=[
            {
                'method': 'GET',
                'path': '/api/health',
                'weight': 1,
                'think_time': 1.0
            },
            {
                'method': 'GET',
                'path': '/api/users',
                'weight': 3,
                'think_time': 2.0
            },
            {
                'method': 'POST',
                'path': '/api/orders',
                'weight': 2,
                'think_time': 3.0,
                'data': {'product_id': 123, 'quantity': 1}
            }
        ],
        success_criteria={
            'max_response_time': 2.0,  # 2 seconds
            'error_rate': 1.0,         # 1%
            'min_throughput': 50.0     # 50 RPS
        },
        monitoring_config={}
    )
    
    # Execute load test
    result = await load_tester.execute_load_test(test_config)
    
    print(f"Load test completed: {result.success_criteria_met}")
    print(f"Total requests: {result.total_requests}")
    print(f"Error rate: {result.error_rate:.2f}%")
    print(f"Average response time: {result.average_response_time:.3f}s")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## AWS Services Used

- **Amazon EC2**: Load testing infrastructure and target system monitoring
- **Elastic Load Balancing**: Performance metrics collection and health monitoring
- **Amazon CloudWatch**: System metrics monitoring and performance analysis
- **AWS Lambda**: Serverless load testing functions and custom metrics collection
- **Amazon DynamoDB**: Storage for test results, metrics, and configuration data
- **Amazon S3**: Storage for test reports, logs, and historical data
- **AWS Auto Scaling**: Validation of scaling behavior during load tests
- **Amazon API Gateway**: API load testing and throttling validation
- **AWS Step Functions**: Complex load testing workflow orchestration
- **Amazon Kinesis**: Real-time metrics streaming and analysis
- **AWS X-Ray**: Application performance tracing during load tests
- **Amazon ECS/EKS**: Container-based load testing infrastructure
- **AWS CodeBuild**: Automated load testing in CI/CD pipelines
- **Amazon SNS**: Load testing notifications and alerting
- **AWS Systems Manager**: Parameter management for test configurations

## Benefits

- **Performance Validation**: Verify system performance under various load conditions
- **Scaling Verification**: Validate that auto scaling mechanisms work correctly
- **Bottleneck Identification**: Identify performance bottlenecks before production deployment
- **Capacity Planning**: Determine optimal resource configurations and limits
- **Reliability Assurance**: Ensure system stability under expected and peak loads
- **Cost Optimization**: Right-size resources based on actual performance requirements
- **Risk Mitigation**: Reduce the risk of performance issues in production
- **Continuous Validation**: Regular testing ensures ongoing performance quality
- **Business Confidence**: Provide confidence in system ability to handle business growth
- **Proactive Optimization**: Identify and resolve issues before they impact users

## Related Resources

- [AWS Well-Architected Reliability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/)
- [Load Test Your Workload](https://docs.aws.amazon.com/wellarchitected/latest/framework/rel_adapt_to_changes_in_demand_load_test.html)
- [Amazon EC2 User Guide](https://docs.aws.amazon.com/ec2/latest/userguide/)
- [Elastic Load Balancing User Guide](https://docs.aws.amazon.com/elasticloadbalancing/latest/userguide/)
- [Amazon CloudWatch User Guide](https://docs.aws.amazon.com/cloudwatch/latest/monitoring/)
- [AWS Lambda Developer Guide](https://docs.aws.amazon.com/lambda/latest/dg/)
- [Amazon DynamoDB Developer Guide](https://docs.aws.amazon.com/dynamodb/latest/developerguide/)
- [AWS Auto Scaling User Guide](https://docs.aws.amazon.com/autoscaling/application/userguide/)
- [AWS Step Functions Developer Guide](https://docs.aws.amazon.com/step-functions/latest/dg/)
- [AWS X-Ray Developer Guide](https://docs.aws.amazon.com/xray/latest/devguide/)
- [Load Testing Best Practices](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)
- [Performance Testing on AWS](https://docs.aws.amazon.com/whitepapers/latest/performance-testing-on-aws/performance-testing-on-aws.html)
