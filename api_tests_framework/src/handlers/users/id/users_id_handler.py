from api_tests_framework.src.handlers import BaseHandler
from api_tests_framework.utils.errors import MethodNotAllowed


class UsersIdHandler(BaseHandler):
    def get(self, user_id):
        """
        Get user details by user id
        {GET} /users/id/<string:user_id>

        :param unicode user_id: User id

        :rtype: requests.Response
        """
        # Send request
        response = self._get(
            url="/users/id/{user_id}".format(user_id=user_id)
        )

        return response

    def post(self):
        raise MethodNotAllowed()

    def delete(self):
        raise MethodNotAllowed()
