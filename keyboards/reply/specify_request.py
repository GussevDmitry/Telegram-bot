from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def specify_request() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    lp_button = KeyboardButton("/lowprice")
    hp_button = KeyboardButton("/highprice")
    bd_button = KeyboardButton("/bestdeal")
    kb.add(lp_button, hp_button, bd_button)
    return kb