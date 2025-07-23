# Setup Instructions for AWS Well-Architected Framework Documentation

This document provides step-by-step instructions for setting up and populating the AWS Well-Architected Framework documentation site.

## Repository Structure

We've created the following structure:

```
wafr-documentation-gh-pages/
├── _config.yml                 # Site configuration
├── index.md                    # Home page
├── docs/                       # Documentation directory
│   ├── operational-excellence/ # Operational Excellence pillar
│   ├── security/               # Security pillar
│   ├── reliability/            # Reliability pillar
│   ├── performance-efficiency/ # Performance Efficiency pillar
│   ├── cost-optimization/      # Cost Optimization pillar
│   ├── sustainability/         # Sustainability pillar
│   └── nav-structure.md        # Navigation structure overview
├── scripts/                    # Utility scripts
│   └── generate_wafr_pages.py  # Script to generate question pages
└── .github/                    # GitHub configuration
    └── workflows/              # GitHub Actions workflows
        └── pages.yml           # Workflow for GitHub Pages deployment
```

## Next Steps

1. **Install Required Dependencies**

   To run the Python script for generating question pages, you'll need to install the required dependencies:

   ```bash
   pip install requests beautifulsoup4
   ```

2. **Generate Question Pages**

   Run the Python script to generate pages for all questions in the AWS Well-Architected Framework:

   ```bash
   python3 ./scripts/generate_wafr_pages.py
   ```

3. **Customize Content**

   Review and customize the generated content for each question. The script creates template pages that need to be filled with detailed information about:
   - Best practices
   - Implementation guidance
   - AWS services to consider
   - Related resources

4. **Test Locally**

   If you have Jekyll installed, you can test the site locally:

   ```bash
   bundle install
   bundle exec jekyll serve
   ```

   Then open your browser to `http://localhost:4000`

5. **Commit and Push**

   Commit your changes and push to GitHub:

   ```bash
   git add .
   git commit -m "Initial setup of AWS Well-Architected Framework documentation"
   git push origin main
   ```

6. **Enable GitHub Pages**

   In your GitHub repository settings, enable GitHub Pages with the source set to "GitHub Actions".

## Customization Options

- **Site Title and Description**: Edit `_config.yml` to change the site title and description.
- **Navigation Order**: Adjust the `nav_order` value in the front matter of each page to change the navigation order.
- **Theme Customization**: See the [Just the Docs documentation](https://just-the-docs.github.io/just-the-docs/docs/customization/) for theme customization options.

## Adding Content

When adding new content, follow these guidelines:

1. Create a new Markdown file in the appropriate directory.
2. Include front matter with title, layout, parent, and nav_order.
3. Use the existing question pages as templates for formatting and structure.

## Maintenance

Regularly update the content to reflect the latest AWS Well-Architected Framework guidance. The AWS Well-Architected Framework is updated periodically, so you should review and update your documentation accordingly.
