import math
# import json
from loguru import logger
from datetime import datetime
from telebot.types import Message
from loader import bot
from states.user_states import UserStateInfo
from exceptions import PriceException, DistanceException
from utils.print_data import print_data
from keyboards.inline.language_choice import language_choice
from keyboards.inline.create_calendar import create_calendar
from keyboards.inline.need_photo_choice import need_photo_choice
from keyboards.inline.change_room_amount import change_room_amount
from keyboards.inline.request_confirmation import request_confirmation


@bot.message_handler(state=UserStateInfo.info_collected, commands=['lowprice', 'highprice', 'bestdeal'])
def choose_lang(message: Message) -> None:
    """
    Asking user to choose preferred language with inline keyboard "language_choice"
    :param message: message from user, one of search mode commands (lowprice, highprice, bestdeal)
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['search'] = {
            'mode': message.text[1:]
        }
        # Logging actions
        logger.debug(f"User {data.get('name')} chooses {data.get('search').get('mode')} mode")

    bot.send_message(message.from_user.id, "Выберете предпочтительный язык поиска.",
                     reply_markup=language_choice())


@bot.message_handler(state=UserStateInfo.search_city)
def choose_rooms_count(message: Message) -> None:
    """
    Asking user to choose the amount of rooms needed
    :param message: message from user with search city
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['querystring_location_search'].update(
            {'query': message.text.strip().lower().title()}
        )
    bot.send_message(message.from_user.id, "Сколько номеров в отеле Вам необходимо?")
    bot.set_state(message.from_user.id, UserStateInfo.rooms_number, message.chat.id)


@bot.message_handler(state=UserStateInfo.rooms_number)
def choose_people_amount(message: Message) -> None:
    """
    Asking user to choose the amount of people in every room
    :param message: message from user with the amount of rooms needed
    """
    if message.text.strip().isdigit():
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['rooms_amount'] = int(message.text.strip())
        bot.send_message(message.from_user.id, "Введите количество взрослых людей в каждом номере через пробел.")
        bot.set_state(message.from_user.id, UserStateInfo.people_amount, message.chat.id)
    else:
        bot.send_message(message.from_user.id, "Количество номеров должно быть целым положительным числом.")


@bot.message_handler(state=UserStateInfo.people_amount)
def choose_year(message: Message) -> None:
    """
    Asking user to choose the year of the trip.
    Asking user if he/she wants to change the amount of rooms needed
    :param message: message from user with the amount of people in every room
    """
    ans = message.text.strip().split()
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        rooms_amount = data['rooms_amount']
    try:
        ans_help = sum(map(lambda elem: int(elem), ans))
        if len(ans) == rooms_amount:
            if len(ans) == 1:
                if int(message.text.strip()) <= 0:
                    raise ValueError
                else:
                    data['querystring_properties_list'].update(
                        {'adults1': message.text.strip()}
                    )
                    bot.set_state(message.from_user.id, UserStateInfo.trip_year)
                    bot.send_message(message.from_user.id, "В каком году планируется Ваша поездка?")
            else:
                for i_ind, i_am in enumerate(ans):
                    if int(i_am) <= 0:
                        raise ValueError
                    else:
                        data['querystring_properties_list'].update(
                            {f'adults{i_ind + 1}': i_am}
                        )
                        bot.set_state(message.from_user.id, UserStateInfo.trip_year)
                bot.send_message(message.from_user.id, "В каком году планируется Ваша поездка?")
        else:
            bot.send_message(message.from_user.id, f"Вы указали количество номеров - {rooms_amount}. "
                                                   f"Хотите указать другое количество номеров?",
                             reply_markup=change_room_amount())

        data['people_amount'] = ans_help
    except ValueError:
        bot.send_message(message.from_user.id, "Количество человек должно быть целым положительным числом.")


