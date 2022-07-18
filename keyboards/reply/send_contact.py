from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def request_contact() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button = KeyboardButton("Отправить контакт",  request_contact=True)
    keyboard.add(button)
    return keyboard