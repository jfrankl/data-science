import requests
import json
import time
import random
import os
import shutil
from datetime import datetime
from datetime import timedelta


def random_sleep():
    print("\n")
    return time.sleep(random.uniform(0, 0.5) + 0)


# Using the API requires an active session id cookie; do a search on the website to get a new cookie and then paste that here
session_key = "JSessionId_9401"

# Using the API requires an active session id cookie; do a search on the website to get a new cookie and then paste that here
session_id = "77CA6215C5E9EE107F8F0B8E73C53299"


case_types = "CF,TR,CT,CM"

# Starting date
search_start = "2022-01-01"

# How many days to search
search_days = 2

# Store information about a case that needs to be repeated due to CAPTCHA
case_to_repeat = None

timeout_amount = 1800

cookies = {
    session_key: session_id,
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


def get_cases(start, end):
    random_sleep()

    search_parameters = {
        "includeMissingDob": True,
        "includeMissingMiddleName": True,
        "attyType": "partyAtty",
        "filingDate": {
            "start": start,
            "end": end,
        },
        "caseType": case_types,
    }

    try:
        search_response = requests.post(
            "https://wcca.wicourts.gov/jsonPost/advancedCaseSearch",
            cookies=cookies,
            headers=headers,
            json=search_parameters,
            timeout=timeout_amount,
        ).json()

        filename = "output/cases-list.ndjson"
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, "a") as file:
            print(123, filename)
            cases = search_response["result"]["cases"]
            for case in cases:
                json.dump(
                    {
                        "caseNo": case["caseNo"],
                        "countyNo": case["countyNo"],
                        "filingDate": start,
                    },
                    file,
                )
                file.write("\n")

    except:
        filename = "output/cases-list-errors.ndjson"
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, "a") as file:
            json.dump(
                {
                    "type": "get_cases fail",
                    "start": start,
                    "parameters": search_parameters,
                },
                file,
            )
            file.write("\n")


start_date = datetime.fromisoformat(search_start).date()

for day in range(search_days):
    delta = 1 * day
    start = start_date - timedelta(delta)
    end = start_date - timedelta(delta)

    get_cases(str(start), str(end))
