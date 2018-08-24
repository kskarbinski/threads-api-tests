from api_tests_framework.src.actions import BaseActions
from api_tests_framework.src.handlers.signup import SignupHandler
from api_tests_framework.src.handlers.user import UserHandler
from api_tests_framework.src.handlers.users import UsersHandler
from api_tests_framework.src.handlers.validate.username import ValidateUsernameHandler
from api_tests_framework.src.handlers.users.id import UsersIdHandler
from api_tests_framework.src.handlers.users.username import UsersUsernameHandler

from api_tests_framework.src.models import UserModel, ValidateUsernameModel


class UserActions(BaseActions):
    def signup(self, username=None, password=None, firstname=None, lastname=None):
        # Send request
        response = SignupHandler(actor=self.actor).post(
            username=self.actor.username if username is None else username,
            password=self.actor.password if password is None else password,
            firstname=self.actor.firstname if firstname is None else firstname,
            lastname=self.actor.lastname if lastname is None else lastname
        )

        # Parse model
        model = UserModel(external_model=response.json())

        return model

    def get_user(self):
        # Send request
        response = UserHandler(actor=self.actor).get()

        # Parse model
        model = UserModel(external_model=response.json())

        return model

    def get_users(self):
        # Send request
        response = UsersHandler(actor=self.actor).get()

        # Parse models
        models = [UserModel(external_model=external_model) for external_model in response.json()["users"]]

        return models

    def validate_username(self, username):
        # Send request
        response = ValidateUsernameHandler(actor=self.actor).get(username=username)

        # Parse model
        model = ValidateUsernameModel(external_model=response.json())

        return model

    def get_user_by_id(self, user_id):
        # Send request
        response = UsersIdHandler(actor=self.actor).get(user_id=user_id)

        # Parse model
        model = UserModel(external_model=response.json())
        
        return model

    def get_user_by_username(self, username):
        # Send request
        response = UsersUsernameHandler(actor=self.actor).get(username=username)

        # Parse model
        model = UserModel(external_model=response.json())

        return model
