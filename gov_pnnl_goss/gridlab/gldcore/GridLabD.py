# 	The runtime module API links the GridLAB-D core to modules that are created to
# 	perform various modeling tasks.  The core interacts with each module according
# 	to a set script that determines which exposed module functions are called and
# 	when.  The general sequence of calls is as follows:
# 	- <b>Registration</b>: A module registers the object classes it implements and
# 	registers the variables that each class publishes.
# 	- <b>Creation</b>: The core calls object creation functions during the model
# 	load operation for each object that is created.  Basic initialization can be
# 	completed at this point.
# 	- <b>Definition</b>: The core sets the values of all published variables that have
# 	been specified in the model being loaded.  After this is completed, all references
# 	to other objects have been resolved.
# 	- <b>Validation</b>: The core gives the module an opportunity to check the model
# 	before initialization begins.  This gives the module an opportunity to validate
# 	the model and reject it or fix it if it fails to meet module-defined criteria.
# 	- <b>Initialization</b>: The core calls the final initialization procedure with
# 	the object's full context now defined.  Properties that are derived based on the
# 	object's context should be initialized only at this point.
# 	- <b>Synchronization</b>: This operation is performed repeatedly until every object
# 	reports that it no longer expects any state changes.  The return value from a
# 	synchronization operation is the amount time expected to elapse before the object's
# 	next state change.  The side effect of a synchronization is a change to one or
# 	more properties of the object, and possible an update to the property of another
# 	object.
#
# 	Note that object destruction is not supported at this time.
#
# 	 GridLAB-D modules usually require a number of functions to access data and interaction
# 	 with the core.  These include
# 	 - memory locking,
# 	 - memory exception handlers,
# 	 - variable publishers,
# 	 - output functions,
# 	 - management routines,
# 	 - module management,
# 	 - class registration,
# 	 - object management,
# 	 - property management,
# 	 - object search,
# 	 - random number generators, and
# 	 - time management.


import errno
import logging
import os
import ctypes
import math
import time
from datetime import datetime
from enum import Enum
from inspect import isclass

from time import time_ns as TIMESTAMP

from gov_pnnl_goss.gridlab.gldcore.Class import PASSCONFIG
from gov_pnnl_goss.gridlab.gldcore.Output import output_verbose, output_message, output_warning
from gov_pnnl_goss.gridlab.gldcore.Property import PROPERTYTYPE, PROPERTYCOMPAREOP

# The GridLAB-D external C module header file


# Module version info (must match core version info)
MAJOR = 5
MINOR = 2

# Define CDECL for C functions
CDECL = ""

# Define EXPORT for exported functions
EXPORT = CDECL

# Include necessary headers
from GridLabHeaders import *

# define NATIVE int64	/**< native integer size */
NATIVE = 64

TS_ZERO = datetime.fromtimestamp(0)
# TS_ZERO = 0

#define TS_NEVER ((int64)(((unsigned int64)-1)>>1))
TS_NEVER = 9_223_372_036_854_775_807
# TS_MAX = 9_223_372_036_854_775_807
TS_INVALID = -1

MINYEAR = 1970
MAXYEAR = 2969


proptype = {}



PI = math.pi  # 3.1415926535897932384626433832795
E = math.e  # 2.71828182845905;
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

# Variable publishing
# /******************************************************************************
#  * Variable publishing
#  */
# /**	@defgroup gridlabd_h_publishing Publishing variables
#
# 	Modules must register public variables that are accessed by other modules, and the core by publishing them.
#
# 	The typical modules will register a class, and immediately publish the variables supported by the class:
# 	@code
#
# 	EXPORT CLASS *init(CALLBACKS *fntable, MODULE *module, int argc, char *argv[])
# 	{
# 		extern CLASS* node_class; // defined globally in the module
# 		if (set_callback(fntable)==NULL)
# 		{
# 			errno = EINVAL;
# 			return NULL;
# 		}
#
# 		node_class = gl_register_class(module,"node",sizeof(node),PASSCONFIG.PC_BOTTOMUP);
# 		PUBLISH_CLASS(node,gld::complex,V);
# 		PUBLISH_CLASS(node,gld::complex,S);
#
# 		return node_class; // always return the *first* class registered
# 	}
# 	@endcode
#
# 	@{


def PUBLISH_STRUCT(C, T, N):
    # /** The PUBLISH_STRUCT macro is used to publish a member of a structure.
    # #define PUBLISH_STRUCT(C,T,N) {struct C *_t=NULL;if (gl_publish_variable(C##_class,PT_##T,#N,(char*)&(_t->N)-(char*)_t,NULL)<1) return NULL;}
    return None

def PUBLISH_CLASS(C, T, N):
    # /** The PUBLISH_CLASS macro is used to publish a member of a class (C++ only).
    # #define PUBLISH_CLASS(C,T,N) {class C *_t=NULL;if (gl_publish_variable(C##_class,PT_##T,#N,(char*)&(_t->N)-(char*)_t,NULL)<1) return NULL;}
    return None

def PUBLISH_CLASSX(C, T, N, V):
    #  /** The PUBLISH_CLASSX macro is used to publish a member of a class (C++ only) using a different name from the member name.
    # define PUBLISH_CLASSX(C,T,N,V) {class C *_t=NULL;if (gl_publish_variable(C##_class,PT_##T,V,(char*)&(_t->N)-(char*)_t,NULL)<1) return NULL;}
    return None

def PUBLISH_DELEGATED(C, T, N):
    # /** The PUBLISH_DELEGATED macro is used to publish a variable that uses a delegated type.
    # define PUBLISH_DELEGATED(C,T,N) {class C *_t=NULL;if (gl_publish_variable(C##_class,PT_delegated,T,#N,(char*)&(_t->N)-(char*)_t,NULL)<1) return NULL;}
    return None
# /** The PUBLISH_ENUM(C,N,E) macro is used to define a keyword for an enumeration variable
# //#define PUBLISH_ENUM(C,N,E) (*Callback()->define_enumeration_member)(C##_class,#N,#E,C::E)
#
# /** The PUBLISH_SET(C,N,E) macro is used to define a keyword for a set variable
# //#define PUBLISH_SET(C,N,E) (*Callback()->define_set_member)(C##_class,#N,#E,C::E)


#

# emulation of PADDR
# class SomeClass:
#     def __init__(self):
#         self.member1 = 0
#         self.member2 = 0
#         self.member3 = 0
#
#     def paddr(self, member_name):
#         return getattr(self, member_name)
#
# # Create an instance of the class
# instance = SomeClass()
#
# # Calculate offsets
# offset_member1 = instance.paddr("member1")
# offset_member2 = instance.paddr("member2")
# offset_member3 = instance.paddr("member3")
#
# print(f"Offset of member1: {offset_member1}")
# print(f"Offset of member2: {offset_member2}")
# print(f"Offset of member3: {offset_member3}")

def PADDR(index):
    pass



# Exception handling
# GL_TRY => try #  "EXCEPTIONHANDLER *_handler = (*Callback()->exception.create_exception_handler)(); if _handler==None: (*Callback()->output_error)(%status(%d): module exception handler creation failed, __FILE__, __LINE__); else if setjmp(_handler.buf) == 0:"
# GL_THROW => raise #  "(*Callback()->exception.throw_exception)"
# GL_CATCH => except # "else: Msg = (*Callback()->exception.exception_msg)();"
# GL_ENDCATCH => finally "(*Callback()->exception.delete_exception_handler)(_handler);"


class GLError(Exception):
    def __init__(self, message):
        raise Exception(message)

class GLWarning(Exception):
    def __init__(self, message):
        raise Warning(message)

class GLTest(logging.Logger):
    def __init__(self, message, name: str):
        super().__init__(name)
        self.log(message, logging.DEBUG)

def gl_error(message):
    GLError(message)

# Produces a fatal error message on stderr.
# The code should exit immediately after a fatal error, or set global_exit_code to XC_ARGERR.
def gl_fatal(message):
    GLError(message)

# Produces a debug message on stderr, but only when --debug is provided on the command line.
def gl_debug(message):
    GLWarning(message)

# Produces a test message in the test record file, but only when --testfile is provided on the command line.
def gl_testmsg(message):
    GLTest(message)

# Provides access to a global module variable.
def gl_get_module_var(variable_name):
    return Callback().module.getvar(variable_name)


# Provide file search function
import glob
def gl_findfile(filename):
    f = glob.glob(filename)
    return f[0] if f else None

# Declare a module dependency. This will automatically load the module if it is not already loaded.
def gl_module_depends(name, major=0, minor=0, build=0):
    return Callback().module.depends(name, major, minor, build)

# # Allow an object class to be registered with the core.
def gl_register_class(class_definition):
    Callback().register_class(class_definition)

# Creates an object by allocating one from the core heap.
def gl_create_object(class_name):
    return Callback().create.single(class_name)

# Creates an array of objects on the core heap.
def gl_create_array(class_name, count):
    return Callback().create.array(class_name, count)

# Set the Callback() table for the module
def set_callback(callback_table):
    pass
    # Callback() = callback_table

# Get the first object class
def gl_class_get_first():
    return Callback().class_getfirst()

# Get an object class by name
def gl_class_get_by_name(class_name):
    return Callback().class_getname(class_name)

# Check if an object is of a specific type within a module
def object_isa(obj, obj_type, module_name=None):
    rv = Callback().object_isa(obj, obj_type) != 0
    mv = module_name is None or (obj.oclass.module == Callback().module_find(module_name))
    return rv and mv

# Declare an object property as publicly accessible
def publish_variable(obj, variable_name):
    # Implement based on your specific requirements
    pass

# Publish a load method
def publish_loadmethod(load_method_name):
    # Implement based on your specific requirements
    pass

# Publish an object function
def publish_function(oclass, function_name, function_call):
    # Implement based on your specific requirements
    pass

# Get an object function
def get_function(obj, function_name):
    if obj:
        return Callback().function.get(obj.oclass.name, function_name)
    else:
        return None

# Set the dependency of an object
def set_dependent(obj, dependent_obj):
    # Implement based on your specific requirements
    pass

# Usage examples
object_to_test = "object_to_test"
object_type_to_check = "object_type_to_check"
module_name_to_check = "module_name_to_check"
variable_name_to_publish = "variable_name_to_publish"
load_method_name_to_publish = "load_method_name_to_publish"
class_to_define_function = "class_to_define_function"
function_name_to_define = "function_name_to_define"
function_call_to_define = "function_call_to_define"
object_to_set_dependency = "object_to_set_dependency"
dependent_object = "dependent_object"

# Check if an object is of a specific type within a module
is_object_of_type = object_isa(obj=object_to_test, obj_type=object_type_to_check, module_name=module_name_to_check)

# Declare an object property as publicly accessible
publish_variable(obj=None, variable_name=variable_name_to_publish)

# Publish a load method
publish_loadmethod(load_method_name=load_method_name_to_publish)

# Publish an object function
publish_function(oclass=class_to_define_function, function_name=function_name_to_define, function_call=function_call_to_define)

# Get an object function
function = get_function(obj=object_to_test, function_name=function_name_to_define)

# Set the dependency of an object
set_dependent(obj=object_to_set_dependency, dependent_obj=dependent_object)

# Set the parent of an object
def set_parent(obj, parent):
    # Implement based on your specific requirements
    pass

# Set the rank of an object
def set_rank(obj, rank):
    # Implement based on your specific requirements
    pass

# Get the first object of a certain type
def get_first(type):
    # Implement based on your specific requirements
    pass


# Find an object by its ID
def find_by_id(id):
    # Implement based on your specific requirements
    pass


# Register a type/class
def register_type(type):
    # Implement based on your specific requirements
    pass


# Add an extended property to a class
def class_add_extended_property(class_name, property):
    # Implement based on your specific requirements
    pass


