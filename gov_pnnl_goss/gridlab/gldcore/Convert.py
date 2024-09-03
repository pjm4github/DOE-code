"""
This code is part of a module that handles the conversion between object properties and strings in
GridLAB-D, an open-source power distribution system simulation and analysis tool. The code defines a series of
functions for converting various data types to and from string representations. These conversions are used when
reading and writing property values from files, user input, or other external sources.

Here's a summary of the key components:

Includes: Standard headers for character type checks, mathematical operations, and standard I/O are included,
along with GridLAB-D specific headers for output handling, global definitions, conversion utilities,
object management, and loading utilities.
Type Definitions: A conditional compilation block checks for the presence of stdint.h and defines uint32 as an alias
for uint32_t if available, or unsigned int otherwise.
Conversion Functions: A set of functions (convert_from_* and convert_to_*) are defined for various data types
including void, double, complex, enumeration, set, int16, int32, int64, char8, char32, char256, char1024, object,
delegated, boolean, double_array, complex_array, and struct. Each function has a specific role:
convert_from_*: Converts a property value to a string representation.
convert_to_*: Parses a string and converts it to the appropriate property value.
Utility Functions: Additional utility functions are provided for tasks such as converting a string to a double with a
given unit (convert_unit_double) and converting between struct objects and strings (convert_from_struct and
convert_to_struct).

Method Conversion Functions: Two functions, convert_from_method and convert_to_method, are defined to handle
conversion for properties that use custom methods for their conversion logic.
Each conversion function takes parameters such as a buffer for the string representation, the size of the buffer,
The data being converted, and a pointer to the property metadata (PROPERTY). The functions return the
number of characters written to the buffer or an indication of success/failure of the conversion.

This module is essential for GridLAB-D's ability to interact with various data types through text-based interfaces,
such as configuration files (GLM files), command-line arguments, and interactive sessions. It ensures that property
values can be accurately represented as strings and that string inputs can be correctly interpreted as property
values within the simulation environment.
"""
import math
import re
from typing import List

import numpy as np

from gridlab.gldcore.Class import ClassRegistry
from gridlab.gldcore.Converted import timestamp

from gridlab.gldcore.Output import output_error

from gridlab.gldcore.PropertyHeader import PropertSpec, PropertyMap

from gridlab.gldcore.Unit import Unit, unit_find


# Global variables
global_double_format = "%.17g"
global_complex_format = "%.17g %c"
global_complex_output_format = 'rect'

# Enum for complex notation
class CNOTATION:
    RECT = 'rect'
    POLAR_DEG = 'polar_deg'
    POLAR_RAD = 'polar_rad'

# class gld_complex:
#     def __init__(self, re=0.0, im=0.0):
#         self.re = re
#         self.im = im
#
#     def Mag(self):
#         return math.sqrt(self.re**2 + self.im**2)
#
#     def Arg(self):
#         return math.atan2(self.im, self.re)
#
#     def Notation(self):
#         return CNOTATION.RECT

# class PROPERTY:
#     def __init__(self, name, unit=None, owner_class=None):
#         self.name = name
#         self.unit = unit
#         self.owner_class = owner_class
#
# def unit_convert_ex(from_unit, to_unit, scale):
#     # Define your unit conversion logic here
#     # Return 0 on failure, or update the 'scale' argument and return 1 on success
#     pass


def convert_from_void(data, prop):
    return "(void)"

def convert_to_void(buffer, data, prop):
    return 1

def convert_from_double(data, prop):
    temp = ""
    count = 0

    scale = 1.0
    if prop.unit is not None:
        ptmp = prop if prop.owner_class is None else ClassRegistry.find_property(prop.owner_class, prop.name)
        scale = data
        if prop.unit != ptmp.unit and ptmp.unit is not None:
            temp = f"{scale:.17g}"
        else:
            temp = f"{data:.17g}"
    else:
        temp = f"{data:.17g}"

    return temp

def convert_to_double(buffer, data, prop):
    unit = ""
    # n = sscanf(buffer, "%lg%s", data, unit)
    pattern = r"\s*([\d\.]+)\s+(\S+)"

    match = re.match(pattern, buffer)
    if match:
        data = float(match.group(1))  # Convert the first captured group to a float
        unit = match.group(2)  # The second captured group is the unit
        print(f"Data: {data}, Unit: '{unit}'")

        if prop.unit is not None:
            from_unit = unit_find(unit)
            if from_unit != prop.unit:
                output_error(f"convert_to_double(): unit conversion failed")
                return 0
        else:
            output_error(f"convert_to_double(): conversion failed")
            return 0
    return 2

