from io import BytesIO

import numpy as np
import copy
from enum import Enum
from typing import Union, List
import math
import ctypes
from ctypes import Structure, c_void_p, c_char_p, c_int, c_uint, c_double, c_float
# import Exception



# Define constants
QNAN = math.nan

# Define integer types
int8 = ctypes.c_int8
int16 = ctypes.c_int16
int32 = ctypes.c_int32
uint16 = ctypes.c_uint16
uint32 = ctypes.c_uint32
uint64 = ctypes.c_uint64


class Charbuf:
    def __init__(self, size):
        self.buffer = bytearray(size)

    def get_size(self):
        return len(self.buffer)

    def get_length(self):
        return len(self.buffer.decode('utf-8'))

    def get_string(self):
        return self.buffer.decode('utf-8')

    def erase(self):
        self.buffer = bytearray(len(self.buffer))

    def copy_to(self, s):
        if s is not None:
            s[:len(self.buffer)] = self.buffer

    def copy_from(self, s):
        if s is not None:
            self.buffer[:len(s)] = s.encode('utf-8')

    def __str__(self):
        return self.buffer.decode('utf-8')

    def __eq__(self, other):
        return str(self) == other

    def __lt__(self, other):
        return str(self) < other

    def __gt__(self, other):
        return str(self) > other

    def __le__(self, other):
        return str(self) <= other

    def __ge__(self, other):
        return str(self) >= other

    def find(self, c):
        return self.buffer.find(bytes(c, 'utf-8'))

    def find_str(self, s):
        return self.buffer.find(bytes(s, 'utf-8'))

    def find_rev(self, c):
        return self.buffer.rfind(bytes(c, 'utf-8'))

    def tokenize(self, delim):
        return str(self).split(delim)

    def format(self, fmt, *args):
        formatted = fmt % args
        self.copy_from(formatted)
        return len(formatted)

    def vformat(self, fmt, args):
        formatted = fmt % args
        self.copy_from(formatted)
        return len(formatted)



#
# class Char2048(Charbuf):
#     def __init__(self):
#         super().__init__(2049)
#
#
# class Char1024(Charbuf):
#     def __init__(self):
#         super().__init__(1025)
#
#
# class Char256(Charbuf):
#     def __init__(self):
#         super().__init__(257)
#
#
# class Char128(Charbuf):
#     def __init__(self):
#         super().__init__(129)
#
#
# class Char64(Charbuf):
#     def __init__(self):
#         super().__init__(65)
#
#
# class Char32(Charbuf):
#     def __init__(self):
#         super().__init__(33)
#
#
# class Char8(Charbuf):
#     def __init__(self):
#         super().__init__(9)

#
# class DoubleVector:
#
#     def __init__(self, data):
#         self.data = data
#
#     def __getitem__(self, index):
#         if self.data[index] is None:
#             self.data[index] = ctypes.c_double()
#         return self.data[index].value
#
#     def __setitem__(self, index, value):
#         if self.data[index] is None:
#             self.data[index] = ctypes.c_double(value)
#         else:
#             self.data[index].value = value


# class DoubleArray:
#     def __init__(self, rows=0, cols=0, data=None):
#         self.n = rows
#         self.m = cols
#         self.max_val = 0
#         self.refs = ctypes.pointer(ctypes.c_uint())
#         self.x = None
#         self.f = None
#         self.name = None
#
#         if rows > 0:
#             self.grow_to(rows, cols)
#
#         if data:
#             for r in range(rows):
#                 for c in range(cols):
#                     self.set_at(r, c, data[r][c])
#
#     def exception(self, msg, *args):
#         pass
#
#     def set_flag(self, r, c, b):
#         pass
#
#     def clr_flag(self, r, c, b):
#         pass
#
#     def tst_flag(self, r, c, b):
#         pass
#
#     def my(self, r, c):
#         pass
#
#     def set_name(self, v):
#         pass
#
#     def get_name(self):
#         pass
#
#     def get_rows(self):
#         pass
#
#     def get_cols(self):
#         pass
#
#     def get_max(self):
#         pass
#
#     def set_name(self, v):
#         pass
#
#     def set_rows(self, i):
#         pass
#
#     def set_cols(self, i):
#         pass
#
#     def set_max(self, size):
#         pass
#
#     def grow_to(self, r, c):
#         pass
#
#     def is_valid(self, r, c):
#         pass
#
#     def is_nan(self, r, c):
#         pass
#
#     def is_empty(self):
#         pass
#
#     def clr_at(self, r, c):
#         pass
#
#     def copy_matrix(self):
#         pass
#
#     def free_matrix(self, y):
#         pass



