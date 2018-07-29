# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
#
# from selenium.webdriver.common.by import By
# import time
# import csv
# import io
# import requests
# from datetime import datetime
# import os
# import sys
# import argparse
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
#
#
# def getMyElementText(my_xpath):
#     my_elements = driver.find_elements_by_xpath(my_xpath)
#     if my_elements:
#         my_element_text = my_elements[0].text
#         # print(my_element_text)
#         return my_element_text
#     else:
#         # print("NA")
#         return "NA"
#
# def GetadvertLink():
#     # MyEc(advert_link_xpath,5)
#     time.sleep(2)
#     yellowpage_main_div_elements = driver.find_elements_by_xpath(advert_link_xpath)
#     if yellowpage_main_div_elements:
#         for yellowpage_link_element in yellowpage_main_div_elements:
#             yellowpage_link = yellowpage_link_element.get_attribute("href")
#             yellowpage_link_list_to_write = [
#                 {'ProfileLink': yellowpage_link}]
#             savetoCsv("Temp","advertLinksTemp",advert_PROFILE_LINKS_FILE_HEADERS,yellowpage_link_list_to_write,"ok")
#
# def savetoCsv(Foldername, FileName, HeadersAsList, DataAsList, myLog):
#
#     try:
#         FileNameCorrected = FileName.replace(":", "")
#         if not os.path.exists(Foldername):
#             os.makedirs(Foldername)
#         with open(Foldername + "\\" + FileNameCorrected + '.csv', 'a', newline='') as csvfile:
#             fieldnames = HeadersAsList
#             writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#             fileEmpty = os.stat(Foldername + "\\" + FileNameCorrected + '.csv').st_size == 0
#             if fileEmpty:
#                 writer.writeheader()
#             writer.writerows(DataAsList)
#             print("*" * 3 + myLog + "*" * 3)
#              # example fieldnames:myFieldnames = ['header1', 'header2', 'header3']
#              # example rows: myRow = [{'header1': "deneme1", 'header2': "deneme2", 'header3': "deneme3"}]
#     except:
#         print("**")
#
# advert_PROFILE_LINKS_FILE_HEADERS = ['ProfileLink']
# advert_PROFILE_LINKS_FILE_PATH = ""
#
# advert_link_xpath = "//*[@id='search-results-page']//*[@class='media-object clearfix inside-gap-medium image-on-right listing-summary']//*[@class='body left']//*[@class='listing-name']"
#
# options = Options()
# #options.add_argument('--headless')
# #options.add_argument('--disable-gpu')
# #options.add_argument('lang=en')
# prefs = {"profile.default_content_setting_values.notifications": 2}
# options.add_experimental_option("prefs", prefs)
# driver = webdriver.Chrome(chrome_options=options)
#
# driver.get("https://www.yellowpages.com.au/")
#
# time.sleep(150)
#
# businessTypeOrName_xpath = "//*[@id='clue']"
# suburbOrPostcode_xpath = "//*[@id='where']"
# searchButton_xpath = "//*[@class='button equilateral-button button-search']"
#
#
# text_businessTypOrName = driver.find_element_by_xpath(businessTypeOrName_xpath)
# text_suburbOrPostcode = driver.find_element_by_xpath(suburbOrPostcode_xpath)
# click_searchButton = driver.find_element_by_xpath(searchButton_xpath)
#
# text_businessTypOrName.send_keys("HOTELS")
# text_suburbOrPostcode.send_keys("NSW")
# click_searchButton.click()
#
#
# #
# #
# # def GetAllProfileLinks():
# #
# #
# #     yellowpage_skills_pagination_links_xpath_template = "//*[@class='pagination'][1]"
# #     GetadvertLink()
# #
# #     # page_number = 1
# #     # yellowpage_skills_pagination_links_xpath_formatted = yellowpage_skills_pagination_links_xpath_template.format(str(page_number))
# #     # paging_element = True
# #     # while paging_element:
# #     #     time.sleep(2)  # TODO: add EC element
# #     #     page_number = page_number + 1
# #     #     yellowpage_skills_pagination_links_xpath_formatted = yellowpage_skills_pagination_links_xpath_template.format(str(page_number))
# #     #     paging_element = driver.find_elements_by_xpath(yellowpage_skills_pagination_links_xpath_formatted)
# #     #     if paging_element:
# #     #         paging_element[0].click()
# #     #         GetadvertLink()
# #
# # GetAllProfileLinks()
# # my_profile_links = []
# #
# # print("Getting Links from 'PostUpdates' CSV file...")
# # try:
# #     with open('Temp/advertLinksTemp.csv') as csvfile:
# #         reader = csv.DictReader(csvfile)
# #         for row in reader:
# #             link = row['ProfileLink']
# #             my_profile_links.append(link)
# #         my_links_count = str(len(my_profile_links))
# #         print("All Links from 'Temp' CSV file are received. Number of links received: " + my_links_count)
# # except:
# #     print("'Temp' CSV file is missing or corrupted, please check.")
# #     time.sleep(10)
# #     sys.exit()
# #
# # advert_PROFILE_LINKS_FILE_HEADERS = ['Company Name', 'Address', 'Phone', 'Email', 'Web Site']
# #
# # for profile_link in my_profile_links:
# #     driver.get(profile_link)
# #     driver.maximize_window()
# #
# #     # company name , address , phone, email and web site
# #
# #     advert_Company_Name_xpath ="//*[@id='business-profile-page']//*[@class='listing-name']"
# #     advert_Address_xpath = "//*[@id='business-profile-page']//*[@class='listing-address mappable-address mappable-address-with-poi']"
# #     advert_Phone_xpath = "//*[@id='contact-card-scroll-to']//*[@class='click-to-call contact contact-preferred contact-phone']//*[@class='text middle  ']"
# #     advert_Email_xpath = "//*[@id='contact-card-scroll-to']//*[@class='contact contact-main contact-email']"
# #     advert_Web_site_xpath = "//*[@id='contact-card-scroll-to']//*[@class='contact contact-main contact-url']"
# #
# #
# #
# #     my_advert_Company_Name = getMyElementText(advert_Company_Name_xpath)
# #     my_advert_Address = getMyElementText(advert_Address_xpath)
# #     my_advert_Phone = getMyElementText(advert_Phone_xpath)
# #     my_advert_Email = driver.find_element_by_xpath(advert_Email_xpath).title
# #     my_advert_Web_site = driver.find_element_by_xpath(advert_Web_site_xpath).title
# #
# #     print(my_advert_Company_Name)
# #     print(my_advert_Address)
# #     print(my_advert_Phone)
# #     print(my_advert_Email)
# #     print(my_advert_Web_site)
#
#
# aa="a688bb96-e5d0-4733-9031-784a6da7922d"
#
#
# advert_Company_Name_xpath = "//*[@id='search-results-page']//*[@data-content-group-id='{0}']//*[@class='listing-name']"
# advert_Address_xpath = "//*[@id='search-results-page']//*[@data-content-group-id='{0}']//*[@class='listing-address mappable-address mappable-address-with-poi']"
# advert_Phone_xpath = "//*[@id='search-results-page']//*[@data-content-group-id='{0}']//*[@class='click-to-call contact contact-preferred contact-phone ']"
# advert_Email_xpath = "//*[@id='search-results-page']//*[@data-content-group-id='{0}']//*[@class='contact contact-main contact-email ']"
# advert_Web_site_xpath = "//*[@id='search-results-page']//*[@data-content-group-id='{0}']//*[@class='contact contact-main contact-url ']"
# print(advert_Company_Name_xpath)
# print(advert_Address_xpath)
# print(advert_Phone_xpath)
# print(advert_Email_xpath)
# print(advert_Web_site_xpath)
# print("************************")
#
# formatted_advert_Company_Name_xpath = advert_Company_Name_xpath.format(aa)
# formatted_advert_Address_xpath = advert_Address_xpath.format(aa)
# formatted_advert_Phone_xpath = advert_Phone_xpath.format(aa)
# formatted_advert_Email_xpath = advert_Email_xpath.format(aa)
# formatted_advert_Web_site_xpath = advert_Web_site_xpath.format(aa)
# print(formatted_advert_Company_Name_xpath)
# print(formatted_advert_Address_xpath)
# print(formatted_advert_Phone_xpath)
# print(formatted_advert_Email_xpath)
# print(formatted_advert_Web_site_xpath)
# print("************************")
#
# inf_advert_Company_Name = driver.find_elements_by_xpath(formatted_advert_Company_Name_xpath)
# inf_advert_Address = driver.find_elements_by_xpath(formatted_advert_Address_xpath)
# inf_advert_Phone = driver.find_elements_by_xpath(formatted_advert_Phone_xpath)
# inf_advert_Email = driver.find_elements_by_xpath(formatted_advert_Email_xpath)
# inf_advert_Web_site = driver.find_elements_by_xpath(formatted_advert_Web_site_xpath)
#
# print(inf_advert_Company_Name)
# print(inf_advert_Address)
# print(inf_advert_Phone)
# print(inf_advert_Email)
# print(inf_advert_Web_site)
# print("************************")
#
# if inf_advert_Company_Name:
#     my_advert_Company_Name = inf_advert_Company_Name[0].text
# else:
#     my_advert_Company_Name = "NA"
# if inf_advert_Address:
#     my_advert_Address = inf_advert_Address[0].text
# else:
#     my_advert_Address = "NA"
# if inf_advert_Phone:
#     my_advert_Phone = inf_advert_Phone[0].text
# else:
#     my_advert_Phone = "NA"
# if inf_advert_Email:
#     my_advert_Email = inf_advert_Email[0].get_attribute('data-email')
# else:
#     my_advert_Email = "NA"
# if inf_advert_Web_site:
#     my_advert_Web_site = inf_advert_Web_site[0].get_attribute('href')
# else:
#     my_advert_Web_site = "NA"
#
# print(my_advert_Company_Name)
# print(my_advert_Address)
# print(my_advert_Phone)
# print(my_advert_Email)
# print(my_advert_Web_site)
#
import os

# open("Temp/advertmainIdTemp.csv","w")

fileEmpty = os.stat("Temp/advertmainIdTemp.csv").st_size
if fileEmpty:
    os.remove('Temp/advertmainIdTemp.csv')


