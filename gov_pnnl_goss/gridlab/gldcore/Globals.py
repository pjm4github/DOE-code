# Static variables
import copy
import math
import threading
import random
import time
import re
import sys
import os
from enum import Enum



# from gov_pnnl_goss.gridlab.gldcore.Class import DynamicClass
from gov_pnnl_goss.gridlab.gldcore.Version import version_major, version_minor, version_patch, version_build, \
    version_branch, Version
# from gridlab.gldcore.Exec import CheckpointType
from gov_pnnl_goss.gridlab.gldcore.PropertyHeader import PropertyType, PropertyAccess, Keyword
##################################################
# PROPERTIES



TS_NEVER = -1
TS_INVALID = -1
TS_ZERO = 0
TS_MAX = math.inf
MIN_YEAR = 1970
MAX_YEAR = 2969

PI = 3.1415926535897932384626433832795
E = 2.71828182845905
NM_PREUPDATE = 0
NM_POSTUPDATE = 1
NM_RESET = 2
OF_NONE = 0
OF_HASPLC = 1
OF_LOCKED = 2
OF_RECALC = 8
OF_FOREIGN = 16
OF_SKIPSAFE = 32
OF_RERANK = 16384

random_init = random.seed

# Constants
# See the TimeStamp module
# DT_INFINITY = math.inf
# DT_INVALID = -1
# DT_SECOND = 1.0
EINVAL = 22  # Invalid argument

HOMEVAR = "HOMEVAR"
PATHSEP = os.path.sep
SIGINT = 0x02
SIGQUIT = 0x03
SIGILL = 0x04
SIGTRAP = 0x05

# FAILED = "FAILED"
# SUCCESS = "SUCCESS"
FAILED = -1
SUCCESS = 0

TEMP = "TEMP"
USERVAR = "USERVAR"

# Exit codes
XC_EXFAILED = -1  # exec/wait failure - per system(3)
XC_SUCCESS = 0  # per system(3)
XC_ARGERR = 1  # error processing command line arguments
XC_ENVERR = 2  # bad environment startup
XC_TSTERR = 3  # test failed
XC_USRERR = 4  # user reject terms of use
XC_RUNERR = 5  # simulation did not complete as desired
XC_INIERR = 6  # initialization failed
XC_PRCERR = 7  # process control error
XC_SVRKLL = 8  # server killed
XC_IOERR = 9  # I/O error
XC_SHFAILED = 127  # shell failure - per system(3)
XC_SIGNAL = 128  # signal caught - must be or'd with SIG value if known
XC_EXCEPTION = 255  # exception caught
XC_SIGINT = XC_SIGNAL | SIGINT  # SIGINT caught

_TMP = "TMP"
env_delim = ":"
env_delim_char = ':'
env_pathsep = "/"

lastvar = None  # Assuming lastvar is a global variable
technology_readiness_level = None  # TODO fix this

TIMESTAMP = 0

class SIGNALS:
    SIGABRT= 6
    SIGFPE = 8
    SIGILL = 4
    SIGINT = 2
    SIGSEGV = 11
    SIGTERM = 15

class CheckpointType:
    WALL = 1
    SIM = 2
    NONE = 3


class STATUS(Enum):
    FAILED = False
    SUCCESS = True


class GLOBALVAR:
    def __init__(self, name, prop_type, addr, access, description=None, units=None, keys=None):
        self.prop = None
        self.next = None
        self.callback = None  # this function will be called whenever the globalvar is set
        self.lock = False
        # self.prop_type = prop_type
        # self.addr = addr
        # self.prop = access
        # self.description = description
        # self.units = units
        # self.keys = keys

# class GLOBALVAR:
#     def __init__(self):
#         self.prop = None
#         self.next = None
#         self.flags = 0
#         self.callback = None  # this function will be called whenever the globalvar is set
#         self.lock = 0


global_streaming_io_enabled = 0
def global_autoclean():
    pass


def global_bigranks():
    pass


def global_check_version():
    pass


def global_client_allowed():
    pass


def global_compileonly():
    pass


def global_deltamode_iteration_limit():
    pass


def global_deltamode_updateorder():
    pass


def global_exit_code():
    pass


def global_hostaddr():
    pass


def global_hostname():
    pass


def global_infourl():
    pass


def global_init_max_defer():
    pass


def global_inline_block_size():
    pass


def global_mainlooppauseat():
    pass


def global_master():
    pass


def global_master_port():
    pass


def global_module_compiler_flags():
    pass


def global_multirun_connection():
    pass


def global_randomnumbergenerator():
    pass


def global_reinclude():
    pass


def global_relax_naming_rules():
    pass


def global_return_code():
    pass


def global_run_power_world():
    pass


def global_sanitize_index():
    pass


def global_sanitize_offset():
    pass


def global_sanitize_options():
    pass


def global_sanitize_prefix():
    pass


def global_server_port_num():
    pass


def global_server_quit_on_close():
    pass


def global_show_progress():
    pass


global_signal_timeout = 100.0


def global_simulation_mode():
    pass


def global_slave_id():
    pass


def global_slave_port():
    pass




def global_svn_root():
    pass


def global_sync_dumpfile():
    pass


def global_validate_options():
    pass



def global_wget_options():
    pass


class DATEFORMAT(Enum):
    DF_ISO = 0
    DF_US = 1
    DF_EURO = 2


class INITSEQ(Enum):
    IS_CREATION = 0
    IS_DEFERRED = 1
    IS_BOTTOMUP = 2
    IS_TOPDOWN = 3


class TECHNOLOGYREADINESSLEVEL(Enum):
    TRL_UNKNOWN = 0
    TRL_PRINCIPLE = 1
    TRL_CONCEPT = 2
    TRL_PROOF = 3
    TRL_STANDALONE = 4
    TRL_INTEGRATED = 5
    TRL_DEMONSTRATED = 6
    TRL_PROTOTYPE = 7
    TRL_QUALIFIED = 8
    TRL_PROVEN = 9


class CHECKPOINTTYPE(Enum):  # checkpoint global_property_types determines how checkpoint intervals are used
    CPT_NONE = 0  # **< checkpoints is not enabled */
    CPT_WALL = 1  # **< checkpoints run on wall clock interval */
    CPT_SIM = 2  # **< checkpoints run on sim clock interval */


class COMPLEXCONVERFORMAT(Enum):
    CNF_DEFAULT = 0
    CNF_RECT = 1
    CNF_POLAR_DEG = 2
    CNF_POLAR_RAD = 3


class RANDOMNUMBERGENERATOR(Enum):  # identifies the global_property_types of random number generator used
    RNG2 = 2  # **< random numbers generated using pre-V3 method */
    RNG3 = 3  # **< random numbers generated using post-V2 method */


class MAINLOOPSTATE(Enum):  # identifies the main loop state
    MLS_INIT = 0  # main loop initializing
    MLS_RUNNING = 1  # main loop is running
    MLS_PAUSED = 2  # main loop is paused (waiting)
    MLS_DONE = 3  # main loop is done (steady)
    MLS_LOCKED = 4  # main loop is locked (possible deadlock)


class SIMULATIONMODE(Enum):  # simulation mode values, delta mode support
    SM_INIT = 0x00  # initial state of simulation
    SM_EVENT = 0x01  # event driven simulation mode
    SM_DELTA = 0x02  # finite difference simulation mode
    SM_DELTA_ITER = 0x03  # Iteration of finite difference simulation mode
    SM_ERROR = 0xff  # simulation mode error


class DELTAMODEFLAGS(Enum):  # /**< delta mode flags */
    DMF_NONE = 0x00  # /**< no flags */
    DMF_SOFTEVENT = 0x01  # /**< event is soft */


class MULTIRUNMODE(Enum):  # determines the global_property_types of run */
    MRM_STANDALONE = 0  # /**< multirun is not enabled (standalone run) */
    MRM_MASTER = 1  # /**< multirun is enabled and this run is the master run */
    MRM_SLAVE = 2  # /**< multirun is enabled and this run is the slace run */


class MULTIRUNCONNECTION(Enum):  # /**< determines the connection mode for a slave run */
    MRC_NONE = 0  # /**< isn't actually connected upwards */
    MRC_MEM = 1  # /**< use shared mem or the like */
    MRC_SOCKET = 2  # **< use a socket */


class MODULECOMPILEFLAGS(Enum):  # ;/* module compile flags */
    MC_NONE = 0x00  # < no module compiler flags */
    MC_CLEAN = 0x01  # < clean build */
    MC_KEEPWORK = 0x02  # < keep intermediate files */
    MC_DEBUG = 0x04  # < debug build */
    MC_VERBOSE = 0x08  # < verbose output */



