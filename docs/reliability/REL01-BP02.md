---
title: REL01-BP02 - Manage service quotas across accounts and regions
layout: default
parent: REL01 - How do you manage service quotas and constraints?
grand_parent: Reliability
nav_order: 2
---

<div class="pillar-header">
  <h1>REL01-BP02: Manage service quotas across accounts and regions</h1>
  <p>If you are using multiple AWS accounts or AWS Regions, ensure that you request the appropriate quotas in all environments in which your production workloads run. Consider quotas for disaster recovery, development, and testing.</p>
</div>

## Implementation guidance

Managing service quotas across multiple AWS accounts and regions is critical for ensuring consistent availability and performance of your workloads. Different environments may have varying quota requirements, and some quotas are account-specific or region-specific, requiring coordinated management to prevent service disruptions during normal operations, scaling events, or disaster recovery scenarios.

### Key steps for implementing this best practice:

1. **Establish multi-account and multi-region quota inventory**:
   - Map all AWS accounts and regions used by your organization
   - Document quota requirements for each environment (production, staging, development, DR)
   - Identify shared quotas vs. account-specific and region-specific quotas
   - Create quota dependency maps between accounts and regions
   - Establish quota baseline requirements for each environment type

2. **Implement centralized quota management**:
   - Create a centralized quota management system across accounts and regions
   - Establish quota governance policies and approval workflows
   - Implement automated quota synchronization between environments
   - Create quota templates for different environment types
   - Establish quota change management processes

3. **Design for quota distribution and sharing**:
   - Distribute workloads across multiple accounts to leverage separate quota pools
   - Use multiple regions to access regional quota limits
   - Implement quota pooling strategies for shared resources
   - Design failover mechanisms that consider quota availability
   - Plan for quota requirements during disaster recovery scenarios

4. **Monitor quotas across all environments**:
   - Implement unified quota monitoring across accounts and regions
   - Create consolidated dashboards for multi-account quota visibility
   - Set up cross-account alerting for quota utilization
   - Monitor quota usage patterns across different environments
   - Track quota increase requests and approvals across accounts

5. **Automate quota management workflows**:
   - Implement automated quota provisioning for new accounts and regions
   - Create automated quota increase request workflows
   - Establish quota compliance checking and enforcement
   - Implement quota drift detection and remediation
   - Automate quota reporting and audit processes

6. **Plan for disaster recovery and scaling scenarios**:
   - Ensure disaster recovery regions have adequate quotas
   - Plan for quota requirements during traffic failover
   - Consider quota needs for auto-scaling scenarios
   - Implement quota pre-warming for disaster recovery
   - Test quota availability during disaster recovery exercises

## Implementation examples

### Example 1: Multi-account quota management system

