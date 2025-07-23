---
title: Security
layout: default
nav_order: 3
has_children: true
permalink: /docs/security
---

# Security Pillar

The security pillar focuses on protecting information and systems. Key topics include confidentiality and integrity of data, identifying and managing who can do what with privilege management, protecting systems, and establishing controls to detect security events.

## Key Areas

The Security pillar includes the following key areas:

- Security Foundations
- Identity and Access Management
- Detection
- Infrastructure Protection
- Data Protection
- Incident Response

## Questions

The AWS Well-Architected Framework provides a set of questions that allows you to review an existing or proposed architecture. It also provides a set of AWS best practices for each pillar.

{% for child in site.pages %}
  {% if child.parent == page.title %}
  - [{{ child.title }}]({{ child.url | absolute_url }})
  {% endif %}
{% endfor %}
