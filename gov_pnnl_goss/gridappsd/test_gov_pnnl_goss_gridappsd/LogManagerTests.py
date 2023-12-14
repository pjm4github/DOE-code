# /*******************************************************************************
#  * Copyright (c) 2017, Battelle Memorial Institute All rights reserved.
#  * Battelle Memorial Institute (hereinafter Battelle) hereby grants permission to any person or entity
#  * lawfully obtaining a copy of this software and associated documentation files (hereinafter the
#  * Software) to redistribute and use the Software in source and binary forms, with or without modification.
#  * Such person or entity may use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
#  * the Software, and may permit others to do so, subject to the following conditions:
#  * Redistributions of source code must retain the above copyright notice, this list of conditions and the
#  * following disclaimers.
#  * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and
#  * the following disclaimer in the documentation and/or other materials provided with the distribution.
#  * Other than as used herein, neither the name Battelle Memorial Institute or Battelle may be used in any
#  * form whatsoever without the express written consent of Battelle.
#  * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
#  * EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
#  * MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL
#  * BATTELLE OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
#  * OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
#  * GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
#  * AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#  * NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
#  * OF THE POSSIBILITY OF SUCH DAMAGE.
#  * General disclaimer for use with OSS licenses
#  *
#  * This material was prepared as an account of work sponsored by an agency of the United States Government.
#  * Neither the United States Government nor the United States Department of Energy, nor Battelle, nor any
#  * of their employees, nor any jurisdiction or organization that has cooperated in the development of these
#  * materials, makes any warranty, express or implied, or assumes any legal liability or responsibility for
#  * the accuracy, completeness, or usefulness or any information, apparatus, product, software, or process
#  * disclosed, or represents that its use would not infringe privately owned rights.
#  *
#  * Reference herein to any specific commercial product, process, or service by trade name, trademark, manufacturer,
#  * or otherwise does not necessarily constitute or imply its endorsement, recommendation, or favoring by the United
#  * States Government or any agency thereof, or Battelle Memorial Institute. The views and opinions of authors expressed
#  * herein do not necessarily state or reflect those of the United States Government or any agency thereof.
#  *
#  * PACIFIC NORTHWEST NATIONAL LABORATORY operated by BATTELLE for the
#  * UNITED STATES DEPARTMENT OF ENERGY under Contract DE-AC05-76RL01830
#  ******************************************************************************/
# package gov.pnnl.goss.gridappsd;
#
# import static org.junit.Assert.assertEquals;
# import gov.pnnl.goss.gridappsd.api.LogDataManager;
# import gov.pnnl.goss.gridappsd.api.LogManager;
# import gov.pnnl.goss.gridappsd.dto.LogMessage;
# import gov.pnnl.goss.gridappsd.dto.LogMessage.LogLevel;
# import gov.pnnl.goss.gridappsd.dto.LogMessage.ProcessStatus;
# import gov.pnnl.goss.gridappsd.dto.RequestLogMessage;
# import gov.pnnl.goss.gridappsd.log.LogManagerImpl;
# import gov.pnnl.goss.gridappsd.utils.GridAppsDConstants;
#
# import java.text.ParseException;
# import java.util.List;
#
# import org.junit.Test;
# import org.junit.runner.RunWith;
# import org.mockito.ArgumentCaptor;
# import org.mockito.Captor;
# import org.mockito.Mock;
# import org.mockito.Mockito;
# import org.mockito.runners.MockitoJUnitRunner;
#
# @RunWith(MockitoJUnitRunner.class)
# public class LogManagerTests {
#
# 	@Mock
# 	LogDataManager logDataManager;
#
# 	@Captor
# 	ArgumentCaptor<String> argCaptor;
# 	@Captor
# 	ArgumentCaptor<Long> argLongCaptor;
# 	@Captor
# 	ArgumentCaptor<LogLevel> argLogLevelCaptor;
# 	@Captor
# 	ArgumentCaptor<ProcessStatus> argProcessStatusCaptor;
#
#
# 	@Test
# 	public void storeCalledWhen_logStoreToDBTrueInObject() throws ParseException{
#
# 		LogManager log_manager = new LogManagerImpl(logDataManager);
#
# 		log_manager.debug(ProcessStatus.RUNNING, "request_1234", "Process manager received message ");
#
# 		Mockito.verify(logDataManager).store(argCaptor.capture(),argCaptor.capture(),
# 				argLongCaptor.capture(), argCaptor.capture(),
# 				argLogLevelCaptor.capture(), argProcessStatusCaptor.capture(),argCaptor.capture(),argCaptor.capture());
#
# 		List<String> allStringValues = argCaptor.getAllValues();
# 		assertEquals(4, allStringValues.size());
# 		assertEquals(this.getClass().getName(), allStringValues.get(0));
# 		assertEquals("request_1234", allStringValues.get(1));
# 		//TODO: User test user for this instead of system
# 		assertEquals("system", allStringValues.get(3));
# 		//assertEquals(new Long(message.getTimestamp()), argLongCaptor.getValue());
# 		//assertEquals(message.getLogLevel(), argLogLevelCaptor.getValue());
# 		assertEquals("Process manager received message ", allStringValues.get(2));
# 		assertEquals(ProcessStatus.RUNNING, argProcessStatusCaptor.getValue());
#
# 	}
#
# 	@Test
# 	public void storeCalledWhen_logStoreToDBTrueInString() throws ParseException{
#
#
# 		LogManager log_manager = new LogManagerImpl(logDataManager);
# 		log_manager.logMessageFromSource(ProcessStatus.RUNNING, "request_123", "Testing LogManager", "app_123", LogLevel.DEBUG);
#
# 		Mockito.verify(logDataManager).store(argCaptor.capture(),argCaptor.capture(),
# 				argLongCaptor.capture(), argCaptor.capture(),
# 				argLogLevelCaptor.capture(), argProcessStatusCaptor.capture(),argCaptor.capture(),argCaptor.capture());
#
# 		List<String> allStringValues = argCaptor.getAllValues();
# 		assertEquals(4, allStringValues.size());
# 		assertEquals("app_123", allStringValues.get(0));
# 		assertEquals("request_123", allStringValues.get(1));
# 		//TODO: User test user for this instead of system
# 		assertEquals("system", allStringValues.get(3));
# 		assertEquals(new Long(GridAppsDConstants.SDF_SIMULATION_REQUEST.parse("8/14/17 2:22:22").getTime()), argLongCaptor.getValue());
# 		assertEquals(LogLevel.DEBUG, argLogLevelCaptor.getValue());
# 		assertEquals("Testing LogManager", allStringValues.get(2));
# 		assertEquals(ProcessStatus.STARTED, argProcessStatusCaptor.getValue());
#
#
# 	}
#
# 	@Test
# 	public void queryCalledWhen_getLogCalledWithObject() throws ParseException{
#
# 		LogManager log_manager = new LogManagerImpl(logDataManager);
#
# 		RequestLogMessage message = new RequestLogMessage();
# 		message.setLogLevel(LogLevel.DEBUG);
# 		message.setSource(this.getClass().getName());
# 		message.setProcessStatus(ProcessStatus.RUNNING);
# 		message.setTimestamp(GridAppsDConstants.SDF_SIMULATION_REQUEST.parse("11/11/11 11:11:11").getTime());
#
# 		String restultTopic = "goss.gridappsd.data.output";
# 		String logTopic = "goss.gridappsd.data.log";
#
# 		log_manager.get(message, restultTopic, logTopic);
#
#
# //		Mockito.verify(logDataManager).query(argCaptor.capture(), argCaptor.capture(),
# //				argCaptor.capture(), argCaptor.capture(), argCaptor.capture());
# //
# //		List<String> allValues = argCaptor.getAllValues();
# //		assertEquals(5, allValues.size());
# //		assertEquals(message.getProcess_id(), allValues.get(0));
# //		assertEquals(message.getTimestamp(), allValues.get(1));
# //		assertEquals(message.getLog_level(), allValues.get(2));
# //		assertEquals(message.getProcess_status(), allValues.get(3));
# //		//TODO: User test user for this instead of system
# //		assertEquals("system", allValues.get(4));
# 	}
#
# 	@Test
# 	public void queryCalledWhen_getLogCalledWithString() throws ParseException{
#
#
# 		LogManager log_manager = new LogManagerImpl(logDataManager);
# 		String message = "{"
# 				+ "\"process_id\":\"app_123\","
# 				+ "\"process_status\":\"started\","
# 				+ "\"log_level\":\"debug\","
# 				+ "\"log_message\":\"something happened\","
# 				+ "\"timestamp\": "+GridAppsDConstants.SDF_SIMULATION_REQUEST.parse("8/14/17 2:22:22").getTime()+"}";
#
# 		String restultTopic = "goss.gridappsd.data.output";
# 		String logTopic = "goss.gridappsd.data.log";
#
# //		log_manager.get(LogMessage.parse(message),restultTopic,logTopic);
#
#
# //		Mockito.verify(logDataManager).query(argCaptor.capture(), argCaptor.capture(),
# //				argCaptor.capture(), argCaptor.capture(), argCaptor.capture());
# //
# //		List<String> allValues = argCaptor.getAllValues();
# //		assertEquals(5, allValues.size());
# //		assertEquals("app_123", allValues.get(0));
# //		assertEquals("8\14\17 2:22:22", allValues.get(1));
# //		assertEquals("debug", allValues.get(2));
# //		assertEquals("started", allValues.get(3));
# //		//TODO: User test user for this instead of system
# //		assertEquals("system", allValues.get(4));
#
#
# 	}
#
#
#
# }

