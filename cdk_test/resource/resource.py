from constructs import Construct

class Resource(Construct):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

    def create_resources(self, scope: Construct) -> None:
        pass

    def create_resource_name(self, scope: Construct, original_name: str) -> str:
        system_name = scope.node.try_get_context('system_name')
        env_type = scope.node.try_get_context('envType')
        resource_name_prefix = f"{system_name}-{env_type}-"

        return f"{resource_name_prefix}{original_name}"