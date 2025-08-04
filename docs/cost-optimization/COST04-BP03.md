---
title: COST04-BP03 - Decommission resources
layout: default
parent: COST04 - How do you decommission resources?
grand_parent: Cost Optimization
nav_order: 3
---

<div class="pillar-header">
  <h1>COST04-BP03: Decommission resources</h1>
  <p>Execute systematic decommissioning of identified resources following established processes and procedures. Proper execution ensures safe resource removal while maintaining service continuity and data integrity.</p>
</div>

## Implementation guidance

Resource decommissioning execution requires careful coordination and systematic approach to safely remove resources while minimizing business disruption and ensuring compliance with organizational policies and regulatory requirements.

### Execution Principles

**Systematic Approach**: Follow established procedures and checklists to ensure consistent and thorough decommissioning execution.

**Safety First**: Prioritize service continuity and data protection throughout the decommissioning process.

**Validation**: Verify each step of the decommissioning process before proceeding to prevent errors and ensure successful completion.

**Documentation**: Maintain detailed records of all decommissioning activities for audit, compliance, and learning purposes.

### Execution Components

**Pre-Execution Validation**: Verify all prerequisites are met before beginning decommissioning activities.

**Coordinated Shutdown**: Execute resource shutdown in proper sequence to minimize dependencies and service disruption.

**Data Handling**: Ensure proper data backup, archival, or migration according to retention policies.

**Post-Execution Verification**: Confirm successful decommissioning and validate achievement of objectives.

## AWS Services to Consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Systems Manager</h4>
    <p>Execute coordinated resource shutdown and management tasks. Use Systems Manager for automated execution of decommissioning procedures.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Lambda</h4>
    <p>Implement custom decommissioning logic and automation. Use Lambda for resource-specific decommissioning tasks and validation.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS CloudFormation</h4>
    <p>Manage infrastructure as code for coordinated stack decommissioning. Use CloudFormation for systematic resource group removal.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon S3</h4>
    <p>Store data backups and archives during decommissioning. Use S3 lifecycle policies for automated data management.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Backup</h4>
    <p>Create and manage backups before resource decommissioning. Use AWS Backup for centralized backup management.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon CloudWatch</h4>
    <p>Monitor decommissioning activities and validate successful completion. Use CloudWatch for process monitoring and alerting.</p>
  </div>
</div>

## Implementation Steps

### 1. Pre-Execution Preparation
- Verify all approvals and prerequisites are in place
- Confirm backup and data protection measures are complete
- Validate decommissioning plan and timeline
- Notify stakeholders of impending decommissioning activities

### 2. Execute Data Protection
- Create final backups of critical data
- Verify backup integrity and accessibility
- Archive data according to retention policies
- Document data locations and access procedures

### 3. Perform Dependency Management
- Update or migrate dependent services
- Modify configurations to remove dependencies
- Test dependency changes in staging environments
- Prepare rollback procedures for dependency issues

### 4. Execute Resource Shutdown
- Follow planned shutdown sequence
- Monitor for errors or unexpected issues
- Validate each step before proceeding
- Document any deviations from planned procedures

### 5. Validate Decommissioning Success
- Confirm resources are properly terminated
- Verify cost savings are achieved
- Validate service continuity is maintained
- Update inventory and documentation systems

### 6. Complete Post-Execution Activities
- Conduct final validation and testing
- Update monitoring and alerting configurations
- Archive decommissioning documentation
- Conduct lessons learned review

## Resource-Specific Decommissioning

