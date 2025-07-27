---
title: "SEC09-BP01: Implement secure key and certificate management"
layout: default
parent: "SEC09 - How do you protect your data in transit?"
grand_parent: Security
nav_order: 1
---

# SEC09-BP01: Implement secure key and certificate management

## Overview

Secure key and certificate management for data in transit ensures that cryptographic keys and digital certificates used for securing communications are properly generated, stored, distributed, rotated, and revoked throughout their lifecycle. This forms the foundation for all encryption in transit, including TLS/SSL connections, API authentication, and service-to-service communication.

Effective key and certificate management provides the cryptographic foundation for secure communications while ensuring scalability, automation, and compliance with security standards. It encompasses both symmetric keys for bulk encryption and asymmetric key pairs for authentication and key exchange.

## Implementation Guidance

### 1. Implement Centralized Certificate Management

Deploy comprehensive certificate lifecycle management:

- **AWS Certificate Manager (ACM)**: Centralized certificate provisioning and management
- **Automated Certificate Renewal**: Automatic renewal before expiration
- **Certificate Discovery**: Inventory and monitoring of all certificates
- **Certificate Validation**: Domain and organization validation processes

### 2. Establish Secure Key Generation and Storage

Implement secure cryptographic key management:

- **Hardware Security Modules (HSM)**: FIPS 140-2 Level 3 validated key storage
- **Key Generation**: Cryptographically secure random key generation
- **Key Escrow**: Secure backup and recovery of critical keys
- **Key Segregation**: Separate keys by environment and purpose

### 3. Deploy Automated Key and Certificate Rotation

Establish automated rotation processes:

- **Scheduled Rotation**: Regular rotation based on policy and risk assessment
- **Emergency Rotation**: Rapid rotation in case of compromise
- **Zero-Downtime Rotation**: Seamless rotation without service interruption
- **Rotation Validation**: Verification of successful rotation

### 4. Implement Certificate Authority (CA) Management

Manage certificate authorities and trust chains:

- **Private CA**: Internal certificate authority for private communications
- **Public CA Integration**: Integration with trusted public certificate authorities
- **Root CA Protection**: Secure storage and limited access to root CA keys
- **Intermediate CA Management**: Proper intermediate CA hierarchy

### 5. Enable Comprehensive Monitoring and Auditing

Deploy monitoring for keys and certificates:

- **Expiration Monitoring**: Alerts for approaching certificate expiration
- **Usage Auditing**: Comprehensive logging of key and certificate usage
- **Compliance Reporting**: Regular compliance assessments and reporting
- **Anomaly Detection**: Detection of unusual key or certificate usage patterns

### 6. Establish Key and Certificate Governance

Implement governance frameworks:

- **Policy Management**: Centralized policies for key and certificate management
- **Access Controls**: Strict access controls for key and certificate operations
- **Approval Workflows**: Approval processes for certificate requests and key operations
- **Compliance Integration**: Integration with regulatory and compliance requirements

## Implementation Examples

### Example 1: Comprehensive Certificate Management System

