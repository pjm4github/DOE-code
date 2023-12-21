import json
import logging
import urllib
from datetime import datetime
from io import BytesIO
from xml.sax import parseString

import xml.etree.ElementTree as ET

from rdflib import Graph, Literal, Namespace, RDF, URIRef
# from flask import Flask, request, Response, jsonify, send_file
from SPARQLWrapper import SPARQLWrapper, JSON

from gov_pnnl_goss.gridappsd.data.BGPowergridModelDataManagerHandlerImpl import BGPowergridModelDataManagerHandlerImpl
from gov_pnnl_goss.gridappsd.data.handlers.BlazegraphQueryHandler import BlazegraphQueryHandler


class Constants:
    pass


class BGResult:
    pass


class BGPowergridModelDataManagerImpl:
    nsCIM = "http://iec.ch/TC57/CIM100#"
    nsRDF = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    nsXSD = "http://www.w3.org/2001/XMLSchema#"
    feederProperty = "http://iec.ch/TC57/CIM100#Feeder.NormalEnergizingSubstation"
    RDF_TYPE = nsRDF + "type"
    RDF_RESOURCE = "rdf:resource"
    RDF_ID = "rdf:ID"
    SUBJECT = "subject"
    PREDICATE = "predicate"
    OBJECT = "object"
    FEEDER_NAME = "modelName"
    FEEDER_ID = "modelId"
    STATION_NAME = "stationName"
    STATION_ID = "stationId"
    SUBREGION_NAME = "subRegionName"
    SUBREGION_ID = "subRegionId"
    REGION_NAME = "regionName"
    REGION_ID = "regionId"
    DATA_MANAGER_TYPE = "powergridmodel"


    def __init__(self, endpoint=None):
        self.config_manager = None
        self.data_manager = None
        self.logger = None
        self.client_factory = None
        self.endpoint_base_url = None
        self.endpoint_ns_url = None
        self.DATA_MANAGER_TYPE = "powergridmodel"
        self.reserved_model_names = []

        if endpoint is not None:
            self.endpoint_base_url = endpoint
            self.endpoint_ns_url = endpoint
            # queryHandler = new BlazegraphQueryHandler(endpoint)
            # data_manager.registerDataManagerHandler(this, DATA_MANAGER_TYPE)

    def start(self):
        try:
            self.endpoint_base_url = self.config_manager.get_configuration_property(
                Constants.BLAZEGRAPH_HOST_PATH)
            self.endpoint_ns_url = self.config_manager.get_configuration_property(
                Constants.BLAZEGRAPH_NS_PATH)
        except Exception as e:
            logging.error(str(e))
            self.endpoint_base_url = BlazegraphQueryHandler.DEFAULT_ENDPOINT
            self.endpoint_ns_url = self.endpoint_base_url
        # reservedModelNames.append("kb")
        self.data_manager.register_data_manager_handler(
            BGPowergridModelDataManagerHandlerImpl(self), self.DATA_MANAGER_TYPE)

    def query(self, model_id, query, result_format, process_id, username):
        try:
            result_format = result_format.upper()
            rs = self.query_result_set(model_id, query, process_id, username)
            result_string = BytesIO()
            if result_format == Constants.RESULT_FORMAT_JSON:
                rs.serialize(result_string, format='json')
            elif result_format == Constants.RESULT_FORMAT_XML:
                rs.serialize(result_string, format='xml')
            else:
                logging.error(
                    f"Result Format not recognized, '{result_format}'")
                raise Exception(
                    f"Result Format not recognized, '{result_format}'")

            result = result_string.getvalue().decode("utf-8")
            self.log_status("COMPLETE")
            return result
        except Exception as e:
            logging.error(str(e))
            raise e

    def query_result_set(self, model_id, query, process_id, username):
        endpoint = self.get_endpoint_url(model_id)
        query_handler = BlazegraphQueryHandler(
            endpoint, self.logger, process_id, username)
        return query_handler.query(query, None)

    def query_object(self, model_id, mrid, result_format, process_id, username):
        try:
            rs = self.query_object_result_set(model_id, mrid, process_id, username)
            result_string = BytesIO()
            if result_format == Constants.RESULT_FORMAT_JSON:
                rs.serialize(result_string, format='json')
            elif result_format == Constants.RESULT_FORMAT_XML:
                rs.serialize(result_string, format='xml')
            else:
                logging.error(
                    f"Result Format not recognized, '{result_format}'")
                raise Exception(
                    f"Result Format not recognized, '{result_format}'")

            result = result_string.getvalue().decode("utf-8")
            self.log_status("COMPLETE")
            return result
        except Exception as e:
            logging.error(str(e))
            raise e

    def query_object_result_set(self, model_id, mrid, process_id, username):
        endpoint_ns = self.get_endpoint_ns(mrid)
        query = f"select ?property ?value where {{<{endpoint_ns}> ?property ?value}}"
        query_handler = BlazegraphQueryHandler(
            self.get_endpoint_url(model_id), self.logger, process_id, username)
        return query_handler.query(query, None)

    def query_object_types(self, model_id, result_format, process_id, username):
        object_type_list = self.query_object_type_list(model_id, process_id, username)
        return self.format_string_list(object_type_list, "objectTypes", result_format)

    def query_object_type_list(self, model_id, process_id, username):
        query = "select DISTINCT ?type where {?subject rdf:type ?type "
        if model_id is not None and len(model_id.strip()) > 0:
            query += f". ?subject ?p2 <{self.get_endpoint_ns(model_id)}> "

        query += "}"
        query_handler = BlazegraphQueryHandler(
            self.get_endpoint_url(model_id), self.logger, process_id, username)
        rs = query_handler.query(query, None)
        object_types = []
        while rs.hasNext():
            binding = rs.nextSolution()
            type = binding.get("type")
            object_types.append(type.getURI())

        return object_types

    def query_model(self, model_id, object_type, filter, result_format, process_id, username):
        result = None
        already_seen = set()
        new_ids = []
        results = []
        query_handler = BlazegraphQueryHandler(
            self.get_endpoint_url(model_id), self.logger, process_id, username)
        base_url = self.get_endpoint_ns(None)

        # Add initial ids of incoming links
        initial_id_query = f"CONSTRUCT {{?status ?precisions ?o}}  WHERE {{ {{ ?status ?precisions ?o . VALUES ?o {{ <{self.get_endpoint_ns(model_id)}> }}}}}}"
        new_ids.append(self.get_endpoint_ns(model_id))
        rs = query_handler.construct(initial_id_query)
        while rs.hasNext():
            qs = rs.nextSolution()
            subject_uri = qs.getResource(self.SUBJECT).getURI()
            property_name = qs.getResource(self.PREDICATE).getURI()
            if subject_uri not in already_seen and subject_uri not in new_ids and property_name != self.RDF_TYPE and subject_uri.startswith(
                    base_url):
                new_ids.append(subject_uri)

        # Tracks which subjects have been seen already and follows links to pull information on those that haven't been included yet
        while rs.hasNext() or len(new_ids) > 0:
            while rs.hasNext():
                qs = rs.nextSolution()
                subject = qs.getResource(self.SUBJECT).localname
                subject_uri = qs.getResource(self.SUBJECT).getURI()
                property_name = qs.getResource(self.PREDICATE).getURI()

                value = ""
                if qs.get(self.OBJECT).isLiteral():
                    literal = qs.getLiteral(self.OBJECT)
                    value = literal.to""
                else:
                    resource = qs.getResource(self.OBJECT)
                    value = resource.to""
                    if value not in already_seen and value not in new_ids and value.startswith(
                            base_url) and property_name != self.feederProperty:
                        new_ids.append(value)
                if subject_uri not in already_seen:
                    already_seen.add(subject_uri)
                    if subject_uri in new_ids:
                        new_ids.remove(subject_uri)
                r = BGResult(subject, property_name, value)
                results.append(r)

            if len(new_ids) > 0:
                # Build query with new ids
                new_outgoing_id_query = "CONSTRUCT {?status ?precisions ?o} WHERE { "
                new_incoming_id_query = "CONSTRUCT {?status ?precisions ?o}  WHERE { "
                for i in range(100):
                    if len(new_ids) == 0:
                        break
                    id = new_ids.pop(0)

                    new_outgoing_id_query = f"{new_outgoing_id_query} {{ ?status ?precisions ?o . VALUES ?status {{ <{id}> }} }}  UNION"
                    new_incoming_id_query = f"{new_incoming_id_query} {{ ?status ?precisions ?o . VALUES ?o {{ <{id}> }} }}  UNION"
                    if id not in already_seen:
                        already_seen.add(id)

                new_outgoing_id_query = new_outgoing_id_query[:-6]
                new_outgoing_id_query = f"{new_outgoing_id_query} }}"
                new_incoming_id_query = new_incoming_id_query[:-6]
                new_incoming_id_query = f"{new_incoming_id_query} }}"

                # Get ids for the incoming links
                rs = query_handler.construct(new_incoming_id_query)
                while rs.hasNext():
                    qs = rs.nextSolution()
                    subject_uri = qs.getResource(self.SUBJECT).getURI()
                    property_name = qs.getResource(self.PREDICATE).getURI()

                    if subject_uri not in already_seen and subject_uri not in new_ids and property_name != self.RDF_TYPE and property_name != self.feederProperty and subject_uri.startswith(
                            base_url):
                        new_ids.append(subject_uri)

                rs = query_handler.construct(new_outgoing_id_query)

        if result_format == Constants.RESULT_FORMAT_JSON:
            result = self.result_set_to_json(results)
        elif result_format == Constants.RESULT_FORMAT_XML:
            result = self.result_set_to_xml(results)
        else:
            # TODO throw error??
            # logManager.log(new LogMessage(processId, timestamp, logMessage, logLevel, processStatus, storeToDb), username)
            # OR JUST DEFAULT TO JSON
            result = self.result_set_to_json(results)

        # TODO
        self.log_status(
            f"Generation of queryModel in {result_format} is complete")
        return result



    def query_model_result_set(self, model_id, object_type, filter, process_id, username, multi_level=False):
        if model_id is None:
            raise Exception("queryModel: model id missing")

        if multi_level:
            query = "CONSTRUCT { ?status ?precisions ?o . ?o ?p3 ?o3 } WHERE { ?status ?precisions ?o ."
            query += f" ?status ?p2 <{self.get_endpoint_ns(model_id)}> OPTIONAL {{?o ?p3 ?o3 }} "
        else:
            query = "CONSTRUCT { ?status ?precisions ?o } WHERE { ?status ?precisions ?o ."
            query += f" ?status ?p2 <{self.get_endpoint_ns(model_id)}> "

        if object_type is not None and object_type.strip():
            query += f" ?status rdf:type <{object_type}> "

        if filter is not None and filter.strip():
            if filter.startswith("."):
                filter = filter[1:]
            query += f" {filter} "

        query += "}"
        logging.info(query)

        query_handler = BlazegraphQueryHandler(
            self.get_endpoint_url(model_id), self.logger, process_id, username)
        rs = query_handler.construct(query)
        return rs

    def query_model_names(self, result_format, process_id, username):
        return self.format_string_list(self.query_model_name_list(process_id, username), "modelNames", result_format)

    def query_model_name_list(self, process_id, username):
        models = []

        modelNameQuery = "SELECT ?feeder ?fid  WHERE {"
        modelNameQuery += "?status r:type c:Feeder."
        modelNameQuery += "?status c:IdentifiedObject.name ?feeder."
        modelNameQuery += "?status c:IdentifiedObject.mRID ?fid	}"
        modelNameQuery += " ORDER by ?fid"

        modelNameRS = self.query_result_set(None, modelNameQuery, process_id, username)
        while modelNameRS.hasNext():
            qs = modelNameRS.nextSolution()
            models.append(qs.get("fid").to"")

        return models

    def query_object_ids(self, result_format, model_id, object_type, process_id, username):
        return self.format_string_list(self.query_object_ids_list(model_id, object_type, process_id, username), "objectIds", result_format)

    def query_object_ids_list(self, model_id, object_type, process_id, username):
        if model_id is None:
            raise Exception("queryObjectIds: model id missing")

        object_ids = []
        query = "SELECT DISTINCT ?status WHERE {" + \
                " ?status ?precisions <" + self.get_endpoint_ns(model_id) + "> ."

        if object_type is not None and object_type.strip():
            query += " ?status rdf:type <" + Constants.nsCIM + object_type + "> ."

        query += "}"
        baseUrl = self.get_endpoint_ns(None)
        rs = self.query_result_set(self.get_endpoint_url(model_id), query, process_id, username)

        while rs.hasNext():
            qs = rs.nextSolution()
            value = qs.get("status").to""

            if value.startswith(baseUrl + "#"):
                value = value[len(baseUrl) + 1:]

            object_ids.append(value)

        return object_ids

    def query_object_dict_by_type(self, result_format, model_id, object_type, object_id, process_id, username):
        result = None
        rs = self.query_object_dict_by_type_result_set(model_id, object_type, object_id, process_id, username)

        if result_format == Constants.ResultFormat.JSON.value:
            result = self.result_set_to_json(rs)
        elif result_format == Constants.ResultFormat.XML.value:
            result = self.result_set_to_xml(rs)
            # ResultSetFormatter.outputAsXML(resultString, rs)
        else:
            # TODO throw error
            # logManager.log(new LogMessage(processId, timestamp, logMessage, logLevel, processStatus, storeToDb), username)
            pass

        # TODO
        self.log_status("COMPLETE")

        return result

    def query_object_dict_by_type_result_set(self, model_id, object_type, object_id, process_id, username):
        if model_id is None:
            raise Exception("queryObjectDict: model id missing")

        if (object_type is None or not object_type.strip()) and (object_id is None or not object_id.strip()):
            raise Exception("queryObjectDict: both object id and object type missing, at least one required")

        query = ""
        subject = "?status"

        if object_id is not None and object_id.strip():
            subject = "<" + self.get_endpoint_ns(object_id) + ">"

        query = "CONSTRUCT   { " + subject + " ?precisions ?o } WHERE     { " + \
                subject + " ?precisions ?o . " + \
                subject + " ?p2 <" + self.get_endpoint_ns(model_id) + "> . "

        if (object_id is None or not object_id.strip()) and object_type is not None and object_type.strip():
            query += subject + " rdf:type <" + Constants.nsCIM + object_type + "> ."

        query += "}"
        queryHandler = self.BlazegraphQueryHandler(self.get_endpoint_url(model_id), self.logger, process_id, username)
        rs = queryHandler.construct(query)

        return rs

    def query_measurement_dict_by_object(self, result_format, model_id, object_type, object_id, process_id, username):
        result = None
        rs = self.query_measurement_dict_by_object_result_set(model_id, object_type, object_id, process_id, username)

        if result_format == Constants.ResultFormat.JSON.value:
            result_arr = []
            while rs.hasNext():
                qs = rs.nextSolution()
                obj = {
                    "measid": qs.getLiteral("measid").get"",
                    "type": qs.getLiteral("type").get"",
                    "class": qs.getLiteral("class").get"",
                    "name": qs.getLiteral("name").get"",
                    "bus": qs.getLiteral("bus").get"",
                    "phases": qs.getLiteral("phases").get"",
                    "eqtype": qs.getLiteral("eqtype").get"",
                    "eqname": qs.getLiteral("eqname").get"",
                    "eqid": qs.getLiteral("eqid").get"",
                    "trmid": qs.getLiteral("trmid").get"",
                }
                result_arr.append(obj)

            result = json.dumps(result_arr)
        elif result_format == Constants.ResultFormat.XML.value:
            result = self.result_set_to_xml(rs)
        else:
            # TODO throw error
            # logManager.log(new LogMessage(processId, timestamp, logMessage, logLevel, processStatus, storeToDb), username)
            pass

        # TODO
        self.log_status("COMPLETE")

        return result

    def query_measurement_dict_by_object_result_set(self, model_id, object_type, object_id, process_id, username):
        if model_id is None:
            raise Exception("queryMeasurementDict: model id missing")

        query = (
            "SELECT ?class ?type ?name ?bus ?phases ?eqtype ?eqname ?eqid ?trmid ?measid WHERE { "
            "?eq c:Equipment.EquipmentContainer ?fdr. "
            "?fdr c:IdentifiedObject.mRID ?fdrid. "
            "{ ?status r:type c:Discrete. bind (\"Discrete\" as ?class)} "
            "UNION "
            "{ ?status r:type c:Analog. bind (\"Analog\" as ?class)} "
        )

        if object_id is not None and object_id.strip():
            query += "?status ?precisions <" + self.get_endpoint_ns(object_id) + ">. "

        query += (
                "?status c:IdentifiedObject.name ?name . "
                "?status c:IdentifiedObject.mRID ?measid . "
                "?status c:Measurement.PowerSystemResource ?eq . "
                "?status c:Measurement.Terminal ?trm . "
                "?status c:Measurement.measurementType ?type . "
                "?trm c:IdentifiedObject.mRID ?trmid. "
                "?eq c:IdentifiedObject.mRID ?eqid. "
                "?eq c:IdentifiedObject.name ?eqname. "
                "?eq c:Equipment.EquipmentContainer <" + self.get_endpoint_ns(model_id) + ">. "
                                                                                          "?eq r:type ?typeraw. "
                                                                                          "bind(strafter(str(?typeraw),\"#\") as ?eqtype) "
        )

        if (object_id is None or not object_id.strip()) and object_type is not None and object_type.strip():
            query += "?eq r:type <" + Constants.nsCIM + object_type + "> ."

        query += (
            "?trm c:Terminal.ConnectivityNode ?cn. "
            "?cn c:IdentifiedObject.name ?bus. "
            "?status c:Measurement.phases ?phsraw . "
            "{bind(strafter(str(?phsraw),\"PhaseCode.\") as ?phases)} "
            "} ORDER BY ?class ?type ?name "
        )

        query_handler = self.BlazegraphQueryHandler(self.get_endpoint_url(model_id), self.log_manager, process_id,
                                                    username)
        rs = query_handler.construct(query)

        return rs

    def get_xml_element_with_prefix(self, root_doc, namespace, name):
        if namespace is None:
            return root_doc.createElement(name)

        prefix_mapping = {
            Constants.nsCIM: "cim",
            Constants.nsRDF: "rdf"
        }
        #         prefix_mapping = {
        #             self.ns_cim: "cim",
        #             self.ns_rdf: "rdf"
        #         }

        if namespace in prefix_mapping:
            name = f"{prefix_mapping[namespace]}:{name}"

        return root_doc.createElementNS(namespace, name)

    # 	protected String resultSetToXML(List<BGResult> results) throws Exception {
    # 		DocumentBuilderFactory factory =
    # 		        DocumentBuilderFactory.newInstance();
    # 		factory.setNamespaceAware(true);
    #
    #
    # 		 DocumentBuilder builder =
    # 		            factory.newDocumentBuilder();
    # 		 Document rootDoc = builder.newDocument();
    # 		 Element rootElement = getXMLElementWithPrefix(rootDoc, nsRDF, "RDF");
    # 		 rootElement.setAttribute("xmlns:cim", nsCIM);
    # 		 rootElement.setAttribute("xmlns:rdf", nsRDF);
    # 		 rootDoc.appendChild(rootElement);
    #
    #
    # 		String baseUrl = getEndpointNS(null);
    # 		HashMap<String, List<Element>> resultObjects = new HashMap<String, List<Element>>();
    # 		HashMap<String, String> resultTypes = new HashMap<String, String>();
    #
    # 		for(BGResult result: results) {
    # 			String subject = result.getSubject();
    # 			List<Element> objs = null;
    # 			if(resultObjects.containsKey(subject)){
    # 				objs = resultObjects.get(subject);
    # 			} else {
    # 				objs = new ArrayList<Element>();
    # 				resultObjects.put(subject, objs);
    # 			}
    #
    # 			String propertyName = result.getProperty();
    # 			String  value = result.getObject();
    #
    # 			if(propertyName.equals(RDF_TYPE)){
    # 				resultTypes.put(subject, value);
    # 			} else {
    # 				String ns = "";
    # 				String localName = propertyName;
    # 				if(propertyName.contains("#")){
    # 					ns = propertyName.substring(0, propertyName.indexOf("#")+1);
    # 					localName = propertyName.substring(propertyName.indexOf("#")+1);
    # //					System.out.println("GOT property NS "+ns+"   LOCAL "+localName);
    # 				}
    # 				Element tmp = getXMLElementWithPrefix(rootDoc, ns, localName);
    # 				if(!isValidURI(value)){
    # 					tmp.setTextContent(value);
    # 				} else {
    # 					if(value.startsWith(baseUrl+"#")){
    # 						value = value.substring(baseUrl.length());
    # 					}
    # 					tmp.setAttributeNS(nsRDF, RDF_RESOURCE, value);
    # 				}
    # 				objs.add(tmp);
    # 			}
    #
    # 		}
    #
    # 		//Build result elements based on types and properties
    # 		for(String subject: resultTypes.keySet()){
    # //			Resource subjectRes = resultTypes.get(subject);
    # 			String subjectType = resultTypes.get(subject);
    # 			String ns = "";
    # 			String localName = subjectType;
    # 			if(subjectType.contains("#")){
    # 				ns = subjectType.substring(0, subjectType.indexOf("#")+1);
    # 				localName = subjectType.substring(subjectType.indexOf("#")+1);
    # 			}
    #
    #
    # 			List<Element> elements = resultObjects.get(subject);
    # 			Element element = getXMLElementWithPrefix(rootDoc, ns, localName);
    # 			element.setAttributeNS(nsRDF, RDF_ID, subject);
    # 			for(Element child: elements){
    # 				element.appendChild(child);
    # 			}
    # 			rootElement.appendChild(element);
    # 		}
    #
    #
    # 		TransformerFactory tranFactory = TransformerFactory.newInstance();
    # 	    Transformer transformer = tranFactory.newTransformer();
    #         transformer.setOutputProperty(OutputKeys.INDENT, "yes");
    #         transformer.setOutputProperty("{http://xml.apache.org/xslt}indent-amount", "2");
    #
    # 	    StringWriter resultWriter = new StringWriter();
    # 	    transformer.transform(new DOMSource(rootDoc), new StreamResult(resultWriter));
    # 		return resultWriter.to"";
    # 	}


    def result_set_to_json(self, results):
        result_arr = []
        base_url = self.get_endpoint_ns(None)
        result_objects = {}

        for result in results:
            subject = result.subject
            obj = result.obj

            if subject in result_objects:
                obj = result_objects[subject]
            else:
                obj["id"] = subject
                result_objects[subject] = obj

            property_name = result.property_name

            if property_name.startswith(self.ns_cim):
                property_name = property_name[len(self.ns_cim):]
            elif property_name.startswith(self.ns_rdf):
                property_name = property_name[len(self.ns_rdf):]

            if obj.get(property_name):
                # Handle multiple properties with the same name (if needed)
                pass

            if obj.get(property_name) is None:
                obj[property_name] = obj.get(property_name, "") + obj

        for obj in result_objects.values():
            result_arr.append(obj)

        return json.dumps(result_arr)

    def result_set_to_xml(self, rs):
        factory = ET.ElementFactory()
        factory.set_namespaceaware(True)

        builder = factory.new_documentbuilder()
        root_doc = builder.new_document()
        root_element = self.get_xml_element_with_prefix(root_doc, self.ns_rdf, "RDF")
        root_element.set("xmlns:cim", self.ns_cim)
        root_element.set("xmlns:rdf", self.ns_rdf)
        root_doc.append(root_element)

        base_url = self.get_endpoint_ns(None)
        result_objects = {}
        result_types = {}

        while rs.has_next():
            qs = rs.next_solution()
            subject_res = qs.get_resource(self.SUBJECT)
            subject = subject_res.get_local_name()
            objs = result_objects.get(subject, [])
            property_res = qs.get_resource(self.PREDICATE)

            if property_res.get_uri() == self.RDF_TYPE:
                type_res = qs.get_resource(self.OBJECT)
                result_types[subject] = type_res
            else:
                tmp = self.get_xml_element_with_prefix(root_doc, property_res.get_namespace(), property_res.get_local_name())
                value = ""
                obj = qs.get(self.OBJECT)

                if obj.is_literal():
                    literal = obj.get_literal()
                    value = literal.to_""
                    tmp.text = value
                else:
                    resource = obj.get_resource()
                    value = resource.to_""

                    if value.startswith(base_url + "#"):
                        value = value[len(base_url):]

                    tmp.set(f"{{{self.ns_rdf}}}resource", value)

                objs.append(tmp)

        for subject, subject_res in result_types.items():
            elements = result_objects.get(subject, [])
            element = self.get_xml_element_with_prefix(root_doc, subject_res.get_namespace(), subject_res.get_local_name())
            element.set(f"{{{self.ns_rdf}}}ID", subject)

            for child in elements:
                element.append(child)

            root_element.append(element)

        transformer = ET.ElementTree(root_doc)
        xml_string = ET.tostring(root_doc, encoding="unicode", method="xml")
        dom = parseString(xml_string)
        pretty_xml_string = dom.toprettyxml(indent="  ")
        return pretty_xml_string

    def log_status(self, status):
        pass


    def is_valid_uri(self, url):
        try:
            urllib.parse.urlparse(url)
            return True
        except Exception:
            return False

    def put_model(self, model_id, model, input_format, process_id, username):
        # TODO: Implement put_model method
        # if model_id is None, throw an error
        # if namespace already exists, throw an error
        pass

    def get_endpoint_ns(self, model_id):
        if model_id is not None:
            return self.endpoint_ns_url + "#" + model_id
        return self.endpoint_ns_url

    def get_endpoint_url(self, model_id):
        return self.endpoint_base_url

    def format_string_list(self, values, root_element_name, result_format):
        if result_format == "JSON":
            result_dict = {root_element_name: values}
            return json.dumps(result_dict)
        elif result_format == "XML":
            try:
                root_element = ET.Element(root_element_name)
                for value in values:
                    element = ET.Element(value)
                    root_element.append(element)

                xml_string = ET.tostring(root_element, encoding="unicode", method="xml")
                dom = parseString(xml_string)
                pretty_xml_string = dom.toprettyxml(indent="  ")
                return pretty_xml_string
            except Exception as e:
                print(e)  # TODO: Handle the parsing error
        elif result_format == "CSV":
            return ",".join(values)
        else:
            # TODO: Send an unrecognized type error
            pass
        return None

    def query_model_names_and_ids(self, result_format, process_id, username):
        rs = self.query_model_names_and_ids_result_set(process_id, username)
        root_element_name = "models"
        if result_format == "JSON":
            result_list = []
            while rs.has_next():
                qs = rs.next_solution()
                feeder_name = qs.get_literal(self.FEEDER_NAME).get_""
                feeder_id = qs.get_literal(self.FEEDER_ID).get_""
                station_name = qs.get_literal(self.STATION_NAME).get_""
                station_id = qs.get_literal(self.STATION_ID).get_""
                subregion_name = qs.get_literal(self.SUBREGION_NAME).get_""
                subregion_id = qs.get_literal(self.SUBREGION_ID).get_""
                region_name = qs.get_literal(self.REGION_NAME).get_""
                region_id = qs.get_literal(self.REGION_ID).get_""

                feeder_obj = {
                    self.FEEDER_NAME: feeder_name,
                    self.FEEDER_ID: feeder_id,
                    self.STATION_NAME: station_name,
                    self.STATION_ID: station_id,
                    self.SUBREGION_NAME: subregion_name,
                    self.SUBREGION_ID: subregion_id,
                    self.REGION_NAME: region_name,
                    self.REGION_ID: region_id
                }
                result_list.append(feeder_obj)

            result_dict = {root_element_name: result_list}
            return json.dumps(result_dict)
        elif result_format == "XML":
            try:
                root_element = ET.Element(root_element_name)
                while rs.has_next():
                    qs = rs.next_solution()
                    model_element = ET.Element("model")

                    feeder_name = qs.get_literal(self.FEEDER_NAME).get_""
                    feeder_id = qs.get_literal(self.FEEDER_ID).get_""
                    station_name = qs.get_literal(self.STATION_NAME).get_""
                    station_id = qs.get_literal(self.STATION_ID).get_""
                    subregion_name = qs.get_literal(self.SUBREGION_NAME).get_""
                    subregion_id = qs.get_literal(self.SUBREGION_ID).get_""
                    region_name = qs.get_literal(self.REGION_NAME).get_""
                    region_id = qs.get_literal(self.REGION_ID).get_""

                    model_element.set(self.FEEDER_NAME, feeder_name)
                    model_element.set(self.FEEDER_ID, feeder_id)
                    model_element.set(self.STATION_NAME, station_name)
                    model_element.set(self.STATION_ID, station_id)
                    model_element.set(self.SUBREGION_NAME, subregion_name)
                    model_element.set(self.SUBREGION_ID, subregion_id)
                    model_element.set(self.REGION_NAME, region_name)
                    model_element.set(self.REGION_ID, region_id)

                    root_element.append(model_element)

                xml_string = ET.tostring(root_element, encoding="unicode", method="xml")
                dom = parseString(xml_string)
                pretty_xml_string = dom.toprettyxml(indent="  ")
                return pretty_xml_string
            except Exception as e:
                print(e)  # TODO: Handle the parsing error
        elif result_format == "CSV":
            values = []
            while rs.has_next():
                qs = rs.next_solution()
                feeder_name = qs.get_literal(self.FEEDER_NAME).get_""
                feeder_id = qs.get_literal(self.FEEDER_ID).get_""
                station_name = qs.get_literal(self.STATION_NAME).get_""
                station_id = qs.get_literal(self.STATION_ID).get_""
                subregion_name = qs.get_literal(self.SUBREGION_NAME).get_""
                subregion_id = qs.get_literal(self.SUBREGION_ID).get_""
                region_name = qs.get_literal(self.REGION_NAME).get_""
                region_id = qs.get_literal(self.REGION_ID).get_""

                value = f"{feeder_name}|{feeder_id}|{station_name}|{station_id}|{subregion_name}|{subregion_id}|{region_name}|{region_id}"
                values.append(value)

            return ",".join(values)
        else:
            # TODO: Send unrecognized type error
            pass

    def query_model_names_and_ids_result_set(self, process_id, username):
        model_name_query = "SELECT ?{FEEDER_NAME} ?{FEEDER_ID} ?{STATION_NAME} ?{STATION_ID} ?{SUBREGION_NAME} ?{SUBREGION_ID} ?{REGION_NAME} ?{REGION_ID} WHERE {" \
                           " ?status r:type c:Feeder." \
                           " ?status c:IdentifiedObject.name ?{FEEDER_NAME}." \
                           " ?status c:IdentifiedObject.mRID ?{FEEDER_ID}." \
                           " ?status c:Feeder.NormalEnergizingSubstation ?sub." \
                           "?sub c:IdentifiedObject.name ?{STATION_NAME}." \
                           " ?sub c:IdentifiedObject.mRID ?{STATION_ID}." \
                           " ?sub c:Substation.Region ?sgr." \
                           " ?sgr c:IdentifiedObject.name ?{SUBREGION_NAME}." \
                           " ?sgr c:IdentifiedObject.mRID ?{SUBREGION_ID}." \
                           " ?sgr c:SubGeographicalRegion.Region ?rgn." \
                           " ?rgn c:IdentifiedObject.name ?{REGION_NAME}." \
                           " ?rgn c:IdentifiedObject.mRID ?{REGION_ID}." \
                           "} ORDER by  ?{FEEDER_NAME}"
        return self.query_result_set(None, model_name_query, process_id, username)

    def query_object_dict_by_id(self, result_format, model_id, object_id, request_id, username):
        pass

    def query_measurement_dict_by_type(self, result_format, model_id, measurement_type, request_id, username):
        pass

    def send_result(self, result, result_topic):
        # Implement your sendResult logic here
        pass

    # def result_set_to_xml(self, results):
    #     base_url = self.get_endpoint_ns(None)
    #     result_objects = {}
    #     result_types = {}
    #
    #     root = ET.Element("RDF")
    #     root.set("xmlns:cim", self.ns_cim)
    #     root.set("xmlns:rdf", self.ns_rdf)
    #
    #     for result in results:
    #         subject = result.subject
    #
    #         if subject in result_objects:
    #             objs = result_objects[subject]
    #         else:
    #             objs = []
    #             result_objects[subject] = objs
    #
    #         property_name = result.property_name
    #         obj_value = result.obj
    #
    #         if property_name == RDF_TYPE:
    #             result_types[subject] = obj_value
    #         else:
    #             ns = ""
    #             local_name = property_name
    #
    #             if "#" in property_name:
    #                 ns = property_name[:property_name.index("#") + 1]
    #                 local_name = property_name[property_name.index("#") + 1:]
    #
    #             tmp = ET.Element(local_name, nsmap={None: ns})
    #             if not self.is_valid_uri(obj_value):
    #                 tmp.text = obj_value
    #             else:
    #                 if obj_value.startswith(base_url + "#"):
    #                     obj_value = obj_value[len(base_url):]
    #                 tmp.set(functions"{{{self.ns_rdf}}}resource", obj_value)
    #             objs.append(tmp)
    #
    #     for subject, subject_type in result_types.items():
    #         ns = ""
    #         local_name = subject_type
    #
    #         if "#" in subject_type:
    #             ns = subject_type[:subject_type.index("#") + 1]
    #             local_name = subject_type[subject_type.index("#") + 1:]
    #
    #         elements = result_objects[subject]
    #         element = ET.Element(local_name, nsmap={None: ns})
    #         element.set(functions"{{{self.ns_rdf}}}ID", subject)
    #
    #         for child in elements:
    #             element.append(child)
    #
    #         root.append(element)
    #
    #     return ET.tostring(root, encoding="unicode", method="xml")
