from api_tests_framework.utils.unittest_wrappers import ModelValidationTestCase
from api_tests_framework.utils.errors import http_exceptions
from api_tests_framework.utils.helpers import generate_random_string

from api_tests_framework.src.actors import Actor

from api_tests_framework.src.actions.user import UserActions
from api_tests_framework.src.actions.thread import ThreadActions


class GetReceivedInvitationTestSuite(ModelValidationTestCase):
    def setUp(self):
        # Create actor1, actor2
        self.actor1, self.actor2 = Actor(), Actor()

        # actors sign up
        self.user_model1, self.user_model2 = (
            UserActions(actor=self.actor1).signup(),
            UserActions(actor=self.actor2).signup()
        )

        # actor1 creates threads
        self.thread_model = ThreadActions(actor=self.actor1).create_thread()

        # actor1 invites actor2 to threads
        self.thread_invitation_model = ThreadActions(actor=self.actor1).invite_users_to_thread(
            thread_id=self.thread_model.id,
            user_ids=[self.user_model2.id]
        )[0]

    def test_get_received_invitation_as_invitee(self):
        # actor2 gets received invitation
        thread_invitation_model = ThreadActions(actor=self.actor2).get_received_thread_invitation(
            invitation_id=self.thread_invitation_model.id
        )

        # Assert correct model has been returned
        self.assertThreadInvitationModel(thread_invitation_model)
        self.assertModelsAreEqual(thread_invitation_model, self.thread_invitation_model)

    def test_get_received_invitation_as_not_invitee(self):
        # Assert unable to get received invitation as not invitee
        with self.assertRaises(http_exceptions.NotFound):
            ThreadActions(actor=self.actor1).get_received_thread_invitation(
                invitation_id=self.thread_invitation_model.id
            )

    def test_get_non_existant_received_invitation(self):
        # Assert unable to get non existant invitation
        with self.assertRaises(http_exceptions.NotFound):
            ThreadActions(actor=self.actor2).get_received_thread_invitation(
                invitation_id=generate_random_string(5, 15)
            )

    def test_get_received_invitation_as_unauthorized_user(self):
        # Assert unable to get received invitation as unauthorized user
        with self.assertRaises(http_exceptions.Unauthorized):
            ThreadActions(actor=Actor()).get_received_thread_invitation(
                invitation_id=self.thread_invitation_model.id
            )
