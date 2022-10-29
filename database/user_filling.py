from loader import bot
from database.create_database import User, db
from telebot.types import Message
from typing import Dict


def user_filling(message: Message, data: Dict, contact_info: str) -> None:
    """
    Filling the database with user's personal information
    :param message: User's phone number
    :param data: memory storage
    :param contact_info:  user's personal information
    """
    with db:
        help_query = User.select(User.phone_number)
        help_set = set()
        for i_num in help_query:
            help_set.add(i_num.phone_number)
        if int(message.contact.phone_number[1:]) not in help_set:
            User.create(name=data.get('name'), age=data.get('age'), country=data.get('country'),
                        city=data.get('city'), phone_number=data.get('phone_number'))
            bot.send_message(message.from_user.id, contact_info)
        else:
            bot.send_message(message.from_user.id, "Вы уже зарегистрированы! Вам доступен просмотр истории поиска."
                                                   "Для просмотра наберите команду /history")
