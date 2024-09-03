from enum import Enum
import numpy as np

from gov_pnnl_goss.gridlab.gldcore.Object import Object
from gov_pnnl_goss.gridlab.gldcore.Output import output_error, output_debug
from gridlab.gldcore.Module import Module
from gridlab.gldcore.PropertyHeader import PropertyType


class LINEARTRANSFORMDATA:
    def __init__(self):
        self.source_addr = None
        self.source_schedule = None
        self.target = None
        self.scale = None
        self.bias = None


class EXTERNALTRANSFORMDATA:
    def __init__(self):
        self.function = None
        self.retval = None
        self.nlhs = None
        self.plhs = None
        self.nrhs = None
        self.prhs = None


class FILTERTRANSFORMDATA:
    def __init__(self):
        self.tf = None,
        self.u = None
        self.y = None
        self.x = None
        self.t2 = None
        self.t2_dbl = None

class TRANSFORMSOURCE(Enum):
    XS_UNKNOWN = 0x00
    XS_DOUBLE = 0x01
    XS_COMPLEX = 0x02
    XS_LOADSHAPE = 0x04
    XS_ENDUSE = 0x08
    XS_SCHEDULE = 0x10
    XS_RANDOMVAR = 0x20
    XS_ALL = 0x1f

class TRANSFORMFUNCTIONTYPE(Enum):
    XT_LINEAR = 0x00
    XT_EXTERNAL = 0x01
    XT_FILTER = 0x04


class UNIT:
    # Define your UNIT structure here
    pass



# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
class GlbVar:
    def __init__(self, dim):
        self.addr = None
        self.prop = None

    def isset(self, var, n):
        pass

    def set(self, var, n, addr, prop):
        pass

    def unset(self, var, n):
        pass

    def getaddr(self, var, n):
        pass

    def getprop(self, var, n):
        pass

    def gettype(self, var, n):
        pass

    def getname(self, var, n):
        pass

    def getstring(self, var, n, buffer, size):
        pass

    def getunits(self, var, n):
        pass

    def gldvar_create(self, dim):
        vars = None
        vars = (GLDVAR*dim)(len(GLDVAR)*dim)
        vars = [0]*dim
        return vars

    def gldvar_isset(self, var, n):
        return var[n]["addr"] != None

    def gldvar_set(self, var, n, addr, prop):
        var[n]["addr"] = addr
        var[n]["prop"] = prop

    def gldvar_unset(self, var, n):
        var[n]['addr'] = var[n]['prop'] = None

    def gldvar_getaddr(self, var, n):
        return var[n].addr

    def gldvar_getprop(self, var, n):
        return var[n]["prop"]

    def gldvar_gettype(self, var, n):
        pass

    def gldvar_getname(self, var, n):
        pass

    def gldvar_getstring(self, var, n, buffer, size):
        pass

    def gldvar_getunits(self, var, n):
        pass

    # Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
    def gldvar_get_type(self, var, n):
        return var[n].prop.global_property_types

    def gldvar_get_name(self, var, n):
        return var[n].prop.name

    # Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
    def gldvar_get_string(self, var, n, buffer, size):
        if self.gldvar_isset(var, n):
            pspec = PropertyType.property_get_spec(var[n].prop.global_property_types)
            pspec.data_to_string(buffer, size, var[n].addr, var[n].prop)
            return buffer
        else:
            return buffer[:size].ljust(size, '\0') if len(buffer) >= size else buffer.ljust(size, '\0')


    def gldvar_get_units(self, var, n):
        if self.gldvar_isset(var, n):
            return var[n].prop.unit
        else:
            return None


GLDVAR = GlbVar

# class Schedule:
#     pass  # Placeholder for SCHEDULE structure
#
class TransformFunction:
    pass  # Placeholder for TRANSFORMFUNCTION structure
#
# class TransferFunction:
#     pass  # Placeholder for TRANSFERFUNCTION structure
#
# class GLDVar:
#     pass  # Placeholder for GLDVAR structure
#
# class TransformSource:
#     pass  # Placeholder for TRANSFORMSOURCE enumeration
#
# class TransformFunctionType:
#     pass  # Placeholder for TRANSFORMFUNCTIONTYPE enumeration
#
# class ObjectList:
#     pass  # Placeholder for s_object_list structure
#
# class PropertyMap:
#     pass  # Placeholder for s_property_map structure


