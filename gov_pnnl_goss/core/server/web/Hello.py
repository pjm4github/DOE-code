import io
from msilib.schema import Component

from gov_pnnl_goss.core.server.web.Default import HttpServlet


class Hello(HttpServlet):

    def do_get(self, req, resp):
        writer = resp.getWriter()
        writer.write("Hello World")

    def starting(self):
        print("Starting servlet")

    def stopping(self):
        print("Stopping servlet")
