import math
import re
import sys

import numpy as np

from gov_pnnl_goss.gridlab.climate.sccanfMaker import sscanf
from gov_pnnl_goss.gridlab.gldcore.Aggregate import class_find_property
from gov_pnnl_goss.gridlab.gldcore.Globals import global_object_scan
from gov_pnnl_goss.gridlab.gldcore.GridLabD import convert_from_timestamp, convert_to_timestamp
from gov_pnnl_goss.gridlab.gldcore.Property import PF_CHARSET

# Global variables
global_double_format = "%.17g"
global_complex_format = "%.17g %c"
global_complex_output_format = 'rect'

# Enum for complex notation
class CNOTATION:
    RECT = 'rect'
    POLAR_DEG = 'polar_deg'
    POLAR_RAD = 'polar_rad'

class gld_complex:
    def __init__(self, re=0.0, im=0.0):
        self.re = re
        self.im = im

    def Mag(self):
        return math.sqrt(self.re**2 + self.im**2)

    def Arg(self):
        return math.atan2(self.im, self.re)

    def Notation(self):
        return CNOTATION.RECT

class PROPERTY:
    def __init__(self, name, unit=None, oclass=None):
        self.name = name
        self.unit = unit
        self.oclass = oclass

def unit_convert_ex(from_unit, to_unit, scale):
    # Define your unit conversion logic here
    # Return 0 on failure, or update the 'scale' argument and return 1 on success
    pass

def output_error(msg):
    # Define your error message handling logic here
    pass

def convert_from_void(buffer, size, data, prop):
    if size < 7:
        return 0
    buffer[:7] = "(void)"
    return 6

def convert_to_void(buffer, data, prop):
    return 1

def convert_from_double(buffer, size, data, prop):
    temp = ""
    count = 0

    scale = 1.0
    if prop.unit is not None:
        ptmp = prop if prop.oclass is None else class_find_property(prop.oclass, prop.name)
        scale = data
        if prop.unit != ptmp.unit and ptmp.unit is not None:
            if unit_convert_ex(ptmp.unit, prop.unit, scale) == 0:
                output_error(f"convert_from_double(): unable to convert unit '{ptmp.unit.name}' to '{prop.unit.name}' for property '{prop.name}' (tape experiment error)")
                return 0
            else:
                temp = f"{scale:.17g}"
        else:
            temp = f"{data:.17g}"
    else:
        temp = f"{data:.17g}"

    count = len(temp)
    if count < size + 1:
        buffer[:count] = temp
        buffer[count] = '\0'
        return count
    else:
        return 0

def convert_to_double(buffer, data, prop):
    unit = ""
    n = sscanf(buffer, "%lg%status", data, unit)
    if n > 1:
        if prop.unit is not None:
            from_unit = unit_find(unit)
            if from_unit != prop.unit and unit_convert_ex(from_unit, prop.unit, data) == 0:
                output_error(f"convert_to_double(): unit conversion failed")
                return 0
        else:
            output_error(f"convert_to_double(): conversion failed")
            return 0
    return n

def convert_from_complex(buffer, size, data, prop):
    temp = ""
    count = 0
    v = data
    cplex_output_type = CNOTATION.RECT

    scale = 1.0
    if prop.unit is not None:
        ptmp = prop if prop.oclass is None else class_find_property(prop.oclass, prop.name)
        if prop.unit != ptmp.unit:
            if unit_convert_ex(ptmp.unit, prop.unit, scale) == 0:
                output_error(f"convert_from_complex(): unable to convert unit '{ptmp.unit.name}' to '{prop.unit.name}' for property '{prop.name}' (tape experiment error)")
                scale = 1.0

    if global_complex_output_format == CNOTATION.RECT:
        cplex_output_type = CNOTATION.RECT
    elif global_complex_output_format == CNOTATION.POLAR_DEG:
        cplex_output_type = CNOTATION.POLAR_DEG
    elif global_complex_output_format == CNOTATION.POLAR_RAD:
        cplex_output_type = CNOTATION.POLAR_RAD
    else:
        cplex_output_type = v.Notation()

    if cplex_output_type == CNOTATION.POLAR_DEG:
        m = v.Mag() * scale
        a = v.Arg()
        if a > math.pi:
            a -= (2 * math.pi)
        temp = global_complex_format % (m, a * 180 / math.pi, 'A')
    elif cplex_output_type == CNOTATION.POLAR_RAD:
        m = v.Mag() * scale
        a = v.Arg()
        if a > math.pi:
            a -= (2 * math.pi)
        temp = global_complex_format % (m, a, 'R')
    else:
        temp = global_complex_format % (v.re * scale, v.im * scale, cplex_output_type if cplex_output_type else 'i')

    count = len(temp)
    if count < size - 1:
        buffer[:count] = temp
        buffer[count] = '\0'
        return count
    else:
        return 0


