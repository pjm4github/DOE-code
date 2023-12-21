import re
import time
import urllib

from numpy.core.defchararray import encode

from gov_pnnl_goss.gridlab.climate.Weather import Weather
from gov_pnnl_goss.gridlab.climate.WeatherReader import WeatherReader
from gov_pnnl_goss.gridlab.gldcore.Globals import PA_REFERENCE
from gov_pnnl_goss.gridlab.gldcore.GridLabD import gl_debug, gl_localtime, gl_error, TS_INVALID, TS_NEVER, gl_warning, \
    gl_register_class, gl_publish_variable
from gov_pnnl_goss.gridlab.gldcore.Property import PROPERTYTYPE

from datetime import datetime
from enum import Enum

class CSVSTATUS(Enum):
    CR_INIT = 1
    CR_OPEN = 2
    CR_ERROR = 3

TIMESTAMP = 0


def gl_create_object(oclass):
    pass


def create_csv_reader(obj, parent):
    my = 0
    obj[0] = gl_create_object(CsvReader.oclass)
    if obj[0] != None:
        return 1
    # print("create_csv_reader")
    return 0  # don't want it to get called, but better to have it not be fatal


def init_csv_reader(obj, parent):
    my = obj.data
    return 1  # let the climate object cause the file to open


# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
def sync_csv_reader(obj, t0):
    return None  # really doesn't do anything


def gl_mktime(then):
    pass



def gl_find_property(oclass, name):
    pass

def ISLEAPYEAR(year):
    pass



