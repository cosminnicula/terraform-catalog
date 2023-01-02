from constructs import Construct
from cdktf import TerraformStack, S3Backend, TerraformOutput, TerraformAsset, AssetType

from imports.aws.provider import AwsProvider
from imports.aws.vpc import Vpc
from imports.aws.subnet import Subnet
from imports.aws.internet_gateway import InternetGateway
from imports.aws.route_table import RouteTable
from imports.aws.route import Route
from imports.aws.route_table_association import RouteTableAssociation
from imports.aws.security_group import SecurityGroup, SecurityGroupIngress, SecurityGroupEgress
from imports.ec2_instance import Ec2Instance
from imports.aws.eip import Eip

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

        vpc = Vpc(
            self,
            "vpc-1",
            cidr_block="172.100.0.0/16",
            tags={
                "env": environmentName
            }
        )

        subnet = Subnet(
            self,
            "subnet-1",
            vpc_id=vpc.id,
            cidr_block="172.100.1.0/24",
            availability_zone="eu-central-1a",
            map_public_ip_on_launch=True
        )

        internetGateway = InternetGateway(
            self,
            "internet-gateway-1",
            vpc_id=vpc.id
        )

        routeTable = RouteTable(
            self,
            "route-table-1",
            vpc_id=vpc.id,
        )

        Route(
            self,
            "route-1",
            route_table_id=routeTable.id,
            destination_cidr_block="0.0.0.0/0",
            gateway_id=internetGateway.id
        )

        RouteTableAssociation(
            self,
            "route-table-association-1",
            route_table_id=routeTable.id,
            subnet_id=subnet.id
        )

        securityGroup = SecurityGroup(
            self,
            "security-group-1",
            description="Security group 1",
            vpc_id=vpc.id,
            ingress=[
                SecurityGroupIngress(
                    description="Allow port 22",
                    from_port=22,
                    to_port=22,
                    protocol="tcp",
                    cidr_blocks=["0.0.0.0/0"]
                ),
                SecurityGroupIngress(
                    description="Allow port 80",
                    from_port=80,
                    to_port=80,
                    protocol="tcp",
                    cidr_blocks=["0.0.0.0/0"]
                )
            ],
            egress=[SecurityGroupEgress(
                description="Allow all ports and IPs",
                from_port=0,
                to_port=0,
                protocol="-1",
                cidr_blocks=["0.0.0.0/0"]
            )]
        )

        ec2Instance = Ec2Instance(
            self,
            "ec2-1",
            instance_type="t2.micro",
            ami="ami-0a261c0e5f51090b1",
            key_name="cn-ec2-1",
            monitoring=False,
            vpc_security_group_ids=[securityGroup.id],
            subnet_id=subnet.id,
            tags={
                "env": environmentName
            }
        )

        # equivalent to TF depends_on meta-argument
        Eip(
          self,
          "eip-1",
          instance=ec2Instance.id_output,
          depends_on=[internetGateway]
        )
