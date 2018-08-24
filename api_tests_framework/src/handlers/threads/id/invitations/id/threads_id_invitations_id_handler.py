from api_tests_framework.src.handlers import BaseHandler
from api_tests_framework.utils.errors import MethodNotAllowed


class ThreadsIdInvitationsIdHandler(BaseHandler):
    def get(self, thread_id, invitation_id):
        """
        Get sent thread invitation (as invitation owner)
        {GET} /threads/id/<string:thread_id>/invitations/id/<string:invitation_id>

        :param unicode thread_id: Thread id
        :param unicode invitation_id: Invitation id

        :rtype: requests.Response
        """
        # Send request
        response = self._get(
            url="/threads/id/{thread_id}/invitations/id/{invitation_id}".format(
                thread_id=thread_id,
                invitation_id=invitation_id
            )
        )

        return response

    def post(self):
        raise MethodNotAllowed()

    def delete(self, thread_id, invitation_id):
        """
        Cancel sent thread invitation (as invitation owner)
        {DELETE} /threads/id/<string:thread_id>/invitations/id/<string:invitation_id>

        :param unicode thread_id: Thread id
        :param unicode invitation_id: Invitation id

        :rtype: requests.Response
        """
        # Send request
        response = self._delete(
            url="/threads/id/{thread_id}/invitations/id/{invitation_id}".format(
                thread_id=thread_id,
                invitation_id=invitation_id
            )
        )

        return response
