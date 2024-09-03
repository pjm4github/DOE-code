import math
import re
from enum import Enum
from math import sqrt, log, atan, pi

from typing import Optional

from gridlab.gldcore import Convert
from gridlab.gldcore.Class import ClassRegistry
from gridlab.gldcore.Find import FindList, FindProgramNew
from gridlab.gldcore.Find import Find
from gridlab.gldcore.PropertyHeader import PropertyType
from gridlab.gldcore.Unit import unit_find

AF_ABS = 0x01
global_clock = 0  # Placeholder for the actual global clock variable



# The SimulationEnvironment should eb defined elsewhere
class SimulationEnvironment:
    # This class represents the simulation environment and its object registry.

    def __init__(self):
        self.object_registry = []  # A list to store all objects in the simulation

    def register_object(self, obj):
        # Method to register an object in the simulation.
        self.object_registry.append(obj)

    def get_all_objects(self):
        # Method to retrieve all registered objects.
        return self.object_registry


# Assuming we have a global instance of the simulation environment
global_simulation_environment = SimulationEnvironment()



class AGGREGATOR(Enum):
    """
    AGGREGATOR; /**< the aggregation method to use */
    """
    AGGR_NOP = 1
    AGGR_MIN = 2
    AGGR_MAX = 3
    AGGR_AVG = 4
    AGGR_STD = 5
    AGGR_MBE = 6
    AGGR_MEAN = 7
    AGGR_VAR = 8
    AGGR_SKEW = 9
    AGGR_KUR = 10
    AGGR_GAMMA = 11
    AGGR_COUNT = 12
    AGGR_SUM = 13
    AGGR_PROD = 14


class AGGRPART(Enum):
    """
    AGGRPART; /**< the part of complex values to aggregate */
    """
    # Constants representing different parts of a complex number (example values)
    AP_NONE = 0x00  # No part specified
    AP_REAL = 0x01  # Real part
    AP_IMAG = 0x02  # Imaginary part
    AP_MAG = 0x04   # Magnitude
    AP_ANG = 0x08   # Angle in radians
    AP_ARG = 0x10   # Argument (angle in radians)




class AGGREGATION:
    """
    Represents an aggregation with various properties and references to other
    structures and types for handling aggregation operations.
    """
    def __init__(self, op: 'AGGREGATOR', group: Optional[FindList],
                 pinfo: 'PROPERTY', punit: 'UNIT', scale: float,
                 part: 'AGGRPART', flags: int, last: 'Optional[FindList]',
                 next: 'Optional[AGGREGATION]'):
        self.flags = flags  # aggregation flags (e.g., AF_ABS)
        self.group = group  # the find program used to build the aggregation
        self.last = last  # the result of the last run
        self.next = next  # the next aggregation in the core's list of aggregators
        self.op = op  # the aggregation operator (min, max, etc.)
        self.part = part  # the property part (complex only)
        self.pinfo = pinfo  # the property over which the aggregation is done
        self.punit = punit  # the unit we want to output the property in
        self.scale = scale  # the scalar to convert from the old units to the desired units


