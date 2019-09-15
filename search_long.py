import requests
import difflib


def comapare(dict1, str2):
    fin_res = {}
    store = []
    ans = []

    for k, v in dict1.items():
        res = difflib.SequenceMatcher(None, v, str2).ratio()
        fin_res.update({v : res})
        store.append(res)

    store.sort()
    store = store[::-1]
    store = store[:5]
    for i in store:
        for k, v in fin_res.items():
            if i == v:
                ans.append(k)

    ans = list(set(ans))
    ans.sort()
    ans = ans[::-1]
    ans = ans[:5]

    print(ans)
    return ans



def fetchData(search_words, results_no, language):
    """return file of dicts with the format {url_to_raw_file:data, lines as a dict with line no being keys}"""
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
            vals["code"] = lines
            for key, val in lines.items():
                lineNums.append(key)
            vals["maxLine"] = max(lineNums)
            vals["minLine"] = min(lineNums)
            vals["lineNums"] = lineNums

            # getting the raw code
            r = requests.get(vals["url"])
            vals["raw"] = r.text.split("\n")
            returnData.append(vals)

    return returnData


dict1 = {1: "Hello",
        2: "Bye",
        3: "Trello",
        4: "Haha",
        5: "Yello",
        6: "bello"}

str2 = "hello"

comapare(dict1, str2)