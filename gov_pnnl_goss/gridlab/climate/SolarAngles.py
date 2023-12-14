import math

HR_PER_RADIAN = 12.0 / math.pi
PI_OVER_180 = math.pi / 180
raddeg = math.pi / 180
degrad = 180 / math.pi
COS85DEG = 0.08715574274765817355806427083747

days_thru_month = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]  # Ignores leap years


# Cumulative number of days prior to beginning of month - SOLPOS constants
month_days = [
    [0, 0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334],
    [0, 0, 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335]
]

# Perez tilt model coefficients
perez_tilt_coeff_F1 = [
    [-0.008, 0.130, 0.330, 0.568, 0.873, 1.132, 1.060, 0.678],
    [0.588, 0.683, 0.487, 0.187, -0.392, -1.237, -1.600, -0.327],
    [-0.062, -0.151, -0.221, -0.295, -0.362, -0.412, -0.359, -0.250]
]

perez_tilt_coeff_F2 = [
    [-0.060, -0.019, 0.055, 0.109, 0.226, 0.288, 0.264, 0.156],
    [0.072, 0.066, -0.064, -0.152, -0.462, -0.823, -1.127, -1.377],
    [-0.022, -0.029, -0.026, -0.014, 0.001, 0.056, 0.131, 0.251]
]

# Boundaries for Perez model "discrete sky clearness" categories
perez_clearness_limits = [1.0, 1.065, 1.230, 1.500, 1.950, 2.800, 4.500, 6.200]


class SOLPOS_TRIGDATA:
    def __init__(self):
        # Used to pass calculated values locally
        self.cd = 0.0  # Cosine of the declination
        self.ch = 0.0  # Cosine of the hour angle
        self.cl = 0.0  # Cosine of the latitude
        self.sd = 0.0  # Sine of the declination
        self.sl = 0.0  # Sine of the latitude


