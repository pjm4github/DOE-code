# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
import subprocess
from datetime import datetime

import os

from enum import IntEnum
from socket import socket
from sys import platform
from typing import List, Dict
import threading

import select

from gov_pnnl_goss.gridlab.climate.CsvReader import TIMESTAMP
from gov_pnnl_goss.gridlab.gldcore.Globals import XC_SUCCESS, XC_EXFAILED, XC_ARGERR, XC_ENVERR, \
    XC_TSTERR, XC_USRERR, XC_RUNERR, XC_INIERR, XC_PRCERR, XC_SVRKLL, XC_IOERR, \
    XC_SHFAILED, XC_SIGNAL, XC_SIGINT, XC_EXCEPTION, global_init, FAILED, SUCCESS
from gov_pnnl_goss.gridlab.gldcore.GridLabD import convert_from_timestamp, TS_NEVER, TS_INVALID

from gov_pnnl_goss.gridlab.gldcore.Output import output_warning, output_debug, output_verbose, output_progress, \
    output_error, output_message, output_fatal
from gov_pnnl_goss.gridlab.gldcore.local1702152845 import locale_push
from gov_pnnl_goss.gridlab.gldcore.realtime1702152845 import realtime_now
from gov_pnnl_goss.gridlab.gldcore.threadpool1702152845 import processor_count

mls_svr_lock = threading.Lock()
mls_svr_signal = threading.Condition(mls_svr_lock)


from cpp_threadpool import CppThreadPool  # Assuming you have a suitable implementation for cpp_threadpool

import time
from enum import Enum

startlock = []  # List of mutexes
donelock = []   # List of mutexes

start = []  # List of condition variables
done = []   # List of condition variables

next_t1 = [0]  # List with a single integer element
donecount = [0]  # List with a single integer element
n_threads = [0]  # List with a single integer element

class PASSCONFIG(Enum):
    PC_PRETOPDOWN = 0
    PC_BOTTOMUP = 1
    PC_POSTTOPDOWN = 2

class arg_data:
    def __init__(self, thread, item, incr):
        self.thread = thread
        self.item = item
        self.incr = incr
ArgData = arg_data

class ListItem:
    def __init__(self, data):
        self.data = data
        self.next = None

# Initialize clock variables
cstart = None
cend = None

# Define constants
_MAX_PATH = 1024


# Constants
OF_INIT = 1
OF_DEFERRED = 2

# Define macros
def PASSINIT(p):
    return ranks[p].first_used if p % 2 else ranks[p].last_used

def PASSCMP(i, p):
    return i <= ranks[p].last_used if p % 2 else i >= ranks[p].first_used

def PASSINC(p):
    return 1 if p % 2 else -1

# Initialize variables
# thread_data = None
# threadpool_data = None
ranks = None

# Define passtype as a list of PASSCONFIG values
passtype = [PASSCONFIG.PC_PRETOPDOWN, PASSCONFIG.PC_BOTTOMUP, PASSCONFIG.PC_POSTTOPDOWN]

# Initialize pass counter
pass_ = 0

# Initialize iteration counters
iteration_counter = 0
federation_iteration_counter = 0

# Define lock-related variables (if needed)
rlock_count = 0
rlock_spin = 0
wlock_count = 0
wlock_spin = 0

# Define pthread_create arguments
arg_data_array = [arg_data(thread=0, item=None, incr=0), arg_data(thread=1, item=None, incr=0)]

# Define external mutex and condition variables (if needed)
mls_inst_lock = threading.Lock()
mls_inst_signal = threading.Condition()

object_heartbeats = None
n_object_heartbeats = 0
max_object_heartbeats = 0


script_exports = None
create_scripts = None
init_scripts = None
sync_scripts = None
term_scripts = None

class STATUS(Enum):
    UNINITIALIZED = 0
    INITIALIZED = 1
    RUNNING = 2
    STOPPED = 3
    FAILED = FAILED
    SUCCESS = SUCCESS

class SimpleLinkList:
    def __init__(self, data):
        self.data = data
        self.next = None

class EXITCODE(IntEnum):
    OK = 0
    ERROR = 1

class INDEX:
    @staticmethod
    def create(start, end):
        return {'start': start, 'end': end, 'objects': []}

    @staticmethod
    def insert(index, obj, rank):
        if index is None:
            return STATUS.FAILED

        index['objects'].append({'object': obj, 'rank': rank})
        return STATUS.SUCCESS

class sync_data:
    def __init__(self):
        self.step_to = 0  # Initialize appropriately
        self.hard_event = 0  # Initialize appropriately
        self.status = STATUS.UNINITIALIZED

SyncData = sync_data

class ThreadData:
    def __init__(self):
        self.count = 0  # Initialize appropriately
        self.data = None  # Initialize appropriately

class threadpool_thread_data:
    def __init__(self, size: int, threadpool: CppThreadPool):
        self.count = size
        self.data = [sync_data() for _ in range(size)]
        self.thread_map = {}  # = threadpool.get_threadmap() # Use a dictionary to map thread IDs to indices
        # for index in range(size):
        #     self.data[index].status = SUCCESS
        self.initialize_thread_map(threadpool)

    def initialize_thread_map(self, threadpool: CppThreadPool):
        for idx, thread_id in enumerate(threadpool.get_thread_ids()):
            self.thread_map[thread_id] = idx

    def get_thread_data(self, thread_id: threading.Thread):
        idx = self.thread_map.get(thread_id)
        return self.data[idx] if idx is not None else None

    def get_data(self, index: int):
        return self.data[index]

class CheckpointType:
    WALL = 1
    SIM = 2
    NONE = 3

class Object:
    def __init__(self, flags, lock, in_svc, in_svc_micro, out_svc, oclass, name=None):
        self.in_svc = in_svc
        self.in_svc_micro = in_svc_micro
        self.out_svc = out_svc
        self.oclass = oclass
        self.name = name
        self.flags = flags
        self.lock = lock
        self.next = None
        self.oclass = None
        self.id = None

OBJECT = Object

class OClass:
    def __init__(self, name):
        self.name = name

OBJECT_CLASS = OClass

class OBJSYNCDATA:
    def __init__(self):
        self.n = 0  # thread id 0~n_threads for this object rank list
        self.pt = None
        self.ok = False
        self.ls = None  # Assuming LISTITEM is a valid class or struct in your Python code
        self.nObj = 0  # number of obj in this object rank list
        self.t0 = 0
        self.i = 0  # index of mutex or cond this object rank list uses


class MyClass:
    def __init__(self):
        self.profiler = Profiler()

class Profiler:
    def __init__(self):
        self.clocks = 0

class DeltaProfile:
    def __init__(self):
        self.t_count = 0
        self.t_preupdate = 0
        self.t_update = 0
        self.t_postupdate = 0
        self.t_delta = 0

def delta_getprofile():
    return DeltaProfile()

# Global variables
global_checkpoint_type = CheckpointType.WALL
global_clock = 0
global_minimum_timestep = 1
global_modelname = ""
global_checkpoint_seqnum = 0
global_checkpoint_keepall = 0
global_checkpoint_file = ""
global_debug_mode = 0
global_nolocks = 0
global_checkpoint_interval = 3600
global_sync_dumpfile = ""  # Provide the file path for debug purposes

from enum import Enum

class STATUS(Enum):
    SUCCESS = 0
    FAILED = -1

# class TIMESTAMP:
#     TS_NEVER = float('inf')
#     TS_INVALID = float('-inf')

class TRANSFORMSOURCE(Enum):
    XS_DOUBLE = 1
    XS_COMPLEX = 2
    XS_ENDUSE = 4

class sync_data:
    def __init__(self):
        self.step_to = TIMESTAMP.TS_NEVER
        self.step_num = 0
        self.status = STATUS.SUCCESS


class LISTITEM:
    def __init__(self):
        self.data = None
        self.next = None



def t_setup_ranks():
    return setup_ranks()  # Define setup_ranks as needed


def sim_time():
    buffer = bytearray(64)
    result, buffer = convert_from_timestamp(global_clock, buffer, len(buffer))
    return buffer.decode() if result > 0 else "(invalid)"

########################################################################

def object_name(obj, b=None, max_len = None):
    return f"{obj.oclass.name}:{obj.id}"


# Simulate the stream function for demonstration purposes
def stream(fp, mode):
    if mode == SF_OUT:
        fp.write("Sample checkpoint data\n")
        return len("Sample checkpoint data\n")
    return 0


def stream_context():
    return "Stream context"


def iter_objects():
    PC_FORCE_NAME = 1
    # Simulate iterating over objects
    obj1 = Object(OClass("Class1", PC_FORCE_NAME), 1, "Object1")
    obj2 = Object(OClass("Class2", 0), 2, "Object2")
    obj3 = Object(OClass("Class3", PC_FORCE_NAME), 3, "")
    return [obj1, obj2, obj3]


# Helper function to get thread-specific data
def get_thread_data(thread_id):
    if thread_id not in threadpool_data:
        threadpool_data[thread_id] = SyncData()
    return threadpool_data[thread_id]


# Simulated functions for demonstration purposes
def object_sync(obj, clock, passtype):
    return clock


def exec_setexitcode(code: EXITCODE) -> EXITCODE:
    global global_exit_code
    # Implement exec_setexitcode logic here and return an EXITCODE
    oldxc = global_exit_code
    if oldxc!=XC_SUCCESS:
        output_warning("new exitcode %d overwrites existing exitcode %d", code, oldxc)
    global_exit_code = code
    output_debug("exit code %d", code)
    return oldxc
#
# def exec_set_exit_code(xc):
#     global global_exit_code
#     old_xc = global_exit_code
#     if old_xc != XC_SUCCESS:
#         output_warning("new exitcode %d overwrites existing exitcode %d" % (xc, old_xc))
#     global_exit_code = xc
#     output_debug("exit code %d" % xc)
#     return old_xc

def exec_getexitcode() -> EXITCODE:
    global global_exit_code
    # Implement exec_getexitcode logic here and return an EXITCODE
    return global_exit_code

# def exec_get_exit_code():
#     global global_exit_code
#     return global_exit_code


def exec_get_exit_code_str(xc: EXITCODE):
    exit_code_strings = {
        XC_SUCCESS: "ok",
        XC_EXFAILED: "exec/wait failed",
        XC_ARGERR: "bad command",
        XC_ENVERR: "environment startup/load failed",
        XC_TSTERR: "test failed",
        XC_USRERR: "user rejected license terms",
        XC_RUNERR: "simulation failed",
        XC_INIERR: "initialization failed",
        XC_PRCERR: "process control error",
        XC_SVRKLL: "server killed",
        XC_IOERR: "I/O error",
        XC_SHFAILED: "shell failed",
        XC_SIGNAL: "signal caught",
        XC_SIGINT: "interrupt received",
        XC_EXCEPTION: "exception caught"
    }
    return exit_code_strings.get(xc, "unknown exception")

