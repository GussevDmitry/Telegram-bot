from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def currency_choice() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    usd_b = InlineKeyboardButton(text="Доллар США", callback_data="доллар")
    eur_b = InlineKeyboardButton(text="Евро", callback_data="евро")
    rub_b = InlineKeyboardButton(text="Рубль", callback_data="рубль")
    kb.add(usd_b, eur_b, rub_b)
    return kb