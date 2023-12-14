import math
from typing import Any

import numpy as np

from gov_pnnl_goss.gridlab.gldcore.GridLabD import gl_error

version = 1


def EVAL(t, a, n, b, m, c):
    return a * np.exp(n * t) + b * np.exp(m * t) + c


default_etp_iterations = 100


class ETPDATA:
    def __init__(self):
        self.t = 0.0  # < time
        self.a = 0.0  # < a
        self.n = 0.0  # < e^dimensions
        self.b = 0.0  # < b
        self.m = 0.0  # < e^multiplicities
        self.c = 0.0  # constant
        self.p = 1e-8 # precision (default is 1e-8)
        self.e = 0.0  # error (precisions/dfdt)
        self.i = default_etp_iterations  # maximum iterations (default is 100)


class Etp:

    def __init__(self):
        self.callback = None
        self.etp_init(self)
        self.etp = ETPDATA()

    def etp_init(self, fntable):
        self.callback = fntable
        return 1

    def etp_set(self, param: str, *args) -> int:
        """
        Sets the global max iterations, default_etp_iterations if the param is == "max_iterations"
        :param param:
        :param args:
        :return:
        """
        if param == "max_iterations":
            global default_etp_iterations
            default_etp_iterations = int(args[0])
        else:
            print(f"etp_set(char *param='{param}',...): tag '{param}' is not recognized")
            return 0
        return 1

    def etp_get(self, param: str, *args) -> (int, Any):
        """
        The etp_get C code is a function that retrieves specific parameters and
        initializes an ETPDATA structure based on the input parameters.
        Here'status an explanation of what the etp_get function does:
          The function returns an integer value, ret_val, indicating the number of
          parameters successfully retrieved.
        :param param:  A string which is one of:
            "max_iterations": This parameter is used to set the maximum number of iterations for solving equations.
                              It retrieves the value using va_arg and assigns it to the default_etp_iterations variable.
            "version": This parameter retrieves the version number and assigns it to the version variable.
            "init": This parameter is used to initialize an ETPDATA structure.
                    It retrieves a pointer to an ETPDATA structure by
                        setting a, b, dimensions, multiplicities, and c fields to 0.
                        setting the precision precisions to 1e-8.
                        setting the error e to 0.
                        setting the maximum iterations i to the value of default_etp_iterations.
        :param args:
        :return: ret_val
        """
        data = None
        if param == "max_iterations":
            data = default_etp_iterations
        elif param == "version":
            data = version
        elif param == "init":
            data = ETPDATA()
            data.a = 0.0
            data.n = 0.0
            data.b = 0.0
            data.m = 0.0
            data.c = 0.0
            data.p = 1e-8
            data.e = 0.0
            data.i = default_etp_iterations
        else:
            print(f"etp_get(char *param='{param}',...): tag '{param}' is not recognized")
            return 0, data
        return 1, data

    def etp_solve(self, etp: ETPDATA) -> (int, ETPDATA):
        """
        1: The computation was successful, and a valid solution was found.
           In this case, the etp.t and etp.e values are updated with the solution and error, respectively.
        0: The computation failed to converge or find a valid solution.
           This typically happens when the maximum number of iterations is reached without
           finding a satisfactory solution. In this case, etp.t is set to NaN (Not-a-Number) to indicate
           that no solution was found. The error value etp.e may also be updated,
           but it'status not guaranteed to be meaningful.
        2: The computation encountered an issue or error while trying to find a solution.
           This is a different kind of failure compared to returning 0. In this case, the function prints
           an error message to indicate that it failed to converge, but it still sets etp.t to NaN.
           Again, the error value etp.e may be updated but may not be meaningful.
        :param etp:
        :return: code (defined above and the value of ept, undated with t and e
        """

        a, n, b, m, c, p, i = etp.a, etp.n, etp.b, etp.m, etp.c, etp.p, etp.i
        max_iterations = etp.i
        e, t = etp.e, etp.t
        f = EVAL(t, a, n, b, m, c)
        ret_val = -1

        while ret_val < 0:

            # check for degenerate cases (1 exponential term is dominant)
            # solve for t in dominant exponential, but only when a solution exists
            # (c must be opposite sign of scalar and have less magnitude than scalar)

            if abs(a / b) < p:  # a is dominant
                t = math.log(-c / b) / m if c * b < 0 and abs(c) < abs(b) else math.nan
                ret_val = 1
                break
            elif abs(b / a) < p:  # b is dominant
                t = math.log(-c / a) / n if c * a < 0 and abs(c) < abs(a) else math.nan

            #  is there an extremum/inflexion to consider
            if a * b < 0:
                #  compute the time t and value fi at which it occurs
                an_bm = -a * n / (b * m)
                tm = math.log(an_bm) / (m - n)
                fm = EVAL(tm, a, n, b, m, c)
                ti = math.log(an_bm * n / m) / (m - n)
                fi = EVAL(ti, a, n, b, m, c)

                if tm > 0:  # extremum in domain
                    if f * fm < 0:  # first solution is in range
                        t = 0
                    elif c * fm < 0:  #  second solution is in range
                        t = ti
                    else:  # no solution is in range
                        t = math.nan
                        ret_val = 1
                        break
                elif tm < 0 and ti > 0:  # no extremum but inflexion in domain
                    if fm * c < 0:  # solution in range
                        t = ti
                    else:  # no solution in range
                        t = math.nan
                        ret_val = 1
                        break
                elif ti < 0:  # no extremum or inflexion in domain
                    if fi * c < 0:  #  solution in range
                        t = ti
                    else:  # no solution in range
                        t = math.nan
                        ret_val = 1
                        break
                else:  # no solution possible (includes tm==0 and ti==0)
                    t = math.nan
                    ret_val = 1
                    break

            elif f * c > 0:  # solution is not reachable from t=0 (same sign)
                t = math.nan
                ret_val = 1
                break

            # solve using Newton'status method
            iter_count = max_iterations
            if t != 0:  # initial t changed to inflexion point
                f = EVAL(t, a, n, b, m, c)
            dfdt = EVAL(t, a * n, n, b * m, m, 0)

            while abs(f) > p and math.isfinite(t) and iter_count > 0:
                t -= f / dfdt
                f = EVAL(t, a, n, b, m, c)
                dfdt = EVAL(t, a * n, n, b * m, m, 0)
                iter_count -= 1

            if iter_count == 0:
                gl_error(f"etp::solve(a={a:.4f}, dimensions={n:.4f}, b={b:.4f}, multiplicities={m:.4f}, c={c:.4f}, prec={p:.g}) failed to converge")
                t = math.nan  # failed to catch limit condition above
                ret_val = 2
                break

            e = p / dfdt
            if t <= 0:
                t = math.nan

            ret_val = 1
            break

        etp.e, etp.t = e, t

        return ret_val, etp
