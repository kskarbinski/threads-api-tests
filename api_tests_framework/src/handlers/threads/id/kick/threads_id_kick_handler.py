from api_tests_framework.src.handlers import BaseHandler
from api_tests_framework.utils.errors import MethodNotAllowed


class ThreadsIdKickHandler(BaseHandler):
    def get(self):
        raise MethodNotAllowed()

    def post(self, thread_id, user_ids):
        """
        Kick users from thread (as thread owner)
        {POST} /threads/id/<string:thread_id>/kick

        :param unicode thread_id: Thread id
        :param list user_ids: List of user ids to be kicked

        :rtype: requests.Response
        """
        # Create payload
        json = {
            "users": user_ids
        }

        # Send request
        response = self._post(
            url="/threads/id/{thread_id}/kick".format(thread_id=thread_id),
            json=json
        )

        return response

    def delete(self):
        raise MethodNotAllowed()
