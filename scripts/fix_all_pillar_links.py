#!/usr/bin/env python3
"""
Script to fix all pillar links to include proper .html extensions
"""

import os
import re

def fix_pillar_links(file_path):
    """Fix pillar links in a file"""
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Pattern to match pillar links that need fixing
    # This will match: href="./SEC01", href="./REL01", href="./COST01", etc.
    pattern = r'href="(\./[A-Z]+\d+(?:-BP\d+)?)"'
    
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
    """Main function to fix all pillar links"""
    
    docs_dir = './docs'
    files_updated = 0
    
    # Process all markdown files in all pillar directories
    for root, dirs, files in os.walk(docs_dir):
        for filename in files:
            if filename.endswith('.md'):
                file_path = os.path.join(root, filename)
                if fix_pillar_links(file_path):
                    files_updated += 1
    
    print(f"Updated {files_updated} files total")

if __name__ == "__main__":
    main()
