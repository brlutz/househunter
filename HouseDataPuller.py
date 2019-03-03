#Heavily based on https://medium.com/@ben.sturm/scraping-house-listing-data-using-selenium-and-beautiful-soup-1cbb94ba9492
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
from pprint import pprint


class HouseDetail:
    def __init__(self,
           url, address, zipcode, city,
           price,estimatePrice,
           beds,baths,
           squareFeet,stories,roomCount,parking,
           type,yearBuilt,
           heating,cooling,
           lotSize,lotWidth,lotDepth,
           highschool,middleschool,elementaryschool, hsdistance, msdistance, esdistance,
           mlsNumber):
        self.Url = url
        self.Address = address
        self.ZipCode = zipcode
        self.City = city
        self.Price = price
        self.EstimatePrice = estimatePrice
        self.Beds = beds
        self.Baths = baths
        self.SquareFeet = squareFeet,
        self.Stories = stories,
        self.RoomCount = roomCount
        self.Parking = parking
        self.Type = type
        self.YearBuilt = yearBuilt
        self.Heating = heating
        self.Cooling = cooling
        self.LotSize = lotSize
        self.LotWidth = lotWidth
        self.LotDepth = lotDepth
        self.Highschool = highschool
        self.Middleschool = middleschool
        self.Elementaryschool = elementaryschool
        self.HSDistance = hsdistance
        self.MSDistance = msdistance
        self.ESDistance = esdistance
        self.MLSNumber = mlsNumber

    def Seralized(self):
        x = {}
        x["Url"] = self.Url
        x["Address"] = self.Address
        x["Zipcode"] = self.ZipCode
        x["City"] = self.City
        x["Price"] = self.Price 
        x["EstimatePrice"] = self.EstimatePrice 
        x["Beds"] = self.Beds 
        x["Baths"] = self.Baths 
        x["SquareFeet"] = self.SquareFeet 
        x["Stories"] = self.Stories 
        x["RoomCount"] = self.RoomCount 
        x["Parking"] = self.Parking 
        x["Type"] = self.Type
        x["YearBuilt"] = self.YearBuilt 
        x["Heating"] = self.Heating
        x["Cooling"] = self.Cooling
        x["LotSize"] = self.LotSize
        x["LotWidth"] = self.LotWidth
        x["LotDepth"] = self.LotDepth
        x["Highschool"] = self.Highschool
        x["Middleschool"] = self.Middleschool
        x["Elementaryschool"] = self.Elementaryschool 
        x["HSDistance"] = self.HSDistance 
        x["MSDistance"] = self.MSDistance
        x["ESDistance"] = self.ESDistance 
        x["MLSNumber"] = self.MLSNumber

        return x

def get_price(soup):
    try:
        for element in soup.find_all(class_='estimates'):
            price = element.find_all("span")[1].text
        price = price.replace(",", "").replace("+", "").replace("$", "").lower()
        return int(price)
    except:
        return np.nan
    
def get_sale_date(soup):
    try:
        for element in soup.find_all(class_='estimates'):
            sale_date = element.find_all("span")[3].text
        sale_date = sale_date.strip()
        return sale_date
    except:
        return 'None'
    
def get_lot_size(soup):
    try:
        lot_size_regex = re.compile('Lot:')
        obj = soup.find(text=lot_size_regex).find_next()
        return obj.text
    except:
        return 'None'
def get_address(soup):

    try:
        address = soup.find("div",class_="hdp-home-header-st-addr").text
        return address
    except: 
        try: #Full page view
            #obj = soup.find("header",class_="ds-address-container").text.split(',')
            address = soup.find("h1",class_="ds-address-container").findNext('span').text.replace(",","")
            return address
        except:
            return 'None'

def get_city(soup):
    try:
        city = soup.find("div",class_="hdp-home-header-st-addr").findNext('div').text.split(',')[0]
        #obj = soup.find("header",class_="zsg-content-header addr").text.split(',')
        #obj = soup.find("h1",class_="ds-address-container").findNext('span').text
        return city
    except:
        try:
            city = soup.find("h1",class_="ds-address-container").findNext('span').text
            return city
        except:
            return 'None'
        
    
def get_zip(soup):
    try:
        zip = soup.find("div",class_="hdp-home-header-st-addr").findNext('div').text.split()[-1:][0]
        return zip
    except:
        try:
            zip = soup.find("h1",class_="ds-address-container").findNext('span').findNext('span').text.split()[-1:][0]
            return zip
        except:
            return 'None'
        return 'None'


