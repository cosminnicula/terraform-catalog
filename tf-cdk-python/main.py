from cdktf import App

from stack.aws.ec2.basic import BasicEc2Stack

app = App()

BasicEc2Stack(app, "basic-ec2-stack")

app.synth()