# this should move to the Sanitize module when ready
class SANITIZEOPTIONS(Enum):
    SO_ERASE = 0x0001  # < option to erase/reset to default instead of obfuscate
    SO_NAMES = 0x0010  # < option to sanitize names
    SO_LATITUDE = 0x0020  # < option to sanitize latitude
    SO_LONGITUDE = 0x0040  # < option to sanitize longitude
    SO_GEOCOORDS = 0x0060  # < option to sanitize	lat/lon
    SO_CITY = 0x0080  # < option to sanitize city
    SO_TIME = 0x0100  # < option to sanitize times (start/stop/in/out)
    SO_DATE = 0x0200  # < option to sanitize date (start/stop/in/out)
    SO_TIMEZONE = 0x0800  # < option to sanitize timezone
    SO_SPATIAL = 0x00f0  # < option to sanitize all spatial info
    SO_TEMPORAL = 0x0f00  # < option to sanitize all temporal info
    SO_ALL = 0x0ff0  # < option to sanitize all info


# Global variables
global_autostartgui = True
global_browser = "your_browser_executable"
global_checkpoint_file = ""
global_checkpoint_interval = 3600
global_checkpoint_keepall = 0
global_checkpoint_seqnum = 0
global_checkpoint_type = CheckpointType.WALL
global_clock = TS_ZERO
global_command_line = ""
global_complex_format = "%+lg%+lg%c"
global_complex_output_format = COMPLEXCONVERFORMAT.CNF_DEFAULT
global_dateformat = DATEFORMAT.DF_ISO
global_debug_mode = False
global_debug_output = False
global_delta_curr_clock = 0
global_deltaclock = 0
global_deltamode_force_preferred_order = False
global_deltamode_forced_always = False
global_deltamode_forced_extra_timesteps = 0
global_deltamode_maximumtime_pub = 0
global_deltamode_timestep_pub = 0
global_double_format = "%+lg"
global_dumpall = False
global_dumpfile = "gridlabd.xml"
global_enter_realtime = TS_NEVER
global_environment = ""
global_execdir = ""
global_execname = ""
global_federation_reiteration = False
global_forbid_multiload = 0
global_force_compile = 0
global_gdb = 0
global_gdb_window = 0
global_guid_first = True
global_include = ""
global_init_sequence = INITSEQ.IS_DEFERRED
global_iteration_limit = 100
global_keep_progress = False
global_kmlfile = ""
global_lock_enabled = True
global_mainloopstate = ""
global_maximum_synctime = 60
global_minimum_timestep = 1
global_modelname = ""
global_ms_per_second = 1000
global_mt_analysis = 0
global_multirun_mode = False
global_next_time = TS_ZERO
global_no_balance = False
global_nolocks = 0
global_nondeterminism_warning = True
global_object_format = "%s:%d"
global_object_scan = "%[^:]:%d"
global_pauseatexit = 0
global_pidfile = ""
global_platform = "WINDOWS" if sys.platform == 'win32' else "MACOSX" if sys.platform == 'darwin' else "LINUX"
global_process_id = 0
global_profiler = 0
global_quiet_mode = False
global_randomseed = 0
global_realtime_metric = 0
global_run_realtime = False
global_runchecks = False
global_savefile = ""
global_skipsafe = 0
global_start_time = 946684800
global_stop_time = TS_NEVER
global_stoptime = 0
global_strictnames = True  # Initialize global_strictnames with the desired value
global_suppress_deprecated_messages = False
global_suppress_repeat_messages = True
global_sync_dumpfile = ""  # Provide the file path for debug purposes
global_test_mode = False
global_testoutputfile = "test.txt"
global_thread_count = 1
global_threadcount = 0
global_tmp = "C:\\WINDOWS\\TEMP" if sys.platform == 'win32' else "/tmp"  # Assuming global_tmp is a global variable
global_trace = ""
global_urlbase = "./" if global_debug_mode else "https://www.gridlabd.org/"
global_value = ""
global_varlist = None  # Assuming global_varlist is a global variable
global_verbose_mode = False
global_version_branch = ""
global_version_build = 0
global_version_major = Version.REV_MAJOR
global_version_minor = Version.REV_MINOR
global_version_patch = Version.REV_PATCH
global_warn_mode = True
global_workdir = "."
global_xml_encoding = 8
global_xmlstrict = True

if global_debug_mode:
    global_sync_dumpfile = ""


# This should move to the Validatre module.
class VALIDATEOPTIONS(Enum):
    VO_NONE = 0x0000  # < run no tests (just go through motions)

    # tests
    VO_TSTRUN = 0x0001  # < run passing tests
    VO_TSTERR = 0x0002  # < run error tests
    VO_TSTEXC = 0x0004  # < run exception tests
    VO_TSTSTD = 0x0007  # < run normal validation tests (run+err+exc)
    VO_TSTOPT = 0x0008  # < run optional tests
    VO_TSTALL = 0x000f  # < run all tests

    # test override
    VO_TSTREQ = 0x0010  # < make all tests required (not supported yet)
    VO_TSTOPTREQ = 0x0018  # < make optional test required (not supported yet)
    VO_TSTALLREQ = 0x001f  # < run all test with optionals required (not supported yet)

    # reports
    VO_RPTDIR = 0x0100  # < report includes individual directories search results
    VO_RPTGLM = 0x0200  # < report includes individual run results
    VO_RPTALL = 0x0300  # < report includes everything

    VO_DEFAULT = 0x000f | 0x0300  # VALIDATEOPTIONS.VO_TSTALL or VALIDATEOPTIONS.VO_RPTALL




# Keyword lists

cnf_keys = [
    {"DEFAULT": COMPLEXCONVERFORMAT.CNF_DEFAULT},
    {"RECT": COMPLEXCONVERFORMAT.CNF_RECT},
    {"POLAR_DEG": COMPLEXCONVERFORMAT.CNF_POLAR_DEG},
    {"POLAR_RAD": COMPLEXCONVERFORMAT.CNF_POLAR_RAD},
]

df_keys = [
    {"ISO": DATEFORMAT.DF_ISO},
    {"US": DATEFORMAT.DF_US},
    {"EURO": DATEFORMAT.DF_EURO},
]

trl_keys = [
    {"PRINCIPLE": TECHNOLOGYREADINESSLEVEL.TRL_PRINCIPLE},
    {"CONCEPT": TECHNOLOGYREADINESSLEVEL.TRL_CONCEPT},
    {"PROOF": TECHNOLOGYREADINESSLEVEL.TRL_PROOF},
    {"STANDALONE": TECHNOLOGYREADINESSLEVEL.TRL_STANDALONE},
    {"INTEGRATED": TECHNOLOGYREADINESSLEVEL.TRL_INTEGRATED},
    {"DEMONSTRATED": TECHNOLOGYREADINESSLEVEL.TRL_DEMONSTRATED},
    {"PROTOTYPE": TECHNOLOGYREADINESSLEVEL.TRL_PROTOTYPE},
    {"QUALIFIED": TECHNOLOGYREADINESSLEVEL.TRL_QUALIFIED},
    {"PROVEN": TECHNOLOGYREADINESSLEVEL.TRL_PROVEN},
    {"UNKNOWN": TECHNOLOGYREADINESSLEVEL.TRL_UNKNOWN},
]

cpt_keys = [
    {"NONE": CHECKPOINTTYPE.CPT_NONE},
    {"WALL": CHECKPOINTTYPE.CPT_WALL},
    {"SIM": CHECKPOINTTYPE.CPT_SIM},
]

rng_keys = [
    {"RNG2": RANDOMNUMBERGENERATOR.RNG2},
    {"RNG3": RANDOMNUMBERGENERATOR.RNG3},
]

mls_keys = [
    {"INIT": MAINLOOPSTATE.MLS_INIT},
    {"RUNNING": MAINLOOPSTATE.MLS_RUNNING},
    {"PAUSED": MAINLOOPSTATE.MLS_PAUSED},
    {"DONE": MAINLOOPSTATE.MLS_DONE},
    {"LOCKED": MAINLOOPSTATE.MLS_LOCKED},
]

mrm_keys = [
    {"STANDALONE": MULTIRUNMODE.MRM_STANDALONE},
    {"MASTER": MULTIRUNMODE.MRM_MASTER},
    {"SLAVE": MULTIRUNMODE.MRM_SLAVE},
]

mrc_keys = [
    {"NONE": MULTIRUNCONNECTION.MRC_NONE},
    {"MEMORY": MULTIRUNCONNECTION.MRC_MEM},
    {"SOCKET": MULTIRUNCONNECTION.MRC_SOCKET},
]

isc_keys = [
    {"CREATION": INITSEQ.IS_CREATION},
    {"DEFERRED": INITSEQ.IS_DEFERRED},
    {"BOTTOMUP": INITSEQ.IS_BOTTOMUP},
    {"TOPDOWN": INITSEQ.IS_TOPDOWN},
]

mcf_keys = [
    {"NONE": MODULECOMPILEFLAGS.MC_NONE},
    {"CLEAN": MODULECOMPILEFLAGS.MC_CLEAN},
    {"KEEPWORK": MODULECOMPILEFLAGS.MC_KEEPWORK},
    {"DEBUG": MODULECOMPILEFLAGS.MC_DEBUG},
    {"VERBOSE": MODULECOMPILEFLAGS.MC_VERBOSE},
]

