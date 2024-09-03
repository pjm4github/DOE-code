from enum import Enum

import subprocess

from gov_pnnl_goss.gridlab.gldcore.Convert import convert_from_timestamp, convert_from_object
from gov_pnnl_goss.gridlab.gldcore.Output import output_error, output_message
from gov_pnnl_goss.gridlab.gldcore.Object import Object, OBJECT_FLAG
from gov_pnnl_goss.gridlab.gldcore.Class import PASSCONFIG
from gov_pnnl_goss.gridlab.gldcore.Globals import SIGNALS
import datetime

class DEBUGCMD(Enum):
    DBG_QUIT = 0
    DBG_RUN = 1
    DBG_NEXT = 2

class BREAKPOINTTYPE(Enum):
    BP_BLANK = -1
    BP_MODULE = 0
    BP_CLASS = 1
    BP_OBJECT = 2
    BP_PASS = 3
    BP_RANK = 4
    BP_TIME = 5
    BP_CLOCK = 6
    BP_ERROR = 7


# Assuming MODULE, CLASS, OBJECT, and TIMESTAMP are defined elsewhere
MODULE = None
CLASS = None
OBJECT = None
TIMESTAMP = datetime.datetime


class Breakpoint:
    """
        # Example usage
        # Assuming MODULE, CLASS, and OBJECT are properly defined elsewhere
        mod_breakpoint = Breakpoint(BREAKPOINTTYPE.BP_MODULE, 1, 1, {"mod": MODULE})
        class_breakpoint = Breakpoint(BREAKPOINTTYPE.BP_CLASS, 1, 2, {"owner_class": CLASS})
        object_breakpoint = Breakpoint(BREAKPOINTTYPE.BP_OBJECT, 1, 3, {"obj": OBJECT})

        # Linking breakpoints
        mod_breakpoint.next = class_breakpoint
        class_breakpoint.next = object_breakpoint

    """
    #
    debug_active = 1  # flag indicating that the debugger is currently active
    error_caught = 0  # flag indicating that the debugger has seen an error
    watch_sync = 0  # flag indicating that sync times should be reported
    sigint_caught = 0  # flag indicating that \p SIGINT has been caught
    sigterm_caught = 0  # flag indicating that \p SIGTERM has been caught
    list_details = 0  # flag indicating that listing includes details
    list_unnamed = 1  # flag indicating that listing includes unnamed objects
    list_inactive = 1  # flag indicating that listing includes inactive objects
    list_sync = 1  # flag indicating that listing includes objects that have syncs

    def __init__(self, type=None, enabled=False, num=-1, criteria=None):
        self.type = type if type else BREAKPOINTTYPE.BP_BLANK  # BREAKPOINTTYPE enum
        self.enabled = enabled  # int
        self.num = num  # int
        self.criteria = criteria  # Union equivalent, dynamically determined based on global_property_types
        self.next = None  # Reference to the next Breakpoint in the list
        self.first_breakpoint: [Breakpoint, None] = None  # pointer to the first breakpoint
        self.last_breakpoint: [Breakpoint, None] = None # pointer to the last breakpoint
        self. breakpoint_count = 0  # the number of breakpoints defined so far

    def set_criteria(self, **kwargs):
        self.criteria = kwargs


def get_objname(obj):
    buf = [0] * 1024
    if obj.name:
        return obj.name
    else:
        return "{}:{}".format(obj.owner_class.name, obj.id)


def exec_cmd(format_str, *args):
    cmd = format_str % args
    print(f"Running '{cmd}'")
    return "SUCCESS" if subprocess.call(cmd, shell=True) == 0 else "FAILED"


def debug_notify_error():
    error_caught = 1


def str_signal(sig):
    if sig == SIGNALS.SIGABRT:
        return "SIGABRT"
    elif sig == SIGNALS.SIGFPE:
        return "SIGFPE"
    elif sig == SIGNALS.SIGILL:
        return "SIGILL"
    elif sig == SIGNALS.SIGINT:
        return "SIGINT"
    elif sig == SIGNALS.SIGSEGV:
        return "SIGSEGV"
    elif sig == SIGNALS.SIGTERM:
        return "SIGTERM"
    else:
        return "SIGUNKNOWN"


def exec_add_breakpoint(breakpoint_type, data):
    global breakpoint_count, last_breakpoint
    bp = Breakpoint()
    if bp is None:
        output_error("exec_add_breakpoint() - memory allocation failed")
        return 0
    bp.type = breakpoint_type
    bp.data = data
    bp.enabled = 1
    bp.num = breakpoint_count
    breakpoint_count += 1
    bp.next = None
    if last_breakpoint is not None:
        last_breakpoint.next = bp
    else:
        first_breakpoint = bp
    last_breakpoint = bp
    return 1

