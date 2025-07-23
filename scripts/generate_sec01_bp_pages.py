#!/usr/bin/env python3
"""
Script to generate the remaining best practice pages for SEC01.
"""

import os

# Define the remaining best practices for SEC01
BEST_PRACTICES = [
    {
        "id": "SEC01-BP05",
        "title": "Reduce security management scope",
        "description": "Reduce security management scope by minimizing the number of security tooling and processes that you need to maintain. For example, if you have multiple security tools that provide similar capabilities, evaluate if there is a compelling reason to maintain multiple tools.",
        "nav_order": 5
    },
    {
        "id": "SEC01-BP06",
        "title": "Automate deployment of standard security controls",
        "description": "Automate testing and validation of all security controls. For example, scan items such as machine images and infrastructure as code templates for security vulnerabilities, irregularities, and drift from an established baseline before they are deployed. Tools and services, such as Amazon Inspector, can be used to automate host and network vulnerability assessments.",
        "nav_order": 6
    },
    {
        "id": "SEC01-BP07",
        "title": "Identify threats and prioritize mitigations using a threat model",
        "description": "Use a threat model to identify and maintain a list of security threats. Prioritize your threats and adjust your security controls to prevent, detect, and respond. Revisit and reprioritize regularly.",
        "nav_order": 7
    },
    {
        "id": "SEC01-BP08",
        "title": "Evaluate and implement new security services and features regularly",
        "description": "Evaluate and implement security services and features from AWS and AWS Partners that allow you to evolve the security posture of your workload.",
        "nav_order": 8
    }
]

# Template for best practice pages
TEMPLATE = """---
title: {id} - {title}
layout: default
parent: SEC01 - How do you securely operate your workload?
grand_parent: Security
nav_order: {nav_order}
---

<div class="pillar-header">
  <h1>{id}: {title}</h1>
  <p>{description}</p>
</div>

## Implementation guidance

### Key steps for implementing this best practice:

1. **Step 1**: Description of first implementation step.

2. **Step 2**: Description of second implementation step.

3. **Step 3**: Description of third implementation step.

4. **Step 4**: Description of fourth implementation step.

## AWS services to consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Service 1</h4>
    <p>Description of how this service helps with this best practice.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Service 2</h4>
    <p>Description of how this service helps with this best practice.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Service 3</h4>
    <p>Description of how this service helps with this best practice.</p>
  </div>
</div>

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html">AWS Well-Architected Framework - Security Pillar</a></li>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/sec-01.html">SEC01: How do you securely operate your workload?</a></li>
    <li><a href="https://aws.amazon.com/security/">AWS Security</a></li>
  </ul>
</div>
"""

def main():
    """Generate best practice pages for SEC01."""
    for bp in BEST_PRACTICES:
        file_path = f"./docs/security/{bp['id']}.md"
        content = TEMPLATE.format(
            id=bp["id"],
            title=bp["title"],
            description=bp["description"],
            nav_order=bp["nav_order"]
        )
        
        with open(file_path, "w") as f:
            f.write(content)
        
        print(f"Generated {file_path}")

if __name__ == "__main__":
    main()
