import json
from utils.get_correct_price import get_correct_price
from utils.get_API_info import get_info
from database.hotel_filling import hotel_filling
from database.hotel_photo_filling import hotel_photo_filling


def collect_data_to_show(data, results, flag):
    if results == []:
        return
    else:
        for i_index, i_item in enumerate(results):
            temp_dict = []
            temp_dict_lm = []

            # try:
            i_item_price = get_correct_price(i_item)

            for j_item in i_item.get('landmarks'):
                if 'Airport' in j_item.get('label') or 'airport' in j_item.get('label'):
                    continue
                else:
                    temp_dict_lm.append(
                        f"{j_item.get('label')} - "
                        f"{j_item.get('distance').replace('miles', 'миль(и)').replace('mile', 'миля')}"
                    )

            data['search'][f"{data.get('search').get('mode')}"]['results'].append(
                {
                    'id' : i_item.get('id'),
                    'name' : i_item.get('name'),
                    'starRating' : i_item.get('starRating'),
                    'address' : f"{i_item.get('address').get('postalCode')}, "
                                f"{i_item.get('address').get('locality')}, "
                                f"{i_item.get('address').get('streetAddress')}".replace('None', '', 3).strip(),
                    'landmarks' : temp_dict_lm,
                    'price' : f"{i_item_price}",
                    'hotel_photos' : ''
                }
            )

            hotel_filling(data=data, i_index=i_index)

            if flag:
                # Для работы с API
                properties_hotel_photos_lp = get_info(url='https://hotels4.p.rapidapi.com/properties/get-hotel-photos',
                                                   querystring={"id": f"{i_item.get('id')}"})


                # Только для работы с файлом
                # with open(f"parced_data/properties_hotel_photos_{data.get('search').get('mode')}.txt", 'r') as file:
                #     properties_hotel_photos_lp = file.read()
                #     data_json = json.loads(f"{properties_hotel_photos_lp}")

                #

                if properties_hotel_photos_lp != '':
                    # Для работы с API
                    with open(f"parced_data/properties_hotel_photos_{data.get('search').get('mode')}.txt", 'w') as file:
                        file.write(properties_hotel_photos_lp)

                    with open(f"parced_data/properties_hotel_photos_{data.get('search').get('mode')}.txt", 'r') as file:
                        data_temp = file.read()
                        data_json = json.loads(f"{data_temp}")
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
                    temp_dict = ['У выбранного Вами отеля нет фотографий']
                    data['search'][f"{data.get('search').get('mode')}"]['results'][i_index].update(
                        {
                            'hotel_photos': temp_dict
                        }
                    )

                # hotel_photo_filling(data=data, temp_dict=temp_dict, i_index=i_index)
                hotel_photo_filling(temp_dict=temp_dict)


        data['search'][f"{data.get('search').get('mode')}"]['results'] = \
            sorted(data['search'][f"{data.get('search').get('mode')}"]['results'],
                   key=lambda elem: int(elem['price'].split()[0].replace(',', '')))

        data['search'][f"{data.get('search').get('mode')}"]['results'] = \
            sorted(data['search'][f"{data.get('search').get('mode')}"]['results'],
                   key=lambda elem: elem['landmarks'][0].split(' - '))

            # except IndexError:
            #     pass