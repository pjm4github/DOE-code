
# import javax.servlet.Filter
# import javax.servlet.FilterChain
# import javax.servlet.FilterConfig
# import javax.servlet.ServletException
# import javax.servlet.ServletRequest
# import javax.servlet.ServletResponse
# import javax.servlet.http.HttpServletRequest
# import javax.servlet.http.HttpServletResponse
# import java.io.IOException
from gov_pnnl_goss.core.server.web.Activator import Filter
from gov_pnnl_goss.core.server.web.LoggedInFilter import HttpServletResponse, HttpServletRequest


class XDomainFilter(Filter):

    def destroy(self):
        pass

    def doFilter(self, req, resp, chain):
        response = HttpServletResponse(resp)
        request = HttpServletRequest(req)

        response.setHeader("Access-Control-Allow-Origin", "*")
        response.setHeader("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept,AuthToken")
        response.setHeader("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")

        if request.getMethod().equalsIgnoreCase("options"):
            response.setStatus(200)
            return

        chain.doFilter(req, resp)

    def init(self, config):
        pass
