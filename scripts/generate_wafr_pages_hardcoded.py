#!/usr/bin/env python3
"""
Script to generate Markdown files for AWS Well-Architected Framework questions using hardcoded data.
"""

import os

# Define the pillars and their questions
PILLARS = {
    "Operational Excellence": {
        "abbr": "OPS",
        "nav_order": 2,
        "questions": [
            {"id": "OPS01", "title": "How do you determine what your priorities are?"},
            {"id": "OPS02", "title": "How do you structure your organization to support your business outcomes?"},
            {"id": "OPS03", "title": "How does your organizational culture support your business outcomes?"},
            {"id": "OPS04", "title": "How do you design your workload so that you can understand its state?"},
            {"id": "OPS05", "title": "How do you reduce defects, ease remediation, and improve flow into production?"},
            {"id": "OPS06", "title": "How do you mitigate deployment risks?"},
            {"id": "OPS07", "title": "How do you know that you are ready to support a workload?"},
            {"id": "OPS08", "title": "How do you understand the health of your workload?"},
            {"id": "OPS09", "title": "How do you understand the health of your operations?"},
            {"id": "OPS10", "title": "How do you manage workload and operations events?"},
            {"id": "OPS11", "title": "How do you evolve operations?"}
        ]
    },
    "Security": {
        "abbr": "SEC",
        "nav_order": 3,
        "questions": [
            {"id": "SEC01", "title": "How do you securely operate your workload?"},
            {"id": "SEC02", "title": "How do you manage identities for people and machines?"},
            {"id": "SEC03", "title": "How do you manage permissions for people and machines?"},
            {"id": "SEC04", "title": "How do you detect and investigate security events?"},
            {"id": "SEC05", "title": "How do you protect your network resources?"},
            {"id": "SEC06", "title": "How do you protect your compute resources?"},
            {"id": "SEC07", "title": "How do you classify your data?"},
            {"id": "SEC08", "title": "How do you protect your data at rest?"},
            {"id": "SEC09", "title": "How do you protect your data in transit?"},
            {"id": "SEC10", "title": "How do you anticipate, respond to, and recover from incidents?"}
        ]
    },
    "Reliability": {
        "abbr": "REL",
        "nav_order": 4,
        "questions": [
            {"id": "REL01", "title": "How do you manage service quotas and constraints?"},
            {"id": "REL02", "title": "How do you plan your network topology?"},
            {"id": "REL03", "title": "How do you design your workload service architecture?"},
            {"id": "REL04", "title": "How do you design interactions in a distributed system to prevent failures?"},
            {"id": "REL05", "title": "How do you design interactions in a distributed system to mitigate or withstand failures?"},
            {"id": "REL06", "title": "How do you monitor workload resources?"},
            {"id": "REL07", "title": "How do you design your workload to adapt to changes in demand?"},
            {"id": "REL08", "title": "How do you implement change?"},
            {"id": "REL09", "title": "How do you back up data?"},
            {"id": "REL10", "title": "How do you use fault isolation to protect your workload?"},
            {"id": "REL11", "title": "How do you design your workload to withstand component failures?"},
            {"id": "REL12", "title": "How do you test reliability?"},
            {"id": "REL13", "title": "How do you plan for disaster recovery?"}
        ]
    },
    "Performance Efficiency": {
        "abbr": "PERF",
        "nav_order": 5,
        "questions": [
            {"id": "PERF01", "title": "How do you select the best performing architecture?"},
            {"id": "PERF02", "title": "How do you select your compute solution?"},
            {"id": "PERF03", "title": "How do you select your storage solution?"},
            {"id": "PERF04", "title": "How do you select your database solution?"},
            {"id": "PERF05", "title": "How do you configure your networking solution?"},
            {"id": "PERF06", "title": "How do you evolve your workload to take advantage of new releases?"},
            {"id": "PERF07", "title": "How do you monitor your resources to ensure they are performing?"},
            {"id": "PERF08", "title": "How do you use tradeoffs to improve performance?"}
        ]
    },
    "Cost Optimization": {
        "abbr": "COST",
        "nav_order": 6,
        "questions": [
            {"id": "COST01", "title": "How do you implement cloud financial management?"},
            {"id": "COST02", "title": "How do you govern usage?"},
            {"id": "COST03", "title": "How do you monitor usage and cost?"},
            {"id": "COST04", "title": "How do you decommission resources?"},
            {"id": "COST05", "title": "How do you evaluate cost when you select services?"},
            {"id": "COST06", "title": "How do you meet cost targets when you select resource type, size and number?"},
            {"id": "COST07", "title": "How do you use pricing models to reduce cost?"},
            {"id": "COST08", "title": "How do you plan for data transfer charges?"},
            {"id": "COST09", "title": "How do you manage demand, and supply resources?"},
            {"id": "COST10", "title": "How do you evaluate new services?"}
        ]
    },
    "Sustainability": {
        "abbr": "SUS",
        "nav_order": 7,
        "questions": [
            {"id": "SUS01", "title": "How do you select Regions to support your sustainability goals?"},
            {"id": "SUS02", "title": "How do you take advantage of user behavior patterns to support your sustainability goals?"},
            {"id": "SUS03", "title": "How do you take advantage of software and architecture patterns to support your sustainability goals?"},
            {"id": "SUS04", "title": "How do you take advantage of data access and usage patterns to support your sustainability goals?"},
            {"id": "SUS05", "title": "How do you take advantage of hardware patterns to support your sustainability goals?"},
            {"id": "SUS06", "title": "How do you take advantage of development and deployment process to support your sustainability goals?"}
        ]
    }
}

def generate_question_file(pillar, question, question_number):
    """Generate a Markdown file for a specific question."""
    pillar_dir = pillar.lower().replace(' ', '-')
    question_id = question['id']
    question_title = question['title']
    
    # Create directory if it doesn't exist
    os.makedirs(f"docs/{pillar_dir}", exist_ok=True)
    
    # Create file path
    file_path = f"docs/{pillar_dir}/{question_id}.md"
    
    # Create file content
    content = f"""---
title: {question_id} - {question_title}
layout: default
parent: {pillar}
nav_order: {question_number}
---

# {question_id}: {question_title}

*This page contains guidance for addressing this question from the AWS Well-Architected Framework.*

## Best Practices

*Add best practices for this question here.*

## Implementation Guidance

1. **Step 1**: Description of first implementation step.

2. **Step 2**: Description of second implementation step.

3. **Step 3**: Description of third implementation step.

## AWS Services to Consider

- **Service 1** - Description of how this service helps
- **Service 2** - Description of how this service helps
- **Service 3** - Description of how this service helps

## Related Resources

- [AWS Well-Architected Framework - {pillar} Pillar](https://docs.aws.amazon.com/wellarchitected/latest/{pillar_dir.replace('-', '')}-pillar/welcome.html)
- [Related Documentation Link 1](https://aws.amazon.com/)
- [Related Documentation Link 2](https://aws.amazon.com/)
"""
    
    # Write content to file
    with open(file_path, 'w') as f:
        f.write(content)
    
    print(f"Generated file: {file_path}")

def main():
    """Main function to generate all WAFR question pages."""
    print("Generating Markdown files for each question...")
    
    for pillar, data in PILLARS.items():
        questions = data["questions"]
        print(f"\nProcessing {pillar} pillar ({len(questions)} questions):")
        
        for i, question in enumerate(questions, 1):
            generate_question_file(pillar, question, i)
    
    print("\nDone! All question files have been generated.")

if __name__ == "__main__":
    main()