# Get a property of an object
def get_property(obj, name, part=None):
    # Implement based on your specific requirements
    pass


# Usage example
object_to_set_parent = "object_to_set_parent"
parent_object = "parent_object"
rank_to_set = 42
object_type_to_get_first = "object_type_to_get_first"
object_id_to_find = 12345
class_name_to_register = "class_name_to_register"
extended_property_to_add = "extended_property_to_add"
property_name_to_get = "property_name_to_get"


# Set the parent of an object
set_parent(obj=object_to_set_parent, parent=parent_object)


# Set the rank of an object
set_rank(obj=None, rank=rank_to_set)


# Get the first object of a certain type
first_object = get_first(type=object_type_to_get_first)


# Find an object by its ID
found_object = find_by_id(id=object_id_to_find)


# Register a type/class
register_type(type=class_name_to_register)

# Add an extended property to a class
class_add_extended_property(class_name=class_name_to_register, property=extended_property_to_add)


# Get a property of an object
property = get_property(obj=None, name=property_name_to_get)


# Get the value of a property in an object by address
def get_value_by_addr(obj, addr, value, size, prop=None):
    # Implement based on your specific requirements
    pass


# Set the value of a property in an object by address
def set_value_by_addr(obj, addr, value, prop):
    # Implement based on your specific requirements
    pass

# Set the typed value of a property
def set_typed_value(obj, prop, value):
    # Implement based on your specific requirements
    pass


# Usage example
value_buffer = "value_buffer"
property_addr = "property_addr"
property_value = "property_value"

# Get the value of a property by address
get_value_by_addr(obj=None, addr=property_addr, value=value_buffer, size=len(value_buffer), prop=None)

# Set the value of a property by address
set_value_by_addr(obj=None, addr=property_addr, value=property_value, prop=None)

# Set the typed value of a property
set_typed_value(obj=None, prop=property, value=property_value)

# Define global variables (You may need to implement these or use appropriate values)
global_clock = time.time_ns()
global_delta_curr_clock = None
global_exit_code = None
global_stoptime = 0

def global_stoptime_manager(val=None):
    global global_stoptime
    if not val:
        return global_stoptime
    else:
        global_stoptime = val

gl_globalstoptime = global_stoptime_manager()

# Define timestamp handling functions
def convert_to_timestamp(string):
    # Implement based on your specific requirements
    pass


def convert_to_timestamp_delta(string):
    # Implement based on your specific requirements
    pass


def convert_from_timestamp(timestamp):
    # Implement based on your specific requirements
    pass


def convert_from_deltatime_timestamp(timestamp):
    # Implement based on your specific requirements
    pass


def mkdatetime(timestamp):
    # Implement based on your specific requirements
    pass


def strdatetime(datetime):
    # Implement based on your specific requirements
    pass


def timestamp_to_days(timestamp):
    # Implement based on your specific requirements
    pass


def timestamp_to_hours(timestamp):
    # Implement based on your specific requirements
    pass


def timestamp_to_minutes(timestamp):
    # Implement based on your specific requirements
    pass


def timestamp_to_seconds(timestamp):
    # Implement based on your specific requirements
    pass


def local_datetime(timestamp, dt):
    # Implement based on your specific requirements
    pass


def local_datetime_delta(timestamp, dt):
    # Implement based on your specific requirements
    pass


def getweekday(timestamp):
    dt = local_datetime(timestamp)
    return dt.weekday


def gethour(timestamp):
    dt = local_datetime(timestamp)
    return dt.hour


# Define global variable handling functions (You may need to implement these)
def global_create(name, initial_value):
    # Implement based on your specific requirements
    pass


def global_setvar(name, value):
    # Implement based on your specific requirements
    pass


def global_getvar(name):
    # Implement based on your specific requirements
    pass


def global_find(name):
    # Implement based on your specific requirements
    pass


def get_oflags():
    # Implement based on your specific requirements
    pass


# Define utility functions (clip) - Only supported in C++
def clip(x, a, b):
    if x < a:
        return a
    elif x > b:
        return b
    else:
        return x


# Define the rest of the code as needed

# Note: You'll need to replace the function implementations with your specific requirements.
# Some functions are marked with "Implement based on your specific requirements" comments
# as you need to provide custom implementations based on your use case.


def bitof(x, use_throw=False):
    n = 0
    if x == 0:
        if use_throw:
            raise ValueError("bitof empty bit pattern")
        return -0x7f
    while (x & 1) == 0:
        x >>= 1
        n += 1
    if x != 0:
        if use_throw:
            raise ValueError("bitof found more than one bit")
        else:
            return -n
    return n


def gl_name(my, buffer, size):
    temp = ""
    if my is None or buffer is None:
        return None
    if my.name is None:
        temp = f"{my.oclass.name}:{my.id}"
    else:
        temp = my.name
    if size < len(temp):
        return None
    buffer[:] = temp
    return buffer


# Define the rest of the functions based on the provided code
# Note that the provided code contains C++ features that don't have direct equivalents in Python,
# so you may need to adapt them or provide implementations based on your specific needs.


def gl_schedule_find(name):
    # Implement based on your specific requirements
    pass


def gl_schedule_create(name, definition):
    # Implement based on your specific requirements
    pass


def gl_schedule_index(sch, ts):
    # Implement based on your specific requirements
    pass


def gl_schedule_value(sch, index):
    # Implement based on your specific requirements
    pass


def gl_schedule_dtnext(sch, index):
    # Implement based on your specific requirements
    pass


def gl_schedule_getfirst():
    # Implement based on your specific requirements
    pass


# Define other functions similarly based on the provided code


def nextpow2(x):
    if x < 0:
        return 0
    x -= 1
    x |= x >> 1
    x |= x >> 2
    x |= x >> 4
    x |= x >> 8
    x |= x >> 16
    return x + 1


# Interpolation functions (Replace with your own implementations)
def gl_lerp():
    pass


def gl_qerp():
    pass


# Forecasting functions (Replace with your own implementations)
def gl_forecast_create():
    pass


def gl_forecast_find():
    pass


def gl_forecast_read():
    pass


def gl_forecast_save():
    pass

# Error handling macros (Replace with Python-style error handling)
# def SYNC_CATCHALL(C):
#     obj = C.oclass
#     gl_error(functions"sync_{C}(obj={obj.id};{obj.name}): {ex}")
#
# def INIT_CATCHALL(C):
#     obj = C.oclass
#     gl_error(functions"init_{C}(obj={obj.id};{obj.name}): {ex}")
#
# def CREATE_CATCHALL(C):
#     gl_error(functions"create_{C}: {ex}")
#
# def I_CATCHALL(T, C):
#     try:
#         pass
#     except Exception as ex:
#         gl_error(functions"{T}_{C}: {ex}")
#
# def T_CATCHALL(T, C):
#     try:
#         pass
#     except Exception as ex:
#         gl_error(functions"{T}_{C}(obj={obj.id};{obj.name}): {ex}")


# Transform access
def gl_transform_getfirst():
    return Callback().transform.getnext(None)


def gl_transform_getnext(xform):
    return Callback().transform.getnext(xform)


def gl_transform_add_linear(stype, source, target, scale, bias, obj, prop, sched):
    return Callback().transform.add_linear(stype, source, target, scale, bias, obj, prop, sched)


def gl_transform_add_external(target_obj, target_prop, function, source_obj, source_prop):
    return Callback().transform.add_external(target_obj, target_prop, function, source_obj, source_prop)


def gl_module_find_transform_function(function):
    return Callback().module.find_transform_function(function)


# Random variable access
def gl_randomvar_getfirst():
    return Callback().randomvar.getnext(None)


def gl_randomvar_getnext(var):
    return Callback().randomvar.getnext(var)


def gl_randomvar_getspec(str, size, var):
    return Callback().randomvar.getspec(str, size, var)


# Remote data access
def gl_read(local, obj, prop):
    return Callback().remote.readobj(local, obj, prop)


def gl_write(local, obj, prop):
    # TODO: Implement the write function
    pass


def gl_read_global(local, var):
    # TODO: Implement the read global function
    pass


def gl_write_global(local, var):
    # TODO: Implement the write global function
    pass


# TODO change this to teh main executable
class MainExec:
    pass


gld_core = MainExec()
# Locking functions
def READLOCK(X):
    gld_core.rlock(X)

def WRITELOCK(X):
    gld_core.wlock(X)

def READUNLOCK(X):
    gld_core.runlock(X)

def WRITEUNLOCK(X):
    gld_core.wunlock(X)

def READLOCK_OBJECT(X):
    READLOCK(X.lock)

def WRITELOCK_OBJECT(X):
    WRITELOCK(X.lock)

def READUNLOCK_OBJECT(X):
    READUNLOCK(X.lock)

def WRITEUNLOCK_OBJECT(X):
    WRITEUNLOCK(X.lock)

def LOCK_OBJECT(X):
    WRITELOCK_OBJECT(X)

def UNLOCK_OBJECT(X):
    WRITEUNLOCK_OBJECT(X)

def LOCKED(X, C):
    WRITELOCK_OBJECT(X)
    #C
    WRITEUNLOCK_OBJECT(X)

_nan = [0xffffffff, 0x7fffffff]

# Python doesn't have a direct equivalent for NaN in C/C++.
# You can use the `math.nan` constant instead.

from math import nan as NaN


class GldString:
    class STRBUF(ctypes.Structure):
        _fields_ = [
            ("lock", ctypes.c_uint),  # TODO implement locking
            ("len", ctypes.c_size_t),
            ("nrefs", ctypes.c_uint),
            ("str", ctypes.c_char_p),
        ]

    def __init__(self, s=None, n=None):
        self.buf = self.STRBUF()
        self.buf_p = ctypes.pointer(self.buf)
        self.init()
        if s is not None:
            if n is None:
                self.copy(s)
            else:
                self.copy(s, n)

    def __del__(self):
        self.unlink()

    def __str__(self):
        return self.buf.str.decode() if self.buf.str else ""

    def __len__(self):
        return self.buf.len

    def init(self):
        self.buf_p.contents = self.STRBUF()
        self.buf.str = None
        self.buf.len = 0
        self.buf.nrefs = 0

    def lock(self):
        if self.buf_p:
            gld_core.wlock(ctypes.pointer(self.buf.lock))

    def unlock(self):
        if self.buf_p:
            gld_core.wunlock(ctypes.pointer(self.buf.lock))

    def fit(self, n):
        if self.buf_p is None or n > self.buf.len:
            self.alloc(n)


    def alloc(self, n):
        len_ = self.nextpow2(n)
        if len_ < ctypes.sizeof(NATIVE):
            len_ = ctypes.sizeof(NATIVE)
        new_str = ctypes.create_string_buffer(len_)
        if self.buf.str is not None:
            ctypes.memmove(new_str, self.buf.str, len(self.buf.str))
            gld_core.free(self.buf.str)
        else:
            self.buf.nrefs = 1
        self.buf.str = ctypes.cast(new_str, ctypes.c_char_p)
        self.buf.len = len_

    def copy(self, s, n=None):
        if n is None:
            self.fit(len(s) + 1)
            ctypes.memmove(self.buf.str, s.encode(), len(s) + 1)
        else:
            self.fit(n + 1)
            ctypes.memmove(self.buf.str, s.encode(), n)
            self.buf.str[n] = b'\0'

    def link(self, s):
        self.unlink()
        self.buf_p = ctypes.pointer(s.buf)
        self.buf.nrefs += 1

    def unlink(self):
        if self.buf.nrefs <= 1:
            if self.buf.str:
                gld_core.free(self.buf.str)
            gld_core.free(ctypes.pointer(self.buf))
        else:
            self.buf.nrefs -= 1

    def is_valid(self):
        return self.buf_p is not None

    def is_null(self):
        return self.is_valid() and self.buf.str is None

    def get_buffer(self):
        return self.buf.str.decode() if self.buf.str else None

    def get_size(self):
        return self.buf.len

    def get_length(self):
        return len(self) if self.buf.str else None

    def set_string(self, s):
        self.copy(s)

    def set_size(self, n):
        self.fit(n)

    def format(self, fmt, *args):
        n = self.buf.len
        self.fit(n)
        return self.vsnprintf(fmt, args)

    def vsnprintf(self, fmt, args):
        return gld_core.vsnprintf(self.buf.str, self.buf.len, fmt, args)

    def operator_lt(self, s):
        return self.buf.str.decode() < s

    def operator_le(self, s):
        return self.buf.str.decode() <= s

    def operator_eq(self, s):
        return self.buf.str.decode() == s

    def operator_ge(self, s):
        return self.buf.str.decode() >= s

    def operator_gt(self, s):
        return self.buf.str.decode() > s

    def operator_ne(self, s):
        return self.buf.str.decode() != s

    def trimleft(self):
        if not self.is_null():
            n = 0
            while self.buf.str[n:n+1] and self.buf.str[n].isspace():
                n += 1
            self.copy(self.buf.str[n:])

    def trimright(self):
        if not self.is_null():
            n = len(self)
            while n > 0 and self.buf.str[n-1:n]:
                if self.buf.str[n-1].isspace():
                    n -= 1
                else:
                    break
            self.buf.str[n:] = b'\0'

    def left(self, n):
        if not self.is_null():
            return GldString(self.buf.str[:n])

    def right(self, n):
        if not self.is_null():
            return GldString(self.buf.str[-n:])

    def mid(self, n, m):
        if not self.is_null():
            return GldString(self.buf.str[n:n + m])

    def findstr(self, s):
        if not self.is_null():
            index = self.buf.str.find(s)
            return index if index != -1 else None

    def findchr(self, c):
        if not self.is_null():
            index = self.buf.str.find(c)
            return index if index != -1 else None

    def split(self, delim=" "):
        pass  # TODO: Implement split

    def merge(self, lst, n, delim=" "):
        pass  # TODO: Implement merge

    def nextpow2(self, n):
        n -= 1
        n |= n >> 1
        n |= n >> 2
        n |= n >> 4
        n |= n >> 8
        n |= n >> 16
        n += 1
        return n


