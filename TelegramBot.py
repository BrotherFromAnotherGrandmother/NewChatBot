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
    while True:
        try:
            payload = {"timestamp": current_timestamp}

            response = requests.get(url, headers=headers, params=payload,  timeout=120)
            response.raise_for_status()
            review_information = response.json()

            if review_information['status'] == 'timeout':
                current_timestamp = review_information['timestamp_to_request']
                continue

            if review_information['status'] == 'found':
                current_timestamp = review_information['last_attempt_timestamp']

            if review_information['new_attempts'][0]['is_negative']:
                bot.send_message(chat_id=os.environ['TG_CHAT_ID'], text=f'''
                Преподаватель проверил работу! {review_information['new_attempts'][0]['lesson_title']}
                Ну ты внатуре не баклажан. И нихуя ты не кабан
                Непррррравильно, ёбаные волки!
                Ссылка на урок: {review_information['new_attempts'][0]['lesson_url']}
                ''')
            else:
                bot.send_message(chat_id=os.environ['TG_CHAT_ID'], text=f'''
                Преподаватель проверил работу! {review_information['new_attempts'][0]['lesson_title']}
                Ты анакондовый Джанго! Всё правильно? Ну естеееесвенно!
                Ссылка на урок: {review_information['new_attempts'][0]['lesson_url']}''')

        except requests.exceptions.ReadTimeout:
            continue
        except requests.exceptions.ConnectionError:
            continue


if __name__ == '__main__':
    main()
