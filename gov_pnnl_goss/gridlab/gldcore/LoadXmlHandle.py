from xml.sax import SAXParseException

from gridlab.gldcore import Random
from gridlab.gldcore.Class import DynamicClass
from gridlab.gldcore.Globals import global_set_var, STATUS, global_find
from gridlab.gldcore.Load import add_unresolved
from gridlab.gldcore.Module import Module
from gridlab.gldcore.Object import Object
from gridlab.gldcore.PropertyHeader import PropertyType
from gridlab.gldcore.TimeStamp import timestamp_set_tz, TimeStamp, convert_to_timestamp
from gridlab.gldcore.Unit import Unit

UR_RANKS = 0
UR_NONE = 1
class gld_load_hndl:
    def set_document_locator(self, loc):
        self.locator = loc


class gld_load_hndl:
    def write_chars(self, to_write):
        pass
# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106

class GLDSTATE:
    EMPTY = 0
    LOAD = 1            # got load tag & not in a module
    MODULE_STATE = 2    # in a module
    MODULE_PROP = 3     # setting a module property
    OBJECT_STATE = 4    # setting up an object
    OBJECT_PROP = 5     # setting an object property
    GLOBAL_STATE = 6    # setting up for global variables
    GLOBAL_PROP = 7     # setting a global variable
    CLOCK_STATE = 8
    CLOCK_PROP = 9



class GldLoadHndl:
    def write_chars(self, to_write, count, formatter):
        pass
# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106 

class gld_load_hndl:
    def error(self, e):
        print("XML_Load: %ls(%i:char %i)\n Message: %ls", e.getSystemId(), e.getLineNumber(), e.getColumnNumber(), e.getMessage())
        load_state = False


def fatal_error(self, e):
    print("XML_Load: %ls(%i:char %i)\n Message: %ls", e.getSystemId(), e.getLineNumber(), e.getColumnNumber(), e.getMessage())
    load_state = False
# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106 


def warning(self, e):
    print("XML_Load: %ls(%i:char %i)\n Message: %ls", e.getSystemId(), e.getLineNumber(), e.getColumnNumber(), e.getMessage())
# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106 

def notation_decl(self, name, public_id, system_id):
    pass

def parse_property(self, buffer):
    pass


def gld_load_hndl_read_module_prop(self, prop_name, buffer, length):
    if prop_name == "major":
        temp = [8]
        major_in = int(buffer)
        major = 0
        self.module_get_var(self.module, "major", temp, 8)
        major = int(temp)
        if major == 0:
            return None
        if major == major_in:
            return None
        elif major > major_in:
            print("The input file was built using an older major version of the module.")
            return None
        elif major < major_in:
            print("The file was built using a newer major version of the module loading it!")
            return None
    elif prop_name == "minor":
        temp = [8]
        minor_in = int(buffer)
        minor = 0
        major = 0
        self.module_get_var(self.module, "major", temp, 8)
        major = int(temp)
        self.module_get_var(self.module, "minor", temp, 8)
        minor = int(temp)
        if major == 0:
            return None
        if minor == minor_in:
            return None
        elif minor > minor_in:
            print("XML::read_module_prop(): The input file was built using an older minor version of the module.")
        elif minor < minor_in:
            print("XML::read_module_prop(): The file was built using a newer minor version of the module loading it!")
    else:
        global_set_var(prop_name, buffer)
    return None
# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106 


class GldLoadHndl:
    def read_global_prop(self, buffer, len):
        return 0
# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106 


def time_value_datetime(buffer, ts_val):
    pass


def time_value_datetimezone(buffer, ts_val):
    pass



class GldLoadHndl:
    def read_clock_prop(self, prop_name, buffer, len):
        ts_val = 0
        errmsg = ""
        if prop_name == "tick":
            pass
        elif prop_name == "timezone":
            if timestamp_set_tz(buffer) is None:
                errmsg = "timezone %s is not defined" % buffer
                return errmsg
        elif prop_name == "timestamp":
            if time_value_datetime(buffer, ts_val):
                global_clock = ts_val
            elif time_value_datetimezone(buffer, ts_val):
                global_clock = ts_val
            else:
                errmsg = "timestamp \"%s\" could not be resolved" % buffer
                return errmsg
        else:
            errmsg = "Unrecognized keyword in start_element_clock(%s)" % buffer
            return errmsg
        return None
# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106 


def load_latitude(buffer):
    pass


def load_longitude(buffer):
    pass



