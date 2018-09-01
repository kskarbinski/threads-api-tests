from api_tests_framework.utils.unittest_wrappers import ModelValidationTestCase
from api_tests_framework.utils.errors import http_exceptions

from api_tests_framework.src.actors import Actor

from api_tests_framework.src.actions.user import UserActions
from api_tests_framework.src.actions.thread import ThreadActions


class GetThreadTestSuite(ModelValidationTestCase):
    def setUp(self):
        # Create actor
        self.actor = Actor()

        # actor signs up
        self.user_model = UserActions(actor=self.actor).signup()

        # actor creates thread
        self.thread_model = ThreadActions(actor=self.actor).create_thread()

    def test_get_thread(self):
        # actor gets thread by id
        thread_model = ThreadActions(actor=self.actor).get_thread(thread_id=self.thread_model.id)

        self.assertThreadModel(thread_model)
        self.assertModelsAreEqual(self.thread_model, thread_model, ignore_attributes=["updated_at"])

    def test_get_threads_as_unauthorized_user(self):
        # Assert unable to get thread by id as unauthorized user
        with self.assertRaises(http_exceptions.Unauthorized):
            ThreadActions(actor=Actor()).get_thread(thread_id=self.thread_model.id)
