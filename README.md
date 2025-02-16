# Deployment of MozioApp with CloudFormation Template

### Overview
This CloudFormation template automates the deployment of a containerized application on AWS ECS Fargate. It provisions necessary resources, including a VPC, subnets, security groups, an Application Load Balancer (ALB), ECS cluster, and CloudWatch logging.

### Pre-requisites
Before deploying the CloudFormation stack, ensure you have the following:
* An AWS account with necessary permissions to create resources (VPC, ECS, IAM, ALB, etc.).
* AWS CLI installed and configured.
* A Docker container image stored in Amazon ECR or another accessible registry.

### Installing AWS CLI
Refer to [AWS CLI installation guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html).
For Linux environment:

```
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
sudo apt install unzip
unzip awscliv2.zip
sudo ./aws/install
```

Then run `aws configure` for authentication. Enter your `Access key`, `Secret access key` and `region` when prompted. `Access key` and `Secret access key` can be generated via AWS IAM. 

### Containerizing the Application
Source code of the application and `Dockerfile` are available in `app` folder. Run `docker build . -t hello-mozio` to create container image.

To push the image to AWS ECR;
* Create a new repo (if not exist):
```
aws ecr create-repository --repository-name mozio
```
* Login to ECR for image push: (Replace ECR URI with the appropriate value)
```
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 794038229667.dkr.ecr.us-east-1.amazonaws.com
```
* Tag the builded image: 
```
docker tag hello-mozio:latest 794038229667.dkr.ecr.us-east-1.amazonaws.com/mozio:latest
```
* Push image to ECR:
```
docker push 794038229667.dkr.ecr.us-east-1.amazonaws.com/mozio
```

Image will now be available in AWS ECR repository.


### Deployment Instructions
#### Step 1: Validate the CloudFormation Template
Before deploying, validate the template to ensure it has no syntax errors:
```
aws cloudformation validate-template --template-body file://deploy_mozio_app.yaml`
```

#### Step 2: Deploy the CloudFormation Stack
Use the AWS CLI to deploy the stack. Replace `ContainerImage` with the appropriate container image URL.

```
aws cloudformation create-stack --stack-name MozioFargate \
  --template-body file://deploy_mozio_app.yaml \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameters \
    ParameterKey=ContainerImage,ParameterValue=794038229667.dkr.ecr.us-east-1.amazonaws.com/mozio:latest

```
Note that it is possible to add more parameters if needed. Below is the list of all parameters that can be used during stack creation:

```
PublicSubnet1Cidr
PublicSubnet2Cidr
PrivateSubnet1Cidr
PrivateSubnet2Cidr
ContainerImage
DesiredCount
MinCapacity
MaxCapacity
```
Here is an example of creating stack with a more parameters:
```
aws cloudformation create-stack --stack-name MozioFargate \
  --template-body file://deploy_mozio_app.yaml \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameters \
    ParameterKey=VpcCIDR,ParameterValue=10.0.0.0/16 \
    ParameterKey=PublicSubnet1CIDR,ParameterValue=10.0.1.0/24 \
    ParameterKey=PublicSubnet2CIDR,ParameterValue=10.0.2.0/24 \
    ParameterKey=PrivateSubnet1CIDR,ParameterValue=10.0.3.0/24 \
    ParameterKey=PrivateSubnet2CIDR,ParameterValue=10.0.4.0/24 \
    ParameterKey=ContainerImage,ParameterValue=794038229667.dkr.ecr.us-east-1.amazonaws.com/mozio:v2 \
    ParameterKey=DesiredCount,ParameterValue=4

```
Each parameter has a default value if no parameter is given. Check `deploy_mozio_app.yaml` file for default values.

#### Step 3: Deploy the CloudFormation Stack
Monitor the stack creation process:
```
aws cloudformation describe-stacks --stack-name MozioFargate
```

Verify the parameters and check `StackStatus` field for the status

Alternatively, check the AWS CloudFormation console for status updates.

#### Step 4: Access the Deployed Application
Once the stack is successfully deployed, retrieve the ALB's DNS name to access the application:
```
aws cloudformation describe-stacks --stack-name MozioFargate --query "Stacks[0].Outputs"
```

Use the DNS name in a browser to verify the application is running.

### Updating Stack Info
To update the stack; e.g. releasing new version of software, use `update-stack` command:

```
aws cloudformation update-stack --stack-name MozioFargate \
  --template-body file://deploy_mozio_app.yaml \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameters \
    ParameterKey=ContainerImage,ParameterValue=794038229667.dkr.ecr.us-east-1.amazonaws.com/mozio:v2

```
This will update the container image to `mozio:v2` in ECS and new release (v2) will be deployed.




### Uninstall
To uninstall the application and delete the deployed resources, run:
```
aws cloudformation delete-stack --stack-name MozioFargate
```
