import datetime
import threading
import time

from gov_pnnl_goss.gridlab.climate.CsvReader import ISLEAPYEAR
from gov_pnnl_goss.gridlab.climate.Test import DATETIME
from gov_pnnl_goss.gridlab.gldcore.Convert import output_error, FMT_INT64
from gov_pnnl_goss.gridlab.gldcore.Globals import SUCCESS, global_thread_count, FAILED
from gov_pnnl_goss.gridlab.gldcore.GridLabD import TS_NEVER, TS_ZERO, local_datetime, TS_INVALID, convert_to_timestamp, \
    mkdatetime, convert_from_timestamp
from gov_pnnl_goss.gridlab.gldcore.Output import output_debug, output_warning, output_test, output_verbose

pthread_mutex = threading.Lock()

SCHEDULE_MAGIC = 0x47ab617e

MAXNAME = 64
MAXDEFINITION = 65536
MAXCALENDARS = 14
MAXMINUTES = 366 * 24 * 60
MAXBLOCKS = 4
MAXVALUES = 64

SN_NORMAL =  0x0001	 # schedule normalization flag - normalize enabled */
SN_ABSOLUTE =0x0002	 # schedule normalization flag - use absolute values */
SN_WEIGHTED= 0x0004	 # schedule normalization flag - use weighted values */
SN_INTERPOLATED =0x0008	 #s chedule values are interpolated between defined values */
SN_BOOLEAN =0x8000  # schedule is boolean (only one/zero values are expected) */
SN_NONZERO =0x4000  # schedule is non-zero (no zero values are expected) */
SN_POSITIVE =0x2000  # schedule is positive (no negative values are expected) */
SN_IS_NORMALIZED =0x0020  # schedule normalization flag - indicates that the schedule has been nomalized already */

# Create locks and conditions
start_lock = threading.Lock()
done_lock = threading.Lock()
start_cond = threading.Condition(start_lock)
done_cond = threading.Condition(done_lock)

# Define global variables
next_t1_sch = 0  # Replace with your initialization
next_t2_sch = float('inf')  # Replace with your initialization
done_count_sch = 0
n_threads_sch = 0

interpolated_schedules = False

# Create and start threads
data1 = {
    'ok': True,
    'sch': [],  # Replace with your list of SCHEDULE objects
    't0': 0,  # Replace with your initialization
}


class SCHEDULESYNCDATA:
    def __init__(self, n, pt, ok, sch, nsch, t0):
        self.n = n
        self.pt = pt
        self.ok = ok
        self.sch = sch
        self.nsch = nsch
        self.t0 = t0

def GET_BLOCK(I):
    return (I >> 6) & 0x02

def GET_VALUE(I):
    return I & 0x3f

SCHEDULEINDEX = int  # Assuming SCHEDULEINDEX is an unsigned 32-bit integer

def GET_CALENDAR(N):
    return (N >> 20) & 0x0f

def GET_MINUTE(N):
    return N & 0x0fffff

def SET_CALENDAR(N, X):
    return N | ((X & 0x0f) << 20)

def SET_MINUTE(N, X):
    return N | (X & 0x0fffff)

class ScheduleTest:
    def __init__(self, name, definition, t1, t2, normalize, value):
        self.name = name
        self.definition = definition
        self.t1 = t1
        self.t2 = t2
        self.normalize = normalize
        self.value = value


class Matcher:
    def __init__(self, name, base, max):
        self.name = name
        self.base = base
        self.max = max
        self.pattern = [0] * 256
        self.table = [0] * 60


