---
title: SEC07-BP01 - Understand your data classification scheme
layout: default
parent: SEC07 - How do you classify your data?
grand_parent: Security
nav_order: 1
---

<div class="pillar-header">
  <h1>SEC07-BP01: Understand your data classification scheme</h1>
  <p>Data classification provides a way to categorize organizational data based on levels of sensitivity and criticality to help you determine appropriate protection and retention controls. Develop a data classification scheme that is aligned to your organization's risk tolerance and regulatory requirements. Ensure that your classification scheme is well-documented, consistently applied, and regularly reviewed.</p>
</div>

## Implementation guidance

Understanding your data classification scheme is the foundation of an effective data protection strategy. A well-designed classification scheme enables you to apply appropriate security controls, meet regulatory requirements, and make informed decisions about data handling throughout its lifecycle.

### Key steps for implementing this best practice:

1. **Define data classification levels**:
   - Establish clear classification categories based on sensitivity and business impact
   - Define criteria for each classification level
   - Align classifications with regulatory and compliance requirements
   - Consider business impact of unauthorized disclosure, modification, or loss
   - Document classification definitions and examples

2. **Identify data types and sources**:
   - Catalog all types of data your organization processes
   - Identify data sources and collection points
   - Map data flows and processing activities
   - Document data ownership and stewardship responsibilities
   - Understand data dependencies and relationships

3. **Establish classification criteria and procedures**:
   - Create decision trees and guidelines for classification
   - Define roles and responsibilities for data classification
   - Establish processes for initial classification and re-classification
   - Implement quality assurance and validation procedures
   - Create training materials and awareness programs

4. **Align with regulatory and compliance requirements**:
   - Map classification levels to regulatory frameworks
   - Understand data residency and sovereignty requirements
   - Identify cross-border data transfer restrictions
   - Document compliance obligations for each classification level
   - Establish audit and reporting procedures

5. **Implement classification governance**:
   - Establish data governance committees and roles
   - Create policies and procedures for data classification
   - Implement approval workflows for classification changes
   - Establish exception handling and escalation procedures
   - Regular review and update of classification schemes

6. **Enable classification automation and tooling**:
   - Implement automated data discovery and classification tools
   - Integrate classification with data management systems
   - Use metadata and tagging for classification tracking
   - Implement policy enforcement based on classification
   - Establish monitoring and reporting capabilities

## Implementation examples

### Example 1: Data classification scheme definition

