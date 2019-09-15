import requests
import difflib


# res = difflib.SequenceMatcher(None, v["url"], str2).ratio()


def sort_function(valsn):
    return valsn["ratio"]


def fetchData(search_words, results_no, language, search_string):
    """search string is the raw string, the thing the user highlights. This is needed for comparison purposes. 
    results_no  should be 100 for this
    note that dome extra data has been added to the dictionaries that are returned like the ratios, but that shouldnt affect anything.
    """
    selected = []
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
    # print(data)

    for result in range(len(data["results"])):
        if result < results_no:
            vals = {}

            link = data["results"][result]["url"]
            link = link.replace("view", "raw")

            str_text = ""
            for i in data["results"][result]["lines"].values():
                str_text += i
            vals["url"] = str_text

            # getting the line nums

            lines = data["results"][result]["lines"]
            lineNums = []
            vals["code"] = lines
            for key, val in lines.items():
                lineNums.append(key)
            vals["maxLine"] = max(lineNums)
            vals["minLine"] = min(lineNums)
            vals["lineNums"] = lineNums

            vals["ratio"] = difflib.SequenceMatcher(
                None, vals["url"], search_string).ratio()

            # getting the raw code
            # r = requests.get(vals["url"])
            # vals["raw"] = r.text.split("\n")
            returnData.append(vals)

    returnData.sort(key=sort_function)

    for i in returnData:
        print(i["ratio"])
        # print(i["url"])

    return returnData

fetchData(["print", "r.status_code", "r.json()"], 100, "python",
          "print(r.status_code) data = r.json()")