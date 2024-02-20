import time
from pprint import pprint

import requests

headers = {
    "Authorization": "Token 6ebf52cd576855857e60303b91c292a6cab40497"
}

url = 'https://dvmn.org/api/long_polling/'
current_timestamp = time.time()
while True:
    try:
        payload = {"timestamp": current_timestamp}
        response = requests.get(url, headers=headers, timeout=5, params=payload)
        current_timestamp = response.json()['last_attempt_timestamp']
    except requests.exceptions.ReadTimeout:
        continue
    except requests.exceptions.ConnectionError:
        continue


    print(response)
    pprint(response.json())
    print('')