class SOLPOS_POSDATA:
    def __init__(self):
        # ALPHABETICAL LIST OF COMMON VARIABLES
        # Each comment begins with a 1-column letter code:
        # I: INPUT variable
        # O: OUTPUT variable
        # T: TRANSITIONAL variable used in the algorithm,
        # of interest only to the solar radiation
        # modelers, and available to you because you
        # may be one of them.
        # The FUNCTION column indicates which sub-function
        # within solpos must be switched on using the
        # "function" parameter to calculate the desired
        # output variable. All function codes are
        # defined in the solpos.h file. The default
        # S_ALL switch calculates all output variables.
        # Multiple functions may be or'd to create a
        # composite function switch. For example,
        # (S_TST | S_SBCF). Specifying only the functions
        # for required output variables may allow solpos
        # to execute more quickly.
        # The S_DOY mask works as a toggle between the
        # input date represented as a day number (daynum)
        # or as month and day. To set the switch (to
        # use daynum input), the function is or'd; to
        # clear the switch (to use month and day input),
        # the function is inverted and "and'd".
        # Whichever date form is used, S_solpos will
        # calculate and return the variable(s) of the
        # other form.

        # Common Variables
        self.day = 0        # I/O: S_DOY      Day of month (May 27 = 27, etc.)
        self.daynum = 0     # I/O: S_DOY      Day number (day of year; Feb 1 = 32 )
        self.function = 0   # I:              Switch to choose functions for desired
                            #                 output.
        self.hour = 12      # I:              Hour of day, 0 - 23, DEFAULT = 12
        self.interval = 0   # I:              Interval of a measurement period in
                            #                 seconds.  Forces solpos to use the
                            #                 time and date from the interval
                            #                 midpoint. The INPUT time (hour,
                            #                 minute, and second) is assumed to
                            #                 be the END of the measurement
                            #                 interval.
        self.minute = 0     # I:              Minute of hour, 0 - 59, DEFAULT = 0
        self.month = 0      # I/O: S_DOY      Month number (Jan = 1, Feb = 2, etc.)
                            #                 solpos will CALCULATE this by default,
                            #                 or will optionally require it as input
                            #                 depending on the setting of the S_DOY
                            #                 function switch.
        self.second = 0     # I:              Second of minute, 0 - 59, DEFAULT = 0
        self.year = 0       # I:              4-digit year (2-digit year is NOT allowed)

        # Double Variables
        self.amass = 0.0          # O:  S_AMASS    Relative optical airmass
        self.ampress = 0.0        # O:  S_AMASS    Pressure-corrected airmass
        self.aspect = 180.0       # I:             Azimuth of panel surface (direction it
                                  #                 faces) N=0, E=90, S=180, W=270,
                                  #                 DEFAULT = 180
        self.azim = 0.0           # O:  S_SOLAZM   Solar azimuth angle:  N=0, E=90, S=180,
                                  #                 W=270
        self.cosinc = 0.0         # O:  S_TILT     Cosine of solar incidence angle on
                                  #                 panel
        self.coszen = 0.0         # O:  S_REFRAC   Cosine of refraction corrected solar
                                  #                 zenith angle
        self.dayang = 0.0         # T:  S_GEOM     Day angle (daynum*360/year-length)
                                  #                 degrees
        self.declin = 0.0         # T:  S_GEOM     Declination--zenith angle of solar noon
                                  #                 at equator, degrees NORTH
        self.eclong = 0.0         # T:  S_GEOM     Ecliptic longitude, degrees
        self.ecobli = 0.0         # T:  S_GEOM     Obliquity of ecliptic
        self.ectime = 0.0         # T:  S_GEOM     Time of ecliptic calculations
        self.elevetr = 0.0        # O:  S_ZENETR   Solar elevation, no atmospheric
                                  #                 correction (= ETR)
        self.elevref = 0.0        # O:  S_REFRAC   Solar elevation angle,
                                  #                 deg. from horizon, refracted
        self.eqntim = 0.0         # T:  S_TST      Equation of time (TST - LMT), minutes
        self.erv = 0.0            # T:  S_GEOM     Earth radius vector
                                  #                 (multiplied to solar constant)
        self.etr = 0.0            # O:  S_ETR      Extraterrestrial (top-of-atmosphere)
                                  #                 W/sq m global horizontal solar
                                  #                 irradiance
        self.etrn = 0.0           # O:  S_ETR      Extraterrestrial (top-of-atmosphere)
                                  #                 W/sq m direct normal solar
                                  #                 irradiance
        self.etrtilt = 0.0        # O:  S_TILT     Extraterrestrial (top-of-atmosphere)
                                  #                 W/sq m global irradiance on a tilted
                                  #                 surface
        self.gmst = 0.0           # T:  S_GEOM     Greenwich mean sidereal time, hours
        self.hrang = 0.0          # T:  S_GEOM     Hour angle--hour of sun from solar noon,
                                  #                 degrees WEST
        self.julday = 0.0         # T:  S_GEOM     Julian Day of 1 JAN 2000 minus
                                  #                 2,400,000 days (in order to regain
                                  #                 single precision)
        self.latitude = 0.0       # I:             Latitude, degrees north (south negative)
        self.longitude = 0.0      # I:             Longitude, degrees east (west negative)
        self.lmst = 0.0           # T:  S_GEOM     Local mean sidereal time, degrees
        self.mnanom = 0.0         # T:  S_GEOM     Mean anomaly, degrees
        self.mnlong = 0.0         # T:  S_GEOM     Mean longitude, degrees
        self.rascen = 0.0         # T:  S_GEOM     Right ascension, degrees
        self.press = 0.0          # I:             Surface pressure, millibars, used for
                                  #                 refraction correction and ampress
        self.prime = 0.0          # O:  S_PRIME    Factor that normalizes Kt, Kn, etc.
        self.sbcf = 0.0           # O:  S_SBCF     Shadow-band correction factor
        self.sbwid = 0.0          # I:             Shadow-band width (cm)
        self.sbrad = 0.0          # I:             Shadow-band radius (cm)
        self.sbsky = 0.0          # I:             Shadow-band sky factor
        self.solcon = 1367.0      # I:             Solar constant (NREL uses 1367 W/sq m)
        self.ssha = 0.0           # T:  S_SRHA     Sunset(/rise) hour angle, degrees
        self.sretr = 0.0          # O:  S_SRSS     Sunrise time, minutes from midnight,
                                  #                 local, WITHOUT refraction
        self.ssetr = 0.0          # O:  S_SRSS     Sunset time, minutes from midnight,
                                  #                 local, WITHOUT refraction
        self.temp = 0.0           # I:             Ambient dry-bulb temperature, degrees C,
                                  #                 used for refraction correction
        self.tilt = 0.0           # I:             Degrees tilt from horizontal of panel
        self.timezone = 0.0       # I:             Time zone, east (west negative).
                                  #                 USA:  Mountain = -7, Central = -6, etc.
        self.tst = 0.0            # T:  S_TST      True solar time, minutes from midnight
        self.tstfix = 0.0         # T:  S_TST      True solar time - local standard time
        self.unprime = 0.0        # O:  S_PRIME    Factor that denormalizes Kt', Kn', etc.
        self.utime = 0.0          # T:  S_GEOM     Universal (Greenwich) standard time
        self.zenetr = 0.0         # T:  S_ZENETR   Solar zenith angle, no atmospheric
                                  #                 correction (= ETR)
        self.zenref = 0.0         # O:  S_REFRAC   Solar zenith angle, deg. from zenith,
                                  #                 refracted
        # Added Variables - Perez Model
        self.diff_horz = 0.0      # Diffuse horizontal radiation for Perez tilt model calculations
        self.dir_norm = 0.0       # Direct normal radiation for Perez tilt model calculations
        self.extra_irrad = 0.0    # Extraterrestrial direct normal irradiance
        self.perez_horz = 0.0     # Horizontal scalar from Perez diffuse model
        self.perez_skyclear_idx = 0  # Sky clearness index from Perez tilt model
        self.perez_skyclear = 0.0  # Sky clearness epsilon value from Perez tilt model
        self.perez_brightness = 0.0  # Sky brightness value from Perez tilt model
        self.perez_F1 = 0.0       # F1 coefficient calculation from Perez tilt model
        self.perez_F2 = 0.0       # F2 coefficient calculation from Perez tilt model


