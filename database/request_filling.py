from database.create_database import db, User, Request
from datetime import datetime
from typing import Dict, List


def request_filling(data: Dict, places: List):
    dest_id_chosen = data.get('querystring_properties_list').get('destinationId')
    for i_place in places:
        if i_place.get('destinationId') == dest_id_chosen:
            dest_name_chosen = f"{i_place.get('name')}, {i_place.get('description')}"
            break

    if data.get('search').get('mode') == 'bestdeal':
        price_from = f"{data.get('search').get('bestdeal').get('price_range')[0]:,d}"
        price_to = f"{data.get('search').get('bestdeal').get('price_range')[1]:,d}"
        price_range = f"от {price_from} до {price_to}"
        dist_from = data.get('search').get('bestdeal').get('distance_range')[0]
        dist_to = data.get('search').get('bestdeal').get('distance_range')[1]
        dist_range = f"от {dist_from} до {dist_to}"
    else:
        price_range = None
        dist_range = None

    with db:
        query_user_id = User.select(User.phone_number).where(User.phone_number == data.get('phone_number'))
        Request.create(user_id=query_user_id,
                       name=data.get('search').get('mode'),
                       date_time=datetime.now(),
                       lang=data.get('querystring_properties_list').get('locale'),
                       curr=data.get('currency')[3],
                       location=dest_name_chosen,
                       rooms_amount=data.get('rooms_amount'),
                       people_count=data.get('people_amount'),
                       check_in=data.get('querystring_properties_list').get('checkIn'),
                       check_out=data.get('querystring_properties_list').get('checkOut'),
                       hotels_count=data.get('hotels_count'),
                       price_range=price_range,
                       distance_range=dist_range)