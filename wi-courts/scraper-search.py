import requests
import json
import time
import random
import os
import shutil
from datetime import datetime
from datetime import timedelta


def random_sleep():
    # return time.sleep(1)
    return time.sleep(random.uniform(0, 0.1) + 0.1)


# Using the API requires an active session id cookie; do a search on the website to get a new cookie and then paste that here
session_id = "9DB7EABFE028BF62ED201221186FC6AA"

# Database class code; Operate without License is "28600"
class_code = "28600"

# Starting date
search_start = "2022-10-26"

# How many months to search
search_months = 60

# Store information about a case that needs to be repeated due to CAPTCHA
case_to_repeat = None

cookies = {
    "JSessionId_9401": session_id,
}

headers = {
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Origin": "https://wcca.wicourts.gov",
    "Pragma": "no-cache",
    "Referer": "https://wcca.wicourts.gov/advanced.html",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Sec-GPC": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
}

test_search_response = {
    "result": {
        "cases": [
            {
                "partyName": "Michaud, Alicia Marie",
                "countyName": "Brown",
                "dob": "1979-08",
                "caseNo": "2022TR008267",
                "countyNo": 5,
                "caption": "State vs. Alicia Marie Michaud",
                "status": "Filed Only",
                "filingDate": "2022-10-18",
            },
            {
                "partyName": "Michaud, Alicia Marie",
                "countyName": "Brown",
                "dob": "1979-08",
                "caseNo": "2022TR008266",
                "countyNo": 5,
                "caption": "State vs. Alicia Marie Michaud",
                "status": "Filed Only",
                "filingDate": "2022-10-18",
            },
        ]
    }
}


def getCases(start, end):
    random_sleep()

    search_parameters = {
        "includeMissingDob": True,
        "includeMissingMiddleName": True,
        "attyType": "partyAtty",
        "filingDate": {
            "start": start,
            "end": end,
        },
        "classCode": class_code,
    }

    # search_response = test_search_response

    search_response = requests.post(
        "https://wcca.wicourts.gov/jsonPost/advancedCaseSearch",
        cookies=cookies,
        headers=headers,
        json=search_parameters,
    ).json()

    filename = "output/search.ndjson"
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "a") as file:
        json.dump(
            {
                "search_parameters": search_parameters,
                "cases": search_response["result"]["cases"],
            },
            file,
        )
        file.write("\n")

    print(f"getCases from {start} to {end}")

    return search_response["result"]["cases"]


start_date = datetime.fromisoformat(search_start).date()


for month in range(search_months):
    delta = 31 * month
    start = start_date - timedelta(delta + 30)
    end = start_date - timedelta(delta)

    cases = getCases(str(start), str(end))
