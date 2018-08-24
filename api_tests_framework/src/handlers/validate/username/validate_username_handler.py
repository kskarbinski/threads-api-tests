from api_tests_framework.src.handlers import BaseHandler
from api_tests_framework.utils.errors import MethodNotAllowed


class ValidateUsernameHandler(BaseHandler):
    def get(self, username):
        """
        Validate username
        {GET} /validate/username

        :param unicode username: Username to be validated

        :rtype: requests.Response
        """
        # Create params
        params = {"username": username}

        # Send request
        response = self._get(
            url="/validate/username",
            params=params
        )

        return response

    def post(self):
        raise MethodNotAllowed()

    def delete(self):
        raise MethodNotAllowed()
