from .base_model import BaseModel


class ThreadApplicationModel(BaseModel):
    def __init__(self, external_model):
        super(ThreadApplicationModel, self).__init__(external_model=external_model)
        self.user = external_model["user"]
        self.thread = external_model["thread"]
        self.status = external_model["status"]
        self.deleted = external_model["deleted"]
