import name_token
import parse

import telebot
from telebot import types

bot = telebot.TeleBot(name_token.name)


@bot.message_handler(commands=['start'])
@bot.message_handler(func=lambda message: message.text.isalpha())
def start(message):
    if message.text.lower() == 'расписание':
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        button_bus = types.InlineKeyboardButton(text='Автобус', callback_data='Автобус')
        button_trolleybus = types.InlineKeyboardButton(text='Троллейбус', callback_data='Троллейбус')
        button_tram = types.InlineKeyboardButton(text='Трамвай', callback_data='Трамвай')
        button_subway = types.InlineKeyboardButton(text='Метро', callback_data='Метро')
        keyboard.add(button_bus, button_trolleybus, button_tram, button_subway)
        bot.send_message(message.chat.id, 'Выберете тип транспорта', reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, 'Данный бот предназначен для получения информации расписания'
                                          ' маршрутного транспортного средства. Введите "Расписание"')


@bot.callback_query_handler(func=lambda callback: callback.data)
def check(callback):
    match callback.data:
        case 'Автобус':
            w = bot.send_message(callback.message.chat.id, 'Введите номер автобуса')
            bot.register_next_step_handler(w, qwer)
        case 'Троллейбус':
            w = bot.send_message(callback.message.chat.id, 'Введите номер троллейбуса')
            bot.register_next_step_handler(w, qwer)
        case 'Трамвай':
            w = bot.send_message(callback.message.chat.id, 'Введите номер трамвая')
            bot.register_next_step_handler(w, qwer)
        case 'Метро':
            w = bot.send_message(callback.message.chat.id, 'Введите цвет линии метро')
            bot.register_next_step_handler(w, qwer)


def qwer(message):
    x = parse.start()
    bot.send_message(message.chat.id, f'{x[int(message.text) - 1]}')


bot.polling()
