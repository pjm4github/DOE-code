# package gov.pnnl.gridappsd.cimhub;
# // ----------------------------------------------------------
# // Copyright (c) 2017-2020, Battelle Memorial Institute
# // All rights reserved.
# // ----------------------------------------------------------
#
# import java.io.*;
# import javax.xml.parsers.DocumentBuilder;
# import javax.xml.parsers.DocumentBuilderFactory;
# import org.w3c.dom.*;
# import java.util.HashMap;
#
# import gov.pnnl.gridappsd.cimhub.CIMImporter;
# import gov.pnnl.gridappsd.cimhub.components.DistComponent;
# import gov.pnnl.gridappsd.cimhub.components.DistBreaker;
# import gov.pnnl.gridappsd.cimhub.components.DistDisconnector;
# import gov.pnnl.gridappsd.cimhub.components.DistFuse;
# import gov.pnnl.gridappsd.cimhub.components.DistGroundDisconnector;
# import gov.pnnl.gridappsd.cimhub.components.DistJumper;
# import gov.pnnl.gridappsd.cimhub.components.DistLoadBreakSwitch;
# import gov.pnnl.gridappsd.cimhub.components.DistRecloser;
# import gov.pnnl.gridappsd.cimhub.components.DistSectionaliser;
#
# public class CIMQuerySetter extends Object {
#
#     HashMap<String,String> mapQueries = new HashMap<>();
#     HashMap<String,String> mapSwitchClasses = new HashMap<>();
#
#     public CIMQuerySetter () {
#
#         mapSwitchClasses.put ("DistBreaker", DistBreaker.sz_cim_class);
#         mapSwitchClasses.put ("DistDisconnector", DistDisconnector.sz_cim_class);
#         mapSwitchClasses.put ("DistFuse", DistFuse.sz_cim_class);
#         mapSwitchClasses.put ("DistGroundDisconnector", DistGroundDisconnector.sz_cim_class);
#         mapSwitchClasses.put ("DistJumper", DistJumper.sz_cim_class);
#         mapSwitchClasses.put ("DistLoadBreakSwitch", DistLoadBreakSwitch.sz_cim_class);
#         mapSwitchClasses.put ("DistRecloser", DistRecloser.sz_cim_class);
#         mapSwitchClasses.put ("DistSectionaliser", DistSectionaliser.sz_cim_class);
#
#         mapQueries.put ("DistBaseVoltage",
#             "SELECT DISTINCT ?vnom WHERE {"+
#             " ?fdr c:IdentifiedObject.mRID ?fdrid."+
#             " ?status c:Equipment.EquipmentContainer ?fdr."+
#             " {?status c:ConductingEquipment.BaseVoltage ?lev.}"+
#             "  UNION "+
#             " { ?end c:PowerTransformerEnd.PowerTransformer|c:TransformerTankEnd.TransformerTank ?status."+
#             "     ?end c:TransformerEnd.BaseVoltage ?lev.}"+
#             " ?lev r:type c:BaseVoltage."+
#             " ?lev c:BaseVoltage.nominalVoltage ?vnom."+
#             "} ORDER BY ?vnom");
#
#         mapQueries.put ("DistCapacitor",
#            "SELECT ?name ?basev ?nomu ?bsection ?bus ?conn ?grnd ?phs"+
#              " ?ctrlenabled ?discrete ?mode ?deadband ?setpoint ?delay ?monclass ?moneq ?monbus ?monphs ?id ?fdrid WHERE {"+
#              " ?status c:Equipment.EquipmentContainer ?fdr."+
#              " ?fdr c:IdentifiedObject.mRID ?fdrid."+
#              " ?status r:type c:LinearShuntCompensator."+
#              " ?status c:IdentifiedObject.name ?name."+
#              " ?status c:ConductingEquipment.BaseVoltage ?bv."+
#              " ?bv c:BaseVoltage.nominalVoltage ?basev."+
#              " ?status c:ShuntCompensator.nomU ?nomu."+
#              " ?status c:LinearShuntCompensator.bPerSection ?bsection."+
#              " ?status c:ShuntCompensator.phaseConnection ?connraw."+
#              "     bind(strafter(str(?connraw),\"PhaseShuntConnectionKind.\") as ?conn)"+
#              " ?status c:ShuntCompensator.grounded ?grnd."+
#              " OPTIONAL {?scp c:ShuntCompensatorPhase.ShuntCompensator ?status."+
#              "     ?scp c:ShuntCompensatorPhase.phase ?phsraw."+
#              "     bind(strafter(str(?phsraw),\"SinglePhaseKind.\") as ?phs) }"+
#              " OPTIONAL {?ctl c:RegulatingControl.RegulatingCondEq ?status."+
#              "     ?ctl c:RegulatingControl.discrete ?discrete."+
#              "     ?ctl c:RegulatingControl.enabled ?ctrlenabled."+
#              "     ?ctl c:RegulatingControl.mode ?moderaw."+
#              "         bind(strafter(str(?moderaw),\"RegulatingControlModeKind.\") as ?mode)"+
#              "     ?ctl c:RegulatingControl.monitoredPhase ?monraw."+
#              "         bind(strafter(str(?monraw),\"PhaseCode.\") as ?monphs)"+
#              "     ?ctl c:RegulatingControl.targetDeadband ?deadband."+
#              "     ?ctl c:RegulatingControl.targetValue ?setpoint."+
#              "  ?status c:ShuntCompensator.aVRDelay ?delay."+
#              "     ?ctl c:RegulatingControl.Terminal ?trm."+
#              "     ?trm c:Terminal.ConductingEquipment ?eq."+
#              "     ?eq a ?classraw."+
#              "         bind(strafter(str(?classraw),\"CIM100#\") as ?monclass)"+
#              "     ?eq c:IdentifiedObject.name ?moneq."+
#              "     ?trm c:Terminal.ConnectivityNode ?moncn."+
#              "     ?moncn c:IdentifiedObject.name ?monbus."+
#              "  }" +
#              " bind(strafter(str(?status),\"#\") as ?id)."+
#              " ?t c:Terminal.ConductingEquipment ?status."+
#              " ?t c:Terminal.ConnectivityNode ?cn."+
#              " ?cn c:IdentifiedObject.name ?bus" +
#              "}");
#
#         mapQueries.put ("DistConcentricNeutralCable",
#             "SELECT DISTINCT ?name ?rad ?corerad ?gmr ?rdc ?r25 ?r50 ?r75 ?amps ?ins ?insmat ?id"+
#             " ?insthick ?diacore ?diains ?diascreen ?diajacket ?sheathneutral"+
#             " ?strand_cnt ?strand_rad ?strand_gmr ?strand_rdc WHERE {"+
#             " ?eq r:type c:ACLineSegment."+
#             " ?eq c:Equipment.EquipmentContainer ?fdr."+
#             " ?fdr c:IdentifiedObject.mRID ?fdrid."+
#             " ?acp c:ACLineSegmentPhase.ACLineSegment ?eq."+
#             " ?acp c:ACLineSegmentPhase.WireInfo ?w."+
#             " ?w r:type c:ConcentricNeutralCableInfo."+
#             " ?w c:IdentifiedObject.name ?name."+
#             " bind(strafter(str(?w),\"#\") as ?id)."+
#             " ?w c:WireInfo.radius ?rad."+
#             " ?w c:WireInfo.gmr ?gmr."+
#             " OPTIONAL {?w c:WireInfo.rDC20 ?rdc.}"+
#             " OPTIONAL {?w c:WireInfo.rAC25 ?r25.}"+
#             " OPTIONAL {?w c:WireInfo.rAC50 ?r50.}"+
#             " OPTIONAL {?w c:WireInfo.rAC75 ?r75.}"+
#             " OPTIONAL {?w c:WireInfo.coreRadius ?corerad.}"+
#             " OPTIONAL {?w c:WireInfo.ratedCurrent ?amps.}"+
#             " OPTIONAL {?w c:WireInfo.insulationMaterial ?insraw."+
#             "           bind(strafter(str(?insraw),\"WireInsulationKind.\") as ?insmat)}"+
#             " OPTIONAL {?w c:WireInfo.insulated ?ins.}"+
#             " OPTIONAL {?w c:WireInfo.insulationThickness ?insthick.}"+
#             " OPTIONAL {?w c:CableInfo.diameterOverCore ?diacore.}"+
#             " OPTIONAL {?w c:CableInfo.diameterOverJacket ?diajacket.}"+
#             " OPTIONAL {?w c:CableInfo.diameterOverInsulation ?diains.}"+
#             " OPTIONAL {?w c:CableInfo.diameterOverScreen ?diascreen.}"+
#             " OPTIONAL {?w c:CableInfo.sheathAsNeutral ?sheathneutral.}"+
#             " OPTIONAL {?w c:ConcentricNeutralCableInfo.diameterOverNeutral ?dianeut.}"+
#             " OPTIONAL {?w c:ConcentricNeutralCableInfo.neutralStrandCount ?strand_cnt.}"+
#             " OPTIONAL {?w c:ConcentricNeutralCableInfo.neutralStrandGmr ?strand_gmr.}"+
#             " OPTIONAL {?w c:ConcentricNeutralCableInfo.neutralStrandRadius ?strand_rad.}"+
#             " OPTIONAL {?w c:ConcentricNeutralCableInfo.neutralStrandRDC20 ?strand_rdc.}"+
#             "} ORDER BY ?name");
#
#         mapQueries.put ("DistCoordinates",
#             "SELECT ?class ?name ?seq ?x ?y WHERE {"+
#             " ?eq c:Equipment.EquipmentContainer ?fdr."+
#             " ?fdr c:IdentifiedObject.mRID ?fdrid."+
#             " ?eq c:PowerSystemResource.Location ?loc."+
#             " { ?eq c:IdentifiedObject.name ?name."+
#             "   ?eq a ?classraw."+
#             "   bind(strafter(str(?classraw),\"CIM100#\") as ?class)}"+
#             "  UNION"+
#             " { ?eq c:PowerElectronicsConnection.PowerElectronicsUnit ?unit."+
#             "   ?unit c:IdentifiedObject.name ?name."+
#             "   ?unit a ?classraw."+
#             "   bind(strafter(str(?classraw),\"CIM100#\") as ?class)}"+
#             " ?pt c:PositionPoint.Location ?loc."+
#             " ?pt c:PositionPoint.xPosition ?x."+
#             " ?pt c:PositionPoint.yPosition ?y."+
#             " ?pt c:PositionPoint.sequenceNumber ?seq."+
#             " FILTER (!regex(?class, \"Phase\"))."+
#             " FILTER (!regex(?class, \"TapChanger\"))."+
#             " FILTER (!regex(?class, \"Tank\"))."+
#             " FILTER (!regex(?class, \"RegulatingControl\"))."+
#             "}"+
#             " ORDER BY ?class ?name ?seq ?x ?y");
#
#         mapQueries.put ("DistFeeder",
#              "SELECT ?feeder ?fid ?station ?sid ?subregion ?sgrid ?region ?rgnid WHERE {"+
#              "?status r:type c:Feeder."+
#              "?status c:IdentifiedObject.name ?feeder."+
#              "?status c:IdentifiedObject.mRID ?fid."+
#              "?status c:Feeder.NormalEnergizingSubstation ?sub."+
#              "?sub c:IdentifiedObject.name ?station."+
#              "?sub c:IdentifiedObject.mRID ?sid."+
#              "?sub c:Substation.Region ?sgr."+
#              "?sgr c:IdentifiedObject.name ?subregion."+
#              "?sgr c:IdentifiedObject.mRID ?sgrid."+
#              "?sgr c:SubGeographicalRegion.Region ?rgn."+
#              "?rgn c:IdentifiedObject.name ?region."+
#              "?rgn c:IdentifiedObject.mRID ?rgnid."+
#              "}"+
#              " ORDER by ?station ?feeder");
#
#         mapQueries.put ("DistHouse",
#             "SELECT ?name ?parent ?coolingSetpoint ?coolingSystem ?floorArea ?heatingSetpoint ?heatingSystem ?hvacPowerFactor ?numberOfStories ?thermalIntegrity ?id ?fdrid WHERE {" +
#                     "?h r:type c:House. " +
#                     "?h c:IdentifiedObject.name ?name. " +
#                     "?h c:IdentifiedObject.mRID ?id. " +
#                     "?h c:House.floorArea ?floorArea. " +
#                     "?h c:House.numberOfStories ?numberOfStories. " +
#                     "OPTIONAL{?h c:House.coolingSetpoint ?coolingSetpoint.} " +
#                     "OPTIONAL{?h c:House.heatingSetpoint ?heatingSetpoint.} " +
#                     "OPTIONAL{?h c:House.hvacPowerFactor ?hvacPowerFactor.} " +
#                     "?h c:House.coolingSystem ?coolingSystemRaw. " +
#                         "bind(strafter(str(?coolingSystemRaw),\"HouseCooling.\") as ?coolingSystem) " +
#                     "?h c:House.heatingSystem ?heatingSystemRaw. " +
#                         "bind(strafter(str(?heatingSystemRaw),\"HouseHeating.\") as ?heatingSystem) " +
#                     "?h c:House.thermalIntegrity ?thermalIntegrityRaw " +
#                         "bind(strafter(str(?thermalIntegrityRaw),\"HouseThermalIntegrity.\") as ?thermalIntegrity) " +
#                     "?h c:House.EnergyConsumer ?econ. " +
#                     "?econ c:IdentifiedObject.name ?parent. " +
#                     "?fdr c:IdentifiedObject.mRID ?fdrid. " +
#                     "?econ c:Equipment.EquipmentContainer ?fdr. " +
#             "} ORDER BY ?name");
#
#         mapQueries.put ("DistLinesCodeZ",
#             "SELECT ?name ?id ?basev ?bus1 ?bus2 ?len ?lname ?codeid ?fdrid ?seq ?phs WHERE {"+
#             " ?status r:type c:ACLineSegment."+
#             " ?status c:Equipment.EquipmentContainer ?fdr."+
#             " ?fdr c:IdentifiedObject.mRID ?fdrid."+
#             " ?status c:IdentifiedObject.name ?name."+
#             " ?status c:ConductingEquipment.BaseVoltage ?bv."+
#             " ?bv c:BaseVoltage.nominalVoltage ?basev."+
#             " ?status c:Conductor.length ?len."+
#             " ?status c:ACLineSegment.PerLengthImpedance ?lcode."+
#             " ?lcode c:IdentifiedObject.name ?lname."+
#             " bind(strafter(str(?lcode),\"#\") as ?codeid)."+
#             " ?t1 c:Terminal.ConductingEquipment ?status."+
#             " ?t1 c:Terminal.ConnectivityNode ?cn1."+
#             " ?t1 c:ACDCTerminal.sequenceNumber \"1\"."+
#             " ?cn1 c:IdentifiedObject.name ?bus1."+
#             " ?t2 c:Terminal.ConductingEquipment ?status."+
#             " ?t2 c:Terminal.ConnectivityNode ?cn2."+
#             " ?t2 c:ACDCTerminal.sequenceNumber \"2\"."+
#             " ?cn2 c:IdentifiedObject.name ?bus2."+
#             " bind(strafter(str(?status),\"#\") as ?id)."+
#             " OPTIONAL {?acp c:ACLineSegmentPhase.ACLineSegment ?status."+
#             " ?acp c:ACLineSegmentPhase.sequenceNumber ?seq."+
#             " ?acp c:ACLineSegmentPhase.phase ?phsraw."+
#             "   bind(strafter(str(?phsraw),\"SinglePhaseKind.\") as ?phs) }"+
#             "}"+
#             " ORDER BY ?name ?seq ?phs");
#
#         mapQueries.put ("DistLinesInstanceZ",
#             "SELECT ?name ?id ?basev ?bus1 ?bus2 ?len ?r ?x ?b ?r0 ?x0 ?b0 ?fdrid WHERE {"+
#             " ?status r:type c:ACLineSegment."+
#             " ?status c:Equipment.EquipmentContainer ?fdr."+
#             " ?fdr c:IdentifiedObject.mRID ?fdrid."+
#             " ?status c:IdentifiedObject.name ?name."+
#             " bind(strafter(str(?status),\"#\") as ?id)."+
#             " ?status c:ConductingEquipment.BaseVoltage ?bv."+
#             " ?bv c:BaseVoltage.nominalVoltage ?basev."+
#             " ?status c:Conductor.length ?len."+
#             " ?status c:ACLineSegment.r ?r."+
#             " ?status c:ACLineSegment.x ?x."+
#             " OPTIONAL {?status c:ACLineSegment.bch ?b.}"+
#             " OPTIONAL {?status c:ACLineSegment.r0 ?r0.}"+
#             " OPTIONAL {?status c:ACLineSegment.x0 ?x0.}"+
#             " OPTIONAL {?status c:ACLineSegment.b0ch ?b0.}"+
#             " ?t1 c:Terminal.ConductingEquipment ?status."+
#             " ?t1 c:Terminal.ConnectivityNode ?cn1."+
#             " ?t1 c:ACDCTerminal.sequenceNumber \"1\"."+
#             " ?cn1 c:IdentifiedObject.name ?bus1."+
#             " ?t2 c:Terminal.ConductingEquipment ?status."+
#             " ?t2 c:Terminal.ConnectivityNode ?cn2."+
#             " ?t2 c:ACDCTerminal.sequenceNumber \"2\"."+
#             " ?cn2 c:IdentifiedObject.name ?bus2"+
#             "}"+
#             " GROUP BY ?name ?id ?basev ?bus1 ?bus2 ?len ?r ?x ?b ?r0 ?x0 ?b0 ?fdrid"+
#             " ORDER BY ?name");
#
#         mapQueries.put ("DistLinesSpacingZ",
#             "SELECT ?name ?id ?basev ?bus1 ?bus2 ?fdrid ?len ?spacing ?spcid ?phs ?phname ?phclass"+
#             " WHERE {"+
#             " ?status r:type c:ACLineSegment."+
#             " ?status c:Equipment.EquipmentContainer ?fdr."+
#             " ?fdr c:IdentifiedObject.mRID ?fdrid."+
#             " ?status c:IdentifiedObject.name ?name."+
#             "   bind(strafter(str(?status),\"#\") as ?id)."+
#             " ?status c:ConductingEquipment.BaseVoltage ?bv."+
#             " ?bv c:BaseVoltage.nominalVoltage ?basev."+
#             " ?status c:Conductor.length ?len."+
#             " ?status c:ACLineSegment.WireSpacingInfo ?inf."+
#             "   bind(strafter(str(?inf),\"#\") as ?spcid)."+
#             " ?inf c:IdentifiedObject.name ?spacing."+
#             " ?t1 c:Terminal.ConductingEquipment ?status."+
#             " ?t1 c:Terminal.ConnectivityNode ?cn1."+
#             " ?t1 c:ACDCTerminal.sequenceNumber \"1\"."+
#             " ?cn1 c:IdentifiedObject.name ?bus1."+
#             " ?t2 c:Terminal.ConductingEquipment ?status."+
#             " ?t2 c:Terminal.ConnectivityNode ?cn2."+
#             " ?t2 c:ACDCTerminal.sequenceNumber \"2\"."+
#             " ?cn2 c:IdentifiedObject.name ?bus2."+
#             " ?acp c:ACLineSegmentPhase.ACLineSegment ?status."+
#             " ?acp c:ACLineSegmentPhase.phase ?phsraw."+
#             "   bind(strafter(str(?phsraw),\"SinglePhaseKind.\") as ?phs)."+
#             " ?acp c:ACLineSegmentPhase.WireInfo ?phinf."+
#             " ?phinf c:IdentifiedObject.name ?phname."+
#             " ?phinf a ?phclassraw."+
#             "   bind(strafter(str(?phclassraw),\"CIM100#\") as ?phclass)"+
#             " }"+
#             " ORDER BY ?id ?name ?phs");
#
#         mapQueries.put ("DistLineSpacing",
#             "SELECT DISTINCT ?name ?cable ?usage ?bundle_count ?bundle_sep ?id ?seq ?x ?y"+
#             " WHERE {"+
#             " ?eq r:type c:ACLineSegment."+
#             " ?eq c:Equipment.EquipmentContainer ?fdr."+
#             " ?fdr c:IdentifiedObject.mRID ?fdrid."+
#             " ?eq c:ACLineSegment.WireSpacingInfo ?w."+
#             " ?w c:IdentifiedObject.name ?name."+
#             "   bind(strafter(str(?w),\"#\") as ?id)."+
#             " ?pos c:WirePosition.WireSpacingInfo ?w."+
#             " ?pos c:WirePosition.xCoord ?x."+
#             " ?pos c:WirePosition.yCoord ?y."+
#             " ?pos c:WirePosition.sequenceNumber ?seq."+
#             " ?w c:WireSpacingInfo.isCable ?cable."+
#             " ?w c:WireSpacingInfo.phaseWireCount ?bundle_count."+
#             " ?w c:WireSpacingInfo.phaseWireSpacing ?bundle_sep."+
#             " ?w c:WireSpacingInfo.usage ?useraw."+
#             "   bind(strafter(str(?useraw),\"WireUsageKind.\") as ?usage)"+
#             "} ORDER BY ?name ?seq");
#
#         mapQueries.put ("DistLoad",
#             "SELECT ?name ?bus ?basev ?precisions ?q ?cnt ?conn ?pz ?qz ?pi ?qi ?pp ?qp ?pe ?qe ?id ?fdrid "+
#             "(group_concat(distinct ?phs;separator=\"\\dimensions\") as ?phases) "+
#             "WHERE {"+
#             " ?status r:type c:EnergyConsumer."+
#             " ?status c:Equipment.EquipmentContainer ?fdr."+
#             " ?fdr c:IdentifiedObject.mRID ?fdrid."+
#             " ?status c:IdentifiedObject.name ?name."+
#              " ?status c:ConductingEquipment.BaseVoltage ?bv."+
#              " ?bv c:BaseVoltage.nominalVoltage ?basev."+
#             " ?status c:EnergyConsumer.precisions ?precisions."+
#             " ?status c:EnergyConsumer.q ?q."+
#             " ?status c:EnergyConsumer.customerCount ?cnt."+
#             " ?status c:EnergyConsumer.phaseConnection ?connraw."+
#             "             bind(strafter(str(?connraw),\"PhaseShuntConnectionKind.\") as ?conn)"+
#             " ?status c:EnergyConsumer.LoadResponse ?lr."+
#             " ?lr c:LoadResponseCharacteristic.pConstantImpedance ?pz."+
#             " ?lr c:LoadResponseCharacteristic.qConstantImpedance ?qz."+
#             " ?lr c:LoadResponseCharacteristic.pConstantCurrent ?pi."+
#             " ?lr c:LoadResponseCharacteristic.qConstantCurrent ?qi."+
#             " ?lr c:LoadResponseCharacteristic.pConstantPower ?pp."+
#             " ?lr c:LoadResponseCharacteristic.qConstantPower ?qp."+
#             " ?lr c:LoadResponseCharacteristic.pVoltageExponent ?pe."+
#             " ?lr c:LoadResponseCharacteristic.qVoltageExponent ?qe."+
#             " OPTIONAL {?ecp c:EnergyConsumerPhase.EnergyConsumer ?status."+
#             " ?ecp c:EnergyConsumerPhase.phase ?phsraw."+
#             "             bind(strafter(str(?phsraw),\"SinglePhaseKind.\") as ?phs) }"+
#             " bind(strafter(str(?status),\"#\") as ?id)."+
#             " ?t c:Terminal.ConductingEquipment ?status."+
#             " ?t c:Terminal.ConnectivityNode ?cn."+
#             " ?cn c:IdentifiedObject.name ?bus"+
#             "} "+
#             "GROUP BY ?name ?bus ?basev ?precisions ?q ?cnt ?conn ?pz ?qz ?pi ?qi ?pp ?qp ?pe ?qe ?id ?fdrid "+
#             "ORDER BY ?name");
#
#         mapQueries.put ("DistMeasurement",
#             "SELECT ?class ?type ?name ?bus ?phases ?eqtype ?eqname ?eqid ?trmid ?id WHERE {"+
#             " ?eq c:Equipment.EquipmentContainer ?fdr."+
#             " ?fdr c:IdentifiedObject.mRID ?fdrid."+
#             " { ?status r:type c:Discrete. bind (\"Discrete\" as ?class)}"+
#             "   UNION"+
#             " { ?status r:type c:Analog. bind (\"Analog\" as ?class)}"+
#             "  ?status c:IdentifiedObject.name ?name ."+
#             "  ?status c:IdentifiedObject.mRID ?id ."+
#             "  ?status c:Measurement.PowerSystemResource ?eq ."+
#             "  ?status c:Measurement.Terminal ?trm ."+
#             "  ?status c:Measurement.measurementType ?type ."+
#             "  ?trm c:IdentifiedObject.mRID ?trmid."+
#             "  ?eq c:IdentifiedObject.mRID ?eqid."+
#             "  ?eq c:IdentifiedObject.name ?eqname."+
#             "  ?eq r:type ?typeraw."+
#             "   bind(strafter(str(?typeraw),\"#\") as ?eqtype)"+
#             "  ?trm c:Terminal.ConnectivityNode ?cn."+
#             "  ?cn c:IdentifiedObject.name ?bus."+
#             "  ?status c:Measurement.phases ?phsraw ."+
#             "    {bind(strafter(str(?phsraw),\"PhaseCode.\") as ?phases)}"+
#             " } ORDER BY ?class ?type ?name");
#
#         mapQueries.put ("DistOverheadWire",
#             "SELECT DISTINCT ?name ?rad ?corerad ?gmr ?rdc ?r25 ?r50 ?r75 ?amps ?ins ?insmat ?insthick ?id WHERE {"+
#             " ?eq r:type c:ACLineSegment."+
#             " ?eq c:Equipment.EquipmentContainer ?fdr."+
#             " ?fdr c:IdentifiedObject.mRID ?fdrid."+
#             " ?acp c:ACLineSegmentPhase.ACLineSegment ?eq."+
#             " ?acp c:ACLineSegmentPhase.WireInfo ?w."+
#             " ?w r:type c:OverheadWireInfo."+
#             " ?w c:IdentifiedObject.name ?name."+
#             "   bind(strafter(str(?w),\"#\") as ?id)."+
#             " ?w c:WireInfo.radius ?rad."+
#             " ?w c:WireInfo.gmr ?gmr."+
#             " OPTIONAL {?w c:WireInfo.rDC20 ?rdc.}"+
#             " OPTIONAL {?w c:WireInfo.rAC25 ?r25.}"+
#             " OPTIONAL {?w c:WireInfo.rAC50 ?r50.}"+
#             " OPTIONAL {?w c:WireInfo.rAC75 ?r75.}"+
#             " OPTIONAL {?w c:WireInfo.coreRadius ?corerad.}"+
#             " OPTIONAL {?w c:WireInfo.ratedCurrent ?amps.}"+
#             " OPTIONAL {?w c:WireInfo.insulationMaterial ?insraw."+
#             "       bind(strafter(str(?insraw),\"WireInsulationKind.\") as ?insmat)}"+
#             " OPTIONAL {?w c:WireInfo.insulated ?ins.}"+
#             " OPTIONAL {?w c:WireInfo.insulationThickness ?insthick.}"+
#             "} ORDER BY ?name");
#
#         mapQueries.put ("DistPhaseMatrix",
#             "SELECT DISTINCT ?name ?cnt ?row ?col ?r ?x ?b ?id WHERE {"+
#             " ?eq r:type c:ACLineSegment."+
#             " ?eq c:Equipment.EquipmentContainer ?fdr."+
#             " ?fdr c:IdentifiedObject.mRID ?fdrid."+
#             " ?eq c:ACLineSegment.PerLengthImpedance ?status."+
#             " ?status r:type c:PerLengthPhaseImpedance."+
#             " ?status c:IdentifiedObject.name ?name."+
#             " ?status c:PerLengthPhaseImpedance.conductorCount ?cnt."+
#             " bind(strafter(str(?status),\"#\") as ?id)."+
#             " ?elm c:PhaseImpedanceData.PhaseImpedance ?status."+
#             " ?elm c:PhaseImpedanceData.row ?row."+
#             " ?elm c:PhaseImpedanceData.column ?col."+
#             " ?elm c:PhaseImpedanceData.r ?r."+
#             " ?elm c:PhaseImpedanceData.x ?x."+
#             " ?elm c:PhaseImpedanceData.b ?b"+
#             "} ORDER BY ?name ?row ?col");
#
#         mapQueries.put ("DistPowerXfmrCore",
#             "SELECT ?pname ?enum ?b ?g WHERE {"+
#             " ?fdr c:IdentifiedObject.mRID ?fdrid."+
#             " ?precisions r:type c:PowerTransformer."+
#             " ?precisions c:Equipment.EquipmentContainer ?fdr."+
#             " ?precisions c:IdentifiedObject.name ?pname."+
#             " ?end c:PowerTransformerEnd.PowerTransformer ?precisions."+
#             " ?adm c:TransformerCoreAdmittance.TransformerEnd ?end."+
#             " ?end c:TransformerEnd.endNumber ?enum."+
#             " ?adm c:TransformerCoreAdmittance.b ?b."+
#             " ?adm c:TransformerCoreAdmittance.g ?g."+
#             "} ORDER BY ?pname");
#
#         mapQueries.put ("DistPowerXfmrMesh",
#             "SELECT ?pname ?fnum ?tnum ?r ?x WHERE {"+
#             " ?fdr c:IdentifiedObject.mRID ?fdrid."+
#             " ?precisions r:type c:PowerTransformer."+
#             " ?precisions c:Equipment.EquipmentContainer ?fdr."+
#             " ?precisions c:IdentifiedObject.name ?pname."+
#             " ?from c:PowerTransformerEnd.PowerTransformer ?precisions."+
#             " ?imp c:TransformerMeshImpedance.FromTransformerEnd ?from."+
#             " ?imp c:TransformerMeshImpedance.ToTransformerEnd ?to."+
#             " ?imp c:TransformerMeshImpedance.r ?r."+
#             " ?imp c:TransformerMeshImpedance.x ?x."+
#             " ?from c:TransformerEnd.endNumber ?fnum."+
#             " ?to c:TransformerEnd.endNumber ?tnum."+
#             "} ORDER BY ?pname ?fnum ?tnum");
#
#         mapQueries.put ("DistPowerXfmrWinding",
#             "SELECT ?pname ?vgrp ?enum ?bus ?basev ?conn ?ratedS ?ratedU ?r ?ang ?grounded ?rground ?xground ?id ?fdrid ?ename ?eid WHERE {"+
#             " ?precisions r:type c:PowerTransformer."+
#             " ?precisions c:Equipment.EquipmentContainer ?fdr."+
#             " ?fdr c:IdentifiedObject.mRID ?fdrid."+
#             " ?precisions c:IdentifiedObject.name ?pname."+
#             " ?precisions c:PowerTransformer.vectorGroup ?vgrp."+
#             " bind(strafter(str(?precisions),\"#\") as ?id)."+
#             " ?end c:PowerTransformerEnd.PowerTransformer ?precisions."+
#             " ?end c:TransformerEnd.endNumber ?enum."+
#             " ?end c:PowerTransformerEnd.ratedS ?ratedS."+
#             " ?end c:PowerTransformerEnd.ratedU ?ratedU."+
#             " ?end c:PowerTransformerEnd.r ?r."+
#             " ?end c:PowerTransformerEnd.phaseAngleClock ?ang."+
#             " ?end c:IdentifiedObject.name ?ename."+
#             " ?end c:IdentifiedObject.mRID ?eid."+
#             " ?end c:PowerTransformerEnd.connectionKind ?connraw."+
#             "  bind(strafter(str(?connraw),\"WindingConnection.\") as ?conn)"+
#             " ?end c:TransformerEnd.grounded ?grounded."+
#             " OPTIONAL {?end c:TransformerEnd.rground ?rground.}"+
#             " OPTIONAL {?end c:TransformerEnd.xground ?xground.}"+
#             " ?end c:TransformerEnd.Terminal ?trm."+
#             " ?trm c:Terminal.ConnectivityNode ?cn. "+
#             " ?cn c:IdentifiedObject.name ?bus."+
#             " ?end c:TransformerEnd.BaseVoltage ?bv."+
#             " ?bv c:BaseVoltage.nominalVoltage ?basev"+
#             "}"+
#             " ORDER BY ?pname ?enum");
#
#         mapQueries.put ("DistRegulatorPrefix",
#             "SELECT ?rname ?pname ?tname ?wnum ?phs ?incr ?mode ?enabled ?highStep ?lowStep ?neutralStep"+
#             " ?normalStep ?neutralU ?step ?initDelay ?subDelay ?ltc ?vlim"+
#             " ?vset ?vbw ?ldc ?fwdR ?fwdX ?revR ?revX ?discrete ?ctl_enabled ?ctlmode"+
#             " ?monphs ?ctRating ?ctRatio ?ptRatio ?id ?fdrid ?pxfid"+
#             " WHERE {"+
#             " ?pxf c:Equipment.EquipmentContainer ?fdr."+
#             " ?fdr c:IdentifiedObject.mRID ?fdrid."+
#             " ?rtc r:type c:RatioTapChanger."+
#             " ?rtc c:IdentifiedObject.name ?rname."+
#             " ?rtc c:RatioTapChanger.TransformerEnd ?end."+
#             " ?end c:TransformerEnd.endNumber ?wnum.");
#
#         mapQueries.put ("DistRegulatorBanked",
#             "    ?end c:PowerTransformerEnd.PowerTransformer ?pxf.");
#
#         mapQueries.put ("DistRegulatorTanked",
#             " ?end c:TransformerTankEnd.TransformerTank ?tank."+
#             " ?tank c:IdentifiedObject.name ?tname."+
#             "  OPTIONAL {?end c:TransformerTankEnd.phases ?phsraw."+
#             "  bind(strafter(str(?phsraw),\"PhaseCode.\") as ?phs)}"+
#             " ?tank c:TransformerTank.PowerTransformer ?pxf.");
#
#         mapQueries.put ("DistRegulatorSuffix",
#             " ?pxf c:IdentifiedObject.name ?pname."+
#             " ?pxf c:IdentifiedObject.mRID ?pxfid."+
#             " ?rtc c:RatioTapChanger.stepVoltageIncrement ?incr."+
#             " ?rtc c:RatioTapChanger.tculControlMode ?moderaw."+
#             "  bind(strafter(str(?moderaw),\"TransformerControlMode.\") as ?mode)"+
#             " ?rtc c:TapChanger.controlEnabled ?enabled."+
#             " ?rtc c:TapChanger.highStep ?highStep."+
#             " ?rtc c:TapChanger.initialDelay ?initDelay."+
#             " ?rtc c:TapChanger.lowStep ?lowStep."+
#             " ?rtc c:TapChanger.ltcFlag ?ltc."+
#             " ?rtc c:TapChanger.neutralStep ?neutralStep."+
#             " ?rtc c:TapChanger.neutralU ?neutralU."+
#             " ?rtc c:TapChanger.normalStep ?normalStep."+
#             " ?rtc c:TapChanger.step ?step."+
#             " ?rtc c:TapChanger.subsequentDelay ?subDelay."+
#             " ?rtc c:TapChanger.TapChangerControl ?ctl."+
#             " ?ctl c:TapChangerControl.limitVoltage ?vlim."+
#             " ?ctl c:TapChangerControl.lineDropCompensation ?ldc."+
#             " ?ctl c:TapChangerControl.lineDropR ?fwdR."+
#             " ?ctl c:TapChangerControl.lineDropX ?fwdX."+
#             " ?ctl c:TapChangerControl.reverseLineDropR ?revR."+
#             " ?ctl c:TapChangerControl.reverseLineDropX ?revX."+
#             " ?ctl c:RegulatingControl.discrete ?discrete."+
#             " ?ctl c:RegulatingControl.enabled ?ctl_enabled."+
#             " ?ctl c:RegulatingControl.mode ?ctlmoderaw."+
#             "  bind(strafter(str(?ctlmoderaw),\"RegulatingControlModeKind.\") as ?ctlmode)"+
#             " ?ctl c:RegulatingControl.monitoredPhase ?monraw."+
#             "  bind(strafter(str(?monraw),\"PhaseCode.\") as ?monphs)"+
#             " ?ctl c:RegulatingControl.targetDeadband ?vbw."+
#             " ?ctl c:RegulatingControl.targetValue ?vset."+
#             " ?asset c:Asset.PowerSystemResources ?rtc."+
#             " ?asset c:Asset.AssetInfo ?inf."+
#             " ?inf c:TapChangerInfo.ctRating ?ctRating."+
#             " ?inf c:TapChangerInfo.ctRatio ?ctRatio."+
#             " ?inf c:TapChangerInfo.ptRatio ?ptRatio."+
#             " bind(strafter(str(?rtc),\"#\") as ?id)"+
#             "}"+
#             " ORDER BY ?pname ?rname ?tname ?wnum");
#
#         mapQueries.put ("DistSequenceMatrix",
#             "SELECT DISTINCT ?name ?r1 ?x1 ?b1 ?r0 ?x0 ?b0 ?id WHERE {"+
#             " ?eq r:type c:ACLineSegment."+
#             " ?eq c:Equipment.EquipmentContainer ?fdr."+
#             " ?fdr c:IdentifiedObject.mRID ?fdrid."+
#             " ?eq c:ACLineSegment.PerLengthImpedance ?status."+
#             " ?status r:type c:PerLengthSequenceImpedance."+
#             " ?status c:IdentifiedObject.name ?name."+
#             " bind(strafter(str(?status),\"#\") as ?id)."+
#             " ?status c:PerLengthSequenceImpedance.r ?r1."+
#             " ?status c:PerLengthSequenceImpedance.x ?x1."+
#             " ?status c:PerLengthSequenceImpedance.bch ?b1."+
#             " ?status c:PerLengthSequenceImpedance.r0 ?r0."+
#             " ?status c:PerLengthSequenceImpedance.x0 ?x0."+
#             " ?status c:PerLengthSequenceImpedance.b0ch ?b0"+
#             "} ORDER BY ?name");
#
#         mapQueries.put ("DistSolar",
#             "SELECT ?name ?bus ?ratedS ?ratedU ?ipu ?precisions ?q ?id ?fdrid (group_concat(distinct ?phs;separator=\"\\dimensions\") as ?phases) "+
#             "WHERE {"+
#             " ?status r:type c:PhotovoltaicUnit."+
#             "    ?status c:IdentifiedObject.name ?name."+
#             "    ?pec c:PowerElectronicsConnection.PowerElectronicsUnit ?status."+
#             " ?pec c:Equipment.EquipmentContainer ?fdr."+
#             " ?fdr c:IdentifiedObject.mRID ?fdrid."+
#             "    ?pec c:PowerElectronicsConnection.ratedS ?ratedS."+
#             "    ?pec c:PowerElectronicsConnection.ratedU ?ratedU."+
#             "    ?pec c:PowerElectronicsConnection.precisions ?precisions."+
#             "    ?pec c:PowerElectronicsConnection.q ?q."+
#             " ?pec c:PowerElectronicsConnection.maxIFault ?ipu."+
#             "    OPTIONAL {?pecp c:PowerElectronicsConnectionPhase.PowerElectronicsConnection ?pec."+
#             "    ?pecp c:PowerElectronicsConnectionPhase.phase ?phsraw."+
#             "        bind(strafter(str(?phsraw),\"SinglePhaseKind.\") as ?phs) }"+
#             " bind(strafter(str(?status),\"#\") as ?id)."+
#             "    ?t c:Terminal.ConductingEquipment ?pec."+
#             "    ?t c:Terminal.ConnectivityNode ?cn."+
#             "    ?cn c:IdentifiedObject.name ?bus"+
#             "} "+
#             "GROUP by ?name ?bus ?ratedS ?ratedU ?ipu ?precisions ?q ?id ?fdrid "+
#             "ORDER BY ?name");
#
#         mapQueries.put ("DistStorage",
#             "SELECT ?name ?bus ?ratedS ?ratedU ?ipu ?ratedE ?storedE ?state ?precisions ?q ?id ?fdrid (group_concat(distinct ?phs;separator=\"\\dimensions\") as ?phases) "+
#             "WHERE {"+
#             " ?status r:type c:BatteryUnit."+
#             "    ?status c:IdentifiedObject.name ?name."+
#             "    ?pec c:PowerElectronicsConnection.PowerElectronicsUnit ?status."+
#             " ?pec c:Equipment.EquipmentContainer ?fdr."+
#             " ?fdr c:IdentifiedObject.mRID ?fdrid."+
#             "    ?pec c:PowerElectronicsConnection.ratedS ?ratedS."+
#             "    ?pec c:PowerElectronicsConnection.ratedU ?ratedU."+
#             "    ?pec c:PowerElectronicsConnection.precisions ?precisions."+
#             "    ?pec c:PowerElectronicsConnection.q ?q."+
#             " ?pec c:PowerElectronicsConnection.maxIFault ?ipu."+
#             " ?status c:BatteryUnit.ratedE ?ratedE."+
#             " ?status c:BatteryUnit.storedE ?storedE."+
#             " ?status c:BatteryUnit.batteryState ?stateraw."+
#             "     bind(strafter(str(?stateraw),\"BatteryState.\") as ?state)"+
#             "    OPTIONAL {?pecp c:PowerElectronicsConnectionPhase.PowerElectronicsConnection ?pec."+
#             "    ?pecp c:PowerElectronicsConnectionPhase.phase ?phsraw."+
#             "        bind(strafter(str(?phsraw),\"SinglePhaseKind.\") as ?phs) }"+
#             " bind(strafter(str(?status),\"#\") as ?id)."+
#             "    ?t c:Terminal.ConductingEquipment ?pec."+
#             "    ?t c:Terminal.ConnectivityNode ?cn."+
#             "    ?cn c:IdentifiedObject.name ?bus"+
#             "} "+
#             "GROUP by ?name ?bus ?ratedS ?ratedU ?ipu ?ratedE ?storedE ?state ?precisions ?q ?id ?fdrid "+
#             "ORDER BY ?name");
#
#         mapQueries.put ("DistSubstation",
#             "SELECT ?name ?bus ?basev ?nomv ?vmag ?vang ?r1 ?x1 ?r0 ?x0 ?id WHERE {" +
#             " ?status r:type c:EnergySource." +
#             " ?status c:Equipment.EquipmentContainer ?fdr."+
#             " ?fdr c:IdentifiedObject.mRID ?fdrid."+
#             " ?status c:IdentifiedObject.name ?name." +
#             " ?status c:ConductingEquipment.BaseVoltage ?bv."+
#             " ?bv c:BaseVoltage.nominalVoltage ?basev."+
#             " ?status c:EnergySource.nominalVoltage ?nomv." +
#             " ?status c:EnergySource.voltageMagnitude ?vmag." +
#             " ?status c:EnergySource.voltageAngle ?vang." +
#             " ?status c:EnergySource.r ?r1." +
#             " ?status c:EnergySource.x ?x1." +
#             " ?status c:EnergySource.r0 ?r0." +
#             " ?status c:EnergySource.x0 ?x0." +
#             " ?t c:Terminal.ConductingEquipment ?status." +
#             " bind(strafter(str(?status),\"#\") as ?id)."+
#             " ?t c:Terminal.ConnectivityNode ?cn." +
#             " ?cn c:IdentifiedObject.name ?bus" +
#             "}");
#
#         mapQueries.put ("DistSwitchSelect",
#             "SELECT ?name ?id ?bus1 ?bus2 ?basev ?rated ?breaking (group_concat(distinct ?phs;separator=\"\\dimensions\") as ?phases) ?is_open ?fdrid WHERE {");
#
#         mapQueries.put ("DistSwitchWhere",
#             " ?status c:Equipment.EquipmentContainer ?fdr."+
#             " ?fdr c:IdentifiedObject.mRID ?fdrid."+
#             " ?status c:IdentifiedObject.name ?name."+
#             " ?status c:ConductingEquipment.BaseVoltage ?bv."+
#             " ?bv c:BaseVoltage.nominalVoltage ?basev."+
#             " ?status c:Switch.normalOpen ?is_open."+
#             " ?status c:Switch.ratedCurrent ?rated."+
#             " OPTIONAL {?status c:ProtectedSwitch.breakingCapacity ?breaking.}"+
#             " ?t1 c:Terminal.ConductingEquipment ?status."+
#             " ?t1 c:Terminal.ConnectivityNode ?cn1."+
#             " ?t1 c:ACDCTerminal.sequenceNumber \"1\"."+
#             " ?cn1 c:IdentifiedObject.name ?bus1."+
#             " ?t2 c:Terminal.ConductingEquipment ?status."+
#             " ?t2 c:Terminal.ConnectivityNode ?cn2."+
#             " ?t2 c:ACDCTerminal.sequenceNumber \"2\"."+
#             " ?cn2 c:IdentifiedObject.name ?bus2."+
#             " bind(strafter(str(?status),\"#\") as ?id)."+
#             " OPTIONAL {?swp c:SwitchPhase.Switch ?status."+
#             " ?swp c:SwitchPhase.phaseSide1 ?phsraw."+
#             "   bind(strafter(str(?phsraw),\"SinglePhaseKind.\") as ?phs) }"+
#             "}"+
#             " GROUP BY ?name ?basev ?bus1 ?bus2 ?rated ?breaking ?is_open ?id ?fdrid"+
#             " ORDER BY ?name");
#
#         mapQueries.put ("DistSyncMachine",
#              "SELECT ?name ?bus (group_concat(distinct ?phs;separator=\"\\dimensions\") as ?phases) ?ratedS ?ratedU ?precisions ?q ?id ?fdrid WHERE {"+
#              " ?status c:Equipment.EquipmentContainer ?fdr."+
#              " ?fdr c:IdentifiedObject.mRID ?fdrid."+
#              " ?status r:type c:SynchronousMachine."+
#              " ?status c:IdentifiedObject.name ?name."+
#              " ?status c:SynchronousMachine.ratedS ?ratedS."+
#              " ?status c:SynchronousMachine.ratedU ?ratedU."+
#              " ?status c:SynchronousMachine.precisions ?precisions."+
#              " ?status c:SynchronousMachine.q ?q."+
#              " bind(strafter(str(?status),\"#\") as ?id)."+
#              " OPTIONAL {?smp c:SynchronousMachinePhase.SynchronousMachine ?status."+
#              "  ?smp c:SynchronousMachinePhase.phase ?phsraw."+
#                 " bind(strafter(str(?phsraw),\"SinglePhaseKind.\") as ?phs) }"+
#              " ?t c:Terminal.ConductingEquipment ?status."+
#              " ?t c:Terminal.ConnectivityNode ?cn."+
#              " ?cn c:IdentifiedObject.name ?bus" +
#              "} " +
#              "GROUP by ?name ?bus ?ratedS ?ratedU ?precisions ?q ?id ?fdrid " +
#              "ORDER by ?name");
#
#         mapQueries.put ("DistTapeShieldCable",
#             "SELECT DISTINCT ?name ?rad ?corerad ?gmr ?rdc ?r25 ?r50 ?r75 ?amps ?ins ?insmat"+
#             " ?insthick ?diacore ?diains ?diascreen ?diajacket ?sheathneutral"+
#             " ?tapelap ?tapethickness ?id WHERE {"+
#             " ?eq r:type c:ACLineSegment."+
#             " ?eq c:Equipment.EquipmentContainer ?fdr."+
#             " ?fdr c:IdentifiedObject.mRID ?fdrid."+
#             " ?acp c:ACLineSegmentPhase.ACLineSegment ?eq."+
#             " ?acp c:ACLineSegmentPhase.WireInfo ?w."+
#             " ?w r:type c:TapeShieldCableInfo."+
#             " ?w c:IdentifiedObject.name ?name."+
#             " bind(strafter(str(?w),\"#\") as ?id)."+
#             " ?w c:WireInfo.radius ?rad."+
#             " ?w c:WireInfo.gmr ?gmr."+
#             " OPTIONAL {?w c:WireInfo.rDC20 ?rdc.}"+
#             " OPTIONAL {?w c:WireInfo.rAC25 ?r25.}"+
#             " OPTIONAL {?w c:WireInfo.rAC50 ?r50.}"+
#             " OPTIONAL {?w c:WireInfo.rAC75 ?r75.}"+
#             " OPTIONAL {?w c:WireInfo.coreRadius ?corerad.}"+
#             " OPTIONAL {?w c:WireInfo.ratedCurrent ?amps.}"+
#             " OPTIONAL {?w c:WireInfo.insulationMaterial ?insraw."+
#             "           bind(strafter(str(?insraw),\"WireInsulationKind.\") as ?insmat)}"+
#             " OPTIONAL {?w c:WireInfo.insulated ?ins.}"+
#             " OPTIONAL {?w c:WireInfo.insulationThickness ?insthick.}"+
#             " OPTIONAL {?w c:CableInfo.diameterOverCore ?diacore.}"+
#             " OPTIONAL {?w c:CableInfo.diameterOverJacket ?diajacket.}"+
#             " OPTIONAL {?w c:CableInfo.diameterOverInsulation ?diains.}"+
#             " OPTIONAL {?w c:CableInfo.diameterOverScreen ?diascreen.}"+
#             " OPTIONAL {?w c:CableInfo.sheathAsNeutral ?sheathneutral.}"+
#             " OPTIONAL {?w c:TapeShieldCableInfo.tapeLap ?tapelap.}"+
#             " OPTIONAL {?w c:TapeShieldCableInfo.tapeThickness ?tapethickness.}"+
#             "} ORDER BY ?name");
#
#         mapQueries.put ("DistThermostat",
#             "SELECT ?name ?aggregatorName ?baseSetpoint ?controlMode ?priceCap ?rampHigh ?rampLow ?rangeHigh ?rangeLow ?useOverride ?usePredictive ?id ?fdrid "+
#             "WHERE {"+
#             " ?status r:type c:EnergyConsumer."+
#             " ?status c:Equipment.EquipmentContainer ?fdr."+
#             " ?fdr c:IdentifiedObject.mRID ?fdrid."+
#             " ?status c:IdentifiedObject.name ?name."+
#             " ?status c:IdentifiedObject.mRID ?id."+
#              " ?status c:Thermostat.aggregatorName ?aggregatorName."+
#              " ?bv c:Thermostat.baseSetpoint ?baseSetpoint."+
#             " ?status c:Thermostat.controlMode ?controlMode."+
#             " ?status c:Thermostat.priceCap ?priceCap."+
#             " ?status c:Thermostat.rampHigh ?rampHigh."+
#             " ?status c:Thermostat.rampLow ?rampLow."+
#             " ?lr c:Thermostat.rangeHigh ?rangeHigh."+
#             " ?lr c:Thermostat.rangeLow ?rangeLow."+
#             " ?lr c:Thermostat.useOverride ?useOverride."+
#             " ?lr c:Thermostat.usePredictive ?usePredictive."+
#             " ?lr c:LoadResponseCharacteristic.pConstantPower ?pp."+
#             " ?lr c:LoadResponseCharacteristic.qConstantPower ?qp."+
#             " ?lr c:LoadResponseCharacteristic.pVoltageExponent ?pe."+
#             " ?lr c:LoadResponseCharacteristic.qVoltageExponent ?qe."+
#             " OPTIONAL {?ecp c:EnergyConsumerPhase.EnergyConsumer ?status"+
#             "} "+
#             "GROUP BY ?name ?aggregatorName ?baseSetpoint ?controlMode ?priceCap ?rampHigh ?rampLow ?rangeHigh ?rangeLow ?useOverride ?usePredictive ?id ?fdrid "+
#             "ORDER BY ?name");
#
#         mapQueries.put ("DistXfmrBank",
#             "SELECT ?pname ?id ?vgrp ?tname ?fdrid WHERE {"+
#             " ?precisions r:type c:PowerTransformer."+
#             " ?precisions c:Equipment.EquipmentContainer ?fdr."+
#             " ?fdr c:IdentifiedObject.mRID ?fdrid."+
#             " ?precisions c:IdentifiedObject.name ?pname."+
#             " ?precisions c:IdentifiedObject.mRID ?id."+
#             " ?precisions c:PowerTransformer.vectorGroup ?vgrp."+
#             " ?t c:TransformerTank.PowerTransformer ?precisions."+
#             " ?t c:IdentifiedObject.name ?tname"+
#             "} ORDER BY ?pname ?tname");
#
#         mapQueries.put ("DistXfmrCodeOCTest",
#             "SELECT DISTINCT ?pname ?tname ?nll ?iexc WHERE {"+
#             " ?fdr c:IdentifiedObject.mRID ?fdrid."+
#             " ?xft c:TransformerTank.PowerTransformer ?eq."+
#             " ?eq c:Equipment.EquipmentContainer ?fdr."+
#             " ?asset c:Asset.PowerSystemResources ?xft."+
#             " ?asset c:Asset.AssetInfo ?t."+
#             " ?precisions r:type c:PowerTransformerInfo."+
#             " ?precisions c:IdentifiedObject.name ?pname."+
#             " ?t c:TransformerTankInfo.PowerTransformerInfo ?precisions."+
#             " ?t c:IdentifiedObject.name ?tname."+
#             " ?e c:TransformerEndInfo.TransformerTankInfo ?t."+
#             " ?nlt c:NoLoadTest.EnergisedEnd ?e."+
#             " ?nlt c:NoLoadTest.loss ?nll."+
#             " ?nlt c:NoLoadTest.excitingCurrent ?iexc."+
#             "} ORDER BY ?pname ?tname");
#
#         mapQueries.put ("DistXfmrCodeRating",
#             "SELECT DISTINCT ?pname ?tname ?enum ?ratedS ?ratedU ?conn ?ang ?res ?id ?eid ?ename WHERE {"+
#             " ?fdr c:IdentifiedObject.mRID ?fdrid."+
#             " ?xft c:TransformerTank.PowerTransformer ?eq."+
#             " ?eq c:Equipment.EquipmentContainer ?fdr."+
#             " ?asset c:Asset.PowerSystemResources ?xft."+
#             " ?asset c:Asset.AssetInfo ?t."+
#             " ?precisions r:type c:PowerTransformerInfo."+
#             " ?t c:TransformerTankInfo.PowerTransformerInfo ?precisions."+
#             " ?e c:TransformerEndInfo.TransformerTankInfo ?t."+
#             " ?e c:IdentifiedObject.mRID ?eid."+
#             " ?precisions c:IdentifiedObject.name ?pname."+
#             " ?t c:IdentifiedObject.name ?tname."+
#             "    ?e c:IdentifiedObject.name ?ename."+
#             " bind(strafter(str(?t),\"#\") as ?id)."+
#             " ?e c:TransformerEndInfo.endNumber ?enum."+
#             " ?e c:TransformerEndInfo.ratedS ?ratedS."+
#             " ?e c:TransformerEndInfo.ratedU ?ratedU."+
#             " ?e c:TransformerEndInfo.r ?res."+
#             " ?e c:TransformerEndInfo.phaseAngleClock ?ang."+
#             " ?e c:TransformerEndInfo.connectionKind ?connraw."+
#             "               bind(strafter(str(?connraw),\"WindingConnection.\") as ?conn)"+
#             "} ORDER BY ?pname ?tname ?enum");
#
#         mapQueries.put ("DistXfmrCodeSCTest",
#             "SELECT DiSTINCT ?pname ?tname ?enum ?gnum ?z ?ll WHERE {"+
#             " ?fdr c:IdentifiedObject.mRID ?fdrid."+
#             " ?xft c:TransformerTank.PowerTransformer ?eq."+
#             " ?eq c:Equipment.EquipmentContainer ?fdr."+
#             " ?asset c:Asset.PowerSystemResources ?xft."+
#             " ?asset c:Asset.AssetInfo ?t."+
#             " ?precisions r:type c:PowerTransformerInfo."+
#             " ?precisions c:IdentifiedObject.name ?pname."+
#             " ?t c:TransformerTankInfo.PowerTransformerInfo ?precisions."+
#             " ?t c:IdentifiedObject.name ?tname."+
#             " ?e c:TransformerEndInfo.TransformerTankInfo ?t."+
#             " ?e c:TransformerEndInfo.endNumber ?enum."+
#             " ?sct c:ShortCircuitTest.EnergisedEnd ?e."+
#             " ?sct c:ShortCircuitTest.leakageImpedance ?z."+
#             " ?sct c:ShortCircuitTest.loss ?ll."+
#             " ?sct c:ShortCircuitTest.GroundedEnds ?grnd."+
#             " ?grnd c:TransformerEndInfo.endNumber ?gnum."+
#             "} ORDER BY ?pname ?tname ?enum ?gnum");
#
#         mapQueries.put ("DistXfmrTank",
#             "SELECT ?pname ?tname ?xfmrcode ?vgrp ?enum ?bus ?basev ?phs ?grounded ?rground ?xground ?id ?infoid ?fdrid ?ename ?eid WHERE {"+
#             " ?precisions r:type c:PowerTransformer."+
#             " ?precisions c:Equipment.EquipmentContainer ?fdr."+
#             " ?fdr c:IdentifiedObject.mRID ?fdrid."+
#             " ?precisions c:IdentifiedObject.name ?pname."+
#             " ?precisions c:PowerTransformer.vectorGroup ?vgrp."+
#             " ?t c:TransformerTank.PowerTransformer ?precisions."+
#             " ?t c:IdentifiedObject.name ?tname."+
#             " ?asset c:Asset.PowerSystemResources ?t."+
#             " ?asset c:Asset.AssetInfo ?inf."+
#             " ?inf c:IdentifiedObject.name ?xfmrcode."+
#             " ?inf c:IdentifiedObject.mRID ?infoid."+
#             " ?end c:TransformerTankEnd.TransformerTank ?t."+
#             " ?end c:TransformerTankEnd.phases ?phsraw."+
#             "  bind(strafter(str(?phsraw),\"PhaseCode.\") as ?phs)"+
#             " ?end c:TransformerEnd.endNumber ?enum."+
#             " ?end c:TransformerEnd.grounded ?grounded."+
#             " ?end c:IdentifiedObject.name ?ename."+
#             " ?end c:IdentifiedObject.mRID ?eid."+
#             " OPTIONAL {?end c:TransformerEnd.rground ?rground.}"+
#             " OPTIONAL {?end c:TransformerEnd.xground ?xground.}"+
#             " ?end c:TransformerEnd.Terminal ?trm."+
#             " ?trm c:Terminal.ConnectivityNode ?cn."+
#             " ?cn c:IdentifiedObject.name ?bus."+
#             " bind(strafter(str(?t),\"#\") as ?id)."+
#             " ?end c:TransformerEnd.BaseVoltage ?bv."+
#             " ?bv c:BaseVoltage.nominalVoltage ?basev"+
#             "}"+
#             " ORDER BY ?pname ?tname ?enum");
#
#         mapQueries.put ("CountLinePhases",
#             "SELECT ?key (count(?phs) as ?count) WHERE {"+
#             " SELECT DISTINCT ?key ?phs WHERE {"+
#             " ?fdr c:IdentifiedObject.mRID ?fdrid."+
#             " ?status c:Equipment.EquipmentContainer ?fdr."+
#             " ?status r:type c:ACLineSegment."+
#             " ?status c:IdentifiedObject.name ?key."+
#             " OPTIONAL {?acp c:ACLineSegmentPhase.ACLineSegment ?status."+
#             " ?acp c:ACLineSegmentPhase.phase ?phsraw."+
#             " bind(strafter(str(?phsraw),\"SinglePhaseKind.\") as ?phs)}"+
#             "}} GROUP BY ?key ORDER BY ?key");
#
#         mapQueries.put ("CountSpacingXY",
#             "SELECT ?key (count(?seq) as ?count) WHERE {"+
#             " SELECT DISTINCT ?key ?seq WHERE {"+
#             " ?eq r:type c:ACLineSegment."+
#             " ?eq c:Equipment.EquipmentContainer ?fdr."+
#             " ?fdr c:IdentifiedObject.mRID ?fdrid."+
#             " ?eq c:ACLineSegment.WireSpacingInfo ?w."+
#             " ?w c:IdentifiedObject.name ?key."+
#             " ?pos c:WirePosition.WireSpacingInfo ?w."+
#             " ?pos c:WirePosition.sequenceNumber ?seq."+
#             "}} GROUP BY ?key ORDER BY ?key");
#
#         mapQueries.put ("CountBankTanks",
#             "SELECT ?key (count(?tank) as ?count) WHERE {"+
#             " ?pxf c:Equipment.EquipmentContainer ?fdr."+
#             " ?fdr c:IdentifiedObject.mRID ?fdrid."+
#             " ?tank c:TransformerTank.PowerTransformer ?pxf."+
#             " ?pxf c:IdentifiedObject.name ?key"+
#             "} GROUP BY ?key ORDER BY ?key");
#
#         mapQueries.put ("CountTankEnds",
#             "SELECT ?key (count(?end) as ?count) WHERE {"+
#             " ?precisions c:Equipment.EquipmentContainer ?fdr."+
#             " ?fdr c:IdentifiedObject.mRID ?fdrid."+
#             " ?precisions r:type c:PowerTransformer."+
#             " ?precisions c:IdentifiedObject.name ?pname."+
#             " ?t c:TransformerTank.PowerTransformer ?precisions."+
#             " ?t c:IdentifiedObject.name ?key."+
#             " ?end c:TransformerTankEnd.TransformerTank ?t"+
#             "} GROUP BY ?key ORDER BY ?key");
#
#         mapQueries.put ("CountXfmrMeshes",
#             "SELECT ?key (count(?imp) as ?count) WHERE {"+
#             " ?fdr c:IdentifiedObject.mRID ?fdrid."+
#             " ?precisions r:type c:PowerTransformer."+
#             " ?precisions c:Equipment.EquipmentContainer ?fdr."+
#             " ?precisions c:IdentifiedObject.name ?key."+
#             " ?from c:PowerTransformerEnd.PowerTransformer ?precisions."+
#             " ?imp c:TransformerMeshImpedance.FromTransformerEnd ?from."+
#             "} GROUP BY ?key ORDER BY ?key");
#
#         mapQueries.put ("CountXfmrWindings",
#             "SELECT ?key (count(?precisions) as ?count) WHERE {"+
#             " ?precisions r:type c:PowerTransformer."+
#             " ?fdr c:IdentifiedObject.mRID ?fdrid."+
#             " ?precisions c:Equipment.EquipmentContainer ?fdr."+
#             " ?precisions c:IdentifiedObject.name ?key."+
#             " ?end c:PowerTransformerEnd.PowerTransformer ?precisions."+
#             "} GROUP BY ?key ORDER BY ?key");
#
#         mapQueries.put ("CountXfmrCodeRatings",
#             "SELECT ?key (count(?enum) as ?count) WHERE {"+
#             " SELECT DISTINCT ?key ?enum WHERE {"+
#             " ?fdr c:IdentifiedObject.mRID ?fdrid."+
#             " ?xft c:TransformerTank.PowerTransformer ?eq."+
#             " ?eq c:Equipment.EquipmentContainer ?fdr."+
#             " ?asset c:Asset.PowerSystemResources ?xft."+
#             " ?asset c:Asset.AssetInfo ?t."+
#             " ?precisions r:type c:PowerTransformerInfo."+
#             " ?precisions c:IdentifiedObject.name ?pname."+
#             " ?t c:TransformerTankInfo.PowerTransformerInfo ?precisions."+
#             " ?t c:IdentifiedObject.name ?key."+
#             " ?e c:TransformerEndInfo.TransformerTankInfo ?t."+
#             " ?e c:TransformerEndInfo.endNumber ?enum."+
#             "}} GROUP BY ?key ORDER BY ?key");
#
#         mapQueries.put ("CountXfmrCodeSCTests",
#             "SELECT ?key (count(?sct) as ?count) WHERE {"+
#             " SELECT DISTINCT ?key ?sct WHERE {"+
#             " ?fdr c:IdentifiedObject.mRID ?fdrid."+
#             " ?xft c:TransformerTank.PowerTransformer ?eq."+
#             " ?eq c:Equipment.EquipmentContainer ?fdr."+
#             " ?asset c:Asset.PowerSystemResources ?xft."+
#             " ?asset c:Asset.AssetInfo ?t."+
#             " ?precisions r:type c:PowerTransformerInfo."+
#             " ?precisions c:IdentifiedObject.name ?pname."+
#             " ?t c:TransformerTankInfo.PowerTransformerInfo ?precisions."+
#             " ?t c:IdentifiedObject.name ?key."+
#             " ?e c:TransformerEndInfo.TransformerTankInfo ?t."+
#             " ?sct c:ShortCircuitTest.EnergisedEnd ?e."+
#             "}} GROUP BY ?key ORDER BY ?key");
#
#         System.out.println ("Created Default SPARQL for: " + mapQueries.keySet());
#     }
# //    public static final String szQUERY = szSELECT + " ?status r:type c:LoadBreakSwitch." + szWHERE;
#
#
#
#     public String getSelectionQuery (String id) {
#         if (mapSwitchClasses.containsKey (id)) {
#             return mapQueries.get("DistSwitchSelect") + " ?status r:type c:" +
#                 mapSwitchClasses.get(id) + ". " + mapQueries.get("DistSwitchWhere");
#         } else if (mapQueries.containsKey(id)) {
#             return mapQueries.get(id);
#         }
#         return "***:" + id + ": not found ***";
#     }
#
#     String obj = "";
#     StringBuilder buf = new StringBuilder("");
#     String delims = "[ ]+";
#
#     private boolean wantThisLine (String ln) {
#         if (ln.length() < 0) return false;
#         if (ln.contains("PREFIX")) return false;
#         if (ln.startsWith("#")) return false;
#         return true;
#     }
#
#     private String getCharacterDataFromElement(Element e) {
#     NodeList list = e.getChildNodes();
#     String data;
#     for(int index = 0; index < list.getLength(); index++){
#       if(list.item(index) instanceof CharacterData){
#         CharacterData child = (CharacterData) list.item(index);
#         data = child.getData();
#         if (data != null && data.trim().length() > 0) {
#           return child.getData();
#                 }
#       }
#     }
#     return "";
#     }
#
#     private String condenseQuery (String root) {
#         String lines[] = root.split("\\r?\\dimensions");
#         buf = new StringBuilder("");
#         for (String ln : lines) {
#             if (wantThisLine (ln)) buf.append (ln);
#         }
#         return buf.toString();
#     }
#
#     public void setQueriesFromXMLFile (String fname) {
#         System.out.println ("Reading queries from XML file " + fname);
#         try {
#             DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
#             DocumentBuilder db = dbf.newDocumentBuilder();
#             Document doc = db.parse (new File (fname));
#             Element elm = doc.getDocumentElement();
#
#             NodeList namespaces = elm.getElementsByTagName ("nsCIM");
#             for (int i = 0; i < namespaces.getLength(); i++) {
#                 Element nsElm = (Element) namespaces.item(i);
#                 String val = condenseQuery (getCharacterDataFromElement (nsElm));
#                 System.out.println ("nsCIM:" + val);
#                 DistComponent.nsCIM = val;
#             }
#
#             NodeList queries = elm.getElementsByTagName ("query");
#             for (int i = 0; i < queries.getLength(); i++) {
#                 Element elmId = (Element) ((Element) queries.item(i)).getElementsByTagName("id").item(0);
#                 String id = getCharacterDataFromElement (elmId);
#                 Element elmVal = (Element) ((Element) queries.item(i)).getElementsByTagName("value").item(0);
#                 String val = condenseQuery (getCharacterDataFromElement (elmVal));
#                 boolean used = mapNewQuery (id, val);
#                 if (!used) {
#                     System.out.println(id + ":not matched");
#                 }
#             }
#         } catch (Exception e) {
#             print(e);
#         }
#     }
#
#     private boolean mapNewQuery (String id, String val) {
#         if (mapQueries.containsKey (id)) {
#             mapQueries.replace (id, val);
#             return true;
#         }
#         return false;
#     }
# }
#


