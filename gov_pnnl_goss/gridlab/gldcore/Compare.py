import math
import ctypes


class TCOperator:
    def __init__(self, code, symbol, function=None, extra_args=0):
        self.code = code
        self.symbol = symbol
        self.function = function
        self.extra_args = extra_args

def compare_tc_double_eq(x, a, b):
    return float(x) == float(a)

def compare_tc_double_le(x, a, b):
    return float(x) <= float(a)

def compare_tc_double_ge(x, a, b):
    return float(x) >= float(a)

def compare_tc_double_ne(x, a, b):
    return float(x) != float(a)

def compare_tc_double_lt(x, a, b):
    return float(x) < float(a)

def compare_tc_double_gt(x, a, b):
    return float(x) > float(a)

def compare_tc_double_in(x, a, b):
    return float(a) <= float(x) <= float(b)

def compare_tc_double_ni(x, a, b):
    return not (float(a) <= float(x) <= float(b))

def compare_tc_float_eq(x, a, b):
    return float(x) == float(a)

def compare_tc_float_le(x, a, b):
    return float(x) <= float(a)

def compare_tc_float_ge(x, a, b):
    return float(x) >= float(a)

def compare_tc_float_ne(x, a, b):
    return float(x) != float(a)

def compare_tc_float_lt(x, a, b):
    return float(x) < float(a)

def compare_tc_float_gt(x, a, b):
    return float(x) > float(a)

def compare_tc_float_in(x, a, b):
    return float(a) <= float(x) <= float(b)

def compare_tc_float_ni(x, a, b):
    return not (float(a) <= float(x) <= float(b))

def compare_tc_uint16_eq(x, a, b):
    return int(x) == int(a)

def compare_tc_uint16_le(x, a, b):
    return int(x) <= int(a)

def compare_tc_uint16_ge(x, a, b):
    return int(x) >= int(a)

def compare_tc_uint16_ne(x, a, b):
    return int(x) != int(a)

def compare_tc_uint16_lt(x, a, b):
    return int(x) < int(a)

def compare_tc_uint16_gt(x, a, b):
    return int(x) > int(a)

def compare_tc_uint16_in(x, a, b):
    return int(a) <= int(x) <= int(b)

def compare_tc_uint16_ni(x, a, b):
    return not (int(a) <= int(x) <= int(b))

def compare_tc_uint32_eq(x, a, b):
    return int(x) == int(a)

def compare_tc_uint32_le(x, a, b):
    return int(x) <= int(a)

def compare_tc_uint32_ge(x, a, b):
    return int(x) >= int(a)

def compare_tc_uint32_ne(x, a, b):
    return int(x) != int(a)

def compare_tc_uint32_lt(x, a, b):
    return int(x) < int(a)

def compare_tc_uint32_gt(x, a, b):
    return int(x) > int(a)

def compare_tc_uint32_in(x, a, b):
    return int(a) <= int(x) <= int(b)

def compare_tc_uint32_ni(x, a, b):
    return not (int(a) <= int(x) <= int(b))

def compare_tc_uint64_eq(x, a, b):
    return int(x) == int(a)

def compare_tc_uint64_le(x, a, b):
    return int(x) <= int(a)

def compare_tc_uint64_ge(x, a, b):
    return int(x) >= int(a)

def compare_tc_uint64_ne(x, a, b):
    return int(x) != int(a)

def compare_tc_uint64_lt(x, a, b):
    return int(x) < int(a)

def compare_tc_uint64_gt(x, a, b):
    return int(x) > int(a)

def compare_tc_uint64_in(x, a, b):
    return int(a) <= int(x) <= int(b)

def compare_tc_uint64_ni(x, a, b):
    return not (int(a) <= int(x) <= int(b))

def compare_tc_string_eq(x, a, b):
    return str(x) == str(a)

def compare_tc_string_le(x, a, b):
    return str(x) <= str(a)

def compare_tc_string_ge(x, a, b):
    return str(x) >= str(a)

def compare_tc_string_ne(x, a, b):
    return str(x) != str(a)

def compare_tc_string_lt(x, a, b):
    return str(x) < str(a)

def compare_tc_string_gt(x, a, b):
    return str(x) > str(a)

def compare_tc_string_in(x, a, b):
    return str(a) in str(x)

def compare_tc_string_ni(x, a, b):
    return str(a) not in str(x)

def compare_tc_bool_eq(x, a, b):
    return bool(x) == bool(a)

def compare_tc_bool_ne(x, a, b):
    return bool(x) != bool(a)

def compare_tc_timestamp_eq(x, a, b):
    return x == a

def compare_tc_timestamp_ne(x, a, b):
    return x != a

def compare_tc_object_eq(x, a, b):
    return x.name == a.name

def compare_tc_object_ne(x, a, b):
    return x.name != a.name

TCNONE = [TCOperator(0, "", None)] * 8

TCOPB = [
    TCOperator(1, "==", compare_tc_double_eq),
    TCOperator(0, "", None),
    TCOperator(0, "", None),
    TCOperator(2, "!=", compare_tc_double_ne),
    TCOperator(0, "", None),
    TCOperator(0, "", None),
    TCOperator(0, "", None),
    TCOperator(0, "", None),
]