class FUNCTIONADDR:
    def __init__(self):
        self.func_ptr = None
        self.args = None

class FUNCTIONNAME(str):
    def __init__(self, value):
        super().__init__(value)

# # Valid GridLAB data types
# class charbuf:
#     def __init__(self, size):
#         self.buffer = ctypes.create_string_buffer(size)
#
#     def get_size(self):
#         return len(self.buffer)
#
#     def get_length(self):
#         return len(self.buffer)
#
#     def get_string(self):
#         return self.buffer.value
#
#     def erase(self):
#         self.buffer = ctypes.create_string_buffer(len(self.buffer))
#
#     def copy_to(self, s):
#         if s:
#             s[:len(self.buffer)] = self.buffer
#         return s
#
#     def copy_from(self, s):
#         if s:
#             self.buffer[:len(s)] = s
#         return self.buffer
#
#     def __str__(self):
#         return self.buffer.value
#
#     def __len__(self):
#         return len(self.buffer)
#
#     def __eq__(self, s):
#         return self.buffer.value == s
#
#     def __lt__(self, s):
#         return self.buffer.value < s
#
#     def __gt__(self, s):
#         return self.buffer.value > s
#
#     def __le__(self, s):
#         return self.buffer.value <= s
#
#     def __ge__(self, s):
#         return self.buffer.value >= s
#
#     def find(self, c):
#         return self.buffer.value.find(c)
#
#     def findrev(self, c):
#         return self.buffer.value.rfind(c)
#
#     def token(self, from_, delim, context):
#         return self.buffer.value
#
#     def format(self, fmt, *args):
#         return len(self.buffer.value)
#
#     def vformat(self, fmt, ptr):
#         return len(self.buffer.value)
#
#     def __getitem__(self, index):
#         return self.buffer[index]
#
#     def __setitem__(self, index, value):
#         self.buffer[index] = value
#
#     def __iter__(self):
#         return iter(self.buffer)
#
# class char2048(charbuf):
#     def __init__(self):
#         super().__init__(2049)
#
# class char1024(charbuf):
#     def __init__(self):
#         super().__init__(1025)
#
# class char256(charbuf):
#     def __init__(self):
#         super().__init__(257)
#
# class char128(charbuf):
#     def __init__(self):
#         super().__init__(129)
#
# class char64(charbuf):
#     def __init__(self):
#         super().__init__(65)
#
# class char32(charbuf):
#     def __init__(self):
#         super().__init__(33)
#
# class char8(charbuf):
#     def __init__(self):
#         super().__init__(9)

# set = ctypes.c_uint64
# enumeration = ctypes.c_uint32
# object = ctypes.POINTER(CLASS)
# triplet = (ctypes.c_double * 3)
# triplex = (ctypes.c_double * 3)

BYREF = 0x01

# class double_vector:
#     def __init__(self, data):
#         self.data = data
#
#     def __getitem__(self, index):
#         if self.data[index] is None:
#             self.data[index] = ctypes.c_double()
#         return self.data[index].value
#
#     def __setitem__(self, index, value):
#         if self.data[index] is None:
#             self.data[index] = ctypes.c_double(value)
#         else:
#             self.data[index].value = value

# class double_array:
#     def __init__(self, rows=0, cols=0, data=None):
#         self.n = rows
#         self.m = cols
#         self.max_val = 0
#         self.refs = ctypes.pointer(ctypes.c_uint())
#         self.x = None
#         self.f = None
#         self.name = None
#
#         if rows > 0:
#             self.grow_to(rows, cols)
#
#         if data:
#             for r in range(rows):
#                 for c in range(cols):
#                     self.set_at(r, c, data[r][c])
#
#     def exception(self, msg, *args):
#         pass
#
#     def set_flag(self, r, c, b):
#         pass
#
#     def clr_flag(self, r, c, b):
#         pass
#
#     def tst_flag(self, r, c, b):
#         pass
#
#     def my(self, r, c):
#         pass
#
#     def set_name(self, v):
#         pass
#
#     def get_name(self):
#         pass
#
#     def get_rows(self):
#         pass
#
#     def get_cols(self):
#         pass
#
#     def get_max(self):
#         pass
#
#     def set_rows(self, i):
#         pass
#
#     def set_cols(self, i):
#         pass
#
#     def set_max(self, size):
#         pass
#
#     def grow_to(self, r, c):
#         pass
#
#     def is_valid(self, r, c):
#         pass
#
#     def is_nan(self, r, c):
#         pass
#
#     def is_empty(self):
#         pass
#
#     def clr_at(self, r, c):
#         pass
#
#     def copy_matrix(self):
#         pass
#
#     def free_matrix(self, y):
#         pass
#
#     def copy_vector(self, y=None):
#         pass
#
#     def transpose(self):
#         pass
#
#     def get_addr(self, r, c):
#         pass
#
#     def get_at(self, r, c):
#         pass
#
#     def set_at(self, r, c, v):
#         pass
#
#
#     def set_ident(self):
#         pass
#
#     def dump(self, r1=0, r2=-1, c1=0, c2=-1):
#         pass
#
#     def copy_name(self, v):
#         pass
#
#     def operator(self, y):
#         pass