def convert_from_complex(data: complex, prop):
    scale = 1.0
    if prop.unit is not None:
        ptmp = prop if prop.owner_class is None else ClassRegistry.find_property(prop.owner_class, prop.name)
    if global_complex_output_format == CNOTATION.RECT:
        cplex_output_type = CNOTATION.RECT
    elif global_complex_output_format == CNOTATION.POLAR_DEG:
        cplex_output_type = CNOTATION.POLAR_DEG
    elif global_complex_output_format == CNOTATION.POLAR_RAD:
        cplex_output_type = CNOTATION.POLAR_RAD
    else:
        cplex_output_type = CNOTATION.RECT

    if cplex_output_type == CNOTATION.POLAR_DEG:
        m = abs(data) * scale
        a = math.atan2(data.imag , data.real)
        if a > math.pi:
            a -= (2 * math.pi)
        temp = global_complex_format % (m, a * 180 / math.pi, 'A')
    elif cplex_output_type == CNOTATION.POLAR_RAD:
        m = abs(data) * scale
        a = math.atan2(data.imag , data.real)
        if a > math.pi:
            a -= (2 * math.pi)
        temp = global_complex_format % (m, a, 'R')
    else:
        temp = global_complex_format % (data.real * scale, data.imag * scale, cplex_output_type if cplex_output_type else 'i')

    return temp


def convert_to_complex(buffer, data, prop):
    """
    Converts a string to a complex property. This function uses the global
    variable `global_complex_format` to perform the conversion.

    :param buffer: A pointer to the string buffer.
    :param data: The data.
    :param prop: A pointer to keywords that are supported.
    :return: 1 when only real is read, 2 when the imaginary part is also read,
             3 when notation is also read, 0 on failure, -1 if the conversion was incomplete.
    """
    v = data
    unit = ""
    notation = ['\0', '\0']  # Force detection of an invalid complex number
    a, b = 0, 0

    if buffer[0] == '\0':
        # Empty string
        v.SetRect(0.0, 0.0, v.Notation())
        return 1

    buffer = "%lg%lg%1[ijdr]%s".format(a, b, notation, unit)
    n= len(buffer)
    if n == 1:  # Only real part
        v.SetRect(a, 0, v.Notation())
    elif n < 3 or notation[0] not in "ijdr":
        # Incomplete imaginary part or missing notation
        output_error(f"convert_to_complex('{buffer}', {prop.name}): complex number format is not valid")
        return 0

    # Appears ok
    elif notation[0] == 'A':  # Polar degrees
        v.SetPolar(a, b * math.pi / 180.0, v.Notation())
    elif notation[0] == 'R':  # Polar radians
        v.SetPolar(a, b, v.Notation())
    else:
        v.SetRect(a, b, v.Notation())  # Rectangular

    if v.Notation() == 'I':  # Only override notation when property is using 'I'
        v.Notation().set_notation(notation[0])

    if n > 3 and prop.unit is not None:  # Unit given and unit allowed
        from_unit = unit_find(unit)
        scale = 1.0
        if from_unit != prop.unit:
            output_error(f"convert_to_double(buffer='{buffer}', data=0x{data:0p}, prop={{name='{prop.name}',...}}): unit conversion failed")
            return 0
        v.real *= scale
        v.imag *= scale

    return 1


def convert_from_enumeration(data, prop):
    """
    Converts an enumeration property to a string.
    :param data: The data.
    :param prop: A pointer to keywords that are supported.
    :return: The string.
    """
    keys = prop.keywords
    count = 0
    temp = ""

    # Get the true value
    value = data

    # Process the keyword list, if any
    while keys is not None:
        # If the key value matches
        if keys.value == value:
            # Use the keyword
            temp = keys.name
            break
        keys = keys.next

    # No keyword found, return the numeric value instead
    if count == 0:
        temp = str(value)
    return temp

