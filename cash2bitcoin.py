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

#making the file start
filename = "cash2bitcoin.csv"
f = open(filename, "w")
headers = "Store Name, Address, Phone\n"
f.write(headers)
#end of making the file
link = "https://www.cash2bitcoin.com/"
browser = webdriver.Chrome(options=options,executable_path=DRIVER_PATH)
browser.get(link)
time.sleep(10)
html = browser.page_source

soup = BeautifulSoup(html, 'lxml')

allres = soup.findAll("id", {"class": "storepoint-container"})
phone = soup.findAll("div", {"class": "storepoint-sidebar-phone"})
storeName = soup.findAll("div", {"class": "storepoint-name"})
address = soup.findAll("div", {"class": "storepoint-address"})
print(allres)

#list for all the data of one ATM
singleData = []
for elem in allres:
    elem = str(elem)
    elem = elem[elem.find("storepoint-name"):]
    storeName = elem[:elem.find("</div>")]
    storeName = storeName[storeName.find("\n") + 1:]
    storeName = storeName[:storeName.find("\n")]
    actualStoreName = ""
    for ch in storeName:
        if not (ch.isspace()):
            actualStoreName = actualStoreName + ch
    elem = elem[elem.find("storepoint-address"):]
    address = elem[:elem.find("</div>")]
    address = address[address.find("\n")+1:]
    address = address[:address.find("\n")]
    actualAddress = ""
    for ch in address:
        #if not (ch.isspace()):     
        if (ch == ","):
            ch = " "
        
        actualAddress = actualAddress + ch
    elem = elem[elem.find("storepoint-sidebar-phone"):]
    phone = elem[:elem.find("</div>")]
    phone = phone[phone.find('phone">') + 8:]
    f.write(storeName + "," + actualAddress + "," + phone + "\n" )
    print(actualStoreName,actualAddress,phone)
    singleData.append([actualStoreName,actualAddress,phone])
    
print(singleData)