from aws_cdk.aws_ec2 import CfnNatGateway, CfnSubnet, CfnEIP
from constructs import Construct
from .resource import Resource

class NatGateway(Resource):
    def __init__(self, scope: Construct, id: str,
                 public1a: CfnSubnet,
                 public1c: CfnSubnet,
                 elasticIpNgw1a: CfnEIP,
                 elasticIpNgw1c: CfnEIP):
        super().__init__(scope,id)
        self.ngw1a = None
        self.ngw1c = None

        self.subnetPublic1a = public1a
        self.subnetPublic1c = public1c
        self.elasticIpNgw1a = elasticIpNgw1a
        self.elasticIpNgw1c = elasticIpNgw1c

        self.resourcesInfo = [
            {
                "id":"NatGateway1a",
                "resourceName":"ngw-1a",
                "allocationId":self.elasticIpNgw1a.attr_allocation_id,
                "subnetId":self.subnetPublic1a.ref,
                "assign": lambda natGateway: setattr(self, "ngw1a", natGateway)
            },
            {
                "id":"NatGateway1c",
                "resourceName":"ngw-1c",
                "allocationId":self.elasticIpNgw1c.attr_allocation_id,
                "subnetId":self.subnetPublic1c.ref,
                "assign": lambda natGateway: setattr(self, "ngw1c", natGateway)
            }
        ]

    def create_resources(self, scope: Construct):
        for resourceinfo in self.resourcesInfo:
            natGateway = self.createNatGateway(scope,resourceinfo)
            resourceinfo["assign"](natGateway)

    def createNatGateway(self, scope: Construct, resourceinfo: dict):
        natGateway = CfnNatGateway(scope,
            resourceinfo["id"],
            subnet_id=resourceinfo["subnetId"],
            allocation_id=resourceinfo["allocationId"],
            tags=[{'key': 'Name', 'value': self.create_resource_name(scope, resourceinfo["resourceName"])}]
        )
        return natGateway
