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

COMMENTS_FILE_HEADERS = ['Date', 'Contact', 'Details', 'Media']
POST_AND_COMMENTS_FILE_HEADERS = ['PostText', 'PosterName', 'PostDate', 'CommentDate', 'CommentContact',
                                  'CommentDetails', 'CommentMedia']
P_formattedLastCommentPostDate = ""
# checking Arguments
try:
    parser = argparse.ArgumentParser()
    parser.add_argument("Page Count", help="Enter the page count you want to get", type=int)
    parser.add_argument("GroupID", help="Enter the group id you want to scrape", type=str)
    args = parser.parse_args()

    pageCount = sys.argv[1]
    groupID = sys.argv[2]
except:
    pageCount = 2
    groupID = "5658649590"
    # groupID = "tijuanamakesmehungry"
    print("Default: Page Count " + str(pageCount))


def convert(t):
    with io.StringIO() as fd:
        for c in t:  # replace all chars outside BMP with a !
            dummy = fd.write(c if ord(c) < 0x10000 else '!')
        return fd.getvalue()


def encode_text(my_text):
    return my_text.encode("utf-8")


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
            print("*" * 3 + PostID + "*" * 3)
            # example fieldnames:myFieldnames = ['header1', 'header2', 'header3']
            # example rows: myRow = [{'header1': "deneme1", 'header2': "deneme2", 'header3': "deneme3"}]
    except:
        print("Ecxeption while writing csv")


def unixTimeFormatter(unixTime):
    dateCorrected = datetime.utcfromtimestamp(int(unixTime)).strftime('%Y%m%d%H%M%S')
    formattedLastCommentPostDate = str(LastCommentPostDate).replace(" ", "")
    formattedLastCommentPostDate = str(formattedLastCommentPostDate).replace(",", "")
    formattedLastCommentPostDate = str(formattedLastCommentPostDate).replace(":", "")
    formattedLastCommentPostDate = str(formattedLastCommentPostDate).replace("/", "")
    formattedLastCommentPostDate = str(formattedLastCommentPostDate).replace("-", "")
    return dateCorrected


def saveImageFromUrl(pathToSave, FileName, imageLink):
    if not os.path.exists(pathToSave):
        os.makedirs(pathToSave)
    with open(pathToSave + '\\' + str(FileName) + '.jpg', 'wb') as handle:
        response = requests.get(imageLink, stream=True)

        if not response.ok:
            print(response)

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)


print("Preparing Files & Folders")
with open('PostUpdates.csv', 'w') as csvfile:
    fieldnames = ['WallPostId', 'PostDate', 'LinkToPost']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

with open('PostsSkipped.csv', 'w') as csvfile:
    fieldnames = ['WallPostId']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

print("Preparing browser")
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
prefs = {"profile.default_content_setting_values.notifications": 2}
options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(chrome_options=options)

# driver = webdriver.Chrome()
driver.get("https://www.facebook.com/groups/" + groupID + "//")

# scroll down all the way
for i in range(0, int(pageCount)):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    print("Preparing Page: " + str(i + 1))
    time.sleep(3)

time.sleep(10)
elementsWallPostDiv = driver.find_elements_by_xpath("//*[starts-with(@id, 'mall_post')]")
elementsImages = driver.find_elements_by_xpath(
    "//*[starts-with(@id, 'mall_post')]//*[starts-with(@id, 'u_')]//*[starts-with(@class,'uiScaledImageContainer')]//img")

print(str(len(elementsWallPostDiv)) + " Posts will be saved")
print(str(len(elementsImages)) + " Media will be saved")

