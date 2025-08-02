---
title: REL03-BP03 - Provide service contracts per API
layout: default
parent: REL03 - How do you design your workload service architecture?
grand_parent: Reliability
nav_order: 3
---

# REL03-BP03: Provide service contracts per API

## Overview

Establish clear, well-defined service contracts for each API to ensure reliable communication between services and clients. Service contracts define the interface, data formats, error handling, versioning strategy, and behavioral expectations, enabling loose coupling, independent evolution, and reliable integration patterns across distributed systems.

## Implementation Steps

### 1. Define Comprehensive API Specifications
- Create detailed OpenAPI/Swagger specifications for all service endpoints
- Define request and response schemas with validation rules
- Specify error codes, messages, and handling patterns
- Document authentication and authorization requirements

### 2. Implement Contract-First Development
- Design API contracts before implementation begins
- Use contract specifications to generate client SDKs and server stubs
- Establish contract validation in CI/CD pipelines
- Implement contract testing to ensure compliance

### 3. Establish API Versioning Strategy
- Implement semantic versioning for API contracts
- Design backward-compatible changes and deprecation policies
- Provide multiple API versions simultaneously during transitions
- Establish clear migration paths for breaking changes

### 4. Implement Contract Validation and Testing
- Deploy contract testing frameworks for producer and consumer validation
- Implement schema validation for all API requests and responses
- Create automated tests that verify contract compliance
- Establish contract regression testing in deployment pipelines

### 5. Design Error Handling and Resilience Patterns
- Define standardized error response formats across all APIs
- Implement circuit breaker patterns for service dependencies
- Design retry policies and timeout configurations
- Establish graceful degradation strategies for service failures

### 6. Establish Contract Governance and Evolution
- Create processes for contract change management and approval
- Implement contract versioning and lifecycle management
- Establish deprecation policies and migration support
- Maintain contract documentation and change logs
## Implementation Examples