vo_keys = [
    {"NONE": VALIDATEOPTIONS.VO_NONE},
    {"TSTD": VALIDATEOPTIONS.VO_TSTSTD},
    {"TALL": VALIDATEOPTIONS.VO_TSTALL},
    {"TRUN": VALIDATEOPTIONS.VO_TSTRUN},
    {"TERR": VALIDATEOPTIONS.VO_TSTERR},
    {"TEXC": VALIDATEOPTIONS.VO_TSTEXC},
    {"TOPT": VALIDATEOPTIONS.VO_TSTOPT},
    {"RALL": VALIDATEOPTIONS.VO_RPTALL},
    {"RDIR": VALIDATEOPTIONS.VO_RPTDIR},
    {"RGLM": VALIDATEOPTIONS.VO_RPTGLM},
]

so_keys = [
    {"NAMES": SANITIZEOPTIONS.SO_NAMES},
    {"POSITIONS": SANITIZEOPTIONS.SO_GEOCOORDS},
]

sm_keys = [
    {"INIT": SIMULATIONMODE.SM_INIT},
    {"EVENT": SIMULATIONMODE.SM_EVENT},
    {"DELTA": SIMULATIONMODE.SM_DELTA},
    {"DELTA_ITER": SIMULATIONMODE.SM_DELTA_ITER},
    {"ERROR": SIMULATIONMODE.SM_ERROR},
]


# Function to build the temporary directory path
def buildtmp():
    global global_tmp

    tmp = os.getenv("GLTEMP")
    if tmp:
        global_tmp = tmp
        return

    home = os.getenv(HOMEVAR)
    if home:
        if os.name == 'nt':
            drive = os.getenv("HOMEDRIVE") or ""
            global_tmp = os.path.join(drive, home, "Local Settings", "Temp", "gridlabd")
        else:
            global_tmp = os.path.join(home, ".gridlabd", "tmp")
        return

    tmp = os.getenv("TMP") or os.getenv("TEMP") or _TMP
    user = os.getenv(USERVAR)
    global_tmp = os.path.join(tmp, user if user else "", "gridlabd")



# Function to register global variables
def global_init():
    buildtmp()

    global global_version_major
    global global_version_minor
    global global_version_patch
    global global_version_build
    global global_version_branch

    global_version_major = version_major()
    global_version_minor = version_minor()
    global_version_patch = version_patch()
    global_version_build = version_build()
    global_version_branch = version_branch()[:len(global_version_branch)]


    for i in range(len(global_map)):
        p = global_map[i]
        var = global_create(p["name"], p["global_property_types"], p["addr"], PropertyType.PT_ACCESS, p["access"],
                            p["description"] if "description" in p else 0,
                            p["description"] if "description" in p else None,
                            PropertyType.PT_UNITS if "units" in p else 0, p["units"] if "units" in p else None, None)
        if var is None:
            print(sys.stderr, "global_init(): global variable '%s' registration failed" % p["name"])
            # TROUBLESHOOT
            # The global variable initialization process was unable to register
            # the indicated global variable. This error usually follows a more
            # detailed explanation of the error. Follow the troubleshooting for
            # that message and try again.
        else:
            var.prop.keywords = p["keys"] if "keys" in p else None
            var.callback = p["callback"] if "callback" in p else None

    return SUCCESS


# Function to find a global variable
def global_find(name):
    var = None
    if name is None:  # Get the first global in the list
        return global_get_next(None)
    for var in global_get_next(None):
        if var.prop.name == name:
            return var
    return None


# Function to get the next global variable name
def global_get_next(previous):
    if previous is None:
        return global_varlist
    else:
        return previous.next


# Function to create a user-defined global variable
def global_create(name, *args):
    va_args = list(args)
    prop_type = va_args.pop(0)
    addr = va_args.pop(0)
    access = va_args.pop(0)
    description = None
    units = None
    keys = None
    while va_args:
        prop_type_arg = va_args.pop(0)
        if prop_type_arg == 0:
            break
        if prop_type_arg == PropertyType.PT_KEYWORD:
            keyword = va_args.pop(0)
            keyvalue = va_args.pop(0)
            key = Keyword(keyword, keyvalue)
            if prop_type == PropertyType.PT_enumeration:
                if keys is None:
                    keys = [key]
                else:
                    keys.append(key)
            elif prop_type == PropertyType.PT_set:
                if keys is None:
                    keys = [(key.name, key.value)]
                else:
                    keys.append((key.name, key.value))
        elif prop_type_arg == PropertyType.PT_ACCESS:
            access_arg = va_args.pop(0)
            if access_arg in [PropertyAccess.PA_PUBLIC, PropertyAccess.PA_REFERENCE, PropertyAccess.PA_PROTECTED,
                              PropertyAccess.PA_PRIVATE, PropertyAccess.PA_HIDDEN]:
                access = access_arg
            else:
                errno = EINVAL
                print(sys.stderr, "global_create(): unrecognized property access code (PropertyAccess=%d)" % access_arg)
                # TROUBLESHOOT
                # The specific property access code is not recognized. Correct the access code and try again.
        elif prop_type_arg == PropertyType.PT_SIZE:
            size = va_args.pop(0)
            if size > 0:
                addr = [None] * size  # Assuming this is a valid way to initialize an array with None
            else:
                print(sys.stderr, "global_create(): property size must be greater than 0 to allocate memory")
                # TROUBLESHOOT
                # The size of the property must be positive.
        elif prop_type_arg == PropertyType.PT_UNITS:
            units = va_args.pop(0)
        elif prop_type_arg == PropertyType.PT_DESCRIPTION:
            description = va_args.pop(0)
        elif prop_type_arg == PropertyType.PT_DEPRECATED:
            pass  # Do nothing for deprecated properties
        else:
            print(sys.stderr, "global_create(): property extension code not recognized (PropertyType=%d)" % prop_type_arg)
            # TROUBLESHOOT
            # The property extension code used is not valid. This is probably a bug and should be reported.

    # Check for duplicate entries
    if global_find(name):
        errno = EINVAL
        print(sys.stderr, "tried to create global variable '%s' a second time" % name)
        # TROUBLESHOOT
        # An attempt to create a global variable failed because the
        # indicated variable already exists. Find out what is attempting
        # to create the variable and fix the problem and try again.

        return None

    # Allocate the global var definition
    var = GLOBALVAR(name, prop_type, addr, access, description, units, keys)

    # if var is None:
    #     errno = ENOMEM
    #     raise(f"global_create(char *name='%s',...): unable to allocate memory for global variable {name}")
    #     # TROUBLESHOOT
    #     # There is insufficient memory to allocate for the global variable. Try freeing up memory and try again.
    #
    #     return None

    var.prop = None
    var.next = None

    # # Link global_map to owner_class if not yet done
    # if lastvar is not None:
    #     lastvar.next = var
    # else:
    #     lastvar = var

    # 	/* read the property args */
    # 	va_start(arg, name);
    #
    # //	while ((proptype = va_arg(arg,PropertyType)) != 0){
    #     uint64 prop_buffer;
    #     while ((prop_buffer = va_arg(arg, uint64)) != 0) {
    #         proptype = PropertyType(prop_buffer);
    #         if (proptype > _PT_LAST) {
    #             if (prop == NULL) {
    #                 throw_exception(
    #                         "global_create(char *name='%s',...): property keyword not specified after an enumeration property definition",
    #                         name);
    #             } else if (proptype == PropertyType.PT_KEYWORD && prop->global_property_types == PropertyType.PT_enumeration) {
    #                 char *keyword = va_arg(arg, char *);
    #                 int32 keyvalue = va_arg(arg, int32);
    #                 Keyword *key = (Keyword *) malloc(sizeof(Keyword));
    #                 if (key == NULL) {
    #                     throw_exception("global_create(char *name='%s',...): property keyword could not be stored" % name);
    #                     /* TROUBLESHOOT
    #                         The memory needed to store the property's keyword is not available.  Try freeing up memory and try again.
    #                      */
    #                 }
    #                 key->next = prop->keywords;
    #                 strncpy(key->name, keyword, sizeof(key->name));
    #                 key->value = keyvalue;
    #                 prop->keywords = key;
    #             } else if (proptype == PropertyType.PT_KEYWORD && prop->global_property_types == PropertyType.PT_set) {
    #                 char *keyword = va_arg(arg, char *);
    #                 unsigned int64 keyvalue = va_arg(arg, uint64);
    #                 Keyword *key = (Keyword *) malloc(sizeof(Keyword));
    #                 if (key == NULL) {
    #                     throw_exception("global_create(char *name='%s',...): property keyword could not be stored" % name);
    #                     /* TROUBLESHOOT
    #                         The memory needed to store the property's keyword is not available.  Try freeing up memory and try again.
    #                      */
    #                 }
    #                 key->next = prop->keywords;
    #                 strncpy(key->name, keyword, sizeof(key->name));
    #                 key->value = keyvalue;
    #                 prop->keywords = key;
    #             } else if (proptype == PropertyType.PT_ACCESS) {
    #                 prop_buffer = va_arg(arg, uint64);
    #                 PropertyAccess pa = PropertyAccess(prop_buffer);
    #                 switch (pa) {
    #                     case PropertyAccess.PA_PUBLIC:
    #                     case PropertyAccess.PA_REFERENCE:
    #                     case PropertyAccess.PA_PROTECTED:
    #                     case PropertyAccess.PA_PRIVATE:
    #                     case PropertyAccess.PA_HIDDEN:
    #                         prop->access = pa;
    #                         break;
    #                     default:
    #                         errno = EINVAL;
    #                         throw_exception(
    #                                 "global_create(char *name='%s',...): unrecognized property access code (PropertyAccess=%d)",
    #                                 name, pa);
    #                         /* TROUBLESHOOT
    #                             The specific property access code is not recognized.  Correct the access code and try again.
    #                          */
    #                         break;
    #                 }
    #             } else if (proptype == PropertyType.PT_SIZE) {
    #                 prop->size = va_arg(arg, uint32);
    #                 if (prop->addr == 0) {
    #                     if (prop->size > 0) {
    #                         prop->addr = (PROPERTYADDR) malloc(prop->size * property_size(prop));
    #                     } else {
    #                         throw_exception(
    #                                 "global_create(char *name='%s',...): property size must be greater than 0 to allocate memory",
    #                                 name);
    #                         /* TROUBLESHOOT
    #                             The size of the property must be positive.
    #                          */
    #                     }
    #                 }
    #             } else if (proptype == PropertyType.PT_UNITS) {
    #                 char *unitspec = va_arg(arg, char *);
    #                 if ((prop->unit = unit_find(unitspec)) == NULL) {
    #                     output_warning("global_create(char *name='%s',...): property %s unit '%s' is not recognized" % name,
    #                                    prop->name, unitspec);
    #                     /* TROUBLESHOOT
    #                         The property definition uses a unit that is not found.  Check the unit and try again.
    #                         If you wish to define a new unit, try adding it to <code>.../etc/unitfile.txt</code>.
    #                      */
    #                 }
    #             } else if (proptype == PropertyType.PT_DESCRIPTION) {
    #                 prop->description = va_arg(arg, char*);
    #             } else if (proptype == PropertyType.PT_DEPRECATED) {
    #                 prop->flags |= PF_DEPRECATED;
    #             } else {
    #                 throw_exception(
    #                         "global_create(char *name='%s',...): property extension code not recognized (PropertyType=%d)",
    #                         name, proptype);
    #                 /* TROUBLESHOOT
    #                     The property extension code used is not valid.  This is probably a bug and should be reported.
    #                  */
    #             }
    #
    # //            prop = property_malloc(proptype, NULL, name, NULL, NULL);
    #         } else {
    #
    #             prop_buffer = va_arg(arg, uint64);
    #             PROPERTYADDR addr = PROPERTYADDR(prop_buffer);
    #             if (strlen(name) >= sizeof(prop->name)) {
    #                 throw_exception("global_create(char *name='%s',...): property name '%s' is too big to store" % name,
    #                                 name);
    #                 /* TROUBLESHOOT
    #                     The property name cannot be longer than the size of the internal buffer used to store it (currently this is 63 characters).
    #                     Use a shorter name and try again.
    #                  */
    #             }
    #             prop = property_malloc(proptype, NULL, strdup(name), addr, NULL);
    #
    #             if (prop == NULL)
    #                 throw_exception("global_create(char *name='%s',...): property '%s' could not be stored" % name, name);
    #             if (var->prop == NULL)
    #                 var->prop = prop;
    #
    #             /* link global_map to owner_class if not yet done */
    #             if (lastprop != NULL)
    #                 lastprop->next = prop;
    #             else
    #                 lastprop = prop;
    #
    #             /* save enum property in case keywords come up */
    #             if (prop->global_property_types > _PT_LAST)
    #                 prop = NULL;
    #         }
    #     }
    # 	va_end(arg);
    #
    # 	if (lastvar==NULL)
    # 		/* first variable */
    # 		global_varlist = lastvar = var;
    # 	else
    # 	{	/* not first */
    # 		lastvar->next = var;
    # 		lastvar = var;
    # 	}

    return var


