import math
import re

from gov_pnnl_goss.gridlab.climate.CsvReader import PADDR
from gov_pnnl_goss.gridlab.gldcore.Class import Class
from gov_pnnl_goss.gridlab.gldcore.Convert import output_error, unit_find
from gov_pnnl_goss.gridlab.gldcore.Exec import exec_clock
from gov_pnnl_goss.gridlab.gldcore.GridLabD import TS_ZERO
from gov_pnnl_goss.gridlab.gldcore.Output import output_verbose
from gov_pnnl_goss.gridlab.gldcore.Property import QNAN, PROPERTYTYPE, PROPERTY, PROPERTYACCESS
from enum import Enum, auto
from ctypes import memset

EUC_IS110 = 0x0000
EUC_IS220 = 0x0001
EUC_HEATLOAD = 0x0002

enduse_list = None
n_enduses = 0
enduse_magic = 0x8c3d7762
run = 0
enduse_synctime = 0


class Enduse:
    """
    This class defines the enduse and its related operations.
    """
    def __init__(self):

        self.cronos = 0

        # meter values
        self.total = complex()  # total power in kW
        self.energy = complex()  # total energy in kWh
        self.demand = complex()  # maximum power in kW (can be reset)

        # circuit configuration
        self.config = set()  # end-use configuration
        self.breaker_amps = 0.0  # breaker limit (if any)

        # zip values
        self.admittance = complex()  # constant impedance option of load in kW
        self.current = complex()  # constant current portion of load in kW
        self.power = complex()  # constant power portion of load in kW

        # composite load data
        self.motor = [EUMOTOR() for _ in range(EUMOTORTYPE._EUMT_COUNT.value)]  # motor loads (A-D)
        self.electronic = [EUELECTRONIC() for _ in range(EUELECTRONICTYPE._EUET_COUNT.value)]  # electronic loads (S/D)

        # loading
        self.impedance_fraction = 0.0  # constant impedance fraction (pu load)
        self.current_fraction = 0.0  # constant current fraction (pu load)
        self.power_fraction = 0.0  # constant power fraction (pu load)
        self.power_factor = 0.0  # power factor
        self.voltage_factor = 0.0  # voltage factor (pu nominal)

        # heat
        self.heatgain = 0.0  # internal heat from load (Btu/h)
        self.cumulative_heatgain = 0.0  # internal cumulative heat gain from load (Btu)
        self.heatgain_fraction = 0.0  # fraction of power that goes to internal heat (pu Btu/h)

        # misc info
        self.name = ""
        self.shape = None
        self.t_last = 0.0  # last time of update

        # added for backward compatibility with res ENDUSELOAD
        # @todo these are obsolete and must be retrofitted with the above values
        self.end_obj = None

        self.next = None

    def enduse_get_part(self, x, name):
        """
        Get part of the enduse data.
        """
        e = x
        if name == "total.real":
            return e.total.Re()
        if name == "total.imag":
            return e.total.Im()
        if name == "total.mag":
            return e.total.Mag()
        if name == "total.arg":
            return e.total.Arg()
        if name == "total.ang":
            return e.total.Arg() * 180 / PI

        if name == "energy.real":
            return e.energy.Re()
        if name == "energy.imag":
            return e.energy.Im()
        if name == "energy.mag":
            return e.energy.Mag()
        if name == "energy.arg":
            return e.energy.Arg()
        if name == "energy.ang":
            return e.energy.Arg() * 180 / PI

        if name == "demand.real":
            return e.demand.Re()
        if name == "demand.imag":
            return e.demand.Im()
        if name == "demand.mag":
            return e.demand.Mag()
        if name == "demand.arg":
            return e.demand.Arg()
        if name == "demand.ang":
            return e.demand.Arg() * 180 / PI

        if name == "breaker_amps":
            return e.breaker_amps

        if name == "admittance.real":
            return e.admittance.Re()
        if name == "admittance.imag":
            return e.admittance.Im()
        if name == "admittance.mag":
            return e.admittance.Mag()
        if name == "admittance.arg":
            return e.admittance.Arg()
        if name == "admittance.ang":
            return e.admittance.Arg() * 180 / PI

        if name == "current.real":
            return e.current.Re()
        if name == "current.imag":
            return e.current.Im()
        if name == "current.mag":
            return e.current.Mag()
        if name == "current.arg":
            return e.current.Arg()
        if name == "current.ang":
            return e.current.Arg() * 180 / PI

        if name == "power.real":
            return e.power.Re()
        if name == "power.imag":
            return e.power.Im()
        if name == "power.mag":
            return e.power.Mag()
        if name == "power.arg":
            return e.power.Arg()
        if name == "power.ang":
            return e.power.Arg() * 180 / PI

        if name == "impedance_fraction":
            return e.impedance_fraction

        if name == "current_fraction":
            return e.current_fraction

        if name == "power_fraction":
            return e.power_fraction

        if name == "power_factor":
            return e.power_factor

        if name == "voltage_factor":
            return e.voltage_factor

        if name == "heatgain":
            return e.heatgain

        if name == "heatgain_fraction":
            return e.heatgain_fraction

        if name == "motorA.power":
            return e.motor[EUMT_MOTOR_A].power
        if name == "motorA.impedance":
            return e.motor[EUMT_MOTOR_A].impedance
        if name == "motorA.inertia":
            return e.motor[EUMT_MOTOR_A].inertia
        if name == "motorA.v_stall":
            return e.motor[EUMT_MOTOR_A].v_stall
        if name == "motorA.v_start":
            return e.motor[EUMT_MOTOR_A].v_start
        if name == "motorA.v_trip":
            return e.motor[EUMT_MOTOR_A].v_trip
        if name == "motorA.t_trip":
            return e.motor[EUMT_MOTOR_A].t_trip

        if name == "motorB.power":
            return e.motor[EUMT_MOTOR_B].power
        if name == "motorB.impedance":
            return e.motor[EUMT_MOTOR_B].impedance
        if name == "motorB.inertia":
            return e.motor[EUMT_MOTOR_B].inertia
        if name == "motorB.v_stall":
            return e.motor[EUMT_MOTOR_B].v_stall
        if name == "motorB.v_start":
            return e.motor[EUMT_MOTOR_B].v_start
        if name == "motorB.v_trip":
            return e.motor[EUMT_MOTOR_B].v_trip
        if name == "motorB.t_trip":
            return e.motor[EUMT_MOTOR_B].t_trip

        if name == "motorC.power":
            return e.motor[EUMT_MOTOR_C].power
        if name == "motorC.impedance":
            return e.motor[EUMT_MOTOR_C].impedance
        if name == "motorC.inertia":
            return e.motor[EUMT_MOTOR_C].inertia
        if name == "motorC.v_stall":
            return e.motor[EUMT_MOTOR_C].v_stall
        if name == "motorC.v_start":
            return e.motor[EUMT_MOTOR_C].v_start
        if name == "motorC.v_trip":
            return e.motor[EUMT_MOTOR_C].v_trip
        if name == "motorC.t_trip":
            return e.motor[EUMT_MOTOR_C].t_trip

        if name == "motorD.power":
            return e.motor[EUMT_MOTOR_D].power
        if name == "motorD.impedance":
            return e.motor[EUMT_MOTOR_D].impedance
        if name == "motorD.inertia":
            return e.motor[EUMT_MOTOR_D].inertia
        if name == "motorD.v_stall":
            return e.motor[EUMT_MOTOR_D].v_stall
        if name == "motorD.v_start":
            return e.motor[EUMT_MOTOR_D].v_start
        if name == "motorD.v_trip":
            return e.motor[EUMT_MOTOR_D].v_trip
        if name == "motorD.t_trip":
            return e.motor[EUMT_MOTOR_D].t_trip

        if name == "electronicA.power":
            return e.electronic[EUMT_MOTOR_A].power
        if name == "electronicA.inertia":
            return e.electronic[EUMT_MOTOR_A].inertia
        if name == "electronicA.v_trip":
            return e.electronic[EUMT_MOTOR_A].v_trip
        if name == "electronicA.v_start":
            return e.electronic[EUMT_MOTOR_A].v_start

        if name == "electronicB.power":
            return e.electronic[EUMT_MOTOR_B].power
        if name == "electronicB.inertia":
            return e.electronic[EUMT_MOTOR_B].inertia
        if name == "electronicB.v_trip":
            return e.electronic[EUMT_MOTOR_B].v_trip
        if name == "electronicB.v_start":
            return e.electronic[EUMT_MOTOR_B].v_start

        return QNAN


    def enduse_create(self, data):
        """
        Create an enduse for debugging.
        """


        memset(data, 0, sizeof(enduse))
        data.next = enduse_list
        enduse_list = data
        n_enduses += 1

        data.power_factor = 1.0
        data.heatgain_fraction = 1.0

        # Enable debugging
        if _DEBUG:
            data.magic = enduse_magic

        return 1

    def enduse_init(self, e):
        """
        Initialize the enduse for debugging.
        """

        if hasattr(e, 'magic') and e.magic != enduse_magic:
            raise Exception("enduse '%s' magic number bad" % e.name)

        e.t_last = TS_ZERO

        return 0


    def enduse_init_all(self):
        """
        Initialize all enduses for debugging.
        """

        e = enduse_list
        while e is not None:
            if enduse_init(e) == 1:
                return FAILED
            e = e.next
        return SUCCESS

    def enduse_sync(self, e, passconfig, t1):
        """
        Synchronize the enduse with the given configuration and timestamp.
        """
        pass

    def enduse_sync_all(self, t1):
        """
        Synchronize all enduses with the given timestamp.
        """
        pass

    def convert_from_enduse(self, string, size, data, prop):
        """
        Convert the properties of an enduse from a string.
        """

        e = data
        len = 0

        def OUTPUT_NZ(X):
            nonlocal len
            if getattr(e, X) != 0:
                len += len + sprintf(string + len, "%s%s: %f", "" if len > 0 else "; ", X, getattr(e, X))

        def OUTPUT(X):
            nonlocal len
            len += sprintf(string + len, "%s%s: %f", "" if len > 0 else "; ", X, getattr(e, X))

        OUTPUT_NZ("impedance_fraction")
        OUTPUT_NZ("current_fraction")
        OUTPUT_NZ("power_fraction")
        OUTPUT("power_factor")
        OUTPUT("power.Re()")
        OUTPUT_NZ("power.Im()")

        return len

    def enduse_publish(self, oclass, struct_address, prefix):
        """
        Publish the enduse properties for a specific oclass and prefix.
        """
        pass

    def convert_to_enduse(self, string, data, prop):
        """
        Convert the properties of an enduse to a string.
        """
        pass

    def enduse_test(self):
        """
        Test the enduse functionality.
        """

        failed = 0
        ok = 0
        errorcount = 0

        class Test:
            def __init__(self, name):
                self.name = name

        test = [Test("TODO")]

        output_test("\nBEGIN: enduse tests")

        for p in test:
            pass

        if failed:
            output_error("endusetest: %d enduse tests failed--see test.txt for more information" % failed)
            output_test("!!! %d enduse tests failed, %d errors found" % (failed, errorcount))
        else:
            output_verbose("%d enduse tests completed with no errors--see test.txt for details" % ok)
            output_test("endusetest: %d schedule tests completed, %d errors found" % (ok, errorcount))
        output_test("END: enduse tests")
        return failed

    def enduse_syncproc(self, ptr):
        """
        Synchronize the enduse data.
        """
        pass

    def exec_clock(self):
        """
        Execute the enduse clock function.
        """
        pass

