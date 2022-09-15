from loader import bot
from telebot.types import Message
from database.create_database import db
from keyboards.inline.show_history_results import show_history_results
from states.user_states import UserStateInfo
from database.request_description import request_description
from utils.misc.commands_comparison import commands_comparison
from datetime import datetime


@bot.message_handler(state=UserStateInfo.info_collected, commands=['history'])
def get_user_history(message: Message):
    bot.send_message(message.from_user.id, "История Ваших поисковых запросов:")

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        query_desc = request_description(data=data)

    for i_req in db.execute(query_desc):
        desc = commands_comparison(i_req[1])
        text_desc = f"Тип запроса - {desc}\n" \
                    f"Место назначения: {i_req[2]}\n" \
                    f"Количество номеров: {i_req[3]}\n" \
                    f"Количество гостей всего: {i_req[4]}\n" \
                    f"Дата заезда: {i_req[5]}\n" \
                    f"Дата выезда: {i_req[6]}\n" \
                    f"Количество ночей: " \
                    f"{(datetime.fromisoformat(i_req[6]).date() - datetime.fromisoformat(i_req[5]).date()).days}"
        bot.send_message(message.from_user.id, text_desc, reply_markup=show_history_results(ident=i_req[0]))
