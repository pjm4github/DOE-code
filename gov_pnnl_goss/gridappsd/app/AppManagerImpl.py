
import os
import re
import time
import shutil
import zipfile
import threading
import subprocess
from enum import Enum
from datetime import datetime
from pathlib import Path
import zipfile
import io

from enum import Enum
from typing import Any, Dict, Union

from gov_pnnl_goss.core.DataError import DataError
from gov_pnnl_goss.core.DataResponse import DataResponse
from gov_pnnl_goss.core.client.GossClient import JsonSyntaxException, Protocol
from gov_pnnl_goss.core.security.SecurityConfig import SecurityConfig
from gov_pnnl_goss.gridappsd.api.AppManager import AppInstance, AppManager
from gov_pnnl_goss.gridappsd.app.RemoteApplicationHeartbeatMonitor import RemoteApplicationHeartbeatMonitor
from gov_pnnl_goss.gridappsd.dto.AppInfo import AppInfo
from gov_pnnl_goss.gridappsd.dto.LogMessage import ProcessStatus, LogLevel
from gov_pnnl_goss.gridappsd.dto.RemoteApplicationRegistrationResponse import RemoteApplicationRegistrationResponse
from gov_pnnl_goss.gridappsd.dto.RequestAppList import RequestAppList
from gov_pnnl_goss.gridappsd.dto.RequestAppRegister import RequestAppRegister
from gov_pnnl_goss.gridappsd.dto.RequestAppStart import RequestAppStart
from gov_pnnl_goss.gridappsd.dto.ResponseAppInfo import ResponseAppInfo
from gov_pnnl_goss.gridappsd.dto.ResponseAppInstance import ResponseAppInstance
from gov_pnnl_goss.gridappsd.test_gov_pnnl_goss_gridappsd.TestDataApplication import Credentials
from gov_pnnl_goss.gridappsd.utils.GridAppsDConstants import GridAppsDConstants