TCOPS = [
    TCOperator(1, "==", compare_tc_double_eq),
    TCOperator(3, "<=", compare_tc_double_le),
    TCOperator(4, ">=", compare_tc_double_ge),
    TCOperator(2, "!=", compare_tc_double_ne),
    TCOperator(5, "<", compare_tc_double_lt),
    TCOperator(6, ">", compare_tc_double_gt),
    TCOperator(7, "inside", compare_tc_double_in, 1),
    TCOperator(8, "outside", compare_tc_double_ni, 1),
]


# Double
TCOPD = [
    TCOperator(1, "==", compare_tc_double_eq),
    TCOperator(3, "<=", compare_tc_double_le),
    TCOperator(4, ">=", compare_tc_double_ge),
    TCOperator(2, "!=", compare_tc_double_ne),
    TCOperator(5, "<", compare_tc_double_lt),
    TCOperator(6, ">", compare_tc_double_gt),
    TCOperator(7, "inside", compare_tc_double_in, 1),
    TCOperator(8, "outside", compare_tc_double_ni, 1),
]

# Float
TCOPF = [
    TCOperator(1, "==", compare_tc_float_eq),
    TCOperator(3, "<=", compare_tc_float_le),
    TCOperator(4, ">=", compare_tc_float_ge),
    TCOperator(2, "!=", compare_tc_float_ne),
    TCOperator(5, "<", compare_tc_float_lt),
    TCOperator(6, ">", compare_tc_float_gt),
    TCOperator(7, "inside", compare_tc_float_in, 1),
    TCOperator(8, "outside", compare_tc_float_ni, 1),
]

# Additional TCOPD, TCOPF, TCOPB, TCOPS, TCOPD can be defined for other types as needed.


class CompareOps:
    @staticmethod
    def eqi(x, a, b):
        return ctypes.c_int32(x).value == ctypes.c_int32(a).value

    @staticmethod
    def lei(x, a, b):
        return ctypes.c_int32(x).value <= ctypes.c_int32(a).value

    @staticmethod
    def gei(x, a, b):
        return ctypes.c_int32(x).value >= ctypes.c_int32(a).value

    @staticmethod
    def nei(x, a, b):
        return ctypes.c_int32(x).value != ctypes.c_int32(a).value

    @staticmethod
    def lti(x, a, b):
        return ctypes.c_int32(x).value < ctypes.c_int32(a).value

    @staticmethod
    def gti(x, a, b):
        return ctypes.c_int32(x).value > ctypes.c_int32(a).value

    @staticmethod
    def ini(x, a, b):
        return (
            ctypes.c_int32(a).value <= ctypes.c_int32(x).value
            and b is not None
            and ctypes.c_int32(x).value <= ctypes.c_int32(b).value
        )

    @staticmethod
    def nii(x, a, b):
        return not (
            ctypes.c_int32(a).value <= ctypes.c_int32(x).value
            and b is not None
            and ctypes.c_int32(x).value <= ctypes.c_int32(b).value
        )


class CompareOpsB:
    @staticmethod
    def eqb(x, a, b):
        return bool(x) == bool(a)

    @staticmethod
    def neb(x, a, b):
        return bool(x) != bool(a)

class CompareOpsO:
    @staticmethod
    def eqo(x, a, b):
        return x.name == a.name

    @staticmethod
    def neo(x, a, b):
        return x.name != a.name

class CompareOpsF:
    @staticmethod
    def eqf(x, a, b):
        if b is None:
            return math.isclose(x, a, rel_tol=1e-9, abs_tol=0.0)
        else:
            return math.isclose(x, a, rel_tol=1e-9, abs_tol=b)

    @staticmethod
    def lef(x, a, b):
        return x <= a

    @staticmethod
    def gef(x, a, b):
        return x >= a

    @staticmethod
    def nef(x, a, b):
        if b is None:
            return not math.isclose(x, a, rel_tol=1e-9, abs_tol=0.0)
        else:
            return math.isclose(x, a, rel_tol=1e-9, abs_tol=b)

    @staticmethod
    def ltf(x, a, b):
        return x < a

    @staticmethod
    def gtf(x, a, b):
        return x > a

    @staticmethod
    def inf(x, a, b):
        return a <= x and b is not None and x <= b

    @staticmethod
    def nif(x, a, b):
        return not (a <= x and b is not None and x <= b)

class CompareOpsS:
    @staticmethod
    def seq(x, a, b):
        return x == a

    @staticmethod
    def sle(x, a, b):
        return x <= a

    @staticmethod
    def sge(x, a, b):
        return x >= a

    @staticmethod
    def sne(x, a, b):
        return x != a

    @staticmethod
    def slt(x, a, b):
        return x < a

    @staticmethod
    def sgt(x, a, b):
        return x > a

    @staticmethod
    def sin(x, a, b):
        return a <= x and b is not None and x <= b

    @staticmethod
    def sni(x, a, b):
        return not (a <= x and b is not None and x <= b)

class CompareOpsObj:
    @staticmethod
    def eqo(x, a, b):
        return x.name == a.name

    @staticmethod
    def neo(x, a, b):
        return x.name != a.name