try:
    for wallPost in elementsWallPostDiv:
        wallPostId = wallPost.get_property("id")
        WallPostTextXpathWithId = "//*[@id='{0}']//*[starts-with(@id, 'u_')]//p"
        WallPostPosterNameXpathWithId_active = "(//*[@id='{0}']//*[starts-with(@id, 'u_')]//h5//span)[3]"
        WallPostLastCommentDateXpathWithId = "//*[@id='{0}']//*[starts-with(@id, 'comment_')][//abbr][1]//abbr"
        WallPostDateXpathWithId = "//*[@id='{0}']//*[starts-with(@id, 'feed_subtitle_')]//abbr"
        # Comments
        WallPostMoreCommentLinkXpathWithID = "//*[@id='{0}']//*[@class = 'UFIPagerLink']"
        WallPostSeeMoreLinkXpathWithId = "//*[@id='{0}']//*[@class = 'see_more_link_inner']"
        WallPostAllRepliesXpathWithId = "//*[@id='{0}']//*[@class = 'UFIReplySocialSentenceLinkText']"

        WallPostAllCommentsXpath = "//*[@id='{0}']//*[starts-with(@id, 'comment_js')]"
        WallPostUniqueCommentActorXpathWithId = "//*[@id='{0}']//*[@id='{1}']//*[@class=' UFICommentActorName']"
        WallPostUniqueCommentTextXpathWithId = "//*[@id='{0}']//*[@id='{1}']//*[@class='UFICommentBody']"
        WallPostUniqueTimestampXpathWithId = "//*[@id='{0}']//*[@id='{1}']//*[@class= 'UFISutroCommentTimestamp livetimestamp']"
        WallPostUniqueImgXpathWithId = "//*[@id='{0}']//*[@id='{1}']//*[@class= 'scaledImageFitHeight img']"

        # Post Links
        WallPostlinkXpathWithId = "//*[@id='feed_subtitle_{0}']/span[3]/span/a"

        # Formations
        # Formatted Posts
        FormattedWallPostXpathWithId = WallPostTextXpathWithId.format(wallPostId)
        FormattedWallPostPosterNameXpathWithId = WallPostPosterNameXpathWithId_active.format(wallPostId)
        FormattedWallPostLastCommentDateXpathWithId = WallPostLastCommentDateXpathWithId.format(wallPostId)
        FormattedWallPostDateXpathWithId = WallPostDateXpathWithId.format(wallPostId)
        # Formatted Comments
        FormattedWallPostMoreCommentLinkXpathWithID = WallPostMoreCommentLinkXpathWithID.format(wallPostId)
        FormattedWallPostSeeMoreLinkXpathWithId = WallPostSeeMoreLinkXpathWithId.format(wallPostId)
        FormattedWallPostAllRepliesXpathWithId = WallPostAllRepliesXpathWithId.format(wallPostId)
        FormattedWallPostAllCommentsXpath = WallPostAllCommentsXpath.format(wallPostId)
        # Formatted Links
        FormattedWallPostlinkXpathWithId = WallPostlinkXpathWithId.format(wallPostId)
        FormattedWallPostlinkXpathWithId = str(FormattedWallPostlinkXpathWithId).replace("mall_post_", "")

        try:
            PostText = driver.find_element_by_xpath(FormattedWallPostXpathWithId).text
            PosterName = driver.find_element_by_xpath(FormattedWallPostPosterNameXpathWithId).text
            PostLink = driver.find_element_by_xpath(FormattedWallPostlinkXpathWithId).get_attribute("href")

            try:
                LastCommentPostDate = driver.find_element_by_xpath(
                    FormattedWallPostLastCommentDateXpathWithId).get_attribute("data-utime")

            except:
                LastCommentPostDate = driver.find_element_by_xpath(FormattedWallPostDateXpathWithId).get_attribute(
                    "data-utime")
            print("*" * 3 + " Post ID: " + wallPostId + " Prepared" + "*" * 3)

            try:
                # convert UnixTime to YYYY/MM/DD/hh/mm/ss
                LastCommentPostDate = datetime.utcfromtimestamp(int(LastCommentPostDate)).strftime('%Y%m%d%H%M%S')
                formattedLastCommentPostDate = str(LastCommentPostDate).replace(" ", "")
                formattedLastCommentPostDate = str(formattedLastCommentPostDate).replace(",", "")
                formattedLastCommentPostDate = str(formattedLastCommentPostDate).replace(":", "")
                formattedLastCommentPostDate = str(formattedLastCommentPostDate).replace("/", "")
                formattedLastCommentPostDate = str(formattedLastCommentPostDate).replace("-", "")
                P_formattedLastCommentPostDate = formattedLastCommentPostDate
                FormattedwallPostID = wallPostId[:27]
                FormattedwallPostID = FormattedwallPostID.replace(":", "")

                if not os.path.exists("Posts"):
                    os.makedirs("Posts")
                with open("Posts\\" + formattedLastCommentPostDate + "_" + FormattedwallPostID + '.csv',
                          'w') as csvfile:
                    fieldnames = POST_AND_COMMENTS_FILE_HEADERS

                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows([{'PostText': encode_text(PostText), 'PosterName': encode_text(PosterName),
                                       'PostDate': LastCommentPostDate, 'CommentDate': "",
                                       'CommentContact': "", 'CommentDetails': "", 'CommentMedia': ""}])
                    print("*" * 3 + " Post ID: " + wallPostId + " Saved" + "*" * 3)

                with open('PostUpdates.csv', 'a') as csvfile:
                    fieldnames = ['WallPostId', 'PostDate', 'LinkToPost']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    wallPostIdFormatted = wallPostId[:27]
                    writer.writerows([{'WallPostId': convert(wallPostIdFormatted), 'PostDate': LastCommentPostDate,
                                       'LinkToPost': PostLink}])

            except:
                print("There is special char in Post: " + wallPostId + ", skipping")
                with open('PostsSkipped.csv', 'a') as csvfile:
                    fieldnames = ['WallPostId']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writerows([{'WallPostId': wallPostId}])

        except:
            print("-" * 20 + "No text found in post. Skipping: " + FormattedWallPostXpathWithId + " " + "-" * 20)
            with open('PostsSkipped.csv', 'a') as csvfile:
                fieldnames = ['WallPostId']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerows([{'WallPostId': wallPostId}])

        MoreCommentElements = driver.find_elements_by_xpath(FormattedWallPostMoreCommentLinkXpathWithID)

        # if there is Load more comment link or more replies, clicks it
        try:
            if MoreCommentElements:
                for moreLink in MoreCommentElements:
                    moreLink.click()
                    print("Expanding...")
                    time.sleep(1)

            SeeMoreElements = driver.find_elements_by_xpath(FormattedWallPostSeeMoreLinkXpathWithId)

            if SeeMoreElements:
                for seeMoreLink in SeeMoreElements:
                    seeMoreLink.click()
                    print("Expanding...")
                    time.sleep(1)

            AllRepliesLinkElements = driver.find_elements_by_xpath(FormattedWallPostAllRepliesXpathWithId)

            if AllRepliesLinkElements:
                for allRepliesLink in AllRepliesLinkElements:
                    allRepliesLink.click()
                    time.sleep(1)
        except:
            print("**!**")
        # get all comments for a post ID

        AllCommentsforPostElements = driver.find_elements_by_xpath(FormattedWallPostAllCommentsXpath)
        if AllCommentsforPostElements:

            for CommentBlock in AllCommentsforPostElements:
                CommentBlockId = CommentBlock.get_attribute("id")
                FormattedWallPostUniqueCommentActorXpathWithId = WallPostUniqueCommentActorXpathWithId.format(
                    wallPostId, CommentBlockId)
                FormattedWallPostUniqueCommentTextXpathWithId = WallPostUniqueCommentTextXpathWithId.format(wallPostId,
                                                                                                            CommentBlockId)
                FormattedWallPostUniqueTimestampXpathWithId = WallPostUniqueTimestampXpathWithId.format(wallPostId,
                                                                                                        CommentBlockId)
                FormattedWallPostUniqueImgXpathWithId = WallPostUniqueImgXpathWithId.format(wallPostId, CommentBlockId)
                CommentActors = driver.find_elements_by_xpath(FormattedWallPostUniqueCommentActorXpathWithId)
                CommentTexts = driver.find_elements_by_xpath(FormattedWallPostUniqueCommentTextXpathWithId)
                CommentDates = driver.find_elements_by_xpath(FormattedWallPostUniqueTimestampXpathWithId)
                CommentMedias = driver.find_elements_by_xpath(FormattedWallPostUniqueImgXpathWithId)
                FormattedwallPostID = wallPostId[:27]
                CommentImageFileName = ""

                try:
                    myCommentActor = CommentActors[0].text
                    MyCommentText = CommentTexts[0].text
                    MyCommentDate = CommentDates[0].get_attribute("data-utime")
                    MyCommentDate = unixTimeFormatter(MyCommentDate)
                    if CommentMedias:
                        for CommentMedia in CommentMedias:
                            CommentMediaUrl = CommentMedia.get_attribute("src")
                            CommentImageFileName = FormattedwallPostID + "_" + MyCommentDate
                            saveImageFromUrl("Comments Media", CommentImageFileName, CommentMediaUrl)

                except:
                    myCommentActor = "Exception, Please check the post: " + wallPostId
                    MyCommentText = "Exception, Please check the post: " + wallPostId
                    MyCommentDate = "Exception, Please check the post: " + wallPostId

                FormattedwallPostID = wallPostId[:27]
                commentAsListToWrite = [{'PostText': "", 'PosterName': "", 'PostDate': "", 'CommentDate': MyCommentDate,
                                         'CommentContact': encode_text(myCommentActor),
                                         'CommentDetails': encode_text(MyCommentText),
                                         'CommentMedia': CommentImageFileName}]
                savetoCsv("Posts\\", P_formattedLastCommentPostDate + "_" + FormattedwallPostID,
                          POST_AND_COMMENTS_FILE_HEADERS, commentAsListToWrite,
                          "Comment contents of " + FormattedwallPostID + " is saved.")
except:
    print(*"")

i = 0
print("Saving Media...")
for image in elementsImages:
    imageLink = image.get_attribute("src")
    imagePostIdElements = image.find_elements(By.XPATH, "ancestor::*[starts-with(@id, 'mall_post')]")
    imagePostId = imagePostIdElements[0].get_attribute("id")
    imagePostId = str(imagePostId).replace(":", "")
    imagePostId = imagePostId[:27]
    i = i + 1
    print("Media " + str(i) + str("/") + str(len(elementsImages)) + " Saved")

    if not os.path.exists("PostsMedia"):
        os.makedirs("PostsMedia")
    with open('PostsMedia\\' + str(imagePostId) + '.jpg', 'wb') as handle:
        response = requests.get(imageLink, stream=True)

        if not response.ok:
            print(response)

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)

driver.quit()
print("Done." + str(len(elementsWallPostDiv)) + " Post Information has been saved.")
