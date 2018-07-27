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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def savetoCsv(Foldername, FileName, HeadersAsList, DataAsList, myLog):

    try:
        FileNameCorrected = FileName.replace(":", "")
        if not os.path.exists(Foldername):
            os.makedirs(Foldername)
        with open(Foldername + "\\" + FileNameCorrected + '.csv', 'a', newline='') as csvfile:
            fieldnames = HeadersAsList
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            fileEmpty = os.stat(Foldername + "\\" + FileNameCorrected + '.csv').st_size == 0
            if fileEmpty:
                writer.writeheader()
            writer.writerows(DataAsList)
            print("*" * 3 + myLog + "*" * 3)
             # example fieldnames:myFieldnames = ['header1', 'header2', 'header3']
             # example rows: myRow = [{'header1': "deneme1", 'header2': "deneme2", 'header3': "deneme3"}]
    except:
        print("**")

def GetadvertLink():
    # MyEc(advert_link_xpath,5)
    time.sleep(2)
    yellowpage_main_div_elements = driver.find_elements_by_xpath(advert_mainId_xpath)
    if yellowpage_main_div_elements:
        for yellowpage_mainId_element in yellowpage_main_div_elements:
            yellowpage_mainId = yellowpage_mainId_element.get_attribute("data-content-group-id")
            yellowpage_mainId_list_to_write = [
                {'ProfileLink': yellowpage_mainId}]
            savetoCsv("Temp","advertmainIdTemp",advert_PROFILE_LINKS_FILE_HEADERS,yellowpage_mainId_list_to_write,"ok")



advert_PROFILE_LINKS_FILE_HEADERS = ['ProfileLink']
advert_PROFILE_LINKS_FILE_PATH = ""

advert_mainId_xpath = "//*[@id='search-results-page']//*[@class='listing listing-search listing-data']"

options = Options()
#options.add_argument('--headless')
#options.add_argument('--disable-gpu')
#options.add_argument('lang=en')
prefs = {"profile.default_content_setting_values.notifications": 2}
options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(chrome_options=options)

driver.get("https://www.yellowpages.com.au/")

time.sleep(150)

businessTypeOrName_xpath = "//*[@id='clue']"
suburbOrPostcode_xpath = "//*[@id='where']"
searchButton_xpath = "//*[@class='button equilateral-button button-search']"


text_businessTypOrName = driver.find_element_by_xpath(businessTypeOrName_xpath)
text_suburbOrPostcode = driver.find_element_by_xpath(suburbOrPostcode_xpath)
click_searchButton = driver.find_element_by_xpath(searchButton_xpath)

text_businessTypOrName.send_keys("HOTELS")
text_suburbOrPostcode.send_keys("NSW")
click_searchButton.click()

GetadvertLink()

my_advert_mainId = []

print("Getting Links from 'PostUpdates' CSV file...")
try:
    with open('Temp/advertLinksTemp.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            advert = row['ProfileLink']
            my_advert_mainId.append(advert)
        my_mainId_count = str(len(my_advert_mainId))
        print("All Links from 'Temp' CSV file are received. Number of links received: " + my_mainId_count)
except:
    print("'Temp' CSV file is missing or corrupted, please check.")
    time.sleep(10)
    sys.exit()

advert_PROFILE_LINKS_FILE_HEADERS = ['Company Name', 'Address', 'Phone', 'Email', 'Web Site']

for profile_mainId in my_advert_mainId:
    driver.maximize_window()


    advert_Company_Name_xpath = "//*[@id='search-results-page']//*[@data-content-group-id='{}']//*[@class='listing-name']"
    advert_Address_xpath = "//*[@id='search-results-page']//*[@data-content-group-id='{}']//*[@class='listing-address mappable-address mappable-address-with-poi']"
    advert_Phone_xpath = "//*[@id='search-results-page']//*[@data-content-group-id='{}']//*[@class='glyph icon-phone border border-dark-blue with-text']"
    advert_Email_xpath ="//*[@id='search-results-page']//*[@data-content-group-id='{}']//*[@class='contact contact-main contact-email ']"
    advert_Web_site_xpath = "// *[ @ id = 'search-results-page'] // *[ @ data - content - group - id = '{}'] // *[ @class ='contact contact-main contact-url ']"

//*[@id="search-results-page"]//*[@data-content-group-id="a688bb96-e5d0-4733-9031-784a6da7922d"]


driver.maximize_window()

    # company name , address , phone, email and web site

    advert_Company_Name_xpath ="//*[@id='business-profile-page']//*[@class='listing-name']"
    advert_Address_xpath = "//*[@id='business-profile-page']//*[@class='listing-address mappable-address mappable-address-with-poi']"
    advert_Phone_xpath = "//*[@id='contact-card-scroll-to']//*[@class='click-to-call contact contact-preferred contact-phone']//*[@class='text middle  ']"
    advert_Email_xpath = "//*[@id='contact-card-scroll-to']//*[@class='contact contact-main contact-email']"
    advert_Web_site_xpath = "//*[@id='contact-card-scroll-to']//*[@class='contact contact-main contact-url']"



    my_advert_Company_Name = getMyElementText(advert_Company_Name_xpath)
    my_advert_Address = getMyElementText(advert_Address_xpath)
    my_advert_Phone = getMyElementText(advert_Phone_xpath)
    my_advert_Email = driver.find_element_by_xpath(advert_Email_xpath).title
    my_advert_Web_site = driver.find_element_by_xpath(advert_Web_site_xpath).title

    print(my_advert_Company_Name)
    print(my_advert_Address)
    print(my_advert_Phone)
    print(my_advert_Email)
    print(my_advert_Web_site)