class EnduseSyncData:
    def __init__(self):
        self.n = 0
        self.pt = None
        self.ok = False
        self.e = None
        self.ne = 0
        self.t0 = 0
        self.ran = 0










class EUMOTORTYPE(Enum):
    EUMT_MOTOR_A = auto()  #  /**< 3ph induction motors driving constant torque loads */
    EUMT_MOTOR_B = auto()  #  /**< induction motors driving high inertia speed-squares torque loads */
    EUMT_MOTOR_C = auto()  #  /**< induction motors driving low inertia loads speed-squared torque loads
    EUMT_MOTOR_D = auto()  #  /**< 1ph induction motors driving constant torque loads */
    _EUMT_COUNT = auto()   # /* must be last */

class EUELECTRONICTYPE(Enum):
    EUET_ELECTRONIC_A = auto()
    EUET_ELECTRONIC_B = auto()
    _EUET_COUNT = auto()


class EUMOTOR:
    def __init__(self):
        self.power = complex()  # motor power when running
        self.impedance = complex()  # motor impedance when stalled
        self.inertia = 0.0  # motor inertia in seconds
        self.v_stall = 0.0  # motor stall voltage (pu)
        self.v_start = 0.0  # motor start voltage (pu)
        self.v_trip = 0.0  # motor trip voltage (pu)
        self.t_trip = 0.0  # motor thermal trip time in seconds


