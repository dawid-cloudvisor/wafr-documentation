---
title: COST03-BP02 - Identify cost attribution categories
layout: default
parent: COST03 - How do you monitor usage and cost?
grand_parent: Cost Optimization
nav_order: 2
---

<div class="pillar-header">
  <h1>COST03-BP02: Identify cost attribution categories</h1>
  <p>Establish clear categories for cost attribution that align with your business structure and enable meaningful cost allocation. Well-defined attribution categories provide the foundation for accurate cost tracking, accountability, and optimization across your organization.</p>
</div>

## Implementation guidance

Cost attribution categories define how you organize and allocate cloud costs to different parts of your business. These categories should reflect your organizational structure, business model, and decision-making processes to enable effective cost management and accountability.

### Attribution Category Design Principles

**Business Alignment**: Categories should align with how your business operates and makes decisions about technology investments and resource allocation.

**Hierarchical Structure**: Design categories in a hierarchical manner that supports both high-level and detailed cost analysis.

**Mutually Exclusive**: Ensure categories are clearly defined and mutually exclusive to prevent double-counting or confusion in cost allocation.

**Actionable Insights**: Categories should enable actionable insights that support cost optimization and business decision-making.

### Common Attribution Categories

**Organizational Structure**: Business units, departments, teams, and cost centers that reflect your organizational hierarchy.

**Product and Service Lines**: Different products, services, or customer segments that your organization supports.

**Project and Initiative Based**: Specific projects, initiatives, or campaigns with defined budgets and timelines.

**Environment and Lifecycle**: Development, testing, staging, and production environments with different cost profiles.

**Functional Categories**: Infrastructure, applications, data, security, and other functional areas of technology spending.

## AWS Services to Consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Cost Categories</h4>
    <p>Create custom cost categories that group costs according to your business logic. Use Cost Categories to implement complex attribution rules and hierarchies.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Resource Groups</h4>
    <p>Organize resources into logical groups for cost attribution. Use resource groups to track costs for specific applications, projects, or business units.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Organizations</h4>
    <p>Use organizational units (OUs) to create account-based cost attribution categories. Align account structure with business attribution requirements.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Cost Explorer</h4>
    <p>Analyze costs using different attribution dimensions. Create custom reports and filters based on your attribution categories.</p>
  </div>
</div>

## Implementation Steps

### 1. Analyze Business Structure
- Map organizational hierarchy and decision-making structure
- Identify key business dimensions for cost allocation
- Understand existing financial reporting and budgeting processes
- Document stakeholder requirements for cost visibility

### 2. Design Attribution Framework
- Define primary and secondary attribution categories
- Create hierarchical category structure
- Establish rules for cost allocation and attribution
- Design category naming conventions and standards

### 3. Implement Tagging Strategy
- Create comprehensive tagging taxonomy aligned with categories
- Implement automated tagging where possible
- Establish tag governance and compliance processes
- Create tag validation and quality assurance procedures

### 4. Configure Cost Categories
- Set up AWS Cost Categories based on attribution framework
- Create rules for automatic cost categorization
- Implement complex allocation logic where needed
- Test and validate category assignments

### 5. Create Reporting Structure
- Design reports and dashboards for each attribution category
- Implement role-based access to category-specific cost data
- Create automated reporting and distribution processes
- Establish regular review and reconciliation procedures

### 6. Monitor and Optimize
- Track attribution coverage and accuracy
- Gather feedback from stakeholders on category usefulness
- Refine categories based on business changes
- Continuously improve attribution processes and automation

## Attribution Category Examples

### Organizational Attribution
```yaml
Business_Units:
  - Engineering
  - Sales_Marketing
  - Operations
  - Finance_Admin

Departments:
  Engineering:
    - Platform_Engineering
    - Product_Development
    - Data_Engineering
    - Security_Engineering
  Sales_Marketing:
    - Sales_Operations
    - Marketing_Technology
    - Customer_Success

Teams:
  Platform_Engineering:
    - Infrastructure_Team
    - DevOps_Team
    - Monitoring_Team
```

### Product-Based Attribution
```yaml
Product_Lines:
  - Core_Platform
  - Mobile_Applications
  - Analytics_Platform
  - Customer_Portal

Services:
  Core_Platform:
    - User_Management
    - Payment_Processing
    - Notification_Service
    - Search_Service
  Mobile_Applications:
    - iOS_App
    - Android_App
    - Mobile_API
```

### Project Attribution
```yaml
Project_Types:
  - Strategic_Initiatives
  - Maintenance_Projects
  - Compliance_Projects
  - Innovation_Projects

Project_Status:
  - Planning
  - Development
  - Testing
  - Production
  - Maintenance
  - Decommissioned
```

