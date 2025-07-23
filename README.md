# AWS Well-Architected Framework Documentation

This repository contains documentation for the AWS Well-Architected Framework, organized by pillars and questions. It uses the [Just the Docs](https://just-the-docs.github.io/just-the-docs/) theme for Jekyll to create a clean, responsive documentation site.

## Overview

The AWS Well-Architected Framework helps cloud architects build secure, high-performing, resilient, and efficient infrastructure for their applications and workloads. This documentation site organizes the framework's guidance by its six pillars:

1. Operational Excellence
2. Security
3. Reliability
4. Performance Efficiency
5. Cost Optimization
6. Sustainability

Each pillar section contains detailed documentation organized by the specific questions from the AWS Well-Architected Framework.

## Local Development

### Prerequisites

- Ruby version 2.5.0 or higher
- RubyGems
- GCC and Make

### Setup

1. Install Jekyll and Bundler:
   ```
   gem install jekyll bundler
   ```

2. Install dependencies:
   ```
   bundle install
   ```

3. Run the Jekyll site locally:
   ```
   bundle exec jekyll serve
   ```

4. Open your browser to `http://localhost:4000`

## Generating Documentation

This repository includes a Python script to generate Markdown files for all questions in the AWS Well-Architected Framework:

```
python3 ./scripts/generate_wafr_pages.py
```

This script will:
1. Fetch the latest questions from the AWS Well-Architected Framework appendix
2. Generate a Markdown file for each question, organized by pillar
3. Place the files in the appropriate directory structure

## Customizing the Documentation

### Adding Content

1. Create or edit Markdown files in the `docs/` directory
2. Follow the front matter format for Just the Docs:
   ```yaml
   ---
   title: Your Page Title
   layout: default
   parent: Parent Page Title
   nav_order: 1
   ---
   ```

### Configuration

Edit the `_config.yml` file to customize the site settings:

- `title`: The title of your site
- `description`: A description of your site
- `url`: The URL where your site will be hosted
- `aux_links`: Additional links to display in the upper right corner

## Deployment

This site is automatically deployed to GitHub Pages when changes are pushed to the main branch.

## License

This project is licensed under the terms specified in the [LICENSE](LICENSE) file.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