### Example 1: API Contract Management and Validation System
{% raw %}
```python
import boto3
import json
import logging
import yaml
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict, field
from enum import Enum
import jsonschema
from jsonschema import validate, ValidationError
import semver
import requests
from pathlib import Path

class ContractType(Enum):
    OPENAPI = "openapi"
    ASYNCAPI = "asyncapi"
    GRAPHQL = "graphql"
    GRPC = "grpc"

class VersioningStrategy(Enum):
    SEMANTIC = "semantic"
    DATE_BASED = "date_based"
    SEQUENTIAL = "sequential"

class CompatibilityLevel(Enum):
    BACKWARD = "backward"
    FORWARD = "forward"
    FULL = "full"
    BREAKING = "breaking"

@dataclass
class APIContract:
    contract_id: str
    service_name: str
    api_name: str
    version: str
    contract_type: ContractType
    specification: Dict[str, Any]
    created_at: str
    updated_at: str
    status: str
    compatibility_level: CompatibilityLevel
    deprecation_date: Optional[str] = None
    migration_guide: Optional[str] = None

@dataclass
class ContractValidationResult:
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    compatibility_issues: List[str]
    validation_timestamp: str

class APIContractManager:
    def __init__(self, config: Dict):
        self.config = config
        self.s3 = boto3.client('s3')
        self.dynamodb = boto3.resource('dynamodb')
        self.apigateway = boto3.client('apigateway')
        self.cloudwatch = boto3.client('cloudwatch')
        self.sns = boto3.client('sns')
        
        # Initialize contract storage
        self.contracts_table = self.dynamodb.Table(
            config.get('contracts_table_name', 'api-contracts')
        )
        self.contracts_bucket = config.get('contracts_bucket_name', 'api-contracts-storage')
        
    def create_api_contract(self, contract_data: Dict) -> Dict:
        """Create and validate a new API contract"""
        contract_id = f"{contract_data['service_name']}_{contract_data['api_name']}_{contract_data['version']}"
        
        try:
            # Validate contract specification
            validation_result = self.validate_contract_specification(
                contract_data['specification'], 
                ContractType(contract_data['contract_type'])
            )
            
            if not validation_result.is_valid:
                raise ValueError(f"Contract validation failed: {validation_result.errors}")
            
            # Check version compatibility
            compatibility_result = self.check_version_compatibility(
                contract_data['service_name'],
                contract_data['api_name'],
                contract_data['version'],
                contract_data['specification']
            )
            
            # Create contract object
            contract = APIContract(
                contract_id=contract_id,
                service_name=contract_data['service_name'],
                api_name=contract_data['api_name'],
                version=contract_data['version'],
                contract_type=ContractType(contract_data['contract_type']),
                specification=contract_data['specification'],
                created_at=datetime.utcnow().isoformat(),
                updated_at=datetime.utcnow().isoformat(),
                status='active',
                compatibility_level=compatibility_result['compatibility_level'],
                deprecation_date=contract_data.get('deprecation_date'),
                migration_guide=contract_data.get('migration_guide')
            )
            
            # Store contract in DynamoDB
            self.contracts_table.put_item(Item=asdict(contract))
            
            # Store specification in S3
            self.store_contract_specification(contract_id, contract_data['specification'])
            
            # Generate client SDKs if requested
            if contract_data.get('generate_sdks', False):
                sdk_results = self.generate_client_sdks(contract)
                contract_dict = asdict(contract)
                contract_dict['sdk_results'] = sdk_results
                return contract_dict
            
            return asdict(contract)
            
        except Exception as e:
            logging.error(f"Failed to create API contract: {str(e)}")
            raise
    
    def validate_contract_specification(self, specification: Dict, contract_type: ContractType) -> ContractValidationResult:
        """Validate API contract specification"""
        errors = []
        warnings = []
        compatibility_issues = []
        
        try:
            if contract_type == ContractType.OPENAPI:
                errors.extend(self.validate_openapi_specification(specification))
            elif contract_type == ContractType.ASYNCAPI:
                errors.extend(self.validate_asyncapi_specification(specification))
            elif contract_type == ContractType.GRAPHQL:
                errors.extend(self.validate_graphql_specification(specification))
            
            # Check for common API design issues
            warnings.extend(self.check_api_design_patterns(specification, contract_type))
            
            # Check for breaking changes if this is an update
            compatibility_issues.extend(self.check_breaking_changes(specification, contract_type))
            
            return ContractValidationResult(
                is_valid=len(errors) == 0,
                errors=errors,
                warnings=warnings,
                compatibility_issues=compatibility_issues,
                validation_timestamp=datetime.utcnow().isoformat()
            )
            
        except Exception as e:
            logging.error(f"Contract validation failed: {str(e)}")
            return ContractValidationResult(
                is_valid=False,
                errors=[f"Validation error: {str(e)}"],
                warnings=[],
                compatibility_issues=[],
                validation_timestamp=datetime.utcnow().isoformat()
            )
    
    def validate_openapi_specification(self, specification: Dict) -> List[str]:
        """Validate OpenAPI specification"""
        errors = []
        
        try:
            # Check required OpenAPI fields
            required_fields = ['openapi', 'info', 'paths']
            for field in required_fields:
                if field not in specification:
                    errors.append(f"Missing required field: {field}")
            
            # Validate OpenAPI version
            if 'openapi' in specification:
                openapi_version = specification['openapi']
                if not openapi_version.startswith('3.'):
                    errors.append(f"Unsupported OpenAPI version: {openapi_version}")
            
            # Validate info section
            if 'info' in specification:
                info = specification['info']
                if 'title' not in info:
                    errors.append("Missing API title in info section")
                if 'version' not in info:
                    errors.append("Missing API version in info section")
            
            # Validate paths
            if 'paths' in specification:
                paths = specification['paths']
                if not paths:
                    errors.append("No paths defined in API specification")
                
                for path, path_item in paths.items():
                    if not isinstance(path_item, dict):
                        errors.append(f"Invalid path item for {path}")
                        continue
                    
                    # Check for HTTP methods
                    http_methods = ['get', 'post', 'put', 'delete', 'patch', 'head', 'options']
                    has_methods = any(method in path_item for method in http_methods)
                    if not has_methods:
                        errors.append(f"No HTTP methods defined for path {path}")
                    
                    # Validate each operation
                    for method, operation in path_item.items():
                        if method in http_methods:
                            if 'responses' not in operation:
                                errors.append(f"Missing responses for {method.upper()} {path}")
            
            # Validate components/schemas if present
            if 'components' in specification and 'schemas' in specification['components']:
                schemas = specification['components']['schemas']
                for schema_name, schema_def in schemas.items():
                    if not isinstance(schema_def, dict):
                        errors.append(f"Invalid schema definition for {schema_name}")
            
            return errors
            
        except Exception as e:
            return [f"OpenAPI validation error: {str(e)}"]
    
    def check_api_design_patterns(self, specification: Dict, contract_type: ContractType) -> List[str]:
        """Check for API design pattern compliance"""
        warnings = []
        
        try:
            if contract_type == ContractType.OPENAPI:
                # Check for RESTful design patterns
                if 'paths' in specification:
                    paths = specification['paths']
                    
                    # Check for proper HTTP method usage
                    for path, path_item in paths.items():
                        # Check for GET methods that modify state
                        if 'get' in path_item:
                            get_op = path_item['get']
                            if 'requestBody' in get_op:
                                warnings.append(f"GET method should not have request body: {path}")
                        
                        # Check for proper status codes
                        for method, operation in path_item.items():
                            if method in ['get', 'post', 'put', 'delete', 'patch']:
                                responses = operation.get('responses', {})
                                
                                # Check for success responses
                                success_codes = [code for code in responses.keys() if code.startswith('2')]
                                if not success_codes:
                                    warnings.append(f"No success response defined for {method.upper()} {path}")
                                
                                # Check for error responses
                                error_codes = [code for code in responses.keys() if code.startswith('4') or code.startswith('5')]
                                if not error_codes:
                                    warnings.append(f"No error responses defined for {method.upper()} {path}")
                
                # Check for consistent error response format
                if 'components' in specification and 'schemas' in specification['components']:
                    schemas = specification['components']['schemas']
                    error_schemas = [name for name in schemas.keys() if 'error' in name.lower()]
                    if not error_schemas:
                        warnings.append("No standardized error response schema found")
            
            return warnings
            
        except Exception as e:
            return [f"Design pattern check error: {str(e)}"]
    
    def generate_client_sdks(self, contract: APIContract) -> Dict[str, Any]:
        """Generate client SDKs from API contract"""
        sdk_results = {
            'generated_sdks': [],
            'generation_errors': [],
            'download_urls': {}
        }
        
        try:
            if contract.contract_type == ContractType.OPENAPI:
                # Generate Python SDK
                python_sdk = self.generate_python_sdk(contract)
                if python_sdk['success']:
                    sdk_results['generated_sdks'].append('python')
                    sdk_results['download_urls']['python'] = python_sdk['download_url']
                else:
                    sdk_results['generation_errors'].append(f"Python SDK: {python_sdk['error']}")
                
                # Generate JavaScript SDK
                js_sdk = self.generate_javascript_sdk(contract)
                if js_sdk['success']:
                    sdk_results['generated_sdks'].append('javascript')
                    sdk_results['download_urls']['javascript'] = js_sdk['download_url']
                else:
                    sdk_results['generation_errors'].append(f"JavaScript SDK: {js_sdk['error']}")
            
            return sdk_results
            
        except Exception as e:
            sdk_results['generation_errors'].append(f"SDK generation failed: {str(e)}")
            return sdk_results
    
    def generate_python_sdk(self, contract: APIContract) -> Dict[str, Any]:
        """Generate Python SDK from OpenAPI specification"""
        try:
            # Create Python client code
            client_code = f'''
"""
Generated Python SDK for {contract.service_name} {contract.api_name}
Version: {contract.version}
Generated at: {datetime.utcnow().isoformat()}
"""

import requests
import json
from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class APIResponse:
    status_code: int
    data: Any
    headers: Dict[str, str]
    success: bool

class {contract.service_name.title()}{contract.api_name.title()}Client:
    """Client for {contract.service_name} {contract.api_name} API"""
    
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        
        if api_key:
            self.session.headers.update({{'Authorization': f'Bearer {{api_key}}'}})
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> APIResponse:
        """Make HTTP request to API"""
        url = f"{{self.base_url}}{{endpoint}}"
        
        try:
            response = self.session.request(method, url, **kwargs)
            
            # Parse JSON response if possible
            try:
                data = response.json()
            except:
                data = response.text
            
            return APIResponse(
                status_code=response.status_code,
                data=data,
                headers=dict(response.headers),
                success=200 <= response.status_code < 300
            )
            
        except Exception as e:
            return APIResponse(
                status_code=0,
                data={{'error': str(e)}},
                headers={{}},
                success=False
            )
'''
            
            # Add methods for each API endpoint
            if 'paths' in contract.specification:
                for path, path_item in contract.specification['paths'].items():
                    for method, operation in path_item.items():
                        if method in ['get', 'post', 'put', 'delete', 'patch']:
                            method_name = self.generate_method_name(method, path, operation)
                            method_code = self.generate_python_method(method, path, operation)
                            client_code += f"\n    {method_code}"
            
            # Store SDK in S3
            sdk_key = f"sdks/{contract.contract_id}/python/client.py"
            self.s3.put_object(
                Bucket=self.contracts_bucket,
                Key=sdk_key,
                Body=client_code,
                ContentType='text/x-python'
            )
            
            # Generate presigned URL for download
            download_url = self.s3.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.contracts_bucket, 'Key': sdk_key},
                ExpiresIn=3600
            )
            
            return {
                'success': True,
                'download_url': download_url,
                'sdk_key': sdk_key
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def generate_method_name(self, http_method: str, path: str, operation: Dict) -> str:
        """Generate Python method name from HTTP method and path"""
        # Use operationId if available
        if 'operationId' in operation:
            return operation['operationId']
        
        # Generate from HTTP method and path
        path_parts = [part for part in path.split('/') if part and not part.startswith('{')]
        method_name = http_method.lower()
        
        if path_parts:
            method_name += '_' + '_'.join(path_parts)
        
        return method_name.replace('-', '_')
    
    def generate_python_method(self, http_method: str, path: str, operation: Dict) -> str:
        """Generate Python method code for API operation"""
        method_name = self.generate_method_name(http_method, path, operation)
        
        # Extract parameters
        path_params = []
        query_params = []
        
        if 'parameters' in operation:
            for param in operation['parameters']:
                if param.get('in') == 'path':
                    path_params.append(param['name'])
                elif param.get('in') == 'query':
                    query_params.append(param['name'])
        
        # Generate method signature
        params = ['self'] + path_params
        if query_params:
            params.extend([f"{param}=None" for param in query_params])
        if http_method.lower() in ['post', 'put', 'patch']:
            params.append('data=None')
        
        method_signature = f"def {method_name}({', '.join(params)}) -> APIResponse:"
        
        # Generate method body
        method_body = f'''
        """
        {operation.get('summary', f'{http_method.upper()} {path}')}
        """
        endpoint = "{path}"
        '''
        
        # Replace path parameters
        for param in path_params:
            method_body += f'\n        endpoint = endpoint.replace("{{{param}}}", str({param}))'
        
        # Add query parameters
        if query_params:
            method_body += '\n        params = {}'
            for param in query_params:
                method_body += f'\n        if {param} is not None: params["{param}"] = {param}'
        
        # Make request
        request_args = [f'"{http_method.upper()}"', 'endpoint']
        if query_params:
            request_args.append('params=params')
        if http_method.lower() in ['post', 'put', 'patch']:
            request_args.append('json=data')
        
        method_body += f'\n        return self._make_request({", ".join(request_args)})'
        
        return method_signature + method_body
    
    def store_contract_specification(self, contract_id: str, specification: Dict):
        """Store contract specification in S3"""
        try:
            spec_key = f"contracts/{contract_id}/specification.json"
            self.s3.put_object(
                Bucket=self.contracts_bucket,
                Key=spec_key,
                Body=json.dumps(specification, indent=2),
                ContentType='application/json'
            )
            
        except Exception as e:
            logging.error(f"Failed to store contract specification: {str(e)}")
            raise
```
{% endraw %}