# Function to set a user-defined global variable
def class_string_to_property(prop, prop_addr, value):
    pass


def global_set_var(def_str, *args):
    name = ""
    value = ""

    if len(args) == 0:
        return FAILED

    if "=" in def_str:
        name, value = def_str.split("=", 1)
    else:
        v = args[0]
        if v is not None:
            value = v
            # if value != v:
            #     print(sys.stderr, "global_setvar(char *name='%s',...): value is too long to store")
            #     return FAILED

    if name != "":
        var = global_find(name)
        global globalvar_lock

        if var is None:
            if global_strictnames:
                print(sys.stderr, "strict naming prevents implicit creation of %s" % name)
                return FAILED

            var = global_create(name, PropertyType.PT_char1024, None,
                                PropertyType.PT_SIZE, 1, PropertyType.PT_ACCESS, PropertyAccess.PA_PUBLIC, None)
            if var is None:
                print(sys.stderr, "unable to implicitly create the global variable '%s'" % name)
                return FAILED

        # WRITELOCK(globalvar_lock)
        retval = class_string_to_property(var.prop, var.prop.prop_addr, value)
        # WRITEUNLOCK(globalvar_lock)

        if retval == 0:
            print(sys.stderr, "global_setvar(): unable to set %s to %s" % (name, value))
            return FAILED
        elif var.callback:
            var.callback(var.prop.name)

        return SUCCESS
    else:
        print(sys.stderr, "global variable definition '%s' not formatted correctly" % def_str)
        return FAILED


# Function to generate a global GUID
def entropy_source():
    pass


def global_guid(buffer, size):
    global global_guid_first

    if size > 36:
        if global_guid_first:
            random.seed(entropy_source())
            global_guid_first = False

        buffer = f'{random.randint(0x0000, 0xffff):04x}{random.randint(0x0000, 0xffff):04x}-' \
                 f'{random.randint(0x0000, 0xffff):04x}-4{random.randint(0x000, 0xfff):03x}-' \
                 f'{random.randint(0x0000, 0xffff):04x}-{random.randint(0x0000, 0xffff):04x}' \
                 f'{random.randint(0x0000, 0xffff):04x}{random.randint(0x0000, 0xffff):04x}'

        return buffer
    else:
        print(sys.stderr, "global_guid(...): buffer too small")
        return None


# Function to generate a global run ID
def global_run(size):
    global global_value

    if global_value == "":
        global_value = global_guid(None, 0)

    if size > 36:
        buffer = global_value
        return buffer
    else:
        return None


# Function to generate the current date and time in a specific format
def global_now(size):
    if size > 32:
        now = time.time()
        # tmbuf = datetime.datetime.utcfromtimestamp(now)
        # buffer = tmbuf.strftime('%Y%m%d-%H%M%S')

        tmbuf = time.gmtime(now)
        buffer = time.strftime("%Y%m%d-%H%M%S", tmbuf)
        return buffer
    else:
        print(sys.stderr, "global_now(...): buffer too small")
        return None


# Function to generate a global "true" value
def global_true(size):
    if size > 1:
        buffer = True
        return buffer
    else:
        print(sys.stderr, "global_now(...): buffer too small")
        return None


# Function to handle global sequence operations
def global_seq(buffer, size, name):
    seq = ""
    opt = ""

    if ":" in name:
        seq, opt = name.split(":", 1)

    if opt == "INIT":
        var = global_find(seq)

        if var is not None:
            print(f"global_seq(char *name='{seq}'): sequence is already initialized")
            return None
        else:
            addr = [0]
            var = global_create(seq, PropertyType.PT_int32, addr, PropertyType.PT_ACCESS, PropertyAccess.PA_PUBLIC,
                                None)
            addr[0] = 0
            return global_get_var(seq, buffer, size)
    elif opt == "INC":
        var = global_find(seq)
        addr = None

        if var is None or var.prop.global_property_types != PropertyType.PT_int32:
            print(sys.stderr, "global_seq(char *name='%s'): sequence name is missing or not an int32 variable" % name)
            return None

        addr = var.prop.prop_addr
        addr[0] += 1
        print(f"updating global sequence '{seq}' to value '{addr[0]}'")
        return global_get_var(seq, buffer, size)
    else:
        print(sys.stderr, "global_seq(..., char *name='%s'): sequence spec '%s' is invalid" % (name, opt))
        return None


def global_isdefined(name):
    return global_find(name) is not None


