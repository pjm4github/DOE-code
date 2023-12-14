import json
from enum import Enum


class LogLevel(Enum):
    TRACE = "TRACE"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"
    FATAL = "FATAL"


class ProcessStatus(Enum):
    STARTING = "STARTING"
    STARTED = "STARTED"
    RUNNING = "RUNNING"
    ERROR = "ERROR"
    CLOSED = "CLOSED"
    COMPLETE = "COMPLETE"
    STOPPED = "STOPPED"
    PAUSED = "PAUSED"


class LogMessage:

    def __init__(self, source="", processId="", timestamp=0, logMessage="",
                 logLevel=None, processStatus=None, storeToDb=True, process_type=""):
        self.source = source
        self.processId = processId
        self.timestamp = timestamp
        self.loggerger = logMessage
        self.loggerLevel = logLevel
        self.processStatus = processStatus
        self.storeToDb = storeToDb
        self.process_type = process_type

    def getSource(self):
        return self.source

    def setSource(self, source):
        self.source = source

    def getProcessId(self):
        return self.processId

    def setProcessId(self, processId):
        self.processId = processId

    def getTimestamp(self):
        return self.timestamp

    def setTimestamp(self, timestamp):
        self.timestamp = timestamp

    def getLogMessage(self):
        return self.loggerMessage

    def setLogMessage(self, logMessage):
        self.loggerMessage = logMessage

    def getLogLevel(self):
        return self.loggerLevel

    def setLogLevel(self, logLevel):
        self.loggerLevel = logLevel

    def getProcessStatus(self):
        return self.processStatus

    def setProcessStatus(self, processStatus):
        self.processStatus = processStatus

    def getStoreToDb(self):
        return self.storeToDb

    def setStoreToDb(self, storeToDb):
        self.storeToDb = storeToDb

    def getProcessType(self):
        return self.process_type

    def setProcessType(self, process_type):
        self.process_type = process_type

    @staticmethod
    def parse(jsonString):
        obj = json.loads(jsonString)
        if "logMessage" not in obj:
            raise ValueError("Expected attribute 'logMessage' not found in JSON string.")
        return LogMessage(
            obj.get("source", ""),
            obj.get("processId", ""),
            obj.get("timestamp", 0),
            obj["logMessage"],
            obj.get("logLevel"),
            obj.get("processStatus"),
            obj.get("storeToDb", True),
            obj.get("process_type", "")
        )

    def toJSON(self):
        return json.dumps(self.__dict__)
