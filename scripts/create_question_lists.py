#!/usr/bin/env python3
"""
Script to create explicit question lists for each pillar.
"""

import os
import re

def get_questions_for_pillar(pillar_dir):
    """Get all questions for a pillar."""
    questions = []
    dir_path = f"./docs/{pillar_dir}"
    
    if not os.path.isdir(dir_path):
        return questions
    
    for filename in os.listdir(dir_path):
        if filename.endswith('.md') and filename != 'index.md':
            file_path = os.path.join(dir_path, filename)
            with open(file_path, 'r') as f:
                content = f.read()
                
                # Extract title from front matter
                title_match = re.search(r'title: (.*?)$', content, re.MULTILINE)
                if title_match:
                    title = title_match.group(1).strip()
                    question_id = filename.split('.')[0]
                    questions.append({
                        'id': question_id,
                        'title': title,
                        'filename': filename
                    })
    
    # Sort questions by ID
    questions.sort(key=lambda q: q['id'])
    return questions

def update_pillar_index(pillar_dir, pillar_title, questions):
    """Update a pillar index page with explicit question list."""
    file_path = f"./docs/{pillar_dir}/index.md"
    
    if not os.path.exists(file_path):
        print(f"Warning: {file_path} does not exist")
        return
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Find the questions section
    questions_section_match = re.search(r'## Questions\s+.*?<div class="question-cards">.*?</div>', content, re.DOTALL)
    
    if not questions_section_match:
        print(f"Warning: Could not find questions section in {file_path}")
        return
    
    # Create new questions section
    new_questions_section = """## Questions

The AWS Well-Architected Framework provides a set of questions that allows you to review an existing or proposed architecture. It also provides a set of AWS best practices for each pillar.

<div class="question-cards">
"""
    
    # Add each question
    for question in questions:
        new_questions_section += f"""  <div class="question-card">
    <h3>{question['title']}</h3>
    <a href="./{question['filename'].replace('.md', '')}">View details →</a>
  </div>
"""
    
    new_questions_section += "</div>"
    
    # Replace the old questions section
    new_content = content.replace(questions_section_match.group(0), new_questions_section)
    
    with open(file_path, 'w') as f:
        f.write(new_content)
    
    print(f"Updated {file_path} with {len(questions)} questions")

def main():
    """Main function to update all pillar index pages."""
    pillars = {
        "operational-excellence": "Operational Excellence",
        "security": "Security",
        "reliability": "Reliability",
        "performance-efficiency": "Performance Efficiency",
        "cost-optimization": "Cost Optimization",
        "sustainability": "Sustainability"
    }
    
    for pillar_dir, pillar_title in pillars.items():
        questions = get_questions_for_pillar(pillar_dir)
        print(f"Found {len(questions)} questions for {pillar_title}")
        update_pillar_index(pillar_dir, pillar_title, questions)

if __name__ == "__main__":
    main()
