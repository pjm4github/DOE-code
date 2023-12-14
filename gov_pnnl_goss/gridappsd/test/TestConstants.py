

class TestConstants:
    ieee8500_mrid = "_4F76A5F9-271D-9EB8-5E31-AA362D86F2C3"
    power_system_config = '{"SubGeographicalRegion_name":"ieee8500_SubRegion","GeographicalRegion_name":"ieee8500_Region","Line_name:"+ieee8500_mrid}'

    application_object_config_esc = '{"static_inputs": {"ieee8500": {"control_method": "ACTIVE", "capacitor_delay": 60, "regulator_delay": 60, "desired_pf": 0.99, "d_max": 0.9, "d_min": 0.1,"substation_link": "xf_hvmv_sub","regulator_list": ["reg_FEEDER_REG", "reg_VREG2", "reg_VREG3", "reg_VREG4"],"regulator_configuration_list": ["rcon_FEEDER_REG", "rcon_VREG2", "rcon_VREG3", "rcon_VREG4"],"capacitor_list": ["cap_capbank0a","cap_capbank0b","cap_capbank0c","cap_capbank1a","cap_capbank1b","cap_capbank1c","cap_capbank2a","cap_capbank2b","cap_capbank2c","cap_capbank3"],"voltage_measurements": ["l2955047,1", "l3160107,1", "l2673313,2", "l2876814,2", "m1047574,3", "l3254238,4"],"maximum_voltages": 7500, "minimum_voltages": 6500,"max_vdrop": 5200,"high_load_deadband": 100, "desired_voltages": 7000,"low_load_deadband": 100,"pf_phase": "ABC"}}}'

    application_object_esc = '{"name":"vvo","config_string:"+application_object_config_esc}'

    application_object = '{"name":"vvo","config_string:"+application_object_config_esc}'

    application_config_esc = '{"applications":[""+application_object.replaceAll("\"", "\\\\\"")+"]}'

    application_config = '{"applications":[""+application_object+"]}'

    model_creation_config = '{"load_scaling_factor":1.0,"triplex":"y","encoding":"u","system_frequency":60,"voltage_multiplier":1.0,"power_unit_conversion":1.0,"unique_names":"y","schedule_name":"ieeezipload","z_fraction":0.0,"i_fraction":1.0,"p_fraction":0.0}'

    simulation_config_output_object_1 = '{"name":"rcon_FEEDER_REG","properties":["connect_type","Control","control_level","PT_phase","band_center","band_width","dwell_time","raise_taps","lower_taps","regulation"]}'

    simulation_config_output_object_2 = '{"name":"rcon_VREG2","properties":["connect_type","Control","control_level","PT_phase","band_center","band_width","dwell_time","raise_taps","lower_taps","regulation"]}'

    simulation_config_output_full = '{"output_objects":[{"name":"rcon_FEEDER_REG","properties":["connect_type","Control","control_level","PT_phase","band_center","band_width","dwell_time","raise_taps","lower_taps","regulation"]},{"name":"rcon_VREG2","properties":["connect_type","Control","control_level","PT_phase","band_center","band_width","dwell_time","raise_taps","lower_taps","regulation"]},{"name":"rcon_VREG3","properties":["connect_type","Control","control_level","PT_phase","band_center","band_width","dwell_time","raise_taps","lower_taps","regulation"]},{"name":"rcon_VREG4","properties":["connect_type","Control","control_level","PT_phase","band_center","band_width","dwell_time","raise_taps","lower_taps","regulation"]},{"name":"reg_FEEDER_REG","properties":["configuration","phases","to","tap_A","tap_B","tap_C"]},{"name":"reg_VREG2","properties":["configuration","phases","to","tap_A","tap_B","tap_C"]},{"name":"reg_VREG3","properties":["configuration","phases","to","tap_A","tap_B","tap_C"]},{"name":"reg_VREG4","properties":["configuration","phases","to","tap_A","tap_B","tap_C"]},{"name":"cap_capbank0a","properties":["phases","pt_phase","phases_connected","control","control_level","capacitor_A","dwell_time","switchA"]},{"name":"cap_capbank1a","properties":["phases","pt_phase","phases_connected","control","control_level","capacitor_A","dwell_time","switchA"]},{"name":"cap_capbank2a","properties":["phases","pt_phase","phases_connected","control","control_level","capacitor_A","dwell_time","switchA"]},{"name":"cap_capbank0b","properties":["phases","pt_phase","phases_connected","control","control_level","capacitor_B","dwell_time","switchB"]},{"name":"cap_capbank1b","properties":["phases","pt_phase","phases_connected","control","control_level","capacitor_B","dwell_time","switchB"]},{"name":"cap_capbank2b","properties":["phases","pt_phase","phases_connected","control","control_level","capacitor_B","dwell_time","switchB"]},{"name":"cap_capbank0c","properties":["phases","pt_phase","phases_connected","control","control_level","capacitor_C","dwell_time","switchC"]},{"name":"cap_capbank1c","properties":["phases","pt_phase","phases_connected","control","control_level","capacitor_C","dwell_time","switchC"]},{"name":"cap_capbank2c","properties":["phases","pt_phase","phases_connected","control","control_level","capacitor_C","dwell_time","switchC"]},{"name":"cap_capbank3","properties":["phases","pt_phase","phases_connected","control","control_level","capacitor_A","capacitor_B","capacitor_C","dwell_time","switchA","switchB","switchC"]},{"name":"xf_hvmv_sub","properties":["power_in_A","power_in_B","power_in_C"]},{"name":"l2955047","properties":["voltage_A","voltage_B","voltage_C"]},{"name":"l2673313","properties":["voltage_A","voltage_B","voltage_C"]},{"name":"l3160107","properties":["voltage_A","voltage_B","voltage_C"]},{"name":"l2876814","properties":["voltage_A","voltage_B","voltage_C"]},{"name":"l3254238","properties":["voltage_A","voltage_B","voltage_C"]},{"name":"m1047574","properties":["voltage_A","voltage_B","voltage_C"]},{"name":"_hvmv_sub_lsb","properties":["voltage_A","voltage_B","voltage_C"]},{"name":"190-8593","properties":["voltage_A","voltage_B","voltage_C"]},{"name":"190-8581","properties":["voltage_A","voltage_B","voltage_C"]},{"name":"190-7361","properties":["voltage_A","voltage_B","voltage_C"]}]}'


    simulation_config_output_short = '{"output_objects":[""+simulation_config_output_object_1+"",""+simulation_config_output_object_2+""]}'

    simulation_config = '{"power_flow_solver_method":"NR","duration":120,"simulation_name":"ieee8500","simulator":"GridLAB-D","start_time":"2009-07-21 00:00:00","timestep_frequency":1000,"timestep_increment":1000,"simulation_output:""+simulation_config_output_short+"","model_creation_config":"+model_creation_config+"}'

    request_simulation_config = '{"power_system_config":""+power_system_config+"","simulation_config":""+simulation_config+"","application_config":""+application_config+"}'

    request_simulation_config_esc = '{"power_system_config":""+power_system_config+"","simulation_config":""+simulation_config+"","application_config":""+application_config_esc+"}'

    fncs_bridge_response = '{"command":"isInitialized","response":"true","output":"Any messages from simulator regarding initialization"}'

    username = "system"
    password = "password"