```python
# certificate_manager.py
import boto3
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import logging
import ssl
import socket
import OpenSSL
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class CertificateInfo:
    domain_name: str
    certificate_arn: str
    status: str
    issued_at: datetime
    expires_at: datetime
    issuer: str
    key_algorithm: str
    key_size: int
    signature_algorithm: str
    san_domains: List[str]
    validation_method: str

@dataclass
class CertificateRequest:
    domain_name: str
    subject_alternative_names: List[str]
    validation_method: str
    key_algorithm: str
    key_size: int
    certificate_authority: str
    tags: Dict[str, str]

class CertificateManager:
    """
    Comprehensive certificate management system for secure communications
    """
    
    def __init__(self, region: str = 'us-east-1'):
        self.region = region
        self.acm_client = boto3.client('acm', region_name=region)
        self.acm_pca_client = boto3.client('acm-pca', region_name=region)
        self.route53_client = boto3.client('route53', region_name=region)
        self.cloudwatch = boto3.client('cloudwatch', region_name=region)
        self.sns_client = boto3.client('sns', region_name=region)
        self.dynamodb = boto3.resource('dynamodb', region_name=region)
        
        # Certificate tracking table
        self.certificate_table = self.dynamodb.Table('certificate-management')
        
        # Certificate policies
        self.certificate_policies = self._define_certificate_policies()
    
    def _define_certificate_policies(self) -> Dict[str, Dict[str, Any]]:
        """
        Define certificate policies for different use cases
        """
        return {
            'web_server': {
                'key_algorithm': 'RSA',
                'key_size': 2048,
                'validity_period_days': 365,
                'renewal_threshold_days': 30,
                'validation_method': 'DNS',
                'required_extensions': ['key_usage', 'extended_key_usage'],
                'allowed_key_usage': ['digital_signature', 'key_encipherment'],
                'allowed_extended_key_usage': ['server_auth']
            },
            'client_auth': {
                'key_algorithm': 'RSA',
                'key_size': 2048,
                'validity_period_days': 180,
                'renewal_threshold_days': 14,
                'validation_method': 'EMAIL',
                'required_extensions': ['key_usage', 'extended_key_usage'],
                'allowed_key_usage': ['digital_signature', 'key_agreement'],
                'allowed_extended_key_usage': ['client_auth']
            },
            'code_signing': {
                'key_algorithm': 'RSA',
                'key_size': 3072,
                'validity_period_days': 1095,  # 3 years
                'renewal_threshold_days': 90,
                'validation_method': 'EMAIL',
                'required_extensions': ['key_usage', 'extended_key_usage'],
                'allowed_key_usage': ['digital_signature'],
                'allowed_extended_key_usage': ['code_signing']
            },
            'internal_service': {
                'key_algorithm': 'ECDSA',
                'key_size': 256,
                'validity_period_days': 90,
                'renewal_threshold_days': 7,
                'validation_method': 'DNS',
                'required_extensions': ['key_usage', 'extended_key_usage', 'subject_alt_name'],
                'allowed_key_usage': ['digital_signature', 'key_agreement'],
                'allowed_extended_key_usage': ['server_auth', 'client_auth']
            }
        }
    
    def request_certificate(self, request: CertificateRequest) -> Dict[str, Any]:
        """
        Request a new certificate through ACM
        """
        try:
            # Validate request against policy
            policy = self.certificate_policies.get(request.certificate_authority, 
                                                  self.certificate_policies['web_server'])
            
            validation_result = self._validate_certificate_request(request, policy)
            if not validation_result['valid']:
                return {
                    'status': 'error',
                    'message': f"Certificate request validation failed: {validation_result['errors']}"
                }
            
            # Prepare ACM request parameters
            request_params = {
                'DomainName': request.domain_name,
                'ValidationMethod': request.validation_method,
                'Tags': [{'Key': k, 'Value': v} for k, v in request.tags.items()]
            }
            
            # Add Subject Alternative Names if provided
            if request.subject_alternative_names:
                request_params['SubjectAlternativeNames'] = request.subject_alternative_names
            
            # Add domain validation options for DNS validation
            if request.validation_method == 'DNS':
                request_params['DomainValidationOptions'] = [
                    {
                        'DomainName': request.domain_name,
                        'ValidationDomain': request.domain_name
                    }
                ]
            
            # Request certificate from ACM
            response = self.acm_client.request_certificate(**request_params)
            certificate_arn = response['CertificateArn']
            
            # Track certificate request
            self._track_certificate_request(certificate_arn, request, policy)
            
            # Set up monitoring for the certificate
            self._setup_certificate_monitoring(certificate_arn, request.domain_name)
            
            logger.info(f"Certificate requested successfully: {certificate_arn}")
            
            return {
                'status': 'success',
                'certificate_arn': certificate_arn,
                'domain_name': request.domain_name,
                'validation_method': request.validation_method,
                'next_steps': self._get_validation_next_steps(request.validation_method, certificate_arn)
            }
            
        except Exception as e:
            logger.error(f"Error requesting certificate: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _validate_certificate_request(self, request: CertificateRequest, policy: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate certificate request against policy
        """
        validation_result = {
            'valid': True,
            'errors': []
        }
        
        # Validate key algorithm and size
        if request.key_algorithm != policy['key_algorithm']:
            validation_result['errors'].append(f"Key algorithm {request.key_algorithm} not allowed, must be {policy['key_algorithm']}")
        
        if request.key_size < policy['key_size']:
            validation_result['errors'].append(f"Key size {request.key_size} too small, minimum is {policy['key_size']}")
        
        # Validate domain name format
        if not self._is_valid_domain(request.domain_name):
            validation_result['errors'].append(f"Invalid domain name format: {request.domain_name}")
        
        # Validate SAN domains
        for san_domain in request.subject_alternative_names:
            if not self._is_valid_domain(san_domain):
                validation_result['errors'].append(f"Invalid SAN domain format: {san_domain}")
        
        # Check for duplicate certificate requests
        if self._certificate_exists(request.domain_name):
            validation_result['errors'].append(f"Active certificate already exists for domain: {request.domain_name}")
        
        validation_result['valid'] = len(validation_result['errors']) == 0
        return validation_result
    
    def _is_valid_domain(self, domain: str) -> bool:
        """
        Validate domain name format
        """
        import re
        domain_pattern = re.compile(
            r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)*[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$'
        )
        return bool(domain_pattern.match(domain)) and len(domain) <= 253
    
    def _certificate_exists(self, domain_name: str) -> bool:
        """
        Check if an active certificate already exists for the domain
        """
        try:
            certificates = self.acm_client.list_certificates(
                CertificateStatuses=['ISSUED', 'PENDING_VALIDATION']
            )
            
            for cert in certificates['CertificateSummaryList']:
                if cert['DomainName'] == domain_name:
                    return True
            
            return False
        except Exception:
            return False
    
    def get_certificate_inventory(self) -> Dict[str, Any]:
        """
        Get comprehensive inventory of all certificates
        """
        try:
            inventory = {
                'total_certificates': 0,
                'certificates_by_status': {},
                'expiring_soon': [],
                'certificates': [],
                'compliance_summary': {
                    'compliant': 0,
                    'non_compliant': 0,
                    'issues': []
                }
            }
            
            # Get all certificates from ACM
            certificates = self.acm_client.list_certificates()
            
            for cert_summary in certificates['CertificateSummaryList']:
                cert_arn = cert_summary['CertificateArn']
                
                # Get detailed certificate information
                cert_details = self.acm_client.describe_certificate(CertificateArn=cert_arn)
                cert_info = self._parse_certificate_details(cert_details['Certificate'])
                
                inventory['certificates'].append(cert_info)
                inventory['total_certificates'] += 1
                
                # Count by status
                status = cert_info.status
                inventory['certificates_by_status'][status] = \
                    inventory['certificates_by_status'].get(status, 0) + 1
                
                # Check for expiring certificates
                days_until_expiry = (cert_info.expires_at - datetime.utcnow()).days
                if days_until_expiry <= 30:
                    inventory['expiring_soon'].append({
                        'domain_name': cert_info.domain_name,
                        'certificate_arn': cert_info.certificate_arn,
                        'expires_at': cert_info.expires_at.isoformat(),
                        'days_until_expiry': days_until_expiry
                    })
                
                # Check compliance
                compliance_check = self._check_certificate_compliance(cert_info)
                if compliance_check['compliant']:
                    inventory['compliance_summary']['compliant'] += 1
                else:
                    inventory['compliance_summary']['non_compliant'] += 1
                    inventory['compliance_summary']['issues'].extend(compliance_check['issues'])
            
            return inventory
            
        except Exception as e:
            logger.error(f"Error getting certificate inventory: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _parse_certificate_details(self, cert_details: Dict[str, Any]) -> CertificateInfo:
        """
        Parse ACM certificate details into CertificateInfo object
        """
        return CertificateInfo(
            domain_name=cert_details['DomainName'],
            certificate_arn=cert_details['CertificateArn'],
            status=cert_details['Status'],
            issued_at=cert_details.get('IssuedAt', datetime.utcnow()),
            expires_at=cert_details.get('NotAfter', datetime.utcnow()),
            issuer=cert_details.get('Issuer', 'Unknown'),
            key_algorithm=cert_details.get('KeyAlgorithm', 'Unknown'),
            key_size=cert_details.get('KeyUsages', [{}])[0].get('Name', 0),
            signature_algorithm=cert_details.get('SignatureAlgorithm', 'Unknown'),
            san_domains=cert_details.get('SubjectAlternativeNames', []),
            validation_method=cert_details.get('Options', {}).get('ValidationMethod', 'Unknown')
        )
    
    def _check_certificate_compliance(self, cert_info: CertificateInfo) -> Dict[str, Any]:
        """
        Check certificate compliance against security policies
        """
        compliance_result = {
            'compliant': True,
            'issues': []
        }
        
        # Check key size
        min_key_sizes = {
            'RSA': 2048,
            'ECDSA': 256,
            'EC': 256
        }
        
        min_size = min_key_sizes.get(cert_info.key_algorithm, 2048)
        if cert_info.key_size < min_size:
            compliance_result['issues'].append(
                f"Key size {cert_info.key_size} below minimum {min_size} for {cert_info.key_algorithm}"
            )
        
        # Check expiration
        days_until_expiry = (cert_info.expires_at - datetime.utcnow()).days
        if days_until_expiry <= 0:
            compliance_result['issues'].append("Certificate has expired")
        elif days_until_expiry <= 30:
            compliance_result['issues'].append(f"Certificate expires in {days_until_expiry} days")
        
        # Check signature algorithm
        weak_algorithms = ['SHA1', 'MD5']
        if any(weak_alg in cert_info.signature_algorithm for weak_alg in weak_algorithms):
            compliance_result['issues'].append(f"Weak signature algorithm: {cert_info.signature_algorithm}")
        
        compliance_result['compliant'] = len(compliance_result['issues']) == 0
        return compliance_result
    
    def automate_certificate_renewal(self, certificate_arn: str) -> Dict[str, Any]:
        """
        Automate certificate renewal process
        """
        try:
            # Get certificate details
            cert_details = self.acm_client.describe_certificate(CertificateArn=certificate_arn)
            certificate = cert_details['Certificate']
            
            # Check if renewal is needed
            expires_at = certificate['NotAfter']
            days_until_expiry = (expires_at - datetime.utcnow()).days
            
            if days_until_expiry > 30:
                return {
                    'status': 'not_needed',
                    'message': f'Certificate does not need renewal yet. Expires in {days_until_expiry} days.',
                    'expires_at': expires_at.isoformat()
                }
            
            # For ACM-managed certificates, renewal is automatic
            if certificate.get('Type') == 'AMAZON_ISSUED':
                # Verify automatic renewal is enabled
                renewal_eligibility = self.acm_client.get_certificate(CertificateArn=certificate_arn)
                
                return {
                    'status': 'automatic',
                    'message': 'Certificate is managed by ACM and will be renewed automatically',
                    'expires_at': expires_at.isoformat(),
                    'renewal_eligible': renewal_eligibility.get('Certificate') is not None
                }
            
            # For imported certificates, manual renewal is required
            else:
                return {
                    'status': 'manual_required',
                    'message': 'Imported certificate requires manual renewal',
                    'expires_at': expires_at.isoformat(),
                    'action_required': 'Import new certificate before expiration'
                }
                
        except Exception as e:
            logger.error(f"Error in certificate renewal automation: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def validate_certificate_chain(self, certificate_arn: str) -> Dict[str, Any]:
        """
        Validate certificate chain and trust path
        """
        try:
            # Get certificate details
            cert_response = self.acm_client.get_certificate(CertificateArn=certificate_arn)
            certificate_pem = cert_response['Certificate']
            certificate_chain_pem = cert_response.get('CertificateChain', '')
            
            # Parse certificate
            certificate = x509.load_pem_x509_certificate(certificate_pem.encode())
            
            validation_result = {
                'certificate_arn': certificate_arn,
                'valid_chain': True,
                'issues': [],
                'certificate_details': {
                    'subject': certificate.subject.rfc4514_string(),
                    'issuer': certificate.issuer.rfc4514_string(),
                    'serial_number': str(certificate.serial_number),
                    'not_valid_before': certificate.not_valid_before.isoformat(),
                    'not_valid_after': certificate.not_valid_after.isoformat(),
                    'signature_algorithm': certificate.signature_algorithm_oid._name
                },
                'chain_validation': []
            }
            
            # Validate certificate dates
            now = datetime.utcnow()
            if certificate.not_valid_before > now:
                validation_result['issues'].append('Certificate is not yet valid')
                validation_result['valid_chain'] = False
            
            if certificate.not_valid_after < now:
                validation_result['issues'].append('Certificate has expired')
                validation_result['valid_chain'] = False
            
            # Validate certificate chain if present
            if certificate_chain_pem:
                chain_validation = self._validate_chain_certificates(certificate_chain_pem)
                validation_result['chain_validation'] = chain_validation
                
                if not chain_validation['valid']:
                    validation_result['issues'].extend(chain_validation['issues'])
                    validation_result['valid_chain'] = False
            
            # Validate key usage extensions
            key_usage_validation = self._validate_key_usage_extensions(certificate)
            if not key_usage_validation['valid']:
                validation_result['issues'].extend(key_usage_validation['issues'])
            
            return validation_result
            
        except Exception as e:
            logger.error(f"Error validating certificate chain: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _validate_chain_certificates(self, chain_pem: str) -> Dict[str, Any]:
        """
        Validate certificate chain
        """
        try:
            chain_validation = {
                'valid': True,
                'issues': [],
                'certificates_in_chain': 0
            }
            
            # Split chain into individual certificates
            chain_certs = []
            cert_blocks = chain_pem.split('-----END CERTIFICATE-----')
            
            for block in cert_blocks:
                if '-----BEGIN CERTIFICATE-----' in block:
                    cert_pem = block + '-----END CERTIFICATE-----'
                    try:
                        cert = x509.load_pem_x509_certificate(cert_pem.encode())
                        chain_certs.append(cert)
                    except Exception as e:
                        chain_validation['issues'].append(f'Invalid certificate in chain: {str(e)}')
                        chain_validation['valid'] = False
            
            chain_validation['certificates_in_chain'] = len(chain_certs)
            
            # Validate each certificate in chain
            for i, cert in enumerate(chain_certs):
                now = datetime.utcnow()
                
                if cert.not_valid_before > now:
                    chain_validation['issues'].append(f'Chain certificate {i+1} is not yet valid')
                    chain_validation['valid'] = False
                
                if cert.not_valid_after < now:
                    chain_validation['issues'].append(f'Chain certificate {i+1} has expired')
                    chain_validation['valid'] = False
            
            return chain_validation
            
        except Exception as e:
            return {
                'valid': False,
                'issues': [f'Chain validation error: {str(e)}'],
                'certificates_in_chain': 0
            }
    
    def _validate_key_usage_extensions(self, certificate: x509.Certificate) -> Dict[str, Any]:
        """
        Validate key usage extensions
        """
        validation_result = {
            'valid': True,
            'issues': []
        }
        
        try:
            # Check for Key Usage extension
            try:
                key_usage = certificate.extensions.get_extension_for_oid(x509.oid.ExtensionOID.KEY_USAGE).value
                
                # Validate key usage for different certificate types
                if key_usage.digital_signature and key_usage.key_encipherment:
                    # Valid for server certificates
                    pass
                elif key_usage.digital_signature and key_usage.key_agreement:
                    # Valid for client certificates
                    pass
                else:
                    validation_result['issues'].append('Unusual key usage combination detected')
                    
            except x509.ExtensionNotFound:
                validation_result['issues'].append('Key Usage extension not found')
                validation_result['valid'] = False
            
            # Check for Extended Key Usage extension
            try:
                ext_key_usage = certificate.extensions.get_extension_for_oid(x509.oid.ExtensionOID.EXTENDED_KEY_USAGE).value
                
                # Common extended key usage OIDs
                server_auth_oid = x509.oid.ExtendedKeyUsageOID.SERVER_AUTH
                client_auth_oid = x509.oid.ExtendedKeyUsageOID.CLIENT_AUTH
                
                if server_auth_oid not in ext_key_usage and client_auth_oid not in ext_key_usage:
                    validation_result['issues'].append('Certificate lacks common extended key usage')
                    
            except x509.ExtensionNotFound:
                validation_result['issues'].append('Extended Key Usage extension not found')
            
        except Exception as e:
            validation_result['issues'].append(f'Key usage validation error: {str(e)}')
            validation_result['valid'] = False
        
        validation_result['valid'] = len(validation_result['issues']) == 0
        return validation_result
    
    def _track_certificate_request(self, certificate_arn: str, request: CertificateRequest, policy: Dict[str, Any]):
        """
        Track certificate request in DynamoDB
        """
        try:
            self.certificate_table.put_item(
                Item={
                    'certificate_arn': certificate_arn,
                    'domain_name': request.domain_name,
                    'request_timestamp': datetime.utcnow().isoformat(),
                    'validation_method': request.validation_method,
                    'key_algorithm': request.key_algorithm,
                    'key_size': request.key_size,
                    'certificate_authority': request.certificate_authority,
                    'policy_applied': policy,
                    'tags': request.tags,
                    'ttl': int((datetime.utcnow() + timedelta(days=1095)).timestamp())  # 3 years
                }
            )
        except Exception as e:
            logger.error(f"Error tracking certificate request: {str(e)}")
    
    def _setup_certificate_monitoring(self, certificate_arn: str, domain_name: str):
        """
        Set up CloudWatch monitoring for certificate
        """
        try:
            # Create custom metric for certificate expiration
            self.cloudwatch.put_metric_data(
                Namespace='AWS/CertificateManager',
                MetricData=[
                    {
                        'MetricName': 'CertificateRequested',
                        'Dimensions': [
                            {
                                'Name': 'DomainName',
                                'Value': domain_name
                            }
                        ],
                        'Value': 1,
                        'Unit': 'Count'
                    }
                ]
            )
            
            logger.info(f"Set up monitoring for certificate: {domain_name}")
            
        except Exception as e:
            logger.error(f"Error setting up certificate monitoring: {str(e)}")
    
    def _get_validation_next_steps(self, validation_method: str, certificate_arn: str) -> List[str]:
        """
        Get next steps for certificate validation
        """
        if validation_method == 'DNS':
            return [
                "1. Retrieve DNS validation records from ACM",
                "2. Add CNAME records to your DNS configuration",
                "3. Wait for DNS propagation and ACM validation",
                "4. Certificate will be issued automatically upon successful validation"
            ]
        elif validation_method == 'EMAIL':
            return [
                "1. Check email for validation messages",
                "2. Click validation links in the emails",
                "3. Complete email validation process",
                "4. Certificate will be issued upon successful validation"
            ]
        else:
            return [
                "1. Follow ACM console instructions for validation",
                "2. Complete required validation steps",
                "3. Monitor certificate status in ACM"
            ]

# Example usage
if __name__ == "__main__":
    # Initialize certificate manager
    cert_manager = CertificateManager()
    
    # Create certificate request
    cert_request = CertificateRequest(
        domain_name='api.example.com',
        subject_alternative_names=['www.api.example.com', 'dev.api.example.com'],
        validation_method='DNS',
        key_algorithm='RSA',
        key_size=2048,
        certificate_authority='web_server',
        tags={
            'Environment': 'Production',
            'Application': 'API Gateway',
            'Owner': 'DevOps Team'
        }
    )
    
    # Request certificate
    request_result = cert_manager.request_certificate(cert_request)
    print(f"Certificate request result: {json.dumps(request_result, indent=2, default=str)}")
    
    # Get certificate inventory
    inventory = cert_manager.get_certificate_inventory()
    print(f"Certificate inventory: {json.dumps(inventory, indent=2, default=str)}")
    
    # Validate certificate chain (if certificate exists)
    if request_result.get('status') == 'success':
        validation_result = cert_manager.validate_certificate_chain(request_result['certificate_arn'])
        print(f"Certificate validation: {json.dumps(validation_result, indent=2, default=str)}")
```

