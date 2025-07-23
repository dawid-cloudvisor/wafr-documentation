---
title: SEC02 - How do you manage identities for people and machines?
layout: default
parent: Security
has_children: true
nav_order: 2
---

<div class="pillar-header">
  <h1>SEC02: How do you manage identities for people and machines?</h1>
  <p>There are two types of identities you need to manage when approaching operating secure AWS workloads. Understanding the type of identity you need to manage and grant access helps you ensure the right identities have access to the right resources under the right conditions.</p>
</div>

## Best Practices

This question includes the following best practices:

<div class="best-practices-list">
  <ul>
    <li><a href="./SEC02-BP01">SEC02-BP01: Use strong sign-in mechanisms</a></li>
    <li><a href="./SEC02-BP02">SEC02-BP02: Rely on a centralized identity provider</a></li>
    <li><a href="./SEC02-BP03">SEC02-BP03: Enforce the use of temporary credentials</a></li>
    <li><a href="./SEC02-BP04">SEC02-BP04: Store and use secrets securely</a></li>
    <li><a href="./SEC02-BP05">SEC02-BP05: Rely on user groups or roles for access control</a></li>
    <li><a href="./SEC02-BP06">SEC02-BP06: Use user groups or roles for access control</a></li>
    <li><a href="./SEC02-BP07">SEC02-BP07: Implement just-in-time access mechanisms</a></li>
  </ul>
</div>

## AWS Services to Consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Identity and Access Management (IAM)</h4>
    <p>Enables you to manage access to AWS services and resources securely.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS IAM Identity Center</h4>
    <p>Helps you securely create or connect your workforce identities and manage their access centrally across AWS accounts and applications.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Secrets Manager</h4>
    <p>Helps you protect secrets needed to access your applications, services, and IT resources.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon Cognito</h4>
    <p>Provides authentication, authorization, and user management for your web and mobile apps.</p>
  </div>
</div>

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html">AWS Well-Architected Framework - Security Pillar</a></li>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/sec-02.html">SEC02: How do you manage identities for people and machines?</a></li>
    <li><a href="https://aws.amazon.com/identity/">AWS Identity Solutions</a></li>
  </ul>
</div>

<style>
.best-practices-list ul {
  list-style-type: none;
  padding-left: 0;
}

.best-practices-list li {
  background-color: #ffead7;
  margin-bottom: 0.5rem;
  border-radius: 5px;
  border: 1px solid #ffcca5;
}

.best-practices-list li a {
  display: block;
  padding: 0.75rem 1rem;
  color: #ff6a00;
  text-decoration: none;
  font-weight: 500;
}

.best-practices-list li a:hover {
  background-color: #ffcca5;
  border-radius: 4px;
}
</style>