@bot.message_handler(state=UserStateInfo.trip_year)
def get_trip_year(message: Message) -> None:
    """
    Asking user to choose the dates of the trip (check-in date) with inline keyboard (calendar) "create_calendar"
    :param message: User's choice of the year of the trip
    """
    if message.text.strip().isdigit():
        year_now = datetime.now().year
        if int(message.text.strip()) > year_now:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['shown_dates'] = (int(message.text.strip()), 1)
            bot.send_message(message.from_user.id, "Выберете дату заезда/выезда.",
                             reply_markup=create_calendar(year=data.get('shown_dates')[0],
                                                          month=data.get('shown_dates')[1]))
        elif int(message.text.strip()) == year_now:
            month_now = datetime.now().month
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['shown_dates'] = (year_now, month_now)
            bot.send_message(message.from_user.id, "Выберете дату заезда/выезда.",
                             reply_markup=create_calendar(year=data.get('shown_dates')[0],
                                                          month=data.get('shown_dates')[1]))
        else:
            bot.send_message(message.from_user.id, f"Значение года не может быть меньше текущего - {year_now}.")
    else:
        bot.send_message(message.from_user.id, "Год не может содержать буквы и символы.")


@bot.message_handler(state=UserStateInfo.hotels_count)
def get_hotels_count(message: Message) -> None:
    """
    Asking the user if he/she wishes to see hotel's photos with inline keyboard "need_photo_choice"
    :param message: the amount of hotels to be shown
    """
    if message.text.strip().isdigit():
        request_count = math.ceil(int(message.text.strip()) / 25)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['querystring_properties_list'].update(
                {'pageNumber': None}
            )
            data['querystring_properties_list'].update(
                {'pageSize': None}
            )
            data['hotels_count'] = int(message.text.strip())
            data['request_count'] = request_count

        # bot.set_state(message.from_user.id, UserStateInfo.hotels_photo_flag, message.chat.id)
        bot.send_message(message.from_user.id, "Показать фотографии отеля?", reply_markup=need_photo_choice())
    else:
        bot.send_message(message.from_user.id, "Количество отелей должно быть целым числом и больше нуля.")


@bot.message_handler(state=UserStateInfo.hotels_photo_count)
def get_hotel_photo(message: Message) -> None:
    """
    Collecting the information about the amount of hotel's photos to be shown
    If the search mode is NOT "bestdeal" confirming the collected information with function "print_data".
    If the search mode is "bestdeal" asking about the range of the hotel's price
    :param message: the amount of hotel's photos to be shown
    """
    if message.text.strip().isdigit():
        photo_count = int(message.text.strip())
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['hotel_photo'].update(
                {
                    'photo_count': photo_count
                }
            )
        if data.get('search').get('mode') in ['lowprice', 'highprice']:
            bot.send_message(message.from_user.id,
                             f"{print_data(data=data)}Верно?",
                             reply_markup=request_confirmation())
            # bot.set_state(message.from_user.id, UserStateInfo.confirm_data, message.chat.id)
        else:
            bot.send_message(message.from_user.id,
                             f"Введите диапазон цен (минимальная цена - максимальная цена "
                             f"в {data.get('currency')[3]}) в формате '1000-2000'.")
            bot.set_state(message.from_user.id, UserStateInfo.price_range, message.chat.id)
    else:
        bot.send_message(message.from_user.id, "Количество фотографий должно быть целым неотрицательным числом.")


