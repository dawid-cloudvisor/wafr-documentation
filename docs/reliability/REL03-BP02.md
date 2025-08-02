---
title: REL03-BP02 - Build services focused on specific business domains and functionality
layout: default
parent: REL03 - How do you design your workload service architecture?
grand_parent: Reliability
nav_order: 2
---

# REL03-BP02: Build services focused on specific business domains and functionality

## Overview

Design services around specific business domains and functionality using domain-driven design principles to create well-bounded, cohesive services that align with business capabilities. This approach ensures services have clear ownership, single responsibility, and minimal coupling while maximizing cohesion within business domain boundaries, leading to more maintainable, scalable, and reliable architectures.

## Implementation Steps

### 1. Conduct Domain-Driven Design Analysis
- Identify core business domains and subdomains within your organization
- Map business capabilities and processes to potential service boundaries
- Engage domain experts and stakeholders to understand business context
- Define ubiquitous language for each domain to ensure clear communication

### 2. Define Bounded Contexts and Service Boundaries
- Establish clear boundaries between different business domains
- Identify entities, value objects, and aggregates within each domain
- Define domain services and their responsibilities
- Ensure each service owns its data and business logic

### 3. Design Domain-Specific APIs and Interfaces
- Create APIs that reflect business operations and workflows
- Design interfaces using domain-specific terminology and concepts
- Implement proper abstraction layers to hide implementation details
- Establish clear input/output contracts for each service

### 4. Implement Service Ownership and Governance
- Assign clear ownership of each service to specific teams
- Establish service-level objectives (SLOs) and key performance indicators
- Implement governance processes for service evolution and changes
- Create documentation and knowledge sharing practices

### 5. Establish Inter-Service Communication Patterns
- Design communication patterns that respect domain boundaries
- Implement event-driven architectures for loose coupling
- Use domain events to communicate business state changes
- Avoid chatty interfaces and minimize cross-domain dependencies

### 6. Implement Domain-Specific Data Management
- Design data models that reflect business domain concepts
- Implement appropriate data consistency patterns for each domain
- Establish data ownership and access patterns
- Consider event sourcing and CQRS patterns where appropriate
## Implementation Examples

