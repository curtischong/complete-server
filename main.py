import json
from search import fetchData, get_search_words
from flask import Flask, request
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello_world():
  print(request.data.decode("utf-8") )
  data = json.loads(request.data.decode("utf-8"))
  print(data)
  search_words = get_search_words(data['code'])
  results = fetchData(search_words, data['results_num'], data['language'])
  return json.dumps(results)
