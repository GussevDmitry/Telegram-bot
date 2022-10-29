from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def change_room_amount() -> InlineKeyboardMarkup:
    """
    Creating the inline keyboard to choose if user would like to change room amount
    :return: InlineKeyboardMarkup with buttons "Да" and "Нет"
    """
    kb = InlineKeyboardMarkup()
    yes_b = InlineKeyboardButton(text="Да", callback_data="change_y")
    no_b = InlineKeyboardButton(text="Нет", callback_data="change_n")
    kb.add(yes_b, no_b)

    return kb