def convert_to_enumeration(buffer, data, prop):
    """
    Converts a string to an enumeration property.

    :param buffer: A pointer to the string buffer.
    :param data: The data.
    :param prop: A pointer to keywords that are supported.
    :return: 1 on success, 0 on failure, -1 if conversion was incomplete.
    """
    found = False
    keys = prop.keywords

    # Process the keyword list
    while keys is not None:
        if keys.name == buffer:
            data = keys.value
            found = True
            break
        keys = keys.next

    if found:
        return 1

    if buffer.startswith("0x"):
        data = int(buffer[2:], 16)
        return data
    if buffer.isdigit():
        return int(data)
    elif buffer == "":
        return 0  # Empty string, do nothing

    output_error(f"keyword '{buffer}' is not valid for property {prop.name}")
    return 0


def convert_from_int16(data):
    """
    Converts an int16 property to a string.

    :param data: The data.
    :return: The string.
    """
    return str(data)


def convert_to_int16(buffer, data, prop):
    """
    Converts a string to an int16 property.

    :param buffer: A pointer to the string buffer.
    :param data: The data.
    :param prop: A pointer to keywords that are supported.
    :return: 1 on success, 0 on failure, -1 if conversion was incomplete.
    """
    try:
        return 1, int(data)
    except ValueError as e:
        return 0, 0


def convert_from_int32(data):
    """
    Converts an int32 property to a string.

    :param data: The data.
    :return: The string.
    """
    return str(data)


def convert_to_int32(buffer, data, prop):
    """
    Converts a string to an int32 property.

    :param buffer: A pointer to the string buffer.
    :param data: The data.
    :param prop: A pointer to keywords that are supported.
    :return: 1 on success, 0 on failure, -1 if conversion was incomplete.
    """
    try:
        val = int(data)
        return 1, val
    except ValueError as e:
        return 0, np.nan

FMT_INT64 = "x"

def convert_from_int64(buffer, size, data, prop):
    """
    Converts an int64 property to a string.

    :param data: The data.
    :return: The string.
    """
    return str(data)

def convert_to_int64(buffer, data, prop):
    """
    Converts a string to an int64 property.

    :param buffer: A pointer to the string buffer.
    :param data: The data.
    :param prop: A pointer to keywords that are supported.
    :return: 1 on success, 0 on failure, -1 if conversion was incomplete.
    """
    try:
        val = int(data)
        return 1, val
    except ValueError as e:
        return 0, np.nan


def convert_from_char8(data):
    """
    Converts a char8 property to a string.
    :param data: The data.
    :return: The string.
    """
    return str(data)


def convert_to_char8(buffer, data, prop):
    """
    Converts a string to a char8 property.

    :param buffer: A pointer to the string buffer.
    :param data: The data.
    :param prop: A pointer to keywords that are supported.
    :return: 1 on success, 0 on failure, -1 if conversion was incomplete.
    """
    try:
        if buffer == "":
            data = ""
            return 1, data
        else:
            buffer = buffer.replace('"', ' ').strip()
            buffer_parts = buffer.split(' ')
            first_part = buffer_parts[0]
            data = first_part[:min(len(first_part), 8)]

            return 1, data
    except ValueError as e:
        return 0, ""


def convert_from_char32(buffer, size, data, prop):
    """
    Converts a char32 property to a string.
    :param data: The data.
    :return: The string.
    """
    return str(data)

def convert_to_char32(buffer, data, prop):
    """
    Converts a string to a char32 property.

    :param buffer: A pointer to the string buffer.
    :param data: The data.
    :param prop: A pointer to keywords that are supported.
    :return: 1 on success, 0 on failure, -1 if conversion was incomplete.
    """

    try:
        if buffer == "":
            data = ""
            return 1, data
        else:
            buffer = buffer.replace('"', ' ').strip()
            buffer_parts = buffer.split(' ')
            first_part = buffer_parts[0]
            data = first_part[:min(len(first_part), 32)]

            return 1, data
    except ValueError as e:
        return 0, ""



def convert_from_char256(size, data)->str:
    """
    Converts a char256 property to a string.
    :param data: The data.
    :return: The string.
    """
    return str(data)

def convert_to_char256(buffer):
    """
    Converts a string to a char256 property.

    :param buffer: A pointer to the string buffer.
    :return: 1 on success, 0 on failure, -1 if conversion was incomplete and the converted string
    """
    try:
        if buffer == "":
            data = ""
            return 1, data
        else:
            buffer = buffer.replace('"', ' ').strip()
            buffer_parts = buffer.split(' ')
            first_part = buffer_parts[0]
            data = first_part[:min(len(first_part), 256)]

            return 1, data
    except ValueError as e:
        return 0, ""


