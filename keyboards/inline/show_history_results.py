from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def show_history_results(ident):
    kb = InlineKeyboardMarkup()
    button = InlineKeyboardButton("Показать результаты!", callback_data=f"Id{ident}")
    kb.add(button)
    return kb