### Environment Attribution
```yaml
Environments:
  - Production
  - Staging
  - Development
  - Testing
  - Sandbox

Environment_Purposes:
  Production:
    - Customer_Facing
    - Internal_Tools
    - Data_Processing
  Development:
    - Feature_Development
    - Bug_Fixes
    - Experimentation
```

## Cost Category Implementation

### AWS Cost Categories Configuration
```python
import boto3
import json

def create_cost_categories():
    """Create comprehensive cost categories for attribution"""
    ce_client = boto3.client('ce')
    
    # Business Unit Cost Category
    business_unit_category = {
        'Name': 'BusinessUnit',
        'RuleVersion': 'CostCategoryExpression.v1',
        'Rules': [
            {
                'Value': 'Engineering',
                'Rule': {
                    'Tags': {
                        'Key': 'BusinessUnit',
                        'Values': ['Engineering', 'engineering'],
                        'MatchOptions': ['EQUALS']
                    }
                }
            },
            {
                'Value': 'Sales-Marketing',
                'Rule': {
                    'Tags': {
                        'Key': 'BusinessUnit',
                        'Values': ['Sales', 'Marketing', 'sales', 'marketing'],
                        'MatchOptions': ['EQUALS']
                    }
                }
            },
            {
                'Value': 'Operations',
                'Rule': {
                    'Tags': {
                        'Key': 'BusinessUnit',
                        'Values': ['Operations', 'operations', 'ops'],
                        'MatchOptions': ['EQUALS']
                    }
                }
            }
        ],
        'DefaultValue': 'Unallocated'
    }
    
    # Environment Cost Category
    environment_category = {
        'Name': 'Environment',
        'RuleVersion': 'CostCategoryExpression.v1',
        'Rules': [
            {
                'Value': 'Production',
                'Rule': {
                    'Tags': {
                        'Key': 'Environment',
                        'Values': ['production', 'prod', 'Production'],
                        'MatchOptions': ['EQUALS']
                    }
                }
            },
            {
                'Value': 'Non-Production',
                'Rule': {
                    'Or': [
                        {
                            'Tags': {
                                'Key': 'Environment',
                                'Values': ['development', 'dev', 'Development'],
                                'MatchOptions': ['EQUALS']
                            }
                        },
                        {
                            'Tags': {
                                'Key': 'Environment',
                                'Values': ['testing', 'test', 'Testing'],
                                'MatchOptions': ['EQUALS']
                            }
                        },
                        {
                            'Tags': {
                                'Key': 'Environment',
                                'Values': ['staging', 'stage', 'Staging'],
                                'MatchOptions': ['EQUALS']
                            }
                        }
                    ]
                }
            }
        ],
        'DefaultValue': 'Unknown'
    }
    
    # Create cost categories
    categories = [business_unit_category, environment_category]
    
    for category in categories:
        try:
            response = ce_client.create_cost_category_definition(**category)
            print(f"Created cost category: {category['Name']}")
            print(f"Cost Category ARN: {response['CostCategoryArn']}")
        except Exception as e:
            print(f"Error creating cost category {category['Name']}: {str(e)}")

def create_project_cost_category():
    """Create project-based cost category with complex rules"""
    ce_client = boto3.client('ce')
    
    project_category = {
        'Name': 'ProjectType',
        'RuleVersion': 'CostCategoryExpression.v1',
        'Rules': [
            {
                'Value': 'Strategic-Initiative',
                'Rule': {
                    'And': [
                        {
                            'Tags': {
                                'Key': 'Project',
                                'Values': ['*'],
                                'MatchOptions': ['STARTS_WITH']
                            }
                        },
                        {
                            'Tags': {
                                'Key': 'ProjectType',
                                'Values': ['Strategic', 'strategic'],
                                'MatchOptions': ['EQUALS']
                            }
                        }
                    ]
                }
            },
            {
                'Value': 'Maintenance',
                'Rule': {
                    'Tags': {
                        'Key': 'ProjectType',
                        'Values': ['Maintenance', 'maintenance', 'maint'],
                        'MatchOptions': ['EQUALS']
                    }
                }
            },
            {
                'Value': 'Innovation',
                'Rule': {
                    'Tags': {
                        'Key': 'ProjectType',
                        'Values': ['Innovation', 'innovation', 'R&D', 'research'],
                        'MatchOptions': ['EQUALS']
                    }
                }
            }
        ],
        'DefaultValue': 'BAU-Operations'
    }
    
    try:
        response = ce_client.create_cost_category_definition(**project_category)
        return response['CostCategoryArn']
    except Exception as e:
        print(f"Error creating project cost category: {str(e)}")
        return None
```

## Tagging Strategy for Attribution

