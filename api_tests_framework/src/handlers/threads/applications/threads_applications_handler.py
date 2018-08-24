from api_tests_framework.src.handlers import BaseHandler
from api_tests_framework.utils.errors import MethodNotAllowed


class ThreadsApplicationsHandler(BaseHandler):
    def get(self):
        """
        Get last 100 sent thread applications as current user
        {GET} /threads/applications

        :rtype: requests.Response
        """
        # Send request
        response = self._get(
            url="/threads/applications"
        )

        return response

    def post(self, name, private):
        raise MethodNotAllowed()

    def delete(self):
        raise MethodNotAllowed()
