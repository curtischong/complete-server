import subprocess
import os
import json
import pprint
import requests
import keyword
import re
import math

importantPackages = [ "tensorflow", "scikit-learn", "numpy", "keras", "pytorch", "lightgbm", "eli5", "scipy", "theano", "pandas", "flask", "django", "beautifulsoup", "requests", "scrapy", "matplotlib", "os", "subprocess", "json", "flask_cors", "request", "app"]

comment = [r'#.*', r'[;|}|{|\w]\s?#.*', r"'''([^*]|[\r\n]|(\*+([^*/]|[\r\n])))'''", r"'''[.*|\s?\r\n]", r".*\s?'''$", r"\"\"\"[.*|\s?\r\n]", r".*\s?\"\"\"$"]

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
        "<",
        "..",
        "<="
    ]

queryParameters = []

modulesUsed = []

def checkComment(line):
    #check for comments
    lonelyComment = comment[0]
    if re.search(lonelyComment, line):
        return True
    return False


def get_search_words(code, fullCode):
    #for the fullCode
    fullCode = fullCode.split('\n')
    tempFullCodeWithoutComments = []
    startFound = False
    commentFound = False
    for line in fullCode:
        if not re.match(r'^\s*$', line):
            if checkComment(line): #start of a single line comment
                commentFound = True
            else: #no comment
                commentFound = False
            if re.search(comment[3], line) or startFound or re.search(comment[5], line): #start of a multiline comment
                startFound = True
            if (not commentFound) and (not startFound):
                tempFullCodeWithoutComments.append(line)
            if re.search(comment[4], line) or re.search(comment[6], line) : #end of a multiline comment
                startFound = False
    fullCodeWithoutComments = []
    for line in tempFullCodeWithoutComments:
        fullCodeWithoutComments.extend(line.split())
    # print(fullCodeWithoutComments)
    fullWords = removeKeywords(fullCodeWithoutComments, False)
    fullCodeFreq = {} 
    for item in fullWords: 
        if (item in fullCodeFreq): 
            fullCodeFreq[item] += 1
        else: 
            fullCodeFreq[item] = 1
    idf = {}
    for key in fullCodeFreq:
        idf[key] = math.log(len(fullWords)/fullCodeFreq[key])
    #for code snippet
    code = code.split('\n')
    tempCodeWithoutComments = []
    startFound = False
    commentFound = False
    for line in code:
        if not re.match(r'^\s*$', line):
            if checkComment(line): #start of a single line comment
                commentFound = True
            else: #no comment
                commentFound = False
            if re.search(comment[3], line) or startFound: #start of a multiline comment
                startFound = True
            if (not commentFound) and (not startFound):
                tempCodeWithoutComments.append(line)
            if re.search(comment[4], line): #end of a multiline comment
                startFound = False
    codeWithoutComments = []
    for line in tempCodeWithoutComments:
        codeWithoutComments.extend(line.split())
    # codeWithoutComments = codeWithoutComments.split()
    words = removeKeywords(codeWithoutComments, True)
    #check if modules used
    for module in modulesUsed:
        for word in words:
            if module in word:
                #do regex parsing
                reg = r'\.(?:.(?!\.))+$'
                search = re.search(reg, word)
                if search:
                    reg_search = re.search(r'\.(.*)[\(\[](.*)', search.group(0))
                    if reg_search and module != reg_search.group(1):
                        function = module + '.' + reg_search.group(1)
                        print(function, module, reg_search.group(1))
                        if function not in queryParameters:
                            queryParameters.append(function)
                if module not in queryParameters:
                    queryParameters.append(module)
    codeFreq = {} 
    for item in words: 
        if (item in codeFreq): 
            codeFreq[item] += 1
        else: 
            codeFreq[item] = 1
    tf = {}
    for key in codeFreq:
        tf[key] = codeFreq[key]/len(words)
    tf_idf = {}
    #do the tf-idf math
    for key in tf:
        if key in idf:
            tf_idf[key] = tf[key] * idf[key]
    tf_idf = sorted(tf_idf, key=tf_idf.get)
    index = 0
    while len(queryParameters) < 3:
        if index < len(tf_idf) and tf_idf[index].lower() not in queryParameters:
            queryParameters.append(tf_idf[index])
        if index >= len(tf_idf):
            break
        index += 1
    print(queryParameters)
    return queryParameters