@bot.message_handler(state=UserStateInfo.price_range)
def price_range(message: Message) -> None:
    """
    Collecting the information about the range of the hotel's price.
    Asking the user about the range of the distance between the hotel and the city center
    :param message: the range of the hotels' price
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        try:
            ans = message.text.strip().split('-')
            if len(ans) == 2 and (int(ans[0]) <= int(ans[1])):
                temp_res = list(map(lambda elem: int(elem), ans))
                data['search'][f"{data.get('search').get('mode')}"] = {
                    'price_range': temp_res
                }

                bot.send_message(message.from_user.id, f"Введите диапазон расстояния до центра города в километрах "
                                                       f"(минимальное - максимальное) в формате '0.1-0.2' или '1-2'.")
                bot.set_state(message.from_user.id, UserStateInfo.distance_range, message.chat.id)
            else:
                raise PriceException
        except PriceException:
            bot.send_message(message.from_user.id, f"Введите диапазон цен (минимальная цена - максимальная цена "
                                                   f"в {data.get('currency')[3]}) в формате '1000-2000'.")
        except ValueError:
            bot.send_message(message.from_user.id, f"Введите диапазон цен (минимальная цена - максимальная цена "
                                                   f"в {data.get('currency')[3]}) в формате '1000-2000'.")


@bot.message_handler(state=UserStateInfo.distance_range)
def distance_range(message: Message) -> None:
    """
    Collecting the information about the range of the range of the distance between the hotel and the city center.
    Confirming the collected information with function "print_data"
    :param message: the range of the distance between the hotel and the city center
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        try:
            temp_res = []
            ans = message.text.strip().split('-')
            if len(ans) == 2:
                for i_elem in ans:
                    if i_elem.isdigit():
                        temp_res.append(int(i_elem))
                    elif '.' in i_elem:
                        temp_res.append(float(i_elem))
                    elif ',' in i_elem:
                        temp_res.append(float(i_elem.replace(',', '.')))
                    else:
                        raise DistanceException
                if temp_res[0] <= temp_res[1]:
                    data['search'][f"{data.get('search').get('mode')}"].update(
                        {
                            'distance_range': temp_res
                        }
                    )

                    temp_text = f"Диапазон цен от {data.get('search').get('bestdeal').get('price_range')[0]:,d} до " \
                                f"{data.get('search').get('bestdeal').get('price_range')[1]:,d} " \
                                f"{data.get('currency')[0]}\n" \
                                f"Диапазон расстояния до центра от " \
                                f"{data.get('search').get('bestdeal').get('distance_range')[0]} до " \
                                f"{data.get('search').get('bestdeal').get('distance_range')[1]} км\n"
                    bot.send_message(message.from_user.id,
                                     f"{print_data(data=data)}{temp_text}Верно?",
                                     reply_markup=request_confirmation())
                    # bot.set_state(message.from_user.id, UserStateInfo.confirm_data, message.chat.id)
                else:
                    raise DistanceException
            else:
                raise DistanceException
        except DistanceException:
            bot.send_message(message.from_user.id, f"Введите диапазон расстояния до центра города в километрах "
                                                   f"(минимальное - максимальное) в формате '0.1-0.2' или '1-2'.")
        except ValueError:
            bot.send_message(message.from_user.id, f"Введите диапазон расстояния до центра города в километрах "
                                                   f"(минимальное - максимальное) в формате '0.1-0.2' или '1-2'.")


# @bot.message_handler(state=UserStateInfo.confirm_data)
# def confirm_data(message: Message) -> None:
#     """
#     Collecting the user's confirmation (or non-confirmation) the information about user's request.
#     Conducting the API request.
#     Specifying the city/neighbourhood to find hotels with with inline keyboard "place_choice"
#     :param message: user's confirmation (or non-confirmation) the information about user's request
#     """
    # if message.text.lower() in ['да', 'д', 'ага', 'yes', 'y']:
    #     with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
    #         location_info = get_info(url='https://hotels4.p.rapidapi.com/locations/v2/search',
    #                                  querystring=data['querystring_location_search'])

            # """Запись в текстовый файл для работы через файлы"""
            # with open(f"parced_data/location_info_result_{data.get('search').get('mode')}.txt", 'w',
            #           encoding='utf-8') as file:
            #     file.write(location_info)

        # location_info_result = location_info_results(location_info=location_info)
        # if len(location_info_result.get('entities')) >= 1:
        #     places_lst = collecting_data_places(location_info_result=location_info_result)
        #     bot.send_message(message.from_user.id,
        #                      "Уточните, пожалуйста, город/район, где ищем:",
        #                      reply_markup=place_choice(places=places_lst))
        #     # with open(f"parced_data/location_info_result_{data.get('search').get('mode')}.json", 'w',
        #     #           encoding='utf-8') as file:
        #     #     json.dump(location_info_result, file, indent=4)
        #
        #     # Filling the database with request's information
        #     with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        #         request_filling(data=data, places=places_lst)
        #
        # else:
        #     bot.send_message(message.from_user.id, "Извините, по данному городу информации нет. "
        #                                            "Давайте уточним запрос.", reply_markup=specify_request())
        #     bot.set_state(message.from_user.id, UserStateInfo.info_collected)

    # else:
    #     bot.send_message(message.from_user.id, "Давайте уточним запрос.", reply_markup=specify_request())
    #     bot.set_state(message.from_user.id, UserStateInfo.info_collected)
