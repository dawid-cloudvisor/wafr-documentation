---
title: "SEC09-BP03: Authenticate network communications"
layout: default
parent: "SEC09 - How do you protect your data in transit?"
grand_parent: Security
nav_order: 3
---

# SEC09-BP03: Authenticate network communications

## Overview

Verify the identity of communications by using protocols that support authentication, such as Transport Layer Security (TLS) or IPsec.

Design your workload to use secure, authenticated network protocols whenever communicating between services, applications, or to users. Using network protocols that support authentication and authorization provides stronger control over network flows and reduces the impact of unauthorized access.

**Desired outcome:** A workload with well-defined data plane and control plane traffic flows between services. The traffic flows use authenticated and encrypted network protocols where technically feasible.

**Common anti-patterns:**
- Unencrypted or unauthenticated traffic flows within your workload
- Reusing authentication credentials across multiple users or entities
- Relying solely on network controls as an access control mechanism
- Creating a custom authentication mechanism rather than relying on industry-standard authentication mechanisms
- Overly permissive traffic flows between service components or other resources in the VPC

**Benefits of establishing this best practice:**
- Limits the scope of impact for unauthorized access to one part of the workload
- Provides a higher level of assurance that actions are only performed by authenticated entities
- Improves decoupling of services by clearly defining and enforcing intended data transfer interfaces
- Enhances monitoring, logging, and incident response through request attribution and well-defined communication interfaces
- Provides defense-in-depth for your workloads by combining network controls with authentication and authorization controls

**Level of risk exposed if this best practice is not established:** Low

## Implementation Guidance

Your workload's network traffic patterns can be characterized into two categories:

- **East-west traffic** represents traffic flows between services that make up a workload
- **North-south traffic** represents traffic flows between your workload and consumers

While it is common practice to encrypt north-south traffic, securing east-west traffic using authenticated protocols is less common. Modern security practices recommend that network design alone does not grant a trusted relationship between two entities. When two services may reside within a common network boundary, it is still best practice to encrypt, authenticate, and authorize communications between those services.

As an example, AWS service APIs use the [AWS Signature Version 4 (SigV4)](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-signing.html) signature protocol to authenticate the caller, no matter what network the request originates from. This authentication ensures that AWS APIs can verify the identity that requested the action, and that identity can then be combined with policies to make an authorization decision to determine whether the action should be allowed or not.

