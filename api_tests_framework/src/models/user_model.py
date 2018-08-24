from .base_model import BaseModel


class UserModel(BaseModel):
    def __init__(self, external_model):
        super(UserModel, self).__init__(external_model=external_model)
        self.firstname = external_model["firstname"]
        self.lastname = external_model["lastname"]
        self.username = external_model["username"]
