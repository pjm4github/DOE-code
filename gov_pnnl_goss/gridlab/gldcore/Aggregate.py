import math
import re
from enum import Enum
from math import sqrt, log, atan, pi


AF_ABS = 0x01
global_clock = 0  # Placeholder for the actual global clock variable


# The FindProgram class should be defined elsewhere
class FindProgram:
    def __init__(self, criteria):
        self.criteria = criteria  # A dictionary of criteria used for filtering objects

    def run(self, all_objects):
        # Execute the find program on a list of all_objects and return the matching ones
        return [obj for obj in all_objects if self.matches_criteria(obj)]

    @staticmethod
    def matches_criteria(obj):
        # Placeholder for matching logic
        # Example: return all(getattr(self, key) == value for key, value in self.criteria.items())
        pass

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


def create_find_program(parsed_expression):
    # Placeholder for creating a find program from the parsed expression
    # In actual implementation, this would involve querying an object database or similar
    # Create a FindProgram object based on the parsed group expression
    return FindProgram(parsed_expression)


def class_find_property(obj, aggrval):
    # Assuming self is a dictionary-like object with properties
    # Find property info (pinfo) in the object's class based on aggrval
    pinfo = obj.get('oclass', {}).get(aggrval, None)
    if pinfo is None:
        raise ValueError(f"Property '{aggrval}' not found in the objects satisfying search criteria")
    return pinfo
