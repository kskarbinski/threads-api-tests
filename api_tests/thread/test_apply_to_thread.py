from api_tests_framework.utils.unittest_wrappers import ModelValidationTestCase
from api_tests_framework.utils.errors import http_exceptions
from api_tests_framework.utils.helpers import generate_random_string

from api_tests_framework.src.actors import Actor

from api_tests_framework.src.actions.user import UserActions
from api_tests_framework.src.actions.thread import ThreadActions


class ApplyToThreadTestSuite(ModelValidationTestCase):
    def setUp(self):
        # Create actor1 and actor2
        self.actor1, self.actor2 = Actor(), Actor()

        # actors sign up
        self.user_model1, self.user_model2 = (
            UserActions(actor=self.actor1).signup(),
            UserActions(actor=self.actor2).signup()
        )

        # actor1 creates thread
        self.thread_model = ThreadActions(actor=self.actor1).create_thread()

    def test_apply_to_thread(self):
        # actor2 applies to thread
        thread_application_model = ThreadActions(actor=self.actor2).apply_to_thread(thread_id=self.thread_model.id)

        # Assert correct model has been returned
        self.assertThreadApplicationModel(thread_application_model)
        self.assertEqual(thread_application_model.user, self.user_model2.id)
        self.assertEqual(thread_application_model.thread, self.thread_model.id)
        self.assertEqual(thread_application_model.status, 1)
        # Assert thread owner can see the application
        thread_application_models = ThreadActions(actor=self.actor1).get_received_thread_applications(
            thread_id=self.thread_model.id
        )
        self.assertModelsAreEqual(thread_application_model, thread_application_models[0])

    def test_apply_to_non_existant_thread(self):
        # Assert unable to apply to non existant thread
        with self.assertRaises(http_exceptions.NotFound):
            ThreadActions(actor=self.actor2).apply_to_thread(thread_id=generate_random_string(5, 10))

    def test_apply_to_thread_as_unauthorized_user(self):
        # Assert unable to apply as unauthorized user
        with self.assertRaises(http_exceptions.Unauthorized):
            ThreadActions(actor=Actor()).apply_to_thread(thread_id=self.thread_model.id)
