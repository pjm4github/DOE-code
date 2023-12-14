import unittest
from unittest.mock import Mock, MagicMock, patch
from queue import Queue
# from pnnl.goss.core.server.DataSourcePooledJdbc import DataSourcePooledJdbc
# from pnnl.goss.core.server.DataSourceBuilder import DataSourceBuilder
# from pnnl.goss.core.server.DataSourceRegistry import DataSourceRegistry
# from pnnl.goss.server.registry.DataSourceRegistryImpl import DataSourceRegistryImpl
# from gov.pnnl.goss.gridappsd.GridAppsDataSourcesImpl import GridAppsDataSourcesImpl

from logging import getLogger

from gov_pnnl_goss.core.server.DataSourceBuilder import DataSourceBuilder
from gov_pnnl_goss.core.server.DataSourcePooledJdbc import DataSourcePooledJdbc
from gov_pnnl_goss.gridappsd.data.GridAppsDataSourcesImpl import GridAppsDataSourcesImpl


# class DataSourceRegistry:   # from the core package
# 	pass


class DataSourceRegistryImpl:  # from the server package
	pass


# class DataSourcePooledJdbc:  # from the core package
# 	pass


# class DataSourceBuilder: # from the core package
# 	pass


class GridAppsDataSourcesComponentTests(unittest.TestCase):

	@patch('gov.pnnl.goss.gridappsd.GridAppsDataSourcesImpl.DataSourceBuilder')
	def setUp(self, mock_datasource_builder):
		self.log = getLogger(__name__)
		self.datasource_builder = mock_datasource_builder
		self.datasource_registry = DataSourceRegistryImpl()
		self.arg_captor = MagicMock()
		self.datasource_object = DataSourcePooledJdbc()

	def test_registry_updated_when_data_sources_started(self):
		# Test when data sources are started.
		# # 	 * 	Succeeds when the proper number of properties are set on the updated call, and datasourcebuilder.create is called, and the correct registered datasource name is added
		datasource_properties = {}
		data_sources = GridAppsDataSourcesImpl(self.log, self.datasource_builder, self.datasource_registry,
											   datasource_properties)
		props = {}
		datasource_name = "pnnl.goss.sql.datasource.gridappsd"
		props["name"] = datasource_name
		props[DataSourceBuilder.DATASOURCE_USER] = "gridappsduser"
		props[DataSourceBuilder.DATASOURCE_PASSWORD] = "gridappsdpw"
		props[DataSourceBuilder.DATASOURCE_URL] = "mysql://lalala"
		props["driver"] = "com.mysql.jdbc.Driver"
		data_sources.updated(props)

		self.assertEqual(5, datasource_properties.size())
		data_sources.start()

		# Verify datasource_builder.create(datasource_name, datasource_properties)
		self.datasource_builder.create.assert_called_once_with(datasource_name, datasource_properties)

		# Verify registered_datasources.add(datasource_name)
		registered_datasources = data_sources.get_registered_datasources()
		self.assertEqual(1, len(registered_datasources))

	def test_registry_cleared_when_data_sources_stopped(self):
		# # 	 * 	Succeeds when the registry is empty after the service has been stopped
		# Test when data sources are stopped.
		datasource_properties = {}
		data_sources = GridAppsDataSourcesImpl(self.log, self.datasource_builder, self.datasource_registry,
											   datasource_properties)
		props = {}
		datasource_name = "pnnl.goss.sql.datasource.gridappsd"
		props["name"] = datasource_name
		props[DataSourceBuilder.DATASOURCE_USER] = "gridappsduser"
		props[DataSourceBuilder.DATASOURCE_PASSWORD] = "gridappsdpw"
		props[DataSourceBuilder.DATASOURCE_URL] = "mysql://lalala"
		props["driver"] = "com.mysql.jdbc.Driver"
		data_sources.updated(props)

		self.assertEqual(5, datasource_properties.size())
		data_sources.start()

		# Verify datasource_builder.create(datasource_name, datasource_properties)
		self.datasource_builder.create.assert_called_once_with(datasource_name, datasource_properties)

		# Verify registered_datasources.add(datasource_name)
		registered_datasources = data_sources.get_registered_datasources()
		self.assertEqual(1, len(registered_datasources))

		data_sources.stop()

		self.assertEqual(0, len(data_sources.get_registered_datasources()))

	def test_error_when_data_sources_started_with_no_properties(self):
		# # 	 * 	Succeeds when there was an error because no properties were passed in
		# Test when data sources are started with no properties.
		datasource_properties = {}
		data_sources = GridAppsDataSourcesImpl(self.log, self.datasource_builder, self.datasource_registry,
											   datasource_properties)

		with self.assertRaises(Exception) as context:
			data_sources.start()

		self.assertEqual("No datasource name provided when registering data source", str(context.exception))

	def test_registry_keys_exist_when_data_sources_started(self):
		#	 * 	Succeeds when the proper number of properties are set on the updated call, and datasourcebuilder.create is called, and the correct registered datasource name is added
		# Test when data sources are started and registry keys exist.
		try:
			# When datasource_builder.create is called, add a fake datasource object to the datasource_registry.
			def answer(invocation):
				args = invocation.getArguments()
				ds_name = str(args[0])
				self.datasource_registry.add(ds_name, self.datasource_object)
				return None

			self.datasource_builder.create.side_effect = answer

			datasource_properties = {}
			data_sources = GridAppsDataSourcesImpl(self.log, self.datasource_builder, self.datasource_registry,
												   datasource_properties)
			props = {}
			datasource_name = "pnnl.goss.sql.datasource.gridappsd"
			props["name"] = datasource_name
			props[DataSourceBuilder.DATASOURCE_USER] = "gridappsduser"
			props[DataSourceBuilder.DATASOURCE_PASSWORD] = "gridappsdpw"
			props[DataSourceBuilder.DATASOURCE_URL] = "mysql://lalala"
			props["driver"] = "com.mysql.jdbc.Driver"
			data_sources.updated(props)

			self.assertEqual(5, datasource_properties.size())
			data_sources.start()

			# Verify datasource_builder.create(datasource_name, datasource_properties)
			self.datasource_builder.create.assert_called_once_with(datasource_name, datasource_properties)

			# Verify registered_datasources.add(datasource_name)
			registered_datasources = data_sources.get_registered_datasources()
			self.assertEqual(1, len(registered_datasources))

			# Test get data source keys
			ds_keys = data_sources.get_data_source_keys()
			self.assertEqual(datasource_name, list(ds_keys)[0])

			# Test get data source by key
			obj = data_sources.get_data_source_by_key(datasource_name)
			self.assertEqual(self.datasource_object, obj)

			# Test get connection by key
			data_sources.get_connection_by_key(datasource_name)
			self.datasource_object.get_connection().assert_called_once()

			# Verify datasource_registry size
			self.assertEqual(1, len(self.datasource_registry.get_available()))

		except Exception as e:
			self.fail(str(e))


if __name__ == '__main__':
	unittest.main()
