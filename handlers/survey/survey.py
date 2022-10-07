import os
from loader import bot
from states.user_states import UserStateInfo
from telebot.types import Message
from keyboards.reply.send_contact import request_contact
from database.user_filling import user_filling
from loguru import logger


@bot.message_handler(commands=['survey'])
def get_name(message: Message) -> None:
    """
    Username request
    :param message: message from user, /survey command
    """
    bot.set_state(message.from_user.id, UserStateInfo.name, message.chat.id)
    bot.send_message(message.from_user.id, f"\U0001F6A9 Приветствую, {message.from_user.username}! Введите Ваше имя.")


@bot.message_handler(state=UserStateInfo.name)
def get_age(message: Message) -> None:
    """
    User's age request
    :param message: message from user with his/her name
    """
    if message.text.isalpha() or map(lambda elem: elem.is_alpha(), message.text.split()):
        bot.send_message(message.from_user.id, "\U0001F44D Запомнил. Введите Ваш возраст?")
        bot.set_state(message.from_user.id, UserStateInfo.age, message.chat.id)
    else:
        bot.send_message(message.from_user.id, "\U0001F4A1 Имя не может содержать цифры.")

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text.strip().lower().title()


@bot.message_handler(state=UserStateInfo.age)
def get_country(message: Message) -> None:
    """
    User's residence country request
    :param message: message from user with his/her age
    """
    if message.text.isdigit():
        bot.send_message(message.from_user.id, "\U0001F44D Запомнил. Введите страну проживания.")
        bot.set_state(message.from_user.id, UserStateInfo.country, message.chat.id)
    else:
        bot.send_message(message.from_user.id, "\U0001F4A1 Возраст не может содержать букв.")

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['age'] = message.text.strip()


@bot.message_handler(state=UserStateInfo.country)
def get_city(message: Message) -> None:
    """
    User's residence city request
    :param message: message from user with his/her residence country
    """
    bot.send_message(message.from_user.id, "\U0001F44D Запомнил. Введите город проживания.")
    bot.set_state(message.from_user.id, UserStateInfo.city, message.chat.id)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['country'] = message.text.strip().lower().title()


@bot.message_handler(state=UserStateInfo.city)
def get_phone_num(message: Message) -> None:
    """
    User's phone number request with reply keyboard "request_contact"
    :param message: message from user with his/her residence city
    """
    bot.send_message(message.from_user.id, "\U0001F44D Запомнил. Отправьте свой номер телефона нажав на кнопку.",
                     reply_markup=request_contact())
    bot.set_state(message.from_user.id, UserStateInfo.phone_num, message.chat.id)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['city'] = message.text.strip().lower().title()


@bot.message_handler(content_types=['text', 'contact'], state=UserStateInfo.phone_num)
def get_contact_info(message: Message) -> None:
    """
    Obtaining user's personal information
    :param message: User's phone number
    """
    if message.content_type == 'contact':
        bot.set_state(message.from_user.id, UserStateInfo.info_collected, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['phone_number'] = int(message.contact.phone_number[1:])
        contact_info = f"\U0001F64CСпасибо. Данные записал\n" \
                       f"Имя - {data['name']}\n" \
                       f"Возраст - {data['age']}\n" \
                       f"Страна проживания - {data['country']}\n" \
                       f"Город проживания - {data['city']}\n" \
                       f"Номер телефона - {data['phone_number']}"

        # Filling the database with user's information
        user_filling(message=message, data=data, contact_info=contact_info)

        # Logging actions
        if not os.path.exists("logging"):
            os.mkdir("logging/")
        logger.add("logging/debug.log",
                   format="{time:YYYY-MM-DD at HH:mm:ss} - {level} - {name} - {message}",
                   level="DEBUG")
        logger.debug(f"User {data.get('name')} passes authentication")

        bot.send_message(message.chat.id, "Давайте приступим к подбору отеля для Вас. "
                                          "Чтобы ознакомиться с основными командами и их описанием, наберите /help")
    else:
        bot.send_message(message.from_user.id, "\U0001F4A1 Чтобы отправить контактную информацию, необходимо "
                                               "нажать на кнопку.")