class Watchpoint:

    def __init__(self, num=-1, obj=None, prop=None, buffer_size=65536):
        self.enabled = False  # Initially, the watchpoint is not enabled
        self.num = num  # The watchpoint ID number
        self.obj = obj  # The object being watched, if any
        self.prop = prop  # The property being watched, if any
        self.buffer = bytearray(buffer_size)  # Allocate a buffer for the current value being watched
        self.next = None  # Pointer to the next watchpoint, for linked list usage

class WatchpointManager:
    """
    # Example usage
    watchpoint_manager = WatchpointManager()
    watchpoint_manager.add_watchpoint(obj="SomeObject", prop="SomeProperty")
    watchpoint_manager.add_watchpoint(obj="AnotherObject", prop="AnotherProperty")

    # Iterate through all watchpoints
    for wp in watchpoint_manager.watchpoints:
        print(f"Watchpoint {wp.num}: Object={wp.obj}, PropertyMap={wp.prop}")
    """


    def __init__(self):
        self.watchpoints = []  # Use a list to manage watchpoints instead of a linked list
        self.watchpoint_count = 0  # Keep track of the number of watchpoints

        self.first_watchpoint: Watchpoint = Watchpoint()  # a pointer to the first watchpoint
        self.last_watchpoint: Watchpoint = Watchpoint()  # a pointer to the last watchpoint
        self.watchpoint_count = 0  # the number of watchpoints defined so far

    def add_watchpoint(self, obj=None, prop=None):
        wp = Watchpoint(num=self.watchpoint_count, obj=obj, prop=prop)
        self.watchpoints.append(wp)
        self.watchpoint_count += 1
        return wp




def exec_add_watchpoint(obj, prop):
    global watchpoint_count, last_watchpoint, first_watchpoint
    wp = Watchpoint()
    buffer = bytearray(65536)
    if wp is None:
        output_error("exec_add_watchpoint() - memory allocation failed")
        return 0
    wp.enabled = 1
    wp.num = watchpoint_count
    watchpoint_count += 1
    wp.obj = obj
    wp.prop = prop
    if prop is None:
        Object.object_dump(wp.buffer)
    else:
        wp.buffer = Object.object_property_to_string(obj, prop.name, buffer, 1023)
    wp.next = None
    if last_watchpoint is not None:
        last_watchpoint.next = wp
    else:
        first_watchpoint = wp
    last_watchpoint = wp
    return 1


def list_object(obj, pass_config):
    global global_clock
    details = ""
    buf1, buf2, buf3 = "", "", ""
    if not list_unnamed and not obj.name:
        return
    if not list_inactive and (global_clock < obj.in_svc or global_clock > obj.out_svc):
        return
    if not list_sync and not obj.owner_class.sync:
        return
    if list_details:
        valid_to = ""
        convert_from_timestamp(obj.valid_to, valid_to, 64)
        details = f"{valid_to} {'c' if obj.flags & OBJECT_FLAG.OF_RECALC else '-'}" \
                  f"{'r' if obj.flags & OBJECT_FLAG.OF_RERANK else '-'} {'f' if obj.flags & OBJECT_FLAG.OF_FOREIGN else '-'}" \
                  f"{obj.owner_class.module.name}/{obj.owner_class.name}/{obj.id}"
    output_message("%1s%1s%1s%1s%1s%1s %4d %-24s %-16s %-16s %s",
                   "P" if global_clock < obj.in_svc else ("A" if global_clock < obj.out_svc else "R"),
                   "t" if obj.owner_class.passconfig & PASSCONFIG.PC_PRETOPDOWN else "T" if pass_config < PASSCONFIG.PC_PRETOPDOWN else "-",
                   "b" if obj.owner_class.passconfig & PASSCONFIG.PC_BOTTOMUP else "B" if pass_config < PASSCONFIG.PC_BOTTOMUP else "-",
                   "t" if obj.owner_class.passconfig & PASSCONFIG.PC_POSTTOPDOWN else "T" if pass_config < PASSCONFIG.PC_POSTTOPDOWN else "-",
                   "l" if obj.flags & OBJECT_FLAG.OF_LOCKED == OBJECT_FLAG.OF_LOCKED else "-",
                   "x" if obj.flags & OBJECT_FLAG.OF_HASPLC == OBJECT_FLAG.OF_HASPLC else "-",
                   obj.rank,
                   convert_from_timestamp(obj.exec_clock, buf3, 64) if obj.exec_clock > 0 else "(error)" if buf3 else "INIT",
                   obj.name if obj.name else (buf1 if convert_from_object(buf1, 64, obj, None) else "(error)"),
                   obj.parent.name if obj.parent else (buf2 if convert_from_object(buf2, 64, obj.parent, None) else "ROOT"),
                   details)
