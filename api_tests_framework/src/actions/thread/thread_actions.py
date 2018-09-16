from api_tests_framework.src.actions import BaseActions
from api_tests_framework.src.handlers.threads import ThreadsHandler
from api_tests_framework.src.handlers.threads.id import ThreadsIdHandler
from api_tests_framework.src.handlers.threads.id.kick import ThreadsIdKickHandler
from api_tests_framework.src.handlers.threads.id.invite import ThreadsIdInviteHandler
from api_tests_framework.src.handlers.threads.id.apply import ThreadsIdApplyHandler
from api_tests_framework.src.handlers.threads.id.invitations import ThreadsIdInvitationsHandler
from api_tests_framework.src.handlers.threads.id.applications import ThreadsIdApplicationsHandler
from api_tests_framework.src.handlers.threads.id.messages import ThreadsIdMessagesHandler
from api_tests_framework.src.handlers.threads.invitations import ThreadsInvitationsHandler
from api_tests_framework.src.handlers.threads.applications import ThreadsApplicationsHandler
from api_tests_framework.src.handlers.threads.invitations.id import ThreadsInvitationsIdHandler
from api_tests_framework.src.handlers.threads.applications.id import ThreadsApplicationsIdHandler
from api_tests_framework.src.handlers.threads.id.invitations.id import ThreadsIdInvitationsIdHandler
from api_tests_framework.src.handlers.threads.id.applications.id import ThreadsIdApplicationsIdHandler
from api_tests_framework.src.handlers.threads.id.messages.id import ThreadsIdMessagesIdHandler

from api_tests_framework.src.models import (
    ThreadModel, ThreadInvitationModel, ThreadApplicationModel, ThreadMessageModel
)

from api_tests_framework.utils.helpers import generate_random_name, generate_random_words


