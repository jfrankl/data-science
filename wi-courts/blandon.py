import requests
import json
from libjson2csv import json_2_csv
import ndjson


# def get_coordinates(address):
#     geocoder_results = requests.post(
#         f"http://192.168.0.212:4000/v1/search?text={address}",
#     ).json()

#     print(address)

#     print(geocoder_results["features"])

#     print(len(geocoder_results["features"]))

#     if len(geocoder_results["features"]) > 0:

#         return {
#             "lng": geocoder_results["features"][0]["geometry"]["coordinates"][0],
#             "lat": geocoder_results["features"][0]["geometry"]["coordinates"][1],
#         }

#     else:

#         return {"lng": "N/A", "lat": "N/A"}


def flatten(data):

    # print(135, data)

    remove_main = [
        "parties",
        "showRssButton",
        "receivables",
        "isReopenedRemandedFromAppeal",
        "daCaseNo",
        "payplanLink",
        "maintenance",
        "execSummary",
        "branchId",
        "countyNo",
        "available",
        "isCriminal",
        "prosAgency",
        "defAttys",
        "allowPurchase",
        "balanceDue",
        "warrants",
        "tac",
        "records",
        "wcisClsCode",
    ]

    keep = [
        "defendant",
        "classType",
        "caseNo",
        "countyName",
        "filingDate",
        "caption",
        "civilJdgmts",
    ]

    obj = {}

    caseNo = data["parameters"]["caseNo"]
    countyNo = data["parameters"]["countyNo"]

    for key in keep:
        try:
            obj[key] = data["response"]["result"][key]
        except:
            print(f"Could not find {key} for {caseNo}")

    obj[
        "caseUrl"
    ] = f"https://wcca.wicourts.gov/caseDetail.html?caseNo={caseNo}&countyNo={countyNo}&mode=details"

    # remove_activities = [
    #     "key",
    #     "loc",
    #     "start",
    #     "type",
    # ]

    # for key in remove_activities:
    #     for item in result["activities"]:
    #         del item[key]

    # remove_chargeHist = [
    #     "chargeNo",
    #     "dispoDesc",
    #     "id",
    #     "isConverted",
    #     "replacedBy",
    #     "seqNo",
    #     "severity",
    #     "statuteCite",
    # ]

    # for key in remove_chargeHist:
    #     for item in result["chargeHist"]:
    #         del item[key]

    # result["chargeHist"] = list(
    #     map(
    #         lambda item: item["descr"],
    #         result["chargeHist"],
    #     )
    # )

    # remove_charges = [
    #     "id",
    #     "isSummaryCandidate",
    #     "chargeNo",
    #     "severity",
    #     "chargeModifiers",
    #     "pleaDescr",
    #     "judgments",
    #     "pleaDate",
    # ]

    # for key in remove_charges:
    #     for item in result["charges"]:
    #         try:
    #             del item[key]
    #         except:
    #             print("Could not delete")

    # remove_defendant = [
    #     "attys",
    #     "fingerprintId",
    #     "inclGal",
    #     "effDate",
    #     "alias",
    #     "status",
    #     "type",
    #     "justisNo",
    #     "sealed",
    # ]

    # for key in remove_defendant:
    #     try:
    #         del result["defendant"][key]
    #     except:
    #         print("Could not delete")

    # try:
    #     defendant_coordinates = get_coordinates(result["defendant"]["address"])
    #     result["defendant"]["generated_lng"] = defendant_coordinates["lng"]
    #     result["defendant"]["generated_lat"] = defendant_coordinates["lat"]
    # except:
    #     print("No", data["response"]["result"])

    # remove_citations = [
    #     "depType",
    #     "countyNo",
    #     "appearTime",
    #     "key",
    #     "offenseDate",
    #     "caseNo",
    #     "appearDate",
    #     "mandatory",
    # ]

    # for key in remove_citations:
    #     for item in result["citations"]:
    #         try:
    #             del item[key]
    #         except:
    #             print("Could not delete")

    # include_count = [
    #     "chargeHist",
    #     "charges",
    #     "citations",
    #     "crossReferenced",
    # ]

    # for key in include_count:
    #     result["_j-" + key + "_count"] = len(result[key])

    # # result[
    # #     "caseUrl"
    # # ] = f"https://wcca.wicourts.gov/caseDetail.html?caseNo={view['caseNo']['value']}&countyNo={view['countyNo']['value']}&mode=details"

    # # rename_columns = [
    # #     {
    # #         "old": "caption",
    # #         "new": "_a-caption",
    # #     },
    # #     {
    # #         "old": "countyName",
    # #         "new": "_b-countyName",
    # #     },
    # #     {
    # #         "old": "caseNo",
    # #         "new": "_c-caseNo",
    # #     },
    # #     {
    # #         "old": "caseUrl",
    # #         "new": "_d-caseUrl",
    # #     },
    # #     {
    # #         "old": "defendant",
    # #         "new": "_e-defendant",
    # #     },
    # #     {
    # #         "old": "classType",
    # #         "new": "_f-classType",
    # #     },
    # #     {
    # #         "old": "filingDate",
    # #         "new": "_g-filingDate",
    # #     },
    # #     {
    # #         "old": "prosAtty",
    # #         "new": "_h-prosAtty",
    # #     },
    # #     {
    # #         "old": "respCtofc",
    # #         "new": "_i-respCtofc",
    # #     },
    # # ]

    # for column in rename_columns:
    #     result[column["new"]] = result.pop(column["old"])

    return obj


directory_name = "final"

file_name = "cases-all"

# load from file-like objects
with open(f"{directory_name}/{file_name}.ndjson") as f:
    print(1)
    data = ndjson.load(f)
    print(2)
    result = list(map(flatten, data))
    print(3)
    with open(f"{directory_name}/{file_name}.json", "w") as file:
        print(4)
        json.dump(result, file)

        with open(f"{directory_name}/{file_name}.csv", "w") as file:
            print(5)
            file.write(json_2_csv.convert_to_csv(result).getvalue())