### Comprehensive Tagging Taxonomy
```yaml
Required_Tags:
  BusinessUnit:
    description: "Primary business unit responsible for the resource"
    values: ["Engineering", "Sales", "Marketing", "Operations", "Finance"]
    
  Environment:
    description: "Environment where the resource is deployed"
    values: ["production", "staging", "development", "testing", "sandbox"]
    
  Project:
    description: "Project or initiative the resource supports"
    format: "PROJ-YYYY-NNN (e.g., PROJ-2024-001)"
    
  Owner:
    description: "Team or individual responsible for the resource"
    format: "team-name or email address"

Optional_Tags:
  Application:
    description: "Application or service the resource supports"
    
  CostCenter:
    description: "Financial cost center for chargeback"
    
  DataClassification:
    description: "Data sensitivity level"
    values: ["public", "internal", "confidential", "restricted"]
    
  Backup:
    description: "Backup requirements"
    values: ["required", "not-required", "custom"]
    
  Schedule:
    description: "Operating schedule for cost optimization"
    values: ["24x7", "business-hours", "on-demand"]
```

### Automated Tagging Implementation
```python
import boto3
import json

def implement_automated_tagging():
    """Implement automated tagging for cost attribution"""
    
    # Lambda function for auto-tagging new resources
    lambda_code = '''
import boto3
import json

def lambda_handler(event, context):
    """Auto-tag resources based on creation context"""
    
    # Parse CloudTrail event
    detail = event['detail']
    event_name = detail['eventName']
    user_identity = detail['userIdentity']
    
    # Determine tags based on context
    tags = []
    
    # Add owner tag based on user identity
    if 'userName' in user_identity:
        tags.append({'Key': 'Owner', 'Value': user_identity['userName']})
    
    # Add environment tag based on account
    account_id = detail['recipientAccountId']
    environment_mapping = {
        '111111111111': 'production',
        '222222222222': 'staging',
        '333333333333': 'development'
    }
    
    if account_id in environment_mapping:
        tags.append({'Key': 'Environment', 'Value': environment_mapping[account_id]})
    
    # Add business unit tag based on IAM role
    if 'sessionContext' in user_identity:
        role_name = user_identity['sessionContext']['sessionIssuer']['userName']
        if 'engineering' in role_name.lower():
            tags.append({'Key': 'BusinessUnit', 'Value': 'Engineering'})
        elif 'sales' in role_name.lower():
            tags.append({'Key': 'BusinessUnit', 'Value': 'Sales'})
    
    # Apply tags to resource
    resource_arn = detail['responseElements'].get('resourceArn')
    if resource_arn and tags:
        apply_tags_to_resource(resource_arn, tags)
    
    return {'statusCode': 200}

def apply_tags_to_resource(resource_arn, tags):
    """Apply tags to AWS resource"""
    try:
        # Determine service and apply tags accordingly
        if ':ec2:' in resource_arn:
            ec2 = boto3.client('ec2')
            resource_id = resource_arn.split('/')[-1]
            ec2.create_tags(Resources=[resource_id], Tags=tags)
        elif ':s3:' in resource_arn:
            s3 = boto3.client('s3')
            bucket_name = resource_arn.split(':::')[-1]
            tag_set = [{'Key': tag['Key'], 'Value': tag['Value']} for tag in tags]
            s3.put_bucket_tagging(Bucket=bucket_name, Tagging={'TagSet': tag_set})
        # Add more services as needed
        
    except Exception as e:
        print(f"Error applying tags: {str(e)}")
'''
    
    # Create Lambda function for auto-tagging
    lambda_client = boto3.client('lambda')
    
    try:
        lambda_client.create_function(
            FunctionName='AutoTagResources',
            Runtime='python3.9',
            Role='arn:aws:iam::ACCOUNT:role/AutoTaggingRole',
            Handler='lambda_function.lambda_handler',
            Code={'ZipFile': lambda_code.encode()},
            Description='Automatically tag resources for cost attribution'
        )
        print("Created auto-tagging Lambda function")
    except Exception as e:
        print(f"Error creating Lambda function: {str(e)}")

def create_tag_compliance_monitor():
    """Create monitoring for tag compliance"""
    config_client = boto3.client('config')
    
    # Config rule for required tags
    config_rule = {
        'ConfigRuleName': 'required-tags-compliance',
        'Source': {
            'Owner': 'AWS',
            'SourceIdentifier': 'REQUIRED_TAGS'
        },
        'InputParameters': json.dumps({
            'requiredTagKeys': 'BusinessUnit,Environment,Project,Owner'
        })
    }
    
    try:
        config_client.put_config_rule(ConfigRule=config_rule)
        print("Created tag compliance Config rule")
    except Exception as e:
        print(f"Error creating Config rule: {str(e)}")
```

## Attribution Reporting and Analysis

