from api_tests_framework.src.handlers import BaseHandler
from api_tests_framework.utils.errors import MethodNotAllowed


class ThreadsIdHandler(BaseHandler):
    def get(self, thread_id):
        """
        Get thread by id
        {GET} /threads/id/<string:thread_id>

        :param unicode thread_id: Thread id

        :rtype: requests.Response
        """
        # Send request
        response = self._get(
            url="/threads/id/{thread_id}".format(thread_id=thread_id)
        )

        return response

    def post(self):
        raise MethodNotAllowed()

    def delete(self, thread_id):
        """
        Delete thread by id (only allowed for owner of thread)
        {DELETE} /threads/id/<string:thread_id>

        :param unicode thread_id: Thread id

        :rtype: requests.Response
        """
        # Send request
        response = self._delete(
            url="/threads/id/{thread_id}".format(thread_id=thread_id)
        )

        return response
