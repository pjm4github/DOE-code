from enum import Enum
from typing import Any, Callable, List



class Keyword:
    """
    # Alternatively, using a list if ordering and direct linkage isn't necessary:
    keywords = [{'name': 'keyword1', 'value': 1}, {'name': 'keyword2', 'value': 2}]
    """
    def __init__(self, name, value, next_keyword=None):
        self.name = name
        self.value = value
        self.next = next_keyword  # Point to next Keyword if needed, otherwise stays None




class PropertyFlags(Enum):
    # Use an appropriate global_property_types for property flags
    PF_RECALC = 0x0001
    PF_CHARSET = 0x0002
    PF_EXTENDED = 0x0004
    PF_DEPRECATED = 0x8000
    PF_DEPRECATED_NONOTICE = 0x04000



class PropertyAccess(Enum):
    PA_N = 0x00 # no access permitted
    PA_R = 0x01  # read access
    PA_W = 0x02  # write access
    PA_S = 0x04  # save access
    PA_L = 0x08  # load access
    PA_H = 0x10  # hidden access
    PA_PUBLIC = 0x0F # PA_R | PA_W | PA_S | PA_L
    PA_REFERENCE = 0x0D  # PA_R | PA_S | PA_L
    PA_PROTECTED = 0x01  # PA_R
    PA_PRIVATE = 0x0C  # PA_S | PA_L
    PA_HIDDEN = 0x1F  # PA_PUBLIC | PA_H


    # PA_PUBLIC = _PA_R | _PA_W | _PA_S | _PA_L # _PA_PUBLIC    # property is public (readable, writable, saved, and loaded)
    # PA_REFERENCE = _PA_R | _PA_S | _PA_L # _PA_REFERENCE  # property is FYI (readable, saved, and loaded
    # PA_PROTECTED = _PA_R # _PA_PROTECTED   # property is semi-public (readable, but not saved or loaded)
    # PA_PRIVATE = _PA_S | _PA_L # _PA_PRIVATE  # property is non-public (not accessible, but saved and loaded)
    # PA_HIDDEN = _PA_R | _PA_W | _PA_S | _PA_L | _PA_H # _PA_HIDDEN  # property is not visible




class DelegatedType:
    """
    Example usage
        class ExampleDelegatedType(DelegatedType):
            def from_string(self, value):
                # Example conversion from string to data
                return int(value)  # Simplified conversion for demonstration

            def to_string(self, addr):
                # Example conversion from data to string
                return str(addr)  # Simplified conversion for demonstration

    Create an instance of the delegated type
        example_type = ExampleDelegatedType("ExampleType", None)

    Create a delegated value with this type
        delegated_value = DelegatedValue(None, example_type)

    Set data using the from_string conversion
        delegated_value.set_data_from_string("123")

    Get data as a string using the to_string conversion
        print(delegated_value.get_data_as_string())  # Should print "123"
    """
    def __init__(self, type_name, owner_class):
        self.type_name = type_name
        self.owner_class = owner_class

    def from_string(self, value):
        """
        Convert from string to the data type.
        This method should be overridden in subclasses to implement
        specific conversion logic.
        """
        raise NotImplementedError

    def to_string(self, addr):
        """
        Convert from the data type to string.
        This method should be overridden in subclasses to implement
        specific conversion logic.
        """
        raise NotImplementedError


class DelegatedValue:
    def __init__(self, data, dtype):
        self.data = data
        self.dtype = dtype

    def set_data_from_string(self, value):
        """
        Use the delegated type's from_string method to set data.
        """
        self.data = self.dtype.from_string(value)

    def get_data_as_string(self):
        """
        Use the delegated type's to_string method to get data as string.
        """
        return self.dtype.to_string(self.data)


delegated = DelegatedValue


