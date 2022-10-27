from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def request_confirmation() -> InlineKeyboardMarkup:
    """
    Creating the inline keyboard to confirm (or not confirm) collected information
    :return: InlineKeyboardMarkup with buttons "Да" and "Нет"
    """
    kb = InlineKeyboardMarkup()
    yes_b = InlineKeyboardButton(text="Да", callback_data="confirm_yes")
    no_b = InlineKeyboardButton(text="Нет", callback_data="confirm_no")
    kb.add(yes_b, no_b)

    return kb
