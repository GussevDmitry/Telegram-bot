from database.create_database import Hotel, Photo
from database.get_hotels_id import get_hotels_id
from typing import List


def hotel_photo_filling(temp_lst: List, hotel_id: int) -> None:
    """
    Filling the database (table Photo) with hotel's photos urls
    :param temp_lst: list with hotel's photos urls
    :param hotel_id: the hotel's identification number
    """
    hotel_ids = get_hotels_id()
    count_id = hotel_ids.count(hotel_id)
    if count_id == 1:
        query_hotel_id = Hotel.select(Hotel.hotel_id) \
            .where(Hotel.hotel_id == hotel_id)
        for i_url in temp_lst:
            Photo.create(hotel_id=query_hotel_id, photo_url=i_url)