```yaml
# Data Classification Scheme Configuration
data_classification_scheme:
  name: "Corporate Data Classification Framework"
  version: "2.0"
  effective_date: "2024-01-01"
  review_cycle: "annual"
  
  classification_levels:
    public:
      level: 1
      label: "Public"
      color_code: "#4CAF50"  # Green
      description: "Information that can be freely shared with the public"
      criteria:
        - "No harm to organization if disclosed"
        - "Already publicly available or intended for public release"
        - "Marketing materials, press releases, public website content"
      examples:
        - "Company brochures and marketing materials"
        - "Public website content"
        - "Press releases and public announcements"
        - "Published research papers"
      handling_requirements:
        access_control: "None required"
        encryption: "Not required"
        retention: "As per business needs"
        disposal: "Standard disposal methods"
      regulatory_considerations: []
      
    internal:
      level: 2
      label: "Internal"
      color_code: "#2196F3"  # Blue
      description: "Information for internal use within the organization"
      criteria:
        - "Limited harm if disclosed outside organization"
        - "Intended for internal business operations"
        - "General business information not requiring special protection"
      examples:
        - "Internal policies and procedures"
        - "Employee directories"
        - "General business correspondence"
        - "Non-sensitive project documentation"
      handling_requirements:
        access_control: "Organization members only"
        encryption: "Recommended for transmission"
        retention: "As per retention policy"
        disposal: "Secure disposal methods"
      regulatory_considerations:
        - "May be subject to discovery in legal proceedings"
        
    confidential:
      level: 3
      label: "Confidential"
      color_code: "#FF9800"  # Orange
      description: "Sensitive information requiring protection from unauthorized disclosure"
      criteria:
        - "Significant harm if disclosed to unauthorized parties"
        - "Competitive advantage or proprietary information"
        - "Personal information of employees or customers"
      examples:
        - "Financial reports and budgets"
        - "Customer lists and contact information"
        - "Employee personal information"
        - "Vendor contracts and agreements"
        - "Strategic business plans"
      handling_requirements:
        access_control: "Need-to-know basis with approval"
        encryption: "Required for storage and transmission"
        retention: "Minimum retention as required by law/business"
        disposal: "Certified secure destruction"
      regulatory_considerations:
        - "May be subject to privacy regulations"
        - "Requires breach notification procedures"
        
    restricted:
      level: 4
      label: "Restricted"
      color_code: "#F44336"  # Red
      description: "Highly sensitive information requiring the highest level of protection"
      criteria:
        - "Severe harm if disclosed to unauthorized parties"
        - "Regulated data with specific compliance requirements"
        - "Trade secrets and intellectual property"
      examples:
        - "Social Security Numbers and government IDs"
        - "Payment card information"
        - "Health records and medical information"
        - "Trade secrets and proprietary algorithms"
        - "Legal privileged communications"
      handling_requirements:
        access_control: "Explicit authorization required"
        encryption: "Strong encryption mandatory"
        retention: "Strict retention limits"
        disposal: "Certified destruction with audit trail"
      regulatory_considerations:
        - "Subject to GDPR, HIPAA, PCI DSS, or other regulations"
        - "Mandatory breach notification requirements"
        - "May require data residency controls"

  special_categories:
    pii:
      name: "Personally Identifiable Information"
      description: "Information that can identify a specific individual"
      minimum_classification: "confidential"
      additional_requirements:
        - "Privacy impact assessment required"
        - "Consent management procedures"
        - "Data subject rights procedures"
        
    phi:
      name: "Protected Health Information"
      description: "Health information protected under HIPAA"
      minimum_classification: "restricted"
      additional_requirements:
        - "HIPAA compliance procedures"
        - "Business associate agreements"
        - "Audit logging requirements"
        
    pci:
      name: "Payment Card Information"
      description: "Credit card and payment information"
      minimum_classification: "restricted"
      additional_requirements:
        - "PCI DSS compliance"
        - "Tokenization or encryption"
        - "Regular security assessments"

  classification_procedures:
    initial_classification:
      responsible_party: "Data owner"
      approval_required: true
      documentation: "Classification rationale must be documented"
      
    reclassification:
      trigger_events:
        - "Change in data sensitivity"
        - "New regulatory requirements"
        - "Business process changes"
      approval_authority: "Data governance committee"
      
    quality_assurance:
      review_frequency: "quarterly"
      sampling_methodology: "Risk-based sampling"
      validation_procedures: "Independent review and validation"

  governance:
    data_governance_committee:
      chair: "Chief Data Officer"
      members:
        - "Chief Information Security Officer"
        - "Chief Privacy Officer"
        - "Legal Counsel"
        - "Business Unit Representatives"
      meeting_frequency: "monthly"
      
    roles_and_responsibilities:
      data_owner:
        - "Assign initial classification"
        - "Approve access requests"
        - "Review classification periodically"
      data_steward:
        - "Implement classification decisions"
        - "Monitor data usage and access"
        - "Report classification issues"
      data_custodian:
        - "Apply technical controls based on classification"
        - "Implement data handling procedures"
        - "Maintain audit logs"

  compliance_mapping:
    gdpr:
      applicable_classifications: ["confidential", "restricted"]
      requirements:
        - "Lawful basis for processing"
        - "Data subject rights procedures"
        - "Breach notification within 72 hours"
        
    hipaa:
      applicable_classifications: ["restricted"]
      requirements:
        - "Administrative, physical, and technical safeguards"
        - "Business associate agreements"
        - "Audit controls and integrity"
        
    pci_dss:
      applicable_classifications: ["restricted"]
      requirements:
        - "Secure network and systems"
        - "Protect cardholder data"
        - "Regular monitoring and testing"
```

