from database.create_database import db, Request, Hotel, Landmark
from database.get_hotels_id import get_hotels_id
from peewee import fn
from typing import Dict


def hotel_filling(data: Dict, i_index: int) -> None:
    with db:
        query_request_id = Request.select(fn.MAX(Request.id))
        guest_rating_str = data.get('search').get(f"{data.get('search').get('mode')}").get('results')[i_index].get('guestRating')
        if guest_rating_str.startswith('Данному'):
            guest_rating = 0.0
        else:
            guest_rating = float(guest_rating_str[:guest_rating_str.find('/')])
        hotel_id = data.get('search').get(f"{data.get('search').get('mode')}").get('results')[i_index].get('id')
        Hotel.create(request_id=query_request_id,
                     hotel_id=hotel_id,
                     name=data.get('search').get(f"{data.get('search').get('mode')}")
                     .get('results')[i_index].get('name'),
                     star_rating=data.get('search').get(f"{data.get('search').get('mode')}")
                     .get('results')[i_index].get('starRating'),
                     guest_rating=guest_rating,
                     address=data.get('search').get(f"{data.get('search').get('mode')}")
                     .get('results')[i_index].get('address'),
                     one_night_price=data.get('search').get(f"{data.get('search').get('mode')}")
                     .get('results')[i_index].get('price_per_night'),
                      price=data.get('search').get(f"{data.get('search').get('mode')}")
                     .get('results')[i_index].get('price'))

        hotel_lm_filling(data=data, i_index=i_index, hotel_id=hotel_id)

def hotel_lm_filling(data: Dict, i_index: int, hotel_id) -> None:
    hotel_ids = get_hotels_id()
    if hotel_id not in hotel_ids:
        # query_hotel_id = Hotel.select(fn.MAX(Hotel.id))
        for i_lm in data.get('search').get(f"{data.get('search').get('mode')}").get('results')[i_index].get('landmarks'):
            label = i_lm.split(' - ')[0]
            distance = float(i_lm.split(' - ')[1].split()[0])
            Landmark.create(hotel_id=hotel_id,
                            lm_name=label,
                            lm_distance=distance)
