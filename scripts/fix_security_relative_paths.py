#!/usr/bin/env python3
"""
Script to fix security links to use explicit security/ path
"""

import os
import re

def fix_security_links(file_path):
    """Fix security links to use explicit security/ path"""
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Pattern to match SEC links that need fixing
    # This will match: href="./SEC01.html" or href="./SEC01-BP01.html" etc.
    pattern = r'href="(\./SEC\d+(?:-BP\d+)?\.html)"'
    
    def replace_link(match):
        link = match.group(1)
        # Replace ./SEC with ./security/SEC
        new_link = link.replace('./SEC', './security/SEC')
        return f'href="{new_link}"'
    
    # Replace all matches
    updated_content = re.sub(pattern, replace_link, content)
    
    # Write back if content changed
    if content != updated_content:
        with open(file_path, 'w') as f:
            f.write(updated_content)
        print(f"Fixed security links in {file_path}")
        return True
    
    return False

def main():
    """Main function to fix security links"""
    
    security_index = './docs/security/index.md'
    
    if os.path.exists(security_index):
        if fix_security_links(security_index):
            print("Updated security index with explicit paths")
        else:
            print("No changes needed")
    else:
        print("Security index file not found")

if __name__ == "__main__":
    main()
