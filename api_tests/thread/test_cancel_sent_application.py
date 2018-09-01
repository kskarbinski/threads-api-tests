from api_tests_framework.utils.unittest_wrappers import ModelValidationTestCase
from api_tests_framework.utils.errors import http_exceptions
from api_tests_framework.utils.helpers import generate_random_string

from api_tests_framework.src.actors import Actor

from api_tests_framework.src.actions.user import UserActions
from api_tests_framework.src.actions.thread import ThreadActions


class CancelSentApplicationTestSuite(ModelValidationTestCase):
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
            thread_id=self.thread_model.id
        )

    def test_cancel_sent_application_as_application_owner(self):
        # actor2 cancels application
        thread_application_model = ThreadActions(actor=self.actor2).cancel_sent_thread_application(
            application_id=self.thread_application_model.id
        )

        # Assert correct model has been returned
        self.assertThreadApplicationModel(thread_application_model)
        self.assertModelsAreEqual(thread_application_model, self.thread_application_model,
                                  ignore_attributes=["updated_at", "status"])
        self.assertEqual(thread_application_model.status, 4)

    def test_cancel_sent_application_as_not_application_owner(self):
        # Assert unable to cancel sent application as not application owner
        with self.assertRaises(http_exceptions.NotFound):
            ThreadActions(actor=self.actor1).cancel_sent_thread_application(
                application_id=self.thread_application_model.id
            )

    def test_cancel_non_existant_sent_application(self):
        # Assert unable to cancel non existant sent application
        with self.assertRaises(http_exceptions.NotFound):
            ThreadActions(actor=self.actor2).cancel_sent_thread_application(
                application_id=generate_random_string(5, 15)
            )

    def test_cancel_sent_application_as_unauthorized_user(self):
        # Assert unable to cancel sent application as unauthorized user
        with self.assertRaises(http_exceptions.Unauthorized):
            ThreadActions(actor=Actor()).cancel_sent_thread_application(
                application_id=self.thread_application_model.id
            )
