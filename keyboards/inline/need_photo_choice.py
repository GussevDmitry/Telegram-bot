from telebot.types import InlineKeyboardMarkup,InlineKeyboardButton


def need_photo_choice():
    kb = InlineKeyboardMarkup()
    button_yes = InlineKeyboardButton(text="Да", callback_data="да")
    button_no = InlineKeyboardButton(text="Нет", callback_data="нет")
    kb.add(button_yes, button_no)

    return kb
