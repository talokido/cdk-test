from aws_cdk.aws_ec2 import CfnInternetGateway,CfnVPCGatewayAttachment,CfnVPC
from constructs import Construct
from .resource import Resource

class Igw(Resource):
    def __init__(self, scope: Construct, vpc: CfnVPC, id: str):
        super().__init__(scope,id)
        self.vpc = vpc

    def create_resources(self, scope: Construct, ):

        self.igw = CfnInternetGateway(scope, "InternetGateway",
            tags=[{'key': 'Name', 'value': self.create_resource_name(scope, 'igw')}]
        )

        self.igw_attach = CfnVPCGatewayAttachment(scope,"VpcGatewayAttachment",
            vpc_id=self.vpc.ref,
            internet_gateway_id=self.igw.ref
        )

