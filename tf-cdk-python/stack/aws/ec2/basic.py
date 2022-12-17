from constructs import Construct
from cdktf import TerraformStack, S3Backend, TerraformOutput

from imports.aws.provider import AwsProvider
from imports.aws.data_aws_caller_identity import DataAwsCallerIdentity
from imports.ec2_instance import Ec2Instance
from imports.s3_bucket import S3Bucket
from imports.dynamodb_table import DynamodbTable

region = "eu-central-1"  # the AWS region
profile = "default"  # the AWS CLI profile to use

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
            'Aws',
            region=region
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

        # equivalent to TF resources
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

        ec2Instance = Ec2Instance(
            self,
            ec2Id,
            instance_type=ec2InstanceType,
            ami=ec2Ami,
            tags={
                "env": environmentName
            }
        )

        # equivalent to TF output values
        TerraformOutput(
            self,
            'ec2_public_ip',
            value=ec2Instance.public_ip_output
        )
