#!/bin/bash

echo "Fixing encoding issues in COST01 files..."

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
        echo "Fixing encoding in $file..."
        
        # Replace problematic characters with standard ASCII equivalents
        sed -i 's/—/--/g' "$file"  # em-dash to double hyphen
        sed -i 's/–/-/g' "$file"   # en-dash to hyphen
        sed -i 's/"/"/g' "$file"   # left double quote
        sed -i 's/"/"/g' "$file"   # right double quote
        sed -i "s/'/'/g" "$file"   # left single quote
        sed -i "s/'/'/g" "$file"   # right single quote
        sed -i 's/…/.../g' "$file" # ellipsis to three dots
        
        echo "✓ Fixed encoding in $file"
    else
        echo "⚠ File not found: $file"
    fi
done

echo "✓ All encoding issues fixed!"
echo "Replaced special Unicode characters with standard ASCII equivalents"
