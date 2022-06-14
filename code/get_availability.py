# CPCBCCR Data Scraper – get_availability.py
# Author: Gurjot Sidhu (github.com/gsidhu)
# Thanks to: Thejesh GN (github.com/thejeshgn)
#
# This script gets the list of months for which data is available for a certain site and stores it the data_availability column in the sites table of the db.
# This data is parsed using check_availability.py

import requests
import dataset
import json
import base64

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:100.0) Gecko/20100101 Firefox/100.0',
    'Accept': 'q=0.8;application/json;q=0.9',
    'Accept-Language': 'en-GB,en-US;q=0.7,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://app.cpcbccr.com/ccr/',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://app.cpcbccr.com',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-GPC': '1',
    'TE': 'trailers',
}

db = dataset.connect("sqlite:///../data/db/data.db")
site_table = db["sites"]

for site_row in site_table:
    site = site_row["site"]
    state = site_row["state"]
    city = site_row["city"]
    print(site)
    query = {"state": state, "city": city, "station_id": site}
    data = base64.b64encode(str(query).replace("'", '"').encode("UTF8"))
    print(data)

    response = requests.post('https://app.cpcbccr.com/caaqms/Year_summarization', headers=headers, data=data)
    raw_json = json.dumps(response.json())
    site_row["data_availability"] = raw_json

    site_table.update(site_row, ["site"])

db.commit()
