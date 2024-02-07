import ctypes
import ctypes.util
from enum import Enum

import numpy as np
import os

from gov_pnnl_goss.gridlab.gldcore import Legal
from gov_pnnl_goss.gridlab.gldcore.Class import Class
from gov_pnnl_goss.gridlab.gldcore.Cmdarg import loadall
from gov_pnnl_goss.gridlab.gldcore.Convert import convert_from_set, convert_to_object, convert_from_timestamp
from gov_pnnl_goss.gridlab.gldcore.Exec import Exec, Object
from gov_pnnl_goss.gridlab.gldcore.Find import Find
from gov_pnnl_goss.gridlab.gldcore.Globals import FAILED, global_create, SUCCESS, global_set_var
from gov_pnnl_goss.gridlab.gldcore.Output import output_error, output_message, output_verbose, output_warning, \
    output_raw
from gov_pnnl_goss.gridlab.gldcore.Property import PROPERTYTYPE
from gov_pnnl_goss.gridlab.gldcore.Object import object_name, object_flag_property
from gov_pnnl_goss.gridlab.gldcore.Timestamp import timestamp_current_timezone

# Constants
RHOWATER = 61.82  # lb/cf
CFPGAL = 0.133681  # cf/gal
CWATER = 0.9994  # BTU/lb/F
BTUPHPW = 3.4120  # BTUPH/W
MWPBTUPH = 1e-6 / BTUPHPW  # MW/BTUPH
TS_SECOND = 1.0


class MEXHANDLETYPE(Enum):
    MH_GLOBAL=0x19c3
    MH_OBJECT=0x82a3
    MH_CLASS=0x5d37
    MH_MODULE=0xb40f


# # Useful functions
# def RANDU(L, H):
#     import random
#     return random.uniform(L, H)
#
# def AEQ(A, B, C):
#     return abs(A - B) < C
#
# def ANE(A, B, C):
#     return abs(A - B) >= C
#
# def ALT(A, B, C):
#     return A <= B + C
#
# def AGT(A, B, C):
#     return A >= B - C
#
# def MAX(A, B):
#     return A if A > B else B
#
# def MIN(A, B):
#     return A if A < B else B
#



def make_handle(type, ptr):
    handle = np.zeros((1, 2), dtype=np.int64)
    handle[0, 0] = type
    handle[0, 1] = ptr
    return handle

def make_fieldname(str):
    for i in range(len(str)):
        if not str[i].isalnum():
            str = str[:i] + '_' + str[i+1:]
    return str

def find_object(handle):
    data = handle[0]
    if data[0] == MEXHANDLETYPE.MH_OBJECT:
        return data[1]
    else:
        return None

def find_global(handle):
    data = handle.data_ptr().astype(np.uint64)
    return data[0] == MEXHANDLETYPE.MH_GLOBAL and data[1] or None


def find_class(handle):
    data = np.array(handle)
    if data[0] == MEXHANDLETYPE.MH_CLASS:
        return data[1]
    else:
        return None

def find_module(handle):
    data = handle[0]
    return data[0] == MEXHANDLETYPE.MH_MODULE and data[1] or None


def cmex_getenv(nlhs, plhs, nrhs, prhs):
    if nrhs > 0:
        if isinstance(prhs[0], str):
            name = prhs[0]

            if nlhs == 0:
                value = os.getenv(name)
                if value is None:
                    output_error(f"{name} is not defined")
                else:
                    output_message(f"{name}='{value}'")
            elif nlhs == 1:
                value = os.getenv(name)
                if value is None:
                    output_error(f"{name} is not defined")
                else:
                    plhs.append(value)
            else:
                output_error("getenv does not return more than one value")
        else:
            output_error("Variable name is not a string")
    else:
        output_error("Environment variable name not specified")


def cmex_setenv(nlhs, plhs, nrhs, prhs):
    if nrhs > 1:
        if isinstance(prhs[0], str) and isinstance(prhs[1], str):
            name = prhs[0]
            value = prhs[1]

            if nlhs > 0:
                output_error("setenv does not return a value")
            else:
                env = f"{name}={value}"
                try:
                    os.environ[name] = value
                except Exception as e:
                    output_error(f"Unable to set environment variable: {str(e)}")
        else:
            output_error("Variable name or value is not a string")
    else:
        output_error("Environment name and value not specified")

