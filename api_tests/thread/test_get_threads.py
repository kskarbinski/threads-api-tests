from api_tests_framework.utils.unittest_wrappers import ModelValidationTestCase
from api_tests_framework.utils.errors import http_exceptions

from api_tests_framework.src.actors import Actor

from api_tests_framework.src.actions.user import UserActions
from api_tests_framework.src.actions.thread import ThreadActions


class GetThreadsTestSuite(ModelValidationTestCase):
    def setUp(self):
        # Create actor
        self.actor = Actor()

        # actor signs up
        self.user_model = UserActions(actor=self.actor).signup()

        # actor creates threads
        self.thread_models = [ThreadActions(actor=self.actor).create_thread() for _ in range(10)]
        self.private_thread_models = [ThreadActions(actor=self.actor).create_thread(private=True) for _ in range(3)]

    def test_get_threads(self):
        # Create actor2 and signup
        actor2 = Actor()
        UserActions(actor=actor2).signup()

        # actor2 gets threads
        thread_models = ThreadActions(actor=actor2).get_threads()

        # Assert threads have the correct model and all created threads are present
        for thread_model in thread_models:
            self.assertThreadModel(thread_model)
        self.assertModelsInListOfModels(container=thread_models, models=self.thread_models)
        self.assertModelsNotInListOfModels(container=thread_models, models=self.private_thread_models)

    def test_get_threads_as_unauthorized_user(self):
        # Assert unable to get threads as unauthorized user
        with self.assertRaises(http_exceptions.Unauthorized):
            ThreadActions(actor=Actor()).get_threads()
