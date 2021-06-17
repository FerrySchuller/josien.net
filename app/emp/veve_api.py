from dotenv import load_dotenv
load_dotenv()

import requests
import os
from pprint import pprint

#url = "https://api.prod.veve.me/graphql"
url = 'https://api.prod.veve.me/api/auth/totp/send'

headers = {'etag': os.getenv('etag')}

endpoint = 'graphql'
data = {"email":"ferry@f-inter.net"}
#data = {"operationName":"OmiConversionRate","variables":{},"query":"query OmiConversionRate {\n  omiConversionRate\n}\n"}


r = requests.post(url, data, headers=headers )
pprint(vars(r))
pprint(r)

pprint(r.content)
#if r.json:
#    pprint(r.json())
