def get_guest_reviews(i_hotel):
    try:
        return f"{i_hotel.get('guestReviews').get('unformattedRating')}/{i_hotel.get('guestReviews').get('scale')} " \
               f"на основании {i_hotel.get('guestReviews').get('total')} оценок!"
    except AttributeError:
        return "Данному отелю пользователи еще не поставили оценку"