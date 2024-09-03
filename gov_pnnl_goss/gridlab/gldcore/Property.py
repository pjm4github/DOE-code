from enum import Enum
from typing import Callable

import numpy as np

from gridlab.gldcore.Compare import TCOPB, TCOPS, TCNONE
from gridlab.gldcore.Convert import *
from gridlab.gldcore.PropertyHeader import PropertyMap, PropertyStruct, PropertSpec

by_ref = 0x01
from gridlab.gldcore.PropertyHeader import PropertyType

import numpy as np

class ComplexArray:
    def __init__(self, rows=0, cols=0, data=None, name=None):
        self.n, self.m = rows, cols
        self.max_val = max(rows, cols)
        self.x = np.zeros((rows, cols), dtype=np.complex) if data is None else np.array(data, dtype=np.complex)
        self.f = np.zeros((rows, cols), dtype=np.uint8)
        self.name = name or ""

    def exception(self, msg):
        full_msg = f"{self.name}: {msg}"
        raise Exception(full_msg)

    def set_flag(self, r, c, b):
        self.f[r, c] |= b

    def clr_flag(self, r, c, b):
        self.f[r, c] &= ~b

    def tst_flag(self, r, c, b):
        return (self.f[r, c] & b) == b

    def grow_to(self, rows, cols):
        new_size = max(rows, cols)
        if new_size > self.max_val:
            new_x = np.zeros((new_size, new_size), dtype=complex)
            new_x[:self.n, :self.m] = self.x
            self.x = new_x
            new_f = np.zeros((new_size, new_size), dtype=np.uint8)
            new_f[:self.n, :self.m] = self.f
            self.f = new_f
            self.max_val = new_size
        self.n, self.m = rows, cols

    def set_at(self, r, c, value):
        if not (0 <= r < self.n) or not (0 <= c < self.m):
            self.exception("Index out of bounds")
        self.x[r, c] = value

    def get_at(self, r, c):
        if not (0 <= r < self.n) or not (0 <= c < self.m):
            self.exception("Index out of bounds")
        return self.x[r, c]

    # Implement other methods as needed, following the above patterns.

    def __str__(self):
        return f"ComplexArray named {self.name} with shape {self.n}x{self.m}"



class ComplexVector:
    def __init__(self, data: [complex]):
        self.data = data

    def __getitem__(self, n):
        if self.data[n] is None:
            self.data[n] = 0.0 + 0.0j
        return self.data[n]

    def __setitem__(self, n, value):
        if self.data[n] is None:
            self.data[n] = 0.0 + 0.0j
        self.data[n] = value

    def __str__(self):
        return f"ComplexVectorConst with {len(self.data)} elements"


# Get the property global_property_types by name
def property_get_type(name):
    for ptype in range(len(global_property_types)):
        if global_property_types[ptype].name.decode('utf-8') == name:
            return ptype
    return 0


# Get a part of a property (specific to complex global_property_types)
def complex_get_part(x, name):
    c = complex(x)
    if name == "real":
        return c.real
    elif name == "imag":
        return c.imag
    elif name == "mag":
        return math.hypot(c.real, c.imag)
    elif name == "arg":
        return math.atan2(c.imag, c.real)
    elif name == "ang":
        return math.atan2(c.imag, c.real) * 180 / math.pi
    return math.nan

def double_array_create(a):
    return np.zeros(0)


# Get a part of a double array
def double_array_get_part(x, name):
    try:
        n, m = map(int, name.split('.'))
        a = x
        if n < len(a) and m < len(a[n]):
            return a[n][m]
    except ValueError:
        pass
    return math.nan


# Create a complex array
def complex_array_create():
    a = [complex(0)]
    return a, 1


def complex_array_get_part(x, name):
    try:
        n, m, subpart = name.split('.')
        n, m = int(n), int(m)
        a = x
        if n < len(a) and m < len(a[n]):
            if subpart == "real":
                return a[n][m][0]
            elif subpart == "imag":
                return a[n][m][1]
    except ValueError:
        pass
    return math.nan


