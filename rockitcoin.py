
from bs4 import BeautifulSoup
import time
from selenium import webdriver
import pandas as pd
import psycopg2
from datetime import date
from sqlalchemy import create_engine


con=psycopg2.connect(dbname= 'cryptomap', host='redshift-cluster-corpbond.cdnvikbx1dtu.us-east-1.redshift.amazonaws.com', 
port= '5439', user= 'nmehta', password= 'NMUmkx9T')

conn =  create_engine('postgresql://nmehta:NMUmkx9T@redshift-cluster-corpbond.cdnvikbx1dtu.us-east-1.redshift.amazonaws.com:5439/cryptomap')

link = "https://rockitcoin.com/locations"

options = webdriver.ChromeOptions()        
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
DRIVER_PATH = './selenium_driver/chromedriver'
headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }



browser = webdriver.Chrome(options=options,executable_path=DRIVER_PATH)
browser.get(link)
time.sleep(5)
html = browser.page_source
soup = BeautifulSoup(html, 'lxml')
storename = soup.findAll("p", {"class": "loc-title"})
storeaddress = soup.findAll("p", {"class": "location-address"})

today = date.today()
count = 0
df = pd.DataFrame()
for i in range(len(storeaddress)):
    storeName = str(storename[i])
    address = str(storeaddress[i])
    storeName = storeName[storeName.find(">") + 1:]
    storeName = storeName[:storeName.find("<")]
    address = address[address.find(">") + 1:]
    street = address[:address.find("<")]
    
    state = address[address.find(">") + 2:]
    city= state[:state.find(" ")]
    #print(address)
    state = state[state.find(" ") + 1:]
    state = state[:state.find("USA") - 1]
    us_state_abbrev = {
            'Alabama': 'AL',
            'Alaska': 'AK',
            'American Samoa': 'AS',
            'Arizona': 'AZ',
            'Arkansas': 'AR',
            'California': 'CA',
            'Colorado': 'CO',
            'Connecticut': 'CT',
            'Delaware': 'DE',
            'District of Columbia': 'DC',
            'Florida': 'FL',
            'Georgia': 'GA',
            'Guam': 'GU',
            'Hawaii': 'HI',
            'Idaho': 'ID',
            'Illinois': 'IL',
            'Indiana': 'IN',
            'Iowa': 'IA',
            'Kansas': 'KS',
            'Kentucky': 'KY',
            'Louisiana': 'LA',
            'Maine': 'ME',
            'Maryland': 'MD',
            'Massachusetts': 'MA',
            'Michigan': 'MI',
            'Minnesota': 'MN',
            'Mississippi': 'MS',
            'Missouri': 'MO',
            'Montana': 'MT',
            'Nebraska': 'NE',
            'Nevada': 'NV',
            'New Hampshire': 'NH',
            'New Jersey': 'NJ',
            'New Mexico': 'NM',
            'New York': 'NY',
            'North Carolina': 'NC',
            'North Dakota': 'ND',
            'Northern Mariana Islands':'MP',
            'Ohio': 'OH',
            'Oklahoma': 'OK',
            'Oregon': 'OR',
            'Pennsylvania': 'PA',
            'Puerto Rico': 'PR',
            'Rhode Island': 'RI',
            'South Carolina': 'SC',
            'South Dakota': 'SD',
            'Tennessee': 'TN',
            'Texas': 'TX',
            'Utah': 'UT',
            'Vermont': 'VT',
            'Virgin Islands': 'VI',
            'Virginia': 'VA',
            'Washington': 'WA',
            'West Virginia': 'WV',
            'Wisconsin': 'WI',
            'Wyoming': 'WY'
        }
    abbrev_us_state = dict(map(reversed, us_state_abbrev.items()))
    if len(state) == 2:
        state = abbrev_us_state[state]
    
    street = street + city
    
    
    df1 = pd.DataFrame({'ATM Company' : ['Rockit Coin'],'Name' : [storeName], 'Street' : [street], 'State' : [state], 'Zip Code' : ["N/A"],'Scrape Date' : [today]})
    df = df.append(df1)
    count = count + 1
    print(df1.head())


df.to_sql('atm_data', conn, index = False, if_exists= 'append')
dfCount = pd.DataFrame({'ATM Count' : [count], 'Date' : [today], 'ATM Company' : ['Rockit Coin']})
dfCount.to_sql('atm_scrape_data', conn, index = False, if_exists= 'append')
con.close()
browser.quit()
