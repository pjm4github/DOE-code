import os
import re
import sys
import threading
import urllib

import requests

from gov_pnnl_goss.gridlab.gldcore.Output import output_message, output_warning, output_verbose
from gov_pnnl_goss.gridlab.gldcore.Version import version_copyright, version_patch, version_build, version_major, version_minor
from gridlab.gldcore.Find import Find
from gridlab.gldcore.Globals import SUCCESS

check_version_thread_id = None
global_suppress_repeat_messages = True


# branch names and histories (named after WECC 500kV busses)
# 	Allston			Version 1.0 originated at PNNL March 2007, released February 2008
# 	Buckley			Version 1.1 originated at PNNL January 2008, released April 2008
# 	Coulee			Version 1.2 originated at PNNL April 2008, released June 2008
# 	Coyote			Version 1.3 originated at PNNL June 2008, not released
# 	Diablo			Version 2.0 originated at PNNL August 2008
# 	Eldorado		Version 2.1 originated at PNNL September 2009
# 	Four Corners	Version 2.2 originated at PNNL November 2010
# 	Grizzly			Version 2.3 originated at PNNL November 2011
# 	Hassayampa		Version 3.0 originated at PNNL November 2011
# 	Hatwai			Version 3.1 originated at PNNL 2013
# 	Jojoba			Version 3.2 originated at PNNL 2014
# 	Keeler			Version 4.0 originated at PNNL 2017
# 	Lugo			Version 4.1 originated at PNNL 2018
# 	McNary			Version 4.2 originated at PNNL 2019
# 	Navajo			Version 4.3 originated at PNNL 2020
# 	Ostrander		Version 5.0 originated at PNNL 2022
# 	Palo Verde      Version 5.1 originated at PNNL 2023
# 	Perkins         Version 5.2 originated at PNNL 2023
# 	Redhawk
# 	Sacajawea
# 	Tesla
# 	Troutdale
# 	Vantage
# 	Vincent
# 	Westwing
# 	Yavapai
# 	(continue with 345kV WECC busses on WECC after this)


def legal_notice():
    global global_suppress_repeat_messages, global_version_major, global_version_minor, global_version_copyright, \
        global_version_patch, global_version_build, global_version_branch, global_platform
    suppress = global_suppress_repeat_messages
    global_suppress_repeat_messages = False
    copyright = f"GridLAB-D {version_copyright()}"
    copyright = copyright.replace('\n', ' ')

    # Assuming find_file function to check the file existence
    path = "path/to/search"  # Define the path to search
    if not Find.find_file(copyright, path=path):
        debug_mode = "DEBUG" if sys.flags.debug else "RELEASE"
        bitness = 8 * sys.getsizeof(None)  # Equivalent to 8*sizeof(void*)
        output_message(
            f"GridLAB-D {global_version_major}.{global_version_minor}.{global_version_patch}-{global_version_build} "
            f"({global_version_branch}) {bitness}-bit {global_platform} {debug_mode}\n{copyright}")

    global_suppress_repeat_messages = suppress
    return True  # conditions of use have been met

def legal_license():
    global global_suppress_repeat_messages
    suppress = global_suppress_repeat_messages
    global_suppress_repeat_messages = 0
    try:
        license_text = (
            f"{version_copyright()}\n"
            "1. Battelle Memorial Institute (hereinafter Battelle) hereby grants\n"
            "   permission to any person or entity lawfully obtaining a copy of\n"
            "   this software and associated documentation files (hereinafter 'the\n"
            "   Software') to redistribute and use the Software in source and\n"
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
            "   'AS IS' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT\n"
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
            "\n"
        )
        output_message(license_text)
    finally:
        global_suppress_repeat_messages = suppress

    return True  # Assuming SUCCESS is represented by True


def check_version(mt):
    global check_version_thread_id
    if mt == 0 or threading.Thread(target=check_version_proc, args=(None,)).start() != 0:
        check_version_proc(None)


CV_NOINFO  = 0x0001
CV_BADURL  = 0x0002
CV_NODATA  = 0x0004
CV_NEWVER  = 0x0008
CV_NEWPATCH = 0x0010
CV_NEWBUILD = 0x0020


def check_version_proc(ptr):
    patch, build = 0, 0
    url = "https://raw.githubusercontent.com/gridlab-d/gridlab-d/master/gldcore/versions.txt"

    result = requests.get(url)
    rc = 0
    mypatch = version_patch()
    mybuild = version_build()
    if result is None or len(result.content) == 0:
        pass
    if result.status_code > 0 and result.status_code < 400:
        pass
    target = "%d.%d:".format(version_major(), version_minor())
    pv = result.text[result.text.find(target):]
    if pv == None:
        pass

    match = re.match(r"\d+\.\d+:(\d+):(\d+)", pv)
    if not match:
        output_warning("check_version: '%s' entry for version %d.%d is bad", url, version_major(), version_minor())
        rc = CV_NODATA
    else:
        patch, build = match.groups()
        patch = int(patch)
        build = int(build)
        nv = pv.find('\n')
        if nv is not None:
            pass
        if mypatch < patch:
            pass
        if mybuild > 0 and mybuild < build:
            pass
        if rc == 0:
            output_verbose("this version is current")

    return rc


# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
def legal_notice_status():
    global global_suppress_repeat_messages, global_debug_mode
    DEBUG = global_debug_mode
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
    if Find.find_file(version, None, os.R_OK, path, len(path)) == None:
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
