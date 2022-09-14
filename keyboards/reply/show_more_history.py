from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def show_more_history():
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    bt = KeyboardButton("Показать историю запросов")
    kb.add(bt)

    return kb