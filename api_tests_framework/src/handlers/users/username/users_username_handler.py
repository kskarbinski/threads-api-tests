from api_tests_framework.src.handlers import BaseHandler
from api_tests_framework.utils.errors import MethodNotAllowed


class UsersUsernameHandler(BaseHandler):
    def get(self, username):
        """
        Get user details by username
        {GET} /users/username/<string:username>

        :param unicode username: Username of the user to get details of

        :rtype: requests.Response
        """
        # Send request
        response = self._get(
            url="/users/username/{username}".format(username=username)
        )

        return response

    def post(self):
        raise MethodNotAllowed()

    def delete(self):
        raise MethodNotAllowed()
