import re
import json
import os
from loader import bot
from states.user_states import UserStateInfo
from telebot.types import Message
from keyboards.inline.place_choice import place_choice
from utils.get_API_info import get_info
from utils.collecting_places_data import collecting_data_places

# data = {
#     'dates_to': None,
#     'dates_from': None,
#     'days_count': 0,
#     'hotels_count': 0,
#     'hotel_photo': {
#         'need_photo': False,
#         'photo_count': 0
#     },
#     'querystring': {
#         'locale': None,
#         'currency': None,
#         'query': None
#     }
# }


@bot.message_handler(state=UserStateInfo.lowprice)
def lowprice_search(message: Message) -> None:

    # with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
    #     location_info = get_info(url='https://hotels4.p.rapidapi.com/locations/v2/search', querystring=data['querystring'])
    # # \U0001F44D\n большой палец вверх
    # pattern = r'(?<="CITY_GROUP",).+?[\]]'
    # find = re.search(pattern, location_info)

    with open(os.path.abspath(os.path.join('test.txt')), 'r') as file:
        temp_data = file.read()

    pattern = r'(?<="CITY_GROUP",).+?[\]]'
    find = re.search(pattern, temp_data)
    if find:
        location_info_result = json.loads(f"{{{find[0]}}}")
        bot.send_message(message.from_user.id, "Уточните, пожалуйста, где ищем:",
                        reply_markup=place_choice(places=collecting_data_places(location_info_result)))
    else:
        bot.send_message(message.from_user.id, "Извините, по данному городу информации нет.")


