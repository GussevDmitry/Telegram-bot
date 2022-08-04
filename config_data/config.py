import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
RAPID_API_KEY = os.getenv('RAPID_API_KEY')
DEFAULT_COMMANDS = (
    ('start', "\U0001F449 Запустить бота"),
    ('help', "\U0001F446 Вывести справку"),
    ('survey', '\U0001F4AC Запустить опрос информации по пользователю'),
    ('lowprice', '\U0001F4C9 Вывод самых дешёвых отелей в городе'),
    ('highprice', '\U0001F4C8 Вывод самых дорогих отелей в городе'),
    ('bestdeal', '\U0001F451 Вывод отелей, наиболее подходящих по цене и расположению от центра'),
    ('history', '\U0001F4DD Вывод истории поиска отелей')
)

ALL_COUNTRIES = []