def cmex_printerr(format, *args):
    count = 0
    buffer = ctypes.create_string_buffer(1024)
    count += ctypes.CDLL(ctypes.util.find_msvcrt()).vsnprintf(buffer, 1024, format, args)
    if buffer.value.startswith(b"ERROR") or buffer.value.startswith(b"FATAL"):
        raise ValueError(buffer.value.decode('utf-8'))
    elif buffer.value.startswith(b"WARN"):
        print(buffer.value.decode('utf-8'))
    else:
        print(buffer.value.decode('utf-8'))
    return count

def cmex_global(nlhs, plhs, nrhs, prhs):
    if nlhs != 0:
        output_error("global does not return a value")
    elif nrhs != 2:
        output_error("global requires a name (arg 1) and an array (arg 2)")
    elif not isinstance(prhs[0], str):
        output_error("global name (arg 1) must be a string")
    else:
        name = prhs[0]
        array = prhs[1]

        if isinstance(array, str):
            if global_create(name, PROPERTYTYPE.PT_char1024, array, PROPERTYTYPE.PT_SIZE, 1, None) is None:
                output_error(f"unable to register string variable '{name}' in globals")
        elif isinstance(array, (list, np.ndarray)):
            size = np.prod(array.shape)
            if isinstance(array, np.ndarray) and array.dtype == np.complex128:
                x = np.zeros(size, dtype=np.complex128)
                x.real = array.real.flatten()
                x.imag = array.imag.flatten()
                x = x.tolist()
            else:
                x = array.flatten().tolist()

            if global_create(name, PROPERTYTYPE.PT_double, x, PROPERTYTYPE.PT_SIZE, size, None) is None:
                output_error(f"unable to register double array variable '{name}' in globals")
        elif isinstance(array, complex):
            x = complex(array.real, array.imag)
            if global_create(name, PROPERTYTYPE.PT_complex, x, PROPERTYTYPE.PT_SIZE, 1, None) is None:
                output_error(f"unable to register complex variable '{name}' in globals")
        elif isinstance(array, (int, float)):
            x = array
            if global_create(name, PROPERTYTYPE.PT_double, x, PROPERTYTYPE.PT_SIZE, 1, None) is None:
                output_error(f"unable to register double variable '{name}' in globals")
        else:
            output_error(f"array (arg 2) type is not supported")


def cmex_object_list(nlhs, plhs, nrhs, prhs):
    criteria = "(undefined)"
    search = None
    fields = ["name", "class", "parent", "flags", "location", "service", "rank", "clock", "handle"]
    list = None

    if nrhs > 0 and prhs[0].size > 0:
        criteria = prhs[0].item().decode("utf-8")

    try:
        search = Find.find_mkpgm(criteria)
        if search is None:
            output_error("gl('list',type='object'): unable to run search '{}'".format(criteria))
            return
    except Exception as e:
        output_error("gl('list',type='object'): unable to read search criteria (arg 2)")

    try:
        if list is None:
            list = Find.find_objects(None, None)
        if list is None:
            output_error("gl('list',type='object'): unable to obtain default list")
            return
    except Exception as e:
        output_error("gl('list',type='object'): unable to search failed")

    try:
        result_list = np.empty(list.hit_count, dtype=[(field, 'U1024') for field in fields])
    except Exception as e:
        output_error("gl('list',type='object'): unable to allocate memory for result list")
        return

    n = 0
    obj = Find.find_first(list)
    while obj is not None:
        try:
            data = np.empty(1, dtype=np.double)
            data[0] = obj.longitude
            result_list[n]["name"] = object_name(obj)
            result_list[n]["class"] = obj.oclass.name
            result_list[n]["parent"] = object_name(obj.parent) if obj.parent else "NONE"
            result_list[n]["flags"] = convert_from_set(
                None, obj.flags, object_flag_property()) if obj.flags else "ERROR"
            result_list[n]["location"] = data
            data = np.empty(1, dtype=np.double)
            data[0] = obj.in_svc / TS_SECOND, obj.out_svc / TS_SECOND
            result_list[n]["service"] = data
            data = np.empty(1, dtype=np.int32)
            data[0] = obj.rank
            result_list[n]["rank"] = data
            data = np.empty(1, dtype=np.double)
            data[0] = obj.clock / TS_SECOND
            result_list[n]["clock"] = data
            result_list[n]["handle"] = make_handle(MEXHANDLETYPE.MH_OBJECT, obj)
        except Exception as e:
            pass
        n += 1
        obj = Find.find_next(list, obj)

    plhs[0] = result_list.view(np.recarray)


