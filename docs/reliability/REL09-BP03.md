---
title: REL09-BP03 - Perform data backup automatically
layout: default
parent: REL09 - How do you back up data?
grand_parent: Reliability
nav_order: 3
---

# REL09-BP03: Perform data backup automatically

## Overview

Implement comprehensive automated backup systems that eliminate manual processes and ensure consistent, reliable data protection. Automated backup solutions provide scheduled backups, policy-driven retention, cross-region replication, and intelligent backup orchestration to meet recovery objectives without human intervention.

## Implementation Steps

### 1. Design Automated Backup Architecture
- Implement centralized backup scheduling and orchestration
- Configure policy-driven backup automation based on data classification
- Design cross-service backup coordination and dependencies
- Establish backup workflow automation and error handling

### 2. Configure Backup Scheduling and Policies
- Implement automated backup scheduling based on RPO requirements
- Configure retention policies with automated lifecycle management
- Design backup frequency optimization based on data change patterns
- Establish backup window management and resource optimization

### 3. Implement Cross-Region Backup Automation
- Configure automated cross-region backup replication
- Implement disaster recovery backup strategies
- Design geographic distribution for backup resilience
- Establish automated failover and recovery procedures

### 4. Set Up Backup Monitoring and Alerting
- Implement automated backup success and failure monitoring
- Configure backup performance and duration tracking
- Design backup storage utilization and cost monitoring
- Establish automated alerting for backup issues and failures

### 5. Configure Backup Validation and Testing
- Implement automated backup integrity validation
- Configure periodic backup restoration testing
- Design backup completeness verification
- Establish automated backup quality assurance

### 6. Optimize Backup Performance and Costs
- Implement intelligent backup deduplication and compression
- Configure storage class optimization and lifecycle policies
- Design backup network optimization and bandwidth management
- Establish cost monitoring and optimization automation

## Implementation Examples

