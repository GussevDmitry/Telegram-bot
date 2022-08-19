import math
import json
import re
from states.user_states import UserStateInfo
from loader import bot
from telebot.types import Message
from datetime import datetime
from exceptions import HotelPhotoError, PriceException, DistanceException
from utils.get_API_info import get_info
from utils.collecting_places_data import collecting_data_places
from keyboards.inline.language_choice import language_choice
from keyboards.inline.place_choice import place_choice
from utils.print_data import print_data
from utils.collecting_lm_ids import collecting_lm_ids
from utils.location_info_results import location_info_results


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


@bot.message_handler(state=UserStateInfo.info_collected, commands=['lowprice', 'highprice', 'bestdeal'])
def choose_lang(message: Message) -> None:
    # if UserStateInfo is UserStateInfo.info_collected:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['search'] = {
            'mode': message.text[1:]
        }
    bot.send_message(message.from_user.id, "Выберете предпочтительный язык поиска.",
                     reply_markup=language_choice())
    bot.set_state(message.from_user.id, UserStateInfo.search_city, message.chat.id)
    # else:
    #     bot.send_message(message.from_user.id, "Сначала неоходимо пройти регистрацию. Для этого наберите команду /survey")


@bot.message_handler(states=UserStateInfo.search_city)
def choose_rooms_count(message: Message) -> None:
    bot.set_state(message.from_user.id, UserStateInfo.rooms_number, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['querystring_location_search'].update(
            {'query': message.text.strip().lower().title()}
        )
    bot.send_message(message.from_user.id, "Сколько номеров в отеле Вам необходимо?")

@bot.message_handler(state=UserStateInfo.rooms_number)
def choose_people_amount(message: Message) -> None:
    try:
        if int(message.text.strip()) <= 0:
            raise ValueError
        else:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['rooms_amount'] = int(message.text.strip())
            bot.send_message(message.from_user.id, "Введите количество взрослых людей в каждом номере через пробел.")
            bot.set_state(message.from_user.id, UserStateInfo.people_amount, message.chat.id)
    except ValueError:
        bot.send_message(message.from_user.id, "Количество номеров должно быть целым положительным числом.")


@bot.message_handler(state=UserStateInfo.people_amount)
def choose_dates(message: Message) -> None:
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
                    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                        data['querystring_properties_list'].update(
                            {'adults1': message.text.strip()}
                        )
                    bot.set_state(message.from_user.id, UserStateInfo.dates, message.chat.id)
                bot.send_message(message.from_user.id,
                                 "Запомнил. Укажите даты заезда и выезда (день-месяц-год) в формате 'дд.мм.гггг-дд.мм.гггг'")
            else:
                for i_ind, i_am in enumerate(ans):
                    if int(i_am) <= 0:
                        raise ValueError
                    else:
                        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                            data['querystring_properties_list'].update(
                                {f'adults{i_ind + 1}': i_am}
                            )
                        bot.set_state(message.from_user.id, UserStateInfo.dates, message.chat.id)
                bot.send_message(message.from_user.id,
                            "Запомнил. Укажите даты заезда и выезда (день-месяц-год) в формате 'дд.мм.гггг-дд.мм.гггг'")
        else:
            bot.send_message(message.from_user.id, f"Вы указали количество номеров - {rooms_amount}. "
                                                   f"Хотите указать другое количество номеров?")
            bot.register_next_step_handler(message, change_state)

        data['people_amount'] = ans_help
    except ValueError:
        bot.send_message(message.from_user.id, "Количество человек должно быть целым положительным числом.")


def change_state(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        rooms_amount = data['rooms_amount']
    if message.text.strip().lower() == 'да':
        bot.set_state(message.from_user.id, UserStateInfo.search_city, message.chat.id)
        bot.send_message(message.from_user.id, "Еще раз введите на АНГЛИЙСКОМ ЯЗЫКЕ в каком городе будем вести поиск отелей.")
        bot.register_next_step_handler(message, choose_rooms_count)
    else:
        bot.send_message(message.from_user.id, f"Вы указали количество номеров - {rooms_amount}. "
                                               f"Введите {rooms_amount} числа через пробел.")


@bot.message_handler(state=UserStateInfo.dates)
def get_dates(message: Message) -> None:
    try:
        dates = message.text.strip().split('-')
        dates_to_list = list(map(lambda elem: int(elem), dates[0].split('.')))
        dates_from_list = list(map(lambda elem: int(elem), dates[1].split('.')))

        dates_to = datetime(dates_to_list[2], dates_to_list[1], dates_to_list[0]).date()
        dates_from = datetime(dates_from_list[2], dates_from_list[1], dates_from_list[0]).date()

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['querystring_properties_list'].update(
                {'checkIn' : str(dates_to)}
            )
            data['querystring_properties_list'].update(
                {'checkOut': str(dates_from)}
            )
            data['days_count'] = dates_from - dates_to
        bot.set_state(message.from_user.id, UserStateInfo.hotels_count, message.chat.id)
        bot.send_message(message.from_user.id, "Введите какое количество отелей показать.")

    except Exception:
        bot.send_message(message.from_user.id, "Введите даты заезда и выезда в формате 'дд.мм.гггг-дд.мм.гггг'.")


@bot.message_handler(state=UserStateInfo.hotels_count)
def get_hotels_count(message: Message) -> None:
    try:
        page_number = math.ceil(int(message.text.strip()) / 25)
        page_size = int(message.text.strip())

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['querystring_properties_list'].update(
                {'pageNumber' : str(page_number)}
            )
            data['querystring_properties_list'].update(
                {'pageSize' : str(page_size)}
            )

        bot.set_state(message.from_user.id, UserStateInfo.hotels_photo, message.chat.id)
        bot.send_message(message.from_user.id, "Показать фотографии отеля? Введите сообщение в формате: "
                                                   "'Да 3' или 'Нет'.")

    except Exception:
        bot.send_message(message.from_user.id, "Количество отелей должно быть целым числом и больше нуля.")


@bot.message_handler(state=UserStateInfo.hotels_photo)
def get_hotel_photo(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        try:
            ans = message.text.strip().split()
            if ans[0].lower() in ['да', 'ага', 'yes', 'y']:
                data['hotel_photo'] = {
                    'need_photo' : True
                }
                try:
                    if len(ans) > 1:
                        decision = int(ans[1])
                        if decision > 0:
                            data['hotel_photo'].update(
                                {
                                    'photo_count': decision
                                }
                            )
                            if data.get('search').get('mode') in ['lowprice', 'highprice']:
                                bot.set_state(message.from_user.id, UserStateInfo.confirm_data, message.chat.id)
                                bot.send_message(message.from_user.id, f"{print_data(data=data)}Верно?")
                            else:
                                bot.send_message(message.from_user.id,
                                                 f"Введите диапазон цен (минимальная цена - максимальная цена "
                                                 f"в {data.get('querystring_location_search').get('currency')})"
                                                 " в формате '1000-2000'.")
                                bot.set_state(message.from_user.id, UserStateInfo.price_range, message.chat.id)
                        else:
                            raise HotelPhotoError
                    else:
                        raise HotelPhotoError
                except ValueError:
                    raise HotelPhotoError
            elif ans[0].lower() in ['нет', 'no', 'nope', 'n']:
                data['hotel_photo'] = {
                    'need_photo' : False
                }
                if data.get('search').get('mode') in ['lowprice', 'highprice']:
                    bot.set_state(message.from_user.id, UserStateInfo.confirm_data, message.chat.id)
                    bot.send_message(message.from_user.id, f"{print_data(data=data)}Верно?")
                else:
                    bot.send_message(message.from_user.id, f"Введите диапазон цен (минимальная цена - максимальная цена "
                                                           f"в {data.get('querystring_location_search').get('currency')})"
                                                           " в формате '1000-2000'.")
                    bot.set_state(message.from_user.id, UserStateInfo.price_range, message.chat.id)
            else:
                raise HotelPhotoError
        except HotelPhotoError:
            bot.send_message(message.from_user.id, "Хм...не понял. Введите сообщение в формате: 'Да 3' или 'Нет'.")


@bot.message_handler(state=UserStateInfo.price_range)
def price_range(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        try:
            ans = message.text.strip().split('-')
            if len(ans) == 2 and (int(ans[0]) <= int(ans[1])):
                temp_res = list(map(lambda elem: int(elem), ans))
                data['search'][f"{data.get('search').get('mode')}"] = {
                    'price_range': temp_res
                }

                bot.send_message(message.from_user.id, f"Введите диапазон расстояния в милях "
                                                       f"(минимальное - максимальное) в формате '0.1-0.2' или '1-2'.")
                bot.set_state(message.from_user.id, UserStateInfo.distance_range, message.chat.id)
            else:
                raise PriceException
        except PriceException:
            bot.send_message(message.from_user.id, f"Введите диапазон цен (минимальная цена - максимальная цена "
                                                   f"в {data.get('querystring_location_search').get('currency')}) "
                                                   f"в формате '1000-2000'.")
        except ValueError:
            bot.send_message(message.from_user.id, f"Введите диапазон цен (минимальная цена - максимальная цена "
                                                   f"в {data.get('querystring_location_search').get('currency')}) "
                                                   f"в формате '1000-2000'.")


@bot.message_handler(state=UserStateInfo.distance_range)
def distance_range(message: Message) -> None:
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
                                f"{data.get('querystring_location_search').get('currency')}\n" \
                                f"Диапазон расстояния до центра от " \
                                f"{data.get('search').get('bestdeal').get('distance_range')[0]} до " \
                                f"{data.get('search').get('bestdeal').get('distance_range')[1]} мили(ь)\n"
                    bot.send_message(message.from_user.id, f"{print_data(data=data)}{temp_text}Верно?")
                    bot.set_state(message.from_user.id, UserStateInfo.confirm_data, message.chat.id)
                    print(data)
                else:
                    raise DistanceException
            else:
                raise DistanceException
        except DistanceException:
            bot.send_message(message.from_user.id, f"Введите диапазон расстояния в милях "
                                                   f"(минимальное - максимальное) в формате '0,1-0,2' или '1-2'.")
        except ValueError:
            bot.send_message(message.from_user.id, f"Введите диапазон расстояния в милях "
                                                   f"(минимальное - максимальное) в формате '0,1-0,2' или '1-2'.")


@bot.message_handler(state=UserStateInfo.confirm_data)
def confirm_data(message: Message) -> None:
    if message.text.lower() in ['да', 'ага', 'yes', 'y']:
        # Через запрос к API
        # with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        #     location_info = get_info(url='https://hotels4.p.rapidapi.com/locations/v2/search',
        #                     querystring=data['querystring_location_search'])
        #
        #     """Запись в текстовый файл для работы через файлы"""
        #     with open(f"parced_data/location_info_result_{data.get('search').get('mode')}.txt", 'w') as file:
        #         file.write(location_info)
        #
        #     if data.get('search').get('mode') == 'bestdeal':
        #         collecting_lm_ids(location_info=location_info, data=data)
        #
        # location_info_result = location_info_results(location_info=location_info)
        # if location_info_result:
        #     bot.send_message(message.from_user.id, "Уточните, пожалуйста, где ищем:",
        #                     reply_markup=place_choice(places=collecting_data_places(location_info_result)))
        #     with open(f"parced_data/location_info_result_{data.get('search').get('mode')}.json", 'w') as file:
        #         json.dump(location_info_result, file, indent=4)
        # else:
        #     bot.send_message(message.from_user.id, "Извините, по данному городу информации нет.")



        # Только для работы с файлом
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            with open(f"parced_data/location_info_result_{data.get('search').get('mode')}.json", 'r') as file:
                location_info_result = json.load(file)
        if data.get('search').get('mode') == 'bestdeal':
            with open(f"parced_data/location_info_result_{data.get('search').get('mode')}.txt", 'r') as file:
                location_info = file.read()
            collecting_lm_ids(location_info=location_info, data=data)
            bot.send_message(message.from_user.id, "Уточните, пожалуйста, где ищем:",
                             reply_markup=place_choice(places=collecting_data_places(location_info_result)))
        #

    else:
        bot.send_message(message.from_user.id, "Давайте уточним запрос.")
        bot.set_state(message.from_user.id, UserStateInfo.info_collected)
        bot.register_next_step_handler(message, choose_lang)