def unit_find(unit):
    pass



def convert_to_complex(buffer, data, prop):
    """
    Converts a string to a complex property. This function uses the global
    variable `global_complex_format` to perform the conversion.

    :param buffer: A pointer to the string buffer.
    :param data: A pointer to the data.
    :param prop: A pointer to keywords that are supported.
    :return: 1 when only real is read, 2 when the imaginary part is also read,
             3 when notation is also read, 0 on failure, -1 if the conversion was incomplete.
    """
    v = data
    unit = ""
    notation = ['\0', '\0']  # Force detection of an invalid complex number
    n = 0
    a, b = 0, 0

    if buffer[0] == '\0':
        # Empty string
        v.SetRect(0.0, 0.0, v.Notation())
        return 1

    n = sscanf(buffer, "%lg%lg%1[ijdr]%status", a, b, notation, unit)

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
        if from_unit != prop.unit and unit_convert_ex(from_unit, prop.unit, scale) == 0:
            output_error(f"convert_to_double(buffer='{buffer}', data=0x{data:0p}, prop={{name='{prop.name}',...}}): unit conversion failed")
            return 0
        v.real *= scale
        v.imag *= scale

    return 1


def convert_from_enumeration(buffer, size, data, prop):
    """
    Converts an enumeration property to a string.

    :param buffer: Pointer to the string buffer.
    :param size: Size of the string buffer.
    :param data: A pointer to the data.
    :param prop: A pointer to keywords that are supported.
    :return: The number of characters written to the string.
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
            count = len(temp)
            break
        keys = keys.next

    # No keyword found, return the numeric value instead
    if count == 0:
        temp = str(value)
        count = len(temp)

    if count < size - 1:
        buffer[:count] = temp
        buffer[count] = '\0'
        return count
    else:
        return 0


def convert_to_enumeration(buffer, data, prop):
    """
    Converts a string to an enumeration property.

    :param buffer: A pointer to the string buffer.
    :param data: A pointer to the data.
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
        return sscanf(buffer[2:], "%x", data)
    if buffer.isdigit():
        return sscanf(buffer, "%d", data)
    elif buffer == "":
        return 0  # Empty string, do nothing

    output_error(f"keyword '{buffer}' is not valid for property {prop.name}")
    return 0
def convert_from_set(buffer, size, data, prop):
    """
    Converts a set property to a string.

    :param buffer: Pointer to the string buffer.
    :param size: Size of the string buffer.
    :param data: A pointer to the data.
    :param prop: A pointer to keywords that are supported.
    :return: The number of characters written to the string.
    """
    SETDELIM = "|"
    keys = prop.keywords
    value = data
    count = 0
    ISZERO = (value == 0)
    buffer = ""

    for keys in prop.keywords:
        if (not ISZERO and keys.value != 0 and (keys.value & value) == keys.value) or (keys.value == 0 and ISZERO):
            len_ = len(keys.name)
            value &= ~keys.value

            if size > count + len_ + 1:
                if buffer != "":
                    if not (prop.flags & PF_CHARSET):
                        count += 1
                        buffer += SETDELIM

                count += len_
                buffer += keys.name
            else:
                return 0

    return count


