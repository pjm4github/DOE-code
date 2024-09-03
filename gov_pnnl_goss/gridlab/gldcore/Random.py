import re
import math
import random
import string

from gov_pnnl_goss.gridlab.gldcore.Find import Find, FL_GROUP
from gov_pnnl_goss.gridlab.gldcore.Globals import FAILED, SUCCESS, RANDOMNUMBERGENERATOR
from gov_pnnl_goss.gridlab.gldcore.Object import Object
from gov_pnnl_goss.gridlab.gldcore.Output import output_warning, output_test
from gov_pnnl_goss.gridlab.gldcore.Platform import QNAN
from gov_pnnl_goss.gridlab.gldcore.TimeStamp import TS_NEVER
from gov_pnnl_goss.gridlab.gldcore.GldRandom import RandomType, RandomVar
from gov_pnnl_goss.gridlab.gldcore.Unit import Unit

RNF_INTEGRATE = True

random_map = [
    # tested
    # name, global_property_types, nargs
    {"name": "degenerate", "global_property_types": RandomType.RT_DEGENERATE, "nargs": 1},
    {"name": "uniform", "global_property_types": RandomType.RT_UNIFORM, "nargs": 2},
    {"name": "normal", "global_property_types": RandomType.RT_NORMAL, "nargs": 2},
    {"name": "bernoulli", "global_property_types": RandomType.RT_BERNOULLI, "nargs": 1},
    {"name": "sampled", "global_property_types": RandomType.RT_SAMPLED, "nargs": -1},
    {"name": "pareto", "global_property_types": RandomType.RT_PARETO, "nargs": 2},
    {"name": "lognormal", "global_property_types": RandomType.RT_LOGNORMAL, "nargs": 2},
    {"name": "exponential", "global_property_types": RandomType.RT_EXPONENTIAL, "nargs": 1},
    {"name": "rayleigh", "global_property_types": RandomType.RT_RAYLEIGH, "nargs": 1},
    # untested
    {"name": "weibull", "global_property_types": RandomType.RT_WEIBULL, "nargs": 2},
    {"name": "gamma", "global_property_types": RandomType.RT_GAMMA, "nargs": 1},
    {"name": "beta", "global_property_types": RandomType.RT_BETA, "nargs": 2},
    {"name": "triangle", "global_property_types": RandomType.RT_TRIANGLE, "nargs": 2},
    # @todo Add some other distributions (e.g., Cauchy, Laplace)  (ticket #56)*/
 ]


def convert_to_randomvar(string, var):
    # Assuming random_type, random_nargs, randomvar_update, unit_convert are defined elsewhere

    # Split string into semicolon-separated tokens
    tokens = string.split(';')

    for token in tokens:
        if ':' in token:
            param, value = token.split(':', 1)
        else:
            param, value = token, '1'

        param = param.strip()
        value = value.strip()

        if param == "global_property_types":
            type_info = re.match(r'(\w+)\(([^)]*)\)', value)
            if type_info:
                type_name, args = type_info.groups()
                var.global_property_types = random_type(type_name)
                if var.global_property_types == RandomType.RT_INVALID:
                    print(f"Error: invalid global_property_types '{type_name}'")
                    return False

                args = args.split(',')
                var.a = float(args[0])
                if len(args) == 2:
                    var.b = float(args[1])
            else:
                print(f"Error: missing '(' in global_property_types spec '{value}'")
                return False

        elif param == "min":
            var.low = float(value)
        elif param == "max":
            var.high = float(value)
        elif param == "refresh":
            # Assuming unit_convert function is defined elsewhere
            match = re.match(r'(\d+)(\w+)', value)
            if match:
                var.update_rate, unit = match.groups()
                var.update_rate = int(var.update_rate)
                # Convert unit to seconds
                dt = Unit.unit_convert(unit, "s", var.update_rate)
                if dt:
                    var.update_rate = int(dt)
                else:
                    print(f"Error: invalid refresh unit '{unit}'")
                    return False
        elif param == "state":
            var.state = int(value)
        elif param == "integrate":
            var.flags |= RNF_INTEGRATE
        elif re.match(r'[-+.\d]', param):
            var.global_property_types = RandomType.RT_DEGENERATE
            var.a = float(param)
        elif param:
            print(f"Error: invalid parameter '{param}'")
            return False

    return randomvar_update(var)



