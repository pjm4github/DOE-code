# from gov_pnnl_goss.gridlab.climate.Climate import Climate
# from gov_pnnl_goss.gridlab.climate.CsvReader import CsvReader
# from gov_pnnl_goss.gridlab.climate.Weather import Weather
# from gov_pnnl_goss.gridlab.gldcore.Globals import EINVAL
# from gov_pnnl_goss.gridlab.gldcore.GridLabD import set_callback
#
#
# # see the gridlabd utilities/ add_class shell script
#
# def init(fntable, module, argc, *argv):
#     if not set_callback(fntable):
#         errno = EINVAL
#         return None
#
#     climate = Climate(module)
#     weather = Weather(module)
#     csv_reader = CsvReader(module)
#
#     # /* always return the first class registered */
#     return climate.owner_class
#
#
# def do_kill():
#     # if global memory needs to be released, this is a good time to do it */
#     return 0
#
#
# def check():
#     # if any climate objects have bad filenames, they'll fail on init() */
#     return 0
