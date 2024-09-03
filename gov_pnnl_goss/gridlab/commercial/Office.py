import math

from gov_pnnl_goss.gridlab.climate.Climate import gl_find_objects, gl_find_next, COMPASS_PTS
# 	@file office.cpp
# 	@defgroup office Single-zone office building
# 	@ingroup commercial
#
# 	The building simultion uses a single zone ETP model with first order ODEs:
#
# 	\f[ T'_i = \frac{1}{c_a} \left[ T_m U_m - T_i (U_a+U_m) + T_o U_a + \Sigma Q_x \right] \f]
#
# 	\f[ T'_m = \frac{U_m}{c_m} \left[ T_i - T_m \right] \f]
#
#  where:
#  - \f$T_i\f$ is the temperature of the air inside the building
#  - \f$T'_i\f$ is \f$\frac{d}{dt}T_i\f$
#  - \f$T_m\f$ is the temperature of the mass inside the buildnig (e.g, furniture, inside walls etc)
#  - \f$T'_m\f$ is \f$\frac{d}{dt}T_m\f$
#  - \f$T_o\f$ is the ambient temperature outside air
#  - \f$U_a\f$ is the UA of the building itself
#  - \f$U_m\f$ is the UA of the mass of the furniture, inside walls etc
#  - \f$c_m\f$ is the heat capacity of the mass of the furniture inside the walls etc
#  - \f$c_a\f$ is the heat capacity of the air inside the building
#  - \f$Q_i\f$ is the heat rate from internal heat gains of the building (e.g., plugs, lights, people)
#  - \f$Q_h\f$ is the heat rate from HVAC unit
#  - \f$Q_s\f$ is the heat rate from the sun (solar heating through windows etc)
#
#  General first order ODEs (with \f$C_1 - C_5\f$ defined by inspection above):
#
#     \f[ T'_i = T_i C_1 + T_m C_2 + C_3 \f]
#     \f[ T'_m = T_i C_4 + T_m C_5 \f]
#
#  where
# 	- \f$ C_1 = - (U_a+U_m) / c_a \f$
# 	- \f$ C_2 = U_m / c_a \f$
# 	- \f$ C_3 = (\Sigma Q_x + U_a T_o) / c_a \f$
# 	- \f$ C_4 = U_m / c_m \f$
# 	- \f$ C_5 = - U_m / c_m \f$
#
#  General form of second order ODE
#
#     \f[ p_4 = p_1 T"_i + p_2 T'_i + p_3 T_i \f]
#
#  where
#
#    - \f$ p_1 = 1 / C_2 \f$
#    - \f$ p_2 = -C_5 / C_2 - C_1 / C_2 \f$
#    - \f$ p_3 = C_5 C_1 / C_2 - C_4 \f$
#    - \f$ p_4 = -C_5 C_3 / C_2\f$
#
#  Solution to second order ODEs for indoor and mass temperatures are
#
#     \f[ T_i(t) = K_1 e^{r_1 t} +  K_1 e^{r_2 t} + \frac{p4}{p3} \f]
#
# 	\f[ T_m(t) = \frac{T'_i(t) - C_1 T_i(t) - C_3}{C_2} \f]
#
#  where:
#
#    - \f$ r_1,r_2 = roots(p_1 p_2 p_3) \f$
#    - \f$ K_1 = \frac{r_1 T_{i,0} - r_1 \frac{p_4}{p_3} - T'_{i,0}}{r_2-r_1} \f$
#    - \f$ K_2 = \frac{T_{i,0} - r_2 K_2}{r_1} \f$
#    - \f$t\f$ is the elapsed time
#    - \f$T_i(t)\f$ is the temperature of the air inside the building at time \f$t\f$
#    - \f$T_{i,0}\f$ is \f$T_i(t=0)\f$, e.g initial temperature of the air inside the building
#    - \f$T'_{i,0}\f$ is \f$T'_i(t=0)\f$ e.g the initial temperature gradient of the air inside the building


from gov_pnnl_goss.gridlab.climate.CsvReader import PADDR
from gov_pnnl_goss.gridlab.comm.NetworkMessage import OBJECTHDR
from gov_pnnl_goss.gridlab.gldcore.Find import FindType, FindOp
from gov_pnnl_goss.gridlab.gldcore.Globals import TECHNOLOGYREADINESSLEVEL
from gov_pnnl_goss.gridlab.gldcore.GridLabD import gl_publish_variable, PC_PRETOPDOWN, PC_BOTTOMUP, TS_NEVER, gl_warning
from gov_pnnl_goss.gridlab.gldcore.PropertyHeader import PropertyType


class HCMODE:
    OFF = 0
    HEAT = 1
    AUX = 2
    COOL = 3
    ECON = 4
    VENT = 5


class ENDUSE:
    def __init__(self):
        self.power_factor = 0.0
        self.energy = complex(0, 0)
        self.power = complex(0, 0)
        self.demand = complex(0, 0)
        self.constant_power = complex(0, 0)
        self.constant_current = complex(0, 0)
        self.constant_admittance = complex(0, 0)
        self.heatgain = 0.0
        self.heatgain_fraction = 0.0


