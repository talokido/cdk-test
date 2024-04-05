from aws_cdk.aws_iam import (
    CfnRole,
    CfnInstanceProfile,
    PolicyDocument,
    PolicyStatement,
    PolicyStatementProps,
    Effect,
    ServicePrincipal
)
from constructs import Construct
from .resource import Resource

class IamRole(Resource):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope,id)
        self.ec2 = None
        self.rd2 = None
        self.instanceProfileEc2 = None

        self.resourcesInfo = [
            {
                "id":"RoleEc2",
                "policyStatementProps": [
                    {
                    "effect": Effect.ALLOW,
                    "principals": [
                        ServicePrincipal("ec2.amazonaws.com")
                    ],
                    "actions": [
                        "sts:AssumeRole"
                    ]
                    }
                ],
                "managedPolicyArns": [
                    "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore",
                    "arn:aws:iam::aws:policy/AmazonRDSFullAccess"
                ],
                "roleName": "role-ec2",
                "assign": lambda role: setattr(self, "ec2", role)
            },
            {
                "id":"RoleRds",
                "policyStatementProps": [
                    {
                    "effect": Effect.ALLOW,
                    "principals": [
                        ServicePrincipal("monitoring.rds.amazonaws.com")
                    ],
                    "actions": [
                        "sts:AssumeRole"
                    ]
                    }
                ],
                "managedPolicyArns": [
                    "arn:aws:iam::aws:policy/service-role/AmazonRDSEnhancedMonitoringRole"
                ],
                "roleName": "role-rds",
                "assign": lambda role: setattr(self, "rds", role)
            }
        ]

    def create_resources(self, scope: Construct):
        for resourceinfo in self.resourcesInfo:
            role = self.createRole(scope,resourceinfo)
            resourceinfo["assign"](role)
        
        self.instanceProfileEc2 = CfnInstanceProfile(scope,
            "InstanceProfileEc2",
            roles=[self.ec2.ref],
            instance_profile_name=self.ec2.role_name
            )
    
    def createRole(self, scope: Construct, resourceinfo: dict):
        policyresourceinfo = resourceinfo["policyStatementProps"][0]
        policyStatement = PolicyStatement(
            actions=policyresourceinfo["actions"],
            effect=policyresourceinfo["effect"],
            principals=policyresourceinfo["principals"]
        )
        policyDocument = PolicyDocument(
            statements=[policyStatement]
        )

        role = CfnRole(scope,
                       resourceinfo["id"],
                       assume_role_policy_document=policyDocument,
                       managed_policy_arns=resourceinfo["managedPolicyArns"],
                       role_name=resourceinfo["roleName"]
                       )

        return role