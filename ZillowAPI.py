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
from pyvirtualdisplay import Display
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
driver.get(zillow_pleasanton_url)
time.sleep(10)
soup = BeautifulSoup(driver.page_source, features="html5lib")

listings = soup.find_all("a", class_="zsg-photo-card-overlay-link")
#listings = soup.find("a", class_="zsg-photo-card-overlay-link")
print(listings)
#listings[:5]
#print(listings)