def convert_from_char1024(size, data):
    """
    Converts a char1024 property to a string.
    :param data: The data.
    :return: The string.
    """
    return str(data)


def object_current_namespace():
    pass


def convert_to_char1024(buffer: str, data: str, prop) -> (int, str):
    """
    Converts a string to a char1024 property.

    :param buffer: A pointer to the string buffer.
    :param data: The data.
    :param prop: A pointer to keywords that are supported.
    :return: 1 on success, 0 on failure, -1 if conversion was incomplete.
    """
    try:
        if buffer == "":
            data = ""
            return 1, data
        else:
            buffer = buffer.replace('"', ' ').strip()
            buffer_parts = buffer.split(' ')
            first_part = buffer_parts[0]
            data = first_part[:min(len(first_part), 1024)]

            return 1, data
    except ValueError as e:
        return 0, ""


def object_get_namespace(obj, buffer, size):
    pass


def convert_from_object(buffer, size, data, prop):
    """
    Converts an object reference to a string.

    :param buffer: Pointer to the string buffer.
    :param size: Size of the string buffer.
    :param data: The data.
    :param prop: A pointer to keywords that are supported.
    :return: The number of characters written to the string.
    """
    obj = data[0] if data else None
    temp = [0] * 256

    if obj is None:
        buffer[0] = '\0'
        return 1

    # Get the object'status namespace
    if object_current_namespace() != obj.space:
        if object_get_namespace(obj, buffer, size):
            buffer += "::"

    # Check if self.name is not None and its length is less than size - 1
    if obj.name and len(obj.name) < size - 1:
        buffer += obj.name
        return 1

    # Construct the object'status name
    global_object_format = "%s:%d"
    temp = global_object_format.format(obj.owner_class.name, obj.id)
    if obj.owner_class is not None and len(temp) < size:
        buffer += temp
    else:
        return 0

    return 1


def object_find_by_id(id):
    pass


def object_find_name(oname):
    pass


def convert_to_object(buffer, data, prop):
    """
    Converts a string to an object property.

    :param buffer: A pointer to the string buffer.
    :param data: The data.
    :param prop: A pointer to keywords that are supported.
    :return: 1 on success, 0 on failure, -1 if conversion was incomplete.
    """
    id = None
    target = None
    count = 0
    if not buffer:
        target = None
        count = 1
    else:
        matches_in_quotes = re.findall(r'"([^"]*)"', buffer)
        num_of_matches = len(matches_in_quotes)
        found_a_colin = buffer.find(':')>-1
        # This looks for anything before a ':' and an integer after the :
        scan2_parts = re.match(r'([^:]*):\s*(-?\d+)*', buffer)
        cname=scan2_parts[0].strip()
        if scan2_parts[1]:
            id = int(scan2_parts[1])


        if num_of_matches == 1 or not found_a_colin:

            oname = buffer[:min(len(buffer),256)]
            from gridlab.gldcore.Object import Object
            target = Object.object_find_name(data, oname)
            count = 1
        elif id:
            from gridlab.gldcore.Object import Object
            obj = Object.object_find_by_id(data, id)
            if obj is None:
                target = None
                count = 0
            elif obj and obj.owner_class.name == cname:
                target = obj
                count = 1

    return count, target

def convert_from_delegated(buffer, size, data, prop):
    """
    Converts a delegated data global_property_types reference to a string.

    :param buffer: Pointer to the string buffer.
    :param size: Size of the string buffer.
    :param data: The data.
    :param prop: A pointer to keywords that are supported.
    :return: The number of characters written to the string.
    """
    value = data[0]
    if not (value and value.global_property_types and value.global_property_types.to_string):
        return 0
    else:
        return value.global_property_types.to_string(value.data, buffer, size)

def convert_to_delegated(buffer, data, prop):
    """
    Converts a string to a delegated data global_property_types property.

    :param buffer: A pointer to the string buffer.
    :param data: The data.
    :param prop: A pointer to keywords that are supported.
    :return: 1 on success, 0 on failure, -1 if conversion was incomplete.
    """
    value = data[0]
    if not (value and value.global_property_types and value.global_property_types.from_string):
        return 0
    else:
        return value.global_property_types.from_string(value.data, buffer)

def convert_from_boolean(data):
    """
    Converts a boolean data global_property_types reference to a string.
    :param data: The data.
    :return: The string.
    """
    return "True" if data else "False"

