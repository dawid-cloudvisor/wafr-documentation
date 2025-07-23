---
title: Reliability
layout: default
nav_order: 4
has_children: true
permalink: /docs/reliability
---

# Reliability Pillar

The reliability pillar focuses on ensuring a workload performs its intended function correctly and consistently when it's expected to. This includes the ability to operate and test the workload through its total lifecycle. Key topics include designing distributed systems, recovery planning, and adapting to changing requirements.

## Key Areas

The Reliability pillar includes the following key areas:

- Foundations
- Workload Architecture
- Change Management
- Failure Management

## Questions

The AWS Well-Architected Framework provides a set of questions that allows you to review an existing or proposed architecture. It also provides a set of AWS best practices for each pillar.

{% for child in site.pages %}
  {% if child.parent == page.title %}
  - [{{ child.title }}]({{ child.url | absolute_url }})
  {% endif %}
{% endfor %}
