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


link = "https://atmcoiners.com/atmcoiners-locations/"

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
filename = "atmcoiners.csv"
f = open(filename, "w")

headers = "Store Name, Address\n"
f.write(headers)
#end of making the file

browser = webdriver.Chrome(options=options,executable_path=DRIVER_PATH)
browser.get(link)


time.sleep(2)
html = browser.page_source
soup = BeautifulSoup(html, 'lxml')

allelements = soup.findAll("div", {"class": "card-map mapresults__cards-item"})
storename = soup.findAll("h3", {"class": "card-map__title"})
info = soup.findAll("div", {"class": "icon-longtext__text"})


for i in range(len(storename)): 
    shopname = str(storename[i])
    
    address = str(info[i *3])
    
    name = shopname[shopname.find(">")+1:]
    name = name[name.find(">")+1:]
    name = name[:name.find("<")]
    
    address = address[address.find(">")+1:]
    address = address[:address.find("<")]
    
    realadd = ""
    
    for ch in address:
        if ch == ",":
            ch = " "
        realadd = realadd + ch
        
  
    
    f.write(name + "," + realadd + "\n")
    

f.close()
    

