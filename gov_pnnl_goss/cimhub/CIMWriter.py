from gov_pnnl_goss.cimhub.CIMImporter import CIMImporter
#
# from gov_pnnl_goss.cimhub.components.DistBaseVoltage import DistBaseVoltage
#
# from gov_pnnl_goss.cimhub.components.DistBaseVoltage import DistBaseVoltage
# from gov_pnnl_goss.cimhub.components.DistBreaker import DistBreaker
# from gov_pnnl_goss.cimhub.components.DistCapacitor import DistCapacitor
from gov_pnnl_goss.cimhub.components.DistComponent import DistComponent
# from gov_pnnl_goss.cimhub.components.DistConcentricNeutralCable import DistConcentricNeutralCable
# from gov_pnnl_goss.cimhub.components.DistCoordinates import DistCoordinates
# from gov_pnnl_goss.cimhub.components.DistDisconnector import DistDisconnector
# from gov_pnnl_goss.cimhub.components.DistFeeder import DistFeeder
# from gov_pnnl_goss.cimhub.components.DistFuse import DistFuse
# from gov_pnnl_goss.cimhub.components.DistGroundDisconnector import DistGroundDisconnector
# from gov_pnnl_goss.cimhub.components.DistHouse import DistHouse
# from gov_pnnl_goss.cimhub.components.DistJumper import DistJumper
# from gov_pnnl_goss.cimhub.components.DistLineSegment import DistLineSegment
# from gov_pnnl_goss.cimhub.components.DistLineSpacing import DistLineSpacing
# from gov_pnnl_goss.cimhub.components.DistLinesCodeZ import DistLinesCodeZ
# from gov_pnnl_goss.cimhub.components.DistLinesInstanceZ import DistLinesInstanceZ
# from gov_pnnl_goss.cimhub.components.DistLinesSpacingZ import DistLinesSpacingZ
# from gov_pnnl_goss.cimhub.components.DistLoad import DistLoad
# from gov_pnnl_goss.cimhub.components.DistLoadBreakSwitch import DistLoadBreakSwitch
# from gov_pnnl_goss.cimhub.components.DistMeasurement import DistMeasurement
# from gov_pnnl_goss.cimhub.components.DistOverheadWire import DistOverheadWire
# from gov_pnnl_goss.cimhub.components.DistPhaseMatrix import DistPhaseMatrix
# from gov_pnnl_goss.cimhub.components.DistPowerXfmrCore import DistPowerXfmrCore
# from gov_pnnl_goss.cimhub.components.DistPowerXfmrMesh import DistPowerXfmrMesh
# from gov_pnnl_goss.cimhub.components.DistPowerXfmrWinding import DistPowerXfmrWinding
# from gov_pnnl_goss.cimhub.components.DistRecloser import DistRecloser
# from gov_pnnl_goss.cimhub.components.DistRegulator import DistRegulator
# from gov_pnnl_goss.cimhub.components.DistSectionaliser import DistSectionaliser
# from gov_pnnl_goss.cimhub.components.DistSequenceMatrix import DistSequenceMatrix
# from gov_pnnl_goss.cimhub.components.DistSolar import DistSolar
# from gov_pnnl_goss.cimhub.components.DistStorage import DistStorage
# from gov_pnnl_goss.cimhub.components.DistSubstation import DistSubstation
# from gov_pnnl_goss.cimhub.components.DistSwitch import DistSwitch
# from gov_pnnl_goss.cimhub.components.DistSyncMachine import DistSyncMachine
# from gov_pnnl_goss.cimhub.components.DistTapeShieldCable import DistTapeShieldCable
# from gov_pnnl_goss.cimhub.components.DistXfmrBank import DistXfmrBank
# from gov_pnnl_goss.cimhub.components.DistXfmrCodeOCTest import DistXfmrCodeOCTest
# from gov_pnnl_goss.cimhub.components.DistXfmrCodeRating import DistXfmrCodeRating
# from gov_pnnl_goss.cimhub.components.DistXfmrCodeSCTest import DistXfmrCodeSCTest
# from gov_pnnl_goss.cimhub.components.DistXfmrTank import DistXfmrTank

import uuid


