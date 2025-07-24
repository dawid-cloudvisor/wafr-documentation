#!/usr/bin/env python3
"""
Script to fix security links to include proper paths and .html extensions
"""

import os
import re

def fix_security_links(file_path):
    """Fix security links in a file"""
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Pattern to match SEC links that need fixing
    # This will match: href="./SEC01" or href="./SEC01-BP01" etc.
    pattern = r'href="(\./SEC\d+(?:-BP\d+)?)"'
    
    def replace_link(match):
        link = match.group(1)
        # Remove the ./ prefix and add .html extension
        new_link = link[2:] + '.html'
        return f'href="{new_link}"'
    
    # Replace all matches
    updated_content = re.sub(pattern, replace_link, content)
    
    # Write back if content changed
    if content != updated_content:
        with open(file_path, 'w') as f:
            f.write(updated_content)
        print(f"Fixed links in {file_path}")
        return True
    
    return False

def main():
    """Main function to fix all security links"""
    
    security_dir = './docs/security'
    files_updated = 0
    
    # Process all markdown files in the security directory
    for filename in os.listdir(security_dir):
        if filename.endswith('.md'):
            file_path = os.path.join(security_dir, filename)
            if fix_security_links(file_path):
                files_updated += 1
    
    print(f"Updated {files_updated} files")

if __name__ == "__main__":
    main()