class GldLoadHandler:
    def read_object_prop(self, buffer, len):
        rand_ptr = None
        rand_mode_ptr = None
        unit_ptr = None
        real_val = 0.0
        unit = None
        e = None
        addr = Object.object_get_addr(self.obj, buffer)
        propname = buffer
        if self.obj is None:
            errmsg = f"Null object pointer in read_object_prop({buffer})"
            return errmsg

        if self.prop is None:
            if buffer == "parent":
                if buffer == "root":
                    self.obj.parent = None
                else:
                    add_unresolved(self.obj, Property.PT_object, self.obj.parent, self.owner_class, buffer, "XML", 42, UR_RANKS)
            elif propname == "rank":
                self.obj.rank = int(buffer)
            elif propname == "clock":
                self.obj.exec_clock = int(buffer)
            elif propname == "latitude":
                self.obj.latitude = load_latitude(buffer)
            elif propname == "longitude":
                self.obj.longitude = load_longitude(buffer)
            elif propname == "in":
                self.obj.in_svc = convert_to_timestamp(buffer)
            elif propname == "out":
                self.obj.out_svc = convert_to_timestamp(buffer)
            else:
                errmsg = f"Null property pointer in read_object_prop({buffer})"
                return errmsg
            return None

        if self.prop.global_property_types == PropertyType.PT_double:
            if buffer.startswith("random."):
                temp = buffer[:256]
                modep = None
                first = 0.0
                second = 0.0
                rt = None
                modep = buffer.find("(")
                if modep is None:
                    load_state = False
                    errmsg = f"Misformed random() value in read_object_prop({buffer})"
                    return errmsg
                rt = Random.random_type(modep)
                if rt == 0:
                    load_state = False
                    errmsg = f"Invalid random distribution in read_object_prop({buffer})"
                    return errmsg
                else:
                    first = float(modep.split(",")[0])
                    second = float(modep.split(")")[0])
                    real_val = Random.random_value(rt, first, second)
                if len(buffer.split(")")) > 0:
                    unit = Unit.unit_find(buffer.split(")")[1])
                    if unit is not None and self.prop.unit is not None and Unit.unit_convert_ex(unit, self.prop.unit, real_val) == 0:
                        errmsg = f"Cannot convert units from {unit.name} to {self.prop.unit.name} in read_object_prop({buffer})"
                        load_state = False
                        return errmsg
            else:
                unit_ptr = None
                real_val = float(buffer, unit_ptr)
                if unit_ptr is not None:
                    while unit_ptr[0] == ' ':
                        unit_ptr += 1
                    unit = Unit.unit_find(unit_ptr)
                    if len(unit_ptr) > 0:
                        if unit is not None and self.prop.unit is not None and self.unit_convert_ex(unit, self.prop.unit, real_val) == 0:
                            errmsg = f"Cannot convert units from {unit.name} to {self.prop.unit.name} in read_object_prop({buffer})"
                            load_state = False
                            return errmsg
            
            if Object.object_set_double_by_name(self.obj, propname, real_val) == 0:
                errmsg = f"Could not set {propname} to {real_val} in read_object_prop({buffer})"
                load_state = False
                return errmsg
            else:
                return None
        elif self.prop.global_property_types == PropertyType.PT_object:
            if add_unresolved(self.obj, PropertyType.PT_object, addr, self.owner_class, buffer, "XML", 42, UR_NONE) == None:
                errmsg = f"Failure with add_unresolved() in read_object_prop({buffer})"
                return errmsg
        else:
            if self.prop.global_property_types < PropertyType.pt_last():
                if Object.object_set_value_by_name(self.obj, propname, buffer) == 0:
                    errmsg = f"Property {propname} of {self.obj.owner_class.name}:{self.obj.id} could not be set to {buffer} in read_object_prop()"
                    load_state = False
                    return errmsg
            else:
                errmsg = f"Invalid property id = {self.prop.global_property_types} in read_object_prop({buffer})"
                return errmsg
        return 0
# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106 


def wcstombs(buffer, chars, param):
    pass


