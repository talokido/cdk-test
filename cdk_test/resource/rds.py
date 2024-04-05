
from aws_cdk.aws_rds import (
    CfnDBSubnetGroup,
    CfnDBClusterParameterGroup,
    CfnDBParameterGroup,
    CfnDBCluster,
    CfnDBInstance
)
from aws_cdk.aws_ec2 import (
    CfnSubnet,
    CfnSecurityGroup
)
from aws_cdk.aws_secretsmanager import CfnSecret
from aws_cdk.aws_iam import CfnRole
from constructs import Construct
from .resource import Resource
from .secretmanager import OSecretKey,SecretManager

class Rds(Resource):
    def __init__(self, scope: Construct, id: str,
                 subnetDb1a: CfnSubnet,
                 subnetDb1c: CfnSubnet,
                 securityGroupRds: CfnSecurityGroup,
                 secretRdsCluster: CfnSecret,
                 iamRoleRds: CfnRole
                 ):
        super().__init__(scope,id)
        self.subnetDb1a  = subnetDb1a
        self.subnetDb1c  = subnetDb1c
        self.securityGroupRds = securityGroupRds
        self.secretRdsCluster = secretRdsCluster
        self.iamRoleRds = iamRoleRds

        self.databasename = "devio"
        self.engine = "aurora-mysql"
        self.dbInstanceClass = "db.r5.large"
        
        self.instancesInfo = [
            {
                "id":"RdsInstance1a",
                "availabilityZone":"ap-northeast-1a",
                "preferredMaintenanceWindow":"sun:20:00-sun:20:30",
                "resourceName":"rds-instance-1a",
                "assign": lambda instance: setattr(self, "dbInstance", instance)
            },
            {
                "id":"RdsInstance1c",
                "availabilityZone":"ap-northeast-1c",
                "preferredMaintenanceWindow":"sun:20:30-sun:21:00",
                "resourceName":"rds-instance-1c",
                "assign": lambda instance: setattr(self, "dbInstance", instance)
            }
        ]

    def create_resources(self, scope: Construct):
            subnetGroup = self.createSubnetGroup(scope)
            clusterParameterGroup = self.createClusterParameterGroup(scope)
            parameterGroup = self.createParameterGroup(scope)
            self.dbCluster = self.createDbCluster(scope,subnetGroup,clusterParameterGroup)

            for instanceInfo in self.instancesInfo:
                 instance = self.createInstance(scope, instanceInfo, self.dbCluster, subnetGroup, parameterGroup)
                 instanceInfo["assign"](instance)

    def createSubnetGroup(self, scope: Construct):
        subnetGroup = CfnDBSubnetGroup(scope,
            "SubnetGroupRds",
            db_subnet_group_description="Subnet Group for RDS",
            subnet_ids=[self.subnetDb1a.ref,self.subnetDb1c.ref],
            db_subnet_group_name=self.create_resource_name(scope, "sng-rds")
        )

        return subnetGroup
    
    def createClusterParameterGroup(self, scope: Construct):
        clusterParameterGroup = CfnDBClusterParameterGroup(scope,
            "ClusterParameterGroupRds",
            description="ClusterParameter Group for RDS",
            family="aurora-mysql5.7",
            parameters={"time_zone": "UTC"}
        )

        return clusterParameterGroup
    
    def createParameterGroup(self, scope: Construct):
        parameterGroup = CfnDBParameterGroup(scope,
            "ParameterGroupRds",
            description="Parameter Group for RDS",
            family="aurora-mysql5.7"
        )

        return parameterGroup
    
    def createDbCluster(self, scope: Construct, subnetGroup:  CfnDBSubnetGroup,clusterParameterGroup: CfnDBClusterParameterGroup):
        dbCluster = CfnDBCluster(scope,
            "RdsDbCluster",
            engine = "aurora-mysql",
            backup_retention_period = 7,
            database_name = self.databasename,
            db_cluster_identifier = self.create_resource_name(scope, "rds-cluster"),
            db_cluster_parameter_group_name = clusterParameterGroup.ref,
            db_subnet_group_name = subnetGroup.ref,
            enable_cloudwatch_logs_exports = ["error"],
            engine_mode = "provisioned",
            engine_version = "5.7.mysql_aurora.2.11.4",
            master_user_password = SecretManager.getDynamicReference(self.secretRdsCluster, OSecretKey["MasterUserPassword"]),
            master_username = SecretManager.getDynamicReference(self.secretRdsCluster, OSecretKey["MasterUsername"]),
            port = 3306,
            preferred_backup_window = "19:00-19:30",
            preferred_maintenance_window = "sun:19:30-sun:20:00",
            storage_encrypted = True,
            vpc_security_group_ids = [self.securityGroupRds.attr_group_id]
        )

        return dbCluster
    
    def createInstance(self, scope: Construct, instanceInfo, cluster: CfnDBCluster,subnetGroup:  CfnDBSubnetGroup,parameterGroup: CfnDBParameterGroup):
        dbCluster = CfnDBInstance(scope,
            instanceInfo["id"],
            db_instance_class = self.dbInstanceClass,
            auto_minor_version_upgrade = False,
            availability_zone = instanceInfo["availabilityZone"],
            db_cluster_identifier = cluster.ref,
            db_instance_identifier = self.create_resource_name(scope, instanceInfo["resourceName"]),
            db_parameter_group_name = parameterGroup.ref,
            db_subnet_group_name = subnetGroup.ref,
            enable_performance_insights = True,
            engine = self.engine,
            monitoring_interval = 60,
            monitoring_role_arn = self.iamRoleRds.attr_arn,
            performance_insights_retention_period = 7,
            preferred_maintenance_window = instanceInfo["preferredMaintenanceWindow"]
        )

        return dbCluster