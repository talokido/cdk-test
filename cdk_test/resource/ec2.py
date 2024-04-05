from aws_cdk.aws_ec2 import (
    CfnInstance,
    CfnSubnet, 
    CfnSecurityGroup,
    UserData
)
from aws_cdk.aws_iam import CfnInstanceProfile
from constructs import Construct
from .resource import Resource
import os
import base64




class Ec2(Resource):
    def __init__(self, scope: Construct, id: str,
                 subnetApp1a: CfnSubnet,
                 subnetApp1c: CfnSubnet,
                 instanceProfileEc2: CfnInstanceProfile,
                 securityGroupEc2: CfnSecurityGroup
                 ):
        super().__init__(scope,id)
        self.subnetApp1a  = subnetApp1a
        self.subnetApp1c  = subnetApp1c
        self.instanceProfileEc2  = instanceProfileEc2
        self.securityGroupEc2 = securityGroupEc2

        self.latestImageIdAmazonLinux2023 = "ami-031134f7a79b6e424"
        self.instanceType = "t2.micro"

        self.userDataFilePath = os.path.join(os.path.dirname(__file__), "scripts/ec2/userData.sh")

        self.resourcesInfo = [
            {
                "id":"Ec2Instance1a",
                "availabilityzone":"ap-northeast-1a",
                "resourceName":"ec2-1a",
                "subnetId": self.subnetApp1a.ref,
                "assign": lambda instance: setattr(self, "instance1a", instance)
            },
            {
                "id":"Ec2Instance1c",
                "availabilityzone":"ap-northeast-1c",
                "resourceName":"ec2-1c",
                "subnetId": self.subnetApp1c.ref,
                "assign": lambda instance: setattr(self, "instance1c", instance)
            }
        ]

    def create_resources(self, scope: Construct):
        for resourceinfo in self.resourcesInfo:
            instance = self.createInstance(scope,resourceinfo)
            resourceinfo["assign"](instance)
 
    def createInstance(self, scope: Construct, resourceinfo: dict):
        with open(self.userDataFilePath, 'r') as file:
            user_data = base64.b64encode(file.read().encode()).decode()
        
        instance = CfnInstance(scope,
            resourceinfo["id"],
            availability_zone=resourceinfo["availabilityzone"],
            iam_instance_profile=self.instanceProfileEc2.ref,
            image_id=self.latestImageIdAmazonLinux2023,
            instance_type=self.instanceType,
            security_group_ids= [self.securityGroupEc2.attr_group_id],
            subnet_id=resourceinfo["subnetId"],
            user_data=user_data,
            tags=[{'key': 'Name', 'value': resourceinfo["resourceName"]}]
        )

        return instance