### Example 2: Automated data classification with Amazon Macie

```python
import boto3
import json
from datetime import datetime
import logging

class DataClassificationManager:
    """Automated data classification using Amazon Macie and custom logic"""
    
    def __init__(self, region='us-west-2'):
        self.macie = boto3.client('macie2', region_name=region)
        self.s3 = boto3.client('s3', region_name=region)
        self.region = region
        self.logger = logging.getLogger(__name__)
        
        # Classification scheme mapping
        self.classification_mapping = {
            'PUBLIC': {
                'level': 1,
                'tag_value': 'Public',
                'encryption_required': False,
                'access_logging': False
            },
            'INTERNAL': {
                'level': 2,
                'tag_value': 'Internal',
                'encryption_required': True,
                'access_logging': True
            },
            'CONFIDENTIAL': {
                'level': 3,
                'tag_value': 'Confidential',
                'encryption_required': True,
                'access_logging': True
            },
            'RESTRICTED': {
                'level': 4,
                'tag_value': 'Restricted',
                'encryption_required': True,
                'access_logging': True
            }
        }
    
    def setup_macie_classification(self):
        """Set up Amazon Macie for automated data classification"""
        
        try:
            # Enable Macie if not already enabled
            try:
                self.macie.get_macie_session()
                self.logger.info("Macie is already enabled")
            except self.macie.exceptions.ResourceNotFoundException:
                self.macie.enable_macie()
                self.logger.info("Enabled Amazon Macie")
            
            # Create custom data identifier for organization-specific data
            custom_identifier = self.macie.create_custom_data_identifier(
                name='OrganizationEmployeeID',
                description='Custom identifier for employee IDs',
                regex=r'EMP-\d{6}',
                keywords=['employee', 'staff', 'personnel'],
                tags={
                    'Purpose': 'DataClassification',
                    'DataType': 'EmployeeID'
                }
            )
            
            self.logger.info(f"Created custom data identifier: {custom_identifier['customDataIdentifierId']}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error setting up Macie: {str(e)}")
            return False
    
    def classify_s3_bucket(self, bucket_name):
        """Classify data in an S3 bucket using Macie"""
        
        try:
            # Create classification job
            job_response = self.macie.create_classification_job(
                jobType='ONE_TIME',
                name=f'classification-job-{bucket_name}-{datetime.now().strftime("%Y%m%d-%H%M%S")}',
                description=f'Data classification job for bucket {bucket_name}',
                s3JobDefinition={
                    'bucketDefinitions': [
                        {
                            'accountId': boto3.client('sts').get_caller_identity()['Account'],
                            'buckets': [bucket_name]
                        }
                    ]
                },
                tags={
                    'Purpose': 'DataClassification',
                    'Bucket': bucket_name
                }
            )
            
            job_id = job_response['jobId']
            self.logger.info(f"Created classification job: {job_id}")
            
            return job_id
            
        except Exception as e:
            self.logger.error(f"Error creating classification job: {str(e)}")
            return None
    
    def get_classification_results(self, job_id):
        """Get results from Macie classification job"""
        
        try:
            # Get job status
            job_details = self.macie.describe_classification_job(jobId=job_id)
            
            if job_details['jobStatus'] != 'COMPLETE':
                return {'status': job_details['jobStatus'], 'results': None}
            
            # Get findings
            findings_response = self.macie.list_findings(
                findingCriteria={
                    'criterion': {
                        'classificationDetails.jobId': {
                            'eq': [job_id]
                        }
                    }
                }
            )
            
            findings = []
            for finding_id in findings_response['findingIds']:
                finding_details = self.macie.get_findings(findingIds=[finding_id])
                findings.extend(finding_details['findings'])
            
            return {'status': 'COMPLETE', 'results': findings}
            
        except Exception as e:
            self.logger.error(f"Error getting classification results: {str(e)}")
            return {'status': 'ERROR', 'results': None}
    
    def apply_classification_tags(self, bucket_name, object_key, classification_level):
        """Apply classification tags to S3 objects"""
        
        try:
            classification_config = self.classification_mapping.get(classification_level.upper())
            
            if not classification_config:
                self.logger.warning(f"Unknown classification level: {classification_level}")
                return False
            
            # Apply object tags
            self.s3.put_object_tagging(
                Bucket=bucket_name,
                Key=object_key,
                Tagging={
                    'TagSet': [
                        {
                            'Key': 'DataClassification',
                            'Value': classification_config['tag_value']
                        },
                        {
                            'Key': 'ClassificationLevel',
                            'Value': str(classification_config['level'])
                        },
                        {
                            'Key': 'ClassificationDate',
                            'Value': datetime.now().isoformat()
                        },
                        {
                            'Key': 'EncryptionRequired',
                            'Value': str(classification_config['encryption_required'])
                        }
                    ]
                }
            )
            
            self.logger.info(f"Applied classification tags to {bucket_name}/{object_key}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error applying classification tags: {str(e)}")
            return False
    
    def classify_based_on_content(self, findings):
        """Determine classification level based on Macie findings"""
        
        classification_scores = {
            'PUBLIC': 0,
            'INTERNAL': 0,
            'CONFIDENTIAL': 0,
            'RESTRICTED': 0
        }
        
        for finding in findings:
            # Check for sensitive data types
            if 'sensitiveData' in finding:
                for sensitive_data in finding['sensitiveData']:
                    category = sensitive_data.get('category', '')
                    
                    if category in ['PII', 'PERSONAL_INFORMATION']:
                        classification_scores['CONFIDENTIAL'] += 10
                    elif category in ['FINANCIAL_INFORMATION', 'CREDENTIALS']:
                        classification_scores['RESTRICTED'] += 20
                    elif category in ['HEALTH_INFORMATION']:
                        classification_scores['RESTRICTED'] += 25
                    else:
                        classification_scores['INTERNAL'] += 5
            
            # Check severity
            severity = finding.get('severity', {}).get('description', 'LOW')
            if severity == 'HIGH':
                classification_scores['RESTRICTED'] += 15
            elif severity == 'MEDIUM':
                classification_scores['CONFIDENTIAL'] += 10
            elif severity == 'LOW':
                classification_scores['INTERNAL'] += 5
        
        # Determine final classification
        max_score = max(classification_scores.values())
        if max_score == 0:
            return 'PUBLIC'
        
        for classification, score in classification_scores.items():
            if score == max_score:
                return classification
        
        return 'INTERNAL'  # Default fallback
    
    def generate_classification_report(self, bucket_name, job_id):
        """Generate a classification report for a bucket"""
        
        try:
            results = self.get_classification_results(job_id)
            
            if results['status'] != 'COMPLETE':
                return {'error': f"Job not complete. Status: {results['status']}"}
            
            findings = results['results']
            
            # Analyze findings
            classification_summary = {
                'PUBLIC': 0,
                'INTERNAL': 0,
                'CONFIDENTIAL': 0,
                'RESTRICTED': 0
            }
            
            object_classifications = {}
            
            for finding in findings:
                resource_arn = finding.get('resourcesAffected', {}).get('s3Object', {}).get('key', '')
                classification = self.classify_based_on_content([finding])
                
                object_classifications[resource_arn] = {
                    'classification': classification,
                    'finding_id': finding.get('id'),
                    'severity': finding.get('severity', {}).get('description', 'LOW'),
                    'sensitive_data_types': []
                }
                
                # Extract sensitive data types
                if 'sensitiveData' in finding:
                    for sensitive_data in finding['sensitiveData']:
                        object_classifications[resource_arn]['sensitive_data_types'].append(
                            sensitive_data.get('category', 'UNKNOWN')
                        )
                
                classification_summary[classification] += 1
            
            # Generate report
            report = {
                'bucket_name': bucket_name,
                'job_id': job_id,
                'scan_date': datetime.now().isoformat(),
                'total_objects_scanned': len(object_classifications),
                'classification_summary': classification_summary,
                'object_classifications': object_classifications,
                'recommendations': self.generate_recommendations(classification_summary)
            }
            
            return report
            
        except Exception as e:
            self.logger.error(f"Error generating classification report: {str(e)}")
            return {'error': str(e)}
    
    def generate_recommendations(self, classification_summary):
        """Generate recommendations based on classification results"""
        
        recommendations = []
        
        if classification_summary['RESTRICTED'] > 0:
            recommendations.append({
                'priority': 'HIGH',
                'recommendation': 'Enable server-side encryption with customer-managed keys for restricted data',
                'rationale': f"{classification_summary['RESTRICTED']} objects contain restricted data requiring enhanced encryption"
            })
            
            recommendations.append({
                'priority': 'HIGH',
                'recommendation': 'Implement access logging and monitoring for restricted data access',
                'rationale': 'Restricted data requires comprehensive audit trails'
            })
        
        if classification_summary['CONFIDENTIAL'] > 0:
            recommendations.append({
                'priority': 'MEDIUM',
                'recommendation': 'Enable server-side encryption for confidential data',
                'rationale': f"{classification_summary['CONFIDENTIAL']} objects contain confidential data"
            })
        
        if classification_summary['PUBLIC'] > 0:
            recommendations.append({
                'priority': 'LOW',
                'recommendation': 'Review public data classification to ensure accuracy',
                'rationale': f"{classification_summary['PUBLIC']} objects classified as public - verify this is correct"
            })
        
        return recommendations

# Example usage
def main():
    """Example usage of the DataClassificationManager"""
    
    # Initialize the classification manager
    classifier = DataClassificationManager()
    
    # Set up Macie
    if classifier.setup_macie_classification():
        print("Macie setup completed successfully")
        
        # Classify a bucket
        bucket_name = 'my-data-bucket'
        job_id = classifier.classify_s3_bucket(bucket_name)
        
        if job_id:
            print(f"Classification job started: {job_id}")
            
            # Note: In practice, you would wait for the job to complete
            # and then generate the report
            # report = classifier.generate_classification_report(bucket_name, job_id)
            # print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()

### Example 3: Data classification policy template

```markdown
# Data Classification Policy

