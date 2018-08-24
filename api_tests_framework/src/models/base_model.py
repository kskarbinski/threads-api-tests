class BaseModel(object):
    def __init__(self, external_model):
        self.id = external_model["id"]
        self.created_at = external_model["createdAt"]
        self.updated_at = external_model["updatedAt"]
        self.model_type = external_model["modelType"]
