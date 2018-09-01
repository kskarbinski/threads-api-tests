from api_tests_framework.utils.unittest_wrappers import ModelValidationTestCase
from api_tests_framework.utils.errors import http_exceptions

from api_tests_framework.src.actors import Actor

from api_tests_framework.src.actions.user import UserActions
from api_tests_framework.src.actions.thread import ThreadActions


class CancelSentInvitationTestSuite(ModelValidationTestCase):
    def setUp(self):
        # Create actor1, actor2
        self.actor1, self.actor2 = Actor(), Actor()

        # actors sign up
        self.user_model1, self.user_model2 = (
            UserActions(actor=self.actor1).signup(),
            UserActions(actor=self.actor2).signup()
        )

        # actor1 creates thread
        self.thread_model = ThreadActions(actor=self.actor1).create_thread()

        # actor1 invites actor2 to thread
        self.thread_invitation_models = ThreadActions(actor=self.actor1).invite_users_to_thread(
            thread_id=self.thread_model.id,
            user_ids=[self.user_model2.id]
        )

    def test_cancel_sent_invitation_as_invitation_owner(self):
        # actor1 cancels sent invitation
        thread_invitation_model = ThreadActions(actor=self.actor1).cancel_sent_thread_invitation(
            thread_id=self.thread_model.id,
            invitation_id=self.thread_invitation_models[0].id
        )

        # Assert proper model has been returned and the invitation is cancelled
        self.assertThreadInvitationModel(thread_invitation_model)
        self.assertModelsAreEqual(
            model1=thread_invitation_model,
            model2=self.thread_invitation_models[0],
            ignore_attributes=["status", "updated_at"]
        )
        self.assertEqual(thread_invitation_model.status, 4)

    def test_cancel_sent_invitation_as_not_invitation_owner(self):
        # Assert unable to cancel sent invitation as not invitation owner
        with self.assertRaises(http_exceptions.Forbidden):
            ThreadActions(actor=self.actor2).cancel_sent_thread_invitation(
                thread_id=self.thread_model.id,
                invitation_id=self.thread_invitation_models[0].id
            )

    def test_cancel_sent_invitation_as_unauthorized_user(self):
        # Assert unable to cancel sent invitation as unauthorized user
        with self.assertRaises(http_exceptions.Unauthorized):
            ThreadActions(actor=Actor()).cancel_sent_thread_invitation(
                thread_id=self.thread_model.id,
                invitation_id=self.thread_invitation_models[0].id
            )
