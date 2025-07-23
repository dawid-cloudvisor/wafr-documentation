#!/bin/bash

# Cleanup script for the WAFR documentation repository

echo "Starting cleanup..."

# Remove Python virtual environment
echo "Removing Python virtual environment..."
rm -rf wafr_venv/

# Remove temporary and development files
echo "Removing temporary and development files..."
rm -f COMPLETED_TASKS.md
rm -f CUSTOMIZATION_SUMMARY.md
rm -f SETUP_INSTRUCTIONS.md

# Clean up scripts directory - keep only essential scripts
echo "Cleaning up scripts directory..."
cd scripts/

# Keep these essential scripts
KEEP_SCRIPTS=(
  "update_pillar_order.py"
  "apply_styling.py"
  "generate_wafr_pages_updated.py"
)

# Remove all scripts except the ones we want to keep
for script in *.py; do
  keep=false
  for keep_script in "${KEEP_SCRIPTS[@]}"; do
    if [ "$script" == "$keep_script" ]; then
      keep=true
      break
    fi
  done
  
  if [ "$keep" == false ]; then
    echo "Removing $script..."
    rm -f "$script"
  else
    echo "Keeping $script..."
  fi
done

cd ..

# Remove old documentation that's been migrated
echo "Removing old documentation..."
rm -rf Docs/

# Remove any Python cache files
echo "Removing Python cache files..."
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
find . -type f -name "*.pyo" -delete
find . -type f -name "*.pyd" -delete

echo "Cleanup complete!"
