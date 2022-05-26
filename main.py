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
            bot.register_next_step_handler(message_, bus, 'https://minsk.btrans.by/avtobus')
        case 'btn_trolleybus':
            message_ = bot.send_message(callback_query.message.chat.id, 'Введите номер троллейбуса')
            bot.register_next_step_handler(message_, bus, 'https://minsk.btrans.by/trollejbus')
        case 'btn_tram':
            message_ = bot.send_message(callback_query.message.chat.id, 'Введите номер трамвая')
            bot.register_next_step_handler(message_, bus, 'https://minsk.btrans.by/tramvaj')


def bus(message, url):
    numbers_ = [item.split('/')[4] for item in parse.start_bus(url)]
    dict_ = {}
    links = []
    keyboard = types.InlineKeyboardMarkup(row_width=1)

    if message.text in [el.partition('%')[0] for el in numbers_]:
        for value, number in enumerate(numbers_):
            if message.text == number.partition('%')[0]:
                links.append(parse.start_bus(url)[value])
        for num, link in enumerate(links):
            dict_[f'avtobus{num}'] = f'{unquote(link.split("/")[4])}'
        for key, value in dict_.items():
            key = types.InlineKeyboardButton(text=f'{value}', callback_data=f'{value}')
            keyboard.add(key)
        bot.send_message(message.chat.id, 'Выберите', reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, 'Данного автобуса не существует')
    return links


bot.polling()
