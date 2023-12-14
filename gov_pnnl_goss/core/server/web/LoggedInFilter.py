
# from javax.servlet import Filter, FilterConfig, ServletException, ServletRequest, ServletResponse, FilterChain
# from javax.servlet.http import HttpServletRequest, HttpServletResponse
# from java.io import IOException, PrintWriter
# from com.google.gson import Gson, JsonObject

import json
from io import BytesIO, BufferedReader

from gov_pnnl_goss.SpecialClasses import FilterConfig, HttpServletRequest, StringBuilder, InputStreamReader, \
    IOException, JsonObject, HttpServletResponse
from gov_pnnl_goss.core.server.web.Activator import Filter
from gov_pnnl_goss.core.server.web.MultiReadHttpServletRequestWrapper import MultiReadHttpServletRequestWrapper




class LoggedInFilter(Filter):

    def init(self, config: FilterConfig) -> None:
        print("Initializing filter with config: " + config)
        self.id_map = None

    def get_token_if_present(self, request: HttpServletRequest) -> str:
        token = request.getHeader("AuthToken")
        if token is None or token.isEmpty():
            if request.getMethod() == "POST":
                body = StringBuilder()
                char_buffer = [''] * 128
                try:
                    input_stream = request.getInputStream()
                    bytes_read = -1
                    reader = BufferedReader(InputStreamReader(input_stream))
                    while (bytes_read := reader.read(char_buffer)) > 0:
                        body.append(char_buffer, 0, bytes_read)
                except IOException as e1:
                    e1.printStackTrace()
                if not body.toString().isEmpty():
                    try:
                        json_obj = json.loads(body.toString(), JsonObject)
                        token = json_obj.get("AuthToken")
                        if token.isEmpty():
                            token = None
                    except Exception as e:
                        print(e)
        return token

    def do_filter(self, req, res, chain) -> None:
        http_req = HttpServletRequest(req)
        wrapper = MultiReadHttpServletRequestWrapper(http_req)
        auth_token = self.get_token_if_present(wrapper)
        ip = http_req.getRemoteAddr()
        identifier = None
        identifier_set = False

        if auth_token is not None:
            identifier = self.id_map.getIdentifier(ip, auth_token)
            if identifier is not None and not identifier.isEmpty():
                wrapper.setAttribute("identifier", identifier)
                identifier_set = True

        if not identifier_set:
            res.setStatus(HttpServletResponse.SC_UNAUTHORIZED)
            out = res.getWriter()
            out.write('{"error":"Invalid Authentication Token"}')
            out.close()
            return

        print("Identifier set: " + identifier)
        chain.do_filter(wrapper, res)

    def destroy(self) -> None:
        print("Destroying filter.")
