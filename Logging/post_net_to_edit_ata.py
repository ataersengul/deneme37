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
import logging


def encode_text(my_text):
    return my_text.encode("utf-8")

def scroll_down_my_page(driver):
    for i in range(0, int(5)):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # logger.info("Preparing Page: " + str(i + 1))
        # time.sleep(1)

def savetoCsv(Foldername, FileName, HeadersAsList, RowsAsList, PostID):

    try:
        FileNameCorrected = FileName.replace(":", "")
        if not os.path.exists(Foldername):
            os.makedirs(Foldername)
        with open(Foldername + "\\" + FileNameCorrected + '.csv', 'a') as csvfile:
            fieldnames = HeadersAsList
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            fileEmpty = os.stat(Foldername + "\\" + FileNameCorrected + '.csv').st_size == 0
            if fileEmpty:
                writer.writeheader()
            writer.writerows(RowsAsList)
            logger.info("*" * 3 + PostID + "*" * 3)
            # example fieldnames:myFieldnames = ['header1', 'header2', 'header3']
            # example rows: myRow = [{'header1': "deneme1", 'header2': "deneme2", 'header3': "deneme3"}]
    except:
        print("**")

def saveImageFromUrl(pathToSave, FileName, imageLink):
    if not os.path.exists(pathToSave):
        os.makedirs(pathToSave)
    with open(pathToSave + '\\' + str(FileName) + '.jpg', 'wb') as handle:
        response = requests.get(imageLink, stream=True)

        if not response.ok:
            logger.info(response)

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)


def unixTimeFormatter(unixTime):
    dateCorrected = datetime.utcfromtimestamp(int(unixTime)).strftime('%Y%m%d%H%M%S')
    return dateCorrected

#region loggingProperty(logger)

# create logger
logger = logging.getLogger('logging')
logger.setLevel(logging.INFO)

# create console handler and set level to info
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.INFO)

# create formatter
formatter = logging.Formatter('%(message)s',
            datefmt='%m/%d/%Y %I:%M:%S %p')

# add formatter to console handler
consoleHandler.setFormatter(formatter)

# add console handler to logger
logger.addHandler(consoleHandler)

# Log kayıt yolunu belirleme
logging.basicConfig(filename='logging.log',
                    format='%(asctime)s - %(levelname)s: %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p',
                    filemode='w',
                    level=logging.INFO)

# # logging messages
# logger.debug('debug message')
# logger.info('info message')
# logger.warning('warn message')
# logger.error('error message')
# logger.critical('critical message')

#endregion

