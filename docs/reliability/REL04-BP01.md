---
title: REL04-BP01 - Identify the kind of distributed systems you depend on
layout: default
parent: REL04 - How do you design interactions in a distributed system to prevent failures?
grand_parent: Reliability
nav_order: 1
---

# REL04-BP01: Identify the kind of distributed systems you depend on

## Overview

Systematically identify and catalog all distributed systems, services, and dependencies that your workload relies upon to understand failure modes, communication patterns, and reliability characteristics. This comprehensive understanding enables you to design appropriate resilience patterns, implement proper monitoring, and establish effective failure handling strategies for each type of distributed system interaction.

## Implementation Steps

### 1. Conduct Comprehensive Dependency Discovery
- Map all external service dependencies and their characteristics
- Identify synchronous and asynchronous communication patterns
- Catalog third-party services, APIs, and external data sources
- Document internal microservices and their interdependencies

### 2. Classify Distributed System Types and Patterns
- Categorize dependencies by communication patterns and reliability characteristics
- Identify request-response, publish-subscribe, and event-driven patterns
- Classify services by criticality and failure impact
- Document data consistency requirements and transaction boundaries

### 3. Analyze Failure Modes and Impact
- Identify potential failure scenarios for each dependency type
- Assess cascading failure risks and blast radius
- Evaluate timeout, retry, and circuit breaker requirements
- Document recovery time objectives and acceptable degradation levels

### 4. Implement Dependency Monitoring and Observability
- Deploy comprehensive monitoring for all identified dependencies
- Implement distributed tracing across service boundaries
- Establish health checks and dependency status monitoring
- Create dashboards and alerting for dependency failures

### 5. Design Resilience Patterns for Each Dependency Type
- Implement appropriate resilience patterns based on dependency characteristics
- Configure circuit breakers, bulkheads, and timeout strategies
- Design fallback mechanisms and graceful degradation
- Establish retry policies and backoff strategies

### 6. Establish Dependency Governance and Documentation
- Create and maintain dependency catalogs and documentation
- Implement dependency approval and review processes
- Establish SLA requirements and monitoring for critical dependencies
- Create runbooks and incident response procedures
## Implementation Examples

