
import math

from gov_pnnl_goss.gridlab.gldcore.GridLabD import gl_error


def eval_eq(t, a, n, b, m, c):
    # /** solve an equation of the form $f[ ae^{nt} + be^{mt} + c = 0 $f]
    # 	@returns the solution in $f[ t $f], or etp::NaN if none found
    #  **/
    return a * math.exp(n * t) + b * math.exp(m * t) + c


def e2solve(a, n, b, m, c, p=1e-8, e=None) -> float:
    """
    :param a: /**< the parameter \p a */
    :param n: /**< the parameter \p n (should be negative) */
    :param b: /**< the parameter \p b */
    :param m: /**< the parameter \p m (should be negative) */
    :param c: /**< the constant \p c */
    :param p: /**< the precision (1e-8 if omitted) */
    :param e: /**< pointer to error estimate (null if none desired) */
    :return:
    """
    t = 0
    f = eval_eq(t, a, n, b, m, c)

    # 	// check for degenerate cases (1 exponential term is dominant)
    # 	// solve for t in dominant exponential, but only when a solution exists
    # 	// (c must be opposite sign of scalar and have less magnitude than scalar)

    if abs(a/b) < p:
        if c * b < 0 and abs(c) < abs(b):
            return math.log(-c/b)/m
    elif abs(b/a) < p:
        if c * a < 0 and abs(c) < abs(a):
            return math.log(-c/a)/n

    t = None
    # // is there an extremum/inflexion to consider
    if a * b < 0:
        # // compute the time t and value fi at which it occurs
        an_bm = -a * n / (b * m)
        tm = math.log(an_bm) / (m - n)
        fm = eval_eq(tm, a, n, b, m, c)
        ti = math.log(an_bm * n / m) / (m - n)
        fi = eval_eq(ti, a, n, b, m, c)
        if tm > 0:  # // extremum in domain
            if f * fm < 0:  # // first solution is in range
                t = 0
            elif c * fm < 0:  #  // second solution is in range
                t = ti
            else:  # // no solution is in range
                return math.nan
        elif tm < 0 and ti > 0:  #  // no extremum but inflexion in domain
            if fm * c < 0:  # // solution in range
                t = ti
            else:  # // no solution in range
                return math.nan
        elif ti < 0: #  // no extremum or inflexion in domain
            if fi * c < 0:  # // solution in range
                t = ti
            else:  # // no solution in range
                return math.nan
        else:  #  // no solution possible (includes tm==0 and ti==0)
            return math.nan

    elif f * c > 0:  # // solution is not reachable from t=0 (same sign)
        return math.nan

    # // solve using Newton's method
    iter = 100
    if t != 0:  # // initial t changed to inflexion point
        f = eval_eq(t, a, n, b, m, c)

    dfdt = eval_eq(t, a*n, n, b*m, m, 0)
    while (abs(f) > p and math.isfinite(t) and iter > 0):
        t -= f/dfdt
        f = eval_eq(t, a, n, b, m, c)
        dfdt = eval_eq(t, a*n, n, b*m, m, 0)
        iter -= 1

    if iter == 0:
        gl_error("etp::solve(a=%.4f,n=%.4f,b=%.4f,m=%.4f,c=%.4f,prec=%.g) failed to converge", a, n, b, m, c, p)
        return float('nan')  # failed to catch limit condition above

    if e is not None:
        e[0] = p/dfdt

    return t if t > 0 else math.nan


def same_sign(x, y):
    if x * y <= 0:
        return math.nan


