from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def start_search():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    bt = KeyboardButton("Запустить поиск!", )
    kb.add(bt)
    return kb