# Define the real global_property_types based on the REAL4 preprocessor directive
REAL4 = True  # Change this to False for double precision
real = float if REAL4 else None  # double



class PROPERTYCOMPAREOP(Enum):
    # Define PROPERTYCOMPAREOP enumeration
    TCOP_EQ = 0  # property are equal to a
    TCOP_LE = 1  #  property is less than or equal to a
    TCOP_GE = 2  #  property is greater than or equal a
    TCOP_NE = 3  #  property is not equal to a
    TCOP_LT = 4  #  property is less than a
    TCOP_GT = 5  #  property is greater than a
    TCOP_IN = 6  #  property is between a and b (inclusive)
    TCOP_NI = 7  #  property is not between a and b (inclusive)
    TCOP_LAST = 8
    TCOP_NOP = 9
    TCOP_ERR = -1


class PropertyValue:
    def __init__(self, name, value, next_prop=None, ptype=None,
                 unit="", description = "", flags=0, keywords=None, size=0, offset=0,
                 attributes=None, extra1=None, extra2=None, function1=None, function2=None):
        self.name = name
        self.value = value
        self.next = next_prop
        self.method: [None, Callable] = None  # A callable method on this property
        self.type = ptype
        self.size = size
        self.offset = offset
        self.attributes = attributes
        self.extra1 = extra1
        self.extra2 = extra2
        self.function1 = function1
        self.function2 = function2

        self.unit = unit
        self.description = description
        self.flags = flags
        self.keywords = keywords



# TODO: Fix "method" - was missing from list and causing segfaults, so populated.  No idea if it works or what it does

# Example initialization functions for different types

def initialize_type_1(addr):
    # Initialize a property of type 1
    default_value_for_type_1 = "None"
    addr.value = default_value_for_type_1

def convert_from_boolean():
    pass

def convert_to_boolean():
    pass

def convert_from_complex():
    pass

def convert_to_complex():
    pass

def convert_from_complex_array():
    pass

def convert_to_complex_array():
    pass

def convert_from_delegated():
    pass

def convert_to_delegated():
    pass

def convert_from_double_array():
    pass

def convert_to_double_array():
    pass

def convert_from_enduse():
    pass

def convert_to_enduse():
    pass

def enduse_create():
    pass

def enduse_get_part():
    pass

def convert_from_enumeration():
    pass

def convert_to_enumeration():
    pass

def convert_from_int16():
    pass

def convert_to_int16():
    pass

def convert_from_loadshape():
    pass

def convert_to_loadshape():
    pass

def loadshape_create():
    pass

def convert_from_method():
    pass

def convert_to_method():
    pass

def convert_from_object():
    pass

def convert_to_object():
    pass

def timestamp_get_part():
    pass

def convert_to_randomvar():
    pass

def convert_from_randomvar():
    pass

def randomvar_create():
    pass

def random_get_part():
    pass

def convert_from_set():
    pass

def convert_to_set():
    pass

def convert_from_timestamp_stub():
    pass

def convert_to_timestamp_stub():
    pass

def convert_from_void():
    pass

def convert_to_void():
    pass

