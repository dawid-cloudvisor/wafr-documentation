#!/usr/bin/env python3
"""
Script to update pillar index pages with custom styling.
"""

import os

# Define the pillars and their descriptions
PILLARS = {
    "operational-excellence": {
        "title": "Operational Excellence",
        "description": "The operational excellence pillar focuses on running and monitoring systems to deliver business value, and continually improving processes and procedures.",
        "key_areas": [
            "Organization - How teams are structured and how they collaborate",
            "Prepare - Design for operations and understand workload health",
            "Operate - Understand workload health and achieve operational success",
            "Evolve - Learn, share, and continuously improve"
        ],
        "services": [
            {"name": "AWS CloudFormation", "description": "Provides a common language to model and provision AWS and third-party resources in your cloud environment."},
            {"name": "AWS Config", "description": "Enables you to assess, audit, and evaluate the configurations of your AWS resources."},
            {"name": "AWS CloudTrail", "description": "Enables governance, compliance, operational auditing, and risk auditing of your AWS account."},
            {"name": "Amazon CloudWatch", "description": "Monitors your AWS resources and the applications you run on AWS in real time."},
            {"name": "AWS Systems Manager", "description": "Gives you visibility and control of your infrastructure on AWS."}
        ],
        "resources": [
            {"name": "AWS Well-Architected Framework - Operational Excellence Pillar", "url": "https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/welcome.html"},
            {"name": "AWS Well-Architected", "url": "https://aws.amazon.com/architecture/well-architected/"},
            {"name": "DevOps on AWS", "url": "https://aws.amazon.com/devops/"}
        ]
    },
    "security": {
        "title": "Security",
        "description": "The security pillar focuses on protecting information and systems. Key topics include confidentiality and integrity of data, identifying and managing who can do what with privilege management, protecting systems, and establishing controls to detect security events.",
        "key_areas": [
            "Security Foundations - Implementing a strong identity foundation",
            "Identity and Access Management - Ensuring only authorized and authenticated users can access your resources",
            "Detection - Implementing monitoring, alerting, and audit actions",
            "Infrastructure Protection - Protecting systems and services within your workload",
            "Data Protection - Classifying data and implementing controls to protect it",
            "Incident Response - Responding to and mitigating the potential impact of security incidents"
        ],
        "services": [
            {"name": "AWS Identity and Access Management (IAM)", "description": "Enables you to manage access to AWS services and resources securely."},
            {"name": "Amazon GuardDuty", "description": "Provides intelligent threat detection for your AWS accounts and workloads."},
            {"name": "AWS Security Hub", "description": "Gives you a comprehensive view of your security alerts and security posture across your AWS accounts."},
            {"name": "AWS Key Management Service (KMS)", "description": "Makes it easy for you to create and manage cryptographic keys and control their use."},
            {"name": "AWS Shield", "description": "Provides protection against DDoS attacks for applications running on AWS."}
        ],
        "resources": [
            {"name": "AWS Well-Architected Framework - Security Pillar", "url": "https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html"},
            {"name": "AWS Security Documentation", "url": "https://docs.aws.amazon.com/security/"},
            {"name": "AWS Security Blog", "url": "https://aws.amazon.com/blogs/security/"}
        ]
    },
    "reliability": {
        "title": "Reliability",
        "description": "The reliability pillar focuses on ensuring a workload performs its intended function correctly and consistently when it's expected to. This includes the ability to operate and test the workload through its total lifecycle.",
        "key_areas": [
            "Foundations - Managing service quotas and network topology",
            "Workload Architecture - Designing distributed systems that withstand failures",
            "Change Management - Monitoring resources and implementing controlled changes",
            "Failure Management - Backing up data, designing for fault isolation, and planning for disaster recovery"
        ],
        "services": [
            {"name": "Amazon CloudWatch", "description": "Monitors your AWS resources and the applications you run on AWS in real time."},
            {"name": "AWS Auto Scaling", "description": "Monitors your applications and automatically adjusts capacity to maintain steady, predictable performance."},
            {"name": "Amazon RDS", "description": "Makes it easy to set up, operate, and scale a relational database in the cloud with high availability."},
            {"name": "AWS Elastic Disaster Recovery", "description": "Minimizes downtime and data loss with fast, reliable recovery of on-premises and cloud-based applications."},
            {"name": "AWS Backup", "description": "Centrally manages and automates backups across AWS services."}
        ],
        "resources": [
            {"name": "AWS Well-Architected Framework - Reliability Pillar", "url": "https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html"},
            {"name": "Reliability on AWS", "url": "https://aws.amazon.com/reliability/"},
            {"name": "AWS Architecture Blog", "url": "https://aws.amazon.com/blogs/architecture/"}
        ]
    },
    "performance-efficiency": {
        "title": "Performance Efficiency",
        "description": "The performance efficiency pillar focuses on using IT and computing resources efficiently. Key topics include selecting the right resource types and sizes based on workload requirements, monitoring performance, and making informed decisions to maintain efficiency as business needs evolve.",
        "key_areas": [
            "Selection - Choosing the right compute, storage, database, and networking solutions",
            "Review - Continuously evaluating new services and technologies",
            "Monitoring - Ensuring resources are performing as expected",
            "Tradeoffs - Using caching, partitioning, and other techniques to improve performance"
        ],
        "services": [
            {"name": "Amazon EC2", "description": "Provides resizable compute capacity in the cloud with a wide selection of instance types."},
            {"name": "Amazon S3", "description": "Object storage built to store and retrieve any amount of data from anywhere."},
            {"name": "Amazon RDS", "description": "Makes it easy to set up, operate, and scale a relational database in the cloud."},
            {"name": "Amazon DynamoDB", "description": "Fast and flexible NoSQL database service for any scale."},
            {"name": "Amazon CloudFront", "description": "Fast content delivery network (CDN) service that securely delivers data, videos, applications, and APIs."}
        ],
        "resources": [
            {"name": "AWS Well-Architected Framework - Performance Efficiency Pillar", "url": "https://docs.aws.amazon.com/wellarchitected/latest/performance-efficiency-pillar/welcome.html"},
            {"name": "AWS Performance Efficiency", "url": "https://aws.amazon.com/architecture/well-architected/performance-efficiency/"},
            {"name": "AWS Compute Blog", "url": "https://aws.amazon.com/blogs/compute/"}
        ]
    },
    "cost-optimization": {
        "title": "Cost Optimization",
        "description": "The cost optimization pillar focuses on avoiding unnecessary costs. Key topics include understanding and controlling where money is being spent, selecting the most appropriate and right number of resource types, analyzing spend over time, and scaling to meet business needs without overspending.",
        "key_areas": [
            "Practice Cloud Financial Management - Implementing organizational processes for cost management",
            "Expenditure and Usage Awareness - Increasing visibility and accountability",
            "Cost-Effective Resources - Using the appropriate services and resources for your workload",
            "Manage Demand and Supply Resources - Scaling resources to match business requirements",
            "Optimize Over Time - Continuously reviewing and refining your cost optimization approach"
        ],
        "services": [
            {"name": "AWS Cost Explorer", "description": "Visualize, understand, and manage your AWS costs and usage over time."},
            {"name": "AWS Budgets", "description": "Set custom cost and usage budgets that alert you when your budget thresholds are exceeded."},
            {"name": "AWS Cost and Usage Report", "description": "Access comprehensive cost and usage data for your AWS account."},
            {"name": "AWS Trusted Advisor", "description": "Provides recommendations that help you follow AWS best practices for cost optimization."},
            {"name": "AWS Compute Optimizer", "description": "Recommends optimal AWS resources for your workloads to reduce costs."}
        ],
        "resources": [
            {"name": "AWS Well-Architected Framework - Cost Optimization Pillar", "url": "https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/welcome.html"},
            {"name": "AWS Cost Management", "url": "https://aws.amazon.com/aws-cost-management/"},
            {"name": "AWS Cost Optimization Hub", "url": "https://aws.amazon.com/aws-cost-management/cost-optimization-hub/"}
        ]
    },
    "sustainability": {
        "title": "Sustainability",
        "description": "The sustainability pillar focuses on minimizing the environmental impacts of running cloud workloads. Key topics include a shared responsibility model for sustainability, understanding impact, and maximizing utilization to minimize required resources and reduce downstream impacts.",
        "key_areas": [
            "Region Selection - Choosing Regions with lower carbon footprints",
            "User Behavior Patterns - Aligning user needs with sustainable practices",
            "Software and Architecture Patterns - Designing efficient applications",
            "Data Patterns - Implementing lifecycle policies and storage tiering",
            "Hardware Patterns - Using the minimum amount of hardware to meet your needs",
            "Development and Deployment Process - Optimizing development and testing environments"
        ],
        "services": [
            {"name": "AWS Customer Carbon Footprint Tool", "description": "Provides visibility into the carbon emissions associated with your AWS usage."},
            {"name": "Amazon EC2 Auto Scaling", "description": "Helps ensure you have the correct number of instances available to handle your application load."},
            {"name": "Amazon S3 Lifecycle Configurations", "description": "Automates moving objects to more cost-effective storage classes or deleting them."},
            {"name": "AWS Graviton Processors", "description": "Deliver better price performance for your cloud workloads with lower energy consumption."},
            {"name": "AWS Compute Optimizer", "description": "Helps you identify idle and underutilized resources."}
        ],
        "resources": [
            {"name": "AWS Well-Architected Framework - Sustainability Pillar", "url": "https://docs.aws.amazon.com/wellarchitected/latest/sustainability-pillar/welcome.html"},
            {"name": "AWS Sustainability", "url": "https://sustainability.aboutamazon.com/environment/the-cloud"},
            {"name": "AWS and Sustainability", "url": "https://aws.amazon.com/about-aws/sustainability/"}
        ]
    }
}

