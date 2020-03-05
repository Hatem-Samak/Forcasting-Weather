
from flask import Flask ,request ,redirect , url_for , render_template
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from datetime import date
from IPython.display import display, HTML

app=Flask(__name__ )

app.config.from_object("config") # call config file which we creat

# app.config.from_pyfile("config.py")# call config from instace folder which has senestive information like password of DB

#local host:5000/
tooday = date.today() # getting current date

@app.route("/")
def first_page():
    return render_template('first.html',var1=tooday) 

@app.route("/weather")
def weather():
    # today = date.ctime() # getting current date
    # page request for scrapping
    response = requests.get("https://weather.com/en-IN/weather/tenday/l/3a0beb62c2ba2c0f73f9eb0219cb2025ba662b27659871d73c15328ce6a681f5") 

    # parsing the scrapped page using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser') 

    # identifying the tag of the HTML page which has weather data
    data = []
    ten_day = soup.find_all('div', class_="twc-table-scroller")
    # print(ten_day) 
    table = soup.find('table', attrs={'class':'twc-table'})
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    # print(rows)

    for row in rows:
        cols = row.find_all('td')      
        cols = [element.text.strip() for element in cols]
        
        regex = re.compile(r'(\d.*)')
        day_date  = regex.split(cols[1].replace('\n',''))
        
        day = day_date[0]
        date = day_date[1] + ", " + str(tooday.year)
        high_temp = cols[3][0:2]+'°'
        low_temp = cols[3][-3:]
        desc = cols[2]
        precip = cols[4]
        wind = cols[5]
        humidity = cols[6]
        record = [day ,  date,  desc , high_temp , low_temp , precip , wind , humidity ]
        
        data.append(record) # Get rid of empty values

    WeatherData = pd.DataFrame(data)
    WeatherData.columns = ["DAY", "DATE", "DESCRIPTION",  "HIGH_TEMP","LOW_TEMP", "PRECIP", "WIND", "HUMIDITY"]
    # print(WeatherData)
    # templet=HTML(WeatherData.to_html())
    
    return render_template('weather.html', vars=tooday, tables=[WeatherData.to_html(classes='data')],title=["DAY", "DATE", "DESCRIPTION",  "HIGH_TEMP","LOW_TEMP", "PRECIP", "WIND", "HUMIDITY"])

# @app.route("/about")
# def about():
#     return "about hello python flask"

# @app.route("/user/<username>")
# def show_user(username):
#     return "username is : {}".format(username)

# @app.route("/path/<path:subpath>")
# def show_path(subpath):
#     return "post is : {}".format(subpath)

# @app.route("/algorthm", methods=["POST","GET","PUT"])
# def algorthm():
#     if request.method=="POST":
#         return "you r using POST method"
#     else:
#         return " You r susing GET method"

if __name__ == "__main__":
    # app.run()
   
    app.run(port=app.config["PORT"],debug=app.config["DEBUG"])