from api_tests_framework.utils.unittest_wrappers import ModelValidationTestCase
from api_tests_framework.utils.errors import http_exceptions
from api_tests_framework.utils.helpers import generate_random_words, generate_random_string

from api_tests_framework.src.actors import Actor

from api_tests_framework.src.actions.user import UserActions
from api_tests_framework.src.actions.thread import ThreadActions


class SendMessageInThreadTestSuite(ModelValidationTestCase):
    def setUp(self):
        # Create actor1, actor2, actor3 and actor4
        self.actor1, self.actor2 = Actor(), Actor()

        # actors sign up
        self.user_model1, self.user_model2 = (
            UserActions(actor=self.actor1).signup(),
            UserActions(actor=self.actor2).signup()
        )

        # actor1 creates thread
        self.thread_model = ThreadActions(actor=self.actor1).create_thread()

        # actor2 applies to thread
        thread_application_model = ThreadActions(actor=self.actor2).apply_to_thread(thread_id=self.thread_model.id)

        # actor1 accepts thread applicatio
        ThreadActions(actor=self.actor1).accept_or_reject_thread_application(
            thread_id=self.thread_model.id,
            application_id=thread_application_model.id,
            accept=True
        )

    def test_send_message_in_thread_as_thread_member(self):
        # actor2 sends message in thread
        message = generate_random_words(5, 10)
        thread_message_model = ThreadActions(actor=self.actor2).send_message_in_thread(
            thread_id=self.thread_model.id,
            message=message
        )

        # Assert correct model has been received
        self.assertThreadMessageModel(thread_message_model)
        self.assertEqual(thread_message_model.user, self.user_model2.id)
        self.assertEqual(thread_message_model.thread, self.thread_model.id)
        self.assertEqual(thread_message_model.message, message)
        self.assertFalse(thread_message_model.deleted)

    def test_send_message_in_thread_as_not_thread_member(self):
        # Create actor3 and sign up
        actor3 = Actor()
        UserActions(actor=actor3).signup()

        # Assert unable to send message in thread while not being a member of the thread
        with self.assertRaises(http_exceptions.Forbidden):
            ThreadActions(actor=actor3).send_message_in_thread(thread_id=self.thread_model.id)

    def test_send_message_in_non_existant_thread(self):
        # Assert unable to send message in non existant thread
        with self.assertRaises(http_exceptions.NotFound):
            ThreadActions(actor=self.actor1).send_message_in_thread(thread_id=generate_random_string(5, 10))

    def test_send_message_in_thread_as_unauthorized_user(self):
        # Assert unable to send message in thread as unauthorized user
        with self.assertRaises(http_exceptions.Unauthorized):
            ThreadActions(actor=Actor()).send_message_in_thread(thread_id=self.thread_model.id)
