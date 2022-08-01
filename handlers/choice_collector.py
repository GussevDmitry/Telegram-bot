from states.user_states import UserStateInfo
from loader import bot
from telebot.types import Message, CallbackQuery
from datetime import datetime
from exceptions import HotelPhotoError
from keyboards.inline.language_choice import language_choice
from keyboards.inline.currency_choice import currency_choice


# basic_data = {
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


@bot.message_handler(state=UserStateInfo.info_collected, commands=['lowprice', 'highprice', 'bestdeal'])
def choose_lang(message: Message) -> None:
    # if UserStateInfo is UserStateInfo.info_collected:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['search_mode'] = message.text[1:]
    bot.set_state(message.from_user.id, UserStateInfo.language, message.chat.id)
    bot.send_message(message.from_user.id, "Выберете предпочтительный язык поиска. После выбора введите 'ок'.",
                     reply_markup=language_choice())
    # else:
    #     bot.send_message(message.from_user.id, "Сначала неоходимо пройти регистрацию. Для этого наберите команду /survey")


@bot.callback_query_handler(func=lambda call: call.data in ['ru-RU', 'en-US'])
def language(call: CallbackQuery):
    if call.data == "ru-RU":
        with bot.retrieve_data(call.from_user.id) as data:
            data['querystring'] = {
                'locale': 'ru-RU'
            }
    elif call.data == "en-US":
        with bot.retrieve_data(call.from_user.id) as data:
            data['querystring'] = {
                'locale': 'en-US'
            }


@bot.message_handler(state=UserStateInfo.language)
def choose_curr(message: Message) -> None:
    bot.send_message(message.from_user.id, "Запомнил. Теперь выберете в какой валюте выводить стоимость отелей."
                                           "После выбора наберите 'ок'.", reply_markup=currency_choice())
    bot.set_state(message.from_user.id, UserStateInfo.currency, message.chat.id)


@bot.callback_query_handler(func=lambda call: call.data in ['USD', 'EUR', 'RUB'])
def currency(call: CallbackQuery):
    if call.data == "USD":
        with bot.retrieve_data(call.from_user.id) as data:
            data['querystring'].update(
                {'currency': 'USD'}
            )

    elif call.data == "EUR":
        with bot.retrieve_data(call.from_user.id) as data:
            data['querystring'].update(
                {'currency': 'EUR'}
            )

    elif call.data == "RUB":
        with bot.retrieve_data(call.from_user.id) as data:
            data['querystring'].update(
                {'currency': 'RUB'}
            )


@bot.message_handler(state=UserStateInfo.currency)
def choose_city(message: Message) -> None:
    bot.send_message(message.from_user.id, "Запомнил. Теперь введите в каком городе будем вести поиск отелей.")
    bot.set_state(message.from_user.id, UserStateInfo.search_city, message.chat.id)


@bot.message_handler(state=UserStateInfo.search_city)
def collected_data(message: Message) -> None:
    bot.set_state(message.from_user.id, UserStateInfo.dates, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['querystring'].update(
            {'query': message.text.strip().lower()}
        )
        print(data.get('querystring'))
    bot.send_message(message.from_user.id, "Запомнил. Укажите даты заезда и выезда (день-месяц-год) в формате "
                                           "'дд.мм.гггг-дд.мм.гггг' ")


@bot.message_handler(state=UserStateInfo.dates)
def get_dates(message: Message) -> None:
    try:
        dates = message.text.strip().split('-')
        dates_to_list = list(map(lambda elem: int(elem), dates[0].split('.')))
        dates_from_list = list(map(lambda elem: int(elem), dates[1].split('.')))

        dates_to = datetime(dates_to_list[2], dates_to_list[1], dates_to_list[0]).date()
        dates_from = datetime(dates_from_list[2], dates_from_list[1], dates_from_list[0]).date()

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['dates_to'] = dates_to
            data['dates_from'] = dates_from
            data['days_count'] = dates_from - dates_to
        bot.set_state(message.from_user.id, UserStateInfo.hotels_count, message.chat.id)
        bot.send_message(message.from_user.id, "Введите какое количество отелей показать.")

    except Exception:
        bot.send_message(message.from_user.id, "Введите даты заезда и выезда в формате 'дд.мм.гггг-дд.мм.гггг'.")


@bot.message_handler(state=UserStateInfo.hotels_count)
def get_hotels_count(message: Message) -> None:
    try:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['hotels_count'] = int(message.text.strip())
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
                            data['hotel_photo'] = {
                                'photo_count' : decision
                            }
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

        if data['search_mode'] == 'lowprice':
            bot.set_state(message.from_user.id, UserStateInfo.lowprice, message.chat.id)
        elif data['search_mode'] == 'highprice':
            bot.set_state(message.from_user.id, UserStateInfo.highprice, message.chat.id)
        else:
            bot.set_state(message.from_user.id, UserStateInfo.bestdeal, message.chat.id)

        text = f"Ищем отель в городе: {data.get('querystring').get('query').title()}\n" \
               f"Язык поиска - {data.get('querystring').get('locale')}\n" \
               f"Стоимость выводим в валюте: {data.get('querystring').get('currency')}\n" \
               f"Даты с {data.get('dates_to')} по {data.get('dates_from')}\n" \
               f"Всего дней - {int(data.get('days_count').days)}\n" \
               f"Показываю отелей: {data.get('hotels_count')}\n"
        bot.send_message(message.from_user.id, f"{text}Верно?")

    except HotelPhotoError:
        bot.send_message(message.from_user.id, "Хм...не понял. Введите сообщение в формате: 'Да 3' или 'Нет'.")