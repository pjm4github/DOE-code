from abc import ABC, abstractmethod
import logging
from enum import Enum

from gov_pnnl_goss.SpecialClasses import RequestLogMessage
from gov_pnnl_goss.gridappsd.dto.LogMessage import ProcessStatus


class LogLevel(Enum):
    TRACE = "TRACE"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"
    FATAL = "FATAL"


class LogManager(logging.Logger):
    """
    This is a special logger that runs across processes and across the GOSS bus
    """

    def __init__(self, name, level=logging.NOTSET):
        super().__init__(name, level)

        # You can customize the logger further if needed
        # For example, add custom handlers or formatters here
        formatter = logging.Formatter('%(asctime)status - %(name)status - %(levelname)status - %(message)status')
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self.addHandler(handler)
        self.process_id = ""  # (str): The process ID.
        self.process_type = ""  # (str): The process type.

    @abstractmethod
    def trace(self, process_status: ProcessStatus, process_id: str, message: str) -> None:
        """
        Log a trace message.

        Args:
            process_status (ProcessStatus): The process status.
            process_id (str): The process ID.
            message (str): The log message.
        """
        pass

    @abstractmethod
    def debug(self, process_status: ProcessStatus, process_id: str, message: str) -> None:
        """
        Log a debug message.

        Args:
            process_status (ProcessStatus): The process status.
            process_id (str): The process ID.
            message (str): The log message.
        """
        super().debug(f"{process_status}: {process_id}, {message}")
        pass

    @abstractmethod
    def info(self, process_status: ProcessStatus, process_id: str, message: str) -> None:
        """
        Log an info message.

        Args:
            process_status (ProcessStatus): The process status.
            process_id (str): The process ID.
            message (str): The log message.
        """
        super().info(f"{process_status}: {process_id}, {message}")
        pass

    @abstractmethod
    def warn(self, process_status: ProcessStatus, process_id: str, message: str) -> None:
        """
        Log a warning message.

        Args:
            process_status (ProcessStatus): The process status.
            process_id (str): The process ID.
            message (str): The log message.
        """
        super().warning(f"{process_status}: {process_id}, {message}")
        pass

    @abstractmethod
    def error(self, process_status: ProcessStatus, process_id: str, message: str) -> None:
        """
        Log an error message.

        Args:
            process_status (ProcessStatus): The process status.
            process_id (str): The process ID.
            message (str): The log message.
        """
        super().error(f"{process_status}: {process_id}, {message}")
        pass

    @abstractmethod
    def fatal(self, process_status: ProcessStatus, process_id: str, message: str) -> None:
        """
        Log a fatal error message.

        Args:
            process_status (ProcessStatus): The process status.
            process_id (str): The process ID.
            message (str): The log message.
        """
        super().error(f"FATAL: {process_status}: {process_id}, {message}")
        pass

    @abstractmethod
    def log_message_from_source(self, process_status: ProcessStatus, process_id: str, message: str, source: str, log_level: LogLevel) -> None:
        """
        Log a message with a specific source and log level.

        Args:
            process_status (ProcessStatus): The process status.
            process_id (str): The process ID.
            message (str): The log message.
            source (str): The source of the log message.
            log_level (LogLevel): The log level (DEBUG, INFO, WARN, ERROR, FATAL).
        """
        pass

    @abstractmethod
    def get(self, message: RequestLogMessage, output_topics: str, log_topic: str) -> None:
        """
        Get log messages based on the request.

        Args:
            message (RequestLogMessage): Log message request details.
            output_topics (str): Topics for output.
            log_topic (str): Log topic.
        """
        pass

    @abstractmethod
    def get_log_data_manager(self):
        """
        Get the log data manager.

        Returns:
            LogDataManager: The log data manager.
        """
        return self

    def get_log_level(self) -> logging:
        """
        Get the log level.

        Returns:
            LogLevel: The current log level (DEBUG, INFO, WARN, ERROR, FATAL).
        """
        return self.level

    def set_process_type(self, process_id: str, process_type: str) -> None:
        """
        Set the process type for a specific process ID.

        Args:
            process_id (str): The process ID.
            process_type (str): The process type.
        """
        self.process_type = process_type
        self.process_id = process_id