class GldClock:
    def __init__(self, y=0, m=0, d=0, H=0, M=0, S=0, ms=0, tz=None, dst=-1):
        self.dt = datetime()
        if tz is not None:
            self.set_tz(tz)
        if dst >= 0:
            self.dt.is_dst = dst
        self.set_datetime(y, m, d, H, M, S, ms)

    def __int__(self):
        return self.dt.timestamp

    def __gt__(self, t):
        return self.dt.timestamp > t

    def __ge__(self, t):
        return self.dt.timestamp >= t

    def __lt__(self, t):
        return self.dt.timestamp < t

    def __le__(self, t):
        return self.dt.timestamp <= t

    def __eq__(self, t):
        return self.dt.timestamp == t

    def __ne__(self, t):
        return self.dt.timestamp != t

    def is_valid(self):
        return self.dt.timestamp > 0

    def is_never(self):
        return self.dt.timestamp == TS_NEVER

    def get_year(self):
        return self.dt.year

    def get_month(self):
        return self.dt.month

    def get_day(self):
        return self.dt.day

    def get_hour(self):
        return self.dt.hour

    def get_minute(self):
        return self.dt.minute

    def get_second(self):
        return self.dt.second

    def get_nanosecond(self):
        return self.dt.nanosecond

    def get_uday(self):
        return self.dt.timestamp // 86400

    def get_jday(self):
        return int(self.dt.timestamp // 86400 + 2440587.5)

    def get_tz(self):
        return self.dt.tz

    def get_is_dst(self):
        return bool(self.dt.is_dst)

    def get_weekday(self):
        return self.dt.weekday

    def get_yearday(self):
        return self.dt.yearday

    def get_tzoffset(self):
        return self.dt.tzoffset

    def get_timestamp(self):
        return self.dt.timestamp

    def get_localtimestamp(self):
        return self.dt.timestamp - self.dt.tzoffset

    def get_localtimestamp_dst(self, force_dst=False):
        return self.dt.timestamp - self.dt.tzoffset + (3600 if self.dt.is_dst or force_dst else 0)

    def set_date(self, y, m, d):
        self.dt.year = y
        self.dt.month = m
        self.dt.day = d
        return Callback().time.mkdatetime(self.dt)

    def set_time(self, H, M, S, u=0, t=None, force_dst=False):
        self.dt.hour = H
        self.dt.minute = M
        self.dt.second = S
        self.dt.nanosecond = u
        if t:
            self.set_tz(t)
        if force_dst:
            self.dt.is_dst = True
        return Callback().time.mkdatetime(self.dt)

    def set_datetime(self, y, m, d, H, M, S, u=0, t=None, force_dst=False):
        self.set_date(y, m, d)
        return self.set_time(H, M, S, u, t, force_dst)

    def set_year(self, y):
        self.dt.year = y
        return Callback().time.mkdatetime(self.dt)

    def set_month(self, m):
        self.dt.month = m
        return Callback().time.mkdatetime(self.dt)

    def set_day(self, d):
        self.dt.day = d
        return Callback().time.mkdatetime(self.dt)

    def set_hour(self, h):
        self.dt.hour = h
        return Callback().time.mkdatetime(self.dt)

    def set_minute(self, m):
        self.dt.minute = m
        return Callback().time.mkdatetime(self.dt)

    def set_second(self, s):
        self.dt.second = s
        return Callback().time.mkdatetime(self.dt)

    def set_nanosecond(self, u):
        self.dt.nanosecond = u
        return Callback().time.mkdatetime(self.dt)

    def set_tz(self, t):
        self.dt.tz = t
        return Callback().time.mkdatetime(self.dt)

    def set_is_dst(self, i):
        self.dt.is_dst = i
        return Callback().time.mkdatetime(self.dt)

    def from_string(self, s):
        return Callback().time.local_datetime(Callback().time.convert_to_timestamp(s), self.dt)

    def to_string(self, size=1024):
        buf = ""
        return Callback().time.convert_from_timestamp(self.dt.timestamp, buf, size)

    def to_days(self, ts=0):
        return (self.dt.timestamp - ts) / 86400.0 + self.dt.nanosecond * 1e-9

    def to_hours(self, ts=0):
        return (self.dt.timestamp - ts) / 3600.0 + self.dt.nanosecond * 1e-9

    def to_minutes(self, ts=0):
        return (self.dt.timestamp - ts) / 60.0 + self.dt.nanosecond * 1e-9

    def to_seconds(self, ts=0):
        return self.dt.timestamp - ts + self.dt.nanosecond * 1e-9

    def to_nanoseconds(self, ts=0):
        return (self.dt.timestamp - ts) * 1e9 + self.dt.nanosecond

    def get_string(self, sz=1024):
        buf = ""
        if self.to_string(sz, buf) >= 0:
            return buf.value.decode("utf-8")
        return ""


class GldWlock:
    def __init__(self, obj):
        self.my = obj
        gld_core.wlock(self.my.lock)

    def __del__(self):
        gld_core.wunlock(self.my.lock)


class GldModule:
    pass  # Define GldModule as needed

class TECHNOLOGYREADINESSLEVEL:
    pass  # Define TECHNOLOGYREADINESSLEVEL as needed


# class GldClass:
#     def __init__(self, oclass):
#         self.oclass = oclass
#
#     def get_name(self):
#         return self.oclass.name


class GldClass:
    def __init__(self, name: object, size:int=None, parent:object=None, module=None, trl=None):
        if isclass(name):
            self.oclass = name()
            self.core = None
        else:
            self.oclass = None
            self.core = name(size, parent, module, trl)

    def get_name(self):
        return self.core.__name__ if self.core else self.oclass.__name__ if self.oclass else None

    def get_size(self):
        return -1

    def get_parent(self):
        self.core.parent()

    def get_module(self):
        return GldModule(self.core.module.name) if self.core.module else None

    def get_first_property(self):
        return GldProperty(self.core.pmap.name) if self.core.pmap else None

    def get_next_property(self, p):
        if p and p.core.next and p.core.next.oclass == self.core:
            return GldProperty(p.core.next.name)
        return None

    def get_first_function(self):
        return GldFunction(self.core.fmap.name, self.core.fmap.oclass, self.core.fmap.classaddr) if self.core.fmap else None

    def get_next_function(self, f):
        if f and f.oclass == self.core:
            next_func = f.core.next
            if next_func:
                return GldFunction(next_func.name, next_func.oclass, next_func.classaddr)
        return None

    def get_trl(self):
        return TECHNOLOGYREADINESSLEVEL(self.core.trl) if self.core.trl else None

    def set_trl(self, t):
        self.core.trl = t

    @staticmethod
    def create(m, n, s, f):
        return Callback().register_class(m, n, s, f)

    def is_last(self):
        return self.core.next is None

    def is_module_last(self):
        return self.core.next is None or self.core.module != self.core.next.module

    def get_next(self):
        return GldClass(self.core.next.name, self.core.next.size, self.core.next.parent, self.core.next.module, self.core.next.trl) if self.core.next else None


class GldFunction:
    def __init__(self, name, oclass, addr):
        self.name = name
        self.oclass = oclass
        self.addr = addr
        self.core = self  # FUNCTION(name, oclass, classaddr)

    def get_name(self):
        return self.core.name

    def get_class(self):
        return GldClass(self.core.oclass)

    def get_addr(self):
        return self.core.addr

    def is_last(self):
        return self.core.next is None

    def get_next(self):
        return GldFunction(self.core.next.name, self.core.next.oclass, self.core.next.classaddr)


class GldType:
    def __init__(self, t):
        self._type = t

    def get_spec(self):
        return Callback().properties.get_spec(self._type)

    def get_first(self):
        return type(self._type.value) # .PT_double

    def get_next(self):
        return type(self._type.next.value)

    def is_last(self):
        return self._type == type(self._type.last.value)


class GldUnit:
    def __init__(self, name=None):
        self.core = None
        self.c = None
        self.e = None
        self.h = None
        self.k = None
        self.m = None
        self.s = None
        self.a = None
        self.b = None
        self.name = ""
        self.next = None
        self.prec = None

        if name:
            unit = Callback().unit_find(name)
            if unit:
                self.name = name
                # ctypes.memmove(ctypes.byref(self.core), ctypes.byref(unit), ctypes.sizeof(UNIT))
        else:
            self.core.name = ""

    def get_name(self):
        return ctypes.string_at(self.core.name).decode("utf-8")

    def get_c(self):
        return self.core.c

    def get_e(self):
        return self.core.e

    def get_h(self):
        return self.core.h

    def get_k(self):
        return self.core.k

    def get_m(self):
        return self.core.multiplicities

    def get_s(self):
        return self.core.status

    def get_a(self):
        return self.core.a

    def get_b(self):
        return self.core.b

    def get_prec(self):
        return self.core.prec

    def is_valid(self):
        return self.core.name != ""

    def set_unit(self, name):
        unit = Callback().unit_find(name)
        if unit:
            self.core.name = name
            # ctypes.memmove(ctypes.byref(self.core), ctypes.byref(unit), ctypes.sizeof(UNIT))
            return True
        else:
            self.core.name = ""
            return False

    def convert(self, name, value):
        unit = Callback().unit_find(name)
        if unit and Callback().unit_convert_ex(ctypes.byref(self.core), unit, ctypes.byref(value)):
            return True
        else:
            return False

    def convert_unit(self, unit, value):
        if Callback().unit_convert_ex(ctypes.byref(self.core), unit, ctypes.byref(value)):
            return True
        else:
            return False

    def convert_gld_unit(self, unit, value):
        if Callback().unit_convert_ex(ctypes.byref(self.core), ctypes.byref(unit.core), ctypes.byref(value)):
            return True
        else:
            return False

    def is_last(self):
        return not bool(self.core.next)

    def get_next(self):
        return GldUnit(self.core.next)


class GldKeyword:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.next = None  # Initialize next to None

    def get_name(self):
        return self.name

    def get_value(self):
        return self.value

    def get_enumeration_value(self):
        return self.value  # Assuming enumeration is equivalent to the value

    def get_set_value(self):
        return self.value  # Assuming set is equivalent to the value

    def compare(self, name_or_value):
        if isinstance(name_or_value, str):
            return 0 if self.name == name_or_value else -1 if self.name < name_or_value else 1
        elif isinstance(name_or_value, int):
            return -1 if name_or_value < self.value else 1 if name_or_value > self.value else 0
        else:
            raise ValueError("Unsupported comparison type")

    def __eq__(self, name_or_value):
        return self.compare(name_or_value) == 0

    def __le__(self, name_or_value):
        return self.compare(name_or_value) <= 0

    def __ge__(self, name_or_value):
        return self.compare(name_or_value) >= 0

    def __lt__(self, name_or_value):
        return self.compare(name_or_value) < 0

    def __gt__(self, name_or_value):
        return self.compare(name_or_value) > 0

    def __ne__(self, name_or_value):
        return self.compare(name_or_value) != 0

    def get_next(self):
        return self.next

    def find(self, value):
        if self.compare(value) == 0:
            return self
        if self.next is None:
            return None
        return self.next.find(value)


class GldRlock:
    def __init__(self, obj):
        self.my = obj
        gld_core.rlock(self.my.lock)

    def __del__(self):
        gld_core.runlock(self.my.lock)


def GL_ATOMIC(T, X):
    class AtomicProperty:
        def __init__(self):
            self.X = T()

        def get_offset(self):
            return getattr(self, X).offset

        def get(self):
            return self.X

        def get_property(self):
            return GldProperty(self, X)

        def get_with_lock(self, lock):
            return self.X

        def set(self, p):
            self.X = p

        def set_with_lock(self, p, lock):
            self.X = p

        def get_string(self):
            return self.get_property().get_""

        def set_string(self, str):
            self.get_property().from_string(str)

    return AtomicProperty()

def GL_STRUCT(T, X):
    class StructuredProperty:
        def __init__(self):
            self.X = T()

        def get_offset(self):
            return getattr(self, X).offset

        def get(self):
            return self.X

        def get_property(self):
            return GldProperty(self, X)

        def get_with_lock(self, lock):
            return self.X

        def set(self, p):
            self.X = p

        def set_with_lock(self, p, lock):
            self.X = p

        def get_string(self):
            return self.get_property().get_""

        def set_string(self, str):
            self.get_property().from_string(str)

    return StructuredProperty()

def GL_STRING(T, X):
    class StringProperty:
        def __init__(self):
            self.X = T()

        def get_offset(self):
            return getattr(self, X).offset

        def get(self):
            return self.X.get_""

        def get_property(self):
            return GldProperty(self, X)

        def get_with_lock(self, lock):
            return self.X.get_""

        def set(self, p):
            self.X.set_string(p)

        def set_with_lock(self, p, lock):
            self.X.set_string(p)

        def get_char(self, n):
            return str(self.X)[n]

        def get_char_with_lock(self, n, lock):
            return str(self.X)[n]

        def set_char(self, n, c):
            temp_str = list(str(self.X))
            temp_str[n] = c
            self.X = ''.join(temp_str)

        def set_char_with_lock(self, n, c, lock):
            temp_str = list(str(self.X))
            temp_str[n] = c
            self.X = ''.join(temp_str)

    return StringProperty()

def GL_ARRAY(T, X, S):
    class ArrayProperty:
        def __init__(self):
            self.X = [T() for _ in range(S)]

        def get_offset(self):
            return getattr(self, X).offset

        def get(self):
            return self.X

        def get_property(self):
            return GldProperty(self, X)

        def get_with_lock(self, lock):
            return self.X

        def set(self, p):
            self.X = p

        def set_with_lock(self, p, lock):
            self.X = p

        def get_at_index(self, n):
            return self.X[n]

        def get_at_index_with_lock(self, n, lock):
            return self.X[n]

        def set_at_index(self, n, m):
            self.X[n] = m

        def set_at_index_with_lock(self, n, m, lock):
            self.X[n] = m

    return ArrayProperty()

def GL_BITFLAGS(T, X):
    class BitflagsProperty:
        def __init__(self):
            self.X = T()

        def get_offset(self):
            return getattr(self, X).offset

        def get(self, mask=-1):
            return self.X & mask

        def get_property(self):
            return GldProperty(self, X)

        def get_with_lock(self, lock):
            return self.X

        def set(self, p):
            self.X = p

        def set_bits(self, p):
            self.X |= p

        def clear_bits(self, p):
            self.X &= ~p

        def set_with_lock(self, p, lock):
            self.X = p

        def get_string(self):
            return self.get_property().get_""

        def set_string(self, str):
            self.get_property().from_string(str)

    return BitflagsProperty()

def GL_METHOD(C, X):
    def method_X(buffer, len):
        pass

    method_X.__name__ = X
    setattr(C, X, method_X)
    return method_X

def IMPL_METHOD(C, X):
    def X_impl(buffer, len):
        pass

    return X_impl

def setbits(flags, bits):
    flags |= bits

def clearbits(flags, bits):
    flags &= ~bits

def hasbits(flags, bits):
    return (flags & bits) != 0


class GldObject:
    def __init__(self, ):
        self.clock = None
        self.flags = None
        self.forecast = None
        self.heartbeat = None
        self.in_svc = None
        self.latitude = None
        self.lock = None
        self.longitude = None
        self.name = None
        self.oclass = None
        self.out_svc = None
        self.parent = None
        self.previous = None
        self.prop = None
        self.rank = None
        self.rng_state = None
        self.schedule_skew = None
        self.space = None
        self.valid_to = None
        self.value = None

    @staticmethod
    def find_object(n):
        obj = Callback().get_object(n)
        return GldObject.get_object(obj)

    def get_id(self):
        return self.previous.id

    def get_groupid(self):
        return self.previous.groupid.get_""

    def get_oclass(self):
        return GldClass(self.previous.oclass)

    def get_parent(self):
        return self.previous.parent if self.previous.parent else None

    def get_rank(self):
        return self.previous.rank

    def get_clock(self):
        return self.previous.clock

    def get_valid_to(self):
        return self.previous.valid_to

    def get_schedule_skew(self):
        return self.previous.schedule_skew

    def get_forecast(self):
        return self.previous.forecast

    def get_latitude(self):
        return self.previous.latitude

    def get_longitude(self):
        return self.previous.longitude

    def get_in_svc(self):
        return self.previous.in_svc

    def get_out_svc(self):
        return self.previous.out_svc

    def get_name(self):
        if self.previous.name:
            return self.previous.name
        elif self.previous.oclass:
            return f"{self.previous.oclass.name}:{self.previous.id}"
        else:
            return "Unknown"

    def get_space(self):
        return self.previous.space

    def get_lock(self):
        return self.previous.lock

    def get_rng_state(self):
        return self.previous.rng_state

    def get_heartbeat(self):
        return self.previous.heartbeat

    def get_flags(self, mask=0xFFFFFFFF):
        return self.previous.flags & mask

    def set_clock(self, ts=0):
        self.previous.clock = ts if ts else gl_globalclock

    def set_heartbeat(self, dt):
        self.previous.heartbeat = dt

    def set_forecast(self, fs):
        self.previous.forecast = fs

    def set_latitude(self, x):
        self.previous.latitude = x

    def set_longitude(self, x):
        self.previous.longitude = x

    def set_flags(self, flags):
        self.previous.flags = flags

    def set_flags_bits(self, bits):
        self.previous.flags |= bits

    def unset_flags_bits(self, bits):
        self.previous.flags &= ~bits

    def rlock(self):
        gld_core.rlock(self.previous.lock)

    def runlock(self):
        gld_core.runlock(self.previous.lock)

    def wlock(self):
        gld_core.wlock(self.previous.lock)

    def wunlock(self):
        gld_core.wunlock(self.previous.lock)

    def rlock_obj(self, obj):
        gld_core.rlock(obj.lock)

    def runlock_obj(self, obj):
        gld_core.runlock(obj.lock)

    def wlock_obj(self, obj):
        gld_core.wlock(obj.lock)

    def wunlock_obj(self, obj):
        gld_core.wunlock(obj.lock)

    def __eq__(self, other):
        return other is not None and self.previous == other.previous

    def get_property(self, name, pstruct=None):
        return Callback().properties.get_property(self.previous, name, pstruct)

    def get_function(self, name):
        return Callback().function.get(self.previous.oclass.name, name)

    def getp(self, prop, value):
        self.rlock()
        self.value[0] = self.previous.prop
        self.wunlock()

    def setp(self, prop, value):
        self.wlock()
        self.previous.prop[0] = value
        self.wunlock()

    def getp_rlock(self, prop, value):
        value[0] = self.previous.prop

    def getp_wlock(self, prop, value):
        value[0] = self.previous.prop

    def setp_wlock(self, prop, value):
        self.previous.prop[0] = value

    def set_dependent(self, obj):
        return Callback().object.set_dependent(self.previous, obj)

    def set_parent(self, obj):
        return Callback().object.set_parent(self.previous, obj)

    def set_rank(self, r):
        return Callback().object.set_rank(self.previous, r)

    def isa(self, otype):
        return Callback().object_isa(self.previous, otype)

    def is_valid(self):
        return self.previous is not None and self.previous == self

    def is_last(self):
        return self.previous.next is None

    @staticmethod
    def get_first():
        o = Callback().object.get_first()
        return GldObject.get_object(o)

    def get_next(self):
        return GldObject.get_object(self.previous.next)

    def exception(self, msg, *args):
        buf = f"{self.get_name()}: {msg}"
        raise Exception(buf)

    def error(self, msg, *args):
        buf = f"{self.get_name()}: {msg}"
        gl_error(buf)

    def warning(self, msg, *args):
        buf = f"{self.get_name()}: {msg}"
        gl_warning(buf)

    def debug(self, msg, *args):
        buf = f"{self.get_name()}: {msg}"
        gl_debug(buf)

    threadsafe = False

    def is_threadsafe(self):
        return self.threadsafe

    @staticmethod
    def get_object(obj):
        return GldObject(obj)

    @staticmethod
    def get_object_by_name(n):
        obj = Callback().get_object(n)
        return GldObject.get_object(obj)


class GldProperty:

    def __init__(self, obj=None, name=None):
        self.pstruct = None
        self.obj = None
        self.name = name
        if obj is not None:
            self.obj = obj.previous
            if obj:
                Callback().properties.get_property(obj.previous, name, self.pstruct)
            else:
                v = Callback().find(name)
                self.pstruct.prop = v.prop if v else None

    def is_valid(self):
        return self.pstruct.prop is not None

    def get_object(self):
        return self.obj

    def get_property(self):
        return self.pstruct.prop

    def get_property_struct(self):
        return self.pstruct

    def get_class(self):
        return GldClass(self.pstruct.prop.oclass) if self.pstruct.prop else None

    def get_name(self):
        return self.pstruct.prop.name if self.pstruct.prop else None

    def get_sql_safe_name(self):
        return f"{self.pstruct.prop.name}_{self.pstruct.part}" if self.pstruct.part else self.pstruct.prop.name

    def get_type(self):
        return GldType(self.pstruct.prop.ptype) if self.pstruct.prop else None

    def get_size(self):
        return self.pstruct.prop.size if self.pstruct.prop else None

    def get_width(self):
        return self.pstruct.prop.width if self.pstruct.prop else None

    def get_access(self):
        return self.pstruct.prop.access if self.pstruct.prop else None

    # def get_access(self, bits, mask=0xffff):
    #     return (self.pstruct.prop.access & mask) | bits if self.pstruct.prop else None

    def get_unit(self):
        return GldUnit(self.pstruct.prop.unit) if self.pstruct.prop else None

    def get_addr(self):
        return (self.obj + 1 + self.pstruct.prop.classaddr) if self.obj else self.pstruct.prop.classaddr

    def get_first_keyword(self):
        return GldKeyword(self.pstruct.prop.keywords) if self.pstruct.prop else None

    def get_description(self):
        return self.pstruct.prop.description if self.pstruct.prop else None

    def get_flags(self):
        return self.pstruct.prop.flags if self.pstruct.prop else None

    def to_string(self, buffer, size):
        return Callback().convert.property_to_string(self.pstruct.prop, self.get_addr(), buffer, size) if self.pstruct.prop else -1

    def get_string(self, sz=1024):
        res = Gld""
        buf = bytearray(1024)
        if len(buf) < sz:
            raise Exception("get_"" over size limit")
        if self.to_string(buf, sz) >= 0:
            res.value = buf.decode("utf-8")
        return res

    def from_string(self, string):
        return Callback().convert.string_to_property(self.pstruct.prop, self.get_addr(), string) if self.pstruct.prop else -1

    def get_partname(self):
        return self.pstruct.part

    def get_part(self, part=None):
        return Callback().properties.get_part(self.obj, self.pstruct.prop, part if part else self.pstruct.part) if self.obj else None

    def set_object(self, o):
        self.obj = o

    # def set_object(self, o):
    #     self.obj = o.previous

    # def set_property(self, dimensions):
    #     Callback().properties.get_property(self.obj, dimensions, self.pstruct)

    def set_property(self, p):
        self.pstruct.prop = p

    def is_valid(self):
        return self.pstruct.prop is not None

    def has_part(self):
        return bool(self.pstruct.part)

    def is_complex(self):
        return self.pstruct.prop.ptype == PROPERTYTYPE.PT_complex if self.pstruct.prop else False

    def is_double(self):
        return self.pstruct.prop.ptype in [PROPERTYTYPE.PT_double, PROPERTYTYPE.PT_random, PROPERTYTYPE.PT_enduse, PROPERTYTYPE.PT_loadshape] if self.pstruct.prop else False

    def is_integer(self):
        return self.pstruct.prop.ptype in [PROPERTYTYPE.PT_int16, PROPERTYTYPE.PT_int32, PROPERTYTYPE.PT_int64] if self.pstruct.prop else False

    def is_enumeration(self):
        return self.pstruct.prop.ptype == PROPERTYTYPE.PT_enumeration if self.pstruct.prop else False

    def is_set(self):
        return self.pstruct.prop.ptype == PROPERTYTYPE.PT_set if self.pstruct.prop else False

    def is_character(self):
        return self.pstruct.prop.ptype in [PROPERTYTYPE.PT_char8, PROPERTYTYPE.PT_char32, PROPERTYTYPE.PT_char256, PROPERTYTYPE.PT_char1024] if self.pstruct.prop else False

    def is_random(self):
        return self.pstruct.prop.ptype == PROPERTYTYPE.PT_random if self.pstruct.prop else False

    def is_enduse(self):
        return self.pstruct.prop.ptype == PROPERTYTYPE.PT_enduse if self.pstruct.prop else False

    def is_loadshape(self):
        return self.pstruct.prop.ptype == PROPERTYTYPE.PT_loadshape if self.pstruct.prop else False

    def is_double_array(self):
        return self.pstruct.prop.ptype == PROPERTYTYPE.PT_double_array if self.pstruct.prop else False

    def is_complex_array(self):
        return self.pstruct.prop.ptype == PROPERTYTYPE.PT_complex_array if self.pstruct.prop else False

    def is_objectref(self):
        return self.pstruct.prop.ptype == PROPERTYTYPE.PT_object if self.pstruct.prop else False

    def is_bool(self):
        return self.pstruct.prop.ptype == PROPERTYTYPE.PT_bool if self.pstruct.prop else False

    def is_timestamp(self):
        return self.pstruct.prop.ptype == PROPERTYTYPE.PT_timestamp if self.pstruct.prop else False

    def get_bool(self):
        errno = 0
        if self.pstruct.prop.ptype != PROPERTYTYPE.PT_bool:
            raise Exception("get_bool() called on a property that is not a bool")
        return bool(self.get_addr())

    def get_double(self, to=None):
        errno = 0
        if self.pstruct.prop.ptype not in [PROPERTYTYPE.PT_double, PROPERTYTYPE.PT_random, PROPERTYTYPE.PT_enduse, PROPERTYTYPE.PT_loadshape]:
            raise Exception("Invalid property type for get_double()")

        rv = self.get_part() if self.has_part() else float(self.get_addr())
        if to:
            return rv if self.get_unit().convert(to, rv) else NaN
        else:
            return rv

    def get_complex(self):
        if self.pstruct.prop.ptype == PROPERTYTYPE.PT_complex:
            return complex(*self.get_addr())
        return complex(NaN, NaN)

    def get_integer(self):
        if self.pstruct.prop.ptype == PROPERTYTYPE.PT_int16:
            return int(self.get_addr())
        if self.pstruct.prop.ptype == PROPERTYTYPE.PT_int32:
            return int(self.get_addr())
        if self.pstruct.prop.ptype == PROPERTYTYPE.PT_int64:
            return int(self.get_addr())

    def get_timestamp(self):
        if self.pstruct.prop.ptype != PROPERTYTYPE.PT_timestamp:
            raise Exception("get_timestamp() called on a property that is not a timestamp")
        return TIMESTAMP(*self.get_addr())

    def get_enumeration(self):
        if self.pstruct.prop.ptype != PROPERTYTYPE.PT_enumeration:
            raise Exception("get_enumeration() called on a property that is not an enumeration")
        raise NotImplemented
        # return enumeration(*self.get_addr())

    def get_set(self):
        if self.pstruct.prop.ptype != PROPERTYTYPE.PT_set:
            raise Exception("get_set() called on a property that is not a set")
        raise NotImplemented
        # return set(*self.get_addr())

    def get_objectref(self):
        if self.is_objectref():
            return self.obj

        return None

    def getp(self, value, lock):
        value = value.__class__(self.get_addr())

    def getp(self, value):
        with gld_core.rlock(self.obj.lock):
            value = value.__class__(self.get_addr())

    def getp(self, value, lock):
        value = value.__class__(self.get_addr())

    def setp(self, value, lock=None):
        if lock:
            self.value = value
        else:
            with gld_core.wlock(self.obj.lock):
                self.value = value

    def find_keyword(self, value=None, name=None):
        if value:
            return self.get_first_keyword().find(value)
        elif name:
            return self.get_first_keyword().find(name)

    def compare(self, op, a, b=None, p=None):
        n = Callback().properties.get_compare_op(self.pstruct.prop.ptype, op)
        if n == PROPERTYCOMPAREOP.TCOP_ERR:
            raise Exception("Invalid property compare operation")
        return self.compare(int(n), a, b, p)

    def compare(self, op, a, b=None):
        v1, v2 = None, None
        if self.pstruct.prop.ptype == PROPERTYTYPE.PT_complex:
            if isinstance(a, str) and isinstance(b, str):
                v1 = complex(float(a), float(b))
            else:
                v1 = a
                v2 = b
        elif self.pstruct.prop.ptype in [PROPERTYTYPE.PT_double, PROPERTYTYPE.PT_random, PROPERTYTYPE.PT_enduse, PROPERTYTYPE.PT_loadshape]:
            v1 = float(a)
            v2 = float(b) if b is not None else 0.0
        return Callback().properties.compare_basic(self.pstruct.prop.ptype, op, self.get_addr(), v1, v2, None)

    def compare(self, op, a, b, p):
        v1, v2 = float(a), float(b) if b else 0.0
        return Callback().properties.compare_basic(self.pstruct.prop.ptype, op, self.get_addr(), v1, v2, p)

    def compare(self, op, a, b=None):
        return Callback().properties.compare_basic(self.pstruct.prop.ptype, op, self.get_addr(), a, b, None);

    # Comparators
    def __eq__(self, a):
        return self.compare(PROPERTYCOMPAREOP.TCOP_EQ, a, None)

    def __le__(self, a):
        return self.compare(PROPERTYCOMPAREOP.TCOP_LE, a, None)

    def __ge__(self, a):
        return self.compare(PROPERTYCOMPAREOP.TCOP_GE, a, None)

    def __ne__(self, a):
        return self.compare(PROPERTYCOMPAREOP.TCOP_NE, a, None)

    def __lt__(self, a):
        return self.compare(PROPERTYCOMPAREOP.TCOP_LT, a, None)

    def __gt__(self, a):
        return self.compare(PROPERTYCOMPAREOP.TCOP_GT, a, None)

    def inside(self, a, b):
        return self.compare(PROPERTYCOMPAREOP.TCOP_IN, a, b)

    def outside(self, a, b):
        return self.compare(PROPERTYCOMPAREOP.TCOP_NI, a, b)

    def is_last(self):
        return (
                self.pstruct.prop is None
                or self.pstruct.prop.next is None
                or self.pstruct.prop.oclass != self.pstruct.prop.next.oclass
        )

    def get_next(self):
        return None if self.is_last() else self.pstruct.prop.next

    # Exceptions
    def exception(self, msg, *args):
        buf = bytearray(1024)
        va_list = [*args]
        buf += f"{self.obj.get_name()}.{self.pstruct.prop.name}: ".encode()
        buf += msg.encode()
        raise Exception(buf.decode())


class GldGlobal:
    def __init__(self, v=None):
        if v is None:
            self.var = Callback().find(None)
        else:
            self.var = v

    def is_valid(self):
        return self.var is not None

    def get_property(self):
        return self.var.prop if self.var else None

    def get_flags(self):
        return self.var.flags if self.var else -1

    def to_string(self, bp, sz):
        if not self.var:
            return -1
        p = GldProperty(self.var)
        return p.to_string(bp, sz)

    def get_string(self, sz=1024):
        res = Gld""
        buf = bytearray(1024)
        if len(buf) < sz:
            raise Exception("get_"" over size limit")
        if self.to_string(buf, sz) >= 0:
            res.value = buf.decode("utf-8")
        return res

    def get_bool(self):
        return bool(self.var.prop.classaddr[0]) if self.var else False

    def get_int16(self):
        return int(self.var.prop.classaddr[0]) if self.var else 0

    def get_int32(self):
        return int(self.var.prop.classaddr[0]) if self.var else 0

    def get_int64(self):
        return int(self.var.prop.classaddr[0]) if self.var else 0

    def get_double(self):
        return float(self.var.prop.classaddr[0]) if self.var else 0.0

    def get_complex(self):
        return complex(self.var.prop.classaddr[0], self.var.prop.classaddr[1]) if self.var else 0j

    def get_timestamp(self):
        return TIMESTAMP(self.var.prop.classaddr[0], self.var.prop.classaddr[1]) if self.var else 0

    def from_string(self, bp):
        if not self.var:
            return -1
        p = GldProperty(self.var)
        return p.from_string(bp)

    def get(self, n):
        self.var = Callback().find.next(n)
        return self.var is not None

    def create(self, n, t, p):
        self.var = Callback().aggregate.create(n, t, p, None)
        return self.var is not None

    def get_first(self):
        return Callback().find.next(None)

    def is_last(self):
        return self.var is not None and self.var.next is None

    def get_next(self):
        return self.var.next if self.var else None


class GldAggregate:
    def __init__(self):
        self.aggr = None

    def set_aggregate(self, spec, group):
        self.aggr = Callback().aggregate.create(spec, group)
        return self.aggr is not None

    def is_valid(self):
        return self.aggr is not None

    def get_value(self):
        if not self.aggr:
            raise Exception("null aggregate")
        return Callback().aggregate.refresh(self.aggr)


class GldObjlist:
    class s_objlist:
        pass

    def __init__(self):
        self.list = None

    def set(self, group):
        if self.list:
            Callback().objlist.destroy(self.list)
        self.list = Callback().objlist.search(group)
        return self.list.size if self.list else -1

    def add(self, m, p, o, a, b=None):
        return Callback().objlist.add(self.list, m, p, o, a, b)

    def del_(self, m, p, o, a, b=None):
        return Callback().objlist.add(self.list, m, p, o, a, b)

    def is_valid(self):
        return self.list is not None

    def get_size(self):
        return self.list.size if self.list else 0

    def get(self, n):
        return self.list.objlist[n] if self.list else None

    def apply(self, arg, function):
        return Callback().objlist.apply(self.list, arg, function) if self.list else -1

    def exception(self, msg):
        buf = msg  # Replace vsprintf with Python string formatting
        raise Exception(buf)


class GldWebdata:
    class s_http:
        pass

    def __init__(self):
        self.result = None

    def open(self, url, maxlen=4096):
        self.result = Callback().http.read(url, int(maxlen))
        return self.is_valid()

    def close(self):
        Callback().http.free(self.result)

    def is_valid(self):
        return self.result is not None

    def get_header(self):
        return self.result.header.data if self.result else None

    def get_header_size(self):
        return self.result.header.size if self.result else 0

    def get_body(self):
        return self.result.body.data if self.result else None

    def get_body_size(self):
        return self.result.body.size if self.result else 0

    def get_status(self):
        return self.result.status if self.result else 0


def do_kill(handle):
    # Define your implementation for do_kill here
    pass

gld_major = MAJOR
gld_minor = MINOR



class ExportedMethodsMixin:
    def init(self, obj, parent):
        try:
            if obj is not None:
                return self.init_method(parent)
            return 0
        except Exception as e:
            self.catch_all(e)

    def commit(self, obj, t1, t2):
        try:
            return self.commit_method(t1, t2) if obj is not None else TS_NEVER
        except Exception as e:
            self.catch_all(e)

    def notify(self, obj, notice, prop, value):
        try:
            if obj is not None:
                if notice == NM_POSTUPDATE:
                    return self.postnotify(prop, value)
                elif notice == NM_PREUPDATE:
                    return self.prenotify(prop, value)
            return 0
        except Exception as e:
            self.catch_all(e)
        return 1

    def sync(self, obj, t0, passconfig):
        try:
            t1 = TS_NEVER
            if obj is not None:
                if passconfig == PASSCONFIG.PC_PRETOPDOWN:
                    t1 = self.presync(t0)
                elif passconfig == PASSCONFIG.PC_BOTTOMUP:
                    t1 = self.sync_method(t0)
                elif passconfig == PASSCONFIG.PC_POSTTOPDOWN:
                    t1 = self.postsync(t0)
                else:
                    raise Exception("invalid pass request")
            if obj.oclass.passconfig & (PASSCONFIG.PC_PRETOPDOWN | PASSCONFIG.PC_BOTTOMUP | PASSCONFIG.PC_POSTTOPDOWN) & (~passconfig) <= passconfig:
                obj.clock = t0
            return t1
        except Exception as e:
            self.catch_all(e)

    def isa(self, obj, name):
        return self.isa_method(name) if obj is not None and name is not None else 0

    def plc(self, obj, t1):
        try:
            return self.plc_method(t1) if obj is not None else 0
        except Exception as e:
            self.catch_all(e)

    def precommit(self, obj, t1):
        try:
            return self.precommit_method(t1) if obj is not None else 0
        except Exception as e:
            self.catch_all(e)

    def finalize(self, obj):
        try:
            return self.finalize_method() if obj is not None else 0
        except Exception as e:
            self.catch_all(e)

    def notify_prop(self, obj, value):
        try:
            return self.notify_prop_method(value) if obj is not None else 0
        except Exception as e:
            self.catch_all(e)

    def loadmethod(self, obj, value):
        try:
            return self.loadmethod_method(value) if obj is not None else 0
        except Exception as e:
            self.catch_all(e)

    def method(self, obj, value, size):
        try:
            return self.method_method(value, size) if obj is not None else 0
        except Exception as e:
            self.catch_all(e)

    def catch_all(self, exception):
        pass


class YourClass(ExportedMethodsMixin):
    # Define your class here and implement the required methods
    def init_method(self, parent):
        # Implementation of init
        pass

    def commit_method(self, t1, t2):
        # Implementation of commit
        pass

    # Implement other methods similarly


# Define the equivalent DLSYM function for both platforms
def DLSYM(handle, symbol):
    try:
        return handle.__getattr__(symbol)
    except AttributeError:
        return None


class glsolver:
    def __init__(self, name, lib="glsolvers"):
        self.init = None
        self.solve = None
        self.set = None
        self.get = None

        def exception(fmt, *args):
            error_message = fmt % args
            error_message += " (%s)" % os.strerror(errno)
            raise Exception(error_message)

        try:
            # Load the dynamic library
            lib_path = ctypes.util.find_library(lib)
            if lib_path is None:
                raise Exception("glsolver(name='%s'): solver library '%s' not found" % (name, lib))

            lib_handle = ctypes.CDLL(lib_path)

            # Define the function names and types
            func_mapping = [
                ("init", ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_void_p)),
                ("solve", ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_void_p)),
                ("set", ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_char_p)),
                ("get", ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_char_p)),
            ]

            for func_name, func_type in func_mapping:
                full_func_name = name + "_" + func_name
                func_ptr = lib_handle.__getattr__(full_func_name)
                if not func_ptr:
                    raise Exception("glsolver(name='%s'): function '%s' not found in '%s'" % (name, full_func_name, lib_path))
                setattr(self, func_name, func_ptr)

            if not self.init(ctypes.c_void_p(0)):
                raise Exception("glsolver(name='%s'): init failed" % name)

        except Exception as e:
            exception(str(e))