class Schedule:
    """
    Schedules are defined as a multiline string

        @par Schedule syntax
        <code>
        // comments are ignored until and end-of-line
        block1-name { // each block must have a unique name
            minutes hours days months weekdays value // uses the crontab format
            minutes hours days months weekdays value // multiple entries separate by newlines or semicolons
        }
        block2-name { // normalization is done over each block
            minutes hours days months weekdays // omitted values a taken to be 1.0
            }
        block3-name { // block are combined
            // omitted entries are taken to be 0.0
        }
        </code>

        Optionally, a simple schedule can be provided

        <code>
        minutes hours days months weekdays value // uses the crontab format
        minutes hours days months weekdays value // multiple entries separate by newlines or semicolons
        </code>
    """

    def __init__(self, name=None, definition=None):

        self.abs = [0.0] * MAXBLOCKS          # < the sum of the absolute values for each block -- used to normalize
        self.block = 0                        # < the last block used (4 max)
        self.blockdef = [""] * MAXBLOCKS      # < the definition of each block
        self.blockname = [""] * MAXBLOCKS     # < the name of each block
        self.checksum = 0
        self.count = [0] * MAXBLOCKS          # < the number of values given in each block
        self.data = [0.0] * (MAXBLOCKS * MAXNAME)  # < the list of values used in each block
        self.definition = definition          # < the definition string of the schedule
        self.done_sch = 0                     # PTHREAD_COND_INITIALIZER
        self.donecount_sch = 0
        self.donelock_sch = 0                 # PTHREAD_MUTEX_INITIALIZER
        self.dtnext = [[]] * MAXCALENDARS     # < the time until the next schedule change (in minutes)
        self.duration = 0.0                   # < the duration of the current scheduled value (in hours)
        self.flags = 0                        # < the schedule flags (see SN_*)
        self.fraction = 0.0                   # < the fractional weight of the block of the current value (pu time)
        self.index = [[]] * MAXCALENDARS      # < the schedule index (enough room for all 14 annual calendars to 1 minute resolution)
        self.magic1 = 0                       # < values between magic1 and magic2 should never change once compiled
        self.magic2 = SCHEDULE_MAGIC          #
        self.minutes = [0] * MAXBLOCKS        # < the total number of minutes associate with each block
        self.n_schedules = None
        self.n_threads = None
        self.name = name                      # < the name of the schedule
        self.next_schedule = None             #
        self.next_t = TS_NEVER                # < the time of the next schedule event
        self.next_t1_sch = 0
        self.next_t2_sch = TS_ZERO
        self.sc_active = False                #
        self.sc_activelock = None             #
        self.sc_done = False                  #
        self.sc_running = False               #
        self.sc_started = False               #
        self.sc_status = SUCCESS              #
        self.schedule_list: [Schedule] = []   #
        self.since = TS_ZERO                  #
        self.start_sch = 0                    # PTHREAD_COND_INITIALIZER
        self.startlock_sch = 0                # PTHREAD_MUTEX_INITIALIZER
        self.schedule_synctime = 0
        self.sum = [0.0] * MAXBLOCKS          # < the sum of values for each block -- used to normalize
        self.value = 0.0                      # < the current scheduled value
        self.weight = [0] * (MAXBLOCKS * MAXNAME)  # < the weight (in minutes) associate with each value


    def schedule_checksum(self, sch):
        sum = 0
        ptr = id(sch) + 1
        while ptr < id(sch) + self.magic2:
            sum ^= ptr.contents
            ptr += 1
        return sum

    def schedule_get_first(self, ):
        return self.schedule_list

    def schedule_get_next(self, sch):
        return self.schedule_list if sch is None else sch.next

    def schedule_find_by_name(self, name):
        sch = self.schedule_list
        while sch is not None:
            if sch.name == name:
                return sch
            sch = sch.next
        return None

    def schedule_matcher(self, pattern, table, max, base):
        go = 0
        start = 0
        stop = -1
        range_ = 0
        p = pattern
        table.fill(0)

        while True:
            if p == '':
                go = 1
            elif p[0] == '*':
                start = base
                stop = max
                go = 1
                p = p[1:]
            elif p[0] == ',':
                go = 1
                p = p[1:]
            elif p[0] == '-':
                range_ = 1
                stop = 0
                p = p[1:]
            elif '0' <= p[0] <= '9':
                if range_:
                    stop = stop * 10 + int(p[0])
                else:
                    stop = start = start * 10 + int(p[0])
                p = p[1:]
            else:
                return 0

            if go and stop >= 0:
                if start < base:
                    print(f"schedule_matcher(pattern='{pattern}',...) start before min of {base}")
                    start = base

                if stop > max:
                    print(f"schedule_matcher(pattern='{pattern}',...) end exceed max of {max}")
                    stop = max

                if start > stop:
                    for i in range(start, max + 1):
                        table[i - base] = 1
                    for i in range(base, stop + 1):
                        table[i - base] = 1
                else:
                    for i in range(start, stop + 1):
                        table[i - base] = 1

                start = 0
                range_ = 0
                go = 0
                stop = -1

            if p == '':
                break

        return 1

    def find_value_index(self, block, value):
        for ndx in range(self.count[block]):
            if float(self.data[block * MAXVALUES + ndx]) == float(value):
                return ndx
        return -1

    def schedule_compile_dtnext(self, calendar):
        # Construct the dtnext array
        invariant = True

        # Number of minutes that are indexed
        t = MAXMINUTES - 1

        # Assume that loopback results in a value change in 1 minute
        self.dtnext[calendar][t] = 1

        # Scan backwards through time
        for t in range(t - 1, -1, -1):
            # Get this and the next index to values
            index0 = self.index[calendar][t]
            index1 = self.index[calendar][t + 1]

            # If the values are the same
            if self.data[index0] == self.data[index1]:
                # If we haven't reached the maximum delta-t (for unsigned char dtnext)
                if self.dtnext[calendar][t + 1] < 255:
                    # Add 1 minute to next value's time
                    self.dtnext[calendar][t] = self.dtnext[calendar][t + 1] + 1
                else:
                    # Start the time over at 1 minute (to next value)
                    self.dtnext[calendar][t] = 1
            else:
                # Start the time over at 1 minute (to next value)
                self.dtnext[calendar][t] = 1
                invariant = False

        # Special case for invariant schedule
        if invariant:
            self.dtnext[calendar] = [0] * MAXMINUTES  # Zero means never

        # Check for gaps in the schedule
        else:
            ngaps = 0
            ingap = False

            for t in range(MAXVALUES - 1):
                if self.dtnext[calendar][t] == 0 and not ingap:
                    day = t // 60 // 24
                    hour = t // 60 - day * 24
                    minute = t - hour * 60 - day * 24 * 60
                    print(
                        f"schedule '{self.name}' gap in calendar {calendar} at day {day}, hour {hour}, minute {minute} lasting {self.dtnext[calendar][t]} minutes")
                    ingap = True
                    ngaps += 1
                elif self.dtnext[calendar][t] != 0 and ingap:
                    ingap = False

            if ngaps > 0:
                print(f"schedule '{self.name}' has {ngaps} gaps which may cause erroneous results")
                return 0

        return 1

    def schedule_compile_block(self, block, blockname, blockdef):
        token = None
        minute = 0

        # Check block count
        if block >= MAXBLOCKS:
            print(f"schedule_compile(SCHEDULE *sch={{name={self.name}, ...}}) maximum number of blocks reached")
            # TROUBLESHOOT: The schedule definition has too many blocks to compile. Consolidate your schedule and try again.
            return 0

        # First index is always default value 0
        self.count[block] = 1

        while True:
            token = blockdef if token is None else None


            # Remove leading whitespace
            while token and token.startswith(' '):
                token = token[1:]

            # Skip blank lines
            if not token:
                continue

            # Check for normalization, etc
            if token == "nonzero":
                self.flags |= SN_NONZERO
                continue
            elif token == "positive":
                self.flags |= SN_POSITIVE
                continue
            elif token == "boolean":
                self.flags |= SN_BOOLEAN
                continue
            elif token == "normal":
                self.flags |= SN_NORMAL
                continue
            elif token == "weighted":
                self.flags |= SN_NORMAL | SN_WEIGHTED
                continue
            elif token == "absolute":
                self.flags |= SN_NORMAL | SN_ABSOLUTE
                continue
            elif token == "interpolated":
                self.flags |= SN_INTERPOLATED
                interpolated_schedules = True
                continue
            matcher = [
                Matcher("minute", 0, 59),
                Matcher("hour", 0, 23),
                Matcher("day", 1, 31),
                Matcher("month", 1, 12),
                Matcher("weekday", 0, 8),
            ]

            # At this point, we assume a line that needs parsing
            # Value can be missing -> defaults to 1.0

            value = 1.0  # Default value is 1.0
            if len(token.split()) < 5 or not all(matcher[i].pattern in token for i in range(5)) or not (
                    len(token.split()) >= 6 and token.split()[-1].replace(".", "", 1).isdigit()):
                print(
                    f"schedule_compile(SCHEDULE *sch={{name={self.name}, ...}}) ignored an invalid definition '{token}'")
                # TROUBLESHOOT: The schedule definition is not valid and has been ignored. Check the syntax of your schedule and try again.
                continue
            else:
                # A valid line was scanned
                if (ndx := self.find_value_index(block, value)) == -1:
                    ndx = self.count[block]
                    # Bound checking
                    if ndx > MAXVALUES - 1:
                        print(
                            f"schedule_compile(SCHEDULE *sch={{name={self.name}, ...}}) maximum number of values reached in block {block}")
                        return 0
                    self.data[block * MAXVALUES + ndx] = value
                self.sum[block] += value
                self.abs[block] += abs(value)

            # Compile matching tables
            for match in matcher:
                # Get match tables
                if not self.schedule_matcher(match.pattern, match.table, match.max, match.base):
                    print(
                        f"schedule_compile(SCHEDULE *sch={{name={self.name}, ...}}) {match.name} pattern syntax error in item '{token}'")
                    # TROUBLESHOOT: The schedule definition is not valid and has been ignored. Check the syntax of your schedule and try again.
                    return 0

            # Load schedule based on the weekday of Jan 1
            for calendar in range(MAXCALENDARS):
                weekday = calendar % 7
                is_leapyear = 1 if calendar >= 7 else 0
                calendar = weekday * 2 + is_leapyear
                days = [31, 29 if is_leapyear else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
                n = block * MAXVALUES + ndx
                if ndx == -2:
                    print(f"schedule_compile(SCHEDULE *sch={{name={self.name}, ...}}) internal index error")
                    return 0
                minute = 0
                for month in range(12):
                    day = 0
                    if not matcher[3].table[month]:
                        minute += 60 * 24 * days[month]
                        weekday += days[month]
                        continue
                    for day in range(days[month]):
                        weekday %= 7  # Wrap day of the week
                        if not matcher[4].table[weekday] or not matcher[2].table[day]:
                            minute += 60 * 24
                            continue
                        for hour in range(24):
                            stop = minute + 60
                            if not matcher[1].table[hour]:
                                minute = stop
                                continue
                            while minute < stop:
                                if matcher[0].table[minute % 60]:
                                    if self.index[calendar] is not None and self.index[calendar][minute] > 0:
                                        dayofweek = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun", "Hol"]
                                        print(
                                            f"schedule_compile(SCHEDULE *sch={{name={self.name}, ...}}) '{token}' in block '{blockname}' has a conflict with value {self.data[self.index[calendar][minute]]} on {dayofweek[weekday]} {month + 1}/{day + 1} {hour:02d}:{minute % 60:02d}")
                                        # TROUBLESHOOT: The schedule definition is not valid and has been ignored. Check the syntax of your schedule and try again.
                                        return 0
                                    else:
                                        # Associate this time with the current value
                                        if self.index[calendar] is not None:
                                            self.index[calendar][minute] = n
                                        self.weight[n] += 1
                                        self.minutes[block] += 1
                                minute += 1

        self.blockname[block] = blockname

        if self.blockname[block] is None:
            print(f"schedule_compile(SCHEDULE *sch={{name={self.name}, ...}}) insufficient memory for block name")
            return 0

        return 1

    def schedule_recompile_block(self, calendar, block, blockname, blockdef):
        token = None
        minute = 0

        if self.index[calendar] is None:
            print(f"schedule_recompile(SCHEDULE *sch={{name={self.name}, ...}}) sch->index was NULL")
            return 0

        # Check block count
        if block >= MAXBLOCKS:
            print(f"schedule_recompile(SCHEDULE *sch={{name={self.name}, ...}}) block index out of bounds")
            return 0

        while True:
            token = blockdef if token is None else None

            # Remove leading whitespace
            while token and token.startswith(' '):
                token = token[1:]

            # Skip blank lines
            if not token:
                continue

            # Check for normalization, etc
            if token == "nonzero":
                continue
            elif token == "positive":
                continue
            elif token == "boolean":
                continue
            elif token == "normal":
                continue
            elif token == "weighted":
                continue
            elif token == "absolute":
                continue
            elif token == "interpolated":
                continue

            # At this point, we assume a line that needs parsing
            # Value can be missing -> defaults to 1.0
            matchers = [
                Matcher("minute", 0, 59),
                Matcher("hour", 0, 23),
                Matcher("day", 1, 31),
                Matcher("month", 1, 12),
                Matcher("weekday", 0, 8)]

            value = 1.0  # Default value is 1.0
            ndx = -2

            # Remove leading whitespace
            while token and token[0].isspace():
                token = token[1:]

            # Skip blank lines
            if not token or token == "":
                continue

            # Check for normalization, etc
            if token in ["nonzero", "positive", "boolean", "normal", "weighted", "absolute", "interpolated"]:
                continue

            # At this point, we assume a line that needs parsing
            # Value can be missing -> defaults to 1.0
            if len(token.split()) < 5 or not all(matcher.pattern in token for matcher in matchers) or not (
                    len(token.split()) >= 6 and token.split()[-1].replace(".", "", 1).isdigit()):
                print(
                    f"schedule_recompile(SCHEDULE *sch={{name={self.name}, ...}}) ignored an invalid definition '{token}'")
                # TROUBLESHOOT: The schedule definition is not valid and has been ignored. Check the syntax of your schedule and try again.
                continue
            else:
                # A valid line was scanned
                if self.flags & SN_IS_NORMALIZED == SN_IS_NORMALIZED:
                    if self.flags & SN_WEIGHTED == SN_WEIGHTED:
                        print(
                            f"schedule_recompile(SCHEDULE *sch={{name={self.name}, ...}}) has a weighted normalization")
                        # TROUBLESHOOT: The schedule is categorized as a weighted normalization. Unfortunately, recompiling this for a new year
                        # requires information that is not present. Avoid running these types of schedules over year transitions.
                        return 0
                    elif self.flags & SN_ABSOLUTE == SN_ABSOLUTE:
                        value /= self.abs[block]
                    else:
                        value /= self.sum[block]

                if (ndx := self.find_value_index(block, value)) == -1:
                    print(f"schedule_recompile(SCHEDULE *sch={{name={self.name}, ...}}) unable to find value")
                    return 0

            # Compile matching tables
            for match in matchers:
                # Get match tables
                if not self.schedule_matcher(match.pattern, match.table, match.max, match.base):
                    print(
                        f"schedule_recompile(SCHEDULE *sch={{name={self.name}, ...}}) {match.name} pattern syntax error in item '{token}'")
                    # TROUBLESHOOT: The schedule definition is not valid and has been ignored. Check the syntax of your schedule and try again.
                    return 0

            # Load schedule based on the weekday of Jan 1
            is_leapyear = calendar % 2
            weekday = calendar // 2
            days = [31, 29 if is_leapyear else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            n = block * MAXVALUES + ndx
            if ndx == -2:
                print(f"schedule_recompile(SCHEDULE *sch={{name={self.name}, ...}}) internal index error")
                return 0
            minute = 0
            for month in range(12):
                day = 0
                if not matchers[3].table[month]:
                    minute += 60 * 24 * days[month]
                    weekday += days[month]
                    continue
                for day in range(days[month]):
                    weekday %= 7  # Wrap day of the week
                    if not matchers[4].table[weekday] or not matchers[2].table[day]:
                        minute += 60 * 24
                        continue
                    for hour in range(24):
                        stop = minute + 60
                        if not matchers[1].table[hour]:
                            minute = stop
                            continue
                        while minute < stop:
                            if matchers[0].table[minute % 60]:
                                if self.index[calendar][minute] > 0:
                                    dayofweek = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun", "Hol"]
                                    print(
                                        f"schedule_recompile(SCHEDULE *sch={{name={self.name}, ...}}) "
                                        f"'{token}' in block '{blockname}' has a conflict with value "
                                        f"{self.data[self.index[calendar][minute]]} on "
                                        f"{dayofweek[weekday]} {month + 1}/{day + 1} {hour:02d}:{minute % 60:02d}")
                                    # TROUBLESHOOT: The schedule definition is not valid and has been ignored.
                                    # Check the syntax of your schedule and try again.
                                    return 0
                                else:
                                    # Associate this time with the current value
                                    self.index[calendar][minute] = n
                            minute += 1
        return 1

    def schedule_recompile(self, calendar):
        block = 0

        if self.index[calendar] is None:
            self.index[calendar] = [0] * MAXMINUTES
            if self.index[calendar] is None:
                print(f"schedule_recompile(SCHEDULE *sch={{name={self.name}, ...}}) insufficient memory for index")
                return 0
            self.index[calendar] = [0] * MAXMINUTES

        if self.dtnext[calendar] is None:
            self.dtnext[calendar] = [0] * MAXMINUTES
            if self.dtnext[calendar] is None:
                print(f"schedule_recompile(SCHEDULE *sch={{name={self.name}, ...}}) insufficient memory for dtnext")
                return 0
            self.dtnext[calendar] = [0] * MAXMINUTES

        while block < self.block:
            # schedule_recompile_block uses strtok and corrupts our stored blockdef, use a copy
            blockdef = self.blockdef[block][:MAXDEFINITION]
            if self.schedule_recompile_block(calendar, block, self.blockname[block], blockdef) == 0:
                print(f"schedule_recompile(SCHEDULE *sch={{name={self.name}, ...}}) error recomputing index")
                return 0
            block += 1

        return 1

    def schedule_compile(self):
        p = self.definition
        q = None
        blockdef = [""] * MAXBLOCKS
        blockname = [""] * MAXBLOCKS
        state = "INIT"
        comment = 0

        # Check to see no blocks are defined
        if '{' not in p and '}' not in p:
            # This is a single block unnamed schedule
            # Remove leading whitespace
            p = p.lstrip()
            blockdef[self.block] = p
            self.blockdef[self.block] = p
            if self.schedule_compile_block(self.block, "*", blockdef[self.block]):
                self.block += 1
                return 1
            else:
                return 0

        # Isolate each block
        while p != '':
            # Handle comments
            if p.startswith('#'):
                comment = 1
                p = p[1:]
                continue
            elif comment:
                if p.startswith('\n'):
                    comment = 0
                p = p[1:]
                continue

            if state == "INIT" or state == "CLOSE":
                if not p.isspace() and not p.isascii():
                    if self.block >= MAXBLOCKS:
                        print("maximum number of allowed schedule blocks exceeded")
                        # TROUBLESHOOT: Up to 4 schedule blocks are allowed. Define your schedule so it only uses four blocks and try again.
                        return 0
                    state = "NAME"
                    q = blockname[self.block]
            else:  # space/control
                p = p[1:]

            if state == "NAME":
                if p.isspace() or p.isascii():
                    state = "OPEN"
                    p = p[1:]
                elif p.startswith('{') or p.startswith(';'):
                    state = "OPEN"
                else:
                    if len(q) < MAXNAME - 1:
                        q += p[0]
                    else:
                        print("schedule name is too long")
                        # TROUBLESHOOT: The name given to the schedule is too long to be used. Use a name that is less than 64 characters and try again.
                        return 0

            if state == "OPEN":
                if p.startswith(';'):  # option
                    if blockname[self.block] == "weighted":
                        self.flags |= SN_WEIGHTED
                    elif blockname[self.block] == "absolute":
                        self.flags |= SN_ABSOLUTE
                    elif blockname[self.block] == "normal":
                        self.flags |= SN_NORMAL
                    elif blockname[self.block] == "positive":
                        self.flags |= SN_POSITIVE
                    elif blockname[self.block] == "nonzero":
                        self.flags |= SN_NONZERO
                    elif blockname[self.block] == "boolean":
                        self.flags |= SN_BOOLEAN
                    elif blockname[self.block] == "interpolated":
                        self.flags |= SN_INTERPOLATED
                        interpolated_schedules = True
                    else:
                        print(f"schedule {self.name}: block option '{blockname[self.block]}' is not recognized")
                    state = "CLOSE"
                    p = p[1:]
                elif p.startswith('{'):  # open block
                    state = "BLOCK"
                    q = blockdef[self.block]
                    p = p[1:]
                elif not p.isspace() and not p.isascii():  # non-white/control
                    print(f"schedule {self.name}: unexpected text before block start")
                    # TROUBLESHOOT: The schedule syntax is not valid. Remove the unexpected or invalid text before the block and try again.
                    return 0
                else:  # space/control
                    p = p[1:]

            if state == "BLOCK":
                if p.startswith('}'):  # end block
                    state = "CLOSE"
                    q = None
                    p = p[1:]
                    blockdef[self.block] = q
                    self.blockdef[self.block] = q
                    if self.schedule_compile_block(self.block, blockname[self.block], blockdef[self.block]):
                        self.block += 1
                    else:
                        return 0
                else:
                    if len(q) < MAXDEFINITION - 1:
                        q += p[0]
                    else:
                        print(f"schedule {self.name}: block {blockname[self.block]} definition is too long")
                        # TROUBLESHOOT: The definition given to the schedule is too long to be used. Use a definition that is less than 1024 characters and try again.
                        return 0

        return 1

    def schedule_createproc(self):
        status = SUCCESS

        self.sc_activelock = threading.Lock()
        self.sc_active = threading.Condition(self.sc_activelock)
        global_threadcount = 0  # You should define the actual value of global_thread_count

        with self.sc_activelock:
            while self.sc_running >= global_threadcount:
                output_debug(f"schedule '{self.name}' creation waiting ({self.sc_running} of {global_threadcount} active)")
                self.sc_active.wait()

            self.sc_running += 1
            output_debug(
                f"deferred schedule '{self.name}' creation starting ({self.sc_running} of {global_threadcount} active)")
            self.sc_active.notify_all()

        # Compile the schedule
        if self.schedule_compile():
            for calendar in range(MAXCALENDARS):
                if self.dtnext[calendar] is not None:
                    self.schedule_compile_dtnext(calendar)

            if (self.flags & (SN_NORMAL | SN_ABSOLUTE | SN_WEIGHTED)) != 0:
                self.schedule_normalize(SN_IS_NORMALIZED)

            if (self.flags & (SN_POSITIVE | SN_NONZERO | SN_BOOLEAN)) != 0 and not self.schedule_validate(self.flags):
                status = FAILED
            else:
                self.checksum = self.schedule_checksum()
                output_debug(f"schedule '{self.name}' checksum is {self.checksum}")
        else:
            status = FAILED

        with self.sc_activelock:
            self.sc_running -= 1
            self.sc_done += 1
            if status == FAILED:
                sc_status = status
            self.sc_active.notify_all()

        if status == SUCCESS:
            output_debug(f"deferred creation of schedule '{self.name}' completed")
        else:
            output_error(f"deferred creation of schedule '{self.name}' failed")

        return status

    def schedule_create_wait(self, ):
        if self.sc_running == 0 and self.sc_done == self.sc_started:
            return self.sc_status
        pthread_mutex.acquire(self.sc_activelock)
        while self.sc_running > 0 or self.sc_done < self.sc_started:
            output_debug("waiting for deferred schedule creations to complete (%d of %d active)", self.sc_running, global_threadcount)
            pthread_mutex.wait(self.sc_active,self.sc_activelock)
        output_debug("all deferred schedule creations completed %s", "successfully" if self.sc_status == SUCCESS else "with at least one failure")
        pthread_mutex.acquire(self.sc_activelock)
        return self.sc_status

    def schedule_create(self, name, definition):
        global global_threadcount

        sch = self.schedule_find_by_name(name)

        if sch is not None:
            if definition is not None and sch.definition != definition:
                output_error(
                    f"schedule_create(name='{name}', definition='{definition}') definition does not match previous definition of schedule '{name}'")
            return sch

        if definition is None:
            return None

        sch = Schedule(name, definition)

        if sch is None:
            output_error(f"schedule_create(name='{name}', definition='{definition}') memory allocation failed)")
            return None

        output_debug(f"schedule '{name}' uses {Schedule.__basicsize__ / 1000000.0:.1f} MB of memory")

        if len(name) >= MAXNAME:
            output_error(f"schedule_create(name='{name}', definition='{definition}') name too long)")
            self.schedule_free(sch)
            return None

        sch.definition = definition

        if len(definition) >= MAXDEFINITION:
            output_error(f"schedule_create(name='{name}', definition='{definition}') definition too long)")
            self.schedule_free(sch)
            return None

        self.schedule_add(sch)

        if global_threadcount <= 1:
            result = self.schedule_createproc(sch)
            if result == "SUCCESS":
                return sch
            else:
                self.schedule_free(sch)
                sch = None
                return None
        else:
            if self.n_threads == 0:
                thread_id = threading.Thread(target=self.schedule_createproc, args=(sch,))
                thread_id.start()
                self.sc_started += 1
                return sch

            else:
                output_warning(f"schedule_createproc failed, schedule '{sch.name}' created inline instead")
                return sch if self.schedule_createproc(sch) else None

    def schedule_new(self, global_starttime, MAXMINUTES=1440):

        sch = Schedule()
        sch.index = [None] * 14
        sch.dtnext = [None] * 14

        ONE_WEEK = datetime.timedelta(days=7)
        now = datetime.datetime.utcfromtimestamp(global_starttime)
        dt_starttime = now
        dt_starttime_lo = now - ONE_WEEK
        dt_starttime_hi = now + ONE_WEEK

        cal = ((dt_starttime.weekday() - dt_starttime.timetuple().tm_yday + 53 * 7) % 7) * 2 + (
            1 if dt_starttime.year % 4 == 0 and (dt_starttime.year % 100 != 0 or dt_starttime.year % 400 == 0) else 0)
        cal_lo = ((dt_starttime_lo.weekday() - dt_starttime_lo.timetuple().tm_yday + 53 * 7) % 7) * 2 + (
            1 if dt_starttime_lo.year % 4 == 0 and (dt_starttime_lo.year % 100 != 0 or dt_starttime_lo.year % 400 == 0) else 0)
        cal_hi = ((dt_starttime_hi.weekday() - dt_starttime_hi.timetuple().tm_yday + 53 * 7) % 7) * 2 + (
            1 if dt_starttime_hi.year % 4 == 0 and (dt_starttime_hi.year % 100 != 0 or dt_starttime_hi.year % 400 == 0) else 0)

        for i in [cal, cal_lo, cal_hi]:
            sch.index[i] = [0] * MAXMINUTES
            sch.dtnext[i] = [0] * MAXMINUTES

        sch.since = 0
        sch.next_t = 'NEVER'
        return sch

    def schedule_free(self, sch):
        for i in range(MAXBLOCKS):
            if sch.blockname[i]:
                del sch.blockname[i]
            if sch.blockdef[i]:
                del sch.blockdef[i]
        for i in range(MAXCALENDARS):
            if sch.index[i]:
                del sch.index[i]
            if sch.dtnext[i]:
                del sch.dtnext[i]
        del sch

    def schedule_add(self, schedule):
        schedule.next = self.schedule_list
        self.schedule_list = schedule
        self.n_schedules += 1

    def schedule_validate(self, flags):
        nzct = 0  # Nonzero count
        failed = False

        for b in range(MAXBLOCKS):
            i = 0 if flags & SN_NONZERO else 1
            for _ in range(i, self.count[b] + 1):
                value = self.data[b * MAXVALUES + i]
                weight = self.weight[b * MAXVALUES + i]
                nonzero = weight > 0 and value != 0.0
                boolean = weight > 0 and (value == 0.0 or value == 1.0)
                positive = weight > 0 and value > 0.0

                if weight == 0:
                    continue

                if value != 0.0:
                    nzct += weight

                if flags & SN_BOOLEAN and not boolean:
                    output_error(
                        f"schedule {self.name} fails 'boolean' validation in block {self.blockname[b]} at schedule index {i}")
                    failed = True
                elif flags & SN_POSITIVE and not positive:
                    output_error(
                        f"schedule {self.name} fails 'positive' validation in block {self.blockname[b]} at schedule index {i}")
                    failed = True
                elif flags & SN_NONZERO and not nonzero:
                    output_error(
                        f"schedule {self.name} fails 'nonzero' validation in block {self.blockname[b]} at schedule index {i}")
                    failed = True

        if flags & SN_NONZERO and nzct != (7 * (365 + 366) * 24 * 60):
            output_error(f"schedule {self.name} fails 'nonzero' validation with unfilled entries")
            failed = True

        return not failed

    def schedule_normalize(self, flags):
        count = 0

        # Check if already normalized
        if self.flags & flags:
            return -1

        # Normalize
        for b in range(MAXBLOCKS):
            # Ignore empty blocks
            if self.count[b] == 0:
                continue

            # Weighted normalization
            if self.flags & SN_WEIGHTED == SN_WEIGHTED:
                scale = [0.0] * (self.count[b] + 1)
                nonzero = 0

                for i in range(1, self.count[b] + 1):
                    if self.weight[b * MAXVALUES + i] != 0:
                        nonzero = 1
                        scale[i] += self.data[b * MAXVALUES + i] * self.weight[b * MAXVALUES + i] / self.minutes[b]

                if nonzero:
                    for i in range(1, self.count[b] + 1):
                        self.data[b * MAXVALUES + i] *= scale[i]

            # Unweighted normalization
            else:
                scale = self.abs[b] if self.flags & SN_ABSOLUTE == SN_ABSOLUTE else self.sum[b]

                # If the coefficient is non-zero
                if scale != 0:
                    # Normalize the values
                    count += 1
                    for i in range(1, self.count[b] + 1):
                        self.data[b * MAXVALUES + i] /= scale

        # Mark as normalized
        self.flags |= flags

        return count

    def schedule_index(self, ts):
        ref = 0
        dt = None
        cal = 0
        min = 0
        try:
            dt = local_datetime(ts)

            if dt is None:
                raise Exception("local_datetime function returned None")

            cal = ((dt.weekday - dt.yearday + 53 * 7) % 7) * 2 + ISLEAPYEAR(dt.year)
            min = (dt.yearday * 24 + dt.hour) * 60 + dt.minute

            if cal >= MAXCALENDARS or min >= MAXMINUTES:
                output_error(
                    "schedule_index(): timestamp %" + FMT_INT64 + "d has calendar %d minute %d which is invalid", ts,
                    cal, min)
                return -1

            SET_CALENDAR(ref, cal)
            SET_MINUTE(ref, min)

            if self.index[cal] == 0:
                return_value = self.schedule_recompile(cal)

                if return_value == 0:
                    return -1

                return_value = self.schedule_compile_dtnext(cal)

                if return_value == 0:
                    return -1

            return ref
        except Exception as e:
            output_error(
                "schedule_read(SCHEDULE *schedule={name='%s',...}, TIMESTAMP ts=%" + FMT_INT64 + "d) error: %s",
                self.name, ts, e)
            return -1

    def schedule_value(self, index):
        global MAX_CALENDARS, MAX_MINUTES
        cal = GET_CALENDAR(index)
        minute = GET_MINUTE(index)
        if cal >= MAX_CALENDARS or minute >= MAX_MINUTES:
            output_error("schedule_index(): index %d has calendar %d minute %d which is invalid" % (index, cal, minute))
        return self.data[self.index[cal][minute]]

    def schedule_dtnext(self, index):
        cal = GET_CALENDAR(index)
        min_val = GET_MINUTE(index)
        if cal >= MAX_CALENDARS or min_val >= MAX_MINUTES:
            output_error("schedule_dtnext(): index {} has calendar {} minute {} which is invalid".format(index, cal, min_val))
        return self.dtnext[cal][min_val]

    def schedule_duration(self, schedule, schedule_index):
        global MAX_BLOCKS
        calendar = GET_CALENDAR(schedule_index)
        minute = GET_MINUTE(schedule_index)
        block = 0
        if calendar >= MAX_CALENDARS or minute >= MAX_MINUTES:
            output_error("schedule_duration(): index %d has calendar %d minute %d which is invalid" % (schedule_index, calendar, minute))
        block = (schedule.index[calendar][minute] >> 6) & MAX_BLOCKS
        return schedule.minutes[block]

    def schedule_weight(self, sch, index):
        cal = GET_CALENDAR(index)
        minutes = GET_MINUTE(index)
        if cal >= MAX_CALENDARS or minutes >= MAX_MINUTES:
            output_error("schedule_weight(): index {} has calendar {} minute {} which is invalid".format(index, cal, minutes))
        return sch.weight[sch.index[cal][minutes]]

    def schedule_dump_all(self, file):
        sch = self.schedule_list
        while sch is not None:
            self.schedule_dump(sch, file, "w" if sch == self.schedule_list else "a")
            sch = sch.next

    def schedule_sync(self, t):
        if self.magic1 != SCHEDULE_MAGIC or self.magic2 != SCHEDULE_MAGIC:
            output_warning("schedule '%s' may be corrupted", self.name)

        if self.flags & SN_INTERPOLATED == SN_INTERPOLATED:
            if self.since == TS_ZERO or t >= self.next_t:
                index = self.schedule_index(t)
                if index < 0:
                    return TS_INVALID
                dtnext = self.schedule_dtnext(index) * 60
                self.since = self.since if self.since != TS_ZERO else t
                self.duration = self.schedule_duration(self, index) / 60.0
                self.next_t = TS_NEVER if dtnext == 0 else t + dtnext - t % 60
                if self.next_t == TS_NEVER:
                    self.value = self.schedule_value(index)

            if self.next_t != TS_NEVER:
                start_index = self.schedule_index(self.since)
                end_index = self.schedule_index(self.next_t)
                if start_index < 0 or end_index < 0:
                    return TS_INVALID
                start_value = self.schedule_value(start_index)
                end_value = self.schedule_value(end_index)
                self.value = start_value + ((end_value - start_value) * ((t - self.since) / (self.next_t - self.since)))
        else:
            if self.next_t == TS_NEVER or t >= self.next_t:
                index = self.schedule_index(t)
                if index < 0:
                    return TS_INVALID
                dtnext = self.schedule_dtnext(index) * 60
                value = self.schedule_value(index)
                if self.value != value:
                    self.since = t
                if self.since == TS_ZERO:
                    self.since = t
                self.value = value
                self.duration = self.schedule_duration(self, index) / 60.0
                self.next_t = TS_NEVER if dtnext == 0 else t + dtnext - t % 60
        return self.next_t

    def schedule_syncproc(self, data):
        global next_t1_sch, done_count_sch, next_t2_sch
        while data.ok:
            # Lock access to start condition
            start_lock.acquire()

            # Wait for thread start condition
            while data.t0 == next_t1_sch:
                start_cond.wait()

            # Unlock access to start count
            start_lock.release()

            # Process the list for this thread
            t2 = float('inf')
            for sch in data['sch']:
                t = self.schedule_sync(next_t1_sch)
                if t < t2:
                    t2 = t

            # Signal completed condition
            data.t0 = next_t1_sch

            # Lock access to done condition
            done_lock.acquire()

            # Signal thread is done for now
            done_count_sch -= 1
            if t2 < next_t2_sch:
                next_t2_sch = t2

            # Signal change in done condition
            done_cond.notify_all()

            # Unlock access to done count
            done_lock.release()

    def schedule_syncall(self, t1):
        global next_t2_sch, done_count_sch, interpolated_schedules
        t2 = TS_NEVER
        ts = time.process_time()
        n_threads_sch = 0
        if self.n_schedules == 0:
            return TS_NEVER

        if n_threads_sch == 0:
            schn = 0
            n_threads_sch = global_threadcount

            if n_threads_sch > 1:
                if self.n_schedules < n_threads_sch * 4:
                    n_threads_sch = self.n_schedules // 4

                if n_threads_sch == 0:
                    n_threads_sch = 1

                n_items = self.n_schedules // n_threads_sch
                n_threads_sch = self.n_schedules // n_items
                if n_threads_sch * n_items < self.n_schedules:
                    n_threads_sch += 1

                thread_sch = []
                schn = 0

                for sch in self.schedule_list:
                    if schn >= n_items:
                        schn += 1
                    if thread_sch[schn].nsch == 0:
                        thread_sch[schn].sch.append(sch)
                    thread_sch[schn].nsch += 1

                for n in range(n_threads_sch):
                    thread_sch[n].ok = True
                    t = threading.Thread(target=self.schedule_syncproc, args=(thread_sch[n],))
                    t.start()

        if next_t2_sch == TS_NEVER:
            return TS_NEVER

        if next_t2_sch > t1 and not interpolated_schedules:
            return next_t2_sch

        if n_threads_sch < 2:
            for sch in self.schedule_list:
                t3 = self.schedule_sync(t1)
                if t3 < t2:
                    t2 = t3
            next_t2_sch = t2
        else:
            done_lock.acquire()
            done_count_sch = n_threads_sch
            start_lock.acquire()
            next_t1_sch = t1
            next_t2_sch = TS_NEVER
            start_cond.notify_all()
            start_lock.release()

            while done_count_sch > 0:
                done_cond.wait()
            output_debug("passed donecount==0 condition")
            done_lock.release()

            if next_t2_sch < t2:
                t2 = next_t2_sch

        self.schedule_synctime += time.process_time() - ts
        return t2

    # Add more data dictionaries and threads if needed


    def schedule_test(self):
        failed = 0
        ok = 0
        errorcount = 0
        ts = ""
        tests = [
            ScheduleTest("empty", "", "2000/01/01 00:00:00", "NEVER", 0, 0.0),
            ScheduleTest("halfday-binary", "* 12-23 * * *", "2001/02/03 01:30:00", "2001/02/03 12:00:00", 0, 0.0),
            ScheduleTest("halfday-binary", None, "2002/03/05 13:45:00", "2002/03/06 00:00:00", 0, 1.0),
            ScheduleTest("halfday-bimodal", "* 0-11 * * * 0.25; * 12-23 * * * 0.75;", "2003/04/07 01:15:00",
                         "2003/04/07 12:00:00", 0, 0.25),
            ScheduleTest("halfday-bimodal", "* 0-11 * * * 0.25; * 12-23 * * * 0.75;", "2004/05/09 00:00:00",
                         "2004/05/09 12:00:00", 0, 0.25),
            ScheduleTest("halfday-bimodal", None, "2005/06/11 13:20:00", "2005/06/12 00:00:00", 0, 0.75),
            ScheduleTest("halfday-bimodal", None, "2006/07/13 12:00:00", "2006/07/14 00:00:00", 0, 0.75),
            ScheduleTest("halfday-bimodal", None, "2007/08/15 00:00:00", "2007/08/15 12:00:00", 0, 0.25),
            ScheduleTest("quarterday-normal", "* 0-5 * * *; * 12-17 * * *;", "2008/09/17 00:00:00",
                         "2008/09/17 06:00:00", SN_WEIGHTED, 0.5),
            ScheduleTest("quarterday-normal", None, "2009/10/19 06:00:00", "2009/10/19 12:00:00", SN_WEIGHTED, 0.0),
            ScheduleTest("quarterday-normal", None, "2010/11/21 12:00:00", "2010/11/21 18:00:00", SN_WEIGHTED, 0.5),
            ScheduleTest("quarterday-normal", None, "2011/12/23 18:00:00", "2011/12/24 00:00:00", SN_WEIGHTED, 0.0)
        ]

        output_test("\nBEGIN: schedule tests")

        for test in tests:
            t1 = convert_to_timestamp(test.t1)
            errors = 0
            s = self.schedule_create(test.name, test.definition)
            output_test(
                f"Schedule {test.name} {{ {test.definition} }} sync to {convert_from_timestamp(t1, ts, len(ts)) if t1 != -1 else '???'}...")

            if s is None:
                output_test(f" ! schedule {test.name} {{ {test.definition} }} create failed")
                errors += 1
            else:
                t2 = TS_NEVER
                if test.normalize:
                    s.schedule_normalize(test.normalize)
                t2 = s.schedule_sync(t1)
                if s.value != test.value:
                    output_test(f" ! expected value {test.value} but found {s.value}")
                    errors += 1
                if t2 != convert_to_timestamp(test.t2):
                    output_test(
                        f" ! expected next time {test.t2} but found {convert_from_timestamp(t2, ts, len(ts)) if t2 != -1 else '???'}")
                    errors += 1

            if errors == 0:
                output_test("   test passed")
                ok += 1
            else:
                failed += 1

            errorcount += errors

        if failed:
            output_error(f"scheduletest: {failed} schedule tests failed--see test.txt for more information")
            output_test(f"!!! {failed} schedule tests failed, {errorcount} errors found")
        else:
            output_verbose(f"{ok} schedule tests completed with no errors--see test.txt for details")
            output_test(f"scheduletest: {ok} schedule tests completed, {errorcount} errors found")

        output_test("END: schedule tests")
        return failed

    def schedule_dumpall(self, file):
        with open(file, "w") as fp:
            for sch in self.schedule_list:
                mode = "w" if sch == self.schedule_list else "a"
                self.schedule_dump(file, mode)

    def schedule_dump(self, file, mode):
        with open(file, mode) as fp:
            calendar_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

            fp.write(f"schedule {self.name} {{ {self.definition} }}\n")
            fp.write(f"sizeof(SCHEDULE) = {Schedule.__basicsize__ / 1024 / 1024:.3f} MB\n")

            for calendar in range(MAXCALENDARS):
                days_in_month = [31, 29 if (calendar & 1) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

                year = 0

                fp.write("\nYears:")
                for y in range(1970, 2039):
                    dt = DATETIME(y, 0, 1, 0, 0, 0)
                    ts = mkdatetime(dt)
                    ndx = self.schedule_index(ts)

                    if GET_CALENDAR(ndx) == calendar:
                        fp.write(f" {y}")
                        if year == 0:
                            year = y

                fp.write(f" (calendar {calendar})\n")

                for month in range(12):
                    fp.write(f"     {calendar_names[month]}  ")
                    for hour in range(24):
                        fp.write(f" {hour:02}:00")
                    fp.write("\n")

                    for day in range(days_in_month[month]):
                        fp.write(f"      {day + 1:02} ")
                        for hour in range(24):
                            minute = 0
                            dt = DATETIME(year, month + 1, day + 1, hour, 0, 0)
                            ts = mkdatetime(dt)
                            local_datetime(ts, dt)
                            fp.write(f"{calendar_names[dt.weekday]} {day + 1:02}")

                            for _ in range(24):
                                dt = DATETIME(year, month + 1, day + 1, hour, minute, 0)
                                ts = mkdatetime(dt)
                                ndx = self.schedule_index(ts)
                                dtn = self.schedule_dtnext(ndx)
                                value = self.schedule_value(ndx)

                                if dtn < 60:
                                    ndx2 = self.schedule_index(ts + dtn)
                                    value2 = self.schedule_value(ndx2)
                                    fp.write(f" {value:.5g}{'~' if value != value2 else ' '}")
                                else:
                                    fp.write(f" {value:.5g}")

                                minute += 1

                            fp.write("\n")

    def schedule_saveall(self, fp):
        count = 0
        count += fp.write("SCHEDULE *sch;\n")
        sch = self.schedule_list
        while sch is not None:
            count += fp.write("schedule %s {\n%s\n}\n" % (sch.name, sch.definition))
            sch = sch.next
        return count

if __name__ == "__main__":
    thread1 = threading.Thread(target=Schedule.schedule_syncproc, args=(data1,))
    thread1.start()
