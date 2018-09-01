from api_tests_framework.utils.unittest_wrappers import ModelValidationTestCase
from api_tests_framework.utils.errors import http_exceptions
from api_tests_framework.utils.helpers import generate_random_string

from api_tests_framework.src.actors import Actor

from api_tests_framework.src.actions.user import UserActions
from api_tests_framework.src.actions.thread import ThreadActions


class AcceptReceivedInvitationTestSuite(ModelValidationTestCase):
    def setUp(self):
        # Create actor1, actor2
        self.actor1, self.actor2 = Actor(), Actor()

        # actors sign up
        self.user_model1, self.user_model2 = (
            UserActions(actor=self.actor1).signup(),
            UserActions(actor=self.actor2).signup()
        )

        # actor1 creates thread
        self.thread_model1 = ThreadActions(actor=self.actor1).create_thread()

        # actor1 invites actor2 to thread
        self.thread_invitation_model = ThreadActions(actor=self.actor1).invite_users_to_thread(
            thread_id=self.thread_model1.id,
            user_ids=[self.user_model2.id]
        )[0]

    def test_accept_received_invitation_as_invitee(self):
        # actor2 accepts received invitation
        thread_invitation_model = ThreadActions(actor=self.actor2).accept_or_reject_thread_invitation(
            invitation_id=self.thread_invitation_model.id,
            accept=True
        )

        # Assert correct model has been returned
        self.assertThreadInvitationModel(thread_invitation_model)
        self.assertModelsAreEqual(thread_invitation_model, self.thread_invitation_model,
                                  ignore_attributes=["status", "updated_at", "users_in_thread"])
        self.assertEqual(thread_invitation_model.status, 2)
        self.assertIn(self.user_model2.id, thread_invitation_model.users_in_thread)

    def test_accept_received_invitation_as_not_invitee(self):
        # Assert unable to accept received invitation as not invitee
        with self.assertRaises(http_exceptions.NotFound):
            ThreadActions(actor=self.actor1).accept_or_reject_thread_invitation(
                invitation_id=self.thread_invitation_model.id,
                accept=True
            )

    def test_accept_non_existant_received_invitation(self):
        # Assert unable to accept non existant invitation
        with self.assertRaises(http_exceptions.NotFound):
            ThreadActions(actor=self.actor2).accept_or_reject_thread_invitation(
                invitation_id=generate_random_string(5, 15),
                accept=True
            )

    def test_accept_received_invitation_as_unauthorized_user(self):
        # Assert unable to accept received invitation as unauthorized user
        with self.assertRaises(http_exceptions.Unauthorized):
            ThreadActions(actor=Actor()).accept_or_reject_thread_invitation(
                invitation_id=self.thread_invitation_model.id,
                accept=True
            )