def characters(self, chars, length):
    buffer = bytearray(1024)
    tbuff = bytearray(1024)
    wbuff = bytearray(1024)
    e = None
    unit_ptr = None
    i = 0
    len = 0
    retval = None
    stack_state = self.stack_state

    if stack_state in (GLDSTATE.MODULE_PROP, GLDSTATE.GLOBAL_PROP, GLDSTATE.OBJECT_PROP, GLDSTATE.CLOCK_PROP):
        len = len(chars)
        if len < 1:
            tbuff = b"Unable to get length of characters in characters()"
            wbuff = tbuff.decode('utf-8').encode('utf-16-le')
            e = SAXParseException(wbuff, self.locator)
            self.error(e)
            del e
            return
        if len != wcstombs(buffer, chars, 1024):
            tbuff = b"Unable to convert wcs to char in characters()"
            wbuff = tbuff.decode('utf-8').encode('utf-16-le')
            e = SAXParseException(wbuff, self.locator)
            self.error(e)
            del e
            return
    else:
        return

    if len > 0:
        j = 0
        i = 0
        for i in range(len):
            if buffer[i] == "":
                j += 1
        if i == j:
            print("XML_Load: ignored: %i spaces.", length)
            retval = 0
            return
    else:
        print("XML_Load: ignored empty characters() call")
        retval = 0
        return

    if buffer[0] == b'"' and buffer[1] == b'"':
        print("XML_Load: ignored empty doublequote characters() call")
        retval = 0
        return

    retval = None
    if stack_state == GLDSTATE.MODULE_PROP:
        retval = self.read_module_prop(buffer, len)
    elif stack_state == GLDSTATE.GLOBAL_PROP:
        retval = self.read_global_prop(buffer, len)
    elif stack_state == GLDSTATE.OBJECT_PROP:
        retval = self.read_object_prop(buffer, len)
    elif stack_state == GLDSTATE.CLOCK_PROP:
        retval = self.read_clock_prop(buffer, len)

    if retval is not None:
        stack_state = GLDSTATE.EMPTY
        print("Error reading the XML file")
        wbuff = ""
        e = SAXParseException(wbuff, self.locator)
        self.error(e)
        del e
        load_state = 0
# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106 


def end_document(self):
    temp_obj = Object.object_get_first()

    if self.load_resolve_all() == STATUS.FAILED:
        print("XML_Load: unable to resolve object linkings!")
        load_state = False

    for obj in temp_obj:
        Object.object_set_parent(obj, obj.parent)
    print("XML_Load: %d object%s loaded.", Object.object_get_count(), "s" if Object.object_get_count() > 0 else "")
    if Object.object_count > 0:
        if Object.object_get_count() != self.object_count:
            print("XML_Load: we expected %i objects instead!" % self.object_count)
    print("XML_Load: %d class%s loaded.", DynamicClass.class_get_count(), "es" if DynamicClass.class_get_count() > 0 else "")
    if DynamicClass.class_count > 0:
        if DynamicClass.class_get_count() != self.class_count:
            print("XML_Load: we expected %i classes instead!" % self.class_count)
# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106 


class GldLoadHndl:
    def end_element_empty(self, buffer, length):
        return None
# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106 


class gld_load_hndl:
    def end_element_load(self, buffer, length):
        if buffer == "load":
            self.stack_state = "empty"
        return None
# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106 


def gld_load_hndl_end_element_module(self, buffer, len):
    if buffer == "module":
        self.stack_state = "LOAD"
    return None
# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106 


def end_element_module_prop(self, buffer, len):
    if buffer == "properties":
        self.propname = [0] * len
        self.stack_state = GLDSTATE.MODULE_STATE
    return None
# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106 


def gld_load_hndl_end_element_object(self, buffer, len):
    if buffer == "object":
        self.stack_state = GLDSTATE.MODULE_STATE
    return None
# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106 


def end_element_object_prop(self, buffer, len):
    if self.propname == buffer:
        propname = 0
        stack_state = GLDSTATE.OBJECT_STATE
    return None
# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106 


def gld_load_hndl_end_element_global(self, buffer, len):
    if buffer == "global":
        self.stack_state = "LOAD"
    return None
# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106 


def end_element_global_prop(self, buffer, len):
    if self.prop_name == buffer.decode('utf-8'):
        self.prop_name = b'\x00' * len
        stack_state = GLDSTATE.GLOBAL_STATE
    return None
# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106 


def gld_load_hndl_end_element_clock_prop(self, buffer, len):
    if self.propname == buffer:
        self.propname = 0
        len(self.propname)
        stack_state = GLDSTATE.CLOCK_STATE
    return None
# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106 


def end_element_clock(self, buffer, len):
    if buffer == "clock":
        self.stack_state = "LOAD"
    return None
# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106 