```python
import boto3
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any
import concurrent.futures
import uuid

class MultiAccountQuotaManager:
    def __init__(self):
        self.organizations = boto3.client('organizations')
        self.sts = boto3.client('sts')
        self.dynamodb = boto3.resource('dynamodb')
        self.sns = boto3.client('sns')
        
        # DynamoDB tables
        self.accounts_table = self.dynamodb.Table('OrganizationAccounts')
        self.quotas_table = self.dynamodb.Table('MultiAccountQuotas')
        self.quota_requests_table = self.dynamodb.Table('MultiAccountQuotaRequests')
        
        # Account role configuration
        self.quota_management_role = 'QuotaManagementRole'
        
        # Environment types and their quota requirements
        self.environment_quota_templates = {
            'production': {
                'ec2': {
                    'L-1216C47A': 1000,  # Running On-Demand EC2 instances
                    'L-0263D0A3': 100,   # EC2-VPC Elastic IPs
                },
                'lambda': {
                    'L-B99A9384': 50000,  # Concurrent executions
                },
                'rds': {
                    'L-7B6409FD': 100,  # DB instances
                },
                'priority': 'high'
            },
            'staging': {
                'ec2': {
                    'L-1216C47A': 200,
                    'L-0263D0A3': 20,
                },
                'lambda': {
                    'L-B99A9384': 10000,
                },
                'rds': {
                    'L-7B6409FD': 20,
                },
                'priority': 'medium'
            },
            'development': {
                'ec2': {
                    'L-1216C47A': 50,
                    'L-0263D0A3': 10,
                },
                'lambda': {
                    'L-B99A9384': 5000,
                },
                'rds': {
                    'L-7B6409FD': 10,
                },
                'priority': 'low'
            },
            'disaster_recovery': {
                'ec2': {
                    'L-1216C47A': 1000,  # Same as production for failover
                    'L-0263D0A3': 100,
                },
                'lambda': {
                    'L-B99A9384': 50000,
                },
                'rds': {
                    'L-7B6409FD': 100,
                },
                'priority': 'critical'
            }
        }
    
    def discover_organization_accounts(self) -> List[Dict[str, Any]]:
        """Discover all accounts in the organization"""
        
        accounts = []
        
        try:
            paginator = self.organizations.get_paginator('list_accounts')
            
            for page in paginator.paginate():
                for account in page['Accounts']:
                    if account['Status'] == 'ACTIVE':
                        account_info = {
                            'account_id': account['Id'],
                            'account_name': account['Name'],
                            'email': account['Email'],
                            'status': account['Status'],
                            'joined_timestamp': account['JoinedTimestamp'].isoformat(),
                            'discovered_at': datetime.utcnow().isoformat()
                        }
                        
                        # Try to determine environment type from account name or tags
                        account_info['environment_type'] = self.determine_environment_type(account_info)
                        
                        # Get account regions
                        account_info['regions'] = self.get_account_regions(account['Id'])
                        
                        accounts.append(account_info)
                        
                        # Store account information
                        self.store_account_info(account_info)
        
        except Exception as e:
            print(f"Error discovering organization accounts: {str(e)}")
        
        return accounts
    
    def determine_environment_type(self, account_info: Dict[str, Any]) -> str:
        """Determine environment type based on account name or tags"""
        
        account_name = account_info['account_name'].lower()
        
        if any(keyword in account_name for keyword in ['prod', 'production']):
            return 'production'
        elif any(keyword in account_name for keyword in ['stag', 'staging']):
            return 'staging'
        elif any(keyword in account_name for keyword in ['dev', 'development']):
            return 'development'
        elif any(keyword in account_name for keyword in ['dr', 'disaster', 'recovery']):
            return 'disaster_recovery'
        else:
            return 'unknown'
    
    def get_account_regions(self, account_id: str) -> List[str]:
        """Get regions enabled for an account"""
        
        try:
            # Assume role in target account
            session = self.assume_role_in_account(account_id)
            if not session:
                return []
            
            ec2 = session.client('ec2', region_name='us-east-1')
            
            # Get enabled regions
            response = ec2.describe_regions()
            return [region['RegionName'] for region in response['Regions']]
        
        except Exception as e:
            print(f"Error getting regions for account {account_id}: {str(e)}")
            return []
    
    def assume_role_in_account(self, account_id: str) -> boto3.Session:
        """Assume quota management role in target account"""
        
        try:
            role_arn = f"arn:aws:iam::{account_id}:role/{self.quota_management_role}"
            
            response = self.sts.assume_role(
                RoleArn=role_arn,
                RoleSessionName=f"QuotaManagement-{account_id}",
                DurationSeconds=3600
            )
            
            credentials = response['Credentials']
            
            return boto3.Session(
                aws_access_key_id=credentials['AccessKeyId'],
                aws_secret_access_key=credentials['SecretAccessKey'],
                aws_session_token=credentials['SessionToken']
            )
        
        except Exception as e:
            print(f"Error assuming role in account {account_id}: {str(e)}")
            return None
    
    def get_multi_account_quota_status(self, accounts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get quota status across multiple accounts and regions"""
        
        quota_status = {
            'scan_timestamp': datetime.utcnow().isoformat(),
            'accounts_scanned': 0,
            'regions_scanned': 0,
            'total_quotas_checked': 0,
            'quota_violations': [],
            'quota_gaps': [],
            'account_details': []
        }
        
        # Use thread pool for parallel processing
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            future_to_account = {
                executor.submit(self.scan_account_quotas, account): account 
                for account in accounts
            }
            
            for future in concurrent.futures.as_completed(future_to_account):
                account = future_to_account[future]
                
                try:
                    account_quota_status = future.result()
                    quota_status['account_details'].append(account_quota_status)
                    quota_status['accounts_scanned'] += 1
                    quota_status['regions_scanned'] += len(account_quota_status.get('regions', []))
                    quota_status['total_quotas_checked'] += account_quota_status.get('quotas_checked', 0)
                    
                    # Collect violations and gaps
                    quota_status['quota_violations'].extend(
                        account_quota_status.get('violations', [])
                    )
                    quota_status['quota_gaps'].extend(
                        account_quota_status.get('gaps', [])
                    )
                
                except Exception as e:
                    print(f"Error scanning account {account['account_id']}: {str(e)}")
        
        # Store consolidated results
        self.store_multi_account_quota_status(quota_status)
        
        # Send alerts if violations or gaps found
        if quota_status['quota_violations'] or quota_status['quota_gaps']:
            self.send_multi_account_quota_alert(quota_status)
        
        return quota_status
    
    def scan_account_quotas(self, account: Dict[str, Any]) -> Dict[str, Any]:
        """Scan quotas for a specific account across all its regions"""
        
        account_status = {
            'account_id': account['account_id'],
            'account_name': account['account_name'],
            'environment_type': account['environment_type'],
            'scan_timestamp': datetime.utcnow().isoformat(),
            'regions': [],
            'quotas_checked': 0,
            'violations': [],
            'gaps': []
        }
        
        # Get expected quotas for this environment type
        expected_quotas = self.environment_quota_templates.get(
            account['environment_type'], 
            self.environment_quota_templates['development']
        )
        
        # Scan each region
        for region in account.get('regions', []):
            try:
                region_status = self.scan_region_quotas(account, region, expected_quotas)
                account_status['regions'].append(region_status)
                account_status['quotas_checked'] += region_status.get('quotas_checked', 0)
                
                # Collect violations and gaps
                for violation in region_status.get('violations', []):
                    violation['account_id'] = account['account_id']
                    violation['account_name'] = account['account_name']
                    violation['region'] = region
                    account_status['violations'].append(violation)
                
                for gap in region_status.get('gaps', []):
                    gap['account_id'] = account['account_id']
                    gap['account_name'] = account['account_name']
                    gap['region'] = region
                    account_status['gaps'].append(gap)
            
            except Exception as e:
                print(f"Error scanning region {region} in account {account['account_id']}: {str(e)}")
        
        return account_status
    
    def scan_region_quotas(self, account: Dict[str, Any], region: str, 
                          expected_quotas: Dict[str, Any]) -> Dict[str, Any]:
        """Scan quotas for a specific region in an account"""
        
        region_status = {
            'region': region,
            'scan_timestamp': datetime.utcnow().isoformat(),
            'quotas_checked': 0,
            'violations': [],
            'gaps': []
        }
        
        # Assume role in target account
        session = self.assume_role_in_account(account['account_id'])
        if not session:
            return region_status
        
        try:
            service_quotas = session.client('service-quotas', region_name=region)
            
            # Check each service's quotas
            for service_code, service_quotas_config in expected_quotas.items():
                if service_code == 'priority':
                    continue
                
                for quota_code, expected_value in service_quotas_config.items():
                    try:
                        # Get current quota
                        response = service_quotas.get_service_quota(
                            ServiceCode=service_code,
                            QuotaCode=quota_code
                        )
                        
                        current_quota = response['Quota']['Value']
                        quota_name = response['Quota']['QuotaName']
                        
                        region_status['quotas_checked'] += 1
                        
                        # Check if quota meets expected value
                        if current_quota < expected_value:
                            gap = {
                                'service_code': service_code,
                                'quota_code': quota_code,
                                'quota_name': quota_name,
                                'current_quota': current_quota,
                                'expected_quota': expected_value,
                                'gap_amount': expected_value - current_quota,
                                'severity': self.determine_gap_severity(
                                    account['environment_type'], 
                                    current_quota, 
                                    expected_value
                                )
                            }
                            region_status['gaps'].append(gap)
                        
                        # Get current usage and check for violations
                        usage_info = self.get_quota_usage(
                            session, service_code, quota_code, region
                        )
                        
                        if usage_info['utilization_percentage'] > 80:
                            violation = {
                                'service_code': service_code,
                                'quota_code': quota_code,
                                'quota_name': quota_name,
                                'current_quota': current_quota,
                                'current_usage': usage_info['current_usage'],
                                'utilization_percentage': usage_info['utilization_percentage'],
                                'severity': 'HIGH' if usage_info['utilization_percentage'] > 90 else 'MEDIUM'
                            }
                            region_status['violations'].append(violation)
                    
                    except Exception as e:
                        print(f"Error checking quota {quota_code} in {service_code}: {str(e)}")
        
        except Exception as e:
            print(f"Error scanning region {region}: {str(e)}")
        
        return region_status
    
    def get_quota_usage(self, session: boto3.Session, service_code: str, 
                       quota_code: str, region: str) -> Dict[str, Any]:
        """Get current usage for a quota in a specific region"""
        
        usage_info = {
            'current_usage': 0,
            'utilization_percentage': 0
        }
        
        try:
            # Service-specific usage retrieval
            if service_code == 'ec2':
                usage_info['current_usage'] = self.get_ec2_usage(session, quota_code, region)
            elif service_code == 'lambda':
                usage_info['current_usage'] = self.get_lambda_usage(session, quota_code, region)
            elif service_code == 'rds':
                usage_info['current_usage'] = self.get_rds_usage(session, quota_code, region)
        
        except Exception as e:
            print(f"Error getting usage for {quota_code}: {str(e)}")
        
        return usage_info
    
    def get_ec2_usage(self, session: boto3.Session, quota_code: str, region: str) -> float:
        """Get EC2-specific usage metrics"""
        
        ec2 = session.client('ec2', region_name=region)
        
        if quota_code == 'L-1216C47A':  # Running On-Demand EC2 instances
            response = ec2.describe_instances(
                Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
            )
            return float(len([i for r in response['Reservations'] for i in r['Instances']]))
        elif quota_code == 'L-0263D0A3':  # EC2-VPC Elastic IPs
            response = ec2.describe_addresses()
            return float(len(response['Addresses']))
        
        return 0
    
    def get_lambda_usage(self, session: boto3.Session, quota_code: str, region: str) -> float:
        """Get Lambda-specific usage metrics"""
        
        lambda_client = session.client('lambda', region_name=region)
        
        if quota_code == 'L-B99A9384':  # Concurrent executions
            try:
                response = lambda_client.get_account_settings()
                return float(response.get('AccountUsage', {}).get('FunctionCount', 0))
            except:
                return 0
        
        return 0
    
    def get_rds_usage(self, session: boto3.Session, quota_code: str, region: str) -> float:
        """Get RDS-specific usage metrics"""
        
        rds = session.client('rds', region_name=region)
        
        if quota_code == 'L-7B6409FD':  # DB instances
            response = rds.describe_db_instances()
            return float(len(response['DBInstances']))
        
        return 0
    
    def determine_gap_severity(self, environment_type: str, current_quota: float, 
                              expected_quota: float) -> str:
        """Determine severity of quota gap"""
        
        gap_percentage = ((expected_quota - current_quota) / expected_quota) * 100
        
        if environment_type in ['production', 'disaster_recovery']:
            if gap_percentage > 50:
                return 'CRITICAL'
            elif gap_percentage > 25:
                return 'HIGH'
            else:
                return 'MEDIUM'
        else:
            if gap_percentage > 75:
                return 'HIGH'
            elif gap_percentage > 50:
                return 'MEDIUM'
            else:
                return 'LOW'
    
    def synchronize_quotas_across_accounts(self, source_account_id: str, 
                                         target_accounts: List[str], 
                                         services: List[str]) -> Dict[str, Any]:
        """Synchronize quotas from source account to target accounts"""
        
        sync_result = {
            'sync_timestamp': datetime.utcnow().isoformat(),
            'source_account': source_account_id,
            'target_accounts': target_accounts,
            'services_synced': services,
            'sync_operations': [],
            'successful_syncs': 0,
            'failed_syncs': 0
        }
        
        # Get source account quotas
        source_quotas = self.get_account_quotas(source_account_id, services)
        
        # Synchronize to each target account
        for target_account in target_accounts:
            account_sync = self.sync_account_quotas(
                source_quotas, target_account, services
            )
            sync_result['sync_operations'].append(account_sync)
            
            if account_sync['status'] == 'success':
                sync_result['successful_syncs'] += 1
            else:
                sync_result['failed_syncs'] += 1
        
        # Store sync results
        self.store_sync_results(sync_result)
        
        return sync_result
    
    def get_account_quotas(self, account_id: str, services: List[str]) -> Dict[str, Any]:
        """Get current quotas for an account"""
        
        account_quotas = {}
        session = self.assume_role_in_account(account_id)
        
        if not session:
            return account_quotas
        
        for service_code in services:
            try:
                service_quotas = session.client('service-quotas', region_name='us-east-1')
                
                paginator = service_quotas.get_paginator('list_service_quotas')
                
                service_quota_list = []
                for page in paginator.paginate(ServiceCode=service_code):
                    for quota in page['Quotas']:
                        service_quota_list.append({
                            'quota_code': quota['QuotaCode'],
                            'quota_name': quota['QuotaName'],
                            'quota_value': quota['Value'],
                            'adjustable': quota['Adjustable']
                        })
                
                account_quotas[service_code] = service_quota_list
            
            except Exception as e:
                print(f"Error getting quotas for service {service_code}: {str(e)}")
        
        return account_quotas
    
    def sync_account_quotas(self, source_quotas: Dict[str, Any], 
                           target_account: str, services: List[str]) -> Dict[str, Any]:
        """Sync quotas to a target account"""
        
        sync_operation = {
            'target_account': target_account,
            'sync_timestamp': datetime.utcnow().isoformat(),
            'status': 'success',
            'quota_updates': [],
            'errors': []
        }
        
        session = self.assume_role_in_account(target_account)
        if not session:
            sync_operation['status'] = 'failed'
            sync_operation['errors'].append('Failed to assume role in target account')
            return sync_operation
        
        try:
            service_quotas = session.client('service-quotas', region_name='us-east-1')
            
            for service_code in services:
                if service_code not in source_quotas:
                    continue
                
                for source_quota in source_quotas[service_code]:
                    if not source_quota['adjustable']:
                        continue
                    
                    try:
                        # Get current quota in target account
                        current_quota = service_quotas.get_service_quota(
                            ServiceCode=service_code,
                            QuotaCode=source_quota['quota_code']
                        )
                        
                        current_value = current_quota['Quota']['Value']
                        desired_value = source_quota['quota_value']
                        
                        # Request increase if needed
                        if current_value < desired_value:
                            response = service_quotas.request_service_quota_increase(
                                ServiceCode=service_code,
                                QuotaCode=source_quota['quota_code'],
                                DesiredValue=desired_value
                            )
                            
                            sync_operation['quota_updates'].append({
                                'service_code': service_code,
                                'quota_code': source_quota['quota_code'],
                                'quota_name': source_quota['quota_name'],
                                'current_value': current_value,
                                'desired_value': desired_value,
                                'request_id': response['RequestedQuota']['Id'],
                                'status': 'requested'
                            })
                    
                    except Exception as e:
                        sync_operation['errors'].append(
                            f"Error syncing {source_quota['quota_code']}: {str(e)}"
                        )
        
        except Exception as e:
            sync_operation['status'] = 'failed'
            sync_operation['errors'].append(f"General sync error: {str(e)}")
        
        if sync_operation['errors']:
            sync_operation['status'] = 'partial' if sync_operation['quota_updates'] else 'failed'
        
        return sync_operation
    
    def store_account_info(self, account_info: Dict[str, Any]):
        """Store account information in DynamoDB"""
        
        try:
            self.accounts_table.put_item(Item=account_info)
        except Exception as e:
            print(f"Error storing account info: {str(e)}")
    
    def store_multi_account_quota_status(self, quota_status: Dict[str, Any]):
        """Store multi-account quota status in DynamoDB"""
        
        try:
            item = {
                'scan_id': str(uuid.uuid4()),
                'scan_timestamp': quota_status['scan_timestamp'],
                'accounts_scanned': quota_status['accounts_scanned'],
                'regions_scanned': quota_status['regions_scanned'],
                'total_quotas_checked': quota_status['total_quotas_checked'],
                'violations_count': len(quota_status['quota_violations']),
                'gaps_count': len(quota_status['quota_gaps']),
                'account_details': quota_status['account_details'],
                'ttl': int((datetime.utcnow() + timedelta(days=90)).timestamp())
            }
            
            self.quotas_table.put_item(Item=item)
        except Exception as e:
            print(f"Error storing quota status: {str(e)}")
    
    def store_sync_results(self, sync_result: Dict[str, Any]):
        """Store quota synchronization results"""
        
        try:
            item = {
                'sync_id': str(uuid.uuid4()),
                'sync_timestamp': sync_result['sync_timestamp'],
                'source_account': sync_result['source_account'],
                'target_accounts': sync_result['target_accounts'],
                'successful_syncs': sync_result['successful_syncs'],
                'failed_syncs': sync_result['failed_syncs'],
                'sync_operations': sync_result['sync_operations'],
                'ttl': int((datetime.utcnow() + timedelta(days=30)).timestamp())
            }
            
            self.quota_requests_table.put_item(Item=item)
        except Exception as e:
            print(f"Error storing sync results: {str(e)}")
    
    def send_multi_account_quota_alert(self, quota_status: Dict[str, Any]):
        """Send alert for multi-account quota issues"""
        
        try:
            message = {
                'alert_type': 'MULTI_ACCOUNT_QUOTA_ALERT',
                'scan_timestamp': quota_status['scan_timestamp'],
                'accounts_scanned': quota_status['accounts_scanned'],
                'regions_scanned': quota_status['regions_scanned'],
                'violations_count': len(quota_status['quota_violations']),
                'gaps_count': len(quota_status['quota_gaps']),
                'critical_violations': [
                    v for v in quota_status['quota_violations'] 
                    if v.get('severity') == 'HIGH'
                ],
                'critical_gaps': [
                    g for g in quota_status['quota_gaps'] 
                    if g.get('severity') in ['CRITICAL', 'HIGH']
                ]
            }
            
            self.sns.publish(
                TopicArn='arn:aws:sns:us-west-2:123456789012:MultiAccountQuotaAlerts',
                Subject=f"Multi-Account Quota Issues Detected: {len(quota_status['quota_violations'])} violations, {len(quota_status['quota_gaps'])} gaps",
                Message=json.dumps(message, indent=2)
            )
        
        except Exception as e:
            print(f"Error sending multi-account quota alert: {str(e)}")

def lambda_handler(event, context):
    """Lambda function for multi-account quota management"""
    
    quota_manager = MultiAccountQuotaManager()
    
    action = event.get('action', 'scan_quotas')
    
    if action == 'discover_accounts':
        result = quota_manager.discover_organization_accounts()
    elif action == 'scan_quotas':
        accounts = event.get('accounts', [])
        if not accounts:
            accounts = quota_manager.discover_organization_accounts()
        result = quota_manager.get_multi_account_quota_status(accounts)
    elif action == 'sync_quotas':
        result = quota_manager.synchronize_quotas_across_accounts(
            event['source_account'],
            event['target_accounts'],
            event['services']
        )
    else:
        result = {'error': 'Invalid action specified'}
    
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
```
### Example 2: Cross-region quota coordination system

