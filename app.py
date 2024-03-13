from flask import Flask
from flask import request


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/team/<id>')
def team_id(id):
    return id