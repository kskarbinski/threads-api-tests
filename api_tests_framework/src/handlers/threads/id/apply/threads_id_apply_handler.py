from api_tests_framework.src.handlers import BaseHandler
from api_tests_framework.utils.errors import MethodNotAllowed


class ThreadsIdApplyHandler(BaseHandler):
    def get(self):
        raise MethodNotAllowed()

    def post(self, thread_id):
        """
        Apply to join a thread
        {POST} /threads/id/<string:thread_id>/apply

        :param unicode thread_id: Thread id

        :rtype: requests.Response
        """
        # Send request
        response = self._post(
            url="/threads/id/{thread_id}/apply".format(thread_id=thread_id)
        )

        return response

    def delete(self):
        raise MethodNotAllowed()
