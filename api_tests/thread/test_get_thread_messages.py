from api_tests_framework.utils.unittest_wrappers import ModelValidationTestCase
from api_tests_framework.utils.errors import http_exceptions
from api_tests_framework.utils.helpers import generate_random_string

from api_tests_framework.src.actors import Actor

from api_tests_framework.src.actions.user import UserActions
from api_tests_framework.src.actions.thread import ThreadActions


class GetThreadMessagesTestSuite(ModelValidationTestCase):
    def setUp(self):
        # Create actor1, actor2, actor3 and actor4
        self.actor1, self.actor2, self.actor3, self.actor4 = [Actor() for _ in xrange(4)]

        # actors sign up
        self.user_model1, self.user_model2, self.user_model3, self.user_model4 = (
            UserActions(actor=self.actor1).signup(),
            UserActions(actor=self.actor2).signup(),
            UserActions(actor=self.actor3).signup(),
            UserActions(actor=self.actor4).signup()
        )

        # actor1 creates thread
        self.thread_model = ThreadActions(actor=self.actor1).create_thread()

        # actor2, actor3 and actor4 apply to thread to thread
        thread_application_models = [
            ThreadActions(actor=actor).apply_to_thread(thread_id=self.thread_model.id)
            for actor in [self.actor2, self.actor3, self.actor4]
        ]

        # actor1 accepts thread applications
        for thread_application_model in thread_application_models:
            ThreadActions(actor=self.actor1).accept_or_reject_thread_application(
                thread_id=self.thread_model.id,
                application_id=thread_application_model.id,
                accept=True
            )

        # actors send messages in thread
        self.thread_message_model1 = ThreadActions(actor=self.actor1).send_message_in_thread(
            thread_id=self.thread_model.id)
        self.thread_message_model2 = ThreadActions(actor=self.actor2).send_message_in_thread(
            thread_id=self.thread_model.id)
        self.thread_message_model3 = ThreadActions(actor=self.actor3).send_message_in_thread(
            thread_id=self.thread_model.id)
        self.thread_message_model4 = ThreadActions(actor=self.actor4).send_message_in_thread(
            thread_id=self.thread_model.id)

    def test_get_thread_messages_as_member_of_thread(self):
        # actor4 gets thread messages
        thread_message_models = ThreadActions(actor=self.actor4).get_thread_messages(thread_id=self.thread_model.id)

        # Assert correct models and amount of models has been returned
        self.assertEqual(len(thread_message_models), 4)
        for thread_message_model in thread_message_models:
            self.assertThreadMessageModel(thread_message_model)
        self.assertModelsInListOfModels(
            container=thread_message_models,
            models=[self.thread_message_model1, self.thread_message_model2,
                    self.thread_message_model3, self.thread_message_model4]
        )

    def test_get_thread_messages_as_not_member_of_thread(self):
        # Create another actor and signup
        actor5 = Actor()
        UserActions(actor=actor5).signup()

        # Assert unable to get thread messages as not member of thread
        with self.assertRaises(http_exceptions.Forbidden):
            ThreadActions(actor=actor5).get_thread_messages(thread_id=self.thread_model.id)

    def test_get_thread_messages_of_non_existant_thread(self):
        # Assert unable to get non existant thread messages
        with self.assertRaises(http_exceptions.NotFound):
            ThreadActions(actor=self.actor1).get_thread_messages(thread_id=generate_random_string(10, 10))

    def test_get_thread_messages_as_unauthorized_user(self):
        # Assert unable to get thread messages as unauthorized user
        with self.assertRaises(http_exceptions.Unauthorized):
            ThreadActions(actor=Actor()).get_thread_messages(thread_id=self.thread_model.id)
