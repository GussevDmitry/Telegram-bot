from database.create_database import db, Hotel


def get_hotels_id() -> set:
    hotel_ids = set()
    query_hotels_ids = Hotel.select(Hotel.hotel_id)
    for i_id in db.execute(query_hotels_ids):
        hotel_ids.add(i_id[0])

    return hotel_ids