#
# class ComplexVector:
#     def __init__(self, x):
#         self.x = x
#
#     def __getitem__(self, key):
#         if isinstance(key, int):
#             if self.x[key] is None:
#                 self.x[key] = 0j
#             return self.x[key]
#         else:
#             raise TypeError("Invalid key type")
#
#     def __setitem__(self, key, value):
#         if isinstance(key, int):
#             if isinstance(value, complex):
#                 self.x[key] = value
#             else:
#                 raise TypeError("Invalid value type")
#         else:
#             raise TypeError("Invalid key type")
#
#     def __str__(self):
#         return f"ComplexVector with {len(self.x)} elements"


class ComplexArray:
    def __init__(self, rows=0, cols=0, data=None):
        self.n = rows
        self.m = cols
        self.max_val = 0
        self.refs = [0]
        self.x = None
        self.f = None
        self.name = None

        if rows > 0:
            self.grow_to(rows, cols)

        if data is not None:
            for r in range(rows):
                for c in range(cols):
                    self.set_at(r, c, data[r][c] if data is not None else 0.0)

    def copy_name(self, v):
        self.name = v

    def get_name(self):
        return self.name

    def get_rows(self):
        return self.n

    def get_cols(self):
        return self.m

    def get_max(self):
        return self.max_val

    def set_name(self, v):
        self.name = v

    def set_rows(self, i):
        self.n = i

    def set_cols(self, i):
        self.m = i

    def set_max(self, size):
        if size <= self.max_val:
            raise ValueError(".set_max(%u): cannot shrink complex_array" % size)

        z = [None] * size

        for r in range(self.max_val):
            if self.x[r] is not None:
                y = [None] * size
                y[:self.m] = self.x[r]
                z[r] = y

        z[self.max_val:size] = [None] * (size - self.max_val)

        if self.f is not None:
            nf = self.f[:self.max_val]
            nf[self.max_val:size] = [0] * (size - self.max_val)
        else:
            nf = [0] * size

        self.x = z
        self.f = nf
        self.max_val = size

    def grow_to(self, r, c):
        s = max(1, self.max_val)
        while c >= s or r >= s:
            s *= 2
        if s > self.max_val:
            self.set_max(s)

        while self.n < r:
            if self.x[self.n] is None:
                self.x[self.n] = [None] * self.max_val
            self.n += 1

        if self.m < c:
            for i in range(self.n):
                y = [None] * c
                if self.x[i] is not None:
                    y[:self.m] = self.x[i]
                self.x[i] = y
            self.m = c

    def check_valid(self, r, c=None):
        if not c:
            c = r
            r = 0
        if not self.is_valid(r, c):
            raise ValueError(".check_value(%u,%u): invalid (r,c)" % (r, c))


    def is_valid(self, r, c=None):
        if not c:
            c = r
            r = 0
        return r < self.n and c < self.m


    def is_nan(self, r, c=None):
        if not c:
            c = r
            r = 0
            return self.is_nan(0, c)
        else:
            self.check_valid(r, c)
            return not ((self.x[r][c] is not None) and
                        isinstance(self.x[r][c], complex) and
                        (self.x[r][c] is not None) and
                        (self.x[r][c].real is not None) and
                        (self.x[r][c].imag is not None)
                        for c in range(self.m))


    def is_empty(self):
        return self.n == 0 and self.m == 0

    def clr_at(self, r, c=None):
        if not c:
            c = r
            r = 0
        self.check_valid(r, c)
        if self.f[r * self.m + c] & 1:
            self.x[r][c] = None

    def copy_matrix(self):
        y = [[None] * self.m for _ in range(self.n)]
        for r in range(self.n):
            for c in range(self.m):
                y[r][c] = self.x[r][c] if self.x[r][c] is not None else 0.0 + 0.0j
        return y

    def free_matrix(self, y):
        for r in range(self.n):
            del y[r]
        del y

    def copy_vector(self, y=None):
        if y is None:
            y = [None] * (self.n * self.m)
        i = 0
        for r in range(self.n):
            for c in range(self.m):
                y[i] = self.x[r][c] if self.x[r][c] is not None else 0.0 + 0.0j
                i += 1
        return y

    def transpose(self):
        xt = [[None] * self.n for _ in range(self.m)]
        for i in range(self.m):
            for j in range(self.n):
                xt[i][j] = self.x[j][i]
        self.x = xt
        self.n, self.m = self.m, self.n

    def get_addr(self, r, c=None):
        if not c:
            c = r
            r = 0
        return self.x[r][c] if self.is_valid(r, c) else None

    def get_at(self, r, c=None):
        if not c:
            c = r
            r = 0
        if self.is_nan(r, c):
            return complex(float('nan'), float('nan'))
        return self.x[r][c]

    def set_at(self, r, c, v=None):
        if not v:
            v = c
            c = r
            r = 0

        self.check_valid(r, c)
        if self.x[r][c] is None:
            self.x[r][c] = v
        else:
            self.x[r][c] = v

    def set_ident(self):
        for r in range(self.n):
            for c in range(self.m):
                self.x[r][c] = 1.0 + 0.0j if r == c else 0.0 + 0.0j

    def dump(self, r1=0, r2=None, c1=0, c2=None):
        if r2 is None:
            r2 = self.n - 1
        if c2 is None:
            c2 = self.m - 1

        if r2 < r1 or c2 < c1:
            raise ValueError(".dump(%u,%u,%u,%u): invalid (r,c)" % (r1, r2, c1, c2))

        print("complex_array %s = {" % (self.name if self.name else "unnamed"))
        for r in range(r1, r2 + 1):
            for c in range(c1, c2 + 1):
                print(" %8g%+8gi" % (self.x[r][c].real, self.x[r][c].imag), end="")
            print()
        print(" }")

    def __setitem__(self, key, value):
        if isinstance(key, int):
            self.x[0][key] = value
        elif isinstance(key, tuple):
            r, c = key
            self.x[r][c] = value
        else:
            raise ValueError("Invalid key")

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.x[0][key]
        elif isinstance(key, tuple):
            r, c = key
            return self.x[r][c]
        else:
            raise ValueError("Invalid key")

    def __add__(self, y):
        if self.get_rows() != y.get_rows() or self.get_cols() != y.get_cols():
            raise ValueError("+%s: size mismatch" % y.get_name())

        a = ComplexArray(self.get_rows(), self.get_cols())
        a.set_name("(?+?)")

        for r in range(self.get_rows()):
            for c in range(y.get_cols()):
                a[r][c] = self.get(r, c) + y[r][c]

        return a

    def __sub__(self, y):
        if self.get_rows() != y.get_rows() or self.get_cols() != y.get_cols():
            raise ValueError("-%s: size mismatch" % y.get_name())

        a = ComplexArray(self.get_rows(), self.get_cols())
        a.set_name("(?-?)")

        for r in range(self.get_rows()):
            for c in range(y.get_cols()):
                a[r][c] = self.get(r, c) - y[r][c]

        return a

    def __mul__(self, y):
        if self.get_cols() != y.get_rows():
            raise ValueError("*%s: size mismatch" % y.get_name())

        a = ComplexArray(self.get_rows(), y.get_cols())
        a.set_name("(?*?)")

        for r in range(self.get_rows()):
            for c in range(y.get_cols()):
                b = 0
                for k in range(self.get_cols()):
                    b += self.get(r, k) * y[k][c]
                a[r][c] = b

        return a

    def extract_row(self, r):
        if r >= self.get_rows():
            raise ValueError("Row index out of bounds")

        y = [0] * self.get_cols()
        for c in range(self.get_cols()):
            y[c] = self.get(r, c)

        return y

    def extract_col(self, c):
        if c >= self.get_cols():
            raise ValueError("Column index out of bounds")

        y = [0] * self.get_rows()
        for r in range(self.get_rows()):
            y[r] = self.get(r, c)

        return y



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



