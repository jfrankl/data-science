# import requests
import json
from libjson2csv import json_2_csv
import ndjson
import json
import os


def save_case(filename, case):
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "a") as file:
        json.dump(
            case,
            file,
        )
        file.write("\n")


uniqueList = []


def add_if_unique(charge_description):
    print(charge_description)
    if charge_description not in uniqueList:
        uniqueList.append(charge_description)


with open("output/cases.ndjson") as c:
    cases = ndjson.load(c)
    for case_response in cases:
        case = case_response["response"]["result"]
        for charge in case["charges"]:
            add_if_unique(charge["descr"])


save_case("output/unique-charge-descriptions.json", uniqueList)
