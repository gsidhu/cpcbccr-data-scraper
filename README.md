# CPCBCCR Data Scraper
Scrapes data from CPCB's CCR dashboard.

## Disclaimer
The work in this repo builds on top of the [work done by Thejesh GN](https://github.com/thejeshgn/cpcbccr). I take no responsibility for Thej's work and Thej takes no responsibility for the work I have done in this repo. Please contact individual authors for any queries.

## Code
This code uses the [`data.db`](./data/db/data.db) file for everything. 

First order of business is to set up the **sites** table in the db.

### 1. How to set up sites in DB
**Add your sites to CSV**

1. Go to [CPCB's CCR website](https://app.cpcbccr.com/ccr/#/caaqm-dashboard-all/caaqm-landing/data) and select the state, city and station of your choice.
2. Open the Network tab in Dev Tools and click 'Submit' on the webpage.
3. In the Network tab, click on the POST request called `fetch_table_data`. Under the Request tab you'll see the payload of the request. Scroll to `filtersToApply > parameterNames > station` and copy the station code which should look something like - `site_123`.
4. Edit [`sites.csv`](./sites.csv) and add the _state_, _city_, _site_ and _site_name_.
5. Leave the header row as is. Leave the remaining columns blank.

**Get available parameters for each site**
1. Use csvjson.com's [csv2json](https://csvjson.com/csv2json) tool to create a [`sites.json`](./sites.json) file out of your edited `sites.csv`. Save that JSON in your root directory.
2. Run `yarn` or `npm install` in your root directory.
3. Run `node cpcb_station_params.js` and you'll get a [`sites_with_params.json`](./sites_with_params.json) file which expands `sites.json` by adding the list of available parameters for each site.
4. Use csvjson.com's [json2csv](https://csvjson.com/json2csv) tool to create a CSV and save it as [`sites_with_params.csv`](./sites_with_params.csv) in your root directory.

**Add the sites data to db**
1. Download and install a tool like [DB Browser for SQLite](https://sqlitebrowser.org/)
2. Open the [`data.db`](./data/db/data.db) file using DB Browser
3. Click on Import > Table from CSV and select the `sites_with_params.csv` file from before. Save this table named as **sites**. You can delete the pre-existing sites table to replace it.

### 2. Scrape the data
Now that your sites are set up, you can begin to scrape data.

0. Use python3 and install the `requests`, `dataset` and `sqlite3` modules using pip. (Ideally inside a [virtualenv](https://python.land/virtual-environments/virtualenv) using [`requirements.txt`](./requirements.txt))

Run the following scripts in the given order –
1. `get_availability.py`: gets the months for which data is available for each site
2. `check_availability.py`: parses the JSON response from #1 into a list
3. `expedite.py`: populates the *params_query* and *params_ids* columns in the **sites** table
4. `setup_pull.py`: edit this script to setup the dates for which you need to get data ([lines 37-39](https://github.com/gsidhu/cpcbccr/blob/master/code/setup_pull.py#L37)); running this script sets up all the requests that needs to be called to pull the data
5. `pull.py`: pulls the data setup in the previous script; data received is a JSON.
6. `parse.py`: parses the JSON data and creates the final **data** table in db

## Notes
While all scripts should run quite swiftly, `pull.py` is going to be the slowest. Pinging the CPCB server takes time so be patient. And be kind and leave some timeout between subsequent pings.

You can browse the data for all stations in Delhi, Mumbai and Chennai from 01-01-2010 till 31-12-2020 in the [reports](./data/reports/) directory. No need to fetch that again.

## License
- This code is licensed under GNU GPL v3.
- Please credit by linking to https://thatgurjot.com and https://thejeshgn.com