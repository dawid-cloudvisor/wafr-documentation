---
title: Reliability
layout: default
nav_order: 3
has_children: true
permalink: /docs/reliability
---

<div class="pillar-header">
  <h1>Reliability Pillar</h1>
  <p>The reliability pillar focuses on ensuring a workload performs its intended function correctly and consistently when it's expected to. This includes the ability to operate and test the workload through its total lifecycle.</p>
</div>

The Reliability pillar includes the ability to support development and run workloads effectively, gain insight into their operations, and to continuously improve supporting processes and procedures to deliver business value.

## Reliability Questions

<div class="question-accordion">
  <div class="question-button">
    <a href="javascript:void(0);">REL01: How do you manage service quotas and constraints?</a>
    <div class="question-content">
      <ul>
        <li><a href="./REL01.html">View all REL01 best practices</a></li>
        <li><a href="./REL01-BP01.html">REL01-BP01: Aware of service quotas and constraints</a></li>
        <li><a href="./REL01-BP02.html">REL01-BP02: Manage service quotas across accounts and regions</a></li>
        <li><a href="./REL01-BP03.html">REL01-BP03: Accommodate fixed service quotas and constraints through architecture</a></li>
        <li><a href="./REL01-BP04.html">REL01-BP04: Monitor and manage quotas</a></li>
        <li><a href="./REL01-BP05.html">REL01-BP05: Automate quota management</a></li>
        <li><a href="./REL01-BP06.html">REL01-BP06: Ensure that a sufficient gap exists between the current quotas and the maximum usage to accommodate failover</a></li>
      </ul>
    </div>
  </div>
  
  <div class="question-button">
    <a href="javascript:void(0);">REL02: How do you plan your network topology?</a>
    <div class="question-content">
      <ul>
        <li><a href="./REL02.html">View all REL02 best practices</a></li>
        <li><a href="./REL02-BP01.html">REL02-BP01: Use highly available network connectivity for your workload public endpoints</a></li>
        <li><a href="./REL02-BP02.html">REL02-BP02: Provision redundant connectivity between private networks in the cloud and on-premises environments</a></li>
        <li><a href="./REL02-BP03.html">REL02-BP03: Ensure IP subnet allocation accounts for expansion and availability</a></li>
        <li><a href="./REL02-BP04.html">REL02-BP04: Prefer hub-and-spoke topologies over many-to-many mesh</a></li>
        <li><a href="./REL02-BP05.html">REL02-BP05: Enforce non-overlapping private IP address ranges in all private address spaces where they are connected</a></li>
      </ul>
    </div>
  </div>
  
  <div class="question-button">
    <a href="javascript:void(0);">REL03: How do you design your workload service architecture?</a>
    <div class="question-content">
      <ul>
        <li><a href="./REL03.html">View all REL03 best practices</a></li>
      </ul>
    </div>
  </div>
  
  <div class="question-button">
    <a href="javascript:void(0);">REL04: How do you design interactions in a distributed system to prevent failures?</a>
    <div class="question-content">
      <ul>
        <li><a href="./REL04.html">View all REL04 best practices</a></li>
      </ul>
    </div>
  </div>
  
  <div class="question-button">
    <a href="javascript:void(0);">REL05: How do you design interactions in a distributed system to mitigate or withstand failures?</a>
    <div class="question-content">
      <ul>
        <li><a href="./REL05.html">View all REL05 best practices</a></li>
      </ul>
    </div>
  </div>
  
  <div class="question-button">
    <a href="javascript:void(0);">REL06: How do you monitor workload resources?</a>
    <div class="question-content">
      <ul>
        <li><a href="./REL06.html">View all REL06 best practices</a></li>
      </ul>
    </div>
  </div>
  
  <div class="question-button">
    <a href="javascript:void(0);">REL07: How do you design your workload to adapt to changes in demand?</a>
    <div class="question-content">
      <ul>
        <li><a href="./REL07.html">View all REL07 best practices</a></li>
      </ul>
    </div>
  </div>
  
  <div class="question-button">
    <a href="javascript:void(0);">REL08: How do you implement change?</a>
    <div class="question-content">
      <ul>
        <li><a href="./REL08.html">View all REL08 best practices</a></li>
      </ul>
    </div>
  </div>
  
  <div class="question-button">
    <a href="javascript:void(0);">REL09: How do you back up data?</a>
    <div class="question-content">
      <ul>
        <li><a href="./REL09.html">View all REL09 best practices</a></li>
      </ul>
    </div>
  </div>
  
  <div class="question-button">
    <a href="javascript:void(0);">REL10: How do you use fault isolation to protect your workload?</a>
    <div class="question-content">
      <ul>
        <li><a href="./REL10.html">View all REL10 best practices</a></li>
      </ul>
    </div>
  </div>
  
  <div class="question-button">
    <a href="javascript:void(0);">REL11: How do you design your workload to withstand component failures?</a>
    <div class="question-content">
      <ul>
        <li><a href="./REL11.html">View all REL11 best practices</a></li>
      </ul>
    </div>
  </div>
  
  <div class="question-button">
    <a href="javascript:void(0);">REL12: How do you test reliability?</a>
    <div class="question-content">
      <ul>
        <li><a href="./REL12.html">View all REL12 best practices</a></li>
      </ul>
    </div>
  </div>
  
  <div class="question-button">
    <a href="javascript:void(0);">REL13: How do you plan for disaster recovery?</a>
    <div class="question-content">
      <ul>
        <li><a href="./REL13.html">View all REL13 best practices</a></li>
      </ul>
    </div>
  </div>
