from xmlrpc.client import boolean

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
import time
import csv
import io
import requests
from datetime import datetime
import datetime
import os
import sys
import argparse
import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import configparser
from configparser import ConfigParser

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create a file handler
handler = logging.FileHandler('YellowPageLog.log')
handler.setLevel(logging.INFO)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)

my_time_stamp = '{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
csv_file_name_with_timestamp= my_time_stamp + "_" + "Yellow Pages"

def scroll_down_my_page(driver):
    for i in range(0, int(5)):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # print("Preparing Page: " + str(i + 1))
# time.sleep(1)

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

def savetoCsvW(Foldername, FileName, HeadersAsList, DataAsList, myLog):
    try:
        FileNameCorrected = FileName.replace(":", "")
        if not os.path.exists(Foldername):
            os.makedirs(Foldername)
        with open(Foldername + "\\" + FileNameCorrected + '.csv', 'w', newline='') as csvfile:
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


def pagging():
    advert_skills_pagination_links_xpath_template = "//*[@class='button-pagination-container responsive']//a[@class= 'pagination navigation' and @data-page = '{0}']"

    # workana_skills_pagination_links_xpath_formatted = workana_skills_pagination_links_xpath_template.format(str(page_number))
    time.sleep(2)  # TODO: add EC element
    # page_number = page_number + 1
    advert_skills_pagination_links_xpath_formatted = advert_skills_pagination_links_xpath_template.format(str(page_number))
    paging_element = driver.find_elements_by_xpath(advert_skills_pagination_links_xpath_formatted)
    return (boolean(paging_element))

def paggingclick(number):
    advert_skills_pagination_links_xpath_template = "//*[@class='button-pagination-container responsive']//a[@class= 'pagination navigation' and @data-page = '{0}']"
    # page_number =
    # workana_skills_pagination_links_xpath_formatted = workana_skills_pagination_links_xpath_template.format(str(page_number))
    # page_number = page_number + 1
    advert_skills_pagination_links_xpath_formatted = advert_skills_pagination_links_xpath_template.format(str(number))
    time.sleep(2)  # TODO: add EC element
    paging_element = driver.find_elements_by_xpath(advert_skills_pagination_links_xpath_formatted)
    if paging_element:
        paging_element[0].click()

try:
    config = ConfigParser()

    # parse existing file
    config.read('yellowPageConfiguration.ini')

    # read values from a section
    input_businessTypOrName = config.get('yellowPageSearch', 'businessTypOrName')
    input_suburbOrPostcode = config.get('yellowPageSearch', 'suburbOrPostcode')

except:
    print("There is a problem with configuration file. Please check and try again!")
    time.sleep(10)
    sys.exit()




advert_PROFILE_LINKS_FILE_HEADERS = ['ProfileLink']
advert_PROFILE_LINKS_FILE_PATH = ""
advert_FILE_HEADERS = ['Company Name', 'Address', 'Phone', 'Email', 'Web Site']

advert_mainId_xpath = "//*[@id='search-results-page']//*[@class='listing listing-search listing-data']"

options = Options()
#options.add_argument('--headless')
#options.add_argument('--disable-gpu')
#options.add_argument('lang=en')
prefs = {"profile.default_content_setting_values.notifications": 2}
options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(chrome_options=options)

driver.get("https://www.yellowpages.com.au/")

# time.sleep(150)


while True:
    businessTypeOrName_xpath = "//*[@id='clue']"
    text_businessTypOrName = driver.find_elements_by_xpath(businessTypeOrName_xpath)
    if text_businessTypOrName:
        print("Page Open.")
        break
    else:
        time.sleep(3)

businessTypeOrName_xpath = "//*[@id='clue']"
suburbOrPostcode_xpath = "//*[@id='where']"
searchButton_xpath = "//*[@class='button equilateral-button button-search']"


text_businessTypOrName = driver.find_element_by_xpath(businessTypeOrName_xpath)
text_suburbOrPostcode = driver.find_element_by_xpath(suburbOrPostcode_xpath)
click_searchButton = driver.find_element_by_xpath(searchButton_xpath)


