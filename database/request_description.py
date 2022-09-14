from database.create_database import User, Request, Hotel


def request_description(data):
    query_desc = User.select(Request.id, Request.name, Request.location, Request.rooms_amount, Request.people_count,
                             Request.check_in, Request.check_out) \
            .where(User.phone_number == data.get('phone_number'))\
            .join(Request, on=(Request.user_id == User.phone_number))

    return query_desc


def request_results(call, data):
    query_res = User.select(Hotel.id, Hotel.hotel_id, Hotel.name, Hotel.star_rating, Hotel.address, Hotel.price) \
            .where(User.phone_number == data.get('phone_number'))\
            .join(Request, on=(Request.user_id == User.phone_number)) \
            .join(Hotel, on=(Hotel.request_id == Request.id)) \
            .where(Request.id == int(call.data[2:]))

    return query_res
