from datetime import time, datetime, timezone, timedelta
from pytz import timezone
import pytz
import logging

from config import TIME_ZONE
from functions import get_weather_today, send_currency_price
from keyboards import kb_cryptocurrency, kb_set_language

from telegram.ext import Job

# from dateutil.tz import *


def start(update, context):
    update.message.reply_text(
        "Привет! Сейчас нам нужно настроить некоторые параметры",
        reply_markup=kb_set_language(),
    )


def help_me(update, context):
    update.message.reply_text(
        """
    Supported commands:
    /help - Show help
    /weather - Add task send weather cast. Format
    /weather 0 1 2 3 4 5 6 7:00
    """
    )


def add_weather_task(update, context):
    logging.info("Call add_weather_task functions")
    # TODO try/except
    if len(context.args) > 1:
        send_days = []
        for i in context.args[0:-1]:
            send_days.append(int(i))
        send_time = time(
            int(context.args[-1].split(sep=":")[0]),
            int(context.args[-1].split(sep=":")[1]),
            tzinfo=pytz.timezone("Europe/Moscow"),
        )
        context.job_queue.run_daily(
            get_weather_today,
            send_time,
            days=(tuple(send_days)),
            context=update.message.chat_id,
            name="daily weather",
        )
        update.message.reply_text("Задание добавлено")


def add_crypto_currency_price_task(update, context):
    logging.info("Call add_crypto_currency_price_task functions")
    # TODO parse args, try/except
    # TODO request timezone
    if len(context.args) > 1:
        currency = context.args[0].strip()
        send_days = []
        for i in context.args[1:-1]:
            send_days.append(int(i) - 1)
        send_time = time(
            int(context.args[-1].split(sep=":")[0]),
            int(context.args[-1].split(sep=":")[1]),
            tzinfo=pytz.timezone("Europe/Moscow"),
        )
    context.user_data["chat_id"] = update.message.chat_id
    context.job_queue.run_daily(
        send_currency_price,
        send_time,
        days=(tuple(send_days)),
        context=context,
        name="daily crypto price",
    )


def remove_task(update, context):
    reply_list = []
    for item in context.job_queue.jobs():
        reply_list.append(f"{item.name}, {item.next_t}")
    update.message.reply_text(reply_list)