class PropertyType(Enum):
    """
    Example usage
        print(PropertyType.PT_double.name, PropertyType.PT_double.value)
    """
    PT_any = 0
    PT_blob = 1
    PT_bool = 2  # the data is a true/ false value, implemented as a C++ bool
    PT_char1024 = 3  # the data is \p NULL -terminated string up to 1024 characters in length
    PT_char128 = 4
    PT_char256 = 5  # the data is \p NULL -terminated string up to 256 characters in length
    PT_char32 = 6  # the data is \p NULL -terminated string up to 32 characters in length
    PT_char64 = 7
    PT_char8 = 8  # the data is \p NULL -terminated string up to 8 characters in length
    PT_class = 9
    PT_complex = 10  # the data is a complex value
    PT_complex128 = 11
    PT_complex32 = 12
    PT_complex64 = 13
    PT_complex_array = 14  # the data is a fixed length complex[]
    PT_delegated = 15  # the data is delegated to a module for implementation
    PT_double = 16  # the data is a double-precision float
    PT_double_array = 17  # the data is a fixed length double[]
    PT_enduse = 18  # end use load data
    PT_enum = 19
    PT_enumeration = 20  # the data is an enumeration
    PT_float = 21  # Single-precision float
    PT_float32 = 22
    PT_float64 = 23
    PT_function = 24
    PT_hex = 25
    PT_int8 = 26
    PT_int16 = 27  # the data is a 16-bit integer
    PT_int32 = 28  # the data is a 32-bit integer
    PT_int64 = 29  # the data is a 64-bit integer
    PT_loadshape = 30  # Loadshapes are state machines driven by schedules
    PT_method = 31  # Method
    PT_object = 32  # the data is a pointer to a GridLAB object
    PT_object32 = 33
    PT_object64 = 34
    PT_oct = 35
    PT_random = 36  # Randomized number
    PT_real = 37  # Single or double precision float ~ allows double values to be overriden
    PT_real32 = 38
    PT_real64 = 39
    PT_ref = 40
    PT_set = 41  # the data is a set
    PT_string = 42
    PT_string32 = 43
    PT_timestamp = 44  # timestamp value
    PT_triple = 45  # triplet of doubles (not supported)
    PT_triplex = 46  # triplet of complexes (not supported)
    PT_type = 47
    PT_uint16 = 48
    PT_uint32 = 49
    PT_uint64 = 50
    PT_uint8 = 51
    PT_void = 52  # the global_property_types has no data
    PT_object_array = 53  # the data is a fixed length array of object pointers
    PT_ACCESS = -1  # used to specify property access rights
    PT_AGGREGATE = -2  # internal use only
    PT_DEPRECATED = -3  # used to flag a property that is deprecated
    PT_DESCRIPTION = -4  # used to provide helpful description of property
    PT_EXTEND = -5  # used to enlarge class size by the size of the current property being mapped
    PT_EXTENDBY = -6  # used to enlarge class size by the size provided in the next argument
    PT_FLAGS = -7  # used to indicate property flags next
    PT_HAS_NOTIFY = -8  # used to indicate that a notify function exists for the specified property
    PT_HAS_NOTIFY_OVERRIDE = -9  # as PT_HAS_NOTIFY, but instructs the core not to set the property to the value being set
    PT_INHERIT = -10  # used to indicate that properties from a parent class are to be published
    PT_KEYWORD = -11  # used to add an enum/ set keyword definition
    PT_NOTYPE = -12
    PT_SIZE = -13  # used to set up arrayed properties
    PT_UNITS = -14  # used to indicate that property has certain units (which following immediately as a string)

    def __int__(self):
        return self.value

    @classmethod
    def list_all(cls):
        return list(map(lambda c: c.value, cls))

    @classmethod
    def pt_last(cls):
        return max(cls.list_all())

    @classmethod
    def pt_first(cls):
        return min(cls.list_all())


class PropertyMap:
    # class PropertyMap:
    #     def __init__(self, oclass, name, global_property_types, size, width, access, unit, addr, delegation, keywords, description, flags, notify, method, notify_override):
    #         self.oclass = oclass
    #         self.name = name
    #         self.global_property_types = global_property_types
    #         self.size = size
    #         self.width = width
    #         self.access = access
    #         self.unit = unit
    #         self.addr = addr
    #         self.delegation = delegation
    #         self.keywords = keywords  # This could be a list of Keyword instances
    #         self.description = description
    #         self.flags = flags
    #         self.notify = notify  # This would be a function or method
    #         self.method = method  # This would be a function or method
    #         self.notify_override = notify_override

    # Define PROPERTY structure
    def __init__(self,
                 owner_class: 'DynamicClass' = None,
                 name: str = "",
                 property_type: PropertyType = None,  # Renamed because global_property_types is a keyword in Python
                 size: int = 0,
                 width: int = None,
                 access: PropertyAccess = None,
                 units: List = None,
                 addr: Callable = None,
                 delegation: DelegatedType = None,
                 keys: [None, List[Keyword]] = None,
                 description: str = "",
                 flags: PropertyFlags = 0,
                 notify: Callable = None,
                 method: Callable = None,
                 notify_override: bool = False,
                 value: Any = None):
        self.owner_class = owner_class  # class implementing the property
        self.name = name  # property name
        self.property_type = property_type   # property global_property_types
        self.size = size  # property array size
        self.width = width  # property byte size, copied from array in class.c
        self.access = access  # property access flags
        self.unit = units  # property unit, if any or None
        self.addr = addr  # DEPRICATED (use .value instead) property location, offset from OBJECT header; OBJECT header itself for methods
        self.delegation = delegation  # property delegation or None
        self.keywords = keys  # keyword list, if any or None (only for set and enumeration types)
        self.description = description  # description of property
        self.next = None   # next property in property list
        self.flags = flags  # property flags (e.g., PF_RECALC)
        self.notify = notify
        self.method = method  # method call, addr must be 0
        self.notify_override = notify_override
        self.value: Any = value

    def data_to_string(self):
        # This is a placeholder. Actual implementation would depend on property global_property_types.
        return str(self.value)