### Example 1: Comprehensive Automated Backup System
{% raw %}
```python
import boto3
import json
import logging
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import cron_descriptor

class BackupFrequency(Enum):
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

class BackupStatus(Enum):
    SCHEDULED = "scheduled"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class AutomatedBackupJob:
    job_id: str
    resource_arn: str
    backup_vault_name: str
    backup_plan_id: str
    schedule_expression: str
    retention_days: int
    cross_region_copy: bool
    destination_region: Optional[str]
    encryption_key_arn: str
    tags: Dict[str, str]
    created_at: datetime
    last_backup_time: Optional[datetime]
    next_backup_time: Optional[datetime]

@dataclass
class BackupExecution:
    execution_id: str
    job_id: str
    backup_job_id: str
    status: BackupStatus
    started_at: datetime
    completed_at: Optional[datetime]
    backup_size_bytes: Optional[int]
    recovery_point_arn: Optional[str]
    error_message: Optional[str]

class AutomatedBackupManager:
    """Comprehensive automated backup management system"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
        # AWS clients
        self.backup = boto3.client('backup')
        self.s3 = boto3.client('s3')
        self.rds = boto3.client('rds')
        self.dynamodb_client = boto3.client('dynamodb')
        self.dynamodb = boto3.resource('dynamodb')
        self.events = boto3.client('events')
        self.lambda_client = boto3.client('lambda')
        self.cloudwatch = boto3.client('cloudwatch')
        self.sns = boto3.client('sns')
        
        # Storage
        self.backup_jobs_table = self.dynamodb.Table(config.get('backup_jobs_table', 'automated-backup-jobs'))
        self.executions_table = self.dynamodb.Table(config.get('executions_table', 'backup-executions'))
        
        # Configuration
        self.default_backup_vault = config.get('default_backup_vault', 'default-backup-vault')
        self.notification_topic_arn = config.get('notification_topic_arn')
        
        # Active backup jobs
        self.active_jobs = {}
        
    async def create_automated_backup_plan(self, plan_config: Dict[str, Any]) -> str:
        """Create automated backup plan with scheduling"""
        try:
            plan_name = plan_config['plan_name']
            
            # Create backup plan
            backup_plan = {
                'BackupPlanName': plan_name,
                'Rules': []
            }
            
            # Add backup rules based on configuration
            for rule_config in plan_config['rules']:
                rule = {
                    'RuleName': rule_config['rule_name'],
                    'TargetBackupVaultName': rule_config.get('backup_vault', self.default_backup_vault),
                    'ScheduleExpression': rule_config['schedule_expression'],
                    'StartWindowMinutes': rule_config.get('start_window_minutes', 60),
                    'CompletionWindowMinutes': rule_config.get('completion_window_minutes', 120),
                    'Lifecycle': {
                        'DeleteAfterDays': rule_config.get('retention_days', 30)
                    },
                    'RecoveryPointTags': rule_config.get('tags', {}),
                    'EnableContinuousBackup': rule_config.get('continuous_backup', False)
                }
                
                # Add cross-region copy if configured
                if rule_config.get('cross_region_copy'):
                    rule['CopyActions'] = [
                        {
                            'DestinationBackupVaultArn': f"arn:aws:backup:{rule_config['destination_region']}:{boto3.client('sts').get_caller_identity()['Account']}:backup-vault:{rule_config.get('destination_vault', self.default_backup_vault)}",
                            'Lifecycle': {
                                'DeleteAfterDays': rule_config.get('cross_region_retention_days', 90)
                            }
                        }
                    ]
                
                backup_plan['Rules'].append(rule)
            
            # Create the backup plan
            plan_response = self.backup.create_backup_plan(BackupPlan=backup_plan)
            backup_plan_id = plan_response['BackupPlanId']
            
            # Create backup selection
            selection_config = plan_config.get('selection', {})
            await self._create_backup_selection(backup_plan_id, selection_config)
            
            logging.info(f"Created automated backup plan: {plan_name}")
            return backup_plan_id
            
        except Exception as e:
            logging.error(f"Failed to create automated backup plan: {str(e)}")
            raise
    
    async def _create_backup_selection(self, backup_plan_id: str, selection_config: Dict[str, Any]):
        """Create backup selection for automated backups"""
        try:
            selection_name = selection_config.get('selection_name', 'default-selection')
            
            backup_selection = {
                'SelectionName': selection_name,
                'IamRoleArn': selection_config['iam_role_arn'],
                'Resources': selection_config.get('resources', []),
                'Conditions': {}
            }
            
            # Add resource selection conditions
            if 'resource_tags' in selection_config:
                backup_selection['Conditions']['StringEquals'] = selection_config['resource_tags']
            
            if 'resource_types' in selection_config:
                backup_selection['Resources'] = [f"arn:aws:{service}:*:*:*" for service in selection_config['resource_types']]
            
            # Create backup selection
            self.backup.create_backup_selection(
                BackupPlanId=backup_plan_id,
                BackupSelection=backup_selection
            )
            
            logging.info(f"Created backup selection: {selection_name}")
            
        except Exception as e:
            logging.error(f"Failed to create backup selection: {str(e)}")
            raise
    
    async def schedule_automated_backups(self, resources: List[Dict[str, Any]]) -> List[str]:
        """Schedule automated backups for resources"""
        try:
            scheduled_jobs = []
            
            for resource in resources:
                job_config = {
                    'resource_arn': resource['resource_arn'],
                    'backup_frequency': BackupFrequency(resource.get('backup_frequency', 'daily')),
                    'retention_days': resource.get('retention_days', 30),
                    'cross_region_copy': resource.get('cross_region_copy', False),
                    'destination_region': resource.get('destination_region'),
                    'encryption_key_arn': resource.get('encryption_key_arn'),
                    'tags': resource.get('tags', {})
                }
                
                job_id = await self._create_backup_job(job_config)
                if job_id:
                    scheduled_jobs.append(job_id)
            
            logging.info(f"Scheduled {len(scheduled_jobs)} automated backup jobs")
            return scheduled_jobs
            
        except Exception as e:
            logging.error(f"Failed to schedule automated backups: {str(e)}")
            return []
    
    async def _create_backup_job(self, job_config: Dict[str, Any]) -> Optional[str]:
        """Create individual automated backup job"""
        try:
            job_id = f"backup_job_{int(datetime.utcnow().timestamp())}"
            
            # Generate schedule expression
            schedule_expression = self._generate_schedule_expression(job_config['backup_frequency'])
            
            # Calculate next backup time
            next_backup_time = self._calculate_next_backup_time(schedule_expression)
            
            # Create backup job record
            backup_job = AutomatedBackupJob(
                job_id=job_id,
                resource_arn=job_config['resource_arn'],
                backup_vault_name=self.default_backup_vault,
                backup_plan_id='',  # Will be set when plan is created
                schedule_expression=schedule_expression,
                retention_days=job_config['retention_days'],
                cross_region_copy=job_config['cross_region_copy'],
                destination_region=job_config.get('destination_region'),
                encryption_key_arn=job_config.get('encryption_key_arn', ''),
                tags=job_config['tags'],
                created_at=datetime.utcnow(),
                last_backup_time=None,
                next_backup_time=next_backup_time
            )
            
            # Store backup job
            await self._store_backup_job(backup_job)
            
            # Create EventBridge rule for scheduling
            await self._create_backup_schedule_rule(backup_job)
            
            self.active_jobs[job_id] = backup_job
            
            logging.info(f"Created automated backup job: {job_id}")
            return job_id
            
        except Exception as e:
            logging.error(f"Failed to create backup job: {str(e)}")
            return None
    
    def _generate_schedule_expression(self, frequency: BackupFrequency) -> str:
        """Generate cron expression for backup frequency"""
        schedule_expressions = {
            BackupFrequency.HOURLY: 'cron(0 * * * ? *)',      # Every hour
            BackupFrequency.DAILY: 'cron(0 2 * * ? *)',       # Daily at 2 AM
            BackupFrequency.WEEKLY: 'cron(0 2 ? * SUN *)',    # Weekly on Sunday at 2 AM
            BackupFrequency.MONTHLY: 'cron(0 2 1 * ? *)'      # Monthly on 1st at 2 AM
        }
        
        return schedule_expressions.get(frequency, 'cron(0 2 * * ? *)')
    
    def _calculate_next_backup_time(self, schedule_expression: str) -> datetime:
        """Calculate next backup time based on schedule expression"""
        # This is simplified - in practice, you'd use a cron library
        # For now, we'll add 24 hours to current time
        return datetime.utcnow() + timedelta(days=1)
    
    async def _create_backup_schedule_rule(self, backup_job: AutomatedBackupJob):
        """Create EventBridge rule for backup scheduling"""
        try:
            rule_name = f"backup-schedule-{backup_job.job_id}"
            
            # Create EventBridge rule
            self.events.put_rule(
                Name=rule_name,
                ScheduleExpression=backup_job.schedule_expression,
                Description=f"Automated backup schedule for {backup_job.resource_arn}",
                State='ENABLED'
            )
            
            # Create Lambda function target
            lambda_function_arn = await self._create_backup_trigger_function(backup_job)
            
            # Add target to rule
            self.events.put_targets(
                Rule=rule_name,
                Targets=[
                    {
                        'Id': '1',
                        'Arn': lambda_function_arn,
                        'Input': json.dumps({
                            'job_id': backup_job.job_id,
                            'resource_arn': backup_job.resource_arn
                        })
                    }
                ]
            )
            
            logging.info(f"Created backup schedule rule: {rule_name}")
            
        except Exception as e:
            logging.error(f"Failed to create backup schedule rule: {str(e)}")
            raise
    
    async def _create_backup_trigger_function(self, backup_job: AutomatedBackupJob) -> str:
        """Create Lambda function to trigger backups"""
        try:
            function_name = f"backup-trigger-{backup_job.job_id}"
            
            # Lambda function code
            lambda_code = f'''
import boto3
import json

def lambda_handler(event, context):
    backup_client = boto3.client('backup')
    
    try:
        # Start backup job
        response = backup_client.start_backup_job(
            BackupVaultName='{backup_job.backup_vault_name}',
            ResourceArn='{backup_job.resource_arn}',
            IamRoleArn='{self.config.get("backup_service_role_arn")}',
            RecoveryPointTags={json.dumps(backup_job.tags)}
        )
        
        return {{
            'statusCode': 200,
            'body': json.dumps({{
                'backup_job_id': response['BackupJobId'],
                'creation_date': response['CreationDate'].isoformat()
            }})
        }}
    except Exception as e:
        return {{
            'statusCode': 500,
            'body': json.dumps({{'error': str(e)}})
        }}
'''
            
            # Create Lambda function
            response = self.lambda_client.create_function(
                FunctionName=function_name,
                Runtime='python3.9',
                Role=self.config.get('lambda_execution_role_arn'),
                Handler='index.lambda_handler',
                Code={'ZipFile': lambda_code.encode()},
                Description=f'Backup trigger function for {backup_job.resource_arn}',
                Timeout=60
            )
            
            return response['FunctionArn']
            
        except Exception as e:
            logging.error(f"Failed to create backup trigger function: {str(e)}")
            raise
    
    async def execute_backup_job(self, job_id: str) -> str:
        """Execute automated backup job"""
        try:
            backup_job = self.active_jobs.get(job_id)
            if not backup_job:
                raise ValueError(f"Backup job {job_id} not found")
            
            # Start backup
            backup_response = self.backup.start_backup_job(
                BackupVaultName=backup_job.backup_vault_name,
                ResourceArn=backup_job.resource_arn,
                IamRoleArn=self.config.get('backup_service_role_arn'),
                RecoveryPointTags=backup_job.tags
            )
            
            backup_job_id = backup_response['BackupJobId']
            
            # Create execution record
            execution = BackupExecution(
                execution_id=f"exec_{int(datetime.utcnow().timestamp())}_{job_id}",
                job_id=job_id,
                backup_job_id=backup_job_id,
                status=BackupStatus.RUNNING,
                started_at=datetime.utcnow(),
                completed_at=None,
                backup_size_bytes=None,
                recovery_point_arn=None,
                error_message=None
            )
            
            # Store execution
            await self._store_backup_execution(execution)
            
            # Start monitoring
            asyncio.create_task(self._monitor_backup_execution(execution))
            
            # Update job last backup time
            backup_job.last_backup_time = datetime.utcnow()
            backup_job.next_backup_time = self._calculate_next_backup_time(backup_job.schedule_expression)
            await self._store_backup_job(backup_job)
            
            logging.info(f"Started backup execution: {execution.execution_id}")
            return execution.execution_id
            
        except Exception as e:
            logging.error(f"Failed to execute backup job: {str(e)}")
            raise
    
    async def _monitor_backup_execution(self, execution: BackupExecution):
        """Monitor backup job execution"""
        try:
            while execution.status == BackupStatus.RUNNING:
                # Get backup job status
                job_response = self.backup.describe_backup_job(
                    BackupJobId=execution.backup_job_id
                )
                
                job_status = job_response['State']
                
                if job_status == 'COMPLETED':
                    execution.status = BackupStatus.COMPLETED
                    execution.completed_at = datetime.utcnow()
                    execution.backup_size_bytes = job_response.get('BackupSizeInBytes')
                    execution.recovery_point_arn = job_response.get('RecoveryPointArn')
                    
                    # Send success notification
                    await self._send_backup_notification(execution, success=True)
                    
                elif job_status in ['FAILED', 'ABORTED']:
                    execution.status = BackupStatus.FAILED
                    execution.completed_at = datetime.utcnow()
                    execution.error_message = job_response.get('StatusMessage', 'Backup failed')
                    
                    # Send failure notification
                    await self._send_backup_notification(execution, success=False)
                    
                # Store updated execution
                await self._store_backup_execution(execution)
                
                # Break if completed or failed
                if execution.status in [BackupStatus.COMPLETED, BackupStatus.FAILED]:
                    break
                
                # Wait before next check
                await asyncio.sleep(60)  # Check every minute
            
        except Exception as e:
            logging.error(f"Failed to monitor backup execution: {str(e)}")
            execution.status = BackupStatus.FAILED
            execution.error_message = str(e)
            execution.completed_at = datetime.utcnow()
            await self._store_backup_execution(execution)
    
    async def _send_backup_notification(self, execution: BackupExecution, success: bool):
        """Send backup completion notification"""
        try:
            if not self.notification_topic_arn:
                return
            
            message = {
                'execution_id': execution.execution_id,
                'job_id': execution.job_id,
                'backup_job_id': execution.backup_job_id,
                'status': execution.status.value,
                'success': success,
                'started_at': execution.started_at.isoformat(),
                'completed_at': execution.completed_at.isoformat() if execution.completed_at else None,
                'backup_size_bytes': execution.backup_size_bytes,
                'error_message': execution.error_message
            }
            
            subject = f"Backup {'Completed' if success else 'Failed'}: {execution.job_id}"
            
            self.sns.publish(
                TopicArn=self.notification_topic_arn,
                Message=json.dumps(message, indent=2),
                Subject=subject
            )
            
        except Exception as e:
            logging.error(f"Failed to send backup notification: {str(e)}")
    
    async def get_backup_status_report(self) -> Dict[str, Any]:
        """Generate comprehensive backup status report"""
        try:
            # Get all backup jobs
            all_jobs = list(self.active_jobs.values())
            
            # Get recent executions
            recent_executions = await self._get_recent_executions(hours=24)
            
            # Calculate statistics
            total_jobs = len(all_jobs)
            successful_backups = len([e for e in recent_executions if e.status == BackupStatus.COMPLETED])
            failed_backups = len([e for e in recent_executions if e.status == BackupStatus.FAILED])
            
            # Calculate total backup size
            total_backup_size = sum([e.backup_size_bytes or 0 for e in recent_executions if e.backup_size_bytes])
            
            report = {
                'report_timestamp': datetime.utcnow().isoformat(),
                'summary': {
                    'total_backup_jobs': total_jobs,
                    'successful_backups_24h': successful_backups,
                    'failed_backups_24h': failed_backups,
                    'success_rate': (successful_backups / (successful_backups + failed_backups) * 100) if (successful_backups + failed_backups) > 0 else 0,
                    'total_backup_size_bytes': total_backup_size
                },
                'job_details': [
                    {
                        'job_id': job.job_id,
                        'resource_arn': job.resource_arn,
                        'schedule': job.schedule_expression,
                        'last_backup': job.last_backup_time.isoformat() if job.last_backup_time else None,
                        'next_backup': job.next_backup_time.isoformat() if job.next_backup_time else None
                    }
                    for job in all_jobs
                ],
                'recent_executions': [
                    {
                        'execution_id': exec.execution_id,
                        'status': exec.status.value,
                        'duration_minutes': ((exec.completed_at - exec.started_at).total_seconds() / 60) if exec.completed_at else None,
                        'backup_size_mb': (exec.backup_size_bytes / (1024*1024)) if exec.backup_size_bytes else None
                    }
                    for exec in recent_executions
                ]
            }
            
            return report
            
        except Exception as e:
            logging.error(f"Failed to generate backup status report: {str(e)}")
            return {'error': str(e)}
    
    async def _get_recent_executions(self, hours: int = 24) -> List[BackupExecution]:
        """Get recent backup executions"""
        try:
            # This would typically query DynamoDB with time-based filters
            # For now, we'll return a placeholder
            return []
            
        except Exception as e:
            logging.error(f"Failed to get recent executions: {str(e)}")
            return []
    
    async def _store_backup_job(self, backup_job: AutomatedBackupJob):
        """Store backup job in DynamoDB"""
        try:
            job_dict = asdict(backup_job)
            job_dict['created_at'] = backup_job.created_at.isoformat()
            if backup_job.last_backup_time:
                job_dict['last_backup_time'] = backup_job.last_backup_time.isoformat()
            if backup_job.next_backup_time:
                job_dict['next_backup_time'] = backup_job.next_backup_time.isoformat()
            
            self.backup_jobs_table.put_item(Item=job_dict)
            
        except Exception as e:
            logging.error(f"Failed to store backup job: {str(e)}")
    
    async def _store_backup_execution(self, execution: BackupExecution):
        """Store backup execution in DynamoDB"""
        try:
            execution_dict = asdict(execution)
            execution_dict['started_at'] = execution.started_at.isoformat()
            if execution.completed_at:
                execution_dict['completed_at'] = execution.completed_at.isoformat()
            
            self.executions_table.put_item(Item=execution_dict)
            
        except Exception as e:
            logging.error(f"Failed to store backup execution: {str(e)}")

# Usage example
async def main():
    config = {
        'backup_jobs_table': 'automated-backup-jobs',
        'executions_table': 'backup-executions',
        'default_backup_vault': 'production-backup-vault',
        'notification_topic_arn': 'arn:aws:sns:us-east-1:123456789012:backup-notifications',
        'backup_service_role_arn': 'arn:aws:iam::123456789012:role/AWSBackupDefaultServiceRole',
        'lambda_execution_role_arn': 'arn:aws:iam::123456789012:role/BackupLambdaExecutionRole'
    }
    
    # Initialize automated backup manager
    backup_manager = AutomatedBackupManager(config)
    
    # Create automated backup plan
    plan_config = {
        'plan_name': 'production-automated-backup-plan',
        'rules': [
            {
                'rule_name': 'daily-backup-rule',
                'schedule_expression': 'cron(0 2 * * ? *)',
                'retention_days': 30,
                'cross_region_copy': True,
                'destination_region': 'us-west-2',
                'tags': {'Environment': 'Production', 'BackupType': 'Automated'}
            }
        ],
        'selection': {
            'selection_name': 'production-resources',
            'iam_role_arn': 'arn:aws:iam::123456789012:role/AWSBackupDefaultServiceRole',
            'resource_tags': {
                'Environment': 'Production',
                'BackupRequired': 'true'
            }
        }
    }
    
    backup_plan_id = await backup_manager.create_automated_backup_plan(plan_config)
    print(f"Created backup plan: {backup_plan_id}")
    
    # Schedule automated backups for specific resources
    resources = [
        {
            'resource_arn': 'arn:aws:rds:us-east-1:123456789012:db:production-db',
            'backup_frequency': 'daily',
            'retention_days': 30,
            'cross_region_copy': True,
            'destination_region': 'us-west-2',
            'tags': {'Environment': 'Production', 'Service': 'Database'}
        }
    ]
    
    scheduled_jobs = await backup_manager.schedule_automated_backups(resources)
    print(f"Scheduled {len(scheduled_jobs)} backup jobs")
    
    # Generate status report
    status_report = await backup_manager.get_backup_status_report()
    print(f"Backup status report generated with {status_report['summary']['total_backup_jobs']} jobs")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```
{% endraw %}

