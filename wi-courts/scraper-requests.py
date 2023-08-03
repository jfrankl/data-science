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


def notify(title, text):
    os.system(
        """
              osascript -e 'display notification "{}" with title "{}"'
              """.format(
            text, title
        )
    )


# Clear output directory

# try:
#     shutil.rmtree("output")
# except:
#     print("No output directory")

# Using the API requires an active session id cookie; do a search on the website to get a new cookie and then paste that here
session_key = "JSessionId_9401"

# Using the API requires an active session id cookie; do a search on the website to get a new cookie and then paste that here
session_id = "7AD0EFCC495AD33EF6A50E5EBBE31C3F"

case_types = "CF,TR,CT,CM"

# Starting date
search_start = "2017-12-31"

# How many days to search
search_days = 365

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


def get_case(county_no, case_no):
    random_sleep()

    case_parameters = {
        "countyNo": county_no,
        "caseNo": case_no,
    }

    print(f"get_case {case_parameters}")

    try:
        case_response = requests.post(
            f"https://wcca.wicourts.gov/caseDetail/{county_no}/{case_no}",
            cookies=cookies,
            headers=headers,
            json=case_parameters,
            timeout=timeout_amount,
        ).json()

        print("this-worked")
        print(case_response)

        # print(case_response)

        if "errors" in case_response.keys():
            print("did this work?")
            # notify("Cookie needed", "Please generate a new cookie and press Enter.")

            new_cookie = input("Refresh captcha and press enter...")

            if new_cookie:
                cookies[session_key] = new_cookie

            get_case(county_no, case_no)
        else:
            timestamp = datetime.now()
            os.makedirs(os.path.dirname("output/history.ndjson"), exist_ok=True)
            with open("output/history.ndjson", "a") as file:
                json.dump(
                    {
                        "type": "success",
                        "parameters": case_parameters,
                    },
                    file,
                )
                file.write("\n")
            return {
                "parameters": case_parameters,
                "timestamp": str(timestamp),
                "response": case_response,
            }

    except:
        print("failllll")
        os.makedirs(os.path.dirname("output/history.ndjson"), exist_ok=True)
        with open("output/history.ndjson", "a") as file:
            json.dump(
                {
                    "type": "failure",
                    "parameters": case_parameters,
                },
                file,
            )
            file.write("\n")


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

    # search_response = test_search_response

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

        cases = search_response["result"]["cases"]

        with open(filename, "a") as file:
            for case in cases:
                json.dump(
                    {
                        "countyNo": case["countyNo"],
                        "caseNo": case["caseNo"],
                    },
                    file,
                )
                file.write("\n")

        return cases

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

    print(str(start), str(end))

    search_cases = get_cases(str(start), str(end))

    cases_in_day = []

    for search_case in search_cases:
        case = get_case(search_case["countyNo"], search_case["caseNo"])
        # print("Case:", case)
        cases_in_day.append(case)

    filename = "output/cases-2017.ndjson"
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    for c in cases_in_day:
        with open(filename, "a") as file:
            json.dump(c, file)
            file.write("\n")
