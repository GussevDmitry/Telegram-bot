from typing import Dict


def get_guest_reviews(i_hotel: Dict) -> str:
    """
    Collecting the rating, the scale and the amount of reviews in the string
    :param i_hotel: hotel with collected information
    :return: the rating, the scale and the amount of reviews in the string
    """
    try:
        return f"{i_hotel.get('guestReviews').get('unformattedRating')}/{i_hotel.get('guestReviews').get('scale')} " \
               f"на основании {i_hotel.get('guestReviews').get('total')} оценок!"
    except AttributeError:
        return "Данному отелю пользователи еще не поставили оценку"
