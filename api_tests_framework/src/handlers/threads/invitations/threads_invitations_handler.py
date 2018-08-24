from api_tests_framework.src.handlers import BaseHandler
from api_tests_framework.utils.errors import MethodNotAllowed


class ThreadsInvitationsHandler(BaseHandler):
    def get(self):
        """
        Get last 100 received thread invitations as current user
        {GET} /threads/invitations

        :rtype: requests.Response
        """
        # Send request
        response = self._get(
            url="/threads/invitations"
        )

        return response

    def post(self, name, private):
        raise MethodNotAllowed()

    def delete(self):
        raise MethodNotAllowed()
