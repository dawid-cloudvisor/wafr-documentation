---
title: COST03-BP05 - Add organization information to cost and usage
layout: default
parent: COST03 - How do you monitor usage and cost?
grand_parent: Cost Optimization
nav_order: 5
---

<div class="pillar-header">
  <h1>COST03-BP05: Add organization information to cost and usage</h1>
  <p>Enhance cost and usage data with organizational context to enable meaningful analysis and attribution. Adding organizational information transforms raw cost data into actionable business intelligence that supports decision-making and accountability.</p>
</div>

## Implementation guidance

Adding organizational information to cost and usage data involves enriching raw AWS billing data with business context, metadata, and organizational structure information. This enrichment enables more meaningful analysis, better cost attribution, and improved decision-making capabilities.

### Information Enhancement Principles

**Business Context**: Add information that relates cloud costs to business operations, such as customer segments, product lines, and revenue streams.

**Organizational Structure**: Include organizational hierarchy information such as business units, departments, teams, and cost centers.

**Operational Context**: Add operational information such as environment types, application classifications, and service levels.

**Temporal Context**: Include time-based information such as project phases, business cycles, and seasonal patterns.

### Types of Organizational Information

**Hierarchical Information**: Business unit, department, team, and individual ownership information that reflects organizational structure.

**Financial Information**: Cost centers, budget allocations, project codes, and financial reporting categories.

**Operational Information**: Environment classifications, service levels, compliance requirements, and operational procedures.

**Business Information**: Product associations, customer segments, revenue attribution, and business value metrics.

## AWS Services to Consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Resource Groups</h4>
    <p>Organize resources with organizational metadata. Use resource groups to apply consistent organizational information across related resources.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Systems Manager Parameter Store</h4>
    <p>Store organizational metadata and configuration information. Use Parameter Store to maintain centralized organizational data for cost enrichment.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon DynamoDB</h4>
    <p>Store complex organizational relationships and metadata. Use DynamoDB for fast lookup of organizational information during cost processing.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Lambda</h4>
    <p>Implement automated organizational information enrichment. Use Lambda to process cost data and add organizational context.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Glue</h4>
    <p>Transform and enrich cost data with organizational information. Use Glue for large-scale data processing and enrichment workflows.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon S3</h4>
    <p>Store organizational data files and enriched cost datasets. Use S3 for scalable storage of organizational metadata and processed cost data.</p>
  </div>
</div>

## Implementation Steps

### 1. Define Organizational Data Model
- Identify organizational information needed for cost analysis
- Design data model for organizational metadata
- Define relationships between organizational entities
- Plan for data model evolution and maintenance

### 2. Collect Organizational Information
- Gather organizational structure and hierarchy data
- Collect financial and operational metadata
- Integrate with HR and financial systems for organizational data
- Establish data quality and validation procedures

### 3. Implement Data Enrichment Pipeline
- Create automated data enrichment processes
- Implement data transformation and mapping logic
- Set up data validation and quality assurance
- Create error handling and exception management

### 4. Integrate with Cost Data
- Combine organizational information with cost and usage data
- Implement real-time and batch enrichment processes
- Create enriched datasets for analysis and reporting
- Set up data lineage and audit trails

### 5. Create Enhanced Reporting
- Build reports and dashboards using enriched data
- Implement role-based access to organizational cost data
- Create automated reporting with organizational context
- Set up alerting based on organizational dimensions

### 6. Maintain Data Quality
- Implement ongoing data quality monitoring
- Create processes for updating organizational information
- Set up validation and reconciliation procedures
- Establish data governance for organizational metadata

## Organizational Data Model