text_businessTypOrName.send_keys(input_businessTypOrName)
text_suburbOrPostcode.send_keys(input_suburbOrPostcode)
click_searchButton.click()




saved_advert_id = 1
#saved_advert_count = int(0)
def get_advert_details(profile_mainId):

    driver.maximize_window()
    print("Saving Advert: " + str(saved_advert_id))
    #saved_advert_count += int(1)

    advert_Company_Name_xpath = "//*[@id='search-results-page']//*[@data-content-group-id='{0}']//*[@class='listing-name']"
    advert_Address_xpath = "//*[@id='search-results-page']//*[@data-content-group-id='{0}']//*[@class='listing-address mappable-address mappable-address-with-poi']"
    advert_Phone_xpath = "//*[@id='search-results-page']//*[@data-content-group-id='{0}']//*[@class='click-to-call contact contact-preferred contact-phone ']"
    advert_Email_xpath = "//*[@id='search-results-page']//*[@data-content-group-id='{0}']//*[@class='contact contact-main contact-email ']"
    advert_Web_site_xpath = "//*[@id='search-results-page']//*[@data-content-group-id='{0}']//*[@class='contact contact-main contact-url ']"

    formatted_advert_Company_Name_xpath = advert_Company_Name_xpath.format(profile_mainId)
    formatted_advert_Address_xpath = advert_Address_xpath.format(profile_mainId)
    formatted_advert_Phone_xpath = advert_Phone_xpath.format(profile_mainId)
    formatted_advert_Email_xpath = advert_Email_xpath.format(profile_mainId)
    formatted_advert_Web_site_xpath = advert_Web_site_xpath.format(profile_mainId)

    inf_advert_Company_Name = driver.find_elements_by_xpath(formatted_advert_Company_Name_xpath)
    inf_advert_Address = driver.find_elements_by_xpath(formatted_advert_Address_xpath)
    inf_advert_Phone = driver.find_elements_by_xpath(formatted_advert_Phone_xpath)
    inf_advert_Email = driver.find_elements_by_xpath(formatted_advert_Email_xpath)
    inf_advert_Web_site = driver.find_elements_by_xpath(formatted_advert_Web_site_xpath)

    if inf_advert_Company_Name:
        my_advert_Company_Name = inf_advert_Company_Name[0].text
    else:
        my_advert_Company_Name = "NA"
    if inf_advert_Address:
        my_advert_Address = inf_advert_Address[0].text
    else:
        my_advert_Address = "NA"
    if inf_advert_Phone:
        my_advert_Phone = inf_advert_Phone[0].text
    else:
        my_advert_Phone = "NA"
    if inf_advert_Email:
        my_advert_Email = inf_advert_Email[0].get_attribute('data-email')
    else:
        my_advert_Email = "NA"
    if inf_advert_Web_site:
        my_advert_Web_site = inf_advert_Web_site[0].get_attribute('href')
    else:
        my_advert_Web_site = "NA"


    # print(my_advert_Company_Name)
    # print(my_advert_Address)
    # print(my_advert_Phone)
    # print(my_advert_Email)
    # print(my_advert_Web_site)

    my_advert_data_as_list_to_write = [{'Company Name':my_advert_Company_Name, 'Address':my_advert_Address, 'Phone':my_advert_Phone, 'Email':my_advert_Email, 'Web Site':my_advert_Web_site}]

    savetoCsv("AdvertDetails", "Yellow Pages", advert_FILE_HEADERS,
            my_advert_data_as_list_to_write, "saved")


#my_advert_mainId:

page_number = 2
while pagging() == True:

    GetadvertLink()

    my_advert_mainId = []

    # print("Getting Links from 'PostUpdates' CSV file...")
    try:
        with open('Temp/advertmainIdTemp.csv') as csvfile:
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

    for advert in my_advert_mainId:
        try:
            get_advert_details(advert)
        except:
            logger.error(logging.exception("message"))
    scroll_down_my_page(driver)
    paggingclick(page_number)
    page_number = page_number +1
    os.remove('Temp/advertmainIdTemp.csv')
    print("**")