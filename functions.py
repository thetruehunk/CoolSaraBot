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
from telegram import (
    InlineQueryResultArticle,
    ParseMode,
    InputTextMessageContent,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Updater,
    InlineQueryHandler,
    CommandHandler,
    CallbackQueryHandler,
)
import datetime
import logging
import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from config import (
    WEATHER_URL,
    WEATHER_PARAM,
    DEFAULT_CITY,
    COINMARKET_API_KEY,
    COINMARKET_URL,
    COINMARKET_PARAM,
    COINMARKET_HEADERS,
)

# Keyboards

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.


def set_lang_ru(update, context):
    query = update.callback_query
    # Здесь я планирую сохранять параметры языка
    query.edit_message_text("Вы выбрали русский!")


def set_lang_en(update, context):
    # Здесь я планирую сохранять параметры языка
    update.message.reply_text("Your choise english!")


def get_weather_today(context):
    logging.info("Run get_weather_today functions")
    try:
        res = requests.get(WEATHER_URL, params=WEATHER_PARAM)
        data = res.json()
        return data

    except (ConnectionError, Timeout, TooManyRedirects) as err:
        logging.info(err)


def get_weather_for_week(context):
    """Получаем погоду на неделю"""
    res = requests.get(
        "http://api.openweathermap.org/data/2.5/forecast",
        params={
            "q": DEFAULT_CITY,
            "type": "like",
            "units": "metric",
            "APPID": WEATHER_TOKEN,
            "lang": "ru",
        },
    )


def get_crypto_currency_price(currency):
    try:
        logging.info("Run get_crypto_currency_price functions")
        res = requests.get(
            COINMARKET_URL,
            params=COINMARKET_PARAM,
            headers=COINMARKET_HEADERS,
        )
        currencys = json.loads(res.text)
        for item in currencys["data"]:
            if item["name"].upper() == currency.upper() or \
               item["symbol"].upper() == currency.upper():
                price = int(item["quote"]["USD"]["price"])
                return price

    except (ConnectionError, Timeout, TooManyRedirects, ValueError, KeyError) as err:
        logging.info(err)


def send_current_weather(context):
    get_weather_today(context)
    context.bot.send_message(
        chat_id=context.job.context.user_data["chat_id"],
        text=(
            f"Погода в {data['name']} сейчас:\n"
            f"Температура: 🌡{int(data['main']['temp'])}️°C\n"
            f"Ощущается как: 🖐️🌡{int(data['main']['feels_like'])}°C\n"
            f"Ветер 🌬️{int(data['wind']['speed'])}️м/c\n"
            f"{data['weather'][0]['description']}️\n"
        ),
    )


def send_currency_price(context):
    currency = context.job.context.args[0]
    price = get_crypto_currency_price(currency)
    context.bot.send_message(
        chat_id=context.job.context.user_data["chat_id"],
        text=(f"Current price of *{currency.upper()}* 💲*{price}*"),
        parse_mode=ParseMode.MARKDOWN,
    )