### Hierarchical Structure
```yaml
Organization:
  Company: "TechCorp Inc"
  BusinessUnits:
    Engineering:
      Departments:
        - Platform_Engineering
        - Product_Development
        - Data_Engineering
        - Security_Engineering
      CostCenter: "ENG-001"
      Budget: 2000000
      
    Sales_Marketing:
      Departments:
        - Sales_Operations
        - Marketing_Technology
        - Customer_Success
      CostCenter: "SM-001"
      Budget: 800000
      
    Operations:
      Departments:
        - IT_Operations
        - Infrastructure
        - Support
      CostCenter: "OPS-001"
      Budget: 1200000

Teams:
  Platform_Engineering:
    Manager: "john.doe@company.com"
    Members: 15
    Projects:
      - "PROJ-2024-001"
      - "PROJ-2024-005"
    Budget_Allocation: 500000
    
  Product_Development:
    Manager: "jane.smith@company.com"
    Members: 25
    Projects:
      - "PROJ-2024-002"
      - "PROJ-2024-003"
    Budget_Allocation: 800000
```

### Financial Context
```yaml
Financial_Structure:
  CostCenters:
    ENG-001:
      Name: "Engineering"
      Budget: 2000000
      Approval_Authority: "VP Engineering"
      
    SM-001:
      Name: "Sales & Marketing"
      Budget: 800000
      Approval_Authority: "VP Sales"
      
  Projects:
    PROJ-2024-001:
      Name: "Platform Modernization"
      Budget: 300000
      Start_Date: "2024-01-01"
      End_Date: "2024-12-31"
      Status: "Active"
      
    PROJ-2024-002:
      Name: "Mobile App Development"
      Budget: 250000
      Start_Date: "2024-03-01"
      End_Date: "2024-09-30"
      Status: "Active"
```

### Operational Context
```yaml
Operational_Classifications:
  Environments:
    Production:
      SLA: "99.9%"
      Backup_Required: true
      Monitoring_Level: "Critical"
      
    Staging:
      SLA: "99%"
      Backup_Required: true
      Monitoring_Level: "Standard"
      
    Development:
      SLA: "95%"
      Backup_Required: false
      Monitoring_Level: "Basic"
      
  Applications:
    CustomerPortal:
      Criticality: "High"
      Data_Classification: "Confidential"
      Compliance_Requirements: ["SOC2", "PCI-DSS"]
      
    InternalTools:
      Criticality: "Medium"
      Data_Classification: "Internal"
      Compliance_Requirements: ["SOC2"]
```

## Data Enrichment Implementation

