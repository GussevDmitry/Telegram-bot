import json
from utils.get_correct_price import get_correct_price
from utils.get_API_info import get_info
from database.hotel_filling import hotel_filling
from database.hotel_photo_filling import hotel_photo_filling
from typing import Dict, List


def get_hotel_photos(i_index, i_result: Dict, data) -> List:
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


def check_the_landmark(i_result: Dict) -> List:
    temp_lst_lm = list()
    for j_item in i_result.get('landmarks'):
        if 'airport' in j_item.get('label').lower():
            continue
        else:
            distance = float(j_item.get('distance').replace(" miles", "").replace("mile", "").replace(",", "."))
            distance *= 1.6093
            temp_lst_lm.append(
                f"{j_item.get('label')} - "
                f"{round(distance, 1)} км"
            )
    return temp_lst_lm


def collect_data_to_show(data, results: List, flag: bool) -> None:
    for i_index, i_item in enumerate(results):
        # Getting correct price from API
        i_item_price = get_correct_price(i_item)
        # Getting correct list of landmarks from API
        temp_lst_lm = check_the_landmark(i_result=i_item)

        data['search'][f"{data.get('search').get('mode')}"]['results'].append(
            {
                'id': i_item.get('id'),
                'name': i_item.get('name'),
                'starRating': int(i_item.get('starRating')),
                'guestRating': f"{i_item.get('guestReviews').get('rating')}/"
                               f"{i_item.get('guestReviews').get('scale')} на основании "
                               f"{i_item.get('guestReviews').get('total')} оценок!",
                'address': f"{i_item.get('address').get('postalCode')}, "
                           f"{i_item.get('address').get('locality')}, "
                           f"{i_item.get('address').get('streetAddress')}".replace('None, ', '', 3).strip(),
                'landmarks': temp_lst_lm,
                'price_per_night': f"{int(i_item.get('ratePlan').get('price').get('exactCurrent')):,d}",
                'price': f"{i_item_price}",
                'hotel_photos': ''
            }
        )
        # Filling the database with hotel's information
        hotel_filling(data=data, i_index=i_index)

        # Check, if user wishes to see hotel's photos
        if flag:
            temp_lst_photos = get_hotel_photos(i_index=i_index, i_result=i_item, data=data)
            # Filling the database with hotel's photos
            hotel_photo_filling(temp_dict=temp_lst_photos)

    # Filter the results
    data['search'][f"{data.get('search').get('mode')}"]['results'] = \
        sorted(data['search'][f"{data.get('search').get('mode')}"]['results'],
               key=lambda elem: int(elem['price'].split()[0].replace(',', '')))

    data['search'][f"{data.get('search').get('mode')}"]['results'] = \
        sorted(data['search'][f"{data.get('search').get('mode')}"]['results'],
               key=lambda elem: elem['landmarks'][0].split(' - '))
