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

def MyEc(myXpath,intTimeOut):
    try:
        WebDriverWait(driver, intTimeOut).until(
            EC.presence_of_element_located((By.XPATH, myXpath))
        )
    finally:
        print("")

def GetWorkerLink():
    # MyEc(worker_link_xpath,5)
    time.sleep(2)
    worker_main_div_elements = driver.find_elements_by_xpath(worker_link_xpath)
    if worker_main_div_elements:
        for worker_link_element in worker_main_div_elements:
            worker_link = worker_link_element.get_attribute("href")
            worker_link_list_to_write = [
                {'ProfileLink': worker_link}]
            savetoCsv("Temp","WorkerLinksTemp",WORKER_PROFILE_LINKS_FILE_HEADERS,worker_link_list_to_write,"ok")


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

WORKER_PROFILE_LINKS_FILE_HEADERS = ['ProfileLink']
WORKER_PROFILE_LINKS_FILE_PATH = ""
URL_WORKANA_SKILLS_TEMPLATE = "https://www.workana.com/freelancers?skills={0}"

print("Preparing browser")
options = Options()
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')
options.add_argument('lang=en')
prefs = {"profile.default_content_setting_values.notifications" : 2}
options.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(chrome_options=options)

worker_link_xpath = "//*[@id='workers']//*[@class='profile-photo img img-circle']//a"
url_workana_skills_formatted = URL_WORKANA_SKILLS_TEMPLATE.format("linux")

def GetAllProfileLinks():
    driver.get(url_workana_skills_formatted)

    driver.maximize_window()
    reminder_dismiss_button_xpath = "//*[@class='footer-reminder']/button/span"

    MyEc(reminder_dismiss_button_xpath,10)

    reminder_dismiss_button_elements = driver.find_elements_by_xpath(reminder_dismiss_button_xpath)
    if reminder_dismiss_button_elements:
        reminder_dismiss_button_elements[0].click()

    workana_skills_pagination_links_xpath_template = "//*[@class='pagination']//a[contains(@href, '{0}')]"


    page_number = 1
    workana_skills_pagination_links_xpath_formatted = workana_skills_pagination_links_xpath_template.format(str(page_number))
    paging_element = True
    while paging_element:
        time.sleep(2) #TODO: add EC element
        page_number = page_number + 1
        workana_skills_pagination_links_xpath_formatted = workana_skills_pagination_links_xpath_template.format(str(page_number))
        paging_element = driver.find_elements_by_xpath(workana_skills_pagination_links_xpath_formatted)
        if paging_element:
            paging_element[0].click()
            GetWorkerLink()


GetAllProfileLinks()
#browse to links from csv
my_profile_links = []