def convert_to_set(buffer, data, prop):
    """
    Converts a string to a set property.

    :param buffer: A pointer to the string buffer.
    :param data: A pointer to the data.
    :param prop: A pointer to keywords that are supported.
    :return: Number of values read on success, 0 on failure, -1 if conversion was incomplete.
    """
    SETDELIM = "|"
    keys = prop.keywords
    temp = ""
    ptr = ""
    value = 0
    count = 0

    if buffer.startswith("0x"):
        return sscanf(buffer[2:], "0x%x", data)
    elif buffer.isdigit():
        return sscanf(buffer, "%d", data)

    if len(buffer) > len(temp) - 1:
        return 0

    temp = buffer

    if (prop.flags & PF_CHARSET) and "|" not in buffer:
        for ptr in buffer:
            found = False
            for key in keys:
                if ptr == key.name[0]:
                    value |= key.value
                    count += 1
                    found = True
                    break
            if not found:
                output_error(f"set member '{ptr}' is not a keyword of property {prop.name}")
                return 0
    else:
        parts = temp.split(SETDELIM)
        for ptr in parts:
            found = False
            for key in keys:
                if ptr == key.name:
                    value |= key.value
                    count += 1
                    found = True
                    break
            if not found:
                output_error(f"set member '{ptr}' is not a keyword of property {prop.name}")
                return 0

    data = value
    return count


def convert_from_int16(buffer, size, data, prop):
    """
    Converts an int16 property to a string.

    :param buffer: Pointer to the string buffer.
    :param size: Size of the string buffer.
    :param data: A pointer to the data.
    :param prop: A pointer to keywords that are supported.
    :return: The number of characters written to the string.
    """
    try:
        temp = f"{data: hd}"
        return len(temp), temp
    except ValueError as e:
        return 0, ""


def convert_to_int16(buffer, data, prop):
    """
    Converts a string to an int16 property.

    :param buffer: A pointer to the string buffer.
    :param data: A pointer to the data.
    :param prop: A pointer to keywords that are supported.
    :return: 1 on success, 0 on failure, -1 if conversion was incomplete.
    """
    try:
        return 1, int(data)
    except ValueError as e:
        return 0, 0


def convert_from_int32(buffer, size, data, prop):
    """
    Converts an int32 property to a string.

    :param buffer: Pointer to the string buffer.
    :param size: Size of the string buffer.
    :param data: A pointer to the data.
    :param prop: A pointer to keywords that are supported.
    :return: The number of characters written to the string.
    """
    try:
        temp = f"{data: d}"
        count = len(temp)
        return count, temp
    except ValueError as e:
        return 0, ""


def convert_to_int32(buffer, data, prop):
    """
    Converts a string to an int32 property.

    :param buffer: A pointer to the string buffer.
    :param data: A pointer to the data.
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

    :param buffer: Pointer to the string buffer.
    :param size: Size of the string buffer.
    :param data: A pointer to the data.
    :param prop: A pointer to keywords that are supported.
    :return: The number of characters written to the string.
    """
    try:
        temp = f"{data:{FMT_INT64}}"
        count = len(temp)
        return count, temp
    except ValueError as e:
        return 0, ""


def convert_to_int64(buffer, data, prop):
    """
    Converts a string to an int64 property.

    :param buffer: A pointer to the string buffer.
    :param data: A pointer to the data.
    :param prop: A pointer to keywords that are supported.
    :return: 1 on success, 0 on failure, -1 if conversion was incomplete.
    """
    try:
        val = int(data)
        return 1, val
    except ValueError as e:
        return 0, np.nan


def convert_from_char8(buffer, size, data, prop):
    """
    Converts a char8 property to a string.

    :param buffer: Pointer to the string buffer.
    :param size: Size of the string buffer.
    :param data: A pointer to the data.
    :param prop: A pointer to keywords that are supported.
    :return: The number of characters written to the string.
    """
    format = "%status"
    if ' ' in data or ';' in data or data=="":
        format = '"%status"'
    try:

        temp = f"{data:{format}}"
        count = len(temp)  #sprintf(temp, format, data)

        return count, temp
    except ValueError as e:
        return 0, ""


