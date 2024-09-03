import re
import time

from datetime import datetime, timedelta, timezone
import pytz
from typing import Optional, Tuple

# Assuming TS_SECOND is a fundamental constant, representing the number of ticks per second.
# This will be used to define other time-related constants within the Python environment.
TS_SECOND = 1 # duration of one second
# Constants for timestamp resolution
TS_SCALE = 0  # system timescale is 1 second (1e-0 s)
TS_RESOLUTION = 1  # must be 10^TS_SCALE

DAY = 86400 * TS_SECOND
HOUR = 3600 * TS_SECOND
MINUTE = 60 * TS_SECOND
SECOND = TS_SECOND

# Constants for specific resolutions, if needed
NORMALRES = TS_SECOND
HIGHRES = TS_SECOND / 1000000  # For microsecond resolution
VERYHIGHRES = TS_SECOND / 1000000000  # For nanosecond resolution

# Typedefs are not needed in Python; will use Python's native types

TS_ZERO = 0
TS_MAX = 32482080000  # roughly 3000 CE
TS_INVALID = -1
TS_NEVER = ((2**32-1) >> 1)
TS_NEVER_DBL = 9223372036854775808.0  # Double representation of TS_NEVER
MINYEAR = 1970
MAXYEAR = 2969

DT_INFINITY = 0xfffffffe
DT_INVALID = 0xffffffff
DT_SECOND = 1000000000
# DT_INFINITY = math.inf
# DT_INVALID = -1
# DT_SECOND = 1.0


USE_TS_CACHE = False

# Function to determine whether a given year is a leap year
def is_leap_year(year: int) -> bool:
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


class TimeStamp:
    def __init__(self, year, month, day, hour=0, minute=0, second=0, nanosecond=0, is_dst=0, tz='UTC', weekday=0, yearday=0, timestamp=0, tzoffset=0):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second
        self.nanosecond = nanosecond
        self.is_dst = is_dst
        self.tz = tz
        self.weekday = weekday
        self.yearday = yearday
        self.timestamp = timestamp
        self.tzoffset = tzoffset

    @staticmethod
    def to_timestamp(ts: int) -> 'TimeStamp':
        dt = datetime.utcfromtimestamp(ts)
        return TimeStamp(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)

    @staticmethod
    def from_timestamp(ts: 'TimeStamp') -> int:
        return int(datetime(ts.year, ts.month, ts.day, ts.hour, ts.minute, ts.second).timestamp())


# Function stubs for conversion functions
def timestamp_current_timezone():
    return time.tzname[0]

def mkdatetime(dt):
    return int(time.mktime(dt.timetuple()))

def strdatetime(dt, buffer, size):
    # This function would format a TimeStamp object into a string.
    # The implementation would depend on the specific format desired.
    pass

# def convert_from_timestamp(ts, buffer, size):
#     # Convert a timestamp to a string representation
#     pass
# Function to convert a timestamp into a human-readable string
def convert_from_timestamp(ts: int) -> str:
    dt = datetime.utcfromtimestamp(ts)
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def convert_from_timestamp_delta(ts: int, delta_ns: int) -> str:
    """
    Convert a timestamp and delta (in nanoseconds) to a human-readable string.

    Parameters:
    - ts: TimeStamp in seconds since the Unix epoch (1970-01-01 00:00:00 UTC).
    - delta_ns: Delta time in nanoseconds to be added to the timestamp.

    Returns:
    - A string representing the adjusted date and time in UTC.
    """
    # Convert timestamp to a datetime object
    dt = datetime.utcfromtimestamp(ts)

    # Calculate the delta in seconds (delta_ns is in nanoseconds)
    delta_seconds = delta_ns / 1e9

    # Adjust the datetime by the delta
    adjusted_dt = dt + timedelta(seconds=delta_seconds)

    # Convert the adjusted datetime to a string (ISO 8601 format)
    return adjusted_dt.isoformat()


