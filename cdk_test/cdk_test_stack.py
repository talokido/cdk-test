from aws_cdk import (
    Stack,
)
from .resource.vpc import Vpc
from .resource.subnet import Subnet
from .resource.internetGateway import Igw
from .resource.elasticip import ElasticIp
from .resource.natgateway import NatGateway
from .resource.routetable import RouteTable
from .resource.networkacl import NetworkAcl
from .resource.iamrole import IamRole
from .resource.securitygroup import SecurityGroup
from .resource.ec2 import Ec2
from .resource.alb import Alb
from .resource.secretmanager import SecretManager
from .resource.rds import Rds
from constructs import Construct

class CdkTestStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = Vpc(self, "CdkTestVpc");
        vpc.create_resources(self);

        subnet = Subnet(self, vpc.vpc, "CdkTestSubnet");
        subnet.create_resources(self);

        igw = Igw(self, vpc.vpc, "CdkTestIgw");
        igw.create_resources(self);

        eip = ElasticIp(self, "CdkTestEip");
        eip.create_resources(self);

        natGateway = NatGateway(self, "CdkTestNgw",
                         subnet.public1a,
                         subnet.public1c,
                         eip.ngw1a,
                         eip.ngw1c
                         );
        natGateway.create_resources(self);

        routeTable = RouteTable(self, "CdkTestRt",
                         vpc.vpc,
                         subnet.public1a,
                         subnet.public1c,
                         subnet.app1a,
                         subnet.app1c,
                         subnet.db1a,
                         subnet.db1c,
                         igw.igw,
                         natGateway.ngw1a,
                         natGateway.ngw1c
                         );
        routeTable.create_resources(self);

        networkAcl = NetworkAcl(self, "CdkTestNAcl",
                         vpc.vpc,
                         subnet.public1a,
                         subnet.public1c,
                         subnet.app1a,
                         subnet.app1c,
                         subnet.db1a,
                         subnet.db1c,
                         );
        networkAcl.create_resources(self);

        iamRole = IamRole(self, "CdkTestIamRole");
        iamRole.create_resources(self);

        securityGroup = SecurityGroup(self, "CdkTestSG",vpc.vpc);
        securityGroup.create_resources(self);

        ec2 = Ec2(self, "CdkTestEc2",
                  subnet.app1a,
                  subnet.app1c,
                  iamRole.instanceProfileEc2,
                  securityGroup.ec2
                  );
        ec2.create_resources(self);

        alb = Alb(self, "CdkTestAlb",
                  vpc.vpc,
                  subnet.public1a,
                  subnet.public1c,
                  securityGroup.alb,
                  ec2.instance1a,
                  ec2.instance1c
                  );
        alb.create_resources(self);

        secretmanager = SecretManager(self, "CdkTestSecretManager");
        secretmanager.create_resources(self);

        rds = Rds(self, "CdkTestRds",
                  subnet.db1a,
                  subnet.db1c,
                  securityGroup.rds,
                  secretmanager.rdsCluster,
                  iamRole.rds
                  );
        rds.create_resources(self);

