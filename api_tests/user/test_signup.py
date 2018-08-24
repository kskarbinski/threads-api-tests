from api_tests_framework.utils.unittest_wrappers import ModelValidationTestCase
from api_tests_framework.utils.helpers import generate_random_string
from api_tests_framework.utils.errors import http_exceptions

from api_tests_framework.src.actors import Actor

from api_tests_framework.src.actions.user import UserActions

from api_tests_framework.src.handlers.signup import SignupHandler


class SignupTestSuite(ModelValidationTestCase):
    def setUp(self):
        # Create actor
        self.actor = Actor()

    def test_signup(self):
        # Signup
        user_model = UserActions(actor=self.actor).signup()

        # Assert correct UserModel has been returned
        self.assertUserModel(user_model)
        self.assertEqual(user_model.username, self.actor.username)
        self.assertEqual(user_model.lastname, self.actor.lastname)
        self.assertEqual(user_model.username, self.actor.username)

    def test_signup_empty_firstname(self):
        # Assert unable to signup with empty firstname
        with self.assertRaises(http_exceptions.UnprocessableEntity):
            UserActions(actor=self.actor).signup(
                firstname=""
            )

    def test_signup_empty_lastname(self):
        # Assert unable to signup with empty lastname
        with self.assertRaises(http_exceptions.UnprocessableEntity):
            UserActions(actor=self.actor).signup(
                lastname=""
            )

    def test_signup_empty_username(self):
        # Assert unable to signup with empty username
        with self.assertRaises(http_exceptions.UnprocessableEntity):
            UserActions(actor=self.actor).signup(
                username=""
            )

    def test_signup_empty_password(self):
        # Assert unable to signup with empty password
        with self.assertRaises(http_exceptions.UnprocessableEntity):
            UserActions(actor=self.actor).signup(
                password=""
            )

    def test_signup_no_firstname(self):
        # Assert unable to signup without sending firstname
        with self.assertRaises(http_exceptions.BadRequest):
            SignupHandler(actor=self.actor).post(
                firstname=None,
                lastname=self.actor.lastname,
                username=self.actor.username,
                password=self.actor.password
            )

    def test_signup_no_lastname(self):
        # Assert unable to signup without sending lastname
        with self.assertRaises(http_exceptions.BadRequest):
            SignupHandler(actor=self.actor).post(
                firstname=self.actor.firstname,
                lastname=None,
                username=self.actor.username,
                password=self.actor.password
            )

    def test_signup_no_username(self):
        # Assert unable to signup without sending username
        with self.assertRaises(http_exceptions.BadRequest):
            SignupHandler(actor=self.actor).post(
                firstname=self.actor.firstname,
                lastname=self.actor.lastname,
                username=None,
                password=self.actor.password
            )

    def test_signup_no_password(self):
        # Assert unable to signup without sending password
        with self.assertRaises(http_exceptions.BadRequest):
            SignupHandler(actor=self.actor).post(
                firstname=self.actor.firstname,
                lastname=self.actor.lastname,
                username=self.actor.username,
                password=None
            )

    def test_signup_as_already_existing_user(self):
        # Create actor2
        actor2 = Actor()

        # Signup
        UserActions(actor=self.actor).signup()

        # Assert unable to signup with already taken username
        with self.assertRaises(http_exceptions.Conflict):
            UserActions(actor=actor2).signup(
                username=self.actor.username
            )

    def test_signup_username_as_digits(self):
        # Assert unable to signup with username as digits
        with self.assertRaises(http_exceptions.UnprocessableEntity):
            UserActions(actor=self.actor).signup(
                username="123"
            )

    def test_signup_username_below_min_length(self):
        # Assert unable to signup with username below minimum length
        with self.assertRaises(http_exceptions.UnprocessableEntity):
            UserActions(actor=self.actor).signup(
                username=generate_random_string(1, 1)
            )

    def test_signup_username_over_max_length(self):
        # Assert unable to signup with username over maximum length
        with self.assertRaises(http_exceptions.UnprocessableEntity):
            UserActions(actor=self.actor).signup(
                username=generate_random_string(21, 21)
            )

    def test_signup_password_below_min_length(self):
        # Assert unable to signup with password below minimum length
        with self.assertRaises(http_exceptions.UnprocessableEntity):
            UserActions(actor=self.actor).signup(
                password=generate_random_string(3, 3)
            )

    def test_signup_password_over_max_length(self):
        # Assert unable to signup with password over maximum length
        with self.assertRaises(http_exceptions.UnprocessableEntity):
            UserActions(actor=self.actor).signup(
                password=generate_random_string(21, 21)
            )

    def test_signup_firstname_below_min_length(self):
        # Assert unable to signup with firstname below minimum length
        with self.assertRaises(http_exceptions.UnprocessableEntity):
            UserActions(actor=self.actor).signup(
                firstname=generate_random_string(1, 1)
            )

    def test_signup_firstname_over_max_length(self):
        # Assert unable to signup with firstname over maximum length
        with self.assertRaises(http_exceptions.UnprocessableEntity):
            UserActions(actor=self.actor).signup(
                firstname=generate_random_string(21, 21)
            )

    def test_signup_lastname_below_min_length(self):
        # Assert unable to signup with lastname below minimum length
        with self.assertRaises(http_exceptions.UnprocessableEntity):
            UserActions(actor=self.actor).signup(
                lastname=generate_random_string(1, 1)
            )

    def test_signup_lastname_over_max_length(self):
        # Assert unable to signup with lastname over maximum length
        with self.assertRaises(http_exceptions.UnprocessableEntity):
            UserActions(actor=self.actor).signup(
                lastname=generate_random_string(51, 51)
            )