#read from csv
my_links = []
logger.info("Getting Links from 'PostUpdates' CSV file...")
try:
    with open('PostUpdates.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            link = row['LinkToPost']
            my_links.append(link)
        my_links_count = str(len(my_links))
        logger.info("All Links from 'PostUpdates' CSV file are received. Number of links received: " + my_links_count)

except:
    logger.error("'PostUpdates' CSV file is missing or corrupted, please check.")
    time.sleep(10)
    sys.exit()


def get_post_details(my_link):
    COMMENTS_FILE_HEADERS = ['Date','Contact','Details','Media']
    POST_AND_COMMENTS_FILE_HEADERS = ['PostId','PostText','PosterName','PostDate','CommentDate','CommentContact','CommentDetails','CommentMedia']
    my_comment_image_file_name = ""
    group_id_from_link = my_link
    group_id_from_link = group_id_from_link.split('groups')

    group_id_from_link = group_id_from_link[1].split('permalink')
    group_id_from_link = group_id_from_link[0].replace("/", "")

    post_id_from_url = my_link
    post_id_from_url = post_id_from_url.split('permalink')
    post_id_from_url = post_id_from_url[1].replace("/", "")
    logger.info("Getting details for Post id: " + post_id_from_url)


    logger.info("Preparing browser")
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('lang=en')
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    options.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome(chrome_options=options)

    #driver = webdriver.Chrome()
    # driver.get("https://www.facebook.com/groups/" + groupID + "//")
    driver.get(my_link)

    my_postId = post_id_from_url
    my_post_text = ""
    my_poster_name_text = ""
    my_post_date = ""
    my_comment_text = ""
    my_comment_actor_text = ""
    my_comment_date = ""
    group_mall_formatted = "group_mall_" + "5658649590"

    #get post text
    post_text_xpath = "//*[starts-with(@id, 'group_mall_" + group_id_from_link + "')]//*[starts-with(@id, 'u_')]//p"
    post_text_element = driver.find_elements_by_xpath(post_text_xpath)
    for text in post_text_element:
        my_post_text = my_post_text + text.text
    # logger.info(my_post_text)


    #get poster name

    poster_name_xpath = "(//*[starts-with(@id, 'group_mall_" + group_id_from_link + "')]//*[starts-with(@id, 'u_')]//h5//span)[3]"

    poster_name_element = driver.find_elements_by_xpath(poster_name_xpath)
    for poster_name in poster_name_element:
        my_poster_name_text = poster_name.text

    # logger.info(my_poster_name_text)

    #get post date
    post_date_xpath = "//*[starts-with(@id, 'group_mall_" + group_id_from_link + "')]//*[starts-with(@id, 'feed_subtitle_')]//abbr"
    post_date_element = driver.find_elements_by_xpath(post_date_xpath)
    for date in post_date_element:
        my_post_date = date.get_attribute("data-utime")

    my_post_date = unixTimeFormatter(my_post_date)
    # logger.info(my_post_date)


     #writePostDetails to csv
    if not os.path.exists("Posts"):
        os.makedirs("Posts")
    with open("Posts\\" + "AllPosts" + '.csv', 'a') as csvfile:
        fieldnames = POST_AND_COMMENTS_FILE_HEADERS

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        fileEmpty = os.stat("Posts\\" + "AllPosts" + '.csv').st_size == 0
        if fileEmpty:
            writer.writeheader()
        writer.writerows([{'PostId': my_postId,'PostText': encode_text(my_post_text), 'PosterName': encode_text(my_poster_name_text),
                           'PostDate': my_post_date, 'CommentDate': "",
                           'CommentContact': "", 'CommentDetails': "", 'CommentMedia': ""}])
        logger.info("*" * 3 + " Post ID: " + my_postId + " Saved" + "*" * 3)

    #get post image
    post_image_xpath = "//*[starts-with(@id, 'group_mall_" + group_id_from_link + "')]//*[starts-with(@id, 'u_')]//*[starts-with(@class,'uiScaledImageContainer')]//img"
    post_image_elements = driver.find_elements_by_xpath(post_image_xpath)
    for post_image in post_image_elements:
        post_image_url = post_image.get_attribute("src")
        my_post_image_file_name = my_postId + "_" + my_post_date
        saveImageFromUrl('PostsMedia', my_post_image_file_name,post_image_url)

    #open all the comments and replies
    comment_click_xpath = "//*[starts-with(@id, 'group_mall_" + group_id_from_link + "')]//*[contains(@aria-label,'comment')]"
    comment_click_element = driver.find_elements_by_xpath(comment_click_xpath)
    for comment_to_click in comment_click_element:
        comment_to_click.click()
        logger.info("Expanding comments and replies...")

    time.sleep(2)

    comment_expand_xpath = "//*[starts-with(@id, 'group_mall_" + group_id_from_link + "')]//*[@class = 'UFIPagerLink']"
    comment_expand_click_element = driver.find_elements_by_xpath(comment_expand_xpath)
    for comment_expand in comment_expand_click_element:
        comment_expand.click()
        logger.info("Expanding comments and replies...")
        scroll_down_my_page(driver)
        time.sleep(1)
    #expand all replies
    comment_replies_xpath = "//*[starts-with(@id, 'group_mall_" + group_id_from_link + "')]//*[@class = 'UFIReplySocialSentenceLinkText']"
    comment_replies_element = driver.find_elements_by_xpath(comment_replies_xpath)
    for comment_replies_expand in comment_replies_element:
        comment_replies_expand.click()
        logger.info("Expanding comments and replies...")
        scroll_down_my_page(driver)
        time.sleep(1)

    comment_expand_xpath = "//*[starts-with(@id, 'group_mall_" + group_id_from_link + "')]//*[@class = 'UFIPagerLink']"
    comment_expand_click_element = driver.find_elements_by_xpath(comment_expand_xpath)
    for comment_expand in comment_expand_click_element:
        comment_expand.click()
        logger.info("Expanding comments and replies...")
        scroll_down_my_page(driver)
        time.sleep(1)




    time.sleep(2)
    scroll_down_my_page(driver)
    comment_body_xpath_template = "//*[starts-with(@id, 'group_mall_" + group_id_from_link + "')]//*[@id='{0}']//*[@class='UFICommentBody']"
    comment_body_actor_xpath_template = "//*[starts-with(@id, 'group_mall_" + group_id_from_link + "')]//*[@id='{0}']//*[@class=' UFICommentActorName']"
    comment_body_date_xpath_template = "//*[starts-with(@id, 'group_mall_" + group_id_from_link + "')]//*[@id='{0}']//*[@class= 'UFISutroCommentTimestamp livetimestamp']"
    comment_body_image_xpath_template = "//*[starts-with(@id, 'group_mall_" + group_id_from_link + "')]//*[@id='{0}']//*[@class= 'scaledImageFitHeight img']"
    Comment_see_more_links_xpath_template = "//*[@id='{0}']//*[text()='See more']"


    #get all comments
    comments_all_containers_xpath = "//*[starts-with(@id, 'group_mall_" + group_id_from_link + "')]//*[starts-with(@id, 'comment_js')]"
    comments_all_containers_element = driver.find_elements_by_xpath(comments_all_containers_xpath)


    #looping in all comments
    for comment_container in comments_all_containers_element:
        #get comment id
        unique_comment_container_id = comment_container.get_attribute("id")
        formatted_comment_body_xpath = comment_body_xpath_template.format(unique_comment_container_id)
        formatted_comment_body_actor_xpath = comment_body_actor_xpath_template.format(unique_comment_container_id)
        formatted_comment_body_date_xpath = comment_body_date_xpath_template.format(unique_comment_container_id)
        formatted_comment_body_image_xpath = comment_body_image_xpath_template.format(unique_comment_container_id)
        formatted_Comment_see_more_links_xpath = Comment_see_more_links_xpath_template.format(unique_comment_container_id)
        comment_body_element = driver.find_elements_by_xpath(formatted_comment_body_xpath)
        comment_see_more_element = driver.find_elements_by_xpath(formatted_Comment_see_more_links_xpath)

        for see_more_link in comment_see_more_element:
            see_more_link.click()

        for comment_body in comment_body_element:
            my_comment_text = comment_body.text
            # logger.info(my_comment_text)
        comment_body_actor_element = driver.find_elements_by_xpath(formatted_comment_body_actor_xpath)
        for actor in comment_body_actor_element:
            my_comment_actor_text = actor.text
            # logger.info(my_comment_actor_text)
        comment_body_date_element = driver.find_elements_by_xpath(formatted_comment_body_date_xpath)
        for date in comment_body_date_element:
            my_comment_date = date.get_attribute("data-utime")
            my_comment_date_formatted = unixTimeFormatter(my_comment_date)
            # logger.info(my_comment_date_formatted)



        #get images
        comment_image_element = driver.find_elements_by_xpath(formatted_comment_body_image_xpath)
        if comment_image_element:
            for image in comment_image_element:
                image_url = image.get_attribute("src")
                my_comment_image_file_name = my_postId + "_" + my_comment_date
                saveImageFromUrl("Comments Media", my_comment_image_file_name, image_url)

    #write comments to csv
        commentAsListToWrite = [{'PostId': my_postId,'PostText': "", 'PosterName': "", 'PostDate': "", 'CommentDate': my_comment_date,
                                 'CommentContact': encode_text(my_comment_actor_text),
                                 'CommentDetails': encode_text(my_comment_text), 'CommentMedia': my_comment_image_file_name}]
        savetoCsv("Posts\\", "AllPosts", POST_AND_COMMENTS_FILE_HEADERS,
              commentAsListToWrite, "Comment contents of " + my_postId + " is saved.")

    driver.quit()


for link in my_links:
    try:
        get_post_details(link)
    except:
        logger.info("**")