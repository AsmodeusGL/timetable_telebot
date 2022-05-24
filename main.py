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
            var_1 = bot.send_message(callback.message.chat.id, 'Введите номер автобуса')
            bot.register_next_step_handler(var_1, bus)
        case 'Троллейбус':
            var_2 = bot.send_message(callback.message.chat.id, 'Введите номер троллейбуса')
            bot.register_next_step_handler(var_2, trolleybus)
        case 'Трамвай':
            var_3 = bot.send_message(callback.message.chat.id, 'Введите номер трамвая')
            bot.register_next_step_handler(var_3, tram)
        case 'Метро':
            w = bot.send_message(callback.message.chat.id, 'Введите цвет линии метро')
            bot.register_next_step_handler(w, bus)


def bus(message):
    arr = [item for item in parse.start_bus() if message.text in item.split('/')[4][0]]
    print(arr)
    bot.send_message(message.chat.id, f'{parse.start_bus()[int(message.text) - 1]}')


def trolleybus(message):
    bot.send_message(message.chat.id, f'{parse.start_trolleybus()[int(message.text) - 1]}')


def tram(message):
    bot.send_message(message.chat.id, f'{parse.start_tram()[int(message.text) - 1]}')


bot.polling()
