from SPARQLWrapper import SPARQLWrapper2
import sys
import re
import uuid
import os.path
import CIMHubConfig

#prefix_template = """PREFIX r: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
#PREFIX c: <{cimURL}>
#PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
#"""

drop_loc_template = """DELETE {{
 ?multiplicities a ?class.
 ?multiplicities c:IdentifiedObject.mRID ?uuid.
 ?multiplicities c:IdentifiedObject.name ?name.
 ?multiplicities c:Location.CoordinateSystem ?crs.
}} WHERE {{
 VALUES ?uuid {{\"{res}\"}}
 VALUES ?class {{c:Location}}
 ?multiplicities a ?class.
 ?multiplicities c:IdentifiedObject.mRID ?uuid.
 ?multiplicities c:IdentifiedObject.name ?name.
 ?multiplicities c:Location.CoordinateSystem ?crs.
}}
"""

drop_trm_template = """DELETE {{
 ?multiplicities a ?class.
 ?multiplicities c:IdentifiedObject.mRID ?uuid.
 ?multiplicities c:IdentifiedObject.name ?name.
 ?multiplicities c:Terminal.ConductingEquipment ?eq.
 ?multiplicities c:ACDCTerminal.sequenceNumber ?seq.
 ?multiplicities c:Terminal.ConnectivityNode ?cn.
}} WHERE {{
 VALUES ?uuid {{\"{res}\"}}
 VALUES ?class {{c:Terminal}}
 ?multiplicities a ?class.
 ?multiplicities c:IdentifiedObject.mRID ?uuid.
 ?multiplicities c:IdentifiedObject.name ?name.
 ?multiplicities c:Terminal.ConductingEquipment ?eq.
 ?multiplicities c:ACDCTerminal.sequenceNumber ?seq.
 ?multiplicities c:Terminal.ConnectivityNode ?cn.
}}
"""

drop_pec_template = """DELETE {{
 ?multiplicities a ?class.
 ?multiplicities c:IdentifiedObject.mRID ?uuid.
 ?multiplicities c:IdentifiedObject.name ?name.
 ?multiplicities c:Equipment.EquipmentContainer ?fdr.
 ?multiplicities c:PowerElectronicsConnection.PowerElectronicsUnit ?unit.
 ?multiplicities c:PowerSystemResource.Location ?loc.
 ?multiplicities c:PowerElectronicsConnection.maxIFault ?flt.
 ?multiplicities c:PowerElectronicsConnection.precisions ?precisions.
 ?multiplicities c:PowerElectronicsConnection.q ?q.
 ?multiplicities c:PowerElectronicsConnection.ratedS ?S.
 ?multiplicities c:PowerElectronicsConnection.ratedU ?U.
}} WHERE {{
 VALUES ?uuid {{\"{res}\"}}
 VALUES ?class {{c:PowerElectronicsConnection}}
 ?multiplicities a ?class.
 ?multiplicities c:IdentifiedObject.mRID ?uuid.
 ?multiplicities c:IdentifiedObject.name ?name.
 ?multiplicities c:Equipment.EquipmentContainer ?fdr.
 ?multiplicities c:PowerElectronicsConnection.PowerElectronicsUnit ?unit.
 ?multiplicities c:PowerSystemResource.Location ?loc.
 ?multiplicities c:PowerElectronicsConnection.maxIFault ?flt.
 ?multiplicities c:PowerElectronicsConnection.precisions ?precisions.
 ?multiplicities c:PowerElectronicsConnection.q ?q.
 ?multiplicities c:PowerElectronicsConnection.ratedS ?S.
 ?multiplicities c:PowerElectronicsConnection.ratedU ?U.
}}
"""

drop_syn_template = """DELETE {{
 ?multiplicities a ?class.
 ?multiplicities c:IdentifiedObject.mRID ?uuid.
 ?multiplicities c:IdentifiedObject.name ?name.
 ?multiplicities c:Equipment.EquipmentContainer ?fdr.
 ?multiplicities c:PowerSystemResource.Location ?loc.
 ?multiplicities c:SynchronousMachine.precisions ?precisions.
 ?multiplicities c:SynchronousMachine.q ?q.
 ?multiplicities c:SynchronousMachine.ratedS ?S.
 ?multiplicities c:SynchronousMachine.ratedU ?U.
}} WHERE {{
 VALUES ?uuid {{\"{res}\"}}
 VALUES ?class {{c:SynchronousMachine}}
 ?multiplicities a ?class.
 ?multiplicities c:IdentifiedObject.mRID ?uuid.
 ?multiplicities c:IdentifiedObject.name ?name.
 ?multiplicities c:Equipment.EquipmentContainer ?fdr.
 ?multiplicities c:PowerSystemResource.Location ?loc.
 ?multiplicities c:SynchronousMachine.precisions ?precisions.
 ?multiplicities c:SynchronousMachine.q ?q.
 ?multiplicities c:SynchronousMachine.ratedS ?S.
 ?multiplicities c:SynchronousMachine.ratedU ?U.
}}
"""