### Example 1: Distributed Systems Discovery and Analysis Engine
```python
import boto3
import json
import logging
import time
import networkx as nx
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set, Tuple, Any
from dataclasses import dataclass, asdict, field
from enum import Enum
import concurrent.futures
import threading
from collections import defaultdict
import requests

class DependencyType(Enum):
    SYNCHRONOUS_API = "synchronous_api"
    ASYNCHRONOUS_MESSAGE = "asynchronous_message"
    DATABASE = "database"
    CACHE = "cache"
    STORAGE = "storage"
    THIRD_PARTY_SERVICE = "third_party_service"
    INTERNAL_SERVICE = "internal_service"
    EVENT_STREAM = "event_stream"

class CommunicationPattern(Enum):
    REQUEST_RESPONSE = "request_response"
    PUBLISH_SUBSCRIBE = "publish_subscribe"
    EVENT_DRIVEN = "event_driven"
    STREAMING = "streaming"
    BATCH_PROCESSING = "batch_processing"

class CriticalityLevel(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

@dataclass
class DistributedSystemDependency:
    dependency_id: str
    name: str
    dependency_type: DependencyType
    communication_pattern: CommunicationPattern
    criticality_level: CriticalityLevel
    endpoint_url: Optional[str]
    service_owner: str
    sla_requirements: Dict[str, Any]
    failure_modes: List[str]
    timeout_config: Dict[str, int]
    retry_config: Dict[str, Any]
    circuit_breaker_config: Dict[str, Any]
    monitoring_config: Dict[str, Any]
    discovered_at: str
    last_validated: str

@dataclass
class DependencyAnalysisResult:
    total_dependencies: int
    dependency_breakdown: Dict[str, int]
    critical_path_analysis: Dict[str, Any]
    failure_impact_analysis: Dict[str, Any]
    resilience_gaps: List[str]
    recommendations: List[str]

class DistributedSystemsAnalyzer:
    def __init__(self, config: Dict):
        self.config = config
        self.ec2 = boto3.client('ec2')
        self.elbv2 = boto3.client('elbv2')
        self.apigateway = boto3.client('apigateway')
        self.lambda_client = boto3.client('lambda')
        self.rds = boto3.client('rds')
        self.elasticache = boto3.client('elasticache')
        self.xray = boto3.client('xray')
        self.cloudwatch = boto3.client('cloudwatch')
        self.dynamodb = boto3.resource('dynamodb')
        self.sns = boto3.client('sns')
        
        # Initialize dependency tracking table
        self.dependencies_table = self.dynamodb.Table(
            config.get('dependencies_table_name', 'distributed-systems-dependencies')
        )
        
        # Thread lock for concurrent operations
        self.lock = threading.Lock()
        
    def discover_distributed_systems(self, discovery_config: Dict) -> Dict:
        """Discover and analyze all distributed system dependencies"""
        analysis_id = f"dependency_analysis_{int(datetime.utcnow().timestamp())}"
        
        analysis_result = {
            'analysis_id': analysis_id,
            'timestamp': datetime.utcnow().isoformat(),
            'discovery_config': discovery_config,
            'discovered_dependencies': {},
            'dependency_graph': {},
            'failure_analysis': {},
            'resilience_assessment': {},
            'recommendations': {},
            'status': 'initiated'
        }
        
        try:
            # 1. Discover AWS service dependencies
            aws_dependencies = self.discover_aws_service_dependencies(
                discovery_config.get('aws_services', {})
            )
            analysis_result['discovered_dependencies']['aws_services'] = aws_dependencies
            
            # 2. Discover external API dependencies
            external_dependencies = self.discover_external_api_dependencies(
                discovery_config.get('external_apis', [])
            )
            analysis_result['discovered_dependencies']['external_apis'] = external_dependencies
            
            # 3. Discover internal service dependencies
            internal_dependencies = self.discover_internal_service_dependencies(
                discovery_config.get('internal_services', {})
            )
            analysis_result['discovered_dependencies']['internal_services'] = internal_dependencies
            
            # 4. Build dependency graph
            dependency_graph = self.build_dependency_graph(analysis_result['discovered_dependencies'])
            analysis_result['dependency_graph'] = dependency_graph
            
            # 5. Analyze failure modes and impact
            failure_analysis = self.analyze_failure_modes(
                analysis_result['discovered_dependencies'], dependency_graph
            )
            analysis_result['failure_analysis'] = failure_analysis
            
            # 6. Assess resilience patterns
            resilience_assessment = self.assess_resilience_patterns(
                analysis_result['discovered_dependencies']
            )
            analysis_result['resilience_assessment'] = resilience_assessment
            
            # 7. Generate recommendations
            recommendations = self.generate_resilience_recommendations(
                analysis_result['discovered_dependencies'], 
                failure_analysis, 
                resilience_assessment
            )
            analysis_result['recommendations'] = recommendations
            
            analysis_result['status'] = 'completed'
            
            # Store analysis results
            self.store_analysis_results(analysis_result)
            
            # Send notifications
            self.send_analysis_notifications(analysis_result)
            
            return analysis_result
            
        except Exception as e:
            logging.error(f"Distributed systems analysis failed: {str(e)}")
            analysis_result['status'] = 'failed'
            analysis_result['error'] = str(e)
            return analysis_result
    
    def discover_aws_service_dependencies(self, aws_config: Dict) -> Dict:
        """Discover AWS service dependencies"""
        aws_dependencies = {
            'databases': [],
            'caches': [],
            'apis': [],
            'storage': [],
            'messaging': [],
            'compute': []
        }
        
        try:
            # Discover RDS databases
            if aws_config.get('include_rds', True):
                rds_dependencies = self.discover_rds_dependencies()
                aws_dependencies['databases'].extend(rds_dependencies)
            
            # Discover DynamoDB tables
            if aws_config.get('include_dynamodb', True):
                dynamodb_dependencies = self.discover_dynamodb_dependencies()
                aws_dependencies['databases'].extend(dynamodb_dependencies)
            
            # Discover ElastiCache clusters
            if aws_config.get('include_elasticache', True):
                cache_dependencies = self.discover_elasticache_dependencies()
                aws_dependencies['caches'].extend(cache_dependencies)
            
            # Discover API Gateway APIs
            if aws_config.get('include_apigateway', True):
                api_dependencies = self.discover_apigateway_dependencies()
                aws_dependencies['apis'].extend(api_dependencies)
            
            # Discover Lambda functions
            if aws_config.get('include_lambda', True):
                lambda_dependencies = self.discover_lambda_dependencies()
                aws_dependencies['compute'].extend(lambda_dependencies)
            
            # Discover S3 buckets
            if aws_config.get('include_s3', True):
                s3_dependencies = self.discover_s3_dependencies()
                aws_dependencies['storage'].extend(s3_dependencies)
            
            return aws_dependencies
            
        except Exception as e:
            logging.error(f"AWS service discovery failed: {str(e)}")
            return aws_dependencies
    
    def discover_rds_dependencies(self) -> List[Dict]:
        """Discover RDS database dependencies"""
        dependencies = []
        
        try:
            response = self.rds.describe_db_instances()
            
            for db_instance in response['DBInstances']:
                if db_instance['DBInstanceStatus'] == 'available':
                    dependency = DistributedSystemDependency(
                        dependency_id=f"rds_{db_instance['DBInstanceIdentifier']}",
                        name=db_instance['DBInstanceIdentifier'],
                        dependency_type=DependencyType.DATABASE,
                        communication_pattern=CommunicationPattern.REQUEST_RESPONSE,
                        criticality_level=self.determine_criticality_from_tags(
                            db_instance.get('TagList', [])
                        ),
                        endpoint_url=f"{db_instance['Endpoint']['Address']}:{db_instance['Endpoint']['Port']}",
                        service_owner=self.extract_owner_from_tags(db_instance.get('TagList', [])),
                        sla_requirements={
                            'availability': '99.95%',
                            'max_latency_ms': 100,
                            'max_connections': db_instance.get('MaxAllocatedStorage', 1000)
                        },
                        failure_modes=[
                            'connection_timeout',
                            'connection_pool_exhaustion',
                            'database_unavailable',
                            'read_replica_lag',
                            'storage_full'
                        ],
                        timeout_config={
                            'connection_timeout_ms': 5000,
                            'query_timeout_ms': 30000
                        },
                        retry_config={
                            'max_retries': 3,
                            'backoff_strategy': 'exponential',
                            'base_delay_ms': 100
                        },
                        circuit_breaker_config={
                            'failure_threshold': 5,
                            'timeout_ms': 60000,
                            'half_open_max_calls': 3
                        },
                        monitoring_config={
                            'health_check_interval_s': 30,
                            'metrics_collection': True,
                            'alerting_enabled': True
                        },
                        discovered_at=datetime.utcnow().isoformat(),
                        last_validated=datetime.utcnow().isoformat()
                    )
                    
                    dependencies.append(asdict(dependency))
            
            return dependencies
            
        except Exception as e:
            logging.error(f"RDS dependency discovery failed: {str(e)}")
            return dependencies
    
    def discover_external_api_dependencies(self, external_apis: List[Dict]) -> List[Dict]:
        """Discover external API dependencies"""
        dependencies = []
        
        try:
            for api_config in external_apis:
                # Validate API endpoint
                endpoint_url = api_config.get('endpoint_url')
                if not endpoint_url:
                    continue
                
                # Test API connectivity
                api_health = self.test_api_connectivity(endpoint_url)
                
                dependency = DistributedSystemDependency(
                    dependency_id=f"external_api_{api_config.get('name', 'unknown')}",
                    name=api_config.get('name', 'Unknown External API'),
                    dependency_type=DependencyType.THIRD_PARTY_SERVICE,
                    communication_pattern=CommunicationPattern.REQUEST_RESPONSE,
                    criticality_level=CriticalityLevel(api_config.get('criticality', 'medium')),
                    endpoint_url=endpoint_url,
                    service_owner=api_config.get('owner', 'external'),
                    sla_requirements=api_config.get('sla_requirements', {
                        'availability': '99.9%',
                        'max_latency_ms': 5000
                    }),
                    failure_modes=[
                        'api_unavailable',
                        'rate_limit_exceeded',
                        'authentication_failure',
                        'timeout',
                        'invalid_response'
                    ],
                    timeout_config={
                        'connection_timeout_ms': api_config.get('timeout_ms', 10000),
                        'read_timeout_ms': api_config.get('read_timeout_ms', 30000)
                    },
                    retry_config=api_config.get('retry_config', {
                        'max_retries': 3,
                        'backoff_strategy': 'exponential',
                        'base_delay_ms': 1000
                    }),
                    circuit_breaker_config=api_config.get('circuit_breaker_config', {
                        'failure_threshold': 5,
                        'timeout_ms': 60000,
                        'half_open_max_calls': 3
                    }),
                    monitoring_config={
                        'health_check_interval_s': 60,
                        'metrics_collection': True,
                        'alerting_enabled': True,
                        'current_status': api_health['status']
                    },
                    discovered_at=datetime.utcnow().isoformat(),
                    last_validated=datetime.utcnow().isoformat()
                )
                
                dependencies.append(asdict(dependency))
            
            return dependencies
            
        except Exception as e:
            logging.error(f"External API discovery failed: {str(e)}")
            return dependencies
    
    def test_api_connectivity(self, endpoint_url: str) -> Dict[str, Any]:
        """Test connectivity to external API"""
        try:
            start_time = time.time()
            response = requests.get(endpoint_url, timeout=10)
            response_time = (time.time() - start_time) * 1000
            
            return {
                'status': 'healthy' if response.status_code < 400 else 'unhealthy',
                'status_code': response.status_code,
                'response_time_ms': response_time,
                'last_checked': datetime.utcnow().isoformat()
            }
            
        except requests.exceptions.Timeout:
            return {
                'status': 'timeout',
                'error': 'Connection timeout',
                'last_checked': datetime.utcnow().isoformat()
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'last_checked': datetime.utcnow().isoformat()
            }
    
    def build_dependency_graph(self, discovered_dependencies: Dict) -> Dict:
        """Build dependency graph for analysis"""
        graph = nx.DiGraph()
        dependency_map = {}
        
        try:
            # Add all dependencies as nodes
            for category, deps in discovered_dependencies.items():
                for dep in deps:
                    dep_id = dep['dependency_id']
                    graph.add_node(dep_id, **dep)
                    dependency_map[dep_id] = dep
            
            # Add edges based on X-Ray traces or configuration
            edges = self.discover_dependency_relationships(dependency_map)
            for source, target in edges:
                if graph.has_node(source) and graph.has_node(target):
                    graph.add_edge(source, target)
            
            # Analyze graph properties
            graph_analysis = {
                'total_nodes': graph.number_of_nodes(),
                'total_edges': graph.number_of_edges(),
                'strongly_connected_components': len(list(nx.strongly_connected_components(graph))),
                'cycles': list(nx.simple_cycles(graph)),
                'critical_paths': self.find_critical_paths(graph),
                'dependency_depth': self.calculate_dependency_depth(graph)
            }
            
            return {
                'graph_data': {
                    'nodes': list(graph.nodes(data=True)),
                    'edges': list(graph.edges(data=True))
                },
                'analysis': graph_analysis
            }
            
        except Exception as e:
            logging.error(f"Dependency graph building failed: {str(e)}")
            return {'graph_data': {'nodes': [], 'edges': []}, 'analysis': {}}
    
    def analyze_failure_modes(self, discovered_dependencies: Dict, dependency_graph: Dict) -> Dict:
        """Analyze failure modes and impact"""
        failure_analysis = {
            'single_points_of_failure': [],
            'cascading_failure_risks': [],
            'blast_radius_analysis': {},
            'recovery_time_analysis': {},
            'mitigation_strategies': {}
        }
        
        try:
            # Identify single points of failure
            for category, deps in discovered_dependencies.items():
                for dep in deps:
                    if dep['criticality_level'] == 'critical':
                        # Check if this dependency has alternatives
                        alternatives = self.find_dependency_alternatives(dep, discovered_dependencies)
                        if not alternatives:
                            failure_analysis['single_points_of_failure'].append({
                                'dependency_id': dep['dependency_id'],
                                'name': dep['name'],
                                'impact': 'Service unavailable',
                                'mitigation_required': True
                            })
            
            # Analyze cascading failure risks
            graph_data = dependency_graph.get('graph_data', {})
            if graph_data.get('nodes'):
                cascading_risks = self.analyze_cascading_failures(graph_data)
                failure_analysis['cascading_failure_risks'] = cascading_risks
            
            # Calculate blast radius for each dependency
            for category, deps in discovered_dependencies.items():
                for dep in deps:
                    blast_radius = self.calculate_blast_radius(dep, dependency_graph)
                    failure_analysis['blast_radius_analysis'][dep['dependency_id']] = blast_radius
            
            return failure_analysis
            
        except Exception as e:
            logging.error(f"Failure mode analysis failed: {str(e)}")
            return failure_analysis
    
    def generate_resilience_recommendations(self, discovered_dependencies: Dict, 
                                          failure_analysis: Dict, 
                                          resilience_assessment: Dict) -> List[Dict]:
        """Generate resilience recommendations"""
        recommendations = []
        
        try:
            # Recommendations for single points of failure
            for spof in failure_analysis.get('single_points_of_failure', []):
                recommendations.append({
                    'type': 'single_point_of_failure',
                    'priority': 'high',
                    'dependency_id': spof['dependency_id'],
                    'recommendation': f"Implement redundancy for {spof['name']}",
                    'implementation_steps': [
                        'Deploy alternative service or backup system',
                        'Implement automatic failover mechanism',
                        'Add health checks and monitoring',
                        'Test failover procedures regularly'
                    ],
                    'estimated_effort': 'high',
                    'business_impact': 'critical'
                })
            
            # Recommendations for missing circuit breakers
            for category, deps in discovered_dependencies.items():
                for dep in deps:
                    if not dep.get('circuit_breaker_config'):
                        recommendations.append({
                            'type': 'circuit_breaker',
                            'priority': 'medium',
                            'dependency_id': dep['dependency_id'],
                            'recommendation': f"Implement circuit breaker for {dep['name']}",
                            'implementation_steps': [
                                'Configure circuit breaker with appropriate thresholds',
                                'Implement fallback mechanisms',
                                'Add monitoring and alerting',
                                'Test circuit breaker behavior'
                            ],
                            'estimated_effort': 'medium',
                            'business_impact': 'medium'
                        })
            
            # Recommendations for timeout configuration
            for category, deps in discovered_dependencies.items():
                for dep in deps:
                    timeout_config = dep.get('timeout_config', {})
                    if not timeout_config or timeout_config.get('connection_timeout_ms', 0) > 10000:
                        recommendations.append({
                            'type': 'timeout_optimization',
                            'priority': 'medium',
                            'dependency_id': dep['dependency_id'],
                            'recommendation': f"Optimize timeout configuration for {dep['name']}",
                            'implementation_steps': [
                                'Analyze response time patterns',
                                'Set appropriate connection and read timeouts',
                                'Implement timeout monitoring',
                                'Test timeout behavior under load'
                            ],
                            'estimated_effort': 'low',
                            'business_impact': 'low'
                        })
            
            return recommendations
            
        except Exception as e:
            logging.error(f"Recommendation generation failed: {str(e)}")
            return recommendations
```

