# Enable multi factor authentications for AWS users

## What is Multi-Factor Authentication (MFA)?

Multi-factor Authentication (MFA) is an authentication method that requires the user to provide two or more verification factors to gain access to a resource such as an application, online account, or a VPN. MFA is a core component of a strong identity and access management (IAM) policy. Rather than just asking for a username and password, MFA requires one or more additional verification factors, which decreases the likelihood of a successful cyber attack.

## How Does MFA work?

MFA works by requiring additional verification information (factors). One of the most common MFA factors that users encounter are one-time passwords (OTP). OTPs are those 4-8 digit codes that you often receive via email, SMS or some sort of mobile app. With OTPs a new code is generated periodically or each time an authentication request is submitted. The code is generated based upon a seed value that is assigned to the user when they first register and some other factor which could simply be a counter that is incremented or a time value.


## How to enable multi factor authentication in AWS

[please follow this video guide](https://www.youtube.com/watch?v=e6A7z7FqQDE&t=28s)


## Further readings:
[wikipedia](https://en.wikipedia.org/wiki/Multi-factor_authentication)

[Using multi-factor authentication (MFA) in AWS](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_mfa.html)
