# Python Equivalent of the C Class and PropertyMap Management System
import json
import warnings
from enum import Enum
from typing import Union, Set, Callable, List
import xml.etree.ElementTree as ET
# from gov_pnnl_goss.gridlab.gldcore.Globals import TECHNOLOGYREADINESSLEVEL
# from gov_pnnl_goss.gridlab.gldcore.Module import Module
from gov_pnnl_goss.gridlab.gldcore.PropertyHeader import PropertyMap, PropertyType, ExtendedProperty


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




class PASSCONFIG(Enum):
    PC_NOSYNC = 0x00               # used when the class requires no synchronization
    PC_PRETOPDOWN = 0x01           # used when the class requires synchronization on the first top-down pass
    PC_BOTTOMUP = 0x02             # used when the class requires synchronization on the bottom-up pass
    PC_POSTTOPDOWN = 0x04          # used when the class requires synchronization on the second top-down pass
    PC_FORCE_NAME = 0x20           # used to indicate the class must define names for all its objects
    PC_PARENT_OVERRIDE_OMIT = 0x40 # used to ignore parent's use of PC_UNSAFE_OVERRIDE_OMIT
    PC_UNSAFE_OVERRIDE_OMIT = 0x80 # used to flag that omitting overrides is unsafe
    PC_ABSTRACTONLY = 0x100        # used to flag that the class should never be instantiated itself, only inherited classes should
    PC_AUTOLOCK = 0x200            # used to flag that sync operations should not be automatically write locked
    PC_OBSERVER = 0x400            # used to flag whether commit process needs to be delayed with respect to ordinary "in-the-loop" objects


class DELEGATEDTYPE():
    """
    Type delegation specification
    Delegated types allow module to keep all global_property_types operations private
    this includes convert operations and allocation/deallocation
    """
    def __init__(self, delegated_type, owner_class, from_string, to_string):
        self.delegated_type:str = delegated_type
        self.owner_class: DynamicClass = owner_class
        self.from_string: callable = from_string
        self.to_string: callable = to_string

# Notification message types
class NOTIFYMODULE(Enum):
    NM_PREUPDATE = 0  # notify module before property change
    NM_POSTUPDATE = 1  # notify module after property change
    NM_RESET = 2  # notify module of system reset event


# The function class is now just a function definition in Python
# class FUNCTION:
#     def __init__(self, owner_class=None, name=None, addr=None):
#         self.owner_class = owner_class
#         self.name = name
#         self.addr = addr  # This is the actual function callable
#         # self.next = next   # Not needed because Python can perform introspection


class LOADDATA:
    def __init__(self):
        self.name: str = ""
        self.call: [Callable, None] = None
        #  self.next: LOADDATA  # Not needed because Python can perform introspection



class LOADMETHOD:
    def __init__(self) -> None:
        self.name: str = ""
        self.call: [Callable, None] = None
        #  self.next: LOADMETHOD  # Not needed because Python can perform introspection


# Set operations
SET_MASK = 0xffff