def end_element(self, uri: str, local_name: str, q_name: str) -> None:
    buffer = [0]*128
    i = 0
    len_ = 0
    temp_stack = None
    retval = None

    self.depth -= 1

    len_ = len(q_name)
    buffer = q_name.encode("utf-8")

    switcher = {
        GLDSTATE.EMPTY: self.end_element_empty,

        GLDSTATE.LOAD: self.end_element_load,
        GLDSTATE.MODULE_STATE: self.end_element_module,
        GLDSTATE.MODULE_PROP: self.end_element_module_prop,
        GLDSTATE.OBJECT_STATE: self.end_element_object,
        GLDSTATE.OBJECT_PROP: self.end_element_object_prop,
        GLDSTATE.GLOBAL_STATE: self.end_element_global,
        GLDSTATE.GLOBAL_PROP: self.end_element_global_prop,
        GLDSTATE.CLOCK_STATE: self.end_element_clock,
        GLDSTATE.CLOCK_PROP: self.end_element_clock_prop
    }
    retval = switcher.get(self.stack_state)(buffer, len)
# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106 


def ignorable_whitespace(self, chars, length):
    print("XML_Load: ignored: %i spaces." % length)
# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106 


class gld_load_hndl:
    def processing_instruction(self, target, data):
        return
# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106 

class gld_load_hndl:
    def start_document(self):
        self.depth = 0
        self.module_name[0] = 0
        self.load_state = True


def start_element_empty(self, buffer, len, attributes):
    if buffer == "load":
        self.stack_state = "LOAD"
    return None
# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106 


def start_element_load(self, buffer, len, attributes):
    wcs_type = {"global_property_types": 5}
    wcs_major = {"major": 6}
    wcs_minor = {"minor": 6}
    
    major = 0
    minor = 0
    
    if buffer == "global":
        self.stack_state = GLDSTATE.GLOBAL_STATE
    elif buffer == "module":
        module_name = ""
        wcs_type_str =wcs_type.keys()
        wcs_major_str = wcs_major.keys()
        wcs_minor_str = wcs_minor.keys()
        
        wcstombs(module_name, attributes.getValue(wcs_type_str), 1024)
        _major = attributes.getValue(wcs_major_str)
        _minor = attributes.getValue(wcs_minor_str)
        
        if _major:
            major.value = float(_major)
        if _minor:
            minor.value = float(_minor)
            
        if Module.module_load(module_name, 0, None) is None:
            errmsg = f"Unable to load module {module_name} in start_element_load()"
            return errmsg
        else:
            self.module_name = buffer
            self.stack_state = GLDSTATE.MODULE_STATE
            if major.value != 0:
                temp = ""
                Module.module_getvar(self.module, b"major", temp, 8)
                major_in = int(temp.value)
                Module.module_getvar(self.module, b"minor", temp, 8)
                minor_in = int(temp.value)
                if major.value < major_in:
                    print("XML::read_module_prop(): The input file was built using an older major version of the module.")
                    return None 
                if minor.value == minor_in:
                    return None
                elif minor.value > minor_in:
                    print("XML::read_module_prop(): The input file was built using an older minor version of the module.")
                else:
                    print("XML::read_module_prop(): The file was built using a newer minor version of the module loading it!")
    elif buffer == "clock":
        self.stack_state = GLDSTATE.CLOCK_STATE
    else:
        errmsg = f"Unrecognized keyword in start_element_load({buffer})"
        return errmsg
    return None
# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106 


