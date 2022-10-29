from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def currency_choice() -> InlineKeyboardMarkup:
    """
    Creating the inline keyboard to choose the currency
    :return: InlineKeyboardMarkup with buttons "Доллар США", "Евро" and "Рубль"
    """
    kb = InlineKeyboardMarkup()
    usd_b = InlineKeyboardButton(text="Доллар США", callback_data="USD")
    eur_b = InlineKeyboardButton(text="Евро", callback_data="EUR")
    rub_b = InlineKeyboardButton(text="Рубль", callback_data="RUB")
    kb.add(usd_b, eur_b, rub_b)
    return kb
