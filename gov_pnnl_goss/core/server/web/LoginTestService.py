
# from javax.servlet.http import HttpServletRequest
# from javax.ws.rs import Consumes, POST, Path, Produces
# from javax.ws.rs.core import Context, MediaType, Response, Status
import json

from gov_pnnl_goss.SpecialClasses import Status
from gov_pnnl_goss.core.Response import Response


# @Path("/api")


class LoginTestService:
    def __init__(self):
        self.request = None

    # @POST
    # @Path("/echo")
    # @Consumes([MediaType.APPLICATION_JSON, MediaType.TEXT_XML])
    # @Produces(MediaType.APPLICATION_JSON)
    def run_test(self, body):
        body_obj = None
        obj = {}

        try:
            body_obj = json.loads(body)
            obj['data'] = body_obj
        except Exception as ex:
            obj['data'] = "Non JSON: " + body

        obj['Status'] = "Success"

        return Response.status(Status.OK).entity(json.dumps(obj)).build()

    # @POST
    # @Path("/loginTest")
    # @Consumes([MediaType.APPLICATION_JSON, MediaType.TEXT_XML])
    # @Produces(MediaType.APPLICATION_JSON)
    def authenticate(self):
        return "{\"status\": \"Success\"}"
