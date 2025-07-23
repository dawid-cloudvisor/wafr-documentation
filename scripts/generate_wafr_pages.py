#!/usr/bin/env python3
"""
Script to generate Markdown files for AWS Well-Architected Framework questions.
This script creates a structured documentation based on the six pillars and their questions.
"""

import os
import re
import sys
import requests
from bs4 import BeautifulSoup

# Define the pillars and their abbreviations
PILLARS = {
    "Operational Excellence": {"abbr": "OPS", "nav_order": 2},
    "Security": {"abbr": "SEC", "nav_order": 3},
    "Reliability": {"abbr": "REL", "nav_order": 4},
    "Performance Efficiency": {"abbr": "PERF", "nav_order": 5},
    "Cost Optimization": {"abbr": "COST", "nav_order": 6},
    "Sustainability": {"abbr": "SUS", "nav_order": 7}
}

# URL of the AWS Well-Architected Framework appendix
WAFR_URL = "https://docs.aws.amazon.com/wellarchitected/latest/framework/appendix.html"

def fetch_wafr_questions():
    """Fetch and parse the AWS Well-Architected Framework questions from the appendix."""
    try:
        response = requests.get(WAFR_URL)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Dictionary to store questions by pillar
        questions_by_pillar = {pillar: [] for pillar in PILLARS.keys()}
        
        # Find all h2 elements (pillar headings)
        h2_elements = soup.find_all('h2')
        
        current_pillar = None
        
        for h2 in h2_elements:
            pillar_text = h2.get_text().strip()
            
            # Check if this h2 is a pillar heading
            for pillar in PILLARS.keys():
                if pillar in pillar_text:
                    current_pillar = pillar
                    break
            
            if current_pillar:
                # Find the next div containing questions
                questions_div = h2.find_next('div', class_='variablelist')
                if questions_div:
                    # Find all dt elements (question IDs and titles)
                    dt_elements = questions_div.find_all('dt')
                    
                    for dt in dt_elements:
                        question_text = dt.get_text().strip()
                        # Extract question ID and title
                        match = re.match(r'([A-Z]+\d+):\s+(.*)', question_text)
                        if match:
                            question_id = match.group(1)
                            question_title = match.group(2)
                            questions_by_pillar[current_pillar].append({
                                'id': question_id,
                                'title': question_title
                            })
        
        return questions_by_pillar
    
    except Exception as e:
        print(f"Error fetching WAFR questions: {e}")
        return None

def generate_question_file(pillar, question, question_number):
    """Generate a Markdown file for a specific question."""
    pillar_dir = pillar.lower().replace(' ', '-')
    question_id = question['id']
    question_title = question['title']
    
    # Create directory if it doesn't exist
    os.makedirs(f"docs/{pillar_dir}", exist_ok=True)
    
    # Create file path
    file_path = f"docs/{pillar_dir}/{question_id}.md"
    
    # Create file content
    content = f"""---
title: {question_id} - {question_title}
layout: default
parent: {pillar}
nav_order: {question_number}
---

# {question_id}: {question_title}

*This page contains guidance for addressing this question from the AWS Well-Architected Framework.*

## Best Practices

*Add best practices for this question here.*

## Implementation Guidance

1. **Step 1**: Description of first implementation step.

2. **Step 2**: Description of second implementation step.

3. **Step 3**: Description of third implementation step.

## AWS Services to Consider

- **Service 1** - Description of how this service helps
- **Service 2** - Description of how this service helps
- **Service 3** - Description of how this service helps

## Related Resources

- [AWS Well-Architected Framework - {pillar} Pillar](https://docs.aws.amazon.com/wellarchitected/latest/{pillar_dir.replace('-', '')}-pillar/welcome.html)
- [Related Documentation Link 1](https://aws.amazon.com/)
- [Related Documentation Link 2](https://aws.amazon.com/)
"""
    
    # Write content to file
    with open(file_path, 'w') as f:
        f.write(content)
    
    print(f"Generated file: {file_path}")

def main():
    """Main function to generate all WAFR question pages."""
    print("Fetching AWS Well-Architected Framework questions...")
    questions_by_pillar = fetch_wafr_questions()
    
    if not questions_by_pillar:
        print("Failed to fetch questions. Exiting.")
        sys.exit(1)
    
    print("Generating Markdown files for each question...")
    
    for pillar, questions in questions_by_pillar.items():
        print(f"\nProcessing {pillar} pillar ({len(questions)} questions):")
        
        for i, question in enumerate(questions, 1):
            generate_question_file(pillar, question, i)
    
    print("\nDone! All question files have been generated.")

if __name__ == "__main__":
    main()
