from loader import bot
from handlers.choice_collector import basic_data
from states.user_states import UserStateInfo
from telebot.types import Message
from get_API_info import get_info

@bot.message_handler(state=UserStateInfo.lowprice)
def lowprice_search(message: Message) -> None:

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

    text = f"Ищем отель в городе {basic_data['querystring']['query']}\n" \
           f"Стоимость выводим в валюте {basic_data['querystring']['currency']}\n" \
           f"Даты с {basic_data['dates_to']} по {basic_data['dates_from']}\n" \
           f"Всего дней - {basic_data['days_count']}\n" \
           f"Показываю {basic_data['hotels_count']} отелей\n"

    bot.send_message(message.from_user.id, text)

    data = get_info(url='https://hotels4.p.rapidapi.com/locations/v2/search', querystring=basic_data['querystring'])
    print(data)

    with open('test.txt', 'w') as file:
        file.write(data)

    bot.stop_polling()