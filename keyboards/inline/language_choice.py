from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def language_choice() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    rus_b = InlineKeyboardButton(text="Русский", callback_data="русский")
    eng_b = InlineKeyboardButton(text="Английский", callback_data="английский")
    kb.add(rus_b, eng_b)
    return kb