def cmex_list(nlhs, plhs, nrhs, prhs):
    type = ""
    if nlhs > 1:
        output_error("gl('list',type=...): returns only one value")
    elif nlhs < 1:
        return
    elif nrhs < 1:
        output_error("gl('list',type=...): needs a type (arg 1)")
    elif prhs[0].itemsize == 1:
        output_error("gl('list',type=...): type (arg 1) should be a string")
    elif type == "object":
        cmex_object_list(nlhs, plhs, nrhs-1, prhs[1:])
    elif type == "global":
        output_error("gl('list',type='{}'): type (arg 1) not implemented".format(type))
    elif type == "class":
        output_error("gl('list',type='{}'): type (arg 1) not implemented".format(type))
    elif type == "module":
        output_error("gl('list',type='{}'): type (arg 1) not implemented".format(type))
    else:
        output_error("gl('list',type='{}'): type (arg 1) not recognized".format(type))

def cmex_version(nlhs, plhs, nrhs, prhs):
    global global_version_major, global_version_minor
    if nlhs > 0:
        res = np.zeros(2)
        plhs[0] = np.asfortranarray(res)
        plhs[0][0] = global_version_major
        plhs[0][1] = global_version_minor
    else:
        Legal.legal_notice()

    return

def cmex_create(nlhs, plhs, nrhs, prhs):
    if nlhs > 1:
        output_error("create only returns one struct")
    elif nrhs < 3 or nrhs % 2 != 1:
        output_error("incorrect number of input arguments")
    elif not isinstance(prhs[0], str):
        output_error("class name (arg 1) must be a string")
    else:
        classname = prhs[0]
        oclass = Class.class_get_class_from_classname(classname)

        if oclass is None:
            output_error(f"class '{classname}' is not registered")
        else:
            obj, result = oclass.create(None)

            if result == FAILED:
                output_error(f"unable to create object of class {classname}")
            else:
                num_properties = (nrhs - 1) // 2
                i = 1

                while i < nrhs:
                    name = prhs[i]

                    if not isinstance(name, str):
                        output_error(f"property name (arg {i}) must be a string")
                        return

                    value = prhs[i + 1]
                    value_str = str(value)

                    if value_str is None:
                        output_error(f"property {name} (arg {i + 1}) value couldn't be converted")
                        return

                    if Object.object_set_value_by_name(obj, name, value_str) == 0:
                        output_error(f"property {name} (arg {i}) couldn't be set to '{value_str}'")
                        return

                    i += 2

                if nlhs > 0:
                    obj_data = Object.get_object_data(obj)

                    if obj_data is not None:
                        plhs.append(obj_data)
                    else:
                        output_error(f"couldn't get object data for {classname}")



def cmex_load(nlhs, plhs, nrhs, prhs):
    if nrhs > 0:
        fname = bytearray(1024)
        if not prhs[0].dtype == 'str':
            output_error("Model name is not a string")
        elif nlhs > 0:
            output_error("load does not return a value")
        elif prhs[0].tostring(fname) != 0:
            output_error("Model name too long")
        elif loadall(fname) == FAILED:
            output_error("Model load failed")
        else:
            output_message("Model %s loaded ok" % fname.decode())
    else:
        output_error("Module not specified")


def cmex_start(nlhs, plhs, nrhs, prhs):
    global global_keep_progress
    global_keep_progress = 1
    result = Exec.exec_start()

    if result == FAILED:
        output_error("Simulation failed!")

def module_find(fname):
    # Your implementation here
    return None  # Replace with the appropriate return value

def module_load(fname, i, none):
    # Your implementation here
    return None  # Replace with the appropriate return value