## 1. Purpose and Scope

This policy establishes the framework for classifying data based on its sensitivity, 
value, and criticality to the organization. It applies to all employees, contractors, 
and third parties who handle organizational data.

## 2. Data Classification Levels

### 2.1 Public Data
**Definition**: Information that can be freely shared with the public without harm to the organization.

**Criteria**:
- No competitive disadvantage if disclosed
- Already publicly available or intended for public release
- No regulatory restrictions on disclosure

**Examples**:
- Marketing materials and brochures
- Public website content
- Press releases
- Published research papers

**Handling Requirements**:
- Access Control: None required
- Encryption: Not required
- Storage: Standard business practices
- Transmission: No special requirements
- Disposal: Standard disposal methods

### 2.2 Internal Data
**Definition**: Information intended for use within the organization that could cause 
minor harm if disclosed externally.

**Criteria**:
- Limited competitive impact if disclosed
- Intended for internal business operations
- No regulatory restrictions

**Examples**:
- Internal policies and procedures
- Employee directories (non-sensitive)
- General business correspondence
- Training materials

**Handling Requirements**:
- Access Control: Organization members only
- Encryption: Recommended for external transmission
- Storage: Secure internal systems
- Transmission: Encrypted when sent externally
- Disposal: Secure disposal methods

### 2.3 Confidential Data
**Definition**: Sensitive information that could cause significant harm to the 
organization if disclosed to unauthorized parties.

