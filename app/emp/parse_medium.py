from bs4 import BeautifulSoup
from pprint import pprint


soup = False
with open("html") as fp:
    soup = BeautifulSoup(fp, 'html.parser')

print(soup)
pprint(soup.title.name)
pprint(soup.p)



