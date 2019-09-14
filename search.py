import subprocess
import os
import json
import pprint
import requests


def fetchData(search_words, results_no, language):
    """return file of dicts with the format {urlto raw:}"""
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

    for result in range(len(data["results"])):
        if result < results_no:
            vals = {}
            link = data["results"][result]["url"]
            link = link.replace("view", "raw")
            vals["url"] = link
            vals["code"] = data["results"][result]["lines"]
        returnData.append(vals)

    # print(data["matchterm"])

    return vals
