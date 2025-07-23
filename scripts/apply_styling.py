#!/usr/bin/env python3
"""
Script to apply custom styling to all question pages.
"""

import os
import re

def convert_to_styled_format(content):
    """Convert standard markdown to styled format with custom classes."""
    # Extract front matter
    front_matter_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if not front_matter_match:
        return content
    
    front_matter = front_matter_match.group(0)
    content_without_front_matter = content[len(front_matter):]
    
    # Extract title and description
    title_match = re.search(r'# ([A-Z]+\d+): (.*?)\n', content_without_front_matter)
    if not title_match:
        return content
    
    question_id = title_match.group(1)
    question_title = title_match.group(2)
    
    # Find the first paragraph after the title
    description_match = re.search(r'# [A-Z]+\d+: .*?\n\n(.*?)\n\n', content_without_front_matter, re.DOTALL)
    description = description_match.group(1) if description_match else "*This page contains guidance for addressing this question from the AWS Well-Architected Framework.*"
    
    # Create the new header
    new_header = f"""<div class="pillar-header">
  <h1>{question_id}: {question_title}</h1>
  <p>{description}</p>
</div>

"""
    
    # Replace the old header
    content_without_header = re.sub(r'# [A-Z]+\d+: .*?\n\n(.*?)\n\n', '', content_without_front_matter, 1, re.DOTALL)
    if not content_without_header:
        content_without_header = re.sub(r'# [A-Z]+\d+: .*?\n\n', '', content_without_front_matter, 1)
    
    # Style best practices
    styled_content = content_without_header
    
    # Replace best practices section
    best_practices_match = re.search(r'## Best Practices\n\n(.*?)(?=\n##|\Z)', styled_content, re.DOTALL)
    if best_practices_match:
        best_practices_content = best_practices_match.group(1)
        styled_best_practices = "## Best Practices\n\n"
        
        # Find all best practices
        practices = re.findall(r'### (.*?)\n(.*?)(?=\n###|\Z)', best_practices_content, re.DOTALL)
        if practices:
            for practice_title, practice_content in practices:
                styled_best_practices += f"""<div class="best-practice">
  <h4>{practice_title}</h4>
  <p>{practice_content.strip()}</p>
</div>

"""
        else:
            # If no ### headings, just wrap the whole content
            styled_best_practices += f"""<div class="best-practice">
  <h4>Best Practice</h4>
  <p>{best_practices_content.strip()}</p>
</div>

"""
        
        styled_content = styled_content.replace(best_practices_match.group(0), styled_best_practices)
    
    # Replace implementation guidance
    impl_match = re.search(r'## Implementation Guidance\n\n(.*?)(?=\n##|\Z)', styled_content, re.DOTALL)
    if impl_match:
        impl_content = impl_match.group(1)
        styled_impl = "## Implementation Guidance\n\n"
        
        # Find all implementation steps
        steps = re.findall(r'\d+\.\s+\*\*(.*?)\*\*:(.*?)(?=\n\d+\.|\Z)', impl_content, re.DOTALL)
        if steps:
            for i, (step_title, step_content) in enumerate(steps, 1):
                styled_impl += f"""<div class="implementation-step">
  <h4>{i}. {step_title}</h4>
  <p>{step_content.strip()}</p>
</div>

"""
        else:
            # If no numbered steps with bold titles, try to find numbered items
            steps = re.findall(r'(\d+\.\s+.*?)(?=\n\d+\.|\Z)', impl_content, re.DOTALL)
            if steps:
                for i, step_content in enumerate(steps, 1):
                    step_text = step_content.strip()
                    step_text = re.sub(r'^\d+\.\s+', '', step_text)
                    styled_impl += f"""<div class="implementation-step">
  <h4>Step {i}</h4>
  <p>{step_text}</p>
</div>

"""
            else:
                # If no structure found, just wrap the whole content
                styled_impl += f"""<div class="implementation-step">
  <h4>Implementation Guidance</h4>
  <p>{impl_content.strip()}</p>
</div>

"""
        
        styled_content = styled_content.replace(impl_match.group(0), styled_impl)
    
    # Replace AWS services section
    services_match = re.search(r'## AWS Services to Consider\n\n(.*?)(?=\n##|\Z)', styled_content, re.DOTALL)
    if services_match:
        services_content = services_match.group(1)
        styled_services = "## AWS Services to Consider\n\n"
        
        # Find all services
        services = re.findall(r'- \*\*(.*?)\*\* - (.*?)(?=\n-|\Z)', services_content, re.DOTALL)
        if services:
            for service_name, service_desc in services:
                styled_services += f"""<div class="aws-service">
  <div class="aws-service-content">
    <h4>{service_name}</h4>
    <p>{service_desc.strip()}</p>
  </div>
</div>

"""
        else:
            # If no structured services, try to find simple list items
            services = re.findall(r'- (.*?)(?=\n-|\Z)', services_content, re.DOTALL)
            if services:
                for service in services:
                    styled_services += f"""<div class="aws-service">
  <div class="aws-service-content">
    <h4>{service.strip()}</h4>
    <p>AWS service for this question.</p>
  </div>
</div>

"""
            else:
                # If no structure found, just add a placeholder
                styled_services += """<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Services</h4>
    <p>Add relevant AWS services for this question.</p>
  </div>
</div>

"""
        
        styled_content = styled_content.replace(services_match.group(0), styled_services)
    
    # Replace related resources section
    resources_match = re.search(r'## Related Resources\n\n(.*?)(?=\n##|\Z)', styled_content, re.DOTALL)
    if resources_match:
        resources_content = resources_match.group(1)
        styled_resources = """<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
"""
        
        # Find all resources
        resources = re.findall(r'- \[(.*?)\]\((.*?)\)', resources_content)
        if resources:
            for resource_name, resource_url in resources:
                styled_resources += f'    <li><a href="{resource_url}">{resource_name}</a></li>\n'
        else:
            # If no structured links, try to find simple list items
            resources = re.findall(r'- (.*?)(?=\n-|\Z)', resources_content, re.DOTALL)
            if resources:
                for resource in resources:
                    styled_resources += f'    <li>{resource.strip()}</li>\n'
            else:
                # If no structure found, just add a placeholder
                styled_resources += '    <li>Add related resources for this question.</li>\n'
        
        styled_resources += "  </ul>\n</div>"
        
        styled_content = styled_content.replace(resources_match.group(0), styled_resources)
    
    # Combine everything
    return front_matter + new_header + styled_content

def process_directory(directory):
    """Process all markdown files in a directory."""
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath) and filepath.endswith('.md') and not filename == 'index.md':
            with open(filepath, 'r') as file:
                content = file.read()
            
            styled_content = convert_to_styled_format(content)
            
            with open(filepath, 'w') as file:
                file.write(styled_content)
            
            print(f"Styled {filepath}")

def main():
    """Main function to process all pillar directories."""
    base_dir = './docs'
    pillars = [
        'operational-excellence',
        'security',
        'reliability',
        'performance-efficiency',
        'cost-optimization',
        'sustainability'
    ]
    
    for pillar in pillars:
        pillar_dir = os.path.join(base_dir, pillar)
        if os.path.isdir(pillar_dir):
            print(f"Processing {pillar} pillar...")
            process_directory(pillar_dir)

if __name__ == "__main__":
    main()
