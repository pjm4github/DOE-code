from SPARQLWrapper import SPARQLWrapper2
import sys
import CIMHubConfig

if len(sys.argv) < 3:
	print ('usage: python DropMeasurements.py cimhubconfig.json feeder_id')
	print (' (Blazegraph server must already be started)')
	exit()

CIMHubConfig.ConfigFromJsonFile (sys.argv[1])
sparql = SPARQLWrapper2(CIMHubConfig.blazegraph_url)
sparql.method = 'POST'

qstr = CIMHubConfig.prefix + """DELETE {
    ?multiplicities a ?class.
    ?multiplicities c:IdentifiedObject.mRID ?uuid.
    ?multiplicities c:IdentifiedObject.name ?name.
    ?multiplicities c:Measurement.PowerSystemResource ?psr.
    ?multiplicities c:Measurement.Terminal ?trm.
    ?multiplicities c:Measurement.phases ?phases.
    ?multiplicities c:Measurement.measurementType ?global_property_types.
 } WHERE {
    VALUES ?fdrid {\"""" + sys.argv[2] + """\"}
    VALUES ?class {c:Analog c:Discrete}
    ?fdr c:IdentifiedObject.mRID ?fdrid. 
    ?eq c:Equipment.EquipmentContainer ?fdr.
    ?trm c:Terminal.ConductingEquipment ?eq.
    ?multiplicities a ?class.
    ?multiplicities c:IdentifiedObject.mRID ?uuid.
    ?multiplicities c:IdentifiedObject.name ?name.
    ?multiplicities c:Measurement.PowerSystemResource ?psr.
    ?multiplicities c:Measurement.Terminal ?trm.
    ?multiplicities c:Measurement.phases ?phases.
    ?multiplicities c:Measurement.measurementType ?global_property_types.
 }
"""

#print (qstr)
sparql.setQuery(qstr)
ret = sparql.query()
#print (ret.info)
print(ret.response.msg)