# About the inputs:
import sys, re, os
import Milsoft_GridLAB_D_Feeder_Generation
import calibrateFeeder
import processSCADA #TODO: write this module
import AddTapeObjects
import feeder
import tempfile
#import writeFeederConfig #TODO: future work (after June 1 deadline)

# MilSoft model ( milsoft = [stdPath, seqPath])
# Case Flag
# Feeder Info (region, ratings, etc) TBD
# SCADA Data
# feeder configuration file (user may input feeder configuration file as created by a previous calibration attempt on this feeder)
# feeder calibration file (user may input calibration file as created by a previous calibration attempt on this feeder)
# user_flag_to_calibrate (user may set to 0 to indicate they don't want to calibrate, just want general popualted model)
def OMFmain(milsoft, scada, case_flag, calibration_config,  model_name='Feeder', user_flag_to_calibrate=1):

	if milsoft is None:
		print ("Please input a model to convert!")
		# error
		return None, None
	else:
		internal_flag_to_calibrate = 0
		if scada is None:
			pass  # Well, we can't do any calibration but we can still pump out a populated model by using defaults.
		else:
			internal_flag_to_calibrate = 1
			days, SCADA = processSCADA.getValues(scada)

		outGLM = milsoft
		directory = tempfile.mkdtemp()
		print "Calibration testing in ", directory
		
		# write base .glm to file (save as .txt so that it isn't run when batch file executed)
		basefile = open(directory+'/'+model_name+'_base_glm.txt','w')
		basefile.write('\\\\ Base feeder model generated by milToGridlab.py.\n')
		basefile.write(feeder.sortedWrite(outGLM))
		basefile.close()
		
		if internal_flag_to_calibrate == 1 and user_flag_to_calibrate == 1:  # The user must want to calibrate (user_flag_to_calibrate = 1) and we must have SCADA input (internal_flag_to_calibrate = 1).
			# Send base .glm dictionary to calibration function
			final_calib_file, final_dict, last_key = calibrateFeeder.calibrateFeeder(outGLM, days, SCADA, case_flag, calibration_config, directory)
		else:
			# Populate the feeder. 
			print ("Either the user selected not to calibrate this feeder, the SCADA was not input, or this feeder has already been calibrated.")
			final_dict, last_key = Milsoft_GridLAB_D_Feeder_Generation.GLD_Feeder(outGLM,case_flag,directory,calibration_config)
		#AddTapeObjects
		#input_code_filename = 'test_feeder'
		if final_dict is not None:
			#AddTapeObjects.add_recorders(final_dict,None,last_key,None,1,0,input_code_filename,None,0,0)
			dict_with_recorders, last_key = AddTapeObjects.add_recorders(final_dict,case_flag,0,1,model_name,last_key)
			return dict_with_recorders, final_calib_file
		else:
			return None, None
		
def _tests():
	feederDict = feeder.parse('./IEEE13Basic.glm')
	model_name = 'testing_model_13Node'
	scada = {'summerDay' : '2012-06-29',
		'winterDay' : '2012-01-19',
		'shoulderDay' : '2012-04-10',
		'summerPeakKW' : 5931.56,
		'summerTotalEnergy' : 107380.8,
		'summerPeakHour' : 17,
		'summerMinimumKW' : 2988,
		'summerMinimumHour' : 6,
		'winterPeakKW' : 3646.08,
		'winterTotalEnergy' : 75604.32,
		'winterPeakHour' : 21,
		'winterMinimumKW' : 2469.60,
		'winterMinimumHour' : 1,
		'shoulderPeakKW' : 2518.56 ,
		'shoulderTotalEnergy' : 52316.64,
		'shoulderPeakHour' : 21,
		'shoulderMinimumKW' : 1738.08,
		'shoulderMinimumHour' : 2} 
	calibration_config = None
	case_flag = -1 # base case, do not put None
	
	calibratedFeederDict, calibrationDict = OMFmain(feederDict, scada, case_flag, calibration_config, model_name, 1)
	
	assert calibratedFeederDict != None
	assert calibrationDict != None 

if __name__ ==  '__main__':
	_tests()