class CIMWriter:
    # Define constants
    xnsCIM = "http://iec.ch/TC57/2009/CIM-schema-cim14#"
    xnsRDF = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"

    szCN = """
    SELECT ?name ?voltage_id WHERE {
     ?fdr c:IdentifiedObject.mRID ?fdrid.
     ?status c:ConnectivityNode.ConnectivityNodeContainer ?fdr.
     ?status r:type c:ConnectivityNode.
     ?status c:IdentifiedObject.name ?name.
     bind(strafter(str(?status),"#") as ?voltage_id).
    } ORDER by ?name
    """

    szTRM = """
    SELECT ?eqclass ?eqname ?seq ?name ?eqid ?tid ?cnid WHERE {
     ?fdr c:IdentifiedObject.mRID ?fdrid.
     ?eq c:Equipment.EquipmentContainer ?fdr.
     ?t c:Terminal.ConductingEquipment ?eq.
     ?t c:Terminal.ConnectivityNode ?cn.
     ?t c:ACDCTerminal.sequenceNumber ?seq.
     bind(strafter(str(?eq),"#") as ?eqid).
     bind(strafter(str(?t),"#") as ?tid).
     bind(strafter(str(?cn),"#") as ?cnid).
     ?t c:IdentifiedObject.name ?name.
     ?eq c:IdentifiedObject.name ?eqname.
     ?eq a ?classraw.
     bind(strafter(str(?classraw),"CIM100#") as ?eqclass)
    } ORDER by ?eqclass ?eqname ?seq
    """

    szEND = """
    SELECT ?endclass ?endid ?tid WHERE {
     ?fdr c:IdentifiedObject.mRID ?fdrid.
     {?pxf c:Equipment.EquipmentContainer ?fdr.
      ?end c:PowerTransformerEnd.PowerTransformer ?pxf.}
     UNION
     {?tank c:Equipment.EquipmentContainer ?fdr.
      ?end c:TransformerTankEnd.TransformerTank ?tank.}
     ?end c:TransformerEnd.Terminal ?t.
     ?t c:ACDCTerminal.sequenceNumber ?seq.
     bind(strafter(str(?end),"#") as ?endid).
     bind(strafter(str(?t),"#") as ?tid).
     ?end a ?classraw.
     bind(strafter(str(?classraw),"CIM100#") as ?endclass)
    } ORDER by ?endclass ?endid
    """
    # TODO: this only gets locations for conducting equipment, not other types of PSR
    szLOC = """
    SELECT DISTINCT ?eqname ?name ?eqid ?locid WHERE {
     ?fdr c:IdentifiedObject.mRID ?fdrid.
     ?eq c:Equipment.EquipmentContainer ?fdr.
     ?eq c:PowerSystemResource.Location ?loc.
     bind(strafter(str(?loc),"#") as ?locid).
     bind(strafter(str(?eq),"#") as ?eqid).
     ?eq c:IdentifiedObject.name ?eqname.
     ?loc c:IdentifiedObject.name ?name.
    } ORDER by ?eqname
    """

    szPOS = """
    SELECT DISTINCT ?locid ?voltage_id ?seq ?x ?y WHERE {
     ?fdr c:IdentifiedObject.mRID ?fdrid.
     ?eq c:Equipment.EquipmentContainer ?fdr.
     ?eq c:PowerSystemResource.Location ?loc.
     ?precisions c:PositionPoint.Location ?loc.
     ?precisions c:PositionPoint.sequenceNumber ?seq.
     ?precisions c:PositionPoint.xPosition ?x.
     ?precisions c:PositionPoint.yPosition ?y.
     bind(strafter(str(?loc),"#") as ?locid).
     bind(strafter(str(?precisions),"#") as ?voltage_id).
    } ORDER by ?locid ?seq
    """

    szXFINF = """
    SELECT ?tname ?ename ?seq ?tid ?eid WHERE {
     ?e c:TransformerEndInfo.TransformerTankInfo ?t.
     ?t c:IdentifiedObject.name ?tname.
     ?t c:IdentifiedObject.mRID ?tid.
     ?e c:IdentifiedObject.name ?ename.
     ?e c:IdentifiedObject.mRID ?eid.
     ?e c:TransformerEndInfo.endNumber ?seq.
    } ORDER BY ?tname ?ename ?seq
    """

    def __init__(self):
        self.query_handler = None
        self.map_locations = {}
        self.map_windings = {}
        self.set_locations = set()
        self.fdrID = ""
        self.rgnID = ""
        self.subrgnID = ""
        self.subID = ""

    def shorten_uuid(self, uuid_str):
        return uuid_str[1:].replace("-", "")

    def start_instance(self, root, id, out):
        out.println(f"<cim:{root} rdf:ID=\"{id}\">")

    def start_free_instance(self, root, out):
        id = self.shorten_uuid("_" + str(uuid.uuid4()).upper())
        self.start_instance(root, id, out)

    def end_instance(self, root, out):
        out.println(f"</cim:{root}>")

    def string_node(self, key, val, out):
        out.println(f"  <cim:{key}>{val}</cim:{key}>")

    def double_node(self, key, val, out):
        out.println(f"  <cim:{key}>{val:.8g}</cim:{key}>")

    def integer_node(self, key, val, out):
        out.println(f"  <cim:{key}>{val}</cim:{key}>")

    def bool_node(self, key, val, out):
        out.println(f"  <cim:{key}>{val}</cim:{key}>")

    def ref_node(self, key, val, out):
        out.println(f"  <cim:{key} rdf:resource=\"#{val}\"/>")

    def winding_connection_enum(self, conn, out):
        out.println(f"  <cim:WindingInfo.connectionKind rdf:resource=\"{self.xnsCIM}WindingConnection.{conn}\"/>")

    def xf_winding_connection_enum(self, conn, out):
        out.println(f"  <cim:TransformerWinding.connectionType rdf:resource=\"{self.xnsCIM}WindingConnection.{conn}\"/>")

    def xf_winding_type_enum(self, end_number, out):
        if end_number == 1:
            val = "primary"
        elif end_number == 2:
            val = "secondary"
        elif end_number == 3:
            val = "tertiary"
        else:
            val = "quaternary"
        out.println(f"  <cim:TransformerWinding.windingType rdf:resource=\"{self.xnsCIM}WindingType.{val}\"/>")

    def phases_enum(self, phs, out):
        val = ""
        if "s1" in phs:
            if "s2" in phs:
                val = "splitSecondary12N"
            else:
                val = "splitSecondary1N"
        elif "s2" in phs:
            val = "splitSecondary2N"
        else:
            val = phs
        out.println(f"  <cim:ConductingEquipment.phases rdf:resource=\"{self.xnsCIM}PhaseCode.{val}\"/>")

    def load_transformer_info(self, out):
        results = self.query_handler.query(self.szXFINF, "xf info")
        last_name = ""
        for soln in results:
            tname = DistComponent.safe_name(soln.get("?tname").toString())
            tid = self.shorten_uuid(soln.get("?tid").toString())
            ename = DistComponent.safe_name(soln.get("?ename").toString())
            eid = self.shorten_uuid(soln.get("?eid").toString())
            if tname != last_name:
                self.start_instance("TransformerInfo", tid, out)
                self.string_node("IdentifiedObject.mRID", tid, out)
                self.string_node("IdentifiedObject.name", tname, out)
                self.end_instance("TransformerInfo", out)
                self.map_windings[tid] = []
                last_name = tname
            self.map_windings[tid].append(eid)
        results.close()

    def load_connectivity_nodes(self, out):
        results = self.query_handler.query(self.szCN, "CN")
        for soln in results:
            name = DistComponent.safe_name(soln.get("?name").toString())
            id = self.shorten_uuid(soln.get("?voltage_id").toString())
            self.start_instance("ConnectivityNode", id, out)
            self.string_node("IdentifiedObject.mRID", id, out)
            self.string_node("IdentifiedObject.name", name, out)
            self.end_instance("ConnectivityNode", out)
        results.close()

    def load_terminals(self, out):
        map_ends = {}
        res_ends = self.query_handler.query(self.szEND, "ends")
        while res_ends.has_next():
            soln = res_ends.next()
            end_id = self.shorten_uuid(soln.get("?endid").to_string())
            tid = self.shorten_uuid(soln.get("?tid").to_string())
            map_ends[tid] = end_id
        res_ends.close()

        results = self.query_handler.query(self.szTRM, "TRM")
        while results.has_next():
            soln = results.next()
            name = DistComponent.safe_name(soln.get("?name").to_string())
            tid = self.shorten_uuid(soln.get("?tid").to_string())
            eq_id = self.shorten_uuid(soln.get("?eqid").to_string())
            cn_id = self.shorten_uuid(soln.get("?cnid").to_string())
            eq_class = soln.get("?eqclass").to_string()
            seq = int(soln.get("?seq").to_string())
            self.start_instance("Terminal", tid, out)
            self.string_node("IdentifiedObject.mRID", tid, out)
            self.string_node("IdentifiedObject.name", name, out)
            self.string_node("Terminal.connected", "true", out)
            self.ref_node("Terminal.ConnectivityNode", cn_id, out)
            if eq_class == "PowerTransformer":
                self.ref_node("Terminal.ConductingEquipment", map_ends[tid], out)
                self.integer_node("Terminal.sequenceNumber", 1, out)
            else:
                self.ref_node("Terminal.ConductingEquipment", eq_id, out)
                self.integer_node("Terminal.sequenceNumber", seq, out)  # after CIM14, it'status ACDCTerminal.sequenceNumber
            self.end_instance("Terminal", out)
        results.close()

    def load_locations(self, out):
        results = self.query_handler.query(self.szLOC, "LOC")
        while results.has_next():
            soln = results.next()
            name = DistComponent.safe_name(soln.get("?name").to_string())
            loc_id = self.shorten_uuid(soln.get("?locid").to_string())
            eq_id = self.shorten_uuid(soln.get("?eqid").to_string())
            if loc_id not in self.set_locations:
                self.start_instance("GeoLocation", loc_id, out)
                self.string_node("IdentifiedObject.mRID", loc_id, out)
                self.string_node("IdentifiedObject.name", name, out)
                self.end_instance("GeoLocation", out)
                self.set_locations.add(loc_id)
            self.map_locations[eq_id] = loc_id
        results.close()

    # def load_locations(self, out):
    #     results = self.query_handler.query(self.szLOC, "Load Locations")
    #     for soln in results:
    #         name = DistComponent.safe_name(soln.get("?name").toString())
    #         voltage_id = self.shorten_uuid(soln.get("?voltage_id").toString())
    #         lat = soln.get("?lat").toString()
    #         lon = soln.get("?lon").toString()
    #         altitude = soln.get("?altitude").toString()
    #
    #         self.start_instance("Location", voltage_id, out)
    #         self.string_node("IdentifiedObject.mRID", voltage_id, out)
    #         self.string_node("IdentifiedObject.name", name, out)
    #         self.string_node("Location.Latitude", lat, out)
    #         self.string_node("Location.Longitude", lon, out)
    #         self.string_node("Location.Altitude", altitude, out)
    #         self.end_instance("Location", out)
    #
    #     results.close()

    # def load_energy_consumers(self, out):
    #     results = self.query_handler.query(self.szEC, "EC")
    #     for soln in results:
    #         name = DistComponent.safe_name(soln.get("?name").toString())
    #         voltage_id = self.shorten_uuid(soln.get("?voltage_id").toString())
    #         precisions = soln.get("?precisions").toString()
    #         q = soln.get("?q").toString()
    #         self.start_instance("EnergyConsumer", voltage_id, out)
    #         self.string_node("IdentifiedObject.mRID", voltage_id, out)
    #         self.string_node("IdentifiedObject.name", name, out)
    #         self.double_node("EnergyConsumer.precisions", float(precisions), out)
    #         self.double_node("EnergyConsumer.q", float(q), out)
    #         self.end_instance("EnergyConsumer", out)
    #     results.close()

    def load_position_points(self, out):
        results = self.query_handler.query(self.szPOS, "POS PTS")
        while results.has_next():
            soln = results.next()
            id = self.shorten_uuid(soln.get("?voltage_id").to_string())
            loc_id = self.shorten_uuid(soln.get("?locid").to_string())
            seq = int(soln.get("?seq").to_string())
            x = float(soln.get("?x").to_string())
            y = float(soln.get("?y").to_string())
            self.start_instance("PositionPoint", id, out)
            self.ref_node("PositionPoint.Location", loc_id, out)
            self.integer_node("PositionPoint.sequenceNumber", seq, out)
            self.double_node("PositionPoint.xPosition", x, out)
            self.double_node("PositionPoint.yPosition", y, out)
            self.end_instance("PositionPoint", out)
        results.close()

    # def load_position_points(self, out):
    #     results = self.query_handler.query(self.szPOC, "Load Position Points")
    #     for soln in results:
    #         voltage_id = self.shorten_uuid(soln.get("?voltage_id").toString())
    #         sequence_number = soln.get("?sequenceNumber").toString()
    #         x = soln.get("?x").toString()
    #         y = soln.get("?y").toString()
    #         z = soln.get("?z").toString()
    #
    #         self.start_instance("PositionPoint", voltage_id, out)
    #         self.string_node("IdentifiedObject.mRID", voltage_id, out)
    #         self.string_node("PositionPoint.sequenceNumber", sequence_number, out)
    #         self.string_node("PositionPoint.xPosition", x, out)
    #         self.string_node("PositionPoint.yPosition", y, out)
    #         self.string_node("PositionPoint.zPosition", z, out)
    #         self.end_instance("PositionPoint", out)
    #
    #     results.close()

    def distribution_line_segment(self, obj, psrtype, out):
        obj_id = self.shorten_uuid(obj.id)
        self.start_instance("DistributionLineSegment", obj_id, out)
        self.string_node("IdentifiedObject.mRID", obj_id, out)
        self.string_node("IdentifiedObject.name", obj.name, out)
        self.double_node("Conductor.length", obj.len, out)
        self.ref_node("Equipment.EquipmentContainer", self.fdrID, out)
        self.ref_node("PowerSystemResource.PSRType", psrtype, out)
        self.ref_node("PowerSystemResource.GeoLocation", self.map_locations.get(obj_id), out)
        self.phases_enum(obj.phases, out)
        self.end_instance("DistributionLineSegment", out)

    # def distribution_line_segment(self, voltage_id, out):
    #     results = self.query_handler.query(self.szT, "Distribution Line Segment")
    #
    #     for soln in results:
    #         voltage_id = self.shorten_uuid(soln.get("?voltage_id").toString())
    #         name = soln.get("?name").toString()
    #         description = soln.get("?description").toString()
    #
    #         self.start_instance("DistributionLineSegment", voltage_id, out)
    #         self.string_node("IdentifiedObject.mRID", voltage_id, out)
    #         self.string_node("IdentifiedObject.name", name, out)
    #         self.string_node("IdentifiedObject.description", description, out)
    #
    #         self.end_instance("DistributionLineSegment", out)
    #
    #     results.close()

    def start_switch(self, class_name, obj, out):
        obj_id = self.shorten_uuid(obj.id)
        self.start_instance(class_name, obj_id, out)
        self.string_node("IdentifiedObject.mRID", obj_id, out)
        self.string_node("IdentifiedObject.name", obj.name, out)
        self.ref_node("Equipment.EquipmentContainer", self.fdrID, out)  # Note: fdr_id should be defined somewhere in your code
        self.ref_node("PowerSystemResource.GeoLocation", self.map_locations.get(obj_id), out)
        self.bool_node("Switch.normalOpen", obj.open, out)
        self.phases_enum(obj.phases, out)

    # def start_switch(self, voltage_id, out):
    #     results = self.query_handler.query(voltage_id, "Start Switch")
    #
    #     for soln in results:
    #         voltage_id = self.shorten_uuid(soln.get("?voltage_id").toString())
    #         name = soln.get("?name").toString()
    #         description = soln.get("?description").toString()
    #
    #         self.start_instance("StartSwitch", voltage_id, out)
    #         self.string_node("IdentifiedObject.mRID", voltage_id, out)
    #         self.string_node("IdentifiedObject.name", name, out)
    #         self.string_node("IdentifiedObject.description", description, out)
    #
    #         self.end_instance("StartSwitch", out)
    #
    #     results.close()

    def psr_type(self, id, name, out):
        self.start_instance("PSRType", id, out)
        self.string_node("IdentifiedObject.name", name, out)
        self.end_instance("PSRType", out)

    def write_cim_file(self, mdl, q_h, out):
        self.query_handler = q_h

        out.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
        out.write("<!-- un-comment this line to enable validation\n")
        out.write("-->\n")
        out.write("<rdf:RDF xmlns:cim=\"" + self.xnsCIM + "\" xmlns:rdf=\"" + self.xnsRDF + "\">\n")
        out.write("<!--\n")
        out.write("-->\n")

        self.start_free_instance("IEC61970CIMVersion", out)
        self.string_node("IEC61970CIMVersion.version", "IEC61970CIM14v12", out)
        self.string_node("IEC61970CIMVersion.date", "2009-11-27T00:00:00", out)
        self.end_instance("IEC61970CIMVersion", out)

        for fdr_pair in mdl.map_feeders.items():
            fdr = fdr_pair[1]
            fdr_id = self.shorten_uuid(fdr.feeder_id)
            rgn_id = self.shorten_uuid(fdr.region_id)
            subrgn_id = self.shorten_uuid(fdr.subregion_id)
            sub_id = self.shorten_uuid(fdr.substation_id)

            self.start_instance("GeographicalRegion", rgn_id, out)
            self.string_node("IdentifiedObject.mRID", rgn_id, out)
            self.string_node("IdentifiedObject.name", fdr.region_name, out)
            self.string_node("IdentifiedObject.description", "Top-level region", out)
            self.end_instance("GeographicalRegion", out)

            self.start_instance("SubGeographicalRegion", subrgn_id, out)
            self.string_node("IdentifiedObject.mRID", subrgn_id, out)
            self.string_node("IdentifiedObject.name", fdr.subregion_name, out)
            self.string_node("IdentifiedObject.description", "Lower-level region", out)
            self.ref_node("SubGeographicalRegion.Region", rgn_id, out)
            self.end_instance("SubGeographicalRegion", out)

            self.start_instance("Substation", sub_id, out)
            self.string_node("IdentifiedObject.mRID", sub_id, out)
            self.string_node("IdentifiedObject.name", fdr.substation_name, out)
            self.end_instance("Substation", out)

            self.start_instance("Line", fdr_id, out)
            self.string_node("IdentifiedObject.mRID", fdr_id, out)
            self.string_node("IdentifiedObject.name", fdr.feeder_name, out)
            self.string_node("IdentifiedObject.description", "Feeder equipment container", out)
            self.ref_node("Line.Region", subrgn_id, out)
            self.end_instance("Line", out)

            self.load_connectivity_nodes(out)
            self.load_terminals(out)
            self.load_locations(out)  # we need a lookup mapper of these before writing out ConductingEquipment
            self.load_position_points(out)

            for obj_pair in mdl.map_substations.items():
                obj = obj_pair[1]
                obj_id = self.shorten_uuid(obj.id)
                self.start_instance("EnergySource", obj_id, out)
                self.string_node("IdentifiedObject.mRID", obj_id, out)
                self.string_node("IdentifiedObject.name", obj.name, out)
                self.ref_node("Equipment.EquipmentContainer", fdr_id, out)
                self.ref_node("PowerSystemResource.GeoLocation", self.map_locations.get(obj_id), out)
                self.double_node("EnergySource.nominalVoltage", obj.nomv, out)
                self.double_node("EnergySource.voltageMagnitude", obj.vmag, out)
                self.double_node("EnergySource.voltageAngle", obj.vang, out)
                self.double_node("EnergySource.r", obj.r1, out)
                self.double_node("EnergySource.x", obj.x1, out)
                self.double_node("EnergySource.r0", obj.r0, out)
                self.double_node("EnergySource.x0", obj.x0, out)
                self.end_instance("EnergySource", out)

            # For Survalent, we are writing line codes and spacings as named PSRTypes,
            #   i.e., not with the actual data
            # If we later write the line code and spacing data, then we should NOT write
            #   PSRTypes that re-use the same UUIDs
            for obj_pair in mdl.map_spacings.items():
                obj = obj_pair[1]
                self.psr_type(self.shorten_uuid(obj.id), "Spacing:" + obj.name, out)

            for obj_pair in mdl.map_phase_matrices.items():
                obj = obj_pair[1]
                self.psr_type(self.shorten_uuid(obj.id), "PhaseZ:" + obj.name, out)

            for obj_pair in mdl.map_sequence_matrices.items():
                obj = obj_pair[1]
                self.psr_type(self.shorten_uuid(obj.id), "SequenceZ:" + obj.name, out)

            inst_z_id = self.shorten_uuid("_" + uuid.uuid4().hex.upper())
            self.psr_type(inst_z_id, "InstanceZ", out)

            for obj_pair in mdl.map_lines_spacing_z.items():
                obj = obj_pair[1]
                self.distribution_line_segment(obj, self.shorten_uuid(obj.spcid), out)

            for obj_pair in mdl.map_lines_instance_z.items():
                obj = obj_pair[1]
                self.distribution_line_segment(obj, inst_z_id, out)

            for obj_pair in mdl.map_lines_code_z.items():
                obj = obj_pair[1]
                self.distribution_line_segment(obj, self.shorten_uuid(obj.codeid), out)

            for obj_pair in mdl.map_fuses.items():
                obj = obj_pair[1]
                self.start_switch("Fuse", obj, out)
                self.double_node("Fuse.ratingCurrent", obj.rated, out)
                self.end_instance("Fuse", out)

            for obj_pair in mdl.map_breakers.items():
                obj = obj_pair[1]
                self.start_switch("Breaker", obj, out)
                self.end_instance("Breaker", out)

            for obj_pair in mdl.map_load_break_switches.items():
                obj = obj_pair[1]
                self.start_switch("LoadBreakSwitch", obj, out)
                self.double_node("LoadBreakSwitch.ratedCurrent", obj.rated, out)
                self.end_instance("LoadBreakSwitch", out)

            for obj_pair in mdl.map_loads.items():
                obj = obj_pair[1]
                obj_id = self.shorten_uuid(obj.id)
                self.start_instance("EnergyConsumer", obj_id, out)
                self.string_node("IdentifiedObject.mRID", obj_id, out)
                self.string_node("IdentifiedObject.name", obj.name, out)
                self.ref_node("Equipment.EquipmentContainer", fdr_id, out)
                self.ref_node("PowerSystemResource.GeoLocation", CIMImporter.map_locations.get(obj_id), out)
                phs = obj.phases.replace(":", "")
                self.phases_enum(phs, out)
                self.double_node("EnergyConsumer.pfixed", 1000.0 * obj.precisions, out)
                self.double_node("EnergyConsumer.qfixed", 1000.0 * obj.q, out)
                self.integer_node("EnergyConsumer.customerCount", obj.cnt, out)
                self.end_instance("EnergyConsumer", out)

            self.load_transformer_info(out)

            map_banks = {}
            sec_xfid = self.shorten_uuid("_" + uuid.uuid4().hex.upper())
            self.psr_type(sec_xfid, "SplitSecondary", out)
            misc_xfid = self.shorten_uuid("_" + uuid.uuid4().hex.upper())
            self.psr_type(misc_xfid, "OtherTransformer", out)
            for obj_pair in mdl.map_banks.items():
                obj = obj_pair[1]
                obj_id = self.shorten_uuid(obj.pid)
                self.start_instance("TransformerBank", obj_id, out)
                self.string_node("IdentifiedObject.mRID", obj_id, out)
                self.string_node("IdentifiedObject.name", obj.pname, out)
                self.ref_node("Equipment.EquipmentContainer", fdr_id, out)
                self.ref_node("PowerSystemResource.GeoLocation", self.map_locations.get(obj_id), out)
                self.string_node("TransformerBank.vectorGroup", obj.vgrp, out)
                if "Iii" in obj.vgrp:
                    self.ref_node("PowerSystemResource.PSRType", sec_xfid, out)
                else:
                    self.ref_node("PowerSystemResource.PSRType", misc_xfid, out)
                self.end_instance("TransformerBank", out)
                map_banks[obj.pname] = obj_id

            for obj_pair in mdl.map_tanks.items():
                obj = obj_pair[1]
                obj_id = self.shorten_uuid(obj.id)
                inf_id = self.shorten_uuid(obj.infoid)
                self.start_instance("DistributionTransformer", obj_id, out)
                self.string_node("IdentifiedObject.mRID", obj_id, out)
                self.string_node("IdentifiedObject.name", obj.tname, out)
                self.ref_node("Equipment.EquipmentContainer", fdr_id, out)
                self.ref_node("PowerSystemResource.GeoLocation", self.map_locations.get(obj_id), out)
                self.ref_node("DistributionTransformer.TransformerBank", map_banks.get(obj.pname), out)
                self.ref_node("DistributionTransformer.TransformerInfo", inf_id, out)
                self.end_instance("DistributionTransformer", out)
                for i in range(obj.size):
                    e_id = self.shorten_uuid(obj.eid[i])
                    self.start_instance("DistributionTransformerWinding", e_id, out)
                    self.string_node("IdentifiedObject.mRID", e_id, out)
                    self.string_node("IdentifiedObject.name", obj.ename[i], out)
                    self.ref_node("Equipment.EquipmentContainer", fdr_id, out)
                    self.ref_node("DistributionTransformerWinding.WindingInfo", self.map_windings.get(inf_id)[i], out)
                    self.phases_enum(obj.phs[i], out)
                    self.bool_node("DistributionTransformerWinding.grounded", obj.grounded[i], out)
                    self.double_node("DistributionTransformerWinding.rground", obj.rg[i], out)
                    self.double_node("DistributionTransformerWinding.xground", obj.xg[i], out)
                    self.ref_node("DistributionTransformerWinding.DistributionTransformer", obj_id, out)
                    self.ref_node("PowerSystemResource.GeoLocation", self.map_locations.get(obj_id), out)
                    self.end_instance("DistributionTransformerWinding", out)

            for obj_pair in mdl.map_code_ratings.items():
                obj = obj_pair[1]
                obj_id = self.shorten_uuid(obj.id)
                for i in range(obj.size):
                    e_id = self.shorten_uuid(obj.eid[i])
                    self.start_instance("WindingInfo", e_id, out)
                    self.string_node("IdentifiedObject.mRID", e_id, out)
                    self.string_node("IdentifiedObject.name", obj.ename[i], out)
                    self.integer_node("WindingInfo.sequenceNumber", obj.wdg[i], out)
                    self.winding_connection_enum(obj.conn[i], out)
                    self.integer_node("WindingInfo.phaseAngle", obj.ang[i], out)
                    self.double_node("WindingInfo.ratedS", obj.ratedS[i], out)
                    self.double_node("WindingInfo.ratedU", obj.ratedU[i], out)
                    self.double_node("WindingInfo.r", obj.r[i], out)
                    self.ref_node("WindingInfo.TransformerInfo", obj_id, out)
                    self.end_instance("WindingInfo", out)

            for obj_pair in mdl.map_xfmr_windings.items():
                obj = obj_pair[1]
                obj_id = self.shorten_uuid(obj.id)
                self.start_instance("PowerTransformer", obj_id, out)
                self.string_node("IdentifiedObject.mRID", obj_id, out)
                self.string_node("IdentifiedObject.name", obj.name, out)
                self.ref_node("Equipment.EquipmentContainer", fdr_id, out)
                self.ref_node("PowerSystemResource.GeoLocation", self.map_locations.get(obj_id), out)
                self.end_instance("PowerTransformer", out)
                for i in range(obj.size):
                    e_id = self.shorten_uuid(obj.eid[i])
                    self.start_instance("TransformerWinding", e_id, out)
                    self.string_node("IdentifiedObject.mRID", e_id, out)
                    self.string_node("IdentifiedObject.name", obj.ename[i], out)
                    self.ref_node("Equipment.EquipmentContainer", fdr_id, out)
                    self.double_node("TransformerWinding.ratedS", obj.ratedS[i], out)
                    self.double_node("TransformerWinding.ratedU", obj.ratedU[i], out)
                    self.xf_winding_connection_enum(obj.conn[i], out)
                    self.xf_winding_type_enum(obj.wdg[i], out)
                    if obj.wdg[i] == 1:
                        mesh = mdl.map_xfmr_meshes.get(obj.name)
                        self.double_node("TransformerWinding.r", mesh.r[0], out)
                        self.double_node("TransformerWinding.x", mesh.x[0], out)
                    self.bool_node("TransformerWinding.grounded", obj.grounded[i], out)
                    self.double_node("TransformerWinding.rground", obj.rg[i], out)
                    self.double_node("TransformerWinding.xground", obj.xg[i], out)
                    self.ref_node("TransformerWinding.PowerTransformer", obj_id, out)
                    self.ref_node("PowerSystemResource.GeoLocation", self.map_locations.get(obj_id), out)
                    self.end_instance("TransformerWinding", out)

        self.map_locations.clear()
        self.set_locations.clear()
        self.map_windings.clear()

        out.write("</rdf:RDF>\n")
        out.close()

    # def load_transformers(self, out):
    #     results = self.query_handler.query(self.szXFMER, "xfmer")
    #     for soln in results:
    #         name = DistComponent.safe_name(soln.get("?name").toString())
    #         voltage_id = self.shorten_uuid(soln.get("?voltage_id").toString())
    #         self.start_instance("PowerTransformer", voltage_id, out)
    #         self.string_node("IdentifiedObject.mRID", voltage_id, out)
    #         self.string_node("IdentifiedObject.name", name, out)
    #         self.end_instance("PowerTransformer", out)
    #     results.close()

    # def load_ders(self, out):
    #     results = self.query_handler.query(self.szDER, "DER")
    #     for soln in results:
    #         name = DistComponent.safe_name(soln.get("?name").toString())
    #         voltage_id = self.shorten_uuid(soln.get("?voltage_id").toString())
    #         precisions = soln.get("?precisions").toString()
    #         q = soln.get("?q").toString()
    #         self.start_instance("DistributedEnergyResource", voltage_id, out)
    #         self.string_node("IdentifiedObject.mRID", voltage_id, out)
    #         self.string_node("IdentifiedObject.name", name, out)
    #         self.double_node("DistributedEnergyResource.precisions", float(precisions), out)
    #         self.double_node("DistributedEnergyResource.q", float(q), out)
    #         self.end_instance("DistributedEnergyResource", out)
    #     results.close()

    # def load_solar_inverters(self, out):
    #     results = self.query_handler.query(self.szINV, "INV")
    #     for soln in results:
    #         name = DistComponent.safe_name(soln.get("?name").toString())
    #         voltage_id = self.shorten_uuid(soln.get("?voltage_id").toString())
    #         precisions = soln.get("?precisions").toString()
    #         q = soln.get("?q").toString()
    #         self.start_instance("SolarInverter", voltage_id, out)
    #         self.string_node("IdentifiedObject.mRID", voltage_id, out)
    #         self.string_node("IdentifiedObject.name", name, out)
    #         self.double_node("PowerElectronicsConnection.precisions", float(precisions), out)
    #         self.double_node("PowerElectronicsConnection.q", float(q), out)
    #         self.end_instance("SolarInverter", out)
    #     results.close()

    # def load_battery_inverters(self, out):
    #     results = self.query_handler.query(self.szBINV, "BINV")
    #     for soln in results:
    #         name = DistComponent.safe_name(soln.get("?name").toString())
    #         voltage_id = self.shorten_uuid(soln.get("?voltage_id").toString())
    #         precisions = soln.get("?precisions").toString()
    #         q = soln.get("?q").toString()
    #         self.start_instance("BatteryInverter", voltage_id, out)
    #         self.string_node("IdentifiedObject.mRID", voltage_id, out)
    #         self.string_node("IdentifiedObject.name", name, out)
    #         self.double_node("PowerElectronicsConnection.precisions", float(precisions), out)
    #         self.double_node("PowerElectronicsConnection.q", float(q), out)
    #         self.end_instance("BatteryInverter", out)
    #     results.close()

    # def load_synchronous_machines(self, out):
    #     results = self.query_handler.query(self.szGEN, "GEN")
    #     for soln in results:
    #         name = DistComponent.safe_name(soln.get("?name").toString())
    #         voltage_id = self.shorten_uuid(soln.get("?voltage_id").toString())
    #         precisions = soln.get("?precisions").toString()
    #         q = soln.get("?q").toString()
    #         self.start_instance("SynchronousMachine", voltage_id, out)
    #         self.string_node("IdentifiedObject.mRID", voltage_id, out)
    #         self.string_node("IdentifiedObject.name", name, out)
    #         self.double_node("RotatingMachine.precisions", float(precisions), out)
    #         self.double_node("RotatingMachine.q", float(q), out)
    #         self.end_instance("SynchronousMachine", out)
    #     results.close()

    # def load_voltage_levels(self, out):
    #     results = self.query_handler.query(self.szVL, "VL")
    #     for soln in results:
    #         name = DistComponent.safe_name(soln.get("?name").toString())
    #         voltage_id = self.shorten_uuid(soln.get("?voltage_id").toString())
    #         self.start_instance("VoltageLevel", voltage_id, out)
    #         self.string_node("IdentifiedObject.mRID", voltage_id, out)
    #         self.string_node("IdentifiedObject.name", name, out)
    #         self.end_instance("VoltageLevel", out)
    #     results.close()

    # def load_connectivity_assets(self, out):
    #     self.load_voltage_levels(out)
    #     self.load_transformers(out)
    #     self.load_energy_consumers(out)
    #     self.load_ders(out)
    #     self.load_solar_inverters(out)
    #     self.load_battery_inverters(out)
    #     self.load_synchronous_machines(out)

    # def load_xf_info_windings(self, out):
    #     results = self.query_handler.query(self.szXFWIND, "xf winding info")
    #     for soln in results:
    #         tid = self.shorten_uuid(soln.get("?tid").toString())
    #         wnd = self.shorten_uuid(soln.get("?wnd").toString())
    #         pht = soln.get("?pht").toString()
    #         self.start_instance("TransformerWinding", wnd, out)
    #         self.string_node("IdentifiedObject.mRID", wnd, out)
    #         self.integer_node("TransformerWinding.phaseTapChangerCount", 0, out)
    #         self.xf_winding_type_enum(int(pht), out)
    #         self.xf_winding_connection_enum("Y", out)
    #         self.ref_node("TransformerWinding.PowerTransformer", tid, out)
    #         self.end_instance("TransformerWinding", out)
    #     results.close()

    # def load_xf_windings(self, out):
    #     results = self.query
