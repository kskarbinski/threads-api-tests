from api_tests_framework.src.handlers import BaseHandler
from api_tests_framework.utils.errors import MethodNotAllowed


class UsersHandler(BaseHandler):
    def get(self):
        """
        Get last 100 users signed up
        {GET} /users

        :rtype: requests.Response
        """
        # Send request
        response = self._get(
            url="/users"
        )

        return response

    def post(self):
        raise MethodNotAllowed()

    def delete(self):
        raise MethodNotAllowed()
