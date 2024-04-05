from aws_cdk.aws_ec2 import (
    CfnVPC, 
    CfnSubnet, 
    CfnNetworkAcl,
    CfnNetworkAclEntry,
    CfnNetworkAclEntryProps,
    CfnSubnetNetworkAclAssociation
)
from constructs import Construct
from .resource import Resource

class NetworkAcl(Resource):
    def __init__(self, scope: Construct, id: str,
                 vpc: CfnVPC,
                 subnetpublic1a: CfnSubnet,
                 subnetpublic1c: CfnSubnet,
                 subnetapp1a: CfnSubnet,
                 subnetapp1c: CfnSubnet,
                 subnetdb1a: CfnSubnet,
                 subnetdb1c: CfnSubnet
                 ):
        super().__init__(scope,id)
        self.public  = CfnNetworkAcl
        self.app  = CfnNetworkAcl
        self.db = CfnNetworkAcl

        self.vpc = vpc
        self.subnetPublic1a = subnetpublic1a
        self.subnetPublic1c = subnetpublic1c
        self.subnetApp1a = subnetapp1a
        self.subnetApp1c = subnetapp1c
        self.subnetDb1a = subnetdb1a
        self.subnetDb1c = subnetdb1c

        self.resourcesInfo = [
            {
                "id":"NetworkAclPublic",
                "resourceName":"nacl-public",
                "entryIdInbound": "NetworkAclEntryInboundPublic",
                "entryIdOutbound": "NetworkAclEntryOutboundPublic",
                "associations": [
                    {
                    "id": "NetworkAclAssociationPublic1a",
                    "subnetId": self.subnetPublic1a.ref
                    },
                    {
                    "id": "NetworkAclAssociationPublic1c",
                    "subnetId": self.subnetPublic1c.ref
                    }
                ],
                "assign": lambda networkAcl: setattr(self, "public", networkAcl)
            },
            {
                "id":"NetworkAclApp",
                "resourceName":"nacl-app",
                "entryIdInbound": "NetworkAclEntryInboundApp",
                "entryIdOutbound": "NetworkAclEntryOutboundApp",
                "associations": [
                    {
                    "id": "NetworkAclAssociationApp1a",
                    "subnetId": self.subnetApp1a.ref
                    },
                    {
                    "id": "NetworkAclAssociationApp1c",
                    "subnetId": self.subnetApp1c.ref
                    }
                ],
                "assign": lambda networkAcl: setattr(self, "app", networkAcl)
            },
            {
                "id":"NetworkAclDb",
                "resourceName":"nacl-db",
                "entryIdInbound": "NetworkAclEntryInboundDb",
                "entryIdOutbound": "NetworkAclEntryOutboundDb",
                "associations": [
                    {
                    "id": "NetworkAclAssociationDb1a",
                    "subnetId": self.subnetDb1a.ref
                    },
                    {
                    "id": "NetworkAclAssociationDb1c",
                    "subnetId": self.subnetDb1c.ref
                    }
                ],
                "assign": lambda networkAcl: setattr(self, "db", networkAcl)
            }
        ]

    def create_resources(self, scope: Construct):
        for resourceinfo in self.resourcesInfo:
            networkAcl = self.createNetworkAcl(scope,resourceinfo)
            resourceinfo["assign"](networkAcl)
    
    def createNetworkAcl(self, scope: Construct, resourceinfo: dict):
        networkAcl = CfnNetworkAcl(scope,
            resourceinfo["id"],
            vpc_id=self.vpc.ref,
            tags=[{'key': 'Name', 'value': self.create_resource_name(scope, resourceinfo["resourceName"])}]
        )

        self.createEntry(scope,resourceinfo["entryIdInbound"], networkAcl, egress=False)
        self.createEntry(scope,resourceinfo["entryIdOutbound"], networkAcl, egress=True)

        for associationInfo in resourceinfo["associations"]:
            self.createAssociation(scope,associationInfo,networkAcl)

        return networkAcl
    
    def createEntry(self,scope: Construct, entryId, networkAcl, egress: bool):
        entry = CfnNetworkAclEntry(scope,
                entryId,
                network_acl_id=networkAcl.ref,
                protocol=-1,
                rule_action="allow",
                rule_number=100,
                cidr_block="0.0.0.0/0",
                egress=egress
        )

    def createAssociation(self,scope: Construct,associationInfo: dict,networkAcl):
        CfnSubnetNetworkAclAssociation(scope,
            associationInfo["id"],
            network_acl_id=networkAcl.ref,
            subnet_id=associationInfo["subnetId"]
        )


