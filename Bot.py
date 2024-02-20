import telegram
bot = telegram.Bot(token='6813297671:AAGyzgBHwpQGFy-jaIdAUy98OIsbArwms18')
chat_id = 2131163741
user = bot.get_chat_member(chat_id=chat_id, user_id=chat_id)
user_name = user.user.first_name

bot.send_message(chat_id=2131163741, text=f"Hello, {user_name}")
