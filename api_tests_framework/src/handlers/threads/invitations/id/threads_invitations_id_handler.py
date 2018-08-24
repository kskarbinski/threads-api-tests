from api_tests_framework.src.handlers import BaseHandler
from api_tests_framework.utils.errors import MethodNotAllowed


class ThreadsInvitationsIdHandler(BaseHandler):
    def get(self, invitation_id):
        """
        Get current user invitation by id
        {GET} /threads/invitations/id/<string:invitation_id>

        :param unicode invitation_id: Invitation id

        :rtype: requests.Response
        """
        # Send request
        response = self._get(
            url="/threads/invitations/id/{invitation_id}".format(invitation_id=invitation_id)
        )

        return response

    def post(self, invitation_id, accept):
        """
        Accept or decline invitation by id
        {POST} /threads/invitations/id/<string:invitation_id>

        :param unicode invitation_id: Invitation id
        :param bool accept: True or False, whether the invitation is accepted or not

        :rtype: requests.Response
        """
        # Create payload
        json = {"accept": accept}

        # Send request
        response = self._post(
            url="/threads/invitations/id/{invitation_id}".format(invitation_id=invitation_id),
            json=json
        )

        return response

    def delete(self):
        raise MethodNotAllowed()
