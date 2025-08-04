---
title: COST08-BP03 - Implement services to reduce data transfer charges
layout: default
parent: COST08 - How do you plan for data transfer charges?
grand_parent: Cost Optimization
nav_order: 3
---

<div class="pillar-header">
  <h1>COST08-BP03: Implement services to reduce data transfer charges</h1>
  <p>Leverage AWS services specifically designed to reduce data transfer costs, such as CloudFront, Direct Connect, VPC endpoints, and regional optimization services. Strategic use of these services can significantly reduce data transfer expenses while improving performance.</p>
</div>

## Implementation guidance

AWS provides numerous services specifically designed to reduce data transfer costs while maintaining or improving performance. These services work by optimizing data paths, reducing internet egress, enabling private connectivity, and providing more cost-effective alternatives to traditional data transfer methods.

### Cost Reduction Services

**Content Delivery Networks**: CloudFront provides global content delivery with reduced data transfer costs compared to direct internet egress from AWS regions.

**Private Connectivity**: Direct Connect and VPC endpoints eliminate internet gateway costs and provide more predictable pricing for high-volume transfers.

**Regional Services**: Services like S3 Transfer Acceleration and Global Accelerator optimize data transfer paths and reduce costs through AWS's global network.

**VPC Optimization**: VPC endpoints, NAT Gateway optimization, and private subnets reduce unnecessary internet gateway usage and associated costs.

### Service Categories

**Edge Services**: CloudFront, Global Accelerator, and edge computing services that bring content and processing closer to users.

**Network Services**: Direct Connect, VPN, and private connectivity services that provide cost-effective alternatives to internet-based transfers.

**Storage Services**: S3 Transfer Acceleration, Cross-Region Replication optimization, and intelligent tiering services.

**Compute Services**: Regional compute placement, edge computing, and serverless services that reduce data movement requirements.

## AWS Services to Consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon CloudFront</h4>
    <p>Global CDN that significantly reduces data transfer costs by caching content at edge locations worldwide. Use CloudFront to reduce origin server load and internet egress costs.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Direct Connect</h4>
    <p>Dedicated network connection that provides predictable, lower-cost data transfer for high-volume workloads. Use Direct Connect for consistent, high-bandwidth requirements.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>VPC Endpoints</h4>
    <p>Private connections to AWS services that eliminate internet gateway data transfer costs. Use VPC endpoints to reduce costs for service-to-service communication.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Global Accelerator</h4>
    <p>Improve application performance and reduce data transfer costs by routing traffic through AWS global network infrastructure.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon S3 Transfer Acceleration</h4>
    <p>Accelerate uploads to S3 using CloudFront edge locations, reducing transfer time and potentially costs for large file uploads.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS PrivateLink</h4>
    <p>Secure, private connectivity between VPCs and AWS services without traversing the internet, reducing data transfer costs and improving security.</p>
  </div>
</div>

## Implementation Steps

### 1. Assess Current Data Transfer Patterns
- Analyze current data transfer costs and volumes
- Identify high-cost transfer patterns and sources
- Map data flows between services, regions, and external endpoints
- Prioritize optimization opportunities based on cost impact

### 2. Design Service Implementation Strategy
- Select appropriate AWS services for each use case
- Design architecture that leverages cost reduction services
- Plan integration with existing infrastructure
- Estimate cost savings and ROI for each service

### 3. Implement Edge and CDN Services
- Deploy CloudFront distributions for content delivery
- Configure Global Accelerator for application acceleration
- Implement S3 Transfer Acceleration for large file uploads
- Optimize edge caching and content delivery strategies

### 4. Establish Private Connectivity
- Implement VPC endpoints for AWS service communication
- Deploy Direct Connect for high-volume data transfer
- Configure PrivateLink for secure service connectivity
- Optimize NAT Gateway usage and placement

### 5. Optimize Regional Architecture
- Implement regional data placement strategies
- Deploy compute resources closer to data sources
- Optimize cross-region replication and synchronization
- Implement intelligent data routing and load balancing

### 6. Monitor and Optimize Service Usage
- Track cost savings and performance improvements
- Monitor service utilization and optimization opportunities
- Continuously refine service configurations
- Implement automated optimization where possible
## Data Transfer Service Implementation Framework

