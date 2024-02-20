from pprint import pprint

import requests

headers = {
    "Authorization": "Token 6ebf52cd576855857e60303b91c292a6cab40497"
}

url = 'https://dvmn.org/api/long_polling/'

while True:
    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.ReadTimeout:
        continue
    except requests.exceptions.ConnectionError:
        continue


    print(response)
    pprint(response.json())
    print('')