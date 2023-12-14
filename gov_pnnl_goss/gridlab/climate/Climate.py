import csv
from datetime import datetime
from datetime import timedelta as dt
import math
from math import modf
import random
import re
from enum import Enum
import numpy as np

from gov_pnnl_goss.gridlab.climate.SolarAngles import SolarAngles
from gov_pnnl_goss.gridlab.gldcore.Find import FindType
from gov_pnnl_goss.gridlab.gldcore.GridLabD import gl_warning, gl_error, gl_name, gl_lerp, gl_globalclock

_CLIMATE_H = True

# Constants
PI = math.pi

surface_angles = [
    360,    # H
    180,    # N
    135,    # NE
    90,     # E
    45,     # SE
    0,      # S
    -45,    # SW
    -90,    # W
    -135,   # NW
]
is_TMY2 = False

# Cloud pattern constants
CLOUD_TILE_SIZE = 512
PIXEL_EDGE_SIZE = 20
KM_PER_DEG = 111.32
EMPTY_VALUE = -999

cloud_pattern = []
normalized_cloud_pattern = []
binary_cloud_pattern = []
fuzzy_cloud_pattern = []
on_screen_size = 0
cloud_pattern_size = 0
last_binary_conversion_time = 0


# object flags
OF_NONE		= 0x0000    #  Object flag; none set
OF_HASPLC   = 0x0001    #  Object flag; external PLC is attached, disables local PLC
OF_LOCKED   = 0x0002    #  Object flag; data write pending, reread recommended after lock clears
OF_RECALC   = 0x0008    #  Object flag; recalculation of derived values is needed
OF_FOREIGN	= 0x0010    #  Object flag; indicates that object was created in a DLL and memory cannot be freed by core
OF_SKIPSAFE	= 0x0020    #  Object flag; indicates that skipping updates is safe
OF_FORECAST = 0x0040    #  Object flag; inidcates that the object has a valid forecast available
OF_DEFERRED	= 0x0080    #  Object flag; indicates that the object started to be initialized, but requested deferral
OF_INIT		= 0x0100	#  Object flag; indicates that the object has been successfully initialized
OF_RERANK   = 0x4000    #  Internal use only



def OBJECTDATA(X, T):
    return (X)+1 if X else None  # /**< get the object data structure */


class COMPASS_PTS(Enum):
    CP_H = 0
    CP_N = 1
    CP_NE = 2
    CP_E = 3
    CP_SE = 4
    CP_S = 5
    CP_SW = 6
    CP_W = 7
    CP_NW = 8
    CP_LAST = 9


class CI(Enum):
    CI_NONE = 0
    CI_LINEAR = 1
    CI_QUADRATIC = 2


class CLOUDMODEL(Enum):
    CM_NONE = 0
    CM_CUMULUS = 1


class TMYDATA:
    def __init__(self):
        self.temp = 0.0  # F
        self.temp_raw = 0.0  # C
        self.rh = 0.0  # %rh
        self.dnr = 0.0
        self.dhr = 0.0
        self.ghr = 0.0
        self.solar = [0.0] * len(COMPASS_PTS)
        self.solar_raw = 0.0
        self.direct_normal_extra = 0.0
        self.pressure = 0.0
        self.windspeed = 0.0
        self.rainfall = 0.0  # in/h
        self.snowdepth = 0.0  # in
        self.solar_azimuth = 0.0
        self.solar_elevation = 0.0
        self.solar_zenith = 0.0
        self.global_horizontal_extra = 0.0
        self.wind_dir = 0.0
        self.tot_sky_cov = 0.0
        self.opq_sky_cov = 0.0


class RT(Enum):
    RT_NONE = 0
    RT_TMY2 = 1
    RT_CSV = 2


# Define functions
def RAD(x):
    return (x * PI) / 180


def calculate_solar_radiation_degrees(obj, tilt, orientation, value):
    return calculate_solar_radiation_shading_radians(obj, RAD(tilt), RAD(orientation), 1.0, value)


def calculate_solar_radiation_radians(obj, tilt, orientation, value):
    return calculate_solar_radiation_shading_radians(obj, tilt, orientation, 1.0, value)


def calculate_solar_radiation_shading_degrees(obj, tilt, orientation, shading_value, value):
    return calculate_solar_radiation_shading_radians(obj, RAD(tilt), RAD(orientation), shading_value, value)


def calculate_solar_radiation_shading_radians(obj, tilt, orientation, shading_value, value):
    return calculate_solar_radiation_shading_position_radians(obj, tilt, orientation, float('NaN'), float('NaN'),
                                                              shading_value, value)


def calculate_solar_radiation_shading_position_radians(obj, tilt, orientation, latitude, longitude, shading_value,
                                                       value):
    sa = SolarAngles()
    ghr, dhr, dnr = 0.0, 0.0, 0.0
    cos_incident = 0.0
    std_time = 0.0
    solar_time = 0.0
    doy = 0
    dt = None

    if obj is None or value is None:
        return 0

    cli = Climate()
    if not isinstance(obj, Climate):
        return 0

    cli.get_solar_for_location(latitude, longitude, dnr, ghr, dhr)

    # Calculate solar radiation here
    value = (shading_value * dnr * cos_incident) + dhr * (1 + math.cos(tilt)) / 2.0 + ghr * (
                1 - math.cos(tilt)) * cli.ground_reflectivity / 2.0

    return 1


def calc_solar_solpos_shading_position_rad(obj, tilt, orientation, latitude, longitude, shading_value, value):
    sa = SolarAngles()
    ghr, dhr, dnr = 0.0, 0.0, 0.0
    cos_incident = 0.0
    temp_value = 0.0
    offsetclock = None

    if obj is None or value is None:
        return 0

    cli = Climate()
    if not isinstance(obj, Climate):
        return 0

    cli.get_solar_for_location(latitude, longitude, dnr, ghr, dhr)

    if cli.reader_type == 1:
        offsetclock = obj.clock + 1800
    else:
        offsetclock = obj.clock

    # Convert temperature to Celsius
    temp_value = ((cli.temperature - 32.0) * 5.0 / 9.0)

    sa.S_init(sa.solpos_vals)
    sa.solpos_vals.longitude = longitude
    sa.solpos_vals.latitude = RAD(latitude)
    sa.solpos_vals.timezone = cli.tz_offset_val - 1.0 if dt.is_dst == 1 else cli.tz_offset_val
    sa.solpos_vals.year = dt.year
    sa.solpos_vals.daynum = (dt.yearday + 1)
    sa.solpos_vals.hour = dt.hour + (-1 if dt.is_dst else 0)
    sa.solpos_vals.minute = dt.minute
    sa.solpos_vals.second = dt.second
    sa.solpos_vals.temp = temp_value
    sa.solpos_vals.press = cli.get_pressure()
    sa.solpos_vals.solcon = cli.get_direct_normal_extra()
    sa.solpos_vals.aspect = orientation
    sa.solpos_vals.tilt = tilt
    sa.solpos_vals.diff_horz = dhr
    sa.solpos_vals.dir_norm = dnr

    sa.S_solpos(sa.solpos_vals)

    if sa.solpos_vals.cosinc >= 0.0:
        cos_incident = sa.solpos_vals.cosinc
    else:
        cos_incident = 0.0

    value = (shading_value * dnr * cos_incident) + dhr * sa.solpos_vals.perez_horz + ghr * (
                (1 - math.cos(tilt)) * cli.get_ground_reflectivity() / 2.0)

    return 1


def calc_solar_ideal_shading_position_radians(obj, tilt, latitude, longitude, shading_value, value):
    ghr, dhr, dnr = 0.0, 0.0, 0.0
    cos_incident = 0.0
    temp_value = 0.0
    offsetclock = None

    if obj is None or value is None:
        return 0

    cli = Climate()
    if not isinstance(obj, Climate):
        return 0

    cli.get_solar_for_location(latitude, longitude, dnr, ghr, dhr)

    # Calculate solar radiation for ideal shading position

    value = (shading_value * dnr) + dhr * (1 + math.cos(tilt)) / 2.0 + ghr * (
                1 - math.cos(tilt)) * cli.get_ground_reflectivity() / 2.0

    return 1

def format_to_pattern(format_str):
    # Escape special characters in the format string
    pattern = re.escape(format_str)

    # Replace format specifiers with capturing groups
    pattern = re.sub(r'%[dfsc]', r'([\d.\w\s]+)', pattern)

    return pattern


class CLIMATERECORD:
    def __init__(self):
        self.low = 0.0
        self.low_day = 0.0
        self.high = 0.0
        self.high_day = 0.0
        self.solar = 0.0


import math