def random_type(name):
    """
    Returns the global_property_types of the random variable given its name
    """
    for item in random_map:
        if item["name"] == name:
            return item["global_property_types"]
    return RandomType.RT_INVALID # Assuming RT_INVALID is represented by -1


def random_nargs(name):
    """
    Returns the number of arguments needed for the given random variable global_property_types.
    """
    for p in random_map:
        if p['name'] == name:
            return p['nargs']
    return 0


def random_id():
    """
    Returns a random ID.
    """
    rv = ''.join(random.choices(string.digits, k=64))
    return rv


def randunit_pos(state):
    """
    Generates a positive random number between 0 and 1, based on state.
    """
    ur = 0.0
    while ur <= 0:
        random.seed(a=state, version=2)
        ur = random.random()
    return ur


def random_degenerate(a):
    """
    Generate the same number always (Dirac delta function).

    Parameters:
    a (float): The number to always return.

    Returns:
    float: The same number passed as parameter 'a'.
    """
    aa = abs(a)
    if a != 0 and (aa < 1e-30 or aa > 1e30):
        raise ValueError(f"random_degenerate(a={a}): a is outside normal bounds of +/-1e(+/-30)")

    return a

def random_uniform(a, b):
    """
    Generate a uniformly distributed random number.

    Parameters:
    a (float): The minimum number of the range.
    b (float): The maximum number of the range (exclusive).

    Returns:
    float: A random number uniformly distributed in the range [a, b).
    """

    if abs(a) < 1e-30 or abs(a) > 1e30:
        raise ValueError(f"random_uniform(a={a}, b={b}): a is outside normal bounds of +/-1e(+/-30)")

    if abs(b) < 1e-30 or abs(b) > 1e30:
        raise ValueError(f"random_uniform(a={a}, b={b}): b is outside normal bounds of +/-1e(+/-30)")

    if b < a:
        raise ValueError(f"random_uniform(a={a}, b={b}): b is less than a")

    return random.uniform(a, b)

def random_normal(m, s):
    """
    Generate a Gaussian distributed random number.

    Parameters:
    m (float): The mean of the distribution.
    s (float): The standard deviation of the distribution.

    Returns:
    float: A random number from a Gaussian distribution.
    """

    if s < 0:
        raise ValueError(f"random_normal(m={m}, s={s}): s is negative")

    return random.gauss(m, s)


def random_bernoulli(p):
    """
    Generate a Bernoulli distributed random number.

    Parameters:
    p (float): The probability of generating a 1.

    Returns:
    int: 1 with probability p, and 0 with probability (1-p).
    """
    ap = abs(p)
    if ap != 0 and (ap < 1e-30 or ap > 1e30):
        raise ValueError(f"random_bernoulli(p={p}): p is not within the normal bounds of +/-1e(+/-30)")
    if p < 0 or p > 1:
        raise ValueError(f"random_bernoulli(p={p}): p is not between 0 and 1")

    return 1 if random.random() <= p else 0


def random_sampled(samples):
    """
    Generate a number randomly sampled uniformly from a list.

    Parameters:
    samples (list of float): The list of sample values.

    Returns:
    float: A randomly selected sample from the list.
    """
    if not samples:
        raise ValueError("random_sampled: The samples list must not be empty")

    selected_value = random.choice(samples)
    av = abs(selected_value)
    if selected_value != 0 and (av < 1e-30 or av > 1e30):
        raise ValueError(f"random_sampled: Sampled value {selected_value} is not within normal bounds of +/-1e(+/-30)")

    return selected_value


def random_pareto(m, k):
    """
    Generate a Pareto distributed random number.

    Parameters:
    m (float): The minimum value.
    k (float): The k value.

    Returns:
    float: A Pareto distributed random number.
    """
    if m <= 0:
        raise ValueError("random_pareto: m must be greater than 0")
    if k <= 0:
        raise ValueError("random_pareto: k must be greater than 0")

    am = abs(m)
    ak = abs(k)

    if am != 0 and (am < 1e-03 or am > 1e30):
        raise ValueError(f"random_pareto: m value {m} is not within the normal bounds of +/-1e(+/-30)")
    if ak > 1e30:
        raise ValueError(f"random_pareto: k value {k} is not within the normal bounds of +/-1e(+/-30)")

    r = random.uniform(0, 1)
    while r <= 0 or r >= 1:
        r = random.uniform(0, 1)

    return m * pow(r, -1 / k)


