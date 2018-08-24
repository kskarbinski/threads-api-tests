from api_tests_framework.src.handlers import BaseHandler
from api_tests_framework.utils.errors import MethodNotAllowed


class ThreadsIdApplicationsHandler(BaseHandler):
    def get(self, thread_id):
        """
        Get received thread applications (as thread owner)
        {GET} /threads/id/<string:thread_id>/applications

        :param unicode thread_id: Thread id

        :rtype: requests.Response
        """
        # Send request
        response = self._get(
            url="/threads/id/{thread_id}/applications".format(thread_id=thread_id)
        )

        return response

    def post(self):
        raise MethodNotAllowed()

    def delete(self):
        raise MethodNotAllowed()