class TMY2Reader:
    """
       /**
       * This implements a Gridlab-D specific TMY2 data reader.  It was implemented
       * to pull specific information from the TMY2 raw format, including latitude
       * information contained in the TMY2 header.  Header information will be
       * maintained for the lifetime of the reader, as it may be needed to populate
       * columns of the TMY2 structure for later use.  Leap years are handled by
       * treating February 29th and March 1 as numerically equivalent.  IE on a
       * leap year, March 1 data is repeated for February 29th.
       */
    """
    def __init__(self, file_path=None):
        self.fp = None
        self.file_path = file_path

        self.buf = [None] * 500
        self.data_city   = ""
        self.data_state = ""
        self.el = [None] * 10
        self.elevation = 0
        self.high_temp = 0
        self.is_TMY2 = False
        self.lat_degrees = 0.0
        self.lat_minutes = 0.0
        self.ld = [None] * 10
        self.location_data = [None] * 10
        self.long_degrees = 0.0
        self.long_minutes = 0.0
        self.low_temp = 0
        self.peak_solar = 0
        self.surface_angles = []

        self.tlad = [None] * 10
        self.tlod = [None] * 10
        self.token = ""
        self.tz = [None] * 10
        self.tz_offset = 0
        self.tz_offset_temp = 0.0

    def open(self, file=None):
        """
        /**
        * Open the file for reading.  This will read in the header information
        * and position the file reader at the first data line in the file.
        *
        * This call will throw an exception if the file fails to open
        *
        * @param file the name of the TMY2 file to open
        */
        :param file:
        :return:
        """
        if not file:
            file = self.file_path

        lat_degrees_temp = 0.0
        long_degrees_temp = 0.0
        s = self.file_path
        delimiter = "."
        pos = 0

        # Process the file path to determine the format (TMY2 or TMY3)
        while s.find(delimiter, pos) != -1:
            pos = s.find(delimiter, pos)
            self.token = s[:pos]
            s = s[pos + len(delimiter):]
            pos = 0

        if file is None:
            gl_error(f"tmy2_reader::open() -- fopen failed on \"{file}\"")
            return False
        try:
            self.fp =  open(file, "r")
            self.buf = self.fp.readline()
            if self.buf:
                temp_lat_hem = ""
                temp_long_hem = ""

                if s == "tmy2":

                    #sscan_rv = sscanf(buf, "%*s %75s %3s %d %c %d %d %c %d %d %d",
                    #                  location_data, data_state, tz_offset, temp_lat_hem, lat_degrees, lat_minutes,
                    #                  temp_long_hem, long_degrees, long_minutes, elevation)
                    # Assuming buf contains the input string
                    pattern = r".{1} (?P<data_city>.{1,75}) (?P<data_state>.{3}) (?P<tz_offset>\d+) (?P<temp_lat_hem>[NS]) (?P<lat_degrees>\d+) (?P<lat_minutes>\d+) (?P<temp_long_hem>[EW]) (?P<long_degrees>\d+) (?P<long_minutes>\d+) (?P<elevation>\d+)"

                    # Use re.search to find the pattern in the input string
                    match = re.search(pattern, self.buf)

                    if match:
                        # Extract the values using group names
                        self.data_city = match.group("data_city")[:75]
                        self.data_state = match.group("data_state")[:3]
                        self.tz_offset = int(match.group("tz_offset"))
                        temp_lat_hem = match.group("temp_lat_hem")
                        self.lat_degrees = int(match.group("lat_degrees"))
                        self.lat_minutes = int(match.group("lat_minutes"))
                        temp_long_hem = match.group("temp_long_hem")
                        self.long_degrees = int(match.group("long_degrees"))
                        self.long_minutes = int(match.group("long_minutes"))
                        self.elevation = int(match.group("elevation"))
                    gl_warning("Daylight saving time (DST) is not handled correctly when using TMY2 datasets; "
                               "please use TMY3 for DST-corrected weather data.")
                    self.is_TMY2 = True
                elif s == "tmy3":
                    #sscan_rv = sscanf(buf, "%*[^','],%[^','],%[^','],%[^','],%[^','],%[^','],%s",
                    #                  location_data, data_state, tz, tlad, tlod, el)
                    # Assuming buf contains the input string
                    pattern = r".*?,(?P<data_city>[^,]*),(?P<data_state>[^,]*),(?P<tz>[^,]*),(?P<tlad>[^,]*),(?P<tlod>[^,]*),(?P<el>[^,]*)"

                    # Use re.search to find the pattern in the input string
                    match = re.search(pattern, self.buf)

                    if match:
                        # Extract the values using group names
                        self.data_city = match.group("data_city")
                        self.data_state = match.group("data_state")
                        tz_offset_temp = float(match.group("tz"))
                        self.tz_offset = int(tz_offset_temp)
                        lat_degrees_temp = float(match.group("tlad"))
                        long_degrees_temp = float(match.group("tlod"))
                        self.elevation = int(match.group("el"))

                    if lat_degrees_temp < 0:
                        temp_lat_hem = 'S'
                        lat_degrees_temp = -lat_degrees_temp
                    else:
                        temp_lat_hem = 'N'

                    if long_degrees_temp < 0:
                        temp_long_hem ='W'
                        long_degrees_temp = -long_degrees_temp
                    else:
                        temp_long_hem = 'E'

                    frac_degrees, degrees = modf(lat_degrees_temp)
                    self.lat_minutes = int(abs(round(frac_degrees * 60)))
                    self.lat_degrees = abs(int(lat_degrees_temp))
                    frac_degrees, degrees = modf(long_degrees_temp)
                    self.long_minutes = int(abs(round(frac_degrees * 60)))
                    self.long_degrees = abs(int(long_degrees_temp))
                if temp_lat_hem.lower() == 's':
                    self.lat_degrees = -self.lat_degrees

                if temp_long_hem.lower() == 'W':
                    self.long_degrees = -self.long_degrees
            else:
                gl_error("tmy2_reader::open() -- first readline read nothing")
                return False

        except FileNotFoundError:
            gl_error(f"tmy2_reader::open() -- file not found: {file}")
            return False

    def next(self):
        """
        /**
        * Store the current line in a buffer for later reading by read_data
        */
        :return:
        """
        self.buf = self.fp.readline()
        return True if self.buf else False

    def header_info(self, city=None, state=None, degrees=None, minutes=None, long_deg=None, long_min=None):
        # /**
        # 	Passes the header data by reference out to the calling function.
        #
        # 	@param city the city the data represents
        # 	@param state the state the city is located in
        # 	@param degrees latitude degrees
        # 	@param minutes latitude minutes
        # 	@param long_deg longitude degrees
        # 	@param long_min longitude minutes
        # */
        self.data_city = "CityName"  # Replace with your default city name
        self.data_state = "StateName"  # Replace with your default state name
        self.lat_degrees = 0  # Replace with your default latitude degrees
        self.lat_minutes = 0  # Replace with your default latitude minutes
        self.long_degrees = 0  # Replace with your default longitude degrees
        self.long_minutes = 0  # Replace with your default longitude minutes

        if city:
            city = self.data_city[:len(city)]  # Potential buffer overflow
        if state:
            state = self.data_state[:len(state)]  # Potential buffer overflow
        if degrees:
            degrees = self.lat_degrees
        if minutes:
            minutes = self.lat_minutes
        if long_deg:
            long_deg = self.long_degrees
        if long_min:
            long_min = self.long_minutes
        return True, city, state, degrees, minutes, long_deg, long_min


    def read_data(self, dnr, dhr, ghr, tdb, rh, month, day, hour,
                  wind, winddir, precip, snowDepth, pressure,
                  extra_terr_dni, extra_terr_ghi, tot_sky_cov,
                  opq_sky_cov):
        """
        :param dnr: Direct Normal Radiation
        :param dhr: Diffuse Horizontal Radiation
        :param ghr:
        :param tdb: Bulb temperature
        :param rh: Relative Humidity
        :param month:  month of year
        :param day: day of month
        :param hour: hour of day
        :param wind: Wind speed (optional)
        :param winddir:
        :param precip:
        :param snowDepth:
        :param pressure: atmospheric pressure
        :param extra_terr_dni: Extra terrestrial direct normal irradiance (top of atmosphere)
        :param extra_terr_ghi:
        :param tot_sky_cov:
        :param opq_sky_cov:
        :return:
        """
        self.buf = self.fp.readline()
        if not self.buf:
            return 0

        rct = 0
        rct_ymd = 0
        rct_hm = 0
        tmp_dnr, tmp_dhr, tmp_tot_sky_cov, tmp_opq_sky_cov, tmp_tdb, tmp_rh, tmp_wd, tmp_ws, tmp_precip, tmp_sf, tmp_ghr, tmp_extra_ghr, tmp_extra_dni, tmp_press = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

        if self.buf[2] == '/':
            # Define a regular expression pattern to match the values
            pattern = r"([^',']+),([^',']+),([^',']+),([^',']+),([^',']+),[^',']+,[^',']+," \
                      r"([^',']+),[^',']+,[^',']+,[^',']+,[^',']+,[^',']+,[^',']+,[^',']+," \
                      r"[^',']+,[^',']+,[^',']+,[^',']+,[^',']+,[^',']+,[^',']+,[^',']+," \
                      r"[^',']+,[^',']+,[^',']+,[^',']+,[^',']+,[^',']+,[^',']+,[^',']+," \
                      r"[^',']+,[^',']+,[^',']+,[^',']+,[^',']+,[^',']+,[^',']+,[^',']+," \
                      r"[^',']+,[^',']+,[^',']+,[^',']+,[^',']+,[^',']+,[^',']+,[^',']+," \
                      r"[^',']+,[^',']+,[^',']+,[^',']+,[^',']+,[^',']+,[^',']+,[^',']+," \
                      r"[^',']+,[^',']+,[^',']+,[^',']+,[^',']+,[^',']+,[^',']+,[^',']+," \
                      r"[^',']+,[^',']+,[^',']+,[^',']+,[^',']+,[^',']+,[^',']+,[^',']+," \
                      r"[^',']+,[^',']+,[^',']+,[^',']+,[^',']+,[^',']+,[^',']+,[^',']+," \
                      r"[^',']+,[^',']+,[^',']+,[^',']+,[^',']+,[^',']+,[^',']+,[^',']+," \
                      r"[^',']+,[^',']+,[^',']+,[^',']+,[^',']+,[^',']+,[^',']+,[^',']+," \
                      r"[^',']+,[^',']+,[^',']+,[^',']+,[^',']+,[^',']+,[^',']+,[^',']+," \
                      r"[^',']+,[^',']+,[^',']+,[^',']+,[^',']+,[^',']+,[^',']+,[^',']+," \
                      r"[^',']+,[^',']+,[^',']+,[^',']+,[^',']+,[^',']+,[^',']+,[^',']+" \
                      r",[^',']+,[^',']+,[^',']+,[^',']+,[^',']+"

            # Use re.findall to find all occurrences of the pattern in the input string
            matches = re.findall(pattern, self.buf)

            if matches:
                # Extract the values
                (t_ymd, t_hm, t_ehr, t_dni, t_ghr, t_dnr, t_dhr, t_tkc, t_osc, t_tdb,
                 t_rh, t_press, t_wd, t_ws, t_precip, t_sf) = matches[0]

                # Example input strings
                # t_ymd = "12/34/5678"  # Replace with your actual input string
                # t_hm = "12:34"  # Replace with your actual input string

                # Define regular expressions to match the values
                ymd_pattern = r"(\d+)/(\d+)/\d+"
                hm_pattern = r"(\d+):\d+"

                # Use re.match to extract the values
                ymd_match = re.match(ymd_pattern, t_ymd)
                hm_match = re.match(hm_pattern, t_hm)

                # Initialize variables
                rct_ymd = 0
                rct_hm = 0

                if ymd_match:
                    # Extract month and day
                    month = int(ymd_match.group(1))
                    day = int(ymd_match.group(2))
                    rct_ymd = 2

                if hm_match:
                    # Extract hour
                    hour = int(hm_match.group(1))
                    rct_hm = 1
                rct = 17

        else:
            rct = 0
            # Define a regular expression pattern to match the values
            pattern = r".*?(\d{2})(\d{2})(\d{2})(\d{4})(\d{4})(\d{4}).*?(\d{4}).*?(\d{4})" \
                      r".*?(\d{3}).*?(\d{4}).*?(\d{2}).*?(\d{2}).*?(\d{4}).*?(\d{3}).*?(\d{4})" \
                      r".*?(\d{2}).*?(\d{3}).*?(\d{3})"

            # Use re.search to find the pattern in the input string
            match = re.search(pattern, self.buf)

            if match:
                # Extract the values
                month = int(match.group(1))
                day = int(match.group(2))
                hour = int(match.group(3))
                tmp_extra_ghr = int(match.group(4))
                tmp_extra_dni = int(match.group(5))
                tmp_ghr = int(match.group(6))
                tmp_dnr = int(match.group(7))
                tmp_dhr = int(match.group(8))
                tmp_tot_sky_cov = int(match.group(9))
                tmp_opq_sky_cov = int(match.group(10))
                tmp_tdb = int(match.group(11))
                tmp_rh = int(match.group(12))
                tmp_press = int(match.group(13))
                tmp_wd = int(match.group(14))
                tmp_ws = int(match.group(15))
                tmp_precip = int(match.group(16))
                tmp_sf = int(match.group(17))
                rct = 17

        if rct != 17:
            print(f"TMY reader did not get 17 values for line time {month}/{day} {hour}00")

        if dnr:
            dnr = tmp_dnr
        if dhr:
            dhr = tmp_dhr
        if ghr:
            ghr = tmp_ghr

        if extra_terr_dni:
            extra_terr_dni = tmp_extra_dni

        if pressure:
            pressure = tmp_press

        if tdb:
            tdb = float(tmp_tdb) / 10.0
            if tdb < self.low_temp or self.low_temp == 0:
                self.low_temp = tdb
            elif tdb > self.high_temp or self.high_temp == 0:
                self.high_temp = tdb

        if rh:
            rh = float(tmp_rh) / 100.0

        if wind:
            wind = float(tmp_ws) / 10.0

        if precip:
            precip = float(tmp_precip) * 0.03937  # Convert precip in mm to in/h

        if snowDepth:
            snowDepth = float(tmp_sf) * 0.3937  # Convert snowfall in cm to in

        if extra_terr_ghi:
            extra_terr_ghi  = tmp_extra_ghr

        if tot_sky_cov:
            tot_sky_cov = float(tmp_tot_sky_cov) / 10.0  # Total sky cover

        if opq_sky_cov:
            opq_sky_cov = float(tmp_opq_sky_cov) / 10.0  # Opaque sky cover

        if winddir:
            winddir = tmp_wd

        return 1, dnr, dhr, ghr, tdb, rh, month, day, hour, \
                  wind, winddir, precip, snowDepth, pressure, \
                  extra_terr_dni, extra_terr_ghi, tot_sky_cov, \
                  opq_sky_cov

    def calc_solar(self, cpt, doy, lat, sol_time, dnr, dhr, ghr, gnd_ref, vert_angle=90):
        """
        Calculate the solar radiation for a surface facing the given compass point.

        :param cpt: compass point of the direction the surface is facing
        :param doy: day of year
        :param lat: latitude of the surface
        :param sol_time: the solar time of day
        :param dnr: Direct Normal Radiation
        :param dhr: Diffuse Horizontal Radiation
        :param ghr: Global Horizontal Radiation
        :param gnd_ref: Ground Reflectivity
        :param vert_angle: the angle of the surface relative to the horizon (Default is 90 degrees)
        :return:
        """

        sa = SolarAngles()
        surface_angle = self.surface_angles[cpt]
        cos_incident = sa.cos_incident(lat, math.radians(vert_angle), math.radians(surface_angle),
                                         sol_time, doy)
        solar = dnr * cos_incident + dhr
        if not hasattr(self, 'peak_solar') or solar > self.peak_solar:
            self.peak_solar = solar
        return solar

    def close(self):
        self.fp.close()