### Example 1: Domain-Driven Service Design and Implementation Engine
{% raw %}
```python
import boto3
import json
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set, Tuple, Any
from dataclasses import dataclass, asdict, field
from enum import Enum
import concurrent.futures
import threading
from collections import defaultdict
import uuid

class DomainType(Enum):
    CORE = "core"
    SUPPORTING = "supporting"
    GENERIC = "generic"

class ServiceType(Enum):
    DOMAIN_SERVICE = "domain_service"
    APPLICATION_SERVICE = "application_service"
    INFRASTRUCTURE_SERVICE = "infrastructure_service"

class CommunicationPattern(Enum):
    SYNCHRONOUS = "synchronous"
    ASYNCHRONOUS = "asynchronous"
    EVENT_DRIVEN = "event_driven"

@dataclass
class BusinessCapability:
    capability_id: str
    name: str
    description: str
    domain_type: DomainType
    business_value: str
    complexity_level: int
    change_frequency: str
    stakeholders: List[str]
    processes: List[str]
    data_entities: List[str]

@dataclass
class BoundedContext:
    context_id: str
    name: str
    description: str
    business_capabilities: List[str]
    ubiquitous_language: Dict[str, str]
    domain_entities: List[str]
    domain_services: List[str]
    data_ownership: List[str]
    team_ownership: str

@dataclass
class DomainService:
    service_id: str
    name: str
    bounded_context: str
    service_type: ServiceType
    business_capabilities: List[str]
    api_endpoints: List[str]
    data_entities: List[str]
    dependencies: List[str]
    communication_patterns: List[CommunicationPattern]
    slo_requirements: Dict[str, Any]

class DomainDrivenServiceDesigner:
    def __init__(self, config: Dict):
        self.config = config
        self.dynamodb = boto3.resource('dynamodb')
        self.lambda_client = boto3.client('lambda')
        self.apigateway = boto3.client('apigateway')
        self.eventbridge = boto3.client('events')
        self.cloudwatch = boto3.client('cloudwatch')
        self.sns = boto3.client('sns')
        
        # Initialize domain design tables
        self.domain_table = self.dynamodb.Table(
            config.get('domain_table_name', 'domain-driven-design')
        )
        
        # Thread lock for concurrent operations
        self.lock = threading.Lock()
        
    def design_domain_services(self, design_config: Dict) -> Dict:
        """Design services based on business domains and functionality"""
        design_id = f"domain_design_{int(datetime.utcnow().timestamp())}"
        
        design_result = {
            'design_id': design_id,
            'timestamp': datetime.utcnow().isoformat(),
            'design_config': design_config,
            'business_capabilities': {},
            'bounded_contexts': {},
            'domain_services': {},
            'service_dependencies': {},
            'implementation_plan': {},
            'status': 'initiated'
        }
        
        try:
            # 1. Analyze business capabilities
            business_capabilities = self.analyze_business_capabilities(
                design_config.get('business_analysis', {})
            )
            design_result['business_capabilities'] = business_capabilities
            
            # 2. Define bounded contexts
            bounded_contexts = self.define_bounded_contexts(
                business_capabilities, design_config.get('context_rules', {})
            )
            design_result['bounded_contexts'] = bounded_contexts
            
            # 3. Design domain services
            domain_services = self.design_services_for_domains(
                bounded_contexts, design_config.get('service_requirements', {})
            )
            design_result['domain_services'] = domain_services
            
            # 4. Analyze service dependencies
            service_dependencies = self.analyze_service_dependencies(
                domain_services, bounded_contexts
            )
            design_result['service_dependencies'] = service_dependencies
            
            # 5. Create implementation plan
            implementation_plan = self.create_implementation_plan(
                domain_services, service_dependencies, design_config
            )
            design_result['implementation_plan'] = implementation_plan
            
            # 6. Validate design principles
            validation_results = self.validate_domain_design(design_result)
            design_result['validation_results'] = validation_results
            
            design_result['status'] = 'completed'
            
            # Store design results
            self.store_design_results(design_result)
            
            # Send notifications
            self.send_design_notifications(design_result)
            
            return design_result
            
        except Exception as e:
            logging.error(f"Domain service design failed: {str(e)}")
            design_result['status'] = 'failed'
            design_result['error'] = str(e)
            return design_result
    
    def analyze_business_capabilities(self, business_analysis: Dict) -> Dict:
        """Analyze and catalog business capabilities"""
        capabilities = {
            'core_capabilities': [],
            'supporting_capabilities': [],
            'generic_capabilities': [],
            'capability_map': {}
        }
        
        try:
            # Process business capability definitions
            capability_definitions = business_analysis.get('capabilities', [])
            
            for cap_def in capability_definitions:
                capability = BusinessCapability(
                    capability_id=cap_def.get('id', str(uuid.uuid4())),
                    name=cap_def.get('name'),
                    description=cap_def.get('description', ''),
                    domain_type=DomainType(cap_def.get('domain_type', 'supporting')),
                    business_value=cap_def.get('business_value', 'medium'),
                    complexity_level=cap_def.get('complexity_level', 3),
                    change_frequency=cap_def.get('change_frequency', 'medium'),
                    stakeholders=cap_def.get('stakeholders', []),
                    processes=cap_def.get('processes', []),
                    data_entities=cap_def.get('data_entities', [])
                )
                
                # Categorize capabilities
                if capability.domain_type == DomainType.CORE:
                    capabilities['core_capabilities'].append(asdict(capability))
                elif capability.domain_type == DomainType.SUPPORTING:
                    capabilities['supporting_capabilities'].append(asdict(capability))
                else:
                    capabilities['generic_capabilities'].append(asdict(capability))
                
                capabilities['capability_map'][capability.capability_id] = asdict(capability)
            
            # Analyze capability relationships
            capability_relationships = self.analyze_capability_relationships(
                capabilities['capability_map']
            )
            capabilities['relationships'] = capability_relationships
            
            return capabilities
            
        except Exception as e:
            logging.error(f"Business capability analysis failed: {str(e)}")
            return capabilities
    
    def define_bounded_contexts(self, business_capabilities: Dict, context_rules: Dict) -> Dict:
        """Define bounded contexts based on business capabilities"""
        bounded_contexts = {
            'contexts': [],
            'context_map': {},
            'context_relationships': {}
        }
        
        try:
            # Group capabilities into bounded contexts
            capability_groups = self.group_capabilities_by_domain(
                business_capabilities['capability_map'], context_rules
            )
            
            for group_name, capabilities in capability_groups.items():
                context_id = f"context_{group_name.lower().replace(' ', '_')}"
                
                # Extract domain entities and services
                domain_entities = []
                domain_services = []
                data_ownership = []
                
                for cap_id in capabilities:
                    capability = business_capabilities['capability_map'][cap_id]
                    domain_entities.extend(capability.get('data_entities', []))
                    domain_services.append(f"{capability['name']}_service")
                    data_ownership.extend(capability.get('data_entities', []))
                
                # Create ubiquitous language
                ubiquitous_language = self.create_ubiquitous_language(
                    capabilities, business_capabilities['capability_map']
                )
                
                bounded_context = BoundedContext(
                    context_id=context_id,
                    name=group_name,
                    description=f"Bounded context for {group_name} domain",
                    business_capabilities=capabilities,
                    ubiquitous_language=ubiquitous_language,
                    domain_entities=list(set(domain_entities)),
                    domain_services=list(set(domain_services)),
                    data_ownership=list(set(data_ownership)),
                    team_ownership=context_rules.get('team_assignments', {}).get(group_name, 'unassigned')
                )
                
                bounded_contexts['contexts'].append(asdict(bounded_context))
                bounded_contexts['context_map'][context_id] = asdict(bounded_context)
            
            # Analyze context relationships
            context_relationships = self.analyze_context_relationships(
                bounded_contexts['context_map']
            )
            bounded_contexts['context_relationships'] = context_relationships
            
            return bounded_contexts
            
        except Exception as e:
            logging.error(f"Bounded context definition failed: {str(e)}")
            return bounded_contexts
    
    def design_services_for_domains(self, bounded_contexts: Dict, service_requirements: Dict) -> Dict:
        """Design services for each bounded context"""
        domain_services = {
            'services': [],
            'service_map': {},
            'service_apis': {},
            'service_dependencies': {}
        }
        
        try:
            for context_id, context in bounded_contexts['context_map'].items():
                # Design services for this bounded context
                context_services = self.design_context_services(context, service_requirements)
                
                for service in context_services:
                    service_id = service['service_id']
                    domain_services['services'].append(service)
                    domain_services['service_map'][service_id] = service
                    
                    # Design API for this service
                    service_api = self.design_service_api(service, context)
                    domain_services['service_apis'][service_id] = service_api
            
            return domain_services
            
        except Exception as e:
            logging.error(f"Domain service design failed: {str(e)}")
            return domain_services
    
    def design_context_services(self, context: Dict, service_requirements: Dict) -> List[Dict]:
        """Design services for a specific bounded context"""
        services = []
        
        try:
            business_capabilities = context.get('business_capabilities', [])
            
            # Create domain service for each major capability
            for capability_id in business_capabilities:
                service_id = f"service_{context['context_id']}_{capability_id}"
                
                domain_service = DomainService(
                    service_id=service_id,
                    name=f"{context['name']} {capability_id} Service",
                    bounded_context=context['context_id'],
                    service_type=ServiceType.DOMAIN_SERVICE,
                    business_capabilities=[capability_id],
                    api_endpoints=self.generate_api_endpoints(capability_id, context),
                    data_entities=context.get('domain_entities', []),
                    dependencies=[],
                    communication_patterns=[CommunicationPattern.SYNCHRONOUS, CommunicationPattern.EVENT_DRIVEN],
                    slo_requirements=service_requirements.get('slo_defaults', {
                        'availability': '99.9%',
                        'latency_p99': '500ms',
                        'error_rate': '<0.1%'
                    })
                )
                
                services.append(asdict(domain_service))
            
            # Create application service for orchestration if needed
            if len(business_capabilities) > 1:
                app_service_id = f"app_service_{context['context_id']}"
                
                application_service = DomainService(
                    service_id=app_service_id,
                    name=f"{context['name']} Application Service",
                    bounded_context=context['context_id'],
                    service_type=ServiceType.APPLICATION_SERVICE,
                    business_capabilities=business_capabilities,
                    api_endpoints=[f"/api/{context['name'].lower()}/orchestrate"],
                    data_entities=[],
                    dependencies=[s['service_id'] for s in services],
                    communication_patterns=[CommunicationPattern.SYNCHRONOUS],
                    slo_requirements=service_requirements.get('slo_defaults', {})
                )
                
                services.append(asdict(application_service))
            
            return services
            
        except Exception as e:
            logging.error(f"Context service design failed: {str(e)}")
            return services
    
    def generate_api_endpoints(self, capability_id: str, context: Dict) -> List[str]:
        """Generate API endpoints based on business capability"""
        endpoints = []
        
        try:
            context_name = context['name'].lower().replace(' ', '-')
            capability_name = capability_id.lower().replace(' ', '-')
            
            # Standard CRUD endpoints
            base_path = f"/api/{context_name}/{capability_name}"
            endpoints.extend([
                f"{base_path}",
                f"{base_path}/{{id}}",
                f"{base_path}/search",
                f"{base_path}/{{id}}/status"
            ])
            
            # Business operation endpoints
            domain_entities = context.get('domain_entities', [])
            for entity in domain_entities:
                entity_name = entity.lower().replace(' ', '-')
                endpoints.extend([
                    f"{base_path}/{entity_name}",
                    f"{base_path}/{entity_name}/{{id}}/validate",
                    f"{base_path}/{entity_name}/{{id}}/process"
                ])
            
            return endpoints
            
        except Exception as e:
            logging.error(f"API endpoint generation failed: {str(e)}")
            return endpoints
```
{% endraw %}

