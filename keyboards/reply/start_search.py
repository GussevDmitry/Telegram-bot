from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def start_search() -> ReplyKeyboardMarkup:
    """
    Creating reply keyboard to start search
    :return: ReplyKeyboardMarkup with text "Запустить поиск!"
    """
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    bt = KeyboardButton("Запустить поиск!")
    kb.add(bt)
    return kb