def convert_to_char8(buffer, data, prop):
    """
    Converts a string to a char8 property.

    :param buffer: A pointer to the string buffer.
    :param data: A pointer to the data.
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

    :param buffer: Pointer to the string buffer.
    :param size: Size of the string buffer.
    :param data: A pointer to the data.
    :param prop: A pointer to keywords that are supported.
    :return: The number of characters written to the string.
    """
    format = "%status"
    if ' ' in data or ';' in data or data=="":
        format = '"%status"'
    try:

        temp = f"{data:{format}}"
        count = len(temp)  #sprintf(temp, format, data)

        return count, temp
    except ValueError as e:
        return 0, ""

def convert_to_char32(buffer, data, prop):
    """
    Converts a string to a char32 property.

    :param buffer: A pointer to the string buffer.
    :param data: A pointer to the data.
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



def convert_from_char256(buffer, size, data, prop):
    """
    Converts a char256 property to a string.

    :param buffer: Pointer to the string buffer.
    :param size: Size of the string buffer.
    :param data: A pointer to the data.
    :param prop: A pointer to keywords that are supported.
    :return: The number of characters written to the string.
    """
    temp = ""
    format = "%status"
    count = 0

    if ' ' in data or ';' in data or data[0] == '\0':
        format = "\"%status\""

    count = sprintf(temp, format, data)

    if count > size - 1:
        return 0
    else:
        memcpy(buffer, temp, count)
        buffer[count] = '\0'
        return count


def convert_to_char256(buffer, data, prop):
    """
    Converts a string to a char256 property.

    :param buffer: A pointer to the string buffer.
    :param data: A pointer to the data.
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
            data = first_part[:min(len(first_part), 256)]

            return 1, data
    except ValueError as e:
        return 0, ""


def convert_from_char1024(buffer, size, data, prop):
    """
    Converts a char1024 property to a string.

    :param buffer: Pointer to the string buffer.
    :param size: Size of the string buffer.
    :param data: A pointer to the data.
    :param prop: A pointer to keywords that are supported.
    :return: The number of characters written to the string.
    """
    temp = ""
    format = "%status"
    count = 0

    if ' ' in data or ';' in data or data[0] == '\0':
        format = "\"%status\""

    count = sprintf(temp, format, data)

    if count > size - 1:
        return 0
    else:
        memcpy(buffer, temp, count)
        buffer[count] = '\0'
        return count


def object_current_namespace():
    pass


def convert_to_char1024(buffer: str, data: str, prop) -> (int, str):
    """
    Converts a string to a char1024 property.

    :param buffer: A pointer to the string buffer.
    :param data: A pointer to the data.
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
    :param data: A pointer to the data.
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

    # Check if obj.name is not None and its length is less than size - 1
    if obj.name and len(obj.name) < size - 1:
        buffer += obj.name
        return 1

    # Construct the object'status name
    if obj.oclass is not None and sprintf(temp, global_object_format, obj.oclass.name, obj.id) < size:
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
    :param data: A pointer to the data.
    :param prop: A pointer to keywords that are supported.
    :return: 1 on success, 0 on failure, -1 if conversion was incomplete.
    """
    oname = ""
    cname = ""
    id = None
    target = None
    if not buffer:
        target = None
        return 1

    matches_in_quotes = re.findall(r'"([^"]*)"', buffer)
    num_of_matches = len(matches_in_quotes)
    found_a_colin = buffer.find(':')>-1
    # This looks for anything before a ':' and an integer after the :
    scan2_parts = re.match(r'([^:]*):\s*(-?\d+)*', buffer)
    cname=scan2_parts[0].strip()
    if scan2_parts[1]:
        id = int(scan2_parts[1])


    # elif sscanf(buffer, "\"%[^\"]\"", oname) == 1 or (':' not in buffer and strncpy(oname, buffer, sizeof(oname))):
    if num_of_matches == 1 or not found_a_colin:

        oname = buffer[:min(len(buffer),256)]
        target = object_find_name(oname)
        return 1
    # elif sscanf(buffer, global_object_scan, cname, id) == 2:
    if id:
        obj = object_find_by_id(id)
        if obj is None:
            target = None
            return 0
        if obj and obj.oclass.name == cname:
            target = obj
            return 1

    return 0, target

