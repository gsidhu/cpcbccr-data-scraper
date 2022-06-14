# CPCBCCR Data Scraper – expedite.py
# Author: Gurjot Sidhu (github.com/gsidhu)
# Thanks to: Thejesh GN (github.com/thejeshgn)
#
# This script populates the params_query and params_ids fields in the sites table in db.
# This saves a little bit of time when generating the search queries using setup_pull.py

import dataset

def create_params_query(params_list):
    # '[{"id":0,"itemName":"PM2.5","itemValue":"parameter_193"},{"id":1,"itemName":"PM10","itemValue":"parameter_215"}'
    result = []
    for i in range(len(params_list)):
        param_dict = {"id": i}
        param_dict['itemName'] = params_list[i]
        param_dict['itemValue'] = PARAMS_MAP[params_list[i]]
        result.append(param_dict)
    result = str(result)
    result = result.replace("'", '"')
    result = result.replace('", "', '","')
    return result

def give_params_ids(params_list):
    # '["parameter_193","parameter_215"]'
    result = []
    for i in params_list:
        result.append(PARAMS_MAP[i])
    result = str(result)
    result = result.replace("'", '"')
    return result

PARAMS_MAP = {"PM2.5": "parameter_193", "PM10": "parameter_215", "NO": "parameter_226", "NO2": "parameter_194", "NOx": "parameter_225", "NH3": "parameter_311", "SO2": "parameter_312", "CO": "parameter_203", "Ozone": "parameter_222", "Benzene": "parameter_202", "Toluene": "parameter_232", "Eth-Benzene": "parameter_216", "MP-Xylene": "parameter_240", "RH": "parameter_235", "WD": "parameter_234", "SR": "parameter_237", "BP": "parameter_238", "AT": "parameter_204", "TOT-RF": "parameter_37", "RF": "parameter_236", "Xylene": "parameter_223", "WS": "parameter_233", "O Xylene": "parameter_241", "Temp": "parameter_198", "VWS": "parameter_239", "P-Xylene": "parameter_324", "Rack Temp": "parameter_218"}

db = dataset.connect("sqlite:///../data/db/data.db")
site_table = db["sites"]
run_name = "run2_"  # leave this as it is

for site_row in site_table:
    site = site_row["site"]
    params_list = site_row["params"].replace("\\","").strip("]['").split(", ") # converts str of list back to list
    params_list = params_list[0].split(',') # converts str of list back to list

    params_query = create_params_query(params_list)
    params_ids = give_params_ids(params_list)

    site_row["params_query"] = params_query
    site_row["params_ids"] = params_ids

    site_table.update(site_row, ["site"])
    db.commit()