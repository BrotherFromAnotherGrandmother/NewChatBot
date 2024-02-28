import time
from pprint import pprint
import requests
import telegram
from dotenv import load_dotenv
import os

load_dotenv()


def main():
    bot = telegram.Bot(token=os.environ['TELEGRAM_TOKEN'])
    headers = {
        "Authorization": f"Token {os.environ['DEVMAN_TOKEN']}"
    }

    url = 'https://dvmn.org/api/long_polling/'
    current_timestamp = time.time()
    while True:
        try:
            payload = {"timestamp": current_timestamp}

            response = requests.get(url, headers=headers, params=payload)
            response.raise_for_status()
            decoded_response = response.json()
            if 'error' in decoded_response:
                raise requests.exceptions.HTTPError(decoded_response['error'])

            current_timestamp = decoded_response['last_attempt_timestamp']

            if decoded_response['new_attempts'][0]['is_negative']:
                bot.send_message(chat_id=os.environ['CHAT_ID'], text=f'''
                Преподаватель проверил работу! {decoded_response['new_attempts'][0]['lesson_title']}
                Ну ты внатуре не баклажан. И нихуя ты не кабан
                Непррррравильно, ёбаные волки!
                Ссылка на урок: {decoded_response['new_attempts'][0]['lesson_url']}
                ''')
            else:
                bot.send_message(chat_id=2131163741, text=f'''
                Преподаватель проверил работу! {decoded_response['new_attempts'][0]['lesson_title']}
                Ты анакондовый Джанго! Всё правильно? Ну естеееесвенно!
                Ссылка на урок: {decoded_response['new_attempts'][0]['lesson_url']}''')

        except requests.exceptions.ReadTimeout:
            continue
        except requests.exceptions.ConnectionError:
            continue

        print(response)
        pprint(decoded_response)
        print('')


if __name__ == '__main__':
    main()