class Transform:
    def __init__(self):
        self.linear_data = None
        self.external_data = None
        self.filter_data = None

        self.source = None  # Initially None, can be set to reference an array of doubles
        self.source_type = None  # Instance of TransformSource
        self.target_obj = None  # Instance of ObjectList
        self.target_prop = None  # Instance of PropertyMap
        self.function_type = None  # Instance of TransformFunctionType

        # Attributes for linear transforms
        self.source_addr = None  # Can be any global_property_types, depending on usage
        self.source_schedule = None  # Instance of Schedule
        self.target = None  # Initially None, can be set to reference an array of doubles
        self.scale = None  # double
        self.bias = None  # double

        # Attributes for external transforms
        self.function = None  # Instance of TransformFunction
        self.retval = None  # int
        self.nlhs = None  # int
        self.plhs = None  # List of GLDVar
        self.nrhs = None  # int
        self.prhs = None  # List of GLDVar

        # Attributes for filter transforms
        self.tf = None  # Instance of TransferFunction
        self.u = None  # vector u
        self.y = None  # vector y
        self.x = None  # vector x
        self.t2 = None  # TIMESTAMP, assuming a placeholder for datetime or int
        self.t2_dbl = None  # double

        self.next = None  # Reference to next Transform object in the list

    def getnext(self, xform):
        return self.next

    def transform_add_external(self, target_obj, target_prop, function, source_obj, source_prop):
        pass

    def transform_add_linear(self, stype, source, target, scale, bias, obj, prop, s):
        pass

    def transform_get_next(self, xform):
        global schedule_xformlist
        return xform.next if xform else schedule_xformlist

    def transform_syncall(self, t, source, t1_dbl):
        pass

    def transform_apply(self, t1, xform, source, dm_time):
        pass

    def transform_add_filter(self, target_obj, target_prop, function, source_obj, source_prop):
        pass

    def transform_saveall(self, fp):
        count = 0
        xform = Transform()
        while xform is not None:
            obj = xform.target_obj
            prop = xform.target_prop
            name= Object.object_name(obj)
            count += fp.write(f"#warning transform to {name}.{prop.name} was not saved\n")
            xform = xform.next
        return count


TRANSFORM = Transform


class TransferFunction:
    tflist = []
    def __init__(self):
        self.name = "" # transfer function name
        self.domain = ""  # domain variable name
        self.timestep = 0.0  # timestep (seconds)
        self.timeskew = 0.0  # timeskew (seconds)
        self.n = 0  # denominator order
        self.a = None  # denominator coefficients (list or array)
        self.m = 0  # numerator order
        self.b = None  # numerator coefficients (list or array)
        self.next = None

    def write_term(self, buffer, a, x, n, first):
        pass

    def add(self, name, domain, timestep, timeskew, n, a, m, b):
        pass

    def find_filter(self, name):
        pass

    def transfer_function_add(self, tfname, domain, timestep, timeskew, n, a, m, b):
        pass

TRANSFERFUNCTION = TransferFunction
tflist = []  # transfer function list

class PropertyType:
    def get_source_type(self, prop):
        pass

    def add_filter(self, target_obj, target_prop, filter, source_obj, source_prop):
        pass

    def add_external(self, target_obj, target_prop, function, source_obj, source_prop):
        pass

    def add_linear(self, stype, source, target, scale, bias, obj, prop, sched):
        pass

    def cast_from_double(self, ptype, addr, value):
        pass


class Timestamp:
    def apply_filter(self, f, u, x, y, t1, dm_time):
        pass

    def transform_apply(self, t1, xform, source, dm_time):
        pass

    def syncall(self, t1, source, t1_dbl):
        pass

    def saveall(self, fp):
        pass



def find_filter(name):
    tf = tflist
    while tf is not None:
        if tf.name == name:
            return tf
        tf = tf.next
    return None

# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
def get_source_type(prop):
    source_type = 0
    if prop.global_property_types == PropertyType.PT_double:
        source_type = TRANSFORMSOURCE.XS_DOUBLE
    elif prop.global_property_types == PropertyType.PT_complex:
        source_type = TRANSFORMSOURCE.XS_COMPLEX
    elif prop.global_property_types == PropertyType.PT_loadshape:
        source_type = TRANSFORMSOURCE.XS_LOADSHAPE
    elif prop.global_property_types == PropertyType.PT_enduse:
        source_type = TRANSFORMSOURCE.XS_ENDUSE
    elif prop.global_property_types == PropertyType.PT_random:
        source_type = TRANSFORMSOURCE.XS_RANDOMVAR
    else:
        output_error("tranform/get_source_type(PROPERTY *prop='%s'): unsupported source property global_property_types '%s'",
                     prop.name, PropertyType.property_getspec(prop.global_property_types).name)
    return source_type


# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
def transform_add_filter(target_obj, target_prop, filter_str, source_obj, source_prop):
    global global_start_time, global_debug_output


    tf = find_filter(filter_str)
    if tf is None:
        output_error("transform_add_filter(source='{}:{}', filter='{}', target='{}:{}'): transfer function not defined".format(
            Object.object_name(target_obj), target_prop.name, filter_str,
            Object.object_name(source_obj), source_prop.name)
        )
        return 0

    xform = TRANSFORM()
    if xform is None:
        output_error("transform_add_filter(source='{}:{}', filter='{}', target='{}:{}'): memory allocation failure".format(
            Object.object_name(target_obj), target_prop.name, filter_str,
            Object.object_name(source_obj), source_prop.name)
        )
        return 0

    xform.x = [0] * (tf.n - 1)

    xform.source = Object.object_get_addr(source_obj, source_prop.name)
    xform.source_type = Transform.get_source_type(source_prop)
    xform.target_obj = target_obj
    xform.target_prop = target_prop
    xform.function_type = TRANSFORMFUNCTIONTYPE.XT_FILTER
    xform.tf = tf
    xform.y = Transform.object_get_addr(target_obj, target_prop.name)
    xform.t2 = int(global_start_time / tf.timestep) * tf.timestep + tf.timeskew
    xform.t2_dbl = int(float(global_start_time / tf.timestep)) * tf.timestep + tf.timeskew
    schedule_xformlist = Transform()
    xform.next = schedule_xformlist
    schedule_xformlist = xform

    if global_debug_output:
        output_debug("added filter '{}' from source '{}:{}' to target '{}:{}'".format(filter_str,
            Object.object_name(target_obj), target_prop.name, Object.object_name(source_obj), source_prop.name)
        )
    
    return 1


# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
def transform_add_external(target_obj, target_prop, function, source_obj, source_prop):
    global schedule_xformlist
    xform = TRANSFORM()
    if xform is None:
        return 0
    xform.function = Module.module_get_transform_function(function)
    if xform.function is None:
        output_error("transform_add_external(source='%s:%s',function='%s',target='%s:%s'): function is not defined (probably a missing or invalid extern directive)" 
            % (Object.object_name(target_obj), target_prop.name, function, Object.object_name(source_obj), source_prop.name))
        return 0
    xform.function_type = TRANSFORMFUNCTIONTYPE.XT_EXTERNAL
    xform.source_type = get_source_type(source_prop)
    xform.nlhs = 1
    xform.plhs = GlbVar.gldvar_create(xform.nlhs)
    GlbVar.gldvar_set(xform.plhs, 0, Transform.object_get_addr(target_obj, target_prop.name), target_prop)
    xform.target_obj = target_obj
    xform.target_prop = target_prop
    xform.nrhs = 1
    xform.prhs = GlbVar.gldvar_create(xform.nrhs)
    GlbVar.gldvar_set(xform.prhs, 0, Transform.object_get_addr(source_obj, source_prop.name))
    xform.next = schedule_xformlist
    schedule_xformlist = xform
    output_debug("added external transform %s:%s <- %s(%s:%s)" % (Object.object_name(target_obj), target_prop.name, function, Object.object_name(source_obj), source_prop.name))
    return 1


# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
def transform_add_linear(stype, source, target, scale, bias, obj, prop, sched):
    global schedule_xformlist
    xform = TRANSFORM()
    if xform is None:
        return 0
    xform.source_type = stype
    xform.source = source
    xform.nrhs = 1
    xform.nlhs = 1
    xform.source_addr = source
    xform.source_schedule = sched
    xform.target_obj = obj
    xform.target_prop = prop
    xform.target = target
    xform.scale = scale
    xform.bias = bias
    xform.function_type = TRANSFORMFUNCTIONTYPE.XT_LINEAR
    xform.next = schedule_xformlist
    schedule_xformlist = xform
    output_debug("added linear transform %s:%s <- scale=%.3g, bias=%.3g" % (Object.object_name(obj), prop.name, scale, bias))
    return 1


# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
def cast_from_double(ptype, addr, value):
    if ptype == PropertyType.PT_void:
        pass
    elif ptype == PropertyType.PT_double:
        addr[0] = value
    elif ptype == PropertyType.PT_complex:
        addr.SetReal(value)
        addr.SetImag(0)
    elif ptype == PropertyType.PT_bool:
        addr[0] = int(value != 0)
    elif ptype == PropertyType.PT_int16:
        addr[0] = int(value)
    elif ptype == PropertyType.PT_int32:
        addr[0] = int(value)
    elif ptype == PropertyType.PT_int64:
        addr[0] = int(value)
    elif ptype == PropertyType.PT_enumeration:
        addr[0] = int(value)
    elif ptype == PropertyType.PT_set:
        addr[0] = int(value)
    elif ptype == PropertyType.PT_object:
        pass
    elif ptype == PropertyType.PT_timestamp:
        addr[0] = int(value)
    elif ptype == PropertyType.PT_float:
        addr[0] = float(value)
    elif ptype == PropertyType.PT_loadshape:
        addr.load = value
    elif ptype == PropertyType.PT_enduse:
        addr.total.SetReal(value)
    else:
        pass

def apply_filter(transfer_function, u, x, y, t1, dm_time):
    n = transfer_function.n - 1
    m = transfer_function.m
    a = transfer_function.a
    b = transfer_function.b
    dx = np.zeros(64)
    curr_dbl_time = dm_time

    if n > len(dx):
        raise ValueError("transfer function order too high")
    
    for i in range(n):
        if i == 0:
            dx[i] = -a[i] * x[n-1]
        else:
            dx[i] = x[i-1] - a[i] * x[n-1]
        
        if i < m:
            dx[i] += b[i] * u
    
    np.copyto(x, dx)

    y[0] = x[n-1]

    dm_time[0] = curr_dbl_time + transfer_function.timestep + transfer_function.timeskew

    return int(t1 / transfer_function.timestep + 1) * transfer_function.timestep + transfer_function.timeskew