class HVACDESIGN:
    def __init__(self):
        self.design_temperature = 0.0
        self.balance_temperature = 0.0
        self.efficiency = 0.0
        self.cop = 0.0
        self.capacity = 0.0
        self.capacity_perF = 0.0


class HVAC:
    def __init__(self):
        self.enduse = ENDUSE()
        self.mode = HCMODE.OFF
        self.cooling = HVACDESIGN()
        self.heating = HVACDESIGN()
        self.minimum_ach = 0.0


class LIGHTS:
    def __init__(self):
        self.enduse = ENDUSE()
        self.capacity = 0.0
        self.fraction = 0.0


class PLUGS:
    def __init__(self):
        self.enduse = ENDUSE()
        self.capacity = 0.0
        self.fraction = 0.0


class CONDITIONS:
    def __init__(self):
        self.pTemperature = [0.0]  # List with one element for compatibility with the C code
        self.pHumidity = [0.0]  # List with one element for compatibility with the C code
        self.pSolar = [0.0]  # List with one element for compatibility with the C code
        self.out_temp = 0.0
        self.air_temperature = 0.0
        self.mass_temperature = 0.0
        self.occupancy = 0.0
        self.temperature_change = 0.0


class CONTROLS:
    def __init__(self):
        self.cooling_setpoint = 0.0
        self.economizer_cutin = 0.0
        self.heating_setpoint = 0.0
        self.auxiliary_cutin = 0.0
        self.setpoint_deadband = 0.0
        self.ventilation_fraction = 0.0
        self.lighting_fraction = 0.0


class FEATURES:
    def __init__(self):
        self.floor_area = 0.0
        self.floor_height = 0.0
        self.exterior_ua = 0.0
        self.interior_ua = 0.0
        self.interior_mass = 0.0
        self.window_area = [0.0] * 9
        self.glazing_coeff = 0.0
        self.occupants = 0.0
        self.schedule =  ""


class ZONEDATA:
    def __init__(self):
        self.design = FEATURES()
        self.hvac = HVAC()
        self.lights = LIGHTS()
        self.plugs = PLUGS()
        self.total = ENDUSE()
        self.current = CONDITIONS()
        self.control = CONTROLS()


