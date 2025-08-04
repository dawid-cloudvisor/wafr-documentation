#!/bin/bash

echo "Fixing all formatting issues in COST01 files..."

# List of all COST01 files
files=(
    "docs/cost-optimization/COST01.md"
    "docs/cost-optimization/COST01-BP01.md"
    "docs/cost-optimization/COST01-BP02.md"
    "docs/cost-optimization/COST01-BP03.md"
    "docs/cost-optimization/COST01-BP04.md"
    "docs/cost-optimization/COST01-BP05.md"
    "docs/cost-optimization/COST01-BP06.md"
    "docs/cost-optimization/COST01-BP07.md"
    "docs/cost-optimization/COST01-BP08.md"
    "docs/cost-optimization/COST01-BP09.md"
)

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "Fixing $file..."
        
        # Create a temporary file
        temp_file=$(mktemp)
        
        # Process the file line by line
        while IFS= read -r line; do
            echo "$line" >> "$temp_file"
            
            # If this line is a "### Challenge:" heading, add a blank line before the next line
            if [[ "$line" =~ ^###\ Challenge: ]]; then
                # Read the next line
                if IFS= read -r next_line; then
                    # If the next line starts with **Solution**, add a blank line
                    if [[ "$next_line" =~ ^\*\*Solution\*\*: ]]; then
                        echo "" >> "$temp_file"
                    fi
                    echo "$next_line" >> "$temp_file"
                fi
            fi
        done < "$file"
        
        # Replace the original file with the fixed version
        mv "$temp_file" "$file"
        
        echo "✓ Fixed $file"
    else
        echo "⚠ File not found: $file"
    fi
done

echo "✓ All formatting issues fixed!"
echo "Added blank lines between '### Challenge:' headings and '**Solution**:' text"