class ThreadActions(BaseActions):
    def create_thread(self, name=None, private=False):
        # Randomize name if not given
        name = generate_random_name() if name is None else name

        # Send request
        response = ThreadsHandler(actor=self.actor).post(
            name=name,
            private=private
        )

        # Parse model
        model = ThreadModel(external_model=response.json())

        return model

    def get_threads(self):
        # Send request
        response = ThreadsHandler(actor=self.actor).get()

        # Parse models
        models = [ThreadModel(external_model=external_model) for external_model in response.json()["items"]]

        return models

    def get_thread(self, thread_id):
        # Send request
        response = ThreadsIdHandler(actor=self.actor).get(thread_id=thread_id)

        # Parse model
        model = ThreadModel(external_model=response.json())

        return model

    def delete_thread(self, thread_id):
        # Send request
        response = ThreadsIdHandler(actor=self.actor).delete(thread_id=thread_id)

        # Parse model
        model = ThreadModel(external_model=response.json())

        return model

    def kick_users_from_thread(self, thread_id, user_ids):
        # Send request
        response = ThreadsIdKickHandler(actor=self.actor).post(thread_id=thread_id, user_ids=user_ids)

        # Parse model
        model = ThreadModel(external_model=response.json())

        return model

    def invite_users_to_thread(self, thread_id, user_ids):
        # Send request
        response = ThreadsIdInviteHandler(actor=self.actor).post(thread_id=thread_id, user_ids=user_ids)

        # Parse models
        models = [ThreadInvitationModel(external_model=external_model) for external_model in response.json()]

        return models

    def apply_to_thread(self, thread_id):
        # Send request
        response = ThreadsIdApplyHandler(actor=self.actor).post(thread_id=thread_id)

        # Parse model
        model = ThreadApplicationModel(external_model=response.json())

        return model

    def get_sent_thread_invitations(self, thread_id):
        # Send request
        response = ThreadsIdInvitationsHandler(actor=self.actor).get(thread_id=thread_id)

        # Parse models
        models = [ThreadInvitationModel(external_model=external_model)
                  for external_model in response.json()["items"]]

        return models

    def get_received_thread_applications(self, thread_id):
        # Send request
        response = ThreadsIdApplicationsHandler(actor=self.actor).get(thread_id=thread_id)

        # Parse models
        models = [ThreadApplicationModel(external_model=external_model)
                  for external_model in response.json()["items"]]

        return models

    def get_thread_messages(self, thread_id):
        # Send request
        response = ThreadsIdMessagesHandler(actor=self.actor).get(thread_id=thread_id)

        # Parse models
        models = [ThreadMessageModel(external_model=external_model) for external_model in response.json()["items"]]

        return models

    def send_message_in_thread(self, thread_id, message=None):
        # Randomize message
        message = generate_random_words(1, 10) if message is None else message

        # Send request
        response = ThreadsIdMessagesHandler(actor=self.actor).post(thread_id=thread_id, message=message)

        # Parse model
        model = ThreadMessageModel(external_model=response.json())

        return model

    def get_received_thread_invitations(self):
        # Send request
        response = ThreadsInvitationsHandler(actor=self.actor).get()

        # Parse models
        models = [ThreadInvitationModel(external_model=external_model)
                  for external_model in response.json()["items"]]

        return models

    def get_sent_thread_applications(self):
        # Send request
        response = ThreadsApplicationsHandler(actor=self.actor).get()

        # Parse models
        models = [ThreadApplicationModel(external_model=external_model)
                  for external_model in response.json()["items"]]

        return models

    def get_received_thread_invitation(self, invitation_id):
        # Send request
        response = ThreadsInvitationsIdHandler(actor=self.actor).get(invitation_id=invitation_id)

        # Parse model
        model = ThreadInvitationModel(external_model=response.json())

        return model

    def accept_or_reject_thread_invitation(self, invitation_id, accept):
        # Send request
        response = ThreadsInvitationsIdHandler(actor=self.actor).post(invitation_id=invitation_id, accept=accept)

        # Parse model
        model = ThreadInvitationModel(external_model=response.json())

        return model

    def get_sent_thread_application(self, application_id):
        # Send request
        response = ThreadsApplicationsIdHandler(actor=self.actor).get(application_id=application_id)

        # Parse model
        model = ThreadApplicationModel(external_model=response.json())

        return model

    def cancel_sent_thread_application(self, application_id):
        # Send request
        response = ThreadsApplicationsIdHandler(actor=self.actor).delete(application_id=application_id)

        # Parse model
        model = ThreadApplicationModel(external_model=response.json())

        return model

    def get_sent_thread_invitation(self, thread_id, invitation_id):
        # Send request
        response = ThreadsIdInvitationsIdHandler(actor=self.actor).get(thread_id=thread_id, invitation_id=invitation_id)

        # Parse model
        model = ThreadInvitationModel(external_model=response.json())

        return model

    def cancel_sent_thread_invitation(self, thread_id, invitation_id):
        # Send request
        response = ThreadsIdInvitationsIdHandler(
            actor=self.actor
        ).delete(
            thread_id=thread_id,
            invitation_id=invitation_id
        )

        # Parse model
        model = ThreadInvitationModel(external_model=response.json())

        return model

    def get_received_thread_application(self, thread_id, application_id):
        # Send request
        response = ThreadsIdApplicationsIdHandler(
            actor=self.actor
        ).get(
            thread_id=thread_id,
            application_id=application_id
        )

        # Parse model
        model = ThreadApplicationModel(external_model=response.json())

        return model

    def accept_or_reject_thread_application(self, thread_id, application_id, accept):
        # Send request
        response = ThreadsIdApplicationsIdHandler(
            actor=self.actor
        ).post(
            thread_id=thread_id,
            application_id=application_id,
            accept=accept
        )

        # Parse model
        model = ThreadApplicationModel(external_model=response.json())

        return model

    def get_thread_message(self, thread_id, message_id):
        # Send request
        response = ThreadsIdMessagesIdHandler(actor=self.actor).get(thread_id=thread_id, message_id=message_id)

        # Parse model
        model = ThreadMessageModel(external_model=response.json())

        return model

    def edit_thread_message(self, thread_id, message_id, message):
        # Send request
        response = ThreadsIdMessagesIdHandler(
            actor=self.actor
        ).post(
            thread_id=thread_id,
            message_id=message_id,
            message=message
        )

        # Parse model
        model = ThreadMessageModel(external_model=response.json())

        return model

    def remove_thread_message(self, thread_id, message_id):
        # Send request
        response = ThreadsIdMessagesIdHandler(actor=self.actor).delete(thread_id=thread_id, message_id=message_id)

        # Parse model
        model = ThreadMessageModel(external_model=response.json())

        return model