class SolarAngles:
    def __init__(self):
        pass

    @staticmethod
    def solar_time(std_time, day_of_yr, std_meridian, longitude):
        return std_time + SolarAngles.eq_time(day_of_yr) + (longitude - std_meridian) * (180.0 / math.pi) / 15.0

    @staticmethod
    def local_time(sol_time, day_of_yr, std_meridian, longitude):
        """
        Compute local standard (not daylight savings) time from apparent solar time and location.

        :param sol_time: Local solar time (decimal hours, e.g., 7:30 is 7.5)
        :param day_of_yr: Day of year from Jan 1
        :param std_meridian: Standard meridian (longitude) of local time zone
                            (radians, e.g., Pacific timezone is 120 times pi/180)
        :param longitude: Local longitude (radians east)
        :return: Local solar time in decimal hours
        """
        # std_meridian and longitude swapped to account for negative west convention (see solar_time above)
        # Unchecked since nothing uses local_time
        return sol_time - SolarAngles.eq_time(day_of_yr) - (longitude - std_meridian) * (180.0 / math.pi) / 15.0

    @staticmethod
    def eq_time(day_of_year):
        rad = (2.0 * math.pi * day_of_year) / 365.0
        return (
            (0.5501 * math.cos(rad) - 3.0195 * math.cos(2 * rad) - 0.0771 * math.cos(3 * rad)
             - 7.3403 * math.sin(rad) - 9.4583 * math.sin(2 * rad) - 0.3284 * math.sin(3 * rad)) / 60.0
        )

    @staticmethod
    def declination(day_of_year):
        """
        Compute the solar declination angle (radians).

        :param day_of_year: Day of year from Jan 1.
        :return: Declination angle in radians.
        """
        return 0.409280 * math.sin(2.0 * math.pi * (284 + day_of_year) / 365)

    @staticmethod
    def cos_incident(latitude, slope, az, sol_time, day_of_yr):
        """
        Compute the cosine of the angle of incidence of solar beam radiation on a surface.
                 !!! Note that this function is ignorant of the presence !!!
                 !!! of the horizon.                                     !!!
        SOURCE:  Duffie & Beckman.

        :param latitude: Latitude (radians north)
        :param slope: Slope of the surface relative to horizontal (radians)
        :param az: Azimuth angle of the surface relative to South (E+, W-) (radians)
        :param sol_time: Solar time (decimal hours)
        :param day_of_yr: Day of year from Jan 1
        :return: Cosine of the angle of incidence (angle between solar beam and surface normal)
        """
        # Calculate the solar declination angle (radians)
        declination = SolarAngles.declination(day_of_yr)

        # Calculate the hour angle (radians)
        hour_angle = (sol_time - 12.0) * (math.pi / 12.0)

        # Calculate the solar zenith angle (radians)
        zenith_angle = math.acos(math.sin(latitude) * math.sin(declination) +
                                 math.cos(latitude) * math.cos(declination) * math.cos(hour_angle))

        # Calculate the cosine of the angle of incidence
        cos_incident = math.sin(declination) * math.sin(slope) * math.cos(az) + \
                       math.cos(declination) * math.cos(slope) * math.cos(zenith_angle) + \
                       math.cos(slope) * math.sin(az) * math.sin(zenith_angle)

        return cos_incident

    @staticmethod
    def incident(latitude, slope, az, sol_time, day_of_yr):
        """
        Compute the angle of incidence of solar beam radiation on a surface.

        :param latitude: Latitude (radians)
        :param slope: Slope of the surface relative to horizontal (radians)
        :param az: Azimuth angle of the surface relative to South (radians, E+, W-)
        :param sol_time: Solar time (decimal hours)
        :param day_of_yr: Day of year from Jan 1
        :return: Angle of incidence (angle between solar beam and surface normal) in radians.
        """
        # Calculate the cosine of the angle of incidence
        cos_incident = SolarAngles.cos_incident(latitude, slope, az, sol_time, day_of_yr)

        # Calculate the angle of incidence (in radians) using the inverse cosine (arccos)
        angle_of_incidence = math.acos(cos_incident)

        return angle_of_incidence

    @staticmethod
    def zenith(day_of_yr, latitude, sol_time):
        """
        Compute the solar zenith angle (radians), the angle between the solar beam
        and the vertical. This is more efficient with this dedicated function.

        :param day_of_yr: Day of year from Jan 1
        :param latitude: Latitude (radians)
        :param sol_time: Solar time (decimal hours)
        :return: Zenith angle in radians.
        """
        # Calculate the hour angle in radians
        hr_ang = -(15.0 * math.pi / 180) * (sol_time - 12.0)  # morning is positive, afternoon is negative

        # Calculate the solar declination angle
        decl = SolarAngles.declination(day_of_yr)

        # Calculate the zenith angle in radians using the formula
        zenith_angle = math.acos(math.sin(decl) * math.sin(latitude) +
                                 math.cos(decl) * math.cos(latitude) * math.cos(hr_ang))

        return zenith_angle

    @staticmethod
    def altitude(day_of_yr, latitude, sol_time):
        """
        Compute the solar altitude angle (radians), the angle between the solar beam
        and the vertical. This is more efficient with this dedicated function.

        :param day_of_yr: Day of year from Jan 1
        :param latitude: Latitude (radians)
        :param sol_time: Solar time (hours)
        :return: Altitude angle (angle above the horizon) in radians.
        """
        # Calculate the zenith angle
        zenith_angle = SolarAngles.zenith(day_of_yr, latitude, sol_time)

        # Calculate the altitude angle in radians (90 degrees - zenith angle)
        altitude_angle = (90.0 * math.pi / 180) - zenith_angle

        return altitude_angle

    @staticmethod
    def hr_sunrise(day_of_yr, latitude):
        """
        Compute the hour of sunrise.

        :param day_of_yr: Day of year
        :param latitude: Latitude (radians)
        :return: Solar hour of sunrise.
        """
        # Calculate the hour angle of sunrise (converted to degrees)
        hr_ang = math.degrees(math.acos(-math.tan(latitude) * math.tan(SolarAngles.declination(day_of_yr))))

        # Convert hour angle to solar time
        return (-hr_ang / 15.0) + 12.0

    @staticmethod
    def day_len(day_of_yr, latitude):
        """
        Compute the length of a given day.

        :param day_of_yr: Day of year
        :param latitude: Latitude (radians)
        :return: Day length (hours).
        """
        return (2.0 * math.acos(-math.tan(latitude) *
                                math.tan(SolarAngles.declination(day_of_yr)))) / (15.0 * math.pi / 180.0)

    @staticmethod
    def day_of_yr(month, day):
        """
        Compute Julian day of the year.

        :param month: Month of the year (1-12)
        :param day: Day of the month (1-31)
        :return: Day of the year (Julian day)
        """
        # Error checking on the range of month and day could be added here.

        # This ignores leap years, but the other functions assume a year has only 365 days.
        return days_thru_month[month - 1] + day

    @staticmethod
    def elevation(day_of_yr, latitude, sol_time):
        """
        Compute the solar elevation angle.

        :param day_of_yr: Day of year
        :param latitude: Latitude (radians)
        :param sol_time: Solar time (decimal hours)
        :return: Solar elevation angle (radians)
        """
        # Calculate the hour angle of the sun (converted to degrees)
        hr_ang = -(15.0 * math.pi / 180.0) * (sol_time - 12.0)  # morning +, afternoon -

        decl = SolarAngles.declination(day_of_yr)

        return math.asin(math.sin(decl) * math.sin(latitude) + math.cos(decl) * math.cos(latitude) * math.cos(hr_ang))

    @staticmethod
    def azimuth(day_of_yr, latitude, sol_time):
        """
        Compute the solar azimuth angle.

        :param day_of_yr: Day of year
        :param latitude: Latitude (radians)
        :param sol_time: Solar time (decimal hours)
        :return: Solar azimuth angle (radians)
        """
        # Calculate the hour angle of the sun (converted to degrees)
        hr_ang = -(15.0 * math.pi / 180.0) * (sol_time - 12.0)  # morning +, afternoon -

        decl = SolarAngles.declination(day_of_yr)

        alpha = (90.0 * math.pi / 180.0) - latitude + decl

        rs = (math.sin(decl) * math.cos(latitude) - math.cos(decl) *
              math.sin(latitude) * math.cos(hr_ang)) / math.cos(alpha)

        # Ensure rs is within the valid range [-1.0, 1.0] to avoid numerical issues
        rs = max(min(rs, 1.0), -1.0)

        return math.acos(rs)

    def S_solpos(self, pdat):
        # /*============================================================================
        # *    Long integer function S_solpos, adapted from the VAX solar libraries
        # *
        # *    This function calculates the apparent solar position and the
        # *    intensity of the sun (theoretical maximum solar energy) from
        # *    time and place on Earth.
        # *
        # *    Requires (from the SOLPOS_POSDATA parameter):
        # *        Date and time:
        # *            year
        # *            daynum   (requirement depends on the S_DOY switch)
        # *            month    (requirement depends on the S_DOY switch)
        # *            day      (requirement depends on the S_DOY switch)
        # *            hour
        # *            minute
        # *            second
        # *            interval  DEFAULT 0
        # *        Location:
        # *            latitude
        # *            longitude
        # *        Location/time adjuster:
        # *            timezone
        # *        Atmospheric pressure and temperature:
        # *            press     DEFAULT 1013.0 mb
        # *            temp      DEFAULT 10.0 degrees C
        # *        Tilt of flat surface that receives solar energy:
        # *            aspect    DEFAULT 180 (South)
        # *            tilt      DEFAULT 0 (Horizontal)
        # *        Function Switch (codes defined in solpos.h)
        # *            function  DEFAULT S_ALL
        # *
        # *    Returns (via the SOLPOS_POSDATA parameter):
        # *        everything defined in the SOLPOS_POSDATA in solpos.h.
        # *----------------------------------------------------------------------------*/

        trigdat = SOLPOS_TRIGDATA()  # Create an instance of SOLPOS_TRIGDATA
        tdat = trigdat  # Point to the structure

        # Initialize the trig structure
        trigdat.sd = -999.0  # Flag to force calculation of trig data
        trigdat.cd = 1.0
        trigdat.ch = 1.0  # Set the rest of these to something safe
        trigdat.cl = 1.0
        trigdat.sl = 1.0

        pdat = self.doy2dom(pdat)  # Convert input doy to month-day
        pdat = self.geometry(pdat)  # Do basic geometry calculations
        pdat = self.zen_no_ref(pdat, tdat)  # Etr at non-refracted zenith angle
        pdat = self.ssha_calc(pdat, tdat)  # Sunset hour calculation
        pdat = self.sbcf(pdat, tdat)  # Shadowband correction factor
        pdat = self.tst(pdat)  # True solar time
        pdat = self.srss(pdat)  # Sunrise/sunset calculations
        pdat = self.sazm(pdat, tdat)  # Solar azimuth calculations
        pdat = self.refrac(pdat)  # Atmospheric refraction calculations
        pdat = self.amass_calc(pdat)  # Airmass calculations
        pdat = self.prime_calc(pdat)  # Kt-prime/unprime calculations
        pdat = self.etr(pdat)  # ETR and ETRN (refracted)
        pdat = self.tilt_calc(pdat)  # Tilt calculations
        pdat = self.perez_tilt(pdat)  # Perez tilt calculations
        return pdat

    @staticmethod
    def S_init(pdat):
        """
        Initialize input parameters in the posdata structure.

        This function initiates all the input parameters in the struct
        posdata passed to S_solpos(). Initialization is either to nominal
        values or to out of range values, which forces the calling program to
        specify parameters.

        NOTE: This function is optional if you initialize ALL input parameters
              in your calling code. Note that the required parameters of date
              and location are deliberately initialized out of bounds to force
              the user to enter real-world values.

        :param pdat: Pointer to a posdata structure, members of which are initialized.
        :return: None
        """
        pdat.day = -99  # Day of month (May 27 = 27, etc.)
        pdat.daynum = -999  # Day number (day of year; Feb 1 = 32)
        pdat.hour = -99  # Hour of day, 0 - 23
        pdat.minute = -99  # Minute of hour, 0 - 59
        pdat.month = -99  # Month number (Jan = 1, Feb = 2, etc.)
        pdat.second = -99  # Second of minute, 0 - 59
        pdat.year = -99  # 4-digit year
        pdat.interval = 0  # instantaneous measurement interval
        pdat.aspect = math.pi  # Azimuth of panel surface (direction it
        # faces) N=0, E=90, S=180, W=270 - converted to radians
        pdat.latitude = -99.0  # Latitude, degrees north (south negative)
        pdat.longitude = -999.0  # Longitude, degrees east (west negative)
        pdat.press = 1013.0  # Surface pressure, millibars
        pdat.solcon = 126.998456  # Solar constant, 1367 W/sq m - 126.998456; W/sq ft
        pdat.temp = 15.0  # Ambient dry-bulb temperature, degrees C
        pdat.tilt = 0.0  # Radians tilt from horizontal of panel
        pdat.timezone = -99.0  # Time zone, east (west negative).
        pdat.sbwid = 7.6  # Eppley shadow bandwidth
        pdat.sbrad = 31.7  # Eppley shadow band radius
        pdat.sbsky = 0.04  # Drummond factor for partly cloudy skies
        pdat.perez_horz = 1.0  # By default, perez_horz is full diffuse
        return pdat

    @staticmethod
    def doy2dom(pdat):
        # /*============================================================================
        # *    Local void function doy2dom
        # *
        # *    This function computes the month/day from the day number.
        # *
        # *    Requires (from SOLPOS_POSDATA parameter):
        # *        Year and day number:
        # *            year
        # *            daynum
        # *
        # *    Returns (via the SOLPOS_POSDATA parameter):
        # *            year
        # *            month
        # *            day
        # *----------------------------------------------------------------------------*/

        # month_days = [
        #     [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334],
        #     [0, 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335]
        # ]

        leap = 1 if ((pdat.year % 4 == 0) and ((pdat.year % 100 != 0) or (pdat.year % 400 == 0))) else 0

        imon = 12
        while pdat.daynum <= month_days[leap][imon]:
            imon -= 1

        pdat.month = imon
        pdat.day = pdat.daynum - month_days[leap][imon]
        return pdat

    @staticmethod
    def geometry(pdat):
        """
        Perform the underlying geometry calculations for a given time and location.

        :param pdat: Pointer to a posdata structure, members of which are initialized.
        :return: None
        """
        # raddeg = math.pi / 180.0
        # degrad = 180.0 / math.pi
        PI = math.pi

        # Day angle
        pdat.dayang = 2.0 * PI * (pdat.daynum - 1) / 365.0

        # Earth radius vector * solar constant = solar energy
        sd = math.sin(pdat.dayang)
        cd = math.cos(pdat.dayang)
        d2 = 2.0 * pdat.dayang
        c2 = math.cos(d2)
        s2 = math.sin(d2)

        pdat.erv = 1.000110 + 0.034221 * cd + 0.001280 * sd
        pdat.erv += 0.000719 * c2 + 0.000077 * s2

        # Universal Coordinated (Greenwich standard) time
        pdat.utime = pdat.hour * 3600.0 + pdat.minute * 60.0 + pdat.second - float(pdat.interval) / 2.0
        pdat.utime = pdat.utime / 3600.0 - pdat.timezone

        # Julian Day minus 2,400,000 days (to eliminate roundoff errors)
        delta = pdat.year - 1949
        leap = int(delta / 4.0)
        pdat.julday = 32916.5 + delta * 365.0 + leap + pdat.daynum + pdat.utime / 24.0

        # Time used in the calculation of ecliptic coordinates
        pdat.ectime = pdat.julday - 51545.0

        # Mean longitude
        pdat.mnlong = 280.460 + 0.9856474 * pdat.ectime

        # (dump the multiples of 360, so the answer is between 0 and 360)
        pdat.mnlong -= 360.0 * int(pdat.mnlong / 360.0)
        if pdat.mnlong < 0.0:
            pdat.mnlong += 360.0

        # Mean anomaly
        pdat.mnanom = 357.528 + 0.9856003 * pdat.ectime

        # (dump the multiples of 360, so the answer is between 0 and 360)
        pdat.mnanom -= 360.0 * int(pdat.mnanom / 360.0)
        if pdat.mnanom < 0.0:
            pdat.mnanom += 360.0

        # Ecliptic longitude
        pdat.eclong = pdat.mnlong + 1.915 * math.sin(pdat.mnanom * raddeg) + 0.020 * math.sin(
            2.0 * pdat.mnanom * raddeg)

        # (dump the multiples of 360, so the answer is between 0 and 360)
        pdat.eclong -= 360.0 * int(pdat.eclong / 360.0)
        if pdat.eclong < 0.0:
            pdat.eclong += 360.0

        # Obliquity of the ecliptic
        pdat.ecobli = 23.439 - 4.0e-07 * pdat.ectime

        # Declination
        pdat.declin = math.asin(math.sin(pdat.ecobli * raddeg) * math.sin(pdat.eclong * raddeg))

        # Right ascension
        top = math.cos(raddeg * pdat.ecobli) * math.sin(raddeg * pdat.eclong)
        bottom = math.cos(raddeg * pdat.eclong)
        pdat.rascen = degrad * math.atan2(top, bottom)

        # (make it a positive angle)
        if pdat.rascen < 0.0:
            pdat.rascen += 360.0

        # Greenwich mean sidereal time
        pdat.gmst = 6.697375 + 0.0657098242 * pdat.ectime + pdat.utime

        # (dump the multiples of 24, so the answer is between 0 and 24)
        pdat.gmst -= 24.0 * int(pdat.gmst / 24.0)
        if pdat.gmst < 0.0:
            pdat.gmst += 24.0

        # Local mean sidereal time
        pdat.lmst = pdat.gmst * 15.0 + pdat.longitude

        # (dump the multiples of 360, so the answer is between 0 and 360)
        pdat.lmst -= 360.0 * int(pdat.lmst / 360.0)
        if pdat.lmst < 0.0:
            pdat.lmst += 360.0

        # Hour angle
        pdat.hrang = pdat.lmst - pdat.rascen

        # (force it between -180 and 180 degrees)
        if pdat.hrang < -180.0:
            pdat.hrang += 360.0
        elif pdat.hrang > 180.0:
            pdat.hrang -= 360.0
        return pdat

    @staticmethod
    def zen_no_ref(pdat, tdat):
        """
        Calculate the ETR solar zenith angle.

        :param pdat: Pointer to a posdata structure.
        :param tdat: Pointer to a trigdata structure.
        :return: None
        """
        # raddeg = math.pi / 180.0
        # degrad = 180.0 / math.pi

        tdat.cd = math.cos(pdat.declin)
        tdat.ch = math.cos(raddeg * pdat.hrang)
        tdat.cl = math.cos(pdat.latitude)
        tdat.sd = math.sin(pdat.declin)
        tdat.sl = math.sin(pdat.latitude)

        cz = tdat.sd * tdat.sl + tdat.cd * tdat.cl * tdat.ch

        # Watch out for roundoff errors
        if abs(cz) > 1.0:
            if cz >= 0.0:
                cz = 1.0
            else:
                cz = -1.0

        pdat.zenetr = math.acos(cz) * degrad

        # Limit the degrees below the horizon to 9 [+90 -> 99]
        if pdat.zenetr > 99.0:
            pdat.zenetr = 99.0

        pdat.elevetr = 90.0 - pdat.zenetr
        return pdat

    @staticmethod
    def ssha_calc(pdat, tdat):
        """
        Calculate the sunset hour angle in degrees.

        :param pdat: Pointer to a posdata structure.
        :param tdat: Pointer to a trigdata structure.
        :return: None
        """
        cdcl = tdat.cd * tdat.cl
        if abs(cdcl) >= 0.001:
            cssha = -tdat.sl * tdat.sd / cdcl
            if cssha < -1.0:
                pdat.ssha = 180.0
            elif cssha > 1.0:
                pdat.ssha = 0.0
            else:
                pdat.ssha = math.degrees(math.acos(cssha))
        elif ((pdat.declin >= 0.0 and pdat.latitude > 0.0) or
              (pdat.declin < 0.0 and pdat.latitude < 0.0)):
            pdat.ssha = 180.0
        else:
            pdat.ssha = 0.0
        return pdat

    @staticmethod
    def sbcf(pdat, tdat):
        # /*============================================================================
        # *    Local Void function sbcf
        # *
        # *    Shadowband correction factor
        # *       Drummond, A. J.  1956.  A contribution to absolute pyrheliometry.
        # *            Q. J. R. Meteorol. Soc. 82, pp. 481-493
        # *----------------------------------------------------------------------------*/
        p = 0.6366198 * pdat.sbwid / pdat.sbrad * math.pow(tdat.cd, 3)
        t1 = tdat.sl * tdat.sd * pdat.ssha * math.degrees
        t2 = tdat.cl * tdat.cd * math.sin(pdat.ssha * math.degrees)
        pdat.sbcf = pdat.sbsky + 1.0 / (1.0 - p * (t1 + t2))
        return pdat

    @staticmethod
    def tst(pdat):
        # /*============================================================================
        # *    Local Void function tst
        # *
        # *    TST -> True Solar Time = local standard time + TSTfix, time
        # *      in minutes from midnight.
        # *        Iqbal, M.  1983.  An Introduction to Solar Radiation.
        # *            Academic Press, NY., page 13
        # *----------------------------------------------------------------------------*/
        pdat.tst = (180.0 + pdat.hrang) * 4.0
        pdat.tstfix = pdat.tst - (float(pdat.hour) * 60.0 +
                                  pdat.minute -
                                  float(pdat.second) / 60.0 +
                                  float(pdat.interval) / 120.0)
        while pdat.tstfix > 720.0:
            pdat.tstfix -= 1440.0
        while pdat.tstfix < -720.0:
            pdat.tstfix += 1440.0
        pdat.eqntim = pdat.tstfix + 60.0 * pdat.timezone - 4.0 * pdat.longitude
        return pdat

    @staticmethod
    def srss(pdat):
        # /*============================================================================
        # *    Local Void function srss
        # *
        # *    Sunrise and sunset times (minutes from midnight)
        # *----------------------------------------------------------------------------*/
        if pdat.ssha <= 1.0:
            pdat.sretr = 2999.0
            pdat.ssetr = -2999.0
        elif pdat.ssha >= 179.0:
            pdat.sretr = -2999.0
            pdat.ssetr = 2999.0
        else:
            pdat.sretr = 720.0 - 4.0 * pdat.ssha - pdat.tstfix
            pdat.ssetr = 720.0 + 4.0 * pdat.ssha - pdat.tstfix
        return pdat

    @staticmethod
    def sazm(pdat, tdat):
        # /*============================================================================
        # *    Local Void function sazm
        # *
        # *    Solar azimuth angle
        # *       Iqbal, M.  1983.  An Introduction to Solar Radiation.
        # *            Academic Press, NY., page 15
        # *----------------------------------------------------------------------------*/
        ce = math.cos(math.radians(pdat.elevetr))
        se = math.sin(math.radians(pdat.elevetr))
        pdat.azim = 180.0
        cecl = ce * tdat.cl
        if abs(cecl) >= 0.001:
            ca = (se * tdat.sl - tdat.sd) / cecl
            if ca > 1.0:
                ca = 1.0
            elif ca < -1.0:
                ca = -1.0
            pdat.azim = 180.0 - math.degrees(math.acos(ca))
            if pdat.hrang > 0:
                pdat.azim = 360.0 - pdat.azim
        return pdat

    @staticmethod
    def refrac(pdat):
        """
        Calculate the refraction correction in degrees.

        :param pdat: Pointer to a posdata structure.
        :return: None
        """
        # raddeg = math.pi / 180.0
        # degrad = 180.0 / math.pi

        prestemp = 0.0  # Temporary pressure/temperature correction
        refcor = 0.0    # Temporary refraction correction
        tanelev = 0.0   # Tangent of the solar elevation angle

        # If the sun is near zenith, the algorithm bombs; refraction near 0
        if pdat.elevetr > 85.0:
            refcor = 0.0
        else:
            tanelev = math.tan(raddeg * pdat.elevetr)
            if pdat.elevetr >= 5.0:
                refcor = 58.1 / tanelev - 0.07 / (tanelev ** 3) + 0.000086 / (tanelev ** 5)
            elif pdat.elevetr >= -0.575:
                refcor = (
                    1735.0
                    + pdat.elevetr * (-518.2 + pdat.elevetr * (103.4 + pdat.elevetr * (-12.79 + pdat.elevetr * 0.711)))
                )
            else:
                refcor = -20.774 / tanelev

            prestemp = (pdat.press * 283.0) / (1013.0 * (273.0 + pdat.temp))
            refcor *= prestemp / 3600.0

        # Refracted solar elevation angle
        pdat.elevref = pdat.elevetr + refcor

        # Limit the degrees below the horizon to 9
        if pdat.elevref < -9.0:
            pdat.elevref = -9.0

        # Refracted solar zenith angle
        pdat.zenref = 90.0 - pdat.elevref
        pdat.coszen = math.cos(raddeg * pdat.zenref)
        return pdat

    @staticmethod
    def amass_calc(pdat):
        """
        Calculate the airmass.

        :param pdat: Pointer to a posdata structure.
        :return: None
        """
        if pdat.zenref > 93.0:
            pdat.amass = -1.0
            pdat.ampress = -1.0
        else:
            pdat.amass = 1.0 / (
                math.cos(raddeg * pdat.zenref) + 0.50572 * (96.07995 - pdat.zenref) ** -1.6364
            )
            pdat.ampress = pdat.amass * pdat.press / 1013.0
        return pdat

    @staticmethod
    def prime_calc(pdat):
        """
        Calculate the prime and unprime factors.

        :param pdat: Pointer to a posdata structure.
        :return: None
        """
        pdat.unprime = 1.031 * math.exp(-1.4 / (0.9 + 9.4 / pdat.amass)) + 0.1
        pdat.prime = 1.0 / pdat.unprime
        return pdat

    @staticmethod
    def etr(pdat):
        """
        Calculate the extraterrestrial solar irradiance.

        :param pdat: Pointer to a posdata structure.
        :return: None
        """
        if pdat.coszen > 0.0:
            pdat.etrn = pdat.solcon * pdat.erv
            pdat.etr = pdat.etrn * pdat.coszen
        else:
            pdat.etrn = 0.0
            pdat.etr = 0.0
        return pdat

    @staticmethod
    def tilt_calc(pdat):
        """
        Calculate the ETR on a tilted surface.

        :param pdat: Pointer to a posdata structure.
        :return: None
        """
        # raddeg = math.pi / 180.0
        # Cosine of the angle between the sun and a tipped flat surface,
        # useful for calculating solar energy on tilted surfaces
        ca = math.cos(raddeg * pdat.azim) # Cosine of the solar azimuth angle
        cp = math.cos(pdat.aspect)  # Cosine of the panel aspect
        ct = math.cos(pdat.tilt)  # Cosine of the panel tilt
        sa = math.sin(raddeg * pdat.azim)  # Sine of the solar azimuth angle
        sp = math.sin(pdat.aspect) # Sine of the panel aspect
        st = math.sin(pdat.tilt) # Sine of the panel tilt
        sz = math.sin(raddeg * pdat.zenref) # Sine of the refraction corrected solar zenith angle
        pdat.cosinc = pdat.coszen * ct + sz * st * (ca * cp + sa * sp)

        if pdat.cosinc > 0.0:
            pdat.etrtilt = pdat.etrn * pdat.cosinc
        else:
            pdat.etrtilt = 0.0
        return pdat

    @staticmethod
    def perez_tilt(pdat):
        """
        Perez diffuse radiation tilt model.

        Extracted from Perez et al., "Modeling Dayling Availability and Irradiance Components from Direct and
        Global Irradiance," Solar Energy, vol. 44, no. 7, pp. 271-289, 1990.

        :param pdat: Pointer to a posdata structure.
        :return: None
        """
        # PI_OVER_180 = math.pi / 180.0
        # COS85DEG = math.cos(85.0 * PI_OVER_180)

        zen_rad = 0.0
        zen_rad_cubed = 0.0
        a_val = 0.0
        b_val = 0.0
        index = 0

        # See if there's even any diffuse radiation to care about - i.e., is it not night
        if pdat.diff_horz != 0.0:
            # Put the zenith angle into radians so that it works with the Perez model
            zen_rad = pdat.zenref * PI_OVER_180

            # Make a cube of it and scale it since we'll need it in a couple places
            # Uses constant of 1.041 for zenith in radians (per Perez et al. 1990)
            zen_rad_cubed = zen_rad * zen_rad * zen_rad * 1.041

            # Compute sky clearness - if there's no direct on the surface, it's 1.0 (save some calculations)
            if pdat.dir_norm != 0.0:
                pdat.perez_skyclear = ((pdat.diff_horz + pdat.dir_norm) / pdat.diff_horz + zen_rad_cubed) / (
                            1 + zen_rad_cubed)
            else:
                pdat.perez_skyclear = 1.0

            # Flag the index
            pdat.perez_skyclear_idx = -1

            # Index out the sky clearness
            for index in range(7):
                if (pdat.perez_skyclear >= perez_clearness_limits[index]) and (
                        pdat.perez_skyclear < perez_clearness_limits[index + 1]):
                    pdat.perez_skyclear_idx = index  # Indices are offset by one since they'll be used as indices later
                    break  # Get us out once we're assigned

            # If exited and is still -1, means it must be "clear" (index region 8)
            if pdat.perez_skyclear_idx == -1:
                pdat.perez_skyclear_idx = 7  # 0 referenced - 8th bin

            # Calculate the sky brightness
            if pdat.etrn == 0.0:
                pdat.perez_brightness = 0.0
            else:
                pdat.perez_brightness = (pdat.diff_horz * pdat.amass / pdat.etrn)

            # Now calculate the F1 and F2 coefficients
            pdat.perez_F1 = perez_tilt_coeff_F1[0][pdat.perez_skyclear_idx] + perez_tilt_coeff_F1[1][
                pdat.perez_skyclear_idx] * pdat.perez_brightness + perez_tilt_coeff_F1[2][
                                pdat.perez_skyclear_idx] * zen_rad
            pdat.perez_F2 = perez_tilt_coeff_F2[0][pdat.perez_skyclear_idx] + perez_tilt_coeff_F2[1][
                pdat.perez_skyclear_idx] * pdat.perez_brightness + perez_tilt_coeff_F2[2][
                                pdat.perez_skyclear_idx] * zen_rad

            # Maximum check
            if pdat.perez_F1 < 0:
                pdat.perez_F1 = 0.0

            # Now compute the Perez horizontal scalar (to be applied to diffuse) - get a & b values first
            if pdat.cosinc > 0.0:
                a_val = pdat.cosinc
            else:
                a_val = 0.0

            if pdat.coszen > COS85DEG:
                b_val = pdat.coszen
            else:
                b_val = COS85DEG

            # Compute the scalar
            pdat.perez_horz = ((1 - pdat.perez_F1) * (1 + math.cos(pdat.tilt)) / 2.0 +
                               pdat.perez_F1 * a_val / b_val + pdat.perez_F2 * math.sin(pdat.tilt))
        else:  # Must be night, just assign a zero constant
            pdat.perez_horz = 0.0

        return pdat


