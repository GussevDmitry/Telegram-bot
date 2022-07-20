from loader import bot
from states.user_states import UserStateInfo
from telebot.types import Message
from keyboards.reply.send_contact import request_contact


@bot.message_handler(commands=['survey'])
def get_name(message: Message) -> None:
    bot.set_state(message.from_user.id, UserStateInfo.name, message.chat.id)
    bot.send_message(message.from_user.id, f"Приветствую, {message.from_user.username}! Введите Ваше имя.")


@bot.message_handler(state=UserStateInfo.name)
def get_age(message: Message) -> None:
    if message.text.isalpha() or map(lambda elem: elem.is_alpha(), message.text.split()):
        bot.send_message(message.from_user.id, "Запомнил. Введите Ваш возраст?")
        bot.set_state(message.from_user.id, UserStateInfo.age, message.chat.id)
    else:
        bot.send_message(message.from_user.id, "Имя не может содержать цифры.")

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text.strip()


@bot.message_handler(state=UserStateInfo.age)
def get_country(message: Message) -> None:
    if message.text.isdigit():
        bot.send_message(message.from_user.id, "Запомнил. Введите страну проживания.")
        bot.set_state(message.from_user.id, UserStateInfo.country, message.chat.id)
    else:
        bot.send_message(message.from_user.id, "Возраст не может содержать букв.")

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['age'] = message.text.strip()


@bot.message_handler(state=UserStateInfo.country)
def get_city(message: Message) -> None:
    bot.send_message(message.from_user.id, "Запомнил. Введите город проживания.")
    bot.set_state(message.from_user.id, UserStateInfo.city, message.chat.id)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['country'] = message.text.strip()


@bot.message_handler(state=UserStateInfo.city)
def get_phone_num(message: Message) -> None:
    bot.send_message(message.from_user.id, "Запомнил. Отправьте свой номер телефона нажав на кнопку.", reply_markup=request_contact())
    bot.set_state(message.from_user.id, UserStateInfo.phone_num, message.chat.id)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['city'] = message.text.strip()


@bot.message_handler(content_types=['text', 'contact'], state=UserStateInfo.phone_num)
def get_contact_info(message: Message) -> None:
    if message.content_type == 'contact':
        bot.set_state(message.from_user.id, UserStateInfo.info_collected, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['phone_number'] = message.contact.phone_number
            contact_info = f"Спасибо. Данные записал\n" \
                           f"Имя - {data['name']}\n" \
                           f"Возраст - {data['age']}\n" \
                           f"Страна проживания - {data['country']}\n" \
                           f"Город проживания - {data['city']}\n" \
                           f"Номер телефона - {data['phone_number']}"
            bot.send_message(message.from_user.id, contact_info)
            bot.send_message(message.chat.id, "Давайте приступим к подбору отеля для Вас. "
                                              "Чтобы ознакомиться с основными командами и их описанием, наберите /help")
    else:
        bot.send_message(message.from_user.id, "Чтобы отправить контактную информация необходимо нажать на кнопку.")