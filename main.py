import parse
import telebot
import os
import logging
from urllib.parse import *

bot = telebot.TeleBot(os.getenv('token'))
logger = telebot.logger
logger.setLevel(logging.DEBUG)


def get_keyboard():
    buttons = [
        telebot.types.InlineKeyboardButton(text='Автобус', callback_data='btn_bus'),
        telebot.types.InlineKeyboardButton(text='Троллейбус', callback_data='btn_trolleybus'),
        telebot.types.InlineKeyboardButton(text='Трамвай', callback_data='btn_tram')
    ]
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard


@bot.message_handler(commands=['start'])
@bot.message_handler(func=lambda message: message.text.isalpha())
def start(message):
    match message.text.lower():
        case 'расписание':
            bot.send_message(message.chat.id, 'Выберите тип транспорта', reply_markup=get_keyboard())
        case '/start':
            keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(telebot.types.KeyboardButton(text='Расписание'))
            bot.send_message(message.chat.id, 'Нажмите на кнопку "Расписание"', reply_markup=keyboard)
        case _:
            bot.send_message(message.chat.id, 'Данный бот предназначен для получения информации расписания'
                                              ' маршрутного транспортного средства. Введите "Расписание"')


@bot.callback_query_handler(func=lambda callback: callback.data.startswith('btn_'))
def check_keyboard_callback(callback_query: telebot.types.CallbackQuery):
    match callback_query.data:
        case 'btn_bus':
            message_ = bot.send_message(callback_query.message.chat.id, 'Введите номер автобуса')
            bot.register_next_step_handler(message_, transport_numbers, 'https://minsk.btrans.by/avtobus')
        case 'btn_trolleybus':
            message_ = bot.send_message(callback_query.message.chat.id, 'Введите номер троллейбуса')
            bot.register_next_step_handler(message_, transport_numbers, 'https://minsk.btrans.by/trollejbus')
        case 'btn_tram':
            message_ = bot.send_message(callback_query.message.chat.id, 'Введите номер трамвая')
            bot.register_next_step_handler(message_, transport_numbers, 'https://minsk.btrans.by/tramvaj')


@bot.callback_query_handler(func=lambda callback: callback.data)
def check_route(callback_query: telebot.types.CallbackQuery):
    if callback_query.data.startswith('https'):
        keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
        for number, (key, value) in enumerate(parse.routes(callback_query.data).items()):
            button = telebot.types.InlineKeyboardButton(text=key, callback_data=f'{number}{callback_query.data}')
            keyboard.add(button)
        bot.send_message(callback_query.message.chat.id, 'Выберите направление', reply_markup=keyboard)
    elif callback_query.data.startswith('number_'):
        for key, value in parse.timetable(callback_query.data).items():
            bot.send_message(callback_query.message.chat.id, key)
            for hour in value[1:]:
                for item in [item for item in value[0].split('-')][1:]:
                    hour = hour.replace(item, '\n' + item + '\t')
                bot.send_message(callback_query.message.chat.id, hour)
    else:
        try:
            keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
            for number, (key, value) in enumerate(parse.routes(callback_query.data[1:]).items()):
                for number_1, (key_1, value_1) in enumerate(value.items()):
                    if str(number) == callback_query.data[0]:
                        button = telebot.types.InlineKeyboardButton(text=key_1, callback_data=f'number_{number}_{number_1}_{callback_query.data[1:]}')
                        keyboard.add(button)
            bot.send_message(callback_query.message.chat.id, 'Выберите остановку', reply_markup=keyboard)
        except IndexError:
            bot.send_message(callback_query.message.chat.id, 'Расписаний на данный маршрут не существует!')


def transport_numbers(message, url):
    numbers_ = {value: item.split('/')[4] for value, item in enumerate(parse.parse_numbers(url)) if message.text == item.split('/')[4].partition('%')[0]}
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
    if numbers_:
        for number, value in numbers_.items():
            key = telebot.types.InlineKeyboardButton(text=f'{unquote(value)}', callback_data=f'{parse.parse_numbers(url)[number]}')
            keyboard.add(key)
        bot.send_message(message.chat.id, 'Выберите', reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, 'Данного номера не существует')


if __name__ == '__main__':
    bot.polling()
