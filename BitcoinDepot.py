#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  2 22:54:57 2021

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
from bs4 import BeautifulSoup
import time
from selenium import webdriver
import pandas as pd
import psycopg2
from datetime import date
from sqlalchemy import create_engine

statearray = ["Alabama","Arizona","Arkansas","California","Colorado","Connecticut"
,"Delaware","Florida","Georgia","Hawaii","Idaho","Illinois","Indiana","Iowa"
,"Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi"
,"Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota"
,"Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina"
,"South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia"
,"Wisconsin","Wyoming"]

con=psycopg2.connect(dbname= 'cryptomap', host='redshift-cluster-corpbond.cdnvikbx1dtu.us-east-1.redshift.amazonaws.com', 
port= '5439', user= 'nmehta', password= 'NMUmkx9T')

conn =  create_engine('postgresql://nmehta:NMUmkx9T@redshift-cluster-corpbond.cdnvikbx1dtu.us-east-1.redshift.amazonaws.com:5439/cryptomap')
today = date.today()
link = "https://bitcoindepot.com/locations/"

options = webdriver.ChromeOptions()        
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--ignore-certificate-errors')
options.add_argument('--headless')
options.add_argument('--incognito')
#ChromeDriver 88.0.4324.96 mac64
DRIVER_PATH = './selenium_driver/chromedriver'

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }



browser = webdriver.Chrome(options = options, executable_path = DRIVER_PATH)
browser.get(link)
time.sleep(10)
html = browser.page_source

soup = BeautifulSoup(html, 'lxml')

find1 = soup.findAll("div",{"class":"list-country-card"})
find2 = soup.findAll("div",{"class":"list-country-answer"})
find3 = soup.findAll("ul",{"class":"list-country-list"})

find_all_locations = soup.findAll("a",{"class":"list-country-list-link"})

singleData = []

count = 0
df = pd.DataFrame()
for element in find_all_locations:

    location_element = element.find("span", class_= "list-country-list-text")
    time_element = element.find("span", class_= "list-country-list-time")
    
    location_data = str(location_element)[str(location_element).find(">")+1:]
    location_data = location_data[:location_data.find("<")]
    #remove the rightmost comma, due to old & new locations different pattern
    location_data = location_data.rstrip(',')
    location_data = location_data.lstrip(',')
    location_data = location_data.split(",")
    
    location_name = re.sub(r"^\s+","",location_data[0])
    location_address = re.sub(r"^\s+","",location_data[1])
    
    
    
    hour = str(time_element)[str(time_element).find(">")+1:]
    hour = hour[:hour.find("<")]
    # for opening hours contain two lines, combine into one line
    hour = hour.replace("\n"," ")
    hour = hour.replace(","," ")
    if hour == "Non":
        hour = "None Available"
    
    #append all atm information from the page, old and new, most new atms don't have hours available
    singleData.append([location_name,location_address,hour])
    df1 = pd.DataFrame({'ATM Company' : ['BitCoin Depot'],'Name' : [location_name], 'Street' : [location_address], 'State' : ["N/A"], 'Zip Code' : ["N/A"],'Scrape Date' : [today]})
    df = df.append(df1)
    count = count + 1
    print(df1.head())
    
df.to_sql('atm_data', conn, index = False, if_exists= 'append')
dfCount = pd.DataFrame({'ATM Count' : [count], 'Date' : [today], 'ATM Company' : ['Bitcoin Depot']})
dfCount.to_sql('atm_scrape_data', conn, index = False, if_exists= 'append')
con.close()
browser.quit()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
