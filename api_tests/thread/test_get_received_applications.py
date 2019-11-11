from api_tests_framework.utils.unittest_wrappers import ModelValidationTestCase
from api_tests_framework.utils.errors import http_exceptions

from api_tests_framework.src.actors import Actor

from api_tests_framework.src.actions.user import UserActions
from api_tests_framework.src.actions.thread import ThreadActions


class GetReceivedApplicationsTestSuite(ModelValidationTestCase):
    def setUp(self):
        # Create actor1, actor2, actor3 and actor4
        self.actor1, self.actor2, self.actor3, self.actor4 = [Actor() for _ in range(4)]

        # actors sign up
        self.user_model1, self.user_model2, self.user_model3, self.user_model4 = (
            UserActions(actor=self.actor1).signup(),
            UserActions(actor=self.actor2).signup(),
            UserActions(actor=self.actor3).signup(),
            UserActions(actor=self.actor4).signup()
        )

        # actor1 creates thread
        self.thread_model = ThreadActions(actor=self.actor1).create_thread()

        # actor2, actor3 and actor4 apply to thread
        self.thread_application_model2 = ThreadActions(
            actor=self.actor2).apply_to_thread(thread_id=self.thread_model.id)
        self.thread_application_model3 = ThreadActions(
            actor=self.actor3).apply_to_thread(thread_id=self.thread_model.id)
        self.thread_application_model4 = ThreadActions(
            actor=self.actor4).apply_to_thread(thread_id=self.thread_model.id)

    def test_get_received_applications_as_thread_owner(self):
        # actor1 gets received thread applications
        thread_application_models = ThreadActions(actor=self.actor1).get_received_thread_applications(
            thread_id=self.thread_model.id
        )

        # Assert correct models and amount of models has been received
        self.assertEqual(len(thread_application_models), 3)
        self.assertModelsInListOfModels(
            container=thread_application_models,
            models=[self.thread_application_model2, self.thread_application_model3, self.thread_application_model3]
        )

    def test_get_received_applications_as_not_thread_owner(self):
        # Assert unable to get thread applications as not thread owner
        with self.assertRaises(http_exceptions.Forbidden):
            ThreadActions(actor=self.actor4).get_received_thread_applications(thread_id=self.thread_model.id)

    def test_get_received_applications_as_unauthorized_user(self):
        # Assert unable to get invitations as unauthorized user
        with self.assertRaises(http_exceptions.Unauthorized):
            ThreadActions(actor=Actor()).get_received_thread_applications(thread_id=self.thread_model.id)
