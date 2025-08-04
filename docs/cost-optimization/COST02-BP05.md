---
title: COST02-BP05 - Implement cost controls
layout: default
parent: COST02 - How do you govern usage?
grand_parent: Cost Optimization
nav_order: 5
---

<div class="pillar-header">
  <h1>COST02-BP05: Implement cost controls</h1>
  <p>Implement cost controls that prevent overspending and ensure resources are used efficiently. Cost controls should be proactive, automated where possible, and aligned with your organization's risk tolerance and business objectives. Effective cost controls balance the need for governance with the flexibility required for innovation and business agility.</p>
</div>

## Implementation guidance

Cost controls are essential mechanisms that prevent unauthorized spending, enforce budget limits, and ensure resources are used efficiently. They should be implemented as part of a comprehensive governance framework that balances control with operational flexibility.

### Cost Control Strategy

**Preventive Controls**: Implement controls that prevent inappropriate spending before it occurs, such as service limits, approval workflows, and automated resource termination.

**Detective Controls**: Deploy monitoring and alerting systems that identify cost anomalies, budget overruns, and policy violations in near real-time.

**Corrective Controls**: Establish automated and manual processes to address cost issues when they are detected, including resource termination, access restriction, and escalation procedures.

**Risk-Based Approach**: Implement controls that are proportionate to risk levels, with stricter controls for high-cost activities and more flexibility for low-risk scenarios.

### Types of Cost Controls

**Budget Controls**: Set spending limits at various levels (account, project, team) with automated alerts and actions when thresholds are approached or exceeded.

**Resource Limits**: Implement service quotas and limits that prevent the creation of expensive resources or excessive resource quantities.

**Approval Workflows**: Require approval for high-cost activities, resource types, or spending above certain thresholds.

**Automated Shutdowns**: Implement automated systems that terminate or scale down resources based on usage patterns, schedules, or cost thresholds.

### Control Implementation Levels

**Account Level**: Controls applied at the AWS account level, such as service control policies, account spending limits, and consolidated billing controls.

**Resource Level**: Controls applied to specific resources or resource types, such as instance size limits, storage quotas, and network bandwidth restrictions.

**User Level**: Controls applied to individual users or roles, such as spending limits, resource creation permissions, and approval requirements.

**Time-Based Controls**: Controls that vary based on time factors, such as business hours, project phases, or seasonal requirements.

## AWS Services to Consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Budgets</h4>
    <p>Create custom budgets with automated alerts and actions. Set up cost, usage, and reservation budgets with thresholds that trigger notifications or automated responses.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Service Control Policies (SCPs)</h4>
    <p>Implement preventive guardrails that restrict actions across accounts in your organization. Use SCPs to prevent the creation of expensive resources or services.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Cost Anomaly Detection</h4>
    <p>Automatically detect unusual spending patterns using machine learning. Receive alerts when costs deviate significantly from expected patterns.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Lambda</h4>
    <p>Implement automated cost control actions such as resource termination, scaling, or notification. Use Lambda functions to respond to budget alerts and cost anomalies.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS CloudWatch</h4>
    <p>Monitor resource utilization and performance metrics that correlate with costs. Set up alarms that trigger cost control actions based on usage patterns.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Auto Scaling</h4>
    <p>Automatically adjust resource capacity based on demand and cost considerations. Implement scaling policies that optimize both performance and cost.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Systems Manager</h4>
    <p>Automate operational tasks including cost control activities. Use Systems Manager to implement scheduled shutdowns, resource optimization, and compliance enforcement.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Config</h4>
    <p>Monitor resource configurations and automatically remediate non-compliant resources. Use Config rules to enforce cost-related compliance requirements.</p>
  </div>
</div>

## Implementation Steps

### 1. Assess Current Cost Patterns
- Analyze historical spending data to identify patterns and trends
- Identify high-cost resources, services, and usage patterns
- Assess current cost control mechanisms and their effectiveness
- Document cost-related risks and vulnerabilities