import unittest
from unittest.mock import Mock, patch
from datetime import datetime

from gov_pnnl_goss.gridappsd.api.LogManager import ProcessStatus, RequestLogMessage
from gov_pnnl_goss.gridappsd.dto.LogMessage import LogLevel


# from pnnl.goss.gridappsd.api.LogDataManager import LogDataManager
# from gov.pnnl.goss.gridappsd.api.LogManager import LogManager
# from gov.pnnl.goss.gridappsd.dto.LogMessage import LogMessage, LogLevel, ProcessStatus
# from gov.pnnl.goss.gridappsd.dto.RequestLogMessage import RequestLogMessage
# from gov.pnnl.goss.gridappsd.log.LogManagerImpl import LogManagerImpl
# from gov.pnnl.goss.gridappsd.utils.GridAppsDConstants import GridAppsDConstants

class LogManagerImpl:
	pass


class LogManagerTests(unittest.TestCase):

    @patch('gov.pnnl.goss.gridappsd.log.LogManagerImpl.LogDataManager')
    def setUp(self, mock_log_data_manager):
        self.logger = mock_log_data_manager
        self.arg_captor = Mock()
        self.arg_long_captor = Mock()
        self.arg_log_level_captor = Mock()
        self.arg_process_status_captor = Mock()

    def test_store_called_when_log_store_to_db_true_in_object(self):
        log_manager = LogManagerImpl(self.logger)

        log_manager.debug(ProcessStatus.RUNNING, "request_1234", "Process manager received message ")

        self.logger.store.assert_called_once_with(
            self.arg_captor.capture(), self.arg_captor.capture(),
            self.arg_long_captor.capture(), self.arg_captor.capture(),
            self.arg_log_level_captor.capture(), self.arg_process_status_captor.capture(),
            self.arg_captor.capture(), self.arg_captor.capture()
        )

        all_string_values = self.arg_captor.mock_calls[0][1]
        self.assertEqual(4, len(all_string_values))
        self.assertEqual(self.__class__.__name__, all_string_values[0])
        self.assertEqual("request_1234", all_string_values[1])
        # TODO: Use test user for this instead of "system"
        self.assertEqual("system", all_string_values[3])
        # assertEquals(new Long(message.getTimestamp()), argLongCaptor.getValue());
        # assertEquals(message.getLogLevel(), argLogLevelCaptor.getValue())
        self.assertEqual("Process manager received message ", all_string_values[2])
        self.assertEqual(ProcessStatus.RUNNING, self.arg_process_status_captor.mock_calls[0][1])

    def test_store_called_when_log_store_to_db_true_in_string(self):
        log_manager = LogManagerImpl(self.logger)
        log_manager.log_message_from_source(ProcessStatus.RUNNING, "request_123", "Testing LogManager", "app_123", LogLevel.DEBUG)

        self.logger.store.assert_called_once_with(
            self.arg_captor.capture(), self.arg_captor.capture(),
            self.arg_long_captor.capture(), self.arg_captor.capture(),
            self.arg_log_level_captor.capture(), self.arg_process_status_captor.capture(),
            self.arg_captor.capture(), self.arg_captor.capture()
        )

        all_string_values = self.arg_captor.mock_calls[0][1]
        self.assertEqual(4, len(all_string_values))
        self.assertEqual("app_123", all_string_values[0])
        self.assertEqual("request_123", all_string_values[1])
        # TODO: Use test user for this instead of "system"
        self.assertEqual("system", all_string_values[3])
        self.assertEqual(datetime.strptime("8/14/17 2:22:22", "%multiplicities/%d/%y %H:%M:%S").timestamp() * 1000, self.arg_long_captor.mock_calls[0][1])
        self.assertEqual(LogLevel.DEBUG, self.arg_log_level_captor.mock_calls[0][1])
        self.assertEqual("Testing LogManager", all_string_values[2])
        self.assertEqual(ProcessStatus.STARTED, self.arg_process_status_captor.mock_calls[0][1])

    def test_query_called_when_get_log_called_with_object(self):
        log_manager = LogManagerImpl(self.logger)
        message = RequestLogMessage()
        message.set_log_level(LogLevel.DEBUG)
        message.set_source(self.__class__.__name__)
        message.set_process_status(ProcessStatus.RUNNING)
        message.set_timestamp(datetime.strptime("11/11/11 11:11:11", "%multiplicities/%d/%y %H:%M:%S").timestamp() * 1000)

        result_topic = "goss.gridappsd.data.output"
        log_topic = "goss.gridappsd.data.log"

        log_manager.get(message, result_topic, log_topic)

        # Mockito.verify(logDataManager).query(argCaptor.capture(), argCaptor.capture(),
        #         argCaptor.capture(), argCaptor.capture(), argCaptor.capture());
        #
        # List<String> allValues = argCaptor.getAllValues();
        # assertEquals(5, allValues.size());
        # assertEquals(message.getProcess_id(), allValues.get(0));
        # assertEquals(message.getTimestamp(), allValues.get(1));
        # assertEquals(message.getLog_level(), allValues.get(2));
        # assertEquals(message.getProcess_status(), allValues.get(3));
        # TODO: Use test user for this instead of "system"
        # assertEquals("system", allValues.get(4))


    def test_query_called_when_get_log_called_with_string(self):
        log_manager = LogManagerImpl(self.logger)
        message = ("{"
                + "\"process_id\":\"app_123\","
                + "\"process_status\":\"started\","
                + "\"log_level\":\"debug\","
                + "\"log_message\":\"something happened\","
                + "\"timestamp\": "+str(datetime.strptime("8/14/17 2:22:22", "%multiplicities/%d/%y %H:%M:%S").timestamp() * 1000)+"}")
        result_topic = "goss.gridappsd.data.output"
        log_topic = "goss.gridappsd.data.log"

        # log_manager.get(LogMessage.parse(message), result_topic, log_topic)

        # Mockito.verify(logDataManager).query(argCaptor.capture(), argCaptor.capture(),
        #         argCaptor.capture(), argCaptor.capture(), argCaptor.capture());
        #
        # List<String> allValues = argCaptor.getAllValues();
        # assertEquals(5, allValues.size());
        # assertEquals("app_123", allValues.get(0));
        # assertEquals("8\14\17 2:22:22", allValues.get(1));
        # assertEquals("debug", allValues.get(2));
        # assertEquals("started", allValues.get(3));
        # TODO: Use test user for this instead of "system"
        # assertEquals("system", allValues.get(4))


if __name__ == '__main__':
    unittest.main()