def module_getvar(mod, varname, buffer, size):
    # Your implementation here
    return False  # Replace with the appropriate return value

def mxIsChar(p):
    # Your implementation here
    return False  # Replace with the appropriate return value

def mxGetString(p, name, sizeof):
    # Your implementation here
    return 0  # Replace with the appropriate return value

def mxCreateString(s):
    # Your implementation here
    return None  # Replace with the appropriate return value

def mxCreateNumericMatrix(m, n, mxUINT32_CLASS, mxREAL):
    # Your implementation here
    return None  # Replace with the appropriate return value

def mxGetPr(value):
    # Your implementation here
    return None  # Replace with the appropriate return value

def mxGetData(handle):
    pass

def mxCreateDoubleMatrix(param, param1, mxREAL):
    pass

def mxCreateStructMatrix(param, param1, nFields, fnames):
    pass

def mxSetFieldByNumber(param, param1, param2, handle):
    pass


# def cmex_module(nlhs, plhs, nrhs, prhs):
#     if nrhs > 0:
#         modulename = str(prhs[0])
#         mod = module_find(modulename)
#         if mod is None:
#             mod = module_load(modulename, 0, None)
#             if mod is None:
#                 output_error("Module load failed")
#         if nlhs == 0:
#             output_message("Module '{}({}.{})' loaded ok".format(mod.name, mod.major, mod.minor))
#         else:
#             field_names = ["handle", "name", "major", "minor"]
#             name = mxCreateString(mod.name)
#             handle = mxCreateNumericMatrix(1, 1, sizeof(int32) == sizeof(int) ? mxUINT32_CLASS : mxUINT64_CLASS, mxREAL)
#             major = mxCreateNumericMatrix(1, 1, mxUINT8_CLASS, mxREAL)
#             minor = mxCreateNumericMatrix(1, 1, mxUINT8_CLASS, mxREAL)
#             value = [None] * 256
#             pHandle = mxGetData(handle)
#             pMajor = mxGetData(major)
#             pMinor = mxGetData(minor)
#             pHandle[0] = int(mod.hLib)
#             pMajor[0] = int(mod.major)
#             pMinor[0] = int(mod.minor)
#             varname = ""
#             nFields = 4
#             vnames = ["" for _ in range(256)]
#
#             while module_getvar(mod, varname, None, 0):
#                 buffer = ""
#                 if module_getvar(mod, varname, buffer, sizeof(buffer)) and nFields < sizeof(fname) / sizeof(fname[0]):
#                     pVal = mxCreateDoubleMatrix(1, 1, mxREAL)
#                     pVal[0] = float(buffer)
#                     vnames[nFields] = varname
#                     field_names.append(vnames[nFields])
#                     value[nFields] = pVal
#                     nFields += 1
#
#             plhs[0] = mxCreateStructMatrix(1, 1, nFields, field_names)
#             mxSetFieldByNumber(plhs[0], 0, 0, handle)
#             mxSetFieldByNumber(plhs[0], 0, 1, name)
#             mxSetFieldByNumber(plhs[0], 0, 2, major)
#             mxSetFieldByNumber(plhs[0], 0, 3, minor)
#             for i in range(nFields - 4):
#                 mxSetFieldByNumber(plhs[0], 0, i + 4, value[i + 4])
#     else:
#         output_error("Module not specified")
#