def exec_clock():
    global initialized
    if 'initialized' not in globals():
        globals()['nt1'] = time.time()
        globals()['nt2'] = globals()['nt1']
        globals()['initialized'] = True
    else:
        globals()['nt2'] = time.time()
    return (globals()['nt2'] - globals()['nt1']) * 1000000

# def exec_clock():
#     if not hasattr(exec_clock, 'initialized'):
#         exec_clock.nt1 = time.time()
#         exec_clock.nt2 = exec_clock.nt1
#         exec_clock.initialized = True
#     else:
#         exec_clock.nt2 = time.time()
#     return int((exec_clock.nt2 - exec_clock.nt1) * 1000000)


def exec_init():
    global glpathlen, global_threadcount, global_starttime
    glpathlen = 0

    if global_threadcount == 0:
        global_threadcount = processor_count()
    output_verbose("detected %d processor(s)" % processor_count())
    output_verbose("using %d helper thread(s)" % global_threadcount)

    if global_starttime == 0:
        global_starttime = realtime_now()

    global_clock = global_starttime

    locale_push()

    if global_init() == FAILED:
        return 0
    return 1


def exec_get_ranks():
    return ranks


def object_get_first():
    pass  # Implement object_get_first logic

def object_get_next(obj):
    pass  # Implement object_get_next logic

def index_shuffle(index):
    pass  # Implement index_shuffle logic

def setup_ranks():
    """
    # Example usage:
        result = setup_ranks()
        if result == STATUS.SUCCESS:
            print("Ranks setup successfully.")
        else:
            print("Failed to setup ranks.")
    :return:
    """
    global ranks
    obj = None
    i = 0

    # Create index objects
    ranks = [INDEX.create(0, 10), INDEX.create(0, 10), INDEX.create(0, 10)]

    # Build the ranks of each pass type
    for i in range(len(passtype)):
        if ranks[i] is None:
            return STATUS.FAILED

        # Add every object to index based on rank
        obj = object_get_first()
        while obj is not None:
            # Ignore objects that don't use this passconfig
            if (obj['oclass']['passconfig'] & passtype[i].value) == 0:
                obj = object_get_next(obj)
                continue

            # Add this object to the ranks for this passconfig
            if INDEX.insert(ranks[i], obj, obj['rank']) == STATUS.FAILED:
                return STATUS.FAILED
            # sjin: print out obj id, pass, rank information
            # else:
            #     print("obj[{}]: pass = {}, rank = {}".format(obj['id'], passtype[i], obj['rank']))

            obj = object_get_next(obj)

        if global_debug_mode == 0 and global_nolocks == 0:
            # Shuffle the objects in the index
            index_shuffle(ranks[i])

    return STATUS.SUCCESS


def simtime() -> str:
    # Implement simtime logic here and return a string
    buffer = convert_from_timestamp(global_clock)
    return  buffer if len(buffer) > 0 else "(invalid)"


def show_progress():
    global wait_status
    wait_status = extern_gui_action_status()
    output_progress()

    realtime_schedule_event(realtime_now() + 1, show_progress)
    return SUCCESS

# /***********************************************************************/
# /* CHECKPOINTS (DPC Apr 2011) */


def do_checkpoint():
    """
    # Example usage:
        global_modelname = "MyModel"
        global_clock = int(time.time())
        do_checkpoint()

    :return:
    """
    # Last checkpoint value
    global last_checkpoint, global_checkpoint_interval
    if 'last_checkpoint' not in globals():
        last_checkpoint = 0

    # Checkpoint type selection
    now = 0

    if global_checkpoint_type == CheckpointType.WALL:
        # Checkpoint based on wall time
        now = int(time.time())

        # Default checkpoint interval for WALL
        if global_checkpoint_interval == 0:
            global_checkpoint_interval = 3600

    elif global_checkpoint_type == CheckpointType.SIM:
        # Checkpoint based on sim time
        now = global_clock

        # Default checkpoint interval for SIM
        if global_checkpoint_interval == 0:
            global_checkpoint_interval = 86400

    elif global_checkpoint_type == CheckpointType.NONE:
        now = 0

    # Checkpoint may be needed
    if now > 0:
        # Initial value of last checkpoint
        if last_checkpoint == 0:
            last_checkpoint = now

        # Checkpoint time elapsed
        if last_checkpoint + global_checkpoint_interval <= now:
            fn = ""

            # Default checkpoint filename
            if global_checkpoint_file == "":
                ext = None

                # Use the model name by default
                global_checkpoint_file = global_modelname
                ext = os.path.splitext(global_checkpoint_file)

                # Trim off the extension, if any
                if ext and (ext[1] == ".glm" or ext[1] == ".xml"):
                    global_checkpoint_file = ext[0]

            # Delete old checkpoint file if not desired
            if not global_checkpoint_keepall and fn != "":
                os.remove(fn)

            # Create current checkpoint save filename
            fn = f"{global_checkpoint_file}.{global_checkpoint_seqnum}"
            global_checkpoint_seqnum += 1
            try:
                with open(fn, "w") as fp:
                    if not stream(fp, SF_OUT):
                        output_error(f"checkpoint failure (stream context is {stream_context()})")
                    last_checkpoint = now
            except Exception as e:
                output_error(f"unable to open checkpoint file '{fn}' for writing: {e}")