</div>

## AWS Services for Reliability

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon CloudWatch</h4>
    <p>Monitors your AWS resources and the applications you run on AWS in real time.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Auto Scaling</h4>
    <p>Monitors your applications and automatically adjusts capacity to maintain steady, predictable performance.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon RDS</h4>
    <p>Makes it easy to set up, operate, and scale a relational database in the cloud with high availability.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Elastic Disaster Recovery</h4>
    <p>Minimizes downtime and data loss with fast, reliable recovery of on-premises and cloud-based applications.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Backup</h4>
    <p>Centrally manages and automates backups across AWS services.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Elastic Load Balancing</h4>
    <p>Automatically distributes incoming application traffic across multiple targets.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon Route 53</h4>
    <p>Provides highly available and scalable cloud Domain Name System (DNS) web service.</p>
  </div>
</div>

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html">AWS Well-Architected Framework - Reliability Pillar</a></li>
    <li><a href="https://aws.amazon.com/reliability/">Reliability on AWS</a></li>
    <li><a href="https://aws.amazon.com/blogs/architecture/">AWS Architecture Blog</a></li>
    <li><a href="https://aws.amazon.com/disaster-recovery/">AWS Disaster Recovery</a></li>
  </ul>
</div>

<style>
.question-accordion {
  margin-bottom: 2rem;
}

.question-button {
  border: 1px solid #ffcca5;
  border-radius: 5px;
  margin-bottom: 0.5rem;
  background-color: #ffead7;
  overflow: hidden;
}

.question-button > a {
  display: block;
  padding: 1rem;
  color: #ff6a00;
  font-weight: bold;
  text-decoration: none;
  position: relative;
}

.question-button > a:after {
  content: '+';
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  font-size: 1.5rem;
}

.question-button > a:hover {
  background-color: #ffcca5;
}

.question-content {
  display: none;
  padding: 0 1rem 1rem 1rem;
  background-color: #fff;
  border-top: 1px solid #ffcca5;
}

.question-content ul {
  list-style-type: none;
  padding-left: 0;
  margin-top: 0.5rem;
}

.question-content li {
  margin-bottom: 0.5rem;
}

.question-content li a {
  color: #ff6a00;
  text-decoration: none;
}

.question-content li a:hover {
  text-decoration: underline;
}
</style>

<script src="/assets/js/reliability-accordion.js"></script>