global_property_types = [
    PropertSpec(name=b'example_type_1', create=lambda addr: initialize_type_1(addr)),  # Example
    PropertSpec(name=b"bool", xsdname=b"string", data_to_string=convert_from_boolean, string_to_data=convert_to_boolean, create=None, stream=None, compare=TCOPB,),
    PropertSpec(name=b"char", xsdname=b"string", data_to_string=None, string_to_data=None,create=None, stream=None, compare=TCOPS),
    PropertSpec(name=b"complex", xsdname=b"string", data_to_string=convert_from_complex, string_to_data=convert_to_complex, create=None, stream=None, compare=TCOPS, get_part=complex_get_part),
    PropertSpec(name=b"complex_array", xsdname=b"string", data_to_string=convert_from_complex_array, string_to_data=convert_to_complex_array, create=complex_array_create, stream=None, compare=TCNONE, get_part=complex_array_get_part),
    PropertSpec(name=b"delegated", xsdname=b"string", data_to_string=convert_from_delegated, string_to_data=convert_to_delegated),
    PropertSpec(name=b"double", xsdname=b"decimal", data_to_string=str, string_to_data=float, create=None, stream=None, compare=None),
    PropertSpec(name=b"double_array", xsdname=b"string", data_to_string=convert_from_double_array, string_to_data=convert_to_double_array, create=double_array_create, stream=None, compare=TCNONE, get_part=double_array_get_part),
    PropertSpec(name=b"enduse", xsdname=b"string", data_to_string=convert_from_enduse, string_to_data=convert_to_enduse, create=enduse_create, stream=None, compare=TCOPS, get_part=enduse_get_part),
    PropertSpec(name=b"enumeration", xsdname=b"string", data_to_string=convert_from_enumeration, string_to_data=convert_to_enumeration, create=None, stream=None, compare=TCOPS,),
    PropertSpec(name=b"float", xsdname=b"decimal", data_to_string=str, string_to_data=float, create=None, stream=None, compare=None),
    PropertSpec(name=b"int", xsdname=b"integer", data_to_string=convert_from_int16, string_to_data=convert_to_int16, create=None, stream=None, compare=TCOPS,),
    PropertSpec(name=b"loadshape", xsdname=b"string", data_to_string=convert_from_loadshape, string_to_data=convert_to_loadshape, create=loadshape_create, stream=None, compare=TCOPS,),
    PropertSpec(name=b"method", xsdname=b"string", data_to_string=convert_from_method, string_to_data=convert_to_method, create=None, stream=None),
   # PropertSpec(name=b"obj", xsdname=b"string", data_to_string=convert_from_object, string_to_data=convert_to_object, create=None, stream=None, compare=TCOPB, get_part=Object.object_get_part),
    PropertSpec(name=b"randomvar", xsdname=b"string", data_to_string=convert_from_randomvar, string_to_data=convert_to_randomvar, create=randomvar_create, stream=None, compare=TCOPS, get_part=random_get_part),
    PropertSpec(name=b"set", xsdname=b"string", data_to_string=convert_from_set, string_to_data=convert_to_set, create=None, stream=None, compare=TCOPS,),
    PropertSpec(name=b"timestamp", xsdname=b"string", data_to_string=convert_from_timestamp_stub, string_to_data=convert_to_timestamp_stub, create=None, stream=None, compare=TCOPS, get_part=timestamp_get_part),
    PropertSpec(name=b"void", xsdname=b"string", data_to_string=convert_from_void, string_to_data=convert_to_void),
]

class Property:
    """
    The PROPERTY struct is represented by the Property class.
    The global global_property_types array from the original C++ code is simulated with a Python dictionary named
    property_type_handlers, which maps property types to their initialization handlers.
    The memset operation is not directly translated because Python's memory management doesn't
    require manual memory initialization.
    Instead, we assign a default value to the property's value attribute.
    The translated property_create function checks if the property type is valid and either calls a type-specific
    initialization function or assigns a default value.

    # Simulating the global_property_types array with a dictionary that maps property types to their handlers
        property_type_handlers = {
            # Example property types with 'create' methods and 'size' attributes
            'example_type_1': {'create': lambda addr: initialize_type_1(addr), 'size': 4},
            'example_type_2': {'create': lambda addr: initialize_type_2(addr), 'size': 8},
            # Add other property types as needed
        }

    # Example initialization functions for different types
        def initialize_type_1(addr):
            # Initialize a property of type 1
            addr.value = default_value_for_type_1

        def initialize_type_2(addr):
            # Initialize a property of type 2
            addr.value = default_value_for_type_2



    # Example usage
        prop = Property('example_type_1')
        result = property_create(prop)
        print(f"Property creation result: {result}, Property value: {prop.value}")
    """
    def __init__(self, property_type, value=None):
        self.property_type = property_type
        self.value = value