# Define the real type based on the REAL4 preprocessor directive
REAL4 = True  # Change this to False for double precision
real = float if REAL4 else None  # double

# Define property access rights flags
_PA_N = 0x00
_PA_R = 0x01
_PA_W = 0x02
_PA_S = 0x04
_PA_L = 0x08
_PA_H = 0x10
_PA_PUBLIC = _PA_R | _PA_W | _PA_S | _PA_L
_PA_REFERENCE = _PA_R | _PA_S | _PA_L
_PA_PROTECTED = _PA_R
_PA_PRIVATE = _PA_S | _PA_L
_PA_HIDDEN = _PA_PUBLIC | _PA_H


class PROPERTYACCESS(Enum):
    PA_N = 0x00
    PA_R = 0x01
    PA_W = 0x02
    PA_S = 0x04
    PA_L = 0x08
    PA_H = 0x10
    PA_PUBLIC = _PA_PUBLIC
    PA_REFERENCE = _PA_REFERENCE
    PA_PROTECTED = _PA_PROTECTED
    PA_PRIVATE = _PA_PRIVATE
    PA_HIDDEN = _PA_HIDDEN


# PROPERTYADDR = int  # You can use an appropriate type for property addresses
class PROPERTYADDR:
    def __init__(self, value):
        self.value = value


