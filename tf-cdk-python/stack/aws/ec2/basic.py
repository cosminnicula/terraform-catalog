from constructs import Construct
from cdktf import TerraformStack, S3Backend, TerraformOutput

from imports.aws.provider import AwsProvider
from imports.aws.data_aws_caller_identity import DataAwsCallerIdentity
from imports.ec2_instance import Ec2Instance

region = "eu-central-1"
profile= "default"

# equivalent to TF variables
environmentName = "dev"
ec2InstanceType = "t2.micro"
ec2Ami = "ami-0a261c0e5f51090b1"


class BasicEc2Stack(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        # equivalent to TF provider
        AwsProvider(self, 'Aws', region=region)

        # equivalent to S3 remote backend
        S3Backend(
            self,
            bucket="tf-cdk-python",
            key="basic-ec2-stack/terraform.tfstate",
            encrypt=False,
            region=region,
            dynamodb_table="tf-cdk-python",
            profile=profile,
        )

        # equivalent to TF local values
        ec2Id = f'{environmentName}-ec2-id'

        # equivalent to TF resources
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