def parameter_expansion(buffer, size, spec):
    name, value, pattern, op, string = "", "", "", "", ""
    yes, no = "1", "0"
    offset, length, number = 0, 0, 0

    # ${name:-value}
    match = re.match(r'([^:]+):-([^}]+)}', spec)
    if match:
        name, value = match.groups()
        if not global_get_var(name, buffer, size):
            buffer = value[:size]
        return (name, value, pattern, op, string, yes, no, offset, length, number)

    # ${name:=value}
    match = re.match(r'([^:]+):=([^}]+)}', spec)
    if match:
        name, value = match.groups()
        if not global_isdefined(name):
            global_set_var(name, value)
        global_get_var(name, buffer, size)
        return (name, value, pattern, op, string, yes, no, offset, length, number)

    # ${name:+value}
    match = re.match(r'([^:]+):\+([^}]+)}', spec)
    if match:
        name, value = match.groups()
        if not global_isdefined(name):
            buffer = ""
        else:
            buffer = value[:size]
        return (name, value, pattern, op, string, yes, no, offset, length, number)

    # ${name:offset:length}
    match = re.match(r'([^:]+):(\d+):(\d+)', spec)
    if match:
        name, offset, length = match.groups()
        temp = global_get_var(name, "", 1024)
        if temp:
            buffer = temp[offset:offset + length]
            buffer = buffer[:size]
            return (name, value, pattern, op, string, yes, no, offset, length, number)
        else:
            return (name, value, pattern, op, string, yes, no, offset, length, number)

    # ${name:offset}
    match = re.match(r'([^:]+):(\d+)', spec)
    if match:
        name, offset = match.groups()
        temp = global_get_var(name, "", 1024)
        if temp:
            buffer = temp[offset:]
            buffer = buffer[:size]
            return (name, value, pattern, op, string, yes, no, offset, length, number)
        else:
            return (name, value, pattern, op, string, yes, no, offset, length, number)

    # ${name/offset/length}
    match = re.match(r'([^/]+)/([^/]+)/([^}]+)}', spec)
    if match:
        name, pattern, string = match.groups()
        temp = global_get_var(name, "", 1024)
        if not temp:
            return (name, value, pattern, op, string, yes, no, offset, length, number)
        buffer = ""
        ptr = temp.find(pattern)
        if ptr != -1:
            start = ptr
            buffer = temp[:size]
            buffer = buffer[:start] + string + buffer[start + len(string):]
        return (name, value, pattern, op, string, yes, no, offset, length, number)

    # ${name//offset/length}
    match = re.match(r'([^/]+)/(/[^/]+)/([^}]+)}', spec)
    if match:
        name, pattern, string = match.groups()
        temp = global_get_var(name, "", 1024)
        if not temp:
            return (name, value, pattern, op, string, yes, no, offset, length, number)
        buffer = ""
        while True:
            ptr = temp.find(pattern)
            if ptr == -1:
                break
            start = ptr
            buffer = temp[:size]
            buffer = buffer[:start] + string + buffer[start + len(string):]
            temp = buffer
        return (name, value, pattern, op, string, yes, no, offset, length, number)

    # ${++name}
    match = re.match(r'\+\+([A-Za-z0-9_:.]+)', spec)
    if match:
        name = match.group(1)
        var = global_find(name)
        if var and var.prop.global_property_types == PropertyType.PT_int32:
            addr = var.prop.prop_addr
            buffer = str(addr[0] + 1)
            return (name, value, pattern, op, string, yes, no, offset, length, number)

    # ${--name}
    match = re.match(r'--([A-Za-z0-9_:.]+)', spec)
    if match:
        name = match.group(1)
        var = global_find(name)
        if var and var.prop.global_property_types == PropertyType.PT_int32:
            addr = var.prop.prop_addr
            buffer = str(addr[0] - 1)
            return (name, value, pattern, op, string, yes, no, offset, length, number)

    # ${name op value}
    match = re.match(r'([^!<>=&|~]+)([!<>=&|~])(\d+)\?([^:]+):([^}]+)', spec)
    if match:
        name, op, number, yes, no = match.groups()
        var = global_find(name)
        if var and var.prop.global_property_types == PropertyType.PT_int32:
            addr = var.prop.prop_addr
            if op == "==":
                buffer = yes if addr[0] == int(number) else no
                return (name, value, pattern, op, string, yes, no, offset, length, number)
            elif op in ("!=", "<>"):
                buffer = yes if addr[0] != int(number) else no
                return (name, value, pattern, op, string, yes, no, offset, length, number)
            elif op == "<=":
                buffer = yes if addr[0] <= int(number) else no
                return (name, value, pattern, op, string, yes, no, offset, length, number)
            elif op == "<":
                buffer = yes if addr[0] < int(number) else no
                return (name, value, pattern, op, string, yes, no, offset, length, number)
            elif op == ">=":
                buffer = yes if addr[0] >= int(number) else no
                return (name, value, pattern, op, string, yes, no, offset, length, number)
            elif op == ">":
                buffer = yes if addr[0] > int(number) else no
                return (name, value, pattern, op, string, yes, no, offset, length, number)
            elif op == "&":
                buffer = yes if addr[0] & int(number) else no
                return (name, value, pattern, op, string, yes, no, offset, length, number)
            elif op == "|~":
                buffer = yes if addr[0] | ~int(number) else no
                return (name, value, pattern, op, string, yes, no, offset, length, number)

    # ${name op= value}
    match = re.match(r'([^+-/*%&^|~=]+)([-+/*%&^|~=])(\d+)', spec)
    if match:
        name, op, number = match.groups()
        var = global_find(name)
        if var and var.prop.global_property_types == PropertyType.PT_int32:
            addr = var.prop.prop_addr
            buffer = str(addr[0])
            if op == "+=":
                addr[0] += int(number)
                buffer = str(addr[0])
                return (name, value, pattern, op, string, yes, no, offset, length, number)
            if op == "-=":
                addr[0] -= int(number)
                buffer = str(addr[0])
                return (name, value, pattern, op, string, yes, no, offset, length, number)
            if op == "*=":
                addr[0] *= int(number)
                buffer = str(addr[0])
                return (name, value, pattern, op, string, yes, no, offset, length, number)
            if op == "/=":
                addr[0] /= int(number)
                buffer = str(addr[0])
                return (name, value, pattern, op, string, yes, no, offset, length, number)
            if op == "%=":
                addr[0] %= int(number)
                buffer = str(addr[0])
                return (name, value, pattern, op, string, yes, no, offset, length, number)
            if op == "&=":
                addr[0] &= int(number)
                buffer = str(addr[0])
                return (name, value, pattern, op, string, yes, no, offset, length, number)
            if op == "|=":
                addr[0] |= int(number)
                buffer = str(addr[0])
                return (name, value, pattern, op, string, yes, no, offset, length, number)
            if op == "^=":
                addr[0] ^= int(number)
                buffer = str(addr[0])
                return (name, value, pattern, op, string, yes, no, offset, length, number)
            if op == "&=~":
                addr[0] &= ~int(number)
                buffer = str(addr[0])
                return (name, value, pattern, op, string, yes, no, offset, length, number)
            if op == "|=~":
                addr[0] |= ~int(number)
                buffer = str(addr[0])
                return (name, value, pattern, op, string, yes, no, offset, length, number)
            if op == "^=~":
                addr[0] ^= ~int(number)
                buffer = str(addr[0])
                return (name, value, pattern, op, string, yes, no, offset, length, number)

    # ${name=number}
    match = re.match(r'([^=]+)=(\d+)', spec)
    if match:
        name, number = match.groups()
        var = global_find(name)
        addr = None
        if var is None:
            addr = [int(number)]
            var = global_create(name, PropertyType.PT_int32, addr, PropertyType.PT_ACCESS, PropertyAccess.PA_PUBLIC,
                                None)
        else:
            addr = var.prop.prop_addr
            addr[0] = int(number)
        buffer = str(number)
        return (name, value, pattern, op, string, yes, no, offset, length, number)

    # ${name=string}
    match = re.match(r'([^=]+)=([^}]+)}', spec)
    if match:
        name, string = match.groups()
        global_set_var(name, string)
        buffer = string[:size]
        return (name, value, pattern, op, string, yes, no, offset, length, number)

    return (name, value, pattern, op, string, yes, no, offset, length, number)


def global_get_var(name, buffer, size):
    """
    Get the value of a global variable in a safer fashion.

    :param name: The name of the variable to retrieve.
    :param buffer: The buffer where the data will be stored.
    :param size: The size of the buffer.
    :return: A pointer to the buffer holding the data, None if insufficient buffer space or if the name was not found.
    """
    temp = [0] * 1024  # Initialize a temporary buffer
    len_ = 0
    var = None

    # Special variables names
    special_variables = [
        {"name": "GUID", "call": global_guid},
        {"name": "NOW", "call": global_now},
        {"name": "RUN", "call": global_run},
        {"name": "WINDOWS", "call": global_true},
        # {"name": "APPLE", "call": global_true} if defined __APPLE__ else
        # {"name": "LINUX", "call": global_true},
        # {"name": "MATLAB", "call": global_true} if HAVE_MATLAB else
        # {"name": "MYSQL", "call": global_true} if HAVE_MYSQL else
        {"name": None, "call": None},  # Placeholder for the loop
    ]

    # Check for buffer, name, and size validity
    if buffer is None:
        print(sys.stderr, "global_getvar: buffer not supplied")
        return None
    if name is None:
        print(sys.stderr, "global_getvar: variable name not supplied")
        return None
    if size < 1:
        print(sys.stderr, "global_getvar: invalid buffer size")
        return None  # User error

    # Special variables
    for special_var in special_variables:
        if special_var["name"] == name:
            return special_var["call"](buffer, size)

    # Sequences
    if name.startswith("SEQ_") and ':' in name:
        return global_seq(buffer, size, name)

    # Expansions
    if parameter_expansion(buffer, size, name):
        return buffer

    var = global_find(name)
    if var is None:
        # Try parameter expansion again
        if parameter_expansion(buffer, size, name):
            return buffer
        else:
            return None

    # len_ = DynamicClass.property_to_string(var.prop, var.prop.addr, temp, len(temp))
    # if len_ < size:
    #     # If we have enough space, copy to the supplied buffer
    #     buffer[:len_] = temp[:len_]
    #     return buffer  # Wrote buffer, return pointer for printf functions

    return None  # None if insufficient buffer space


