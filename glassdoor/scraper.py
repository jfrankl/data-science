'''
Example of web scraping using Python and BeautifulSoup. 
Sraping ESPN College Football data 
http://www.espn.com/college-sports/football/recruiting/databaseresults/_/sportid/24/class/2006/sort/school/starsfilter/GT/ratingfilter/GT/statuscommit/Commitments/statusuncommit/Uncommited
The script will loop through a defined number of pages to extract footballer data. 
'''

from bs4 import BeautifulSoup
import requests
import os 
import os.path
import csv 
import time 


def writerows(rows, filename):
	with open(filename, 'a', encoding='utf-8') as toWrite:
		writer = csv.writer(toWrite)
		writer.writerows(rows)
 

def process_text(html):
	if html is None:
		return ""
	else: 
		return html.getText().replace("\t", " ").replace("\r", " ").replace("\n", " ")

def get_reviews(pageurl):
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}

	try:
		response = requests.get(pageurl, headers=headers)
	except requests.exceptions.RequestException as e:
		print(e)
		exit()

	soup = BeautifulSoup(response.text, "html.parser")

	review = []

	rows = soup.find_all("li", {"class": "empReview"})

	for row in rows:     
		
		rating = process_text(row.find("span", {"class": "ratingNumber"}))
		datetitle = process_text(row.find("span", {"class": "authorJobTitle"})).split(" - ")
		date = datetitle[0]
		title = datetitle[1]
		tenure = process_text(row.find("span", {"class": "eg4psks0"}))
		location = process_text(row.find("span", {"class": "authorLocation"}))
		pros = process_text(row.find("span", {"data-test": "pros"}))
		cons = process_text(row.find("span", {"data-test": "cons"}))

		review.append([rating, date, title, tenure, location, pros, cons])

	return review


if __name__ == "__main__":
	filename = "output/uline_reviews_en2.csv"
	if os.path.exists(filename):
		os.remove(filename)
	
	baseurl = "https://www.glassdoor.com/Reviews/Uline-Reviews-E26828_P" 
	page = 1
	parturl = ".htm?sort.sortType=RD&sort.ascending=false&filter.iso3Language=eng&filter.employmentStatus=PART_TIME&filter.employmentStatus=CONTRACT&filter.employmentStatus=REGULAR&filter.employmentStatus=FREELANCE&filter.employmentStatus=INTERN"

	# Add header row
	writerows([["rating", "date", "title", "tenure", "location", "pros", "cons"]], filename)

	while page < 115:
		pageurl = baseurl + str(page) + parturl
		reviews = get_reviews(pageurl)

		writerows(reviews, filename)

		# take a break
		time.sleep(3)

		page += 1

if page > 1:
	print("Pages fetched successfully.")