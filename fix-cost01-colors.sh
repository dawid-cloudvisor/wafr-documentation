#!/bin/bash

echo "Fixing COST01 colors to use green theme..."

# List of COST01-BP files to update
files=(
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
        echo "Updating $file..."
        
        # Add cost-optimization div wrapper after the pillar-header opening
        sed -i 's|<div class="pillar-header">|<div class="cost-optimization">\n<div class="pillar-header">|' "$file"
        
        # Close the cost-optimization div at the end before the last </div>
        sed -i '$s|</div>|</div>\n</div>|' "$file"
        
        echo "✓ Updated $file"
    else
        echo "⚠ File not found: $file"
    fi
done

echo "✓ All COST01 files updated with green color theme"
echo "The files now use the cost-optimization CSS class for proper green styling"
