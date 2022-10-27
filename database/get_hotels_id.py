from database.create_database import db, Hotel
from typing import List


def get_hotels_id() -> List:
    """
    Collecting hotels' identification numbers already containing in database (table Hotel)
    :return: the list with hotels' identification numbers already containing in database (table Hotel)
    """
    hotel_ids = list()
    query_hotels_ids = Hotel.select(Hotel.hotel_id)
    for i_id in db.execute(query_hotels_ids):
        hotel_ids.append(i_id[0])

    return hotel_ids
