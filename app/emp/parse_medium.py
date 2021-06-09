from bs4 import BeautifulSoup
import requests
from pprint import pprint


soup = False
with open("html") as fp:
    soup = BeautifulSoup(fp, 'html.parser')

#url = 'https://medium.com/veve-collectibles/dc-cover-girls-series-1-c37f14a378ad'
#r = requests.get(url)
#soup = BeautifulSoup(r.content, 'html.parser')

print(type(soup))
#print(vars(soup))
xo = soup.find_all("strong", class_="iz jt")
pprint(xo)
