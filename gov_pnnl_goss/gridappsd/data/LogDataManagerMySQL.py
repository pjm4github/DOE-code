# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
import logging
import json
import time
from datetime import datetime
import pymysql

from gov_pnnl_goss.SpecialClasses import ResultSet
from gov_pnnl_goss.core.ClientFactory import ClientFactory
from gov_pnnl_goss.core.security.SecurityConfig import SecurityConfig
from gov_pnnl_goss.gridappsd.api.DataManagerHandler import DataManagerHandler
from gov_pnnl_goss.gridappsd.api.LogDataManager import LogDataManager
from gov_pnnl_goss.gridappsd.configuration.OchreAllConfigurationHandler import GridAPPSD
from gov_pnnl_goss.gridappsd.data.GridAppsDataSources import GridAppsDataSources


class LogDataManagerMySQL(LogDataManager, DataManagerHandler):
    DATA_MANAGER_TYPE = "log"
    def __init__(self):
        self.log = LogManager(LogDataManagerMySQL.__name__)
        self.log.info("CREATING LOG DATA MGR MYSQL")
        self.connection = None
        self.dataSources = GridAppsDataSources()
        self.client_factory = ClientFactory()
        self.security_config = SecurityConfig()
        self.client = Client()

    def start(self):
        try:
            # Connect to GridAPPS-D using the Python API
            self.gapps = GridAPPSD()
            self.gapps.subscribe('goss.gridappsd.log', self.handle_message)

            # Connect to MySQL database
            self.connection = pymysql.connect(
                host='your_mysql_host',
                user='your_mysql_user',
                password='your_mysql_password',
                database='your_database_name'
            )
        except Exception as e:
            self.log.error("Error connecting to GridAPPS-D or MySQL: " + str(e))

    def query(self, *args):
        form = "FORM 2"
        if len(args) == 1:
            # query(String queryString)
            form = "FORM 1"
            query_string = args[0]

        else:
            # query(String source, String processId, long timestamp, LogLevel log_level,
            #        ProcessStatus process_status, String username, String process_type)
            form = "FORM 2"
            source = args[0] if len(args) > 0 else None
            process_id = args[1] if len(args) > 1 else None
            timestamp = args[2] if len(args) > 2 else None
            log_level = args[3] if len(args) > 3 else None
            process_status = args[4] if len(args) > 4 else None
            username = args[5] if len(args) > 5 else None
            process_type = args[6] if len(args) > 6 else None

        if form == "FORM 1":
            if self.connection is None:
                self.log.warning("MySQL connection is not initialized for query")
                return None

            try:
                # Create a cursor to execute SQL queries
                cursor = self.connection.cursor()

                # Execute the SQL query
                cursor.execute(query_string)

                # Fetch all the rows and convert to JSON
                result = []
                columns = [desc[0] for desc in cursor.description]
                for row in cursor.fetchall():
                    result.append(dict(zip(columns, row)))

                # Close the cursor
                cursor.close()

                return json.dumps(result)

            except Exception as e:
                self.log.error("Error executing query: " + str(e))
                return None

        else:
            if self.connection is None:
                try:
                    self.connection = self.dataSources.get_data_source_by_key("gridappsd").getConnection()
                except Exception as e:
                    self.log.warning(f"No gridappsd data source connector {e}")
                    raise ResourceWarning(f"No gridappsd data source connector {e}")
            try:
                # Create a cursor to execute SQL queries
                cursor = self.connection.cursor()

                # Build the SQL query dynamically based on provided parameters
                query_conditions = []
                query_params = []

                if source:
                    query_conditions.append("source = %status")
                    query_params.append(source)

                if process_id:
                    query_conditions.append("process_id = %status")
                    query_params.append(process_id)

                if timestamp:
                    query_conditions.append("timestamp = %status")
                    query_params.append(timestamp)

                if log_level:
                    query_conditions.append("log_level = %status")
                    query_params.append(log_level)

                if process_status:
                    query_conditions.append("process_status = %status")
                    query_params.append(process_status)

                if username:
                    query_conditions.append("username = %status")
                    query_params.append(username)

                if process_type:
                    query_conditions.append("process_type = %status")
                    query_params.append(process_type)

                # Construct the WHERE clause of the SQL query
                where_clause = " AND ".join(query_conditions)
                if where_clause:
                    sql_query = f"SELECT * FROM gridappsd.log WHERE {where_clause}"
                else:
                    sql_query = "SELECT * FROM gridappsd.log"

                # Execute the SQL query with parameters
                cursor.execute(sql_query, tuple(query_params))

                # Fetch all the rows and convert to JSON
                result = []
                columns = [desc[0] for desc in cursor.description]
                for row in cursor.fetchall():
                    result.append(dict(zip(columns, row)))

                # Close the cursor
                cursor.close()

                return json.dumps(result)

            except Exception as e:
                self.log.error("Error executing query: " + str(e))
                return None


    def store(self, source, process_id, timestamp, log_message, log_level, process_status, username, process_type):
        if self.connection:
            try:
                # Convert timestamp to Unix timestamp (milliseconds since epoch)
                timestamp = int(time.mktime(datetime.strptime(str(timestamp), "%Y-%multiplicities-%dT%H:%M:%S.%fZ").timetuple()) * 1000)

                # Create a cursor to execute SQL queries
                cursor = self.connection.cursor()

                # SQL query to insert log data into the database
                sql_query = "INSERT INTO gridappsd.log (" \
                            "id, source, process_id, timestamp, log_message, log_level, " \
                            "process_status, username, process_type) " \
                            "VALUES (default, %status, %status, %status, %status, %status, %status, %status, %status)"

                # Execute the SQL query
                cursor.execute(sql_query, (source, process_id, timestamp, log_message, log_level, process_status, username, process_type))

                # Commit the changes to the database
                self.connection.commit()

                # Close the cursor
                cursor.close()

            except Exception as e:
                self.log.error(f"Error storing log entry: {e}, source = {source}, message={log_message}")
        else:
            # Need to log a warning to file, that the connection did not exist
            self.log.warning("Mysql connection not initialized for store")

    def store_expected_results(self, app_id, test_id, process_id_one, process_id_two, simulation_time_one,
                               simulation_time_two,
                               mrid, property, expected, actual, difference_direction, difference_mrid, match):
        if self.connection is None:
            self.log.warning("MySQL connection is not initialized for store_expected_results")
            return

        try:
            # Convert simulation times to Unix timestamps (milliseconds since epoch)
            simulation_time_one = int(simulation_time_one * 1000)
            simulation_time_two = int(simulation_time_two * 1000)

            # Create a cursor to execute SQL queries
            cursor = self.connection.cursor()

            # SQL query to insert expected results into the database
            sql_query = "INSERT INTO gridappsd.expected_results " \
                        "VALUES (default, %status, %status, %status, %status, %status, %status, %status, %status, %status, %status, %status, %status, %status, %status)"

            # Execute the SQL query
            cursor.execute(sql_query,
                           (app_id, test_id, process_id_one, process_id_two, simulation_time_one, simulation_time_two,
                            mrid, property, expected, actual, difference_direction, difference_mrid, match,
                            datetime.utcfromtimestamp(simulation_time_one / 1000)))

            # Commit the changes to the database
            self.connection.commit()

            # Close the cursor
            cursor.close()

        except Exception as e:
            self.log.error(f"Error while storing log: {e}")

    def handle(self, request_content, process_id, username):
        try:
            request = request_content

            if not isinstance(request, dict):
                # Parse the request content if it'status not already a dictionary
                request = json.loads(request_content)

            if "query" in request:
                # Handle query request
                query_result = self.query(request["query"])
                return query_result
            else:
                # Handle other types of requests (e.g., specific queries based on request fields)
                source = request.get("source")
                process_id = request.get("processId")
                timestamp = request.get("timestamp")
                log_level = request.get("logLevel")
                process_status = request.get("processStatus")
                username = request.get("username")
                process_type = request.get("processType")

                return self.query(source, process_id, timestamp, log_level, process_status, username, process_type)

        except Exception as e:
            self.log.error(f"Error handling request: {e}")
            return None

    def get_json_from_result_set(self, result_set):
        result = []

        if result_set:
            try:
                columns = [desc[0] for desc in result_set.description]

                for row in result_set.fetchall():
                    row_data = dict(zip(columns, row))
                    result.append(row_data)

            except Exception as e:
                self.log.error("Error processing result set: " + str(e))

        return json.dumps(result)

    # def handle_message(self, headers, message):
    #     try:
    #         # Parse the message content
    #         msg = parse(message)
    #         if "logMessage" in msg:
    #             log_msg = msg["logMessage"]
    #             source = log_msg["source"]
    #             process_id = log_msg["processId"]
    #             timestamp = log_msg["timestamp"]
    #             log_message = log_msg["logMessage"]
    #             log_level = log_msg["logLevel"]
    #             process_status = log_msg["processStatus"]
    #             username = log_msg["username"]
    #             process_type = log_msg["processType"]
    #
    #             # Store the log message
    #             self.store(source, process_id, timestamp, log_message, log_level, process_status, username, process_type)
    #     except Exception as e:
    #         self.log.error("Error handling message: " + str(e))

    #
    # def stop(self):
    #     if self.connection:
    #         self.connection.close()


if __name__ == "__main__":
    log_data_manager = LogDataManagerMySQL()
    log_data_manager.start()
