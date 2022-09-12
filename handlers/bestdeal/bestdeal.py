from loader import bot
from states.user_states import UserStateInfo
from telebot.types import Message
from utils.collect_data_to_show import collect_data_to_show
from utils.properties_info_results import properties_info_results
from keyboards.inline.create_photo_buttons import create_photo_buttons


def bestdeal_search(message: Message) -> None:
    # Через запрос к API
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        flag = data.get('hotel_photo').get('need_photo')
        results_to_show = properties_info_results(data=data)

        collect_data_to_show(data=data, results=results_to_show, flag=flag)

    if results_to_show == []:
        text = "По выбранным критериям отели не найдены. Давайте попробуем изменить критерии поиска!"
        bot.send_message(message.from_user.id, text)
    else:
        for i_index, i_data in enumerate(data['search'][f"{data.get('search').get('mode')}"]['results']):
            photos = ["Фотографии отеля не запрашивались"]
            if flag:
                photos = data['search'][f"{data.get('search').get('mode')}"]['results'][i_index].get('hotel_photos')
            lm_text = ', '.join(i_data.get('landmarks')[:1])
            text = f"\U0001F3E8 Отель {i_data.get('name')}\n" \
                   f"Адрес - {i_data.get('address')}\n" \
                   f"Расстояние до {lm_text}\n" \
                   f"Стоимость итого: {i_data.get('price')} за {data.get('rooms_amount')} " \
                   f"комнату(ы) для {data.get('people_amount')} гостей\n"
            bot.send_message(message.from_user.id, f"{text}")

            if photos[0] not in ('У выбранного Вами отеля нет фотографий', 'Фотографии отеля не запрашивались'):
                bot.send_photo(message.from_user.id, photos[0],
                               reply_markup=create_photo_buttons(index=0, hotel_index=i_index))
            else:
                bot.send_message(message.from_user.id, f"\U0001F4DB{photos[0]}")

    print(data)
    bot.set_state(message.from_user.id, UserStateInfo.info_collected, message.chat.id)
