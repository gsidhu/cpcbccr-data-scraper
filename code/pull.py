# CPCBCCR Data Scraper – setup_pull.py
# Author: Gurjot Sidhu (github.com/gsidhu)
# Thanks to: Thejesh GN (github.com/thejeshgn)
#
# This script sends the encoded requests to the CPCBCCR server and stores the JSON response in the request_status_data table.

import requests
import json
import sqlite3
import hashlib
import time
import warnings
warnings.filterwarnings("ignore") # just to ignore the SSL warning

headers = {"Origin": "https://app.cpcbccr.com"}
headers["Accept-Encoding"] = "gzip, deflate, br"
headers["Accept-Language"] = "en-GB,en-US;q=0.9,en;q=0.8"
headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36"
headers["Content-Type"] = "application/x-www-form-urlencoded"
headers["Accept"] = "application/json, text/plain, */*"
headers["Referer"] = "https://app.cpcbccr.com/ccr/"
headers["Connection"] = "keep-alive"
headers["Host"] = "app.cpcbccr.com"

con = sqlite3.connect('../data/db/data.db')
cur = con.cursor()
query = "SELECT id, encoded_data FROM request_status_data WHERE status_code = 1 OR status_code = 404 LIMIT 15"
n = 0
while n < 8230:
  sample = []
  for r in cur.execute(query):
    sample.append(r)

  for row in sample:
    n = row[0]
    print(n)
    encoded_data = row[1]
    try:
      r = requests.post(
        "https://app.cpcbccr.com/caaqms/fetch_table_data",
        headers=headers,
        data=encoded_data,
        verify=False, # turning it on hangs the request randomly
      )
      # print(r.request.url)

      if r.status_code == 200:
        print("Awesome response code 200")
        json_data = json.dumps(r.json())
        json_data_hash = hashlib.md5(json_data.encode("UTF8"))
        json_data_hash = json_data_hash.hexdigest()
        status_code = r.status_code
      else:
        print("Response code %s", r.status_code)
        json_data = ""
        json_data_hash = ""
        status_code = r.status_code

      # print("UPDATING")
      cur.execute("UPDATE request_status_data SET json_data = ?, json_data_hash = ?, status_code = ? WHERE id=?", (json_data, json_data_hash, status_code, row[0]))
      con.commit()
    except:
      pass

    time.sleep(5)
con.close()
