from api_tests_framework.src.handlers import BaseHandler
from api_tests_framework.utils.errors import MethodNotAllowed


class UserHandler(BaseHandler):
    def get(self):
        """
        Get current user details
        {GET} /user

        :rtype: requests.Response
        """
        # Send request
        response = self._get(
            url="/user"
        )

        return response

    def post(self):
        raise MethodNotAllowed()

    def delete(self):
        raise MethodNotAllowed()
