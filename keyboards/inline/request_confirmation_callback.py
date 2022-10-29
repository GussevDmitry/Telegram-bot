import json
from loader import bot
from telebot.types import CallbackQuery
from states.user_states import UserStateInfo
from keyboards.inline.place_choice import place_choice
from keyboards.reply.specify_request import specify_request
from database.request_filling import request_filling
from utils.get_API_info import get_info
from utils.location_info_results import location_info_results
from utils.collecting_places_data import collecting_data_places


@bot.callback_query_handler(func=lambda call: call.data in ("confirm_yes", "confirm_no"))
def request_confirmation_callback(call: CallbackQuery) -> None:
    """
    Handling the callback (function "request_confirmation") with user's preferred option.
    If user's choice is positive asking sending the request to API with required parameters.
    If user's choice is negative asking user to specify the request (return to handler "choose_lang").
    :param call: user's choice ("да" or "нет")
    """
    if call.data == "confirm_yes":
        with bot.retrieve_data(call.from_user.id) as data:
            location_info = get_info(url='https://hotels4.p.rapidapi.com/locations/v2/search',
                                     querystring=data['querystring_location_search'])

        location_info_result = location_info_results(location_info=location_info)
        if len(location_info_result.get('entities')) >= 1:
            places_lst = collecting_data_places(location_info_result=location_info_result)
            bot.send_message(call.message.chat.id,
                             "Уточните, пожалуйста, город/район, где ищем:",
                             reply_markup=place_choice(places=places_lst))

            with open(f"parced_data/location_info_result_{data.get('search').get('mode')}.json", 'w',
                      encoding='utf-8') as file:
                json.dump(location_info_result, file, indent=4)

            # Filling the database with request's information
            request_filling(data=data, places=places_lst)

        else:
            bot.send_message(call.message.chat.id, "Извините, по данному городу информации нет. "
                                                   "Давайте уточним запрос.", reply_markup=specify_request())
            bot.set_state(call.from_user.id, UserStateInfo.info_collected)
    else:
        bot.send_message(call.message.chat.id, "Давайте уточним запрос.", reply_markup=specify_request())
        bot.set_state(call.from_user.id, UserStateInfo.info_collected)
