# How to use secrets manager secrets with Beanstalk

- [How to use secrets manager secrets with Beanstalk](#how-to-use-secrets-manager-secrets-with-beanstalk)
  - [Create the secret](#create-the-secret)
  - [Create the IAM policy and attach it to the instance profile](#create-the-iam-policy-and-attach-it-to-the-instance-profile)
  - [Create secrests manager endpoint in subnets that used by the beanstalk deployment](#create-secrests-manager-endpoint-in-subnets-that-used-by-the-beanstalk-deployment)
  - [Integrate '.ebextensions' and 'container\_commands' in your custom logic](#integrate-ebextensions-and-container_commands-in-your-custom-logic)
  - [Example implementation](#example-implementation)

Unfortunately there is not an easy way currently. You need to implement your own logic to retrieve secrets manager secrets.


## Create the secret

Go to Secrets Manager AWS console in the region where your infra can be found
To store your secret create a custom secret in AWS-Secret-Manager. In secret manager you can create a new secret by clicking "Store a new secret", then selecting "Other type of secret" and entering your secret key/value:
![ssm](ssm.png)
At the next step you need to provide a Secret Name (say "your_secret_name") and you can leave everything else to their default settings.


## Create the IAM policy and attach it to the instance profile

1. Create a new (Customer Managed) IAM policy on the IAM AWS console with the content similar as below:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "Getsecretvalue",
      "Effect": "Allow",
      "Action": [
          "secretsmanager:GetResourcePolicy",
          "secretsmanager:GetSecretValue",
          "secretsmanager:DescribeSecret",
          "secretsmanager:ListSecretVersionIds"
      ],
      "Resource": "your-secret-arn"
    }
  ]
}
```

![policy](policy.png)

Change the "Resource" value with the arn of the secret you have created earlier.

2. Attach the policy to the EC2 instance profile

Choose 'Roles' on the left side navigation panel on IAM console, and choose the profile  you want the plocy to attach to. In 'Permissions' section (Permission Policies) click on 'Add permissions' and choose attach policies. Then chose the policy that you have just created and attach it to the Role.


## Create secrests manager endpoint in subnets that used by the beanstalk deployment

Go to VPC AWS console, and chose 'Endpoints' from left side menu. Follow [this guide](https://docs.aws.amazon.com/vpc/latest/privatelink/create-interface-endpoint.html).

![endpoint](endpoint.png)


## Integrate '.ebextensions' and 'container_commands' in your custom logic

In your application source on root level path create a folder called `.ebextensions`
here you can implement your custom logic that retrieves the secret value for you.

Read [this guide about 'container_commands'](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/customize-containers-ec2.html#linux-container-commands:~:text=true%0A%20%20%20%20%20%20ensureRunning%3A%20true-,Container%20commands,-You%20can%20use) and [this one about .ebextensions](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/environment-configuration-methods-before.html#:~:text=Use%20.ebextensions%20to%20configure%20options%20that%20are%20required%20to%20make%20your%20application%20work)


## Example implementation

```sh
# .ebextensions/setup-env.config
container_commands:
  01-extract-env:
    env:
      AWS_SECRET_ID:
        "Fn::GetOptionSetting":
          Namespace: "aws:elasticbeanstalk:application:environment"
          OptionName: AWS_SECRET_ID
      AWS_REGION: {"Ref" : "AWS::Region"}
      ENVFILE: .env

    command: >
        aws secretsmanager get-secret-value --secret-id $AWS_SECRET_ID --region $AWS_REGION |
        jq -r '.SecretString' |
        jq -r 'to_entries|map("\(.key)=\(.value|tostring)")|.[]' > $ENVFILE
```

Your application then needs to catch up the `.env` file