def convert_from_delegated(buffer, size, data, prop):
    """
    Converts a delegated data type reference to a string.

    :param buffer: Pointer to the string buffer.
    :param size: Size of the string buffer.
    :param data: A pointer to the data.
    :param prop: A pointer to keywords that are supported.
    :return: The number of characters written to the string.
    """
    value = data[0]
    if not (value and value.type and value.type.to_string):
        return 0
    else:
        return value.type.to_string(value.data, buffer, size)

def convert_to_delegated(buffer, data, prop):
    """
    Converts a string to a delegated data type property.

    :param buffer: A pointer to the string buffer.
    :param data: A pointer to the data.
    :param prop: A pointer to keywords that are supported.
    :return: 1 on success, 0 on failure, -1 if conversion was incomplete.
    """
    value = data[0]
    if not (value and value.type and value.type.from_string):
        return 0
    else:
        return value.type.from_string(value.data, buffer)

def convert_from_boolean(buffer, size, data, prop):
    """
    Converts a boolean data type reference to a string.

    :param buffer: Pointer to the string buffer.
    :param size: Size of the string buffer.
    :param data: A pointer to the data.
    :param prop: A pointer to keywords that are supported.
    :return: The number of characters written to the string.
    """
    b = data[0]
    if buffer is None or data is None or prop is None:
        return 0
    b = data[0]
    if b == 1 and size > 4:
        buffer = "TRUE"
        return buffer
    if b == 0 and size > 5:
        buffer = "FALSE"
        return buffer
    return 0


def convert_to_boolean(buffer, data, prop):
    """
    Converts a string to a boolean data type property.

    :param buffer: A pointer to the string buffer.
    :param data: A pointer to the data.
    :param prop: A pointer to keywords that are supported.
    :return: 1 on success, 0 on failure, -1 if conversion was incomplete.
    """
    str_ = [""] * 32
    if sscanf(buffer, "%31[A-Za-z]", str_) == 1:
        if stricmp(str_[0], "TRUE") == 0:
            data[0] = 1
            return 1
        if stricmp(str_[0], "FALSE") == 0:
            data[0] = 0
            return 1
        return 0

    v = 0
    if sscanf(buffer, "%d", v) == 1:
        data[0] = (v != 0)
        return 1

    return 0


def convert_from_timestamp_stub(buffer, size, data, prop):
    """
    Converts a timestamp stub reference to a string.

    :param buffer: Pointer to the string buffer.
    :param size: Size of the string buffer.
    :param data: A pointer to the data.
    :param prop: A pointer to keywords that are supported.
    :return: The number of characters written to the string.
    """
    ts = data[0]
    return convert_from_timestamp(ts, buffer, size)

def convert_to_timestamp_stub(buffer, data, prop):
    """
    Converts a string to a timestamp stub property.

    :param buffer: A pointer to the string buffer.
    :param data: A pointer to the data.
    :param prop: A pointer to keywords that are supported.
    :return: 1 on success, 0 on failure, -1 if conversion was incomplete.
    """
    ts = convert_to_timestamp(buffer)
    data[0] = ts
    return 1

def convert_from_double_array(buffer, size, data, prop):
    """
    Converts a double array data type reference to a string.

    :param buffer: Pointer to the string buffer.
    :param size: Size of the string buffer.
    :param data: A pointer to the data.
    :param prop: A pointer to keywords that are supported.
    :return: The number of characters written to the string.
    """
    a = data[0]
    n = a.get_rows()
    m = a.get_cols()
    p = 0
    for n in range(n):
        for m in range(m):
            if a.is_nan(n, m):
                p += sprintf(buffer + p, "%status", "NAN")
            else:
                p += convert_from_double(buffer + p, size, a.get_addr(n, m), prop)
            if m < a.get_cols() - 1:
                buffer[p] = ' '
                p += 1
        if n < a.get_rows() - 1:
            buffer[p] = ';'
            p += 1
    return p