### Example 2: Distributed Systems Discovery Script
```bash
#!/bin/bash

# Distributed Systems Discovery Script
# This script discovers and catalogs distributed system dependencies

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="${SCRIPT_DIR}/dependency-discovery-config.json"
LOG_FILE="${SCRIPT_DIR}/dependency-discovery.log"
TEMP_DIR=$(mktemp -d)
RESULTS_DIR="${SCRIPT_DIR}/results"

# Create results directory
mkdir -p "$RESULTS_DIR"

# Logging function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Error handling
error_exit() {
    log "ERROR: $1"
    cleanup
    exit 1
}

# Cleanup function
cleanup() {
    rm -rf "$TEMP_DIR"
}

# Trap for cleanup
trap cleanup EXIT

# Load configuration
load_configuration() {
    if [[ ! -f "$CONFIG_FILE" ]]; then
        error_exit "Configuration file not found: $CONFIG_FILE"
    fi
    
    log "Loading dependency discovery configuration from $CONFIG_FILE"
    
    # Validate JSON configuration
    if ! jq empty "$CONFIG_FILE" 2>/dev/null; then
        error_exit "Invalid JSON in configuration file"
    fi
    
    # Extract configuration values
    AWS_REGIONS=$(jq -r '.aws_regions[]?' "$CONFIG_FILE" | tr '\n' ' ')
    INCLUDE_RDS=$(jq -r '.include_rds // true' "$CONFIG_FILE")
    INCLUDE_DYNAMODB=$(jq -r '.include_dynamodb // true' "$CONFIG_FILE")
    INCLUDE_ELASTICACHE=$(jq -r '.include_elasticache // true' "$CONFIG_FILE")
    INCLUDE_EXTERNAL_APIS=$(jq -r '.include_external_apis // true' "$CONFIG_FILE")
    
    log "Configuration loaded successfully"
}

# Discover RDS dependencies
discover_rds_dependencies() {
    if [[ "$INCLUDE_RDS" == "true" ]]; then
        log "Discovering RDS dependencies..."
        
        echo "[]" > "$TEMP_DIR/rds_dependencies.json"
        
        for region in $AWS_REGIONS; do
            log "Scanning RDS instances in region: $region"
            
            aws rds describe-db-instances \
                --region "$region" \
                --query 'DBInstances[?DBInstanceStatus==`available`].[DBInstanceIdentifier,Engine,DBInstanceClass,Endpoint.Address,Endpoint.Port,MultiAZ,TagList]' \
                --output json > "$TEMP_DIR/rds_${region}.json"
            
            jq -c '.[]' "$TEMP_DIR/rds_${region}.json" | while read -r instance; do
                DB_IDENTIFIER=$(echo "$instance" | jq -r '.[0]')
                ENGINE=$(echo "$instance" | jq -r '.[1]')
                DB_CLASS=$(echo "$instance" | jq -r '.[2]')
                ENDPOINT=$(echo "$instance" | jq -r '.[3]')
                PORT=$(echo "$instance" | jq -r '.[4]')
                MULTI_AZ=$(echo "$instance" | jq -r '.[5]')
                TAGS=$(echo "$instance" | jq -r '.[6]')
                
                # Extract criticality from tags
                CRITICALITY=$(echo "$TAGS" | jq -r '.[] | select(.Key=="Criticality") | .Value // "medium"')
                OWNER=$(echo "$TAGS" | jq -r '.[] | select(.Key=="Owner") | .Value // "unknown"')
                
                # Create dependency entry
                DEPENDENCY_ENTRY=$(cat << EOF
{
    "dependency_id": "rds_${DB_IDENTIFIER}",
    "name": "$DB_IDENTIFIER",
    "dependency_type": "database",
    "communication_pattern": "request_response",
    "criticality_level": "${CRITICALITY,,}",
    "endpoint_url": "$ENDPOINT:$PORT",
    "service_owner": "$OWNER",
    "region": "$region",
    "engine": "$ENGINE",
    "instance_class": "$DB_CLASS",
    "multi_az": $MULTI_AZ,
    "sla_requirements": {
        "availability": "99.95%",
        "max_latency_ms": 100
    },
    "failure_modes": [
        "connection_timeout",
        "connection_pool_exhaustion",
        "database_unavailable",
        "read_replica_lag"
    ],
    "timeout_config": {
        "connection_timeout_ms": 5000,
        "query_timeout_ms": 30000
    },
    "discovered_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF
)
                
                # Add to dependencies list
                jq --argjson entry "$DEPENDENCY_ENTRY" '. += [$entry]' "$TEMP_DIR/rds_dependencies.json" > "$TEMP_DIR/rds_dependencies_tmp.json"
                mv "$TEMP_DIR/rds_dependencies_tmp.json" "$TEMP_DIR/rds_dependencies.json"
                
                log "Discovered RDS dependency: $DB_IDENTIFIER ($ENGINE)"
            done
        done
        
        RDS_COUNT=$(jq length "$TEMP_DIR/rds_dependencies.json")
        log "Discovered $RDS_COUNT RDS dependencies"
    else
        echo "[]" > "$TEMP_DIR/rds_dependencies.json"
        log "Skipping RDS dependency discovery"
    fi
}

# Discover DynamoDB dependencies
discover_dynamodb_dependencies() {
    if [[ "$INCLUDE_DYNAMODB" == "true" ]]; then
        log "Discovering DynamoDB dependencies..."
        
        echo "[]" > "$TEMP_DIR/dynamodb_dependencies.json"
        
        for region in $AWS_REGIONS; do
            log "Scanning DynamoDB tables in region: $region"
            
            aws dynamodb list-tables \
                --region "$region" \
                --query 'TableNames[]' \
                --output text | while read -r table_name; do
                
                if [[ -n "$table_name" ]]; then
                    # Get table details
                    aws dynamodb describe-table \
                        --region "$region" \
                        --table-name "$table_name" \
                        --query 'Table.{TableName:TableName,TableStatus:TableStatus,BillingMode:BillingModeSummary.BillingMode,ItemCount:ItemCount,TableSizeBytes:TableSizeBytes}' \
                        --output json > "$TEMP_DIR/dynamodb_${table_name}.json"
                    
                    TABLE_STATUS=$(jq -r '.TableStatus' "$TEMP_DIR/dynamodb_${table_name}.json")
                    BILLING_MODE=$(jq -r '.BillingMode // "PROVISIONED"' "$TEMP_DIR/dynamodb_${table_name}.json")
                    ITEM_COUNT=$(jq -r '.ItemCount // 0' "$TEMP_DIR/dynamodb_${table_name}.json")
                    
                    if [[ "$TABLE_STATUS" == "ACTIVE" ]]; then
                        # Determine criticality based on item count and naming
                        CRITICALITY="medium"
                        if [[ $ITEM_COUNT -gt 1000000 ]] || [[ "$table_name" == *"prod"* ]] || [[ "$table_name" == *"critical"* ]]; then
                            CRITICALITY="high"
                        fi
                        
                        DEPENDENCY_ENTRY=$(cat << EOF
{
    "dependency_id": "dynamodb_${table_name}",
    "name": "$table_name",
    "dependency_type": "database",
    "communication_pattern": "request_response",
    "criticality_level": "$CRITICALITY",
    "endpoint_url": "dynamodb.$region.amazonaws.com",
    "service_owner": "aws",
    "region": "$region",
    "billing_mode": "$BILLING_MODE",
    "item_count": $ITEM_COUNT,
    "sla_requirements": {
        "availability": "99.99%",
        "max_latency_ms": 10
    },
    "failure_modes": [
        "throttling",
        "service_unavailable",
        "timeout",
        "capacity_exceeded"
    ],
    "timeout_config": {
        "connection_timeout_ms": 2000,
        "request_timeout_ms": 5000
    },
    "discovered_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF
)
                        
                        jq --argjson entry "$DEPENDENCY_ENTRY" '. += [$entry]' "$TEMP_DIR/dynamodb_dependencies.json" > "$TEMP_DIR/dynamodb_dependencies_tmp.json"
                        mv "$TEMP_DIR/dynamodb_dependencies_tmp.json" "$TEMP_DIR/dynamodb_dependencies.json"
                        
                        log "Discovered DynamoDB dependency: $table_name ($CRITICALITY criticality)"
                    fi
                fi
            done
        done
        
        DYNAMODB_COUNT=$(jq length "$TEMP_DIR/dynamodb_dependencies.json")
        log "Discovered $DYNAMODB_COUNT DynamoDB dependencies"
    else
        echo "[]" > "$TEMP_DIR/dynamodb_dependencies.json"
        log "Skipping DynamoDB dependency discovery"
    fi
}

# Test external API dependencies
test_external_api_dependencies() {
    if [[ "$INCLUDE_EXTERNAL_APIS" == "true" ]]; then
        log "Testing external API dependencies..."
        
        echo "[]" > "$TEMP_DIR/external_api_dependencies.json"
        
        # Read external APIs from configuration
        if jq -e '.external_apis' "$CONFIG_FILE" > /dev/null; then
            jq -c '.external_apis[]' "$CONFIG_FILE" | while read -r api; do
                API_NAME=$(echo "$api" | jq -r '.name')
                ENDPOINT_URL=$(echo "$api" | jq -r '.endpoint_url')
                CRITICALITY=$(echo "$api" | jq -r '.criticality // "medium"')
                OWNER=$(echo "$api" | jq -r '.owner // "external"')
                
                log "Testing external API: $API_NAME ($ENDPOINT_URL)"
                
                # Test API connectivity
                START_TIME=$(date +%s%3N)
                if HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$ENDPOINT_URL" 2>/dev/null); then
                    END_TIME=$(date +%s%3N)
                    RESPONSE_TIME=$((END_TIME - START_TIME))
                    
                    if [[ $HTTP_STATUS -lt 400 ]]; then
                        API_STATUS="healthy"
                    else
                        API_STATUS="unhealthy"
                    fi
                else
                    RESPONSE_TIME=0
                    HTTP_STATUS=0
                    API_STATUS="timeout"
                fi
                
                DEPENDENCY_ENTRY=$(cat << EOF
{
    "dependency_id": "external_api_$(echo "$API_NAME" | tr ' ' '_' | tr '[:upper:]' '[:lower:]')",
    "name": "$API_NAME",
    "dependency_type": "third_party_service",
    "communication_pattern": "request_response",
    "criticality_level": "${CRITICALITY,,}",
    "endpoint_url": "$ENDPOINT_URL",
    "service_owner": "$OWNER",
    "current_status": "$API_STATUS",
    "last_status_code": $HTTP_STATUS,
    "last_response_time_ms": $RESPONSE_TIME,
    "sla_requirements": {
        "availability": "99.9%",
        "max_latency_ms": 5000
    },
    "failure_modes": [
        "api_unavailable",
        "rate_limit_exceeded",
        "authentication_failure",
        "timeout",
        "invalid_response"
    ],
    "timeout_config": {
        "connection_timeout_ms": 10000,
        "read_timeout_ms": 30000
    },
    "discovered_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF
)
                
                jq --argjson entry "$DEPENDENCY_ENTRY" '. += [$entry]' "$TEMP_DIR/external_api_dependencies.json" > "$TEMP_DIR/external_api_dependencies_tmp.json"
                mv "$TEMP_DIR/external_api_dependencies_tmp.json" "$TEMP_DIR/external_api_dependencies.json"
                
                log "External API $API_NAME status: $API_STATUS (${RESPONSE_TIME}ms)"
            done
        fi
        
        EXTERNAL_API_COUNT=$(jq length "$TEMP_DIR/external_api_dependencies.json")
        log "Tested $EXTERNAL_API_COUNT external API dependencies"
    else
        echo "[]" > "$TEMP_DIR/external_api_dependencies.json"
        log "Skipping external API dependency testing"
    fi
}

# Analyze dependency relationships
analyze_dependency_relationships() {
    log "Analyzing dependency relationships..."
    
    # Combine all discovered dependencies
    jq -s 'add' "$TEMP_DIR"/*_dependencies.json > "$TEMP_DIR/all_dependencies.json"
    
    TOTAL_DEPENDENCIES=$(jq length "$TEMP_DIR/all_dependencies.json")
    log "Total dependencies discovered: $TOTAL_DEPENDENCIES"
    
    # Analyze dependency breakdown
    DEPENDENCY_BREAKDOWN=$(jq -r '
        group_by(.dependency_type) | 
        map({
            type: .[0].dependency_type,
            count: length,
            critical_count: map(select(.criticality_level == "critical")) | length,
            high_count: map(select(.criticality_level == "high")) | length
        })
    ' "$TEMP_DIR/all_dependencies.json")
    
    # Identify single points of failure
    CRITICAL_DEPENDENCIES=$(jq -r '
        map(select(.criticality_level == "critical" or .criticality_level == "high")) |
        map({
            dependency_id: .dependency_id,
            name: .name,
            type: .dependency_type,
            criticality: .criticality_level,
            endpoint: .endpoint_url
        })
    ' "$TEMP_DIR/all_dependencies.json")
    
    # Create analysis summary
    ANALYSIS_SUMMARY=$(cat << EOF
{
    "analysis_timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "total_dependencies": $TOTAL_DEPENDENCIES,
    "dependency_breakdown": $DEPENDENCY_BREAKDOWN,
    "critical_dependencies": $CRITICAL_DEPENDENCIES,
    "recommendations": [
        {
            "type": "monitoring",
            "priority": "high",
            "description": "Implement comprehensive monitoring for all critical dependencies"
        },
        {
            "type": "circuit_breakers",
            "priority": "high", 
            "description": "Implement circuit breakers for external service dependencies"
        },
        {
            "type": "redundancy",
            "priority": "medium",
            "description": "Evaluate redundancy options for single points of failure"
        }
    ]
}
EOF
)
    
    echo "$ANALYSIS_SUMMARY" > "$TEMP_DIR/dependency_analysis.json"
    
    # Copy results to results directory
    cp "$TEMP_DIR/dependency_analysis.json" "$RESULTS_DIR/dependency_analysis_$(date +%Y%m%d_%H%M%S).json"
    cp "$TEMP_DIR/all_dependencies.json" "$RESULTS_DIR/all_dependencies_$(date +%Y%m%d_%H%M%S).json"
    
    log "Dependency analysis completed"
}

# Generate dependency report
generate_dependency_report() {
    log "Generating dependency discovery report..."
    
    REPORT_FILE="$RESULTS_DIR/dependency_discovery_report_$(date +%Y%m%d_%H%M%S).html"
    
    cat << 'EOF' > "$REPORT_FILE"
<!DOCTYPE html>
<html>
<head>
    <title>Distributed Systems Dependency Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { background-color: #f0f0f0; padding: 20px; border-radius: 5px; }
        .dependency { margin: 20px 0; padding: 15px; border-left: 4px solid #007cba; background-color: #f0f8ff; }
        .dependency.critical { border-left-color: #dc3545; background-color: #f8d7da; }
        .dependency.high { border-left-color: #fd7e14; background-color: #fff3cd; }
        .dependency.medium { border-left-color: #28a745; background-color: #d4edda; }
        .summary { background-color: #e3f2fd; padding: 15px; border-radius: 5px; margin: 20px 0; }
        .failure-modes { background-color: #fff3e0; padding: 10px; margin: 10px 0; border-radius: 3px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Distributed Systems Dependency Discovery Report</h1>
        <p>Generated on: $(date)</p>
        <p>Total Dependencies: $(jq length "$TEMP_DIR/all_dependencies.json")</p>
    </div>
EOF
    
    # Add summary statistics
    cat << EOF >> "$REPORT_FILE"
    <div class="summary">
        <h2>Dependency Summary</h2>
        <ul>
EOF
    
    jq -r '.[] | "\(.type): \(.count) (\(.critical_count) critical, \(.high_count) high)"' "$TEMP_DIR/dependency_analysis.json" | jq -r '.dependency_breakdown[]' | while read -r breakdown; do
        echo "            <li>$breakdown</li>" >> "$REPORT_FILE"
    done
    
    cat << EOF >> "$REPORT_FILE"
        </ul>
    </div>
    
    <h2>Discovered Dependencies</h2>
EOF
    
    # Add detailed dependencies
    jq -c '.[]' "$TEMP_DIR/all_dependencies.json" | while read -r dep; do
        DEP_NAME=$(echo "$dep" | jq -r '.name')
        DEP_TYPE=$(echo "$dep" | jq -r '.dependency_type')
        CRITICALITY=$(echo "$dep" | jq -r '.criticality_level')
        ENDPOINT=$(echo "$dep" | jq -r '.endpoint_url')
        OWNER=$(echo "$dep" | jq -r '.service_owner')
        
        cat << EOF >> "$REPORT_FILE"
    <div class="dependency $CRITICALITY">
        <h3>$DEP_NAME</h3>
        <p><strong>Type:</strong> $DEP_TYPE</p>
        <p><strong>Criticality:</strong> $CRITICALITY</p>
        <p><strong>Endpoint:</strong> $ENDPOINT</p>
        <p><strong>Owner:</strong> $OWNER</p>
        
        <div class="failure-modes">
            <strong>Potential Failure Modes:</strong>
            <ul>
EOF
        
        echo "$dep" | jq -r '.failure_modes[]' | while read -r failure_mode; do
            echo "                <li>$failure_mode</li>" >> "$REPORT_FILE"
        done
        
        cat << EOF >> "$REPORT_FILE"
            </ul>
        </div>
    </div>
EOF
    done
    
    echo "</body></html>" >> "$REPORT_FILE"
    
    log "Dependency discovery report generated: $REPORT_FILE"
}

# Main execution
main() {
    log "Starting distributed systems dependency discovery"
    
    # Check prerequisites
    if ! command -v aws &> /dev/null; then
        error_exit "AWS CLI not found. Please install AWS CLI."
    fi
    
    if ! command -v jq &> /dev/null; then
        error_exit "jq not found. Please install jq."
    fi
    
    if ! command -v curl &> /dev/null; then
        error_exit "curl not found. Please install curl."
    fi
    
    # Load configuration
    load_configuration
    
    # Execute discovery steps
    case "${1:-discover}" in
        "discover")
            discover_rds_dependencies
            discover_dynamodb_dependencies
            test_external_api_dependencies
            analyze_dependency_relationships
            generate_dependency_report
            log "Distributed systems dependency discovery completed successfully"
            ;;
        "test")
            test_external_api_dependencies
            log "External API testing completed"
            ;;
        "analyze")
            if [[ -f "$TEMP_DIR/all_dependencies.json" ]]; then
                analyze_dependency_relationships
            else
                error_exit "No dependency data found. Run discovery first."
            fi
            ;;
        *)
            echo "Usage: $0 {discover|test|analyze}"
            echo "  discover - Run full dependency discovery (default)"
            echo "  test     - Test external API dependencies only"
            echo "  analyze  - Analyze existing dependency data"
            exit 1
            ;;
    esac
}

# Execute main function
main "$@"
```