class Aggregate:
    #     "aggregate.create": create_aggregate,
    #     "aggregate.refresh": run_aggregate,
    def __init__(self):
        pass

    def create(self, property_list):
        pass

    def refresh(self, aggregate_property):
        pass


class GLFind():
    def __init__(self):
        pass

    def add(self, original_list, objects_to_add):
        pass

    def clear(self, original_list):
        pass

    def copy(self, original_list):
        pass

    def __del__(self, original_list, objects_to_delete):
        pass

    def next(self, found_objects):
        pass

    def objects(self, query):
        pass



class GlProperties:
    def get_addr(self, property_name):
        # Get the memory address of a property
        pass

    def get_reference(self, reference_name):
        # Get a reference to another object
        pass

    def get_unit(self, property_name):
        # Get the unit of a property
        pass

    def get_value_by_name(self, property_name):
        # Get the value of a property in an object by name
        pass

    def set_value_by_name(self, property_name, value):
        # Set the value of a property in an object by name
        pass


class GlObjectVar:
    def bool_var(self, property_name):
        # Get a boolean property
        pass

    def complex_var(self, property_name):
        # Get a complex property
        pass

    def double_var(self, property_name):
        # Get a double property
        pass

    def enum_var(self, property_name):
        # Get an enumeration property
        pass

    def int16_var(self, property_name):
        # Get an int16 property
        pass

    def int32_var(self, property_name):
        # Get an int32 property
        pass

    def int64_var(self, property_name):
        # Get an int64 property
        pass

    def object_var(self, property_name):
        # Get an object property by name
        pass

    def set_var(self, property_name):
        # Get a set property
        pass