**Criteria**:
- Significant competitive disadvantage if disclosed
- Contains personal information
- Proprietary business information

**Examples**:
- Financial reports and budgets
- Customer information and lists
- Employee personal information
- Vendor contracts
- Strategic business plans

**Handling Requirements**:
- Access Control: Need-to-know basis with manager approval
- Encryption: Required for storage and transmission
- Storage: Encrypted systems with access controls
- Transmission: Encrypted channels only
- Disposal: Certified secure destruction

### 2.4 Restricted Data
**Definition**: Highly sensitive information that could cause severe harm if disclosed 
and is subject to regulatory requirements.

**Criteria**:
- Severe harm if disclosed
- Subject to regulatory compliance requirements
- Legal or contractual obligations for protection

**Examples**:
- Social Security Numbers
- Payment card information
- Health records
- Trade secrets
- Legal privileged communications

**Handling Requirements**:
- Access Control: Explicit authorization required
- Encryption: Strong encryption mandatory
- Storage: Highly secure systems with audit logging
- Transmission: Encrypted with additional controls
- Disposal: Certified destruction with audit trail

## 3. Classification Procedures

### 3.1 Initial Classification
1. Data owner reviews data content and context
2. Applies classification criteria and decision tree
3. Documents classification rationale
4. Obtains required approvals
5. Applies classification labels and controls

