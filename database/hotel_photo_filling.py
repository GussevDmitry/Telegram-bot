from database.create_database import Hotel, Photo
from peewee import fn
from database.get_hotels_id import get_hotels_id


def hotel_photo_filling(temp_dict, hotel_id):
    hotel_ids = get_hotels_id()
    if hotel_id not in hotel_ids:
        for i_url in temp_dict:
            # query_hotel_id = Hotel.select(fn.MAX(Hotel.id))
            Photo.create(hotel_id=hotel_id, photo_url=i_url)
