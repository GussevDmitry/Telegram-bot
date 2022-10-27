from loader import bot
from telebot.types import CallbackQuery
from states.user_states import UserStateInfo
from loguru import logger


@bot.callback_query_handler(func=lambda call: call.data in ("change_y", "change_n"))
def change_room_amount_callback(call: CallbackQuery) -> None:
    """
    Handling the callback (function "change_room_amount") with user's preferred option.
    If user's choice is positive asking about city to search again and returning to handler "choose_rooms_count"
    If user's choice is negative asking to enter the amount of people in every room correctly
    :param call: user's preferred option
    """
    with bot.retrieve_data(call.from_user.id) as data:
        rooms_amount = data['rooms_amount']
        print(rooms_amount)
    if call.data == "change_y":
        logger.debug("Yes_change")
        bot.send_message(call.message.chat.id, f"Еще раз введите на {data.get('language')} языке в каком городе будем "
                                               f"вести поиск отелей.")
        bot.set_state(call.from_user.id, UserStateInfo.search_city)
    else:
        logger.debug("No_change")
        bot.send_message(call.message.chat.id, f"Вы указали количество номеров - {rooms_amount}. "
                                               f"Введите {rooms_amount} числа через пробел.")
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
