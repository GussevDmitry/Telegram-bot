import json
from utils.get_correct_price import get_correct_price

def collect_data_to_show(data, results, flag):
    for i_index, i_item in enumerate(results):
        temp_dict = []

        # try:
        i_item_price = get_correct_price(i_item)
        data['search'][f"{data.get('search').get('mode')}"]['results'].append(
            {
                'id' : i_item.get('id'),
                'name' : i_item.get('name'),
                'starRating' : i_item.get('starRating'),
                'address' : f"{i_item.get('address').get('postalCode')}, "
                            f"{i_item.get('address').get('locality')}, "
                            f"{i_item.get('address').get('streetAddress')}",
                'landmark_1' : f"{i_item.get('landmarks')[0].get('label')} - "
                             f"{i_item.get('landmarks')[0].get('distance').replace('miles', 'миль(и)')}",
                'landmark_2' : f"{i_item.get('landmarks')[1].get('label')} - "
                             f"{i_item.get('landmarks')[1].get('distance').replace('miles', 'миль(и)')}",
                'price' : f"{i_item_price}",
                'hotel_photos' : ''
            }
        )

        if flag:
            # Для работы с API
            # properties_hotel_photos_lp = get_info(url='https://hotels4.p.rapidapi.com/properties/get-hotel-photos',
            #                                    querystring={"id": f"{i_item.get('id')}"})


            # Только для работы с файлом
            with open('parced_data/properties_hotel_photos_lp.txt', 'r') as file:
                properties_hotel_photos_lp = file.read()
                data_json = json.loads(f"{properties_hotel_photos_lp}")

            #

            if properties_hotel_photos_lp != '':
                # Для работы с API
                # with open('properties_hotel_photos_lp.txt', 'w') as file:
                #     file.write(properties_hotel_photos_lp)
                #
                # with open('properties_hotel_photos_lp.txt', 'r') as file:
                #     data_temp = file.read()
                # data_json = json.loads(f"{data_temp}")
                #

                if len(data_json.get('hotelImages')) < data.get('hotel_photo').get('photo_count'):
                    for i_photo in data_json.get('hotelImages'):
                        i_url = i_photo.get('baseUrl').replace('_{size}', '')
                        temp_dict.append(i_url)
                else:
                    for i_photo in data_json.get('hotelImages')[:data.get('hotel_photo').get('photo_count')]:
                        i_url = i_photo.get('baseUrl').replace('_{size}', '')
                        temp_dict.append(i_url)
                data['search'][f"{data.get('search').get('mode')}"]['results'][i_index].update(
                    {
                        'hotel_photos': temp_dict
                    }
                )
            else:
                temp_dict = ['Нет', 'фотографий',  'отеля']
                data['search'][f"{data.get('search').get('mode')}"]['results'][i_index].update(
                    {
                        'hotel_photos': temp_dict
                    }
                )

        # except IndexError:
        #     pass