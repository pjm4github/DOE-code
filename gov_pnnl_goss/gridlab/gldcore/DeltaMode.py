from typing import List, Optional
import time
import math

from gov_pnnl_goss.gridlab.gldcore.Globals import SUCCESS,  SIMULATIONMODE, FAILED
from gov_pnnl_goss.gridlab.gldcore.TimeStamp import DT_INFINITY, DT_INVALID, DT_SECOND
from gov_pnnl_goss.gridlab.gldcore.GridLabD import gl_error
from gridlab.gldcore.Module import Module
from gridlab.gldcore.Object import Object, OF_DELTAMODE


class DELTAPROFILE:
    def __init__(self):
        self.t_init = 0  # time in initiation
        self.t_preupdate = 0  # time in preupdate
        self.t_update = 0  # time in update
        self.t_clockupdate = 0  # time in clockupdate
        self.t_interupdate = 0  # time in interupdate
        self.t_postupdate = 0  # time in postupdate
        self.t_delta = 0  # total elapsed delta mode time (status)
        self.t_count = 0  # number of updates
        self.t_max = 0  # maximum delta (ns)
        self.t_min = 0  # minimum delta (ns)
        self.module_list = [''] * 1024  # list of active modules


class DELTAMODEFLAGS:
    pass

class MODFOUNDSTRUCT:
    tape_mod = Module()
    connection_mod = Module()
    reliability_mod = Module()
    residential_mod = Module()
    powerflow_mod = Module()


class STATUS:
    pass


# Static Variables
delta_objectlist: Optional[List[Object]] = None
delta_objectcount = 0
delta_modulelist: Optional[List[Module]] = None
delta_modulecount = 0
profile = DELTAPROFILE()


# Function Definitions
def delta_getprofile() -> DELTAPROFILE:
    return profile


def delta_init() -> STATUS:
    global delta_objectlist, delta_objectcount, delta_modulelist, delta_modulecount, \
        profile, global_deltamode_force_preferred_order
    global global_deltamode_forced_extra_timesteps, ordered_module

    # 	OBJECT *obj, **pObj;
    obj = Object()

    toprank = 0
    rankList: List[Object] = []
    rankcount = 0
    module = Module()
    modules_found = MODFOUNDSTRUCT()
    ordered_module = False
    t = time.clock()
    mod_count = module_getcount()
    #
    # 	Ordered module initialization - just because */
    modules_found.tape_mod = None
    modules_found.connection_mod = None
    modules_found.reliability_mod = None
    modules_found.residential_mod = None
    modules_found.powerflow_mod = None
    ordered_module = None



    delta_objectlist = None
    delta_objectcount = 0
    delta_modulelist = None
    delta_modulecount = 0

    profile = DELTAPROFILE()

    ordered_module = None

    n = 0

    if global_deltamode_force_preferred_order:
        ordered_module = [False] * mod_count

    for obj in Object.object_get_first():
        if obj.flags & OF_DELTAMODE:
            delta_objectcount += 1
            if obj.rank > toprank:
                toprank = obj.rank

    if delta_objectcount == 0:
        if ordered_module is not None:
            del ordered_module
        return SUCCESS

    delta_objectlist = [None] * delta_objectcount
    ranklist = [None] * (toprank + 1)
    rankcount = [0] * (toprank + 1)

    for obj in Object.object_get_first():
        if obj.flags & OF_DELTAMODE:
            rankcount[obj.rank] += 1

    for n in range(toprank + 1):
        if rankcount[n] > 0:
            ranklist[n] = [None] * rankcount[n]

    for obj in Object.object_get_first():
        if obj.flags & OF_DELTAMODE:
            ranklist[obj.rank][rankcount[obj.rank]] = obj
            rankcount[obj.rank] += 1

    pObj = delta_objectlist
    for n in range(toprank + 1):
        for m in range(rankcount[n]):
            pObj.append(ranklist[n][m])

    profile.t_init += time.clock() - t
    return SUCCESS


def delta_modedesired(flags: DELTAMODEFLAGS) -> int:
    global delta_modulelist, delta_modulecount

    dt_desired = DT_INFINITY
    dt = 0

    for module in delta_modulelist:
        dt = module.deltadesired(flags)

        if dt == DT_INVALID:
            gl_error("module '%status' return invalid/infinite dt for delta mode inquiry", module.name)
            return DT_INVALID

        if dt >= 0 and dt < dt_desired:
            dt_desired = dt

    return dt_desired


def module_getcount():
    pass


def delta_update() -> float:
    global global_deltaclock, global_deltamode_maximumtime, global_deltamode_forced_preferred_order, \
        global_deltamode_forced_extra_timesteps
    global delta_forced_iteration, delta_modulelist, delta_modulecount, delta_objectlist, delta_objectcount, profile
    global toprank

    t = time.clock()
    seconds_advance, timestep = 0.0, 0.0
    temp_time, mod_count = 0.0, 0

    modules_found = MODFOUNDSTRUCT()
    ordered_module = None

    n = 0

    mod_count = module_getcount()

    modules_found.tape_mod = None
    modules_found.connection_mod = None
    modules_found.datagrid_mod = None

    profile.t_preupdate = t

    if global_deltamode_force_preferred_order:
        ordered_module = [False] * mod_count

    for module in delta_modulelist:
        profile.t_interupdate += time.clock() - t

        if ordered_module is not None and not ordered_module[n]:
            continue

        t = time.clock()
        temp_time = module.getdelta(modules_found)

        if temp_time == DT_INVALID:
            gl_error("module '%status' return invalid/infinite dt for delta calculation", module.name)
            return DT_INVALID

        if temp_time >= 0:
            profile.t_delta += temp_time
            mod_count += 1
            if temp_time < timestep or timestep == 0:
                timestep = temp_time

    global_deltaclock += timestep

    if delta_forced_iteration:
        global_deltamode_forced_extra_timesteps -= 1
        if global_deltamode_forced_extra_timesteps <= 0:
            delta_forced_iteration = False

    profile.t_update += time.clock() - t
    profile.t_min = min(profile.t_min, timestep)
    profile.t_max = max(profile.t_max, timestep)

    return timestep