### Example 2: Private Certificate Authority Management

```python
# private_ca_manager.py
import boto3
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

@dataclass
class CAConfiguration:
    ca_name: str
    ca_type: str  # ROOT or SUBORDINATE
    key_algorithm: str
    key_size: int
    signing_algorithm: str
    subject: Dict[str, str]
    validity_period_years: int
    crl_configuration: Dict[str, Any]
    ocsp_configuration: Dict[str, Any]

class PrivateCAManager:
    """
    Manages AWS Private Certificate Authority for internal certificate issuance
    """
    
    def __init__(self, region: str = 'us-east-1'):
        self.region = region
        self.acm_pca_client = boto3.client('acm-pca', region_name=region)
        self.s3_client = boto3.client('s3', region_name=region)
        self.iam_client = boto3.client('iam', region_name=region)
        self.cloudwatch = boto3.client('cloudwatch', region_name=region)
        self.dynamodb = boto3.resource('dynamodb', region_name=region)
        
        # CA tracking table
        self.ca_table = self.dynamodb.Table('private-ca-management')
    
    def create_private_ca(self, ca_config: CAConfiguration) -> Dict[str, Any]:
        """
        Create a new private certificate authority
        """
        try:
            # Prepare CA configuration
            ca_configuration = {
                'KeyAlgorithm': ca_config.key_algorithm,
                'KeySize': ca_config.key_size,
                'SigningAlgorithm': ca_config.signing_algorithm,
                'Subject': {
                    'Country': ca_config.subject.get('country', 'US'),
                    'Organization': ca_config.subject.get('organization', 'Example Corp'),
                    'OrganizationalUnit': ca_config.subject.get('organizational_unit', 'IT Department'),
                    'State': ca_config.subject.get('state', 'Washington'),
                    'Locality': ca_config.subject.get('locality', 'Seattle'),
                    'CommonName': ca_config.subject.get('common_name', ca_config.ca_name)
                }
            }
            
            # Create the CA
            response = self.acm_pca_client.create_certificate_authority(
                CertificateAuthorityConfiguration=ca_configuration,
                CertificateAuthorityType=ca_config.ca_type,
                IdempotencyToken=f"{ca_config.ca_name}-{int(datetime.utcnow().timestamp())}",
                Tags=[
                    {'Key': 'Name', 'Value': ca_config.ca_name},
                    {'Key': 'Type', 'Value': ca_config.ca_type},
                    {'Key': 'CreatedBy', 'Value': 'PrivateCAManager'}
                ]
            )
            
            ca_arn = response['CertificateAuthorityArn']
            
            # Configure CRL if specified
            if ca_config.crl_configuration:
                self._configure_crl(ca_arn, ca_config.crl_configuration)
            
            # Configure OCSP if specified
            if ca_config.ocsp_configuration:
                self._configure_ocsp(ca_arn, ca_config.ocsp_configuration)
            
            # Track CA creation
            self._track_ca_creation(ca_arn, ca_config)
            
            logger.info(f"Created private CA: {ca_arn}")
            
            return {
                'status': 'success',
                'ca_arn': ca_arn,
                'ca_name': ca_config.ca_name,
                'ca_type': ca_config.ca_type,
                'next_steps': self._get_ca_next_steps(ca_config.ca_type)
            }
            
        except Exception as e:
            logger.error(f"Error creating private CA: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _configure_crl(self, ca_arn: str, crl_config: Dict[str, Any]):
        """
        Configure Certificate Revocation List for the CA
        """
        try:
            crl_configuration = {
                'Enabled': crl_config.get('enabled', True),
                'ExpirationInDays': crl_config.get('expiration_days', 7),
                'CustomCname': crl_config.get('custom_cname'),
                'S3BucketName': crl_config.get('s3_bucket_name')
            }
            
            # Remove None values
            crl_configuration = {k: v for k, v in crl_configuration.items() if v is not None}
            
            self.acm_pca_client.put_policy(
                ResourceArn=ca_arn,
                Policy=json.dumps({
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Principal": {"Service": "acm-pca.amazonaws.com"},
                            "Action": "s3:PutObject",
                            "Resource": f"arn:aws:s3:::{crl_config['s3_bucket_name']}/*"
                        },
                        {
                            "Effect": "Allow",
                            "Principal": {"Service": "acm-pca.amazonaws.com"},
                            "Action": "s3:GetBucketAcl",
                            "Resource": f"arn:aws:s3:::{crl_config['s3_bucket_name']}"
                        }
                    ]
                })
            )
            
            logger.info(f"Configured CRL for CA: {ca_arn}")
            
        except Exception as e:
            logger.error(f"Error configuring CRL: {str(e)}")
    
    def _configure_ocsp(self, ca_arn: str, ocsp_config: Dict[str, Any]):
        """
        Configure OCSP (Online Certificate Status Protocol) for the CA
        """
        try:
            ocsp_configuration = {
                'Enabled': ocsp_config.get('enabled', True),
                'OcspCustomCname': ocsp_config.get('custom_cname')
            }
            
            # OCSP configuration is typically handled through CA configuration
            # This is a placeholder for OCSP-specific configuration
            logger.info(f"OCSP configuration prepared for CA: {ca_arn}")
            
        except Exception as e:
            logger.error(f"Error configuring OCSP: {str(e)}")
    
    def issue_certificate(self, 
                         ca_arn: str, 
                         csr: str, 
                         template_arn: str,
                         validity_period_days: int = 365) -> Dict[str, Any]:
        """
        Issue a certificate from the private CA
        """
        try:
            # Issue certificate
            response = self.acm_pca_client.issue_certificate(
                CertificateAuthorityArn=ca_arn,
                Csr=csr.encode(),
                SigningAlgorithm='SHA256WITHRSA',
                TemplateArn=template_arn,
                Validity={
                    'Value': validity_period_days,
                    'Type': 'DAYS'
                },
                IdempotencyToken=f"cert-{int(datetime.utcnow().timestamp())}"
            )
            
            certificate_arn = response['CertificateArn']
            
            # Wait for certificate to be issued
            waiter = self.acm_pca_client.get_waiter('certificate_issued')
            waiter.wait(
                CertificateAuthorityArn=ca_arn,
                CertificateArn=certificate_arn,
                WaiterConfig={
                    'Delay': 5,
                    'MaxAttempts': 60
                }
            )
            
            # Get the issued certificate
            cert_response = self.acm_pca_client.get_certificate(
                CertificateAuthorityArn=ca_arn,
                CertificateArn=certificate_arn
            )
            
            logger.info(f"Issued certificate: {certificate_arn}")
            
            return {
                'status': 'success',
                'certificate_arn': certificate_arn,
                'certificate': cert_response['Certificate'],
                'certificate_chain': cert_response['CertificateChain']
            }
            
        except Exception as e:
            logger.error(f"Error issuing certificate: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def revoke_certificate(self, ca_arn: str, certificate_arn: str, revocation_reason: str) -> Dict[str, Any]:
        """
        Revoke a certificate issued by the private CA
        """
        try:
            # Map revocation reasons to ACM PCA values
            reason_mapping = {
                'unspecified': 'UNSPECIFIED',
                'key_compromise': 'KEY_COMPROMISE',
                'ca_compromise': 'CERTIFICATE_AUTHORITY_COMPROMISE',
                'affiliation_changed': 'AFFILIATION_CHANGED',
                'superseded': 'SUPERSEDED',
                'cessation_of_operation': 'CESSATION_OF_OPERATION',
                'privilege_withdrawn': 'PRIVILEGE_WITHDRAWN',
                'aa_compromise': 'A_A_COMPROMISE'
            }
            
            acm_reason = reason_mapping.get(revocation_reason, 'UNSPECIFIED')
            
            # Revoke the certificate
            self.acm_pca_client.revoke_certificate(
                CertificateAuthorityArn=ca_arn,
                CertificateSerial=self._get_certificate_serial(ca_arn, certificate_arn),
                RevocationReason=acm_reason
            )
            
            logger.info(f"Revoked certificate: {certificate_arn}")
            
            return {
                'status': 'success',
                'certificate_arn': certificate_arn,
                'revocation_reason': revocation_reason,
                'revoked_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error revoking certificate: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _get_certificate_serial(self, ca_arn: str, certificate_arn: str) -> str:
        """
        Get certificate serial number
        """
        try:
            response = self.acm_pca_client.get_certificate(
                CertificateAuthorityArn=ca_arn,
                CertificateArn=certificate_arn
            )
            
            # Parse certificate to get serial number
            from cryptography import x509
            certificate = x509.load_pem_x509_certificate(response['Certificate'].encode())
            return str(certificate.serial_number)
            
        except Exception as e:
            logger.error(f"Error getting certificate serial: {str(e)}")
            return ""
    
    def get_ca_status(self, ca_arn: str) -> Dict[str, Any]:
        """
        Get comprehensive status of a private CA
        """
        try:
            # Get CA details
            response = self.acm_pca_client.describe_certificate_authority(
                CertificateAuthorityArn=ca_arn
            )
            
            ca_details = response['CertificateAuthority']
            
            status_info = {
                'ca_arn': ca_arn,
                'status': ca_details['Status'],
                'type': ca_details['Type'],
                'key_algorithm': ca_details['CertificateAuthorityConfiguration']['KeyAlgorithm'],
                'signing_algorithm': ca_details['CertificateAuthorityConfiguration']['SigningAlgorithm'],
                'subject': ca_details['CertificateAuthorityConfiguration']['Subject'],
                'created_at': ca_details.get('CreatedAt', '').isoformat() if ca_details.get('CreatedAt') else '',
                'not_before': ca_details.get('NotBefore', '').isoformat() if ca_details.get('NotBefore') else '',
                'not_after': ca_details.get('NotAfter', '').isoformat() if ca_details.get('NotAfter') else '',
                'serial': ca_details.get('Serial', ''),
                'revocation_configuration': ca_details.get('RevocationConfiguration', {}),
                'restore_expiry_time': ca_details.get('RestorableUntil', '').isoformat() if ca_details.get('RestorableUntil') else ''
            }
            
            # Get certificate count
            try:
                cert_list = self.acm_pca_client.list_certificates(
                    CertificateAuthorityArn=ca_arn
                )
                status_info['issued_certificates_count'] = len(cert_list['Certificates'])
            except:
                status_info['issued_certificates_count'] = 0
            
            return status_info
            
        except Exception as e:
            logger.error(f"Error getting CA status: {str(e)}")
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _track_ca_creation(self, ca_arn: str, ca_config: CAConfiguration):
        """
        Track CA creation in DynamoDB
        """
        try:
            self.ca_table.put_item(
                Item={
                    'ca_arn': ca_arn,
                    'ca_name': ca_config.ca_name,
                    'ca_type': ca_config.ca_type,
                    'created_timestamp': datetime.utcnow().isoformat(),
                    'key_algorithm': ca_config.key_algorithm,
                    'key_size': ca_config.key_size,
                    'signing_algorithm': ca_config.signing_algorithm,
                    'validity_period_years': ca_config.validity_period_years,
                    'subject': ca_config.subject,
                    'ttl': int((datetime.utcnow() + timedelta(days=ca_config.validity_period_years * 365)).timestamp())
                }
            )
        except Exception as e:
            logger.error(f"Error tracking CA creation: {str(e)}")
    
    def _get_ca_next_steps(self, ca_type: str) -> List[str]:
        """
        Get next steps after CA creation
        """
        if ca_type == 'ROOT':
            return [
                "1. Install and activate the root CA certificate",
                "2. Configure certificate templates for different use cases",
                "3. Set up monitoring and alerting for the CA",
                "4. Create subordinate CAs if needed",
                "5. Establish certificate issuance procedures"
            ]
        else:  # SUBORDINATE
            return [
                "1. Get the CA certificate signed by the parent CA",
                "2. Install the signed CA certificate",
                "3. Configure certificate templates",
                "4. Set up certificate issuance procedures",
                "5. Configure CRL and OCSP endpoints"
            ]

# Example usage
if __name__ == "__main__":
    # Initialize private CA manager
    ca_manager = PrivateCAManager()
    
    # Create root CA configuration
    root_ca_config = CAConfiguration(
        ca_name='CompanyRootCA',
        ca_type='ROOT',
        key_algorithm='RSA_2048',
        key_size=2048,
        signing_algorithm='SHA256WITHRSA',
        subject={
            'country': 'US',
            'organization': 'Example Corporation',
            'organizational_unit': 'IT Security',
            'state': 'Washington',
            'locality': 'Seattle',
            'common_name': 'Example Corp Root CA'
        },
        validity_period_years=10,
        crl_configuration={
            'enabled': True,
            'expiration_days': 7,
            's3_bucket_name': 'company-ca-crl-bucket'
        },
        ocsp_configuration={
            'enabled': True,
            'custom_cname': 'ocsp.example.com'
        }
    )
    
    # Create the root CA
    ca_result = ca_manager.create_private_ca(root_ca_config)
    print(f"CA creation result: {json.dumps(ca_result, indent=2)}")
    
    # Get CA status
    if ca_result.get('status') == 'success':
        status = ca_manager.get_ca_status(ca_result['ca_arn'])
        print(f"CA status: {json.dumps(status, indent=2)}")
```

