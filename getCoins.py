#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 13:21:45 2021

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




link = "https://www.getcoins.com/locations/#"

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
time.sleep(10)
count = 0
html = browser.page_source
soup = BeautifulSoup(html, 'lxml')
linklist = []
df = pd.DataFrame()
while (html.find("bitcoin-atm.html") != -1):
    html = html[html.find("bitcoin-atm.html"):]
    index = html.find('"')
    link = html[:index]
    html = html[index:]
    finalink = "https://www.getcoins.com/locations/" + link
    linklist.append(finalink)

for element in linklist:
    browser.get(element)
    time.sleep(2)
    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')
    allres = soup.findAll("div", {"class": "listing-item-inner"})
    for item in allres:
        item = str(item)
        firstindex = item.find("<h3>")
        item = item[firstindex + 4:]
        secondindex = item.find("<i>")
        name = item[:secondindex]
        item = item[secondindex:]
        item = item[item.find("<span>") + 6:]
        address = item[:item.find("</span>")]
    
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
        nameIndex = name.find("-")
        name = name[nameIndex+1:]
        
        
        
        df1 = pd.DataFrame({'ATM Company' : ['GetCoins'],'Name' : [name], 'Street' : [street], 'State' : [state], 'Zip Code' : [zipCode],'Scrape Date' : [today]})
        
        df = df.append(df1)
        count = count + 1
        print(df1.head())
        
        
        


df.to_sql('atm_data', conn, index = False, if_exists= 'append')
dfCount = pd.DataFrame({'ATM Count' : [count], 'Date' : [today], 'ATM Company' : ['Get Coins']})
dfCount.to_sql('atm_scrape_data', conn, index = False, if_exists= 'append')

con.close()
browser.quit()
