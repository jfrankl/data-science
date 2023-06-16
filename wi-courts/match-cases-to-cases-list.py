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


with open("output/cases-list.ndjson") as a:
    with open("output/cases.ndjson") as b:
        cases_definitive = ndjson.load(a)
        cases_scraped = ndjson.load(b)
        for case_definitive in cases_definitive:
            found = False
            for case_scraped in cases_scraped:
                if (
                    case_definitive["countyNo"]
                    == case_scraped["parameters"]["countyNo"]
                    and case_definitive["caseNo"]
                    == case_scraped["parameters"]["caseNo"]
                ):
                    found = True
                    break
            if found == True:
                print("Found:", case_scraped)
                save_case("output/cases-list-found.ndjson", case_scraped)
            else:
                print("Not found:", case_definitive)
                save_case("output/cases-list-not-found.ndjson", case_definitive)