### 2. Define Cost Control Policies
- Establish spending limits and thresholds for different organizational levels
- Define approval requirements for high-cost activities
- Create resource usage policies and restrictions
- Document exception handling procedures

### 3. Implement Preventive Controls
- Set up service quotas and limits to prevent excessive resource creation
- Implement service control policies to restrict high-cost services
- Configure approval workflows for expensive resource types
- Set up automated resource tagging for cost allocation

### 4. Deploy Detective Controls
- Configure budget alerts and notifications
- Set up cost anomaly detection and monitoring
- Implement real-time cost monitoring dashboards
- Create automated reporting for cost trends and violations

### 5. Establish Corrective Controls
- Implement automated responses to budget overruns
- Set up resource termination and scaling automation
- Create escalation procedures for cost violations
- Establish manual intervention processes for complex scenarios

### 6. Monitor and Optimize
- Regularly review control effectiveness and adjust thresholds
- Analyze false positives and tune detection algorithms
- Gather feedback from users and stakeholders
- Continuously improve control mechanisms based on lessons learned

## Cost Control Mechanisms

### Budget-Based Controls

**Account Budgets**: Set overall spending limits for AWS accounts with alerts at 50%, 80%, and 100% of budget.

**Project Budgets**: Create project-specific budgets that track spending against allocated amounts with automated notifications to project managers.

**Service Budgets**: Monitor spending on specific AWS services to identify cost drivers and prevent runaway costs.

**Time-Based Budgets**: Implement monthly, quarterly, or annual budgets with appropriate alert thresholds and actions.

### Resource-Based Controls

**Instance Size Limits**: Restrict the creation of large, expensive instance types without approval, allowing only cost-effective sizes for most use cases.

**Storage Quotas**: Implement limits on storage usage and require approval for large storage allocations or premium storage types.

**Network Limits**: Control data transfer costs by monitoring and limiting bandwidth usage, especially for cross-region and internet traffic.

**Service Restrictions**: Use service control policies to prevent the use of expensive or unnecessary services in certain accounts or environments.

### Time-Based Controls

**Scheduled Shutdowns**: Automatically shut down development and testing resources during non-business hours to reduce costs.

**Lifecycle Management**: Implement automated lifecycle policies for storage, backups, and other resources to optimize costs over time.

**Temporary Resource Limits**: Set time-limited permissions for expensive resources, requiring renewal or approval for extended use.

**Seasonal Adjustments**: Adjust cost controls based on business cycles, such as increased limits during peak seasons.

### Approval-Based Controls

**High-Cost Approvals**: Require manager approval for resource requests above certain cost thresholds.

**Reserved Instance Approvals**: Implement approval workflows for Reserved Instance and Savings Plan purchases to ensure they align with usage patterns.

**Architecture Reviews**: Require architecture reviews for new applications or significant changes that could impact costs.

**Exception Approvals**: Create formal processes for approving exceptions to standard cost control policies.

## Automated Cost Control Examples

### Budget Alert Automation
```python
# Example Lambda function for budget alert response
import boto3
import json

def lambda_handler(event, context):
    # Parse budget alert
    message = json.loads(event['Records'][0]['Sns']['Message'])
    account_id = message['AccountId']
    budget_name = message['BudgetName']
    threshold_type = message['ThresholdType']
    
    if threshold_type == 'PERCENTAGE' and message['ActualAmount'] > 90:
        # Take corrective action for budget overrun
        ec2 = boto3.client('ec2')
        
        # Stop non-production instances
        instances = ec2.describe_instances(
            Filters=[
                {'Name': 'tag:Environment', 'Values': ['dev', 'test']},
                {'Name': 'instance-state-name', 'Values': ['running']}
            ]
        )
        
        for reservation in instances['Reservations']:
            for instance in reservation['Instances']:
                ec2.stop_instances(InstanceIds=[instance['InstanceId']])
                
        # Send notification
        sns = boto3.client('sns')
        sns.publish(
            TopicArn='arn:aws:sns:region:account:cost-alerts',
            Message=f'Budget {budget_name} exceeded 90%. Non-production instances stopped.',
            Subject='Automated Cost Control Action'
        )
    
    return {'statusCode': 200}
```

