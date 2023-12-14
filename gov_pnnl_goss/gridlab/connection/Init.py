import math

from gov_pnnl_goss.gridlab.commercial.Init import gl_global_create
from gov_pnnl_goss.gridlab.connection.Connection import CONNECTIONSECURITY
from gov_pnnl_goss.gridlab.connection.FncsMsg import FncsMsg
from gov_pnnl_goss.gridlab.connection.HelicsMsg import HelicsMsg
from gov_pnnl_goss.gridlab.connection.Json import Json
from gov_pnnl_goss.gridlab.connection.Native import Native
from gov_pnnl_goss.gridlab.connection.Socket import Socket
from gov_pnnl_goss.gridlab.gldcore.Globals import EINVAL, SIMULATIONMODE, DT_INFINITY, DT_INVALID
from gov_pnnl_goss.gridlab.gldcore.GridLabD import gl_error, Callback
from gov_pnnl_goss.gridlab.gldcore.Property import PROPERTYTYPE


connection_lockout = 0.0
enable_subsecond_models = False


class ConnectionSecurity:
    def __init__(self):
        self.connection_security = "CS_STANDARD"
        self.connection_lockout = 0.0
        self.enable_subsecond_models = False


def deltaClockUpdate(module, t1, timestep, systemmode):
    pass


def delta_mode_desired(flags):
    return math.nan  # Returns time in seconds to when the next delta mode transition is desired
    # Return float('inf') if this module doesn't have any specific triggering times


def convert_subsecond_models():
    # NOTE: that given how this is used currently, preupdate could just be a return dt_infinity for all cases
    # Pull global timestep
    dtimestep = gld_global("deltamode_timestep")
    if not dtimestep.is_valid():
        gl_error("connection::preupdate: unable to find delamode_timestep!")
        return DT_INVALID

    # Pull it for use
    double_timestep_value = dtimestep.get_double()

    if double_timestep_value <= 0.0:
        gl_error("connection::preupdate: deltamode_timestep must be a positive, non-zero number!")
        #  TROUBLESHOOT
        # The value for global_deltamode_timestep, must be a positive, non-zero number.
        # Please use such a number and try again.

        return DT_INVALID
    else:
        # Do the casting conversion on it to put it back in integer format
        return int(double_timestep_value + 0.5)