### Service Implementation Manager
```python
import boto3
import json
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from enum import Enum

class TransferService(Enum):
    CLOUDFRONT = "cloudfront"
    DIRECT_CONNECT = "direct_connect"
    VPC_ENDPOINTS = "vpc_endpoints"
    GLOBAL_ACCELERATOR = "global_accelerator"
    S3_TRANSFER_ACCELERATION = "s3_transfer_acceleration"
    PRIVATELINK = "privatelink"

@dataclass
class ServiceImplementation:
    service_type: TransferService
    current_monthly_cost: float
    estimated_monthly_savings: float
    implementation_cost: float
    payback_period_months: float
    complexity_score: float
    recommended_priority: str

class DataTransferServiceManager:
    def __init__(self):
        self.cloudfront = boto3.client('cloudfront')
        self.directconnect = boto3.client('directconnect')
        self.ec2 = boto3.client('ec2')
        self.globalaccelerator = boto3.client('globalaccelerator')
        self.s3 = boto3.client('s3')
        
    def analyze_service_opportunities(self, transfer_data: Dict) -> List[ServiceImplementation]:
        """Analyze opportunities for implementing data transfer cost reduction services"""
        
        implementations = []
        
        # CloudFront CDN analysis
        cloudfront_impl = self.analyze_cloudfront_opportunity(transfer_data)
        if cloudfront_impl:
            implementations.append(cloudfront_impl)
        
        # Direct Connect analysis
        directconnect_impl = self.analyze_directconnect_opportunity(transfer_data)
        if directconnect_impl:
            implementations.append(directconnect_impl)
        
        # VPC Endpoints analysis
        vpc_endpoints_impl = self.analyze_vpc_endpoints_opportunity(transfer_data)
        if vpc_endpoints_impl:
            implementations.append(vpc_endpoints_impl)
        
        # Global Accelerator analysis
        global_accelerator_impl = self.analyze_global_accelerator_opportunity(transfer_data)
        if global_accelerator_impl:
            implementations.append(global_accelerator_impl)
        
        # S3 Transfer Acceleration analysis
        s3_acceleration_impl = self.analyze_s3_acceleration_opportunity(transfer_data)
        if s3_acceleration_impl:
            implementations.append(s3_acceleration_impl)
        
        # Sort by priority (payback period and savings potential)
        implementations.sort(key=lambda x: (x.payback_period_months, -x.estimated_monthly_savings))
        
        return implementations
    
    def analyze_cloudfront_opportunity(self, transfer_data: Dict) -> Optional[ServiceImplementation]:
        """Analyze CloudFront CDN implementation opportunity"""
        
        internet_egress_cost = transfer_data.get('cost_breakdown', {}).get('internet_egress', 0)
        internet_egress_volume = transfer_data.get('volume_breakdown', {}).get('internet_egress', 0)
        
        if internet_egress_cost > 500:  # $500/month threshold
            # Calculate CloudFront costs and savings
            cloudfront_cost = self.estimate_cloudfront_cost(internet_egress_volume)
            potential_savings = max(0, internet_egress_cost - cloudfront_cost)
            
            if potential_savings > 100:  # Minimum $100/month savings
                implementation_cost = 2000  # Setup and configuration costs
                payback_months = implementation_cost / potential_savings if potential_savings > 0 else float('inf')
                
                return ServiceImplementation(
                    service_type=TransferService.CLOUDFRONT,
                    current_monthly_cost=internet_egress_cost,
                    estimated_monthly_savings=potential_savings,
                    implementation_cost=implementation_cost,
                    payback_period_months=payback_months,
                    complexity_score=0.3,  # Low complexity
                    recommended_priority='high' if payback_months < 6 else 'medium'
                )
        
        return None
    
    def analyze_directconnect_opportunity(self, transfer_data: Dict) -> Optional[ServiceImplementation]:
        """Analyze Direct Connect implementation opportunity"""
        
        total_transfer_cost = sum(transfer_data.get('cost_breakdown', {}).values())
        total_transfer_volume = sum(transfer_data.get('volume_breakdown', {}).values())
        
        # Direct Connect is cost-effective for high-volume, consistent transfers
        if total_transfer_volume > 100000:  # 100TB/month threshold
            # Estimate Direct Connect costs
            directconnect_monthly_cost = self.estimate_directconnect_cost(total_transfer_volume)
            potential_savings = max(0, total_transfer_cost - directconnect_monthly_cost)
            
            if potential_savings > 500:  # Minimum $500/month savings
                implementation_cost = 10000  # Setup, hardware, and configuration
                payback_months = implementation_cost / potential_savings if potential_savings > 0 else float('inf')
                
                return ServiceImplementation(
                    service_type=TransferService.DIRECT_CONNECT,
                    current_monthly_cost=total_transfer_cost,
                    estimated_monthly_savings=potential_savings,
                    implementation_cost=implementation_cost,
                    payback_period_months=payback_months,
                    complexity_score=0.8,  # High complexity
                    recommended_priority='high' if payback_months < 12 else 'medium'
                )
        
        return None
    
    def analyze_vpc_endpoints_opportunity(self, transfer_data: Dict) -> Optional[ServiceImplementation]:
        """Analyze VPC Endpoints implementation opportunity"""
        
        # Look for service-to-service transfer costs that could be eliminated
        service_transfer_cost = transfer_data.get('cost_breakdown', {}).get('service_specific', 0)
        
        if service_transfer_cost > 200:  # $200/month threshold
            # VPC Endpoints eliminate NAT Gateway and internet gateway costs
            vpc_endpoint_cost = self.estimate_vpc_endpoint_cost()
            potential_savings = max(0, service_transfer_cost * 0.7 - vpc_endpoint_cost)  # 70% of service transfers
            
            if potential_savings > 50:  # Minimum $50/month savings
                implementation_cost = 1000  # Setup and configuration
                payback_months = implementation_cost / potential_savings if potential_savings > 0 else float('inf')
                
                return ServiceImplementation(
                    service_type=TransferService.VPC_ENDPOINTS,
                    current_monthly_cost=service_transfer_cost,
                    estimated_monthly_savings=potential_savings,
                    implementation_cost=implementation_cost,
                    payback_period_months=payback_months,
                    complexity_score=0.4,  # Medium-low complexity
                    recommended_priority='high' if payback_months < 3 else 'medium'
                )
        
        return None
    
    def implement_cloudfront_distribution(self, config: Dict) -> Dict:
        """Implement CloudFront distribution for cost optimization"""
        
        distribution_config = {
            'CallerReference': f'cost-opt-{datetime.now().strftime("%Y%m%d%H%M%S")}',
            'Comment': 'Data transfer cost optimization distribution',
            'DefaultRootObject': config.get('default_root_object', 'index.html'),
            'Origins': {
                'Quantity': 1,
                'Items': [
                    {
                        'Id': 'primary-origin',
                        'DomainName': config['origin_domain'],
                        'CustomOriginConfig': {
                            'HTTPPort': 80,
                            'HTTPSPort': 443,
                            'OriginProtocolPolicy': 'https-only',
                            'OriginSslProtocols': {
                                'Quantity': 1,
                                'Items': ['TLSv1.2']
                            }
                        }
                    }
                ]
            },
            'DefaultCacheBehavior': {
                'TargetOriginId': 'primary-origin',
                'ViewerProtocolPolicy': 'redirect-to-https',
                'AllowedMethods': {
                    'Quantity': 7,
                    'Items': ['GET', 'HEAD', 'OPTIONS', 'PUT', 'POST', 'PATCH', 'DELETE'],
                    'CachedMethods': {
                        'Quantity': 2,
                        'Items': ['GET', 'HEAD']
                    }
                },
                'ForwardedValues': {
                    'QueryString': False,
                    'Cookies': {'Forward': 'none'}
                },
                'TrustedSigners': {
                    'Enabled': False,
                    'Quantity': 0
                },
                'MinTTL': 0,
                'DefaultTTL': 86400,
                'MaxTTL': 31536000,
                'Compress': True
            },
            'Enabled': True,
            'PriceClass': config.get('price_class', 'PriceClass_100')
        }
        
        return distribution_config
    
    def implement_vpc_endpoints(self, vpc_config: Dict) -> List[Dict]:
        """Implement VPC endpoints for cost optimization"""
        
        # Common AWS services that benefit from VPC endpoints
        recommended_endpoints = [
            {
                'service_name': 's3',
                'endpoint_type': 'Gateway',
                'estimated_monthly_savings': 150,
                'use_case': 'S3 access without internet gateway'
            },
            {
                'service_name': 'dynamodb',
                'endpoint_type': 'Gateway',
                'estimated_monthly_savings': 100,
                'use_case': 'DynamoDB access without internet gateway'
            },
            {
                'service_name': 'ec2',
                'endpoint_type': 'Interface',
                'estimated_monthly_savings': 75,
                'use_case': 'EC2 API calls without internet gateway'
            },
            {
                'service_name': 'lambda',
                'endpoint_type': 'Interface',
                'estimated_monthly_savings': 50,
                'use_case': 'Lambda invocations without internet gateway'
            },
            {
                'service_name': 'sns',
                'endpoint_type': 'Interface',
                'estimated_monthly_savings': 25,
                'use_case': 'SNS notifications without internet gateway'
            }
        ]
        
        vpc_endpoints = []
        for endpoint in recommended_endpoints:
            endpoint_config = {
                'VpcId': vpc_config['vpc_id'],
                'ServiceName': f"com.amazonaws.{vpc_config['region']}.{endpoint['service_name']}",
                'VpcEndpointType': endpoint['endpoint_type'],
                'RouteTableIds': vpc_config.get('route_table_ids', []),
                'SubnetIds': vpc_config.get('subnet_ids', []) if endpoint['endpoint_type'] == 'Interface' else [],
                'SecurityGroupIds': vpc_config.get('security_group_ids', []) if endpoint['endpoint_type'] == 'Interface' else [],
                'PolicyDocument': self.create_vpc_endpoint_policy(endpoint['service_name']),
                'Tags': [
                    {'Key': 'Purpose', 'Value': 'CostOptimization'},
                    {'Key': 'Service', 'Value': endpoint['service_name']},
                    {'Key': 'EstimatedMonthlySavings', 'Value': str(endpoint['estimated_monthly_savings'])}
                ]
            }
            vpc_endpoints.append(endpoint_config)
        
        return vpc_endpoints
    
    def implement_direct_connect(self, dc_config: Dict) -> Dict:
        """Implement Direct Connect for high-volume data transfer cost optimization"""
        
        direct_connect_config = {
            'connection_name': f"cost-optimization-{datetime.now().strftime('%Y%m%d')}",
            'bandwidth': dc_config.get('bandwidth', '1Gbps'),
            'location': dc_config['location'],
            'lag_id': dc_config.get('lag_id'),
            'tags': [
                {'Key': 'Purpose', 'Value': 'DataTransferCostOptimization'},
                {'Key': 'Environment', 'Value': dc_config.get('environment', 'production')}
            ],
            'virtual_interfaces': [
                {
                    'vif_name': 'primary-vif',
                    'vif_type': 'private',
                    'vlan': dc_config.get('vlan', 100),
                    'bgp_asn': dc_config.get('bgp_asn', 65000),
                    'customer_address': dc_config['customer_address'],
                    'amazon_address': dc_config['amazon_address'],
                    'address_family': 'ipv4'
                }
            ],
            'cost_analysis': {
                'monthly_port_cost': self.calculate_direct_connect_port_cost(dc_config['bandwidth']),
                'data_transfer_cost_per_gb': 0.02,  # Typical Direct Connect transfer cost
                'estimated_monthly_savings': dc_config.get('estimated_savings', 0)
            }
        }
        
        return direct_connect_config
    
    def create_service_implementation_plan(self, implementations: List[ServiceImplementation]) -> Dict:
        """Create comprehensive implementation plan for data transfer services"""
        
        plan = {
            'plan_id': f"DT_SERVICE_PLAN_{datetime.now().strftime('%Y%m%d')}",
            'total_current_cost': sum(impl.current_monthly_cost for impl in implementations),
            'total_potential_savings': sum(impl.estimated_monthly_savings for impl in implementations),
            'total_implementation_cost': sum(impl.implementation_cost for impl in implementations),
            'overall_payback_months': 0,
            'implementation_phases': [],
            'risk_assessment': {},
            'success_metrics': []
        }
        
        # Calculate overall payback period
        if plan['total_potential_savings'] > 0:
            plan['overall_payback_months'] = plan['total_implementation_cost'] / plan['total_potential_savings']
        
        # Create implementation phases
        high_priority = [impl for impl in implementations if impl.recommended_priority == 'high']
        medium_priority = [impl for impl in implementations if impl.recommended_priority == 'medium']
        low_priority = [impl for impl in implementations if impl.recommended_priority == 'low']
        
        if high_priority:
            plan['implementation_phases'].append({
                'phase': 1,
                'name': 'High Priority Services',
                'duration': '4-8 weeks',
                'services': [impl.service_type.value for impl in high_priority],
                'expected_savings': sum(impl.estimated_monthly_savings for impl in high_priority),
                'implementation_cost': sum(impl.implementation_cost for impl in high_priority)
            })
        
        if medium_priority:
            plan['implementation_phases'].append({
                'phase': 2,
                'name': 'Medium Priority Services',
                'duration': '8-16 weeks',
                'services': [impl.service_type.value for impl in medium_priority],
                'expected_savings': sum(impl.estimated_monthly_savings for impl in medium_priority),
                'implementation_cost': sum(impl.implementation_cost for impl in medium_priority)
            })
        
        # Risk assessment
        plan['risk_assessment'] = {
            'implementation_complexity': np.mean([impl.complexity_score for impl in implementations]),
            'payback_risk': 'low' if plan['overall_payback_months'] < 12 else 'medium',
            'operational_impact': self.assess_operational_impact(implementations),
            'mitigation_strategies': self.create_risk_mitigation_strategies(implementations)
        }
        
        # Success metrics
        plan['success_metrics'] = [
            'Monthly data transfer cost reduction percentage',
            'Service implementation timeline adherence',
            'Performance impact measurement',
            'User experience improvement metrics',
            'ROI achievement within projected timeframe'
        ]
        
        return plan
```