### 3.2 Classification Review
- Annual review of all classified data
- Event-driven review for significant changes
- Quality assurance sampling and validation
- Update classification as needed

### 3.3 Reclassification
- Triggered by changes in sensitivity, regulations, or business context
- Requires approval from data governance committee
- Documentation of rationale for change
- Update of all related systems and controls

## 4. Roles and Responsibilities

### 4.1 Data Owner
- Assign initial data classification
- Approve access requests
- Review classification periodically
- Ensure compliance with handling requirements

### 4.2 Data Steward
- Implement classification decisions
- Monitor data usage and access
- Report classification issues
- Maintain classification documentation

### 4.3 Data Custodian
- Apply technical controls based on classification
- Implement data handling procedures
- Maintain audit logs and monitoring
- Execute secure disposal procedures

### 4.4 All Employees
- Follow data handling requirements
- Report suspected classification errors
- Complete required training
- Comply with access controls

## 5. Compliance and Enforcement

### 5.1 Monitoring
- Regular audits of classification compliance
- Automated monitoring where possible
- Incident reporting and investigation
- Metrics and reporting to management

### 5.2 Violations
- Immediate investigation of violations
- Corrective actions and remediation
- Disciplinary actions as appropriate
- Process improvements to prevent recurrence

## 6. Training and Awareness

### 6.1 Required Training
- Annual data classification training for all employees
- Role-specific training for data handlers
- New employee orientation on data classification
- Regular updates on policy changes

### 6.2 Awareness Programs
- Regular communications about data classification
- Examples and case studies
- Recognition of good practices
- Incident lessons learned

## 7. Policy Review and Updates

This policy will be reviewed annually and updated as needed to reflect:
- Changes in business requirements
- New regulatory requirements
- Technology changes
- Lessons learned from incidents

## 8. Related Documents

- Data Governance Policy
- Information Security Policy
- Privacy Policy
- Incident Response Procedures
- Data Retention Policy