class CsvReader(WeatherReader):
    oclass = 0

    def __init__(self, module):
        super().__init__()
        self.city_name = ""
        self.column_ct = 0
        self.columns = []
        self.columns_str = ""
        self.elevation = 0
        self.filename = ""
        self.high_temp = 0.0
        self.index = 0
        self.last_ts = None
        self.lat_deg = 0.0
        self.lat_min = 0.0
        self.long_deg = 0.0
        self.long_min = 0.0
        self.low_temp = 0.0
        self.next_ts = None
        self.peak_solar = 0.0
        self.sample_ct = 0
        self.samples = []
        self.state_name = ""
        self.status = ""
        self.status = CSVSTATUS.CR_INIT
        self.timefmt = ""
        self.timezone = ""
        self.timezone_offset = 0.0
        self.tz_numval = 0.0
        self.weather_last = None
        self.weather_root = None

        if not hasattr(self, 'oclass'):
            self.oclass = gl_register_class(module, "csv_reader", CsvReader.__sizeof__(), 0)
            if not gl_publish_variable(self.oclass,
                                       PROPERTYTYPE.PT_int32, "index", PADDR(self.index),
                                       PROPERTYTYPE.PT_ACCESS, PA_REFERENCE,
                                       PROPERTYTYPE.PT_char32, "city_name", PADDR(self.city_name),
                                       PROPERTYTYPE.PT_char32, "state_name", PADDR(self.state_name),
                                       PROPERTYTYPE.PT_double, "lat_deg", PADDR(self.lat_deg),
                                       PROPERTYTYPE.PT_double, "lat_min", PADDR(self.lat_min),
                                       PROPERTYTYPE.PT_double, "long_deg", PADDR(self.long_deg),
                                       PROPERTYTYPE.PT_double, "long_min", PADDR(self.long_min),
                                       PROPERTYTYPE.PT_double, "low_temp", PADDR(self.low_temp),
                                       PROPERTYTYPE.PT_ACCESS, PA_REFERENCE,
                                       PROPERTYTYPE.PT_double, "high_temp", PADDR(self.high_temp),
                                       PROPERTYTYPE.PT_ACCESS, PA_REFERENCE,
                                       PROPERTYTYPE.PT_double, "peak_solar", PADDR(self.peak_solar),
                                       PROPERTYTYPE.PT_ACCESS, PA_REFERENCE,
                                       PROPERTYTYPE.PT_int32, "elevation", PADDR(self.elevation),
                                       PROPERTYTYPE.PT_enumeration, "status", PADDR(self.status),
                                       PROPERTYTYPE.PT_ACCESS, PA_REFERENCE,
                                       PROPERTYTYPE.PT_KEYWORD, "INIT", CSVSTATUS.CR_INIT,
                                       PROPERTYTYPE.PT_KEYWORD, "OPEN", CSVSTATUS.CR_OPEN,
                                       PROPERTYTYPE.PT_KEYWORD, "ERROR", CSVSTATUS.CR_ERROR,
                                       PROPERTYTYPE.PT_char32, "timefmt", PADDR(self.timefmt),
                                       PROPERTYTYPE.PT_char32, "timezone", PADDR(self.timezone),
                                       PROPERTYTYPE.PT_double, "timezone_offset", PADDR(self.tz_numval),
                                       PROPERTYTYPE.PT_char256, "columns", PADDR(self.columns_str),
                                       PROPERTYTYPE.PT_char256, "filename", PADDR(self.filename),
                                       None) < 1:
                raise Exception(f"unable to publish properties in {__name__}")

    # # Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
    # def initialize_csv_reader(self):
    #     if self.oclass is None:
    #         self.oclass = gl_register_class(module, "csv_reader", sizeof(csv_reader), 0)
    #         if gl_publish_variable(self.oclass,
    #             PROPERTYTYPE.PT_int32, "index", PADDR(index), PROPERTYTYPE.PT_ACCESS, PA_REFERENCE,
    #             PROPERTYTYPE.PT_char32, "city_name", PADDR(city_name),
    #             PROPERTYTYPE.PT_char32, "state_name", PADDR(state_name),
    #             PROPERTYTYPE.PT_double, "lat_deg", PADDR(lat_deg),
    #             PROPERTYTYPE.PT_double, "lat_min", PADDR(lat_min),
    #             PROPERTYTYPE.PT_double, "long_deg", PADDR(long_deg),
    #             PROPERTYTYPE.PT_double, "long_min", PADDR(long_min),
    #             PROPERTYTYPE.PT_double, "low_temp", PADDR(low_temp), PROPERTYTYPE.PT_ACCESS, PA_REFERENCE,
    #             PROPERTYTYPE.PT_double, "high_temp", PADDR(high_temp), PROPERTYTYPE.PT_ACCESS, PA_REFERENCE,
    #             PROPERTYTYPE.PT_double, "peak_solar", PADDR(peak_solar), PROPERTYTYPE.PT_ACCESS, PA_REFERENCE,
    #             PROPERTYTYPE.PT_int32, "elevation", PADDR(elevation),
    #             PROPERTYTYPE.PT_enumeration, "status", PADDR(status), PROPERTYTYPE.PT_ACCESS, PA_REFERENCE,
    #                 PROPERTYTYPE.PT_KEYWORD, "INIT", CR_INIT,
    #                 PROPERTYTYPE.PT_KEYWORD, "OPEN", CR_OPEN,
    #                 PROPERTYTYPE.PT_KEYWORD, "ERROR", CR_ERROR,
    #             PROPERTYTYPE.PT_char32, "timefmt", PADDR(timefmt),
    #             PROPERTYTYPE.PT_char32, "timezone", PADDR(timezone),
    #             PROPERTYTYPE.PT_double, "timezone_offset", PADDR(tz_numval),
    #             PROPERTYTYPE.PT_char256, "columns", PADDR(columns_str),
    #             PROPERTYTYPE.PT_char256, "filename", PADDR(filename),
    #             None) < 1:
    #             GL_THROW("unable to publish properties in %s", __FILE__)
    #         memset(self, 0, sizeof(csv_reader))


    # Converted by an OPENAI API call using model: gpt-3.5-turbo-1106 python
    def open_csv(self, file):
        line = [1024]
        filename = [128]
        has_cols = 0
        linenum = 0
        i = 0
        obj = self.objecthdr
        wtr = None

        if file == 0:
            gl_error("csv_reader has no input file name!")
            return 0

        filename[:127] = file
        self.infile = open(str(filename), "r")
        if self.infile == 0:
            gl_error("csv_reader could not open \'%s\' for input!", file)
            return 0

        if self.columns_str[0] != 0:
            if 0 == self.read_header(self.columns_str):
                gl_error("csv_reader::open ~ column header read failure from explicit headers")
                return 0
            else:
                has_cols = 1

        for line in self.infile.read(1024):
            linenum += 1
            if line[0] == '#':  # comment
                continue
            elif len(line) < 1:
                continue  # blank line
            elif line[0] == '$':  # property
                if 0 == self.read_prop(line[1:]):
                    gl_error(f"csv_reader::open ~ property read failure on line {linenum}")
                    return 0
                else:
                    continue
            elif has_cols == 0:
                if 0 == self.read_header(line):
                    gl_error(f"csv_reader::open ~ column header read failure on line  {linenum}")
                    return 0
                else:
                    has_cols = 1
            else:
                line_rv = self.read_line(line, linenum)
                if 0 == line_rv:
                    gl_error(f"csv_reader::open ~ data line read failure on line {linenum}")
                    return 0
                elif 1 == line_rv:  # good read
                    self.sample_ct += 1
                elif 2 == line_rv:  # read went 'backwards' or was blank, line discarded.
                    pass

        self.samples = [None] * self.sample_ct
        for i, wtr in enumerate(self.weather_root):
            self.samples[i] = wtr

        self.sample_ct = i

        obj.latitude = self.lat_deg + (self.lat_min if self.lat_deg > 0 else -self.lat_min) / 60
        obj.longitude = self.long_deg + (self.long_min if self.long_deg > 0  else -self.long_min) / 60

        return 1

    # Converted by an OPENAI API call using model: gpt-3.5-turbo-1106 python
    def read_prop(self, line):
        my = self.OBJECTHDR()
        split = line.find('=')
        propstr = line.split('=')[0]
        valstr = line.split('=')[1]
        prop = None

        if split == -1:
            gl_error("csv_reader::read_prop ~ missing '=' separator")
            return 0

        if 2 != len(line.split("=")):
            gl_error("csv_reader::read_prop ~ error reading property & value")
            return 0

        prop = self.gl_find_property(self.oclass, propstr)
        if prop == 0:
            gl_error("csv_reader::read_prop ~ unrecognized csv_reader property '%s'" % propstr)
            return 0

        addr = (self + prop.addr)
        if prop.ptype == PROPERTYTYPE.PT_double:
            try:
                setattr(addr, 'double', float(valstr))
            except ValueError:
                gl_error("csv_reader::read_prop ~ unable to set property '%s' to '%s'" % (propstr, valstr))
                return 0
        elif prop.ptype == PROPERTYTYPE.PT_char32:
            addr.char32 = valstr[:32]

        elif prop.ptype == PROPERTYTYPE.PT_int32:
            try:
                setattr(addr, 'int', int(valstr))
            except ValueError:
                gl_error("csv_reader::read_prop ~ unable to set property '%s' to '%s'" % (propstr, valstr))
                return 0
        else:
            gl_error("csv_reader::read_prop ~ unable to convert property '%s' due to type restrictions" % propstr)
            return 0
        return 1

    # Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
    def read_header(self, line):
        class CmnList:
            def __init__(self):
                self.name = ""
                self.column = None
                self.next = None

        buffer = bytearray(1024)
        index = 0
        start_idx = 0
        done = 0
        i = 0
        prop = None
        first = None
        last = None
        temp = None
        column_ct = 0
        columns = []

        # expected format: x,y,z\n
        buffer[:1024] = line.encode()

        # split column header list
        while index < 1024 and not done:
            while buffer[index] != 0 and buffer[index] != ord(',') and buffer[index] != ord('\n') \
                    and buffer[index] != ord('\r') and buffer[index] != ord('#'):
                index += 1
            if buffer[index] == ord(','):
                buffer[index] = 0
                index += 1
            if buffer[index] == ord('\n') or buffer[index] == ord('\r') or buffer[index] == ord('#'):
                buffer[index] = 0
            temp = CmnList()
            temp.name = buffer[start_idx:index].decode()
            temp.column = prop
            temp.next = None
            start_idx = index
            column_ct += 1
            if first is None:
                first = temp
                last = temp
            else:
                last.next = temp
                last = temp
            if buffer[index] == 0 or buffer[index] == ord('\n') or buffer[index] == ord('\r'):
                done = 1
                break

        # find properties for each column header
        temp = first
        columns = [None] * column_ct
        i = 0
        while temp is not None and i < column_ct:
            temp.column = gl_find_property(self.weather.oclass, temp.name)
            if temp.column is None:
                gl_error("csv_reader::read_header ~ unable to find column property '%s'", urllib.parse.quote(temp))
                return 0
            columns[i] = temp.column
            temp = temp.next
            i += 1
        return 1

    def read_line(self, line, linenum):
        done = 0
        col = 0
        buffer = [0] * 2048
        token = 0
        sample = 0
        t1, t2 = 0, 0

        buffer[:1023] = line
        #token = strtok(buffer, " ,\t\n\r")
        tokens = str(buffer).split(" \t\n\r,")

        if len(tokens) == 0:
            return 2  # blank line
        token = tokens.pop(0)
        sample = Weather()

        if self.timefmt[0] == 0:
            ts = self.callback.time.convert_to_timestamp(token)
            dt = datetime.now()
            dt.nanosecond = 0

            if ts != TS_INVALID and ts != TS_NEVER and self.callback.time.local_datetime(ts, dt):
                sample.month = dt.month
                sample.day = dt.day
                sample.hour = dt.hour
                sample.minute = dt.minute
                sample.second = dt.second
                # IMPORTANT NOTE: if DST is not handled properly by sample, don't try to fix
                # the problem here.  The weather class may need to be fixed so it uses UTC internally.
            else:
                pattern = r'(\d+):(\d+):(\d+):(\d+):(\d+)'

                # Match the pattern in the input string
                match = re.match(pattern, token)
                if not match:
                    gl_error("csv_reader::read_line ~ unable to read time string '%s' with default format" % token)
                    sample = None
                    return 0

                sample.month, sample.day, sample.hour, sample.minute, sample.second = map(int, match.groups())

        else:
            match = re.match(self.timefmt.get_"", token)
            if not match:
                gl_error(R"(csv_reader::read_line ~ unable to read time string '%s' with format '%s')" % (
                token, self.timefmt.get_""))
                sample = None
                return 0
            else:
                sample.month, sample.day, sample.hour, sample.minute, sample.second = map(int, match.groups())

        if self.weather_last != 0:
            t1 = self.weather_last.month * 31 * 24 * 60 * 60 + self.weather_last.day * 24 * 60 * 60 + self.weather_last.hour * 60 * 60 + \
                 self.weather_last.minute * 60 + self.weather_last.second
            t2 = sample.month * 31 * 24 * 60 * 60 + sample.day * 24 * 60 * 60 + sample.hour * 60 * 60 + sample.minute * 60 + sample.second
            if t1 >= t2:
                gl_warning(
                    "csv_reader::read_line ~ sample on line %i does not advance in time and has been discarded" % linenum)
                sample = None
                return 2
        token = tokens.pop(0)
        while token:
            if col >= self.column_ct:
                break
            if self.columns[col].ptype == PROPERTYTYPE.PT_double:
                self.dptr = float(self.columns[col].addr + sample)
                try:
                    self.dptr = float(token)
                except ValueError as e:
                    gl_error(f"(csv_reader::read_line ~ unable to set value "
                             f"{token} to double property {self.columns[col].name})")
                    sample = None
                    return 0
            col += 1
            token = tokens.pop(0)

        if self.weather_root == 0:
            self.weather_root = sample
        else:
            self.weather_last.next = sample
        self.weather_last = sample

        return 1

    def get_data(self, t0, temp, humid, direct, diffuse, global_rad, extra_global, wind,
                 winddir_or_rain, opaque_or_snow, total_or_pressure, rain=None, snow=None, pressure=None):

        windir = winddir_or_rain if rain else None
        opaque = opaque_or_snow if snow else None
        total = total_or_pressure if pressure else None
        rain = rain if rain else winddir_or_rain
        snow = snow if snow else opaque_or_snow
        pressure = pressure if pressure else total_or_pressure


        now = datetime.now()
        then = datetime.now()
        next_year = 0
        i = 0
        idx = self.index
        start = self.index
        now.nanosecond = 0
        then.nanosecond = 0

        localres = 0

        if t0 < self.next_ts:
            return -self.next_ts

        localres = gl_localtime(t0, now)  # error check

        gl_debug("csv_reader::get_data start")

        if self.next_ts == 0:
            guess_dt = datetime.now()
            guess_dt.nanosecond = 0
            guess_ts = 0
            i = 0

            for i in range(self.sample_ct):
                guess_dt.year = now.year
                guess_dt.month = self.samples[i].month
                guess_dt.day = self.samples[i].day
                guess_dt.hour = self.samples[i].hour
                guess_dt.minute = self.samples[i].minute
                guess_dt.second = self.samples[i].second
                guess_dt.tz = now.tz

                if guess_dt.month == 2 and guess_dt.day == 29:
                    if not ISLEAPYEAR(now.year):
                        continue  # skip leap days on non-leap years

                guess_ts = TIMESTAMP
                gl_mktime(guess_dt)

                if guess_ts >= t0:
                    i -= 1  # we want the sample *before* this one
                    break

            self.index = i

            if self.index > -1 and self.index < self.sample_ct:
                temp = self.samples[self.index].temperature
                humid = self.samples[self.index].humidity
                direct = self.samples[self.index].solar_dir
                diffuse = self.samples[self.index].solar_diff
                global_rad = self.samples[self.index].solar_global
                extra_global = self.samples[self.index].global_horizontal_extra
                wind = self.samples[self.index].wind_speed
                winddir = self.samples[self.index].wind_dir
                opaque = self.samples[self.index].opq_sky_cov
                total = self.samples[self.index].tot_sky_cov
                rain = self.samples[self.index].rainfall
                snow = self.samples[self.index].snowdepth
                pressure = self.samples[self.index].pressure
            else:  # somewhere between the last and the first element
                temp = self.samples[self.sample_ct - 1].temperature
                humid = self.samples[self.sample_ct - 1].humidity
                direct = self.samples[self.sample_ct - 1].solar_dir
                diffuse = self.samples[self.sample_ct - 1].solar_diff
                global_rad = self.samples[self.sample_ct - 1].solar_global
                extra_global = self.samples[self.sample_ct - 1].global_horizontal_extra
                wind = self.samples[self.sample_ct - 1].wind_speed
                winddir = self.samples[self.sample_ct - 1].wind_dir
                opaque = self.samples[self.sample_ct - 1].opq_sky_cov
                total = self.samples[self.sample_ct - 1].tot_sky_cov
                rain = self.samples[self.sample_ct - 1].rainfall
                snow = self.samples[self.sample_ct - 1].snowdepth
                pressure = self.samples[self.sample_ct - 1].pressure

            then.year = now.year + (1 if self.index + 1 == self.sample_ct else 0)
            then.month = self.samples[(self.index + 1) % self.sample_ct].month
            then.day = self.samples[(self.index + 1) % self.sample_ct].day
            then.hour = self.samples[(self.index + 1) % self.sample_ct].hour
            then.minute = self.samples[(self.index + 1) % self.sample_ct].minute
            then.second = self.samples[(self.index + 1) % self.sample_ct].second
            then.nanosecond = 0
            then.tz = now.tz

            self.next_ts = (TIMESTAMP)
            gl_mktime(then)

            return -self.next_ts

        if self.sample_ct == 1:  # only one sample ~ ignore it and keep feeding the same data back, but in a year
            self.next_ts += 365 * 24 * 3600
            return -self.next_ts

        while True:
            # should we roll the year over?
            if self.index + 1 >= self.sample_ct:
                self.index = 0
            else:
                self.index += 1

            if self.index + 1 == self.sample_ct:
                next_year = 1
            else:
                next_year = 0

            then.year = now.year + next_year
            then.month = self.samples[(self.index + 1) % self.sample_ct].month
            then.day = self.samples[(self.index + 1) % self.sample_ct].day
            then.hour = self.samples[(self.index + 1) % self.sample_ct].hour
            then.minute = self.samples[(self.index + 1) % self.sample_ct].minute
            then.second = self.samples[(self.index + 1) % self.sample_ct].second
            if then.month == 2 and then.day == 29:
                if not ISLEAPYEAR(then.year):
                    continue  # skip leap days on non-leap years
            then.tz = now.tz

            self.next_ts = (TIMESTAMP)
            gl_mktime(then)

            if self.next_ts >= t0 or self.index == start:
                break

        temp = self.samples[self.index].temperature
        humid = self.samples[self.index].humidity
        direct = self.samples[self.index].solar_dir
        diffuse = self.samples[self.index].solar_diff
        global_rad = self.samples[self.index].solar_global
        extra_global = self.samples[self.index].global_horizontal_extra
        wind = self.samples[self.index].wind_speed
        winddir = self.samples[self.index].wind_dir
        opaque = self.samples[self.index].opq_sky_cov
        total = self.samples[self.index].tot_sky_cov
        rain = self.samples[self.index].rainfall
        snow = self.samples[self.index].snowdepth
        pressure = self.samples[self.index].pressure

        if self.index == start:
            gl_error("something strange happened with the schedule in csv_reader")
        # TROUBLESHOOT
        # An unidentified error occured while reading data and constructing the weather
        # data schedule.  Please post a ticket detailing this event on the GridLAB-D
        # SourceForge page.

        gl_debug("csv_reader::get_data end")

        return -self.next_ts


