import name_token
import telebot
import datetime
from telebot import types

bot = telebot.TeleBot(name_token.name)


@bot.message_handler()
def start(message):
    match message.text.lower():
        case 'расписание':
            kb = types.InlineKeyboardMarkup(row_width=1)
            button_bus = types.InlineKeyboardButton(text='Автобус', url='https://kogda.by/routes/minsk/autobus')
            button_trolleybus = types.InlineKeyboardButton(text='Троллейбус', url='https://kogda.by/routes/minsk/trolleybus')
            button_tram = types.InlineKeyboardButton(text='Трамвай', url='https://kogda.by/routes/minsk/tram')
            button_subway = types.InlineKeyboardButton(text='Метро', url='https://kogda.by/routes/minsk/metro')
            kb.add(button_bus, button_trolleybus, button_tram, button_subway)
            bot.send_message(message.chat.id, 'Расписание', reply_markup=kb)
        case 'время':
            bot.send_message(message.chat.id, f'Время отправки сообщения {datetime.datetime.utcfromtimestamp(message.date + 3 * 60 * 60)}')
        case _:
            bot.reply_to(message, message.text)


bot.polling()
