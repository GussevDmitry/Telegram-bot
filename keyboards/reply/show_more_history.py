from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def show_more_history() -> ReplyKeyboardMarkup:
    """
    Creating reply keyboard with button "Показать историю запросов" to show user's history again
    :return: ReplyKeyboardMarkup with button "Показать историю запросов"
    """
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    bt = KeyboardButton("Показать историю запросов")
    kb.add(bt)

    return kb
