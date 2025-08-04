#!/bin/bash

echo "Fixing custom domain configuration for wafr.cloudvisor.eu..."

# 1. Ensure CNAME file exists
echo "wafr.cloudvisor.eu" > CNAME
echo "✓ Created CNAME file"

# 2. Check if _config.yml has correct URL
if grep -q "url: https://wafr.cloudvisor.eu" _config.yml; then
    echo "✓ _config.yml URL is correct"
else
    echo "⚠ Please manually update _config.yml URL to: https://wafr.cloudvisor.eu"
fi

# 3. Ensure assets directory structure is correct
mkdir -p assets/images assets/css assets/js
echo "✓ Asset directories verified"

# 4. Copy favicon if it exists in root
if [ -f "favicon.ico" ]; then
    cp favicon.ico assets/images/
    echo "✓ Favicon copied to assets/images/"
fi

# 5. Check for any hardcoded URLs
echo "Checking for hardcoded URLs..."
if grep -r "dawid-cloudvisor.github.io" . --exclude-dir=.git --exclude-dir=vendor --exclude-dir=.bundle 2>/dev/null; then
    echo "⚠ Found hardcoded URLs that need to be updated"
else
    echo "✓ No hardcoded URLs found"
fi

# 6. Commit and push changes
echo "Committing changes..."
git add .
git commit -m "Fix custom domain configuration for wafr.cloudvisor.eu"
git push origin main

echo "✓ Changes committed and pushed"
echo ""
echo "Next steps:"
echo "1. Wait 5-10 minutes for GitHub Pages to rebuild"
echo "2. Check https://wafr.cloudvisor.eu"
echo "3. If still having issues, check GitHub Pages settings in repository"
echo "4. Ensure DNS is properly configured for wafr.cloudvisor.eu"
