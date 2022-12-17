from constructs import Construct
from cdktf import TerraformStack, TerraformOutput

from imports.aws.provider import AwsProvider
from imports.aws.data_aws_caller_identity import DataAwsCallerIdentity
from imports.ec2_instance import Ec2Instance


class BasicEc2Stack(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        AwsProvider(self, 'Aws', region='eu-central-1')

        Ec2Instance(
            self,
            "ec2-demo",
            instance_type="t2.micro",
            ami="ami-0a261c0e5f51090b1"
        )

        TerraformOutput(
            self, 'create_user_arn',
            value=DataAwsCallerIdentity(self, 'current').arn
        )