def generate_pillar_index(pillar_dir, data):
    """Generate a styled index page for a pillar."""
    title = data["title"]
    description = data["description"]
    key_areas = data["key_areas"]
    services = data["services"]
    resources = data["resources"]
    
    # Create file path
    file_path = f"docs/{pillar_dir}/index.md"
    
    # Create file content
    content = f"""---
title: {title}
layout: default
nav_order: {PILLARS[pillar_dir].get("nav_order", 2)}
has_children: true
permalink: /docs/{pillar_dir}
---

<div class="pillar-header">
  <h1>{title} Pillar</h1>
  <p>{description}</p>
</div>

The {title} pillar includes the ability to support development and run workloads effectively, gain insight into their operations, and to continuously improve supporting processes and procedures to deliver business value.

## Key Areas

The {title} pillar includes the following key areas:

"""

    # Add key areas
    for area in key_areas:
        content += f"- **{area.split(' - ')[0]}** - {area.split(' - ')[1] if ' - ' in area else ''}\n"
    
    content += """
## Questions

The AWS Well-Architected Framework provides a set of questions that allows you to review an existing or proposed architecture. It also provides a set of AWS best practices for each pillar.

<div class="question-cards">
  {% for child in site.pages %}
    {% if child.parent == page.title %}
      <div class="question-card">
        <h3>{{ child.title }}</h3>
        <a href="{{ child.url | absolute_url }}">View details →</a>
      </div>
    {% endif %}
  {% endfor %}
</div>

## AWS Services for {title}

"""

    # Add services
    for service in services:
        content += f"""<div class="aws-service">
  <div class="aws-service-content">
    <h4>{service["name"]}</h4>
    <p>{service["description"]}</p>
  </div>
</div>

"""

    # Add related resources
    content += """<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
"""
    
    for resource in resources:
        content += f'    <li><a href="{resource["url"]}">{resource["name"]}</a></li>\n'
    
    content += "  </ul>\n</div>"
    
    # Write content to file
    with open(file_path, 'w') as f:
        f.write(content)
    
    print(f"Generated index file: {file_path}")

def main():
    """Main function to update all pillar index pages."""
    print("Updating pillar index pages with custom styling...")
    
    for pillar_dir, data in PILLARS.items():
        generate_pillar_index(pillar_dir, data)
    
    print("\nDone! All pillar index pages have been updated.")

if __name__ == "__main__":
    main()
