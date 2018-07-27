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
from oauth2client.service_account import ServiceAccountCredentials


def scroll_down_my_page(driver):
    for i in range(0, int(10)):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


# to Google Spreadsheets
# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('gs.json', scope)
client = gspread.authorize(creds)

sheet = client.open("quora").sheet1

my_row = 1
my_column_question = 1
my_column_n_of_answers = 2
my_column_n_of_public_followers = 3
my_column_number_of_views = 4
my_column_last_asked_date = 5
my_column_question_url = 6

options = Options()
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')
options.add_argument('lang=en')
prefs = {"profile.default_content_setting_values.notifications": 2}
options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(chrome_options=options)
driver2 = webdriver.Chrome(chrome_options=options)
driver3 = webdriver.Chrome(chrome_options=options)

driver.get("https://www.quora.com/topic/Zendesk-company")
time.sleep(10)

scroll_down_my_page(driver)

time.sleep(10)

feed_main_xpath = "//*[@class='FeedStory AnswerFeedStory feed_item']"
feed_user_xpath_template = "//*[@id='{0}']//*[@class='user']"
feed_question_xpath_template = "(//*[@id='{0}']//*[@class='ui_qtext_rendered_qtext'])[1]"
feed_number_of_answers_xpath_template = "(//*[@id='{0}']//*[@class='bold_num'])[1]"
feed_number_of_public_followers_xpath_template = ""
feed_number_of_views_xpath_template = "(//*[@id='{0}']//*[@class='bold_num'])[2]"
feed_last_asked_date_xpath_template = "//*[@id='{0}']//*[@class='datetime']"
feed_question_link_xpath_template = "//*[@id='{0}']//*[@class='question_link']"
question_number_of_answers_template = "//*[@class='QuestionPageAnswerHeader']/div[@class='answer_count']"
feed_user_profile_link_template = "(//*[@id='{0}']//*[@class='user'])[1]"
profile_public_followers_list_count_xpath = "//*[contains(@class,'Followers')]//*[@class='list_count']"

# get feed IDs
all_feeds = driver.find_elements_by_xpath(feed_main_xpath)

for feed in all_feeds:
    my_row = my_row + 1
    feed_id = feed.get_attribute("id")
    # print(feed_id)
    # get user
    feed_user_xpath_formatted = feed_user_xpath_template.format(feed_id)
    feed_question_xpath_formatted = feed_question_xpath_template.format(feed_id)
    feed_number_of_answers_xpath_formatted = feed_number_of_answers_xpath_template.format(feed_id)
    feed_number_of_views_xpath_formatted = feed_number_of_views_xpath_template.format(feed_id)
    feed_last_asked_date_xpath_formatted = feed_last_asked_date_xpath_template.format(feed_id)
    feed_question_link_xpath_formatted = feed_question_link_xpath_template.format(feed_id)
    feed_user_profile_link_formatted = feed_user_profile_link_template.format(feed_id)

    feed_user_element = driver.find_elements_by_xpath(feed_user_xpath_formatted)
    feed_question_element = driver.find_elements_by_xpath(feed_question_xpath_formatted)
    feed_number_of_answers_element = driver.find_elements_by_xpath(feed_number_of_answers_xpath_formatted)
    feed_number_of_views_element = driver.find_elements_by_xpath(feed_number_of_views_xpath_formatted)
    feed_last_asked_date_element = driver.find_elements_by_xpath(feed_last_asked_date_xpath_formatted)
    feed_question_link_element = driver.find_elements_by_xpath(feed_question_link_xpath_formatted)
    feed_user_profile_link_element = driver.find_elements_by_xpath(feed_user_profile_link_formatted)

    if feed_user_element:
        my_feed_user = feed_user_element[0].text
    else:
        my_feed_user = "NA"

    if feed_question_element:
        my_feed_question = feed_question_element[0].text
    else:
        my_feed_question = "NA"

    if feed_number_of_answers_element:
        my_feed_number_of_answers = feed_number_of_answers_element[0].text
    else:
        my_feed_number_of_answers = "NA"

    if feed_number_of_views_element:
        my_feed_number_of_views = feed_number_of_views_element[0].text
    else:
        my_feed_number_of_views = "NA"

    if feed_last_asked_date_element:
        my_feed_feed_last_asked_date = feed_last_asked_date_element[0].text
    else:
        my_feed_feed_last_asked_date = "NA"

    if feed_question_link_element:
        my_feed_feed_question_link = feed_question_link_element[0].get_attribute("href")
    else:
        my_feed_feed_question_link = ""

    if feed_user_profile_link_element:
        my_feed_user_profile_link = feed_user_profile_link_element[0].get_attribute("href")
    else:
        my_feed_user_profile_link = ""

    print("User: " + my_feed_user)
    print("Question: " + my_feed_question)
    print("Total Number of User Answers: " + my_feed_number_of_answers)
    print("Total number of Answer Views: " + my_feed_number_of_views)
    print("Last Update Date: " + my_feed_feed_last_asked_date)
    print("Question Link: " + my_feed_feed_question_link)
    print("User Profile Link: " + my_feed_user_profile_link)

    question_number_of_answers = "NA"
    profile_public_followers_list_count = "NA"

    if my_feed_feed_question_link is not None:
        driver2.get(my_feed_feed_question_link)
        time.sleep(2)
        question_number_of_answers_element = driver2.find_elements_by_xpath(question_number_of_answers_template)
        if question_number_of_answers_element:
            question_number_of_answers = question_number_of_answers_element[0].text
        else:
            question_number_of_answers = "NA"
        print("Total Number of Question Answers: " + question_number_of_answers)

    if my_feed_user_profile_link is not None:
        driver3.get(my_feed_user_profile_link)
        time.sleep(2)
        profile_public_followers_list_count_element = driver3.find_elements_by_xpath(
            profile_public_followers_list_count_xpath)
        if profile_public_followers_list_count_element:
            profile_public_followers_list_count = profile_public_followers_list_count_element[0].text
        else:
            profile_public_followers_list_count = "NA"
        print("Total Number of User Followers: " + profile_public_followers_list_count)

    sheet.update_cell(my_row, my_column_question, my_feed_question)
    sheet.update_cell(my_row, my_column_n_of_answers, question_number_of_answers)
    sheet.update_cell(my_row, my_column_n_of_public_followers, profile_public_followers_list_count)
    sheet.update_cell(my_row, my_column_number_of_views, my_feed_number_of_views)
    sheet.update_cell(my_row, my_column_last_asked_date, my_feed_feed_last_asked_date)
    sheet.update_cell(my_row, my_column_question_url, my_feed_feed_question_link)

    print("*" * 30)
