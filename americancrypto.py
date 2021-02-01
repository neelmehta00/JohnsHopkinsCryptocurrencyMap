#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 15:46:07 2021

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




statearray = ["Arizona","California","Colorado"
,"Delaware","Florida","Georgia","Illinois","Indiana","Iowa"
,"Kansas","Kentucky","Maryland","Massachusetts","Michigan","Minnesota","Mississippi"
,"Missouri","Montana","Nebraska","Nevada","New-Jersey","New-Mexico","North-Carolina","North-Dakota"
,"Ohio","Pennsylvania","South-Carolina"
,"Tennessee","Texas","Virginia","West-Virginia"
,"Wisconsin"]
print(len(statearray))

first = "https://www.digitalmint.io/"
last = "-bitcoin-atm/"
linklist = []
for item in statearray:
    linklist.append(first+item+last)


#making the file start
filename = "diigitalmint.csv"
f = open(filename, "w")

headers = "Store Name, Address\n"
f.write(headers)
#end of making the file

browser = webdriver.Chrome(options=options,executable_path=DRIVER_PATH)

for element in linklist:
    browser.get(element)
    time.sleep(2)
    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')
    allres = soup.findAll("div", {"class": "column is-6 state-container"})
    #print(allres[0])
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
        address = firstAddress+secondAddress
        readdress = ""
        for ch in address:
            if ch == ",":
                ch = " "
            readdress = readdress + ch
            
                
                
        f.write(name + "," + readdress + "\n")
        
        print(name)
        print(readdress)
        
    
f.close()