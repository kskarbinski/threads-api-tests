from api_tests_framework.utils.unittest_wrappers import ModelValidationTestCase
from api_tests_framework.utils.errors import http_exceptions

from api_tests_framework.src.actors import Actor

from api_tests_framework.src.actions.user import UserActions


class GetUserTestSuite(ModelValidationTestCase):
    def setUp(self):
        # Create actors
        self.actors = [Actor() for _ in range(10)]

        # Actors sign up
        self.user_models = [UserActions(actor=actor).signup() for actor in self.actors]

    def test_get_users(self):
        # Get users
        user_models = UserActions(actor=self.actors[0]).get_users()

        # Assert all signed up actors are present and are correct models
        for user_model in user_models:
            self.assertUserModel(user_model)
        self.assertModelsInListOfModels(container=user_models, models=self.user_models)

    def test_get_users_as_unauthorized_user(self):
        with self.assertRaises(http_exceptions.Unauthorized):
            UserActions(actor=Actor()).get_users()