### Example 2: Domain-Driven Service Implementation Script
```bash
#!/bin/bash

# Domain-Driven Service Implementation Script
# This script implements services focused on specific business domains

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="${SCRIPT_DIR}/domain-service-config.json"
LOG_FILE="${SCRIPT_DIR}/domain-service-implementation.log"
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
    
    log "Loading domain service configuration from $CONFIG_FILE"
    
    # Validate JSON configuration
    if ! jq empty "$CONFIG_FILE" 2>/dev/null; then
        error_exit "Invalid JSON in configuration file"
    fi
    
    # Extract configuration values
    PROJECT_NAME=$(jq -r '.project_name // "domain-services"' "$CONFIG_FILE")
    AWS_REGION=$(jq -r '.aws_region // "us-east-1"' "$CONFIG_FILE")
    DEPLOYMENT_STAGE=$(jq -r '.deployment_stage // "dev"' "$CONFIG_FILE")
    
    log "Configuration loaded successfully for project: $PROJECT_NAME"
}

# Create domain service structure
create_domain_service_structure() {
    local domain_name=$1
    local service_name=$2
    
    log "Creating domain service structure for $domain_name::$service_name"
    
    SERVICE_DIR="$TEMP_DIR/services/$domain_name/$service_name"
    mkdir -p "$SERVICE_DIR"/{src,tests,infrastructure,docs}
    
    # Create service implementation
    cat << EOF > "$SERVICE_DIR/src/handler.py"
import json
import logging
import boto3
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class DomainEntity:
    """Base class for domain entities"""
    id: str
    created_at: str
    updated_at: str
    version: int = 1

@dataclass
class BusinessEvent:
    """Domain event for business state changes"""
    event_id: str
    event_type: str
    aggregate_id: str
    event_data: Dict[str, Any]
    timestamp: str
    version: int = 1

class ${service_name^}DomainService:
    """Domain service for ${domain_name} business capability"""
    
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.eventbridge = boto3.client('events')
        self.table_name = f"${PROJECT_NAME}-${domain_name}-${service_name}-${DEPLOYMENT_STAGE}"
        self.table = self.dynamodb.Table(self.table_name)
        
    def create_entity(self, entity_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new domain entity"""
        try:
            entity_id = str(uuid.uuid4())
            timestamp = datetime.utcnow().isoformat()
            
            entity = DomainEntity(
                id=entity_id,
                created_at=timestamp,
                updated_at=timestamp,
                **entity_data
            )
            
            # Store entity
            self.table.put_item(Item=asdict(entity))
            
            # Publish domain event
            event = BusinessEvent(
                event_id=str(uuid.uuid4()),
                event_type=f"${domain_name}.${service_name}.EntityCreated",
                aggregate_id=entity_id,
                event_data=asdict(entity),
                timestamp=timestamp
            )
            
            self._publish_domain_event(event)
            
            logger.info(f"Created entity {entity_id} in ${domain_name}::${service_name}")
            return asdict(entity)
            
        except Exception as e:
            logger.error(f"Failed to create entity: {str(e)}")
            raise
    
    def get_entity(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve domain entity by ID"""
        try:
            response = self.table.get_item(Key={'id': entity_id})
            return response.get('Item')
            
        except Exception as e:
            logger.error(f"Failed to get entity {entity_id}: {str(e)}")
            raise
    
    def update_entity(self, entity_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update domain entity"""
        try:
            timestamp = datetime.utcnow().isoformat()
            
            # Get current entity
            current_entity = self.get_entity(entity_id)
            if not current_entity:
                raise ValueError(f"Entity {entity_id} not found")
            
            # Update entity
            updated_entity = {**current_entity, **updates}
            updated_entity['updated_at'] = timestamp
            updated_entity['version'] = current_entity.get('version', 1) + 1
            
            # Store updated entity
            self.table.put_item(Item=updated_entity)
            
            # Publish domain event
            event = BusinessEvent(
                event_id=str(uuid.uuid4()),
                event_type=f"${domain_name}.${service_name}.EntityUpdated",
                aggregate_id=entity_id,
                event_data=updated_entity,
                timestamp=timestamp
            )
            
            self._publish_domain_event(event)
            
            logger.info(f"Updated entity {entity_id} in ${domain_name}::${service_name}")
            return updated_entity
            
        except Exception as e:
            logger.error(f"Failed to update entity {entity_id}: {str(e)}")
            raise
    
    def _publish_domain_event(self, event: BusinessEvent):
        """Publish domain event to EventBridge"""
        try:
            self.eventbridge.put_events(
                Entries=[
                    {
                        'Source': f'${PROJECT_NAME}.${domain_name}',
                        'DetailType': event.event_type,
                        'Detail': json.dumps(asdict(event)),
                        'EventBusName': f'${PROJECT_NAME}-domain-events'
                    }
                ]
            )
            
        except Exception as e:
            logger.error(f"Failed to publish domain event: {str(e)}")
            raise

# Lambda handler
domain_service = ${service_name^}DomainService()

def lambda_handler(event, context):
    """AWS Lambda handler for ${domain_name}::${service_name}"""
    try:
        http_method = event.get('httpMethod', 'GET')
        path_parameters = event.get('pathParameters') or {}
        body = json.loads(event.get('body', '{}')) if event.get('body') else {}
        
        if http_method == 'POST':
            result = domain_service.create_entity(body)
            return {
                'statusCode': 201,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps(result)
            }
            
        elif http_method == 'GET' and path_parameters.get('id'):
            entity_id = path_parameters['id']
            result = domain_service.get_entity(entity_id)
            
            if result:
                return {
                    'statusCode': 200,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps(result)
                }
            else:
                return {
                    'statusCode': 404,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({'error': 'Entity not found'})
                }
                
        elif http_method == 'PUT' and path_parameters.get('id'):
            entity_id = path_parameters['id']
            result = domain_service.update_entity(entity_id, body)
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps(result)
            }
            
        else:
            return {
                'statusCode': 405,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Method not allowed'})
            }
            
    except Exception as e:
        logger.error(f"Handler error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Internal server error'})
        }
EOF

    # Create CloudFormation template
    cat << EOF > "$SERVICE_DIR/infrastructure/template.yaml"
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: Domain service for ${domain_name}::${service_name}

Parameters:
  Stage:
    Type: String
    Default: ${DEPLOYMENT_STAGE}
  ProjectName:
    Type: String
    Default: ${PROJECT_NAME}

Globals:
  Function:
    Timeout: 30
    Runtime: python3.9
    Environment:
      Variables:
        STAGE: !Ref Stage
        PROJECT_NAME: !Ref ProjectName

Resources:
  # DynamoDB Table for domain entities
  DomainEntityTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: !Sub "\${ProjectName}-${domain_name}-${service_name}-\${Stage}"
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: id
          AttributeType: S
      KeySchema:
        - AttributeName: id
          KeyType: HASH
      StreamSpecification:
        StreamViewType: NEW_AND_OLD_IMAGES
      PointInTimeRecoverySpecification:
        PointInTimeRecoveryEnabled: true
      Tags:
        - Key: Domain
          Value: ${domain_name}
        - Key: Service
          Value: ${service_name}
        - Key: Stage
          Value: !Ref Stage

  # Lambda function for domain service
  DomainServiceFunction:
    Type: AWS::Serverless::Function
    Properties:
      FunctionName: !Sub "\${ProjectName}-${domain_name}-${service_name}-\${Stage}"
      CodeUri: ../src/
      Handler: handler.lambda_handler
      Policies:
        - DynamoDBCrudPolicy:
            TableName: !Ref DomainEntityTable
        - EventBridgePutEventsPolicy:
            EventBusName: !Sub "\${ProjectName}-domain-events"
      Events:
        ApiEvent:
          Type: Api
          Properties:
            Path: /api/${domain_name}/${service_name}
            Method: ANY
        ApiEventWithId:
          Type: Api
          Properties:
            Path: /api/${domain_name}/${service_name}/{id}
            Method: ANY

  # EventBridge Custom Bus for domain events
  DomainEventBus:
    Type: AWS::Events::EventBus
    Properties:
      Name: !Sub "\${ProjectName}-domain-events"
      Tags:
        - Key: Domain
          Value: ${domain_name}
        - Key: Purpose
          Value: DomainEvents

  # CloudWatch Log Group
  DomainServiceLogGroup:
    Type: AWS::Logs::LogGroup
    Properties:
      LogGroupName: !Sub "/aws/lambda/\${ProjectName}-${domain_name}-${service_name}-\${Stage}"
      RetentionInDays: 14

Outputs:
  DomainServiceApi:
    Description: API Gateway endpoint URL for domain service
    Value: !Sub "https://\${ServerlessRestApi}.execute-api.\${AWS::Region}.amazonaws.com/Prod/api/${domain_name}/${service_name}"
    Export:
      Name: !Sub "\${ProjectName}-${domain_name}-${service_name}-api-\${Stage}"
      
  DomainEntityTableName:
    Description: DynamoDB table name for domain entities
    Value: !Ref DomainEntityTable
    Export:
      Name: !Sub "\${ProjectName}-${domain_name}-${service_name}-table-\${Stage}"
      
  DomainEventBusName:
    Description: EventBridge bus name for domain events
    Value: !Ref DomainEventBus
    Export:
      Name: !Sub "\${ProjectName}-domain-events-\${Stage}"
EOF

    # Create requirements.txt
    cat << EOF > "$SERVICE_DIR/src/requirements.txt"
boto3>=1.26.0
botocore>=1.29.0
EOF

    # Create test file
    cat << EOF > "$SERVICE_DIR/tests/test_${service_name}.py"
import json
import pytest
import boto3
from moto import mock_dynamodb, mock_events
from unittest.mock import patch, MagicMock
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from handler import ${service_name^}DomainService, lambda_handler

@mock_dynamodb
@mock_events
class Test${service_name^}DomainService:
    
    def setup_method(self):
        """Setup test environment"""
        self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        self.eventbridge = boto3.client('events', region_name='us-east-1')
        
        # Create test table
        self.table = self.dynamodb.create_table(
            TableName='test-${domain_name}-${service_name}-dev',
            KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S'}],
            BillingMode='PAY_PER_REQUEST'
        )
        
        # Create test event bus
        self.eventbridge.create_event_bus(Name='test-domain-events')
        
        self.service = ${service_name^}DomainService()
        self.service.table_name = 'test-${domain_name}-${service_name}-dev'
        self.service.table = self.table
    
    def test_create_entity(self):
        """Test entity creation"""
        entity_data = {'name': 'Test Entity', 'description': 'Test Description'}
        
        result = self.service.create_entity(entity_data)
        
        assert 'id' in result
        assert result['name'] == 'Test Entity'
        assert result['description'] == 'Test Description'
        assert 'created_at' in result
        assert 'updated_at' in result
    
    def test_get_entity(self):
        """Test entity retrieval"""
        # Create entity first
        entity_data = {'name': 'Test Entity'}
        created_entity = self.service.create_entity(entity_data)
        entity_id = created_entity['id']
        
        # Retrieve entity
        result = self.service.get_entity(entity_id)
        
        assert result is not None
        assert result['id'] == entity_id
        assert result['name'] == 'Test Entity'
    
    def test_update_entity(self):
        """Test entity update"""
        # Create entity first
        entity_data = {'name': 'Original Name'}
        created_entity = self.service.create_entity(entity_data)
        entity_id = created_entity['id']
        
        # Update entity
        updates = {'name': 'Updated Name', 'status': 'active'}
        result = self.service.update_entity(entity_id, updates)
        
        assert result['id'] == entity_id
        assert result['name'] == 'Updated Name'
        assert result['status'] == 'active'
        assert result['version'] == 2

def test_lambda_handler_post():
    """Test Lambda handler for POST request"""
    event = {
        'httpMethod': 'POST',
        'body': json.dumps({'name': 'Test Entity', 'description': 'Test'})
    }
    
    with patch('handler.${service_name^}DomainService') as mock_service:
        mock_instance = MagicMock()
        mock_service.return_value = mock_instance
        mock_instance.create_entity.return_value = {'id': '123', 'name': 'Test Entity'}
        
        result = lambda_handler(event, {})
        
        assert result['statusCode'] == 201
        body = json.loads(result['body'])
        assert body['id'] == '123'
        assert body['name'] == 'Test Entity'

def test_lambda_handler_get():
    """Test Lambda handler for GET request"""
    event = {
        'httpMethod': 'GET',
        'pathParameters': {'id': '123'}
    }
    
    with patch('handler.${service_name^}DomainService') as mock_service:
        mock_instance = MagicMock()
        mock_service.return_value = mock_instance
        mock_instance.get_entity.return_value = {'id': '123', 'name': 'Test Entity'}
        
        result = lambda_handler(event, {})
        
        assert result['statusCode'] == 200
        body = json.loads(result['body'])
        assert body['id'] == '123'
        assert body['name'] == 'Test Entity'
EOF

    log "Created domain service structure for $domain_name::$service_name"
}

# Deploy domain service
deploy_domain_service() {
    local domain_name=$1
    local service_name=$2
    
    log "Deploying domain service $domain_name::$service_name"
    
    SERVICE_DIR="$TEMP_DIR/services/$domain_name/$service_name"
    
    # Install dependencies
    cd "$SERVICE_DIR/src"
    pip install -r requirements.txt -t .
    
    # Deploy using SAM
    cd "$SERVICE_DIR"
    
    # Build SAM application
    sam build --template-file infrastructure/template.yaml
    
    # Deploy SAM application
    sam deploy \
        --template-file infrastructure/template.yaml \
        --stack-name "$PROJECT_NAME-$domain_name-$service_name-$DEPLOYMENT_STAGE" \
        --capabilities CAPABILITY_IAM \
        --region "$AWS_REGION" \
        --parameter-overrides \
            Stage="$DEPLOYMENT_STAGE" \
            ProjectName="$PROJECT_NAME" \
        --no-confirm-changeset \
        --no-fail-on-empty-changeset
    
    # Get deployment outputs
    aws cloudformation describe-stacks \
        --stack-name "$PROJECT_NAME-$domain_name-$service_name-$DEPLOYMENT_STAGE" \
        --region "$AWS_REGION" \
        --query 'Stacks[0].Outputs' \
        --output json > "$RESULTS_DIR/${domain_name}_${service_name}_outputs.json"
    
    log "Successfully deployed domain service $domain_name::$service_name"
}

# Create domain services from configuration
create_domain_services() {
    log "Creating domain services from configuration..."
    
    # Read domain definitions from configuration
    jq -c '.domains[]' "$CONFIG_FILE" | while read -r domain; do
        DOMAIN_NAME=$(echo "$domain" | jq -r '.name')
        
        echo "$domain" | jq -c '.services[]' | while read -r service; do
            SERVICE_NAME=$(echo "$service" | jq -r '.name')
            
            log "Processing domain service: $DOMAIN_NAME::$SERVICE_NAME"
            
            create_domain_service_structure "$DOMAIN_NAME" "$SERVICE_NAME"
            
            # Deploy if requested
            if [[ "$(jq -r '.auto_deploy // false' "$CONFIG_FILE")" == "true" ]]; then
                deploy_domain_service "$DOMAIN_NAME" "$SERVICE_NAME"
            fi
        done
    done
    
    log "Domain services creation completed"
}

# Generate domain service documentation
generate_documentation() {
    log "Generating domain service documentation..."
    
    DOC_FILE="$RESULTS_DIR/domain_services_documentation.md"
    
    cat << EOF > "$DOC_FILE"
# Domain Services Documentation

Generated on: $(date)
Project: $PROJECT_NAME
Stage: $DEPLOYMENT_STAGE

## Overview

This document describes the domain services implemented following Domain-Driven Design principles.

## Domain Services

EOF
    
    # Add documentation for each domain service
    jq -c '.domains[]' "$CONFIG_FILE" | while read -r domain; do
        DOMAIN_NAME=$(echo "$domain" | jq -r '.name')
        DOMAIN_DESC=$(echo "$domain" | jq -r '.description // "No description provided"')
        
        cat << EOF >> "$DOC_FILE"
### $DOMAIN_NAME Domain

**Description:** $DOMAIN_DESC

**Services:**

EOF
        
        echo "$domain" | jq -c '.services[]' | while read -r service; do
            SERVICE_NAME=$(echo "$service" | jq -r '.name')
            SERVICE_DESC=$(echo "$service" | jq -r '.description // "No description provided"')
            
            cat << EOF >> "$DOC_FILE"
#### $SERVICE_NAME Service

- **Description:** $SERVICE_DESC
- **Domain:** $DOMAIN_NAME
- **API Endpoints:**
  - POST /api/$DOMAIN_NAME/$SERVICE_NAME - Create entity
  - GET /api/$DOMAIN_NAME/$SERVICE_NAME/{id} - Get entity
  - PUT /api/$DOMAIN_NAME/$SERVICE_NAME/{id} - Update entity

**Business Capabilities:**
$(echo "$service" | jq -r '.business_capabilities[]?' | sed 's/^/- /')

**Domain Events:**
- $DOMAIN_NAME.$SERVICE_NAME.EntityCreated
- $DOMAIN_NAME.$SERVICE_NAME.EntityUpdated

EOF
        done
    done
    
    log "Documentation generated: $DOC_FILE"
}

# Main execution
main() {
    log "Starting domain-driven service implementation"
    
    # Check prerequisites
    if ! command -v aws &> /dev/null; then
        error_exit "AWS CLI not found. Please install AWS CLI."
    fi
    
    if ! command -v jq &> /dev/null; then
        error_exit "jq not found. Please install jq."
    fi
    
    if ! command -v sam &> /dev/null; then
        error_exit "SAM CLI not found. Please install SAM CLI."
    fi
    
    if ! command -v python3 &> /dev/null; then
        error_exit "Python 3 not found. Please install Python 3."
    fi
    
    if ! command -v pip &> /dev/null; then
        error_exit "pip not found. Please install pip."
    fi
    
    # Load configuration
    load_configuration
    
    # Execute implementation steps
    case "${1:-create}" in
        "create")
            create_domain_services
            generate_documentation
            log "Domain service implementation completed successfully"
            ;;
        "deploy")
            create_domain_services
            log "Domain services deployed successfully"
            ;;
        "docs")
            generate_documentation
            log "Documentation generated successfully"
            ;;
        *)
            echo "Usage: $0 {create|deploy|docs}"
            echo "  create - Create domain service structure (default)"
            echo "  deploy - Create and deploy domain services"
            echo "  docs   - Generate documentation only"
            exit 1
            ;;
    esac
}

# Execute main function
main "$@"
```

