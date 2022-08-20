import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

collegeIds = ["iit-madras", "iit-delhi", "iit-bombay", "iit-kanpur", "iit-kharagpur", "iit-roorkee", "iit-guwahati", "iit-hyderabad", "iit-ism-dhanbad", "iit-indore", "iit-bhu-varanasi",
              "iit-ropar", "iit-patna", "iit-gandhinagar", "iit-bhubaneswar", "iit-mandi", "iit-jodhpur", "iit-tirupati", "iit-bhilai", "iit-goa", "iit-jammu", "iit-dharwad", "iit-palakkad"]
#collegeIds = ["iit-madras"]
categoryIds = ["op-gn", "bc-gn"]
roundNumbers = [1, 6]
data = {"college": [""], "G_R1_O_R": [""], "G_R1_C_R": [""], "G_R6_O_R": [""], "G_R6_C_R": [
    ""], "OBCNCL_R1_O_R": [""], "OBCNCL_R1_C_R": [""], "OBC_NCL_R6_O_R": [""], "OBC_NCL_R6_C_R": [""]}
df = pd.DataFrame(data)

for college in collegeIds:
    # url of the page we want to scrape
    dfRow = [college]
    url = "https://www.collegepravesh.com/cutoff/" + college + "-cutoff-2021/"

    # initiating the webdriver. Parameter includes the path of the webdriver.
    driver = webdriver.Chrome(
        'C:\\DRIVERS\\chromedriver_win32\\chromedriver.exe')
    driver.get(url)

    # this is just to ensure that the page is loaded
    time.sleep(5)

    html = driver.page_source

    # this renders the JS code and stores all
    # of the information in static HTML code.

    # Now, we could simply apply bs4 to html variable
    soup = BeautifulSoup(html, "html.parser")
    # print(soup.prettify())
    print("College:" + college)
    for categoryId in categoryIds:
        print("categoryId:" + categoryId)
        cutoffContainerHtml = soup.find(id=categoryId)
        for roundNumber in roundNumbers:
            round1Tab = cutoffContainerHtml.find_all(
                class_="pane")[roundNumber - 1]  # Gives round 1 details
            allRows = round1Tab.find_all('tr')
            for rowCount in range(0, len(allRows)):
                row = allRows[rowCount].find_all('td')
                # print(row)
                if (row[0].string == "Computer Science and Engineering"):
                    print("Round", roundNumber, ": ")
                    print("Opening Rank:" + row[1].string)
                    dfRow.append(row[1].string)
                    print("Closing Rank:" + row[2].string)
                    dfRow.append(row[2].string)
                    break
    print()
    print(dfRow)
    df.loc[len(df)] = dfRow
    print(df)

driver.close()
df.to_excel("iitCutoffs.xlsx")
