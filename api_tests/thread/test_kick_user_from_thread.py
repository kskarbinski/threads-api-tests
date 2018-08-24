from api_tests_framework.utils.unittest_wrappers import ModelValidationTestCase
from api_tests_framework.utils.errors import http_exceptions

from api_tests_framework.src.actors import Actor

from api_tests_framework.src.actions.user import UserActions
from api_tests_framework.src.actions.thread import ThreadActions


class KickUserFromThreadTestSuite(ModelValidationTestCase):
    def setUp(self):
        # Create actor1, actor2 and actor3
        self.actor1, self.actor2, self.actor3 = Actor(), Actor(), Actor()

        # actors sign up
        self.user_model1, self.user_model2, self.user_model3 = (
            UserActions(actor=self.actor1).signup(),
            UserActions(actor=self.actor2).signup(),
            UserActions(actor=self.actor3).signup()
        )

        # actor1 creates thread
        self.thread_model = ThreadActions(actor=self.actor1).create_thread()

        # actor1 invites actor2 and actor3 to thread
        ThreadActions(
            actor=self.actor1
        ).invite_users_to_thread(
            thread_id=self.thread_model.id,
            user_ids=[self.user_model2.id, self.user_model3.id]
        )

        # actor2 and actor3 accept thread invitations
        actor2_invitation_model = ThreadActions(actor=self.actor2).get_received_thread_invitations()[0]
        actor3_invitation_model = ThreadActions(actor=self.actor3).get_received_thread_invitations()[0]
        ThreadActions(actor=self.actor2).accept_or_reject_thread_invitation(
            invitation_id=actor2_invitation_model.id,
            accept=True
        )
        ThreadActions(self.actor3).accept_or_reject_thread_invitation(
            invitation_id=actor3_invitation_model.id,
            accept=True
        )

    def test_kick_single_user_from_thread_as_thread_owner(self):
        # actor1 kicks actor2 from thread
        thread_model = ThreadActions(actor=self.actor1).kick_users_from_thread(
            thread_id=self.thread_model.id,
            user_ids=[self.user_model2.id]
        )

        # Assert user has been kicked
        self.assertNotIn(self.user_model2.id, thread_model.users)
        # Assert user has no access to thread
        with self.assertRaises(http_exceptions.Forbidden):
            ThreadActions(actor=self.actor2).send_message_in_thread(thread_id=self.thread_model.id)

    def test_kick_multiple_users_from_thread_as_thread_owner(self):
        # actor1 kicks actor2 and actor3 from thread
        thread_model = ThreadActions(actor=self.actor1).kick_users_from_thread(
            thread_id=self.thread_model.id,
            user_ids=[self.user_model2.id, self.user_model3.id]
        )

        # Assert users have been kicked
        self.assertNotIn(self.user_model2.id, thread_model.users)
        self.assertNotIn(self.user_model3.id, thread_model.users)
        # Assert users have no access to thread
        for actor in [self.actor2, self.actor3]:
            with self.assertRaises(http_exceptions.Forbidden):
                ThreadActions(actor=actor).send_message_in_thread(thread_id=self.thread_model.id)

    def test_kick_owner_from_thread_as_owner(self):
        # Assert unable to kick owner as owner
        with self.assertRaises(http_exceptions.UnprocessableEntity):
            ThreadActions(actor=self.actor1).kick_users_from_thread(
                thread_id=self.thread_model.id,
                user_ids=[self.user_model1.id]
            )

    def test_kick_user_from_thread_as_not_owner(self):
        # Assert unable to kick user as not thread owner
        with self.assertRaises(http_exceptions.Forbidden):
            ThreadActions(actor=self.actor2).kick_users_from_thread(
                thread_id=self.thread_model.id,
                user_ids=[self.user_model3.id]
            )

    def test_kick_user_from_thread_as_unauthorized_user(self):
        # Assert unable to kick user as unauthorized user
        with self.assertRaises(http_exceptions.Unauthorized):
            ThreadActions(actor=Actor()).kick_users_from_thread(
                thread_id=self.thread_model.id,
                user_ids=[self.user_model3.id]
            )