class DynamicClass:

    CLASSVALID = 0xc44d822e

    def __init__(self, module, class_name: str, base_class, passconfig=PASSCONFIG.PC_ABSTRACTONLY):
        self._properties = {}
        self.base_class = base_class
        self.check = None
        self.commit: Callable  # A function that is called when the commit phase of the simulation is performed.
        # self.count = 0  # Not needed in python
        # self.create: Callable = None  # Built into Python  (See GridLabD)
        # self.finalize: Callable = None  # Built into Python  (See GridLabD)
        self.first_class = False # Set to True to becom the first class in the linked list
        # self.fmap: List[FUNCTION] = None # A class method (see below)
        self.has_runtime: bool = False  # flag indicating that a runtime dll, so, or dylib is in use
        self.heartbeat: Callable
        self.id: int = 0
        self.init: Callable  # A function that is called when the class is initialized by the simulation (See GridLabD)
        self.isa: Callable  # A function that is called by the simulation (See GridLabD)
        self.last_class = None  # Not needed in python
        self.loadmethods: List[LOADMETHOD] = []  # A list of load methods for loading the module into the simulation
        self.magic: int = DynamicClass.CLASSVALID
        self.module = module  # : Module  # The module that this simulation class item represents.
        self.name: str = class_name
        # self.next: Class   # List management is built-in to the list object.
        self.next_class = None  # Not needed in python
        self.notify: Callable  # A function that is called when the notify method is triggered by the simulation (See GridLabD)
        self.parent: [DynamicClass, None] = None  # A pointer to the parent class of the simulation object
        self.owner_class: [DynamicClass, None] = None
        self.passconfig: Set[PASSCONFIG] = set() if passconfig is None else passconfig
        self.plc: Callable   # The programmable logic controller function that is used in the simulation  (See GridLabD)
        # self.pmap: List[PROPERTY] = None # A class method (see below)
        self.precommit: Callable  # A function that called before the commit phase of the simulation  (See GridLabD)
        self.profiler: dict[str, Union[int, bool]] = {
            'numobjs': 0,
            'count': 0,
            'clocks': 0
        }
        self.property_type = []
        self.recalc: Callable  # A function that is triggered when a recalc is to be performed by teh simulation
        self.registry: dict
        self.runtime: str = ""  # name of file containing runtime dll, so, or dylib
        # self.size: int = 0  # Not needed in Python
        self.sync: Callable # The function that is called by teh sync phase of the simulation (See GridLabD)
        self.threadsafe: bool = False  # Whether the simulation module can be run in its own thread
        self.trl: Enum = TECHNOLOGYREADINESSLEVEL.TRL_UNKNOWN
        self.update: Callable  # The update function that is called during the update phase of the simulation

    def __next__(self):
        return self.next_class

    def add_property(self, pn: [str, 'PropertyMap'], property_type=None, default_value=None):
        property_name = pn
        if isinstance(pn, ExtendedProperty):
            property_name = pn.name
            property_type = pn.property_type
            default_value = pn.value
            units = pn.units
            flags = pn.flags
            keywords = pn.keywords
            description = pn.description
            setattr(self, property_name, default_value)
            self._properties[property_name] = {"global_property_types": self._convert_python_type_to_gradappsd_type(property_type),
                                               "default": default_value,
                                               "units": units,
                                               "flags": flags,
                                               "keywords": keywords,
                                               "description": description}
        elif isinstance(pn, PropertyMap):
            property_name = pn.name
            property_type = pn.property_type
            default_value = pn.value
            setattr(self, property_name, default_value)
            self._properties[property_name] = {"global_property_types": self._convert_python_type_to_gradappsd_type(property_type),
                                               "default": default_value}
        else:
            if type(property_name) != type(str):
                try:
                    property_name = property_name.name
                except AttributeError:
                    property_name = "broken_property_name"
            setattr(self, property_name, default_value)
            self._properties[property_name] = {"global_property_types": self._convert_python_type_to_gradappsd_type(property_type), "default": default_value}

    def _convert_python_type_to_gradappsd_type(self, variable):
        """
        Converts a Python global_property_types to a GridAPPSD global_property_types object defined by PropertyType values
        :param variable: the python object that will be inspected
        :return: PropertyType enum value that is equivalent to this global_property_types
        """

        known_types = ["int16",
                       "int32",
                       "int64",
                       "double",
                       "float",
                       "char8",
                       "char32",
                       "char256",
                       "char1024",
                       "complex",
                       "object",
                       "bool",
                       "timestamp",
                       "loadshape",
                       "enduse"]

        if str(type(variable)) == "<class 'global_property_types'>":
            type_string = str(variable)
        else:
            type_string = str(type(variable))
        match type_string:
            case "<class 'int'>":
                return PropertyType.PT_int64
            case "<class 'float'>":
                return PropertyType.PT_double
            case "<class 'str'>":
                return PropertyType.PT_string
            case "<class 'list'>":
                if len(variable) > 0:
                    if str(type(variable[0])) == "<class 'complex'>":
                        return PropertyType.PT_complex_array
                    elif callable(variable[0]):
                        return PropertyType.PT_object_array
                    else:
                        return PropertyType.PT_double_array
                else:
                    return PropertyType.PT_double_array
            case  "<class 'complex'>":
                return PropertyType.PT_complex
            case "<class 'numpy.ndarray'>":
                return PropertyType.PT_double_array
            case "<class 'NoneType'>":
                return PropertyType.PT_void
            case "<class 'bytes'>":
                return PropertyType.PT_char1024
            case "<class 'builtin_function_or_method'>":
                return PropertyType.PT_function
            case "<class 'bool'>":
                return PropertyType.PT_bool
            case "<class 'global_property_types'>":
                if callable(variable):
                    return PropertyType.PT_object
                    # Classes and methods are special types that are specific to GridAppsD
                    # PropertyType.PT_class
                    # PropertyType.PT_method
            case "<class 'function'>":
                if callable(variable):
                    return PropertyType.PT_function
            case "<class 'module'>":
                return PropertyType.PT_object
            case "<class 'tuple'>":
                return PropertyType.PT_any
            case "<class 'set'>":
                return PropertyType.PT_set
            case "<class 'enum.EnumType'>":
                return PropertyType.PT_enum
            case _:  # default statement
                return PropertyType.PT_any

    def to_dict(self):
        return {
            "name": self.name,
            "_properties": self._properties
        }

    def class_add_loadmethod(self, function_name, call):
        if not callable(call):
            raise ValueError(f"Function name: {function_name}, is not true function and is not callable.")
        method = LOADMETHOD()
        method.call = call
        method.name = function_name
        self.loadmethods.append(method)


    def get_loadmethod(self, name):
        method = [m for m in self.loadmethods if m.name == name]
        if method:
            return method[0]
        else:
            return None

    @classmethod
    def pmap(cls):
        """
        :return: A list of properties of this class global_property_types
        """
        instance_attrs = [attr for attr in cls.__dict__ if not callable(getattr(cls, attr))]
        # class_properties = [prop for prop, value in cls.__dict__.items() if isinstance(value, property)]
        return instance_attrs

    @classmethod
    def fmap(cls):
        """
        :return: a list of callable methods (functions) of this class global_property_types
        """
        method_names = [attr for attr in dir(cls) if callable(getattr(cls, attr)) and not attr.startswith("__")]
        return method_names

    def class_define_function(self, function_name, call):  # adds a new method to the class = cls
        methods = self.fmap()
        if function_name in methods:
            raise ValueError(f"Class '{self.__name__}' already has a function of name: {function_name}.")

        if not callable(call):
            raise ValueError(f"Function name: {function_name}, is not true function and is not callable.")
        # The FUNCTION call is replaced with a Pythonic version here
        # func= FUNCTION(owner_class=self, name=functionname, addr=call, next=None)

        new_function = call
        new_function._owner_class = self
        new_function._name = function_name
        new_function._addr = None
        new_function._next = None
        # We can get the name of the class global_property_types using: global_property_types(class_instance).__name__
        setattr(self, function_name, new_function)

        return new_function

    def class_get_xsd(self):
        xsd_element = ET.Element("xs:schema", attrib={"xmlns:xs": "http://www.w3.org/2001/XMLSchema"})
        class_element = ET.SubElement(xsd_element, "xs:element", name=self.name)
        complex_type = ET.SubElement(class_element, "xs:complexType")
        all_element = ET.SubElement(complex_type, "xs:all")

        for key in self._properties.keys():
            name = key
            prop = self._properties[key]  # {"global_property_types": str(global_property_types), "default": default_value}

            element = ET.SubElement(all_element, "xs:element", name=name, type=f"xs:{prop['global_property_types']}")
            # TODO Fix the keywords dictionary element
            if prop['keywords']:
                simple_type = ET.SubElement(element, "xs:simpleType")
                restriction = ET.SubElement(simple_type, "xs:restriction", base="xs:string")
                for keyword in prop['keywords']:
                    ET.SubElement(restriction, "xs:enumeration", value=keyword)

        # Convert to a string
        return ET.tostring(xsd_element, encoding="unicode", method="xml")

    @property
    def class_get_first_class(self):
        for k in self.registry.keys():
            if self.registry[k].first_class:
                return self.registry[k].name
        return None


