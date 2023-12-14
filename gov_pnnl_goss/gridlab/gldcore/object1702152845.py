

# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
import ctypes

def object_get_oflags(extflags):
    flag_size = ctypes.sizeof(oflags)

    extflags[0] = ctypes.cast(module_malloc(flag_size), ctypes.POINTER(KEYWORD))

    if extflags[0] is None:
        output_error("object_get_oflags: malloc failure")
        errno = ENOMEM
        return -1

    ctypes.memcpy(extflags[0], oflags, flag_size)

    return flag_size // ctypes.sizeof(KEYWORD)


def object_flag_property():
    flags = {"value": 0, "name": "flags", "type": "set", "size": 1, "max_size": 8, "attribute": "public", "data": None, "pointer": (void*)-4, "function1": None, "function2": oflags, "function3": None}
    return flags

def object_access_property():
    flags = {"value": 0, "name": "access", "type": "enumeration", "size": 1, "precision": 8, "access": "public", "data": None, "pointer": (void*) -4, "function_pointer": oaccess, "other": None}
    return flags

def object_get_count():
    return next_object_id - deleted_object_count

# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
def object_build_object_array():
    tcount = object_get_count()
    i = 0
    optr = object_get_first()

    if object_array is not None:
        free(object_array)
        object_array = None

    object_array = (ctypes.c_void_p * tcount)()
    if object_array is None:
        return 0

    object_array_size = tcount

    for i in range(tcount):
        object_array[i] = optr
        optr = optr.next

    return object_array_size


# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
def object_prop_in_class(obj, prop):
    if prop is None:
        return None
    
    if obj is not None:
        return class_prop_in_class(obj.oclass, prop)
    else:
        return None


# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
def object_name(obj, oname, size):
    convert_from_object(oname, size, [obj], None)
    return oname


# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
def object_get_unit(obj, name):
    dimless = None
    unitlock = 0

    prop = object_get_property(obj, name, None)

    if prop is None:
        buffer = bytearray(64)
        buffer[:64] = bytes(64)
        raise Exception("property '{}' not found in object '{}'".format(name, object_name(obj, buffer, 63)))

    rlock(unitlock)
    if dimless is None:
        runlock(unitlock)
        wlock(unitlock)
        dimless = unit_find("1")
        wunlock(unitlock)
    else:
        runlock(unitlock)

    if prop.unit is not None:
        return prop.unit.name
    else:
        return dimless.name


# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
import ctypes

def object_create_single(oclass):
    global tp_next
    global tp_count
  
    obj = ctypes.POINTER(ctypes.c_int)()
    sz = ctypes.sizeof(ctypes.c_int)

    if tp_count == 0:
        tp_count = processor_count()

    if oclass is None:
        raise Exception("object_create_single(CLASS *oclass=None): class is None")
        
    if oclass.passconfig & PC_ABSTRACTONLY:
        raise Exception("object_create_single(CLASS *oclass='%s'): abstract class '%s' cannot be instantiated" % (oclass.name, oclass.name))
    
    obj = ctypes.cast(ctypes.c_int(), ctypes.pointer( (ctypes.c_int * sz) ((sz + oclass.size)) ))
    if obj is None:
        raise Exception("object_create_single(CLASS *oclass='%s'): memory allocation failed" % (oclass.name))
    
    ctypes.memset(obj, 0, sz + oclass.size)

    tp_next = tp_next % tp_count

    obj.contents.id = next_object_id
    next_object_id += 1
    obj.contents.oclass = oclass
    obj.contents.next = ctypes.POINTER(ctypes.c_int)()
    obj.contents.name = None
    obj.contents.parent = None
    obj.contents.child_count = 0
    obj.contents.rank = 0
    obj.contents.clock = 0
    obj.contents.latitude = QNAN
    obj.contents.longitude = QNAN
    obj.contents.in_svc = TS_ZERO
    obj.contents.in_svc_micro = 0
    obj.contents.in_svc_double = ctypes.c_double(obj.contents.in_svc)
    obj.contents.out_svc = TS_NEVER
    obj.contents.out_svc_micro = 0
    obj.contents.out_svc_double = ctypes.c_double(obj.contents.out_svc)
    obj.contents.space = object_current_namespace()
    obj.contents.flags = OF_NONE
    obj.contents.rng_state = randwarn(None)
    obj.contents.heartbeat = 0

    prop = oclass.pmap
    while prop is not None:
        property_create(prop, ctypes.cast((ctypes.c_char * (int64)(prop.addr)), ctypes.c_void_p))
        if prop.next is not None:
            prop = prop.next
        elif prop.oclass.parent:
            prop = prop.oclass.parent.pmap
        else:
            prop = None

    if first_object is None:
        first_object = obj
    else:
        last_object.contents.next = obj

    last_object = obj
    oclass.profiler.numobjs += 1

    return obj


# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
def object_create_foreign(obj):
    if obj is None:
        raise Exception("object_create_foreign(obj=None): object is None")
    
    if obj.oclass is None:
        raise Exception("object_create_foreign(obj=<new>): obj.oclass is None")
    
    if obj.oclass.magic != CLASSVALID:
        raise Exception("object_create_foreign(obj=<new>): obj.oclass is not really a class")

    obj.synctime = [0] * sizeof(obj.synctime)
    obj.id = next_object_id
    next_object_id += 1
    obj.next = None
    obj.name = None
    obj.parent = None
    obj.rank = 0
    obj.clock = 0
    obj.latitude = QNAN
    obj.longitude = QNAN
    obj.in_svc = TS_ZERO
    obj.in_svc_micro = 0
    obj.in_svc_double = float(obj.in_svc)
    obj.out_svc = TS_NEVER
    obj.out_svc_micro = 0
    obj.out_svc_double = float(obj.out_svc)
    obj.flags = OF_FOREIGN

    if first_object is None:
        first_object = obj
    else:
        last_object.next = obj

    last_object = obj
    obj.oclass.profiler.numobjs += 1

    return obj


def object_stream_fixup(obj, class_name, obj_name):
    obj.oclass = class_get_class_from_class_name(class_name)
    obj.name = str(obj_name)
    obj.next = None
    if first_object is None:
        first_object = obj
    else:
        last_object.next = obj
    last_object = obj