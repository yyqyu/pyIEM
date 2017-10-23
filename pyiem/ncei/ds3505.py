"""Implementation of the NCEI DS3505 format

    ftp://ftp.ncdc.noaa.gov/pub/data/noaa/ish-format-document.pdf

"""
from __future__ import print_function
import re

ADDITIONAL = {
    # Hourly Precip
    'AA1': [['hrs', 2], ['depth', 4], ['cond_code', 1], ['qc', 1]],
    'AA2': [['hrs', 2], ['depth', 4], ['cond_code', 1], ['qc', 1]],
    'AA3': [['hrs', 2], ['depth', 4], ['cond_code', 1], ['qc', 1]],
    'AA4': [['hrs', 2], ['depth', 4], ['cond_code', 1], ['qc', 1]],
    # Monthly Precip
    'AB1': [['depth', 5], ['cond_code', 1], ['qc', 1]],
    # Precip History
    'AC1': [['duration', 1], ['char_code', 1], ['qc', 1]],
    # Greatest amount in a month
    'AD1': [['depth', 5], ['cond_code', 1], ['date1', 4], ['date2', 4],
            ['date3', 4], ['qc', 1]],
    # Precip number of days
    'AE1': [['q01_days', 2], ['q01_days_qc', 1],
            ['q10_days', 2], ['q10_days_qc', 1],
            ['q50_days', 2], ['q50_days_qc', 1],
            ['q100_days', 2], ['q100_days_qc', 1]],
    # Precip estimated?
    'AG1': [['code', 1], ['depth', 3]],
    # Short duration precip
    'AH1': [['period', 3], ['depth', 4], ['code', 1], ['enddate', 6],
            ['qc', 1]],
    'AH2': [['period', 3], ['depth', 4], ['code', 1], ['enddate', 6],
            ['qc', 1]],
    'AH3': [['period', 3], ['depth', 4], ['code', 1], ['enddate', 6],
            ['qc', 1]],
    'AH4': [['period', 3], ['depth', 4], ['code', 1], ['enddate', 6],
            ['qc', 1]],
    'AH5': [['period', 3], ['depth', 4], ['code', 1], ['enddate', 6],
            ['qc', 1]],
    'AH6': [['period', 3], ['depth', 4], ['code', 1], ['enddate', 6],
            ['qc', 1]],
    # Short duration precip for month
    'AI1': [['period', 3], ['depth', 4], ['code', 1], ['enddate', 6],
            ['qc', 1]],
    'AI2': [['period', 3], ['depth', 4], ['code', 1], ['enddate', 6],
            ['qc', 1]],
    'AI3': [['period', 3], ['depth', 4], ['code', 1], ['enddate', 6],
            ['qc', 1]],
    'AI4': [['period', 3], ['depth', 4], ['code', 1], ['enddate', 6],
            ['qc', 1]],
    'AI5': [['period', 3], ['depth', 4], ['code', 1], ['enddate', 6],
            ['qc', 1]],
    'AI6': [['period', 3], ['depth', 4], ['code', 1], ['enddate', 6],
            ['qc', 1]],
    # Snow depth
    'AJ1': [['depth', 4], ['cond_code', 1], ['qc', 1], ['swe', 6],
            ['swe_cond_code', 1],
            ['swe_qc', 1]],
    # Snow depth month
    'AK1': [['depth', 4], ['cond_code', 1], ['dates', 6], ['qc', 1]],
    # Snow accumulation
    'AL1': [['period', 2], ['depth', 3], ['cond_code', 1], ['qc', 1]],
    'AL2': [['period', 2], ['depth', 3], ['cond_code', 1], ['qc', 1]],
    'AL3': [['period', 2], ['depth', 3], ['cond_code', 1], ['qc', 1]],
    'AL4': [['period', 2], ['depth', 3], ['cond_code', 1], ['qc', 1]],
    # Snow greatest in month
    'AM1': [['depth', 4], ['cond_code', 1], ['dates1', 4], ['dates2', 4],
            ['dates3', 4], ['qc', 1]],
    # snow for day month?
    'AN1': [['period', 3], ['depth', 4], ['cond_code', 1], ['qc', 1]],
    # precip occurence
    'AO1': [['minutes', 2], ['depth', 4], ['cond_code', 1], ['qc', 1]],
    'AO2': [['minutes', 2], ['depth', 4], ['cond_code', 1], ['qc', 1]],
    'AO3': [['minutes', 2], ['depth', 4], ['cond_code', 1], ['qc', 1]],
    'AO4': [['minutes', 2], ['depth', 4], ['cond_code', 1], ['qc', 1]],
    # 15 minute precip
    'AP1': [['depth', 4], ['cond_code', 1], ['qc', 1]],
    'AP2': [['depth', 4], ['cond_code', 1], ['qc', 1]],
    'AP3': [['depth', 4], ['cond_code', 1], ['qc', 1]],
    'AP4': [['depth', 4], ['cond_code', 1], ['qc', 1]],
    # presentweather
    'AT1': [['source', 2], ['type', 2], ['abbr', 4], ['qc', 1]],
    'AT2': [['source', 2], ['type', 2], ['abbr', 4], ['qc', 1]],
    'AT3': [['source', 2], ['type', 2], ['abbr', 4], ['qc', 1]],
    'AT4': [['source', 2], ['type', 2], ['abbr', 4], ['qc', 1]],
    'AT5': [['source', 2], ['type', 2], ['abbr', 4], ['qc', 1]],
    'AT6': [['source', 2], ['type', 2], ['abbr', 4], ['qc', 1]],
    'AT7': [['source', 2], ['type', 2], ['abbr', 4], ['qc', 1]],
    'AT8': [['source', 2], ['type', 2], ['abbr', 4], ['qc', 1]],
    # present weather intensity
    'AU1': [['proximity', 1], ['descriptor', 1], ['precip', 2], ['obscure', 1],
            ['other', 1], ['combo', 1], ['qc', 1]],
    'AU2': [['proximity', 1], ['descriptor', 1], ['precip', 2], ['obscure', 1],
            ['other', 1], ['combo', 1], ['qc', 1]],
    'AU3': [['proximity', 1], ['descriptor', 1], ['precip', 2], ['obscure', 1],
            ['other', 1], ['combo', 1], ['qc', 1]],
    'AU4': [['proximity', 1], ['descriptor', 1], ['precip', 2], ['obscure', 1],
            ['other', 1], ['combo', 1], ['qc', 1]],
    'AU5': [['proximity', 1], ['descriptor', 1], ['precip', 2], ['obscure', 1],
            ['other', 1], ['combo', 1], ['qc', 1]],
    'AU6': [['proximity', 1], ['descriptor', 1], ['precip', 2], ['obscure', 1],
            ['other', 1], ['combo', 1], ['qc', 1]],
    'AU7': [['proximity', 1], ['descriptor', 1], ['precip', 2], ['obscure', 1],
            ['other', 1], ['combo', 1], ['qc', 1]],
    'AU8': [['proximity', 1], ['descriptor', 1], ['precip', 2], ['obscure', 1],
            ['other', 1], ['combo', 1], ['qc', 1]],
    'AU9': [['proximity', 1], ['descriptor', 1], ['precip', 2], ['obscure', 1],
            ['other', 1], ['combo', 1], ['qc', 1]],
    # Automated weather
    'AW1': [['cond_code', 2], ['qc', 1]],
    'AW2': [['cond_code', 2], ['qc', 1]],
    'AW3': [['cond_code', 2], ['qc', 1]],
    'AW4': [['cond_code', 2], ['qc', 1]],
    # Past Weather
    'AX1': [['cond_code', 2], ['qc', 1], ['period', 2], ['period_qc', 1]],
    'AX2': [['cond_code', 2], ['qc', 1], ['period', 2], ['period_qc', 1]],
    'AX3': [['cond_code', 2], ['qc', 1], ['period', 2], ['period_qc', 1]],
    'AX4': [['cond_code', 2], ['qc', 1], ['period', 2], ['period_qc', 1]],
    'AX5': [['cond_code', 2], ['qc', 1], ['period', 2], ['period_qc', 1]],
    'AX6': [['cond_code', 2], ['qc', 1], ['period', 2], ['period_qc', 1]],
    # Past weather
    'AY1': [['cond_code', 1], ['qc', 1], ['period', 2], ['period_qc', 1]],
    'AY2': [['cond_code', 1], ['qc', 1], ['period', 2], ['period_qc', 1]],
    # Past weather automated
    'AZ1': [['cond_code', 1], ['qc', 1], ['period', 2], ['period_qc', 1]],
    'AZ2': [['cond_code', 1], ['qc', 1], ['period', 2], ['period_qc', 1]],
    # CRN Secondary Precip
    'CB1': [['minutes', 2], ['depth', 6], ['qc', 1], ['precip_flag', 1]],
    'CB2': [['minutes', 2], ['depth', 6], ['qc', 1], ['precip_flag', 1]],
    # CRN, Fan Speed
    'CF1': [['speed', 4], ['qc', 1], ['speed_flag', 1]],
    'CF2': [['speed', 4], ['qc', 1], ['speed_flag', 1]],
    'CF3': [['speed', 4], ['qc', 1], ['speed_flag', 1]],
    # CRN, subhour precip
    'CG1': [['depth', 6], ['qc', 1], ['depth_flag', 1]],
    'CG2': [['depth', 6], ['qc', 1], ['depth_flag', 1]],
    'CG3': [['depth', 6], ['qc', 1], ['depth_flag', 1]],
    # CRN, rh
    'CH1': [['minutes', 2], ['tmpc', 5], ['tmpc_qc', 1], ['tmpc_flag', 1],
            ['avg_rh', 4], ['qc', 1], ['avg_rh_flag', 1]],
    'CH2': [['minutes', 2], ['tmpc', 5], ['tmpc_qc', 1], ['tmpc_flag', 1],
            ['avg_rh', 4], ['qc', 1], ['avg_rh_flag', 1]],
    # CRN, rh
    'CI1': [['min_rh_temp', 5], ['min_rh_temp_qc', 1], ['min_rh_temp_flag', 1],
            ['max_rh_temp', 5], ['max_rh_temp_qc', 1], ['max_rh_temp_flag', 1],
            ['std_rh_temp', 5], ['std_rh_temp_qc', 1], ['std_rh_temp_flag', 1],
            ['std_rh', 5], ['std_rh_qc', 1], ['std_rh_flag', 1]],
    # CRN, battery voltage
    'CN1': [['batvol', 4], ['batvol_qc', 1], ['batvol_flag', 1],
            ['batvol_fl', 4], ['batvol_fl_qc', 1], ['batvol_fl_flag', 1],
            ['batvol_dl', 4], ['batvol_dl_qc', 1], ['batvol_dl_flag', 1]],
    # CRN, misc diagnostics
    'CN2': [['tranel', 5], ['tranel_qc', 1], ['tranel_flag', 1],
            ['tinlet_max', 5], ['tinlet_max_qc', 1], ['trinlet_max_flag', 1],
            ['opendoor_tm', 2], ['opendoor_tm_qc', 1],
            ['opendoor_tm_flag', 1]],
    # CRN, secondary diagnostic
    'CN3': [['refresavg', 6], ['refresavg_qc', 1], ['refresavg_flag', 1],
            ['dsignature', 6], ['dsignature__qc', 1], ['dsignature_flag', 1]],
    # CRN, secondary hourly diagnostic
    'CN4': [['heater_flag', 1], ['heater_flag_code', 1],
            ['heater_flag_code2', 1],
            ['doorflag', 1], ['doorflag_code', 1], ['doorflag_code2', 1],
            ['fortrans', 1], ['fortrans_code', 1], ['fortrans_code2', 1],
            ['refltrans', 3], ['refltrans_code', 1], ['refltrans_code2', 1]],
    # CRN, metadata
    'CO1': [['climat_division', 2], ['lst_conversion', 3]],
    'CO2': [['elementid', 3], ['time_offset', 5]],
    'CO3': [['elementid', 3], ['time_offset', 5]],
    'CO4': [['elementid', 3], ['time_offset', 5]],
    'CO5': [['elementid', 3], ['time_offset', 5]],
    'CO6': [['elementid', 3], ['time_offset', 5]],
    'CO7': [['elementid', 3], ['time_offset', 5]],
    'CO8': [['elementid', 3], ['time_offset', 5]],
    'CO9': [['elementid', 3], ['time_offset', 5]],
    # CRN, control section
    'CR1': [['dl_vn', 5], ['dl_vn_qc', 1], ['dl_vn_flag', 1]],
    # CRN, sub-hourly temperature
    'CT1': [['avg_temp', 5], ['avg_temp_qc', 1], ['avg_temp_flag', 1]],
    'CT2': [['avg_temp', 5], ['avg_temp_qc', 1], ['avg_temp_flag', 1]],
    'CT3': [['avg_temp', 5], ['avg_temp_qc', 1], ['avg_temp_flag', 1]],
    # CRN, colocated temp sensors
    'CU1': [['avg_temp', 5], ['avg_temp_qc', 1], ['avg_temp_flag', 1],
            ['temp_std', 4], ['temp_std_qc', 1], ['temp_std_flag', 1]],
    'CU2': [['avg_temp', 5], ['avg_temp_qc', 1], ['avg_temp_flag', 1],
            ['temp_std', 4], ['temp_std_qc', 1], ['temp_std_flag', 1]],
    'CU3': [['avg_temp', 5], ['avg_temp_qc', 1], ['avg_temp_flag', 1],
            ['temp_std', 4], ['temp_std_qc', 1], ['temp_std_flag', 1]],
    # CRN, hourly temp extreme
    'CV1': [['temp_min', 5], ['temp_min_qc', 1], ['temp_min_flag', 1],
            ['temp_min_time', 4], ['temp_min_time_qc', 1],
            ['temp_min_time_flag', 1],
            ['temp_max', 5], ['temp_max_qc', 1], ['temp_max_flag', 1],
            ['temp_max_time', 4], ['temp_max_time_qc', 1],
            ['temp_max_time_flag', 1]],
    'CV2': [['temp_min', 5], ['temp_min_qc', 1], ['temp_min_flag', 1],
            ['temp_min_time', 4], ['temp_min_time_qc', 1],
            ['temp_min_time_flag', 1],
            ['temp_max', 5], ['temp_max_qc', 1], ['temp_max_flag', 1],
            ['temp_max_time', 4], ['temp_max_time_qc', 1],
            ['temp_max_time_flag', 1]],
    'CV3': [['temp_min', 5], ['temp_min_qc', 1], ['temp_min_flag', 1],
            ['temp_min_time', 4], ['temp_min_time_qc', 1],
            ['temp_min_time_flag', 1],
            ['temp_max', 5], ['temp_max_qc', 1], ['temp_max_flag', 1],
            ['temp_max_time', 4], ['temp_max_time_qc', 1],
            ['temp_max_time_flag', 1]],
    # CRN, subhourly wetness
    'CW1': [['wet1', 5], ['wet1_qc', 1], ['wet1_flag', 1],
            ['wet2', 5], ['wet2_qc', 1], ['wet2_flag', 1]],
    # CRN, vibrating wire summary
    'CX1': [['precipitation', 6], ['precip_qc', 1], ['precip_flag', 1],
            ['freq_avg', 4], ['freq_avg_qc', 1], ['freq_avg_flag', 1],
            ['freq_min', 4], ['freq_min_qc', 1], ['freq_min_flag', 1],
            ['freq_max', 4], ['freq_max_qc', 1], ['freq_max_flag', 1]],
    'CX2': [['precipitation', 6], ['precip_qc', 1], ['precip_flag', 1],
            ['freq_avg', 4], ['freq_avg_qc', 1], ['freq_avg_flag', 1],
            ['freq_min', 4], ['freq_min_qc', 1], ['freq_min_flag', 1],
            ['freq_max', 4], ['freq_max_qc', 1], ['freq_max_flag', 1]],
    'CX3': [['precipitation', 6], ['precip_qc', 1], ['precip_flag', 1],
            ['freq_avg', 4], ['freq_avg_qc', 1], ['freq_avg_flag', 1],
            ['freq_min', 4], ['freq_min_qc', 1], ['freq_min_flag', 1],
            ['freq_max', 4], ['freq_max_qc', 1], ['freq_max_flag', 1]],
    # Visual Runway
    'ED1': [['angle', 2], ['runway', 1], ['visibility', 4],
            ['visibility_qc', 1]],
    # Sky coverage
    'GA1': [['coverage', 2], ['coverage_qc', 1], ['height', 6],
            ['height_qc', 1],
            ['type', 2], ['type_qc', 1]],
    'GA2': [['coverage', 2], ['coverage_qc', 1], ['height', 6],
            ['height_qc', 1],
            ['type', 2], ['type_qc', 1]],
    'GA3': [['coverage', 2], ['coverage_qc', 1], ['height', 6],
            ['height_qc', 1],
            ['type', 2], ['type_qc', 1]],
    'GA4': [['coverage', 2], ['coverage_qc', 1], ['height', 6],
            ['height_qc', 1],
            ['type', 2], ['type_qc', 1]],
    'GA5': [['coverage', 2], ['coverage_qc', 1], ['height', 6],
            ['height_qc', 1],
            ['type', 2], ['type_qc', 1]],
    'GA6': [['coverage', 2], ['coverage_qc', 1], ['height', 6],
            ['height_qc', 1],
            ['type', 2], ['type_qc', 1]],
    # sky cover summation
    'GD1': [['state_code', 1], ['state_code2', 2], ['state_qc', 1],
            ['height', 6], ['height_qc', 1], ['height_char', 1]],
    'GD2': [['state_code', 1], ['state_code2', 2], ['state_qc', 1],
            ['height', 6], ['height_qc', 1], ['height_char', 1]],
    'GD3': [['state_code', 1], ['state_code2', 2], ['state_qc', 1],
            ['height', 6], ['height_qc', 1], ['height_char', 1]],
    'GD4': [['state_code', 1], ['state_code2', 2], ['state_qc', 1],
            ['height', 6], ['height_qc', 1], ['height_char', 1]],
    'GD5': [['state_code', 1], ['state_code2', 2], ['state_qc', 1],
            ['height', 6], ['height_qc', 1], ['height_char', 1]],
    'GD6': [['state_code', 1], ['state_code2', 2], ['state_qc', 1],
            ['height', 6], ['height_qc', 1], ['height_char', 1]],
    # sky coverage identifier
    'GE1': [['convective', 1], ['vertical_datum', 6], ['height', 6],
            ['lower_range', 6]],
    # Sky coverage
    'GF1': [['total', 2], ['opaque', 2], ['coverage_qc', 1],
            ['lowest_coverage', 2], ['lowest_coverage_qc', 1],
            ['lowest_genus', 2], ['lowest_genus_code', 1],
            ['lowest_height', 5], ['lowest_height_qc', 1],
            ['mid_genus', 2], ['mid_genus_qc', 1],
            ['high_genus', 2], ['high_genus_qc', 1]],
    # below station cloud ID
    'GG1': [['coverage_code', 2], ['coverage_qc', 1], ['height', 5],
            ['height_qc', 1], ['type_code', 2], ['type_code_qc', 1],
            ['top_code', 2], ['top_code_qc', 1]],
    'GG2': [['coverage_code', 2], ['coverage_qc', 1], ['height', 5],
            ['height_qc', 1], ['type_code', 2], ['type_code_qc', 1],
            ['top_code', 2], ['top_code_qc', 1]],
    'GG3': [['coverage_code', 2], ['coverage_qc', 1], ['height', 5],
            ['height_qc', 1], ['type_code', 2], ['type_code_qc', 1],
            ['top_code', 2], ['top_code_qc', 1]],
    'GG4': [['coverage_code', 2], ['coverage_qc', 1], ['height', 5],
            ['height_qc', 1], ['type_code', 2], ['type_code_qc', 1],
            ['top_code', 2], ['top_code_qc', 1]],
    'GG5': [['coverage_code', 2], ['coverage_qc', 1], ['height', 5],
            ['height_qc', 1], ['type_code', 2], ['type_code_qc', 1],
            ['top_code', 2], ['top_code_qc', 1]],
    'GG6': [['coverage_code', 2], ['coverage_qc', 1], ['height', 5],
            ['height_qc', 1], ['type_code', 2], ['type_code_qc', 1],
            ['top_code', 2], ['top_code_qc', 1]],
    # Solar Radiation
    'GH1': [['solarrad', 5], ['solarrad_qc', 1], ['solarrad_flag', 1],
            ['solarrad_min', 5], ['solarrad_min_qc', 1],
            ['solarrad_min_flag', 1],
            ['solarrad_max', 5], ['solarrad_max_qc', 1],
            ['solarrad_max_flag', 1],
            ['solarrad_std', 5], ['solarrad_std_qc', 1],
            ['solarrad_std_flag', 1]],
    # Sunshine
    'GJ1': [['duration', 4], ['duration_qc', 1]],
    # sunhine
    'GK1': [['percent', 3], ['percent_qc', 1]],
    # sunshine for month
    'GL1': [['duration', 5], ['duration_qc', 1]],
    # solar irradiance
    'GM1': [['time', 4], ['global_irradiance', 4],
            ['global_irradiance_flag', 2],
            ['global_irradiance_qc', 1],
            ['direct_irradiance', 4], ['direct_irradiance_flag', 2],
            ['direct_irradiance_qc', 1],
            ['diffuse_irradiance', 4], ['diffuse_irradiance_flag', 2],
            ['diffuse_irradiance_qc', 1],
            ['uvb_irradiance', 4], ['uvb_irradiance_flag', 2],
            ['uvb_irradiance_qc', 1]],
    # solar radiation
    'GN1': [['period', 4], ['upwelling_global', 4], ['upwelling_global_qc', 1],
            ['downwelling_thermal', 4], ['downwelling_thermal_qc', 1],
            ['upwelling_thermal', 4], ['upwelling_thermal_qc', 1],
            ['par', 4], ['par_qc', 4],
            ['solar_zenith', 3], ['solar_zenith_qc', 1]],
    # Net Solar
    'GO1': [['time', 4], ['net_solar', 4], ['net_solar_qc', 1],
            ['net_infrared', 4], ['net_infrared_qc', 1],
            ['net_radiation', 4], ['net_radiation_qc', 1]],
    # Modelled irradiance
    'GP1': [['time', 4], ['global_horizontal', 4],
            ['global_horizontal_flag', 2],
            ['global_horizontal_uncertainty', 3],
            ['direct_normal', 4], ['direct_normal_flag', 2],
            ['direct_normal_uncertainty', 3],
            ['diffuse_horizontal', 4], ['diffuse_horizontal_flag', 2],
            ['diffuse_horizontal_uncertainty', 3]],
    # hourly solar angle
    'GQ1': [['time', 4], ['zenith_angle', 4], ['zenith_angle_qc', 1],
            ['azimuth_angle', 4], ['azimuth_angle_qc', 1]],
    # hourly extraterrestrial rad
    'GR1': [['time', 4], ['horizontal', 4], ['horizontal_qc', 1],
            ['normal', 4], ['normal_qc', 1]],
    # Hail data
    'HL1': [['size', 3], ['size_qc', 1]],
    # Ground Surface
    'IA1': [['code', 2], ['code_qc', 1]],
    # Ground Surface Min temp
    'IA2': [['period', 3], ['min_tmpc', 5], ['min_tempc_qc', 1]],
    # Hourly surface temperature
    'IB1': [['surftemp', 5], ['surftemp_qc', 1], ['surftemp_flag', 1],
            ['surftemp_min', 5], ['surftemp_min_qc', 1],
            ['surftemp_min_flag', 1],
            ['surftemp_max', 5], ['surftemp_max_qc', 1],
            ['surftemp_max_flag', 1],
            ['surftemp_std', 4], ['surftemp_std_qc', 1],
            ['surftemp_std_flag', 1]],
    # Hourly Surface
    'IB2': [['surftemp_sb', 5], ['surftemp_sb_qc', 1], ['surftemp_sb_flag', 1],
            ['surftemp_sb_std', 4], ['surftemp_sb_std_qc', 1],
            ['surftemp_sb_std_flag', 1]],
    # Ground surface obs
    'IC1': [['hours', 2], ['wind_movement', 4], ['wind_movement_code', 1],
            ['wind_movement_flag', 1], ['evaporation', 3],
            ['evaporation_code', 1],
            ['evaporation_qc', 1], ['max_pan_tmpc', 4],
            ['max_pan_tmpc_code', 1],
            ['max_pan_tmpc_qc', 1], ['min_pan_tmpc', 4],
            ['min_pan_tmpc_code', 1],
            ['min_pan_tmpc_qc', 1]],
    # Temperature extremes
    'KA1': [['hours', 3], ['code', 1], ['tmpc', 5], ['qc', 1]],
    'KA2': [['hours', 3], ['code', 1], ['tmpc', 5], ['qc', 1]],
    'KA3': [['hours', 3], ['code', 1], ['tmpc', 5], ['qc', 1]],
    'KA4': [['hours', 3], ['code', 1], ['tmpc', 5], ['qc', 1]],
    # average air temp
    'KB1': [['hours', 3], ['code', 1], ['tmpc', 5], ['qc', 1]],
    'KB2': [['hours', 3], ['code', 1], ['tmpc', 5], ['qc', 1]],
    'KB3': [['hours', 3], ['code', 1], ['tmpc', 5], ['qc', 1]],
    # extreme air temp
    'KC1': [['month_code', 1], ['cond_code', 1], ['tmpc', 5], ['dates', 6],
            ['tmpc_qc', 1]],
    'KC2': [['month_code', 1], ['cond_code', 1], ['tmpc', 5], ['dates', 6],
            ['tmpc_qc', 1]],
    # heating/cooling degree days
    'KD1': [['period', 3], ['code', 1], ['value', 4], ['qc', 1]],
    'KD2': [['period', 3], ['code', 1], ['value', 4], ['qc', 1]],
    # extreme temperatures, number of days
    'KE1': [['days32', 2], ['days32_code', 1],
            ['days90', 2], ['days90_code', 1],
            ['daysmin32', 2], ['daysmin32_code', 1],
            ['daysmin0', 2], ['daysmin0_code', 1]],
    # Hourly calc temp
    'KF1': [['temp', 5], ['temp_qc', 1]],
    # average dewpoint
    'KG1': [['period', 3], ['code', 1], ['dewpoint', 5], ['dewpoint_code', 1],
            ['dewpoint_qc', 1]],
    'KG2': [['period', 3], ['code', 1], ['dewpoint', 5], ['dewpoint_code', 1],
            ['dewpoint_qc', 1]],
    # pressure
    'MA1': [['altimer', 5], ['altimeter_code', 1], ['station_pressure', 5],
            ['station_pressure_code', 1]],
    # Pressure Tendency
    'MD1': [['code', 1], ['code_qc', 1], ['threehour', 3], ['threehour_qc', 1],
            ['24hour', 4], ['24hour_qc', 1]],
    # geopotential
    'ME1': [['level_code', 1], ['height', 4], ['height_qc', 1]],
    # SLP
    'MF1': [['pressure', 5], ['pressure_qc', 1], ['pressure_day', 5],
            ['pressure_day_qc']],
    # Pressure
    'MG1': [['avg_pressure', 5], ['avg_pressure_qc', 1],
            ['min_pressure', 5], ['min_pressure_qc', 1]],
    # Pressure for the month
    'MH1': [['avg_pressure', 5], ['avg_pressure_qc', 1],
            ['avg_slp', 5], ['avg_slp_qc', 1]],
    # Pressure for the month
    'MK1': [['max_pressure', 5], ['max_pressure_datetime', 6],
            ['max_pressure_qc', 1],
            ['min_pressure', 5], ['min_pressure_datetime', 6],
            ['min_pressure_qc', 1]],
    # Present Weather
    'MV1': [['code', 2], ['code_qc', 1]],
    'MV2': [['code', 2], ['code_qc', 1]],
    'MV3': [['code', 2], ['code_qc', 1]],
    'MV4': [['code', 2], ['code_qc', 1]],
    'MV5': [['code', 2], ['code_qc', 1]],
    'MV6': [['code', 2], ['code_qc', 1]],
    'MV7': [['code', 2], ['code_qc', 1]],
    # Present Weather Manual
    'MW1': [['code', 2], ['qc', 1]],
    'MW2': [['code', 2], ['qc', 1]],
    'MW3': [['code', 2], ['qc', 1]],
    'MW4': [['code', 2], ['qc', 1]],
    'MW5': [['code', 2], ['qc', 1]],
    'MW6': [['code', 2], ['qc', 1]],
    'MW7': [['code', 2], ['qc', 1]],
    # Supplemental Wind
    'OA1': [['code', 1], ['period', 2], ['smps', 4], ['qc', 1]],
    'OA2': [['code', 1], ['period', 2], ['smps', 4], ['qc', 1]],
    'OA3': [['code', 1], ['period', 2], ['smps', 4], ['qc', 1]],
    # hourly subhourly wind
    'OB1': [['period', 4], ['wind_max', 4], ['wind_max_qc', 1],
            ['wind_max_flag', 1], ['wind_max_drct', 3],
            ['wind_max_drct_qc', 1], ['wind_max_drct_flag', 1],
            ['wind_std', 5], ['wind_std_qc', 1], ['wind_std_flag', 1],
            ['wind_dir_std', 5], ['wind_dir_std_qc', 1],
            ['wind_dir_std_flag', 1]],
    'OB2': [['period', 4], ['wind_max', 4], ['wind_max_qc', 1],
            ['wind_max_flag', 1], ['wind_max_drct', 3],
            ['wind_max_drct_qc', 1], ['wind_max_drct_flag', 1],
            ['wind_std', 5], ['wind_std_qc', 1], ['wind_std_flag', 1],
            ['wind_dir_std', 5], ['wind_dir_std_qc', 1],
            ['wind_dir_std_flag', 1]],
    # Wind gust
    'OC1': [['speed', 4], ['speed_qc', 1]],
    # Supplementary Wind
    'OD1': [['code', 1], ['hours', 2], ['speed', 4], ['speed_qc', 1],
            ['direction', 3]],
    'OD2': [['code', 1], ['hours', 2], ['speed', 4], ['speed_qc', 1],
            ['direction', 3]],
    'OD3': [['code', 1], ['hours', 2], ['speed', 4], ['speed_qc', 1],
            ['direction', 3]],
    # -------------------------- page 108 ---------------------
    # Remarks
    'REM': [['id', 3], ['length', 3]],
    # Sea Surface temp
    'SA1': [['tmpc', 4], ['qc', 1]],
    # Wave
    'UA1': [['method', 1], ['period', 2], ['height', 3], ['height_qc', 1],
            ['state', 2], ['state_qc', 1]],
}