```python
import boto3
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any
import concurrent.futures
import uuid

class CrossRegionQuotaCoordinator:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.sns = boto3.client('sns')
        
        # DynamoDB tables
        self.region_quotas_table = self.dynamodb.Table('CrossRegionQuotas')
        self.failover_plans_table = self.dynamodb.Table('FailoverPlans')
        
        # Primary regions and their disaster recovery pairs
        self.region_pairs = {
            'us-east-1': 'us-west-2',
            'us-west-2': 'us-east-1',
            'eu-west-1': 'eu-central-1',
            'eu-central-1': 'eu-west-1',
            'ap-southeast-1': 'ap-northeast-1',
            'ap-northeast-1': 'ap-southeast-1'
        }
        
        # Critical services that need quota coordination
        self.critical_services = {
            'ec2': {
                'L-1216C47A': 'Running On-Demand EC2 instances',
                'L-34B43A08': 'All Standard Spot Instance Requests',
                'L-0263D0A3': 'EC2-VPC Elastic IPs'
            },
            'lambda': {
                'L-B99A9384': 'Concurrent executions'
            },
            'rds': {
                'L-7B6409FD': 'DB instances',
                'L-952B80B8': 'DB clusters'
            },
            'elasticloadbalancing': {
                'L-53EA6B1F': 'Application Load Balancers per Region',
                'L-E9E9831D': 'Network Load Balancers per Region'
            }
        }
    
    def analyze_cross_region_quota_requirements(self, workload_config: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze quota requirements across regions for a workload"""
        
        analysis = {
            'workload_id': workload_config['workload_id'],
            'workload_name': workload_config['workload_name'],
            'analysis_timestamp': datetime.utcnow().isoformat(),
            'primary_region': workload_config['primary_region'],
            'dr_region': workload_config.get('dr_region', self.region_pairs.get(workload_config['primary_region'])),
            'additional_regions': workload_config.get('additional_regions', []),
            'quota_requirements': {},
            'failover_capacity_needs': {},
            'quota_gaps': [],
            'recommendations': []
        }
        
        # Calculate quota requirements for each region
        all_regions = [analysis['primary_region']]
        if analysis['dr_region']:
            all_regions.append(analysis['dr_region'])
        all_regions.extend(analysis['additional_regions'])
        
        for region in all_regions:
            region_requirements = self.calculate_region_quota_requirements(
                workload_config, region, analysis['primary_region']
            )
            analysis['quota_requirements'][region] = region_requirements
        
        # Analyze failover capacity needs
        if analysis['dr_region']:
            analysis['failover_capacity_needs'] = self.calculate_failover_capacity_needs(
                workload_config, analysis['primary_region'], analysis['dr_region']
            )
        
        # Check current quotas against requirements
        analysis['quota_gaps'] = self.identify_quota_gaps(analysis)
        
        # Generate recommendations
        analysis['recommendations'] = self.generate_cross_region_recommendations(analysis)
        
        # Store analysis results
        self.store_cross_region_analysis(analysis)
        
        return analysis
    
    def calculate_region_quota_requirements(self, workload_config: Dict[str, Any], 
                                          region: str, primary_region: str) -> Dict[str, Any]:
        """Calculate quota requirements for a specific region"""
        
        requirements = {
            'region': region,
            'region_type': 'primary' if region == primary_region else 'secondary',
            'service_requirements': {}
        }
        
        # Base requirements from workload configuration
        base_requirements = workload_config.get('resource_requirements', {})
        
        # Calculate requirements based on region type
        for service_code, service_requirements in base_requirements.items():
            if service_code not in self.critical_services:
                continue
            
            service_quotas = {}
            
            for quota_code, base_requirement in service_requirements.items():
                if quota_code not in self.critical_services[service_code]:
                    continue
                
                # Adjust requirements based on region type and scaling factors
                if requirements['region_type'] == 'primary':
                    # Primary region needs full capacity plus growth buffer
                    required_quota = int(base_requirement * 1.5)  # 50% buffer
                elif region == self.region_pairs.get(primary_region):
                    # DR region needs full failover capacity
                    required_quota = int(base_requirement * 1.2)  # 20% buffer for failover
                else:
                    # Additional regions need partial capacity
                    required_quota = int(base_requirement * 0.5)  # 50% of primary
                
                service_quotas[quota_code] = {
                    'quota_name': self.critical_services[service_code][quota_code],
                    'required_quota': required_quota,
                    'base_requirement': base_requirement,
                    'scaling_factor': required_quota / base_requirement if base_requirement > 0 else 1
                }
            
            requirements['service_requirements'][service_code] = service_quotas
        
        return requirements
    
    def calculate_failover_capacity_needs(self, workload_config: Dict[str, Any], 
                                        primary_region: str, dr_region: str) -> Dict[str, Any]:
        """Calculate capacity needs for disaster recovery failover"""
        
        failover_needs = {
            'primary_region': primary_region,
            'dr_region': dr_region,
            'failover_type': workload_config.get('failover_type', 'warm_standby'),
            'rto_requirement': workload_config.get('rto_minutes', 60),
            'rpo_requirement': workload_config.get('rpo_minutes', 15),
            'capacity_requirements': {}
        }
        
        # Calculate capacity based on failover type
        failover_multipliers = {
            'hot_standby': 1.0,    # 100% capacity ready
            'warm_standby': 0.5,   # 50% capacity, scale up on failover
            'cold_standby': 0.1    # 10% capacity, full provisioning on failover
        }
        
        multiplier = failover_multipliers.get(failover_needs['failover_type'], 0.5)
        
        base_requirements = workload_config.get('resource_requirements', {})
        
        for service_code, service_requirements in base_requirements.items():
            if service_code not in self.critical_services:
                continue
            
            service_capacity = {}
            
            for quota_code, base_requirement in service_requirements.items():
                if quota_code not in self.critical_services[service_code]:
                    continue
                
                # Calculate immediate failover capacity
                immediate_capacity = int(base_requirement * multiplier)
                
                # Calculate full failover capacity (what we need to scale to)
                full_capacity = int(base_requirement * 1.1)  # 10% buffer
                
                service_capacity[quota_code] = {
                    'quota_name': self.critical_services[service_code][quota_code],
                    'immediate_capacity': immediate_capacity,
                    'full_capacity': full_capacity,
                    'scale_up_needed': full_capacity - immediate_capacity
                }
            
            failover_needs['capacity_requirements'][service_code] = service_capacity
        
        return failover_needs
    
    def identify_quota_gaps(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify gaps between required and current quotas"""
        
        gaps = []
        
        for region, requirements in analysis['quota_requirements'].items():
            # Get current quotas for the region
            current_quotas = self.get_current_region_quotas(region)
            
            for service_code, service_requirements in requirements['service_requirements'].items():
                for quota_code, quota_requirement in service_requirements.items():
                    current_quota = current_quotas.get(service_code, {}).get(quota_code, {}).get('value', 0)
                    required_quota = quota_requirement['required_quota']
                    
                    if current_quota < required_quota:
                        gap = {
                            'region': region,
                            'region_type': requirements['region_type'],
                            'service_code': service_code,
                            'quota_code': quota_code,
                            'quota_name': quota_requirement['quota_name'],
                            'current_quota': current_quota,
                            'required_quota': required_quota,
                            'gap_amount': required_quota - current_quota,
                            'gap_percentage': ((required_quota - current_quota) / required_quota * 100) if required_quota > 0 else 0,
                            'priority': self.determine_gap_priority(requirements['region_type'], quota_requirement),
                            'adjustable': current_quotas.get(service_code, {}).get(quota_code, {}).get('adjustable', True)
                        }
                        gaps.append(gap)
        
        return gaps
    
    def get_current_region_quotas(self, region: str) -> Dict[str, Any]:
        """Get current quotas for a specific region"""
        
        current_quotas = {}
        
        try:
            service_quotas = boto3.client('service-quotas', region_name=region)
            
            for service_code in self.critical_services.keys():
                service_quotas_dict = {}
                
                for quota_code in self.critical_services[service_code].keys():
                    try:
                        response = service_quotas.get_service_quota(
                            ServiceCode=service_code,
                            QuotaCode=quota_code
                        )
                        
                        service_quotas_dict[quota_code] = {
                            'value': response['Quota']['Value'],
                            'adjustable': response['Quota']['Adjustable'],
                            'quota_name': response['Quota']['QuotaName']
                        }
                    
                    except Exception as e:
                        print(f"Error getting quota {quota_code} for {service_code} in {region}: {str(e)}")
                
                current_quotas[service_code] = service_quotas_dict
        
        except Exception as e:
            print(f"Error getting quotas for region {region}: {str(e)}")
        
        return current_quotas
    
    def determine_gap_priority(self, region_type: str, quota_requirement: Dict[str, Any]) -> str:
        """Determine priority of quota gap"""
        
        gap_percentage = quota_requirement.get('gap_percentage', 0)
        
        if region_type == 'primary':
            if gap_percentage > 50:
                return 'CRITICAL'
            elif gap_percentage > 25:
                return 'HIGH'
            else:
                return 'MEDIUM'
        else:  # secondary regions
            if gap_percentage > 75:
                return 'HIGH'
            elif gap_percentage > 50:
                return 'MEDIUM'
            else:
                return 'LOW'
    
    def generate_cross_region_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate recommendations for cross-region quota management"""
        
        recommendations = []
        
        # Analyze quota gaps
        critical_gaps = [g for g in analysis['quota_gaps'] if g['priority'] == 'CRITICAL']
        high_gaps = [g for g in analysis['quota_gaps'] if g['priority'] == 'HIGH']
        
        if critical_gaps:
            recommendations.append(
                f"URGENT: Submit quota increase requests for {len(critical_gaps)} critical gaps in primary regions"
            )
            
            for gap in critical_gaps[:3]:  # Top 3 critical gaps
                recommendations.append(
                    f"• Increase {gap['quota_name']} in {gap['region']} from {gap['current_quota']} to {gap['required_quota']}"
                )
        
        if high_gaps:
            recommendations.append(
                f"Submit quota increase requests for {len(high_gaps)} high-priority gaps"
            )
        
        # Failover capacity recommendations
        if 'failover_capacity_needs' in analysis:
            failover_needs = analysis['failover_capacity_needs']
            
            if failover_needs['failover_type'] == 'cold_standby':
                recommendations.append(
                    "Consider upgrading to warm standby for faster failover given current RTO requirements"
                )
            
            recommendations.append(
                f"Pre-warm disaster recovery capacity in {failover_needs['dr_region']} for RTO of {failover_needs['rto_requirement']} minutes"
            )
        
        # Regional distribution recommendations
        regions_with_gaps = set(g['region'] for g in analysis['quota_gaps'])
        if len(regions_with_gaps) > 1:
            recommendations.append(
                "Consider redistributing workload across regions to better utilize available quotas"
            )
        
        # Monitoring recommendations
        recommendations.append(
            "Implement cross-region quota monitoring with automated alerting"
        )
        recommendations.append(
            "Establish quota increase request automation for disaster recovery scenarios"
        )
        
        return recommendations
    
    def create_failover_plan(self, workload_config: Dict[str, Any], 
                           analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Create a detailed failover plan with quota considerations"""
        
        plan_id = str(uuid.uuid4())
        
        failover_plan = {
            'plan_id': plan_id,
            'workload_id': workload_config['workload_id'],
            'workload_name': workload_config['workload_name'],
            'created_timestamp': datetime.utcnow().isoformat(),
            'primary_region': analysis['primary_region'],
            'dr_region': analysis['dr_region'],
            'failover_type': workload_config.get('failover_type', 'warm_standby'),
            'rto_target': workload_config.get('rto_minutes', 60),
            'rpo_target': workload_config.get('rpo_minutes', 15),
            'quota_prerequisites': [],
            'failover_steps': [],
            'rollback_steps': [],
            'validation_checks': []
        }
        
        # Define quota prerequisites
        if 'failover_capacity_needs' in analysis:
            capacity_needs = analysis['failover_capacity_needs']
            
            for service_code, service_capacity in capacity_needs['capacity_requirements'].items():
                for quota_code, quota_capacity in service_capacity.items():
                    prerequisite = {
                        'service_code': service_code,
                        'quota_code': quota_code,
                        'quota_name': quota_capacity['quota_name'],
                        'required_quota': quota_capacity['full_capacity'],
                        'immediate_capacity': quota_capacity['immediate_capacity'],
                        'scale_up_needed': quota_capacity['scale_up_needed']
                    }
                    failover_plan['quota_prerequisites'].append(prerequisite)
        
        # Define failover steps
        failover_plan['failover_steps'] = [
            {
                'step': 1,
                'action': 'Validate DR region quota availability',
                'description': 'Verify sufficient quotas are available in DR region',
                'estimated_time_minutes': 2,
                'automation_possible': True
            },
            {
                'step': 2,
                'action': 'Scale up DR region resources',
                'description': 'Scale DR resources to handle production traffic',
                'estimated_time_minutes': 10,
                'automation_possible': True,
                'quota_impact': 'Consumes reserved DR quotas'
            },
            {
                'step': 3,
                'action': 'Update DNS routing',
                'description': 'Route traffic from primary to DR region',
                'estimated_time_minutes': 5,
                'automation_possible': True
            },
            {
                'step': 4,
                'action': 'Validate application functionality',
                'description': 'Verify application is working correctly in DR region',
                'estimated_time_minutes': 10,
                'automation_possible': False
            }
        ]
        
        # Define rollback steps
        failover_plan['rollback_steps'] = [
            {
                'step': 1,
                'action': 'Restore primary region services',
                'description': 'Bring primary region back online',
                'estimated_time_minutes': 15,
                'quota_impact': 'Requires primary region quotas'
            },
            {
                'step': 2,
                'action': 'Synchronize data',
                'description': 'Sync data from DR back to primary',
                'estimated_time_minutes': 30,
                'automation_possible': True
            },
            {
                'step': 3,
                'action': 'Switch traffic back to primary',
                'description': 'Route traffic back to primary region',
                'estimated_time_minutes': 5,
                'automation_possible': True
            },
            {
                'step': 4,
                'action': 'Scale down DR resources',
                'description': 'Return DR to standby capacity',
                'estimated_time_minutes': 10,
                'automation_possible': True,
                'quota_impact': 'Releases DR quotas'
            }
        ]
        
        # Define validation checks
        failover_plan['validation_checks'] = [
            {
                'check': 'Quota availability validation',
                'description': 'Verify sufficient quotas in both regions',
                'frequency': 'daily',
                'automation_possible': True
            },
            {
                'check': 'Failover capacity test',
                'description': 'Test scaling to full capacity in DR region',
                'frequency': 'monthly',
                'automation_possible': True
            },
            {
                'check': 'End-to-end failover test',
                'description': 'Complete failover and rollback test',
                'frequency': 'quarterly',
                'automation_possible': False
            }
        ]
        
        # Store failover plan
        self.store_failover_plan(failover_plan)
        
        return failover_plan
    
    def monitor_cross_region_quota_health(self, workload_ids: List[str]) -> Dict[str, Any]:
        """Monitor quota health across regions for multiple workloads"""
        
        health_report = {
            'monitoring_timestamp': datetime.utcnow().isoformat(),
            'workloads_monitored': len(workload_ids),
            'overall_health': 'HEALTHY',
            'workload_health': [],
            'regional_issues': [],
            'recommendations': []
        }
        
        for workload_id in workload_ids:
            workload_health = self.check_workload_quota_health(workload_id)
            health_report['workload_health'].append(workload_health)
            
            # Collect regional issues
            for issue in workload_health.get('issues', []):
                if issue not in health_report['regional_issues']:
                    health_report['regional_issues'].append(issue)
        
        # Determine overall health
        unhealthy_workloads = [w for w in health_report['workload_health'] if w['health_status'] != 'HEALTHY']
        
        if len(unhealthy_workloads) > len(workload_ids) * 0.5:
            health_report['overall_health'] = 'UNHEALTHY'
        elif len(unhealthy_workloads) > 0:
            health_report['overall_health'] = 'DEGRADED'
        
        # Generate recommendations
        health_report['recommendations'] = self.generate_health_recommendations(health_report)
        
        # Send alerts if needed
        if health_report['overall_health'] != 'HEALTHY':
            self.send_cross_region_health_alert(health_report)
        
        return health_report
    
    def check_workload_quota_health(self, workload_id: str) -> Dict[str, Any]:
        """Check quota health for a specific workload"""
        
        workload_health = {
            'workload_id': workload_id,
            'health_status': 'HEALTHY',
            'issues': [],
            'regions_checked': [],
            'quota_utilization': {}
        }
        
        # Get workload configuration and analysis
        # This would typically come from a configuration store
        # For this example, we'll use a simplified approach
        
        try:
            # Get stored analysis for the workload
            response = self.region_quotas_table.query(
                KeyConditionExpression='workload_id = :workload_id',
                ExpressionAttributeValues={':workload_id': workload_id},
                ScanIndexForward=False,
                Limit=1
            )
            
            if not response['Items']:
                workload_health['health_status'] = 'UNKNOWN'
                workload_health['issues'].append('No quota analysis found for workload')
                return workload_health
            
            analysis = response['Items'][0]
            
            # Check quota health for each region
            for region, requirements in analysis.get('quota_requirements', {}).items():
                region_health = self.check_region_quota_health(region, requirements)
                workload_health['regions_checked'].append(region)
                workload_health['quota_utilization'][region] = region_health
                
                if region_health['health_status'] != 'HEALTHY':
                    workload_health['health_status'] = 'DEGRADED'
                    workload_health['issues'].extend(region_health['issues'])
        
        except Exception as e:
            workload_health['health_status'] = 'ERROR'
            workload_health['issues'].append(f"Error checking workload health: {str(e)}")
        
        return workload_health
    
    def check_region_quota_health(self, region: str, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Check quota health for a specific region"""
        
        region_health = {
            'region': region,
            'health_status': 'HEALTHY',
            'issues': [],
            'quota_checks': []
        }
        
        try:
            current_quotas = self.get_current_region_quotas(region)
            
            for service_code, service_requirements in requirements.get('service_requirements', {}).items():
                for quota_code, quota_requirement in service_requirements.items():
                    current_quota = current_quotas.get(service_code, {}).get(quota_code, {}).get('value', 0)
                    required_quota = quota_requirement['required_quota']
                    
                    # Get current usage
                    current_usage = self.get_quota_usage_for_region(region, service_code, quota_code)
                    utilization = (current_usage / current_quota * 100) if current_quota > 0 else 0
                    
                    quota_check = {
                        'service_code': service_code,
                        'quota_code': quota_code,
                        'quota_name': quota_requirement['quota_name'],
                        'current_quota': current_quota,
                        'required_quota': required_quota,
                        'current_usage': current_usage,
                        'utilization_percentage': utilization,
                        'health_status': 'HEALTHY'
                    }
                    
                    # Determine health status
                    if current_quota < required_quota:
                        quota_check['health_status'] = 'INSUFFICIENT_QUOTA'
                        region_health['health_status'] = 'DEGRADED'
                        region_health['issues'].append(
                            f"Insufficient quota for {quota_requirement['quota_name']} in {region}"
                        )
                    elif utilization > 80:
                        quota_check['health_status'] = 'HIGH_UTILIZATION'
                        region_health['health_status'] = 'DEGRADED'
                        region_health['issues'].append(
                            f"High utilization ({utilization:.1f}%) for {quota_requirement['quota_name']} in {region}"
                        )
                    
                    region_health['quota_checks'].append(quota_check)
        
        except Exception as e:
            region_health['health_status'] = 'ERROR'
            region_health['issues'].append(f"Error checking region health: {str(e)}")
        
        return region_health
    
    def get_quota_usage_for_region(self, region: str, service_code: str, quota_code: str) -> float:
        """Get current quota usage for a specific region and quota"""
        
        # This would implement service-specific usage retrieval
        # For brevity, returning a placeholder value
        return 0.0
    
    def generate_health_recommendations(self, health_report: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on health report"""
        
        recommendations = []
        
        if health_report['overall_health'] == 'UNHEALTHY':
            recommendations.append("URGENT: Multiple workloads have quota health issues requiring immediate attention")
        
        # Analyze common issues
        issue_counts = {}
        for workload in health_report['workload_health']:
            for issue in workload.get('issues', []):
                issue_counts[issue] = issue_counts.get(issue, 0) + 1
        
        # Recommend actions for common issues
        for issue, count in issue_counts.items():
            if count > 1:
                recommendations.append(f"Address common issue affecting {count} workloads: {issue}")
        
        return recommendations
    
    def store_cross_region_analysis(self, analysis: Dict[str, Any]):
        """Store cross-region analysis results"""
        
        try:
            item = {
                'workload_id': analysis['workload_id'],
                'analysis_timestamp': analysis['analysis_timestamp'],
                'analysis_data': analysis,
                'ttl': int((datetime.utcnow() + timedelta(days=30)).timestamp())
            }
            
            self.region_quotas_table.put_item(Item=item)
        except Exception as e:
            print(f"Error storing cross-region analysis: {str(e)}")
    
    def store_failover_plan(self, failover_plan: Dict[str, Any]):
        """Store failover plan"""
        
        try:
            self.failover_plans_table.put_item(Item=failover_plan)
        except Exception as e:
            print(f"Error storing failover plan: {str(e)}")
    
    def send_cross_region_health_alert(self, health_report: Dict[str, Any]):
        """Send alert for cross-region health issues"""
        
        try:
            message = {
                'alert_type': 'CROSS_REGION_QUOTA_HEALTH',
                'overall_health': health_report['overall_health'],
                'workloads_affected': len([w for w in health_report['workload_health'] if w['health_status'] != 'HEALTHY']),
                'regional_issues': health_report['regional_issues'],
                'recommendations': health_report['recommendations']
            }
            
            self.sns.publish(
                TopicArn='arn:aws:sns:us-west-2:123456789012:CrossRegionQuotaHealth',
                Subject=f"Cross-Region Quota Health Alert: {health_report['overall_health']}",
                Message=json.dumps(message, indent=2)
            )
        except Exception as e:
            print(f"Error sending cross-region health alert: {str(e)}")

def lambda_handler(event, context):
    """Lambda function for cross-region quota coordination"""
    
    coordinator = CrossRegionQuotaCoordinator()
    
    action = event.get('action', 'analyze_requirements')
    
    if action == 'analyze_requirements':
        result = coordinator.analyze_cross_region_quota_requirements(event['workload_config'])
    elif action == 'create_failover_plan':
        workload_config = event['workload_config']
        analysis = event['analysis']
        result = coordinator.create_failover_plan(workload_config, analysis)
    elif action == 'monitor_health':
        result = coordinator.monitor_cross_region_quota_health(event['workload_ids'])
    else:
        result = {'error': 'Invalid action specified'}
    
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
```
### Example 3: AWS Organizations-based quota governance

