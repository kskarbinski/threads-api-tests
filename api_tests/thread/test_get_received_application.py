from api_tests_framework.utils.unittest_wrappers import ModelValidationTestCase
from api_tests_framework.utils.errors import http_exceptions

from api_tests_framework.src.actors import Actor

from api_tests_framework.src.actions.user import UserActions
from api_tests_framework.src.actions.thread import ThreadActions


class GetReceivedApplicationTestSuite(ModelValidationTestCase):
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

        # actor2 applies to thread
        self.thread_application_model = ThreadActions(actor=self.actor2).apply_to_thread(
            thread_id=self.thread_model.id,
        )

    def test_get_received_thread_application_as_thread_owner(self):
        # actor1 gets received thread application
        thread_application_model = ThreadActions(actor=self.actor1).get_received_thread_application(
            thread_id=self.thread_model.id,
            application_id=self.thread_application_model.id
        )

        # Assert correct model has been returned
        self.assertThreadApplicationModel(thread_application_model)
        self.assertModelsAreEqual(
            model1=thread_application_model,
            model2=self.thread_application_model,
            ignore_attributes=["updated_at"]
        )

    def test_get_received_thread_application_as_not_thread_owner(self):
        # Assert unable to get received thread application as not thread owner
        with self.assertRaises(http_exceptions.Forbidden):
            ThreadActions(actor=self.actor2).get_received_thread_application(
                thread_id=self.thread_model.id,
                application_id=self.thread_application_model.id
            )

    def test_get_received_thread_application_as_unauthorized_user(self):
        # Assert unable to get received thread application as unauthorized user
        with self.assertRaises(http_exceptions.Unauthorized):
            ThreadActions(actor=Actor()).get_received_thread_application(
                thread_id=self.thread_model.id,
                application_id=self.thread_application_model.id
            )
