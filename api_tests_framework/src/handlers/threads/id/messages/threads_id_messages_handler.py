from api_tests_framework.src.handlers import BaseHandler
from api_tests_framework.utils.errors import MethodNotAllowed


class ThreadsIdMessagesHandler(BaseHandler):
    def get(self, thread_id):
        """
        Get thread messages
        {GET} /threads/id/<string:thread_id>/messages

        :param unicode thread_id: Thread id

        :rtype: requests.Response
        """
        # Send request
        response = self._get(
            url="/threads/id/{thread_id}/messages".format(thread_id=thread_id)
        )

        return response

    def post(self, thread_id, message):
        """
        Send a message in thread
        {POST} /threads/id/<string:thread_id>/messages

        :param unicode thread_id: Thread id
        :param unicode message: Message to be sent

        :rtype: requests.Response
        """
        # Create payload
        json = {
            "message": message
        }

        # Send request
        response = self._post(
            url="/threads/id/{thread_id}/messages".format(thread_id=thread_id),
            json=json
        )

        return response

    def delete(self):
        raise MethodNotAllowed()
