from loader import bot
from states.user_states import UserStateInfo
from telebot.types import Message
from utils.collect_data_to_show import collect_data_to_show
from utils.properties_info_results import properties_info_results
from keyboards.inline.create_photo_buttons import create_photo_buttons
from utils.misc.currency_output import currency_output
from keyboards.reply.specify_request import specify_request
from loguru import logger


def highprice_search(message: Message) -> None:
    """
    Collecting information about appropriate for requirements hotels (highprice command).
    Printing the information about hotels and sending hotel's photos (if needed)
    :param message: Start search message (reply keyboard "start_search")
    """
    # Через запрос к API
    bot.send_message(message.from_user.id, "Начинаю подбор отелей по Вашему запросу. Ожидайте завершающего сообщения.")
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        flag = data.get('hotel_photo').get('need_photo')
        total_results = properties_info_results(data=data)
    #

    # Только для работы с файлом
    # with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
    #     with open(f"parced_data/properties_info_{data.get('search').get('mode')}.txt", 'r') as file:
    #         temp_data = file.read()
    #     result = json.loads(f"{temp_data}")
    #     results = result.get('data').get('body').get('searchResults').get('results')
    #     flag = data.get('hotel_photo').get('need_photo')

    if isinstance(total_results, list):
        collect_data_to_show(data=data, results=total_results, flag=flag)

        for i_index, i_data in enumerate(data['search'][f"{data.get('search').get('mode')}"]['results']):
            photos = ["Фотографии отеля не запрашивались"]
            if flag:
                photos = data['search'][f"{data.get('search').get('mode')}"]['results'][i_index].get('hotel_photos')
            lm_text = ', '.join(i_data.get('landmarks'))
            text = f"\U0001F3E8 Отель {i_data.get('name')}\n" \
                   f"Адрес - {i_data.get('address')}\n" \
                   f"Количество звезд: {i_data.get('starRating')}\n" \
                   f"Рейтинг гостей: {i_data.get('guestRating')}\n" \
                   f"Расстояние до {lm_text}\n" \
                   f"Стоимость за одну ночь: {i_data.get('price_per_night'):,d} " \
                   f"{currency_output(price=i_data.get('price_per_night'), data=data)}\n" \
                   f"Стоимость итого: {i_data.get('price'):,d} " \
                   f"{currency_output(price=i_data.get('price_per_night'), data=data)} за {data.get('rooms_amount')} " \
                   f"комнату(ы) для {data.get('people_amount')} гостей\n за {data.get('days_count')} ночь/ночей"
            bot.send_message(message.from_user.id, f"{text}")

            if photos[0] not in ('У выбранного Вами отеля нет фотографий', 'Фотографии отеля не запрашивались'):
                if len(photos) > 1:
                    bot.send_photo(message.from_user.id, photos[0],
                                   reply_markup=create_photo_buttons(index=0, hotel_index=i_index))
                else:
                    bot.send_photo(message.from_user.id, photos[0])
            else:
                bot.send_message(message.from_user.id, f"\U0001F4DB{photos[0]}")

        bot.send_message(message.from_user.id, "Поиск завершен! Для перехода в главное меню нажмите команду /help.")
    else:
        bot.send_message(message.from_user.id, total_results, reply_markup=specify_request())
    logger.debug(f"{data}")
    bot.set_state(message.from_user.id, UserStateInfo.info_collected, message.chat.id)