print("Getting Links from 'PostUpdates' CSV file...")
try:
    with open('Temp/WorkerLinksTemp.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            link = row['ProfileLink']
            my_profile_links.append(link)
        my_links_count = str(len(my_profile_links))
        print("All Links from 'Temp' CSV file are received. Number of links received: " + my_links_count)
except:
    print("'Temp' CSV file is missing or corrupted, please check.")
    time.sleep(10)
    sys.exit()

WORKER_PROFILE_LINKS_FILE_HEADERS = ['Name', 'Tagline', 'ProfileUrl', 'Rating', 'Country', 'Category', 'HourlyRate','Skills', 'Ranking Workana', 'Category Ranking'
                                     ,'Country Ranking', 'Completed Projects', 'Hours Worked', 'Profile Level', 'Number of Certificates', 'Rating from Clients',
                                     'Last Login', 'Registered', 'My Top Skills', 'About Me', 'Work History', 'English Level', 'Spanish Level'
                                     'AdWords Básico Score', 'AdWords Básico Percentage',
                                     'ANGULAR JS Score', 'ANGULAR JS Percentage',
                                     'Bootstrap Básico Score', 'Bootstrap Básico Percentage',
                                     'CSS Básico Score', 'CSS Básico Percentage',
                                     'Finanzas Score', 'Finanzas Percentage','HTML 5 Intermedio Score', 'HTML 5 Intermedio Percentage',
                                     'Indesign básico Score', 'Indesign básico Percentage', 'Javascript Avanzado Score', 'Javascript Avanzado Percentage',
                                     'LINUX Score', 'LINUX Percentage',
                                     'Marketing Online Básico Percentage', 'Marketing Online Básico Score',
                                     'MySql Intermediário Percentage', 'MySql Intermediário Score',
                                     'PATRONES DE DISEÑO Percentage', 'PATRONES DE DISEÑO Score',
                                     'PHP 5 Avanzado Percentage', 'PHP 5 Avanzado Score',
                                     'PHP Avanzado Percentage', 'PHP Avanzado Score',
                                     'PYTHON Percentage', 'PYTHON Score',
                                     'SEO AVANZADO Percentage', 'SEO AVANZADO Score',
                                     'Sql Intermediário Percentage', 'Sql Intermediário Score',
                                     'WEB DESIGN Percentage', 'WEB DESIGN Score',
                                     'Wordpress Avanzado Percentage', 'Wordpress Avanzado Score',
                                     'Wordpress Intermediário Percentage', 'Wordpress Intermediário Score'
                                     ]

for profile_link in my_profile_links:
    driver.get(profile_link)
    driver.maximize_window()
    # worker_name_xpath = "//*[@id='section-personal-data']/div[1]"
    # worker_tagline_xpath = "//*[@id='section-personal-data']/h4"
    # worker_profile_url = profile_link
    # worker_rating_xpath = "//*[@id='section-personal-data']//*[@class = 'average']"
    # worker_country_xpath = "//*[@id='section-personal-data']//*[@class = 'country-name']/a"
    # worker_hourly_rate_xpath = "//*[@id='section-personal-data']//*[@class = 'hourly-rate']/h3"
    # worker_main_skill_xpath = "//*[@id='section-personal-data']//*[@class = 'main-skill']/span"
    #
    # #box common main div
    # worker_ranking_workana = "//*[@class='box-common']//*[contains(@class, 'ranking')]/p[1]"
    #
    # #ata

    worker_country_ranking_xpath = "//*[@class='box-common']//*[contains(@class, 'ranking')]"
    # worker_completed_projects_xpath ="//*[@class='box-common']//*[contains(@class, 'rating')]/p[1]/text()"
    # worker_hours_worked_xpath = "//*[@class='box-common']//*[contains(@class, 'rating')]/p[2]/text()"
    # # worker_profile_level_xpath = "//*[@class='box-common']//*[contains(@class, 'rating')]//*[contains(@class, 'hidden-xs')]/text()"
    # worker_number_of_certificates_xpath = "//*[@class='box-common']//*[contains(@class, 'rating')]//*[contains(@href, '#section-certifications')]"
    # worker_rating_from_clients_xpath = "//*[@class='box-common']//*[contains(@class, 'rating')]//*[contains(@href, '#section-ratings')]"
    # worker_last_login_xpath = "//*[@class='box-common']//*[contains(@class, 'activity')]/p[2]/span"
    # worker_registered_xpath = "//*[@class='box-common']//*[contains(@class, 'activity')]/p[3]/span"
    # worker_my_top_skills_xpath = ""
    # worker_about_me_xpath = "//*[@id='collapse-about-me']/div/text()"
    # worker_work_history_xpath = "//*[@id='collapse-work-history']/div"
    # worker_work_history_details_xpath = "//*[@id='collapse-work-history']//*[contains(@class, 'expander-details')]"
    # worker_languages_level_xpath = "//*[@id='collapse-languages']/ul"
    # worker_certificate_table_xpath = "//*[@id='certifications-table']/tbody"


    # post_name = driver.find_element_by_xpath(worker_name_xpath).text
    # post_tagline = driver.find_element_by_xpath(worker_tagline_xpath).text
    # post_profile_url = worker_profile_url
    # post_rating = driver.find_element_by_xpath(worker_rating_xpath).text
    # post_country = driver.find_element_by_xpath(worker_country_xpath).text
    # post_hourly_rate = driver.find_element_by_xpath(worker_hourly_rate_xpath).text
    # post_main_skill = driver.find_element_by_xpath(worker_main_skill_xpath).text
    # post_ranking_workana = driver.find_element_by_xpath(worker_ranking_workana).text
    post_country_ranking = driver.find_element_by_xpath(worker_country_ranking_xpath).text





    print(type(post_country_ranking))


