from aws_cdk.aws_secretsmanager import CfnSecret
from constructs import Construct
from .resource import Resource

OSecretKey = {
            "MasterUsername": "MasterUsername",
            "MasterUserPassword": "MasterUserPassword"
        }

class ResourceInfo:
     def __init__(self, id, description,generateSecretstring,resourceName,assign):
          self.id = id
          self.description = description
          self.generateSecretstring = generateSecretstring
          self.resourceName = resourceName
          self.assign = assign

class SecretManager(Resource):
    
    def __init__(self, scope: Construct, id: str,):
        super().__init__(scope,id)
    
        self.rdsClusterMasterUsername = "admin"
        self.resourceInfo = ResourceInfo(
                id = "SecretRdsCluster",
                description = "for RDS cluster",
                generateSecretstring = {
                     "excludeCharacters": "\"@/\\\'",
                     "generateStringKey": OSecretKey["MasterUserPassword"],
                     "passwordLength": 16,
                     "secretStringTemplate": f'{{"{OSecretKey["MasterUsername"]}": "{self.rdsClusterMasterUsername}"}}'
                },
                resourceName = "secret-rds-cluster",
                assign = lambda secret: setattr(self, "rdsCluster", secret)
        )
    
    def create_resources(self, scope: Construct):
            secret = self.createSecret(scope,self.resourceInfo)
            self.resourceInfo.assign(secret)
    
    @staticmethod
    def getDynamicReference(secret: CfnSecret, secretKey: str ):
         return f'{{{{resolve:secretsmanager:{secret.ref}:SecretString:{secretKey}}}}}'
 
    def createSecret(self, scope: Construct,resourceInfo):
        
        secret = CfnSecret(scope,
            resourceInfo.id,
            description=resourceInfo.description,
            generate_secret_string=resourceInfo.generateSecretstring,
            name=self.create_resource_name(scope, resourceInfo.resourceName)
        )

        return secret