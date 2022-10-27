from telebot.types import CallbackQuery
from loader import bot
from database.create_database import db
from handlers.history.history import get_user_history
from keyboards.reply.show_more_history import show_more_history
from database.request_description import request_results, photo_urls, landmarks_info
from keyboards.inline.create_photo_buttons import create_photo_buttons_history


@bot.callback_query_handler(func=lambda call: call.data.istitle())
def show_history_results_callback(call: CallbackQuery) -> None:
    """
    Handling the callback (function "show_history_results") with user's request choice
    :param call: user's request choice
    """
    with bot.retrieve_data(call.from_user.id) as data:
        query_res = request_results(call=call, data=data)

    data["history_urls"] = {}
    for i_hotel in db.execute(query_res):
        url_str = photo_urls(data=data, call=call, i_hotel=i_hotel)
        lm_str = landmarks_info(data=data, call=call, i_hotel=i_hotel)

        text_hotel = f"Название отеля: {i_hotel[2]}\n" \
                     f"Рейтинг отеля (звезды): {i_hotel[3]}\n" \
                     f"Рейтинг гостей: {i_hotel[4]}/10.0\n" \
                     f"Адрес: {i_hotel[5]}\n" \
                     f"Стоимость за одну ночь в {i_hotel[8]}: {i_hotel[6]:,d}\n" \
                     f"Стоимость итого в {i_hotel[8]}: {i_hotel[7]:,d}\n" \
                     f"Расстояние: {lm_str}"

        urls_lst = url_str.split(", ")
        data["history_urls"].update(
            {
                f"{i_hotel[0]}": urls_lst
            }
        )
        bot.send_message(call.from_user.id, f"{text_hotel}")
        if len(url_str) > 1:
            bot.send_photo(call.from_user.id, urls_lst[0], reply_markup=create_photo_buttons_history(0, i_hotel[0]))
        elif len(url_str) == 1:
            bot.send_photo(call.from_user.id, urls_lst[0])
        else:
            bot.send_message(call.from_user.id, "\U0001F4DBУ отеля нет "
                                                "фотографий или фотографии отеля не запрашивались")
    bot.send_message(call.from_user.id, "Для вывода истории запросов нажмите на кнопку.",
                     reply_markup=show_more_history())
    bot.register_next_step_handler(call.message, get_user_history)
