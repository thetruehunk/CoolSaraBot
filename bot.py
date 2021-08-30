import logging

from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    Dispatcher,
    Filters,
    MessageHandler,
    Updater,
)

from config import BOT_TOKEN
from handlers import add_weather_task, add_crypto_currency_price_task, help_me, start, remove_task
from keyboards import kb_cryptocurrency, kb_set_language

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    filename="bot.log",
)


def main():
    bot = Updater(BOT_TOKEN, use_context=True)
    dp = bot.dispatcher

    logging.info("Bot is run")

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_me))
    dp.add_handler(CommandHandler("weather", add_weather_task, pass_job_queue=True, pass_args=True))
    dp.add_handler(CommandHandler("crypto", add_crypto_currency_price_task, pass_job_queue=True, pass_args=True))
    dp.add_handler(CommandHandler('remove', remove_task, pass_job_queue=True, pass_args=True))

    bot.start_polling()
    bot.idle()


if __name__ == "__main__":
    main()

