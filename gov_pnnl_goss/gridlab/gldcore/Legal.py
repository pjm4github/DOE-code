
import threading

from gov_pnnl_goss.gridlab.gldcore.Output import output_message
from gov_pnnl_goss.gridlab.gldcore.Version import version_copyright

check_version_thread_id = None
global_suppress_repeat_messages = True

class Status:
    def legal_notice(self):
        pass

    def legal_license(self):
        pass


def check_version(mt):
    global check_version_thread_id
    if mt == 0 or threading.Thread(target=check_version_proc, args=(None,)).start() != 0:
        check_version_proc(None)


def check_version_proc(ptr):
    patch, build = 0, 0
    url = "https:"
    result = cast(HTTPRESULT, http_read(url, 0x1000))
    target = [32]
    pv, nv = None, None
    rc = 0
    mypatch = version_patch()
    mybuild = version_build()
    if result == None or result.body.size == 0:
        pass
    if result.status > 0 and result.status < 400:
        pass
    sprintf(target, "%d.%d:", version_major(), version_minor())
    pv = strstr(result.body.data, target)
    if pv == None:
        pass
    if sscanf(pv, "%*d.%*d:%d:%d", patch, build) != 2:
        output_warning("check_version: '%s' entry for version %d.%d is bad", url, version_major(), version_minor())
        rc = CV_NODATA

    else:
        nv = strchr(pv, '\n')
        if nv != None:
            pass
        if mypatch < patch:
            pass
        if mybuild > 0 and mybuild < build:
            pass
        if rc == 0:
            output_verbose("this version is current")

    http_delete_result(result)
    return rc


# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
def legal_notice_status():
    global global_suppress_repeat_messages
    copyright = bytearray(1024)
    end = None
    suppress = global_suppress_repeat_messages
    path = bytearray(1024)
    global_suppress_repeat_messages = False
    version = "GridLAB-D " + version_copyright()
    end = version.find('\n')
    while end != -1:
        version = version.replace('\n', ' ', 1)
        end = version.find('\n')
    if find_file(version, None, R_OK, path, len(path)) == None:
        output_message("GridLAB-D %d.%d.%d-%d (%s) %d-bit %s %s\n%s" % (
            global_version_major, global_version_minor, global_version_patch, global_version_build, 
            global_version_branch, 0, global_platform,
            "DEBUG" if DEBUG else "RELEASE",
            version
        ))
    global_suppress_repeat_messages = suppress
    return SUCCESS


# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
def legal_license():
    global global_suppress_repeat_messages
    surpress = global_suppress_repeat_messages
    global_suppress_repeat_messages = False
    output_message(
        "{}\n"
        "1. Battelle Memorial Institute (hereinafter Battelle) hereby grants\n"
        "   permission to any person or entity lawfully obtaining a copy of\n"
        "   this software and associated documentation files (hereinafter \"the\n"
        "   Software\") to redistribute and use the Software in source and\n"
        "   binary forms, with or without modification.  Such person or entity\n"
        "   may use, copy, modify, merge, publish, distribute, sublicense,\n"
        "   and/or sell copies of the Software, and may permit others to do so,\n"
        "   subject to the following conditions:\n"
        "   - Redistributions of source code must retain the above copyright\n"
        "     notice, this list of conditions and the following disclaimers.\n"
        "   - Redistributions in binary form must reproduce the above copyright\n"
        "     notice, this list of conditions and the following disclaimer in\n"
        "     the documentation and/or other materials provided with the\n"
        "     distribution.\n"
        "   - Other than as used herein, neither the name Battelle Memorial\n"
        "     Institute or Battelle may be used in any form whatsoever without\n"
        "     the express written consent of Battelle.\n"
        "2. THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS\n"
        "   \"AS IS\" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT\n"
        "   LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR\n"
        "   A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL BATTELLE OR\n"
        "   CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,\n"
        "   EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,\n"
        "   PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR\n"
        "   PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY\n"
        "   OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING\n"
        "   NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS\n"
        "   SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.\n"
        "3. The Software was produced by Battelle under Contract No.\n"
        "   DE-AC05-76RL01830 with the Department of Energy.  The U.S. Government\n"
        "   is granted for itself and others acting on its behalf a nonexclusive,\n"
        "   paid-up, irrevocable worldwide license in this data to reproduce,\n"
        "   prepare derivative works, distribute copies to the public, perform\n"
        "   publicly and display publicly, and to permit others to do so.  The\n"
        "   specific term of the license can be identified by inquiry made to\n"
        "   Battelle or DOE.  Neither the United States nor the United States\n"
        "   Department of Energy, nor any of their employees, makes any warranty,\n"
        "   express or implied, or assumes any legal liability or responsibility\n"
        "   for the accuracy, completeness or usefulness of any data, apparatus,\n"
        "   product or process disclosed, or represents that its use would not\n"
        "   infringe privately owned rights.\n"
        "\n".format(version_copyright())
    )
    global_suppress_repeat_messages = surpress
    return SUCCESS
