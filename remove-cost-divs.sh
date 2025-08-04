#!/bin/bash

echo "Removing cost-optimization div wrappers from COST01 files..."

# List of COST01-BP files to update
files=(
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
        echo "Updating $file..."
        
        # Remove the opening cost-optimization div wrapper
        sed -i 's|<div class="cost-optimization">||' "$file"
        
        # Remove the closing div at the end (only the extra one we added)
        sed -i '$s|</div>||' "$file"
        
        echo "✓ Updated $file"
    else
        echo "⚠ File not found: $file"
    fi
done

echo "✓ All cost-optimization div wrappers removed"
