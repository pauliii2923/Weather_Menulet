import re
import requests
import numpy as np
import urllib
import rumps
from bs4 import BeautifulSoup
from rumps import MenuItem

key = lambda x, y: list(map(lambda i:getattr(i,x),y))
lmap = lambda func, *args: list(map(func, *np.transpose(args[0])))

class Weather_Menulet:
  def __init__(self):
    self.app = rumps.App("Weather Menulet",quit_button=None)
    self.set_menu()
    self.app.run()
  def set_menu(self):
    list(map(lambda i:self.app.menu.pop(i), list(self.app.menu.keys())))
    print("getting zip code...")
    zip_code = re.findall("(?s)(\d{5})</span>.*<span>.*Weather</span>", requests.get("https://www.google.com/search?q=weather").text)[0]
    hourly,tenday = requests.get("https://weather.com/weather/hourbyhour/l/%s"%(zip_code)).text, requests.get("https://weather.com/weather/tenday/l/%s"%(zip_code)).text
    hourly_time = list(map(lambda i:i.strip(),key("text",BeautifulSoup(hourly).findAll("div",attrs={"class":"hourly-time"}))))
    hourly_date = list(map(lambda i:i.strip(),key("text",BeautifulSoup(hourly).findAll("div",attrs={"class":"hourly-date"}))))
    hourly_desc = list(map(lambda i:i.strip(),key("text",BeautifulSoup(hourly).findAll("td",attrs={"class":"description"}))))
    hourly_temp = list(map(lambda i:i.strip(),key("text",BeautifulSoup(hourly).findAll("td",attrs={"class":"temp"}))))
    tenday_time = list(map(lambda i:i.strip(),key("text",BeautifulSoup(tenday).findAll("span",attrs={"class":"date-time"}))))
    tenday_date = list(map(lambda i:i.strip(),key("text",BeautifulSoup(tenday).findAll("span",attrs={"class":"day-detail"}))))
    tenday_desc = list(map(lambda i:i.strip(),key("text",BeautifulSoup(tenday).findAll("td",attrs={"class":"description"}))))
    tenday_temp = list(map(lambda i:i.strip(),key("text",BeautifulSoup(tenday).findAll("td",attrs={"class":"temp"}))))
    hourly_prints = lmap(lambda time,date,desc,temp:"{} on {}, {} - {}".format(time,date,desc,temp),list(zip(hourly_time,hourly_date,hourly_desc,hourly_temp)))
    tenday_prints = lmap(lambda time,date,desc,temp:"{} on {}, {} - {}".format(time,date,desc,temp),list(zip(tenday_time,tenday_date,tenday_desc,tenday_temp)))
    self.app.icon = urllib.request.urlretrieve("https://cdn3.iconfinder.com/data/icons/bebreezee-weather-symbols/690/icon-weather-sunrainheavy-512.png","icon.png")[0]
    self.app.menu = [MenuItem("Hourly"),*list(map(lambda i:MenuItem(i),hourly_prints)),MenuItem(""),MenuItem("Tenday"),*list(map(lambda i:MenuItem(i),tenday_prints))]
    self.app.run()


