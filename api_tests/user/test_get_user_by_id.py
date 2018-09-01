from api_tests_framework.utils.unittest_wrappers import ModelValidationTestCase
from api_tests_framework.utils.errors import http_exceptions

from api_tests_framework.src.actors import Actor

from api_tests_framework.src.actions.user import UserActions


class GetUserById(ModelValidationTestCase):
    def setUp(self):
        # Create actor
        self.actor = Actor()

        # Sign up
        self.signup_user_model = UserActions(actor=self.actor).signup()

    def test_get_user_by_id(self):
        # Create actor2
        actor2 = Actor()

        # actor2 signs up
        UserActions(actor=actor2).signup()

        # actor2 gets actor1 details by id
        user_model = UserActions(actor=actor2).get_user_by_id(user_id=self.signup_user_model.id)

        # Assert correct model has been returned
        self.assertUserModel(user_model)
        self.assertModelsAreEqual(model1=self.signup_user_model, model2=user_model, ignore_attributes=["updated_at"])

    def test_get_user_by_id_as_unauthorized_user(self):
        # Assert unable to get user by id as unauthorized user
        with self.assertRaises(http_exceptions.Unauthorized):
            UserActions(actor=Actor()).get_user_by_id(user_id=self.signup_user_model.id)