Services such as [Amazon VPC Lattice](https://docs.aws.amazon.com/vpc-lattice/latest/ug/access-management-overview.html) and [Amazon API Gateway](https://docs.aws.amazon.com/apigateway/latest/developerguide/permissions.html) allow you use the same SigV4 signature protocol to add authentication and authorization to east-west traffic in your own workloads. If resources outside of your AWS environment need to communicate with services that require SigV4-based authentication and authorization, you can use [AWS Identity and Access Management (IAM) Roles Anywhere](https://docs.aws.amazon.com/rolesanywhere/latest/userguide/introduction.html) on the non-AWS resource to acquire temporary AWS credentials. These credentials can be used to sign requests to services using SigV4 to authorize access.

Another common mechanism for authenticating east-west traffic is TLS mutual authentication (mTLS). Many Internet of Things (IoT), business-to-business applications, and microservices use mTLS to validate the identity of both sides of a TLS communication through the use of both client and server-side X.509 certificates. These certificates can be issued by AWS Private Certificate Authority (AWS Private CA). You can use services such as [Amazon API Gateway](https://docs.aws.amazon.com/apigateway/latest/developerguide/rest-api-mutual-tls.html) to provide mTLS authentication for inter- or intra-workload communication. [Application Load Balancer also supports mTLS](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/mutual-authentication.html) for internal or external facing workloads. While mTLS provides authentication information for both sides of a TLS communication, it does not provide a mechanism for authorization.

Finally, OAuth 2.0 and OpenID Connect (OIDC) are two protocols typically used for controlling access to services by users, but are now becoming popular for service-to-service traffic as well. API Gateway provides a [JSON Web Token (JWT) authorizer](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-jwt-authorizer.html), allowing workloads to restrict access to API routes using JWTs issued from OIDC or OAuth 2.0 identity providers. OAuth2 scopes can be used as a source for basic authorization decisions, but the authorization checks still need to be implemented in the application layer, and OAuth2 scopes alone cannot support more complex authorization needs.

### Implementation Steps

1. **Define and document your workload network flows:** The first step in implementing a defense-in-depth strategy is defining your workload's traffic flows.
   - Create a data flow diagram that clearly defines how data is transmitted between different services that comprise your workload. This diagram is the first step to enforcing those flows through authenticated network channels.
   - Instrument your workload in development and testing phases to validate that the data flow diagram accurately reflects the workload's behavior at runtime.
   - A data flow diagram can also be useful when performing a threat modeling exercise, as described in [SEC01-BP07 Identify threats and prioritize mitigations using a threat model](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/sec_securely_operate_threat_model.html).

2. **Establish network controls:** Consider AWS capabilities to establish network controls aligned to your data flows. While network boundaries should not be the only security control, they provide a layer in the defense-in-depth strategy to protect your workload.
   - Use [security groups](https://docs.aws.amazon.com/vpc/latest/userguide/security-groups.html) to establish define and restrict data flows between resources.
   - Consider using [AWS PrivateLink](https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html) to communicate with both AWS and third-party services that support AWS PrivateLink. Data sent through a AWS PrivateLink interface endpoint stays within the AWS network backbone and does not traverse the public Internet.

3. **Implement authentication and authorization across services in your workload:** Choose the set of AWS services most appropriate to provide authenticated, encrypted traffic flows in your workload.
   - Consider [Amazon VPC Lattice](https://docs.aws.amazon.com/vpc-lattice/latest/ug/what-is-vpc-lattice.html) to secure service-to-service communication. VPC Lattice can use [SigV4 authentication combined with auth policies](https://docs.aws.amazon.com/vpc-lattice/latest/ug/auth-policies.html) to control service-to-service access.
   - For service-to-service communication using mTLS, consider [API Gateway](https://docs.aws.amazon.com/apigateway/latest/developerguide/rest-api-mutual-tls.html), [Application Load Balancer](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/mutual-authentication.html). [AWS Private CA](https://docs.aws.amazon.com/privateca/latest/userguide/PcaWelcome.html) can be used to establish a private CA hierarchy capable of issuing certificates for use with mTLS.
   - When integrating with services using OAuth 2.0 or OIDC, consider [API Gateway using the JWT authorizer](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-jwt-authorizer.html).
   - For communication between your workload and IoT devices, consider [AWS IoT Core](https://docs.aws.amazon.com/iot/latest/developerguide/client-authentication.html), which provides several options for network traffic encryption and authentication.

4. **Monitor for unauthorized access:** Continually monitor for unintended communication channels, unauthorized principals attempting to access protected resources, and other improper access patterns.
   - If using VPC Lattice to manage access to your services, consider enabling and monitoring [VPC Lattice access logs](https://docs.aws.amazon.com/vpc-lattice/latest/ug/monitoring-access-logs.html). These access logs include information on the requesting entity, network information including source and destination VPC, and request metadata.
   - Consider enabling [VPC flow logs](https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html) to capture metadata on network flows and periodically review for anomalies.
   - Refer to the [AWS Security Incident Response Guide](https://docs.aws.amazon.com/whitepapers/latest/aws-security-incident-response-guide/aws-security-incident-response-guide.html) and the [Incident Response section](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/incident-response.html) of the AWS Well-Architected Framework security pillar for more guidance on planning, simulating, and responding to security incidents.

## Implementation Examples

### Example 1: VPC Lattice with SigV4 Authentication

```python
# vpc_lattice_auth_example.py
import boto3
import json
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class VPCLatticeAuthManager:
    """
    Example implementation for VPC Lattice with SigV4 authentication
    """
    
    def __init__(self, region: str = 'us-east-1'):
        self.region = region
        self.vpc_lattice_client = boto3.client('vpc-lattice', region_name=region)
        self.iam_client = boto3.client('iam', region_name=region)
    
    def create_service_network_with_auth(self, service_network_name: str, auth_type: str = 'AWS_IAM'):
        """
        Create a VPC Lattice service network with authentication
        """
        try:
            response = self.vpc_lattice_client.create_service_network(
                name=service_network_name,
                authType=auth_type,
                tags={
                    'Purpose': 'Authenticated Service Communication',
                    'SecurityLevel': 'High'
                }
            )
            
            service_network_arn = response['arn']
            
            # Create auth policy for the service network
            auth_policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": {
                            "AWS": "*"
                        },
                        "Action": "vpc-lattice-svcs:Invoke",
                        "Resource": "*",
                        "Condition": {
                            "StringEquals": {
                                "vpc-lattice-svcs:ServiceNetworkArn": service_network_arn
                            }
                        }
                    }
                ]
            }
            
            # Apply the auth policy
            self.vpc_lattice_client.put_auth_policy(
                resourceIdentifier=service_network_arn,
                policy=json.dumps(auth_policy)
            )
            
            logger.info(f"Created service network with authentication: {service_network_arn}")
            return service_network_arn
            
        except Exception as e:
            logger.error(f"Error creating service network: {str(e)}")
            raise

# Example usage
if __name__ == "__main__":
    auth_manager = VPCLatticeAuthManager()
    service_network_arn = auth_manager.create_service_network_with_auth("secure-microservices")
```

### Example 2: API Gateway with mTLS Authentication

```python
# api_gateway_mtls_example.py
import boto3
import json
from typing import Dict, Any

class APIGatewayMTLSManager:
    """
    Example implementation for API Gateway with mutual TLS authentication
    """
    
    def __init__(self, region: str = 'us-east-1'):
        self.region = region
        self.apigateway_client = boto3.client('apigateway', region_name=region)
        self.acm_client = boto3.client('acm', region_name=region)
    
    def create_api_with_mtls(self, api_name: str, domain_name: str, certificate_arn: str):
        """
        Create API Gateway with mutual TLS authentication
        """
        try:
            # Create the REST API
            api_response = self.apigateway_client.create_rest_api(
                name=api_name,
                description='API with mutual TLS authentication',
                policy=json.dumps({
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Principal": "*",
                            "Action": "execute-api:Invoke",
                            "Resource": "*",
                            "Condition": {
                                "Bool": {
                                    "aws:SecureTransport": "true"
                                }
                            }
                        }
                    ]
                }),
                tags={
                    'Authentication': 'mTLS',
                    'SecurityLevel': 'High'
                }
            )
            
            api_id = api_response['id']
            
            # Create domain name with mTLS
            domain_response = self.apigateway_client.create_domain_name(
                domainName=domain_name,
                certificateArn=certificate_arn,
                securityPolicy='TLS_1_2',
                mutualTlsAuthentication={
                    'truststoreUri': f's3://my-truststore-bucket/truststore.pem',
                    'truststoreVersion': '1'
                },
                tags={
                    'API': api_name,
                    'mTLS': 'enabled'
                }
            )
            
            logger.info(f"Created API with mTLS: {api_id}")
            return {
                'api_id': api_id,
                'domain_name': domain_name,
                'certificate_arn': certificate_arn
            }
            
        except Exception as e:
            logger.error(f"Error creating API with mTLS: {str(e)}")
            raise

# Example usage
if __name__ == "__main__":
    mtls_manager = APIGatewayMTLSManager()
    result = mtls_manager.create_api_with_mtls(
        "secure-api",
        "api.example.com",
        "arn:aws:acm:us-east-1:123456789012:certificate/12345678-1234-1234-1234-123456789012"
    )
```

### Example 3: Application Load Balancer with mTLS

```python
# alb_mtls_example.py
import boto3
from typing import List, Dict, Any

class ALBMTLSManager:
    """
    Example implementation for Application Load Balancer with mutual TLS
    """
    
    def __init__(self, region: str = 'us-east-1'):
        self.region = region
        self.elbv2_client = boto3.client('elbv2', region_name=region)
        self.acm_client = boto3.client('acm', region_name=region)
    
    def create_alb_with_mtls(self, 
                            alb_name: str,
                            subnet_ids: List[str],
                            security_group_ids: List[str],
                            certificate_arn: str,
                            truststore_s3_bucket: str,
                            truststore_s3_key: str):
        """
        Create Application Load Balancer with mutual TLS authentication
        """
        try:
            # Create the load balancer
            lb_response = self.elbv2_client.create_load_balancer(
                Name=alb_name,
                Subnets=subnet_ids,
                SecurityGroups=security_group_ids,
                Scheme='internet-facing',
                Tags=[
                    {'Key': 'Authentication', 'Value': 'mTLS'},
                    {'Key': 'SecurityLevel', 'Value': 'High'}
                ],
                Type='application',
                IpAddressType='ipv4'
            )
            
            lb_arn = lb_response['LoadBalancers'][0]['LoadBalancerArn']
            
            # Create target group
            tg_response = self.elbv2_client.create_target_group(
                Name=f'{alb_name}-tg',
                Protocol='HTTPS',
                Port=443,
                VpcId=subnet_ids[0].split('-')[0],  # Simplified VPC ID extraction
                HealthCheckProtocol='HTTPS',
                HealthCheckPath='/health',
                Tags=[
                    {'Key': 'LoadBalancer', 'Value': alb_name}
                ]
            )
            
            tg_arn = tg_response['TargetGroups'][0]['TargetGroupArn']
            
            # Create HTTPS listener with mTLS
            listener_response = self.elbv2_client.create_listener(
                LoadBalancerArn=lb_arn,
                Protocol='HTTPS',
                Port=443,
                Certificates=[
                    {
                        'CertificateArn': certificate_arn
                    }
                ],
                SslPolicy='ELBSecurityPolicy-TLS-1-2-2017-01',
                DefaultActions=[
                    {
                        'Type': 'forward',
                        'TargetGroupArn': tg_arn
                    }
                ],
                MutualAuthentication={
                    'Mode': 'verify',
                    'TrustStoreArn': f'arn:aws:elasticloadbalancing:{self.region}:123456789012:truststore/{alb_name}-truststore'
                },
                Tags=[
                    {'Key': 'mTLS', 'Value': 'enabled'}
                ]
            )
            
            logger.info(f"Created ALB with mTLS: {lb_arn}")
            return {
                'load_balancer_arn': lb_arn,
                'target_group_arn': tg_arn,
                'listener_arn': listener_response['Listeners'][0]['ListenerArn']
            }
            
        except Exception as e:
            logger.error(f"Error creating ALB with mTLS: {str(e)}")
            raise

# Example usage
if __name__ == "__main__":
    alb_manager = ALBMTLSManager()
    result = alb_manager.create_alb_with_mtls(
        "secure-alb",
        ["subnet-12345", "subnet-67890"],
        ["sg-12345"],
        "arn:aws:acm:us-east-1:123456789012:certificate/12345678-1234-1234-1234-123456789012",
        "my-truststore-bucket",
        "truststore.pem"
    )
```

## Resources

### Related Best Practices

- [SEC03-BP07 Analyze public and cross-account access](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/sec_permissions_analyze_cross_account.html)
- [SEC02-BP02 Use temporary credentials](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/sec_identities_unique.html)
- [SEC01-BP07 Identify threats and prioritize mitigations using a threat model](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/sec_securely_operate_threat_model.html)

### Related Documents

- [Evaluating access control methods to secure Amazon API Gateway APIs](https://aws.amazon.com/blogs/compute/evaluating-access-control-methods-to-secure-amazon-api-gateway-apis/)
- [Configuring mutual TLS authentication for a REST API](https://docs.aws.amazon.com/apigateway/latest/developerguide/rest-api-mutual-tls.html)
- [How to secure API Gateway HTTP endpoints with JWT authorizer](https://aws.amazon.com/blogs/security/how-to-secure-api-gateway-http-endpoints-with-jwt-authorizer/)
- [Authorizing direct calls to AWS services using AWS IoT Core credential provider](https://docs.aws.amazon.com/iot/latest/developerguide/authorizing-direct-aws.html)
- [AWS Security Incident Response Guide](https://docs.aws.amazon.com/whitepapers/latest/aws-security-incident-response-guide/aws-security-incident-response-guide.html)

### Related Videos

- [AWS re:invent 2022: Introducing VPC Lattice](https://www.youtube.com/watch?v=fRjD1JI0H5w)
- [AWS re:invent 2020: Serverless API authentication for HTTP APIs on AWS](https://www.youtube.com/watch?v=AW4kvUkUKZ0)

### Related Examples

- [Amazon VPC Lattice Workshop](https://catalog.us-east-1.prod.workshops.aws/workshops/9e543f60-e409-43d4-b37f-78ff3e1a07f5/en-US)
- [Zero-Trust Episode 1 – The Phantom Service Perimeter workshop](https://catalog.us-east-1.prod.workshops.aws/workshops/dc413216-deab-4371-9e4a-879a4f14233d/en-US)
