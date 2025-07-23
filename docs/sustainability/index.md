---
title: Sustainability
layout: default
nav_order: 7
has_children: true
permalink: /docs/sustainability
---

# Sustainability Pillar

The sustainability pillar focuses on minimizing the environmental impacts of running cloud workloads. Key topics include a shared responsibility model for sustainability, understanding impact, and maximizing utilization to minimize required resources and reduce downstream impacts.

## Key Areas

The Sustainability pillar includes the following key areas:

- Region Selection
- User Behavior Patterns
- Software and Architecture Patterns
- Data Patterns
- Hardware Patterns
- Development and Deployment Process

## Questions

The AWS Well-Architected Framework provides a set of questions that allows you to review an existing or proposed architecture. It also provides a set of AWS best practices for each pillar.

{% for child in site.pages %}
  {% if child.parent == page.title %}
  - [{{ child.title }}]({{ child.url | absolute_url }})
  {% endif %}
{% endfor %}