### Organizational Data Storage
```python
import boto3
import json
from datetime import datetime

class OrganizationalDataManager:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.ssm = boto3.client('ssm')
        self.s3 = boto3.client('s3')
        
        # Initialize tables
        self.org_table = self.dynamodb.Table('OrganizationalStructure')
        self.project_table = self.dynamodb.Table('ProjectInformation')
        self.financial_table = self.dynamodb.Table('FinancialContext')
    
    def store_organizational_structure(self, org_data):
        """Store organizational structure in DynamoDB"""
        
        try:
            # Store business units
            for bu_name, bu_data in org_data['BusinessUnits'].items():
                self.org_table.put_item(
                    Item={
                        'EntityType': 'BusinessUnit',
                        'EntityId': bu_name,
                        'Name': bu_name,
                        'CostCenter': bu_data['CostCenter'],
                        'Budget': bu_data['Budget'],
                        'Departments': bu_data['Departments'],
                        'LastUpdated': datetime.now().isoformat()
                    }
                )
            
            # Store teams
            for team_name, team_data in org_data['Teams'].items():
                self.org_table.put_item(
                    Item={
                        'EntityType': 'Team',
                        'EntityId': team_name,
                        'Name': team_name,
                        'Manager': team_data['Manager'],
                        'Members': team_data['Members'],
                        'Projects': team_data['Projects'],
                        'BudgetAllocation': team_data['Budget_Allocation'],
                        'LastUpdated': datetime.now().isoformat()
                    }
                )
            
            print("Organizational structure stored successfully")
            
        except Exception as e:
            print(f"Error storing organizational structure: {str(e)}")
    
    def store_project_information(self, project_data):
        """Store project information for cost attribution"""
        
        try:
            for project_id, project_info in project_data['Projects'].items():
                self.project_table.put_item(
                    Item={
                        'ProjectId': project_id,
                        'Name': project_info['Name'],
                        'Budget': project_info['Budget'],
                        'StartDate': project_info['Start_Date'],
                        'EndDate': project_info['End_Date'],
                        'Status': project_info['Status'],
                        'LastUpdated': datetime.now().isoformat()
                    }
                )
            
            print("Project information stored successfully")
            
        except Exception as e:
            print(f"Error storing project information: {str(e)}")
    
    def get_organizational_context(self, entity_type, entity_id):
        """Retrieve organizational context for cost enrichment"""
        
        try:
            response = self.org_table.get_item(
                Key={
                    'EntityType': entity_type,
                    'EntityId': entity_id
                }
            )
            
            if 'Item' in response:
                return response['Item']
            else:
                return None
                
        except Exception as e:
            print(f"Error retrieving organizational context: {str(e)}")
            return None

def enrich_cost_data_with_org_info():
    """Enrich cost data with organizational information"""
    
    org_manager = OrganizationalDataManager()
    ce_client = boto3.client('ce')
    
    # Get cost data
    response = ce_client.get_cost_and_usage(
        TimePeriod={
            'Start': '2024-01-01',
            'End': '2024-01-31'
        },
        Granularity='DAILY',
        Metrics=['BlendedCost'],
        GroupBy=[
            {'Type': 'TAG', 'Key': 'BusinessUnit'},
            {'Type': 'TAG', 'Key': 'Project'},
            {'Type': 'TAG', 'Key': 'Team'},
            {'Type': 'DIMENSION', 'Key': 'SERVICE'}
        ]
    )
    
    enriched_data = []
    
    # Enrich each cost record
    for result in response['ResultsByTime']:
        date = result['TimePeriod']['Start']
        
        for group in result['Groups']:
            cost_record = {
                'date': date,
                'cost': float(group['Metrics']['BlendedCost']['Amount']),
                'service': group['Keys'][3] if len(group['Keys']) > 3 else 'Unknown',
                'raw_tags': {
                    'business_unit': group['Keys'][0] if len(group['Keys']) > 0 else None,
                    'project': group['Keys'][1] if len(group['Keys']) > 1 else None,
                    'team': group['Keys'][2] if len(group['Keys']) > 2 else None
                }
            }
            
            # Enrich with organizational context
            if cost_record['raw_tags']['business_unit']:
                bu_context = org_manager.get_organizational_context(
                    'BusinessUnit', 
                    cost_record['raw_tags']['business_unit']
                )
                if bu_context:
                    cost_record['business_unit_info'] = {
                        'name': bu_context['Name'],
                        'cost_center': bu_context['CostCenter'],
                        'budget': bu_context['Budget']
                    }
            
            # Enrich with team context
            if cost_record['raw_tags']['team']:
                team_context = org_manager.get_organizational_context(
                    'Team',
                    cost_record['raw_tags']['team']
                )
                if team_context:
                    cost_record['team_info'] = {
                        'name': team_context['Name'],
                        'manager': team_context['Manager'],
                        'budget_allocation': team_context['BudgetAllocation']
                    }
            
            # Enrich with project context
            if cost_record['raw_tags']['project']:
                project_context = org_manager.project_table.get_item(
                    Key={'ProjectId': cost_record['raw_tags']['project']}
                )
                if 'Item' in project_context:
                    project_info = project_context['Item']
                    cost_record['project_info'] = {
                        'name': project_info['Name'],
                        'budget': project_info['Budget'],
                        'status': project_info['Status'],
                        'start_date': project_info['StartDate'],
                        'end_date': project_info['EndDate']
                    }
            
            enriched_data.append(cost_record)
    
    return enriched_data
```

