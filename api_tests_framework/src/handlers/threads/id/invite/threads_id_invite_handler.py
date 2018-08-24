from api_tests_framework.src.handlers import BaseHandler
from api_tests_framework.utils.errors import MethodNotAllowed


class ThreadsIdInviteHandler(BaseHandler):
    def get(self):
        raise MethodNotAllowed()

    def post(self, thread_id, user_ids):
        """
        Invite users to thread (as thread owner)
        {POST} /threads/id/<string:thread_id>/invite

        :param unicode thread_id: Thread id
        :param list user_ids: List of user ids to be invited

        :rtype: requests.Response
        """
        # Create payload
        json = {
            "users": user_ids
        }

        # Send request
        response = self._post(
            url="/threads/id/{thread_id}/invite".format(thread_id=thread_id),
            json=json
        )

        return response

    def delete(self):
        raise MethodNotAllowed()
