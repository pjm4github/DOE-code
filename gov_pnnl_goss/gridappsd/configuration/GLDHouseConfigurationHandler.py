import os

from gov_pnnl_goss.gridappsd.dto.LogMessage import ProcessStatus


class GLDHouseConfigurationHandler:
    def __init__(self, log_manager, data_manager, powergrid_model_manager):
        self.logger = log_manager
        self.dataManager = data_manager
        self.powergridModelManager = powergrid_model_manager

    def generate_config(self, parameters, out, process_id, username):
        self.logger.info(ProcessStatus.RUNNING, process_id, "Generating GridLAB-D house configuration files")

        directory = parameters.get(self.DIRECTORY, None)
        if directory is None or directory.strip() == "":
            self.logger.error(ProcessStatus.ERROR, process_id, "No " + self.DIRECTORY + " parameter provided")
            raise Exception("Missing parameter " + self.DIRECTORY)

        houses = parameters.get(self.HOUSES, None)
        if houses is None or houses.strip() == "":
            self.logger.error(ProcessStatus.ERROR, process_id, "No " + self.HOUSES + " parameter provided")
            raise Exception("Missing parameter " + self.HOUSES)

        house_list = houses.split(',')

        housing_type = parameters.get(self.HOUSINGTYPE, "")
        hvac_system = parameters.get(self.HVACSYSTEM, "")
        hvac_system_capacity = parameters.get(self.HVACSYSTEMCAPACITY, "")
        water_heater_type = parameters.get(self.WATERHEATERTYPE, "")
        water_heater_capacity = parameters.get(self.WATERHEATERCAPACITY, "")
        refrigerator_type = parameters.get(self.REFRIGERATORTYPE, "")
        refrigerator_capacity = parameters.get(self.REFRIGERATORCAPACITY, "")

        if len(house_list) == 0:
            self.logger.error(ProcessStatus.ERROR, process_id, "No " + self.HOUSES + " parameter provided")
            raise Exception("Missing parameter " + self.HOUSES)

        housing_units = parameters.get(self.HOUSINGUNITS, 1)
        bedrooms = parameters.get(self.BEDROOMS, 3)
        baths = parameters.get(self.BATHS, 2)
        sqft = parameters.get(self.SQFT, 1500)
        electrification_pct = parameters.get(self.ELECTRIFICATIONPCT, 100)
        cooling_pct = parameters.get(self.COOLINGPCT, 100)
        heating_pct = parameters.get(self.HEATINGPCT, 100)
        hotwater_pct = parameters.get(self.HOTWATERPCT, 100)

        for house in house_list:
            house_file_name = house + ".glm"
            house_file_path = os.path.join(directory, house_file_name)

            with open(house_file_path, 'w') as house_file:
                house_file.write("module residential {\n")
                house_file.write("  module house {\n")
                house_file.write("    name " + house + ";\n")
                house_file.write("    num_units " + str(housing_units) + ";\n")
                house_file.write("    num_bedrooms " + str(bedrooms) + ";\n")
                house_file.write("    num_baths " + str(baths) + ";\n")
                house_file.write("    floor_area " + str(sqft) + ";\n")
                house_file.write("    household_min_temperature 18;\n")
                house_file.write("    household_max_temperature 30;\n")
                house_file.write("    thermostat_deadband 2.0;\n")

                if housing_type:
                    house_file.write("    housing_type " + housing_type + ";\n")

                if hvac_system:
                    house_file.write("    hvac_system " + hvac_system + ";\n")

                if hvac_system_capacity:
                    house_file.write("    hvac_system_capacity " + hvac_system_capacity + ";\n")

                if water_heater_type:
                    house_file.write("    water_heater_type " + water_heater_type + ";\n")

                if water_heater_capacity:
                    house_file.write("    water_heater_capacity " + water_heater_capacity + ";\n")

                if refrigerator_type:
                    house_file.write("    refrigerator_type " + refrigerator_type + ";\n")

                if refrigerator_capacity:
                    house_file.write("    refrigerator_capacity " + refrigerator_capacity + ";\n")

                house_file.write("    electrification_pct " + str(electrification_pct) + ";\n")
                house_file.write("    cooling_pct " + str(cooling_pct) + ";\n")
                house_file.write("    heating_pct " + str(heating_pct) + ";\n")
                house_file.write("    hotwater_pct " + str(hotwater_pct) + ";\n")

                house_file.write("  }\n")
                house_file.write("}\n")

        self.logger.info(ProcessStatus.RUNNING, process_id, "Completed generating GridLAB-D house configuration files")
