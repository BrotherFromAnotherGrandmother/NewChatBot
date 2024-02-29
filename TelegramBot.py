import time
import requests
import telegram
from dotenv import load_dotenv
import os


def main():
    load_dotenv()
    bot = telegram.Bot(token=os.environ['TELEGRAM_TOKEN'])
    headers = {
        "Authorization": f"Token {os.environ['DEVMAN_TOKEN']}"
    }

    url = 'https://dvmn.org/api/long_polling/'
    current_timestamp = time.time()

    counter = 0
    while True:
        counter += 1
        try:
            payload = {"timestamp": current_timestamp}

            response = requests.get(url, headers=headers, params=payload)
            response.raise_for_status()
            decoded_response = response.json()
            if 'error' in decoded_response:
                raise requests.exceptions.HTTPError(decoded_response['error'])

            current_timestamp = decoded_response['last_attempt_timestamp']

            if decoded_response['new_attempts'][0]['is_negative']:
                bot.send_message(chat_id=os.environ['TG_CHAT_ID'], text=f'''
                Преподаватель проверил работу! {decoded_response['new_attempts'][0]['lesson_title']}
                Ну ты внатуре не баклажан. И нихуя ты не кабан
                Непррррравильно, ёбаные волки!
                Ссылка на урок: {decoded_response['new_attempts'][0]['lesson_url']}
                ''')
            else:
                bot.send_message(chat_id=os.environ['TG_CHAT_ID'], text=f'''
                Преподаватель проверил работу! {decoded_response['new_attempts'][0]['lesson_title']}
                Ты анакондовый Джанго! Всё правильно? Ну естеееесвенно!
                Ссылка на урок: {decoded_response['new_attempts'][0]['lesson_url']}''')

        except requests.exceptions.ReadTimeout:
            if counter == 10:
                time.sleep(120)
                counter = 0
            continue
        except requests.exceptions.ConnectionError:
            if counter == 10:
                time.sleep(120)
                counter = 0
            continue


if __name__ == '__main__':
    main()