### EC2 Instance Decommissioning
```python
import boto3
import time
from datetime import datetime

class EC2Decommissioner:
    def __init__(self):
        self.ec2 = boto3.client('ec2')
        self.backup = boto3.client('backup')
        self.s3 = boto3.client('s3')
        self.cloudwatch = boto3.client('cloudwatch')
    
    def decommission_ec2_instance(self, instance_id, backup_required=True):
        """Safely decommission an EC2 instance"""
        
        decommission_log = {
            'instance_id': instance_id,
            'start_time': datetime.now().isoformat(),
            'steps': [],
            'status': 'in_progress'
        }
        
        try:
            # Step 1: Get instance details
            instance_details = self.get_instance_details(instance_id)
            decommission_log['instance_details'] = instance_details
            decommission_log['steps'].append({
                'step': 'get_instance_details',
                'status': 'completed',
                'timestamp': datetime.now().isoformat()
            })
            
            # Step 2: Create backup if required
            if backup_required:
                backup_result = self.create_instance_backup(instance_id, instance_details)
                decommission_log['backup_result'] = backup_result
                decommission_log['steps'].append({
                    'step': 'create_backup',
                    'status': 'completed',
                    'timestamp': datetime.now().isoformat(),
                    'backup_id': backup_result.get('backup_job_id')
                })
            
            # Step 3: Stop instance gracefully
            stop_result = self.stop_instance_gracefully(instance_id)
            decommission_log['stop_result'] = stop_result
            decommission_log['steps'].append({
                'step': 'stop_instance',
                'status': 'completed',
                'timestamp': datetime.now().isoformat()
            })
            
            # Step 4: Create final snapshot of EBS volumes
            snapshot_results = self.create_volume_snapshots(instance_details['volumes'])
            decommission_log['snapshot_results'] = snapshot_results
            decommission_log['steps'].append({
                'step': 'create_snapshots',
                'status': 'completed',
                'timestamp': datetime.now().isoformat(),
                'snapshots': [s['snapshot_id'] for s in snapshot_results]
            })
            
            # Step 5: Terminate instance
            terminate_result = self.terminate_instance(instance_id)
            decommission_log['terminate_result'] = terminate_result
            decommission_log['steps'].append({
                'step': 'terminate_instance',
                'status': 'completed',
                'timestamp': datetime.now().isoformat()
            })
            
            # Step 6: Clean up associated resources
            cleanup_results = self.cleanup_associated_resources(instance_details)
            decommission_log['cleanup_results'] = cleanup_results
            decommission_log['steps'].append({
                'step': 'cleanup_resources',
                'status': 'completed',
                'timestamp': datetime.now().isoformat()
            })
            
            # Step 7: Validate decommissioning
            validation_result = self.validate_decommissioning(instance_id)
            decommission_log['validation_result'] = validation_result
            decommission_log['steps'].append({
                'step': 'validate_decommissioning',
                'status': 'completed',
                'timestamp': datetime.now().isoformat()
            })
            
            decommission_log['status'] = 'completed'
            decommission_log['end_time'] = datetime.now().isoformat()
            
        except Exception as e:
            decommission_log['status'] = 'failed'
            decommission_log['error'] = str(e)
            decommission_log['end_time'] = datetime.now().isoformat()
            
            # Attempt rollback if possible
            self.attempt_rollback(instance_id, decommission_log)
        
        # Store decommissioning log
        self.store_decommission_log(decommission_log)
        
        return decommission_log
    
    def get_instance_details(self, instance_id):
        """Get comprehensive instance details"""
        
        response = self.ec2.describe_instances(InstanceIds=[instance_id])
        instance = response['Reservations'][0]['Instances'][0]
        
        # Get attached volumes
        volumes = []
        for bdm in instance.get('BlockDeviceMappings', []):
            if 'Ebs' in bdm:
                volumes.append({
                    'volume_id': bdm['Ebs']['VolumeId'],
                    'device_name': bdm['DeviceName'],
                    'delete_on_termination': bdm['Ebs']['DeleteOnTermination']
                })
        
        # Get security groups
        security_groups = [sg['GroupId'] for sg in instance.get('SecurityGroups', [])]
        
        # Get tags
        tags = {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])}
        
        return {
            'instance_id': instance_id,
            'instance_type': instance['InstanceType'],
            'state': instance['State']['Name'],
            'vpc_id': instance.get('VpcId'),
            'subnet_id': instance.get('SubnetId'),
            'security_groups': security_groups,
            'volumes': volumes,
            'tags': tags,
            'launch_time': instance['LaunchTime'].isoformat()
        }
    
    def create_instance_backup(self, instance_id, instance_details):
        """Create backup of instance using AWS Backup"""
        
        try:
            # Create backup job
            backup_job = self.backup.start_backup_job(
                BackupVaultName='default',
                ResourceArn=f'arn:aws:ec2:region:account:instance/{instance_id}',
                IamRoleArn='arn:aws:iam::account:role/AWSBackupDefaultServiceRole',
                IdempotencyToken=f'backup-{instance_id}-{int(time.time())}',
                StartWindowMinutes=60,
                CompleteWindowMinutes=120
            )
            
            return {
                'backup_job_id': backup_job['BackupJobId'],
                'status': 'initiated',
                'creation_date': backup_job['CreationDate'].isoformat()
            }
            
        except Exception as e:
            # Fallback to manual snapshot creation
            return self.create_manual_backup(instance_id, instance_details)
    
    def create_manual_backup(self, instance_id, instance_details):
        """Create manual backup using EBS snapshots"""
        
        snapshots = []
        
        for volume in instance_details['volumes']:
            try:
                snapshot = self.ec2.create_snapshot(
                    VolumeId=volume['volume_id'],
                    Description=f'Backup snapshot for {instance_id} before decommissioning'
                )
                
                # Tag the snapshot
                self.ec2.create_tags(
                    Resources=[snapshot['SnapshotId']],
                    Tags=[
                        {'Key': 'Name', 'Value': f'{instance_id}-backup-{volume["device_name"]}'},
                        {'Key': 'SourceInstance', 'Value': instance_id},
                        {'Key': 'BackupType', 'Value': 'decommissioning'},
                        {'Key': 'CreatedDate', 'Value': datetime.now().strftime('%Y-%m-%d')}
                    ]
                )
                
                snapshots.append({
                    'snapshot_id': snapshot['SnapshotId'],
                    'volume_id': volume['volume_id'],
                    'device_name': volume['device_name']
                })
                
            except Exception as e:
                snapshots.append({
                    'volume_id': volume['volume_id'],
                    'error': str(e)
                })
        
        return {
            'backup_type': 'manual_snapshots',
            'snapshots': snapshots,
            'status': 'completed'
        }
    
    def stop_instance_gracefully(self, instance_id):
        """Stop instance gracefully with proper shutdown"""
        
        try:
            # Stop the instance
            response = self.ec2.stop_instances(
                InstanceIds=[instance_id],
                Force=False  # Graceful shutdown
            )
            
            # Wait for instance to stop
            waiter = self.ec2.get_waiter('instance_stopped')
            waiter.wait(
                InstanceIds=[instance_id],
                WaiterConfig={
                    'Delay': 15,
                    'MaxAttempts': 40  # Wait up to 10 minutes
                }
            )
            
            return {
                'status': 'stopped',
                'stopping_instances': response['StoppingInstances']
            }
            
        except Exception as e:
            return {
                'status': 'failed',
                'error': str(e)
            }
    
    def create_volume_snapshots(self, volumes):
        """Create final snapshots of all volumes"""
        
        snapshot_results = []
        
        for volume in volumes:
            try:
                snapshot = self.ec2.create_snapshot(
                    VolumeId=volume['volume_id'],
                    Description=f'Final snapshot before decommissioning - {volume["device_name"]}'
                )
                
                # Tag the snapshot
                self.ec2.create_tags(
                    Resources=[snapshot['SnapshotId']],
                    Tags=[
                        {'Key': 'Name', 'Value': f'final-snapshot-{volume["volume_id"]}'},
                        {'Key': 'VolumeId', 'Value': volume['volume_id']},
                        {'Key': 'DeviceName', 'Value': volume['device_name']},
                        {'Key': 'SnapshotType', 'Value': 'final_decommissioning'},
                        {'Key': 'CreatedDate', 'Value': datetime.now().strftime('%Y-%m-%d')}
                    ]
                )
                
                snapshot_results.append({
                    'volume_id': volume['volume_id'],
                    'snapshot_id': snapshot['SnapshotId'],
                    'device_name': volume['device_name'],
                    'status': 'created'
                })
                
            except Exception as e:
                snapshot_results.append({
                    'volume_id': volume['volume_id'],
                    'device_name': volume['device_name'],
                    'status': 'failed',
                    'error': str(e)
                })
        
        return snapshot_results
    
    def terminate_instance(self, instance_id):
        """Terminate the instance"""
        
        try:
            response = self.ec2.terminate_instances(InstanceIds=[instance_id])
            
            # Wait for termination
            waiter = self.ec2.get_waiter('instance_terminated')
            waiter.wait(
                InstanceIds=[instance_id],
                WaiterConfig={
                    'Delay': 15,
                    'MaxAttempts': 40
                }
            )
            
            return {
                'status': 'terminated',
                'terminating_instances': response['TerminatingInstances']
            }
            
        except Exception as e:
            return {
                'status': 'failed',
                'error': str(e)
            }
    
    def cleanup_associated_resources(self, instance_details):
        """Clean up resources associated with the instance"""
        
        cleanup_results = {}
        
        # Clean up unused security groups (if not used by other instances)
        cleanup_results['security_groups'] = self.cleanup_security_groups(
            instance_details['security_groups']
        )
        
        # Clean up unused EBS volumes (if not set to delete on termination)
        cleanup_results['volumes'] = self.cleanup_volumes(instance_details['volumes'])
        
        return cleanup_results
    
    def cleanup_security_groups(self, security_group_ids):
        """Clean up unused security groups"""
        
        cleanup_results = []
        
        for sg_id in security_group_ids:
            try:
                # Check if security group is used by other instances
                instances = self.ec2.describe_instances(
                    Filters=[
                        {'Name': 'instance.group-id', 'Values': [sg_id]},
                        {'Name': 'instance-state-name', 'Values': ['running', 'stopped']}
                    ]
                )
                
                if not instances['Reservations']:
                    # Security group is not used, can be deleted
                    # Note: Only delete if it's not the default security group
                    sg_details = self.ec2.describe_security_groups(GroupIds=[sg_id])
                    sg = sg_details['SecurityGroups'][0]
                    
                    if sg['GroupName'] != 'default':
                        self.ec2.delete_security_group(GroupId=sg_id)
                        cleanup_results.append({
                            'security_group_id': sg_id,
                            'status': 'deleted'
                        })
                    else:
                        cleanup_results.append({
                            'security_group_id': sg_id,
                            'status': 'skipped_default'
                        })
                else:
                    cleanup_results.append({
                        'security_group_id': sg_id,
                        'status': 'in_use'
                    })
                    
            except Exception as e:
                cleanup_results.append({
                    'security_group_id': sg_id,
                    'status': 'error',
                    'error': str(e)
                })
        
        return cleanup_results
    
    def cleanup_volumes(self, volumes):
        """Clean up EBS volumes that weren't set to delete on termination"""
        
        cleanup_results = []
        
        for volume in volumes:
            if not volume['delete_on_termination']:
                try:
                    # Check if volume still exists and is available
                    volume_details = self.ec2.describe_volumes(
                        VolumeIds=[volume['volume_id']]
                    )
                    
                    vol = volume_details['Volumes'][0]
                    if vol['State'] == 'available':
                        # Volume is available and can be deleted
                        self.ec2.delete_volume(VolumeId=volume['volume_id'])
                        cleanup_results.append({
                            'volume_id': volume['volume_id'],
                            'status': 'deleted'
                        })
                    else:
                        cleanup_results.append({
                            'volume_id': volume['volume_id'],
                            'status': f'not_available_{vol["State"]}'
                        })
                        
                except Exception as e:
                    cleanup_results.append({
                        'volume_id': volume['volume_id'],
                        'status': 'error',
                        'error': str(e)
                    })
            else:
                cleanup_results.append({
                    'volume_id': volume['volume_id'],
                    'status': 'auto_deleted'
                })
        
        return cleanup_results
    
    def validate_decommissioning(self, instance_id):
        """Validate that decommissioning was successful"""
        
        validation_results = {
            'instance_terminated': False,
            'cost_impact': {},
            'service_impact': {},
            'validation_timestamp': datetime.now().isoformat()
        }
        
        try:
            # Check instance state
            response = self.ec2.describe_instances(InstanceIds=[instance_id])
            instance = response['Reservations'][0]['Instances'][0]
            
            if instance['State']['Name'] == 'terminated':
                validation_results['instance_terminated'] = True
            
            # Estimate cost savings (simplified calculation)
            instance_type = instance['InstanceType']
            validation_results['cost_impact'] = self.estimate_cost_savings(instance_type)
            
            # Check for service impact (simplified)
            validation_results['service_impact'] = self.check_service_impact(instance_id)
            
        except Exception as e:
            validation_results['error'] = str(e)
        
        return validation_results
    
    def store_decommission_log(self, decommission_log):
        """Store decommissioning log for audit and analysis"""
        
        try:
            # Store in S3 for long-term retention
            log_key = f"decommissioning-logs/{decommission_log['instance_id']}/{datetime.now().strftime('%Y/%m/%d')}/decommission-log.json"
            
            self.s3.put_object(
                Bucket='decommissioning-audit-logs',
                Key=log_key,
                Body=json.dumps(decommission_log, indent=2),
                ContentType='application/json'
            )
            
            # Also store in DynamoDB for quick access
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('DecommissioningLogs')
            
            table.put_item(
                Item={
                    'ResourceId': decommission_log['instance_id'],
                    'DecommissionDate': decommission_log['start_time'][:10],
                    'LogData': decommission_log,
                    'Status': decommission_log['status'],
                    'TTL': int((datetime.now() + timedelta(days=2555)).timestamp())
                }
            )
            
        except Exception as e:
            print(f"Error storing decommission log: {str(e)}")
```