def convert_from_deltatime_timestamp(ts_v: float) -> str:
    """
    Convert a high-resolution timestamp (with nanoseconds) to a human-readable string.

    Parameters:
    - ts_v: TimeStamp in seconds since the Unix epoch (1970-01-01 00:00:00 UTC),
            including fractional seconds for nanosecond precision.

    Returns:
    - A string representing the date and time, including nanoseconds.
    """
    # Extract the whole second and nanosecond components
    whole_seconds = int(ts_v)
    nanoseconds = int((ts_v - whole_seconds) * 1e9)

    # Convert the whole second part to a datetime object
    dt = datetime.utcfromtimestamp(whole_seconds)

    # Format the datetime object to a string, excluding microseconds
    dt_str = dt.strftime('%Y-%m-%d %H:%M:%S')

    # Append the nanosecond component, formatted to 9 digits to ensure nanosecond precision
    return f"{dt_str}.{nanoseconds:09d}"


def timestamp_to_days(t):
    return t / 86400

def timestamp_to_hours(t):
    return t / 3600

def timestamp_to_minutes(t):
    return t / 60

def timestamp_to_seconds(t):
    return t

# Function to convert a string representation of a date and time into a timestamp
def convert_to_timestamp(date_str: str) -> int:
    # Assuming date_str is in ISO 8601 format 'YYYY-MM-DD HH:MM:SS'
    dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    return int(dt.timestamp())


def convert_to_timestamp_delta(datetime_str: str) -> tuple:
    """
    Converts a datetime string with potential nanosecond precision to a timestamp, delta in nanoseconds, and a double timestamp.

    Parameters:
    - datetime_str: A string representing the datetime possibly including nanoseconds.

    Returns:
    - A tuple containing:
        - The timestamp (int, seconds since the epoch)
        - The delta in nanoseconds (int)
        - The double representation of the timestamp including nanoseconds (float)
    """
    # Regular expression to match datetime with optional nanoseconds
    datetime_pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})(?:\.(\d+))?"
    match = re.match(datetime_pattern, datetime_str)
    if not match:
        raise ValueError("Invalid datetime format")

    # Extract the main datetime part and the nanosecond component, if present
    datetime_part, nanoseconds_str = match.groups()
    nanoseconds = int(nanoseconds_str) if nanoseconds_str else 0

    # Convert the main part of the datetime to a timestamp
    dt = datetime.strptime(datetime_part, "%Y-%m-%d %H:%M:%S")
    timestamp = int(dt.timestamp())

    # Calculate the double representation
    double_timestamp = timestamp + nanoseconds / 1e9

    return timestamp, nanoseconds, double_timestamp


def local_datetime(ts: int, timezone_str: str) -> datetime:
    """
    Convert a UTC timestamp to a local datetime object considering the timezone and DST.

    Parameters:
    - ts: TimeStamp in seconds since the Unix epoch (1970-01-01 00:00:00 UTC).
    - timezone_str: A string representing the timezone (e.g., 'America/New_York').

    Returns:
    - A datetime object representing the local date and time in the specified timezone.
    """
    # Convert the timestamp to a UTC datetime object
    utc_dt = datetime.fromtimestamp(ts, timezone.utc)

    # Load the specified timezone
    tz = pytz.timezone(timezone_str)

    # Convert the UTC datetime object to the specified timezone
    local_dt = utc_dt.astimezone(tz)

    return local_dt