### Resource Lifecycle Management
```python
# Example for automated resource cleanup
import boto3
from datetime import datetime, timedelta

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    
    # Find instances older than 30 days without production tag
    cutoff_date = datetime.now() - timedelta(days=30)
    
    instances = ec2.describe_instances(
        Filters=[
            {'Name': 'instance-state-name', 'Values': ['running', 'stopped']},
            {'Name': 'tag:Environment', 'Values': ['dev', 'test', 'sandbox']}
        ]
    )
    
    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            launch_time = instance['LaunchTime'].replace(tzinfo=None)
            
            if launch_time < cutoff_date:
                # Check for keep-alive tag
                keep_alive = False
                for tag in instance.get('Tags', []):
                    if tag['Key'] == 'KeepAlive' and tag['Value'].lower() == 'true':
                        keep_alive = True
                        break
                
                if not keep_alive:
                    # Terminate old instances
                    ec2.terminate_instances(InstanceIds=[instance['InstanceId']])
                    
                    # Log action
                    print(f"Terminated instance {instance['InstanceId']} - older than 30 days")
    
    return {'statusCode': 200}
```

### Cost Anomaly Response
```python
# Example for responding to cost anomalies
import boto3
import json

def lambda_handler(event, context):
    # Parse cost anomaly detection alert
    message = json.loads(event['Records'][0]['Sns']['Message'])
    anomaly_details = message['AnomalyDetails']
    
    if anomaly_details['TotalImpact'] > 1000:  # $1000 threshold
        # Investigate high-impact anomalies
        ce = boto3.client('ce')
        
        # Get detailed cost data for the anomaly period
        response = ce.get_cost_and_usage(
            TimePeriod={
                'Start': anomaly_details['StartDate'],
                'End': anomaly_details['EndDate']
            },
            Granularity='DAILY',
            Metrics=['BlendedCost'],
            GroupBy=[
                {'Type': 'DIMENSION', 'Key': 'SERVICE'},
                {'Type': 'DIMENSION', 'Key': 'USAGE_TYPE'}
            ]
        )
        
        # Identify top cost drivers
        cost_drivers = []
        for result in response['ResultsByTime']:
            for group in result['Groups']:
                cost = float(group['Metrics']['BlendedCost']['Amount'])
                if cost > 100:  # Focus on significant costs
                    cost_drivers.append({
                        'service': group['Keys'][0],
                        'usage_type': group['Keys'][1],
                        'cost': cost
                    })
        
        # Send detailed alert
        sns = boto3.client('sns')
        message_body = f"Cost anomaly detected with impact ${anomaly_details['TotalImpact']}\n"
        message_body += "Top cost drivers:\n"
        
        for driver in sorted(cost_drivers, key=lambda x: x['cost'], reverse=True)[:5]:
            message_body += f"- {driver['service']}: ${driver['cost']:.2f}\n"
        
        sns.publish(
            TopicArn='arn:aws:sns:region:account:cost-anomaly-alerts',
            Message=message_body,
            Subject='High-Impact Cost Anomaly Detected'
        )
    
    return {'statusCode': 200}
```

## Cost Control Best Practices

### Graduated Controls
- Implement different control levels based on risk and cost impact
- Use more restrictive controls for high-cost resources and activities
- Provide more flexibility for low-cost, low-risk activities
- Adjust controls based on user experience and trust levels

### Automation First
- Automate cost controls wherever possible to reduce manual overhead
- Use event-driven automation to respond quickly to cost issues
- Implement self-healing systems that can resolve common cost problems
- Provide manual override capabilities for exceptional circumstances

### User Experience Focus
- Design controls that minimize friction for legitimate activities
- Provide clear feedback and guidance when controls are triggered
- Offer self-service options for routine requests and approvals
- Create educational resources to help users understand and work with controls

