import os
import sys
import time

import numpy as np
import ctypes
import ctypes.util

from gov_pnnl_goss.gridlab.gldcore.GridLabD import gl_error

# Placeholder for other functions and includes

# Constants
mod_eul_solver_version = 1

# Structure
class MEULERDATA(ctypes.Structure):
    _fields_ = [
        ("number_y_variables", ctypes.c_int),
        ("number_x_variables", ctypes.c_int),
        ("x", ctypes.POINTER(ctypes.c_double)),
        ("x_next", ctypes.POINTER(ctypes.c_double)),
        ("y", ctypes.POINTER(ctypes.c_double)),
        ("y_intermed", ctypes.POINTER(ctypes.c_double)),
        ("y_first_deriv", ctypes.POINTER(ctypes.c_double)),
        ("y_second_deriv", ctypes.POINTER(ctypes.c_double)),
        ("y_next", ctypes.POINTER(ctypes.c_double)),
        ("deltaT", ctypes.c_double),
        ("deriv_function", ctypes.CFUNCTYPE(ctypes.c_ubyte, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_double, ctypes.c_double)),
        ("status_val", ctypes.c_ubyte),
    ]

# Functions
def modified_euler_init(fntable):
    callback = fntable
    return 1

def modified_euler_set(param, *args):
    tag = param
    if tag is not None:
        gl_error(f"modified_euler_set(char *param='{param}',...): tag '{tag}' is not recognized - no input parameters expected!")
        return 0
    else:
        return 1

def modified_euler_get(param, *args):
    n = 0
    variable_x_size = 1
    variable_y_size = 1
    tag = param
    while tag is not None:
        try:
            if param == "solver_version":
                args[0].value = mod_eul_solver_version
            elif param == "number_x_variables":
                variable_x_size = args[0]
            elif param == "number_y_variables":
                variable_y_size = args[0]
            elif param == "init":
                data = args[0]
                data.number_x_variables = variable_x_size
                data.number_y_variables = variable_y_size
                data.x = np.zeros(variable_x_size, dtype=np.float64)
                data.x_next = np.zeros(variable_x_size, dtype=np.float64)
                data.y = np.zeros(variable_y_size, dtype=np.float64)
                data.y_intermed = np.zeros(variable_y_size, dtype=np.float64)
                data.y_first_deriv = np.zeros(variable_y_size, dtype=np.float64)
                data.y_second_deriv = np.zeros(variable_y_size, dtype=np.float64)
                data.y_next = np.zeros(variable_y_size, dtype=np.float64)
                data.deltaT = 1.0
                data.status_val = 0
            else:
                gl_error(f"modified_euler_get(char *param='{param}',...): tag '{tag}' is not recognized")
                return n
        except MemoryError as e:
            gl_error(f"modified_euler_get:init - failed to allocate storage array: {e}")
            return n

        tag = args[1]
        n += 1
    return n


def modified_euler_solve(data):
    indexval = 0
    returnval = 0
    dfx = data.deriv_function
    returnval = dfx(data.x, data.y, data.y_first_deriv, data.number_x_variables, data.number_y_variables)
    if returnval != 1:
        gl_error("modified_euler_solve - the derivative function did not return success")
        return 0
    # Create y-intermediate
    # Y_intermed = Y_0 + functions'(X_0,Y_0)*dT
    data.y_intermed = data.y + data.y_first_deriv * data.deltaT
    # Get second derivative - functions'(X_0+dT,Y_intermed)
    returnval = dfx(data.x_next, data.y_intermed, data.y_second_deriv, data.number_x_variables, data.number_y_variables)
    if returnval != 1:
        gl_error("modified_euler_solve - the derivative function did not return success")
        return 0
    # Put it into the final answer
    #   Y_final = Y_0 + 0.5*[functions'(X_0,Y_0)+functions'(X_0+dT,Y_intermed)]*dT
    data.y_next = data.y + 0.5 * (data.y_first_deriv + data.y_second_deriv) * data.deltaT
    #   We're always successful for now
    data.status_val = 1
    return data.status_val