class Office:
    oclass = None
    defaults = None
    warn_low_temp = 50.0
    warn_high_temp = 90.0
    warn_control = True

    def __init__(self, module):
        # Initialize other attributes here
        self.Qh = 0.0
        self.Qi = 0.0
        self.Qs = 0.0
        self.Qz = 0.0
        self.Teq = 0.0
        self.Tevent = 0.0

        self.TheatOff = 0.0
        self.Theat_off = 0.0

        self.TheatOn = 0.0
        self.Theat_on = None

        self.TcoolOff = 0.0
        self.Tcool_off = 0.0

        self.TcoolOn = 0.0
        self.Tcool_on = 0.0
        self.Teq = 0.0

        self.c1 = 0.0
        self.c2 = 0.0
        self.c3 = 0.0
        self.c4 = 0.0
        self.c5 = 0.0
        self.c6 = 0.0
        self.c7 = 0.0
        self.cooling_mode = True  # Update based on requirements
        self.cop = 0.0
        self.dTi = 0.0
        self.defaults = None
        self.k1 = 0.0
        self.k2 = 0.0
        self.module = module
        self.occupied = [0] * 24
        self.oclass = None
        self.pCurrent = None
        self.pVoltage = None
        self.r1 = 0.0
        self.r2 = 0.0
        self.tcool_off = None
        self.tcool_on = None
        self.theat_off = None
        self.theat_on = None
        self.warn_control = True  # Update based on requirements
        self.warn_high_temp = 90.0
        self.warn_low_temp = 50.0
        self.zone = ZONEDATA()  # Assuming zone is an instance of another class

        if Office.oclass is None:
            Office.oclass = gld_class.create(
                module, "office", 0, PC_PRETOPDOWN | PC_BOTTOMUP | PC_AUTOLOCK
            )
            if Office.oclass is None:
                raise Exception("Unable to register class office")
            Office.oclass.trl = TECHNOLOGYREADINESSLEVEL.TRL_DEMONSTRATED
            Office.defaults = self

            if gl_publish_variable(
                    Office.oclass,
                    PropertyType.PT_double, "floor_area[sf]", PADDR(self.zone.design.floor_area),
                    PropertyType.PT_double, "floor_height[ft]", PADDR(self.zone.design.floor_height),
                    PropertyType.PT_double, "exterior_ua[Btu/degF/h]", PADDR(self.zone.design.exterior_ua),
                    PropertyType.PT_double, "interior_ua[Btu/degF/h]", PADDR(self.zone.design.interior_ua),
                    PropertyType.PT_double, "interior_mass[Btu/degF]", PADDR(self.zone.design.interior_mass),
                    PropertyType.PT_double, "glazing[sf]", PADDR(self.zone.design.window_area[0]),
                    PropertyType.PT_SIZE, 0, # sizeof(self.zone.design.window_area) / sizeof(self.zone.design.window_area[0]),
                    PropertyType.PT_double, "glazing.north[sf]", PADDR(self.zone.design.window_area[COMPASS_PTS.CP_N]),
                    PropertyType.PT_double, "glazing.northeast[sf]", PADDR(self.zone.design.window_area[COMPASS_PTS.CP_NE]),
                    PropertyType.PT_double, "glazing.east[sf]", PADDR(self.zone.design.window_area[COMPASS_PTS.CP_E]),
                    PropertyType.PT_double, "glazing.southeast[sf]", PADDR(self.zone.design.window_area[COMPASS_PTS.CP_SE]),
                    PropertyType.PT_double, "glazing.south[sf]", PADDR(self.zone.design.window_area[COMPASS_PTS.CP_S]),
                    PropertyType.PT_double, "glazing.southwest[sf]", PADDR(self.zone.design.window_area[COMPASS_PTS.CP_SW]),
                    PropertyType.PT_double, "glazing.west[sf]", PADDR(self.zone.design.window_area[COMPASS_PTS.CP_W]),
                    PropertyType.PT_double, "glazing.northwest[sf]", PADDR(self.zone.design.window_area[COMPASS_PTS.CP_NW]),
                    PropertyType.PT_double, "glazing.horizontal[sf]", PADDR(self.zone.design.window_area[COMPASS_PTS.CP_H]),
                    PropertyType.PT_double, "glazing.coefficient[pu]", PADDR(self.zone.design.glazing_coeff),
                    PropertyType.PT_double, "occupancy", PADDR(self.zone.current.occupancy),
                    PropertyType.PT_double, "occupants", PADDR(self.zone.design.occupants),
                    PropertyType.PT_char256, "schedule", PADDR(self.zone.design.schedule),
                    PropertyType.PT_double, "air_temperature[degF]", PADDR(self.zone.current.air_temperature),
                    PropertyType.PT_double, "mass_temperature[degF]", PADDR(self.zone.current.mass_temperature),
                    PropertyType.PT_double, "temperature_change[degF/h]", PADDR(self.zone.current.temperature_change),
                    PropertyType.PT_double, "outdoor_temperature[degF]", PADDR(self.zone.current.out_temp),
                    PropertyType.PT_double, "Qh[Btu/h]", PADDR(self.Qh),
                    PropertyType.PT_double, "Qs[Btu/h]", PADDR(self.Qs),
                    PropertyType.PT_double, "Qi[Btu/h]", PADDR(self.Qi),
                    PropertyType.PT_double, "Qz[Btu/h]", PADDR(self.Qz),
                    PropertyType.PT_enumeration, "hvac_mode", PADDR(self.zone.hvac.mode),
                    PropertyType.PT_KEYWORD, "HEAT", HCMODE.HEAT,
                    PropertyType.PT_KEYWORD, "AUX", HCMODE.AUX,
                    PropertyType.PT_KEYWORD, "COOL", HCMODE.COOL,
                    PropertyType.PT_KEYWORD, "ECON", HCMODE.ECON,
                    PropertyType.PT_KEYWORD, "VENT", HCMODE.VENT,
                    PropertyType.PT_KEYWORD, "OFF", HCMODE.OFF,
                    PropertyType.PT_double, "hvac.cooling.balance_temperature[degF]",
                    PADDR(self.zone.hvac.cooling.balance_temperature),
                    PropertyType.PT_double, "hvac.cooling.capacity[Btu/h]", PADDR(self.zone.hvac.cooling.capacity),
                    PropertyType.PT_double, "hvac.cooling.capacity_perF[Btu/degF/h]",
                    PADDR(self.zone.hvac.cooling.capacity_perF),
                    PropertyType.PT_double, "hvac.cooling.design_temperature[degF]",
                    PADDR(self.zone.hvac.cooling.design_temperature),
                    PropertyType.PT_double, "hvac.cooling.efficiency[pu]", PADDR(self.zone.hvac.cooling.efficiency),
                    PropertyType.PT_double, "hvac.cooling.cop[pu]", PADDR(self.zone.hvac.cooling.cop),
                    PropertyType.PT_double, "hvac.heating.balance_temperature[degF]",
                    PADDR(self.zone.hvac.heating.balance_temperature),
                    PropertyType.PT_double, "hvac.heating.capacity[Btu/h]", PADDR(self.zone.hvac.heating.capacity),
                    PropertyType.PT_double, "hvac.heating.capacity_perF[Btu/degF/h]",
                    PADDR(self.zone.hvac.heating.capacity_perF),
                    PropertyType.PT_double, "hvac.heating.design_temperature[degF]",
                    PADDR(self.zone.hvac.heating.design_temperature),
                    PropertyType.PT_double, "hvac.heating.efficiency[pu]", PADDR(self.zone.hvac.heating.efficiency),
                    PropertyType.PT_double, "hvac.heating.cop[pu]", PADDR(self.zone.hvac.heating.cop),
                    PropertyType.PT_double, "lights.capacity[kW]", PADDR(self.zone.lights.capacity),
                    PropertyType.PT_double, "lights.fraction[pu]", PADDR(self.zone.lights.fraction),
                    PropertyType.PT_double, "plugs.capacity[kW]", PADDR(self.zone.plugs.capacity),
                    PropertyType.PT_double, "plugs.fraction[pu]", PADDR(self.zone.plugs.fraction),
                    PropertyType.PT_complex, "demand[kW]", PADDR(self.zone.total.demand),
                    PropertyType.PT_complex, "total_load[kW]", PADDR(self.zone.total.power),
                    PropertyType.PT_complex, "energy[kWh]", PADDR(self.zone.total.energy),
                    PropertyType.PT_double, "power_factor", PADDR(self.zone.total.power_factor),
                    PropertyType.PT_complex, "power[kW]", PADDR(self.zone.total.constant_power),
                    PropertyType.PT_complex, "current[A]", PADDR(self.zone.total.constant_current),
                    PropertyType.PT_complex, "admittance[1/Ohm]", PADDR(self.zone.total.constant_admittance),
                    PropertyType.PT_complex, "hvac.demand[kW]", PADDR(self.zone.hvac.enduse.demand),
                    PropertyType.PT_complex, "hvac.load[kW]", PADDR(self.zone.hvac.enduse.power),
                    PropertyType.PT_complex, "hvac.energy[kWh]", PADDR(self.zone.hvac.enduse.energy),
                    PropertyType.PT_double, "hvac.power_factor", PADDR(self.zone.hvac.enduse.power_factor),
                    PropertyType.PT_complex, "lights.demand[kW]", PADDR(self.zone.lights.enduse.demand),
                    PropertyType.PT_complex, "lights.load[kW]", PADDR(self.zone.lights.enduse.power),
                    PropertyType.PT_complex, "lights.energy[kWh]", PADDR(self.zone.lights.enduse.energy),
                    PropertyType.PT_double, "lights.power_factor", PADDR(self.zone.lights.enduse.power_factor),
                    PropertyType.PT_double, "lights.heatgain_fraction", PADDR(self.zone.lights.enduse.heatgain_fraction),
                    PropertyType.PT_double, "lights.heatgain[kW]", PADDR(self.zone.lights.enduse.heatgain),
                    PropertyType.PT_complex, "plugs.demand[kW]", PADDR(self.zone.plugs.enduse.demand),
                    PropertyType.PT_complex, "plugs.load[kW]", PADDR(self.zone.plugs.enduse.power),
                    PropertyType.PT_complex, "plugs.energy[kWh]", PADDR(self.zone.plugs.enduse.energy),
                    PropertyType.PT_double, "plugs.power_factor", PADDR(self.zone.plugs.enduse.power_factor),
                    PropertyType.PT_double, "plugs.heatgain_fraction", PADDR(self.zone.plugs.enduse.heatgain_fraction),
                    PropertyType.PT_double, "plugs.heatgain[kW]", PADDR(self.zone.plugs.enduse.heatgain),
                    PropertyType.PT_double, "cooling_setpoint[degF]", PADDR(self.zone.control.cooling_setpoint),
                    PropertyType.PT_double, "heating_setpoint[degF]", PADDR(self.zone.control.heating_setpoint),
                    PropertyType.PT_double, "thermostat_deadband[degF]", PADDR(self.zone.control.setpoint_deadband),
                    PropertyType.PT_double, "control.ventilation_fraction", PADDR(self.zone.control.ventilation_fraction),
                    PropertyType.PT_double, "control.lighting_fraction", PADDR(self.zone.control.lighting_fraction),
                    PropertyType.PT_double, "ACH", PADDR(self.zone.hvac.minimum_ach),
                    None,
            ) < 1:
                raise Exception("Unable to publish properties in " + __file__)

            # memset(Office.defaults, 0, sizeof(Office))

            # Set default power factors
            self.zone.lights.enduse.power_factor = 1.0
            self.zone.plugs.enduse.power_factor = 1.0
            self.zone.hvac.enduse.power_factor = 1.0

            # Set default climate to static values
            Tout = 59
            RHout = 0.75
            Solar = [0, 0, 0, 0, 0, 0, 0, 0, 0]
            self.zone.current.pTemperature = Tout
            self.zone.current.pHumidity = RHout
            self.zone.current.pSolar = Solar

            # Set default thermal conditions
            self.zone.current.air_temperature = Tout
            self.zone.current.mass_temperature = Tout

            # Set default control strategy
            self.zone.control.heating_setpoint = 70
            self.zone.control.cooling_setpoint = 75
            self.zone.control.setpoint_deadband = 1
            self.zone.control.ventilation_fraction = 1
            self.zone.control.lighting_fraction = 0.5

        if self.oclass is None:
            self.oclass = gld_class.create(module, "office", 0, # sizeof(Office),
                                                     PC_PRETOPDOWN | PC_BOTTOMUP | PC_AUTOLOCK)
            if self.oclass is None:
                raise Exception("unable to register class office")
            self.oclass.trl = TECHNOLOGYREADINESSLEVEL.TRL_DEMONSTRATED
            self.defaults = self
            #memset(self.defaults, 0, sizeof(Office))
            self.zone.lights.enduse.power_factor = 1.0
            self.zone.plugs.enduse.power_factor = 1.0
            self.zone.hvac.enduse.power_factor = 1.0

            static_Tout = 59
            static_RHout = 0.75
            static_Solar = [0, 0, 0, 0, 0, 0, 0, 0, 0]
            self.zone.current.pTemperature = static_Tout
            self.zone.current.pHumidity = static_RHout
            self.zone.current.pSolar = static_Solar

            self.zone.current.air_temperature = static_Tout
            self.zone.current.mass_temperature = static_Tout

            self.zone.control.heating_setpoint = 70
            self.zone.control.cooling_setpoint = 75
            self.zone.control.setpoint_deadband = 1
            self.zone.control.ventilation_fraction = 1
            self.zone.control.lighting_fraction = 0.5

    def create(self):
        return 1

    def init(self, parent):
        oversize = 1.2
        self.update_control_setpoints()

        if self.zone.design.floor_area == 0:
            self.zone.design.floor_area = 10000
        if self.zone.design.floor_height == 0:
            self.zone.design.floor_height = 9
        if self.zone.design.interior_mass == 0:
            self.zone.design.interior_mass = 40000
        if self.zone.design.interior_ua == 0:
            self.zone.design.interior_ua = 1
        if self.zone.design.exterior_ua == 0:
            self.zone.design.exterior_ua = 0.375

        if self.zone.hvac.cooling.design_temperature == 0:
            self.zone.hvac.cooling.design_temperature = 93  # Pittsburgh, PA
        if self.zone.hvac.heating.design_temperature == 0:
            self.zone.hvac.heating.design_temperature = -6  # Pittsburgh, PA

        if self.zone.hvac.minimum_ach == 0:
            self.zone.hvac.minimum_ach = 1.5
        if self.zone.control.economizer_cutin == 0:
            self.zone.control.economizer_cutin = 60
        if self.zone.control.auxiliary_cutin == 0:
            self.zone.control.auxiliary_cutin = 2

        if self.zone.design.schedule == "":
            self.zone.design.schedule = "1-5 8-17"
        occupancy_schedule(self.zone.design.schedule, self.occupied)

        if self.zone.hvac.heating.capacity == 0:
            self.zone.hvac.heating.capacity = (oversize
                                               * (self.zone.design.exterior_ua
                                                  * (self.zone.control.heating_setpoint
                                                     - self.zone.hvac.heating.design_temperature)
                                                  + (self.zone.hvac.heating.design_temperature
                                                     - self.zone.control.heating_setpoint)
                                                  * (0.2402 * 0.0735 * self.zone.design.floor_height
                                                     * self.zone.design.floor_area)
                                                  * self.zone.hvac.minimum_ach))
        if self.zone.hvac.cooling.capacity == 0:
            self.zone.hvac.cooling.capacity = (oversize
                                               * (-self.zone.design.exterior_ua
                                                  * (self.zone.hvac.cooling.design_temperature
                                                     - self.zone.control.cooling_setpoint)
                                                  - (self.zone.design.window_area[0]
                                                     + self.zone.design.window_area[1]
                                                     + self.zone.design.window_area[2]
                                                     + self.zone.design.window_area[3]
                                                     + self.zone.design.window_area[4]
                                                     + self.zone.design.window_area[5]
                                                     + self.zone.design.window_area[6]
                                                     + self.zone.design.window_area[7]
                                                     + self.zone.design.window_area[8])
                                                  * 100 * 3.412 * self.zone.design.glazing_coeff
                                                  - (self.zone.hvac.cooling.design_temperature
                                                     - self.zone.control.cooling_setpoint)
                                                  * (0.2402 * 0.0735 * self.zone.design.floor_height
                                                     * self.zone.design.floor_area)
                                                  * self.zone.hvac.minimum_ach
                                                  - (self.zone.lights.capacity + self.zone.plugs.capacity) * 3.412))
        if self.zone.hvac.cooling.cop == 0:
            self.zone.hvac.cooling.cop = -3
        if self.zone.hvac.heating.cop == 0:
            self.zone.hvac.heating.cop = 1.25

        hdr = OBJECTHDR(self)

        # link to climate data
        climates = gl_find_objects(FL_NEW, FindType.FT_CLASS, FindOp.SAME, "climate", FindType.FT_END)
        if climates == None:
            gl_warning("office: no climate data found, using static data")
        elif climates.hit_count > 1:
            gl_warning("house: %d climates found, using first one defined" % climates.hit_count)
        if climates.hit_count > 0:
            obj = gl_find_next(climates, None)
            if obj.rank <= hdr.rank:
                gl_set_dependent(obj, hdr)
            self.zone.current.p_temperature = float(gl_get_property(obj, "temperature"))
            self.zone.current.p_humidity = float(gl_get_property(obj, "humidity"))
            self.zone.current.p_solar = float(gl_get_property(obj, "solar_flux"))

        map = [
            {"desc": "floor height is not valid", "test": self.zone.design.floor_height <= 0},
            {"desc": "interior mass is not valid", "test": self.zone.design.interior_mass <= 0},
            {"desc": "interior UA is not valid", "test": self.zone.design.interior_ua <= 0},
            {"desc": "exterior UA is not valid", "test": self.zone.design.exterior_ua <= 0},
            {"desc": "floor area is not valid", "test": self.zone.design.floor_area <= 0},
            {"desc": "control setpoint deadpoint is invalid", "test": self.zone.control.setpoint_deadband <= 0},
            {"desc": "heating and cooling setpoints conflict", "test": self.TheatOn >= self.TcoolOff},
            {"desc": "cooling capacity is not negative", "test": self.zone.hvac.cooling.capacity >= 0},
            {"desc": "heating capacity is not positive", "test": self.zone.hvac.heating.capacity <= 0},
            {"desc": "cooling cop is not negative", "test": self.zone.hvac.cooling.cop >= 0},
            {"desc": "heating cop is not positive", "test": self.zone.hvac.heating.cop <= 0},
            {"desc": "minimum ach is not positive", "test": self.zone.hvac.minimum_ach <= 0},
            {"desc": "auxiliary cutin is not positive", "test": self.zone.control.auxiliary_cutin <= 0},
            {"desc": "economizer cutin is above cooling setpoint deadband",
             "test": self.zone.control.economizer_cutin >= self.zone.control.cooling_setpoint - self.zone.control.setpoint_deadband},
        ]
        for m in map:
            if m["test"]:
                raise m["desc"]

        return 1

    def presync(self, t1):
        t0 = self.get_clock()
        dt = DATETIME()

        self.Qz = 0

        self.zone.current.out_temp = self.zone.current.p_temperature[0]

        if t0 > 0:
            day = gl_getweekday(t0)
            hour = gl_gethour(t0)

            gl_localtime(t0, dt)

            if self.zone.design.schedule[0] != '':
                self.zone.current.occupancy = IS_OCCUPIED(day, hour)

        return TS_NEVER

    def update_control_setpoints(self):
        self.tcool_on = self.zone.control.cooling_setpoint + self.zone.control.setpoint_deadband
        self.tcool_off = self.zone.control.cooling_setpoint - self.zone.control.setpoint_deadband
        self.theat_on = self.zone.control.heating_setpoint - self.zone.control.setpoint_deadband
        self.theat_off = self.zone.control.heating_setpoint + self.zone.control.setpoint_deadband
        if self.tcool_off - self.theat_off <= 0:  # deadband needs to be smaller/ setpoints need to be farther apart
            raise ValueError("thermostat deadband causes heating/cooling turn-off points to overlap")
        self.zone.control.ventilation_fraction =  self.zone.hvac.minimum_ach if self.zone.current.occupancy > 0 else 0

    def update_lighting(self, t1: float) -> float:
        t0 = self.get_clock()

        # power calculation
        self.zone.lights.enduse.power.set_power_factor(self.zone.lights.capacity *
                                                       self.zone.lights.fraction,
                                                       self.zone.lights.enduse.power_factor, 'J')
        # energy calculation
        if 0 < t0 < t1:
            self.zone.lights.enduse.energy += self.zone.lights.enduse.power * self.gl_tohours(t1 - t0)
        # heatgain calculation
        self.zone.lights.enduse.heatgain = self.zone.lights.enduse.power.mag() * self.zone.lights.enduse.heatgain_fraction
        return TS_NEVER

    def update_plugs(self, t1):
        t0 = self.get_clock()

        # power calculation
        self.zone.plugs.enduse.power.set_power_factor(self.zone.plugs.capacity *
                                                      self.zone.plugs.fraction, self.zone.plugs.enduse.power_factor, J)

        # energy calculation
        if 0 < t0 < t1:
            self.zone.plugs.enduse.energy += self.zone.plugs.enduse.power * gl_tohours(t1 - t0)

        # heatgain calculation
        self.zone.plugs.enduse.heatgain = self.zone.plugs.enduse.power.mag() * self.zone.plugs.enduse.heatgain_fraction

        return TS_NEVER

    def update_hvac(self):
        Ti = self.zone.current.air_temperature
        dTi = self.zone.current.temperature_change
        Tout = self.zone.current.p_temperature
        Trange = 40
        Taux = self.zone.hvac.heating.balance_temperature - Trange
        Tecon = self.zone.hvac.cooling.balance_temperature
        Tbal_heat = self.zone.hvac.heating.balance_temperature
        Tmax_cool = self.zone.hvac.cooling.design_temperature
        mode = self.zone.hvac.mode

        Qvent = 0
        Qactive = 0
        cop = 0
        Tevent = 0

        if mode == HCMODE.OFF:
            cop = 0
            Qactive = Qvent = 0
            if dTi < 0 and Ti < self.Tcool_on:
                Tevent = self.Theat_on
            elif dTi > 0 and Ti > self.Theat_on:
                Tevent = self.Tcool_on
            else:
                Tevent = self.Teq
        elif mode == HCMODE.HEAT:
            cop = 1.0 + (self.zone.hvac.heating.cop - 1) * (Tout - Taux) / Trange
            Qactive = self.zone.hvac.heating.capacity + self.zone.hvac.heating.capacity_perF * (
                        self.zone.hvac.heating.balance_temperature - Tout)
            Qvent = (self.zone.current.p_temperature - self.zone.current.air_temperature) * (
                        0.2402 * 0.0735 * self.zone.design.floor_height * self.zone.design.floor_area) * self.zone.control.ventilation_fraction
            Tevent = self.Theat_off
        elif mode == HCMODE.AUX:
            cop = 1.0
            Qactive = self.zone.hvac.heating.capacity
            Qvent = (self.zone.current.p_temperature - self.zone.current.air_temperature) * (
                        0.2402 * 0.0735 * self.zone.design.floor_height * self.zone.design.floor_area) * self.zone.control.ventilation_fraction
            Tevent = self.Theat_off
        elif mode == HCMODE.COOL:
            cop = -1.0 - (self.zone.hvac.cooling.cop + 1) * (Tout - Tmax_cool) / (Tmax_cool - Tecon)
            Qactive = self.zone.hvac.cooling.capacity - self.zone.hvac.cooling.capacity_perF * (
                        Tout - self.zone.hvac.cooling.balance_temperature)
            Qvent = (self.zone.current.p_temperature - self.zone.current.air_temperature) * (
                        0.2402 * 0.0735 * self.zone.design.floor_height * self.zone.design.floor_area) * self.zone.control.ventilation_fraction
            Tevent = self.Tcool_off
        elif mode == HCMODE.VENT:
            cop = 0
            Qactive = 0
            Qvent = (self.zone.current.p_temperature - self.zone.current.air_temperature) * (
                        0.2402 * 0.0735 * self.zone.design.floor_height * self.zone.design.floor_area) * self.zone.control.ventilation_fraction
            if dTi < 0 and Ti < self.Tcool_on:
                Tevent = self.Theat_on
            elif dTi > 0 and Ti > self.Theat_on:
                Tevent = self.Tcool_on
            else:
                Tevent = self.Teq
        elif mode == HCMODE.ECON:
            cop = 0.0
            Qactive = 0
            Qvent = (self.zone.current.p_temperature - self.zone.current.air_temperature) * (
                        0.2402 * 0.0735 * self.zone.design.floor_height * self.zone.design.floor_area) * self.zone.control.ventilation_fraction
            Tevent = self.Tcool_off
        else:
            raise ValueError('hvac mode is invalid')

        if Qactive != 0:
            self.zone.hvac.enduse.power.set_power_factor(Qactive / cop / 1000, self.zone.hvac.enduse.power_factor)
        else:
            self.zone.hvac.enduse.power = gld.complex(0, 0)

        if Qvent != 0:
            self.zone.hvac.enduse.power += gld.complex(0.1, -0.01) / 1000 * self.zone.design.floor_area

        self.zone.hvac.enduse.energy += self.zone.hvac.enduse.power
        if self.zone.hvac.enduse.power.real < 0:
            raise ValueError('hvac unit is generating electricity')
        elif not math.isfinite(self.zone.hvac.enduse.power.real) or not math.isfinite(self.zone.hvac.enduse.power.imag):
            raise ValueError('hvac power is not finite')

        return Qvent + Qactive

    def plc(self, t1):
        t0 = self.get_clock()

        Tout = self.zone.current.p_temperature
        Tair = self.zone.current.air_temperature
        Tmass = self.zone.current.mass_temperature
        Tecon = self.zone.control.economizer_cutin
        Taux = self.zone.control.heating_setpoint - self.zone.control.auxiliary_cutin
        MinAch = self.zone.hvac.minimum_ach
        mode = self.zone.hvac.mode
        vent = self.zone.control.ventilation_fraction

        self.update_control_setpoints()

        if Tair > self.TheatOff and Tair < self.TcoolOff:  # enter VENT/OFF mode
            if vent > 0:
                mode = HCMODE.VENT
            else:
                mode = HCMODE.OFF
        elif Tair <= self.TheatOn or (mode == HCMODE.AUX or mode == HCMODE.HEAT):  # enter HEAT/AUX mode
            if Tair <= Taux:
                mode = HCMODE.AUX
            else:
                mode = HCMODE.HEAT
        elif Tair >= self.TcoolOn or (mode == HCMODE.ECON or mode == HCMODE.COOL):  # enter ECON/COOL mode
            if Tout < Tecon:
                Qgain = self.Qs + self.Qi - self.zone.design.exterior_ua * (
                        Tair - Tout) - self.zone.design.interior_ua * (Tair - Tmass)
                vent = Qgain / ((Tair - Tout) * (
                        0.2402 * 0.0735 * self.zone.design.floor_height * self.zone.design.floor_area))
                if vent < MinAch:
                    vent = MinAch
                    mode = HCMODE.ECON
                elif vent > 5.0:
                    if Tout > Tair:
                        vent = MinAch
                    mode = HCMODE.COOL
                else:
                    mode = HCMODE.ECON
            else:
                mode = HCMODE.COOL

        return TS_NEVER

    def sync(self, t1):
        t0 = self.get_clock()

        # Load calculations
        self.update_lighting(t1)
        self.update_plugs(t1)

        # Local aliases
        Tout = self.zone.current.pTemperature
        Ua = self.zone.design.exterior_ua
        Cm = self.zone.design.interior_mass
        Um = self.zone.design.interior_ua
        Ti = self.zone.current.air_temperature
        dTi = self.zone.current.temperature_change
        Tm = self.zone.current.mass_temperature
        mode = self.zone.hvac.mode

        # Rest of the code
        # ...
        # Update the variables accordingly

    def get_clock(self):
        # Implement the get_clock method to retrieve the current timestamp
        pass

    def e2solve(self, k1, r1, k2, r2, delta_T):
        # Implement the e2solve method
        pass


