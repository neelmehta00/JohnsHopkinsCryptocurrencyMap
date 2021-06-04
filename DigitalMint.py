#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 16:33:55 2021
@author: neelmehta
"""

from bs4 import BeautifulSoup
import time
from selenium import webdriver
import pandas as pd
import psycopg2
from datetime import date
from sqlalchemy import create_engine

today = date.today()


con=psycopg2.connect(dbname= 'cryptomap', host='redshift-cluster-corpbond.cdnvikbx1dtu.us-east-1.redshift.amazonaws.com', 
port= '5439', user= 'nmehta', password= 'NMUmkx9T')

conn =  create_engine('postgresql://nmehta:NMUmkx9T@redshift-cluster-corpbond.cdnvikbx1dtu.us-east-1.redshift.amazonaws.com:5439/cryptomap')
df = pd.DataFrame()


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



'''
statearray = ["Arizona","California","Colorado"
,"Delaware","Florida","Georgia","Illinois","Indiana","Iowa"
,"Kansas","Kentucky","Maryland","Massachusetts","Michigan","Minnesota","Mississippi"
,"Missouri","Montana","Nebraska","Nevada","New-Jersey","New-Mexico","North-Carolina","North-Dakota"
,"Ohio","Pennsylvania","South-Carolina"
,"Tennessee","Texas","Virginia","West-Virginia"
,"Wisconsin"]
'''
statearray = ["Alabama","Arizona","Arkansas","California","Colorado","Connecticut"
,"Delaware","Florida","Georgia","Hawaii","Idaho","Illinois","Indiana","Iowa"
,"Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi"
,"Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota"
,"Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina"
,"South Dakota"
,"Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia"
,"Wisconsin","Wyoming"]


first = "https://www.digitalmint.io/"
last = "-bitcoin-atm/"
linklist = []
for item in statearray:
    linklist.append(first+item+last)




browser = webdriver.Chrome(options=options,executable_path=DRIVER_PATH)
count = 0
for element in linklist:
    browser.get(element)
    time.sleep(2)
    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')
    allres = soup.findAll("div", {"class": "column is-6 state-container"})
    
    for i in range(len(allres)):
        item = str(allres[i])
        
        firstindex = item.find("<p>")
        item = item[firstindex + 3:]
        secondindex = item.find("</p>")
        name = item[:secondindex]
        
        item = item[secondindex:]
        item = item[item.find("<p class=") + 19:]
        address = item[:item.find("</p>")]
        removeIndex = address.find("<")
        
        remove2Index = address.find(">")+1
        firstAddress = address[:removeIndex]
        
        
        secondAddress = address[remove2Index:]
        firstAddress = firstAddress[9:]
        secondAddress = secondAddress[9:]
        secondAddress = secondAddress[:len(secondAddress)-7]
        
        
        address = firstAddress+ " " +secondAddress
        
        readdress = ""
        for ch in address:
            if ch == ",":
                ch = ""
            readdress = readdress + ch
        address = readdress
        zipCode = address[-5:]
        
        stateIndex = address.rfind(" ",0,len(address)-7)
        
        state = address[stateIndex+1:-5]
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
        
        street = address[:stateIndex]
        
        count = count + 1
        
        
        
        
        
        df1 = pd.DataFrame({'ATM Company' : ['DigitalMint'],'Name' : [name], 'Street' : [street], 'State' : [state], 'Zip Code' : [zipCode],'Scrape Date' : [today]})
        df = df.append(df1)
        print(df1.head())
df.to_sql('atm_data', conn, index = False, if_exists= 'append')
dfCount = pd.DataFrame({'ATM Count' : [count], 'Date' : [today], 'ATM Company' : ['Digital Mint']})
dfCount.to_sql('atm_scrape_data', conn, index = False, if_exists= 'append')
con.close()
browser.quit()
                

        

        
    