def tp_do_object_sync(obj):
    """
    # Example usage:
        oclass = OClass("MyObjectClass")
        obj = Object(10, 0, 100, oclass)
        global_clock = 50
        passstype = [1, 2, 3]  # Replace with actual passtype values
        pass = 0  # Replace with the desired pass value
        tp_do_object_sync(obj)

    :param obj:
    :return:
    """
    thread_id = threading.get_ident()
    data = get_thread_data(thread_id)
    this_t = 0

    # Check in and out-of-service dates
    if global_clock < obj.in_svc:
        this_t = obj.in_svc  # Yet to go in service
    elif global_clock == obj.in_svc and obj.in_svc_micro != 0:
        this_t = obj.in_svc + 1  # Technically yet to go into service (deltamode handled separately)
    elif global_clock <= obj.out_svc:
        this_t = object_sync(obj, global_clock, passtype[pass])
        if this_t == global_clock:
            print(f"{simtime()}: object {object_name(obj)} calling for re-sync")

    else:
        this_t = float("inf")  # Already out of service

    # Check for "soft" event (events that are ignored when stopping)
    if this_t < -1:
        this_t = abs(this_t)
    elif this_t != float("inf"):
        data.hard_event += 1  # This counts the number of hard events

    # Check for stopped clock
    if this_t < global_clock:
        print(f"{simtime()}: object {object_name(obj)} stopped its clock (exec)!")
        data.status = "FAILED"
    else:
        # Check for iteration limit approach
        if iteration_counter == 2 and this_t == global_clock:
            print(f"{simtime()}: object {object_name(obj)} iteration limit imminent")
        elif iteration_counter == 1 and this_t == global_clock:
            print(f"Convergence iteration limit reached for object {obj.oclass.name}:{obj.id}")

        # Manage minimum timestep
        if global_minimum_timestep > 1 and this_t > global_clock and this_t < float("inf"):
            this_t = ((this_t - 1) // global_minimum_timestep + 1) * global_minimum_timestep

        # If this event precedes next step, next step is now this event
        if data.step_to > this_t:
            data.step_to = this_t


def ss_do_object_sync(thread, item):
    """
    # Example usage:
        oclass = OClass("MyObjectClass")
        obj = Object(10, 0, 100, oclass)
        global_clock = 50
        passstype = [1, 2, 3]  # Replace with actual passtype values
        pass = 0  # Replace with the desired pass value
        thread_data = {"data": {}}
        ss_do_object_sync(0, obj)
    :param thread:
    :param item:
    :return:
    """
    global global_iteration_limit
    data = ThreadData.data[thread]
    obj = item
    this_t = 0

    # Check in and out-of-service dates
    if global_clock < obj.in_svc:
        this_t = obj.in_svc  # Yet to go in service
    elif global_clock == obj.in_svc and obj.in_svc_micro != 0:
        this_t = obj.in_svc + 1  # Technically yet to go into service (deltamode handled separately)
    elif global_clock <= obj.out_svc:
        this_t = object_sync(obj, global_clock, passtype[pass_])
        if this_t == global_clock:
            print(f"{simtime()}: object {object_name(obj)} calling for re-sync")

    else:
        this_t = float("inf")  # Already out of service

    # Check for "soft" event (events that are ignored when stopping)
    if this_t < -1:
        this_t = abs(this_t)
    elif this_t != float("inf"):
        data.hard_event += 1  # This counts the number of hard events

    # Check for stopped clock
    if this_t < global_clock:
        print(f"{simtime()}: object {object_name(obj)} stopped its clock (exec)!")
        data.status = "FAILED"
    else:
        # Check for iteration limit approach
        if iteration_counter == 2 and this_t == global_clock:
            print(f"{simtime()}: object {object_name(obj)} iteration limit imminent")
        elif iteration_counter == 1 and this_t == global_clock:
            print(f"Convergence iteration limit reached for object {obj.oclass.name}:{obj.id}")

        # Manage minimum timestep
        if global_minimum_timestep > 1 and this_t > global_clock and this_t < float("inf"):
            this_t = ((this_t - 1) // global_minimum_timestep + 1) * global_minimum_timestep

        # If this event precedes the next step, the next step is now this event
        if data.step_to > this_t:
            data.step_to = this_t

        # Debug dumpfile handling
        if global_sync_dumpfile:
            with open(global_sync_dumpfile, "a") as fp:
                if global_clock < obj.in_svc:
                    passname = "IN_SERVICE"
                elif global_clock <= obj.out_svc:
                    passname = "SYNC"
                else:
                    passname = "OUT_OF_SERVICE"

                objname = f"{obj.oclass.name}:{obj.id}" if obj.name is None else obj.name
                syncdate = abs(this_t)
                fp.write(f"{global_clock},{passname},{global_iteration_limit - iteration_counter},{thread},{objname},{syncdate}\n")

# # Helper function to get thread-specific data
# def get_thread_data(thread):
#     if thread not in thread_data.data:
#         thread_data.data[thread] = SyncData()
#     return thread_data.data[thread]
#
# # Simulated functions for demonstration purposes
# def object_sync(obj, clock, passtype):
#     return clock
#


def ss_do_object_sync_list(threadarg):
    """
    # Example usage:
        list_item1 = ListItem(1)
        list_item2 = ListItem(2)
        list_item3 = ListItem(3)
        list_item1.next = list_item2
        list_item2.next = list_item3

        arg_data = ArgData(1, list_item1, 2)
        ss_do_object_sync_list(arg_data)

    :param threadarg:
    :return:
    """
    mydata = threadarg
    thread = mydata.thread
    item = mydata.item
    incr = mydata.incr

    iPtr = 0
    ptr = item
    while ptr is not None:
        if iPtr < incr:
            ss_do_object_sync(thread, ptr.data)
            iPtr += 1
        ptr = ptr.next


def init_by_creation():
    """
    # Example usage:
        result = init_by_creation()
        if result == Status.SUCCESS:
            print("Initialization successful")
        else:
            print("Initialization failed")
    :return:
    """
    PC_FORCE_NAME = 1
    rv = SUCCESS

    try:
        for obj in iter_objects():
            if not object_init(obj):
                b = [0] * 64
                raise Exception(f"object {object_name(obj, b, 63)} initialization failed")

            if obj.oclass.passconfig & PC_FORCE_NAME == PC_FORCE_NAME:
                if obj.name == "":
                    output_warning(f"init: object {obj.oclass.name}:{obj.id} should have a name, but doesn't")

    except Exception as e:
        output_error(f"init failure: {e}")
        rv = FAILED

    return rv


def init_by_deferral_retry(def_array):
    ct = 0
    i = 0
    obj_rv = 0
    rv = SUCCESS
    b = [0] * 64
    retry = 1
    tries = 0
    exit_check = 0
    tarray = None

    # Split out the allocation so it can be checked
    next_arr = [None] * len(def_array)

    # Check it, like a proper programmer
    if next_arr is None:
        output_error("init_by_deferral_retry(): error allocating temporary array")
        return FAILED

    global_init_max_defer = 1  # Simulated global variable

    if global_init_max_defer < 1:
        output_warning("init_max_defer is less than 1, disabling deferred initialization")

    while retry:
        if global_init_max_defer <= tries:
            output_error("init_by_deferral_retry(): exhausted initialization attempts")
            rv = FAILED
            break

        # Zero the temp array AND its tracking variable
        next_arr = [None] * len(def_array)
        ct = 0

        # Initialize each object in def_array
        for i in range(len(def_array)):
            obj = def_array[i]
            obj_rv = object_init(obj)
            if obj_rv == 0:
                rv = FAILED
                output_error(f"init_by_deferral_retry(): object {object_name(obj, b, 63)} initialization failed")
            elif obj_rv == 1:
                with obj.lock.Lock():  # assumig obj.lock is a threading.lock type
                    obj.flags |= 1  # OF_INIT
                    obj.flags -= 2  # OF_DEFERRED
            elif obj_rv == 2:
                next_arr[ct] = obj
                ct += 1

            if rv == FAILED:
                next_arr = None
                return rv

        if ct == len(def_array):
            output_error("init_by_deferral_retry(): all uninitialized objects deferred, model is unable to initialize")
            rv = FAILED
            retry = 0

            # See which iteration we exited on - multi-swap messes up pointers alternatingly
            exit_check = tries % 2

            # Determine how to handle that iteration
            if exit_check == 1:
                # Yes - fix the pointers before leaving; otherwise, we'll double-free things!
                tarray = def_array
                def_array = next_arr
                next_arr = tarray
            # Default else - we failed on the first try, so pointer swap-around below didn't occur
        elif ct == 0:
            rv = SUCCESS
            retry = 0

            # See which iteration we exited on - multi-swap messes up pointers alternatingly
            exit_check = tries % 2

            # Determine how to handle that iteration
            if exit_check == 1:
                # Yes - fix the pointers before leaving; otherwise, we'll double-free things!
                tarray = def_array
                def_array = next_arr
                next_arr = tarray
            # Default else - we succeeded on the first try, so pointer swap-around below didn't occur
        else:
            tries += 1
            retry = 1
            tarray = next_arr
            next_arr = def_array
            def_array = tarray

    return rv



def init_by_deferral():
    """
    # Example usage:
        obj1 = Object(0, None)
        obj2 = Object(OF_DEFERRED, None)
        obj3 = Object(0, None)
        obj4 = Object(0, None)

        # Simulate linking the objects
        obj1.next = obj2
        obj2.next = obj3
        obj3.next = obj4

        result = init_by_deferral()
        if result == Status.SUCCESS:
            print("Initialization successful")
        else:
            print("Initialization failed")

    :return:
    """
    def_array = []
    obj = object_get_first()
    while obj:
        def_array.append(obj)
        obj = obj.next

    if not def_array:
        return SUCCESS

    rv = SUCCESS

    try:
        rv = init_by_deferral_retry(def_array, len(def_array))
        if rv == FAILED:
            return FAILED

        obj = object_get_first()
        while obj:
            if obj.oclass.passconfig & 4:  # PC_FORCE_NAME == 4
                if obj.name == "":
                    output_warning(f"init: object {obj.oclass.name}:{obj.id} should have a name, but doesn't")
            obj = obj.next

    except Exception as e:
        output_error(f"init_by_deferral(): {e}")
        rv = FAILED

    return rv


def init_all():
    """
    # Example usage:
        result = init_all()
        if result == Status.SUCCESS:
            print("Initialization successful")
        else:
            print("Initialization failed")
    :return:
    """
    objects = []

    # Simulate object creation with heartbeat values
    obj1 = Object(1)
    obj2 = Object(0)
    obj3 = Object(1)
    obj4 = Object(1)

    # Simulate linking the objects
    obj1.next = obj2
    obj2.next = obj3
    obj3.next = obj4

    output_verbose("initializing objects...")

    if instance_initall() == Status.FAILED:
        return Status.FAILED

    if loadshape_initall() == Status.FAILED or enduse_initall() == Status.FAILED:
        return Status.FAILED

    global_init_sequence = "IS_DEFERRED"  # Set the initialization mode

    if global_init_sequence == "IS_CREATION":
        rv = init_by_creation()
    elif global_init_sequence == "IS_DEFERRED":
        rv = init_by_deferral()
    elif global_init_sequence == "IS_BOTTOMUP":
        print("Bottom-up rank-based initialization mode not yet supported")
        return Status.FAILED
    elif global_init_sequence == "IS_TOPDOWN":
        print("Top-down rank-based initialization mode not yet supported")
        return Status.FAILED
    else:
        print("Unrecognized initialization mode")
        return Status.FAILED

    if rv == Status.FAILED:
        return Status.FAILED

    n_object_heartbeats = 0
    max_object_heartbeats = 0
    object_heartbeats = []

    for obj in objects:
        if obj.heartbeat > 0:
            if n_object_heartbeats >= max_object_heartbeats:
                size = max_object_heartbeats * 2 if max_object_heartbeats > 0 else 256
                bigger = [None] * size
                if max_object_heartbeats > 0:
                    bigger[:max_object_heartbeats] = object_heartbeats
                object_heartbeats = bigger
                max_object_heartbeats = size

            object_heartbeats[n_object_heartbeats] = obj
            n_object_heartbeats += 1

    return link_initall()

# def precommit(t0):
#     """
#     This callback function allows an object to perform actions at the beginning
#     of a timestep, before the sync process. This callback is only triggered
#     once per timestep, and will not fire between iterations.
#     """
#     pass  # Implement your precommit logic here


# /**************************************************************************
#  ** PRECOMMIT ITERATOR
#  **************************************************************************/
def precommit_all(t0):
    """
    This function performs precommit operations on all objects that have a precommit method.
    Args:
        t0 (TIMESTAMP): The timestamp at which precommit is executed.
    Returns:
        STATUS: SUCCESS if all precommit operations succeed, FAILED otherwise.
    """
    rv = SUCCESS
    first = True
    precommit_list = None

    if first:
        for obj in object_get_all():
            if obj.oclass.precommit is not None:
                item = SimpleLinkList(obj)
                if item is None:
                    name = object_name(obj)[:63]
                    output_error(f"object {name} precommit memory allocation failed")
                    return FAILED
                item.next = precommit_list
                precommit_list = item
        first = False

    try:
        for item in precommit_list:
            obj = item.data
            if (obj.in_svc <= t0 and obj.out_svc >= t0) and (obj.in_svc_micro >= obj.out_svc_micro):
                if object_precommit(obj, t0) == FAILED:
                    name = object_name(obj)[:63]
                    output_error(f"object {name} precommit failed")
                    rv = FAILED
                    break
    except Exception as e:
        output_error(f"precommit_all() failure: {str(e)}")
        rv = FAILED

    return rv



# /**************************************************************************
#  ** COMMIT ITERATOR
#  **************************************************************************/
def commit_init():
    """
    Initializes the commit_list and builds a list of objects that have a commit method.

    Returns:
        int: The number of objects in the commit list.
    """
    n_commits = 0
    commit_list = [None, None]

    for obj in object_get_all():
        if obj.oclass.commit is not None:
            # Separate observers
            pc = 1 if (obj.oclass.passconfig & PC_OBSERVER) == PC_OBSERVER else 0
            item = SimpleLinkList(obj)
            if item is None:
                raise Exception("commit_init memory allocation failure")
            item.next = commit_list[pc]
            commit_list[pc] = item
            n_commits += 1

    return n_commits


def commit_get0(item):
    if item is None:
        return commit_list[0]
    else:
        return item.next

def commit_get1(item):
    if item is None:
        return commit_list[1]
    else:
        return item.next

def commit_call(output, item, input):
    obj = OBJECT(SIMPLELINKLIST(item).data)
    t2 = TIMESTAMP(output)
    t0 = TIMESTAMP(input)
    if t0 < obj.in_svc:
        t2 = obj.in_svc
    elif (t0 == obj.in_svc) and (obj.in_svc_micro != 0):
        t2 = obj.in_svc + 1
    elif obj.out_svc >= t0:
        t2 = obj.oclass.commit(obj, t0)
    else:
        t2 = TS_NEVER


def commit_set(to, from_value):
    """
    Commit data set accessor.

    Args:
        to: MTIDATA
            The destination data to be set.
        from_value: MTIDATA
            The source data to copy from.

    Returns:
        MTIDATA: The updated destination data.
    """
    # Allocation request
    if to is None:
        to = [None]

    # Clear request (may follow allocation request)
    if from_value is None:
        to[0] = TS_NEVER

    # Copy request
    else:
        to[0] = from_value[0]

    return to


def commit_compare(a, b):
    t0 = a if a else TS_NEVER
    t1 = b if b else TS_NEVER
    if t0 > t1:
        return 1
    elif t0 < t1:
        return -1
    else:
        return 0

def commit_gather(mti_data_a, mti_data_b):
    t0 = mti_data_a
    t1 = mti_data_b
    if mti_data_a is None or mti_data_b is None:
        return
    if t1 < t0:
        t0 = t1

def commit_reject(mti, value):
    t1 = value
    t2 = mti.output
    if value is None:
        return 0
    return 1 if (t2 > t1 and t2 < TS_NEVER) else 0

def commit_all_st(t0, t2):
    """
    Single-threaded version of commit_all.

    Args:
        t0: TIMESTAMP
            The start time of the timestep.
        t2: TIMESTAMP
            The end time of the timestep.

    Returns:
        TIMESTAMP: The result timestamp.
    """
    result = TS_NEVER
    for pc in range(2):
        item = commit_list[pc]
        while item is not None:
            obj = item.data
            if t0 < obj.in_svc:
                if obj.in_svc < result:
                    result = obj.in_svc
            elif t0 == obj.in_svc and obj.in_svc_micro != 0:
                if obj.in_svc == result:
                    result = obj.in_svc + 1
            elif obj.out_svc >= t0:
                next_time = object_commit(obj, t0, t2)
                if next_time == TS_INVALID:
                    name = object_name(obj, 64)
                    raise Exception(f"object {name} commit failed")
                    # TROUBLESHOOT: The commit function of the named object has failed.
                    # Make sure that the object's requirements for committing are satisfied
                    # and try again. (likely internal state aberrations)
                if next_time < result:
                    result = next_time
            item = item.next
    return result

def commit_all(t0, t2):
    """
    Multi-threaded version of commit_all.

    Args:
        t0: TIMESTAMP
            The start time of the timestep.
        t2: TIMESTAMP
            The end time of the timestep.

    Returns:
        TIMESTAMP: The result timestamp.
    """
    global n_commits
    global mti
    global init_tried

    input_data = [t0]
    output_data = [t2]
    result = TS_NEVER

    try:
        # Build commit list
        if n_commits == -1:
            n_commits = commit_init()

        # If no commits found, stop here
        if n_commits == 0:
            result = TS_NEVER
        else:
            # Initialize MTI
            for pc in range(2):
                if mti[pc] is None and global_threadcount != 1 and not init_tried:
                    # Build MTI
                    fns = [
                        (commit_get0, commit_call, commit_set, commit_compare, commit_gather, commit_reject),
                        (commit_get1, commit_call, commit_set, commit_compare, commit_gather, commit_reject),
                    ]
                    mti[pc] = mti_init("commit", fns[pc], 8)
                    if mti[pc] is None:
                        output_warning("commit_all multi-threaded iterator initialization failed - using single-threaded iterator as fallback")
                        init_tried = True

                # Attempt to run multithreaded iterator
                if mti[pc] is not None and mti_run(output_data, mti[pc], input_data):
                    result = output_data[0]

                # Resort to single threaded iterator (which handles both passes)
                elif pc == 0:
                    result = commit_all_st(t0, t2)
    except Exception as e:
        output_error(f"commit_all() failure: {str(e)}")
        # TROUBLESHOOT: The commit'ing procedure failed. This is usually preceded
        # by a more detailed message that explains why it failed. Follow
        # the guidance for that message and try again.
        result = TS_INVALID

    return result


def tp_commit_all(t0, t2, threadpool):
    """
    Single threaded version of commit_all.

    Args:
        t0: TIMESTAMP
            The start time of the timestep.
        t2: TIMESTAMP
            The end time of the timestep.
        threadpool: concurrent.futures.ThreadPoolExecutor
            The thread pool for executing tasks concurrently.

    Returns:
        TIMESTAMP: The result timestamp.
    """
    result = TS_NEVER
    item
    pc
    global n_commits

    try:
        # Build commit list
        if n_commits == -1:
            n_commits = commit_init()

        # If no commits found, stop here
        if n_commits == 0:
            result = TS_NEVER
        else:
            for pc in range(2):
                for item in commit_list[pc]:
                    obj = item.data

                    def commit_task():
                        nonlocal result

                        inner_result = result

                        if t0 < obj.in_svc:
                            if obj.in_svc < inner_result:
                                result = obj.in_svc
                        elif t0 == obj.in_svc and obj.in_svc_micro != 0:
                            if obj.in_svc == inner_result:
                                result = obj.in_svc + 1
                        elif obj.out_svc >= t0:
                            next = object_commit(obj, t0, t2)
                            if next == TS_INVALID:
                                name = object_name(obj, name, sizeof(name) - 1)
                                raise Exception(f"object {name} commit failed")
                                # TROUBLESHOOT: The commit function of the named object has failed. Make sure that the object's
                                # requirements for committing are satisfied and try again. (likely internal state aberrations)
                            if next < result:
                                result = next

                    threadpool.submit(commit_task)

        threadpool.shutdown(wait=True)
    except Exception as e:
        output_error(f"tp_commit_all() failure: {str(e)}")
        # TROUBLESHOOT: The commit'ing procedure failed. This is usually preceded
        # by a more detailed message that explains why it failed. Follow
        # the guidance for that message and try again.
        result = TS_INVALID

    return result

# /**************************************************************************
#  ** FINALIZE ITERATOR
#  **************************************************************************/

def finalize_all():
    """
    Finalize all objects.

    Returns:
        STATUS: The status of the finalization process.
    """
    rv = SUCCESS
    item
    global first
    global finalize_list

    if first:
        for obj in object_get_all():
            if obj.oclass.finalize is not None:
                item = SIMPLELINKLIST()
                try:
                    item.data = obj
                    item.next = finalize_list
                    finalize_list = item
                except MemoryError:
                    name = object_name(obj, name, sizeof(name) - 1)
                    output_error(f"object {name} finalize memory allocation failed")
                    # TROUBLESHOOT: Insufficient memory remains to perform the finalize operation.
                    # Free up memory and try again.
                    return FAILED
        first = False

    try:
        for item in finalize_list:
            obj = item.data
            if object_finalize(obj) == FAILED:
                name = object_name(obj, name, sizeof(name) - 1)
                output_error(f"object {name} finalize failed")
                # TROUBLESHOOT: The finalize function of the named object has failed. Make sure that the object's
                # requirements for finalizing are satisfied and try again. (likely internal state aberrations)
                rv = FAILED
                break
    except Exception as e:
        output_error(f"finalize_all() failure: {str(e)}")
        # TROUBLESHOOT: The finalizing procedure failed. This is usually preceded
        # by a more detailed message that explains why it failed. Follow
        # the guidance for that message and try again.
        rv = FAILED

    return rv



def t_sync_all(pass_config):
    pass_index = int(pass_config / 2)  # Calculate pass_index based on pass_config value

    sync = sync_data()
    sync.status = STATUS.SUCCESS

    if ranks[pass_index] is not None:
        for i in range(PASSINIT(pass_index), PASSCMP(i, pass_index), PASSINC(pass_index)):
            if ranks[pass_index].ordinal[i] is None:
                continue

            for item in ranks[pass_index].ordinal[i].first:
                obj = item.data
                if exec_test(sync, pass_config, obj) == STATUS.FAILED:
                    return STATUS.FAILED

    st = transform_syncall(global_clock, TRANSFORMSOURCE(XS_DOUBLE | XS_COMPLEX | XS_ENDUSE), None)
    if st == TIMESTAMP.TS_INVALID:
        return STATUS.FAILED

    if st < sync.step_to:
        sync.step_to = st

    return STATUS.SUCCESS


def sync_heartbeats():
    t1 = TS_NEVER
    n = 0
    while n < n_object_heartbeats:
        t2 = object_heartbeat(object_heartbeats[n])
        if absolute_timestamp(t2) < absolute_timestamp(t1):
            t1 = t2
        n += 1
    return -absolute_timestamp(t1) if t1 < TS_NEVER else TS_NEVER


def syncall_internals(t1):
    h1 = link_syncall(t1)
    h2 = instance_syncall(t1)
    s1 = randomvar_syncall(t1)
    s2 = schedule_syncall(t1)
    s3 = loadshape_syncall(t1)
    s4 = transform_syncall(t1, TRANSFORMSOURCE.XS_SCHEDULE|TRANSFORMSOURCE.XS_LOADSHAPE, None)
    s5 = enduse_syncall(t1)
    s6 = sync_heartbeats()

    se = absolute_timestamp(earliest_timestamp(s1, s2, s3, s4, s5, s6, TS_ZERO))
    sa = earliest_timestamp(h1, h2, -se if se != TS_NEVER else TS_NEVER, TS_ZERO)

    if global_minimum_timestep > 1 and absolute_timestamp(sa) > global_clock and sa < TS_NEVER:
        if sa > 0:
            sa = (((sa-1)//global_minimum_timestep)+1)*global_minimum_timestep
        else:
            sa = -(((-sa-1)//global_minimum_timestep)+1)*global_minimum_timestep

    return sa


def exec_sleep(usec):
    if os.system == 'Windows':
        time.sleep(usec / 1000000)
    else:
        time.sleep(usec / 1000000)

# /** MAIN LOOP CONTROL ******************************************************************/


# MAIN LOOP


mls_created = False

def exec_mls_create():
    rv = 0
    global mls_created
    mls_created = 1

    output_debug("exec_mls_create()")
    #     rv = pthread_mutex_init(mls_svr_lock, None)
    rv = threading.Lock()
    if rv != 0:
        output_error("error with pthread_mutex_init() in exec_mls_init()")
    #     rv = pthread_cond_init(mls_svr_signal, None)
    rv = threading.Condition()
    if rv != 0:
        output_error("error with pthread_cond_init() in exec_mls_init()")

def exec_mls_init():
    if mls_created == 0:
        exec_mls_create()
    if global_mainloopstate == MLS_PAUSED:
        exec_mls_suspend()
    else:
        sched_update(global_clock, global_mainloopstate)

def exec_mls_suspend():
    global global_multirun_mode, global_environment, global_mainlooppauseat
    loopctr = 10
    rv = 0
    output_debug("pausing simulation")

    if global_multirun_mode == MRM_STANDALONE and global_environment != "server":
        output_warning("suspending simulation with no server/multirun active to control mainloop state")

    output_debug(f"lock_ ({mls_svr_lock} -> {mls_svr_lock})")
    with mls_svr_lock:
        output_debug("sched update_")
        sched_update(global_clock, global_mainloopstate=MLS_PAUSED)
        output_debug("wait loop_")

        while global_clock == TS_ZERO or (global_clock >= global_mainlooppauseat and global_mainlooppauseat < TS_NEVER):
            if loopctr > 0:
                output_debug(f" * tick ({loopctr})")
                loopctr -= 1
            mls_svr_signal.wait()

        output_debug("sched update_")
        sched_update(global_clock, global_mainloopstate=MLS_RUNNING)
        output_debug("unlock_")

def exec_mls_resume(timestamp):
    rv = 0
    rv = pthread_mutex_lock(mls_svr_lock)
    if rv != 0:
        output_error("error in pthread_mutex_lock() in exec_mls_resume() (error %i)", rv)
    global_mainlooppauseat = timestamp
    rv = pthread_mutex_unlock(mls_svr_lock)
    if rv != 0:
        output_error("error in pthread_mutex_unlock() in exec_mls_resume()")
    rv = pthread_cond_broadcast(mls_svr_signal)
    if rv != 0:
        output_error("error in pthread_cond_broadcast() in exec_mls_resume()")

def exec_mls_statewait(states):
    global mls_svr_lock, mls_svr_signal, global_mainloopstate
    mls_svr_lock.acquire()
    while ((global_mainloopstate & states | states) == 0):
        mls_svr_signal.wait()
    mls_svr_lock.release()

def exec_mls_done():
    global global_clock, global_mainloopstate
    global_mainloopstate = MLS_DONE
    sched_update(global_clock, global_mainloopstate)
    # 	sched_update(global_clock,global_mainloopstate=MLS_DONE);
    # 	pthread_mutex_destroy(&mls_svr_lock);
    # 	pthread_cond_destroy(&mls_svr_signal);
    mls_svr_lock = threading.Lock()
    mls_svr_lock.acquire()
    mls_svr_lock.release()
    mls_svr_signal = threading.Condition()
    mls_svr_signal.acquire()
    mls_svr_signal.release()

# /******************************************************************
#  SYNC HANDLING API
#  *******************************************************************/
main_sync = {TS_NEVER, 0, SUCCESS}


def exec_sync_reset(d):
    # /** Reset the sync time data structure
    #
    # 	This call clears the sync data structure
    # 	and prepares it for a new interation pass.
    # 	If no sync event are posted, the result of
    # 	the pass will be a successful soft NEVER,
    # 	which usually means the simulation stops at
    # 	steady state.
    #  **/
    if d is None:
        d = main_sync
    d.step_to = TS_NEVER
    d.hard_event = 0
    d.status = SUCCESS


def exec_sync_merge(to_data,  # < sync data to merge to (nullptr to update main)
                    from_data  # < sync data to merge from
                    ):
    # /** Merge the sync data structure
    #
    #     This call posts a new sync event \p to into
    # 	an existing sync data structure \p from.
    # 	If \p to is \p nullptr, then the main exec sync
    # 	event is updated.  If the status of \p from
    # 	is \p FAILED, then the \p to sync time is
    # 	set to \p TS_INVALID.  If the time of \p from
    # 	is \p TS_NEVER, then \p to is not updated.  In
    # 	all other cases, the \p to sync time is updated
    # 	with #exec_sync_set.
    #
    # 	@see #exec_sync_set
    #  **/
    main_sync = "some_value"  # Assuming 'main_sync' is of some specific type
    if to_data is None:
        to_data = main_sync
    if from_data is None:
        from_data = main_sync
    if from_data == to_data:
        return
    if exec_sync_isinvalid(from_data):
        exec_sync_set(to_data, TS_INVALID, False)
    elif exec_sync_isnever(from_data):
        pass
    elif exec_sync_ishard(from_data):
        exec_sync_set(to_data, exec_sync_get(from_data), False)
    else:
        exec_sync_set(to_data, -exec_sync_get(from_data), False)


def exec_sync_set(d, t, deltaflag):
    """
    Update the sync data structure.

    This function posts a new time to a sync event.
    If the event is None, then the main sync event is updated.
    If the new time is TS_NEVER, then the event is not updated.
    If the new time is TS_INVALID, then the event status is changed to FAILED.
    If the new time is not between -TS_MAX and TS_MAX, then an exception is thrown.
    If the event time is TS_NEVER, then if the time is positive, a hard event is posted;
    if the time is negative, a soft event is posted; otherwise, the event status is changed to FAILED.
    Otherwise, if the event is hard, then the hard event count is incremented, and if the time is earlier, it is posted.
    Otherwise, if the event is soft, then if the time is earlier, it is posted.
    Otherwise, the event status is changed to FAILED.

    :param d: The sync data to update (None to update main).
    :param t: The timestamp to update with (negative time means a soft event, 0 means failure).
    :param deltaflag: A flag to indicate if this was a deltamode exit - force it forward, otherwise, it can fail to exit.
    :return: None
    """
    if d is None:
        d = main_sync

    if t == TS_NEVER:
        return  # Nothing to do
    if t == TS_INVALID:
        d['status'] = FAILED
        return

    if t <= -TS_MAX or t > TS_MAX:
        raise Exception(f"Timestamp is not valid: {t}")

    if d['step_to'] == TS_NEVER:
        if 0 < t < TS_NEVER:
            d['step_to'] = t
            d['hard_event'] += 1
        elif t < 0:
            d['step_to'] = -t
        else:
            d['status'] = FAILED
    elif t > 0:  # Hard event
        d['hard_event'] += 1
        if not deltaflag:
            if d['step_to'] > t:
                d['step_to'] = t
        else:  # Deltamode exit - override
            d['step_to'] = t
    elif t < 0:  # Soft event
        if d['step_to'] > -t:
            d['step_to'] = -t
    else:  # t == 0 -> invalid
        d['status'] = FAILED


def exec_sync_get(d):
    """
    Get the current sync time.

    :param d: Sync data to get sync time from (None to read main).
    :return: The proper (positive) event sync time, TS_NEVER, or TS_INVALID.
    """
    if d is None:
        d = main_sync

    if exec_sync_isnever(d):
        return TS_NEVER
    if exec_sync_isinvalid(d):
        return TS_INVALID

    return absolute_timestamp(d['step_to'])

# def exec_sync_get(sync_data):
#     main_sync = "some_value"  # Assuming 'main_sync' is of some specific type
#     if sync_data is None:
#         sync_data = main_sync
#     if exec_sync_is_never(sync_data):
#         return TS_NEVER
#     if exec_sync_is_invalid(sync_data):
#         return TS_INVALID
#     return absolute_timestamp(sync_data.step_to)



def exec_sync_getevents(d):
    """
    Get the current hard event count.

    :param d: Sync data to get sync events from (None to read main).
    :return: The number of hard events associated with this sync event.
    """
    if d is None:
        d = main_sync

    return d['hard_event']


def exec_sync_ishard(d):
    """
    Determine whether the current sync data is a hard sync.

    :param d: Sync data to read hard sync status from (None to read main).
    :return: Non-zero if the event is a hard event, 0 if the event is a soft event.
    """
    if d is None:
        d = main_sync

    return d['hard_event'] > 0


def exec_sync_isnever(d):
    """
    Determine whether the current sync data time is never.

    :param d: Sync data to read never sync status from (None to read main).
    :return: Non-zero if the event is NEVER, 0 otherwise.
    """
    if d is None:
        d = main_sync

    return d['step_to'] == TS_NEVER


def exec_sync_isinvalid(d):
    """
    Determine whether the current sync time is invalid.

    :param d: Sync data to read invalid sync status from.
    :return: Non-zero if the status if FAILED, 0 otherwise.
    """
    if d is None:
        d = main_sync

    return exec_sync_getstatus(d) == FAILED


def exec_sync_getstatus(d):
    """
    Determine the current sync status.

    :param d: Sync data to read sync status from (None to read main).
    :return: The event status (SUCCESS or FAILED).
    """
    if d is None:
        d = main_sync

    return d['status']


def exec_sync_isrunning(d):
    """
    Determine whether sync time is a running simulation.

    :param d: Sync data to determine if the simulation is running (None to read main).
    :return: True if the simulation should keep going, False if it should stop.
    """
    global global_stoptime
    return exec_sync_get(d) <= global_stoptime and not exec_sync_isnever(d) and exec_sync_ishard(d)


def exec_clock_update_modules():
    """
    Update clock for modules.

    This function updates the clock for all modules that have a 'clockupdate' function.

    """
    t1 = exec_sync_get(None)
    ok = False

    while not ok:
        ok = True
        for mod in module_get_first():
            if mod['clockupdate'] is not None:
                t2 = mod['clockupdate'](t1)
                if t2 < t1:
                    t1 = t2
                    ok = False

    exec_sync_set(None, t1, False)


# /******************************************************************
#  *  MAIN EXEC LOOP
#  ******************************************************************/

def exec_start():
    """
    This is the main simulation loop.

    :return: STATUS is SUCCESS if the simulation reached equilibrium, and FAILED if a problem was encountered.
    """
    global iteration_counter, global_clock,  global_compile_only,  global_debug_mode,  global_delta_clock
    global global_delta_curr_clock,  global_deltaclock,  global_enter_realtime,  global_federation_reiteration
    global global_iteration_limit,  global_mainloop_pause_at,  global_minimum_timestep,  global_ms_per_second
    global global_multirun_mode,  global_nondeterminism_warning ,  global_profiler,  global_randomseed
    global global_realtime_metric, global_run_realtime, global_runaway_time, global_runchecks, global_show_progress
    global global_simulation_mode, global_starttime, global_stoptime , global_test_mode, global_threadcount

    threadpool = cpp_threadpool(global_threadcount)
    passes = 0
    tsteps = 0
    ptc_rv = 0  # unused
    ptj_rv = 0  # unused
    pc_rv = 0  # precommit return value
    fnl_rv = STATUS(0)  # finalize all return value
    started_at = realtime_now()  # for profiler
    j = 0
    k = 0
    ptr = None
    incr = 0
    arg_data_array = None

    # Only setup threadpool for each object rank list at the first iteration;
    # After the first iteration, setTP = false;
    setTP = True

    # int n_threads; #number of thread used in the threadpool of an object rank list
    thread = None

    nObjRankList = 0
    iObjRankList = 0

    # run create scripts, if any
    if exec_run_createscripts() != XC_SUCCESS:
        output_error("create script(s) failed")
        return FAILED

    # initialize the main loop state control
    exec_mls_init()

    # perform object initialization
    if init_all() == FAILED:
        output_error("model initialization failed")
        return FAILED

    # establish rank index if necessary
    if ranks is None and setup_ranks() == FAILED:
        output_error("ranks setup failed")
        return FAILED

    # run checks
    if global_runchecks:
        return STATUS(module_checkall())

    # compile only check
    if global_compile_only:
        return SUCCESS

    # enable non-determinism check, if any
    if global_randomseed != 0 and global_threadcount > 1:
        global_nondeterminism_warning = 1

    if not global_debug_mode:
        # schedule progress report event
        if global_show_progress:
            realtime_schedule_event(realtime_now() + 1, show_progress)

        # set thread count equal to processor count if not passed on command-line
        if global_threadcount == 0:
            global_threadcount = processor_count()
            output_verbose("using %d helper thread(s)", global_threadcount)

        # sjin: allocate arg_data_array to store pthreads creation argument
        arg_data_array = [arg_data()] * global_threadcount

        # allocate thread synchronization data
        thread_data = [ThreadData()] * global_threadcount
        threadpool_data = cpp_threadpool_thread_data(global_threadcount, threadpool)
        if not thread_data:
            output_error("thread memory allocation failed")
            return FAILED
        thread_data.count = global_threadcount
        thread_data.data = thread_data[0]
        for j in range(thread_data.count):
            thread_data.data[j].status = SUCCESS
    else:
        output_debug("debug mode running single threaded")
        output_message("GridLAB-D entering debug mode")

    # run init scripts, if any
    if exec_run_initscripts() != XC_SUCCESS:
        output_error("init script(s) failed")
        return FAILED

    # realtime startup
    if global_run_realtime > 0:
        buffer = 64
        gtime = None
        gtime = time(gtime)
        global_clock = gtime
        c, buffer = convert_from_timestamp(global_clock)
        output_verbose(f"realtime mode requires using now ({buffer if c > 0 else 'invalid time'}) as starttime")
        if global_stoptime < global_clock:
            global_stoptime = TS_NEVER

    # GET FIRST SIGNAL FROM MASTER HERE
    if global_multirun_mode == MRM_SLAVE:
        pthread_cond_broadcast(mls_inst_signal)
        output_debug("exec_start(), slave waiting for first time signal")
        pthread_mutex_lock(mls_inst_lock)
        pthread_cond_wait(mls_inst_signal, mls_inst_lock)
        pthread_mutex_unlock(mls_inst_lock)
        # will have copied data down and updated step_to with slave_cache
        # global_clock = exec_sync_get(None) # copy time signal to gc
        output_debug(f"exec_start(), slave received first time signal of {global_clock}")

    iteration_counter = global_iteration_limit
    federation_iteration_counter = global_iteration_limit

    # reset sync event
    exec_sync_reset(None)
    exec_sync_set(None, global_clock, False)
    if global_stoptime < TS_NEVER:
        exec_sync_set(None, global_stoptime + 1, False)

    # signal handler
    exec_sighandler = SIGABRT
    exec_sighandler = SIGINT
    exec_sighandler = SIGTERM

    # initialize delta mode
    if not delta_init():
        output_error("delta mode initialization failed")

    nObjRankList = 0
    # Scan the ranks of objects
    for pass_idx, rank in enumerate(ranks):
        i = PASSINIT(pass_idx)
        while PASSCMP(i, pass_idx):
            # Skip empty lists
            if rank.ordinal[i] is not None:
                nObjRankList += 1  # Count how many object rank lists in one iteration
            i += PASSINC(pass_idx)

    next_t1 = [0] * nObjRankList
    donecount = [0] * nObjRankList

    n_threads = [0] * nObjRankList

    startlock = []
    donelock = []
    start = []
    done = []

    startlock = [threading.Lock() for _ in range(nObjRankList)]
    donelock = [threading.Lock() for _ in range(nObjRankList)]
    start = [threading.Condition(lock=lock) for lock in startlock]
    done = [threading.Condition(lock=lock) for lock in donelock]

    if global_test_mode:
        return test_exec()

    # check for a model
    if object_get_count() == 0:
        # no object -> nothing to do
        return SUCCESS

    # sjin: GetMachineCycleCount
    cstart = exec_clock()
    try:
        while (
                iteration_counter > 0
                and exec_sync_isrunning(None)
                and exec_getexitcode() == XC_SUCCESS
        ):
            internal_synctime = 0

            output_debug(
                "*** main loop event at {}; stoptime={}, n_events={}, exitcode={} ***".format(
                    exec_sync_get(None), global_stoptime, exec_sync_getevents(None), exec_getexitcode()
                )
            )

            sched_update(global_clock, MLS_RUNNING)

            if global_clock >= global_mainlooppauseat and global_mainlooppauseat < TS_NEVER:
                exec_mls_suspend()

            do_checkpoint()

            if global_run_realtime == 0 and global_clock >= global_enter_realtime:
                global_run_realtime = 1

            if global_run_realtime > 0 and iteration_counter > 0:
                metric = 0.0
                fall_behind = 0
                initialized = False
                t1 = None
                t2 = None
                if not initialized:
                    t1 = time.time()
                    t2 = t1 + 1.0
                    initialized = True
                else:
                    t1 = t2
                    t2 += 1.0
                # if (system_clock::now() < t2)
                if time.time() < t2:
                    print("waiting {} nsec".format(int((t2 - time.time()) * 1e9)))
                    simulate_sleep((t2 - time.time()) * 1e9)
                    global_clock += global_run_realtime
                    metric = (t2 - t1) / 1.0
                    fall_behind = 0
                else:
                    output_error("simulation failed to keep up with real time")
                    fall_behind += 1

                if fall_behind > 5:
                    output_fatal("simulation fell behind realtime for more than 5 consecutive cycles")

                IIR = 0.9
                global_realtime_metric = global_realtime_metric * IIR + metric * (1 - IIR)
                exec_sync_reset(None)
                exec_sync_set(None, global_clock, False)
                print("realtime clock advancing to {}".format(int(global_clock)))

            else:
                global_clock = exec_sync_get(None)

            global_deltaclock = 0
            global_delta_curr_clock = float(global_clock)
            flags = DMF_NONE
            delta_dt = delta_modedesired(flags)
            t = TS_NEVER
            print("delta_dt is {}".format(int(delta_dt)))

            if delta_dt == DT_INFINITY:
                global_simulation_mode = SM_EVENT
                t = TS_NEVER
            elif delta_dt == DT_INVALID:
                global_simulation_mode = SM_ERROR
                t = TS_INVALID
            else:
                if global_minimum_timestep > 1:
                    global_simulation_mode = SM_ERROR
                    print("minimum_timestep must be 1 second to operate in deltamode")
                    t = TS_INVALID
                else:
                    if delta_dt == 0:
                        global_simulation_mode = SM_DELTA
                        t = global_clock
                    else:
                        global_simulation_mode = SM_EVENT
                        t = global_clock + delta_dt

            if global_simulation_mode == SM_ERROR:
                print("a simulation mode error has occurred")
                break

            exec_sync_set(None, t, False)
            if global_clock < 0:
                raise Exception("clock time is negative (global_clock={})".format(global_clock))
            else:
                dt = convert_from_timestamp(global_clock) # , "%Y-%m-%d %H:%M:%S", 64)
                output_debug("global_clock -> {}".format(dt))

            output_set_time_context(global_clock)
            exec_sync_reset(None)

            if global_clock <= global_stoptime and global_stoptime != TS_NEVER:
                exec_sync_set(None, global_stoptime + 1, False)

            internal_synctime = syncall_internals(global_clock)
            if (
                    internal_synctime != TS_NEVER
                    and abs(int(internal_synctime)) < global_clock
            ):
                output_debug("internal property sync failure")
                raise Exception(
                    "An internal property such as schedule, enduse, or loadshape has failed to synchronize and the simulation aborted."
                )

            exec_sync_set(None, internal_synctime, False)

            if not global_debug_mode:
                for j in range(thread_data.count):
                    thread_data.data[j].hard_event = 0
                    thread_data.data[j].step_to = TS_NEVER

                if global_clock >= global_runaway_time:
                    raise Exception("running clock detected")

                if iteration_counter == global_iteration_limit:
                    pc_rv = precommit_all(global_clock)
                    if pc_rv != SUCCESS:
                        raise Exception("precommit failure")

                iObjRankList = -1

                for pass_ in range(len(ranks)):
                    i = PASSINIT(pass_)
                    while PASSCMP(i, pass_):
                        if ranks[pass_].ordinal[i] is not None:
                            iObjRankList += 1

                            if global_debug_mode:
                                for item in ranks[pass_].ordinal[i].first:
                                    obj = item.data
                                    if exec_debug(main_sync, pass_, i, obj) == FAILED:
                                        raise Exception("debugger quit")
                            else:
                                if global_threadcount == 1:
                                    for ptr in ranks[pass_].ordinal[i].first:
                                        obj = ptr.data
                                        ss_do_object_sync(0, ptr.data)

                                        if obj.valid_to == TS_INVALID:
                                            break
                                else:
                                    n_items = 0
                                    objn = 0
                                    n_obj = ranks[pass_].ordinal[i].size
                                    if n_obj <= 1:
                                        n_threads[iObjRankList] = n_obj
                                        n_items = 1
                                    else:
                                        n_threads[iObjRankList] = int(
                                            (n_obj / global_threadcount) * (1 / 1.0)
                                        )

                                    thread = [None] * n_threads[iObjRankList]
                                    for ptr in ranks[pass_].ordinal[i].first:
                                        if thread[objn].nObj == n_items:
                                            objn += 1
                                        if thread[objn].nObj == 0:
                                            thread[objn].ls = ptr
                                        thread[objn].nObj += 1

                                    # Lock access to done count
                                    lock_done = threading.Lock()

                                    # Initialize wait count
                                    donecount[iObjRankList] = n_threads[iObjRankList]

                                    # Lock access to start condition
                                    lock_start = threading.Lock()

                                    # Update start condition
                                    next_t1[iObjRankList] += 1

                                    # Signal all the threads
                                    condition = threading.Condition(lock_start)
                                    condition.notify_all()

                                    while donecount[iObjRankList] > 0:
                                        lock_done.acquire()
                                        lock_done.release()
                                        with condition:
                                            condition.wait(timeout=0.1)

                        i += PASSINC(pass_)

                    st = transform_syncall(
                        global_clock,
                        TRANSFORMSOURCE(XS_DOUBLE | XS_COMPLEX | XS_ENDUSE),
                        None,
                    )
                    exec_sync_set(None, st, False)

                if not global_debug_mode:
                    for j in range(thread_data.count):
                        if thread_data.data[j].status == FAILED:
                            exec_sync_set(None, TS_INVALID, False)
                            raise Exception("synchronization failed")

                passes += 1

                if global_multirun_mode == MRM_SLAVE:
                    output_debug("step_to =", exec_sync_get(None))
                    output_debug("exec_start(), slave waiting for looped time signal")

                    mls_inst_signal.broadcast()

                    mls_inst_lock.acquire()
                    mls_inst_signal.wait()
                    mls_inst_lock.release()

                    output_debug("exec_start(), slave received looped time signal ({})".format(exec_sync_get(None)))

                if exec_run_syncscripts() != XC_SUCCESS:
                    output_error("sync script(s) failed")
                    raise Exception("script synchronization failure")

                if exec_sync_get(None) != global_clock and global_simulation_mode == SM_EVENT:
                    exec_clock_update_modules()
                    if exec_sync_get(None) > global_clock:
                        global_federation_reiteration = False
                        commit_time = commit_all(global_clock, exec_sync_get(None))
                        if absolute_timestamp(commit_time) <= global_clock:
                            output_error("model commit failed")
                            exec_sync_set(None, TS_INVALID, False)
                            raise Exception("commit failure")
                        elif absolute_timestamp(commit_time) < exec_sync_get(None):
                            exec_sync_set(None, commit_time, False)
                        iteration_counter = global_iteration_limit
                        federation_iteration_counter = global_iteration_limit
                        tsteps += 1
                    elif exec_sync_get(None) == global_clock:
                        iteration_counter = global_iteration_limit
                        global_federation_reiteration = True
                        if federation_iteration_counter == 0:
                            output_error("federation convergence iteration limit reached at {} (exec)".format(simtime()))
                            exec_sync_set(None, TS_INVALID, False)
                            raise Exception("convergence failure")
                elif iteration_counter == 0:
                    iteration_counter -= 1
                    output_error("convergence iteration limit reached at {} (exec)".format(simtime()))
                    exec_sync_set(None, TS_INVALID, False)
                    raise Exception("convergence failure")
                if global_simulation_mode == SM_DELTA and exec_sync_get(None) >= global_clock:
                    deltatime = delta_update()
                    if deltatime == DT_INVALID:
                        print("delta_update() failed, deltamode operation cannot continue")
                        global_simulation_mode = SM_ERROR
                        exec_sync_set(None, TS_INVALID, False)
                        raise Exception("Deltamode simulation failure")
                    elif deltatime > 0:
                        iteration_counter = global_iteration_limit
                        federation_iteration_counter = global_iteration_limit
                    exec_sync_set(None, global_clock + deltatime, True)
                    global_simulation_mode = SM_EVENT

        signal(SIGINT, None)

        if exec_sync_isnever(None):
            buffer = [0] * 64
            if convert_from_timestamp(global_clock, buffer, 64):
                print("simulation at steady state at {}".format(buffer))
        exec_mls_done()
    except Exception as e:
        output_error("exec halted:", str(e))
        exec_sync_set(None, TS_INVALID, False)
        # 		/* TROUBLESHOOT
        # 			This indicates that the core's solver shut down.  This message
        # 			is usually preceded by more detailed messages.  Follow the guidance
        # 			for those messages and try again.
        # 		 */
    # sjin: GetMachineCycleCount
    output_debug("*** main loop ended at %lli; stoptime=%lli, n_events=%i, exitcode=%i ***", exec_sync_get(nullptr), global_stoptime, exec_sync_getevents(nullptr), exec_getexitcode());
    if global_multirun_mode == MRM_MASTER:
        instance_master_done(TS_NEVER)   # tell everyone to pack up and go home

    cend = exec_clock()

    fnl_rv = finalize_all()
    if FAILED == fnl_rv:
        output_error("finalize_all() failed")

    # run term scripts, if any
    if exec_run_termscripts() != XC_SUCCESS:
        output_error("term script(s) failed")
        return FAILED

    # deallocate threadpool
    if not global_debug_mode:
        thread_data = None

    # report performance
    if global_profiler and not exec_sync_isinvalid(None):
        elapsed_sim = timestamp_to_hours(global_clock) - timestamp_to_hours(global_starttime)
        elapsed_wall = double(realtime_now() - started_at + 1)
        sync_time = 0
        sim_speed = object_get_count() / 1000.0 * elapsed_sim / elapsed_wall
        # Assuming these are global variables in your Python code
        loader_time = 0
        instance_synctime = 0
        randomvar_synctime = 0
        schedule_synctime = 0
        loadshape_synctime = 0
        enduse_synctime = 0
        transform_synctime = 0

        # Initialize class and delta profile
        cl = MyClass()
        dp = delta_getprofile()

        delta_runtime = 0
        delta_simtime = 0

        if global_threadcount == 0:
            global_threadcount = 1

        # Calculate sync time
        sync_time = 0
        for cl in class_get_first_class():
            sync_time += float(cl.profiler.clocks) / global_ms_per_second
        sync_time /= global_threadcount

        # Calculate delta runtime
        if dp.t_count > 0:
            delta_runtime = (dp.t_preupdate + dp.t_update + dp.t_postupdate) / global_ms_per_second
        else:
            delta_runtime = 0

        # Calculate delta simtime
        if dp.t_count > 0:
            delta_simtime = float(dp.t_count * dp.t_delta) / float(dp.t_count) / 1e9
        else:
            delta_simtime = 0

        def output_profile(msg, *args):
            print(msg % args)

        output_profile("\nCore profiler results")
        output_profile("======================\n")
        output_profile("Total objects           %8d objects", object_get_count())
        output_profile("Parallelism             %8d thread%s", global_threadcount, "s" if global_threadcount > 1 else "")
        output_profile("Total time              %8.1f seconds", elapsed_wall)
        output_profile("  Core time             %8.1f seconds (%.1f%%)", (elapsed_wall - sync_time - delta_runtime), (elapsed_wall - sync_time - delta_runtime) / elapsed_wall * 100)
        output_profile("    Compiler            %8.1f seconds (%.1f%%)", (loader_time / global_ms_per_second), (loader_time / global_ms_per_second) / elapsed_wall * 100)
        output_profile("    Instances           %8.1f seconds (%.1f%%)", (instance_synctime / global_ms_per_second), (instance_synctime / global_ms_per_second) / elapsed_wall * 100)
        output_profile("    Random variables    %8.1f seconds (%.1f%%)", (randomvar_synctime / global_ms_per_second), (randomvar_synctime / global_ms_per_second) / elapsed_wall * 100)
        output_profile("    Schedules           %8.1f seconds (%.1f%%)", (schedule_synctime / global_ms_per_second), (schedule_synctime / global_ms_per_second) / elapsed_wall * 100)
        output_profile("    Loadshapes          %8.1f seconds (%.1f%%)", (loadshape_synctime / global_ms_per_second), (loadshape_synctime / global_ms_per_second) / elapsed_wall * 100)
        output_profile("    Enduses             %8.1f seconds (%.1f%%)", (enduse_synctime / global_ms_per_second), (enduse_synctime / global_ms_per_second) / elapsed_wall * 100)
        output_profile("    Transforms          %8.1f seconds (%.1f%%)", (transform_synctime / global_ms_per_second), (transform_synctime / global_ms_per_second) / elapsed_wall * 100)
        output_profile("  Model time            %8.1f seconds/thread (%.1f%%)", sync_time, (sync_time / elapsed_wall) * 100)
        if dp.t_count > 0:
            output_profile("  Deltamode time        %8.1f seconds/thread (%.1f%%)", delta_runtime, delta_runtime / elapsed_wall * 100)
        output_profile("Simulation time         %8.0f days", elapsed_sim / 24)
        if sim_speed > 10.0:
            output_profile("Simulation speed         %7.0lfk object.hours/second", sim_speed)
        elif sim_speed > 1.0:
            output_profile("Simulation speed         %7.1lfk object.hours/second", sim_speed)
        else:
            output_profile("Simulation speed         %7.0lf object.hours/second", sim_speed * 1000)
        output_profile("Passes completed        %8d passes", passes)
        output_profile("Time steps completed    %8d timesteps", tsteps)
        output_profile("Convergence efficiency  %8.02lf passes/timestep", (passes / tsteps))
        output_profile("Read lock contention    %7.01lf%%", (1 - (rlock_count / rlock_spin) * 100) if rlock_spin > 0 else 0)
        output_profile("Write lock contention   %7.01lf%%", (1 - (wlock_count / wlock_spin) * 100) if wlock_spin > 0 else 0)
        output_profile("Average timestep        %7.0lf seconds/timestep", (global_clock - global_starttime) / tsteps)
        output_profile("Simulation rate         %7.0lf x realtime", (global_clock - global_starttime) / elapsed_wall)
        if dp.t_count > 0:
            # Calculate the total
            total = dp.t_preupdate + dp.t_update + dp.t_interupdate + dp.t_postupdate
            output_profile("\nDelta mode profiler results")
            output_profile("===========================\n")
            output_profile("Active modules          %s", dp.module_list)
            output_profile(f"Initialization time     {dp.t_init / global_ms_per_second:.1lf} seconds")
            output_profile(f"Number of updates       {dp.t_count:u}")
            output_profile(f"Average update timestep {dp.t_delta / dp.t_count / 1e6:.4lf} ms")
            output_profile(f"Minimum update timestep {dp.t_min / 1e6:.4lf} ms")
            output_profile(f"Maximum update timestep {dp.t_max / 1e6:.4lf} ms")
            output_profile(f"Total deltamode simtime {delta_simtime / 1000:.1lf} s")
            output_profile(f"Preupdate time          {dp.t_preupdate / global_ms_per_second:.1lf} s ({(dp.t_preupdate / total) * 100:.1f}%)")
            output_profile(f"Object update time      {dp.t_update / global_ms_per_second:.1lf} s ({(dp.t_update / total) * 100:.1f}%)")
            output_profile(f"Interupdate time        {dp.t_interupdate / global_ms_per_second:.1lf} s ({(dp.t_interupdate / total) * 100:.1f}%)")
            output_profile(f"Postupdate time         {dp.t_postupdate / global_ms_per_second:.1lf} s ({(dp.t_postupdate / total) * 100:.1f}%)")
            output_profile("Total deltamode runtime %8.1lf s (100%%)", delta_runtime)
            output_profile("Simulation rate         %8.1lf x realtime", delta_simtime / delta_runtime / 1000)

    sched_update(global_clock, MLS_DONE)

    # terminate links
    del threadpool
    return exec_sync_getstatus(None)


def exec_test(data, pass_num, obj):
    """
    Starts the executive test loop.

    Args:
        data (struct sync_data): The synchronization state data.
        pass_num (int): The pass number.
        obj (OBJECT): The current object.

    Returns:
        STATUS: SUCCESS if all tests passed, FAILED if any test failed.
    """
    this_t = None

    # Check in and out-of-service dates
    if global_clock < obj.in_svc:
        this_t = obj.in_svc  # Yet to go in service
    elif global_clock == obj.in_svc and obj.in_svc_micro != 0:
        this_t = obj.in_svc + 1  # Round up for service (deltamode handled separately)
    elif global_clock <= obj.out_svc:
        this_t = object_sync(obj, global_clock, pass_num)
    else:
        this_t = TS_NEVER  # Already out of service

    # Check for "soft" event (events that are ignored when stopping)
    if this_t < -1:
        this_t = -this_t
    elif this_t != TS_NEVER:
        data.hard_event += 1  # This counts the number of hard events

    # Check for stopped clock
    if this_t < global_clock:
        b = ""
        output_error(f"{simtime()}: object {object_name(obj, b, 63)} stopped its clock! (test)")
        # TROUBLESHOOT:
        # This indicates that one of the objects in the simulator has encountered a
        # state where it cannot calculate the time to the next state. This usually
        # is caused by a bug in the module that implements that object's class.
        data.status = FAILED
    else:
        # Check for iteration limit approach
        if iteration_counter == 2 and this_t == global_clock:
            b = ""
            output_verbose(f"{simtime()}: object {object_name(obj, b, 63)} iteration limit imminent")
        elif iteration_counter == 1 and this_t == global_clock:
            output_error(f"convergence iteration limit reached for object {obj.oclass.name}:{obj.id} (test)")
            # TROUBLESHOOT:
            # This indicates that one of the objects in the simulator has encountered a
            # state where it cannot calculate the time to the next state. This usually
            # is caused by a bug in the module that implements that object's class.

        # Manage minimum timestep
        if global_minimum_timestep > 1 and this_t > global_clock and this_t < TS_NEVER:
            this_t = ((this_t / global_minimum_timestep) + 1) * global_minimum_timestep

        # If this event precedes next step, next step is now this event
        if data.step_to > this_t:
            data.step_to = this_t
        data.status = SUCCESS

    return data.status


def slave_node_proc(args):
    global global_execdir
    args_in = args[0]
    sockfd_ptr = args_in[1]
    masterfd: socket = args_in[2]
    done_ptr = args[0]
    addrin = args_in[3]

    buffer = bytearray(1024)
    response = bytearray(1024)
    addrstr = bytearray(17)
    paddrstr = None
    token_to = None
    params = None
    cmd = bytearray(1024)
    dirname = bytearray(256)
    filename = bytearray(256)
    filepath = bytearray(256)
    ippath = bytearray(256)
    mtr_port = 0
    id = 0

    token = [
        "HS_CMD",
        "dir=\"",
        " file=\"",
        " port=",
        " id="
    ]

    token_len = [
        len(token[0]),
        len(token[1]),
        len(token[2]),
        len(token[3]),
        len(token[4])
    ]

    offset = 0
    tok_len = 0

    sockfd = sockfd_ptr[0]

    if sockfd_ptr[0] == 0:
        output_error("slave_node_proc(): no pointer to listener socket")
        return 0
    if done_ptr[0] == 0:
        output_error("slave_node_proc(): no pointer to stop condition")
        return 0
    if not masterfd:
        output_error("slave_node_proc(): no accepted socket")
        return 0
    if addrin == 0:
        output_error("slave_node_proc(): no address struct")
        return 0

    if done_ptr[0] != 0:
        output_error("slave_node_proc(): slavenode finished while thread started")
        masterfd.close()
        return 0

    rv, buffer = masterfd.recv(1023)
    if rv < 0:
        output_error("slave_node_proc(): error receiving handshake")
        masterfd.close()
        return 0
    elif rv == 0:
        output_error("slave_node_proc(): socket closed before receiving handshake")
        masterfd.close()
        return 0

    if buffer.decode() != "HS_SYN":
        output_error("slave_node_proc(): received handshake mismatch (\"%s\")", buffer.decode())
        masterfd.close()
        return 0

    response = "HS_ACK".encode()
    rv = masterfd.send(response, len(response))
    if rv < 0:
        output_error("slave_node_proc(): error sending handshake response")
        masterfd.close()
        return 0
    elif rv == 0:
        output_error("slave_node_proc(): socket closed before sending handshake response")
        masterfd.close()
        return 0

    rv, buffer = masterfd.recv(1023)
    if rv < 0:
        output_error("slave_node_proc(): error receiving command instruction")
        masterfd.close()
        return 0
    elif rv == 0:
        output_error("slave_node_proc(): socket closed before receiving command instruction")
        masterfd.close()
        return 0

    output_debug("cmd: '%s'", buffer.decode())

    if buffer.decode() != "HS_CMD":
        output_error("slave_node_proc(): bad command instruction token")
        masterfd.close()
        return 0

    offset += token_len[0]

    if buffer[offset:offset+token_len[1]].decode() != token[1]:
        output_error("slave_node_proc(): error in command instruction dir token")
        output_debug("t=\"%5s\" vs c=\"%5s\"", token[1], buffer[offset:offset+token_len[1]].decode())
        masterfd.close()
        return 0

    offset += token_len[1]
    tok_len = 0

    while buffer[offset+tok_len] != ord('"') and buffer[offset+tok_len] != 0:
        tok_len += 1

    output_debug("tok_len = %d", tok_len)

    if tok_len > 0:
        temp = "%%ld offset and %%ld len for '%%%lds'" % tok_len
        output_debug(temp, offset, tok_len, buffer[offset:offset+tok_len].decode())
        dirname = buffer[offset:offset+tok_len]
    else:
        dirname[0] = 0

    offset += 1 + tok_len

    if buffer[offset:offset+token_len[2]].decode() != token[2]:
        output_error("slave_node_proc(): error in command instruction file token")
        output_debug("(%d)t=\"%7s\" vs c=\"%7s\"", offset, token[2], buffer[offset:offset+token_len[2]].decode())
        masterfd.close()
        return 0

    offset += token_len[2]
    tok_len = buffer[offset:].find(b'"\n\r\t\0')  # whitespace in filename allowable
    if tok_len > 0:
        temp = "%%ld offset and %%ld len for '%%%lds'" % tok_len
        filename = buffer[offset:offset+tok_len]
        filename[tok_len] = 0
        output_debug(temp, offset, tok_len, buffer[offset:offset+tok_len].decode())
    else:
        filename[0] = 0

    offset += 1 + tok_len

    if buffer[offset:offset+token_len[3]].decode() != token[3]:
        output_error("slave_node_proc(): error in command instruction port token")
        masterfd.close()
        return 0

    offset += token_len[3]
    mtr_port = int(buffer[offset:offset+tok_len].decode())

    if mtr_port < 0:
        output_error("slave_node_proc(): bad return port specified in command instruction")
        masterfd.close()
        return 0
    elif mtr_port < 1024:
        output_warning("slave_node_proc(): return port %d specified, may cause system conflicts", mtr_port)

    if buffer[offset+tok_len:] != token[4]:
        output_error("slave_node_proc(): error in command instruction id token")
        masterfd.close()
        return 0

    offset = token_len[4]
    output_debug("%12s -> ???", buffer[offset:])

    id = int(buffer[offset:].decode())

    if id < 0:
        output_error("slave_node_proc(): id %d specified, may cause system conflicts", id)
        masterfd.close()
        return 0
    else:
        output_debug("id = %d", id)

    params = buffer[offset:]

    paddrstr = socket.inet_ntoa(addrin.sin_addr)
    if paddrstr == 0:
        output_error("slave_node_proc(): unable to write address to a string")
        masterfd.close()
        return 0
    else:
        addrstr = paddrstr
        output_debug("snp(): connect to %s:%d", addrstr, mtr_port)

    if os.name == 'nt':
        filepath = "%s%s%s" % (dirname, "\\" if dirname[0] else "", filename)
        output_debug("filepath = %s", filepath)
        ippath = "--slave %s:%d" % (addrstr, mtr_port)
        output_debug("ippath = %s", ippath)
        cmd = "\"%s%sgridlabd.exe\" %s --id %d %s %s" % (
            global_execdir if global_execdir[0] else "",
            "\\" if global_execdir[0] else "",
            params, id, ippath, filepath)
        output_debug("system(\"%s\")", cmd)

        rv = os.system(cmd)

    masterfd.close()


    return None


def exec_slave_node():
    """
    # Define global variables
    global_slave_port = 12345
    node_done = False
    sockfd = -1

    # Run exec_slave_node
    exec_slave_node()
    :return:
    """
    global node_done, global_slave_port, sockfd

    node_done = False
    sockfd = -1

    inaddrsz = 16  # Size of sockaddr_in in bytes

    try:
        # Initialize socket (Windows-specific)
        if hasattr(socket, 'AF_INET'):
            sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            sockfd = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

        # Bind to global_slave_port
        server_addr = ('', global_slave_port)
        sockfd.bind(server_addr)
        sockfd.listen(5)
        print(f"exec_slave_node(): listening on port {global_slave_port}")

        while not node_done:
            # Wait for connection
            reader_fdset = [sockfd]
            rlist, _, _ = select.select(reader_fdset, [], [], 3)

            if sockfd in rlist:
                inaddr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                inaddr.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                inaddr.bind(server_addr)
                inaddr.listen(1)
                print("esn(): accepted client")

                conn, _ = inaddr.accept()
                print("esn(): accepted client")

                # Thread off connection
                args = [node_done, sockfd, inaddr, conn]
                slave_thread = threading.Thread(target=slave_node_proc, args=(args,))
                slave_thread.daemon = True
                slave_thread.start()

    except Exception as e:
        print(f"exec_slave_node() error: {e}")
        node_done = True
        if sockfd != -1:
            sockfd.close()
        return


# /*************************************
#  * Script support
#  *************************************/

class SimpleList:
    def __init__(self, data, next_node=None):
        self.data = data
        self.next = next_node

def exec_add_scriptexport(name):
    global script_exports
    item = SimpleList(name)
    if item.data is None:
        return 0
    item.next = script_exports
    script_exports = item
    return 1


def update_exports():
    global script_exports
    item = script_exports
    while item is not None:
        name = item.data
        value = os.getenv(name)
        if value is not None:
            env = f"{name}={value}"
            if os.putenv(env) != 0:
                print(f"Unable to update script export '{name}' with value '{value}'")
        item = item.next
    return 1

def add_script(list_var, file):
    global create_scripts, init_scripts, sync_scripts, term_scripts
    item = SimpleList(file)
    if item.data is None:
        return 0
    item.next = list_var
    list_var = item
    if list_var is create_scripts:
        create_scripts = list_var
    elif list_var is init_scripts:
        init_scripts = list_var
    elif list_var is sync_scripts:
        sync_scripts = list_var
    elif list_var is term_scripts:
        term_scripts = list_var
    return 1


def run_scripts(list_var):
    update_exports()
    item = list_var
    while item is not None:
        rc = subprocess.call(item.data, shell=True)
        if rc != 0:
            print(f"script '{item.data}' returned with exit code {rc}")
            return rc
        else:
            print(f"script '{item.data}' returned ok")
        item = item.next
    return 0


def exec_add_createscript(file):
    output_debug("adding create script '{}'".format(file))
    return add_script(create_scripts, file)


def exec_add_initscript(file):
    output_debug("adding init script '%s'" % file)
    return add_script(init_scripts, file)


def exec_add_syncscript(file):
    output_debug("adding sync script '{}'".format(file))
    return add_script(sync_scripts, file)


def exec_add_term_script(file):
    output_debug("adding term script '%s'" % file)
    return add_script(term_scripts, file)

def exec_run_createscripts():
    return run_scripts(create_scripts())


def exec_run_initscripts():
    return run_scripts(init_scripts)

def exec_run_syncscripts():
    return run_scripts(sync_scripts)

def exec_run_termscripts():
    return run_scripts(term_scripts)




def absolute_timestamp(step):
    return datetime.fromtimestamp(step)

# def exec_sync_getevents(d):
#     if d is None:
#         d = main_sync
#     return d.hard_event
#
# def exec_sync_ishard(d):
#     if d is None:
#         d = main_sync
#     return d.hard_event > 0

def exec_sync_is_never(d):
    if d is None:
        d = main_sync
    return d.step_to == TS_NEVER

def exec_sync_is_invalid(sync_data):
    if sync_data is None:
        sync_data = main_sync
    return exec_sync_get_status(sync_data) == FAILED

# def exec_sync_getstatus(sync_data):
#     if sync_data is None:
#         sync_data = main_sync
#     return sync_data.status

#







