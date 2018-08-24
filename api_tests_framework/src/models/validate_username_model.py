from .base_model import BaseModel


class ValidateUsernameModel(BaseModel):
    def __init__(self, external_model):
        super(ValidateUsernameModel, self).__init__(external_model=external_model)
        self.errors = external_model["errors"]