## Service Implementation Templates

### CloudFront Implementation Template
```yaml
CloudFront_Implementation:
  implementation_id: "CF-IMPL-2024-001"
  objective: "Reduce internet egress costs by implementing global CDN"
  
  current_state:
    monthly_internet_egress_cost: 1800.00
    monthly_data_volume_gb: 20000
    primary_regions: ["us-east-1", "eu-west-1"]
    
  cloudfront_configuration:
    distribution_settings:
      price_class: "PriceClass_100"  # US, Canada, Europe
      http_version: "http2"
      ipv6_enabled: true
      compression_enabled: true
      
    cache_behaviors:
      default:
        viewer_protocol_policy: "redirect-to-https"
        compress: true
        ttl:
          min: 0
          default: 86400
          max: 31536000
          
      api_endpoints:
        path_pattern: "/api/*"
        cache_policy: "CachingDisabled"
        origin_request_policy: "CORS-S3Origin"
        
      static_content:
        path_pattern: "/static/*"
        cache_policy: "CachingOptimized"
        ttl:
          min: 86400
          default: 604800
          max: 31536000
          
    origins:
      primary:
        domain_name: "api.example.com"
        protocol_policy: "https-only"
        custom_headers:
          - name: "X-Forwarded-Proto"
            value: "https"
            
  cost_analysis:
    estimated_cloudfront_cost: 1200.00
    estimated_savings: 600.00
    implementation_cost: 2000.00
    payback_period_months: 3.3
    
  implementation_timeline:
    phase_1:
      duration: "Week 1-2"
      tasks:
        - "Create CloudFront distribution"
        - "Configure cache behaviors"
        - "Set up SSL certificates"
        
    phase_2:
      duration: "Week 3-4"
      tasks:
        - "Update DNS records"
        - "Test and validate functionality"
        - "Monitor performance and costs"
        
  success_criteria:
    - "Cache hit rate > 80%"
    - "Cost reduction > 30%"
    - "No performance degradation"
    - "Implementation within 4 weeks"
```

