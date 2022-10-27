from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def show_history_results(ident: int) -> InlineKeyboardMarkup:
    """
    Creating inline keyboard to show results of the request with specified id
    :param ident: request identification number
    :return: InlineKeyboardMarkup with button "Показать результаты!"
    """
    kb = InlineKeyboardMarkup()
    button = InlineKeyboardButton("Показать результаты!", callback_data=f"Id{ident}")
    kb.add(button)

    return kb
