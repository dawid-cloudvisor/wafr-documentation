#!/bin/bash

echo "Checking and fixing formatting issues in COST01 files..."

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
        echo "Checking $file..."
        
        # Check for lines where bold text immediately follows a heading without a blank line
        if grep -n "^### .*$" "$file" | while read line; do
            line_num=$(echo "$line" | cut -d: -f1)
            next_line_num=$((line_num + 1))
            next_line=$(sed -n "${next_line_num}p" "$file")
            
            if [[ "$next_line" =~ ^\*\*.*\*\*: ]]; then
                echo "  ⚠ Formatting issue found at line $line_num in $file"
                echo "    Heading: $(echo "$line" | cut -d: -f2-)"
                echo "    Next line: $next_line"
                return 1
            fi
        done; then
            echo "  ✓ No formatting issues found in $file"
        else
            echo "  ⚠ Found formatting issues in $file"
        fi
    else
        echo "  ⚠ File not found: $file"
    fi
done

echo ""
echo "Manual review recommended for any files with formatting issues."
echo "Look for patterns where headings (###) are immediately followed by bold text (**text**:)"
echo "without a blank line in between."
