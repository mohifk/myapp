import requests 
import time
import sqlite3

def sql_connector():
    con = sqlite3.connect("weather.db")
    cur = con.cursor()
    return con,cur

def create_table(con,cur):
    cur.execute("CREATE TABLE IF NOT EXISTS weather (name TEXT,datetime TEXT,temp TEXT,humidity TEXT)")
    con.commit()

def insert_data(con,cur,data):
    cur.execute("INSERT INTO weather values (?,?,?,?)",tuple([v for k,v in data.items()]))
    con.commit()
def proccess_data(data):
    return {"city":data['name'],"datetime":time.ctime(int(data['dt'])),"temp":int(data['main']['temp']-272) ,"humidity":data["main"]['humidity']}

def get_weather_data(city='Tehran',appid='36d6361e253d7429ea92cce37adc86f8'):
    URL = "https://api.openweathermap.org/data/2.5/weather"
    PARAMS = {'q':city , 'appid' : appid}
    r = requests.get(url = URL, params = PARAMS)
    return proccess_data(r.json())

con,cur = sql_connector()
create_table(con,cur)

while True :
    data_weather = get_weather_data('Isfahan')
    insert_data(con,cur,data_weather)
    print(data_weather)
    time.sleep(5)
