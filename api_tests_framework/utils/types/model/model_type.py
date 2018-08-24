from enum import Enum


class ModelType(Enum):
    USER_MODEL = "UserModel"
    THREAD_APPLICATION_MODEL = "ThreadApplicationModel"
    THREAD_INVITATION_MODEL = "ThreadInvitationModel"
    THREAD_MESSAGE_MODEL = "ThreadMessageModel"
    THREAD_MODEL = "ThreadModel"
    USERNAME_VALIDATION_MODEL = "UsernameValidationModel"
