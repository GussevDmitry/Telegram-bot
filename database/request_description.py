from database.create_database import User, Request, Hotel, Photo, Landmark, db
from telebot.types import CallbackQuery
from typing import Dict, Tuple
from peewee import ModelSelect


def request_description(data: Dict) -> ModelSelect:
    """
    Sending query to database to collect information about user's requests (user's phone number is primary key)
    :param data: memory storage
    :return: Select query with user's request parameters
    """
    query_desc = User.select(Request.id, Request.name, Request.date_time, Request.curr, Request.location,
                             Request.rooms_amount, Request.people_count, Request.check_in, Request.check_out,
                             Request.price_range, Request.distance_range)\
        .where(User.phone_number == data.get('phone_number'))\
        .join(Request, on=(Request.user_id == User.phone_number))

    return query_desc


def request_results(call: CallbackQuery, data: Dict) -> ModelSelect:
    """
    Sending query to database to collect results of user's request (user's phone number is primary key)
    :param call: user's choice which request results to show
    :param data: memory storage
    :return: Select query with user's request results
    """
    query_res = User.select(Hotel.id, Hotel.hotel_id, Hotel.name, Hotel.star_rating, Hotel.guest_rating, Hotel.address,
                            Hotel.one_night_price, Hotel.price, Request.curr)\
        .where(User.phone_number == data.get('phone_number'))\
        .join(Request, on=(Request.user_id == User.phone_number)) \
        .join(Hotel, on=(Hotel.request_id == Request.id)) \
        .where(Request.id == int(call.data[2:]))

    return query_res


def photo_urls(data: Dict, call: CallbackQuery, i_hotel: Tuple) -> str:
    """
    Collecting hotel's photo urls from database (user's phone number is primary key)
    :param data: memory storage
    :param call: user's choice which request results to show
    :param i_hotel: select query result
    :return: string with hotel's photo urls
    """
    query_photo = User.select(Photo.photo_url) \
        .where(User.phone_number == data.get('phone_number')) \
        .join(Request, on=(Request.user_id == User.phone_number)) \
        .join(Hotel, on=(Hotel.request_id == Request.id)) \
        .where(Request.id == int(call.data[2:])) \
        .join(Photo, on=(Photo.hotel_id == i_hotel[1])) \
        .where(Hotel.hotel_id == i_hotel[1])

    url_lst = []
    for i_url in db.execute(query_photo):
        url_lst.append(i_url[0])
    url_str = ', '.join(url_lst)

    return url_str


def landmarks_info(data: Dict, call: CallbackQuery, i_hotel: Tuple) -> str:
    """
    Collecting hotel's landmarks and distances from landmarks to hotel from database
    (user's phone number is primary key)
    :param data: memory storage
    :param call: user's choice which request results to show
    :param i_hotel: select query result
    :return: string with landmarks and distances from landmarks to hotel
    """
    query_lm = User.select(Landmark.lm_name, Landmark.lm_distance) \
        .where(User.phone_number == data.get('phone_number')) \
        .join(Request, on=(Request.user_id == User.phone_number)) \
        .join(Hotel, on=(Hotel.request_id == Request.id)) \
        .where(Request.id == int(call.data[2:])) \
        .join(Landmark, on=(Landmark.hotel_id == i_hotel[1])) \
        .where(Hotel.hotel_id == i_hotel[1])

    lm_str = ''
    for i_lm in db.execute(query_lm):
        lm_str += f"{i_lm[0]} - {i_lm[1]}\n"

    return lm_str