def gl_convert(param, param1, meter_to_feet):
    pass


def gl_find_objects(FL_GROUP, param):
    pass


def gl_find_next(items, param):
    pass



class Climate:
    oclass = None
    defaults = None

    def __init__(self, parent=None):

        # data not shared with classes in this module (no locks needed)
        # get_/set_ accessors for classes in this module only (non-atomic data need locks on access)
        self.MAX_LAT = 0.0
        self.MAX_LAT_INDEX = 0
        self.MIN_LAT = 0.0
        self.MIN_LAT_INDEX = 0
        self.city = ""
        self.cloud_aerosol_transmissivity = 0.95 # Attenuation factor of no-cloud (clear-sky) radiation due to aerosols
        self.cloud_alpha = 400  # Determines the distance between the shading layers of the normalized patterns.
        self.cloud_model = CLOUDMODEL.CM_NONE
        self.cloud_num_layers = 40 # Higher number of layers makes for the possibility of wispier clouds.
        self.cloud_opacity = 1.0
        self.cloud_reflectivity = 0.0
        self.cloud_speed_factor = 1.0
        self.direct_normal_extra = 126.998456
        self.file = TMY2Reader()
        self.forecast_spec = ""
        self.global_horizontal_extra = 0.0
        self.global_transmissivity = 0.0
        self.ground_reflectivity = 0.3  # flux reflectivity of ground (W/sf)
        self.humidity = 0.75 # relative humidity (%)
        self.interpolate = CI.CI_NONE
        self.opq_sky_cov = 0.0
        self.parent = parent
        self.pressure = 1000
        self.rainfall = 0.0  # rainfall rate (in/h)
        self.reader = None  # the file reader to use when loading data
        self.reader_hndl = None
        self.reader_type = None
        self.record = CLIMATERECORD()
        self.record_high = 0.0
        self.record_high_day = 0
        self.record_low = 0.0
        self.record_low_day = 0
        self.record_solar = 0.0
        self.sa = None
        self.snowdepth = 0.0  # snow accumulation (in)
        self.solar_azimuth = 0.0
        self.solar_cloud_diffuse = 0.0  # READ ONLY: diffuse solar flux after modification by the cloud model (W/sf)
        self.solar_cloud_direct = 0.0  # READ ONLY: direct solar flux after modification by the cloud model (W/sf)
        self.solar_cloud_global = 0.0  # READ ONLY: global solar flux after modification by the cloud model (W/sf)
        self.solar_diffuse = 0.0  # diffuse solar flux (W/sf)
        self.solar_direct = 0.0  # direct solar flux (W/sf)
        self.solar_elevation = 0.0
        self.solar_flux = [0.0] * 9  # [0.0] * CP_LAST  # Solar flux array (W/sf)
        self.solar_flux_CP_E = 0.0
        self.solar_flux_CP_H = 0.0
        self.solar_flux_CP_N = 0.0
        self.solar_flux_CP_NE = 0.0
        self.solar_flux_CP_NW = 0.0
        self.solar_flux_CP_S = 0.0
        self.solar_flux_CP_SE = 0.0
        self.solar_flux_CP_SW = 0.0
        self.solar_flux_CP_W = 0.0
        self.solar_global = 0.0  # global solar flux (W/sf)
        self.solar_raw = 0.0
        self.solar_zenith = 0.0
        self.temperature = 59.0  # temperature (degF)
        self.temperature_raw = 0.0  # the temperature (degC)
        self.tmy = TMYDATA()
        self.tmyfile = ""  # the TMY file name
        self.tot_sky_cov = 0.0
        self.tz_meridian = 0.0  # timezone meridian
        self.tz_offset_val = 0.0
        self.update_time = 0.0
        self.wind_dir = 0.0
        self.wind_gust = 0.0
        self.wind_speed = 0.0  # wind speed (mph)


        if Climate.oclass is None:
            Climate.oclass = self.create_class(parent)
        if Climate.defaults is None:
            Climate.defaults = self

    def create_class(self, module):
        # Create and return the class
        oclass = Climate(module)  # gl_register_class(module, "climate", PC_PRETOPDOWN | PC_AUTOLOCK)
        if oclass is None:
            raise Exception("Unable to register class climate")

        # gl_publish_variable(oclass,
        #     PT_double, "solar_elevation", self.get_offset("solar_elevation"),
        #     PT_double, "solar_azimuth", self.get_offset("solar_azimuth"),
        #     PT_double, "solar_zenith", self.get_offset("solar_zenith"),
        #     PT_char32, "city", self.get_offset("city"),
        #     PT_char1024, "tmyfile", self.get_offset("tmyfile"),
        #     PT_double, "tz_meridian", self.get_offset("tz_meridian"),
        #     PT_double, "temperature[degF]", self.get_offset("temperature"),
        #     PT_double, "humidity[pu]", self.get_offset("humidity"),
        #     PT_double, "solar_flux[W/sf]", self.get_offset("solar_flux"), PT_SIZE, 9,
        #     PT_double, "solar_direct[W/sf]", self.get_offset("solar_direct"),
        #     PT_double, "solar_diffuse[W/sf]", self.get_offset("solar_diffuse"),
        #     PT_double, "solar_global[W/sf]", self.get_offset("solar_global"),
        #     PT_double, "extraterrestrial_global_horizontal[W/sf]", self.get_offset("global_horizontal_extra"),
        #     PT_double, "extraterrestrial_direct_normal[W/sf]", self.get_offset("direct_normal_extra"),
        #     PT_double, "pressure[mbar]", self.get_offset("pressure"),
        #     PT_double, "wind_speed[mph]", self.get_offset("wind_speed"),
        #     PT_double, "wind_dir[deg]", self.get_offset("wind_dir"),
        #     PT_double, "wind_gust[mph]", self.get_offset("wind_gust"),
        #     PT_double, "record.low[degF]", self.get_offset("record_low"),
        #     PT_int32, "record.low_day", self.get_offset("record_low_day"),
        #     PT_double, "record.high[degF]", self.get_offset("record_high"),
        #     PT_int32, "record.high_day", self.get_offset("record_high_day"),
        #     PT_double, "record.solar[W/sf]", self.get_offset("record_solar"),
        #     PT_double, "rainfall[in/h]", self.get_offset("rainfall"),
        #     PT_double, "snowdepth[in]", self.get_offset("snowdepth"),
        #     PT_enumeration, "interpolate", self.get_offset("interpolate"),
        #     PT_KEYWORD, "NONE", CI.CI_NONE,
        #     PT_KEYWORD, "LINEAR", CI.CI_LINEAR,
        #     PT_KEYWORD, "QUADRATIC", CI_QUADRATIC,
        #     PT_double, "solar_horiz", self.get_offset("solar_flux_CP_H"),
        #     PT_double, "solar_north", self.get_offset("solar_flux_CP_N"),
        #     PT_double, "solar_northeast", self.get_offset("solar_flux_CP_NE"),
        #     PT_double, "solar_east", self.get_offset("solar_flux_CP_E"),
        #     PT_double, "solar_southeast", self.get_offset("solar_flux_CP_SE"),
        #     PT_double, "solar_south", self.get_offset("solar_flux_CP_S"),
        #     PT_double, "solar_southwest", self.get_offset("solar_flux_CP_SW"),
        #     PT_double, "solar_west", self.get_offset("solar_flux_CP_W"),
        #     PT_double, "solar_northwest", self.get_offset("solar_flux_CP_NW"),
        #     PT_double, "solar_raw[W/sf]", self.get_offset("solar_raw"),
        #     PT_double, "ground_reflectivity[pu]", self.get_offset("ground_reflectivity"),
        #     PT_object, "reader", self.get_offset("reader"),
        #     PT_char1024, "forecast", self.get_offset("forecast_spec"),
        #     PT_enumeration, "cloud_model", self.get_offset("cloud_model"),
        #     PT_KEYWORD, "NONE", CM_NONE,
        #     PT_KEYWORD, "CUMULUS", CM_CUMULUS,
        #     PT_double, "cloud_opacity[pu]", self.get_offset("cloud_opacity"),
        #     PT_double, "opq_sky_cov[pu]", self.get_offset("opq_sky_cov"),
        #     PT_double, "cloud_speed_factor[pu]", self.get_offset("cloud_speed_factor"),
        #     PT_double, "solar_cloud_direct[W/sf]", self.get_offset("solar_cloud_direct"),
        #     PT_double, "solar_cloud_diffuse[W/sf]", self.get_offset("solar_cloud_diffuse"),
        #     PT_double, "solar_cloud_global[W/sf]", self.get_offset("solar_cloud_global"),
        #     PT_double, "cloud_alpha[pu]", self.get_offset("cloud_alpha"),
        #     PT_double, "cloud_num_layers[pu]", self.get_offset("cloud_num_layers"),
        #     PT_double, "cloud_aerosol_transmissivity[pu]", self.get_offset("cloud_aerosol_transmissivity"),
        #     PT_double, "update_time", self.get_offset("update_time"),
        #     None)

        return oclass

    def create(self):
        defaults = Climate.defaults

        # cloud_reflectivity = 1.0; // very reflective!
        # solar_flux = malloc(8 * sizeof(double));
        # solar_flux_S = solar_flux_SE = solar_flux_SW = solar_flux_E = solar_flux_W = solar_flux_NE = solar_flux_NW = solar_flux_N = 0.0; // W / sf normal
        self.city = ""
        self.cloud_aerosol_transmissivity = 0.95
        self.cloud_alpha = 400
        self.cloud_model = CLOUDMODEL.CM_NONE
        self.cloud_num_layers = 40
        self.cloud_opacity = defaults.cloud_opacity
        self.cloud_speed_factor = 1.0
        self.direct_normal_extra = defaults.direct_normal_extra  # 1367 W / m ^ 2 constant in W / ft ^ 2
        self.forecast_spec = ""
        self.global_horizontal_extra = defaults.global_horizontal_extra
        self.ground_reflectivity = defaults.ground_reflectivity
        self.humidity = 0.75
        self.interpolate = CI.CI_NONE
        self.opq_sky_cov = 0.0
        self.pressure = 1000  # Sea level assumption
        self.rainfall = 0.0
        self.reader = None
        self.record_high = 0.0
        self.record_high_day = 0
        self.record_low = 0.0
        self.record_low_day = 0
        self.record_solar = 0.0
        self.snowdepth = 0.0
        self.solar_azimuth = defaults.solar_azimuth
        self.solar_cloud_diffuse = 0.0
        self.solar_cloud_direct = 0.0
        self.solar_cloud_global = 0.0
        self.solar_diffuse = 0.0
        self.solar_direct = 0.0
        self.solar_elevation = defaults.solar_elevation
        self.solar_flux = [0.0] * 9  # W / sf normal
        self.solar_flux_CP_E = defaults.solar_flux_CP_E
        self.solar_flux_CP_H = defaults.solar_flux_CP_H
        self.solar_flux_CP_N = defaults.solar_flux_CP_N
        self.solar_flux_CP_NE = defaults.solar_flux_CP_NE
        self.solar_flux_CP_NW = defaults.solar_flux_CP_NW
        self.solar_flux_CP_S = defaults.solar_flux_CP_S
        self.solar_flux_CP_SE = defaults.solar_flux_CP_SE
        self.solar_flux_CP_SW = defaults.solar_flux_CP_SW
        self.solar_flux_CP_W = defaults.solar_flux_CP_W
        self.solar_global = 0.0
        self.solar_raw = 0.0
        self.solar_zenith = defaults.solar_zenith
        self.temperature = 59.0
        self.temperature_raw = 15.0;
        self.tmy = None
        self.tmyfile = ""
        self.tz_meridian = defaults.tz_meridian
        self.update_time = 0.0
        self.wind_dir = 0.0
        self.wind_gust = 0.0
        self.wind_speed = 0.0

    def isa(self, classname):
        return classname == "climate"

    def init(self, parent):
        dot = None
        # obj = self
        t0 = self.clock
        meter_to_feet = 1.0
        tz_num_offset = 0.0

        self.reader_type = RT.RT_NONE

        # Ignore "" files ~ manual climate control is a feature
        if self.tmyfile == "":
            print("Manual or FNCS/HELICS climate control; initializing to the starttime")
            self.presync(gl_globalclock)
            return 1

        # Open access to the TMY file
        found_file = None  # You need to set this to the path of the found file
        if found_file is None:
            print("Weather file access failed: " + self.tmyfile)
            return 0

        if self.cloud_model != CLOUDMODEL.CM_NONE:
            # Cloud model input error checking
            if self.cloud_opacity > 1:
                print("Climate: {} - Cloud opacity must be no greater than 1.0, setting to 1.0".format(self.name))
                self.cloud_opacity = 1.0
            elif self.cloud_opacity < 0:
                print("Climate: {} - Cloud opacity must be no less than 0.0, setting to 0.0".format(self.name))
                self.cloud_opacity = 0.0

            if self.cloud_speed_factor < 0:
                print("Climate: {} - Cloud speed adjustment cannot be negative, setting to 1.0".format(self.name))
                self.cloud_speed_factor = 1.0

            if self.cloud_alpha < self.cloud_num_layers:
                print(
                    "Climate: {} - Cloud model alpha value must be less than or equal to cloud_num_layers, setting to cloud_num_layers".format(
                        self.name))
                self.cloud_alpha = self.cloud_num_layers

            if self.cloud_aerosol_transmissivity < 0:
                print(
                    "Climate: {} - Cloud model aerosol transmissivity must be greater than or equal to 0, setting to default value of 0.9".format(
                        self.name))
                self.cloud_aerosol_transmissivity = 0.9

            if self.cloud_aerosol_transmissivity > 1:
                print(
                    "Climate: {} - Cloud model aerosol transmissivity must be less than or equal to 1, setting to 1".format(
                        self.name))
                self.cloud_aerosol_transmissivity = 1.0

            print(
                "This cloud model places a large burden on computational resources. Patience and/or a more capable computer may be required.")
            self.init_cloud_pattern()
            self.convert_to_binary_cloud()
            self.convert_to_fuzzy_cloud(EMPTY_VALUE, self.cloud_num_layers, self.cloud_alpha)
            self.prev_NTime = t0 - 60

        if ".tmy2" in self.tmyfile or ".tmy" in self.tmyfile:
            self.reader_type = RT.RT_TMY2
        elif ".csv" in self.tmyfile:
            self.reader_type = RT.RT_CSV
        else:
            print("Climate: unrecognized filetype, assuming TMY2")

        if self.reader_type == RT.RT_CSV:
            # May or may not have an object, have not called open()
            rv = 0

            if self.reader is None:
                print("Climate::init(): no csv_reader specified for tmyfile", self.tmyfile)
                return 0
            else:
                if (self.reader.flags & OF_INIT) != OF_INIT:
                    objname = ""
                    print("Climate::init(): deferring initialization on", gl_name(self.reader, objname, 255))
                    return 2  # Defer

                with open('file.csv', 'r') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        print(row)

                self.reader_hndl = csv.reader(self.reader)
                tz_num_offset =  self.reader_hndl.__next__()
                self.tz_offset_val = tz_num_offset

                # Copy latitude and longitude information from CSV reader
                self.latitude = self.reader.latitude
                self.longitude = self.reader.longitude

                # CSV Reader validity check
                if abs(self.latitude) > 90:
                    print("Climate: {} - Latitude is outside +/-90!".format(self.name))
                    return 0

                if abs(self.longitude) > 180:
                    print("Climate: {} - Longitude is outside +/-180!".format(self.name))
                    return 0

                # Generic warning about the southern hemisphere and Duffie-Beckman usage
                if self.latitude < 0:
                    print("Climate: {} - Southern hemisphere solar position model may have issues".format(self.name))

                # Set the timezone offset
                self.tz_meridian = 15 * tz_num_offset

        # Implicit if self.reader_type == RT_TMY2
        if self.file.open(found_file) < 3:
            print("Climate::init() -- weather file header improperly formed")
            return 0

        # Begin parsing the TMY file
        line = 0
        self.tmy = [None] * 8760
        lat_deg, lat_min, long_deg, long_min = 0, 0, 0, 0
        # The city/state data isn't used anywhere.
        # self.file.header_info(cty, st, lat_deg, lat_min, long_deg, long_min)
        self.file.header_info(None, None, lat_deg, lat_min, long_deg, long_min)

        # Handle hemispheres
        if lat_deg < 0:
            self.set_latitude(float(lat_deg) - (float(lat_min) / 60))
        else:
            self.set_latitude(float(lat_deg) + (float(lat_min) / 60))

        if long_deg < 0:
            self.set_longitude(float(long_deg) - (float(long_min) / 60))
        else:
            self.set_longitude(float(long_deg) + (float(long_min) / 60))

        # Generic check for TMY files
        if abs(self.latitude) > 90:
            print("Climate: {} - Latitude is outside +/-90!".format(self.name))
            # 		/*  TROUBLESHOOT
            # 		The value read from the weather data indicates a latitude of greater
            # 		than 90 or less than -90 degrees.  This is not a valid value.  Please specify
            # 		the latitude in this range, with positive values representing the northern hemisphere
            # 		and negative values representing the southern hemisphere.
            # 		*/
            return 0

        if abs(self.longitude) > 180:
            print("Climate: {} - Longitude is outside +/-180!".format(self.name))
            # 		/*  TROUBLESHOOT
            # 		The value read from the weather data indicates a longitude of greater
            # 		than 180 or less than -180 degrees.  This is not a valid value.  Please specify
            # 		the longitude in this range, with positive values representing the eastern hemisphere
            # 		and negative values representing the western hemisphere.
            # 		*/
            return 0

        # Generic warning about southern hemisphere and Duffie-Beckman usage
        if self.latitude < 0:
            print("Climate: {} - Southern hemisphere solar position model may have issues".format(self.name))

        if gl_convert("multiplicities", "ft", meter_to_feet) == 0:
            print("Climate::init unable to gl_convert() 'multiplicities' to 'ft'!")
            return 0

        self.file.elevation = int(self.file.elevation * meter_to_feet)
        self.tz_meridian = 15 * self.file.tz_offset
        self.tz_offset_val = self.file.tz_offset

        while line < 8760 and self.file.next():
            while not self.file.buf.isdigit():
                self.file.next()

            dnr = 0
            dhr = 0
            ghr = 0
            month = 0
            day = 0
            hour = 0
            wspeed = 0
            wdir = 0
            precip = 0
            snowdepth = 0
            pressure = 0
            extra_dni = 0
            extra_ghi = 0
            tot_sky_cov = 0
            opq_sky_cov = 0
            windgust = 0
            (cnt, self.dnr, self.dhr, self.ghr,  self.temperature, self.humidity, self.month, self.day, self.hour, self.wspeed, self.wdir,
             self.precip, self.snowdepth, self.pressure, self.extra_dni, self.extra_ghi, self.tot_sky_cov,
             self.opq_sky_cov, self.windgust) =  \
                self.file.read_data(dnr, dhr, ghr, self.temperature, self.humidity, month, day, hour, wspeed, wdir,
                                    precip, snowdepth, pressure, extra_dni, extra_ghi, tot_sky_cov,
                                    opq_sky_cov)

            doy, hoy = self.doy_to_hoy(self.month, self.day, self.hour)

            if hoy >= 0 and hoy < 8760:
                # pre-conversion of solar data from W/multiplicities^2 to W/sf
                if 0 == gl_convert("W/multiplicities^2", "W/sf", self.dnr):
                    gl_error("climate::init unable to gl_convert() 'W/multiplicities^2' to 'W/sf'!")
                    return 0

                if 0 == gl_convert("W/multiplicities^2", "W/sf", self.dhr):
                    gl_error("climate::init unable to gl_convert() 'W/multiplicities^2' to 'W/sf'!")
                    return 0

                if 0 == gl_convert("W/multiplicities^2", "W/sf", self.ghr):
                    gl_error("climate::init unable to gl_convert() 'W/multiplicities^2' to 'W/sf'!")
                    return 0

                if 0 == gl_convert("W/multiplicities^2", "W/sf", self.extra_dni):
                    gl_error("climate::init unable to gl_convert() 'W/multiplicities^2' to 'W/sf'!")
                    return 0

                if 0 == gl_convert("W/multiplicities^2", "W/sf", self.extra_ghi):
                    gl_error("climate::init unable to gl_convert() 'W/multiplicities^2' to 'W/sf'!")
                    return 0

                if 0 == gl_convert("mps", "mph", self.wspeed):
                    gl_error("climate::init unable to gl_convert() 'multiplicities/status' to 'miles/h'!")
                    return 0

                self.tmy[hoy].temp_raw = self.temperature
                self.tmy[hoy].temp = self.temperature
                # post-conversion of copy of temperature from C to F
                if 0 == gl_convert("degC", "degF", self.tmy[hoy].temp):
                    gl_error("climate::init unable to gl_convert() 'degC' to 'degF'!")
                    return 0

                self.tmy[hoy].windspeed = self.wspeed
                self.tmy[hoy].rh = self.humidity
                self.tmy[hoy].dnr = self.dnr
                self.tmy[hoy].dhr = self.dhr
                self.tmy[hoy].ghr = self.ghr
                self.tmy[hoy].rainfall = self.precip
                self.tmy[hoy].snowdepth = self.snowdepth
                self.tmy[hoy].solar_raw = self.dnr
                self.tmy[hoy].direct_normal_extra = self.extra_dni
                self.tmy[hoy].pressure = self.pressure
                self.tmy[hoy].global_horizontal_extra = self.extra_ghi
                self.tmy[hoy].wind_dir = self.wdir
                self.tmy[hoy].tot_sky_cov = self.tot_sky_cov
                self.tmy[hoy].opq_sky_cov = self.opq_sky_cov

                sol_time = self.solar_time(hour, doy, RAD(self.tz_meridian), RAD(self.get_longitude()))
                sol_rad = 0.0

                self.tmy[hoy].solar_elevation = self.altitude(doy, RAD(self.latitude), sol_time)
                self.tmy[hoy].solar_azimuth = self.azimuth(doy, RAD(self.latitude), sol_time)
                self.tmy[hoy].solar_zenith = ( math.pi/2.0 ) - self.tmy[hoy].solar_elevation

                for c_point in range(COMPASS_PTS.CP_H, COMPASS_PTS.CP_LAST):
                    if c_point == COMPASS_PTS.CP_H:
                        sol_rad = self.file.calc_solar(COMPASS_PTS.CP_E, doy,
                                                       RAD(self.get_latitude()),
                                                       sol_time, self.dnr, self.dhr, self.ghr, self.ground_reflectivity,
                                                  0.0)
                    else:
                        sol_rad = self.file.calc_solar(c_point, doy, RAD(self.get_latitude()), sol_time, dnr, dhr, ghr,
                                                  self.ground_reflectivity)
                    # TMY2 solar radiation data is in Watt-hours per square meter.
                    self.tmy[hoy].solar[c_point] = sol_rad

                    # track records
                    if sol_rad > self.record.solar or self.record.solar == 0:
                        self.record.solar = sol_rad
                    if self.tmy[hoy].temp > self.record.high or self.record.high == 0:
                        self.record.high = self.tmy[hoy].temp
                        self.record.high_day = doy
                    if self.tmy[hoy].temp < self.record.low or self.record.low == 0:
                        self.record.low = self.tmy[hoy].temp
                        self.record.low_day = doy
                else:
                    gl_error("%status(%d): day %d, hour %d is out of allowed range 0-8759 hours", self.tmyfile.get_string(), line,
                             day, hour)

                line += 1
        self.file.close()

        self.presync(self.gl_globalclock)

        # 	/* enable forecasting if specified */
        # #if 0
        # 	if ( strcmp(forecast_spec,"")!=0 && gl_forecast_create(my(),forecast_spec)==NULL )
        # 	{
        # 		gl_error("%status: forecast '%status' is not valid", get_name(), forecast_spec.get_string());
        # 		return 0;
        # 	}
        # 	else if (get_forecast()!=NULL)
        # 	{
        # 		/* initialize the forecast data entity */
        # 		FORECAST *fc = get_forecast();
        # 		fc->propref = get_property("temperature");
        # 		gl_forecast_save(fc,get_clock(),3600,0,NULL);
        # 		set_flags(get_flags()|OF_FORECAST);
        # 	}
        # #endif


        return 1

    def get_solar_for_location(self, latitude, longitude, direct, global_solar, diffuse):
        retval = 1
        cloud = 0  # Fuzzy cloud
        f = 0.0
        ETR = 0.0
        ETRN = 0.0
        sol_z = 0.0

        dt = self.get_localtime(self.clock)

        # Switch to handle different cloud models (you may need to implement these methods)
        # You can uncomment and implement get_fuzzy_cloud_value_for_location and get_binary_cloud_value_for_location as needed.
        # For now, I'multiplicities using a placeholder function get_cloud_model to determine the cloud model.
        cloud_model = self.get_cloud_model()
        if cloud_model == CLOUDMODEL.CM_CUMULUS:
            # cloud = 0 -> clear view of sun
            # cloud = 1 -> very dark cloud blocking sun
            retval = self.get_fuzzy_cloud_value_for_location(latitude, longitude, cloud)  # Fuzzy cloud pattern evaluation
            f = 1 - (cloud * self.cloud_opacity)  # functions=1 -> clear view of sun, functions=0 -> very dark cloud blocking view of sun.
            # retval = self.get_binary_cloud_value_for_location(latitude, longitude, cloud)  # Binary cloud pattern evaluation
            # functions = 1.0 if cloud == 0 else (1.0 - self.cloud_opacity)

            sol_z = self.get_solar_zenith()
            ETRN = self.get_direct_normal_extra()
            ETR = ETRN * math.cos(sol_z)

            if sol_z > math.radians(90):  # When the sun is below the horizon, DNI must be zero.
                direct = 0
            else:
                direct = f * self.global_transmissivity * ETRN

            diffuse = self.get_solar_diffuse()
            cos_solar_zenith = max(math.cos(sol_z), 0.0)
            global_solar = max(direct * cos_solar_zenith + diffuse, 0.0)

            self.solar_cloud_direct = direct
            self.solar_cloud_diffuse = diffuse
            self.solar_cloud_global = global_solar
        else:
            direct = self.get_solar_direct()
            global_solar = self.get_solar_global()
            diffuse = self.get_solar_diffuse()

        return retval, direct, global_solar, diffuse

    # Define the placeholder methods (you need to implement these)
    def get_cloud_model(self):
        return CLOUDMODEL.CM_CUMULUS


    def get_solar_zenith(self):
        # Implement this function to get the solar zenith angle
        # You can replace this with the actual implementation
        pass

    def get_direct_normal_extra(self):
        # Implement this function to get the direct normal extraterrestrial radiation
        # You can replace this with the actual implementation
        pass

    def get_solar_direct(self):
        # Implement this function to get the solar direct radiation
        # You can replace this with the actual implementation
        pass

    def get_solar_global(self):
        # Implement this function to get the solar global radiation
        # You can replace this with the actual implementation
        pass

    def get_solar_diffuse(self):
        # Implement this function to get the solar diffuse radiation
        # You can replace this with the actual implementation
        pass

    def get_localtime(self, clock):
        # Implement this function to convert the clock time to local time
        # You can replace this with the actual implementation
        pass

    def get_binary_cloud_value_for_location(self, latitude, longitude):
        pixel_x = math.floor(gl_lerp(latitude, self.MIN_LAT, self.MIN_LAT_INDEX, self.MAX_LAT, self.MAX_LAT_INDEX))
        pixel_y = math.floor(gl_lerp(longitude, self.MIN_LON, self.MIN_LON_INDEX, self.MAX_LON, self.MAX_LON_INDEX))
        cloud = binary_cloud_pattern[pixel_x][pixel_y]
        # Debugging and validation
        # write_out_cloud_pattern('C');
        # write_out_cloud_pattern('B');
        # gl_output("%i,%functions,%functions,%i,%i,%i", prev_NTime, latitude, longitude, pixel_x, pixel_y,*cloud);
        # gl_output("%functions,%i,%functions,%i", latitude, pixel_x, longitude, pixel_y);
        # gl_output(" ");
        return 1, cloud

    def get_fuzzy_cloud_value_for_location(self, latitude, longitude):
        # write_out_cloud_pattern('F');
        pixel_x = math.floor(self.gl_lerp(latitude, self.MIN_LAT, self.MIN_LAT_INDEX, self.MAX_LAT, self.MAX_LAT_INDEX))
        pixel_y = math.floor(self.gl_lerp(longitude, self.MIN_LON, self.MIN_LON_INDEX, self.MAX_LON, self.MAX_LON_INDEX))
        value = fuzzy_cloud_pattern[0][pixel_x][pixel_y]
        cloud = fuzzy_cloud_pattern[0][pixel_x][pixel_y]
        # Debugging and validation
        # write_out_cloud_pattern('F');
        # write_out_cloud_pattern('B');
        # gl_output("%i,%functions,%functions,%i,%i,%functions", prev_NTime, latitude, longitude, pixel_x, pixel_y,*cloud); # fuzzy clouds
        # gl_output("%functions,%i,%functions,%i", latitude, pixel_x, longitude, pixel_y);
        # gl_output(" ");
        return 1, cloud

    def init_cloud_pattern(self):
        num_points = 0

        # find the solar objects and count them
        gr_obj = None
        items = gl_find_objects(FindType.FL_GROUP, "class=solar")
        for gr_obj in gl_find_next(items, 0):
            num_points += 1

        # resize the container to the max number of objects
        coord_list = np.empty((num_points, 2))

        # now populate the lat and lon, but only for those that have it
        num_points = 0
        for gr_obj in gl_find_next(items, 0):
            latitude = gr_obj.latitude
            longitude = gr_obj.longitude
            if not np.isnan(longitude) and not np.isnan(latitude):
                coord_list[num_points, 0] = latitude
                coord_list[num_points, 1] = longitude
                num_points += 1

        # finally resize to the number of solar objects that have lat and lon
        coord_list = coord_list[:num_points]

        num_tile_edge = self.calc_cloud_pattern_size(coord_list)
        cloud_pattern_size = num_tile_edge * CLOUD_TILE_SIZE + 1  # pattern must be 2^x + 1 square
        on_screen_size = (num_tile_edge - 2) * CLOUD_TILE_SIZE  # Off-screen area is one tile width around the perimeter of the on-screen area.

        # Build empty cloud pattern array
        cloud_pattern = np.full((cloud_pattern_size, cloud_pattern_size), EMPTY_VALUE)
        binary_cloud_pattern = np.full((cloud_pattern_size, cloud_pattern_size), EMPTY_VALUE)
        normalized_cloud_pattern = np.full((cloud_pattern_size, cloud_pattern_size), EMPTY_VALUE)

        for i in range(num_tile_edge):
            for j in range(num_tile_edge):
                # Building pattern as a series of tiles
                col_min = i * CLOUD_TILE_SIZE
                col_max = (i + 1) * CLOUD_TILE_SIZE
                row_min = j * CLOUD_TILE_SIZE
                row_max = (j + 1) * CLOUD_TILE_SIZE
                self.build_cloud_pattern(col_min, col_max, row_min, row_max)  # Min/Max x/y must always define a 2^x + 1 region of cloud_pattern
                # write_out_cloud_pattern('C')

    def update_cloud_pattern(self, delta_t):
        col_shifted_px = 0
        row_shifted_px = 0
        col_shift_request_px = 0
        row_shift_request_px = 0

        # Calculating pattern shift vector due to wind
        windspeed_tmy2 = self.get_wind_speed() * self.cloud_speed_factor
        wind_direct = self.get_wind_dir()

        # Using European Wind Atlas terrain roughness class and length to translate TMY2 windspeed at 10m to
        # cumulus cloud height, 1000m.
        # float roughness_class = 3;  # Assumed. Slightly rural to suburban value.
        # double roughness_length = exp(log(10.0/3.0)*(roughness_class - 3.91249));
        # double windspeed = windspeed_tmy2 * log(1000/roughness_length)/log(10/roughness_length);

        # C. W. Hansen, J. S. Stein, and A. Ellis,
        # "Simulation of One-Minute Power Output from Utility-Scale Photovoltaic Generation Systems," SAND2011-5529, 2011.
        # Shows distribution of wind speeds at cumulus cloud elevations based on weather balloon launches (pg. 18)
        # A cursory inspection of the TMY3 measured wind speeds shows this is roughly consistent with histogram
        # presented in the paper.
        #
        # As part of validation I found I was having to scale back the windspeed to roughly the same
        # speeds as the original source data. (Thus the "cloud_speed_factor" parameter.)
        # Removing windspeed adjustment and using source data as is.
        windspeed = windspeed_tmy2

        # Reformatting wind direction data
        wind_direct = wind_direct - 180
        wind_direct = -1 * (wind_direct - 90)
        if wind_direct <= -360:
            wind_direct = wind_direct + 360
        elif wind_direct >= 360:
            wind_direct = wind_direct - 360
        wind_direct = math.radians(wind_direct)

        time_step = delta_t  # Placeholder until we dig into the actual GLD synchronization process.

        col_shift_px = (windspeed * math.cos(wind_direct) * time_step) / PIXEL_EDGE_SIZE
        row_shift_px = (windspeed * math.sin(wind_direct) * time_step) / PIXEL_EDGE_SIZE

        col_shift_request_px = col_shift_request_px + col_shift_px
        row_shift_request_px = row_shift_request_px + row_shift_px

        # Accumulating wind shift vector so that small persistent winds still have an effect.
        col_shift = 0
        row_shift = 0
        if abs(col_shift_request_px - col_shifted_px) >= 1:
            col_shift = math.floor(col_shift_request_px - col_shifted_px)
            col_shifted_px = col_shifted_px + col_shift
        if abs(row_shift_request_px - row_shifted_px) >= 1:
            row_shift = math.floor(row_shift_request_px - row_shifted_px)
            row_shifted_px = row_shifted_px + row_shift

        row_boundary = abs(row_shift)
        col_boundary = abs(col_shift)

        col = 0
        row = 0

        if row_shift != 0 or col_shift != 0:
            if row_shift >= 0 and col_shift >= 0:  # Wind blows from SW to NE
                if col_shift > 0:
                    col = CLOUD_TILE_SIZE - col_boundary
                    # Checking to see if barely off-screen values are empty before shifting the pattern.
                    # If check is not done, may result in EMPTY_VALUES getting shifted on_screen.
                    for row in range(CLOUD_TILE_SIZE, CLOUD_TILE_SIZE + on_screen_size):
                        if cloud_pattern[row][col] == EMPTY_VALUE:
                            self.rebuild_cloud_pattern_edge('W')
                            break
                if row_shift > 0:
                    row = CLOUD_TILE_SIZE - row_boundary
                    for col in range(CLOUD_TILE_SIZE, CLOUD_TILE_SIZE + on_screen_size):
                        if cloud_pattern[row][col] == EMPTY_VALUE:
                            self.rebuild_cloud_pattern_edge('S')
                            break
                # Shifting pattern (after any edges have been rebuilt).
                for row in range(cloud_pattern_size - 1, -1, -1):
                    for col in range(cloud_pattern_size - 1, -1, -1):
                        if row + row_shift > cloud_pattern_size - 1:
                            cloud_pattern[row][col] = EMPTY_VALUE
                        elif col + col_shift > cloud_pattern_size - 1:
                            cloud_pattern[row][col] = EMPTY_VALUE
                        else:
                            cloud_pattern[row + row_shift][col + col_shift] = cloud_pattern[row][col]
                            cloud_pattern[row][col] = EMPTY_VALUE
            elif row_shift >= 0 and col_shift <= 0:  # Wind blows from SE to NW
                if col_shift < 0:
                    col = CLOUD_TILE_SIZE + on_screen_size + col_boundary
                    # Checking to see if barely off-screen values are empty before shifting the pattern.
                    # If check is not done, may result in EMPTY_VALUES getting shifted on_screen.
                    for row in range(CLOUD_TILE_SIZE, CLOUD_TILE_SIZE + on_screen_size):
                        if cloud_pattern[row][col] == EMPTY_VALUE:
                            self.rebuild_cloud_pattern_edge('E')
                            break
                if row_shift > 0:
                    row = CLOUD_TILE_SIZE - row_boundary
                    for col in range(CLOUD_TILE_SIZE, CLOUD_TILE_SIZE + on_screen_size):
                        if cloud_pattern[row][col] == EMPTY_VALUE:
                            self.rebuild_cloud_pattern_edge('S')
                            break
                # Shifting pattern (after any edges have been rebuilt).
                for row in range(cloud_pattern_size - 1, -1, -1):
                    for col in range(cloud_pattern_size):
                        if row + row_shift > cloud_pattern_size - 1:
                            cloud_pattern[row][col] = EMPTY_VALUE
                        elif col + col_shift < 0:
                            cloud_pattern[row][col] = EMPTY_VALUE
                        else:
                            cloud_pattern[row + row_shift][col + col_shift] = cloud_pattern[row][col]
                            cloud_pattern[row][col] = EMPTY_VALUE
            elif row_shift <= 0 and col_shift >= 0:  # Wind blows from NW to SE
                if col_shift > 0:
                    col = CLOUD_TILE_SIZE - col_boundary
                    # Checking to see if barely off-screen values are empty before shifting the pattern.
                    # If check is not done, may result in EMPTY_VALUES getting shifted on_screen.
                    for row in range(CLOUD_TILE_SIZE, CLOUD_TILE_SIZE + on_screen_size + 1):
                        if cloud_pattern[row][col] == EMPTY_VALUE:
                            self.rebuild_cloud_pattern_edge('W')
                            break
                if row_shift < 0:
                    row = CLOUD_TILE_SIZE + on_screen_size + row_boundary
                    for col in range(CLOUD_TILE_SIZE, CLOUD_TILE_SIZE + on_screen_size):
                        if cloud_pattern[row][col] == EMPTY_VALUE:
                            self.rebuild_cloud_pattern_edge('N')
                            break
                # Shifting pattern (after any edges have been rebuilt).
                for row in range(cloud_pattern_size):
                    for col in range(cloud_pattern_size - 1, -1, -1):
                        if row + row_shift < 0:
                            cloud_pattern[row][col] = EMPTY_VALUE
                        elif col + col_shift > cloud_pattern_size - 1:
                            cloud_pattern[row][col] = EMPTY_VALUE
                        else:
                            cloud_pattern[row + row_shift][col + col_shift] = cloud_pattern[row][col]
                            cloud_pattern[row][col] = EMPTY_VALUE
            elif row_shift <= 0 and col_shift <= 0:  # Wind blows from NE to SW
                if col_shift < 0:
                    col = CLOUD_TILE_SIZE + on_screen_size + col_boundary
                    # Checking to see if barely off-screen values are empty before shifting the pattern.
                    # If check is not done, may result in EMPTY_VALUES getting shifted on_screen.
                    for row in range(CLOUD_TILE_SIZE, CLOUD_TILE_SIZE + on_screen_size):
                        if cloud_pattern[row][col] == EMPTY_VALUE:
                            self.rebuild_cloud_pattern_edge('E')
                            break
                if row_shift < 0:
                    row = CLOUD_TILE_SIZE + on_screen_size + row_boundary
                    for col in range(CLOUD_TILE_SIZE, CLOUD_TILE_SIZE + on_screen_size):
                        if cloud_pattern[row][col] == EMPTY_VALUE:
                            self.rebuild_cloud_pattern_edge('N')
                            break
                # Shifting pattern (after any edges have been rebuilt).
                for row in range(cloud_pattern_size):
                    for col in range(cloud_pattern_size):
                        if row + row_shift < 0:
                            cloud_pattern[row][col] = EMPTY_VALUE
                        elif col + col_shift < 0:
                            cloud_pattern[row][col] = EMPTY_VALUE
                        else:
                            cloud_pattern[row + row_shift][col + col_shift] = cloud_pattern[row][col]
                            cloud_pattern[row][col] = EMPTY_VALUE
            else:
                # Shouldn't be able to get here.
                pass

            solar_zenith = self.get_solar_zenith()
            if solar_zenith < (110 * math.pi / 180):  # Only do these things if the sun is above (or slightly below) the horizon.
                # Fractal cloud pattern is preserved and shifted appropriately but since the sun is below the horizon
                # and the solar radiation on the surface is zero, we don't need to fully define the clouds.
                # Finding cloud outline shape
                cut_elevation = 0
                cut_elevation = self.convert_to_binary_cloud()
                # write_out_cloud_pattern('B')
                self.convert_to_fuzzy_cloud(cut_elevation, self.cloud_num_layers, self.cloud_alpha)
                # write_out_cloud_pattern('F')




    def convert_to_binary_cloud(self):
        # Convert fractal cloud pattern to binary value based on TMY2 opaque sky value.
        # Place-holder location.  Eventually needs to be driven by objects asking for updated
        # cloud values.  If the time since the last conversion is non-zero, this function needs
        # to run to generate the new binary value.
        cloud_value = self.get_opq_sky_cov()  # get_tot_sky_cov() or get_opq_sky_cov()

        # TDH:
        # Trying to counteract the fuzzification process by artificially boosting the coverage.
        # This is a bit of a hack. The best way to handle this is to include the fuzzification process
        # in the elevation cut adjustment. This way, the percentage of the sky covered by opaque clouds
        # is ensured after the fuzzification has taken place. I've tested this and it REALLY slows things
        # down (in an already slow function). For now, this is what I've chosen to do because it more
        # or less works.
        cloud_value = cloud_value * 2.0
        if cloud_value >= 1:
            cloud_value = 0.99

        search_tolerance = 0.005  # Defines how close is close enough when dialing in the binary cloud pattern.

        # TDH: trivially parallelizable
        cloud_pattern_max = cloud_pattern[CLOUD_TILE_SIZE][CLOUD_TILE_SIZE]
        cloud_pattern_min = cloud_pattern[CLOUD_TILE_SIZE][CLOUD_TILE_SIZE]

        # Finding max and min value
        for i in range(cloud_pattern_size):
            for j in range(cloud_pattern_size):
                if cloud_pattern[i][j] != EMPTY_VALUE:
                    if cloud_pattern[i][j] > cloud_pattern_max:
                        cloud_pattern_max = cloud_pattern[i][j]
                    if cloud_pattern[i][j] < cloud_pattern_min:
                        cloud_pattern_min = cloud_pattern[i][j]

        cloud_pattern_range = cloud_pattern_max - cloud_pattern_min
        cut_elevation = cloud_pattern_min
        running_count = 0
        measured_coverage = 0
        step_size = 0
        max_cut_elevation = cloud_pattern_max
        min_cut_elevation = cloud_pattern_min

        # Creating normalized cloud pattern
        normalized_cloud_pattern = np.zeros((cloud_pattern_size, cloud_pattern_size))
        for i in range(cloud_pattern_size):
            for j in range(cloud_pattern_size):
                if cloud_pattern[i][j] != EMPTY_VALUE:
                    normalized_cloud_pattern[i][j] = (cloud_pattern[i][j] - cloud_pattern_min) / cloud_pattern_range

        while True:
            cut_elevation += step_size
            running_count = 0
            for i in range(CLOUD_TILE_SIZE, CLOUD_TILE_SIZE + on_screen_size):
                for j in range(CLOUD_TILE_SIZE, CLOUD_TILE_SIZE + on_screen_size):
                    if (
                        normalized_cloud_pattern[i][j] != EMPTY_VALUE
                        and normalized_cloud_pattern[i][j] <= cut_elevation
                    ):
                        # Values less than cut elevation are clouds
                        running_count += 1

            measured_coverage = running_count / (on_screen_size * on_screen_size)  # Factor, range [0 1]

            # Calculating next cut elevation.
            if measured_coverage > (cloud_value + search_tolerance):
                max_cut_elevation = cut_elevation
                step_size = (max_cut_elevation - min_cut_elevation) / -2
            elif measured_coverage < (cloud_value - search_tolerance):
                min_cut_elevation = cut_elevation
                step_size = (max_cut_elevation - min_cut_elevation) / 2

            if measured_coverage >= (cloud_value - search_tolerance) and measured_coverage <= (
                cloud_value + search_tolerance
            ):
                break

        # Converting cloud_pattern to binary_cloud_pattern
        binary_cloud_pattern = np.zeros((cloud_pattern_size, cloud_pattern_size), dtype=int)
        for i in range(cloud_pattern_size):
            for j in range(cloud_pattern_size):
                if normalized_cloud_pattern[i][j] == EMPTY_VALUE:
                    binary_cloud_pattern[i][j] = EMPTY_VALUE
                elif normalized_cloud_pattern[i][j] <= cut_elevation:
                    binary_cloud_pattern[i][j] = 0  # Cloud
                elif normalized_cloud_pattern[i][j] > cut_elevation:
                    binary_cloud_pattern[i][j] = 1  # Blue sky

        return cut_elevation

    def convert_to_fuzzy_cloud(self, cut_elevation, num_fuzzy_layers, alpha):
        shade_step_size = 1.0 / alpha

        if cut_elevation == EMPTY_VALUE:  # Initialization call uses EMPTY_VALUE as the cut elevation.
            # TDH: trivially parallelizable
            # Resizing fuzzy cloud pattern
            fuzzy_cloud_pattern = [
                [[0] * cloud_pattern_size for _ in range(cloud_pattern_size)]
                for _ in range(num_fuzzy_layers)
            ]

        # Filling in fuzzy pattern with random values
        for i in range(num_fuzzy_layers):
            rand_upper = ((i + 1) / num_fuzzy_layers) * cut_elevation
            rand_lower = ((i + 1 - 1) / num_fuzzy_layers) * cut_elevation
            for j in range(cloud_pattern_size):
                for kk in range(cloud_pattern_size):
                    binary = binary_cloud_pattern[j][kk]
                    normalized = normalized_cloud_pattern[j][kk]
                    fuzzy = fuzzy_cloud_pattern[0][j][kk]
                    if (
                        binary_cloud_pattern[j][kk] == 0.0
                        and normalized_cloud_pattern[j][kk] != EMPTY_VALUE
                        and fuzzy_cloud_pattern[0][j][kk] != EMPTY_VALUE
                    ):  # Areas with 0 in the binary pattern are cloudy
                        if normalized_cloud_pattern[j][kk] <= cut_elevation - (
                            (i + 1) * shade_step_size
                        ):  # only values below the cut elevation accumulate
                            fuzzy_cloud_pattern[0][j][kk] = (
                                random.uniform(rand_lower, rand_upper)
                                + fuzzy_cloud_pattern[0][j][kk]
                            )
                            fuzzy = fuzzy_cloud_pattern[0][j][kk]
                    else:  # EMPTY_VALUES get coerced into 0.
                        fuzzy_cloud_pattern[0][j][kk] = 0

        # Normalizing fuzzy pattern
        max_value = fuzzy_cloud_pattern[0][0][0]
        min_value = fuzzy_cloud_pattern[0][0][0]
        for j in range(cloud_pattern_size):
            for k in range(cloud_pattern_size):
                value = fuzzy_cloud_pattern[0][j][k]
                if value > max_value:
                    max_value = value
                if value < min_value:
                    min_value = value

        range_val = max_value - min_value
        if range_val != 0:
            for j in range(cloud_pattern_size):
                for k in range(cloud_pattern_size):
                    value = (fuzzy_cloud_pattern[0][j][k] - min_value) / range_val
                    fuzzy_cloud_pattern[0][j][k] = value
        else:
            # Do we need to do anything if the pattern is uniform?
            pass

        # Put EMPTY_VALUEs back in before calling it good.
        for j in range(cloud_pattern_size):
            for k in range(cloud_pattern_size):
                if cloud_pattern[j][k] == EMPTY_VALUE:
                    fuzzy_cloud_pattern[0][j][k] = EMPTY_VALUE

    # Assuming you have defined required constants and structures
    # For example:
    # CLOUD_TILE_SIZE = 64
    # EMPTY_VALUE = -999  # Replace with your actual EMPTY_VALUE
    # cloud_pattern_size = 128  # Replace with your actual size
    # on_screen_size = 64  # Replace with your actual size

    def rebuild_cloud_pattern_edge(self, edge_needing_rebuilt):
        col_min = 0
        row_min = 0
        i = 0

        if edge_needing_rebuilt == 'W':
            col_min = 0
            row_min = 0
            self.erase_off_screen_pattern('W')
            for i in range(1 + on_screen_size // CLOUD_TILE_SIZE + 1):
                self.build_cloud_pattern(col_min, col_min + CLOUD_TILE_SIZE, row_min, row_min + CLOUD_TILE_SIZE)
                row_min = row_min + CLOUD_TILE_SIZE
            self.trim_pattern_edge('W')
        elif edge_needing_rebuilt == 'E':
            col_min = CLOUD_TILE_SIZE + on_screen_size - 1
            row_min = 0
            self.erase_off_screen_pattern('E')
            for i in range(1 + on_screen_size // CLOUD_TILE_SIZE + 1):
                self.build_cloud_pattern(col_min, col_min + CLOUD_TILE_SIZE, row_min, row_min + CLOUD_TILE_SIZE)
                row_min = row_min + CLOUD_TILE_SIZE
            self.trim_pattern_edge('E')
        elif edge_needing_rebuilt == 'N':
            col_min = 0
            row_min = CLOUD_TILE_SIZE + on_screen_size - 1
            self.erase_off_screen_pattern('N')
            for i in range(1 + on_screen_size // CLOUD_TILE_SIZE + 1):
                self.build_cloud_pattern(col_min, col_min + CLOUD_TILE_SIZE, row_min, row_min + CLOUD_TILE_SIZE)
                col_min = col_min + CLOUD_TILE_SIZE
            self.trim_pattern_edge('N')
        elif edge_needing_rebuilt == 'S':
            col_min = 0
            row_min = 0
            self.erase_off_screen_pattern('S')
            for i in range(1 + on_screen_size // CLOUD_TILE_SIZE + 1):
                self.build_cloud_pattern(col_min, col_min + CLOUD_TILE_SIZE, row_min, row_min + CLOUD_TILE_SIZE)
                col_min = col_min + CLOUD_TILE_SIZE
            self.trim_pattern_edge('S')
        else:
            # Shouldn't be able to get here.
            pass

    def trim_pattern_edge(self, rebuilt_edge):
        min_edge = 0
        min_edge_1 = 0
        min_edge_2 = min_edge_1
        min_edge_3 = min_edge_1
        max_edge = 0
        max_edge_1 = CLOUD_TILE_SIZE + on_screen_size + CLOUD_TILE_SIZE
        max_edge_2 = max_edge_1
        max_edge_3 = max_edge_1
        i = 0
        j = 0

        if rebuilt_edge == 'W' or rebuilt_edge == 'E':
            # Checking for boundary at southern edge of pattern.
            for i in range(CLOUD_TILE_SIZE):
                if cloud_pattern[i][10] != EMPTY_VALUE:
                    min_edge_1 = i
                    break
            for i in range(CLOUD_TILE_SIZE):
                if cloud_pattern[i][CLOUD_TILE_SIZE + 10] != EMPTY_VALUE:
                    min_edge_2 = i
                    break
            for i in range(CLOUD_TILE_SIZE):
                if cloud_pattern[i][CLOUD_TILE_SIZE + on_screen_size + 10] != EMPTY_VALUE:
                    min_edge_3 = i
                    break
            min_edge = max(min_edge_1, min_edge_2, min_edge_3)

            # Checking for boundary at northern edge of pattern
            for i in range(CLOUD_TILE_SIZE + on_screen_size, cloud_pattern_size):
                if cloud_pattern[i][10] == EMPTY_VALUE:
                    max_edge_1 = i
                    break
            for i in range(CLOUD_TILE_SIZE + on_screen_size, cloud_pattern_size):
                if cloud_pattern[i][CLOUD_TILE_SIZE + 10] == EMPTY_VALUE:
                    max_edge_2 = i
                    break
            for i in range(CLOUD_TILE_SIZE + on_screen_size, cloud_pattern_size):
                if cloud_pattern[i][CLOUD_TILE_SIZE + on_screen_size + 10] == EMPTY_VALUE:
                    max_edge_3 = i
                    break
            max_edge = min(max_edge_1, max_edge_2, max_edge_3)

            # Trimming pattern
            for j in range(cloud_pattern_size):
                for i in range(min_edge):
                    cloud_pattern[i][j] = EMPTY_VALUE
                for i in range(max_edge, cloud_pattern_size):
                    cloud_pattern[i][j] = EMPTY_VALUE
        elif rebuilt_edge == 'N' or rebuilt_edge == 'S':
            # Checking for boundary at western edge of pattern.
            for j in range(CLOUD_TILE_SIZE):
                if cloud_pattern[10][j] != EMPTY_VALUE:
                    min_edge_1 = j
                    break
            for j in range(CLOUD_TILE_SIZE):
                if cloud_pattern[CLOUD_TILE_SIZE + 10][j] != EMPTY_VALUE:
                    min_edge_2 = j
                    break
            for j in range(CLOUD_TILE_SIZE):
                if cloud_pattern[CLOUD_TILE_SIZE + on_screen_size + 10][j] != EMPTY_VALUE:
                    min_edge_3 = j
                    break
            min_edge = max(min_edge_1, min_edge_2, min_edge_3)

            # Checking for boundary at eastern edge of pattern
            for j in range(CLOUD_TILE_SIZE + on_screen_size, cloud_pattern_size):
                if cloud_pattern[10][j] == EMPTY_VALUE:
                    max_edge_1 = j
                    break
            for j in range(CLOUD_TILE_SIZE + on_screen_size, cloud_pattern_size):
                if cloud_pattern[CLOUD_TILE_SIZE + 10][j] == EMPTY_VALUE:
                    max_edge_2 = j
                    break
            for j in range(CLOUD_TILE_SIZE + on_screen_size, cloud_pattern_size):
                if cloud_pattern[CLOUD_TILE_SIZE + on_screen_size + 10][j] == EMPTY_VALUE:
                    max_edge_3 = j
                    break
            max_edge = min(max_edge_1, max_edge_2, max_edge_3)

            # Trimming pattern
            for i in range(cloud_pattern_size):
                for j in range(min_edge):
                    cloud_pattern[i][j] = EMPTY_VALUE
                for j in range(max_edge, cloud_pattern_size):
                    cloud_pattern[i][j] = EMPTY_VALUE
        else:
            # Shouldn't be able to get here.
            pass

    # Assuming you have defined required constants and structures
    # For example:
    # CLOUD_TILE_SIZE = 64
    # EMPTY_VALUE = -999  # Replace with your actual EMPTY_VALUE
    # cloud_pattern_size = 128  # Replace with your actual size
    # prev_NTime = 0  # Replace with your actual value

    def erase_off_screen_pattern(self, edge_to_erase):
        col_min = 0
        row_min = 0

        if edge_to_erase == 'W':
            col_min = 0
            row_min = 0
            for i in range(cloud_pattern_size):  # rows
                for j in range(CLOUD_TILE_SIZE - 1):  # cols
                    cloud_pattern[i][j] = EMPTY_VALUE
        elif edge_to_erase == 'E':
            col_min = 0
            row_min = 0
            for i in range(cloud_pattern_size):  # rows
                for j in range(cloud_pattern_size - CLOUD_TILE_SIZE + 1, cloud_pattern_size):  # cols
                    cloud_pattern[i][j] = EMPTY_VALUE
        elif edge_to_erase == 'N':
            col_min = 0
            row_min = 0
            for i in range(cloud_pattern_size - CLOUD_TILE_SIZE + 1, cloud_pattern_size):  # rows
                for j in range(cloud_pattern_size):  # cols
                    cloud_pattern[i][j] = EMPTY_VALUE
        elif edge_to_erase == 'S':
            col_min = 0
            row_min = 0
            for i in range(CLOUD_TILE_SIZE - 1):  # rows
                for j in range(cloud_pattern_size):  # cols
                    cloud_pattern[i][j] = EMPTY_VALUE
        # write_out_cloud_pattern('C')

    def write_out_pattern_shift(self, row_shift, col_shift):
        with open("pattern_shift.csv", "a") as out_file:
            out_file.write(f"{self.prev_NTime},{row_shift},{col_shift}\n")

    def write_out_cloud_pattern(self, pattern):
        file_string = f"cloud_pattern_{self.prev_NTime:010d}.csv"

        with open(file_string, "w") as out_file:
            if pattern == 'C':
                for i in range(cloud_pattern_size):
                    for j in range(cloud_pattern_size):
                        if j == (cloud_pattern_size - 1):
                            out_file.write(f"{cloud_pattern[i][j]}\n")
                        else:
                            out_file.write(f"{cloud_pattern[i][j]},")
            elif pattern == 'B':
                for i in range(cloud_pattern_size):
                    for j in range(cloud_pattern_size):
                        if j == (cloud_pattern_size - 1):
                            out_file.write(f"{binary_cloud_pattern[i][j]}\n")
                        else:
                            out_file.write(f"{binary_cloud_pattern[i][j]},")
            elif pattern == 'F':
                for i in range(cloud_pattern_size):
                    for j in range(cloud_pattern_size):
                        if j == (cloud_pattern_size - 1):
                            out_file.write(f"{fuzzy_cloud_pattern[0][i][j]}\n")
                        else:
                            out_file.write(f"{fuzzy_cloud_pattern[0][i][j]},")

    # Assuming you have defined required constants and structures
    # For example:
    # CLOUD_TILE_SIZE = 64
    # EMPTY_VALUE = -999  # Replace with your actual EMPTY_VALUE
    # cloud_pattern_size = 128  # Replace with your actual size
    # RNGSTATE = random.Random()  # Replace with your random number generator state
    # KM_PER_DEG = 111.32
    # PIXEL_EDGE_SIZE = 1  # Replace with your actual pixel edge size
    # MIN_LAT_INDEX = 0  # Replace with your actual values
    # MAX_LAT_INDEX = 0  # Replace with your actual values
    # MIN_LON_INDEX = 0  # Replace with your actual values
    # MAX_LON_INDEX = 0  # Replace with your actual values
    # MIN_LAT = 0.0  # Replace with your actual values
    # MAX_LAT = 0.0  # Replace with your actual values
    # MIN_LON = 0.0  # Replace with your actual values
    # MAX_LON = 0.0  # Replace with your actual values
    # location_list = []  # Replace with your actual location data


    def build_cloud_pattern(self, col_min, col_max, row_min, row_max):
        SIGMA = 5
        step = col_max - col_min
        half_step = step // 2
        max_num_recursions = int(math.log((col_max - col_min), 2))
        col_start = col_min
        row_start = row_min
        stdev = SIGMA * SIGMA

        # Seed corner values that are empty
        if cloud_pattern[row_start][col_start] < EMPTY_VALUE * 0.98:
            cloud_pattern[row_start][col_start] = self.gl_random_normal(0, stdev)
        if cloud_pattern[row_start + step][col_start] < EMPTY_VALUE * 0.98:
            cloud_pattern[row_start + step][col_start] = self.gl_random_normal(0, stdev)
        if cloud_pattern[row_start][col_start + step] < EMPTY_VALUE * 0.98:
            cloud_pattern[row_start][col_start + step] = self.gl_random_normal(0, stdev)
        if cloud_pattern[row_start + step][col_start + step] < EMPTY_VALUE * 0.98:
            cloud_pattern[row_start + step][col_start + step] = self.gl_random_normal(0, stdev)

        # Filling in the rest of the pattern
        D = 0
        delta = 0
        for k in range(max_num_recursions):
            col_start = col_min
            row_start = row_min
            if k <= 3:
                D = 1.9
            else:
                D = 1.33

            if k == 0:
                delta = SIGMA * pow(0.5, (0.5 * (2 - D)))
            else:
                delta = delta * pow(0.5, (0.5 * (2 - D)))

            stdev = delta * delta
            end = int(pow(2, k))
            for i in range(end):
                for j in range(end):
                    c1 = cloud_pattern[row_start][col_start]
                    c2 = cloud_pattern[row_start][col_start + step]
                    c3 = cloud_pattern[row_start + step][col_start]
                    c4 = cloud_pattern[row_start + step][col_start + step]
                    x = (c1 + c2 + c3 + c4) / 4 + self.gl_random_normal(0, stdev)
                    e_a = (x + c1 + c3) / 3 + self.gl_random_normal(0, stdev)
                    e_b = (x + c1 + c2) / 3 + self.gl_random_normal(0, stdev)
                    e_c = (x + c2 + c4) / 3 + self.gl_random_normal(0, stdev)
                    e_d = (x + c3 + c4) / 3 + self.gl_random_normal(0, stdev)

                    if cloud_pattern[row_start + half_step][col_start + half_step] < EMPTY_VALUE * 0.98:
                        cloud_pattern[row_start + half_step][col_start + half_step] = x
                    if cloud_pattern[row_start + half_step][col_start] < EMPTY_VALUE * 0.98:
                        cloud_pattern[row_start + half_step][col_start] = e_a
                    if cloud_pattern[row_start][col_start + half_step] < EMPTY_VALUE * 0.98:
                        cloud_pattern[row_start][col_start + half_step] = e_b
                    if cloud_pattern[row_start + half_step][col_start + step] < EMPTY_VALUE * 0.98:
                        cloud_pattern[row_start + half_step][col_start + step] = e_c
                    if cloud_pattern[row_start + step][col_start + half_step] < EMPTY_VALUE * 0.98:
                        cloud_pattern[row_start + step][col_start + half_step] = e_d
                    row_start = row_start + step
                row_start = row_min
                col_start = col_start + step
            step = half_step
            half_step = half_step // 2

    def calc_cloud_pattern_size(self, location_list):
        lat_max = location_list[0][0]
        lat_min = location_list[0][0]
        long_max = location_list[0][1]
        long_min = location_list[0][1]
        lat_delta = 0
        long_delta = 0
        degree_range_lat = 0
        degree_range_lon = 0
        num_tile_edge = 1  # Minimum size (1 on-screen tile with 1 off-screen on all sides; 9 tiles total).

        if len(location_list) > 1:
            for i in range(1, len(location_list)):
                lat_max = max(lat_max, location_list[i][0])
                lat_min = min(lat_min, location_list[i][0])
                long_max = max(long_max, location_list[i][1])
                long_min = min(long_min, location_list[i][1])

            lat_delta = abs(lat_max - lat_min)
            long_delta = abs(long_max - long_min)
            x_size_km = lat_delta * KM_PER_DEG  # 111.32 km/degree latitude
            y_size_km = long_delta * math.cos(math.radians(lat_min)) * KM_PER_DEG  # Assumes the lat_delta is small enough that the polar convergence of the longitudinal lines is insignificant.
            max_dim_km = max(x_size_km, y_size_km)
            num_tile_edge = math.ceil(((max_dim_km * 1000.0 / PIXEL_EDGE_SIZE) / CLOUD_TILE_SIZE))

        MIN_LAT_INDEX = CLOUD_TILE_SIZE  # because there is always a buffer
        MAX_LAT_INDEX = CLOUD_TILE_SIZE + num_tile_edge * CLOUD_TILE_SIZE  # buffer plus the number of pixels
        MIN_LON_INDEX = MIN_LAT_INDEX  # square
        MAX_LON_INDEX = MAX_LAT_INDEX  # still square

        degree_range_lat = ((num_tile_edge * CLOUD_TILE_SIZE * PIXEL_EDGE_SIZE) / 1000.0 / KM_PER_DEG)
        degree_range_lon = ((num_tile_edge * CLOUD_TILE_SIZE * PIXEL_EDGE_SIZE) / 1000.0 / KM_PER_DEG / math.cos(math.radians(lat_min)))

        MIN_LAT = lat_min - (degree_range_lat - lat_delta) / 2.0
        MAX_LAT = MIN_LAT + degree_range_lat
        MIN_LON = long_min - (degree_range_lon - long_delta) / 2.0
        MAX_LON = MIN_LON + degree_range_lon

        return num_tile_edge + 2  # Adding extra tiles for the off-screen buffer around the perimeter

    def update_forecasts(self, t0):
        Nh = 72  # number of hours in forecast
        dt = 3600  # number of seconds in forecast interval

        # The rest of the code inside the method
        # ...

    def presync(self, t0):
        csv_rv = 0
        tmy_rv = 0
        cloud_rv = 0

        # Establish the current time
        update_time = t0

        if t0 > 0 and self.tmy is None and self.reader_type != "RT_CSV":
            # Calculate solar radiation
            now = datetime.fromtimestamp(t0)
            longitude = self.longitude

            # Calculate solar time
            sol_time = self.solar_time(now.hour + now.minute / 60.0 + now.second / 3600.0 + (now.dst() - 1), now.timetuple().tm_yday, math.radians(self.tz_meridian), math.radians(longitude))

            # Calculate other solar parameters
            # ...

        if t0 > 0 and self.reader_type == "RT_CSV":
            now = datetime.fromtimestamp(t0)
            cr = self.reader
            csv_rv = cr.get_data(t0, self.temperature, self.humidity, self.solar_direct, self.solar_diffuse, self.solar_global, self.global_horizontal_extra, self.wind_speed, self.wind_dir, self.opq_sky_cov, self.tot_sky_cov, self.rainfall, self.snowdepth, self.pressure)

            # Calculate solar radiation
            # ...

        if t0 > 0 and self.tmy is not None:
            ts = datetime.fromtimestamp(t0)
            localres = 1  # Replace with your logic to resolve localtime
            hoy = 0
            now = 0
            hoy0 = 0
            hoy1 = 0
            hoy2 = 0

            if localres == 0:
                raise Exception("climate::sync -- unable to resolve localtime!")

            doy = self.day_of_yr(ts.month, ts.day)
            hoy = (doy - 1) * 24 + ts.hour

            # Rest of the code for interpolation
            # ...

            # Update forecasts
            self.update_forecasts(t0)

            tmy_rv = -(t0 + (3600 * 1000000 - t0 % (3600 * 1000000)))  # Negative means soft event

        if self.cloud_model == "CM_CUMULUS":
            if self.prev_NTime != t0:
                p = self.pressure * 0.1  # Convert to kPa
                Z = self.solar_zenith
                M = 0.02857 * math.sqrt((1224.0 * math.cos(Z) * math.cos(Z)) + 1.0)
                u = 4.5
                aw = 0.077 * math.pow(u / M, 0.3)
                Pa = self.cloud_aerosol_transmissivity
                PRPA = 1.041 - (0.15 * math.sqrt(((p * 0.00949) + 0.051) / M))
                self.global_transmissivity = max(0.0, (PRPA - aw) * Pa)
                self.update_cloud_pattern(t0 - self.prev_NTime)
                self.prev_NTime = t0

            cloud_rv = t0 + 60

        if t0 <= 0:
            return "TS_NEVER"
        elif self.cloud_model == "CM_NONE":
            if self.reader_type == "RT_CSV":
                return cloud_rv if cloud_rv <= abs(csv_rv) else csv_rv
            elif self.tmy is not None:
                return cloud_rv if cloud_rv <= abs(tmy_rv) else tmy_rv
            else:
                return "TS_NEVER"
        else:
            if self.reader_type == "RT_CSV":
                return cloud_rv if cloud_rv <= abs(csv_rv) else csv_rv
            else:
                return cloud_rv if cloud_rv <= abs(tmy_rv) else tmy_rv