### RDS Instance Decommissioning
```python
class RDSDecommissioner:
    def __init__(self):
        self.rds = boto3.client('rds')
        self.s3 = boto3.client('s3')
    
    def decommission_rds_instance(self, db_instance_id, final_snapshot=True):
        """Safely decommission an RDS instance"""
        
        decommission_log = {
            'db_instance_id': db_instance_id,
            'start_time': datetime.now().isoformat(),
            'steps': [],
            'status': 'in_progress'
        }
        
        try:
            # Step 1: Get instance details
            instance_details = self.get_rds_instance_details(db_instance_id)
            decommission_log['instance_details'] = instance_details
            
            # Step 2: Create final backup/snapshot
            if final_snapshot:
                snapshot_result = self.create_final_snapshot(db_instance_id)
                decommission_log['snapshot_result'] = snapshot_result
            
            # Step 3: Export data if required
            export_result = self.export_database_data(db_instance_id, instance_details)
            decommission_log['export_result'] = export_result
            
            # Step 4: Delete instance
            delete_result = self.delete_rds_instance(db_instance_id, final_snapshot)
            decommission_log['delete_result'] = delete_result
            
            # Step 5: Clean up associated resources
            cleanup_result = self.cleanup_rds_resources(instance_details)
            decommission_log['cleanup_result'] = cleanup_result
            
            decommission_log['status'] = 'completed'
            decommission_log['end_time'] = datetime.now().isoformat()
            
        except Exception as e:
            decommission_log['status'] = 'failed'
            decommission_log['error'] = str(e)
            decommission_log['end_time'] = datetime.now().isoformat()
        
        return decommission_log
    
    def create_final_snapshot(self, db_instance_id):
        """Create final snapshot before deletion"""
        
        snapshot_id = f"{db_instance_id}-final-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        try:
            response = self.rds.create_db_snapshot(
                DBSnapshotIdentifier=snapshot_id,
                DBInstanceIdentifier=db_instance_id
            )
            
            # Wait for snapshot completion
            waiter = self.rds.get_waiter('db_snapshot_completed')
            waiter.wait(
                DBSnapshotIdentifier=snapshot_id,
                WaiterConfig={
                    'Delay': 30,
                    'MaxAttempts': 120  # Wait up to 1 hour
                }
            )
            
            return {
                'snapshot_id': snapshot_id,
                'status': 'completed',
                'snapshot_arn': response['DBSnapshot']['DBSnapshotArn']
            }
            
        except Exception as e:
            return {
                'snapshot_id': snapshot_id,
                'status': 'failed',
                'error': str(e)
            }
```

