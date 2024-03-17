from flask import Flask, json
from bson import json_util
import pymongo
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

names = {
  "Yankees":"NYY"
}

def scrape():
  r = requests.get('https://www.espn.com/mlb/team/_/name/bos/boston-red-sox',headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
  soup = BeautifulSoup(r.text, 'lxml')

  game_tab = soup.select_one('a[class^="Schedule__Game"]')

  team_one = game_tab.select_one('span[class^="Schedule__Team"]').text

  vs_at = game_tab.select_one('span[class^="Schedule_atVs"]').text

  is_live = game_tab.select_one('span[class^="Schedule__Time"]').text
  if "LIVE!" in is_live:
    link = game_tab.get('href')
    r_one = requests.get(link,headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    soup_one = BeautifulSoup(r_one.text, 'lxml')

    divs = soup_one.select('div[class^="Gamestrip__Team"]')
    team_one_data = divs[0].text.split("away")[1]
    team_two_data = divs[3].text.split("home")[1]

    if("vs" in vs_at):
      line_one = team_two_data+" BOS "+vs_at+" "+names[team_one]+" "+team_one_data
    else:
      line_one = team_one_data+" BOS "+vs_at+" "+names[team_one]+" "+team_two_data

    hitter = soup_one.select('span[class^="Athlete__Header"]')[1].text
    if("Batter" not in hitter):
      line_two = "between innnings"
    else:
      line_two = soup_one.select('span[class^="Athlete__PlayerName"]')[1].text
    return {'team': '001','line_one': line_one,'line_two': line_two}
  else:
    line_one = "BOS "+vs_at+" "+team_one
    line_two = is_live
    return {'team': '001','line_one': line_one,'line_two': line_two}

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/team/<id>')
def team_id(id):
  myclient = pymongo.MongoClient("mongodb+srv://benjaminvachon:Cyberpatriot123@sports.a7dkt84.mongodb.net/?retryWrites=true&w=majority&appName=sports")
  
  mydb = myclient["sports"]
  mycol = mydb["sports"]

  myquery = { "team": "001" }

  return json.loads(json_util.dumps(mycol.find(myquery)[0]))

@app.route('/update/team/<id>')
def update_team(id):

  temp_json = scrape()

  myclient = pymongo.MongoClient("mongodb+srv://benjaminvachon:Cyberpatriot123@sports.a7dkt84.mongodb.net/?retryWrites=true&w=majority&appName=sports")
  
  mydb = myclient["sports"]
  mycol = mydb["sports"]

  myquery = { "team": id }
  newvalues = { "$set": { "line_one": temp_json["line_one"], "line_two": temp_json["line_two"] } }
  mycol.update_one(myquery, newvalues)

  return "updated"