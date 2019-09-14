import subprocess
import os
import json
import pprint
import requests

def get_search_words(code):
  return ["hello"]

def fetchData(search_words, results_no, language):
    """return file of dicts with the format {url_to_raw_file:data, lines as a dict with line no being keys}"""

    returnData = []
    lang_no = {"python": "19"}

    cmd = "https://searchcode.com/api/codesearch_I/?q="
    for search_word in search_words:
        cmd += search_word + "+"
    cmd = cmd[:-1]
    cmd += "&p=1&per_page=100&lan="+lang_no[language]
    print(cmd)

    r = requests.get(cmd)
    print(r.status_code)
    data = r.json()
    print(data)

    for result in range(len(data["results"])):
        if result < results_no:
            vals = {}
            
            link = data["results"][result]["url"]
            link = link.replace("view", "raw")
            vals["url"] = link
            
            # getting the line nums
            lines = data["results"][result]["lines"]
            lineNums = []
            for key, val in lines.items():
                lineNums.append(key)
            vals["maxLine"] = max(lineNums)
            vals["minLine"] = min(lineNums)
            
            # getting the raw code
            r = requests.get("https://searchcode.com/codesearch/raw/47298605/")
            vals["raw"] = r.text.split("\n")
            returnData.append(vals)

    return returnData
