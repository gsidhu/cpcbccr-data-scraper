// CPCBCCR Data Scraper – cpcb_station_params.js
// Author: Gurjot Sidhu (github.com/gsidhu)
// 
// This script loads the CPCB dashboard and iteratively saves the list of parameters for each station listed in sites.json

import fs from 'fs';
import playwright from 'playwright';

let URL = "https://app.cpcbccr.com/ccr/#/caaqm-dashboard-all/caaqm-landing/caaqm-comparison-data"

let sites = JSON.parse(fs.readFileSync('./sites.json', 'utf8'));
let result = []

const INPUT = ".filter > input:nth-child(1)"
const PARAMS_LI = 'li.pure-checkbox'

const STATE_SELECTOR = "body > app-root > app-caaqm-dashboard > div.container-fluid > div > main > section > app-caaqm-view-data > div > div > div:nth-child(1) > div:nth-child(1) > div > ng-select > div > div > div.toggle"
const CITY_SELECTOR = "body > app-root > app-caaqm-dashboard > div.container-fluid > div > main > section > app-caaqm-view-data > div > div > div:nth-child(1) > div:nth-child(2) > div > ng-select > div > div > div.toggle"
const STATION_SELECTOR = "body > app-root > app-caaqm-dashboard > div.container-fluid > div > main > section > app-caaqm-view-data > div > div > div:nth-child(2) > div:nth-child(1) > div > ng-select > div > div > div.toggle"

async function pullData(i, state, city, siteName) {
  // Enter STATE
  await page.click(STATE_SELECTOR);
  await page.click(INPUT)
  await page.keyboard.type(state)
  await page.keyboard.press('Enter')

  // Enter CITY
  await page.click(CITY_SELECTOR);
  await page.click(INPUT)
  await page.keyboard.type(city)
  await page.keyboard.press('Enter')

  // Select Station
  await page.click(STATION_SELECTOR);
  await page.click(INPUT)
  await page.keyboard.type(siteName)
  await page.keyboard.press('Enter')

  // Download Parameters list for station
  // let LIST_PARAMS = []
  let LIS = await page.locator(PARAMS_LI)
  let LIST_PARAMS = await LIS.allInnerTexts()
  let NEW_PARAMS = []
  for (var i=0; i<LIST_PARAMS.length; i++) {
    NEW_PARAMS.push(LIST_PARAMS[i].trim())
  }
  // console.log(NEW_PARAMS)

  // await page.waitForTimeout(5000)

  return NEW_PARAMS
}

let browser = await playwright.chromium.launch({ headless: true, acceptDownloads: true });
const page = await browser.newPage();
await page.goto(URL)
await page.waitForLoadState();

for (var i=0; i < sites.length; i++) {
  console.log(sites[i]["site_name"])

  let newParams = await pullData(i, sites[i]["state"], sites[i]["city"], sites[i]["site_name"])
  let temp = {
    "state": sites[i]["state"],
    "city": sites[i]["city"],
    "site": sites[i]["site"],
    "site_name": sites[i]["site_name"],
    "params": newParams,
    "params_query": "",
    "params_ids": "",
    "data_availability": ""
  }
  result.push(temp)
}

fs.appendFile('./sites_with_params.json', JSON.stringify(result), function (err) {
  if (err) return console.log(err);
});

await browser.close();
