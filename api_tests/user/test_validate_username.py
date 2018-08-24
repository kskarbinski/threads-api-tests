from api_tests_framework.utils.unittest_wrappers import ModelValidationTestCase
from api_tests_framework.utils.errors import http_exceptions
from api_tests_framework.utils.helpers import generate_random_string

from api_tests_framework.src.actors import Actor

from api_tests_framework.src.actions.user import UserActions


class ValidateUsernameTestSuite(ModelValidationTestCase):
    def setUp(self):
        # Create actors
        self.actor = Actor()

    def test_validate_username(self):
        # Validate correct username
        username_validation_model = UserActions(
            actor=self.actor
        ).validate_username(username=generate_random_string(2, 20))

        # Assert correct model has been returned and no validation errors
        self.assertUsernameValidationModel(username_validation_model)
        self.assertFalse(username_validation_model.errors)

    def test_validate_empty_username(self):
        # Validate empty username
        username_validation_model = UserActions(actor=self.actor).validate_username(username="")

        # Assert empty username raises error
        self.assertTrue(len(username_validation_model.errors), 1)
        self.assertIn("Username length must be between 2 and 20 characters", username_validation_model.errors)

    def test_validate_no_username(self):
        # Assert unable to send no username
        with self.assertRaises(http_exceptions.BadRequest):
            UserActions(actor=self.actor).validate_username(username=None)

    def test_validate_already_taken_username(self):
        # Create another actor and sign up
        actor2 = Actor()
        UserActions(actor=actor2).signup()

        # Validate already taken username
        username_validation_model = UserActions(actor=self.actor).validate_username(username=actor2.username)

        # Assert already taken username raises error
        self.assertTrue(len(username_validation_model.errors), 1)
        self.assertIn("Username already taken", username_validation_model.errors)

    def test_validate_too_short_username(self):
        # Validate too short username
        username_validation_model = UserActions(
            actor=self.actor
        ).validate_username(username=generate_random_string(1, 1))

        # Assert too short username raises error
        self.assertTrue(len(username_validation_model.errors), 1)
        self.assertIn("Username length must be between 2 and 20 characters", username_validation_model.errors)

    def test_validate_too_long_username(self):
        # Validate too long username
        username_validation_model = UserActions(
            actor=self.actor
        ).validate_username(username=generate_random_string(21, 30))

        # Assert too long username raises error
        self.assertTrue(len(username_validation_model.errors), 1)
        self.assertIn("Username length must be between 2 and 20 characters", username_validation_model.errors)

    def test_validate_number_username(self):
        # Validate number username
        username_validation_model = UserActions(
            actor=self.actor
        ).validate_username(username="123456")

        # Assert number username raises error
        self.assertTrue(len(username_validation_model.errors), 1)
        self.assertIn("Username must not be a number", username_validation_model.errors)