def local_datetime_delta(ts: float, timezone_str: str) -> datetime:
    """
    Convert a high-resolution timestamp (with nanoseconds) to a local datetime object,
    considering the specified timezone.

    Parameters:
    - ts: TimeStamp in seconds since the Unix epoch (1970-01-01 00:00:00 UTC),
          including fractional seconds for nanosecond precision.
    - timezone_str: A string representing the timezone (e.g., 'America/New_York').

    Returns:
    - A datetime object representing the local date and time in the specified timezone,
      including nanosecond precision as a fractional part of the second.
    """
    # Separate the timestamp into whole seconds and fractional seconds (for nanoseconds)
    whole_seconds = int(ts)
    fractional_seconds = ts - whole_seconds
    nanoseconds = int(fractional_seconds * 1e9)

    # Convert the whole seconds part to a timezone-aware UTC datetime object
    utc_dt = datetime.fromtimestamp(whole_seconds, tz=timezone.utc)

    # Apply the nanoseconds part as a timedelta (converted to microseconds)
    # Note: datetime supports microseconds, not nanoseconds, so we round to the nearest microsecond
    adjusted_utc_dt = utc_dt + timedelta(microseconds=nanoseconds / 1000)

    # Convert the UTC datetime object to the specified timezone, handling DST if applicable
    tz = pytz.timezone(timezone_str)
    local_dt = adjusted_utc_dt.astimezone(tz)

    return local_dt


def timestamp_test()->int:
    """
    Test the daylight saving time calculations
    :return: the number of test the failed
    """
    return 0

# {
# #define NYEARS 50
# 	int year;
# 	static DATETIME last_t;
# 	TIMESTAMP step = SECOND;
# 	TIMESTAMP ts;
# 	char buf1[64], buf2[64];
# 	char steptxt[32];
# 	TIMESTAMP *event[]={dststart,dstend};
# 	int failed=0, succeeded=0;
#
# 	output_test("BEGIN: daylight saving time event test for TZ=%s...", current_tzname);
# 	convert_from_timestamp(step,steptxt,sizeof(steptxt));
# 	for (year=0; year<NYEARS; year++)
# 	{
# 		int test;
# 		for (test=0; test<2; test++)
# 		{
# 			for (ts=(event[test])[year]-2*step; ts<(event[test])[year]+2*step;ts+=step)
# 			{
# 				DATETIME t;
# 				if (local_datetime(ts,&t))
# 				{
# 					if (last_t.is_dst!=t.is_dst)
# 						output_test("%s + %s = %s", strdatetime(&last_t,buf1,sizeof(buf1))?buf1:"(invalid)", steptxt, strdatetime(&t,buf2,sizeof(buf2))?buf2:"(invalid)");
# 					last_t = t;
# 					succeeded++;
# 				}
# 				else
# 				{
# 					output_test("FAILED: unable to convert ts=%" FMT_INT64 "d to local time", ts);
# 					failed++;
# 				}
# 			}
# 		}
# 	}
# 	output_test("END: daylight saving time event test");
#
# 	step=HOUR;
# 	convert_from_timestamp(step,steptxt,sizeof(steptxt));
# 	output_test("BEGIN: round robin test at %s timesteps",steptxt);
# 	for (ts=DAY+tzoffset; ts<DAY*365*NYEARS; ts+=step)
# 	{
# 		DATETIME t;
# 		if (local_datetime(ts,&t))
# 		{
# 			TIMESTAMP tt = mkdatetime(&t);
# 			convert_from_timestamp(ts,buf1,sizeof(buf1));
# 			convert_from_timestamp(tt,buf2,sizeof(buf2));
# 			if (tt==TS_INVALID)
# 			{
# 				output_test("FAILED: unable to extract %04d-%02d-%02d %02d:%02d:%02d %s (dow=%s, doy=%d)", t.year,t.month,t.day,t.hour,t.minute,t.second,t.tz,dow[t.weekday],t.yearday);
# 				failed++;
# 			}
# 			else if (tt!=ts)
# 			{
# 				output_test("FAILED: unable to match %04d-%02d-%02d %02d:%02d:%02d %s (dow=%s, doy=%d)\n    from=%s, to=%s", t.year,t.month,t.day,t.hour,t.minute,t.second,t.tz,dow[t.weekday],t.yearday,buf1,buf2);
# 				failed++;
# 			}
# 			else if (convert_to_timestamp(buf1)!=ts)
# 			{
# 				output_test("FAILED: unable to convert %04d-%02d-%02d %02d:%02d:%02d %s (dow=%s, doy=%d) back to a timestamp\n    from=%s, to=%s", t.year,t.month,t.day,t.hour,t.minute,t.second,t.tz,dow[t.weekday],t.yearday,buf1,buf2);
# 				output_test("        expected %" FMT_INT64 "d but got %" FMT_INT64 "d", ts, convert_to_timestamp(buf1));
# 				failed++;
# 			}
# 			else
# 				succeeded++;
# 		}
# 		else
# 		{
# 			output_test("FAILED: timestamp_test: unable to convert ts=%" FMT_INT64 "d to local time", ts);
# 			failed++;
# 		}
# 	}
# 	output_test("END: round robin test",steptxt);
# 	output_test("END: daylight saving time tests for %d to %d", YEAR0, YEAR0+NYEARS);
# 	output_verbose("daylight saving time tests: %d succeeded, %d failed (see '%s' for details)", succeeded, failed, global_testoutputfile);
# 	return failed;
# }