## AWS Services Used

- **AWS X-Ray**: Distributed tracing to identify service dependencies and communication patterns
- **Amazon CloudWatch**: Monitoring and metrics collection for dependency health and performance
- **AWS Systems Manager**: Service discovery and configuration management for internal dependencies
- **Amazon API Gateway**: API management and monitoring for service-to-service communication
- **AWS Lambda**: Serverless functions for dependency health checks and monitoring
- **Amazon RDS**: Relational database services with connection pooling and failover capabilities
- **Amazon DynamoDB**: NoSQL database with built-in resilience and scaling capabilities
- **Amazon ElastiCache**: In-memory caching layer for reducing dependency load
- **Amazon SQS**: Message queuing for asynchronous communication patterns
- **Amazon SNS**: Publish-subscribe messaging for event-driven architectures
- **AWS Step Functions**: Workflow orchestration for complex distributed processes
- **Amazon EventBridge**: Event routing and processing for loosely coupled systems
- **AWS App Mesh**: Service mesh for microservices communication and observability
- **Amazon ECS/EKS**: Container orchestration with service discovery and load balancing
- **Elastic Load Balancing**: Load distribution and health checking for service endpoints
- **AWS Config**: Configuration tracking and compliance monitoring for dependencies

## Benefits

- **Comprehensive Visibility**: Complete understanding of all distributed system dependencies
- **Proactive Risk Management**: Early identification of potential failure points and risks
- **Informed Architecture Decisions**: Data-driven decisions about resilience patterns and strategies
- **Improved Incident Response**: Better understanding of failure impact and recovery procedures
- **Optimized Performance**: Identification of bottlenecks and optimization opportunities
- **Enhanced Monitoring**: Targeted monitoring and alerting for critical dependencies
- **Risk Assessment**: Quantified analysis of failure modes and business impact
- **Compliance Support**: Documentation and tracking of system dependencies for audits
- **Team Alignment**: Shared understanding of system architecture and dependencies
- **Continuous Improvement**: Regular assessment and optimization of distributed system design