### Automated Enrichment Pipeline
```python
def create_enrichment_pipeline():
    """Create automated pipeline for cost data enrichment"""
    
    # Lambda function for cost data enrichment
    lambda_code = '''
import boto3
import json
from datetime import datetime, timedelta

def lambda_handler(event, context):
    """Enrich cost data with organizational information"""
    
    # Initialize clients
    dynamodb = boto3.resource('dynamodb')
    s3 = boto3.client('s3')
    
    # Get organizational data
    org_table = dynamodb.Table('OrganizationalStructure')
    project_table = dynamodb.Table('ProjectInformation')
    
    # Process cost data from S3
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    # Download cost data
    response = s3.get_object(Bucket=bucket, Key=key)
    cost_data = json.loads(response['Body'].read())
    
    # Enrich data
    enriched_data = []
    
    for record in cost_data:
        enriched_record = record.copy()
        
        # Add organizational context
        if 'business_unit' in record:
            org_response = org_table.get_item(
                Key={
                    'EntityType': 'BusinessUnit',
                    'EntityId': record['business_unit']
                }
            )
            
            if 'Item' in org_response:
                enriched_record['org_context'] = {
                    'cost_center': org_response['Item']['CostCenter'],
                    'budget': org_response['Item']['Budget'],
                    'departments': org_response['Item']['Departments']
                }
        
        # Add project context
        if 'project' in record:
            project_response = project_table.get_item(
                Key={'ProjectId': record['project']}
            )
            
            if 'Item' in project_response:
                enriched_record['project_context'] = {
                    'name': project_response['Item']['Name'],
                    'budget': project_response['Item']['Budget'],
                    'status': project_response['Item']['Status']
                }
        
        # Add calculated fields
        enriched_record['enrichment_timestamp'] = datetime.now().isoformat()
        enriched_record['cost_per_team_member'] = calculate_cost_per_member(enriched_record)
        enriched_record['budget_utilization'] = calculate_budget_utilization(enriched_record)
        
        enriched_data.append(enriched_record)
    
    # Store enriched data
    enriched_key = key.replace('raw/', 'enriched/')
    s3.put_object(
        Bucket=bucket,
        Key=enriched_key,
        Body=json.dumps(enriched_data, indent=2)
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps(f'Enriched {len(enriched_data)} records')
    }

def calculate_cost_per_member(record):
    """Calculate cost per team member"""
    if 'team_info' in record and 'members' in record['team_info']:
        return record['cost'] / record['team_info']['members']
    return 0

def calculate_budget_utilization(record):
    """Calculate budget utilization percentage"""
    if 'project_context' in record and 'budget' in record['project_context']:
        return (record['cost'] / record['project_context']['budget']) * 100
    return 0
'''
    
    # Create Lambda function
    lambda_client = boto3.client('lambda')
    
    try:
        lambda_client.create_function(
            FunctionName='CostDataEnrichment',
            Runtime='python3.9',
            Role='arn:aws:iam::ACCOUNT:role/CostEnrichmentRole',
            Handler='lambda_function.lambda_handler',
            Code={'ZipFile': lambda_code.encode()},
            Description='Enrich cost data with organizational information',
            Timeout=300
        )
        
        # Set up S3 trigger
        s3 = boto3.client('s3')
        
        s3.put_bucket_notification_configuration(
            Bucket='cost-data-bucket',
            NotificationConfiguration={
                'LambdaConfigurations': [
                    {
                        'Id': 'CostDataEnrichmentTrigger',
                        'LambdaFunctionArn': f'arn:aws:lambda:REGION:ACCOUNT:function:CostDataEnrichment',
                        'Events': ['s3:ObjectCreated:*'],
                        'Filter': {
                            'Key': {
                                'FilterRules': [
                                    {
                                        'Name': 'prefix',
                                        'Value': 'raw/cost-data/'
                                    }
                                ]
                            }
                        }
                    }
                ]
            }
        )
        
        print("Created cost data enrichment pipeline")
        
    except Exception as e:
        print(f"Error creating enrichment pipeline: {str(e)}")
```

## Business Intelligence Integration

