from constructs import Construct
from cdktf import TerraformStack, S3Backend, TerraformOutput, TerraformAsset, AssetType

from imports.aws.provider import AwsProvider
from imports.aws.data_aws_caller_identity import DataAwsCallerIdentity
from imports.ec2_instance import Ec2Instance
from imports.s3_bucket import S3Bucket
from imports.dynamodb_table import DynamodbTable
from imports.aws.data_aws_ami import DataAwsAmi
from imports.random.provider import RandomProvider
from imports.random.string_resource import StringResource

import os

region = "eu-central-1"  # the AWS region
# the AWS CLI profile to use; if not explicitly specified, "default" is used
profile = "default"

# equivalent to TF variables
environmentName = "dev"
ec2InstanceType = "t2.micro"
ec2Ami = "ami-0a261c0e5f51090b1"


class BasicEc2Stack(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        # equivalent to TF provider
        AwsProvider(
            self,
            "aws",
            region=region
        )

        RandomProvider(
            self,
            "random"
        )

        # equivalent to S3 remote backend
        # S3Backend(
        #     self,
        #     bucket="tf-cdk-python",
        #     key="basic-ec2-stack/terraform.tfstate",
        #     encrypt=False,
        #     region=region,
        #     dynamodb_table="tf-cdk-python",
        #     profile=profile,
        # )

        # equivalent to TF local values
        ec2Id = f'{environmentName}-ec2-id'

        # equivalent to TF resources / modules
        # the following S3 bucket and DynamoDB table needs to be provisioned before activating the S3 backend
        # next, run terraform init --migrate-state inside cdktf.out/stacks/basic-ec2-stack
        # S3Bucket(
        #     self,
        #     "tf-cdk-python-s3-bucket",
        #     bucket="tf-cdk-python",
        # )
        # DynamodbTable(
        #     self,
        #     "tf-cdk-python-dynamodb-lock-table",
        #     name="tf-cdk-python",
        #     billing_mode="PAY_PER_REQUEST",
        #     attributes=[{
        #         "name": "LockID",
        #         "type": "S"
        #     }],
        #     hash_key="LockID",
        # )

        # equivalent to TF data sources (gets latest AMI ID for Amazon Linux2 OS)
        ami = DataAwsAmi(
            self,
            "data-aws-ami",
            most_recent=True,
            owners=["amazon"],
            filter=[
                {
                    "name": "name",
                    "values": ["amzn2-ami-hvm-*"]
                }, {
                    "name": "root-device-type",
                    "values": ["ebs"]
                }, {
                    "name": "virtualization-type",
                    "values": ["hvm"]
                }, {
                    "name": "architecture",
                    "values": ["x86_64"]
                }
            ]
        )

        setupApacheScript = TerraformAsset(
            self,
            "setup-apache-script",
            path=os.path.join(os.path.dirname(__file__), 'setup_apache.sh'),
            type=AssetType.FILE
        )

        # equivalent to TF EC2 module
        ec2Instance = Ec2Instance(
            self,
            ec2Id,
            instance_type=ec2InstanceType,
            ami=ec2Ami,
            key_name="cn-ec2-1",
            monitoring=True,
            vpc_security_group_ids=["sg-020054ce43d5db33c"],
            subnet_id="subnet-2af24542",
            user_data=setupApacheScript.path,
            tags={
                "env": environmentName
            }
        )

        # # equivalent to TF EC2 module's instance_count meta-argument
        # see also TerraformHclModule (https://developer.hashicorp.com/terraform/cdktf/concepts/modules)
        # for i in range(2):
        #     # equivalent to TF modules
        #     ec2Instance = Ec2Instance(
        #         self,
        #         f'{ec2Id}-{i}',
        #         instance_type=ec2InstanceType,
        #         ami=ec2Ami,
        #         tags={
        #             "env": environmentName
        #         }
        #     )

        randomString = StringResource(
            self,
            "random-string",
            length=8
        )

        # equivalent to TF output values
        TerraformOutput(
            self,
            "ami",
            value=ami.id
        )

        TerraformOutput(
            self,
            "ec2_public_ip",
            value=ec2Instance.public_ip_output
        )

        TerraformOutput(
            self,
            "some_random_string",
            value=randomString
        )