class Init:
    oclass = 0
    def __init__(self):
        pass
        self.dClockUpdateList = []
        self.clkupdatelist = []
        self.errno = None
        self.dInterUpdateList = []



    def init(self, fntable, module, argc, argv):
        if Callback.set_callback(fntable) is None:
            errno = EINVAL
            return None

        Socket.init(module)

        gl_global_create("connection::security",
                         PROPERTYTYPE.PT_enumeration, CONNECTIONSECURITY.CS_STANDARD,
                         PROPERTYTYPE.PT_DESCRIPTION, "default connection security level",
                         PROPERTYTYPE.PT_KEYWORD, "NONE", CONNECTIONSECURITY.CS_NONE,
                         PROPERTYTYPE.PT_KEYWORD, "LOW", CONNECTIONSECURITY.CS_LOW,
                         PROPERTYTYPE.PT_KEYWORD, "STANDARD", CONNECTIONSECURITY.CS_STANDARD,
                         PROPERTYTYPE.PT_KEYWORD, "HIGH", CONNECTIONSECURITY.CS_HIGH,
                         PROPERTYTYPE.PT_KEYWORD, "EXTREME", CONNECTIONSECURITY.CS_EXTREME,
                         PROPERTYTYPE.PT_KEYWORD, "PARANOID", CONNECTIONSECURITY.CS_PARANOID,
                         None)

        gl_global_create("connection::lockout", PROPERTYTYPE.PT_double, connection_lockout,
                         PROPERTYTYPE.PT_UNITS, "s",
                         PROPERTYTYPE.PT_DESCRIPTION, "default connection security lockout time",
                         None)

        gl_global_create("connection::enable_subsecond_models", PROPERTYTYPE.PT_bool, enable_subsecond_models,
                         PROPERTYTYPE.PT_DESCRIPTION, "Enable deltamode capabilities within the connection module",
                         None)

        # These will register the various objects
        native = Native(module)
        # new xml(module)  # TODO finish XML implementation
        Json(module)
        # new fncs_msg(module)  # Uncomment if needed
        # new helics_msg(module)  # Uncomment if needed
        # TODO add new classes before this line

        FncsMsg(module)
        # always return the first class registered
        HelicsMsg(module)
        return native.oclass

    def do_kill(self, data):
        # if global memory needs to be released, this is a good time to do it
        # TODO process all term() for each object created by this module
        return 0

    def check(self):
        # if any assert objects have bad filenames, they'll fail on init()
        return 0

    def add_clock_update(self, data, clkupdate):
        item = {"clkupdate": clkupdate, "data": data}
        clkupdatelist.append(item)

    # def add_clock_update(data, clk_update):
    #     item = {"clk_update": clk_update, "data": data, "next": clk_update_list}
    #     clk_update_list = item

    def clock_update(self, t1):
        # send t1 to an external tool and return an alternate proposed time
        # Return t1 if t1 is OK to use. Do not return TS_INVALID or any values less than global_clock
        # CAVEAT: this will be called multiple times until all modules that use clock_update
        # agree on the value of t1.
        global clkupdatelist
        ok = False
        while not ok:
            ok = True
            for item in clkupdatelist:
                t2 = item["clkupdate"](item["data"], t1)
                if t2 < t1:
                    ok = False
                    t1 = t2
        return t1

    # def clock_update(t1):
    #     item = None
    #     t2 = t1
    #     ok = 0
    #     while not ok:
    #         ok = 1
    #         for item in clkupdatelist:
    #             pass
    #     return t1

    def delta_clock_update(self, module, t1, timestep, systemmode):
        result = SIMULATIONMODE.SM_DELTA
        item = self.dClockUpdateList
        while item is not None:
            result = item.dclkupdate(item.data, t1, timestep, systemmode)
            return result

        if self.dClockUpdateList is None:
            return SIMULATIONMODE.SM_EVENT
        else:
            return SIMULATIONMODE.SM_ERROR

    def deltamode_desired(self, flags):
        return DT_INFINITY  # Returns time in seconds to when the next deltamode transition is desired

    # 
    def postupdate(self, module, t_0, dt):
        """
        t_0 is the current global clock time (event-based)
        dt is the current delta clock nanosecond offset from t_0
        """
        return 1  # return 0 for FAILURE or 1 for SUCCESS

    # def preupdate(self, module, t0, dt):
    #     double_timestep_value = 0
    #     if enable_subsecond_models == true:
    #         pass
    #     else:  # Not desired, just return an arbitrarily large value
    #         return DT_INFINITY

    # Deltamode functions
    def preupdate(self, module, t0, dt):
        double_timestep_value = 0.0

        if enable_subsecond_models:
            # NOTE: that given how this is used currently, preupdate could just be a return DT_INFINITY for all cases

            # Pull global timestep
            dtimestep = gld_global("deltamode_timestep")
            if not dtimestep.is_valid():
                gl_error("connection::preupdate: unable to find deltamode_timestep!")
                return DT_INVALID

            # Pull it for use
            double_timestep_value = dtimestep.get_double()

            if double_timestep_value <= 0.0:
                gl_error("connection::preupdate: deltamode_timestep must be a positive, non-zero number!")
                return DT_INVALID
            else:
                # Do the casting conversion on it to put it back in integer format
                return int(double_timestep_value + 0.5)
        else:  # Not desired, just return an arbitrarily large value
            return DT_INFINITY

    # def register_object_interupdate(data, dInterUpdate):
    #     item = {'deltainterupdate': dInterUpdate, 'data': data, 'next': dInterUpdateList}
    #     dInterUpdateList = item

    def register_object_interupdate(self, data, dInterUpdate):
        item = {"deltainterupdate": dInterUpdate, "data": data}
        self.dInterUpdateList.append(item)


    def interupdate(self, module, t0, delta_time, dt, iteration_count_val):
        result = SIMULATIONMODE.SM_EVENT
        rv = SIMULATIONMODE.SM_EVENT
        for item in self.dInterUpdateList:
            result = item["deltainterupdate"](item["data"], iteration_count_val, t0, delta_time)
            if result == SIMULATIONMODE.SM_DELTA_ITER:
                rv = SIMULATIONMODE.SM_DELTA_ITER
            elif result == SIMULATIONMODE.SM_DELTA:
                if rv != SIMULATIONMODE.SM_DELTA_ITER:
                    rv = SIMULATIONMODE.SM_DELTA
            elif result == SIMULATIONMODE.SM_EVENT:
                if rv != SIMULATIONMODE.SM_DELTA_ITER or rv != SIMULATIONMODE.SM_DELTA:
                    rv = SIMULATIONMODE.SM_EVENT
            elif result == SIMULATIONMODE.SM_ERROR:
                return SIMULATIONMODE.SM_ERROR
        return rv

        # def interupdate(module, t0, delta_time, dt, iteration_count_val):
        #     item = None
        #     result = SIMULATIONMODE.SM_EVENT
        #     rv = SIMULATIONMODE.SM_EVENT
        #     for item in dInterUpdateList:
        #         result = item.deltainterupdate(item.data, iteration_count_val, t0, delta_time)
        #         if result == SIMULATIONMODE.SM_DELTA_ITER:
        #             rv = SIMULATIONMODE.SM_DELTA_ITER
        #         elif result == SIMULATIONMODE.SM_DELTA:
        #             if rv != SIMULATIONMODE.SM_DELTA_ITER:
        #                 rv = SIMULATIONMODE.SM_DELTA
        #         elif result == SIMULATIONMODE.SM_EVENT:
        #             if rv != SIMULATIONMODE.SM_DELTA_ITER or rv != SIMULATIONMODE.SM_DELTA:
        #                 rv = SIMULATIONMODE.SM_EVENT
        #         elif result == SIMULATIONMODE.SM_ERROR:
        #             return SIMULATIONMODE.SM_ERROR
        #     return rv


    def register_object_deltaclockupdate(self, data, dClockUpdate):
        item = {"dclkupdate": dClockUpdate, "data": data}
        self.dClockUpdateList.append(item)