```yaml
# cloudformation/multi-account-quota-governance.yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Multi-Account Quota Governance Infrastructure'

Parameters:
  OrganizationId:
    Type: String
    Description: AWS Organizations ID
  
  ManagementAccountId:
    Type: String
    Description: Management account ID
  
  NotificationEmail:
    Type: String
    Description: Email for quota governance notifications
    Default: quota-admin@company.com

Resources:
  # Cross-account role for quota management
  QuotaManagementRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: QuotaManagementRole
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              AWS: !Sub 'arn:aws:iam::${ManagementAccountId}:root'
            Action: sts:AssumeRole
            Condition:
              StringEquals:
                'aws:PrincipalOrgID': !Ref OrganizationId
          - Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
      Policies:
        - PolicyName: QuotaManagementPolicy
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
                  - elasticloadbalancing:Describe*
                Resource: '*'
              - Effect: Allow
                Action:
                  - organizations:ListAccounts
                  - organizations:DescribeAccount
                  - organizations:ListTagsForResource
                Resource: '*'

  # DynamoDB tables for quota governance
  OrganizationAccountsTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: OrganizationAccounts
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: account_id
          AttributeType: S
        - AttributeName: environment_type
          AttributeType: S
      KeySchema:
        - AttributeName: account_id
          KeyType: HASH
      GlobalSecondaryIndexes:
        - IndexName: EnvironmentTypeIndex
          KeySchema:
            - AttributeName: environment_type
              KeyType: HASH
          Projection:
            ProjectionType: ALL
      PointInTimeRecoverySpecification:
        PointInTimeRecoveryEnabled: true
      Tags:
        - Key: Purpose
          Value: QuotaGovernance
        - Key: Component
          Value: AccountManagement

  MultiAccountQuotasTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: MultiAccountQuotas
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: scan_id
          AttributeType: S
        - AttributeName: scan_timestamp
          AttributeType: S
      KeySchema:
        - AttributeName: scan_id
          KeyType: HASH
      TimeToLiveSpecification:
        AttributeName: ttl
        Enabled: true
      Tags:
        - Key: Purpose
          Value: QuotaGovernance
        - Key: Component
          Value: QuotaTracking

  MultiAccountQuotaRequestsTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: MultiAccountQuotaRequests
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: sync_id
          AttributeType: S
        - AttributeName: sync_timestamp
          AttributeType: S
      KeySchema:
        - AttributeName: sync_id
          KeyType: HASH
      TimeToLiveSpecification:
        AttributeName: ttl
        Enabled: true
      Tags:
        - Key: Purpose
          Value: QuotaGovernance
        - Key: Component
          Value: RequestTracking

  CrossRegionQuotasTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: CrossRegionQuotas
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: workload_id
          AttributeType: S
        - AttributeName: analysis_timestamp
          AttributeType: S
      KeySchema:
        - AttributeName: workload_id
          KeyType: HASH
        - AttributeName: analysis_timestamp
          KeyType: RANGE
      TimeToLiveSpecification:
        AttributeName: ttl
        Enabled: true
      Tags:
        - Key: Purpose
          Value: QuotaGovernance
        - Key: Component
          Value: CrossRegionAnalysis

  FailoverPlansTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: FailoverPlans
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: plan_id
          AttributeType: S
        - AttributeName: workload_id
          AttributeType: S
      KeySchema:
        - AttributeName: plan_id
          KeyType: HASH
      GlobalSecondaryIndexes:
        - IndexName: WorkloadIdIndex
          KeySchema:
            - AttributeName: workload_id
              KeyType: HASH
          Projection:
            ProjectionType: ALL
      Tags:
        - Key: Purpose
          Value: QuotaGovernance
        - Key: Component
          Value: FailoverPlanning

  # SNS Topics for notifications
  MultiAccountQuotaAlertsTopicPolicy:
    Type: AWS::SNS::TopicPolicy
    Properties:
      Topics:
        - !Ref MultiAccountQuotaAlertsTopic
      PolicyDocument:
        Statement:
          - Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action: sns:Publish
            Resource: !Ref MultiAccountQuotaAlertsTopic

  MultiAccountQuotaAlertsTopic:
    Type: AWS::SNS::Topic
    Properties:
      TopicName: MultiAccountQuotaAlerts
      DisplayName: Multi-Account Quota Alerts
      KmsMasterKeyId: alias/aws/sns

  MultiAccountQuotaAlertsSubscription:
    Type: AWS::SNS::Subscription
    Properties:
      Protocol: email
      TopicArn: !Ref MultiAccountQuotaAlertsTopic
      Endpoint: !Ref NotificationEmail

  CrossRegionQuotaHealthTopic:
    Type: AWS::SNS::Topic
    Properties:
      TopicName: CrossRegionQuotaHealth
      DisplayName: Cross-Region Quota Health Alerts
      KmsMasterKeyId: alias/aws/sns

  CrossRegionQuotaHealthSubscription:
    Type: AWS::SNS::Subscription
    Properties:
      Protocol: email
      TopicArn: !Ref CrossRegionQuotaHealthTopic
      Endpoint: !Ref NotificationEmail

  # Lambda functions
  MultiAccountQuotaManagerFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: multi-account-quota-manager
      Runtime: python3.9
      Handler: lambda_function.lambda_handler
      Role: !GetAtt MultiAccountQuotaManagerRole.Arn
      Timeout: 900
      MemorySize: 1024
      Environment:
        Variables:
          ACCOUNTS_TABLE_NAME: !Ref OrganizationAccountsTable
          QUOTAS_TABLE_NAME: !Ref MultiAccountQuotasTable
          REQUESTS_TABLE_NAME: !Ref MultiAccountQuotaRequestsTable
          ALERT_TOPIC_ARN: !Ref MultiAccountQuotaAlertsTopic
          ORGANIZATION_ID: !Ref OrganizationId
          QUOTA_MANAGEMENT_ROLE: !Ref QuotaManagementRole
      Code:
        ZipFile: |
          import json
          import boto3
          import os
          from datetime import datetime
          
          def lambda_handler(event, context):
              print("Multi-account quota manager function executed")
              
              return {
                  'statusCode': 200,
                  'body': json.dumps('Multi-account quota management completed')
              }

  CrossRegionQuotaCoordinatorFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: cross-region-quota-coordinator
      Runtime: python3.9
      Handler: lambda_function.lambda_handler
      Role: !GetAtt CrossRegionQuotaCoordinatorRole.Arn
      Timeout: 600
      MemorySize: 512
      Environment:
        Variables:
          REGION_QUOTAS_TABLE_NAME: !Ref CrossRegionQuotasTable
          FAILOVER_PLANS_TABLE_NAME: !Ref FailoverPlansTable
          HEALTH_ALERT_TOPIC_ARN: !Ref CrossRegionQuotaHealthTopic
      Code:
        ZipFile: |
          import json
          import boto3
          import os
          from datetime import datetime
          
          def lambda_handler(event, context):
              print("Cross-region quota coordinator function executed")
              
              return {
                  'statusCode': 200,
                  'body': json.dumps('Cross-region quota coordination completed')
              }

  # IAM roles for Lambda functions
  MultiAccountQuotaManagerRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: MultiAccountQuotaManagerRole
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
        - PolicyName: MultiAccountQuotaManagerPolicy
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - organizations:ListAccounts
                  - organizations:DescribeAccount
                  - organizations:ListTagsForResource
                Resource: '*'
              - Effect: Allow
                Action:
                  - sts:AssumeRole
                Resource: !Sub 'arn:aws:iam::*:role/${QuotaManagementRole}'
                Condition:
                  StringEquals:
                    'aws:PrincipalOrgID': !Ref OrganizationId
              - Effect: Allow
                Action:
                  - dynamodb:GetItem
                  - dynamodb:PutItem
                  - dynamodb:Query
                  - dynamodb:Scan
                Resource:
                  - !GetAtt OrganizationAccountsTable.Arn
                  - !GetAtt MultiAccountQuotasTable.Arn
                  - !GetAtt MultiAccountQuotaRequestsTable.Arn
                  - !Sub '${OrganizationAccountsTable.Arn}/index/*'
              - Effect: Allow
                Action:
                  - sns:Publish
                Resource: !Ref MultiAccountQuotaAlertsTopic

  CrossRegionQuotaCoordinatorRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: CrossRegionQuotaCoordinatorRole
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
        - PolicyName: CrossRegionQuotaCoordinatorPolicy
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - service-quotas:GetServiceQuota
                  - service-quotas:ListServiceQuotas
                  - service-quotas:GetServiceQuotaUsageMetric
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
                  - rds:Describe*
                  - elasticloadbalancing:Describe*
                Resource: '*'
              - Effect: Allow
                Action:
                  - dynamodb:GetItem
                  - dynamodb:PutItem
                  - dynamodb:Query
                  - dynamodb:Scan
                Resource:
                  - !GetAtt CrossRegionQuotasTable.Arn
                  - !GetAtt FailoverPlansTable.Arn
                  - !Sub '${FailoverPlansTable.Arn}/index/*'
              - Effect: Allow
                Action:
                  - sns:Publish
                Resource: !Ref CrossRegionQuotaHealthTopic

  # EventBridge rules for scheduled operations
  MultiAccountQuotaScanSchedule:
    Type: AWS::Events::Rule
    Properties:
      Name: MultiAccountQuotaScanSchedule
      Description: Schedule for multi-account quota scanning
      ScheduleExpression: 'rate(6 hours)'
      State: ENABLED
      Targets:
        - Arn: !GetAtt MultiAccountQuotaManagerFunction.Arn
          Id: MultiAccountQuotaScanTarget
          Input: !Sub |
            {
              "action": "scan_quotas"
            }

  MultiAccountQuotaScanPermission:
    Type: AWS::Lambda::Permission
    Properties:
      FunctionName: !Ref MultiAccountQuotaManagerFunction
      Action: lambda:InvokeFunction
      Principal: events.amazonaws.com
      SourceArn: !GetAtt MultiAccountQuotaScanSchedule.Arn

  CrossRegionHealthMonitorSchedule:
    Type: AWS::Events::Rule
    Properties:
      Name: CrossRegionHealthMonitorSchedule
      Description: Schedule for cross-region quota health monitoring
      ScheduleExpression: 'rate(2 hours)'
      State: ENABLED
      Targets:
        - Arn: !GetAtt CrossRegionQuotaCoordinatorFunction.Arn
          Id: CrossRegionHealthMonitorTarget
          Input: !Sub |
            {
              "action": "monitor_health",
              "workload_ids": ["all"]
            }

  CrossRegionHealthMonitorPermission:
    Type: AWS::Lambda::Permission
    Properties:
      FunctionName: !Ref CrossRegionQuotaCoordinatorFunction
      Action: lambda:InvokeFunction
      Principal: events.amazonaws.com
      SourceArn: !GetAtt CrossRegionHealthMonitorSchedule.Arn

  # CloudWatch Dashboard
  QuotaGovernanceDashboard:
    Type: AWS::CloudWatch::Dashboard
    Properties:
      DashboardName: MultiAccountQuotaGovernance
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
                  ["AWS/Lambda", "Duration", "FunctionName", "${MultiAccountQuotaManagerFunction}"],
                  [".", "Errors", ".", "."],
                  [".", "Invocations", ".", "."]
                ],
                "view": "timeSeries",
                "stacked": false,
                "region": "${AWS::Region}",
                "title": "Multi-Account Quota Manager Metrics",
                "period": 300
              }
            },
            {
              "type": "metric",
              "x": 12,
              "y": 0,
              "width": 12,
              "height": 6,
              "properties": {
                "metrics": [
                  ["AWS/Lambda", "Duration", "FunctionName", "${CrossRegionQuotaCoordinatorFunction}"],
                  [".", "Errors", ".", "."],
                  [".", "Invocations", ".", "."]
                ],
                "view": "timeSeries",
                "stacked": false,
                "region": "${AWS::Region}",
                "title": "Cross-Region Coordinator Metrics",
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
                "query": "SOURCE '/aws/lambda/${MultiAccountQuotaManagerFunction}' | fields @timestamp, @message\n| filter @message like /ALERT/\n| sort @timestamp desc\n| limit 20",
                "region": "${AWS::Region}",
                "title": "Recent Multi-Account Quota Alerts",
                "view": "table"
              }
            }
          ]
        }

  # Service Catalog portfolio for quota templates
  QuotaTemplatesPortfolio:
    Type: AWS::ServiceCatalog::Portfolio
    Properties:
      ProviderName: Platform Team
      Description: Quota templates for different environment types
      DisplayName: Quota Management Templates

  # Step Functions for quota orchestration
  QuotaOrchestrationStateMachine:
    Type: AWS::StepFunctions::StateMachine
    Properties:
      StateMachineName: QuotaOrchestrationWorkflow
      RoleArn: !GetAtt StepFunctionsExecutionRole.Arn
      DefinitionString: !Sub |
        {
          "Comment": "Quota orchestration workflow",
          "StartAt": "DiscoverAccounts",
          "States": {
            "DiscoverAccounts": {
              "Type": "Task",
              "Resource": "${MultiAccountQuotaManagerFunction.Arn}",
              "Parameters": {
                "action": "discover_accounts"
              },
              "Next": "ScanQuotas"
            },
            "ScanQuotas": {
              "Type": "Task",
              "Resource": "${MultiAccountQuotaManagerFunction.Arn}",
              "Parameters": {
                "action": "scan_quotas"
              },
              "Next": "AnalyzeResults"
            },
            "AnalyzeResults": {
              "Type": "Task",
              "Resource": "${CrossRegionQuotaCoordinatorFunction.Arn}",
              "Parameters": {
                "action": "analyze_requirements"
              },
              "End": true
            }
          }
        }

  StepFunctionsExecutionRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: states.amazonaws.com
            Action: sts:AssumeRole
      Policies:
        - PolicyName: StepFunctionsExecutionPolicy
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - lambda:InvokeFunction
                Resource:
                  - !GetAtt MultiAccountQuotaManagerFunction.Arn
                  - !GetAtt CrossRegionQuotaCoordinatorFunction.Arn

Outputs:
  QuotaManagementRoleArn:
    Description: ARN of the quota management role to be deployed in member accounts
    Value: !GetAtt QuotaManagementRole.Arn
    Export:
      Name: !Sub '${AWS::StackName}-QuotaManagementRole'

  MultiAccountQuotaManagerFunctionArn:
    Description: ARN of the multi-account quota manager function
    Value: !GetAtt MultiAccountQuotaManagerFunction.Arn
    Export:
      Name: !Sub '${AWS::StackName}-MultiAccountQuotaManager'

  CrossRegionQuotaCoordinatorFunctionArn:
    Description: ARN of the cross-region quota coordinator function
    Value: !GetAtt CrossRegionQuotaCoordinatorFunction.Arn
    Export:
      Name: !Sub '${AWS::StackName}-CrossRegionQuotaCoordinator'

  DashboardURL:
    Description: URL of the quota governance dashboard
    Value: !Sub 'https://${AWS::Region}.console.aws.amazon.com/cloudwatch/home?region=${AWS::Region}#dashboards:name=${QuotaGovernanceDashboard}'

  StepFunctionsStateMachineArn:
    Description: ARN of the quota orchestration state machine
    Value: !Ref QuotaOrchestrationStateMachine
    Export:
      Name: !Sub '${AWS::StackName}-QuotaOrchestrationStateMachine'
```
### Example 4: Disaster recovery quota pre-warming script

