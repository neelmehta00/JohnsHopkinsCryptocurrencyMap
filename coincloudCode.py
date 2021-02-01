#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 16:15:30 2021

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
DRIVER_PATH = '/Users/neelmehta/Downloads/chromedriver'
headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

#making the file start
filename = "coinCloud.csv"
f = open(filename, "w")

headers = "Store Name, Address\n"
f.write(headers)
#end of making the file

browser = webdriver.Chrome(options=options,executable_path=DRIVER_PATH)
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
    print(storename[0])
    print(info[0])
    for i in range(len(storename)):
        
        address = str(info[i])
        
        name = str(storename[i])
        name = name[name.find("http"):]
        name = name[name.find(">") + 1:]
        name = name[:name.find("</a>")]
        address = address[address.find(">") + 1:]
        address = address[:address.find("<")]
        realadd = ""
        for ch in address:
            if ch == ",":
                ch = " "
            realadd = realadd + ch
            
        print(name)
        print(realadd)
        f.write(name + "," + realadd + "\n")
f.close()