### Continuous Improvement
- Regularly review control effectiveness and adjust thresholds
- Analyze false positives and tune detection algorithms
- Gather feedback from users and stakeholders
- Evolve controls based on changing business needs and usage patterns

## Monitoring and Reporting

### Control Effectiveness Metrics
- **Control Trigger Rate**: Frequency of control activations and their outcomes
- **False Positive Rate**: Percentage of control triggers that were inappropriate
- **Cost Savings**: Measurable cost savings achieved through control implementation
- **User Satisfaction**: Feedback from users on control impact and effectiveness

### Cost Control Dashboards
- Real-time view of budget status and spending trends
- Control activation history and outcomes
- Cost anomaly detection and investigation status
- Resource utilization and optimization opportunities

### Regular Reporting
- Monthly cost control effectiveness reports
- Quarterly review of control policies and thresholds
- Annual assessment of control ROI and business impact
- Ad-hoc reports for specific cost events or investigations

## Common Challenges and Solutions

### Challenge: Balancing Control and Flexibility

**Solution**: Implement graduated controls based on risk levels. Use approval workflows rather than blanket restrictions. Provide self-service options for routine activities. Create clear exception processes for legitimate needs.

### Challenge: False Positives and Alert Fatigue

**Solution**: Tune control thresholds based on historical data and feedback. Implement intelligent alerting that considers context and patterns. Use machine learning to improve detection accuracy. Provide clear escalation and feedback mechanisms.

### Challenge: User Resistance to Controls

**Solution**: Involve users in control design and implementation. Provide clear rationale for controls and their business benefits. Offer training and support for working with controls. Create incentives for compliance and cost optimization.

### Challenge: Keeping Controls Current

**Solution**: Implement regular review cycles for control policies and thresholds. Monitor AWS service changes and pricing updates. Use automated tools to identify control gaps or obsolete rules. Create feedback loops from control effectiveness data.

### Challenge: Complex Multi-Account Environments

**Solution**: Use AWS Organizations and service control policies for consistent control implementation. Implement centralized monitoring and reporting across accounts. Create standardized control templates and automation. Establish clear governance processes for control management.

## Integration with Business Processes

### Budget Planning Integration
- Align cost controls with annual budget planning processes
- Use control data to inform budget allocations and forecasts
- Create feedback loops between control effectiveness and budget accuracy
- Integrate control thresholds with approved budget levels

### Project Management Integration
- Implement project-specific cost controls and budgets
- Integrate cost control status into project reporting and reviews
- Create project lifecycle controls that adjust based on project phases
- Align cost controls with project approval and governance processes

### Financial Reporting Integration
- Include cost control effectiveness in financial reporting
- Use control data to support cost allocation and chargeback processes
- Create variance reports that include control impact analysis
- Integrate control metrics into financial performance dashboards

## Related Resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/cost_govern_usage_controls.html">AWS Well-Architected Framework - Implement cost controls</a></li>
    <li><a href="https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html">Managing Costs with AWS Budgets</a></li>
    <li><a href="https://docs.aws.amazon.com/cost-management/latest/userguide/getting-started-ad.html">AWS Cost Anomaly Detection</a></li>
    <li><a href="https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html">Service Control Policies (SCPs)</a></li>
    <li><a href="https://aws.amazon.com/blogs/aws-cost-management/cost-optimization-pillar-aws-well-architected-framework/">Cost Optimization Pillar - AWS Well-Architected Framework</a></li>
    <li><a href="https://docs.aws.amazon.com/general/latest/gr/aws_service_limits.html">AWS Service Quotas</a></li>
    <li><a href="https://aws.amazon.com/blogs/aws-cost-management/automate-cost-optimization-with-aws-budgets-actions/">Automate Cost Optimization with AWS Budgets Actions</a></li>
    <li><a href="https://docs.aws.amazon.com/lambda/latest/dg/welcome.html">AWS Lambda Developer Guide</a></li>
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
