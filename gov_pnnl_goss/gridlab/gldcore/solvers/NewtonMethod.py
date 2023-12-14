# Copyright (C) 2012 Battelle Memorial Institute
# DP Chassin
from enum import Enum
from typing import Any

import numpy as np

from gov_pnnl_goss.gridlab.gldcore.GridLabD import gl_error

# Definitions for constants
solver_version = 1
max_iterations = 100
dimensions = 1


class Status(Enum):
    FAILED = 0
    CONVERGE = 1
    NON_CONVERGED = 2


# Define the NMDATA structure
class NMDATA:
    def __init__(self, n=1):
        self.dimensions = n # // dimensions (default 1)
        self.x = np.zeros(n, dtype=np.double)  # // current values of x
        self.functions = np.empty(n, dtype=np.object)  # // functions
        self.df = np.empty(n, dtype=np.object)  # // derivatives
        self.precisions = np.full(n, 1e-8, dtype=np.double)  # // precisions
        self.multiplicities = np.ones(n, dtype=np.uint)  # // multiplicities (default is 1)
        self.status = np.ones(n, dtype=np.ubyte)  # // status (0=failed, 1=converge, 2=non-converged)


class NewtonMethod:
    def __init__(self, fntable):
        self.newton_method_init(fntable)
        self.data = NMDATA()

    # Define the Newton method functions
    def newton_method_init(self, fntable):
        global callback
        callback = fntable
        return 1

    def newton_method_set(self, param, *args):
        global max_iterations, dimensions
        n = 0
        args = iter(args)
        try:
            while True:
                tag = next(args)
                if tag == "max_iterations":
                    max_iterations = next(args, max_iterations)
                elif tag == "dimensions":
                    dimensions = next(args, dimensions)
                else:
                    gl_error(f"newton_method_set(char *param='{param}',...): tag '{tag}' is not recognized")
                    return n
                n += 1
        except StopIteration:
            pass
        return n

    def newton_method_get(self, param: str, *args) -> (int, Any):
        global solver_version, max_iterations, dimensions
        n = 0
        data = None
        tag = param
        arg_list = args if args else []
        while True:
            if param == "solver_version":
                data = int(arg_list[0]) if arg_list[0] else solver_version
            elif param == "max_iterations":
                data = int(arg_list[0]) if arg_list[0] else max_iterations
            elif param == "dimensions":
                data = int(arg_list[0]) if arg_list[0] else dimensions
            elif param == "init":
                dimensions = int(arg_list[0]) if arg_list[0] else self.data.dimensions
                data.dimensions = dimensions
                data.df = np.empty(dimensions, dtype=np.object)
                data.functions = np.empty(dimensions, dtype=np.object)
                data.x = np.zeros(dimensions, dtype=np.double)
                data.multiplicities = np.ones(dimensions, dtype=np.uint)
                data.precisions = np.full(dimensions, 1e-8, dtype=np.double)
                data.status = np.ones(dimensions, dtype=np.ubyte)
            else:
                gl_error(f"newton_method_get(char *param='{param}',...): tag '{tag}' is not recognized")
                break
            n += 1
            if len(arg_list) > 2:
                param = arg_list[1]
                arg_list = arg_list[2:]
            else:
                break
        return n, data

    def newton_method_solve(self):
        """
        The function returns the final status s to indicate whether the solution process was successful or not.
        The newton_method_solve function iteratively applies the Newton-Raphson method to find solutions for a
        system of nonlinear equations for each dimension separately.
        It checks for convergence, non-convergence, or failures and returns an appropriate status code.
        Final State:
            After the loop, the function has either found a solution within the specified precision or
            terminated due to reaching the maximum number of iterations. The status s reflects the outcome:
                If s is 1, it means the solution has converged successfully.
                If s is 2, it means the solution did not converge within the allowed iterations.
                If s is 0, it means there was an issue with the calculations (e.g., dydx was zero or NaN).
        :return:
        """
        s = Status.CONVERGE
        data = self.data
        for n in range(data.dimensions):
            p = data.precisions[n]
            x = data.x[n:n + 1]
            f = data.functions[n]
            df = data.df[n]
            m = data.multiplicities[n:n + 1]
            s_byte = data.status[n:n + 1]
            dx = np.array([0.0], dtype=np.double)
            i = 0
            while True:
                dydx = df(x)
                if np.isnan(dydx) or dydx == 0:
                    x[...] = np.nan
                    s_byte[...] = 0
                    s = Status.FAILED
                    break
                elif not np.isfinite(dydx):
                    break
                else:
                    dx[0] = m[0] * f(x[0]) / dydx
                    x[0] -= dx[0]
                i += 1
                if i > max_iterations:
                    if s != Status.FAILED:
                        s = Status.NON_CONVERGED
                    s_byte[...] = 2
                if np.abs(dx[0]) <= p:
                    break
            self.data.x[n:n + 1] = x
            self.data.status[n:n + 1] = s_byte
        return s
