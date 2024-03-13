from flask import Flask
import pymongo
from selenium import webdriver
from selenium.webdriver.common.by import By

def scrape():
  chrome_options = webdriver.ChromeOptions()
  chrome_options.add_argument("--headless=new")
  chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
  driver = webdriver.Chrome(options=chrome_options)
  driver.get("https://www.espn.com/mlb/team/_/name/bos/boston-red-sox")
  elems = driver.find_elements(By.CLASS_NAME, "Schedule__Game")

  elem = elems[0]

  if("LIVE!" in elem.get_attribute('innerHTML')):
    url = elem.get_attribute('href')
    driver.get(url)
    game_strip_team_away = driver.find_elements(By.CLASS_NAME, "Gamestrip__Team--away")[0]
    away_name = game_strip_team_away.find_elements(By.CLASS_NAME, "ScoreCell__TeamName--abbev")[0].get_attribute('innerHTML')
    away_score = game_strip_team_away.find_elements(By.CLASS_NAME, "Gamestrip__Score")[0].get_attribute('innerHTML')

    game_strip_team_home = driver.find_elements(By.CLASS_NAME, "Gamestrip__Team--home")[0]
    home_name = game_strip_team_home.find_elements(By.CLASS_NAME, "ScoreCell__TeamName--abbev")[0].get_attribute('innerHTML')
    home_score = game_strip_team_home.find_elements(By.CLASS_NAME, "Gamestrip__Score")[0].get_attribute('innerHTML')
    
    #line one is done
    line_one = away_name+" "+ away_score +" @ "+home_score+" "+home_name

    batter_wrapper = driver.find_elements(By.CLASS_NAME, "Athlete__PlayerWrapper")[1]
    player_type = batter_wrapper.find_element(By.CLASS_NAME, "Athlete__Header").get_attribute('innerHTML')

    if(player_type == "Batter"):
      player_name = batter_wrapper.find_element(By.CLASS_NAME, "Athlete__PlayerName").get_attribute('innerHTML').split(' ')[1]
      line_two = player_name
    else:
      line_two = "Between Innings"
    
    driver.close()

  else:
    at_vs = elem.find_element(By.CLASS_NAME,"Schedule_atVs").get_attribute('innerHTML')
    if(at_vs == "vs"):
      team_vs = elem.find_element(By.CLASS_NAME,"Schedule__Team").get_attribute('innerHTML')
      line_one = "BOS "+at_vs+" "+team_vs 
    else:
      team_at = elem.find_element(By.CLASS_NAME,"Schedule__Team").get_attribute('innerHTML')
      line_one = "BOS "+at_vs+" "+team_at

    date_time = elem.find_elements(By.CLASS_NAME, "Schedule__Time")

    line_two = date_time[0].get_attribute('innerHTML')+" @ "+date_time[1].get_attribute('innerHTML')

    print(line_two)

    driver.close()

  return {"team": "001", "line_one": line_one, "line_two": line_two}


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/team/<id>')
def team_id(id):
    json = scrape()

    myclient = pymongo.MongoClient("mongodb+srv://benjaminvachon:Cyberpatriot123@sports.a7dkt84.mongodb.net/?retryWrites=true&w=majority&appName=sports")
    
    mydb = myclient["sports"]
    mycol = mydb["sports"]

    myquery = { "team": "001" }
    mydoc = list(mycol.find(myquery))

    if(len(mydoc) > 0):
      newvalues = { "$set": { "line_one": json['line_one'], 'line_two': json['line_two']} }
      mycol.update_one(myquery, newvalues)
      mydoc_final = list(mycol.find(myquery))
      return mydoc_final
    else:
      return {"message": "No Team Exists"}