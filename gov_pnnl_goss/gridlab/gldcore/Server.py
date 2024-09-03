import errno
import threading
import ctypes
import ctypes.util
import os

from gov_pnnl_goss.gridlab.gldcore.Output import output_verbose


def shutdown_now():
    output_verbose("server shutdown on exit in progress...")
    exec_setexitcode(XC_SVRKLL)
    shutdown_server = 1
    if sockfd != (SOCKET)0:
        # Checking the OS to use the correct function for shutdown
        if sys.platform == "_WIN32":
            shutdown(sockfd, SD_BOTH)
        else:
            shutdown(sockfd, SHUT_RDWR)
    sockfd = (SOCKET)0
    gui_wait_status(GUIACT_HALT)
    output_verbose("server shutdown on exit done")


def get_last_error():
    return errno


# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
def send_data(socket, buffer, length):
    try:
        return len(socket.send(buffer[:length]))
    except:
        return 0


def recv_data(s, buffer, len):
    return recv(s, buffer, len, 0) if _WIN32 else read(s, buffer, len)

def client_allowed(saddr):
    return saddr.startswith(global_client_allowed)


def status_server_join():
    result = ctypes.c_void_p()
    if threading.join(startup_thread, ctypes.byref(result)) == 0:
        return ctypes.cast(result, ctypes.POINTER(Status)).contents
    else:
        output_error("server thread join failed: %s", strerror(GetLastError()))
        return Status.FAILED

def http_create(s):
    http = HTTPCNX()
    http.s = s
    http.max_size = 65536
    http.buffer = bytearray(http.max_size)
    return http


def http_reset(http_cnx):
    http_cnx['status'] = None
    http_cnx['global_property_types'] = None

def http_status(http_cnx, status):
    http_cnx.status = status

def http_type(http_cnx, type):
    http_cnx.global_property_types = type


def http_send(http):
    header = ""
    len = 0
    len += len(header[len:])
    header += "HTTP/1.1 {}".format(http.status if http.status else "HTTP_INTERNALSERVERERROR")
    output_verbose("{} (len={}, mime={})".format(header, http.len, http.global_property_types if http.global_property_types else "none"))
    len += len(header[len:])
    header += "\nContent-Length: {}\n".format(http.len)
    if http.global_property_types and http.global_property_types[0] != '\0':
        len += len(header[len:])
        header += "Content-Type: {}\n".format(http.global_property_types)
    len += len(header[len:])
    header += "Cache-Control: no-cache\n"
    len += len(header[len:])
    header += "Cache-Control: no-store\n"
    len += len(header[len:])
    header += "Expires: -1\n"
    len += len(header[len:])
    header += "\n"
    send_data(http.s, header, len)
    if http.len > 0:
        send_data(http.s, http.buffer, http.len)
    http.len = 0

def http_close(http):
    if http.len > 0:
        http_send(http)
    if "_WIN32" in globals():
        closesocket(http.s)
    else:
        close(http.s)
    free(http.buffer)


def http_format(http, format, *args):
    libc = ctypes.CDLL(ctypes.util.find_library('c'))
    data = (ctypes.c_char * 65536)()
    len = libc.vsprintf(data, format, args)
    http_write(http, data, len)
    return len


def http_unquote(buffer):
    eob = buffer + len(buffer) - 1
    if buffer[0] == '"':
        buffer = buffer[1:]
    if eob[0] == '"':
        eob = eob[:0]
    return buffer


def hex_to_dec(c):
    if '0' <= c <= '9':
        return ord(c) - ord('0')
    elif 'A' <= c <= 'F':
        return ord(c) - ord('A') + 10
    elif 'a' <= c <= 'f':
        return ord(c) - ord('a') + 10
    else:
        return 0

def property(n, f, v):
    if use_tuple:
        http_format(http, f"\n\t{{\"{n}\": \"{f}\"}}, {v}")
    else:
        http_format(http, f" \"{n}\": \"{f}\", {v}")


def http_gui_request(http_cnx, uri):
    gui_set_html_stream(http_cnx, cast(GUISTREAMFN, http_format))
    if gui_html_output_page(uri) >= 0:
        http_type(http_cnx, "text/html")
        return 1
    else:
        return 0

def file_length(fd):
    fs = os.fstat(fd)
    if fs:
        return fs.st_size
    else:
        return -1

def http_copy(http, context, source, cook, pos):
    fp = open(source,"rb")
    if fp is None:
        print("unable to find %s output '%s': %s" % (context, source, os.strerror(os.errno)))
        return 0
    if pos >= 0:
        fp.seek(pos, os.SEEK_SET)
    else:
        pos = 0
    len = os.fstat(fp.fileno()).st_size - pos
    if len < 0:
        print("%s output '%s' not accessible" % (context, source))
        fp.close()
        return 0
    if len == 0:
        http.mime(source)
        http.write("")
        fp.close()
        return 1
    buffer = fp.read(len)
    if buffer is None:
        print("%s output buffer for '%s' not available" % (context, source))
        fp.close()
        return 0
    http.mime(source)
    old_cooked = http.cooked
    http.cooked = cook
    http.write(buffer)
    http.cooked = old_cooked
    fp.close()
    return 1

def http_output_request(http, uri):
    full_path = global_workdir
    if full_path[-1] != '/' or full_path[-1] != '\\':
        full_path += "/"
    full_path += uri
    return http_copy(http, "file", full_path, False, 0)

def http_get_rt(http, uri):
    full_path = [1024]
    file_name = [1024]
    pos = 0
    if not sscanf(uri, "%1023[^:]:%ld", file_name, pos) == 0:
        strncpy(file_name, uri, sizeof(file_name) - 1)
    if not find_file(file_name, None, R_OK, full_path, sizeof(full_path)):
        output_error("runtime file '%s' couldn't be located in GLPATH='%s'", file_name, getenv("GLPATH"))
        return 0
    return http_copy(http, "runtime", full_path, True, pos)

def http_get_rb(http_cnx, uri):
    full_path = [1024]
    if not find_file(uri, None, os.R_OK, full_path, len(full_path)):
        output_error("binary file '{}' couldn't be located in GLPATH='{}'".format(uri, os.getenv("GLPATH")))
        return 0
    return http_copy(http_cnx, "runtime", full_path, False, 0)


def http_action_request(http, action):
    if gui_post_action(action) == -1:
        http_status(http, "HTTP_ACCEPTED")
        http_type(http, "text/plain")
        http_format(http, "Goodbye")
        http_send(http)
        http_close(http)
        shutdown_now()
        return 1
    else:
        return 0


def http_open_request(http_cnx, action):
    if load_all(action):
        return 1
    else:
        return 0

def http_favicon(http):
    fullpath = bytearray(1024)
    if find_file("favicon.ico", None, os.R_OK, fullpath, len(fullpath)) is None:
        output_error("file 'favicon.ico' not found", fullpath.decode('utf-8'))
        return 0
    return http_copy(http, "icon", fullpath.decode('utf-8'), False, 0)
