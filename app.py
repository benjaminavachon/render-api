from flask import Flask
import pymongo
from selenium import webdriver
from selenium.webdriver.common.by import By

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/team/<id>')
def team_id(id):
    myclient = pymongo.MongoClient("mongodb+srv://benjaminvachon:Cyberpatriot123@sports.a7dkt84.mongodb.net/?retryWrites=true&w=majority&appName=sports")
    
    mydb = myclient["sports"]
    mycol = mydb["sports"]

    myquery = { "team": "001" }
    mydoc = list(mycol.find(myquery))

    if(len(mydoc) > 0):
      mydoc_final = list(mycol.find(myquery))
      return mydoc_final
    else:
      return {"message": "No Team Exists"}