class EUELECTRONIC:
    def __init__(self):
        self.power = complex()  # load power when running
        self.inertia = 0.0  # load "inertia"
        self.v_trip = 0.0  # load "trip" voltage (pu)
        self.v_start = 0.0  # load "start" voltage (pu)

    def create(self, data):
        data.fill(0)
        data.next = self.enduse_list
        enduse_list = data
        self.n_enduses += 1

        data.power_factor = 1.0
        data.heatgain_fraction = 1.0


    def init(self, e):
        if hasattr(e, 'magic') and e.magic != enduse_magic:
            raise Exception("enduse '%s' magic number bad" % e.name)
        e.t_last = TS_ZERO

        return 0

    def initall(self):
        e = enduse_list
        while e is not None:
            if self.init(e) == 1:
                return "FAILED"
            e = e.next
        return "SUCCESS"

    def sync(self, e, passconfig, t1):
        pass

    def convert_from_enduse(self, data, prop):
        """
        Convert enduse data to a string representation.

        Args:
            data (enduse): The enduse data structure.
            prop (PROPERTY): The property associated with the enduse.

        Returns:
            str: A string representation of the enduse data.
        """
        len = 0
        output_string = ""

        def output_nz(X):
            nonlocal len, output_string
            if getattr(data, X) != 0:
                output_string += f"{'; ' if len > 0 else ''}{X}: {getattr(data, X)}"
                len += 1

        def output(X):
            nonlocal len, output_string
            output_string += f"{'; ' if len > 0 else ''}{X}: {getattr(data, X)}"
            len += 1

        output_nz("impedance_fraction")
        output_nz("current_fraction")
        output_nz("power_fraction")
        output("power_factor")
        output("power.Re()")
        output_nz("power.Im()")

        return output_string

    def publish(self, oclass, struct_address, prefix):
        """
        Publish properties of an enduse class.

        Args:
            oclass (Class): The class to which properties are published.
            struct_address: The struct address.
            prefix (str): The prefix for property names.

        Returns:
            int: The number of properties published.
        """
        # self = None  # temporary enduse structure used for mapping variables
        result = 0

        class PropItem:
            def __init__(self, prop_type, name, addr, description, flags):
                self.type = prop_type
                self.name = name
                self.addr = addr
                self.description = description
                self.flags = flags

        prop_list = [
            PropItem(PROPERTYTYPE.PT_complex, "energy[kVAh]", PADDR(self.energy),
                     "the total energy consumed since the last meter reading", 0),
            PropItem(PROPERTYTYPE.PT_complex, "power[kVA]", PADDR(self.total), "the total power consumption of the load", 0),
            PropItem(PROPERTYTYPE.PT_complex, "peak_demand[kVA]", PADDR(self.demand),
                     "the peak power consumption since the last meter reading", 0),
            PropItem(PROPERTYTYPE.PT_double, "heatgain[Btu/h]", PADDR(self.heatgain),
                     "the heat transferred from the enduse to the parent", 0),
            PropItem(PROPERTYTYPE.PT_double, "cumulative_heatgain[Btu]", PADDR(self.cumulative_heatgain),
                     "the cumulative heatgain from the enduse to the parent", 0),
            PropItem(PROPERTYTYPE.PT_double, "heatgain_fraction[pu]", PADDR(self.heatgain_fraction),
                     "the fraction of the heat that goes to the parent", 0),
            PropItem(PROPERTYTYPE.PT_double, "current_fraction[pu]", PADDR(self.current_fraction),
                     "the fraction of total power that is constant current", 0),
            PropItem(PROPERTYTYPE.PT_double, "impedance_fraction[pu]", PADDR(self.impedance_fraction),
                     "the fraction of total power that is constant impedance", 0),
            PropItem(PROPERTYTYPE.PT_double, "power_fraction[pu]", PADDR(self.power_fraction),
                     "the fraction of the total power that is constant power", 0),
            PropItem(PROPERTYTYPE.PT_double, "power_factor", PADDR(self.power_factor), "the power factor of the load", 0),
            PropItem(PROPERTYTYPE.PT_complex, "constant_power[kVA]", PADDR(self.power), "the constant power portion of the total load",
                     0),
            PropItem(PROPERTYTYPE.PT_complex, "constant_current[kVA]", PADDR(self.current),
                     "the constant current portion of the total load", 0),
            PropItem(PROPERTYTYPE.PT_complex, "constant_admittance[kVA]", PADDR(self.admittance),
                     "the constant admittance portion of the total load", 0),
            PropItem(PROPERTYTYPE.PT_double, "voltage_factor[pu]", PADDR(self.voltage_factor), "the voltage change factor", 0),
            PropItem(PROPERTYTYPE.PT_double, "breaker_amps[A]", PADDR(self.breaker_amps), "the rated breaker amperage", 0),
            PropItem(PROPERTYTYPE.PT_set, "configuration", PADDR(self.config), "the load configuration options", 0),
            PropItem(PROPERTYTYPE.PT_KEYWORD, "IS110", "EUC_IS110", None, 0),
            PropItem(PROPERTYTYPE.PT_KEYWORD, "IS220", "EUC_IS220", None, 0),
        ]

      # Publish the enduse load itself
        prop = PROPERTY(PROPERTYTYPE.PT_enduse, oclass, "load" if prefix == "" else prefix, struct_address, None)

        prop.description = "the enduse load description"
        prop.flags = 0
        Class.class_add_property(oclass, prop)

        last = None
        for p in prop_list:
            name = p.name
            lastname = ""

            if prefix != "" and prefix is not None:
                name = f"{prefix}.{p.name}"

            if p.ptype < PROPERTYTYPE._PT_LAST:
                prop = PROPERTY(p.ptype, oclass, name, p.addr + struct_address, None)
                prop.description = p.description
                prop.flags = p.flags
                Class.class_add_property(oclass, prop)
                result += 1
            elif last is None:
                output_error("PT_KEYWORD not allowed unless it follows another property specification")
                """
                The enduse_publish structure is not defined correctly. This is an internal error and cannot be corrected by
                users. Contact technical support and report this problem.
                """
                return -result
            elif p.ptype == PROPERTYTYPE.PT_KEYWORD:
                if last.ptype == PROPERTYTYPE.PT_enumeration:
                    if not Class.class_define_enumeration_member(oclass, lastname, p.name, p.ptype):
                        output_error(f"unable to publish enumeration member '{p.name}' of enduse '{last.name}'")
                        """
                        The enduse_publish structure is not defined correctly. This is an internal error and cannot be corrected by
                        users. Contact technical support and report this problem.
                        """
                        return -result
                elif last.ptype == PROPERTYTYPE.PT_set:
                    if not Class.class_define_set_member(oclass, lastname, p.name, int(p.addr)):
                        output_error(f"unable to publish set member '{p.name}' of enduse '{last.name}'")
                        """
                        The enduse_publish structure is not defined correctly. This is an internal error and cannot be corrected by
                        users. Contact technical support and report this problem.
                        """
                        return -result
                else:
                    output_error(
                        f"PT_KEYWORD not supported after property '{Class.class_get_property_typename(last.ptype)} {last.name}' in enduse.publish")

    def test(self):
        failed = 0
        ok = 0
        error_count = 0

        class Test:
            def __init__(self, name):
                self.name = name

        tests = [Test("TODO")]

        print("\nBEGIN: enduse tests")

        for test in tests:
            pass
            # Perform test

        if failed:
            output_error("endusetest: %d enduse tests failed--see test.txt for more information", failed)
            print("!!! %d enduse tests failed, %d errors found" % (failed, error_count))
        else:
            output_verbose("%d enduse tests completed with no errors--see test.txt for details", ok)
            print("endusetest: %d schedule tests completed, %d errors found" % (ok, error_count))

        print("END: enduse tests")
        return failed

    def get_part(self, x, name):
        e = x
        def do_double(X, Y=None):
            if not Y:
                Y = X
            if name == Y:
                return getattr(e, X)

        def do_complex(X, Y=None):
            if not Y:
                Y = X
            if name == Y + ".real":
                return e.X.Re()
            if name == Y + ".imag":
                return e.X.Im()
            if name == Y + ".mag":
                return e.X.Mag()
            if name == Y + ".arg":
                return e.X.Arg()
            if name == Y + ".ang":
                return e.X.Arg() * 180 / math.pi

        def do_motor(X):
            IND = EUMOTORTYPE._EUMT_COUNT
            if X == "A":
                IND = EUMOTORTYPE.EUMT_MOTOR_A
            elif X== "B":
                IND = EUMOTORTYPE.EUMT_MOTOR_B
            elif X == "C":
                IND = EUMOTORTYPE.EUMT_MOTOR_C
            elif X == "D":
                IND = EUMOTORTYPE.EUMT_MOTOR_D
            else:
                raise Exception("wrong motor type")
            do_complex(self.motor[IND].power, "motor"+X+".power")
            do_complex(self.motor[IND].impedance, "motor"+X+".impedance")
            do_double(self.motor[IND].inertia, "motor"+X+".inertia")
            do_double(self.motor[IND].v_stall, "motor"+X+".v_stall")
            do_double(self.motor[IND].v_start, "motor"+X+".v_start")
            do_double(self.motor[IND].v_trip, "motor"+X+".v_trip")
            do_double(self.motor[IND].t_trip, "motor"+X+".t_trip")

        def do_electronic(X):
            IND = EUMOTORTYPE._EUMT_COUNT
            if X == "A":
                IND = EUMOTORTYPE.EUMT_MOTOR_A
            elif X== "B":
                IND = EUMOTORTYPE.EUMT_MOTOR_B
            elif X == "C":
                IND = EUMOTORTYPE.EUMT_MOTOR_C
            elif X == "D":
                IND = EUMOTORTYPE.EUMT_MOTOR_D
            else:
                raise Exception("wrong motor type")
            do_complex(self.electronic[IND].power, "electronic"+X+".power")
            do_double(self.electronic[IND].inertia, "electronic"+X+".inertia")
            do_double(self.electronic[IND].v_trip, "electronic"+X+".v_trip")
            do_double(self.electronic[IND].v_start, "electronic"+X+".v_start")
        do_complex(self.total)
        do_complex(self.energy)
        do_complex(self.demand)
        do_double(self.breaker_amps)
        do_complex(self.admittance)
        do_complex(self.current)
        do_complex(self.power)
        do_double(self.impedance_fraction)
        do_double(self.current_fraction)
        do_double(self.power_fraction)
        do_double(self.power_factor)
        do_double(self.voltage_factor)
        do_double(self.heatgain)
        do_double(self.heatgain_fraction)
        do_motor("A")
        do_motor("B")
        do_motor("C")
        do_motor("D")
        do_electronic("A")
        do_electronic("B")
        return QNAN


