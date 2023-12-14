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
# import org.slf4j.Logger;
#
# import static org.junit.Assert.*;
#
# import java.io.Serializable;
# import java.sql.SQLException;
# import java.util.Collection;
# import java.util.Dictionary;
# import java.util.HashMap;
# import java.util.Hashtable;
# import java.util.List;
# import java.util.Properties;
#
# import javax.jms.Destination;
#
# import static gov.pnnl.goss.gridappsd.TestConstants.*;
#
# import org.apache.felix.dm.annotation.api.ServiceDependency;
# import org.junit.Test;
# import org.junit.runner.RunWith;
# import org.mockito.ArgumentCaptor;
# import org.mockito.Captor;
# import org.mockito.Mock;
# import org.mockito.Mockito;
# import org.mockito.invocation.InvocationOnMock;
# import org.mockito.runners.MockitoJUnitRunner;
# import org.mockito.stubbing.Answer;
#
# import gov.pnnl.goss.gridappsd.api.DataManager;
# import gov.pnnl.goss.gridappsd.api.LogManager;
# import gov.pnnl.goss.gridappsd.configuration.ConfigurationManagerImpl;
# import gov.pnnl.goss.gridappsd.data.GridAppsDataSourcesImpl;
# import pnnl.goss.core.server.DataSourceBuilder;
# import pnnl.goss.core.server.DataSourceObject;
# import pnnl.goss.core.server.DataSourcePooledJdbc;
# import pnnl.goss.core.server.DataSourceRegistry;
#
# @RunWith(MockitoJUnitRunner.class)
# public class ConfigurationManagerComponentTests {
#
# 	@Mock
# 	Logger logger;
#
#
# 	@Mock
# 	private LogManager log_manager;
#
# 	@Mock
# 	private DataManager data_manager;
#
# 	@Captor
# 	ArgumentCaptor<String> argCaptor;
#
# 	@Mock DataSourcePooledJdbc datasourceObject;
#
#
#
#
#
# 	//test updated and get configuration property
# 	@Test
# 	public void configPropertiesSetWhen_configManagerUpdated() {
# 		ArgumentCaptor<String> argCaptor = ArgumentCaptor.forClass(String.class);
# 		ConfigurationManagerImpl config_manager = new ConfigurationManagerImpl(log_manager, data_manager);
# 		config_manager.start();
#
# 		final String FNCS_PATH_PROP = "fncs.path";
# 		final String FNCS_PATH_VAL = "fncs_broker";
# 		final String GRIDLABD_PATH_PROP = "gridlabd.path";
# 		final String GRIDLABD_PATH_VAL = "gridlabd";
# 		final String GRIDAPPSD_PATH_PROP = "gridappsd.temp.path";
# 		final String GRIDAPPSD_PATH_VAL = "\\tmp\\gridappsd_tmp";
# 		final String FNCS_BRIDGE_PATH_PROP = "fncs.bridge.path";
# 		final String FNCS_BRIDGE_PATH_VAL = ".\\scripts\\goss_fncs_bridge.py";
#
#
#
#
# 		Hashtable<String, String> props = new Hashtable<String, String>();
# 		props.put(FNCS_PATH_PROP, FNCS_PATH_VAL);
# 		props.put(GRIDLABD_PATH_PROP, GRIDLABD_PATH_VAL);
# 		props.put(GRIDAPPSD_PATH_PROP, GRIDAPPSD_PATH_VAL);
# 		props.put(FNCS_BRIDGE_PATH_PROP, FNCS_BRIDGE_PATH_VAL);
# 		config_manager.updated(props);
#
# 		assertEquals(FNCS_PATH_VAL, config_manager.getConfigurationProperty(FNCS_PATH_PROP));
# 		assertEquals(GRIDLABD_PATH_VAL, config_manager.getConfigurationProperty(GRIDLABD_PATH_PROP));
# 		assertEquals(GRIDAPPSD_PATH_VAL, config_manager.getConfigurationProperty(GRIDAPPSD_PATH_PROP));
# 		assertEquals(FNCS_BRIDGE_PATH_VAL, config_manager.getConfigurationProperty(FNCS_BRIDGE_PATH_PROP));
# 	}
#
#
# 	//get simulation file
#
#
#
	# @Test
	# /**
	#  * 	Succeeds when the proper number of properties are set on the updated call, and datasourcebuilder.create is called, and the correct registered datasource name is added
	#  */
	# public void registryUpdatedWhen_dataSourcesStarted(){
	# 	ArgumentCaptor<String> argCaptor = ArgumentCaptor.forClass(String.class);
	# 	Properties datasource_properties = new Properties();
	# 	GridAppsDataSourcesImpl dataSources = new GridAppsDataSourcesImpl(logger, datasource_builder, datasource_registry, datasource_properties);
	# 	Hashtable<String, String> props = new Hashtable<String, String>();
	# 	String datasourceName = "pnnl.goss.sql.datasource.gridappsd";
	# 	props.put("name", datasourceName);
	# 	props.put(DataSourceBuilder.DATASOURCE_USER, "gridappsduser");
	# 	props.put(DataSourceBuilder.DATASOURCE_PASSWORD, "gridappsdpw");
	# 	props.put(DataSourceBuilder.DATASOURCE_URL, "mysql://lalala");
	# 	props.put("driver", "com.mysql.jdbc.Driver");
	# 	dataSources.updated(props);
    #
	# 	assertEquals(5, datasource_properties.size());
	# 	dataSources.start();
    #
	# 	//verify datasource_builder.create(datasourceName, datasource_properties);
	# 	try {
	# 		Mockito.verify(datasource_builder).create(argCaptor.capture(), Mockito.any());
	# 		assertEquals(datasourceName, argCaptor.getValue());
	# 	} catch (ClassNotFoundException e) {
	# 		print(e);
	# 		assert(false);
	# 	} catch (Exception e) {
	# 		print(e);
	# 		assert(false);
	# 	}
    #
	# 	//verify registeredDatasources.add(datasourceName);
	# 	List<String> registeredDatasources = dataSources.getRegisteredDatasources();
	# 	assertEquals(1, registeredDatasources.size());
    #
	# }
    #
	# @Test
	# /**
	#  * 	Succeeds when the registry is empty after the service has been stopped
	#  */
	# public void registryClearedWhen_dataSourcesStopped(){
	# 	ArgumentCaptor<String> argCaptor = ArgumentCaptor.forClass(String.class);
	# 	Properties datasource_properties = new Properties();
	# 	GridAppsDataSourcesImpl dataSources = new GridAppsDataSourcesImpl(logger, datasource_builder, datasource_registry, datasource_properties);
	# 	Hashtable<String, String> props = new Hashtable<String, String>();
	# 	String datasourceName = "pnnl.goss.sql.datasource.gridappsd";
	# 	props.put("name", datasourceName);
	# 	props.put(DataSourceBuilder.DATASOURCE_USER, "gridappsduser");
	# 	props.put(DataSourceBuilder.DATASOURCE_PASSWORD, "gridappsdpw");
	# 	props.put(DataSourceBuilder.DATASOURCE_URL, "mysql://lalala");
	# 	props.put("driver", "com.mysql.jdbc.Driver");
	# 	dataSources.updated(props);
    #
	# 	assertEquals(5, datasource_properties.size());
	# 	dataSources.start();
    #
	# 	//verify datasource_builder.create(datasourceName, datasource_properties);
	# 	try {
	# 		Mockito.verify(datasource_builder).create(argCaptor.capture(), Mockito.any());
	# 		assertEquals(datasourceName, argCaptor.getValue());
	# 	} catch (ClassNotFoundException e) {
	# 		print(e);
	# 		assert(false);
	# 	} catch (Exception e) {
	# 		print(e);
	# 		assert(false);
	# 	}
    #
	# 	//verify registeredDatasources.add(datasourceName);
	# 	List<String> registeredDatasources = dataSources.getRegisteredDatasources();
	# 	assertEquals(1, registeredDatasources.size());
    #
    #
	# 	dataSources.stop();
    #
    #
	# 	assertEquals(0, dataSources.getRegisteredDatasources().size());
    #
	# }
    #
    #
	# @Test
	# /**
	#  * 	Succeeds when there was an error because no properties were passed in
	#  */
	# public void errorWhen_dataSourcesStartedWithNoProperties(){
	# 	ArgumentCaptor<String> argCaptor = ArgumentCaptor.forClass(String.class);
	# 	Properties datasource_properties = new Properties();
	# 	GridAppsDataSourcesImpl dataSources = new GridAppsDataSourcesImpl(logger, datasource_builder, datasource_registry, datasource_properties);
    #
	# 	try{
	# 		dataSources.start();
	# 	}catch(Exception e){
	# 		assertEquals("No datasource name provided when registering data source", e.getMessage());
	# 	}
    #
    #
	# }
    #
    #
    #
	# @Test
	# /**
	#  * 	Succeeds when the proper number of properties are set on the updated call, and datasourcebuilder.create is called, and the correct registered datasource name is added
	#  */
	# public void registryKeysExistWhen_dataSourcesStarted(){
	# 	ArgumentCaptor<String> argCaptor = ArgumentCaptor.forClass(String.class);
    #
	# 	try {
	# 		//When datasource_builder.create is called add a face datasource object to the datasource_registry (similar to what the actual implementation would do)
	# 		Answer answer = new Answer() {
	# 			@Override
	# 			public Object answer(InvocationOnMock invocation) throws Throwable {
	# 				Object[] args = invocation.getArguments();
	# 				String dsName = args[0].toString();
	# 				datasource_registry.add(dsName, datasourceObject);
	# 				return null;
	# 			}
	# 		};
	# 		Mockito.doAnswer(answer).when(datasource_builder).create(argCaptor.capture(), Mockito.any());
	# 	} catch (Exception e) {
	# 		print(e);
	# 	}
    #
    #
    #
	# 	Properties datasource_properties = new Properties();
	# 	GridAppsDataSourcesImpl dataSources = new GridAppsDataSourcesImpl(logger, datasource_builder, datasource_registry, datasource_properties);
	# 	Hashtable<String, String> props = new Hashtable<String, String>();
	# 	String datasourceName = "pnnl.goss.sql.datasource.gridappsd";
	# 	props.put("name", datasourceName);
	# 	props.put(DataSourceBuilder.DATASOURCE_USER, "gridappsduser");
	# 	props.put(DataSourceBuilder.DATASOURCE_PASSWORD, "gridappsdpw");
	# 	props.put(DataSourceBuilder.DATASOURCE_URL, "mysql://lalala");
	# 	props.put("driver", "com.mysql.jdbc.Driver");
	# 	dataSources.updated(props);
    #
	# 	assertEquals(5, datasource_properties.size());
	# 	dataSources.start();
    #
	# 	//verify datasource_builder.create(datasourceName, datasource_properties);
	# 	try {
	# 		Mockito.verify(datasource_builder).create(argCaptor.capture(), Mockito.any());
	# 		assertEquals(datasourceName, argCaptor.getValue());
	# 	} catch (ClassNotFoundException e) {
	# 		print(e);
	# 		assert(false);
	# 	} catch (Exception e) {
	# 		print(e);
	# 		assert(false);
	# 	}
    #
	# 	//verify registeredDatasources.add(datasourceName);
	# 	List<String> registeredDatasources = dataSources.getRegisteredDatasources();
	# 	assertEquals(1, registeredDatasources.size());
    #
    #
	# 	//  test get data source keys
	# 	Collection<String> dsKeys = dataSources.getDataSourceKeys();
	# 	assertEquals(datasourceName, dsKeys.toArray()[0]);
    #
	# 	// test get data source by key
	# 	DataSourcePooledJdbc obj = dataSources.getDataSourceByKey(datasourceName);
	# 	assertEquals(datasourceObject, obj);
    #
    #
    #
	# 	// test get connection by key
	# 	dataSources.getConnectionByKey(datasourceName);
	# 	try {
	# 		Mockito.verify(datasourceObject).getConnection();
	# 	} catch (SQLException e) {
	# 		print(e);
	# 	}
    #
	# 	//verify datasourceregistry size
	# 	assertEquals(1, datasource_registry.getAvailable().size());
    #
    #
	# }
