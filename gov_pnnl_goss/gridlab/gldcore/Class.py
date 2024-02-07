# Pass configuration
from base64 import encode
from errno import ENOENT, E2BIG, EINVAL, ENOMEM
from enum import Enum
from typing import Union, List, Any

from gov_pnnl_goss.gridlab.gldcore.Convert import unit_find
#  PROPERTYACCESS.PA_PUBLIC, PROPERTYACCESS.PA_PROTECTED, PROPERTYACCESS.PA_PRIVATE, PROPERTYACCESS.PA_REFERENCE, PROPERTYACCESS.PA_HIDDEN,
from gov_pnnl_goss.gridlab.gldcore.Globals import \
    global_suppress_deprecated_messages, global_suppress_repeat_messages, PROPERTYACCESS
from gov_pnnl_goss.gridlab.gldcore.GridLabD import gl_error, gl_warning
# PROPERTYFLAGS.PF_CHARSET, PROPERTYFLAGS.PF_DEPRECATED, PROPERTYFLAGS.PF_EXTENDED, PROPERTYFLAGS.PF_DEPRECATED_NONOTICE,
from gov_pnnl_goss.gridlab.gldcore.Property import \
    FUNCTIONADDR, PROPERTY, PROPERTYTYPE, PROPERTYFLAGS, DELEGATEDTYPE
from gridlab.gldcore.Module import Module

global_ms_per_second = 1000  # Assuming this value


class PASSCONFIG(Enum):
    PC_NOSYNC = 0x00               # < used when the class requires no synchronization */
    PC_PRETOPDOWN = 0x01           # < used when the class requires synchronization on the first top-down pass */
    PC_BOTTOMUP = 0x02             # < used when the class requires synchronization on the bottom-up pass */
    PC_POSTTOPDOWN = 0x04          # < used when the class requires synchronization on the second top-down pass */
    PC_FORCE_NAME = 0x20           # < used to indicate the class must define names for all its objects */
    PC_PARENT_OVERRIDE_OMIT = 0x40 # < used to ignore parent's use of PC_UNSAFE_OVERRIDE_OMIT */
    PC_UNSAFE_OVERRIDE_OMIT = 0x80 # < used to flag that omitting overrides is unsafe */
    PC_ABSTRACTONLY = 0x100        # < used to flag that the class should never be instantiated itself, only inherited classes should */
    PC_AUTOLOCK = 0x200            # < used to flag that sync operations should not be automatically write locked */
    PC_OBSERVER = 0x400            # < used to flag whether commit process needs to be delayed with respect to ordinary "in-the-loop" objects */


# Notification message types
class NOTIFYMODULE(Enum):
    NM_PREUPDATE = 0
    NM_POSTUPDATE = 1
    NM_RESET = 2


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


class PROPERTYNAME:
    pass


class FUNCTION:
    def __init__(self):
        self.oclass = None
        self.name = None
        self.addr = None
        self.next = None

# class FUNCTION:
#     def __init__(self) -> None:
#         self.oclass: Class
#         self.name: FUNCTIONNAME
#         self.addr: FUNCTIONADDR
#         self.next: FUNCTION


class LOADDATA:
    def __init__(self):
        self.name = None
        self.call = None
        self.next = None


class KEYWORD:
    def __init__(self):
        self.name = None
        self.value = None
        self.next = None

class LOADMETHOD:
    def __init__(self) -> None:
        self.name: str = ""
        self.call: Any = None
        self.next: LOADMETHOD


# Set operations
SET_MASK = 0xffff


def SET_ADD(set_value, value):
    return set_value | value

def SET_DEL(set_value, value):
    return (value ^ SET_MASK) & set_value

def SET_CLEAR(set_value):
    return 0

def SET_HAS(set_value, value):
    return set_value & value


class CLASSMAGIC(Enum):
    CLASSVALID = 0xc44d822e