def cmex_module(nlhs, plhs, nrhs, prhs):
    mxUINT64_CLASS = 1
    mxUINT8_CLASS = 2
    mxREAL = 3

    if nrhs > 0:
        fname = ""
        mod = None
        if not mxIsChar(prhs[0]):
            output_error("Module name is not a string")
        elif nlhs > 1:
            output_error("Only one return value is possible")
        elif mxGetString(prhs[0], fname, 1) != 0:
            output_error("Module name too long")
        elif (mod := module_find(fname)) is None and (mod := module_load(fname, 0, None)) is None:
            output_error("Module load failed")
        elif nlhs == 0:
            output_message(f"Module '{mod.name}({mod.major}.{mod.minor})' loaded ok")
        else:
            fnames = ["handle", "name", "major", "minor"]
            name = mxCreateString(mod.name)
            handle = mxCreateNumericMatrix(1, 1, mxUINT64_CLASS, mxREAL)
            major = mxCreateNumericMatrix(1, 1, mxUINT8_CLASS, mxREAL)
            minor = mxCreateNumericMatrix(1, 1, mxUINT8_CLASS, mxREAL)
            value = [None] * 256
            pHandle = mxGetData(handle)
            pMajor = mxGetData(major)
            pMinor = mxGetData(minor)
            varname = ""
            nFields = 4
            vnames = [""] * 256
            pHandle[0] = int(mod.hLib)
            pMajor[0] = int(mod.major)
            pMinor[0] = int(mod.minor)

            while module_getvar(mod, varname, None, 0):
                buffer = ""
                if module_getvar(mod, varname, buffer, 1) and nFields < len(fnames):
                    output_verbose(f"module variable {varname} = '{buffer}'")
                    value[nFields] = mxCreateDoubleMatrix(1, 1, mxREAL)
                    pVal = mxGetPr(value[nFields])
                    pVal[0] = float(buffer)
                    vnames[nFields] = varname
                    fnames[nFields] = vnames[nFields]
                    nFields += 1

            plhs[0] = mxCreateStructMatrix(1, 1, nFields, fnames)
            mxSetFieldByNumber(plhs[0], 0, 0, handle)
            mxSetFieldByNumber(plhs[0], 0, 1, name)
            mxSetFieldByNumber(plhs[0], 0, 2, major)
            mxSetFieldByNumber(plhs[0], 0, 3, minor)

            while nFields > 4:
                nFields -= 1
                mxSetFieldByNumber(plhs[0], 0, nFields, value[nFields])

    else:
        output_error("Module not specified")
    return


def object_get_property(obj, prop_name):
    pass


def set_object_data(param):
    pass


def object_set_value_by_name(obj, prop_name, value):
    pass


def object_set_double_by_name(obj, prop_name, value):
    pass



def cmex_set(nlhs, plhs, nrhs, prhs):
    if nlhs > 0:
        print("set does not return a value")
    elif nrhs == 1 and isinstance(prhs[0], dict):
        set_object_data(prhs[0])
    elif nrhs != 3:
        print("set requires either a structure, or object id, property name, and value")
    elif not isinstance(prhs[0], str):
        print("object id (arg 0) must be a string")
    elif isinstance(prhs[1], str):
        obj = None
        prop = None
        value = ""
        object_name = prhs[0]

        if len(object_name) > 1024:
            print("object name (arg 0) too long")
            return

        if object_name == "global":
            if not isinstance(prhs[1], str):
                print("global variable name is not a string")
            elif not isinstance(prhs[2], str):
                print("global value is not a string")
            else:
                variable_name = prhs[1]
                variable_value = prhs[2]

                if global_set_var(variable_name, variable_value) != SUCCESS:
                    print("unable to set global '{}' to '{}'".format(variable_name, variable_value))
        else:
            object_id = object_name
            if convert_to_object(object_id, obj, None) == 0:
                print("object (arg 0) {} not found".format(object_id))
            elif len(prhs[1]) > 1024:
                print("property name (arg 1) too long")
            else:
                prop_name = prhs[1]
                if object_get_property(obj, prop_name) is None:
                    print("property name (arg 1) {} not found in object {}:{}".format(
                        prop_name, obj.oclass.name, obj.id))
                elif isinstance(prhs[2], str):
                    value = prhs[2]
                    if object_set_value_by_name(obj, prop_name, value) == 0:
                        print("unable to set {}:{}/{} to {}".format(
                            obj.oclass.name, obj.id, prop_name, value))
                elif isinstance(prhs[2], float) and object_get_property(obj, prop_name).ptype == PROPERTYTYPE.PT_double:
                    value = prhs[2]
                    if object_set_double_by_name(obj, prop_name, value) == 0:
                        print("unable to set {}:{}/{} to {}".format(
                            obj.oclass.name, obj.id, prop_name, value))
                elif isinstance(prhs[2], (complex, float)):
                    real_value = prhs[2].real
                    imag_value = prhs[2].imag
                    value = "{}{:+g}i".format(real_value, imag_value)
                    if object_set_value_by_name(obj, prop_name, value) == 0:
                        print("unable to set {}:{}/{} to {}".format(
                            obj.oclass.name, obj.id, prop_name, value))
                else:
                    print("value (arg 2) has an unsupported data type")
    else:
        print("property or data (arg 1) type is not valid")