### Example 3: CloudFormation Template for Certificate Infrastructure

```yaml
# certificate-infrastructure.yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Comprehensive certificate management infrastructure'

Parameters:
  Environment:
    Type: String
    Default: 'prod'
    AllowedValues: ['dev', 'staging', 'prod']
  
  DomainName:
    Type: String
    Description: 'Primary domain name for certificate'
  
  SubjectAlternativeNames:
    Type: CommaDelimitedList
    Description: 'Subject Alternative Names for certificate'
    Default: ''

Resources:
  # S3 bucket for CRL storage
  CRLBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub '${Environment}-ca-crl-${AWS::AccountId}'
      BucketEncryption:
        ServerSideEncryptionConfiguration:
          - ServerSideEncryptionByDefault:
              SSEAlgorithm: AES256
      PublicAccessBlockConfiguration:
        BlockPublicAcls: false
        BlockPublicPolicy: false
        IgnorePublicAcls: false
        RestrictPublicBuckets: false
      CorsConfiguration:
        CorsRules:
          - AllowedHeaders: ['*']
            AllowedMethods: [GET]
            AllowedOrigins: ['*']
            MaxAge: 3600

  # S3 bucket policy for CRL access
  CRLBucketPolicy:
    Type: AWS::S3::BucketPolicy
    Properties:
      Bucket: !Ref CRLBucket
      PolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Sid: AllowPublicRead
            Effect: Allow
            Principal: '*'
            Action: 's3:GetObject'
            Resource: !Sub '${CRLBucket}/*'
          - Sid: AllowACMPCAAccess
            Effect: Allow
            Principal:
              Service: acm-pca.amazonaws.com
            Action:
              - 's3:PutObject'
              - 's3:GetBucketAcl'
              - 's3:GetBucketLocation'
            Resource:
              - !Sub '${CRLBucket}'
              - !Sub '${CRLBucket}/*'

  # Private Certificate Authority
  PrivateCA:
    Type: AWS::ACMPCA::CertificateAuthority
    Properties:
      Type: ROOT
      KeyAlgorithm: RSA_2048
      SigningAlgorithm: SHA256WITHRSA
      Subject:
        Country: US
        Organization: !Sub '${Environment} Organization'
        OrganizationalUnit: IT Security
        State: Washington
        Locality: Seattle
        CommonName: !Sub '${Environment} Root CA'
      RevocationConfiguration:
        CrlConfiguration:
          Enabled: true
          ExpirationInDays: 7
          S3BucketName: !Ref CRLBucket
          S3ObjectAcl: PUBLIC_READ
      Tags:
        - Key: Environment
          Value: !Ref Environment
        - Key: Purpose
          Value: RootCA

  # CA Certificate
  CACertificate:
    Type: AWS::ACMPCA::Certificate
    Properties:
      CertificateAuthorityArn: !Ref PrivateCA
      CertificateSigningRequest: !GetAtt PrivateCA.CertificateSigningRequest
      SigningAlgorithm: SHA256WITHRSA
      TemplateArn: 'arn:aws:acm-pca:::template/RootCACertificate/V1'
      Validity:
        Type: YEARS
        Value: 10

  # Activate the CA
  CAActivation:
    Type: AWS::ACMPCA::CertificateAuthorityActivation
    Properties:
      CertificateAuthorityArn: !Ref PrivateCA
      Certificate: !GetAtt CACertificate.Certificate
      Status: ACTIVE

  # Public certificate from ACM
  PublicCertificate:
    Type: AWS::CertificateManager::Certificate
    Properties:
      DomainName: !Ref DomainName
      SubjectAlternativeNames: !Ref SubjectAlternativeNames
      ValidationMethod: DNS
      DomainValidationOptions:
        - DomainName: !Ref DomainName
          HostedZoneId: !Ref HostedZone
      Tags:
        - Key: Environment
          Value: !Ref Environment
        - Key: CertificateType
          Value: Public

  # Route53 Hosted Zone for DNS validation
  HostedZone:
    Type: AWS::Route53::HostedZone
    Properties:
      Name: !Ref DomainName
      HostedZoneConfig:
        Comment: !Sub 'Hosted zone for ${DomainName}'
      HostedZoneTags:
        - Key: Environment
          Value: !Ref Environment

  # DynamoDB table for certificate tracking
  CertificateTrackingTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: !Sub '${Environment}-certificate-management'
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: certificate_arn
          AttributeType: S
        - AttributeName: domain_name
          AttributeType: S
      KeySchema:
        - AttributeName: certificate_arn
          KeyType: HASH
      GlobalSecondaryIndexes:
        - IndexName: DomainNameIndex
          KeySchema:
            - AttributeName: domain_name
              KeyType: HASH
          Projection:
            ProjectionType: ALL
      TimeToLiveSpecification:
        AttributeName: ttl
        Enabled: true
      StreamSpecification:
        StreamViewType: NEW_AND_OLD_IMAGES

  # Lambda function for certificate monitoring
  CertificateMonitorFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: !Sub '${Environment}-certificate-monitor'
      Runtime: python3.9
      Handler: index.lambda_handler
      Role: !GetAtt CertificateMonitorRole.Arn
      Timeout: 300
      Environment:
        Variables:
          CERTIFICATE_TABLE: !Ref CertificateTrackingTable
          SNS_TOPIC_ARN: !Ref CertificateAlertsTopic
      Code:
        ZipFile: |
          import boto3
          import json
          import os
          from datetime import datetime, timedelta
          
          def lambda_handler(event, context):
              """Monitor certificates for expiration and compliance"""
              
              acm = boto3.client('acm')
              dynamodb = boto3.resource('dynamodb')
              sns = boto3.client('sns')
              
              table = dynamodb.Table(os.environ['CERTIFICATE_TABLE'])
              topic_arn = os.environ['SNS_TOPIC_ARN']
              
              try:
                  # Get all certificates
                  certificates = acm.list_certificates()
                  
                  alerts = []
                  
                  for cert_summary in certificates['CertificateSummaryList']:
                      cert_arn = cert_summary['CertificateArn']
                      
                      # Get certificate details
                      cert_details = acm.describe_certificate(CertificateArn=cert_arn)
                      certificate = cert_details['Certificate']
                      
                      # Check expiration
                      not_after = certificate.get('NotAfter')
                      if not_after:
                          days_until_expiry = (not_after - datetime.utcnow()).days
                          
                          if days_until_expiry <= 30:
                              alerts.append({
                                  'certificate_arn': cert_arn,
                                  'domain_name': certificate['DomainName'],
                                  'days_until_expiry': days_until_expiry,
                                  'expires_at': not_after.isoformat()
                              })
                      
                      # Update tracking table
                      table.put_item(
                          Item={
                              'certificate_arn': cert_arn,
                              'domain_name': certificate['DomainName'],
                              'status': certificate['Status'],
                              'expires_at': not_after.isoformat() if not_after else '',
                              'last_checked': datetime.utcnow().isoformat(),
                              'ttl': int((datetime.utcnow() + timedelta(days=90)).timestamp())
                          }
                      )
                  
                  # Send alerts if any certificates are expiring
                  if alerts:
                      message = {
                          'alert_type': 'certificate_expiration',
                          'certificates': alerts,
                          'timestamp': datetime.utcnow().isoformat()
                      }
                      
                      sns.publish(
                          TopicArn=topic_arn,
                          Message=json.dumps(message, indent=2),
                          Subject=f'Certificate Expiration Alert - {len(alerts)} certificates expiring soon'
                      )
                  
                  return {
                      'statusCode': 200,
                      'body': json.dumps({
                          'certificates_checked': len(certificates['CertificateSummaryList']),
                          'expiring_certificates': len(alerts)
                      })
                  }
                  
              except Exception as e:
                  return {
                      'statusCode': 500,
                      'body': json.dumps({'error': str(e)})
                  }

  # IAM role for certificate monitor function
  CertificateMonitorRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
      Policies:
        - PolicyName: CertificateMonitorPolicy
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - 'acm:ListCertificates'
                  - 'acm:DescribeCertificate'
                  - 'acm-pca:ListCertificateAuthorities'
                  - 'acm-pca:DescribeCertificateAuthority'
                Resource: '*'
              - Effect: Allow
                Action:
                  - 'dynamodb:PutItem'
                  - 'dynamodb:GetItem'
                  - 'dynamodb:UpdateItem'
                Resource: !GetAtt CertificateTrackingTable.Arn
              - Effect: Allow
                Action:
                  - 'sns:Publish'
                Resource: !Ref CertificateAlertsTopic

  # EventBridge rule for scheduled certificate monitoring
  CertificateMonitorSchedule:
    Type: AWS::Events::Rule
    Properties:
      Name: !Sub '${Environment}-certificate-monitor-schedule'
      ScheduleExpression: 'rate(1 day)'
      State: ENABLED
      Targets:
        - Arn: !GetAtt CertificateMonitorFunction.Arn
          Id: CertificateMonitorTarget

  # Permission for EventBridge to invoke Lambda
  CertificateMonitorPermission:
    Type: AWS::Lambda::Permission
    Properties:
      FunctionName: !Ref CertificateMonitorFunction
      Action: lambda:InvokeFunction
      Principal: events.amazonaws.com
      SourceArn: !GetAtt CertificateMonitorSchedule.Arn

  # SNS topic for certificate alerts
  CertificateAlertsTopic:
    Type: AWS::SNS::Topic
    Properties:
      TopicName: !Sub '${Environment}-certificate-alerts'
      DisplayName: 'Certificate Management Alerts'

  # CloudWatch dashboard for certificate monitoring
  CertificateDashboard:
    Type: AWS::CloudWatch::Dashboard
    Properties:
      DashboardName: !Sub '${Environment}-certificate-management'
      DashboardBody: !Sub |
        {
          "widgets": [
            {
              "type": "metric",
              "x": 0,
              "y": 0,
              "width": 12,
              "height": 6,
              "properties": {
                "metrics": [
                  [ "AWS/Lambda", "Invocations", "FunctionName", "${CertificateMonitorFunction}" ],
                  [ ".", "Errors", ".", "." ],
                  [ ".", "Duration", ".", "." ]
                ],
                "period": 300,
                "stat": "Sum",
                "region": "${AWS::Region}",
                "title": "Certificate Monitor Function Metrics"
              }
            },
            {
              "type": "metric",
              "x": 12,
              "y": 0,
              "width": 12,
              "height": 6,
              "properties": {
                "metrics": [
                  [ "AWS/CertificateManager", "DaysToExpiry", "CertificateArn", "${PublicCertificate}" ]
                ],
                "period": 86400,
                "stat": "Average",
                "region": "${AWS::Region}",
                "title": "Certificate Days to Expiry"
              }
            }
          ]
        }

Outputs:
  PrivateCAArn:
    Description: 'ARN of the private certificate authority'
    Value: !Ref PrivateCA
    Export:
      Name: !Sub '${AWS::StackName}-PrivateCA'
  
  PublicCertificateArn:
    Description: 'ARN of the public certificate'
    Value: !Ref PublicCertificate
    Export:
      Name: !Sub '${AWS::StackName}-PublicCertificate'
  
  CRLBucketName:
    Description: 'Name of the CRL S3 bucket'
    Value: !Ref CRLBucket
    Export:
      Name: !Sub '${AWS::StackName}-CRLBucket'
  
  CertificateTrackingTableName:
    Description: 'Name of the certificate tracking table'
    Value: !Ref CertificateTrackingTable
    Export:
      Name: !Sub '${AWS::StackName}-CertificateTable'
  
  CertificateMonitorFunctionArn:
    Description: 'ARN of the certificate monitor function'
    Value: !GetAtt CertificateMonitorFunction.Arn
    Export:
      Name: !Sub '${AWS::StackName}-MonitorFunction'
```