class AppManagerImpl(AppManager):
    """
     This class implements subset of functionalities for Internal Functions 405
     Simulation Manager and 406 Power System Model Manager. ConfigurationManager
     is responsible for:
           - subscribing to configuration topics and
           - converting configuration message into simulation configuration files and power grid model files.
     @author shar064
    """

    CONFIG_PID = "pnnl.goss.gridappsd"
    CONFIG_FILE_EXT = ".config"

    def __init__(self, log_manager, client_factory):
        self.logger_manager = log_manager
        self.client_factory = client_factory
        self.username = None
        self.client = None
        self.configuration_properties = None
        self.remote_app_monitor = None
        self.apps = {}
        self.app_instances = {}
        self.security_config = SecurityConfig()

    def initialize_app_manager(self, log_manager, client_factory):
        self.logger_manager = log_manager
        self.client_factory = client_factory

    def process(self, process_id: str, event: DataResponse, message: Union[str, Dict[str, Any]]) -> None:
        self.username = event.username

        if self.client is None:
            credentials = Credentials(self.security_config.manager_user, self.security_config.manager_password)
            self.client = self.client_factory.create(Protocol.STOMP, credentials, True)

        reply_destination = event.reply_destination
        destination = event.destination

        if "topic_app_list" in destination:
            request_obj = RequestAppList.parse(message) if isinstance(message, str) else message

            if not request_obj.list_running_only:
                app_response_list = self.list_apps()
                self.client.publish(reply_destination, ResponseAppInfo(app_response_list))
            else:
                app_instance_response_list = (
                    self.list_running_apps(request_obj.app_id)
                    if request_obj.app_id is not None
                    else self.list_running_apps()
                )
                self.client.publish(reply_destination, ResponseAppInstance(app_instance_response_list))
        elif "topic_app_get" in destination:
            app_id = message
            app_info = self.get_app(app_id)
            self.client.publish(reply_destination, app_info)
        elif "topic_app_register_remote" in destination:
            request = message.data if isinstance(message, DataResponse) else message
            app_info = AppInfo.parse(request) if isinstance(request, str) else AppInfo(**request)
            topics = self.register_remote_app(app_info)
            self.client.publish(reply_destination, str(topics))
        elif "topic_app_register" in destination:
            request_obj = RequestAppRegister.parse(message)
            self.register_app(request_obj.app_info, request_obj.app_package)
        elif "topic_app_deregister" in destination:
            app_id = message
            self.deregister_app(app_id)
        elif "topic_app_start" in destination:
            try:
                request_obj = RequestAppStart.parse(message)
            except JsonSyntaxException as ex:
                request_obj = RequestAppStart.parse(event.data)

            instance_id = None
            if request_obj.simulation_id is None:
                instance_id = self.start_app(
                    request_obj.app_id, request_obj.runtime_options, str(process_id)
                )
            else:
                instance_id = self.start_app_for_simulation(
                    request_obj.app_id, request_obj.runtime_options, None
                )

            self.client.publish(reply_destination, instance_id)
        elif "topic_app_stop" in destination:
            app_id = message
            self.stop_app(app_id)
        elif "topic_app_stop_instance" in destination:
            app_instance_id = message
            self.stop_app_instance(app_instance_id)
        else:
            # throw error, destination unrecognized
            self.client.publish(
                reply_destination,
                DataError(f"App manager destination not recognized: {event.destination}"),
            )
    def start(self):
        try:
            self.logger_manager.info(ProcessStatus.RUNNING, None, f"Starting {self.__class__.__name__}")
            self.scan_for_apps()
            self.logger_manager.info(ProcessStatus.RUNNING, None, f"Found {len(self.apps)} applications")
        except Exception as e:
            print(e)

    def register_remote_app(self, app_info):
        if self.remote_app_monitor is None:
            self.remote_app_monitor = RemoteApplicationHeartbeatMonitor(self.logger_manager, self.client)

        print(app_info)

        # Simple routine to make sure appid is unique.
        app_count = 1
        app_id = app_info['id'] + str(app_count)
        while app_id in self.apps:
            app_count += 1
            app_id = app_info['id'] + str(app_count)

        app_id = app_info['id']
        app_info['id'] = app_id
        self.apps[app_id] = app_info

        response = RemoteApplicationRegistrationResponse()
        response['applicationId'] = app_id
        response['errorTopic'] = "Error"
        response['heartbeatTopic'] = "/queue/" + GridAppsDConstants.topic_remoteapp_heartbeat + "." + app_id
        response['startControlTopic'] = "/topic/" + GridAppsDConstants.topic_remoteapp_start + "." + app_id
        response['stopControlTopic'] = "/topic/" + GridAppsDConstants.topic_remoteapp_stop + "." + app_id
        print(response)
        self.remote_app_monitor.add_remote_application(app_id, response)
        return response

    def register_app(self, app_info, app_package):
        print("REGISTER REQUEST RECEIVED")
        app_home_dir = self.get_app_config_directory()

        if not os.path.exists(app_home_dir):
            os.makedirs(app_home_dir)
            if not os.path.exists(app_home_dir):
                raise Exception(
                    f"App home directory does not exist and cannot be created {app_home_dir}")

        print("HOME DIR", app_home_dir)

        new_app_dir = os.path.join(app_home_dir, app_info['id'])

        if os.path.exists(new_app_dir):
            raise Exception(f"App {app_info['id']} already exists")

        try:
            os.makedirs(new_app_dir)

            # Extract zip file into new app dir
            with zipfile.ZipFile(io.BytesIO(app_package), 'r') as zip_in:
                zip_in.extractall(new_app_dir)

            self.write_app_info(app_info)

            # add to apps dictionary
            self.apps[app_info['id']] = app_info
        except Exception as e:
            # Clean up app dir if fails
            os.rmdir(new_app_dir)
            raise e

    def list_apps(self):
        result = list(self.apps.values())
        return result

    def list_running_apps(self, app_id=None):
        if app_id:
            result = []
            for instance_id, instance in self.app_instances.items():
                if instance.app_info.id == app_id:
                    result.append(instance)
            return result
        else:
            result = list(self.app_instances.values())
            return result

    def get_app(self, app_id):
        app_id = app_id.strip()
        return self.apps.get(app_id)

    def get_app_id_for_instance(self, app_instance_id):
        app_instance_id = app_instance_id.strip()
        return self.app_instances.get(app_instance_id).app_info.id

    def de_register_app(self, app_id):
        app_id = app_id.strip()

        # Find and stop any running instances
        self.stop_app(app_id)

        # Remove app from mapping
        if app_id in self.apps:
            del self.apps[app_id]

        # Get app directory from config and remove files for id
        config_dir = self.get_app_config_directory()
        app_dir = os.path.join(config_dir, app_id)

        try:
            # Use shutil to remove the directory and its contents
            shutil.rmtree(app_dir)

            # Remove the app info file
            app_info_file = os.path.join(config_dir, app_id + self.CONFIG_FILE_EXT)
            if os.path.exists(app_info_file):
                os.remove(app_info_file)

        except Exception as e:
            print(f"Error while de-registering app {app_id}: {str(e)}")

    def start_app(self, app_id, runtime_options, request_id):
        return self.start_app_for_simulation(app_id, runtime_options, None)

    def start_app_for_simulation(self, app_id, runtime_options, simulation_context):
        simulation_id = None
        if simulation_context:
            simulation_id = str(simulation_context.get("simulation_id"))

        app_id = app_id.strip()
        instance_id = app_id + "-" + str(int(datetime.now().timestamp()))

        app_info = self.apps.get(app_id)
        if not app_info:
            raise RuntimeError("App not found: " + app_id)

        if not app_info.is_multiple_instances() and self.list_running_apps(app_id):
            raise RuntimeError(
                "App is already running and multiple instances are not allowed: " + app_id)

        app_directory = os.path.join(self.get_app_config_directory(), app_id)
        process = None

        if app_info.get_type() == "REMOTE":
            commands = self.build_command_string(runtime_options, simulation_context, app_info)
            args = " ".join(commands)
            self.remote_app_monitor.start_remote_application(app_info.get_id(), args)
        elif app_info.get_type() == "PYTHON":
            commands = self.build_command_string(runtime_options, simulation_context, app_info)
            commands.insert(0, "python")
            process_app_builder = subprocess.Popen(commands, cwd=app_directory, stdout=subprocess.PIPE,
                                                   stderr=subprocess.STDOUT)
            log_message = "Starting app with command " + " ".join(commands)
            self.logger.info(ProcessStatus.RUNNING, simulation_id, log_message)
            process = process_app_builder
        elif app_info.get_type() == "JAVA":
            pass  # Add Java specific code here if needed
        elif app_info.get_type() == "WEB":
            pass  # Add web app specific code here if needed
        else:
            raise RuntimeError("Type not recognized: " + app_info.get_type())

        app_instance = AppInstance(instance_id, app_info, runtime_options, simulation_id, simulation_id, process)
        app_instance.set_app_info(app_info)
        if app_info.get_type() != "REMOTE":
            self.watch(app_instance, simulation_id)

        self.app_instances[instance_id] = app_instance

        return instance_id

    def build_command_string(self, runtime_options, simulation_context, app_info):
        commands = [app_info.get_execution_path()]

        # Check if static args contain any replacement values
        static_args_list = app_info.get_options()
        if static_args_list:
            for static_arg in static_args_list:
                if static_arg:
                    if "(" in static_arg:
                        replace_args = re.findall(r'\((.*?)\)', static_arg)
                        for args in replace_args:
                            if args in simulation_context:
                                static_arg = static_arg.replace(f"({args})", str(simulation_context[args]))
                    commands.append(static_arg)

        if runtime_options and not runtime_options.isspace():
            run_time_string = runtime_options.replace(" ", "").replace("\n", "")
            commands.append(run_time_string)

        return commands

    def stop_app(self, app_id):
        app_id = app_id.strip()
        for instance in self.list_running_apps(app_id):
            app_info = instance.get_app_info()
            if app_info.get_id() == app_id:
                if app_info.get_type() == AppInfo.AppType.REMOTE:
                    self.remote_app_monitor.stop_remote_application(app_id)
                else:
                    self.stop_app_instance(instance.get_instance_id())

    def stop_app_instance(self, instance_id):
        instance_id = instance_id.strip()
        instance = self.app_instances.get(instance_id)
        if instance.get_app_info().get_type() == AppInfo.AppType.REMOTE:
            self.remote_app_monitor.stop_remote_application(instance.get_app_info().get_id())
        else:
            instance.get_process().terminate()
        self.app_instances.pop(instance_id)

    def updated(self, config):
        with self.lock:
            self.configuration_properties = config

    def get_configuration_property(self, key):
        if self.configuration_properties is not None:
            value = self.configuration_properties.get(key)
            if value is not None:
                return str(value)
        return None

    def get_app_config_directory(self):
        config_dir_str = self.get_configuration_property(GridAppsDConstants.APPLICATIONS_PATH)
        if config_dir_str is None:
            config_dir_str = "applications"

        config_dir = os.path.abspath(config_dir_str)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
            if not os.path.exists(config_dir):
                raise RuntimeError(f"Applications directory {config_dir} does not exist and cannot be created.")

        return config_dir

    def parse_app_info(self, app_config_file):
        app_info = None

        if not os.path.exists(app_config_file):
            raise RuntimeError(f"App config file does not exist: {app_config_file}")

        try:
            with open(app_config_file, "r") as file:
                app_config_str = file.read()
                app_info = AppInfo.parse(app_config_str)
        except IOError as e:
            self.logger.error(ProcessStatus.RUNNING, None, f"Error while reading app config file: {e}")

        return app_info

    def write_app_info(self, app_info):
        app_config_directory = self.get_app_config_directory()

        conf_file = os.path.join(app_config_directory, app_info.get_id() + self.CONFIG_FILE_EXT)
        try:
            with open(conf_file, "w") as file:
                file.write(app_info.to_"")
        except IOError as e:
            self.logger.error(ProcessStatus.ERROR, None, f"Error while writing app config file: {e}")

    BUFFER_SIZE = 4096

    def extract_file(self, zip_in, file_path):
        with open(file_path, "wb") as bos:
            bytes_in = zip_in.read(self.BUFFER_SIZE)
            while bytes_in:
                bos.write(bytes_in)
                bytes_in = zip_in.read(self.BUFFER_SIZE)

    def watch(self, app_instance, simulation_id):
        print("WATCHING " + app_instance.get_instance_id())

        def run_thread():
            try:
                process = app_instance.get_process()
                with process.stdout:
                    for line in iter(process.stdout.readline, b''):
                        log_message = line.decode("utf-8").strip()
                        self.logger.log_message_from_source(ProcessStatus.RUNNING, simulation_id, log_message, app_instance.get_instance_id(), LogLevel.DEBUG)
            except Exception as e:
                e_message = str(e)
                print(e)
                self.log_manager.log_message_from_source(ProcessStatus.ERROR, simulation_id, e_message, app_instance.get_instance_id(), LogLevel.ERROR)

        thread = threading.Thread(target=run_thread)
        thread.start()

    def split_options_string(self, options_str):
        # First replace all \" with a string that won't get parsed
        options_str = options_str.replace('\\"', 'ESC_QUOTE')
        options_list = []

        # Use regular expression to split the options string
        pattern = r'([^\s"]\S*|".+?")\s*'
        matches = re.finditer(pattern, options_str)

        for match in matches:
            group_str = match.group(1)
            # Revert back all ESC_QUOTE to \"
            group_str = group_str.replace('ESC_QUOTE', '\\"')
            options_list.append(group_str)

        return options_list


    # def scan_for_apps(self):
    #     app_config_dir = self.get_app_config_directory()
    #     app_config_files = [functions for functions in os.listdir(app_config_dir) if functions.endswith(self.CONFIG_FILE_EXT)]
    #     for app_config_file in app_config_files:
    #         app_info = self.parse_app_info(os.path.join(app_config_dir, app_config_file))
    #         self.apps[app_info.id] = app_info
    #
    # def deregister_app(self, id: str):
    #     # Implement deregisterApp logic here
    #     pass
    #