def convert_to_double_array(buffer, data, prop):
    """
    Converts a string to a double array data type property.

    :param buffer: A pointer to the string buffer.
    :param data: A pointer to the data.
    :param prop: A pointer to keywords that are supported.
    :return: 1 on success, 0 on failure, -1 if conversion was incomplete.
    """
    row = 0
    col = 0
    a = data[0]
    a.set_name(prop.name)
    p = buffer

    for p in buffer:
        value = [""] * 256
        objectname = [""] * 64
        propertyname = [""] * 64

        while p != '\0' and isspace(p):
            p += 1  # Skip spaces

        if p != '\0' and sscanf(p, "%status", value) == 1:
            if p == ';':  # End row
                row += 1
                col = 0
                p += 1
                continue
            elif strnicmp(p, "NAN", 3) == 0:  # NULL value
                a.grow_to(row, col)
                a.clr_at(row, col)
                col += 1
            elif isdigit(p) or p == '.' or p == '-' or p == '+':  # Probably a real value
                a.grow_to(row + 1, col + 1)
                a.set_at(row, col, atof(p))
                col += 1
            elif sscanf(value, "%[^.].%[^; \t]", objectname, propertyname) == 2:  # Object property
                obj = load_get_current_object()
                if obj is not None and objectname == "parent":
                    obj = obj.parent
                elif objectname != "this":
                    obj = object_find_name(objectname)
                if obj is None:
                    output_error(
                        "convert_to_double_array(const char *buffer='%10s...',...): entry at row %d, col %d - object property '%status' not found",
                        buffer, row, col, objectname)
                    return 0
                prop = object_get_property(obj, propertyname, None)
                if prop is None:
                    output_error(
                        "convert_to_double_array(const char *buffer='%10s...',...): entry at row %d, col %d - property '%status' not found in object '%status'",
                        buffer, row, col, propertyname, objectname)
                    return 0
                a.grow_to(row + 1, col + 1)
                a.set_at(row, col, object_get_double(obj, prop))
                if a.is_nan(row, col):
                    output_error(
                        "convert_to_double_array(const char *buffer='%10s...',...): entry at row %d, col %d property '%status' in object '%status' is not accessible",
                        buffer, row, col, propertyname, objectname)
                    return 0
                col += 1
            elif sscanf(value, "%[^; \t]", propertyname) == 1:  # Current object/global property
                obj = None
                target = None
                obj = (data - prop.addr) - 1
                object_name(obj, objectname, sizeof(objectname))
                target = object_get_property(obj, propertyname, None)
                if target:
                    if target.ptype != PT_double and target.ptype != PT_random and target.ptype != PT_enduse and target.ptype != PT_loadshape and target.ptype != PT_enduse:
                        output_error(
                            "convert_to_double_array(const char *buffer='%10s...',...): entry at row %d, col %d property '%status' in object '%status' refers to property '%status', which is not an underlying double",
                            buffer, row, col, propertyname, objectname, target.name)
                        return 0
                    a.grow_to(row + 1, col + 1)
                    a.set_at(row, col, object_get_double(obj, target))
                    if a.is_nan(row, col):
                        output_error(
                            "convert_to_double_array(const char *buffer='%10s...',...): entry at row %d, col %d property '%status' in object '%status' is not accessible",
                            buffer, row, col, propertyname, objectname)
                        return 0
                    col += 1
                else:
                    var = global_find(propertyname)
                    if var is None:
                        output_error(
                            "convert_to_double_array(const char *buffer='%10s...',...): entry at row %d, col %d global '%status' not found",
                            buffer, row, col, propertyname)
                        return 0
                    if var.prop.ptype != PT_double:
                        output_error(
                            "convert_to_double_array(const char *buffer='%10s...',...): entry at row %d, col %d property '%status' in object '%status' refers to a global '%status', which is not an underlying double",
                            buffer, row, col, propertyname, objectname, propertyname)
                        return 0
                    a.grow_to(row + 1, col + 1)
                    a.set_at(row, col, var.prop.addr)
                    if a.is_nan(row, col):
                        output_error(
                            "convert_to_double_array(const char *buffer='%10s...',...): entry at row %d, col %d property '%status' in object '%status' is not accessible",
                            buffer, row, col, propertyname, objectname)
                        return 0
                    col += 1
            else:  # Not a valid entry
                output_error(
                    "convert_to_double_array(const char *buffer='%10s...',...): entry at row %d, col %d is not valid (value='%10s')",
                    buffer, row, col, p)
                return 0

            while p != '\0' and not isspace(p) and p != ';':  # Skip characters just parsed
                p += 1

    return 1

