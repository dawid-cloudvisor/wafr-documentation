#!/usr/bin/env python3
"""
Script to update the order of pillars in the navigation.
"""

import os
import re

# Define the new order of pillars
PILLAR_ORDER = {
    "security": 2,
    "reliability": 3,
    "cost-optimization": 4,
    "performance-efficiency": 5,
    "operational-excellence": 6,
    "sustainability": 7
}

def update_pillar_nav_order(pillar_dir, nav_order):
    """Update the nav_order in a pillar's index.md file."""
    file_path = f"./docs/{pillar_dir}/index.md"
    
    if not os.path.exists(file_path):
        print(f"Warning: {file_path} does not exist")
        return
    
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    # Update the nav_order in the front matter
    for i, line in enumerate(lines):
        if line.strip().startswith('nav_order:'):
            lines[i] = f'nav_order: {nav_order}\n'
            break
    
    with open(file_path, 'w') as f:
        f.writelines(lines)
    
    print(f"Updated nav_order to {nav_order} in {file_path}")

def main():
    """Main function to update all pillar nav orders."""
    for pillar, nav_order in PILLAR_ORDER.items():
        update_pillar_nav_order(pillar, nav_order)

if __name__ == "__main__":
    main()