## AWS Services Used

- **AWS Lambda**: Serverless functions for implementing domain services with clear business boundaries
- **Amazon DynamoDB**: NoSQL database for domain entity storage with single-table design per domain
- **Amazon EventBridge**: Event-driven communication for publishing domain events across bounded contexts
- **Amazon API Gateway**: RESTful APIs that reflect business operations and domain terminology
- **AWS Step Functions**: Workflow orchestration for complex business processes within domains
- **Amazon SQS**: Message queuing for asynchronous communication between domain services
- **Amazon SNS**: Publish-subscribe messaging for domain event distribution
- **AWS CloudFormation**: Infrastructure as code for consistent domain service deployment
- **Amazon CloudWatch**: Monitoring and logging for domain service observability
- **AWS X-Ray**: Distributed tracing for understanding cross-domain service interactions
- **AWS CodePipeline**: CI/CD pipelines for independent domain service deployments
- **AWS Systems Manager**: Parameter store for domain-specific configuration management
- **Amazon Cognito**: Authentication and authorization aligned with business domain access patterns
- **AWS AppSync**: GraphQL APIs for complex domain queries and real-time subscriptions
- **Amazon ElastiCache**: Caching layer for domain-specific data access patterns
- **AWS Secrets Manager**: Secure storage of domain service credentials and API keys

