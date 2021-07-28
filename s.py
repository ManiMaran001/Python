from bs4 import BeautifulSoup as bs
import requests
import json
import pickle
def clean_tags(soup):
   for tag in soup.find_all(["sup","span"]):
      tag.decompose()
      #print(tag)
         
def get_list(row_data):
   if row_data.find("li"):
      return [li.get_text(" ",strip=True).replace('\xa0'," ") for li in row_data.find_all("li")]
   #this elif is to solve the un listed key pair values makes a list with stripped strings
   elif row_data.find("br"):
      return [tag for tag in row_data.stripped_strings]
   else:
      return row_data.get_text(" ",strip=True).replace('\xa0'," ")


def get_url(url1):

   html_text=requests.get(url1)
   soup=bs(html_text.content)
   table=soup.find("table",class_="infobox vevent")
   tr=table.select("tr")
   clean_tags(soup)
   movie_info={}
   for index,value in enumerate(tr):
      if index==0:
         movie_info['title']=value.find("th").get_text()
      else:
         header=value.find("th")
         if header:
            content_key=value.find("th").get_text(" ",strip=True)
            content_value=get_list(value.find("td"))
            movie_info[content_key]=content_value
   return movie_info


def save_json(title,data):
   with open(title,"w",encoding='utf-8') as fil:
      json.dump(data,fil,indent=2)

def load_data_json(title):
   with open(title,"r") as fil:
      return json.load(fil)


def clean_minutes(running_time):
   if running_time=='N/A':
      return None
   
   if isinstance(running_time,list):
      return int(running_time[0].split()[0])
   else:
      return (int(running_time.split()[0]))


def word_dict(word):
   value={"thousand":1000,"million":1000000,"billion":1000000000}
   return value[word]


def parse_word_string(string):
   value_string=re.search(number,string).group()
   print(value_string)
   value=float(value_string.replace(",",""))
   word=re.search(amounts,string,flags=re.I).group().lower()
   #print(word)
   word_value=word_dict(word)
   return value*word_value

def parse_value_string(string):
   value_string=re.search(number,string).group()
   return float(value_string.replace(",",""))


def money_conversion(money):
   if money=="N/A":
      return None
   if isinstance(money,list):
      money=money[0]
   word_syntax=re.search(word_re,money,flags=re.I)
   value_syntax=re.search(value_re,money)

   if word_syntax:
      #print("word_syntax")
      #print(word_syntax.group())
      return parse_word_string(word_syntax.group().lower())

   elif value_syntax:
      #print("value_syntax")
      #print(value_syntax.group())
      return parse_value_string(value_syntax.group())

#clean date time
from datetime import datetime as dt
import json

def load_data(title):
   with open(title,"r") as fil:
      return json.load(fil)

def clean_date(date):
   return date.split("(")[0].strip()

def date_conversion(date):

   if date=="N/A":
      return None

   if isinstance(date,list):
      date=date[0]

   date_str=clean_date(date)

   fonts=["%B %d, %Y","%d %B, %y"]

   for i in fonts:
      try:
         return dt.strptime(date_str,i)
      except:
         pass
   return None

def write_pickle(title,movie_info):
   with open(title,"wb") as fil:
      pickle.dump(movie_info,fil)
      print("successfull")
      
def load_pickle(title):
   with open(title,"rb") as fil:
      return pickle.load(fil)
   

#movie=get_url("https://en.wikipedia.org/wiki/The_Great_Locomotive_Chase")
#print(movie)
import re

number=r"\d+(,\d{3})*\.*\d*"
amounts=r"thousand|million|billion"
value_re=rf"\${number}"
word_re=rf"\${number}(-|\sto\s)?({number})?\s({amounts})"

url1="https://en.wikipedia.org"
all_disney=requests.get(url1+"/wiki/List_of_Walt_Disney_Pictures_films")
soup=bs(all_disney.content)

movies_link=[]
none_type=[]
movie_info_box=[]
movie_title=[]

movies=soup.select(".wikitable.sortable i a")

for index,movie in enumerate(movies):
   try:
      link=movie["href"]
      movies_link.append(link)
      movie_title.append(movie['title'])
      print(movie['title'])
      full_url=url1+link
      movie_info_box.append(get_url(full_url))
   except Exception as e:
      none_type.append(movie.get_text())
      print(e)

print("disney pictures link length {}".format(len(movies_link)))
print("disney pic movies {} ".format(len(movie_title)))
print("none type movies {}".format(len(none_type)))
for i in none_type:
   print("none type {}".format(i))
print("overall movie data {}".format(len(movie_info_box)))

#movie_info_box=load_data_json("disney_movies2.json")

for movie in movie_info_box:
   movie["Running time (int)"]=clean_minutes(movie.get("Running time","N/A"))
   #print(movie["Running time (int)"])

#movies=[movie.get("Running time (int)",'N/A')for movie in movie_info_box]
#print(movies)

#print(movie_info_box)



for movie in movie_info_box:
   movie["Budget (float)"]=money_conversion(movie.get("Budget","N/A"))
   movie["Box office (float)"]=money_conversion(movie.get("Box office","N/A"))
   movie["Release date (datetime)"]=date_conversion(movie.get("Release date","N/A"))

#print(movie_info_box)

#write_pickle("store.pickle",movie_info_box)

data=load_pickle("store.pickle")

print(data[-10])

#save_json("disney_movies2.json",movie_info_box)




#movies_data=load_data_json("disney_movies.json")

#print(movies_data[0]["Box office"])
#for movie in movies_data:
   #movie["Box office (float)"]=money_conversion(movie.get("Box office","N/A"))
   #print(movie["Box office (float)"])
#print(money_conversion("$"))

   #write_pickle("store_disney.pickle",movie["Box office (float)"])

#print(load_pickle("store_disney.pickle"))
#movie_data=load_data("disney_movies2.json")

#dates=[date.get("Release date","N/A")for date in movie_data]

#for date in dates:
   #dat=date_conversion(date)
   #print(dat)