def occupancy_schedule(text, occupied):
    # /* convert a schedule into an occupancy buffer
    #    syntax: DAYS,HOURS
    #    where DAYS is a range of day numbers and HOURS is a range of hours
    #    e.g.,
    # 	"1-5 8-17;6,7 10,11,13,14" means Mon-Fri 8a-5p, and Sat & Holidays 10a-noon and 1p-3p
    #    with
    # 	Day 0 = Sunday, etc., day 7 = holiday
    # 	Hour 0 = midnight to 1am
    #  */
    days = [0] * 8
    hours = [0] * 24

    p = text
    next_val = -1
    start = -1
    stop = -1
    target = days

    for char in text:
        if char == ';':
            # Recursion on the rest of the schedule
            occupancy_schedule(text[p:], occupied)
            break

        if char.isdigit():
            if next_val == -1:
                next_val = 0
            next_val += next_val * 10 + int(char)
            continue
        elif char == '*':
            start = 0
            next_val = -1
            continue
        elif char in (',', ' ', ';', '\0'):
            stop = next_val
            for n in range(start, stop + 1 if stop >= 0 else (8 if target == days else 24)):
                target[n] = 1

            if char == ',':
                continue
            elif char == ' ':
                target = hours
                start = -1
                stop = -1
                next_val = -1
                continue
            elif char == ';' or char == '\0':
                for d in range(8):
                    for h in range(24):
                        if days[d] and hours[h]:
                            occupied[d][h] = 1

                if char == '\0':
                    break
                else:
                    start = -1
                    stop = -1
                    next_val = -1
                    continue
            else:
                raise Exception("office/occupancy_schedule(): invalid parser state")
        elif char == '-':
            start = next_val
            stop = -1
            next_val = -1
            continue
        else:
            raise Exception("office/occupancy_schedule(): schedule syntax error")


