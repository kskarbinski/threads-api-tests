from api_tests_framework.utils.unittest_wrappers import ModelValidationTestCase
from api_tests_framework.utils.errors import http_exceptions

from api_tests_framework.src.actors import Actor

from api_tests_framework.src.actions.user import UserActions
from api_tests_framework.src.actions.thread import ThreadActions


class GetSentApplicationsTestSuite(ModelValidationTestCase):
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

        # actor2 applies to threads
        self.thread_application_model1 = ThreadActions(actor=self.actor2).apply_to_thread(
            thread_id=self.thread_model1.id
        )
        self.thread_application_model2 = ThreadActions(actor=self.actor2).apply_to_thread(
            thread_id=self.thread_model2.id
        )
        self.thread_application_model3 = ThreadActions(actor=self.actor2).apply_to_thread(
            thread_id=self.thread_model3.id
        )

    def test_get_sent_applications(self):
        # actor2 gets sent applications
        thread_application_models = ThreadActions(actor=self.actor2).get_sent_thread_applications()

        # Assert correct models have been returned
        for thread_application_model in thread_application_models:
            self.assertThreadApplicationModel(thread_application_model)
        self.assertModelsInListOfModels(
            container=thread_application_models,
            models=[self.thread_application_model1, self.thread_application_model2, self.thread_application_model3]
        )

    def test_get_sent_applications_as_unauthorized_user(self):
        # Assert unable to get sent applications as unauthorized user
        with self.assertRaises(http_exceptions.Unauthorized):
            ThreadActions(actor=Actor()).get_sent_thread_applications()