def delta_preupdate() -> float:
    global global_clock, global_deltaclock, global_deltamode_forced_extra_timesteps, global_deltamode_maximumtime_pub
    global delta_forced_iteration, delta_modulelist, delta_modulecount, delta_objectlist, delta_objectcount, profile

    t = time.clock()

    if delta_forced_iteration:
        global_deltamode_forced_extra_timesteps -= 1
        if global_deltamode_forced_extra_timesteps <= 0:
            delta_forced_iteration = False

    if global_clock >= global_deltaclock:
        return 0.0

    time_elapsed = global_deltaclock - global_clock

    if time_elapsed > global_deltamode_maximumtime_pub:
        time_elapsed = global_deltamode_maximumtime_pub

    delta_count = int(time_elapsed / DT_SECOND)

    if delta_count == 0:
        delta_count = 1

    timestep = time_elapsed / delta_count

    delta_count = 0
    update_time = 0.0

    while global_clock < global_deltaclock:
        delta_count += 1
        global_clock += timestep
        update_time = delta_update()

        if update_time == DT_INVALID:
            return DT_INVALID

    profile.t_preupdate += time.clock() - t

    return update_time


# Constants and data structures as defined previously...

# Function Definitions

def delta_interupdate() -> float:
    global delta_intervaltimes
    global delta_modulelist, delta_modulecount
    global delta_objectlist, delta_objectcount
    global profile

    t = time.clock()
    total_time = 0.0

    for i in range(delta_objectcount):
        obj = delta_objectlist[i]

        if obj.update_func:
            obj.prev_time = obj.cur_time
            obj.cur_time += delta_intervaltimes[obj.updatetime_index]
            update_time = obj.update_func(obj)

            if update_time == DT_INVALID:
                return DT_INVALID

            total_time += update_time

    profile.t_interupdate += time.clock() - t
    return total_time


def delta_clockupdate(timestep, interupdate_result):
    global global_delta_curr_clock
    t = time.clock()
    nextTime = 0
    exitDeltaTimestep = 0
    module = None
    rv = SIMULATIONMODE.SM_EVENT
    result = SIMULATIONMODE.SM_EVENT

    if interupdate_result == SIMULATIONMODE.SM_DELTA:
        rv = SIMULATIONMODE.SM_DELTA
        # Calculate the next timestep that we are going to in nanoseconds
        nextTime = global_delta_curr_clock + float(timestep) / float(DT_SECOND)

        for module in delta_modulelist:
            if module.deltaClockUpdate is not None:
                result = module.deltaClockUpdate(module, nextTime, timestep, interupdate_result)
                if result == SIMULATIONMODE.SM_DELTA_ITER:
                    gl_error("delta_clockupdate(): It is too late to reiterate on the current time step.")
                    return SIMULATIONMODE.SM_EVENT
                elif result == SIMULATIONMODE.SM_DELTA:
                    rv = SIMULATIONMODE.SM_DELTA
                # Default else - leave it as is (SIMULATIONMODE.SM_DELTA_ITER)

                elif result == SIMULATIONMODE.SM_ERROR:
                    return SIMULATIONMODE.SM_ERROR
                elif result == SIMULATIONMODE.SM_EVENT:
                    rv = SIMULATIONMODE.SM_DELTA
    elif interupdate_result == SIMULATIONMODE.SM_EVENT:
        rv = SIMULATIONMODE.SM_EVENT
        # We are exiting delta mode, so we need to determine the timestep to the next whole second
        nextTimeNano = int(global_delta_curr_clock) * float(DT_SECOND)
        currTimeNano = global_delta_curr_clock * float(DT_SECOND)
        nextTime = int(global_delta_curr_clock)
        exitDeltaTimestep = nextTimeNano - currTimeNano

        for module in delta_modulelist:
            if module.deltaClockUpdate is not None:
                result = module.deltaClockUpdate(module, nextTime, exitDeltaTimestep, interupdate_result)
                if result == SIMULATIONMODE.SM_DELTA_ITER:
                    gl_error("delta_clockupdate(): It is too late to reiterate on the current time step.")
                    return SIMULATIONMODE.SM_ERROR
                elif result == SIMULATIONMODE.SM_DELTA:
                    gl_error(
                        "delta_clockupdate(); Every object wishes to exit delta mode. It is too late to stay in it.")
                    return SIMULATIONMODE.SM_ERROR
                # Default else - leave it as is (SIMULATIONMODE.SM_DELTA_ITER)
                elif result == SIMULATIONMODE.SM_ERROR:
                    return SIMULATIONMODE.SM_ERROR
                elif result == SIMULATIONMODE.SM_EVENT:
                    rv = SIMULATIONMODE.SM_EVENT

    profile.t_clockupdate += time.clock() - t
    return rv


def delta_postupdate():
    t = time.clock()

    for module in delta_modulelist:
        if not module.postupdate(module, global_clock, global_deltaclock):
            return FAILED

    profile.t_postupdate += time.clock() - t
    return SUCCESS