class GlObjVarName:
    def bool_var(self, property_name):
        # Get a boolean property by name
        pass

    def complex_var(self, property_name):
        # Get a complex property by name
        pass

    def double_var(self, property_name):
        # Get a double property by name
        pass

    def enum_var(self, property_name):
        # Get an enumeration property by name
        pass

    def int16_var(self, property_name):
        # Get an int16 property by name
        pass

    def int32_var(self, property_name):
        # Get an int32 property by name
        pass

    def int64_var(self, property_name):
        # Get an int64 property by name
        pass

    def set_var(self, property_name):
        # Get a set property by name
        pass

    def string_var(self, property_name):
        # Get a string property by name
        pass


class GlRandom:
    def bernoulli(self, property_name):
        # Implement based on your specific requirements
        pass

    def beta(self, property_name):
        # Implement based on your specific requirements
        pass

    def exponential(self):
        # Implement based on your specific requirements
        pass

    def gamma(self):
        # Implement based on your specific requirements
        pass

    def lognormal(self):
        # Implement based on your specific requirements
        pass

    def normal(self):
        # Implement based on your specific requirements
        pass

    def pareto(self):
        # Implement based on your specific requirements
        pass

    def pseudo(self):
        # Implement based on your specific requirements
        pass

    def rayleigh(self):
        # Implement based on your specific requirements
        pass

    def sampled(self):
        # Implement based on your specific requirements
        pass

    def triangle(self):
        # Implement based on your specific requirements
        pass

    def type(self, name):
        # Implement based on your specific requirements
        pass

    def uniform(self):
        # Implement based on your specific requirements
        pass

    def value(self, random_type):
        # Implement based on your specific requirements
        pass

    def weibull(self):
        # Implement based on your specific requirements
        pass


