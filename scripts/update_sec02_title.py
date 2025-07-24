#!/usr/bin/env python3
"""
Script to update SEC02 title from 'identities' to 'authentication'.
"""

import os
import re

def update_file(file_path):
    """Update the SEC02 title in a file."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Replace the title in different formats
    updated_content = content.replace(
        "SEC02 - How do you manage identities for people and machines?",
        "SEC02 - How do you manage authentication for people and machines?"
    )
    updated_content = updated_content.replace(
        "SEC02: How do you manage identities for people and machines?",
        "SEC02: How do you manage authentication for people and machines?"
    )
    
    if content != updated_content:
        with open(file_path, 'w') as f:
            f.write(updated_content)
        print(f"Updated {file_path}")
    else:
        print(f"No changes needed in {file_path}")

def main():
    """Main function to update all relevant files."""
    # List of files to update
    files_to_update = [
        "./docs/security/SEC02.md",
        "./docs/security/SEC02-BP01.md",
        "./docs/security/SEC02-BP02.md",
        "./docs/security/SEC02-BP03.md",
        "./docs/security/SEC02-BP04.md",
        "./docs/security/SEC02-BP05.md",
        "./docs/security/SEC02-BP06.md",
        "./docs/security/index.md"
    ]
    
    for file_path in files_to_update:
        if os.path.exists(file_path):
            update_file(file_path)
        else:
            print(f"Warning: {file_path} does not exist")

if __name__ == "__main__":
    main()