class Aggregate:
    """
    $Id: aggregate.c 4738 2014-07-03 00:55:39Z dchassin $
    Copyright (C) 2008 Battelle Memorial Institute
    @file aggregate.c
    @addtogroup aggregate Aggregate of object properties
    @ingroup core

    Aggregate functions support calculations over properties of multiple objects.
    This is used primarily by the collector object in the tape module to define groups
    (see the \p group property in aggregate_mkgroupthe collector object). The \p group can defined
    by specifying a boolean series are relationship of object properties, e.g.,

        \verbatim class=node and parent=root \endverbatim.

    Aggregations also must specify the property that is to be aggregated. Most common
    aggregations and some uncommon ones are supported.  In addition, if the aggregation is
    over a complex quantity, the aggregation must specific how a double is to be obtained
    from it, e.g., magnitude, angle, real, imaginary.  Some examples aggregate \p property
    definitions are

        \verbatim
        sum(cost)
        max(power.angle)
        mean(energy.mag)
        std(price)
        \endverbatim

    @bug Right now, not all allowed aggregations are invariant (meaning that the members of the group
    do not change over time). However, the collector object requires invariant aggregations. Using
    an aggregation that isn't invariant will cause the simulation to fail. (ticket #112)

    Example usage:
        aggr = Aggregate('sum(cost)', 'class=node and parent=root')
        result = aggr.aggregate_value()
    """
    # Define aggregate flags constants
    AF_ABS = 0x01
    CF_CONSTANT = 0x01
    CF_CLASS = 0x02

    def __init__(self, aggregator: str, group_expression: str):
        self.aggregator = aggregator
        self.from_unit = None
        self.group_expression = group_expression
        self.aggregation = AGGREGATION(
            op=AGGREGATOR.AGGR_NOP,
            group=None,
            pinfo=None,
            punit=None,
            scale=1.0,
            part=AGGRPART.AP_NONE,
            flags=0,
            last=None,
            next=None)
        self.aggregate_mkgroup()

    def aggregate_mkgroup(self):
        aggregate_op, aggregate_value, aggregate_unit = self.parse_aggregator()

        # Parse the group expression to create a find program (program)
        # program = Find.find_mkpgm(self.group_expression)
        obj = None
        program = self.parse_group_expression()
        aggregtate_part = ""
        list_of_objects = None
        if program is not None:
            # Run the program and get a list of results
            # Assuming we have a list of objects that match the group expression
            list_of_objects = Find.find_runpgm(program)
            if list_of_objects is not None:
                # Attempt to get the first object from the list
                obj = Find.find_first(list_of_objects)
                if obj is not None:
                    # Try to find the property within the object's class
                    self.pinfo = ClassRegistry.find_property(obj.oclass, aggregate_value)
                    if self.pinfo is None:
                        # Attempt to split the aggregate value and part, if specified
                        aggregate_part_position = aggregate_value.rfind('.')
                        aggregate_parts = aggregate_value.split('.')
                        aggregate_value = aggregate_parts[0]
                        if len(aggregate_parts) > 1:
                            aggregtate_part = aggregate_parts[1]
                        else:
                            aggregtate_part = ""
                    else:
                        aggregtate_part = ""  # No part given

        # aggprop, aggunit = self.extract_units(aggregate_value)
        # Handle units and get scale factor

        base_unit, aggrprop_value = self.extract_units(aggregate_unit)
        # Placeholder for unit conversion logic
        # In actual implementation, this would involve converting units
        scale = self.aggregation.scale  # Replace with actual scale after unit conversion
        # Return the base unit. If aggregate_unit = M^3 then unit_file will return M
        self.to_unit = unit_find(base_unit)  #self.extract_units(aggregate_unit)
        # Assuming `unit_find`, `output_error`, and the variables
        # `aggregate_unit`, `aggregate_value`, and `aggrprop` are properly defined or imported
        # self.to_unit = unit_find(aggregate_unit)
        if self.to_unit is None:
            # Simulate the output_error function, perhaps by raising an exception or logging an error
            raise ValueError(
                f"Aggregate group '{aggregate_value}' has invalid units ({aggregate_unit}). Check your aggregations and make sure all the units are defined.")
            # Alternatively, if you're logging instead of raising an exception:
            # output_error(f"Aggregate group '{aggregate_value}' has invalid units ({aggregate_unit}).")

        if aggregate_op != AGGREGATOR.AGGR_NOP:
            # part = self.determine_part(aggregate_value)
            part = AGGRPART.AP_NONE

            if program is None:
                raise ValueError(f"Aggregate group expression '{self.group_expression}' failed")
            else:
                flags = Find.find_pgmconstants(program)

                if not (flags & self.CF_CLASS == self.CF_CLASS):
                    raise ValueError(
                        f"Aggregate group expression '{self.group_expression}' does not result in a set with a fixed class")
                elif list is None:
                    raise ValueError(
                        f"Aggregate group expression '{self.group_expression}' does not result is a usable object list")
                elif obj is None:
                    raise ValueError(f"Aggregate group expression '{self.group_expression}' results is an empty object list")
                else:
                    self.pinfo = ClassRegistry.find_property(obj.oclass, aggregate_value)
                    if self.pinfo is None:
                        raise ValueError(
                            f"Aggregate group property '{aggregate_value}' is not found in the objects satisfying search criteria '{self.group_expression}'")

                    if self.pinfo.ptype in [PropertyType.PT_double, PropertyType.PT_random, PropertyType.PT_loadshape] and aggregtate_part != "":
                        raise ValueError(f"Aggregate group property '{aggregate_value}' cannot have part '{aggregtate_part}'")
                    elif self.pinfo.ptype in [PropertyType.PT_complex, PropertyType.PT_enduse]:
                        if aggregtate_part == "real":
                            part = AGGRPART.AP_REAL
                        # Add other parts as elif branches
                        else:
                            raise ValueError(f"Aggregate group property '{aggregate_value}' cannot have part '{aggregtate_part}'")
                    else:
                        raise ValueError(f"Aggregate group property '{aggregate_value}' cannot be aggregated")

                    self.from_unit = self.pinfo.unit
                    if self.to_unit is not None and self.from_unit is None:
                        raise ValueError(f"Aggregate group property '{aggregate_value}' is unitless and cannot be converted")
                    if self.from_unit and self.to_unit and not Convert.unit_convert_ex(self.from_unit, self.to_unit, scale):
                        raise ValueError(f"Aggregate group property '{aggregate_value}' cannot use units '{aggregate_unit}'")

                # build aggregation unit
                # self.result = self.build_aggregation_unit(self.aggregation.op, program, self.pinfo, part, list_of_objects, flags, self.to_unit, scale)
                self.result = AGGREGATION(self.aggregation.op, program, self.pinfo, self.to_unit, scale, part, flags, list_of_objects, None)

        else:
            self.result = None
        return self.result

    def aggregate_value(self):
        numerator = 0
        denominator = 0
        secondary = 0
        # third = 0
        # fourth = 0
        # scale = self.scale if self.to_unit else 1.0
        if (self.aggregation.group.constflags & self.CF_CONSTANT) != self.CF_CONSTANT:
            self.last = self.find_runpgm(self.aggregation.group)
        for obj in self.last:  # Assuming self.last is a list of objects to aggregate

            # Assuming self is a dictionary-like object with properties
            if obj['in_svc'] >= global_clock or obj['out_svc'] <= global_clock:
                continue

            value = self.get_value_from_object(obj)  # Placeholder for actual value retrieval method

            if self.aggregation.flags & AF_ABS:
                value = abs(value)

            if self.aggregation.op == AGGREGATOR.AGGR_MIN:
                if value < numerator or denominator == 0:
                    numerator = value
                denominator = 1

            elif self.aggregation.op == AGGREGATOR.AGGR_MAX:
                if value > numerator or denominator == 0:
                    numerator = value
                denominator = 1

            elif self.aggregation.op == AGGREGATOR.AGGR_COUNT:
                numerator += 1
                denominator = 1

            elif self.aggregation.op == AGGREGATOR.AGGR_MBE:
                denominator += 1
                numerator += value
                secondary += (value - secondary) / denominator

            elif self.aggregation.op == AGGREGATOR.AGGR_AVG or self.aggregation.op == AGGREGATOR.AGGR_MEAN:
                numerator += value
                denominator += 1

            elif self.aggregation.op == AGGREGATOR.AGGR_SUM:
                numerator += value
                denominator = 1

            elif self.aggregation.op == AGGREGATOR.AGGR_PROD:
                numerator *= value
                denominator = 1

            elif self.aggregation.op == AGGREGATOR.AGGR_GAMMA:
                denominator += log(value)
                if numerator == 0 or secondary > value:
                    secondary = value
                numerator += 1

            elif self.aggregation.op == AGGREGATOR.AGGR_STD or self.aggregation.op == AGGREGATOR.AGGR_VAR:
                denominator += 1
                delta = value - secondary
                secondary += delta / denominator
                numerator += delta * (value - secondary)
            elif self.aggregation.op == AGGREGATOR.AGGR_SKEW or self.aggregation.op == AGGREGATOR.AGGR_KUR:
                # Additional cases like AGGR_SKEW and AGGR_KUR would be added here
                pass
            else:
                pass

        # Finalize the aggregation based on self.op
        if self.aggregation.op == AGGREGATOR.AGGR_GAMMA:
            return 1 + numerator / (denominator - numerator * log(secondary))

        elif self.aggregation.op == AGGREGATOR.AGGR_STD:
            return sqrt(numerator / (denominator - 1)) # * scale

        elif self.aggregation.op == AGGREGATOR.AGGR_MBE:
            return numerator / denominator - secondary

        # Additional finalizations for other operations like AGGR_SKEW and AGGR_KUR

        elif self.aggregation.op == 'AGGR_SKEW':
            # 		/** @todo implement skewness aggregate (no ticket) */
            # 		throw_exception("skewness aggregation is not implemented");
            # 		/* TROUBLESHOOT
            # 			An attempt to use the skew aggregator failed because it is not implemented yet.
            # 			Remove or replace the reference to the skew aggregate and try again.
            # 		 */
            raise NotImplemented
        elif self.aggregation.op == 'AGGR_KUR':
            # 		/** @todo implement kurtosis aggregate (no ticket) */
            # 		throw_exception("kurtosis aggregation is not implemented");
            # 		/* TROUBLESHOOT
            # 			An attempt to use the kurtosis aggregator failed because it is not implemented yet.
            # 			Remove or replace the reference to the
            # 		 */
            raise NotImplemented

        else:
            return numerator / denominator # * scale

    # def build_aggregation_unit(self, op, pgm, pinfo, part, list, flags, to_unit, scale):
    #     # Build the aggregation unit based on provided parameters
    #     # result = {
    #     #     'op': op,
    #     #     'group': pgm,
    #     #     'pinfo': pinfo,
    #     #     'part': part,
    #     #     'last': list,
    #     #     'flags': flags,
    #     #     'punit': to_unit,
    #     #     'scale': scale
    #     # }
    #     result = AGGREGATION(op, pgm, pinfo, to_unit, scale, part, flags, list, None)
    #     return result


    def determine_part(self, aggrval):
        # This method determines the part of the property to be aggregated.
        if 'complex' in self.pinfo['global_property_types'] or 'enduse' in self.pinfo['global_property_types']:
            # Complex properties must specify a part
            match = re.search(r'.(\w+)$', aggrval)
            if match:
                part_name = match.group(1)
                part_switcher = {
                    'real': AGGRPART.AP_REAL,
                    'imag': AGGRPART.AP_IMAG,
                    'mag': AGGRPART.AP_MAG,
                    'ang': AGGRPART.AP_ANG,
                    'arg': AGGRPART.AP_ARG
                }
                aggrpart = part_switcher.get(part_name.lower())
                if aggrpart is None:
                    raise ValueError(f"Unknown part '{part_name}' for property '{aggrval}'")
            else:
                raise ValueError(f"Complex property '{aggrval}' must specify a part (e.g., real, imag)")
        elif 'double' in self.pinfo['global_property_types'] or 'random' in self.pinfo['global_property_types'] or 'loadshape' in self.pinfo['global_property_types']:
            # These types cannot have parts
            if '.' in aggrval:
                raise ValueError(f"Property '{aggrval}' cannot have a part specified")
            aggrpart = AGGRPART.AP_NONE  # self.aggregation.part # AP_NONE
        else:
            raise ValueError(f"Property '{aggrval}' cannot be aggregated")

        return aggrpart

    def extract_flags(self, pgm: FindProgramNew):
        # This method should extract flags from the program (pgm).
        # Since the actual flag extraction logic depends on the simulation environment,
        # this is a placeholder for the actual implementation.

        # Placeholder: get the flags from the pgm
        # In an actual implementation, this might involve calling a function similar to find_pgmconstants
        flags = self.get_pgm_constants(pgm)

        # Check if the flags include CF_CLASS using bitwise AND
        if (flags & self.CF_CLASS) != self.CF_CLASS:
            raise ValueError("Group expression does not result in a set with a fixed class")

        return flags

    @staticmethod
    def extract_units(aggrval):
        modifier = ""
        base_unit = None

        if aggrval:
            # Extract property name and units from aggrval
            p = r"\[([\w]+)([\^\w]*)\]"  # matches ''[m^3]' or '[M]'

            # this string '100[M^3]' will parse into 100 for property_value and M^3 for aggrunit
            # the units must be enclosed in [] brackets without a space between the bracket and no spaces in the bracket
            prop_match = re.match(p, aggrval)
            if prop_match:
                base_unit, modifier = prop_match.groups()

        return base_unit, modifier

    def find_runpgm(self, pgm):
        # This method runs the search program (pgm) to find matching objects.
        # The actual implementation would depend on the simulation environment and object model.

        # Placeholder: list of all available objects in the simulation environment
        all_objects = self.get_all_objects()

        # Placeholder: list to store objects that match the search criteria
        matching_objects = []

        # Iterate over all objects and select those that match the criteria defined in pgm
        for obj in all_objects:
            if self.matches_criteria(obj, pgm):
                matching_objects.append(obj)

        return matching_objects

    def get_all_objects(self):
        # This method retrieves all available objects in the simulation environment.
        # It's a placeholder for the actual implementation.
        # Example implementation could be:
        # return environment.get_all_objects()

        # Retrieve all objects from the global simulation environment.
        return global_simulation_environment.get_all_objects()

    def get_pgm_constants(self, pgm: [FindProgramNew, dict]):
        # This method retrieves the constant flags associated with the program (pgm).
        # It's a placeholder for the actual implementation.
        # Example implementation could be:
        # return pgm.get_constants()
        # This method retrieves the constant flags associated with the program (pgm).
        # The actual implementation would depend on how the pgm object is structured and how it stores constants.

        # Hypothetical example: if pgm is a dictionary with a 'constflags' key
        if isinstance(pgm, dict) and 'constflags' in pgm:
            return pgm['constflags']

        # Hypothetical example: if pgm is an object with a method to get constants
        elif hasattr(pgm, 'get_constants'):
            return pgm.get_constants()

        # If pgm does not have the expected structure or method, raise an error
        else:
            raise AttributeError("The program does not contain constant flags information.")

    def get_value_from_object(self, obj):
        # Retrieve the property value based on the property global_property_types
        if self.pinfo['global_property_types'] in ['PT_complex', 'PT_enduse']:
            pcomplex = obj[self.pinfo['name']]
            if pcomplex is not None:
                part_switcher = {
                    AGGRPART.AP_REAL: pcomplex.real,
                    AGGRPART.AP_IMAG: pcomplex.imag,
                    AGGRPART.AP_MAG: abs(pcomplex),
                    AGGRPART.AP_ARG: math.atan2(pcomplex.imag, pcomplex.real),
                    AGGRPART.AP_ANG: math.degrees(math.atan2(pcomplex.imag, pcomplex.real))
                }
                return part_switcher.get(self.aggregation.part, None)

        elif self.pinfo['global_property_types'] in ['PT_double', 'PT_loadshape', 'PT_random']:
            pdouble = obj[self.pinfo['name']]
            if pdouble is not None:
                return pdouble

        # Handle other property types if necessary
        return None

    def matches_criteria(self, obj, pgm):
        # This method checks if an object matches the search criteria defined in pgm.
        # It's a placeholder for the actual implementation.
        # Example implementation could be:
        # return all(getattr(self, key) == value for key, value in pgm.items())
        pass

    def parse_aggregator(self):
        # Parse aggregator
        # self.op = aggrop
        # Parse the aggregator to determine the operation
        # Regular expressions for the patterns

        # match = re.match(r'\s*(\w+)\(([\w.]+)\)', self.aggregator)  # matches 'sum(length)'
        # if not match:
        #     raise ValueError("Invalid aggregator syntax")
        #
        # aggrop, aggrval = match.groups()
        #
        # aggrprop, aggrunit = self.extract_units(aggrval)
        #
        # # Map aggregator string to operation
        # ops = {
        #     'min': AGGREGATOR.AGGR_MIN,
        #     'max': AGGREGATOR.AGGR_MAX,
        #     'avg': AGGREGATOR.AGGR_AVG,
        #     'std': AGGREGATOR.AGGR_STD,
        #     'sum': AGGREGATOR.AGGR_SUM,
        #     'prod': AGGREGATOR.AGGR_PROD,
        #     'mbe': AGGREGATOR.AGGR_MBE,
        #     'mean': AGGREGATOR.AGGR_MEAN,
        #     'var': AGGREGATOR.AGGR_VAR,
        #     'skew': AGGREGATOR.AGGR_SKEW,
        #     'kur': AGGREGATOR.AGGR_KUR,
        #     'count': AGGREGATOR.AGGR_COUNT,
        #     'gamma': AGGREGATOR.AGGR_GAMMA
        # }
        # op = ops.get(aggrop.lower())
        aggregator_string = self.aggregator.strip()

        p = r"(\w+)\(([\w.^]+)(\[[\w.^]+\])*\)"
        # will match
        #     sum(price.real)
        #     sum(price.real[W])
        #     sum(price.50^10[W^3])
        #     sum(power.real[A])
        match = re.match(p, aggregator_string)
        if match:
            aggregate_property, aggregate_value, aggregate_unit = match.groups()
        else:
            p = r"(\w+)[\(|]([\w.^]+)(\[[\w.^]+\])*[\)|]"
            # Set the flag and try the second pattern if the first fails
            match = re.match(p, aggregator_string)
            if match:
                self.aggregation.flags |= AF_ABS
                aggregate_property, aggregate_value, aggregate_unit = match.groups()
            else:
                # Handle the error case
                raise ValueError(
                    f"Aggregate group '{aggregator_string}' is not valid. \n"
                    f"An aggregation expression does not have the required syntax, e.g., <i>aggregation</i>(<i>value</i>[.<i>part</i>])."
                    f"Check the aggregation's syntax and make sure it conforms to the required syntax.")
                # In actual code, instead of raising an exception, you might log an error or handle it differently based on your application's needs

        # aggrprop, aggrunit = self.extract_units(aggrval)

        ops = {
            'min': AGGREGATOR.AGGR_MIN,
            'max': AGGREGATOR.AGGR_MAX,
            'avg': AGGREGATOR.AGGR_AVG,
            'std': AGGREGATOR.AGGR_STD,
            'sum': AGGREGATOR.AGGR_SUM,
            'prod': AGGREGATOR.AGGR_PROD,
            'mbe': AGGREGATOR.AGGR_MBE,
            'mean': AGGREGATOR.AGGR_MEAN,
            'var': AGGREGATOR.AGGR_VAR,
            'skew': AGGREGATOR.AGGR_SKEW,
            'kur': AGGREGATOR.AGGR_KUR,
            'count': AGGREGATOR.AGGR_COUNT,
            'gamma': AGGREGATOR.AGGR_GAMMA
        }
        op = ops.get(aggregate_property.lower(), AGGREGATOR.AGGR_NOP)

        return op, aggregate_value, aggregate_unit

    def parse_group_expression(self):
        # Parse the group expression and create a program (pgm) to find objects
        parsed_expression = {}
        for condition in self.group_expression.split('and'):
            key, value = map(str.strip, condition.split('='))
            parsed_expression[key] = value
        # Placeholder for creating a program to find objects based on parsed_expression
        pgm = FindProgramNew.find_program(parsed_expression)
        return pgm


if __name__ == "__main__":
    # Test the AGGREGATOR class
    try:
        test_aggregator = "sum(length[m])"
        aggregator = Aggregate(test_aggregator, "class=node and parent=root")
        if aggregator:
            result = Aggregate.aggregate_value(aggregator)
            print("Aggregate Result:", result)
    except ValueError as e:
        print(e)

    try:
        test_aggregator ="max(power.angle[deg])"
        aggregator = Aggregate(test_aggregator, "class=node and parent=root")
        if aggregator:
            result = Aggregate.aggregate_value(aggregator)
            print("Aggregate Result:", result)
    except ValueError as e:
        print(e)

    try:

        test_aggregator = "mean(energy.mag[W])"
        aggregator = Aggregate(test_aggregator, "class=node and parent=root")
        if aggregator:
            result = Aggregate.aggregate_value(aggregator)
            print("Aggregate Result:", result)
    except ValueError as e:
        print(e)

    try:
        test_aggregator = "std(price[$])"
        aggregator = Aggregate(test_aggregator, "class=node and parent=root")
        if aggregator:
            result = Aggregate.aggregate_value(aggregator)
            print("Aggregate Result:", result)
    except ValueError as e:
        print(e)