---
**Policy Owner**: Chief Data Officer
**Approved By**: Executive Committee
**Effective Date**: January 1, 2024
**Next Review**: January 1, 2025
```

### Example 4: Classification decision tree and workflow

```python
class DataClassificationDecisionTree:
    """Decision tree for automated data classification"""
    
    def __init__(self):
        self.classification_rules = {
            'regulatory_data': {
                'pii': 'CONFIDENTIAL',
                'phi': 'RESTRICTED',
                'pci': 'RESTRICTED',
                'financial': 'CONFIDENTIAL'
            },
            'business_impact': {
                'high': 'RESTRICTED',
                'medium': 'CONFIDENTIAL',
                'low': 'INTERNAL',
                'none': 'PUBLIC'
            },
            'sensitivity_indicators': {
                'ssn': 'RESTRICTED',
                'credit_card': 'RESTRICTED',
                'medical': 'RESTRICTED',
                'financial_account': 'CONFIDENTIAL',
                'employee_id': 'CONFIDENTIAL',
                'customer_info': 'CONFIDENTIAL'
            }
        }
    
    def classify_data(self, data_attributes):
        """
        Classify data based on attributes and decision tree logic
        
        Args:
            data_attributes (dict): Dictionary containing data attributes
                - content_type: Type of content
                - contains_pii: Boolean indicating PII presence
                - regulatory_scope: List of applicable regulations
                - business_impact: Impact level if disclosed
                - sensitivity_indicators: List of sensitive data types found
        
        Returns:
            dict: Classification result with level and rationale
        """
        
        classification_scores = {
            'PUBLIC': 0,
            'INTERNAL': 1,
            'CONFIDENTIAL': 2,
            'RESTRICTED': 3
        }
        
        max_score = 0
        classification_rationale = []
        
        # Check regulatory requirements
        if data_attributes.get('regulatory_scope'):
            for regulation in data_attributes['regulatory_scope']:
                if regulation.lower() in ['gdpr', 'hipaa', 'pci-dss']:
                    max_score = max(max_score, classification_scores['RESTRICTED'])
                    classification_rationale.append(f"Subject to {regulation} regulation")
                elif regulation.lower() in ['sox', 'ferpa']:
                    max_score = max(max_score, classification_scores['CONFIDENTIAL'])
                    classification_rationale.append(f"Subject to {regulation} regulation")
        
        # Check for PII
        if data_attributes.get('contains_pii'):
            max_score = max(max_score, classification_scores['CONFIDENTIAL'])
            classification_rationale.append("Contains personally identifiable information")
        
        # Check sensitivity indicators
        if data_attributes.get('sensitivity_indicators'):
            for indicator in data_attributes['sensitivity_indicators']:
                if indicator in self.classification_rules['sensitivity_indicators']:
                    required_level = self.classification_rules['sensitivity_indicators'][indicator]
                    max_score = max(max_score, classification_scores[required_level])
                    classification_rationale.append(f"Contains {indicator}")
        
        # Check business impact
        business_impact = data_attributes.get('business_impact', 'low')
        if business_impact in self.classification_rules['business_impact']:
            required_level = self.classification_rules['business_impact'][business_impact]
            max_score = max(max_score, classification_scores[required_level])
            classification_rationale.append(f"Business impact level: {business_impact}")
        
        # Determine final classification
        final_classification = 'PUBLIC'
        for level, score in classification_scores.items():
            if score == max_score:
                final_classification = level
                break
        
        return {
            'classification': final_classification,
            'confidence_score': max_score,
            'rationale': classification_rationale,
            'recommended_controls': self.get_recommended_controls(final_classification)
        }
    
    def get_recommended_controls(self, classification):
        """Get recommended security controls for classification level"""
        
        controls = {
            'PUBLIC': {
                'access_control': 'None required',
                'encryption': 'Not required',
                'monitoring': 'Standard logging',
                'retention': 'Business requirements'
            },
            'INTERNAL': {
                'access_control': 'Organization members only',
                'encryption': 'Recommended for transmission',
                'monitoring': 'Access logging',
                'retention': 'Standard retention policy'
            },
            'CONFIDENTIAL': {
                'access_control': 'Need-to-know with approval',
                'encryption': 'Required for storage and transmission',
                'monitoring': 'Comprehensive access logging',
                'retention': 'Minimum required retention'
            },
            'RESTRICTED': {
                'access_control': 'Explicit authorization required',
                'encryption': 'Strong encryption mandatory',
                'monitoring': 'Full audit logging and monitoring',
                'retention': 'Strict retention limits with audit trail'
            }
        }
        
        return controls.get(classification, controls['INTERNAL'])

