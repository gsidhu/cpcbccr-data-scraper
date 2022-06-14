# CPCBCCR Data Scraper – setup_pull.py
# Author: Gurjot Sidhu (github.com/gsidhu)
# Thanks to: Thejesh GN (github.com/thejeshgn)
#
# This script reads the JSON response and populates the data table.

import sqlite3
import json

con = sqlite3.connect('../data/db/data.db')
cur = con.cursor()
query = "SELECT state, city, site, site_name, query_name, json_data FROM request_status_data WHERE parsed = 0 AND status_code = 200"

parameters_in_order = ['PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3', 'SO2', 'CO', 'Ozone', 'Benzene', 'Toluene', 'Eth-Benzene', 'MP-Xylene', 'RH', 'WD', 'SR', 'BP', 'AT', 'TOT-RF', 'RF', 'Xylene', 'WS', 'O Xylene', 'Temp', 'P-Xylene', 'VWS', 'Rack Temp']
# sql_query = "INSERT INTO data('city','site_name','site','state','query_name','to_date','to_time','from_date','from_time','PM2.5','PM10','NO','NO2','NOx','NH3','SO2','CO','Ozone','Benzene','Toluene','Eth-Benzene','MP-Xylene','RH','WD','SR','BP','AT','TOT-RF','RF','Xylene','WS','O Xylene','Temp','P-Xylene','VWS','Rack Temp') VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
sql_query = "INSERT INTO data VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
cursor = cur.execute(query)
row = cursor.fetchone()
prev_query = ''
while row:
    state = row[0]
    city = row[1]
    site = row[2]
    site_name = row[3]
    query_name = row[4]
    json_data = json.loads(row[5])

    # stopping the while loop
    if query_name != prev_query:
        prev_query = query_name
    else:
        break
    print(query_name)

    if json_data["status"] == "failed":
        print("moving on")
        # update parsed status
        parsed_query = "UPDATE request_status_data SET parsed = 1 WHERE query_name='" + query_name + "'"
        cur.execute(parsed_query)
        con.commit()
        # move to next row
        cur = con.cursor()
        cursor = cur.execute(query)
        row = cursor.fetchone()
        continue

    try:
        raw_data = json_data["data"]["tabularData"]
        body = raw_data["bodyContent"]
        records = []
        for i in range(len(body)):
            from_date = body[i]['from date'].split(' - ')[0]
            from_time = body[i]['from date'].split(' - ')[1]
            to_date = body[i]['to date'].split(' - ')[0]
            to_time = body[i]['to date'].split(' - ')[1]
            insert_record = [city,site_name,site,state,query_name,to_date,to_time,from_date,from_time]
            for p in parameters_in_order:
                # try to read the value from json
                try:
                    value = body[i][p]
                except:
                    value = None # assign None type if param is missing
                # insert numbers as float and others as is
                try:
                    insert_record.append(float(value))
                except:
                    insert_record.append(value)
            records.append(tuple(insert_record))

        # insert parsed rows
        cur.executemany(sql_query, records)

        # update parsed status
        parsed_query = "UPDATE request_status_data SET parsed = 1 WHERE query_name='" + query_name + "'"
        cur.execute(parsed_query)
        con.commit()
    except:
        pass

    # move to next row
    cur = con.cursor()
    cursor = cur.execute(query)
    row = cursor.fetchone()

con.close()