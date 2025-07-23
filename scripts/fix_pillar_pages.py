#!/usr/bin/env python3
"""
Script to fix pillar index pages.
"""

import os
import re

def fix_pillar_page(file_path, pillar_title):
    """Fix a pillar index page."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Replace {title} placeholder with actual pillar title
    content = content.replace('## AWS Services for {title}', f'## AWS Services for {pillar_title}')
    
    with open(file_path, 'w') as f:
        f.write(content)
    
    print(f"Fixed {file_path}")

def main():
    """Main function to fix all pillar index pages."""
    pillars = {
        "operational-excellence": "Operational Excellence",
        "security": "Security",
        "reliability": "Reliability",
        "performance-efficiency": "Performance Efficiency",
        "cost-optimization": "Cost Optimization",
        "sustainability": "Sustainability"
    }
    
    for pillar_dir, pillar_title in pillars.items():
        file_path = f"./docs/{pillar_dir}/index.md"
        if os.path.exists(file_path):
            fix_pillar_page(file_path, pillar_title)
        else:
            print(f"Warning: {file_path} does not exist")

if __name__ == "__main__":
    main()