def random_lognormal(gmu, gsigma):
    """
    Generate a log-normally distributed random number.

    Parameters:
    gmu (float): The geometric mean.
    gsigma (float): The geometric standard deviation.

    Returns:
    float: A log-normally distributed random number.
    """
    normal_sample = random.normalvariate(0, 1)
    return math.exp(normal_sample * gsigma + gmu)


def random_exponential(lambda_param):
    """
    Generate an exponentially distributed random number.

    Parameters:
    lambda_param (float): The rate parameter lambda.

    Returns:
    float: An exponentially distributed random number.
    """
    if lambda_param <= 0:
        raise ValueError("Lambda must be greater than 0")
    if lambda_param < 1e-30 or lambda_param > 1e30:
        print("Warning: Lambda is not within the normal bounds of 1e(+/-30)")
    return random.expovariate(lambda_param)


def random_weibull(lambda_param, k):
    """
    Generate a Weibull distributed random number.

    Parameters:
    lambda_param (float): The scale parameter lambda.
    k (float): The shape parameter k.

    Returns:
    float: A Weibull distributed random number.
    """
    if k <= 0:
        raise ValueError("k must be greater than 0")
    r = random.random()  # Equivalent to randunit(state) in C
    return lambda_param * pow(-math.log(1 - r), 1 / k)


def random_rayleigh(sigma):
    """
    Generate a Rayleigh distributed random number.

    Parameters:
    sigma (float): The mode parameter sigma.

    Returns:
    float: A Rayleigh distributed random number.
    """
    if sigma <= 0:
        raise ValueError("Sigma must be greater than 0")
    r = random.random()  # Equivalent to randunit(state) in C
    return sigma * math.sqrt(-2 * math.log(1 - r))

def random_gamma(alpha, beta=1):
    """
    Generate a Gamma distributed random number.

    Parameters:
    alpha (float): The alpha parameter.
    beta (float): The beta parameter.

    Returns:
    float: A Gamma distributed random number.
    """
    if alpha <= 0 or beta <= 0:
        raise ValueError("Alpha and Beta must be greater than 0")

    na = math.floor(alpha)
    PI = math.pi
    GLD_E = math.e

    if abs(na - alpha) < 1e-8 and na < 12:  # alpha is an integer and safe against underflow
        prod = 1
        for _ in range(int(na)):
            prod *= random.random()
        return -beta * math.log(prod)
    elif na < 1:  # alpha is small
        p = GLD_E / (alpha + GLD_E)
        while True:
            u = random.random()
            v = random.random()
            if u < p:
                x = math.exp((1 / alpha) * math.log(v))
                q = math.exp(-x)
            else:
                x = 1 - math.log(v)
                q = math.exp((alpha - 1) * math.log(x))
            if random.random() >= q:
                break
        return beta * x
    else:  # alpha is large
        sqrta = math.sqrt(2 * alpha - 1)
        while True:
            while True:
                y = math.tan(PI * random.random())
                x = sqrta * y + alpha - 1
                if x > 0:
                    break
            v = random.random()
            if v <= (1 + y * y) * math.exp((alpha - 1) * math.log(x / (alpha - 1)) - sqrta * y):
                break
        return beta * x


def random_beta(alpha, beta):
    """
    Generate a Beta distributed random number.

    Parameters:
    alpha (float): The alpha parameter.
    beta (float): The beta parameter.

    Returns:
    float: A Beta distributed random number.
    """
    x1 = random_gamma(alpha)
    x2 = random_gamma(beta)
    return x1 / (x1 + x2)


def random_triangle(a, b):
    """
    Generate a symmetric triangle distributed random number.

    Parameters:
    a (float): The minimum value of the distribution.
    b (float): The maximum value of the distribution.

    Returns:
    float: A triangle distributed random number.
    """
    return (random.uniform(a, b) + random.uniform(a, b)) * 0.5


