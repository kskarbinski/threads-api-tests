from api_tests_framework.utils.unittest_wrappers import ModelValidationTestCase
from api_tests_framework.utils.errors import http_exceptions

from api_tests_framework.src.actors import Actor

from api_tests_framework.src.actions.user import UserActions


class GetUserTestSuite(ModelValidationTestCase):
    def setUp(self):
        # Create actor
        self.actor = Actor()

    def test_get_user(self):
        # Signup
        signup_user_model = UserActions(actor=self.actor).signup()

        # Get user details
        user_model = UserActions(actor=self.actor).get_user()

        # Assert correct UserModel has been returned
        self.assertUserModel(user_model)
        self.assertEqual(user_model.username, signup_user_model.username)
        self.assertEqual(user_model.lastname, signup_user_model.lastname)
        self.assertEqual(user_model.username, signup_user_model.username)

    def test_get_user_as_unauthorized_user(self):
        # Assert unable to get user details as unauthorized user
        with self.assertRaises(http_exceptions.Unauthorized):
            UserActions(actor=self.actor).get_user()
