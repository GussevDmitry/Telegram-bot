from telebot.handler_backends import State, StatesGroup

class UserStateInfo(StatesGroup):
    name = State()
    age = State()
    country = State()
    city = State()
    phone_num = State()
    info_collected = State()
    language = State()
    currency = State()
    search_city = State()
    dates = State()
    hotels_count = State()
    hotels_photo = State()
    lowprice = State()
    highprice = State()
    bestdeal = State()