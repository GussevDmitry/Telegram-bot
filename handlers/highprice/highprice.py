import re
import json
from loader import bot
from states.user_states import UserStateInfo
from telebot.types import Message, CallbackQuery
from keyboards.inline.place_choice import place_choice
from keyboards.reply.start_search import start_search
from utils.get_API_info import get_info
from utils.collecting_places_data import collecting_data_places
from utils.collect_data_to_show import collect_data_to_show

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

@bot.message_handler(state=UserStateInfo.highprice)
def highprice_presearch(message: Message) -> None:
    # Через запрос к API
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        location_info_hp = get_info(url='https://hotels4.p.rapidapi.com/locations/v2/search',
                        querystring=data['querystring_location_search'])
    pattern = r'(?<="CITY_GROUP",).+?[\]]'
    find = re.search(pattern, location_info_hp)

    if find:
        location_info_result_hp = json.loads(f"{{{find[0]}}}")
        bot.send_message(message.from_user.id, "Уточните, пожалуйста, где ищем:",
                        reply_markup=place_choice(places=collecting_data_places(location_info_result_hp)))

        """Запись в json-файл"""
        with open('parced_data/location_info_result_hp.json', 'w') as file:
            json.dump(location_info_result_hp, file, indent=4)
    else:
        bot.send_message(message.from_user.id, "Извините, по данному городу информации нет.")

    # Только для работы с файлом
    # with open('parced_data/location_info_result_hp.json', 'r') as file:
    #     location_info_result_hp = json.load(file)
    # bot.send_message(message.from_user.id, "Уточните, пожалуйста, где ищем:",
    #                  reply_markup=place_choice(places=collecting_data_places(location_info_result_hp)))


@bot.callback_query_handler(func=lambda call: call.data.isdigit())
def choose_place(call: CallbackQuery):
    with bot.retrieve_data(call.from_user.id) as data:
        data['querystring_properties_list'].update(
            {'destinationId': str(call.data)}
        )
        data['querystring_properties_list'].update(
            {'sortOrder': 'PRICE_HIGHEST_FIRST'}
        )
        data['search'].update(
            {
                f"{data.get('search').get('mode')}": {
                    'header': call.data
                }
            }
        )
        data['search'][f"{data.get('search').get('mode')}"].update(
            {
                'results': []
            }
        )

    bot.send_message(call.from_user.id, "Нажмите на кнопку для начала поиска.", reply_markup=start_search())
    bot.register_next_step_handler(call.message, highprice_search)


def highprice_search(message: Message) -> None:
    # Через запрос к API
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        properties_info_hp = get_info(url='https://hotels4.p.rapidapi.com/properties/list',
                        querystring=data['querystring_properties_list'])
        flag = data.get('hotel_photo').get('need_photo')

    with open('parced_data/properties_info_hp.txt', 'w', encoding='utf-8') as file:
        file.write(properties_info_hp)

    with open('parced_data/properties_info_hp.txt', 'r') as file:
        temp_data = file.read()
    result = json.loads(f"{temp_data}")

    # result = re.search(r'(?<="searchResults":).+', properties_info)
    # print(result.group(0))
    # result = json.loads(f"{{{properties_info}}}")

    results = result.get('data').get('body').get('searchResults').get('results')
    #

    # Только для работы с файлом
    # with open('parced_data/properties_info_hp.txt', 'r') as file:
    #     temp_data = file.read()
    # result = json.loads(f"{temp_data}")
    # results = result.get('data').get('body').get('searchResults').get('results')
    # with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
    #     flag = data.get('hotel_photo').get('need_photo')

    """Запись в json-файл"""
    with open('parced_data/properties_info_hp.json', 'w') as file:
        json.dump(results, file, indent=4)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        collect_data_to_show(data, results, flag)

        for i_index, i_data in enumerate(data['search'][f"{data.get('search').get('mode')}"]['results']):
            photos_text = '\n'.join(data['search'][f"{data.get('search').get('mode')}"]['results'][i_index].get('hotel_photos'))
            text = f"\U0001F3E8 Отель {i_data.get('name')}\n" \
                   f"Адрес - {i_data.get('address')}\n" \
                   f"Расстояние до {i_data.get('landmark_1')}\n" \
                   f"Расстояние до {i_data.get('landmark_2')}\n" \
                   f"Стоимость итого: {i_data.get('price')} за {data.get('rooms_amount')} " \
                   f"комнаты для {data.get('people_amount')} гостей\n" \
                   f"Фотографии:\n{photos_text}"
            bot.send_message(message.from_user.id, text)