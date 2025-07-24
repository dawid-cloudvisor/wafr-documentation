#!/usr/bin/env python3
"""
Script to fix relative links within pillar directories
"""

import os
import re

def fix_pillar_index_links(file_path, pillar_name):
    """Fix links in pillar index files to use relative paths"""
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Pattern to match pillar links that need fixing
    # This will match: href="SEC01.html", href="SEC01-BP01.html", etc.
    pattern = rf'href="({pillar_name}\d+(?:-BP\d+)?\.html)"'
    
    def replace_link(match):
        link = match.group(1)
        # Add ./ prefix for relative path
        new_link = './' + link
        return f'href="{new_link}"'
    
    # Replace all matches
    updated_content = re.sub(pattern, replace_link, content)
    
    # Write back if content changed
    if content != updated_content:
        with open(file_path, 'w') as f:
            f.write(updated_content)
        print(f"Fixed relative links in {file_path}")
        return True
    
    return False

def fix_pillar_question_links(file_path, pillar_name):
    """Fix links in pillar question files (like SEC01.md) to use relative paths"""
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Pattern to match best practice links that need fixing
    # This will match: href="SEC01-BP01.html", etc.
    pattern = rf'href="({pillar_name}\d+-BP\d+\.html)"'
    
    def replace_link(match):
        link = match.group(1)
        # Add ./ prefix for relative path
        new_link = './' + link
        return f'href="{new_link}"'
    
    # Replace all matches
    updated_content = re.sub(pattern, replace_link, content)
    
    # Write back if content changed
    if content != updated_content:
        with open(file_path, 'w') as f:
            f.write(updated_content)
        print(f"Fixed relative links in {file_path}")
        return True
    
    return False

def main():
    """Main function to fix all relative links"""
    
    # Define pillar mappings
    pillars = {
        'security': 'SEC',
        'reliability': 'REL',
        'cost-optimization': 'COST',
        'performance-efficiency': 'PERF',
        'operational-excellence': 'OPS',
        'sustainability': 'SUS'
    }
    
    files_updated = 0
    
    for pillar_dir, pillar_prefix in pillars.items():
        pillar_path = f'./docs/{pillar_dir}'
        
        if os.path.exists(pillar_path):
            # Fix index.md file
            index_file = os.path.join(pillar_path, 'index.md')
            if os.path.exists(index_file):
                if fix_pillar_index_links(index_file, pillar_prefix):
                    files_updated += 1
            
            # Fix question files (like SEC01.md, SEC02.md, etc.)
            for filename in os.listdir(pillar_path):
                if filename.endswith('.md') and filename != 'index.md':
                    file_path = os.path.join(pillar_path, filename)
                    if fix_pillar_question_links(file_path, pillar_prefix):
                        files_updated += 1
    
    print(f"Updated {files_updated} files total")

if __name__ == "__main__":
    main()