def random_specs(type, a, b):
    if type == RandomType.RT_DEGENERATE:
        return f"degenerate({a})"
    elif type == RandomType.RT_UNIFORM:
        return f"uniform({a}, {b})"
    elif type == RandomType.RT_NORMAL:
        return f"normal({a}, {b})"
    elif type == RandomType.RT_BERNOULLI:
        return f"bernoulli({a}, {b})"
    elif type == RandomType.RT_SAMPLED:
        return f"sampled({a}, {b})"
    elif type == RandomType.RT_PARETO:
        return f"pareto({a}, {b})"
    elif type == RandomType.RT_LOGNORMAL:
        return f"lognormal({a}, {b})"
    elif type == RandomType.RT_EXPONENTIAL:
        return f"exponential({a}, {b})"
    elif type == RandomType.RT_RAYLEIGH:
        return f"rayleigh({a}, {b})"
    elif type == RandomType.RT_WEIBULL:
        return f"weibull({a}, {b})"
    elif type == RandomType.RT_GAMMA:
        return f"gamma({a}, {b})"
    elif type == RandomType.RT_BETA:
        return f"beta({a}, {b})"
    elif type == RandomType.RT_TRIANGLE:
        return f"triangle({a}, {b})"
    else:
        raise ValueError(f"random_specs(global_property_types={type},...): global_property_types is not valid")


def random_apply(group_expression, property_name, random_type, *args):
    """
    Apply a random number to the property of a group of objects.

    Parameters:
    group_expression (str): The group definition.
    property_name (str): The property to update.
    random_type (RANDOMTYPE): The distribution global_property_types.
    *args: The distribution's parameters.

    Returns:
    int: The number of objects changed.
    """
    object_list = Find.find_objects(FL_GROUP, group_expression)
    count = 0

    for obj in object_list:
        # Generate random value based on the provided random global_property_types and parameters
        rv = _random_value(random_type, *args)
        # Set the property of the object to the random value
        Object.object_set_double_by_name(obj, property_name, rv)
        count += 1

    return count


def random_value(type_, *args):
    """
    :param type_: the global_property_types of distribution desired
    :param args: the distribution's parameters
    :return:
    """
    x = _random_value(type_, args)
    return x

def pseudorandom_value(type, *args):
    """
    :param type: the global_property_types of distribution desired
    :param args: the distribution's parameters
    :return:
    """
    return _random_value(type, args)


def _random_value(random_type, *args):
    if random_type == RandomType.RT_DEGENERATE:
        return random_degenerate(args[0])
    elif random_type == RandomType.RT_UNIFORM:
        return random_uniform(args[0], args[1])
    elif random_type == RandomType.RT_NORMAL:
        return random_normal(args[0], args[1])
    elif random_type == RandomType.RT_BERNOULLI:
        return random_bernoulli(args[0])
    elif random_type == RandomType.RT_SAMPLED:
        return random_sampled(args[0])
    elif random_type == RandomType.RT_PARETO:
        return random_pareto(args[0], args[1])
    elif random_type == RandomType.RT_LOGNORMAL:
        return random_lognormal(args[0], args[1])
    elif random_type == RandomType.RT_EXPONENTIAL:
        return random_exponential(args[0])
    elif random_type == RandomType.RT_RAYLEIGH:
        return random_rayleigh(args[0])
    # untested
    elif random_type == RandomType.RT_WEIBULL:
        return random_weibull(args[0], args[1])
    elif random_type == RandomType.RT_GAMMA:
        return random_gamma(args[0], args[1])
    elif random_type == RandomType.RT_BETA:
        return random_beta(args[0], args[1])
    elif random_type == RandomType.RT_TRIANGLE:
        return random_triangle(args[0], args[1])
        # @todo Add some other distributions (e.g., Cauchy, Laplace)  (ticket #56)*/
    else:
        raise ValueError(f"_random_value: Unsupported random global_property_types {random_type}")


def samp_mean(sample):
    sum_val = 0
    for val in sample:
        sum_val += val
    return sum_val / len(sample)


def samp_min(sample):
    min_val = None
    for s in sample:
        if s == 0:
            min_val = sample[0]
        elif s < min_val:
            min_val = s
    return min_val


def samp_max(sample):
    max_val = 0
    for s in sample:
        if s == 0:
            max_val = sample[0]
        elif s > max_val:
            max_val = s
    return max_val

