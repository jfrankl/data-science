# import requests
import json
from libjson2csv import json_2_csv

# import time
# import random
# import os
# import shutil
# import datetime

import ndjson

# load from file-like objects
with open("final/cases-all.ndjson") as c:
    cases = ndjson.load(c)

    with open("output/search.ndjson") as s:
        search = ndjson.load(s)

        result["chargeHist"] = list(
            map(
                lambda item: item["descr"],
                result["chargeHist"],
            )
        )

    # with open(f"{directory_name}/{file_name}.json", "w") as file:
    #     json.dump(result, file)

    #     with open(f"{directory_name}/{file_name}.csv", "w") as file:
    #         file.write(json_2_csv.convert_to_csv(result).getvalue())
