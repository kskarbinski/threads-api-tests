from api_tests_framework.utils.unittest_wrappers import ModelValidationTestCase
from api_tests_framework.utils.errors import http_exceptions

from api_tests_framework.src.actors import Actor

from api_tests_framework.src.actions.user import UserActions
from api_tests_framework.src.actions.thread import ThreadActions

from api_tests_framework.src.handlers.threads import ThreadsHandler

from api_tests_framework.utils.helpers import generate_random_name, generate_random_string


class CreateThreadTestSuite(ModelValidationTestCase):
    def setUp(self):
        # Create actor
        self.actor = Actor()

        # actor signs up
        self.user_model = UserActions(actor=self.actor).signup()

    def test_create_thread(self):
        # actor creates a thread
        thread_name = generate_random_name()
        thread_model = ThreadActions(actor=self.actor).create_thread(name=thread_name)

        # Assert correct model has been returned
        self.assertThreadModel(thread_model)
        self.assertEqual(thread_model.name, thread_name)
        self.assertEqual(thread_model.owner, self.user_model.id)
        self.assertIn(self.user_model.id, thread_model.users)
        self.assertFalse(thread_model.private)
        self.assertFalse(thread_model.deleted)

    def test_create_private_thread(self):
        # actor creates a private thread
        thread_name = generate_random_name()
        thread_model = ThreadActions(actor=self.actor).create_thread(name=thread_name, private=True)

        # Assert correct model has been returned
        self.assertThreadModel(thread_model)
        self.assertEqual(thread_model.name, thread_name)
        self.assertEqual(thread_model.owner, self.user_model.id)
        self.assertIn(self.user_model.id, thread_model.users)
        self.assertTrue(thread_model.private)
        self.assertFalse(thread_model.deleted)

    def test_create_thread_exceeding_max_name(self):
        # Assert unable to create thread exceeding max name characters limit
        with self.assertRaises(http_exceptions.UnprocessableEntity):
            ThreadActions(actor=self.actor).create_thread(name=generate_random_string(51, 51))

    def test_create_thread_not_reaching_min_name(self):
        # Assert unable to create thread not reaching min name characters limit
        with self.assertRaises(http_exceptions.UnprocessableEntity):
            ThreadActions(actor=self.actor).create_thread(name=generate_random_string(1, 1))

    def test_create_thread_digits_as_name(self):
        # Assert unable to create thread with digits as name
        with self.assertRaises(http_exceptions.UnprocessableEntity):
            ThreadActions(actor=self.actor).create_thread(name="12345")

    def test_create_thread_no_name_param(self):
        # Assert unable to create thread without sending the name param
        with self.assertRaises(http_exceptions.BadRequest):
            ThreadsHandler(actor=self.actor).post(name=None, private=False)

    def test_create_thread_empty_name(self):
        # Assert unable to create a thread with empty name param
        with self.assertRaises(http_exceptions.UnprocessableEntity):
            ThreadActions(actor=self.actor).create_thread(name="")

    def test_create_thread_no_private_param(self):
        #  Assert unable to create thread without sending the private param
        with self.assertRaises(http_exceptions.BadRequest):
            ThreadsHandler(actor=self.actor).post(name=generate_random_string(10, 20), private=None)

    def test_create_thread_as_signed_out_user(self):
        # Assert unable to create thread as signed out user
        with self.assertRaises(http_exceptions.Unauthorized):
            ThreadActions(actor=Actor()).create_thread()
