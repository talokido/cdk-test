from aws_cdk.aws_ec2 import CfnVPC
from constructs import Construct
from .resource import Resource

class Vpc(Resource):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope,id)

    def create_resources(self, scope: Construct):

        self.vpc = CfnVPC(scope, 'Vpc',
            cidr_block='10.0.0.0/16',
            tags=[{'key': 'Name', 'value': self.create_resource_name(scope, 'vpc')}]
        )