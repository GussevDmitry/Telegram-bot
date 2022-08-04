import math
from states.user_states import UserStateInfo
from loader import bot
from telebot.types import Message, CallbackQuery
from datetime import datetime
from exceptions import HotelPhotoError
from keyboards.inline.language_choice import language_choice
from keyboards.inline.currency_choice import currency_choice


# data = {
#     'search_mode': None,
#     'rooms_amount': 0,
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


@bot.callback_query_handler(func=lambda call: call.data in ['ru-RU', 'en-US'])
def language(call: CallbackQuery):
    bot.answer_callback_query(callback_query_id=call.id, text='Запомнил!')
    if call.data == "ru-RU":
        with bot.retrieve_data(call.from_user.id) as data:
            data['querystring_location_search'] = {
                'locale': 'ru-RU'
            }
            data['querystring_properties_list'] = {
                'locale': 'ru-RU'
            }
    elif call.data == "en-US":
        with bot.retrieve_data(call.from_user.id) as data:
            data['querystring_location_search'] = {
                'locale': 'en-US'
            }
            data['querystring_properties_list'] = {
                'locale': 'en-US'
            }
    bot.send_message(call.message.chat.id, "Теперь выберете в какой валюте выводить стоимость отелей.",
                     reply_markup=currency_choice())


@bot.callback_query_handler(func=lambda call: call.data in ['USD', 'EUR', 'RUB'])
def currency(call: CallbackQuery):
    bot.answer_callback_query(callback_query_id=call.id, text='Запомнил!')
    if call.data == "USD":
        with bot.retrieve_data(call.from_user.id) as data:
            data['querystring_location_search'].update(
                {'currency': 'USD'}
            )
            data['querystring_properties_list'].update(
                {'currency': 'USD'}
            )

    elif call.data == "EUR":
        with bot.retrieve_data(call.from_user.id) as data:
            data['querystring_location_search'].update(
                {'currency': 'EUR'}
            )
            data['querystring_properties_list'].update(
                {'currency': 'EUR'}
            )

    elif call.data == "RUB":
        with bot.retrieve_data(call.from_user.id) as data:
            data['querystring_location_search'].update(
                {'currency': 'RUB'}
            )
            data['querystring_properties_list'].update(
                {'currency': 'RUB'}
            )
    bot.send_message(call.message.chat.id, "Запомнил. Теперь введите на АНГЛИЙСКОМ ЯЗЫКЕ "
                                           "в каком городе будем вести поиск отелей.")
    bot.register_next_step_handler(call.message, choose_rooms_count)


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
        bot.send_message(message.from_user.id, "Еще раз введите в каком городе будем вести поиск отелей.")
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
    try:
        ans = message.text.strip().split()
        if ans[0].lower() == 'да':
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['hotel_photo'] = {
                    'need_photo' : True
                }
            try:
                if len(ans) > 1:
                    decision = int(ans[1])
                    if decision > 0:
                        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                            data['hotel_photo'].update(
                                {
                                    'photo_count': decision
                                }
                            )
                    else:
                        raise HotelPhotoError
            except ValueError:
                raise HotelPhotoError
        elif ans[0].lower() == 'нет':
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['hotel_photo'] = {
                    'need_photo' : False
                }
        else:
            raise HotelPhotoError

        if data['search'].get('mode') == 'lowprice':
            bot.set_state(message.from_user.id, UserStateInfo.lowprice, message.chat.id)
        elif data['search'].get('mode') == 'highprice':
            bot.set_state(message.from_user.id, UserStateInfo.highprice, message.chat.id)
        else:
            bot.set_state(message.from_user.id, UserStateInfo.bestdeal, message.chat.id)

        text = f"Ищем отель в городе: {data.get('querystring_location_search').get('query').title()}\n" \
               f"Стоимость выводим в валюте: {data.get('querystring_properties_list').get('currency')}\n" \
               f"Даты с {data.get('querystring_properties_list').get('checkIn')} по " \
               f"{data.get('querystring_properties_list').get('checkOut')}\n" \
               f"Всего дней - {int(data.get('days_count').days)}\n" \
               f"Показываю отелей: {data.get('querystring_properties_list').get('pageSize')}\n"
        bot.send_message(message.from_user.id, f"{text}Верно?")

    except HotelPhotoError:
        bot.send_message(message.from_user.id, "Хм...не понял. Введите сообщение в формате: 'Да 3' или 'Нет'.")