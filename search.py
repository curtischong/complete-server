import subprocess
import os
import json
import pprint
import requests
import keyword


def get_search_words(code):
    """Given a string, returns the searchable keywords as a list of strings"""

    """Our tool will not teach a kid how to program,
    it will help power users be more efficient.
    We can have a broad but innacurrate search or
    a deep and narrow search. Deep and narrow is much better
    Atleast, its about finding a balance. By removing these common words, I can cut through a lot of
    false positives."""

    words_list = [
        "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "not", "print",
        "console", "log", "and", "in", "if", "else", "continue", "break", "while",
        "try", "except", "elif", "def", "for", "print", "return",
        "assert", "raise", "i", "or", "as", "pass", "import", "from",
        "False", "True", "class", "global", "with", "#!/usr/bin/env"
    ]
    words_list = list(set(words_list.append(keyword.kwlist)))

    chars_list = [
        ":",
        ")",
        "(",
        "]",
        "[",
        "{",
        "}",
        "=",
        "+",
        "-",
        "/",
        "%",
        "*",
        ">",
        "<"
    ]

    code = code.split()
    keywords = []
    for word in code:
        if word not in words_list and len(word) > 1:
            for char in word:
                if char in chars_list:
                    word = word.replace(char, "")
            keywords.append(word)
    print("searchwords:")
    print(keywords)
    return keywords


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
    if data is None:
        return []

    for result in range(len(data["results"])):
        if result < results_no:
            vals = {}
            
            link = data["results"][result]["url"]
            link = link.replace("view", "raw")
            vals["url"] = link
            
            # getting the line nums
            lines = data["results"][result]["lines"]
            lineNums = []
            codeLines = []
            for key, val in lines.items():
                lineNums.append(key)
                codeLines.append(val)
            vals["maxLine"] = max(lineNums)
            vals["minLine"] = min(lineNums)
            
            # getting the raw code
            #r = requests.get(vals["url"])
            vals["lineNums"] = lineNums
            vals["codeLines"] = codeLines
            #vals["raw"] = r.text.split("\n")
            returnData.append(vals)

    return returnData
