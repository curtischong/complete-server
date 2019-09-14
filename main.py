import json
from flask import Flask, request
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello_world():
  print(request.data.decode("utf-8") )
  data = json.loads(request.data.decode("utf-8"))
  return 'Hello, World!' + data['language']
