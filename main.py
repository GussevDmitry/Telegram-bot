from loader import bot
import handlers
from utils.set_bot_commands import set_default_commands
from telebot.custom_filters import StateFilter
from requests.exceptions import ConnectTimeout, ConnectionError
from database.create_database import db, User, Request, Hotel, Photo, Landmark
from peewee import fn
from loguru import logger


def main():
    bot.add_custom_filter(StateFilter(bot))
    try:
        set_default_commands(bot)
        bot.polling(non_stop=True, timeout=15)
    except ConnectTimeout:
        print("Connection to api.telegram.org timed out")
    except ConnectionError:
        print("Connection to api.telegram.org failed")

    # for i in db.execute(Photo.select()):
    #     print(i)

    # photos = set()
    # for i in db.execute(Photo.select(Photo.photo_url)):
    #     photos.add(i[0])
    #
    # print(photos)

    # query = User.select(User.name, Request.name, Request.location, Hotel.id, Hotel.hotel_id, Landmark.lm_name)\
    #     .join(Request, on=(Request.user_id == User.phone_number))\
    #     .join(Hotel, on = (Hotel.request_id == Request.id)) \
    #     .where(Hotel.hotel_id == 470429)\
    #     .join(Landmark) \
    #
    # for i in db.execute(query):
    #     print(i)
    #
    # query_2 = User.select(User.name, fn.COUNT().alias('count'))\
    #     .left_outer_join(Request, on=(Request.user_id == User.phone_number)).group_by(User.name)
    #
    # for i in db.execute(query_2):
    #     print(i)

    """Получилось!!!!!!"""
    # query_total = User.select(User.name, Request.name, Request.location, Request.rooms_amount, Request.people_count,
    #                           Request.check_in, Request.check_out, Hotel.name, Hotel.star_rating, Hotel.address,
    #                           Hotel.price, Photo.photo_url)\
    #     .join(Request, on=(Request.user_id == User.phone_number))\
    #     .join(Hotel, on=(Hotel.request_id == Request.id))\
    #     .join(Photo, on=(Photo.hotel_id == Hotel.id))
    # #
    # for i in db.execute(query_total):
    #     print(i)

    #
    # query_photo = User.select(Hotel.id, Hotel.hotel_id)\
    #     .where(User.phone_number == 9251957900) \
    #     .join(Request, on=(Request.user_id == User.phone_number)) \
    #     .join(Hotel, on=(Hotel.request_id == Request.id)) \
    # .where(Request.id == 37) \
    # .join(Landmark, on=(Landmark.hotel_id == Hotel.id))\

    # for i in db.execute(query_photo):
    #     print(i)

    # query_res = User.select(Hotel.id, Hotel.hotel_id, Hotel.name, Hotel.star_rating, Hotel.address, Hotel.price) \
    #     .where(User.phone_number == 9251957900) \
    #     .join(Request, on=(Request.user_id == User.phone_number)) \
    #     .join(Hotel, on=(Hotel.request_id == Request.id)) \
    #     .where(Request.id == 1)
    #
    # for i in db.execute(query_res):
    #     print(i)

if __name__ == '__main__':
    try:
        main()
    except Exception:
        print("Something went wrong...")
        logger.add("logging/error.log",
                   format="{time:YYYY-MM-DD at HH:mm:ss} - {level} - {name} - {message}",
                   level="ERROR")
        logger.exception("Uncontrolled exception occured...")
