import json
from search import fetchData, get_search_words
from flask import Flask, request
from scrape import scrape, initialize_browser
from selenium import webdriver
app = Flask(__name__)

initialize_browser()

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    print(request.data.decode("utf-8") )
    data = json.loads(request.data.decode("utf-8")) 
    print(data['code'])
    search_words = get_search_words(data['code'], data['fullCode'])
    results = fetchData(search_words, data['results_num'], data['language'])
    return json.dumps(results)


@app.route('/getCodeFromDocStrings', methods=['GET', 'POST'])
def getCodeFromDocStrings():
    global first_time_scrape
    print(request.data.decode("utf-8") )
    data = json.loads(request.data.decode("utf-8"))
    results = scrape(data['docString'])
    return json.dumps(results)