def convert_to_boolean(buffer, data):
    """
    Converts a string to a boolean data global_property_types property.

    :param buffer: A pointer to the string buffer.
    :param data: The data.
    :param prop: A pointer to keywords that are supported.
    :return: 1 on success, 0 on failure, -1 if conversion was incomplete.
    """

    pattern = re.compile(r'^([A-Za-z]{1,31})')  # Compiles a pattern that matches 1 to 31 alphabetical characters
    match = pattern.match(buffer)

    # Initialize str variable to store the matched string
    str_var = ""

    if match:
        str_var = match.group(1)  # Extracts the matched portion of the string
        result = True
    else:
        result = False

    # Checking if the match was successful, equivalent to sscanf(...) == 1
    if str_var.upper() == "TRUE":
        result = True
    elif str_var.upper() == "FALSE":
        result = False

    else:
        try:
            # Attempt to convert the first part of the string to an integer
            v = int(buffer.split()[0])  # Splits the string by whitespace and converts the first part to an integer
            result = True
        except ValueError:
            # Handle the case where conversion to integer fails
            result = False
    return result

# Define timestamp handling functions
def convert_to_timestamp(item: [str, timestamp]):
    if type(item) == str:
        convert_to_timestamp_stub()
    elif type(item) == timestamp:
        convert_to_timestamp_stub()


def convert_to_timestamp_delta(string):
    # Implement based on your specific requirements
    pass


def convert_from_timestamp(timestamp):
    # Implement based on your specific requirements
    return str(timestamp)


def convert_from_deltatime_timestamp(timestamp):
    # Implement based on your specific requirements
    return str(timestamp)



def convert_from_timestamp_stub(data):
    """
    Converts a timestamp stub reference to a string.
    :param data: The data.
    :return: The number of characters written to the string.
    """
    ts = data[0]
    return convert_from_timestamp(ts)

def convert_to_timestamp_stub(buffer, data, prop):
    """
    Converts a string to a timestamp stub property.

    :param buffer: A pointer to the string buffer.
    :param data: The data.
    :param prop: A pointer to keywords that are supported.
    :return: 1 on success, 0 on failure, -1 if conversion was incomplete.
    """
    ts = convert_to_timestamp(buffer)
    data[0] = ts
    return 1


def convert_from_double_array(data):
    """
    Convert a 2D list of doubles to a string representation.
        # Example usage
        data = [
            [1.1, float('nan'), 2.2],
            [3.3, 4.4, float('nan')]
        ]

        result = convert_from_double_array(data)
        print(result)

    :param data: 2D list of doubles
    :return: The string representation of the array
    """
    return str(data)



def convert_to_double_array(buffer):
    """
    Converts a string to a double array data global_property_types property.

    :param buffer: A pointer to the string buffer.
    :return: 1, data on success, 0, None on failure, -1, None if conversion was incomplete.

    # Example usage
    buffer = "1.0 2.0; 3.0 NAN; 4.5 6.7"
    status, data = convert_to_double_array(buffer)
    if status > 0:
        print("Conversion successful:", data)
    else:
        print("Conversion failed or incomplete")
    """


    data = []  # This will hold the 2D array
    row = []
    parsing_success = True
    incomplete = False

    tokens = re.split(r'(;|\s+)', buffer.strip())  # Split by space or semicolon
    for token in tokens:
        if token == ';':
            if row:  # End of a row
                data.append(row)
                row = []
            else:
                incomplete = True
            continue
        elif token.strip() == '' or token.isspace():  # Skip empty tokens or spaces
            continue

        # Attempt to convert token to float or handle special cases
        try:
            if token.upper() == "NAN":
                row.append(float('nan'))
            else:
                row.append(float(token))
        except ValueError:
            parsing_success = False
            break

    if row:  # Add any remaining row
        data.append(row)

    if not parsing_success:
        return 0, None  # Failure
    elif incomplete or not data:
        return -1, None  # Incomplete or empty
    else:
        return 1, data  # Success, return data as well


