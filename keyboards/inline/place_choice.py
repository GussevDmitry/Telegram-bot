from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import re


def place_choice(places):
    kb = InlineKeyboardMarkup()
    for i_data in places:
        pattern = rf"{i_data['name']}"
        if not re.search(pattern, i_data['description']):
            i_button = InlineKeyboardButton(f"{i_data['name']}, {i_data['description']}", callback_data=f"{i_data['dest_ID']}")
        else:
            i_button = InlineKeyboardButton(f"{i_data['description']}", callback_data=f"{i_data['dest_ID']}")
        kb.add(i_button)

    return kb