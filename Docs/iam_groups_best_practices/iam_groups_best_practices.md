# Working with IAM Groups

## Table of contents

- [Working with IAM Groups](#working-with-iam-groups)
	- [Table of contents](#table-of-contents)
	- [IAM Groups best practices](#iam-groups-best-practices)
		- [Use Groups for Permissions Management:](#use-groups-for-permissions-management)
		- [Follow the Principle of Least Privilege (PoLP):](#follow-the-principle-of-least-privilege-polp)
		- [Avoid Hard-Coding IAM Group Names:](#avoid-hard-coding-iam-group-names)
		- [Naming Conventions:](#naming-conventions)
		- [Avoid Using Root User and Access Keys:](#avoid-using-root-user-and-access-keys)
		- [Regularly Review and Rotate Permissions:](#regularly-review-and-rotate-permissions)
		- [Implement MFA:](#implement-mfa)
		- [Use **Managed Policies:**](#use-managed-policies)
		- [Use Policy Conditions:](#use-policy-conditions)
		- [Regularly Audit and Monitor:](#regularly-audit-and-monitor)
		- [Separation of Duties:](#separation-of-duties)
		- [Document and Communicate:](#document-and-communicate)
		- [Testing:](#testing)
		- [Automate:](#automate)
	- [Choosing IAM Groups](#choosing-iam-groups)
		- [Administrators:](#administrators)
		- [Developers:](#developers)
		- [Operations:](#operations)
		- [Billing:](#billing)
		- [SecurityAuditors:](#securityauditors)
		- [Support:](#support)
		- [DataScientists:](#datascientists)
		- [Marketing:](#marketing)
		- [Sales:](#sales)
		- [Training:](#training)
		- [BackupOperators:](#backupoperators)
		- [ReadOnlyUsers:](#readonlyusers)


## IAM Groups best practices

### Use Groups for Permissions Management:

Instead of assigning permissions directly to users, use IAM groups to define sets of permissions. This simplifies access management and allows for easier updates across multiple users.

### Follow the Principle of Least Privilege (PoLP):

Assign the minimum permissions required for each group to perform its tasks. Avoid giving excessive permissions, as this reduces the potential impact of a security breach.

### Avoid Hard-Coding IAM Group Names:

Instead of referring to IAM groups by name in your applications or scripts, use IAM policies and roles with dynamic variables to ensure better maintainability and flexibility.

### Naming Conventions:

Use clear and descriptive names for your IAM groups. This makes it easier to understand the purpose of each group and improves overall organization.

### Avoid Using Root User and Access Keys:

Never assign permissions directly to the root user. Instead, create IAM users or groups with the necessary permissions. Also, avoid using access keys whenever possible, as IAM roles and instance profiles are more secure for programmatic access.

### Regularly Review and Rotate Permissions:

Periodically review the permissions assigned to IAM groups. Remove unnecessary permissions and rotate credentials to minimize the risk of unauthorized access.

### Implement MFA:

Require multi-factor authentication (MFA) for users belonging to high-privilege groups. This adds an extra layer of security to prevent unauthorized access.

### Use **Managed Policies:**

AWS provides managed policies that are predefined and regularly updated by AWS. These policies follow best practices and can help you avoid common pitfalls in permissions management.

### Use Policy Conditions:

Implement policy conditions to add extra layers of security. For instance, you can restrict access to certain resources based on IP addresses or time of day.

### Regularly Audit and Monitor:

Set up AWS CloudTrail and Amazon CloudWatch to monitor and log actions taken by IAM users and groups. This helps in identifying unusual or potentially malicious activities.

### Separation of Duties:

Avoid granting conflicting permissions to the same group. For example, a group should not have both administrative privileges and restricted application-specific privileges.

### Document and Communicate:

Clearly document the purpose of each IAM group, along with the associated permissions. Communicate these to your team to ensure everyone understands their access levels.

### Testing:

Before deploying changes to IAM groups or policies in a production environment, thoroughly test them in a staging environment to avoid unintended consequences.

### Automate:

Use AWS CloudFormation or Infrastructure as Code (IaC) tools to automate the provisioning of IAM groups and permissions. This ensures consistency and repeatability.


IAM is a critical component of securing your AWS environment. Following these best practices helps you maintain a secure and well-organized access management strategy.

## Choosing IAM Groups

When choosing IAM group names for a small organization, it's important to opt for names that are descriptive, easy to understand, and follow a consistent naming convention. Below you can find examples for different groups and the kind of AWS Policies that one may associate to the group.


### Administrators:

**Group Description:** Users with full administrative privileges.

**Managed Policy:** `AdministratorAccess`

**Description:** Provides full administrative access to AWS resources.


### Developers:

**Group Description:** Users responsible for development, deployment, and APIs.

**Managed Policies:** `AWSCodeDeployFullAccess`, `AmazonS3FullAccess`, `AWSLambda_FullAccess`

**Description:** Provides access to resources needed for application deployment, storage, and serverless functions.


### Operations:

**Group Description:** Users managing operational aspects and monitoring.

**Managed Policies:** `AmazonEC2FullAccess`, `CloudWatchFullAccess`, `AWSAutoScalingFullAccess`

**Description:** Grants access to manage and monitor EC2 instances, Auto Scaling, and CloudWatch metrics.


### Billing:

**Group Description:** Users responsible for viewing and managing billing.

**Managed Policy:** `Billing`

**Description:** Provides access to view and manage billing information without granting broader permissions.


### SecurityAuditors:

**Group Description:** Users conducting security audits and reviews.

**Managed Policies:** `AWSSecurityAudit`, `AmazonInspectorFullAccess`

**Description:** Enables security auditors to assess and review security configurations and vulnerabilities.


### Support:

**Group Description:** Users providing support and troubleshooting.

**Managed Policy:** `AWSSupportAccess`

**Description:** Provides basic access needed for AWS Support to troubleshoot issues.


### DataScientists:

**Group Description:** Users working with data-related services.

**Managed Policies:** `AmazonS3ReadOnlyAccess`, `AmazonRedshiftReadOnlyAccess`, `AWSGlueConsoleFullAccess`

**Description:** Enables access to read data from S3, Amazon Redshift, and manage Glue resources.


### Marketing:

**Group Description:** Users responsible for marketing activities.

**Custom Policy:** Define a custom policy granting access to specific marketing-related resources, such as analytics services.


### Sales:

**Group Description:** Users in the sales team.

**Custom Policy:** Define a custom policy granting access to specific CRM and sales-related tools.


### Training:

**Group Description:** Users providing training and onboarding.

**Custom Policy:** Define a custom policy granting access to training materials and resources.


### BackupOperators:

**Group Description:** Users responsible for backup and disaster recovery.

**Managed Policies:** `AmazonRDSBackUpRole`

**Description:** Enables backup-related operations on EC2 instances and RDS databases.


### ReadOnlyUsers:

**Group Description:** Users requiring read-only access to resources.

**Managed Policy:** ReadOnlyAccess

**Description:** Provides read-only access to AWS resources.
