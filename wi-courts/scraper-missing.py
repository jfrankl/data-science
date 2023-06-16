import requests
import json
import time
import random
import os
import shutil
import ndjson

from datetime import datetime
from datetime import timedelta


def random_sleep():
    print("\n")
    return time.sleep(random.uniform(0, 0.5) + 0)


# Clear output directory

# try:
#     shutil.rmtree("output")
# except:
#     print("No output directory")

# Using the API requires an active session id cookie; do a search on the website to get a new cookie and then paste that here
session_key = "JSessionId_9401"

# Using the API requires an active session id cookie; do a search on the website to get a new cookie and then paste that here
session_id = "7C7B9263AD34023914AB43D45903EF64"

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
            "https://wcca.wicourts.gov/jsonPost/caseDetail",
            cookies=cookies,
            headers=headers,
            json=case_parameters,
            timeout=timeout_amount,
        ).json()

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


all_cases = []

with open("output/missing.ndjson") as cases:
    cases_parsed = ndjson.load(cases)
    for case in cases_parsed:
        case_data = get_case(case["countyNo"], case["caseNo"])
        with open("output/found.ndjson", "a") as file:
            json.dump(case_data, file)
            file.write("\n")