class Callback:
    def __init__(self):
        self.version = GlVersion()
        self.properties = GlProperties()
        self.aggregate = Aggregate()
        self.find = GLFind()
        self.objvar = GlObjectVar()
        self.objvarname = GlObjVarName()
        self.random = GlRandom()
        self.global_clock = None


    def free(self, memory_block):
        # Implement based on your specific requirements
        pass

    def get_object(self, name_or_id):
        # Get an object by its name or ID
        # Implement based on your specific requirements
        pass

    def name_object(self, obj):
        # Get the name of an object
        # Implement based on your specific requirements
        pass

    def object_count(self):
        # Get the count of objects
        pass

    def unit_convert(self, property_name, target_unit):
        # Convert the units of a property using unit name
        pass

    def unit_convert_ex(self, property_name, target_unit):
        # Convert the units of a property using unit data
        pass

    def unit_find(self, unit_name):
        # Find a unit by name
        pass

    def output_verbose(self, message):
        output_verbose(message)

    def output_message(self, message):
        output_message(message)

    def output_warning(self, message):
        output_warning(message)

    def object_isa(self, obj, obj_type, module_name=None):
        # Check if an object is of a specific type within a module
        return object_isa(obj, obj_type, module_name=None)

    def local_clock(self,offsetclock, dt):
        return local_datetime(offsetclock, dt)

# Usage example
# reference = callback["properties.get_reference"](obj, reference_name="your_reference_here")
# value = callback["properties.get_value_by_name"](obj, property_name="your_property_name")
# callback["properties.set_value_by_name"](obj, property_name="your_property_name", value="new_value")
# unit = callback["properties.get_unit"](obj, property_name="your_property_name")
# converted_value = callback["unit_convert"](obj, property_name="your_property_name", target_unit="target_unit")


# Define a dictionary to map function names to their Python counterparts

