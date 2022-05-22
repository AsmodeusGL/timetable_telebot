import name_token
import parse

import telebot
from telebot import types

bot = telebot.TeleBot(name_token.name)


@bot.message_handler(commands=['start'])
def start(message):
    if message.text.isalpha():
        if message.text.lower() == 'расписание':
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            button_bus = types.InlineKeyboardButton(text='Автобус', callback_data='Автобус')
            button_trolleybus = types.InlineKeyboardButton(text='Троллейбус', url='https://kogda.by/routes/minsk/trolleybus')
            button_tram = types.InlineKeyboardButton(text='Трамвай', url='https://kogda.by/routes/minsk/tram')
            button_subway = types.InlineKeyboardButton(text='Метро', url='https://kogda.by/routes/minsk/metro')
            keyboard.add(button_bus, button_trolleybus, button_tram, button_subway)
            bot.send_message(message.chat.id, 'Выберете тип транспорта', reply_markup=keyboard)
        else:
            bot.send_message(message.chat.id, 'Данный бот предназначен для получения информации расписания'
                                              ' маршрутного транспортного средства. Введите "Расписание"')


@bot.callback_query_handler(func=lambda callback: callback.data)
def check(callback):
    if callback.data == 'Автобус':
        bot.send_message(callback.message.chat.id, 'Введите номер автобуса')


@bot.message_handler(func=lambda message: message.text.isdigit())
def qwer(message):
    x = parse.start()
    bot.send_message(message.chat.id, f'{x[int(message.text) - 1]}')



bot.polling()