class PROPERTYTYPE(Enum):
    PT_void = 0
    PT_double = 1
    PT_complex = 2
    PT_enumeration = 3
    PT_set = 4
    PT_int16 = 5
    PT_int32 = 6
    PT_int64 = 7
    PT_char8 = 8
    PT_char32 = 9
    PT_char256 = 10
    PT_char1024 = 11
    PT_object = 12
    PT_delegated = 13
    PT_bool = 14
    PT_timestamp = 15
    PT_double_array = 16
    PT_complex_array = 17
    PT_real = 18
    PT_float = 19
    PT_loadshape = 20
    PT_enduse = 21
    PT_random = 22
    PT_method = 23
    PT_AGGREGATE = -1
    PT_KEYWORD = -2
    PT_ACCESS = -3
    PT_SIZE = -4
    PT_FLAGS = -5
    PT_INHERIT = -6
    PT_UNITS = -7
    PT_DESCRIPTION = -8
    PT_EXTEND = -9
    PT_EXTENDBY = -10
    PT_DEPRECATED = -32768
    PT_HAS_NOTIFY = -16384
    PT_HAS_NOTIFY_OVERRIDE = -8192
    PT_LAST = 37

    # Define operator++ for PROPERTYTYPE enumeration
    def _incr_(d) -> Enum:
        return PROPERTYTYPE(d.value + 1)



class PROPERTYTYPE(Enum):
    PT_NOTYPE = 0
    PT_int32 = 1
    PT_int64 = 2
    PT_real32 = 3
    PT_real64 = 4
    PT_complex32 = 5
    PT_complex64 = 6
    PT_bool = 7
    PT_string = 8
    PT_object = 9
    PT_hex = 10
    PT_oct = 11
    PT_string32 = 12
    PT_method = 13
    PT_set = 14
    PT_object32 = 15
    PT_object64 = 16
    PT_enum = 17
    PT_delegated = 18
    PT_class = 19
    PT_ref = 20
    PT_blob = 21
    PT_any = 22
    PT_last = 23
    PT_DEPRECATED = 24
    PT_ACCESS = 25
    PT_SIZE = 26
    PT_EXTEND = 27
    PT_EXTENDBY = 28
    PT_FLAGS = 29
    PT_INHERIT = 30
    PT_UNITS = 31
    PT_DESCRIPTION = 32
    PT_HAS_NOTIFY = 33
    PT_HAS_NOTIFY_OVERRIDE = 34
    PT_KEYWORD = 35
    PT_enduse = 36
    PT_complex128 = 37
    PT_enumeration = 38
    PT_float32 = 39
    PT_float64 = 40
    PT_function = 41
    PT_int16 = 42
    PT_int8 = 43
    PT_type = 44
    PT_uint16 = 45
    PT_uint32 = 46
    PT_uint64 = 47
    PT_uint8 = 48
    PT_void = 49



class DELEGATEDTYPE:
    def __init__(self):
        self.oclass = None
        self.type =  [''] * 256
        self.from_string =  None
        self.to_string = None




# PROPERTYFLAGS = int  # Use an appropriate type for property flags
class PROPERTYFLAGS(Enum):
    PF_RECALC = 0x0001
    PF_CHARSET = 0x0002
    PF_EXTENDED = 0x0004
    PF_DEPRECATED = 0x8000
    PF_DEPRECATED_NONOTICE = 0x04000