```bash
#!/bin/bash
# dr-quota-prewarming.sh
# Script to pre-warm disaster recovery region quotas

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="${SCRIPT_DIR}/dr-config.json"
LOG_FILE="${SCRIPT_DIR}/dr-quota-prewarming.log"
PRIMARY_REGION="${PRIMARY_REGION:-us-east-1}"
DR_REGION="${DR_REGION:-us-west-2}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

# Error handling
error_exit() {
    echo -e "${RED}ERROR: $1${NC}" >&2
    exit 1
}

# Success message
success() {
    echo -e "${GREEN}✓ $1${NC}"
}

# Warning message
warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Info message
info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Load configuration
load_config() {
    if [[ ! -f "$CONFIG_FILE" ]]; then
        error_exit "Configuration file not found: $CONFIG_FILE"
    fi
    
    # Validate JSON
    if ! jq empty "$CONFIG_FILE" 2>/dev/null; then
        error_exit "Invalid JSON in configuration file: $CONFIG_FILE"
    fi
    
    info "Configuration loaded from $CONFIG_FILE"
}

# Get current quota value
get_current_quota() {
    local service_code=$1
    local quota_code=$2
    local region=$3
    
    aws service-quotas get-service-quota \
        --service-code "$service_code" \
        --quota-code "$quota_code" \
        --region "$region" \
        --query 'Quota.Value' \
        --output text 2>/dev/null || echo "0"
}

# Get quota usage
get_quota_usage() {
    local service_code=$1
    local quota_code=$2
    local region=$3
    
    case "$service_code" in
        "ec2")
            case "$quota_code" in
                "L-1216C47A") # Running On-Demand EC2 instances
                    aws ec2 describe-instances \
                        --region "$region" \
                        --filters "Name=instance-state-name,Values=running" \
                        --query 'length(Reservations[].Instances[])' \
                        --output text 2>/dev/null || echo "0"
                    ;;
                "L-0263D0A3") # EC2-VPC Elastic IPs
                    aws ec2 describe-addresses \
                        --region "$region" \
                        --query 'length(Addresses)' \
                        --output text 2>/dev/null || echo "0"
                    ;;
                *)
                    echo "0"
                    ;;
            esac
            ;;
        "lambda")
            case "$quota_code" in
                "L-B99A9384") # Concurrent executions
                    aws lambda get-account-settings \
                        --region "$region" \
                        --query 'AccountUsage.FunctionCount' \
                        --output text 2>/dev/null || echo "0"
                    ;;
                *)
                    echo "0"
                    ;;
            esac
            ;;
        "rds")
            case "$quota_code" in
                "L-7B6409FD") # DB instances
                    aws rds describe-db-instances \
                        --region "$region" \
                        --query 'length(DBInstances)' \
                        --output text 2>/dev/null || echo "0"
                    ;;
                *)
                    echo "0"
                    ;;
            esac
            ;;
        *)
            echo "0"
            ;;
    esac
}

# Request quota increase
request_quota_increase() {
    local service_code=$1
    local quota_code=$2
    local desired_value=$3
    local region=$4
    
    log "Requesting quota increase for $service_code:$quota_code to $desired_value in $region"
    
    local request_id
    request_id=$(aws service-quotas request-service-quota-increase \
        --service-code "$service_code" \
        --quota-code "$quota_code" \
        --desired-value "$desired_value" \
        --region "$region" \
        --query 'RequestedQuota.Id' \
        --output text 2>/dev/null)
    
    if [[ -n "$request_id" && "$request_id" != "None" ]]; then
        success "Quota increase requested: $request_id"
        echo "$request_id"
    else
        warning "Failed to request quota increase"
        echo ""
    fi
}

# Check quota increase status
check_quota_request_status() {
    local request_id=$1
    local region=$2
    
    if [[ -z "$request_id" ]]; then
        echo "UNKNOWN"
        return
    fi
    
    aws service-quotas get-requested-service-quota-change \
        --request-id "$request_id" \
        --region "$region" \
        --query 'RequestedQuota.Status' \
        --output text 2>/dev/null || echo "UNKNOWN"
}

# Analyze primary region quotas
analyze_primary_region() {
    local analysis_file="${SCRIPT_DIR}/primary-region-analysis.json"
    
    info "Analyzing primary region quotas: $PRIMARY_REGION"
    
    local analysis_data="{\"region\":\"$PRIMARY_REGION\",\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"services\":{}}"
    
    # Read services from configuration
    local services
    services=$(jq -r '.services | keys[]' "$CONFIG_FILE")
    
    for service_code in $services; do
        info "Analyzing service: $service_code"
        
        local service_data="{\"quotas\":{}}"
        local quotas
        quotas=$(jq -r ".services.\"$service_code\" | keys[]" "$CONFIG_FILE")
        
        for quota_code in $quotas; do
            local quota_name
            quota_name=$(jq -r ".services.\"$service_code\".\"$quota_code\".name" "$CONFIG_FILE")
            
            local current_quota
            current_quota=$(get_current_quota "$service_code" "$quota_code" "$PRIMARY_REGION")
            
            local current_usage
            current_usage=$(get_quota_usage "$service_code" "$quota_code" "$PRIMARY_REGION")
            
            local utilization=0
            if [[ "$current_quota" -gt 0 ]]; then
                utilization=$(echo "scale=2; $current_usage * 100 / $current_quota" | bc -l)
            fi
            
            local quota_data
            quota_data=$(jq -n \
                --arg name "$quota_name" \
                --argjson current_quota "$current_quota" \
                --argjson current_usage "$current_usage" \
                --argjson utilization "$utilization" \
                '{
                    name: $name,
                    current_quota: $current_quota,
                    current_usage: $current_usage,
                    utilization_percentage: $utilization
                }')
            
            service_data=$(echo "$service_data" | jq ".quotas.\"$quota_code\" = $quota_data")
        done
        
        analysis_data=$(echo "$analysis_data" | jq ".services.\"$service_code\" = $service_data")
    done
    
    echo "$analysis_data" | jq . > "$analysis_file"
    success "Primary region analysis saved to $analysis_file"
}

# Calculate DR requirements
calculate_dr_requirements() {
    local analysis_file="${SCRIPT_DIR}/primary-region-analysis.json"
    local requirements_file="${SCRIPT_DIR}/dr-requirements.json"
    
    info "Calculating DR region requirements"
    
    if [[ ! -f "$analysis_file" ]]; then
        error_exit "Primary region analysis file not found: $analysis_file"
    fi
    
    local dr_requirements="{\"region\":\"$DR_REGION\",\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"requirements\":{}}"
    
    # Read failover type from configuration
    local failover_type
    failover_type=$(jq -r '.failover_type // "warm_standby"' "$CONFIG_FILE")
    
    # Set capacity multiplier based on failover type
    local capacity_multiplier
    case "$failover_type" in
        "hot_standby")
            capacity_multiplier="1.0"
            ;;
        "warm_standby")
            capacity_multiplier="0.5"
            ;;
        "cold_standby")
            capacity_multiplier="0.1"
            ;;
        *)
            capacity_multiplier="0.5"
            ;;
    esac
    
    info "Using failover type: $failover_type (capacity multiplier: $capacity_multiplier)"
    
    # Calculate requirements for each service
    local services
    services=$(jq -r '.services | keys[]' "$analysis_file")
    
    for service_code in $services; do
        local service_requirements="{}"
        local quotas
        quotas=$(jq -r ".services.\"$service_code\".quotas | keys[]" "$analysis_file")
        
        for quota_code in $quotas; do
            local primary_usage
            primary_usage=$(jq -r ".services.\"$service_code\".quotas.\"$quota_code\".current_usage" "$analysis_file")
            
            # Calculate required DR capacity
            local dr_capacity
            dr_capacity=$(echo "scale=0; $primary_usage * $capacity_multiplier" | bc -l)
            
            # Add buffer for scaling
            local buffer_multiplier
            buffer_multiplier=$(jq -r ".services.\"$service_code\".\"$quota_code\".buffer_multiplier // 1.2" "$CONFIG_FILE")
            
            local required_quota
            required_quota=$(echo "scale=0; $dr_capacity * $buffer_multiplier" | bc -l)
            
            # Ensure minimum quota
            local min_quota
            min_quota=$(jq -r ".services.\"$service_code\".\"$quota_code\".min_quota // 10" "$CONFIG_FILE")
            
            if [[ "$required_quota" -lt "$min_quota" ]]; then
                required_quota="$min_quota"
            fi
            
            local quota_name
            quota_name=$(jq -r ".services.\"$service_code\".quotas.\"$quota_code\".name" "$analysis_file")
            
            local requirement_data
            requirement_data=$(jq -n \
                --arg name "$quota_name" \
                --argjson primary_usage "$primary_usage" \
                --argjson dr_capacity "$dr_capacity" \
                --argjson required_quota "$required_quota" \
                --arg failover_type "$failover_type" \
                '{
                    name: $name,
                    primary_usage: $primary_usage,
                    dr_capacity: $dr_capacity,
                    required_quota: $required_quota,
                    failover_type: $failover_type
                }')
            
            service_requirements=$(echo "$service_requirements" | jq ".\"$quota_code\" = $requirement_data")
        done
        
        dr_requirements=$(echo "$dr_requirements" | jq ".requirements.\"$service_code\" = $service_requirements")
    done
    
    echo "$dr_requirements" | jq . > "$requirements_file"
    success "DR requirements calculated and saved to $requirements_file"
}

# Pre-warm DR quotas
prewarm_dr_quotas() {
    local requirements_file="${SCRIPT_DIR}/dr-requirements.json"
    local requests_file="${SCRIPT_DIR}/quota-requests.json"
    
    info "Pre-warming DR region quotas: $DR_REGION"
    
    if [[ ! -f "$requirements_file" ]]; then
        error_exit "DR requirements file not found: $requirements_file"
    fi
    
    local quota_requests="{\"region\":\"$DR_REGION\",\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"requests\":[]}"
    
    # Process each service
    local services
    services=$(jq -r '.requirements | keys[]' "$requirements_file")
    
    for service_code in $services; do
        info "Processing service: $service_code"
        
        local quotas
        quotas=$(jq -r ".requirements.\"$service_code\" | keys[]" "$requirements_file")
        
        for quota_code in $quotas; do
            local quota_name
            quota_name=$(jq -r ".requirements.\"$service_code\".\"$quota_code\".name" "$requirements_file")
            
            local required_quota
            required_quota=$(jq -r ".requirements.\"$service_code\".\"$quota_code\".required_quota" "$requirements_file")
            
            # Get current quota in DR region
            local current_quota
            current_quota=$(get_current_quota "$service_code" "$quota_code" "$DR_REGION")
            
            info "Checking $quota_name: current=$current_quota, required=$required_quota"
            
            if [[ "$current_quota" -lt "$required_quota" ]]; then
                warning "Quota increase needed for $quota_name"
                
                # Request quota increase
                local request_id
                request_id=$(request_quota_increase "$service_code" "$quota_code" "$required_quota" "$DR_REGION")
                
                local request_data
                request_data=$(jq -n \
                    --arg service_code "$service_code" \
                    --arg quota_code "$quota_code" \
                    --arg quota_name "$quota_name" \
                    --argjson current_quota "$current_quota" \
                    --argjson required_quota "$required_quota" \
                    --arg request_id "$request_id" \
                    --arg status "PENDING" \
                    '{
                        service_code: $service_code,
                        quota_code: $quota_code,
                        quota_name: $quota_name,
                        current_quota: $current_quota,
                        required_quota: $required_quota,
                        request_id: $request_id,
                        status: $status,
                        timestamp: now | strftime("%Y-%m-%dT%H:%M:%SZ")
                    }')
                
                quota_requests=$(echo "$quota_requests" | jq ".requests += [$request_data]")
            else
                success "$quota_name already has sufficient quota"
            fi
        done
    done
    
    echo "$quota_requests" | jq . > "$requests_file"
    success "Quota requests saved to $requests_file"
}

# Monitor quota requests
monitor_quota_requests() {
    local requests_file="${SCRIPT_DIR}/quota-requests.json"
    
    if [[ ! -f "$requests_file" ]]; then
        warning "No quota requests file found"
        return
    fi
    
    info "Monitoring quota request status"
    
    local updated_requests="{\"region\":\"$DR_REGION\",\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"requests\":[]}"
    
    local request_count
    request_count=$(jq '.requests | length' "$requests_file")
    
    if [[ "$request_count" -eq 0 ]]; then
        info "No quota requests to monitor"
        return
    fi
    
    for ((i=0; i<request_count; i++)); do
        local request
        request=$(jq ".requests[$i]" "$requests_file")
        
        local request_id
        request_id=$(echo "$request" | jq -r '.request_id')
        
        local quota_name
        quota_name=$(echo "$request" | jq -r '.quota_name')
        
        if [[ -n "$request_id" && "$request_id" != "null" && "$request_id" != "" ]]; then
            local status
            status=$(check_quota_request_status "$request_id" "$DR_REGION")
            
            info "Request for $quota_name: $status"
            
            # Update request with current status
            request=$(echo "$request" | jq --arg status "$status" '.status = $status')
        else
            warning "No request ID for $quota_name"
        fi
        
        updated_requests=$(echo "$updated_requests" | jq ".requests += [$request]")
    done
    
    echo "$updated_requests" | jq . > "$requests_file"
    
    # Summary
    local approved_count
    approved_count=$(jq '.requests | map(select(.status == "APPROVED")) | length' "$requests_file")
    
    local pending_count
    pending_count=$(jq '.requests | map(select(.status == "PENDING")) | length' "$requests_file")
    
    local denied_count
    denied_count=$(jq '.requests | map(select(.status == "DENIED")) | length' "$requests_file")
    
    info "Quota request summary:"
    info "  Approved: $approved_count"
    info "  Pending: $pending_count"
    info "  Denied: $denied_count"
}

# Generate report
generate_report() {
    local report_file="${SCRIPT_DIR}/dr-quota-report.json"
    
    info "Generating DR quota pre-warming report"
    
    local report="{\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"primary_region\":\"$PRIMARY_REGION\",\"dr_region\":\"$DR_REGION\"}"
    
    # Include analysis data if available
    if [[ -f "${SCRIPT_DIR}/primary-region-analysis.json" ]]; then
        local analysis
        analysis=$(cat "${SCRIPT_DIR}/primary-region-analysis.json")
        report=$(echo "$report" | jq ".primary_analysis = $analysis")
    fi
    
    # Include requirements data if available
    if [[ -f "${SCRIPT_DIR}/dr-requirements.json" ]]; then
        local requirements
        requirements=$(cat "${SCRIPT_DIR}/dr-requirements.json")
        report=$(echo "$report" | jq ".dr_requirements = $requirements")
    fi
    
    # Include requests data if available
    if [[ -f "${SCRIPT_DIR}/quota-requests.json" ]]; then
        local requests
        requests=$(cat "${SCRIPT_DIR}/quota-requests.json")
        report=$(echo "$report" | jq ".quota_requests = $requests")
    fi
    
    echo "$report" | jq . > "$report_file"
    success "Report generated: $report_file"
}

# Main execution
main() {
    local action="${1:-all}"
    
    echo "DR Quota Pre-warming Tool"
    echo "========================="
    echo "Primary Region: $PRIMARY_REGION"
    echo "DR Region: $DR_REGION"
    echo "Action: $action"
    echo
    
    # Load configuration
    load_config
    
    case "$action" in
        "analyze")
            analyze_primary_region
            ;;
        "calculate")
            calculate_dr_requirements
            ;;
        "prewarm")
            prewarm_dr_quotas
            ;;
        "monitor")
            monitor_quota_requests
            ;;
        "report")
            generate_report
            ;;
        "all")
            analyze_primary_region
            calculate_dr_requirements
            prewarm_dr_quotas
            monitor_quota_requests
            generate_report
            ;;
        *)
            echo "Usage: $0 [analyze|calculate|prewarm|monitor|report|all]"
            exit 1
            ;;
    esac
    
    success "DR quota pre-warming completed successfully"
}

# Check dependencies
check_dependencies() {
    local deps=("aws" "jq" "bc")
    
    for dep in "${deps[@]}"; do
        if ! command -v "$dep" &> /dev/null; then
            error_exit "$dep is required but not installed"
        fi
    done
    
    # Check AWS CLI configuration
    if ! aws sts get-caller-identity &> /dev/null; then
        error_exit "AWS CLI is not configured or credentials are invalid"
    fi
}

# Script entry point
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    check_dependencies
    main "$@"
fi
```

