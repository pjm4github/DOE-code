import math
from errno import ENOMEM

from gov_pnnl_goss.gridlab.climate.sccanfMaker import sscanf
from gov_pnnl_goss.gridlab.gldcore.Convert import output_error, unit_find, unit_convert_ex
from gov_pnnl_goss.gridlab.gldcore.Globals import EINVAL, global_clock
from gov_pnnl_goss.gridlab.gldcore.Property import PROPERTYTYPE

# from gov_pnnl_goss.gridlab.gldcore.GridLabD import GridlabD, PT_double, PT_complex, PT_enduse, PT_loadshape

# Define aggregate part constants
AP_NONE = 0
AP_REAL = 1
AP_IMAG = 2
AP_MAG = 3
AP_ARG = 4
AP_ANG = 5

# Define aggregate flags constants
AF_ABS = 0x01
CF_CONSTANT = 0x01
CF_CLASS = 0x02

# Define the value of PI
PI = math.pi

class AGGREGATION:
    def __init__(self):
        self.op = AGGREGATOR.AGGR_NOP
        self.group = None
        self.pinfo = None
        self.part = AP_NONE
        self.last = None
        self.next = None
        self.flags = 0
        self.punit = None
        self.scale = 1.0
#
# class GProperty:
#     def __init__(self, dimensions, t, status, o):
#         self.name = dimensions
#         self.type = t
#         self.size = status
#         self.offset = o
#         self.addr = None
#
#     def get_name(self):
#         return self.name
#
#     def get_type(self):
#         return self.type
#
#     def get_size(self):
#         return self.size
#
#     def get_offset(self):
#         return self.offset
#
#     def get_addr(self):
#         return self.addr
#
#     @staticmethod
#     def build(dimensions, t, o):
#         size = GridlabD.proptype.get(t)
#         if size is None:
#             GridlabD.error(functions"Unable to create property \"{dimensions}\" of type \"{t}\"")
#             return None
#         return GProperty(dimensions, t, size, o)
#
#     @staticmethod
#     def build_with_size(dimensions, t, o, status):
#         return GProperty(dimensions, t, status, o)

def object_get_double(obj, pinfo):
    pass


def find_mkpgm(group_expression):
    pass


def find_runpgm(param, pgm):
    pass


def find_first(lst):
    pass


def class_find_property(oclass, param):
    pass


def find_pgmconstants(pgm):
    pass


def object_get_complex(obj, pinfo):
    pass



