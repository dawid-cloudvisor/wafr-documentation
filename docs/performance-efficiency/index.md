---
title: Performance Efficiency
layout: default
nav_order: 5
has_children: true
permalink: /docs/performance-efficiency
---

# Performance Efficiency Pillar

The performance efficiency pillar focuses on using IT and computing resources efficiently. Key topics include selecting the right resource types and sizes based on workload requirements, monitoring performance, and making informed decisions to maintain efficiency as business needs evolve.

## Key Areas

The Performance Efficiency pillar includes the following key areas:

- Selection
- Review
- Monitoring
- Tradeoffs

## Questions

The AWS Well-Architected Framework provides a set of questions that allows you to review an existing or proposed architecture. It also provides a set of AWS best practices for each pillar.

{% for child in site.pages %}
  {% if child.parent == page.title %}
  - [{{ child.title }}]({{ child.url | absolute_url }})
  {% endif %}
{% endfor %}