def gld_load_hndl_start_element_module_build_object(self, attributes):
    str_id = ['id']
    str_name = ['name']
    str_type = ['global_property_types']
    
    str_id_len = len(str_id[0])
    str_name_len = len(str_name[0])
    str_type_len = len(str_type[0])
    
    object_type = [64]
    object_id = [64]
    object_name = [64]
    temp = None
    retval = None
    first = -1
    last = -1
    
    if attributes.get_index(str_type[0]) < 0:
        errmsg = "object tag without a global_property_types in start_element_module_build_object()"
        return errmsg
    else:
        object_type[0] = attributes.get_value(str_type[0])[:64]
        owner_class = DynamicClass.class_get_class_from_classname_in_module(object_type, self.module)
        
        if owner_class is None:
            errmsg = "DynamicClass \"%s\" for module \"%s\" is not recognized in start_element_module_build_object()" % (object_type, self.module_name)
            return errmsg
        
    if attributes.get_index(str_id[0]) < 0:
        last = first = -1
    else:
        object_id[0] = attributes.get_value(str_id[0])[:64]
        temp = object_id[0].find('.')
        
        if temp == -1:
            first = int(object_id[0])
            if first < 0:
                errmsg = "Invalid object id of %i in start_element_module_build_object()" % first
                return errmsg
            else:
                last = first
        else:
            temp = object_id[0].split('.')
            if temp[0] == temp[1]:
                if temp == object_id[0]:
                    last = int(object_id[0][2:])
                    if last < 1:
                        errmsg = "Invalid object id of %i in start_element_module_build_object()" % last
                        return errmsg
                    else:
                        first = -1
                else:
                    first = int(temp[0])
                    last = int(temp[1])
                    if first < 0:
                        print("XML_Load: first ID < 0 !")
                        errmsg = "Invalid object id of %i in start_element_module_build_object()" % first
                        return errmsg
                    
                    if last < 1:
                        print("XML_Load: last ID < 1 !")
                        errmsg = "Invalid object id of %i in start_element_module_build_object()" % first
                        return errmsg
                    
                    if first >= last:
                        print("XML_Load: first id >= last id!")
                        errmsg = "Invalid object id of %i in start_element_module_build_object()" % first
                        return errmsg
            else:
                errmsg = "Invalid ID format in start_element_module_build_object()"
                return errmsg
    
    if (retval := Object.object_build_object_vect(self, first, last)) != 0:
        errmsg = "Unable to create objects in start_element_module_build_object()"
        return errmsg
    
    if attributes.get_index(str_name[0]) < 0:
        object_name[0] = "(none)"
    else:
        object_name[0] = attributes.get_value(str_name[0])[:64]
        Object.object_set_name(self.obj, object_name)
    
    stack_state = GLDSTATE.OBJECT_STATE
    return None
# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106 


def start_element_module(self, buffer, len, attributes):
    if buffer == "object":
        self.propname = "object"
        return self.start_element_module_build_object(attributes)
    elif buffer == "properties":
        self.propname = buffer
        self.stack_state = GLDSTATE.MODULE_PROP
    else:
        self.errmsg = f"Unrecognized keyword in start_element_module({buffer})"
        return self.errmsg
    return None
# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106 


def start_element_module_prop(self, buffer, len, attributes):
    pname = "{}::{}".format(self.module.name, buffer)
    if global_find(pname):
        self.propname = pname
    else:
        print("XML: start_element_module_prop: property \"\" not found, initializing")
        self.propname = pname
    return None


def start_element_object(self, buffer, len, attributes):
    if buffer == "parent":
        self.propname = "parent"
        stack_state = GLDSTATE.OBJECT_PROP
    elif buffer == "root":
        self.propname = "root"
        stack_state = GLDSTATE.OBJECT_PROP
    elif buffer == "rank":
        self.propname = "rank"
        stack_state = GLDSTATE.OBJECT_PROP
    elif buffer == "clock":
        self.propname = "clock"
        stack_state = GLDSTATE.OBJECT_PROP
    elif buffer == "latitude":
        propname = "latitude"
        stack_state = GLDSTATE.OBJECT_PROP
    elif buffer == "longitude":
        propname = "longitude"
        stack_state = GLDSTATE.OBJECT_PROP
    elif buffer == "in":
        propname = "in"
        stack_state = GLDSTATE.OBJECT_PROP
    elif buffer == "out":
        propname = "out"
        stack_state = GLDSTATE.OBJECT_PROP
    elif buffer == "library":
        propname = "library"
        stack_state = GLDSTATE.OBJECT_PROP
    elif (prop := DynamicClass.class_find_property(self.owner_class, buffer)) != None:
        propname = buffer
        stack_state = GLDSTATE.OBJECT_PROP
    else:
        print(f"Unrecognized property in start_element_object({buffer})")
    prop = DynamicClass.class_find_property(self.owner_class, buffer)
    return None
# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106 


class gld_load_hndl:
    def start_element_object_prop(self, buffer, len, attributes):
        return None
# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106 


def start_element_global(self, buffer, len, attributes):
    
	if buffer == "version_major":
		self.propname = "version_major"
		self.stack_state = GLDSTATE.GLOBAL_PROP
	elif buffer == "version_minor":
		self.propname = "version_minor"
		self.stack_state = GLDSTATE.GLOBAL_PROP
	elif buffer == "savefilename":
		self.propname = "savefilename"
		self.stack_state = GLDSTATE.GLOBAL_PROP
	elif buffer == "class_count":
		self.propname = "class_count"
		self.stack_state = GLDSTATE.GLOBAL_PROP
	elif buffer == "object_count":
		self.propname = "object_count"
		self.stack_state = GLDSTATE.GLOBAL_PROP
	elif buffer == "property":
		self.propname = "property"
		self.stack_state = GLDSTATE.GLOBAL_PROP

	return None
# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106 


class gld_load_hndl:
    def start_element_global_prop(self, buffer, len, attributes):
        return None
# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106 


def start_element_clock(self, buffer, len, attributes):
        if buffer == "tick":
            self.stack_state = GLDSTATE.CLOCK_PROP
            self.propname = "tick"
        elif buffer == "timezone":
            self.stack_state = GLDSTATE.CLOCK_PROP
            self.propname = "timezone"
        elif buffer == "timestamp":
            self.stack_state = GLDSTATE.CLOCK_PROP
            self.propname = "timestamp"
        elif buffer == "starttime":
            self.stack_state = GLDSTATE.CLOCK_PROP
            self.propname = "timestamp"
        elif buffer == "stoptime":
            self.stack_state = GLDSTATE.CLOCK_PROP
            self.propname = "stoptime"
        else:	
            self.errmsg = f"Unrecognized keyword in start_element_clock({buffer})"
            return self.errmsg
        return None
# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106 


class gld_load_hndl:
    def start_element_clock_prop(self, buffer, len, attributes):
        return None
# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106 


def start_element(self, uri, local_name, qname, attributes):
    buffer = ""
    temp = None
    i = 0
    len = 0
    retval = 0
    curr_stack = None
    str_id = 'id'
    str_name = 'name'
    str_type = 'global_property_types'

    if len(qname) < 1:
        self.print("startElement: Unable to parse element tag length!")
        self.load_state = 0
        return

    if wcstombs(buffer, qname, 128) < 1:
        self.print("startElement: Unable to convert element tag name from wchar to char!")
        self.load_state = 0
        return
    
    switcher = {
        GLDSTATE.EMPTY: self.start_element_empty(buffer, len, attributes),
        GLDSTATE.LOAD: self.start_element_load(buffer, len, attributes),
        GLDSTATE.MODULE_STATE: self.start_element_module(buffer, len, attributes),
        GLDSTATE.MODULE_PROP: self.start_element_module_prop(buffer, len, attributes),
        GLDSTATE.OBJECT_STATE: self.start_element_object(buffer, len, attributes),
        GLDSTATE.OBJECT_PROP: self.start_element_object_prop(buffer, len, attributes),
        GLDSTATE.GLOBAL_STATE: self.start_element_global(buffer, len, attributes),
        GLDSTATE.GLOBAL_PROP: self.start_element_global_prop(buffer, len, attributes),
        GLDSTATE.CLOCK_STATE: self.start_element_clock(buffer, len, attributes),
        GLDSTATE.CLOCK_PROP: self.start_element_clock_prop(buffer, len, attributes)
    }

    retval = switcher.get(self.stack_state, None)

    if retval is not None:
        tbuff = "Error in start_element with tag \"%s\": %s" % (buffer.value, retval)
        wbuff = tbuff.encode('utf-8')
        e = SAXParseException(wbuff, self.locator.contents)
        self.error(e)
# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106 


class GldLoadHndl:
    def build_object_vect(self, start, end):
        count = 0
        i = 0
        self.obj_vect.clear()
        if start == end:
            if self.owner_class.create(self.obj, None) == 0:
                errmsg = "Unable to create a lone object with ID = {} in build_object_vect({}, {})".format(start, start, end)
                self.load_state = False
                return errmsg
            if start != -1:
                if self.load_set_index(self.obj, int(end)) == 0:
                    errmsg = "Unable to index an item in build_object_vect({}, {})".format(start, end)
                    self.load_state = False
                    return errmsg
                else:
                    pass
            return None
        if start == -1:
            count = end
        else:
            if end > start:
                count = end - start + 1
            else:
                errmsg = "last < first, aborting build_object_vect({}, {})".format(start, end)
                self.load_state = False
                return errmsg
        self.obj_vect.reserve(count)
        for i in range(0 if start == -1 else start, end + 1):
            if self.oclass.create(self.obj_vect[i], None) != 0:
                if start != -1:
                    if self.load_set_index(self.obj_vect[i], int(i)) == 0:
                        errmsg = "Unable to index a batch item in build_object_vect({}, {})".format(start, end)
                        self.load_state = False
                        return errmsg
            else:
                errmsg = "Unable to create an object in build_object_vect({}, {})".format(start, end)
                self.load_state = False
                return errmsg
        return None
# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106 