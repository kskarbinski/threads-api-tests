from .base_model import BaseModel


class ThreadModel(BaseModel):
    def __init__(self, external_model):
        super(ThreadModel, self).__init__(external_model=external_model)
        self.name = external_model["name"]
        self.owner = external_model["owner"]
        self.users = external_model["users"]
        self.private = external_model["private"]
        self.deleted = external_model["deleted"]
