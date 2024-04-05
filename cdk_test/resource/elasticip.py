from aws_cdk.aws_ec2 import CfnEIP
from constructs import Construct
from .resource import Resource

class ElasticIp(Resource):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope,id)
        self.ngw1a = None
        self.ngw1c = None

        self.resourcesInfo = [
            {
                "id":"ElasticIpNgw1a",
                "resourceName":"eip-ngw-1a",
                "assign": lambda elastic_ip: setattr(self, "ngw1a", elastic_ip)
            },
            {
                "id":"ElasticIpNgw1c",
                "resourceName":"eip-ngw-1c",
                "assign": lambda elastic_ip: setattr(self, "ngw1c", elastic_ip)
            }
        ]

    def create_resources(self, scope: Construct, ):
        for resourceinfo in self.resourcesInfo:
            elasticIp = self.createElasticIp(scope,resourceinfo)
            resourceinfo["assign"](elasticIp)

    def createElasticIp(self, scope: Construct, resourceinfo: dict):
        elasticIp = CfnEIP(scope,
            resourceinfo["id"],
            domain="vpc",
            tags=[{'key': 'Name', 'value': self.create_resource_name(scope, resourceinfo["resourceName"])}]
        )
        return elasticIp
