import math
import json
from states.user_states import UserStateInfo
from loader import bot
from telebot.types import Message
from datetime import datetime
from exceptions import PriceException, DistanceException
from utils.get_API_info import get_info
from utils.collecting_places_data import collecting_data_places
from keyboards.inline.language_choice import language_choice
from keyboards.inline.place_choice import place_choice
from utils.print_data import print_data
from utils.collecting_lm_ids import collecting_lm_ids
from utils.location_info_results import location_info_results
from database.request_filling import request_filling
from keyboards.inline.create_calendar import create_calendar
from keyboards.inline.need_photo_choice import need_photo_choice
from keyboards.reply.specify_request import specify_request


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
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['search'] = {
            'mode': message.text[1:]
        }
    bot.send_message(message.from_user.id, "Выберете предпочтительный язык поиска.",
                     reply_markup=language_choice())


@bot.message_handler(state=UserStateInfo.search_city)
def choose_rooms_count(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['querystring_location_search'].update(
            {'query': message.text.strip().lower().title()}
        )
    bot.send_message(message.from_user.id, "Сколько номеров в отеле Вам необходимо?")
    bot.set_state(message.from_user.id, UserStateInfo.rooms_number, message.chat.id)


@bot.message_handler(state=UserStateInfo.rooms_number)
def choose_people_amount(message: Message) -> None:
    if message.text.strip().isdigit():
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['rooms_amount'] = int(message.text.strip())
        bot.send_message(message.from_user.id, "Введите количество взрослых людей в каждом номере через пробел.")
        bot.set_state(message.from_user.id, UserStateInfo.people_amount, message.chat.id)
    else:
        bot.send_message(message.from_user.id, "Количество номеров должно быть целым положительным числом.")


@bot.message_handler(state=UserStateInfo.people_amount)
def choose_year(message: Message) -> None:
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
                                                   f"Хотите указать другое количество номеров?")
            bot.register_next_step_handler(message, change_state)

        data['people_amount'] = ans_help
    except ValueError:
        bot.send_message(message.from_user.id, "Количество человек должно быть целым положительным числом.")


def change_state(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        rooms_amount = data['rooms_amount']
    if message.text.strip().lower() == 'да':
        bot.send_message(message.from_user.id, f"Еще раз введите на {data.get('language')} языке в каком городе будем "
                                               f"вести поиск отелей.")
        bot.set_state(message.from_user.id, UserStateInfo.search_city, message.chat.id)
    else:
        bot.send_message(message.from_user.id, f"Вы указали количество номеров - {rooms_amount}. "
                                               f"Введите {rooms_amount} числа через пробел.")


@bot.message_handler(state=UserStateInfo.trip_year)
def get_trip_year(message:Message) -> None:
    if message.text.strip().isdigit():
        year_now = datetime.now().year
        if int(message.text.strip()) > year_now:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['shown_dates'] = (int(message.text.strip()), 1)
            bot.send_message(message.from_user.id, "Выберете дату заезда.",
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

        bot.set_state(message.from_user.id, UserStateInfo.hotels_photo_flag, message.chat.id)
        bot.send_message(message.from_user.id, "Показать фотографии отеля?", reply_markup=need_photo_choice())
    else:
        bot.send_message(message.from_user.id, "Количество отелей должно быть целым числом и больше нуля.")


@bot.message_handler(state=UserStateInfo.hotels_photo_count)
def get_hotel_photo(message: Message) -> None:
    if message.text.strip().isdigit():
        photo_count = int(message.text.strip())
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['hotel_photo'].update(
                {
                    'photo_count': photo_count
                }
            )
        if data.get('search').get('mode') in ['lowprice', 'highprice']:
            bot.send_message(message.from_user.id, f"{print_data(data=data)}Верно?")
            bot.set_state(message.from_user.id, UserStateInfo.confirm_data, message.chat.id)
        else:
            bot.send_message(message.from_user.id,
                             f"Введите диапазон цен (минимальная цена - максимальная цена "
                             f"в {data.get('currency')[3]}) в формате '1000-2000'.")
            bot.set_state(message.from_user.id, UserStateInfo.price_range, message.chat.id)
    else:
        bot.send_message(message.from_user.id, "Количество фотографий должно быть целым неотрицательным числом.")


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
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        try:
            temp_res = []
            ans = message.text.strip().split('-')
            if len(ans) == 2:
                for i_elem in ans:
                    if i_elem.isdigit():
                        temp_res.append(round(int(i_elem) / 1.6093, 2))
                    elif '.' in i_elem:
                        temp_res.append(round(float(i_elem) / 1.6093, 2))
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
                                f"{round(data.get('search').get('bestdeal').get('distance_range')[0] * 1.6093, 1)} до " \
                                f"{round(data.get('search').get('bestdeal').get('distance_range')[1] * 1.6093, 1)} км\n"
                    bot.send_message(message.from_user.id, f"{print_data(data=data)}{temp_text}Верно?")
                    bot.set_state(message.from_user.id, UserStateInfo.confirm_data, message.chat.id)
                    print(data)
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


@bot.message_handler(state=UserStateInfo.confirm_data)
def confirm_data(message: Message) -> None:
    if message.text.lower() in ['да', 'д', 'ага', 'yes', 'y']:
        # Через запрос к API
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            location_info = get_info(url='https://hotels4.p.rapidapi.com/locations/v2/search',
                            querystring=data['querystring_location_search'])

            """Запись в текстовый файл для работы через файлы"""
            with open(f"parced_data/location_info_result_{data.get('search').get('mode')}.txt", 'w',
                      encoding='utf-8') as file:
                file.write(location_info)

            if data.get('search').get('mode') == 'bestdeal':
                collecting_lm_ids(location_info=location_info, data=data)
                print(data)

        location_info_result = location_info_results(location_info=location_info)
        if location_info_result:
            places_lst = collecting_data_places(location_info_result)
            bot.send_message(message.from_user.id, "Уточните, пожалуйста, город\район, где ищем:",
                            reply_markup=place_choice(places=places_lst))
            with open(f"parced_data/location_info_result_{data.get('search').get('mode')}.json", 'w',
                      encoding='utf-8') as file:
                json.dump(location_info_result, file, indent=4)

            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                request_filling(data=data, places=places_lst)

        else:
            bot.send_message(message.from_user.id, "Извините, по данному городу информации нет. "
                                                   "Давайте уточним запрос.", reply_markup=specify_request())
            bot.set_state(message.from_user.id, UserStateInfo.info_collected)

    else:
        bot.send_message(message.from_user.id, "Давайте уточним запрос.", reply_markup=specify_request())
        bot.set_state(message.from_user.id, UserStateInfo.info_collected)