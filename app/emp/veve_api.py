import requests
from pprint import pprint

url = "https://api.prod.veve.me/graphql"
endpoint = 'graphql'
data = {"operationName":"OmiConversionRate","variables":{},"query":"query OmiConversionRate {\n  omiConversionRate\n}\n"}


r = requests.post(url, data)
pprint(vars(r))
pprint(r)
pprint(r.json())
