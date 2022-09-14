from loader import bot
from telebot.types import Message
from database.create_database import db
from keyboards.inline.show_history_results import show_history_results
from states.user_states import UserStateInfo
from database.request_description import request_description


@bot.message_handler(state=UserStateInfo.info_collected, commands=['history'])
def get_user_history(message: Message):
    bot.send_message(message.from_user.id, "История Ваших поисковых запросов:")

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        query_desc = request_description(data=data)

    for i_req in db.execute(query_desc):
        text_desc = f"Тип запроса - {i_req[1]}\n" \
               f"Место назначения: {i_req[2]}\n" \
               f"Количество номеров: {i_req[3]}\n" \
               f"Количество гостей всего: {i_req[4]}\n" \
               f"Дата заезда: {i_req[5]}\n" \
               f"Дата выезда: {i_req[6]}"
        bot.send_message(message.from_user.id, text_desc, reply_markup=show_history_results(ident=i_req[0]))
