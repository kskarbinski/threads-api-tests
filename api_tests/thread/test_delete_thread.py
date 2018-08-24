from api_tests_framework.utils.unittest_wrappers import ModelValidationTestCase
from api_tests_framework.utils.errors import http_exceptions

from api_tests_framework.src.actors import Actor

from api_tests_framework.src.actions.user import UserActions
from api_tests_framework.src.actions.thread import ThreadActions


class DeleteThreadTestSuite(ModelValidationTestCase):
    def setUp(self):
        # Create actor
        self.actor = Actor()

        # actor signs up
        self.user_model = UserActions(actor=self.actor).signup()

        # actor creates thread
        self.thread_model = ThreadActions(actor=self.actor).create_thread()

    def test_delete_thread_as_owner(self):
        # actor deletes thread
        thread_model = ThreadActions(actor=self.actor).delete_thread(thread_id=self.thread_model.id)

        # Assert thread has been marked as deleted
        self.assertThreadModel(thread_model)
        self.assertModelsAreEqual(self.thread_model, thread_model, ignore_attributes=["deleted"])
        self.assertTrue(thread_model.deleted)

    def test_delete_thread_as_not_owner(self):
        # Create another actor and signup
        actor2 = Actor()
        UserActions(actor=actor2).signup()

        # Assert unable to delete thread as not owner
        with self.assertRaises(http_exceptions.Forbidden):
            ThreadActions(actor=actor2).delete_thread(thread_id=self.thread_model.id)

    def test_delete_thread_as_unauthorized_user(self):
        # Assert unable to delete thread as unauthorized user
        with self.assertRaises(http_exceptions.Unauthorized):
            ThreadActions(actor=Actor()).delete_thread(thread_id=self.thread_model.id)
