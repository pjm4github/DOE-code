import json

class ModelCreationConfig:
    def __init__(self):
        self.load_scaling_factor = 1
        self.triplex = 'y'
        self.encoding = 'u'
        self.system_frequency = 60
        self.voltage_multiplier = 1
        self.power_unit_conversion = 1
        self.unique_names = 'y'
        self.schedule_name = None
        self.z_fraction = 0
        self.i_fraction = 1
        self.p_fraction = 0
        self.randomize_zipload_fractions = False
        self.use_houses = False
        self.model_state = None
        self.separated_loads_file = None

    def get_load_scaling_factor(self):
        return self.load_scaling_factor

    def set_load_scaling_factor(self, load_scaling_factor):
        self.load_scaling_factor = load_scaling_factor

    def get_triplex(self):
        return self.triplex

    def set_triplex(self, triplex):
        self.triplex = triplex

    def get_encoding(self):
        return self.encoding

    def set_encoding(self, encoding):
        self.encoding = encoding

    def get_system_frequency(self):
        return self.system_frequency

    def set_system_frequency(self, system_frequency):
        self.system_frequency = system_frequency

    def get_voltage_multiplier(self):
        return self.voltage_multiplier

    def set_voltage_multiplier(self, voltage_multiplier):
        self.voltage_multiplier = voltage_multiplier

    def get_power_unit_conversion(self):
        return self.power_unit_conversion

    def set_power_unit_conversion(self, power_unit_conversion):
        self.power_unit_conversion = power_unit_conversion

    def get_unique_names(self):
        return self.unique_names

    def set_unique_names(self, unique_names):
        self.unique_names = unique_names

    def get_schedule_name(self):
        return self.schedule_name

    def set_schedule_name(self, schedule_name):
        self.schedule_name = schedule_name

    def get_z_fraction(self):
        return self.z_fraction

    def set_z_fraction(self, z_fraction):
        self.z_fraction = z_fraction

    def get_i_fraction(self):
        return self.i_fraction

    def set_i_fraction(self, i_fraction):
        self.i_fraction = i_fraction

    def get_p_fraction(self):
        return self.p_fraction

    def set_p_fraction(self, p_fraction):
        self.p_fraction = p_fraction

    def is_randomize_zipload_fractions(self):
        return self.randomize_zipload_fractions

    def set_randomize_zipload_fractions(self, randomize_zipload_fractions):
        self.randomize_zipload_fractions = randomize_zipload_fractions

    def is_use_houses(self):
        return self.use_houses

    def set_use_houses(self, use_houses):
        self.use_houses = use_houses

    def __str__(self):
        return json.dumps(self.__dict__)

    def get_model_state(self):
        return self.model_state

    def set_model_state(self, model_state):
        self.model_state = model_state

    def get_separated_loads_file(self):
        return self.separated_loads_file

    def set_separated_loads_file(self, file_name):
        self.separated_loads_file = file_name

    @staticmethod
    def parse(json_string):
        obj = json.loads(json_string)
        if obj['schedule_name'] is None:
            raise ValueError("Expected attribute schedule_name not found")
        return obj
