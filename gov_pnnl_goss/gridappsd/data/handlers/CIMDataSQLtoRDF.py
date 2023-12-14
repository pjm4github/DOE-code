# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106
import logging
import sys
import xml.etree.ElementTree as ET
#from psycopg import connect as PsycopgConnector
import psycopg
from psycopg import Error as PsycopgError
# from mysql.connector import Error
# import io

from gov_pnnl_goss.SpecialClasses import IOException
from gov_pnnl_goss.gridappsd.api.LogManager import LogManager


def setup_logger():
    # Replace with your preferred Python logging setup
    logger = LogManager(__name__)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)status - %(levelname)status - %(message)status')
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


class CimDataSqlToRdf:
    CIM_NS = "http://iec.ch/TC57/CIM100#"
    RDF_NS = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    CIM_PREFIX = "cim:"
    RDF_PREFIX = "rdf:"
    ID_ATTRIBUTE = "ID"
    RESOURCE_ATTRIBUTE = "resource"

    def __init__(self):
        self.log = setup_logger()  # LogManager(self.__class__.__name__)
        # 	static HashMap<String, String> fieldNameMap = new HashMap<String, String>();
        self.field_name_map = {}
        # 	static HashMap<String, String> referenceMap = new HashMap<String, String>();
        self.reference_map = {}
        # //	static List<String> typesWithParent = new ArrayList<String>();
        self.types_with_parent = []
        # 	static List<String> booleanColumns = new ArrayList<String>();
        self.boolean_columns = []
        # 	static HashMap<String, String> joinFields = new HashMap<String, String>();
        self.join_fields = {}
        self.field_name_map["IEC61970CIMVersion.version"] = "IEC61970CIMVersion.version"
        self.field_name_map["IEC61970CIMVersion.date"] = "IEC61970CIMVersion.date"
        self.field_name_map["CoordinateSystem.mRID"] = "IdentifiedObject.mRID"
        self.field_name_map["CoordinateSystem.name"] = "IdentifiedObject.name"
        self.field_name_map["GeographicalRegion.mRID"] = "IdentifiedObject.mRID"
        self.field_name_map["GeographicalRegion.name"] = "IdentifiedObject.name"
        self.field_name_map["SubGeographicalRegion.mRID"] = "IdentifiedObject.mRID"
        self.field_name_map["SubGeographicalRegion.name"] = "IdentifiedObject.name"
        self.field_name_map["Location.mRID"] = "IdentifiedObject.mRID"
        self.field_name_map["Location.name"] = "IdentifiedObject.name"
        self.field_name_map["Line.mRID"] = "IdentifiedObject.mRID"
        self.field_name_map["Line.name"] = "IdentifiedObject.name"
        self.field_name_map["Line.Location"] = "PowerSystemResource.Location"
        self.field_name_map["TopologicalNode.mRID"] = "IdentifiedObject.mRID"
        self.field_name_map["TopologicalNode.name"] = "IdentifiedObject.name"
        self.field_name_map["ConnectivityNode.mRID"] = "IdentifiedObject.mRID"
        self.field_name_map["ConnectivityNode.name"] = "IdentifiedObject.name"
        self.field_name_map["TopologicalIsland.mRID"] = "IdentifiedObject.mRID"
        self.field_name_map["TopologicalIsland.name"] = "IdentifiedObject.name"
        self.field_name_map["BaseVoltage.mRID"] = "IdentifiedObject.mRID"
        self.field_name_map["BaseVoltage.name"] = "IdentifiedObject.name"
        self.field_name_map["EnergySource.mRID"] = "IdentifiedObject.mRID"
        self.field_name_map["EnergySource.name"] = "IdentifiedObject.name"
        self.field_name_map["EnergySource.BaseVoltage"] = "ConductingEquipment.BaseVoltage"
        self.field_name_map["EnergySource.EquipmentContainer"] = "Equipment.EquipmentContainer"
        self.field_name_map["EnergySource.Location"] = "PowerSystemResource.Location"
        self.field_name_map["Terminal.mRID"] = "IdentifiedObject.mRID"
        self.field_name_map["Terminal.name"] = "IdentifiedObject.name"
        self.field_name_map["PositionPoint.mRID"] = "IdentifiedObject.mRID"
        self.field_name_map["PositionPoint.name"] = "IdentifiedObject.name"
        self.field_name_map["LinearShuntCompensator.mRID"] = "IdentifiedObject.mRID"
        self.field_name_map["LinearShuntCompensator.name"] = "IdentifiedObject.name"
        self.field_name_map["LinearShuntCompensator.EquipmentContainer"] = "Equipment.EquipmentContainer"
        self.field_name_map["LinearShuntCompensator.BaseVoltage"] = "ConductingEquipment.BaseVoltage"
        self.field_name_map["LinearShuntCompensator.nomU"] = "ShuntCompensator.nomU"
        self.field_name_map["LinearShuntCompensator.aVRDelay"] = "ShuntCompensator.aVRDelay"
        self.field_name_map["LinearShuntCompensator.phaseConnection"] = "ShuntCompensator.phaseConnection"
        self.field_name_map["LinearShuntCompensator.grounded"] = "ShuntCompensator.grounded"
        self.field_name_map["LinearShuntCompensator.normalSections"] = "ShuntCompensator.normalSections"
        self.field_name_map["LinearShuntCompensator.maximumSections"] = "ShuntCompensator.maximumSections"
        self.field_name_map["LinearShuntCompensator.Location"] = "PowerSystemResource.Location"
        self.field_name_map["LinearShuntCompensatorPhase.mRID"] = "IdentifiedObject.mRID"
        self.field_name_map["LinearShuntCompensatorPhase.name"] = "IdentifiedObject.name"
        self.field_name_map["LinearShuntCompensatorPhase.phase"] = "ShuntCompensatorPhase.phase"
        self.field_name_map["LinearShuntCompensatorPhase.normalSections"] = "ShuntCompensatorPhase.normalSections"
        self.field_name_map["LinearShuntCompensatorPhase.maximumSections"] = "ShuntCompensatorPhase.maximumSections"
        self.field_name_map["LinearShuntCompensatorPhase.ShuntCompensator"] = "ShuntCompensatorPhase.ShuntCompensator"
        self.field_name_map["LinearShuntCompensatorPhase.Location"] = "PowerSystemResource.Location"
        self.field_name_map["RegulatingControl.mRID"] = "IdentifiedObject.mRID"
        self.field_name_map["RegulatingControl.name"] = "IdentifiedObject.name"
        self.field_name_map["RegulatingControl.Location"] = "PowerSystemResource.Location"
        self.field_name_map["PowerTransformerInfo.mRID"] = "IdentifiedObject.mRID"
        self.field_name_map["PowerTransformerInfo.name"] = "IdentifiedObject.name"
        self.field_name_map["TransformerTankInfo.mRID"] = "IdentifiedObject.mRID"
        self.field_name_map["TransformerTankInfo.name"] = "IdentifiedObject.name"
        self.field_name_map["TransformerEndInfo.mRID"] = "IdentifiedObject.mRID"
        self.field_name_map["TransformerEndInfo.name"] = "IdentifiedObject.name"
        self.field_name_map["NoLoadTest.mRID"] = "IdentifiedObject.mRID"
        self.field_name_map["NoLoadTest.name"] = "IdentifiedObject.name"
        self.field_name_map["NoLoadTest.basePower"] = "TransformerTest.basePower"
        self.field_name_map["NoLoadTest.temperature"] = "TransformerTest.temperature"
        self.field_name_map["ShortCircuitTest.mRID"] = "IdentifiedObject.mRID"
        self.field_name_map["ShortCircuitTest.name"] = "IdentifiedObject.name"
        self.field_name_map["ShortCircuitTest.basePower"] = "TransformerTest.basePower"
        self.field_name_map["ShortCircuitTest.temperature"] = "TransformerTest.temperature"
        self.field_name_map["Asset.mRID"] = "IdentifiedObject.mRID"
        self.field_name_map["Asset.name"] = "IdentifiedObject.name"
        self.field_name_map["TapChangerInfo.mRID"] = "IdentifiedObject.mRID"
        self.field_name_map["TapChangerInfo.name"] = "IdentifiedObject.name"
        self.field_name_map["TapChangerControl.mRID"] = "IdentifiedObject.mRID"
        self.field_name_map["TapChangerControl.name"] = "IdentifiedObject.name"
        self.field_name_map["TapChangerControl.mode"] = "RegulatingControl.mode"
        self.field_name_map["TapChangerControl.Terminal"] = "RegulatingControl.Terminal"
        self.field_name_map["TapChangerControl.monitoredPhase"] = "RegulatingControl.monitoredPhase"
        self.field_name_map["TapChangerControl.enabled"] = "RegulatingControl.enabled"
        self.field_name_map["TapChangerControl.discrete"] = "RegulatingControl.discrete"
        self.field_name_map["TapChangerControl.targetValue"] = "RegulatingControl.targetValue"
        self.field_name_map["TapChangerControl.targetDeadband"] = "RegulatingControl.targetDeadband"
        self.field_name_map["TapChangerControl.Location"] = "PowerSystemResource.Location"
        self.field_name_map["RatioTapChanger.mRID"] = "IdentifiedObject.mRID"
        self.field_name_map["RatioTapChanger.name"] = "IdentifiedObject.name"
        self.field_name_map["RatioTapChanger.TapChangerControl"] = "TapChanger.TapChangerControl"
        self.field_name_map["RatioTapChanger.highStep"] = "TapChanger.highStep"
        self.field_name_map["RatioTapChanger.lowStep"] = "TapChanger.lowStep"
        self.field_name_map["RatioTapChanger.neutralStep"] = "TapChanger.neutralStep"
        self.field_name_map["RatioTapChanger.normalStep"] = "TapChanger.normalStep"
        self.field_name_map["RatioTapChanger.neutralU"] = "TapChanger.neutralU"
        self.field_name_map["RatioTapChanger.initialDelay"] = "TapChanger.initialDelay"
        self.field_name_map["RatioTapChanger.subsequentDelay"] = "TapChanger.subsequentDelay"
        self.field_name_map["RatioTapChanger.ltcFlag"] = "TapChanger.ltcFlag"
        self.field_name_map["RatioTapChanger.controlEnabled"] = "TapChanger.controlEnabled"
        self.field_name_map["RatioTapChanger.step"] = "TapChanger.step"
        self.field_name_map["RatioTapChanger.Location"] = "PowerSystemResource.Location"
        self.field_name_map["ACLineSegment.mRID"] = "IdentifiedObject.mRID"
        self.field_name_map["ACLineSegment.name"] = "IdentifiedObject.name"
        self.field_name_map["ACLineSegment.EquipmentContainer"] = "Equipment.EquipmentContaine"
        self.field_name_map["ACLineSegment.BaseVoltage"] = "ConductingEquipment.BaseVoltage"
        self.field_name_map["ACLineSegment.Location"] = "PowerSystemResource.Location"
        self.field_name_map["ACLineSegment.length"] = "Conductor.length"
        self.field_name_map["ACLineSegment.Location"] = "PowerSystemResource.Location"
        self.field_name_map["ACLineSegmentPhase.mRID"] = "IdentifiedObject.mRID"
        self.field_name_map["ACLineSegmentPhase.name"] = "IdentifiedObject.name"
        self.field_name_map["ACLineSegmentPhase.Location"] = "PowerSystemResource.Location"
        self.field_name_map["LoadBreakSwitch.mRID"] = "IdentifiedObject.mRID"
        self.field_name_map["LoadBreakSwitch.name"] = "IdentifiedObject.name"
        self.field_name_map["LoadBreakSwitch.EquipmentContainer"] = "Equipment.EquipmentContainer"
        self.field_name_map["LoadBreakSwitch.BaseVoltage"] = "ConductingEquipment.BaseVoltage"
        self.field_name_map["LoadBreakSwitch.breakingCapacity"] = "ProtectedSwitch.breakingCapacity"
        self.field_name_map["LoadBreakSwitch.ratedCurrent"] = "Switch.ratedCurrent"
        self.field_name_map["LoadBreakSwitch.normalOpen"] = "Switch.normalOpen"
        self.field_name_map["LoadBreakSwitch.open"] = "Switch.open"
        self.field_name_map["LoadBreakSwitch.retained"] = "Switch.retained"
        self.field_name_map["LoadBreakSwitch.Location"] = "PowerSystemResource.Location"
        self.field_name_map["SwitchPhase.mRID"] = "IdentifiedObject.mRID"
        self.field_name_map["SwitchPhase.name"] = "IdentifiedObject.name"
        self.field_name_map["SwitchPhase.Location"] = "PowerSystemResource.Location"
        self.field_name_map["LoadResponseCharacteristic.mRID"] = "IdentifiedObject.mRID"
        self.field_name_map["LoadResponseCharacteristic.name"] = "IdentifiedObject.name"
        self.field_name_map["EnergyConsumer.mRID"] = "IdentifiedObject.mRID"
        self.field_name_map["EnergyConsumer.name"] = "IdentifiedObject.name"
        self.field_name_map["EnergyConsumer.EquipmentContainer"] = "Equipment.EquipmentContainer"
        self.field_name_map["EnergyConsumer.BaseVoltage"] = "ConductingEquipment.BaseVoltage"
        self.field_name_map["EnergyConsumer.Location"] = "PowerSystemResource.Location"
        self.field_name_map["EnergyConsumerPhase.mRID"] = "IdentifiedObject.mRID"
        self.field_name_map["EnergyConsumerPhase.name"] = "IdentifiedObject.name"
        self.field_name_map["EnergyConsumerPhase.Location"] = "PowerSystemResource.Location"
        self.field_name_map["PerLengthPhaseImpedance.mRID"] = "IdentifiedObject.mRID"
        self.field_name_map["PerLengthPhaseImpedance.name"] = "IdentifiedObject.name"
        self.field_name_map["PerLengthSequenceImpedance.mRID"] = "IdentifiedObject.mRID"
        self.field_name_map["PerLengthSequenceImpedance.name"] = "IdentifiedObject.name"
        self.field_name_map["TransformerCoreAdmittance.mRID"] = "IdentifiedObject.mRID"
        self.field_name_map["TransformerCoreAdmittance.name"] = "IdentifiedObject.name"
        self.field_name_map["TransformerMeshImpedance.mRID"] = "IdentifiedObject.mRID"
        self.field_name_map["TransformerMeshImpedance.name"] = "IdentifiedObject.name"
        self.field_name_map["PowerTransformerEnd.mRID"] = "IdentifiedObject.mRID"
        self.field_name_map["PowerTransformerEnd.name"] = "IdentifiedObject.name"
        self.field_name_map["PowerTransformerEnd.endNumber"] = "TransformerEnd.endNumber"
        self.field_name_map["PowerTransformerEnd.grounded"] = "TransformerEnd.grounded"
        self.field_name_map["PowerTransformerEnd.Terminal"] = "TransformerEnd.Terminal"
        self.field_name_map["PowerTransformerEnd.BaseVoltage"] = "TransformerEnd.BaseVoltage"
        self.field_name_map["TransformerTank.mRID"] = "IdentifiedObject.mRID"
        self.field_name_map["TransformerTank.name"] = "IdentifiedObject.name"
        self.field_name_map["TransformerTank.EquipmentContainer"] = "Equipment.EquipmentContainer"
        self.field_name_map["TransformerTank.Location"] = "PowerSystemResource.Location"
        self.field_name_map["TransformerTankEnd.mRID"] = "IdentifiedObject.mRID"
        self.field_name_map["TransformerTankEnd.name"] = "IdentifiedObject.name"
        self.field_name_map["TransformerTankEnd.endNumber"] = "TransformerEnd.endNumber"
        self.field_name_map["TransformerTankEnd.grounded"] = "TransformerEnd.grounded"
        self.field_name_map["TransformerTankEnd.Terminal"] = "TransformerEnd.Terminal"
        self.field_name_map["TransformerTankEnd.BaseVoltage"] = "TransformerEnd.BaseVoltage"
        self.field_name_map["PowerTransformer.mRID"] = "IdentifiedObject.mRID"
        self.field_name_map["PowerTransformer.name"] = "IdentifiedObject.name"
        self.field_name_map["PowerTransformer.EquipmentContainer"] = "Equipment.EquipmentContainer"
        self.field_name_map["PowerTransformer.Location"] = "PowerSystemResource.Location"
        self.field_name_map["PhaseImpedanceData.mRID"] = "IdentifiedObject.mRID"
        self.field_name_map["PhaseImpedanceData.name"] = "IdentifiedObject.name"

        self.reference_map["phaseConnection"] = "PhaseShuntConnectionKind"
        self.reference_map["phase"] = "SinglePhaseKind"
        self.reference_map["phaseSide1"] = "SinglePhaseKind"
        self.reference_map["phaseSide2"] = "SinglePhaseKind"
        self.reference_map["connectionKind"] = "WindingConnection"
        self.reference_map["phases"] = "PhaseCode"
        self.reference_map["mode"] = "RegulatingControlModeKind"
        self.reference_map["monitoredPhase"] = "PhaseCode"
        self.reference_map["tculControlMode"] = "TransformerControlMode"
        #
        #		self.types_with_parent.append("ConcentricNeutralCableInfo")
        #		self.types_with_parent.append("TapeShieldCableInfo")
        #		self.types_with_parent.append("OverheadWireInfo")
        #		self.types_with_parent.append("WireSpacingInfo")
        #		self.types_with_parent.append("TapChangerInfo")
        #		self.types_with_parent.append("TransformerTankInfo")
        #		self.types_with_parent.append("PowerTransformerEnd")
        #		self.types_with_parent.append("TransformerTankEnd")
        #		self.types_with_parent.append("PerLengthPhaseImpedance")
        #		self.types_with_parent.append("PerLengthSequenceImpedance")
        #		self.types_with_parent.append("ACLineSegment")
        #		self.types_with_parent.append("EnergySource")
        #		self.types_with_parent.append("EnergyConsumer")
        #		self.types_with_parent.append("LinearShuntCompensator")
        #		self.types_with_parent.append("PowerTransformer")
        #		self.types_with_parent.append("Breaker")
        #		self.types_with_parent.append("Recloser")
        #		self.types_with_parent.append("LoadBreakSwitch")
        #		self.types_with_parent.append("Sectionaliser")
        #		self.types_with_parent.append("Jumper")
        #		self.types_with_parent.append("Fuse")
        #		self.types_with_parent.append("Disconnector")
        self.boolean_columns.append("ShuntCompensator.grounded")
        self.boolean_columns.append("TransformerEnd.grounded")
        self.boolean_columns.append("EnergyConsumer.grounded")
        self.boolean_columns.append("TapChangerControl.enabled")
        self.boolean_columns.append("TapChangerControl.discrete")
        self.boolean_columns.append("TapChangerControl.lineDropCompensation")
        self.boolean_columns.append("cim:RegulatingControl.enabled.enabled")
        self.boolean_columns.append("cim:RegulatingControl.enabled.discrete")
        self.boolean_columns.append("cim:RegulatingControl.enabled.lineDropCompensation")
        self.boolean_columns.append("RatioTapChanger.ltcFlag")
        self.boolean_columns.append("RatioTapChanger.controlEnabled")
        self.boolean_columns.append("TapChanger.ltcFlag")
        self.boolean_columns.append("TapChanger.controlEnabled")
        self.boolean_columns.append("LoadBreakSwitch.normalOpen")
        self.boolean_columns.append("Switch.normalOpen")
        self.boolean_columns.append("LoadBreakSwitch.open")
        self.boolean_columns.append("Switch.open")
        self.boolean_columns.append("LoadBreakSwitch.retained")
        self.boolean_columns.append("Switch.retained")
        self.boolean_columns.append("LoadResponseCharacteristic.exponentModel")

        self.join_fields["ShortCircuitTest"] = "GroundedEnds"
        self.join_fields["Asset"] = "PowerSystemResources"

    def main(self, args):
        if len(args) < 4:
            print("Usage: <output file> <database url> <database user> <database password>")
            sys.exit(1)
        conn = None
        out = None
        data_location = args[0]
        db = args[1]
        user = args[2]
        pw = args[3]

        try:
            conn = psycopg.connect(f"dbname={db} user={user} password={pw}")
            # conn = sql.DriverManager.getConnection(host=db, user=user, password=pw)
            with open(data_location, "wb") as out:
                self.output_model("ieee8500", out, conn)
                # self.output_model("Feeder1", out, conn)
                # self.output_model("ieee13nodeckt", out, conn)

        except PsycopgError as e:
            self.log.error(f"Error connecting to the database: {e}")

        # try:
        #     conn = sql.DriverManager.getConnection(db, user, pw)
        #     parse = CimDataSqlToRdf()
        #     out = io.FileOutputStream(data_location)
        #     parse.output_model("ieee8500", io.BufferedWriter(io.OutputStreamWriter(out)), conn)
        #
        # except sql.SQLException as e:
        #     print(e)
        # except IOException as e:
        #     print(e)
        # finally:
        #     try:
        #         if conn is not None:
        #             conn.close()
        #         if out is not None:
        #             out.close()
        #     except Exception as e:
        #         print(e)

    def output_model(self, line_name, out, conn):
        factory = ET.ElementTree()
        factory.setroot(ET.Element("root"))
        root_element = factory.getroot()
        root_element.set("xmlns:cim", self.CIM_NS)
        root_element.set("xmlns:rdf", self.RDF_NS)

        not_found = []

        # All components that belong in the same model as the line
        line_lookup = f"SELECT distinct mc2.componentMRID, mc2.tableName, mc2.id " \
                      f"FROM ModelComponents mc1, Line l, ModelComponents mc2 " \
                      f"WHERE mc1.componentMRID=l.mRID AND l.name='{line_name}' AND mc1.mRID=mc2.mRID " \
                      f"ORDER BY mc2.id"

        self.log.debug(f"Querying line components: {line_lookup}")

        try:
            lookup_stmt = conn.cursor()
            lookup_stmt.execute(line_lookup)
            count = 0

            for (component_mrid, table_name, _) in lookup_stmt:
                count += 1
                next_element = ET.Element(f"{{{self.CIM_NS}}} {table_name}")
                next_element.set(f"{{{self.RDF_NS}}} {self.ID_ATTRIBUTE}", component_mrid)
                root_element.append(next_element)

                table_lookup = f"SELECT * FROM {table_name} WHERE mRID='{component_mrid}'"
                table_lookup_stmt = conn.cursor()
                table_lookup_stmt.execute(table_lookup)
                table_results = table_lookup_stmt.fetchone()

                for i, column in enumerate(table_lookup_stmt.column_names):
                    full_column = f"{table_name}.{column}"
                    value = table_results[i]

                    if value is not None:
                        if full_column in self.field_name_map:
                            full_column = self.field_name_map[full_column]
                        elif full_column not in not_found:
                            not_found.append(full_column)

                        if column != "Parent" and column != "SwtParent" and column != "PowerSystemResource":
                            field = ET.Element(f"{{{self.CIM_NS}}} {full_column}")

                            if column in self.reference_map:
                                field.set(f"{{{self.RDF_NS}}} {self.RESOURCE_ATTRIBUTE}",
                                          f"{self.CIM_NS}{self.reference_map[column]}.{value}")
                            elif value.startswith("_") and column != "mRID" and column != "name":
                                field.set(f"{{{self.RDF_NS}}} {self.RESOURCE_ATTRIBUTE}", f"#{value}")
                            else:
                                if full_column in self.boolean_columns:
                                    if value == "1":
                                        field.text = "true"
                                    elif value == "0":
                                        field.text = "false"
                                    else:
                                        field.text = str(bool(value))
                                else:
                                    field.text = str(value)

                            next_element.append(field)

                if table_name in self.join_fields:
                    join_field = self.join_fields[table_name]
                    lookup_table = f"{table_name}_{join_field}Join"
                    join_lookup = f"SELECT distinct {join_field} FROM {lookup_table} WHERE " \
                                  f"{table_name}='{component_mrid}'"
                    join_lookup_stmt = conn.cursor()
                    join_lookup_stmt.execute(join_lookup)

                    for (join_value,) in join_lookup_stmt:
                        field = ET.Element(f"{{{self.CIM_NS}}} {table_name}.{join_field}")
                        field.set(f"{{{self.RDF_NS}}} {self.RESOURCE_ATTRIBUTE}", f"#{join_value}")
                        next_element.append(field)

            self.log.debug(f"{count} components added to output model")

            # Save XML to the output file
            factory.write(out, encoding="utf-8", xml_declaration=True)
            self.log.debug("Output model transformation complete")

        except IOException as e:
            self.log.error(f"Error executing queries: {e}")


        # factory = ET.DocumentBuilderFactory.newInstance()
        # factory.setNamespaceAware(True)
        # builder = factory.newDocumentBuilder()
        # doc = builder.newDocument()
        # doc.setXmlStandalone(True)
        # doc.setDocumentURI(self.RDF_NS)
        # root_element = doc.createElementNS(self.RDF_NS, self.RDF_PREFIX+"RDF")
        # root_element.setAttributeNS("http://www.w3.org/2000/xmlns/", "xmlns:cim", self.CIM_NS)
        # root_element.setAttributeNS("http://www.w3.org/2000/xmlns/", "xmlns:rdf", self.RDF_NS)
        # doc.appendChild(root_element)
        #
        # not_found = []
        #
        # line_lookup = "SELECT distinct mc2.componentMRID, mc2.tableName, mc2.id FROM ModelComponents mc1, Line l, ModelComponents mc2 where mc1.componentMRID=l.mRID and l.name='"+line_name+"' and mc1.mRID=mc2.mRID order by mc2.id"
        # self.log.debug("Querying line components: "+line_lookup)
        #
        # lookup_stmt = conn.createStatement()
        # results = lookup_stmt.executeQuery(line_lookup)
        # while results.next():
        #     ...
        #     # rest of the code is omitted for brevity
