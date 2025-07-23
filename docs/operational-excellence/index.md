---
title: Operational Excellence
layout: default
nav_order: 2
has_children: true
permalink: /docs/operational-excellence
---

# Operational Excellence Pillar

The operational excellence pillar focuses on running and monitoring systems to deliver business value, and continually improving processes and procedures. Key topics include automating changes, responding to events, and defining standards to manage daily operations.

## Key Areas

The Operational Excellence pillar includes the following key areas:

- Organization
- Prepare
- Operate
- Evolve

## Questions

The AWS Well-Architected Framework provides a set of questions that allows you to review an existing or proposed architecture. It also provides a set of AWS best practices for each pillar.

{% for child in site.pages %}
  {% if child.parent == page.title %}
  - [{{ child.title }}]({{ child.url | absolute_url }})
  {% endif %}
{% endfor %}
