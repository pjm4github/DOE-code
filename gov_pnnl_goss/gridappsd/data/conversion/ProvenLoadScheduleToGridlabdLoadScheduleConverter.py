# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
import calendar
import datetime
import io

from gov_pnnl_goss.gridappsd.api.DataManager import DataManager
from gov_pnnl_goss.gridappsd.api.LogManager import LogManager
from gov_pnnl_goss.gridappsd.configuration.CIMDictionaryConfigurationHandler import PrintWriter
from gov_pnnl_goss.gridappsd.data.conversion.DataFormatConverter import DataFormatConverter
from gov_pnnl_goss.gridappsd.dto.LogMessage import ProcessStatus
from gov_pnnl_goss.gridappsd.dto.RequestTimeseriesData import RequestTimeseriesData
from gov_pnnl_goss.gridappsd.dto.TimeSeriesEntryResult import TimeSeriesEntryResult


class Calendar(datetime.date):
    """

    """
    YEAR = 0
    MONTH = 1
    DAY_OF_MONTH = 2

    # Format Style
    SHORT = 0
    LONG = 1

    def __init__(self, **kwargs):
        super().__init__(kwargs)
        self._cal_object  = {self.YEAR: 0,
                             self.MONTH: 0,
                             self.DAY_OF_MONTH: 0
                            }

    def get(self, field):
        #  get(int field): Returns the value of the specified field
        #  (e.g., Calendar.YEAR, Calendar.MONTH, Calendar.DAY_OF_MONTH, etc.) for the calendar instance.
        return self._cal_object[field]

    def set(self, field: int, value: int):
        # Sets the value of the specified field to the given value.
        self._cal_object[field] = value

    def add(self, field: int, amount: int):
        # add(int field, int amount): Adds or subtracts the specified amount to/from the specified field.
        pass

    def get_time(self):
        # getTime(): Returns a java.util.Date object representing the date and time of the calendar instance.
        pass

    def set_time(self, date: datetime):
        #     setTime(date): Sets the calendar'status date and time to that of the specified java.util.Date object.
        pass

    def get_actual_maximum(self, field:int):
        #     getActualMaximum(int field): Returns the maximum value that can be set for the specified field in the current calendar instance.
        pass

    def get_actual_minimum(self, field: int):
        #     getActualMinimum(int field): Returns the minimum value that can be set for the specified field in the current calendar instance.
        pass

    def get_display_name(self, field:int, style: int, locale: datetime.timezone):
        #  getDisplayName(int field, int style, locale):
        #  Returns the display name of the specified field in the specified style (e.g., Calendar.SHORT, Calendar.LONG) and locale.
        pass

    def is_leap_year(self, year: int):
        #     isLeapYear(int year): Checks if the given year is a leap year.
        pass

    def is_set(self, field):
        #     isSet(int field): Checks if a specific field has been set in the calendar.
        pass

    def clear(self):
        #     clear(): Clears all fields of the calendar, setting them to their default values.
        pass

    def before(self, when):
        #     before(Object when): Checks if the calendar date and time is before the specified date and time.
        pass

    def after(self, when):
        #     after(Object when): Checks if the calendar date and time is after the specified date and time.
        pass
    def __eq__(self, other):
        #     equals(Object obj): Checks if two calendar instances represent the same date and time.
        pass

    def roll(self,field: int, up: bool):
        #     roll(int field, boolean up): Rolls (increments or decrements) the specified field without changing the larger fields (e.g., rolling the day of the month while keeping the month and year unchanged).
        pass

    def set_timezone(self, value: datetime.timezone):
        #     setTimeZone(TimeZone value): Sets the time zone of the calendar instance.
        pass


class ProvenLoadScheduleToGridlabdLoadScheduleConverter(DataFormatConverter):
    sdf_in = "MM/dd/yyyy HH:mm"
    sdf_out = "yyyy-MM-dd HH:mm:ss"

    INPUT_FORMAT = "PROVEN_loadprofile"
    OUTPUT_FORMAT = "GRIDLABD_LOAD_SCHEDULE"

    SOLAR_DIFFUSE = "Diffuse"
    AVG_WIND_SPEED = "AvgWindSpeed"
    AVG_WIND_DIRECTION = "AvgWindDirection"
    HUMIDITY = "TowerRH"
    LONGITUDE = "long"
    LATITUDE = "lat"
    MST = "UTC"
    TEMPERATURE = "TowerDryBulbTemp"
    DATE = "DATE"
    TIME = "time"
    SOLAR_DIRECT = "DirectCH1"
    SOLAR_GLOBAL = "GlobalCM22"
    PLACE = "place"

    def __init__(self, logManager=None, dataManager=None):
        self.logger = logManager if logManager else LogManager(ProvenLoadScheduleToGridlabdLoadScheduleConverter.__name__)
        self.data_manager = dataManager if dataManager else DataManager()

    def start(self):
        if self.data_manager:
            self.data_manager.register_converter(self.INPUT_FORMAT, self.OUTPUT_FORMAT, self)
        else:
            if self.logger:
                self.logger.warn(ProcessStatus.RUNNING, None, "No Data manager available for " + self.getClass())

    def convert(self, input_content, output_content: PrintWriter, request: RequestTimeseriesData):
        if isinstance(input_content, str):
            result_obj = TimeSeriesEntryResult.parse(input_content)
        else:
            str_content = str(input_content)
            result_obj = TimeSeriesEntryResult.parse(str_content)

        is_first_record = True
        c = Calendar()
        year = request.simulation_year
        for _map in result_obj.getData():
            if is_first_record:
                long_time = int(float(_map.get("time")))
                c.set_time((long_time * 1000))
                c.set(Calendar.YEAR, year)
                output_content.print(self.sdf_out.format(c.get_time()) + " UTC," + _map.get("value") + "\n")
                is_first_record = False
            else:
                output_content.print("+1m," + _map.get("value") + "\n")

