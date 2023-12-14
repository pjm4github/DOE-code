# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
import datetime
import sys
from io import StringIO

from gov_pnnl_goss.core.security.SecurityConfig import SecurityConfig
from gov_pnnl_goss.gridappsd.api.DataManager import DataManager
from gov_pnnl_goss.gridappsd.api.LogManager import LogManager
from gov_pnnl_goss.gridappsd.data.conversion.DataFormatConverter import DataFormatConverter
from gov_pnnl_goss.gridappsd.dto.LogMessage import ProcessStatus
from gov_pnnl_goss.gridappsd.dto.TimeSeriesEntryResult import TimeSeriesEntryResult


class ProvenWeatherToGridlabdWeatherConverter(DataFormatConverter):
    
    sdf_in = "MM/dd/yyyy HH:mm"
    sdf_out = "MM:dd:HH:mm:ss"
    INPUT_FORMAT = "PROVEN_WEATHER"
    OUTPUT_FORMAT = "GRIDLABD_WEATHER"
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

    def __init__(self, log_manager=None, data_manager=None):
        self.logger = log_manager if log_manager else LogManager(ProvenWeatherToGridlabdWeatherConverter.__name__)
        self.data_manager = data_manager if data_manager else DataManager()
        self.security_config = SecurityConfig()

    def start(self):
        if self.data_manager is not None:
            self.data_manager.register_converter(self.INPUT_FORMAT, self.OUTPUT_FORMAT, self)
        else:
            if self.logger is not None:
                self.logger.warn(ProcessStatus.RUNNING, None, "No Data manager available for " + self.__class__.__name__)

    def convert(self, input_content, output_content, request):
        if isinstance(input_content, str):
            result_obj = TimeSeriesEntryResult.parse(input_content)
        else:
            str_content = str(input_content)
            result_obj = TimeSeriesEntryResult.parse(str_content)
        header_printed = False
        # for (TimeSeriesMeasurementResult record: resultObj.getMeasurements()):
        if not header_printed:
            self.print_gld_header(result_obj.data[0], output_content)
            header_printed = True
        self.convert_record(result_obj, output_content)

    def print_gld_header(self, mp, output_content):
        place_str, year_str, latlong = "", "", ""
        try:
            place_str = mp.get(self.PLACE).replace("\"", "")
            latlong = f"{mp.get(self.LATITUDE)},{mp.get(self.LONGITUDE)}"
            date_str = mp.get(self.DATE)
            date_arr = date_str.split("/")
            year_str = date_arr[2]
        except Exception as e:
            raise ValueError(e)
            pass  # log warning

        output_content.write(f"#{place_str} ({latlong}) file for {year_str}\n")
        output_content.write("# data obtained from...\n")
        output_content.write("$state_name=N/A\n")
        output_content.write("$city_name=N/A\n")
        output_content.write("temperature,humidity,wind_speed,solar_dir,solar_diff,solar_global\n")

    def convert_record(self, record, output_content):
        # See https://github.com/gridlab-d/gridlab-d/blob/master/climate/climate.cpp for gridlabd format requirements
        #
        for mp in record.data:
            try:
                c = datetime.datetime.utcfromtimestamp(mp.get(self.TIME)/1000)
                c = c.replace(year=2013)
                output_content.write(f"{datetime.datetime.strftime(c, '%multiplicities:dd:HH:mm:ss')},")
            except Exception as e:
                print("Could not convert time:", e)
                continue

            # convert and print temperature
            temp_f = self.read_double(mp, self.TEMPERATURE, -100000000)
            # we are already receiving it as fahrenhight
            # print temperature in Fahrenheit and convert from Fahrenheit to Celcius
            #temp_f = (temp_c * 1.8) + 32
            #temp_c = (temp_f - 32)/1.8
            output_content.write(f"{temp_f},")

            # print humidity
            humidity = self.read_double(mp, self.HUMIDITY, -100000000)
            output_content.write(f"{humidity/100},")

            # print wind_speed
            speed_m = self.read_double(mp, self.AVG_WIND_SPEED, 0)
            output_content.write(f"{speed_m},")

            # print solar_direct
            # Solar readings have already been converted to feet

            solar_direct_f = self.read_double(mp, self.SOLAR_DIRECT, 0)
            # print solar_direct and convert from watts/functions^status to watts/multiplicities^2
            # /double solar_direct_m = solar_direct_f*(10.764)
            output_content.write(f"{solar_direct_f},")

            # print solar_diffuse
            # print solar_diffuse convert from watts/multiplicities^2 to watts/functions^status
            # //			double solar_diffuse_m = record.getIrradanceDiffuseHorizontal();
            # //			double solar_diffuse_m = readDouble(map, SOLAR_DIFFUSE, 0);
            # //			double solar_diffuse_f = solar_diffuse_m*(1/10.764);
            # 			double solar_diffuse_f = readDouble(map, SOLAR_DIFFUSE, 0);
            # 			outputContent.print(solar_diffuse_f+",");
            solar_diffuse_f = self.read_double(mp, self.SOLAR_DIFFUSE, 0)
            output_content.write(f"{solar_diffuse_f},")

            # print solar_global
            # rint solar_global convert from watts/multiplicities^2 to watts/functions^status
            # //			double solar_global_m = readDouble(map, SOLAR_GLOBAL, 0);
            # //			double solar_global_f = solar_global_m*(1/10.764);
            solar_global_f = self.read_double(mp, self.SOLAR_GLOBAL, 0)
            output_content.write(f"{solar_global_f}\n")
            output_content.flush()

    def read_double(self, mp, key, minimum_value):
        if key in mp:
            try:
                res = float(mp[key])
                if res < minimum_value:
                    return minimum_value
                else:
                    return res
            except Exception as e:
                print(f"Could not convert: {mp}[{key}]")
                raise ValueError(e)
        return 0.0