def cmex_get(nlhs, plhs, nrhs, prhs):
    global global_clock
    if nrhs > 0:
        name = ""
        obj = None
        if not isinstance(prhs[0], str):
            print("entity name (arg 1) is not a string")
        elif nlhs > 1:
            print("only one return value is possible")
        else:
            name = prhs[0]
            if name == "clock":
                timestamp = float(global_clock) / TS_SECOND
                timestring = convert_from_timestamp(global_clock, "", 0)
                timezone = timestamp_current_timezone()
                result = {
                    "timestamp": timestamp,
                    "timestring": timestring if timestring else "(error)",
                    "timezone": timezone,
                }
                plhs[0] = result
            elif name.startswith("property.") and nrhs > 1:
                _, propname = name.split(".", 1)
                classname, propname = propname.split(".", 1)
                pClass = Class.class_get_class_from_classname(classname)
                if pClass:
                    pProp = Class.class_find_property(pClass, propname)
                    if pProp:
                        result = {
                            "class": classname,
                            "name": pProp.name,
                            "type": Class.class_get_property_typename(pProp.ptype),
                            "size": pProp.size if pProp.size else 1,
                            "access": "(na)",  # Implement access info if needed
                            "unit": pProp.unit.name,
                            "delegation": pProp.delegation.oclass.name if pProp.delegation else "(none)",
                            "keywords": "(na)",  # Implement keywords if needed
                        }
                        plhs[0] = result
                    else:
                        print("property %s is not found in class %s" % (propname, classname))
                else:
                    print("class %s is not found" % classname)
            elif name == "global":
                # Replace with your implementation for global variables
                pass
            else:
                if not convert_to_object(name, obj, None):
                    # Replace with your implementation for object-related data retrieval
                    pass
                else:
                    print("entity '%s' not found" % name)
    else:
        print("object not specified")

class CMDMAP:
    def __init__(self, name, call, brief, detail):
        self.name = name
        self.call = call
        self.brief = brief
        self.detail = detail



# Define other functions similarly as above.

def mexFunction(nlhs, plhs, nrhs, prhs):
    first = 1
    key = ""
    i = 0

    if first == 1:
        first = 0
        # mexLock()
        # output_set_stdout(mexPrintf)
        # output_set_stderr(cmex_printerr)
        # legal_license()
        # exec_init()

    if nrhs < 1:
        output_error("Use gl('help') for a list of commands.")
        return

    if not mxIsChar(prhs[0]):
        output_error("token must be a string")
        return

    if mxGetString(prhs[0], key, len(key)) != 0:
        output_warning("GridLAB key string too long")

    for i in range(len(CMDMAP)):
        if key == CMDMAP[i].name:
            if CMDMAP[i].call is None:
                if nrhs == 1:
                    output_raw("Available top-level commands\n")
                    for j in range(len(CMDMAP)):
                        output_raw("\t{}\t{}\n".format(CMDMAP[j].name, CMDMAP[j].brief))
                    output_raw("Use gl('help',command) for details\n")
                    return
                elif mxIsChar(prhs[1]):
                    cmd = ""
                    if mxGetString(prhs[1], cmd, len(cmd)) != 0:
                        output_warning("command string too long to read fully")

                    for j in range(len(CMDMAP)):
                        if cmd == CMDMAP[j].name:
                            output_raw("Help for command '{}'\n\n{}\n".format(cmd, CMDMAP[j].detail if CMDMAP[j].detail else "\tNo details available\n"))
                            return

                    output_error("Command '{}' does not exist".format(cmd))
                    return
                else:
                    output_error("command must be a string")
                    return
            else:
                CMDMAP[i].call(nlhs, plhs, nrhs - 1, prhs + 1)
                return

    nret = nlhs
    output_error("unrecognized GridLAB operation--gl('help') for list")
    while nret > 0:
        mxREAL =1
        plhs[nret - 1] = mxCreateDoubleMatrix(0, 0, mxREAL)
        nret -= 1
