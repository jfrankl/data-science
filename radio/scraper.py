"""
Example of web scraping using Python and BeautifulSoup. 
Sraping ESPN College Football data 
http://www.espn.com/college-sports/football/recruiting/databaseresults/_/sportid/24/class/2006/sort/school/starsfilter/GT/ratingfilter/GT/statuscommit/Commitments/statusuncommit/Uncommited
The script will loop through a defined number of pages to extract footballer data. 
"""

from bs4 import BeautifulSoup
import requests
import os
import os.path
import csv
import time


# def writerows(rows, filename):
#     with open(filename, "a", encoding="utf-8") as toWrite:
#         writer = csv.writer(toWrite)
#         writer.writerows(rows)


def process_text(html):
    if html is None:
        return ""
    else:
        return html.getText().replace("\t", " ").replace("\r", " ").replace("\n", " ")


def get_download_url(pageurl):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
    }

    try:
        response_search = requests.get(pageurl, headers=headers)
        soup_search = BeautifulSoup(response_search.text, "html.parser")
        for a in soup_search.find_all("h3", {"class": "title"}):
            time.sleep(1)
            url_detail = a.find("a")["href"]
            print(url_detail)
            response_detail = requests.get(url_detail, headers=headers)
            soup_detail = BeautifulSoup(response_detail.text, "html.parser")
            url_download = soup_detail.find("a", {"title": "Download"})["href"]
            print(url_download)

            filename = "output/urls.txt"
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, "a") as file:
                file.write(url_download)
                file.write("\n")
    except requests.exceptions.RequestException as e:
        print(e)
        exit()


if __name__ == "__main__":
    baseurl = "https://www.kins1063.com/page/"
    page = 1
    parturl = "/?s=arkley"

    while page < 11:
        pageurl = baseurl + str(page) + parturl
        reviews = get_download_url(pageurl)

        # take a break
        time.sleep(1)

        page += 1

if page > 1:
    print("Pages fetched successfully.")