## Related Resources

- [AWS Well-Architected Reliability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/)
- [Identify Distributed System Dependencies](https://docs.aws.amazon.com/wellarchitected/latest/framework/rel_prevent_interaction_failure_identify.html)
- [AWS X-Ray User Guide](https://docs.aws.amazon.com/xray/latest/devguide/)
- [Amazon CloudWatch User Guide](https://docs.aws.amazon.com/cloudwatch/latest/monitoring/)
- [Distributed Systems Observability](https://aws.amazon.com/builders-library/instrumenting-distributed-systems-for-operational-visibility/)
- [AWS Systems Manager User Guide](https://docs.aws.amazon.com/systems-manager/latest/userguide/)
- [Service Discovery on AWS](https://aws.amazon.com/blogs/aws/amazon-ecs-service-discovery/)
- [AWS App Mesh User Guide](https://docs.aws.amazon.com/app-mesh/latest/userguide/)
- [Microservices Observability](https://aws.amazon.com/blogs/architecture/microservices-observability-with-amazon-cloudwatch/)
- [Distributed Tracing Best Practices](https://aws.amazon.com/blogs/mt/distributed-tracing-aws-x-ray/)
- [AWS Config User Guide](https://docs.aws.amazon.com/config/latest/developerguide/)
- [Building Resilient Systems](https://aws.amazon.com/builders-library/)
