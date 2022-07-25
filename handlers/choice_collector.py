from states.user_states import UserStateInfo
from loader import bot
from telebot.types import Message, CallbackQuery
from datetime import datetime
from exceptions import HotelPhotoError
from keyboards.inline.language_choice import language_choice
from keyboards.inline.currency_choice import currency_choice


basic_data = {
    'dates_to': None,
    'dates_from': None,
    'days_count': 0,
    'hotels_count': 0,
    'hotel_photo': {
        'need_photo': False,
        'photo_count': 0
    },
    'querystring': {
        'locale': None,
        'currency': None,
        'query': None
    }
}
search_mode = None


@bot.message_handler(state=None, commands=['lowprice', 'highprce', 'bestdeal'])
def choose_lang(message: Message) -> None:
    global search_mode
    search_mode = message.text[1:]
    bot.send_message(message.from_user.id, "Выберете предпочтительный язык поиска.", reply_markup=language_choice())
    bot.set_state(message.from_user.id, UserStateInfo.language, message.chat.id)


@bot.callback_query_handler(state=UserStateInfo.language, func=None)
def choose_curr(call: CallbackQuery) -> None:
    global basic_data
    if call.data == 'русский':
        basic_data['querystring']['locale'] = 'ru-RU'
        bot.send_message(call.message.from_user.id, "Запомнил. Теперь введите в какой валюте выводить стоимость отелей "
                                               "(доллар, евро, рубль).", reply_markup=currency_choice())
        bot.set_state(call.message.from_user.id, UserStateInfo.currency, call.message.chat.id)
    elif call.data == 'английский':
        basic_data['querystring']['locale'] = 'en-US'
        bot.send_message(call.message.from_user.id, "Запомнил. Теперь введите в какой валюте выводить стоимость отелей "
                                               "(доллар, евро, рубль).", reply_markup=currency_choice())
        bot.set_state(call.message.from_user.id, UserStateInfo.currency, call.message.chat.id)
    else:
        bot.send_message(call.message.from_user.id, "[ERROR] Повторите ввод. Введите 'русский' или 'английский'.")


@bot.callback_query_handler(state=UserStateInfo.currency, func=None)
def choose_city(call: CallbackQuery) -> None:
    global basic_data
    if call.data == 'доллар':
        basic_data['querystring']['currency'] = 'USD'
        bot.set_state(call.message.from_user.id, UserStateInfo.search_city, call.message.chat.id)
        bot.send_message(call.message.from_user.id, "Запомнил. Теперь введите в каком городе будем вести поиск отелей.")
    elif call.data == 'евро':
        basic_data['querystring']['currency'] = 'EUR'
        bot.set_state(call.message.from_user.id, UserStateInfo.search_city, call.message.chat.id)
        bot.send_message(call.message.from_user.id, "Запомнил. Теперь введите в каком городе будем вести поиск отелей.")
    elif call.data == 'рубль':
        basic_data['querystring']['currency'] = 'RUB'
        bot.set_state(call.message.from_user.id, UserStateInfo.search_city, call.message.chat.id)
        bot.send_message(call.message.from_user.id, "Запомнил. Теперь введите в каком городе будем вести поиск отелей.")
    else:
        bot.send_message(call.message.from_user.id, "[ERROR] Повторите ввод. Введите 'доллар', 'евро' или 'рубль'.")


@bot.message_handler(state=UserStateInfo.search_city)
def collected_data(message: Message) -> None:
    bot.send_message(message.from_user.id, "Спасибо, запомнил.")
    bot.set_state(message.from_user.id, UserStateInfo.dates, message.chat.id)
    global basic_data
    basic_data['querystring']['query'] = message.text.strip().lower()
    bot.send_message(message.from_user.id, "Укажите даты заезда и выезда (день-месяц-год) в формате "
                                           "'дд.мм.гггг-дд.мм.гггг' ")


@bot.message_handler(state=UserStateInfo.dates)
def get_dates(message: Message) -> None:
    try:
        dates = message.text.strip().split('-')
        dates_to_list = list(map(lambda elem: int(elem), dates[0].split('.')))
        dates_from_list = list(map(lambda elem: int(elem), dates[1].split('.')))

        global basic_data
        dates_to = datetime(dates_to_list[2], dates_to_list[1], dates_to_list[0]).date()
        dates_from = datetime(dates_from_list[2], dates_from_list[1], dates_from_list[0]).date()
        basic_data['dates_to'] = dates_to
        basic_data['dates_from'] = dates_from
        basic_data['days_count'] = dates_from - dates_to
        bot.set_state(message.from_user.id, UserStateInfo.hotels_count, message.chat.id)
        bot.send_message(message.from_user.id, "Введите какое количество отелей показать.")

    except Exception:
        bot.send_message(message.from_user.id, "Введите даты заезда и выезда в формате 'дд.мм.гггг-дд.мм.гггг'.")


@bot.message_handler(state=UserStateInfo.hotels_count)
def get_hotels_count(message: Message) -> None:
    try:
        global basic_data
        basic_data['hotels_count'] = int(message.text.strip())
        bot.set_state(message.from_user.id, UserStateInfo.hotels_photo, message.chat.id)
        bot.send_message(message.from_user.id, "Показать фотографии отеля? Введите сообщение в формате: "
                                               "'Да 3' или 'Нет'.")

    except Exception:
        bot.send_message(message.from_user.id, "Количество отелей должно быть целым числом и больше нуля.")


@bot.message_handler(state=UserStateInfo.hotels_photo)
def get_hotel_photo(message: Message) -> None:
    try:
        ans = message.text.strip().split()
        global basic_data
        if ans[0].lower() == 'да':
            basic_data['hotel_photo']['need_photo'] = True
            try:
                decision = int(ans[1])
                if decision > 0:
                    basic_data['hotel_photo']['photo_count'] = decision
                    # print(search_mode)
                    if search_mode == 'lowprice':
                        bot.set_state(message.from_user.id, UserStateInfo.lowprice, message.chat.id)
                    elif search_mode == 'highprice':
                        bot.set_state(message.from_user.id, UserStateInfo.highprice, message.chat.id)
                    else:
                        bot.set_state(message.from_user.id, UserStateInfo.bestdeal, message.chat.id)
                else:
                    raise HotelPhotoError

            except ValueError:
                raise HotelPhotoError
        elif ans[0].lower() != 'да' and ans[0].lower() != 'нет':
            raise HotelPhotoError

    except HotelPhotoError:
        bot.send_message(message.from_user.id, "Хм...не понял. Введите сообщение в формате: 'Да 3' или 'Нет'.")