class CLASSNAME(str):
    def __init__(self, value):
        super().__init__(value)


class DELEGATEDTYPE:
    def __init__(self, type, oclass, from_string, to_string):
        self.type = type
        self.oclass = oclass
        self.from_string = from_string
        self.to_string = to_string


# Define DELEGATEDVALUE structure
class DELEGATEDVALUE:
    def __init__(self, data, type: DELEGATEDTYPE):
        self.data = data
        self.type = type

# Define delegated as an alias for DELEGATEDVALUE
delegated = DELEGATEDVALUE


class KEYWORD:
    def __init__(self, name, value, next=None):
        self.name = name
        self.value = value
        self.next = next

# Define METHODCALL function type
# < the function that read and writes a string
class METHODCALL(BytesIO):
    def __init__(self, string: bytes, size: int=None):
        super().__init__(string)
        self.methodcall_size = size

    pass  # Replace with your implementation

# Define FUNCTIONNAME type
FUNCTIONNAME = str  # You can use an appropriate string type for function names

# Define PROPERTYSTRUCT structure
class PROPERTYSTRUCT:
    def __init__(self, prop, part: str):
        self.prop = prop
        self.part = part

# Define PROPERTYCOMPAREOP enumeration
class PROPERTYCOMPAREOP(Enum):
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

# Define PROPERTYCOMPAREFUNCTION function type
def PROPERTYCOMPAREFUNCTION(x, a, b) -> int:
    pass  # Replace with your implementation


# PROPERTYNAME = str  # You can use a suitable string type for property names
class PROPERTYNAME(str):
    def __init__(self, value):
        super().__init__(value)


# class PROPERTYSPEC:
#     def __init__(self):
#         self.name = None
#         self.xsdname = None
#         self.size = None
#         self.csize = None
#         self.data_to_string = None
#         self.string_to_data = None
#         self.create = None
#         self.stream = None
#         self.compare = None
#         self.get_part = None


# Define PROPERTYSPEC structure
class PROPERTYSPEC:
    def __init__(self, name: bytes = None, xsdname: bytes = None, size: int = None, csize: int = None,
                 data_to_string = None, string_to_data = None, create = None, stream = None,
                 compare: List[dict] = None, get_part = None):
        self.name = name
        self.xsdname = xsdname
        self.size = size
        self.csize = csize
        self.data_to_string = data_to_string
        self.string_to_data = string_to_data
        self.create = create
        self.stream = stream
        self.compare = compare
        self.get_part = get_part


# # Define property_getspec function
# def property_getspec(ptype: PROPERTYTYPE) -> Union[None, PROPERTYSPEC]:
#     pass  # Replace with your implementation

# Define PROPERTY structure
class PROPERTY:
    def __init__(self, oclass = None, name: str = None, ptype: PROPERTYTYPE = None,
                 size: int = None, width: int = None,
                 access: PROPERTYACCESS = None, unit = None, addr: PROPERTYADDR = None,
                 delegation = None,
                 keywords: KEYWORD = None, description: str = None, flags: PROPERTYFLAGS = None,
                 notify = None, method: METHODCALL = None, notify_override: bool = None):
        self.oclass = oclass
        self.name = name
        self.ptype = ptype
        self.size = size
        self.width = width
        self.access = access
        self.unit = unit
        self.addr = addr
        self.delegation = delegation
        self.keywords = keywords
        self.description = description
        self.flags = flags
        self.notify = notify
        self.method = method
        self.notify_override = notify_override

#
# class PROPERTY:
#     def __init__(self, prop_type, prop_addr, name, prop_units, prop_keys, prop_access, prop_description, flags):
#         self.ptype = prop_type
#         self.addr = prop_addr
#         self.name = name
#         self.unit = prop_units
#         self.keywords = prop_keys
#         self.access = prop_access
#         self.description = prop_description
#         self.flags = flags



# class PROPERTY:
#     def __init__(self, name="", ptype=None, access=0, size=0, flags=[], unit=None, description="",
#                  notify="", notify_override=False, keywords=""):
#         self.name = name
#         self.ptype = ptype
#         self.access = access
#         self.size = size
#         self.flags = flags
#         self.unit = unit
#         self.description = description
#         self.notify = notify
#         self.notify_override = notify_override
#         self.keywords = keywords



#
# # Define property_get_part function
# def property_get_part(obj, prop: PROPERTY, part: str) -> float:
#     pass  # Replace with your implementation
#
# # Define double_array_create function
# def double_array_create(a: List[List[real]]) -> int:
#     pass  # Replace with your implementation
#
# # Define complex_array_create function
# def complex_array_create(a: List[List[complex]]) -> int:
#     pass  # Replace with your implementation

