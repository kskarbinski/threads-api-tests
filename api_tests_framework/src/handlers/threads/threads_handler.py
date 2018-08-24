from api_tests_framework.src.handlers import BaseHandler
from api_tests_framework.utils.errors import MethodNotAllowed


class ThreadsHandler(BaseHandler):
    def get(self):
        """
        Get last 100 threads created (which are not private and not deleted)
        {GET} /threads

        :rtype: requests.Response
        """
        # Send request
        response = self._get(
            url="/threads"
        )

        return response

    def post(self, name, private):
        """
        Create a new thread
        {POST} /threads

        :param unicode | None name: Thread name. Size must be between 2 and 50 characters.
        :param bool | None private: Whether the threat is private or not

        :rtype: requests.Response
        """
        # Create payload
        json = {
            "name": name,
            "private": private
        }

        # Send request
        response = self._post(
            url="/threads",
            json=json
        )

        return response

    def delete(self):
        raise MethodNotAllowed()