#
# }

import unittest
import logging
from unittest.mock import Mock, MagicMock, patch, PropertyMock

from gov_pnnl_goss.gridappsd.simulation.ConfigurationManagerImpl import ConfigurationManagerImpl
# from gov.pnnl.goss.gridappsd import ConfigurationManagerImpl
# from gov.pnnl.goss.gridappsd.api import DataManager, LogManager
# from gov.pnnl.goss.gridappsd.data import GridAppsDataSourcesImpl
# from pnnl.goss.core.server import DataSourceBuilder, DataSourcePooledJdbc, DataSourceRegistry
# from pnnl.goss.gridappsd import TestConstants


class ConfigurationManagerComponentTests(unittest.TestCase):

    @patch('LogManager', return_value=Mock(spec=logging.Logger))
    @patch('gov.pnnl.goss.gridappsd.ConfigurationManagerImpl.log_manager')
    @patch('gov.pnnl.goss.gridappsd.ConfigurationManagerImpl.data_manager')
    def test_config_properties_set_when_config_manager_updated(self, mock_data_manager, mock_log_manager, mock_logger):
        mock_data_manager.return_value = MagicMock(spec=DataManager)
        mock_log_manager.return_value = MagicMock(spec=LogManager)

        configManager = ConfigurationManagerImpl(logManager, dataManager)
        configManager.start()

        FNCS_PATH_PROP = "fncs.path"
        FNCS_PATH_VAL = "fncs_broker"
        GRIDLABD_PATH_PROP = "gridlabd.path"
        GRIDLABD_PATH_VAL = "gridlabd"
        GRIDAPPSD_PATH_PROP = "gridappsd.temp.path"
        GRIDAPPSD_PATH_VAL = "\\tmp\\gridappsd_tmp"
        FNCS_BRIDGE_PATH_PROP = "fncs.bridge.path"
        FNCS_BRIDGE_PATH_VAL = ".\\scripts\\goss_fncs_bridge.py"

        props = {
            FNCS_PATH_PROP: FNCS_PATH_VAL,
            GRIDLABD_PATH_PROP: GRIDLABD_PATH_VAL,
            GRIDAPPSD_PATH_PROP: GRIDAPPSD_PATH_VAL,
            FNCS_BRIDGE_PATH_PROP: FNCS_BRIDGE_PATH_VAL
        }

        configManager.updated(props)

        self.assertEqual(FNCS_PATH_VAL, configManager.getConfigurationProperty(FNCS_PATH_PROP))
        self.assertEqual(GRIDLABD_PATH_VAL, configManager.getConfigurationProperty(GRIDLABD_PATH_PROP))
        self.assertEqual(GRIDAPPSD_PATH_VAL, configManager.getConfigurationProperty(GRIDAPPSD_PATH_PROP))
        self.assertEqual(FNCS_BRIDGE_PATH_VAL, configManager.getConfigurationProperty(FNCS_BRIDGE_PATH_PROP))

    @patch('LogManager', return_value=Mock(spec=logging.Logger))
    @patch('gov.pnnl.goss.gridappsd.ConfigurationManagerImpl.log_manager')
    @patch('gov.pnnl.goss.gridappsd.ConfigurationManagerImpl.data_manager')
    def test_registry_updated_when_data_sources_started(self, mock_data_manager, mock_log_manager, mock_logger):
        mock_data_manager.return_value = MagicMock(spec=DataManager)
        mock_log_manager.return_value = MagicMock(spec=LogManager)

        datasourceBuilder = Mock(spec=DataSourceBuilder)
        datasourceRegistry = Mock(spec=DataSourceRegistry)
        datasourceProperties = Mock(spec=dict)
        logger = MagicMock(spec=logging.Logger)

        configManager = ConfigurationManagerImpl(logger, datasourceBuilder, datasourceRegistry, datasourceProperties)
        configManager.start()

        FNCS_PATH_PROP = "fncs.path"
        FNCS_PATH_VAL = "fncs_broker"
        GRIDLABD_PATH_PROP = "gridlabd.path"
        GRIDLABD_PATH_VAL = "gridlabd"
        GRIDAPPSD_PATH_PROP = "gridappsd.temp.path"
        GRIDAPPSD_PATH_VAL = "\\tmp\\gridappsd_tmp"
        FNCS_BRIDGE_PATH_PROP = "fncs.bridge.path"
        FNCS_BRIDGE_PATH_VAL = ".\\scripts\\goss_fncs_bridge.py"

        props = {
            FNCS_PATH_PROP: FNCS_PATH_VAL,
            GRIDLABD_PATH_PROP: GRIDLABD_PATH_VAL,
            GRIDAPPSD_PATH_PROP: GRIDAPPSD_PATH_VAL,
            FNCS_BRIDGE_PATH_PROP: FNCS_BRIDGE_PATH_VAL,
            "name": "pnnl.goss.sql.datasource.gridappsd",
            DataSourceBuilder.DATASOURCE_USER: "gridappsduser",
            DataSourceBuilder.DATASOURCE_PASSWORD: "gridappsdpw",
            DataSourceBuilder.DATASOURCE_URL: "mysql://lalala",
            "driver": "com.mysql.jdbc.Driver"
        }

        configManager.updated(props)

        self.assertEqual(5, len(datasourceProperties))
        configManager.start()

        datasourceBuilder.create.assert_called_with("pnnl.goss.sql.datasource.gridappsd", datasourceProperties)
        self.assertEqual(1, len(configManager.getRegisteredDatasources()))

    @patch('LogManager', return_value=Mock(spec=logging.Logger))
    @patch('gov.pnnl.goss.gridappsd.ConfigurationManagerImpl.log_manager')
    @patch('gov.pnnl.goss.gridappsd.ConfigurationManagerImpl.data_manager')
    def test_registry_cleared_when_data_sources_stopped(self, mock_data_manager, mock_log_manager, mock_logger):
        mock_data_manager.return_value = MagicMock(spec=DataManager)
        mock_log_manager.return_value = MagicMock(spec=LogManager)

        datasourceBuilder = Mock(spec=DataSourceBuilder)
        datasourceRegistry = Mock(spec=DataSourceRegistry)
        datasourceProperties = Mock(spec=dict)
        logger = MagicMock(spec=logging.Logger)

        configManager = ConfigurationManagerImpl(logger, datasourceBuilder, datasourceRegistry, datasourceProperties)
        configManager.start()

        FNCS_PATH_PROP = "fncs.path"
        FNCS_PATH_VAL = "fncs_broker"
        GRIDLABD_PATH_PROP = "gridlabd.path"
        GRIDLABD_PATH_VAL = "gridlabd"
        GRIDAPPSD_PATH_PROP = "gridappsd.temp.path"
        GRIDAPPSD_PATH_VAL = "\\tmp\\gridappsd_tmp"
        FNCS_BRIDGE_PATH_PROP = "fncs.bridge.path"
        FNCS_BRIDGE_PATH_VAL = ".\\scripts\\goss_fncs_bridge.py"

        props = {
            FNCS_PATH_PROP: FNCS_PATH_VAL,
            GRIDLABD_PATH_PROP: GRIDLABD_PATH_VAL,
            GRIDAPPSD_PATH_PROP: GRIDAPPSD_PATH_VAL,
            FNCS_BRIDGE_PATH_PROP: FNCS_BRIDGE_PATH_VAL,
            "name": "pnnl.goss.sql.datasource.gridappsd",
            DataSourceBuilder.DATASOURCE_USER: "gridappsduser",
            DataSourceBuilder.DATASOURCE_PASSWORD: "gridappsdpw",
            DataSourceBuilder.DATASOURCE_URL: "mysql://lalala",
            "driver": "com.mysql.jdbc.Driver"
        }

        configManager.updated(props)

        self.assertEqual(5, len(datasourceProperties))
        configManager.start()

        datasourceBuilder.create.assert_called_with("pnnl.goss.sql.datasource.gridappsd", datasourceProperties)
        self.assertEqual(1, len(configManager.getRegisteredDatasources()))

        configManager.stop()
        self.assertEqual(0, len(configManager.getRegisteredDatasources()))

    @patch('LogManager', return_value=Mock(spec=logging.Logger))
    @patch('gov.pnnl.goss.gridappsd.ConfigurationManagerImpl.log_manager')
    @patch('gov.pnnl.goss.gridappsd.ConfigurationManagerImpl.data_manager')
    def test_error_when_data_sources_started_with_no_properties(self, mock_data_manager, mock_log_manager, mock_logger):
        mock_data_manager.return_value = MagicMock(spec=DataManager)
        mock_log_manager.return_value = MagicMock(spec=LogManager)

        datasourceBuilder = Mock(spec=DataSourceBuilder)
        datasourceRegistry = Mock(spec=DataSourceRegistry)
        datasourceProperties = Mock(spec=dict)
        logger = MagicMock(spec=logging.Logger)

        configManager = ConfigurationManagerImpl(logger, datasourceBuilder, datasourceRegistry, datasourceProperties)

        with self.assertRaises(Exception) as context:
            configManager.start()

        self.assertEqual("No datasource name provided when registering data source", str(context.exception))

    @patch('LogManager', return_value=Mock(spec=logging.Logger))
    @patch('gov.pnnl.goss.gridappsd.ConfigurationManagerImpl.log_manager')
    @patch('gov.pnnl.goss.gridappsd.ConfigurationManagerImpl.data_manager')
    def test_registry_keys_exist_when_data_sources_started(self, mock_data_manager, mock_log_manager, mock_logger):
        mock_data_manager.return_value = MagicMock(spec=DataManager)
        mock_log_manager.return_value = MagicMock(spec=LogManager)

        datasourceBuilder = Mock(spec=DataSourceBuilder)
        datasourceRegistry = Mock(spec=DataSourceRegistry)
        datasourceProperties = Mock(spec=dict)
        datasourceObject = Mock(spec=DataSourcePooledJdbc)
        logger = MagicMock(spec=logging.Logger)

        def answer(invocation):
            args = invocation.arguments
            dsName = str(args[0])
            datasourceRegistry.add(dsName, datasourceObject)
            return None

        with patch.object(datasourceBuilder, 'create', side_effect=answer):
            configManager = ConfigurationManagerImpl(logger, datasourceBuilder, datasourceRegistry,
                                                     datasourceProperties)
            configManager.start()

            FNCS_PATH_PROP = "fncs.path"
            FNCS_PATH_VAL = "fncs_broker"
            GRIDLABD_PATH_PROP = "gridlabd.path"
            GRIDLABD_PATH_VAL = "gridlabd"
            GRIDAPPSD_PATH_PROP = "gridappsd.temp.path"
            GRIDAPPSD_PATH_VAL = "\\tmp\\gridappsd_tmp"
            FNCS_BRIDGE_PATH_PROP = "fncs.bridge.path"
            FNCS_BRIDGE_PATH_VAL = ".\\scripts\\goss_fncs_bridge.py"

            props = {
                FNCS_PATH_PROP: FNCS_PATH_VAL,
                GRIDLABD_PATH_PROP: GRIDLABD_PATH_VAL,
                GRIDAPPSD_PATH_PROP: GRIDAPPSD_PATH_VAL,
                FNCS_BRIDGE_PATH_PROP: FNCS_BRIDGE_PATH_VAL,
                "name": "pnnl.goss.sql.datasource.gridappsd",
                DataSourceBuilder.DATASOURCE_USER: "gridappsduser",
                DataSourceBuilder.DATASOURCE_PASSWORD: "gridappsdpw",
                DataSourceBuilder.DATASOURCE_URL: "mysql://lalala",
                "driver": "com.mysql.jdbc.Driver"
            }

            configManager.updated(props)

            self.assertEqual(5, len(datasourceProperties))
            configManager.start()

            datasourceBuilder.create.assert_called_with("pnnl.goss.sql.datasource.gridappsd", datasourceProperties)
            self.assertEqual(1, len(configManager.getRegisteredDatasources()))

            dsKeys = configManager.getDataSourceKeys()
            self.assertEqual("pnnl.goss.sql.datasource.gridappsd", list(dsKeys)[0])

            obj = configManager.getDataSourceByKey("pnnl.goss.sql.datasource.gridappsd")
            self.assertEqual(datasourceObject, obj)

            configManager.getConnectionByKey("pnnl.goss.sql.datasource.gridappsd")
            datasourceObject.getConnection.assert_called_once()

            self.assertEqual(1, len(datasourceRegistry.getAvailable()))


if __name__ == '__main__':
    unittest.main()