DS3505_RE = re.compile(r"""
^(?P<chars>[0-9]{4})
(?P<stationid>......)
(?P<wban>.....)
(?P<yyyymmdd>[0-9]{8})
(?P<hhmi>[0-9]{4})
(?P<srcflag>.)
(?P<lat>[\+\-][0-9]{5})
(?P<lon>[\+\-][0-9]{6})
(?P<report_type>.....)
(?P<elevation>[\+\-][0-9]{4})
(?P<call_id>.....)
(?P<qc_process>....)
(?P<drct>[0-9]{3})
(?P<drct_qc>.)
(?P<wind_code>.)
(?P<wind_speed_mps>[0-9]{4})
(?P<wind_speed_mps_qc>.)
(?P<ceiling_m>[0-9]{5})
(?P<ceiling_m_qc>.)
(?P<ceiling_m_how>.)
(?P<ceiling_m_cavok>.)
(?P<vsby_m>[0-9]{6})
(?P<vsby_m_qc>.)
(?P<vsby_m_variable>.)
(?P<vsby_m_variable_qc>.)
(?P<airtemp_c>[\+\-][0-9]{4})
(?P<airtemp_c_qc>.)
(?P<dewpointtemp_c>[\+\-][0-9]{4})
(?P<dewpointtemp_c_qc>.)
(?P<pressure_hpa>[0-9]{5})
(?P<pressure_hpa_qc>.)
""", re.VERBOSE)


