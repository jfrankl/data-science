# import requests
import json
from libjson2csv import json_2_csv
import ndjson
import json
import os


def find_missing(l):
    if len(l) > 0:
        sorted_list = sorted(l)
        return sorted(set(range(sorted_list[0], sorted_list[-1])) - set(sorted_list))


years = [2020, 2021, 2022, 2023]
counties = list(range(1, 72 + 1))
categories = ["CF", "TR", "CT", "CM"]

everything = {}
missing = []

for year in years:
    everything[year] = {}
    for county in counties:
        everything[year][county] = {}
        for category in categories:
            everything[year][county][category] = []

with open("output/cases.ndjson") as c:
    cases = ndjson.load(c)
    for case in cases:
        county_no = int(case["parameters"]["countyNo"])
        case_no = case["parameters"]["caseNo"]
        year = int(case_no[0:4])
        category = case_no[4:6]
        number = int(case_no[6:12])

        everything[year][county_no][category].append(number)

os.makedirs(os.path.dirname("output/missing.ndjson"), exist_ok=True)

for year in everything:
    for county in everything[year]:
        for category in everything[year][county]:
            missing_nums = find_missing(everything[year][county][category])
            if missing_nums:
                for num in missing_nums:
                    if year == 2022:
                        with open("output/missing.ndjson", "a") as file:
                            parameters = {
                                "countyNo": county,
                                "caseNo": f"{year}{category}{str(num).zfill(6)}",
                            }
                            json.dump(
                                parameters,
                                file,
                            )
                            file.write("\n")
                            print(parameters)
