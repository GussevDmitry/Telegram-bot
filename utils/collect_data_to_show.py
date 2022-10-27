import json
from utils.get_correct_price import get_correct_price
from utils.get_API_info import get_info
from database.hotel_filling import hotel_filling
from database.hotel_photo_filling import hotel_photo_filling
from typing import Dict, List
from utils.misc.get_guest_reviews import get_guest_reviews


def get_hotel_photos(i_index: int, i_result: Dict, data: Dict) -> List:
    """
    Sending the request to API with required parameters to collect hotel's photo urls.
    Filling the list with hotel's photos urls
    :param i_index: serial number (index) of the hotel storing in memory storage
    :param i_result: hotel with collected information
    :param data: memory storage
    :return: list with hotel's photos urls
    """
    temp_lst_photos = list()
    properties_hotel_photos_lp = get_info(url='https://hotels4.p.rapidapi.com/properties/get-hotel-photos',
                                          querystring={"id": f"{i_result.get('id')}"})

    if properties_hotel_photos_lp != '':
        with open(f"parced_data/properties_hotel_photos_{data.get('search').get('mode')}.txt", 'w',
                  encoding='utf-8') as file:
            file.write(properties_hotel_photos_lp)

        with open(f"parced_data/properties_hotel_photos_{data.get('search').get('mode')}.txt", 'r',
                  encoding='utf-8') as file:
            data_temp = file.read()
            data_json = json.loads(f"{data_temp}")

        if len(data_json.get('hotelImages')) < data.get('hotel_photo').get('photo_count'):
            for i_photo in data_json.get('hotelImages'):
                i_url = i_photo.get('baseUrl').replace('_{size}', '')
                temp_lst_photos.append(i_url)
        else:
            for i_photo in data_json.get('hotelImages')[:data.get('hotel_photo').get('photo_count')]:
                i_url = i_photo.get('baseUrl').replace('_{size}', '')
                temp_lst_photos.append(i_url)
        data['search'][f"{data.get('search').get('mode')}"]['results'][i_index].update(
            {
                'hotel_photos': temp_lst_photos
            }
        )
    else:
        temp_lst_photos = ['У выбранного Вами отеля нет фотографий']
        data['search'][f"{data.get('search').get('mode')}"]['results'][i_index].update(
            {
                'hotel_photos': temp_lst_photos
            }
        )
    return temp_lst_photos


def check_the_landmark(i_result: Dict, data: Dict) -> List:
    """
    Checking if user needs to get the distance to landmark in miles and converting the information in string
    :param i_result: hotel with collected information
    :param data: memory storage
    :return: the list with strings containing the landmarks and the distance to hotel
    """
    temp_lst_lm = list()
    for j_item in i_result.get('landmarks'):
        distance = float(j_item.get('distance').split()[0].replace(",", "."))
        if data.get("language") == "английском":
            distance *= 1.6093
        temp_lst_lm.append(
            f"{j_item.get('label')} - "
            f"{round(distance, 1)} км"
        )
    return temp_lst_lm


def collect_data_to_show(data: Dict, results: List, flag: bool) -> None:
    """
    Preparing collected information about hotels to show to user
    :param data: memory storage
    :param results: the list with appropriate hotels which should be shown to user
    :param flag: flag which marks if user wants to overlook hotel's photos
    """
    for i_index, i_item in enumerate(results):
        i_item_price = get_correct_price(i_item, data)

        # Getting correct list of landmarks from API
        temp_lst_lm = check_the_landmark(i_result=i_item, data=data)
        guest_rating = get_guest_reviews(i_hotel=i_item)

        data['search'][f"{data.get('search').get('mode')}"]['results'].append(
            {
                'id': i_item.get('id'),
                'name': i_item.get('name'),
                'starRating': int(i_item.get('starRating')),
                'guestRating': guest_rating,
                'address': f"{i_item.get('address').get('postalCode')}, "
                           f"{i_item.get('address').get('locality')}, "
                           f"{i_item.get('address').get('streetAddress')}".replace('None,',
                                                                                   '', 3).replace(', None', '', 3),
                'landmarks': temp_lst_lm,
                'price_per_night': int(i_item.get('ratePlan').get('price').get('exactCurrent')),
                'price': i_item_price,
                'hotel_photos': ''
            }
        )
        # Filling the database with hotel's information
        hotel_filling(data=data, i_index=i_index)

        # Check, if user wishes to overlook hotels' photos
        if flag:
            temp_lst_photos = get_hotel_photos(i_index=i_index, i_result=i_item, data=data)

            # Filling the database with hotel's photos
            hotel_id = data.get('search').get(f"{data.get('search').get('mode')}").get('results')[i_index].get('id')
            hotel_photo_filling(temp_lst=temp_lst_photos, hotel_id=hotel_id)

    # Filter the results
    data['search'][f"{data.get('search').get('mode')}"]['results'] = \
        sorted(data['search'][f"{data.get('search').get('mode')}"]['results'],
               key=lambda elem: elem['price'])
