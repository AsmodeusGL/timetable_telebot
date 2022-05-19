import name_token
import telebot

bot = telebot.TeleBot(name_token.name)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет!')


@bot.message_handler(commands=['end'])
def start(message):
    bot.send_message(message.chat.id, 'Пока!')


bot.polling()