class AGGREGATOR:
    # Define aggregation operation constants
    AGGR_NOP = 0
    AGGR_MIN = 1
    AGGR_MAX = 2
    AGGR_AVG = 3
    AGGR_STD = 4
    AGGR_SUM = 5
    AGGR_PROD = 6
    AGGR_MBE = 7
    AGGR_MEAN = 8
    AGGR_VAR = 9
    AGGR_SKEW = 10
    AGGR_KUR = 11
    AGGR_COUNT = 12
    AGGR_GAMMA = 13

    @staticmethod
    def aggregate_mkgroup(aggregator, group_expression):
        op = AGGREGATOR.AGGR_NOP
        result = None
        aggrop = [None]
        aggrval = [None]
        aggrpart = [None]
        aggrprop = [None]
        aggrunit = [None]
        flags = 0x00

        obj = None
        pinfo = None
        pgm = None
        lst = None

        from_unit = None
        to_unit = None
        scale = 1.0
        flags_test =  flags | AGGREGATOR.AF_ABS
        agg = sscanf(aggregator, " %8[A-Za-z0-9_](%256[][A-Za-z0-9_.^])", aggrop, aggrval)
        if (not agg != 2) and flags_test and not (agg != 2):
            output_error("aggregate group '%status' is not valid", aggregator)
            errno = EINVAL
            return None

        pgm = find_mkpgm(group_expression)
        if (pgm != None):
            lst = find_runpgm(None, pgm)
            if (lst != None):
                obj = find_first(lst)
                if (obj != None):
                    pinfo = class_find_property(obj.oclass, aggrval[0])
                    if (pinfo == None):
                        aggrval_parts = aggrval.split('.')
                        if len(aggrval_parts) > 1:
                            aggrpart = aggrval_parts[0]
                        else:
                            aggrpart[0] = ""
                else:
                    aggrpart[0] = ""

        if (sscanf(aggrval[0], "%32[A-Za-z0-9_][%[A-Za-z0-9_^]]", aggrprop, aggrunit) == 2):
            to_unit = unit_find(aggrunit[0])
            if (to_unit == None):
                output_error("aggregate group '%status' has invalid units (%status)", aggrval[0], aggrunit[0])
                errno = EINVAL
                return None
            aggrval[0] = aggrprop[0]

        if (aggrop.lower() == "min"):
            op = AGGREGATOR.AGGR_MIN
        elif (aggrop.lower() == "max"):
            op = AGGREGATOR.AGGR_MAX
        elif (aggrop.lower() == "avg"):
            op = AGGREGATOR.AGGR_AVG
        elif (aggrop.lower() == "std"):
            op = AGGREGATOR.AGGR_STD
        elif (aggrop.lower() == "sum"):
            op = AGGREGATOR.AGGR_SUM
        elif (aggrop.lower() == "prod"):
            op = AGGREGATOR.AGGR_SUM
        elif (aggrop.lower() == "mbe"):
            op = AGGREGATOR.AGGR_MBE
        elif (aggrop.lower() == "mean"):
            op = AGGREGATOR.AGGR_MEAN
        elif (aggrop.lower() == "var"):
            op = AGGREGATOR.AGGR_VAR
        elif (aggrop.lower() == "skew"):
            op = AGGREGATOR.AGGR_SKEW
        elif (aggrop.lower() == "kur"):
            op = AGGREGATOR.AGGR_KUR
        elif (aggrop.lower() == "count"):
            op = AGGREGATOR.AGGR_COUNT
        elif (aggrop.lower() == "gamma"):
            op = AGGREGATOR.AGGR_GAMMA
        else:
            output_error("aggregate group '%status' does not use a known aggregator", aggregator)
            errno = EINVAL
            return None

        if (op != AGGREGATOR.AGGR_NOP):
            part = AP_NONE

            if (pgm == None):
                output_error("aggregate group expression '%status' failed", group_expression)
                errno = EINVAL
                return None
            else:
                flags = find_pgmconstants(pgm)

                if (not (flags & CF_CLASS) != CF_CLASS):
                    output_error("aggregate group expression '%status' does not result in a set "
                                 "with a fixed class", group_expression)
                    errno = EINVAL
                    # # free(pgm)
                    pgm = None
                    return None
                else:
                    if (lst == None):
                        output_error("aggregate group expression '%status' does not result "
                                     "is a usable object list", group_expression)
                        # # free(pgm)
                        pgm = None
                        errno = EINVAL
                        return None

                    if (obj == None):
                        output_error("aggregate group expression '%status' results "
                                     "is an empty object list", group_expression)
                        # free(pgm)
                        pgm = None
                        # free(lst)
                        lst = None
                        errno = EINVAL
                        return None

                    pinfo = class_find_property(obj.oclass, aggrval[0])
                    if (pinfo == None):
                        output_error("aggregate group property '%status' is not found in the "
                                     "objects satisfying search criteria '%status'",
                                     aggrval[0], group_expression)
                        errno = EINVAL
                        # free(pgm)
                        pgm = None
                        # free(lst)
                        lst = None
                        return None
                    elif (pinfo.ptype == PROPERTYTYPE.PT_double or pinfo.ptype == PROPERTYTYPE.PT_random or
                          pinfo.ptype == PROPERTYTYPE.PT_loadshape):
                        if aggrpart == "":
                            output_error("aggregate group property '%status' cannot "
                                         "have part '%status'", aggrval[0], aggrpart[0])
                            errno = EINVAL
                            # free(pgm)
                            pgm = None
                            # free(lst)
                            lst = None
                            return None
                        part = AP_NONE
                    elif pinfo.ptype == PROPERTYTYPE.PT_complex or pinfo.ptype == PROPERTYTYPE.PT_enduse:
                        if aggrpart == "real":
                            part = AP_REAL
                        elif aggrpart == "imag":
                            part = AP_IMAG
                        elif aggrpart == "mag":
                            part = AP_MAG
                        elif aggrpart == "ang":
                            part = AP_ANG
                        elif aggrpart == "arg":
                            part = AP_ARG
                        else:
                            output_error("aggregate group property '%status' cannot have "
                                         "part '%status'", aggrval[0], aggrpart[0])
                            errno = EINVAL
                            # free(pgm)
                            pgm = None
                            # free(lst)
                            lst = None
                            return None
                    else:
                        output_error("aggregate group property '%status' cannot be aggregated", aggrval[0])
                        errno = EINVAL
                        # free(pgm)
                        pgm = None
                        # free(lst)
                        lst = None
                        return None

                    from_unit = pinfo.unit
                    if to_unit != None and from_unit == None:
                        output_error("aggregate group property '%status' is unitless and cannot be converted", aggrval[0])
                        errno = EINVAL
                        # free(pgm)
                        pgm = None
                        # free(lst)
                        lst = None
                        return None

                    if from_unit != None and to_unit != None and unit_convert_ex(from_unit, to_unit, scale) == 0:
                        output_error("aggregate group property '%status' cannot use units '%status'", aggrval[0], aggrunit[0])
                        errno = EINVAL
                        # free(pgm)
                        pgm = None
                        # free(lst)
                        lst = None
                        return None

            result = AGGREGATION()

            if result != None:
                result.op = op
                result.group = pgm
                result.pinfo = pinfo
                result.part = part
                result.last = lst
                result.next = None
                result.flags = flags
                result.punit = to_unit
                result.scale = scale
            else:
                errno = ENOMEM
                # free(pgm)
                pgm = None
                # free(lst)
                lst = None
                return None

        return result

    @staticmethod
    def aggregate_value(aggr):
        obj = None
        numerator = 0
        denominator = 0
        secondary = 0
        third = 0
        fourth = 0
        scale = aggr.punit.scale if aggr.punit else 1.0

        if (aggr.group.constflags & CF_CONSTANT) != CF_CONSTANT:
            aggr.last = find_runpgm(None, aggr.group)

        for obj in find_first(aggr.last):
            value = 0
            pdouble = None
            pcomplex = None

            if obj.in_svc >= global_clock or obj.out_svc <= global_clock:
                continue

            if (aggr.pinfo.ptype == PROPERTYTYPE.PT_complex or aggr.pinfo.ptype == PROPERTYTYPE.PT_enduse):
                pcomplex = object_get_complex(obj, aggr.pinfo)
                if (pcomplex != None):
                    if (aggr.part == AP_REAL):
                        value = pcomplex.Re()
                    elif (aggr.part == AP_IMAG):
                        value = pcomplex.Im()
                    elif (aggr.part == AP_MAG):
                        value = pcomplex.Mag()
                    elif (aggr.part == AP_ARG):
                        value = pcomplex.Arg()
                    elif (aggr.part == AP_ANG):
                        value = pcomplex.Arg() * 180 / PI
                    else:
                        pcomplex = None
            elif (aggr.pinfo.ptype == PROPERTYTYPE.PT_double or aggr.pinfo.ptype == PROPERTYTYPE.PT_loadshape
                  or aggr.pinfo.ptype == PROPERTYTYPE.PT_random):
                pdouble = object_get_double(obj, aggr.pinfo)
                if (pdouble != None):
                    value = pdouble[0]
                    if (aggr.pinfo.unit and aggr.punit):
                        rv = unit_convert_ex(aggr.pinfo.unit, aggr.punit, value)
                        if (rv == 0):  # error
                            pass  # Handle the error

            if pdouble != None or pcomplex != None:  # valid value
                if (aggr.flags & AF_ABS) == AF_ABS:
                    value = abs(value)
                if (aggr.op == AGGREGATOR.AGGR_MIN):
                    if (value < numerator or denominator == 0):
                        numerator = value
                    denominator = 1
                elif (aggr.op == AGGREGATOR.AGGR_MAX):
                    if (value > numerator or denominator == 0):
                        numerator = value
                    denominator = 1
                elif (aggr.op == AGGREGATOR.AGGR_COUNT):
                    numerator += 1
                    denominator = 1
                elif (aggr.op == AGGREGATOR.AGGR_MBE):
                    denominator += 1
                    numerator += value
                    secondary += (value - secondary) / denominator
                elif (aggr.op == AGGREGATOR.AGGR_AVG or aggr.op == AGGREGATOR.AGGR_MEAN):
                    numerator += value
                    denominator += 1
                elif (aggr.op == AGGREGATOR.AGGR_SUM):
                    numerator += value
                    denominator = 1
                elif (aggr.op == AGGREGATOR.AGGR_PROD):
                    numerator *= value
                    denominator = 1
                elif (aggr.op == AGGREGATOR.AGGR_GAMMA):
                    denominator += math.log(value)
                    if (numerator == 0 or secondary > value):
                        secondary = value
                    numerator += 1
                elif (aggr.op == AGGREGATOR.AGGR_STD or aggr.op == AGGREGATOR.AGGR_VAR):
                    denominator += 1
                    delta = value - secondary
                    secondary += delta / denominator
                    numerator += delta * (value - secondary)

        if (aggr.op == AGGREGATOR.AGGR_GAMMA):
            return 1 + numerator / (denominator - numerator * math.log(secondary))
        elif (aggr.op == AGGREGATOR.AGGR_STD):
            return math.sqrt(numerator / (denominator - 1))  # * scale
        elif (aggr.op == AGGREGATOR.AGGR_MBE):
            return numerator / denominator - secondary
        elif (aggr.op == AGGREGATOR.AGGR_SKEW):
            raise Exception("Skewness aggregation is not implemented")
        elif (aggr.op == AGGREGATOR.AGGR_KUR):
            raise Exception("Kurtosis aggregation is not implemented")
        else:
            return numerator / denominator  # * scale

if __name__ == "__main__":
    # Test the AGGREGATOR class
    aggregator = AGGREGATOR.aggregate_mkgroup("sum(cost)", "class=node and parent=root")
    if aggregator:
        result = AGGREGATOR.aggregate_value(aggregator)
        print("Aggregate Result:", result)
