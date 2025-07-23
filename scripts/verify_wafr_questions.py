#!/usr/bin/env python3
"""
Script to verify and update the AWS Well-Architected Framework questions.
"""

import os
import re
import sys
import requests
from bs4 import BeautifulSoup

# URL of the AWS Well-Architected Framework appendix
WAFR_URL = "https://docs.aws.amazon.com/wellarchitected/latest/framework/appendix.html"

def fetch_wafr_questions():
    """Fetch and parse the AWS Well-Architected Framework questions from the appendix."""
    try:
        print(f"Fetching questions from {WAFR_URL}...")
        response = requests.get(WAFR_URL)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Dictionary to store questions by pillar
        questions_by_pillar = {}
        
        # Find all h2 elements (pillar headings)
        h2_elements = soup.find_all('h2')
        
        for h2 in h2_elements:
            pillar_text = h2.get_text().strip()
            
            # Check if this h2 is a pillar heading
            if "pillar" in pillar_text.lower():
                # Extract pillar name
                pillar_name = pillar_text.split(" pillar")[0].strip()
                questions_by_pillar[pillar_name] = []
                
                # Find the next div containing questions
                next_element = h2.find_next()
                while next_element and next_element.name != 'h2':
                    if next_element.name == 'div' and 'variablelist' in next_element.get('class', []):
                        # Find all dt elements (question IDs and titles)
                        dt_elements = next_element.find_all('dt')
                        
                        for dt in dt_elements:
                            question_text = dt.get_text().strip()
                            # Extract question ID and title
                            match = re.match(r'([A-Z]+\d+):\s+(.*)', question_text)
                            if match:
                                question_id = match.group(1)
                                question_title = match.group(2)
                                questions_by_pillar[pillar_name].append({
                                    'id': question_id,
                                    'title': question_title
                                })
                    next_element = next_element.find_next()
        
        return questions_by_pillar
    
    except Exception as e:
        print(f"Error fetching WAFR questions: {e}")
        return None

def compare_with_hardcoded():
    """Compare fetched questions with our hardcoded ones."""
    # Define the mapping between pillar names in the AWS doc and our directory names
    pillar_mapping = {
        "Operational excellence": "operational-excellence",
        "Security": "security",
        "Reliability": "reliability",
        "Performance efficiency": "performance-efficiency",
        "Cost optimization": "cost-optimization",
        "Sustainability": "sustainability"
    }
    
    # Fetch questions from AWS
    aws_questions = fetch_wafr_questions()
    
    if not aws_questions:
        print("Failed to fetch questions from AWS. Exiting.")
        return
    
    # Print the counts for each pillar
    print("\nQuestion counts from AWS documentation:")
    for pillar, questions in aws_questions.items():
        print(f"{pillar}: {len(questions)} questions")
    
    # Check our local files
    print("\nChecking local files...")
    for aws_pillar, dir_name in pillar_mapping.items():
        if aws_pillar not in aws_questions:
            print(f"Warning: Pillar '{aws_pillar}' not found in AWS documentation")
            continue
        
        # Check if directory exists
        pillar_dir = f"./docs/{dir_name}"
        if not os.path.isdir(pillar_dir):
            print(f"Warning: Directory '{pillar_dir}' does not exist")
            continue
        
        # Count question files
        question_files = [f for f in os.listdir(pillar_dir) if f.endswith('.md') and f != 'index.md']
        print(f"{aws_pillar} ({dir_name}): {len(question_files)} local files, {len(aws_questions[aws_pillar])} in AWS doc")
        
        # Check for missing questions
        aws_question_ids = {q['id'] for q in aws_questions[aws_pillar]}
        local_question_ids = {f.split('.')[0] for f in question_files}
        
        missing_questions = aws_question_ids - local_question_ids
        if missing_questions:
            print(f"  Missing questions: {', '.join(sorted(missing_questions))}")
            
            # Get the full details of missing questions
            missing_details = [q for q in aws_questions[aws_pillar] if q['id'] in missing_questions]
            for q in missing_details:
                print(f"    {q['id']}: {q['title']}")
        
        extra_questions = local_question_ids - aws_question_ids
        if extra_questions:
            print(f"  Extra questions not in AWS doc: {', '.join(sorted(extra_questions))}")

def main():
    """Main function."""
    compare_with_hardcoded()

if __name__ == "__main__":
    main()
