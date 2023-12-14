
# from javax.servlet.http import HttpServlet
# from javax.servlet import ServletException, HttpServletRequest, HttpServletResponse
# from org.springframework.stereotype import Component
# from org.springframework.context.annotation import Start, Stop
# from java.io import IOException
# from java.io import PrintWriter
from gov_pnnl_goss.SpecialClasses import HttpServlet


# @Component


class Default(HttpServlet):

    serial_version_UID = -543706852564073624

    # @Start
    def starting(self):
        print("Starting")

    def do_get(self, req, resp):
        super().do_get(req, resp)

    #@Stop
    def stopping(self):
        print("Stopping")