# IMPORTANT: this list must match PROPERTYTYPE enum in property.h
# TODO: Fix "method" - was missing from list and causing segfaults, so populated.  No idea if it works or what it does

property_type = [
    PROPERTYSPEC(b"void", b"string", 0, 0, None, None),
    PROPERTYSPEC(b"double", b"decimal", 0, 24, None, None, None, None, None),
    PROPERTYSPEC(b"complex", b"string", 0, 48, None, None, None, None, None),
    PROPERTYSPEC(b"enumeration", b"string",  0, 32, None, None, None, None, None),
    PROPERTYSPEC(b"set", b"string",  0, 32, None, None, None, None, None),
    PROPERTYSPEC(b"int16", b"integer", 0, 6, None, None, None, None, None),
    PROPERTYSPEC(b"int32", b"integer", 0, 12, None, None, None, None, None),
    PROPERTYSPEC(b"int64", b"integer", 0, 24, None, None, None, None, None),
    PROPERTYSPEC(b"char8", b"string", 0, 8, None, None, None, None, None),
    PROPERTYSPEC(b"char32", b"string", 0, 32, None, None, None, None, None),
    PROPERTYSPEC(b"char256", b"string", 0, 256, None, None, None, None, None),
    PROPERTYSPEC(b"char1024", b"string", 0, 1024, None, None, None, None, None),
    PROPERTYSPEC(b"object", b"string", 0, 0, None, None, None, None, None),
    PROPERTYSPEC(b"delegated", b"string", 0xFFFFFFFF, 0, None, None),
    PROPERTYSPEC(b"bool", b"string", 0, 6, None, None, None, None, None),
    PROPERTYSPEC(b"timestamp", b"string", 0, 24, None, None, None, None, None),
    PROPERTYSPEC(b"double_array", b"string", 0, 0, None, None, 0, None, None),
    PROPERTYSPEC(b"complex_array", b"string", 0, 0, None, None, 0, None, None),
    PROPERTYSPEC(b"real", b"decimal", 0, 24, None, None),
    PROPERTYSPEC(b"float", b"decimal", 0, 24, None, None),
    PROPERTYSPEC(b"loadshape", b"string", 0, 0, None, 0, 0, None, None),
    PROPERTYSPEC(b"enduse", b"string", 0, 0, None,0, 0, None, None),
    PROPERTYSPEC(b"randomvar", b"string",0, 24, None,0, 0, None, None),
    PROPERTYSPEC(b"method", b"string", 0, 0, 0, 0)
]


# Check whether the properties as defined are mapping safely to memory
# Returns 0 on failure, 1 on success
def property_check():
    status = 1
    for ptype in range(1, len(property_type)):
        sz = 0
        if ptype == 1:
            sz = ctypes.sizeof(c_double)
        elif ptype == 2:
            sz = ctypes.sizeof(ctypes.c_double * 2)
        elif ptype == 3:
            sz = ctypes.sizeof(ctypes.c_int32)
        elif ptype == 4:
            sz = ctypes.sizeof(ctypes.c_int64)
        elif ptype == 5:
            sz = ctypes.sizeof(ctypes.c_int16)
        elif ptype == 6:
            sz = ctypes.sizeof(ctypes.c_int32)
        elif ptype == 7:
            sz = ctypes.sizeof(ctypes.c_int64)
        elif ptype == 8:
            sz = ctypes.sizeof(ctypes.c_char * 8)
        elif ptype == 9:
            sz = ctypes.sizeof(ctypes.c_char * 32)
        elif ptype == 10:
            sz = ctypes.sizeof(ctypes.c_char * 256)
        elif ptype == 11:
            sz = ctypes.sizeof(ctypes.c_char * 1024)
        elif ptype == 12:
            sz = ctypes.sizeof(ctypes.c_void_p)
        elif ptype == 13:
            sz = ctypes.sizeof(ctypes.c_bool)
        elif ptype == 14:
            sz = ctypes.sizeof(ctypes.c_int64)
        elif ptype == 15:
            sz = ctypes.sizeof(c_double * 1)
        elif ptype == 16:
            sz = ctypes.sizeof(c_double * 2)
        elif ptype == 17:
            sz = ctypes.sizeof(c_float)
        elif ptype == 18:
            sz = ctypes.sizeof(c_float)
        elif ptype == 19:
            sz = ctypes.sizeof(loadshape)
        elif ptype == 20:
            sz = ctypes.sizeof(enduse)
        elif ptype == 21:
            sz = ctypes.sizeof(randomvar_struct)

        print(
            f"property_check of {property_type[ptype].name.decode('utf-8')}: declared size is {property_type[ptype].size}, actual size is {sz}")
        if sz > 0 and property_type[ptype].size < sz:
            status = 0
            print(
                f"declared size of property {property_type[ptype].name.decode('utf-8')} smaller than actual size in memory on this platform (declared {property_type[ptype].size}, actual {sz})")
        elif sz > 0 and property_type[ptype].size != sz:
            print(
                f"declared size of property {property_type[ptype].name.decode('utf-8')} does not match actual size in memory on this platform (declared {property_type[ptype].size}, actual {sz})")

    return status


