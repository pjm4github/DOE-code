from gov_pnnl_goss.gridlab.gldcore.Globals import TECHNOLOGYREADINESSLEVEL
from gov_pnnl_goss.gridlab.gldcore.GridLabD import gl_register_class, gl_publish_variable, gl_error, PADDR
from gov_pnnl_goss.gridlab.gldcore.PropertyHeader import PropertyType


# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
# weather.py


def create_weather(obj, parent):
    return 1  # don't want it to get called, but better to have it not be fatal


def sync_weather(obj, t0):
    return None  # really doesn't do anything


# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106 python
class Weather:
    owner_class = 0

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
        if self.owner_class is None:
            owner_class = gl_register_class(module, "weather", Weather.__sizeof__(), 0)
            if owner_class is None:
                raise Exception("unable to register class weather")
            else:
                owner_class.trl = TECHNOLOGYREADINESSLEVEL.TRL_CONCEPT
            if gl_publish_variable(owner_class,
                                   PropertyType.PT_double, "temperature[degF]", PADDR(self.temperature),
                                   PropertyType.PT_double, "humidity[%]", PADDR(self.humidity),
                                   PropertyType.PT_double, "solar_dir[W/sf]", PADDR(self.solar_dir),
                                   PropertyType.PT_double, "solar_direct[W/sf]", PADDR(self.solar_dir),
                                   PropertyType.PT_double, "solar_diff[W/sf]", PADDR(self.solar_diff),
                                   PropertyType.PT_double, "solar_diffuse[W/sf]", PADDR(self.solar_diff),
                                   PropertyType.PT_double, "solar_global[W/sf]", PADDR(self.solar_global),
                                   PropertyType.PT_double, "global_horizontal_extra[W/sf]", PADDR(self.global_horizontal_extra),
                                   PropertyType.PT_double, "wind_speed[mph]", PADDR(self.wind_speed),
                                   PropertyType.PT_double, "wind_dir[deg]", PADDR(self.wind_dir),
                                   PropertyType.PT_double, "opq_sky_cov[pu]", PADDR(self.opq_sky_cov),
                                   PropertyType.PT_double, "tot_sky_cov[pu]", PADDR(self.tot_sky_cov),
                                   PropertyType.PT_double, "rainfall[in/h]", PADDR(self.rainfall),
                                   PropertyType.PT_double, "snowdepth[in]", PADDR(self.snowdepth),
                                   PropertyType.PT_double, "pressure[mbar]", PADDR(self.pressure),
                                   PropertyType.PT_int16, "month", PADDR(self.month),
                                   PropertyType.PT_int16, "day", PADDR(self.day),
                                   PropertyType.PT_int16, "hour", PADDR(self.hour),
                                   PropertyType.PT_int16, "minute", PADDR(self.minute),
                                   PropertyType.PT_int16, "second", PADDR(self.second),
                                   None) < 1:
                raise Exception("unable to publish properties in" + __file__)