def global_get_count():
    """
    Get the count of global variables.

    :return: The count of global variables.
    """
    count = 0
    var = None
    while var is not None:
        var = global_get_next(var)
        count += 1
    return count


def global_dump():
    """
    Dump global variables.

    """
    global global_suppress_repeat_messages
    var = None
    old = global_suppress_repeat_messages
    global_suppress_repeat_messages = 0
    while var is not None:
        var = global_get_next(var)
        buffer = [0] * 1024
        # if DynamicClass.property_to_string(var.prop, var.prop.addr, buffer, len(buffer)):
        #     print(f"{var.prop.name}={buffer};")
    global_suppress_repeat_messages = old


def global_remote_read(local, var):
    """
    Thread-safe remote global read.

    :param local: Local memory for data (must be the correct size for global).
    :param var: Global variable from which to get data.
    :return: Local memory with data copied from the global variable.
    """
    size = len(var.prop)
    addr = var.prop.addr
    global global_multirun_mode
    # Single host
    if global_multirun_mode == MULTIRUNMODE.MRM_STANDALONE:
        # Single thread
        if global_thread_count == 1:
            # No lock or fetch required
            local[:size] = addr[:size]
            return local
        # Multithread
        else:
            with threading.RLock().acquire():
                # rlock(var.lock)
                local[:size] = copy.copy(addr[:size])
                # runlock(var.lock)
            return local
    else:
        # @todo remote object read for multihost
        return None


def global_remote_write(local, var):
    """
    Thread-safe remote global write.

    :param local: Local memory for data.
    :param var: Global variable to which data is written.
    """
    size = len(var.prop)
    addr = var.prop.addr

    # Single host
    if global_multirun_mode == MULTIRUNMODE.MRM_STANDALONE:
        # Single thread
        if global_thread_count == 1:
            # No lock or fetch required
            addr[:size] = local[:size]
        # Multithread
        else:
            with threading.Lock().acquire():
                # wlock(var.lock)
                addr[:size] = copy.copy(local[:size])
                # wunlock(var.lock)
    else:
        # @todo remote object write for multihost
        pass  # Placeholder for multihost implementation


# PropertyMap global_map
global_map = [
    {"name": "version.major", "global_property_types": PropertyType.PT_int32, "addr": global_version_major,
     "access": PropertyAccess.PA_REFERENCE, "description": "major version"},
    {"name": "version.minor", "global_property_types": PropertyType.PT_int32, "addr": global_version_minor,
     "access": PropertyAccess.PA_REFERENCE, "description": "minor version"},
    {"name": "version.patch", "global_property_types": PropertyType.PT_int32, "addr": global_version_patch,
     "access": PropertyAccess.PA_REFERENCE, "description": "patch number"},
    {"name": "version.build", "global_property_types": PropertyType.PT_int32, "addr": global_version_build,
     "access": PropertyAccess.PA_REFERENCE, "description": "build number"},
    {"name": "version.branch", "global_property_types": PropertyType.PT_char256, "addr": global_version_branch,
     "access": PropertyAccess.PA_REFERENCE, "description": "branch name"},
    {"name": "command_line", "global_property_types": PropertyType.PT_char1024, "addr": global_command_line,
     "access": PropertyAccess.PA_REFERENCE, "description": "command line"},
    {"name": "environment", "global_property_types": PropertyType.PT_char1024, "addr": global_environment,
     "access": PropertyAccess.PA_PUBLIC, "description": "operating environment"},
    {"name": "quiet", "global_property_types": PropertyType.PT_bool, "addr": global_quiet_mode, "access": PropertyAccess.PA_PUBLIC,
     "description": "quiet output status flag"},
    {"name": "warn", "global_property_types": PropertyType.PT_bool, "addr": global_warn_mode, "access": PropertyAccess.PA_PUBLIC,
     "description": "warning output status flag"},
    {"name": "debugger", "global_property_types": PropertyType.PT_bool, "addr": global_debug_mode, "access": PropertyAccess.PA_PUBLIC,
     "description": "debugger enable flag"},
    {"name": "gdb", "global_property_types": PropertyType.PT_bool, "addr": global_gdb, "access": PropertyAccess.PA_PUBLIC,
     "description": "gdb enable flag"},
    {"name": "debug", "global_property_types": PropertyType.PT_bool, "addr": global_debug_output, "access": PropertyAccess.PA_PUBLIC,
     "description": "debug output status flag"},
    {"name": "test", "global_property_types": PropertyType.PT_bool, "addr": global_debug_mode, "access": PropertyAccess.PA_PUBLIC,
     "description": "test enable flag"},
    {"name": "verbose", "global_property_types": PropertyType.PT_bool, "addr": global_verbose_mode, "access": PropertyAccess.PA_PUBLIC,
     "description": "verbose enable flag"},
    {"name": "iteration_limit", "global_property_types": PropertyType.PT_int32, "addr": global_iteration_limit,
     "access": PropertyAccess.PA_PUBLIC, "description": "iteration limit"},
    {"name": "federation_reiteration", "global_property_types": PropertyType.PT_bool, "addr": global_federation_reiteration,
     "access": PropertyAccess.PA_REFERENCE,
     "description": "global boolean to enforce a reiteration for all modules due to an external federation reiteration"},
    {"name": "workdir", "global_property_types": PropertyType.PT_char1024, "addr": global_workdir, "access": PropertyAccess.PA_REFERENCE,
     "description": "working directory"},
    {"name": "lock", "global_property_types": PropertyType.PT_bool, "addr": global_lock_enabled, "access": PropertyAccess.PA_PUBLIC,
     "description": "lock enabled flag"},
    {"name": "dumpfile", "global_property_types": PropertyType.PT_char1024, "addr": global_dumpfile, "access": PropertyAccess.PA_PUBLIC,
     "description": "dump input_code_filename"},
    {"name": "savefile", "global_property_types": PropertyType.PT_char1024, "addr": global_savefile, "access": PropertyAccess.PA_PUBLIC,
     "description": "save input_code_filename"},
    {"name": "dumpall", "global_property_types": PropertyType.PT_bool, "addr": global_dumpall, "access": PropertyAccess.PA_PUBLIC,
     "description": "dumpall enable flag"},
    {"name": "runchecks", "global_property_types": PropertyType.PT_bool, "addr": global_runchecks, "access": PropertyAccess.PA_PUBLIC,
     "description": "runchecks enable flag"},
    {"name": "threadcount", "global_property_types": PropertyType.PT_int32, "addr": global_thread_count,
     "access": PropertyAccess.PA_PUBLIC, "description": "number of threads to use while using multicore"},
    {"name": "profiler", "global_property_types": PropertyType.PT_bool, "addr": global_profiler, "access": PropertyAccess.PA_PUBLIC,
     "description": "profiler enable flag"},
    {"name": "pauseatexit", "global_property_types": PropertyType.PT_bool, "addr": global_pauseatexit,
     "access": PropertyAccess.PA_PUBLIC, "description": "pause at exit flag"},
    {"name": "testoutputfile", "global_property_types": PropertyType.PT_char1024, "addr": global_testoutputfile,
     "access": PropertyAccess.PA_PUBLIC, "description": "input_code_filename for test output"},
    {"name": "xml_encoding", "global_property_types": PropertyType.PT_int32, "addr": global_xml_encoding,
     "access": PropertyAccess.PA_PUBLIC, "description": "XML data encoding"},
    {"name": "clock", "global_property_types": PropertyType.PT_timestamp, "addr": global_clock, "access": PropertyAccess.PA_PUBLIC,
     "description": "global clock"},
    {"name": "starttime", "global_property_types": PropertyType.PT_timestamp, "addr": global_start_time,
     "access": PropertyAccess.PA_PUBLIC, "description": "simulation start time"},
    {"name": "stoptime", "global_property_types": PropertyType.PT_timestamp, "addr": global_stop_time,
     "access": PropertyAccess.PA_PUBLIC, "description": "simulation stop time"},
    {"name": "double_format", "global_property_types": PropertyType.PT_char32, "addr": global_double_format,
     "access": PropertyAccess.PA_PUBLIC, "description": "format for writing double values"},
    {"name": "complex_format", "global_property_types": PropertyType.PT_char256, "addr": global_complex_format,
     "access": PropertyAccess.PA_PUBLIC, "description": "format for writing complex values"},
    {"name": "complex_output_format", "global_property_types": PropertyType.PT_enumeration, "addr": global_complex_output_format,
     "access": PropertyAccess.PA_PUBLIC, "description": "complex output representation", "enum_keys": cnf_keys},
    {"name": "object_format", "global_property_types": PropertyType.PT_char32, "addr": global_object_format,
     "access": PropertyAccess.PA_PUBLIC, "description": "format for writing anonymous object names"},
    {"name": "object_scan", "global_property_types": PropertyType.PT_char32, "addr": global_object_scan,
     "access": PropertyAccess.PA_PUBLIC, "description": "format for reading anonymous object names"},
    {"name": "object_tree_balance", "global_property_types": PropertyType.PT_bool, "addr": global_no_balance,
     "access": PropertyAccess.PA_PUBLIC, "description": "object index tree balancing enable flag"},
    {"name": "kmlfile", "global_property_types": PropertyType.PT_char1024, "addr": global_kmlfile, "access": PropertyAccess.PA_PUBLIC,
     "description": "KML output file name"},
    {"name": "modelname", "global_property_types": PropertyType.PT_char1024, "addr": global_modelname,
     "access": PropertyAccess.PA_REFERENCE, "description": "model name"},
    {"name": "execdir", "global_property_types": PropertyType.PT_char1024, "addr": global_execdir, "access": PropertyAccess.PA_REFERENCE,
     "description": "directory where executable binary was found"},
    {"name": "strictnames", "global_property_types": PropertyType.PT_bool, "addr": global_strictnames,
     "access": PropertyAccess.PA_PUBLIC, "description": "strict global name enable flag"},
    {"name": "website", "global_property_types": PropertyType.PT_char1024, "addr": global_urlbase, "access": PropertyAccess.PA_PUBLIC,
     "description": "url base string (deprecated)"},  # @todo deprecate use of 'website'
    {"name": "urlbase", "global_property_types": PropertyType.PT_char1024, "addr": global_urlbase, "access": PropertyAccess.PA_PUBLIC,
     "description": "url base string"},
    {"name": "randomseed", "global_property_types": PropertyType.PT_int32, "addr": global_randomseed, "access": PropertyAccess.PA_PUBLIC,
     "description": "random number generator seed value", "enum_keys": None, "enum_function": random_init},
    {"name": "include", "global_property_types": PropertyType.PT_char1024, "addr": global_include, "access": PropertyAccess.PA_REFERENCE,
     "description": "include folder path"},
    {"name": "trace", "global_property_types": PropertyType.PT_char1024, "addr": global_trace, "access": PropertyAccess.PA_PUBLIC,
     "description": "trace function list"},
    {"name": "gdb_window", "global_property_types": PropertyType.PT_bool, "addr": global_gdb_window, "access": PropertyAccess.PA_PUBLIC,
     "description": "gdb window enable flag"},
    {"name": "tmp", "global_property_types": PropertyType.PT_char1024, "addr": global_tmp, "access": PropertyAccess.PA_PUBLIC,
     "description": "temporary folder name"},
    {"name": "force_compile", "global_property_types": PropertyType.PT_int32, "addr": global_force_compile,
     "access": PropertyAccess.PA_PUBLIC, "description": "force recompile enable flag"},
    {"name": "nolocks", "global_property_types": PropertyType.PT_bool, "addr": global_nolocks, "access": PropertyAccess.PA_PUBLIC,
     "description": "locking disable flag"},
    {"name": "skipsafe", "global_property_types": PropertyType.PT_bool, "addr": global_skipsafe, "access": PropertyAccess.PA_PUBLIC,
     "description": "skip sync safe enable flag"},
    {"name": "dateformat", "global_property_types": PropertyType.PT_enumeration, "addr": global_dateformat,
     "access": PropertyAccess.PA_PUBLIC, "description": "date format string", "enum_keys": df_keys},
    {"name": "init_sequence", "global_property_types": PropertyType.PT_enumeration, "addr": global_init_sequence,
     "access": PropertyAccess.PA_PUBLIC, "description": "initialization sequence control flag", "enum_keys": isc_keys},
    {"name": "minimum_timestep", "global_property_types": PropertyType.PT_int32, "addr": global_minimum_timestep,
     "access": PropertyAccess.PA_PUBLIC, "description": "minimum timestep"},
    {"name": "platform", "global_property_types": PropertyType.PT_char8, "addr": global_platform, "access": PropertyAccess.PA_REFERENCE,
     "description": "operating platform"},
    {"name": "suppress_repeat_messages", "global_property_types": PropertyType.PT_bool, "addr": global_suppress_repeat_messages,
     "access": PropertyAccess.PA_PUBLIC, "description": "suppress repeated messages enable flag"},
    {"name": "maximum_synctime", "global_property_types": PropertyType.PT_int32, "addr": global_maximum_synctime,
     "access": PropertyAccess.PA_PUBLIC, "description": "maximum sync time for deltamode"},
    {"name": "run_realtime", "global_property_types": PropertyType.PT_bool, "addr": global_run_realtime,
     "access": PropertyAccess.PA_PUBLIC, "description": "realtime enable flag"},
    {"name": "enter_realtime", "global_property_types": PropertyType.PT_timestamp, "addr": global_enter_realtime,
     "access": PropertyAccess.PA_PUBLIC, "description": "timestamp to transition to realtime mode"},
    {"name": "realtime_metric", "global_property_types": PropertyType.PT_double, "addr": global_realtime_metric,
     "access": PropertyAccess.PA_REFERENCE, "description": "realtime performance metric (0=worst, 1=best)"},
    {"name": "no_deprecate", "global_property_types": PropertyType.PT_bool, "addr": global_suppress_deprecated_messages,
     "access": PropertyAccess.PA_PUBLIC, "description": "suppress deprecated usage message enable flag"},
]