### VPC Endpoints Implementation Strategy
```python
def create_vpc_endpoints_strategy():
    """Create comprehensive VPC endpoints implementation strategy"""
    
    strategy = {
        'service_prioritization': {
            'tier_1_services': {
                'services': ['s3', 'dynamodb'],
                'endpoint_type': 'Gateway',
                'cost_impact': 'High',
                'implementation_complexity': 'Low',
                'estimated_savings': '60-80% of NAT Gateway costs'
            },
            'tier_2_services': {
                'services': ['ec2', 'lambda', 'sns', 'sqs'],
                'endpoint_type': 'Interface',
                'cost_impact': 'Medium',
                'implementation_complexity': 'Medium',
                'estimated_savings': '40-60% of internet gateway costs'
            },
            'tier_3_services': {
                'services': ['cloudwatch', 'logs', 'ssm'],
                'endpoint_type': 'Interface',
                'cost_impact': 'Low-Medium',
                'implementation_complexity': 'Medium',
                'estimated_savings': '20-40% of management traffic costs'
            }
        },
        
        'implementation_approach': {
            'gateway_endpoints': {
                'implementation_method': 'Route table modification',
                'cost_model': 'No additional charges',
                'security_considerations': 'Policy-based access control',
                'monitoring': 'VPC Flow Logs analysis'
            },
            'interface_endpoints': {
                'implementation_method': 'ENI in private subnets',
                'cost_model': '$0.01 per hour per endpoint + data processing',
                'security_considerations': 'Security group and NACLs',
                'monitoring': 'CloudWatch metrics and VPC Flow Logs'
            }
        },
        
        'cost_optimization_techniques': {
            'endpoint_consolidation': 'Use single interface endpoint for multiple AZs where possible',
            'policy_optimization': 'Implement least-privilege endpoint policies',
            'monitoring_optimization': 'Track usage patterns to optimize endpoint placement',
            'automation': 'Automate endpoint lifecycle management'
        },
        
        'migration_strategy': {
            'assessment_phase': {
                'duration': '1-2 weeks',
                'activities': [
                    'Analyze current NAT Gateway and internet gateway usage',
                    'Identify services suitable for VPC endpoints',
                    'Calculate potential cost savings',
                    'Plan endpoint placement and security'
                ]
            },
            'implementation_phase': {
                'duration': '2-4 weeks',
                'activities': [
                    'Create gateway endpoints for S3 and DynamoDB',
                    'Implement interface endpoints for high-usage services',
                    'Update security groups and route tables',
                    'Test and validate connectivity'
                ]
            },
            'optimization_phase': {
                'duration': '2-4 weeks',
                'activities': [
                    'Monitor usage patterns and costs',
                    'Optimize endpoint policies and placement',
                    'Implement additional endpoints based on usage',
                    'Document and share best practices'
                ]
            }
        }
    }
    
    return strategy
```

