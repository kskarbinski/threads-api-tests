from api_tests_framework.utils.unittest_wrappers import ModelValidationTestCase
from api_tests_framework.utils.errors import http_exceptions

from api_tests_framework.src.actors import Actor

from api_tests_framework.src.actions.user import UserActions
from api_tests_framework.src.actions.thread import ThreadActions


class InviteUserToThreadTestSuite(ModelValidationTestCase):
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

    def test_invite_single_user_to_thread(self):
        # actor1 invites actor2
        thread_invitation_models = ThreadActions(
            actor=self.actor1
        ).invite_users_to_thread(
            thread_id=self.thread_model.id,
            user_ids=[self.user_model2.id]
        )

        # Assert correct model has been returned
        self.assertEqual(len(thread_invitation_models), 1)
        self.assertThreadInvitationModel(thread_invitation_models[0])
        self.assertEqual(thread_invitation_models[0].user, self.user_model2.id)
        self.assertEqual(thread_invitation_models[0].thread, self.thread_model.id)
        self.assertEqual(thread_invitation_models[0].status, 1)
        self.assertEqual(thread_invitation_models[0].invited_by, self.user_model1.id)
        self.assertEqual(thread_invitation_models[0].users_in_thread, [self.user_model1.id])
        # Assert actor2 got invited
        user2_thread_invitation_model = ThreadActions(actor=self.actor2).get_received_thread_invitations()
        self.assertModelsAreEqual(thread_invitation_models[0], user2_thread_invitation_model[0],
                                  ignore_attributes=["updated_at"])

    def test_invite_multiple_users_to_thread(self):
        # actor1 invites actor2
        thread_invitation_models = ThreadActions(
            actor=self.actor1
        ).invite_users_to_thread(
            thread_id=self.thread_model.id,
            user_ids=[self.user_model2.id, self.user_model3.id]
        )

        # Assert correct models have been returned
        self.assertEqual(len(thread_invitation_models), 2)
        for thread_invitation_model in thread_invitation_models:
            self.assertThreadInvitationModel(thread_invitation_model)
            self.assertIn(thread_invitation_model.user, [self.user_model2.id, self.user_model3.id])
            self.assertEqual(thread_invitation_model.thread, self.thread_model.id)
            self.assertEqual(thread_invitation_model.status, 1)
            self.assertEqual(thread_invitation_model.invited_by, self.user_model1.id)
            self.assertEqual(thread_invitation_model.users_in_thread, [self.user_model1.id])
        # Assert actor2 and actor3 got invited
        for actor in [self.actor2, self.actor3]:
            obtained_thread_invitation_model = ThreadActions(actor=actor).get_received_thread_invitations()[0]
            self.assertModelInListOfModels(obtained_thread_invitation_model, thread_invitation_models)

    def test_invite_user_to_thread_as_not_thread_owner(self):
        # Assert unable to invite user to thread as not thread owner
        with self.assertRaises(http_exceptions.Forbidden):
            ThreadActions(actor=self.actor2).invite_users_to_thread(
                thread_id=self.thread_model.id,
                user_ids=[self.user_model3.id]
            )

    def test_invite_already_invited_user_to_thread(self):
        # actor1 invites actor2
        ThreadActions(actor=self.actor1).invite_users_to_thread(
            thread_id=self.thread_model.id,
            user_ids=[self.user_model2.id]
        )
        # Assert unable to invite already invited user
        with self.assertRaises(http_exceptions.Conflict):
            ThreadActions(actor=self.actor1).invite_users_to_thread(
                thread_id=self.thread_model.id,
                user_ids=[self.user_model2.id]
            )

    def test_invite_user_to_thread_as_unauthorized_user(self):
        # Assert unable to invite to thread as unauthorized user
        with self.assertRaises(http_exceptions.Unauthorized):
            ThreadActions(actor=Actor()).invite_users_to_thread(
                thread_id=self.thread_model.id,
                user_ids=[self.user_model2.id]
            )