# //Most additions below here are from the NREL Solar Position algorithm 2.0
# //http://rredc.nrel.gov/solar/codesandalgorithms/solpos/aboutsolpos.html
# //Perez model function at the end (perez_tilt) extracted from referenced paper
# /*============================================================================
# *    Contains:
# *        S_solpos     (computes solar position and intensity
# *                      from time and place)
# *
# *            INPUTS:     (via posdata struct) year, daynum, hour,
# *                        minute, second, latitude, longitude, timezone,
# *                        intervl
# *            OPTIONAL:   (via posdata struct) month, day, press, temp, tilt,
# *                        aspect, function
# *            OUTPUTS:    EVERY variable in the SOLPOS_POSDATA
# *                            (defined in solpos.h)
# *
# *                       NOTE: Certain conditions exist during which some of
# *                       the output variables are undefined or cannot be
# *                       calculated.  In these cases, the variables are
# *                       returned with flag values indicating such.  In other
# *                       cases, the variables may return a realistic, though
# *                       invalid, value. These variables and the flag values
# *                       or invalid conditions are listed below:
# *
# *                       amass     -1.0 at zenetr angles greater than 93.0
# *                                 degrees
# *                       ampress   -1.0 at zenetr angles greater than 93.0
# *                                 degrees
# *                       azim      invalid at zenetr angle 0.0 or latitude
# *                                 +/-90.0 or at night
# *                       elevetr   limited to -9 degrees at night
# *                       etr       0.0 at night
# *                       etrn      0.0 at night
# *                       etrtilt   0.0 when cosinc is less than 0
# *                       prime     invalid at zenetr angles greater than 93.0
# *                                 degrees
# *                       sretr     +/- 2999.0 during periods of 24 hour sunup or
# *                                 sundown
# *                       ssetr     +/- 2999.0 during periods of 24 hour sunup or
# *                                 sundown
# *                       ssha      invalid at the North and South Poles
# *                       unprime   invalid at zenetr angles greater than 93.0
# *                                 degrees
# *                       zenetr    limited to 99.0 degrees at night
# *
# *        S_init       (optional initialization for all input parameters in
# *                      the posdata struct)
# *           INPUTS:     SOLPOS_POSDATA*
# *           OUTPUTS:    SOLPOS_POSDATA*
# *
# *                     (Note: initializes the required S_solpos INPUTS above
# *                      to out-of-bounds conditions, forcing the user to
# *                      supply the parameters; initializes the OPTIONAL
# *                      S_solpos inputs above to nominal values.)
# *
# *       S_decode      (optional utility for decoding the S_solpos return code)
# *           INPUTS:     long integer S_solpos return value, SOLPOS_POSDATA*
# *           OUTPUTS:    text to stderr
# *
# *    Usage:
# *         In calling program, just after other 'includes', insert:
# *
# *              #include "solpos00.h"
# *
# *         Function calls:
# *              S_init(SOLPOS_POSDATA*)  [optional]
# *              .
# *              .
# *              [set time and location parameters before S_solpos call]
# *              .
# *              .
# *              int retval = S_solpos(SOLPOS_POSDATA*)
# *              S_decode(int retval, SOLPOS_POSDATA*) [optional]
# *                  (Note: you should always look at the S_solpos return
# *                   value, which contains error codes. S_decode is one option
# *                   for examining these codes.  It can also serve as a
# *                   template for building your own application-specific
# *                   decoder.)
# *
# *    Martin Rymes
# *    National Renewable Energy Laboratory
# *    25 March 1998
# *
# *    27 April 1999 REVISION:  Corrected leap year in S_date.
# *    13 January 2000 REVISION:  SMW converted to structure posdata parameter
# *                               and subdivided into functions.
# *    01 February 2001 REVISION: SMW corrected ecobli calculation
# *                               (changed sign). Error is small (max 0.015 deg
# *                               in calculation of declination angle)
# *----------------------------------------------------------------------------*/