### Example 2: API Contract Testing and Validation Script
```bash
#!/bin/bash

# API Contract Testing and Validation Script
# This script validates API contracts and performs contract testing

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="${SCRIPT_DIR}/contract-testing-config.json"
LOG_FILE="${SCRIPT_DIR}/contract-testing.log"
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
    
    log "Loading contract testing configuration from $CONFIG_FILE"
    
    # Validate JSON configuration
    if ! jq empty "$CONFIG_FILE" 2>/dev/null; then
        error_exit "Invalid JSON in configuration file"
    fi
    
    # Extract configuration values
    API_BASE_URL=$(jq -r '.api_base_url // "http://localhost:3000"' "$CONFIG_FILE")
    CONTRACT_SPEC_PATH=$(jq -r '.contract_spec_path // "./openapi.yaml"' "$CONFIG_FILE")
    ENABLE_PACT_TESTING=$(jq -r '.enable_pact_testing // false' "$CONFIG_FILE")
    ENABLE_SCHEMA_VALIDATION=$(jq -r '.enable_schema_validation // true' "$CONFIG_FILE")
    
    log "Configuration loaded successfully"
}

# Validate OpenAPI specification
validate_openapi_spec() {
    log "Validating OpenAPI specification..."
    
    if [[ ! -f "$CONTRACT_SPEC_PATH" ]]; then
        error_exit "Contract specification not found: $CONTRACT_SPEC_PATH"
    fi
    
    # Install swagger-codegen if not present
    if ! command -v swagger-codegen &> /dev/null; then
        log "Installing swagger-codegen..."
        
        # Download swagger-codegen
        SWAGGER_CODEGEN_VERSION="3.0.34"
        SWAGGER_CODEGEN_JAR="$TEMP_DIR/swagger-codegen-cli.jar"
        
        curl -L "https://repo1.maven.org/maven2/io/swagger/codegen/v3/swagger-codegen-cli/$SWAGGER_CODEGEN_VERSION/swagger-codegen-cli-$SWAGGER_CODEGEN_VERSION.jar" \
            -o "$SWAGGER_CODEGEN_JAR"
        
        # Create wrapper script
        cat << EOF > "$TEMP_DIR/swagger-codegen"
#!/bin/bash
java -jar "$SWAGGER_CODEGEN_JAR" "\$@"
EOF
        chmod +x "$TEMP_DIR/swagger-codegen"
        export PATH="$TEMP_DIR:$PATH"
    fi
    
    # Validate specification
    log "Running OpenAPI specification validation..."
    
    if swagger-codegen validate -i "$CONTRACT_SPEC_PATH" > "$TEMP_DIR/validation_output.txt" 2>&1; then
        log "OpenAPI specification validation passed"
        echo "PASSED" > "$TEMP_DIR/spec_validation_result.txt"
    else
        log "OpenAPI specification validation failed"
        cat "$TEMP_DIR/validation_output.txt" | tee -a "$LOG_FILE"
        echo "FAILED" > "$TEMP_DIR/spec_validation_result.txt"
    fi
}

# Generate client SDK for testing
generate_test_client() {
    log "Generating test client from OpenAPI specification..."
    
    CLIENT_DIR="$TEMP_DIR/test_client"
    mkdir -p "$CLIENT_DIR"
    
    # Generate Python client
    if swagger-codegen generate \
        -i "$CONTRACT_SPEC_PATH" \
        -l python \
        -o "$CLIENT_DIR/python" \
        --additional-properties packageName=test_api_client > "$TEMP_DIR/client_generation.log" 2>&1; then
        
        log "Python client generated successfully"
        
        # Install client dependencies
        cd "$CLIENT_DIR/python"
        if [[ -f "requirements.txt" ]]; then
            pip install -r requirements.txt > "$TEMP_DIR/pip_install.log" 2>&1
        fi
        
        # Install the client package
        pip install . > "$TEMP_DIR/pip_install_client.log" 2>&1
        
        cd "$SCRIPT_DIR"
        echo "SUCCESS" > "$TEMP_DIR/client_generation_result.txt"
    else
        log "Failed to generate Python client"
        cat "$TEMP_DIR/client_generation.log" | tee -a "$LOG_FILE"
        echo "FAILED" > "$TEMP_DIR/client_generation_result.txt"
    fi
}

# Perform contract testing
perform_contract_testing() {
    log "Performing contract testing..."
    
    # Create contract test script
    cat << 'EOF' > "$TEMP_DIR/contract_tests.py"
import json
import requests
import sys
import yaml
from typing import Dict, Any, List
import jsonschema
from jsonschema import validate, ValidationError

class ContractTester:
    def __init__(self, base_url: str, spec_path: str):
        self.base_url = base_url.rstrip('/')
        self.spec_path = spec_path
        self.spec = self.load_specification()
        self.test_results = []
    
    def load_specification(self) -> Dict[str, Any]:
        """Load OpenAPI specification"""
        try:
            with open(self.spec_path, 'r') as f:
                if self.spec_path.endswith('.yaml') or self.spec_path.endswith('.yml'):
                    return yaml.safe_load(f)
                else:
                    return json.load(f)
        except Exception as e:
            print(f"Failed to load specification: {e}")
            sys.exit(1)
    
    def test_all_endpoints(self) -> List[Dict[str, Any]]:
        """Test all endpoints defined in the specification"""
        if 'paths' not in self.spec:
            print("No paths found in specification")
            return []
        
        for path, path_item in self.spec['paths'].items():
            for method, operation in path_item.items():
                if method.lower() in ['get', 'post', 'put', 'delete', 'patch']:
                    self.test_endpoint(path, method.upper(), operation)
        
        return self.test_results
    
    def test_endpoint(self, path: str, method: str, operation: Dict[str, Any]):
        """Test a specific endpoint"""
        test_name = f"{method} {path}"
        print(f"Testing {test_name}...")
        
        try:
            # Prepare request
            url = f"{self.base_url}{path}"
            headers = {'Content-Type': 'application/json'}
            
            # Replace path parameters with test values
            if 'parameters' in operation:
                for param in operation['parameters']:
                    if param.get('in') == 'path':
                        param_name = param['name']
                        test_value = self.generate_test_value(param)
                        url = url.replace(f'{{{param_name}}}', str(test_value))
            
            # Prepare request body for POST/PUT/PATCH
            data = None
            if method in ['POST', 'PUT', 'PATCH'] and 'requestBody' in operation:
                data = self.generate_test_request_body(operation['requestBody'])
            
            # Make request
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                json=data,
                timeout=30
            )
            
            # Validate response
            validation_result = self.validate_response(response, operation)
            
            test_result = {
                'test_name': test_name,
                'url': url,
                'method': method,
                'status_code': response.status_code,
                'response_time_ms': response.elapsed.total_seconds() * 1000,
                'validation_passed': validation_result['passed'],
                'validation_errors': validation_result['errors'],
                'timestamp': response.headers.get('date', 'unknown')
            }
            
            self.test_results.append(test_result)
            
            if validation_result['passed']:
                print(f"✓ {test_name} - PASSED")
            else:
                print(f"✗ {test_name} - FAILED: {validation_result['errors']}")
        
        except Exception as e:
            test_result = {
                'test_name': test_name,
                'url': url,
                'method': method,
                'status_code': 0,
                'response_time_ms': 0,
                'validation_passed': False,
                'validation_errors': [str(e)],
                'timestamp': 'unknown'
            }
            
            self.test_results.append(test_result)
            print(f"✗ {test_name} - ERROR: {e}")
    
    def generate_test_value(self, param: Dict[str, Any]) -> Any:
        """Generate test value for parameter"""
        param_type = param.get('schema', {}).get('type', 'string')
        
        if param_type == 'integer':
            return 123
        elif param_type == 'number':
            return 123.45
        elif param_type == 'boolean':
            return True
        else:
            return 'test-value'
    
    def generate_test_request_body(self, request_body: Dict[str, Any]) -> Dict[str, Any]:
        """Generate test request body"""
        content = request_body.get('content', {})
        
        if 'application/json' in content:
            schema = content['application/json'].get('schema', {})
            return self.generate_test_data_from_schema(schema)
        
        return {}
    
    def generate_test_data_from_schema(self, schema: Dict[str, Any]) -> Any:
        """Generate test data from JSON schema"""
        schema_type = schema.get('type', 'object')
        
        if schema_type == 'object':
            result = {}
            properties = schema.get('properties', {})
            required = schema.get('required', [])
            
            for prop_name, prop_schema in properties.items():
                if prop_name in required or len(properties) <= 3:  # Include all if few properties
                    result[prop_name] = self.generate_test_data_from_schema(prop_schema)
            
            return result
        
        elif schema_type == 'array':
            items_schema = schema.get('items', {})
            return [self.generate_test_data_from_schema(items_schema)]
        
        elif schema_type == 'string':
            return schema.get('example', 'test-string')
        
        elif schema_type == 'integer':
            return schema.get('example', 42)
        
        elif schema_type == 'number':
            return schema.get('example', 42.0)
        
        elif schema_type == 'boolean':
            return schema.get('example', True)
        
        else:
            return None
    
    def validate_response(self, response: requests.Response, operation: Dict[str, Any]) -> Dict[str, Any]:
        """Validate response against contract"""
        errors = []
        
        try:
            # Check if status code is defined in contract
            responses = operation.get('responses', {})
            status_code = str(response.status_code)
            
            if status_code not in responses and 'default' not in responses:
                errors.append(f"Status code {status_code} not defined in contract")
                return {'passed': False, 'errors': errors}
            
            # Get response schema
            response_spec = responses.get(status_code, responses.get('default', {}))
            content_spec = response_spec.get('content', {})
            
            if 'application/json' in content_spec:
                schema = content_spec['application/json'].get('schema')
                
                if schema:
                    try:
                        response_data = response.json()
                        
                        # Resolve schema references if needed
                        resolved_schema = self.resolve_schema_refs(schema)
                        
                        # Validate response data against schema
                        validate(instance=response_data, schema=resolved_schema)
                        
                    except ValidationError as e:
                        errors.append(f"Response validation error: {e.message}")
                    except json.JSONDecodeError:
                        errors.append("Response is not valid JSON")
            
            return {'passed': len(errors) == 0, 'errors': errors}
        
        except Exception as e:
            return {'passed': False, 'errors': [f"Validation error: {str(e)}"]}
    
    def resolve_schema_refs(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Resolve schema references (simplified)"""
        if isinstance(schema, dict):
            if '$ref' in schema:
                # Simple reference resolution for #/components/schemas/
                ref = schema['$ref']
                if ref.startswith('#/components/schemas/'):
                    schema_name = ref.split('/')[-1]
                    components = self.spec.get('components', {})
                    schemas = components.get('schemas', {})
                    return schemas.get(schema_name, schema)
            else:
                # Recursively resolve references in nested objects
                resolved = {}
                for key, value in schema.items():
                    resolved[key] = self.resolve_schema_refs(value)
                return resolved
        elif isinstance(schema, list):
            return [self.resolve_schema_refs(item) for item in schema]
        
        return schema

# Main execution
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 3:
        print("Usage: python contract_tests.py <base_url> <spec_path>")
        sys.exit(1)
    
    base_url = sys.argv[1]
    spec_path = sys.argv[2]
    
    tester = ContractTester(base_url, spec_path)
    results = tester.test_all_endpoints()
    
    # Print summary
    total_tests = len(results)
    passed_tests = sum(1 for r in results if r['validation_passed'])
    failed_tests = total_tests - passed_tests
    
    print(f"\n=== Contract Testing Summary ===")
    print(f"Total tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {failed_tests}")
    print(f"Success rate: {(passed_tests/total_tests*100):.1f}%" if total_tests > 0 else "No tests run")
    
    # Save detailed results
    with open('/tmp/contract_test_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    # Exit with error code if any tests failed
    sys.exit(0 if failed_tests == 0 else 1)
EOF

    # Run contract tests
    log "Running contract tests against API..."
    
    if python3 "$TEMP_DIR/contract_tests.py" "$API_BASE_URL" "$CONTRACT_SPEC_PATH" > "$TEMP_DIR/contract_test_output.txt" 2>&1; then
        log "Contract tests passed"
        echo "PASSED" > "$TEMP_DIR/contract_test_result.txt"
    else
        log "Contract tests failed"
        echo "FAILED" > "$TEMP_DIR/contract_test_result.txt"
    fi
    
    # Copy test results
    if [[ -f "/tmp/contract_test_results.json" ]]; then
        cp "/tmp/contract_test_results.json" "$RESULTS_DIR/contract_test_results.json"
    fi
    
    cat "$TEMP_DIR/contract_test_output.txt" | tee -a "$LOG_FILE"
}

# Perform Pact testing (if enabled)
perform_pact_testing() {
    if [[ "$ENABLE_PACT_TESTING" == "true" ]]; then
        log "Performing Pact contract testing..."
        
        # Install Pact if not present
        if ! command -v pact-mock-service &> /dev/null; then
            log "Installing Pact..."
            
            # Install Pact Ruby gem
            if command -v gem &> /dev/null; then
                gem install pact-mock_service pact-provider-verifier
            else
                log "Ruby not found, skipping Pact testing"
                return
            fi
        fi
        
        # Create Pact consumer test
        cat << 'EOF' > "$TEMP_DIR/pact_consumer_test.py"
import json
import requests
from pact import Consumer, Provider, Like, Term
import pytest

# Define Pact consumer and provider
pact = Consumer('TestConsumer').has_pact_with(Provider('APIProvider'))

class TestAPIContract:
    def test_get_resource(self):
        """Test GET endpoint contract"""
        expected_response = {
            'id': Like(123),
            'name': Like('Test Resource'),
            'status': Term(r'active|inactive', 'active'),
            'created_at': Term(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z', '2023-01-01T00:00:00Z')
        }
        
        (pact
         .given('resource exists')
         .upon_receiving('a request for a resource')
         .with_request('GET', '/api/resources/123')
         .will_respond_with(200, body=expected_response))
        
        with pact:
            response = requests.get(f'{pact.uri}/api/resources/123')
            assert response.status_code == 200
            data = response.json()
            assert 'id' in data
            assert 'name' in data
            assert 'status' in data
    
    def test_create_resource(self):
        """Test POST endpoint contract"""
        request_body = {
            'name': 'New Resource',
            'description': 'Test description'
        }
        
        expected_response = {
            'id': Like(456),
            'name': Like('New Resource'),
            'description': Like('Test description'),
            'status': 'active',
            'created_at': Term(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z', '2023-01-01T00:00:00Z')
        }
        
        (pact
         .given('resource can be created')
         .upon_receiving('a request to create a resource')
         .with_request('POST', '/api/resources', body=request_body)
         .will_respond_with(201, body=expected_response))
        
        with pact:
            response = requests.post(f'{pact.uri}/api/resources', json=request_body)
            assert response.status_code == 201
            data = response.json()
            assert data['name'] == 'New Resource'
            assert data['status'] == 'active'

if __name__ == "__main__":
    pytest.main([__file__, '-v'])
EOF

        # Run Pact consumer tests
        if python3 -m pytest "$TEMP_DIR/pact_consumer_test.py" -v > "$TEMP_DIR/pact_test_output.txt" 2>&1; then
            log "Pact consumer tests passed"
            echo "PASSED" > "$TEMP_DIR/pact_test_result.txt"
        else
            log "Pact consumer tests failed"
            echo "FAILED" > "$TEMP_DIR/pact_test_result.txt"
        fi
        
        cat "$TEMP_DIR/pact_test_output.txt" | tee -a "$LOG_FILE"
    else
        log "Pact testing disabled"
        echo "SKIPPED" > "$TEMP_DIR/pact_test_result.txt"
    fi
}

# Generate contract testing report
generate_contract_report() {
    log "Generating contract testing report..."
    
    REPORT_FILE="$RESULTS_DIR/contract_testing_report.html"
    
    # Get test results
    SPEC_VALIDATION=$(cat "$TEMP_DIR/spec_validation_result.txt" 2>/dev/null || echo "NOT_RUN")
    CLIENT_GENERATION=$(cat "$TEMP_DIR/client_generation_result.txt" 2>/dev/null || echo "NOT_RUN")
    CONTRACT_TESTING=$(cat "$TEMP_DIR/contract_test_result.txt" 2>/dev/null || echo "NOT_RUN")
    PACT_TESTING=$(cat "$TEMP_DIR/pact_test_result.txt" 2>/dev/null || echo "NOT_RUN")
    
    cat << EOF > "$REPORT_FILE"
<!DOCTYPE html>
<html>
<head>
    <title>API Contract Testing Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { background-color: #f0f0f0; padding: 20px; border-radius: 5px; }
        .test-result { margin: 20px 0; padding: 15px; border-radius: 5px; }
        .passed { background-color: #d4edda; border-left: 4px solid #28a745; }
        .failed { background-color: #f8d7da; border-left: 4px solid #dc3545; }
        .skipped { background-color: #fff3cd; border-left: 4px solid #ffc107; }
        .not-run { background-color: #e2e3e5; border-left: 4px solid #6c757d; }
        .summary { background-color: #e3f2fd; padding: 15px; border-radius: 5px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="header">
        <h1>API Contract Testing Report</h1>
        <p>Generated on: $(date)</p>
        <p>API Base URL: $API_BASE_URL</p>
        <p>Contract Specification: $CONTRACT_SPEC_PATH</p>
    </div>
    
    <div class="summary">
        <h2>Test Summary</h2>
        <ul>
            <li>Specification Validation: $SPEC_VALIDATION</li>
            <li>Client Generation: $CLIENT_GENERATION</li>
            <li>Contract Testing: $CONTRACT_TESTING</li>
            <li>Pact Testing: $PACT_TESTING</li>
        </ul>
    </div>
    
    <h2>Test Results</h2>
    
    <div class="test-result $(echo "$SPEC_VALIDATION" | tr '[:upper:]' '[:lower:]')">
        <h3>OpenAPI Specification Validation</h3>
        <p><strong>Result:</strong> $SPEC_VALIDATION</p>
        <p>Validates that the OpenAPI specification is syntactically correct and follows OpenAPI standards.</p>
    </div>
    
    <div class="test-result $(echo "$CLIENT_GENERATION" | tr '[:upper:]' '[:lower:]')">
        <h3>Client SDK Generation</h3>
        <p><strong>Result:</strong> $CLIENT_GENERATION</p>
        <p>Tests whether client SDKs can be successfully generated from the API specification.</p>
    </div>
    
    <div class="test-result $(echo "$CONTRACT_TESTING" | tr '[:upper:]' '[:lower:]')">
        <h3>Contract Testing</h3>
        <p><strong>Result:</strong> $CONTRACT_TESTING</p>
        <p>Validates that the API implementation matches the contract specification.</p>
    </div>
    
    <div class="test-result $(echo "$PACT_TESTING" | tr '[:upper:]' '[:lower:]')">
        <h3>Pact Contract Testing</h3>
        <p><strong>Result:</strong> $PACT_TESTING</p>
        <p>Consumer-driven contract testing using Pact framework.</p>
    </div>
    
</body>
</html>
EOF
    
    log "Contract testing report generated: $REPORT_FILE"
}

# Main execution
main() {
    log "Starting API contract testing"
    
    # Check prerequisites
    if ! command -v python3 &> /dev/null; then
        error_exit "Python 3 not found. Please install Python 3."
    fi
    
    if ! command -v pip &> /dev/null; then
        error_exit "pip not found. Please install pip."
    fi
    
    if ! command -v jq &> /dev/null; then
        error_exit "jq not found. Please install jq."
    fi
    
    if ! command -v curl &> /dev/null; then
        error_exit "curl not found. Please install curl."
    fi
    
    # Install required Python packages
    pip install requests jsonschema pyyaml pytest pact-python > "$TEMP_DIR/pip_install_deps.log" 2>&1 || true
    
    # Load configuration
    load_configuration
    
    # Execute testing steps
    case "${1:-test}" in
        "test")
            validate_openapi_spec
            generate_test_client
            perform_contract_testing
            perform_pact_testing
            generate_contract_report
            log "API contract testing completed successfully"
            ;;
        "validate")
            validate_openapi_spec
            log "API specification validation completed"
            ;;
        "generate")
            generate_test_client
            log "Test client generation completed"
            ;;
        "pact")
            perform_pact_testing
            log "Pact testing completed"
            ;;
        *)
            echo "Usage: $0 {test|validate|generate|pact}"
            echo "  test     - Run all contract tests (default)"
            echo "  validate - Validate OpenAPI specification only"
            echo "  generate - Generate test client only"
            echo "  pact     - Run Pact testing only"
            exit 1
            ;;
    esac
}

# Execute main function
main "$@"
```