## AWS services to consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Organizations</h4>
    <p>Centralized management service for multiple AWS accounts. Enables organization-wide quota governance and policy enforcement across member accounts.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Service Quotas</h4>
    <p>Service for viewing and managing quotas across multiple accounts and regions. Provides APIs for quota retrieval, monitoring, and increase requests.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Lambda</h4>
    <p>Serverless compute service for running multi-account quota management functions and cross-region coordination workflows.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon DynamoDB</h4>
    <p>NoSQL database service for storing multi-account quota information, cross-region analysis data, and failover plans.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Step Functions</h4>
    <p>Workflow orchestration service for coordinating complex multi-account and multi-region quota management processes.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon EventBridge</h4>
    <p>Event bus service for scheduling and triggering quota management workflows across accounts and regions.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Systems Manager</h4>
    <p>Management service for maintaining quota configurations and automating quota management tasks across multiple accounts.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon SNS</h4>
    <p>Messaging service for sending quota alerts and notifications across multiple accounts and regions.</p>
  </div>
</div>

## Benefits of managing service quotas across accounts and regions

- **Consistent availability**: Ensures adequate quotas are available across all environments and regions
- **Disaster recovery readiness**: Guarantees sufficient capacity for failover scenarios
- **Simplified governance**: Provides centralized management and visibility across multiple accounts
- **Proactive scaling**: Enables coordinated quota increases across environments
- **Cost optimization**: Prevents over-provisioning while ensuring adequate capacity
- **Compliance assurance**: Maintains consistent quota policies across the organization
- **Reduced operational overhead**: Automates quota management across multiple environments
- **Improved reliability**: Prevents service disruptions due to quota limitations during scaling or failover

## Related resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/rel_manage_service_limits_limits_considered.html">AWS Well-Architected Framework - Manage service quotas across accounts and regions</a></li>
    <li><a href="https://docs.aws.amazon.com/organizations/latest/userguide/orgs_introduction.html">AWS Organizations User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/servicequotas/latest/userguide/organization-templates.html">Service Quotas Organization Templates</a></li>
    <li><a href="https://aws.amazon.com/blogs/aws/new-service-quotas-view-and-manage-quotas-for-aws-services-from-one-location/">New – Service Quotas: View and Manage Quotas for AWS Services from One Location</a></li>
    <li><a href="https://docs.aws.amazon.com/general/latest/gr/aws-service-information.html">AWS Service Information</a></li>
    <li><a href="https://aws.amazon.com/premiumsupport/knowledge-center/manage-service-limits-across-accounts/">How do I manage service quotas across multiple AWS accounts?</a></li>
  </ul>
</div>