### Cost Attribution Reports
```python
import boto3
import pandas as pd
from datetime import datetime, timedelta

def generate_attribution_reports():
    """Generate comprehensive cost attribution reports"""
    ce_client = boto3.client('ce')
    
    # Define time period
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    
    # Business Unit Attribution Report
    bu_response = ce_client.get_cost_and_usage(
        TimePeriod={'Start': start_date, 'End': end_date},
        Granularity='MONTHLY',
        Metrics=['BlendedCost'],
        GroupBy=[
            {'Type': 'COST_CATEGORY', 'Key': 'BusinessUnit'},
            {'Type': 'DIMENSION', 'Key': 'SERVICE'}
        ]
    )
    
    # Environment Attribution Report
    env_response = ce_client.get_cost_and_usage(
        TimePeriod={'Start': start_date, 'End': end_date},
        Granularity='MONTHLY',
        Metrics=['BlendedCost'],
        GroupBy=[
            {'Type': 'COST_CATEGORY', 'Key': 'Environment'},
            {'Type': 'TAG', 'Key': 'Application'}
        ]
    )
    
    # Process and format reports
    reports = {
        'business_unit_costs': process_cost_response(bu_response),
        'environment_costs': process_cost_response(env_response),
        'unallocated_costs': calculate_unallocated_costs(bu_response)
    }
    
    return reports

def process_cost_response(response):
    """Process Cost Explorer response into structured data"""
    processed_data = []
    
    for result in response['ResultsByTime']:
        time_period = result['TimePeriod']['Start']
        
        for group in result['Groups']:
            cost = float(group['Metrics']['BlendedCost']['Amount'])
            keys = group['Keys']
            
            processed_data.append({
                'time_period': time_period,
                'category': keys[0] if len(keys) > 0 else 'Unknown',
                'subcategory': keys[1] if len(keys) > 1 else 'Unknown',
                'cost': cost
            })
    
    return processed_data

def calculate_unallocated_costs(response):
    """Calculate costs that are not properly attributed"""
    total_cost = 0
    unallocated_cost = 0
    
    for result in response['ResultsByTime']:
        for group in result['Groups']:
            cost = float(group['Metrics']['BlendedCost']['Amount'])
            total_cost += cost
            
            # Check if cost is unallocated
            if 'Unallocated' in group['Keys'] or 'Unknown' in group['Keys']:
                unallocated_cost += cost
    
    return {
        'total_cost': total_cost,
        'unallocated_cost': unallocated_cost,
        'allocation_percentage': ((total_cost - unallocated_cost) / total_cost * 100) if total_cost > 0 else 0
    }
```

## Common Challenges and Solutions

### Challenge: Inconsistent Tagging Across Teams

**Solution**: Implement automated tagging where possible. Create tag governance policies and compliance monitoring. Provide training and tools to make tagging easier. Use AWS Config rules to enforce tagging requirements.

### Challenge: Complex Cost Allocation Requirements

**Solution**: Use AWS Cost Categories to implement complex allocation logic. Create hierarchical attribution structures. Use multiple attribution dimensions simultaneously. Implement custom allocation algorithms where needed.

### Challenge: Changing Business Structure

**Solution**: Design flexible attribution categories that can adapt to organizational changes. Use hierarchical structures that can be reorganized. Implement versioning for attribution rules. Create processes for updating categories based on business changes.

### Challenge: Attribution Coverage Gaps

**Solution**: Implement comprehensive monitoring of attribution coverage. Create processes for identifying and addressing unallocated costs. Use default categories for resources that don't fit standard patterns. Regular audits of attribution accuracy.

### Challenge: Stakeholder Alignment on Categories

**Solution**: Involve stakeholders in category design and validation. Create clear documentation and examples of attribution categories. Provide training on how categories support business objectives. Regular review and refinement based on stakeholder feedback.

## Related Resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/cost_monitor_usage_attribution.html">AWS Well-Architected Framework - Identify cost attribution categories</a></li>
    <li><a href="https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-categories.html">AWS Cost Categories</a></li>
    <li><a href="https://docs.aws.amazon.com/ARG/latest/userguide/welcome.html">AWS Resource Groups User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-alloc-tags.html">Cost Allocation Tags</a></li>
    <li><a href="https://aws.amazon.com/blogs/aws-cost-management/cost-optimization-pillar-aws-well-architected-framework/">Cost Optimization Pillar - AWS Well-Architected Framework</a></li>
    <li><a href="https://docs.aws.amazon.com/organizations/latest/userguide/orgs_introduction.html">AWS Organizations User Guide</a></li>
    <li><a href="https://aws.amazon.com/blogs/aws-cost-management/best-practices-for-tagging-aws-resources/">Best Practices for Tagging AWS Resources</a></li>
    <li><a href="https://docs.aws.amazon.com/cost-management/latest/userguide/ce-what-is.html">AWS Cost Explorer User Guide</a></li>
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