# Get the size of a single instance of a property
# Returns the size in bytes of a property
def property_size(prop: PROPERTY) -> int:
    if prop and prop.ptype > 0 and prop.ptype < len(property_type):
        return property_type[prop.ptype].size
    else:
        return 0
    # return prop.size


# # Get the size of a single instance of a property by type
# # Returns the size in bytes of a property
# def property_size_by_type(ptype):
#     return property_type[ptype].size
#

# # Create a property
# def property_create(prop, addr):
#     if prop and prop.ptype > 0 and prop.ptype < len(property_type):
#         if property_type[prop.ptype].create:
#             return property_type[prop.ptype].create(addr)
#         if property_type[prop.ptype].size > 0:
#             ctypes.memset(addr, 0, property_type[prop.ptype].size)
#         return 1
#     else:
#         return 0

#
# # Get the minimum buffer size of a property
# def property_minimum_buffersize(prop):
#     size = property_type[prop.ptype].csize
#     if size > 0:
#         return size
#     # @todo dynamic sizing
#     return 0

#
# # Get the comparison operation for a property type
# def property_compare_op(ptype, opstr):
#     for n in range(len(property_type[ptype].compare)):
#         if property_type[ptype].compare[n].str.decode('utf-8') == opstr:
#             return n
#     return -1

#
# # Compare two properties of the same type
# def property_compare_basic(ptype, op, x, a, b, part):
#     if part is None and property_type[ptype].compare[op].fn is not None:
#         return property_type[ptype].compare[op].fn(x, a, b)
#     elif property_type[ptype].get_part is not None:
#         d = property_type[ptype].get_part(x, part)
#         if math.isfinite(d):
#             return property_type[1].compare[op].fn(ctypes.byref(d), a, b)
#         else:
#             print(f"part {part} is not defined for type {property_type[ptype].name.decode('utf-8')}")
#             return False
#     else:
#         print(
#             f"property type '{property_type[ptype].name.decode('utf-8')}' does not support comparison operations or parts")
#         return False

#
# # Get the property type by name
# def property_get_type(name):
#     for ptype in range(len(property_type)):
#         if property_type[ptype].name.decode('utf-8') == name:
#             return ptype
#     return 0


# # Get a part of a property (specific to complex type)
# def complex_get_part(x, name):
#     c = ctypes.cast(x, ctypes.POINTER(c_double * 2)).contents
#     if name == "real":
#         return c[0]
#     elif name == "imag":
#         return c[1]
#     elif name == "mag":
#         return math.hypot(c[0], c[1])
#     elif name == "arg":
#         return math.atan2(c[1], c[0])
#     elif name == "ang":
#         return math.atan2(c[1], c[0]) * 180 / math.pi
#     return math.nan

#
# # Create a double array
# def double_array_create(a):
#     a = []
#     return 1


# # Get a part of a double array
# def double_array_get_part(x, name):
#     try:
#         n, m = map(int, name.split('.'))
#         a = x
#         if n < len(a) and m < len(a[n]):
#             return a[n][m]
#     except ValueError:
#         pass
#     return math.nan
#
#
# # Create a complex array
# def complex_array_create(a):
#     a = []
#     return 1

#
# # Get a part of a complex array
# def complex_array_get_part(x, name):
#     try:
#         n, m, subpart = name.split('.')
#         n, m = int(n), int(m)
#         a = x
#         if n < len(a) and m < len(a[n]):
#             if subpart == "real":
#                 return a[n][m][0]
#             elif subpart == "imag":
#                 return a[n][m][1]
#     except ValueError:
#         pass
#     return math.nan

# Rest of the functions that are not provided or are dependent on other code are commented out.
