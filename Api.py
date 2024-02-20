from pprint import pprint

import requests

headers = {
    "Authorization": "Token 6ebf52cd576855857e60303b91c292a6cab40497"
}

url = 'https://dvmn.org/api/long_polling/'
response = requests.get(url, headers=headers)


print(response)
pprint(response.json())