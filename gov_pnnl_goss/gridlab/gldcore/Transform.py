from enum import Enum
import numpy as np

from gov_pnnl_goss.gridlab.gldcore.object1702152845 import object_name


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

class PROPERTYTYPE(Enum):
    # Define your property types here
    pass

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
        return var[n].prop.ptype

    def gldvar_get_name(self, var, n):
        return var[n].prop.name

    # Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
    def gldvar_get_string(self, var, n, buffer, size):
        if self.gldvar_isset(var, n):
            pspec = property_get_spec(var[n].prop.ptype)
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


class Transform:
    def __init__(self):
        self.source = None
        self.source_type = 0
        self.target_obj = None
        self.target_prop = None
        self.function_type = 0
        self.linear_data = None
        self.external_data = None
        self.filter_data = None
        self.next = None

    def getnext(self, xform):
        pass

    def transform_add_external(self, target_obj, target_prop, function, source_obj, source_prop):
        pass

    def transform_add_linear(self, stype, source, target, scale, bias, obj, prop, s):
        pass

    def transform_get_next(self, xform):
        return xform.next if xform else schedule_xformlist

    def transform_syncall(self, t, source, t1_dbl):
        pass

    def transform_apply(self, t1, xform, source, dm_time):
        pass

    def transform_add_filter(self, target_obj, target_prop, function, source_obj, source_prop):
        pass

    def transform_saveall(self, fp):
        count = 0
        xform = schedule_xformlist
        while xform is not None:
            obj = xform.target_obj
            prop = xform.target_prop
            name = [0] * 1024
            object_name(obj, name, len(name))
            count += fp.write(f"#warning transform to {name.decode('utf-8')}.{prop.name} was not saved\n")
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
    if prop.ptype == PROPERTYTYPE.PT_double:
        source_type = XS_DOUBLE
    elif prop.ptype == PROPERTYTYPE.PT_complex:
        source_type = XS_COMPLEX
    elif prop.ptype == PROPERTYTYPE.PT_loadshape:
        source_type = XS_LOADSHAPE
    elif prop.ptype == PROPERTYTYPE.PT_enduse:
        source_type = XS_ENDUSE
    elif prop.ptype == PROPERTYTYPE.PT_random:
        source_type = XS_RANDOMVAR
    else:
        output_error("tranform/get_source_type(PROPERTY *prop='%s'): unsupported source property type '%s'",
                      prop.name,property_getspec(prop.ptype).name)
    return source_type


# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
def transform_add_filter(target_obj, target_prop, filter_str, source_obj, source_prop):
    buffer1 = [1024]
    buffer2 = [1024]
    xform = None
    tf = None
    
    tf = find_filter(filter_str)
    if tf is None:
        output_error("transform_add_filter(source='{}:{}', filter='{}', target='{}:{}'): transfer function not defined".format(
            object_name(target_obj, buffer1, len(buffer1)), target_prop.name, filter_str,
            object_name(source_obj, buffer2, len(buffer2)), source_prop.name)
        )
        return 0

    xform = TRANSFORM()
    if xform is None:
        output_error("transform_add_filter(source='{}:{}', filter='{}', target='{}:{}'): memory allocation failure".format(
            object_name(target_obj, buffer1, len(buffer1)), target_prop.name, filter_str,
            object_name(source_obj, buffer2, len(buffer2)), source_prop.name)
        )
        return 0

    xform.x = [0] * (tf.n - 1)

    xform.source = static_cast(object_get_addr(source_obj, source_prop.name), double)
    xform.source_type = static_cast(get_source_type(source_prop), TRANSFORMSOURCE)
    xform.target_obj = target_obj
    xform.target_prop = target_prop
    xform.function_type = XT_FILTER
    xform.tf = tf
    xform.y = static_cast(object_get_addr(target_obj, target_prop.name), double)
    xform.t2 = int64(global_starttime / tf.timestep) * tf.timestep + tf.timeskew
    xform.t2_dbl = floor(double(global_starttime / tf.timestep)) * tf.timestep + tf.timeskew
    xform.next = schedule_xformlist
    schedule_xformlist = xform

    if global_debug_output:
        output_debug("added filter '{}' from source '{}:{}' to target '{}:{}'".format(filter_str,
            object_name(target_obj, buffer1, len(buffer1)), target_prop.name, object_name(source_obj, buffer2, len(buffer2)), source_prop.name)
        )
    
    return 1


# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
def transform_add_external(target_obj, target_prop, function, source_obj, source_prop):
    buffer1 = [1024]
    buffer2 = [1024]
    xform = TRANSFORM()
    if xform is None:
        return 0
    xform.function = module_get_transform_function(function)
    if xform.function is None:
        output_error("transform_add_external(source='%s:%s',function='%s',target='%s:%s'): function is not defined (probably a missing or invalid extern directive)" 
            % (object_name(target_obj, buffer1, buffer1.size), target_prop.name, function, object_name(source_obj, buffer2, buffer2.size), source_prop.name))
        free(xform)
        return 0
    xform.function_type = XT_EXTERNAL
    xform.source_type = get_source_type(source_prop)
    xform.nlhs = 1
    xform.plhs = gldvar_create(xform.nlhs)
    gldvar_set(xform.plhs, 0, object_get_addr(target_obj, target_prop.name), target_prop)
    xform.target_obj = target_obj
    xform.target_prop = target_prop
    xform.nrhs = 1
    xform.prhs = gldvar_create(xform.nrhs)
    gldvar_set(xform.prhs, 0, object_get_addr(source_obj, source_prop.name), source_prop)
    xform.next = schedule_xformlist
    schedule_xformlist = xform
    output_debug("added external transform %s:%s <- %s(%s:%s)" % (object_name(target_obj, buffer1, buffer1.size), target_prop.name, function, object_name(source_obj, buffer2, buffer2.size), source_prop.name))
    return 1


# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
def transform_add_linear(stype, source, target, scale, bias, obj, prop, sched):
    buffer = [0] * 1024
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
    xform.function_type = XT_LINEAR
    xform.next = schedule_xformlist
    schedule_xformlist = xform
    output_debug("added linear transform %s:%s <- scale=%.3g, bias=%.3g" % (object_name(obj, buffer, 1024), prop.name, scale, bias))
    return 1


# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
def cast_from_double(ptype, addr, value):
    if ptype == PROPERTYTYPE.PT_void:
        pass
    elif ptype == PROPERTYTYPE.PT_double:
        addr[0] = value
    elif ptype == PROPERTYTYPE.PT_complex:
        addr.SetReal(value)
        addr.SetImag(0)
    elif ptype == PROPERTYTYPE.PT_bool:
        addr[0] = int(value != 0)
    elif ptype == PROPERTYTYPE.PT_int16:
        addr[0] = int(value)
    elif ptype == PROPERTYTYPE.PT_int32:
        addr[0] = int(value)
    elif ptype == PROPERTYTYPE.PT_int64:
        addr[0] = int(value)
    elif ptype == PROPERTYTYPE.PT_enumeration:
        addr[0] = int(value)
    elif ptype == PROPERTYTYPE.PT_set:
        addr[0] = int(value)
    elif ptype == PROPERTYTYPE.PT_object:
        pass
    elif ptype == PROPERTYTYPE.PT_timestamp:
        addr[0] = int(value)
    elif ptype == PROPERTYTYPE.PT_float:
        addr[0] = float(value)
    elif ptype == PROPERTYTYPE.PT_loadshape:
        addr.load = value
    elif ptype == PROPERTYTYPE.PT_enduse:
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
