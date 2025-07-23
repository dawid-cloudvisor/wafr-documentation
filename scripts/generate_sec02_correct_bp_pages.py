#!/usr/bin/env python3
"""
Script to generate the correct best practice pages for SEC02.
"""

import os

# Define the correct best practices for SEC02
BEST_PRACTICES = [
    {
        "id": "SEC02-BP01",
        "title": "Use strong sign-in mechanisms",
        "description": "Enforce minimum password length, and educate your users to avoid common or reused passwords. Enforce multi-factor authentication (MFA) with software or hardware mechanisms to provide an additional layer of verification.",
        "nav_order": 1
    },
    {
        "id": "SEC02-BP02",
        "title": "Use temporary credentials",
        "description": "Require identities to dynamically acquire temporary credentials. For workforce identities, use AWS IAM Identity Center, or a federation with IAM roles to access AWS accounts. For machine identities, require the use of IAM roles instead of IAM users with long-term access keys.",
        "nav_order": 2
    },
    {
        "id": "SEC02-BP03",
        "title": "Store and use secrets securely",
        "description": "For workforce and machine identities that require secrets, such as passwords to third-party applications, store them with automatic rotation using the latest industry standards in a specialized service.",
        "nav_order": 3
    },
    {
        "id": "SEC02-BP04",
        "title": "Rely on a centralized identity provider",
        "description": "For workforce identities (your employees, contractors, and partners), rely on an identity provider that enables you to manage identities in a centralized place. This makes it easier to manage access across multiple applications and services because you are creating, managing, and revoking access from a single location.",
        "nav_order": 4
    },
    {
        "id": "SEC02-BP05",
        "title": "Audit and rotate credentials periodically",
        "description": "When you cannot rely on temporary credentials and need to use long-term credentials, audit the credentials to ensure that the defined controls (such as MFA) are enforced, rotated regularly, and have the appropriate level of access.",
        "nav_order": 5
    },
    {
        "id": "SEC02-BP06",
        "title": "Employ user groups and attributes",
        "description": "As the number of users you manage grows, you need to reduce the overhead of managing access. Place users with common security requirements in groups defined by your identity provider, and put mechanisms in place to ensure that user attributes that may be used for access control (such as department or location) are correct and updated.",
        "nav_order": 6
    }
]

# Template for best practice pages
TEMPLATE = """---
title: {id} - {title}
layout: default
parent: SEC02 - How do you manage identities for people and machines?
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
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/sec-02.html">SEC02: How do you manage identities for people and machines?</a></li>
    <li><a href="https://aws.amazon.com/identity/">AWS Identity Solutions</a></li>
  </ul>
</div>
"""

def main():
    """Generate best practice pages for SEC02."""
    for bp in BEST_PRACTICES:
        # Skip BP01 and BP04 as they already have detailed content
        if bp['id'] in ['SEC02-BP01', 'SEC02-BP04']:
            print(f"Skipping {bp['id']} as it already has detailed content")
            continue
            
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
