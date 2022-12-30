from constructs import Construct
from cdktf import TerraformStack, S3Backend, TerraformOutput, TerraformAsset, AssetType

from imports.aws.provider import AwsProvider
from imports.aws.vpc import Vpc

region = "eu-central-1"  # the AWS region
# the AWS CLI profile to use; if not explicitly specified, "default" is used
profile = "default"

# equivalent to TF variables
environmentName = "dev"


class BasicVpcStack(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        # equivalent to TF provider
        AwsProvider(
            self,
            "aws",
            region=region
        )

        Vpc(
          self,
          "vpc-1",
          cidr_block="172.0.0.0/16",
          tags={
            "env": environmentName
          }
        )
