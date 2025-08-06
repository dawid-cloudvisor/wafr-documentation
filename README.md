# AWS Well-Architected Framework Documentation

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-brightgreen)](https://wafr.cloudvisor.eu)
[![Jekyll](https://img.shields.io/badge/Jekyll-4.3.2-red)](https://jekyllrb.com/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

A comprehensive, interactive documentation site for the AWS Well-Architected Framework, featuring detailed implementation guidance, code examples, and best practices for all six pillars of well-architected design.

## 🌟 Features

- **Complete Framework Coverage**: All 6 pillars with detailed questions and best practices
- **Interactive Design**: Expandable accordion sections for easy navigation
- **Practical Implementation**: Real-world code examples and automation frameworks
- **Responsive Layout**: Mobile-friendly design using Just the Docs theme
- **Search Functionality**: Built-in search across all documentation
- **Live Examples**: Python, TypeScript, and YAML code samples
- **Best Practice Guidance**: Detailed implementation steps and common challenges

## 📚 Documentation Structure

### Six Well-Architected Pillars

1. **🔧 Operational Excellence** - How you support development and run workloads effectively
2. **🔒 Security** - How you protect information, systems, and assets
3. **⚡ Reliability** - How workloads perform their intended functions correctly and consistently
4. **🚀 Performance Efficiency** - How you use computing resources efficiently
5. **💰 Cost Optimization** - How you avoid unnecessary costs and optimize spending
6. **🌱 Sustainability** - How you minimize environmental impacts of running cloud workloads

### Content Organization

Each pillar contains:
- **Main Overview**: Pillar principles and key concepts
- **Framework Questions**: All official AWS Well-Architected questions
- **Best Practices**: Detailed implementation guidance (BP01, BP02, etc.)
- **Code Examples**: Practical automation and monitoring frameworks
- **AWS Services**: Relevant services and implementation patterns
- **Common Challenges**: Solutions to frequent implementation issues

## 🚀 Live Site

Visit the live documentation at: **[wafr.cloudvisor.eu](https://wafr.cloudvisor.eu)**

## 🛠 Local Development

### Prerequisites

- Ruby 2.7+ with development headers
- RubyGems
- GCC and Make (for native extensions)
- Git

### Quick Start

```bash
# Clone the repository
git clone https://github.com/your-org/wafr-documentation-gh-pages.git
cd wafr-documentation-gh-pages

# Install dependencies
bundle install

# Serve locally with live reload
bundle exec jekyll serve --livereload

# Open browser to http://localhost:4000
```

### Development Commands

```bash
# Build the site
bundle exec jekyll build

# Serve with drafts
bundle exec jekyll serve --drafts

# Serve on different port
bundle exec jekyll serve --port 4001

# Clean build artifacts
bundle exec jekyll clean
```

## 📖 Content Highlights

### Comprehensive Implementation Frameworks

- **Cost Optimization**: Complete automation frameworks for cost monitoring, analysis, and optimization
- **Security**: Advanced security patterns, compliance frameworks, and threat modeling
- **Reliability**: Disaster recovery, fault tolerance, and monitoring implementations
- **Performance**: Auto-scaling, caching strategies, and performance optimization
- **Operational Excellence**: Infrastructure as Code, CI/CD pipelines, and operational metrics
- **Sustainability**: Green computing practices and resource optimization

### Real-World Code Examples

- **Python Frameworks**: Complete classes for AWS service automation
- **Infrastructure as Code**: CloudFormation and CDK examples
- **Monitoring Solutions**: CloudWatch dashboards and alerting
- **Cost Management**: Automated cost analysis and optimization tools
- **Security Automation**: Compliance checking and security monitoring

### Interactive Features

- **Accordion Navigation**: Expandable sections for easy content discovery
- **Search Integration**: Find specific topics across all documentation
- **Mobile Responsive**: Optimized for all device sizes
- **Syntax Highlighting**: Code examples with proper formatting
- **Cross-References**: Linked related topics and best practices

## 🏗 Architecture

### Technology Stack

- **Static Site Generator**: Jekyll 4.3.2
- **Theme**: Just the Docs (customized)
- **Hosting**: GitHub Pages
- **Domain**: Custom domain with SSL
- **Search**: Lunr.js integration
- **Styling**: SCSS with custom variables
- **JavaScript**: Vanilla JS for interactions

### File Structure

```
├── docs/                          # Main documentation content
│   ├── cost-optimization/         # Cost Optimization pillar
│   ├── security/                  # Security pillar  
│   ├── reliability/               # Reliability pillar
│   ├── performance-efficiency/    # Performance Efficiency pillar
│   ├── operational-excellence/    # Operational Excellence pillar
│   └── sustainability/            # Sustainability pillar
├── assets/                        # Static assets
│   ├── css/                       # Custom stylesheets
│   ├── js/                        # JavaScript files
│   └── images/                    # Images and icons
├── _includes/                     # Jekyll includes
├── _layouts/                      # Jekyll layouts
├── _config.yml                    # Jekyll configuration
└── README.md                      # This file
```

## 🎨 Customization

### Theme Customization

The site uses a customized version of Just the Docs with:
- **Custom Color Schemes**: Pillar-specific color themes
- **Enhanced Navigation**: Accordion-style expandable sections
- **Improved Typography**: Better readability and code formatting
- **Mobile Optimization**: Responsive design improvements

### Adding Content

1. **Create New Pages**: Add Markdown files in appropriate pillar directories
2. **Front Matter**: Use proper YAML front matter for navigation
3. **Code Examples**: Include practical implementation examples
4. **Cross-References**: Link to related best practices and services

Example front matter:
```yaml
---
title: Your Best Practice Title
layout: default
parent: COST01 - How do you implement cloud financial management?
grand_parent: Cost Optimization
nav_order: 1.1
---
```

## 🤝 Contributing

We welcome contributions to improve the documentation! Here's how you can help:

### Types of Contributions

- **Content Updates**: Improve existing documentation
- **New Examples**: Add practical code examples and use cases
- **Bug Fixes**: Fix typos, broken links, or formatting issues
- **Feature Enhancements**: Improve site functionality or user experience

### Contribution Process

1. **Fork the Repository**: Create your own fork
2. **Create Feature Branch**: `git checkout -b feature/your-improvement`
3. **Make Changes**: Update documentation or add new content
4. **Test Locally**: Verify changes work correctly
5. **Submit Pull Request**: Describe your changes and their benefits

### Content Guidelines

- **Accuracy**: Ensure all AWS service information is current
- **Clarity**: Write clear, actionable guidance
- **Examples**: Include practical, working code examples
- **Consistency**: Follow existing formatting and style patterns
- **Attribution**: Credit sources and maintain proper licensing

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🏢 About Cloudvisor

This documentation is maintained by [Cloudvisor](https://cloudvisor.eu), a cloud consulting company specializing in AWS Well-Architected implementations and cloud optimization strategies.

## 📞 Support

- **Issues**: Report bugs or request features via [GitHub Issues](https://github.com/your-org/wafr-documentation-gh-pages/issues)
- **Discussions**: Join conversations in [GitHub Discussions](https://github.com/your-org/wafr-documentation-gh-pages/discussions)
- **Website**: Visit [wafr.cloudvisor.eu](https://wafr.cloudvisor.eu) for the live documentation

## 🔗 Related Resources

- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [AWS Well-Architected Tool](https://aws.amazon.com/well-architected-tool/)
- [Just the Docs Theme](https://just-the-docs.github.io/just-the-docs/)
- [Jekyll Documentation](https://jekyllrb.com/docs/)

---

**⭐ Star this repository if you find it helpful!**
