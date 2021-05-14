#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 09:30:01 2021

@author: neelmehta
"""
from bs4 import BeautifulSoup
import requests
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from selenium import webdriver
from selenium.common import exceptions
import urllib
from selenium.webdriver.common.keys import Keys
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import date

import firebase_admin
from firebase_admin import credentials
import os
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="JHUCryptoMap.json"
today = date.today()

#default_app = firebase_admin.initialize_app()

#db = firestore.client()
from sqlalchemy import create_engine
import pandas as pd
import psycopg2

con=psycopg2.connect(dbname= 'cryptomap', host='redshift-cluster-corpbond.cdnvikbx1dtu.us-east-1.redshift.amazonaws.com', 
port= '5439', user= 'nmehta', password= 'NMUmkx9T')


conn =  create_engine('postgresql://nmehta:NMUmkx9T@redshift-cluster-corpbond.cdnvikbx1dtu.us-east-1.redshift.amazonaws.com:5439/cryptomap')


statearray = ["Alabama","Arizona","Arkansas","California","Colorado","Connecticut"
,"Delaware","Florida","Georgia","Hawaii","Idaho","Illinois","Indiana","Iowa"
,"Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi"
,"Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota"
,"Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina"
,"South Dakota"
,"Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia"
,"Wisconsin","Wyoming"]

link = "https://www.coincloudatm.com/atms"

options = webdriver.ChromeOptions()        
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
#options.add_argument('--headless')
DRIVER_PATH = '/Users/neelmehta/Downloads/chromedriver 3'
headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }


count = 0
browser = webdriver.Chrome(options=options,executable_path=DRIVER_PATH)
df = pd.DataFrame()

for element in statearray:
    browser.get(link)
    time.sleep(2)
    inputloc = browser.find_element_by_xpath('//*[@id="autocompleteList"]')
    inputloc.send_keys(element)
    time.sleep(2)
    inputloc.send_keys(Keys.ARROW_DOWN)
    inputloc.send_keys(Keys.ENTER)
    #button = browser.find_element_by_xpath('//*[@id="bh-sl-submit"]')
    #button.click()
    time.sleep(2)
    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')
    allelements = soup.findAll("div", {"class": "card-map mapresults__cards-item"})
    storename = soup.findAll("h3", {"class": "display-5 company-name"})
    info = soup.findAll("p", {"class": "display-6 grey-text"})
    
    atmName = 'CoinCloud ' + str(today)
    for i in range(len(storename)):
        
        address = str(info[i])
        
        name = str(storename[i])
        
        
        name = name[name.find(">") + 1:]
        name = name[:name.find("<")]
        
        address = address[address.find(">") + 1:]
        address = address[:address.find("<")]
        realadd = ""
        for ch in address:
            if ch == ",":
                ch = " "
            realadd = realadd + ch
            
        address = realadd
        zipCode = address[-5:]
        stateIndex = address.rfind(" ",0,len(address)-6)
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
        
        df1 = pd.DataFrame({'ATM Company' : ['CoinCloud'],'Name' : [name], 'Street' : [street], 'State' : [state], 'Zip Code' : [zipCode], 'Scrape Date' : [today]})
        
        df = df.append(df1)
       
        count = count + 1
        
       
df.to_sql('atm_data', conn, index = False, if_exists= 'append')
dfCount = pd.DataFrame({'ATM Count' : [count], 'Date' : [today], 'ATM Company' : ['Coin Cloud']})
dfCount.to_sql('atm_scrape_data', conn, index = False, if_exists= 'append')



con.close()