def convert_from_complex_array(data):
    """
    Converts a 2D list of complex numbers to a string representation.
    This directly converts complex numbers to strings using Python's built-in str() function. If you have a
    custom format or specific handling for complex numbers (like the mentioned convert_from_complex),
    you should implement that logic in Python as well.

    The string representation of complex numbers in Python is in the form (real+imagj), which may differ from how you
    wish to represent them based on the convert_from_complex function's behavior in the original C code.

        # Example usage
        data = [
            [complex(1, 2), complex(3, 4)],
            [complex(5, 6), float('nan')]  # Python's complex global_property_types doesn't directly support NaN, this is for illustration
        ]
        result = convert_from_complex_array(data)
        print(result)


    :param data: 2D list of complex numbers

    The function returns the string representation of the complex array.
    Python manages string sizes dynamically, so the equivalent function focuses on producing the correct string output.

    :return: The string representation of the array
    """
    buffer = []
    for n, row in enumerate(data):
        row_str = []
        for m, val in enumerate(row):
            if val != val:  # Checking for NaN in complex numbers is not straightforward in Python; this is a placeholder
                row_str.append("NAN")
            else:
                # Assuming convert_from_complex is another function that converts a complex number to a string
                # Here, we directly convert the complex number to string using Python's str()
                row_str.append(str(val))
        buffer.append(' '.join(row_str))
    return ';'.join(buffer)


def convert_to_complex_array(buffer):
    """
    Converts a string to a 2D list of complex numbers.
        # Example usage
        buffer = "1+2j 3+4j; 5+6j NAN"
        status, data = convert_to_complex_array(buffer)
        if status > 0:
            print("Conversion successful:", data)
        else:
            print("Conversion failed or incomplete")

    :param buffer: String representation of a complex array
    :return: Tuple of (status, data) where status is 1 on success, 0 on failure, -1 if incomplete, and data is the complex array
    """
    data = []  # Will hold the 2D complex array
    row = []
    success = True

    # Split the input buffer into tokens, handling ';' as row delimiters
    tokens = buffer.split()
    for token in tokens:
        clean_token = token
        semicolon = token.strip().endswith(';')
        if semicolon:
            clean_token = token.replace(';','')
        # Attempt to convert token to complex or handle special cases
        try:
            if clean_token.upper() == "NAN":
                row.append(complex('nan'))
            else:
                # Direct conversion of numeric values to complex numbers
                row.append(complex(clean_token.replace('i', 'j')))  # Replace 'i' with 'j' if needed
        except ValueError:
            success = False
            break
        if semicolon:
            if row:
                data.append(row)
                row = []
    if row:  # Add the last row if any
        data.append(row)

    if not success:
        return 0, []  # Failure
    elif not data:
        return -1, []  # Incomplete
    else:
        return 1, data  # Success


def convert_unit_double(buffer, to_unit):
    """
    Convert a string to a double with a given unit.

        # Example usage
        buffer = "123.45 kg"
        unit = "lb"
        result = convert_unit_double(buffer, unit)
        if result == 1:
            print("Conversion successful")
        else:
            print("Conversion failed")


    :param buffer: The input string containing the numerical value and its unit.
    :param unit: The target unit for conversion.
    :return: 1 on success, 0 on failure.
    """
    parts = buffer.split()
    try:
        data = float(parts[0])
        # Assuming unit_convert is a function that converts `data` from its original unit (if specified) to `unit`
        # For simplicity, this example assumes no actual conversion logic is performed
        # Here you would call your unit conversion logic, e.g., unit_convert(from_unit=parts[1] if len(parts) > 1 else "", to_unit=unit, value=data)
        from_unit =  parts[1]
        converted_data = Unit.unit_convert(from_unit, to_unit, data)

        # Placeholder for unit conversion; assuming success for now
        conversion_success = True  # You would set this based on the actual conversion result

        return 1, converted_data  if conversion_success else 0, None
    except ValueError:
        # The string does not start with a convertible number
        return 0, None


def convert_from_struct(properties: PropertyMap):
    """
    Convert a list of PropertyMap objects to a string representation.

        # Example usage
        prop3 = PropertyMap("height", "5.9")
        prop2 = PropertyMap("age", "30", prop3)
        prop1 = PropertyMap("name", "John Doe", prop2)

        length, result = convert_from_struct(prop1)
        if length > 0:
            print(f"Conversion successful: {result} (Length: {length})")
        else:
            print("Conversion failed or empty")

    Assuming that the properties if a class object like this:
        class PropertyMap:
        def __init__(self, name, value, next_prop=None):
            self.name = name
            self.value = value
            self.next = next_prop

        def data_to_string(self):
            # This is a placeholder. Actual implementation would depend on property global_property_types.
            return str(self.value)


    :param properties: List of PropertyMap objects.
    :return: The length of the string on success, 0 for empty, <0 for failure.
    """
    if not properties:
        return 0  # Empty list

    buffer = ["{ "]
    prop = properties
    while prop:
        temp = prop.data_to_string()
        buffer.append(f"{prop.name} {temp}; ")
        prop = prop.next

    buffer.append("}")
    result = "".join(buffer)
    return result


