from telebot.handler_backends import State, StatesGroup


class UserStateInfo(StatesGroup):
    """
    Class which represents states of user (logical scenario which store information about user's "location" in project)

    Attributes:
        name (State): username collected
        age (State): user age collected
        country (State): user residence country collected
        city (State): user residence city collected
        phone_num (State): user's phone number
        info_collected (State): personal information about user collected
        search_city (State): destination collected
        rooms_number (State): amount of rooms collected
        people_amount (State): amount of people in every room collected
        trip_year (State): year of the trip collected
        hotels_count (State): amount of hotels collected
        # hotels_photo_flag (State): username
        hotels_photo_count (State): amount of hotels' photos collected
        # confirm_data (State): username
        price_range (State): the range of hotels' price collected
        distance_range (State): the range of the distance between the hotel and the city center collected
    """
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
    # hotels_photo_flag = State()
    hotels_photo_count = State()
    # confirm_data = State()
    price_range = State()
    distance_range = State()
