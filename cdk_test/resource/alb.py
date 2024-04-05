from aws_cdk.aws_ec2 import (
    CfnVPC,
    CfnInstance,
    CfnSubnet, 
    CfnSecurityGroup,
)
from aws_cdk.aws_elasticloadbalancingv2 import (
    CfnLoadBalancer,
    CfnTargetGroup,
    CfnListener
)
from constructs import Construct
from .resource import Resource

class Alb(Resource):
    def __init__(self, scope: Construct, id: str,
                 Vpc: CfnVPC,
                 subnetPublic1a: CfnSubnet,
                 subnetPublic1c: CfnSubnet,
                 securityGroupAlb: CfnSecurityGroup,
                 ec2Insatnace1a: CfnInstance,
                 ec2Insatnace1c: CfnInstance
                 ):
        super().__init__(scope,id)
        self.Vpc = Vpc
        self.subnetPublic1a  = subnetPublic1a
        self.subnetPublic1c  = subnetPublic1c
        self.securityGroupAlb = securityGroupAlb
        self.ec2Insatnace1a = ec2Insatnace1a
        self.ec2Insatnace1c = ec2Insatnace1c


    def create_resources(self, scope: Construct):
            loadBalancer = self.createLoadBalancer(scope)
            targetGroup = self.createTargetGroup(scope)
            self.createListner(scope, loadBalancer, targetGroup)
 
    def createLoadBalancer(self, scope: Construct):
        loadBalancer = CfnLoadBalancer(scope,
            "Alb",
            ip_address_type="ipv4",
            name=self.create_resource_name(scope, 'alb'),
            scheme="internet-facing",
            security_groups=[self.securityGroupAlb.attr_group_id],
            subnets=[self.subnetPublic1a.ref, self.subnetPublic1c.ref],
            type="application"
        )

        return loadBalancer

    def createTargetGroup(self, scope: Construct):
        targetGroup = CfnTargetGroup(scope,
            "AlbTargetGroup",
            name=self.create_resource_name(scope, 'tg'),
            port=80,
            protocol="HTTP",
            target_type="instance",
            targets=[
                 {"id": self.ec2Insatnace1a.ref},
                 {"id": self.ec2Insatnace1c.ref}
            ],
            vpc_id=self.Vpc.ref
        )

        return targetGroup
    
    def createListner(self, scope: Construct, loadBalancer: CfnLoadBalancer, targetGroup: CfnTargetGroup):
        CfnListener(scope,
            "AlbListner",
            default_actions=[
                {
                "type": "forward",
                "forwardConfig": {
                    "targetGroups": [
                        {
                        "targetGroupArn": targetGroup.ref,
                        "weight": 1
                        }
                    ]
                    }
                }
            ],
            load_balancer_arn=loadBalancer.ref,
            port=80,
            protocol="HTTP"
        )