## Common Challenges and Solutions

### Challenge: Service Dependencies During Decommissioning

**Solution**: Implement comprehensive dependency mapping and impact analysis. Use staged decommissioning approaches. Create detailed rollback procedures and test them regularly.

### Challenge: Data Loss Prevention

**Solution**: Implement mandatory backup procedures before decommissioning. Use automated backup validation. Create multiple backup copies and verify accessibility.

### Challenge: Coordinating Complex Decommissioning

**Solution**: Use workflow orchestration tools like Step Functions. Implement automated coordination and monitoring. Create detailed execution plans with checkpoints.

### Challenge: Rollback and Recovery

**Solution**: Design comprehensive rollback procedures for each decommissioning step. Test rollback procedures regularly. Maintain detailed recovery documentation.

### Challenge: Compliance and Audit Requirements

**Solution**: Implement comprehensive audit logging for all decommissioning activities. Create standardized documentation templates. Use automated compliance checking and reporting.

## Related Resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/cost_decommission_resources_decommission.html">AWS Well-Architected Framework - Decommission resources</a></li>
    <li><a href="https://docs.aws.amazon.com/systems-manager/latest/userguide/what-is-systems-manager.html">AWS Systems Manager User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/lambda/latest/dg/welcome.html">AWS Lambda Developer Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html">AWS CloudFormation User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/aws-backup/latest/devguide/whatisbackup.html">AWS Backup Developer Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html">Amazon S3 User Guide</a></li>
    <li><a href="https://aws.amazon.com/blogs/aws-cost-management/">AWS Cost Management Blog</a></li>
    <li><a href="https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html">Amazon CloudWatch User Guide</a></li>
  </ul>
</div>

<style>
.pillar-header {
  background-color: #e8f5e8;
  border-left: 5px solid #2d7d2d;
}

.pillar-header h1 {
  color: #2d7d2d;
}

.aws-service-content h4 {
  color: #2d7d2d;
}

.related-resources {
  background-color: #e8f5e8;
}

.related-resources h2 {
  color: #2d7d2d;
}
</style>
