from .base_model import BaseModel


class ThreadInvitationModel(BaseModel):
    def __init__(self, external_model):
        super(ThreadInvitationModel, self).__init__(external_model=external_model)
        self.user = external_model["user"]
        self.thread = external_model["thread"]
        self.status = external_model["status"]
        self.invited_by = external_model["invitedBy"]
        self.users_in_thread = external_model["usersInThread"]
        self.deleted = external_model["deleted"]
