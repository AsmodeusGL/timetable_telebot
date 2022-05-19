import name_token
import telebot
import datetime

bot = telebot.TeleBot(name_token.name)


@bot.message_handler()
def start(message):
    match message.text.lower():
        case 'время':
            bot.send_message(message.chat.id, f'Время отправки сообщения {datetime.datetime.utcfromtimestamp(message.date + 3 * 60 * 60)}')
        case _:
            bot.reply_to(message, message.text)


bot.polling()