# # Usage example
# found_objects = callback["find.objects"](query="your_query_here")
# next_object = callback["find.next"](found_objects)
#
#
# # Example usage
# set_callback(callback_table)  # Set the callback table for the module
# module_var_value = gl_get_module_var("module_var_name")  # Get a global module variable
# file_path = gl_findfile("file_to_find.txt")  # Find a file
# gl_module_depends("dependency_module_name", 1, 0, 0)  # Declare a module dependency
# gl_register_class(class_definition)  # Register an object class with the core
# object_instance = gl_create_object("ClassTypeName")  # Create an object instance
# object_array = gl_create_array("ClassTypeName", 5)  # Create an array of objects
# is_object_type = gl_object_isa(object_instance, "ObjectType", "ModuleToCheck")  # Check object type
# gl_fatal("This is a fatal error message")  # Produce a fatal error message
# gl_debug("This is a debug message")  # Produce a debug message
# gl_testmsg("This is a test message")  # Produce a test message
#

# Runtime module API functions
def set_callback(fntable):
    fntable.callback = Callback()
    return fntable


class GlVersion:
    major = MAJOR
    minor = MINOR
    patch = 0
    build = 0
    branch = ''

# Access information about the version of the core
gl_version_major = Callback().version.major
gl_version_minor = Callback().version.minor
gl_version_patch = Callback().version.patch
gl_version_build = Callback().version.build
gl_version_branch = Callback().version.branch

# Output functions
gl_verbose = Callback().output_verbose
gl_output = Callback().output_message
gl_warning = Callback().output_warning
gl_globalclock = Callback().global_clock
gl_localtime = Callback().local_clock
gl_object_isa = Callback().object_isa

# Object type test
def gl_object_isa(obj, obj_type, module_name=None):
    rv = Callback().object_isa(obj, obj_type) != 0
    mv = module_name is None or (obj.oclass.module == Callback().module_find(module_name))
    return rv and mv


# Declare an object property as publicly accessible.
# @see object_define_map()
#
gl_publish_variable = Callback().define_map
gl_publish_loadmethod = Callback().loadmethod


class GClass:
    """
    The primary representation of the GridLAB-D CLASS struct in Java.  Includes native hooks for
    calls in the GridLAB-D core that pertain to the CLASS structures.
    @author Matthew Hauer <matthew.hauer@pnl.gov>

    Contains the properties of GridLAB-D classes registered by Java modules and keys them in a HashTable by name.
    @deprecated Use GClass instead of GridlabD.GClass
    """

    def __init__(self, cname, caddr, modaddr, synctype):
        """
        Constructor for GClass.

        :param cname: The name of the class to publish.
        :param caddr: The address of the class.
        :param maddr: The address of the module.
        :param sync: The pass configuration for this class.
        """
        self.classaddr = caddr
        self.classname = cname
        self.in_use = False
        self.modaddr = modaddr
        self.proptable = {}
        self.size = 0
        self.synctype = synctype
        self.objtable = {}

    def get_addr(self):
        return self.classaddr

    def get_name(self):
        return self.classname

    def set_used(self):
        self.in_use = True

    @staticmethod
    def build_class(classname, mod, sync):
        """
        Registers a classname with a core module and adds the new class object to the GModule.

        :param classname: The name of the class to publish.
        :param mod: The GModule object that is registering the class.
        :param sync: The pass configuration for this class.
        :return: New GClass on success, None on failure.
        """
        classaddr = GridlabD.register_class(mod.get_addr(), classname, sync)
        if classaddr == 0:
            GridlabD.error(f"register_class({mod.get_addr()}, {classname}, {sync}) failed")
            return None
        gc = GridlabD.GClass(classname, classaddr, mod.get_addr(), sync)
        mod.add_class(gc)
        return gc

    def add_property(self, pname, ptype):
        """
        Adds a property to a GClass, appends it to the property table, and increases the estimated
        size of the class objects. Will not add a property if the class is in use.

        :param pname: Name of the property to add.
        :param ptype: Name of the property type to add (see GridlabD.proptype).
        :return: None if the class is in use, if the property already exists for this class, or if
        an error occurs. Returns the new GProperty on success.
        """
        if self.in_use:
            GridlabD.error(f"Class {self.classname} is in use, ignoring AddProperty attempt")
            return None
        GridlabD.verbose(f"{self.classname}.AddProperty({pname}, {ptype})")
        offset = sum(prop.get_size() for prop in self.proptable.values())
        GridlabD.verbose(f"\toffset = {offset}")
        if pname in self.proptable:
            GridlabD.error(f"Property \"{pname}\" already exists")
            return None
        else:
            GridlabD.verbose(f"Property {pname} is unique")
        psize = GridlabD.publish_variable(self.modaddr, self.classaddr, pname, ptype, offset)
        if psize == 0:
            GridlabD.error(
                f"Unable to GridlabD.publish_variable({self.modaddr}, {self.classaddr}, {pname}, {ptype}, {offset})")
        p = GProperty.build(pname, ptype, offset, psize)
        if p is None:
            GridlabD.error(f"Unable to GProperty.Build({pname}, {ptype}, {offset}, {psize})")
            return None
        self.proptable[pname] = p
        self.size = offset + psize  # Update class size
        return p

    def put_obj(self, obj):
        """
        Adds an object to this GClass'status Hashtable of instantiated objects.

        :param obj: The GObject to add to the object table.
        """
        if obj.get_addr() not in self.objtable:
            self.objtable[obj.get_addr()] = obj

    def get_classname(self):
        """
        Get the classname.

        :return: The classname.
        """
        return self.classname

    def get_class_addr(self):
        """
        Get the class address.

        :return: The class address.
        """
        return self.classaddr

    def get_module_addr(self):
        """
        Get the module address.

        :return: The module address.
        """
        return self.modaddr

    def get_sync_type(self):
        """
        Get the synchronization type.

        :return: The synchronization type.
        """
        return self.synctype

    def is_in_use(self):
        """
        Check if the class is in use.

        :return: True if the class is in use, False otherwise.
        """
        return self.in_use

    def get_size(self):
        """
        Get the size of the class.

        :return: The size of the class.
        """
        return self.size

    def has_property(self, pname):
        """
        Check if the class has a property by name.

        :param pname: The property name.
        :return: True if the property exists, False otherwise.
        """
        return pname in self.proptable

    def find_property(self, pname):
        """
        Retrieves a property by name from the GClass'status property table.

        :param pname: The property name.
        :return: The GProperty if it is found, None otherwise.
        """
        return self.proptable.get(pname)

    def has_object(self, addr):
        """
        Check if a particular OBJECT * has a corresponding GObject in this GClass'status object table.

        :param addr: The address of the OBJECT structure in the core.
        :return: True if the pointer references an object of this class, False otherwise.
        """
        return addr in self.objtable

    def get_object(self, addr):
        """
        Get the object by address from the GClass'status object table.

        :param addr: The address of the object.
        :return: The object if found, None otherwise.
        """
        return self.objtable.get(addr)


class GModule:
    """
    Module inner class
    NOTE: modules are already registered with the core by the time we get to Java.
        All we're doing on this side is storing what we'll want for later, the
        class information, and the property information.
    """

    def __init__(self, a, n):
        """
        Constructor for GModule.

        :param a: The address of the module.
        :param n: The name of the module.
        """
        self.name = n
        self.addr = a
        self.ctable = {}

    def get_first_class_addr(self):
        """
        Get the core memory address of the first class that was registered.

        :return: A pointer to the first class registered for this module in the core.
        """
        if not self.ctable:
            return 0
        return next(iter(self.ctable.values())).get_class_addr()

    def add_class(self, gc):
        """
        Adds a class to the module'status class table.

        :param gc: The GClass object to add.
        :return: True on success, False if the class already exists in the module.
        """
        if gc.get_classname() not in self.ctable:
            self.ctable[gc.get_classname()] = gc
            return True
        GridlabD.error(f"Module {self.name} already contains class {gc.get_classname()}")
        return False

    def get_addr(self):
        """
        Get the module address.

        :return: The module address.
        """
        return self.addr

    def get_name(self):
        """
        Get the module name.

        :return: The module name.
        """
        return self.name

    @staticmethod
    def init(mod_addr, mod_name, argc, argv):
        """
        Initialize the module.

        :param mod_addr: The module address.
        :param mod_name: The module name.
        :param argc: Number of command-line arguments.
        :param argv: Array of command-line arguments.
        :return: GModule object.
        """
        mod = GModule(mod_addr, mod_name)
        return mod

    @staticmethod
    def do_kill():
        """
        Perform cleanup when the module is killed.

        :return: 0.
        """
        # If anything needs to be deleted or freed, this is a good time to do it
        return 0

    @staticmethod
    def check():
        """
        Check module.

        :return: 0.
        """
        return 0

    @staticmethod
    def import_file(filename):
        """
        Import a file into the module.

        :param filename: The name of the file to import.
        :return: 0.
        """
        return 0

    @staticmethod
    def export_file(filename):
        """
        Export a file from the module.

        :param filename: The name of the file to export.
        :return: 0.
        """
        return 0

    @staticmethod
    def setvar(varname, value):
        """
        Set a variable in the module.

        :param varname: The name of the variable.
        :param value: The value to set.
        :return: 0.
        """
        return 0

    @staticmethod
    def module_test(argc, argv):
        """
        Perform module test.

        :param argc: Number of command-line arguments.
        :param argv: Array of command-line arguments.
        :return: 0.
        """
        return 0

    @staticmethod
    def cmdargs(argc, argv):
        """
        Handle command-line arguments.

        :param argc: Number of command-line arguments.
        :param argv: Array of command-line arguments.
        :return: 0.
        """
        return 0

    def kmldump(self, object_addr):
        """
        Returns a string to fprintf into the C-side stub.

        :param object_addr: The address of the object.
        :return: An empty string.
        """
        return ""


class GProperty:
    def __init__(self, name, type, size, offset):
        """
        Constructor for GProperty.

        :param name: Name of this property.
        :param type: Name of the type of this property (see GridlabD.proptype).
        :param size: Estimated size of this property, in bytes.
        :param offset: Estimated offset within the OBJECT data block in C for this property, in bytes.
        """
        self.name = name
        self.type = type
        self.size = size
        self.offset = offset
        self.addr = None

    def get_name(self):
        """
        Get the name of this property.

        :return: The name of this property.
        """
        return self.name

    def get_type(self):
        """
        Get the type of this property.

        :return: The type of this property.
        """
        return self.type

    def get_size(self):
        """
        Get the estimated size of this property in bytes.

        :return: The estimated size of this property.
        """
        return self.size

    def get_offset(self):
        """
        Get the estimated offset within the OBJECT data block in C for this property in bytes.

        :return: The estimated offset of this property.
        """
        return self.offset

    def get_addr(self):
        """
        Get the address pointer for this property.

        :return: The address pointer for this property.
        """
        return self.addr

    @staticmethod
    def build(name, type, offset):
        """
        Public constructor wrapper.

        :param name: Name of the property to create.
        :param type: Name of the type of property to create.
        :param offset: Offset for this property, in bytes.
        :return: The new GProperty object, None if the property type was invalid.
        """
        size = GridlabD.proptype.get(type)
        if size is None:
            GridlabD.error(f"Unable to create property \"{name}\" of type \"{type}\"")
            return None
        return GProperty(name, type, size, offset)

    @staticmethod
    def build_with_size(name, type, offset, size):
        """
        Public constructor wrapper.

        :param name: Name of the property to create.
        :param type: Name of the type of property to create.
        :param offset: Offset for this property, in bytes.
        :param size: Size of this property, in bytes.
        :return: The new GProperty object.
        """
        return GProperty(name, type, size, offset)