class Class:
    def __init__(self, module, name, size, passconfig):
        self.commit: FUNCTIONADDR = None
        self.create: FUNCTIONADDR = None
        self.finalize: FUNCTIONADDR = None
        self.first_class = []
        self.fmap: List[FUNCTION] = None
        self.has_runtime: bool = None
        self.heartbeat: FUNCTIONADDR = None
        self.id: int = None
        self.init: FUNCTIONADDR = None
        self.isa: FUNCTIONADDR = None
        self.loadmethods: List[LOADMETHOD] = None
        self.magic: CLASSMAGIC = CLASSMAGIC.CLASSVALID
        self.module: Module = module
        self.name: str = name
        self.next: Class = None
        self.notify: FUNCTIONADDR = None
        self.parent: Class = None
        self.passconfig: PASSCONFIG = passconfig
        self.plc: FUNCTIONADDR = None
        self.pmap: List[PROPERTY] = None
        self.precommit: FUNCTIONADDR = None
        self.profiler: dict[str, Union[int, bool]] = {
            'numobjs': 0,
            'count': 0,
            'clocks': 0
        }
        self.recalc: FUNCTIONADDR = None
        self.runtime: str = None
        self.size: int = size
        self.sync: FUNCTIONADDR = None
        self.threadsafe: bool = None
        self.trl: TECHNOLOGYREADINESSLEVEL = None
        self.update: FUNCTIONADDR = None
        self.property_type = []
        self.last_class = None
        self.count = 0
        self.next_class = None
        self.check = None

    def unit_find(self):
        pass

    def buffer_write(self, buffer, len, format, *args):
        count = 0
        if buffer is None:
            return 0
        if len < 1:
            return 0
        if self.check == 0:
            return 0
        temp = ""
        for a in args:
            temp = str(a).encode(format)
        count = len(args)
        if count < len:
            buffer = temp
            return count, buffer
        else:
            check = 0
            return 0, None


    def get_first_property(self, oclass):
        if oclass is None:
            raise Exception("get_first_property(Class *oclass=None): oclass is None")
        return oclass.pmap

    def get_next_property(self, prop):
        if prop.next and prop.oclass == prop.next.oclass:
            return prop.next
        else:
            return None

    def prop_in_class(self, oclass, prop):
        if oclass == prop.oclass:
            return prop
        elif oclass.parent is not None:
            return self.prop_in_class(self, oclass.parent, prop)
        else:
            return None

    def find_property_rec(self, oclass, name, pclass):
        prop = oclass.pmap
        while prop and prop.oclass == oclass:
            if prop.name == name.encode('utf-8'):
                return prop
            prop = prop.next

        if oclass.parent == pclass:
            gl_error(
                f"find_property_rec(Class *oclass='{oclass.name}', "
                f"PROPERTYNAME name='{name}', Class *pclass='{pclass.name}') causes an infinite class inheritance loop"
            )
            """
            TROUBLESHOOT
            A class has somehow specified itself as a parent class, either directly or indirectly.
            This means there is a problem with the module that publishes the class.
            """
            return None
        elif oclass.parent:
            return self.find_property_rec(oclass.parent, name, pclass)
        else:
            return None

    def find_property(self, oclass, name):
        if not oclass:
            return None

        prop = oclass.get(name, None)

        if prop:
            return prop

        for prop in oclass.pmap:
            if prop.oclass == oclass:
                if prop.name == name.encode('utf-8'):
                    if prop.flags & PROPERTYFLAGS.PF_DEPRECATED and not (
                            prop.flags & PROPERTYFLAGS.PF_DEPRECATED_NONOTICE) and not global_suppress_deprecated_messages:
                        gl_warning(
                            f"find_property(Class *oclass='{oclass.name}', PROPERTYNAME name='{name}': property is deprecated")
                        """
                        TROUBLESHOOT
                        You have done a search on a property that has been flagged as deprecated and will most likely not be supported soon.
                        Correct the usage of this property to get rid of this message.
                        """
                        if global_suppress_repeat_messages:
                            prop.flags |= ~PROPERTYFLAGS.PF_DEPRECATED_NONOTICE
                    return prop

        if oclass.parent == oclass:
            gl_error(
                f"find_property(oclass='{oclass.name}', name='{name}') causes an infinite class inheritance loop")
            """
            TROUBLESHOOT
            A class has somehow specified itself as a parent class, either directly or indirectly.
            This means there is a problem with the module that publishes the class.
            """
            return None
        elif oclass.parent:
            return self.find_property_rec(oclass.parent, name, oclass)
        else:
            return None

    def add_property(self, oclass, prop):
        last = oclass.pmap
        while last is not None and last.next is not None:
            last = last.next
        if last is None:
            oclass.pmap = prop
        else:
            last.next = prop

    def add_extended_property(self, oclass, name, ptype, unit):
        prop = PROPERTY()
        pUnit = None

        try:
            if unit:
                pUnit = self.unit_find(unit)
        except Exception as msg:
            # will get picked up later
            pass

        if prop is None:
            raise Exception(
                f"add_extended_property(oclass='{oclass.name}', name='{name}', ...): memory allocation failed")
            # TROUBLESHOOT: The system has run out of memory. Try making the model smaller and trying again.

        if ptype <= PROPERTYTYPE.PT_FIRST or ptype >= PROPERTYTYPE.PT_LAST:
            raise Exception(
                f"add_extended_property(oclass='{oclass.name}', name='{name}', ...): property type is invalid")
            # TROUBLESHOOT: The function was called with a property type that is not recognized. This is a bug that should be reported.

        if unit is not None and pUnit is None:
            raise Exception(
                f"add_extended_property(oclass='{oclass.name}', name='{name}', ...): unit '{unit}' is not found")
            # TROUBLESHOOT: The function was called with a unit that is not defined in the units file. Try using a defined unit or adding the desired unit to the units file and try again.

        prop.access = PROPERTYACCESS.PA_PUBLIC
        prop.addr = int(oclass.size)
        prop.size = 0
        prop.delegation = None
        prop.flags = PROPERTYFLAGS.PF_EXTENDED
        prop.keywords = None
        prop.description = None
        prop.unit = pUnit
        prop.name = name
        prop.next = None
        prop.oclass = oclass
        prop.ptype = ptype
        prop.width = self.property_type[ptype].size

        oclass.size += self.property_type[ptype].size

        self.add_property(oclass, prop)
        return prop

    def get_last_class(self,):
        return self.last_class

    def get_count(self,):
        return self.count


    def get_property_typename(self, type):
        if type <= PROPERTYTYPE.PT_FIRST or type >= PROPERTYTYPE.PT_LAST:
            return "//UNDEF//"
        else:
            return self.property_type[type].name

    def get_property_typexsdname(self, type):
        if type <= PROPERTYTYPE.PT_FIRST or type >= PROPERTYTYPE.PT_LAST:
            return "//UNDEF//"
        else:
            return self.property_type[type].xsdname

    def get_propertytype_from_typename(self, name):
        for i, prop_type in enumerate(self.property_type):
            if prop_type.name == name:
                return PROPERTYTYPE(i)
        return PROPERTYTYPE.PT_void

    def string_to_propertytype(self, type, addr, value):
        if type > PROPERTYTYPE.PT_void and type < PROPERTYTYPE.PT_last:
            return self.property_type[type.value].string_to_data(value, addr, None)
        else:
            return 0

    def string_to_property(self, prop, addr, value):
        if prop.ptype > PROPERTYTYPE.PT_void and prop.ptype < PROPERTYTYPE.PT_last:
            return self.property_type[prop.ptype.value].string_to_data(value, addr, prop)
        else:
            return 0

    def property_to_string(self, prop, addr, value, size):
        if prop.ptype == PROPERTYTYPE.PT_delegated:
            print("unable to convert from delegated property value")
            # TROUBLESHOOT: Property delegation is not yet fully implemented, so you should never get this error.
            return 0
        elif prop.ptype > PROPERTYTYPE.PT_void and prop.ptype < PROPERTYTYPE.PT_last:
            rv = self.property_type[prop.ptype.value].data_to_string(value, size, addr, prop)
            if rv > 0 and prop.unit != 0:
                value += f" {prop.unit.name}"
                rv += len(prop.unit.name) + 1
            return rv
        else:
            return 0

    def register(self, module, name, size, passconfig):
        oclass = self.get_from_classname(name)

        if oclass is not None:
            if oclass.module.name == module.name:
                print(
                    f"module {module.name} cannot register class {name}, it is already registered by module {oclass.module.name}")
                # TROUBLESHOOT: This error is caused by an attempt to define a new class which is already defined in the module or namespace given. This is generally caused by a bug in a module or an incorrectly defined class.
                return None
            else:
                print(
                    f"module {module.name} is registering a 2nd class {name}, previous one in module {oclass.module.name}")

        oclass = Class(module, name, size, passconfig)
        if oclass is None:
            errno = ENOMEM
            return 0

        oclass.magic = CLASSMAGIC.CLASSVALID
        oclass.id = self.count
        oclass.module = module
        oclass.name = name
        oclass.size = size
        oclass.passconfig = passconfig
        oclass.profiler = {
            'numobjs': 0,
            'count': 0,
            'clocks': 0
        }

        if self.first_class is None:
            first_class = oclass
        else:
            self.last_class.next = oclass

        last_class = oclass
        print(f"class {name} registered ok")
        return oclass

    def get_first_class(self,):
        return self.first_class

    def get_next_classes(self,):
        return self.next_class

    def get_from_classname_in_module(self, name, mod):
        if name is None or mod is None:
            return None

        for oclass in self.first_class:
            if oclass.module == mod and oclass.name == name:
                return oclass

        return None

    def get_runtimecount(self,):
        count = 0
        for oclass in self.first_class:
            if oclass.has_runtime:
                count += 1
        return count

    def get_first_runtime(self,):
        for oclass in self.first_class:
            if oclass.has_runtime:
                return oclass
        return None

    def get_next_runtime(self, oclass):
        oclass = oclass.next
        while oclass is not None:
            if oclass.has_runtime:
                return oclass
            oclass = oclass.next
        return None

    def get_extended_count(self, oclass):
        count = 0
        prop = oclass.pmap
        while prop is not None:
            if prop.flags & PROPERTYFLAGS.PF_EXTENDED:
                count += 1
            prop = prop.next
        return count

    def get_from_classname(self, name):
        oclass = None
        mod = None
        temp = name
        ptr = temp.find('.')
        if ptr != -1:
            temp, ptr = temp.split('.', 1)
            mod = self.module_find(temp)
            if mod is None:
                print(f"could not search for '{name}', module not loaded")
                return None
            for oclass in self.first_class:
                if oclass.module == mod and oclass.name == ptr:
                    return oclass
            return None
        for oclass in self.first_class:
            if oclass.name == name:
                return oclass
        return None

    def define_map(self, oclass, *args):
        va_list = list(args)
        count = 0
        prop = None
        va_start = 0
        errno = 0

        while va_start < len(va_list):
            prop_buffer = va_list[va_start]
            va_start += 1
            proptype = PROPERTYTYPE(prop_buffer)

            if proptype > PROPERTYTYPE.PT_last:
                if proptype == PROPERTYTYPE.PT_INHERIT:
                    if oclass.parent is not None:
                        errno = EINVAL
                        gl_error(
                            f"define_map(oclass='{oclass.name}',...): PT_INHERIT unexpected; class already inherits properties from class {oclass.parent.name}")

                    else:
                        classname = va_list[va_start]
                        va_start += 1
                        no_override = ~(~oclass.parent.passconfig | oclass.passconfig)
                        if (
                                oclass.parent.passconfig & PASSCONFIG.PC_UNSAFE_OVERRIDE_OMIT
                                and not (oclass.passconfig & PASSCONFIG.PC_PARENT_OVERRIDE_OMIT)
                                and no_override & PASSCONFIG.PC_PRETOPDOWN
                        ):
                            gl_warning(
                                f"define_map(oclass='{oclass.name}',...): class '{oclass.name}' suppresses parent class '{oclass.parent.name}' PRETOPDOWN sync behavior by omitting override"
                            )
                        if (
                                oclass.parent.passconfig & PASSCONFIG.PC_UNSAFE_OVERRIDE_OMIT
                                and not (oclass.passconfig & PASSCONFIG.PC_PARENT_OVERRIDE_OMIT)
                                and no_override & PASSCONFIG.PC_BOTTOMUP
                        ):
                            gl_warning(
                                f"define_map(oclass='{oclass.name}',...): class '{oclass.name}' suppresses parent class '{oclass.parent.name}' BOTTOMUP sync behavior by omitting override"
                            )
                        if (
                                oclass.parent.passconfig & PASSCONFIG.PC_UNSAFE_OVERRIDE_OMIT
                                and not (oclass.passconfig & PASSCONFIG.PC_PARENT_OVERRIDE_OMIT)
                                and no_override & PASSCONFIG.PC_POSTTOPDOWN
                        ):
                            gl_warning(
                                f"define_map(oclass='{oclass.name}',...): class '{oclass.name}' suppresses parent class '{oclass.parent.name}' POSTTOPDOWN sync behavior by omitting override"
                            )
                        if (
                                oclass.parent.passconfig & PASSCONFIG.PC_UNSAFE_OVERRIDE_OMIT
                                and not (oclass.passconfig & PASSCONFIG.PC_PARENT_OVERRIDE_OMIT)
                                and no_override & PASSCONFIG.PC_UNSAFE_OVERRIDE_OMIT
                        ):
                            gl_warning(
                                f"define_map(oclass='{oclass.name}',...): class '{oclass.name}' does not assert UNSAFE_OVERRIDE_OMIT when parent class '{oclass.parent.name}' does"
                            )
                        count += 1
                elif proptype == PROPERTYTYPE.PT_KEYWORD and prop.ptype == PROPERTYTYPE.PT_enumeration:
                    keyword = va_list[va_start]
                    va_start += 1
                    keyvalue = va_list[va_start]
                    va_start += 1
                    if not self.define_enumeration_member(oclass, prop.name, keyword, keyvalue):
                        errno = EINVAL
                        gl_error(
                            f"define_map(oclass='{oclass.name}',...): property keyword '{keyword}' could not be defined as value {keyvalue}"
                        )

                elif proptype == PROPERTYTYPE.PT_KEYWORD and prop.ptype == PROPERTYTYPE.PT_set:
                    keyword = va_list[va_start]
                    va_start += 1
                    keyvalue = va_list[va_start]
                    va_start += 1
                    if not self.define_set_member(oclass, prop.name, keyword, keyvalue):
                        errno = EINVAL
                        gl_error(
                            f"define_map(oclass='{oclass.name}',...): property keyword '{keyword}' could not be defined as value {keyvalue}"
                        )

                elif proptype == PROPERTYTYPE.PT_ACCESS:
                    prop_buffer = va_list[va_start]
                    va_start += 1
                    pa = PROPERTYACCESS(prop_buffer)
                    if pa == PROPERTYACCESS.PA_PUBLIC or pa == PROPERTYACCESS.PA_PROTECTED or pa == PROPERTYACCESS.PA_PRIVATE or pa == PROPERTYACCESS.PA_REFERENCE or pa == PROPERTYACCESS.PA_HIDDEN:
                        prop.access = pa
                    else:
                        errno = EINVAL
                        gl_error(
                            f"define_map(oclass='{oclass.name}',...): unrecognized property access code (value={pa} is not valid)"
                        )

                elif proptype == PROPERTYTYPE.PT_SIZE:
                    prop.size = va_list[va_start]
                    va_start += 1
                    if prop.size < 1:
                        errno = EINVAL
                        gl_error(f"define_map(oclass='{oclass.name}',...): property size must be greater than 0")

                elif proptype == PROPERTYTYPE.PT_EXTEND:
                    oclass.size += self.property_type[prop.ptype].size
                elif proptype == PROPERTYTYPE.PT_EXTENDBY:
                    oclass.size += va_list[va_start]
                    va_start += 1
                elif proptype == PROPERTYTYPE.PT_FLAGS:
                    prop.flags |= va_list[va_start]
                    va_start += 1
                elif proptype == PROPERTYTYPE.PT_DEPRECATED:
                    prop.flags |= PROPERTYFLAGS.PF_DEPRECATED
                elif proptype == PROPERTYTYPE.PT_UNITS:
                    unitspec = va_list[va_start]
                    va_start += 1
                    try:
                        prop.unit = unit_find(unitspec)
                        if prop.unit is None:
                            gl_error(f"unable to define unit '{unitspec}'")
                    except Exception as msg:
                        gl_error(
                            f"define_map(oclass='{oclass.name}',...): property {prop.name} unit '{unitspec}' is not recognized: {msg}"
                        )

                elif proptype == PROPERTYTYPE.PT_DESCRIPTION:
                    prop.description = va_list[va_start]
                    va_start += 1
                elif proptype == PROPERTYTYPE.PT_HAS_NOTIFY or proptype == PROPERTYTYPE.PT_HAS_NOTIFY_OVERRIDE:
                    notify_fname = f"notify_{prop.oclass.name}_{prop.name}"
                    prop.notify = FUNCTIONADDR()
                    if prop.notify == 0:
                        errno = EINVAL
                        gl_error(f"Unable to find function '{notify_fname}' in {prop.oclass.module.name} module")

                    if proptype == PROPERTYTYPE.PT_HAS_NOTIFY_OVERRIDE:
                        prop.notify_override = True
                    else:
                        prop.notify_override = False
                else:
                    tcode = str(proptype)
                    ptypestr = self.get_property_typename(proptype)
                    if ptypestr == "//UNDEF//":
                        ptypestr = tcode
                    errno = EINVAL
                    gl_error(
                        f"define_map(oclass='{oclass.name}',...): unrecognized extended property (PROPERTYTYPE={ptypestr if ptypestr else tcode})")

            elif proptype == PROPERTYTYPE.PT_enduse:
                name = va_list[va_start]
                va_start += 1
                addr = va_list[va_start]
                va_start += 1
                if self.enduse_publish(oclass, addr, name) <= 0:
                    gl_error(
                        f"define_map(oclass='{oclass.name}',...): substructure of property '{prop.name}' substructure could not be published"
                    )
                    errno = E2BIG

            else:
                delegation = va_list[va_start] if proptype == PROPERTYTYPE.PT_delegated else None
                name = va_list[va_start]
                va_start += 1
                addr = va_list[va_start]
                va_start += 1
                if prop != None and len(name) >= len(prop.name):
                    gl_error(f"define_map(oclass='{oclass.name}',...): property name '{name}' is too big")
                    errno = E2BIG

                if name == "parent":
                    gl_error(
                        f"define_map(oclass='{oclass.name}',...): property name '{name}' conflicts with built-in property")

                elif name == "rank":
                    gl_error(
                        f"define_map(oclass='{oclass.name}',...): property name '{name}' conflicts with built-in property")

                elif name == "clock":
                    gl_error(
                        f"define_map(oclass='{oclass.name}',...): property name '{name}' conflicts with built-in property")

                elif name == "valid_to":
                    gl_error(
                        f"define_map(oclass='{oclass.name}',...): property name '{name}' conflicts with built-in property")

                elif name == "latitude":
                    gl_error(
                        f"define_map(oclass='{oclass.name}',...): property name '{name}' conflicts with built-in property")

                elif name == "longitude":
                    gl_error(
                        f"define_map(oclass='{oclass.name}',...): property name '{name}' conflicts with built-in property")

                elif name == "in_svc":
                    gl_error(
                        f"define_map(oclass='{oclass.name}',...): property name '{name}' conflicts with built-in property")

                elif name == "out_svc":
                    gl_error(
                        f"define_map(oclass='{oclass.name}',...): property name '{name}' conflicts with built-in property")

                elif name == "name":
                    gl_error(
                        f"define_map(oclass='{oclass.name}',...): property name '{name}' conflicts with built-in property")

                elif name == "flags":
                    gl_error(
                        f"define_map(oclass='{oclass.name}',...): property name '{name}' conflicts with built-in property")

                prop = PROPERTY(proptype, oclass, name, addr, delegation)
                if prop == None:
                    pass
                if proptype == PROPERTYTYPE.PT_method:
                    prop.addr = 0
                    prop.method = None
                self.add_property(oclass, prop)
                count += 1
                if prop.ptype > PROPERTYTYPE.PT_last:
                    prop = None
        return count

    def define_enumeration_member(self, oclass, property_name, member, value):
        prop = self.find_property(oclass, property_name)
        key = KEYWORD()
        if prop == None or key == None:
            return 0
        key.next = prop.keywords
        key.name = member
        key.value = value
        prop.keywords = key
        return 1

    def define_set_member(self, oclass, property_name, member, value):
        prop = self.find_property(oclass, property_name)
        key = KEYWORD()
        if not prop or not key:
            return 0
        if not prop.keywords:
            prop.flags |= PROPERTYFLAGS.PF_CHARSET  # Enable single character keywords until a long keyword is defined
        key.next = prop.keywords
        key.name = member.encode('utf-8')
        key.value = value
        prop.keywords = key
        return 1

    def define_function(self, oclass, functionname, call):
        if self.get_function(oclass.name, functionname) is not None:
            gl_error(
                f"define_function(Class *class={{name='{oclass.name}',...}}, FUNCTIONNAME functionname='{functionname}', ...) the function name has already been defined")
            errno = 1
            return None

        func = FUNCTION()
        if not func:
            errno = ENOMEM
            return None
        func.addr = call
        func.name = functionname.encode('utf-8')
        func.next = None
        func.oclass = oclass
        if not oclass.fmap:
            oclass.fmap = func
        elif not oclass.fmap.next:
            oclass.fmap.next = func
        else:
            tempfunc = oclass.fmap
            while tempfunc.next:
                tempfunc = tempfunc.next
            tempfunc.next = func

        return func

    def get_function(self, classname, functionname):
        oclass = self.get_from_classname(classname)
        func = oclass.fmap
        while func and func.oclass == oclass:
            if func.name.decode('utf-8') == functionname:
                return func.addr
            func = func.next
        self.errno = ENOENT
        return None

    def saveall(self, fp):
        count = 0
        fp.write("\n////////////////////////////////////////////////////////\n")
        fp.write("// classes\n")
        oclass = self.get_first_class()
        while oclass:
            prop = oclass.pmap
            fp.write("class {} {{\n".format(oclass.name.decode('utf-8')))
            if oclass.parent:
                fp.write("#ifdef INCLUDE_PARENT_CLASS\n\tparent {};\n#endif\n".format(
                    oclass.parent.name.decode('utf-8')))
            func = oclass.fmap
            while func and func.oclass == oclass:
                fp.write("#ifdef INCLUDE_FUNCTIONS\n\tfunction {}();\n#endif\n".format(
                    func.name.decode('utf-8')))
                func = func.next
            while prop and prop.oclass == oclass:
                ptype = self.get_property_typename(prop.ptype)
                if ptype:
                    if b'.' not in prop.name:
                        fp.write("\t{} {};\n".format(ptype, prop.name.decode('utf-8')))
                    else:
                        fp.write("#ifdef INCLUDE_DOTTED_PROPERTIES\t{} {};\n#endif\n".format(
                            ptype, prop.name.decode('utf-8')))
                prop = prop.next
            fp.write("}\n")
            oclass = oclass.next
        return count

    def saveall_xml(self, fp):
        count = 0
        fp.write("\t<classes>\n")
        oclass = self.get_first_class()
        while oclass:
            prop = oclass.pmap
            fp.write("\t\t<class name=\"{}\">\n".format(oclass.name))
            if oclass.parent:
                fp.write("\t\t<parent>{}</parent>\n".format(oclass.parent.name))
            func = oclass.fmap
            while func and func.oclass == oclass:
                fp.write("\t\t<function>{}</function>\n".format(func.name.decode('utf-8')))
                func = func.next
            while prop and prop.oclass == oclass:
                propname = self.get_property_typename(prop.ptype)
                if propname:
                    fp.write("\t\t\t<property type=\"{}\">{}</property>\n".format(
                        propname, prop.name.decode('utf-8')))
                prop = prop.next
            fp.write("\t\t</class>\n")
            oclass = oclass.next
        fp.write("\t</classes>\n")
        return count

    def profiles(self,):
        total = 0
        count = 0
        i = 0
        hits = 0
        print("Model profiler results")
        print("======================\n")
        print("Class            Time (s) Time (%%) msec/self")
        print("---------------- -------- -------- --------")
        cl = self.first_class
        while cl:
            total += cl.profiler.clocks
            count += 1
            cl = cl.next

        if count == 0:
            return

        index = Class()
        i = 0
        cl = self.first_class
        while cl:
            index[i] = cl
            i += 1
            cl = cl.next

        hits = -1
        while hits != 0:
            hits = 0
            for i in range(count - 1):
                if index[i].profiler.clocks < index[i + 1].profiler.clocks:
                    index[i], index[i + 1] = index[i + 1], index[i]
                    hits += 1

        for i in range(count):
            cl = index[i]
            if cl.profiler.clocks > 0:
                ts = float(cl.profiler.clocks) / global_ms_per_second
                tp = float(cl.profiler.clocks) / total * 100
                mt = ts / cl.profiler.numobjs * 1000
                print("{:<16.16s} {:7.3f} {:8.1f}% {:8.1f}".format(cl.name.decode('utf-8'), ts, tp, mt))
            else:
                break

        index = None
        print("================ ======== ======== =======")
        print("{:<16.16s} {:7.3f} {:8.1f}% {:8.1f}".format("Total", float(total) / global_ms_per_second, 100.0,
                                                                    1000 * float(
                                                                        total) / global_ms_per_second / self.object_get_count()))

    def register_type(self, oclass, ptype, from_string, to_string):
        dt = DELEGATEDTYPE()
        if dt:
            dt.oclass = oclass
            dt.type = ptype.encode('utf-8')
            dt.from_string = from_string
            dt.to_string = to_string
        else:
            gl_error("unable to register delegated type (memory allocation failed)")
            # TROUBLESHOOT
            # Property delegation is not supported yet, so this should never happen.
            # This is most likely caused by a lack of memory or an unstable system.
        return dt

    def add_loadmethod(self, oclass, name, call):
        method = LOADDATA()
        method.name = name.encode('utf-8')
        method.call = call
        method.next = oclass.loadmethods
        oclass.loadmethods = method
        return 1

    def get_loadmethod(self, oclass, name):
        method = oclass.loadmethods
        while method:
            if method.name.decode('utf-8') == name:
                return method
            method = method.next
        return None

    def define_type(self, oclass, delegation, *args):
        gl_error("delegated types not supported using define_type (use define_map instead)")
        # TROUBLESHOOT
        # Property delegation is not supported yet, so this should never happen.
        # This is most likely caused by a lack of memory or an unstable system.
        return 0


    def get_xsd(self, oclass, buffer, len_):
        n = 0
        prop = None
        i = 0
        oc = oclass
        # Assuming oflags is defined elsewhere
        oflags = []
        attribute = [
            {"name": "id", "type": "integer", "keys": None},
            {"name": "parent", "type": "string", "keys": None},
            {"name": "rank", "type": "integer", "keys": None},
            {"name": "clock", "type": "string", "keys": None},
            {"name": "valid_to", "type": "string", "keys": None},
            {"name": "latitude", "type": "string", "keys": None},
            {"name": "longitude", "type": "string", "keys": None},
            {"name": "in_svc", "type": "string", "keys": None},
            {"name": "out_svc", "type": "string", "keys": None},
            {"name": "flags", "type": "string", "keys": oflags},
        ]

        check = 1

        n += self.buffer_write(buffer + n, len_ - n, f"<xs:element name=\"{oclass.name}\">\n")
        n += self.buffer_write(buffer + n, len_ - n, "\t<xs:complexType>\n")
        n += self.buffer_write(buffer + n, len_ - n, "\t\t<xs:all>\n")

        for i in range(len_(attribute)):
            n += self.buffer_write(buffer + n, len_ - n, f"\t\t\t<xs:element name=\"{attribute[i]['name']}\">\n")
            n += self.buffer_write(buffer + n, len_ - n, "\t\t\t\t<xs:simpleType>\n")

            if attribute[i]['keys'] is None:
                n += self.buffer_write(buffer + n, len_ - n, f"\t\t\t\t\t<xs:restriction base=\"xs:{attribute[i]['type']}\"/>\n")
            else:
                keys = attribute[i]['keys']
                n += self.buffer_write(buffer + n, len_ - n, "\t\t\t\t\t<xs:restriction base=\"xs:string\">\n")
                n += self.buffer_write(buffer + n, len_ - n, "\t\t\t\t\t\t<xs:pattern value=\"")

                for key in keys:
                    n += self.buffer_write(buffer + n, len_ - n, f"{'' if key == keys[0] else '|'}{key['name']}")

                n += self.buffer_write(buffer + n, len_ - n, "\"/>\n")
                n += self.buffer_write(buffer + n, len_ - n, "\t\t\t\t\t</xs:restriction>\n")

            n += self.buffer_write(buffer + n, len_ - n, "\t\t\t\t</xs:simpleType>\n")
            n += self.buffer_write(buffer + n, len_ - n, "\t\t\t</xs:element>\n")

        while oc is not None:
            for prop in oc.pmap:
                if prop.oclass == oc:
                    proptype = self.get_property_typexsdname(prop.ptype)

                    if prop.unit is not None:
                        n += self.buffer_write(buffer + n, len_ - n,
                                          f"\t\t\t\t<xs:element name=\"{prop.name}\" type=\"xs:string\"/>\n")
                    else:
                        n += self.buffer_write(buffer + n, len_ - n, f"\t\t\t<xs:element name=\"{prop.name}\">\n")
                        n += self.buffer_write(buffer + n, len_ - n, "\t\t\t\t<xs:simpleType>\n")
                        n += self.buffer_write(buffer + n, len_ - n,
                                          f"\t\t\t\t\t<xs:restriction base=\"xs:{'string' if proptype is None else proptype}\">\n")

                        if prop.keywords is not None:
                            keywords = prop.keywords
                            n += self.buffer_write(buffer + n, len_ - n, "\t\t\t\t\t<xs:pattern value=\"")

                            for key in keywords:
                                n += self.buffer_write(buffer + n, len_ - n, f"{'' if key == keywords[0] else '|'}{key['name']}")

                            n += self.buffer_write(buffer + n, len_ - n, "\"/>\n")

                        n += self.buffer_write(buffer + n, len_ - n, "\t\t\t\t\t</xs:restriction>\n")
                        n += self.buffer_write(buffer + n, len_ - n, "\t\t\t\t</xs:simpleType>\n")
                        n += self.buffer_write(buffer + n, len_ - n, "\t\t\t</xs:element>\n")

            oc = oc.parent

        n += self.buffer_write(buffer + n, len_ - n, "\t\t</xs:all>\n")
        n += self.buffer_write(buffer + n, len_ - n, "\t</xs:complexType>\n")
        n += self.buffer_write(buffer + n, len_ - n, "</xs:element>\n")
        buffer[n] = 0

        if check == 0:
            print("get_xsd() overflowed.\n")
            buffer[0] = 0
            return 0

        return n