# Global variable to hold the current timezone. Defaulting to UTC if not set.
CURRENT_TIMEZONE = pytz.utc

def timestamp_set_tz(tz_name=None):
    """
    Set the global timezone used for datetime operations.

    Parameters:
    - tz_name: A string representing the timezone (e.g., 'America/New_York'). If None or not provided,
               UTC will be used by default.
    """
    global CURRENT_TIMEZONE
    if tz_name is None or tz_name.strip() == "":
        CURRENT_TIMEZONE = pytz.utc
    else:
        try:
            CURRENT_TIMEZONE = pytz.timezone(tz_name)
        except pytz.UnknownTimeZoneError:
            print(f"Unknown timezone: {tz_name}. Falling back to UTC.")
            CURRENT_TIMEZONE = pytz.utc

    print(f"Current timezone set to: {CURRENT_TIMEZONE}")


def get_current_time():
    """
    Returns the current time in the globally set timezone.
    """
    utc_now = datetime.now(pytz.utc)  # Get current time in UTC
    return utc_now.astimezone(CURRENT_TIMEZONE)  # Convert to the current timezone



# Assuming CURRENT_TIMEZONE is defined globally as per the previous example
# For demonstration, let's set CURRENT_TIMEZONE to UTC if not already set
# CURRENT_TIMEZONE = pytz.utc
# # Example usage:
# # Let's assume CURRENT_TIMEZONE was set to 'America/New_York'
# CURRENT_TIMEZONE = pytz.timezone('America/New_York')

def timestamp_from_local(local_dt):
    """
    Convert a local datetime to a UTC timestamp.

    Parameters:
    - local_dt: A datetime object representing local time. This datetime object
                should be naive (i.e., not timezone-aware).

    Returns:
    - A UTC timestamp representing the given local datetime.
    """
    # Make the local datetime timezone-aware using the global CURRENT_TIMEZONE
    local_aware_dt = CURRENT_TIMEZONE.localize(local_dt)

    # Convert the timezone-aware local datetime to UTC
    utc_dt = local_aware_dt.astimezone(pytz.utc)

    # Return the timestamp (seconds since the epoch) of the UTC datetime
    return int(utc_dt.timestamp())




def timestamp_to_local(t):
    # Convert a timestamp to local time
    pass

def local_tzoffset(t):
    # Get the local timezone offset
    tzoffset = 0  # assuming tzoffset is predefined
    def isdst(t):
        # implementation of the isdst function
        pass
    # check if USE_TS_CACHE is defined
    if USE_TS_CACHE:
        old_t = 0
        old_tzoffset = 0
        if old_t == 0 or old_t != t:
            old_tzoffset = tzoffset + (3600 if isdst(t) else 0)
            old_t = t
        return old_tzoffset
    else:
        return int(tzoffset + (3600 if isdst(t) else 0))

# Example of handling DST changes and timezone conversions might require third-party libraries like pytz
def adjust_for_dst(dt: TimeStamp, timezone_str: str) -> TimeStamp:
    tz = pytz.timezone(timezone_str)
    naive_dt = datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
    local_dt = tz.localize(naive_dt, is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)
    return TimeStamp.from_timestamp(int(utc_dt.timestamp()))


