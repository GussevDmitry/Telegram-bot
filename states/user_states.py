from telebot.handler_backends import State, StatesGroup

class UserStateInfo(StatesGroup):
    name = State()
    age = State()
    country = State()
    city = State()
    phone_num = State()