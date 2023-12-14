import time
import urllib.request

from gov_pnnl_goss.gridlab.gldcore.Output import output_debug

import os
import requests
import errno


class HttpClient:

    def __init__(self):
        pass

    # HTTP request function
    def http_read(self, url, maxlen=0):
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()  # Check for HTTP errors

            # Initialize the result structure
            result = {
                "body": response.content,
                "header": response.headers,
                "status": response.status_code,
            }

            return result

        except requests.exceptions.RequestException as e:
            print(f"Error while making an HTTP request: {e}")
            return None

    # Save HTTP response body to a file
    def http_saveas(self, url, file_path):
        result = self.http_read(url)

        if result is None:
            return False

        try:
            with open(file_path, "wb") as file:
                file.write(result["body"])
            return True

        except OSError as e:
            if e.errno == errno.ENOENT:
                print(f"Error: Directory not found for {file_path}")
            else:
                print(f"Error while writing to {file_path}: {e}")
            return False

# Main function
def main():
    url = "http://example.com"  # Replace with your URL
    file_path = "output.html"  # Replace with your desired file path
    h = HttpClient()
    if h.http_saveas(url, file_path):
        print(f"Saved content from {url} to {file_path} successfully.")
    else:
        print(f"Failed to save content from {url} to {file_path}.")

if __name__ == "__main__":
    main()
#
#
#
#
# class HttpClient:
#     @staticmethod
#     def h_open(url, maxlen):
#         pass
#
#     @staticmethod
#     def h_close(http):
#         pass
#
#     @staticmethod
#     def h_file_length(http):
#         pass
#
#     @staticmethod
#     def h_eof(http):
#         pass
#
#     @staticmethod
#     def h_read(buffer, size, http):
#         pass
#
#     @staticmethod
#     def http_new_result():
#         pass
#
#     @staticmethod
#     def http_delete_result(result_in):
#         pass
#
#     @staticmethod
#     def http_read(url, maxlen):
#         pass
#
#     @staticmethod
#     def http_get_header_data(result, param):
#         pass
#
#     @staticmethod
#     def http_get_status(result):
#         pass
#
#     @staticmethod
#     def http_read_datetime(timestamp):
#         pass
#
#     @staticmethod
#     def http_save_as(url, file):
#         pass
#
#     @staticmethod
#     def http_get_options():
#         pass
#
#
# def hclose(http):
#     if http:
#         if http.sd:
#             # close socket for Windows and other systems
#             http.sd.close()
#         if http.buf:
#             del http.buf
#         del http
#     return 1
#
# def hfile_length(http):
#     return http.len
#
# def heof(http):
#     return http['pos'] >= http['len']
#
# def read_http(buffer, size, http):
#     len = http.len - http.pos
#     if http.pos >= http.len:
#         return 0
#     if len > size:
#         len = size
#     buffer[:len] = http.buf[http.pos : http.pos + len]
#     http.pos += len
#     return len
#
# class HttpResult:
#     def __init__(self):
#         self.body = {"data": None, "size": 0}
#         self.header = {"data": None, "size": 0}
#         self.status = 0
#
# def http_new_result():
#     result = HttpResult()
#     return result
#
# def http_delete_result(result_in):
#     result = result_in.contents
#     if result.body.size > 0:
#         del result.body.data
#     if result.header.size > 0:
#         del result.header.data
#     del result
#
# def http_get_status(result):
#     output_debug("http_get_status(): '%s'", result.header.data + 9)
#     return int(result.header.data + 9)
#
#
# def http_read_datetime(timestamp):
#     dt = time.struct_time
#     month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
#     tzone = ""
#
#     if timestamp is None:
#         return 0
#
#     parsed_values = timestamp.split(" ")
#     if len(parsed_values) != 6:
#         print("http_read_datetime(timestamp='{}'): unable to parse string".format(timestamp))
#         return 0
#
#     dt.tm_mday = int(parsed_values[1])
#     month_abbr = parsed_values[2]
#     dt.tm_year = int(parsed_values[3]) - 1900
#     dt.tm_hour = int(parsed_values[4].split(":")[0])
#     dt.tm_min = int(parsed_values[4].split(":")[1])
#     dt.tm_sec = int(parsed_values[4].split(":")[2])
#     tzone = parsed_values[5]
#
#     try:
#         dt.tm_mon = month.index(month_abbr)
#     except ValueError:
#         print("http_read_datetime(timestamp='{}'): month not recognized".format(timestamp))
#         return 0
#     else:
#         return time.mktime(dt)
