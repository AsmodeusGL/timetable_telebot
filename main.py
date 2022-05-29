import name_token
import parse
import telebot
from telebot import types
from urllib.parse import *

bot = telebot.TeleBot(name_token.name)


def get_keyboard():
    buttons = [
        types.InlineKeyboardButton(text='Автобус', callback_data='btn_bus'),
        types.InlineKeyboardButton(text='Троллейбус', callback_data='btn_trolleybus'),
        types.InlineKeyboardButton(text='Трамвай', callback_data='btn_tram')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard


@bot.message_handler(commands=['start'])
@bot.message_handler(func=lambda message: message.text.isalpha())
def start(message):
    if message.text.lower() == 'расписание':
        bot.send_message(message.chat.id, 'Выберете тип транспорта', reply_markup=get_keyboard())
    else:
        bot.send_message(message.chat.id, 'Данный бот предназначен для получения информации расписания'
                                          ' маршрутного транспортного средства. Введите "Расписание"')


@bot.callback_query_handler(func=lambda callback: callback.data.startswith('btn_'))
def check_keyboard_callback(callback_query: types.CallbackQuery):
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
def check_route(callback_query: types.CallbackQuery):
    if callback_query.data.startswith('https'):
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        for number, (key, value) in enumerate(parse.routes(callback_query.data).items()):
            button = types.InlineKeyboardButton(text=key, callback_data=f'{number}{callback_query.data}')
            keyboard.add(button)
        bot.send_message(callback_query.message.chat.id, 'Выберите направление', reply_markup=keyboard)
    else:
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        for number, (key, value) in enumerate(parse.routes(callback_query.data[1:]).items()):
            for key_1, value_1 in value.items():
                if str(number) == callback_query.data[0]:
                    button = types.InlineKeyboardButton(text=key_1, callback_data=f'{number}{callback_query.data}')
                    keyboard.add(button)
        bot.send_message(callback_query.message.chat.id, 'Выберите остановку', reply_markup=keyboard)


def transport_numbers(message, url):
    numbers_ = {value: item.split('/')[4] for value, item in enumerate(parse.parse_numbers(url)) if message.text == item.split('/')[4].partition('%')[0]}
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    if numbers_:
        for number, value in numbers_.items():
            key = types.InlineKeyboardButton(text=f'{unquote(value)}', callback_data=f'{parse.parse_numbers(url)[number]}')
            keyboard.add(key)
        bot.send_message(message.chat.id, 'Выберите', reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, 'Данного номера не существует')


bot.polling()
