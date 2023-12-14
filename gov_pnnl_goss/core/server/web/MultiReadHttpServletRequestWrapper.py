
# from java.io import ByteArrayInputStream, ByteArrayOutputStream, IOException, InputStreamReader
# from javax.servlet import ReadListener, ServletInputStream, HttpServletRequest, HttpServletRequestWrapper
from io import BufferedReader

from gov_pnnl_goss.SpecialClasses import HttpServletRequestWrapper, ServletInputStream, ByteArrayOutputStream, IOUtils, \
    ByteArrayInputStream, ReadListener
from gov_pnnl_goss.core.server.web.LoggedInFilter import HttpServletRequest, InputStreamReader




class MultiReadHttpServletRequestWrapper(HttpServletRequestWrapper):

    def __init__(self, request: HttpServletRequest):
        super().__init__(request)
        self.cached_bytes = None

    def get_input_stream(self) -> ServletInputStream:
        if self.cached_bytes is None:
            self.cache_input_stream()
        return self.CachedServletInputStream()

    def get_reader(self) -> BufferedReader:
        return BufferedReader(InputStreamReader(self.get_input_stream()))

    def cache_input_stream(self):
        self.cached_bytes = ByteArrayOutputStream()
        IOUtils.copy(super().get_input_stream(), self.cached_bytes)

    class CachedServletInputStream(ServletInputStream):

        def __init__(self):
            self.input = ByteArrayInputStream(self.cached_bytes.to_byte_array())

        def read(self) -> int:
            return self.input.read()

        def is_finished(self) -> bool:
            return False

        def is_ready(self) -> bool:
            return False

        def set_read_listener(self, arg0: ReadListener):
            pass