## AWS Services Used

- **Amazon API Gateway**: RESTful API management with built-in contract validation and documentation
- **AWS Lambda**: Serverless functions for implementing API endpoints with contract compliance
- **Amazon S3**: Storage for API specifications, generated SDKs, and contract documentation
- **Amazon DynamoDB**: Storage for contract metadata, versioning information, and validation results
- **Amazon EventBridge**: Event-driven notifications for contract changes and validation results
- **AWS CodePipeline**: CI/CD pipelines with integrated contract testing and validation
- **AWS CodeBuild**: Build service for automated contract testing and SDK generation
- **Amazon CloudWatch**: Monitoring and logging for API contract compliance and performance
- **AWS X-Ray**: Distributed tracing for API request/response validation and debugging
- **Amazon SNS**: Notifications for contract validation failures and breaking changes
- **AWS Systems Manager**: Parameter store for API configuration and contract metadata
- **AWS Secrets Manager**: Secure storage of API keys and authentication credentials
- **Amazon CloudFront**: CDN for distributing API documentation and SDK downloads
- **AWS AppSync**: GraphQL APIs with built-in schema validation and contract enforcement
- **Amazon Cognito**: Authentication and authorization for API access control
- **AWS Step Functions**: Workflow orchestration for complex contract validation processes

