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
import random

headers = {
	"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
}

cookies = {
    "iabbb_accredited_search": "false",
}

def random_sleep():
	return time.sleep(random.uniform(0, 1))

def writerows(rows, filename):
	with open(filename, 'a', encoding='utf-8') as toWrite:
		writer = csv.writer(toWrite)
		writer.writerows(rows)

def get_businesses(pageurl):
	try:
		response_search = requests.get(pageurl, headers=headers, cookies=cookies)
		soup_search = BeautifulSoup(response_search.text, "html.parser")
		all_links = soup_search.find_all("a", {"class": ["text-blue-medium", "css-1jw2l11", "eou9tt70"]})
		print(f"Number of things on this page {len(all_links)}")
		# print(soup_search.find_all("h1", {"class": ["font-normal", "text-black", "css-1tkwvbe", "e1o9no5h2"]}))
		businesses = []
		for a in all_links:
			url = a["href"]
			split_hyphen = url.split("-")
			split_slash = url.split("/")
			businessId = split_hyphen[-1]
			bbbId = split_hyphen[-2]
			country = split_slash[3]
			state = split_slash[4]
			city = split_slash[5]
			businesses.append({"businessId": businessId, "bbbId": bbbId, "country": country, "state": state, "city": city, "url": url})
	except requests.exceptions.RequestException as e:
		print(e)
		exit()
	return businesses

def get_reviews(pageurl, city, state, country, business_website):
	try:
		response = requests.get(pageurl, headers=headers).json()
	except requests.exceptions.RequestException as e:
		print(e)
		exit()

	review = []

	for entry in response['items']:   
		rating = entry['reviewStarRating']
		name = entry['displayName']

		if entry['hasExtendedText']:
			final_entry = entry['extendedText'][0]
		else:
			final_entry = entry

		
		the_id = final_entry['id']
		date = f"{final_entry['date']['year']}-{final_entry['date']['month']}-{final_entry['date']['day']}"
		text = final_entry['text']
		review.append([country, state, city, rating, name, the_id, date, text, pageurl, business_website])

	return review


if __name__ == "__main__":
	filename = "output/bbb-reviews.csv"
	if os.path.exists(filename):
		os.remove(filename)

	filename_meta = "output/bbb-meta.csv"
	if os.path.exists(filename_meta):
		os.remove(filename_meta)

	# Add header row
	writerows([["country", "state", "city", "rating", "name", "id", "date", "text", "source", "website"]], filename)
	writerows([["country", "state", "city", "businessId", "bbbId", "review_page_count", "review_url", "business_url"]], filename_meta)

	business_url = "https://www.bbb.org/search?sort=Rating&find_country=USA&find_text=homevestors&page="
	business_page = 1

	while business_page < 16:
		business_pageurl = business_url + str(business_page)
		businesses = get_businesses(business_pageurl)
		print(f"I am on page {business_page} of the results!!!")
		print(business_pageurl)
		# take a break
		random_sleep()

		for business in businesses:
			baseurl = "https://www.bbb.org/api/businessprofile/customerreviews?page=" 
			review_page = 1
			parturl = f"&pageSize=15&businessId={business['businessId']}&bbbId={business['bbbId']}&sort=reviewDate%20desc,%20id%20desc"

			try:
				response = requests.get(f"{baseurl}1{parturl}", headers=headers).json()
			except requests.exceptions.RequestException as e:
				print(e)
				exit()

			total_pages = response['totalPages']

			writerows([[business['country'], business['state'], business['city'], business['businessId'], business['bbbId'], total_pages, f"{business['url']}/customer-reviews", business['url']]], filename_meta)

			print(f"{business['businessId']}/{business['bbbId']}: {total_pages} pages in {business['city']} {business['state']}, {business['country']}")
			

			while review_page < total_pages + 1:
				print(f"Scraping page {review_page}")
				
				review_pageurl = baseurl + str(review_page) + parturl
				reviews = get_reviews(review_pageurl, business["city"], business["state"], business["country"], business["url"])

				# print(reviews)

				writerows(reviews, filename)

				# take a break
				random_sleep()

				review_page += 1

		business_page += 1