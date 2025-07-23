#!/usr/bin/env python3
"""
Script to fix template code in pillar index pages.
"""

import os
import re

def fix_pillar_page(file_path):
    """Fix a pillar index page by removing leftover template code."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Remove leftover template code
    content = re.sub(r'</div>\s+\{% endif %\}\s+\{% endfor %\}\s+</div>', '</div>', content)
    
    with open(file_path, 'w') as f:
        f.write(content)
    
    print(f"Fixed template code in {file_path}")

def main():
    """Main function to fix all pillar index pages."""
    pillars = [
        "operational-excellence",
        "security",
        "reliability",
        "performance-efficiency",
        "cost-optimization",
        "sustainability"
    ]
    
    for pillar_dir in pillars:
        file_path = f"./docs/{pillar_dir}/index.md"
        if os.path.exists(file_path):
            fix_pillar_page(file_path)
        else:
            print(f"Warning: {file_path} does not exist")

if __name__ == "__main__":
    main()