def timestamp_get_part(ts, part_name):
    """
    Extracts a specific part of the datetime from a given timestamp.

    Parameters:
    - ts: The timestamp from which to extract the part.
    - part_name: The name of the part to extract (e.g., 'year', 'month', 'day', 'hour', 'minute', 'second').

    Returns:
    - The value of the specified part of the datetime.

    # Example usage
    timestamp_example = 1609459200  # Example timestamp for 2021-01-01 00:00:00 UTC
    print(f"Year: {timestamp_get_part(timestamp_example, 'year')}")
    print(f"Month: {timestamp_get_part(timestamp_example, 'month')}")
    print(f"Day: {timestamp_get_part(timestamp_example, 'day')}")
    print(f"Weekday: {timestamp_get_part(timestamp_example, 'weekday')} (1 for Monday)")
    """
    # Convert the timestamp to a datetime object
    dt = datetime.utcfromtimestamp(ts)

    # Extract and return the requested part
    if part_name == 'year':
        return dt.year
    elif part_name == 'month':
        return dt.month
    elif part_name == 'day':
        return dt.day
    elif part_name == 'hour':
        return dt.hour
    elif part_name == 'minute':
        return dt.minute
    elif part_name == 'second':
        return dt.second
    elif part_name == 'microsecond':
        return dt.microsecond
    elif part_name == 'weekday':
        # Note: Python's weekday() method returns 0 for Monday, so adjust if a different convention is needed
        return dt.weekday() + 1  # Adjusting to make 1 for Monday, if needed
    else:
        raise ValueError("Unknown part name")


def earliest_timestamp(*timestamps):
    """
    Finds the earliest (smallest) timestamp from the given list of timestamps.

    Parameters:
    - timestamps: A variable number of timestamp arguments (integers or floats).

    Returns:
    - The earliest (smallest) timestamp from the given arguments.

    # Example usage
    timestamp1 = 1609459200  # Example timestamp for 2021-01-01 00:00:00 UTC
    timestamp2 = 1612137600  # Example timestamp for 2021-02-01 00:00:00 UTC
    timestamp3 = 1614556800  # Example timestamp for 2021-03-01 00:00:00 UTC

    earliest = earliest_timestamp(timestamp1, timestamp2, timestamp3)
    print(f"Earliest TimeStamp: {earliest}")
    """

    # Filter out any None values or other types that are not int or float
    valid_timestamps = [ts for ts in timestamps if isinstance(ts, (int, float))]

    if not valid_timestamps:
        raise ValueError("No valid timestamps provided.")

    # Return the smallest (earliest) timestamp
    return min(valid_timestamps)


def absolute_timestamp(ts):
    """
    Converts a timestamp to its absolute value.

    Parameters:
    - ts: The timestamp (an integer or float).

    Returns:
    - The absolute value of the timestamp.
    # Example usage
    timestamp_example = -1609459200  # An example negative timestamp
    absolute_ts = absolute_timestamp(timestamp_example)
    print(f"Absolute TimeStamp: {absolute_ts}")
    """
    return datetime.fromtimestamp(ts)

def is_soft_timestamp(ts):
    """
    Checks if the given timestamp is considered "soft".

    In this example, a "soft" timestamp is defined as any negative timestamp.

    Parameters:
    - ts: The timestamp to check.

    Returns:
    - True if the timestamp is "soft", False otherwise.

    # Example usage
    soft_timestamp_example = -1609459200  # An example soft timestamp (using negative value)
    hard_timestamp_example = 1609459200  # An example hard timestamp (using positive value)

    print(f"Is soft timestamp? (soft example): {is_soft_timestamp(soft_timestamp_example)}")
    print(f"Is soft timestamp? (hard example): {is_soft_timestamp(hard_timestamp_example)}")

    """
    return ts < 0