def convert_to_struct(buffer, structure: List[dict]):
    """
        # Example usage
        structure = [
            PropertyMap("name", "string"),
            PropertyMap("age", "int"),
        ]

        buffer = "{ name John Doe; age 30; }"
        result = convert_to_struct(buffer, structure)
        if result > 0:
            print(f"Conversion successful: {result} characters processed.")
            for prop in structure:
                print(f"{prop.name}: {prop.value}")
        else:
            print("Conversion failed or empty")


    :param buffer:
    :param structure:
    :return: prop
    """
    prop = {}

    if not buffer.startswith('{'):
        return -1

    items = buffer[1:].split(';')
    len_value = 0
    for item in items:
        item = item.strip()
        if item.endswith('}'):
            item = item[:-1].strip()

        if not item:
            continue

        name_value = item.split(maxsplit=1)
        if len(name_value) != 2:
            return -len_value  # Assuming -len indicates parsing error with len characters processed

        prop = None
        name, value = name_value
        for d in structure:
            prop = d.get(name, None)
            if prop:
                break
        if prop is None:
            return -len_value  # No matching property found

        prop.value = float(value)
        len_value += len(value)

    return prop


def convert_from_method(buffer, data, prop:PropertyMap):
    """
    Convert from a method.

        # Example usage
        def example_method(obj, buffer, size):
            # Example method that would be associated with a property
            print(f"Called example_method with buffer='{buffer}' and size={size}")
            return 0  # Simulate success

        prop = PropertyMap("example", example_method)
        obj = Object()

        # Simulate calling these functions
        buffer = "test buffer"
        result = convert_from_method(buffer, obj, prop)
        print(f"convert_from_method returned {result}")

    :param buffer: A pointer to the string buffer.
    :param data: The data.
    :param prop: A pointer to keywords that are supported.
    :return: -1 on error.
    """

    if buffer is None:
        output_error("convert_from_method(): buffer is null")
        return -1
    if data is None:
        output_error("convert_from_method(): data is null")
        return -1
    if prop is None or prop.method is None:
        prop_name = prop.name if prop and prop.name else "(anon)"
        output_error(f"convert_from_method(prop='{prop_name}'): prop or method is null")
        return -1

    # Assuming prop.method is a callable that accepts buffer and size
    return prop.method(data, buffer, len(buffer))


def convert_to_method(buffer, data, prop):
    """
        # Example usage
        def example_method(obj, buffer, size):
            # Example method that would be associated with a property
            print(f"Called example_method with buffer='{buffer}' and size={size}")
            return 0  # Simulate success


        prop = PropertyMap("example", example_method)
        obj = Object()

        # Simulate calling these functions
        buffer = "test buffer"


        result = convert_to_method(buffer, obj, prop)
        print(f"convert_to_method returned {result}")



    :param buffer:
    :param data:
    :param prop:
    :return:
    """

    if buffer is None:
        output_error("convert_to_method(): buffer is null")
        return -1
    if data is None:
        output_error("convert_to_method(): data is null")
        return -1
    if prop is None or prop.method is None:
        prop_name = prop.name if prop and prop.name else "(anon)"
        output_error(f"convert_to_method(prop='{prop_name}'): prop or method is null")
        return -1

    # Assuming prop.method is a callable that can handle buffer being None or empty
    return prop.method(data, buffer, 0)


def convert_from_enduse(buffer, data, prop):
    pass

def convert_to_enduse(buffer, data, prop):
    pass

def enduse_create(buffer, data, prop):
    pass

def convert_from_loadshape(buffer, data, prop):
    pass

def convert_to_loadshape(buffer, data, prop):
    pass

def loadshape_create(buffer, data, prop):
    pass

def convert_from_randomvar(buffer, data, prop):
    pass

def convert_to_randomvar(buffer, data, prop):
    pass

def randomvar_create(buffer, data, prop):
    pass

def convert_to_enduse(buffer, data, prop):
    pass


# Define your other functions and classes as needed



# Entry point
if __name__ == "__main__":
    # Your main code logic here
    pass
