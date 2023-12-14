from gov_pnnl_goss.gridlab.climate.CsvReader import PADDR
from gov_pnnl_goss.gridlab.gldcore.Globals import TECHNOLOGYREADINESSLEVEL
from gov_pnnl_goss.gridlab.gldcore.GridLabD import gl_register_class, gl_publish_variable, gl_error
from gov_pnnl_goss.gridlab.gldcore.Property import PROPERTYTYPE


# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
# weather.py


def create_weather(obj, parent):
    return 1  # don't want it to get called, but better to have it not be fatal


def sync_weather(obj, t0):
    return None  # really doesn't do anything


# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106 python
class Weather:
    oclass = 0

    def __init__(self, module=None):
        self.day = 0
        self.global_horizontal_extra = 0.0
        self.hour = 0
        self.humidity = 0.0
        self.minute = 0
        self.month = 0
        self.opq_sky_cov = 0.0
        self.pressure = 0.0
        self.rainfall = 0.0
        self.second = 0
        self.snowdepth = 0.0
        self.solar_diff = 0.0
        self.solar_dir = 0.0
        self.solar_global = 0.0
        self.temperature = 0.0
        self.tot_sky_cov = 0.0
        self.wind_dir = 0.0
        self.wind_speed = 0.0
        if self.oclass is None:
            oclass = gl_register_class(module, "weather", Weather.__sizeof__(), 0)
            if oclass is None:
                raise Exception("unable to register class weather")
            else:
                oclass.trl = TECHNOLOGYREADINESSLEVEL.TRL_CONCEPT
            if gl_publish_variable(oclass,
                PROPERTYTYPE.PT_double, "temperature[degF]", PADDR(self.temperature),
                PROPERTYTYPE.PT_double, "humidity[%]", PADDR(self.humidity),
                PROPERTYTYPE.PT_double, "solar_dir[W/sf]", PADDR(self.solar_dir),
                PROPERTYTYPE.PT_double, "solar_direct[W/sf]", PADDR(self.solar_dir),
                PROPERTYTYPE.PT_double, "solar_diff[W/sf]", PADDR(self.solar_diff),
                PROPERTYTYPE.PT_double, "solar_diffuse[W/sf]", PADDR(self.solar_diff),
                PROPERTYTYPE.PT_double, "solar_global[W/sf]", PADDR(self.solar_global),
                PROPERTYTYPE.PT_double, "global_horizontal_extra[W/sf]", PADDR(self.global_horizontal_extra),
                PROPERTYTYPE.PT_double, "wind_speed[mph]", PADDR(self.wind_speed),
                PROPERTYTYPE.PT_double, "wind_dir[deg]", PADDR(self.wind_dir),
                PROPERTYTYPE.PT_double, "opq_sky_cov[pu]", PADDR(self.opq_sky_cov),
                PROPERTYTYPE.PT_double, "tot_sky_cov[pu]", PADDR(self.tot_sky_cov),
                PROPERTYTYPE.PT_double, "rainfall[in/h]", PADDR(self.rainfall),
                PROPERTYTYPE.PT_double, "snowdepth[in]", PADDR(self.snowdepth),
                PROPERTYTYPE.PT_double, "pressure[mbar]", PADDR(self.pressure),
                PROPERTYTYPE.PT_int16, "month", PADDR(self.month),
                PROPERTYTYPE.PT_int16, "day", PADDR(self.day),
                PROPERTYTYPE.PT_int16, "hour", PADDR(self.hour),
                PROPERTYTYPE.PT_int16, "minute", PADDR(self.minute),
                PROPERTYTYPE.PT_int16, "second", PADDR(self.second),
                None) < 1:
                raise Exception("unable to publish properties in" + __file__)
