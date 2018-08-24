from api_tests_framework.src.handlers import BaseHandler
from api_tests_framework.utils.errors import MethodNotAllowed


class SignupHandler(BaseHandler):
    def get(self):
        raise MethodNotAllowed()

    def post(self, username, password, firstname, lastname):
        """
        Sign up a new user
        {POST} /signup

        :param unicode | None username: Username
        :param unicode | None password: Password
        :param unicode | None firstname: First name
        :param unicode | None lastname: Last name

        :rtype: requests.Response
        """
        # Create payload
        json = {
            "username": username,
            "password": password,
            "firstname": firstname,
            "lastname": lastname
        }
        # Send request
        response = self._post(
            url="/signup",
            json=json
        )

        return response

    def delete(self):
        raise MethodNotAllowed()
