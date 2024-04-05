from aws_cdk.aws_ec2 import CfnSubnet,CfnVPC
from constructs import Construct
from .resource import Resource
from .vpc import Vpc

class Subnet(Resource):
    def __init__(self, scope: Construct, vpc: CfnVPC,id: str):
        super().__init__(scope,id)
        self.public1a = None
        self.public1c = None
        self.app1a = None
        self.app1c = None
        self.db1a = None
        self.db1c = None
        self.vpc = vpc

        self.resources_info = [
            {
                "id": 'SubnetPublic1a',
                "cidr_block": '10.0.11.0/24',
                "availability_zone": 'ap-northeast-1a',
                "resourceName": 'subnet-public-1a',
                "assign": lambda subnet: setattr(self, "public1a", subnet),
            },
            {
                "id": 'SubnetPublic1c',
                "cidr_block": '10.0.12.0/24',
                "availability_zone": 'ap-northeast-1c',
                "resourceName": 'subnet-public-1c',
                "assign": lambda subnet: setattr(self, "public1c", subnet),
            },
            {
                "id": 'SubnetApp1a',
                "cidr_block": '10.0.21.0/24',
                "availability_zone": 'ap-northeast-1a',
                "resourceName": 'subnet-app-1a',
                "assign": lambda subnet: setattr(self, "app1a", subnet),
            },
            {
                "id": 'SubnetApp1c',
                "cidr_block": '10.0.22.0/24',
                "availability_zone": 'ap-northeast-1c',
                "resourceName": 'subnet-app-1c',
                "assign": lambda subnet: setattr(self, "app1c", subnet),
            },
            {
                "id": 'SubnetDb1a',
                "cidr_block": '10.0.31.0/24',
                "availability_zone": 'ap-northeast-1a',
                "resourceName": 'subnet-db-1a',
                "assign": lambda subnet: setattr(self, "db1a", subnet),
            },
            {
                "id": 'SubnetDb1c',
                "cidr_block": '10.0.32.0/24',
                "availability_zone": 'ap-northeast-1c',
                "resourceName": 'subnet-db-1c',
                "assign": lambda subnet: setattr(self, "db1c", subnet),
            }
        ]
    
    def create_resources(self, scope: Construct):
        for resource_info in self.resources_info:
            subnet = self.create_subnet(scope,resource_info)
            resource_info["assign"](subnet)
    
    def create_subnet(self, scope: Construct, resource_info: dict):
        subnet = CfnSubnet(
            scope,
            resource_info["id"],
            cidr_block=resource_info["cidr_block"],
            vpc_id=self.vpc.ref,
            availability_zone=resource_info["availability_zone"],
            tags=[{'key': 'Name', 'value': self.create_resource_name(scope, resource_info["resourceName"])}]
        )

        return subnet