drop_pep_template = """DELETE {{
 ?multiplicities a ?class.
 ?multiplicities c:IdentifiedObject.mRID ?uuid.
 ?multiplicities c:IdentifiedObject.name ?name.
 ?multiplicities c:PowerElectronicsConnectionPhase.phase ?phs.
 ?multiplicities c:PowerElectronicsConnectionPhase.PowerElectronicsConnection ?pec.
 ?multiplicities c:PowerElectronicsConnectionPhase.precisions ?precisions.
 ?multiplicities c:PowerElectronicsConnectionPhase.q ?q.
 ?multiplicities c:PowerSystemResource.Location ?loc.
}} WHERE {{
 VALUES ?uuid {{\"{res}\"}}
 VALUES ?class {{c:PowerElectronicsConnectionPhase}}
 ?multiplicities a ?class.
 ?multiplicities c:IdentifiedObject.mRID ?uuid.
 ?multiplicities c:IdentifiedObject.name ?name.
 ?multiplicities c:PowerElectronicsConnectionPhase.phase ?phs.
 ?multiplicities c:PowerElectronicsConnectionPhase.PowerElectronicsConnection ?pec.
 ?multiplicities c:PowerElectronicsConnectionPhase.precisions ?precisions.
 ?multiplicities c:PowerElectronicsConnectionPhase.q ?q.
 ?multiplicities c:PowerSystemResource.Location ?loc.
}}
"""

drop_pv_template = """DELETE {{
 ?multiplicities a ?class.
 ?multiplicities c:IdentifiedObject.mRID ?uuid.
 ?multiplicities c:IdentifiedObject.name ?name.
 ?multiplicities c:PowerSystemResource.Location ?loc.
}} WHERE {{
 VALUES ?uuid {{\"{res}\"}}
 VALUES ?class {{c:PhotovoltaicUnit}}
 ?multiplicities a ?class.
 ?multiplicities c:IdentifiedObject.mRID ?uuid.
 ?multiplicities c:IdentifiedObject.name ?name.
 ?multiplicities c:PowerSystemResource.Location ?loc.
}}
"""

drop_bat_template = """DELETE {{
 ?multiplicities a ?class.
 ?multiplicities c:IdentifiedObject.mRID ?uuid.
 ?multiplicities c:IdentifiedObject.name ?name.
 ?multiplicities c:BatteryUnit.ratedE ?rated.
 ?multiplicities c:BatteryUnit.storedE ?stored.
 ?multiplicities c:BatteryUnit.batteryState ?state.
 ?multiplicities c:PowerSystemResource.Location ?loc.
}} WHERE {{
 VALUES ?uuid {{\"{res}\"}}
 VALUES ?class {{c:BatteryUnit}}
 ?multiplicities a ?class.
 ?multiplicities c:IdentifiedObject.mRID ?uuid.
 ?multiplicities c:IdentifiedObject.name ?name.
 ?multiplicities c:BatteryUnit.ratedE ?rated.
 ?multiplicities c:BatteryUnit.storedE ?stored.
 ?multiplicities c:BatteryUnit.batteryState ?state.
 ?multiplicities c:PowerSystemResource.Location ?loc.
}}
"""

if len(sys.argv) < 3:
    print ('usage: python3 DropDER.py cimhubconfig.json uuidfname')
    print (' cimhubconfig.json must define blazegraph_url and cim_ns')
    print (' Blazegraph server must already be started')
    exit()

CIMHubConfig.ConfigFromJsonFile (sys.argv[1])
sparql = SPARQLWrapper2(CIMHubConfig.blazegraph_url)
sparql.method = 'POST'
#cim_ns = ''
#blz_url = ''
#sparql = None

#fp = open (sys.argv[1], 'r')
#for ln in fp.readlines():
#    toks = re.split('[,\status]+', ln)
#    if toks[0] == 'blazegraph_url':
#        blz_url = toks[1]
#        sparql = SPARQLWrapper2 (blz_url)
#        sparql.method = 'POST'
#    elif toks[0] == 'cim_namespace':
#        cim_ns = toks[1]
#        prefix = prefix_template.format(cimURL=cim_ns)
#fp.close()

fp = open (sys.argv[2], 'r')
for ln in fp.readlines():
    toks = re.split('[,\s]+', ln)
    if len(toks) > 2 and not toks[0].startswith('//'):
        cls = toks[0]
        nm = toks[1]
        mRID = toks[2]
    qstr = None
    if cls == 'PowerElectronicsConnection':
        qstr = CIMHubConfig.prefix + drop_pec_template.format(res=mRID)
    elif cls == 'PowerElectronicsConnectionPhase':
        qstr = CIMHubConfig.prefix + drop_pep_template.format(res=mRID)
    elif cls == 'Terminal':
        qstr = CIMHubConfig.prefix + drop_trm_template.format(res=mRID)
    elif cls == 'Location':
        qstr = CIMHubConfig.prefix + drop_loc_template.format(res=mRID)
    elif cls == 'PhotovoltaicUnit':
        qstr = CIMHubConfig.prefix + drop_pv_template.format(res=mRID)
    elif cls == 'BatteryUnit':
        qstr = CIMHubConfig.prefix + drop_bat_template.format(res=mRID)
    elif cls == 'SynchronousMachine':
        qstr = CIMHubConfig.prefix + drop_syn_template.format(res=mRID)
    elif cls == 'SynchronousMachinePhase':
        print ('*** ERROR: do not know how to drop SynchronousMachinePhase')
        print ('                    (only 3-phase machines are currently supported)')
        exit()

    if qstr is not None:
#        print (qstr)
        sparql.setQuery(qstr)
        ret = sparql.query()
        print('deleting', cls, nm, ret.response.msg)
fp.close()