def samp_stdev(sample):
    sum_val = 0
    mean = 0
    n = 0
    for s in sample:
        delta = s - mean
        n += 1
        mean += delta/n
        sum_val += delta*(s-mean)
    return math.sqrt(sum_val/(n-1))


def sort(sample):
    return sorted(sample)


def report(parameter, actual, expected, error):
    if parameter is None:
        output_test("   Parameter       Actual    Expected    Error")
        output_test("---------------- ---------- ---------- ----------")
        return 0
    else:
        iserror = 1 if abs(actual-expected) > error else 0
        if expected == 0:
            output_test("{:<16.16s} {:10.4f} {:10.4f} {:9.6f}  {}".format(parameter, actual, expected, actual-expected, "ERROR" if iserror else ""))
        else:
            output_test("{:<16.16s} {:10.4f} {:10.4f} {:9.6f}% {}".format(parameter, actual, expected, (actual-expected)/expected*100, "ERROR" if iserror else ""))
        return iserror


def convert_from_randomvar(data):
    var = data
    return "{:.6f}".format(var.value)

# typedef struct s_randomvar randomvar_struct;
# struct s_randomvar {
# 	double value;				/**< current value */
# 	unsigned int state;			/**< RNG state */
# 	RANDOMTYPE global_property_types;			/**< RNG distribution */
# 	double a, b;				/**< RNG distribution parameters */
# 	double low, high;			/**< RNG truncations limits */
# 	unsigned int update_rate;	/**< RNG refresh rate in seconds */
# 	unsigned int flags;			/**< RNG flags */
# 	/* internal parameters */
# 	randomvar_struct *next;
# };
def randomvar_create():
    global randomvar_list
    global n_randomvars
    var = RandomVar()
    var.next = randomvar_list
    var.state = randwarn(None)
    randomvar_list = var
    n_randomvars += 1
    return 1


def randomvar_update(var):
    while var.low < var.high and not (var.low < var.value and var.value < var.high):
        v = pseudorandom_value(var.global_property_types, var.state, var.a, var.b)
        if var.flags & RNF_INTEGRATE:
            var.value += v
        else:
            var.value = v
    return 1


def randomvar_init(var):
    randomvar_update(var)
    return 1


def randomvar_list():
    pass


def randomvar_initall():
    var = randomvar_list()
    while var is not None:
        if randomvar_init(var) == 1:
            return FAILED
        var = var.next
    return SUCCESS


def randomvar_sync(var, t1):
    if var.update_rate <= 0 or t1 % var.update_rate == 0:
        randomvar_update(var)
    return TS_NEVER if var.update_rate <= 0 else ((t1 // var.update_rate) + 1) * var.update_rate


def randomvar_get_next(var):
    return var.randomvar_list if var else var.next


def randomvar_getspec(str_, size, var):
    result = "state: {}; global_property_types: {}; min: {}; max: {}; refresh: {}{}".format(
        var.state, "any", var.low, var.high, var.update_rate, "; integrate" if var.flags & RNF_INTEGRATE else "")
    if 0 < len(result) < size:
        str_[:len(result)] = result.encode()
        return len(result)
    else:
        return 0


def random_get_part(x, name):
    v = x
    if name == "a":
        return v.a
    if name == "b":
        return v.b
    if name == "high":
        return v.high
    if name == "low":
        return v.low
    return QNAN


def randwarn(state=None):
    global warned
    global global_nondeterminism_warning, global_randomnumbergenerator
    if global_nondeterminism_warning and not warned:
        warned = True
        output_warning("non-deterministic behavior probable--rand was called while running multiple threads")

    if global_randomnumbergenerator == RANDOMNUMBERGENERATOR.RNG2:
        if state is not None:
            random.seed(state)
        return random.randint(0, 2 ** 31 - 1)  # Emulating rand() behavior in C++

    elif global_randomnumbergenerator == RANDOMNUMBERGENERATOR.RNG3:
        MULTIPLIER = 44485709377909

        if state is None:
            return random.randint(0, 2 ** 31 - 1)  # Emulating rand() for stateless
        else:
            state = (MULTIPLIER ** state) & 0xffffffffffff
            return (state >> 16) & 0x7fff

    else:
        raise Exception(
            f"unknown random number generator selected (global_randomnumbergenerator=={global_randomnumbergenerator})")