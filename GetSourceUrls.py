import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import sys
import numpy as np
import pandas as pd
import regex as re
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import datetime
import pymongo
from pymongo import MongoClient

class SourceUrl:
    def __init__(self, url):
        self.url = url
        self.timeRetrived = datetime.datetime.now()
    
    def Serialized(self):
        c = {}
        c["Url"] = self.url
        c["Retrieved"] = self.timeRetrived
        return c

def get_house_links(url, driver, pages=20):
    house_links=[]
    driver.get(url)
    time.sleep(np.random.lognormal(0,1)+35)
    for i in range(pages):
        print("Pulling down page:" + str(i))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        time.sleep(np.random.lognormal(0,1)+10)
        listings = soup.find_all("a", class_="zsg-photo-card-overlay-link")
        
        page_data = ['https://www.zillow.com'+row['href'] for row in listings]
        #house_links.append(page_data)
        house_links = house_links + page_data
        time.sleep(np.random.lognormal(0,1)+10)
        next_button = soup.find_all("a", class_="on")
        next_button_link = ['https://www.zillow.com'+row['href'] for row in next_button]
        if i<19:
            driver.find_element_by_css_selector('.on').click()
            #driver.get(next_button_link[0])
    
    return house_links        


client = MongoClient()
client = MongoClient('localhost', 27017)
db = client.housedata
sourceUrls = db.sourceUrls
sourceUrls.delete_many({})



chromedriver = r"C:/Users/benry/AppData/Roaming/npm" # path to the chromedriver executable
chromedriver = os.path.expanduser(chromedriver)
print('chromedriver path: {}'.format(chromedriver))

#display = Display(visible=0, size=(1024, 768))
#display.start()


#capabilities = webdriver.DesiredCapabilities().FIREFOX
#capabilities["marionette"] = False
binary = FirefoxBinary(chromedriver)
#driver = webdriver.Firefox(firefox_binary=binary, capabilities=capabilities)

sys.path.append(chromedriver)
caps = DesiredCapabilities.FIREFOX.copy()
caps['marionette'] = False
driver = webdriver.Firefox()

zillow_pleasanton_url = "https://www.zillow.com/homes/for_sale/house_type/globalrelevanceex_sort/40.465234,-74.232559,39.585053,-75.708847_rect/9_zm/640825c7a9X1-CR6bj9zwsm022m_z5m02_crid/"
#driver.get(zillow_pleasanton_url)
#time.sleep(5)#/soup = BeautifulSoup(driver.page_source, 'html.parser')

#listings = soup.find_all("a", class_="zsg-photo-card-overlay-link")
#listings = soup.find("a", class_="zsg-photo-card-overlay-link")
listings = get_house_links(zillow_pleasanton_url, driver, 20)


for listing in listings:
    print(listing)
    sourceUrls.insert_one(SourceUrl(listing).Serialized())

#next_button = soup.find_all("a", class_="on")
#next_link = ['https://www.zillow.com'+row['href'] for row in next_button]


#print(listings)
#listings[:5]
#print(listings)

