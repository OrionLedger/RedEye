from . import NodeModel

class user_model(NodeModel):
    label = "User"
    required_fields = ["user_id"]

    def __init__(self, user_id, **kwargs):
        super().__init__(
            user_id=user_id,
            **kwargs
        )
