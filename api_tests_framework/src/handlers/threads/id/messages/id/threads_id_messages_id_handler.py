from api_tests_framework.src.handlers import BaseHandler
from api_tests_framework.utils.errors import MethodNotAllowed


class ThreadsIdMessagesIdHandler(BaseHandler):
    def get(self, thread_id, message_id):
        """
        Get thread message by id
        {GET} /threads/id/<string:thread_id>/messages/id/<string:message_id>

        :param unicode thread_id: Thread id
        :param unicode message_id: Message id

        :rtype: requests.Response
        """
        # Send request
        response = self._get(
            url="/threads/id/{thread_id}/messages/id/{message_id}".format(
                thread_id=thread_id,
                message_id=message_id
            )
        )

        return response

    def post(self, thread_id, message_id, message):
        """
        Edit thread message (as message owner)
        {POST} /threads/id/<string:thread_id>/messages/id/<string:message_id>

        :param unicode thread_id: Thread id
        :param unicode message_id: Message id
        :param unicode message: Message to be sent

        :rtype: requests.Response
        """
        # Create payload
        json = {
            "message": message
        }

        # Send request
        response = self._post(
            url="/threads/id/{thread_id}/messages/id/{message_id}".format(
                thread_id=thread_id,
                message_id=message_id
            ),
            json=json
        )

        return response

    def delete(self, thread_id, message_id):
        """
        Delete thread message (as message owner)

        :param unicode thread_id: Thread id
        :param unicode message_id: Message id

        :rtype: requests.Response
        """
        # Send request
        response = self._delete(
            url="/threads/id/{thread_id}/messages/id/{message_id}".format(
                thread_id=thread_id,
                message_id=message_id
            )
        )

        return response
