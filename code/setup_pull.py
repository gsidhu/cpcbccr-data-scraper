# CPCBCCR Data Scraper – setup_pull.py
# Author: Gurjot Sidhu (github.com/gsidhu)
# Thanks to: Thejesh GN (github.com/thejeshgn)
#
# This script uses the data in the sites table to generate the search query for each site in the request_status_data table.

from datetime import datetime
from datetime import timedelta
import base64
import dataset

db = dataset.connect("sqlite:///../data/db/data.db")
# TODO 1: edit data/db/data.sqlite3 and add the sites you want to scrape into sites table
site_table = db["sites"]
run_name = "run2_"  # leave this as it is

for site_row in site_table:
    state = site_row["state"]
    city = site_row["city"]
    site = site_row["site"]
    site_name = site_row["site_name"]
    params_list = site_row["params"].strip("]['").split(", ") # converts str of list back to list because we want string quotes on elements
    params_query = site_row["params_query"]
    params_ids = site_row["params_ids"]
    data_availability = site_row["data_availability"].strip("]['").split("', '") # converts str of list back to list because we want string quotes on elements

    label = (
        state.lower().replace(" ", "")
        + "_"
        + city.lower().replace(" ", "-")
        + "_"
        + site
        + "_"
    )
    table = db["request_status_data"]

    fromDate = "01-01-2010"  # TODO 2: starting date (inclusive)
    endDate = "31-12-2020"  # TODO 3: ending date (inclusive)
    how_many_days = 10

    toDate = ""
    objFromDate = datetime.strptime(fromDate, "%d-%m-%Y")
    time_part = " T00:00:00Z"
    time_part_end = " T00:10:00Z"
    status_code = 1

    print(site_name)
    # print(data_availability)
    while objFromDate <= datetime.strptime(endDate, "%d-%m-%Y"):
        # print("####################################################")
        objToDate = objFromDate + timedelta(days=how_many_days)
        
        # stop if this month's data is not available
        current_month = objFromDate.strftime("%m-%Y")
        # print(current_month)
        if current_month not in data_availability:
            objFromDate = objToDate
            continue

        fromDate = objFromDate.strftime("%d-%m-%Y") + time_part
        toDate = objToDate.strftime("%d-%m-%Y") + time_part_end

        query_name = run_name + label + objFromDate.strftime("%Y%m%d")
        # print(query_name)
        
        ## this query slows the code
        ## its faster to just rewrite the data than check for existence
        # row_exists = table.find_one(query_name=query_name)
        # if row_exists:
        #     objFromDate = objToDate
        #     # print("EXISTS SO GO TO NEXT")
        #     continue

        prompt_all = (
            '{"draw":1,"columns":[{"data":0,"name":"","searchable":true,"orderable":false,"search":{"value":"","regex":false}}],"order":[],"start":0,"length":30,"search":{"value":"","regex":false},"filtersToApply":{"parameter_list":'
            + params_query
            + ',"criteria":"24 Hours","reportFormat":"Tabular","fromDate":"'
            + fromDate
            + '","toDate":"'
            + toDate
            + '","state":"'
            + state
            + '","city":"'
            + city
            + '","station":"'
            + site
            + '","parameter":'
            + params_ids
            + ',"parameterNames":'
            + str(params_list).replace("'", '"') # need double quotes for it to work
            + '},"pagination":1}'
        )

        data_to_encode = prompt_all
        encoded_data = base64.b64encode(data_to_encode.encode("UTF8"))
        # print(data_to_encode)

        row = {}
        row["query_name"] = query_name
        row["fromDate"] = fromDate
        row["toDate"] = toDate
        row["state"] = state
        row["city"] = city
        row["site"] = site
        row["site_name"] = site_name
        row["data_to_encode"] = data_to_encode
        row["encoded_data"] = encoded_data
        row["status_code"] = status_code
        row["parsed"] = 0
        table.insert(row)

        # forward in date for next
        objFromDate = objToDate
        # print("_______________________________________________________________")
        # end while
