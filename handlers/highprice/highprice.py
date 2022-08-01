from loader import bot
from states.user_states import UserStateInfo
from telebot.types import Message


@bot.message_handler(state=UserStateInfo.highprice)
def highprice_search(message: Message) -> None:

    # data = {
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

    bot.send_message(message.from_user.id, "\U0001F44D\nРезультаты поиска самых дорогих отелей:")