def hvac_control(mode, cop, Qactive, Qvent, zone, dTi, Ti, TcoolOn, TheatOn, Teq, Tout, Taux, Trange, TheatOff, TmaxCool, Tecon, TcoolOff):
    if mode == "hc_off": 
        cop = 0
        Qactive = Qvent = 0
        if dTi<0 and Ti<TcoolOn:
            Tevent = TheatOn
        elif dTi>0 and Ti>TheatOn:
            Tevent = TcoolOn
        else:
            Tevent = Teq
    elif mode == "hc_heat": 
        cop = 1.0 + (zone.hvac.heating.cop-1)*(Tout-Taux)/Trange
        Qactive = zone.hvac.heating.capacity + zone.hvac.heating.capacity_perF*(zone.hvac.heating.balance_temperature-Tout)
        Qvent = (zone.current.pTemperature - zone.current.air_temperature) * (0.2402 * 0.0735 * zone.design.floor_height * zone.design.floor_area) * zone.control.ventilation_fraction
        Tevent = TheatOff
    elif mode == "hc_aux": 
        cop = 1.0
        Qactive = zone.hvac.heating.capacity
        Qvent = (zone.current.pTemperature - zone.current.air_temperature) * (0.2402 * 0.0735 * zone.design.floor_height * zone.design.floor_area) * zone.control.ventilation_fraction
        Tevent = TheatOff
    elif mode == "hc_cool": 
        cop = -1.0 - (zone.hvac.cooling.cop+1)*(Tout-TmaxCool)/(TmaxCool-Tecon)
        Qactive = zone.hvac.cooling.capacity - zone.hvac.cooling.capacity_perF*(Tout-zone.hvac.cooling.balance_temperature)
        Qvent = (zone.current.pTemperature - zone.current.air_temperature) * (0.2402 * 0.0735 * zone.design.floor_height * zone.design.floor_area) * zone.control.ventilation_fraction
        Tevent = TcoolOff
    elif mode == "hc_vent": 
        cop = 0
        Qactive = 0
        Qvent = (zone.current.pTemperature - zone.current.air_temperature) * (0.2402 * 0.0735 * zone.design.floor_height * zone.design.floor_area) * zone.control.ventilation_fraction
        if dTi<0 and Ti<TcoolOn:
            Tevent = TheatOn
        elif dTi>0 and Ti>TheatOn:
            Tevent = TcoolOn
        else:
            Tevent = Teq
    elif mode == "hc_econ": 
        cop = 0.0
        Qactive = 0
        Qvent = (zone.current.pTemperature - zone.current.air_temperature) * (0.2402 * 0.0735 * zone.design.floor_height * zone.design.floor_area) * zone.control.ventilation_fraction
        Tevent = TcoolOff
    else:
        raise ValueError("hvac mode is invalid")


def calculate_ventilation_rate(t_out, t_econ, q_s, q_i, t_air, t_mass, min_ach, zone):
    if t_out < t_econ:
        q_gain = q_s + q_i - zone.design.exterior_ua*(t_air - t_out) - zone.design.interior_ua*(t_air - t_mass)
        vent = q_gain / ((t_air - t_out) * (0.2402 * 0.0735 * zone.design.floor_height * zone.design.floor_area))
        if vent < min_ach:
            vent = min_ach
            mode = "HCMODE.ECON"
        elif vent > 5.0:
            if t_out > t_air: 
                vent = min_ach
            mode = "HCMODE.COOL"
        else:
            mode = "HCMODE.ECON"