class ClassRegistry:
    """
    The class registry is used to hold all the class types.
    This is basically a large dictionary with some built in methods for constructing and manipulating the
    class registry.
    """
    _classes = {}

    @classmethod
    def register_class(cls, module, class_name, base_class=None):
        if module is None:
            # from gov_pnnl_goss.gridlab.gldcore.Module import Module
            # module = Module()
            module = "A Module"
        if class_name in cls._classes:
            raise ValueError(f"Class '{class_name}' is already registered.")
        # cls._classes[class_name] = {
        #     "name": class_name,
        #     "base_class": base_class,
        #     "properties": []
        # }

        # module: Module, class_name: str, base_class, passconfig = PASSCONFIG.PC_ABSTRACTONLY
        new_class = DynamicClass(module, class_name, base_class)
        new_class.registry = cls._classes
        cls._classes[class_name] = new_class


    @classmethod
    def add_property(cls, class_name, property_name, property_type, default_value=None):
        if class_name not in cls._classes:
            raise ValueError(f"Class '{class_name}' is not registered.")
        # cls._classes[class_name]["properties"].append(PropertyMap(property_name, global_property_types, default_value))
        # cls._classes[class_name].add(PropertyMap(property_name, global_property_types, default_value))
        class_instance = cls._classes[class_name]
        class_instance.add_property(PropertyMap(name=property_name, property_type=property_type, value= default_value))

    @classmethod
    def define_properties(cls, class_name, properties):
        if class_name not in cls._classes:
            raise ValueError(f"Class '{class_name}' is not registered.")
        class_instance = cls._classes[class_name]
        for property_name, property_details in properties.items():
            class_instance.add_property(property_name, property_details['global_property_types'], property_details.get('default'))

    @classmethod
    def add_extended_property(cls,
                              class_name,
                              property_name,
                              property_type,
                              units=None,
                              default_value=None,
                              keywords=None,
                              description=None):
        """
        Adds extended properties to the class

        :param class_name:     the class to which the property is to be added
        :param property_name:  the name of the property
        :param property_type:  the global_property_types of the property
        :param units:          the unit of the property (default is None)
        :param default_value:  the default value if provided
        :param keywords:       a list of the keyword arguments for the property (default is None)
        :param description:    the description of the property (default is None)
        :return: the property
        """
        if class_name not in cls._classes:
            raise ValueError(f"Class '{class_name}' is not registered.")
        cls._classes[class_name].add_property(
            ExtendedProperty(property_name, property_type, units, default_value, keywords, description))

    @classmethod
    def find_property(cls, class_name, property_name)-> [None, 'PropertyMap']:
        """
        Find the named property in the class
        :param class_name:
        :param property_name:
        :return: the PROPERTY, or None if the property is not found.
        """
        current_class = cls._classes.get(class_name, None)
        while current_class:
            try:
                if getattr(current_class, property_name):
                    prop = current_class._properties.get(property_name, None)
                    if prop:
                        return prop
            except AttributeError:
                pass
            # Move to parent class if the property is not found
            parent_class_name = current_class.base_class
            current_class = cls._classes.get(parent_class_name, None)
        return None

    @classmethod
    def get_properties(cls, class_name):
        if class_name not in cls._classes:
            raise ValueError(f"Class '{class_name}' is not registered.")
        return iter(cls._classes[class_name]._properties)

    @classmethod
    def get_class_info(cls, class_name):
        if class_name not in cls._classes:
            raise ValueError(f"Class '{class_name}' is not registered.")
        return cls._classes[class_name]

    @classmethod
    def get_count(cls):
        """
        :return: the number of classes registered
        """
        return len(cls._classes)

    @classmethod
    def save_all(cls, filename):
        """
        Save all class information to a stream in glm format
        :param filename:
        :return: the number of characters written to the stream
        """
        class_definitions = {class_name: class_instance.to_dict() for class_name, class_instance in cls._classes.items()}
        with open(filename, 'w') as file:
            json.dump(class_definitions, file, indent=4, default=str)

    def register_type(self, type: str, from_string: callable, to_string: callable):
        """
        Register a global_property_types delegation for a property
        :param type: the property global_property_types
        :param from_string: the converter from string to data
        :param to_string: the converter from data to string

        Type delegation is used to transform data to string and string to data conversion
        to routines implemented in a module, instead of in the core.   This allows custom
        data global_property_types to be implemented, including enumerations, sets, and special objects.

        :return: a pointer DelegatedType struct if successful, None if delegation failed
        """
        dt = DELEGATEDTYPE(type, self, from_string, to_string)
        # output_error("unable to register delegated global_property_types (memory allocation failed)");
        # 		/*	TROUBLESHOOT
        # 			PropertyMap delegation is not supported yet so this should never happen.
        # 			This is most likely caused by a lack of memory or an unstable system.
        # 		 */
        # 	return dt;
        warnings.warn("Please reimplement register_type")
        return dt