def removeKeywords(words, isCodeSnippet):
    keyWords = [
        "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "not", "print",
        "console", "log", "and", "in", "if", "else", "continue", "break", "while",
        "try", "except", "elif", "def", "for", "print", "return",
        "assert", "raise", "i", "or", "as", "pass", "import", "from",
        "False", "True", "class", "global", "with", "#!/usr/bin/env"
    ]
    newWords = []
    for word in words:
        if word.lower() not in keyWords and word not in chars_list:
            newWords.append(word)
    if isCodeSnippet:
        for word in words:
            if word.lower() in importantPackages:
                queryParameters.append(word.lower())  #only update when code snippet
    else:
        for word in words:
            if word.lower() in importantPackages:
                modulesUsed.append(word)

    return newWords
    

def fetchData(search_words, results_no, language):
    """return file of dicts with the format {url_to_raw_file:data, lines as a dict with line no being keys}"""
    print("search_words")
    print(search_words)

    returnData = []
    lang_no = {"python": "19"}

    cmd = "https://searchcode.com/api/codesearch_I/?q="
    for search_word in search_words:
        cmd += search_word + "+"
    queryParameters.clear()
    cmd = cmd[:-1]
    cmd += "&p=1&per_page=100&lan="+lang_no[language]
    print(cmd)

    r = requests.get(cmd)
    print(r.status_code)
    data = r.json()
    print(data)
    if data is None:
        print("No match found :( ")
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

# tfCode = '''
# import os
# sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/cardUpdates")
# #print(sys.path)

# import CardUpdates as CardUpdates
# import Eat as Eat
# import Phrase as Phrase
# import Morning as Morning
# import Break as Break
# import Eval as Eval
# import LizzieData as LizzieData
# import CongratsWordUse as CongratsWordUse

# import json

# from flask import Flask, request
# from flask_cors import CORS
# import databaseManager
# app = Flask(__name__)
# CORS(app)


# cards = []

# def updateCards():
#   # Cards
#   if(CardUpdates.updateEatCard()):
#     cards.append(Eat.sendEatCard())
#   if(CardUpdates.updatePhrase()):
#     cards.append(Phrase.sendPhraseCard())
#   if(CardUpdates.updateBreak()):
#     cards.append(Break.sendBreakCard())
#   if(CardUpdates.updateLizzieDataCard()):
#     cards.append(LizzieData.sendLizzieDataCard())
#   #if(CardUpdates.updateCongratsWordUseCard()):
#   #  cards.append(CongratsWordUse.sendCongratsWordUseCard())

#   # Panels
#   if(CardUpdates.updateMorning()):
#     cards.append(Morning.sendMorningPanel())
#   if(CardUpdates.updateEval()):
#     cards.append(Eval.sendEvalPanel())
#   if(CardUpdates.updateEval()):
#     cards.append(Eval.sendAllEvalPanel())

# # TODO: remove
# @app.route('/get_card', methods=['GET'])
# def get_card():
#     while(len(cards) > 0):
#       cards.pop()
#     updateCards()
#     return json.dumps(cards)


# @app.route('/dismiss_panel', methods=['POST'])
# def dismiss_panel():
#   timePlaced = request.json['timePlaced'] if request.json['timePlaced'] else None
#   if(timePlaced == None):
#     return "timePlaced field not found!"
#   databaseManager.dismissPanel(timePlaced)
#   return "dismissed panel!"
# '''

# tCode = '''
#     @app.route('/dismiss_panel', methods=['POST'])
# def dismiss_panel():
#   timePlaced = request.json['timePlaced'] if request.json['timePlaced'] else None
#   if(timePlaced == None):
#     return "timePlaced field not found!"
# '''

# output_words = get_search_words(tCode, tfCode)
# fetchData(output_words, 4, "python")
# get_search_words(tCode, tfCode)