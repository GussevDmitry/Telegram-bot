from database.create_database import db, Request, Hotel
from peewee import fn


def hotel_filling(data, i_index):
    with db:
        query_request_id = Request.select(fn.MAX(Request.id))
        Hotel.create(request_id=query_request_id,
                     hotel_id=data.get('search').get(f"{data.get('search').get('mode')}")
                     .get('results')[i_index].get('id'),
                     name=data.get('search').get(f"{data.get('search').get('mode')}")
                     .get('results')[i_index].get('name'),
                     star_rating=data.get('search').get(f"{data.get('search').get('mode')}")
                     .get('results')[i_index].get('starRating'),
                     address=data.get('search').get(f"{data.get('search').get('mode')}")
                     .get('results')[i_index].get('address'),
                     price=data.get('search').get(f"{data.get('search').get('mode')}")
                     .get('results')[i_index].get('price'))