

### Реализовать ###
- [ ] Прогноз погоды на сегодня (погода, текушая темп., min, max)
- [ ] Прогноз погоды на 5 дней
- [ ] Курс валют
- [ ] Планирование задач


<h1>Работа с очередью</h1>
https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.jobqueue.html


""" Докеризация приложения """
https://runnable.com/docker/python/dockerize-your-python-application


Рассмотреть возможность работы с Скедулером
Возможно, стоит установить эту библиотеку: https://pypi.python.org/pypi/schedule, в основном помогает делать все, что вы только что описали. Вот пример:

import schedule
import time

def job():
    print("I'm working...")

schedule.every(10).minutes.do(job)
schedule.every().hour.do(job)
schedule.every().day.at("10:30").do(job)
schedule.every().monday.do(job)
schedule.every().wednesday.at("13:15").do(job)

while True:
    schedule.run_pending()

""" Парсинг json конфига """
Working With JSON Data in Python
https://realpython.com/python-json/

parsed = ujson.loads("""{"name":"John"}""")
print(parsed["name"])

"""  Configuration files in Python  """
https://martin-thoma.com/configuration-files-in-python/