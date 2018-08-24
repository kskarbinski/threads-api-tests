from api_tests_framework.utils.unittest_wrappers import ModelValidationTestCase
from api_tests_framework.utils.errors import http_exceptions

from api_tests_framework.src.actors import Actor

from api_tests_framework.src.actions.user import UserActions
from api_tests_framework.src.actions.thread import ThreadActions


class GetSentInvitationsTestSuite(ModelValidationTestCase):
    def setUp(self):
        # Create actor1, actor2, actor3 and actor4
        self.actor1, self.actor2, self.actor3, self.actor4 = [Actor() for _ in xrange(4)]

        # actors sign up
        self.user_model1, self.user_model2, self.user_model3, self.user_model4 = (
            UserActions(actor=self.actor1).signup(),
            UserActions(actor=self.actor2).signup(),
            UserActions(actor=self.actor3).signup(),
            UserActions(actor=self.actor4).signup()
        )

        # actor1 creates thread
        self.thread_model = ThreadActions(actor=self.actor1).create_thread()

        # actor1 invites actor2, actor3, actor4 to thread
        self.thread_invitation_models = ThreadActions(actor=self.actor1).invite_users_to_thread(
            thread_id=self.thread_model.id,
            user_ids=[self.user_model2.id, self.user_model3.id, self.user_model4.id]
        )

    def test_get_sent_invitations_as_thread_owner(self):
        # actor2 gets sent invitations
        thread_invitation_models = ThreadActions(actor=self.actor1).get_sent_thread_invitations(
            thread_id=self.thread_model.id
        )

        # Assert each invitation is a proper model and the amount of models obtained is correct
        self.assertEqual(len(thread_invitation_models), 3)
        for thread_invitation_model in thread_invitation_models:
            self.assertThreadInvitationModel(thread_invitation_model)
        self.assertModelsInListOfModels(thread_invitation_models, self.thread_invitation_models)

    def test_get_sent_invitations_as_not_thread_owner(self):
        # Assert unable to get invitations as not thread owner
        with self.assertRaises(http_exceptions.Forbidden):
            ThreadActions(actor=self.actor4).get_sent_thread_invitations(thread_id=self.thread_model.id)

    def test_get_sent_invitations_as_unauthorized_user(self):
        # Assert unable to get invitations as unauthorized user
        with self.assertRaises(http_exceptions.Unauthorized):
            ThreadActions(actor=Actor()).get_sent_thread_invitations(thread_id=self.thread_model.id)