global_map += [
    {"name": "sync_dumpfile", "global_property_types": PropertyType.PT_char1024, "addr": global_sync_dumpfile,
     "access": PropertyAccess.PA_PUBLIC, "description": "sync event dump file name"},
    {"name": "streaming_io", "global_property_types": PropertyType.PT_bool, "addr": global_streaming_io_enabled,
     "access": PropertyAccess.PA_PROTECTED, "description": "streaming I/O enable flag"},
    {"name": "compileonly", "global_property_types": PropertyType.PT_bool, "addr": global_compileonly,
     "access": PropertyAccess.PA_PROTECTED, "description": "compile only enable flag"},
    {"name": "relax_naming_rules", "global_property_types": PropertyType.PT_bool, "addr": global_relax_naming_rules,
     "access": PropertyAccess.PA_PUBLIC, "description": "relax object naming rules enable flag"},
    {"name": "browser", "global_property_types": PropertyType.PT_char1024, "addr": global_browser, "access": PropertyAccess.PA_PUBLIC,
     "description": "browser selection"},
    {"name": "server_portnum", "global_property_types": PropertyType.PT_int32, "addr": global_server_port_num,
     "access": PropertyAccess.PA_PUBLIC,
     "description": "server port number (default is find first open starting at 6267)"},
    {"name": "server_quit_on_close", "global_property_types": PropertyType.PT_bool, "addr": global_server_quit_on_close,
     "access": PropertyAccess.PA_PUBLIC, "description": "server quit on connection closed enable flag"},
    {"name": "client_allowed", "global_property_types": PropertyType.PT_char1024, "addr": global_client_allowed,
     "access": PropertyAccess.PA_PUBLIC, "description": "clients from which to accept connections"},
    {"name": "autoclean", "global_property_types": PropertyType.PT_bool, "addr": global_autoclean, "access": PropertyAccess.PA_PUBLIC,
     "description": "autoclean enable flag"},
    {"name": "technology_readiness_level", "global_property_types": PropertyType.PT_enumeration, "addr": technology_readiness_level,
     "access": PropertyAccess.PA_PUBLIC, "description": "technology readiness level", "enum_keys": trl_keys},
    {"name": "show_progress", "global_property_types": PropertyType.PT_bool, "addr": global_show_progress,
     "access": PropertyAccess.PA_PUBLIC, "description": "show progress enable flag"},
    {"name": "checkpoint_type", "global_property_types": PropertyType.PT_enumeration, "addr": global_checkpoint_type,
     "access": PropertyAccess.PA_PUBLIC, "description": "checkpoint global_property_types usage flag", "enum_keys": cpt_keys},
    {"name": "checkpoint_file", "global_property_types": PropertyType.PT_char1024, "addr": global_checkpoint_file,
     "access": PropertyAccess.PA_PUBLIC, "description": "checkpoint file base name"},
    {"name": "checkpoint_seqnum", "global_property_types": PropertyType.PT_int32, "addr": global_checkpoint_seqnum,
     "access": PropertyAccess.PA_PUBLIC, "description": "checkpoint sequence number"},
    {"name": "checkpoint_interval", "global_property_types": PropertyType.PT_int32, "addr": global_checkpoint_interval,
     "access": PropertyAccess.PA_PUBLIC, "description": "checkpoint interval"},
    {"name": "checkpoint_keepall", "global_property_types": PropertyType.PT_bool, "addr": global_checkpoint_keepall,
     "access": PropertyAccess.PA_PUBLIC, "description": "checkpoint file keep enable flag"},
    {"name": "check_version", "global_property_types": PropertyType.PT_bool, "addr": global_check_version,
     "access": PropertyAccess.PA_PUBLIC, "description": "check version enable flag"},
    {"name": "random_number_generator", "global_property_types": PropertyType.PT_enumeration, "addr": global_randomnumbergenerator,
     "access": PropertyAccess.PA_PUBLIC, "description": "random number generator version control flag",
     "enum_keys": rng_keys},
    {"name": "mainloop_state", "global_property_types": PropertyType.PT_enumeration, "addr": global_mainloopstate,
     "access": PropertyAccess.PA_PUBLIC, "description": "main sync loop state flag", "enum_keys": mls_keys},
    {"name": "pauseat", "global_property_types": PropertyType.PT_timestamp, "addr": global_mainlooppauseat,
     "access": PropertyAccess.PA_PUBLIC, "description": "pause at time"},
    {"name": "infourl", "global_property_types": PropertyType.PT_char1024, "addr": global_infourl, "access": PropertyAccess.PA_PUBLIC,
     "description": "URL to use for obtaining online help"},
    {"name": "hostname", "global_property_types": PropertyType.PT_char1024, "addr": global_hostname, "access": PropertyAccess.PA_PUBLIC,
     "description": "unused"},
    {"name": "hostaddr", "global_property_types": PropertyType.PT_char32, "addr": global_hostaddr, "access": PropertyAccess.PA_PUBLIC,
     "description": "unused"},
    {"name": "autostart_gui", "global_property_types": PropertyType.PT_bool, "addr": global_autostartgui,
     "access": PropertyAccess.PA_PUBLIC, "description": "automatic GUI start enable flag"},
    {"name": "master", "global_property_types": PropertyType.PT_char1024, "addr": global_master, "access": PropertyAccess.PA_PUBLIC,
     "description": "master server hostname"},
    {"name": "master_port", "global_property_types": PropertyType.PT_int64, "addr": global_master_port,
     "access": PropertyAccess.PA_PUBLIC, "description": "master server port number"},
    {"name": "multirun_mode", "global_property_types": PropertyType.PT_enumeration, "addr": global_multirun_mode,
     "access": PropertyAccess.PA_PUBLIC, "description": "multirun enable flag", "enum_keys": mrm_keys},
    {"name": "multirun_conn", "global_property_types": PropertyType.PT_enumeration, "addr": global_multirun_connection,
     "access": PropertyAccess.PA_PUBLIC, "description": "unused", "enum_keys": mrc_keys},
    {"name": "signal_timeout", "global_property_types": PropertyType.PT_int32, "addr": global_signal_timeout,
     "access": PropertyAccess.PA_PUBLIC, "description": "unused"},
    {"name": "slave_port", "global_property_types": PropertyType.PT_int16, "addr": global_slave_port, "access": PropertyAccess.PA_PUBLIC,
     "description": "unused"},
    {"name": "slave_id", "global_property_types": PropertyType.PT_int64, "addr": global_slave_id, "access": PropertyAccess.PA_PUBLIC,
     "description": "unused"},
    {"name": "return_code", "global_property_types": PropertyType.PT_int32, "addr": global_return_code,
     "access": PropertyAccess.PA_REFERENCE, "description": "unused"},
    {"name": "exit_code", "global_property_types": PropertyType.PT_int16, "addr": global_exit_code,
     "access": PropertyAccess.PA_REFERENCE, "description": "The exit code for GridLAB-D"},
    {"name": "module_compiler_flags", "global_property_types": PropertyType.PT_set, "addr": global_module_compiler_flags,
     "access": PropertyAccess.PA_PUBLIC, "description": "module compiler flags", "enum_keys": mcf_keys},
    {"name": "init_max_defer", "global_property_types": PropertyType.PT_int32, "addr": global_init_max_defer,
     "access": PropertyAccess.PA_REFERENCE, "description": "deferred initialization limit"},
    {"name": "mt_analysis", "global_property_types": PropertyType.PT_bool, "addr": global_mt_analysis,
     "access": PropertyAccess.PA_PUBLIC, "description": "perform multithread profile optimization analysis"},
    {"name": "inline_block_size", "global_property_types": PropertyType.PT_int32, "addr": global_inline_block_size,
     "access": PropertyAccess.PA_PUBLIC, "description": "inline code block size"},
    {"name": "validate", "global_property_types": PropertyType.PT_set, "addr": global_validate_options,
     "access": PropertyAccess.PA_PUBLIC, "description": "validation test options", "enum_keys": vo_keys},
    {"name": "sanitize", "global_property_types": PropertyType.PT_set, "addr": global_sanitize_options,
     "access": PropertyAccess.PA_PUBLIC, "description": "sanitize process options", "enum_keys": so_keys},
    {"name": "sanitize_prefix", "global_property_types": PropertyType.PT_char8, "addr": global_sanitize_prefix,
     "access": PropertyAccess.PA_PUBLIC, "description": "sanitized name prefix"},
    {"name": "sanitize_index", "global_property_types": PropertyType.PT_char1024, "addr": global_sanitize_index,
     "access": PropertyAccess.PA_PUBLIC, "description": "sanitization index file spec"},
    {"name": "sanitize_offset", "global_property_types": PropertyType.PT_char32, "addr": global_sanitize_offset,
     "access": PropertyAccess.PA_PUBLIC, "description": "sanitization lat/lon offset"},
    {"name": "simulation_mode", "global_property_types": PropertyType.PT_enumeration, "addr": global_simulation_mode,
     "access": PropertyAccess.PA_PUBLIC, "description": "current time simulation global_property_types", "enum_keys": sm_keys},
    {"name": "deltamode_timestep", "global_property_types": PropertyType.PT_double, "addr": global_deltamode_timestep_pub,
     "access": PropertyAccess.PA_PUBLIC, "description": "uniform step size for deltamode simulations",
     "enum_keys": None, "enum_function": None, "enum_unit": "ns"},
    {"name": "deltamode_maximumtime", "global_property_types": PropertyType.PT_double, "addr": global_deltamode_maximumtime_pub,
     "access": PropertyAccess.PA_PUBLIC, "description": "maximum time (ns) deltamode can run", "enum_keys": None,
     "enum_function": None, "enum_unit": "ns"},
    {"name": "deltaclock", "global_property_types": PropertyType.PT_int64, "addr": global_deltaclock, "access": PropertyAccess.PA_PUBLIC,
     "description": "cumulative delta runtime with respect to the global clock"},
    {"name": "delta_current_clock", "global_property_types": PropertyType.PT_double, "addr": global_delta_curr_clock,
     "access": PropertyAccess.PA_PUBLIC, "description": "Absolute delta time (global clock offset)"},
    {"name": "deltamode_updateorder", "global_property_types": PropertyType.PT_char1024, "addr": global_deltamode_updateorder,
     "access": PropertyAccess.PA_REFERENCE, "description": "order in which modules are updated in deltamode"},
    {"name": "deltamode_iteration_limit", "global_property_types": PropertyType.PT_int32, "addr": global_deltamode_iteration_limit,
     "access": PropertyAccess.PA_PUBLIC,
     "description": "iteration limit for each delta timestep (object and interupdate)"},
    {"name": "deltamode_forced_extra_timesteps", "global_property_types": PropertyType.PT_int32,
     "addr": global_deltamode_forced_extra_timesteps, "access": PropertyAccess.PA_PUBLIC,
     "description": "forced extra deltamode timesteps before returning to event-driven mode"},
    {"name": "deltamode_forced_always", "global_property_types": PropertyType.PT_bool, "addr": global_deltamode_forced_always,
     "access": PropertyAccess.PA_PUBLIC, "description": "forced deltamode for debugging -- prevents event-driven mode"},
    {"name": "deltamode_preferred_module_order", "global_property_types": PropertyType.PT_bool,
     "addr": global_deltamode_force_preferred_order, "access": PropertyAccess.PA_PUBLIC,
     "description": "sets execution order for deltamode, as opposed to GLM order"},
    {"name": "run_powerworld", "global_property_types": PropertyType.PT_bool, "addr": global_run_power_world,
     "access": PropertyAccess.PA_PUBLIC,
     "description": "boolean that says your system is set up correctly to run with PowerWorld"},
    {"name": "bigranks", "global_property_types": PropertyType.PT_bool, "addr": global_bigranks, "access": PropertyAccess.PA_PUBLIC,
     "description": "enable fast/blind set_rank operations"},
    {"name": "exename", "global_property_types": PropertyType.PT_char1024, "addr": global_execname,
     "access": PropertyAccess.PA_REFERENCE, "description": "argv[0] value"},
    {"name": "wget_options", "global_property_types": PropertyType.PT_char1024, "addr": global_wget_options,
     "access": PropertyAccess.PA_PUBLIC, "description": "wget options"},
    {"name": "svnroot", "global_property_types": PropertyType.PT_char1024, "addr": global_svn_root, "access": PropertyAccess.PA_PUBLIC,
     "description": "svnroot"},
    {"name": "allow_reinclude", "global_property_types": PropertyType.PT_bool, "addr": global_reinclude,
     "access": PropertyAccess.PA_PUBLIC, "description": "allow the same include file to be included multiple times"},
]

global_randomnumbergenerator = RANDOMNUMBERGENERATOR.RNG2