# Example usage and workflow
def classification_workflow_example():
    """Example of classification workflow"""
    
    classifier = DataClassificationDecisionTree()
    
    # Example data attributes for different scenarios
    test_cases = [
        {
            'name': 'Customer Database',
            'attributes': {
                'content_type': 'database',
                'contains_pii': True,
                'regulatory_scope': ['GDPR'],
                'business_impact': 'high',
                'sensitivity_indicators': ['customer_info', 'financial_account']
            }
        },
        {
            'name': 'Marketing Brochure',
            'attributes': {
                'content_type': 'document',
                'contains_pii': False,
                'regulatory_scope': [],
                'business_impact': 'none',
                'sensitivity_indicators': []
            }
        },
        {
            'name': 'Employee Records',
            'attributes': {
                'content_type': 'database',
                'contains_pii': True,
                'regulatory_scope': [],
                'business_impact': 'medium',
                'sensitivity_indicators': ['ssn', 'employee_id']
            }
        }
    ]
    
    print("Data Classification Results:")
    print("=" * 50)
    
    for test_case in test_cases:
        result = classifier.classify_data(test_case['attributes'])
        
        print(f"\nData: {test_case['name']}")
        print(f"Classification: {result['classification']}")
        print(f"Confidence Score: {result['confidence_score']}")
        print(f"Rationale: {'; '.join(result['rationale'])}")
        print("Recommended Controls:")
        for control_type, control_desc in result['recommended_controls'].items():
            print(f"  - {control_type.replace('_', ' ').title()}: {control_desc}")

if __name__ == "__main__":
    classification_workflow_example()
```

## AWS services to consider

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon Macie</h4>
    <p>Uses machine learning and pattern matching to discover and protect your sensitive data in AWS. Automatically identifies personally identifiable information (PII) and provides detailed classification findings.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Resource Groups</h4>
    <p>Helps you organize your AWS resources using tags. Enables grouping and management of resources based on data classification and other criteria.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>Amazon S3</h4>
    <p>Object storage service with built-in tagging capabilities. Supports object-level and bucket-level tags for data classification and automated policy enforcement.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Config</h4>
    <p>Enables you to assess, audit, and evaluate the configurations of your AWS resources. Helps track data storage configurations and ensure compliance with classification policies.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS CloudTrail</h4>
    <p>Records API calls for your account and delivers log files to you. Provides audit trails for data access and classification activities across your AWS environment.</p>
  </div>
</div>

<div class="aws-service">
  <div class="aws-service-content">
    <h4>AWS Systems Manager</h4>
    <p>Gives you visibility and control of your infrastructure on AWS. Provides automation capabilities for applying classification-based policies and controls.</p>
  </div>
</div>

## Benefits of understanding your data classification scheme

- **Appropriate protection**: Enables application of security controls proportionate to data sensitivity and business value
- **Regulatory compliance**: Helps meet legal and regulatory requirements for data protection and privacy
- **Risk management**: Provides foundation for data-related risk assessment and mitigation strategies
- **Resource optimization**: Allows efficient allocation of security resources based on data criticality
- **Incident response**: Enables prioritized response to data security incidents based on classification levels
- **Data governance**: Supports effective data governance and stewardship programs
- **Cost optimization**: Helps optimize storage and protection costs based on data value and requirements

## Related resources

<div class="related-resources">
  <h2>Related Resources</h2>
  <ul>
    <li><a href="https://docs.aws.amazon.com/wellarchitected/latest/framework/sec_data_classification_identify_data.html">AWS Well-Architected Framework - Understand your data classification scheme</a></li>
    <li><a href="https://docs.aws.amazon.com/macie/latest/user/what-is-macie.html">Amazon Macie User Guide</a></li>
    <li><a href="https://docs.aws.amazon.com/config/latest/developerguide/WhatIsConfig.html">AWS Config Developer Guide</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-use-amazon-macie-to-preview-sensitive-data-in-s3-buckets/">How to use Amazon Macie to preview sensitive data in S3 buckets</a></li>
    <li><a href="https://aws.amazon.com/blogs/security/how-to-implement-data-classification-and-protection-using-aws-services/">How to implement data classification and protection using AWS services</a></li>
    <li><a href="https://www.nist.gov/privacy-framework">NIST Privacy Framework</a></li>
  </ul>
</div>
```
