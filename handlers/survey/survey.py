from loader import bot
from states.user_states import UserStateInfo
from telebot.types import Message
from keyboards.reply.send_contact import request_contact
from database.create_database import db, User


@bot.message_handler(commands=['survey'])
def get_name(message: Message) -> None:
    bot.set_state(message.from_user.id, UserStateInfo.name, message.chat.id)
    bot.send_message(message.from_user.id, f"\U0001F6A9 Приветствую, {message.from_user.username}! Введите Ваше имя.")


@bot.message_handler(state=UserStateInfo.name)
def get_age(message: Message) -> None:
    if message.text.isalpha() or map(lambda elem: elem.is_alpha(), message.text.split()):
        bot.send_message(message.from_user.id, "\U0001F44D Запомнил. Введите Ваш возраст?")
        bot.set_state(message.from_user.id, UserStateInfo.age, message.chat.id)
    else:
        bot.send_message(message.from_user.id, "\U0001F4A1 Имя не может содержать цифры.")

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text.strip().lower().title()


@bot.message_handler(state=UserStateInfo.age)
def get_country(message: Message) -> None:
    if message.text.isdigit():
        bot.send_message(message.from_user.id, "\U0001F44D Запомнил. Введите страну проживания.")
        bot.set_state(message.from_user.id, UserStateInfo.country, message.chat.id)
    else:
        bot.send_message(message.from_user.id, "\U0001F4A1 Возраст не может содержать букв.")

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['age'] = message.text.strip()


@bot.message_handler(state=UserStateInfo.country)
def get_city(message: Message) -> None:
    bot.send_message(message.from_user.id, "\U0001F44D Запомнил. Введите город проживания.")
    bot.set_state(message.from_user.id, UserStateInfo.city, message.chat.id)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['country'] = message.text.strip().lower().title()


@bot.message_handler(state=UserStateInfo.city)
def get_phone_num(message: Message) -> None:
    bot.send_message(message.from_user.id, "\U0001F44D Запомнил. Отправьте свой номер телефона нажав на кнопку.",
                     reply_markup=request_contact())
    bot.set_state(message.from_user.id, UserStateInfo.phone_num, message.chat.id)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['city'] = message.text.strip().lower().title()


@bot.message_handler(content_types=['text', 'contact'], state=UserStateInfo.phone_num)
def get_contact_info(message: Message) -> None:
    if message.content_type == 'contact':
        bot.set_state(message.from_user.id, UserStateInfo.info_collected, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['phone_number'] = int(message.contact.phone_number[2:])
        contact_info = f"\U0001F64CСпасибо. Данные записал\n" \
                       f"Имя - {data['name']}\n" \
                       f"Возраст - {data['age']}\n" \
                       f"Страна проживания - {data['country']}\n" \
                       f"Город проживания - {data['city']}\n" \
                       f"Номер телефона - {data['phone_number']}"

        # Может быть разместить в отдельной функции...
        with db:
            help_query = User.select(User.phone_number)
            help_set = set()
            for i_num in help_query:
                help_set.add(i_num.phone_number)
            if int(message.contact.phone_number[2:]) not in help_set:
                User.create(name=data.get('name'), age=data.get('age'), country=data.get('country'),
                            city=data.get('city'), phone_number=data.get('phone_number'))
                bot.send_message(message.from_user.id, contact_info)
            else:
                bot.send_message(message.from_user.id, "Вы уже зарегистрированы! Вам доступен просмотр истории поиска."
                                                       "Для просмотра наберите команду /history")
            help_set = set()

        bot.send_message(message.chat.id, "Давайте приступим к подбору отеля для Вас. "
                                          "Чтобы ознакомиться с основными командами и их описанием, наберите /help")
    else:
        bot.send_message(message.from_user.id, "\U0001F4A1 Чтобы отправить контактную информация необходимо нажать на кнопку.")