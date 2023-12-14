# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
from gov_pnnl_goss.SpecialClasses import Gson, RuntimeException
from gov_pnnl_goss.core.Event import Event


class CommOutage(Event):
    serial_version_UID = 6374753495662389807

    def __init__(self):
        super().__init__()
        self.__all_output_outage = False
        self.__all_input_outage = False
        self.__input_outage_list = []
        self.__output_outage_list = []

    def is_all_output_outage(self):
        return self.__all_output_outage

    def set_all_output_outage(self, all_output_outage):
        self.__all_output_outage = all_output_outage

    def is_all_input_outage(self):
        return self.__all_input_outage

    def set_all_input_outage(self, all_input_outage):
        self.__all_input_outage = all_input_outage

    def get_input_outage_list(self):
        return self.__input_outage_list

    def set_input_outage_list(self, input_outage_list):
        self.__input_outage_list = input_outage_list

    def get_output_outage_list(self):
        return self.__output_outage_list

    def set_output_outage_list(self, output_outage_list):
        self.__output_outage_list = output_outage_list

    @staticmethod
    def parse(json_string):
        gson = Gson()
        obj = gson.fromJson(json_string, CommOutage)
        if obj.occuredDateTime == 0 or obj.stopDateTime == 0:
            raise RuntimeException("Expected attribute timeInitiated or timeCleared is not found")
        return obj
