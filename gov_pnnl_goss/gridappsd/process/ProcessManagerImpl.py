import random
import threading
from datetime import datetime
from queue import Queue
from threading import Thread, Lock

from gov_pnnl_goss.SpecialClasses import UsernamePasswordCredentials
from gov_pnnl_goss.core.client.GossClient import Protocol

from gov_pnnl_goss.gridappsd.api import  AppManager, ConfigurationManager, DataManager, FieldBusManager, \
           LogManager, ProcessManager, RoleManager, ServiceManager, SimulationManager, TestManager

from gov_pnnl_goss.gridappsd.dto.LogMessage import LogLevel, LogMessage, ProcessStatus
from gov_pnnl_goss.gridappsd.test_gov_pnnl_goss_gridappsd.ProcessEventTests import ProcessEvent
from gov_pnnl_goss.gridappsd.utils.GridAppsDConstants import GridAppsDConstants
from gov_pnnl_goss.gridappsd.process.ProcessNewSimulationRequest import ProcessNewSimulationRequest


class AtomicInteger:
    def __init__(self, initial_value=0):
        self._value = initial_value
        self._lock = Lock()

    def get(self):
        with self._lock:
            return self._value

    def set(self, new_value):
        with self._lock:
            self._value = new_value

    def get_and_set(self, new_value):
        # Atomically sets the value of the AtomicInteger to the specified newValue and returns the previous value.
        with self._lock:
            old_value = self._value
            self._value = new_value
            return old_value

    def __add__(self, other):
        with self._lock:
            return self._value + other

    def __sub__(self, other):
        with self._lock:
            return self._value - other

    def increment_and_get(self):
        # Atomically increments the value of the AtomicInteger by 1 and returns the updated value.
        with self._lock:
            self._value += 1
            return self._value

    def decrement_and_get(self):
        # Atomically decrements the value of the AtomicInteger by 1 and returns the updated value.
        with self._lock:
            self._value -= 1
            return self._value

    def get_and_increment(self):
        # Atomically increments the value of the AtomicInteger by 1 and returns the previous value.
        with self._lock:
            old_value = self._value
            self._value += 1
            return old_value

    def get_and_decrement(self):
        # Atomically decrements the value of the AtomicInteger by 1 and returns the previous value.
        with self._lock:
            old_value = self._value
            self._value -= 1
            return old_value

    def add_and_get(self, delta):
        # Atomically adds the specified delta to the value of the AtomicInteger and returns the updated value.
        with self._lock:
            self._value += delta
            return self._value

    def get_and_add(self, delta):
        # Atomically adds the specified delta to the value of the AtomicInteger and returns the previous value.
        with self._lock:
            old_value = self._value
            self._value += delta
            return old_value

    def compare_and_set(self, expect, update):
        # Atomically updates the value of the AtomicInteger to the update value
        # if the current value is equal to the expect value.
        # Returns true if the update is successful; otherwise, returns false.
        with self._lock:
            if self._value == expect:
                self._value = update
                return True
            return False

    def weak_compare_and_set(self, expect, update):
        # A variant of compare_and_set, but with weaker guarantees
        with self._lock:
            if self._value == expect:
                self._value = update
                return True
            return False

    def accumulate_and_get(self, x, accumulator_function):
        # Atomically updates the value of the AtomicInteger using the specified accumulator
        # function and returns the updated value. The accumulator function takes two arguments: the current value and x.
        with self._lock:
            self._value = accumulator_function(self._value, x)
            return self._value

    def get_and_accumulate(self, x, accumulator_function):
        # Atomically updates the value of the AtomicInteger using the specified accumulator
        # function and returns the previous value.
        with self._lock:
            old_value = self._value
            self._value = accumulator_function(self._value, x)
            return old_value

    def __str__(self):
        return str(self.get())


class ProcessManagerImpl(ProcessManager):

    def __init__(self):
        self.new_simulation_process = None
        self.simulation_ports = {}
        self.rand_port = random.Random()
        self.queue = Queue()

    def set_client_factory(self, clientFactory):
        self.client_factory = clientFactory

    def set_configuration_manager(self, configurationManager):
        self.configuration_manager = configurationManager

    def set_simulation_manager(self, simulationManager):
        self.simulation_manager = simulationManager

    def set_app_manager(self, appManager):
        self.app_manager = appManager

    def set_log_manager(self, logManager):
        self.logger = logManager

    def set_service_manager(self, serviceManager):
        self.service_manager = serviceManager

    def set_security_config(self, securityConfig):
        self.security_config = securityConfig

    def set_data_manager(self, dataManager):
        self.data_manager = dataManager

    def set_test_manager(self, testManager):
        self.test_manager = testManager

    def set_field_bus_manager(self, fieldBusManager):
        self.field_bus_manager = fieldBusManager

    def start(self):
        logMessageObj = LogMessage()
        try:
            credentials = UsernamePasswordCredentials(
                self.security_config.getManagerUser(),
                self.security_config.getManagerPassword(),
            )

            client = self.client_factory.create(Protocol.STOMP, credentials, True)

            logMessageObj.setLogLevel(LogLevel.DEBUG)
            logMessageObj.setSource(self.getClass().getName())
            logMessageObj.setProcessStatus(ProcessStatus.RUNNING)
            logMessageObj.setStoreToDb(True)
            logMessageObj.setLogMessage(f"Starting {self.getClass().getName()}")

            client.publish(GridAppsDConstants.topic_platformLog, logMessageObj)

            if self.new_simulation_process is None:
                self.new_simulation_process = ProcessNewSimulationRequest(
                    self.logger, self.security_config
                )

            logMessageObj.setTimestamp(int(datetime.now().timestamp() * 1000))
            logMessageObj.setLogMessage(f"Starting {self.getClass().getName()}")
            client.publish(GridAppsDConstants.topic_platformLog, logMessageObj)

            client.subscribe(
                GridAppsDConstants.topic_process_prefix + ".>",
                ProcessEvent(
                    self,
                    client,
                    self.new_simulation_process,
                    self.configuration_manager,
                    self.simulation_manager,
                    self.app_manager,
                    self.logManager,
                    self.service_manager,
                    self.data_manager,
                    self.test_manager,
                    self.security_config,
                    self.field_bus_manager,
                ),
            )
        except Exception as e:
            print(e)
            self.logger.error(ProcessStatus.ERROR, None, e)

    @staticmethod
    def generateProcessId():
        return str(abs(random.randint(0, 2 ** 31)))

    def assignSimulationPort(self, simulationId):
        simIdKey = int(simulationId)
        if simIdKey not in self.simulation_ports:
            tempPort = 49152 + self.rand_port.randint(0, 16384)
            tempPortObj = AtomicInteger(tempPort)
            while tempPortObj in self.simulation_ports.values():
                newTempPort = 49152 + self.rand_port.randint(0, 16384)
                tempPortObj.set(newTempPort)
            self.simulation_ports[simIdKey] = tempPortObj
            return tempPortObj.get()
        else:
            raise Exception(
                "The simulation id already exists. This indicates that the simulation "
                "id is part of a simulation in progress."
            )