class EnduseSync:
    def __init__(self):
        self.start_ed = None
        self.startlock_ed = None
        self.done_ed = None
        self.donelock_ed = None
        self.next_t1_ed, self.next_t2_ed = 0, 0
        self.donecount_ed = 0
        self.run = 0
        self.enduse_synctime = 0

    def syncproc(self, ptr):
        data = ptr
        e = None
        n = 0
        t2 = 0
        while data.ok:
            pass
        return None

    def syncall(self, t1):
        global global_threadcount, enduse_synctime, run
        n_threads_ed = 0
        thread_ed = None
        t2 = float('inf')
        ts = 0
        if n_enduses == 0:
            return float('inf')
        if n_threads_ed == 0:
            enduse = None
            n_items, en = 0, 0
            print("enduse_syncall setting up for %d enduses" % n_enduses)
            n_threads_ed = global_threadcount
            if n_threads_ed > 1:
                n = 0
                if n_enduses < n_threads_ed*4:
                    n_threads_ed = n_enduses//4
                if n_threads_ed == 0:
                    n_threads_ed = 1
                n_items = n_enduses // n_threads_ed
                n_threads_ed = n_enduses // n_items
                if n_threads_ed*n_items < n_enduses:
                    n_threads_ed += 1
                print("enduse_syncall is using %d of %d available threads" % (n_threads_ed, global_threadcount))
                print("enduse_syncall is assigning %d enduses per thread" % n_items)
                thread_ed = [EnduseSyncData() for _ in range(n_threads_ed)]
                for e in enduse_list:
                    if thread_ed[en].ne == n_items:
                        en += 1
                    if thread_ed[en].ne == 0:
                        thread_ed[en].e = e
                    thread_ed[en].ne += 1
                for n in range(n_threads_ed):
                    pass
        if n_threads_ed < 2:
            pass
        else:
            donecount_ed = n_threads_ed
            next_t1_ed = t1
            next_t2_ed = float('inf')
            run += 1
            while donecount_ed > 0:
                pass
            print("passed donecount==0 condition")
            if next_t2_ed < t2:
                t2 = next_t2_ed
        enduse_synctime += exec_clock()
        enduse_synctime -= ts
        return t2


    def convert_from(self, string, size, data, prop):
        pass

    def publish(self, oclass, struct_address, prefix):
        pass

    def convert_to_struct(self, string, data, props):
        pass

    def convert_to_enduse(self, string, data, prop):
        e = data
        buffer = [""] * 1024
        token = None
        if string[0] == '{':
            unit = unit_find("kVA")
            eus = [
                PROPERTY(None, "total", PROPERTYTYPE.PT_complex, 0, 0, PROPERTYACCESS.PA_PUBLIC, unit, e.total, None, None, None, prop.next()),
                PROPERTY(None, "energy", PROPERTYTYPE.PT_complex, 0, 0, PROPERTYACCESS.PA_PUBLIC, unit, e.energy, None, None, None, prop.next()),
                PROPERTY(None, "demand", PROPERTYTYPE.PT_complex, 0, 0, PROPERTYACCESS.PA_PUBLIC, unit, e.demand, None, None, None, prop.next())
            ]  
            return self.convert_to_struct(string, data, eus)


