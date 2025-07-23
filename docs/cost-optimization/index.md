---
title: Cost Optimization
layout: default
nav_order: 6
has_children: true
permalink: /docs/cost-optimization
---

# Cost Optimization Pillar

The cost optimization pillar focuses on avoiding unnecessary costs. Key topics include understanding and controlling where money is being spent, selecting the most appropriate and right number of resource types, analyzing spend over time, and scaling to meet business needs without overspending.

## Key Areas

The Cost Optimization pillar includes the following key areas:

- Practice Cloud Financial Management
- Expenditure and Usage Awareness
- Cost-Effective Resources
- Manage Demand and Supply Resources
- Optimize Over Time

## Questions

The AWS Well-Architected Framework provides a set of questions that allows you to review an existing or proposed architecture. It also provides a set of AWS best practices for each pillar.

{% for child in site.pages %}
  {% if child.parent == page.title %}
  - [{{ child.title }}]({{ child.url | absolute_url }})
  {% endif %}
{% endfor %}
