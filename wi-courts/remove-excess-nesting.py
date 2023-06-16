import requests
import json
from libjson2csv import json_2_csv
import ndjson

directory_name = "output"

file_name = "cases"

# load from file-like objects
with open(f"{directory_name}/{file_name}.ndjson") as f:
    data = ndjson.load(f)
    with open(f"{directory_name}/{file_name}_unnested.ndjson", "w") as file:
        for d in data:
            unnested = d["response"]["result"]
            json.dump(unnested, file)
            file.write("\n")
