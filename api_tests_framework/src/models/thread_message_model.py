from .base_model import BaseModel


class ThreadMessageModel(BaseModel):
    def __init__(self, external_model):
        super(ThreadMessageModel, self).__init__(external_model=external_model)
        self.user = external_model["user"]
        self.thread = external_model["thread"]
        self.message = external_model["message"]
        self.deleted = external_model["deleted"]