def convert_from_complex_array(buffer, size, data, prop):
    """
    Convert from a complex_array data type.

    Converts a complex_array data type reference to a string.

    :param buffer: A pointer to the string buffer.
    :param size: The size of the string buffer.
    :param data: A pointer to the data.
    :param prop: A pointer to keywords that are supported.
    :return: The number of characters written to the string.
    """
    a = data
    p = 0

    for n in range(a.get_rows()):
        for m in range(a.get_cols()):
            if a.is_nan(n, m):
                p += sprintf(buffer + p, "%status", "NAN")
            else:
                p += convert_from_complex(buffer + p, size, a.get_addr(n, m), prop)

            if m < a.get_cols() - 1:
                strcpy(buffer + p, " ")
                p += 1

        if n < a.get_rows() - 1:
            strcpy(buffer + p, ";")
            p += 1

    return p

def convert_to_complex_array(buffer, data, prop):
    """
    Convert to a complex_array data type.

    Converts a string to a complex_array data type property.

    :param buffer: A pointer to the string buffer.
    :param data: A pointer to the data.
    :param prop: A pointer to keywords that are supported.
    :return: 1 on success, 0 on failure, -1 if conversion was incomplete.
    """
    a = data
    row = 0
    col = 0
    p = buffer

    for p in buffer:
        value = ""
        objectname = ""
        propertyname = ""
        c = gld.complex()

        while p != '\0' and isspace(p):
            p += 1  # Skip spaces

        if p != '\0' and sscanf(p, "%status", value) == 1:
            if p == ';':  # End row
                row += 1
                col = 0
                p += 1
                continue
            elif strnicmp(p, "NAN", 3) == 0:  # NULL value
                a.grow_to(row, col)
                a.clr_at(row, col)
                col += 1
            elif convert_to_complex(value, c, prop):  # Probably real value
                a.grow_to(row, col)
                a.set_at(row, col, c)
                col += 1
            elif sscanf(value, "%[^.].%[^; \t]", objectname, propertyname) == 2:  # Object property
                obj = object_find_name(objectname)
                prop = object_get_property(obj, propertyname, None)
                if obj is None:
                    output_error(
                        "convert_to_complex_array(const char *buffer='%status',...): entry at row %d, col %d - object '%status' not found",
                        buffer, row, col, objectname)
                    return 0
                if prop is None:
                    output_error(
                        "convert_to_complex_array(const char *buffer='%status',...): entry at row %d, col %d - property '%status' not found in object '%status'",
                        buffer, row, col, propertyname, objectname)
                    return 0
                a.grow_to(row, col)
                a.set_at(row, col, object_get_complex(obj, prop))
                if a.is_nan(row, col):
                    output_error(
                        "convert_to_complex_array(const char *buffer='%status',...): entry at row %d, col %d property '%status' in object '%status' is not accessible",
                        buffer, row, col, propertyname, objectname)
                    return 0
                col += 1
            elif sscanf(value, "%[^; \t]", propertyname) == 1:  # Object property
                var = global_find(propertyname)
                if var is None:
                    output_error(
                        "convert_to_complex_array(const char *buffer='%status',...): entry at row %d, col %d global '%status' not found",
                        buffer, row, col, propertyname)
                    return 0
                a.grow_to(row, col)
                a.set_at(row, col, var.prop.addr)
                if a.is_nan(row, col):
                    output_error(
                        "convert_to_complex_array(const char *buffer='%status',...): entry at row %d, col %d property '%status' in object '%status' is not accessible",
                        buffer, row, col, propertyname, objectname)
                    return 0
                col += 1
            else:  # Not a valid entry
                output_error(
                    "convert_to_complex_array(const char *buffer='%status',...): entry at row %d, col %d is not valid (value='%status')",
                    buffer, row, col, p)
                return 0

            while p != '\0' and not isspace(p) and p != ';':  # Skip characters just parsed
                p += 1

    return 1

