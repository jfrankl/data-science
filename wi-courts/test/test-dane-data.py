import json
from libjson2csv import json_2_csv
import ndjson
import csv


def in_dane_county(case):
    if case["result"]["countyName"] == "Dane":
        return True
    else:
        return False


def get_case_nums(case):
    return case["result"]["caseNo"]


with open("final/cases-all.ndjson") as c:
    cases = ndjson.load(c)

    filtered = filter(in_dane_county, cases)

    case_nums = list(map(get_case_nums, filtered))

    with open("test/dane-county.csv", newline="") as file:
        reader = csv.reader(file, delimiter=",")
        for row in reader:
            date = row[0]
            caseNo = row[1]
            name = row[2]

            if caseNo in case_nums:
                print(f"YES {date} {caseNo} {name}")
            else:
                print(f"X --- NO {date} {caseNo} {name}")
