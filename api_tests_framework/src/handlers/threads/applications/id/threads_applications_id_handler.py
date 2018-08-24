from api_tests_framework.src.handlers import BaseHandler
from api_tests_framework.utils.errors import MethodNotAllowed


class ThreadsApplicationsIdHandler(BaseHandler):
    def get(self, application_id):
        """
        Get current user application by id
        {GET} /threads/applications/id/<string:application_id>

        :param unicode application_id: Application id

        :rtype: requests.Response
        """
        # Send request
        response = self._get(
            url="/threads/applications/id/{application_id}".format(application_id=application_id)
        )

        return response

    def post(self):
        raise MethodNotAllowed()

    def delete(self, application_id):
        """
        Delete current user application by id
        {DELETE} /threads/applications/id/<string:application_id>

        :param unicode application_id: Application id

        :rtype: requests.Response
        """
        # Send request
        response = self._delete(
            url="/threads/applications/id/{application_id}".format(application_id=application_id)
        )

        return response
