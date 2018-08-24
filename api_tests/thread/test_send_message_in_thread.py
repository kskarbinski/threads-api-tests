from api_tests_framework.utils.unittest_wrappers import ModelValidationTestCase
from api_tests_framework.utils.errors import http_exceptions

from api_tests_framework.src.actors import Actor

from api_tests_framework.src.actions.user import UserActions
from api_tests_framework.src.actions.thread import ThreadActions


class SendMessageInThreadTestSuite(ModelValidationTestCase):
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

    def test_send_message_in_thread_as_thread_member(self):
        pass

    def test_send_message_in_thread_as_not_thread_member(self):
        pass

    def test_send_message_in_non_existant_thread(self):
        pass

    def test_send_message_in_thread_as_unauthorized_user(self):
        pass