### Enhanced Reporting with Organizational Context
```python
def create_organizational_cost_reports():
    """Create comprehensive cost reports with organizational context"""
    
    # Get enriched cost data
    enriched_data = get_enriched_cost_data()
    
    # Generate organizational reports
    reports = {
        'business_unit_performance': generate_bu_performance_report(enriched_data),
        'project_cost_analysis': generate_project_cost_report(enriched_data),
        'team_efficiency_metrics': generate_team_efficiency_report(enriched_data),
        'cost_center_utilization': generate_cost_center_report(enriched_data)
    }
    
    return reports

def generate_bu_performance_report(data):
    """Generate business unit performance report"""
    
    bu_summary = {}
    
    for record in data:
        if 'business_unit_info' in record:
            bu_name = record['business_unit_info']['name']
            
            if bu_name not in bu_summary:
                bu_summary[bu_name] = {
                    'total_cost': 0,
                    'budget': record['business_unit_info']['budget'],
                    'cost_center': record['business_unit_info']['cost_center'],
                    'monthly_costs': {},
                    'service_breakdown': {}
                }
            
            # Aggregate costs
            bu_summary[bu_name]['total_cost'] += record['cost']
            
            # Monthly breakdown
            month = record['date'][:7]  # YYYY-MM
            if month not in bu_summary[bu_name]['monthly_costs']:
                bu_summary[bu_name]['monthly_costs'][month] = 0
            bu_summary[bu_name]['monthly_costs'][month] += record['cost']
            
            # Service breakdown
            service = record['service']
            if service not in bu_summary[bu_name]['service_breakdown']:
                bu_summary[bu_name]['service_breakdown'][service] = 0
            bu_summary[bu_name]['service_breakdown'][service] += record['cost']
    
    # Calculate performance metrics
    for bu_name, bu_data in bu_summary.items():
        bu_data['budget_utilization'] = (bu_data['total_cost'] / bu_data['budget']) * 100
        bu_data['variance'] = bu_data['total_cost'] - bu_data['budget']
        bu_data['variance_percentage'] = (bu_data['variance'] / bu_data['budget']) * 100
    
    return bu_summary

def generate_project_cost_report(data):
    """Generate project-specific cost analysis"""
    
    project_summary = {}
    
    for record in data:
        if 'project_info' in record:
            project_id = record['raw_tags']['project']
            
            if project_id not in project_summary:
                project_summary[project_id] = {
                    'name': record['project_info']['name'],
                    'budget': record['project_info']['budget'],
                    'status': record['project_info']['status'],
                    'start_date': record['project_info']['start_date'],
                    'end_date': record['project_info']['end_date'],
                    'total_cost': 0,
                    'daily_costs': {},
                    'team_costs': {}
                }
            
            # Aggregate costs
            project_summary[project_id]['total_cost'] += record['cost']
            
            # Daily breakdown
            date = record['date']
            if date not in project_summary[project_id]['daily_costs']:
                project_summary[project_id]['daily_costs'][date] = 0
            project_summary[project_id]['daily_costs'][date] += record['cost']
            
            # Team breakdown
            if 'team_info' in record:
                team = record['team_info']['name']
                if team not in project_summary[project_id]['team_costs']:
                    project_summary[project_id]['team_costs'][team] = 0
                project_summary[project_id]['team_costs'][team] += record['cost']
    
    # Calculate project metrics
    for project_id, project_data in project_summary.items():
        project_data['budget_utilization'] = (project_data['total_cost'] / project_data['budget']) * 100
        project_data['burn_rate'] = calculate_project_burn_rate(project_data)
        project_data['projected_total'] = calculate_projected_cost(project_data)
    
    return project_summary
```

## Data Quality and Governance