4
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
    AP_NONE = 0
    AP_REAL = 1
    AP_IMAG = 2
    AP_MAG = 3
    AP_ANG = 4
    AP_ARG = 5


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


    # Constants representing different parts of a complex number (example values)
    AP_NONE = 0x00  # No part specified
    AP_REAL = 0x01  # Real part
    AP_IMAG = 0x02  # Imaginary part
    AP_MAG = 0x04   # Magnitude
    AP_ANG = 0x08   # Angle in radians
    AP_ARG = 0x10   # Argument (angle in radians)


    def __init__(self, aggregator, group_expression):
        self.aggregator = aggregator
        self.group_expression = group_expression
        self.op = None
        self.result = None
        self.group = None
        self.pinfo = None
        self.part = None
        self.last = None
        self.flags = 0x00
        self.from_unit = None
        self.to_unit = None
        self.scale = 1.0
        self.aggregate_mkgroup()

    def aggregate_mkgroup(self):

        # Parse the aggregator to determine the operation
        op, aggrval, aggrunit = self.parse_aggregator()
        self.op = op
        # Parse the group expression to create a find program (pgm)
        pgm = create_find_program(self.group_expression)
        # pgm = self.parse_group_expression()

        # Assuming we have a list of objects that match the group expression
        list_of_objects = self.find_runpgm(pgm)

        # Find property information (pinfo) based on aggrval
        obj = list_of_objects[0]
        self.pinfo = class_find_property(obj, aggrval)  # Example using the first object

        # Handle units and get scale factor
        property_name, unit, scale = self.handle_units(aggrval)
        flags = self.extract_flags(pgm)
        part = self.determine_part(aggrval)

        # Build the aggregation unit
        self.result = self.build_aggregation_unit(self.op, pgm, self.pinfo, part, list_of_objects, flags, unit, scale)
        self.from_unit = self.pinfo.unit
        self.to_unit = self.extract_units(aggrunit)


    def parse_aggregator(self):
        # Parse aggregator and group_expression
        match = re.match(r'\s*(\w+)\(([\w.]+)\)', self.aggregator)
        if not match:
            raise ValueError("Invalid aggregator syntax")

        aggrop, aggrval = match.groups()
        # Parse property and unit
        prop_match = re.match(r'(\w+)([(\w+)])?', aggrval)
        aggrunit = None
        if prop_match:
            aggrprop, _, aggrunit = prop_match.groups()

        # Map aggregator string to operation
        ops = {
            'min': 'AGGR_MIN',
            'max': 'AGGR_MAX',
            'avg': 'AGGR_AVG',
            'std': 'AGGR_STD',
            'sum': 'AGGR_SUM',
            'prod': 'AGGR_PROD',
            'mbe': 'AGGR_MBE',
            'mean': 'AGGR_MEAN',
            'var': 'AGGR_VAR',
            'skew': 'AGGR_SKEW',
            'kur': 'AGGR_KUR',
            'count': 'AGGR_COUNT',
            'gamma': 'AGGR_GAMMA'
        }
        op = ops.get(aggrop.lower())

        if op is None:
            raise ValueError("Unknown aggregator")

        return op, aggrval, aggrunit


    def extract_flags(self, pgm: FindProgram):
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

    def get_pgm_constants(self, pgm: [FindProgram, dict]):
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

    def matches_criteria(self, obj, pgm):
        # This method checks if an object matches the search criteria defined in pgm.
        # It's a placeholder for the actual implementation.
        # Example implementation could be:
        # return all(getattr(self, key) == value for key, value in pgm.items())
        pass

    # Assume __init__ and other methods are defined above

    def get_all_objects(self):
        # This method retrieves all available objects in the simulation environment.
        # It's a placeholder for the actual implementation.
        # Example implementation could be:
        # return environment.get_all_objects()

        # Retrieve all objects from the global simulation environment.
        return global_simulation_environment.get_all_objects()


    def parse_group_expression(self):
        # Parse the group expression and create a program (pgm) to find objects
        parsed_expression = {}
        for condition in self.group_expression.split('and'):
            key, value = map(str.strip, condition.split('='))
            parsed_expression[key] = value
        # Placeholder for creating a program to find objects based on parsed_expression
        pgm = create_find_program(parsed_expression)
        return pgm


    def handle_units(self, aggrval):
        # Handle unit conversion if necessary
        property_name, unit = self.extract_units(aggrval)
        # Placeholder for unit conversion logic
        # In actual implementation, this would involve converting units
        scale = self.scale  # Replace with actual scale after unit conversion
        return property_name, unit, scale

    def extract_units(self, aggrval):
        # Extract property name and units from aggrval
        match = re.match(r'(\w+)[(\w+)]', aggrval)
        if match:
            property_name, unit = match.groups()
        else:
            property_name, unit = aggrval, None
        return property_name, unit

    def build_aggregation_unit(self, op, pgm, pinfo, part, list, flags, to_unit, scale):
        # Build the aggregation unit based on provided parameters
        result = {
            'op': op,
            'group': pgm,
            'pinfo': pinfo,
            'part': part,
            'last': list,
            'flags': flags,
            'punit': to_unit,
            'scale': scale
        }
        return result

    def aggregate_value(self):
        numerator = 0
        denominator = 0
        secondary = 0
        # third = 0
        # fourth = 0
        # scale = self.scale if self.to_unit else 1.0
        if (self.group.constflags & self.CF_CONSTANT) != self.CF_CONSTANT:
            self.last = self.find_runpgm(self.group)
        for obj in self.last:  # Assuming self.last is a list of objects to aggregate

            # Assuming self is a dictionary-like object with properties
            if obj['in_svc'] >= global_clock or obj['out_svc'] <= global_clock:
                continue

            value = self.get_value_from_object(obj)  # Placeholder for actual value retrieval method

            if self.flags & AF_ABS:
                value = abs(value)

            if self.op == 'AGGR_MIN':
                if value < numerator or denominator == 0:
                    numerator = value
                denominator = 1

            elif self.op == 'AGGR_MAX':
                if value > numerator or denominator == 0:
                    numerator = value
                denominator = 1

            elif self.op == 'AGGR_COUNT':
                numerator += 1
                denominator = 1

            elif self.op == 'AGGR_MBE':
                denominator += 1
                numerator += value
                secondary += (value - secondary) / denominator

            elif self.op == 'AGGR_AVG' or self.op == 'AGGR_MEAN':
                numerator += value
                denominator += 1

            elif self.op == 'AGGR_SUM':
                numerator += value
                denominator = 1

            elif self.op == 'AGGR_PROD':
                numerator *= value
                denominator = 1

            elif self.op == 'AGGR_GAMMA':
                denominator += log(value)
                if numerator == 0 or secondary > value:
                    secondary = value
                numerator += 1

            elif self.op == 'AGGR_STD' or self.op == 'AGGR_VAR':
                denominator += 1
                delta = value - secondary
                secondary += delta / denominator
                numerator += delta * (value - secondary)
            elif self.op == 'AGGR_SKEW' or self.op == 'AGGR_KUR':
                # Additional cases like AGGR_SKEW and AGGR_KUR would be added here
                pass
            else:
                pass

        # Finalize the aggregation based on self.op
        if self.op == 'AGGR_GAMMA':
            return 1 + numerator / (denominator - numerator * log(secondary))

        elif self.op == 'AGGR_STD':
            return sqrt(numerator / (denominator - 1)) # * scale

        elif self.op == 'AGGR_MBE':
            return numerator / denominator - secondary

        # Additional finalizations for other operations like AGGR_SKEW and AGGR_KUR

        elif self.op == 'AGGR_SKEW':
            # 		/** @todo implement skewness aggregate (no ticket) */
            # 		throw_exception("skewness aggregation is not implemented");
            # 		/* TROUBLESHOOT
            # 			An attempt to use the skew aggregator failed because it is not implemented yet.
            # 			Remove or replace the reference to the skew aggregate and try again.
            # 		 */
            raise NotImplemented
        elif self.op == 'AGGR_KUR':
            # 		/** @todo implement kurtosis aggregate (no ticket) */
            # 		throw_exception("kurtosis aggregation is not implemented");
            # 		/* TROUBLESHOOT
            # 			An attempt to use the kurtosis aggregator failed because it is not implemented yet.
            # 			Remove or replace the reference to the
            # 		 */
            raise NotImplemented

        else:
            return numerator / denominator # * scale

    def get_value_from_object(self, obj):
        # Retrieve the property value based on the property type
        if self.pinfo['ptype'] in ['PT_complex', 'PT_enduse']:
            pcomplex = obj[self.pinfo['name']]
            if pcomplex is not None:
                part_switcher = {
                    'AP_REAL': pcomplex.real,
                    'AP_IMAG': pcomplex.imag,
                    'AP_MAG': abs(pcomplex),
                    'AP_ARG': math.atan2(pcomplex.imag, pcomplex.real),
                    'AP_ANG': math.degrees(math.atan2(pcomplex.imag, pcomplex.real))
                }
                return part_switcher.get(self.part, None)

        elif self.pinfo['ptype'] in ['PT_double', 'PT_loadshape', 'PT_random']:
            pdouble = obj[self.pinfo['name']]
            if pdouble is not None:
                return pdouble

        # Handle other property types if necessary
        return None

    def determine_part(self, aggrval):
        # This method determines the part of the property to be aggregated.
        if 'complex' in self.pinfo['ptype'] or 'enduse' in self.pinfo['ptype']:
            # Complex properties must specify a part
            match = re.search(r'.(\w+)$', aggrval)
            if match:
                part_name = match.group(1)
                part_switcher = {
                    'real': self.AP_REAL,
                    'imag': self.AP_IMAG,
                    'mag': self.AP_MAG,
                    'ang': self.AP_ANG,
                    'arg': self.AP_ARG
                }
                aggrpart = part_switcher.get(part_name.lower())
                if aggrpart is None:
                    raise ValueError(f"Unknown part '{part_name}' for property '{aggrval}'")
            else:
                raise ValueError(f"Complex property '{aggrval}' must specify a part (e.g., real, imag)")
        elif 'double' in self.pinfo['ptype'] or 'random' in self.pinfo['ptype'] or 'loadshape' in self.pinfo['ptype']:
            # These types cannot have parts
            if '.' in aggrval:
                raise ValueError(f"Property '{aggrval}' cannot have a part specified")
            aggrpart = self.AP_NONE
        else:
            raise ValueError(f"Property '{aggrval}' cannot be aggregated")

        return aggrpart

if __name__ == "__main__":
    # Test the AGGREGATOR class
    aggregator = Aggregate("sum(cost)", "class=node and parent=root")
    if aggregator:
        result = Aggregate.aggregate_value(aggregator)
        print("Aggregate Result:", result)