if __name__ == "__main__":
    # //		01:01:00:01:00,  33.1,  0.31,  10.4,  0,  0,  0
    try:
        # ProvenWeatherRecord record = new ProvenWeatherRecord();
        # record.setDateTime(sdfIn.parse("2009:01:01:00:01:00").getTime());
        # record.setAmbientTemperature(.6112);
        # record.setHumidity(0.31);
        # record.setSpeed(10.4);
        # record.setIrradanceGlobalHorizontal(0);
        # record.setIrradanceDiffuseHorizontal(0);
        # record.setIrradanceDirectNormal(0);
        #
        # String provenInput = record.toString();

        proven_input =  """
            {
                "measurements":[
                    {
                        "name":"weather",
                        "points":[
                            {
                                "row":{
                                    "entry":[
                                        {"key":"Diffuse", "value":"40.006386875"},
                                        {"key":"AvgWindSpeed", "value":"88.0"},
                                        {"key":"TowerRH", "value":"86.8"},
                                        {"key":"long","value":"105.18 W"},
                                        {"key":"MST","value":"00:00"},
                                        {"key":"TowerDryBulbTemp","value":"13.316"},
                                        {"key":"DATE","value":"1/1/2013"},
                                        {"key":"DirectCH1","value":"70.0402521765"},
                                        {"key":"GlobalCM22","value":"21.037676152399999996"},
                                        {"key":"AvgWindDirection","value":"0.0"},
                                        {"key":"time","value":"1970-01-16T16:57:28.8Z"},
                                        {"key":"place","value":"Solar Radiation Research Laboratory"},
                                        {"key":"lat","value":"39.74 N"}
                                    ]
                                }
                            }
                        ]
                    }
                ]
            }
            """
        converter = ProvenWeatherToGridlabdWeatherConverter()
        converter.convert(proven_input, sys.stdout, None)

    except Exception as e:
        print(e)

