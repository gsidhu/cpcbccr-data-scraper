# CPCBCCR Data Scraper – check_availability.py
# Author: Gurjot Sidhu (github.com/gsidhu)
# Thanks to: Thejesh GN (github.com/thejeshgn)
#
# This script reads the JSON data from data_availability column and rewrites it as a list with MM-YYYY elements.

# sample_raw_json = '{"header": ["Year", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], "body": [[{"value": "2022"}, {"value": "NA", "color": "#f3f3f3"}, {"value": "NA", "color": "#f3f3f3"}, {"value": "NA", "color": "#f3f3f3"}, {"value": "NA", "color": "#f3f3f3"}, {"value": "NA", "color": "#f3f3f3"}, {"value": "NA", "color": "#f3f3f3"}, {"value": "NA", "color": "#f3f3f3"}, {"value": "NA", "color": "#f3f3f3"}, {"value": "NA", "color": "#f3f3f3"}, {"value": "NA", "color": "#f3f3f3"}, {"value": "NA", "color": "#f3f3f3"}, {"value": "NA", "color": "#f3f3f3"}], [{"value": "2021"}, {"value": 31, "color": "#00b050"}, {"value": 27, "color": "#00b050"}, {"value": 31, "color": "#00b050"}, {"value": "NA", "color": "#f3f3f3"}, {"value": "NA", "color": "#f3f3f3"}, {"value": "NA", "color": "#f3f3f3"}, {"value": "NA", "color": "#f3f3f3"}, {"value": "NA", "color": "#f3f3f3"}, {"value": "NA", "color": "#f3f3f3"}, {"value": "NA", "color": "#f3f3f3"}, {"value": "NA", "color": "#f3f3f3"}, {"value": "NA", "color": "#f3f3f3"}], [{"value": "2020"}, {"value": 31, "color": "#00b050"}, {"value": 29, "color": "#00b050"}, {"value": 31, "color": "#00b050"}, {"value": 30, "color": "#00b050"}, {"value": 31, "color": "#00b050"}, {"value": 30, "color": "#00b050"}, {"value": 31, "color": "#00b050"}, {"value": 31, "color": "#00b050"}, {"value": 31, "color": "#00b050"}, {"value": 31, "color": "#00b050"}, {"value": 31, "color": "#00b050"}, {"value": 31, "color": "#00b050"}], [{"value": "2019"}, {"value": 31, "color": "#00b050"}, {"value": 28, "color": "#00b050"}, {"value": 31, "color": "#00b050"}, {"value": 30, "color": "#00b050"}, {"value": 31, "color": "#00b050"}, {"value": 30, "color": "#00b050"}, {"value": 31, "color": "#00b050"}, {"value": 31, "color": "#00b050"}, {"value": 30, "color": "#00b050"}, {"value": 31, "color": "#00b050"}, {"value": 30, "color": "#00b050"}, {"value": 30, "color": "#00b050"}], [{"value": "2018"}, {"value": 31, "color": "#00b050"}, {"value": 28, "color": "#00b050"}, {"value": 31, "color": "#00b050"}, {"value": 30, "color": "#00b050"}, {"value": 31, "color": "#00b050"}, {"value": 30, "color": "#00b050"}, {"value": 31, "color": "#00b050"}, {"value": 31, "color": "#00b050"}, {"value": 30, "color": "#00b050"}, {"value": 31, "color": "#00b050"}, {"value": 30, "color": "#00b050"}, {"value": 31, "color": "#00b050"}], [{"value": "2017"}, {"value": 31, "color": "#00b050"}, {"value": 28, "color": "#00b050"}, {"value": 31, "color": "#00b050"}, {"value": 30, "color": "#00b050"}, {"value": 31, "color": "#00b050"}, {"value": 30, "color": "#00b050"}, {"value": 31, "color": "#00b050"}, {"value": 22, "color": "#00b050"}, {"value": 30, "color": "#00b050"}, {"value": 31, "color": "#00b050"}, {"value": 30, "color": "#00b050"}, {"value": 29, "color": "#00b050"}], [{"value": "2016"}, {"value": 28, "color": "#00b050"}, {"value": 29, "color": "#00b050"}, {"value": 31, "color": "#00b050"}, {"value": 30, "color": "#00b050"}, {"value": 31, "color": "#00b050"}, {"value": 16, "color": "#ff9900"}, {"value": 21, "color": "#00b050"}, {"value": 26, "color": "#00b050"}, {"value": 30, "color": "#00b050"}, {"value": 31, "color": "#00b050"}, {"value": 30, "color": "#00b050"}, {"value": 21, "color": "#00b050"}], [{"value": "2015"}, {"value": 31, "color": "#00b050"}, {"value": 28, "color": "#00b050"}, {"value": 31, "color": "#00b050"}, {"value": 30, "color": "#00b050"}, {"value": 31, "color": "#00b050"}, {"value": 30, "color": "#00b050"}, {"value": 30, "color": "#00b050"}, {"value": 31, "color": "#00b050"}, {"value": 30, "color": "#00b050"}, {"value": 31, "color": "#00b050"}, {"value": 30, "color": "#00b050"}, {"value": 16, "color": "#ff9900"}], [{"value": "2014"}, {"value": 30, "color": "#00b050"}, {"value": 27, "color": "#00b050"}, {"value": 31, "color": "#00b050"}, {"value": 26, "color": "#00b050"}, {"value": 31, "color": "#00b050"}, {"value": 30, "color": "#00b050"}, {"value": 31, "color": "#00b050"}, {"value": 23, "color": "#00b050"}, {"value": 30, "color": "#00b050"}, {"value": 25, "color": "#00b050"}, {"value": 28, "color": "#00b050"}, {"value": 29, "color": "#00b050"}], [{"value": "2013"}, {"value": 23, "color": "#00b050"}, {"value": 23, "color": "#00b050"}, {"value": 23, "color": "#00b050"}, {"value": 10, "color": "#ff0000"}, {"value": 18, "color": "#ff9900"}, {"value": 27, "color": "#00b050"}, {"value": 31, "color": "#00b050"}, {"value": 19, "color": "#ff9900"}, {"value": 30, "color": "#00b050"}, {"value": 23, "color": "#00b050"}, {"value": 20, "color": "#ff9900"}, {"value": 29, "color": "#00b050"}], [{"value": "2012"}, {"value": 31, "color": "#00b050"}, {"value": 29, "color": "#00b050"}, {"value": 31, "color": "#00b050"}, {"value": 30, "color": "#00b050"}, {"value": 31, "color": "#00b050"}, {"value": 30, "color": "#00b050"}, {"value": 31, "color": "#00b050"}, {"value": 31, "color": "#00b050"}, {"value": 30, "color": "#00b050"}, {"value": 23, "color": "#00b050"}, {"value": 4, "color": "#ff0000"}, {"value": 16, "color": "#ff9900"}], [{"value": "2011"}, {"value": 29, "color": "#00b050"}, {"value": 28, "color": "#00b050"}, {"value": 25, "color": "#00b050"}, {"value": 15, "color": "#ff9900"}, {"value": 18, "color": "#ff9900"}, {"value": 29, "color": "#00b050"}, {"value": 7, "color": "#ff0000"}, {"value": "NA", "color": "#f3f3f3"}, {"value": "NA", "color": "#f3f3f3"}, {"value": 21, "color": "#00b050"}, {"value": 30, "color": "#00b050"}, {"value": 14, "color": "#ff9900"}], [{"value": "2010"}, {"value": 31, "color": "#00b050"}, {"value": 27, "color": "#00b050"}, {"value": 31, "color": "#00b050"}, {"value": 29, "color": "#00b050"}, {"value": 31, "color": "#00b050"}, {"value": 12, "color": "#ff9900"}, {"value": "NA", "color": "#f3f3f3"}, {"value": 5, "color": "#ff0000"}, {"value": 30, "color": "#00b050"}, {"value": 2, "color": "#ff0000"}, {"value": 30, "color": "#00b050"}, {"value": 31, "color": "#00b050"}], [{"value": "2009"}, {"value": "NA", "color": "#f3f3f3"}, {"value": 15, "color": "#ff9900"}, {"value": 31, "color": "#00b050"}, {"value": 30, "color": "#00b050"}, {"value": 31, "color": "#00b050"}, {"value": 30, "color": "#00b050"}, {"value": 29, "color": "#00b050"}, {"value": 31, "color": "#00b050"}, {"value": 30, "color": "#00b050"}, {"value": 31, "color": "#00b050"}, {"value": 30, "color": "#00b050"}, {"value": 29, "color": "#00b050"}]], "selectedData": {"selectedState": "Tamil Nadu", "selectedCity": "Chennai", "selectedStation": "site_288", "selectedStationName": "Velachery Res. Area, Chennai - CPCB"}, "status": "success"}'

import json
import dataset 

db = dataset.connect("sqlite:///../data/db/data.db")
site_table = db["sites"]

for site_row in site_table:
    site = site_row['site']
    raw_json = site_row["data_availability"]
    json_data = json.loads(raw_json)

    body = json_data['body']
    years = []
    data_available = []
    for row in body:
      year = row[0]['value']
      years.append(year)
      for i in range(1,13):
        if row[i]['value'] != 'NA':
          if i < 10:
            m = '0' + str(i)
          else:
            m = str(i)
          data_available.append(m + '-' + year)

    site_row["data_availability"] = str(data_available)
    site_table.update(site_row, ["site"])

db.commit()