## Benefits

- **Reliable Integration**: Clear contracts ensure consistent communication between services and clients
- **Independent Evolution**: Services can evolve independently while maintaining contract compatibility
- **Automated Validation**: Contract testing prevents breaking changes from reaching production
- **Improved Documentation**: Living documentation that stays synchronized with implementation
- **Faster Development**: Generated SDKs and clear contracts accelerate client development
- **Better Testing**: Contract-based testing ensures comprehensive API coverage
- **Version Management**: Structured approach to API versioning and backward compatibility
- **Reduced Integration Issues**: Early detection of contract violations prevents runtime failures
- **Enhanced Collaboration**: Clear contracts improve communication between teams
- **Quality Assurance**: Automated contract validation ensures API quality and consistency

## Related Resources

- [AWS Well-Architected Reliability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/)
- [Provide Service Contracts per API](https://docs.aws.amazon.com/wellarchitected/latest/framework/rel_service_architecture_api_contracts.html)
- [API Gateway Best Practices](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-basic-concept.html)
- [OpenAPI Specification](https://swagger.io/specification/)
- [Contract Testing with Pact](https://docs.pact.io/)
- [AWS Lambda Best Practices](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
- [API Versioning Strategies](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-usage-plans.html)
- [JSON Schema Validation](https://json-schema.org/)
- [Consumer-Driven Contract Testing](https://martinfowler.com/articles/consumerDrivenContracts.html)
- [API Design Guidelines](https://docs.aws.amazon.com/whitepapers/latest/api-design-guidance/)
- [Swagger Codegen](https://swagger.io/tools/swagger-codegen/)
- [AWS CodePipeline User Guide](https://docs.aws.amazon.com/codepipeline/latest/userguide/)
