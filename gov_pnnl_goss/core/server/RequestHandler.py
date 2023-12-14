
from gov_pnnl_goss.core.Request import Request
from gov_pnnl_goss.core.Response import Response
from gov_pnnl_goss.core.security.AuthorizationHandler import RequestHandlerInterface


class RequestHandler(RequestHandlerInterface):
    def get_handles(self):
        """
        /**
        * Explicitly provide a map from request to authorization handler.
        *
        * @return
        */
        :return:
        """
        pass

    def handle(self, request: Request) -> Response:
        """
        /**
        * Handle a request of a specific type of service.
        *
        * @param request
        */
        :param request:
        :return:
        """
        pass
