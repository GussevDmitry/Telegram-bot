from loader import bot
from telebot.types import CallbackQuery
from utils.print_data import print_data
from states.user_states import UserStateInfo
from keyboards.inline.request_confirmation import request_confirmation


@bot.callback_query_handler(func=lambda call: call.data in ["да", "нет"])
def need_photo_choice_callback(call: CallbackQuery) -> None:
    """
    Handling the callback (function "need_photo_choice") with user's preferred option.
    If user's choice is positive asking about the amount of photos to be shown.
    If user's choice is negative and the search mode is NOT "bestdeal" confirming the collected information
    with function "print_data".
    If user's choice is negative and the search mode is "bestdeal" asking about the range of the hotel's price
    :param call: user's choice ("да" or "нет")
    """
    with bot.retrieve_data(call.from_user.id) as data:
        if call.data == "да":
            data['hotel_photo'] = {
                'need_photo': True
            }
            bot.send_message(call.from_user.id, "Сколько фотографий?")
            bot.set_state(call.from_user.id, UserStateInfo.hotels_photo_count)
        else:
            data['hotel_photo'] = {
                'need_photo': False
            }
            if data.get('search').get('mode') in ['lowprice', 'highprice']:
                bot.send_message(call.from_user.id,
                                 f"{print_data(data=data)}Верно?",
                                 reply_markup=request_confirmation())
                # bot.set_state(call.from_user.id, UserStateInfo.confirm_data)
            else:
                bot.send_message(call.from_user.id, f"Введите диапазон цен (минимальная цена - максимальная цена "
                                                    f"в {data.get('querystring_location_search').get('currency')}) "
                                                    f"в формате '1000-2000'.")
                bot.set_state(call.from_user.id, UserStateInfo.price_range)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
