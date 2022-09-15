from telebot.handler_backends import State, StatesGroup


class UserStateInfo(StatesGroup):
    name = State()
    age = State()
    country = State()
    city = State()
    phone_num = State()
    info_collected = State()
    search_city = State()
    rooms_number = State()
    people_amount = State()
    trip_year = State()
    hotels_count = State()
    hotels_photo_flag = State()
    hotels_photo_count = State()
    confirm_data = State()
    price_range = State()
    distance_range = State()