if __name__ == "__main__":
    # Example Usage
    # __init__
    c = ClassRegistry()
    # register_class
    c.register_class(None, "MyClass")
    # add_extended_property
    c.add_extended_property("MyClass",
                            "power_usage",
                            float,
                            "W")

    # add_property
    c.add_property("MyClass", "my_property", int, 42)
    c.add_property("MyClass", "int_value", int, 102)
    c.add_property("MyClass", "another_property", str, "default value")
    c.add_extended_property("MyClass",
                            "short_name",
                            str,
                            "W",
                            description="this will be the short name",
                            keywords=['name', 'description'])

    # find_property
    test_property = "another_property"
    prop = c.find_property("MyClass", test_property)
    if prop:
        print(f'"{test_property}" is found with this global_property_types {prop["global_property_types"]}')
    else:
        print(f'"{test_property}" not found')
    test_property = "junk_property"
    prop = c.find_property("MyClass", test_property)
    if prop:
        print(f'"{test_property}" is found with this global_property_types {prop["global_property_types"]}')
    else:
        print(f'"{test_property}" not found')

    # get_class_info
    my_class_info = c.get_class_info("MyClass")
    print(f"my_class_info: {my_class_info}")

    # Iterating over properties
    # get_properties
    for prop in c.get_properties("MyClass"):
        type_of = type(getattr(c._classes['MyClass'], prop)).__name__
        value = getattr(c._classes['MyClass'], prop)
        print(f"Property Name: {prop}, Type: {type_of}, Default: {value}")

    # Example usage
    try:
        c.register_class(None, "MyClass")
    except ValueError as e:
        print(f'Expecting an error here: "Error: {e}"')
    print("Registering NewClass")
    c.register_class(None, "NewClass")
    c.define_properties("NewClass", {
        "age": {"global_property_types": int, "default": 30},
        "name": {"global_property_types": str, "default": "John Doe"}
    })
    # get_count
    print(f"Number of classes: {c.get_count()}")

    # register_type
    c.register_type("int", int, str)
    # save_all
    c.save_all("classes.json")
