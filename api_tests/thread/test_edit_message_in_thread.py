from api_tests_framework.utils.unittest_wrappers import ModelValidationTestCase
from api_tests_framework.utils.errors import http_exceptions
from api_tests_framework.utils.helpers import generate_random_words, generate_random_string

from api_tests_framework.src.actors import Actor

from api_tests_framework.src.actions.user import UserActions
from api_tests_framework.src.actions.thread import ThreadActions


class EditMessageInThreadTestSuite(ModelValidationTestCase):
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
        thread_application_model = ThreadActions(actor=self.actor2).apply_to_thread(thread_id=self.thread_model.id)

        # actor1 accepts thread application
        ThreadActions(actor=self.actor1).accept_or_reject_thread_application(
            thread_id=self.thread_model.id,
            application_id=thread_application_model.id,
            accept=True
        )

        # actor1 sends message in thread
        self.thread_message_model = ThreadActions(actor=self.actor1).send_message_in_thread(
            thread_id=self.thread_model.id,
        )

    def test_edit_thread_message_as_message_owner(self):
        # actor1 edits thread message
        message = generate_random_words(5, 15)
        thread_message_model = ThreadActions(actor=self.actor1).edit_thread_message(
            thread_id=self.thread_model.id,
            message_id=self.thread_message_model.id,
            message=message
        )

        # Assert correct model has been returned
        self.assertThreadMessageModel(thread_message_model)
        self.assertModelsAreEqual(
            model1=thread_message_model,
            model2=self.thread_message_model,
            ignore_attributes=["message", "updated_at"]
        )
        self.assertEqual(thread_message_model.message, message)

    def test_edit_thread_message_as_thread_member(self):
        # Assert unable to edit message even as thread member, but not message owner
        with self.assertRaises(http_exceptions.Forbidden):
            ThreadActions(actor=self.actor2).edit_thread_message(
                thread_id=self.thread_model.id,
                message_id=self.thread_message_model.id,
                message=generate_random_words(5, 15)
            )

    def test_edit_thread_message_as_not_thread_member(self):
        # Create additional actor and sign up
        actor3 = Actor()
        UserActions(actor=actor3).signup()

        # Assert unable to edit thread message as not thread member
        with self.assertRaises(http_exceptions.Forbidden):
            ThreadActions(actor=actor3).edit_thread_message(
                thread_id=self.thread_model.id,
                message_id=self.thread_message_model.id,
                message=generate_random_words(5, 15)
            )

    def test_edit_non_existant_thread_message(self):
        # Assert unable to edit non existant thread message
        with self.assertRaises(http_exceptions.NotFound):
            ThreadActions(actor=self.actor1).edit_thread_message(
                thread_id=self.thread_model.id,
                message_id=generate_random_string(5, 10),
                message=generate_random_words(5, 15)
            )

    def test_edit_thread_message_as_unauthorized_user(self):
        # Assert unable to edit thread message as unauthorized user
        with self.assertRaises(http_exceptions.Unauthorized):
            ThreadActions(actor=Actor()).edit_thread_message(
                thread_id=self.thread_model.id,
                message_id=self.thread_message_model.id,
                message=generate_random_string(5, 15)
            )
