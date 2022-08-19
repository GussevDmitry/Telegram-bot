import re
import json
from loader import bot
from states.user_states import UserStateInfo
from telebot.types import Message
from keyboards.inline.place_choice import place_choice
from utils.get_API_info import get_info
from utils.collect_data_to_show import collect_data_to_show
from utils.properties_info_results import properties_info_results


# data = {
#     'search' : {
#         'mode': None,
#         'lowprice': {
#             'header': 'Midtown, New York, New York, United States of America',
#             'results' : [
#                 {
#                     'id' : None,
#                     'name' : 'Club Quarters Hotel, Grand Central',
#                     'starRating' : 4.0,
#                     'address' : f"address",
#                     'landmark' : f"landmarks",
#                     'price' : "fullyBundledPricePerStay"
#                 }
#             ]
#         },
#         'highprice' : {
#
#         },
#         'destdeal' : {
#
#         }
#     },
#     'rooms_amount': 0,
#     'people_amount': 0
#     'days_count': 0,
#     'hotels_count': 0,
#     'hotel_photo': {
#         'need_photo': False,
#         'photo_count': 0
#     },
#     'querystring_location_search': {
#         'locale': None,
#         'currency': None,
#         'query': None
#     },
#     'querystring_properties_list': {
#             'destinationId': None,
#             'pageNumber': None,
#             'pageSize': None,
#             'checkIn': None,
#             'checkOut': None,
#             'adults1': None,
#             'adults2': None,
#             'sortOrder': None,
#             'locale': None,
#             'currency': None
#         }
# }


def highprice_search(message: Message) -> None:
    # Через запрос к API
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        properties_info_hp = get_info(url='https://hotels4.p.rapidapi.com/properties/list',
                        querystring=data['querystring_properties_list'])
        flag = data.get('hotel_photo').get('need_photo')

        with open(f'parced_data/properties_info_{data.get("search").get("mode")}.txt', 'w', encoding='utf-8') as file:
            file.write(properties_info_hp)

    # result = re.search(r'(?<="searchResults":).+', properties_info)
    # print(result.group(0))
    # result = json.loads(f"{{{properties_info}}}")

        results = properties_info_results(data=data)
    #

    # Только для работы с файлом
    # with open(f"parced_data/properties_info_{data.get('search').get('mode')}.txt", 'r') as file:
    #     temp_data = file.read()
    # result = json.loads(f"{temp_data}")
    # results = result.get('data').get('body').get('searchResults').get('results')
    # with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
    #     flag = data.get('hotel_photo').get('need_photo')

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        collect_data_to_show(data, results, flag)

        for i_index, i_data in enumerate(data['search'][f"{data.get('search').get('mode')}"]['results']):
            photos_text = '\n'.join(data['search'][f"{data.get('search').get('mode')}"]['results'][i_index].get('hotel_photos'))
            lm_text = ', '.join(i_data.get('landmarks'))
            text = f"\U0001F3E8 Отель {i_data.get('name')}\n" \
                   f"Адрес - {i_data.get('address')}\n" \
                   f"Расстояние до {lm_text}\n" \
                   f"Стоимость итого: {i_data.get('price')} за {data.get('rooms_amount')} " \
                   f"комнаты для {data.get('people_amount')} гостей\n" \
                   f"Фотографии:\n{photos_text}"
            bot.send_message(message.from_user.id, text)
        print(data)
    bot.set_state(message.from_user.id, UserStateInfo.info_collected, message.chat.id)