class GridlabD:
    # Simple GridlabD statics
    # Initialization block
    proptype = {
        "int16": 2,
        "int32": 4,
        "int64": 8,
        "double": 8,
        "char8": 9,
        "char32": 33,
        "char256": 257,
        "char1024": 1025,
        "complex": 24,
        "object": 8,
        "bool": 4,
        "timestamp": 8,
        "loadshape": 256,
        "enduse": 256,
    }
    TS_NEVER = ctypes.c_longlong(ctypes.c_ulonglong(-1).value >> 1).value
    TS_INVALID = -1
    TS_ZERO = 0
    TS_MAX = ctypes.c_longlong(-1).value
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

    # Inner classes
    class Complex:
        def __init__(self, re=0.0, im=0.0):
            self.re = re
            self.im = im

        def __str__(self):
            if self.im >= 0.0:
                return f"{self.re}+{self.im}i"
            return f"{self.re}{self.im}i"

    # Other class members and methods go here



    # Static methods
    @staticmethod
    def clip(x, a, b):
        return a if x < a else b if x > b else x

    # Utility native stubs and other native methods

    # Complex number methods
    @staticmethod
    def get_complex(object_addr, property_addr):
        r = GridlabD.get_complex_real(object_addr, property_addr)
        i = GridlabD.get_complex_imag(object_addr, property_addr)
        return GridlabD.Complex(r, i)

    @staticmethod
    def get_complex_by_name(object_addr, property_name):
        r = GridlabD.get_complex_real_by_name(object_addr, property_name)
        i = GridlabD.get_complex_imag_by_name(object_addr, property_name)
        return GridlabD.Complex(r, i)

    @staticmethod
    def get_int16(block, offset):
        pass  # Implement the logic for GetInt16 in Python

    @staticmethod
    def get_int32(block, offset):
        pass  # Implement the logic for GetInt32 in Python

    @staticmethod
    def get_int64(block, offset):
        pass  # Implement the logic for GetInt64 in Python

    @staticmethod
    def get_double(block, offset):
        pass  # Implement the logic for GetDouble in Python

    @staticmethod
    def set_int16(block, offset, value):
        pass  # Implement the logic for SetInt16 in Python

    @staticmethod
    def set_int32(block, offset, value):
        pass  # Implement the logic for SetInt32 in Python

    @staticmethod
    def set_int64(block, offset, value):
        pass  # Implement the logic for SetInt64 in Python

    @staticmethod
    def set_double(block, offset, value):
        pass  # Implement the logic for SetDouble in Python

    @staticmethod
    def set_complex(block, offset, r, i):
        pass  # Implement the logic for SetComplex in Python

    # More native stubs and methods
    @staticmethod
    def verbose(str):
        pass  # Implement the logic for verbose in Python

    @staticmethod
    def output(str):
        pass  # Implement the logic for output in Python

    @staticmethod
    def warning(str):
        pass  # Implement the logic for warning in Python

    @staticmethod
    def error(str):
        pass  # Implement the logic for error in Python

    @staticmethod
    def debug(str):
        pass  # Implement the logic for debug in Python

    @staticmethod
    def testmsg(str):
        pass  # Implement the logic for testmsg in Python

    @staticmethod
    def malloc(size):
        pass  # Implement the logic for malloc in Python

    @staticmethod
    def get_module_var(modulename, varname):
        pass  # Implement the logic for get_module_var in Python

    @staticmethod
    def findfile(filename):
        pass  # Implement the logic for findfile in Python

    @staticmethod
    def find_module(modulename):
        pass  # Implement the logic for find_module in Python

    @staticmethod
    def register_class(moduleaddr, classname, passconfig):
        pass  # Implement the logic for register_class in Python

    @staticmethod
    def create_object(oclass_addr, size):
        pass  # Implement the logic for create_object in Python

    @staticmethod
    def create_array(oclass_addr, size, n_objects):
        pass  # Implement the logic for create_array in Python

    @staticmethod
    def object_isa(obj_addr, typename):
        pass  # Implement the logic for object_isa in Python

    @staticmethod
    def publish_variable(moduleaddr, classaddr, varname, vartype, offset):
        pass  # Implement the logic for publish_variable in Python

    @staticmethod
    def publish_function(modulename, classname, funcname):
        pass  # Implement the logic for publish_function in Python

    @staticmethod
    def set_dependent(from_addr, to_addr):
        pass  # Implement the logic for set_dependent in Python

    @staticmethod
    def set_parent(child_addr, parent_addr):
        pass  # Implement the logic for set_parent in Python

    @staticmethod
    def register_type(oclass_addr, typename, from_string_fname, to_string_fname):
        pass  # Implement the logic for register_type in Python

    @staticmethod
    def publish_delegate():
        pass  # Implement the logic for publish_delegate in Python

    @staticmethod
    def get_property(objaddr, propertyname):
        pass  # Implement the logic for get_property in Python

    @staticmethod
    def get_property_by_name(objectname, propertyname):
        pass  # Implement the logic for get_property_by_name in Python

    @staticmethod
    def get_value(object_addr, propertyname):
        pass  # Implement the logic for get_value in Python

    @staticmethod
    def set_value(object_addr, propertyname, value):
        pass  # Implement the logic for set_value in Python

    @staticmethod
    def unit_convert(from_unit, to_unit, invalue):
        pass  # Implement the logic for unit_convert in Python

    @staticmethod
    def get_complex_real(object_addr, property_addr):
        pass  # Implement the logic for get_complex_real in Python

    @staticmethod
    def get_complex_imag(object_addr, property_addr):
        pass  # Implement the logic for get_complex_imag in Python

    @staticmethod
    def get_complex_real_by_name(object_addr, propertyname):
        pass  # Implement the logic for get_complex_real_by_name in Python

    @staticmethod
    def get_complex_imag_by_name(object_addr, propertyname):
        pass  # Implement the logic for get_complex_imag_by_name in Python

    @staticmethod
    def get_object(oname):
        pass  # Implement the logic for get_object in Python

    @staticmethod
    def get_object_prop(object_addr, property_addr):
        pass  # Implement the logic for get_object_prop in Python

    @staticmethod
    def get_int16_by_name(object_addr, propertyname):
        pass  # Implement the logic for get_int16_by_name in Python

    @staticmethod
    def get_int32_by_name(object_addr, propertyname):
        pass  # Implement the logic for get_int32_by_name in Python

    @staticmethod
    def get_int64_by_name(object_addr, propertyname):
        pass  # Implement the logic for get_int64_by_name in Python

    @staticmethod
    def get_double_by_name(object_addr, propertyname):
        pass  # Implement the logic for get_double_by_name in Python

    @staticmethod
    def get_string(object_addr, property_addr):
        pass  # Implement the logic for get_string in Python

    @staticmethod
    def get_string_by_name(object_addr, propertyname):
        pass  # Implement the logic for get_string_by_name in Python

    @staticmethod
    def find_objects(findlist_addr, args):
        pass  # Implement the logic for find_objects in Python

    @staticmethod
    def find_next(findlist_addr):
        pass  # Implement the logic for find_next in Python


    @staticmethod
    def create_aggregate(aggregator, group_expression):
        pass  # Implement the logic for create_aggregate in Python

    @staticmethod
    def run_aggregate(aggregate_addr):
        pass  # Implement the logic for run_aggregate in Python

    @staticmethod
    def random_uniform(a, b):
        pass  # Implement the logic for random_uniform in Python

    @staticmethod
    def random_normal(m, s):
        pass  # Implement the logic for random_normal in Python

    @staticmethod
    def random_lognormal(m, s):
        pass  # Implement the logic for random_lognormal in Python

    @staticmethod
    def random_bernoulli(p):
        pass  # Implement the logic for random_bernoulli in Python

    @staticmethod
    def random_pareto(m, a):
        pass  # Implement the logic for random_pareto in Python

    @staticmethod
    def random_sampled(n, x):
        pass  # Implement the logic for random_sampled in Python

    @staticmethod
    def random_exponential(l):
        pass  # Implement the logic for random_exponential in Python

    @staticmethod
    def parsetime(value):
        pass  # Implement the logic for parsetime in Python

    @staticmethod
    def strtime(timestamp, buffer, size):
        pass  # Implement the logic for strtime in Python

    @staticmethod
    def todays(t):
        pass  # Implement the logic for todays in Python

    @staticmethod
    def tohours(t):
        pass  # Implement the logic for tohours in Python

    @staticmethod
    def tominutes(t):
        pass  # Implement the logic for tominutes in Python

    @staticmethod
    def localtime(t, datetime):
        pass  # Implement the logic for localtime in Python

    @staticmethod
    def global_create(name, args):
        pass  # Implement the logic for global_create in Python

    @staticmethod
    def global_setvar(def_, args):
        pass  # Implement the logic for global_setvar in Python

    @staticmethod
    def global_getvar(name):
        pass  # Implement the logic for global_getvar in Python

    @staticmethod
    def global_find(name):
        pass  # Implement the logic for global_find in Python

    @staticmethod
    def bitof(x):
        pass  # Implement the logic for bitof in Python

    @staticmethod
    def name(myaddr):
        pass  # Implement the logic for name in Python

    @staticmethod
    def find_schedule(name):
        pass  # Implement the logic for find_schedule in Python

    @staticmethod
    def schedule_create(name, def_):
        pass  # Implement the logic for schedule_create in Python

    @staticmethod
    def schedule_index(sch, ts):
        pass  # Implement the logic for schedule_index in Python

    @staticmethod
    def schedule_value(sch, index):
        pass  # Implement the logic for schedule_value in Python

    @staticmethod
    def schedule_dtnext(sch, index):
        pass  # Implement the logic for schedule_dtnext in Python

    @staticmethod
    def enduse_create():
        pass  # Implement the logic for enduse_create in Python

    @staticmethod
    def enduse_sync(e, t1):
        pass  # Implement the logic for enduse_sync in Python

    @staticmethod
    def loadshape_create(sched_addr):
        pass  # Implement the logic for loadshape_create in Python

    @staticmethod
    def get_loadshape_value(ls_addr):
        pass  # Implement the logic for get_loadshape_value in Python

    @staticmethod
    def strftime(ts):
        pass  # Implement the logic for strftime in Python

    @staticmethod
    def lerp(t, x0, y0, x1, y1):
        pass  # Implement the logic for lerp in Python

    @staticmethod
    def l1erp(t, x0, y0, x1, y1, x2, y2):
        pass  # Implement the logic for l1erp in Python

    # Other class members and methods go here

    class Property:
        """
        The inner Property class is used to cache published properties from classes in Java modules.

        An extensible class that mirrors the struct PROPERTY in the GridLAB-D core.  Used in GObject,
        but little is done with this class beyond struct-like behavior.  Primarily for internal use and
        passing a property address to GridLAB-D core calls.
        @author Matthew Hauer <matthew.hauer@pnl.gov>
        """
        def __init__(self, name, type, size, offset, addr):
            self.name = name  # Name of this property*/
            self.type = type  # Name of the type of this property (see GridlabD.proptype) */
            self.size = size  # Estimated size of this property, in bytes. */
            self.offset = offset  # Estimated offset within the OBJECT data block in C for this property, in bytes */
            self.addr = addr  # Pointer to the */

        def get_name(self):
            return self.name

        def get_type(self):
            return self.type

        def get_size(self):
            return self.size

        def get_offset(self):
            return self.offset

        def get_addr(self):
            return self.addr

        @classmethod
        def build(cls, name, type, offset, addr):
            size = GridlabD.proptype.get(type)
            if size is None:
                GridlabD.error(f"Unable to create property \"{name}\" of type \"{type}\"")
                return None
            return cls(name, type, size, offset, addr)

        @classmethod
        def build_within_core(cls, name, type, offset, size):
            return cls(name, type, size, offset, None)




WIN32_LEAN_AND_MEAN = 1
DLL_PROCESS_DETACH = 0
DLL_PROCESS_ATTACH = 1

def DllMain(h, r):
    if r == DLL_PROCESS_DETACH:
        do_kill(h)
    return True



if __name__ == "__main__":
    DllMain(None, DLL_PROCESS_ATTACH)