## Common Challenges and Solutions

### Challenge: Service Selection Complexity

**Solution**: Use data-driven analysis to prioritize services based on cost impact and implementation complexity. Start with high-impact, low-complexity services like VPC endpoints for S3 and DynamoDB.

### Challenge: Integration with Existing Architecture

**Solution**: Plan phased implementations with comprehensive testing. Use blue-green deployment strategies where possible. Implement comprehensive monitoring to validate functionality.

### Challenge: Cost vs. Performance Trade-offs

**Solution**: Establish clear performance baselines before implementation. Use A/B testing to validate performance impact. Implement comprehensive monitoring of both cost and performance metrics.

### Challenge: Managing Multiple Service Implementations

**Solution**: Create centralized implementation plans with clear phases and dependencies. Use infrastructure as code for consistent deployments. Establish clear success criteria and rollback procedures.

### Challenge: Measuring ROI and Effectiveness

**Solution**: Establish clear baseline metrics before implementation. Implement comprehensive cost and performance monitoring. Create regular review cycles to assess optimization effectiveness.

## Related Resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/cost_data_transfer_services.html">AWS Well-Architected Framework - Implement services to reduce data transfer charges</a></li>
    <li><a href="https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Introduction.html">Amazon CloudFront Developer Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/directconnect/latest/UserGuide/Welcome.html">AWS Direct Connect User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints.html">VPC Endpoints User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/global-accelerator/latest/dg/what-is-global-accelerator.html">AWS Global Accelerator Developer Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/AmazonS3/latest/userguide/transfer-acceleration.html">Amazon S3 Transfer Acceleration</a></li>
    <li><a href="https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html">AWS PrivateLink User Guide</a></li>
    <li><a href="https://aws.amazon.com/blogs/networking-and-content-delivery/">AWS Networking & Content Delivery Blog</a></li>
  </ul>
</div>

<style>
.pillar-header {
  background-color: #e8f5e8;
  border-left: 5px solid #2d7d2d;
}

.pillar-header h1 {
  color: #2d7d2d;
}

.aws-service-content h4 {
  color: #2d7d2d;
}

.related-resources {
  background-color: #e8f5e8;
}

.related-resources h2 {
  color: #2d7d2d;
}
</style>
