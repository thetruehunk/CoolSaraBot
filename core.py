#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Simple Bot to reply to Telegram messages.
This program is dedicated to the public domain under the CC0 license.
This Bot uses the Updater class to handle the bot.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic inline bot example. Applies different text transformations.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from uuid import uuid4
import telegram
from telegram.utils.helpers import escape_markdown
from telegram import InlineQueryResultArticle, ParseMode, \
    InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, InlineQueryHandler, \
    CommandHandler, CallbackQueryHandler
import datetime
from time import sleep
import logging
import requests
import emoji
import config  # подключаем конфигурационный файл


s_city = "Yevpatoriya,UA"
appid = "1111111111"

""" Settings """
#Time Zone
tz = 3
# Emoji
wind  = (emoji.emojize(':wind_face:'))
thermometer = (emoji.emojize(':thermometer:'))
watch  = (emoji.emojize(':watch:'))


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.


def start(update, context):
    """Send a message when the command /start is issued."""
    global chat_id
    update.message.reply_text(
        'Привет! Сейчас нам нужно настроить некоторые параметры',
        reply_markup=kbSetLang())
    chat_id = update.message.chat_id  # Полчучаем чат ID


def kbSetLang():
    keyboard = [[InlineKeyboardButton('Русский', callback_data='Ru')],
                [InlineKeyboardButton('English', callback_data='En')]]
    return InlineKeyboardMarkup(keyboard)


def setLangRu(update, context):
    query = update.callback_query
    # Здесь я планирую сохранять параметры языка
    query.edit_message_text('Вы выбрали русский!')


def setLangEn(update, context):
    # Здесь я планирую сохранять параметры языка
    update.message.reply_text('Your choise english!')


def help(update, context):
    """Send a message when the command /help is issued."""
    bot.send_message(chat_id, text="""Supported commands: 
    /help - Show help 
    /weather - Add task send weather cast. Format
    /weather 0 1 2 3 4 5 6 7:00""")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def addWeatherTask(update, context):
    """Add task send message when the command /weather + args."""
    if len(context.args) > 1:
        print("all args OK", context.args)
        sendDays = []
        for i in context.args[0:-1]:
            sendDays.append(int(i))
        sendTime = datetime.time(int(context.args[-1].split(sep=':')[0]) - tz , \
        int(context.args[-1].split(sep=':')[1]), 00)
        print(sendTime)
        context.job_morning = myJob.run_daily(getWeatherToday, sendTime, days=(
            tuple(sendDays)), context=None, name=None)


def rmTask(update, context):
    pass


def getWeatherToday(context):
    """Получаем погоду на сегодня"""
    res = requests.get("http://api.openweathermap.org/data/2.5/find",
                       params={'q': s_city, 'type': 'like', 'units': \
                       'metric', 'APPID': appid, 'lang': 'ru'})
    data = res.json()
    print(data)
    weather = str(*["{} ({}) {} \n {} {} {} {} {} {} \n {} {}".format(d['name'], d['sys']['country'], \
    d['weather'][0][u'description'], thermometer, int(d['main']['temp']), 'min:', int(d['main']['temp_min']), \
    'max:', int(d['main']['temp_max']), wind, int(d['wind']['speed']))
              for d in data['list']])
    context.bot.send_message(chat_id, text=weather)


def getWeatherForWeek(context):
    """Получаем погоду на неделю"""
    res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                       params={'q': s_city, 'type': 'like', 'units': \
                       'metric', 'APPID': appid, 'lang': 'ru'})


def addCryptoCurrencyPriceTask(update, context):
    """Add task send message when the command /crypto + args."""
    if len(context.args) > 1:
        print("all args OK", context.args)
        sendDays = []
        for i in context.args[0:-1]:
            sendDays.append(int(i))
        sendTime = datetime.time(int(context.args[-1].split(sep=':')[0]) - tz , \
        int(context.args[-1].split(sep=':')[1]), 00)
        print(sendTime)
        context.job_morning = myJob.run_daily(getCryptoCurrencyPrice, sendTime, days=(
            tuple(sendDays)), context=None, name=None)
        


def getCryptoCurrencyPrice(context):
    data = requests.get('https://api.coinmarketcap.com/v1/ticker/' + 'Ethereum')
    data_json = data.json()
    price = str(*["Текущая стоимость ETH: {:.6} {}% 24{}".format(a['price_usd'], \
    a['percent_change_24h'], watch) for a in data_json])
    context.bot.send_message(chat_id, text=price)


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(config.token, use_context=True)
    # Создаем очередь
    global myJob
    myJob = updater.job_queue
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("weather", addWeatherTask, pass_args=True))
    dp.add_handler(CommandHandler("crypto", addCryptoCurrencyPriceTask, pass_args=True))
    # add weather today
    # add weather for a week
    dp.add_handler(CallbackQueryHandler(setLangRu, pattern='Ru'))
    dp.add_handler(CallbackQueryHandler(setLangEn, pattern='En'))
    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