def get_num_beds(soup):
    try:
        lot_size_regex = re.compile('Beds:')
        numBeds = soup.find(text=lot_size_regex).find_next().text
        return numBeds
    except:
        return 'None'
    
def get_num_baths(soup):
    try:
        bath_number_regex = re.compile('Bathrooms Full:')
        numBaths = soup.find(text=bath_number_regex).find_next().text
        return numBaths
    except:
        return 'None'
    
def get_floor_size(soup):
    try:
        floor_size_regex = re.compile('Floor size:')
        floorSize = soup.find(text=floor_size_regex).find_next().text
        return floorSize
    except:
        return 'None'

def get_parking(soup):
    try:
        parking_regex = re.compile('Parking:')
        parking = soup.find(text=parking_regex).find_next().text
        return parking
    except:
        return 'None'
    
def get_year_built(soup):
    try:
        objs = soup.find_all("div",class_='fact-label')
        built_in_regex = re.compile('Year Built')
        for obj in objs:
            out = obj.find(text=built_in_regex)
            if out is not None:
                return out.find_next().text
    except:
        return 'None'

def get_stories(soup):
    try:
        stories_regex = re.compile('Stories:')
        stories = soup.find(text=stories_regex).find_next().text
        return stories
    except:
        return 'None'

def get_html_data(url, driver):
    
    
    driver.get(url)
    time.sleep(np.random.lognormal(0,1)+10)
    error = False
    try:
        driver.find_element_by_link_text("See More Facts and Features").click()
        #driver.find_element_by_css_selector('.read-more').click()
    except:
        error = True
    
    if error:
        driver.find_element_by_link_text("See more facts and features").click()

    time.sleep(np.random.lognormal(0,1)+5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    return soup

    
def get_house_data(driver,link):
    
    soup = get_html_data(link,driver)
    address = get_address(soup)
    zip_code = get_zip(soup)
    city = get_city(soup)
    price = get_price(soup)
    estimatePrice = None
    beds = get_num_beds(soup)
    baths = get_num_baths(soup)
    squareFeet = get_floor_size(soup)
    stories = get_stories(soup)
    roomCount = "roomCount"
    parking = get_parking(soup)
    type = "type"
    yearBuilt = get_year_built(soup)
    heating = "heating"
    cooling = "cooling"
    lotSize = get_lot_size(soup)
    lotWidth = "lotWidth"
    lotDepth = "lotDepth"
    highschool = "highschool"
    middleschool = "middleschool"
    elementaryschool = "elementarySchool"
    hsdistance = "hsdistance"
    msdistance = "msdistance"
    esdistance = "esdistance"
    mlsNumber = "mlsNumber"
    sale_date = get_sale_date(soup)
    
    
    result = HouseDetail(link, address, zip_code, city,
           price, estimatePrice,
           beds,baths,
           squareFeet,stories,roomCount,parking,
           type,yearBuilt,
           heating,cooling,
           lotSize,lotWidth,lotDepth,
           highschool,middleschool,elementaryschool, hsdistance, msdistance, esdistance,
           mlsNumber) 

    return result


client = MongoClient()
client = MongoClient('localhost', 27017)
db = client.housedata
sourceUrls = db.sourceUrls

chromedriver = r"C:/Users/benry/AppData/Roaming/npm" # path to the chromedriver executable
chromedriver = os.path.expanduser(chromedriver)
print('chromedriver path: {}'.format(chromedriver))
binary = FirefoxBinary(chromedriver)
sys.path.append(chromedriver)
caps = DesiredCapabilities.FIREFOX.copy()
caps['marionette'] = False
driver = webdriver.Firefox()

sourceUrlObjs = sourceUrls.find().limit(1)
links = []
for house in sourceUrlObjs:
    houseData = get_house_data(driver, house["Url"])
    #houseData.Seralized()
    attrs = vars(houseData)
    print (', '.join("%s: %s" % item for item in attrs.items()))




#for listing in listings:
#    print(listing)
#    sourceUrls.insert_one(SourceUrl(listing).Serialized())

#next_button = soup.find_all("a", class_="on")
#next_link = ['https://www.zillow.com'+row['href'] for row in next_button]


#print(listings)
#listings[:5]
#print(listings)

