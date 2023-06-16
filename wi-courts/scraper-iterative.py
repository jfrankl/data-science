import requests
import json
import time
import random
import os
import shutil
import datetime
from daves_utilities.for_long import for_long


def random_sleep():
    # return time.sleep(1)
    return time.sleep(random.uniform(0, 0.25) + 10.25)


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
session_id = "71C1E9EBDD62B283FF0E135B5202130D"

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


scrape_config = {
    "years": list(reversed(range(2018, 2022 + 1))),  # years 2018–2022
    "counties": list(range(1, 72 + 1)),  # Counties 1–72
    "types": ["CT", "TR"],
}


# Need to reset counts somehow

for year in scrape_config["years"]:
    for county in scrape_config["counties"]:
        for case_type in scrape_config["types"]:
            for case_iterator in range(1, 5 + 1):
                filename = f"output/{year}/{county}/{case_type}.ndjson"
                timestamp = datetime.datetime.now()
                number = f"{year}{case_type}{str(case_iterator).zfill(6)}"
                case_parameters = {"countyNo": county, "caseNo": number}

                os.makedirs(os.path.dirname(filename), exist_ok=True)

                with open(filename, "a+") as file:
                    file.seek(0)  # Back to the beginning of the file
                    length_of_file = len(file.readlines())
                    if length_of_file >= case_iterator:
                        print(f"Old: /{year}/{county}/{case_type}/{case_iterator}")
                    else:
                        print(f"New: /{year}/{county}/{case_type}/{case_iterator}")

                        case_response = requests.post(
                            "https://wcca.wicourts.gov/jsonPost/caseDetail",
                            cookies=cookies,
                            headers=headers,
                            json=case_parameters,
                            timeout=300,
                        ).json()

                        print(12345, case_response["result"]["available"])

                        if length_of_file > 0:
                            file.write("\n")

                        json.dump(
                            {
                                "id": case_iterator,
                                "timestamp": str(timestamp),
                                "parameters": case_parameters,
                                "response": case_response,
                            },
                            file,
                        )

                        random_sleep()
