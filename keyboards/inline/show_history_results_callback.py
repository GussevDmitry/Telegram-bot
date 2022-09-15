from telebot.types import CallbackQuery
from loader import bot
from database.create_database import db, User, Hotel, Request, Photo
from handlers.history.history import get_user_history
from keyboards.reply.show_more_history import show_more_history
from database.request_description import request_results


@bot.callback_query_handler(func=lambda call: call.data.istitle())
def show_history_results_callback(call: CallbackQuery):
    with bot.retrieve_data(call.from_user.id) as data:
        query_res = request_results(call=call, data=data)

    for i_hotel in db.execute(query_res):

        query_photo = User.select(Photo.photo_url) \
            .where(User.phone_number == data.get('phone_number')) \
            .join(Request, on=(Request.user_id == User.phone_number)) \
            .join(Hotel, on=(Hotel.request_id == Request.id)) \
            .where(Request.id == int(call.data[2:]))\
            .join(Photo, on=(Photo.hotel_id == i_hotel[0]))\
            .where(Hotel.hotel_id == i_hotel[1])

        url_str = ''
        for i_url in db.execute(query_photo):
            url_str += f"{i_url[0]}\n"

        text_hotel = f"Название отеля: {i_hotel[2]}\n" \
                     f"Рейтинг отеля: {i_hotel[3]}\n" \
                     f"Адрес: {i_hotel[4]}\n" \
                     f"Стоимость: {i_hotel[5]}\n"

        text_photo = f"Фото: {url_str}" if len(url_str) >= 1 else ""
        bot.send_message(call.from_user.id, f"{text_hotel}{text_photo}")
    bot.send_message(call.from_user.id, "Для вывода истории запросов нажмите на кнопку.",
                     reply_markup=show_more_history())
    bot.register_next_step_handler(call.message, get_user_history)
