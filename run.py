import os
import requests
from bs4 import BeautifulSoup
#Public base URL
base_url = "https://www.gob.mx{}"
current = 1
full_url = "https://www.gob.mx/presidencia/es/archivo/articulos?category=764&filter_origin=archive&idiom=es&order=DESC&page={}"
#Getting first page
r = requests.get(full_url.format(str(current)))
contn = BeautifulSoup(r.content, 'html.parser')
#Iterate over content while article is in it
while contn.find_all('article'):
  #iterate over articles in page
  for i in contn.find_all('article'):
    month = "-".join(i.time["date"].replace("\\\"","").split("-")[::-1][1:])
    name = i.a["href"].replace("\\\"","").split("?")[0].split("/")[-1]
    link = i.a["href"].replace("\\\"","")
    tmp = requests.get(base_url.format(link))
    #Folder three generator with format /root/month-year/file_name.txt
    path = "/content/conferencias/{}/{}.txt".format(month,name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    #Conference data extraction
    with open(path,"w") as f:
      f.write(BeautifulSoup(tmp.content, 'html.parser').find("div",{"class": "article-body"}).text)
  current += 1
  #Next page view
  r = requests.get(full_url.format(str(current)))
  contn = BeautifulSoup(r.content, 'html.parser')