### Organizational Data Validation
```python
def implement_data_quality_checks():
    """Implement comprehensive data quality checks for organizational data"""
    
    class DataQualityChecker:
        def __init__(self):
            self.validation_rules = {
                'business_unit': self.validate_business_unit,
                'project': self.validate_project,
                'team': self.validate_team,
                'cost_center': self.validate_cost_center
            }
        
        def validate_enriched_data(self, data):
            """Validate enriched cost data"""
            
            validation_results = {
                'total_records': len(data),
                'valid_records': 0,
                'invalid_records': 0,
                'validation_errors': []
            }
            
            for record in data:
                is_valid = True
                record_errors = []
                
                # Check required organizational fields
                for field, validator in self.validation_rules.items():
                    if field in record['raw_tags'] and record['raw_tags'][field]:
                        if not validator(record['raw_tags'][field], record):
                            is_valid = False
                            record_errors.append(f"Invalid {field}: {record['raw_tags'][field]}")
                
                # Check data consistency
                consistency_errors = self.check_data_consistency(record)
                if consistency_errors:
                    is_valid = False
                    record_errors.extend(consistency_errors)
                
                if is_valid:
                    validation_results['valid_records'] += 1
                else:
                    validation_results['invalid_records'] += 1
                    validation_results['validation_errors'].append({
                        'record_id': record.get('id', 'unknown'),
                        'errors': record_errors
                    })
            
            return validation_results
        
        def validate_business_unit(self, bu_name, record):
            """Validate business unit information"""
            
            # Check if business unit exists in organizational structure
            if 'business_unit_info' not in record:
                return False
            
            # Check budget consistency
            if record['business_unit_info']['budget'] <= 0:
                return False
            
            # Check cost center format
            cost_center = record['business_unit_info']['cost_center']
            if not cost_center or len(cost_center) < 3:
                return False
            
            return True
        
        def validate_project(self, project_id, record):
            """Validate project information"""
            
            if 'project_info' not in record:
                return False
            
            # Check project status
            valid_statuses = ['Active', 'Completed', 'On Hold', 'Cancelled']
            if record['project_info']['status'] not in valid_statuses:
                return False
            
            # Check date consistency
            start_date = record['project_info']['start_date']
            end_date = record['project_info']['end_date']
            
            if start_date >= end_date:
                return False
            
            return True
        
        def check_data_consistency(self, record):
            """Check for data consistency issues"""
            
            errors = []
            
            # Check cost allocation consistency
            if 'project_info' in record and 'team_info' in record:
                if record['cost'] > record['team_info']['budget_allocation']:
                    errors.append("Cost exceeds team budget allocation")
            
            # Check temporal consistency
            record_date = datetime.strptime(record['date'], '%Y-%m-%d')
            if 'project_info' in record:
                project_start = datetime.strptime(record['project_info']['start_date'], '%Y-%m-%d')
                project_end = datetime.strptime(record['project_info']['end_date'], '%Y-%m-%d')
                
                if record_date < project_start or record_date > project_end:
                    errors.append("Cost date outside project timeline")
            
            return errors
    
    # Run data quality checks
    checker = DataQualityChecker()
    enriched_data = get_enriched_cost_data()
    validation_results = checker.validate_enriched_data(enriched_data)
    
    return validation_results
```

## Common Challenges and Solutions

### Challenge: Incomplete Organizational Data

**Solution**: Implement data collection processes from multiple sources. Create default values for missing information. Use automated data discovery and inference. Establish data governance processes for maintaining organizational information.

### Challenge: Organizational Structure Changes

**Solution**: Design flexible data models that can accommodate changes. Implement versioning for organizational data. Create automated processes for detecting and handling structure changes. Maintain historical organizational context.

### Challenge: Data Integration Complexity

**Solution**: Use standardized data formats and APIs. Implement robust data transformation and mapping logic. Create comprehensive error handling and validation. Use managed integration services where possible.

### Challenge: Performance Impact of Enrichment

**Solution**: Optimize data processing pipelines for performance. Use appropriate caching strategies. Implement parallel processing where possible. Consider using managed analytics services for large-scale processing.

### Challenge: Data Quality and Consistency

**Solution**: Implement comprehensive data validation and quality checks. Create automated data quality monitoring. Establish data governance processes and ownership. Use data lineage tracking for audit and troubleshooting.

## Related Resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/cost_monitor_usage_organization_information.html">AWS Well-Architected Framework - Add organization information to cost and usage</a></li>
    <li><a href="https://docs.aws.amazon.com/ARG/latest/userguide/welcome.html">AWS Resource Groups User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html">AWS Systems Manager Parameter Store</a></li>
    <li><a href="https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html">Amazon DynamoDB Developer Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/lambda/latest/dg/welcome.html">AWS Lambda Developer Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/glue/latest/dg/what-is-glue.html">AWS Glue Developer Guide</a></li>
    <li><a href="https://aws.amazon.com/blogs/aws-cost-management/">AWS Cost Management Blog</a></li>
    <li><a href="https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-alloc-tags.html">Cost Allocation Tags</a></li>
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