## AWS Services Used

- **AWS Backup**: Centralized backup service with automated scheduling and policies
- **Amazon EventBridge**: Event-driven backup scheduling and automation triggers
- **AWS Lambda**: Custom backup automation functions and workflow orchestration
- **Amazon S3**: Backup storage with lifecycle policies and cross-region replication
- **Amazon RDS**: Automated database backups with point-in-time recovery
- **Amazon DynamoDB**: Backup job tracking and execution history storage
- **Amazon CloudWatch**: Backup monitoring, metrics, and performance tracking
- **Amazon SNS**: Backup completion notifications and alerting
- **AWS Step Functions**: Complex backup workflow orchestration and coordination
- **AWS Systems Manager**: Parameter management for backup configurations
- **Amazon EBS**: Automated snapshot creation and lifecycle management
- **Amazon EFS**: File system backup automation with scheduled snapshots
- **AWS Organizations**: Multi-account backup automation and governance
- **AWS Config**: Resource inventory and backup compliance monitoring
- **Amazon Kinesis**: Real-time backup event streaming and processing

## Benefits

- **Consistency**: Automated processes eliminate human error and ensure reliable backups
- **Efficiency**: Scheduled backups reduce manual effort and operational overhead
- **Scalability**: Automated systems scale with infrastructure growth and complexity
- **Cost Optimization**: Intelligent scheduling and lifecycle policies optimize storage costs
- **Compliance**: Automated retention and documentation support regulatory requirements
- **Reliability**: Redundant automation ensures backups continue even during failures
- **Monitoring**: Comprehensive tracking provides visibility into backup operations
- **Recovery Assurance**: Regular automated testing validates backup integrity
- **Cross-Region Protection**: Automated replication provides geographic redundancy
- **Policy Enforcement**: Automated compliance with organizational backup policies

## Related Resources

- [AWS Well-Architected Reliability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/)
- [Perform Data Backup Automatically](https://docs.aws.amazon.com/wellarchitected/latest/framework/rel_back_up_data_automated_backups_data.html)
- [AWS Backup User Guide](https://docs.aws.amazon.com/aws-backup/latest/devguide/)
- [Amazon EventBridge User Guide](https://docs.aws.amazon.com/eventbridge/latest/userguide/)
- [AWS Lambda Developer Guide](https://docs.aws.amazon.com/lambda/latest/dg/)
- [Amazon S3 User Guide](https://docs.aws.amazon.com/s3/latest/userguide/)
- [Amazon RDS User Guide](https://docs.aws.amazon.com/rds/latest/userguide/)
- [Amazon CloudWatch User Guide](https://docs.aws.amazon.com/cloudwatch/latest/monitoring/)
- [AWS Step Functions Developer Guide](https://docs.aws.amazon.com/step-functions/latest/dg/)
- [Backup Automation Best Practices](https://aws.amazon.com/backup-recovery/)
- [Disaster Recovery Strategies](https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-options-in-the-cloud.html)
- [Data Protection Automation](https://aws.amazon.com/architecture/well-architected/)
