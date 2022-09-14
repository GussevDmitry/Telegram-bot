from database.create_database import db, Hotel, Photo
from peewee import fn

# def hotel_photo_filling(data, temp_dict, i_index):
#     for i_url in temp_dict:
#         with db:
#             query_hotel_id = Hotel.select(Hotel.hotel_id) \
#                 .where(Hotel.hotel_id == data.get('search').get(f"{data.get('search').get('mode')}")
#                        .get('results')[i_index].get('id'))
#             Photo.create(hotel_id=query_hotel_id, photo_url=i_url)


def hotel_photo_filling(temp_dict):
    for i_url in temp_dict:
        with db:
            query_hotel_id = Hotel.select(fn.MAX(Hotel.id))
            Photo.create(hotel_id=query_hotel_id, photo_url=i_url)