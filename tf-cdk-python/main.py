from cdktf import App

from stack.aws.ec2.basic import BasicEc2Stack
from stack.aws.vpc.basic import BasicVpcStack

app = App()

# BasicEc2Stack(app, "basic-ec2-stack")
BasicVpcStack(app, "basic-vpc-stack")

app.synth()
