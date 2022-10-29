from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def need_photo_choice() -> InlineKeyboardMarkup:
    """
    Creating the inline keyboard to confirm user's choice
    :return: InlineKeyboardMarkup with buttons "Да" and "Нет"
    """
    kb = InlineKeyboardMarkup()
    button_yes = InlineKeyboardButton(text="Да", callback_data="да")
    button_no = InlineKeyboardButton(text="Нет", callback_data="нет")
    kb.add(button_yes, button_no)

    return kb