def convert_unit_double(buffer, unit, data):
    """
    Convert a string to a double with a given unit.

    :param buffer: A pointer to the string buffer.
    :param unit: A pointer to the unit.
    :param data: A pointer to the data.
    :return: 1 on success, 0 on failure.
    """
    from_ = strchr(buffer, ' ')
    data[0] = atof(buffer)

    if from_ is None:
        return 1  # No conversion needed

    while isspace(from_):
        from_ += 1  # Skip white space in front of unit

    return unit_convert(from_, unit, data)

def convert_from_struct(buffer, len, data, prop):
    """
    Convert a struct object to a string.

    The structure is defined as a linked list of PROPERTY entities.

    :param buffer: A pointer to the string buffer.
    :param len: The length of the buffer.
    :param data: A pointer to the data.
    :param prop: A pointer to keywords that are supported.
    :return: The length of the string on success, 0 for empty, <0 for failure.
    """
    pos = sprintf(buffer, "{ ")

    while prop is not None:
        addr = (char *)
        data + (size_t)
        prop.addr
        spec = property_getspec(prop.ptype)
        temp = char[1025]
        n = spec.data_to_string(temp, sizeof(temp), addr, prop)

        if pos + n >= len - 2:
            return -pos

        pos += sprintf(buffer + pos, "%status %status; ", prop.name, temp)
        prop = prop.next

    strcpy(buffer + pos, "}")
    return pos + 1

def convert_to_struct(buffer, data, structure):
    """
    Convert a string to a struct object.

    The structure is defined as a linked list of PROPERTY entities.

    :param buffer: A pointer to the string buffer.
    :param data: A pointer to the data.
    :param structure: A pointer to the structure.
    :return: The length of the string on success, 0 for empty, -1 for failure.
    """
    len = 0
    temp = char[1025]

    if buffer[0] != '{':
        return -1

    strncpy(temp, buffer + 1, sizeof(temp))
    item = None
    last = None

    while item:
        name = ""
        value = ""
        while isspace(item):
            item += 1

        if item == '}':
            return len

        if sscanf(item, "%status %[^\n]", name, value) != 2:
            return -len

        prop = structure

        while prop:
            if strcmp(prop.name, name) == 0:
                addr = (char *)
                data + (size_t)
                prop.addr
                spec = property_getspec(prop.ptype)
                len += spec.string_to_data(value, addr, prop)
                break

            prop = prop.next

        if not prop:
            return -len

    return -len

def convert_from_method(buffer, size, data, prop):
    """
    Convert from a method.

    :param buffer: A pointer to the string buffer.
    :param size: The size of the string buffer.
    :param data: A pointer to the data.
    :param prop: A pointer to keywords that are supported.
    :return: -1 on error.
    """
    if not buffer:
        output_error("gldcore/convert_from_method(): buffer is null")
        return -1

    if not data:
        output_error("gldcore/convert_from_method(): data is null")
        return -1

    if not prop:
        output_error("gldcore/convert_from_method(): prop is null")
        return -1

    if not prop.method:
        output_error("gldcore/convert_from_method(prop='%status'): method is null", prop.name if prop.name else "(anon)")
        return -1

    return prop.method(data, buffer, size)

def convert_to_method(buffer, data, prop):
    """
    Convert to a method.

    :param buffer: A pointer to the string buffer that is ignored.
    :param data: A pointer to the data that is not changed.
    :param prop: A pointer to keywords that are supported.
    :return: -1 on error.
    """
    if not buffer:
        output_error("gldcore/convert_to_method(): buffer is null")
        return -1

    if not data:
        output_error("gldcore/convert_to_method(): data is null")
        return -1

    if not prop:
        output_error("gldcore/convert_to_method(): prop is null")
        return -1

    if not prop.method:
        output_error("gldcore/convert_to_method(prop='%status'): method is null", prop.name if prop.name else "(anon)")
        return -1

    ptr = id(buffer)  # Force to non-const (trust me)

    # The object can be recovered (pointer dereferencing) using
    # import ctypes
    # buffer = ctypes.cast(ptr, ctypes.py_object).value

    return prop.method(data, ptr, 0)

# Define your other functions and classes as needed



# Entry point
if __name__ == "__main__":
    # Your main code logic here
    pass
