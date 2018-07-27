from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import csv
import io
import requests
from datetime import datetime
import os
import sys
import argparse
import json
import gspread
#from oauth2client.service_account import ServiceAccountCredentials

def scroll_down_my_page(driver):
    for i in range(0, int(10)):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

options = Options()
options.add_argument('lang=en')
prefs = {"profile.default_content_setting_values.notifications": 2}
options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(chrome_options=options)


driver.get("https://www.facebook.com/hismileteeth/")

#scroll down all the way
#for i in range(0, int(pageCount)):
 #   driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
  #  print("Preparing Page: " + str(i + 1))
   # time.sleep(3)

time.sleep(10)

post = driver.find_element_by_xpath("//*[@id='u_0_t']")

text = driver.find_element_by_xpath("//*[@id='u_0_u']/div[3]/div[1]/div[2]/div[2]/p")

#print(str(len(post)))

print(str(len(text)))

time.sleep(5)