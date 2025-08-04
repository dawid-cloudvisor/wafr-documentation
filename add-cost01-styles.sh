#!/bin/bash

echo "Adding inline CSS styles to all COST01-BP files..."

# CSS to add
css_styles='
<style>
.pillar-header {
  background-color: #e8f5e8;
  border-left: 5px solid #2d7d2d;
}

.pillar-header h1 {
  color: #2d7d2d;
}

.aws-service-content h4 {
  color: #2d7d2d;
}

.related-resources {
  background-color: #e8f5e8;
}

.related-resources h2 {
  color: #2d7d2d;
}
</style>'

# List of COST01-BP files to update (excluding BP01 which is already done)
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
        echo "Adding styles to $file..."
        
        # Add the CSS styles at the end of the file
        echo "$css_styles" >> "$file"
        
        echo "✓ Added styles to $file"
    else
        echo "⚠ File not found: $file"
    fi
done

echo "✓ All COST01-BP files updated with green color styles!"
echo "All files now have consistent Cost Optimization pillar styling"
