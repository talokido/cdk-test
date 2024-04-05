from aws_cdk.aws_ec2 import (
    CfnSecurityGroup, 
    CfnSecurityGroupIngress, 
    CfnVPC
)
from constructs import Construct
from .resource import Resource

class SecurityGroup(Resource):
    def __init__(self, scope: Construct, id: str,
                 vpc: CfnVPC
                 ):
        super().__init__(scope,id)
        self.alb  = CfnSecurityGroup
        self.ec2  = CfnSecurityGroup
        self.rds = CfnSecurityGroup

        self.vpc = vpc

        self.resourcesInfo = [
            {
                "id":"SecureGroupAlb",
                "groupDescription":"for ALB",
                "ingress": [
                    {
                    "id": "SecurityGroupIngressAlb1",
                    "SecurityGroupIngressProps": {
                        "ipProtocols": "tcp",
                        "cidrIp": "0.0.0.0/0",
                        "fromPort": 80,
                        "toPort": 80
                        },
                    "groupId": lambda : self.alb.attr_group_id
                    },
                    {
                    "id": "SecurityGroupIngressAlb2",
                    "SecurityGroupIngressProps": {
                        "ipProtocols": "tcp",
                        "cidrIp": "0.0.0.0/0",
                        "fromPort": 443,
                        "toPort": 443
                        },
                    "groupId": lambda : self.alb.attr_group_id
                    },
                ],
                "resourceName": "sg-alb",
                "assign": lambda securityGroup: setattr(self, "alb", securityGroup)
            },
            {
                "id":"SecureGroupEc2",
                "groupDescription":"for EC2",
                "ingress": [
                    {
                    "id": "SecurityGroupIngressEc21",
                    "SecurityGroupIngressProps": {
                        "ipProtocols": "tcp",
                        "fromPort": 80,
                        "toPort": 80
                        },
                    "groupId": lambda : self.ec2.attr_group_id,
                    "sourceSecurityGroupId": lambda : self.alb.attr_group_id
                    },
                ],
                "resourceName": "sg-ec2",
                "assign": lambda securityGroup: setattr(self, "ec2", securityGroup)
            },
            {
                "id":"SecureGroupRds",
                "groupDescription":"for RDS",
                "ingress": [
                    {
                    "id": "SecurityGroupIngressRds1",
                    "SecurityGroupIngressProps": {
                        "ipProtocols": "tcp",
                        "fromPort": 3306,
                        "toPort": 3306
                        },
                    "groupId": lambda : self.rds.attr_group_id,
                    "sourceSecurityGroupId": lambda : self.ec2.attr_group_id
                    },
                ],
                "resourceName": "sg-rds",
                "assign": lambda securityGroup: setattr(self, "rds", securityGroup)
            }
        ]

    def create_resources(self, scope: Construct):
        for resourceinfo in self.resourcesInfo:
            securityGroup = self.createSecurityGroup(scope,resourceinfo)
            resourceinfo["assign"](securityGroup)

            self.createSecurityGroupIngress(scope,resourceinfo)
    
    def createSecurityGroup(self, scope: Construct, resourceinfo: dict):
        resourceName = self.create_resource_name(scope, resourceinfo["resourceName"])
        securityGroup = CfnSecurityGroup(scope,
            resourceinfo["id"],
            group_description=resourceinfo["groupDescription"],
            group_name=resourceName,
            vpc_id=self.vpc.ref,
            tags=[{'key': 'Name', 'value': resourceName}]
        )

        return securityGroup
    
    def createSecurityGroupIngress(self,scope: Construct, resourceinfo: dict):
        for ingress in resourceinfo["ingress"]:
            SecurityGroupIngressinfo = ingress["SecurityGroupIngressProps"]
            security_group_id = ingress["groupId"]()
            if ("cidrIp" in SecurityGroupIngressinfo):
                SecurityGroupIngress= CfnSecurityGroupIngress(scope,
                    ingress["id"],
                    ip_protocol=SecurityGroupIngressinfo["ipProtocols"],
                    from_port=SecurityGroupIngressinfo["fromPort"],
                    to_port=SecurityGroupIngressinfo["toPort"],
                    cidr_ip=SecurityGroupIngressinfo["cidrIp"],
                    group_id=security_group_id
                )

            elif ("sourceSecurityGroupId" in ingress):
                source_security_group_Id=ingress["sourceSecurityGroupId"]()
                SecurityGroupIngress= CfnSecurityGroupIngress(scope,
                    ingress["id"],
                    ip_protocol=SecurityGroupIngressinfo["ipProtocols"],
                    from_port=SecurityGroupIngressinfo["fromPort"],
                    to_port=SecurityGroupIngressinfo["toPort"],
                    source_security_group_id=source_security_group_Id,
                    group_id=security_group_id
                )

            SecurityGroupIngress = ingress["groupId"]


