from api_tests_framework.src.handlers import BaseHandler
from api_tests_framework.utils.errors import MethodNotAllowed


class ThreadsIdApplicationsIdHandler(BaseHandler):
    def get(self, thread_id, application_id):
        """
        Get sent thread application (as thread owner)
        {GET} /threads/id/<string:thread_id>/applications/id/<string:application_id>

        :param unicode thread_id: Thread id
        :param unicode application_id: Application id

        :rtype: requests.Response
        """
        # Send request
        response = self._get(
            url="/threads/id/{thread_id}/applications/id/{application_id}".format(
                thread_id=thread_id,
                application_id=application_id
            )
        )

        return response

    def post(self, thread_id, application_id, accept):
        """
        Accept or reject received thread application (as thread owner)
        {POST} /threads/id/<string:thread_id>/applications/id/<string:application_id>

        :param unicode thread_id: Thread id
        :param unicode application_id: Application id
        :param bool accept: Whether to accept or reject the application

        :rtype: requests.Response
        """
        # Create payload
        json = {"accept": accept}

        # Send request
        response = self._post(
            url="/threads/id/{thread_id}/applications/id/{application_id}".format(
                thread_id=thread_id,
                application_id=application_id
            ),
            json=json
        )

        return response

    def delete(self):
        raise MethodNotAllowed()