#
# # Define property_get_part function
# def property_get_part(self, prop: PROPERTY, part: str) -> float:
#     pass  # Replace with your implementation
#


class PropertyStruct:
    """
    # Example usage
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
        print("After:", my_property_struct.get_value(example_obj))  # After: New Value
    """
    def __init__(self, prop: PropertyMap, part: str=None):
        self.prop = prop  # Reference to a Property object or similar structure
        self.part = part  # Optional: Specific part or aspect of the property, if applicable

    def get_value(self, obj):
        """
        Retrieve the value of the property from a given object.
        This could involve accessing the property directly, calling a getter method,
        or performing any necessary computation or conversion.
        """
        # Example implementation, assuming 'prop' is the name of the property
        if hasattr(obj, self.prop):
            return getattr(obj, self.prop)
        else:
            raise AttributeError(f"Property {self.prop} not found in object.")

    def set_value(self, obj, value):
        """
        Set the value of the property for a given object.
        This could involve direct assignment, calling a setter method,
        or performing necessary validation or conversion.
        """
        # Example implementation, assuming 'prop' is the name of the property
        if hasattr(obj, self.prop):
            setattr(obj, self.prop, value)
        else:
            raise AttributeError(f"Property {self.prop} not found in object.")


class ExtendedProperty(PropertyMap):
    def __init__(self, name, property_type, units=None, default_value=None, keywords=None, description=""):
        super().__init__("", name, property_type, default_value)
        self.units = units
        self.flags: Enum = PropertyFlags.PF_EXTENDED
        self.keywords = keywords
        self.description = description

class PropertyTypeBase:
    def __init__(self):
        pass

    def create(self, addr: object):
        """
        Placeholder for the create method. In Python, 'addr' would likely be an object or key
        where the property value should be initialized.
        """
        raise NotImplementedError("Create method should be implemented by subclasses.")

    def stream(self, d: dict):
        raise NotImplementedError("stream method should be implemented by subclasses.")

    def compare(self, c: list):
        # Usually of this form: [{"op": "EQUAL", "str": "==", "fn": lambda x, y: x == y, "trinary": False}]
        raise NotImplementedError("compare method should be implemented by subclasses.")

    def get_part(self, ):
        raise NotImplementedError("")



class PropertSpec(PropertyTypeBase):
    """
    Function pointers are represented as methods within the PropertySpec class. These methods can be overridden in
    subclasses if different behavior is needed for different property types.

    The compare struct array is represented as a list of dictionaries or objects. Each entry can hold the comparison
    operation, its string representation, a lambda or function for the comparison, and a flag indicating if it's a
    trinary operation.

    For operations like data_to_string and string_to_data that operate on data, you would implement the corresponding
    logic within these methods, potentially handling different data types dynamically, given Python's global_property_types system.

    Example of how to populate the compare field
        compare_example = [
            {"op": "EQUAL", "str": "==", "fn": lambda x, y: x == y, "trinary": False},
            # Add other comparison operations as needed
        ]

        # Example instantiation of the PropertySpec class
        prop_spec_example = PropertySpec(
            name="ExampleType",
            xsdname="ExampleXSD",
            size=4,
            csize=0,  # Assuming property_minimum_buffersize() handles this case
            data_to_string=PropertySpec.data_to_string_method,
            string_to_data=PropertySpec.string_to_data_method,
            create=PropertySpec.create_method,
            stream=PropertySpec.stream_method,
            compare=compare_example,
            get_part=PropertySpec.get_part_method,
        )

    """
    # Define PropertSpec structure
    def __init__(self, name: bytes = None, xsdname: bytes = None,
                 data_to_string: Callable = None, string_to_data: Callable = None, create: Callable = None,
                 stream: Callable = None, compare: List['TCOperator'] = None, get_part: Callable = None):
        super().__init__()
        self.name = name
        self.xsdname = xsdname
        self.data_to_string = data_to_string if data_to_string else self.data_to_string_method
        self.string_to_data = string_to_data if string_to_data else self.string_to_data_method
        self.create = create if create else self.create_method
        self.stream = stream if stream else self.stream_method
        self.compare = compare if compare else \
            [{"op": "EQUAL", "str": "==", "fn": lambda x, y: x == y, "trinary": False}]
        self.get_part = get_part if get_part else self.get_part_method

    @staticmethod
    def property_getspec(ptype: PropertyType):
        return None  # global_property_types[int(ptype)]

    def data_to_string_method(self, data):
        # Placeholder for data_to_string function logic
        pass

    def string_to_data_method(self, string):
        # Placeholder for string_to_data function logic
        pass

    def create_method(self, name:object, value, ):
        # Placeholder for create function logic
        return name.property_type(value)

    def stream_method(self, file, mode, data):
        # Placeholder for stream function logic
        pass

    def get_part_method(self, name):
        # Placeholder for get_part function logic
        pass