## Benefits

- **Clear Business Alignment**: Services directly map to business capabilities and domain expertise
- **Improved Maintainability**: Well-defined boundaries reduce complexity and improve code organization
- **Enhanced Team Ownership**: Clear service ownership aligned with business domain expertise
- **Better Scalability**: Independent scaling based on domain-specific load patterns
- **Reduced Coupling**: Loose coupling between domains through well-defined interfaces
- **Faster Development**: Domain experts can work independently within their bounded contexts
- **Improved Testing**: Domain-focused testing strategies with clear business scenarios
- **Better Communication**: Ubiquitous language improves communication between technical and business teams
- **Easier Evolution**: Services can evolve independently based on business domain changes
- **Enhanced Reliability**: Fault isolation prevents failures from cascading across business domains

## Related Resources

- [AWS Well-Architected Reliability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/)
- [Build Services Focused on Business Domains](https://docs.aws.amazon.com/wellarchitected/latest/framework/rel_service_architecture_business_domains.html)
- [Domain-Driven Design on AWS](https://aws.amazon.com/blogs/architecture/domain-driven-design-on-aws/)
- [Microservices on AWS](https://docs.aws.amazon.com/whitepapers/latest/microservices-on-aws/microservices-on-aws.html)
- [Event-Driven Architecture on AWS](https://aws.amazon.com/event-driven-architecture/)
- [AWS Lambda Best Practices](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
- [Amazon EventBridge User Guide](https://docs.aws.amazon.com/eventbridge/latest/userguide/)
- [DynamoDB Single-Table Design](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-modeling-nosql-B.html)
- [API Gateway Best Practices](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-basic-concept.html)
- [Bounded Context Pattern](https://martinfowler.com/bliki/BoundedContext.html)
- [AWS Serverless Application Model](https://docs.aws.amazon.com/serverless-application-model/)
- [Event Sourcing on AWS](https://aws.amazon.com/blogs/compute/building-event-sourcing-applications-with-amazon-msk-and-amazon-kinesis-data-streams/)
