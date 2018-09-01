from api_tests_framework.utils.unittest_wrappers import ModelValidationTestCase
from api_tests_framework.utils.errors import http_exceptions

from api_tests_framework.src.actors import Actor

from api_tests_framework.src.actions.user import UserActions
from api_tests_framework.src.actions.thread import ThreadActions


class GetReceivedInvitationsTestSuite(ModelValidationTestCase):
    def setUp(self):
        # Create actor1, actor2
        self.actor1, self.actor2 = Actor(), Actor()

        # actors sign up
        self.user_model1, self.user_model2 = (
            UserActions(actor=self.actor1).signup(),
            UserActions(actor=self.actor2).signup()
        )

        # actor1 creates threads
        self.thread_model1, self.thread_model2, self.thread_model3 = (
            ThreadActions(actor=self.actor1).create_thread(),
            ThreadActions(actor=self.actor1).create_thread(),
            ThreadActions(actor=self.actor1).create_thread()
        )

        # actor1 invites actor2 to threads
        self.thread_invitation_models1 = ThreadActions(actor=self.actor1).invite_users_to_thread(
            thread_id=self.thread_model1.id,
            user_ids=[self.user_model2.id]
        )
        self.thread_invitation_models2 = ThreadActions(actor=self.actor1).invite_users_to_thread(
            thread_id=self.thread_model2.id,
            user_ids=[self.user_model2.id]
        )
        self.thread_invitation_models3 = ThreadActions(actor=self.actor1).invite_users_to_thread(
            thread_id=self.thread_model3.id,
            user_ids=[self.user_model2.id]
        )

    def test_get_received_invitations(self):
        # actor2 gets received invitations
        thread_invitation_models = ThreadActions(actor=self.actor2).get_received_thread_invitations()

        # Assert correct models have been returned
        for thread_invitation_model in thread_invitation_models:
            self.assertThreadInvitationModel(thread_invitation_model)
        self.assertModelsInListOfModels(
            container=thread_invitation_models,
            models=self.thread_invitation_models1 + self.thread_invitation_models2 + self.thread_invitation_models3
        )

    def test_get_received_invitations_as_unauthorized_user(self):
        # Assert unable to get received invitations as unauthorized user
        with self.assertRaises(http_exceptions.Unauthorized):
            ThreadActions(actor=Actor()).get_received_thread_invitations()
