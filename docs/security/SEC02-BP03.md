---
title: SEC02-BP03 - Store and use secrets securely
layout: default
parent: SEC02 - How do you manage identities for people and machines?
grand_parent: Security
nav_order: 3
---

<div class="pillar-header">
  <h1>SEC02-BP03: Store and use secrets securely</h1>
  <p>For workforce and machine identities that require secrets, such as passwords to third-party applications, store them with automatic rotation using the latest industry standards in a specialized service.</p>
</div>

## Implementation guidance

Secrets such as API keys, database passwords, and other credentials need to be stored securely and accessed only by authorized identities. Using a specialized service for secret management helps you protect sensitive information, implement automatic rotation, and maintain an audit trail of secret usage.

### Key steps for implementing this best practice:

1. **Identify and inventory all secrets**:
   - Document all secrets used in your environment
   - Identify where secrets are currently stored
   - Classify secrets based on sensitivity and usage
   - Determine which secrets need to be migrated to a secure storage solution
   - Identify secrets that can be replaced with temporary credentials

2. **Implement a secure secrets management solution**:
   - Use AWS Secrets Manager for storing and managing secrets
   - Configure AWS Systems Manager Parameter Store for less sensitive configuration data
   - Implement appropriate encryption for all stored secrets
   - Set up appropriate access controls and permissions
   - Enable detailed logging and monitoring

3. **Implement automatic secret rotation**:
   - Configure automatic rotation for database credentials
   - Set up rotation for API keys and other application secrets
   - Implement custom rotation functions for specialized secrets
   - Test rotation procedures to ensure application continuity
   - Monitor rotation events and failures

4. **Secure secret retrieval and usage**:
   - Use IAM roles to control access to secrets
   - Implement the principle of least privilege for secret access
   - Use VPC endpoints to access secrets without traversing the internet
   - Cache secrets appropriately to minimize retrieval calls
   - Implement secure coding practices for handling secrets in applications

5. **Monitor and audit secret access**:
   - Enable AWS CloudTrail logging for secret access
   - Set up alerts for unusual access patterns
   - Regularly review access logs
   - Implement detective controls to identify unauthorized access
   - Conduct periodic access reviews

6. **Eliminate hardcoded secrets**:
   - Scan code repositories for hardcoded secrets
   - Implement pre-commit hooks to prevent committing secrets
   - Use tools like git-secrets or Amazon CodeGuru to detect secrets in code
   - Educate developers on secure secret handling
   - Implement CI/CD pipeline checks for secrets

## Implementation examples

### Example 1: Storing and retrieving a secret with AWS Secrets Manager

```bash
# Store a new secret
aws secretsmanager create-secret \
  --name "prod/app/database-credentials" \
  --description "Database credentials for production application" \
  --secret-string '{"username":"admin","password":"t0p-S3cr3t!"}'

# Retrieve a secret
aws secretsmanager get-secret-value \
  --secret-id "prod/app/database-credentials"
```

### Example 2: Setting up automatic rotation for database credentials

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "secretsmanager:DescribeSecret",
        "secretsmanager:GetSecretValue",
        "secretsmanager:PutSecretValue",
        "secretsmanager:UpdateSecretVersionStage"
      ],
      "Resource": "arn:aws:secretsmanager:region:account-id:secret:prod/app/database-credentials-*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "rds:DescribeDBInstances"
      ],
      "Resource": "*"
    }
  ]
}
```

```bash
# Enable rotation with a Lambda function
aws secretsmanager rotate-secret \
  --secret-id "prod/app/database-credentials" \
  --rotation-lambda-arn "arn:aws:lambda:region:account-id:function:SecretsManagerRotationFunction" \
  --rotation-rules '{"AutomaticallyAfterDays": 30}'
```

### Example 3: Using AWS Secrets Manager with AWS SDK in an application

```python
import boto3
import json
from botocore.exceptions import ClientError

def get_secret(secret_name):
    """
    Retrieve a secret from AWS Secrets Manager
    """
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name='us-west-2'
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # Handle exceptions
        raise e
    else:
        # Decrypts secret using the associated KMS key
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
            return json.loads(secret)
        else:
            # Binary secrets
            return get_secret_value_response['SecretBinary']

# Example usage
try:
    db_credentials = get_secret("prod/app/database-credentials")
    username = db_credentials['username']
    password = db_credentials['password']
    # Use the credentials to connect to the database
except Exception as e:
    # Handle error
    print(f"Error retrieving secret: {e}")
```

## AWS services to consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Secrets Manager</h4>
    <p>Helps you protect secrets needed to access your applications, services, and IT resources. Enables you to rotate, manage, and retrieve database credentials, API keys, and other secrets throughout their lifecycle.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Systems Manager Parameter Store</h4>
    <p>Provides secure, hierarchical storage for configuration data management and secrets management. You can store data such as passwords, database strings, Amazon Machine Image (AMI) IDs, and license codes as parameter values.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Key Management Service (KMS)</h4>
    <p>Makes it easy for you to create and manage cryptographic keys and control their use across a wide range of AWS services and in your applications. Used by Secrets Manager to encrypt secrets.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Lambda</h4>
    <p>Lets you run code without provisioning or managing servers. Used by Secrets Manager for implementing custom secret rotation functions.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS CloudTrail</h4>
    <p>Records API calls for your account and delivers log files to you. Use CloudTrail to monitor secret access and detect unauthorized access attempts.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon CodeGuru</h4>
    <p>Uses machine learning to identify critical issues, security vulnerabilities, and hard-to-find bugs during application development. Can help identify hardcoded secrets in your code.</p>
  </div>
</div>

## Benefits of storing and using secrets securely

- **Enhanced security**: Centralized management of secrets with encryption at rest and in transit
- **Reduced risk of exposure**: Elimination of hardcoded secrets in application code and configuration files
- **Simplified secret rotation**: Automatic rotation of secrets without application downtime
- **Improved auditability**: Detailed logs of secret access and usage
- **Centralized control**: Manage all secrets from a single service
- **Fine-grained access control**: Control who can access which secrets
- **Compliance support**: Meet regulatory requirements for secure credential management

## Related resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/sec_identities_secrets.html">AWS Well-Architected Framework - Store and use secrets securely</a></li>
    <li><a href="https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html">AWS Secrets Manager User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html">AWS Systems Manager Parameter Store</a></li>
    <li><a href="https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets.html">Rotating your AWS Secrets Manager secrets</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-securely-provide-database-credentials-to-lambda-functions-by-using-aws-secrets-manager/">How to securely provide database credentials to Lambda functions by using AWS Secrets Manager</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-use-aws-secrets-manager-securely-store-rotate-database-credentials/">How to use AWS Secrets Manager to securely store and rotate database credentials</a></li>
  </ul>
</div>