def parser(msg):
    """Parse the message into a dict"""
    match = DS3505_RE.match(msg)
    if not match:
        return None
    data = match.groupdict()
    data['lat'] = (float(data['lat']) / 1000.
                   if data['lat'] != '+99999'
                   else None)
    data['lon'] = (float(data['lon']) / 1000.
                   if data['lon'] != '+999999'
                   else None)
    data['elevation'] = (float(data['elevation'])
                         if data['elevation'] != '+9999'
                         else None)
    data['wind_speed_mps'] = (float(data['wind_speed_mps']) / 10.
                              if data['wind_speed_mps'] != '9999'
                              else None)
    data['airtemp_c'] = (float(data['airtemp_c']) / 10.
                         if data['airtemp_c'] != '+9999'
                         else None)
    data['dewpointtemp_c'] = (float(data['dewpointtemp_c']) / 10.
                              if data['dewpointtemp_c'] != '+9999'
                              else None)
    data['pressure_hpa'] = (float(data['pressure_hpa']) / 10.
                            if data['pressure_hpa'] != '99999'
                            else None)
    for elem in ['drct', 'ceiling_m', 'vsby_m']:
        if data[elem][0] == 9 and len(data[elem]) * "9":
            data[elem] = None
        else:
            data[elem] = float(data[elem])

    parse_extra(data, msg[105:])

    return data


def parse_extra(data, extra):
    """Parse the additional data fields"""
    # ADD can be ignored
    extra = extra[3:]
    pos = 0
    data['extra'] = {}
    while pos < len(extra):
        code = extra[pos:pos+3]
        pos += 3
        if code == 'EQD':
            # TODO: unsure how we will handle this one
            break
        if code not in ADDITIONAL:
            raise Exception("Unaccounted for %s, remaining %s" % (code,
                                                                  extra[pos:]))
        data['extra'][code] = dict()
        for token in ADDITIONAL[code]:
            data['extra'][code][token[0]] = extra[pos:pos+token[1]]
            pos += token[1]
        if code == 'REM':
            sz = int(data['extra'][code]['length'])
            data['extra'][code]['remark'] = extra[pos:pos+int(sz)]
            pos += sz