def property_check():
    # Check whether the properties as defined are mapping safely to memory
    # Returns 0 on failure, 1 on success
    status = 1
    return status


def property_size(prop: PropertyMap) -> int:
    # Get the size of a single instance of a property
    # Returns the size in bytes of a property
    if prop is not None and PropertyType.pt_first() < int(prop.property_type) < PropertyType.pt_last():
        return global_property_types[PropertyType.value(prop.property_type)].size
    else:
        return 0
    # return prop.size

def property_size_by_type(ptype):
    # Get the size of a single instance of a property by global_property_types
    # Returns the size in bytes of a property
    return global_property_types[ptype].size


# def property_create(prop, addr):
#     if prop and prop.ptype in global_property_types:
#         property_type = global_property_types[prop.ptype]
#         if property_type.size > 0:
#             property_type.create(addr)
#             return 1
#     return 0

def property_create(prop: PropertyMap, value=None):
    """
    Example usage
        prop = Property('example_type_1')
        result = property_create(prop, 20.0)
        print(f"Property creation result: {result}, Property value: {prop.value}")
    :param prop:
    :return:
    """
    result = 0
    if prop:
        ptype_index = -1
        for i, p in enumerate(global_property_types):
            if prop.property_type == p.name:
                ptype_index = i
        if ptype_index > 0:
            if global_property_types[ptype_index].create:
                # Call the create method and return the property
                return global_property_types[ptype_index].create(prop)
            if global_property_types[ptype_index].size > 0:
                if value:
                    prop.value = value
                else:
                    prop.value = 0
            result = 1
    return result


# def property_create(prop):
#     if prop and prop.global_property_types in property_type_handlers:
#         handler = property_type_handlers[prop.global_property_types]
#         if 'create' in handler:
#             handler['create'](prop)
#             return 1
#         else:
#             # If no specific create method, initialize with a default value based on 'size'
#             # Since Python handles memory management, we directly assign a default value
#             prop.value = 0  # or any other appropriate default value
#             return 1
#     else:
#         return 0

def property_minimum_buffersize(prop):
    # Get the minimum buffer size of a property
    size = global_property_types[prop.global_property_types].csize
    if size > 0:
        return size
    # TODO dynamic sizing
    return 0

def property_compare_op(ptype, opstr):
    # Get the comparison operation for a property global_property_types
    for n in range(len(global_property_types[ptype].compare)):
        if str(global_property_types[ptype].compare[n]) == opstr:
            return n
    return -1


def property_compare_basic(ptype, op, x, a, b, part):
    # Compare two properties of the same global_property_types
    if part is None and global_property_types[ptype].compare[op]["fn"] is not None:
        return global_property_types[ptype].compare[op]["fn"](x, a, b)
    elif global_property_types[ptype].get_part is not None:
        d = global_property_types[ptype].get_part(x, part)
        if math.isfinite(d):
            return a > b
        else:
            print(f"part {part} is not defined for global_property_types {global_property_types[ptype].name.decode('utf-8')}")
            return False
    else:
        print(
            f"property global_property_types '{global_property_types[ptype].name.decode('utf-8')}' does not support comparison operations or parts")
        return False



if __name__ == '__main__':

    print("Testing PropertyStruct")    # Example usage
    class ExampleObject:
        def __init__(self, my_property):
            self.my_property = my_property

    # Create an instance of PropertyStruct
    my_property_struct = PropertyStruct("my_property")
    # Create an example object with a specific property value
    example_obj = ExampleObject("Initial Value")
    # Use PropertyStruct to get and set property values
    print("Before:", my_property_struct.get_value(example_obj))  # Before: Initial Value
    my_property_struct.set_value(example_obj, "New Value")
    print("After:", my_property_struct.get_value(example_obj))  # After: New V

    print("Testing Propery class and property_create function")
    prop = Property('example_type_1')
    result = property_create(prop, -3.45)
    print(f"Property creation result: {result}, Property value: {prop.value}")