## Relevant AWS Services

### Certificate Management Services
- **AWS Certificate Manager (ACM)**: Managed certificate provisioning, deployment, and renewal
- **AWS Certificate Manager Private Certificate Authority**: Private CA for internal certificates
- **AWS Secrets Manager**: Secure storage of private keys and certificate materials
- **AWS Systems Manager Parameter Store**: Configuration storage for certificate parameters

### Key Management and Security
- **AWS Key Management Service (KMS)**: Encryption key management for certificate protection
- **AWS CloudHSM**: Hardware security modules for high-security key storage
- **AWS Identity and Access Management (IAM)**: Access control for certificate operations
- **AWS Organizations**: Service Control Policies for certificate governance

### Monitoring and Automation
- **Amazon CloudWatch**: Certificate expiration monitoring and alerting
- **AWS Lambda**: Automated certificate management and monitoring functions
- **Amazon EventBridge**: Event-driven certificate lifecycle automation
- **Amazon SNS**: Certificate alert notifications

### DNS and Networking
- **Amazon Route 53**: DNS validation for certificate requests
- **AWS Global Accelerator**: Certificate deployment for global applications
- **Amazon CloudFront**: CDN certificate management
- **Elastic Load Balancing**: Load balancer certificate integration

## Benefits of Secure Key and Certificate Management

