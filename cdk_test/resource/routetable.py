from aws_cdk.aws_ec2 import (
    CfnVPC, 
    CfnNatGateway, 
    CfnSubnet, 
    CfnInternetGateway,
    CfnRouteTable,
    CfnRoute,
    CfnSubnetRouteTableAssociation
)
from constructs import Construct
from .resource import Resource

class RouteTable(Resource):
    def __init__(self, scope: Construct, id: str,
                 vpc: CfnVPC,
                 subnetpublic1a: CfnSubnet,
                 subnetpublic1c: CfnSubnet,
                 subnetapp1a: CfnSubnet,
                 subnetapp1c: CfnSubnet,
                 subnetdb1a: CfnSubnet,
                 subnetdb1c: CfnSubnet,
                 igw: CfnInternetGateway,
                 ngw1a: CfnNatGateway,
                 ngw1c: CfnNatGateway
                 ):
        super().__init__(scope,id)
        self.public  = CfnRouteTable
        self.app1a  = CfnRouteTable
        self.app1c = CfnRouteTable
        self.db = CfnRouteTable

        self.vpc = vpc
        self.subnetPublic1a = subnetpublic1a
        self.subnetPublic1c = subnetpublic1c
        self.subnetApp1a = subnetapp1a
        self.subnetApp1c = subnetapp1c
        self.subnetDb1a = subnetdb1a
        self.subnetDb1c = subnetdb1c
        self.internetGateway = igw
        self.natGateway1a = ngw1a
        self.natGateway1c = ngw1c

        self.resourcesInfo = [
            {
                "id":"RouteTablePublic",
                "resourceName":"rtb-public",
                "routes":[{
                    "id": "RoutePublic",
                    "destinationCidrBlock": "0.0.0.0/0",
                    "gatewayId": self.internetGateway.ref
                }],
                "associations": [
                    {
                    "id": "AssociationPublic1a",
                    "subnetId": self.subnetPublic1a.ref
                    },
                    {
                    "id": "AssociationPublic1c",
                    "subnetId": self.subnetPublic1c.ref
                    }
                ],
                "assign": lambda routeTable: setattr(self, "public", routeTable)
            },
            {
                "id":"RouteTableApp1a",
                "resourceName":"rtb-app-1a",
                "routes":[{
                    "id": "RouteApp1a",
                    "destinationCidrBlock": "0.0.0.0/0",
                    "natGatewayId": self.natGateway1a.ref
                }],
                "associations": [
                    {
                    "id": "AssociationApp1a",
                    "subnetId": self.subnetApp1a.ref
                    }
                ],
                "assign": lambda routeTable: setattr(self, "app1a", routeTable)
            },
            {
                "id":"RouteTableApp1c",
                "resourceName":"rtb-app-1c",
                "routes":[{
                    "id": "RouteApp1c",
                    "destinationCidrBlock": "0.0.0.0/0",
                    "natGatewayId": self.natGateway1c.ref
                }],
                "associations": [
                    {
                    "id": "AssociationApp1c",
                    "subnetId": self.subnetApp1c.ref
                    }
                ],
                "assign": lambda routeTable: setattr(self, "app1c", routeTable)
            },
            {
                "id":"RouteTableDb",
                "resourceName":"rtb-db",
                "routes":[],
                "associations": [
                    {
                    "id": "AssociationDb1a",
                    "subnetId": self.subnetDb1a.ref
                    },
                    {
                    "id": "AssociationDb1c",
                    "subnetId": self.subnetDb1c.ref
                    }
                ],
                "assign": lambda routeTable: setattr(self, "db", routeTable)
            }
        ]

    def create_resources(self, scope: Construct):
        for resourceinfo in self.resourcesInfo:
            routeTable = self.createRouteTable(scope,resourceinfo)
            resourceinfo["assign"](routeTable)
    
    def createRouteTable(self, scope: Construct, resourceinfo: dict):
        routeTable = CfnRouteTable(scope,
            resourceinfo["id"],
            vpc_id=self.vpc.ref,
            tags=[{'key': 'Name', 'value': self.create_resource_name(scope, resourceinfo["resourceName"])}]
        )

        for routeInfo in resourceinfo["routes"]:
            self.createRoute(scope,routeInfo,routeTable)

        for associationInfo in resourceinfo["associations"]:
            self.createAssociation(scope,associationInfo,routeTable)

        return routeTable
    
    def createRoute(self,scope: Construct, routeInfo, routeTable):
        if("gatewayId" in routeInfo):
            route = CfnRoute(scope,
                routeInfo["id"],
                route_table_id=routeTable.ref,
                destination_cidr_block=routeInfo["destinationCidrBlock"],
                gateway_id=routeInfo["gatewayId"]
        )

        elif("natGatewayId" in routeInfo):
            route = CfnRoute(scope,
                routeInfo["id"],
                route_table_id=routeTable.ref,
                destination_cidr_block=routeInfo["destinationCidrBlock"],
                nat_gateway_id=routeInfo["natGatewayId"]
        )

    def createAssociation(self,scope: Construct,associationInfo,routeTable):
        CfnSubnetRouteTableAssociation(scope,
            associationInfo["id"],
            route_table_id=routeTable.ref,
            subnet_id=associationInfo["subnetId"]
        )


