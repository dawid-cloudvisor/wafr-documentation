# Recommendations/best practices regarding AWS root user

Using the AWS root user is generally discouraged due to security and management concerns. The root user has unrestricted access to all AWS resources and services, making it a prime target for malicious activities. Instead, best practices recommend creating and using IAM (Identity and Access Management) users with appropriate permissions. However, if you must use the root user for certain tasks, here are some best practices:

## Limited Usage:

Reserve the root user for only critical tasks that cannot be performed by IAM users. Regular operational tasks should be carried out using IAM users with the least privilege necessary.

## MFA (Multi-Factor Authentication):

Enable MFA for the root user to add an extra layer of security. This ensures that even if the password is compromised, an additional authentication step is required.

## Strong Password:

Use a strong and unique password for the root user account. Avoid using easily guessable or commonly used passwords.

## Enable CloudTrail Logging:

AWS CloudTrail should be enabled to track and log all activities performed using the root user. This provides an audit trail for security and compliance purposes.

## Enable GuardDuty:

AWS GuardDuty is a threat detection service that monitors for malicious activity in your AWS environment. Enabling GuardDuty helps detect potential unauthorized access attempts.

## Regular Monitoring:

Keep a close eye on the root user's activities. Regularly review the CloudTrail logs and other monitoring tools to identify any suspicious behavior.

## Rotate Access Keys:

If you use the root user's access keys, rotate them regularly. It's better to avoid using access keys for the root user and rely on IAM users instead.

## Use IAM for Daily Tasks:

Whenever possible, use IAM users with the least privilege necessary for everyday tasks. This principle follows the "principle of least privilege," ensuring users only have access to the resources they need.

## Segregation of Duties:

Divide responsibilities among multiple users or roles. This prevents a single user from having unrestricted access and reduces the risk of insider threats.

## Root User Deactivation:

AWS now recommends deactivating the root user's access keys and even the ability to sign in using the root user account, relying solely on IAM users for access.

## Regular Security Assessments:

Perform regular security assessments and audits to identify potential vulnerabilities and areas for improvement.


Remember, the ultimate goal is to minimize the use of the root user account due to its elevated privileges and potential security risks. Utilize IAM users and follow the principle of least privilege to maintain a secure and well-managed AWS environment.


## Further readings:

[Best practices to protect your account's root user](https://docs.aws.amazon.com/SetUp/latest/UserGuide/best-practices-root-user.html)