### Security Benefits
- **Strong Cryptographic Foundation**: Proper key generation and storage using HSMs
- **Certificate Lifecycle Management**: Automated renewal and rotation processes
- **Trust Chain Validation**: Comprehensive certificate chain verification
- **Revocation Management**: Efficient certificate revocation and CRL distribution

### Operational Benefits
- **Automated Renewal**: Elimination of certificate expiration outages
- **Centralized Management**: Single point of control for all certificates
- **Scalable Architecture**: Support for thousands of certificates and domains
- **Integration Capabilities**: Seamless integration with AWS services

### Compliance Benefits
- **Regulatory Adherence**: Support for industry-specific certificate requirements
- **Audit Trails**: Comprehensive logging of all certificate operations
- **Policy Enforcement**: Automated enforcement of certificate policies
- **Documentation**: Complete certificate inventory and compliance reporting

### Cost Benefits
- **Reduced Operational Overhead**: Automated certificate management processes
- **Elimination of Outages**: Prevention of certificate expiration incidents
- **Efficient Resource Utilization**: Optimized certificate deployment and management
- **Scalable Economics**: Cost-effective certificate management at scale

## Related Resources

- [AWS Well-Architected Framework - Data in Transit Protection](https://docs.aws.amazon.com/wellarchitected/latest/framework/sec-09.html)
- [AWS Certificate Manager User Guide](https://docs.aws.amazon.com/acm/latest/userguide/acm-overview.html)
- [AWS Certificate Manager Private Certificate Authority User Guide](https://docs.aws.amazon.com/acm-pca/latest/userguide/PcaWelcome.html)
- [AWS Key Management Service Developer Guide](https://docs.aws.amazon.com/kms/latest/developerguide/overview.html)
- [TLS Best Practices](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/create-https-listener.html#describe-ssl-policies)
- [Certificate Transparency](https://docs.aws.amazon.com/acm/latest/userguide/acm-concepts.html#concept-transparency)
```
```
