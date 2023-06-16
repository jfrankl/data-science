import json
from libjson2csv import json_2_csv
import ndjson


def process_row(data):
    result = data["response"]["result"]
    view = data["response"]["view"]

    # Remove these columns, which were determined to be less useful.
    remove_columns = [
        "showRssButton",
        "receivables",
        "isReopenedRemandedFromAppeal",
        "daCaseNo",
        "maintenance",
        "execSummary",
        "branchId",
        "countyNo",
        "available",
        "isCriminal",
        "allowPurchase",
        "balanceDue",
        "warrants",
        "tac",
        "wcisClsCode",
    ]

    for key in remove_columns:
        result.pop(key)

    # Adds a link to the court website for this case, for easy look ups.
    result[
        "caseUrl"
    ] = f"https://wcca.wicourts.gov/caseDetail.html?caseNo={view['caseNo']['value']}&countyNo={view['countyNo']['value']}&mode=details"

    # I am adding a prefix to these columns to control the order in which they'll show up in the file
    # For example, _a-caption will be the first column and _b-countyName will be the second column. There
    # is probably a smarter way to do this.
    rename_columns = [
        {
            "old": "caption",
            "new": "_a-caption",
        },
        {
            "old": "countyName",
            "new": "_b-countyName",
        },
        {
            "old": "caseNo",
            "new": "_c-caseNo",
        },
        {
            "old": "caseUrl",
            "new": "_d-caseUrl",
        },
        {
            "old": "defendant",
            "new": "_e-defendant",
        },
        {
            "old": "classType",
            "new": "_f-classType",
        },
        {
            "old": "filingDate",
            "new": "_g-filingDate",
        },
        {
            "old": "prosAtty",
            "new": "_h-prosAtty",
        },
        {
            "old": "respCtofc",
            "new": "_i-respCtofc",
        },
    ]

    for column in rename_columns:
        result[column["new"]] = result.pop(column["old"])

    return result


# load from file-like objects
with open(f"output/cases.ndjson") as f:
    data = ndjson.load(f)
    result = list(map(process_row, data))
    with open(f"output/cases.json", "w") as file:
        json.dump(result, file)
        with open(f"output/cases.csv", "w") as file:
            file.write(json_2_csv.convert_to_csv(result).getvalue())