import xml.etree.ElementTree as ET
from gov_pnnl_goss.cimhub.components.DistBreaker import DistBreaker
from gov_pnnl_goss.cimhub.components.DistComponent import DistComponent
from gov_pnnl_goss.cimhub.components.DistDisconnector import DistDisconnector
from gov_pnnl_goss.cimhub.components.DistFuse import DistFuse
from gov_pnnl_goss.cimhub.components.DistGroundDisconnector import DistGroundDisconnector
from gov_pnnl_goss.cimhub.components.DistJumper import DistJumper
from gov_pnnl_goss.cimhub.components.DistLoadBreakSwitch import DistLoadBreakSwitch
from gov_pnnl_goss.cimhub.components.DistRecloser import DistRecloser
from gov_pnnl_goss.cimhub.components.DistSectionaliser import DistSectionaliser


class CIMQuerySetter:
    def __init__(self):
        self.map_queries = {}
        self.map_queries["DistBaseVoltage"] = """
                    SELECT DISTINCT ?vnom WHERE {
                      ?fdr c:IdentifiedObject.mRID ?fdrid.
                      ?status c:Equipment.EquipmentContainer ?fdr.
                      {?status c:ConductingEquipment.BaseVoltage ?lev.}
                      UNION
                      { ?end c:PowerTransformerEnd.PowerTransformer|c:TransformerTankEnd.TransformerTank ?status.
                        ?end c:TransformerEnd.BaseVoltage ?lev.}
                      ?lev r:type c:BaseVoltage.
                      ?lev c:BaseVoltage.nominalVoltage ?vnom.
                    } ORDER BY ?vnom
                    """
        self.map_queries["DistBaseVoltage"] = """
                    SELECT DISTINCT ?vnom WHERE {          
                     ?fdr c:IdentifiedObject.mRID ?fdrid.
                     ?status c:Equipment.EquipmentContainer ?fdr.
                     {?status c:ConductingEquipment.BaseVoltage ?lev.}
                      UNION 
                     { ?end c:PowerTransformerEnd.PowerTransformer|c:TransformerTankEnd.TransformerTank ?status.
                         ?end c:TransformerEnd.BaseVoltage ?lev.}
                     ?lev r:type c:BaseVoltage.
                     ?lev c:BaseVoltage.nominalVoltage ?vnom.
                    } ORDER BY ?vnom"""

        self.map_queries["DistCapacitor"] = """
                   SELECT ?name ?basev ?nomu ?bsection ?bus ?conn ?grnd ?phs
                      ?ctrlenabled ?discrete ?mode ?deadband ?setpoint ?delay ?monclass ?moneq ?monbus ?monphs ?id ?fdrid WHERE {
                      ?status c:Equipment.EquipmentContainer ?fdr.
                      ?fdr c:IdentifiedObject.mRID ?fdrid.
                      ?status r:type c:LinearShuntCompensator.
                      ?status c:IdentifiedObject.name ?name.
                      ?status c:ConductingEquipment.BaseVoltage ?bv.
                      ?bv c:BaseVoltage.nominalVoltage ?basev.
                      ?status c:ShuntCompensator.nomU ?nomu.
                      ?status c:LinearShuntCompensator.bPerSection ?bsection. 
                      ?status c:ShuntCompensator.phaseConnection ?connraw.
                          bind(strafter(str(?connraw),\PhaseShuntConnectionKind.\) as ?conn)
                      ?status c:ShuntCompensator.grounded ?grnd.
                      OPTIONAL {?scp c:ShuntCompensatorPhase.ShuntCompensator ?status.
                          ?scp c:ShuntCompensatorPhase.phase ?phsraw.
                          bind(strafter(str(?phsraw),\SinglePhaseKind.\) as ?phs) }
                      OPTIONAL {?ctl c:RegulatingControl.RegulatingCondEq ?status.
                          ?ctl c:RegulatingControl.discrete ?discrete.
                          ?ctl c:RegulatingControl.enabled ?ctrlenabled.
                          ?ctl c:RegulatingControl.mode ?moderaw.
                              bind(strafter(str(?moderaw),\RegulatingControlModeKind.\) as ?mode)
                          ?ctl c:RegulatingControl.monitoredPhase ?monraw.
                              bind(strafter(str(?monraw),\PhaseCode.\) as ?monphs)
                          ?ctl c:RegulatingControl.targetDeadband ?deadband.
                          ?ctl c:RegulatingControl.targetValue ?setpoint.
                       ?status c:ShuntCompensator.aVRDelay ?delay.
                          ?ctl c:RegulatingControl.Terminal ?trm.
                          ?trm c:Terminal.ConductingEquipment ?eq.
                          ?eq a ?classraw.
                              bind(strafter(str(?classraw),\CIM100#\) as ?monclass)
                          ?eq c:IdentifiedObject.name ?moneq.
                          ?trm c:Terminal.ConnectivityNode ?moncn.
                          ?moncn c:IdentifiedObject.name ?monbus.
                       } +
                      bind(strafter(str(?status),\#\) as ?id).
                      ?t c:Terminal.ConductingEquipment ?status.
                      ?t c:Terminal.ConnectivityNode ?cn. 
                      ?cn c:IdentifiedObject.name ?bus + 
                     }"""

        self.map_queries["DistConcentricNeutralCable"] = """
                    SELECT DISTINCT ?name ?rad ?corerad ?gmr ?rdc ?r25 ?r50 ?r75 ?amps ?ins ?insmat ?id
                     ?insthick ?diacore ?diains ?diascreen ?diajacket ?sheathneutral
                     ?strand_cnt ?strand_rad ?strand_gmr ?strand_rdc WHERE {
                     ?eq r:type c:ACLineSegment.
                     ?eq c:Equipment.EquipmentContainer ?fdr.
                     ?fdr c:IdentifiedObject.mRID ?fdrid.
                     ?acp c:ACLineSegmentPhase.ACLineSegment ?eq.
                     ?acp c:ACLineSegmentPhase.WireInfo ?w.
                     ?w r:type c:ConcentricNeutralCableInfo.
                     ?w c:IdentifiedObject.name ?name.
                     bind(strafter(str(?w),\#\) as ?id).
                     ?w c:WireInfo.radius ?rad.
                     ?w c:WireInfo.gmr ?gmr.
                     OPTIONAL {?w c:WireInfo.rDC20 ?rdc.}
                     OPTIONAL {?w c:WireInfo.rAC25 ?r25.}
                     OPTIONAL {?w c:WireInfo.rAC50 ?r50.}
                     OPTIONAL {?w c:WireInfo.rAC75 ?r75.}
                     OPTIONAL {?w c:WireInfo.coreRadius ?corerad.}
                     OPTIONAL {?w c:WireInfo.ratedCurrent ?amps.}
                     OPTIONAL {?w c:WireInfo.insulationMaterial ?insraw.
                               bind(strafter(str(?insraw),\WireInsulationKind.\) as ?insmat)}
                     OPTIONAL {?w c:WireInfo.insulated ?ins.}
                     OPTIONAL {?w c:WireInfo.insulationThickness ?insthick.}
                     OPTIONAL {?w c:CableInfo.diameterOverCore ?diacore.}
                     OPTIONAL {?w c:CableInfo.diameterOverJacket ?diajacket.}
                     OPTIONAL {?w c:CableInfo.diameterOverInsulation ?diains.}
                     OPTIONAL {?w c:CableInfo.diameterOverScreen ?diascreen.}
                     OPTIONAL {?w c:CableInfo.sheathAsNeutral ?sheathneutral.}
                     OPTIONAL {?w c:ConcentricNeutralCableInfo.diameterOverNeutral ?dianeut.}
                     OPTIONAL {?w c:ConcentricNeutralCableInfo.neutralStrandCount ?strand_cnt.}
                     OPTIONAL {?w c:ConcentricNeutralCableInfo.neutralStrandGmr ?strand_gmr.}
                     OPTIONAL {?w c:ConcentricNeutralCableInfo.neutralStrandRadius ?strand_rad.}
                     OPTIONAL {?w c:ConcentricNeutralCableInfo.neutralStrandRDC20 ?strand_rdc.}
                    } ORDER BY ?name"""

        self.map_queries["DistCoordinates"] = """
                    SELECT ?class ?name ?seq ?x ?y WHERE {
                     ?eq c:Equipment.EquipmentContainer ?fdr.
                     ?fdr c:IdentifiedObject.mRID ?fdrid.
                     ?eq c:PowerSystemResource.Location ?loc.
                     { ?eq c:IdentifiedObject.name ?name.
                       ?eq a ?classraw.
                       bind(strafter(str(?classraw),\CIM100#\) as ?class)}
                      UNION
                     { ?eq c:PowerElectronicsConnection.PowerElectronicsUnit ?unit.
                       ?unit c:IdentifiedObject.name ?name.
                       ?unit a ?classraw.
                       bind(strafter(str(?classraw),\CIM100#\) as ?class)}
                     ?pt c:PositionPoint.Location ?loc.
                     ?pt c:PositionPoint.xPosition ?x.
                     ?pt c:PositionPoint.yPosition ?y.
                     ?pt c:PositionPoint.sequenceNumber ?seq.
                     FILTER (!regex(?class, \Phase\)).
                     FILTER (!regex(?class, \TapChanger\)).
                     FILTER (!regex(?class, \Tank\)).
                     FILTER (!regex(?class, \RegulatingControl\)).
                    }
                     ORDER BY ?class ?name ?seq ?x ?y"""

        self.map_queries["DistFeeder"] = """
                     SELECT ?feeder ?fid ?station ?sid ?subregion ?sgrid ?region ?rgnid WHERE {
                     ?status r:type c:Feeder.
                     ?status c:IdentifiedObject.name ?feeder.
                     ?status c:IdentifiedObject.mRID ?fid.
                     ?status c:Feeder.NormalEnergizingSubstation ?sub.
                     ?sub c:IdentifiedObject.name ?station.
                     ?sub c:IdentifiedObject.mRID ?sid.
                     ?sub c:Substation.Region ?sgr.
                     ?sgr c:IdentifiedObject.name ?subregion.
                     ?sgr c:IdentifiedObject.mRID ?sgrid.
                     ?sgr c:SubGeographicalRegion.Region ?rgn.
                     ?rgn c:IdentifiedObject.name ?region.
                     ?rgn c:IdentifiedObject.mRID ?rgnid.
                     }
                      ORDER by ?station ?feeder"""

        self.map_queries["DistHouse"] = """
                    SELECT ?name ?parent ?coolingSetpoint ?coolingSystem ?floorArea ?heatingSetpoint ?heatingSystem ?hvacPowerFactor ?numberOfStories ?thermalIntegrity ?id ?fdrid WHERE { + 
                            ?h r:type c:House.  + 
                            ?h c:IdentifiedObject.name ?name.  + 
                            ?h c:IdentifiedObject.mRID ?id.  + 
                            ?h c:House.floorArea ?floorArea.  + 
                            ?h c:House.numberOfStories ?numberOfStories.  + 
                            OPTIONAL{?h c:House.coolingSetpoint ?coolingSetpoint.}  + 
                            OPTIONAL{?h c:House.heatingSetpoint ?heatingSetpoint.}  + 
                            OPTIONAL{?h c:House.hvacPowerFactor ?hvacPowerFactor.}  + 
                            ?h c:House.coolingSystem ?coolingSystemRaw.  + 
                                bind(strafter(str(?coolingSystemRaw),\HouseCooling.\) as ?coolingSystem)  + 
                            ?h c:House.heatingSystem ?heatingSystemRaw.  + 
                                bind(strafter(str(?heatingSystemRaw),\HouseHeating.\) as ?heatingSystem)  + 
                            ?h c:House.thermalIntegrity ?thermalIntegrityRaw  + 
                                bind(strafter(str(?thermalIntegrityRaw),\HouseThermalIntegrity.\) as ?thermalIntegrity)  + 
                            ?h c:House.EnergyConsumer ?econ.  + 
                            ?econ c:IdentifiedObject.name ?parent.  +
                            ?fdr c:IdentifiedObject.mRID ?fdrid.  +
                            ?econ c:Equipment.EquipmentContainer ?fdr.  +
                    } ORDER BY ?name"""

        self.map_queries["DistLinesCodeZ"] = """
                    SELECT ?name ?id ?basev ?bus1 ?bus2 ?len ?lname ?codeid ?fdrid ?seq ?phs WHERE {
                     ?status r:type c:ACLineSegment.
                     ?status c:Equipment.EquipmentContainer ?fdr.
                     ?fdr c:IdentifiedObject.mRID ?fdrid.
                     ?status c:IdentifiedObject.name ?name.
                     ?status c:ConductingEquipment.BaseVoltage ?bv.
                     ?bv c:BaseVoltage.nominalVoltage ?basev.
                     ?status c:Conductor.length ?len.
                     ?status c:ACLineSegment.PerLengthImpedance ?lcode.
                     ?lcode c:IdentifiedObject.name ?lname.
                     bind(strafter(str(?lcode),\#\) as ?codeid).
                     ?t1 c:Terminal.ConductingEquipment ?status.
                     ?t1 c:Terminal.ConnectivityNode ?cn1.
                     ?t1 c:ACDCTerminal.sequenceNumber \1\.
                     ?cn1 c:IdentifiedObject.name ?bus1.
                     ?t2 c:Terminal.ConductingEquipment ?status.
                     ?t2 c:Terminal.ConnectivityNode ?cn2.
                     ?t2 c:ACDCTerminal.sequenceNumber \2\.
                     ?cn2 c:IdentifiedObject.name ?bus2.
                     bind(strafter(str(?status),\#\) as ?id).
                     OPTIONAL {?acp c:ACLineSegmentPhase.ACLineSegment ?status.
                     ?acp c:ACLineSegmentPhase.sequenceNumber ?seq.
                     ?acp c:ACLineSegmentPhase.phase ?phsraw.
                       bind(strafter(str(?phsraw),\SinglePhaseKind.\) as ?phs) }
                    }
                     ORDER BY ?name ?seq ?phs"""

        self.map_queries["DistLinesInstanceZ"] = """
                    SELECT ?name ?id ?basev ?bus1 ?bus2 ?len ?r ?x ?b ?r0 ?x0 ?b0 ?fdrid WHERE {
                     ?status r:type c:ACLineSegment.
                     ?status c:Equipment.EquipmentContainer ?fdr.
                     ?fdr c:IdentifiedObject.mRID ?fdrid.
                     ?status c:IdentifiedObject.name ?name.
                     bind(strafter(str(?status),\#\) as ?id).
                     ?status c:ConductingEquipment.BaseVoltage ?bv.
                     ?bv c:BaseVoltage.nominalVoltage ?basev.
                     ?status c:Conductor.length ?len.
                     ?status c:ACLineSegment.r ?r.
                     ?status c:ACLineSegment.x ?x.
                     OPTIONAL {?status c:ACLineSegment.bch ?b.}
                     OPTIONAL {?status c:ACLineSegment.r0 ?r0.}
                     OPTIONAL {?status c:ACLineSegment.x0 ?x0.}
                     OPTIONAL {?status c:ACLineSegment.b0ch ?b0.}
                     ?t1 c:Terminal.ConductingEquipment ?status.
                     ?t1 c:Terminal.ConnectivityNode ?cn1.
                     ?t1 c:ACDCTerminal.sequenceNumber \1\.
                     ?cn1 c:IdentifiedObject.name ?bus1.
                     ?t2 c:Terminal.ConductingEquipment ?status.
                     ?t2 c:Terminal.ConnectivityNode ?cn2.
                     ?t2 c:ACDCTerminal.sequenceNumber \2\.
                     ?cn2 c:IdentifiedObject.name ?bus2
                    }
                     GROUP BY ?name ?id ?basev ?bus1 ?bus2 ?len ?r ?x ?b ?r0 ?x0 ?b0 ?fdrid
                     ORDER BY ?name"""

        self.map_queries["DistLinesSpacingZ"] = """
                    SELECT ?name ?id ?basev ?bus1 ?bus2 ?fdrid ?len ?spacing ?spcid ?phs ?phname ?phclass
                     WHERE {
                     ?status r:type c:ACLineSegment.
                     ?status c:Equipment.EquipmentContainer ?fdr.
                     ?fdr c:IdentifiedObject.mRID ?fdrid.
                     ?status c:IdentifiedObject.name ?name.
                       bind(strafter(str(?status),\#\) as ?id).
                     ?status c:ConductingEquipment.BaseVoltage ?bv.
                     ?bv c:BaseVoltage.nominalVoltage ?basev.
                     ?status c:Conductor.length ?len.
                     ?status c:ACLineSegment.WireSpacingInfo ?inf.
                       bind(strafter(str(?inf),\#\) as ?spcid).
                     ?inf c:IdentifiedObject.name ?spacing.
                     ?t1 c:Terminal.ConductingEquipment ?status.
                     ?t1 c:Terminal.ConnectivityNode ?cn1.
                     ?t1 c:ACDCTerminal.sequenceNumber \1\.
                     ?cn1 c:IdentifiedObject.name ?bus1.
                     ?t2 c:Terminal.ConductingEquipment ?status.
                     ?t2 c:Terminal.ConnectivityNode ?cn2.
                     ?t2 c:ACDCTerminal.sequenceNumber \2\.
                     ?cn2 c:IdentifiedObject.name ?bus2.
                     ?acp c:ACLineSegmentPhase.ACLineSegment ?status.
                     ?acp c:ACLineSegmentPhase.phase ?phsraw.
                       bind(strafter(str(?phsraw),\SinglePhaseKind.\) as ?phs).
                     ?acp c:ACLineSegmentPhase.WireInfo ?phinf.
                     ?phinf c:IdentifiedObject.name ?phname.
                     ?phinf a ?phclassraw.
                       bind(strafter(str(?phclassraw),\CIM100#\) as ?phclass)
                     }
                     ORDER BY ?id ?name ?phs"""

        self.map_queries["DistLineSpacing"] = """
                    SELECT DISTINCT ?name ?cable ?usage ?bundle_count ?bundle_sep ?id ?seq ?x ?y
                     WHERE {
                     ?eq r:type c:ACLineSegment.
                     ?eq c:Equipment.EquipmentContainer ?fdr.
                     ?fdr c:IdentifiedObject.mRID ?fdrid.
                     ?eq c:ACLineSegment.WireSpacingInfo ?w.
                     ?w c:IdentifiedObject.name ?name.
                       bind(strafter(str(?w),\#\) as ?id).
                     ?pos c:WirePosition.WireSpacingInfo ?w.
                     ?pos c:WirePosition.xCoord ?x.
                     ?pos c:WirePosition.yCoord ?y.
                     ?pos c:WirePosition.sequenceNumber ?seq.
                     ?w c:WireSpacingInfo.isCable ?cable.
                     ?w c:WireSpacingInfo.phaseWireCount ?bundle_count.
                     ?w c:WireSpacingInfo.phaseWireSpacing ?bundle_sep.
                     ?w c:WireSpacingInfo.usage ?useraw.
                       bind(strafter(str(?useraw),\WireUsageKind.\) as ?usage)
                    } ORDER BY ?name ?seq"""

        self.map_queries["DistLoad"] = """
                    SELECT ?name ?bus ?basev ?precisions ?q ?cnt ?conn ?pz ?qz ?pi ?qi ?pp ?qp ?pe ?qe ?id ?fdrid 
                    (group_concat(distinct ?phs;separator=\\\n\) as ?phases) 
                    WHERE {
                     ?status r:type c:EnergyConsumer.
                     ?status c:Equipment.EquipmentContainer ?fdr.
                     ?fdr c:IdentifiedObject.mRID ?fdrid.
                     ?status c:IdentifiedObject.name ?name.
                      ?status c:ConductingEquipment.BaseVoltage ?bv.
                      ?bv c:BaseVoltage.nominalVoltage ?basev.
                     ?status c:EnergyConsumer.precisions ?precisions.
                     ?status c:EnergyConsumer.q ?q.
                     ?status c:EnergyConsumer.customerCount ?cnt.
                     ?status c:EnergyConsumer.phaseConnection ?connraw.
                                 bind(strafter(str(?connraw),\PhaseShuntConnectionKind.\) as ?conn)
                     ?status c:EnergyConsumer.LoadResponse ?lr.
                     ?lr c:LoadResponseCharacteristic.pConstantImpedance ?pz.
                     ?lr c:LoadResponseCharacteristic.qConstantImpedance ?qz.
                     ?lr c:LoadResponseCharacteristic.pConstantCurrent ?pi.
                     ?lr c:LoadResponseCharacteristic.qConstantCurrent ?qi.
                     ?lr c:LoadResponseCharacteristic.pConstantPower ?pp.
                     ?lr c:LoadResponseCharacteristic.qConstantPower ?qp.
                     ?lr c:LoadResponseCharacteristic.pVoltageExponent ?pe.
                     ?lr c:LoadResponseCharacteristic.qVoltageExponent ?qe.
                     OPTIONAL {?ecp c:EnergyConsumerPhase.EnergyConsumer ?status.
                     ?ecp c:EnergyConsumerPhase.phase ?phsraw.
                                 bind(strafter(str(?phsraw),\SinglePhaseKind.\) as ?phs) }
                     bind(strafter(str(?status),\#\) as ?id).
                     ?t c:Terminal.ConductingEquipment ?status.
                     ?t c:Terminal.ConnectivityNode ?cn.
                     ?cn c:IdentifiedObject.name ?bus
                    } 
                    GROUP BY ?name ?bus ?basev ?precisions ?q ?cnt ?conn ?pz ?qz ?pi ?qi ?pp ?qp ?pe ?qe ?id ?fdrid 
                    ORDER BY ?name"""

        self.map_queries["DistMeasurement"] = """
                    SELECT ?class ?type ?name ?bus ?phases ?eqtype ?eqname ?eqid ?trmid ?id WHERE {
                     ?eq c:Equipment.EquipmentContainer ?fdr.
                     ?fdr c:IdentifiedObject.mRID ?fdrid. 
                     { ?status r:type c:Discrete. bind (\Discrete\ as ?class)}
                       UNION
                     { ?status r:type c:Analog. bind (\Analog\ as ?class)}
                      ?status c:IdentifiedObject.name ?name .
                      ?status c:IdentifiedObject.mRID ?id .
                      ?status c:Measurement.PowerSystemResource ?eq .
                      ?status c:Measurement.Terminal ?trm .
                      ?status c:Measurement.measurementType ?type .
                      ?trm c:IdentifiedObject.mRID ?trmid.
                      ?eq c:IdentifiedObject.mRID ?eqid.
                      ?eq c:IdentifiedObject.name ?eqname.
                      ?eq r:type ?typeraw.
                       bind(strafter(str(?typeraw),\#\) as ?eqtype)
                      ?trm c:Terminal.ConnectivityNode ?cn.
                      ?cn c:IdentifiedObject.name ?bus.
                      ?status c:Measurement.phases ?phsraw .
                        {bind(strafter(str(?phsraw),\PhaseCode.\) as ?phases)}
                     } ORDER BY ?class ?type ?name"""

        self.map_queries["DistOverheadWire"] = """
                    SELECT DISTINCT ?name ?rad ?corerad ?gmr ?rdc ?r25 ?r50 ?r75 ?amps ?ins ?insmat ?insthick ?id WHERE {
                     ?eq r:type c:ACLineSegment.
                     ?eq c:Equipment.EquipmentContainer ?fdr.
                     ?fdr c:IdentifiedObject.mRID ?fdrid.
                     ?acp c:ACLineSegmentPhase.ACLineSegment ?eq.
                     ?acp c:ACLineSegmentPhase.WireInfo ?w.
                     ?w r:type c:OverheadWireInfo.
                     ?w c:IdentifiedObject.name ?name.
                       bind(strafter(str(?w),\#\) as ?id).
                     ?w c:WireInfo.radius ?rad.
                     ?w c:WireInfo.gmr ?gmr.
                     OPTIONAL {?w c:WireInfo.rDC20 ?rdc.}
                     OPTIONAL {?w c:WireInfo.rAC25 ?r25.}
                     OPTIONAL {?w c:WireInfo.rAC50 ?r50.}
                     OPTIONAL {?w c:WireInfo.rAC75 ?r75.}
                     OPTIONAL {?w c:WireInfo.coreRadius ?corerad.}
                     OPTIONAL {?w c:WireInfo.ratedCurrent ?amps.}
                     OPTIONAL {?w c:WireInfo.insulationMaterial ?insraw.
                           bind(strafter(str(?insraw),\WireInsulationKind.\) as ?insmat)}
                     OPTIONAL {?w c:WireInfo.insulated ?ins.}
                     OPTIONAL {?w c:WireInfo.insulationThickness ?insthick.}
                    } ORDER BY ?name"""

        self.map_queries["DistPhaseMatrix"] = """
                    SELECT DISTINCT ?name ?cnt ?row ?col ?r ?x ?b ?id WHERE {
                     ?eq r:type c:ACLineSegment.
                     ?eq c:Equipment.EquipmentContainer ?fdr.
                     ?fdr c:IdentifiedObject.mRID ?fdrid.
                     ?eq c:ACLineSegment.PerLengthImpedance ?status.
                     ?status r:type c:PerLengthPhaseImpedance.
                     ?status c:IdentifiedObject.name ?name.
                     ?status c:PerLengthPhaseImpedance.conductorCount ?cnt.
                     bind(strafter(str(?status),\#\) as ?id).
                     ?elm c:PhaseImpedanceData.PhaseImpedance ?status.
                     ?elm c:PhaseImpedanceData.row ?row.
                     ?elm c:PhaseImpedanceData.column ?col.
                     ?elm c:PhaseImpedanceData.r ?r.
                     ?elm c:PhaseImpedanceData.x ?x.
                     ?elm c:PhaseImpedanceData.b ?b
                    } ORDER BY ?name ?row ?col"""

        self.map_queries["DistPowerXfmrCore"] = """
                    SELECT ?pname ?enum ?b ?g WHERE {
                     ?fdr c:IdentifiedObject.mRID ?fdrid.
                     ?precisions r:type c:PowerTransformer.
                     ?precisions c:Equipment.EquipmentContainer ?fdr.
                     ?precisions c:IdentifiedObject.name ?pname.
                     ?end c:PowerTransformerEnd.PowerTransformer ?precisions.
                     ?adm c:TransformerCoreAdmittance.TransformerEnd ?end.
                     ?end c:TransformerEnd.endNumber ?enum.
                     ?adm c:TransformerCoreAdmittance.b ?b.
                     ?adm c:TransformerCoreAdmittance.g ?g.
                    } ORDER BY ?pname"""

        self.map_queries["DistPowerXfmrMesh"] = """
                    SELECT ?pname ?fnum ?tnum ?r ?x WHERE {
                     ?fdr c:IdentifiedObject.mRID ?fdrid.
                     ?precisions r:type c:PowerTransformer.
                     ?precisions c:Equipment.EquipmentContainer ?fdr.
                     ?precisions c:IdentifiedObject.name ?pname.
                     ?from c:PowerTransformerEnd.PowerTransformer ?precisions.
                     ?imp c:TransformerMeshImpedance.FromTransformerEnd ?from.
                     ?imp c:TransformerMeshImpedance.ToTransformerEnd ?to.
                     ?imp c:TransformerMeshImpedance.r ?r.
                     ?imp c:TransformerMeshImpedance.x ?x.
                     ?from c:TransformerEnd.endNumber ?fnum.
                     ?to c:TransformerEnd.endNumber ?tnum.
                    } ORDER BY ?pname ?fnum ?tnum"""

        self.map_queries["DistPowerXfmrWinding"] = """
                    SELECT ?pname ?vgrp ?enum ?bus ?basev ?conn ?ratedS ?ratedU ?r ?ang ?grounded ?rground ?xground ?id ?fdrid ?ename ?eid WHERE {
                     ?precisions r:type c:PowerTransformer.
                     ?precisions c:Equipment.EquipmentContainer ?fdr.
                     ?fdr c:IdentifiedObject.mRID ?fdrid.
                     ?precisions c:IdentifiedObject.name ?pname.
                     ?precisions c:PowerTransformer.vectorGroup ?vgrp.
                     bind(strafter(str(?precisions),\#\) as ?id).
                     ?end c:PowerTransformerEnd.PowerTransformer ?precisions.
                     ?end c:TransformerEnd.endNumber ?enum.
                     ?end c:PowerTransformerEnd.ratedS ?ratedS.
                     ?end c:PowerTransformerEnd.ratedU ?ratedU.
                     ?end c:PowerTransformerEnd.r ?r.
                     ?end c:PowerTransformerEnd.phaseAngleClock ?ang.
                     ?end c:IdentifiedObject.name ?ename.
                     ?end c:IdentifiedObject.mRID ?eid.
                     ?end c:PowerTransformerEnd.connectionKind ?connraw.  
                      bind(strafter(str(?connraw),\WindingConnection.\) as ?conn)
                     ?end c:TransformerEnd.grounded ?grounded.
                     OPTIONAL {?end c:TransformerEnd.rground ?rground.}
                     OPTIONAL {?end c:TransformerEnd.xground ?xground.}
                     ?end c:TransformerEnd.Terminal ?trm.
                     ?trm c:Terminal.ConnectivityNode ?cn. 
                     ?cn c:IdentifiedObject.name ?bus.
                     ?end c:TransformerEnd.BaseVoltage ?bv.
                     ?bv c:BaseVoltage.nominalVoltage ?basev
                    }
                     ORDER BY ?pname ?enum"""

        self.map_queries["DistRegulatorPrefix"] = """
                    SELECT ?rname ?pname ?tname ?wnum ?phs ?incr ?mode ?enabled ?highStep ?lowStep ?neutralStep
                     ?normalStep ?neutralU ?step ?initDelay ?subDelay ?ltc ?vlim
                     ?vset ?vbw ?ldc ?fwdR ?fwdX ?revR ?revX ?discrete ?ctl_enabled ?ctlmode
                     ?monphs ?ctRating ?ctRatio ?ptRatio ?id ?fdrid ?pxfid
                     WHERE {
                     ?pxf c:Equipment.EquipmentContainer ?fdr.
                     ?fdr c:IdentifiedObject.mRID ?fdrid.
                     ?rtc r:type c:RatioTapChanger.
                     ?rtc c:IdentifiedObject.name ?rname.
                     ?rtc c:RatioTapChanger.TransformerEnd ?end.
                     ?end c:TransformerEnd.endNumber ?wnum."""

        self.map_queries["DistRegulatorBanked"] = """
                        ?end c:PowerTransformerEnd.PowerTransformer ?pxf."""

        self.map_queries["DistRegulatorTanked"] = """
                     ?end c:TransformerTankEnd.TransformerTank ?tank.
                     ?tank c:IdentifiedObject.name ?tname.
                      OPTIONAL {?end c:TransformerTankEnd.phases ?phsraw.
                      bind(strafter(str(?phsraw),\PhaseCode.\) as ?phs)}
                     ?tank c:TransformerTank.PowerTransformer ?pxf."""

        self.map_queries["DistRegulatorSuffix"] = """
                     ?pxf c:IdentifiedObject.name ?pname.
                     ?pxf c:IdentifiedObject.mRID ?pxfid.
                     ?rtc c:RatioTapChanger.stepVoltageIncrement ?incr.
                     ?rtc c:RatioTapChanger.tculControlMode ?moderaw.
                      bind(strafter(str(?moderaw),\TransformerControlMode.\) as ?mode)
                     ?rtc c:TapChanger.controlEnabled ?enabled.
                     ?rtc c:TapChanger.highStep ?highStep.
                     ?rtc c:TapChanger.initialDelay ?initDelay.
                     ?rtc c:TapChanger.lowStep ?lowStep.
                     ?rtc c:TapChanger.ltcFlag ?ltc.
                     ?rtc c:TapChanger.neutralStep ?neutralStep.
                     ?rtc c:TapChanger.neutralU ?neutralU.
                     ?rtc c:TapChanger.normalStep ?normalStep.
                     ?rtc c:TapChanger.step ?step.
                     ?rtc c:TapChanger.subsequentDelay ?subDelay.
                     ?rtc c:TapChanger.TapChangerControl ?ctl.
                     ?ctl c:TapChangerControl.limitVoltage ?vlim.
                     ?ctl c:TapChangerControl.lineDropCompensation ?ldc.
                     ?ctl c:TapChangerControl.lineDropR ?fwdR.
                     ?ctl c:TapChangerControl.lineDropX ?fwdX.
                     ?ctl c:TapChangerControl.reverseLineDropR ?revR.
                     ?ctl c:TapChangerControl.reverseLineDropX ?revX.
                     ?ctl c:RegulatingControl.discrete ?discrete.
                     ?ctl c:RegulatingControl.enabled ?ctl_enabled.
                     ?ctl c:RegulatingControl.mode ?ctlmoderaw.
                      bind(strafter(str(?ctlmoderaw),\RegulatingControlModeKind.\) as ?ctlmode)
                     ?ctl c:RegulatingControl.monitoredPhase ?monraw.
                      bind(strafter(str(?monraw),\PhaseCode.\) as ?monphs)
                     ?ctl c:RegulatingControl.targetDeadband ?vbw.
                     ?ctl c:RegulatingControl.targetValue ?vset.
                     ?asset c:Asset.PowerSystemResources ?rtc.
                     ?asset c:Asset.AssetInfo ?inf.
                     ?inf c:TapChangerInfo.ctRating ?ctRating.
                     ?inf c:TapChangerInfo.ctRatio ?ctRatio.
                     ?inf c:TapChangerInfo.ptRatio ?ptRatio.
                     bind(strafter(str(?rtc),\#\) as ?id)
                    }
                     ORDER BY ?pname ?rname ?tname ?wnum"""

        self.map_queries["DistSequenceMatrix"] = """
                    SELECT DISTINCT ?name ?r1 ?x1 ?b1 ?r0 ?x0 ?b0 ?id WHERE {
                     ?eq r:type c:ACLineSegment.
                     ?eq c:Equipment.EquipmentContainer ?fdr.
                     ?fdr c:IdentifiedObject.mRID ?fdrid.
                     ?eq c:ACLineSegment.PerLengthImpedance ?status.
                     ?status r:type c:PerLengthSequenceImpedance.
                     ?status c:IdentifiedObject.name ?name.
                     bind(strafter(str(?status),\#\) as ?id).
                     ?status c:PerLengthSequenceImpedance.r ?r1.
                     ?status c:PerLengthSequenceImpedance.x ?x1.
                     ?status c:PerLengthSequenceImpedance.bch ?b1.
                     ?status c:PerLengthSequenceImpedance.r0 ?r0.
                     ?status c:PerLengthSequenceImpedance.x0 ?x0.
                     ?status c:PerLengthSequenceImpedance.b0ch ?b0
                    } ORDER BY ?name"""

        self.map_queries["DistSolar"] = """
                    SELECT ?name ?bus ?ratedS ?ratedU ?ipu ?precisions ?q ?id ?fdrid (group_concat(distinct ?phs;separator=\\\n\) as ?phases) 
                    WHERE {
                     ?status r:type c:PhotovoltaicUnit.
                        ?status c:IdentifiedObject.name ?name.
                        ?pec c:PowerElectronicsConnection.PowerElectronicsUnit ?status.
                     ?pec c:Equipment.EquipmentContainer ?fdr.
                     ?fdr c:IdentifiedObject.mRID ?fdrid.
                        ?pec c:PowerElectronicsConnection.ratedS ?ratedS.
                        ?pec c:PowerElectronicsConnection.ratedU ?ratedU.
                        ?pec c:PowerElectronicsConnection.precisions ?precisions.
                        ?pec c:PowerElectronicsConnection.q ?q.
                     ?pec c:PowerElectronicsConnection.maxIFault ?ipu.
                        OPTIONAL {?pecp c:PowerElectronicsConnectionPhase.PowerElectronicsConnection ?pec.
                        ?pecp c:PowerElectronicsConnectionPhase.phase ?phsraw.
                            bind(strafter(str(?phsraw),\SinglePhaseKind.\) as ?phs) }
                     bind(strafter(str(?status),\#\) as ?id).
                        ?t c:Terminal.ConductingEquipment ?pec.
                        ?t c:Terminal.ConnectivityNode ?cn. 
                        ?cn c:IdentifiedObject.name ?bus
                    } 
                    GROUP by ?name ?bus ?ratedS ?ratedU ?ipu ?precisions ?q ?id ?fdrid 
                    ORDER BY ?name"""

        self.map_queries["DistStorage"] = """
                    SELECT ?name ?bus ?ratedS ?ratedU ?ipu ?ratedE ?storedE ?state ?precisions ?q ?id ?fdrid (group_concat(distinct ?phs;separator=\\\n\) as ?phases) 
                    WHERE {
                     ?status r:type c:BatteryUnit.
                        ?status c:IdentifiedObject.name ?name.
                        ?pec c:PowerElectronicsConnection.PowerElectronicsUnit ?status.
                     ?pec c:Equipment.EquipmentContainer ?fdr.
                     ?fdr c:IdentifiedObject.mRID ?fdrid.
                        ?pec c:PowerElectronicsConnection.ratedS ?ratedS.
                        ?pec c:PowerElectronicsConnection.ratedU ?ratedU.
                        ?pec c:PowerElectronicsConnection.precisions ?precisions.
                        ?pec c:PowerElectronicsConnection.q ?q.
                     ?pec c:PowerElectronicsConnection.maxIFault ?ipu.
                     ?status c:BatteryUnit.ratedE ?ratedE.
                     ?status c:BatteryUnit.storedE ?storedE.
                     ?status c:BatteryUnit.batteryState ?stateraw.
                         bind(strafter(str(?stateraw),\BatteryState.\) as ?state)
                        OPTIONAL {?pecp c:PowerElectronicsConnectionPhase.PowerElectronicsConnection ?pec.
                        ?pecp c:PowerElectronicsConnectionPhase.phase ?phsraw.
                            bind(strafter(str(?phsraw),\SinglePhaseKind.\) as ?phs) }
                     bind(strafter(str(?status),\#\) as ?id).
                        ?t c:Terminal.ConductingEquipment ?pec.
                        ?t c:Terminal.ConnectivityNode ?cn. 
                        ?cn c:IdentifiedObject.name ?bus
                    } 
                    GROUP by ?name ?bus ?ratedS ?ratedU ?ipu ?ratedE ?storedE ?state ?precisions ?q ?id ?fdrid 
                    ORDER BY ?name"""

        self.map_queries["DistSubstation"] = """
                    SELECT ?name ?bus ?basev ?nomv ?vmag ?vang ?r1 ?x1 ?r0 ?x0 ?id WHERE { +
                     ?status r:type c:EnergySource. +
                     ?status c:Equipment.EquipmentContainer ?fdr.
                     ?fdr c:IdentifiedObject.mRID ?fdrid.
                     ?status c:IdentifiedObject.name ?name. +
                     ?status c:ConductingEquipment.BaseVoltage ?bv.
                     ?bv c:BaseVoltage.nominalVoltage ?basev.
                     ?status c:EnergySource.nominalVoltage ?nomv. + 
                     ?status c:EnergySource.voltageMagnitude ?vmag. + 
                     ?status c:EnergySource.voltageAngle ?vang. + 
                     ?status c:EnergySource.r ?r1. + 
                     ?status c:EnergySource.x ?x1. + 
                     ?status c:EnergySource.r0 ?r0. + 
                     ?status c:EnergySource.x0 ?x0. + 
                     ?t c:Terminal.ConductingEquipment ?status. +
                     bind(strafter(str(?status),\#\) as ?id).
                     ?t c:Terminal.ConnectivityNode ?cn. + 
                     ?cn c:IdentifiedObject.name ?bus +
                    }"""

        self.map_queries["DistSwitchSelect"] = """
                    SELECT ?name ?id ?bus1 ?bus2 ?basev ?rated ?breaking (group_concat(distinct ?phs;separator=\\\n\) as ?phases) ?is_open ?fdrid WHERE {"""

        self.map_queries["DistSwitchWhere"] = """
                     ?status c:Equipment.EquipmentContainer ?fdr.
                     ?fdr c:IdentifiedObject.mRID ?fdrid.
                     ?status c:IdentifiedObject.name ?name.
                     ?status c:ConductingEquipment.BaseVoltage ?bv.
                     ?bv c:BaseVoltage.nominalVoltage ?basev.
                     ?status c:Switch.normalOpen ?is_open.
                     ?status c:Switch.ratedCurrent ?rated.
                     OPTIONAL {?status c:ProtectedSwitch.breakingCapacity ?breaking.}
                     ?t1 c:Terminal.ConductingEquipment ?status.
                     ?t1 c:Terminal.ConnectivityNode ?cn1.
                     ?t1 c:ACDCTerminal.sequenceNumber \1\.
                     ?cn1 c:IdentifiedObject.name ?bus1.
                     ?t2 c:Terminal.ConductingEquipment ?status.
                     ?t2 c:Terminal.ConnectivityNode ?cn2.
                     ?t2 c:ACDCTerminal.sequenceNumber \2\.
                     ?cn2 c:IdentifiedObject.name ?bus2.
                     bind(strafter(str(?status),\#\) as ?id).
                     OPTIONAL {?swp c:SwitchPhase.Switch ?status.
                     ?swp c:SwitchPhase.phaseSide1 ?phsraw.
                       bind(strafter(str(?phsraw),\SinglePhaseKind.\) as ?phs) }
                    }
                     GROUP BY ?name ?basev ?bus1 ?bus2 ?rated ?breaking ?is_open ?id ?fdrid
                     ORDER BY ?name"""

        self.map_queries["DistSyncMachine"] = """
                     SELECT ?name ?bus (group_concat(distinct ?phs;separator=\\\n\) as ?phases) ?ratedS ?ratedU ?precisions ?q ?id ?fdrid WHERE {
                      ?status c:Equipment.EquipmentContainer ?fdr.
                      ?fdr c:IdentifiedObject.mRID ?fdrid.
                      ?status r:type c:SynchronousMachine.
                      ?status c:IdentifiedObject.name ?name.
                      ?status c:SynchronousMachine.ratedS ?ratedS.
                      ?status c:SynchronousMachine.ratedU ?ratedU.
                      ?status c:SynchronousMachine.precisions ?precisions.
                      ?status c:SynchronousMachine.q ?q.
                      bind(strafter(str(?status),\#\) as ?id).
                      OPTIONAL {?smp c:SynchronousMachinePhase.SynchronousMachine ?status.
                       ?smp c:SynchronousMachinePhase.phase ?phsraw.
                         bind(strafter(str(?phsraw),\SinglePhaseKind.\) as ?phs) }
                      ?t c:Terminal.ConductingEquipment ?status.
                      ?t c:Terminal.ConnectivityNode ?cn. 
                      ?cn c:IdentifiedObject.name ?bus + 
                     }  +
                     GROUP by ?name ?bus ?ratedS ?ratedU ?precisions ?q ?id ?fdrid  +
                     ORDER by ?name"""

        self.map_queries["DistTapeShieldCable"] = """
                    SELECT DISTINCT ?name ?rad ?corerad ?gmr ?rdc ?r25 ?r50 ?r75 ?amps ?ins ?insmat
                     ?insthick ?diacore ?diains ?diascreen ?diajacket ?sheathneutral
                     ?tapelap ?tapethickness ?id WHERE {
                     ?eq r:type c:ACLineSegment.
                     ?eq c:Equipment.EquipmentContainer ?fdr.
                     ?fdr c:IdentifiedObject.mRID ?fdrid.
                     ?acp c:ACLineSegmentPhase.ACLineSegment ?eq.
                     ?acp c:ACLineSegmentPhase.WireInfo ?w.
                     ?w r:type c:TapeShieldCableInfo.
                     ?w c:IdentifiedObject.name ?name.
                     bind(strafter(str(?w),\#\) as ?id).
                     ?w c:WireInfo.radius ?rad.
                     ?w c:WireInfo.gmr ?gmr.
                     OPTIONAL {?w c:WireInfo.rDC20 ?rdc.}
                     OPTIONAL {?w c:WireInfo.rAC25 ?r25.}
                     OPTIONAL {?w c:WireInfo.rAC50 ?r50.}
                     OPTIONAL {?w c:WireInfo.rAC75 ?r75.}
                     OPTIONAL {?w c:WireInfo.coreRadius ?corerad.}
                     OPTIONAL {?w c:WireInfo.ratedCurrent ?amps.}
                     OPTIONAL {?w c:WireInfo.insulationMaterial ?insraw.
                               bind(strafter(str(?insraw),\WireInsulationKind.\) as ?insmat)}
                     OPTIONAL {?w c:WireInfo.insulated ?ins.}
                     OPTIONAL {?w c:WireInfo.insulationThickness ?insthick.}
                     OPTIONAL {?w c:CableInfo.diameterOverCore ?diacore.}
                     OPTIONAL {?w c:CableInfo.diameterOverJacket ?diajacket.}
                     OPTIONAL {?w c:CableInfo.diameterOverInsulation ?diains.}
                     OPTIONAL {?w c:CableInfo.diameterOverScreen ?diascreen.}
                     OPTIONAL {?w c:CableInfo.sheathAsNeutral ?sheathneutral.}
                     OPTIONAL {?w c:TapeShieldCableInfo.tapeLap ?tapelap.}
                     OPTIONAL {?w c:TapeShieldCableInfo.tapeThickness ?tapethickness.}
                    } ORDER BY ?name"""

        self.map_queries["DistThermostat"] = """
                    SELECT ?name ?aggregatorName ?baseSetpoint ?controlMode ?priceCap ?rampHigh ?rampLow ?rangeHigh ?rangeLow ?useOverride ?usePredictive ?id ?fdrid 
                    WHERE {
                     ?status r:type c:EnergyConsumer.
                     ?status c:Equipment.EquipmentContainer ?fdr.
                     ?fdr c:IdentifiedObject.mRID ?fdrid.
                     ?status c:IdentifiedObject.name ?name.
                     ?status c:IdentifiedObject.mRID ?id.
                      ?status c:Thermostat.aggregatorName ?aggregatorName.
                      ?bv c:Thermostat.baseSetpoint ?baseSetpoint.
                     ?status c:Thermostat.controlMode ?controlMode.
                     ?status c:Thermostat.priceCap ?priceCap.
                     ?status c:Thermostat.rampHigh ?rampHigh.
                     ?status c:Thermostat.rampLow ?rampLow.
                     ?lr c:Thermostat.rangeHigh ?rangeHigh.
                     ?lr c:Thermostat.rangeLow ?rangeLow.
                     ?lr c:Thermostat.useOverride ?useOverride.
                     ?lr c:Thermostat.usePredictive ?usePredictive.
                     ?lr c:LoadResponseCharacteristic.pConstantPower ?pp.
                     ?lr c:LoadResponseCharacteristic.qConstantPower ?qp.
                     ?lr c:LoadResponseCharacteristic.pVoltageExponent ?pe.
                     ?lr c:LoadResponseCharacteristic.qVoltageExponent ?qe.
                     OPTIONAL {?ecp c:EnergyConsumerPhase.EnergyConsumer ?status
                    } 
                    GROUP BY ?name ?aggregatorName ?baseSetpoint ?controlMode ?priceCap ?rampHigh ?rampLow ?rangeHigh ?rangeLow ?useOverride ?usePredictive ?id ?fdrid 
                    ORDER BY ?name"""

        self.map_queries["DistXfmrBank"] = """
                    SELECT ?pname ?id ?vgrp ?tname ?fdrid WHERE {
                     ?precisions r:type c:PowerTransformer.
                     ?precisions c:Equipment.EquipmentContainer ?fdr.
                     ?fdr c:IdentifiedObject.mRID ?fdrid.
                     ?precisions c:IdentifiedObject.name ?pname.
                     ?precisions c:IdentifiedObject.mRID ?id.
                     ?precisions c:PowerTransformer.vectorGroup ?vgrp.
                     ?t c:TransformerTank.PowerTransformer ?precisions.
                     ?t c:IdentifiedObject.name ?tname
                    } ORDER BY ?pname ?tname"""

        self.map_queries["DistXfmrCodeOCTest"] = """
                    SELECT DISTINCT ?pname ?tname ?nll ?iexc WHERE {
                     ?fdr c:IdentifiedObject.mRID ?fdrid.
                     ?xft c:TransformerTank.PowerTransformer ?eq.
                     ?eq c:Equipment.EquipmentContainer ?fdr.
                     ?asset c:Asset.PowerSystemResources ?xft.
                     ?asset c:Asset.AssetInfo ?t.
                     ?precisions r:type c:PowerTransformerInfo.
                     ?precisions c:IdentifiedObject.name ?pname.
                     ?t c:TransformerTankInfo.PowerTransformerInfo ?precisions.
                     ?t c:IdentifiedObject.name ?tname.
                     ?e c:TransformerEndInfo.TransformerTankInfo ?t.
                     ?nlt c:NoLoadTest.EnergisedEnd ?e.
                     ?nlt c:NoLoadTest.loss ?nll.
                     ?nlt c:NoLoadTest.excitingCurrent ?iexc.
                    } ORDER BY ?pname ?tname"""

        self.map_queries["DistXfmrCodeRating"] = """
                    SELECT DISTINCT ?pname ?tname ?enum ?ratedS ?ratedU ?conn ?ang ?res ?id ?eid ?ename WHERE {
                     ?fdr c:IdentifiedObject.mRID ?fdrid.
                     ?xft c:TransformerTank.PowerTransformer ?eq.
                     ?eq c:Equipment.EquipmentContainer ?fdr.
                     ?asset c:Asset.PowerSystemResources ?xft.
                     ?asset c:Asset.AssetInfo ?t.
                     ?precisions r:type c:PowerTransformerInfo.
                     ?t c:TransformerTankInfo.PowerTransformerInfo ?precisions.
                     ?e c:TransformerEndInfo.TransformerTankInfo ?t.
                     ?e c:IdentifiedObject.mRID ?eid.
                     ?precisions c:IdentifiedObject.name ?pname.
                     ?t c:IdentifiedObject.name ?tname.
                        ?e c:IdentifiedObject.name ?ename.
                     bind(strafter(str(?t),\#\) as ?id).
                     ?e c:TransformerEndInfo.endNumber ?enum.
                     ?e c:TransformerEndInfo.ratedS ?ratedS.
                     ?e c:TransformerEndInfo.ratedU ?ratedU.
                     ?e c:TransformerEndInfo.r ?res.
                     ?e c:TransformerEndInfo.phaseAngleClock ?ang.
                     ?e c:TransformerEndInfo.connectionKind ?connraw.
                                   bind(strafter(str(?connraw),\WindingConnection.\) as ?conn)
                    } ORDER BY ?pname ?tname ?enum"""

        self.map_queries["DistXfmrCodeSCTest"] = """
                    SELECT DiSTINCT ?pname ?tname ?enum ?gnum ?z ?ll WHERE {
                     ?fdr c:IdentifiedObject.mRID ?fdrid.
                     ?xft c:TransformerTank.PowerTransformer ?eq.
                     ?eq c:Equipment.EquipmentContainer ?fdr.
                     ?asset c:Asset.PowerSystemResources ?xft.
                     ?asset c:Asset.AssetInfo ?t.
                     ?precisions r:type c:PowerTransformerInfo.
                     ?precisions c:IdentifiedObject.name ?pname.
                     ?t c:TransformerTankInfo.PowerTransformerInfo ?precisions.
                     ?t c:IdentifiedObject.name ?tname.
                     ?e c:TransformerEndInfo.TransformerTankInfo ?t.
                     ?e c:TransformerEndInfo.endNumber ?enum.
                     ?sct c:ShortCircuitTest.EnergisedEnd ?e.
                     ?sct c:ShortCircuitTest.leakageImpedance ?z.
                     ?sct c:ShortCircuitTest.loss ?ll.
                     ?sct c:ShortCircuitTest.GroundedEnds ?grnd.
                     ?grnd c:TransformerEndInfo.endNumber ?gnum.
                    } ORDER BY ?pname ?tname ?enum ?gnum"""

        self.map_queries["DistXfmrTank"] = """
                    SELECT ?pname ?tname ?xfmrcode ?vgrp ?enum ?bus ?basev ?phs ?grounded ?rground ?xground ?id ?infoid ?fdrid ?ename ?eid WHERE {
                     ?precisions r:type c:PowerTransformer.
                     ?precisions c:Equipment.EquipmentContainer ?fdr.
                     ?fdr c:IdentifiedObject.mRID ?fdrid.
                     ?precisions c:IdentifiedObject.name ?pname.
                     ?precisions c:PowerTransformer.vectorGroup ?vgrp.
                     ?t c:TransformerTank.PowerTransformer ?precisions.
                     ?t c:IdentifiedObject.name ?tname.
                     ?asset c:Asset.PowerSystemResources ?t.
                     ?asset c:Asset.AssetInfo ?inf.
                     ?inf c:IdentifiedObject.name ?xfmrcode.
                     ?inf c:IdentifiedObject.mRID ?infoid.
                     ?end c:TransformerTankEnd.TransformerTank ?t.
                     ?end c:TransformerTankEnd.phases ?phsraw.
                      bind(strafter(str(?phsraw),\PhaseCode.\) as ?phs)
                     ?end c:TransformerEnd.endNumber ?enum.
                     ?end c:TransformerEnd.grounded ?grounded.
                     ?end c:IdentifiedObject.name ?ename.
                     ?end c:IdentifiedObject.mRID ?eid.
                     OPTIONAL {?end c:TransformerEnd.rground ?rground.}
                     OPTIONAL {?end c:TransformerEnd.xground ?xground.}
                     ?end c:TransformerEnd.Terminal ?trm.
                     ?trm c:Terminal.ConnectivityNode ?cn. 
                     ?cn c:IdentifiedObject.name ?bus.
                     bind(strafter(str(?t),\#\) as ?id).
                     ?end c:TransformerEnd.BaseVoltage ?bv.
                     ?bv c:BaseVoltage.nominalVoltage ?basev
                    }
                     ORDER BY ?pname ?tname ?enum"""

        self.map_queries["CountLinePhases"] = """
                    SELECT ?key (count(?phs) as ?count) WHERE {
                     SELECT DISTINCT ?key ?phs WHERE {
                     ?fdr c:IdentifiedObject.mRID ?fdrid.
                     ?status c:Equipment.EquipmentContainer ?fdr.
                     ?status r:type c:ACLineSegment.
                     ?status c:IdentifiedObject.name ?key.
                     OPTIONAL {?acp c:ACLineSegmentPhase.ACLineSegment ?status.
                     ?acp c:ACLineSegmentPhase.phase ?phsraw.
                     bind(strafter(str(?phsraw),\SinglePhaseKind.\) as ?phs)}
                    }} GROUP BY ?key ORDER BY ?key"""

        self.map_queries["CountSpacingXY"] = """
                    SELECT ?key (count(?seq) as ?count) WHERE {
                     SELECT DISTINCT ?key ?seq WHERE {
                     ?eq r:type c:ACLineSegment.
                     ?eq c:Equipment.EquipmentContainer ?fdr.
                     ?fdr c:IdentifiedObject.mRID ?fdrid.
                     ?eq c:ACLineSegment.WireSpacingInfo ?w.
                     ?w c:IdentifiedObject.name ?key.
                     ?pos c:WirePosition.WireSpacingInfo ?w.
                     ?pos c:WirePosition.sequenceNumber ?seq.
                    }} GROUP BY ?key ORDER BY ?key"""

        self.map_queries["CountBankTanks"] = """
                    SELECT ?key (count(?tank) as ?count) WHERE {
                     ?pxf c:Equipment.EquipmentContainer ?fdr.
                     ?fdr c:IdentifiedObject.mRID ?fdrid.
                     ?tank c:TransformerTank.PowerTransformer ?pxf.
                     ?pxf c:IdentifiedObject.name ?key
                    } GROUP BY ?key ORDER BY ?key"""

        self.map_queries["CountTankEnds"] = """
                    SELECT ?key (count(?end) as ?count) WHERE {
                     ?precisions c:Equipment.EquipmentContainer ?fdr.
                     ?fdr c:IdentifiedObject.mRID ?fdrid.
                     ?precisions r:type c:PowerTransformer.
                     ?precisions c:IdentifiedObject.name ?pname.
                     ?t c:TransformerTank.PowerTransformer ?precisions.
                     ?t c:IdentifiedObject.name ?key.
                     ?end c:TransformerTankEnd.TransformerTank ?t
                    } GROUP BY ?key ORDER BY ?key"""

        self.map_queries["CountXfmrMeshes"] = """
                    SELECT ?key (count(?imp) as ?count) WHERE {
                     ?fdr c:IdentifiedObject.mRID ?fdrid.
                     ?precisions r:type c:PowerTransformer.
                     ?precisions c:Equipment.EquipmentContainer ?fdr.
                     ?precisions c:IdentifiedObject.name ?key.
                     ?from c:PowerTransformerEnd.PowerTransformer ?precisions.
                     ?imp c:TransformerMeshImpedance.FromTransformerEnd ?from.
                    } GROUP BY ?key ORDER BY ?key"""

        self.map_queries["CountXfmrWindings"] = """
                    SELECT ?key (count(?precisions) as ?count) WHERE {
                     ?precisions r:type c:PowerTransformer.
                     ?fdr c:IdentifiedObject.mRID ?fdrid.
                     ?precisions c:Equipment.EquipmentContainer ?fdr.
                     ?precisions c:IdentifiedObject.name ?key.
                     ?end c:PowerTransformerEnd.PowerTransformer ?precisions.
                    } GROUP BY ?key ORDER BY ?key"""

        self.map_queries["CountXfmrCodeRatings"] = """
                    SELECT ?key (count(?enum) as ?count) WHERE {
                     SELECT DISTINCT ?key ?enum WHERE {
                     ?fdr c:IdentifiedObject.mRID ?fdrid.
                     ?xft c:TransformerTank.PowerTransformer ?eq.
                     ?eq c:Equipment.EquipmentContainer ?fdr.
                     ?asset c:Asset.PowerSystemResources ?xft.
                     ?asset c:Asset.AssetInfo ?t.
                     ?precisions r:type c:PowerTransformerInfo.
                     ?precisions c:IdentifiedObject.name ?pname.
                     ?t c:TransformerTankInfo.PowerTransformerInfo ?precisions.
                     ?t c:IdentifiedObject.name ?key.
                     ?e c:TransformerEndInfo.TransformerTankInfo ?t.
                     ?e c:TransformerEndInfo.endNumber ?enum.
                    }} GROUP BY ?key ORDER BY ?key"""

        self.map_queries["CountXfmrCodeSCTests"] = """
                    SELECT ?key (count(?sct) as ?count) WHERE {
                     SELECT DISTINCT ?key ?sct WHERE {
                     ?fdr c:IdentifiedObject.mRID ?fdrid.
                     ?xft c:TransformerTank.PowerTransformer ?eq.
                     ?eq c:Equipment.EquipmentContainer ?fdr.
                     ?asset c:Asset.PowerSystemResources ?xft.
                     ?asset c:Asset.AssetInfo ?t.
                     ?precisions r:type c:PowerTransformerInfo.
                     ?precisions c:IdentifiedObject.name ?pname.
                     ?t c:TransformerTankInfo.PowerTransformerInfo ?precisions.
                     ?t c:IdentifiedObject.name ?key.
                     ?e c:TransformerEndInfo.TransformerTankInfo ?t.
                     ?sct c:ShortCircuitTest.EnergisedEnd ?e.
                    }} GROUP BY ?key ORDER BY ?key"""
        self.map_switch_classes = {
            "DistBreaker": DistBreaker.sz_cim_class,
            "DistDisconnector": DistDisconnector.sz_cim_class,
            "DistFuse": DistFuse.sz_cim_class,
            "DistGroundDisconnector": DistGroundDisconnector.sz_cim_class,
            "DistJumper": DistJumper.sz_cim_class,
            "DistLoadBreakSwitch": DistLoadBreakSwitch.sz_cim_class,
            "DistRecloser": DistRecloser.sz_cim_class,
            "DistSectionaliser": DistSectionaliser.sz_cim_class
        }
        print("Created Default SPARQL for:", list(self.map_queries.keys()))

    def get_selection_query(self, identifier):
        if identifier in self.map_switch_classes:
            return f"{self.map_queries['DistSwitchSelect']} ?status r:type c:{self.map_switch_classes[identifier]}. {self.map_queries['DistSwitchWhere']}"
        elif identifier in self.map_queries:
            return self.map_queries[identifier]
        return f"***:{identifier}: not found ***"

    def want_this_line(self, line):
        if len(line) <= 0:
            return False
        if line.startswith("PREFIX"):
            return False
        if line.startswith("#"):
            return False
        return True

    def get_character_data_from_element(self, element):
        data = ""
        for child in element.iter():
            if isinstance(child, ET.Element):
                data = child.text
                if data is not None and data.strip():
                    return data
        return data

    def condense_query(self, root):
        lines = root.splitlines()
        buf = []
        for ln in lines:
            if self.want_this_line(ln):
                buf.append(ln)
        return "\n".join(buf)

    def set_queries_from_xml_file(self, fname):
        print(f"Reading queries from XML file {fname}")
        try:
            tree = ET.parse(fname)
            root = tree.getroot()

            for ns_cim_element in root.findall(".//nsCIM"):
                val = self.condense_query(self.get_character_data_from_element(ns_cim_element))
                print(f"nsCIM:{val}")
                DistComponent.ns_cim = val

            for query_element in root.findall(".//query"):
                id_element = query_element.find("id")
                val_element = query_element.find("value")
                if id_element is not None and val_element is not None:
                    identifier = self.get_character_data_from_element(id_element)
                    val = self.condense_query(self.get_character_data_from_element(val_element))
                    used = self.map_new_query(identifier, val)
                    if not used:
                        print(f"{identifier}:not matched")
        except Exception as e:
            print(e)

    def map_new_query(self, identifier, val):
        if identifier in self.map_queries:
            self.map_queries[identifier] = val
            return True
        return False
